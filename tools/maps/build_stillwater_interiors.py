#!/usr/bin/env python3
"""
Stillwater's interiors (walkthrough/11 Part A) on the roomkit
(docs/world/interiors.md, binding): every room a composition — the SNES
enclosure + an internal partition + wall-mounted pieces + one focal point.

The village's own SHUTTER-GREY kit (build_stillwater_interior_set.py: the warm
kit's tile order, drained — grey-washed boards, pale limewash, the windows
shuttered), dressed with Stillwater pieces drawn by stillwaterforge.py (the
shutter-wall, hooded-lamp racks, the lamp-maker's bench, grey blankets over
sleeping kin, wool baskets). The one warm note in every room is its hearth.

  stillwater_quiet_hall   18x14  the meeting-house: the SHUTTER-WALL (focal, the
                                 names of the lamps they've put out), pews, a vestry
  stillwater_shutter      16x12  the inn ("The Shutter"): a rest point — the id goes
                                 in WorldScene.HEAL_ENTRANCE_MAPS (engine; coordinator)
  stillwater_lampmaker    14x10  the dark-lamp maker's shop + storeroom (a counter)
  stillwater_home_a       12x9   the old couple's cottage: hearth room + bed nook
  stillwater_home_b       12x9   Maren's house (the candle child's mother)

Door landings pair with build_stillwater.py (each room's doormat is at
(W//2, H-1); the town lands one tile above it).

Run:  python3 tools/maps/build_stillwater_interiors.py
"""
from __future__ import annotations

import sys

from roomkit import (WARM_SET, faced_room, windows, partition_v, place, wall_mount,
                     aisle_runner, mapdef, finish, _MANIFEST)

SHUTTER_SET = dict(WARM_SET, name="interior_shutter_set",
                   image="assets/tilesets/interior_shutter_set.webp")

INN_MUSIC = "assets/audio/music/inn-rest.mp3"
SHOP_MUSIC = "assets/audio/music/shop-counter.mp3"
HUSH_MUSIC = "assets/audio/music/interior-hush.mp3"
UNEASE_MUSIC = "assets/audio/music/interior-unease.mp3"


def still(objects: list, stem: str, tx: int, ty: int, *, oid: str | None = None,
          solid: bool = True) -> dict:
    """A free-standing Stillwater piece (`stillwater_<stem>`), manifest footprint."""
    sp = _MANIFEST[f"stillwater_{stem}"]
    o = {"id": oid or stem, "sprite": f"stillwater_{stem}", "at": {"tx": tx, "ty": ty},
         "w": sp["tw"], "h": sp["th"]}
    if not solid:
        o["solid"] = False
    objects.append(o)
    return o


def hung(objects: list, stem: str, tx: int, *, oid: str | None = None) -> dict:
    """A wall-HUNG Stillwater piece on the north wall's face row (decor over the
    face tile, which keeps colliding: the banner convention)."""
    sp = _MANIFEST[f"stillwater_{stem}"]
    o = {"id": oid or stem, "sprite": f"stillwater_{stem}", "at": {"tx": tx, "ty": 1},
         "w": sp["tw"], "h": sp["th"], "overhang": 1, "walk_under": True, "solid": False}
    objects.append(o)
    return o


def out_warp(door_x, H, tx, ty):
    return [{"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
             "to_map": "stillwater", "to": {"tx": tx, "ty": ty}, "facing": "down",
             "transition": "door"}]


def npc(nid, at, sprite, ref, facing="down", **kw):
    n = {"id": nid, "at": {"tx": at[0], "ty": at[1]}, "facing": facing, "sprite": sprite,
         "movement": "static", "dialogue_ref": ref}
    n.update(kw)
    return n


def build_hall():
    W, H = 18, 14
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [3, 13])
    partition_v(over, W, 14, 1, 4, lip="w")                  # the vestry alcove
    objects: list = []
    hung(objects, "shutter_wall", 5, oid="shutter_wall_a")    # THE SHUTTER-WALL (focal)
    hung(objects, "shutter_wall", 9, oid="shutter_wall_b")
    place(objects, "table_long", 8, 4, oid="remembrance_table")
    hung(objects, "hood_rack", 1, oid="hall_hoods")
    wall_mount(objects, "bookcase", 15)
    place(objects, "desk", 15, 4)
    for n, (x, y) in enumerate([(3, 7), (11, 7), (3, 9), (11, 9)]):
        place(objects, "pew", x, y, oid=f"pew_{n}")
    aisle_runner(objects, 9, 6, 11)
    still(objects, "blanket_kin", 1, 11, oid="hall_sleeper")
    still(objects, "wool_basket", 16, 11)
    still(objects, "wool_basket", 2, 4, oid="wool_b")
    still(objects, "blanket_kin_b", 14, 11, oid="hall_sleeper_b")
    triggers = [{"id": f"wall_read_{x}", "kind": "script", "at": {"tx": x, "ty": 2},
                 "activation": "interact", "ref": "script.still_shutter_wall"}
                for x in (5, 6, 7, 11, 12)]
    triggers.append({"id": "vestry_read", "kind": "script", "at": {"tx": 15, "ty": 5},
                     "activation": "interact", "ref": "script.still_vestry_ledger"})
    npcs = [
        npc("hall_keeper", (12, 4), "hollowing_elder", "script.still_hall_keeper"),
        npc("hall_mourner", (6, 10), "npc_woman", "script.still_hall_mourner", facing="up"),
        npc("hall_reader", (16, 8), "hollowing_acolyte", "script.still_hall_reader", facing="left"),
    ]
    return mapdef("stillwater_quiet_hall", "The Quiet Hall", W, H, SHUTTER_SET, base, over,
                  objects, out_warp(door_x, H, 15, 15), triggers, npcs, HUSH_MUSIC)


def build_inn():
    W, H = 16, 12
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [6, 14])
    partition_v(over, W, 5, 1, 6, lip="e")                    # the bunk bay
    objects: list = []
    place(objects, "bed_inn", 1, 2, oid="bed1")
    place(objects, "bed_inn", 3, 2, oid="bed2")
    still(objects, "wool_basket", 1, 5, oid="bay_wool")
    wall_mount(objects, "hearth", 8)
    hung(objects, "hood_rack", 12)
    place(objects, "counter", 10, 4, oid="counter")
    place(objects, "desk", 11, 8)
    place(objects, "stool", 10, 8, oid="stool_a")
    place(objects, "stool", 13, 8, oid="stool_b")
    place(objects, "desk", 2, 8, oid="table_b")
    place(objects, "stool", 1, 8, oid="stool_c")
    still(objects, "blanket_kin_b", 5, 9, oid="hearth_sleeper")
    triggers = [{"id": "sign_welcome", "kind": "sign", "at": {"tx": 14, "ty": 4},
                 "activation": "interact", "ref": "sign.stillwater_inn"}]
    npcs = [
        npc("innkeeper", (12, 3), "innkeeper", "script.still_inn_rest"),
        npc("inn_guest", (4, 9), "hollowing_acolyte", "script.still_inn_guest", facing="right"),
        npc("inn_pilgrim", (12, 10), "pass_walker", "script.still_inn_pilgrim", facing="up"),
    ]
    return mapdef("stillwater_shutter", "The Shutter", W, H, SHUTTER_SET, base, over,
                  objects, out_warp(door_x, H, 4, 15), triggers, npcs, INN_MUSIC)


def build_lampmaker():
    W, H = 14, 10
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [11])
    partition_v(over, W, 10, 1, 4, lip="w")                  # the storeroom
    objects: list = []
    hung(objects, "hood_rack", 1, oid="rack_a")
    wall_mount(objects, "shelf", 3)
    hung(objects, "hood_rack", 6, oid="rack_b")
    place(objects, "counter", 4, 3)
    still(objects, "lamp_bench", 1, 6)
    still(objects, "lamp_bench", 8, 6, oid="lamp_bench_b")
    place(objects, "stool", 1, 7)
    place(objects, "crates", 11, 2)
    place(objects, "oil_jars", 11, 5, oid="stock")
    place(objects, "barrels", 11, 8)
    triggers = [{"id": "bench_read", "kind": "script", "at": {"tx": 2, "ty": 7},
                 "activation": "interact", "ref": "script.still_lamp_bench"}]
    npcs = [npc("lampmaker", (6, 2), "lamplighter", "script.still_lampmaker")]
    return mapdef("stillwater_lampmaker", "The Dark-Lamp Maker", W, H, SHUTTER_SET, base,
                  over, objects, out_warp(door_x, H, 23, 15), triggers, npcs, SHOP_MUSIC)


def build_home_a():
    W, H = 12, 9
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [6])
    partition_v(over, W, 8, 1, 4, lip="w")                   # the bed nook
    objects: list = []
    wall_mount(objects, "hearth", 1)
    wall_mount(objects, "dresser", 4)
    place(objects, "bed", 9, 2)
    place(objects, "desk", 2, 5)
    place(objects, "stool", 4, 5)
    place(objects, "armchair", 5, 4)
    still(objects, "blanket_kin", 9, 6, oid="nook_sleeper")
    still(objects, "wool_basket", 1, 7)
    npcs = [npc("old_tam", (7, 5), "npc_old_man", "script.still_home_a_elder", facing="left"),
            npc("old_ines", (2, 4), "npc_old_woman", "script.still_home_a_wife")]
    triggers = [{"id": "sleeper_read", "kind": "script", "at": {"tx": 9, "ty": 5},
                 "activation": "interact", "ref": "script.still_sleeper"}]
    return mapdef("stillwater_home_a", "Ines and Tam's Cottage", W, H, SHUTTER_SET, base, over,
                  objects, out_warp(door_x, H, 10, 25), triggers, npcs, HUSH_MUSIC)


def build_home_b():
    W, H = 12, 9
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [6])
    partition_v(over, W, 3, 1, 4, lip="e")                   # the child's nook
    objects: list = []
    place(objects, "bed", 1, 2, oid="child_bed")
    wall_mount(objects, "hearth", 7)
    wall_mount(objects, "shelf", 4)
    place(objects, "desk", 7, 5)
    place(objects, "stool", 9, 5)
    still(objects, "wool_basket", 10, 7)
    still(objects, "blanket_kin_b", 1, 6, oid="child_sleeper")
    npcs = [npc("maren", (5, 5), "npc_parent", "script.still_maren", facing="down")]
    triggers = [{"id": "child_bed_read", "kind": "script", "at": {"tx": 1, "ty": 5},
                 "activation": "interact", "ref": "script.still_child_bed"}]
    return mapdef("stillwater_home_b", "Maren's House", W, H, SHUTTER_SET, base, over,
                  objects, out_warp(door_x, H, 19, 25), triggers, npcs, UNEASE_MUSIC)


def all_maps():
    return [build_hall(), build_inn(), build_lampmaker(), build_home_a(), build_home_b()]


if __name__ == "__main__":
    ok = True
    for m in all_maps():
        print(f"== {m['id']}")
        ok = finish(m) and ok
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
