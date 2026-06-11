#!/usr/bin/env python3
"""
Saltreach Fen II — deep channels and lantern-reeds (walkthrough/02-east).

Tidecall is LOAD-BEARING here: the route itself is the parted moon-channels
between reed isles (water carries the gate in its tileset metadata — no plank
bypass exists by construction, and no soft-lock either: the Fen I boundary
already required Tidecall, so every arrival holds it). South→north:

  landing (firm ground, sign) → the parted-channel crossing → the DENSEST reed
  isle of the marsh (band 17–19) → the fisher's jetty isle (E1 "The Quiet
  Reeds": three snuffed lantern-reeds, the third will not light — the silent
  B2 foreshadow; nobody names the Hollowing) → the signed Sunkbell turn-off
  east across the water → firm ground, a mandatory fringe-grass band, the
  reed-lamplighter sight trainer, and the treeline north to Lowleaf Hollow.

Hidden: a far reed isle no plank reaches (tide-walkers only) keeps a
Moth-amber. One ambient snuffed reed stands by the crossing — deco only, the
quiet visual foreshadow (no dialogue, per the region file).

Run:  ./venv/bin/python tools/maps/build_saltreach_fen_ii.py

audit_flow WAIVER — `loop` WARN accepted: Tidecall makes the whole channel
plane freely crossable, so the walk back is never the walk in (the §3a loop
lives in the WATER, not in a ledge); the one-way shortcut tier arrives with
the region's dungeons.
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 32, 44
rng = random.Random(73)
owed: list[str] = []

# ---- terrain grids ---------------------------------------------------------------
tree = mk.make_grid(W, H)
water = mk.make_grid(W, H)
sand = mk.make_grid(W, H)
tallgrass = mk.make_grid(W, H)
path = mk.make_grid(W, H)

# enclosure: organic tree border, bottom sealed (off-map = continuation)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(6, 2, 2), (24, 2, 2), (2, 24, 2), (30, 30, 2), (29, 7, 2)],
                  rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)

# the open fen: one broad water body — the isles are carved back out of it
mk.rect(water, W, H, 1, 7, 30, 39)

# firm ground: a sandy SHORE strip at the south landing; the north treeline
# band stays plain grass (the fen thins to firm green ground — hooks §1 beat 4)
mk.rect(sand, W, H, 10, 38, 21, 40)          # the landing shore strip
grass_north = mk.make_grid(W, H)             # carve the water back to grass
mk.rect(grass_north, W, H, 1, 2, 30, 7)
mk.blob(grass_north, W, H, 16, 8.5, 6.0, 1.8)

# reed ISLES (carved from the water as grass ground)
isles = {
    "first":  (10.5, 34.0, 4.2, 2.2),   # the crossing's far side
    "dense":  (8.0, 26.0, 5.0, 2.8),    # the densest reed isle of the marsh
    "reed_b": (14.0, 14.0, 3.2, 2.0),   # the mid-water reed's isle
    "lane":   (17.5, 21.0, 3.6, 2.2),   # the main lane's stepping isle
    "jetty":  (24.0, 28.0, 4.4, 2.6),   # the fisher's jetty isle (E1)
    "hidden": (3.8, 14.0, 2.4, 1.7),    # tide-walkers only: the Moth-amber isle
}
grass_isle = mk.make_grid(W, H)
for (cx, cy, rx, ry) in isles.values():
    mk.blob(grass_isle, W, H, cx, cy, rx, ry)
# the Sunkbell outcrop: a sand toe at the east border (the spur's doorstep) —
# the border opening stays exactly 2 tiles (a warp on EVERY open tile)
mk.rect(sand, W, H, 28, 13, 31, 16)
for x in (30, 31):
    for y in (14, 15):
        tree[y * W + x] = 0

# reed beds (the encounter terrain): the dense isle, the first isle, reed-B isle
mk.blob(tallgrass, W, H, 8.0, 26.0, 4.0, 2.2)
mk.blob(tallgrass, W, H, 9.5, 34.0, 2.4, 1.4)
mk.blob(tallgrass, W, H, 13.5, 14.0, 2.2, 1.4)
# the north fringe: a MANDATORY band across the firm ground (the lane pauses)
pt.mandatory_band(tallgrass, path, W, H, y0=4, y1=5, x0=3, x1=28)

# the lane: landing -> shore; north shore -> treeline (the wet middle is water)
mk.vline(path, W, H, 15, 39, 42)
mk.vline(path, W, H, 16, 39, 42)
mk.vline(path, W, H, 15, 1, 7)
mk.vline(path, W, H, 16, 1, 7)

# warp openings carved out of the enclosure
for (x, y) in [(15, 0), (16, 0), (15, 1), (16, 1), (15, 42), (16, 42), (15, 43), (16, 43)]:
    tree[y * W + x] = 0

# precedence: trees claim; isles/sand carve the water; grass beds only on land;
# the lane rides land only (the channels are the road — that's the point)
for i in range(W * H):
    if grass_isle[i] or sand[i] or grass_north[i]:
        water[i] = 0
    if tallgrass[i]:
        sand[i] = 0
    if tree[i]:
        water[i] = 0
        sand[i] = 0
        grass_isle[i] = 0
        tallgrass[i] = 0
        path[i] = 0
    if water[i]:
        tallgrass[i] = 0
        path[i] = 0
    if path[i]:
        tallgrass[i] = 0 if not (4 <= i // W <= 5) else tallgrass[i]

terrain_layers = [
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]

# ---- base + deco -----------------------------------------------------------------
gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]

deco = mk.make_grid(W, H)
m: dict = {}

# the fisher's jetty boards (dock over the isle's dry ground — always walkable)
for (x, y) in [(24, 27), (25, 27), (26, 27), (24, 28), (25, 28), (26, 28)]:
    deco[y * W + x] = gid("dock")
# lantern-buoys: the channel lane north, and the breadcrumb line east to Sunkbell
for (x, y) in [(13, 36), (12, 30), (12, 22), (14, 18), (15, 10),       # the lane
               (27, 22), (28, 18), (29, 16)]:                          # to Sunkbell
    deco[y * W + x] = gid("buoy")
# a boulder chokes the treeline lane to ONE column so the trainer's line holds
deco[3 * W + 15] = gid("boulder")

# ---- content stamps ----------------------------------------------------------------
m.update({
    "id": "saltreach_fen_ii", "display_name": "Saltreach Deeps", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "warps": [
        # south: back across the boundary channel to Fen I
        {"id": "to_fen_i", "at": {"tx": 15, "ty": 43}, "trigger": "step_on",
         "to_map": "saltreach_fen_i", "to": {"tx": 15, "ty": 1}, "facing": "down",
         "transition": "fade"},
        {"id": "to_fen_i_e", "at": {"tx": 16, "ty": 43}, "trigger": "step_on",
         "to_map": "saltreach_fen_i", "to": {"tx": 16, "ty": 1}, "facing": "down",
         "transition": "fade"},
        # north: through the treeline to Lowleaf Hollow (ungated — graph.ts)
        {"id": "to_hollow", "at": {"tx": 15, "ty": 0}, "trigger": "step_on",
         "to_map": "lowleaf_hollow", "to": {"tx": 14, "ty": 30}, "facing": "up",
         "transition": "fade"},
        {"id": "to_hollow_e", "at": {"tx": 16, "ty": 0}, "trigger": "step_on",
         "to_map": "lowleaf_hollow", "to": {"tx": 15, "ty": 30}, "facing": "up",
         "transition": "fade"},
        # east: the Sunkbell Shallows spur (Tidecall; MISSABLE by design)
        {"id": "to_sunkbell", "at": {"tx": 31, "ty": 14}, "trigger": "step_on",
         "to_map": "sunkbell_shallows", "to": {"tx": 1, "ty": 7}, "facing": "right",
         "requires_ability": "tidecall", "transition": "fade"},
        {"id": "to_sunkbell_s", "at": {"tx": 31, "ty": 15}, "trigger": "step_on",
         "to_map": "sunkbell_shallows", "to": {"tx": 1, "ty": 8}, "facing": "right",
         "requires_ability": "tidecall", "transition": "fade"},
    ],
    "npcs": [
        # E1 "The Quiet Reeds" — the fen fisher, four flag-disjoint stages on
        # her jetty (the standing giver-swap kit).
        {"id": "fen_fisher", "at": {"tx": 25, "ty": 27}, "facing": "down",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.fen_fisher",
         "hidden_when_flag": "flag:q_east_reeds"},
        {"id": "fen_fisher_wait", "at": {"tx": 25, "ty": 27}, "facing": "down",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "npc.fen_fisher_wait",
         "requires_flag": "flag:q_east_reeds",
         "hidden_when_flag": "flag:q_east_reed_third"},
        {"id": "fen_fisher_report", "at": {"tx": 25, "ty": 27}, "facing": "down",
         "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.fen_fisher_report",
         "requires_flag": "flag:q_east_reed_third",
         "hidden_when_flag": "flag:q_east_reeds_done"},
        {"id": "fen_fisher_after", "at": {"tx": 25, "ty": 27}, "facing": "down",
         "sprite": "npc_old_woman", "movement": "look_around",
         "dialogue_ref": "npc.fen_fisher_after",
         "requires_flag": "flag:q_east_reeds_done"},
    ],
    "gates": [],
    "encounters": [],
    "triggers": [],
    # The lantern-reed line (objects): LIT ambience along the channels, ONE
    # ambient snuffed reed by the crossing (the silent foreshadow — deco only,
    # no dialogue), and the three QUEST reeds. Reeds A/B swap dark→lit on
    # their flags (MapObject requires/hidden — the §8 pattern); reed C never
    # lights. All share footprints, so collision stays constant.
    "objects": [
        # ambience: lit reeds the fen still keeps
        {"id": "reed_lit_1", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 12, "ty": 33}, "w": 1, "h": 2, "overhang": 1},
        {"id": "reed_lit_2", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 6, "ty": 24}, "w": 1, "h": 2, "overhang": 1},
        {"id": "reed_lit_3", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 19, "ty": 20}, "w": 1, "h": 2, "overhang": 1},
        {"id": "reed_lit_4", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 26, "ty": 26}, "w": 1, "h": 2, "overhang": 1},
        # THE silent foreshadow: one dead reed-lamp among the glowing ones
        {"id": "reed_snuffed", "sprite": "saltreach_reed_lantern_dark",
         "at": {"tx": 8, "ty": 33}, "w": 1, "h": 2, "overhang": 1},
        # E1 reed A (near, jetty isle): dark -> lit on flag:q_east_reed_a
        {"id": "reed_a_dark", "sprite": "saltreach_reed_lantern_dark",
         "at": {"tx": 22, "ty": 26}, "w": 1, "h": 2, "overhang": 1,
         "hidden_when_flag": "flag:q_east_reed_a"},
        {"id": "reed_a_lit", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 22, "ty": 26}, "w": 1, "h": 2, "overhang": 1,
         "requires_flag": "flag:q_east_reed_a"},
        # E1 reed B (mid-water isle): dark -> lit on flag:q_east_reed_b
        {"id": "reed_b_dark", "sprite": "saltreach_reed_lantern_dark",
         "at": {"tx": 13, "ty": 12}, "w": 1, "h": 2, "overhang": 1,
         "hidden_when_flag": "flag:q_east_reed_b"},
        {"id": "reed_b_lit", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 13, "ty": 12}, "w": 1, "h": 2, "overhang": 1,
         "requires_flag": "flag:q_east_reed_b"},
        # E1 reed C (the treeline reed): it will NOT light. It stays dark.
        {"id": "reed_c_dark", "sprite": "saltreach_reed_lantern_dark",
         "at": {"tx": 19, "ty": 6}, "w": 1, "h": 2, "overhang": 1},
    ],
    "music": "assets/audio/music/saltreach-fen-b.mp3",
})

# E1: the three reed interact chains (base tile of each reed object). Order
# matters within a tile: the quest stage first, the post-state after it.
m["triggers"] += [
    # reed A — the near reed (channel order starts here)
    {"id": "reed_a_do", "kind": "script", "at": {"tx": 22, "ty": 27},
     "activation": "interact", "ref": "script.reed_first", "once": True,
     "requires_flag": "flag:q_east_reeds", "blocked_ref": "npc.reed_unasked",
     "sets_flags": ["flag:q_east_reed_a"], "hidden_when_flag": "flag:q_east_reed_a"},
    {"id": "reed_a_lit_t", "kind": "sign", "at": {"tx": 22, "ty": 27},
     "activation": "interact", "ref": "npc.reed_lit_a",
     "requires_flag": "flag:q_east_reed_a"},
    # reed B — mid-water (refused until A burns: a line lights from home outward)
    {"id": "reed_b_do", "kind": "script", "at": {"tx": 13, "ty": 13},
     "activation": "interact", "ref": "script.reed_second", "once": True,
     "requires_flag": "flag:q_east_reed_a", "blocked_ref": "npc.reed_order",
     "sets_flags": ["flag:q_east_reed_b"], "hidden_when_flag": "flag:q_east_reed_b"},
    {"id": "reed_b_lit_t", "kind": "sign", "at": {"tx": 13, "ty": 13},
     "activation": "interact", "ref": "npc.reed_lit_b",
     "requires_flag": "flag:q_east_reed_b"},
    # reed C — the third will not light (the SILENT B2 foreshadow)
    {"id": "reed_c_do", "kind": "script", "at": {"tx": 19, "ty": 7},
     "activation": "interact", "ref": "script.reed_third", "once": True,
     "requires_flag": "flag:q_east_reed_b", "blocked_ref": "npc.reed_order",
     "sets_flags": ["flag:q_east_reed_third"], "hidden_when_flag": "flag:q_east_reed_third"},
    {"id": "reed_c_dark_t", "kind": "sign", "at": {"tx": 19, "ty": 7},
     "activation": "interact", "ref": "npc.reed_dark_third",
     "requires_flag": "flag:q_east_reed_third"},
]

# the route's one sight trainer holds the treeline neck (boulder chokes col 15)
owed += pt.trainer_beat(m, tid="reed_lamplighter", at=(16, 3), facing="down",
                        sight=4, sprite="npc_man")

# caches (variety rule): the tide-walk Moth-amber, a wicks tin off the jetty,
# balms by the landing
owed += pt.cache(m, cid="fen_isle_amber", at=(4, 14))
owed += pt.cache(m, cid="fen_ii_wicks", at=(27, 29))
owed += pt.cache(m, cid="fen_ii_balm", at=(12, 40))

# signs: the landing, the Sunkbell turn-off, the treeline
owed += pt.sign(m, deco, W, sid="fen_ii_landing", at=(13, 40))
owed += pt.sign(m, deco, W, sid="sunkbell_turnoff", at=(27, 27))
owed += pt.sign(m, deco, W, sid="fen_ii_treeline", at=(13, 2))

# encounter zones FROM the paint (band 17-19, hooks §6): the reed isles…
FEN2_TABLE = [
    {"kin_id": 59, "weight": 40, "min_level": 17, "max_level": 19},  # Dewling
    {"kin_id": 31, "weight": 25, "min_level": 17, "max_level": 19},  # Lumpin
    {"kin_id": 27, "weight": 20, "min_level": 17, "max_level": 19},  # Brineroll
    {"kin_id": 60, "weight": 15, "min_level": 18, "max_level": 19},  # Poolfrond
]
m["encounters"] = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass",
                                     rate=0.10, table=FEN2_TABLE, id_prefix="reed")
# …and the parted channels themselves (water rolls only on water tiles)
m["encounters"].append(
    {"id": "channels", "terrain": "water", "rect": {"tx": 1, "ty": 8, "w": 30, "h": 31},
     "encounter_rate": 0.06, "requires_ability": "tidecall",
     "table": [{"kin_id": 31, "weight": 40, "min_level": 17, "max_level": 19},
               {"kin_id": 27, "weight": 35, "min_level": 17, "max_level": 19},
               {"kin_id": 60, "weight": 25, "min_level": 18, "max_level": 19}]})

# dry-bank trees with real shape (§11 rule 2)
pt.crown_tree(m, oid="landing_tree", sprite="tinderwick_tree", at=(19, 39))
pt.crown_tree(m, oid="north_tree", sprite="tinderwick_tree", at=(5, 1))
pt.crown_tree(m, oid="north_tree_e", sprite="tinderwick_tree", at=(24, 1))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

mk.scatter_decor(deco, base, W, H, rng, density=0.10,
                 avoid={(x, y) for y in range(H) for x in range(W)
                        if path[y * W + x] or tallgrass[y * W + x] or water[y * W + x]
                        or sand[y * W + x] or tree[y * W + x]})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
