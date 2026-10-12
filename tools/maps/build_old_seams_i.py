#!/usr/bin/env python3
"""
The Old Seams I — the Shaft Benches (09-the-wild-ways §2 D; kind cave, region
east, band 27-29, dark). The first floor under Cinderhead's sealed seam-door.

The old crew worked this floor as three BENCHES stepping down the seam, each cut
through by open SHAFTS the foremen bored to follow the warm coal down. Nobody
filled them; they laid planks. The floor teaches the descent's two verbs, one
per bench (§3a r5), and zig-zags you down:

  1. BENCH A (rows 2-7): the headframe at the foot of the seam-door ladder
     (the way home), then the first shaft — walk the plank over it (along the
     boards only; there's nothing either side). East end: a timber ladder down
     the rock band (rows 8-9) — the second verb.
  2. BENCH B (rows 10-17): back WEST over a longer plank; off it a short plank
     to a pillar islet over the pit (a dead end that pays). A boulder wall turns
     you down to the band's west ladder; a seam-miner works the pocket.
  3. BENCH C (rows 20-27): a plank to a rock pillar, a plank DOWN off it to the
     bottom ledge, along the ledge east to the ladder-pit to the rail yard.

Every ladder climbs both ways (wildkit spans), so the whole floor walks back
to the headframe. The one ONE-WAY line is a cinder-scree spill through band 2 at
the east end (x24, a slope flow): a quick drop from bench B to bench C on the
way down — the way back up is the long zig-zag (§3a r1: loops, not corridors).
Stand-ins: none (the Old Seams prop kit is in).

HANDSHAKE: `to_mine` (4,4) on the headframe collar <-> cinderhead_mine's
seam-door (16,3) [lands (16,4)]; `ladder_down` (26,24) <-> old_seams_ii's
`ladder_up` (5,6).

Run:  python3 tools/maps/build_old_seams_i.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import seamskit as sk
import wildkit as wk
from mapkit import gid

W, H = 30, 30
rng = random.Random(16601)
owed: list[str] = []

wall = sk.grid(W, H)
shaft = sk.grid(W, H)
deco = sk.grid(W, H)
above = sk.grid(W, H)
sk.fill(wall, W, 0, 0, W - 1, H - 1)

FLOOR = (sk.cells(1, 2, 28, 7) | sk.cells(1, 10, 28, 17) |
         sk.cells(1, 20, 8, 26) | sk.cells(9, 20, 28, 27))
# ragged rock: bites out of the bench edges so the benches never read as boxes
for c in [(1, 2), (2, 2), (28, 2), (28, 3), (1, 7), (27, 7), (28, 7), (1, 10), (28, 10),
          (28, 11), (1, 17), (2, 17), (28, 17), (1, 20), (28, 20), (28, 21), (1, 26),
          (19, 27), (20, 27), (28, 27), (10, 2), (19, 2)]:
    FLOOR.discard(c)
for (x, y) in FLOOR:
    wall[y * W + x] = 0

# the open shafts (pits) — collide; the boards over them are spans
PITS = (sk.cells(11, 2, 18, 7) |
        (sk.cells(12, 10, 19, 17) - sk.cells(15, 10, 16, 12)) |
        (sk.cells(9, 20, 18, 26) - sk.cells(13, 21, 14, 23)))
# never ruler-drawn: the pits bite into the benches here and there
PITS |= {(10, 7), (19, 3), (19, 4), (11, 17), (20, 16), (20, 17), (11, 10), (8, 25), (8, 26),
         (19, 20)}
PITS -= {(11, 2), (18, 7), (19, 10), (18, 26), (9, 20)}
wall[2 * W + 11] = 1                                    # the pit's NW lip is rock, not a stub
for (x, y) in PITS:
    shaft[y * W + x] = 1
    wall[y * W + x] = 0

m: dict = {
    "id": "old_seams_i", "display_name": "The Old Seams",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": sk.MUSIC, "battle_backdrops": list(sk.BACKDROPS),
}
wk.use_traverse(m)
sk.use_seams(m)

# ---- the traversal: planks over the shafts, ladders down the bands -------------
wk.plank(m, deco, W, rect=(11, 5, 8, 1), axis="h", sid="plank_a")
wk.plank(m, deco, W, rect=(12, 14, 8, 1), axis="h", sid="plank_b")
wk.plank(m, deco, W, rect=(12, 11, 3, 1), axis="h", sid="plank_islet")
wk.plank(m, deco, W, rect=(9, 22, 4, 1), axis="h", sid="plank_c")
wk.plank(m, deco, W, rect=(13, 24, 1, 3), axis="v", sid="plank_c_drop")
wk.ladder(m, deco, W, x=26, y0=8, y1=9, sid="ladder_band_a")
wk.ladder(m, deco, W, x=3, y0=18, y1=19, sid="ladder_band_b")
# the one-way way down: a cinder-scree spill through band 2 at the east end (a
# slope flow — carried down, never back up). Riders of it skip bench B's west
# and bench C's planks on the way DOWN; the way back up is the long zig-zag.
SPILL = sk.cells(24, 18, 24, 19)
pin: dict = {}
for (x, y) in SPILL:
    wall[y * W + x] = 0
wk.chute(m, pin, deco, W, SPILL, "down", fid="band_spill", berms=False, chevrons=0)
for (x, y) in SPILL:
    pin[(x, y)] = f"scree_v_{y % 2}"
for sp in m["spans"]:
    r = sp["rect"]
    for y in range(r["ty"], r["ty"] + r["h"]):
        for x in range(r["tx"], r["tx"] + r["w"]):
            ok = shaft[y * W + x] if sp["kind"] == "plank" else wall[y * W + x]
            assert ok, (sp["id"], x, y)

# ---- warps --------------------------------------------------------------------
m["warps"].append({"id": "to_mine", "at": {"tx": 4, "ty": 4}, "trigger": "step_on",
                   "to_map": "cinderhead_mine", "to": {"tx": 16, "ty": 4}, "facing": "down",
                   "transition": "fade"})
pt.cave_ladder(m, deco, W, kind="down", at=(26, 24), to_map="old_seams_ii", to=(5, 6))


def put(x, y, name):
    deco[y * W + x] = gid(name)


def sput(x, y, name):
    deco[y * W + x] = sk.S(name)


# ---- objects: the headframe home, timber props, the warm coal ------------------
sk.obj(m, "headframe", "old_seams_headframe", (3, 1), 3, 4, overhang=3, solid=False)
sk.obj(m, "tub_a", "traverse_ore_cart", (6, 3), 1, 1)
sk.obj(m, "props_a", "old_seams_timber_props", (21, 2), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "props_b", "old_seams_timber_props", (7, 2), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "crystal_a", "cinderhead_crystal_cluster", (24, 5), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "vein_a", "old_seams_cinder_vein", (2, 5), 2, 2, solid=False)
sk.obj(m, "props_c", "old_seams_timber_props", (24, 10), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "vein_b", "old_seams_cinder_vein", (22, 15), 2, 2, solid=False)
sk.obj(m, "cart_b", "cinderhead_ore_cart", (26, 15), 2, 2, overhang=0)
sk.obj(m, "lamp_b", "hoard_lamp_unlit", (2, 10), 1, 3, overhang=2, walk_under=True)
sk.obj(m, "crystal_b", "cinderhead_crystal_cluster", (9, 10), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "props_d", "old_seams_timber_props", (5, 20), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "vein_c", "old_seams_cinder_vein", (22, 24), 2, 2, solid=False)
sk.obj(m, "props_e", "old_seams_timber_props", (21, 20), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "crystal_c", "cinderhead_crystal_cluster", (27, 21), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "lamp_c", "hoard_lamp_unlit", (24, 25), 1, 3, overhang=2, walk_under=True)

# the boulder wall on bench B: the pocket turns you DOWN before the west ladder
for y in range(10, 16):
    put(8, y, "boulder")
for (x, y) in [(4, 12), (25, 3), (20, 6), (6, 24), (27, 13)]:
    put(x, y, "boulder")
# light: sparse glowshrooms + cinder veins (this floor is dark)
for (x, y, n) in [(9, 4, "glowshroom_a"), (20, 4, "glowshroom_b"), (21, 11, "glowshroom_a"),
                  (10, 16, "glowshroom_b"), (2, 21, "glowshroom_a"), (19, 25, "glowshroom_b")]:
    put(x, y, n)
for (x, y, n) in [(5, 6, "vein_a"), (23, 7, "vein_b"), (27, 11, "vein_a"), (4, 15, "vein_b"),
                  (6, 22, "vein_a"), (15, 27, "vein_b"), (25, 22, "vein_a")]:
    sput(x, y, n)
for (x, y) in [(8, 6), (22, 3), (26, 6), (23, 13), (2, 13), (10, 13), (3, 23), (21, 26),
               (11, 27), (27, 26)]:
    put(x, y, "g_pebble")

# ---- trainer, caches, sign ------------------------------------------------------
owed += pt.trainer_beat(m, tid="seams_miner_kester", at=(5, 13), facing="down", sight=3,
                        sprite="miner_man")
owed += pt.cache(m, cid="seams_islet", at=(16, 11))
owed += pt.cache(m, cid="seams_bench_balm", at=(2, 25))
owed += pt.cache(m, cid="seams_bench_tin", at=(27, 4))       # pays the NE corner
owed += pt.sign(m, deco, W, sid="old_seams_i", at=(6, 6))

# ---- encounters (night + day) ---------------------------------------------------
# mirrored in build_species.py OLD_SEAMS_TABLES (keep the two in step)
NIGHT = sk.T((53, 30, 27, 29), (42, 25, 27, 28), (69, 20, 28, 29), (49, 15, 27, 29),
             (54, 10, 28, 29))
DAY = sk.T((53, 26, 55, 60), (42, 22, 56, 61), (69, 20, 57, 62), (49, 16, 55, 60),
           (54, 16, 58, 63))
sk.zone_pair(m, "bench_a", (19, 2, 28, 7), NIGHT, DAY)
sk.zone_pair(m, "bench_b_e", (20, 10, 28, 17), NIGHT, DAY)
sk.zone_pair(m, "bench_b_w", (1, 10, 11, 17), NIGHT, DAY)
sk.zone_pair(m, "bench_c_e", (19, 20, 28, 27), NIGHT, DAY)
sk.zone_pair(m, "bench_c_w", (1, 20, 8, 26), NIGHT, DAY)

sk.finish(m, W, H, wall=wall, shaft=shaft, deco=deco, above=above, rng=rng, floor_mix=0.5)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3, pin_base=pin)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
