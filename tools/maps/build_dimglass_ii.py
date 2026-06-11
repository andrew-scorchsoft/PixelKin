#!/usr/bin/env python3
"""
Build Dimglass Coast II — the tidal flats — on the SHARED overworld set.

The canon middle segment of the South spine (walkthrough/01-south.md): wider, lower,
wetter than segment I, travelled south→north between Dimglass Coast I and Pearlmoor
Quay. Its job in the journey is the LEVEL BRIDGE (~8→10 band, so Pearlmoor's 12 isn't
a cliff) and the "come back later" web: BOTH gift-gated spurs live here per graph.ts —
the lantern-buoy line to Gullcry Rock (Tidecall) and the Tideglass Cavern mouth
(Glimmerstep) — visible, signed, unsolvable yet. Two travelling-Wayfarer trainer
battles carry the XP between the wild beats (the route GAMEPLAY between towns).

Run:  python3 tools/maps/build_dimglass_ii.py   (after build_shared_overworld.py)
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 18, 32
rng = random.Random(23)

# ---- terrain presence grids -------------------------------------------------
# West cliff wall (the same shelf as segment I, lower), sea east, and a WIDE tidal
# sand flat through the middle pocked with tide pools — the segment's own look.
cliff = mk.make_grid(W, H)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.rect(cliff, W, H, 0, H - 2, W - 1, H - 1)
for (bx, by, br) in [(2, 6, 1), (2, 17, 2), (2, 26, 1)]:
    mk.blob(cliff, W, H, bx, by, br + 0.4, br)
for x in range(6, 9):                                # north exit gap (to Pearlmoor)
    cliff[0 * W + x] = 0; cliff[1 * W + x] = 0
for x in range(6, 9):                                # south entry gap (from segment I)
    cliff[(H - 1) * W + x] = 0; cliff[(H - 2) * W + x] = 0

water = mk.make_grid(W, H)
mk.rect(water, W, H, 14, 2, W - 1, H - 3)            # open sea east
mk.blob(water, W, H, 14, 7, 1.8, 1.6)                # tide bites
mk.blob(water, W, H, 14, 21, 1.8, 1.8)
# tide pools in the flats (1-2 tile pools the player walks between)
for (cx, cy, rx, ry) in [(8.5, 8.5, 1.4, 1.0), (6.5, 19.5, 1.4, 1.0), (10.5, 25.5, 1.2, 1.0)]:
    mk.blob(water, W, H, cx, cy, rx, ry)
# the SHALLOWS finger out to Gullcry Rock — pure water tiles under an AbilityGate,
# the visible Tidecall promise (level-design Fork D)
mk.rect(water, W, H, 14, 11, 15, 14)

sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 5, 2, 13, H - 3)                 # the wide tidal flat
mk.blob(sand, W, H, 5, 12, 1.8, 2.6)
mk.blob(sand, W, H, 12, 17, 2.0, 2.0)

tallgrass = mk.make_grid(W, H)                       # dune-grass beats on the west strip
for (cx, cy, rx, ry) in [(4.5, 5.5, 2.0, 2.0), (4.0, 13.5, 1.8, 2.0), (4.5, 22.5, 2.0, 2.2)]:
    mk.blob(tallgrass, W, H, cx, cy, rx, ry)

# MANDATORY crossing: a dune-grass band (tufts over the sand bed) spans the flat
# at rows 16-17 — the road to Pearlmoor passes THROUGH encounter ground.
dunegrass = mk.make_grid(W, H)
for y in (16, 17):
    for x in range(5, 14):
        dunegrass[y * W + x] = 1

# THE TIDAL CHANNEL + BOARDWALK: the flats end at a water channel crossed by a
# pier — so arriving at Pearlmoor's jetty reads as one continuous walk over the
# shallows, not a teleport. Water spans rows 1-2; the lane crosses on boards
# laid over SAND (carved from the channel — dock over open water stays gated).
for y in (0, 1, 2):
    for x in range(2, W):
        water[y * W + x] = 1
        sand[y * W + x] = 0
        cliff[y * W + x] = 0
for y in (0, 1, 2):                                  # the pier's sand causeway
    for x in (6, 7, 8):
        water[y * W + x] = 0
        sand[y * W + x] = 1

# the lit lane: hugs the flat's west side, swings east around the pools;
# interrupted at the crossing rows (the dune grass spans the road)
path = mk.make_grid(W, H)
spine = [7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 8, 8,
         8, 8, 8, 7, 7, 7, 7, 7, 7, 7]
def spine_col(ty):
    return spine[min(max(ty - 2, 0), len(spine) - 1)]
for ty in range(3, H - 2):
    if ty in (16, 17):
        continue
    cx = spine_col(ty)
    path[ty * W + cx] = 1; path[ty * W + cx + 1] = 1
for x in range(6, 9):
    path[(H - 3) * W + x] = 1

# ---- base + terrain layers --------------------------------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    # dunegrass expands AFTER sand so the crossing's tufts sit ON the flat
    {"name": "t_dunegrass", "role": "terrain", "terrain": "dunegrass",
     "set": "vesper_overworld_set", "depth": 0, "data": dunegrass},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
    # path expands LAST: the lit lane stays continuous where tide pools lap it
    {"name": "t_path", "role": "terrain", "terrain": "trail",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
]

# ---- objects ------------------------------------------------------------------
objects = [
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 3, "ty": 7}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 2, "ty": 27}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 6, "ty": 4}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 11, "ty": 14}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 6, "ty": 24}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (cliff, water, sand, tallgrass, dunegrass, path))}
avoid = covered | building_cells

# ---- deco ---------------------------------------------------------------------
deco = mk.make_grid(W, H)
cave_xy = (2, 13)
for (x, y) in [cave_xy, (cave_xy[0], cave_xy[1] + 1)]:    # Tideglass Cavern mouth
    deco[y * W + x] = gid("cliff_fill")
# the buoy line THICKENS toward Gullcry (the spur is here on II, per graph.ts):
for (x, y) in [(14, 9), (15, 10), (15, 11), (16, 12), (15, 13), (14, 15), (16, 20), (15, 26)]:
    deco[y * W + x] = gid("buoy")
# the boardwalk pier over the tidal channel (boards on the sand causeway — dock
# over open water would inherit the Tidecall gate), continuing Pearlmoor's jetty
for y in (0, 1, 2):
    for x in (6, 7, 8):
        deco[y * W + x] = gid("dock")
for (x, y) in [(4, 1), (11, 1)]:                     # channel buoys flank the pier
    deco[y * W + x] = gid("buoy")
# boulders pock the flats + choke the spine at each trainer beat:
for (x, y) in [(11, 5), (12, 11), (5, 16), (12, 23), (9, 20)]:
    deco[y * W + x] = gid("boulder")
sign_xy = {
    "sign_gullcry": (13, 12),    # on the sand, facing the buoy line
    "sign_cave": (4, 16),        # by the cavern mouth
    "sign_quay": (6, 3),         # boundary sign — Pearlmoor sight-lined ahead
}
for (x, y) in sign_xy.values():
    deco[y * W + x] = gid("sign")
mk.scatter_decor(deco, base, W, H, rng, density=0.14, avoid=avoid)

# ---- assemble -------------------------------------------------------------------
m = {
    "id": "dimglass_coast_ii", "display_name": "Dimglass Coast", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # South gap is 3 wide -> a warp per tile, landing ON segment I's exit warps.
        {"id": "from_coast_i_w", "at": {"tx": 6, "ty": 31}, "trigger": "step_on",
         "to_map": "dimglass_coast", "to": {"tx": 6, "ty": 0}, "facing": "down", "transition": "fade"},
        {"id": "from_coast_i", "at": {"tx": 7, "ty": 31}, "trigger": "step_on",
         "to_map": "dimglass_coast", "to": {"tx": 7, "ty": 0}, "facing": "down", "transition": "fade"},
        {"id": "from_coast_i_e", "at": {"tx": 8, "ty": 31}, "trigger": "step_on",
         "to_map": "dimglass_coast", "to": {"tx": 8, "ty": 0}, "facing": "down", "transition": "fade"},
        # North: the boardwalk causeway (3 wide) onto Pearlmoor's jetty (2 wide),
        # landing ON the quay's return warps at the jetty tip.
        {"id": "to_quay_w", "at": {"tx": 6, "ty": 0}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 13, "ty": 21}, "facing": "up", "transition": "fade"},
        {"id": "to_quay", "at": {"tx": 7, "ty": 0}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 13, "ty": 21}, "facing": "up", "transition": "fade"},
        {"id": "to_quay_e", "at": {"tx": 8, "ty": 0}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 14, "ty": 21}, "facing": "up", "transition": "fade"},
        # The two gift-gated spurs (graph.ts pins both off II — the South region's
        # richest backtrack node). Inert until their target maps are authored; the
        # engine no-ops warps to unregistered maps (safe teases).
        {"id": "to_gullcry", "at": {"tx": 15, "ty": 12}, "trigger": "step_on",
         "to_map": "gullcry_rock", "to": {"tx": 4, "ty": 8}, "facing": "up",
         "requires_ability": "tidecall", "transition": "fade"},
        {"id": "to_tideglass", "at": {"tx": 2, "ty": 13}, "trigger": "interact",
         "to_map": "tideglass_cavern", "to": {"tx": 4, "ty": 8}, "facing": "left",
         "requires_ability": "glimmerstep", "transition": "door"},
    ],
    "triggers": [
        {"id": "sign_gullcry", "kind": "sign", "at": {"tx": sign_xy["sign_gullcry"][0], "ty": sign_xy["sign_gullcry"][1]},
         "activation": "interact", "ref": "sign.flats_gullcry"},
        {"id": "sign_cave", "kind": "sign", "at": {"tx": sign_xy["sign_cave"][0], "ty": sign_xy["sign_cave"][1]},
         "activation": "interact", "ref": "sign.flats_cave"},
        {"id": "sign_quay", "kind": "sign", "at": {"tx": sign_xy["sign_quay"][0], "ty": sign_xy["sign_quay"][1]},
         "activation": "interact", "ref": "sign.flats_to_quay"},
        # (The two route trainers are SIGHT-driven NPCs now — they stand beside
        # the lane and challenge the player who walks into their line.)
    ],
    # Level band ~8-10 (walkthrough §6): the bridge into Pearlmoor's 12. Brinelet/
    # Lumpin carry over from I; Brineroll (#27) is the flats' bigger tide-shape.
    "encounters": [
        {"id": "dune_a", "terrain": "tall_grass", "rect": {"tx": 2, "ty": 3, "w": 5, "h": 5},
         "encounter_rate": 0.10,
         "table": [{"kin_id": 26, "weight": 50, "min_level": 8, "max_level": 10},
                   {"kin_id": 31, "weight": 30, "min_level": 8, "max_level": 10},
                   {"kin_id": 27, "weight": 20, "min_level": 9, "max_level": 10}]},
        {"id": "dune_b", "terrain": "tall_grass", "rect": {"tx": 2, "ty": 11, "w": 4, "h": 5},
         "encounter_rate": 0.10,
         "table": [{"kin_id": 26, "weight": 50, "min_level": 8, "max_level": 10},
                   {"kin_id": 31, "weight": 30, "min_level": 8, "max_level": 10},
                   {"kin_id": 27, "weight": 20, "min_level": 9, "max_level": 10}]},
        {"id": "dune_c", "terrain": "tall_grass", "rect": {"tx": 2, "ty": 20, "w": 5, "h": 5},
         "encounter_rate": 0.10,
         "table": [{"kin_id": 26, "weight": 45, "min_level": 9, "max_level": 10},
                   {"kin_id": 31, "weight": 30, "min_level": 9, "max_level": 10},
                   {"kin_id": 27, "weight": 25, "min_level": 9, "max_level": 11}]},
        # The MANDATORY dune-grass crossing — the road to Pearlmoor runs through it.
        {"id": "dune_crossing", "terrain": "tall_grass", "rect": {"tx": 5, "ty": 16, "w": 9, "h": 2},
         "encounter_rate": 0.10,
         "table": [{"kin_id": 26, "weight": 45, "min_level": 9, "max_level": 11},
                   {"kin_id": 31, "weight": 30, "min_level": 9, "max_level": 11},
                   {"kin_id": 27, "weight": 25, "min_level": 9, "max_level": 11}]},
        {"id": "gullcry_shallows", "terrain": "water", "rect": {"tx": 14, "ty": 11, "w": 2, "h": 4},
         "encounter_rate": 0.06, "requires_ability": "tidecall",
         "table": [{"kin_id": 2, "weight": 100, "min_level": 9, "max_level": 11}]}],
    "npcs": [
        # Two travelling-Wayfarer SIGHT trainers (the route's XP bridge) — they
        # stand beside the lane, spot the player walking it, and challenge.
        # Beaten placements swap in once their flags set.
        {"id": "wayfarer_a", "at": {"tx": 5, "ty": 11}, "facing": "right", "sprite": "npc_shopkeeper",
         "movement": "static", "dialogue_ref": "script.flats_trainer_a",
         "sight_range": 4, "defeated_flag": "flag:flats_trainer_a_beaten",
         "hidden_when_flag": "flag:flats_trainer_a_beaten"},
        {"id": "wayfarer_a_after", "at": {"tx": 5, "ty": 11}, "facing": "right", "sprite": "npc_shopkeeper",
         "movement": "static", "dialogue_ref": "npc.flats_wayfarer_a",
         "requires_flag": "flag:flats_trainer_a_beaten"},
        {"id": "wayfarer_b", "at": {"tx": 12, "ty": 22}, "facing": "left", "sprite": "npc_shopkeeper",
         "movement": "static", "dialogue_ref": "script.flats_trainer_b",
         "sight_range": 4, "defeated_flag": "flag:flats_trainer_b_beaten",
         "hidden_when_flag": "flag:flats_trainer_b_beaten"},
        {"id": "wayfarer_b_after", "at": {"tx": 12, "ty": 22}, "facing": "left", "sprite": "npc_shopkeeper",
         "movement": "static", "dialogue_ref": "npc.flats_wayfarer_b",
         "requires_flag": "flag:flats_trainer_b_beaten"},
        {"id": "sky_watcher", "at": {"tx": 12, "ty": 18}, "facing": "up", "sprite": "npc_mentor",
         "movement": "look_around", "dialogue_ref": "npc.flats_sky_watcher"},
        # Item caches on the flats (interact -> pickup script -> vanish by flag).
        {"id": "cache_balm", "at": {"tx": 11, "ty": 9}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_flats_balm",
         "hidden_when_flag": "flag:picked_flats_balm"},
        {"id": "cache_lamp", "at": {"tx": 11, "ty": 19}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_flats_lamp",
         "hidden_when_flag": "flag:picked_flats_lamp"},
        # Loose wicks west of the lane (the cache-variety rule's money find —
        # ~half a route-trainer payout for poking about the flats).
        {"id": "cache_wicks", "at": {"tx": 9, "ty": 13}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_flats_wicks",
         "hidden_when_flag": "flag:picked_flats_wicks"}],
    "gates": [
        # The shallow finger to Gullcry opens with Tidecall — rect kept on PURE water
        # (an AbilityGate force-gates every tile it covers; see CLAUDE.md gotcha).
        {"id": "gullcry_gate", "ability": "tidecall", "effect": "make_passable",
         "rect": {"tx": 14, "ty": 11, "w": 2, "h": 4}}],
    "music": "assets/audio/music/dimglass-coast-a.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
