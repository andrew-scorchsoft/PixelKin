#!/usr/bin/env python3
"""
Build Dimglass Coast — the first route — on the SHARED overworld set.

Replaces the old flat-kit map (which FAILED the quality gate: no autotile vocabulary,
blocky fills) with a proper autotiled coastal route per level-design §7.3: an 18×34
vertical tidal shelf travelled south→north, cliff wall to the WEST, sea to the EAST,
a continuous lit path spine (the safe lane), alternating tall-grass patches, a sand
rest pocket, lantern-buoys teasing Tidecall offshore, and a cave mouth in the cliff
teasing Glimmerstep — each signed. Variant autotiling + scatter decor for polish.

Run:  python3 tools/maps/build_dimglass.py   (after build_shared_overworld.py)
"""
from __future__ import annotations
import json, random
import mapkit as mk
from mapkit import gid

W, H = 18, 34
rng = random.Random(19)

# ---- terrain presence grids -------------------------------------------------
cliff = mk.make_grid(W, H)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)                 # west cliff wall (continues off-west)
mk.rect(cliff, W, H, 0, 0, W - 1, 1)                 # north cliff band
mk.rect(cliff, W, H, 0, H - 2, W - 1, H - 1)         # south cliff band
for x in range(6, 9):                                # north exit gap
    cliff[0 * W + x] = 0; cliff[1 * W + x] = 0
for x in range(5, 9):                                # south entry gap (land-in from Tinderwick)
    cliff[(H - 1) * W + x] = 0; cliff[(H - 2) * W + x] = 0

water = mk.make_grid(W, H)
mk.rect(water, W, H, 14, 2, W - 1, H - 3)            # sea along the east (continues off-east)
sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 13, 2, 13, H - 3)               # thin beach line meeting the sea
mk.rect(sand, W, H, 9, 26, 13, 29)                  # widened sand rest pocket before the boundary

# alternating tall-grass beats (encounter patches), each a clean rect
tallgrass = mk.make_grid(W, H)
for (x0, y0, x1, y1) in [(3, 5, 6, 8), (8, 12, 11, 15), (4, 17, 7, 20), (8, 22, 11, 25)]:
    mk.rect(tallgrass, W, H, x0, y0, x1, y1)

# the lit path spine — a continuous safe lane from the south entry to the north exit
path = mk.make_grid(W, H)
spine = [6, 6, 6, 7, 7, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 8, 8, 7, 7, 6]
for ty in range(2, H - 2):
    cx = spine[min(ty - 2, len(spine) - 1)]
    path[ty * W + cx] = 1; path[ty * W + cx + 1] = 1
for x in range(6, 9):                                 # connect spine to both gaps
    path[2 * W + x] = 1; path[(H - 3) * W + x] = 1

# cave mouth recess in the west cliff (Glimmerstep tease) — carve grass, place dark rock
cave_xy = (2, 10)

# ---- base + terrain layers --------------------------------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

# ---- objects: a few canopy trees for walk-under depth ------------------------
objects = [
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 10, "ty": 6}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 3, "ty": 23}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
]
building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (cliff, water, sand, tallgrass, path))}
avoid = covered | building_cells

# ---- deco: cave, signs, buoys, lamps, scatter -------------------------------
deco = mk.make_grid(W, H)
for (x, y) in [cave_xy, (cave_xy[0], cave_xy[1] + 1)]:    # dark cave recess
    deco[y * W + x] = gid("cliff_fill")
for (x, y) in [(3, 7), (14, 6), (14, 13), (15, 20)]:      # lantern-buoys offshore + shore
    deco[y * W + x] = gid("buoy")
for (x, y) in [(3, 12), (12, 7), (4, 16), (3, 28)]:       # signs (buoys / cave / route / boundary)
    deco[y * W + x] = gid("sign")
for (x, y) in [(6, 4), (9, 11), (6, 18), (9, 24)]:        # lamp breadcrumbs up the lit lane
    deco[y * W + x] = gid("lamp")
mk.scatter_decor(deco, base, W, H, rng, density=0.10, avoid=avoid)

# ---- assemble ---------------------------------------------------------------
m = {
    "id": "dimglass_coast", "display_name": "Dimglass Coast", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        {"id": "from_tinderwick", "at": {"tx": 6, "ty": 32}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 13, "ty": 2}, "facing": "down", "transition": "fade"},
        {"id": "to_coast_ii", "at": {"tx": 7, "ty": 0}, "trigger": "step_on",
         "to_map": "dimglass_coast_ii", "to": {"tx": 7, "ty": 31}, "facing": "up", "transition": "fade"},
        {"id": "to_tideglass", "at": {"tx": 2, "ty": 10}, "trigger": "interact",
         "to_map": "tideglass_cavern", "to": {"tx": 5, "ty": 8}, "facing": "left",
         "requires_ability": "glimmerstep", "transition": "door"},
    ],
    "triggers": [
        {"id": "sign_buoys", "kind": "sign", "at": {"tx": 3, "ty": 12}, "activation": "interact",
         "ref": "sign.dimglass_buoys"},
        {"id": "sign_cave", "kind": "sign", "at": {"tx": 12, "ty": 7}, "activation": "interact",
         "ref": "sign.dimglass_cave"},
        {"id": "sign_route", "kind": "sign", "at": {"tx": 4, "ty": 16}, "activation": "interact",
         "ref": "sign.dimglass_route"},
        {"id": "sign_boundary", "kind": "sign", "at": {"tx": 3, "ty": 28}, "activation": "interact",
         "ref": "sign.dimglass_to_pearlmoor"},
    ],
    "encounters": [
        {"id": "grass_a", "terrain": "tall_grass", "rect": {"tx": 3, "ty": 5, "w": 4, "h": 4},
         "encounter_rate": 0.09,
         "table": [{"kin_id": 11, "weight": 60, "min_level": 3, "max_level": 5},
                   {"kin_id": 14, "weight": 40, "min_level": 3, "max_level": 5}]},
        {"id": "grass_b", "terrain": "tall_grass", "rect": {"tx": 8, "ty": 12, "w": 4, "h": 4},
         "encounter_rate": 0.09,
         "table": [{"kin_id": 11, "weight": 60, "min_level": 3, "max_level": 5},
                   {"kin_id": 14, "weight": 40, "min_level": 3, "max_level": 5}]},
        {"id": "tide_shallows", "terrain": "water", "rect": {"tx": 14, "ty": 5, "w": 2, "h": 4},
         "encounter_rate": 0.06, "requires_ability": "tidecall",
         "table": [{"kin_id": 2, "weight": 100, "min_level": 4, "max_level": 6}]}],
    "npcs": [
        {"id": "wayfarer", "at": {"tx": 6, "ty": 11}, "facing": "right", "sprite": "npc_mentor",
         "movement": "look_around", "dialogue_ref": "npc.dimglass_wayfarer"}],
    "gates": [
        {"id": "tide_gate", "ability": "tidecall", "effect": "make_passable",
         "rect": {"tx": 14, "ty": 5, "w": 2, "h": 4}}],
    "music": "assets/audio/music/dimglass-coast-a.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
