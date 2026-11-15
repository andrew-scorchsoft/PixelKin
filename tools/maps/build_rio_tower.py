#!/usr/bin/env python3
"""
The RIO TOWER — the old storm-watchers' tower on the Thousandfold's rim (the Sere,
build_the_sere.py), three stacked interiors on roomkit:

  rio_tower_1    THE FOOT — the porter's lobby: the tower's history on the wall
                 (the Rio, the river that cut the Thousandfold and is long gone),
                 benches for drovers waiting out the heat. Up-stairs NE.
  rio_tower_2    THE WATCH — Calder Voss, the last storm-watcher, keeps the Storm
                 Log at his lectern; a storm-chaser holds the crossing (top-row
                 sight post, the Beacon pattern). Down NE, up NW (a spiral).
  rio_tower_top  THE THUNDER TABLE — the restaurant under the awning: a great
                 window over the canyon across the north wall, tables, and
                 Ottoline Bask at the kitchen pass (`sere_dish_counter`: talk across
                 it). Order a dish (the `pay` op); with all three Calling Rods lit
                 the rolling thunder comes across the Sere (script.rio_thunder).

Spiral read: in at the foot door -> NE stair -> the watch -> NW stair -> the top.
Warm sandstone register (WARM_SET) — an eating-house, not a shrine.

Run:  python3 tools/maps/build_rio_tower.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, FLOOR, DOORMAT, CAP_N, faced_room, windows, partition_v,
                     place, wall_mount, aisle_runner, mapdef, obj, finish)

MUSIC = "assets/audio/music/interior-lamplit.mp3"
TOP_MUSIC = "assets/audio/music/inn-rest.mp3"


def wall_up_door(m: dict, door_x: int) -> None:
    """A tower floor has no bottom door: wall the default doormat back up."""
    W, H = m["width"], m["height"]
    m["layers"][0]["data"][(H - 1) * W + door_x] = FLOOR
    m["layers"][1]["data"][(H - 1) * W + door_x] = CAP_N


def foot():
    W, H = 12, 10
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [3, 9])
    up = (10, 2)
    base[up[1] * W + up[0]] = DOORMAT
    objects: list = []
    aisle_runner(objects, door_x, 3, H - 2)
    wall_mount(objects, "bookcase", 1)                       # the tower's ledgers
    objects.append(obj("barometer", "sere_barometer", 4, 1, 1, 2, overhang=1))
    place(objects, "table", 7, 5, oid="drovers_table")
    place(objects, "stool", 7, 7, oid="stool_a")
    place(objects, "stool", 9, 6, oid="stool_b")
    place(objects, "barrels", 1, 8)
    place(objects, "plant", 10, 8)
    warps = [
        {"id": "to_sere", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "the_sere", "to": {"tx": 30, "ty": 18}, "facing": "down",
         "transition": "door"},
        {"id": "up_stairs", "at": {"tx": up[0], "ty": up[1]}, "trigger": "step_on",
         "to_map": "rio_tower_2", "to": {"tx": 10, "ty": 3}, "facing": "down",
         "transition": "fade"},
    ]
    triggers = [
        {"id": "plaque", "kind": "sign", "at": {"tx": 1, "ty": 3}, "activation": "interact",
         "ref": "sign.rio_plaque"},
        {"id": "barometer", "kind": "sign", "at": {"tx": 4, "ty": 2}, "activation": "interact",
         "ref": "sign.rio_barometer"},
    ]
    npcs = [
        {"id": "porter_amsel", "at": {"tx": 4, "ty": 5}, "facing": "down",
         "sprite": "innkeeper", "movement": "static", "dialogue_ref": "script.rio_porter"},
        {"id": "drover_resting", "at": {"tx": 9, "ty": 5}, "facing": "left",
         "sprite": "market_trader", "movement": "static", "dialogue_ref": "npc.rio_drover"},
    ]
    return mapdef("rio_tower_1", "Rio Tower", W, H, WARM_SET, base, over, objects,
                  warps, triggers, npcs, MUSIC)


def watch():
    W, H = 12, 10
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [4, 8])
    down, up = (10, 2), (1, 2)
    base[down[1] * W + down[0]] = DOORMAT
    base[up[1] * W + up[0]] = DOORMAT
    objects: list = []
    objects.append(obj("storm_log", "sere_storm_log", 2, 5, 2, 2))
    objects.append(obj("barometer", "sere_barometer", 8, 1, 1, 2, overhang=1))
    wall_mount(objects, "lamp_rack", 6, solid=False)
    place(objects, "rug", 4, 7, solid=False)
    place(objects, "desk", 8, 6)
    place(objects, "stool", 9, 8, oid="stool_a")
    place(objects, "plant", 1, 8)
    warps = [
        {"id": "down_stairs", "at": {"tx": down[0], "ty": down[1]}, "trigger": "step_on",
         "to_map": "rio_tower_1", "to": {"tx": 10, "ty": 3}, "facing": "down",
         "transition": "fade"},
        {"id": "up_stairs", "at": {"tx": up[0], "ty": up[1]}, "trigger": "step_on",
         "to_map": "rio_tower_top", "to": {"tx": 1, "ty": 3}, "facing": "down",
         "transition": "fade"},
    ]
    triggers = [
        {"id": "storm_log", "kind": "cutscene", "at": {"tx": 2, "ty": 5},
         "activation": "interact", "ref": "script.rio_storm_log"},
    ]
    npcs = [
        {"id": "calder", "at": {"tx": 4, "ty": 5}, "facing": "down", "sprite": "npc_old_man",
         "movement": "look_around", "dialogue_ref": "script.rio_calder"},
        # the storm-chaser holds the crossing: top row, facing DOWN col 6 — every
        # way from the NE stair to the NW stair crosses it (the Beacon post)
        {"id": "rio_chaser", "at": {"tx": 6, "ty": 2}, "facing": "down", "sprite": "kite_weaver",
         "movement": "static", "dialogue_ref": "script.rio_chaser", "sight_range": 6,
         "defeated_flag": "flag:rio_chaser_beaten", "hidden_when_flag": "flag:rio_chaser_beaten"},
        {"id": "rio_chaser_after", "at": {"tx": 6, "ty": 2}, "facing": "down", "sprite": "kite_weaver",
         "movement": "look_around", "dialogue_ref": "npc.rio_chaser_after",
         "requires_flag": "flag:rio_chaser_beaten"},
    ]
    m = mapdef("rio_tower_2", "Rio Tower — the Watch", W, H, WARM_SET, base, over, objects,
               warps, triggers, npcs, MUSIC)
    wall_up_door(m, door_x)
    return m


def top():
    W, H = 16, 11
    base, over = faced_room(W, H, W // 2)
    down = (1, 2)
    base[down[1] * W + down[0]] = DOORMAT
    objects: list = []
    # THE VIEW: two great windows over the Thousandfold across the north wall
    # (cap + face rows — both collide underneath, so the art is solid:false)
    objects.append(obj("vista_w", "sere_vista", 3, 0, 6, 2, solid=False))
    objects.append(obj("vista_e", "sere_vista", 9, 0, 6, 2, solid=False))
    # the kitchen pass, Ottoline behind it (talk across: 'counter' in the sprite)
    objects.append(obj("pass", "sere_dish_counter", 11, 7, 3, 2))
    place(objects, "rug", 6, 7, solid=False)
    # tables under the windows (the window seat is the watcher's), stools drawn up
    place(objects, "table", 4, 4, oid="table_window")
    place(objects, "stool", 4, 6, oid="stool_w1")
    place(objects, "stool", 6, 5, oid="stool_w2")
    place(objects, "table", 9, 4, oid="table_mid")
    place(objects, "stool", 9, 6, oid="stool_m1")
    place(objects, "stool", 11, 5, oid="stool_m2")
    place(objects, "table", 3, 8, oid="table_corner")
    place(objects, "stool", 5, 8, oid="stool_c1")
    place(objects, "plant", 14, 3)
    place(objects, "plant", 1, 9, oid="plant_sw")
    place(objects, "barrels", 13, 9)
    warps = [
        {"id": "down_stairs", "at": {"tx": down[0], "ty": down[1]}, "trigger": "step_on",
         "to_map": "rio_tower_2", "to": {"tx": 1, "ty": 3}, "facing": "down",
         "transition": "fade"},
    ]
    triggers = [
        {"id": "window", "kind": "cutscene", "at": {"tx": 7, "ty": 2},
         "activation": "interact", "ref": "script.rio_window"},
    ]
    npcs = [
        {"id": "ottoline", "at": {"tx": 12, "ty": 6}, "facing": "down", "sprite": "innkeeper",
         "movement": "static", "dialogue_ref": "script.rio_ottoline"},
        {"id": "diner_a", "at": {"tx": 8, "ty": 5}, "facing": "right", "sprite": "npc_old_woman",
         "movement": "static", "dialogue_ref": "npc.rio_diner_a"},
        {"id": "diner_b", "at": {"tx": 2, "ty": 8}, "facing": "right", "sprite": "star_watcher",
         "movement": "static", "dialogue_ref": "npc.rio_diner_b"},
    ]
    m = mapdef("rio_tower_top", "Rio Tower — the Thunder Table", W, H, WARM_SET, base, over,
               objects, warps, triggers, npcs, TOP_MUSIC)
    wall_up_door(m, W // 2)
    return m


def all_maps():
    return [foot(), watch(), top()]


if __name__ == "__main__":
    ok = True
    for mp in all_maps():
        ok = finish(mp) and ok
    raise SystemExit(0 if ok else 1)
