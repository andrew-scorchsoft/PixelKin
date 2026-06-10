#!/usr/bin/env python3
"""
Build Dimglass Coast — the first route — on the SHARED overworld set.

Replaces the old flat-kit map (which FAILED the quality gate: no autotile vocabulary,
blocky fills) with a proper autotiled coastal route per level-design §7.3: an 18×34
vertical tidal shelf travelled south→north, cliff wall to the WEST, sea to the EAST,
a continuous lit path spine (the safe lane), alternating tall-grass patches, a sand
rest pocket, lantern-buoys teasing Tidecall offshore, and a cave mouth in the cliff
teasing Glimmerstep — each signed. Variant autotiling + scatter decor for polish.

Run:  python3 tools/maps/build_dimglass.py   (after build_shared_overworld.py)
"""
from __future__ import annotations
import json, random
import mapkit as mk
from mapkit import gid

W, H = 18, 34
rng = random.Random(19)

# ---- terrain presence grids -------------------------------------------------
# Composition per level-design §11: the west cliff is a real WALL (2-3 deep with
# organic bumps — its lit-rim/face/seam edges carry the height read), the east
# shore is a wavy tideline, and the grass beats are shaped patches, not rects.
cliff = mk.make_grid(W, H)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)                 # west cliff wall (continues off-west)
mk.rect(cliff, W, H, 0, 0, W - 1, 1)                 # north cliff band
mk.rect(cliff, W, H, 0, H - 2, W - 1, H - 1)         # south cliff band
for (bx, by, br) in [(2, 4, 1), (2, 14, 2), (2, 21, 1), (2, 28, 1), (3, 9, 1)]:
    mk.blob(cliff, W, H, bx, by, br + 0.4, br)       # the wall bulges into the shelf
for x in range(6, 9):                                # north exit gap
    cliff[0 * W + x] = 0; cliff[1 * W + x] = 0
for x in range(5, 9):                                # south entry gap (land-in from Tinderwick)
    cliff[(H - 1) * W + x] = 0; cliff[(H - 2) * W + x] = 0

water = mk.make_grid(W, H)
mk.rect(water, W, H, 14, 2, W - 1, H - 3)            # sea along the east (continues off-east)
mk.blob(water, W, H, 14, 9, 1.6, 2.0)                # the tide bites into the beach…
mk.blob(water, W, H, 14, 24, 1.6, 1.6)
sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 12, 2, 13, H - 3)               # beach band meeting the sea
mk.blob(sand, W, H, 12, 16, 1.6, 2.2)               # …and the dunes bite back
mk.rect(sand, W, H, 9, 26, 13, 29)                  # widened sand rest pocket before the boundary

# alternating tall-grass beats (encounter patches) — shaped blobs beside the lane
tallgrass = mk.make_grid(W, H)
for (cx, cy, rx, ry) in [(4.5, 6.5, 2.4, 2.2), (9.5, 13.5, 2.4, 2.2),
                         (5.5, 18.5, 2.4, 2.2), (9.5, 23.5, 2.4, 2.2)]:
    mk.blob(tallgrass, W, H, cx, cy, rx, ry)

# MANDATORY crossings (level-design §11 rule 7 / the classic route convention):
# two grass bands span the whole walkable corridor — tallgrass on the green,
# DUNEGRASS over the beach band — so the road north passes THROUGH encounter
# ground, not beside it. The lit lane is carved out at these rows below.
dunegrass = mk.make_grid(W, H)
CROSSINGS = [(9, 10), (26, 27)]
for (y0, y1) in CROSSINGS:
    for y in range(y0, y1 + 1):
        for x in range(3, 12):
            tallgrass[y * W + x] = 1
        for x in range(12, 14):
            dunegrass[y * W + x] = 1

# the lit path spine — interrupted at each crossing (the grass spans the road)
path = mk.make_grid(W, H)
spine = [6, 6, 6, 7, 7, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 8, 8, 7, 7, 6]

def spine_col(ty):
    return spine[min(ty - 2, len(spine) - 1)]

crossing_rows = {y for (y0, y1) in CROSSINGS for y in range(y0, y1 + 1)}
for ty in range(2, H - 2):
    if ty in crossing_rows:
        continue
    cx = spine_col(ty)
    path[ty * W + cx] = 1; path[ty * W + cx + 1] = 1
for x in range(6, 9):                                 # connect spine to both gaps
    path[2 * W + x] = 1; path[(H - 3) * W + x] = 1

# cave mouth recess in the west cliff (Glimmerstep tease) — carve grass, place dark rock
cave_xy = (2, 10)

# ---- base + terrain layers --------------------------------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    # dunegrass expands AFTER sand so the crossing's tufts sit ON the beach band
    {"name": "t_dunegrass", "role": "terrain", "terrain": "dunegrass",
     "set": "vesper_overworld_set", "depth": 0, "data": dunegrass},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

# ---- objects: canopy trees for walk-under depth (crowns break the hedge read) --
objects = [
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 10, "ty": 6}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 3, "ty": 23}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 2, "ty": 11}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_d", "sprite": "tinderwick_tree", "at": {"tx": 11, "ty": 18}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    # Lamp breadcrumbs are the 1x3 lamp-post OBJECT (art-style 14b: a one-tile lamp is
    # wrong) — trunks stand just BESIDE the lit lane, never on it.
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 7, "ty": 6}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 8, "ty": 14}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 7, "ty": 19}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_d", "sprite": "tinderwick_lamp_post", "at": {"tx": 11, "ty": 24}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (cliff, water, sand, tallgrass, dunegrass, path))}
avoid = covered | building_cells

# ---- deco: cave, signs, buoys, lamps, scatter -------------------------------
# Signs and lamps must sit IMMEDIATELY BESIDE the lit spine the player walks (never
# floating mid-field). The spine occupies cols (cx, cx+1) per row; we drop props on
# the tile one column to the LEFT of the spine (cx-1) at chosen rows.
deco = mk.make_grid(W, H)
for (x, y) in [cave_xy, (cave_xy[0], cave_xy[1] + 1)]:    # dark cave recess
    deco[y * W + x] = gid("cliff_fill")
# lantern-buoys OFFSHORE in the sea (east) — a LINE arcing out toward Gullcry Rock,
# so the Tidecall tease reads as a route, not random floats:
for (x, y) in [(14, 5), (15, 6), (16, 7), (15, 13), (16, 14), (15, 20), (16, 27)]:
    deco[y * W + x] = gid("buoy")
# shore boulders + a rock choke at each story beat (the spine narrows to ONE tile
# at Wren and at the night-sky beat so the cutscene tile can't be walked around):
for (x, y) in [(12, 4), (13, 11), (12, 22), (3, 15), (10, 11), (9, 28)]:
    deco[y * W + x] = gid("boulder")

def beside_spine(ty, side=-1):
    """A walkable grass tile just off the spine at row ty (side -1 = left, +2 = right)."""
    cx = spine_col(ty)
    return (cx + (-1 if side < 0 else 2), ty)

# signs keyed to refs, each placed beside the spine at its row:
sign_rows = {
    "sign_buoys": (7, +2),      # right of the spine, facing the offshore buoys
    "sign_cave": (11, -1),      # left of the spine, by the cliff cave mouth (row 10 is the crossing)
    "sign_route": (16, -1),     # left of the spine, mid-route
    "sign_boundary": (29, -1),  # left of the spine, by the north boundary
}
sign_xy = {}
for k, (ty, side) in sign_rows.items():
    x, y = beside_spine(ty, side)
    sign_xy[k] = (x, y)
    deco[y * W + x] = gid("sign")
# Scatter decor ONLY beside the lit lane (within 2 tiles of a path cell), so the open
# field stays clean and the eye follows the lamps — not random tufts mid-meadow.
near_path = set()
for y in range(H):
    for x in range(W):
        if path[y * W + x]:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    near_path.add((x + dx, y + dy))
scatter_avoid = avoid | {(x, y) for y in range(H) for x in range(W) if (x, y) not in near_path}
mk.scatter_decor(deco, base, W, H, rng, density=0.12, avoid=scatter_avoid)

# ---- assemble ---------------------------------------------------------------
m = {
    "id": "dimglass_coast", "display_name": "Dimglass Coast", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # South entry gap is 4 tiles wide -> a warp on EVERY tile, each landing ON
        # one of Tinderwick's two exit warps (audit_warps.py conventions).
        {"id": "from_tinderwick_a", "at": {"tx": 5, "ty": 33}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 13, "ty": 0}, "facing": "down", "transition": "fade"},
        {"id": "from_tinderwick_b", "at": {"tx": 6, "ty": 33}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 13, "ty": 0}, "facing": "down", "transition": "fade"},
        {"id": "from_tinderwick_c", "at": {"tx": 7, "ty": 33}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 14, "ty": 0}, "facing": "down", "transition": "fade"},
        {"id": "from_tinderwick_d", "at": {"tx": 8, "ty": 33}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": 14, "ty": 0}, "facing": "down", "transition": "fade"},
        # North exit continues onto the tidal flats of Dimglass Coast II (the canon
        # segment chain: I -> II -> Pearlmoor); 3-wide gap, 3 warps.
        {"id": "to_coast_ii_w", "at": {"tx": 6, "ty": 0}, "trigger": "step_on",
         "to_map": "dimglass_coast_ii", "to": {"tx": 6, "ty": 31}, "facing": "up", "transition": "fade"},
        {"id": "to_coast_ii", "at": {"tx": 7, "ty": 0}, "trigger": "step_on",
         "to_map": "dimglass_coast_ii", "to": {"tx": 7, "ty": 31}, "facing": "up", "transition": "fade"},
        {"id": "to_coast_ii_e", "at": {"tx": 8, "ty": 0}, "trigger": "step_on",
         "to_map": "dimglass_coast_ii", "to": {"tx": 8, "ty": 31}, "facing": "up", "transition": "fade"},
        {"id": "to_tideglass", "at": {"tx": 2, "ty": 10}, "trigger": "interact",
         "to_map": "tideglass_cavern", "to": {"tx": 5, "ty": 8}, "facing": "left",
         "requires_ability": "glimmerstep", "transition": "door"},
    ],
    "triggers": [
        {"id": "sign_buoys", "kind": "sign", "at": {"tx": sign_xy["sign_buoys"][0], "ty": sign_xy["sign_buoys"][1]},
         "activation": "interact", "ref": "sign.dimglass_buoys"},
        {"id": "sign_cave", "kind": "sign", "at": {"tx": sign_xy["sign_cave"][0], "ty": sign_xy["sign_cave"][1]},
         "activation": "interact", "ref": "sign.dimglass_cave"},
        {"id": "sign_route", "kind": "sign", "at": {"tx": sign_xy["sign_route"][0], "ty": sign_xy["sign_route"][1]},
         "activation": "interact", "ref": "sign.dimglass_route"},
        {"id": "sign_boundary", "kind": "sign", "at": {"tx": sign_xy["sign_boundary"][0], "ty": sign_xy["sign_boundary"][1]},
         "activation": "interact", "ref": "sign.dimglass_to_pearlmoor"},
        # (A2 — Wren's friendly battle is now SIGHT-driven: Wren stands beside the
        # lane with sight_range and challenges the player who walks into view.)
        # B1 — the inciting incident: a far constellation winks out on first nightfall
        # here. Quiet, not loud. Spine choked by the boulder at (9,28).
        {"id": "dusk_begins", "kind": "cutscene", "at": {"tx": 8, "ty": 28},
         "activation": "step_on", "ref": "script.dusk_begins", "once": True,
         "sets_flags": ["flag:dusk_begins"]},
    ],
    # A Tide coast (walkthrough/01-south): wild kin are Tide/Light, not Ember. Common
    # #26 Brinelet (Tide); #31 Lumpin (Tide/Light); #8 Glimflit (Light, drifted from town).
    # Level band 3-6. The Tidecall-gated shallows keep the #2 Brinix rare-read.
    # Four grass beats ramping 3-5 -> 4-6 down the route (walkthrough band 3-6, §4
    # "5 -> ~8"): the player who fights the beats arrives at II around level 7.
    "encounters": [
        {"id": "grass_a", "terrain": "tall_grass", "rect": {"tx": 2, "ty": 4, "w": 5, "h": 5},
         "encounter_rate": 0.09,
         "table": [{"kin_id": 26, "weight": 55, "min_level": 3, "max_level": 5},
                   {"kin_id": 31, "weight": 30, "min_level": 3, "max_level": 5},
                   {"kin_id": 8, "weight": 15, "min_level": 3, "max_level": 5}]},
        {"id": "grass_b", "terrain": "tall_grass", "rect": {"tx": 7, "ty": 11, "w": 5, "h": 5},
         "encounter_rate": 0.09,
         "table": [{"kin_id": 26, "weight": 55, "min_level": 3, "max_level": 6},
                   {"kin_id": 31, "weight": 30, "min_level": 4, "max_level": 6},
                   {"kin_id": 8, "weight": 15, "min_level": 3, "max_level": 5}]},
        {"id": "grass_c", "terrain": "tall_grass", "rect": {"tx": 3, "ty": 16, "w": 5, "h": 5},
         "encounter_rate": 0.09,
         "table": [{"kin_id": 26, "weight": 55, "min_level": 4, "max_level": 6},
                   {"kin_id": 31, "weight": 30, "min_level": 4, "max_level": 6},
                   {"kin_id": 8, "weight": 15, "min_level": 4, "max_level": 6}]},
        {"id": "grass_d", "terrain": "tall_grass", "rect": {"tx": 7, "ty": 21, "w": 5, "h": 5},
         "encounter_rate": 0.09,
         "table": [{"kin_id": 26, "weight": 55, "min_level": 4, "max_level": 6},
                   {"kin_id": 31, "weight": 30, "min_level": 4, "max_level": 6},
                   {"kin_id": 8, "weight": 15, "min_level": 4, "max_level": 6}]},
        # The two MANDATORY crossings — the road north passes through these bands
        # (tallgrass + dunegrass over the beach), so every traveller rolls a few
        # encounters; the optional patches beside the lane stay the grind spots.
        {"id": "crossing_a", "terrain": "tall_grass", "rect": {"tx": 3, "ty": 9, "w": 11, "h": 2},
         "encounter_rate": 0.10,
         "table": [{"kin_id": 26, "weight": 55, "min_level": 3, "max_level": 5},
                   {"kin_id": 31, "weight": 30, "min_level": 3, "max_level": 5},
                   {"kin_id": 8, "weight": 15, "min_level": 3, "max_level": 5}]},
        {"id": "crossing_b", "terrain": "tall_grass", "rect": {"tx": 3, "ty": 26, "w": 11, "h": 2},
         "encounter_rate": 0.10,
         "table": [{"kin_id": 26, "weight": 55, "min_level": 4, "max_level": 6},
                   {"kin_id": 31, "weight": 30, "min_level": 4, "max_level": 6},
                   {"kin_id": 8, "weight": 15, "min_level": 4, "max_level": 6}]},
        {"id": "tide_shallows", "terrain": "water", "rect": {"tx": 14, "ty": 5, "w": 2, "h": 4},
         "encounter_rate": 0.06, "requires_ability": "tidecall",
         "table": [{"kin_id": 2, "weight": 100, "min_level": 4, "max_level": 6}]}],
    "npcs": [
        # The rival Wren (A2): a SIGHT trainer — waits beside the lane and challenges
        # the player who walks into view (the classic "they see you coming" hook).
        # The beaten placement swaps in once the friendly battle is done.
        {"id": "wren", "at": {"tx": 5, "ty": 11}, "facing": "right", "sprite": "wren",
         "movement": "static", "dialogue_ref": "script.wren_dimglass",
         "sight_range": 4, "defeated_flag": "flag:wren_dimglass_battled",
         "hidden_when_flag": "flag:wren_dimglass_battled"},
        {"id": "wren_after", "at": {"tx": 5, "ty": 11}, "facing": "right", "sprite": "wren",
         "movement": "static", "dialogue_ref": "npc.dimglass_wayfarer",
         "requires_flag": "flag:wren_dimglass_battled"},
        # B1 witness — the old lamplighter appears near the beat once dusk_begins has
        # fired. He KEEPS THE BEACON'S WICK-KEY (the Tinderwick ascent quest): his
        # first talk hands it over, then the plain witness placement swaps in.
        {"id": "witness", "at": {"tx": 10, "ty": 29}, "facing": "up",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.give_wick", "requires_flag": "flag:dusk_begins",
         "hidden_when_flag": "flag:has_beacon_wick"},
        {"id": "witness_after", "at": {"tx": 10, "ty": 29}, "facing": "up",
         "sprite": "npc_shopkeeper", "movement": "look_around",
         "dialogue_ref": "npc.dimglass_witness", "requires_flag": "flag:has_beacon_wick"},
        # Route item caches (sprite 'item_cache'): interact runs the pickup script,
        # then hidden_when_flag removes the bundle — the classic ground item.
        {"id": "cache_balm", "at": {"tx": beside_spine(18, +2)[0], "ty": 18}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_dimglass_balm",
         "hidden_when_flag": "flag:picked_dimglass_balm"},
        {"id": "cache_lamps", "at": {"tx": beside_spine(24, -1)[0], "ty": 24}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_dimglass_lamps",
         "hidden_when_flag": "flag:picked_dimglass_lamps"}],
    "gates": [
        {"id": "tide_gate", "ability": "tidecall", "effect": "make_passable",
         "rect": {"tx": 14, "ty": 5, "w": 2, "h": 4}}],
    "music": "assets/audio/music/dimglass-coast-a.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
