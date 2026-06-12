#!/usr/bin/env python3
"""
Vigil IV — Sunfall (`vigil_sunfall`) — "where summer was put away for
safekeeping" (walkthrough/06-postgame §STARFALL VIGILS, the one-shape annex).
A golden terrace-garden fold above Sunvault Climb II: sun-vines blooming wild
now the sky does the work, the fourth star-shard resting in a cracked
sun-basin (a ruinfloor court), dreamlight pooling where its glow meets the
stone — the one site played in two lights.

The one shape: shard set-piece far end · Dame Solenne posted before it behind
the un-walk-aroundable trial band (`script.vigil_sunfall`, hidden once
`flag:vigil_4_kept`) · three flag-disjoint keeper placements · two goldtuft
encounter zones in the 64-66 band (DAWNWATCHER #129 and HELITHORN #119 very
rare — the register ledger's western pair) · one starglass cache · NO rest
point.

Host edit (add_vigil_scars.py): sunvault_climb_ii (27,2) `to_vigil_sun`,
`requires_flag: flag:vigil_reading_4`. Reuse: sunvault-climb-a loop +
backdrops (the host's keys).

audit_flow note — a one-portal dead-end annex: the screen IS the payoff
(§3a r5); the trial band rides the basin court's only mouth.

Run:  ./venv/bin/python tools/maps/build_vigil_sunfall.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 18
rng = random.Random(334)
owed: list[str] = []

ENTRY = (11, 16)          # sunvault_climb_ii's to_vigil_sun lands here
SHARD_AT = (11, 2)
KEEPER_AT = (11, 4)
BAND_Y, BAND_X = 6, (10, 13)
CACHE_AT = (3, 4)

# ---- terrain ------------------------------------------------------------------------
cliff = mk.make_grid(W, H)     # the terrace fold's walls + the court flanks
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)
mk.rect(cliff, W, H, 22, 0, 23, H - 1)
mk.rect(cliff, W, H, 0, 16, W - 1, H - 1)
mk.organic_border(cliff, W, H, depth=0,
                  bumps=[(21, 9, 1), (2, 12, 1), (15, 16, 1)], rng=rng)
mk.rect(cliff, W, H, 2, 2, 9, 6)               # court west flank
mk.rect(cliff, W, H, 14, 2, 21, 6)             # court east flank
cliff[16 * W + 11] = 0                          # the entry seam (ENTRY)
# the cache garden: a walled pocket carved INTO the west flank, mouth at (5,7)
for (x, y) in [(3, 4), (4, 4), (3, 5), (4, 5), (5, 5), (5, 6)]:
    cliff[y * W + x] = 0

# the sun-basin court (ruinfloor): the alcove floor + a weathered apron below
ruin = mk.make_grid(W, H)
mk.rect(ruin, W, H, 10, 2, 13, 6)
mk.blob(ruin, W, H, 11.5, 9.0, 2.2, 1.5)
for i in range(W * H):
    if cliff[i]:
        ruin[i] = 0

# dreamlight pooling in the basin's crack (sunpool: scenery, kept off the lane)
pool = mk.make_grid(W, H)
pool[3 * W + 13] = 1
pool[2 * W + 13] = 1
for i in range(W * H):
    if cliff[i]:
        pool[i] = 0

# the garden beds run wild (the 64-66 grind beds; two zones by design)
tuft = mk.make_grid(W, H)
mk.blob(tuft, W, H, 5.5, 11.5, 2.8, 2.2)
mk.blob(tuft, W, H, 17.0, 11.0, 2.8, 2.0)
for i in range(W * H):
    if cliff[i] or ruin[i] or pool[i]:
        tuft[i] = 0
for (x, y) in [(11, 14), (11, 15), (10, 14), (12, 14)]:
    tuft[y * W + x] = 0                         # keep the entry lane clear

terrain_layers = [
    {"name": "t_tuft", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": tuft},
    {"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": ruin},
    {"name": "t_pool", "role": "terrain", "terrain": "sunpool",
     "set": "vesper_overworld_set", "depth": 0, "data": pool},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

# ---- base: the gold terraces ------------------------------------------------------------
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

m: dict = {
    "id": "vigil_sunfall", "display_name": "Sunfall",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [
        # THE SHARD — resting in the cracked sun-basin, warm to look at
        {"id": "star_shard", "sprite": "vigil_star_shard",
         "at": {"tx": SHARD_AT[0], "ty": SHARD_AT[1]}, "w": 2, "h": 2, "overhang": 1},
        # the court's columns, the vine doing the sky's old work over the mouth
        {"id": "court_col_w", "sprite": "solarium_column", "at": {"tx": 9, "ty": 5},
         "w": 1, "h": 3, "overhang": 1},
        {"id": "court_col_e", "sprite": "solarium_column", "at": {"tx": 14, "ty": 5},
         "w": 1, "h": 3, "overhang": 1},
        {"id": "court_vine", "sprite": "sunvault_vine_h_bloomed", "at": {"tx": 10, "ty": 1},
         "w": 3, "h": 1, "solid": False},
        # a fallen column among the beds (summer, put away)
        {"id": "fallen_col", "sprite": "solarium_column_fallen", "at": {"tx": 15, "ty": 14},
         "w": 3, "h": 1},
    ],
    "warps": [
        # back down the fold — lands ON sunvault_climb_ii's to_vigil_sun
        {"id": "to_sunvault", "at": {"tx": ENTRY[0], "ty": ENTRY[1]},
         "trigger": "step_on", "to_map": "sunvault_climb_ii", "to": {"tx": 27, "ty": 2},
         "facing": "down", "transition": "fade"},
    ],
    "triggers": [
        # THE TRIAL BAND — every walkable tile of the basin court's mouth
        *[{"id": f"vigil_trial_{i}", "kind": "cutscene",
           "at": {"tx": x, "ty": BAND_Y}, "activation": "step_on",
           "ref": "script.vigil_sunfall",
           "hidden_when_flag": "flag:vigil_4_kept"}
          for i, x in enumerate(range(BAND_X[0], BAND_X[1] + 1))],
    ],
    "encounters": [],
    "npcs": [
        # DAME SOLENNE — trial -> kept -> post-crown re-runnable bout
        {"id": "solenne_trial", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.vigil_sunfall",
         "hidden_when_flag": "flag:vigil_4_kept"},
        {"id": "solenne_kept", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "npc.vigil_sunfall_kept",
         "requires_flag": "flag:vigil_4_kept",
         "hidden_when_flag": "flag:starfall_crown"},
        {"id": "solenne_bout", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.vigil_sunfall_again",
         "requires_flag": "flag:starfall_crown"},
    ],
    "gates": [],
    # the one-shape reuse rule: the HOST's loop + backdrops
    "music": "assets/audio/music/sunvault-climb-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/sunvault-climb-a.webp",
        "assets/backgrounds/battle/sunvault-climb-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- the cache (starglass_shard x1) in the walled garden pocket ------------------------
owed += pt.cache(m, cid="vigil_sun_glass", at=CACHE_AT)

# ---- encounters: the spec table VERBATIM (06-postgame, Vigil IV hooks) -----------------
SUN_TABLE = [
    {"kin_id": 121, "weight": 25, "min_level": 64, "max_level": 66},  # Sunstag (uncommon)
    {"kin_id": 123, "weight": 24, "min_level": 64, "max_level": 66},  # Solreach (uncommon)
    {"kin_id": 125, "weight": 20, "min_level": 64, "max_level": 66},  # Crystalune (uncommon)
    {"kin_id": 110, "weight": 16, "min_level": 64, "max_level": 66},  # Lunaquell (rare)
    {"kin_id": 129, "weight": 8, "min_level": 65, "max_level": 65},   # DAWNWATCHER (very rare)
    {"kin_id": 119, "weight": 7, "min_level": 66, "max_level": 66},   # HELITHORN (very rare)
]
m["encounters"] += pt.zones_from_grid(tuft, W, H, terrain="tall_grass",
                                      rate=0.12, table=SUN_TABLE, id_prefix="sun_bed")

# ---- the garden gone wild ----------------------------------------------------------------
avoid = {(x, BAND_Y) for x in range(BAND_X[0], BAND_X[1] + 1)}
avoid |= {ENTRY, KEEPER_AT, CACHE_AT}
avoid |= {(x, y) for o in m["objects"]
          for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
          for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
for (x, y, name) in [(8, 9, "flowers"), (14, 9, "g_daisy"), (4, 8, "flowerbed_a"),
                     (19, 8, "flowerbed_b"), (7, 14, "g_daisy"), (13, 12, "flowers"),
                     (3, 14, "g_tuft"), (20, 14, "g_pebble"), (5, 6, "g_patch")]:
    i = y * W + x
    if not (cliff[i] or ruin[i] or pool[i] or tuft[i]) and (x, y) not in avoid and deco[i] == 0:
        deco[i] = gid(name)

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
