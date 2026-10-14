#!/usr/bin/env python3
"""
The Undertide IV — the Drowned Stair (10-the-farlamp-isles.md Part I; kind cave,
portal, lv 63-66, dark). The last descent: the old tower's stair, gone under.

No bells down here: the tide-races are the stair. They all run DOWN, terrace to
terrace, with side lanes peeling off into the nooks — choose your way down — and
one long UP-RACE along the east wall carries you from the bottom straight back to
the top (the floor's return compressor).

  T1  the STAIR-HEAD (top): the ladder up to the Bell Galleries.
  T2  the WEST LANDING: a Hearth Coal, a pool.     -> T3, or -> N1
  N1  the WEST NOOK: the keeper's wick-purse (2,000w).          -> T4
  T3  the EAST LANDING: a lamp-diver.               -> T4, or -> N2
  N2  the EAST NOOK: the floor's LUMEN DROP.                    -> T5
  T4  the LOWER LANDING: the keeper's fourth page, a pool.      -> T5
  T5  the STAIR-FOOT: the keeper's dry NICHE (the floor's REST POINT, a bed before
      the Drowned Lamp), the way down to it, and the up-race home.
  After the isles' dawn: the T2 race calls in at the DAWN ISLET (cache) on its way
  to T3, and Ondine the diver waits at the stair-head for a re-runnable bout.

HANDSHAKE: `ladder_up` (12,2) <-> undertide_iii `ladder_down` (24,2);
`ladder_down` (16,28) <-> farlamp_drowned `ladder_up` (10,1).

Run:  python3 tools/maps/build_undertide_iv.py
"""
from __future__ import annotations

import undertidekit as uk
from undertidekit import Floor

PLAN = [
    "##########################",
    "###~~~~~~........~~~~~~###",
    "##~~~~~~..........~~~~~~##",
    "#~~v<<<<..........<<<<<<<#",
    "#~~v~~~~..........~~~~~~^#",
    "#~~v~~~~..........~~~~~~^#",
    "#~~v~~~~~~~~~~~~~~~~~~~~^#",
    "#~~v~~~~~~~~~~~~~~~~~~~~^#",
    "#~.......~~~~~~~~~~~~~~~^#",
    "#........~~~~~~~~~~~~~~~^#",
    "#..ooo...>>J>>>>v~~~~~~~^#",
    "#.oooo...~~v~~~~v~~~~~~~^#",
    "#.......~~~v~~~~v~~~~~~~^#",
    "#~v~~~~~~~~v~~~.......~~^#",
    "#~v~~~~~~~~v~~~........~^#",
    "#~v~~~~~~~,,~~~...ooo..~^#",
    "#~v~~~~~~~,,>>>..oooo..~^#",
    "#.....~~~~~~~~~~.......~^#",
    "#.....~~~~~~~~~~v~~~v~~~^#",
    "#.....~~~~~~~~~~v~~~v~~~^#",
    "#.....>........~v~~~v~~~^#",
    "#~....~........~v~....~~^#",
    "#~~~~~~..ooo...<<~.....~^#",
    "#~~~~~~..oooo..~~~.....~^#",
    "#~~~~~~~......~~~~~....~^#",
    "#~~~~~~~~~v~~~~~~~~~v~~~^#",
    "#~~~~~~~................^#",
    "##~~~~~~................^#",
    "###~~~~~#..............#~#",
    "##########################",
]

f = Floor("undertide_iv", "The Undertide: the Drowned Stair", PLAN, seed=17704)
f.home = (12, 3)
# the dawn islet: once the Farlamp burns, the T2 -> T3 race calls in at an islet
f.junction((11, 10), "right", "down", "flag:isles_dawn")

# ---- warps --------------------------------------------------------------------
f.ladder("up", (12, 2), "undertide_iii", (24, 2))
f.ladder("down", (16, 28), "farlamp_drowned", (10, 1))
f.sign("undertide_stair", (14, 27))
f.owed.append("sign.undertide_stair")

# ---- the landings ----------------------------------------------------------------
f.obj("pillar_t1", "undertide_pillar", (15, 1), 2, 3, overhang=1)
f.obj("glass_t1", "undertide_glassheap", (9, 4), 2, 1)
f.cache("undertide_iv_coal", (1, 9))                      # T2
f.obj("kelp_t2", "undertide_kelp", (7, 8), 1, 2, overhang=1, walk_under=True, solid=False)
f.cache("undertide_purse", (1, 18))                       # N1: the keeper's purse
f.obj("kelp_n1", "undertide_kelp", (4, 17), 1, 2, overhang=1, walk_under=True, solid=False)
f.trainer("undertide_diver_marlo", (21, 14), "left", 3, "fisher_woman")   # T3
f.obj("glass_t3", "undertide_glassheap", (15, 15), 2, 1)
f.cache("undertide_iv_drop", (21, 23))                    # N2
f.obj("pillar_n2", "undertide_pillar", (18, 21), 2, 3, overhang=1)
f.logbook(4, (13, 20))                                    # T4
f.cache("undertide_iv_dawn", (10, 15))                    # the dawn islet
# the keeper's dry niche at the stair-foot: the REST POINT before the Drowned Lamp
f.obj("niche", "undertide_niche", (18, 26), 2, 2)
f.m["triggers"].append({"id": "keeper_niche", "kind": "script", "at": {"tx": 18, "ty": 27},
                        "activation": "interact", "ref": "script.undertide_niche_rest"})
f.owed.append("script.undertide_niche_rest")
# after the dawn: a diver who stays to race you (re-runnable bout, never a sight-line)
f.m["npcs"].append({"id": "undertide_diver_ondine", "at": {"tx": 14, "ty": 4}, "facing": "down",
                    "sprite": "fisher_woman", "movement": "static",
                    "dialogue_ref": "script.undertide_diver_ondine",
                    "requires_flag": "flag:isles_dawn"})
f.solid_extra.add((14, 4))
f.owed.append("script.undertide_diver_ondine")
f.obj("kelp_t4", "undertide_kelp", (7, 21), 1, 2, overhang=1, walk_under=True, solid=False)
f.obj("pillar_t5", "undertide_pillar", (8, 25), 2, 3, overhang=1)
f.obj("kelp_t5", "undertide_kelp", (21, 26), 1, 2, overhang=1, walk_under=True, solid=False)

f.scatter(["barnacle_a", "barnacle_b", "shell_a", "wrack_a", "glass_a", "glass_b"], 26)

# ---- beds (mirrored in build_species.py UNDERTIDE_TABLES — keep in step) ------
CAVE = [(176, 26, 63, 66), (174, 22, 63, 65), (175, 14, 64, 66), (138, 14, 64, 66),
        (85, 14, 63, 65), (55, 10, 64, 66)]
WATER = [(172, 26, 63, 65), (173, 18, 64, 66), (28, 18, 64, 66), (30, 14, 64, 66),
         (25, 14, 64, 66), (34, 4, 66, 66)]


def T(rows):
    return [{"kin_id": k, "weight": w, "min_level": lo, "max_level": hi} for (k, w, lo, hi) in rows]


f.zone("stair_t1", "cave", (9, 1, 16, 5), T(CAVE), 0.06)
f.zone("stair_t2", "cave", (1, 8, 7, 12), T(CAVE), 0.1)
f.zone("stair_n1", "cave", (1, 17, 5, 21), T(CAVE), 0.1)
f.zone("stair_t3", "cave", (15, 13, 22, 17), T(CAVE), 0.1)
f.zone("stair_n2", "cave", (18, 21, 22, 24), T(CAVE), 0.1)
f.zone("stair_t4", "cave", (7, 20, 14, 24), T(CAVE), 0.1)
f.zone("stair_t5", "cave", (8, 26, 23, 28), T(CAVE), 0.06)
f.zone("stair_pool_t2", "water", (2, 10, 5, 11), T(WATER), 0.12)
f.zone("stair_pool_t3", "water", (17, 15, 20, 16), T(WATER), 0.12)
f.zone("stair_pool_t4", "water", (9, 22, 12, 23), T(WATER), 0.12)


# ---- the proof --------------------------------------------------------------------
f.prove()
P = {k: f.pocket_of(c) for k, c in {"T1": (12, 3), "T2": (3, 9), "N1": (3, 19), "T3": (17, 14),
                                    "N2": (20, 22), "T4": (8, 21), "T5": (12, 27)}.items()}
D0, D1 = {"flag:isles_dawn": False}, {"flag:isles_dawn": True}
reach = f.reach((12, 3), D0)
assert all(p in reach for p in P.values()), "every landing and nook is on the way down"
assert P["T1"] in f.links(D0)[P["T5"]], "the up-race carries the stair-foot home in one ride"
islet = f.pocket_of((11, 16))
assert islet not in reach and islet in f.reach((12, 3), D1)
assert all(p in f.reach((12, 3), D1) for p in P.values())

# ---- pass 2: the surge dressed; the tide-lamps that light at the isles' dawn ----
f.dress_surge(per_screen=4)
f.tide_lamps(spacing=6)

f.finish()

if __name__ == "__main__":
    raise SystemExit(f.build())
