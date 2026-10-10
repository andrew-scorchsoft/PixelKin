#!/usr/bin/env python3
"""
Build Tinderwick — the starter town — on the SHARED overworld set (the gold-standard area).

No longer bakes its own atlas: it references `vesper_overworld_set` (build_shared_overworld.py)
and paints terrain layers; mapkit.finalize() runs the autotiler (with variant scatter so
shorelines/tree-lines don't repeat), strips the terrain layers, renders and validates.

Redesigned to the level-design §7.1 target (28×24, blue-hour coastal village): an organic
2-deep tree-line with a north exit, a lit path spine from the exit down to the shore, a
plaza with the player's cottage + Lumenary, the general store down the lower-left lane
(R8, 2026-10: the two SWAPPED — see SHOP/COTTAGE below), a small ornamental POND
inland, a fenced flower garden, a tall-grass verge by the exit, and a sand beach + sea to
the south with lantern-buoys. Scatter decor breaks the field.

R8 also opened a WEST hedge gap off the square to Duskapple Orchard
(build_duskapple_orchard.py — the courier's cart now holds Fenn's satchel; Wren waits
there) and made this builder the FULL source of truth: the post-build additions that used
to live only in the shipped JSON (vigil host warp + scar, the verge's day-form twin, the
letter NPC, the townguide, Andrew, the wick purse, door blocked_refs) are authored here,
so re-running it no longer regresses anything.

DOOR ALIGNMENT (the core fix): every enterable building's door warp sits on the actual
door-art tile, with the tile directly BELOW it walkable and on the path.
  * cottage  (5 wide): door art = col 2  -> door tile (tx0+2, ty_bottom)
  * shop     (5 wide): door art = col 2  -> door tile (tx0+2, ty_bottom)
  * lumenary (6 wide): grand arch centred across cols 2-3 -> BOTH tiles are walkable
    approach tiles; the interact-warp sits on the left door tile (col 2), col 3 is also
    clear, and the street runs directly below both. (See _doors below; verify in the render.)

STORY (walkthrough/01-south.md): the opening is the SATCHEL ERRAND — Star-tender **Fenn**
waits at the Vesper Crossroads waystone (build_crossroads.py) and the lamp+starter ceremony
happens THERE once his satchel comes home from the store. In town: the north gate-warden
turns an unstarted player back (script.gate_warden + has_starter-gated coast warps), and
everyone points east. The rival **Wren** (sprite key `wren`) is out in the orchard (R8).

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
# R8 "the town remembers it differently" (2026-10): the shop and the apprentice's
# cottage SWAPPED places — the cottage now fronts the square (NW) and the store
# sits down the lower-left lane. The door TILES are exactly swapped too: (5,7) used
# to be the store, (6,16) used to be home. A first-timer sees an ordinary village;
# a returning player walks "home" into the shop.
SHOP = {"at": (4, 13), "w": 5, "h": 4, "door_col": 2}
LUMENARY = {"at": (17, 2), "w": 6, "h": 6, "door_col": 2}   # arch straddles cols 2-3
COTTAGE = {"at": (3, 3), "w": 5, "h": 5, "door_col": 2}

def door_tile(b):
    return (b["at"][0] + b["door_col"], b["at"][1] + b["h"] - 1)

shop_door = door_tile(SHOP)          # (6, 16)
lum_door = door_tile(LUMENARY)       # (19, 7)  -- col 3 == (20,7) is the twin door tile
cottage_door = door_tile(COTTAGE)    # (5, 7)
lum_door_r = (lum_door[0] + 1, lum_door[1])   # (20, 7) walkable twin (grand double entrance)

# ---- terrain presence grids -------------------------------------------------
# Composition per level-design §11: a DEEP organic enclosure (the camera margin is
# always forest/cliff/sea, never flat void), one elevation accent (the NE cliff
# terrace behind the Lumenary), and organic — not ruled — shores and patches.
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(9, 2, 1), (25, 11, 2), (3, 18, 2),
                         (26, 16, 1), (2, 13, 1)])
for x in (13, 14):                       # punch the north exit gap
    tree[0 * W + x] = 0; tree[1 * W + x] = 0
mk.rect(tree, W, H, 0, 19, W - 1, H - 1, 0)   # clear the border below the shoreline
# Seal the SW border slivers the bump shapes leave: walkable-looking cells with
# no approach (the cottage + tree bodies enclose them). A pocket the player can
# SEE but never reach is a broken promise — fill it with forest instead.
for (x, y) in ((2, 11), (3, 12), (2, 15), (3, 15), (2, 16)):
    tree[y * W + x] = 1
# R8: the WEST gap — the plaza street runs straight out through the hedge to
# Duskapple Orchard (build_duskapple_orchard.py). (The old (3,9) border bump
# that walled this side is gone.)
for y in (8, 9):
    for x in range(0, 5):
        tree[y * W + x] = 0
# ...and the cottage now backs onto the north treeline: fill the strip behind
# and beside it with forest (render_walkable flagged the 10-tile orphan pocket
# it left — seen-but-unreachable ground is a broken promise).
for x in range(2, 8):
    tree[2 * W + x] = 1
for y in range(3, 7):
    tree[y * W + 2] = 1

# NE cliff terrace — the town's elevation accent, rising behind the Lumenary so the
# landmark sits against rock, not empty field (the reference-map "terrace" read).
cliff = mk.make_grid(W, H)
mk.rect(cliff, W, H, 23, 0, W - 1, 2)
mk.blob(cliff, W, H, 25, 3, 2.2, 1.2)
mk.rect(tree, W, H, 23, 0, W - 1, 4, 0)       # cliff replaces the tree border here

water_sea = mk.make_grid(W, H)
mk.rect(water_sea, W, H, 0, 22, W - 1, H - 1)            # full-width sea (continues off bottom)
mk.blob(water_sea, W, H, 4, 22, 2.6, 1.4)                # the tideline bites the beach…
mk.blob(water_sea, W, H, 19, 22, 3.0, 1.4)
pond = mk.make_grid(W, H)
mk.rect(pond, W, H, 22, 12, 25, 14)                      # small inland ornamental pond (right side)
sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 0, 19, W - 1, 21)                    # 3-row beach
mk.blob(sand, W, H, 7, 18, 2.4, 1.2)                     # dunes lap up into the green
mk.blob(sand, W, H, 22, 18, 2.0, 1.2)
tallgrass = mk.make_grid(W, H)
# R8: the verge sits one column further east than it used to (11-16, not 10-15)
mk.rect(tallgrass, W, H, 11, 2, 16, 4)                   # verge straddling the exit lane
for (x, y) in ((11, 2), (16, 2), (11, 4), (16, 4)):      # clipped corners -> organic patch
    tallgrass[y * W + x] = 0

# ---- the lit path spine + approach lanes to every door ----------------------
path = mk.make_grid(W, H)
mk.vline(path, W, H, 13, 2, 18); mk.vline(path, W, H, 14, 2, 18)  # N–S spine (2 wide)
mk.hline(path, W, H, 8, 5, 21)                            # plaza street along the building fronts
# the plaza street is TWO rows deep (8-9) — a square, not a footpath — so the
# building fronts open onto a real town apron (the reference-town read).
mk.rect(path, W, H, 5, 8, 21, 9)
# R8: ...and on out WEST through the hedge gap to the orchard
mk.rect(path, W, H, 0, 8, 4, 9)
# cottage approach: door (5,7) -> below (5,8) is on the street row (8).
path[8 * W + cottage_door[0]] = 1
# lumenary approach: doors (19,7)/(20,7) -> below row 8 on the street.
path[8 * W + lum_door[0]] = 1
path[8 * W + lum_door_r[0]] = 1
# store lane: door (6,16) -> down to the spine. carve a vertical lane.
mk.vline(path, W, H, shop_door[0], shop_door[1] + 1, 18)   # (6, 17..18)
mk.hline(path, W, H, 18, 6, 14)                            # join the store lane to the spine
# the Lanternway: a lane east below the garden, out to Vesper Crossroads (graph.ts
# tinderwick <-> vesper_crossroads). Runs under tree_d's crown (walk-under rows).
mk.hline(path, W, H, 16, 14, W - 1)
for x in (W - 2, W - 1):                                          # punch the east border
    tree[16 * W + x] = 0
# the BEACON approach: a short spur from the plaza street to the old lamp-tower's
# foot door on the NE bluff (the tower object stands over the cliff terrace)
mk.hline(path, W, H, 8, 22, 24)
path[7 * W + 24] = 1

# ---- base = full grass scatter; terrain layers mesh over it -----------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_pond", "role": "terrain", "terrain": "pond",
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
    # THE OLD BEACON — the town's tower, standing on the NE cliff terrace. Its
    # foot door is wick-locked until the Dimglass lamplighter's key comes home.
    {"id": "beacon", "sprite": "tinderwick_beacon", "at": {"tx": 23, "ty": 0},
     "w": 4, "h": 7, "overhang": 3},
    # Object trees with REAL crowns are scattered along the tree-line and pond so the
    # forest reads as overlapping canopies, not one repeating hedge tile (§11).
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 9, "ty": 12}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 24, "ty": 15}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 0, "ty": 4}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_d", "sprite": "tinderwick_tree", "at": {"tx": 16, "ty": 14}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_e", "sprite": "tinderwick_tree", "at": {"tx": 1, "ty": 11}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_f", "sprite": "tinderwick_tree", "at": {"tx": 25, "ty": 7}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_g", "sprite": "tinderwick_tree", "at": {"tx": 8, "ty": 0}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_h", "sprite": "tinderwick_tree", "at": {"tx": 1, "ty": 16}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 9, "ty": 5}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 15, "ty": 13}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 15, "ty": 18}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_d", "sprite": "tinderwick_lamp_post", "at": {"tx": 22, "ty": 8}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # Vigil I host scar (06-postgame R3 — was a post-build surgical addition,
    # now owned by the builder so a rebuild can't regress it).
    {"id": "vigil_scar_hearthfall", "sprite": "vigil_star_scar", "at": {"tx": 25, "ty": 8},
     "w": 1, "h": 1, "solid": False, "requires_flag": "flag:dawn"},
]
building_cells = set()
for o in objects:
    if not o.get("solid", True):
        continue
    for yy in range(o["at"]["ty"], o["at"]["ty"] + o["h"]):
        for xx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
            building_cells.add((xx, yy))

# cells the player can't decorate over: any terrain + building footprints
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, cliff, water_sea, pond, sand, tallgrass, path))}
avoid = covered | building_cells

# ---- deco: fenced flower garden + signs (beside the path) + scatter + buoys --
deco = mk.make_grid(W, H)
# A proper fenced flower garden (east of the spine, below the Lumenary square):
# slat fence top + bottom with end posts, flowerbeds inside, open east mouth.
mk.fence_run(deco, W, H, 16, 10, 19)
mk.fence_run(deco, W, H, 16, 13, 19)
deco[11 * W + 16] = gid("fence_post")
deco[12 * W + 16] = gid("fence_post")
for (x, y) in [(17, 11), (18, 11), (17, 12), (18, 12)]:
    deco[y * W + x] = gid("flowerbed_a") if (x + y) % 2 else gid("flowerbed_b")
deco[11 * W + 19] = gid("flowers")
# Signs sit immediately BESIDE the path the player walks, never mid-field:
# R8: the old "TINDERWICK SQUARE" board (4,8) and the DOCKS sign (15,18) are
# gone; the store wears its own sign down its new lane, and a fingerboard at
# the west gap names the orchard.
sign_tiles = {
    "sign_store": (7, 17),     # right of the store's door lane
    "sign_orchard": (3, 10),   # under the west street, at the hedge gap
    "sign_lumenary": (21, 8),  # right of the Lumenary door, on the plaza street
    "sign_mentor": (12, 11),   # on the spine
    "sign_lanternway": (21, 15),  # beside the east lane, pointing to the Crossroads
    "sign_beacon": (23, 7),       # at the beacon's foot, beside the door spur
}
for (x, y) in sign_tiles.values():
    deco[y * W + x] = gid("sign")
for (x, y) in [(7, 20), (16, 20), (21, 20)]:                     # lantern-buoys on the shore
    deco[y * W + x] = gid("buoy")
for (x, y) in [(2, 21), (25, 20), (11, 20)]:                     # shore boulders
    deco[y * W + x] = gid("boulder")
for (x, y) in [(23, 11), (26, 13)]:                              # pondside rocks
    deco[y * W + x] = gid("boulder")
mk.scatter_decor(deco, base, W, H, rng, density=0.16, avoid=avoid)

# ---- assemble ---------------------------------------------------------------
# The verge's tables: the journey band, and its flag:dawn day-form twin (R4 —
# both used to be post-build surgical additions; the builder now owns them and
# build_species.py mirrors them under area "tinderwick").
VERGE_RECT = {"tx": 11, "ty": 2, "w": 6, "h": 3}

m = {
    "id": "tinderwick", "display_name": "Tinderwick", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # Land ON the coast's return warps (the engine never auto-fires a step_on
        # warp on arrival) so going back is always one step — audit_warps.py.
        # Both coast warps are has_starter-gated: the gate-warden band at (13,1)
        # carries the diegetic "not yet" (the warps themselves stay silent).
        {"id": "to_coast", "at": {"tx": 13, "ty": 0}, "trigger": "step_on",
         "to_map": "dimglass_coast", "to": {"tx": 6, "ty": 33}, "facing": "up",
         "requires_flag": "flag:has_starter", "transition": "fade"},
        {"id": "to_coast_e", "at": {"tx": 14, "ty": 0}, "trigger": "step_on",
         "to_map": "dimglass_coast", "to": {"tx": 7, "ty": 33}, "facing": "up",
         "requires_flag": "flag:has_starter", "transition": "fade"},
        # Doors are WALK-ONTO (step_on + transition:'door'), on the door-art tile.
        # House door (cottage col 2) — now on the square, where the store used to be.
        {"id": "to_house", "at": {"tx": cottage_door[0], "ty": cottage_door[1]}, "trigger": "step_on",
         "to_map": "tinderwick_house", "to": {"tx": 7, "ty": 9}, "facing": "down", "transition": "door"},
        # Shop door (col 2) — down the lower-left lane, where home used to be.
        {"id": "to_shop", "at": {"tx": shop_door[0], "ty": shop_door[1]}, "trigger": "step_on",
         "to_map": "tinderwick_shop", "to": {"tx": 7, "ty": 8}, "facing": "down", "transition": "door"},
        # Lumenary GRAND DOUBLE DOOR — the arch straddles cols 2-3, so BOTH art tiles
        # warp in. One warp alone leaves the other half of the arch a solid wall (the
        # "leftmost tile only lets you in" bug). Soft-gated on holding a starter.
        {"id": "to_lumenary", "at": {"tx": lum_door[0], "ty": lum_door[1]}, "trigger": "step_on",
         "to_map": "tinderwick_lumenary", "to": {"tx": 8, "ty": 10}, "facing": "down",
         "requires_flag": "flag:has_starter", "transition": "door", "blocked_ref": "door.locked_lumenary"},
        {"id": "to_lumenary_e", "at": {"tx": lum_door_r[0], "ty": lum_door_r[1]}, "trigger": "step_on",
         "to_map": "tinderwick_lumenary", "to": {"tx": 8, "ty": 10}, "facing": "down",
         "requires_flag": "flag:has_starter", "transition": "door", "blocked_ref": "door.locked_lumenary"},
        # The Lanternway east (the lane map lanternway_tinderwick -> Vesper Crossroads).
        {"id": "to_crossroads", "at": {"tx": W - 1, "ty": 16}, "trigger": "step_on",
         "to_map": "lanternway_tinderwick", "to": {"tx": 0, "ty": 12}, "facing": "right",
         "transition": "fade"},
        # The Beacon foot door — wick-locked until the key comes home from the
        # coast road (the earned-first-Gleam quest; see graph.ts + build_beacon.py).
        {"id": "to_beacon", "at": {"tx": 24, "ty": 6}, "trigger": "step_on",
         "to_map": "tinderwick_beacon_i", "to": {"tx": 6, "ty": 7}, "facing": "down",
         "requires_flag": "flag:has_beacon_wick", "transition": "door", "blocked_ref": "door.locked_beacon"},
        # Vigil I host (06-postgame R3): the star-scar on the bluff.
        {"id": "to_vigil_hearth", "at": {"tx": 25, "ty": 7}, "trigger": "step_on",
         "to_map": "vigil_hearthfall", "to": {"tx": 11, "ty": 16}, "facing": "up",
         "requires_flag": "flag:vigil_reading_1", "blocked_ref": "npc.vigil_scar_sealed",
         "transition": "fade"},
    ] + [
        # R8: WEST through the hedge gap to Duskapple Orchard — ungated (safe,
        # always open; it's where the courier's cart threw a wheel with Fenn's
        # satchel aboard). Landing ON the orchard's return warps.
        {"id": "to_orchard" + ("" if y == 8 else "_s"), "at": {"tx": 0, "ty": y}, "trigger": "step_on",
         "to_map": "duskapple_orchard", "to": {"tx": 21, "ty": y}, "facing": "left",
         "transition": "fade"}
        for y in (8, 9)
    ],
    "triggers": [
        # The north-gate band: pre-starter, stepping into the open gate column runs
        # the warden's intercept (he warns, points east to Fenn, walks you back a
        # step). The warden's body blocks the other column (14,1), so (13,1) is the
        # only way through — and the band vanishes once the Wayfaring begins.
        {"id": "gate_warden", "kind": "cutscene", "at": {"tx": 13, "ty": 1},
         "activation": "step_on", "ref": "script.gate_warden",
         "hidden_when_flag": "flag:has_starter"},
        {"id": "sign_store", "kind": "sign", "at": {"tx": sign_tiles["sign_store"][0], "ty": sign_tiles["sign_store"][1]},
         "activation": "interact", "ref": "sign.tinderwick_store"},
        {"id": "sign_orchard", "kind": "sign", "at": {"tx": sign_tiles["sign_orchard"][0], "ty": sign_tiles["sign_orchard"][1]},
         "activation": "interact", "ref": "sign.tinderwick_orchard"},
        {"id": "sign_lumenary", "kind": "sign", "at": {"tx": sign_tiles["sign_lumenary"][0], "ty": sign_tiles["sign_lumenary"][1]},
         "activation": "interact", "ref": "sign.tinderwick_lumenary"},
        {"id": "sign_mentor", "kind": "sign", "at": {"tx": sign_tiles["sign_mentor"][0], "ty": sign_tiles["sign_mentor"][1]},
         "activation": "interact", "ref": "sign.tinderwick_mentor"},
        {"id": "sign_lanternway", "kind": "sign",
         "at": {"tx": sign_tiles["sign_lanternway"][0], "ty": sign_tiles["sign_lanternway"][1]},
         "activation": "interact", "ref": "sign.tinderwick_lanternway"},
        {"id": "sign_beacon", "kind": "sign",
         "at": {"tx": sign_tiles["sign_beacon"][0], "ty": sign_tiles["sign_beacon"][1]},
         "activation": "interact", "ref": "sign.beacon_door"},
    ],
    "encounters": [
        {"id": "verge_grass", "terrain": "tall_grass", "rect": dict(VERGE_RECT),
         "encounter_rate": 0.07,
         "table": [{"kin_id": 16, "weight": 60, "min_level": 2, "max_level": 4},
                   {"kin_id": 10, "weight": 40, "min_level": 2, "max_level": 3},
                   {"kin_id": 13, "weight": 20, "min_level": 2, "max_level": 4},
                   {"kin_id": 5, "weight": 12, "min_level": 3, "max_level": 4}],
         "hidden_when_flag": "flag:dawn"},
        {"id": "verge_grass_day", "terrain": "tall_grass", "rect": dict(VERGE_RECT),
         "encounter_rate": 0.07,
         "table": [{"kin_id": 16, "weight": 35, "min_level": 55, "max_level": 60},
                   {"kin_id": 10, "weight": 25, "min_level": 55, "max_level": 58},
                   {"kin_id": 5, "weight": 20, "min_level": 56, "max_level": 60},
                   {"kin_id": 8, "weight": 20, "min_level": 56, "max_level": 62},
                   {"kin_id": 13, "weight": 15, "min_level": 56, "max_level": 62}],
         "requires_flag": "flag:dawn"}],
    "npcs": [
        # The north gate-warden: posted IN the gate gap pre-starter (his body blocks
        # col 14; the script band guards col 13), swapped for a well-wisher stood
        # aside by the verge once the Wayfaring begins. Interacting with him runs
        # the same warning script as the band.
        {"id": "gatewarden_pre", "at": {"tx": 14, "ty": 1}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "script.gate_warden", "hidden_when_flag": "flag:has_starter"},
        {"id": "gatewarden_post", "at": {"tx": 16, "ty": 2}, "facing": "left",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.gatewarden_after", "requires_flag": "flag:has_starter"},
        # A valuable cache tucked on the EAST strand under the hedge (R8: it used to
        # sit on the west strand, where the purse now lies).
        {"id": "cache_waxcake", "at": {"tx": 26, "ty": 20}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_tinderwick_waxcake",
         "hidden_when_flag": "flag:picked_tinderwick_waxcake"},
        # (R8: Wren no longer mills by the garden — she's out in Duskapple Orchard,
        # "helping" the courier, until the Wayfaring begins.)
        # The Lantern-fair (Arc E): festival folk fill the square once the Ember
        # Gleam stands — the "Gleam = belonging" payoff, pure data via requires_flag.
        {"id": "fair_piper", "at": {"tx": 16, "ty": 9}, "facing": "down", "sprite": "npc_shopkeeper",
         "movement": "look_around", "dialogue_ref": "npc.fair_piper",
         "requires_flag": "gleam:ember"},
        {"id": "fair_kid", "at": {"tx": 11, "ty": 9}, "facing": "up", "sprite": "npc_child",
         "movement": "wander", "dialogue_ref": "npc.fair_kid",
         "requires_flag": "gleam:ember"},
        # P1 — the post-letters round: Brisa takes her letter in the square.
        {"id": "letter_brisa", "at": {"tx": 12, "ty": 9}, "facing": "down", "sprite": "npc_lampwarden",
         "movement": "static", "dialogue_ref": "script.post_letter_tinderwick",
         "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_tinderwick"},
        # Opening wayfinding: a townswoman by the east lane points at Fenn.
        {"id": "townguide_fenn", "at": {"tx": 20, "ty": 17}, "facing": "up", "sprite": "npc_woman",
         "movement": "look_around", "dialogue_ref": "npc.tinderwick_fenn_hint",
         "hidden_when_flag": "flag:has_starter"},
        # Andrew — the easter-egg trail's first voice + the WHERE NEXT? hint. Both
        # stage ids share ONE tile (the `emote` actor resolves by id). R8: he leans
        # on the garden fence now, not the old cottage lane.
        {"id": "andrew_pre", "at": {"tx": 15, "ty": 12}, "facing": "left", "sprite": "andrew_ward",
         "movement": "look_around", "dialogue_ref": "script.andrew_name",
         "hidden_when_flag": "flag:met_andrew"},
        {"id": "andrew_post", "at": {"tx": 15, "ty": 12}, "facing": "left", "sprite": "andrew_ward",
         "movement": "look_around", "dialogue_ref": "script.andrew_after",
         "requires_flag": "flag:met_andrew"},
        # R9 The Worry Club — Hester Fretwell, knitting furiously in the square
        # west of the main lane (off every path; Gilly on the flats is her sister).
        {"id": "worry_hester", "at": {"tx": 11, "ty": 11}, "facing": "down", "sprite": "npc_old_woman",
         "movement": "look_around", "dialogue_ref": "script.worry_hester"},
        # R9 peril thread: a neighbour watching the west gap toward the fallen
        # star in Duskapple Orchard (script stages itself on dusk_begins/gleam/dawn).
        {"id": "peril_neighbour", "at": {"tx": 2, "ty": 10}, "facing": "up", "sprite": "npc_old_woman",
         "movement": "static", "dialogue_ref": "script.peril_tinderwick_neighbour"},
        # The wick-purse safety net (one per early area) — now on the WEST strand.
        {"id": "cache_purse", "at": {"tx": 1, "ty": 20}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_tinderwick_purse",
         "hidden_when_flag": "flag:picked_tinderwick_purse"}],
    "gates": [], "music": "assets/audio/music/tinderwick-a.mp3",
    "_doors": {"shop": shop_door, "lumenary": lum_door, "lumenary_twin": lum_door_r,
               "house": cottage_door},
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
