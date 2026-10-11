#!/usr/bin/env python3
"""
The Sounding Cave — the middle leg of the Pearlmoor <-> Vesper Crossroads route.
A sea-cave you duck into off the Wrackline Path and come out the far side onto the
Lanternfall descent. A single through-floor (a traversal cave, not a region
dungeon): NORTH mouth from Wrackline, SOUTH mouth out to Lanternfall, three chambers
on the drawn glowmoss-cave families joined by 1-tile chokes. The only path crosses
a glowmoss bed in the middle chamber, so the cave's kin can't be skirted; a west
alcove off it hides the valuable cache. Band 16-19 (Stone dwellers).

Chain:  wrackline_path -> sounding_cave -> lanternfall_road

Run:  python3 tools/maps/build_sounding_cave.py   (after build_shared_overworld.py)
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 14, 20
rng = random.Random(53)

# 2026-10 geometry fix: the cave stands on end — a NORTH mouth (col 12) from
# Wrackline Path and a SOUTH mouth (col 4) out onto Lanternfall Road, so the
# loop home runs compass-true down the bay shore. Same three chambers, the same
# unavoidable glowmoss bed and the same hidden alcove cache, turned on end.

# ---- terrain: solid wall mass, rooms carved as rects + overlapping chokes -------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)                 # rock everywhere…

floor = mk.make_grid(W, H)                              # …carved chambers + chokes
mk.vline(floor, W, H, 12, 0, 2)                         # north throat to the mouth
mk.rect(floor, W, H, 8, 1, 12, 5)                       # NORTH entry chamber
mk.vline(floor, W, H, 9, 5, 7)                          # choke entry -> mid (overlaps both)
mk.rect(floor, W, H, 4, 7, 10, 12)                      # MID chamber (the glowmoss bed)
mk.rect(floor, W, H, 1, 8, 2, 10)                       # WEST alcove (the cache)
mk.hline(floor, W, H, 9, 2, 4)                          # alcove throat (overlaps mid)
mk.vline(floor, W, H, 6, 12, 14)                        # choke mid -> exit (overlaps both)
mk.rect(floor, W, H, 3, 14, 8, 17)                      # SOUTH exit chamber
mk.vline(floor, W, H, 4, 17, H - 1)                     # south throat to the mouth

for i in range(W * H):                                  # carve the rock
    if floor[i]:
        wall[i] = 0

# glowmoss — a full band across the ONLY path through the mid chamber (rows 9-10)
# plus an organic blob, so the bed can't be skirted:
glow = mk.make_grid(W, H)
mk.blob(glow, W, H, 7.0, 9.5, 3.4, 1.9)
mk.rect(glow, W, H, 4, 9, 10, 10)
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
for (x, y, n) in [(10, 2, "glowshroom_a"), (8, 4, "glowshroom_b"), (5, 8, "glowshroom_a"),
                  (10, 11, "glowshroom_b"), (7, 16, "glowshroom_a"), (3, 15, "glowshroom_b"),
                  (1, 8, "glowshroom_a")]:
    deco[y * W + x] = gid(n)
for (x, y) in [(11, 4), (4, 12), (8, 14), (3, 17)]:      # boulders
    deco[y * W + x] = gid("boulder")
for (x, y) in [(9, 3), (5, 11), (6, 16), (2, 10)]:       # stray pebbles
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
        # NORTH mouth <-> Wrackline Path (its bottom gap). Lands one row IN from
        # Wrackline's bottom-edge return warps.
        {"id": "to_wrackline", "at": {"tx": 12, "ty": 0}, "trigger": "step_on",
         "to_map": "wrackline_path", "to": {"tx": 13, "ty": 24}, "facing": "up",
         "transition": "door"},
        # SOUTH mouth -> Lanternfall Road (its top gap).
        {"id": "to_lanternfall", "at": {"tx": 4, "ty": H - 1}, "trigger": "step_on",
         "to_map": "lanternfall_road", "to": {"tx": 2, "ty": 1}, "facing": "down",
         "transition": "door"},
    ],
    "triggers": [],
    "encounters": [],
    "npcs": [],
    "gates": [],
    "music": "assets/audio/music/dimglass-coast-c.mp3",
}

# ---- stamps (signs, cache) ------------------------------------------------------
owed: list[str] = []
owed += pt.sign(m, deco, W, sid="sounding_mouth", at=(10, 1))
# the valuable cache in the west alcove (the cave's reward — off the lane)
owed += pt.cache(m, cid="sounding_amber", at=(1, 9))

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
