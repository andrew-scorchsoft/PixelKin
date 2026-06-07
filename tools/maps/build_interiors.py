#!/usr/bin/env python3
"""
Rebuild ALL of PixelKin's building interiors to the binding spec in docs/world/interiors.md:
cosy 16-bit SNES-era top-down rooms with walls that have a VISIBLE FACE (a wall_cap cornice
row above a wall_face row on top, one face tile on the sides, faced corners), a PATTERNED
floor, a bordered RUG, perimeter FURNITURE (interior_* objects), ONE focal point at top-centre,
a single doormat exit centre-bottom, ≥1 window/banner on the top face, and clear walkable lanes.

Two accent registers, both packed by pack_tileset.py:
  WARM  interior_set        (wood/plaster)  -> homes, shops, inns
  COOL  interior_stone_set  (stone/dark panel) -> Lumenaries (a shrine, never a cabin)

Big props are interior_* OBJECTS (pack_objects.py), placed via the map `objects` array; their
footprint collides unless solid:false (the rug). Walls + furniture collide; floor/rug/doormat
walk-on. After building, every doormat tile, every NPC `at` tile, and the door->NPC/trigger lane
is walkable (verified by EYE via render_map.py — see the NOTE below).

NOTE: validate_map.py is the OVERWORLD gate (needs terrain/autotile vocab interiors lack); the
interiors are checked by render_map.py (/tmp/<id>.png), the acceptance pattern in interiors.md §4.

Run:  python3 tools/maps/build_interiors.py
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public/assets/maps"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

# --- tileset refs (first_gid=1) -------------------------------------------------
# WARM interior_set local indices: 0 floor 1 floor_b 2 doormat 3 cap 4 face 5 corner 6 wall_s 7 window
# COOL interior_stone_set:         0 floor 1 floor_b 2 runner 3 cap 4 face 5 corner 6 wall_s 7 banner
WARM_SET = {
    "name": "interior_set", "image": "assets/tilesets/interior_set.webp",
    "tile_width": 16, "tile_height": 16, "first_gid": 1, "columns": 8, "tile_count": 8,
}
COOL_SET = {
    "name": "interior_stone_set", "image": "assets/tilesets/interior_stone_set.webp",
    "tile_width": 16, "tile_height": 16, "first_gid": 1, "columns": 8, "tile_count": 8,
}
# gids = local index + 1
FLOOR, FLOOR_B, DOORMAT, CAP, FACE, CORNER, WALL_S, WINDOW = 1, 2, 3, 4, 5, 6, 7, 8
RUNNER, BANNER = 3, 8  # cool-set aliases for indices 2 and 7


def grid(w, h, fill=0):
    return [fill] * (w * h)


def rect(g, w, x0, y0, x1, y1, val):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g[y * w + x] = val


def faced_room(W, H, door_x, floor_fill=FLOOR, floor_alt=FLOOR_B):
    """Return (base, over) tile layers for a faced room.

    base = floor + bottom wall + doormat (depth 0).
    over = the upper wall frame drawn ABOVE objects so furniture tucks under the wall
           (cap row 0, face row 1, side faces, faced corners). depth high.
    Layout (interiors.md §0):
      row 0          : wall_cap  (cornice), corners at the two ends
      row 1          : wall_face (visible vertical face), corners at the two ends
      rows 2..H-2    : side wall_face on col 0 / col W-1, floor between
      row H-1        : wall_s, faced corners, doormat at door_x
    """
    base = grid(W, H, floor_fill)
    over = grid(W, H, 0)
    # checker the floor with the alt variant for a patterned (not flat) look
    for y in range(2, H - 1):
        for x in range(1, W - 1):
            if (x + y) % 2 == 0:
                base[y * W + x] = floor_alt
    # top frame: cap row + face row (the HEIGHT)
    for x in range(W):
        over[0 * W + x] = CAP
        over[1 * W + x] = FACE
    over[0 * W + 0] = CORNER
    over[0 * W + (W - 1)] = CORNER
    over[1 * W + 0] = CORNER
    over[1 * W + (W - 1)] = CORNER
    # side faces
    for y in range(2, H - 1):
        over[y * W + 0] = FACE
        over[y * W + (W - 1)] = FACE
    # bottom wall + faced corners + doormat
    for x in range(W):
        over[(H - 1) * W + x] = WALL_S
    over[(H - 1) * W + 0] = CORNER
    over[(H - 1) * W + (W - 1)] = CORNER
    base[(H - 1) * W + door_x] = DOORMAT
    over[(H - 1) * W + door_x] = 0  # doormat shows through the bottom wall (the exit gap)
    return base, over


def windows(over, W, cols, tile=WINDOW):
    for c in cols:
        over[1 * W + c] = tile  # windows sit on the top wall-FACE row (row 1)


def mapdef(id_, name, W, H, tileset, base, over, objects, warps, triggers, npcs, music):
    return {
        "id": id_, "display_name": name,
        "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "interior",
        "tilesets": [tileset],
        "layers": [
            # The wall frame is a normal (non-`above`) layer so its `collides` tiles
            # actually block movement (CollisionGrid skips `above` layers). Furniture
            # objects render over it. depth 5 = above the floor, below objects.
            {"name": "base", "role": "base", "depth": 0, "data": base},
            {"name": "walls", "role": "deco", "depth": 5, "data": over},
        ],
        "objects": objects,
        "warps": warps, "triggers": triggers, "encounters": [], "npcs": npcs,
        "gates": [], "music": music,
    }


def obj(id_, sprite, tx, ty, w, h, overhang=0, solid=True):
    o = {"id": id_, "sprite": sprite, "at": {"tx": tx, "ty": ty}, "w": w, "h": h}
    if overhang:
        o["overhang"] = overhang
    if not solid:
        o["solid"] = False
    return o


# =============================================================================
#  LUMENARIES (cool register, shrine) — tinderwick & pearlmoor
# =============================================================================
def build_lumenary(id_, name, music, out_warp, script_ref, sign_ref, warden_id, warden_dialogue):
    W, H = 14, 11
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x, floor_fill=FLOOR, floor_alt=FLOOR_B)
    # banners flank the centre on the top wall-face; a window between would break symmetry,
    # so use two banners (interiors.md §2: banners on the top wall-face).
    windows(over, W, [door_x - 2, door_x + 2], tile=BANNER)
    # runner rug aisle from the doormat up to the altar dais (centre column, walk-on)
    for y in range(2, H - 1):
        base[y * W + door_x] = RUNNER

    objects = [
        # focal altar/lamp-shrine at top-centre (its glowing lantern overhangs into the face)
        obj("altar", "interior_altar", door_x - 1, 2, 3, 3, overhang=1),
        # braziers flanking the aisle (two pairs) — warm light
        obj("brazier_l1", "interior_brazier", door_x - 3, 5, 1, 2, overhang=1),
        obj("brazier_r1", "interior_brazier", door_x + 3, 5, 1, 2, overhang=1),
        obj("brazier_l2", "interior_brazier", door_x - 3, 8, 1, 2, overhang=1),
        obj("brazier_r2", "interior_brazier", door_x + 3, 8, 1, 2, overhang=1),
    ]
    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": out_warp[0], "to": {"tx": out_warp[1], "ty": out_warp[2]},
         "facing": "down", "transition": "door"},
    ]
    triggers = [
        # step-on bond-test trigger sits on the aisle just south of where the warden stands
        {"id": "lumenary_battle", "kind": "cutscene", "at": {"tx": door_x, "ty": 6},
         "activation": "step_on", "ref": script_ref, "once": True,
         "requires_flag": "flag:has_starter"},
        {"id": "sign_lumenary", "kind": "sign", "at": {"tx": 2, "ty": 2}, "activation": "interact",
         "ref": sign_ref},
    ]
    npcs = [
        # the warden stands at the foot of the altar dais (row 5, just below the 3x3 altar)
        {"id": warden_id, "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static", "dialogue_ref": warden_dialogue},
    ]
    return mapdef(id_, name, W, H, COOL_SET, base, over, objects, warps, triggers, npcs, music)


# =============================================================================
#  SHOPS (warm) — tinderwick & pearlmoor
# =============================================================================
def build_shop(id_, name, music, out_warp, sign_ref, keeper_id, keeper_dialogue):
    W, H = 12, 9
    door_x = W // 2  # tx 6
    base, over = faced_room(W, H, door_x)
    windows(over, W, [2, W - 3])
    # rug FIRST (drawn under furniture) then props on top.
    objects = [
        # bordered rug staging the goods, centre-front
        obj("rug", "interior_rug", door_x - 2, 5, 3, 2, solid=False),
        # counter spanning near the top-centre, shopkeeper stands behind (above) it
        obj("counter", "interior_counter", door_x - 1, 3, 3, 2),
        # wares: shelves + barrels along the side walls
        obj("shelf_l", "interior_shelf", 1, 2, 2, 2),
        obj("shelf_r", "interior_shelf", W - 3, 2, 2, 2),
        obj("barrels_l", "interior_barrels", 1, 6, 2, 1),
        obj("barrels_r", "interior_barrels", W - 3, 6, 2, 1),
    ]
    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": out_warp[0], "to": {"tx": out_warp[1], "ty": out_warp[2]},
         "facing": "down", "transition": "door"},
    ]
    triggers = [
        # a wares sign on the right wall side, on a clear floor-adjacent tile
        {"id": "sign_wares", "kind": "sign", "at": {"tx": W - 2, "ty": 5}, "activation": "interact",
         "ref": sign_ref},
    ]
    npcs = [
        # behind the counter (counter occupies ty 3-4; keeper at ty 2, the wall-face is row 1 so 2 is floor)
        {"id": keeper_id, "at": {"tx": door_x, "ty": 2}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static", "dialogue_ref": keeper_dialogue},
    ]
    return mapdef(id_, name, W, H, WARM_SET, base, over, objects, warps, triggers, npcs, music)


# =============================================================================
#  INN (warm) — pearlmoor
# =============================================================================
def build_inn():
    W, H = 14, 10
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [2, W - 3])
    # Layout keeps a clear horizontal corridor at row 3 and a clear vertical lane up the
    # centre; beds sit lower-left (rows 5-7), tables lower-right, so no region is sealed.
    objects = [
        obj("rug", "interior_rug", door_x - 1, 6, 3, 2, solid=False),
        # focal hearth top-centre with braziers hugging it
        obj("hearth", "interior_hearth", door_x - 1, 2, 2, 2),
        obj("brazier_l", "interior_brazier", door_x - 2, 2, 1, 2, overhang=1),
        obj("brazier_r", "interior_brazier", door_x + 2, 2, 1, 2, overhang=1),
        # a row of beds along the lower-left wall
        obj("bed1", "interior_bed", 1, 5, 2, 3),
        obj("bed2", "interior_bed", 3, 5, 2, 3),
        # tables in the common room (lower-right)
        obj("table1", "interior_table", W - 4, 4, 2, 2),
        obj("table2", "interior_table", W - 4, 7, 2, 2),
    ]
    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 22, "ty": 12}, "facing": "down", "transition": "door"},
    ]
    triggers = [
        # welcome sign on the right wall side at a clear, reachable tile
        {"id": "sign_welcome", "kind": "sign", "at": {"tx": W - 2, "ty": 3}, "activation": "interact",
         "ref": "sign.pearlmoor_welcome"},
    ]
    npcs = [
        {"id": "innkeep", "at": {"tx": 2, "ty": 3}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static", "dialogue_ref": "npc.pearlmoor_innkeep"},
        {"id": "fisher", "at": {"tx": W - 5, "ty": 5}, "facing": "right",
         "sprite": "wren", "movement": "static", "dialogue_ref": "npc.pearlmoor_fisher"},
    ]
    return mapdef("pearlmoor_inn", "Pearlmoor Quayside Inn", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/dimglass-coast-a.mp3")


# =============================================================================
#  HOME (warm cosy) — tinderwick_house
# =============================================================================
def build_house():
    W, H = 12, 9
    door_x = W // 2  # tx 6
    base, over = faced_room(W, H, door_x)
    windows(over, W, [2, W - 3])
    objects = [
        # rug FIRST (under the table), then props
        obj("rug", "interior_rug", door_x - 2, 5, 3, 2, solid=False),
        # focal hearth top-centre
        obj("hearth", "interior_hearth", door_x - 1, 2, 2, 2),
        obj("bookcase", "interior_bookcase", 1, 2, 2, 2),
        obj("bed", "interior_bed", W - 3, 2, 2, 3),
        obj("table", "interior_table", door_x - 1, 5, 2, 2),
        obj("barrels", "interior_barrels", 1, 6, 2, 1),
    ]
    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 6, "ty": 17}, "facing": "down", "transition": "door"},
    ]
    triggers = [
        {"id": "sign_shelf", "kind": "sign", "at": {"tx": 2, "ty": 2}, "activation": "interact",
         "ref": "sign.house_shelf"},
    ]
    npcs = [
        {"id": "house_parent", "at": {"tx": W - 4, "ty": 6}, "facing": "down",
         "sprite": "npc_parent", "movement": "static", "dialogue_ref": "npc.house_parent"},
    ]
    return mapdef("tinderwick_house", "Apprentice's House", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/tinderwick-b.mp3")


def write_and_render(m):
    path = MAPS / f"{m['id']}.json"
    path.write_text(json.dumps(m, indent=2) + "\n")
    out = Path("/tmp") / f"{m['id']}.png"
    subprocess.run([sys.executable, str(SCRIPTS / "render_map.py"), str(path),
                    "--output", str(out), "--scale", "5"], capture_output=True)
    print(f"  wrote {path.relative_to(REPO)}  ->  rendered {out}")


def all_maps():
    return [
        build_house(),
        build_shop("tinderwick_shop", "Tinderwick General Store",
                   "assets/audio/music/tinderwick-b.mp3", ("tinderwick", 5, 8),
                   "sign.tinderwick_shop_wares", "shopkeeper", "npc.tinderwick_shopkeeper"),
        build_lumenary("tinderwick_lumenary", "Tinderwick Lumenary",
                       "assets/audio/music/tinderwick-a.mp3", ("tinderwick", 19, 8),
                       "script.lumenary_tinderwick", "sign.tinderwick_lumenary_inside",
                       "brisa", "npc.brisa_tallow"),
        build_lumenary("pearlmoor_lumenary", "Pearlmoor Tide Lumenary",
                       "assets/audio/music/dimglass-coast-a.mp3", ("pearlmoor_quay", 14, 7),
                       "script.lumenary_pearlmoor", "sign.pearlmoor_lumenary",
                       "reyl", "npc.reyl_wash"),
        build_shop("pearlmoor_shop", "Pearlmoor Chandlery",
                   "assets/audio/music/dimglass-coast-a.mp3", ("pearlmoor_quay", 5, 12),
                   "sign.pearlmoor_shop", "chandler", "npc.pearlmoor_shopkeeper"),
        build_inn(),
    ]


if __name__ == "__main__":
    for m in all_maps():
        write_and_render(m)
    print("DONE")
