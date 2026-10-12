#!/usr/bin/env python3
"""
The Old Seams II — the Rail Yard (09-the-wild-ways §2 D; kind cave, region
east, band 29-31, dark). The floor's one real PUZZLE.

The old crew sorted coal here: four platforms round a great sunk working (a
chasm, the seams_set `shaft`), joined by ORE-CART RAILS laid along rock ribs
across it. Step onto a rail and it carries you (kind:'rail' flows: no steering,
never back up a line). Three JUNCTIONS are thrown by three LEVERS; a point-stand
beside each shows its setting (white = straight, red = turnout).

  A  the LEVER GALLERY (NW): the ladder up, levers 1 and 2, the yard-board.
  B  the EAST STAGE (NE): a sorter's stage — a cache, a seam-miner.
  D  the SOUTH-WEST SIDING (SW): a dead end with lever 3 and the valuable.
  C  the FAR PLATFORM (SE): the ladder down. Visible from A across the dark.

  A --right--> J1 (16,5)   lever 1 off: straight on to B
                           lever 1 on : turn down to J2
  J2 (16,12)               lever 2 off: straight down to J3
                           lever 2 on : turn east, up to B
  J3 (16,18)               lever 3 off: straight down, west to D
                           lever 3 on : turn east, down to C
  returns:  B -> A (row 3), D -> A (col 3), C -> B (col 28)

THE SOLUTION (lever 3 lives on D, which is only reached THROUGH the yard):
throw lever 1, ride to D (J2, J3 straight), throw lever 3, ride the return to
A, ride again — J3 now turns you to C. NO SOFTLOCK: every line ends on a
platform under every lever setting, and every platform has a return line that
ends at A (C via B), so the levers are always one ride away. (Verified in the
builder below by walking every lever state.)

HANDSHAKE: `ladder_up` (5,6) <-> old_seams_i's `ladder_down` (26,24);
`ladder_down` (27,27) <-> old_seams_iii's `ladder_up` (24,3).

Run:  python3 tools/maps/build_old_seams_ii.py
"""
from __future__ import annotations

import random
from collections import deque

import mapkit as mk
import patterns as pt
import seamskit as sk
import wildkit as wk
from mapkit import gid

W, H = 32, 32
rng = random.Random(16602)
owed: list[str] = []

wall = sk.grid(W, H)
shaft = sk.grid(W, H)
deco = sk.grid(W, H)
above = sk.grid(W, H)
sk.fill(wall, W, 0, 0, W - 1, H - 1)

A = sk.cells(2, 2, 8, 9) - {(2, 9), (8, 9), (2, 2)}
B = sk.cells(24, 2, 29, 8) - {(29, 8), (24, 8)}
D = sk.cells(2, 20, 8, 27) - {(8, 20), (8, 27), (2, 20)}
C = sk.cells(23, 22, 29, 29) - {(23, 22), (23, 29), (29, 22)}
PLATFORMS = A | B | D | C

# the sunk working: everything inside the rim that isn't a platform is the pit
for (x, y) in sk.cells(2, 2, 29, 29):
    wall[y * W + x] = 0
    shaft[y * W + x] = 0 if (x, y) in PLATFORMS else 1
# rock pillars rising out of the dark (cavewall islands — never walkable)
for (x, y) in (sk.cells(11, 14, 12, 15) | sk.cells(20, 21, 21, 22) | sk.cells(5, 13, 6, 14) |
               sk.cells(20, 8, 21, 9)):
    wall[y * W + x] = 1
    shaft[y * W + x] = 0
# the platforms' clipped corners: the pit bites in (the NW one is rim rock)
wall[2 * W + 2] = 1
shaft[2 * W + 2] = 0
# more pillars in the deep south of the working, so the dark has a far shore
for (x, y) in sk.cells(12, 27, 13, 28) | sk.cells(18, 25, 18, 26):
    wall[y * W + x] = 1
    shaft[y * W + x] = 0

m: dict = {
    "id": "old_seams_ii", "display_name": "The Old Seams: Rail Yard",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": sk.MUSIC, "battle_backdrops": list(sk.BACKDROPS),
}
wk.use_traverse(m)
sk.use_seams(m)

# ---- the rails: (cells, dir, art) runs; a rail rib is walkable rock -------------
L1, L2, L3 = "flag:seams_lever_1", "flag:seams_lever_2", "flag:seams_lever_3"
RAILS: list[tuple[str, list[tuple[int, int]], str, dict]] = []


def run(fid, cells, d, flags=None):
    RAILS.append((fid, cells, d, flags or {}))


def h(x0, x1, y):
    return [(x, y) for x in range(min(x0, x1), max(x0, x1) + 1)]


def v(x, y0, y1):
    return [(x, y) for y in range(min(y0, y1), max(y0, y1) + 1)]


run("out_a", h(9, 15, 5), "right")
run("j1_b", h(17, 23, 5), "right")
run("j1_down", v(16, 6, 11), "down")
run("j2_mid", v(16, 13, 17), "down")
run("j2_east", h(17, 26, 12), "right")
run("j2_rise", [(27, 12)] + v(27, 9, 11), "up")
run("j3_down", v(16, 19, 23), "down")
run("j3_west", [(16, 24)] + h(9, 15, 24), "left")
run("j3_east", h(17, 24, 18), "right")
run("j3_drop", [(25, 18)] + v(25, 19, 21), "down")
run("ret_b", h(9, 23, 3), "left")
run("ret_d", v(3, 10, 19), "up")
run("ret_c", v(28, 9, 21), "up")
# the junctions: the straight flow hides when its lever is thrown, the turnout
# appears (listed last, so it wins in Traversal.flowAt)
run("j1_straight", [(16, 5)], "right", {"hidden_when_flag": L1})
run("j1_turn", [(16, 5)], "down", {"requires_flag": L1})
run("j2_straight", [(16, 12)], "down", {"hidden_when_flag": L2})
run("j2_turn", [(16, 12)], "right", {"requires_flag": L2})
run("j3_straight", [(16, 18)], "down", {"hidden_when_flag": L3})
run("j3_turn", [(16, 18)], "right", {"requires_flag": L3})
for fid, cs, d, fl in RAILS:
    for (x, y) in cs:
        shaft[y * W + x] = 0
        wall[y * W + x] = 0
    wk.rail_flow(m, cs, d, fid=fid, flags=fl)

ART = {}
for fid in ("out_a", "j1_b", "j2_east", "j3_east", "ret_b"):
    for c in next(r[1] for r in RAILS if r[0] == fid):
        ART[c] = "srail_h"
for (x, y) in h(9, 15, 24):
    ART[(x, y)] = "srail_h"
for fid in ("j1_down", "j2_mid", "j3_down", "ret_d", "ret_c"):
    for c in next(r[1] for r in RAILS if r[0] == fid):
        ART[c] = "srail_v"
for c in v(27, 9, 11) + v(25, 19, 21):
    ART[c] = "srail_v"
ART.update({(16, 5): "srail_tee_h_sw", (16, 12): "srail_tee_v_ne", (16, 18): "srail_tee_v_ne",
            (16, 24): "srail_nw", (27, 12): "srail_nw", (25, 18): "srail_sw",
            # buffer stops on the platforms' landing tiles
            (24, 5): "srail_end_e", (27, 8): "srail_end_n", (28, 8): "srail_end_n",
            (8, 24): "srail_end_w", (25, 22): "srail_end_s", (8, 3): "srail_end_w",
            (3, 9): "srail_end_n"})
for (x, y), name in ART.items():
    deco[y * W + x] = sk.S(name)

# ---- no-softlock proof: every lever state, every platform returns to A --------
RAIL_AT: dict = {}
for fid, cs, d, fl in RAILS:
    for c in cs:
        RAIL_AT.setdefault(c, []).append((d, fl))
STEP = {"right": (1, 0), "left": (-1, 0), "down": (0, 1), "up": (0, -1)}


def flow_dir(c, state):
    for d, fl in reversed(RAIL_AT.get(c, [])):
        if "requires_flag" in fl and not state[fl["requires_flag"]]:
            continue
        if "hidden_when_flag" in fl and state[fl["hidden_when_flag"]]:
            continue
        return d
    return None


def ride(start, state):
    c, seen = start, set()
    while (d := flow_dir(c, state)) is not None:
        assert c not in seen, ("rail loop", c)
        seen.add(c)
        c = (c[0] + STEP[d][0], c[1] + STEP[d][1])
    assert c in PLATFORMS, ("rail dead-stops off a platform", start, state, c)
    return c


def which(c):
    return next(n for n, p in (("A", A), ("B", B), ("C", C), ("D", D)) if c in p)


DEPART = {"A": [(9, 5)], "B": [(23, 3)], "D": [(3, 19)], "C": [(28, 21)]}
for s in range(8):
    st = {L1: bool(s & 1), L2: bool(s & 2), L3: bool(s & 4)}
    for plat, starts in DEPART.items():
        for st_c in starts:
            ride(st_c, st)
    # from every platform you can reach A in this state
    for plat in "ABCD":
        seen, q = {plat}, deque([plat])
        while q:
            p = q.popleft()
            for st_c in DEPART[p]:
                n = which(ride(st_c, st))
                if n not in seen:
                    seen.add(n)
                    q.append(n)
        assert "A" in seen, ("softlock", plat, st)
# the solution exists and needs lever 3 (thrown only on D)
assert which(ride((9, 5), {L1: True, L2: False, L3: True})) == "C"
assert all(which(ride((9, 5), {L1: a, L2: b, L3: False})) != "C"
           for a in (False, True) for b in (False, True))

# ---- warps --------------------------------------------------------------------
pt.cave_ladder(m, deco, W, kind="up", at=(5, 6), to_map="old_seams_i", to=(26, 24))
pt.cave_ladder(m, deco, W, kind="down", at=(27, 27), to_map="old_seams_iii", to=(24, 3))

# ---- levers, point-stands, the yard-board -------------------------------------
sk.lever(m, 1, (5, 1))
sk.lever(m, 2, (7, 1))
sk.lever(m, 3, (2, 24))
sk.point_stand(m, 1, (15, 4))
sk.point_stand(m, 2, (15, 11))
sk.point_stand(m, 3, (15, 17))
for (x, y) in [(15, 4), (15, 11), (15, 17)]:      # the stands sit on rock nubs by the points
    shaft[y * W + x] = 0
owed += pt.sign(m, deco, W, sid="old_seams_yard", at=(3, 3))
owed += ["script.seams_lever_1", "script.seams_lever_2", "script.seams_lever_3"]


def put(x, y, name):
    deco[y * W + x] = gid(name)


def sput(x, y, name):
    deco[y * W + x] = sk.S(name)


# ---- the yard's furniture ---------------------------------------------------------
sk.obj(m, "tub_a", "traverse_ore_cart", (8, 6), 1, 1)
sk.obj(m, "tub_b", "traverse_ore_cart", (6, 8), 1, 1)
sk.obj(m, "props_a", "old_seams_timber_props", (2, 4), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "crystal_p1", "cinderhead_crystal_cluster", (11, 13), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "props_p2", "old_seams_timber_props", (20, 20), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "crystal_p3", "cinderhead_crystal_cluster", (5, 12), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "vein_p4", "old_seams_cinder_vein", (20, 8), 2, 2, solid=False)
sk.obj(m, "crystal_p5", "cinderhead_crystal_cluster", (12, 26), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "props_b", "old_seams_timber_props", (26, 2), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "cart_b", "cinderhead_ore_cart", (24, 6), 2, 2, overhang=0)
sk.obj(m, "lamp_d", "hoard_lamp_unlit", (7, 21), 1, 3, overhang=2, walk_under=True)
sk.obj(m, "vein_d", "old_seams_cinder_vein", (4, 22), 2, 2, solid=False)
sk.obj(m, "props_c", "old_seams_timber_props", (24, 23), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "crystal_c", "cinderhead_crystal_cluster", (28, 24), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "vein_c", "old_seams_cinder_vein", (24, 27), 2, 2, solid=False)

for (x, y, n) in [(7, 4, "glowshroom_a"), (29, 5, "glowshroom_b"), (3, 26, "glowshroom_a"),
                  (26, 29, "glowshroom_b")]:
    put(x, y, n)
for (x, y, n) in [(4, 7, "vein_b"), (26, 6, "vein_a"), (6, 26, "vein_b"), (27, 25, "vein_a")]:
    sput(x, y, n)
for (x, y) in [(6, 3), (25, 7), (5, 20), (29, 27), (24, 25)]:
    put(x, y, "g_pebble")

# ---- trainers, caches -------------------------------------------------------------
owed += pt.trainer_beat(m, tid="seams_miner_wenna", at=(6, 23), facing="down", sight=3,
                        sprite="miner_woman")
owed += pt.trainer_beat(m, tid="seams_miner_tam", at=(27, 4), facing="left", sight=2,
                        sprite="miner_man")
owed += pt.cache(m, cid="seams_siding", at=(2, 27))       # the valuable, at the dead end
owed += pt.cache(m, cid="seams_stage", at=(29, 3))        # a sorter's tin on the east stage

# mirrored in build_species.py OLD_SEAMS_TABLES (keep the two in step)
NIGHT = sk.T((54, 30, 29, 31), (69, 20, 29, 30), (45, 20, 29, 30), (43, 15, 29, 31),
             (52, 10, 30, 31), (55, 5, 31, 31))
DAY = sk.T((54, 26, 56, 61), (69, 20, 56, 60), (45, 18, 56, 60), (43, 16, 57, 62),
           (52, 12, 58, 63), (55, 8, 60, 65))
sk.zone_pair(m, "stage_b", (24, 2, 29, 8), NIGHT, DAY)
sk.zone_pair(m, "siding_d", (2, 20, 8, 27), NIGHT, DAY)
sk.zone_pair(m, "far_c", (23, 22, 29, 29), NIGHT, DAY)

sk.finish(m, W, H, wall=wall, shaft=shaft, deco=deco, above=above, rng=rng, floor_mix=0.45)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
