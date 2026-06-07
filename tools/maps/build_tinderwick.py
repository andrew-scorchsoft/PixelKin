#!/usr/bin/env python3
"""
Build Tinderwick — the starter town — on the SHARED overworld set (the gold-standard area).

No longer bakes its own atlas: it references `vesper_overworld_set` (build_shared_overworld.py)
and paints terrain layers; mapkit.finalize() runs the autotiler (with variant scatter so
shorelines/tree-lines don't repeat), strips the terrain layers, renders and validates.

Redesigned to the level-design §7.1 target (28×24, blue-hour coastal village): an organic
2-deep tree-line with a north exit, a lit path spine from the exit down to the shore, a
plaza with the shop + Lumenary, the player's cottage lower-left, a small ornamental POND
inland (shows off inland water meshing), a fenced flower garden, a tall-grass verge by the
exit, and a sand beach + sea to the south with lantern-buoys. Scatter decor breaks the field.

Run:  python3 tools/maps/build_tinderwick.py
Prereq: python3 tools/maps/build_shared_overworld.py  (the shared set must exist).
"""
from __future__ import annotations
import json, random
import mapkit as mk
from mapkit import gid

W, H = 28, 24
rng = random.Random(7)

# ---- terrain presence grids -------------------------------------------------
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(5, 4, 1), (23, 4, 1), (3, 9, 1), (24, 11, 1), (4, 16, 1)])
for x in (13, 14):                       # punch the north exit gap
    tree[0 * W + x] = 0; tree[1 * W + x] = 0
mk.rect(tree, W, H, 0, 19, W - 1, H - 1, 0)   # clear the border below the shoreline

water_sea = mk.make_grid(W, H)
mk.rect(water_sea, W, H, 0, 22, W - 1, H - 1)            # full-width sea (continues off bottom)
pond = mk.make_grid(W, H)
mk.rect(pond, W, H, 18, 12, 21, 14)                      # small inland ornamental pond
sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 0, 19, W - 1, 21)                    # 3-row beach (edge/fill/edge); the sea
#   below draws its own foam shore. Sand meshes to grass above and water below.
tallgrass = mk.make_grid(W, H)
mk.rect(tallgrass, W, H, 10, 2, 15, 3)                   # verge straddling the exit lane

path = mk.make_grid(W, H)
mk.vline(path, W, H, 13, 2, 18); mk.vline(path, W, H, 14, 2, 18)  # the lit N–S spine (2 wide)
mk.hline(path, W, H, 8, 4, 22)                            # the street along the building fronts
mk.hline(path, W, H, 17, 6, 14)                           # lane to the cottage
mk.vline(path, W, H, 6, 8, 17)                            # cottage/shop door lane

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
    {"id": "shop", "sprite": "tinderwick_shop", "at": {"tx": 3, "ty": 4}, "w": 5, "h": 4, "overhang": 2},
    {"id": "lumenary", "sprite": "tinderwick_lumenary", "at": {"tx": 17, "ty": 2}, "w": 6, "h": 6, "overhang": 3},
    {"id": "house", "sprite": "tinderwick_cottage", "at": {"tx": 3, "ty": 12}, "w": 5, "h": 5, "overhang": 3},
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 9, "ty": 9}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 22, "ty": 13}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 5}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 15, "ty": 12}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
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

# ---- deco: flowers garden + signs + scatter + buoys -------------------------
deco = mk.make_grid(W, H)
for (x, y) in [(9, 13), (11, 13), (10, 14), (9, 15), (11, 15)]:   # fenced flower garden
    deco[y * W + x] = gid("flowers")
for (x, y) in [(8, 12), (12, 12), (8, 16), (12, 16)]:             # garden fence posts
    deco[y * W + x] = gid("fence")
for (x, y) in [(5, 9), (19, 9), (13, 12), (10, 18)]:              # signs (interact lessons)
    deco[y * W + x] = gid("sign")
for (x, y) in [(7, 20), (16, 20), (21, 20)]:                      # lantern-buoys on the shore
    deco[y * W + x] = gid("buoy")
mk.scatter_decor(deco, base, W, H, rng, density=0.11, avoid=avoid)

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
        {"id": "to_house", "at": {"tx": 6, "ty": 16}, "trigger": "interact",
         "to_map": "tinderwick_house", "to": {"tx": 5, "ty": 7}, "facing": "up", "transition": "door"},
    ],
    "triggers": [
        {"id": "intro_mentor", "kind": "cutscene", "at": {"tx": 13, "ty": 11},
         "activation": "step_on", "ref": "script.intro_mentor", "once": True,
         "sets_flags": ["flag:has_vesperlamp", "flag:has_starter"]},
        {"id": "lumenary_battle", "kind": "cutscene", "at": {"tx": 19, "ty": 8},
         "activation": "interact", "ref": "script.lumenary_tinderwick", "once": True,
         "requires_flag": "flag:has_starter"},
        {"id": "sign_shop", "kind": "sign", "at": {"tx": 5, "ty": 9}, "activation": "interact",
         "ref": "sign.tinderwick_square"},
        {"id": "sign_lumenary", "kind": "sign", "at": {"tx": 19, "ty": 9},
         "activation": "interact", "ref": "sign.tinderwick_lumenary"},
        {"id": "sign_mentor", "kind": "sign", "at": {"tx": 13, "ty": 12},
         "activation": "interact", "ref": "sign.tinderwick_mentor"},
        {"id": "sign_shore", "kind": "sign", "at": {"tx": 10, "ty": 18},
         "activation": "interact", "ref": "sign.tinderwick_dock"},
    ],
    "encounters": [
        {"id": "verge_grass", "terrain": "tall_grass", "rect": {"tx": 10, "ty": 2, "w": 6, "h": 2},
         "encounter_rate": 0.07,
         "table": [{"kin_id": 16, "weight": 60, "min_level": 2, "max_level": 4},
                   {"kin_id": 10, "weight": 40, "min_level": 2, "max_level": 3}]}],
    "npcs": [
        {"id": "mentor", "at": {"tx": 13, "ty": 10}, "facing": "down", "sprite": "npc_mentor",
         "movement": "static", "dialogue_ref": "npc.mentor_intro"},
        {"id": "child_runner", "at": {"tx": 16, "ty": 13}, "facing": "left", "sprite": "npc_child",
         "movement": "wander", "dialogue_ref": "npc.child_lanterns"}],
    "gates": [], "music": "assets/audio/music/tinderwick-a.mp3",
    "_doors": {"shop": (5, 7), "lumenary": (19, 8), "house": (6, 16)},
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
