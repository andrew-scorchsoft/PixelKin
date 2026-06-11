#!/usr/bin/env python3
"""
Cinderhead Deep (upper galleries) — the mid-region dungeon's TOP floor
(walkthrough/02-east; level-design §2a: a region's mid dungeon is a multi-floor
ladder MAZE, not one room). Three interlinked floors:

    cinderhead_deep      (this file)  — entry from the mine; the FORK
    cinderhead_deep_b1f                — the descent; gallery-miner B
    cinderhead_deep_b2f                — the third gallery: the VIGIL-LAMP

This floor is the fork (§3a: choices, not a corridor). From the entry chamber a
gallery-miner (Druse) holds the only choke down into the hub; from the hub the
dungeon splits:
  * WEST — the ladder DOWN, the Descent Vigil's way to the still-lit vigil-lamp
    two floors below (the §4 gap-closer: 24-27 galleries before Otho's wall);
  * EAST — the FAR SIDE: the Crystoll void-gap [LATER] tease (Starreach), the
    sealed mine door opened from inside (flag:shortcut_mine -> the hub re-link),
    and the ungated gallery OUT to Galehigh (the East->North handoff).

All graph-required warps (to_mine, to_terraces, to_crystoll, shortcut_crossroads)
live on THIS node; the ladder pair is a spur edge to b1f.

Run:  ./venv/bin/python tools/maps/build_cinderhead_deep.py

audit_flow WAIVER — `loop` WARN stands: the one-way feel is the sealed-door
re-link (set on first reaching the far side), the mid-dungeon shortcut per §2a.
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 28, 22
rng = random.Random(94)
owed: list[str] = []

# ---- terrain: solid rock, the galleries carved out ------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 13, 1, 14, 4)                     # top throat in (from the mine)
mk.blob(floor, W, H, 13.5, 4.5, 4.5, 2.2)              # A — entry chamber
mk.vline(floor, W, H, 13, 6, 9)                         # choke A -> B (gallery-miner A)
mk.blob(floor, W, H, 13.0, 12.0, 5.0, 3.2)             # B — the hub chamber (the FORK)
# WEST arm: the ladder-down room (the Descent Vigil's way down)
mk.hline(floor, W, H, 12, 4, 8)                         # west corridor
mk.blob(floor, W, H, 4.5, 12.0, 2.4, 2.0)              # ladder room
# EAST arm: the FAR SIDE (sealed door + Crystoll + the Galehigh exit)
mk.hline(floor, W, H, 12, 18, 21)                       # east corridor (the choke band)
mk.blob(floor, W, H, 23.0, 13.0, 3.6, 3.4)             # E — the far-side chamber
mk.rect(floor, W, H, 26, 12, 27, 13)                   # E -> the gallery out to Galehigh
mk.vline(floor, W, H, 24, 6, 9)                         # E's north nook (the Crystoll void)
mk.blob(floor, W, H, 24.0, 6.0, 1.8, 1.6)

for i in range(W * H):                                  # carve the rock
    if floor[i]:
        wall[i] = 0

LADDER_DOWN = (4, 12)        # pairs with b1f's ladder_up

# ---- base + terrain layers ------------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.50 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco: crystal-vein light along the spine, rubble, the ladder ----------------
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


for (x, y, n) in [(13, 3, "glowshroom_a"), (13, 8, "glowshroom_b"), (10, 12, "glowshroom_a"),
                  (16, 12, "glowshroom_b"), (20, 12, "glowshroom_a"), (24, 7, "glowshroom_b"),
                  (23, 13, "glowshroom_a"), (5, 11, "glowshroom_b")]:
    put(x, y, n)
for (x, y) in [(11, 11), (15, 13), (22, 14), (24, 13), (6, 13)]:
    put(x, y, "boulder")
for (x, y) in [(12, 3), (10, 13), (17, 11), (21, 13), (25, 12), (4, 13)]:
    put(x, y, "g_pebble")
put(*LADDER_DOWN, "cave_ladder_down")
put(26, 6, "sign")                                      # the Crystoll void-gap notice

# ---- objects: glowing crystal outcrops (the deep-earth gleam) --------------------
objects = [
    {"id": "crystal_a", "sprite": "cinderhead_crystal_cluster", "at": {"tx": 24, "ty": 5},
     "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "crystal_b", "sprite": "cinderhead_crystal_cluster", "at": {"tx": 9, "ty": 13},
     "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "ore_cart", "sprite": "cinderhead_ore_cart", "at": {"tx": 17, "ty": 13},
     "w": 2, "h": 2, "overhang": 0},
]

m: dict = {
    "id": "cinderhead_deep", "display_name": "Cinderhead Deep", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": objects,
    "warps": [
        # UP — back to the mine mouth (graph.ts `to_deep` return half)
        {"id": "to_mine", "at": {"tx": 13, "ty": 1}, "trigger": "step_on",
         "to_map": "cinderhead_mine", "to": {"tx": 13, "ty": 22}, "facing": "up",
         "transition": "fade"},
        {"id": "to_mine_e", "at": {"tx": 14, "ty": 1}, "trigger": "step_on",
         "to_map": "cinderhead_mine", "to": {"tx": 14, "ty": 22}, "facing": "up",
         "transition": "fade"},
        # DOWN — the ladder to b1f (the Descent Vigil; lands ON b1f's ladder_up)
        {"id": "ladder_down", "at": {"tx": LADDER_DOWN[0], "ty": LADDER_DOWN[1]},
         "trigger": "step_on", "to_map": "cinderhead_deep_b1f", "to": {"tx": 19, "ty": 3},
         "facing": "down", "transition": "fade"},
        # OUT — the ungated gallery on to Galehigh (East->North handoff, graph.ts
        # `to_terraces`; galehigh unauthored — a safe inert tease for now)
        {"id": "to_terraces", "at": {"tx": 27, "ty": 12}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 1, "ty": 14}, "facing": "right",
         "transition": "fade"},
        {"id": "to_terraces_s", "at": {"tx": 27, "ty": 13}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 1, "ty": 15}, "facing": "right",
         "transition": "fade"},
        # SPUR — Crystoll Vault (graph.ts `to_crystoll`, Starreach — [LATER])
        {"id": "to_crystoll", "at": {"tx": 24, "ty": 5}, "trigger": "step_on",
         "to_map": "crystoll_vault", "to": {"tx": 5, "ty": 8}, "facing": "up",
         "requires_ability": "starreach", "transition": "fade"},
        # SHORTCUT — the sealed door opened from the inside (graph.ts
        # `shortcut_crossroads`, requires_flag set by the far-side beat below)
        {"id": "shortcut_crossroads", "at": {"tx": 22, "ty": 15}, "trigger": "step_on",
         "to_map": "vesper_crossroads", "to": {"tx": 8, "ty": 16}, "facing": "up",
         "requires_flag": "flag:shortcut_mine", "transition": "fade"},
    ],
    "triggers": [
        # THE SEALED-DOOR BEAT — on the only choke into the far side E (the east
        # corridor, row 12, cols 18-21), banded so it can't be walked around.
        *[{"id": f"open_shortcut_{tx}", "kind": "script", "at": {"tx": tx, "ty": 12},
           "activation": "step_on", "ref": "script.open_mine_shortcut", "once": True,
           "sets_flags": ["flag:shortcut_mine"],
           "hidden_when_flag": "flag:shortcut_mine"}
          for tx in (18, 19, 20, 21)],
        {"id": "sign_sealed", "kind": "sign", "at": {"tx": 25, "ty": 14},
         "activation": "interact", "ref": "sign.cinderhead_sealed"},
    ],
    # band 24-26 on the upper galleries (the deeper floors top out at 27).
    "encounters": [
        {"id": "gallery_a", "terrain": "cave", "rect": {"tx": 9, "ty": 10, "w": 9, "h": 5},
         "encounter_rate": 0.12,
         "table": [{"kin_id": 49, "weight": 45, "min_level": 24, "max_level": 26},
                   {"kin_id": 45, "weight": 35, "min_level": 24, "max_level": 26},
                   {"kin_id": 35, "weight": 20, "min_level": 24, "max_level": 26}]},
        {"id": "far_side", "terrain": "cave", "rect": {"tx": 20, "ty": 11, "w": 7, "h": 5},
         "encounter_rate": 0.12,
         "table": [{"kin_id": 49, "weight": 40, "min_level": 25, "max_level": 26},
                   {"kin_id": 45, "weight": 35, "min_level": 25, "max_level": 26},
                   {"kin_id": 35, "weight": 25, "min_level": 25, "max_level": 26}]},
    ],
    "npcs": [
        # the far-side lone miner ("been meaning to clear that door for years")
        {"id": "sealed_miner", "at": {"tx": 22, "ty": 13}, "facing": "down",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.cinderhead_sealed_miner",
         "requires_flag": "flag:shortcut_mine"},
        # an upper-gallery cache a step off the hub (variety: loose wicks)
        {"id": "cache_deepwicks", "at": {"tx": 11, "ty": 14}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_cinderhead_wicks_deep",
         "hidden_when_flag": "flag:picked_cinderhead_wicks_deep"},
    ],
    "gates": [],
    "music": "assets/audio/music/cinderhead-mine-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/cinderhead-mine-a.webp",
        "assets/backgrounds/battle/cinderhead-mine-b.webp",
    ],
}

# gallery-miner A (keeper) holds the choke down into the hub
owed += pt.trainer_beat(m, tid="gallery_miner_a", at=(13, 7), facing="down",
                        sight=4, sprite="npc_man")
# the Crystoll void-gap sign (the [LATER] tease, §5 back-reference)
owed += pt.sign(m, deco, W, sid="cinderhead_crystoll", at=(25, 6))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
