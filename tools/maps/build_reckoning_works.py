#!/usr/bin/env python3
"""
The Reckoning-Works (09-the-wild-ways §C2) — the side quest "Measured in Miles":
a brass-and-punch-card works on the Rimeway Fold where clerks and their kin run
calculating engines that compute the STAR-TABLES (when each lamp and
constellation should be tended). Once that work mattered; now the engines run
faster and faster, the output board climbs, and the tables stack unread.

One interior, three rooms (docs/world/interiors.md — warm register, roomkit):
  * THE ENGINE HALL (west, the main room): focal point = the OUTPUT BOARD flush
    on the north face (swaps to its chalk-drawn twin on flag:q_works_done); two
    calculating engines with a card-belt between them, worked by a Chillpip and a
    Snowcune (creature NPCs); clerks' desks; stacks of unread tables.
  * THE OVERSEER'S OFFICE (south-east, behind a partition door): Ketterly at her
    desk (talk ACROSS it), the ledger shelf.
  * THE STAR-ROOM (north-east, through the office): the old observation window
    nobody opens — dusty stacks, a stool. After the Paul story the apprentice Nib
    stands here, and it's where the quest's first "find" happens (frost-ferns).

Cast placement is flag-staged (flags in src/game/content/regions/reckonworks.ts):
  hall clerks `hidden_when_flag: flag:q_works_story` (they wander out after the
  story) -> their `_back` twins `requires_flag: flag:works_found_<name>` (each one
  comes home as you find them out on the Rimeway / in Pale Vault).

HANDSHAKE: doormat (7,13) `to_fold` -> rimeway_fold (24,20); the Fold's door warp
  `to_works` (24,19) lands here at (7,12).

Run:  python3 tools/maps/build_reckoning_works.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, faced_room, windows, partition_v, partition_h,
                     place, wall_mount, spec, mapdef, finish)

W, H = 20, 14
DOOR_X = 7
STORY = "flag:q_works_story"
DONE = "flag:q_works_done"

OWED = [
    "script.works_ketterly", "script.works_nib", "script.works_hollis",
    "script.works_teague", "script.works_brann", "script.works_board",
    "script.works_window", "script.works_engine_kin", "script.works_stacks",
]


def wall_piece(objects: list, stem: str, tx: int, *, face_row: int = 1, oid: str | None = None,
               solid: bool = True, **flags) -> dict:
    """roomkit.wall_mount for this works' own wall pieces (output board, star
    window): top row over the wall FACE (walk-under), floor rows solid."""
    s = spec(stem)
    o = {"id": oid or stem, "sprite": f"interior_{stem}", "at": {"tx": tx, "ty": face_row},
         "w": s["tw"], "h": s["th"], "overhang": 1, "walk_under": True}
    if not solid:
        o["solid"] = False
    o.update(flags)
    objects.append(o)
    return o


def npc(nid, x, y, facing, sprite, ref, **flags) -> dict:
    d = {"id": nid, "at": {"tx": x, "ty": y}, "facing": facing, "sprite": sprite,
         "movement": "static", "dialogue_ref": ref}
    d.update(flags)
    return d


def build():
    base, over = faced_room(W, H, DOOR_X)
    windows(over, W, [4, 10])
    # the east wing: one partition wall (hall | wing) with a door at row 10,
    # then the wing split into the star-room (north) and the office (south)
    partition_v(over, W, 13, 1, 12, lip="w", doors=(10,))
    partition_h(base, over, W, 7, 14, 18, doors=(16,))

    objects: list = []
    # ---- THE ENGINE HALL ---------------------------------------------------------
    # focal: the output board, top-centre over the aisle (flag-pair swap, same
    # footprint + solidity — collision is flag-blind)
    wall_piece(objects, "output_board", 6, oid="output_board", hidden_when_flag=DONE)
    wall_piece(objects, "output_board_after", 6, oid="output_board_after", requires_flag=DONE)
    wall_mount(objects, "lamp_rack", 1, oid="lamps_w", solid=False)
    wall_mount(objects, "lamp_rack", 11, oid="lamps_e", solid=False)
    # two calculating engines and the card-belt between them
    place(objects, "reckoning_engine", 1, 4, oid="engine_a")
    place(objects, "reckoning_engine", 10, 4, oid="engine_b")
    place(objects, "card_belt", 5, 6, oid="belt")
    # the clerks' desks + stools, the unread tables
    place(objects, "desk", 2, 9, oid="desk_hollis")
    place(objects, "desk", 10, 9, oid="desk_teague")
    place(objects, "card_stacks", 4, 11, oid="stacks_hall_a")
    place(objects, "card_stacks", 10, 11, oid="stacks_hall_b")
    place(objects, "crates", 1, 11, oid="card_crates")

    # ---- THE OVERSEER'S OFFICE (rows 8-12, x14-18) -------------------------------
    place(objects, "desk", 14, 9, oid="desk_ketterly")
    wall_mount(objects, "bookcase", 17, face_row=7, oid="ledger_case")
    place(objects, "plant", 14, 12, oid="office_fern")
    place(objects, "stool", 18, 12, oid="office_stool")

    # ---- THE STAR-ROOM (rows 2-5, x14-18) ----------------------------------------
    wall_piece(objects, "star_window", 15, oid="star_window")
    place(objects, "card_stacks", 17, 4, oid="stacks_star")
    place(objects, "stool", 14, 3, oid="star_stool")

    warps = [
        {"id": "to_fold", "at": {"tx": DOOR_X, "ty": H - 1}, "trigger": "step_on",
         "to_map": "rimeway_fold", "to": {"tx": 24, "ty": 20}, "facing": "down",
         "transition": "door"},
    ]
    triggers = [
        # the output board (face it from the floor below its bottom row)
        {"id": "read_board", "kind": "script", "at": {"tx": 7, "ty": 3},
         "activation": "interact", "ref": "script.works_board"},
        # the star window (dusty until someone opens it)
        {"id": "star_window_look", "kind": "script", "at": {"tx": 15, "ty": 3},
         "activation": "interact", "ref": "script.works_window"},
        {"id": "stacks_look", "kind": "script", "at": {"tx": 4, "ty": 11},
         "activation": "interact", "ref": "script.works_stacks"},
    ]
    npcs = [
        # the overseer, across her desk
        npc("ketterly", 14, 8, "down", "star_watcher", "script.works_ketterly"),
        # the kin at the engines (creature NPCs)
        npc("engine_chillpip", 4, 6, "left", "kin_77_overworld", "script.works_engine_kin"),
        npc("engine_snowcune", 10, 7, "up", "kin_80_overworld", "script.works_engine_kin"),
        # the clerks — at work until the story ...
        npc("clerk_hollis", 2, 10, "up", "npc_man", "script.works_hollis", hidden_when_flag=STORY),
        npc("clerk_teague", 11, 10, "up", "npc_woman", "script.works_teague", hidden_when_flag=STORY),
        npc("clerk_brann", 6, 7, "up", "npc_old_man", "script.works_brann", hidden_when_flag=STORY),
        npc("clerk_nib", 8, 8, "up", "npc_girl", "script.works_nib", hidden_when_flag=STORY),
        # ... and home again, one by one, as you find them out wandering
        npc("clerk_hollis_back", 2, 10, "up", "npc_man", "script.works_hollis",
            requires_flag="flag:works_found_hollis"),
        npc("clerk_teague_back", 11, 10, "up", "npc_woman", "script.works_teague",
            requires_flag="flag:works_found_teague"),
        npc("clerk_brann_back", 6, 7, "up", "npc_old_man", "script.works_brann",
            requires_flag="flag:works_found_brann"),
        # Nib keeps the star-room from the story on (the window's new keeper)
        npc("nib_star", 16, 4, "up", "npc_girl", "script.works_nib", requires_flag=STORY),
    ]
    return mapdef("reckoning_works", "The Reckoning-Works", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/reckoning-aurora.mp3")


if __name__ == "__main__":
    ok = finish(build())
    print("content refs owed (src/game/content/regions/reckonworks.ts):")
    for ref in OWED:
        print(f"  - {ref}")
    print("DONE" if ok else "DONE (with audit failures)")
    raise SystemExit(0 if ok else 1)
