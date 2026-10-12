#!/usr/bin/env python3
"""
The Mirelights: the Glassmere (09-the-wild-ways §2 B; kind route, region east,
bands 40-42). THE FALSE-LIGHTS MAZE — a drowned field of deep black water with
the old causeway's islands standing out of it, joined by rope-plank walks.

Every walk has a blue will-light hanging at its far end, and they all look
alike: that is the lie. Through the Frostglass Lens (always held out here —
it was Ansel's price) the causeway-reeds at each walk's mouth tell the truth:
a LIT reed, a real board-walk; a DEAD reed, boards that stop short over the
deep and give way (`script.mirelight_dunk_<id>`: a splash, and you haul out
back at the walk's mouth). No Gift swims the deep; Tidecall still swims the
shallow shelf round every island — and the mere's CURRENTS, one-way slope
flows over that shallow water, carry swimmers where no board goes.

The route (islands I0..I4 + the current islet C):
  I0 (west shore, entry)  --A-->  I1  --B-->  I2  --C-->  I3  --D-->  I4 (exit)
  three walks leave I0 (one true), two leave I1, two leave I2, two leave I3.
  THE CURRENTS: from I3's south shelf a current runs DOWN to islet C (the
  Glassmere pearl, the valuable cache) whose only way off is a long true walk
  back west to I1 — a loop you can only ride one way (§3a rule 1). From I2's
  west shelf the RETURN current sweeps you back down to I0 (the compressor
  home after a dunk-heavy crossing).

HANDSHAKE: west `to_landing`/`_s` (0,34)/(0,35) <-> mirelight_landing (29,34)/(29,35);
east `to_chapel`/`_s` (29,9)/(29,10) <-> mirelight_chapel (0,9)/(0,10).
Geometry: x 89..119, y -116..-72.

Run:  python3 tools/maps/build_mirelight_glassmere.py
"""
from __future__ import annotations

import random

import mapkit as mk
import mirelight_common as mc
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 30, 44
rng = random.Random(16502)
owed: list[str] = []

tree = mk.make_grid(W, H)
pond = [1] * (W * H)            # the whole field is drowned; islands are carved out
grass = mk.make_grid(W, H)
path = mk.make_grid(W, H)
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)

# the wood rims the mere north and south (off-map = continuation)
for y in (0, 1, H - 2, H - 1):
    for x in range(W):
        tree[y * W + x] = 1
mk.blob(tree, W, H, 6.0, 2.0, 4.0, 1.4)
mk.blob(tree, W, H, 19.0, 2.2, 3.0, 1.2)
mk.blob(tree, W, H, 14.0, 41.5, 5.0, 1.6)
mk.blob(tree, W, H, 26.0, 41.0, 3.0, 1.4)

ISLANDS = {
    "I0": (0, 28, 6, 40),
    "I1": (12, 30, 17, 36),
    "I2": (12, 17, 17, 22),
    "I3": (22, 18, 27, 23),
    "I4": (24, 4, 29, 12),
    "C": (24, 30, 27, 34),
}
DRY: set[tuple[int, int]] = set()
for (x0, y0, x1, y1) in ISLANDS.values():
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            DRY.add((x, y))
DRY |= {(7, 28), (7, 29)}               # I0's north spit (where the return current lands)
# round the islands' corners so they read as old ground, not tiles
for (x, y) in [(17, 30), (12, 36), (17, 36), (12, 17), (17, 22), (22, 23), (27, 18),
               (27, 23), (24, 4), (24, 12), (27, 30), (27, 34), (6, 40), (6, 28)]:
    DRY.discard((x, y))
for (x, y) in DRY:
    pond[y * W + x] = 0
for i in range(W * H):
    if tree[i]:
        pond[i] = 0
# the west wood runs on beside the entry shore, the east beside the exit
for y in range(2, H - 2):
    if y not in (34, 35):
        tree[y * W + 0] = 1
        pond[y * W + 0] = 0
    if y not in (9, 10):
        tree[y * W + W - 1] = 1
        pond[y * W + W - 1] = 0

m: dict = {
    "id": "mirelight_glassmere", "display_name": "The Glassmere",
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

# ---- the causeway stones: the old road's paving still crowns each island -----
LANE = set()


def lane(x0, y0, x1, y1):
    for y in range(min(y0, y1), max(y0, y1) + 1):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            LANE.add((x, y))


lane(0, 34, 6, 35)                 # in from the landing
lane(3, 28, 3, 35)                 # I0's spine
lane(3, 33, 6, 33)
lane(3, 38, 6, 38)
lane(3, 35, 3, 38)
lane(12, 33, 14, 33)               # I1
lane(14, 30, 14, 33)
lane(16, 30, 16, 33)
lane(14, 33, 17, 33)
lane(17, 32, 17, 33)
lane(14, 19, 17, 19)               # I2
lane(14, 19, 14, 22)
lane(13, 17, 13, 19)
lane(22, 19, 25, 19)               # I3
lane(25, 18, 25, 19)
lane(22, 18, 22, 19)
lane(25, 9, 29, 10)                # I4 -> the exit
lane(25, 9, 25, 12)
for (x, y) in LANE:
    path[y * W + x] = 1

# ---- reed beds on the islands (the encounter terrain) ------------------------------
mk.blob(grass, W, H, 2.0, 30.5, 1.6, 1.8)
mk.blob(grass, W, H, 2.5, 39.0, 2.2, 1.2)
mk.blob(grass, W, H, 15.5, 35.0, 1.6, 1.4)
mk.blob(grass, W, H, 16.5, 21.0, 1.4, 1.4)
mk.blob(grass, W, H, 26.0, 21.5, 1.6, 1.6)
mk.blob(grass, W, H, 27.5, 6.0, 1.6, 1.6)
for i in range(W * H):
    if path[i] or pond[i] or tree[i]:
        grass[i] = 0
# I2's reed crossing: every way off the north board rolls (§11 rule 7) — the
# lane pauses through it
for y in (20, 21):
    for x in range(12, 18):
        if (x, y) in DRY:
            grass[y * W + x] = 1
            path[y * W + x] = 0

# ---- warps --------------------------------------------------------------------------
for i, y in enumerate((34, 35)):
    m["warps"].append({"id": "to_landing" + ("_s" if i else ""), "at": {"tx": 0, "ty": y},
                       "trigger": "step_on", "to_map": "mirelight_landing",
                       "to": {"tx": 29, "ty": y}, "facing": "left", "transition": "fade"})
for i, y in enumerate((9, 10)):
    m["warps"].append({"id": "to_chapel" + ("_s" if i else ""), "at": {"tx": W - 1, "ty": y},
                       "trigger": "step_on", "to_map": "mirelight_chapel",
                       "to": {"tx": 0, "ty": y}, "facing": "right", "transition": "fade"})

# ---- THE WALKS (true/false) ---------------------------------------------------------
dunks: list = []
# A: off I0 — three walks, the middle one true
mc.walk(m, deco, W, wid="mere_a_north", mouth=(3, 28), dir="up", length=4, true=False, dunks=dunks,
        reed_side=+1)
mc.walk(m, deco, W, wid="mere_a_true", mouth=(6, 33), dir="right", length=5, true=True, dunks=dunks)
mc.walk(m, deco, W, wid="mere_a_south", mouth=(6, 38), dir="right", length=4, true=False, dunks=dunks)
# B: off I1, north
mc.walk(m, deco, W, wid="mere_b_true", mouth=(14, 30), dir="up", length=7, true=True, dunks=dunks)
mc.walk(m, deco, W, wid="mere_b_east", mouth=(16, 30), dir="up", length=5, true=False, dunks=dunks,
        reed_side=+1)
# C: off I2 — east is true, north is the lie
mc.walk(m, deco, W, wid="mere_c_true", mouth=(17, 19), dir="right", length=4, true=True, dunks=dunks)
mc.walk(m, deco, W, wid="mere_c_north", mouth=(13, 17), dir="up", length=4, true=False, dunks=dunks)
# D: off I3, north to the far shore
mc.walk(m, deco, W, wid="mere_d_true", mouth=(25, 18), dir="up", length=5, true=True, dunks=dunks,
        reed_side=+1)
mc.walk(m, deco, W, wid="mere_d_west", mouth=(22, 18), dir="up", length=4, true=False, dunks=dunks)
# E: the long way home off the current islet (true, one-way in practice)
mc.walk(m, deco, W, wid="mere_e_back", mouth=(24, 32), dir="left", length=6, true=True,
        dunks=dunks)
owed += [f"script.mirelight_dunk_{d[0]}" for d in dunks]

# ---- THE CURRENTS (shallow lanes; one-way slope flows) -------------------------------
DOWN_C = {(x, y) for x in (26, 27) for y in range(25, 29)}          # I3 -> islet C
RET_W = {(9, 20), (10, 20)}                                           # I2 -> ...
RET_S = {(8, y) for y in range(20, 27)}                               # ... -> I0
mc.current(m, DOWN_C, "down", fid="current_islet")
mc.current(m, RET_W, "left", fid="current_home_w")
mc.current(m, RET_S, "down", fid="current_home_s")
SHALLOW = DOWN_C | RET_W | RET_S
# mark the currents: buoys on their banks, a sign at each head
for (x, y) in [(25, 26), (28, 27), (7, 22), (9, 24), (11, 21)]:
    deco[y * W + x] = gid("buoy")
for (x, y) in DOWN_C | RET_S:
    if (x + y) % 3 == 0:
        deco[y * W + x] = wk.T("chev_down")
deco[20 * W + 10] = wk.T("chev_left")

# ---- more lies on the water (the will-lights drift where no board goes) ------------
for k, (x, y) in enumerate([(4, 8), (9, 13), (20, 9), (19, 27), (10, 26), (22, 37),
                            (5, 17), (15, 11), (21, 31)]):
    obj(f"will_light_{k}", "mirelight_marsh_light", (x, y), 1, 1, solid=False)

# ---- islands: dressing, trainer, caches, signs -------------------------------------
owed += pt.trainer_beat(m, tid="mire_lampdiver", at=(16, 18), facing="down", sight=4,
                        sprite="fisher_man")
owed += pt.cache(m, cid="mire_pearl", at=(26, 32))             # the valuable: current-only
owed += pt.cache(m, cid="mire_glassmere_balm", at=(27, 9))
owed += pt.sign(m, deco, W, sid="mirelight_glassmere", at=(2, 33))
owed += pt.sign(m, deco, W, sid="mirelight_current", at=(23, 22))
m["npcs"].append({"id": "amb_tidwraith", "at": {"tx": 16, "ty": 35}, "facing": "down",
                  "sprite": "kin_22_overworld", "movement": "wander", "ambient": True,
                  "wander_radius": 1})

pt.crown_tree(m, oid="willow_i0", sprite="coldfog_dead_willow", at=(1, 36))
pt.crown_tree(m, oid="willow_i3", sprite="coldfog_dead_willow", at=(24, 20))
pt.crown_tree(m, oid="tree_i4", sprite="tinderwick_tree_b", at=(26, 4))
obj("drowned_lamp_a", "saltreach_sunken_lamp", (10, 28), 1, 3, overhang=2, walk_under=True, solid=False)
obj("drowned_lamp_b", "saltreach_sunken_lamp", (19, 14), 1, 3, overhang=2, walk_under=True, solid=False)
obj("drowned_lamp_c", "saltreach_sunken_lamp", (21, 39), 1, 3, overhang=2, walk_under=True, solid=False)
obj("drowned_lamp_d", "saltreach_sunken_lamp", (5, 11), 1, 3, overhang=2, walk_under=True, solid=False)
obj("stooks_i1", "saltreach_reed_stooks", (12, 34), 2, 2, overhang=1, walk_under=True)
obj("stooks_i4", "saltreach_reed_stooks", (28, 11), 2, 2, overhang=1, walk_under=True)
obj("reeds_i2", "saltreach_cattails", (12, 20), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_i3", "saltreach_cattails", (26, 22), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_c", "saltreach_cattails", (24, 33), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_i0", "saltreach_cattails", (4, 29), 2, 2, overhang=1, walk_under=True, solid=False)
obj("lily_a", "saltreach_lilypads", (10, 9), 2, 2, solid=False)
obj("lily_b", "saltreach_lilypads", (20, 34), 2, 2, solid=False)
obj("lily_c", "saltreach_lilypads", (2, 21), 2, 2, solid=False)
obj("lily_d", "saltreach_lilypads", (17, 39), 2, 2, solid=False)
obj("wreck_punt", "saltreach_punt", (11, 39), 2, 3, solid=False)
obj("wreck_ribs", "pearlmoor_wreck_ribs", (16, 6), 3, 2, solid=False)
for (x, y) in [(5, 30), (16, 31), (13, 21), (23, 21), (28, 7), (4, 39)]:
    if (x, y) in DRY and not path[y * W + x] and not grass[y * W + x]:
        deco[y * W + x] = gid("boulder")

mc.zones(m, grass, W, H, prefix="mere", night=mc.GLASSMERE_NIGHT, day=mc.GLASSMERE_DAY)

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
deep = mc.deep_layer(m, pond, WALK, W, H, shallow=SHALLOW)

# ---- prove the puzzle: no island reaches another by swimming the shelf ----------------
# (currents excluded — they're one-way by design; planks are the only true links)
swim = {(x, y) for y in range(H) for x in range(W)
        if (pond[y * W + x] and not deep[y * W + x]) and (x, y) not in SHALLOW}
land = {k: {(x, y) for (x, y) in DRY if ISLANDS[k][0] <= x <= ISLANDS[k][2]
            and ISLANDS[k][1] <= y <= ISLANDS[k][3]} for k in ISLANDS}
land["I0"] |= {(7, 28), (7, 29)}


def comp(start):
    seen, st = set(start), list(start)
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n not in seen and (n in swim or n in DRY):
                seen.add(n)
                st.append(n)
    return seen


for k, cells in land.items():
    reach = comp(cells)
    others = [o for o in land if o != k and land[o] & reach]
    assert not others, f"island {k} swims to {others} without a board"

covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (tree, path, grass, pond, deco))}
objcells = {(x, y) for o in m["objects"]
            for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
            for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.14, flowers=0.03,
                 avoid=covered | objcells | busy | LANE)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("DUNKS:", dunks)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
