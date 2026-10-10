#!/usr/bin/env python3
"""
THE OLD LIGHT ("the Guffaw") — Pearlmoor's second lighthouse, seven floors (R9).

Eleven winters ago Reyl Wash took the lamp out of this tower and put Tam's
clockwork joke-engine, MR. PUNCHWHEEL, where the light had been. The climb is
the middle leg of the Causeway Bell chain (walkthrough/01-south.md): Reyl's hook
sets flag:q_south_bell (opens the door on Lightkeeper's Point) -> seven floors of
increasingly strange jokes -> the top floor sets flag:picked_net_floats +
flag:q_south_jest_done -> the netmender's rope.

Tower pattern = the Beacon's (build_beacon.py), rebuilt on roomkit: stair rooms
whose stairs ALTERNATE corners floor by floor (a spiral read), each up-stair a
step_on warp gated on that floor's `flag:oldlight_N_solved` with a stair-gate
`blocked_ref`. The riddle runs as a step_on cutscene band on the ONE walkable
approach tile below the up-stair (the speaking-tube object blocks the side
approach) and as an interact on the speaking-tube itself; both vanish once
solved (hidden_when_flag) and the tube gets a post-solve line. Down-stairs are
always open; solved flags persist. No wild encounters anywhere.

  F1 pearlmoor_oldlight_1   The Lobby of Groaners   warm  up NE   (door below)
  F2 pearlmoor_oldlight_2   The Late Laugh          cool  dn NE / up NW  — the HECKLER
  F3 pearlmoor_oldlight_3   Intermission            warm  dn NW / up NE  — tea-urn REST
  F4 pearlmoor_oldlight_4   The Backwards Inn       cool  dn NE / up NW  — the RINGMASTER
  F5 pearlmoor_oldlight_5   The Gallery of Confident Facts  cool  dn NW / up NE
  F6 pearlmoor_oldlight_6   The One Joke            warm  dn NE / up NW  (no gate)
  TOP pearlmoor_oldlight_top The Winding Room       warm  dn NW + the SLIDE

Every stair pair lands ON the partner floor's own return stair column, one row
below it (the Beacon convention). The top's SLIDE (7,9) drops to the Point
(7,8); the Point's chute-mouth (7,7) climbs back up to (7,8) here.

Run:  python3 tools/maps/build_pearlmoor_oldlight.py
"""
from __future__ import annotations

from roomkit import (COOL_SET, WARM_SET, DOORMAT, FLOOR, CAP_N, WINDOW,
                     aisle_runner, faced_room, finish, mapdef, partition_h,
                     partition_v, place, wall_mount, windows)

STAGE = "assets/audio/music/sunken-solarium-a.mp3"
GALLERY = "assets/audio/music/sunken-solarium-c.mp3"
ATTIC = "assets/audio/music/pearlmoor-quay-c.mp3"

POINT_DOOR = (3, 7)       # the Old Light's door on pearlmoor_point
TUBE = "solarium_sun_mask"  # Punchwheel's brass speaking-tube mouth (1x1)


def mid(n: int) -> str:
    return "pearlmoor_oldlight_top" if n == 7 else f"pearlmoor_oldlight_{n}"


def corner_x(W: int, c: str) -> int:
    return W - 2 if c == "ne" else 1


def shell(W, H, tileset, *, door=False):
    base, over = faced_room(W, H, W // 2)
    if not door:  # a tower floor has no bottom door: wall the doormat back up
        base[(H - 1) * W + W // 2] = FLOOR
        over[(H - 1) * W + W // 2] = CAP_N
    return base, over


def stairs(n, W, base, objects, warps, triggers, *, down, up, gate=True,
           band_requires=None, band_blocked=None, partner_w=None):
    """Lay floor n's stair pads + warps (+ the riddle band and the tube)."""
    pw = partner_w or {}
    if down:
        dx = corner_x(W, down)
        base[2 * W + dx] = DOORMAT
        lw = pw.get(n - 1, 14)
        warps.append({"id": "down_stairs", "at": {"tx": dx, "ty": 2}, "trigger": "step_on",
                      "to_map": mid(n - 1), "to": {"tx": corner_x(lw, down), "ty": 3},
                      "facing": "down", "transition": "fade"})
    if up:
        ux = corner_x(W, up)
        base[2 * W + ux] = DOORMAT
        uw = pw.get(n + 1, 14)
        w = {"id": "up_stairs", "at": {"tx": ux, "ty": 2}, "trigger": "step_on",
             "to_map": mid(n + 1), "to": {"tx": corner_x(uw, up), "ty": 3},
             "facing": "down", "transition": "fade"}
        if gate:
            w["requires_flag"] = f"flag:oldlight_{n}_solved"
            w["blocked_ref"] = "sign.oldlight_stairgate"
        warps.append(w)
        # the speaking-tube beside the stair (blocks the side approach, so the
        # stair is reached only across the band tile below it)
        tx = ux - 1 if up == "ne" else ux + 1
        objects.append({"id": "speaking_tube", "sprite": TUBE,
                        "at": {"tx": tx, "ty": 2}, "w": 1, "h": 1})
        if gate:
            band = {"id": "riddle_band", "kind": "cutscene", "at": {"tx": ux, "ty": 3},
                    "activation": "step_on", "ref": f"script.oldlight_{n}",
                    "hidden_when_flag": f"flag:oldlight_{n}_solved"}
            tube = {"id": "tube", "kind": "cutscene", "at": {"tx": tx, "ty": 2},
                    "activation": "interact", "ref": f"script.oldlight_{n}",
                    "hidden_when_flag": f"flag:oldlight_{n}_solved"}
            if band_requires:
                for t in (band, tube):
                    t["requires_flag"] = band_requires
                    t["blocked_ref"] = band_blocked
            triggers += [band, tube,
                         {"id": "tube_after", "kind": "dialogue", "at": {"tx": tx, "ty": 2},
                          "activation": "interact", "ref": f"npc.oldlight_tube_{n}",
                          "requires_flag": f"flag:oldlight_{n}_solved"}]
        else:
            triggers.append({"id": "tube", "kind": "cutscene", "at": {"tx": tx, "ty": 2},
                             "activation": "interact", "ref": f"script.oldlight_{n}"})


def sign_at(triggers, tid, x, y, ref, kind="sign"):
    triggers.append({"id": tid, "kind": kind, "at": {"tx": x, "ty": y},
                     "activation": "interact", "ref": ref})


def trainer(npcs, tid, x, y, facing, sprite):
    flag = f"flag:oldlight_{tid}_beaten"
    npcs += [
        {"id": tid, "at": {"tx": x, "ty": y}, "facing": facing, "sprite": sprite,
         "movement": "static", "dialogue_ref": f"script.oldlight_{tid}",
         "defeated_flag": flag, "hidden_when_flag": flag},
        {"id": f"{tid}_after", "at": {"tx": x, "ty": y}, "facing": facing, "sprite": sprite,
         "movement": "look_around", "dialogue_ref": f"npc.oldlight_{tid}_after",
         "requires_flag": flag},
    ]
    return flag


# ---- F1: The Lobby of Groaners ----------------------------------------------------------
def floor_1():
    W, H = 14, 11
    base, over = shell(W, H, WARM_SET, door=True)
    objects, warps, triggers, npcs = [], [], [], []
    # the CLOAKROOM west (rooms within the room): coats nobody came back for
    partition_v(over, W, 4, 2, 5, lip="w")
    objects.append({"id": "coats", "sprite": "solarium_costume_rack",
                    "at": {"tx": 1, "ty": 2}, "w": 2, "h": 2})
    place(objects, "plant", 3, 5, oid="cloak_plant")
    place(objects, "stool", 1, 6, oid="cloak_stool")
    # the BOX OFFICE counter, top-centre: the focal point
    place(objects, "counter", 5, 2, oid="box_office")
    wall_mount(objects, "banner_warm", 5, oid="banner_l", solid=False)
    wall_mount(objects, "banner_warm", 8, oid="banner_r", solid=False)
    windows(over, W, [10])
    # THE PLAQUE on the face beside the box office (who wrote every joke here)
    sign_at(triggers, "plaque", 9, 1, "sign.oldlight_plaque")
    sign_at(triggers, "box_office_sign", 6, 3, "sign.oldlight_box_office")
    # lobby benches + the aisle in from the door
    aisle_runner(objects, 7, 4, 9)
    place(objects, "pew", 3, 7, oid="bench_l")
    place(objects, "pew", 9, 7, oid="bench_r")
    place(objects, "brazier", 5, 8, oid="brazier_l")
    place(objects, "brazier", 9, 8, oid="brazier_r")
    warps.append({"id": "to_point", "at": {"tx": W // 2, "ty": H - 1}, "trigger": "step_on",
                  "to_map": "pearlmoor_point", "to": {"tx": POINT_DOOR[0], "ty": POINT_DOOR[1] + 1},
                  "facing": "down", "transition": "door"})
    stairs(1, W, base, objects, warps, triggers, down=None, up="ne")
    # Punchwheel's welcome rolls once, three steps in from the door
    triggers.append({"id": "welcome", "kind": "cutscene", "at": {"tx": 7, "ty": 8},
                     "activation": "step_on", "ref": "script.oldlight_welcome",
                     "hidden_when_flag": "flag:oldlight_welcomed"})
    return mapdef(mid(1), "The Old Light — The Lobby of Groaners", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs, STAGE)


# ---- F2: The Room That Laughs a Beat Too Late --------------------------------------------
def floor_2():
    W, H = 14, 11
    base, over = shell(W, H, COOL_SET)
    objects, warps, triggers, npcs = [], [], [], []
    # the little STAGE top-centre, braziers as footlights
    objects.append({"id": "stage", "sprite": "solarium_stage_arch",
                    "at": {"tx": 5, "ty": 2}, "w": 5, "h": 3})
    place(objects, "brazier", 4, 3, oid="footlight_l")
    place(objects, "brazier", 10, 3, oid="footlight_r")
    wall_mount(objects, "banner_ice", 3, oid="curtain_l", solid=False)
    wall_mount(objects, "banner_ice", 11, oid="curtain_r", solid=False)
    # the WINGS (east): a partition with the prop store behind it
    partition_v(over, W, 10, 6, 9, lip="e")
    place(objects, "crates", 11, 7, oid="props")
    # the pews and the audience that laughs one line late
    place(objects, "pew", 2, 6, oid="pew_a")
    place(objects, "pew", 6, 6, oid="pew_b")
    place(objects, "pew", 2, 8, oid="pew_c")
    place(objects, "pew", 6, 8, oid="pew_d")
    for nid, x, y, spr in (("late_a", 3, 7, "npc_old_woman"), ("late_b", 7, 7, "npc_man"),
                           ("late_c", 8, 9, "npc_boy")):
        npcs.append({"id": nid, "at": {"tx": x, "ty": y}, "facing": "up", "sprite": spr,
                     "movement": "static", "dialogue_ref": f"npc.oldlight_{nid}"})
    stairs(2, W, base, objects, warps, triggers, down="ne", up="nw",
           band_requires="flag:oldlight_heckler_beaten",
           band_blocked="npc.oldlight_heckler_block")
    trainer(npcs, "heckler", 2, 3, "left", "npc_man")
    return mapdef(mid(2), "The Old Light — The Late Laugh", W, H, COOL_SET,
                  base, over, objects, warps, triggers, npcs, STAGE)


# ---- F3: Intermission (the soft floor, the tea-urn, the Hall of Mouths) ---------------------
def floor_3():
    W, H = 14, 11
    base, over = shell(W, H, WARM_SET)
    objects, warps, triggers, npcs = [], [], [], []
    # the INTERVAL BAR west (you arrive in it): the tea-urn automaton + a stool
    partition_v(over, W, 4, 2, 6, lip="w")
    objects.append({"id": "tea_urn", "sprite": "tideglass_lens_lit",
                    "at": {"tx": 1, "ty": 5}, "w": 2, "h": 2})
    for y in (5, 6):
        sign_at(triggers, f"urn_{y}", 2, y, "script.oldlight_urn", kind="cutscene")
    place(objects, "stool", 3, 8, oid="bar_stool")
    # the soft furniture with faces and opinions
    wall_mount(objects, "stove", 6)            # the stove that laughs first
    wall_mount(objects, "bookcase", 8)         # the bookcase that clears its throat
    windows(over, W, [5, 10])
    place(objects, "table", 6, 6, oid="table")
    place(objects, "stool", 5, 7, oid="stool_l")
    place(objects, "stool", 8, 7, oid="stool_r")
    place(objects, "sacks", 10, 9, oid="sacks")
    sign_at(triggers, "stove", 6, 2, "npc.oldlight_stove")
    sign_at(triggers, "stove_b", 7, 2, "npc.oldlight_stove")
    sign_at(triggers, "bookcase", 8, 3, "npc.oldlight_bookcase")
    sign_at(triggers, "bookcase_b", 9, 3, "npc.oldlight_bookcase")
    sign_at(triggers, "p_note", 6, 6, "sign.oldlight_p_note")
    # the three escaped PUNCHLINES, loose in the room
    for nid, x, y, spr in (("punch_tuesday", 10, 5, "npc_girl"),
                           ("punch_buns", 3, 7, "npc_child"),
                           ("punch_ladder", 9, 8, "npc_boy")):
        npcs.append({"id": nid, "at": {"tx": x, "ty": y}, "facing": "down", "sprite": spr,
                     "movement": "look_around", "dialogue_ref": f"npc.oldlight_{nid}"})
    stairs(3, W, base, objects, warps, triggers, down="nw", up="ne")
    return mapdef(mid(3), "The Old Light — Intermission", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs, STAGE)


# ---- F4: The Backwards Inn (the lobby, mirrored) -----------------------------------------
def floor_4():
    W, H = 14, 11
    base, over = shell(W, H, COOL_SET)
    objects, warps, triggers, npcs = [], [], [], []
    # the lobby turned inside out: the cloakroom is EAST now, the counter faces the wall
    partition_v(over, W, 9, 2, 5, lip="e")
    objects.append({"id": "coats", "sprite": "solarium_costume_rack",
                    "at": {"tx": 10, "ty": 4}, "w": 2, "h": 2})
    place(objects, "counter", 5, 2, oid="box_office")
    wall_mount(objects, "banner_warm", 5, oid="banner_l", solid=False)
    wall_mount(objects, "banner_warm", 8, oid="banner_r", solid=False)
    sign_at(triggers, "backwards_a", 4, 1, "sign.oldlight_backwards_a")
    sign_at(triggers, "backwards_b", 7, 3, "sign.oldlight_backwards_b")
    aisle_runner(objects, 7, 4, 9)
    place(objects, "pew", 3, 7, oid="bench_l")
    place(objects, "pew", 9, 6, oid="bench_r")
    place(objects, "table", 10, 8, oid="carved_table")
    sign_at(triggers, "reassess", 5, 3, "sign.oldlight_reassess")
    sign_at(triggers, "reassess_b", 8, 3, "sign.oldlight_reassess")
    objects.append({"id": "troupe_cart", "sprite": "solarium_troupe_cart",
                    "at": {"tx": 2, "ty": 5}, "w": 3, "h": 2})
    sign_at(triggers, "troupe_cart", 4, 5, "npc.oldlight_cart")
    sign_at(triggers, "box_office_sign", 6, 3, "script.oldlight_lamps_out", kind="cutscene")
    # the floor's opener plays once on the only way out of the east cloakroom
    triggers.append({"id": "backwards_opener", "kind": "cutscene", "at": {"tx": 12, "ty": 5},
                     "activation": "step_on", "ref": "script.oldlight_backwards",
                     "hidden_when_flag": "flag:oldlight_4_opened"})
    place(objects, "brazier", 5, 8, oid="brazier_l")
    place(objects, "brazier", 8, 8, oid="brazier_r")
    stairs(4, W, base, objects, warps, triggers, down="ne", up="nw",
           band_requires="flag:oldlight_ringmaster_beaten",
           band_blocked="npc.oldlight_ringmaster_block")
    trainer(npcs, "ringmaster", 2, 3, "left", "npc_shopkeeper")
    return mapdef(mid(4), "The Old Light — The Backwards Inn", W, H, COOL_SET,
                  base, over, objects, warps, triggers, npcs, STAGE)


# ---- F5: The Gallery of Confident Facts --------------------------------------------------
def floor_5():
    W, H = 14, 11
    base, over = shell(W, H, COOL_SET)
    objects, warps, triggers, npcs = [], [], [], []
    # a hanging wall splits the gallery: the back room north, the front south
    partition_h(base, over, W, 6, 1, 8, doors=(4,))
    # six framed captions: three on the north face, three on the partition face
    frames = [("cap_reyl", 3, 1, "banner_warm"), ("cap_tuesday", 6, 1, "banner_ice"),
              ("cap_stars", 9, 1, None), ("cap_sea", 2, 6, "banner_ice"),
              ("cap_gerald", 5, 6, "banner_warm"), ("cap_tam", 7, 6, "banner_warm")]
    for fid, x, y, stem in frames:
        if stem:
            wall_mount(objects, stem, x, face_row=y, oid=f"frame_{fid}", solid=False)
        else:  # the solid-black picture
            objects.append({"id": f"frame_{fid}", "sprite": "nightreach_star_banner",
                            "at": {"tx": x, "ty": y}, "w": 1, "h": 2, "solid": False})
        sign_at(triggers, fid, x, y, f"sign.oldlight_{fid}")
    place(objects, "brazier", 5, 2, oid="brazier_n")
    place(objects, "brazier", 10, 7, oid="brazier_s")
    place(objects, "pew", 4, 8, oid="viewing_bench")
    place(objects, "plant", 12, 9, oid="plant")
    # (Punchwheel's never-told joke — the knock-knock loop — opens the riddle
    #  itself, once: script.oldlight_5 guards it on flag:oldlight_knock_done)
    stairs(5, W, base, objects, warps, triggers, down="nw", up="ne",
           partner_w={6: 12})
    return mapdef(mid(5), "The Old Light — The Gallery of Confident Facts", W, H, COOL_SET,
                  base, over, objects, warps, triggers, npcs, GALLERY)


# ---- F6: The One Joke (almost empty; the music drops out) --------------------------------
def floor_6():
    W, H = 12, 9
    base, over = shell(W, H, WARM_SET)
    objects, warps, triggers, npcs = [], [], [], []
    windows(over, W, [6])
    partition_v(over, W, 4, 2, 4, lip="w")      # the coat alcove
    objects.append({"id": "coat_peg", "sprite": "solarium_costume_rack",
                    "at": {"tx": 2, "ty": 4}, "w": 2, "h": 2})
    sign_at(triggers, "coat", 2, 5, "sign.oldlight_coat")
    sign_at(triggers, "coat_b", 3, 5, "sign.oldlight_coat")
    place(objects, "table", 6, 4, oid="two_cups")
    place(objects, "stool", 5, 5, oid="stool_l")
    place(objects, "stool", 8, 5, oid="stool_r")
    sign_at(triggers, "cups", 6, 4, "sign.oldlight_cups")
    sign_at(triggers, "cups_b", 7, 4, "sign.oldlight_cups")
    sign_at(triggers, "window", 6, 1, "sign.oldlight_window")
    stairs(6, W, base, objects, warps, triggers, down="ne", up="nw", gate=False,
           partner_w={5: 14, 7: 14})
    # the loop: one band across the room's only crossing (every walkable tile
    # of column 9's run between the arrival stair and the rest of the room)
    for y in range(2, H - 1):
        triggers.append({"id": f"one_joke_{y}", "kind": "cutscene", "at": {"tx": 9, "ty": y},
                         "activation": "step_on", "ref": "script.oldlight_one_joke",
                         "hidden_when_flag": "flag:oldlight_6_heard"})
    return mapdef(mid(6), "The Old Light — The One Joke", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs, None)


# ---- TOP: The Winding Room ---------------------------------------------------------------
def floor_top():
    W, H = 14, 11
    base, over = shell(W, H, WARM_SET)
    objects, warps, triggers, npcs = [], [], [], []
    # MR. PUNCHWHEEL, half-stopped: the great winding drum + his brass face
    objects.append({"id": "punchwheel_drum", "sprite": "galehigh_winch",
                    "at": {"tx": 5, "ty": 2}, "w": 4, "h": 5})
    objects.append({"id": "punchwheel_face", "sprite": TUBE,
                    "at": {"tx": 9, "ty": 2}, "w": 1, "h": 1})
    for x in range(5, 10):
        sign_at(triggers, f"drum_{x}", x, 6 if x < 9 else 2, "script.oldlight_top",
                kind="cutscene")
    for t in triggers:
        t["hidden_when_flag"] = "flag:q_south_jest_done"
    for x in range(5, 10):
        triggers.append({"id": f"drum_after_{x}", "kind": "dialogue",
                         "at": {"tx": x, "ty": 6 if x < 9 else 2}, "activation": "interact",
                         "ref": "npc.oldlight_punchwheel_after",
                         "requires_flag": "flag:q_south_jest_done"})
    # the reveal fires on the approach: every walkable tile of row 7 under the drum
    for x in range(5, 9):
        triggers.append({"id": f"reveal_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 7},
                         "activation": "step_on", "ref": "script.oldlight_top",
                         "hidden_when_flag": "flag:q_south_jest_done"})
    # the sill with the old rope, the keeper's cubby with Reyl's log
    windows(over, W, [3])
    sign_at(triggers, "rope_sill", 3, 1, "sign.oldlight_rope")
    partition_v(over, W, 10, 5, 9, lip="e")
    place(objects, "table", 11, 6, oid="log_table")
    place(objects, "stool", 11, 8, oid="log_stool")
    for x in (11, 12):
        sign_at(triggers, f"log_{x}", x, 6, "script.oldlight_log", kind="cutscene")
    wall_mount(objects, "lamp_rack", 11, solid=False)
    place(objects, "brazier", 3, 7, oid="brazier_w")
    place(objects, "oil_jars", 1, 9, oid="jars")
    stairs(7, W, base, objects, warps, triggers, down="nw", up=None)
    # THE SLIDE: the tower's last joke — a chute down to the Point
    base[9 * W + 7] = DOORMAT
    warps.append({"id": "slide", "at": {"tx": 7, "ty": 9}, "trigger": "step_on",
                  "to_map": "pearlmoor_point", "to": {"tx": 7, "ty": 8},
                  "facing": "down", "transition": "fade",
                  "requires_flag": "flag:q_south_jest_done",
                  "blocked_ref": "sign.oldlight_slide_shut"})
    return mapdef(mid(7), "The Old Light — The Winding Room", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs, ATTIC)


def all_maps():
    return [floor_1(), floor_2(), floor_3(), floor_4(), floor_5(), floor_6(), floor_top()]


if __name__ == "__main__":
    ok = True
    for m in all_maps():
        if m.get("music") is None:
            del m["music"]  # F6: the bed carries up from F5 and the band fades it out
        ok = finish(m) and ok
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
