#!/usr/bin/env python3
"""
Cinderhead Deep B1F — the descent's middle floor (the multi-floor maze, §2a).

Darker and tighter than the upper galleries: the ladder up (NE, pairs with the
upper floor), a single choke held by gallery-miner B (Hobb — the second of the
two vigil-miners), the E3 Foreman's-Ledger dead-end off the west, and the ladder
DOWN to the third gallery (b2f) where the vigil-lamp waits. Band 25-27.

Ladder pairs (audited, mutual step_on landing ON each other):
  upper ladder_down (4,12)  <-> this floor's ladder_up   (19,3)
  this floor's ladder_down (13,18) <-> b2f's ladder_up   (11,3)

Run:  ./venv/bin/python tools/maps/build_cinderhead_deep_b1f.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 20
rng = random.Random(95)
owed: list[str] = []

LADDER_UP = (19, 3)         # pairs with cinderhead_deep's ladder_down (4,12)
LADDER_DOWN = (12, 16)      # pairs with b2f's ladder_up (11,3)

# ---- terrain: solid rock, a winding gallery carved out (rect rooms+corridors
# for guaranteed connectivity; ladders kept off the border rows) -----------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 16, 2, 21, 5)                     # NE — the ladder-up room
mk.rect(floor, W, H, 17, 5, 18, 9)                     # choke down (gallery-miner B)
mk.rect(floor, W, H, 7, 9, 18, 14)                     # the hub gallery
mk.rect(floor, W, H, 2, 11, 7, 12)                     # WEST corridor -> ledger alcove
mk.rect(floor, W, H, 2, 10, 3, 13)                     # the ledger dead-end alcove
mk.rect(floor, W, H, 11, 14, 13, 16)                   # DOWN to b2f
mk.rect(floor, W, H, 10, 15, 14, 17)                   # the down-ladder room

for i in range(W * H):
    if floor[i]:
        wall[i] = 0

# ---- base + terrain layers ------------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.50 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco --------------------------------------------------------------------
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


for (x, y, n) in [(19, 5, "glowshroom_a"), (15, 11, "glowshroom_b"), (10, 11, "glowshroom_a"),
                  (13, 15, "glowshroom_b"), (5, 11, "glowshroom_a")]:
    put(x, y, n)
for (x, y) in [(11, 10), (16, 12), (12, 13), (6, 12)]:
    put(x, y, "boulder")
for (x, y) in [(17, 6), (14, 10), (9, 12), (13, 16)]:
    put(x, y, "g_pebble")
put(*LADDER_UP, "cave_ladder_up")
put(*LADDER_DOWN, "cave_ladder_down")

objects = [
    {"id": "crystal_a", "sprite": "cinderhead_crystal_cluster", "at": {"tx": 16, "ty": 12},
     "w": 2, "h": 2, "overhang": 1, "walk_under": True},
]

m: dict = {
    "id": "cinderhead_deep_b1f", "display_name": "Cinderhead Deep B1F",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": objects,
    "warps": [
        {"id": "ladder_up", "at": {"tx": LADDER_UP[0], "ty": LADDER_UP[1]},
         "trigger": "step_on", "to_map": "cinderhead_deep", "to": {"tx": 4, "ty": 12},
         "facing": "down", "transition": "fade"},
        {"id": "ladder_down", "at": {"tx": LADDER_DOWN[0], "ty": LADDER_DOWN[1]},
         "trigger": "step_on", "to_map": "cinderhead_deep_b2f", "to": {"tx": 11, "ty": 3},
         "facing": "down", "transition": "fade"},
    ],
    "triggers": [],
    "encounters": [
        {"id": "b1f_gallery", "terrain": "cave", "rect": {"tx": 9, "ty": 9, "w": 9, "h": 5},
         "encounter_rate": 0.13,
         "table": [{"kin_id": 49, "weight": 40, "min_level": 25, "max_level": 27},
                   {"kin_id": 45, "weight": 35, "min_level": 25, "max_level": 27},
                   {"kin_id": 35, "weight": 25, "min_level": 25, "max_level": 27}]},
    ],
    "npcs": [
        # E3 ledger — the old crew's ledger in the west dead-end gallery
        {"id": "cache_ledger", "at": {"tx": 2, "ty": 11}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_ledger",
         "requires_flag": "flag:q_east_ledger",
         "hidden_when_flag": "flag:q_east_ledger_found"},
        # a balm cache by the down-ladder (variety)
        {"id": "cache_b1f_balm", "at": {"tx": 11, "ty": 16}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_cinderhead_balm_deep",
         "hidden_when_flag": "flag:picked_cinderhead_balm_deep"},
    ],
    "gates": [],
    "music": "assets/audio/music/cinderhead-mine-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/cinderhead-mine-a.webp",
        "assets/backgrounds/battle/cinderhead-mine-b.webp",
    ],
}

# gallery-miner B (keeper) holds the only choke deeper
owed += pt.trainer_beat(m, tid="gallery_miner_b", at=(18, 6), facing="down",
                        sight=4, sprite="npc_woman")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
