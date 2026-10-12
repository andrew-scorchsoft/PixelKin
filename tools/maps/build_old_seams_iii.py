#!/usr/bin/env python3
"""
The Old Seams III — the Scree Galleries (09-the-wild-ways §2 D; kind cave,
region east, band 31-33, the darkest floor). The deep the coal comes from.

Down here the floor is cinder-coal itself — warm black stone, glowing in its
cracks — and the galleries are joined by SCREE: loose cinder raked steep, a
`kind:'slope'` flow (carried downhill every step, left/right steers, never back
up). Each scree runs one way only, so every gallery also has a TIMBER LADDER up
its band on the far side — the descent is a zig-zag, the way home is too.

  1. THE UPPER GALLERY (rows 2-8): the ladder down from the rail yard, the
     foremen's old camp (a brazier the coal has kept warm for ninety winters —
     the REST point), a seam-miner. The west scree drops away beyond it.
  2. THE WEST SCREE (x 4-9, rows 9-14) into THE MIDDLE GALLERY (rows 11-17).
     Steer hard left at the top and the scree drops you on a ledge you can only
     reach riding it (a Lumen Drop); ride off it and the scree takes you on.
     The ladder home is at the gallery's EAST end (x24).
  3. THE EAST SCREE (x 20-25, rows 18-23) into THE ROOT (rows 20-27): the
     cinder floor, the veins brightest, and in the middle of the floor the old
     foremen's last ladder — DOWN, into a dark the lamp can't hold (gated on
     the derived Lamplight tier `flag:lamplight_starlight`, blocked line
     `npc.emberroot_dark`). The ladder home is at the WEST end (x6).

HANDSHAKE: `ladder_up` (24,3) <-> old_seams_ii's `ladder_down` (27,27);
`to_heart` (14,26) <-> emberroot_heart's `ladder_up` (9,3).

Run:  python3 tools/maps/build_old_seams_iii.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import seamskit as sk
import wildkit as wk
from mapkit import gid

W, H = 30, 30
rng = random.Random(16603)
owed: list[str] = []

wall = sk.grid(W, H)
shaft = sk.grid(W, H)
deco = sk.grid(W, H)
above = sk.grid(W, H)
sk.fill(wall, W, 0, 0, W - 1, H - 1)

U = sk.cells(2, 2, 27, 8)
M = sk.cells(2, 11, 27, 17)
L = sk.cells(2, 20, 27, 27)
S1 = sk.cells(4, 9, 9, 14)
S2 = sk.cells(20, 18, 25, 23)
FLOOR = U | M | L | S1 | S2
for c in [(2, 2), (3, 2), (27, 2), (27, 3), (2, 8), (27, 8), (26, 8), (2, 14), (3, 14),
          (27, 11), (27, 17), (26, 17), (2, 20), (27, 20), (2, 27), (3, 27), (27, 27),
          (14, 2), (15, 2), (12, 17), (13, 17)]:
    FLOOR.discard(c)
for (x, y) in FLOOR:
    wall[y * W + x] = 0

m: dict = {
    "id": "old_seams_iii", "display_name": "The Old Seams: Scree Galleries",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": sk.MUSIC, "battle_backdrops": list(sk.BACKDROPS),
}
wk.use_traverse(m)
sk.use_seams(m)

# ---- the scree (slopes) + their raked-cinder art; the ladders home ----------------
pin: dict = {}
wk.chute(m, pin, deco, W, S1, "down", fid="west_scree", berms=False, chevrons=0)
wk.chute(m, pin, deco, W, S2, "down", fid="east_scree", berms=False, chevrons=0)
for (x, y) in S1 | S2:
    pin[(x, y)] = f"scree_v_{(x * 3 + y) % 2}"
wk.ladder(m, deco, W, x=24, y0=9, y1=10, sid="ladder_upper")
wk.ladder(m, deco, W, x=6, y0=18, y1=19, sid="ladder_root")
for sp in m["spans"]:
    r = sp["rect"]
    for y in range(r["ty"], r["ty"] + r["h"]):
        assert wall[y * W + r["tx"]], sp["id"]

# cinder-coal floor: the Root is all cinder; the middle gallery is patched with it
for (x, y) in L - S2:
    if not wall[y * W + x]:
        pin[(x, y)] = f"cinder_{(x * 5 + y * 3) % 3}"
for (x, y) in M:          # below the first band it's cinder all the way down
    if not wall[y * W + x] and (x, y) not in S1:
        pin[(x, y)] = f"cinder_{(x * 5 + y * 3) % 3}"

# ---- warps --------------------------------------------------------------------
pt.cave_ladder(m, deco, W, kind="up", at=(24, 3), to_map="old_seams_ii", to=(27, 27))
deco[26 * W + 14] = gid("cave_ladder_down")
m["warps"].append({"id": "to_heart", "at": {"tx": 14, "ty": 26}, "trigger": "step_on",
                   "to_map": "emberroot_heart", "to": {"tx": 9, "ty": 3}, "facing": "down",
                   "requires_flag": "flag:lamplight_starlight",
                   "blocked_ref": "npc.emberroot_dark", "transition": "fade"})


def put(x, y, name):
    deco[y * W + x] = gid(name)


def sput(x, y, name):
    deco[y * W + x] = sk.S(name)


# ---- the foremen's camp (rest point) + the galleries' furniture -------------------
sk.obj(m, "camp_brazier", "interior_brazier", (5, 3), 1, 2, overhang=1, walk_under=True)
sk.obj(m, "camp_barrels", "interior_barrels", (3, 3), 2, 1)
sk.obj(m, "camp_crates", "interior_crates", (7, 2), 2, 2, overhang=1, walk_under=True)
m["triggers"].append({"id": "camp_rest", "kind": "script", "at": {"tx": 5, "ty": 4},
                      "activation": "interact", "ref": "script.old_seams_camp_rest"})
owed.append("script.old_seams_camp_rest")
sk.obj(m, "props_u1", "old_seams_timber_props", (12, 2), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "props_u2", "old_seams_timber_props", (19, 2), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "vein_u", "old_seams_cinder_vein", (16, 5), 2, 2, solid=False)
sk.obj(m, "crystal_u2", "cinderhead_crystal_cluster", (10, 2), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "cart_u", "cinderhead_ore_cart", (12, 6), 2, 2, overhang=0)
sk.obj(m, "tub_u", "traverse_ore_cart", (21, 6), 1, 1)
sk.obj(m, "crystal_u", "cinderhead_crystal_cluster", (25, 6), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "props_m1", "old_seams_timber_props", (14, 11), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "vein_m1", "old_seams_cinder_vein", (11, 15), 2, 2, solid=False)
sk.obj(m, "vein_m2", "old_seams_cinder_vein", (19, 13), 2, 2, solid=False)
sk.obj(m, "lamp_m", "hoard_lamp_unlit", (26, 12), 1, 3, overhang=2, walk_under=True)
sk.obj(m, "vein_l1", "old_seams_cinder_vein", (9, 22), 2, 2, solid=False)
sk.obj(m, "vein_l2", "old_seams_cinder_vein", (16, 21), 2, 2, solid=False)
sk.obj(m, "vein_l3", "old_seams_cinder_vein", (4, 25), 2, 2, solid=False)
sk.obj(m, "vein_l4", "old_seams_cinder_vein", (23, 25), 2, 2, solid=False)
sk.obj(m, "props_l1", "old_seams_timber_props", (12, 24), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "props_l2", "old_seams_timber_props", (15, 24), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "crystal_l", "cinderhead_crystal_cluster", (2, 21), 2, 2, overhang=1, walk_under=True)

for (x, y) in [(10, 6), (22, 4), (17, 15), (8, 16), (25, 15), (19, 26), (7, 23), (11, 20)]:
    put(x, y, "boulder")
for (x, y, n) in [(18, 7, "glowshroom_b"), (21, 16, "glowshroom_a"), (3, 24, "glowshroom_b")]:
    put(x, y, n)
for (x, y, n) in [(9, 4, "vein_a"), (22, 7, "vein_b"), (5, 16, "vein_a"), (16, 13, "vein_b"),
                  (24, 13, "vein_a"), (5, 21, "vein_b"), (11, 25, "vein_a"), (18, 23, "vein_b"),
                  (14, 25, "vein_a"), (26, 22, "vein_b"), (14, 27, "vein_b"), (8, 26, "vein_a")]:
    sput(x, y, n)
for (x, y) in [(13, 6), (3, 6), (10, 12), (23, 16), (16, 20), (21, 27)]:
    put(x, y, "g_pebble")

# ---- trainers, caches, sign ------------------------------------------------------
owed += pt.trainer_beat(m, tid="seams_miner_penhal", at=(17, 4), facing="down", sight=3,
                        sprite="miner_man")
owed += pt.trainer_beat(m, tid="seams_miner_jory", at=(21, 15), facing="left", sight=4,
                        sprite="miner_woman")
owed += pt.cache(m, cid="seams_scree_ledge", at=(2, 12))     # the scree-only ledge
owed += pt.cache(m, cid="seams_root_charge", at=(26, 26))
owed += pt.sign(m, deco, W, sid="old_seams_root", at=(16, 26))

# mirrored in build_species.py OLD_SEAMS_TABLES (keep the two in step)
NIGHT = sk.T((54, 26, 31, 33), (42, 22, 31, 32), (43, 20, 31, 33), (52, 14, 31, 33),
             (55, 8, 32, 33), (37, 4, 33, 33))
DAY = sk.T((54, 24, 57, 62), (42, 20, 56, 61), (43, 20, 58, 63), (52, 14, 58, 63),
           (55, 12, 60, 65), (37, 6, 62, 65))
sk.zone_pair(m, "upper", (10, 2, 27, 8), NIGHT, DAY)
sk.zone_pair(m, "middle", (10, 11, 27, 17), NIGHT, DAY)
sk.zone_pair(m, "root_w", (2, 20, 13, 27), NIGHT, DAY)
sk.zone_pair(m, "root_e", (16, 24, 27, 27), NIGHT, DAY)

sk.finish(m, W, H, wall=wall, shaft=shaft, deco=deco, above=above, rng=rng, floor_mix=0.35)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3, pin_base=pin)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
