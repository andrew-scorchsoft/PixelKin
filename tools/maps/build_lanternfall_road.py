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
                  bumps=[(2, 3, 1), (2, 12, 2), (3, 18, 1), (12, 1, 1)])
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)             # south border
mk.rect(tree, W, H, W - 2, 0, W - 1, H - 1)             # east tree-cliff wall
# punch the TOP gap (cols 2-3: the cave mouth) and the BOTTOM gap (cols 12-13:
# down to the Crossroads)
for x in (2, 3):
    for y in (0, 1):
        tree[y * W + x] = 0
for x in (12, 13):
    for y in (H - 2, H - 1):
        tree[y * W + x] = 0

# the descending lit lane (spine) — winds as it drops from the cave to the hub
path = mk.make_grid(W, H)
spine = {4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 7, 11: 8, 12: 9, 13: 9,
         14: 8, 15: 7, 16: 6, 17: 5, 18: 5, 19: 6, 20: 8, 21: 10, 22: 12}
tallgrass = mk.make_grid(W, H)
BANDS = [(10, 11), (17, 18)]
for ty, cx in spine.items():
    if any(y0 <= ty <= y1 for (y0, y1) in BANDS):
        continue
    path[ty * W + cx] = 1
    path[ty * W + cx + 1] = 1
    prev = spine.get(ty - 1)
    if prev is not None and abs(cx - prev) > 1:     # a 2-col jump: bridge it so
        for x in range(min(cx, prev) + 1, max(cx, prev) + 1):   # the lane stays
            path[ty * W + x] = 1                    # orthogonally contiguous
# connect the lane up into the top gap and down into the bottom gap
for y in range(0, 4):
    path[y * W + 2] = 1; path[y * W + 3] = 1
for y in range(22, H):
    path[y * W + 12] = 1; path[y * W + 13] = 1
# mandatory bands span the WHOLE walkable corridor (cols 2-13, up to the east
# wall) so there is no dodge lane — the brief: encounters are unavoidable.
for (y0, y1) in BANDS:
    pt.mandatory_band(tallgrass, path, W, H, y0=y0, y1=y1, x0=2, x1=13)
for (cx, cy, rx, ry) in [(10.5, 6.5, 1.8, 1.8), (5.0, 19.5, 1.8, 1.8)]:
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
]

# ---- objects: crown trees + lamp breadcrumbs --------------------------------
objects = [
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 8, "ty": 3}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 10, "ty": 12}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 2, "ty": 21}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 3, "ty": 6}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 9, "ty": 14}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 19}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, tallgrass, path))}
avoid = covered | building_cells

# ---- deco: cave recess, boulders, scatter -----------------------------------
deco = mk.make_grid(W, H)
for (x, y) in [(12, 7), (4, 16), (11, 19), (3, 11)]:     # verge boulders
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
owed += pt.sign(m, deco, W, sid="lanternfall_view", at=(3, 5))
owed += pt.sign(m, deco, W, sid="lanternfall_hub", at=(11, 23))
owed += pt.cache(m, cid="lanternfall_charge", at=(11, 6))
owed += pt.trainer_beat(m, tid="lanternfall_warden", at=(9, 11), facing="up", sight=4,
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
