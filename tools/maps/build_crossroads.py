#!/usr/bin/env python3
"""
Vesper Crossroads — the Lanternway hub (graph.ts `vesper_crossroads`, kind `hub`).

Where every lit road in Vesperholm meets (walkthrough/01-south: discovered from
Pearlmoor as South's fast-travel anchor; its inward Spire road stays `[LATER]`,
flag:hub_unlocked). A safe, warm clearing — no encounters: four roads meeting at
a lamplit plaza around the Waystone, deep forest enclosure, one cliff accent.

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
                  bumps=[(4, 3, 2), (15, 2, 2), (2, 12, 2), (17, 13, 2), (8, 1, 1)])
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)              # bottom border too
mk.blob(tree, W, H, 5, 15, 2.0, 1.4)
mk.blob(tree, W, H, 14, 15, 2.0, 1.4)

# the clearing's accent: a small still pool in the NE quadrant (the pond family —
# water-over-grass foam edge), where wayfarers water their kin
pond = mk.make_grid(W, H)
mk.blob(pond, W, H, 15.5, 4.5, 1.8, 1.3)
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
# punch the borders where the roads leave
for y in (CY - 1, CY):
    tree[y * W + 0] = 0; tree[y * W + 1] = 0
    tree[y * W + (W - 1)] = 0; tree[y * W + (W - 2)] = 0
for x in (CX, CX + 1):
    tree[0 * W + x] = 0; tree[1 * W + x] = 0
    tree[(H - 1) * W + x] = 0; tree[(H - 2) * W + x] = 0

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
        {"id": "to_pearlmoor", "at": {"tx": W - 1, "ty": CY}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 1, "ty": 12}, "facing": "right", "transition": "fade"},
        {"id": "to_pearlmoor_n", "at": {"tx": W - 1, "ty": CY - 1}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 1, "ty": 12}, "facing": "right", "transition": "fade"},
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
    ],
    "triggers": [
        {"id": "sign_waystone", "kind": "sign",
         "at": {"tx": sign_tiles["sign_waystone"][0], "ty": sign_tiles["sign_waystone"][1]},
         "activation": "interact", "ref": "sign.crossroads"},
        {"id": "sign_spire", "kind": "sign",
         "at": {"tx": sign_tiles["sign_spire"][0], "ty": sign_tiles["sign_spire"][1]},
         "activation": "interact", "ref": "sign.crossroads_spire"},
    ],
    "encounters": [],   # the hub is safe ground — a breath between roads
    "npcs": [
        # the Waykeeper tends the plaza lamps; stands just off the Waystone
        {"id": "waykeeper", "at": {"tx": CX - 1, "ty": CY - 1}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "look_around",
         "dialogue_ref": "npc.lanternway_keeper"},
    ],
    "gates": [],
    "music": "assets/audio/music/tinderwick-a.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
