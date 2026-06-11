#!/usr/bin/env python3
"""
Spore Grotto — the Glowmoss complex's deep spur (atlas §3: rare Verdant kin +
item; Glimmerstep). A small fungal pocket OFF Glowmoss Deep B1F — the §3a
braided-reward payoff for descending the ladder and finding the notch: the
Sporeling line's middle stage is common here, the grotto keeps the region's
big valuable in a dead end, and the very patient may meet a MYCELARCH — the
line's shadowed apex, nowhere else wild this early.

Run:  ./venv/bin/python tools/maps/build_spore_grotto.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 18, 14
rng = random.Random(73)
owed: list[str] = []

ENTRY = (5, 8)        # B1F's to_grotto lands here
RETURN_DOOR = (5, 9)  # the notch back (interact; landing beside B1F's mouth)
CACHE_AT = (15, 3)    # the dead end's prize

# ---- terrain: a fungal pocket carved from rock ----------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.blob(floor, W, H, 5.0, 7.5, 3.0, 2.6)               # entry chamber
mk.hline(floor, W, H, 6, 8, 10)                        # the winding passage east
mk.blob(floor, W, H, 12.5, 7.0, 3.4, 3.2)              # the SPORE BED chamber
mk.vline(floor, W, H, 14, 3, 4)                        # branch north...
mk.hline(floor, W, H, 3, 14, 16)                       # ...to the dead end (the prize)
for i in range(W * H):
    if floor[i]:
        wall[i] = 0

# the spore bed — the whole chamber floor blooms (the rare table lives here)
glow = mk.make_grid(W, H)
mk.blob(glow, W, H, 12.5, 7.5, 2.6, 2.4)
for i in range(W * H):
    if glow[i] and not floor[i]:
        glow[i] = 0

terrain_layers = [
    {"name": "t_glowmoss", "role": "terrain", "terrain": "glowmoss",
     "set": "vesper_overworld_set", "depth": 0, "data": glow},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]

deco = mk.make_grid(W, H)
# shroom-light: the entry breadcrumb and the bed's glow
for (x, y, n) in [(7, 6, "glowshroom_a"), (4, 5, "glowshroom_b"), (11, 9, "glowshroom_a"),
                  (15, 5, "glowshroom_b")]:
    deco[y * W + x] = gid(n)
for (x, y) in [(3, 9), (13, 4)]:
    deco[y * W + x] = gid("boulder")
for (x, y) in [(6, 9), (10, 6), (16, 4)]:
    deco[y * W + x] = gid("g_pebble")
# the notch back to B1F (a dark recess in the entry chamber's south wall)
deco[RETURN_DOOR[1] * W + RETURN_DOOR[0]] = gid("cavewall_fill")

m: dict = {
    "id": "spore_grotto", "display_name": "Spore Grotto", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "warps": [
        # the notch back to Glowmoss Deep B1F (lands beside its grotto mouth)
        {"id": "to_b1f", "at": {"tx": RETURN_DOOR[0], "ty": RETURN_DOOR[1]},
         "trigger": "interact", "to_map": "glowmoss_deep_b1f", "to": {"tx": 6, "ty": 17},
         "facing": "up", "transition": "door"},
    ],
    "npcs": [],
    "gates": [],
    "encounters": [],
    "triggers": [],
    "objects": [
        # the grotto's heart: the ember-capped huddle over the bed
        {"id": "shrooms_heart", "sprite": "glowmoss_deep_glowshrooms_ember",
         "at": {"tx": 11, "ty": 5}, "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    ],
    "music": "assets/audio/music/lowleaf-hollow-c.mp3",
}

# the prize at the dead end (§3a rule 4: a detour ALWAYS pays — this one big)
owed += pt.cache(m, cid="grotto_starglass", at=CACHE_AT)
# a lore sign at the bed's edge
owed += pt.sign(m, deco, W, sid="spore_grotto", at=(9, 7))

# the spore bed's table: Sporemid common AT LAST, and the line's shadowed apex
# as the very-rare prize (band 21-23; Mycelarch is wild nowhere else this early)
GROTTO_TABLE = [
    {"kin_id": 57, "weight": 40, "min_level": 21, "max_level": 23},  # Sporemid
    {"kin_id": 56, "weight": 30, "min_level": 21, "max_level": 23},  # Sporeling
    {"kin_id": 67, "weight": 22, "min_level": 22, "max_level": 23},  # Fennlight
    {"kin_id": 58, "weight": 8, "min_level": 22, "max_level": 23},   # MYCELARCH — the prize
]
m["encounters"] = pt.zones_from_grid(glow, W, H, terrain="tall_grass",
                                     rate=0.12, table=GROTTO_TABLE, id_prefix="spore")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
