#!/usr/bin/env python3
"""
Georgina's cottage (georgina_cottage) — the interior of the optional East side
quest "The Sunniest House in the Dark" (gloamwood_dell, off lowleaf_hollow).

A warm-register cottage on roomkit (docs/world/interiors.md): a fairy-lit,
cat-stuffed home in the darkest dell of the hollow. ONE internal partition
makes the dragon-cat's nook east (a cushioned bed where the Gloampurr rests),
the hearth is the focal point top-centre, and the floor is busy with plants,
a tea table and ambient cats underfoot — the "crazy cat lady" read carried by
dressing + NPCs, not by a single box of props.

Georgina stands at the hearth in FOUR flag-disjoint stages (the standing
giver-swap): intro (asks you to fetch her bolted kitten Pim) -> waiting ->
ready-to-battle (Pim home) -> after (the gift given). The resting Gloampurr
appears in the nook only once she's been beaten and the secret revealed.

Run:  ./venv/bin/python tools/maps/build_georgina_cottage.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, faced_room, windows, partition_v,
                     place, wall_mount, mapdef, finish)


def build_cottage():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    windows(over, W, [4, 11])
    # the dragon-cat's nook behind a partition, east — cushioned, out of the way
    partition_v(over, W, 11, 1, 5, lip="w")

    objects: list = []
    # focal hearth top-centre; fairy-light lamp-racks either side (warm and busy)
    wall_mount(objects, "hearth", 7)
    wall_mount(objects, "lamp_rack", 2, solid=False)
    wall_mount(objects, "lamp_rack", 13, oid="lamp_rack_e", solid=False)
    # the nook: the Gloampurr's cushion-bed + a fern keeping it company
    place(objects, "bed_inn", 12, 2, oid="cat_cushion")
    place(objects, "plant", 15, 5, oid="nook_fern")
    # the home: tea table + stools west, a rug, plants everywhere, sacks of cat-food
    place(objects, "table_long", 2, 5)
    place(objects, "stool", 2, 7, oid="stool_a")
    place(objects, "stool", 4, 7, oid="stool_b")
    place(objects, "rug", 6, 7, solid=False)
    place(objects, "barrels", 1, 3, oid="cat_food")
    place(objects, "plant", 5, 3, oid="plant_a")
    place(objects, "plant", 10, 3, oid="plant_b")
    place(objects, "plant", 9, 8, oid="plant_c")

    warps = [
        {"id": "to_dell", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "gloamwood_dell", "to": {"tx": 8, "ty": 7}, "facing": "down",
         "transition": "door"},
    ]
    triggers = []
    # Georgina's four stages, all at the hearth-front tile. The kitten gate is
    # flag:q_east_georgina_kitten (set out in the dell); the battle + dragon-cat
    # gift live in script.georgina_battle, closing on flag:q_east_georgina_done.
    npcs = [
        {"id": "georgina_intro", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "georgina", "movement": "static",
         "dialogue_ref": "script.georgina_intro",
         "hidden_when_flag": "flag:q_east_georgina_met"},
        {"id": "georgina_waiting", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "georgina", "movement": "static",
         "dialogue_ref": "npc.georgina_waiting",
         "requires_flag": "flag:q_east_georgina_met",
         "hidden_when_flag": "flag:q_east_georgina_kitten"},
        {"id": "georgina_battle", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "georgina", "movement": "static",
         "dialogue_ref": "script.georgina_battle",
         "requires_flag": "flag:q_east_georgina_kitten",
         "hidden_when_flag": "flag:georgina_beaten"},
        {"id": "georgina_after", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "georgina", "movement": "look_around",
         "dialogue_ref": "script.georgina_after",
         "requires_flag": "flag:georgina_beaten"},
        # the pride of the house — uncurls in the nook once the secret is out
        {"id": "gloampurr_nook", "at": {"tx": 13, "ty": 4}, "facing": "down",
         "sprite": "cottage_cat", "movement": "static",
         "dialogue_ref": "npc.gloampurr_nook",
         "requires_flag": "flag:georgina_beaten"},
        # ambient cats underfoot (the crazy-cat-lady read)
        {"id": "cottage_cat_a", "at": {"tx": 4, "ty": 8}, "facing": "right",
         "sprite": "cottage_cat", "movement": "wander",
         "dialogue_ref": "npc.cottage_cat_a"},
        {"id": "cottage_cat_b", "at": {"tx": 10, "ty": 7}, "facing": "left",
         "sprite": "cottage_cat", "movement": "look_around",
         "dialogue_ref": "npc.cottage_cat_b"},
    ]
    return mapdef("georgina_cottage", "Georgina's Cottage", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/lowleaf-hollow-b.mp3")


if __name__ == "__main__":
    ok = finish(build_cottage())
    print("DONE" if ok else "DONE (with audit failures)")
