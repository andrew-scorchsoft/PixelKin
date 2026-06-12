#!/usr/bin/env python3
"""
Sunken Solarium interior (docs/world/interiors.md, on roomkit):

  * sunken_solarium_lumenary — Lucan's Solar hall: the ONE WARM Lumenary.
    Cool stone walls per the binding standard (a shrine, never a cabin),
    but the dressing is THEATRICAL GOLD — the Heliarium's tiring-house:
    warm banners on the face, the stage braziers burning indoors, the
    troupe's costume rack and prop crates in the west GREEN-ROOM partition
    (rooms within the room), the sun-ledger niche east. NO bond-test here:
    Lucan fights ON THE LIT STAGE outdoors (walkthrough 04-west beat 5);
    the hall is the troupe's home and the region's REST POINT — the matron's
    full rest-heal (script.solarium_rest, the standing kit; the Solarium is
    a ruin, not a town — no inn exists, the green-room is where the
    Last-Warm-Day pilgrims doss down). No shop either: the festival trades
    in bread and stories (the Pale Vault precedent; counters live at
    Galehigh behind and Nightreach ahead).

  * HUMOUR slot 3 (the cluster's last sanctioned wry line — the prompter):
    npc.solarium_prompter "Everyone's a critic. The dark heckled us for
    forty years, and tonight it's losing its seat."

Door pairing: town side `to_lumenary`/`to_lumenary_e` at (5,7)/(6,7) land
at our (8,11); our `to_town` at (8,11) lands at the hall's apron (5,8).

Run:  ./venv/bin/python tools/maps/build_solarium_interiors.py
"""
from __future__ import annotations

from roomkit import (COOL_SET, aisle_runner, faced_room, mapdef, finish,
                     partition_v, place, wall_mount)

OWED = [
    "script.solarium_rest (the matron's full rest-heal — ends in the heal op)",
    "npc.solarium_prompter (HUMOUR slot 3 — copy in the docstring)",
    "npc.solarium_hall_keeper (the sun-ledger keeper: the Heliarium's record "
    "of every Last-Warm-Day kept)",
    "npc.solarium_hall_festival (requires gleam:solar — the troupe toasts the "
    "relit constellation)",
]


def build_lumenary():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    # the GREEN-ROOM west + the sun-ledger niche east (rooms within the room)
    partition_v(over, W, 4, 1, 4, lip="e")
    partition_v(over, W, 12, 1, 4, lip="w")

    objects: list = []
    # the carpet aisle (drawn runner objects — NEVER the doormat tile)
    aisle_runner(objects, door_x, 5, H - 2)
    # THE SOLAR IDENTITY: warm banners, the stage braziers burning indoors
    wall_mount(objects, "banner_warm", 5, oid="banner_l", solid=False)
    wall_mount(objects, "banner_warm", 11, oid="banner_r", solid=False)
    wall_mount(objects, "lamp_rack", 6, solid=False)
    # the sun-altar on its dais
    place(objects, "altar", door_x - 1, 2)
    objects += [
        {"id": "brazier_l", "sprite": "solarium_brazier_lit",
         "at": {"tx": 5, "ty": 3}, "w": 2, "h": 3},
        {"id": "brazier_r", "sprite": "solarium_brazier_lit",
         "at": {"tx": 10, "ty": 3}, "w": 2, "h": 3},
    ]
    # west: the GREEN-ROOM — the troupe's tiring-house (their whole theatre)
    wall_mount(objects, "shelf", 1, oid="prop_shelf")
    objects += [
        {"id": "costume_rack", "sprite": "solarium_costume_rack",
         "at": {"tx": 1, "ty": 6}, "w": 2, "h": 2},
    ]
    place(objects, "crates", 2, 9, oid="prop_crates")
    # east: the sun-ledger niche (every Last-Warm-Day, kept)
    wall_mount(objects, "bookcase", 13, oid="sun_ledger")
    place(objects, "table", 13, 7, oid="ledger_table")
    place(objects, "stool", 12, 8, oid="ledger_stool")
    # pews where the pilgrims keep the warm day
    place(objects, "pew", 5, 8, oid="pew_l")
    place(objects, "pew", 10, 8, oid="pew_r")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "sunken_solarium", "to": {"tx": 5, "ty": 8}, "facing": "down",
         "transition": "door"},
    ]
    npcs = [
        # the troupe matron — the region's REST POINT (standing kit)
        {"id": "matron", "at": {"tx": 6, "ty": 6}, "facing": "right",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.solarium_rest"},
        # the prompter in the green-room (humour slot 3)
        {"id": "prompter", "at": {"tx": 2, "ty": 7}, "facing": "down",
         "sprite": "npc_man", "movement": "look_around",
         "dialogue_ref": "npc.solarium_prompter"},
        # the sun-ledger keeper at the niche
        {"id": "hall_keeper", "at": {"tx": 13, "ty": 6}, "facing": "down",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.solarium_hall_keeper"},
        # Arc E payoff: the hall answers the Gleam (standing kit)
        {"id": "hall_festival", "at": {"tx": 10, "ty": 7}, "facing": "left",
         "sprite": "npc_woman", "movement": "look_around",
         "dialogue_ref": "npc.solarium_hall_festival",
         "requires_flag": "gleam:solar"},
    ]
    return mapdef("sunken_solarium_lumenary", "Solar Lumenary", W, H, COOL_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/sunken-solarium-b.mp3")


if __name__ == "__main__":
    ok = finish(build_lumenary())
    print("content refs owed by this map (register in src/game/content/):")
    for ref in OWED:
        print(f"  - {ref}")
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
