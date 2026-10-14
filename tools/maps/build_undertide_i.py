#!/usr/bin/env python3
"""
The Undertide I (10-the-farlamp-isles.md Part I; kind cave, portal, lv 61-63, dark).
Under Gullwrack Isle. The sea-cave's MOUTH and its lesson.

The cave opens on a great flooded basin of SURGE — white water churning over a
drop, never swum. Through it run the TIDE-RACES: calm lanes with a current you
can see (chevrons), which carry you (kind:'rail' flows) and never let you swim
back up them. One junction pool in the middle and ONE tide-bell on the landing
teach the whole Undertide:

  S  the LANDING (south): the way out to Gullwrack, the bell, a race north.
  J  the junction (15,11): bell still -> the race turns WEST; bell rung -> EAST.
  W  the WEST LEDGE: the keeper's first logbook page, a Hearth Coal, a pool.
  I  the BELL-RINGERS' ISLET (mid-basin): seen from the landing at once; its race
     off the west return only wakes once the Bell Galleries are tuned (III) —
     a Starglass Shard for coming back.
  NE the LADDER LEDGE: a lamp-diver, the ladder down to the Kelp Vaults.
  Both ledges race home to the landing (unswitched returns), so nothing strands.

HANDSHAKE: `to_gullwrack` (15,27) <-> farlamp_gullwrack `to_undertide` (13,9)
[lands (13,10)]; `ladder_down` (26,2) <-> undertide_ii `ladder_up` (5,2).

Run:  python3 tools/maps/build_undertide_i.py
"""
from __future__ import annotations

import undertidekit as uk
from undertidekit import Floor

PLAN = [
    "##############################",
    "####################.......###",
    "###.....###########.........##",
    "##.......##########..ooo.....#",
    "##.......##########..ooo.....#",
    "#..ooo...##########..........#",
    "#.ooooo..##########..........#",
    "#..oooo..##########.........##",
    "#...oo...~~~~~~~~~~~~^~~~v~~##",
    "#........~~~~~~~~~~~~^~~~v~~~#",
    "#~.......~~~~~,~~~~~~^~~~v~~~#",
    "#~.......<<<<<<J>>>>>^~~~v~~~#",
    "#~~~v~~~~~~~~~~^~~~~~~~~~v~~~#",
    "#~~~v~~~~~~~~~~^~~~~~~~~~v~~~#",
    "#~~,v~~~~,,~~~~^~~~~~,,~~v~~~#",
    "#~~~J>>>>,,~~~~^~~~~~,,~~v~~~#",
    "#~~~v~~~~v~~~~~^~~~~~~~~~v~~~#",
    "#~~~v~~~~v~~~~~^~~~~~~~~~v~~~#",
    "#~~~v~~~~v~~~~~^~~~~~~~~~v~~~#",
    "##~~v~~~~v~~~~~^~~~~~~~~~v~~##",
    "###~v~~~~.............~~~v~###",
    "###~>>>>>.............<<<<~###",
    "###~~~~~...............~~~~###",
    "########..........ooo..#######",
    "########..........ooo..#######",
    "########..........ooo..#######",
    "#########.............########",
    "###############.##############",
]

BELL = "flag:undertide_bell_mouth"

f = Floor("undertide_i", "The Undertide", PLAN, seed=17701)
f.junction((15, 11), "left", "right", BELL)
# the islet race: wakes only when the Bell Galleries ring true (a come-back)
f.junction((4, 15), "down", "right", "flag:q_isles_bells_tuned")
f.home = (15, 26)

# ---- warps --------------------------------------------------------------------
f.edge_warp("to_gullwrack", (15, 27), "farlamp_gullwrack", (13, 10), "down")
f.ladder("down", (26, 2), "undertide_ii", (5, 2))

# ---- the bell, its post, the board --------------------------------------------
f.bell(1, (11, 20), BELL, "script.undertide_bell_mouth")
f.post(1, (14, 10), BELL)
f.sign("undertide_mouth", (17, 21))
f.owed += ["script.undertide_bell_mouth", "sign.undertide_mouth"]

# ---- the west ledge: page one, a coal, the shallows -------------------------------
f.logbook(1, (3, 3))
f.cache("undertide_i_coal", (1, 6))
f.obj("kelp_w1", "undertide_kelp", (7, 3), 1, 2, overhang=1, walk_under=True)
f.obj("kelp_w2", "undertide_kelp", (2, 9), 1, 2, overhang=1, walk_under=True)

# ---- the ladder ledge -----------------------------------------------------------
f.trainer("undertide_diver_ness", (24, 5), "left", 3, "fisher_woman")
f.obj("glass_ne", "undertide_glassheap", (19, 2), 2, 1)
f.obj("kelp_ne", "undertide_kelp", (28, 4), 1, 2, overhang=1, walk_under=True)

# the bell-ringers' islet (seen from the first visit; reached after Tide-bell Tuning)
f.cache("undertide_i_islet", (10, 14))
f.obj("kelp_islet", "undertide_kelp", (9, 13), 1, 2, overhang=1, walk_under=True, solid=False)
f.post(2, (3, 14), "flag:q_isles_bells_tuned")
f.obj("pillar_e", "undertide_pillar", (21, 13), 2, 3, overhang=1)

# ---- the landing ----------------------------------------------------------------
f.obj("kelp_s1", "undertide_kelp", (9, 23), 1, 2, overhang=1, walk_under=True)
f.obj("kelp_s2", "undertide_kelp", (21, 22), 1, 2, overhang=1, walk_under=True)

f.scatter(["barnacle_a", "barnacle_b", "shell_a", "wrack_a", "glass_a"], 22)

# the shallows rounded off (no box pools): corners off, a bulge per long side
f.organic_pools()

# ---- beds (mirrored in build_species.py UNDERTIDE_TABLES — keep in step) ------
CAVE = [(174, 30, 61, 63), (176, 26, 61, 63), (52, 20, 62, 63), (85, 14, 62, 63),
        (55, 10, 62, 63)]
WATER = [(172, 34, 61, 63), (29, 24, 61, 62), (28, 20, 62, 63), (61, 14, 62, 63),
         (30, 8, 63, 63)]


def T(rows):
    return [{"kin_id": k, "weight": w, "min_level": lo, "max_level": hi} for (k, w, lo, hi) in rows]


f.zone("mouth_landing", "cave", (9, 20, 21, 26), T(CAVE), 0.08,
       day=T(uk.day_table(CAVE)))
f.zone("mouth_west", "cave", (1, 2, 8, 11), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("mouth_ne", "cave", (19, 1, 28, 7), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("mouth_pools_w", "water", (2, 5, 6, 8), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))
f.zone("mouth_pools_ne", "water", (21, 3, 23, 4), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))
f.zone("mouth_pools_s", "water", (18, 23, 20, 25), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))


# ---- the proof --------------------------------------------------------------------
f.prove()
st0 = {BELL: False, "flag:q_isles_bells_tuned": False}
st1 = {BELL: True, "flag:q_isles_bells_tuned": False}
west, ne = f.pocket_of((4, 6)), f.pocket_of((24, 3))
assert west in f.reach((15, 26), st0) and ne not in f.reach((15, 26), st0)
assert ne in f.reach((15, 26), st1)
TUNED = "flag:q_isles_bells_tuned"
islet = f.pocket_of((9, 15))
assert islet not in f.reach((15, 26), {BELL: False, TUNED: False})
assert islet in f.reach((15, 26), {BELL: False, TUNED: True})

# ---- pass 2: the surge dressed; the tide-lamps that light at the isles' dawn ----
f.dress_surge(per_screen=4, palette="mouth")
f.tide_lamps(spacing=6)

f.finish()

if __name__ == "__main__":
    raise SystemExit(f.build())
