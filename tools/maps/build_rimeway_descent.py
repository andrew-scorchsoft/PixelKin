#!/usr/bin/env python3
"""
The Rimeway Descent (09-the-wild-ways §2 C; kind route, region outer, band
46-48). The marsh end of the star-tenders' high road: out of Coldfog Marches
II's east edge, up a ladder off the drained fen onto the col ridge, along the
ridge and down the far band to the RIME GATE — whose bar is on THIS side.

Lore (story-bible §11-§12; the Hollowing is sympathetic, never cartoonish):
eleven winters ago the Wardens of the Quiet barred the gate from below "to
keep the coldfog in and the curious out" — the high road was the one way a
lamp could still reach the drained country, and they wanted the marsh left
asleep. An acolyte still keeps the bar; she doesn't stop you lifting it.

Signature touches (§8):
  1. THE BAR (south edge, cols 38-39): walk onto the yard before the gate and
     you lift it (`script.rime_gate_lift`, a step_on band that sets
     flag:rime_gate_open) — from then on the Rimeway is open both ways, a
     return compressor Coldfog <-> Pale Vault, and the rime-lamps along the
     whole road wake (their dead/lit swap rides the same flag).
  2. THE COL RIDGE — the drained fen below, the ridge road above: ladder up
     (west), ladder down (east); the WEST NOTCH ledge is the quick way back
     down to the marsh.
  3. THE ACOLYTE AT THE BAR — the Hollowing's side of it, in one quiet scene.

HANDSHAKES:
  WEST  (0,14)/(0,15) `to_coldfog`/`_s` -> coldfog_marches_ii (28,16)/(28,17);
        Coldfog II's `to_rimeway`/`_s` (29,16)/(29,17) land at our (1,14)/(1,15).
  SOUTH (38,27)/(39,27) `to_fold`/`_e` (requires flag:rime_gate_open,
        blocked_ref npc.rime_gate_wrongside) -> rimeway_fold (6,1)/(7,1); the
        Fold's `to_descent` lands at our (38,26)/(39,26).
  NORTH (16..19,0) `to_fields` (Lane N3, walkthrough/11 Part C) -> mourning_fields
        (10..13,30); the Fields' `to_rimeway` (10..13,31) lands at our (16..19,1).
Geometry (world_geometry frame): x 62..104, y -429..-401.

Run:  python3 tools/maps/build_rimeway_descent.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 42, 28
rng = random.Random(9203)
owed: list[str] = []

c = fk.Canvas(W, H, ".")
c.rect(0, 0, W - 1, 1, "#").rect(0, 0, 1, H - 1, "#").rect(40, 0, 41, H - 1, "#")
c.rect(0, 27, W - 1, 27, "#")
c.rect(16, 0, 19, 1, ".")                     # north: up to the Mourning Fields (Lane N3)
c.rect(0, 14, 1, 15, "=")                     # west: the marsh
c.rect(38, 25, 39, 27, "=")                   # south: THE RIME GATE's passage
c.put([(37, 25), (37, 26), (40, 25), (40, 26)], "#")   # the gate's piers
c.put([(2, 2), (39, 2), (38, 2), (39, 3), (2, 26), (3, 26), (2, 12)], "#")

# band A (rows 8-11) between the fen (south-west) and the ridge (north)
c.band(2, 26, 8, lip=2, face=2)
c.ladder(12, 8, 11)
c.rect(4, 8, 5, 10, ".").rect(4, 11, 5, 11, "v")      # the west notch home
# the divide: the fen and the gate yard never touch
c.rect(25, 12, 26, 26, "#")
# band B (rows 13-16) across the east, the far ladder down to the gate yard
c.band(27, 39, 13, lip=2, face=2)
c.ladder(34, 13, 16)

# roads (snowtrail on the col; the fen keeps its own drained ground)
c.rect(2, 14, 12, 15, "=").rect(12, 12, 12, 15, "=")                 # fen road
c.rect(17, 0, 18, 3, "=")                     # the field road down onto the ridge
c.rect(12, 4, 13, 7, "=").rect(12, 4, 34, 5, "=").rect(34, 5, 34, 12, "=")   # ridge
c.rect(34, 17, 35, 20, "=").rect(34, 20, 39, 21, "=").rect(38, 21, 39, 24, "=")  # gate yard
# tufts
c.rect(7, 12, 8, 26, '"')                     # MANDATORY: the fen, full height
c.rect(16, 18, 23, 24, '"')                   # the fen's deep bed
c.rect(20, 2, 25, 3, '"').rect(26, 6, 31, 7, '"')   # ridge beds
c.rect(28, 22, 33, 25, '"')                   # the gate yard bed
c.rect(2, 5, 4, 7, '"')                      # the ridge's west corner
rows = c.rows()
for y in (14, 15):                            # the mandatory band cuts the fen road
    rows[y] = rows[y][:7] + '""' + rows[y][9:]

COLDFOG_REF = mk.register_tileset(
    "coldfog_set", index=mk.REPO / "assets/tilesets/coldfog/coldfog_set.index.json")
m: dict = {
    "id": "rimeway_descent", "display_name": "The Rimeway",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref(), COLDFOG_REF],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/rimeway.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/rimeway-a.webp",
                         "assets/backgrounds/battle/rimeway-b.webp"],
}
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)
pin: dict = {}
g = fk.paint(m, rows, deco=deco, above=above, pin=pin, face="rock", ledge="scree", rng=rng)

FEN = {(x, y) for y in range(12, 27) for x in range(2, 25)}     # the drained fen
murk = mk.make_grid(W, H)
mk.blob(murk, W, H, 19.0, 14.5, 2.4, 1.4)
mk.blob(murk, W, H, 4.0, 21.5, 1.6, 2.0)
mk.blob(murk, W, H, 12.0, 24.0, 2.0, 1.0)
for i in range(W * H):
    x, y = i % W, i // W
    if rows[y][x] != "." or (x, y) not in FEN:
        murk[i] = 0
blighttuft = [v if (i % W, i // W) in FEN else 0 for i, v in enumerate(g["tuft"])]
frosttuft = [v if (i % W, i // W) not in FEN else 0 for i, v in enumerate(g["tuft"])]

fk.edge_warps(m, wid="to_coldfog", cells=[(0, 14), (0, 15)], to_map="coldfog_marches_ii",
              to=[(28, 16), (28, 17)], facing="left", suffix="_s")
fk.edge_warps(m, wid="to_fields", cells=[(x, 0) for x in (16, 17, 18, 19)],
              to_map="mourning_fields", to=[(x, 30) for x in (10, 11, 12, 13)], facing="up")
fk.edge_warps(m, wid="to_fold", cells=[(38, 27), (39, 27)], to_map="rimeway_fold",
              to=[(6, 1), (7, 1)], facing="down", requires_flag="flag:rime_gate_open",
              blocked_ref="npc.rime_gate_wrongside")
owed.append("npc.rime_gate_wrongside")

# ---- THE RIME GATE, this side (the same pair as the Fold's) -------------------------
m["objects"] += [
    {"id": "rime_gate_barred", "sprite": "rimeway_rime_gate_barred", "at": {"tx": 37, "ty": 25},
     "w": 4, "h": 3, "overhang": 2, "solid": False, "hidden_when_flag": "flag:rime_gate_open"},
    {"id": "rime_gate_open", "sprite": "rimeway_rime_gate_open", "at": {"tx": 37, "ty": 25},
     "w": 4, "h": 3, "overhang": 2, "solid": False, "requires_flag": "flag:rime_gate_open"},
]
# THE BAR: the yard before the gate (its whole walkable width) lifts it
for x in (38, 39):
    m["triggers"].append({"id": f"rime_gate_lift_{x}", "kind": "cutscene",
                          "at": {"tx": x, "ty": 24}, "activation": "step_on",
                          "ref": "script.rime_gate_lift", "sets_flags": ["flag:rime_gate_open"],
                          "hidden_when_flag": "flag:rime_gate_open"})
owed.append("script.rime_gate_lift")
m["npcs"].append({"id": "rime_acolyte", "at": {"tx": 36, "ty": 22}, "facing": "right",
                  "sprite": "hollowing_acolyte", "movement": "static",
                  "dialogue_ref": "script.rime_acolyte"})
owed.append("script.rime_acolyte")

# ---- the rime-lamps (the marsh end — dead until the gate opens) ---------------------
LAMPS = [(10, 13), (14, 7), (22, 7), (30, 4 + 2), (36, 10), (33, 19), (37, 22 + 1)]
for n, (x, y) in enumerate(LAMPS):
    for state, flag in (("dead", "hidden_when_flag"), ("lit", "requires_flag")):
        m["objects"].append({"id": f"rime_lamp_{n}_{state}", "sprite": f"rimeway_rime_lamp_{state}",
                             "at": {"tx": x, "ty": y - 1}, "w": 1, "h": 2, "overhang": 1,
                             "walk_under": True, flag: "flag:rime_gate_open"})

# ---- trainer / caches / signs / the drained fen's props ------------------------------
owed += pt.trainer_beat(m, tid="rimeway_fogwalker", at=(24, 6), facing="left",
                        sight=6, sprite="pass_walker")
owed += pt.cache(m, cid="rimeway_oil", at=(38, 7))
owed += pt.cache(m, cid="rimeway_fen", at=(3, 17))
owed += pt.sign(m, deco, W, sid="rimeway_marsh_end", at=(3, 13))
m["objects"] += [
    {"id": "notice", "sprite": "coldfog_hollowing_notice", "at": {"tx": 35, "ty": 24}, "w": 1, "h": 2,
     "overhang": 1},
    {"id": "null_rack", "sprite": "coldfog_null_rack", "at": {"tx": 28, "ty": 18}, "w": 4, "h": 2,
     "overhang": 1},
    {"id": "fen_lantern_a", "sprite": "saltreach_reed_lantern_dark", "at": {"tx": 15, "ty": 16},
     "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "fen_lantern_b", "sprite": "saltreach_reed_lantern_dark", "at": {"tx": 10, "ty": 22},
     "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "dead_tree", "sprite": "hushfrost_dead_tree", "at": {"tx": 21, "ty": 11 + 1}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "ridge_pine", "sprite": "hushfrost_snow_pine", "at": {"tx": 5, "ty": 2}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "ridge_outcrop", "sprite": "hushfrost_rock_outcrop_b", "at": {"tx": 36, "ty": 2}, "w": 2, "h": 2},
    {"id": "ridge_drift", "sprite": "hushfrost_snowdrift", "at": {"tx": 16, "ty": 6}, "w": 3, "h": 2},
]
m["triggers"].append({"id": "notice_read", "kind": "dialogue", "at": {"tx": 35, "ty": 25},
                      "activation": "interact", "ref": "sign.rimeway_hollowing_notice"})
owed.append("sign.rimeway_hollowing_notice")

# ---- encounters (46-48; night/day pairs) --------------------------------------------
# FC3 (2026-10-14, third review): FINAL forms only. The old tables rolled base forms
# 10-40 levels past their kindling (Crystarn at 41, Mothdim at 62); every line is now
# its kindled form, the Rimeway keeping its frost/stone (and, below, its moth) voice.
NIGHT = [
    {"kin_id": 135, "weight": 23, "min_level": 46, "max_level": 47},  # Liminalux (was Wispwane)
    {"kin_id": 138, "weight": 20, "min_level": 46, "max_level": 48},  # Voidmantle (was Nullmoth)
    {"kin_id": 140, "weight": 14, "min_level": 46, "max_level": 48},  # Wisprestored (was WispwaneNull)
    {"kin_id": 180, "weight": 12, "min_level": 46, "max_level": 47},  # Lullwing (was Mothdim)
    {"kin_id": 85, "weight": 10, "min_level": 46, "max_level": 47},  # Stillwarden (was Crystarn)
    {"kin_id": 142, "weight": 12, "min_level": 47, "max_level": 48},  # Embergone (was Cindersob)
    {"kin_id": 79, "weight": 7, "min_level": 47, "max_level": 48},  # Glacitern
]
DAY = [
    {"kin_id": 135, "weight": 18, "min_level": 56, "max_level": 62},  # Liminalux
    {"kin_id": 138, "weight": 16, "min_level": 57, "max_level": 63},  # Voidmantle
    {"kin_id": 140, "weight": 14, "min_level": 57, "max_level": 63},  # Wisprestored
    {"kin_id": 180, "weight": 12, "min_level": 56, "max_level": 62},  # Lullwing
    {"kin_id": 85, "weight": 12, "min_level": 57, "max_level": 63},  # Stillwarden
    {"kin_id": 142, "weight": 14, "min_level": 57, "max_level": 64},  # Embergone
    {"kin_id": 79, "weight": 10, "min_level": 58, "max_level": 64},  # Glacitern
]
band = mk.make_grid(W, H)
patch = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        (band if (i % W) in (7, 8) else patch)[i] = 1
zones = pt.zones_from_grid(patch, W, H, terrain="tall_grass", rate=0.11, table=NIGHT,
                           id_prefix="rime")
zones += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.06, table=NIGHT,
                            id_prefix="crossing")
m["encounters"] = fk.night_day(zones, DAY)

# ---- ground -------------------------------------------------------------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
base = []
for i in range(W * H):
    pool = bl if (i % W, i // W) in FEN else sn
    base.append(rng.choice(pool) if rng.random() < 0.5 else pool[0])
avoid = fk.busy_cells(m) | set(pin)
avoid |= {(x, y) for y in range(H) for x in range(W)
          if rows[y][x] != "." or deco[y * W + x] or murk[y * W + x]}
avoid |= {(38, 24), (39, 24), (38, 23), (39, 23)}
avoid |= {(x, y) for x in range(16, 20) for y in range(0, 3)}   # the Fields road (N3)
litter = [gid("g_pebble"), gid("g_tuft")]
for y in range(H):
    for x in range(W):
        if (x, y) in avoid:
            continue
        r = rng.random()
        if r < 0.05:
            deco[y * W + x] = gid("boulder")
        elif r < 0.22:
            deco[y * W + x] = rng.choice(litter)

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_trail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": g["road"]},
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": blighttuft},
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_murk", "role": "terrain", "terrain": "murk",
     "set": "vesper_overworld_set", "depth": 0, "data": murk},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": g["cliff"]},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": above},
]

if __name__ == "__main__":
    import sys
    if "--show" in sys.argv:
        print("\n".join(f"{y:3d} {r}" for y, r in enumerate(rows)))
    ok = mk.finalize(m, scale=3, pin_base=pin)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
