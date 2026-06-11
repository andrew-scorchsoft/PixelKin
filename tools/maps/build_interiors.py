#!/usr/bin/env python3
"""
Rebuild ALL of PixelKin's building interiors to the binding spec in docs/world/interiors.md —
now as MULTI-ROOM compositions on the roomkit (tools/maps/roomkit.py):

  * the SNES enclosure (cap + visible north FACE) plus INTERNAL partitions in the
    same wall system — a cottage is a hearth-room with a bed nook, a shop has a
    storeroom, the inn a bunk room, a Lumenary its side niches: no more one-square
    same-y rooms;
  * furniture is the DRAWN interiorforge kit (straight-on, multi-tile): wall pieces
    (hearth/bookcase/shelf/dresser/stove/lamp-rack) go through `wall_mount` so they
    stand flush AGAINST the wall (top row over the face), free-standing pieces
    (beds/tables/counter/crates/…) through manifest-driven `place`;
  * every map ends with rk.finish(): write -> render -> audit_flow reach.

Two accent registers (build_interior_walls.py): WARM interior_set (homes, shops,
inns) and COOL interior_stone_set (Lumenaries — a shrine, never a cabin).

NPC stacks (the satchel-errand keeper stages, Brisa's quest stages, the inn
rest-heal) are wired exactly as before — only the rooms changed.

Run:  ./venv/bin/python tools/maps/build_interiors.py
"""
from __future__ import annotations

# re-exports for build_beacon.py (the tower floors ride the same kit)
from roomkit import (WARM_SET, COOL_SET, FLOOR, FLOOR_B, DOORMAT, FACE, WINDOW,
                     CAP_S, CAP_N, CAP_E, CAP_W, RUNNER, BANNER,
                     faced_room, windows, partition_v, partition_h,
                     place, wall_mount, runner, aisle_runner, mapdef, obj, finish,
                     write_and_render)
import roomkit as rk


# =============================================================================
#  LUMENARIES (cool register, shrine) — 16x12: nave + altar + side niches
# =============================================================================
def build_lumenary(id_, name, music, out_warp, script_ref, sign_ref, warden_id, warden_dialogue,
                   gate_flag="flag:has_starter", blocked_ref=None, npcs_override=None):
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    # side-niche stubs: short internal walls framing a west ledger-niche and an
    # east offering-niche — the nave reads as three bays, not one box
    partition_v(over, W, 4, 1, 3, lip="e")
    partition_v(over, W, 12, 1, 3, lip="w")
    # banners flank the dais on the face
    windows(over, W, [6, 10], tile=BANNER)
    objects: list = []
    # the carpet aisle from the doormat to the dais foot — drawn runner objects,
    # NOT the doormat tile repeated (that reads as a ladder, the dodgy-path look)
    aisle_runner(objects, door_x, 5, H - 2)
    # the focal lamp-shrine on its dais, top-centre
    place(objects, "altar", door_x - 1, 2)
    # braziers flanking the dais
    place(objects, "brazier", 5, 3, oid="brazier_l")
    place(objects, "brazier", 11, 3, oid="brazier_r")
    # west niche: the star-ledger shelves; east niche: offerings
    wall_mount(objects, "bookcase", 1, oid="ledger")
    place(objects, "barrels", 13, 2, oid="offerings")
    place(objects, "brazier", 14, 3, oid="brazier_e")
    # pew rows flanking the aisle (the congregation's bays)
    place(objects, "pew", 4, 7, oid="pew_l1")
    place(objects, "pew", 10, 7, oid="pew_r1")
    place(objects, "pew", 4, 9, oid="pew_l2")
    place(objects, "pew", 10, 9, oid="pew_r2")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": out_warp[0], "to": {"tx": out_warp[1], "ty": out_warp[2]},
         "facing": "down", "transition": "door"},
    ]
    triggers = [
        # the star-ledger (the readable lore shelf in the west niche)
        {"id": "sign_lumenary", "kind": "sign", "at": {"tx": 1, "ty": 3}, "activation": "interact",
         "ref": sign_ref},
    ]
    if script_ref:
        # step-on bond-test trigger on the aisle just south of where the warden stands
        battle_trigger = {"id": "lumenary_battle", "kind": "cutscene", "at": {"tx": door_x, "ty": 6},
                          "activation": "step_on", "ref": script_ref, "once": True,
                          "requires_flag": gate_flag}
        if blocked_ref:
            battle_trigger["blocked_ref"] = blocked_ref
        triggers.insert(0, battle_trigger)
    if npcs_override is not None:
        npcs = [dict(n, at={"tx": door_x, "ty": 5}) if n.get("at") == "dais" else n
                for n in npcs_override]
    else:
        npcs = [
            # the warden stands at the foot of the altar dais, on the runner
            {"id": warden_id, "at": {"tx": door_x, "ty": 5}, "facing": "down",
             "sprite": "npc_lampwarden", "movement": "static", "dialogue_ref": warden_dialogue},
        ]
    return mapdef(id_, name, W, H, COOL_SET, base, over, objects, warps, triggers, npcs, music)


# =============================================================================
#  SHOPS (warm) — 14x10: counter hall + a stocked storeroom behind a partition
# =============================================================================
def build_shop(id_, name, music, out_warp, sign_ref, keeper_id, keeper_dialogue,
               kit_script=None, kit_flag=None, npcs_override=None, chandlery=False):
    W, H = 14, 10
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [3])
    # the storeroom: an eastern bay behind an internal wall, entered from the
    # south — stacked stock the player can SEE but doesn't shop from
    partition_v(over, W, 10, 1, 4, lip="w")

    objects: list = []
    # wares flush against the north wall; hanging vesperlamps over the counter end
    wall_mount(objects, "shelf", 1, oid="wares")
    wall_mount(objects, "lamp_rack", 8, solid=False)
    # the counter spans mid-room; the keeper stands behind it
    place(objects, "counter", 4, 3)
    # the storeroom's stock
    place(objects, "crates", 11, 2)
    place(objects, "oil_jars" if chandlery else "barrels", 11, 4, oid="stock")
    # staging
    place(objects, "rug", 5, 6, solid=False)
    place(objects, "plant", 1, 8)

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": out_warp[0], "to": {"tx": out_warp[1], "ty": out_warp[2]},
         "facing": "down", "transition": "door"},
    ]
    triggers = [
        # the wares board on the shelf's lower row
        {"id": "sign_wares", "kind": "sign", "at": {"tx": 1, "ty": 3}, "activation": "interact",
         "ref": sign_ref},
    ]
    # keeper stages (the satchel-errand stack rides npcs_override; the kit/plain
    # pair rides the flags) — entries with at="counter" land behind the counter.
    npcs = []
    counter_at = {"tx": door_x - 1, "ty": 2}
    if npcs_override is not None:
        npcs = [dict(n, at=dict(counter_at)) if n.get("at") == "counter" else n
                for n in npcs_override]
    elif kit_script and kit_flag:
        npcs.append({"id": f"{keeper_id}_kit", "at": dict(counter_at), "facing": "down",
                     "sprite": "npc_shopkeeper", "movement": "static",
                     "dialogue_ref": kit_script, "hidden_when_flag": kit_flag})
        npcs.append({"id": keeper_id, "at": dict(counter_at), "facing": "down",
                     "sprite": "npc_shopkeeper", "movement": "static",
                     "dialogue_ref": keeper_dialogue, "requires_flag": kit_flag})
    else:
        npcs.append({"id": keeper_id, "at": dict(counter_at), "facing": "down",
                     "sprite": "npc_shopkeeper", "movement": "static", "dialogue_ref": keeper_dialogue})
    return mapdef(id_, name, W, H, WARM_SET, base, over, objects, warps, triggers, npcs, music)


# =============================================================================
#  INN (warm) — pearlmoor: 16x12 common room + a partitioned bunk room
# =============================================================================
def build_inn():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    windows(over, W, [6, 14])
    # the bunk room: the western bay behind a full-height partition, entered
    # round its south end — guests sleep OFF the common room
    partition_v(over, W, 5, 1, 6, lip="e")

    objects: list = []
    # bunk room: two made beds + a touch of green
    place(objects, "bed_inn", 1, 2, oid="bed1")
    place(objects, "bed_inn", 3, 2, oid="bed2")
    place(objects, "plant", 1, 6)
    # common room: the hearth is the focal wall piece; lamps hang by the corner
    wall_mount(objects, "hearth", 8)
    wall_mount(objects, "lamp_rack", 12, solid=False)
    place(objects, "brazier", 14, 2, oid="brazier_e")
    # tables: the long board + a round corner table, stools pulled up
    place(objects, "table_long", 11, 5)
    place(objects, "stool", 11, 7, oid="stool_a")
    place(objects, "stool", 13, 7, oid="stool_b")
    place(objects, "table", 2, 8, oid="table_round")
    place(objects, "stool", 1, 8, oid="stool_c")
    place(objects, "stool", 4, 9, oid="stool_d")
    place(objects, "rug", 7, 8, solid=False)

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 22, "ty": 12}, "facing": "down", "transition": "door"},
    ]
    triggers = [
        {"id": "sign_welcome", "kind": "sign", "at": {"tx": 14, "ty": 4}, "activation": "interact",
         "ref": "sign.pearlmoor_welcome"},
    ]
    npcs = [
        # The innkeep's dialogue_ref is a SCRIPT: talking to them runs the full
        # rest-heal beat (script.inn_rest) — the genre's heal loop, diegetic.
        {"id": "innkeep", "at": {"tx": 9, "ty": 4}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static", "dialogue_ref": "script.inn_rest"},
        {"id": "fisher", "at": {"tx": 12, "ty": 7}, "facing": "left",
         "sprite": "wren", "movement": "static", "dialogue_ref": "npc.pearlmoor_fisher"},
        # THE OLD FISHER (S3 "The Cavern Keeps a Light") — the long-game promise:
        # tale (post-bell) -> the wreck-lamp ask -> waiting on Glimmerstep (the
        # relight trigger ships with tideglass_cavern) -> thanks -> after.
        {"id": "old_fisher_pre", "at": {"tx": 14, "ty": 8}, "facing": "left",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.old_fisher_pre",
         "hidden_when_flag": "flag:q_south_bell_rung"},
        {"id": "old_fisher_tale", "at": {"tx": 14, "ty": 8}, "facing": "left",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "script.fisher_wrecklamp",
         "requires_flag": "flag:q_south_bell_rung",
         "hidden_when_flag": "flag:q_south_wrecklamp"},
        {"id": "old_fisher_wait", "at": {"tx": 14, "ty": 8}, "facing": "left",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.old_fisher_wait",
         "requires_flag": "flag:q_south_wrecklamp",
         "hidden_when_flag": "flag:q_south_wrecklamp_lit"},
        {"id": "old_fisher_thanks", "at": {"tx": 14, "ty": 8}, "facing": "left",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "script.fisher_thanks",
         "requires_flag": "flag:q_south_wrecklamp_lit",
         "hidden_when_flag": "flag:q_south_wrecklamp_done"},
        {"id": "old_fisher_after", "at": {"tx": 14, "ty": 8}, "facing": "left",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.old_fisher_after",
         "requires_flag": "flag:q_south_wrecklamp_done"},
    ]
    return mapdef("pearlmoor_inn", "Pearlmoor Quayside Inn", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/dimglass-coast-a.mp3")


# =============================================================================
#  HOME (warm cosy) — tinderwick_house: 14x11 hearth-room + bed nook + kitchen
# =============================================================================
def build_house():
    W, H = 14, 11
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [8, 11])
    # the bed nook: the apprentice's corner behind a partition, entered from
    # the south — a home with rooms in it, not a furniture square
    partition_v(over, W, 9, 1, 5, lip="w")

    objects: list = []
    # kitchen wall, west to east: the stove, the family bookcase, the hearth
    wall_mount(objects, "stove", 1)
    wall_mount(objects, "bookcase", 3)
    wall_mount(objects, "hearth", 5)
    place(objects, "sacks", 1, 3)
    place(objects, "barrels", 1, 8)
    # the nook: bed, a plant on the sill side, a stool
    place(objects, "bed", 10, 2)
    place(objects, "plant", 12, 2)
    place(objects, "stool", 12, 4)
    # the living floor: rug + round table + stools
    place(objects, "rug", 4, 6, solid=False)
    place(objects, "table", 4, 6, oid="table_round")
    place(objects, "stool", 6, 6, oid="stool_a")
    place(objects, "stool", 3, 7, oid="stool_b")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 6, "ty": 17}, "facing": "down", "transition": "door"},
    ]
    triggers = [
        {"id": "sign_shelf", "kind": "sign", "at": {"tx": 3, "ty": 3}, "activation": "interact",
         "ref": "sign.house_shelf"},
        # your own bed = a free full rest (interact with the bed's foot tile)
        {"id": "bed_rest", "kind": "script", "at": {"tx": 10, "ty": 4}, "activation": "interact",
         "ref": "script.home_rest"},
    ]
    # GRAN — six flag-disjoint stages on one tile (the standing giver-swap kit):
    #   pointer (pre-starter) -> the WARM keepsake beat (G4/F2: grandfather's
    #   brass wick-trimmer, before the road) -> the shaken post-omen witness +
    #   S2 "A Letter for Fenn" hook -> waiting -> thanks (balms) -> after.
    # External-event ordering is safe: every pre-omen stage hides on
    # `flag:dusk_begins`; everything later is talk-gated, so no two coexist.
    npcs = [
        {"id": "house_parent", "at": {"tx": 5, "ty": 5}, "facing": "down",
         "sprite": "npc_parent", "movement": "static", "dialogue_ref": "npc.house_parent",
         "hidden_when_flag": "flag:has_starter"},
        {"id": "house_parent_warm", "at": {"tx": 5, "ty": 5}, "facing": "down",
         "sprite": "npc_parent", "movement": "static", "dialogue_ref": "npc.house_parent_warm",
         "requires_flag": "flag:has_starter",
         "hidden_when_flag": "flag:dusk_begins"},
        {"id": "house_parent_letter", "at": {"tx": 5, "ty": 5}, "facing": "down",
         "sprite": "npc_parent", "movement": "static", "dialogue_ref": "script.gran_letter",
         "requires_flag": "flag:dusk_begins",
         "hidden_when_flag": "flag:q_south_letter"},
        {"id": "house_parent_wait", "at": {"tx": 5, "ty": 5}, "facing": "down",
         "sprite": "npc_parent", "movement": "static", "dialogue_ref": "npc.house_parent_wait",
         "requires_flag": "flag:q_south_letter",
         "hidden_when_flag": "flag:q_south_letter_given"},
        {"id": "house_parent_thanks", "at": {"tx": 5, "ty": 5}, "facing": "down",
         "sprite": "npc_parent", "movement": "static", "dialogue_ref": "script.gran_thanks",
         "requires_flag": "flag:q_south_letter_given",
         "hidden_when_flag": "flag:q_south_letter_done"},
        {"id": "house_parent_after", "at": {"tx": 5, "ty": 5}, "facing": "down",
         "sprite": "npc_parent", "movement": "static", "dialogue_ref": "npc.house_parent_after",
         "requires_flag": "flag:q_south_letter_done"},
    ]
    return mapdef("tinderwick_house", "Apprentice's House", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/tinderwick-b.mp3")


def all_maps():
    return [
        build_house(),
        # The Tinderwick keeper has FOUR flag-disjoint stages (the opening's satchel
        # errand runs through this counter before the kit/plain pair takes over):
        #   early  (t0)                      -> points the player east to Fenn
        #   errand (Fenn asked)              -> "satchel's by the counter, dear"
        #   kit    (Wayfaring begun, no kit) -> the one-time Wayfarer's kit
        #   plain  (kit given)               -> flavour
        # Plus Fenn's satchel itself: an item_cache beside the counter while the
        # errand runs (script.take_satchel -> flag:has_satchel).
        build_shop("tinderwick_shop", "Tinderwick General Store",
                   "assets/audio/music/tinderwick-b.mp3", ("tinderwick", 5, 8),
                   "sign.tinderwick_shop_wares", "shopkeeper", "npc.tinderwick_shopkeeper",
                   npcs_override=[
                       {"id": "shopkeeper_early", "at": "counter", "facing": "down",
                        "sprite": "npc_shopkeeper", "movement": "static",
                        "dialogue_ref": "npc.tinderwick_keeper_early",
                        "hidden_when_flag": "flag:fenn_errand"},
                       {"id": "shopkeeper_errand", "at": "counter", "facing": "down",
                        "sprite": "npc_shopkeeper", "movement": "static",
                        "dialogue_ref": "npc.tinderwick_keeper_errand",
                        "requires_flag": "flag:fenn_errand",
                        "hidden_when_flag": "flag:has_starter"},
                       {"id": "shopkeeper_kit", "at": "counter", "facing": "down",
                        "sprite": "npc_shopkeeper", "movement": "static",
                        "dialogue_ref": "script.shop_kit_tinderwick",
                        "requires_flag": "flag:has_starter",
                        "hidden_when_flag": "flag:tinderwick_kit"},
                       {"id": "shopkeeper", "at": "counter", "facing": "down",
                        "sprite": "npc_shopkeeper", "movement": "static",
                        "dialogue_ref": "script.shop_tinderwick",
                        "requires_flag": "flag:tinderwick_kit"},
                       {"id": "fenn_satchel", "at": {"tx": 3, "ty": 5}, "facing": "down",
                        "sprite": "item_cache", "movement": "static",
                        "dialogue_ref": "script.take_satchel",
                        "requires_flag": "flag:fenn_errand",
                        "hidden_when_flag": "flag:has_satchel"},
                   ]),
        # The Ember Lumenary HALL: no battle here any more — the bond-test waits
        # at the BEACON TOP (the earned first Gleam). Brisa stages the quest from
        # the dais: catch-first -> the wick-key errand -> "meet me at the lantern"
        # -> the post-Gleam festival line. Pure flag-pair NPC swaps.
        build_lumenary("tinderwick_lumenary", "Tinderwick Lumenary",
                       "assets/audio/music/tinderwick-a.mp3", ("tinderwick", 19, 8),
                       None, "sign.tinderwick_lumenary_inside",
                       "brisa", "npc.brisa_tallow",
                       npcs_override=[
                           {"id": "brisa_pre", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "npc.brisa_not_ready",
                            "hidden_when_flag": "flag:caught_first_kin"},
                           {"id": "brisa_quest", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "script.brisa_quest",
                            "requires_flag": "flag:caught_first_kin",
                            "hidden_when_flag": "flag:has_beacon_wick"},
                           {"id": "brisa_ready", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "npc.brisa_meet_beacon",
                            "requires_flag": "flag:has_beacon_wick",
                            "hidden_when_flag": "gleam:ember"},
                           {"id": "brisa_fair", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "npc.brisa_after",
                            "requires_flag": "gleam:ember"},
                       ]),
        # The Tide Lumenary: the bond-test is EARNED (the Causeway Bell loop,
        # walkthrough/01-south) — the battle trigger waits on the Moor-bell
        # (`flag:q_south_bell_rung`, blocked in Reyl's own voice), and Reyl
        # stages the quest from the dais: hook -> waiting -> ready -> festival.
        build_lumenary("pearlmoor_lumenary", "Pearlmoor Tide Lumenary",
                       "assets/audio/music/dimglass-coast-a.mp3", ("pearlmoor_quay", 14, 7),
                       "script.lumenary_pearlmoor", "sign.pearlmoor_lumenary",
                       "reyl", "npc.reyl_wash",
                       gate_flag="flag:q_south_bell_rung",
                       blocked_ref="npc.reyl_blocked",
                       npcs_override=[
                           {"id": "reyl_quest", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "script.reyl_quest",
                            "hidden_when_flag": "flag:q_south_bell"},
                           {"id": "reyl_waiting", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "npc.reyl_waiting",
                            "requires_flag": "flag:q_south_bell",
                            "hidden_when_flag": "flag:q_south_bell_rung"},
                           {"id": "reyl", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "npc.reyl_wash",
                            "requires_flag": "flag:q_south_bell_rung",
                            "hidden_when_flag": "gleam:tide"},
                           {"id": "reyl_after", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "npc.reyl_after",
                            "requires_flag": "gleam:tide"},
                       ]),
        build_shop("pearlmoor_shop", "Pearlmoor Chandlery",
                   "assets/audio/music/dimglass-coast-a.mp3", ("pearlmoor_quay", 5, 12),
                   "sign.pearlmoor_shop", "chandler", "script.shop_pearlmoor",
                   kit_script="script.shop_kit_pearlmoor", kit_flag="flag:pearlmoor_kit",
                   chandlery=True),
        build_inn(),
    ]


if __name__ == "__main__":
    ok = True
    for m in all_maps():
        ok = finish(m) and ok
    print("DONE" if ok else "DONE (with audit failures)")
