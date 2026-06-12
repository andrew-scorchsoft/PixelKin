#!/usr/bin/env python3
"""
Sunvault Climb I — the overgrown golden terraces (walkthrough/04-west
"Sunvault Climb I→II" beat 1-2; kind route, region west, band 46-47, the
lower half). The brightest, most hopeful stretch of road in the region:
bone garden-steps, gold overgrowth, the dead sun-vine bridge framed at the
top of the climb from the moment you enter (§3a r3).

Three signature touches (§8):
  1. THE DEAD SUN-VINES at the north gorge — the I→II boundary, a bridge
     that died when the long night fell. Sunsketch's first REQUIRED
     crossing ("Sunsketch in anger", earned at Lucan just behind you).
     Withered until gleam:solar, blooming the moment the Gleam is held
     (the flag-pair swap; sunsketch and gleam:solar land together).
  2. THE TERRACE LADDER — the route climbs two tiers (stairs east, the
     one-way ledge west: out the long way, home the short way, §3a r1/r2).
  3. THE SOUTH POCKET — an overgrown lower garden under the entry road,
     the optional grind bed + a wicks find (braided risk-reward, §3a r4).

HANDSHAKE (W2-internal, built both sides): sunken_solarium `to_climb` at
(0,28)/(0,29) lands HERE at (28,14)/(28,15) — landings ON our return pair
`to_solarium`/`to_solarium_s` at (29,14)/(29,15), which land at the
solarium's (1,28)/(1,29). UNGATED both ways (§0 rule 1: the lower terraces
need no Gift; you can wander in BEFORE the Solar Gleam and read the tease).
BOUNDARY (graph.ts verbatim): `to_climb_ii` at (6,0)/(7,0), requires_ability
sunsketch BOTH directions (the vines are the boundary), blocked_ref
sign.sunvault_vines, landing sunvault_climb_ii (6,26)/(7,26); its return
pair `to_climb_i` at (6,27)/(7,27) lands at our (6,1)/(7,1).

Trainer beat (route class, payout 16 x ace — wiring agent authors):
  sunvault_terracer "Terrace-tender Bel", 2 kin lv46-47, ace 47, payout 752.

Encounter picks (band 46-47, continuous with the Solarium's 42-46): the
Solar/Verdant register with the kindled stage-2s weighting in — Sunsprout/
Helibud/Dawnfawn young, Solvyne/Helicore risen, Goldmane/Auravane/Sunstag
rare. (The atlas' "glass-wing bee" flavour name has no species row — the
N1 Kiteling precedent; the designed Solar/Verdant lines carry the register.)
Mirror into EXTRA_ENCOUNTERS (tools/balance/build_species.py) = wiring agent.

Suggested sign copy (wiring agent; the climb stays sincere — the cluster's
humour lives with the troupe at the Solarium):
  sign.sunvault_welcome "THE SUNVAULT CLIMB. The old garden-roads rise
                         toward the stars. Mind the overgrowth — it minds
                         you back."
  sign.sunvault_vines   "The bridge of sun-vines died with the long night.
                         Shut flowers, forty years. A pocket of daylight
                         would wake them." (the boundary blocked_ref + the
                         §3 'now accessible (Sunsketch)' callout)

audit_flow notes — the south pocket is a paid dead end (§3a r4); the west
ledge is the return compressor for the terrace ladder (§3a r1/r2).

Run:  ./venv/bin/python tools/maps/build_sunvault_climb_i.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 26
rng = random.Random(73)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
cliff = mk.make_grid(W, H)
ruin = mk.make_grid(W, H)       # the bone garden-road
goldtuft = mk.make_grid(W, H)
deco = mk.make_grid(W, H)

# BORDERS: terrace cliff all round, 2 deep, organic bumps
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.rect(cliff, W, H, 0, 24, W - 1, H - 1)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)
mk.rect(cliff, W, H, 28, 0, 29, H - 1)
mk.organic_border(cliff, W, H, depth=0,
                  bumps=[(10, 1, 2), (24, 1, 2), (1, 6, 2), (1, 20, 2),
                         (28, 5, 2), (28, 21, 2), (16, 25, 2)],
                  rng=rng)
# EAST gap — the solarium handshake (rows 14-15)
for x in (28, 29):
    for y in (14, 15):
        cliff[y * W + x] = 0
# NORTH gap — the gorge boundary to Climb II (cols 6-7)
for y in (0, 1):
    for x in (6, 7):
        cliff[y * W + x] = 0

# THE TERRACE LADDER: tier B (north, y2-9) over tier A (entry level, y12-17)
# over the south pocket (y20-23). Cliff bands separate the tiers.
mk.rect(cliff, W, H, 2, 10, 27, 11)           # band A/B
mk.blob(cliff, W, H, 14.0, 10.0, 2.0, 1.1)
mk.rect(cliff, W, H, 2, 18, 27, 19)           # band A/pocket
mk.blob(cliff, W, H, 9.0, 18.5, 1.8, 1.0)
# the STAIR pierce up to tier B (east side — the long way round)
for y in (10, 11):
    for x in (22, 23):
        cliff[y * W + x] = 0
# the one-way LEDGE back down (west side — the §3a return compressor)
for y in (10, 11):
    for x in (8, 9, 10):
        cliff[y * W + x] = 0
pt.ledge_run(deco, W, H, 10, 8, 10, rng, family="sand")
mk.rect(cliff, W, H, 8, 11, 10, 11, 0)        # the hop lands on tier A's top row
# the pocket pierce (south-east — the optional lower garden)
for y in (18, 19):
    for x in (24, 25):
        cliff[y * W + x] = 0

# ---- the garden-road (ruinfloor lanes; §3a r11 S-bends) -----------------------------
mk.rect(ruin, W, H, 6, 14, 29, 15)            # the entry road west
mk.rect(ruin, W, H, 6, 12, 7, 17)             # west landing under the ledge
mk.rect(ruin, W, H, 22, 12, 23, 15)           # the stair approach
mk.rect(ruin, W, H, 22, 8, 23, 11)            # the stair itself
mk.rect(ruin, W, H, 4, 8, 23, 9)              # tier B road west
mk.rect(ruin, W, H, 6, 2, 7, 9)               # north to the gorge
# jogs so the long roads never run ruled
mk.rect(ruin, W, H, 12, 13, 14, 13)
mk.rect(ruin, W, H, 17, 16, 19, 16)
mk.rect(ruin, W, H, 10, 7, 12, 7)
mk.rect(ruin, W, H, 16, 10, 17, 10)

# ---- encounter terrain --------------------------------------------------------------
mk.blob(goldtuft, W, H, 14.0, 21.5, 3.4, 1.8)  # the south pocket bed (optional)
mk.blob(goldtuft, W, H, 16.0, 4.5, 2.6, 1.6)   # tier B upper garden (optional)
mk.blob(goldtuft, W, H, 4.0, 13.5, 1.8, 1.2)   # west landing tuft
# MANDATORY crossing on tier B (§11 r7): tier B is 8 rows tall, so the band
# is VERTICAL — overgrowth swallowing the road's full corridor height at
# x12-13 (no walking around it along the upper garden), plus the road's own
# pause where the horizontal stretch meets it
pt.mandatory_band(goldtuft, ruin, W, H, y0=8, y1=9, x0=11, x1=14)
for y in range(2, 10):
    for x in (12, 13):
        i = y * W + x
        if not cliff[i]:
            goldtuft[i] = 1
            ruin[i] = 0

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if cliff[i]:
        ruin[i] = 0
        goldtuft[i] = 0
    if ruin[i]:
        goldtuft[i] = 0

# ---- base: gold grass ---------------------------------------------------------------
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": ruin},
    {"name": "t_goldtuft", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": goldtuft},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

m: dict = {
    "id": "sunvault_climb_i", "display_name": "Sunvault Climb",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/sunvault-climb-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/sunvault-climb-a.webp",
        "assets/backgrounds/battle/sunvault-climb-b.webp",
    ],
}

# ---- warps (graph.ts edge ids verbatim) ---------------------------------------------
m["warps"] += [
    # EAST <-> sunken_solarium (UNGATED both ways)
    {"id": "to_solarium", "at": {"tx": 29, "ty": 14}, "trigger": "step_on",
     "to_map": "sunken_solarium", "to": {"tx": 1, "ty": 28}, "facing": "right",
     "transition": "fade"},
    {"id": "to_solarium_s", "at": {"tx": 29, "ty": 15}, "trigger": "step_on",
     "to_map": "sunken_solarium", "to": {"tx": 1, "ty": 29}, "facing": "right",
     "transition": "fade"},
    # NORTH -> sunvault_climb_ii (`to_climb_ii`, SUNSKETCH — the dead vines;
    # gated BOTH directions, the W1 fog pattern)
    {"id": "to_climb_ii", "at": {"tx": 6, "ty": 0}, "trigger": "step_on",
     "to_map": "sunvault_climb_ii", "to": {"tx": 6, "ty": 26}, "facing": "up",
     "requires_ability": "sunsketch",
     "blocked_ref": "sign.sunvault_vines", "transition": "fade"},
    {"id": "to_climb_ii_e", "at": {"tx": 7, "ty": 0}, "trigger": "step_on",
     "to_map": "sunvault_climb_ii", "to": {"tx": 7, "ty": 26}, "facing": "up",
     "requires_ability": "sunsketch",
     "blocked_ref": "sign.sunvault_vines", "transition": "fade"},
]

# ---- THE DEAD SUN-VINE BRIDGE at the gorge (the flag-pair swap) ---------------------
m["objects"] += [
    {"id": "gorge_vines_bloomed", "sprite": "sunvault_vine_gate_bloomed",
     "at": {"tx": 6, "ty": 0}, "w": 2, "h": 3, "solid": False,
     "requires_flag": "gleam:solar"},
    {"id": "gorge_vines_withered", "sprite": "sunvault_vine_gate_withered",
     "at": {"tx": 6, "ty": 0}, "w": 2, "h": 3, "solid": False,
     "hidden_when_flag": "gleam:solar"},
]

# ---- signs --------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="sunvault_welcome", at=(26, 13))
owed += pt.sign(m, deco, W, sid="sunvault_vines", at=(8, 3))

# ---- trainer beat (the terrace road — her line covers the entry corridor) ----------
owed += pt.trainer_beat(m, tid="sunvault_terracer", at=(15, 12), facing="right",
                        sight=4, sprite="npc_woman")

# ---- a resting wayfarer (the "last bright calm road" beat — top up and bond) -------
m["npcs"].append({
    "id": "sunvault_wayfarer", "at": {"tx": 18, "ty": 7}, "facing": "down",
    "sprite": "npc_old_man", "movement": "static",
    "dialogue_ref": "npc.sunvault_wayfarer"})
owed += ["npc.sunvault_wayfarer (rests by the tier-B road: the last calm "
         "stretch before the eighth Lumenary — sincere, warm)"]

# ---- caches (variety: consumable off-lane, loose wicks in the pocket) ---------------
owed += pt.cache(m, cid="sunvault_balm", at=(17, 3))     # consumable, tier B garden
owed += pt.cache(m, cid="sunvault_wicks", at=(12, 22))   # loose wicks, south pocket

# ---- encounters (band 46-47; stage-2 forms weight in) -------------------------------
TABLE_SV1 = [
    {"kin_id": 114, "weight": 18, "min_level": 46, "max_level": 47},  # Sunsprout
    {"kin_id": 117, "weight": 16, "min_level": 46, "max_level": 47},  # Helibud
    {"kin_id": 120, "weight": 14, "min_level": 46, "max_level": 47},  # Dawnfawn
    {"kin_id": 115, "weight": 14, "min_level": 46, "max_level": 48},  # Solvyne
    {"kin_id": 118, "weight": 12, "min_level": 46, "max_level": 48},  # Helicore
    {"kin_id": 103, "weight": 10, "min_level": 46, "max_level": 47},  # Gilpaw
    {"kin_id": 104, "weight": 7, "min_level": 47, "max_level": 48},   # Goldmane
    {"kin_id": 116, "weight": 5, "min_level": 47, "max_level": 48},   # Auravane
    {"kin_id": 121, "weight": 4, "min_level": 47, "max_level": 48},   # Sunstag
]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if goldtuft[i]:
        (band_grid if (i // W) in (8, 9) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE_SV1, id_prefix="terrace")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE_SV1, id_prefix="crossing")

# ---- dressing: columns, lamps, gold blooms ------------------------------------------
m["objects"] += [
    {"id": "column_a", "sprite": "solarium_column", "at": {"tx": 11, "ty": 15},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_b", "sprite": "solarium_column", "at": {"tx": 20, "ty": 3},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_fallen_a", "sprite": "solarium_column_fallen",
     "at": {"tx": 18, "ty": 21}, "w": 3, "h": 1},
    {"id": "column_fallen_b", "sprite": "solarium_column_fallen",
     "at": {"tx": 3, "ty": 5}, "w": 3, "h": 1},
    {"id": "lamp_entry", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 26, "ty": 11}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_gorge", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 4, "ty": 2}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_pocket", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 23, "ty": 20}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (cliff, ruin, goldtuft))}
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
            deco[i] = rng.choice(blooms) if rng.random() < 0.5 else gid("boulder")
for (x, y) in [(4, 16), (26, 6), (13, 5), (5, 22), (27, 17)]:
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
