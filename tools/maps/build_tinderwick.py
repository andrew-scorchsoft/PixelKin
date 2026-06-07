#!/usr/bin/env python3
"""
Build Tinderwick — the starter town — on the SHARED overworld set (the gold-standard area).

No longer bakes its own atlas: it references `vesper_overworld_set` (build_shared_overworld.py)
and paints terrain layers; mapkit.finalize() runs the autotiler (with variant scatter so
shorelines/tree-lines don't repeat), strips the terrain layers, renders and validates.

Redesigned to the level-design §7.1 target (28×24, blue-hour coastal village): an organic
2-deep tree-line with a north exit, a lit path spine from the exit down to the shore, a
plaza with the shop + Lumenary, the player's cottage lower-left, a small ornamental POND
inland, a fenced flower garden, a tall-grass verge by the exit, and a sand beach + sea to
the south with lantern-buoys. Scatter decor breaks the field.

DOOR ALIGNMENT (the core fix): every enterable building's interact-warp sits on the actual
door-art tile, with the tile directly BELOW it walkable and on the path.
  * cottage  (5 wide): door art = col 2  -> door tile (tx0+2, ty_bottom)
  * shop     (5 wide): door art = col 2  -> door tile (tx0+2, ty_bottom)
  * lumenary (6 wide): grand arch centred across cols 2-3 -> BOTH tiles are walkable
    approach tiles; the interact-warp sits on the left door tile (col 2), col 3 is also
    clear, and the street runs directly below both. (See _doors below; verify in the render.)

STORY (walkthrough/01-south.md): the mentor is Star-tender **Fenn** (intro cutscene gifts
the vesperlamp + starter); the young NPC is the rival **Wren** (sprite key `wren`).

Run:  python3 tools/maps/build_tinderwick.py
Prereq: python3 tools/maps/build_shared_overworld.py  (the shared set must exist).
"""
from __future__ import annotations
import json, random
import mapkit as mk
from mapkit import gid

W, H = 28, 24
rng = random.Random(7)

# ---- building footprints (top-left anchor) + measured door columns -----------
# door tile = (at.tx + door_col, at.ty + h - 1); approach tile = one row below that.
SHOP = {"at": (3, 4), "w": 5, "h": 4, "door_col": 2}
LUMENARY = {"at": (17, 2), "w": 6, "h": 6, "door_col": 2}   # arch straddles cols 2-3
COTTAGE = {"at": (4, 12), "w": 5, "h": 5, "door_col": 2}

def door_tile(b):
    return (b["at"][0] + b["door_col"], b["at"][1] + b["h"] - 1)

shop_door = door_tile(SHOP)          # (5, 7)
lum_door = door_tile(LUMENARY)       # (19, 7)  -- col 3 == (20,7) is the twin door tile
cottage_door = door_tile(COTTAGE)    # (6, 16)
lum_door_r = (lum_door[0] + 1, lum_door[1])   # (20, 7) walkable twin (grand double entrance)

# ---- terrain presence grids -------------------------------------------------
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(5, 4, 1), (24, 4, 1), (3, 9, 1), (25, 11, 1), (3, 18, 1)])
for x in (13, 14):                       # punch the north exit gap
    tree[0 * W + x] = 0; tree[1 * W + x] = 0
mk.rect(tree, W, H, 0, 19, W - 1, H - 1, 0)   # clear the border below the shoreline

water_sea = mk.make_grid(W, H)
mk.rect(water_sea, W, H, 0, 22, W - 1, H - 1)            # full-width sea (continues off bottom)
pond = mk.make_grid(W, H)
mk.rect(pond, W, H, 22, 12, 25, 14)                      # small inland ornamental pond (right side)
sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 0, 19, W - 1, 21)                    # 3-row beach
tallgrass = mk.make_grid(W, H)
mk.rect(tallgrass, W, H, 10, 2, 15, 3)                   # verge straddling the exit lane

# ---- the lit path spine + approach lanes to every door ----------------------
path = mk.make_grid(W, H)
mk.vline(path, W, H, 13, 2, 18); mk.vline(path, W, H, 14, 2, 18)  # N–S spine (2 wide)
mk.hline(path, W, H, 8, 5, 21)                            # plaza street along the building fronts
# shop approach: door (5,7) -> below (5,8) is on the street row (8). add the stub up to it.
path[8 * W + shop_door[0]] = 1
# lumenary approach: doors (19,7)/(20,7) -> below row 8 on the street.
path[8 * W + lum_door[0]] = 1
path[8 * W + lum_door_r[0]] = 1
# cottage lane: door (6,16) -> down to the spine. carve a vertical lane.
mk.vline(path, W, H, cottage_door[0], cottage_door[1] + 1, 18)   # (6, 17..18)
mk.hline(path, W, H, 18, 6, 14)                                  # join cottage lane to the spine

# ---- base = full grass scatter; terrain layers mesh over it -----------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_pond", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": pond},
    {"name": "t_sea", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water_sea},
]

# ---- objects: buildings, standalone trees, lamps (walk-under) ----------------
objects = [
    {"id": "shop", "sprite": "tinderwick_shop", "at": {"tx": SHOP["at"][0], "ty": SHOP["at"][1]},
     "w": SHOP["w"], "h": SHOP["h"], "overhang": 2},
    {"id": "lumenary", "sprite": "tinderwick_lumenary", "at": {"tx": LUMENARY["at"][0], "ty": LUMENARY["at"][1]},
     "w": LUMENARY["w"], "h": LUMENARY["h"], "overhang": 3},
    {"id": "house", "sprite": "tinderwick_cottage", "at": {"tx": COTTAGE["at"][0], "ty": COTTAGE["at"][1]},
     "w": COTTAGE["w"], "h": COTTAGE["h"], "overhang": 3},
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 9, "ty": 10}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 24, "ty": 16}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 5}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 15, "ty": 13}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 18}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = set()
for o in objects:
    for yy in range(o["at"]["ty"], o["at"]["ty"] + o["h"]):
        for xx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
            building_cells.add((xx, yy))

# cells the player can't decorate over: any terrain + building footprints
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, water_sea, pond, sand, tallgrass, path))}
avoid = covered | building_cells

# ---- deco: flowers garden + signs (beside the path) + scatter + buoys --------
deco = mk.make_grid(W, H)
for (x, y) in [(8, 11), (10, 11), (9, 12), (8, 13)]:             # small fenced flower garden (left, off-path)
    deco[y * W + x] = gid("flowers")
for (x, y) in [(7, 10), (11, 10), (7, 14), (11, 14)]:            # garden fence posts
    deco[y * W + x] = gid("fence")
# Signs sit immediately BESIDE the path the player walks, never mid-field:
sign_tiles = {
    "sign_shop": (4, 8),       # left of the shop door, on the plaza street
    "sign_lumenary": (21, 8),  # right of the Lumenary door, on the plaza street
    "sign_mentor": (12, 11),   # on the spine, by Fenn
    "sign_dock": (15, 18),     # by the shore-bound lane
}
for (x, y) in sign_tiles.values():
    deco[y * W + x] = gid("sign")
for (x, y) in [(7, 20), (16, 20), (21, 20)]:                     # lantern-buoys on the shore
    deco[y * W + x] = gid("buoy")
mk.scatter_decor(deco, base, W, H, rng, density=0.10, avoid=avoid)

# ---- assemble ---------------------------------------------------------------
m = {
    "id": "tinderwick", "display_name": "Tinderwick", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        {"id": "to_coast", "at": {"tx": 13, "ty": 0}, "trigger": "step_on",
         "to_map": "dimglass_coast", "to": {"tx": 6, "ty": 32}, "facing": "up", "transition": "fade"},
        {"id": "to_coast_e", "at": {"tx": 14, "ty": 0}, "trigger": "step_on",
         "to_map": "dimglass_coast", "to": {"tx": 7, "ty": 32}, "facing": "up", "transition": "fade"},
        # House door — interact on the actual door-art tile (cottage col 2).
        {"id": "to_house", "at": {"tx": cottage_door[0], "ty": cottage_door[1]}, "trigger": "interact",
         "to_map": "tinderwick_house", "to": {"tx": 6, "ty": 7}, "facing": "down", "transition": "door"},
        # Shop door — interact on the shop's door-art tile (col 2).
        {"id": "to_shop", "at": {"tx": shop_door[0], "ty": shop_door[1]}, "trigger": "interact",
         "to_map": "tinderwick_shop", "to": {"tx": 6, "ty": 7}, "facing": "down", "transition": "door"},
        # Lumenary door — interact on the arch door-art tile (col 2); col 3 is the twin
        # walkable approach tile. Requires the player to hold a starter (soft gate).
        {"id": "to_lumenary", "at": {"tx": lum_door[0], "ty": lum_door[1]}, "trigger": "interact",
         "to_map": "tinderwick_lumenary", "to": {"tx": 7, "ty": 9}, "facing": "down",
         "requires_flag": "flag:has_starter", "transition": "door"},
    ],
    "triggers": [
        {"id": "intro_mentor", "kind": "cutscene", "at": {"tx": 13, "ty": 11},
         "activation": "step_on", "ref": "script.intro_mentor", "once": True,
         "sets_flags": ["flag:has_vesperlamp", "flag:has_starter"]},
        {"id": "sign_shop", "kind": "sign", "at": {"tx": sign_tiles["sign_shop"][0], "ty": sign_tiles["sign_shop"][1]},
         "activation": "interact", "ref": "sign.tinderwick_square"},
        {"id": "sign_lumenary", "kind": "sign", "at": {"tx": sign_tiles["sign_lumenary"][0], "ty": sign_tiles["sign_lumenary"][1]},
         "activation": "interact", "ref": "sign.tinderwick_lumenary"},
        {"id": "sign_mentor", "kind": "sign", "at": {"tx": sign_tiles["sign_mentor"][0], "ty": sign_tiles["sign_mentor"][1]},
         "activation": "interact", "ref": "sign.tinderwick_mentor"},
        {"id": "sign_dock", "kind": "sign", "at": {"tx": sign_tiles["sign_dock"][0], "ty": sign_tiles["sign_dock"][1]},
         "activation": "interact", "ref": "sign.tinderwick_dock"},
    ],
    "encounters": [
        {"id": "verge_grass", "terrain": "tall_grass", "rect": {"tx": 10, "ty": 2, "w": 6, "h": 2},
         "encounter_rate": 0.07,
         "table": [{"kin_id": 16, "weight": 60, "min_level": 2, "max_level": 4},
                   {"kin_id": 10, "weight": 40, "min_level": 2, "max_level": 3}]}],
    "npcs": [
        # Star-tender Fenn — the mentor, on the spine; the intro cutscene fires just north of him.
        {"id": "mentor", "at": {"tx": 13, "ty": 12}, "facing": "down", "sprite": "npc_mentor",
         "movement": "static", "dialogue_ref": "npc.mentor_intro"},
        # Wren — the rival, a fellow young Wayfarer milling in the plaza.
        {"id": "wren", "at": {"tx": 17, "ty": 13}, "facing": "left", "sprite": "wren",
         "movement": "wander", "dialogue_ref": "npc.wren_intro"}],
    "gates": [], "music": "assets/audio/music/tinderwick-a.mp3",
    "_doors": {"shop": shop_door, "lumenary": lum_door, "lumenary_twin": lum_door_r,
               "house": cottage_door},
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
