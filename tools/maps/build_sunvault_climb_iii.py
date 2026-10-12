#!/usr/bin/env python3
"""
Sunvault Climb III — the Gilt Face (09-the-wild-ways §2 S; kind route, region
west, band 48-49). The sheer middle of the Sunvault: the garden-roads give out
and the old sun-keepers' way goes straight UP the gilt sandstone on ladder
pitches, shelf to shelf, zig-zagging across the face.

Lore (story-bible §11-§12): before the Long Dusk the sun-keepers climbed this
face every dawn to wipe the frost off Nightreach's mirrors; their ladders are
still pegged into the stone, their trestle still spans the gully. Eleven
winters of dark and nobody has kept the pegs — but the brass holds.

Signature touches (§8):
  1. THE TRESTLE OVER THE GULLY — the road crosses the slot-gully on a timber
     trestle (row 23, `spans` bridge with `under:true`). Going home you come
     back down THE GULLY ITSELF (a one-way ledge drops you in at its head) and
     walk out UNDER the trestle you crossed — and from below, it's a dead end
     with a find at the top of the slot (§3a r3: seen early, paid later).
  2. THE PITCHES — four ladders, E/W/E/W, up four tiers; each tier is a
     shelf with a lit lip over a tall gilt face. One mid-face ledge (band A,
     east) holds a cache only a fifth ladder reaches.
  3. THE KEEPERS' SHELTER on the top shelf — a rest point (the leg from the
     Solarium is three maps long; level-design §2b heal spacing).

HANDSHAKES:
  SOUTH (22,43)/(23,43) `to_climb_ii`/`_e` -> sunvault_climb_ii (22,1)/(23,1);
        climb_ii's `to_climb_iii` lands at our (22,42)/(23,42).
  NORTH (6,0)/(7,0) `to_climb_iv`/`_e` -> sunvault_climb_iv (6,34)/(7,34);
        climb_iv's return pair lands at our (6,1)/(7,1).

Trainers (route class, 16 x ace): sunvault_suncaller (S1, ace 49) and
sunvault_stargazer (S3, ace 49) — each posted over a column the road crosses.

Run:  python3 tools/maps/build_sunvault_climb_iii.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 44
rng = random.Random(75)
owed: list[str] = []

c = fk.Canvas(W, H, ".")
c.rect(0, 0, W - 1, 1, "#").rect(0, 0, 1, H - 1, "#").rect(28, 0, 29, H - 1, "#")
c.rect(0, 43, W - 1, 43, "#")
c.rect(6, 0, 7, 1, "=")                       # north: the Sun Ledges
c.rect(22, 43, 23, 43, "=")                   # south: Climb II
c.put([(2, 2), (27, 2), (27, 3), (2, 42), (27, 42), (26, 42), (27, 13), (2, 31)], "#")

# band A (rows 7-12): sheer — lip 2, face 4; the pitch up to the top shelf (x12)
c.band(2, 27, 7, lip=2, face=4)
c.ladder(12, 7, 12)
# the mid-face ledge (east): an open row on the face, its own lip below, one
# short ladder up from S3 — a find only a climber sees
c.rect(20, 9, 25, 9, ".").rect(20, 10, 25, 11, "#")
c.ladder(23, 10, 12)
# band B (rows 17-21): the pitch up to S3 (west, x4) + the GULLY head
c.band(2, 27, 17, lip=2, face=3)
c.ladder(4, 17, 21)
# band C (rows 26-30): the pitch up to S2 (east, x19)
c.band(2, 27, 26, lip=2, face=3)
c.ladder(19, 26, 30)
# band D (rows 35-38): the pitch up from the bottom shelf (east, x26) + the
# west notch home (one-way)
c.band(2, 27, 35, lip=2, face=2)
c.ladder(26, 35, 38)
c.rect(3, 35, 4, 37, ".").rect(3, 38, 4, 38, "v")
# THE GULLY: a slot from S3's floor down to S1, x15-16; its walls through S2
c.rect(15, 17, 16, 30, "=")
c.rect(15, 17, 16, 17, "v")                   # the drop in at its head (one-way)
c.rect(14, 22, 14, 25, "F").rect(17, 22, 17, 25, "F")
c.rect(14, 23, 17, 23, "D")                   # THE TRESTLE (an underpass)

# ---- roads (ruinfloor) ------------------------------------------------------------
c.rect(22, 39, 23, 42, "=").rect(22, 39, 26, 40, "=")                  # S0
c.rect(19, 31, 26, 32, "=").rect(26, 31, 26, 34, "=")                  # S1
c.rect(18, 23, 19, 25, "=").rect(5, 23, 13, 24, "=").rect(4, 22, 4, 24, "=")   # S2
c.rect(4, 13, 4, 16, "=").rect(4, 14, 12, 15, "=").rect(12, 13, 12, 14, "=")   # S3
c.rect(12, 5, 12, 6, "=").rect(6, 4, 12, 5, "=").rect(6, 2, 7, 4, "=")       # top
# ---- encounter tuft -----------------------------------------------------------------
c.rect(9, 22, 10, 25, '"')                    # MANDATORY: S2 west, full shelf height
c.rect(2, 39, 8, 42, '"')                     # S0 west bed
c.rect(3, 31, 10, 34, '"')                    # S1 west (the notch's apron)
c.rect(20, 13, 26, 16, '"')                   # S3 east, under the mid-face ledge
c.rect(18, 2, 23, 5, '"')                     # the top shelf's high garden
c.rect(3, 2, 5, 3, '"')                       # ...and its west corner
c.rect(23, 22, 26, 23, '"')                   # S2 east, past the pitch
rows = c.rows()

m: dict = {
    "id": "sunvault_climb_iii", "display_name": "The Gilt Face",
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

fk.edge_warps(m, wid="to_climb_ii", cells=[(22, 43), (23, 43)], to_map="sunvault_climb_ii",
              to=[(22, 1), (23, 1)], facing="down")
fk.edge_warps(m, wid="to_climb_iv", cells=[(6, 0), (7, 0)], to_map="sunvault_climb_iv",
              to=[(6, 34), (7, 34)], facing="up")

# ---- the keepers' shelter (rest point) ----------------------------------------------
m["objects"].append({"id": "keepers_shelter", "sprite": "sunvault_rest_alcove",
                     "at": {"tx": 13, "ty": 2}, "w": 4, "h": 3, "overhang": 1})
for x in (13, 14, 15, 16):
    m["triggers"].append({"id": f"keepers_shelter_rest_{x}", "kind": "script",
                          "at": {"tx": x, "ty": 4}, "activation": "interact",
                          "ref": "script.sunvault_keepers_shelter"})
owed.append("script.sunvault_keepers_shelter")

# ---- trainers / signs / caches ------------------------------------------------------
owed += pt.trainer_beat(m, tid="sunvault_suncaller", at=(21, 34), facing="up",
                        sight=3, sprite="sun_keeper")
owed += pt.trainer_beat(m, tid="sunvault_stargazer", at=(8, 13), facing="down",
                        sight=3, sprite="star_watcher")
owed += pt.sign(m, deco, W, sid="sunvault_gilt_face", at=(24, 41))
owed += pt.sign(m, deco, W, sid="sunvault_gully", at=(13, 16))
owed += pt.cache(m, cid="sunvault_gully", at=(16, 19))      # top of the slot (from below)
owed += pt.cache(m, cid="sunvault_pitch", at=(21, 9))       # the mid-face ledge

# ---- encounters (48-49; night/day pairs) --------------------------------------------
NIGHT = [
    {"kin_id": 115, "weight": 20, "min_level": 48, "max_level": 49},  # Solvyne
    {"kin_id": 118, "weight": 18, "min_level": 48, "max_level": 49},  # Helicore
    {"kin_id": 122, "weight": 14, "min_level": 48, "max_level": 49},  # Solray
    {"kin_id": 126, "weight": 12, "min_level": 48, "max_level": 49},  # Lunveil
    {"kin_id": 117, "weight": 10, "min_level": 48, "max_level": 49},  # Helibud
    {"kin_id": 120, "weight": 8, "min_level": 48, "max_level": 49},  # Dawnfawn
    {"kin_id": 104, "weight": 6, "min_level": 48, "max_level": 49},  # Goldmane
    {"kin_id": 116, "weight": 5, "min_level": 48, "max_level": 49},  # Auravane
    {"kin_id": 121, "weight": 4, "min_level": 49, "max_level": 49},  # Sunstag
    {"kin_id": 127, "weight": 3, "min_level": 49, "max_level": 49},  # Lunvane
    {"kin_id": 123, "weight": 3, "min_level": 49, "max_level": 49},  # Solreach
]
DAY = [
    {"kin_id": 115, "weight": 16, "min_level": 57, "max_level": 63},  # Solvyne
    {"kin_id": 118, "weight": 16, "min_level": 57, "max_level": 63},  # Helicore
    {"kin_id": 122, "weight": 14, "min_level": 57, "max_level": 64},  # Solray
    {"kin_id": 126, "weight": 12, "min_level": 58, "max_level": 64},  # Lunveil
    {"kin_id": 117, "weight": 10, "min_level": 57, "max_level": 63},  # Helibud
    {"kin_id": 120, "weight": 8, "min_level": 57, "max_level": 63},  # Dawnfawn
    {"kin_id": 104, "weight": 8, "min_level": 58, "max_level": 64},  # Goldmane
    {"kin_id": 116, "weight": 6, "min_level": 58, "max_level": 64},  # Auravane
    {"kin_id": 121, "weight": 6, "min_level": 59, "max_level": 65},  # Sunstag
    {"kin_id": 127, "weight": 5, "min_level": 60, "max_level": 65},  # Lunvane
    {"kin_id": 123, "weight": 5, "min_level": 60, "max_level": 65},  # Solreach
]
band = mk.make_grid(W, H)
patch = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        (band if (i % W) in (9, 10) and 22 <= (i // W) <= 25 else patch)[i] = 1
zones = pt.zones_from_grid(patch, W, H, terrain="tall_grass", rate=0.11, table=NIGHT,
                           id_prefix="face")
zones += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.06, table=NIGHT,
                            id_prefix="crossing")
m["encounters"] = fk.night_day(zones, DAY)

# ---- dressing -----------------------------------------------------------------------
m["objects"] += [
    {"id": "lamp_foot", "sprite": "sunvault_sun_lamp", "at": {"tx": 24, "ty": 37},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_s1", "sprite": "sunvault_sun_lamp", "at": {"tx": 24, "ty": 31},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_trestle", "sprite": "sunvault_sun_lamp", "at": {"tx": 13, "ty": 20},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_s3", "sprite": "sunvault_sun_lamp", "at": {"tx": 5, "ty": 11},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_top", "sprite": "sunvault_sun_lamp", "at": {"tx": 11, "ty": 4},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "column_s2", "sprite": "solarium_column", "at": {"tx": 24, "ty": 22},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "masonry_s1", "sprite": "sunvault_masonry", "at": {"tx": 12, "ty": 32}, "w": 2, "h": 2},
    {"id": "masonry_s0", "sprite": "sunvault_masonry", "at": {"tx": 14, "ty": 40}, "w": 2, "h": 2},
    {"id": "fallen_s3", "sprite": "solarium_column_fallen", "at": {"tx": 9, "ty": 16}, "w": 3, "h": 1},
    {"id": "fallen_s2", "sprite": "solarium_column_fallen", "at": {"tx": 22, "ty": 25}, "w": 3, "h": 1},
    {"id": "spyglass_top", "sprite": "sunvault_sun_spyglass", "at": {"tx": 24, "ty": 4}, "w": 2, "h": 2},
    {"id": "flags_top", "sprite": "sunvault_sun_pennants", "at": {"tx": 2, "ty": 4}, "w": 4, "h": 2,
     "overhang": 2, "walk_under": True, "solid": False},
]
m["triggers"].append({"id": "spyglass_look", "kind": "script", "at": {"tx": 24, "ty": 5},
                      "activation": "interact", "ref": "script.sunvault_spyglass"})
owed.append("script.sunvault_spyglass")
for n, (x, y) in enumerate([(21, 2), (9, 2), (26, 8), (3, 13), (25, 27)]):
    m["objects"].append({"id": f"starglint_{n}", "sprite": rng.choice(
        ["sunvault_sunmote_a", "sunvault_sunmote_b"]),
        "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})

gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
avoid = fk.busy_cells(m) | set(pin)
avoid |= {(x, y) for y in range(H) for x in range(W) if rows[y][x] != "." or deco[y * W + x]}
litter = [gid("g_tuft"), gid("g_pebble"), gid("g_daisy")]
blooms = [gid("flowerbed_a"), gid("flowerbed_b")]
for y in range(H):
    for x in range(W):
        if (x, y) in avoid:
            continue
        r = rng.random()
        if r < 0.05:
            deco[y * W + x] = rng.choice(blooms)
        elif r < 0.09:
            deco[y * W + x] = gid("boulder")
        elif r < 0.27:
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
