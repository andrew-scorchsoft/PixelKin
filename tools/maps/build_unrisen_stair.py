#!/usr/bin/env python3
"""
The Unrisen Stair — the Dawn that waited (walkthrough/07-the-three §6: Site
III of the Three Hours, the hardest and last). A vertical processional ruin
annexed off the Sunken Solarium's deepest fold (the host edit: the
First-Light basin + the `to_unrisen` warp, sealed on flag:three_dawn_poured).

A pale stair that once greeted the sunrise, climbing in three flights over
still black water, crossable only by sun-vine — THE SUNSKETCH PUZZLE
DIMENSION IN FULL (sequential + redirect, the Helia Vault grammar). Three
signature touches (§8):
  1. THE BLOOM ASCENT — vine A over the first water; from A's landing the
     SUN-MIRROR FLOWER on the east spur bends the pocket of daylight across
     the water to the far vine (the redirect); vine B opens the east flight
     to the head terrace.
  2. THE HEAD TERRACE — where the first light was meant to land. ERSTMORN
     stands at its centre, facing east. It has been facing east for years.
  3. PROCESSIONAL QUIET — no encounter zones anywhere (hooks verbatim): wild
     kin defer. One MISSABLE Starglass Shard in a fallen capital off flight 2.

ENCODING (the Helia precedent, spelled out):
  * The crossings ride Sunsketch AbilityGates (held by everyone here — the
    warp requires it); their SEQUENCE is geometric, their BEAT is the bloom
    band; the REDIRECT'S LOCK is on the REWARD (collision cannot key on a
    flag): `hour_dawn` requires flag:three_dawn_bloom_b — the flag table's
    "_b -> head terrace" consumption — so a Tidecall swim over the black
    water (all water families gate on tidecall, long held) can never skip
    the mirror: the terrace stands empty until the daylight is bent.
  * Both water bands wear cliff lips on their north shores except at the
    vine columns, and the bloom bands sit on BOTH the root and landing
    cells, so walker and swimmer alike fire the beats in order.
  * vine A: root/landing bands set flag:three_dawn_bloom_a (consume
    flag:three_dawn_poured per the hooks' table).
  * mirror: interact, requires _a, blocked npc.unrisen_mirror_waits ->
    script.three_dawn_mirror sets flag:three_dawn_bloom_b (dim->alight swap).
  * vine B: root/landing band requires _b, blocked npc.unrisen_far_vine
    (narrates the lock on every early attempt), ref npc.unrisen_stair_wakes.

The set-piece (wiring pass — hooks VERBATIM; `script.three_dawn_battle` must
set flag:three_dawn_met BEFORE the op, win or withdraw, and its false-dawn
tint must rhyme with the Keystar relight — same family, a fraction of the
strength; cinematics.md):
  { op: 'legendaryBattle', name: 'three_dawn', kin: 162, level: 55,
    caughtFlag: 'flag:three_dawn_caught', cooldownBattles: 18,
    cooldownRef: 'npc.three_dawn_resting' }
  (NO terrain — the stair is no encounter ground; conditional charges read
  plain here, intended: the last Hour offers no shortcuts.)

audit_flow WAIVERS — `loop`/`free-pass` WARNs accepted if raised: a
processional dead-end shrine; the descent retraces the ascent on purpose.

Run:  ./venv/bin/python tools/maps/build_unrisen_stair.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 26
rng = random.Random(162)
owed: list[str] = []

ENTRY = (10, 24)           # to_solarium pad; host to_unrisen lands ON it

# ---- terrain presence grids ---------------------------------------------------------
cliff = mk.make_grid(W, H)   # the ruin basin's walls + the water bands' lips
ruin = mk.make_grid(W, H)    # the processional paving
pool = mk.make_grid(W, H)    # the still black water (sunpool)
gold = mk.make_grid(W, H)    # goldtuft dressing (zoneless — never rolls)

# borders: cliff all round, 2 deep, organic bumps (§11 r2)
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.rect(cliff, W, H, 0, 24, W - 1, H - 1)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)
mk.rect(cliff, W, H, 18, 0, 19, H - 1)
mk.organic_border(cliff, W, H, depth=0,
                  bumps=[(5, 1, 2), (14, 1, 2), (1, 7, 2), (1, 15, 2),
                         (18, 12, 2), (18, 20, 2), (4, 24, 2)],
                  rng=rng)
# the entry recess (the sealed stair's foot; landing (10,24) stays walkable)
for (x, y) in [(9, 23), (10, 23), (11, 23), (10, 24)]:
    cliff[y * W + x] = 0

# THE FOOT COURT (flight 1)
def open_rect(x0, y0, x1, y1):
    mk.rect(cliff, W, H, x0, y0, x1, y1, 0)

open_rect(4, 19, 15, 22)
# WATER BAND A (rows 17-18) + its north cliff lip (row 16) pierced at vine A (x9)
mk.rect(pool, W, H, 3, 17, 16, 18)
mk.rect(cliff, W, H, 3, 16, 16, 16)
cliff[16 * W + 9] = 0
# FLIGHT 2 (rows 12-15) + the mirror spur east
open_rect(3, 12, 16, 15)
# WATER BAND B (rows 9-11) + its north lip (row 8) pierced at the far vine (x12)
mk.rect(pool, W, H, 3, 9, 16, 11)
mk.rect(cliff, W, H, 3, 8, 16, 8)
cliff[8 * W + 12] = 0
# THE HEAD TERRACE (rows 4-7)
open_rect(6, 4, 15, 7)

# ---- the processional paving (ruinfloor) --------------------------------------------
mk.rect(ruin, W, H, 9, 19, 11, 24)        # the court's centre lane
mk.rect(ruin, W, H, 9, 16, 9, 19)         # to vine A's root
mk.rect(ruin, W, H, 8, 12, 13, 13)        # flight 2's landing walk
mk.rect(ruin, W, H, 12, 12, 12, 12)       # to the far vine's root
mk.rect(ruin, W, H, 14, 13, 16, 14)       # the mirror spur's worked floor
mk.rect(ruin, W, H, 7, 4, 14, 8)          # the head terrace floor
# the water bands keep their cells (precedence below): paving never crosses them

# ---- gold dressing (zoneless) -------------------------------------------------------
for (x, y) in [(5, 20), (13, 21), (4, 14), (15, 15), (7, 14), (8, 6), (13, 7), (6, 21)]:
    gold[y * W + x] = 1

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if cliff[i]:
        ruin[i] = pool[i] = gold[i] = 0
    if pool[i]:
        ruin[i] = gold[i] = 0
    if ruin[i]:
        gold[i] = 0

# ---- base: gold grass (the West's remembered light, a half-shade to dawn) -----------
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": ruin},
    {"name": "t_gold", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": gold},
    {"name": "t_pool", "role": "terrain", "terrain": "sunpool",
     "set": "vesper_overworld_set", "depth": 0, "data": pool},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

deco = mk.make_grid(W, H)

m: dict = {
    "id": "unrisen_stair", "display_name": "The Unrisen Stair",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [
        # the two vine crossings (Sunsketch held by everyone here — the warp's
        # own gate; sequence is geometric, the lock is on the reward)
        {"id": "vine_a", "ability": "sunsketch",
         "rect": {"tx": 9, "ty": 17, "w": 1, "h": 2}, "effect": "make_passable"},
        {"id": "vine_b", "ability": "sunsketch",
         "rect": {"tx": 12, "ty": 9, "w": 1, "h": 3}, "effect": "make_passable"},
    ],
    # the annex reuses the Solarium loop's sparsest variant (the reuse table)
    "music": "assets/audio/music/sunken-solarium-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/unrisen-stair-a.webp",
    ],
}

# ---- warps --------------------------------------------------------------------------
m["warps"].append(
    # back down to the Solarium's pour pocket — lands ON the host's to_unrisen
    {"id": "to_solarium", "at": {"tx": ENTRY[0], "ty": ENTRY[1]}, "trigger": "step_on",
     "to_map": "sunken_solarium", "to": {"tx": 18, "ty": 29}, "facing": "down",
     "transition": "door"})

# ---- VINE A (sequential bloom; root + landing bands so a swim never skips it) -------
m["objects"] += [
    {"id": "vine_a_bloomed", "sprite": "sunvault_vine_v_bloomed",
     "at": {"tx": 9, "ty": 16}, "w": 1, "h": 3, "solid": False,
     "requires_flag": "flag:three_dawn_bloom_a"},
    {"id": "vine_a_withered", "sprite": "sunvault_vine_v_withered",
     "at": {"tx": 9, "ty": 16}, "w": 1, "h": 3, "solid": False,
     "hidden_when_flag": "flag:three_dawn_bloom_a"},
]
for i, (tx, ty) in enumerate([(9, 19), (9, 16)]):     # root, then landing
    m["triggers"].append(
        {"id": f"bloom_a_{i}", "kind": "script", "at": {"tx": tx, "ty": ty},
         "activation": "step_on", "ref": "script.three_dawn_bloom_a", "once": True,
         "requires_flag": "flag:three_dawn_poured",
         "sets_flags": ["flag:three_dawn_bloom_a"],
         "hidden_when_flag": "flag:three_dawn_bloom_a"})
owed += ["script.three_dawn_bloom_a (the basin's cupful wakes the first "
         "sun-vine; sets flag:three_dawn_bloom_a)"]

# ---- THE SUN-MIRROR FLOWER (the redirect) -------------------------------------------
m["objects"] += [
    {"id": "mirror_alight", "sprite": "sunvault_mirror_alight",
     "at": {"tx": 16, "ty": 12}, "w": 1, "h": 2,
     "requires_flag": "flag:three_dawn_bloom_b"},
    {"id": "mirror_dim", "sprite": "sunvault_mirror_dim",
     "at": {"tx": 16, "ty": 12}, "w": 1, "h": 2,
     "hidden_when_flag": "flag:three_dawn_bloom_b"},
]
m["triggers"].append(
    {"id": "dawn_mirror", "kind": "script", "at": {"tx": 16, "ty": 13},
     "activation": "interact", "ref": "script.three_dawn_mirror", "once": True,
     "requires_flag": "flag:three_dawn_bloom_a",
     "blocked_ref": "npc.unrisen_mirror_waits",
     "sets_flags": ["flag:three_dawn_bloom_b"],
     "hidden_when_flag": "flag:three_dawn_bloom_b"})
owed += ["script.three_dawn_mirror (the dish-bloom turns; the pocket of "
         "daylight lands across the water on the far vine; sets "
         "flag:three_dawn_bloom_b)",
         "npc.unrisen_mirror_waits (blocked: the dish-bloom sleeps until a "
         "nearer vine carries the light to it)"]

# ---- VINE B (the far vine; the east flight to the head terrace) ---------------------
m["objects"] += [
    {"id": "vine_b_bloomed", "sprite": "sunvault_vine_far_bloomed",
     "at": {"tx": 12, "ty": 8}, "w": 1, "h": 4, "solid": False,
     "requires_flag": "flag:three_dawn_bloom_b"},
    {"id": "vine_b_withered", "sprite": "sunvault_vine_far_withered",
     "at": {"tx": 12, "ty": 8}, "w": 1, "h": 4, "solid": False,
     "hidden_when_flag": "flag:three_dawn_bloom_b"},
]
for i, (tx, ty) in enumerate([(12, 12), (12, 8)]):    # root, then landing
    m["triggers"].append(
        {"id": f"bloom_b_{i}", "kind": "dialogue", "at": {"tx": tx, "ty": ty},
         "activation": "step_on", "ref": "npc.unrisen_stair_wakes", "once": True,
         "requires_flag": "flag:three_dawn_bloom_b",
         "blocked_ref": "npc.unrisen_far_vine"})
owed += ["npc.unrisen_stair_wakes (the east flight blooms underfoot — one "
         "narrate line)",
         "npc.unrisen_far_vine (blocked: the great vine sleeps beyond any "
         "pocket of daylight; something here must bend the light)"]

# ---- THE LOST HOUR ------------------------------------------------------------------
m["npcs"].append(
    {"id": "hour_dawn", "at": {"tx": 10, "ty": 5}, "facing": "right",
     "sprite": "kin_162_overworld", "movement": "static",
     "dialogue_ref": "script.three_dawn_battle",
     "requires_flag": "flag:three_dawn_bloom_b",
     "hidden_when_flag": "flag:three_dawn_caught"})
owed += ["script.three_dawn_battle (letterbox + silence 1200 -> the slow warm "
         "false-dawn tint, the Keystar rhyme -> narrate 'For one held breath, "
         "the stair remembers what it was for.' -> sting-hour -> battle-hours "
         "-> sets flag:three_dawn_met BEFORE the op (win or withdraw) -> the "
         "op VERBATIM in the docstring)",
         "npc.three_dawn_resting (the {remaining} cooldown hint — §7 verbatim)"]

# ---- the fallen capital + the MISSABLE shard (off flight two, west) -----------------
m["objects"] += [
    {"id": "capital_fallen", "sprite": "solarium_column_fallen",
     "at": {"tx": 3, "ty": 14}, "w": 3, "h": 1},
    # the terrace's broken colonnade (walk-under)
    {"id": "column_w", "sprite": "solarium_column", "at": {"tx": 6, "ty": 4},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_e", "sprite": "solarium_column", "at": {"tx": 15, "ty": 4},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_court", "sprite": "solarium_column", "at": {"tx": 4, "ty": 19},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    # a second toppled capital pays the court's east edge its idea (§3a r5)
    {"id": "capital_court", "sprite": "solarium_column_fallen",
     "at": {"tx": 13, "ty": 21}, "w": 3, "h": 1},
]
owed += pt.cache(m, cid="unrisen_shard", at=(4, 15))

# ---- dressing: blooms in the gold, a few stones -------------------------------------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (cliff, ruin, pool, gold))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
blooms = [gid("flowerbed_a"), gid("flowerbed_b")]
for y in range(H):
    for x in range(W):
        i = y * W + x
        if base[i] in gg and deco[i] == 0 and (x, y) not in avoid \
                and rng.random() < 0.12:
            deco[i] = rng.choice(blooms) if rng.random() < 0.5 else gid("g_pebble")
for (x, y) in [(13, 20), (5, 13), (8, 7), (13, 6), (15, 22)]:
    if (x, y) not in avoid and deco[y * W + x] == 0:
        deco[y * W + x] = gid("boulder")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
