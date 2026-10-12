#!/usr/bin/env python3
"""
Build Wrackline Path — the Pearlmoor-side leg of the new Pearlmoor <-> Vesper
Crossroads route (REPLACES the bare lanternway_pearlmoor lane). A coastal cliff
path that descends south along the bay's EAST shore: sea off the WEST (the bay
between Dimglass and here), a tree-cliff wall to the EAST. The 2026-10 geometry fix
turned it into a true north->south leg: it comes in at the TOP from Saltreach Fen I
(the old drowned road surfacing past the lagoon) and leaves at the BOTTOM into the
Sounding Cave, so the loop home is compass-true. Level band 15-18 (a notch above
Pearlmoor).

TRAVERSAL PASS (2026-10, 09-the-wild-ways §3) — THE WRACK CUT. The path used to
be a grass corridor you walked straight down. Now a sea-cut gully (the Wrack
Cut) slices the headland east-west, and the old wrack-haulers' TRESTLE spans it.
The way down crosses OVER the cut and comes back UNDER it:

  1. the north meadow -> over the trestle (wildkit.deck, axis v, under=True —
     the deck sits in the `above` layer) onto the south bank;
  2. west across the bank (a mandatory grass band) to the shore, and north up
     the strand into the cut's sea mouth;
  3. east along the cut's shingle floor, UNDER the trestle you just crossed
     (one pass-through move; the deck is drawn over you), to the cut's head;
  4. the head turns south down a narrow ravine (the second mandatory band, the
     drifter posted at its head) to the Sounding Cave.

Both directions walk the same loop (no one-way pieces, so nobody is ever
stranded); the trestle and the underpass are the route. With Tidecall a swimmer
can slip round the strand into the cut's mouth — still the cut, the ravine
band and the drifter's eye, so no encounter-free pass.

Chain:  saltreach_fen_i (south exit) -> wrackline_path -> sounding_cave -> ...

Run:  python3 tools/maps/build_wrackline_path.py   (after build_shared_overworld.py)
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 16, 26
rng = random.Random(47)

m: dict = {
    "id": "wrackline_path", "display_name": "Wrackline Path", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/dimglass-coast-b.mp3",
}
wk.use_traverse(m)

# ---- terrain presence grids -------------------------------------------------
# EAST tree wall (2 deep); WEST sea with a sand strand; the Wrack Cut across the
# middle; the ravine down the east side to the cave.
tree = mk.make_grid(W, H)
mk.organic_border(tree, W, H, top=1, right=1, depth=2, bumps=[(13, 3, 1), (3, 1, 1)])
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)             # south border
TOP, BOT = (8, 9), (13, 14)
for x in TOP:
    for y in (0, 1):
        tree[y * W + x] = 0
for x in BOT:
    for y in (H - 2, H - 1):
        tree[y * W + x] = 0

water = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 2, 1, H - 3)                    # sea off the west
mk.blob(water, W, H, 1, 6, 1.4, 2.0)
mk.blob(water, W, H, 1, 19, 1.2, 1.8)
sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 2, 2, 2, H - 3)                     # the strand
mk.blob(sand, W, H, 2, 7, 1.4, 1.6)

# THE WRACK CUT: a north wall (rim + face, rows 10-11) over a one-row shingle
# floor (row 12) that opens to the sea, and a south lip (rows 13-14). Its head
# (cols 12-13) turns south as the ravine, walled from the south bank by a
# two-wide wooded spine (cols 10-11) all the way down to the south treeline.
CUT_N, CUT_FLOOR, CUT_S = (10, 11), 12, (13, 14)
cliff = mk.make_grid(W, H)
for y in CUT_N:
    mk.hline(cliff, W, H, y, 2, 13)
for y in CUT_S:
    mk.hline(cliff, W, H, y, 3, 11)
for y in range(CUT_S[1] + 1, H - 2):
    for x in (10, 11):
        tree[y * W + x] = 1                          # the wooded spine
RAVINE = {(x, y) for x in (12, 13) for y in range(CUT_FLOOR, H - 2)}
for (x, y) in RAVINE:
    tree[y * W + x] = 0
FLOOR = {(x, CUT_FLOOR) for x in range(2, 14)}
for (x, y) in FLOOR:
    sand[y * W + x] = 1                                  # wrack shingle

# THE TRESTLE: N-S over the cut at cols 8-9, rows 10-14; walk its length, or
# pass beneath it along the floor. Deck art in `above` (you go under it).
above = mk.make_grid(W, H)
deco = mk.make_grid(W, H)
TRESTLE = (8, 10, 2, 5)
wk.deck(m, above, W, rect=TRESTLE, axis="v", sid="wrack_trestle", under=True)
for x in (8, 9):
    deco[CUT_FLOOR * W + x] = wk.T("under_shade")         # its shadow on the floor
TRESTLE_CELLS = {(x, y) for x in (8, 9) for y in range(10, 15)}

# the lane: down the north meadow to the trestle; off it, west across the bank;
# the ravine path down to the cave.
path = mk.make_grid(W, H)
LANE = set()
for y in range(0, 10):
    LANE |= {(8, y), (9, y)}
for x in range(6, 10):
    LANE |= {(x, 15), (x, 16)}
for (x, y) in RAVINE:
    LANE.add((x, y))
for y in (H - 2, H - 1):
    LANE |= {(13, y), (14, y)}
for (x, y) in LANE:
    path[y * W + x] = 1

# two MANDATORY grass bands — the bank's full height (cols 4-5: every way from
# the trestle to the strand) and the ravine's full width (rows 17-18) — plus an
# optional patch in the north meadow.
tallgrass = mk.make_grid(W, H)
pt.mandatory_band(tallgrass, path, W, H, y0=15, y1=H - 3, x0=4, x1=5)
pt.mandatory_band(tallgrass, path, W, H, y0=17, y1=18, x0=12, x1=13)
mk.blob(tallgrass, W, H, 5.0, 6.5, 1.8, 1.8)

# precedence: structure wins
for i in range(W * H):
    x, y = i % W, i // W
    if cliff[i]:
        tree[i] = sand[i] = path[i] = tallgrass[i] = water[i] = 0
    if water[i]:
        sand[i] = path[i] = tallgrass[i] = 0
    if tree[i]:
        sand[i] = path[i] = tallgrass[i] = 0
    if (x, y) in FLOOR:
        tallgrass[i] = path[i] = 0

# ---- base + terrain layers --------------------------------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

# ---- objects: crown trees + lamp breadcrumbs --------------------------------
m["objects"] = [
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 11, "ty": 3}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 6, "ty": 19}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 3, "ty": 2}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 7, "ty": 4}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 10, "ty": 7}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 7, "ty": 15}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_d", "sprite": "tinderwick_lamp_post", "at": {"tx": 9, "ty": 19}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = {(x, y) for o in m["objects"]
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(gr[y * W + x] for gr in (tree, water, sand, tallgrass, path, cliff))}
avoid = covered | building_cells | TRESTLE_CELLS | FLOOR

# ---- deco: boulders, scatter ------------------------------------------------
for (x, y) in [(3, 8), (12, 8), (7, 21), (3, 21)]:
    deco[y * W + x] = gid("boulder")

# scatter only beside the lit lane (keeps the open field clean)
near_path = set()
for y in range(H):
    for x in range(W):
        if path[y * W + x]:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    near_path.add((x + dx, y + dy))
scatter_avoid = avoid | {(x, y) for y in range(H) for x in range(W) if (x, y) not in near_path}
mk.scatter_decor(deco, base, W, H, rng, density=0.12, avoid=scatter_avoid)

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + \
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": above}]
m["warps"] = [
    # TOP: <-> Saltreach Fen I's south exit (the drowned road). Lands one row
    # IN from the fen's return warps; a warp on each tile of the 2-wide gap.
    {"id": "to_fen", "at": {"tx": 8, "ty": 0}, "trigger": "step_on",
     "to_map": "saltreach_fen_i", "to": {"tx": 20, "ty": 42}, "facing": "up", "transition": "fade"},
    {"id": "to_fen_e", "at": {"tx": 9, "ty": 0}, "trigger": "step_on",
     "to_map": "saltreach_fen_i", "to": {"tx": 21, "ty": 42}, "facing": "up", "transition": "fade"},
    # BOTTOM: the Sounding Cave's north mouth (door). Lands one tile IN.
    {"id": "to_cave", "at": {"tx": 13, "ty": H - 1}, "trigger": "step_on",
     "to_map": "sounding_cave", "to": {"tx": 12, "ty": 1}, "facing": "down", "transition": "door"},
    {"id": "to_cave_e", "at": {"tx": 14, "ty": H - 1}, "trigger": "step_on",
     "to_map": "sounding_cave", "to": {"tx": 12, "ty": 1}, "facing": "down", "transition": "door"},
]

# ---- stamps that need `m` (signs, cache, trainer) ---------------------------
owed = []
owed += pt.sign(m, deco, W, sid="wrackline_view", at=(10, 5))
owed += pt.sign(m, deco, W, sid="wrackline_cave", at=(12, 23))
owed += pt.cache(m, cid="wrackline_balm", at=(10, 6))
# the sight trainer at the cut's head, facing up the ravine's west lane: every
# way between the cut floor and the ravine walks (12,12)-(12,13)
owed += pt.trainer_beat(m, tid="wrackline_drifter", at=(12, 14), facing="up", sight=2,
                        sprite="npc_man")

# encounter zones from the painted tall-grass (mandatory bands + patches), 15-18
m["encounters"] = pt.zones_from_grid(
    tallgrass, W, H, terrain="tall_grass", rate=0.11, id_prefix="grass",
    table=[{"kin_id": 31, "weight": 45, "min_level": 15, "max_level": 18},
           {"kin_id": 26, "weight": 35, "min_level": 15, "max_level": 17},
           {"kin_id": 53, "weight": 20, "min_level": 16, "max_level": 18}])

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
