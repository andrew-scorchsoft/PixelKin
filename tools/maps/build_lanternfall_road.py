#!/usr/bin/env python3
"""
Build Lanternfall Road — the Crossroads-side leg of the new Pearlmoor <-> Vesper
Crossroads route (REPLACES the bare lanternway_pearlmoor lane). You come out the
Sounding Cave's south mouth onto this descent and follow the lit lane DOWN to the
Crossroads. 2026-10 geometry fix: a true north->south leg — the cave mouth at the
TOP (cols 2-3), the Crossroads' north road at the BOTTOM (cols 12-13); a
tree-cliff wall to the EAST. Two mandatory
tall-grass crossings + a sight trainer in a choke keep the band unavoidable.
Level 18-20 (the route's top). The Crossroads->here direction stays gleam:tide-
gated (the spoke is still the earned shortcut home); here->Crossroads is open.

TRAVERSAL PASS (2026-10, 09-the-wild-ways §3) — THE LANTERN STEPS: three cliff
steps cross the hillside wall to wall, each with one walk-up ramp, alternating
east / west / east, so the climb from the crossroads zig-zags the whole hill.
Coming down, a one-way grass DROP on the middle step's east end (right under the
first ramp) lets the descent run straight down the east side. A full-width
grass band on each terrace between the steps, and the lamp-keeper watching the
first ramp's foot, keep both directions honest. Warps, tables, trainer and
cache are unchanged (positions moved to fit the steps).

Chain:  ... sounding_cave -> lanternfall_road -> vesper_crossroads (north-west road)

Run:  python3 tools/maps/build_lanternfall_road.py   (after build_shared_overworld.py)
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 16, 26
rng = random.Random(61)

# ---- terrain presence grids -------------------------------------------------
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, left=1, depth=2,
                  bumps=[(12, 1, 1)])
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)             # south border
mk.rect(tree, W, H, W - 2, 0, W - 1, H - 1)             # east tree-cliff wall
for x in (2, 3):
    for y in (0, 1):
        tree[y * W + x] = 0
for x in (12, 13):
    for y in (H - 2, H - 1):
        tree[y * W + x] = 0

# TRAVERSAL PASS (2026-10, 09-the-wild-ways §3) — THE LANTERN STEPS. Three
# cliff steps cross the road (rim + face, wall to wall). Each has ONE walk-up
# ramp, and the ramps alternate ends (east / west / east), so the walk UP from
# the crossroads zig-zags the whole hillside. Coming DOWN, the lamplighters'
# quick way is the lit drop on the middle step's east end (a one-way grass
# ledge right under the first ramp): down the east side in one hop, up the
# long way round — the earned return the spoke was always meant to be.
STEPS = {1: (7, 8), 2: (13, 14), 3: (19, 20)}         # (rim, face) rows
RAMPS = {1: (12, 13), 2: (2, 3), 3: (12, 13)}         # walk-up gap columns
DROP_COLS = range(10, 14)                              # step 2's east-end ledge
cliff = mk.make_grid(W, H)
for s, (rim, face) in STEPS.items():
    for y in (rim, face):
        mk.hline(cliff, W, H, y, 2, 13)
    for x in RAMPS[s]:
        cliff[rim * W + x] = cliff[face * W + x] = 0
for x in DROP_COLS:
    cliff[STEPS[2][0] * W + x] = cliff[STEPS[2][1] * W + x] = 0

# the lit lane: the descent (down the east, over the drop) + the switchback up
path = mk.make_grid(W, H)
LANE: set[tuple[int, int]] = set()
for y in range(0, 5):
    LANE |= {(2, y), (3, y)}                    # out of the cave mouth
for x in range(2, 14):
    LANE |= {(x, 4), (x, 5)}                    # T0: east along the top terrace
for y in range(5, 14):
    LANE |= {(12, y), (13, y)}                  # ramp 1, down T1's east side to the drop
for y in range(15, H):
    LANE |= {(12, y), (13, y)}                  # T2's east side, ramp 3, T3, the exit
for y in range(9, 17):
    LANE |= {(2, y), (3, y)}                    # the switchback's west leg + ramp 2
for x in range(2, 14):
    LANE |= {(x, 16)}                           # T2: the switchback's long traverse
for x in range(4, 12):
    LANE |= {(x, 10)}                           # T1: back east to ramp 1
for (x, y) in LANE:
    path[y * W + x] = 1

# MANDATORY grass: each terrace between the steps carries a full-width band, so
# up or down, every crossing rolls the road's encounters.
tallgrass = mk.make_grid(W, H)
pt.mandatory_band(tallgrass, path, W, H, y0=11, y1=12, x0=2, x1=13)
pt.mandatory_band(tallgrass, path, W, H, y0=17, y1=18, x0=2, x1=13)
for (cx, cy, rx, ry) in [(8.5, 2.6, 1.8, 1.0), (6.0, 22.6, 2.0, 1.1)]:
    mk.blob(tallgrass, W, H, cx, cy, rx, ry)

for i in range(W * H):
    if tree[i] or cliff[i]:
        path[i] = tallgrass[i] = 0

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
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

# ---- objects: crown trees + lamp breadcrumbs (a lamp at every ramp) ---------
objects = [
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 7, "ty": 1}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 8, "ty": 20}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 2, "ty": 21}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 11, "ty": 6}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 4, "ty": 12}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 11, "ty": 18}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, tallgrass, path, cliff))}
avoid = covered | building_cells

# ---- deco: ledge, boulders, scatter -----------------------------------------
deco = mk.make_grid(W, H)
pt.ledge_run(deco, W, H, STEPS[2][1], DROP_COLS.start, DROP_COLS.stop - 1, rng, family="grass")
for (x, y) in [(5, 3), (8, 9), (9, 15), (6, 21)]:      # verge boulders
    deco[y * W + x] = gid("boulder")

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
    "id": "lanternfall_road", "display_name": "Lanternfall Road", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # TOP: the Sounding Cave's south mouth (door). Lands one row IN from the
        # cave's bottom-edge return warp.
        {"id": "to_cave", "at": {"tx": 2, "ty": 0}, "trigger": "step_on",
         "to_map": "sounding_cave", "to": {"tx": 4, "ty": 18}, "facing": "up", "transition": "door"},
        {"id": "to_cave_e", "at": {"tx": 3, "ty": 0}, "trigger": "step_on",
         "to_map": "sounding_cave", "to": {"tx": 4, "ty": 18}, "facing": "up", "transition": "door"},
        # BOTTOM: down onto the Vesper Crossroads' north-west road (the hub). OPEN
        # this way (the shortcut home); the Crossroads->here side carries the
        # gleam:tide gate.
        {"id": "to_crossroads", "at": {"tx": 12, "ty": H - 1}, "trigger": "step_on",
         "to_map": "vesper_crossroads", "to": {"tx": 3, "ty": 1}, "facing": "down", "transition": "fade"},
        {"id": "to_crossroads_e", "at": {"tx": 13, "ty": H - 1}, "trigger": "step_on",
         "to_map": "vesper_crossroads", "to": {"tx": 4, "ty": 1}, "facing": "down", "transition": "fade"},
    ],
    "triggers": [],
    "encounters": [],
    "npcs": [],
    "gates": [],
    "music": "assets/audio/music/dimglass-coast-b.mp3",
}

# ---- stamps (signs, cache, trainer) ----------------------------------------
owed: list[str] = []
owed += pt.sign(m, deco, W, sid="lanternfall_view", at=(4, 2))
owed += pt.sign(m, deco, W, sid="lanternfall_hub", at=(11, 23))
owed += pt.cache(m, cid="lanternfall_charge", at=(4, 6))
# the lamp-keeper tests the first ramp's foot: every way between the top terrace
# and the rest of the hill walks (12|13, 9) under her eye
owed += pt.trainer_beat(m, tid="lanternfall_warden", at=(11, 9), facing="right", sight=2,
                        sprite="npc_woman")

m["encounters"] = pt.zones_from_grid(
    tallgrass, W, H, terrain="tall_grass", rate=0.11, id_prefix="grass",
    table=[{"kin_id": 31, "weight": 45, "min_level": 18, "max_level": 20},
           {"kin_id": 26, "weight": 30, "min_level": 18, "max_level": 20},
           {"kin_id": 53, "weight": 25, "min_level": 18, "max_level": 20}])

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
