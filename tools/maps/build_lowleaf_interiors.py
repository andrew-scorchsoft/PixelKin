#!/usr/bin/env python3
"""
Lowleaf Hollow interiors (docs/world/interiors.md, on roomkit):

  * lowleaf_lumenary — Sable Quill's Verdant hall: the cool stone register
    grown over into a LIVING MOSS-GARDEN. Hers, specifically: a shy botanist's
    hall — a curtained study nook full of pressed-leaf ledgers west (where she
    can hide from conversations), a glowing moss-garden bay east, planters
    where a grander hall would put pews, and the pinned letter (sign.cor_letter,
    the first whisper of Còr's voice) on her notice-board. Bond-test trigger
    on the aisle, gated on the Tended Bed (flag:q_east_bed_warm) with her own
    "not yet" (npc.sable_not_ready).
  * lowleaf_bower — the festival guest-bower (the town's rest point): warm
    register, a bunk nook behind a partition, the keeper's full rest-heal
    (script.lowleaf_rest).

Run:  ./venv/bin/python tools/maps/build_lowleaf_interiors.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, COOL_SET, BANNER, faced_room, windows, partition_v,
                     place, wall_mount, runner, aisle_runner, mapdef, finish)


def build_lumenary():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    # the study nook west (her hiding place) + the moss-garden bay east
    partition_v(over, W, 4, 1, 4, lip="e")
    partition_v(over, W, 12, 1, 4, lip="w")
    windows(over, W, [6, 10], tile=BANNER)

    objects: list = []
    # the carpet aisle (drawn runner objects, not the ladder-like doormat tile)
    aisle_runner(objects, door_x, 5, H - 2)
    # the focal moss-shrine on its dais, top-centre; braziers burn green-gold
    place(objects, "altar", door_x - 1, 2)
    place(objects, "brazier", 5, 3, oid="brazier_l")
    place(objects, "brazier", 11, 3, oid="brazier_r")
    # west: the study nook — pressed-leaf ledgers + her notice-board + a stool
    wall_mount(objects, "bookcase", 1, oid="ledgers")
    place(objects, "table", 2, 7, oid="study_table")
    place(objects, "stool", 1, 8, oid="study_stool")
    # east: the moss-garden bay — living glow-beds where offerings would be
    objects.append({"id": "moss_bay_teal", "sprite": "glowmoss_deep_glowshrooms_teal",
                    "at": {"tx": 13, "ty": 2}, "w": 2, "h": 2, "overhang": 1,
                    "walk_under": True})
    objects.append({"id": "moss_bay_ember", "sprite": "glowmoss_deep_glowshrooms_ember",
                    "at": {"tx": 13, "ty": 4}, "w": 2, "h": 2, "overhang": 1,
                    "walk_under": True})
    # planters flank the aisle where a grander hall would put pews
    place(objects, "plant", 5, 7, oid="planter_l1")
    place(objects, "plant", 11, 7, oid="planter_r1")
    place(objects, "plant", 5, 9, oid="planter_l2")
    place(objects, "plant", 11, 9, oid="planter_r2")
    place(objects, "pew", 10, 9, oid="visitors_bench")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "lowleaf_hollow", "to": {"tx": 10, "ty": 9}, "facing": "down",
         "transition": "door"},
    ]
    triggers = [
        # the bond-test, on the aisle south of the dais — gated on the Tended
        # Bed, blocked in Sable's own voice (the earned-loop grammar, §5)
        {"id": "lumenary_battle", "kind": "cutscene", "at": {"tx": door_x, "ty": 6},
         "activation": "step_on", "ref": "script.lumenary_lowleaf", "once": True,
         "requires_flag": "flag:q_east_bed_warm", "blocked_ref": "npc.sable_not_ready"},
        # THE PINNED LETTER — unsigned, courteous; the only Còr foreshadow a
        # careful player gets before Glowmoss Deep (B2 starts here, pays there)
        {"id": "cor_letter", "kind": "sign", "at": {"tx": 1, "ty": 3},
         "activation": "interact", "ref": "sign.cor_letter"},
    ]
    # Sable, four flag-disjoint stages at the dais (the standing giver-swap):
    # hook -> waiting (chain running) -> ready (bed warm) -> after (Gleam up).
    npcs = [
        {"id": "sable_quest", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "script.sable_quest",
         "hidden_when_flag": "flag:q_east_bloom"},
        {"id": "sable_waiting", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.sable_waiting",
         "requires_flag": "flag:q_east_bloom",
         "hidden_when_flag": "flag:q_east_bed_warm"},
        {"id": "sable", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.sable_ready",
         "requires_flag": "flag:q_east_bed_warm",
         "hidden_when_flag": "gleam:verdant"},
        {"id": "sable_after", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.sable_after",
         "requires_flag": "gleam:verdant"},
    ]
    return mapdef("lowleaf_lumenary", "Lowleaf Verdant Lumenary", W, H, COOL_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/lowleaf-hollow-b.mp3")


def build_bower():
    W, H = 14, 11
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [4, 11])
    # the bunk nook behind a partition — guests sleep off the common room
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
    place(objects, "barrels", 1, 3, oid="moss_ale")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "lowleaf_hollow", "to": {"tx": 24, "ty": 23}, "facing": "down",
         "transition": "door"},
    ]
    triggers = []
    npcs = [
        # the keeper's dialogue_ref is a SCRIPT ending in `heal` — the town's
        # rest point (the standing per-region kit)
        {"id": "bower_keeper", "at": {"tx": 5, "ty": 4}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.lowleaf_rest"},
        {"id": "bloom_guest", "at": {"tx": 4, "ty": 6}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.bower_guest"},
    ]
    return mapdef("lowleaf_bower", "Lowleaf Guest-bower", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/lowleaf-hollow-b.mp3")


if __name__ == "__main__":
    ok = True
    for m in (build_lumenary(), build_bower()):
        ok = finish(m) and ok
    print("DONE" if ok else "DONE (with audit failures)")
