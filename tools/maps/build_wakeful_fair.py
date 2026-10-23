#!/usr/bin/env python3
"""
THE WAKEFUL FAIR — the great coffee festival in the marquee on Wayward Rise
(S7 "Just One More Cup", 2026-10). Content: src/game/content/regions/brewfair.ts.
Art: tools/maps/brewforge.py (the drawn `brewfair_*` pieces) + the two re-skinned
kits from build_brewfair_sets.py. Placed by build_wayward_rise.py (the marquee).

The fair is Paul's story, retold for the player. He went to a coffee festival once
and tried everything, because everywhere had free samples and he could not say no
— and before he knew it he was very nearly hallucinating. So: every stall pours you
a sample (a numbered `flag:brewcup_<n>`), and how many you've had is how strange the
marquee gets (FlagStore COUNT_AT_LEAST: brew_perky at 3, brew_buzzing at 7,
brew_seeing at 12). The caffeine is also the KEY — the fair opens up as you drink:

  * PERKY (3)    you talk so fast the TRADE ONLY steward takes you for a buyer:
                 the stair up to the Roasters' Loft (`flag:brew_was_perky`).
  * BUZZING (7)  you vibrate straight through the queue for the Siphon Lab
                 (`flag:brew_was_buzzing`); the Stall That Isn't There appears
                 (non-solid — it isn't there; you can walk right through it).
  * SEEING (12)  the Grand Urn wakes up and sings, every brewer is a kin, and the
                 puddle at the urn's foot is the way down into the cup.

Three maps, all roomkit interiors:

  wakeful_fair       30x21  THE MARQUEE (brewfair_set). Door (15,20) <- the Rise.
      north wall: the pour-over bar, the sand-pot, the cold-drip; the cup-record
      chalkboard between them; the TRADE ONLY stair (1,2) in the NW corner behind
      the bean sacks. The SIPHON LAB is the walled NE wing (x 23-28, y 2-7), its
      one doorway (22,5) full of queue. The GRAND URN stands in the middle on its
      dais (13,8) — you walk ROUND it — with the espresso, press and mushroom
      stalls on the middle row and Percy's moka stand, the latte artist and the
      decaf stall on the south row. The QUIET TENT (the decaf corner's first aid)
      is walled off in the SE (x 23-28, y 15-19; door 25,13-14): cots, a water
      table nobody visits, the medic, and the plaque with the cup record. Sample
      Sal, the free-sample hawker, works the east corridor (sight 5).
  wakeful_fair_loft  20x13  THE ROASTERS' LOFT (brewfair_set) — up the stair.
      the frost-brew, the Dawnbean and the Midnight Oil on the north wall, the big
      drum roaster in the NE, the CUPPING TABLE, the Championship stage + the
      Golden Cup, and Free-Sample Fred (sight 8) on the south aisle.
  wakeful_fair_dream 24x18  THE BOTTOM OF THE CUP (brewdream_set). The hallucination.
      You arrive by the door that stands on its own in the foam (it leads back);
      the floor between you and the Bottomless Cup is a CARAMEL SLICK (an `ice`
      flow — slide until something stops you) studded with sugar cubes, coffee
      beans and giant spoons. Proven here: the inlet below the cup (13,5) is
      reachable, takes 17 presses at best, and no resting place strands you
      (every one slides home again). Islets: a cache west, a talking kin east.

Run:  python3 tools/maps/build_wakeful_fair.py
"""
from __future__ import annotations

from collections import deque

from roomkit import (CAP_N, CAP_S, DOORMAT, FLOOR, WARM_SET, WINDOW, faced_room, finish,
                     mapdef, partition_h, partition_v, place, wall_mount, windows)

FAIR, LOFT, DREAM = "wakeful_fair", "wakeful_fair_loft", "wakeful_fair_dream"
FAIR_SET = dict(WARM_SET, name="brewfair_set", image="assets/tilesets/brewfair_set.webp")
DREAM_SET = dict(WARM_SET, name="brewdream_set", image="assets/tilesets/brewdream_set.webp")
MUSIC = "assets/audio/music/wakeful-fair.mp3"
DREAM_MUSIC = "assets/audio/music/wakeful-fair-dream.mp3"
RISE_APPROACH = (14, 19)        # the tile below the marquee's flap on wayward_rise

PERKY, BUZZING, SEEING = "flag:brew_perky", "flag:brew_buzzing", "flag:brew_seeing"
DONE = "flag:q_south_brew_done"


def o(objects, oid, stem, tx, ty, w, h, *, solid=True, **extra):
    """A drawn `brewfair_*` piece."""
    ob = {"id": oid, "sprite": f"brewfair_{stem}", "at": {"tx": tx, "ty": ty}, "w": w, "h": h}
    if not solid:
        ob["solid"] = False
    ob.update(extra)
    objects.append(ob)
    return ob


def stall(objects, triggers, npcs, kind, tx, ty, keeper, sprite, *, trip=None, flags=None):
    """A 3x2 counter at (tx,ty) with its keeper behind it (north, the middle
    column) — talked to ACROSS the counter. `trip` = a kin sprite the keeper turns
    into once you're SEEING things (a same-tile flag-pair twin, same script)."""
    o(objects, f"stall_{kind}", f"stall_{kind}", tx, ty, 3, 2, **(flags or {}))
    at = {"tx": tx + 1, "ty": ty - 1}
    ref = f"script.brew_{kind}"
    npc = {"id": keeper, "sprite": sprite, "at": at, "facing": "down",
           "movement": "static", "dialogue_ref": ref}
    if flags and flags.get("requires_flag"):
        npc["requires_flag"] = flags["requires_flag"]
    if trip:
        npc["hidden_when_flag"] = SEEING
        npcs.append(npc)
        npcs.append({"id": f"{keeper}_trip", "sprite": trip, "at": at, "facing": "down",
                     "movement": "static", "dialogue_ref": ref, "requires_flag": SEEING})
    else:
        npcs.append(npc)


def sign(triggers, tid, x, y, ref, kind="sign", **extra):
    t = {"id": tid, "kind": kind, "at": {"tx": x, "ty": y}, "activation": "interact", "ref": ref}
    t.update(extra)
    triggers.append(t)


def cache(npcs, cid, x, y):
    npcs.append({"id": f"cache_{cid}", "sprite": "item_cache", "at": {"tx": x, "ty": y},
                 "facing": "down", "movement": "static",
                 "dialogue_ref": f"script.pickup_brew_{cid}",
                 "hidden_when_flag": f"flag:picked_brew_{cid}"})


def no_door(base, over, W, H, x):
    """A floor with no south door: wall the doormat back up."""
    base[(H - 1) * W + x] = FLOOR
    over[(H - 1) * W + x] = CAP_N


# =====================================================================================
#  THE MARQUEE
# =====================================================================================
def fair() -> dict:
    W, H, DOOR = 30, 21, 15
    base, over = faced_room(W, H, DOOR)
    objects, warps, triggers, npcs = [], [], [], []

    # ---- walls: the Siphon Lab wing (NE) and the Quiet Tent (SE) -------------------
    partition_v(over, W, 22, 2, 7, lip="w", doors=(5,))
    partition_h(base, over, W, 9, 22, 28)
    partition_v(over, W, 22, 13, 19, lip="w")
    partition_h(base, over, W, 14, 22, 28, doors=(25,))
    # the north face: lanterns between the banners
    windows(over, W, [8, 12, 16, 21, 23, 27])

    # ---- north wall stalls (keepers on row 2, counters rows 3-4) -------------------
    stall(objects, triggers, npcs, "pourover", 5, 3, "prudence", "npc_woman",
          trip="kin_8_overworld")
    stall(objects, triggers, npcs, "sandpot", 9, 3, "ilka", "npc_old_woman",
          trip="kin_69_overworld")
    stall(objects, triggers, npcs, "coldbrew", 18, 3, "tidwell", "fisher_man",
          trip="kin_27_overworld")
    for kind, x in (("pourover", 5), ("sandpot", 9), ("coldbrew", 18)):
        o(objects, f"banner_{kind}", f"banner_{kind}", x, 1, 3, 1, solid=False)
    o(objects, "bunting_nw", "bunting", 2, 1, 3, 1, solid=False)
    # the CUP RECORD chalkboard (a wall piece) between the stalls
    wall_mount(objects, "chalkboard", 13, oid="record_board")
    for x in (13, 14, 15, 16):
        sign(triggers, f"record_{x}", x, 2, "sign.brewfair_record")

    # ---- the TRADE ONLY stair (NW) ------------------------------------------------
    base[2 * W + 1] = DOORMAT
    warps.append({"id": "up_stairs", "at": {"tx": 1, "ty": 2}, "trigger": "step_on",
                  "to_map": LOFT, "to": {"tx": 1, "ty": 3}, "facing": "down",
                  "transition": "fade"})
    o(objects, "stair_sacks", "bean_sacks", 2, 2, 2, 1)
    o(objects, "trade_board", "aboard", 3, 3, 1, 1)
    sign(triggers, "trade_board", 3, 3, "sign.brewfair_trade_only")
    npcs.append({"id": "wilmot", "sprite": "npc_shopkeeper", "at": {"tx": 2, "ty": 4},
                 "facing": "up", "movement": "static",
                 "dialogue_ref": "script.brewfair_wilmot"})
    # the one tile before the stair turns you back until you're talking fast enough
    triggers.append({"id": "trade_only", "kind": "cutscene", "at": {"tx": 1, "ty": 3},
                     "activation": "step_on", "ref": "script.brewfair_trade_block",
                     "hidden_when_flag": "flag:brew_was_perky"})

    # ---- the GRAND URN (centre; you walk round it) ----------------------------------
    o(objects, "urn", "grand_urn", 13, 8, 4, 4, overhang=1, hidden_when_flag=SEEING)
    o(objects, "urn_awake", "grand_urn_awake", 13, 8, 4, 4, overhang=1, requires_flag=SEEING)
    for x in (14, 15):
        triggers.append({"id": f"urn_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 11},
                         "activation": "interact", "ref": "script.brewfair_urn"})
    # the puddle at its foot: the way down into the cup (only while SEEING)
    o(objects, "puddle", "urn_puddle", 14, 12, 1, 1, solid=False, requires_flag=SEEING)
    warps.append({"id": "into_the_cup", "at": {"tx": 14, "ty": 12}, "trigger": "step_on",
                  "to_map": DREAM, "to": {"tx": 11, "ty": 15}, "facing": "up",
                  "transition": "fade", "requires_flag": SEEING})

    # ---- the middle row (keepers row 7, counters rows 8-9) -------------------------
    stall(objects, triggers, npcs, "ember", 3, 8, "corbin", "miner_man",
          trip="kin_1_overworld")
    stall(objects, triggers, npcs, "press", 7, 8, "hefty", "lifter_andy",
          trip="kin_48_overworld")
    stall(objects, triggers, npcs, "mushroom", 18, 8, "margery", "hollow_gardener",
          trip="kin_56_overworld")

    # ---- the Siphon Lab wing (behind its queue) ------------------------------------
    stall(objects, triggers, npcs, "siphon", 24, 3, "alembic", "star_watcher",
          trip="kin_44_overworld")
    o(objects, "banner_siphon", "banner_siphon", 24, 1, 3, 1, solid=False)
    o(objects, "wing_cups", "cup_tower", 28, 2, 1, 2)
    o(objects, "wing_sacks", "bean_sacks", 26, 7, 2, 1)
    cache(npcs, "wing", 23, 7)
    # the queue: the doorway (22,5) and the next in line step aside once you're
    # buzzing; the rest of the line stays (they've been here since Tuesday)
    queue = [("q_front", 22, 5, "pass_walker", "left"), ("q_two", 21, 5, "npc_man", "right"),
             ("q_three", 21, 6, "fisher_woman", "up"), ("q_four", 21, 7, "road_courier", "up"),
             ("q_five", 21, 8, "village_child", "up")]
    for qid, x, y, spr, face in queue:
        n = {"id": qid, "sprite": spr, "at": {"tx": x, "ty": y}, "facing": face,
             "movement": "static", "dialogue_ref": "script.brewfair_queue"}
        if qid in ("q_front", "q_two"):
            n["hidden_when_flag"] = "flag:brew_was_buzzing"
        npcs.append(n)
    # the two who stepped aside, still grumbling, one tile off the line
    npcs.append({"id": "q_front_aside", "sprite": "pass_walker", "at": {"tx": 17, "ty": 6},
                 "facing": "right", "movement": "static", "dialogue_ref": "script.brewfair_queue",
                 "requires_flag": "flag:brew_was_buzzing"})
    o(objects, "q_post_a", "rope_post", 20, 7, 1, 1, solid=False)

    # ---- the south row (keepers row 13, counters rows 14-15) -----------------------
    objects.append({"id": "moka_stand", "sprite": "kitchens_moka_stall",
                    "at": {"tx": 3, "ty": 13}, "w": 2, "h": 2, "overhang": 1})
    npcs.append({"id": "percy", "sprite": "innkeeper", "at": {"tx": 5, "ty": 14},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brew_moka",
                 "hidden_when_flag": SEEING})
    npcs.append({"id": "percy_trip", "sprite": "kin_18_overworld", "at": {"tx": 5, "ty": 14},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brew_moka",
                 "requires_flag": SEEING})
    stall(objects, triggers, npcs, "latte", 7, 14, "fern", "npc_girl",
          trip="kin_86_overworld")
    stall(objects, triggers, npcs, "decaf", 18, 14, "dennis", "npc_old_man")
    # the Stall That Isn't There (only for the buzzing; non-solid — it isn't there)
    stall(objects, triggers, npcs, "nothing", 5, 17, "nobody", "kin_133_overworld",
          flags={"solid": False, "requires_flag": "flag:brew_was_buzzing"})

    # ---- poles, sacks, the hawker ---------------------------------------------------
    for pid, x in (("pole_w", 12), ("pole_e", 17)):
        o(objects, pid, "tent_pole", x, 13, 1, 2, overhang=1, walk_under=True)
    o(objects, "west_sacks", "bean_sacks", 1, 11, 2, 1)
    o(objects, "west_cups", "cup_tower", 1, 16, 1, 2)
    o(objects, "aboard_s", "aboard", 20, 18, 1, 1)
    sign(triggers, "aboard_s", 20, 18, "sign.brewfair_aboard")
    npcs.append({"id": "sal", "sprite": "fisher_woman", "at": {"tx": 28, "ty": 11},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brew_hawker_sal",
                 "sight_range": 5, "defeated_flag": "flag:brew_sal_poured",
                 "hidden_when_flag": "flag:brew_sal_poured"})
    npcs.append({"id": "sal_after", "sprite": "fisher_woman", "at": {"tx": 28, "ty": 11},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brew_hawker_sal_after",
                 "requires_flag": "flag:brew_sal_poured"})

    # ---- the crowd: fairgoers, each with one thing to say ---------------------------
    for gid_, x, y, spr, face in (("goer_a", 6, 6, "npc_boy", "down"), ("goer_b", 11, 13, "kite_child", "left"),
                                  ("goer_c", 16, 16, "orchard_farmer", "up"), ("goer_d", 27, 12, "lamplighter", "up"),
                                  ("goer_e", 10, 12, "fen_folk", "right"), ("goer_f", 2, 15, "miner_woman", "right")):
        npcs.append({"id": gid_, "sprite": spr, "at": {"tx": x, "ty": y}, "facing": face,
                     "movement": "static", "dialogue_ref": f"npc.brewfair_{gid_}"})

    # ---- the foyer: the ticket table, Marigold, the welcome ------------------------
    place(objects, "desk", 11, 17, oid="ticket_table")
    npcs.append({"id": "marigold", "sprite": "market_trader", "at": {"tx": 12, "ty": 16},
                 "facing": "down", "movement": "static", "dialogue_ref": "script.brewfair_marigold"})
    # the three ways off the landing tile (15,19): you can't take a step in without her
    for tid, x, y in (("welcome_w", 14, 19), ("welcome_e", 16, 19), ("welcome_n", 15, 18)):
        triggers.append({"id": tid, "kind": "cutscene", "at": {"tx": x, "ty": y},
                         "activation": "step_on", "ref": "script.brewfair_welcome",
                         "hidden_when_flag": "flag:brew_has_card"})
    # and on the way out, once you're buzzing, your feet turn round. Once.
    triggers.append({"id": "one_more", "kind": "cutscene", "at": {"tx": 15, "ty": 19},
                     "activation": "step_on", "ref": "script.brewfair_one_more",
                     "requires_flag": BUZZING, "hidden_when_flag": "flag:brew_tried_leave"})
    warps.append({"id": "to_rise", "at": {"tx": DOOR, "ty": H - 1}, "trigger": "step_on",
                  "to_map": "wayward_rise", "to": {"tx": RISE_APPROACH[0], "ty": RISE_APPROACH[1]},
                  "facing": "down", "transition": "door"})

    # ---- the QUIET TENT (SE) --------------------------------------------------------
    o(objects, "cot_a", "cot", 23, 16, 1, 2)
    o(objects, "cot_b", "cot", 23, 18, 1, 2)
    o(objects, "cot_c", "cot", 28, 18, 1, 2)
    o(objects, "water", "water_table", 27, 15, 2, 1)
    sign(triggers, "water", 27, 15, "sign.brewfair_water")
    sign(triggers, "water_b", 28, 15, "sign.brewfair_water")
    o(objects, "plaque", "plaque", 26, 14, 1, 1, solid=False)
    sign(triggers, "plaque", 26, 14, "sign.brewfair_plaque")
    for cid, x, y in (("cot_a", 23, 16), ("cot_b", 23, 18), ("cot_c", 28, 18)):
        sign(triggers, cid, x, y, "sign.brewfair_cot")
    npcs.append({"id": "medic", "sprite": "npc_parent", "at": {"tx": 26, "ty": 17},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brewfair_medic"})

    m = mapdef(FAIR, "The Wakeful Fair", W, H, FAIR_SET, base, over, objects, warps,
               triggers, npcs, MUSIC)
    m["ambience"] = fair_ambience()
    return m


def fair_ambience() -> dict:
    """The marquee's mood follows your cup count (MapAmbience.when — re-read after
    every scene, WorldScene.refreshStoryState). After the trip it settles back."""
    normal = {"particles": [{"kind": "steam", "density": 0.6}, {"kind": "dust", "density": 0.3}],
              "starfall": False}
    return {
        **normal,
        "when": [
            {"flag": DONE, "ambience": normal},
            {"flag": SEEING, "ambience": {
                "particles": [{"kind": "confetti", "density": 1.0}, {"kind": "spores", "density": 0.8},
                              {"kind": "starglint", "density": 0.8}],
                "tint": {"color": "#c050ff", "alpha": 0.16},
                "mist": {"color": "#ff8ad8", "alpha": 0.10, "speed": 14},
                "starfall": False}},
            {"flag": BUZZING, "ambience": {
                "particles": [{"kind": "steam", "density": 1.0}, {"kind": "glowmotes", "density": 0.7},
                              {"kind": "confetti", "density": 0.35}],
                "tint": {"color": "#ffb040", "alpha": 0.08},
                "mist": {"color": "#f0dcb8", "alpha": 0.06, "speed": 8},
                "starfall": False}},
            {"flag": PERKY, "ambience": {
                "particles": [{"kind": "steam", "density": 0.9}, {"kind": "glowmotes", "density": 0.35}],
                "starfall": False}},
        ],
    }


# =====================================================================================
#  THE ROASTERS' LOFT
# =====================================================================================
def loft() -> dict:
    W, H = 20, 13
    base, over = faced_room(W, H, W // 2)
    no_door(base, over, W, H, W // 2)
    objects, warps, triggers, npcs = [], [], [], []
    windows(over, W, [3, 7, 11, 15])
    base[2 * W + 1] = DOORMAT
    warps.append({"id": "down_stairs", "at": {"tx": 1, "ty": 2}, "trigger": "step_on",
                  "to_map": FAIR, "to": {"tx": 1, "ty": 3}, "facing": "down",
                  "transition": "fade"})
    stall(objects, triggers, npcs, "frost", 4, 3, "rime", "frost_herder", trip="kin_77_overworld")
    stall(objects, triggers, npcs, "dawn", 8, 3, "solveig", "sun_keeper", trip="kin_117_overworld")
    stall(objects, triggers, npcs, "midnight", 12, 3, "vesper", "hollowing_acolyte",
          trip="kin_105_overworld")
    for kind, x in (("frost", 4), ("dawn", 8), ("midnight", 12)):
        o(objects, f"banner_{kind}", f"banner_{kind}", x, 1, 3, 1, solid=False)
    o(objects, "roaster", "roaster", 16, 2, 3, 3, overhang=1)
    sign(triggers, "roaster", 17, 4, "sign.brewfair_roaster")
    o(objects, "loft_sacks", "bean_sacks", 16, 6, 2, 1)
    # the cupping table: Slurrington at its east end (a talked-to bout + a cup)
    o(objects, "cupping", "cupping_table", 3, 7, 3, 2)
    npcs.append({"id": "slurrington", "sprite": "old_salt", "at": {"tx": 6, "ty": 8},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brew_cupping"})
    npcs.append({"id": "slurrington_trip", "sprite": "kin_59_overworld", "at": {"tx": 6, "ty": 8},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brew_cupping",
                 "requires_flag": SEEING})
    npcs[-2]["hidden_when_flag"] = SEEING
    # the Championship stage + the Golden Cup; the champion in front of it
    o(objects, "stage", "stage", 10, 7, 4, 2)
    o(objects, "trophy", "trophy", 14, 7, 1, 2, overhang=1)
    sign(triggers, "trophy", 14, 8, "sign.brewfair_trophy")
    npcs.append({"id": "ottoline", "sprite": "npc_woman", "at": {"tx": 12, "ty": 9},
                 "facing": "down", "movement": "static", "dialogue_ref": "script.brew_champion"})
    # Free-Sample Fred on the south aisle
    npcs.append({"id": "fred", "sprite": "road_courier", "at": {"tx": 18, "ty": 10},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brew_hawker_fred",
                 "sight_range": 8, "defeated_flag": "flag:brew_fred_poured",
                 "hidden_when_flag": "flag:brew_fred_poured"})
    npcs.append({"id": "fred_after", "sprite": "road_courier", "at": {"tx": 18, "ty": 10},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brew_hawker_fred_after",
                 "requires_flag": "flag:brew_fred_poured"})
    for gid_, x, y, spr, face in (("goer_g", 16, 8, "miner_man", "left"), ("goer_h", 2, 11, "npc_old_woman", "up")):
        npcs.append({"id": gid_, "sprite": spr, "at": {"tx": x, "ty": y}, "facing": face,
                     "movement": "static", "dialogue_ref": f"npc.brewfair_{gid_}"})
    o(objects, "loft_pole", "tent_pole", 8, 9, 1, 2, overhang=1, walk_under=True)
    o(objects, "loft_cups", "cup_tower", 1, 9, 1, 2)
    cache(npcs, "loft", 18, 11)
    m = mapdef(LOFT, "The Roasters' Loft", W, H, FAIR_SET, base, over, objects, warps,
               triggers, npcs, MUSIC)
    m["ambience"] = {"particles": [{"kind": "steam", "density": 0.8}, {"kind": "dust", "density": 0.4}],
                     "light_sources_extra": [{"at": {"tx": 17, "ty": 4}, "radius": 2,
                                              "color": "#ff8a3d"}],
                     "starfall": False,
                     "when": fair_ambience()["when"]}
    return m


# =====================================================================================
#  THE BOTTOM OF THE CUP
# =====================================================================================
DW, DH = 24, 18
DREAM_START = (11, 15)          # where you land (beside the door back)
DREAM_GOAL = (13, 5)            # the inlet under the Bottomless Cup
# the slick's obstacles: (x, y, w, h, kind) — found by a solver search, then pinned
OBSTACLES = [(18, 9, 3, 1, "spoon"), (13, 11, 1, 1, "sugar_cube"), (9, 12, 1, 1, "sugar_cube"),
             (5, 6, 3, 1, "spoon"), (10, 10, 3, 1, "spoon"), (7, 10, 1, 1, "bean"),
             (19, 7, 1, 1, "bean"), (12, 7, 1, 1, "sugar_cube")]
CUP = (10, 2)                   # the Bottomless Cup, 3x3


def dream_cells():
    """'f' foam, 'i' the caramel slick, everything else coffee."""
    cells = {}
    for y in range(14, 17):
        for x in range(9, 15):
            cells[(x, y)] = "f"
    cells[(11, 13)] = cells[(12, 13)] = "f"            # the neck up onto the slick
    for y in range(6, 13):
        for x in range(3, 21):
            cells[(x, y)] = "i"
    for y in range(2, 5):
        for x in range(13, 18):
            cells[(x, y)] = "f"                          # the cup's lip (the cup stands in the coffee)
    cells[DREAM_GOAL] = "f"
    for y in (8, 9):
        for x in (1, 2):
            cells[(x, y)] = "f"                          # the west islet
    for y in (7, 8):
        for x in (21, 22):
            cells[(x, y)] = "f"                          # the east islet
    return cells


def prove_slick(cells, solid):
    """The engine's ice rule (Traversal.ts): step; while on the slick keep going
    until the next tile is blocked. Proves the goal is reachable, that it takes
    a real solution, and that every resting place slides home again."""
    D = ((0, -1), (0, 1), (-1, 0), (1, 0))

    def blocked(x, y):
        return (x, y) not in cells or (x, y) in solid

    def move(p, d):
        x, y = p[0] + d[0], p[1] + d[1]
        if blocked(x, y):
            return None
        while cells[(x, y)] == "i" and not blocked(x + d[0], y + d[1]):
            x, y = x + d[0], y + d[1]
        return (x, y)

    def reach(start):
        dist = {start: 0}
        q = deque([start])
        while q:
            p = q.popleft()
            for d in D:
                n = move(p, d)
                if n and n not in dist:
                    dist[n] = dist[p] + 1
                    q.append(n)
        return dist

    dist = reach(DREAM_START)
    assert DREAM_GOAL in dist, "the Bottomless Cup can't be reached"
    assert dist[DREAM_GOAL] >= 12, f"the slick is too easy ({dist[DREAM_GOAL]} presses)"
    for p in dist:
        assert DREAM_START in reach(p), f"a resting place strands you: {p}"
    for islet in (((1, 8), (2, 8), (1, 9), (2, 9)), ((21, 7), (22, 7), (21, 8), (22, 8))):
        assert any(t in dist for t in islet), f"an islet is unreachable: {islet}"
    return dist[DREAM_GOAL]


def dream() -> dict:
    W, H = DW, DH
    base, over = faced_room(W, H, 12)
    no_door(base, over, W, H, 12)
    objects, warps, triggers, npcs = [], [], [], []
    cells = dream_cells()
    for y in range(2, H - 1):
        for x in range(1, W - 1):
            kind = cells.get((x, y))
            if kind is None:
                over[y * W + x] = CAP_S           # coffee (autotiled to a foam shore)
            elif kind == "i":
                base[y * W + x] = DOORMAT          # the dream set's caramel slick
            else:
                base[y * W + x] = FLOOR
    windows(over, W, [5, 18])                      # the eyes painted on the cup
    slick = sorted(p for p, k in cells.items() if k == "i")
    solid = set()
    for i, (x, y, w, h, kind) in enumerate(OBSTACLES):
        o(objects, f"{kind}_{i}", kind, x, y, w, h)
        solid |= {(xx, yy) for xx in range(x, x + w) for yy in range(y, y + h)}
    # flotsam on the coffee (decor only — it all sits on the liquid, which collides anyway)
    for i, (kind, x, y, w, h) in enumerate((("teacup", 3, 14, 2, 2), ("spoon", 16, 15, 3, 1),
                                            ("bean", 21, 15, 1, 1), ("sugar_cube", 5, 3, 1, 1),
                                            ("bean", 19, 3, 1, 1), ("sugar_cube", 7, 15, 1, 1))):
        o(objects, f"flotsam_{i}", kind, x, y, w, h)
    o(objects, "bottomless", "bottomless", CUP[0], CUP[1], 3, 3, overhang=1)
    solid |= {(CUP[0] + dx, CUP[1] + dy) for dx in range(3) for dy in range(3)}
    for y in (3, 4):
        sign(triggers, f"cup_{y}", CUP[0] + 2, y, "script.brewfair_bottomless", kind="cutscene")
    # the islets' furniture: a teacup that talks (north island), a spoon you can read
    o(objects, "teacup", "teacup", 16, 2, 2, 2)
    solid |= {(16, 2), (17, 2), (16, 3), (17, 3)}
    sign(triggers, "teacup", 16, 3, "script.brewfair_teacup", kind="cutscene")
    # NPC bodies stop a slide too: the islets' cache + kin, the Buzz
    solid |= {(1, 8), (22, 8), (17, 4), (13, 3)}
    presses = prove_slick(cells, solid)
    m_flows = [{"id": "caramel_slick", "kind": "ice",
                "tiles": [{"tx": x, "ty": y} for (x, y) in slick]}]
    # the door that stands on its own (the way back) and where you land beside it
    o(objects, "dream_door", "dream_door", 12, 14, 1, 2, overhang=1, walk_under=True, solid=False)
    warps.append({"id": "back_to_fair", "at": {"tx": 12, "ty": 15}, "trigger": "step_on",
                  "to_map": FAIR, "to": {"tx": 14, "ty": 13}, "facing": "down",
                  "transition": "fade"})
    sign(triggers, "door_note", 13, 15, "sign.brewfair_dream_door")
    # THE BUZZ: your own heartbeat, given wings — it waits at the cup's lip and
    # spots you the moment you reach the inlet (sight 2); the scene is the boss
    npcs.append({"id": "buzz", "sprite": "kin_98_overworld", "at": {"tx": 13, "ty": 3},
                 "facing": "down", "movement": "static", "dialogue_ref": "script.brewfair_buzz",
                 "sight_range": 2, "defeated_flag": "flag:brew_buzz_beaten",
                 "hidden_when_flag": "flag:brew_buzz_beaten"})
    # the islets: a cache west, a very small philosopher east
    cache(npcs, "dream", 1, 8)
    npcs.append({"id": "dream_kin", "sprite": "kin_111_overworld", "at": {"tx": 22, "ty": 8},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brewfair_dream_kin"})
    npcs.append({"id": "dream_kin_b", "sprite": "kin_133_overworld", "at": {"tx": 17, "ty": 4},
                 "facing": "left", "movement": "static", "dialogue_ref": "script.brewfair_dream_moth"})
    m = mapdef(DREAM, "The Bottom of the Cup", W, H, DREAM_SET, base, over, objects, warps,
               triggers, npcs, DREAM_MUSIC)
    m["flows"] = m_flows
    m["ambience"] = {
        "particles": [{"kind": "confetti", "density": 0.6}, {"kind": "steam", "density": 1.0},
                      {"kind": "starglint", "density": 0.7}],
        "tint": {"color": "#b050ff", "alpha": 0.10},
        "mist": {"color": "#f0dcb8", "alpha": 0.08, "speed": 18},
        "starfall": False,
    }
    print(f"  {DREAM}: the slick solves in {presses} presses")
    return m


if __name__ == "__main__":
    ok = True
    for build in (fair, loft, dream):
        ok = finish(build()) and ok
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
