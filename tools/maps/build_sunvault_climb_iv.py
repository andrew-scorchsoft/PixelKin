#!/usr/bin/env python3
"""
Sunvault Climb IV — the Sun Ledges (09-the-wild-ways §2 S; kind route, region
west, band 48-49). The last, most exposed stretch: no shelves left, only the
LEDGES — two-tile paths pegged along the top of the gilt face, broken by
clefts the sun-keepers bridged with rope-PLANKS — zig-zagging up four ladder
pitches to the observatory hill, where Nightreach's dome sits against the
densest sky in Vesperholm.

  the foot shelf -> ladder (W) -> ledge A, plank E -> ladder (E) -> ledge B,
  plank W (the ledge-watcher stands over it) -> ladder (W) -> ledge C, plank
  E -> ladder -> THE HILL (spyglass, the watchers' prayer flags, the road
  north). Two notch-ledges (one-way) are the quick way home.

Lore: the watchers' brass pegs, the sun-keepers' planks — the two orders
shared this face when the mirrors and the lamps were still one job (story-
bible §11 cinder law: "a light kept is a light shared").

HANDSHAKES:
  SOUTH (6,35)/(7,35) `to_climb_iii`/`_e` -> sunvault_climb_iii (6,1)/(7,1);
        climb_iii's `to_climb_iv` lands at our (6,34)/(7,34).
  NORTH (22,0)/(23,0) `to_observatory`/`_e` -> nightreach_observatory (15,28)/(16,28);
        Nightreach's `to_sunvault`/`_e` at (15,29)/(16,29) land at our (22,1)/(23,1).
        UNGATED both ways — the MAIN-PATH rim approach (spine §0 rule 2).

Trainer: sunvault_ledgewatcher (route, ace 49) on ledge B over its plank.

Run:  python3 tools/maps/build_sunvault_climb_iv.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 36
rng = random.Random(76)
owed: list[str] = []

c = fk.Canvas(W, H, ".")
c.rect(0, 0, W - 1, 1, "#").rect(0, 0, 1, H - 1, "#").rect(28, 0, 29, H - 1, "#")
c.rect(0, 35, W - 1, 35, "#")
c.rect(22, 0, 23, 1, "=")                     # north: Nightreach
c.rect(6, 35, 7, 35, "=")                     # south: the Gilt Face
c.put([(2, 2), (27, 2), (26, 2), (27, 3), (27, 34), (2, 34)], "#")

# four bands, three ledges (rows: hill 2-7 | band4 8-11 | C 12-13 | band3 14-17
#                                  | B 18-19 | band2 20-23 | A 24-25 | band1 26-29 | foot 30-34)
for y0 in (8, 14, 20, 26):
    c.band(2, 27, y0, lip=2, face=2)
# the ledges' clefts: the face runs on down through the ledge, a plank across
c.rect(13, 24, 15, 25, "F").plank([(13, 25), (14, 25), (15, 25)])     # ledge A
c.rect(16, 18, 18, 19, "F").plank([(16, 19), (17, 19), (18, 19)])     # ledge B
c.rect(10, 12, 12, 13, "F").plank([(10, 13), (11, 13), (12, 13)])     # ledge C
# the ledges narrow at their ends (lip bites) — exposed, not shelves
c.rect(2, 24, 2, 24, "#").rect(27, 18, 27, 18, "#").rect(2, 12, 3, 12, "#")
# the pitches, alternating ends
c.ladder(4, 26, 29)                           # foot -> A (west)
c.ladder(25, 20, 23)                          # A -> B (east)
c.ladder(5, 14, 17)                           # B -> C (west)
c.ladder(20, 8, 11)                           # C -> hill
# the quick way home: notches through bands 3 and 1 (one-way, east)
c.rect(24, 14, 25, 16, ".").rect(24, 17, 25, 17, "v")
c.rect(22, 26, 23, 28, ".").rect(22, 29, 23, 29, "v")

# ---- roads ----------------------------------------------------------------------
c.rect(6, 30, 7, 34, "=").rect(4, 30, 7, 31, "=")                     # foot
c.rect(20, 2, 21, 7, "=").rect(20, 2, 23, 3, "=")                     # the hill road
# ---- encounter tuft ----------------------------------------------------------------
c.rect(9, 30, 18, 33, '"')                    # the foot's bed
c.rect(7, 24, 8, 25, '"')                     # MANDATORY: ledge A, full width of the path
c.rect(21, 18, 22, 19, '"')                   # MANDATORY: ledge B
c.rect(15, 12, 16, 13, '"')                   # MANDATORY: ledge C
c.rect(3, 3, 9, 6, '"')                       # the hill's west meadow
rows = c.rows()

m: dict = {
    "id": "sunvault_climb_iv", "display_name": "The Sun Ledges",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/sunvault-climb-b.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/sunvault-climb-a.webp",
        "assets/backgrounds/battle/sunvault-climb-b.webp",
    ],
}
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)
pin: dict = {}
g = fk.paint(m, rows, deco=deco, above=above, pin=pin, face="gold", ledge="sand", rng=rng)

fk.edge_warps(m, wid="to_climb_iii", cells=[(6, 35), (7, 35)], to_map="sunvault_climb_iii",
              to=[(6, 1), (7, 1)], facing="down")
fk.edge_warps(m, wid="to_observatory", cells=[(22, 0), (23, 0)],
              to_map="nightreach_observatory", to=[(15, 28), (16, 28)], facing="up")

# ---- the hill: the watchers' lookout ------------------------------------------------
m["objects"] += [
    {"id": "hill_spyglass", "sprite": "windward_spyglass", "at": {"tx": 13, "ty": 3}, "w": 2, "h": 2},
    {"id": "hill_flags", "sprite": "windward_prayer_flags", "at": {"tx": 16, "ty": 2}, "w": 4, "h": 2,
     "overhang": 2, "walk_under": True, "solid": False},
    {"id": "hill_banner_w", "sprite": "nightreach_star_banner", "at": {"tx": 19, "ty": 5}, "w": 1, "h": 2,
     "solid": False},
    {"id": "hill_banner_e", "sprite": "nightreach_star_banner", "at": {"tx": 24, "ty": 5}, "w": 1, "h": 2,
     "solid": False},
    {"id": "hill_camp", "sprite": "pale_vault_camp_lit", "at": {"tx": 24, "ty": 3}, "w": 3, "h": 2},
]
m["triggers"].append({"id": "hill_spyglass_look", "kind": "script", "at": {"tx": 13, "ty": 4},
                      "activation": "interact", "ref": "script.sunvault_hill_spyglass"})
owed.append("script.sunvault_hill_spyglass")
m["npcs"].append({"id": "hill_watcher", "at": {"tx": 25, "ty": 6}, "facing": "left",
                  "sprite": "npc_old_woman", "movement": "static",
                  "dialogue_ref": "npc.sunvault_hill_watcher"})
owed.append("npc.sunvault_hill_watcher")
owed += pt.sign(m, deco, W, sid="sunvault_observatory_hill", at=(21, 8 - 1))
owed += pt.sign(m, deco, W, sid="sunvault_sun_ledges", at=(5, 32))

# ---- trainer / caches ---------------------------------------------------------------
owed += pt.trainer_beat(m, tid="sunvault_ledgewatcher", at=(20, 19), facing="left",
                        sight=5, sprite="star_watcher")
owed += pt.cache(m, cid="sunvault_ledge_tin", at=(26, 12))   # ledge C's far end
owed += pt.cache(m, cid="sunvault_brass", at=(3, 18))       # ledge B's west end

# ---- encounters (48-49; night/day pairs) --------------------------------------------
NIGHT = [
    {"kin_id": 126, "weight": 18, "min_level": 48, "max_level": 49},  # Lunveil
    {"kin_id": 122, "weight": 16, "min_level": 48, "max_level": 49},  # Solray
    {"kin_id": 118, "weight": 14, "min_level": 48, "max_level": 49},  # Helicore
    {"kin_id": 124, "weight": 12, "min_level": 48, "max_level": 49},  # Petalune
    {"kin_id": 106, "weight": 10, "min_level": 48, "max_level": 49},  # Drowshorn
    {"kin_id": 127, "weight": 10, "min_level": 48, "max_level": 49},  # Lunvane
    {"kin_id": 104, "weight": 8, "min_level": 48, "max_level": 49},   # Goldmane
    {"kin_id": 123, "weight": 6, "min_level": 49, "max_level": 49},   # Solreach
    {"kin_id": 125, "weight": 4, "min_level": 49, "max_level": 49},   # Crystalune
]
DAY = [
    {"kin_id": 126, "weight": 14, "min_level": 58, "max_level": 64},
    {"kin_id": 122, "weight": 16, "min_level": 57, "max_level": 64},
    {"kin_id": 118, "weight": 14, "min_level": 57, "max_level": 63},
    {"kin_id": 124, "weight": 12, "min_level": 58, "max_level": 64},
    {"kin_id": 106, "weight": 8, "min_level": 58, "max_level": 64},
    {"kin_id": 127, "weight": 10, "min_level": 60, "max_level": 65},
    {"kin_id": 104, "weight": 10, "min_level": 58, "max_level": 64},
    {"kin_id": 123, "weight": 10, "min_level": 60, "max_level": 65},
    {"kin_id": 125, "weight": 6, "min_level": 60, "max_level": 65},
]
band = mk.make_grid(W, H)
patch = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        y = i // W
        (band if 12 <= y <= 25 else patch)[i] = 1
zones = pt.zones_from_grid(patch, W, H, terrain="tall_grass", rate=0.11, table=NIGHT,
                           id_prefix="ledges")
zones += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.06, table=NIGHT,
                            id_prefix="crossing")
m["encounters"] = fk.night_day(zones, DAY)

# ---- dressing -----------------------------------------------------------------------
m["objects"] += [
    {"id": "lamp_foot", "sprite": "tinderwick_lamp_post", "at": {"tx": 8, "ty": 31},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 24, "ty": 23},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 6, "ty": 17},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 19, "ty": 11},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "masonry_foot", "sprite": "sunvault_masonry", "at": {"tx": 22, "ty": 32}, "w": 2, "h": 2},
    {"id": "pine_hill", "sprite": "windward_bent_pine", "at": {"tx": 9, "ty": 4}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
]
for n, (x, y) in enumerate([(11, 2), (5, 2), (17, 5), (26, 7), (9, 12), (14, 18), (2, 25),
                            (19, 24), (12, 31)]):
    m["objects"].append({"id": f"starglint_{n}", "sprite": rng.choice(
        ["windward_starglint_a", "windward_starglint_b"]),
        "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})

gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
avoid = fk.busy_cells(m) | set(pin)
avoid |= {(x, y) for y in range(H) for x in range(W) if rows[y][x] != "." or deco[y * W + x]}
# the ledges stay clear of boulders (a 2-wide path must never be blocked)
ledge_rows = {12, 13, 18, 19, 24, 25}
litter = [gid("g_tuft"), gid("g_pebble"), gid("g_daisy")]
blooms = [gid("flowerbed_a"), gid("flowerbed_b")]
for y in range(H):
    for x in range(W):
        if (x, y) in avoid:
            continue
        r = rng.random()
        if r < 0.05 and y not in ledge_rows:
            deco[y * W + x] = rng.choice(blooms)
        elif r < 0.08 and y not in ledge_rows:
            deco[y * W + x] = gid("boulder")
        elif r < 0.28:
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
