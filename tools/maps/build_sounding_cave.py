#!/usr/bin/env python3
"""
The Sounding Cave — the middle leg of the Pearlmoor <-> Vesper Crossroads route.
A sea-cave you duck into off the Wrackline Path and come out the far side onto the
Lanternfall descent. A single through-floor (a traversal cave, not a region
dungeon): WEST mouth from Wrackline, EAST mouth out to Lanternfall, three chambers
on the drawn glowmoss-cave families joined by 1-tile chokes. The only path crosses
a glowmoss bed in the middle chamber, so the cave's kin can't be skirted; a north
alcove off it hides the valuable cache. Band 16-19 (Stone dwellers).

Chain:  wrackline_path -> sounding_cave -> lanternfall_road

Run:  python3 tools/maps/build_sounding_cave.py   (after build_shared_overworld.py)
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 14
rng = random.Random(53)

# ---- terrain: solid wall mass, rooms carved as rects + overlapping chokes -------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)                 # rock everywhere…

floor = mk.make_grid(W, H)                              # …carved chambers + chokes
mk.rect(floor, W, H, 1, 5, 6, 9)                        # WEST entry chamber
mk.hline(floor, W, H, 7, 1, 2)                          # west throat to the mouth
mk.hline(floor, W, H, 7, 6, 9)                          # choke entry -> mid (overlaps both)
mk.rect(floor, W, H, 8, 4, 13, 10)                      # MID chamber (the glowmoss bed)
mk.rect(floor, W, H, 9, 1, 12, 4)                       # NORTH alcove (the cache)
mk.vline(floor, W, H, 10, 3, 5)                         # alcove throat (overlaps mid)
mk.hline(floor, W, H, 7, 13, 16)                        # choke mid -> exit (overlaps both)
mk.rect(floor, W, H, 15, 5, 18, 9)                      # EAST exit chamber
mk.hline(floor, W, H, 7, 17, 18)                        # east throat to the mouth

for i in range(W * H):                                  # carve the rock
    if floor[i]:
        wall[i] = 0

# glowmoss — across the ONLY path through the mid chamber (rows 6-8, cols 8-13):
glow = mk.make_grid(W, H)
mk.blob(glow, W, H, 10.5, 7.0, 3.2, 1.8)
for i in range(W * H):                                  # moss only on open floor
    if glow[i] and not floor[i]:
        glow[i] = 0

# ---- base + terrain layers -----------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]
terrain_layers = [
    {"name": "t_glowmoss", "role": "terrain", "terrain": "glowmoss",
     "set": "vesper_overworld_set", "depth": 0, "data": glow},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco: shroom breadcrumbs, boulders, pebbles -------------------------------
deco = mk.make_grid(W, H)
for (x, y, n) in [(3, 8, "glowshroom_a"), (5, 6, "glowshroom_b"), (9, 9, "glowshroom_a"),
                  (12, 5, "glowshroom_b"), (16, 8, "glowshroom_a"), (17, 6, "glowshroom_b"),
                  (10, 2, "glowshroom_a")]:
    deco[y * W + x] = gid(n)
for (x, y) in [(2, 6), (13, 9), (16, 6), (4, 9)]:       # boulders
    deco[y * W + x] = gid("boulder")
for (x, y) in [(5, 8), (11, 9), (15, 9), (11, 2)]:      # stray pebbles
    deco[y * W + x] = gid("g_pebble")

# ---- assemble --------------------------------------------------------------------
m = {
    "id": "sounding_cave", "display_name": "The Sounding Cave", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": [],
    "warps": [
        # WEST mouth <-> Wrackline Path. Land one tile IN from Wrackline's east-edge
        # return warp (so a turn-straight-back re-enters); the mouth is 1 throat row.
        {"id": "to_wrackline", "at": {"tx": 0, "ty": 7}, "trigger": "step_on",
         "to_map": "wrackline_path", "to": {"tx": 14, "ty": 21}, "facing": "left",
         "transition": "door"},
        # EAST mouth -> Lanternfall Road (unauthored yet — inert tease until paired).
        {"id": "to_lanternfall", "at": {"tx": W - 1, "ty": 7}, "trigger": "step_on",
         "to_map": "lanternfall_road", "to": {"tx": 1, "ty": 4}, "facing": "right",
         "transition": "door"},
    ],
    "triggers": [],
    "encounters": [],
    "npcs": [],
    "gates": [],
    "music": "assets/audio/music/lowleaf-hollow-c.mp3",
}

# ---- stamps (signs, cache) ------------------------------------------------------
owed: list[str] = []
owed += pt.sign(m, deco, W, sid="sounding_mouth", at=(4, 6))
# the valuable cache in the north alcove (the cave's reward — off the lane)
owed += pt.cache(m, cid="sounding_amber", at=(11, 2))

# encounter beds from the glowmoss (the unavoidable mid bed), 16-19 Stone dwellers
m["encounters"] = pt.zones_from_grid(
    glow, W, H, terrain="tall_grass", rate=0.13, id_prefix="glow",
    table=[{"kin_id": 53, "weight": 55, "min_level": 16, "max_level": 19},
           {"kin_id": 69, "weight": 30, "min_level": 17, "max_level": 19},
           {"kin_id": 26, "weight": 15, "min_level": 16, "max_level": 18}])

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
