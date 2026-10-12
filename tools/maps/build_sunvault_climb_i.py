#!/usr/bin/env python3
"""
Sunvault Climb I — the foot of the face (walkthrough/04-west "Sunvault Climb";
09-the-wild-ways §2 S; kind route, region west, band 46-47). REBUILT 2026-10
as a terraced MOUNTAIN FACE: the old garden-roads climb the Sunvault's
sandstone in three tiers, each wall a lit cliff lip over a tall gilt face, and
the roads climb them on LADDERS (the traversal kit's `ladder` span — up/down
only, you face the rungs).

The climb is four maps now (I -> II -> III the Gilt Face -> IV the Sun Ledges
-> Nightreach); this is the foot, the brightest, most hopeful stretch.

Three signature touches (§8):
  1. THE DEAD SUN-VINES at the north gorge — the I->II boundary, Sunsketch's
     first REQUIRED crossing; withered until gleam:solar (the flag-pair swap).
  2. THE FIRST PITCH — the main road meets the face and goes UP a ladder
     (east); the way home is the WEST NOTCH, a cut in the face with a one-way
     ledge at its foot (out the long way, home the short way — §3a r1/r2).
  3. THE OLD GARDEN under the face (tier A) — two ladders down, a loop, the
     fall crater, the grind bed and the wax road leaving south for the
     Wick-Run crest.

HANDSHAKES (unchanged — the Wick-Run's geometry closes against this map):
  EAST (29,14)/(29,15) `to_solarium`/`_s` <-> sunken_solarium (1,28)/(1,29).
  SOUTH (14,25)/(15,25) `to_wickrun`/`_e` <-> wickrun_crest (14,0)/(15,0).
  NORTH (6,0)/(7,0) `to_climb_ii`/`_e` (Sunsketch both ways, blocked_ref
  sign.sunvault_vines) -> sunvault_climb_ii (6,38)/(7,38); its return pair at
  (6,39)/(7,39) lands at our (6,1)/(7,1).
Runner-placed content on this map (coordinates honoured): the peril thread's
quiet family + brazier (add_peril_thread.py: brazier (24,6) 2x3, family (26,8)).

Trainer: sunvault_terracer "Terrace-tender Bel" (route, ace 47) — posted on
the entry tier facing down her column; the entry road can't pass unseen.

Run:  python3 tools/maps/build_sunvault_climb_i.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 26
rng = random.Random(73)
owed: list[str] = []

# ---- the face (ASCII; facekit legend) -----------------------------------------------
c = fk.Canvas(W, H, ".")
# borders: two deep at the sides, the gorge rim north, one row of wall south
c.rect(0, 0, W - 1, 1, "#").rect(0, 0, 1, H - 1, "#").rect(28, 0, 29, H - 1, "#")
c.rect(0, 25, W - 1, 25, "#")
c.rect(6, 0, 7, 1, "=")                       # the gorge gap (the vine bridge)
c.rect(28, 14, 29, 15, "=")                   # the Solarium road in (east)
c.rect(14, 25, 15, 25, "=")                   # the wax road out (south)
# organic bumps on the rims
c.put([(2, 2), (2, 3), (27, 2), (26, 2), (27, 3), (2, 16), (27, 24), (2, 24), (3, 24)], "#")

# BAND 1 (tier C over tier B): lip rows 9-10, face rows 11-12
c.band(2, 27, 9, lip=2, face=2)
c.rect(14, 9, 17, 9, ".")                     # a ragged lip (a bite out of the rim)
c.ladder(21, 9, 12)                           # THE FIRST PITCH (the way up)
c.rect(10, 9, 11, 11, ".").rect(10, 12, 11, 12, "v")   # THE WEST NOTCH + its ledge
# BAND 2 (tier B over the old garden): lip rows 17-18, face rows 19-20
c.band(2, 27, 17, lip=2, face=2)
c.ladder(12, 17, 20)                          # down to the garden (west)
c.ladder(25, 17, 20)                          # ...and (east) — the garden is a loop

# roads (ruinfloor)
c.rect(6, 2, 7, 6, "=").rect(6, 6, 22, 7, "=").rect(21, 7, 21, 8, "=")   # tier C
c.rect(16, 13, 27, 13, "=").rect(16, 14, 29, 14, "=").rect(20, 13, 22, 15, "=").rect(28, 15, 29, 15, "=")
c.rect(12, 13, 16, 13, "=").rect(10, 13, 13, 14, "=")                  # tier B west
c.rect(12, 21, 25, 22, "=").rect(14, 22, 15, 25, "=")                  # the wax road
# encounter tuft
c.rect(12, 2, 13, 5, '"').rect(12, 8, 13, 8, '"')    # MANDATORY tier-C crossing...
c.rect(14, 2, 17, 4, '"')                             # ...+ the upper garden
c.rect(2, 13, 5, 14, '"')                             # tier B west bed
c.rect(17, 23, 22, 24, '"').rect(18, 22, 21, 22, '"')  # the old garden's grind bed
rows = c.rows()
# the mandatory band must swallow the road where it crosses (rows 6-7)
for y in (6, 7):
    rows[y] = rows[y][:12] + '""' + rows[y][14:]
# rows 6-7 + 8: tier C's full height at x12-13 is tuft (no walking round it)

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
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)
pin: dict = {}
g = fk.paint(m, rows, deco=deco, above=above, pin=pin, face="gold", ledge="sand", rng=rng)

# ---- warps (graph.ts edge ids verbatim) ---------------------------------------------
fk.edge_warps(m, wid="to_wickrun", cells=[(14, 25), (15, 25)], to_map="wickrun_crest",
              to=[(14, 0), (15, 0)], facing="down")
fk.edge_warps(m, wid="to_solarium", cells=[(29, 14), (29, 15)], to_map="sunken_solarium",
              to=[(1, 28), (1, 29)], facing="right", suffix="_s")
fk.edge_warps(m, wid="to_climb_ii", cells=[(6, 0), (7, 0)], to_map="sunvault_climb_ii",
              to=[(6, 38), (7, 38)], facing="up", requires_ability="sunsketch",
              blocked_ref="sign.sunvault_vines")

# ---- THE DEAD SUN-VINE BRIDGE at the gorge (the flag-pair swap) ---------------------
m["objects"] += [
    {"id": "gorge_vines_bloomed", "sprite": "sunvault_vine_gate_bloomed",
     "at": {"tx": 6, "ty": 0}, "w": 2, "h": 3, "solid": False,
     "requires_flag": "gleam:solar"},
    {"id": "gorge_vines_withered", "sprite": "sunvault_vine_gate_withered",
     "at": {"tx": 6, "ty": 0}, "w": 2, "h": 3, "solid": False,
     "hidden_when_flag": "gleam:solar"},
]

# ---- R10 RUIN: the garden of the sun, remembered -------------------------------------
m["objects"] += [
    {"id": "sundial", "sprite": "sunvault_sundial_fallen", "at": {"tx": 2, "ty": 4},
     "w": 3, "h": 2},
    {"id": "colonnade", "sprite": "sunvault_colonnade", "at": {"tx": 6, "ty": 14},
     "w": 3, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "masonry_mid", "sprite": "sunvault_masonry", "at": {"tx": 17, "ty": 15},
     "w": 2, "h": 2},
    {"id": "masonry_low", "sprite": "sunvault_masonry", "at": {"tx": 23, "ty": 23},
     "w": 2, "h": 2},
    # W-4: a scorch in the old garden — the fall nearest the Solarium
    {"id": "fall_crater", "sprite": "fallenstar_crater", "at": {"tx": 3, "ty": 21},
     "w": 6, "h": 4, "solid": False},
    {"id": "fall_cinder", "sprite": "fallenstar_cinder_star", "at": {"tx": 5, "ty": 22},
     "w": 2, "h": 2, "overhang": 1, "hidden_when_flag": "flag:dawn"},
    {"id": "fall_cinder_woken", "sprite": "vigil_star_shard", "at": {"tx": 5, "ty": 22},
     "w": 2, "h": 2, "overhang": 1, "requires_flag": "flag:dawn"},
]
m["triggers"] += [
    {"id": "sundial_read", "kind": "script", "at": {"tx": 3, "ty": 5},
     "activation": "interact", "ref": "script.sunvault_sundial"},
    {"id": "fall_cinder_read", "kind": "script", "at": {"tx": 5, "ty": 23},
     "activation": "interact", "ref": "script.fall_mark_sunvault"},
    {"id": "fall_cinder_read_b", "kind": "script", "at": {"tx": 6, "ty": 23},
     "activation": "interact", "ref": "script.fall_mark_sunvault"},
]

# ---- signs --------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="sunvault_welcome", at=(27, 16))
owed += pt.sign(m, deco, W, sid="sunvault_vines", at=(8, 3))
owed += pt.sign(m, deco, W, sid="sunvault_face", at=(22, 15))

# ---- trainer beat (the entry tier — she watches the road come in) -------------------
owed += pt.trainer_beat(m, tid="sunvault_terracer", at=(24, 13), facing="down",
                        sight=3, sprite="npc_woman")

# ---- a resting wayfarer at the top of the first pitch -------------------------------
m["npcs"].append({
    "id": "sunvault_wayfarer", "at": {"tx": 19, "ty": 8}, "facing": "down",
    "sprite": "npc_old_man", "movement": "static",
    "dialogue_ref": "npc.sunvault_wayfarer_face"})

# ---- caches -------------------------------------------------------------------------
owed += pt.cache(m, cid="sunvault_balm", at=(17, 2))     # consumable, the upper garden
owed += pt.cache(m, cid="sunvault_wicks", at=(26, 23))   # loose wicks, the old garden

# ---- encounters (band 46-47; night/day pairs) ---------------------------------------
NIGHT = [
    {"kin_id": 114, "weight": 28, "min_level": 46, "max_level": 47},  # Sunsprout
    {"kin_id": 117, "weight": 16, "min_level": 46, "max_level": 47},  # Helibud
    {"kin_id": 120, "weight": 14, "min_level": 46, "max_level": 47},  # Dawnfawn
    {"kin_id": 115, "weight": 14, "min_level": 46, "max_level": 48},  # Solvyne
    {"kin_id": 118, "weight": 12, "min_level": 46, "max_level": 48},  # Helicore
    {"kin_id": 103, "weight": 10, "min_level": 46, "max_level": 47},  # Gilpaw
    {"kin_id": 104, "weight": 7, "min_level": 47, "max_level": 48},   # Goldmane
    {"kin_id": 116, "weight": 5, "min_level": 47, "max_level": 48},   # Auravane
    {"kin_id": 121, "weight": 4, "min_level": 47, "max_level": 48},   # Sunstag
]
DAY = [
    {"kin_id": 114, "weight": 18, "min_level": 56, "max_level": 62},
    {"kin_id": 117, "weight": 16, "min_level": 56, "max_level": 62},
    {"kin_id": 120, "weight": 14, "min_level": 56, "max_level": 63},
    {"kin_id": 115, "weight": 14, "min_level": 56, "max_level": 63},
    {"kin_id": 118, "weight": 12, "min_level": 56, "max_level": 63},
    {"kin_id": 103, "weight": 10, "min_level": 56, "max_level": 62},
    {"kin_id": 104, "weight": 7, "min_level": 58, "max_level": 64},
    {"kin_id": 116, "weight": 5, "min_level": 58, "max_level": 64},
    {"kin_id": 121, "weight": 4, "min_level": 59, "max_level": 65},
]
band = mk.make_grid(W, H)
patch = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        (band if (i % W) in (12, 13) and (i // W) < 9 else patch)[i] = 1
zones = pt.zones_from_grid(patch, W, H, terrain="tall_grass", rate=0.11, table=NIGHT,
                           id_prefix="terrace")
zones += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.05, table=NIGHT,
                            id_prefix="crossing")
m["encounters"] = fk.night_day(zones, DAY)

# ---- dressing -----------------------------------------------------------------------
m["objects"] += [
    {"id": "column_a", "sprite": "solarium_column", "at": {"tx": 3, "ty": 14},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_b", "sprite": "solarium_column", "at": {"tx": 23, "ty": 3},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_fallen_a", "sprite": "solarium_column_fallen",
     "at": {"tx": 9, "ty": 23}, "w": 3, "h": 1},
    {"id": "column_fallen_b", "sprite": "solarium_column_fallen",
     "at": {"tx": 19, "ty": 3}, "w": 3, "h": 1},
    {"id": "lamp_entry", "sprite": "sunvault_sun_lamp",
     "at": {"tx": 26, "ty": 14}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_gorge", "sprite": "sunvault_sun_lamp",
     "at": {"tx": 4, "ty": 6}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_pitch", "sprite": "sunvault_sun_lamp",
     "at": {"tx": 22, "ty": 6}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_pocket", "sprite": "sunvault_sun_lamp",
     "at": {"tx": 16, "ty": 21}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- ground + scatter ---------------------------------------------------------------
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
avoid = fk.busy_cells(m) | set(pin)
avoid |= {(26, 6), (27, 6), (24, 6), (25, 6), (24, 7), (25, 7), (24, 8), (25, 8), (26, 8)}  # peril thread
avoid |= {(x, y) for y in range(H) for x in range(W)
          if rows[y][x] != "." or deco[y * W + x]}
litter = [gid("g_tuft"), gid("g_pebble"), gid("g_daisy")]
blooms = [gid("flowerbed_a"), gid("flowerbed_b")]
for y in range(H):
    for x in range(W):
        if (x, y) in avoid:
            continue
        r = rng.random()
        if r < 0.06:
            deco[y * W + x] = rng.choice(blooms)
        elif r < 0.08:
            deco[y * W + x] = gid("boulder")
        elif r < 0.26:
            deco[y * W + x] = rng.choice(litter)

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": g["road"]},
    {"name": "t_goldtuft", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": g["tuft"]},
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
