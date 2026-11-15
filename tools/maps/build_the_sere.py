#!/usr/bin/env python3
"""
Build THE SERE — Galehigh's dry side: the rain-shadow desert east of the terraces,
the Rio Tower on the canyon rim, and the Thousandfold beyond (optional, mid-game).

Scene (level-design §2b): a SPUR off Galehigh's east gap (the drovers' track out of
the festival terrace), band 30-34 against Galehigh's 28-30 and the Ashfall's 30-33.
The terraces catch every cloud that comes up the Windward side; nothing is left to
rain on the Sere — so the storms here are DRY, all thunder and no rain, and in the
Long Dusk they have lost their road altogether.

Signature touches (§8):
  1. THE RIO TOWER — the old storm-watchers' tower on the rim, the Thunder Table
     restaurant at its top (rio_tower_1/2/top, build_rio_tower.py).
  2. THE THOUSANDFOLD — the canyon itself, the whole east side of the map: a drop
     in strata bands (sere_set `canyon`), running off the north and south edges.
  3. THE CALLING RODS — three storm-callers' copper masts whose lamps went out.
     Relight all three (flag:sere_rod_1..3 -> the DERIVED flag:sere_storm_called,
     FlagStore COUNT_AT_LEAST) and the storm has its road again: eat at the Thunder
     Table and the rolling thunder comes across the Sere.

Layout (W 44 x H 34):
  * west gap rows 16-17 <- Galehigh's `to_sere` (31,19)/(31,20)
  * the drovers' track east along rows 16-17, round the tower's foot onto its apron
  * NW: rod 1 behind the sage-scrub and the dune bank (hop down, walk round)
  * N : the drovers' camp — Hesk's tent, fire and wagon (a rest point)
  * S : the dry wash (hardpan), rod 2, watched by a storm-chaser
  * E : the rim lookout, rod 3, the spyglass and the canyon surveyor
  * a full-corridor scrub band at cols 16-17 (the road itself rolls, §11 r7)

Run:  python3 tools/maps/build_the_sere.py
"""
from __future__ import annotations

import math
import random

import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 44, 34
rng = random.Random(4417)

SERE_REF = mk.register_tileset(
    "sere_set", index=mk.REPO / "assets/tilesets/sere/sere_set.index.json")
S = "sere_set"

redrock = mk.make_grid(W, H)
canyon = mk.make_grid(W, H)
trail = mk.make_grid(W, H)
hardpan = mk.make_grid(W, H)
scrub = mk.make_grid(W, H)

# ---- the Thousandfold: the rim wanders, the drop runs off N and S ------------------
RIM = {}
for y in range(H):
    rx = 35 + round(1.4 * math.sin(y / 3.1) + 0.8 * math.sin(y / 1.7 + 1.0))
    if 6 <= y <= 18:          # the tower's shoulder: the rim stands right behind it
        rx = max(rx, 34)
    RIM[y] = rx
    for x in range(rx, W):
        canyon[y * W + x] = 1
# the side gorge that bites in below the lookout (the rim isn't a ruler)
mk.blob(canyon, W, H, 33.5, 25, 2.6, 2.2)
mk.blob(canyon, W, H, 31.5, 26.5, 1.6, 1.3)

# ---- the mesa walls (map border) + three free-standing mesas ----------------------
mk.rect(redrock, W, H, 0, 0, W - 1, 2)
mk.rect(redrock, W, H, 0, H - 3, W - 1, H - 1)
mk.rect(redrock, W, H, 0, 0, 1, H - 1)
mk.organic_border(redrock, W, H, depth=0,
                  bumps=[(5, 3, 1), (19, 3, 1), (29, 3, 1), (9, 30, 1), (24, 30, 2),
                         (2, 10, 1), (2, 27, 1)], rng=rng)
for y in (16, 17):            # the west gap from Galehigh
    for x in (0, 1, 2):
        redrock[y * W + x] = 0
mk.blob(redrock, W, H, 23, 7.5, 2.6, 1.4)        # the north mesa
mk.blob(redrock, W, H, 8.5, 22.5, 2.8, 1.5)      # the south-west mesa
mk.blob(redrock, W, H, 27, 29, 2.0, 1.0)         # a low butte by the south wall

# ---- the drovers' track ---------------------------------------------------------------
mk.rect(trail, W, H, 0, 16, 26, 17)              # in from the west gap
mk.rect(trail, W, H, 25, 18, 32, 19)             # round onto the tower's apron
mk.rect(trail, W, H, 31, 20, 32, 21)             # down to the rim lookout
mk.rect(trail, W, H, 12, 7, 13, 15)              # north to the drovers' camp
mk.rect(trail, W, H, 10, 7, 15, 8)               # the camp yard
mk.rect(trail, W, H, 20, 18, 21, 24)             # south into the dry wash

# ---- the dry wash (cracked hardpan) + small pans ----------------------------------------
mk.blob(hardpan, W, H, 21, 25.5, 6.5, 2.6)

# ---- sage-scrub (the encounter tile; hard-edged) ---------------------------------------
mk.blob(scrub, W, H, 6.5, 10, 3.2, 2.2)          # bed A: before rod 1
mk.blob(scrub, W, H, 26, 4.2, 4.0, 1.2)          # bed D: under the north wall
mk.blob(scrub, W, H, 13.5, 27.5, 3.0, 1.6)       # bed C: the wash's west lip
for y in range(3, H - 3):                        # the full-corridor band (cols 16-17)
    for x in (16, 17):
        scrub[y * W + x] = 1

# ---- precedence: structure > drop > track > pan > scrub ---------------------------------
for i in range(W * H):
    if canyon[i]:
        redrock[i] = 0
    if redrock[i] or canyon[i]:
        trail[i] = hardpan[i] = scrub[i] = 0
    if trail[i]:
        hardpan[i] = 0
        scrub[i] = 0 if not (i % W in (16, 17)) else scrub[i]
    if scrub[i]:
        hardpan[i] = 0
# the band pauses the track THROUGH it (the road rolls, §11 r7), except the camp leg
for y in (16, 17):
    for x in (16, 17):
        trail[y * W + x] = 0
# the rim lookout pocket stays open sand (never scrub/pan)
for y in range(19, 23):
    for x in range(27, 34):
        if not canyon[y * W + x]:
            scrub[y * W + x] = hardpan[y * W + x] = 0

# ---- base: four ripple fills ----------------------------------------------------------------
base = [gid(f"sere{rng.choice((0, 0, 1, 2, 3))}", set=S) for _ in range(W * H)]

terrain_layers = [
    {"name": "t_hardpan", "role": "terrain", "terrain": "hardpan", "set": S, "depth": 0, "data": hardpan},
    {"name": "t_scrub", "role": "terrain", "terrain": "serescrub", "set": S, "depth": 0, "data": scrub},
    {"name": "t_redrock", "role": "terrain", "terrain": "redrock", "set": S, "depth": 0, "data": redrock},
    {"name": "t_canyon", "role": "terrain", "terrain": "canyon", "set": S, "depth": 0, "data": canyon},
    {"name": "t_trail", "role": "terrain", "terrain": "seretrail", "set": S, "depth": 0, "data": trail},
]

deco = mk.make_grid(W, H)

m = {
    "id": "the_sere", "display_name": "The Sere", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref(), SERE_REF],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": [], "warps": [], "triggers": [], "npcs": [], "gates": [], "encounters": [],
    "music": "assets/audio/music/galehigh-terraces-c.mp3",
}
owed: list[str] = []

# ---- THE RIO TOWER on the rim (walk-behind: only the 2-row base collides) --------------
TOWER = (28, 7)                                    # 5x11; door on col 2 -> (30,17)
m["objects"].append({"id": "rio_tower", "sprite": "sere_rio_tower",
                     "at": {"tx": TOWER[0], "ty": TOWER[1]}, "w": 5, "h": 11,
                     "overhang": 9, "walk_under": True})
DOOR = (TOWER[0] + 2, TOWER[1] + 10)
m["warps"].append({"id": "enter_rio_tower", "at": {"tx": DOOR[0], "ty": DOOR[1]},
                   "trigger": "step_on", "to_map": "rio_tower_1", "to": {"tx": 6, "ty": 9},
                   "facing": "up", "transition": "door"})

# ---- west gap <- Galehigh (lands ON Galehigh's to_sere pair at (31,19)/(31,20)) ----------
for i, y in enumerate((16, 17)):
    m["warps"].append({"id": "to_galehigh" if i == 0 else "to_galehigh_s",
                       "at": {"tx": 0, "ty": y}, "trigger": "step_on",
                       "to_map": "galehigh_terraces", "to": {"tx": 30, "ty": 19 + i},
                       "facing": "left", "transition": "fade"})

# ---- THE CALLING RODS: dark/lit twins (same footprint), the interact on the base ---------
RODS = {1: (4, 4), 2: (26, 23), 3: (33, 18)}      # top tile; the base is (x, y+2)
for n, (x, y) in RODS.items():
    flag = f"flag:sere_rod_{n}"
    m["objects"] += [
        {"id": f"rod_{n}", "sprite": "sere_rod_dark", "at": {"tx": x, "ty": y}, "w": 1, "h": 3,
         "overhang": 2, "walk_under": True, "hidden_when_flag": flag},
        {"id": f"rod_{n}_lit", "sprite": "sere_rod_lit", "at": {"tx": x, "ty": y}, "w": 1, "h": 3,
         "overhang": 2, "walk_under": True, "requires_flag": flag},
    ]
    m["triggers"].append({"id": f"rod_{n}", "kind": "cutscene", "at": {"tx": x, "ty": y + 2},
                          "activation": "interact", "ref": f"script.sere_rod_{n}"})
    owed.append(f"script.sere_rod_{n}")

# ---- the dune bank (a one-way hop south from the rod-1 shelf; walk back round) -----------
for x in range(3, 11):
    if x == 11:
        continue
    deco[14 * W + x] = gid("sere_ledge_s" if x % 3 else "sere_ledge_s_v1", set=S)

# ---- the drovers' camp (north) -------------------------------------------------------------
m["objects"] += [
    {"id": "camp_tent", "sprite": "sere_tent", "at": {"tx": 14, "ty": 4}, "w": 3, "h": 3},
    {"id": "camp_fire", "sprite": "sere_campfire", "at": {"tx": 15, "ty": 9}, "w": 1, "h": 1},
    {"id": "camp_wagon", "sprite": "sere_wagon", "at": {"tx": 8, "ty": 5}, "w": 3, "h": 2},
    {"id": "camp_jars", "sprite": "sere_water_jars", "at": {"tx": 11, "ty": 5}, "w": 2, "h": 1},
]
m["npcs"] += [
    {"id": "drover_hesk", "at": {"tx": 14, "ty": 9}, "facing": "right", "sprite": "market_trader",
     "movement": "static", "dialogue_ref": "script.sere_hesk"},
    {"id": "drover_kid", "at": {"tx": 16, "ty": 7}, "facing": "down", "sprite": "kite_child",
     "movement": "look_around", "dialogue_ref": "npc.sere_drover_kid"},
]
owed += ["script.sere_hesk (the camp rest)", "npc.sere_drover_kid"]

# ---- the rim lookout (east) ----------------------------------------------------------------
m["objects"] += [
    {"id": "spyglass", "sprite": "sere_spyglass", "at": {"tx": 31, "ty": 22}, "w": 1, "h": 2,
     "overhang": 1, "walk_under": True},
    {"id": "rim_post_a", "sprite": "sere_rim_post", "at": {"tx": 29, "ty": 23}, "w": 1, "h": 1},
    {"id": "rim_post_b", "sprite": "sere_rim_post", "at": {"tx": 33, "ty": 21}, "w": 1, "h": 1},
]
m["triggers"].append({"id": "spyglass", "kind": "cutscene", "at": {"tx": 31, "ty": 23},
                      "activation": "interact", "ref": "script.sere_spyglass"})
m["npcs"].append({"id": "surveyor_lio", "at": {"tx": 29, "ty": 21}, "facing": "right",
                  "sprite": "star_watcher", "movement": "look_around",
                  "dialogue_ref": "script.sere_surveyor"})
owed += ["script.sere_spyglass", "script.sere_surveyor"]

# ---- trainer beats (sight trainers ARE geometry) -------------------------------------------
# A: the dune-runner on the camp leg (row 11 crosses the track at cols 12-13)
owed += pt.trainer_beat(m, tid="sere_runner", at=(15, 11), facing="left", sight=3,
                        sprite="kite_weaver")
# B: the storm-chaser watching the wash's east end (col 24 — rod 2's approach)
owed += pt.trainer_beat(m, tid="sere_chaser", at=(24, 21), facing="down", sight=5,
                        sprite="pass_walker")

# ---- caches (variety rule: a valuable off the lane, a consumable, loose wicks) -------------
owed += pt.cache(m, cid="sere_beacon", at=(3, 26))
owed += pt.cache(m, cid="sere_balm", at=(12, 22))
owed += pt.cache(m, cid="sere_wicks", at=(31, 4))

# ---- signs ----------------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="sere_welcome", at=(4, 15))
owed += pt.sign(m, deco, W, sid="sere_rio_tower", at=(25, 15))
owed += pt.sign(m, deco, W, sid="sere_rods", at=(19, 15))
owed += pt.sign(m, deco, W, sid="sere_wash", at=(22, 19))

# ---- props: a landmark on every screen (§11; audit_visual) ----------------------------------
PROPS = [
    ("hoodoo", (6, 17), "sere_hoodoo", 2, 3, 2),   # stands at the gap like a gatepost
    ("hoodoo_b", (21, 11), "sere_hoodoo", 2, 3, 2),
    ("hoodoo_c", (10, 27), "sere_hoodoo", 2, 3, 2),
    ("hoodoo_d", (37 - 9, 25), "sere_hoodoo", 2, 3, 2),
    ("butte_a", (3, 20), "sere_butte", 3, 2, 1),
    ("butte_b", (22, 13), "sere_butte", 3, 2, 1),
    ("butte_c", (18, 29), "sere_butte", 3, 2, 1),
    ("rocks_a", (9, 18), "sere_rock_pair", 2, 2, 1),
    ("rocks_b", (23, 3), "sere_rock_pair", 2, 2, 1),
    ("rocks_c", (14, 19), "sere_rock_pair", 2, 2, 1),
    ("rocks_d", (6, 29), "sere_rock_pair", 2, 2, 1),
    ("rocks_e", (36 - 11, 10), "sere_rock_pair", 2, 2, 1),
]
for oid, (x, y), sprite, w_, h_, ov in PROPS:
    o = {"id": oid, "sprite": sprite, "at": {"tx": x, "ty": y}, "w": w_, "h": h_}
    if ov:
        o.update(overhang=ov, walk_under=True)
    m["objects"].append(o)
SCRUBS = [(3, 7), (9, 3), (19, 5), (7, 15), (11, 19), (19, 21), (4, 23), (13, 24),
          (25, 20), (8, 31 - 2), (23, 29), (28, 3), (32, 7), (26, 9), (11, 13), (2, 18),
          (15, 21), (5, 13), (30, 29), (24, 16)]
for i, (x, y) in enumerate(SCRUBS):
    m["objects"].append({"id": f"bush_{i}", "sprite": "sere_thornbush" if i % 2 else "sere_saltbush",
                         "at": {"tx": x, "ty": y}, "w": 1, "h": 1})
for (x, y) in [(18, 9), (10, 25), (27, 17 - 1), (5, 19)]:
    deco[y * W + x] = gid("boulder")

# ---- encounters (zones from the paint; band 30-34) ------------------------------------------
def T(*rows):
    return [{"kin_id": k, "weight": w_, "min_level": lo, "max_level": hi} for (k, w_, lo, hi) in rows]


SCRUB_TABLE = T((101, 35, 30, 32), (45, 30, 30, 32), (48, 20, 30, 32), (46, 15, 31, 33))
DEEP_TABLE = T((89, 30, 31, 33), (98, 25, 31, 33), (43, 20, 32, 33), (46, 20, 32, 34),
               (102, 5, 33, 34))
band = mk.make_grid(W, H)
beds = mk.make_grid(W, H)
deep = mk.make_grid(W, H)
for i in range(W * H):
    if scrub[i]:
        x, y = i % W, i // W
        if x in (16, 17):
            band[i] = 1
        elif y >= 20:
            deep[i] = 1
        else:
            beds[i] = 1
m["encounters"] += pt.zones_from_grid(beds, W, H, terrain="tall_grass", rate=0.10,
                                      table=SCRUB_TABLE, id_prefix="scrub")
m["encounters"] += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.10,
                                      table=DEEP_TABLE, id_prefix="band")
m["encounters"] += pt.zones_from_grid(deep, W, H, terrain="tall_grass", rate=0.10,
                                      table=DEEP_TABLE, id_prefix="wash")

if __name__ == "__main__":
    ok = mk.finalize(m)
    pt.report(owed)
    raise SystemExit(0 if ok else 1)
