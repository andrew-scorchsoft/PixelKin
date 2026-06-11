#!/usr/bin/env python3
"""
The Tinderwick BEACON — the earned first Gleam (three stacked interiors).

Tinderwick's "big tower" moment: the old lamp-tower on the NE bluff whose foot
door answers the wick-key carried home from Dimglass Coast (script.give_wick).
Floors I and II are stair rooms held by Brisa's wick-tenders — SIGHT trainers
posted in the TOP ROW facing DOWN their own column, so every route across the
floor crosses their line (their body blocks the top row itself: the classic
"you can't dodge this one" post). The lantern room at the top stages the
bond-test (script.beacon_battle) and the Ember Gleam.

Spiral read: enter at the foot door -> up-stairs NE -> floor II -> up-stairs NW
-> the lantern room. Cool stone register (a shrine, not a cabin).

Run:  python3 tools/maps/build_beacon.py
"""
from __future__ import annotations

from build_interiors import (COOL_SET, FLOOR, DOORMAT, RUNNER, BANNER, CAP_N,
                             faced_room, windows, mapdef, obj, write_and_render)

MUSIC = "assets/audio/music/tinderwick-a.mp3"


def stair_floor(id_, name, *, keeper_id, keeper_script, keeper_after,
                keeper_flag, sign_ref, down_warp, up_warp):
    """One stair room: doormat exit at the bottom (or a down-landing), an
    up-landing doormat in a corner, a wick-tender holding the crossing."""
    W, H = 12, 9
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    windows(over, W, [2, W - 3], tile=BANNER)
    # the UP landing: a doormat pad in the NE corner (the stairwell)
    up_x, up_y = W - 2, 2
    base[up_y * W + up_x] = DOORMAT
    # runner lane from the entrance up the middle (the climb's visual pull)
    for y in range(3, H - 1):
        base[y * W + door_x] = RUNNER

    objects = [
        obj("rug", "interior_rug", door_x - 1, 4, 3, 2, solid=False),
        # braziers light the stairwell corner + the west wall
        obj("brazier_stair", "interior_brazier", up_x - 1, up_y, 1, 2, overhang=1),
        obj("brazier_w", "interior_brazier", 1, 4, 1, 2, overhang=1),
        # wick stores: the shelf mounts FLUSH against the north wall (the drawn
        # 2x3 front-elevation piece; top row over the face), barrels below
        obj("shelf", "interior_shelf", 1, 1, 2, 3, overhang=1),
        obj("barrels", "interior_barrels", 1, 7, 2, 1),
    ]
    warps = [down_warp]
    if up_warp:
        warps.append(dict(up_warp, at={"tx": up_x, "ty": up_y}, trigger="step_on"))
    triggers = [
        {"id": "sign_litany", "kind": "sign", "at": {"tx": 2, "ty": 6},
         "activation": "interact", "ref": sign_ref},
    ]
    # The wick-tender: top row, facing DOWN their column (col 8). Their body
    # blocks the top row, so every floor crossing meets their sight line.
    npcs = [
        {"id": keeper_id, "at": {"tx": 8, "ty": 2}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": keeper_script, "sight_range": 5,
         "defeated_flag": keeper_flag, "hidden_when_flag": keeper_flag},
        {"id": f"{keeper_id}_after", "at": {"tx": 8, "ty": 2}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "look_around",
         "dialogue_ref": keeper_after, "requires_flag": keeper_flag},
    ]
    return mapdef(id_, name, W, H, COOL_SET, base, over, objects, warps,
                  triggers, npcs, MUSIC)


def lantern_room():
    """The top: the great lantern, Brisa, the bond-test, the Ember Gleam."""
    W, H = 12, 9
    door_x = W // 2
    base, over = faced_room(W, H, door_x)
    # no bottom exit at the top of a tower — restore the wall band over the
    # default doormat and stair down from the NW landing instead
    base[(H - 1) * W + door_x] = FLOOR
    over[(H - 1) * W + door_x] = CAP_N
    windows(over, W, [door_x - 2, door_x + 2], tile=BANNER)
    down_x, down_y = 1, 2
    base[down_y * W + down_x] = DOORMAT
    for y in range(3, H - 2):
        base[y * W + door_x] = RUNNER

    objects = [
        # THE LANTERN — the beacon's great lamp, top-centre (altar object)
        obj("lantern", "interior_altar", door_x - 1, 2, 3, 3, overhang=1),
        obj("rug", "interior_rug", door_x - 1, 5, 3, 2, solid=False),
        obj("brazier_l", "interior_brazier", door_x - 3, 5, 1, 2, overhang=1),
        obj("brazier_r", "interior_brazier", door_x + 3, 5, 1, 2, overhang=1),
        obj("brazier_stair", "interior_brazier", down_x + 1, down_y, 1, 2, overhang=1),
    ]
    warps = [
        {"id": "down_stairs", "at": {"tx": down_x, "ty": down_y}, "trigger": "step_on",
         "to_map": "tinderwick_beacon_ii", "to": {"tx": 2, "ty": 3}, "facing": "down",
         "transition": "fade"},
    ]
    triggers = [
        # the bond-test: stepping up the aisle to Brisa starts it (once)
        {"id": "beacon_battle", "kind": "cutscene", "at": {"tx": door_x, "ty": 6},
         "activation": "step_on", "ref": "script.beacon_battle", "once": True,
         "requires_flag": "flag:caught_first_kin",
         "blocked_ref": "npc.brisa_not_ready"},
    ]
    npcs = [
        # Brisa waits at the lantern until the Ember stands; then she keeps the
        # hall below (npc.brisa_after) and the fair takes the square.
        {"id": "brisa", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.brisa_tallow", "hidden_when_flag": "gleam:ember"},
    ]
    return mapdef("tinderwick_beacon_top", "The Beacon — Lantern Room", W, H,
                  COOL_SET, base, over, objects, warps, triggers, npcs, MUSIC)


def all_maps():
    floor_i = stair_floor(
        "tinderwick_beacon_i", "The Beacon — Floor I",
        keeper_id="tansy", keeper_script="script.beacon_keeper_a",
        keeper_after="npc.beacon_keeper_a_after",
        keeper_flag="flag:beacon_keeper_a_beaten", sign_ref="sign.beacon_floor_i",
        down_warp={"id": "to_town", "at": {"tx": 6, "ty": 8}, "trigger": "step_on",
                   "to_map": "tinderwick", "to": {"tx": 24, "ty": 7},
                   "facing": "down", "transition": "door"},
        up_warp={"id": "up_stairs", "to_map": "tinderwick_beacon_ii",
                 "to": {"tx": 10, "ty": 3}, "facing": "down", "transition": "fade"},
    )
    floor_ii = stair_floor(
        "tinderwick_beacon_ii", "The Beacon — Floor II",
        keeper_id="cole", keeper_script="script.beacon_keeper_b",
        keeper_after="npc.beacon_keeper_b_after",
        keeper_flag="flag:beacon_keeper_b_beaten", sign_ref="sign.beacon_floor_ii",
        down_warp={"id": "down_stairs", "at": {"tx": 10, "ty": 2}, "trigger": "step_on",
                   "to_map": "tinderwick_beacon_i", "to": {"tx": 10, "ty": 3},
                   "facing": "down", "transition": "fade"},
        up_warp=None,
    )
    # floor II's UP stairs spiral to the NW corner (opposite floor I's NE);
    # and a tower floor has no bottom door — wall the default doormat back up
    fii_W = 12
    floor_ii["layers"][0]["data"][2 * fii_W + 1] = DOORMAT
    floor_ii["layers"][0]["data"][8 * fii_W + 6] = FLOOR
    floor_ii["layers"][1]["data"][8 * fii_W + 6] = CAP_N
    floor_ii["warps"].append(
        {"id": "up_stairs", "at": {"tx": 1, "ty": 2}, "trigger": "step_on",
         "to_map": "tinderwick_beacon_top", "to": {"tx": 1, "ty": 3},
         "facing": "down", "transition": "fade"})
    # keep the NW stairwell clear: floor II's shelf slides ALONG the north wall
    # to cols 3-4 (a wall-elevation piece must stay mounted on a north-facing
    # wall — parked at the south wall it draws over the bottom wall band)
    for o in floor_ii["objects"]:
        if o["id"] == "shelf":
            o["at"] = {"tx": 3, "ty": 1}
    return [floor_i, floor_ii, lantern_room()]


if __name__ == "__main__":
    for m in all_maps():
        write_and_render(m)
    print("DONE")
