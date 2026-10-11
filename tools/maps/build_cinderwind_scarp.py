#!/usr/bin/env python3
"""
Cinderwind Scarp — the climb out of the mine (graph.ts `cinderwind_scarp`,
kind route, region north, band 28-31). NEW in the 2026-10 geometry fix.

Why it exists: Cinderhead Deep used to open straight onto Galehigh Terraces —
a cave mouth and then a town, with no road in between, and a level dead zone
(the Deep tops out at 27; Galehigh's wilds start at 28 and Mira's ace is 34).
This is the missing leg: you come up out of the Deep's east mouth into the
wind, and climb a scree-and-grass scarp in three ledged tiers to the terraces'
west gate. It reads as the seam between two regions — ore-carts and crystal
spoil at the foot (Cinderhead's), kite-poles and a wind cairn at the top
(Galehigh's) — so arriving at the terraces feels earned.

  * the FOOT (rows 18-25): the mine's spoil — ore carts, crystal clusters, a
    mandatory grass strip across the lower road;
  * the MIDDLE TIER (rows 10-15): the ore-hauler keeps the turn; a second strip;
  * the TOP TIER (rows 2-7): the kite-runner, the kite poles, the wind cairn —
    the terraces' gate in sight.
Two cliff bands separate the tiers; each carries a one-way ledge back DOWN
(§3a r1 — the return is shorter than the climb).

Wild kin (lv 28-31, closing the Deep->Galehigh gap): Rubbol, Galefox,
Thrumble, Lumecite, Nimbruff, rare Voltcrag. Four of them (Rubbol, Galefox,
Lumecite, Nimbruff) were in no wild table before this road.

HANDSHAKE: cinderhead_deep `to_terraces`/`_s` at (27,12)/(27,13) land here at
(1,20)/(1,21); our `to_deep`/`_s` at (0,20)/(0,21) land at the deep's
(26,12)/(26,13). Our `to_terraces`/`_n` at (23,4)/(23,5) land on Galehigh's
west gate (1,14)/(1,15); Galehigh's `to_cinderhead`/`_s` land at our
(22,4)/(22,5).

Run:  python3 tools/maps/build_cinderwind_scarp.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 28
rng = random.Random(173)
owed: list[str] = []

tree = mk.make_grid(W, H)
cliff = mk.make_grid(W, H)
path = mk.make_grid(W, H)
tallgrass = mk.make_grid(W, H)
deco = mk.make_grid(W, H)

# enclosure: wooded crest N + S, crag flanks W (the mine's rock) / E (the terrace wall)
mk.organic_border(tree, W, H, top=1, depth=2, bumps=[(6, 1, 2), (15, 1, 1)], rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)
mk.organic_border(cliff, W, H, left=1, right=1, depth=2,
                  bumps=[(1, 6, 2), (22, 12, 2), (1, 15, 1), (22, 21, 2)], rng=rng)
for y in (20, 21):                     # WEST gap: the Deep's east mouth (low)
    for x in (0, 1, 2):
        cliff[y * W + x] = 0
for y in (4, 5):                       # EAST gap: Galehigh's west gate (high)
    for x in (W - 3, W - 2, W - 1):
        cliff[y * W + x] = 0

# the two tier bands, each with the lane's gap + a ledge segment
for y in (16, 17):
    mk.hline(cliff, W, H, y, 2, W - 3)
for y in (8, 9):
    mk.hline(cliff, W, H, y, 2, W - 3)
for x in (8, 9):                        # band A gap (the lane climbs)
    cliff[16 * W + x] = cliff[17 * W + x] = 0
for x in (17, 18):                      # band B gap
    cliff[8 * W + x] = cliff[9 * W + x] = 0
for x in range(13, 17):                 # band A ledge (hop back down)
    cliff[16 * W + x] = cliff[17 * W + x] = 0
for x in range(3, 7):                   # band B ledge
    cliff[8 * W + x] = cliff[9 * W + x] = 0

# the lane (a worn path the whole way — this is still lamp-country)
LANE = set()
for x in range(0, 10):
    LANE |= {(x, 20), (x, 21)}          # L1 in from the mine mouth
for y in range(12, 22):
    LANE |= {(8, y), (9, y)}            # L2 up through band A's gap
for x in range(8, 19):
    LANE |= {(x, 12), (x, 13)}          # L3 east along the middle tier
for y in range(4, 14):
    LANE |= {(17, y), (18, y)}          # L4 up through band B's gap
for x in range(17, W):
    LANE |= {(x, 4), (x, 5)}            # L5 out to the terraces' gate
for (x, y) in LANE:
    path[y * W + x] = 1

# mandatory grass strips (full tier height, the road pauses through them)
for y in range(18, 26):
    for x in (4, 5, 6):
        tallgrass[y * W + x] = 1
for y in range(10, 16):
    for x in (12, 13, 14):
        tallgrass[y * W + x] = 1
mk.blob(tallgrass, W, H, 18.0, 22.5, 2.2, 1.6)      # optional grind patch at the foot
mk.blob(tallgrass, W, H, 8.0, 4.5, 2.0, 1.4)        # and one on the top tier

for i in range(W * H):
    if tree[i] or cliff[i]:
        path[i] = tallgrass[i] = 0
    if tallgrass[i]:
        path[i] = 0

pt.ledge_run(deco, W, H, 17, 13, 16, rng, family="grass")
pt.ledge_run(deco, W, H, 9, 3, 6, rng, family="grass")

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

m: dict = {
    "id": "cinderwind_scarp", "display_name": "Cinderwind Scarp",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base},
               {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
                "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
               {"name": "t_path", "role": "terrain", "terrain": "path",
                "set": "vesper_overworld_set", "depth": 0, "data": path},
               {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
                "set": "vesper_overworld_set", "depth": 0, "data": cliff},
               {"name": "t_tree", "role": "terrain", "terrain": "tree",
                "set": "vesper_overworld_set", "depth": 0, "data": tree},
               {"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/windward-stair-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/windward-stair-a.webp",
        "assets/backgrounds/battle/windward-stair-b.webp",
    ],
}

m["warps"] += [
    {"id": "to_deep", "at": {"tx": 0, "ty": 20}, "trigger": "step_on",
     "to_map": "cinderhead_deep", "to": {"tx": 26, "ty": 12}, "facing": "left", "transition": "door"},
    {"id": "to_deep_s", "at": {"tx": 0, "ty": 21}, "trigger": "step_on",
     "to_map": "cinderhead_deep", "to": {"tx": 26, "ty": 13}, "facing": "left", "transition": "door"},
    {"id": "to_terraces", "at": {"tx": W - 1, "ty": 4}, "trigger": "step_on",
     "to_map": "galehigh_terraces", "to": {"tx": 1, "ty": 14}, "facing": "right", "transition": "fade"},
    {"id": "to_terraces_s", "at": {"tx": W - 1, "ty": 5}, "trigger": "step_on",
     "to_map": "galehigh_terraces", "to": {"tx": 1, "ty": 15}, "facing": "right", "transition": "fade"},
]


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


# the foot: Cinderhead's spoil — ore carts left where the rail gave out, crystal
obj("spoil_cart_a", "cinderhead_ore_cart", (2, 23), 2, 2, overhang=1)
obj("spoil_cart_b", "cinderhead_ore_cart", (13, 19), 2, 2, overhang=1)
obj("spoil_crystal_a", "cinderhead_crystal_cluster", (20, 19), 2, 2, overhang=1)
obj("spoil_crystal_b", "cinderhead_crystal_cluster", (10, 23), 2, 2, overhang=1)
obj("foot_lamp", "tinderwick_lamp_post", (7, 17), 1, 3, overhang=2, walk_under=True)
# the middle tier: a lamp at the turn, a crown tree on the far side
obj("mid_lamp", "tinderwick_lamp_post", (16, 9), 1, 3, overhang=2, walk_under=True)
obj("mid_tree", "tinderwick_tree", (3, 10), 3, 4, overhang=3, walk_under=True)
# the top tier: Galehigh's first kite poles + the wind cairn — the gate in sight
obj("kite_pole_a", "galehigh_kite_pole_a", (12, 2), 2, 3, overhang=2, walk_under=True)
obj("kite_pole_b", "galehigh_kite_pole_b", (20, 6), 2, 3, overhang=2, walk_under=True)
obj("wind_cairn", "windward_cairn", (3, 3), 2, 3, overhang=2)
m["triggers"].append({"id": "cairn_read", "kind": "dialogue", "at": {"tx": 4, "ty": 5},
                      "activation": "interact", "ref": "npc.scarp_cairn"})
owed.append("npc.scarp_cairn")

for (x, y) in [(15, 23), (21, 14), (2, 14), (11, 6), (22, 23)]:
    deco[y * W + x] = gid("boulder")

# trainers keep the two turns (each faces down onto its tier's road)
owed += pt.trainer_beat(m, tid="scarp_hauler", at=(11, 11), facing="down", sight=3,
                        sprite="npc_man")
owed += pt.trainer_beat(m, tid="scarp_kiterunner", at=(21, 3), facing="down", sight=3,
                        sprite="kite_weaver")

owed += pt.sign(m, deco, W, sid="cinderwind_scarp", at=(3, 19))
owed += pt.cache(m, cid="scarp_amber", at=(20, 24))         # off the foot, behind the crystals
owed += pt.cache(m, cid="scarp_balm", at=(2, 11))           # the middle tier, behind the crown tree

TABLE = [
    {"kin_id": 48, "weight": 30, "min_level": 28, "max_level": 30},    # Rubbol
    {"kin_id": 101, "weight": 25, "min_level": 28, "max_level": 31},   # Galefox
    {"kin_id": 98, "weight": 20, "min_level": 29, "max_level": 31},    # Thrumble
    {"kin_id": 36, "weight": 15, "min_level": 29, "max_level": 31},    # Lumecite
    {"kin_id": 92, "weight": 8, "min_level": 30, "max_level": 31},     # Nimbruff
    {"kin_id": 46, "weight": 2, "min_level": 31, "max_level": 31},     # Voltcrag (rare)
]
m["encounters"] = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                                     id_prefix="scarp", table=TABLE)

covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (tree, cliff, path, tallgrass, deco))}
cells = {(x, y) for o in m["objects"]
         for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
         for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.12, avoid=covered | cells | busy | LANE)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
