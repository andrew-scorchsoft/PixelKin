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
                  "assets/audio/music/inn-rest.mp3")


def build_crossroads_inn():
    """The Vesper Crossroads waystation inn — the cosy two-storey house from the
    crossroads concept art, now enterable. The C2 'Inn's Empty Lamps' innkeeper
    stages move here from the outdoor hub (an innkeeper belongs in an inn); a
    pre-quest welcome+rest keeps the inn hosted before the token quest opens."""
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    windows(over, W, [6, 14])
    partition_v(over, W, 5, 1, 6, lip="e")  # the western bunk bay

    objects: list = []
    place(objects, "bed_inn", 1, 2, oid="bed1")
    place(objects, "bed_inn", 3, 2, oid="bed2")
    place(objects, "plant", 1, 6)
    wall_mount(objects, "hearth", 8)
    wall_mount(objects, "lamp_rack", 12, solid=False)
    place(objects, "brazier", 14, 2, oid="brazier_e")
    # the innkeeper's bar, east of the hearth (its back row used to sit ON the
    # hearth's floor row); she keeps its west end, before the fire
    place(objects, "counter", 10, 4, oid="counter")
    place(objects, "table_long", 11, 7)
    place(objects, "stool", 11, 9, oid="stool_a")
    place(objects, "stool", 13, 9, oid="stool_b")
    place(objects, "table", 2, 8, oid="table_round")
    place(objects, "stool", 1, 8, oid="stool_c")
    place(objects, "rug", 7, 8, solid=False)

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "vesper_crossroads", "to": {"tx": 15, "ty": 15}, "facing": "down", "transition": "door"},
    ]
    triggers = [
        {"id": "sign_welcome", "kind": "sign", "at": {"tx": 14, "ty": 4}, "activation": "interact",
         "ref": "sign.crossroads_inn"},
    ]
    # The innkeeper (behind the counter): a pre-quest host, then the four C2
    # stages (strictly-ordered token chain) exactly as they ran outdoors.
    npcs = [
        {"id": "innkeeper_pre", "at": {"tx": 8, "ty": 4}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_rest_crossroads",
         "hidden_when_flag": "gleam:tide"},
        {"id": "innkeeper_ask", "at": {"tx": 8, "ty": 4}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_empty_lamps",
         "requires_flag": "gleam:tide",
         "hidden_when_flag": "flag:q_central_tokens"},
        {"id": "innkeeper_waiting", "at": {"tx": 8, "ty": 4}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_rest_waiting",
         "requires_flag": "flag:q_central_tokens",
         "hidden_when_flag": "flag:q_token_west"},
        {"id": "innkeeper_hang", "at": {"tx": 8, "ty": 4}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_lamps_hang",
         "requires_flag": "flag:q_token_west",
         "hidden_when_flag": "flag:q_central_tokens_done"},
        {"id": "innkeeper_done", "at": {"tx": 8, "ty": 4}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_rest_crossroads",
         "requires_flag": "flag:q_central_tokens_done"},
    ]
    return mapdef("crossroads_inn", "Vesper Crossroads Inn", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/inn-rest.mp3")


# =============================================================================
#  GYM (warm) — the Lifting House, two floors (gymforge.py draws the kit):
#    pearlmoor_lifting_house     18x12 street-level CARDIO hall (you walk in here)
#    pearlmoor_lifting_house_b1  15x10 the WEIGHTS floor down the stairs
# =============================================================================
_OBJ_MANIFEST = rk._MANIFEST


def gym(objects: list, stem: str, tx: int, ty: int, *, oid: str | None = None,
        solid: bool = True, overhang: int = 0, walk_under: bool = False) -> dict:
    """Place a gymforge piece (`gym_<stem>`) by its manifest footprint."""
    s = _OBJ_MANIFEST[f"gym_{stem}"]
    o = {"id": oid or stem, "sprite": f"gym_{stem}",
         "at": {"tx": tx, "ty": ty}, "w": s["tw"], "h": s["th"]}
    if overhang:
        o["overhang"] = overhang
    if walk_under:
        o["walk_under"] = True
    if not solid:
        o["solid"] = False
    objects.append(o)
    return o


def treadmill(objects: list, tx: int, ty: int, oid: str, *, runner: bool = False) -> None:
    """A 1x3 treadmill turned to FACE THE CAMERA: the belt on top, the console
    (seen from behind, solid) at the near end, so a runner on it shows his
    face. Under a runner the belt is solid:false so he can stand ON it (and
    you can step up behind him)."""
    gym(objects, "treadmill_belt_s", tx, ty, oid=f"{oid}_belt", solid=not runner)
    gym(objects, "treadmill_console_s", tx, ty + 2, oid=f"{oid}_console")


def build_lifting_house():
    W, H = 18, 12
    door_x = W // 2  # tx 9
    base, over = faced_room(W, H, door_x)
    windows(over, W, [3, 5, 7])

    objects: list = []
    # rubber matting under the bikes (laid first: drawn under; the treadmills
    # stay on the boards — their dark belts vanish against the rubber)
    for x in (11, 13, 15):
        for y in (4, 5):
            gym(objects, "mat", x, y, oid=f"mat_{x}_{y}", solid=False)
    # the class timetable (the house rules) on the north face, over the bikes
    wall_mount(objects, "chalkboard", 12, oid="timetable")
    # the treadmill row along the north-west wall — Andy runs the second one
    for i, x in enumerate((2, 4, 6, 8)):
        treadmill(objects, x, 2, f"treadmill_{i}", runner=(x == 4))
    # the bikes under the windows, east
    for i, x in enumerate((11, 13, 15)):
        gym(objects, "bike", x, 4, oid=f"bike_{i}")
    # the rowing machines mid-floor, west
    gym(objects, "rower", 2, 6, oid="rower_a")
    gym(objects, "rower", 6, 6, oid="rower_b")
    # the front desk by the door, the cooler, the towel crates, plants
    place(objects, "counter", 2, 8, oid="front_desk")
    gym(objects, "water_cooler", 16, 6, oid="cooler")
    place(objects, "plant", 1, 2, oid="plant_nw")
    place(objects, "plant", 16, 3, oid="plant_ne")
    place(objects, "stool", 6, 9, oid="desk_stool")

    warps = [
        {"id": "to_town", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 21, "ty": 5}, "facing": "down", "transition": "door"},
        # the stairwell down to the weights floor (dressed by roomkit.finish)
        {"id": "down_stairs", "at": {"tx": 15, "ty": 9}, "trigger": "step_on",
         "to_map": "pearlmoor_lifting_house_b1", "to": {"tx": 13, "ty": 2}, "facing": "down"},
    ]
    triggers = [
        # the house rules chalked on the timetable board
        {"id": "sign_rules", "kind": "sign", "at": {"tx": 13, "ty": 2}, "activation": "interact",
         "ref": "sign.lifting_house_rules"},
    ]
    # The Booji-Wooji Man side quest (S-line): Andy hooks it from the treadmill
    # (a stack of flag-disjoint stages on one tile, all running in place);
    # Abdul passes a clue along up here; Sid, Andrew and Rod lift downstairs.
    # Everyone in the gym faces the CAMERA at rest (owner's call: you want to see
    # them) and turns to whoever talks to them (Npc.facePoint).
    andy_at = {"tx": 4, "ty": 3}     # on treadmill_1's belt, running toward the console
    abdul_at = {"tx": 12, "ty": 7}   # stretching in front of the bikes
    andy = {"facing": "down", "sprite": "lifter_andy", "movement": "static",
            "in_place_walk": True}
    npcs = [
        {"id": "andy_hook", "at": dict(andy_at), **andy,
         "dialogue_ref": "script.booji_andy",
         "hidden_when_flag": "flag:q_south_booji"},
        {"id": "andy_wait", "at": dict(andy_at), **andy,
         "dialogue_ref": "script.booji_andy_wait",
         "requires_flag": "flag:q_south_booji",
         "hidden_when_flag": "flag:q_south_booji_met"},
        {"id": "andy_done", "at": dict(andy_at), **andy,
         "dialogue_ref": "script.booji_andy_done",
         "requires_flag": "flag:q_south_booji_met",
         "hidden_when_flag": "flag:q_south_booji_done"},
        {"id": "andy_after", "at": dict(andy_at), **andy,
         "dialogue_ref": "script.booji_andy_after",
         "requires_flag": "flag:q_south_booji_done"},
        # Abdul/Sid give clues but no longer GATE Paul (any lifter opens him). Their
        # clue is available from the start; their own flag just advances them to the
        # after-line.
        {"id": "abdul_clue", "at": dict(abdul_at), "facing": "down",
         "sprite": "lifter_abdul", "movement": "static",
         "dialogue_ref": "script.booji_abdul",
         "hidden_when_flag": "flag:q_south_booji_abdul"},
        {"id": "abdul_after", "at": dict(abdul_at), "facing": "down",
         "sprite": "lifter_abdul", "movement": "static",
         "dialogue_ref": "npc.booji_abdul_after",
         "requires_flag": "flag:q_south_booji_abdul"},
    ]
    return mapdef("pearlmoor_lifting_house", "The Lifting House", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/interior-sunny.mp3")


def build_lifting_house_b1():
    W, H = 15, 10
    base, over = faced_room(W, H, 7)
    # no street door down here: close the doormat back into the bottom wall
    base[(H - 1) * W + 7] = FLOOR
    over[(H - 1) * W + 7] = CAP_N

    objects: list = []
    # the rubber lifting floor under the bench-press bay (laid first: drawn under)
    for y in (4, 6, 7):
        for x in (1, 3, 5):
            gym(objects, "mat", x, y, oid=f"mat_{x}_{y}", solid=False)
    # mirrors along the north face, over the dumbbells
    for i, x in enumerate((1, 3, 5, 7, 9)):
        gym(objects, "mirror", x, 1, oid=f"mirror_{i}", solid=False)
    # the dumbbell rack under the mirrors, the plate tree + kettlebells beside it
    gym(objects, "dumbbell_rack", 4, 2, oid="dumbbells")
    gym(objects, "plate_tree", 8, 2, oid="plate_tree")
    gym(objects, "kettlebells", 9, 3, oid="kettlebells")
    gym(objects, "kettlebells", 1, 3, oid="kettlebells_w")
    # WEST: the bench presses
    gym(objects, "bench_press", 1, 5, oid="bench_a")
    gym(objects, "bench_press", 4, 5, oid="bench_b")
    # EAST: the squat racks (each on its own wooden platform)
    gym(objects, "squat_rack", 8, 5, oid="rack_a")
    gym(objects, "squat_rack", 11, 5, oid="rack_b")

    warps = [
        # the stair back up to the cardio hall (dressed by roomkit.finish)
        {"id": "up_stairs", "at": {"tx": 13, "ty": 2}, "trigger": "step_on",
         "to_map": "pearlmoor_lifting_house", "to": {"tx": 15, "ty": 9}, "facing": "left"},
    ]
    sid_at = {"tx": 3, "ty": 3}      # at the dumbbell rack's west end (off the lane)
    npcs = [
        # Andrew — the OTHER bench guy (not Andy; two separate lifters). Between
        # sets at bench_a, permanently; one flavour stage, no quest stack.
        {"id": "andrew", "at": {"tx": 2, "ty": 8}, "facing": "down",
         "sprite": "lifter_andrew", "movement": "static",
         "dialogue_ref": "npc.booji_andrew"},
        # Rod — the house's strongest AND oldest (an allotment-keeper of 72 who
        # squats the big rack). One flavour stage; he points on to Paul and
        # seeds the Chickenpig (never naming it).
        {"id": "rod", "at": {"tx": 12, "ty": 8}, "facing": "down",
         "sprite": "lifter_rod", "movement": "static",
         "dialogue_ref": "script.booji_rod"},
        {"id": "sid_clue", "at": dict(sid_at), "facing": "down",
         "sprite": "lifter_sid", "movement": "static",
         "dialogue_ref": "script.booji_sid",
         "hidden_when_flag": "flag:q_south_booji_sid"},
        {"id": "sid_after", "at": dict(sid_at), "facing": "down",
         "sprite": "lifter_sid", "movement": "static",
         "dialogue_ref": "npc.booji_sid_after",
         "requires_flag": "flag:q_south_booji_sid"},
    ]
    return mapdef("pearlmoor_lifting_house_b1", "The Lifting House: Weights", W, H, WARM_SET,
                  base, over, objects, warps, [], npcs,
                  "assets/audio/music/interior-sunny.mp3")


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
         # R8: the cottage now fronts the square (door (5,7)) — land on its apron.
         "to_map": "tinderwick", "to": {"tx": 5, "ty": 8}, "facing": "down", "transition": "door"},
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
        # Gran's travelling satchel, left out on the floor for your Wayfaring —
        # three balms to start you off (player-suggested, 2026-06). Always
        # available; vanishes once taken.
        {"id": "cache_gran_satchel", "at": {"tx": 8, "ty": 8}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_gran_satchel",
         "hidden_when_flag": "flag:picked_gran_satchel"},
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
        #   errand (Fenn asked)              -> "the courier carted it WEST, dear"
        #   kit    (Wayfaring begun, no kit) -> the one-time Wayfarer's kit
        #   plain  (kit given)               -> flavour
        # R8: Fenn's satchel no longer sits by the counter — it rides the courier's
        # cart out to Duskapple Orchard (build_duskapple_orchard.py; same placement
        # id + script.take_satchel -> flag:has_satchel). The store moved too: its
        # door is now (6,16) down the lower-left lane, so we land on (6,17).
        build_shop("tinderwick_shop", "Tinderwick General Store",
                   "assets/audio/music/shop-counter.mp3", ("tinderwick", 6, 17),
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
                   ]),
        # The Ember Lumenary HALL: no battle here any more — the bond-test waits
        # at the BEACON TOP (the earned first Gleam). Brisa stages the quest from
        # the dais: catch-first -> the wick-key errand -> "meet me at the lantern"
        # -> the post-Gleam festival line. Pure flag-pair NPC swaps.
        build_lumenary("tinderwick_lumenary", "Tinderwick Lumenary",
                       "assets/audio/music/lumenary-hall.mp3", ("tinderwick", 19, 8),
                       None, "sign.tinderwick_lumenary_inside",
                       "brisa", "npc.brisa_tallow",
                       npcs_override=[
                           {"id": "brisa_pre", "at": "dais", "facing": "down",
                            "sprite": "brisa", "movement": "static",
                            "dialogue_ref": "npc.brisa_not_ready",
                            "hidden_when_flag": "flag:caught_first_kin"},
                           {"id": "brisa_quest", "at": "dais", "facing": "down",
                            "sprite": "brisa", "movement": "static",
                            "dialogue_ref": "script.brisa_quest",
                            "requires_flag": "flag:caught_first_kin",
                            "hidden_when_flag": "flag:has_beacon_wick"},
                           {"id": "brisa_ready", "at": "dais", "facing": "down",
                            "sprite": "brisa", "movement": "static",
                            "dialogue_ref": "npc.brisa_meet_beacon",
                            "requires_flag": "flag:has_beacon_wick",
                            "hidden_when_flag": "gleam:ember"},
                           {"id": "brisa_fair", "at": "dais", "facing": "down",
                            "sprite": "brisa", "movement": "static",
                            "dialogue_ref": "script.brisa_after_staged",  # W-1 witness stage (content/regions/west.ts)
                            "requires_flag": "gleam:ember"},
                       ]),
        # The Tide Lumenary: the bond-test is EARNED (the Causeway Bell loop,
        # walkthrough/01-south) — the battle trigger waits on the Moor-bell
        # (`flag:q_south_bell_rung`, blocked in Reyl's own voice), and Reyl
        # stages the quest from the dais: hook -> waiting -> ready -> festival.
        build_lumenary("pearlmoor_lumenary", "Pearlmoor Tide Lumenary",
                       "assets/audio/music/lumenary-hall.mp3", ("pearlmoor_quay", 14, 7),
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
                            "dialogue_ref": "script.reyl_waiting",
                            "requires_flag": "flag:q_south_bell",
                            "hidden_when_flag": "flag:q_south_bell_rung"},
                           {"id": "reyl", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "npc.reyl_wash",
                            "requires_flag": "flag:q_south_bell_rung",
                            "hidden_when_flag": "gleam:tide"},
                           {"id": "reyl_after", "at": "dais", "facing": "down",
                            "sprite": "npc_lampwarden", "movement": "static",
                            "dialogue_ref": "script.reyl_after",
                            "requires_flag": "gleam:tide"},
                       ]),
        build_shop("pearlmoor_shop", "Pearlmoor Chandlery",
                   "assets/audio/music/shop-counter.mp3", ("pearlmoor_quay", 5, 12),
                   "sign.pearlmoor_shop", "chandler", "script.shop_pearlmoor",
                   kit_script="script.shop_kit_pearlmoor", kit_flag="flag:pearlmoor_kit",
                   chandlery=True),
        build_inn(),
        # (was never in this list — the shipped JSON had drifted from its builder
        # and check_rebuild could not see it; 2026-10 interior pass)
        build_crossroads_inn(),
        build_lifting_house(),
        build_lifting_house_b1(),
    ]


if __name__ == "__main__":
    ok = True
    for m in all_maps():
        ok = finish(m) and ok
    print("DONE" if ok else "DONE (with audit failures)")
