#!/usr/bin/env python3
"""
Nightreach Observatory interiors (docs/world/interiors.md, on roomkit):

  * nightreach_lumenary — Nessa's Lunar hall, the star-temple SANCTUM: cool
    stone register, telescope brass + indigo (the MIN-1 re-skin: this hall is
    an observatory chancel, no other warden's dressing). THE GREAT EYEPIECE
    (bespoke 3x3, the telescope's lower barrel descending out of the dome) is
    the focal on the dais; the EIGHTH WATCH-LAMP stands at its side — dark
    until the eighth constellation answers (MapObject flag-swap pair on
    gleam:lunar, same footprint + solidity). A pale-flame brazier flanks the
    west side (the starlight register — cold light, not hearth-fire); star
    banners on the face; the star-ledger niche west, the chart niche east;
    vigil lamps flank the door; pews where the watchers keep the vigil.
    THE BOND-TEST is here: the dais cut (the only approach to Nessa at the
    eyepiece) is banded with script.lumenary_nightreach — requires
    flag:q_west_vigil_kept (the 7th lamp set it), blocked_ref
    npc.nessa_not_ready (her voice), hidden once gleam:lunar.
    TRAINERS['nessa_cole']: warden class ai:'smart', ace ~52, payout 60x52 =
    3120, reward_flags ['gleam:lunar'] + reward_abilities ['starreach'] — the
    Lampwarden grant pattern; with gleam:solar already held the ENGINE derives
    flag:crown_west AND (last quadrant) flag:hub_unlocked. NEVER hand-set.
    Nessa is FOUR flag-disjoint placements on the dais tile (the Fenn
    waystone pattern): hook (script.nessa_quest, sets flag:q_west_vigil) ->
    keeping (npc.nessa_keeping, while the walk is lit; hidden at
    flag:q_west_lamp_6 — she has gone up to the seventh lamp, where
    script.great_null_named plays out at the great telescope outdoors) ->
    ready (npc.nessa_cole, back at the eyepiece once flag:q_west_lamp_7) ->
    after (npc.nessa_after, gleam:lunar). ZERO humour in this hall.

  * nightreach_inn  — "The Long Watch" (the town's rest point): hearth, bunk
    room behind a partition, keeper's full rest-heal
    (script.nightreach_inn_rest — the standing kit). The inn guest carries
    the cluster's ONE permitted dry line; suggested copy:
      npc.nightreach_inn_guest "Eight years I've kept the quietest watch in
      Vesperholm, and the sky saves all its history for the week I booked
      off. Wake me if the dawn comes in."
    Everything else in the cluster stays reverent.

  * nightreach_home — a watcher household: hearth-room + bed nook; the elder
    ground the dome's first lens, the kid keeps a paper star-chart.

Door pairings (audit_warps enforces):
  town `to_lumenary`/`to_lumenary_e` at (15,9)/(16,9) land at our (8,11);
    our `to_town` at (8,11) lands the dome apron (15,10).
  town `to_inn` at (6,19) lands (7,10); our `to_town` lands (6,20).
  town `to_home` at (24,19) lands (6,8); our `to_town` lands (24,20).

Run:  ./venv/bin/python tools/maps/build_nightreach_interiors.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, COOL_SET, faced_room, windows, partition_v,
                     place, wall_mount, aisle_runner, mapdef, finish)

OWED = [
    "script.nessa_quest (the hook, from the eyepiece — 'Seven watch-fires for "
    "seven stars you've already given back...'; sets flag:q_west_vigil)",
    "npc.nessa_keeping (while the walk is being lit)",
    "npc.nessa_cole (back at the eyepiece, flag:q_west_lamp_7 held)",
    "npc.nessa_not_ready (bond-test blocked_ref, her voice)",
    "script.lumenary_nightreach (the bond-test: battle vs TRAINERS['nessa_cole'] "
    "— warden class ai:'smart', ace ~52, payout 60x52=3120, reward_flags "
    "['gleam:lunar'] + reward_abilities ['starreach']; engine derives "
    "flag:crown_west + flag:hub_unlocked — never hand-set. The Gleam cadence "
    "at full reverence: hold a silence, bloom the cool tint, fire gleam as the "
    "eighth watch-lamp lights itself, crossfade to the Star-vigil swell)",
    "npc.nessa_after (requires gleam:lunar)",
    "npc.nightreach_hall_keeper (the night-clerk at the star-ledger)",
    "npc.nightreach_hall_festival (requires gleam:lunar — the hall answers)",
    "script.nightreach_inn_rest (ends in the heal op — the standing kit)",
    "npc.nightreach_inn_guest (the cluster's ONE dry line — copy in docstring)",
    "npc.nightreach_inn_watcher (a vigil-keeper turning in at dawn-watch)",
    "npc.nightreach_home_elder (ground the dome's first lens)",
    "npc.nightreach_home_kid (keeps a paper star-chart of the relit eight)",
]


def build_lumenary():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    # the star-ledger niche west + the chart niche east (rooms within the room)
    partition_v(over, W, 4, 1, 4, lip="e")
    partition_v(over, W, 12, 1, 4, lip="w")

    objects: list = []
    # the carpet aisle (drawn runner objects — never the doormat tile)
    aisle_runner(objects, door_x, 6, H - 2)
    # THE LUNAR IDENTITY: indigo banners on the face, THE GREAT EYEPIECE on
    # the dais, the EIGHTH WATCH-LAMP at its side (dark -> lit on gleam:lunar)
    wall_mount(objects, "banner_ice", 6, oid="banner_l", solid=False)
    wall_mount(objects, "banner_ice", 11, oid="banner_r", solid=False)
    objects += [
        {"id": "great_eyepiece", "sprite": "nightreach_eyepiece",
         "at": {"tx": 7, "ty": 2}, "w": 3, "h": 3},
        # the eighth watch-lamp — east flank of the dais (the swap pair MUST
        # share footprint + solidity; collision is flag-blind)
        {"id": "watch_lamp_8_dark", "sprite": "nightreach_watch_lamp_dark",
         "at": {"tx": 10, "ty": 3}, "w": 2, "h": 3,
         "hidden_when_flag": "gleam:lunar"},
        {"id": "watch_lamp_8_lit", "sprite": "nightreach_watch_lamp_lit",
         "at": {"tx": 10, "ty": 3}, "w": 2, "h": 3,
         "requires_flag": "gleam:lunar"},
        # the pale-flame brazier — west flank (cold starlight, not hearth-fire)
        {"id": "brazier_w", "sprite": "pale_vault_brazier",
         "at": {"tx": 4, "ty": 3}, "w": 2, "h": 3},
        # vigil lamps flank the door (the Star-vigil's small brave lights)
        {"id": "vigil_lamp_l", "sprite": "nightreach_vigil_lamp",
         "at": {"tx": 2, "ty": 9}, "w": 1, "h": 2},
        {"id": "vigil_lamp_r", "sprite": "nightreach_vigil_lamp",
         "at": {"tx": 13, "ty": 9}, "w": 1, "h": 2},
    ]
    # west niche: the star-ledger (every vigil kept, every star come home)
    wall_mount(objects, "bookcase", 1, oid="star_ledger")
    place(objects, "stool", 2, 4, oid="ledger_stool")
    # east niche: the chart shelf + her working table
    wall_mount(objects, "shelf", 13, oid="chart_shelf")
    place(objects, "table", 13, 6, oid="chart_table")
    place(objects, "stool", 12, 7, oid="chart_stool")
    # pews where the watchers keep the vigil
    place(objects, "pew", 4, 8, oid="pew_l")
    place(objects, "pew", 10, 8, oid="pew_r")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "nightreach_observatory", "to": {"tx": 15, "ty": 10},
         "facing": "down", "transition": "door"},
    ]
    # THE BOND-TEST BAND — the dais cut: with the brazier (4-5) and the eighth
    # lamp (10-11) solid through row 5 and Nessa herself on (8,5), the only
    # cells that reach the eyepiece are (6,5), (7,5) and (9,5). Band exactly
    # those (the whole walkable cut, only walkable cells).
    triggers = []
    for i, tx in enumerate((6, 7, 9)):
        triggers.append({
            "id": f"lumenary_battle_{i}", "kind": "cutscene",
            "at": {"tx": tx, "ty": 5}, "activation": "step_on",
            "ref": "script.lumenary_nightreach", "once": True,
            "requires_flag": "flag:q_west_vigil_kept",
            "blocked_ref": "npc.nessa_not_ready",
            "hidden_when_flag": "gleam:lunar"})

    # Nessa at the eyepiece — four flag-disjoint placements on one tile.
    # (Lamp 7's trigger also sets flag:q_west_vigil, so the hook placement can
    # never coexist with her post-walk stages even if the player skipped her.)
    npcs = [
        {"id": "nessa_hook", "at": {"tx": 8, "ty": 5}, "facing": "down",
         "sprite": "nessa_cole", "movement": "static",
         "dialogue_ref": "script.nessa_quest",
         "hidden_when_flag": "flag:q_west_vigil"},
        {"id": "nessa_keeping", "at": {"tx": 8, "ty": 5}, "facing": "up",
         "sprite": "nessa_cole", "movement": "static",
         "dialogue_ref": "npc.nessa_keeping",
         "requires_flag": "flag:q_west_vigil",
         "hidden_when_flag": "flag:q_west_lamp_6"},
        # (between lamps 6 and 7 she stands at the seventh lamp outdoors)
        {"id": "nessa_ready", "at": {"tx": 8, "ty": 5}, "facing": "down",
         "sprite": "nessa_cole", "movement": "static",
         "dialogue_ref": "npc.nessa_cole",
         "requires_flag": "flag:q_west_lamp_7",
         "hidden_when_flag": "gleam:lunar"},
        {"id": "nessa_after", "at": {"tx": 8, "ty": 5}, "facing": "down",
         "sprite": "nessa_cole", "movement": "static",
         "dialogue_ref": "npc.nessa_after",
         "requires_flag": "gleam:lunar"},
        # the night-clerk at the star-ledger
        {"id": "hall_keeper", "at": {"tx": 2, "ty": 6}, "facing": "down",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.nightreach_hall_keeper"},
        # Arc E payoff: the hall answers the eighth Gleam (standing kit)
        {"id": "hall_festival", "at": {"tx": 12, "ty": 8}, "facing": "left",
         "sprite": "npc_woman", "movement": "look_around",
         "dialogue_ref": "npc.nightreach_hall_festival",
         "requires_flag": "gleam:lunar"},
    ]
    return mapdef("nightreach_lumenary", "Lunar Lumenary", W, H, COOL_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/nightreach-observatory-b.mp3")


def build_inn():
    W, H = 14, 11
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [4, 11])
    # the bunk room behind a partition — watchers sleep out the dawn-watch
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
    place(objects, "barrels", 1, 3, oid="cellar_casks")
    place(objects, "sacks", 12, 8, oid="grain")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "nightreach_observatory", "to": {"tx": 6, "ty": 20},
         "facing": "down", "transition": "door"},
    ]
    npcs = [
        # the keeper's rest-heal (script ends in the `heal` op — standing kit)
        {"id": "innkeeper", "at": {"tx": 6, "ty": 4}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.nightreach_inn_rest"},
        # the ONE dry line lives here (see docstring) — nowhere else
        {"id": "guest", "at": {"tx": 3, "ty": 6}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.nightreach_inn_guest"},
        {"id": "watcher_off_shift", "at": {"tx": 11, "ty": 6}, "facing": "left",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "npc.nightreach_inn_watcher"},
    ]
    return mapdef("nightreach_inn", "The Long Watch Inn", W, H, WARM_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/nightreach-observatory-b.mp3")


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
    place(objects, "oil_jars", 1, 7, oid="lamp_oil")
    place(objects, "plant", 10, 6, oid="sill_fern")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "nightreach_observatory", "to": {"tx": 24, "ty": 20},
         "facing": "down", "transition": "door"},
    ]
    npcs = [
        {"id": "home_elder", "at": {"tx": 4, "ty": 4}, "facing": "down",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.nightreach_home_elder"},
        {"id": "home_kid", "at": {"tx": 7, "ty": 6}, "facing": "left",
         "sprite": "npc_child", "movement": "wander",
         "dialogue_ref": "npc.nightreach_home_kid"},
    ]
    return mapdef("nightreach_home", "Watcher's Cottage", W, H, WARM_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/nightreach-observatory-b.mp3")


if __name__ == "__main__":
    ok = True
    for build in (build_lumenary, build_inn, build_home):
        ok = finish(build()) and ok
    print("content refs owed (register in src/game/content/):")
    for ref in OWED:
        print(f"  - {ref}")
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
