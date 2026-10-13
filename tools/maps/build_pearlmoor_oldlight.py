#!/usr/bin/env python3
"""
THE OLD LIGHT ("the Guffaw") — Pearlmoor's second lighthouse, seven floors (R9, R10).

Eleven winters ago Reyl Wash took the lamp out of this tower and put Tam's
clockwork joke-engine, MR. PUNCHWHEEL, where the light had been. The climb is
the middle leg of the Causeway Bell chain (walkthrough/01-south.md): Reyl's hook
sets flag:q_south_bell (opens the door on Lightkeeper's Point) -> seven floors of
increasingly strange jokes -> the top floor sets flag:picked_net_floats +
flag:q_south_jest_done -> the netmender's rope.

R10 (2026-10, playtest: "the ground floor was empty and not a funny place"):
the floors are BIG now (22x15, the haunted-tower pattern) and every one makes
you WALK it. You arrive in one north corner; the way up is in the other; a
divider splits the north strip and a long wall splits it from the hall below,
so the climb runs arrival room -> side door -> the hall -> far door -> the
stair room (F1: in from the street door, west and up, then east along the top).
The HALL carries the floor's wild encounters (a whimsical tower table rising
10 -> 15, the grind bed before the fen's 16s) and an optional sight trainer
waiting in an ALCOVE off the main line (step into its mouth and they see you).
Rest points: the tea-urn (F3), its backwards twin beside the Ringmaster (F4) and the two cups (F6). Each floor wears its
own warped tileset (oldlight_fN_set, build_oldlight_sets.py — the same gids as
the interior kits, more deranged the higher you go), its own Punchwheel cue
(oldlight-fN.mp3, more unhinged per floor) and the drawn joke props of
oldlightforge.py (`oldlight_*`).

Tower mechanics are unchanged: stairs ALTERNATE corners (a spiral read), each
up-stair a step_on warp gated on `flag:oldlight_N_solved` with a stair-gate
`blocked_ref`; the riddle runs as a step_on band on the ONE walkable tile below
the up-stair (the speaking-tube blocks the side) and as an interact on the
tube; both vanish once solved. Down-stairs are always open; solved flags persist.

  F1 The Lobby of Groaners          f1 (warm)  up NE   (street door below)
  F2 The Late Laugh                 f2 (cool)  dn NE / up NW  — the HECKLER (gate)
  F3 Intermission                   f3 (warm)  dn NW / up NE  — tea-urn REST + the COMPUTER
  F4 The Backwards Inn              f4 (cool)  dn NE / up NW  — the RINGMASTER (gate)
  F5 The Gallery of Confident Facts f5 (cool)  dn NW / up NE
  F6 The One Joke                   f6 (warm)  dn NE / up NW  (no gate) — the two-cups REST
  TOP The Winding Room              f7 (warm)  dn NW + the SLIDE

Run:  python3 tools/maps/build_pearlmoor_oldlight.py
"""
from __future__ import annotations

from pathlib import Path

from roomkit import (COOL_SET, WARM_SET, DOORMAT, FLOOR, CAP_N, WINDOW,
                     aisle_runner, faced_room, finish, mapdef, partition_h,
                     partition_v, place, wall_mount, windows)

REPO = Path(__file__).resolve().parents[2]
POINT_DOOR = (3, 7)       # the Old Light's door on pearlmoor_point
TUBE = "solarium_sun_mask"  # Punchwheel's brass speaking-tube mouth (1x1)

W, H = 22, 15             # the big floors (the top stays 14x11)
MID = 7                   # the long wall's FACE row (its band is row 6)
NDIV = W // 2             # the north strip's divider column
WEST_DOOR, EAST_DOOR = 3, W - 4
HALL = (1, MID + 1, W - 2, H - 2 - MID)  # rect of the hall below the long wall


def music(n: int) -> str:
    return f"assets/audio/music/oldlight-f{n}.mp3"


def tileset(n: int, base: dict) -> dict:
    """The floor's warped kit (same gids as `base`). Falls back to the plain kit
    only if the warped sidecar hasn't been drawn yet (fresh checkout mid-build)."""
    name = f"oldlight_f{n}_set"
    if not (REPO / f"public/assets/tilesets/{name}.tileset.json").is_file():
        return base
    return dict(base, name=name, image=f"assets/tilesets/{name}.webp")


def mid(n: int) -> str:
    return "pearlmoor_oldlight_top" if n == 7 else f"pearlmoor_oldlight_{n}"


def corner_x(w: int, c: str) -> int:
    return w - 2 if c == "ne" else 1


# --- the drawn joke kit (oldlightforge.py): stem -> (w, h, mount) ---------------------------
OL = {
    "jack_box": (1, 1, "free"), "rubber_chickens": (1, 2, "free"), "pie_table": (2, 1, "free"),
    "clown_shoes": (2, 1, "free"), "joke_lectern": (1, 2, "free"), "mallet": (1, 2, "free"),
    "laugh_dolls": (2, 2, "free"), "laugh_meter": (1, 2, "free"), "teacups": (1, 2, "free"),
    "unicycle": (1, 2, "free"), "spring_can": (1, 1, "free"), "upside_chair": (1, 1, "free"),
    "spotlight": (1, 2, "free"), "cog_heap": (2, 1, "free"), "tea_urn": (2, 2, "free"),
    "whoopee": (1, 1, "decal"), "banana": (1, 1, "decal"), "confetti": (1, 1, "decal"),
    "mask_wall": (1, 1, "hung"), "applause_sign": (2, 1, "hung"), "bunting": (2, 1, "hung"),
    "clock_backwards": (1, 1, "hung"), "funhouse_mirror": (1, 2, "wall"),
    "wax_shine": (1, 1, "decal"), "wax_shine_b": (1, 1, "decal"),
}


def ol(objects, stem, x, y, oid=None):
    """Place an oldlightforge piece by its contract footprint + mount class."""
    w, h, mount = OL[stem]
    o = {"id": oid or stem, "sprite": f"oldlight_{stem}", "at": {"tx": x, "ty": y}, "w": w, "h": h}
    if mount in ("decal", "hung"):
        o["solid"] = False
    elif mount == "wall":  # stands against the wall: top row drawn over the face
        o["overhang"] = 1
        o["walk_under"] = True
    objects.append(o)
    return o


def shell(tileset_, *, door=False, w=W, h=H):
    base, over = faced_room(w, h, w // 2)
    if not door:  # a tower floor has no street door: wall the doormat back up
        base[(h - 1) * w + w // 2] = FLOOR
        over[(h - 1) * w + w // 2] = CAP_N
    return base, over


def tower_walls(base, over, *, f1=False):
    """The haunted-tower plan: a long wall splits the north strip from the hall
    (doors at both ends — or only the west one on F1), and a divider splits the
    north strip into the arrival room and the stair room (F1: a doorway at row 4,
    since you come in from the street instead)."""
    partition_h(base, over, W, MID, 1, W - 2,
                doors=(WEST_DOOR,) if f1 else (WEST_DOOR, EAST_DOOR))
    partition_v(over, W, NDIV, 1, MID - 2, lip="w", doors=(4,) if f1 else ())


def alcove(over, c):
    """A three-wide nook off the hall's south side (walls at c-2 and c+2, open to
    the north): an optional trainer waits at its back, out of the main line."""
    partition_v(over, W, c - 2, H - 4, H - 2, lip="e")
    partition_v(over, W, c + 2, H - 4, H - 2, lip="w")


# the wild tables, floor by floor — MIRRORED by OLDLIGHT_TABLES in
# tools/balance/build_species.py (slug rows there; keep the two in step).
# The jest-house's own kin (JesterHalf #167, The Smiler #169, McClownface #171)
# live only here; the regulars are the Point's lamplit flutterers.
TOWER_TABLES = {
    1: [(8, 30, 9, 11), (169, 35, 9, 11), (16, 20, 9, 11), (69, 15, 10, 11)],
    2: [(169, 25, 10, 12), (167, 30, 10, 12), (8, 20, 10, 12), (111, 15, 10, 12), (31, 10, 11, 12)],
    3: [(105, 40, 10, 12), (167, 30, 10, 12), (111, 30, 11, 12)],
    4: [(167, 30, 11, 13), (69, 25, 11, 13), (111, 25, 11, 13), (171, 20, 12, 13)],
    5: [(171, 25, 12, 14), (167, 25, 12, 14), (69, 25, 12, 14), (169, 25, 13, 14)],
    6: [(111, 50, 13, 14), (105, 30, 13, 14), (171, 20, 13, 14)],
}

def encounters(zone_id, table, rect=HALL, rate=0.07):
    tx, ty, w, h = rect
    return {"id": zone_id, "terrain": "cave", "rect": {"tx": tx, "ty": ty, "w": w, "h": h},
            "encounter_rate": rate,
            "table": [{"kin_id": k, "weight": wt, "min_level": lo, "max_level": hi}
                      for k, wt, lo, hi in table]}


def stairs(n, w, base, objects, warps, triggers, *, down, up, gate=True,
           band_requires=None, band_blocked=None, partner_w=None):
    """Lay floor n's stair pads + warps (+ the riddle band and the tube)."""
    pw = partner_w or {}
    if down:
        dx = corner_x(w, down)
        base[2 * w + dx] = DOORMAT
        lw = pw.get(n - 1, W)
        warps.append({"id": "down_stairs", "at": {"tx": dx, "ty": 2}, "trigger": "step_on",
                      "to_map": mid(n - 1), "to": {"tx": corner_x(lw, down), "ty": 3},
                      "facing": "down", "transition": "fade"})
    if up:
        ux = corner_x(w, up)
        base[2 * w + ux] = DOORMAT
        uw = pw.get(n + 1, W)
        wp = {"id": "up_stairs", "at": {"tx": ux, "ty": 2}, "trigger": "step_on",
              "to_map": mid(n + 1), "to": {"tx": corner_x(uw, up), "ty": 3},
              "facing": "down", "transition": "fade"}
        if gate:
            wp["requires_flag"] = f"flag:oldlight_{n}_solved"
            wp["blocked_ref"] = "sign.oldlight_stairgate"
        warps.append(wp)
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


def talk(npcs, nid, x, y, sprite, ref, facing="down", movement="look_around"):
    npcs.append({"id": nid, "at": {"tx": x, "ty": y}, "facing": facing, "sprite": sprite,
                 "movement": movement, "dialogue_ref": ref})


def trainer(npcs, tid, x, y, facing, sprite, sight=None):
    """A jest-keeper: the challenge NPC (script.oldlight_<tid>) swapped for a
    chatty after-stage once beaten. `sight` makes it a sight trainer (the
    optional alcove regulars); without it you talk to them (the floor gates)."""
    flag = f"flag:oldlight_{tid}_beaten"
    challenger = {"id": tid, "at": {"tx": x, "ty": y}, "facing": facing, "sprite": sprite,
                  "movement": "static", "dialogue_ref": f"script.oldlight_{tid}",
                  "defeated_flag": flag, "hidden_when_flag": flag}
    if sight:
        challenger["sight_range"] = sight
    npcs += [challenger,
             {"id": f"{tid}_after", "at": {"tx": x, "ty": y}, "facing": facing, "sprite": sprite,
              "movement": "look_around", "dialogue_ref": f"npc.oldlight_{tid}_after",
              "requires_flag": flag}]
    return flag


def alcove_trainer(over, npcs, c, tid, sprite):
    """An optional sight trainer at the back of an alcove, watching its mouth."""
    alcove(over, c)
    trainer(npcs, tid, c, H - 2, "up", sprite, sight=3)


# ---- F1: The Lobby of Groaners ----------------------------------------------------------
def floor_1():
    ts = tileset(1, WARM_SET)
    base, over = shell(ts, door=True)
    tower_walls(base, over, f1=True)
    objects, warps, triggers, npcs = [], [], [], []
    door_x = W // 2
    # --- the LOBBY (the hall: in from the street) ---------------------------------
    # the banners + applause sign hang on the long wall's face behind the box office
    wall_mount(objects, "banner_warm", 8, face_row=MID, oid="banner_l", solid=False)
    wall_mount(objects, "banner_warm", 13, face_row=MID, oid="banner_r", solid=False)
    ol(objects, "applause_sign", 15, MID, oid="applause")
    ol(objects, "bunting", 5, MID, oid="bunting_w")
    sign_at(triggers, "bunting_sign", 5, MID, "sign.oldlight_bunting")
    place(objects, "counter", 9, MID + 1, oid="box_office")
    sign_at(triggers, "box_office_sign", 10, MID + 2, "sign.oldlight_box_office")
    sign_at(triggers, "plaque", 14, MID, "sign.oldlight_plaque")
    sign_at(triggers, "applause_sign", 16, MID, "sign.oldlight_applause")
    # the cloakroom corner (coats nobody came back for) + the groaners' benches
    objects.append({"id": "coats", "sprite": "solarium_costume_rack",
                    "at": {"tx": 1, "ty": 9}, "w": 2, "h": 2})
    sign_at(triggers, "coats_sign", 2, 11, "sign.oldlight_coats")
    place(objects, "pew", 5, 11, oid="bench_l")
    place(objects, "pew", 14, 11, oid="bench_r")
    sign_at(triggers, "bench_l_sign", 6, 11, "sign.oldlight_bench_reserved")
    ol(objects, "rubber_chickens", 8, 11, oid="chicken_stand")
    sign_at(triggers, "chickens", 8, 12, "sign.oldlight_chickens")
    ol(objects, "laugh_meter", 12, 11, oid="laugh_meter")
    sign_at(triggers, "laugh_meter_sign", 12, 12, "script.oldlight_laugh_meter", kind="cutscene")
    ol(objects, "whoopee", 7, 9, oid="whoopee")
    triggers.append({"id": "whoopee", "kind": "cutscene", "at": {"tx": 7, "ty": 9},
                     "activation": "step_on", "ref": "script.oldlight_whoopee",
                     "hidden_when_flag": "flag:oldlight_whoopee_sat"})
    # the lobby's regulars: the GROANER (groans at everything) and the MIME
    talk(npcs, "groaner", 6, 12, "npc_old_man", "npc.oldlight_groaner", facing="up",
         movement="static")
    talk(npcs, "mime", 17, 9, "npc_girl", "script.oldlight_mime")
    # the USHER waits in the south-east alcove (optional): tickets, please
    alcove_trainer(over, npcs, 18, "usher", "npc_man")
    warps.append({"id": "to_point", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
                  "to_map": "pearlmoor_point", "to": {"tx": POINT_DOOR[0], "ty": POINT_DOOR[1] + 1},
                  "facing": "down", "transition": "door"})
    # Punchwheel's welcome rolls once, two steps in from the door (the lobby's
    # mouth: every walkable tile of the row in front of the street door; the
    # east one sits under the laugh meter's base, so it's left out)
    for x in (door_x - 1, door_x):
        triggers.append({"id": f"welcome_{x}", "kind": "cutscene", "at": {"tx": x, "ty": H - 3},
                         "activation": "step_on", "ref": "script.oldlight_welcome",
                         "hidden_when_flag": "flag:oldlight_welcomed"})
    # --- the north strip: the HALL OF GROANS (west), the stair room (east) ---------
    ol(objects, "laugh_dolls", 3, 2, oid="laugh_track")
    sign_at(triggers, "laugh_track_sign", 4, 4, "script.oldlight_laugh_track", kind="cutscene")
    ol(objects, "mask_wall", 7, 1, oid="masks")
    sign_at(triggers, "masks_sign", 7, 1, "sign.oldlight_masks")
    windows(over, W, [8, 15])
    ol(objects, "jack_box", 9, 3, oid="jack_box")
    sign_at(triggers, "jack_box_sign", 9, 3, "script.oldlight_jack_box", kind="cutscene")
    ol(objects, "spotlight", 14, 2, oid="spotlight")
    sign_at(triggers, "spotlight_sign", 14, 3, "sign.oldlight_spotlight")
    stairs(1, W, base, objects, warps, triggers, down=None, up="ne")
    enc = [encounters("tower_f1", TOWER_TABLES[1],
                      rect=(1, 2, W - 2, 4), rate=0.05)]
    m = mapdef(mid(1), "The Old Light — The Lobby of Groaners", W, H, ts,
               base, over, objects, warps, triggers, npcs, music(1))
    m["encounters"] = enc
    return m


# ---- F2: The Room That Laughs a Beat Too Late --------------------------------------------
def floor_2():
    ts = tileset(2, COOL_SET)
    base, over = shell(ts)
    tower_walls(base, over)
    objects, warps, triggers, npcs = [], [], [], []
    # arrival (NE): the WINGS — the prop store behind the stage
    place(objects, "crates", 14, 2, oid="props")
    sign_at(triggers, "props_sign", 14, 3, "sign.oldlight_props")
    ol(objects, "unicycle", 17, 2, oid="unicycle")
    sign_at(triggers, "unicycle_sign", 17, 3, "sign.oldlight_unicycle")
    ol(objects, "clown_shoes", 13, 5, oid="clown_shoes")
    sign_at(triggers, "shoes_sign", 13, 5, "sign.oldlight_clown_shoes")
    # the HALL: the little stage against the long wall, footlights, the pews
    objects.append({"id": "stage", "sprite": "solarium_stage_arch",
                    "at": {"tx": 9, "ty": MID + 1}, "w": 5, "h": 3})
    # the red curtains frame the stage arch itself (in place of the old footlight braziers)
    for oid, stem, x in (("curtain_l", "stage_curtain", 8), ("curtain_r", "stage_curtain_r", 14)):
        objects.append({"id": oid, "sprite": f"oldlight_{stem}", "at": {"tx": x, "ty": MID + 1},
                        "w": 1, "h": 2, "solid": False})
    ol(objects, "spotlight", 16, MID + 2, oid="spotlight")
    sign_at(triggers, "spotlight_sign", 16, MID + 3, "sign.oldlight_spotlight_late")
    place(objects, "pew", 9, 11, oid="pew_a")
    place(objects, "pew", 13, 11, oid="pew_b")
    # the audience that laughs one line late (stood behind the pews; the aisle
    # along rows 12-13 is the hall's one lane east-west)
    for nid, x, y, spr in (("late_a", 10, 12, "npc_old_woman"), ("late_b", 14, 12, "fisher_man"),
                           ("late_c", 12, 13, "npc_boy")):
        npcs.append({"id": nid, "at": {"tx": x, "ty": y}, "facing": "up", "sprite": spr,
                     "movement": "static", "dialogue_ref": f"npc.oldlight_{nid}"})
    ol(objects, "laugh_dolls", 18, 11, oid="laugh_track")
    sign_at(triggers, "laugh_track_sign", 18, 13, "script.oldlight_laugh_track_late", kind="cutscene")
    # the LATE LAUGH, felt: cross the aisle past the audience and they laugh at
    # you a beat after you've gone by (a once band on every walkable tile of the cut)
    for y in (11, 12, 13):
        triggers.append({"id": f"late_laugh_{y}", "kind": "cutscene", "at": {"tx": 16, "ty": y},
                         "activation": "step_on", "ref": "script.oldlight_late_laugh",
                         "hidden_when_flag": "flag:oldlight_late_laughed"})
    # the JUGGLER in the south-west alcove (optional)
    alcove_trainer(over, npcs, 5, "juggler", "village_child")
    # the stair room (NW): the HECKLER guards the tube
    ol(objects, "mask_wall", 5, 1, oid="masks")
    sign_at(triggers, "masks_sign", 5, 1, "sign.oldlight_masks_late")
    stairs(2, W, base, objects, warps, triggers, down="ne", up="nw",
           band_requires="flag:oldlight_heckler_beaten",
           band_blocked="npc.oldlight_heckler_block")
    trainer(npcs, "heckler", 4, 3, "left", "npc_man")
    m = mapdef(mid(2), "The Old Light — The Late Laugh", W, H, ts,
               base, over, objects, warps, triggers, npcs, music(2))
    m["encounters"] = [encounters("tower_f2", TOWER_TABLES[2])]
    return m


# ---- F3: Intermission (the soft floor, the tea-urn, the Hall of Mouths) ---------------------
def floor_3():
    ts = tileset(3, WARM_SET)
    base, over = shell(ts)
    tower_walls(base, over)
    objects, warps, triggers, npcs = [], [], [], []
    # arrival (NW): the INTERVAL BAR — the tea-urn automaton (the floor's REST)
    ol(objects, "tea_urn", 4, 2, oid="tea_urn")
    for x in (4, 5):
        sign_at(triggers, f"urn_{x}", x, 3, "script.oldlight_urn", kind="cutscene")
    ol(objects, "teacups", 7, 2, oid="teacups")
    sign_at(triggers, "teacups_sign", 7, 3, "sign.oldlight_teacups")
    place(objects, "stool", 3, 4, oid="bar_stool")
    sign_at(triggers, "bar_stool_sign", 3, 4, "sign.oldlight_bar_stool")
    place(objects, "stool", 6, 4, oid="bar_stool_b")
    # the hall is TWO rooms (the floor's own shape): the Hall of Mouths (west)
    # and the computer room (east), one doorway between them at row 11
    partition_v(over, W, 11, MID + 1, H - 2, lip="w", doors=(11,))
    # the HALL OF MOUTHS: soft furniture with faces and opinions on the long wall
    wall_mount(objects, "stove", 6, face_row=MID)            # the stove that laughs first
    wall_mount(objects, "bookcase", 9, face_row=MID)         # the bookcase that clears its throat
    sign_at(triggers, "stove", 6, MID + 1, "npc.oldlight_stove")
    sign_at(triggers, "stove_b", 7, MID + 1, "npc.oldlight_stove")
    sign_at(triggers, "bookcase", 9, MID + 2, "npc.oldlight_bookcase")
    sign_at(triggers, "bookcase_b", 10, MID + 2, "npc.oldlight_bookcase")
    place(objects, "table", 8, 11, oid="table")
    place(objects, "stool", 7, 12, oid="stool_l")
    place(objects, "stool", 10, 12, oid="stool_r")
    sign_at(triggers, "p_note", 8, 11, "sign.oldlight_p_note")
    ol(objects, "pie_table", 3, 10, oid="pies")
    sign_at(triggers, "pies_sign", 3, 11, "sign.oldlight_pies")
    # the COMPUTER (an anachronism nobody can explain — the tower's own joke),
    # off the line in the east of the hall; Confirm facing its front row -> ANDY-LAND
    # (the triggers sit ON the object, row 9: one row lower = facing bare floor)
    place(objects, "computer", 12, 8, oid="computer")
    for x in (12, 13):
        sign_at(triggers, f"computer_{x}", x, 9, "script.oldlight_computer", kind="cutscene")
    # the three escaped PUNCHLINES, loose in the hall
    for nid, x, y, spr in (("punch_tuesday", 15, 9, "npc_girl"),
                           ("punch_buns", 6, 12, "npc_child"),
                           ("punch_ladder", 10, 13, "npc_boy")):
        npcs.append({"id": nid, "at": {"tx": x, "ty": y}, "facing": "down", "sprite": spr,
                     "movement": "look_around", "dialogue_ref": f"npc.oldlight_{nid}"})
    # the PIE-THROWER in the south-east alcove (optional)
    alcove_trainer(over, npcs, 18, "pie_thrower", "market_trader")
    # the stair room (NE)
    ol(objects, "cog_heap", 14, 4, oid="cogs")
    sign_at(triggers, "cogs_sign", 14, 4, "sign.oldlight_cogs")
    windows(over, W, [15, 17])
    stairs(3, W, base, objects, warps, triggers, down="nw", up="ne")
    m = mapdef(mid(3), "The Old Light — Intermission", W, H, ts,
               base, over, objects, warps, triggers, npcs, music(3))
    m["encounters"] = [encounters("tower_f3", TOWER_TABLES[3], rate=0.04)]
    return m


# ---- F4: The Backwards Inn (the lobby, mirrored) -----------------------------------------
def floor_4():
    ts = tileset(4, COOL_SET)
    base, over = shell(ts)
    tower_walls(base, over)
    objects, warps, triggers, npcs = [], [], [], []
    # arrival (NE): the cloakroom, mirrored — the coats hang the other way
    objects.append({"id": "coats", "sprite": "solarium_costume_rack",
                    "at": {"tx": 13, "ty": 4}, "w": 2, "h": 2})
    ol(objects, "clock_backwards", 15, 1, oid="clock")
    sign_at(triggers, "clock_sign", 15, 1, "sign.oldlight_clock_backwards")
    ol(objects, "upside_chair", 16, 3, oid="upside_chair")
    sign_at(triggers, "chair_sign", 16, 3, "sign.oldlight_upside_chair")
    # the floor's opener plays once on the only way out of the cloakroom
    for y in (MID - 1, MID):
        triggers.append({"id": f"backwards_opener_{y}", "kind": "cutscene",
                         "at": {"tx": EAST_DOOR, "ty": y}, "activation": "step_on",
                         "ref": "script.oldlight_backwards",
                         "hidden_when_flag": "flag:oldlight_4_opened"})
    # the HALL: the lobby turned inside out — the counter faces the wall
    wall_mount(objects, "banner_warm", 8, face_row=MID, oid="banner_l", solid=False)
    wall_mount(objects, "banner_warm", 13, face_row=MID, oid="banner_r", solid=False)
    place(objects, "counter", 9, MID + 1, oid="box_office")
    sign_at(triggers, "backwards_a", 7, MID, "sign.oldlight_backwards_a")
    sign_at(triggers, "backwards_b", 11, MID + 3, "sign.oldlight_backwards_b")
    sign_at(triggers, "reassess", 9, MID + 3, "sign.oldlight_reassess")
    sign_at(triggers, "reassess_b", 12, MID + 3, "sign.oldlight_reassess")
    sign_at(triggers, "box_office_sign", 10, MID + 3, "script.oldlight_lamps_out", kind="cutscene")
    ol(objects, "funhouse_mirror", 5, MID, oid="mirror_a")
    ol(objects, "funhouse_mirror", 16, MID, oid="mirror_b")
    # every glass bends you its own way: one line each, on the glass itself
    sign_at(triggers, "mirror_a_sign", 5, MID + 1, "sign.oldlight_mirror_squat")
    sign_at(triggers, "mirror_b_sign", 16, MID + 1, "sign.oldlight_funhouse")
    place(objects, "pew", 13, 12, oid="bench_r")
    objects.append({"id": "troupe_cart", "sprite": "solarium_troupe_cart",
                    "at": {"tx": 8, "ty": 12}, "w": 3, "h": 2})
    sign_at(triggers, "troupe_cart", 11, 12, "npc.oldlight_cart")
    place(objects, "brazier", 15, 10, oid="brazier_r")
    sign_at(triggers, "brazier_sign", 15, 11, "sign.oldlight_brazier")
    # the MIRROR MAZE (small): free-standing funhouse glasses zig-zag the east
    # hall, so the walk to the stair is a little dance with your reflections.
    # Each glass's TOP row is walk-behind (you slip behind the frame's crown,
    # drawn over you — depth), and each answers Confirm with its own distortion.
    maze = (((17, 9), "sign.oldlight_mirror_upside"), ((19, 11), "sign.oldlight_maze_end"),
            ((13, 10), "sign.oldlight_mirror_bighead"), ((17, 12), "sign.oldlight_mirror_wavy"),
            ((19, 8), "sign.oldlight_mirror_late"))
    for i, ((x, y), ref) in enumerate(maze):
        objects.append({"id": f"maze_mirror_{i}", "sprite": "oldlight_funhouse_mirror",
                        "at": {"tx": x, "ty": y}, "w": 1, "h": 2,
                        "overhang": 1, "walk_under": True})
        sign_at(triggers, "maze_end" if i == 1 else f"maze_mirror_{i}_sign", x, y + 1, ref)
    sign_at(triggers, "maze_sign", 20, 9, "sign.oldlight_mirror_maze")
    # THE MIRROR in the south-west alcove (optional): a mimic, battles in pairs
    alcove_trainer(over, npcs, 5, "mirror", "player_indi")  # wears YOUR face
    # the stair room (NW): the RINGMASTER guards the tube
    stairs(4, W, base, objects, warps, triggers, down="ne", up="nw",
           band_requires="flag:oldlight_ringmaster_beaten",
           band_blocked="npc.oldlight_ringmaster_block")
    trainer(npcs, "ringmaster", 4, 3, "left", "npc_shopkeeper")
    ol(objects, "mallet", 8, 2, oid="mallet")
    # the BACKWARDS URN: the tea-urn's twin pours the interval at the START, so you
    # can mend your kin right beside the Ringmaster before (and after) the bout
    ol(objects, "tea_urn", 6, 2, oid="tea_urn_backwards")
    for x in (6, 7):
        sign_at(triggers, f"urn_backwards_{x}", x, 3, "script.oldlight_urn_backwards", kind="cutscene")
    m = mapdef(mid(4), "The Old Light — The Backwards Inn", W, H, ts,
               base, over, objects, warps, triggers, npcs, music(4))
    m["encounters"] = [encounters("tower_f4", TOWER_TABLES[4])]
    return m


# ---- F5: The Gallery of Confident Facts --------------------------------------------------
def floor_5():
    ts = tileset(5, COOL_SET)
    base, over = shell(ts)
    tower_walls(base, over)
    objects, warps, triggers, npcs = [], [], [], []
    # six framed captions: three in the arrival room (north face), three on the
    # long wall's face over the hall
    frames = [("cap_reyl", 3, 1, "reyl"), ("cap_tuesday", 6, 1, "tuesday"),
              ("cap_stars", 9, 1, "stars"), ("cap_sea", 5, MID, "sea"),
              ("cap_gerald", 10, MID, "gerald"), ("cap_tam", 15, MID, "ferry")]
    for fid, x, y, pic in frames:
        # hung on the wall face (the cap row above + the face row), non-solid;
        # the TRUE picture (cap_tam) is Tam's ferry in its plain dark frame
        objects.append({"id": f"frame_{fid}", "sprite": f"oldlight_painting_{pic}",
                        "at": {"tx": x, "ty": y - 1}, "w": 1, "h": 2, "solid": False})
        sign_at(triggers, fid, x, y, f"sign.oldlight_{fid}")
    place(objects, "brazier", 2, 3, oid="brazier_n")
    place(objects, "brazier", 18, 9, oid="brazier_s")
    place(objects, "pew", 8, 11, oid="viewing_bench")
    sign_at(triggers, "viewing_bench_sign", 9, 11, "sign.oldlight_viewing_bench")
    place(objects, "plant", 1, 13, oid="plant")
    sign_at(triggers, "plant_sign", 1, 13, "sign.oldlight_plant")
    ol(objects, "joke_lectern", 12, 10, oid="lectern")
    sign_at(triggers, "lectern_sign", 12, 12, "script.oldlight_lectern", kind="cutscene")
    ol(objects, "mallet", 3, 9, oid="mallet")
    # the GALLERY FLOOR, waxed to a mirror shine: the hall's north lane is a
    # glare-ice FLOW (traversal kit: you skid until something stops you), with
    # banana skins on it, because of course. Dry ground either side; never a trap.
    m_flows = [{"id": "waxed_floor", "kind": "ice", "rect": {"tx": 4, "ty": 8, "w": 14, "h": 2}}]
    for y in (8, 9):  # the shine, painted over every tile of the flow
        for x in range(4, 18):
            ol(objects, "wax_shine" if (x + y) % 2 else "wax_shine_b", x, y, oid=f"wax_{x}_{y}")
    for i, (x, y) in enumerate(((7, 8), (13, 9), (16, 8))):
        ol(objects, "banana", x, y, oid=f"slick_banana_{i}")
    triggers.append({"id": "waxed_floor_warn", "kind": "cutscene", "at": {"tx": 3, "ty": 7},
                     "activation": "step_on", "ref": "script.oldlight_waxed_floor",
                     "hidden_when_flag": "flag:oldlight_waxed_seen"})
    sign_at(triggers, "mallet_sign", 3, 11, "sign.oldlight_mallet")
    # the banana peels: the gallery's one confident fact ("floors are safe")
    for i, (x, y) in enumerate(((7, 10), (14, 13), (16, 10))):
        ol(objects, "banana", x, y, oid=f"banana_{i}")
    triggers.append({"id": "banana_slip", "kind": "cutscene", "at": {"tx": 7, "ty": 10},
                     "activation": "step_on", "ref": "script.oldlight_banana",
                     "hidden_when_flag": "flag:oldlight_banana_slipped"})
    # THE CRITIC in the south-east alcove (optional)
    alcove_trainer(over, npcs, 18, "critic", "npc_old_woman")
    # the stair room (NE)
    ol(objects, "laugh_meter", 14, 2, oid="laugh_meter")
    sign_at(triggers, "laugh_meter_sign", 14, 4, "script.oldlight_laugh_meter_f5", kind="cutscene")
    # (Punchwheel's never-told joke — the knock-knock loop — opens the riddle
    #  itself, once: script.oldlight_5 guards it on flag:oldlight_knock_done)
    stairs(5, W, base, objects, warps, triggers, down="nw", up="ne")
    m = mapdef(mid(5), "The Old Light — The Gallery of Confident Facts", W, H, ts,
               base, over, objects, warps, triggers, npcs, music(5))
    m["encounters"] = [encounters("tower_f5", TOWER_TABLES[5])]
    m["flows"] = m_flows
    return m


# ---- F6: The One Joke (almost empty; the quiet in the middle of the noise) --------------
def floor_6():
    ts = tileset(6, WARM_SET)
    base, over = shell(ts)
    tower_walls(base, over)
    objects, warps, triggers, npcs = [], [], [], []
    windows(over, W, [6, 16])
    # arrival (NE): the coat alcove — one coat, one peg
    objects.append({"id": "coat_peg", "sprite": "solarium_costume_rack",
                    "at": {"tx": 17, "ty": 3}, "w": 2, "h": 2})
    sign_at(triggers, "coat", 17, 5, "sign.oldlight_coat")
    sign_at(triggers, "coat_b", 18, 5, "sign.oldlight_coat")
    sign_at(triggers, "window", 16, 1, "sign.oldlight_window")
    # the loop: the One Joke plays on the only way out of the arrival room
    for y in (MID - 1, MID):
        triggers.append({"id": f"one_joke_{y}", "kind": "cutscene",
                         "at": {"tx": EAST_DOOR, "ty": y}, "activation": "step_on",
                         "ref": "script.oldlight_one_joke",
                         "hidden_when_flag": "flag:oldlight_6_heard"})
    # the HALL: a long, nearly bare room — the table with two cups is its heart
    # (and the floor's REST: sit across from the empty chair a while)
    place(objects, "table", 10, 10, oid="two_cups")
    place(objects, "stool", 9, 11, oid="stool_l")
    place(objects, "stool", 12, 11, oid="stool_r")
    sign_at(triggers, "cups", 10, 10, "script.oldlight_cups_rest", kind="cutscene")
    sign_at(triggers, "cups_b", 11, 10, "script.oldlight_cups_rest", kind="cutscene")
    # the AUDIENCE: twelve stools set out in rows facing the two cups, every
    # one dusted, every one empty (the floor's shape: an aisle down the middle)
    for i, (x, y) in enumerate((x, y) for y in (9, 12) for x in (3, 5, 7, 14, 16, 18)):
        if (x, y) != (18, 12):  # the spring-can sits there
            place(objects, "stool", x, y, oid=f"audience_{i}")
    sign_at(triggers, "audience_sign", 7, 8, "sign.oldlight_audience")
    ol(objects, "confetti", 4, 12, oid="confetti_old")
    sign_at(triggers, "confetti_sign", 4, 12, "sign.oldlight_old_confetti")
    ol(objects, "spring_can", 18, 12, oid="spring_can")
    sign_at(triggers, "spring_can_sign", 18, 12, "sign.oldlight_spring_can")
    stairs(6, W, base, objects, warps, triggers, down="ne", up="nw", gate=False,
           partner_w={7: 14})
    m = mapdef(mid(6), "The Old Light — The One Joke", W, H, ts,
               base, over, objects, warps, triggers, npcs, music(6))
    m["encounters"] = [encounters("tower_f6", TOWER_TABLES[6], rate=0.04)]
    return m


# ---- TOP: The Winding Room ---------------------------------------------------------------
def floor_top():
    w, h = 14, 11
    ts = tileset(7, WARM_SET)
    base, over = shell(ts, w=w, h=h)
    objects, warps, triggers, npcs = [], [], [], []
    # MR. PUNCHWHEEL, half-stopped: the great winding drum + his brass face
    objects.append({"id": "punchwheel_drum", "sprite": "oldlight_punchwheel_drum",
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
    over[1 * w + 3] = WINDOW
    sign_at(triggers, "rope_sill", 3, 1, "sign.oldlight_rope")
    partition_v(over, w, 10, 5, 9, lip="e")
    place(objects, "table", 11, 6, oid="log_table")
    place(objects, "stool", 11, 8, oid="log_stool")
    for x in (11, 12):
        sign_at(triggers, f"log_{x}", x, 6, "script.oldlight_log", kind="cutscene")
    wall_mount(objects, "lamp_rack", 11, solid=False)
    place(objects, "brazier", 3, 7, oid="brazier_w")
    place(objects, "oil_jars", 1, 9, oid="jars")
    sign_at(triggers, "jars_sign", 1, 9, "sign.oldlight_jars")
    # the workshop clutter of a machine that wound itself too tight
    ol(objects, "cog_heap", 2, 4, oid="cogs")
    # the GREEN ROOM chair by the stairhead: the top floor's rest point, before the
    # headline act at the drum (script.oldlight_greenroom; the boss is in script.oldlight_top)
    place(objects, "armchair_green", 4, 2, oid="greenroom_chair")
    sign_at(triggers, "greenroom", 4, 3, "script.oldlight_greenroom", kind="cutscene")
    # the HEADLINE ACT bars the way to the drum: the only way from the stairhead
    # side into the drum room is the x=5 gap (rows 7-8), and the three clowns stand
    # in it. Punchwheel won't let anyone near Tam's card; beating his act is the toll,
    # not the climax (the card is) — they step aside on flag:oldlight_headliners_beaten.
    for nid, (x, y), spr in (("act_smiler", (5, 7), "kin_169_overworld"),
                             ("act_clown", (5, 8), "kin_171_overworld"),
                             ("act_jester", (6, 7), "kin_167_overworld")):
        npcs.append({"id": nid, "at": {"tx": x, "ty": y}, "facing": "left", "sprite": spr,
                     "movement": "static", "dialogue_ref": "script.oldlight_headliners",
                     "hidden_when_flag": "flag:oldlight_headliners_beaten"})
    triggers.append({"id": "headliners_band", "kind": "cutscene", "at": {"tx": 4, "ty": 7},
                     "activation": "step_on", "ref": "script.oldlight_headliners",
                     "hidden_when_flag": "flag:oldlight_headliners_beaten"})
    ol(objects, "spring_can", 4, 9, oid="spring_can")
    ol(objects, "confetti", 9, 8, oid="confetti_a")
    ol(objects, "confetti", 5, 9, oid="confetti_b")
    ol(objects, "bunting", 6, 1, oid="bunting")
    stairs(7, w, base, objects, warps, triggers, down="nw", up=None, partner_w={6: W})
    # THE SLIDE: the tower's last joke — a chute down to the Point
    base[9 * w + 7] = DOORMAT
    warps.append({"id": "slide", "at": {"tx": 7, "ty": 9}, "trigger": "step_on",
                  "to_map": "pearlmoor_point", "to": {"tx": 7, "ty": 8},
                  "facing": "down", "transition": "fade",
                  "requires_flag": "flag:q_south_jest_done",
                  "blocked_ref": "sign.oldlight_slide_shut"})
    # ...and it LOOKS like one: the hatch thrown open over the brass chute
    # (drawn by draw_warp_markers.py), only once the slide is unbolted
    objects.append({"id": "slide_hatch", "sprite": "markers_trapdoor",
                    "at": {"tx": 7, "ty": 9}, "w": 1, "h": 1, "solid": False,
                    "requires_flag": "flag:q_south_jest_done"})
    return mapdef(mid(7), "The Old Light — The Winding Room", w, h, ts,
                  base, over, objects, warps, triggers, npcs, music(7))


# MOLL, Tam's old stage partner — the tower's one non-fighting companion. She
# is always a floor AHEAD of you (each placement hides once that floor's stair
# opens: "back stairs, love"), cheers you on, and tells Tam's story a piece per
# floor (npc.oldlight_moll_*, regions/jesthouse.ts). She reaches the top only
# after you've finished Tam's card. Parked in a corner by each arrival pad, off
# the lane to the hall.
MOLL = [  # (floor, id, tile, ref, hidden_when, requires)
    (1, "moll", (14, 12), "npc.oldlight_moll_1", "flag:oldlight_1_solved", None),
    (2, "moll", (20, 5), "script.oldlight_moll_2", "flag:oldlight_2_solved", None),
    (3, "moll", (1, 5), "npc.oldlight_moll_3", "flag:oldlight_3_solved", None),
    (4, "moll", (20, 5), "script.oldlight_moll_4", "flag:oldlight_4_solved", None),
    (5, "moll", (5, 3), "npc.oldlight_moll_5", "flag:oldlight_5_solved", None),
    (6, "moll", (20, 5), "npc.oldlight_moll_6", "flag:q_south_jest_done", None),
    # the top: she's there for the card (by the stairhead), then after it
    (7, "moll", (4, 8), "npc.oldlight_moll_card", "flag:q_south_jest_done", "flag:oldlight_6_heard"),
    (7, "moll_after", (4, 8), "npc.oldlight_moll_top", None, "flag:q_south_jest_done"),
]


def add_moll(n, m):
    for floor, nid, (x, y), ref, hide, need in MOLL:
        if floor != n:
            continue
        npc = {"id": nid, "at": {"tx": x, "ty": y}, "facing": "down", "sprite": "fisher_woman",
               "movement": "look_around", "dialogue_ref": ref}
        if hide:
            npc["hidden_when_flag"] = hide
        if need:
            npc["requires_flag"] = need
        m["npcs"].append(npc)
    return m


def all_maps():
    floors = [floor_1(), floor_2(), floor_3(), floor_4(), floor_5(), floor_6(), floor_top()]
    return [add_moll(n, m) for n, m in enumerate(floors, 1)]


if __name__ == "__main__":
    ok = True
    for m in all_maps():
        ok = finish(m) and ok
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
