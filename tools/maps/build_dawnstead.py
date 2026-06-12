#!/usr/bin/env python3
"""
Build Dawnstead — the post-game epilogue town (walkthrough/06-postgame
§Dawnstead; PROGRESS.md R2). Tinderwick reborn in the first true daylight in
years: the same cottage rooflines and dock shape, open-skied, on the frozen
shared set's DAYLIT register (dawngrass / dawnpath / dawntuft — TILEFORGE
2026-06). Gate: post-game only (`flag:dawn`; the graph node carries
`unlocked_by_flag`). Rec. level 55-65. No Lumenary, no Gleam — a town to
WALK, not a route to clear.

THE C2 HANDSHAKE (build_umbral_spire.py docstring, honoured verbatim): the
summit's to_dawn/to_dawn_e step_on warps at (16,20)/(17,20) land HERE at
(15,28)/(16,28) facing up — the head of the dawn-road pier. Our return pair
to_spire/to_spire_e sits ON those landing tiles and lands back at the
summit's (16,20)/(17,20) facing down (audit_warps proves the round trip;
the engine never auto-fires a step_on warp on arrival).

Three signature touches (level-design §8):
  1. THE DAWN PIER — the player arrives up a dock-board causeway out of the
     sea-light, the town's "same dock" rhyme with Tinderwick's shore; the
     arrival band on the pier holds the sky beat before anything else.
  2. THE SUNLIT VERGE — the day-form encounter bed (dawntuft, hard-edged
     fill) where the sun-bright Wickmoth headlines the post-dawn collecting
     hook (the day-form table, 55-65).
  3. CÒR'S LAMP-NOOK — off to one side on the west strand, behind the old
     tree: a single tended lamp (the watch-lamp swap pair: low flame ->
     a shade warmer once the First-Dawn Wick comes home — quest P2).

STORY WIRING (all data; refs paid in content/*.ts):
  * arrival band (pier, both columns)        -> script.dawnstead_arrival
  * first-dawn festival band (plaza spine)   -> cutscene.dawnstead_first_dawn
      (OPTIONAL ambient colour — deliberately walk-aroundable across the open
      green; the festival is `[MISSABLE]` by spec, not a progression cut)
  * Fenn on the front (flag-staggered)       -> script.fenn_dawnstead /
      script.fenn_survey_wait / script.fenn_survey_done / npc.fenn_dawnstead_after
      (P2 giver beat + P3 "Day-form Survey" — boolean-chain fallback, spine §8:
      three survey-mark finds in/by the verge, one named day-form at a time)
  * Wren by the water (A6)                   -> script.wren_dawnstead then the
      re-runnable optional rematch script.wren_rematch (trainer.wren_rematch,
      lv55-65, rival 24×ace — no progression gate, no defeated flag)
  * Còr tending a lamp                       -> cutscene.cor_resolution on the
      nook approach band (hidden_when flag:cor_greeted — the multi-tile band
      pattern; sets only its own hide flag, no progression flag) + the staged
      Còr placements npc.cor_lamp / script.cor_wick_given / npc.cor_after
  * P1 First-Dawn Letters: the local recipients' bands (Wren, Fenn) fire on
      flag:q_post_letters (giver = the Waykeeper's post-bag at the crossroads).

Run:  ./venv/bin/python tools/maps/build_dawnstead.py
Prereq: the shared set (python3 tools/maps/build_shared_overworld.py).
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 28, 30
rng = random.Random(151)

# ---- building footprints (Tinderwick's silhouette, re-set in daylight) -------
SHOP = {"at": (3, 4), "w": 5, "h": 4, "door_col": 2}       # the store roofline
COTTAGE_E = {"at": (17, 3), "w": 5, "h": 5, "door_col": 2}  # east cottage
COTTAGE_W = {"at": (4, 12), "w": 5, "h": 5, "door_col": 2}  # the home-shaped one

def door_tile(b):
    return (b["at"][0] + b["door_col"], b["at"][1] + b["h"] - 1)

shop_door = door_tile(SHOP)        # (5, 7)
cot_e_door = door_tile(COTTAGE_E)  # (19, 7)
cot_w_door = door_tile(COTTAGE_W)  # (6, 16)

# ---- terrain presence grids ---------------------------------------------------
# Deep organic enclosure (§11): tree border N/W/E, the NE cliff knoll as the
# elevation accent, the sea as the southern border (off-map = continuation).
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(5, 2, 2), (10, 1, 1), (2, 9, 2), (26, 10, 2),
                         (2, 14, 1), (26, 19, 1)])
mk.rect(tree, W, H, 0, 21, W - 1, H - 1, 0)   # border stops at the strand

# NE cliff knoll — the elevation accent (rock behind the east cottage).
cliff = mk.make_grid(W, H)
mk.rect(cliff, W, H, 23, 0, W - 1, 2)
mk.blob(cliff, W, H, 25, 3, 2.2, 1.2)
mk.rect(tree, W, H, 23, 0, W - 1, 2, 0)       # cliff replaces the tree border here

# Sunlit verge — the day-form bed (dawntuft = the daylit encounter tile,
# hard-edged fill-only; clipped corners so the patch reads organic).
tuft = mk.make_grid(W, H)
mk.rect(tuft, W, H, 20, 13, 25, 18)
for (x, y) in ((20, 13), (25, 13), (20, 18), (25, 18)):
    tuft[y * W + x] = 0

# The lit path spine + plaza street (dawnpath — the daylit lane register).
path = mk.make_grid(W, H)
mk.vline(path, W, H, 13, 2, 20)
mk.vline(path, W, H, 14, 2, 20)
mk.rect(path, W, H, 5, 8, 21, 9)                       # the plaza street, two rows deep
path[8 * W + shop_door[0]] = 1                         # door stubs onto the street
path[8 * W + cot_e_door[0]] = 1
mk.vline(path, W, H, cot_w_door[0], cot_w_door[1] + 1, 18)  # home lane down…
mk.hline(path, W, H, 18, cot_w_door[0], 13)                 # …and across to the spine

# Sand strand (rows 21-23) + dune bites; the sea (rows 24-29).
sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 0, 21, W - 1, 23)
mk.blob(sand, W, H, 7, 20, 2.4, 1.2)
mk.blob(sand, W, H, 22, 20, 2.0, 1.2)
water = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 24, W - 1, H - 1)
mk.blob(water, W, H, 5, 24, 2.6, 1.4)                  # tideline bites the beach
mk.blob(water, W, H, 20, 24, 3.0, 1.4)
for x in (1, 2, 3):                                    # the tide curls in under Còr's nook
    water[23 * W + x] = 1
# THE DAWN PIER (the C2 handshake): carve the sea out under the causeway and
# lay sand + dock boards — an ALWAYS-walkable pier (the Pearlmoor jetty rule:
# water gates ride the tiles, so the water grid must be cut, not covered).
PIER_X = (15, 16)
for y in range(23, 29):
    for x in PIER_X:
        water[y * W + x] = 0
        sand[y * W + x] = 1

# ---- base = daylit grass scatter ---------------------------------------------
dg = [gid("dawngrass0"), gid("dawngrass1"), gid("dawngrass2"), gid("dawngrass3")]
base = [rng.choice(dg) if rng.random() < 0.5 else dg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_tuft", "role": "terrain", "terrain": "dawntuft",
     "set": "vesper_overworld_set", "depth": 0, "data": tuft},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_path", "role": "terrain", "terrain": "dawnpath",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_sea", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

# ---- objects: the Tinderwick rooflines, trees, lamps, Còr's lamp pair --------
objects = [
    {"id": "store", "sprite": "tinderwick_shop",
     "at": {"tx": SHOP["at"][0], "ty": SHOP["at"][1]}, "w": 5, "h": 4, "overhang": 2},
    {"id": "cottage_e", "sprite": "tinderwick_cottage",
     "at": {"tx": COTTAGE_E["at"][0], "ty": COTTAGE_E["at"][1]}, "w": 5, "h": 5, "overhang": 3},
    {"id": "cottage_w", "sprite": "tinderwick_cottage",
     "at": {"tx": COTTAGE_W["at"][0], "ty": COTTAGE_W["at"][1]}, "w": 5, "h": 5, "overhang": 3},
    # Object trees break the border into overlapping canopies (§11). tree_d is
    # the NOOK WALL: its trunk row (19) closes Còr's strand nook from the north
    # so the resolution band on the east approach can't be slipped past.
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 1, "ty": 5}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 9, "ty": 10}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 24, "ty": 9}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_d", "sprite": "tinderwick_tree", "at": {"tx": 1, "ty": 16}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_e", "sprite": "tinderwick_tree", "at": {"tx": 16, "ty": 17}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_f", "sprite": "tinderwick_tree", "at": {"tx": 21, "ty": 1}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    # Lamp-posts — keepsakes now, not necessities: unlit posts along the lanes.
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 5}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 15, "ty": 12}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 18}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_d", "sprite": "tinderwick_lamp_post", "at": {"tx": 20, "ty": 8}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # CÒR'S LAMP — the P2 deco swap pair (same footprint + solidity, the
    # watch-lamp convention): the low-banked flame until the First-Dawn Wick
    # is set to it, a shade warmer thereafter (flag:q_post_wick_given).
    {"id": "cor_lamp_low", "sprite": "nightreach_watch_lamp_dark",
     "at": {"tx": 1, "ty": 20}, "w": 2, "h": 3, "overhang": 2,
     "hidden_when_flag": "flag:q_post_wick_given"},
    {"id": "cor_lamp_warm", "sprite": "nightreach_watch_lamp_lit",
     "at": {"tx": 1, "ty": 20}, "w": 2, "h": 3, "overhang": 2,
     "requires_flag": "flag:q_post_wick_given"},
]
building_cells = set()
for o in objects:
    for yy in range(o["at"]["ty"], o["at"]["ty"] + o["h"]):
        for xx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
            building_cells.add((xx, yy))

covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, cliff, water, sand, tuft, path))}
avoid = covered | building_cells

# ---- deco: the garden echo, signs, dock boards, shore props -------------------
deco = mk.make_grid(W, H)
# The fenced flower garden, kept exactly where Tinderwick keeps hers — the
# "is this home?" beat told in furniture (open mouth east, toward the verge).
mk.fence_run(deco, W, H, 16, 10, 19)
mk.fence_run(deco, W, H, 16, 13, 19)
deco[11 * W + 16] = gid("fence_post")
deco[12 * W + 16] = gid("fence_post")
for (x, y) in [(17, 11), (18, 11), (17, 12), (18, 12)]:
    deco[y * W + x] = gid("flowerbed_a") if (x + y) % 2 else gid("flowerbed_b")
# The dock boards of the dawn pier (over the carved-out sand causeway).
for y in range(23, 29):
    for x in PIER_X:
        deco[y * W + x] = gid("dock")
# Signs beside the lanes (never mid-field).
sign_tiles = {
    "sign_town": (12, 10),    # beside the spine, under the plaza
    "sign_verge": (19, 14),   # at the sunlit verge's mouth
}
for (x, y) in sign_tiles.values():
    deco[y * W + x] = gid("sign")
# Survey marks (P3): dawn-blooms where the day-forms fed — visible, off the
# encounter bed, each carrying its interact find (the boolean chain).
survey_tiles = {"survey_1": (20, 12), "survey_2": (23, 19), "survey_3": (19, 17)}
for (x, y) in survey_tiles.values():
    deco[y * W + x] = gid("flowers")
for (x, y) in [(8, 22), (20, 22), (25, 21)]:           # shore boulders
    deco[y * W + x] = gid("boulder")
# Seal the strand's open edge runs with shore rocks (camera-margin rule §11).
for (x, y) in [(0, 21), (0, 22), (0, 23), (27, 21), (27, 22), (27, 23)]:
    deco[y * W + x] = gid("boulder")
for (x, y) in [(5, 26), (10, 27), (22, 26)]:           # morning buoys at rest
    deco[y * W + x] = gid("buoy")
# Daylit ground scatter (scatter_decor only fires on the dusk grass gids, so
# Dawnstead scatters its own morning meadow: daisies, pebbles, open blooms).
props = [gid("g_daisy"), gid("g_daisy"), gid("g_pebble"), gid("flowerbed_a"), gid("flowerbed_b")]
for y in range(H):
    for x in range(W):
        i = y * W + x
        if base[i] in dg and deco[i] == 0 and (x, y) not in avoid and rng.random() < 0.14:
            deco[i] = rng.choice(props)

# ---- assemble -----------------------------------------------------------------
m = {
    "id": "dawnstead", "display_name": "Dawnstead", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # The dawn road back up the mountain — sitting ON the summit's landing
        # tiles (the C2 contract): (15,28)/(16,28) <-> summit (16,20)/(17,20).
        {"id": "to_spire", "at": {"tx": 15, "ty": 28}, "trigger": "step_on",
         "to_map": "umbral_spire_summit", "to": {"tx": 16, "ty": 20}, "facing": "down",
         "transition": "fade"},
        {"id": "to_spire_e", "at": {"tx": 16, "ty": 28}, "trigger": "step_on",
         "to_map": "umbral_spire_summit", "to": {"tx": 17, "ty": 20}, "facing": "down",
         "transition": "fade"},
    ],
    "triggers": [
        # THE ARRIVAL — the sky beat, banded across both pier columns (the only
        # way in), one fire (the band pattern: sets_flags + hidden_when_flag).
        {"id": "arrival_w", "kind": "cutscene", "at": {"tx": 15, "ty": 27},
         "activation": "step_on", "ref": "script.dawnstead_arrival",
         "sets_flags": ["flag:dawnstead_arrived"], "hidden_when_flag": "flag:dawnstead_arrived"},
        {"id": "arrival_e", "kind": "cutscene", "at": {"tx": 16, "ty": 27},
         "activation": "step_on", "ref": "script.dawnstead_arrival",
         "sets_flags": ["flag:dawnstead_arrived"], "hidden_when_flag": "flag:dawnstead_arrived"},
        # THE FIRST-DAWN FESTIVAL (Arc E capstone) — ambient colour on the spine
        # into the plaza. Deliberately walk-aroundable (the open green): the
        # festival is [MISSABLE] by spec; only the arrival band is a true cut.
        {"id": "festival_w", "kind": "cutscene", "at": {"tx": 13, "ty": 10},
         "activation": "step_on", "ref": "cutscene.dawnstead_first_dawn",
         "requires_flag": "flag:dawn",
         "sets_flags": ["flag:dawnstead_festival"], "hidden_when_flag": "flag:dawnstead_festival"},
        {"id": "festival_e", "kind": "cutscene", "at": {"tx": 14, "ty": 10},
         "activation": "step_on", "ref": "cutscene.dawnstead_first_dawn",
         "requires_flag": "flag:dawn",
         "sets_flags": ["flag:dawnstead_festival"], "hidden_when_flag": "flag:dawnstead_festival"},
        # CÒR'S RESOLUTION — banded over every walkable approach into the
        # lamp-nook (tree_d's trunk seals the north; the tide seals the south),
        # so the gentlest beat in the game can't be slipped past. Sets only its
        # own hide flag — the resolution stays narrative (no progression flag).
        *[{"id": f"cor_meet_{i}", "kind": "cutscene", "at": {"tx": x, "ty": y},
           "activation": "step_on", "ref": "cutscene.cor_resolution",
           "requires_flag": "flag:dawn",
           "sets_flags": ["flag:cor_greeted"], "hidden_when_flag": "flag:cor_greeted"}
          for i, (x, y) in enumerate([(4, 20), (4, 21), (4, 22), (3, 20), (3, 22)])],
        # P1 — the letter bands by the two local recipients (giver: the
        # Waykeeper's post-bag at Vesper Crossroads). Inert until the bundle is
        # carried; hidden once each letter lands.
        *[{"id": f"letter_wren_{i}", "kind": "cutscene", "at": {"tx": x, "ty": y},
           "activation": "step_on", "ref": "script.post_letter_wren",
           "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_wren"}
          for i, (x, y) in enumerate([(15, 22), (16, 21), (15, 23), (16, 23)])],
        *[{"id": f"letter_fenn_{i}", "kind": "cutscene", "at": {"tx": x, "ty": y},
           "activation": "step_on", "ref": "script.post_letter_fenn",
           "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_fenn"}
          for i, (x, y) in enumerate([(8, 9), (10, 9), (9, 10)])],
        # P3 — the survey-mark finds (the boolean chain: 1 -> 2 -> 3; Fenn names
        # the next mark each time). blocked_ref gives the pre-quest tease.
        {"id": "survey_1", "kind": "script", "at": {"tx": survey_tiles["survey_1"][0], "ty": survey_tiles["survey_1"][1]},
         "activation": "interact", "ref": "script.survey_find_1",
         "requires_flag": "flag:q_post_survey", "hidden_when_flag": "flag:q_post_survey_1",
         "blocked_ref": "sign.dawnstead_blooms"},
        {"id": "survey_2", "kind": "script", "at": {"tx": survey_tiles["survey_2"][0], "ty": survey_tiles["survey_2"][1]},
         "activation": "interact", "ref": "script.survey_find_2",
         "requires_flag": "flag:q_post_survey_1", "hidden_when_flag": "flag:q_post_survey_2",
         "blocked_ref": "sign.dawnstead_blooms"},
        {"id": "survey_3", "kind": "script", "at": {"tx": survey_tiles["survey_3"][0], "ty": survey_tiles["survey_3"][1]},
         "activation": "interact", "ref": "script.survey_find_3",
         "requires_flag": "flag:q_post_survey_2", "hidden_when_flag": "flag:q_post_survey_3",
         "blocked_ref": "sign.dawnstead_blooms"},
        # Latched doors — everyone's out in the sun (no silent doors; the warm
        # line answers a walk-up Confirm; no warp = no graph geometry).
        {"id": "door_store", "kind": "dialogue", "at": {"tx": shop_door[0], "ty": shop_door[1]},
         "activation": "interact", "ref": "door.dawnstead_store"},
        {"id": "door_cottage_e", "kind": "dialogue", "at": {"tx": cot_e_door[0], "ty": cot_e_door[1]},
         "activation": "interact", "ref": "door.dawnstead_cottage"},
        {"id": "door_cottage_w", "kind": "dialogue", "at": {"tx": cot_w_door[0], "ty": cot_w_door[1]},
         "activation": "interact", "ref": "door.dawnstead_home"},
        # Signs.
        {"id": "sign_town", "kind": "sign", "at": {"tx": sign_tiles["sign_town"][0], "ty": sign_tiles["sign_town"][1]},
         "activation": "interact", "ref": "sign.dawnstead_town"},
        {"id": "sign_verge", "kind": "sign", "at": {"tx": sign_tiles["sign_verge"][0], "ty": sign_tiles["sign_verge"][1]},
         "activation": "interact", "ref": "sign.dawnstead_verge"},
    ],
    "encounters": [
        # THE SUNLIT VERGE — the day-form table (post-game band 55-65; element-
        # matched to Tinderwick's Ember/Light roster, the sun-bright Wickmoth
        # headlining). The map itself is dawn-gated, so no flag pair is needed.
        {"id": "sunlit_verge", "terrain": "tall_grass",
         "rect": {"tx": 20, "ty": 13, "w": 6, "h": 6}, "encounter_rate": 0.07,
         "table": [
             {"kin_id": 16, "weight": 30, "min_level": 55, "max_level": 60},  # Wickmoth — the headline day-form
             {"kin_id": 10, "weight": 20, "min_level": 55, "max_level": 58},  # Tallowpup
             {"kin_id": 18, "weight": 15, "min_level": 56, "max_level": 60},  # Hearthkit
             {"kin_id": 9, "weight": 15, "min_level": 56, "max_level": 60},   # Glimscout
             {"kin_id": 12, "weight": 12, "min_level": 58, "max_level": 62},  # Chandrek
             {"kin_id": 7, "weight": 8, "min_level": 60, "max_level": 65},    # Wicklord (rare)
         ]},
    ],
    "npcs": [
        # FENN ON THE FRONT — the mentor at peace; P2/P3 giver. Four
        # flag-disjoint placements (the waystone pattern).
        {"id": "fenn_meet", "at": {"tx": 9, "ty": 9}, "facing": "down",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "script.fenn_dawnstead", "hidden_when_flag": "flag:q_post_survey"},
        {"id": "fenn_survey", "at": {"tx": 9, "ty": 9}, "facing": "down",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "script.fenn_survey_wait",
         "requires_flag": "flag:q_post_survey", "hidden_when_flag": "flag:q_post_survey_3"},
        {"id": "fenn_done", "at": {"tx": 9, "ty": 9}, "facing": "down",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "script.fenn_survey_done",
         "requires_flag": "flag:q_post_survey_3", "hidden_when_flag": "flag:q_post_survey_done"},
        {"id": "fenn_after", "at": {"tx": 9, "ty": 9}, "facing": "down",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "npc.fenn_dawnstead_after", "requires_flag": "flag:q_post_survey_done"},
        # WREN BY THE WATER (A6) — talk first; the rematch is offered, never
        # forced: it lives on the second placement, re-runnable forever.
        {"id": "wren_a6", "at": {"tx": 16, "ty": 22}, "facing": "down",
         "sprite": "wren", "movement": "static",
         "dialogue_ref": "script.wren_dawnstead", "hidden_when_flag": "flag:wren_a6"},
        {"id": "wren_rm", "at": {"tx": 16, "ty": 22}, "facing": "down",
         "sprite": "wren", "movement": "static",
         "dialogue_ref": "script.wren_rematch", "requires_flag": "flag:wren_a6"},
        # CÒR AT HIS LAMP — staged: quiet keeping -> the wick hand-in (P2) ->
        # the line he earns. Never gloated over; grief eased, not defeated.
        {"id": "cor_lamp_keeper", "at": {"tx": 3, "ty": 21}, "facing": "left",
         "sprite": "cor", "movement": "static",
         "dialogue_ref": "npc.cor_lamp",
         "requires_flag": "flag:dawn", "hidden_when_flag": "flag:q_post_wick"},
        {"id": "cor_wick", "at": {"tx": 3, "ty": 21}, "facing": "left",
         "sprite": "cor", "movement": "static",
         "dialogue_ref": "script.cor_wick_given",
         "requires_flag": "flag:q_post_wick", "hidden_when_flag": "flag:q_post_wick_given"},
        {"id": "cor_after", "at": {"tx": 3, "ty": 21}, "facing": "left",
         "sprite": "cor", "movement": "static",
         "dialogue_ref": "npc.cor_lamp_after", "requires_flag": "flag:q_post_wick_given"},
        # The first-dawn festival — the town out in the sun (Arc E capstone).
        {"id": "dawn_piper", "at": {"tx": 11, "ty": 8}, "facing": "down",
         "sprite": "npc_man", "movement": "look_around",
         "dialogue_ref": "npc.dawnstead_piper", "requires_flag": "flag:dawn"},
        {"id": "dawn_baker", "at": {"tx": 17, "ty": 9}, "facing": "down",
         "sprite": "npc_woman", "movement": "wander",
         "dialogue_ref": "npc.dawnstead_baker", "requires_flag": "flag:dawn"},
        {"id": "dawn_kid", "at": {"tx": 7, "ty": 9}, "facing": "up",
         "sprite": "npc_boy", "movement": "look_around",
         "dialogue_ref": "npc.dawnstead_kid", "requires_flag": "flag:dawn"},
        # A cache on the strand (the variety rule: loose wicks off the lane).
        {"id": "cache_dawnstead_wicks", "at": {"tx": 24, "ty": 6}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_dawnstead_cache",
         "hidden_when_flag": "flag:picked_dawnstead_cache"},
    ],
    "gates": [], "music": "assets/audio/music/dawnstead-a.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
