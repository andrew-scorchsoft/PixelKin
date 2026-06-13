#!/usr/bin/env python3
"""
Lowleaf Hollow — the bioluminescent fern town, mid-Glowmoss-Bloom
(walkthrough/02-east; Lumenary 3: Sable Quill, Verdant; Glimmerstep earned here).

The hour's heart. Three signature touches (level-design §8):
  1. THE GREY ELDER BED at the hollow's exact centre — the festival's missing
     note, flag-swapped grey→green by the Tended Bed chain (the §8 null-lantern
     pattern, warm edition: flag-gated MapObjects + the dancing ring around it);
  2. THE BLOOM ITSELF — stalls, a piper, kids chasing glow-motes, lantern-light
     everywhere EXCEPT the bed (festival NPCs are unconditional: the Bloom is
     in full swing on arrival, the Gleam only crowns it);
  3. THE DARK DEEPWOOD MOUTH on the north edge — the one place the green light
     stops dead; Glimmerstep-gated, signed, and straight ahead of the player
     the moment Sable grants the Gift.

Layout: fen road in from the south (the arrival band rides its tree pinch) →
the plaza + Elder Bed → Sable's Lumenary north-west (tallest) → the kiln and
stalls flanking the plaza → the forest-fringe lane east (band 18–20, two
bloom-warden sight trainers, the fen-wood cache) → `to_deepwood` north
(Glimmerstep) and the Lanternway spoke west to the Vesper Crossroads.

The Tended Bed (spine §5 shape #3, the LIGHT loop, deliberately the breath
between South's Causeway Bell and Cinderhead's Descent Vigil):
  script.sable_quest (hall) → flag:q_east_bloom → fen-wood cache
  (flag:picked_fenwood) → script.kiln_relight (flag:q_east_hearthspore) →
  script.warm_elder_bed at the bed (flag:q_east_bed_warm; grey→green) →
  the bond-test in the hall (requires q_east_bed_warm, blocked in her voice).

Run:  ./venv/bin/python tools/maps/build_lowleaf.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 32
rng = random.Random(83)
owed: list[str] = []

# ---- terrain grids ---------------------------------------------------------------
tree = mk.make_grid(W, H)
tallgrass = mk.make_grid(W, H)
path = mk.make_grid(W, H)

mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(5, 2, 2), (27, 10, 2), (2, 20, 2), (27, 26, 2)],
                  rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)
# the south road's TREE PINCH (the arrival band's choke, rows 24-25): a full
# seal to the borders — the band must cover EVERY walkable tile of the cut
mk.rect(tree, W, H, 1, 24, 12, 25)
mk.rect(tree, W, H, 17, 24, 28, 25)
mk.blob(tree, W, H, 11, 23.5, 2.4, 1.4)
mk.blob(tree, W, H, 18, 26.0, 2.4, 1.4)
# the fringe's inner tree tongue (shapes the lane east)
mk.blob(tree, W, H, 21, 1.5, 4.0, 1.6)

# the forest-fringe encounter beds (NE), the lane threading them
mk.blob(tallgrass, W, H, 19.5, 4.0, 2.6, 1.8)
mk.blob(tallgrass, W, H, 24.0, 7.5, 3.0, 1.8)
mk.blob(tallgrass, W, H, 27.0, 4.0, 1.8, 1.6)
# the MANDATORY crossing on the lane (cols 21-22; grass wins over the lane there)
for y in (5, 6, 7):
    for x in (21, 22):
        tallgrass[y * W + x] = 1

# roads: south (fen), north (deepwood), west (Lanternway), the plaza, the lanes
mk.vline(path, W, H, 14, 17, 31); mk.vline(path, W, H, 15, 17, 31)   # south road
mk.vline(path, W, H, 14, 0, 11); mk.vline(path, W, H, 15, 0, 11)     # north road
mk.hline(path, W, H, 14, 0, 10); mk.hline(path, W, H, 15, 0, 10)     # west road
mk.rect(path, W, H, 10, 11, 19, 16)                                  # the plaza
mk.hline(path, W, H, 9, 8, 15)                                       # Lumenary forecourt
mk.vline(path, W, H, 10, 9, 11)                                      # forecourt -> plaza
mk.hline(path, W, H, 6, 16, 26)                                      # fringe lane east
mk.vline(path, W, H, 26, 2, 6)                                       # lane up to the wood-stack
mk.vline(path, W, H, 24, 17, 22)                                     # lane to the bower door
mk.hline(path, W, H, 17, 16, 24)
mk.vline(path, W, H, 19, 13, 13)                                     # kiln approach
mk.hline(path, W, H, 13, 16, 19)

# warp openings carved from the enclosure
for (x, y) in [(14, 0), (15, 0), (14, 1), (15, 1),
               (14, 30), (15, 30), (14, 31), (15, 31)]:
    tree[y * W + x] = 0
for (x, y) in [(0, 14), (0, 15), (1, 14), (1, 15)]:
    tree[y * W + x] = 0

# precedence: trees claim; the lane pauses through the mandatory fringe band,
# elsewhere it carves grass
for i in range(W * H):
    y, x = i // W, i % W
    if path[i] and tallgrass[i]:
        if 21 <= x <= 22 and 5 <= y <= 7:
            path[i] = 0      # the lane pauses through the crossing
        else:
            tallgrass[i] = 0
    if tree[i]:
        tallgrass[i] = 0
        path[i] = 0

terrain_layers = [
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]

# ---- base + deco -----------------------------------------------------------------
gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]

deco = mk.make_grid(W, H)
# glow-shrooms: the town's own light, thickest near the bed and the lane mouths
for (x, y, n) in [(9, 12, "glowshroom_a"), (17, 11, "glowshroom_b"), (12, 17, "glowshroom_a"),
                  (18, 16, "glowshroom_b"), (16, 2, "glowshroom_a"), (7, 10, "glowshroom_b"),
                  (3, 16, "glowshroom_a"), (24, 16, "glowshroom_b"), (13, 19, "glowshroom_a"),
                  (16, 9, "glowshroom_b")]:
    deco[y * W + x] = gid(n)
# a fenced festival garden between plaza and bower lane
mk.fence_run(deco, W, H, 17, 18, 20)
for (x, y) in [(17, 19), (18, 19), (19, 19), (20, 19)]:
    deco[y * W + x] = gid("flowerbed_a") if x % 2 else gid("flowerbed_b")
mk.fence_run(deco, W, H, 17, 20, 20)

# ---- objects: the town -------------------------------------------------------------
objects = [
    # Sable's Lumenary — central-north, the tallest thing in the hollow
    {"id": "lumenary", "sprite": "lowleaf_lumenary", "at": {"tx": 8, "ty": 3},
     "w": 6, "h": 6, "overhang": 3},
    # cottages: one latched for the festival (everyone's outside), one the bower
    {"id": "cottage_a", "sprite": "lowleaf_cottage", "at": {"tx": 2, "ty": 4},
     "w": 5, "h": 5, "overhang": 3},
    {"id": "bower", "sprite": "lowleaf_cottage", "at": {"tx": 22, "ty": 18},
     "w": 5, "h": 5, "overhang": 3},
    # the kiln, cold until the Tended Bed chain fires it
    {"id": "kiln", "sprite": "lowleaf_kiln", "at": {"tx": 19, "ty": 10},
     "w": 2, "h": 3, "overhang": 1},
    # festival stalls flanking the plaza
    {"id": "stall_a", "sprite": "lowleaf_stall", "at": {"tx": 7, "ty": 13},
     "w": 2, "h": 2, "overhang": 1},
    {"id": "stall_b", "sprite": "lowleaf_stall", "at": {"tx": 20, "ty": 13},
     "w": 2, "h": 2, "overhang": 1},
    # THE ELDER BED — the Bloom's centrepiece, grey until tended (the §8 swap:
    # same footprint, same solidity, flag-paired visibility)
    {"id": "elder_bed_grey", "sprite": "lowleaf_elder_bed_grey",
     "at": {"tx": 13, "ty": 12}, "w": 3, "h": 2,
     "hidden_when_flag": "flag:q_east_bed_warm"},
    {"id": "elder_bed_green", "sprite": "lowleaf_elder_bed_green",
     "at": {"tx": 13, "ty": 12}, "w": 3, "h": 2,
     "requires_flag": "flag:q_east_bed_warm"},
    # lamp posts along the roads (1x3 objects — never 1-tile lamps)
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 9},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 16, "ty": 18},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 4, "ty": 12},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_d", "sprite": "tinderwick_lamp_post", "at": {"tx": 13, "ty": 26},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
m: dict = {
    "id": "lowleaf_hollow", "display_name": "Lowleaf Hollow", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": objects,
    "warps": [
        # north: the deepwood mouth — Glimmerstep, freshly earned, gates it
        {"id": "to_deepwood", "at": {"tx": 14, "ty": 0}, "trigger": "step_on",
         "to_map": "glowmoss_deep", "to": {"tx": 7, "ty": 27}, "facing": "up",
         "requires_ability": "glimmerstep", "blocked_ref": "sign.lowleaf_deepwood",
         "transition": "fade"},
        {"id": "to_deepwood_e", "at": {"tx": 15, "ty": 0}, "trigger": "step_on",
         "to_map": "glowmoss_deep", "to": {"tx": 8, "ty": 27}, "facing": "up",
         "requires_ability": "glimmerstep", "blocked_ref": "sign.lowleaf_deepwood",
         "transition": "fade"},
        # south: back through the treeline into the fen
        {"id": "to_fen_ii", "at": {"tx": 14, "ty": 31}, "trigger": "step_on",
         "to_map": "saltreach_fen_ii", "to": {"tx": 15, "ty": 1}, "facing": "down",
         "transition": "fade"},
        {"id": "to_fen_ii_e", "at": {"tx": 15, "ty": 31}, "trigger": "step_on",
         "to_map": "saltreach_fen_ii", "to": {"tx": 16, "ty": 1}, "facing": "down",
         "transition": "fade"},
        # west: the Lanternway spoke to the Vesper Crossroads (graph.ts)
        {"id": "to_crossroads", "at": {"tx": 0, "ty": 14}, "trigger": "step_on",
         "to_map": "vesper_crossroads", "to": {"tx": 19, "ty": 3}, "facing": "left",
         "transition": "fade"},
        {"id": "to_crossroads_s", "at": {"tx": 0, "ty": 15}, "trigger": "step_on",
         "to_map": "vesper_crossroads", "to": {"tx": 19, "ty": 4}, "facing": "left",
         "transition": "fade"},
        # The Lumenary's double door. This cottage is drawn in 3/4 view, so the door
        # art sits LEFT of centre (cols 1-2 = tiles (9,8)/(10,8)); both art tiles warp
        # in. (Earlier the twin sat at (11,8) — a wall tile right of the door, a
        # phantom entry — while the door's own left half (9,8) stayed solid.)
        {"id": "to_lumenary", "at": {"tx": 10, "ty": 8}, "trigger": "interact",
         "to_map": "lowleaf_lumenary", "to": {"tx": 8, "ty": 10}, "facing": "down",
         "requires_flag": "flag:has_starter", "transition": "door"},
        {"id": "to_lumenary_e", "at": {"tx": 9, "ty": 8}, "trigger": "interact",
         "to_map": "lowleaf_lumenary", "to": {"tx": 8, "ty": 10}, "facing": "down",
         "requires_flag": "flag:has_starter", "transition": "door"},
        # the guest-bower (the town's rest point)
        {"id": "to_bower", "at": {"tx": 24, "ty": 22}, "trigger": "interact",
         "to_map": "lowleaf_bower", "to": {"tx": 7, "ty": 9}, "facing": "down",
         "transition": "door"},
    ],
    "triggers": [
        # the ARRIVAL band — the Bloom reveal + grey-bed tease, on every
        # walkable tile of the south pinch (over-banding is safe)
        *[{"id": f"bloom_arrival_{x}_{y}", "kind": "cutscene", "at": {"tx": x, "ty": y},
           "activation": "step_on", "ref": "script.glowmoss_bloom_arrival", "once": True,
           "sets_flags": ["flag:bloom_arrival_seen"],
           "hidden_when_flag": "flag:bloom_arrival_seen"}
          for y in (23, 24, 25) for x in (13, 14, 15, 16)],
        # the CROWNING band — fires on the first walk out of the hall with the
        # Verdant standing (rows 9-10 around the door; landing never auto-fires)
        *[{"id": f"bloom_crowning_{x}_{y}", "kind": "cutscene", "at": {"tx": x, "ty": y},
           "activation": "step_on", "ref": "script.bloom_crowning", "once": True,
           "requires_flag": "gleam:verdant",
           "sets_flags": ["flag:bloom_crowned"],
           "hidden_when_flag": "flag:bloom_crowned"}
          for y in (9, 10) for x in range(8, 17)],
        # THE ELDER BED — interact chain on its south face: cold (blocked, in
        # narration) -> the warming (the loop's payoff) -> the green read
        *[t for x in (13, 14, 15) for t in (
            {"id": f"elder_bed_warm_{x}", "kind": "script", "at": {"tx": x, "ty": 13},
             "activation": "interact", "ref": "script.warm_elder_bed", "once": True,
             "requires_flag": "flag:q_east_hearthspore",
             "blocked_ref": "npc.elder_bed_cold",
             "sets_flags": ["flag:q_east_bed_warm"],
             "hidden_when_flag": "flag:q_east_bed_warm"},
            {"id": f"elder_bed_green_{x}", "kind": "sign", "at": {"tx": x, "ty": 13},
             "activation": "interact", "ref": "npc.elder_bed_green",
             "requires_flag": "flag:q_east_bed_warm"},
        )],
        # cottage A is latched for the festival (everyone is outside)
        {"id": "cottage_latched", "kind": "sign", "at": {"tx": 4, "ty": 8},
         "activation": "interact", "ref": "npc.cottage_latched"},
    ],
    "npcs": [
        # --- the Tended Bed cast -------------------------------------------------
        # the kilner, three flag-disjoint stages beside her cold kiln
        {"id": "kilner_pre", "at": {"tx": 18, "ty": 12}, "facing": "right",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "npc.kilner_cold",
         "hidden_when_flag": "flag:picked_fenwood"},
        {"id": "kilner_fire", "at": {"tx": 18, "ty": 12}, "facing": "right",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.kiln_relight",
         "requires_flag": "flag:picked_fenwood",
         "hidden_when_flag": "flag:q_east_hearthspore"},
        {"id": "kilner_after", "at": {"tx": 18, "ty": 12}, "facing": "right",
         "sprite": "npc_old_woman", "movement": "look_around",
         "dialogue_ref": "npc.kilner_after",
         "requires_flag": "flag:q_east_hearthspore"},
        # --- the festival (UNCONDITIONAL — the Bloom is on when you arrive) -------
        {"id": "bloom_piper", "at": {"tx": 12, "ty": 15}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.bloom_piper"},
        {"id": "bloom_fencer", "at": {"tx": 16, "ty": 14}, "facing": "left",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "npc.bloom_fencer"},
        {"id": "moss_kid", "at": {"tx": 17, "ty": 12}, "facing": "down",
         "sprite": "npc_child", "movement": "wander",
         "dialogue_ref": "npc.bloom_kid_a"},
        {"id": "fern_kid", "at": {"tx": 11, "ty": 12}, "facing": "down",
         "sprite": "npc_child", "movement": "wander",
         "dialogue_ref": "npc.bloom_kid_b"},
        {"id": "kindle_elder", "at": {"tx": 18, "ty": 15}, "facing": "left",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.kindle_elder"},
        # Wren — bright, ribbing; gone east once the Deep has shaken them (A3)
        {"id": "wren_lowleaf", "at": {"tx": 10, "ty": 17}, "facing": "right",
         "sprite": "wren", "movement": "look_around",
         "dialogue_ref": "npc.wren_lowleaf",
         "hidden_when_flag": "flag:met_hollowing"},
        # the crier — the post-Gleam mapwide "now accessible" callout (§5)
        {"id": "bloom_crier", "at": {"tx": 14, "ty": 16}, "facing": "down",
         "sprite": "npc_man", "movement": "look_around",
         "dialogue_ref": "npc.bloom_crier",
         "requires_flag": "gleam:verdant"},
        # --- the provisioner stall (kit -> open counter, the standing pattern) ----
        {"id": "provisioner_kit", "at": {"tx": 8, "ty": 15}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.shop_kit_lowleaf",
         "hidden_when_flag": "flag:lowleaf_kit"},
        {"id": "provisioner", "at": {"tx": 8, "ty": 15}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.shop_lowleaf",
         "requires_flag": "flag:lowleaf_kit"},
        # --- E2 "Spores for the Stall" — the Bloom stall-keeper's four stages -----
        {"id": "stall_quest", "at": {"tx": 20, "ty": 15}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.stall_quest",
         "hidden_when_flag": "flag:q_east_spores"},
        {"id": "stall_waiting", "at": {"tx": 20, "ty": 15}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "npc.stall_waiting",
         "requires_flag": "flag:q_east_spores",
         "hidden_when_flag": "flag:spore_squatter_beaten"},
        {"id": "stall_reward", "at": {"tx": 20, "ty": 15}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.stall_reward",
         "requires_flag": "flag:spore_squatter_beaten",
         "hidden_when_flag": "flag:q_east_spores_done"},
        {"id": "stall_after", "at": {"tx": 20, "ty": 15}, "facing": "down",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "npc.stall_after",
         "requires_flag": "flag:q_east_spores_done"},
    ],
    "gates": [],
    "encounters": [],
    "music": "assets/audio/music/lowleaf-hollow-a.mp3",
}

# the fringe lane's two bloom-warden SIGHT trainers (the fen-wood errand walks
# straight through both lines — trainers are geometry, §3a)
owed += pt.trainer_beat(m, tid="bloom_warden_a", at=(20, 6), facing="left",
                        sight=4, sprite="npc_woman")
owed += pt.trainer_beat(m, tid="bloom_warden_b", at=(26, 3), facing="down",
                        sight=3, sprite="npc_man")

# caches: the fen-wood (the chain's middle link), wicks behind the cottage,
# a charge at the fringe mouth
owed += pt.cache(m, cid="fenwood", at=(25, 2))
owed += pt.cache(m, cid="lowleaf_wicks", at=(5, 28))  # the SW pocket pays (§3a rule 4)
owed += pt.cache(m, cid="lowleaf_balm", at=(23, 28))  # …and the SE pocket behind the bower
owed += pt.cache(m, cid="lowleaf_charge", at=(17, 5))

# signs: the welcome, the Lumenary, the dark mouth, the Lanternway
owed += pt.sign(m, deco, W, sid="lowleaf_welcome", at=(13, 21))
owed += pt.sign(m, deco, W, sid="lowleaf_lumenary", at=(13, 9))
owed += pt.sign(m, deco, W, sid="lowleaf_deepwood", at=(13, 2))
owed += pt.sign(m, deco, W, sid="lowleaf_lanternway", at=(3, 13))

# the fringe encounter bed — band 18-20 (hooks §6): Sporeling / Fennlight /
# Mossglow / Barkhelm, rate 0.10 (Fennlight drifts in for the Bloom)
FRINGE_TABLE = [
    {"kin_id": 56, "weight": 40, "min_level": 18, "max_level": 20},  # Sporeling
    {"kin_id": 67, "weight": 25, "min_level": 18, "max_level": 20},  # Fennlight
    {"kin_id": 38, "weight": 20, "min_level": 18, "max_level": 20},  # Mossglow
    {"kin_id": 62, "weight": 15, "min_level": 18, "max_level": 20},  # Barkhelm
]
m["encounters"] = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass",
                                     rate=0.10, table=FRINGE_TABLE, id_prefix="fringe")

# crown trees for depth (§11 rule 2)
pt.crown_tree(m, oid="tree_a", sprite="tinderwick_tree", at=(2, 11))
pt.crown_tree(m, oid="tree_b", sprite="tinderwick_tree", at=(5, 17))
pt.crown_tree(m, oid="tree_c", sprite="tinderwick_tree", at=(17, 19))
pt.crown_tree(m, oid="tree_d", sprite="tinderwick_tree", at=(25, 12))
pt.crown_tree(m, oid="tree_e", sprite="tinderwick_tree", at=(8, 19))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
mk.scatter_decor(deco, base, W, H, rng, density=0.12,
                 avoid=building_cells | {(x, y) for y in range(H) for x in range(W)
                                         if path[y * W + x] or tallgrass[y * W + x]
                                         or tree[y * W + x]})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
