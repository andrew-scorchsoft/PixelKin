#!/usr/bin/env python3
"""
Cinderhead Deep B2F — the third gallery, the deepest floor (the multi-floor
maze's bottom; walkthrough/02-east: "my crew left the vigil-lamp at the THIRD
gallery"). The darkest, with the fewest crystal-lights — the floor the
vesperlamp is truly for.

The Descent Vigil's turnaround: the still-lit VIGIL-LAMP waits at the heart
(script.take_vigil_lamp -> flag:q_east_vigil_lamp; appears only once Otho has
sent you, flag:q_east_vigil). A dead-end branch pays in deep MOTH-AMBER (the §4
grind reward). Band 26-27 (top of band — the careful player grinds up to meet
Otho's ace 28 here). The only way on is back UP the ladders to Otho's hall.

Ladder: ladder_up (11,3) <-> b1f's ladder_down (13,18).

Run:  ./venv/bin/python tools/maps/build_cinderhead_deep_b2f.py
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 22, 18
rng = random.Random(96)

LADDER_UP = (11, 3)         # pairs with b1f's ladder_down (12,16)

# ---- terrain (rect rooms+corridors for guaranteed connectivity) -----------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 9, 2, 13, 5)                      # ladder-up room (top)
mk.rect(floor, W, H, 10, 5, 12, 8)                     # choke down to the heart
mk.rect(floor, W, H, 7, 8, 15, 14)                     # the vigil-lamp chamber (heart)
mk.rect(floor, W, H, 2, 11, 7, 12)                     # WEST corridor -> moth-amber seam
mk.rect(floor, W, H, 2, 10, 3, 13)                     # the moth-amber dead-end
mk.rect(floor, W, H, 15, 11, 19, 12)                   # EAST corridor -> rubble pocket
mk.rect(floor, W, H, 17, 10, 19, 13)                   # the east rubble pocket

for i in range(W * H):
    if floor[i]:
        wall[i] = 0

# ---- base + terrain layers ------------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.45 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco: very sparse light (this is the dark floor) ---------------------------
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


for (x, y, n) in [(11, 5, "glowshroom_a"), (8, 11, "glowshroom_b"), (14, 11, "glowshroom_a")]:
    put(x, y, n)
for (x, y) in [(9, 10), (13, 12), (4, 11), (18, 11)]:
    put(x, y, "boulder")
for (x, y) in [(10, 4), (12, 12), (7, 11), (16, 11)]:
    put(x, y, "g_pebble")
put(*LADDER_UP, "cave_ladder_up")

# one crystal cluster over the vigil chamber — the heart's only landmark light
objects = [
    {"id": "crystal_heart", "sprite": "cinderhead_crystal_cluster", "at": {"tx": 13, "ty": 10},
     "w": 2, "h": 2, "overhang": 1, "walk_under": True},
]

m: dict = {
    "id": "cinderhead_deep_b2f", "display_name": "Cinderhead Deep B2F",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": objects,
    "warps": [
        {"id": "ladder_up", "at": {"tx": LADDER_UP[0], "ty": LADDER_UP[1]},
         "trigger": "step_on", "to_map": "cinderhead_deep_b1f", "to": {"tx": 12, "ty": 16},
         "facing": "down", "transition": "fade"},
    ],
    "triggers": [],
    "encounters": [
        {"id": "b2f_heart", "terrain": "cave", "rect": {"tx": 7, "ty": 9, "w": 9, "h": 5},
         "encounter_rate": 0.13,
         "table": [{"kin_id": 49, "weight": 40, "min_level": 26, "max_level": 27},
                   {"kin_id": 45, "weight": 35, "min_level": 26, "max_level": 27},
                   {"kin_id": 35, "weight": 25, "min_level": 26, "max_level": 27}]},
    ],
    "npcs": [
        # the still-lit VIGIL-LAMP at the heart of the third gallery — only present
        # once Otho has sent you (flag:q_east_vigil); taking it sets the loop flag.
        {"id": "vigil_lamp", "at": {"tx": 11, "ty": 11}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.take_vigil_lamp",
         "requires_flag": "flag:q_east_vigil",
         "hidden_when_flag": "flag:q_east_vigil_lamp"},
        # the deep moth-amber seam (the §4 grind reward, a dead-end away)
        {"id": "cache_deepcrystal", "at": {"tx": 3, "ty": 11}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_deepcrystal",
         "hidden_when_flag": "flag:picked_deepcrystal"},
    ],
    "gates": [],
    "music": "assets/audio/music/cinderhead-mine-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/cinderhead-mine-a.webp",
        "assets/backgrounds/battle/cinderhead-mine-b.webp",
    ],
}

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
