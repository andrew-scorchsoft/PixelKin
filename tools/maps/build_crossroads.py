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
        # sleeping roads (inert teases until their maps are authored)
        {"id": "to_marsh", "at": {"tx": CX, "ty": 0}, "trigger": "step_on",
         "to_map": "coldfog_marches_i", "to": {"tx": 8, "ty": 28}, "facing": "up", "transition": "fade"},
        {"id": "to_marsh_e", "at": {"tx": CX + 1, "ty": 0}, "trigger": "step_on",
         "to_map": "coldfog_marches_i", "to": {"tx": 8, "ty": 28}, "facing": "up", "transition": "fade"},
        # the inward Spire road — gated on the full crown (endgame), and inert besides
        {"id": "to_penumbra", "at": {"tx": CX, "ty": H - 1}, "trigger": "step_on",
         "to_map": "penumbra_ring", "to": {"tx": 10, "ty": 2}, "facing": "down",
         "requires_flag": "flag:hub_unlocked", "transition": "fade"},
        {"id": "to_penumbra_e", "at": {"tx": CX + 1, "ty": H - 1}, "trigger": "step_on",
         "to_map": "penumbra_ring", "to": {"tx": 10, "ty": 2}, "facing": "down",
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
        {"id": "sign_spire", "kind": "sign",
         "at": {"tx": sign_tiles["sign_spire"][0], "ty": sign_tiles["sign_spire"][1]},
         "activation": "interact", "ref": "sign.crossroads_spire"},
        {"id": "sign_lowleaf", "kind": "sign",
         "at": {"tx": sign_tiles["sign_lowleaf"][0], "ty": sign_tiles["sign_lowleaf"][1]},
         "activation": "interact", "ref": "sign.crossroads_lowleaf"},
        {"id": "sign_galehigh", "kind": "sign",
         "at": {"tx": sign_tiles["sign_galehigh"][0], "ty": sign_tiles["sign_galehigh"][1]},
         "activation": "interact", "ref": "sign.crossroads_galehigh"},
        {"id": "sign_mineshortcut", "kind": "sign",
         "at": {"tx": sign_tiles["sign_mineshortcut"][0], "ty": sign_tiles["sign_mineshortcut"][1]},
         "activation": "interact", "ref": "sign.crossroads_mineshortcut"},
    ],
    "encounters": [],   # the hub is safe ground — a breath between roads
    "npcs": [
        # the Waykeeper tends the plaza lamps; stands just off the Waystone
        {"id": "waykeeper", "at": {"tx": CX - 1, "ty": CY - 1}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "look_around",
         "dialogue_ref": "npc.lanternway_keeper"},
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
        # Delivery sets flag:q_round_kite; the kid flies the kite thereafter.
        {"id": "waystone_kid", "at": {"tx": CX - 2, "ty": CY + 2}, "facing": "up",
         "sprite": "npc_boy", "movement": "static",
         "dialogue_ref": "script.round_kite_deliver",
         "hidden_when_flag": "flag:q_round_kite"},
        {"id": "waystone_kid_kite", "at": {"tx": CX - 2, "ty": CY + 2}, "facing": "up",
         "sprite": "npc_boy", "movement": "wander",
         "dialogue_ref": "npc.waystone_kid_kite",
         "requires_flag": "flag:q_round_kite"},
    ],
    "gates": [],
    "music": "assets/audio/music/tinderwick-a.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
