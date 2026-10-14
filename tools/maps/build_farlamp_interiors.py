#!/usr/bin/env python3
"""
The Farlamp Isles' interiors (walkthrough/10 Part I) on the roomkit
(docs/world/interiors.md, binding): every room a composition — the SNES
enclosure + an internal partition + wall-mounted pieces + one focal point.

  driftholm_inn        16x12  common room (hearth focal) + a bunk bay; the
                              innkeeper rests you (rest point — the id is in
                              WorldScene.HEAL_ENTRANCE_MAPS, so the door wears
                              the rest-lantern)
  driftholm_chandlery  14x10  counter hall + storeroom; the Driftholm counter
                              (content/shops.ts `driftholm_chandlery`)
  driftholm_elder      14x10  Elder Nan Creel's house: hearth room + a bed nook;
                              she opens the well-stair (flag:q_isles_wellstair)
                              and keeps the Letters Home tally
  driftholm_boathouse  16x10  the boat-shed: a hull on the stocks, oars and
                              lamp-cells; the boat-builder's apprentice + a cache
  gullwrack_hut        10x9   the Gullwrack keeper's bothy: a cot and a fire —
                              a rest point on the wild isle (HEAL_ENTRANCE_MAPS)

Door landings pair with build_driftholm.py / build_farlamp_isles.py.

Run:  python3 tools/maps/build_farlamp_interiors.py
"""
from __future__ import annotations

import sys

from roomkit import (WARM_SET, faced_room, windows, partition_v, place, wall_mount,
                     mapdef, finish)

INN_MUSIC = "assets/audio/music/inn-rest.mp3"
SHOP_MUSIC = "assets/audio/music/shop-counter.mp3"
HOME_MUSIC = "assets/audio/music/interior-lamplit.mp3"
HUSH_MUSIC = "assets/audio/music/interior-hush.mp3"


def out_warps(door_x, H, to_map, xs, to_y):
    """One exit doormat -> the town tile below the door; a 2-wide town door
    lands on its LEFT tile."""
    return [{"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
             "to_map": to_map, "to": {"tx": xs, "ty": to_y}, "facing": "down",
             "transition": "door"}]


def build_inn():
    W, H = 16, 12
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [6, 14])
    partition_v(over, W, 5, 1, 6, lip="e")          # the bunk bay
    objects: list = []
    place(objects, "bed_inn", 1, 2, oid="bed1")
    place(objects, "bed_inn", 3, 2, oid="bed2")
    place(objects, "plant", 1, 6)
    wall_mount(objects, "hearth", 8)
    wall_mount(objects, "lamp_rack", 12, solid=False)
    place(objects, "counter", 10, 4, oid="counter")
    place(objects, "table_long", 11, 7)
    place(objects, "stool", 11, 9, oid="stool_a")
    place(objects, "stool", 13, 9, oid="stool_b")
    place(objects, "table", 2, 8, oid="table_round")
    place(objects, "stool", 1, 8, oid="stool_c")
    place(objects, "barrels", 6, 9, oid="barrels")
    place(objects, "rug", 7, 7, solid=False)
    triggers = [{"id": "sign_welcome", "kind": "sign", "at": {"tx": 14, "ty": 4},
                 "activation": "interact", "ref": "sign.driftholm_inn"}]
    npcs = [
        {"id": "innkeeper", "at": {"tx": 12, "ty": 3}, "facing": "down", "sprite": "innkeeper",
         "movement": "static", "dialogue_ref": "script.driftholm_inn_rest"},
        {"id": "inn_fisher_night", "at": {"tx": 12, "ty": 9}, "facing": "up",
         "sprite": "fisher_man", "movement": "static", "dialogue_ref": "npc.driftholm_inn_fisher",
         "hidden_when_flag": "flag:isles_dawn"},
        {"id": "inn_fisher_day", "at": {"tx": 4, "ty": 9}, "facing": "up",
         "sprite": "fisher_man", "movement": "static",
         "dialogue_ref": "npc.driftholm_inn_fisher_day", "requires_flag": "flag:isles_dawn"},
    ]
    return mapdef("driftholm_inn", "The Lamplighters' Rest", W, H, WARM_SET, base, over,
                  objects, out_warps(door_x, H, "driftholm", 4, 17), triggers, npcs, INN_MUSIC)


def build_chandlery():
    W, H = 14, 10
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [3])
    partition_v(over, W, 10, 1, 4, lip="w")          # the storeroom
    objects: list = []
    wall_mount(objects, "shelf", 1, oid="wares")
    wall_mount(objects, "lamp_rack", 8, solid=False)
    place(objects, "counter", 4, 3)
    place(objects, "crates", 11, 2)
    place(objects, "oil_jars", 11, 4, oid="stock")
    place(objects, "rug", 5, 6, solid=False)
    place(objects, "barrels", 1, 8)
    place(objects, "plant", 12, 8)
    triggers = [{"id": "sign_wares", "kind": "sign", "at": {"tx": 1, "ty": 3},
                 "activation": "interact", "ref": "sign.driftholm_chandlery"}]
    npcs = [{"id": "chandler", "at": {"tx": door_x - 1, "ty": 2}, "facing": "down",
             "sprite": "market_trader", "movement": "static",
             "dialogue_ref": "script.driftholm_chandler"}]
    return mapdef("driftholm_chandlery", "Creel & Daughter, Chandlers", W, H, WARM_SET, base,
                  over, objects, out_warps(door_x, H, "driftholm", 22, 14), triggers, npcs,
                  SHOP_MUSIC)


def build_elder():
    W, H = 14, 10
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [6, 11])
    partition_v(over, W, 9, 1, 5, lip="w")           # Nan's bed nook
    objects: list = []
    wall_mount(objects, "bookcase", 1)
    wall_mount(objects, "hearth", 4)
    wall_mount(objects, "dresser", 7)
    place(objects, "bed", 10, 2)
    place(objects, "plant", 12, 2)
    place(objects, "rug", 3, 5, solid=False)
    place(objects, "table", 3, 5, oid="table_round")
    place(objects, "armchair", 6, 5)
    place(objects, "sacks", 1, 8)
    place(objects, "stool", 12, 7)
    triggers = [{"id": "sign_logbook", "kind": "sign", "at": {"tx": 1, "ty": 3},
                 "activation": "interact", "ref": "sign.driftholm_elder_shelf"}]
    npcs = [{"id": "nan_creel", "at": {"tx": 6, "ty": 7}, "facing": "down",
             "sprite": "npc_old_woman", "movement": "static", "dialogue_ref": "script.nan_creel"}]
    return mapdef("driftholm_elder", "Elder Creel's House", W, H, WARM_SET, base, over,
                  objects, out_warps(door_x, H, "driftholm", 17, 24), triggers, npcs, HOME_MUSIC)


def build_boathouse():
    W, H = 16, 10
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [4, 11])
    partition_v(over, W, 11, 1, 4, lip="w")          # the oar-store
    objects: list = []
    wall_mount(objects, "lamp_rack", 1, solid=False)
    wall_mount(objects, "shelf", 3)
    wall_mount(objects, "lamp_rack", 8, solid=False, oid="lamp_rack_b")
    objects.append({"id": "hull", "sprite": "farlamp_hull", "at": {"tx": 5, "ty": 4},
                    "w": 3, "h": 2})
    place(objects, "crates", 12, 2)
    place(objects, "barrels", 12, 5, oid="tar")
    place(objects, "sacks", 1, 7)
    place(objects, "desk", 13, 7)
    place(objects, "stool", 12, 7)
    triggers = [{"id": "sign_hull", "kind": "sign", "at": {"tx": 6, "ty": 5},
                 "activation": "interact", "ref": "sign.driftholm_boathouse_hull"}]
    npcs = [
        {"id": "boatwright_apprentice", "at": {"tx": 9, "ty": 6}, "facing": "left",
         "sprite": "npc_boy", "movement": "static", "dialogue_ref": "npc.driftholm_apprentice"},
        {"id": "cache_boathouse", "at": {"tx": 14, "ty": 4}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_driftholm_boathouse",
         "hidden_when_flag": "flag:picked_driftholm_boathouse"},
    ]
    return mapdef("driftholm_boathouse", "The Boathouse", W, H, WARM_SET, base, over,
                  objects, out_warps(door_x, H, "driftholm", 4, 10), triggers, npcs, HUSH_MUSIC)


def build_hut():
    W, H = 10, 9
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [7])
    objects: list = []
    wall_mount(objects, "hearth", 1)
    wall_mount(objects, "shelf", 6)
    place(objects, "bed", 7, 4)
    place(objects, "table", 2, 5, oid="table_round")
    place(objects, "stool", 4, 5)
    place(objects, "sacks", 1, 7)
    triggers = [{"id": "hut_bed", "kind": "script", "at": {"tx": 7, "ty": 6},
                 "activation": "interact", "ref": "script.gullwrack_hut_rest"},
                {"id": "sign_log", "kind": "sign", "at": {"tx": 6, "ty": 3},
                 "activation": "interact", "ref": "sign.gullwrack_hut_log"}]
    npcs = [{"id": "hut_keeper", "at": {"tx": 4, "ty": 4}, "facing": "down",
             "sprite": "frost_herder", "movement": "static",
             "dialogue_ref": "script.gullwrack_hut_rest"}]
    return mapdef("gullwrack_hut", "The Keeper's Bothy", W, H, WARM_SET, base, over,
                  objects, out_warps(door_x, H, "farlamp_gullwrack", 7, 24), triggers, npcs,
                  HUSH_MUSIC)


def all_maps():
    return [build_inn(), build_chandlery(), build_elder(), build_boathouse(), build_hut()]


if __name__ == "__main__":
    ok = True
    for m in all_maps():
        print(f"== {m['id']}")
        ok = finish(m) and ok
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
