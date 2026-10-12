#!/usr/bin/env python3
"""
The Rimeway Ascent (09-the-wild-ways §2 C; kind route, region north, band
39-41). The old star-tenders' high road climbs out of Pale Vault Glacier's
north edge toward the Fold: ice bands with ladders pegged into them, and the
GLARE — wind-polished ice the tenders crossed by reading the stones.

Lore (story-bible §11-§12): the Rimeway joined the Pale Vault's lamp-line to
the Nightreach watchers; a tender walked it every night with oil for the
rime-lamps. Eleven winters ago the lamps went out one by one and nobody came
up with the oil. They still stand along the road — dead, waiting.

Three signature touches (§8):
  1. THE GLARE (shelf 1): a full-width sheet of glare ice (an `ice` flow —
     you slide until something stops you). The only way up the next band is
     a ladder at the sheet's far north-west corner; the stopper stones make
     the route. The strip at the sheet's foot is a reset lane (no trap).
  2. THE CACHE POOL (shelf 2): a small frozen pool with a cache on its far
     bank — a second, shorter slide puzzle, optional.
  3. THE BANDS: three glacier-wall bands (lit lip over a tall ice face), each
     climbed on a ladder; the top band's WEST NOTCH is the one-way way home.

HANDSHAKES:
  SOUTH (23,55)/(24,55) `to_pale_vault`/`_e` -> pale_vault_glacier (23,1)/(24,1);
        Pale Vault's `to_rimeway`/`_e` (23,0)/(24,0) land at our (23,54)/(24,54).
  NORTH (4,0)/(5,0) `to_fold`/`_e` -> rimeway_fold (28,42)/(29,42);
        the Fold's `to_ascent`/`_e` (28,43)/(29,43) land at our (4,1)/(5,1).
Geometry (world_geometry frame): x 118..148, y -357..-301.

Trainer: rimeway_walker_ivo (route, ace 41) on shelf 2.

Run:  python3 tools/maps/build_rimeway_ascent.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 56
rng = random.Random(9201)
owed: list[str] = []

c = fk.Canvas(W, H, ".")
c.rect(0, 0, W - 1, 1, "#").rect(0, 0, 1, H - 1, "#").rect(28, 0, 29, H - 1, "#")
c.rect(0, 55, W - 1, 55, "#")
c.rect(4, 0, 5, 1, "=")                       # north: the Fold
c.rect(23, 55, 24, 55, "=")                   # south: Pale Vault
c.put([(2, 2), (27, 2), (27, 3), (2, 54), (3, 54), (27, 54), (2, 46), (27, 47)], "#")

# band 1 (rows 42-45) + its ladder (x20)
c.band(2, 27, 42, lip=2, face=2)
c.ladder(20, 42, 45)
# THE GLARE (rows 31-40) over the reset strip (row 41); the pad + ladder NW
c.rect(2, 31, 27, 40, "i")
GLARE_STONES = [(2, 36), (4, 31), (5, 36), (6, 38), (7, 35), (7, 36), (7, 40), (8, 31),
                (12, 36), (15, 37), (17, 37), (23, 31), (23, 32), (24, 33), (24, 34),
                (26, 31), (26, 38)]   # searched: 5 slides minimum, no trap (facekit.ice_solve)
c.put(GLARE_STONES, "o")
c.band(2, 27, 26, lip=2, face=3)              # band 2: rows 26-30
c.rect(5, 30, 7, 30, ".")                     # the pad at the foot of the ladder
c.ladder(6, 26, 29)
# shelf 2 (rows 14-25): the cache pool (rows 17-21, x17-26)
c.rect(17, 17, 26, 21, "i")
c.put([(17, 17), (26, 21), (21, 19), (25, 17), (18, 21)], "o")
c.rect(23, 18, 23, 18, ".")                   # the islet the cache sits on
c.put([(24, 18), (23, 17), (23, 20)], "o")
# band 3 (rows 10-13) + ladder (x24) + the west notch home
c.band(2, 27, 10, lip=2, face=2)
c.ladder(15, 10, 13)
c.rect(10, 10, 11, 12, ".").rect(10, 13, 11, 13, "v")

# roads (snowtrail)
c.rect(23, 46, 24, 54, "=").rect(20, 46, 24, 47, "=")
c.rect(6, 22, 7, 25, "=").rect(6, 22, 15, 23, "=").rect(15, 14, 15, 23, "=")
c.rect(4, 2, 5, 6, "=").rect(4, 6, 15, 7, "=").rect(15, 7, 15, 9, "=")
# frosttuft
c.rect(3, 48, 12, 53, '"')                    # the foot's bed
c.rect(12, 22, 13, 25, '"').rect(12, 14, 13, 21, '"')   # MANDATORY: shelf 2, full height
c.rect(2, 14, 8, 18, '"')                     # shelf 2 west bed
c.rect(14, 2, 20, 5, '"')                     # shelf 3 bed
c.rect(25, 48, 26, 50, '"')                   # the foot's east nook
rows = c.rows()

m: dict = {
    "id": "rimeway_ascent", "display_name": "The Rimeway",
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

fk.edge_warps(m, wid="to_pale_vault", cells=[(23, 55), (24, 55)], to_map="pale_vault_glacier",
              to=[(23, 1), (24, 1)], facing="down")
fk.edge_warps(m, wid="to_fold", cells=[(4, 0), (5, 0)], to_map="rimeway_fold",
              to=[(28, 42), (29, 42)], facing="up")

# ---- the dead rime-lamps along the road (they wake when the Gate is open) ----------
LAMPS = [(25, 50), (19, 46), (21, 41), (8, 30), (25, 24), (9, 21), (22, 8), (6, 4)]
for n, (x, y) in enumerate(LAMPS):
    for state, flag in (("dead", "hidden_when_flag"), ("lit", "requires_flag")):
        m["objects"].append({"id": f"rime_lamp_{n}_{state}", "sprite": f"rimeway_rime_lamp_{state}",
                             "at": {"tx": x, "ty": y - 1}, "w": 1, "h": 2, "overhang": 1,
                             "walk_under": True, flag: "flag:rime_gate_open"})

# ---- trainer / signs / caches -------------------------------------------------------
owed += pt.trainer_beat(m, tid="rimeway_walker_ivo", at=(15, 21), facing="down",
                        sight=4, sprite="frost_herder")
owed += pt.sign(m, deco, W, sid="rimeway_foot", at=(25, 52))
owed += pt.sign(m, deco, W, sid="rimeway_glare", at=(18, 46))
owed += pt.cache(m, cid="rimeway_pool", at=(23, 18))
owed += pt.cache(m, cid="rimeway_tin", at=(27, 4))

# ---- encounters (39-41; night/day pairs) --------------------------------------------
NIGHT = [
    {"kin_id": 81, "weight": 22, "min_level": 39, "max_level": 41},   # Blizzrhare
    {"kin_id": 78, "weight": 18, "min_level": 39, "max_level": 41},   # Crystarn
    {"kin_id": 75, "weight": 16, "min_level": 39, "max_level": 41},   # Geodrake
    {"kin_id": 84, "weight": 14, "min_level": 39, "max_level": 41},   # Hushbore
    {"kin_id": 86, "weight": 12, "min_level": 39, "max_level": 40},   # Prismcub
    {"kin_id": 74, "weight": 10, "min_level": 39, "max_level": 40},   # Geolace
    {"kin_id": 79, "weight": 6, "min_level": 40, "max_level": 41},    # Glacitern
    {"kin_id": 76, "weight": 2, "min_level": 41, "max_level": 41},    # Vaultclaw (the Fold's own)
]
DAY = [
    {"kin_id": 81, "weight": 18, "min_level": 56, "max_level": 62},
    {"kin_id": 78, "weight": 18, "min_level": 56, "max_level": 63},
    {"kin_id": 75, "weight": 16, "min_level": 57, "max_level": 63},
    {"kin_id": 84, "weight": 14, "min_level": 56, "max_level": 62},
    {"kin_id": 86, "weight": 12, "min_level": 56, "max_level": 62},
    {"kin_id": 74, "weight": 10, "min_level": 56, "max_level": 62},
    {"kin_id": 79, "weight": 8, "min_level": 58, "max_level": 64},
    {"kin_id": 76, "weight": 4, "min_level": 60, "max_level": 65},
]
band = mk.make_grid(W, H)
patch = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        (band if (i % W) in (12, 13) and 14 <= (i // W) <= 25 else patch)[i] = 1
zones = pt.zones_from_grid(patch, W, H, terrain="tall_grass", rate=0.11, table=NIGHT,
                           id_prefix="rime")
zones += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.06, table=NIGHT,
                            id_prefix="crossing")
m["encounters"] = fk.night_day(zones, DAY)

# ---- dressing -----------------------------------------------------------------------
m["objects"] += [
    {"id": "pine_foot", "sprite": "hushfrost_snow_pine_big", "at": {"tx": 14, "ty": 49}, "w": 3, "h": 4,
     "overhang": 3, "walk_under": True},
    {"id": "pine_shelf2", "sprite": "hushfrost_snow_pine", "at": {"tx": 2, "ty": 21}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "spire_shelf2", "sprite": "pale_vault_ice_spire", "at": {"tx": 9, "ty": 15}, "w": 2, "h": 3},
    {"id": "drift_top", "sprite": "hushfrost_snowdrift", "at": {"tx": 8, "ty": 2}, "w": 3, "h": 2},
    {"id": "outcrop_foot", "sprite": "hushfrost_icicle_outcrop", "at": {"tx": 6, "ty": 46}, "w": 3, "h": 2},
    {"id": "sled_wreck", "sprite": "pale_vault_herder_sled", "at": {"tx": 26, "ty": 44 + 3}, "w": 2, "h": 2},
    {"id": "cairn_top", "sprite": "windward_cairn", "at": {"tx": 26, "ty": 7}, "w": 2, "h": 3, "overhang": 1},
    # the bands' icicles + the Glare's glints (non-solid: the stones alone stop you)
    {"id": "spire_top", "sprite": "pale_vault_ice_spire", "at": {"tx": 21, "ty": 2}, "w": 2, "h": 3},
    {"id": "boulders_top", "sprite": "hushfrost_snow_boulders", "at": {"tx": 9, "ty": 8}, "w": 2, "h": 2,
     "overhang": 1, "walk_under": True},
    {"id": "drift_shelf2", "sprite": "hushfrost_snowdrift", "at": {"tx": 18, "ty": 24}, "w": 3, "h": 2},
    {"id": "outcrop_shelf2", "sprite": "hushfrost_rock_outcrop_b", "at": {"tx": 26, "ty": 23}, "w": 2, "h": 2},
    {"id": "shrub_a", "sprite": "hushfrost_frozen_shrub", "at": {"tx": 3, "ty": 19}, "w": 1, "h": 1},
    {"id": "shrub_b", "sprite": "hushfrost_frozen_shrub", "at": {"tx": 20, "ty": 51}, "w": 1, "h": 1},
    {"id": "drift_foot", "sprite": "windward_snow_drift", "at": {"tx": 9, "ty": 47}, "w": 2, "h": 1, "solid": False},
]
for n, (x, y) in enumerate([(4, 44), (11, 45), (16, 44), (25, 45), (3, 29), (14, 28), (22, 29),
                            (8, 12), (19, 12), (26, 13)]):
    m["objects"].append({"id": f"icicles_{n}", "sprite": f"hushfrost_icicles_{'ab'[n % 2]}",
                         "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})
for n, (x, y) in enumerate([(9, 33), (19, 34), (5, 39), (13, 38), (25, 36), (20, 19), (24, 20),
                            (3, 32), (16, 32), (21, 33), (10, 35), (18, 36), (27, 34), (4, 37),
                            (23, 37), (11, 39), (15, 40), (26, 40), (8, 40), (20, 39)]):
    m["objects"].append({"id": f"glint_{n}", "sprite": f"hushfrost_aurora_glint_{'ab'[n % 2]}",
                         "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})

# the Glare's sheen: a scatter of glints over the sheet (non-solid — never a stopper)
taken = {(o["at"]["tx"], o["at"]["ty"]) for o in m["objects"]}
for (x, y) in sorted(g["ice"]):
    if (x, y) not in taken and (x * 7 + y * 13) % 5 == 0:
        m["objects"].append({"id": f"sheen_{x}_{y}", "sprite": f"hushfrost_aurora_glint_{'ab'[(x + y) % 2]}",
                             "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})

sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]
avoid = fk.busy_cells(m) | set(pin)
avoid |= {(x, y) for y in range(H) for x in range(W) if rows[y][x] != "." or deco[y * W + x]}
avoid |= {(x, 41) for x in range(W)} | {(x, 30) for x in range(W)}     # the strip + pad stay clear
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
        best, traps = fk.ice_solve(rows, [(x, 41) for x in range(2, 28)],
                                   [(5, 30), (6, 30), (7, 30)], box=(2, 30, 27, 41))
        print("GLARE: min slides", best, "traps", traps)
        best, traps = fk.ice_solve(rows, [(x, 22) for x in range(14, 28)] + [(16, y) for y in range(14, 22)],
                                   [(23, 18)], box=(14, 14, 27, 23))
        print("POOL: min slides", best, "traps", traps)
    ok = mk.finalize(m, scale=3, pin_base=pin)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
