#!/usr/bin/env python3
"""
Vesper Crossroads — the Lanternway hub (graph.ts `vesper_crossroads`, kind `hub`).

Where every lit road in Vesperholm meets (walkthrough/01-south). A safe, warm
clearing — no encounters: four roads meeting at a lamplit plaza around the
Waystone, deep forest enclosure, one cliff accent.

THE OPENING HAPPENS HERE (the satchel errand): Star-tender Fenn waits at the
waystone from minute one — the town points the unstarted player east along the
safe Lanternway, Fenn sends them back for his forgotten satchel, and the
vesperlamp + starter ceremony (script.intro_mentor) is held AT the waystone.
Fenn is four flag-disjoint placements on one tile; the Pearlmoor spoke is
has_starter-gated so the opening can't wander past the ceremony.

Live spokes: WEST -> Tinderwick, EAST -> Pearlmoor Quay. The NORTH road (Coldfog
Marches) and SOUTH inward road (the Spire approach / penumbra_ring) are signed,
visible, inert teases — the engine no-ops warps to unregistered maps.

THE ENDGAME ALSO HAPPENS HERE (C3 wiring, walkthrough/05): C4 Fenn's counsel +
A5 Wren-joins (the inward road's full-cut band at y=16 carries Fenn's Starlamp
up — the Keylumen's asking-gift, un-missable), C1 "Lampling's Trail" (the kid +
three guttering dusk-lamp interacts + the gentle set-piece catch on the lamp
ring), C2 "The Inn's Empty Lamps" (the four-stage waystation innkeeper — rest +
the crossroads_inn counter at every stage), and C3 "The Long Round" (the
Waykeeper's close-out, riding his chart-hung stage).

audit_flow WAIVER — `choke` WARN on script.wren_joins accepted (the fenn_wave
precedent): the only band-avoiding paths the model finds start at the penumbra
return landing (reachable only by crossing the band once, going in) or idle on
the gated mine-shortcut warp tile (8,17), which the engine whisks away from
(or, unheld, can only be reached THROUGH the band). The Starlamp delivery is
safe by mechanics.

Run:  python3 tools/maps/build_crossroads.py
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 20, 18
rng = random.Random(31)

# ---- terrain ------------------------------------------------------------------
# Deep forest enclosure on ALL sides (a clearing, not a coast) with organic bumps.
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(7, 1, 1), (13, 1, 1), (2, 12, 2), (17, 13, 2), (8, 1, 1)])
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)              # bottom border too
mk.blob(tree, W, H, 5, 15, 2.0, 1.4)
mk.blob(tree, W, H, 14, 15, 2.0, 1.4)

# the clearing's accent: a small still pool in the west, where wayfarers water
# their kin. (It moved south-west when the Galehigh spoke woke through the old
# NW corner — the pond keeps migrating as the Lanternway wakes.)
pond = mk.make_grid(W, H)
mk.blob(pond, W, H, 4.5, 12, 1.6, 1.2)
for y in range(H):                                       # pool replaces tree there
    for x in range(W):
        if pond[y * W + x]:
            tree[y * W + x] = 0

# the four roads + the plaza around the Waystone
path = mk.make_grid(W, H)
CX, CY = 9, 9                                            # plaza centre-ish
mk.rect(path, W, H, CX - 2, CY - 2, CX + 3, CY + 2)      # the plaza apron
mk.hline(path, W, H, CY, 0, CX); mk.hline(path, W, H, CY - 1, 0, CX)   # west road
mk.hline(path, W, H, CY, CX, W - 1); mk.hline(path, W, H, CY - 1, CX, W - 1)  # east road
mk.vline(path, W, H, CX, 0, CY); mk.vline(path, W, H, CX + 1, 0, CY)   # north road
mk.vline(path, W, H, CX, CY, H - 1); mk.vline(path, W, H, CX + 1, CY, H - 1)  # south road
# the LOWLEAF spoke: east-north out of the clearing (wakes with the Verdant
# Gleam — the warp below carries the gate; walkthrough R3 "wakes with spoke")
mk.hline(path, W, H, 3, CX, W - 1); mk.hline(path, W, H, 4, CX, W - 1)
# the GALEHIGH spoke: west-north out of the clearing (wakes with the Storm
# Gleam — same pattern; walkthrough R4 "[wakes with spoke]")
mk.hline(path, W, H, 3, 0, CX); mk.hline(path, W, H, 4, 0, CX)
# the NIGHTREACH spoke: out of the clearing's NW corner, joining the Galehigh
# road rows (wakes with the Lunar Gleam — the warp below carries the gate; the
# LAST Lanternway spoke, walkthrough 04-west "exit via the Lanternway". With it
# the Round's anchor faces all five lit roads.)
mk.vline(path, W, H, 3, 0, 4); mk.vline(path, W, H, 4, 0, 4)
# the MINE-CART HOIST spur (SW, by the south road): the Cinderhead Deep
# shortcut's hub end — a cart-lift that only runs once the sealed door is
# opened from the deep (graph.ts `shortcut_crossroads`, wakes with
# flag:shortcut_mine; walkthrough/02-east §0 rule 3). A short stub to the edge.
mk.rect(path, W, H, CX - 1, 16, CX, 16); mk.vline(path, W, H, CX - 1, 16, 17)
# punch the borders where the roads leave
for y in (CY - 1, CY):
    tree[y * W + 0] = 0; tree[y * W + 1] = 0
    tree[y * W + (W - 1)] = 0; tree[y * W + (W - 2)] = 0
for x in (CX, CX + 1):
    tree[0 * W + x] = 0; tree[1 * W + x] = 0
    tree[(H - 1) * W + x] = 0; tree[(H - 2) * W + x] = 0
for y in (3, 4):
    tree[y * W + (W - 1)] = 0; tree[y * W + (W - 2)] = 0
    tree[y * W + 0] = 0; tree[y * W + 1] = 0
# punch the Nightreach spoke opening (NW, cols 3-4)
for x in (3, 4):
    tree[0 * W + x] = 0; tree[1 * W + x] = 0
# punch the mine-cart hoist opening (SW edge, col CX-1)
for y in (16, 17):
    tree[y * W + (CX - 1)] = 0

# ---- base + layers --------------------------------------------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_pond", "role": "terrain", "terrain": "pond",
     "set": "vesper_overworld_set", "depth": 0, "data": pond},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
]

# ---- objects: crown trees + the plaza's four lamps -------------------------------
objects = [
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 2, "ty": 2}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 14, "ty": 12}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 3, "ty": 12}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_d", "sprite": "tinderwick_tree", "at": {"tx": 12, "ty": 1}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    # the plaza's lamp ring — the hub IS lamplight (no 1-tile lamps; 1x3 posts)
    {"id": "lamp_nw", "sprite": "tinderwick_lamp_post", "at": {"tx": CX - 3, "ty": CY - 4}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_ne", "sprite": "tinderwick_lamp_post", "at": {"tx": CX + 4, "ty": CY - 4}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_sw", "sprite": "tinderwick_lamp_post", "at": {"tx": CX - 3, "ty": CY + 1}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_se", "sprite": "tinderwick_lamp_post", "at": {"tx": CX + 4, "ty": CY + 1}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, pond, path))}
avoid = covered | building_cells
# C3 ENDGAME placements stand on these grass tiles — keep scatter decor off them
# (the trail kid, the waystation innkeeper, Wren at the inward road).
ENDGAME_NPC_TILES = {(5, 7), (11, 12), (11, 14)}
avoid |= ENDGAME_NPC_TILES

# ---- deco: the Waystone, signs, flowerbeds, scatter -------------------------------
deco = mk.make_grid(W, H)
# the Waystone: a boulder cluster at the plaza's heart (collides; walked around)
for (x, y) in [(CX, CY - 1), (CX + 1, CY - 1)]:
    deco[y * W + x] = gid("boulder")
# flowerbeds soften the plaza corners
for (x, y) in [(CX - 2, CY - 2), (CX + 3, CY - 2), (CX - 2, CY + 2), (CX + 3, CY + 2)]:
    deco[y * W + x] = gid("flowerbed_a") if (x + y) % 2 else gid("flowerbed_b")
sign_tiles = {
    "sign_waystone": (CX + 2, CY),       # on the plaza, by the Waystone
    "sign_spire": (CX - 1, CY + 3),      # beside the south (inward) road
    "sign_lowleaf": (CX + 3, 5),         # beside the east-north (Lowleaf) spoke
    "sign_galehigh": (CX - 4, 5),        # beside the west-north (Galehigh) spoke
    "sign_nightreach": (2, 5),           # beside the NW (Nightreach) spoke
    "sign_mineshortcut": (CX - 2, 16),   # beside the mine-cart hoist (SW stub)
}
for (x, y) in sign_tiles.values():
    deco[y * W + x] = gid("sign")
mk.scatter_decor(deco, base, W, H, rng, density=0.14, avoid=avoid)

# ---- assemble ---------------------------------------------------------------------
m = {
    "id": "vesper_crossroads", "display_name": "Vesper Crossroads", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "hub",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # live spokes (graph.ts): WEST <-> Tinderwick, EAST <-> Pearlmoor Quay
        {"id": "to_tinderwick", "at": {"tx": 0, "ty": CY}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 26, "ty": 16}, "facing": "left", "transition": "fade"},
        {"id": "to_tinderwick_n", "at": {"tx": 0, "ty": CY - 1}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 26, "ty": 16}, "facing": "left", "transition": "fade"},
        # has_starter-gated: the opening's errand loop happens at the waystone —
        # the east road wakes the moment the ceremony ends.
        {"id": "to_pearlmoor", "at": {"tx": W - 1, "ty": CY}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 1, "ty": 12}, "facing": "right",
         "requires_flag": "flag:has_starter", "transition": "fade"},
        {"id": "to_pearlmoor_n", "at": {"tx": W - 1, "ty": CY - 1}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 1, "ty": 12}, "facing": "right",
         "requires_flag": "flag:has_starter", "transition": "fade"},
        # the Lowleaf spoke (east-north) — wakes with the Verdant Gleam
        # (graph.ts declares it ungated; the warp-level flag mirrors the South
        # pattern of gating stricter than the graph, with the Waykeeper's own
        # "not yet" — the long way round is the fen-road, always open).
        {"id": "to_lowleaf", "at": {"tx": W - 1, "ty": 3}, "trigger": "step_on",
         "to_map": "lowleaf_hollow", "to": {"tx": 1, "ty": 14}, "facing": "right",
         "requires_flag": "gleam:verdant", "blocked_ref": "npc.waykeeper_lowleaf_gate",
         "transition": "fade"},
        {"id": "to_lowleaf_s", "at": {"tx": W - 1, "ty": 4}, "trigger": "step_on",
         "to_map": "lowleaf_hollow", "to": {"tx": 1, "ty": 15}, "facing": "right",
         "requires_flag": "gleam:verdant", "blocked_ref": "npc.waykeeper_lowleaf_gate",
         "transition": "fade"},
        # the Galehigh spoke (west-north) — wakes with the Storm Gleam (the
        # Lowleaf pattern verbatim: graph.ts declares it ungated, the warp
        # gates stricter with the Waykeeper's own "not yet"; the long way
        # round is Cinderhead Deep's gallery, always open).
        {"id": "to_galehigh", "at": {"tx": 0, "ty": 3}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 15, "ty": 30}, "facing": "up",
         "requires_flag": "gleam:storm", "blocked_ref": "npc.waykeeper_galehigh_gate",
         "transition": "fade"},
        {"id": "to_galehigh_s", "at": {"tx": 0, "ty": 4}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 16, "ty": 30}, "facing": "up",
         "requires_flag": "gleam:storm", "blocked_ref": "npc.waykeeper_galehigh_gate",
         "transition": "fade"},
        # the Nightreach spoke (NW) — wakes with the Lunar Gleam (the
        # Lowleaf/Galehigh pattern verbatim: graph.ts declares it ungated,
        # the warp gates stricter with the Waykeeper's own "not yet"; the
        # long way round is the rim road, always open).
        {"id": "to_nightreach", "at": {"tx": 3, "ty": 0}, "trigger": "step_on",
         "to_map": "nightreach_observatory", "to": {"tx": 4, "ty": 28}, "facing": "up",
         "requires_flag": "gleam:lunar", "blocked_ref": "npc.waykeeper_nightreach_gate",
         "transition": "fade"},
        {"id": "to_nightreach_e", "at": {"tx": 4, "ty": 0}, "trigger": "step_on",
         "to_map": "nightreach_observatory", "to": {"tx": 5, "ty": 28}, "facing": "up",
         "requires_flag": "gleam:lunar", "blocked_ref": "npc.waykeeper_nightreach_gate",
         "transition": "fade"},
        # sleeping roads (inert teases until their maps are authored)
        {"id": "to_marsh", "at": {"tx": CX, "ty": 0}, "trigger": "step_on",
         "to_map": "coldfog_marches_i", "to": {"tx": 8, "ty": 28}, "facing": "up", "transition": "fade"},
        {"id": "to_marsh_e", "at": {"tx": CX + 1, "ty": 0}, "trigger": "step_on",
         "to_map": "coldfog_marches_i", "to": {"tx": 8, "ty": 28}, "facing": "up", "transition": "fade"},
        # the inward Spire road — gated on the full crown (endgame). The fade is
        # a step THROUGH the fog-wall: it lands on the Ring's SOUTH entry (ON
        # its return pair, facing up toward the Spire silhouette at the north
        # rim — the C1 look-up moment; see build_penumbra_ring.py HANDSHAKE).
        {"id": "to_penumbra", "at": {"tx": CX, "ty": H - 1}, "trigger": "step_on",
         "to_map": "penumbra_ring", "to": {"tx": 13, "ty": 33}, "facing": "up",
         "requires_flag": "flag:hub_unlocked", "transition": "fade"},
        {"id": "to_penumbra_e", "at": {"tx": CX + 1, "ty": H - 1}, "trigger": "step_on",
         "to_map": "penumbra_ring", "to": {"tx": 14, "ty": 33}, "facing": "up",
         "requires_flag": "flag:hub_unlocked", "transition": "fade"},
        # the Cinderhead Deep mine-cart shortcut (graph.ts `shortcut_crossroads`
        # return half) — wakes with flag:shortcut_mine, set on opening the sealed
        # door from the deep. Lands beside the deep's far-side return warp.
        {"id": "shortcut_cinderhead", "at": {"tx": CX - 1, "ty": H - 1}, "trigger": "step_on",
         "to_map": "cinderhead_deep", "to": {"tx": 21, "ty": 15}, "facing": "up",
         "requires_flag": "flag:shortcut_mine", "blocked_ref": "sign.crossroads_mineshortcut",
         "transition": "fade"},
    ],
    "triggers": [
        # Fenn hails the player the first time they step into the plaza from the
        # west road (both lane rows covered; the script's sets_flags hides both).
        # audit_flow WAIVER — `choke` WARN accepted: the wave is a cosmetic
        # greeting, not a story gate; the ceremony rides the Fenn NPC himself,
        # so a player who skirts the band loses nothing.
        {"id": "fenn_wave", "kind": "cutscene", "at": {"tx": CX - 2, "ty": CY - 1},
         "activation": "step_on", "ref": "script.fenn_wave", "once": True,
         "hidden_when_flag": "flag:fenn_waved", "sets_flags": ["flag:fenn_waved"]},
        {"id": "fenn_wave_s", "kind": "cutscene", "at": {"tx": CX - 2, "ty": CY},
         "activation": "step_on", "ref": "script.fenn_wave", "once": True,
         "hidden_when_flag": "flag:fenn_waved", "sets_flags": ["flag:fenn_waved"]},
        {"id": "sign_waystone", "kind": "sign",
         "at": {"tx": sign_tiles["sign_waystone"][0], "ty": sign_tiles["sign_waystone"][1]},
         "activation": "interact", "ref": "sign.crossroads"},
        # The inward-road sign swaps on the full Crown: cold braziers -> the
        # "now accessible" callout (05 §1.3). Hidden trigger is GONE at lookup,
        # so the open twin (requires hub_unlocked, listed second) takes over.
        {"id": "sign_spire", "kind": "sign",
         "at": {"tx": sign_tiles["sign_spire"][0], "ty": sign_tiles["sign_spire"][1]},
         "activation": "interact", "ref": "sign.crossroads_spire",
         "hidden_when_flag": "flag:hub_unlocked"},
        {"id": "sign_spire_open", "kind": "sign",
         "at": {"tx": sign_tiles["sign_spire"][0], "ty": sign_tiles["sign_spire"][1]},
         "activation": "interact", "ref": "sign.crossroads_spire_open",
         "requires_flag": "flag:hub_unlocked"},
        {"id": "sign_lowleaf", "kind": "sign",
         "at": {"tx": sign_tiles["sign_lowleaf"][0], "ty": sign_tiles["sign_lowleaf"][1]},
         "activation": "interact", "ref": "sign.crossroads_lowleaf"},
        {"id": "sign_galehigh", "kind": "sign",
         "at": {"tx": sign_tiles["sign_galehigh"][0], "ty": sign_tiles["sign_galehigh"][1]},
         "activation": "interact", "ref": "sign.crossroads_galehigh"},
        {"id": "sign_nightreach", "kind": "sign",
         "at": {"tx": sign_tiles["sign_nightreach"][0], "ty": sign_tiles["sign_nightreach"][1]},
         "activation": "interact", "ref": "sign.crossroads_nightreach"},
        {"id": "sign_mineshortcut", "kind": "sign",
         "at": {"tx": sign_tiles["sign_mineshortcut"][0], "ty": sign_tiles["sign_mineshortcut"][1]},
         "activation": "interact", "ref": "sign.crossroads_mineshortcut"},
        # --- C3 ENDGAME (walkthrough/05) ------------------------------------
        # A5 — Wren joins for the climb: a FULL-CUT band on the inward road's
        # only walkable row (cols 8-10 at y=16; everything else is tree), so
        # the Starlamp it carries can never be walked past. Silent pre-hub
        # (requires unmet + no blocked_ref = no-op, the dawn_breaks pattern).
        {"id": "wren_joins_w", "kind": "cutscene", "at": {"tx": CX - 1, "ty": 16},
         "activation": "step_on", "ref": "script.wren_joins", "once": True,
         "requires_flag": "flag:hub_unlocked",
         "hidden_when_flag": "flag:wren_joined", "sets_flags": ["flag:wren_joined"]},
        {"id": "wren_joins", "kind": "cutscene", "at": {"tx": CX, "ty": 16},
         "activation": "step_on", "ref": "script.wren_joins", "once": True,
         "requires_flag": "flag:hub_unlocked",
         "hidden_when_flag": "flag:wren_joined", "sets_flags": ["flag:wren_joined"]},
        {"id": "wren_joins_e", "kind": "cutscene", "at": {"tx": CX + 1, "ty": 16},
         "activation": "step_on", "ref": "script.wren_joins", "once": True,
         "requires_flag": "flag:hub_unlocked",
         "hidden_when_flag": "flag:wren_joined", "sets_flags": ["flag:wren_joined"]},
        # C1 "Lampling's Trail" — three guttering dusk-lamps (the plaza lamp
        # posts' solid base tiles, the sign-trigger pattern), in the kid's
        # order nw -> ne -> sw, then the catch at the se lamp. Pre-quest the
        # lamps answer with their quiet read (blocked_ref).
        {"id": "trail_lamp_1", "kind": "cutscene", "at": {"tx": CX - 3, "ty": CY - 2},
         "activation": "interact", "ref": "script.trail_lamp_1",
         "requires_flag": "flag:q_central_trail",
         "hidden_when_flag": "flag:q_central_trail_lamp1",
         "sets_flags": ["flag:q_central_trail_lamp1"],
         "blocked_ref": "npc.dusk_lamp_quiet"},
        {"id": "trail_lamp_2", "kind": "cutscene", "at": {"tx": CX + 4, "ty": CY - 2},
         "activation": "interact", "ref": "script.trail_lamp_2",
         "requires_flag": "flag:q_central_trail_lamp1",
         "hidden_when_flag": "flag:q_central_trail_lamp2",
         "sets_flags": ["flag:q_central_trail_lamp2"],
         "blocked_ref": "npc.dusk_lamp_quiet"},
        {"id": "trail_lamp_3", "kind": "cutscene", "at": {"tx": CX - 3, "ty": CY + 3},
         "activation": "interact", "ref": "script.trail_lamp_3",
         "requires_flag": "flag:q_central_trail_lamp2",
         "hidden_when_flag": "flag:q_central_trail_lamp3",
         "sets_flags": ["flag:q_central_trail_lamp3"],
         "blocked_ref": "npc.dusk_lamp_quiet"},
        # The trail's end: the Lampling, surfaced as a gentle set-piece catch
        # (legendaryBattle, cooldown 3 — the caughtFlag hides the trigger).
        {"id": "lampling_catch", "kind": "cutscene", "at": {"tx": CX + 4, "ty": CY + 3},
         "activation": "interact", "ref": "script.lampling_catch",
         "requires_flag": "flag:q_central_trail_lamp3",
         "hidden_when_flag": "flag:lampling_caught",
         "blocked_ref": "npc.dusk_lamp_quiet"},
        {"id": "lampling_after", "kind": "dialogue", "at": {"tx": CX + 4, "ty": CY + 3},
         "activation": "interact", "ref": "npc.lampling_after",
         "requires_flag": "flag:q_central_trail_done"},
    ],
    "encounters": [],   # the hub is safe ground — a breath between roads
    "npcs": [
        # the Waykeeper tends the plaza lamps; stands just off the Waystone.
        # R5 "A Chart for the Waykeeper" (the Round's LAST leg; walkthrough
        # 04-west) stages him in three flag-disjoint placements on one tile
        # (the Fenn waystone pattern): base -> delivery (the Nightreach junior
        # watcher's fresh star-chart, flag:q_round_chart_taken ->
        # script.round_chart_deliver -> flag:q_round_chart) -> the chart hung
        # on the Waystone (his after line carries the deco beat).
        {"id": "waykeeper", "at": {"tx": CX - 1, "ty": CY - 1}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "look_around",
         "dialogue_ref": "npc.lanternway_keeper",
         "hidden_when_flag": "flag:q_round_chart_taken"},
        {"id": "waykeeper_chart", "at": {"tx": CX - 1, "ty": CY - 1}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "script.round_chart_deliver",
         "requires_flag": "flag:q_round_chart_taken",
         "hidden_when_flag": "flag:q_round_chart"},
        # C3 "The Long Round": once the chart hangs (q_round_chart = the Round's
        # last leg, so ALL legs — the boolean chain), the Waykeeper offers one
        # last walk of the plaza lamps (script.long_round -> the Way-lamp
        # keepsake + flag:q_central_round_done), then settles into his done line.
        {"id": "waykeeper_hung", "at": {"tx": CX - 1, "ty": CY - 1}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "look_around",
         "dialogue_ref": "script.long_round",
         "requires_flag": "flag:q_round_chart",
         "hidden_when_flag": "flag:q_central_round_done"},
        {"id": "waykeeper_round_done", "at": {"tx": CX - 1, "ty": CY - 1}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "look_around",
         "dialogue_ref": "npc.waykeeper_round_done",
         "requires_flag": "flag:q_central_round_done"},
        # Star-tender Fenn at the waystone — the opening's anchor, in four
        # flag-disjoint stages on one tile (south of the Waystone, facing it):
        #   pre   (t0)               -> the satchel ask (script.fenn_crossroads)
        #   wait  (errand running)   -> "it's on the store counter, dear"
        #   ready (satchel in hand)  -> THE CEREMONY (script.intro_mentor)
        #   after (Wayfaring begun)  -> send-off; he moves on once dusk_begins
        {"id": "fenn_pre", "at": {"tx": CX + 1, "ty": CY + 1}, "facing": "up",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "script.fenn_crossroads",
         "hidden_when_flag": "flag:fenn_errand"},
        {"id": "fenn_waiting", "at": {"tx": CX + 1, "ty": CY + 1}, "facing": "up",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "npc.fenn_waiting",
         "requires_flag": "flag:fenn_errand", "hidden_when_flag": "flag:has_satchel"},
        {"id": "fenn_ready", "at": {"tx": CX + 1, "ty": CY + 1}, "facing": "up",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "script.intro_mentor",
         "requires_flag": "flag:has_satchel", "hidden_when_flag": "flag:has_starter"},
        {"id": "fenn_after", "at": {"tx": CX + 1, "ty": CY + 1}, "facing": "up",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "npc.fenn_waystone_after",
         "requires_flag": "flag:has_starter", "hidden_when_flag": "flag:dusk_begins"},
        # the Waystone kid — R4 "A Kite for the Waystone Kid"'s delivery anchor
        # (the kite-maker's leg of the Waykeeper's Round; walkthrough 03-north).
        # The kid waits for the kite (flag:q_round_kite_taken — set when the
        # kite-maker hands it over); delivery sets flag:q_round_kite and the
        # kid flies the kite thereafter.
        {"id": "waystone_kid", "at": {"tx": CX - 2, "ty": CY + 2}, "facing": "up",
         "sprite": "npc_boy", "movement": "static",
         "dialogue_ref": "script.round_kite_deliver",
         "requires_flag": "flag:q_round_kite_taken",
         "hidden_when_flag": "flag:q_round_kite"},
        # At endgame the kid trades the kite for the lamp-flickers (C1 below) —
        # hidden once the hub opens so the trail chain owns the cast slot.
        {"id": "waystone_kid_kite", "at": {"tx": CX - 2, "ty": CY + 2}, "facing": "up",
         "sprite": "npc_boy", "movement": "wander",
         "dialogue_ref": "npc.waystone_kid_kite",
         "requires_flag": "flag:q_round_kite",
         "hidden_when_flag": "flag:hub_unlocked"},

        # --- C3 ENDGAME placements (walkthrough/05 §1-§2, quests C1/C2/C4/A5) --
        # C4 — Fenn's counsel before the Spire: back at his waystone tile once
        # the Crown completes (flag-disjoint with the opening chain, which the
        # long-held flag:dusk_begins has retired).
        {"id": "fenn_counsel", "at": {"tx": CX + 1, "ty": CY + 1}, "facing": "up",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "script.fenn_crossroads_counsel",
         "requires_flag": "flag:hub_unlocked",
         "hidden_when_flag": "flag:fenn_counsel_given"},
        # SYNC 2026-06 (Three Hours wiring, 07-the-three §6): the after-stage
        # is now a script — it wraps npc.fenn_counsel_after and adds Fenn's
        # third-watch payoff on flag:three_dawn_met. Mirrored into the shipped
        # vesper_crossroads.json by hand — reconcile before re-running.
        {"id": "fenn_counsel_after", "at": {"tx": CX + 1, "ty": CY + 1}, "facing": "up",
         "sprite": "npc_mentor", "movement": "static",
         "dialogue_ref": "script.fenn_counsel_after",
         "requires_flag": "flag:fenn_counsel_given"},
        # A5 — Wren at the inward road (the band below is the guarantee; the
        # NPC is the face of it, interactable for players who walk up first).
        {"id": "wren_inward", "at": {"tx": CX + 2, "ty": 14}, "facing": "left",
         "sprite": "wren", "movement": "static",
         "dialogue_ref": "script.wren_joins",
         "requires_flag": "flag:hub_unlocked",
         "hidden_when_flag": "flag:wren_joined"},
        # C1 — the Waystone kid's trail (giver -> mid-quest hint -> done), by
        # the NW lamp where she saw the flickers first.
        {"id": "kid_trail", "at": {"tx": CX - 4, "ty": CY - 2}, "facing": "right",
         "sprite": "npc_boy", "movement": "static",
         "dialogue_ref": "script.lampling_trail_start",
         "requires_flag": "flag:hub_unlocked",
         "hidden_when_flag": "flag:q_central_trail"},
        {"id": "kid_trail_during", "at": {"tx": CX - 4, "ty": CY - 2}, "facing": "right",
         "sprite": "npc_boy", "movement": "static",
         "dialogue_ref": "npc.waystone_kid_trail",
         "requires_flag": "flag:q_central_trail",
         "hidden_when_flag": "flag:q_central_trail_done"},
        {"id": "kid_trail_done", "at": {"tx": CX - 4, "ty": CY - 2}, "facing": "right",
         "sprite": "npc_boy", "movement": "wander",
         "dialogue_ref": "npc.waystone_kid_trail_done",
         "requires_flag": "flag:q_central_trail_done"},
        # C2 — the waystation innkeeper (rest + counter at EVERY stage; the
        # four-token chain rides the strictly-ordered flags q_central_tokens ->
        # q_token_west -> q_central_tokens_done). Appears with the Tide Gleam
        # (the south festival pair complete — the first token's festival).
        {"id": "innkeeper_ask", "at": {"tx": CX + 2, "ty": CY + 3}, "facing": "left",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_empty_lamps",
         "requires_flag": "gleam:tide",
         "hidden_when_flag": "flag:q_central_tokens"},
        {"id": "innkeeper_waiting", "at": {"tx": CX + 2, "ty": CY + 3}, "facing": "left",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_rest_waiting",
         "requires_flag": "flag:q_central_tokens",
         "hidden_when_flag": "flag:q_token_west"},
        {"id": "innkeeper_hang", "at": {"tx": CX + 2, "ty": CY + 3}, "facing": "left",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_lamps_hang",
         "requires_flag": "flag:q_token_west",
         "hidden_when_flag": "flag:q_central_tokens_done"},
        {"id": "innkeeper_done", "at": {"tx": CX + 2, "ty": CY + 3}, "facing": "left",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.inn_rest_crossroads",
         "requires_flag": "flag:q_central_tokens_done"},
    ],
    "gates": [],
    "music": "assets/audio/music/tinderwick-a.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
