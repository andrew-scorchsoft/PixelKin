#!/usr/bin/env python3
"""
Sunvault Climb II — the sun-vine bridges (walkthrough/04-west "Sunvault Climb";
09-the-wild-ways §2 S; kind route, region west, band 47-48). REBUILT 2026-10
as the second stretch of the MOUNTAIN FACE: four tiers stacked up the gilt
sandstone, each wall crossed a different way —

  band 1 (rows 29-31): a LIVING SUN-VINE BRIDGE up the face (the Sunsketch
          AbilityGate over the cut; vine art swaps withered->bloomed on
          gleam:solar), the one-way NOTCH beside it for the trip home;
  band 2 (rows 20-23): a LADDER pitch (east) and the west notch-ledge;
  the CLEFT (tier C): a rope-PLANK over the chasm that splits the shelf;
  band 3 (rows 9-13): the long LADDER (west) to the top tier, and the east
          notch-ledge home.

Signature touches kept from the first build: THE LIVING BRIDGE; THE X3
VIEWPOINT (script.chart_sunvault, requires flag:q_west_chart, sets
flag:q_west_chart_1); THE HELIA MOUTH on the west wall (Sunsketch spur,
missable); THE VINE-SHADE REST ARBOR (encounter-free breath, no heal); the
NE striker pocket (script.pickup_striker -> flag:picked_striker, Nightreach
lamp 1's errand) — which also hosts the R3 vigil scar (add_hand_placed.py
VIGIL_SCARS: `to_vigil_sun` at (27,2), scar (27,1)).

HANDSHAKES:
  SOUTH (6,39)/(7,39) `to_climb_i`/`_e` (Sunsketch) -> sunvault_climb_i (6,1)/(7,1);
        climb_i's `to_climb_ii` lands at our (6,38)/(7,38).
  NORTH (22,0)/(23,0) `to_climb_iii`/`_e` -> sunvault_climb_iii (22,42)/(23,42);
        its return pair `to_climb_ii` at (22,43)/(23,43) lands at our (22,1)/(23,1).
  WEST  (0,7)/(0,8) `to_helia`/`_s` (Sunsketch) -> helia_vault (23,10)/(23,11).

Trainer: sunvault_skywatcher "Sky-watcher Tam" (route, ace 48), tier C east,
facing down his column — the road west to the plank crosses it.

Run:  python3 tools/maps/build_sunvault_climb_ii.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 40
rng = random.Random(74)
owed: list[str] = []

c = fk.Canvas(W, H, ".")
c.rect(0, 0, W - 1, 1, "#").rect(0, 0, 1, H - 1, "#").rect(28, 0, 29, H - 1, "#")
c.rect(0, 39, W - 1, 39, "#")
c.rect(22, 0, 23, 1, "=")                     # north: the Gilt Face
c.rect(6, 39, 7, 39, "=")                     # south: the vine gorge
c.rect(0, 7, 1, 8, "=")                       # west: the Helia mouth
c.put([(2, 2), (2, 3), (27, 6), (2, 38), (3, 38), (27, 38), (26, 38), (2, 14), (27, 24)], "#")

# ---- tier D (rows 2-8): the striker pocket (NE) + the amber shelf ------------------
c.rect(24, 2, 24, 5, "#").rect(24, 5, 27, 5, "#")
c.put([(24, 3)], ".")                          # the pocket's mouth
c.rect(19, 2, 21, 5, "#").put([(20, 3), (20, 4)], ".")   # the shelf (vine cut at (20,5))
# ---- band 3 (rows 9-13): the long ladder (west) + the east notch home -------------
c.band(2, 27, 9, lip=2, face=3)
c.ladder(4, 9, 13)
c.rect(25, 9, 26, 12, ".").rect(25, 13, 26, 13, "v")
# ---- tier C (rows 14-19) split by the cleft; the plank over it --------------------
c.rect(14, 14, 15, 19, "#")
c.plank([(14, 16), (15, 16)])
# ---- band 2 (rows 20-23): the ladder pitch (east) + the west notch ----------------
c.band(2, 27, 20, lip=2, face=2)
c.ladder(24, 20, 23)
c.rect(3, 20, 4, 22, ".").rect(3, 23, 4, 23, "v")
# ---- band 1 (rows 29-31): the living bridge cut (x10-11) + the notch (x16-17) ------
c.band(2, 27, 29, lip=2, face=1)
c.rect(16, 29, 17, 30, ".").rect(16, 31, 17, 31, "v")

# ---- roads ------------------------------------------------------------------------
c.rect(6, 32, 7, 38, "=").rect(6, 32, 11, 33, "=")                 # tier A
c.rect(10, 24, 11, 28, "=").rect(10, 24, 24, 25, "=")              # tier B
c.rect(24, 19, 24, 19, "=").rect(16, 17, 24, 18, "=").rect(16, 16, 16, 18, "=")  # tier C east
c.rect(4, 15, 13, 16, "=").rect(4, 14, 4, 15, "=")                 # tier C west
c.rect(4, 6, 23, 7, "=").rect(4, 8, 4, 8, "=").rect(22, 2, 23, 7, "=").rect(2, 7, 4, 8, "=")
# ---- encounter tuft ---------------------------------------------------------------
c.rect(11, 14, 12, 19, '"')                   # MANDATORY: tier C west, full height
c.rect(14, 34, 21, 37, '"')                   # the south garden (optional)
c.rect(2, 34, 4, 37, '"')                     # the SW entry garden
c.rect(19, 27, 23, 28, '"')                   # tier B's east bed
c.rect(3, 26, 7, 28, '"')                     # tier B's west bed (under the notch)
c.rect(2, 17, 3, 19, '"')                     # the west notch's lip-bed
c.rect(5, 3, 9, 4, '"')                       # the NW high garden
rows = c.rows()

m: dict = {
    "id": "sunvault_climb_ii", "display_name": "Sunvault Climb",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [
        # THE LIVING BRIDGE — Sunsketch opens the band cells under the vine art
        {"id": "bridge_1", "ability": "sunsketch",
         "rect": {"tx": 10, "ty": 29, "w": 2, "h": 3}, "effect": "make_passable"},
        # the amber shelf's night-flower cut (optional pocket)
        {"id": "amber_vines", "ability": "sunsketch",
         "rect": {"tx": 20, "ty": 5, "w": 1, "h": 1}, "effect": "make_passable"},
    ],
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

# ---- warps --------------------------------------------------------------------------
fk.edge_warps(m, wid="to_climb_i", cells=[(6, 39), (7, 39)], to_map="sunvault_climb_i",
              to=[(6, 1), (7, 1)], facing="down", requires_ability="sunsketch",
              blocked_ref="sign.sunvault_vines")
fk.edge_warps(m, wid="to_climb_iii", cells=[(22, 0), (23, 0)], to_map="sunvault_climb_iii",
              to=[(22, 42), (23, 42)], facing="up")
for n, y in enumerate((7, 8)):
    m["warps"].append({"id": "to_helia" + ("_s" if n else ""), "at": {"tx": 0, "ty": y},
                       "trigger": "step_on", "to_map": "helia_vault", "to": {"tx": 23, "ty": 10 + n},
                       "facing": "left", "requires_ability": "sunsketch",
                       "blocked_ref": "sign.sunvault_helia", "transition": "door"})

# ---- vine art (flag-pair swaps on gleam:solar) --------------------------------------
for oid, sprite, at, w, h in [("bridge_1", "sunvault_vine_gate", (10, 29), 2, 3),
                              ("amber_vine", "sunvault_vine_v", (20, 4), 1, 3)]:
    m["objects"] += [
        {"id": f"{oid}_bloomed", "sprite": f"{sprite}_bloomed", "at": {"tx": at[0], "ty": at[1]},
         "w": w, "h": h, "solid": False, "requires_flag": "gleam:solar"},
        {"id": f"{oid}_withered", "sprite": f"{sprite}_withered", "at": {"tx": at[0], "ty": at[1]},
         "w": w, "h": h, "solid": False, "hidden_when_flag": "gleam:solar"},
    ]

# ---- THE X3 VIEWPOINT (the top tier's lookout) --------------------------------------
m["triggers"].append({
    "id": "chart_sunvault", "kind": "script", "at": {"tx": 14, "ty": 3},
    "activation": "interact", "ref": "script.chart_sunvault", "once": True,
    "requires_flag": "flag:q_west_chart", "sets_flags": ["flag:q_west_chart_1"],
    "hidden_when_flag": "flag:q_west_chart_1"})
m["objects"].append({"id": "lookout_dial", "sprite": "sunvault_sundial_fallen",
                     "at": {"tx": 13, "ty": 2}, "w": 3, "h": 2, "solid": False})
for n, (x, y) in enumerate([(12, 3), (16, 2), (18, 4), (26, 7), (10, 2), (8, 6), (3, 4)]):
    m["objects"].append({"id": f"starglint_{n}", "sprite": rng.choice(
        ["windward_starglint_a", "windward_starglint_b"]),
        "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})

# ---- signs / NPCs / trainer / caches -------------------------------------------------
owed += pt.sign(m, deco, W, sid="sunvault_helia", at=(2, 6))
owed += pt.sign(m, deco, W, sid="sunvault_observatory", at=(25, 7))
owed += pt.sign(m, deco, W, sid="sunvault_cleft", at=(13, 17))
m["npcs"].append({"id": "vine_tender", "at": {"tx": 12, "ty": 33}, "facing": "left",
                  "sprite": "npc_old_woman", "movement": "static",
                  "dialogue_ref": "npc.sunvault_vine_tender"})
owed += pt.trainer_beat(m, tid="sunvault_skywatcher", at=(20, 14), facing="down",
                        sight=5, sprite="npc_man")
owed += pt.cache(m, cid="striker", at=(26, 3))
owed += pt.cache(m, cid="sunvault_amber", at=(20, 3))
owed += pt.cache(m, cid="sunvault_charge", at=(21, 36))

# ---- encounters (band 47-48; night/day pairs) ---------------------------------------
NIGHT = [
    {"kin_id": 115, "weight": 26, "min_level": 47, "max_level": 48},  # Solvyne
    {"kin_id": 118, "weight": 24, "min_level": 47, "max_level": 48},  # Helicore
    {"kin_id": 120, "weight": 12, "min_level": 47, "max_level": 48},  # Dawnfawn
    {"kin_id": 117, "weight": 10, "min_level": 47, "max_level": 48},  # Helibud
    {"kin_id": 104, "weight": 10, "min_level": 47, "max_level": 48},  # Goldmane
    {"kin_id": 126, "weight": 10, "min_level": 47, "max_level": 48},  # Lunveil
    {"kin_id": 116, "weight": 8, "min_level": 47, "max_level": 48},   # Auravane
    {"kin_id": 121, "weight": 6, "min_level": 47, "max_level": 48},   # Sunstag
    {"kin_id": 127, "weight": 4, "min_level": 48, "max_level": 48},   # Lunvane
]
DAY = [
    {"kin_id": 115, "weight": 18, "min_level": 57, "max_level": 63},
    {"kin_id": 118, "weight": 16, "min_level": 57, "max_level": 63},
    {"kin_id": 120, "weight": 12, "min_level": 57, "max_level": 64},
    {"kin_id": 117, "weight": 10, "min_level": 57, "max_level": 63},
    {"kin_id": 104, "weight": 10, "min_level": 58, "max_level": 64},
    {"kin_id": 126, "weight": 14, "min_level": 58, "max_level": 64},
    {"kin_id": 116, "weight": 8, "min_level": 58, "max_level": 64},
    {"kin_id": 121, "weight": 6, "min_level": 59, "max_level": 65},
    {"kin_id": 127, "weight": 6, "min_level": 60, "max_level": 65},
]
band = mk.make_grid(W, H)
patch = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        (band if (i % W) in (11, 12) and 14 <= (i // W) <= 19 else patch)[i] = 1
zones = pt.zones_from_grid(patch, W, H, terrain="tall_grass", rate=0.11, table=NIGHT,
                           id_prefix="terrace")
zones += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.05, table=NIGHT,
                            id_prefix="crossing")
m["encounters"] = fk.night_day(zones, DAY)

# ---- dressing -----------------------------------------------------------------------
m["objects"] += [
    {"id": "column_a", "sprite": "solarium_column", "at": {"tx": 13, "ty": 32},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_b", "sprite": "solarium_column", "at": {"tx": 26, "ty": 25},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_fallen_a", "sprite": "solarium_column_fallen",
     "at": {"tx": 5, "ty": 24}, "w": 3, "h": 1},
    {"id": "column_fallen_b", "sprite": "solarium_column_fallen",
     "at": {"tx": 23, "ty": 33}, "w": 3, "h": 1},
    {"id": "lamp_entry", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 8, "ty": 35}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_mid", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 25, "ty": 22}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_north", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 21, "ty": 6}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_ladder", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 5, "ty": 12}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # THE VINE-SHADE REST ARBOR (tier C west, the climb's halfway breath)
    {"id": "rest_arbor_col_w", "sprite": "solarium_column",
     "at": {"tx": 6, "ty": 16}, "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "rest_arbor_col_e", "sprite": "solarium_column",
     "at": {"tx": 9, "ty": 16}, "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "rest_arbor_vine", "sprite": "sunvault_vine_h_bloomed",
     "at": {"tx": 7, "ty": 16}, "w": 3, "h": 1, "solid": False},
    {"id": "rest_seat", "sprite": "solarium_column_fallen",
     "at": {"tx": 6, "ty": 19}, "w": 3, "h": 1},
    {"id": "masonry_c", "sprite": "sunvault_masonry", "at": {"tx": 26, "ty": 15},
     "w": 2, "h": 2},
]

gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
avoid = fk.busy_cells(m) | set(pin) | {(27, 1), (27, 2)}
avoid |= {(x, y) for y in range(H) for x in range(W) if rows[y][x] != "." or deco[y * W + x]}
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
