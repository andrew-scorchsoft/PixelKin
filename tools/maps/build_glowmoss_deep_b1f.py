#!/usr/bin/env python3
"""
Glowmoss Deep B1F — the dungeon's lower floor (the genre's descend-and-surface
verb, level-design §11a "dungeon scale ladder").

A darker, tighter MAZE under the moss chambers: one ladder back up (NE), two
dead-end branches (one hiding a Star-chart cache), a deeper glowmoss bed at the
heart, and the Spore Grotto's true mouth in the SW — the spur now EARNS its
rarity by being a floor down. Almost no shroom-light: this is the floor the
vesperlamp is for.

Ladder pairing (audited): upper (25,23) cave_ladder_down -> lands ON this
floor's cave_ladder_up at (19,4), and back. step_on both ways is safe — the
engine never auto-fires a warp on arrival.

Run:  ./venv/bin/python tools/maps/build_glowmoss_deep_b1f.py
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 24, 20
rng = random.Random(68)

LADDER_UP = (19, 4)       # pairs with glowmoss_deep's ladder_down at (25,23)
GROTTO_MOUTH = (6, 18)    # the spur's true mouth, a floor down
SIGN_GROTTO = (5, 17)
CACHE_CHART = (3, 7)      # dead-end A's reward

# ---- terrain: solid rock, a winding corridor maze carved out --------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.blob(floor, W, H, 19.5, 4.5, 2.2, 1.8)               # NE: the ladder room
mk.hline(floor, W, H, 4, 8, 17)                         # long west corridor
mk.hline(floor, W, H, 4, 3, 7)                          # ...continuing to dead-end A
mk.vline(floor, W, H, 3, 5, 7)                          # dead-end A: the chart alcove
mk.vline(floor, W, H, 8, 5, 9)                          # junction shaft down
mk.blob(floor, W, H, 7.0, 11.0, 3.0, 2.5)               # heart chamber (the deep bed)
mk.hline(floor, W, H, 13, 8, 16)                        # east passage
mk.blob(floor, W, H, 18.0, 14.0, 2.5, 2.0)              # SE chamber
mk.hline(floor, W, H, 14, 21, 22)                       # dead-end B: a rubble pocket
mk.vline(floor, W, H, 18, 16, 17)                       # south shaft
mk.hline(floor, W, H, 17, 8, 18)                        # SW corridor
mk.blob(floor, W, H, 6.5, 17.5, 2.0, 1.5)               # SW: the grotto antechamber

for i in range(W * H):
    if floor[i]:
        wall[i] = 0

# the deep bed — glowmoss only at the heart (the rest of the floor is dark)…
glow = mk.make_grid(W, H)
mk.blob(glow, W, H, 7.0, 11.5, 2.2, 1.8)
# …plus a small overflow pooled in the SE chamber, so the floor's east half
# isn't a dead screenful (§3a rule 5; audit_flow flagged it) and the rubble
# dead-end's approach carries a roll
mk.blob(glow, W, H, 18.0, 14.5, 1.4, 1.1)
for i in range(W * H):
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

# ---- deco: the ladder, sparse light, rubble ------------------------------------
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


put(*LADDER_UP, "cave_ladder_up")
# B1F is the DARK floor: three breadcrumbs only, marking the three ways onward
for (x, y, n) in [(17, 5, "glowshroom_a"), (9, 9, "glowshroom_b"), (16, 13, "glowshroom_a")]:
    put(x, y, n)
# rubble + pebbles breaking the corridors
for (x, y) in [(11, 5), (5, 10), (19, 15)]:
    put(x, y, "boulder")
for (x, y) in [(13, 4), (6, 9), (10, 12), (17, 14), (8, 17), (22, 13)]:
    put(x, y, "g_pebble")
put(*SIGN_GROTTO, "sign")
# the grotto's dark recess in the antechamber's south wall
deco[GROTTO_MOUTH[1] * W + GROTTO_MOUTH[0]] = gid("cavewall_fill")

# ---- assemble --------------------------------------------------------------------
m = {
    "id": "glowmoss_deep_b1f", "display_name": "Glowmoss Deep B1F",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": [
        # one living cluster over the deep bed — the only landmark down here
        {"id": "shrooms_heart", "sprite": "glowmoss_deep_glowshrooms_teal",
         "at": {"tx": 5, "ty": 12}, "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    ],
    "warps": [
        # the ladder back up — lands ON the upper floor's ladder-pit (mutual pair)
        {"id": "ladder_up", "at": {"tx": LADDER_UP[0], "ty": LADDER_UP[1]},
         "trigger": "step_on", "to_map": "glowmoss_deep", "to": {"tx": 25, "ty": 23},
         "facing": "down", "transition": "fade"},
        # the Spore Grotto's true mouth (graph.ts `to_grotto`) — a floor down,
        # so the spur's rare bed is EARNED by the descent.
        {"id": "to_grotto", "at": {"tx": GROTTO_MOUTH[0], "ty": GROTTO_MOUTH[1]},
         "trigger": "interact", "to_map": "spore_grotto", "to": {"tx": 5, "ty": 8},
         "facing": "down", "requires_ability": "glimmerstep", "transition": "door"},
    ],
    "triggers": [
        {"id": "sign_grotto", "kind": "sign",
         "at": {"tx": SIGN_GROTTO[0], "ty": SIGN_GROTTO[1]},
         "activation": "interact", "ref": "sign.glowmoss_b1f_grotto"},
    ],
    # The deep bed: band 21-23, the floor where Sporemid stops being rare —
    # descending is how you meet the line's middle stage before Cinderhead.
    "encounters": [
        {"id": "deep_bed", "terrain": "tall_grass", "rect": {"tx": 4, "ty": 9, "w": 7, "h": 5},
         "encounter_rate": 0.12,
         "table": [{"kin_id": 56, "weight": 35, "min_level": 21, "max_level": 23},
                   {"kin_id": 38, "weight": 25, "min_level": 21, "max_level": 23},
                   {"kin_id": 57, "weight": 25, "min_level": 21, "max_level": 23},
                   {"kin_id": 67, "weight": 15, "min_level": 22, "max_level": 23}]},
        # the SE overflow pool — same band, Mossglow-leaning (the light pools)
        {"id": "se_pool", "terrain": "tall_grass", "rect": {"tx": 16, "ty": 13, "w": 5, "h": 3},
         "encounter_rate": 0.12,
         "table": [{"kin_id": 38, "weight": 40, "min_level": 21, "max_level": 23},
                   {"kin_id": 56, "weight": 35, "min_level": 21, "max_level": 23},
                   {"kin_id": 57, "weight": 25, "min_level": 21, "max_level": 23}]},
    ],
    "npcs": [
        # dead-end A's prize: a Star-chart cache (the maze pays in kind)
        {"id": "cache_chart", "at": {"tx": CACHE_CHART[0], "ty": CACHE_CHART[1]},
         "facing": "down", "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_b1f_chart",
         "hidden_when_flag": "flag:picked_b1f_chart"},
    ],
    "gates": [],
    "music": "assets/audio/music/lowleaf-hollow-c.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
