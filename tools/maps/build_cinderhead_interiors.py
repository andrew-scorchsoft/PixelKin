#!/usr/bin/env python3
"""
Cinderhead Mine interior (docs/world/interiors.md, on roomkit):

  * cinderhead_lumenary — Otho Grist's Stone hall at the mine mouth: the cool
    stone register kept plain and load-bearing, the way the mine likes it. A
    vigil-lamp shrine on its dais top-centre (the lamp the whole town's waiting
    on), ore-barrels and a foreman's table west, a partitioned tool-store east,
    pews where the crew keep the Lamp-down vigil. Bond-test on the aisle, gated
    on the Descent Vigil (flag:q_east_vigil_lamp) with Otho's own "not yet"
    (npc.otho_not_ready). The Stone Gleam ceremony is the most MELANCHOLY swell
    of the eight (Arc E — lean on `silence` before the lift; gleam:stone, and
    the engine derives flag:crown_east, East's second quadrant).

Run:  ./venv/bin/python tools/maps/build_cinderhead_interiors.py
"""
from __future__ import annotations

from roomkit import (COOL_SET, BANNER, faced_room, windows, partition_v,
                     place, wall_mount, aisle_runner, mapdef, finish)


def build_lumenary():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    # a tool-store nook east (partition) + the foreman's corner west
    partition_v(over, W, 12, 1, 4, lip="w")
    windows(over, W, [6, 10], tile=BANNER)

    objects: list = []
    # the carpet aisle (drawn runner objects, not the ladder-like doormat tile)
    aisle_runner(objects, door_x, 5, H - 2)
    # the vigil-lamp shrine on its dais, top-centre; braziers burn low (the vigil)
    place(objects, "altar", door_x - 1, 2)
    place(objects, "brazier", 5, 3, oid="brazier_l")
    place(objects, "brazier", 11, 3, oid="brazier_r")
    # west: the foreman's corner — ore-barrels, a worked table, a stool
    place(objects, "barrels", 1, 3, oid="ore_a")
    place(objects, "table", 2, 7, oid="foreman_table")
    place(objects, "stool", 1, 8, oid="foreman_stool")
    wall_mount(objects, "lamp_rack", 4, solid=False)
    # east: the tool-store — barrels behind the partition
    place(objects, "barrels", 13, 7, oid="ore_b")
    place(objects, "barrels", 13, 9, oid="ore_c")
    # the crew's vigil pews flanking the aisle (where a grander hall puts pews)
    place(objects, "pew", 5, 8, oid="vigil_pew_l")
    place(objects, "pew", 10, 8, oid="vigil_pew_r")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "cinderhead_mine", "to": {"tx": 12, "ty": 9}, "facing": "down",
         "transition": "door"},
    ]
    triggers = [
        # the bond-test, on the aisle south of the dais — gated on the Descent
        # Vigil (the vigil-lamp carried up), blocked in Otho's own voice (§5)
        {"id": "lumenary_battle", "kind": "cutscene", "at": {"tx": door_x, "ty": 6},
         "activation": "step_on", "ref": "script.lumenary_cinderhead", "once": True,
         "requires_flag": "flag:q_east_vigil_lamp", "blocked_ref": "npc.otho_not_ready"},
    ]
    # Otho, four flag-disjoint stages at the dais (the standing giver-swap):
    # hook (the vigil-lamp errand) -> waiting -> ready (lamp up) -> after (Gleam).
    npcs = [
        {"id": "otho_quest", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "script.otho_quest",
         "hidden_when_flag": "flag:q_east_vigil"},
        {"id": "otho_waiting", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.otho_waiting",
         "requires_flag": "flag:q_east_vigil",
         "hidden_when_flag": "flag:q_east_vigil_lamp"},
        {"id": "otho", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.otho_ready",
         "requires_flag": "flag:q_east_vigil_lamp",
         "hidden_when_flag": "gleam:stone"},
        {"id": "otho_after", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.otho_after",
         "requires_flag": "gleam:stone"},
    ]
    return mapdef("cinderhead_lumenary", "Cinderhead Stone Lumenary", W, H, COOL_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/cinderhead-mine-b.mp3")


if __name__ == "__main__":
    ok = finish(build_lumenary())
    print("DONE" if ok else "DONE (with audit failures)")
