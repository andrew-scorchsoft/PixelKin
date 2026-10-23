#!/usr/bin/env python3
"""
PAUL'S HOUSE — the Booji-Wooji Man's crooked three-storey home on Wayward Rise
(2026-10). Content: src/game/content/regions/paul.ts. Art: tools/maps/paulforge.py
(drawn `paul_*` pieces) + the image-gen exterior (`paul_house`, `paul_bike`,
`paul_washing_line`), placed by build_wayward_rise.py.

Paul is the quiet wanderer at the dark lamp (S4) who walks the old wood (S5).
His house is the opposite of a mystery: it is ALL the evidence, and none of it
agrees. A lifetime of travel between the maple country across the northern
sea and the cape country far to the south, t-shirts from everywhere, a WANTED
poster he swears is a joke — and his granddaughter LOTTIE in the attic, who
loves the Chickenpig more than anything in the world (after you've caught it;
the Rise is only reachable after S5's waystone, which itself needs the catch).
Paul himself is never home: he's out walking. Never confirm the Registry story;
never say what the Booji-Wooji Man IS.

Three floors, warm register, roomkit (docs/world/interiors.md, binding). The
stairs alternate corners (the Old Light convention): every `up_stairs` /
`down_stairs` pad sits on row 2 in a north corner and lands ONE row below the
partner floor's own return stair (roomkit.finish dresses both with stair sprites).

  G  paul_house_1  16x11  THE KITCHEN-HALL  focal: the hearth (top-centre)
       west: the kitchen (stove, the tea bench with the kettle and the red tin of
       red-bush, Paul's NOTE on the table) behind a partition; east: the hall —
       the bike helmet + gym bag by the door, the carved antelope, Paul's chair by
       the fire. Wall: the pin-board of tickets, the WANTED poster, the sunny cape
       painting. Up-stair NE (14,2). Doormat (8,10) -> wayward_rise.
  1  paul_house_2  18x11  THE T-SHIRT MUSEUM  focal: the three rails (OUT / IN / NEVER)
       the north wall is shirts in frames (each a tiny story) between the maple
       country's snowy-lake painting, antlers and painted paddle; a partition_h
       makes the CAPE CORNER (south-west: protea, beadwork, the hooped jersey,
       the sunset over the flat-topped mountain, the rugby ball, the sticker
       trunk, a globe); the MAPLE CORNER east (the plaid jacket on its stand,
       the syrup tin). Down-stair NE (16,2), up-stair NW (1,2).
  2  paul_house_3  12x10  LOTTIE'S ATTIC  focal: the star window (top-centre)
       her drawings on the wall (two always; four Chickenpig ones once
       `flag:chickenpig_caught`), the Chickenpig PLUSH on the floor (same
       flag), her desk, the toy crates, and her bed in the nook behind the
       partition. LOTTIE stands mid-room (script.paul_lottie). Down-stair NW (1,2).

The Lottie scene stages on these tiles (keep them floor; audit_flow proves
reach, the shoot proves the scene): Lottie (5,5); the Chickenpig "visitor" NPC
(`kin_163_overworld`, flag:paul_lottie_cp_out) appears at (6,6) when you let
it out of your lamp (a `travel` re-entry onto the same map, so it spawns
mid-scene), and goes back in when the scene ends.

Run:  python3 tools/maps/build_paul_house.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, faced_room, finish, mapdef, obj,
                     partition_h, partition_v, place, wall_mount, windows)

MUSIC = "assets/audio/music/interior-sunny.mp3"
RISE_APPROACH = (4, 10)   # the tile below Paul's door on wayward_rise
G, M, A = "paul_house_1", "paul_house_2", "paul_house_3"
GW, MW, AW = 16, 18, 12


def corner_x(W: int, c: str) -> int:
    return W - 2 if c == "ne" else 1


def hang(objects, oid, stem, tx, ty=1, w=1):
    """A wall-hung paul_* piece ON a wall-face row (non-solid; the face collides)."""
    objects.append({"id": oid, "sprite": f"paul_{stem}", "at": {"tx": tx, "ty": ty},
                    "w": w, "h": 1, "solid": False})


def stand(objects, oid, stem, tx, ty, w, h, *, solid=True, **extra):
    o = {"id": oid, "sprite": f"paul_{stem}", "at": {"tx": tx, "ty": ty}, "w": w, "h": h}
    if not solid:
        o["solid"] = False
    o.update(extra)
    objects.append(o)
    return o


def sign(triggers, tid, x, y, ref, **extra):
    t = {"id": tid, "kind": "sign", "at": {"tx": x, "ty": y}, "activation": "interact",
         "ref": ref}
    t.update(extra)
    triggers.append(t)


def stair(warps, base, W, wid, corner, to_map, to_w):
    from roomkit import DOORMAT
    x = corner_x(W, corner)
    base[2 * W + x] = DOORMAT
    warps.append({"id": wid, "at": {"tx": x, "ty": 2}, "trigger": "step_on",
                  "to_map": to_map, "to": {"tx": corner_x(to_w, corner), "ty": 3},
                  "facing": "down", "transition": "fade"})


# ---- GROUND: the kitchen-hall -------------------------------------------------------------
def ground() -> dict:
    W, H, DOOR = GW, 11, 8
    base, over = faced_room(W, H, DOOR)
    objects, warps, triggers, npcs = [], [], [], []
    windows(over, W, [3, 4])                       # the kitchen window over the bench
    # the kitchen (west) — a partition with its open end at the top
    partition_v(over, W, 5, 5, 9, lip="w")
    wall_mount(objects, "stove", 1)                # cols 1-2, rows 1-2
    stand(objects, "tea_bench", "tea_bench", 3, 2, 2, 2)
    place(objects, "table", 2, 6, oid="kitchen_table")
    place(objects, "stool", 1, 7, oid="stool_a")
    place(objects, "barrels", 1, 9, oid="kitchen_barrels")
    place(objects, "plant", 4, 9, oid="kitchen_plant")
    # the wall: WANTED, the hearth (focal), the sunny cape, the pin-board
    hang(objects, "wanted", "wanted", 5)
    wall_mount(objects, "hearth", 7)               # cols 7-9, rows 1-3
    hang(objects, "painting_cape_day", "painting_cape_day", 10, w=2)
    hang(objects, "pinboard", "pinboard", 12, w=2)
    # the hall: Paul's chair by the fire, a rug, the antelope, the gym kit by the door
    objects.append(obj("paul_chair", "interior_armchair_green", 10, 3, 1, 2))
    place(objects, "rug", 7, 5, oid="hearth_rug", solid=False)
    stand(objects, "antelope", "antelope", 14, 5, 1, 2)
    stand(objects, "gym_kit", "gym_kit", 9, 9, 1, 1)
    place(objects, "plant", 14, 9, oid="hall_plant")
    stand(objects, "trunk", "trunk", 11, 9, 2, 1)
    stair(warps, base, W, "up_stairs", "ne", M, MW)
    warps.append({"id": "to_rise", "at": {"tx": DOOR, "ty": H - 1}, "trigger": "step_on",
                  "to_map": "wayward_rise",
                  "to": {"tx": RISE_APPROACH[0], "ty": RISE_APPROACH[1]},
                  "facing": "down", "transition": "door"})
    # first step inside: the welcome (banks flag:paul_house_seen -> the LORE entry)
    # (a band across the hall's whole width at row 8: you land on the doormat's
    # inner tile (8,9), and every way further in crosses row 8 east of the partition)
    for x in range(6, W - 1):
        triggers.append({"id": f"welcome_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 8},
                         "activation": "step_on", "ref": "script.paul_house_welcome",
                         "hidden_when_flag": "flag:paul_house_seen"})
    triggers.append({"id": "note", "kind": "cutscene", "at": {"tx": 2, "ty": 6},
                     "activation": "interact", "ref": "script.paul_note"})
    sign(triggers, "wanted", 5, 1, "sign.paul_wanted")
    sign(triggers, "pinboard_a", 12, 1, "sign.paul_pinboard")
    sign(triggers, "pinboard_b", 13, 1, "sign.paul_pinboard")
    sign(triggers, "cape_a", 10, 1, "sign.paul_cape_day")
    sign(triggers, "cape_b", 11, 1, "sign.paul_cape_day")
    sign(triggers, "tea", 3, 3, "sign.paul_tea")
    sign(triggers, "antelope", 14, 6, "sign.paul_antelope")
    sign(triggers, "gym_kit", 9, 9, "sign.paul_gym_kit")
    sign(triggers, "trunk", 11, 9, "sign.paul_trunk")
    sign(triggers, "chair", 10, 4, "sign.paul_chair")
    return mapdef(G, "Paul's House", W, H, WARM_SET, base, over, objects, warps,
                  triggers, npcs, MUSIC)


# ---- FIRST FLOOR: the T-shirt museum ------------------------------------------------------
SHIRTS_N = [("race", 2), ("sun", 3), ("ferry", 4), ("leaf", 5), ("gym", 6)]


def middle() -> dict:
    W, H = MW, 11
    base, over = faced_room(W, H, W // 2)
    # a tower floor has no bottom door: wall the doormat back up
    from roomkit import FLOOR, CAP_N
    base[(H - 1) * W + W // 2] = FLOOR
    over[(H - 1) * W + W // 2] = CAP_N
    objects, warps, triggers, npcs = [], [], [], []
    # the north wall: five framed shirts, the snowy lake, a lamp rack, antlers, the paddle
    for stem, x in SHIRTS_N:
        hang(objects, f"shirt_{stem}", f"shirt_{stem}", x)
        sign(triggers, f"shirt_{stem}", x, 1, f"sign.paul_shirt_{stem}")
    hang(objects, "lake", "painting_lake", 7, w=2)
    wall_mount(objects, "lamp_rack", 9, solid=False)    # cols 9-10
    hang(objects, "antlers", "antlers", 11, w=2)
    hang(objects, "paddle", "paddle", 13, w=2)
    windows(over, W, [15])
    for x in (7, 8):
        sign(triggers, f"lake_{x}", x, 1, "sign.paul_lake")
    for x in (11, 12):
        sign(triggers, f"antlers_{x}", x, 1, "sign.paul_antlers")
    for x in (13, 14):
        sign(triggers, f"paddle_{x}", x, 1, "sign.paul_paddle")
    # the centrepiece: THREE RAILS, one per category of shirt — OUT (safe to be
    # seen in), IN (house only) and NEVER (roped off). Each wears its category
    # board on the bar (the overhang row) and runs a "hold one up" menu.
    for rid, x in (("out", 2), ("in", 6), ("never", 11)):
        stand(objects, f"rack_{rid}", f"rack_{rid}", x, 2, 3, 3, overhang=1, walk_under=True)
        triggers.append({"id": f"rack_{rid}", "kind": "cutscene", "at": {"tx": x + 1, "ty": 4},
                         "activation": "interact", "ref": f"script.paul_rail_{rid}"})
    # the display table: the folded ones, too precious to hang
    place(objects, "table", 14, 3, oid="folded_table")
    sign(triggers, "folded", 14, 4, "sign.paul_folded")
    # the CAPE CORNER (south-west): a partition_h with a door gap at col 5
    face = partition_h(base, over, W, 7, 1, 9, doors=(5,))
    hang(objects, "protea", "painting_protea", 1, ty=face)
    hang(objects, "beadwork", "beadwork", 2, ty=face)
    hang(objects, "shirt_stripe", "shirt_stripe", 3, ty=face)
    hang(objects, "shirt_boat", "shirt_boat", 4, ty=face)
    hang(objects, "sunset", "painting_cape", 6, ty=face, w=2)
    hang(objects, "shirt_star", "shirt_star", 8, ty=face)
    for stem, x in (("protea", 1), ("beadwork", 2), ("shirt_stripe", 3), ("shirt_boat", 4),
                    ("shirt_star", 8)):
        sign(triggers, f"c_{stem}", x, face, f"sign.paul_{stem}")
    for x in (6, 7):
        sign(triggers, f"sunset_{x}", x, face, "sign.paul_sunset")
    stand(objects, "rugby", "rugby_stand", 1, 9, 1, 1)
    stand(objects, "trunk", "trunk", 6, 9, 2, 1)
    stand(objects, "globe", "globe", 3, 9, 1, 1)
    place(objects, "brazier", 9, 8, oid="cape_brazier")
    sign(triggers, "rugby", 1, 9, "sign.paul_rugby")
    sign(triggers, "trunk_m", 6, 9, "sign.paul_trunk_stickers")
    sign(triggers, "globe", 3, 9, "sign.paul_globe")
    # the MAPLE CORNER (east): the plaid jacket, the syrup tin, a rug
    stand(objects, "coat_stand", "coat_stand", 15, 5, 1, 2)
    stand(objects, "syrup", "syrup_table", 13, 8, 1, 1)
    place(objects, "rug", 11, 6, oid="maple_rug", solid=False)
    place(objects, "stool", 12, 8, oid="maple_stool")
    place(objects, "plant", 16, 9, oid="maple_plant")
    sign(triggers, "coat", 15, 6, "sign.paul_plaid")
    sign(triggers, "syrup", 13, 8, "sign.paul_syrup")
    # the museum's opening placard, by the stair-head
    triggers.append({"id": "placard", "kind": "cutscene", "at": {"tx": 16, "ty": 3},
                     "activation": "step_on", "ref": "script.paul_museum",
                     "hidden_when_flag": "flag:paul_museum_seen"})
    stair(warps, base, W, "down_stairs", "ne", G, GW)
    stair(warps, base, W, "up_stairs", "nw", A, AW)
    return mapdef(M, "Paul's House — The T-Shirt Museum", W, H, WARM_SET, base, over,
                  objects, warps, triggers, npcs, MUSIC)


# ---- TOP: Lottie's attic ------------------------------------------------------------------
CP = "flag:chickenpig_caught"


def attic() -> dict:
    W, H = AW, 10
    base, over = faced_room(W, H, W // 2)
    from roomkit import FLOOR, CAP_N
    base[(H - 1) * W + W // 2] = FLOOR
    over[(H - 1) * W + W // 2] = CAP_N
    objects, warps, triggers, npcs = [], [], [], []
    # the focal: the star window, top-centre
    objects.append({"id": "star_window", "sprite": "interior_star_window",
                    "at": {"tx": 5, "ty": 1}, "w": 2, "h": 3, "overhang": 1,
                    "walk_under": True})
    # her drawings: two always; four Chickenpig ones once it's caught
    hang(objects, "draw_bike", "drawing_bike", 2)
    hang(objects, "draw_sea", "drawing_sea", 3)
    sign(triggers, "draw_bike", 2, 1, "sign.paul_drawing_bike")
    sign(triggers, "draw_sea", 3, 1, "sign.paul_drawing_sea")
    for stem, x in (("a", 4), ("b", 7), ("c", 8), ("d", 9)):
        o = {"id": f"cp_{stem}", "sprite": f"paul_cp_drawing_{stem}",
             "at": {"tx": x, "ty": 1}, "w": 1, "h": 1, "solid": False, "requires_flag": CP}
        objects.append(o)
        sign(triggers, f"cp_{stem}", x, 1, f"sign.paul_cp_drawing_{stem}", requires_flag=CP)
    windows(over, W, [10])
    # the bed nook (east), behind a partition open at the top
    partition_v(over, W, 8, 5, 8, lip="e")
    place(objects, "bed", 9, 5, oid="lottie_bed")
    sign(triggers, "bed", 9, 5, "sign.paul_lottie_bed")
    # her corner: the desk with crayons, the toy crates, a rug, the plush (after)
    place(objects, "desk", 1, 5, oid="lottie_desk")
    sign(triggers, "desk", 1, 5, "sign.paul_lottie_desk")
    place(objects, "crates", 1, 7, oid="toy_crates")
    sign(triggers, "toys", 1, 7, "sign.paul_lottie_toys")
    place(objects, "rug", 4, 6, oid="attic_rug", solid=False)
    stand(objects, "plush", "plush", 7, 8, 1, 1, solid=False, requires_flag=CP)
    sign(triggers, "plush", 7, 8, "sign.paul_plush", requires_flag=CP)
    place(objects, "plant", 10, 2, oid="attic_plant")
    npcs.append({"id": "lottie", "at": {"tx": 5, "ty": 5}, "facing": "down",
                 "sprite": "npc_girl", "movement": "static",
                 "dialogue_ref": "script.paul_lottie"})
    # the Chickenpig, out of your lamp for a visit (the scene's travel re-entry
    # spawns it; it goes back in when the scene clears the flag)
    npcs.append({"id": "lottie_cp", "at": {"tx": 6, "ty": 6}, "facing": "left",
                 "sprite": "kin_163_overworld", "movement": "static",
                 "dialogue_ref": "script.paul_lottie",
                 "requires_flag": "flag:paul_lottie_cp_out"})
    stair(warps, base, W, "down_stairs", "nw", M, MW)
    return mapdef(A, "Paul's House — Lottie's Attic", W, H, WARM_SET, base, over,
                  objects, warps, triggers, npcs, MUSIC)


if __name__ == "__main__":
    ok = all([finish(ground()), finish(middle()), finish(attic())])
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
