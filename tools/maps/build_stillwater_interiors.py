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
  stillwater_home_b       12x9   Maren's house (Linnet, the candle child, and her mother)

Door landings pair with build_stillwater.py (each room's doormat is at
(W//2, H-1); the town lands one tile above it).

Run:  python3 tools/maps/build_stillwater_interiors.py
"""
from __future__ import annotations

import sys

from roomkit import (WARM_SET, faced_room, windows, partition_v, partition_h, place, wall_mount,
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


def hearth(objects: list, tx: int) -> None:
    """Stillwater's hearth, a flag-pair on ONE footprint (same w/h/overhang/
    solidity): the BANKED hearth — its face to the wall, a louvred screen latched
    across the fire — until the dawn, then the open warm hearth."""
    wall_mount(objects, "hearth", tx, oid="hearth_open")["requires_flag"] = "flag:dawn"
    sp = _MANIFEST["stillwater_hearth_banked"]
    objects.append({"id": "hearth_banked", "sprite": "stillwater_hearth_banked",
                    "at": {"tx": tx, "ty": 1}, "w": sp["tw"], "h": sp["th"],
                    "overhang": 1, "walk_under": True, "hidden_when_flag": "flag:dawn"})


def stove(objects: list, tx: int) -> None:
    """The cook-stove, the same flag-pair as the hearth (one footprint): BANKED —
    its firebox shut behind a louvred iron door — until the dawn, then the open
    stove. (The r2 review: an open, glowing stove beside a banked hearth.)"""
    wall_mount(objects, "stove", tx, oid="stove_open")["requires_flag"] = "flag:dawn"
    sp = _MANIFEST["stillwater_stove_banked"]
    objects.append({"id": "stove_banked", "sprite": "stillwater_stove_banked",
                    "at": {"tx": tx, "ty": 1}, "w": sp["tw"], "h": sp["th"],
                    "overhang": 1, "walk_under": True, "hidden_when_flag": "flag:dawn"})


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
    # the r2 review: the lower half was bare floor. A back row of memorial benches,
    # the reading lectern (the ledger of put-out lamps) where the reader keeps it,
    # boxes of spare shutters by the walls, baskets of the sprigs they tuck in.
    for n, x in enumerate((3, 11)):
        place(objects, "pew", x, 11, oid=f"pew_back_{n}")
    still(objects, "lectern", 16, 9)
    still(objects, "shutter_box", 1, 8, oid="shutter_box_w")
    still(objects, "shutter_box", 16, 6, oid="shutter_box_e")
    still(objects, "sprig_basket", 7, 12, oid="sprigs_w")
    still(objects, "sprig_basket", 11, 12, oid="sprigs_e")
    still(objects, "sprig_basket", 13, 3, oid="sprigs_wall")
    triggers = [{"id": f"wall_read_{x}", "kind": "script", "at": {"tx": x, "ty": 2},
                 "activation": "interact", "ref": "script.still_shutter_wall"}
                for x in (5, 6, 7, 11, 12)]
    triggers.append({"id": "vestry_read", "kind": "script", "at": {"tx": 15, "ty": 5},
                     "activation": "interact", "ref": "script.still_vestry_ledger"})
    npcs = [
        npc("hall_keeper", (12, 4), "hollowing_elder", "script.still_hall_keeper"),
        npc("hall_mourner", (6, 10), "npc_woman", "script.still_hall_mourner", facing="up"),
        npc("hall_reader", (16, 8), "hollowing_acolyte", "script.still_hall_reader", facing="down"),
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
    hearth(objects, 8)
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
    """The old couple's cottage — WIDE and low: one long hearth-room where two old
    chairs sit with their backs to the screened hearth, a tea table by the stove,
    and a bed nook behind a partition where Old Bracken sleeps in his basket."""
    W, H = 14, 9
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [6, 12])
    partition_v(over, W, 9, 1, 4, lip="w")                   # the bed nook (east)
    objects: list = []
    hearth(objects, 1)                                        # screened; open at dawn
    still(objects, "old_chairs", 1, 5, oid="old_chairs")      # backs to the hearth
    stove(objects, 4)                                         # banked too; open at dawn
    place(objects, "table", 6, 2, oid="tea_table")
    place(objects, "stool", 8, 3, oid="tea_stool")
    place(objects, "rug", 4, 5, solid=False)
    place(objects, "bed", 10, 2)
    still(objects, "kin_basket", 10, 6, oid="bracken_basket")  # Old Bracken, by the bed
    still(objects, "wool_basket", 12, 2)
    still(objects, "wool_basket", 1, 7, oid="wool_b")
    npcs = [npc("old_edwy", (8, 6), "npc_old_man", "script.still_home_a_elder", facing="right"),
            npc("old_margery", (5, 3), "npc_old_woman", "script.still_home_a_wife", facing="right")]
    triggers = [{"id": "bracken_read", "kind": "script", "at": {"tx": 10, "ty": 6},
                 "activation": "interact", "ref": "script.still_home_a_basket"}]
    return mapdef("stillwater_home_a", "Margery and Edwy's Cottage", W, H, SHUTTER_SET, base, over,
                  objects, out_warp(door_x, H, 10, 25), triggers, npcs, HUSH_MUSIC)


def build_home_b():
    """Maren's house — TALL and divided the other way: a work-room with her
    spinning wheel and the screened hearth, and the child's own little room in
    the north-east corner behind a real wall and door (the candle sill there)."""
    W, H = 12, 11
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [9])
    partition_v(over, W, 7, 1, 5, lip="e")                   # the child's room, west wall
    partition_h(base, over, W, 6, 9, 10)                      # ...its south wall (door at x 8)
    objects: list = []
    place(objects, "bed", 9, 2, oid="child_bed")
    still(objects, "candle_sill", 8, 2, oid="candle_sill", solid=False).update(
        requires_flag="flag:q_still_candle_shown")
    hearth(objects, 2)                                        # screened; open at dawn
    wall_mount(objects, "shelf", 5)
    still(objects, "spinning_wheel", 1, 6)
    place(objects, "table", 4, 7, oid="table")
    place(objects, "stool", 6, 8)
    still(objects, "wool_basket", 1, 8)
    still(objects, "wool_basket", 10, 9, oid="wool_b")
    npcs = [npc("maren", (3, 5), "npc_parent", "script.still_maren", facing="down")]
    triggers = [{"id": "child_bed_read", "kind": "script", "at": {"tx": 8, "ty": 3},
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
