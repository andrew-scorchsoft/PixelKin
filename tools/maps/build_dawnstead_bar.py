#!/usr/bin/env python3
"""
The Bright Bubble (dawnstead_bar) — the little bar in Dawnstead's east cottage
(2026-11). Content: src/game/content/regions/paul.ts (`script.bubble_*`).

Paul's memory of the bubbles. Years back he'd go into a bar for the serial on a
Thursday and a glass of fizz from the tap, and the tap poured it over-bubbled:
big, bright bubbles, the best bit of the night. Then one day somebody FIXED the
tap. Perfect glass, polite little bubbles, and it was never the same.

Here, at the end of the whole journey, the Bright Bubble's old brass tap has
broken again since the dawn, and the keeper hasn't the heart to mend it. Order
a fizz (DUSK FIZZ, the dark one, or LIGHT FIZZ, the light one) and it comes up
in bubbles as big as marbles. Once you've walked the Wanderwood with him
(`flag:q_south_wander_done`) Paul is sitting in the snug; after your glass is
poured, he looks at it, and says "wait a minute..." Hidden content, like all of
Paul's: never in the changelog or the guide.

Roomkit composition (docs/world/interiors.md, binding):
  * THE BAR (west): the back-bar is the focal piece, top-left of centre, with the
    counter in front and a service aisle (row 4) open at its east end (8, 4).
    The keeper, ODELL, stands behind the counter at (4, 4); you talk to him
    ACROSS it (the counter is a DESK_SPRITE). The tap is (6, 3), read from the
    aisle.
  * THE SNUG (east), behind a partition at col 10 open below row 6: the hearth,
    a rug, a table, and Paul at (14, 6).

Door: doormat (8, 10) -> dawnstead (19, 8); the cottage door (19, 7) lands on (8, 9).

Run:  python3 tools/maps/build_dawnstead_bar.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, faced_room, finish, mapdef, partition_v, place,
                     wall_mount, windows)

W, H = 16, 11
DOOR_X = 8
TOWN_APPROACH = (19, 8)   # the tile below the cottage door on dawnstead


def build() -> dict:
    base, over = faced_room(W, H, DOOR_X)
    windows(over, W, [8, 14])
    # the snug: a partition at col 10, lip to the bar, open below row 6
    partition_v(over, W, 10, 1, 6, lip="w")

    objects: list = []
    # --- the bar
    wall_mount(objects, "bar_back", 3)                 # cols 3-6, rows 1-3
    place(objects, "bar_counter", 2, 5)                # cols 2-7, rows 5-6
    wall_mount(objects, "lamp_rack", 1, solid=False)   # cols 1-2
    place(objects, "stool", 3, 7, oid="bar_stool_a")
    place(objects, "stool", 6, 7, oid="bar_stool_b")
    place(objects, "table", 1, 8, oid="table_west")    # cols 1-2, rows 8-9
    place(objects, "stool", 3, 9, oid="stool_west")
    place(objects, "rug", 7, 8, oid="rug_door", solid=False)
    # --- the snug: hearth, rug, Paul's table
    wall_mount(objects, "hearth", 11)                  # cols 11-13, rows 1-3
    place(objects, "rug", 11, 4, oid="rug_snug", solid=False)
    place(objects, "table", 12, 6, oid="table_snug")   # cols 12-13, rows 6-7
    place(objects, "barrels", 12, 9, oid="barrels_snug")
    place(objects, "plant", 14, 9, oid="plant_snug")
    # a WANTED poster by the window (Odell hasn't seen him; the fella in the snug agrees)
    objects.append({"id": "wanted_poster", "sprite": "paul_wanted",
                    "at": {"tx": 9, "ty": 1}, "w": 1, "h": 1, "solid": False})

    warps = [
        {"id": "to_dawnstead", "at": {"tx": DOOR_X, "ty": H - 1}, "trigger": "step_on",
         "to_map": "dawnstead", "to": {"tx": TOWN_APPROACH[0], "ty": TOWN_APPROACH[1]},
         "facing": "down", "transition": "door"},
    ]
    triggers = [
        # first step inside: the welcome (a band across the doormat's inner row)
        *[{"id": f"welcome_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 9},
           "activation": "step_on", "ref": "script.bubble_welcome",
           "hidden_when_flag": "flag:bubble_seen"} for x in (DOOR_X - 1, DOOR_X, DOOR_X + 1)],
        # the old brass tap, read from behind the bar
        {"id": "tap", "kind": "sign", "at": {"tx": 6, "ty": 3},
         "activation": "interact", "ref": "sign.bubble_tap"},
        {"id": "wanted_poster", "kind": "sign", "at": {"tx": 9, "ty": 1},
         "activation": "interact", "ref": "sign.wanted_bubble"},
        # the chalkboard price list on the counter's front
        {"id": "board_5", "kind": "sign", "at": {"tx": 5, "ty": 6},
         "activation": "interact", "ref": "sign.bubble_board"},
    ]
    npcs = [
        {"id": "odell", "at": {"tx": 4, "ty": 4}, "facing": "down",
         "sprite": "innkeeper", "movement": "static",
         "dialogue_ref": "script.bubble_keeper"},
        # Paul, in the snug, once you've walked the old wood with him
        {"id": "paul_bubble", "at": {"tx": 14, "ty": 6}, "facing": "left",
         "sprite": "booji_paul", "movement": "static",
         "dialogue_ref": "script.bubble_paul",
         "requires_flag": "flag:q_south_wander_done"},
    ]
    return mapdef("dawnstead_bar", "The Bright Bubble", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/interior-sunny.mp3")


if __name__ == "__main__":
    ok = finish(build())
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
