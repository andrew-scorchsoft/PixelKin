#!/usr/bin/env python3
"""
Sunkbell Shallows — the drowned shrine (walkthrough/02-east; Tidecall spur,
MISSABLE by design).

A small half-flooded shrine map off Saltreach Fen II: the silent verdigris
bell on its drowned arch, rare Tide kin circling the steps (low-weight zone),
and the pilgrims' dry-kept offerings (the cache payoff). Atmospheric, signed,
and reachable only by parted channel — the region's "you can already get
this" reward that pays Tidecall off immediately.

Run:  ./venv/bin/python tools/maps/build_sunkbell.py

audit_flow WAIVER — `loop` WARN accepted: a one-screen spur is a destination,
not a route (level-design §2a first-tier scale); the water plane crosses
freely under Tidecall anyway.
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 16
rng = random.Random(79)
owed: list[str] = []

tree = mk.make_grid(W, H)
water = mk.make_grid(W, H)
sand = mk.make_grid(W, H)

mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(6, 1, 2), (15, 2, 2), (18, 11, 2)], rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)

# the flooded floor: still black water wall to wall…
mk.rect(water, W, H, 1, 2, W - 2, H - 3)
# …broken by the entry shore, the shrine platform, and the offering isle
mk.rect(sand, W, H, 1, 6, 3, 9)              # the entry shore (the warp toe)
mk.blob(sand, W, H, 10.0, 7.0, 3.4, 2.4)     # the shrine platform
mk.blob(sand, W, H, 15.5, 11.5, 1.8, 1.2)    # the offering isle (SE)
mk.blob(sand, W, H, 5.5, 12.5, 1.6, 1.2)     # a drowned-step stone (SW)

# entry opening west (exactly the two warp rows)
for y in (7, 8):
    tree[y * W + 0] = 0
    tree[y * W + 1] = 0

for i in range(W * H):
    if sand[i]:
        water[i] = 0
    if tree[i]:
        water[i] = 0
        sand[i] = 0

terrain_layers = [
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]

gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]

deco = mk.make_grid(W, H)
# lantern-buoys ringing the bell's reflection; drowned-step boulders
for (x, y) in [(6, 4), (14, 5), (13, 11), (4, 10)]:
    deco[y * W + x] = gid("buoy")
for (x, y) in [(8, 9), (12, 8), (5, 12)]:
    deco[y * W + x] = gid("boulder")

m: dict = {
    "id": "sunkbell_shallows", "display_name": "Sunkbell Shallows",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "warps": [
        # west, back across the channel to Fen II (lands ON its outcrop warps)
        {"id": "to_fen_ii", "at": {"tx": 0, "ty": 7}, "trigger": "step_on",
         "to_map": "saltreach_fen_ii", "to": {"tx": 31, "ty": 14}, "facing": "left",
         "transition": "fade"},
        {"id": "to_fen_ii_s", "at": {"tx": 0, "ty": 8}, "trigger": "step_on",
         "to_map": "saltreach_fen_ii", "to": {"tx": 31, "ty": 15}, "facing": "left",
         "transition": "fade"},
    ],
    # the drowned shrine itself — the bell hangs over the platform's crown
    "objects": [
        {"id": "bell_shrine", "sprite": "sunkbell_shrine",
         "at": {"tx": 9, "ty": 4}, "w": 3, "h": 3, "overhang": 1},
    ],
    "triggers": [
        # reading the bell up close (the platform's south face)
        {"id": "bell_read", "kind": "sign", "at": {"tx": 10, "ty": 6},
         "activation": "interact", "ref": "sign.sunkbell_bell"},
    ],
    "npcs": [],
    "gates": [],
    # the rare-Tide bed: low weight, low rate (hooks §6 — spur ~0.08), with
    # the spur's prize at the bottom of the table (Shimmral, a young Tidalarch)
    "encounters": [
        {"id": "shallows", "terrain": "water", "rect": {"tx": 2, "ty": 3, "w": 16, "h": 11},
         "encounter_rate": 0.08, "requires_ability": "tidecall",
         "table": [{"kin_id": 27, "weight": 35, "min_level": 17, "max_level": 19},
                   {"kin_id": 31, "weight": 30, "min_level": 17, "max_level": 19},
                   {"kin_id": 24, "weight": 20, "min_level": 18, "max_level": 20},
                   {"kin_id": 61, "weight": 15, "min_level": 19, "max_level": 20}]},
    ],
    "music": "assets/audio/music/saltreach-fen-c.mp3",
}

# entry sign + the two dry-kept caches (the atlas §3 reward)
owed += pt.sign(m, deco, W, sid="sunkbell_shrine", at=(2, 6))
owed += pt.cache(m, cid="sunkbell_charges", at=(11, 7))
owed += pt.cache(m, cid="sunkbell_balm", at=(15, 12))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

mk.scatter_decor(deco, base, W, H, rng, density=0.10,
                 avoid={(x, y) for y in range(H) for x in range(W)
                        if water[y * W + x] or sand[y * W + x] or tree[y * W + x]})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
