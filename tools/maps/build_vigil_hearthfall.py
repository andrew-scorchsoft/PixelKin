#!/usr/bin/env python3
"""
Vigil I — Hearthfall (`vigil_hearthfall`) — "where the first lamp learned its
name" (walkthrough/06-postgame §STARFALL VIGILS, the one-shape annex stamped
five times). A wind-bitten grass bluff above Tinderwick's Beacon, in FULL
DAYLIGHT (post-`flag:dawn` content — the dawngrass register), the sea along
the east, the first star-shard seated in its crater at the bluff's head.

The one shape: shard set-piece far end · Wick-Mother Esra posted before it
behind an un-walk-aroundable step_on trial band (`script.vigil_hearthfall`,
hidden once `flag:vigil_1_kept`) · three flag-disjoint keeper placements
(trial -> kept -> post-crown re-runnable bout, the Fenn-waystone pattern) ·
two encounter zones in the 58-60 band (dawntuft bed + the Tidecall shore:
EMBRALUX #33 and TIDEVEIL #34 very rare — the register ledger's southern
pair) · one starglass cache · NO rest point.

Host edit (tools/maps/add_vigil_scars.py): tinderwick (25,7) `to_vigil_hearth`,
`requires_flag: flag:vigil_reading_1`. Reuse: tinderwick-a loop + backdrops.

audit_flow note — a one-portal dead-end annex (like thunderroost): no
through-pair, the screen IS the payoff (§3a r5); the trial band rides the
alcove's only mouth so it cannot be walked around.

Run:  ./venv/bin/python tools/maps/build_vigil_hearthfall.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 18
rng = random.Random(331)
owed: list[str] = []

ENTRY = (11, 16)          # tinderwick's to_vigil_hearth lands here (ON the return warp)
SHARD_AT = (11, 2)        # 2x2 set-piece
KEEPER_AT = (11, 4)       # Esra, posted before the shard
BAND_Y, BAND_X = 6, (10, 13)   # the trial band across the alcove's only mouth

# ---- terrain ------------------------------------------------------------------------
water = mk.make_grid(W, H)     # the sea, east + south-east
mk.rect(water, W, H, 19, 0, W - 1, H - 1)
mk.blob(water, W, H, 18.5, 14.5, 3.6, 3.2)     # the SE bight
mk.blob(water, W, H, 19.0, 4.0, 2.0, 2.6)      # a northern inlet

cliff = mk.make_grid(W, H)     # the bluff rim + the alcove flanks
mk.rect(cliff, W, H, 0, 0, W - 1, 1)           # north rim
mk.rect(cliff, W, H, 0, 0, 1, H - 1)           # west rim
mk.rect(cliff, W, H, 0, 16, 17, H - 1)         # south rim (the sea takes the rest)
mk.organic_border(cliff, W, H, depth=0, bumps=[(2, 8, 1), (5, 16, 1), (2, 13, 1)], rng=rng)
mk.rect(cliff, W, H, 2, 2, 9, 6)               # alcove west flank
mk.rect(cliff, W, H, 14, 2, 15, 6)             # alcove east flank (the sea does the rest)
# the entry notch (the seam the starfall tore open) — ONE tile, the warp
cliff[16 * W + 11] = 0

# cliffs never stand in the sea
for i in range(W * H):
    if water[i]:
        cliff[i] = 0

# sand: every land cell touching water becomes shore (water edges are
# sand-context in the shared set — the standing rule)
sand = mk.make_grid(W, H)
for y in range(H):
    for x in range(W):
        i = y * W + x
        if water[i] or cliff[i]:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and water[ny * W + nx]:
                sand[i] = 1
                break
mk.rect(sand, W, H, 16, 7, 17, 13)             # the walkable shore strip
for i in range(W * H):
    if cliff[i] or water[i]:
        sand[i] = 0

# the dawntuft bed (the 58-60 grind bed) — one hard-edged blob mid-bluff
tuft = mk.make_grid(W, H)
mk.blob(tuft, W, H, 6.5, 10.5, 3.2, 2.4)
mk.blob(tuft, W, H, 9.5, 12.5, 1.6, 1.3)       # spills toward the lane (same zone)
for i in range(W * H):
    if cliff[i] or water[i] or sand[i]:
        tuft[i] = 0
for (x, y) in [(10, 14), (11, 14), (10, 15), (11, 15), (12, 14)]:
    tuft[y * W + x] = 0                         # keep the entry lane clear

terrain_layers = [
    {"name": "t_tuft", "role": "terrain", "terrain": "dawntuft",
     "set": "vesper_overworld_set", "depth": 0, "data": tuft},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

# ---- base: daylit grass (the post-dawn register) -------------------------------------
gg = [gid("dawngrass0"), gid("dawngrass1"), gid("dawngrass2"), gid("dawngrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

m: dict = {
    "id": "vigil_hearthfall", "display_name": "Hearthfall",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [
        # THE SHARD — the first fall, seated where the gulls go quiet
        {"id": "star_shard", "sprite": "vigil_star_shard",
         "at": {"tx": SHARD_AT[0], "ty": SHARD_AT[1]}, "w": 2, "h": 2},
        # a wind-bent tree on the bluff shoulder (composition accent)
        {"id": "bluff_tree", "sprite": "tinderwick_tree", "at": {"tx": 3, "ty": 8},
         "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    ],
    "warps": [
        # back down the seam to Tinderwick — lands ON the host's to_vigil_hearth
        {"id": "to_tinderwick", "at": {"tx": ENTRY[0], "ty": ENTRY[1]},
         "trigger": "step_on", "to_map": "tinderwick", "to": {"tx": 25, "ty": 7},
         "facing": "down", "transition": "fade"},
    ],
    "triggers": [
        # THE TRIAL BAND — every walkable tile of the alcove mouth (the
        # un-walk-aroundable rule); a loss re-arms (no `once`), the kept
        # flag retires it. The script owes Esra's intro -> battle -> rewards.
        *[{"id": f"vigil_trial_{i}", "kind": "cutscene",
           "at": {"tx": x, "ty": BAND_Y}, "activation": "step_on",
           "ref": "script.vigil_hearthfall",
           "hidden_when_flag": "flag:vigil_1_kept"}
          for i, x in enumerate(range(BAND_X[0], BAND_X[1] + 1))],
    ],
    "encounters": [],
    "npcs": [
        # WICK-MOTHER ESRA — three flag-disjoint placements (the Fenn-waystone
        # pattern): trial keeper -> kept (plain line) -> post-crown re-runnable bout.
        {"id": "esra_trial", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.vigil_hearthfall",
         "hidden_when_flag": "flag:vigil_1_kept"},
        {"id": "esra_kept", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "npc.vigil_hearthfall_kept",
         "requires_flag": "flag:vigil_1_kept",
         "hidden_when_flag": "flag:starfall_crown"},
        {"id": "esra_bout", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.vigil_hearthfall_again",
         "requires_flag": "flag:starfall_crown"},
    ],
    "gates": [],
    # the one-shape reuse rule: the HOST's loop + backdrops
    "music": "assets/audio/music/tinderwick-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/tinderwick-a.webp",
        "assets/backgrounds/battle/tinderwick-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- the cache (starglass_shard x1 — content lane authors the pickup) ----------------
deco[13 * W + 4] = gid("boulder")
deco[12 * W + 3] = gid("boulder")
owed += pt.cache(m, cid="vigil_hearth_glass", at=(3, 14))

# ---- encounters: the spec tables VERBATIM (06-postgame, Vigil I hooks) ---------------
GRASS_TABLE = [
    {"kin_id": 17, "weight": 40, "min_level": 58, "max_level": 60},  # Scorchwing (uncommon)
    {"kin_id": 12, "weight": 37, "min_level": 58, "max_level": 60},  # Chandrek (uncommon)
    {"kin_id": 7, "weight": 15, "min_level": 59, "max_level": 60},   # Wicklord (rare)
    {"kin_id": 33, "weight": 8, "min_level": 60, "max_level": 60},   # EMBRALUX (very rare)
]
WATER_TABLE = [
    {"kin_id": 25, "weight": 90, "min_level": 58, "max_level": 60},  # Prismare (uncommon)
    {"kin_id": 34, "weight": 10, "min_level": 60, "max_level": 60},  # TIDEVEIL (very rare)
]
m["encounters"] += pt.zones_from_grid(tuft, W, H, terrain="tall_grass",
                                      rate=0.12, table=GRASS_TABLE, id_prefix="hearth_bluff")
zones = pt.zones_from_grid(water, W, H, terrain="water",
                           rate=0.09, table=WATER_TABLE, id_prefix="hearth_surf")
for z in zones:
    z["requires_ability"] = "tidecall"
m["encounters"] += zones

# Tidecall gates as PURE-WATER row runs (the make_passable gotcha)
gi = 0
for y in range(H):
    x = 0
    while x < W:
        if water[y * W + x]:
            x0 = x
            while x < W and water[y * W + x]:
                x += 1
            m["gates"].append({"id": f"surf_gate_{gi}", "ability": "tidecall",
                               "effect": "make_passable",
                               "rect": {"tx": x0, "ty": y, "w": x - x0, "h": 1}})
            gi += 1
        else:
            x += 1

# ---- daylight dressing ----------------------------------------------------------------
avoid = {(x, BAND_Y) for x in range(BAND_X[0], BAND_X[1] + 1)}
avoid |= {ENTRY, KEEPER_AT, (3, 14)}
avoid |= {(x, y) for o in m["objects"]
          for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
          for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
for (x, y, name) in [(13, 9, "g_daisy"), (8, 8, "flowers"), (14, 12, "g_tuft"),
                     (5, 15, "g_pebble"), (12, 11, "g_daisy"), (16, 6, "g_pebble"),
                     (13, 4, "g_patch"), (10, 3, "flowers")]:
    i = y * W + x
    if not (cliff[i] or water[i] or tuft[i] or sand[i]) and (x, y) not in avoid and deco[i] == 0:
        deco[i] = gid(name)
# a buoy line out in the bight (the sea remembers the harbour)
for (x, y) in [(20, 9), (18, 16), (22, 4)]:
    if water[y * W + x]:
        deco[y * W + x] = gid("buoy")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
