#!/usr/bin/env python3
"""
The Wayward Arms (wayward_arms) — the ground-floor bar of the old country
hotel on Wayward Rise, north of the Wanderwood (2026-10). Warm register,
roomkit composition (docs/world/interiors.md, binding):

  * THE BAR (main room, west): the focal point at top-centre is the BACK-BAR
    (`bar_back`, wall-mounted, 4x3) — three shelves of bottles, the TOP shelf
    keeping the good ones (the bourbon stands proud in the middle, col 9) — with
    the long `bar_counter` (6x2) in front of it and a one-tile service aisle
    between them, open at the counter's EAST end (12, 4) so a guest can step
    behind. Nobody keeps it tonight: a card on the counter says HELP YOURSELVES.
    The stair to the rooms (`stair_up`, wall-mounted) climbs into the west wall
    (sign.wayward_stairs — every door upstairs shut and quiet); a long table and
    a round one with stools, a lamp rack, a rug at the door.
  * THE SNUG (east, behind the partition at col 13, open at its south end): the
    hearth (its minor anchor) and two wing-back armchairs against the wall — the
    green one (17) and, in the CORNER, the wine-red one (18). Both are raw-placed
    at the face row, NON-solid, so the seat tiles (17, 2) and (18, 2) can be sat in.
    The STRANGER stands at (17, 3), beside the corner chair, a well-dressed man
    (`npc_man`). He is never named, and the scene never says who he is.

The scene (script.wayward_stranger, content/regions/hotel.ts): ask him, or try
the corner chair (an interact trigger on its seat) -> sit with him? -> he says
the bar's open ("We've been told we can help ourselves.") -> you walk round
the bar's east end to (9, 4) under the top shelf, take down the bourbon, walk
back to the corner chair -> the night talked away -> `heal` (a REST: it sleeps,
heals, and banks this room as a rest point) -> morning, of a kind. The scene's
walking is single-axis `move` legs over these tiles:
    (18,3) -> (18,8) -> (12,8) -> (12,4) -> (9,4)  and back the same way to (18,2).
Keep them floor (audit_flow proves reach; the shoot proves the walk).

Door: doormat (10, 12) -> wayward_rise (11, 9) (the door's apron);
the rise's door warps (11-12, 8) land here on (10, 11).

Run:  python3 tools/maps/build_wayward_arms.py
"""
from __future__ import annotations

import roomkit as rk
from roomkit import (WARM_SET, faced_room, windows, partition_v, place, wall_mount,
                     mapdef, obj, finish)

W, H = 20, 13
DOOR_X = 10


def build() -> dict:
    base, over = faced_room(W, H, DOOR_X)
    windows(over, W, [6, 12])
    # the snug: a full-height partition at col 13, lip facing the bar, open
    # below row 7 so the snug is an alcove off the bar's south end
    partition_v(over, W, 13, 1, 7, lip="w")

    objects: list = []
    # --- the bar (focal point, top-centre of the main room)
    wall_mount(objects, "bar_back", 7)                 # cols 7-10, rows 1-3
    place(objects, "bar_counter", 6, 5)                # cols 6-11, rows 5-6
    wall_mount(objects, "stair_up", 1)                 # cols 1-2 — up to the rooms
    wall_mount(objects, "lamp_rack", 4, solid=False)
    place(objects, "stool", 7, 7, oid="bar_stool_a")
    place(objects, "stool", 9, 7, oid="bar_stool_b")
    place(objects, "stool", 11, 7, oid="bar_stool_c")
    # tables: the long board by the stair, a round corner table, stools pulled up
    place(objects, "table_long", 1, 5)
    place(objects, "stool", 1, 7, oid="stool_long_a")
    place(objects, "stool", 3, 7, oid="stool_long_b")
    place(objects, "table", 2, 9, oid="table_round")
    place(objects, "stool", 1, 10, oid="stool_round_a")
    place(objects, "stool", 4, 10, oid="stool_round_b")
    place(objects, "barrels", 4, 4)
    place(objects, "plant", 12, 11, oid="plant_door")
    place(objects, "rug", 9, 9, solid=False)
    # --- the snug: hearth + the two armchairs (seats open), a rug before the fire
    wall_mount(objects, "hearth", 14)                  # cols 14-16, rows 1-3
    objects.append(obj("chair_stranger", "interior_armchair_green", 17, 1, 1, 2,
                       solid=False))
    objects.append(obj("chair_corner", "interior_armchair", 18, 1, 1, 2, solid=False))
    place(objects, "rug", 14, 5, oid="rug_snug", solid=False)
    place(objects, "table", 15, 9, oid="table_snug")
    place(objects, "stool", 14, 10, oid="stool_snug")
    place(objects, "stool", 17, 10, oid="stool_snug_b")
    place(objects, "plant", 18, 11, oid="plant_snug")

    warps = [
        {"id": "to_rise", "at": {"tx": DOOR_X, "ty": H - 1}, "trigger": "step_on",
         "to_map": "wayward_rise", "to": {"tx": 11, "ty": 9}, "facing": "down",
         "transition": "door"},
    ]
    triggers = [
        # the corner chair: Confirm on it (either tile) offers the seat — the same
        # scene as talking to the stranger beside it
        {"id": "corner_chair", "kind": "cutscene", "at": {"tx": 18, "ty": 2},
         "activation": "interact", "ref": "script.wayward_stranger"},
        # the card on the bar (its front row, both halves of the counter's middle)
        {"id": "bar_card_8", "kind": "sign", "at": {"tx": 8, "ty": 6},
         "activation": "interact", "ref": "sign.wayward_bar"},
        {"id": "bar_card_10", "kind": "sign", "at": {"tx": 10, "ty": 6},
         "activation": "interact", "ref": "sign.wayward_bar"},
        # the top shelf itself, from behind the bar
        {"id": "top_shelf", "kind": "sign", "at": {"tx": 9, "ty": 3},
         "activation": "interact", "ref": "sign.wayward_top_shelf"},
        # the stair to the rooms
        {"id": "stairs", "kind": "sign", "at": {"tx": 1, "ty": 3},
         "activation": "interact", "ref": "sign.wayward_stairs"},
        # the guest-book left open on the snug's table
        {"id": "guest_book", "kind": "sign", "at": {"tx": 15, "ty": 9},
         "activation": "interact", "ref": "sign.wayward_guestbook"},
    ]
    npcs = [
        {"id": "stranger", "at": {"tx": 17, "ty": 3}, "facing": "down",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "script.wayward_stranger"},
    ]
    return mapdef("wayward_arms", "The Wayward Arms", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/inn-rest.mp3")


if __name__ == "__main__":
    ok = finish(build())
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
