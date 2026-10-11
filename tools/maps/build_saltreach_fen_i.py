#!/usr/bin/env python3
"""
Saltreach Fen I — brackish reed marsh under glinting mist (walkthrough/02-east).

RECOMPOSED 2026-10 (the world-craft panel's follow-up richness pilot, §4 #1):
the old build read as "a lawn with rectangles in it" (0.32 props/screen, 0
scripted beats). Same skeleton and contracts — every warp, landing, trainer
tile + sight line, cache, sign and the encounter TABLE/RATE are unchanged —
but the fen is now a fen:

  * organic, noise-edged pools joined by REED CHANNELS (the causeway crosses
    them on boardwalks), a south-east LAGOON where the old drowned road runs a
    line of ruined lamp-posts down into the water;
  * the reed-cutter's STILT HUT over the west pool (+ punt, net-rack, reed
    stooks, mooring stakes, eel traps) — "the fishing-stilt nook": an old
    eel-wife tells one fen story, and inspecting her net-weights turns up a
    tin under the boards (optional find, no required step);
  * the LOST VILLAGE: three dark lantern-reeds lit from home outward lead to
    a drowned cottage whose name you can read once the line is lit (lore);
  * shore reed-beds (cattails) and lily-pads hide the pond family's square
    corners — the pond terrain has no inner corners, so props round the shore.

Post-build additions it now OWNS (so re-running is safe): the Wayfarer's purse
cache. Re-run tools/maps/add_peril_thread.py (the leaver + bundles) and
tools/maps/add_world_craft.py --region east (ambience + ambient kin) after.

Run:  ./venv/bin/python tools/maps/build_saltreach_fen_i.py
"""
from __future__ import annotations
import math
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 32, 44
rng = random.Random(71)
owed: list[str] = []

# ---- terrain grids ---------------------------------------------------------------
tree = mk.make_grid(W, H)       # the marsh's wooded enclosure
pond = mk.make_grid(W, H)       # marsh pools + reed channels (water-over-grass)
tallgrass = mk.make_grid(W, H)  # reed beds (the encounter terrain)
cliff = mk.make_grid(W, H)      # the raised east bank's rim
path = mk.make_grid(W, H)       # the causeway spine


def fen_pool(g, cx, cy, rx, ry, seed, wob=0.22):
    """A noise-edged pool: an ellipse whose radius wobbles with angle (two low
    harmonics), so shores read as bays and spits, not a stamped oval."""
    r = random.Random(seed)
    a1, a2 = r.uniform(0, 6.28), r.uniform(0, 6.28)
    for y in range(int(cy - ry - 2), int(cy + ry + 3)):
        for x in range(int(cx - rx - 2), int(cx + rx + 3)):
            if not (0 <= x < W and 0 <= y < H):
                continue
            dx, dy = (x - cx) / rx, (y - cy) / ry
            ang = math.atan2(dy, dx)
            k = 1 + wob * math.sin(2 * ang + a1) + wob * 0.6 * math.sin(3 * ang + a2)
            if dx * dx + dy * dy <= k * k:
                g[y * W + x] = 1


def channel(g, pts, width=1):
    """A meandering reed channel through waypoints (1-2 tiles wide)."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0)) * 2 + 1
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n)
            y = round(y0 + (y1 - y0) * i / n)
            for dx in range(width):
                if 0 <= x + dx < W and 0 <= y < H:
                    g[y * W + x + dx] = 1


# enclosure: organic tree border, bottom sealed too (off-map = continuation)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(7, 2, 3), (26, 3, 3), (1, 18, 2), (30, 36, 3), (29, 12, 2)],
                  rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)

# pools — the fen's water, noise-edged
fen_pool(pond, 13.5, 40.6, 4.2, 1.7, 1)        # south pool by the landing
fen_pool(pond, 21.5, 36.2, 5.6, 2.9, 2)        # the SE lagoon (the drowned road)
fen_pool(pond, 5.8, 27.4, 3.9, 2.4, 3)         # the stilt-hut pool (west)
fen_pool(pond, 16.0, 28.6, 4.0, 2.0, 4)        # the centre pool
fen_pool(pond, 9.6, 16.8, 2.8, 1.9, 5)         # the reed-mere by the bank turn-off
fen_pool(pond, 24.0, 8.6, 4.4, 2.6, 6)         # the north-east mere
fen_pool(pond, 5.0, 7.0, 2.6, 2.0, 7)          # the north-west mere
# the DEEP-CHANNEL tease east of the fork (Tidecall visibly wanted — and held)
fen_pool(pond, 27.0, 29.0, 3.0, 4.0, 8, wob=0.15)
# reed channels joining the waters (the causeway crosses them on boardwalks)
channel(pond, [(9, 28), (11, 29), (13, 29)])               # hut pool -> centre pool
channel(pond, [(19, 29), (21, 31), (21, 33)])              # centre pool -> lagoon
channel(pond, [(6, 9), (7, 12), (8, 15)])                  # NW mere -> reed-mere
channel(pond, [(27, 33), (27, 34)], width=1)               # deep finger -> lagoon
# the BOUNDARY channel: a full-width water band before the Fen II exit
fen_pool(pond, 16.0, 3.6, 15.0, 1.25, 9, wob=0.06)
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

# the raised EAST BANK: cliff rim, ledge lip south, entered via the west gap
BANK = pt.Area(18, 13, 28, 21)
pt.terrace(cliff, mk.make_grid(W, H), W, H, BANK, gap=(17, 18), gap_side="left", rng=rng)

# reed beds — the same four beds (the big mid bed STRADDLES the lane: the
# mandatory crossing), the west verge beds pay the off-lane strip
mk.blob(tallgrass, W, H, 17.5, 40, 3.0, 1.6)
mk.blob(tallgrass, W, H, 6.5, 34, 2.8, 1.4)
mk.blob(tallgrass, W, H, 13, 22, 4.2, 2.3)
mk.blob(tallgrass, W, H, 8, 12, 3, 2)
mk.blob(tallgrass, W, H, 3.5, 7, 1.6, 2.0)
mk.blob(tallgrass, W, H, 3.5, 14, 1.5, 1.6)

# warp openings carved out of the enclosure (west entry, north exit)
for (x, y) in [(0, 37), (0, 38), (1, 37), (1, 38), (15, 0), (16, 0), (15, 1), (16, 1)]:
    tree[y * W + x] = 0

# keep dry: the islet under its cache, the hut-pool's east shore by the
# eel-wife, the lantern-reed footings + the ruin's reading spot, the trainer
# sight lines, and the cache/sign tiles
DRY = {(27, 29), (26, 29), (9, 25), (10, 25), (9, 24), (10, 24),
       (14, 37), (19, 38), (23, 39), (24, 41), (25, 41), (26, 41), (23, 40), (22, 39),
       (19, 41), (22, 16), (2, 30), (3, 39), (20, 29), (14, 6), (8, 30), (7, 31), (8, 31),
       (5, 32), (6, 32), (7, 32), (4, 37), (5, 41), (6, 41), (7, 41)}
for (x, y) in DRY:
    pond[y * W + x] = 0
# the drowned cottage stands half IN the lagoon's east shore
for (x, y) in [(24, 37), (25, 37), (24, 38), (25, 38)]:
    pond[y * W + x] = 1

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

# planks: dock boards where the causeway bridges a pool neck or a reed channel
for i in range(W * H):
    if path[i]:
        x, y = i % W, i // W
        neighbours_water = sum(
            1 for (nx, ny) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
            if 0 <= nx < W and 0 <= ny < H and pond[ny * W + nx])
        if neighbours_water >= 2:
            deco[i] = gid("dock")
# lantern-buoys marking the deep water
for (x, y) in [(29, 27), (12, 41), (25, 7), (16, 4)]:
    if pond[y * W + x]:
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
        # north: across the Tidecall channel to Fen II
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
         "sprite": "old_salt", "movement": "look_around",
         "dialogue_ref": "npc.fen_warden"},
        # the fishing-stilt nook (world-craft §4 #1b): the reed-cutter's eel-wife
        {"id": "fen_eelwife", "at": {"tx": 9, "ty": 25}, "facing": "left",
         "sprite": "fen_folk", "movement": "look_around",
         "dialogue_ref": "script.fen_eelwife"},
    ],
    "gates": [],
    "encounters": [],
    "triggers": [],
    "objects": [],
    "music": "assets/audio/music/saltreach-fen-a.mp3",
})

# sight-trainer beats on the causeway (level-design §11 rule 7)
owed += pt.trainer_beat(m, tid="fen_wader_a", at=(11, 26), facing="down",
                        sight=4, sprite="fisher_woman")
owed += pt.trainer_beat(m, tid="fen_courier_b", at=(14, 10), facing="left",
                        sight=4, sprite="road_courier")

# caches (variety rule): a charge behind the reed screen [MISSABLE], the
# bank's wicks purse (ledge shelf), the Tidecall islet's balm, the
# Wayfarer's purse by the hut pool (post-build addition, now owned here)
owed += pt.cache(m, cid="fen_reed", at=(19, 41))
owed += pt.cache(m, cid="fen_bank_wicks", at=(22, 16))
owed += pt.cache(m, cid="fen_islet", at=(27, 29))
owed += pt.cache(m, cid="fen_purse", at=(2, 30))
m["npcs"][-1]["id"] = "cache_purse"  # the shipped id (save-compatible)
# the eel-wife's net-weights find: appears once you've looked under the boards
owed += pt.cache(m, cid="fen_netweights", at=(8, 30))
m["npcs"][-1]["requires_flag"] = "flag:fen_netweights_seen"

# signs: the landing, the channel tease at the fork's end, the boundary
owed += pt.sign(m, deco, W, sid="fen_landing", at=(3, 39))
owed += pt.sign(m, deco, W, sid="fen_channel", at=(20, 29))
owed += pt.sign(m, deco, W, sid="fen_boundary", at=(14, 6))

# encounter zones — the SHIPPED tables, verbatim (night tables + the R4
# day-form pairs; mirrored in build_species EXTRA_ENCOUNTERS — never retune
# here). The rects are loose bounding boxes over the painted reed beds (the
# engine only rolls tall_grass ON painted tiles); reed_c/reed_d widened by a
# column/row to cover the re-blobbed beds.
NIGHT = [{"kin_id": 59, "weight": 40, "min_level": 16, "max_level": 18},
         {"kin_id": 27, "weight": 25, "min_level": 16, "max_level": 18},
         {"kin_id": 60, "weight": 15, "min_level": 17, "max_level": 18},
         {"kin_id": 47, "weight": 15, "min_level": 16, "max_level": 18}]
DAY = [{"kin_id": 59, "weight": 35, "min_level": 55, "max_level": 61},
       {"kin_id": 27, "weight": 20, "min_level": 55, "max_level": 61},
       {"kin_id": 60, "weight": 12, "min_level": 56, "max_level": 62},
       {"kin_id": 67, "weight": 8, "min_level": 57, "max_level": 63}]
RECTS = {"reed_a": (2, 7, 9, 9), "reed_b": (9, 20, 9, 5),
         "reed_c": (4, 32, 6, 4), "reed_d": (15, 39, 6, 3)}
m["encounters"] = (
    [{"id": z, "terrain": "tall_grass", "rect": dict(zip(("tx", "ty", "w", "h"), r)),
      "encounter_rate": 0.1, "table": NIGHT, "hidden_when_flag": "flag:dawn"}
     for z, r in RECTS.items()] +
    [{"id": f"{z}_day", "terrain": "tall_grass", "rect": dict(zip(("tx", "ty", "w", "h"), r)),
      "encounter_rate": 0.1, "table": DAY, "requires_flag": "flag:dawn"}
     for z, r in RECTS.items()])
# every painted reed tile must sit inside some zone rect (or it never rolls)
_cov = {(x, y) for (rx, ry, rw, rh) in RECTS.values()
        for y in range(ry, ry + rh) for x in range(rx, rx + rw)}
_out = [(i % W, i // W) for i in range(W * H) if tallgrass[i] and (i % W, i // W) not in _cov]
assert not _out, f"reed tiles outside every zone: {_out}"


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


# a few dry-bank trees with real shape (§11 rule 2)
pt.crown_tree(m, oid="bank_tree", sprite="tinderwick_tree", at=(24, 15))
pt.crown_tree(m, oid="south_tree", sprite="tinderwick_tree", at=(22, 23))
pt.crown_tree(m, oid="mere_tree", sprite="tinderwick_tree", at=(18, 6))
pt.crown_tree(m, oid="verge_tree", sprite="tinderwick_tree", at=(1, 20))

# --- the fishing-stilt nook (west): hut over the pool, punt, nets, stooks ---
obj("reedcutter_hut", "saltreach_reedcutter_hut", (4, 21), 5, 5, overhang=3)
obj("hut_punt", "saltreach_punt", (2, 26), 2, 3, solid=False)
obj("hut_netrack", "saltreach_net_rack", (5, 31), 3, 2, overhang=1, walk_under=True)
obj("hut_stooks", "saltreach_reed_stooks", (9, 19), 2, 2, overhang=1, walk_under=True)
obj("hut_moorings", "saltreach_mooring_posts", (9, 27), 1, 2, overhang=1, walk_under=True)
obj("eel_trap_a", "saltreach_eel_trap", (7, 14), 2, 2, overhang=1, walk_under=True, solid=False)
obj("eel_trap_b", "saltreach_eel_trap", (19, 26), 2, 2, overhang=1, walk_under=True, solid=False)
obj("eel_trap_c", "saltreach_eel_trap", (2, 9), 2, 2, overhang=1, walk_under=True, solid=False)
obj("eel_trap_d", "saltreach_eel_trap", (21, 11), 2, 2, overhang=1, walk_under=True, solid=False)
# the heron stakes on the open flat between the lane and the bank (a perch,
# not a wall — the flat's focal point)
obj("heron_stakes", "saltreach_mooring_posts", (15, 14), 1, 2, overhang=1, walk_under=True)
obj("flat_stooks", "saltreach_reed_stooks", (13, 12), 2, 2, overhang=1, walk_under=True)

# --- the drowned road: a ruined lamp-post line walking down into the lagoon ---
for k, (x, y) in enumerate([(13, 35), (16, 34), (18, 36), (21, 37)]):
    obj(f"drowned_lamp_{k}", "saltreach_sunken_lamp", (x, y - 2), 1, 3,
        overhang=2, walk_under=True, solid=False)
obj("lagoon_moorings", "saltreach_mooring_posts", (25, 33), 1, 2, overhang=1, walk_under=True,
    solid=False)

# --- the lost village: three dark lantern-reeds lit from home outward lead to
# the drowned cottage; each pair shares footprint + solidity (flag-blind collision)
LANTERNS = [(14, 36), (19, 37), (23, 38)]
for k, (x, y) in enumerate(LANTERNS, start=1):
    obj(f"lost_reed_{k}", "saltreach_reed_lantern_dark", (x, y), 1, 2, overhang=1,
        walk_under=True, hidden_when_flag=f"flag:fen_lostreed_{k}")
    obj(f"lost_reed_{k}_lit", "saltreach_reed_lantern_lit", (x, y), 1, 2, overhang=1,
        walk_under=True, requires_flag=f"flag:fen_lostreed_{k}")
    trig = {"id": f"lost_reed_{k}", "kind": "script", "at": {"tx": x, "ty": y + 1},
            "activation": "interact", "ref": f"script.fen_lostreed_{k}",
            "hidden_when_flag": f"flag:fen_lostreed_{k}"}
    if k > 1:
        trig["requires_flag"] = f"flag:fen_lostreed_{k - 1}"
        trig["blocked_ref"] = "npc.fen_lostreed_wait"
    m["triggers"].append(trig)
obj("drowned_cottage", "saltreach_drowned_cottage", (23, 37), 4, 4, overhang=2, walk_under=True)
m["triggers"].append({"id": "lost_village", "kind": "script", "at": {"tx": 25, "ty": 40},
                      "activation": "interact", "ref": "script.fen_lost_village"})
# the eel-wife's net-weights (the nook's find)
m["triggers"].append({"id": "net_weights", "kind": "script", "at": {"tx": 6, "ty": 32},
                      "activation": "interact", "ref": "script.fen_netweights"})

# --- shore dressing: lily-pads on open water, reed clumps on the pond's
# square corners (the pond family has no inner corners — props round them)
for k, (x, y) in enumerate([(4, 6), (14, 27), (20, 35), (23, 8), (15, 40), (26, 9)]):
    obj(f"lily_{k}", "saltreach_lilypads", (x, y), 2, 2, solid=False)

busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]}
busy |= {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
taken = set()
for o in m["objects"]:
    for yy in range(o["at"]["ty"], o["at"]["ty"] + o["h"]):
        for xx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
            taken.add((xx, yy))


def is_water(x, y):
    return 0 <= x < W and 0 <= y < H and pond[y * W + x]


corners = []
for y in range(3, H - 3):
    for x in range(2, W - 3):
        i = y * W + x
        if pond[i] or tree[i] or cliff[i] or path[i] or tallgrass[i] or y in (3, 4, 5):
            continue
        n = [is_water(x + 1, y), is_water(x - 1, y), is_water(x, y + 1), is_water(x, y - 1)]
        diag = sum(is_water(x + dx, y + dy) for dx in (-1, 1) for dy in (-1, 1))
        # an inner-corner shore cell: water on two orthogonal sides, or a lone
        # diagonal notch the autotile squares off
        if (n[0] or n[1]) and (n[2] or n[3]) or (sum(n) == 0 and diag >= 1):
            corners.append((x, y))
rng.shuffle(corners)
placed = []
for (x, y) in corners:
    # the clump's 2x2 box sits with its base row ON the corner cell
    ax, ay = x - (1 if is_water(x - 1, y) else 0), y - 1
    cells = {(ax, ay), (ax + 1, ay), (ax, ay + 1), (ax + 1, ay + 1)}
    if cells & taken or cells & busy:
        continue
    if any(path[cy * W + cx] for (cx, cy) in cells if 0 <= cx < W and 0 <= cy < H):
        continue
    if any(abs(ax - px) + abs(ay - py) < 4 for (px, py) in placed):
        continue
    placed.append((ax, ay))
    taken |= cells
    obj(f"cattails_{len(placed)}", "saltreach_cattails", (ax, ay), 2, 2, overhang=1,
        walk_under=True, solid=False)
    if len(placed) >= 16:
        break

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

mk.scatter_decor(deco, base, W, H, rng, density=0.16, flowers=0.05,
                 avoid={(x, y) for y in range(H) for x in range(W)
                        if path[y * W + x] or tallgrass[y * W + x] or pond[y * W + x]
                        or cliff[y * W + x] or tree[y * W + x]})

if __name__ == "__main__":
    print(f"reed-bed (encounter) tiles: {sum(tallgrass)} (was 82; keep 70-94)")
    print(f"objects: {len(m['objects'])}")
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
