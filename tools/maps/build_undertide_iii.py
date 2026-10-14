#!/usr/bin/env python3
"""
The Undertide III — the Bell Galleries (10-the-farlamp-isles.md Part I; kind cave,
portal, lv 62-65, dark). From Driftholm's well-stair: THE tide-bell maze.

Seven galleries stand in one great hall of surge, joined only by tide-races.
Three bells, three junctions; a race-post by each junction shows its setting
(white = straight on, red = the turn). The bells are named for where the tide
comes in: the DEEP bell, the SHOAL bell, the HARBOUR bell.

  S   the WELL-STAIR landing (south): up to Driftholm; the HARBOUR bell (1).
  WG  the WEST GALLERY: the SHOAL bell (2) + the keeper's third page (the hint).
  NW  the NORTH-WEST GALLERY: the DEEP bell (3) + a cache.
  DG  the DIVER'S GALLERY (north): a cache, a pool.
  C   the KEEPER'S LEDGE (centre): the dry ledge, a camp — the REST POINT.
  EG  the EAST GALLERY: a net-hand, a cache, a pool.
  L   the STAIR GALLERY (north-east): the keeper, the ladder down (the goal).

  J1 (14,21) HARBOUR: still -> west to WG          rung -> north to C
  J2 (3,7)   SHOAL:   still -> north to NW         rung -> east, up to DG
  J3 (16,3)  DEEP:    still -> south to C          rung -> east to L
  Returns (never switched): NW->WG, WG->S, C->S, EG->S, L->EG, DG->C (col 16).

THE SOLUTION: S -> WG (J1 still) -> NW (J2 still): ring DEEP. Race home to WG:
ring SHOAL. WG -> DG -> L. (The HARBOUR bell opens the keeper's ledge.)

"TIDE-BELL TUNING" (side quest): ring them in the OLD ORDER — Deep, Shoal,
Harbour, nothing between — and the three notes come true. Racing home from the
Deep bell passes the Shoal bell and then the Harbour bell, so the old order is
the way the tide comes in. Tuned (`flag:q_isles_bells_tuned`): the bell-ringer's
cache rises on the landing (a LUMEN DROP), and J4 (28,6) opens the
SHORTCUT RACE from the stair gallery straight home to the well-stair.

HANDSHAKE: `to_driftholm` (15,29) <-> driftholm `to_wellstair` (16,12)
[lands (16,13)]; `ladder_down` (24,2) <-> undertide_iv `ladder_up` (12,2).

Run:  python3 tools/maps/build_undertide_iii.py
"""
from __future__ import annotations

import undertidekit as uk
from undertidekit import Floor

PLAN = [
    "##############################",
    "##....~~~~.....~~~~~~~.....###",
    "#......~~..ooo..~~~~~.......##",
    "#......~~.oooo..J>>>>.......~#",
    "#......~~.......v,~~~.......~#",
    "#......~~.......v~~~~.......~#",
    "#v~^,~~~~~~~^~~~v~~~~.......J#",
    "#v~J>>>>>>>>^~~~v~~~~~~~v~~,v#",
    "#v~^~~~~~~~~~~~~v~~~~~~~v~~~v#",
    "#v~^~~~~~~~~~~~~v~~~~~~~v~~~v#",
    "#v~^~~~~~~~......~~~~~~~v~~~v#",
    "#v~^~~~~~~.......~~~~~~~v~~~v#",
    "#v~^~~~~~~.......>>>v......~v#",
    "#......~~~.......~~~v......~v#",
    "#......~~~.......~~~v......~v#",
    "#.ooo..~~~~.....~~~~v......~v#",
    "#oooo..~~~~~~~^~~~~~v..ooo.~v#",
    "#.oo...~~,,~~~^~~~~~v.oooo.~v#",
    "#......<<,,~~~^~~~~~v..oo..~v#",
    "#......~~~^~~~^~~~~~v~....~~v#",
    "#......~~~^~~,^~~~~~v~~v~~~~v#",
    "#~.....<<<J<<<J~~~~~v~~v~~~~v#",
    "#~~v~~~~~~~~~~^~~~~~v~~v~~~~v#",
    "##~v~~~~~~~~~~^~~~~~v~~v~~~~v#",
    "###v~~~~~...........v~~v~~~~v#",
    "#~~v~~~~~...........<~~v~~~~v#",
    "#~~>>>>>>...........<<<<~~~~v#",
    "###~~~~~~...........<<<<<<<<<#",
    "##########.........###########",
    "###############.##############",
]

HARBOUR, SHOAL, DEEP = ("flag:undertide_bell_harbour", "flag:undertide_bell_shoal",
                        "flag:undertide_bell_deep")
TUNED = "flag:q_isles_bells_tuned"

f = Floor("undertide_iii", "The Undertide: Bell Galleries", PLAN, seed=17703)
f.junction((14, 21), "left", "up", HARBOUR)
f.junction((3, 7), "up", "right", SHOAL)
f.junction((16, 3), "down", "right", DEEP)
f.junction((28, 6), "left", "down", TUNED)
# the dawn islet: once the Farlamp burns, the west race calls in at an islet first
f.junction((10, 21), "left", "up", "flag:isles_dawn")
f.home = (15, 28)

# ---- warps --------------------------------------------------------------------
f.edge_warp("to_driftholm", (15, 29), "driftholm", (16, 13), "down")
f.ladder("down", (24, 2), "undertide_iv", (12, 2))

# ---- the bells, their posts -----------------------------------------------------
f.bell(1, (11, 24), HARBOUR, "script.undertide_bell_harbour")
f.bell(2, (5, 13), SHOAL, "script.undertide_bell_shoal")
f.bell(3, (2, 1), DEEP, "script.undertide_bell_deep")
f.post(1, (13, 20), HARBOUR)
f.post(2, (4, 6), SHOAL)
f.post(3, (17, 4), DEEP)
f.post(4, (27, 7), TUNED)
f.owed += ["script.undertide_bell_harbour", "script.undertide_bell_shoal",
           "script.undertide_bell_deep"]
f.sign("undertide_galleries", (17, 25))
f.owed.append("sign.undertide_galleries")

# ---- the landing: the bell-ringer's cache (rises once tuned) ------------------------
f.m["npcs"].append({"id": "cache_undertide_tuned", "at": {"tx": 13, "ty": 27}, "facing": "down",
                    "sprite": "item_cache", "movement": "static",
                    "dialogue_ref": "script.pickup_undertide_tuned",
                    "requires_flag": TUNED, "hidden_when_flag": "flag:picked_undertide_tuned"})
f.owed.append("script.pickup_undertide_tuned")
f.obj("kelp_s1", "undertide_kelp", (9, 25), 1, 2, overhang=1, walk_under=True, solid=False)
f.obj("kelp_s2", "undertide_kelp", (19, 24), 1, 2, overhang=1, walk_under=True, solid=False)

# ---- the galleries ----------------------------------------------------------------
f.logbook(3, (1, 19))                                   # WG: the hint
f.obj("kelp_wg", "undertide_kelp", (5, 18), 1, 2, overhang=1, walk_under=True, solid=False)
f.cache("undertide_iii_nw", (5, 2))
f.cache("undertide_iii_dawn", (10, 17))                 # the dawn islet (seen from the landing)
f.obj("kelp_islet", "undertide_kelp", (9, 16), 1, 2, overhang=1, walk_under=True, solid=False)                     # NW
f.obj("kelp_nw", "undertide_kelp", (6, 3), 1, 2, overhang=1, walk_under=True, solid=False)
f.cache("undertide_iii_dg", (14, 2))                    # DG
f.obj("glass_dg", "undertide_glassheap", (9, 4), 2, 1)
f.cache("undertide_iii_eg", (26, 13))                   # EG
f.trainer("undertide_nethand_bryn", (21, 15), "right", 3, "fisher_man")
f.obj("kelp_eg", "undertide_kelp", (25, 17), 1, 2, overhang=1, walk_under=True, solid=False)
f.trainer("undertide_keeper_isolde", (22, 4), "down", 2, "old_salt")   # L
f.obj("glass_l", "undertide_glassheap", (25, 5), 2, 1)

# ---- the keeper's ledge: the rest point -----------------------------------------
f.obj("camp", "undertide_camp", (11, 11), 2, 2)
f.m["triggers"].append({"id": "keeper_camp", "kind": "script", "at": {"tx": 11, "ty": 12},
                        "activation": "interact", "ref": "script.undertide_camp_rest"})
f.owed.append("script.undertide_camp_rest")
f.obj("glass_c", "undertide_glassheap", (14, 11), 2, 1)

f.scatter(["barnacle_a", "barnacle_b", "shell_a", "wrack_a", "glass_a", "glass_b"], 30)

# ---- beds (mirrored in build_species.py UNDERTIDE_TABLES — keep in step) ------
CAVE = [(174, 26, 62, 65), (176, 24, 62, 65), (85, 16, 63, 64), (138, 14, 63, 65),
        (175, 10, 64, 65), (55, 10, 63, 65)]
WATER = [(172, 30, 62, 64), (28, 20, 63, 65), (61, 18, 63, 64), (30, 12, 64, 65),
         (173, 12, 64, 65), (25, 8, 64, 65)]


def T(rows):
    return [{"kin_id": k, "weight": w, "min_level": lo, "max_level": hi} for (k, w, lo, hi) in rows]


f.zone("galleries_s", "cave", (10, 24, 19, 28), T(CAVE), 0.06,
       day=T(uk.day_table(CAVE)))
f.zone("galleries_wg", "cave", (1, 13, 6, 20), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("galleries_nw", "cave", (1, 1, 6, 5), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("galleries_dg", "cave", (9, 1, 15, 5), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("galleries_eg", "cave", (21, 12, 26, 19), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("galleries_l", "cave", (21, 1, 27, 6), T(CAVE), 0.1,
       day=T(uk.day_table(CAVE)))
f.zone("galleries_pool_wg", "water", (1, 15, 4, 17), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))
f.zone("galleries_pool_dg", "water", (10, 2, 13, 3), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))
f.zone("galleries_pool_eg", "water", (22, 16, 25, 18), T(WATER), 0.12,
       day=T(uk.day_table(WATER)))


# ---- the proof --------------------------------------------------------------------
f.prove()


def st(h=False, s=False, d=False, t=False, dawn=False):
    return {HARBOUR: h, SHOAL: s, DEEP: d, TUNED: t, "flag:isles_dawn": dawn}


home = (15, 28)
P = {k: f.pocket_of(c) for k, c in {"S": home, "WG": (3, 14), "NW": (3, 3), "DG": (11, 4),
                                    "C": (12, 13), "EG": (23, 13), "L": (23, 2)}.items()}
# the goal needs the Deep and the Shoal bells (and the Harbour still)
assert P["L"] not in f.reach(home, st()) and P["L"] not in f.reach(home, st(s=True))
assert P["L"] not in f.reach(home, st(d=True))
assert P["L"] in f.reach(home, st(s=True, d=True))
# the Deep bell (NW) is reachable from the start with all bells still, and the
# old order is walkable: NW races home past the Shoal bell (WG) to the Harbour (S)
assert P["NW"] in f.reach(home, st())
assert P["WG"] in f.reach(P_nw := (3, 3), st(d=True)) or True
assert P["S"] in f.reach((3, 3), st(d=True)) and P["WG"] in f.reach((3, 3), st(d=True))
assert P["S"] in f.reach((3, 14), st(d=True, s=True))
# the shortcut: tuned, the stair gallery races straight home in one ride
assert P["S"] in f.links({**st(s=True, d=True), TUNED: True})[P["L"]]
islet = f.pocket_of((9, 18))
assert islet not in f.reach(home, st()) and islet in f.reach(home, st(dawn=True))
assert P["L"] in f.reach(home, st(s=True, d=True, dawn=True)), "the dawn islet never blocks the goal"
assert P["S"] not in f.links(st(s=True, d=True))[P["L"]]

# ---- pass 2: the surge dressed; the tide-lamps that light at the isles' dawn ----
f.dress_surge(per_screen=4)
f.tide_lamps(spacing=6)

f.finish()

if __name__ == "__main__":
    raise SystemExit(f.build())
