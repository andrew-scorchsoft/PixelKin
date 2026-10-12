#!/usr/bin/env python3
"""
The Wick-Run: Upper Chute (09-the-wild-ways §2 A; kind route, region west,
band 46-48, `ride: true`). The first real drop of the old wax road.

The traversal kit's teaching map — one new idea per screen (§3a r5):
  1. THE START LINE (rows 0-4): a flat landing under the crest; crossing row 4
     starts the run clock (`script.wickrun_start`). Then the CHUTE: you're
     carried downhill every step, left/right steers, and there's no pedalling
     back up — the run is one-way, which is why the Tallow Lift exists.
  2. THE FORK (rows 13-30): a wide steering bowl, then a pine-and-rock island
     splits the road. WEST LINE: a flat landing with grass and a Runner who
     calls you out (stop, fight, breathe). EAST LINE: faster, with a kicker
     that leaps a boulder, and a side-ramp that clears a crevice onto a
     ledge you can SEE from the bowl (§3a r3) — the cache only riders reach;
     the ledge drains back into the line by its own little chute.
  3. THE RUN-OUT (rows 31-35): the lines rejoin on a flat shelf (grass,
     the second Runner, a sign) before the last drop to the trestles.

HANDSHAKE: north `to_crest`/`_e` (13,0)/(14,0) <-> wickrun_crest (10,27)/(11,27);
south `to_trestles`/`_e` (4,43)/(5,43) -> wickrun_trestles (23,0)/(24,0).
Geometry: x -8..20, y -238..-194.

Run:  python3 tools/maps/build_wickrun_chute.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 28, 44
rng = random.Random(9062)
owed: list[str] = []

tree = mk.make_grid(W, H)
path = mk.make_grid(W, H)
tallgrass = mk.make_grid(W, H)
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)

# Start from a solid wooded mountainside; carve the road out of it.
mk.rect(tree, W, H, 0, 0, W - 1, H - 1)
OPEN: set[tuple[int, int]] = set()


def carve(x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            OPEN.add((x, y))


carve(10, 1, 17, 4)          # the start landing
carve(13, 0, 14, 0)          # the gate from the crest
carve(10, 5, 17, 12)         # chute A + its verges
carve(4, 13, 23, 14)         # the steering bowl
carve(4, 15, 10, 19)         # west line, upper
carve(3, 20, 10, 25)         # west landing (flat)
carve(4, 26, 10, 30)         # west line, lower
carve(17, 15, 22, 30)        # east line (+ its west verge)
carve(24, 16, 26, 20)        # the ledge pocket (flat)
carve(25, 21, 25, 30)        # the ledge's drain chute
carve(2, 31, 26, 35)         # the run-out shelf
carve(2, 36, 8, 42)          # the last drop + verges
carve(4, 43, 5, 43)          # the exit
for (x, y) in OPEN:
    tree[y * W + x] = 0

pin: dict = {}
m: dict = {
    "id": "wickrun_chute", "display_name": "The Wick-Run",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/wickrun.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/wickrun-a.webp",
                         "assets/backgrounds/battle/wickrun-b.webp"],
    "ride": True,
}
wk.use_traverse(m)

# ---- the chutes (slope flows + art) ---------------------------------------------
def cells(x0, y0, x1, y1):
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}


wk.chute(m, pin, deco, W, cells(12, 5, 15, 12), "down", fid="chute_a")
wk.chute(m, pin, deco, W, cells(5, 13, 22, 14), "down", fid="bowl", berms=False, chevrons=0)
wk.chute(m, pin, deco, W, cells(6, 15, 8, 19), "down", fid="west_upper")
wk.chute(m, pin, deco, W, cells(6, 26, 8, 30), "down", fid="west_lower")
wk.chute(m, pin, deco, W, cells(18, 15, 22, 30), "down", fid="east_line")
wk.chute(m, pin, deco, W, cells(25, 21, 25, 30), "down", fid="ledge_drain", berms=False, chevrons=3)
wk.chute(m, pin, deco, W, cells(4, 36, 6, 42), "down", fid="last_drop")

# the kickers: a side-ramp off the east line onto the ledge (over the crevice
# at x23), and a boulder-leap further down the line
wk.jump(m, deco, W, at=(22, 18), dir="right", length=3, jid="ledge_kicker")
wk.jump(m, deco, W, at=(20, 23), dir="down", length=3, jid="boulder_kicker")
deco[24 * W + 20] = gid("boulder")          # the boulder the kicker clears
OPEN.discard((20, 24))

# flat ground: the landing, the west landing, the ledge pocket, the run-out
LANE = cells(12, 0, 15, 4) | cells(5, 20, 9, 25) | cells(24, 16, 26, 20) | cells(3, 31, 26, 35)
for (x, y) in LANE:
    path[y * W + x] = 1
path[43 * W + 4] = path[43 * W + 5] = 1
for (x, y) in cells(4, 0, 9, 0) | cells(18, 0, 23, 0):
    pass

# grass: the west landing's bed + a patch at each end of the run-out (the
# run-out's middle stays a dry lane — riders can roll through)
for (x, y) in cells(3, 21, 5, 25):
    tallgrass[y * W + x] = 1
    path[y * W + x] = 0
mk.blob(tallgrass, W, H, 23.5, 33.0, 2.6, 1.6)
mk.blob(tallgrass, W, H, 11.0, 34.0, 2.4, 1.2)
for i in range(W * H):
    x, y = i % W, i // W
    if (x, y) not in OPEN or (x, y) in pin:
        tallgrass[i] = 0
    if tallgrass[i]:
        path[i] = 0
    if (x, y) in pin:
        path[i] = 0

# ---- warps ---------------------------------------------------------------------
for i, x in enumerate((13, 14)):
    m["warps"].append({"id": "to_crest" + ("_e" if i else ""), "at": {"tx": x, "ty": 0},
                       "trigger": "step_on", "to_map": "wickrun_crest",
                       "to": {"tx": x - 3, "ty": 27}, "facing": "up", "transition": "fade"})
for i, x in enumerate((4, 5)):
    m["warps"].append({"id": "to_trestles" + ("_e" if i else ""), "at": {"tx": x, "ty": H - 1},
                       "trigger": "step_on", "to_map": "wickrun_trestles",
                       "to": {"tx": x + 19, "ty": 0}, "facing": "down", "transition": "fade"})

# ---- the start line (the run clock) ------------------------------------------------
for x in range(10, 18):
    if (x, 4) in OPEN:
        m["triggers"].append({"id": f"start_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 4},
                              "activation": "step_on", "ref": "script.wickrun_start"})
owed.append("script.wickrun_start")


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


# ---- landmarks ------------------------------------------------------------------
obj("start_lamp_w", "tinderwick_lamp_post", (10, 1), 1, 3, overhang=2, walk_under=True)
obj("start_lamp_e", "tinderwick_lamp_post", (17, 1), 1, 3, overhang=2, walk_under=True)
obj("island_pine", "windward_bent_pine", (13, 17), 2, 3, overhang=2, walk_under=True)
obj("island_tree", "tinderwick_tree_c", (12, 22), 3, 4, overhang=3, walk_under=True)
obj("wreck", "solarium_troupe_cart", (10, 32), 3, 2)       # stand-in for the wax-cart wreck
obj("runout_lamp", "tinderwick_lamp_post", (16, 31), 1, 3, overhang=2, walk_under=True)
# the wax-road lanterns: a post on a verge every few rows, alternating sides —
# the run reads as a lit line down the dark mountain (and from the lift)
for i, (lx, ly) in enumerate([(10, 5), (17, 9), (4, 15), (10, 27), (17, 17), (17, 25),
                              (2, 37), (8, 40)]):
    obj(f"run_lamp_{i}", "tinderwick_lamp_post", (lx, ly), 1, 3, overhang=2, walk_under=True)
obj("verge_pine_a", "windward_bent_pine", (4, 28), 2, 3, overhang=2, walk_under=True)
obj("bowl_crates", "pearlmoor_fish_crates", (4, 13), 1, 1)
obj("bowl_crates_b", "pearlmoor_fish_crates", (23, 14), 1, 1)
for (x, y) in cells(10, 15, 17, 30):
    if (x, y) not in OPEN and rng.random() < 0.10:
        pass
# the island: rocks among the pines
for (x, y) in [(11, 16), (16, 19), (15, 27), (11, 29)]:
    tree[y * W + x] = 0
    deco[y * W + x] = gid("boulder")

# ---- trainers, cache, sign ------------------------------------------------------
owed += pt.trainer_beat(m, tid="runner_vess", at=(9, 22), facing="left", sight=4,
                        sprite="npc_girl")
owed += pt.trainer_beat(m, tid="runner_dace", at=(19, 33), facing="left", sight=5,
                        sprite="npc_boy")
owed += pt.cache(m, cid="wickrun_ledge", at=(25, 17))
owed += pt.sign(m, deco, W, sid="wickrun_runout", at=(14, 31))

TABLE = [
    {"kin_id": 11, "weight": 26, "min_level": 46, "max_level": 48},   # Tallowcrest (run-only)
    {"kin_id": 115, "weight": 20, "min_level": 46, "max_level": 47},  # Solvyne
    {"kin_id": 6, "weight": 18, "min_level": 46, "max_level": 48},    # Wickmere (run-only)
    {"kin_id": 118, "weight": 14, "min_level": 46, "max_level": 47},  # Helicore
    {"kin_id": 120, "weight": 12, "min_level": 46, "max_level": 47},  # Dawnfawn
    {"kin_id": 19, "weight": 6, "min_level": 47, "max_level": 48},    # Warmantis (run-only)
    {"kin_id": 12, "weight": 4, "min_level": 48, "max_level": 48},    # Chandrek (rare)
]
DAY = [
    {"kin_id": 11, "weight": 22, "min_level": 56, "max_level": 62},
    {"kin_id": 115, "weight": 18, "min_level": 56, "max_level": 62},
    {"kin_id": 6, "weight": 18, "min_level": 56, "max_level": 63},
    {"kin_id": 118, "weight": 14, "min_level": 56, "max_level": 62},
    {"kin_id": 19, "weight": 14, "min_level": 57, "max_level": 63},
    {"kin_id": 12, "weight": 8, "min_level": 58, "max_level": 64},
    {"kin_id": 7, "weight": 6, "min_level": 59, "max_level": 65},     # Wicklord (day only)
]
night = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                           id_prefix="run", table=TABLE)
for z in night:
    z["hidden_when_flag"] = "flag:dawn"
day = [{**z, "id": z["id"] + "_day", "table": DAY, "requires_flag": "flag:dawn"}
       for z in pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                                   id_prefix="run", table=DAY)]
for z in day:
    z.pop("hidden_when_flag", None)
m["encounters"] = night + day

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": above},
]

covered = set(pin) | {(x, y) for y in range(H) for x in range(W)
                      if any(g[y * W + x] for g in (tree, path, tallgrass, deco))}
objcells = {(x, y) for o in m["objects"]
            for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
            for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.10, avoid=covered | objcells | busy)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3, pin_base=pin)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
