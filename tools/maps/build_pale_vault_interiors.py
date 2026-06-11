#!/usr/bin/env python3
"""
Pale Vault Glacier interiors (docs/world/interiors.md, on roomkit):

  * pale_vault_lumenary — Ysolde's Frost hall: cool stone register, a quiet
    GLACIER identity — the Frost altar on its dais, an aurora-oil store west
    (the Lamp-Line's fuel: oil jars + barrels), a star-ledger niche east. NO
    bond-test here: Ysolde fights at the UNDERCROFT's heart (walkthrough
    03-north beat 8); the hall is the Aurora-watch's home and where she
    returns once gleam:frost is held.
  * pale_vault_inn      — the glacier inn (the town's rest point): hearth,
    bunk room behind a partition, keeper's full rest-heal
    (script.pale_vault_inn_rest — the standing kit). The inn guest carries
    the cluster's ONE permitted dry line; everything else stays sincere
    (the Aurora-watch is a silent vigil).
  * pale_vault_home     — an ice-block cottage: hearth-room + bed nook, a
    quiet watcher household.

No shop: the walkthrough names no Pale Vault provisioner (the town is
deliberately sparse — resupply lives on the Galehigh drop-shortcut loop).

Run:  ./venv/bin/python tools/maps/build_pale_vault_interiors.py
"""
from __future__ import annotations

from roomkit import (WARM_SET, COOL_SET, BANNER, faced_room, windows, partition_v,
                     place, wall_mount, aisle_runner, mapdef, finish)

OWED = [
    "npc.pale_vault_hall_keeper",
    "npc.ysolde_hall_after (requires gleam:frost — Ysolde home from the vault)",
    "npc.pale_vault_hall_festival (requires gleam:frost)",
    "script.pale_vault_inn_rest (ends in the heal op)",
    "npc.pale_vault_inn_guest (the cluster's ONE dry line)",
    "npc.pale_vault_home_elder", "npc.pale_vault_home_kid",
]


def build_lumenary():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    # the aurora-oil store west + the star-ledger niche east
    partition_v(over, W, 4, 1, 4, lip="e")
    partition_v(over, W, 12, 1, 4, lip="w")
    windows(over, W, [6, 10], tile=BANNER)

    objects: list = []
    # the carpet aisle (drawn runner objects — never the doormat tile)
    aisle_runner(objects, door_x, 5, H - 2)
    # the Frost altar on its dais, braziers flanking (the vigil's lamps)
    place(objects, "altar", door_x - 1, 2)
    place(objects, "brazier", 5, 3, oid="brazier_l")
    place(objects, "brazier", 11, 3, oid="brazier_r")
    # west: the aurora-oil store — the Lamp-Line's fuel kept against the wall
    wall_mount(objects, "shelf", 1, oid="oil_shelf")
    place(objects, "oil_jars", 1, 7, oid="aurora_oil")
    place(objects, "barrels", 2, 4, oid="tallow_casks")
    # east: the star-ledger niche
    wall_mount(objects, "bookcase", 13, oid="star_ledger")
    place(objects, "table", 13, 7, oid="ledger_table")
    place(objects, "stool", 12, 8, oid="ledger_stool")
    # pews where the town keeps the watch
    place(objects, "pew", 5, 8, oid="pew_l")
    place(objects, "pew", 10, 8, oid="pew_r")
    wall_mount(objects, "lamp_rack", 6, solid=False)

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "pale_vault_glacier", "to": {"tx": 14, "ty": 9}, "facing": "down",
         "transition": "door"},
    ]
    # the hall-keeper tends the altar (Ysolde keeps the undercroft until the
    # Gleam); Ysolde + a festival witness join once gleam:frost stands (Arc E)
    npcs = [
        {"id": "hall_keeper", "at": {"tx": door_x, "ty": 5}, "facing": "down",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "npc.pale_vault_hall_keeper"},
        {"id": "ysolde_after", "at": {"tx": door_x - 1, "ty": 4}, "facing": "down",
         "sprite": "ysolde_frost", "movement": "static",
         "dialogue_ref": "npc.ysolde_hall_after",
         "requires_flag": "gleam:frost"},
        {"id": "hall_festival", "at": {"tx": 10, "ty": 7}, "facing": "left",
         "sprite": "npc_woman", "movement": "look_around",
         "dialogue_ref": "npc.pale_vault_hall_festival",
         "requires_flag": "gleam:frost"},
    ]
    return mapdef("pale_vault_lumenary", "Pale Vault Frost Lumenary", W, H, COOL_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/pale-vault-glacier-b.mp3")


def build_inn():
    W, H = 14, 11
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [4, 11])
    # the bunk room behind a partition — watchers sleep before the vigil
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
         "to_map": "pale_vault_glacier", "to": {"tx": 5, "ty": 9}, "facing": "down",
         "transition": "door"},
    ]
    npcs = [
        # the keeper's rest-heal (script ends in the `heal` op — standing kit)
        {"id": "innkeeper", "at": {"tx": 6, "ty": 4}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.pale_vault_inn_rest"},
        {"id": "guest", "at": {"tx": 3, "ty": 6}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.pale_vault_inn_guest"},
    ]
    return mapdef("pale_vault_inn", "The Held Flame Inn", W, H, WARM_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/pale-vault-glacier-b.mp3")


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
         "to_map": "pale_vault_glacier", "to": {"tx": 26, "ty": 8}, "facing": "down",
         "transition": "door"},
    ]
    npcs = [
        {"id": "home_elder", "at": {"tx": 4, "ty": 4}, "facing": "down",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.pale_vault_home_elder"},
        {"id": "home_kid", "at": {"tx": 7, "ty": 6}, "facing": "left",
         "sprite": "npc_child", "movement": "wander",
         "dialogue_ref": "npc.pale_vault_home_kid"},
    ]
    return mapdef("pale_vault_home", "Glacier Cottage", W, H, WARM_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/pale-vault-glacier-b.mp3")


if __name__ == "__main__":
    ok = True
    for build in (build_lumenary, build_inn, build_home):
        ok = finish(build()) and ok
    print("content refs owed (register in src/game/content/):")
    for ref in OWED:
        print(f"  - {ref}")
    print("DONE" if ok else "DONE (with audit failures)")
    raise SystemExit(0 if ok else 1)
