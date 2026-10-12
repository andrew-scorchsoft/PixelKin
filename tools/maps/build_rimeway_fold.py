#!/usr/bin/env python3
"""
The Rimeway Fold (09-the-wild-ways §2 C; kind route, region north, band 40-42).
The high plateau at the top of the star-tenders' road: wind, dead rime-lamps,
the tenders' refuge, and the FROZEN FALLS — and at its head, the RIME GATE.

Lore (story-bible §11-§12): the Hollowing barred the Rime Gate from the MARSH
side eleven winters ago, to keep the coldfog in and the curious out — the high
road was the one way a lamp could still reach the drained country. From up
here you see the bar through the grille and the fog beyond; you can't lift it.
(Cinder law: a sleeping light starves its star — the tenders' lamps went dark
the night the gate shut, because nobody could bring the oil round.)

Three signature touches (§8):
  1. THE RIME GATE (north edge, cols 6-7): barred/open object pair on
     flag:rime_gate_open. From the Fold the gate is a locked door with a line
     (`npc.rime_gate_barred`); it is lifted from the Descent's side (West era).
  2. THE FROZEN FALLS over a plunge pool of glare ice — slide the stones to
     reach the falls' foot and cut the CLEAR-ICE CORE (`script.rimeway_ice_core`
     -> flag:rimeway_ice_core), the lens-grinder Isel's errand (-> the
     Frostglass Lens -> the Mirelights' ferry).
  3. THE TENDERS' REFUGE — a rest point (the Fold is two maps up from town),
     and the last star-tender, Hale, who still keeps one lamp.

HANDSHAKES:
  SOUTH (28,43)/(29,43) `to_ascent`/`_e` -> rimeway_ascent (4,1)/(5,1);
        the Ascent's `to_fold` lands at our (28,42)/(29,42).
  NORTH (6,0)/(7,0) `to_descent`/`_e` (requires flag:rime_gate_open, blocked_ref
        npc.rime_gate_barred) -> rimeway_descent (38,26)/(39,26); the Descent's
        `to_fold` (38,27)/(39,27) lands at our (6,1)/(7,1).
Geometry (north component frame): x 46..78, y 60..104.

Run:  python3 tools/maps/build_rimeway_fold.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 32, 44
rng = random.Random(9202)
owed: list[str] = []

c = fk.Canvas(W, H, ".")
c.rect(0, 0, W - 1, 1, "#").rect(0, 0, 1, H - 1, "#").rect(30, 0, 31, H - 1, "#")
c.rect(0, 43, W - 1, 43, "#")
c.rect(6, 0, 7, 2, "=")                       # THE RIME GATE's passage (north)
c.put([(5, 2), (8, 2)], "#")                  # the gate's piers
c.rect(28, 43, 29, 43, "=")                   # south: the Ascent
c.put([(2, 2), (2, 3), (29, 2), (28, 2), (29, 3), (2, 42), (29, 42), (2, 30)], "#")

# THE FROZEN FALLS' basin: cliff behind (rows 2-4), walls each side, the pool
c.rect(9, 2, 21, 4, "#").rect(9, 2, 9, 10, "#").rect(21, 2, 21, 10, "#")
c.rect(10, 5, 20, 10, "i")
POOL_STONES = [(10, 7), (10, 8), (12, 7), (12, 8), (15, 9), (16, 6), (16, 7), (16, 8),
               (20, 9)]                       # searched: 5 slides, no trap
c.put(POOL_STONES, "o")
# the band across the plateau (rows 22-26) + ladder (x10) + the east notch home
c.band(2, 29, 22, lip=2, face=3)
c.ladder(10, 22, 26)
c.rect(26, 22, 27, 25, ".").rect(26, 26, 27, 26, "v")

# roads (snowtrail)
c.rect(28, 37, 29, 42, "=").rect(12, 37, 29, 38, "=").rect(10, 27, 11, 38, "=")   # lower
c.rect(6, 3, 7, 20, "=").rect(6, 19, 10, 21, "=")                                 # gate road
c.rect(8, 13, 27, 14, "=").rect(24, 7, 25, 13, "=")                               # to the refuge
# frosttuft — the Fold's beds (Vaultclaw lives here)
c.rect(16, 27, 17, 36, '"').rect(16, 39, 17, 42, '"')     # MANDATORY: the lower plateau
c.rect(19, 27, 27, 33, '"')                   # the wind-bed (east)
c.rect(3, 31, 8, 36, '"')                     # west bed
c.rect(2, 15, 5, 20, '"')                     # upper west
c.rect(14, 16, 20, 20, '"')                   # upper middle
rows = c.rows()
# the mandatory crossing must cut the road at rows 37-38
for y in (37, 38):
    rows[y] = rows[y][:16] + '""' + rows[y][18:]

m: dict = {
    "id": "rimeway_fold", "display_name": "The Rimeway Fold",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/rimeway.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/rimeway-a.webp",
                         "assets/backgrounds/battle/rimeway-b.webp"],
}
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)
pin: dict = {}
g = fk.paint(m, rows, deco=deco, above=above, pin=pin, face="ice", ledge="snow", rng=rng)

fk.edge_warps(m, wid="to_ascent", cells=[(28, 43), (29, 43)], to_map="rimeway_ascent",
              to=[(4, 1), (5, 1)], facing="down")
fk.edge_warps(m, wid="to_descent", cells=[(6, 0), (7, 0)], to_map="rimeway_descent",
              to=[(38, 26), (39, 26)], facing="up", requires_flag="flag:rime_gate_open",
              blocked_ref="npc.rime_gate_barred")
owed.append("npc.rime_gate_barred")

# ---- THE RIME GATE (flag-pair swap; non-solid — the piers + warps do the work) -----
m["objects"] += [
    {"id": "rime_gate_barred", "sprite": "rimeway_rime_gate_barred", "at": {"tx": 5, "ty": 0},
     "w": 4, "h": 3, "overhang": 2, "solid": False, "hidden_when_flag": "flag:rime_gate_open"},
    {"id": "rime_gate_open", "sprite": "rimeway_rime_gate_open", "at": {"tx": 5, "ty": 0},
     "w": 4, "h": 3, "overhang": 2, "solid": False, "requires_flag": "flag:rime_gate_open"},
]
for x in (6, 7):
    m["triggers"].append({"id": f"rime_gate_look_{x}", "kind": "dialogue", "at": {"tx": x, "ty": 2},
                          "activation": "interact", "ref": "npc.rime_gate_barred",
                          "hidden_when_flag": "flag:rime_gate_open"})

# ---- THE FROZEN FALLS + the clear-ice core ------------------------------------------
m["objects"].append({"id": "frozen_falls", "sprite": "rimeway_frozen_falls",
                     "at": {"tx": 14, "ty": 2}, "w": 3, "h": 3})
m["triggers"].append({"id": "ice_core", "kind": "script", "at": {"tx": 15, "ty": 4},
                      "activation": "interact", "ref": "script.rimeway_ice_core"})
owed.append("script.rimeway_ice_core")
owed += pt.sign(m, deco, W, sid="rimeway_falls", at=(22, 11))

# ---- THE TENDERS' REFUGE (rest point) + Hale ----------------------------------------
m["objects"].append({"id": "tender_refuge", "sprite": "rimeway_tender_waystation",
                     "at": {"tx": 24, "ty": 4}, "w": 3, "h": 3, "overhang": 1})
m["triggers"].append({"id": "refuge_rest", "kind": "script", "at": {"tx": 25, "ty": 6},
                      "activation": "interact", "ref": "script.rimeway_refuge"})
owed.append("script.rimeway_refuge")
m["npcs"].append({"id": "tender_hale", "at": {"tx": 27, "ty": 7}, "facing": "left",
                  "sprite": "lamplighter", "movement": "static",
                  "dialogue_ref": "script.tender_hale"})
owed.append("script.tender_hale")

# ---- the rime-lamps (dead until the gate stands open) -------------------------------
LAMPS = [(5, 5), (8, 12), (5, 18), (12, 26 + 1), (13, 35), (24, 36), (27, 40), (20, 12), (26, 11)]
for n, (x, y) in enumerate(LAMPS):
    for state, flag in (("dead", "hidden_when_flag"), ("lit", "requires_flag")):
        m["objects"].append({"id": f"rime_lamp_{n}_{state}", "sprite": f"rimeway_rime_lamp_{state}",
                             "at": {"tx": x, "ty": y - 1}, "w": 1, "h": 2, "overhang": 1,
                             "walk_under": True, flag: "flag:rime_gate_open"})

# ---- trainers / caches / signs ------------------------------------------------------
owed += pt.trainer_beat(m, tid="rimeway_walker_sef", at=(13, 42), facing="up",
                        sight=6, sprite="pass_walker")
owed += pt.sign(m, deco, W, sid="rimeway_fold", at=(26, 40))
owed += pt.cache(m, cid="rimeway_cairn", at=(3, 39))
m["objects"].append({"id": "cairn_west", "sprite": "windward_cairn", "at": {"tx": 4, "ty": 38},
                     "w": 2, "h": 3, "overhang": 1})

# ---- encounters (40-42; night/day pairs; VAULTCLAW #76 lives only here) ---------------
NIGHT = [
    {"kin_id": 78, "weight": 21, "min_level": 40, "max_level": 42},  # Crystarn
    {"kin_id": 75, "weight": 18, "min_level": 40, "max_level": 42},  # Geodrake
    {"kin_id": 81, "weight": 16, "min_level": 40, "max_level": 41},  # Blizzrhare
    {"kin_id": 80, "weight": 14, "min_level": 40, "max_level": 41},  # Snowcune
    {"kin_id": 74, "weight": 12, "min_level": 40, "max_level": 41},  # Geolace
    {"kin_id": 77, "weight": 10, "min_level": 40, "max_level": 41},  # Chillpip
    {"kin_id": 76, "weight": 9, "min_level": 41, "max_level": 42},  # Vaultclaw (Fold-exclusive)
]
DAY = [
    {"kin_id": 78, "weight": 18, "min_level": 57, "max_level": 63},  # Crystarn
    {"kin_id": 75, "weight": 16, "min_level": 57, "max_level": 63},  # Geodrake
    {"kin_id": 81, "weight": 14, "min_level": 56, "max_level": 62},  # Blizzrhare
    {"kin_id": 80, "weight": 14, "min_level": 56, "max_level": 62},  # Snowcune
    {"kin_id": 74, "weight": 12, "min_level": 56, "max_level": 62},  # Geolace
    {"kin_id": 77, "weight": 12, "min_level": 56, "max_level": 61},  # Chillpip
    {"kin_id": 76, "weight": 14, "min_level": 58, "max_level": 64},  # Vaultclaw
]
band = mk.make_grid(W, H)
patch = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        (band if (i % W) in (16, 17) and (i // W) >= 29 else patch)[i] = 1
zones = pt.zones_from_grid(patch, W, H, terrain="tall_grass", rate=0.11, table=NIGHT,
                           id_prefix="fold")
zones += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.06, table=NIGHT,
                            id_prefix="crossing")
m["encounters"] = fk.night_day(zones, DAY)

# ---- dressing -----------------------------------------------------------------------
m["objects"] += [
    {"id": "spire_a", "sprite": "pale_vault_ice_spire", "at": {"tx": 3, "ty": 8}, "w": 2, "h": 3},
    {"id": "spire_b", "sprite": "pale_vault_ice_spire", "at": {"tx": 22, "ty": 30 - 1}, "w": 2, "h": 3},
    {"id": "pine_a", "sprite": "hushfrost_snow_pine", "at": {"tx": 27, "ty": 15}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "pine_b", "sprite": "hushfrost_snow_pine_big", "at": {"tx": 6, "ty": 27}, "w": 3, "h": 4,
     "overhang": 3, "walk_under": True},
    {"id": "outcrop", "sprite": "hushfrost_rock_outcrop_a", "at": {"tx": 22, "ty": 17}, "w": 3, "h": 2},
    {"id": "drift", "sprite": "hushfrost_snowdrift", "at": {"tx": 12, "ty": 40}, "w": 3, "h": 2},
    {"id": "icicles", "sprite": "hushfrost_icicle_outcrop", "at": {"tx": 18, "ty": 2 + 3 - 1}, "w": 3, "h": 2,
     "solid": False},
]
for n, (x, y) in enumerate([(12, 6), (18, 7), (4, 13), (27, 21), (9, 33)]):
    m["objects"].append({"id": f"glint_{n}", "sprite": rng.choice(
        ["hushfrost_aurora_glint_a", "hushfrost_aurora_glint_b"]),
        "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})

sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]
avoid = fk.busy_cells(m) | set(pin)
avoid |= {(x, y) for y in range(H) for x in range(W) if rows[y][x] != "." or deco[y * W + x]}
avoid |= {(x, 11) for x in range(9, 22)}      # the pool's bank stays clear (the reset lane)
litter = [gid("g_pebble"), gid("g_tuft")]
for y in range(H):
    for x in range(W):
        if (x, y) in avoid:
            continue
        r = rng.random()
        if r < 0.05:
            deco[y * W + x] = gid("boulder")
        elif r < 0.20:
            deco[y * W + x] = rng.choice(litter)

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_trail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": g["road"]},
    {"name": "t_tuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": g["tuft"]},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": g["cliff"]},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": above},
]

if __name__ == "__main__":
    import sys
    if "--show" in sys.argv:
        print("\n".join(f"{y:3d} {r}" for y, r in enumerate(rows)))
        best, traps = fk.ice_solve(rows, [(x, 11) for x in range(10, 21)], [(15, 5)],
                                   box=(9, 2, 21, 11))
        print("POOL: min slides", best, "traps", traps)
    ok = mk.finalize(m, scale=3, pin_base=pin)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
