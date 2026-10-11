#!/usr/bin/env python3
"""
The Wickstead Lamp-school (wickstead_school) — the schoolroom on Wickstead
Green (build_wickstead_green.py), on the roomkit (docs/world/interiors.md).

A 16x12 warm-register civic room, composed to the interior rules:
  * FOCAL POINT top-centre: the drawn CHALKBOARD (interiorforge `chalkboard`,
    wall-mounted flush over the face) — the type-wheel in chalk; read it.
  * PARTITION: the east HEARTH NOOK behind an internal wall (open to the south),
    with the fireplace, a rug and the Hearthkeeper; below it the sick-bay cot.
  * dressing: the school bookcase + a lamp rack flush on the north wall, two
    rows of pupils' desks (interiorforge `desk`), plants, windows on the face.

A teacher per desk/corner, each ONE mechanic (content/regions/school.ts):
  headmistress (types) at the board · catching (west wall) · statuses (by the
  partition) · kindling & bond (east of the desks) · the Hearthkeeper (the
  nook) · resting (the cot — she'll let you lie down: a real rest point).
Two pupils at their desks carry colour. Every lesson is re-askable.

Run:  ./venv/bin/python tools/maps/build_wickstead_school.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, faced_room, windows, partition_v, place, wall_mount,
                     aisle_runner, mapdef, finish)

W, H = 16, 12
DOOR_X = W // 2  # 8


def build():
    base, over = faced_room(W, H, DOOR_X)
    windows(over, W, [3, 8])
    # the hearth nook: an internal wall at x=11 (rows 1-6), open at its south end
    partition_v(over, W, 11, 1, 6, lip="w")

    objects: list = []
    # north wall, west to east: the school bookcase, the CHALKBOARD (focal), lamps
    wall_mount(objects, "bookcase", 1)
    wall_mount(objects, "chalkboard", 4)
    wall_mount(objects, "lamp_rack", 9, solid=False)
    # the nook: the fire the Hearth is named for, a rug, a stool
    wall_mount(objects, "hearth", 12)
    place(objects, "rug", 12, 4, solid=False)
    place(objects, "stool", 14, 5)
    # the sick-bay cot under the nook (Master Mallow's rest lesson)
    place(objects, "bed", 13, 8, oid="cot")
    # two rows of pupils' desks facing the board; the aisle runs up to the door
    for i, (x, y) in enumerate([(2, 5), (5, 5), (2, 8), (5, 8)]):
        place(objects, "desk", x, y, oid=f"desk_{i}")
    aisle_runner(objects, DOOR_X, 4, 9)
    place(objects, "plant", 10, 10, oid="plant_e")
    place(objects, "plant", 1, 10, oid="plant_w")
    place(objects, "crates", 3, 9)

    warps = [
        {"id": "to_green", "at": {"tx": DOOR_X, "ty": H - 1}, "trigger": "step_on",
         "to_map": "wickstead_green", "to": {"tx": 10, "ty": 7}, "facing": "down",
         "transition": "door"},
    ]
    # the chalkboard reads from any of its four floor tiles
    triggers = [
        {"id": f"chalkboard_{x}", "kind": "sign", "at": {"tx": x, "ty": 2},
         "activation": "interact", "ref": "sign.school_chalkboard"}
        for x in range(4, 8)
    ]
    triggers.append({"id": "bookcase", "kind": "sign", "at": {"tx": 1, "ty": 3},
                     "activation": "interact", "ref": "sign.school_bookcase"})
    npcs = [
        # TYPES — the headmistress at the board (also banks flag:school_visited)
        {"id": "teacher_types", "at": {"tx": 8, "ty": 3}, "facing": "down",
         "sprite": "star_watcher", "movement": "static", "dialogue_ref": "script.school_types"},
        # CATCHING & charges — west wall, between the desk rows
        {"id": "teacher_catching", "at": {"tx": 1, "ty": 7}, "facing": "right",
         "sprite": "npc_man", "movement": "static", "dialogue_ref": "script.school_catching"},
        # STATUSES — by the partition, under the lamps
        {"id": "teacher_status", "at": {"tx": 10, "ty": 4}, "facing": "left",
         "sprite": "npc_lampwarden", "movement": "static", "dialogue_ref": "script.school_status"},
        # KINDLING & BOND — east of the desks, by the plant
        {"id": "teacher_kindling", "at": {"tx": 10, "ty": 7}, "facing": "left",
         "sprite": "hollow_gardener", "movement": "static", "dialogue_ref": "script.school_kindling"},
        # THE HEARTH — the Hearthkeeper herself, by the nook's fire
        {"id": "hearthkeeper", "at": {"tx": 13, "ty": 5}, "facing": "down",
         "sprite": "npc_old_woman", "movement": "static", "dialogue_ref": "script.school_hearth"},
        # RESTING — by the sick-bay cot
        {"id": "teacher_rest", "at": {"tx": 12, "ty": 9}, "facing": "left",
         "sprite": "innkeeper", "movement": "static", "dialogue_ref": "script.school_rest"},
        # pupils at their desks (facing the board)
        {"id": "pupil_willa", "at": {"tx": 2, "ty": 6}, "facing": "up",
         "sprite": "npc_girl", "movement": "static", "dialogue_ref": "npc.school_pupil_willa"},
        {"id": "pupil_dob", "at": {"tx": 6, "ty": 9}, "facing": "up",
         "sprite": "npc_boy", "movement": "static", "dialogue_ref": "npc.school_pupil_dob"},
    ]
    return mapdef("wickstead_school", "Wickstead Lamp-school", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/interior-study.mp3")


if __name__ == "__main__":
    ok = finish(build())
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
