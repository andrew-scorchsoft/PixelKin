#!/usr/bin/env python3
"""
Saltreach Fen I — brackish reed marsh under glinting mist (walkthrough/02-east).

THE PATTERN-LIBRARY SHOWCASE: a big route (32x44) with real depth, built as a
list of decisions via tools/maps/patterns.py — pools and causeways, two reed-bed
encounter bands (zones derived FROM the paint), two sight-trainer beats, a
raised east BANK entered the long way round and hopped down by one-way LEDGES,
a Tidecall channel tease with an islet cache, and the gated boundary channel
north to Fen II. Enter west from Pearlmoor; exit north (Tidecall held).

Run:  ./venv/bin/python tools/maps/build_saltreach_fen_i.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 32, 44
rng = random.Random(71)
owed: list[str] = []

# ---- terrain grids ---------------------------------------------------------------
tree = mk.make_grid(W, H)       # the marsh's wooded enclosure
pond = mk.make_grid(W, H)       # marsh pools + the two channels (water-over-grass)
tallgrass = mk.make_grid(W, H)  # reed beds (the encounter terrain)
cliff = mk.make_grid(W, H)      # the raised east bank's rim
path = mk.make_grid(W, H)       # the causeway spine

# enclosure: organic tree border, bottom sealed too (off-map = continuation)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(7, 2, 3), (26, 3, 3), (2, 20, 3), (30, 36, 3), (29, 12, 2)],
                  rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)

# pools — scattered organic marsh water
for (cx, cy, rx, ry) in [(13, 40.5, 4, 1.8), (22, 36, 5, 2.5), (5, 28, 3.5, 2.5),
                         (15, 29, 4, 2.2), (10, 17, 3, 2), (24, 9, 4, 2.5), (5, 7, 2.5, 2)]:
    mk.blob(pond, W, H, cx, cy, rx, ry)
# the DEEP-CHANNEL tease east of the fork (Tidecall visibly wanted — and held)
mk.blob(pond, W, H, 27, 29, 3.2, 4.2)
# the BOUNDARY channel: a full-width water band before the Fen II exit
mk.rect(pond, W, H, 2, 3, 29, 4)

# the causeway spine (south landing -> fork -> north shore) + the side plank
mk.hline(path, W, H, 38, 1, 11)          # in from Pearlmoor's landing
mk.vline(path, W, H, 11, 24, 38)         # main causeway north
mk.hline(path, W, H, 30, 12, 20)         # the fork's side plank toward the channel
mk.vline(path, W, H, 11, 10, 24)         # causeway past the bank turn-off
mk.hline(path, W, H, 18, 12, 17)         # the bank turn-off (the long way up)
mk.hline(path, W, H, 10, 11, 15)         # north shore approach
mk.vline(path, W, H, 15, 5, 9)           # to the channel's south shore
mk.vline(path, W, H, 15, 1, 2)           # the far shore (reached by Tidecall)
mk.vline(path, W, H, 16, 1, 2)

# the raised EAST BANK: cliff rim, ledge lip south, entered via the west gap —
# walk up the turn-off, explore, hop the ledge back down to the causeway side
BANK = pt.Area(18, 13, 28, 21)
pt.terrace(cliff, mk.make_grid(W, H), W, H, BANK, gap=(17, 18), gap_side="left", rng=rng)
# (the rim grid is what we want here; the LEDGE lip is re-stamped onto the
#  real deco grid below.)

# reed beds — south bed optional, the big mid bed STRADDLES the lane (mandatory
# crossing), the north bed guards the shore approach
mk.blob(tallgrass, W, H, 17, 40, 3.2, 1.7)
mk.blob(tallgrass, W, H, 7, 33, 2.5, 1.6)
mk.blob(tallgrass, W, H, 13, 22, 4.2, 2.3)
mk.blob(tallgrass, W, H, 8, 12, 3, 2)

# warp openings carved out of the enclosure (west entry, north exit)
for (x, y) in [(0, 37), (0, 38), (1, 37), (1, 38), (15, 0), (16, 0), (15, 1), (16, 1)]:
    tree[y * W + x] = 0

# the islet in the channel finger (dry ground under its cache)
pond[29 * W + 27] = 0
pond[29 * W + 26] = 0

# precedence: trees/cliff claim their cells; planks carve water; the big mid
# bed (rows 20-24) keeps its grass OVER the lane — the mandatory crossing —
# elsewhere the lane carves grass
for i in range(W * H):
    y = i // W
    if path[i]:
        pond[i] = 0
        if tallgrass[i]:
            if 20 <= y <= 24:
                path[i] = 0  # the lane pauses through the reed crossing
            else:
                tallgrass[i] = 0
    if tree[i] or cliff[i]:
        pond[i] = 0
        tallgrass[i] = 0
        path[i] = 0
    if pond[i]:
        tallgrass[i] = 0

terrain_layers = [
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_pond", "role": "terrain", "terrain": "pond",
     "set": "vesper_overworld_set", "depth": 0, "data": pond},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]

# ---- base + deco -----------------------------------------------------------------
gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]

deco = mk.make_grid(W, H)
m: dict = {}

# the bank's hop-down LEDGE lip (re-stamped onto the real deco grid)
pt.ledge_run(deco, W, H, BANK.y1, BANK.x0 + 2, BANK.x1 - 2, rng)

# planks: dock boards where the causeway bridges a carved pool neck
for i in range(W * H):
    if path[i]:
        x, y = i % W, i // W
        neighbours_water = sum(
            1 for (nx, ny) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
            if 0 <= nx < W and 0 <= ny < H and pond[ny * W + nx])
        if neighbours_water >= 2:
            deco[i] = gid("dock")
# lantern-buoys marking the deep water
for (x, y) in [(24, 30), (13, 41), (24, 8), (16, 4)]:
    deco[y * W + x] = gid("buoy")

# ---- content stamps ----------------------------------------------------------------
m.update({
    "id": "saltreach_fen_i", "display_name": "Saltreach Fen", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "warps": [
        # west: in/out of Pearlmoor (landing ON pearlmoor's to_fen warp tile)
        {"id": "to_quay", "at": {"tx": 0, "ty": 37}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 27, "ty": 12}, "facing": "left",
         "transition": "fade"},
        {"id": "to_quay_s", "at": {"tx": 0, "ty": 38}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 27, "ty": 12}, "facing": "left",
         "transition": "fade"},
        # north: across the Tidecall channel to Fen II (inert tease until authored)
        {"id": "to_fen_ii", "at": {"tx": 15, "ty": 0}, "trigger": "step_on",
         "to_map": "saltreach_fen_ii", "to": {"tx": 15, "ty": 42}, "facing": "up",
         "transition": "fade"},
        {"id": "to_fen_ii_e", "at": {"tx": 16, "ty": 0}, "trigger": "step_on",
         "to_map": "saltreach_fen_ii", "to": {"tx": 16, "ty": 42}, "facing": "up",
         "transition": "fade"},
    ],
    "npcs": [
        # the travelling fen-warden (mood + the soft B-arc seed, hooks §6)
        {"id": "fen_warden", "at": {"tx": 4, "ty": 37}, "facing": "right",
         "sprite": "npc_old_man", "movement": "look_around",
         "dialogue_ref": "npc.fen_warden"},
    ],
    "gates": [],
    "encounters": [],
    "triggers": [],
    "music": "assets/audio/music/saltreach-fen-a.mp3",
})

# sight-trainer beats on the causeway (level-design §11 rule 7)
owed += pt.trainer_beat(m, tid="fen_wader_a", at=(11, 26), facing="down",
                        sight=4, sprite="npc_woman")
owed += pt.trainer_beat(m, tid="fen_courier_b", at=(14, 10), facing="left",
                        sight=4, sprite="npc_man")

# caches (variety rule): a charge behind the reed screen [MISSABLE], the
# bank's wicks purse (ledge shelf), the Tidecall islet's balm
owed += pt.cache(m, cid="fen_reed", at=(19, 41))
owed += pt.cache(m, cid="fen_bank_wicks", at=(22, 16))
owed += pt.cache(m, cid="fen_islet", at=(27, 29))

# signs: the landing, the channel tease at the fork's end, the boundary
owed += pt.sign(m, deco, W, sid="fen_landing", at=(3, 39))
owed += pt.sign(m, deco, W, sid="fen_channel", at=(20, 29))
owed += pt.sign(m, deco, W, sid="fen_boundary", at=(14, 6))

# encounter zones FROM the painted reed beds (band 16-18, rate 0.10, hooks §6)
FEN_TABLE = [
    {"kin_id": 59, "weight": 40, "min_level": 16, "max_level": 18},  # Dewling — marsh sprite
    {"kin_id": 27, "weight": 25, "min_level": 16, "max_level": 18},  # Brineroll
    {"kin_id": 31, "weight": 20, "min_level": 16, "max_level": 18},  # Lumpin
    {"kin_id": 60, "weight": 15, "min_level": 17, "max_level": 18},  # Poolfrond — the rarer middle stage
]
m["encounters"] = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass",
                                     rate=0.10, table=FEN_TABLE, id_prefix="reed")

# a few dry-bank trees with real shape (§11 rule 2)
pt.crown_tree(m, oid="bank_tree", sprite="tinderwick_tree", at=(24, 15))
pt.crown_tree(m, oid="south_tree", sprite="tinderwick_tree", at=(3, 31))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

mk.scatter_decor(deco, base, W, H, rng, density=0.10,
                 avoid={(x, y) for y in range(H) for x in range(W)
                        if path[y * W + x] or tallgrass[y * W + x] or pond[y * W + x]
                        or cliff[y * W + x] or tree[y * W + x]})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
