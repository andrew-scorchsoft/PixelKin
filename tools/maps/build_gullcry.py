#!/usr/bin/env python3
"""
Gullcry Rock — the Tidecall spur off Dimglass Coast II (graph.ts `gullcry_rock`).

The South region's signature "the map reopened" payoff (walkthrough/01-south):
a wave-bitten sea-stack past the buoy line, reachable only once Tidecall is
earned at Pearlmoor. Short and rewarding — the rare harbour-light kin
(#29 Glostern) drifts in the surrounding shallows, and the TIDE CHARM (the
South's best lamp) is lashed to the high stone.

Arrival: the dimglass_coast_ii `to_gullcry` warp lands the player on the south
beach at (4,8); stepping back south returns to the flats' shallows.

Run:  python3 tools/maps/build_gullcry.py
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 16, 13
rng = random.Random(43)

# ---- terrain: open sea, one wave-bitten islet, a rock crown ---------------------
water = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 0, W - 1, H - 1)                  # sea everywhere…

sand = mk.make_grid(W, H)
mk.blob(sand, W, H, 7.0, 5.5, 4.6, 3.4)                   # …the islet body
mk.blob(sand, W, H, 4.0, 8.0, 1.8, 1.4)                   # south landing tongue
mk.blob(sand, W, H, 10.5, 8.5, 1.6, 1.2)                  # east spit
for y in range(H):                                        # carve the sea from under it
    for x in range(W):
        if sand[y * W + x]:
            water[y * W + x] = 0

# (the "high stone" crown is a boulder cluster on the deco pass below — a
# free-standing cliff mass mid-islet reads as a wall slab, not an outcrop)

# ---- base + layers ----------------------------------------------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

# ---- deco: buoys, boulders, the nesting ledges -------------------------------------
deco = mk.make_grid(W, H)
# the buoy line the player followed out — arriving FROM the southwest
for (x, y) in [(2, 11), (1, 9), (3, 12), (13, 2), (14, 6), (12, 11)]:
    deco[y * W + x] = gid("buoy")
# the HIGH STONE: a tight 2x2 boulder crown at the islet's heart — the charm
# cache sits at its southern foot
for (x, y) in [(7, 4), (8, 4), (7, 5), (8, 5)]:
    deco[y * W + x] = gid("boulder")
# wave-worn boulders on the islet skirts (the gulls' perches)
for (x, y) in [(3, 6), (11, 4), (10, 8)]:
    deco[y * W + x] = gid("boulder")
sign_xy = (5, 8)                                          # by the landing tongue
deco[sign_xy[1] * W + sign_xy[0]] = gid("sign")

objects = []   # a bare sea-stack: no trees out here, just stone, spray and lamps

# ---- assemble ------------------------------------------------------------------------
m = {
    "id": "gullcry_rock", "display_name": "Gullcry Rock", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # back to the flats' shallow finger (the player swam in; they have Tidecall)
        {"id": "to_flats", "at": {"tx": 4, "ty": 9}, "trigger": "step_on",
         "to_map": "dimglass_coast_ii", "to": {"tx": 15, "ty": 13}, "facing": "down",
         "transition": "fade"},
    ],
    "triggers": [
        {"id": "sign_gullcry", "kind": "sign", "at": {"tx": sign_xy[0], "ty": sign_xy[1]},
         "activation": "interact", "ref": "sign.gullcry_rock"},
    ],
    # The reward shallows: the rare harbour-light kin drifts here. Tidecall-gated
    # water ring (the player must hold it to BE here at all).
    "encounters": [
        {"id": "gullcry_surf", "terrain": "water", "rect": {"tx": 0, "ty": 0, "w": 16, "h": 13},
         "encounter_rate": 0.09, "requires_ability": "tidecall",
         "table": [{"kin_id": 29, "weight": 40, "min_level": 11, "max_level": 13},
                   {"kin_id": 27, "weight": 30, "min_level": 11, "max_level": 13},
                   {"kin_id": 31, "weight": 30, "min_level": 10, "max_level": 12}]},
    ],
    "npcs": [
        # THE prize: the Tide Charm, lashed to the foot of the rock crown.
        {"id": "charm_cache", "at": {"tx": 8, "ty": 6}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_gullcry_charm",
         "hidden_when_flag": "flag:picked_gullcry_charm"},
    ],
    # Gates are emitted below as PURE-WATER row runs: make_passable force-gates
    # every tile its rect covers (the CLAUDE.md gotcha) — one big rect would let a
    # Tidecall-holder walk up the rock crown.
    "gates": [],
    "music": "assets/audio/music/dimglass-coast-a.mp3",
}

gi = 0
for y in range(H):
    x = 0
    while x < W:
        if water[y * W + x]:
            x0 = x
            while x < W and water[y * W + x]:
                x += 1
            m["gates"].append({"id": f"surf_gate_{gi}", "ability": "tidecall",
                               "effect": "make_passable",
                               "rect": {"tx": x0, "ty": y, "w": x - x0, "h": 1}})
            gi += 1
        else:
            x += 1

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
