#!/usr/bin/env python3
"""
Build Wrackline Path — the Pearlmoor-side leg of the new Pearlmoor <-> Vesper
Crossroads route (REPLACES the bare lanternway_pearlmoor lane). A coastal cliff
path that descends south along the bay's EAST shore: sea off the WEST (the bay
between Dimglass and here), a tree-cliff wall to the EAST. The 2026-10 geometry fix
turned it into a true north->south leg: it comes in at the TOP from Saltreach Fen I
(the old drowned road surfacing past the lagoon) and leaves at the BOTTOM into the
Sounding Cave, so the loop home is compass-true. The
lit lane winds down THROUGH two mandatory tall-grass crossings and a sight trainer
posted in a choke, so the grass and the bout cannot be skirted (the design brief:
unavoidable encounters, no bypass). Level band 15-18 (a notch above Pearlmoor).

Chain:  saltreach_fen_i (south exit) -> wrackline_path -> sounding_cave -> ...

Run:  python3 tools/maps/build_wrackline_path.py   (after build_shared_overworld.py)
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 16, 26
rng = random.Random(47)

# ---- terrain presence grids -------------------------------------------------
# EAST tree-cliff wall (2 deep, the warps punch through it); WEST sea with a
# sand shore; the rest is the descending grass corridor.
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, right=1, depth=2,
                  bumps=[(13, 3, 1), (13, 12, 2), (12, 18, 1), (3, 1, 1)])
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)             # south border
# punch the TOP gap (cols 8-9: down from Saltreach Fen I) and the BOTTOM gap
# (cols 13-14: the Sounding Cave mouth)
TOP, BOT = (8, 9), (13, 14)
for x in TOP:
    for y in (0, 1):
        tree[y * W + x] = 0
for x in BOT:
    for y in (H - 2, H - 1):
        tree[y * W + x] = 0

water = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 2, 1, H - 3)                    # sea off the west
mk.blob(water, W, H, 1, 9, 1.4, 2.0)
mk.blob(water, W, H, 1, 17, 1.2, 1.8)
sand = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 2, 1, H - 3)
mk.rect(sand, W, H, 2, 2, 2, H - 3)                     # sand shore band
mk.blob(sand, W, H, 2, 13, 1.4, 2.0)

# the descending lit lane (spine) — winds left/right as it drops
path = mk.make_grid(W, H)
# col per row from the fen entry (top, cols 8-9) down to the cave (bottom, cols 13-14)
spine = {5: 8, 6: 8, 7: 8, 8: 9, 9: 9, 10: 9, 11: 8, 12: 7, 13: 6, 14: 6,
         15: 7, 16: 8, 17: 9, 18: 10, 19: 11, 20: 12, 21: 13}
# two MANDATORY tall-grass crossings — the lane is paused THROUGH them (the road
# itself rolls); the sight-trainer choke at row 14 makes the bout unavoidable too.
tallgrass = mk.make_grid(W, H)
BANDS = [(9, 10), (17, 18)]
for ty, cx in spine.items():
    if any(y0 <= ty <= y1 for (y0, y1) in BANDS):
        continue
    path[ty * W + cx] = 1
    path[ty * W + cx + 1] = 1
# connect the lane up into the top gap and down into the bottom gap
for y in range(0, 5):
    path[y * W + 8] = 1; path[y * W + 9] = 1
for y in range(20, H):
    path[y * W + 13] = 1; path[y * W + 14] = 1
# the mandatory bands span the WHOLE walkable corridor (cols 3-13), lane paused
for (y0, y1) in BANDS:
    pt.mandatory_band(tallgrass, path, W, H, y0=y0, y1=y1, x0=3, x1=13)
# a couple of optional grass patches beside the lane (the grind spots)
for (cx, cy, rx, ry) in [(5.0, 6.5, 1.8, 1.8), (10.5, 19.5, 1.8, 1.8)]:
    mk.blob(tallgrass, W, H, cx, cy, rx, ry)

# ---- base + terrain layers --------------------------------------------------
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
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

# ---- objects: crown trees + lamp breadcrumbs --------------------------------
objects = [
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 12, "ty": 3}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 4, "ty": 12}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 9, "ty": 22}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 7, "ty": 4}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 6, "ty": 14}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 20}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, water, sand, tallgrass, path))}
avoid = covered | building_cells

# ---- deco: cave mouth recess, signs, boulders, scatter ----------------------
deco = mk.make_grid(W, H)
for (x, y) in [(3, 7), (11, 16), (4, 19), (12, 11)]:    # shore/verge boulders
    deco[y * W + x] = gid("boulder")

# scatter only beside the lit lane (keeps the open field clean)
near_path = set()
for y in range(H):
    for x in range(W):
        if path[y * W + x]:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    near_path.add((x + dx, y + dy))
scatter_avoid = avoid | {(x, y) for y in range(H) for x in range(W) if (x, y) not in near_path}
mk.scatter_decor(deco, base, W, H, rng, density=0.12, avoid=scatter_avoid)

# ---- assemble ---------------------------------------------------------------
m = {
    "id": "wrackline_path", "display_name": "Wrackline Path", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # TOP: <-> Saltreach Fen I's south exit (the drowned road). Lands one row
        # IN from the fen's return warps; a warp on each tile of the 2-wide gap.
        {"id": "to_fen", "at": {"tx": 8, "ty": 0}, "trigger": "step_on",
         "to_map": "saltreach_fen_i", "to": {"tx": 20, "ty": 42}, "facing": "up", "transition": "fade"},
        {"id": "to_fen_e", "at": {"tx": 9, "ty": 0}, "trigger": "step_on",
         "to_map": "saltreach_fen_i", "to": {"tx": 21, "ty": 42}, "facing": "up", "transition": "fade"},
        # BOTTOM: the Sounding Cave's north mouth (door). Lands one tile IN.
        {"id": "to_cave", "at": {"tx": 13, "ty": H - 1}, "trigger": "step_on",
         "to_map": "sounding_cave", "to": {"tx": 12, "ty": 1}, "facing": "down", "transition": "door"},
        {"id": "to_cave_e", "at": {"tx": 14, "ty": H - 1}, "trigger": "step_on",
         "to_map": "sounding_cave", "to": {"tx": 12, "ty": 1}, "facing": "down", "transition": "door"},
    ],
    "triggers": [],
    "encounters": [],
    "npcs": [],
    "gates": [],
    "music": "assets/audio/music/dimglass-coast-b.mp3",
}

# ---- stamps that need `m` (signs, cache, trainer) ---------------------------
owed = []
owed += pt.sign(m, deco, W, sid="wrackline_view", at=(10, 5))
owed += pt.sign(m, deco, W, sid="wrackline_cave", at=(12, 23))
owed += pt.cache(m, cid="wrackline_balm", at=(10, 6))
# the unavoidable sight trainer, posted in the row-14 choke facing UP the lane
owed += pt.trainer_beat(m, tid="wrackline_drifter", at=(6, 14), facing="up", sight=4,
                        sprite="npc_man")

# encounter zones from the painted tall-grass (mandatory bands + patches), 15-18
m["encounters"] = pt.zones_from_grid(
    tallgrass, W, H, terrain="tall_grass", rate=0.11, id_prefix="grass",
    table=[{"kin_id": 31, "weight": 45, "min_level": 15, "max_level": 18},
           {"kin_id": 26, "weight": 35, "min_level": 15, "max_level": 17},
           {"kin_id": 53, "weight": 20, "min_level": 16, "max_level": 18}])

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
