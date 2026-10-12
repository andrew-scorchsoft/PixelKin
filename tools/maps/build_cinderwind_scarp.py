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

TRAVERSAL PASS (2026-10, 09-the-wild-ways §3): the bands are TALL scarp faces
now (rim + face + a pinned rock-face foot row, wildkit.face_wall) with NO
walk-up gap — the main climb is by the ore-haulers' LADDERS (wildkit.ladder),
and the two pitches sit at opposite ends (A at the east end, B at the west),
so the way up zig-zags the whole face: in along the foot, up A, back west
across the middle tier past the hauler, up B, east along the top to the gate.
The ledges sit at the other ends, so the way DOWN is two quick hops (62 steps
up vs 36 down). No Gift involved; warps, trainers, caches and tables unchanged.

Wild kin (lv 28-31, closing the Deep->Galehigh gap): Rubbol, Galefox,
Thrumble, Lumecite, Nimbruff, very rare Voltcrag. Four of them (Rubbol, Galefox,
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
import wildkit as wk
from mapkit import gid

W, H = 24, 28
rng = random.Random(173)
owed: list[str] = []

tree = mk.make_grid(W, H)
cliff = mk.make_grid(W, H)
path = mk.make_grid(W, H)
tallgrass = mk.make_grid(W, H)
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)
pin: dict = {}

m: dict = {
    "id": "cinderwind_scarp", "display_name": "Cinderwind Scarp",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/windward-stair-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/windward-stair-a.webp",
        "assets/backgrounds/battle/windward-stair-b.webp",
    ],
}
wk.use_traverse(m)

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

# THE TWO PITCHES (traversal pass 2026-10): each tier band is a TALL scarp face
# now — two cliff rows (rim + lit face) over a third, pinned rock-face FOOT row —
# with NO walk-up gap. The haulers' ladders are the way up, and they sit at
# OPPOSITE ends: pitch A (foot -> middle) at the EAST end, pitch B (middle ->
# top) at the WEST end, so the climb zig-zags the whole face. Each band keeps
# one grass LEDGE at the other end (pitch B's in the east, A's in the west):
# the way down hops them in two quick drops — the climb is earned, the
# descent is a shortcut (§3a r1).
BAND_A, BAND_B = (15, 16, 17), (7, 8, 9)       # (rim, face, foot) rows
LADDER_A, LADDER_B = 19, 7                       # ladder columns
LEDGE_A, LEDGE_B = range(3, 7), range(17, 20)    # hop-down notches
for (rim, face, foot), ledge in ((BAND_A, LEDGE_A), (BAND_B, LEDGE_B)):
    mk.hline(cliff, W, H, rim, 2, W - 3)
    mk.hline(cliff, W, H, face, 2, W - 3)
    for x in ledge:                              # the notch: open, ledge mid-band
        cliff[rim * W + x] = cliff[face * W + x] = 0
    pt.ledge_run(deco, W, H, face, ledge.start, ledge.stop - 1, rng, family="grass")
    wk.face_wall(pin, x0=2, x1=W - 3, y0=foot, y1=foot)
    for x in ledge:
        pin.pop((x, foot), None)                 # ...and the hop lands on grass

wk.ladder(m, deco, W, x=LADDER_A, y0=BAND_A[0], y1=BAND_A[2], sid="scarp_ladder_a")
wk.ladder(m, deco, W, x=LADDER_B, y0=BAND_B[0], y1=BAND_B[2], sid="scarp_ladder_b")
FACE = set(pin)

# the lane (a worn path the whole way — this is still lamp-country)
LANE = set()
for x in range(0, LADDER_A + 1):
    LANE |= {(x, 20), (x, 21)}          # L1 in from the mine mouth, east along the foot
for y in range(18, 20):
    LANE.add((LADDER_A, y))             # ... to the foot of ladder A
for y in range(12, 15):
    LANE.add((LADDER_A, y))             # off the top of ladder A
for x in range(LADDER_B, LADDER_A + 1):
    LANE |= {(x, 12), (x, 13)}          # L2 back WEST along the middle tier
for y in range(10, 12):
    LANE.add((LADDER_B, y))             # ... to the foot of ladder B
for y in range(4, 7):
    LANE.add((LADDER_B, y))             # off the top of ladder B
for x in range(LADDER_B, W):
    LANE |= {(x, 4), (x, 5)}            # L3 east along the top tier to the terraces' gate
for (x, y) in LANE:
    path[y * W + x] = 1

# mandatory grass strips (full tier height, the road pauses through them)
for y in range(18, 26):
    for x in (15, 16, 17):
        tallgrass[y * W + x] = 1        # the foot: between the mouth and ladder A
for y in range(10, 15):
    for x in (11, 12, 13):
        tallgrass[y * W + x] = 1        # the middle tier: crossed up AND down
mk.blob(tallgrass, W, H, 5.0, 24.6, 2.2, 1.2)       # optional grind patch in the foot's SW corner
mk.blob(tallgrass, W, H, 11.5, 2.6, 2.0, 0.9)       # and one on the top tier

for i in range(W * H):
    x, y = i % W, i // W
    if tree[i] or cliff[i] or (x, y) in FACE:
        path[i] = tallgrass[i] = 0
    if tallgrass[i]:
        path[i] = 0

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base},
               {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
                "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
               {"name": "t_path", "role": "terrain", "terrain": "path",
                "set": "vesper_overworld_set", "depth": 0, "data": path},
               {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
                "set": "vesper_overworld_set", "depth": 0, "data": cliff},
               {"name": "t_tree", "role": "terrain", "terrain": "tree",
                "set": "vesper_overworld_set", "depth": 0, "data": tree},
               {"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": above}]

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
obj("spoil_cart_b", "cinderhead_ore_cart", (12, 18), 2, 2, overhang=1)
obj("spoil_crystal_a", "cinderhead_crystal_cluster", (21, 22), 2, 2, overhang=1)
obj("spoil_crystal_b", "cinderhead_crystal_cluster", (8, 23), 2, 2, overhang=1)
# lamps at each ladder's foot and head — the hauler's way, lit
obj("foot_lamp", "tinderwick_lamp_post", (20, 17), 1, 3, overhang=2, walk_under=True)
obj("mid_lamp", "tinderwick_lamp_post", (20, 11), 1, 3, overhang=2, walk_under=True)
obj("pitch_lamp", "tinderwick_lamp_post", (8, 9), 1, 3, overhang=2, walk_under=True)
# the middle tier: a crown tree on the far (west) side, over the balm cache
obj("mid_tree", "tinderwick_tree", (3, 10), 3, 4, overhang=3, walk_under=True)
# the top tier: Galehigh's first kite poles + the wind cairn — the gate in sight
obj("kite_pole_a", "galehigh_kite_pole_a", (13, 1), 2, 3, overhang=2, walk_under=True)
obj("kite_pole_b", "galehigh_kite_pole_b", (17, 1), 2, 3, overhang=2, walk_under=True)
obj("wind_cairn", "windward_cairn", (3, 3), 2, 3, overhang=2)
m["triggers"].append({"id": "cairn_read", "kind": "dialogue", "at": {"tx": 4, "ty": 5},
                      "activation": "interact", "ref": "npc.scarp_cairn"})
owed.append("npc.scarp_cairn")

for (x, y) in [(10, 25), (21, 14), (16, 11), (11, 6), (5, 25), (22, 19)]:
    deco[y * W + x] = gid("boulder")

# trainers keep the tiers: the hauler watches the middle tier's whole height
# (every way west across it walks his column), the kite-runner the gate.
owed += pt.trainer_beat(m, tid="scarp_hauler", at=(15, 10), facing="down", sight=4,
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
    {"kin_id": 46, "weight": 2, "min_level": 31, "max_level": 31},     # Voltcrag (very rare)
]
m["encounters"] = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                                     id_prefix="scarp", table=TABLE)

covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (tree, cliff, path, tallgrass, deco))} | FACE
cells = {(x, y) for o in m["objects"]
         for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
         for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
# keep the ladders' head and foot tiles clear of scatter
ends = {(LADDER_A, BAND_A[0] - 1), (LADDER_A, BAND_A[2] + 1),
        (LADDER_B, BAND_B[0] - 1), (LADDER_B, BAND_B[2] + 1)}
mk.scatter_decor(deco, base, W, H, rng, density=0.12, avoid=covered | cells | busy | LANE | ends)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3, pin_base=pin)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
