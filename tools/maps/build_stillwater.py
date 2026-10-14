#!/usr/bin/env python3
"""
Stillwater — the Hollowing's village (walkthrough/11 Part A). Town, 30x30, world
(48,-491): its south edge meets Coldfog Marches I's north edge (x 48-68).

Where the quieted go. North of the drained marsh the Hollowing keep a village of
shuttered lamps, soft voices and sleeping kin, kept warm by hearths with their
faces to the wall. Its people are tired, grieving, kind, and certain the dark is
mercy. Not evil, not stupid; some are beginning to doubt. You are TOLERATED, not
attacked ("you're the one relighting the sky").

THE REGISTER: the Coldfog dread register, but LIVED-IN. Everything tended: the
lanes swept, the shutters painted, blankets folded over the sleeping kin. No
humour at anyone's expense, nothing broken, nobody harmed. The kin are ASLEEP.

Three signature touches (level-design §8):
  1. THE STILL WATER — the mere the village is named for, dead-still murk under
     the north crags, its south shore lined with SHUTTERED lamp-posts (lamps put
     to sleep, not put out). After the dawn two of them stand open and lit.
  2. THE QUIET HALL — the meeting-house on the square, the shutter-wall inside
     (the names of the lamps they've put out; quest 3).
  3. THE SLEEPING YARDS — kin asleep under grey blankets in every yard, breathing
     slow. After the dawn: one window opens on home B, a lamp in it, a child at it.

Standing kit: the inn (`stillwater_shutter`, a rest point -> WorldScene
HEAL_ENTRANCE_MAPS, engine-owned: the coordinator adds it), the dark-lamp maker,
two homes, the quiet hall. Three Hollowing trainers who'd rather TALK first (no
sight lines: you ask, they answer, and then they offer). Wild kin in the grey
meadows (the Hollowing family #178-#180 with the drained Dark/Lunar beds); the
lampmaker's yard keeps the young snuffer-caps (#178, at/below its kindling).

Seams (11 build contract):
  * south cols 4-7  <-> Coldfog Marches I north row 0, cols 4-7 (this lane owns both)
  * south cols 22-25 <-> mourning_fields north row 0, cols 2-5 (Lane N3 owns MF's side;
    the engine no-ops the warps until MF lands)

All optional and late: Coldfog I is reached at gleam:solar. Nothing here grants
a Gleam, a Gift or a crown.

Run:  python3 tools/maps/build_stillwater.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 30
rng = random.Random(178)
owed: list[str] = []
DAWN = "flag:dawn"

COLDFOG_REF = mk.register_tileset(
    "coldfog_set", index=mk.REPO / "assets/tilesets/coldfog/coldfog_set.index.json")
# the village lanes: `flagway`, swept flagstones whose rims are drawn over BLIGHT
# (build_stillwater_set.py — the shared `path` would ring them in green)
STILL_REF = mk.register_tileset(
    "stillwater_set", index=mk.REPO / "assets/tilesets/stillwater/stillwater_set.index.json")

# ---- the seams -------------------------------------------------------------------
CF_COLS = (4, 5, 6, 7)          # -> coldfog_marches_i (x, 1), its north gap
MF_COLS = (22, 23, 24, 25)      # -> mourning_fields (x - 20, 1), Lane N3's north edge

# ---- buildings (tile at, w, h, overhang, door cols) ---------------------------------
HALL = (12, 10)        # 7x5, door col 3
INN = (2, 9)           # 6x6, door cols 2-3
LAMPMAKER = (21, 10)   # 6x5, door cols 2-3
HOME_A = (8, 20)       # 5x5, door col 2
HOME_B = (17, 20)      # 5x5, door col 2

crag = mk.make_grid(W, H)
murk = mk.make_grid(W, H)
tuft = mk.make_grid(W, H)       # the grey meadows (blighttuft)
path = mk.make_grid(W, H)
deco = mk.make_grid(W, H)

# BORDERS: fogcrag all round (the village sits in a bowl of grey crags), organic
mk.rect(crag, W, H, 0, 0, W - 1, 1)
mk.rect(crag, W, H, 0, 0, 1, H - 1)
mk.rect(crag, W, H, 28, 0, 29, H - 1)
mk.rect(crag, W, H, 0, 28, W - 1, H - 1)
mk.organic_border(crag, W, H, depth=0,
                  bumps=[(1, 7, 2), (1, 18, 2), (1, 25, 2), (28, 9, 2), (28, 19, 2),
                         (10, 1, 2), (20, 1, 2), (3, 1, 1), (26, 1, 1),
                         (12, 28, 2), (17, 28, 2), (27, 27, 1)],
                  rng=rng)
for x in list(CF_COLS) + list(MF_COLS):
    for y in range(25, H):
        crag[y * W + x] = 0
for (x, y) in [(3, 27), (8, 27), (21, 27), (26, 27)]:   # soften the gap shoulders
    crag[y * W + x] = 0

# ---- THE STILL WATER (touch #1) ------------------------------------------------------
mk.blob(murk, W, H, 15.2, 4.8, 4.6, 1.9)
mk.blob(murk, W, H, 11.2, 4.9, 1.8, 1.2)
mk.blob(murk, W, H, 19.6, 3.6, 1.9, 1.1)
mk.blob(murk, W, H, 15.8, 6.2, 1.5, 0.8)
mk.blob(murk, W, H, 12.8, 3.0, 1.2, 0.7)
for (x, y) in [(10, 3), (20, 5), (11, 6), (19, 2)]:      # ragged, never a ruled box
    murk[y * W + x] = 0

# ---- lanes -------------------------------------------------------------------------
P: set[tuple[int, int]] = set()
P |= {(x, y) for x in range(3, 27) for y in (15, 16)}                # the main lane
P |= {(x, y) for y in range(16, 20) for x in range(11, 20)
      if ((x - 15) / 3.4) ** 2 + ((y - 17.0) / 1.7) ** 2 <= 1}       # the square
P |= {(x, y) for x in (5, 6) for y in range(15, H)}                  # to Coldfog I
P |= {(x, y) for x in (23, 24) for y in range(15, H)}                # to the Mourning Fields
P |= {(x, y) for x in range(6, 11) for y in (26, 27)} | {(10, 25)}   # home A's door
P |= {(x, y) for x in range(19, 24) for y in (26, 27)} | {(19, 25)}  # home B's door
P |= {(x, 9) for x in range(8, 23)}                                  # the shore walk
P |= {(x, y) for x in (8, 9) for y in range(9, 15)}                  # round the hall, west
P |= {(x, y) for x in (19, 20) for y in range(9, 15)}                # round the hall, east
for (x, y) in P:
    path[y * W + x] = 1
# the four gap columns walk on lane all the way to the edge
for x in (4, 7):
    for y in range(26, H):
        path[y * W + x] = 1
for x in (22, 25):
    for y in range(26, H):
        path[y * W + x] = 1

# ---- the grey meadows (encounter beds) ----------------------------------------------
mk.blob(tuft, W, H, 4.5, 4.4, 2.6, 1.8)        # NW, by the mere's west shore
mk.blob(tuft, W, H, 24.6, 5.0, 2.8, 2.0)       # NE, under the crags
mk.blob(tuft, W, H, 14.5, 24.8, 2.6, 2.2)      # the south meadow between the homes
mk.blob(tuft, W, H, 2.8, 21.5, 1.3, 2.4)       # the west strip
yard = mk.make_grid(W, H)
mk.blob(yard, W, H, 26.2, 17.8, 1.3, 1.6)      # the lampmaker's yard (#178's bed)

# ---- precedence ----------------------------------------------------------------------
for i in range(W * H):
    if crag[i]:
        murk[i] = tuft[i] = path[i] = yard[i] = 0
    if murk[i]:
        tuft[i] = path[i] = yard[i] = 0
    if path[i]:
        tuft[i] = yard[i] = 0
    if yard[i]:
        tuft[i] = 0
for i in range(W * H):
    if yard[i]:
        tuft[i] = 1                    # painted as the same meadow; its own zone below

# ---- base: blight everywhere (the quieted ground) ------------------------------------
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
base = [rng.choice(bl) if rng.random() < 0.5 else bl[0] for _ in range(W * H)]

m: dict = {
    "id": "stillwater", "display_name": "Stillwater",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref(), COLDFOG_REF, STILL_REF],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/stillwater.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/stillwater-a.webp"],
}


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)
    return o


def npc(nid, at, sprite, ref, *, facing="down", movement="static", **kw):
    n = {"id": nid, "at": {"tx": at[0], "ty": at[1]}, "facing": facing,
         "sprite": sprite, "movement": movement, "dialogue_ref": ref}
    n.update(kw)
    m["npcs"].append(n)
    owed.append(ref)
    return n


def trig(tid, at, ref, *, kind="script", activation="interact", **kw):
    t = {"id": tid, "kind": kind, "at": {"tx": at[0], "ty": at[1]},
         "activation": activation, "ref": ref}
    t.update(kw)
    m["triggers"].append(t)
    owed.append(ref)
    return t


# ---- warps: the two seams ------------------------------------------------------------
for x in CF_COLS:
    m["warps"].append({"id": f"to_coldfog_{x}", "at": {"tx": x, "ty": H - 1},
                       "trigger": "step_on", "to_map": "coldfog_marches_i",
                       "to": {"tx": x, "ty": 1}, "facing": "down", "transition": "fade"})
for x in MF_COLS:
    m["warps"].append({"id": f"to_mourning_{x}", "at": {"tx": x, "ty": H - 1},
                       "trigger": "step_on", "to_map": "mourning_fields",
                       "to": {"tx": x - 20, "ty": 1}, "facing": "down", "transition": "fade"})


# ---- buildings + doors ---------------------------------------------------------------
def building(oid, sprite, at, w, h, cols, to_map, landing):
    obj(oid, sprite, at, w, h, overhang=2)
    for c in cols:
        dx, dy = at[0] + c, at[1] + h - 1
        m["warps"].append({"id": f"enter_{oid}" + (f"_{c}" if len(cols) > 1 else ""),
                           "at": {"tx": dx, "ty": dy}, "trigger": "step_on",
                           "to_map": to_map, "to": {"tx": landing[0], "ty": landing[1]},
                           "facing": "up", "transition": "door"})
        path[(dy + 1) * W + dx] = 1
        tuft[(dy + 1) * W + dx] = 0


# interior landings (the interiors' builder pairs them back): see
# build_stillwater_interiors.py — each room's doormat is at (W//2, H-1) and its
# landing one tile above it.
building("quiet_hall", "stillwater_quiet_hall", HALL, 7, 5, (3,), "stillwater_quiet_hall", (9, 12))
building("inn", "stillwater_inn", INN, 6, 6, (2, 3), "stillwater_shutter", (8, 10))
building("lampmaker", "stillwater_lampmaker", LAMPMAKER, 6, 5, (2, 3), "stillwater_lampmaker", (7, 8))
building("home_a", "stillwater_home_a", HOME_A, 5, 5, (2,), "stillwater_home_a", (6, 7))
building("home_b", "stillwater_home_b", HOME_B, 5, 5, (2,), "stillwater_home_b", (6, 7))
# after the dawn: home B's upstairs window stands open, lit, a child at it (touch #3)
obj("home_b_window", "stillwater_window_lit", (HOME_B[0], HOME_B[1] + 2), 2, 2,
    solid=False, requires_flag=DAWN)

# ---- the Still Water's shore: the lamps put to sleep (touch #1) ----------------------
SHORE_LAMPS = [(10, 6), (13, 6), (17, 6), (21, 6)]
for n, (x, y) in enumerate(SHORE_LAMPS):
    opens = n in (1, 2)                       # after the dawn, two of them stand open
    obj(f"shore_lamp_{n}", "stillwater_shut_lamp", (x, y), 1, 3, overhang=2,
        walk_under=True, **({"hidden_when_flag": DAWN} if opens else {}))
    if opens:
        obj(f"shore_lamp_{n}_open", "stillwater_open_lamp", (x, y), 1, 3, overhang=2,
            walk_under=True, requires_flag=DAWN)
trig("shore_lamp_read", (13, 9), "script.still_shore_lamp")
trig("shore_lamp_read_b", (17, 9), "script.still_shore_lamp")
# lane lamps: shuttered, every one
for n, (x, y) in enumerate([(4, 17), (10, 14), (21, 17), (26, 17), (7, 22), (22, 22)]):
    obj(f"lane_lamp_{n}", "stillwater_shut_lamp", (x, y - 2), 1, 3, overhang=2, walk_under=True)

# the far-shore cold lamp (the Shutter-wall's third name) — seen across the water
# from the square, reached the long way round the mere's east shore
obj("far_shore_lamp", "coldfog_doused_lamp", (24, 1), 1, 3, overhang=2, walk_under=True)
trig("far_shore_lamp_read", (24, 3), "script.still_coldlamp_3")

# ---- the willow hollow (quest 1's hiding place) + the notice by the hall -------------
obj("mere_willow", "coldfog_dead_willow", (5, 2), 3, 4, overhang=2, walk_under=True)
obj("willow_candle", "stillwater_candle_jar", (6, 5), 1, 1, solid=False,
    requires_flag="flag:q_still_candle_hidden")
trig("willow_hollow", (6, 6), "script.still_willow_hollow")
obj("hall_notice", "coldfog_hollowing_notice", (10, 11), 1, 2, overhang=1, walk_under=True)
trig("hall_notice_read", (10, 13), "script.still_notice")

# ---- the sleeping yards (touch #3): kin under grey blankets ---------------------------
for n, (x, y, s, ry) in enumerate([(2, 17, "blanket_kin", -1), (12, 22, "blanket_kin_b", 1),
                                   (25, 23, "blanket_kin", 1), (19, 18, "blanket_kin_b", 1),
                                   (26, 13, "blanket_kin_b", 1)]):
    obj(f"sleeper_{n}", f"stillwater_{s}", (x, y), 2, 1)
    trig(f"sleeper_{n}_read", (x, y + ry), "script.still_sleeper")
obj("well", "tinderwick_well", (25, 25), 2, 3, overhang=1)
for n, (x, y) in enumerate([(26, 20), (3, 25), (10, 4), (21, 4)]):
    obj(f"pine_{n}", "windward_bent_pine", (x, y - 2), 2, 3, overhang=2, walk_under=True)

# ---- people ------------------------------------------------------------------------
# the arrival: a greeter at the south gate (a talk, not a band — you're tolerated)
npc("gate_greeter", (8, 25), "hollowing_acolyte", "script.still_greeter", facing="left")
npc("wall_elder", (16, 18), "hollowing_elder", "script.still_elder", facing="down")
npc("candle_child", (13, 21), "npc_girl", "script.still_candle_child", facing="down",
    hidden_when_flag="flag:q_still_candle_done")
npc("candle_child_after", (13, 21), "npc_girl", "script.still_candle_child_after",
    facing="down", movement="look_around", requires_flag="flag:q_still_candle_done")
npc("blanket_folder", (7, 19), "npc_old_woman", "script.still_blanket_folder", facing="left")
npc("lane_sweeper", (20, 15), "npc_man", "script.still_sweeper", facing="left",
    movement="wander", wander_radius=2)
npc("shore_watcher", (15, 8), "npc_woman", "script.still_shore_watcher", facing="up")
npc("doubter", (26, 15), "pass_walker", "script.still_doubter", facing="left",
    movement="look_around")
npc("water_carrier", (27, 24), "npc_parent", "script.still_water_carrier", facing="left")
npc("meadow_keeper", (21, 6), "frost_herder", "script.still_meadow_keeper", facing="left")
npc("tessaly", (9, 16), "fen_folk", "script.still_tessaly", facing="down",
    hidden_when_flag="flag:q_still_tessaly")

# the three trainers who'd rather talk first (no sight line — you ask)
for tid, at, sprite, facing in [("still_acolyte_hale", (12, 18), "hollowing_acolyte", "right"),
                                ("still_acolyte_vesna", (22, 18), "star_watcher", "left"),
                                ("still_lamplighter_grisel", (7, 8), "lamplighter", "right")]:
    flag = f"flag:{tid}_beaten"
    npc(tid, at, sprite, f"script.{tid}", facing=facing, hidden_when_flag=flag)
    npc(f"{tid}_after", at, sprite, f"script.{tid}_after", facing=facing, requires_flag=flag,
        movement="look_around")
    owed.append(f"TRAINERS[{tid}]")

# ambient: the kin that DIDN'T sleep (a dream-moth over the meadow, a snuffer-cap in the yard)
for nid, at, kin in [("amb_moth", (24, 5), 180), ("amb_cap", (26, 17), 178)]:
    m["npcs"].append({"id": nid, "at": {"tx": at[0], "ty": at[1]}, "facing": "down",
                      "sprite": f"kin_{kin}_overworld", "movement": "wander",
                      "ambient": True, "wander_radius": 1})

# ---- signs + caches --------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="stillwater", at=(8, 27))
owed += pt.sign(m, deco, W, sid="stillwater_hall", at=(14, 15))
owed += pt.sign(m, deco, W, sid="stillwater_mourning", at=(21, 26))
owed += pt.cache(m, cid="stillwater_meadow", at=(3, 4))        # NW meadow nook
owed += pt.cache(m, cid="stillwater_far_shore", at=(26, 3))    # round the mere, by the cold lamp

# ---- encounters (night 48-52; the dawn wakes the beds into their day forms) ----------
NIGHT = [
    {"kin_id": 180, "weight": 28, "min_level": 48, "max_level": 51},  # the dream-moth
    {"kin_id": 179, "weight": 18, "min_level": 49, "max_level": 52},  # the lantern-keeper
    {"kin_id": 136, "weight": 18, "min_level": 48, "max_level": 50},  # Mothdim
    {"kin_id": 137, "weight": 14, "min_level": 49, "max_level": 51},  # Nullmoth
    {"kin_id": 113, "weight": 10, "min_level": 50, "max_level": 52},  # Omenire (Lunar/Dark)
    {"kin_id": 112, "weight": 12, "min_level": 49, "max_level": 51},  # Nightwraith (Lunar)
]
YARD = [
    {"kin_id": 178, "weight": 70, "min_level": 42, "max_level": 44},  # snuffer-caps (pre-kindle)
    {"kin_id": 180, "weight": 30, "min_level": 46, "max_level": 48},
]
DAY = [
    {"kin_id": 179, "weight": 24, "min_level": 56, "max_level": 60},
    {"kin_id": 180, "weight": 22, "min_level": 55, "max_level": 59},
    {"kin_id": 140, "weight": 18, "min_level": 58, "max_level": 62},  # Wisprestored: the light back
    {"kin_id": 133, "weight": 18, "min_level": 55, "max_level": 60},  # Flutterwane
    {"kin_id": 134, "weight": 18, "min_level": 56, "max_level": 61},  # Wispwane
]
DAY_YARD = [
    {"kin_id": 178, "weight": 60, "min_level": 42, "max_level": 44},
    {"kin_id": 140, "weight": 40, "min_level": 55, "max_level": 58},
]
meadow = [tuft[i] and not yard[i] for i in range(W * H)]
zones = pt.zones_from_grid([1 if v else 0 for v in meadow], W, H, terrain="tall_grass",
                           rate=0.10, table=NIGHT, id_prefix="meadow")
zones += pt.zones_from_grid(yard, W, H, terrain="tall_grass", rate=0.10, table=YARD,
                            id_prefix="yard", min_cells=1)
for z in zones:
    day = dict(z)
    z["hidden_when_flag"] = DAWN
    day.update(id=f"{z['id']}_day", table=DAY_YARD if z["id"].startswith("yard") else DAY,
               requires_flag=DAWN)
    m["encounters"] += [z, day]

# ---- drained dressing --------------------------------------------------------------------
busy = {(x, y) for y in range(H) for x in range(W)
        if any(g[y * W + x] for g in (crag, murk, tuft, path))}
busy |= {(x, y) for o in m["objects"]
         for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
         for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy |= {(p["at"]["tx"], p["at"]["ty"]) for p in m["npcs"] + m["triggers"] + m["warps"]}
for (x, y) in [(9, 19), (2, 12), (27, 22), (20, 2)]:
    if (x, y) not in busy and deco[y * W + x] == 0:
        deco[y * W + x] = gid("boulder")
        busy.add((x, y))
litter = [gid("greymoss_a"), gid("greymoss_b"), gid("g_pebble")]
for y in range(2, 27):
    for x in range(2, 28):
        if (x, y) not in busy and deco[y * W + x] == 0 and rng.random() < 0.09:
            deco[y * W + x] = rng.choice(litter)

# ---- ambience: the coldfog's hush, a little gentler (the village is warm indoors) -----
m["ambience"] = {
    "particles": [{"kind": "motes", "density": 0.7}],
    "mist": {"color": "#c9ced6", "alpha": 0.24, "speed": 4},
    "tint": {"color": "#7d8796", "alpha": 0.14},
    "starfall": {"min_s": 30, "max_s": 60},
    "when": [{"flag": DAWN, "ambience": {
        "particles": [{"kind": "motes", "density": 0.5}],
        "mist": {"color": "#e8eef6", "alpha": 0.08, "speed": 8},
        "starfall": {"min_s": 40, "max_s": 90},
        "light_sources_extra": [
            {"at": {"tx": 12, "ty": 7}, "radius": 14, "color": "#ffd089"},
            {"at": {"tx": 18, "ty": 7}, "radius": 14, "color": "#ffd089"},
            {"at": {"tx": 18, "ty": 22}, "radius": 12, "color": "#ffcf7a"},
        ]}}],
}

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_path", "role": "terrain", "terrain": "flagway",
     "set": "stillwater_set", "depth": 0, "data": path},
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": tuft},
    {"name": "t_murk", "role": "terrain", "terrain": "murk",
     "set": "vesper_overworld_set", "depth": 0, "data": murk},
    {"name": "t_fogcrag", "role": "terrain", "terrain": "fogcrag",
     "set": "coldfog_set", "depth": 0, "data": crag},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(sorted(set(owed)))
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
