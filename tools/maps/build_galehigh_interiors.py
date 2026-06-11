#!/usr/bin/env python3
"""
Galehigh Terraces interiors (docs/world/interiors.md, on roomkit):

  * galehigh_lumenary  — Mira Vael's Storm hall: cool stone register with a
    WIND/KITE identity — banner insets on the face, the Storm altar on its
    dais, a kite-loft nook west (the festival's spare sails + line), a
    star-ledger niche east. NO bond-test here: Mira fights at the SKYLOFT
    launch ledge (walkthrough 03-north beat 6); the hall is the festival's
    home and the Gleam's witness room.
  * galehigh_inn       — the terrace inn (the town's rest point): hearth,
    bunk room behind a partition, keeper's full rest-heal
    (script.galehigh_inn_rest — the standing kit).
  * galehigh_home      — a wind-break cottage: hearth-room + bed nook, the
    terrace-farm couple.
  * galehigh_kitemaker — the kite-maker's workshop/shop: counter focal, a
    storeroom bay of crates + a wares shelf (kite stock), the shop-kit ->
    open-counter keeper pair (flag:galehigh_kit; ShopDef 'galehigh' comes
    with the economy wiring — script.shop_galehigh ends in the shop op).

Run:  ./venv/bin/python tools/maps/build_galehigh_interiors.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, COOL_SET, BANNER, faced_room, windows, partition_v,
                     place, wall_mount, aisle_runner, mapdef, finish)

OWED = [
    "npc.galehigh_hall_keeper", "npc.galehigh_hall_festival (requires gleam:storm)",
    "script.galehigh_inn_rest (ends in the heal op)", "npc.galehigh_inn_guest",
    "npc.galehigh_home_elder", "npc.galehigh_home_kid",
    "script.shop_kit_galehigh (one-time kit; sets flag:galehigh_kit)",
    "script.shop_galehigh (open counter; ends in { op:'shop', shop:'galehigh' })",
]


def build_lumenary():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    # the kite-loft nook west + the star-ledger niche east
    partition_v(over, W, 4, 1, 4, lip="e")
    partition_v(over, W, 12, 1, 4, lip="w")
    windows(over, W, [6, 10], tile=BANNER)

    objects: list = []
    # the carpet aisle (drawn runner objects — never the doormat tile)
    aisle_runner(objects, door_x, 5, H - 2)
    # the Storm altar on its dais, braziers flanking (the festival's hearth)
    place(objects, "altar", door_x - 1, 2)
    place(objects, "brazier", 5, 3, oid="brazier_l")
    place(objects, "brazier", 11, 3, oid="brazier_r")
    # west: the kite-loft — spare sails on a wares shelf, line in barrels
    wall_mount(objects, "shelf", 1, oid="kite_sails")
    place(objects, "barrels", 1, 7, oid="kite_line")
    place(objects, "crates", 2, 4, oid="festival_crates")
    # east: the star-ledger niche
    wall_mount(objects, "bookcase", 13, oid="star_ledger")
    place(objects, "table", 13, 7, oid="ledger_table")
    place(objects, "stool", 12, 8, oid="ledger_stool")
    # pews where the town gathers before the rising
    place(objects, "pew", 5, 8, oid="pew_l")
    place(objects, "pew", 10, 8, oid="pew_r")
    wall_mount(objects, "lamp_rack", 6, solid=False)

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 9, "ty": 18}, "facing": "down",
         "transition": "door"},
    ]
    triggers = []
    # the hall-keeper tends the altar (Mira is flying — the skyloft has her);
    # a festival witness joins once the Storm Gleam stands (Arc E payoff)
    npcs = [
        {"id": "hall_keeper", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "npc.galehigh_hall_keeper"},
        {"id": "hall_festival", "at": {"tx": 6, "ty": 7}, "facing": "right",
         "sprite": "npc_woman", "movement": "look_around",
         "dialogue_ref": "npc.galehigh_hall_festival",
         "requires_flag": "gleam:storm"},
    ]
    return mapdef("galehigh_lumenary", "Galehigh Storm Lumenary", W, H, COOL_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/galehigh-terraces-b.mp3")


def build_inn():
    W, H = 14, 11
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [4, 11])
    # the bunk room behind a partition — festival guests sleep off the common room
    partition_v(over, W, 9, 1, 5, lip="w")

    objects: list = []
    wall_mount(objects, "hearth", 5)
    wall_mount(objects, "lamp_rack", 2, solid=False)
    place(objects, "bed_inn", 10, 2, oid="bunk_a")
    place(objects, "bed_inn", 12, 2, oid="bunk_b")
    place(objects, "plant", 10, 5, oid="nook_fern")
    place(objects, "table_long", 2, 5)
    place(objects, "stool", 2, 7, oid="stool_a")
    place(objects, "stool", 4, 7, oid="stool_b")
    place(objects, "rug", 6, 7, solid=False)
    place(objects, "barrels", 1, 3, oid="cellar_ale")
    place(objects, "sacks", 12, 8, oid="grain")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 4, "ty": 28}, "facing": "down",
         "transition": "door"},
    ]
    npcs = [
        # the keeper's rest-heal (script ends in the `heal` op — standing kit)
        {"id": "innkeeper", "at": {"tx": 6, "ty": 4}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.galehigh_inn_rest"},
        {"id": "guest", "at": {"tx": 3, "ty": 6}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.galehigh_inn_guest"},
    ]
    return mapdef("galehigh_inn", "The Steady Gust Inn", W, H, WARM_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/galehigh-terraces-b.mp3")


def build_home():
    W, H = 12, 9
    door_x = W // 2  # tx 6
    base, over = faced_room(W, H, door_x)
    windows(over, W, [3, 9])
    # the bed nook east
    partition_v(over, W, 8, 1, 3, lip="w")

    objects: list = []
    wall_mount(objects, "hearth", 4)
    place(objects, "bed", 9, 2, oid="bed")
    place(objects, "table", 3, 4)
    place(objects, "stool", 2, 5, oid="stool")
    place(objects, "rug", 5, 5, solid=False)
    place(objects, "sacks", 1, 7, oid="seed_sacks")
    place(objects, "plant", 10, 6, oid="sill_fern")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 26, "ty": 28}, "facing": "down",
         "transition": "door"},
    ]
    npcs = [
        {"id": "home_elder", "at": {"tx": 4, "ty": 4}, "facing": "down",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.galehigh_home_elder"},
        {"id": "home_kid", "at": {"tx": 7, "ty": 6}, "facing": "left",
         "sprite": "npc_child", "movement": "wander",
         "dialogue_ref": "npc.galehigh_home_kid"},
    ]
    return mapdef("galehigh_home", "Terrace Cottage", W, H, WARM_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/galehigh-terraces-b.mp3")


def build_kitemaker():
    W, H = 14, 10
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [3, 11])
    # the storeroom bay west: kite stock the player sees but can't shop from
    partition_v(over, W, 4, 1, 4, lip="e")

    objects: list = []
    # the counter focal, keeper behind it
    place(objects, "counter", 6, 3)
    wall_mount(objects, "shelf", 8, oid="kite_wares")
    wall_mount(objects, "lamp_rack", 11, solid=False)
    # the storeroom: crates of spars + sail rolls
    place(objects, "crates", 1, 3, oid="spar_crates")
    place(objects, "barrels", 1, 6, oid="line_spools")
    place(objects, "sacks", 2, 8, oid="sail_rolls")
    place(objects, "rug", 8, 6, solid=False)
    place(objects, "plant", 12, 7, oid="door_fern")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 13, "ty": 27}, "facing": "down",
         "transition": "door"},
    ]
    # the standing shop pattern: one-time kit -> the open counter (the shop
    # DATA — ShopDef 'galehigh', prices, stock — lands with the wiring agent)
    npcs = [
        {"id": "keeper_kit", "at": {"tx": 7, "ty": 2}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.shop_kit_galehigh",
         "hidden_when_flag": "flag:galehigh_kit"},
        {"id": "keeper", "at": {"tx": 7, "ty": 2}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.shop_galehigh",
         "requires_flag": "flag:galehigh_kit"},
    ]
    return mapdef("galehigh_kitemaker", "The Kite-Maker's", W, H, WARM_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/galehigh-terraces-b.mp3")


if __name__ == "__main__":
    ok = True
    for build in (build_lumenary, build_inn, build_home, build_kitemaker):
        ok = finish(build()) and ok
    print("content refs owed (register in src/game/content/):")
    for ref in OWED:
        print(f"  - {ref}")
    print("DONE" if ok else "DONE (with audit failures)")
    raise SystemExit(0 if ok else 1)
