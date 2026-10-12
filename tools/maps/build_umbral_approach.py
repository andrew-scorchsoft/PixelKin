#!/usr/bin/env python3
"""
The Umbral Approach — the mountain road (graph.ts `umbral_approach`, kind route,
region central, band 50-53). NEW in the 2026-10 geometry fix.

Why it exists: the honest north-up world puts the dark mountain NORTH of the
Vesper Crossroads, and the Spire's road now leaves the hub's north edge. The
old link dropped you straight from the warm plaza into the Penumbra Ring — the
endgame's one missing leg of travel. This is it: the last climb, where the
lamplit country gives out and the Hollowing's quiet begins.

THE DIMMING (the map's spine, read bottom to top — three switchback tiers):
  * the FOOT (rows 24-33): the crossroads' green grass and a real path, crown
    trees, the last tall-grass bed — still the lit world;
  * the DRAINED SHELF (rows 14-23): blight ground, no path survives (the
    "road that forgets", Coldfog's register), way-lamps the only line;
  * the BASALT SHOULDER (rows 0-13): the burned-back ground of the Penumbra
    itself, Còr's null-lanterns begin, kin go quiet (no encounters up here —
    "kin refuse the dark", 05 §6, starts at this tier).
Two cliff bands separate the tiers; the lane climbs each through a single gap,
and each band carries a one-way LEDGE shortcut back down (§3a r1 — the return
is shorter than the climb). Three Hollowing acolytes keep the turns: grief
dressed as mercy, never cartoonish — they ask you to turn back, kindly, and
fight only because you won't.

Wild kin (lv 50-53, the last before the Spire): Dark/Lunar mountain-dwellers —
Voidmantle, Omenire, Nightwraith, Whorlix, Pyriven (new to the wild) and the
uncommon Liminalux. (Lunaveil stays the Starwell's scripted set-piece — never wild.)

HANDSHAKE: crossroads `to_penumbra`/`_e` at (9,0)/(10,0) land here at
(2,32)/(3,32); our `to_crossroads`/`_e` at (2,33)/(3,33) land at crossroads
(9,1)/(10,1) (the Wren band row — landing ON a trigger never fires it).
Our `to_penumbra`/`_e` at (15,0)/(16,0) land on the Ring's south entry
(13,33)/(14,33); the Ring's `to_approach`/`_e` land at our (15,1)/(16,1).

audit_flow notes: the lane's §3a loop is the two ledges; the top tier is
deliberately encounter-free (the dark's edge) — its gameplay load is the
third acolyte and the lookout's lore.

Run:  python3 tools/maps/build_umbral_approach.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 34
rng = random.Random(171)
owed: list[str] = []

FOOT, SHELF = 24, 14            # first row of each tier (grass foot / blight shelf)

# ---- terrain presence grids ---------------------------------------------------------
tree = mk.make_grid(W, H)       # the foot's wooded flanks
wall = mk.make_grid(W, H)       # basalt walls (shelf + shoulder flanks, the top rim)
cliff = mk.make_grid(W, H)      # the two tier bands
path = mk.make_grid(W, H)       # the foot's real road (it gives out at the shelf)
tallgrass = mk.make_grid(W, H)  # the foot's bed
blight = mk.make_grid(W, H)     # the shelf's blighttuft bed
deco = mk.make_grid(W, H)

# flanks: trees at the foot, basalt above it
mk.organic_border(tree, W, H, left=1, right=1, depth=2,
                  bumps=[(1, 28, 2), (22, 30, 2)], rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)                  # the foot's south edge
for y in range(0, FOOT):
    for x in range(W):
        tree[y * W + x] = 0
mk.organic_border(wall, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(4, 1, 2), (21, 1, 2), (1, 9, 2), (22, 6, 2), (1, 18, 1), (22, 17, 2)],
                  rng=rng)
for y in range(FOOT, H):
    for x in range(W):
        wall[y * W + x] = 0

# the two tier bands (rows 22-23 and 12-13), each with the lane's gap + a ledge
for y in (22, 23):
    mk.hline(cliff, W, H, y, 2, W - 3)
for y in (12, 13):
    mk.hline(cliff, W, H, y, 2, W - 3)
GAP_A, GAP_B = (18, 19), (5, 6)
for x in GAP_A:
    for y in (22, 23):
        cliff[y * W + x] = 0
for x in GAP_B:
    for y in (12, 13):
        cliff[y * W + x] = 0
# the ledge shortcuts: the band's top row opens, its lower row is the hop
for x in range(8, 12):
    cliff[22 * W + x] = 0
    cliff[23 * W + x] = 0
for x in range(12, 16):
    cliff[12 * W + x] = 0
    cliff[13 * W + x] = 0

# openings: the crossroads foot (cols 2-3) and the Ring gate (cols 15-16)
for x in (2, 3):
    for y in (H - 2, H - 1):
        tree[y * W + x] = 0
for x in (15, 16):
    for y in (0, 1):
        wall[y * W + x] = 0

# ---- the lane (logical route; only the FOOT carries real path tiles) ----------------
LANE = set()
def run(cells):
    for c in cells:
        LANE.add(c)
for y in range(26, H):
    run([(2, y), (3, y)])                              # L1 up from the crossroads
for x in range(2, 20):
    run([(x, 26), (x, 27)])                            # L2 east along the foot
for y in range(17, 28):
    run([(18, y), (19, y)])                            # L3 up through band A's gap
for x in range(5, 20):
    run([(x, 17), (x, 18)])                            # L4 west along the shelf
for y in range(8, 19):
    run([(5, y), (6, y)])                              # L5 up through band B's gap
for x in range(5, 17):
    run([(x, 8), (x, 9)])                              # L6 east along the shoulder
for y in range(0, 10):
    run([(15, y), (16, y)])                            # L7 up to the Ring gate
for (x, y) in LANE:
    if y >= FOOT:
        path[y * W + x] = 1

# encounter beds — each a FULL-HEIGHT strip across its tier's corridor, so the
# lane can't skirt it (the road pauses through the bed):
for y in range(FOOT, H - 2):                           # the foot's grass strip
    for x in range(8, 12):
        tallgrass[y * W + x] = 1
for y in range(SHELF, 22):                             # the shelf's blight strip
    for x in range(9, 13):
        blight[y * W + x] = 1
mk.blob(tallgrass, W, H, 14.5, 30.0, 2.0, 1.4)         # an optional patch by the foot
mk.blob(blight, W, H, 3.5, 20.0, 1.6, 1.4)             # …and one under the shelf's lip

# precedence: structure wins; the road pauses through the beds
for i in range(W * H):
    if tree[i] or wall[i] or cliff[i]:
        path[i] = tallgrass[i] = blight[i] = 0
    if tallgrass[i] or blight[i]:
        path[i] = 0

# ledges on the bands' lower rows (hop SOUTH back down a tier)
pt.ledge_run(deco, W, H, 23, 8, 11, rng, family="grass")
pt.ledge_run(deco, W, H, 13, 12, 15, rng, family="scree")

# ---- base: grass foot -> blight shelf -> basalt shoulder ----------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
bs = [gid("basalt0"), gid("basalt1"), gid("basalt2")]
base = []
for y in range(H):
    for x in range(W):
        fam = gg if y >= FOOT else (bl if y >= SHELF else bs)
        base.append(rng.choice(fam) if rng.random() < 0.5 else fam[0])

terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": blight},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_basaltwall", "role": "terrain", "terrain": "basaltwall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

m: dict = {
    "id": "umbral_approach", "display_name": "The Umbral Approach",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/penumbra-ring-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/penumbra-ring-a.webp",
        "assets/backgrounds/battle/penumbra-ring-b.webp",
    ],
}

# ---- warps --------------------------------------------------------------------------
m["warps"] += [
    {"id": "to_crossroads", "at": {"tx": 2, "ty": H - 1}, "trigger": "step_on",
     "to_map": "vesper_crossroads", "to": {"tx": 9, "ty": 1}, "facing": "down",
     "transition": "fade"},
    {"id": "to_crossroads_e", "at": {"tx": 3, "ty": H - 1}, "trigger": "step_on",
     "to_map": "vesper_crossroads", "to": {"tx": 10, "ty": 1}, "facing": "down",
     "transition": "fade"},
    {"id": "to_penumbra", "at": {"tx": 15, "ty": 0}, "trigger": "step_on",
     "to_map": "penumbra_ring", "to": {"tx": 13, "ty": 33}, "facing": "up",
     "transition": "fade"},
    {"id": "to_penumbra_e", "at": {"tx": 16, "ty": 0}, "trigger": "step_on",
     "to_map": "penumbra_ring", "to": {"tx": 14, "ty": 33}, "facing": "up",
     "transition": "fade"},
]

# ---- objects: crown trees at the foot, way-lamps on the shelf + shoulder, the shrine --
def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


obj("foot_tree_a", "tinderwick_tree", (5, 28), 3, 4, overhang=3, walk_under=True)
obj("foot_tree_b", "tinderwick_tree", (19, 29), 3, 4, overhang=3, walk_under=True)
obj("foot_lamp", "tinderwick_lamp_post", (4, 23), 1, 3, overhang=2, walk_under=True)
# the way-lamps: the only warm line once the road gives out (the Ring's own lamps)
for n, (x, y) in enumerate([(17, 19), (8, 14), (4, 9), (13, 5)]):
    obj(f"way_lamp_{n}", "penumbra_way_lamp", (x, y), 1, 3, overhang=2, walk_under=True)
# a snuffed wayshrine on the shoulder — the old inward road's, put out gently
obj("snuffed_shrine", "glowmoss_deep_null_lantern_shrine", (19, 3), 2, 3, overhang=2)
for i, tx in enumerate((19, 20)):
    m["triggers"].append({"id": f"shrine_read_{i}", "kind": "dialogue",
                          "at": {"tx": tx, "ty": 6}, "activation": "interact",
                          "ref": "npc.approach_snuffed_shrine"})
owed.append("npc.approach_snuffed_shrine")

# the shelf + shoulder dressing: what the dimming leaves behind — a dead tree,
# doused road-lamps, a Hollowing notice, a quiet camp left tidy, a charred tree
obj("shelf_dead_tree", "hushfrost_dead_tree", (14, 19), 2, 3, overhang=2, walk_under=True)
obj("shelf_doused_w", "coldfog_doused_lamp", (7, 14), 1, 3, overhang=2, walk_under=True)
obj("shelf_doused_e", "coldfog_doused_lamp", (16, 14), 1, 3, overhang=2, walk_under=True)
obj("shoulder_doused", "coldfog_doused_lamp", (13, 10), 1, 3, overhang=2, walk_under=True)
obj("shelf_notice", "coldfog_hollowing_notice", (17, 15), 1, 2, overhang=1, walk_under=True)
m["triggers"].append({"id": "notice_read", "kind": "dialogue", "at": {"tx": 17, "ty": 16},
                      "activation": "interact", "ref": "npc.approach_notice"})
owed.append("npc.approach_notice")
obj("shoulder_camp", "penumbra_vigil_camp", (3, 4), 3, 2, overhang=1)
m["triggers"].append({"id": "camp_read", "kind": "dialogue", "at": {"tx": 4, "ty": 5},
                      "activation": "interact", "ref": "npc.approach_vigil_camp"})
owed.append("npc.approach_vigil_camp")
obj("shoulder_quiet_camp", "coldfog_quiet_camp", (8, 10), 3, 2, overhang=1)
obj("shoulder_charred", "fallenstar_tree_charred", (11, 2), 3, 4, overhang=3, walk_under=True)

# Còr's null-lanterns begin on the shoulder (the safe line ends where his begins)
for (x, y) in [(9, 6), (11, 6), (18, 10)]:
    deco[y * W + x] = gid("null_lantern")
# outcrops (boulder clusters, never wall slabs) + drained dressing
for (x, y) in [(20, 15), (21, 16), (14, 21), (2, 11), (3, 11), (21, 25)]:
    deco[y * W + x] = gid("boulder")
for (x, y, n) in [(7, 20, "greymoss_a"), (16, 15, "greymoss_b"), (10, 10, "greymoss_a"),
                  (7, 3, "greymoss_b"), (20, 8, "greymoss_a"), (8, 3, "greymoss_b"),
                  (5, 21, "greymoss_b"), (19, 14, "greymoss_a"), (12, 15, "greymoss_b"),
                  (3, 8, "greymoss_a"), (17, 5, "greymoss_b"), (21, 12, "greymoss_a")]:
    deco[y * W + x] = gid(n)

# ---- trainers: three Hollowing acolytes, each facing down onto a lane leg -----------
owed += pt.trainer_beat(m, tid="approach_acolyte_a", at=(14, 25), facing="down", sight=3,
                        sprite="hollowing_acolyte")
owed += pt.trainer_beat(m, tid="approach_acolyte_b", at=(14, 16), facing="down", sight=3,
                        sprite="hollowing_acolyte")
owed += pt.trainer_beat(m, tid="approach_acolyte_c", at=(10, 7), facing="down", sight=3,
                        sprite="hollowing_acolyte")

# ---- signs + caches -----------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="umbral_approach", at=(4, 30))
owed += pt.sign(m, deco, W, sid="umbral_lookout", at=(21, 19))
owed += pt.cache(m, cid="approach_shard", at=(18, 31))     # the foot's off-lane pocket
owed += pt.cache(m, cid="approach_wicks", at=(2, 15))      # under the shelf's west lip

# ---- encounters (the foot's grass + the shelf's blight; the shoulder is quiet) ------
TABLE_FOOT = [
    {"kin_id": 138, "weight": 25, "min_level": 50, "max_level": 52},   # Voidmantle
    {"kin_id": 113, "weight": 20, "min_level": 50, "max_level": 52},   # Omenire
    {"kin_id": 112, "weight": 18, "min_level": 50, "max_level": 52},   # Nightwraith
    {"kin_id": 143, "weight": 15, "min_level": 50, "max_level": 52},   # Whorlix
    {"kin_id": 15, "weight": 12, "min_level": 51, "max_level": 52},    # Pyriven
    {"kin_id": 135, "weight": 10, "min_level": 51, "max_level": 52},   # Liminalux (uncommon)
]
TABLE_SHELF = [dict(e, min_level=e["min_level"] + 1, max_level=e["max_level"] + 1)
               for e in TABLE_FOOT]
m["encounters"] = (
    pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                       id_prefix="foot", table=TABLE_FOOT)
    + pt.zones_from_grid(blight, W, H, terrain="tall_grass", rate=0.11,
                         id_prefix="shelf", table=TABLE_SHELF))

# ---- scatter (beside the foot's road only — the upper tiers stay sparse) -----------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (tree, wall, cliff, path, tallgrass, blight, deco))}
cells = {(x, y) for o in m["objects"]
         for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
         for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
upper = {(x, y) for y in range(FOOT) for x in range(W)}
mk.scatter_decor(deco, base, W, H, rng, density=0.10,
                 avoid=covered | cells | busy | LANE | upper)

# the upper tiers get their own sparse drained scatter (moss, grit) — never on
# the lane, never beside a way-lamp's line of sight
drained = [gid("greymoss_a"), gid("greymoss_b"), gid("g_pebble")]
for y in range(2, FOOT):
    for x in range(2, W - 2):
        i = y * W + x
        if deco[i] or (x, y) in LANE or (x, y) in cells or (x, y) in busy:
            continue
        if wall[i] or cliff[i] or blight[i]:
            continue
        if rng.random() < 0.09:
            deco[i] = rng.choice(drained)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
