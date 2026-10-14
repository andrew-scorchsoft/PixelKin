#!/usr/bin/env python3
"""
The Undertide II — the Kelp Vaults (10-the-farlamp-isles.md Part I; kind cave,
portal, lv 61-64, dark). Under the old keepers' quarter: it joins Gullwrack's
cave (the ladder up to the Undertide's mouth) to Kelpcrown's (the south stair),
so the isles have a way through underground.

  A  the LADDER VAULT (NW): up to the mouth. A race runs east to the bell vault.
  W  the KELP WALK (west): the through-route ON FOOT, A <-> K — a kelp forest
     with its pools (the floor's water beds). Nobody has to solve anything to
     pass through.
  K  the KELPCROWN STAIR (south): out to Kelpcrown Isle; a race north.
  J  the junction (18,9): bell still -> EAST to the bell vault; rung -> WEST,
     round the corner onto the island.
  E  the BELL VAULT (NE): the bell, a lamp-diver, the floor's LUMEN DROP.
  H  the HEART (island): the keeper's FOG-GLASS on its stand, her second
     logbook page. Seen from the stair long before you reach it.

  Returns: E races down the east side to K; H races west to the kelp walk.
  THE SOLUTION: ride north from K (or east from A) to E, ring the bell, ride
  home, ride north again — the junction now turns you onto the island.

HANDSHAKE: `ladder_up` (5,2) <-> undertide_i `ladder_down` (26,2);
`to_kelpcrown` (14,29) <-> farlamp_kelpcrown `to_undertide` (10,9) [lands (10,10)].

Run:  python3 tools/maps/build_undertide_ii.py
"""
from __future__ import annotations

import undertidekit as uk
from undertidekit import Floor

PLAN = [
    "##############################",
    "##......#~~~~~~~~~~~~~#.....##",
    "#........~~~~~~~~~~~~~.......#",
    "#........>>>>>>>>>>>>>.......#",
    "#........~~~~~~~~~~~~~..oo...#",
    "#........~~~~~~~~~~~~~.oooo..#",
    "#........~~~~~~~~~~~~~.......#",
    "#........~~~~~~~~~~~~~.......#",
    "#.....~~~~~~~~~~~,~~~~.......#",
    "##....~~~~~~~~~v<<J>>>.......#",
    "#.....~~~~.....<~~^~~~~~~~v~~#",
    "#.oo..~~~......~~~^~~~~~~~v~~#",
    "#oooo.~~~......~~~^~~~~~~~v~##",
    "#.ooo.<<<......~~~^~~~~~~~v~~#",
    "#.....~~~......~~~^~~~~~~~v~~#",
    "#.....~~~......~~~^~~~~~~~v~~#",
    "##....~~~~....~~~~^~~~~~~~v~~#",
    "#.....~~~~~~~~~~~~^~~~~~~~v~##",
    "#.ooo.~~~~~~~~~~~~^~~~~~~~v~~#",
    "#ooooo~~~~~~~~~~~~^~~~~~~~v~~#",
    "#ooooo~~~~~~~~~~~~^~~~~~~~v~~#",
    "#.ooo.~~~~~~~~~~~~^~~~~~~~v~~#",
    "#.....~~~~~~~~~~~~^~~~~~~~v~~#",
    "#........................<<~~#",
    "##.......................~~~~#",
    "#................oooo....#####",
    "#...............oooooo...#####",
    "##...............oooo....#####",
    "#######.................######",
    "##############.###############",
]

BELL = "flag:undertide_bell_vaults"

f = Floor("undertide_ii", "The Undertide: Kelp Vaults", PLAN, seed=17702)
f.junction((18, 9), "right", "left", BELL)
f.home = (14, 28)

# ---- warps --------------------------------------------------------------------
f.edge_warp("to_kelpcrown", (14, 29), "farlamp_kelpcrown", (10, 10), "down")
f.ladder("up", (5, 2), "undertide_i", (26, 2))

# ---- the heart: the fog-glass + page two --------------------------------------------
f.obj("fogglass", "undertide_fogglass", (11, 10), 1, 2, overhang=1, walk_under=True,
      hidden_when_flag="flag:q_isles_fogglass")
f.obj("fogglass_empty", "undertide_fogglass_empty", (11, 10), 1, 2, overhang=1,
      walk_under=True, requires_flag="flag:q_isles_fogglass")
f.m["triggers"].append({"id": "fogglass", "kind": "script", "at": {"tx": 11, "ty": 11},
                        "activation": "interact", "ref": "script.undertide_fogglass"})
f.owed.append("script.undertide_fogglass")
f.logbook(2, (13, 15))
f.obj("glass_h", "undertide_glassheap", (9, 14), 2, 1)
f.sign("undertide_vaults", (10, 24))
f.owed.append("sign.undertide_vaults")

# ---- the bell vault ----------------------------------------------------------------
f.bell(2, (23, 2), BELL, "script.undertide_bell_vaults")
f.post(2, (17, 8), BELL)
f.cache("undertide_ii_drop", (28, 2))
f.trainer("undertide_diver_corin", (25, 7), "left", 3, "fisher_man")
f.obj("pillar_e", "undertide_pillar", (27, 6), 2, 3, overhang=1)
f.owed.append("script.undertide_bell_vaults")

# ---- the kelp walk: a wading forest (fronds don't block) ---------------------------
for i, (x, y) in enumerate([(1, 9), (4, 10), (5, 14), (1, 15), (3, 16), (5, 17), (1, 22),
                            (4, 23), (2, 25), (5, 26), (3, 8), (7, 2)]):
    f.obj(f"kelp_{i}", "undertide_kelp", (x, y - 1), 1, 2, overhang=1, walk_under=True,
          solid=False)
for i, (x, y) in enumerate([(8, 25), (12, 27), (22, 26), (23, 24)]):
    f.obj(f"kelp_k{i}", "undertide_kelp", (x, y - 1), 1, 2, overhang=1, walk_under=True,
          solid=False)
f.obj("glass_a", "undertide_glassheap", (2, 5), 2, 1)

f.scatter(["barnacle_a", "barnacle_b", "shell_a", "wrack_a", "wrack_a"], 26)

# ---- beds (mirrored in build_species.py UNDERTIDE_TABLES — keep in step) ------
CAVE = [(174, 28, 61, 64), (176, 24, 62, 64), (52, 18, 62, 63), (85, 14, 62, 64),
        (175, 6, 63, 64), (138, 10, 62, 64)]
WATER = [(172, 32, 61, 63), (61, 22, 62, 64), (28, 20, 62, 64), (29, 16, 61, 63),
         (173, 6, 63, 64), (30, 4, 64, 64)]


def T(rows):
    return [{"kin_id": k, "weight": w, "min_level": lo, "max_level": hi} for (k, w, lo, hi) in rows]


f.zone("vaults_a", "cave", (1, 1, 8, 7), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("vaults_walk", "cave", (1, 8, 5, 22), T(CAVE), 0.08,
       day=T(uk.day_table(CAVE)))
f.zone("vaults_k", "cave", (1, 23, 24, 28), T(CAVE), 0.08,
       day=T(uk.day_table(CAVE)))
f.zone("vaults_e", "cave", (22, 1, 28, 9), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("vaults_h", "cave", (10, 10, 14, 16), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("vaults_pool_n", "water", (1, 11, 4, 13), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))
f.zone("vaults_pool_s", "water", (1, 18, 4, 21), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))
f.zone("vaults_pool_k", "water", (16, 25, 21, 27), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))
f.zone("vaults_pool_e", "water", (23, 4, 26, 5), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))


# ---- the proof --------------------------------------------------------------------
f.prove()
still, rung = {BELL: False}, {BELL: True}
heart, east = f.pocket_of((12, 12)), f.pocket_of((25, 3))
assert heart not in f.reach((14, 28), still) and east in f.reach((14, 28), still)
assert heart in f.reach((14, 28), rung)
assert f.pocket_of((5, 3)) == f.pocket_of((14, 28)), "the kelp walk must join ladder and stair"

# ---- pass 2: the surge dressed; the tide-lamps that light at the isles' dawn ----
f.dress_surge(per_screen=4)
f.tide_lamps(spacing=6)

f.finish()

if __name__ == "__main__":
    raise SystemExit(f.build())
