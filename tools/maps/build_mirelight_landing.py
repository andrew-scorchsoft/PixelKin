#!/usr/bin/env python3
"""
The Mirelights: the Landing (09-the-wild-ways §2 B; kind route, region east,
bands 38-41). The far shore of the Glassmere, where Old Ansel's ferry puts in:
the last stilts of the drowned causeway-village, and the first of the boards.

Three signature touches (level-design §8):
  1. THE STILT VILLAGE: three huts standing in their own pools along a reed
     lane — one still kept, by Nell, the last causeway-villager, who tells you
     what the lights are (the fen's one lamp, asleep; these are its dreams).
  2. TOBIN'S BOAT, beached by the boards, painter tied, oars shipped neat: he
     went on by foot, after the lights.
  3. THE FIRST BOARDS (the kit's teaching beat, one new idea per screen): the
     Glassmere's first arm is DEEP (no Gift swims it) and three plank walks
     cross it, each under its own blue will-light. Through the Frostglass Lens
     the causeway-reeds at their mouths tell the truth: one LIT (the real
     board-walk, the middle one), two DEAD — their last boards give way.

HANDSHAKE: west `to_fen`/`_s` (0,23)/(0,24) <-> saltreach_fen_i's ferry stage
`to_mirelight`/`_s` (31,23)/(31,24); east `to_glassmere`/`_s` (29,34)/(29,35) <->
mirelight_glassmere (0,34)/(0,35). Geometry: x 59..89, y -116..-72.

Run:  python3 tools/maps/build_mirelight_landing.py
"""
from __future__ import annotations

import random

import mapkit as mk
import mirelight_common as mc
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 30, 44
rng = random.Random(16501)
owed: list[str] = []

tree = mk.make_grid(W, H)
pond = mk.make_grid(W, H)
grass = mk.make_grid(W, H)
path = mk.make_grid(W, H)
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)

mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(1, 8, 2), (1, 36, 2), (6, 1, 2), (17, 42, 2)], rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)

# ---- the Glassmere's edge on the west (Ansel's water, continuing fen_i's inlet)
for y in range(17, 31):
    for x in range(0, 5):
        tree[y * W + x] = 0
mk.blob(pond, W, H, 1.5, 20.5, 2.6, 2.4)
mk.blob(pond, W, H, 1.5, 27.0, 2.6, 2.4)
for y in list(range(20, 23)) + list(range(25, 28)):
    for x in range(0, 3):
        pond[y * W + x] = 1

# ---- the first ARM of the mere: a full-height deep channel (x 20-26) ----------
ARM_X0, ARM_X1 = 20, 26
for y in range(0, H):
    for x in range(ARM_X0, ARM_X1 + 1):
        pond[y * W + x] = 1
        tree[y * W + x] = 0
mk.blob(pond, W, H, 19.0, 12.0, 1.6, 3.2)        # bays bite the west shore
mk.blob(pond, W, H, 19.2, 22.0, 1.4, 2.4)
# the east shore: a strip at the exit, wood above and below
for y in range(0, H):
    for x in range(ARM_X1 + 1, W):
        tree[y * W + x] = 1
for y in range(29, 40):
    for x in range(ARM_X1 + 1, W):
        tree[y * W + x] = 0
mk.blob(tree, W, H, 28.5, 29.0, 1.4, 1.0)
mk.blob(tree, W, H, 28.5, 40.0, 1.4, 1.0)
for y in range(29, 40):                         # the wood runs on past the exit
    if y not in (34, 35):
        tree[y * W + W - 1] = 1
for y in (17, 18, 29, 30):                      # the west shore's wood edge
    tree[y * W + 0] = 1

# ---- the stilt huts' pools ------------------------------------------------------
HUTS = {"hut_a": (4, 11), "hut_b": (14, 14), "hut_c": (6, 31)}
mk.blob(pond, W, H, 5.5, 12.6, 2.9, 1.6)
mk.blob(pond, W, H, 15.5, 15.8, 2.7, 1.5)
mk.blob(pond, W, H, 7.5, 32.6, 2.8, 1.5)
mk.blob(pond, W, H, 9.0, 5.0, 2.0, 1.2)         # a reed-mere in the north

# ---- the reed lane (path) ---------------------------------------------------------
LANE = set()


def lane(x0, y0, x1, y1):
    for y in range(min(y0, y1), max(y0, y1) + 1):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            LANE.add((x, y))


lane(0, 23, 11, 24)        # off Ansel's stage
lane(11, 6, 11, 39)        # the spine, north-south
lane(5, 15, 11, 15)        # to hut A's ladder
lane(11, 18, 15, 18)       # to hut B's ladder
lane(7, 34, 19, 34)        # hut C + the middle walk's mouth
lane(11, 30, 19, 30)       # the north walk's mouth
lane(11, 38, 19, 38)       # the south walk's mouth
lane(27, 33, 28, 35)       # the far shore
lane(29, 34, 29, 35)       # the exit
for (x, y) in LANE:
    path[y * W + x] = 1
    pond[y * W + x] = 0
    tree[y * W + x] = 0
# hut approaches stay dry (the ladder's foot)
DRY = {(5, 14), (5, 15), (15, 17), (15, 18), (7, 33), (7, 34), (19, 28), (19, 29),
       (19, 32), (19, 33), (19, 36), (19, 37), (17, 39), (19, 30), (19, 34), (19, 38)}
for (x, y) in DRY:
    pond[y * W + x] = 0

# ---- reed beds (the encounter terrain) — the lane pauses through the band ----
mk.blob(grass, W, H, 6.5, 5.5, 3.4, 1.8)
mk.blob(grass, W, H, 16.5, 8.0, 2.6, 2.2)
mk.blob(grass, W, H, 5.5, 37.0, 3.0, 1.6)
for y in (26, 27):                              # the mandatory reed crossing
    for x in range(5, 19):
        grass[y * W + x] = 1
mk.blob(grass, W, H, 15.5, 25.5, 2.6, 1.6)
for i in range(W * H):
    x, y = i % W, i // W
    if path[i]:
        if grass[i] and y in (26, 27):
            path[i] = 0
        else:
            grass[i] = 0
    if tree[i] or pond[i]:
        grass[i] = 0
    if tree[i]:
        pond[i] = 0
        path[i] = 0

m: dict = {
    "id": "mirelight_landing", "display_name": "The Mirelights",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/mirelight.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/mirelight-a.webp",
                         "assets/backgrounds/battle/mirelight-b.webp"],
    "ambience": {**mc.MIRE_AMB, "bob_gids": [gid("buoy")]},
}
wk.use_traverse(m)
obj = lambda *a, **k: mc.obj(m, *a, **k)  # noqa: E731

# ---- warps -------------------------------------------------------------------------
for i, y in enumerate((23, 24)):
    m["warps"].append({"id": "to_fen" + ("_s" if i else ""), "at": {"tx": 0, "ty": y},
                       "trigger": "step_on", "to_map": "saltreach_fen_i",
                       "to": {"tx": 31, "ty": y}, "facing": "left", "transition": "fade"})
for i, y in enumerate((34, 35)):
    m["warps"].append({"id": "to_glassmere" + ("_s" if i else ""), "at": {"tx": W - 1, "ty": y},
                       "trigger": "step_on", "to_map": "mirelight_glassmere",
                       "to": {"tx": 0, "ty": y}, "facing": "right", "transition": "fade"})

# ---- 3. the first boards: three walks over the arm, one true ------------------------
dunks: list = []
mc.walk(m, deco, W, wid="landing_north", mouth=(19, 30), dir="right", length=5,
        true=False, dunks=dunks)
mc.walk(m, deco, W, wid="landing_mid", mouth=(19, 34), dir="right", length=7,
        true=True, dunks=dunks)
mc.walk(m, deco, W, wid="landing_south", mouth=(19, 38), dir="right", length=4,
        true=False, dunks=dunks)
owed += [f"script.mirelight_dunk_{d[0]}" for d in dunks]
# more lies drifting on the arm (they all look the same without the lens)
for k, (x, y) in enumerate([(23, 6), (22, 15), (24, 21), (21, 41), (25, 26)]):
    obj(f"will_light_{k}", "mirelight_marsh_light", (x, y), 1, 1, solid=False)

# ---- the jetty + Ansel waiting with his punt ---------------------------------------
obj("ferry_stage", "mirelight_ferry_stage", (0, 23), 3, 2, solid=False)
obj("ansel_punt", "saltreach_punt", (1, 25), 2, 3, solid=False)
m["npcs"].append({"id": "ansel_landing", "at": {"tx": 4, "ty": 22}, "facing": "down",
                  "sprite": "old_salt", "movement": "look_around",
                  "dialogue_ref": "script.mirelight_ansel_landing"})
owed.append("script.mirelight_ansel_landing")

# ---- 1. the stilt village ---------------------------------------------------------
for hid, (hx, hy) in HUTS.items():
    obj(hid, "mirelight_stilt_hut", (hx, hy), 3, 3, overhang=1)
m["npcs"].append({"id": "nell", "at": {"tx": 16, "ty": 18}, "facing": "left",
                  "sprite": "npc_old_woman", "movement": "look_around",
                  "dialogue_ref": "script.mirelight_nell"})
owed.append("script.mirelight_nell")
m["triggers"].append({"id": "hut_c_door", "kind": "script", "at": {"tx": 7, "ty": 33},
                      "activation": "interact", "ref": "script.mirelight_empty_hut"})
owed.append("script.mirelight_empty_hut")
obj("nell_net_rack", "saltreach_net_rack", (17, 16), 3, 2, overhang=1, walk_under=True)
obj("village_stooks", "saltreach_reed_stooks", (8, 16), 2, 2, overhang=1, walk_under=True)
obj("village_traps", "saltreach_eel_trap", (2, 13), 2, 2, overhang=1, walk_under=True,
    solid=False)
obj("village_moorings", "saltreach_mooring_posts", (9, 33), 1, 2, overhang=1, walk_under=True)
obj("drowned_lamp_a", "saltreach_sunken_lamp", (20, 3), 1, 3, overhang=2, walk_under=True,
    solid=False)
obj("drowned_lamp_b", "saltreach_sunken_lamp", (20, 17), 1, 3, overhang=2, walk_under=True,
    solid=False)
obj("village_lamp", "coldfog_doused_lamp", (12, 21), 1, 3, overhang=2, walk_under=True)

# ---- 2. Tobin's boat --------------------------------------------------------------
obj("tobins_boat", "coldfog_beached_boat", (15, 40), 3, 2)
m["triggers"].append({"id": "tobins_boat", "kind": "script", "at": {"tx": 16, "ty": 40},
                      "activation": "interact", "ref": "script.mirelight_tobins_boat"})
owed.append("script.mirelight_tobins_boat")

# ---- trainer, cache, signs ----------------------------------------------------------
owed += pt.trainer_beat(m, tid="mire_eelcatcher", at=(11, 19), facing="down", sight=4,
                        sprite="fen_folk")
owed += pt.cache(m, cid="mire_landing_reeds", at=(17, 6))
owed += pt.cache(m, cid="mire_landing_tin", at=(28, 38))   # the far-shore pocket pays
owed += pt.sign(m, deco, W, sid="mirelight_landing", at=(6, 22))
owed += pt.sign(m, deco, W, sid="mirelight_boards", at=(18, 35))

# landmarks + set dressing so no screen reads flat (§11)
pt.crown_tree(m, oid="willow_n", sprite="coldfog_dead_willow", at=(14, 2))
pt.crown_tree(m, oid="tree_w", sprite="tinderwick_tree_b", at=(1, 3))
pt.crown_tree(m, oid="tree_sw", sprite="tinderwick_tree", at=(2, 38))
pt.crown_tree(m, oid="willow_s", sprite="coldfog_dead_willow", at=(13, 21))
obj("reeds_a", "saltreach_cattails", (17, 11), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_b", "saltreach_cattails", (8, 9), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_c", "saltreach_cattails", (3, 29), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_d", "saltreach_cattails", (9, 35), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_e", "saltreach_cattails", (27, 36), 2, 2, overhang=1, walk_under=True, solid=False)
obj("lily_a", "saltreach_lilypads", (8, 4), 2, 2, solid=False)
obj("lily_b", "saltreach_lilypads", (21, 9), 2, 2, solid=False)
obj("lily_c", "saltreach_lilypads", (22, 24), 2, 2, solid=False)
obj("south_stooks", "saltreach_reed_stooks", (6, 40), 2, 2, overhang=1, walk_under=True)
obj("far_lamp", "saltreach_reed_lantern_lit", (28, 32), 1, 2, overhang=1, walk_under=True)
for (x, y) in [(15, 4), (4, 19), (17, 24), (9, 40), (14, 11), (6, 29)]:
    if not (path[y * W + x] or pond[y * W + x] or tree[y * W + x] or grass[y * W + x]):
        deco[y * W + x] = gid("boulder")
for (x, y) in [(23, 12), (22, 36), (24, 18)]:
    deco[y * W + x] = gid("buoy")

# ambient kin from the landing's own table, off the lane
m["npcs"].append({"id": "amb_lumpin", "at": {"tx": 3, "ty": 17}, "facing": "down",
                  "sprite": "kin_31_overworld", "movement": "wander", "ambient": True,
                  "wander_radius": 1})

mc.zones(m, grass, W, H, prefix="mire", night=mc.LANDING_NIGHT, day=mc.LANDING_DAY)

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": grass},
    {"name": "t_pond", "role": "terrain", "terrain": "pond",
     "set": "vesper_overworld_set", "depth": 0, "data": pond},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": above},
]
WALK = {(x, y) for y in range(H) for x in range(W)
        if not (tree[y * W + x] or pond[y * W + x])}
mc.deep_layer(m, pond, WALK, W, H)

covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (tree, path, grass, pond, deco))}
objcells = {(x, y) for o in m["objects"]
            for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
            for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.12, flowers=0.03,
                 avoid=covered | objcells | busy | LANE)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("DUNKS:", dunks)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
