#!/usr/bin/env python3
"""
The Far Side (pearlmoor_wanderwood_far) — the Wanderwood's deeper pocket, S5.

An OPTIONAL loop off the Wanderwood's west arm: two roads out of the wood's west
edge (a low one off the hub side, a high one near the glade) are the two ends of
one long wander round the far side of the hill — so you can go out low and come
back in high, a few steps from the glade ("Coming Round" again, one size up).
Nothing here gates the quest; it is all discovery, and it stays after the cup.

Everything in it is a thing Paul would recognise (S5's love letter, carried on):
  * the LAUGH — a one-time step_on band on the low road: somebody's unholy
    laughter rolls through the trees (`sign.wander_far_laugh`).
  * the LIFTING BENCH — a fallen-column bench + a cairn of harbour-stones; the
    80 / 140 / "sixty-three years" scratchings (`sign.wander_far_bench`).
  * MAGS at her GRIDDLE — cheese-buns (a no-rest heal), the clockwork
    lamplighters joke, and a word about Paul (`script.wander_mags`).
  * the GLASS STEPS — a pond crossed on flat grey slabs (the round boulders sit on water:
    only some hold); "p. went first" (`sign.wander_glass_steps`) -> an islet cache
    with a note hinting he's been quietly looking out for you all along
    (`script.pickup_wander_far_steps`).
  * the ANSWERING LAMP — a brass, glass-headed lamp in the hollow that answers
    everything with total confidence (`script.wander_answering_lamp`), and p.'s
    carving beside it: REASSESS (`sign.wander_far_reassess`).
  * the SUGAR STUMP — a triangle and an umbrella burned into its rings
    (`sign.wander_far_stump`).
  * two more story trees (`sign.wander_story_5/6`): the quiet helper at the fair,
    and the friend's book read across two seas.
  * a little tall grass — the Wanderwood's own table (14-17 + dawn twin),
    mirrored in build_species (WANDERWOOD rows, CURATED_AREAS).

Wiring (W<->E, mirrored rows): wanderwood `to_far(_b)` (0,16-17) -> here (28,16-17);
wanderwood `to_far_n(_b)` (0,8-9) -> here (28,8-9). Our `to_wood*` at x=29 land on
the wood's (1, same row).

Run:  python3 tools/maps/build_pearlmoor_wanderwood_far.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 24
rng = random.Random(1163)
owed: list[str] = []

tree = [1] * (W * H)
path = mk.make_grid(W, H)
grass = mk.make_grid(W, H)
pond = mk.make_grid(W, H)


def carve_blob(cx, cy, rx, ry=None):
    g = mk.make_grid(W, H)
    mk.blob(g, W, H, cx, cy, rx, ry if ry is not None else rx)
    for i, v in enumerate(g):
        if v:
            tree[i] = 0


def trail(points, r=1.25, lane=True):
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        for k in range(n + 1):
            t = k / n
            carve_blob(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r)
        if lane:
            x, y = round(x0), round(y0)
            tx, ty = round(x1), round(y1)
            while (x, y) != (tx, ty):
                path[y * W + x] = 1
                if abs(tx - x) >= abs(ty - y):
                    x += 1 if tx > x else -1
                else:
                    y += 1 if ty > y else -1
            path[y * W + x] = 1


# ---- the two road mouths on the east edge (rows 16-17 low, 8-9 high) ----------
for y in (16, 17, 8, 9):
    for x in range(W - 3, W):
        tree[y * W + x] = 0

# ---- the loop: low road west -> bench -> griddle -> up the west side ->
#      the Answering Lamp's hollow -> along the top -> back down to the high road
trail([(29, 17), (25, 17), (21, 18), (16, 19), (11, 19), (6, 17), (4, 13),
       (4, 9), (6, 6), (10, 5), (15, 5), (20, 5), (24, 5), (25, 8), (29, 8)])
# clearings strung along it
carve_blob(21.5, 18.6, 3.2, 2.0)     # the lifting bench
carve_blob(10.5, 18.6, 3.4, 2.2)     # Mags's griddle
carve_blob(6.0, 4.4, 2.8, 2.0)       # the Answering Lamp's hollow
carve_blob(15.0, 4.0, 2.6, 1.8)      # the sugar stump
carve_blob(20.5, 3.2, 2.6, 1.6)      # story tree 5's clearing
carve_blob(24.6, 12.6, 2.2, 2.6)     # story tree 6, off the high road's bend
trail([(25, 8), (25, 11)], r=1.0, lane=False)
# the GLASS STEPS: a pond clearing off the west side, an islet on its far shore
carve_blob(11.5, 11.6, 5.2, 3.9)
trail([(4, 11), (7, 11)], r=1.0)
mk.blob(pond, W, H, 12.0, 11.5, 4.6, 3.0)

# a solid 2-deep frame (the east road mouths excepted)
for y in range(H):
    for x in range(W):
        if (x < 2 or x >= W - 2 or y < 2 or y >= H - 2) and \
                not (x >= W - 2 and y in (16, 17, 8, 9)):
            tree[y * W + x] = 1

# the steps: a zig-zag of mossy (walkable) stones across to the islet; the bare
# pebbles (decoys) are deco on WATER, so they look like stones and don't hold.
# (the bend keeps every stretch of water left round them >= 2 tiles thick, so
# the pond autotiles as one body instead of slivers)
STONES = [(8, 11), (9, 11), (10, 11), (10, 12), (11, 12), (12, 12), (13, 12)]
ISLET = [(14, 11), (15, 11), (14, 12), (15, 12)]
DECOYS = [(11, 11), (9, 12), (12, 13), (13, 10), (10, 13), (12, 11)]
for x, y in STONES + ISLET:
    pond[y * W + x] = 0
# the pond's far (east) shore is wood: the islet is only an islet if it's cut off
for y in range(8, 16):
    for x in range(16, 19):
        tree[y * W + x] = 1
# and the water fills its clearing to the trees (bar the near shore by the lane),
# so no strip of shore is left that only a swimmer could stand on
_clear = mk.make_grid(W, H)
mk.blob(_clear, W, H, 11.5, 11.6, 5.2, 3.9)
for y in range(H):
    for x in range(W):
        i = y * W + x
        if _clear[i] and not tree[i] and (x >= 8 or (x == 7 and y not in (10, 11, 12))) \
                and (x, y) not in STONES + ISLET:
            pond[i] = 1

# tall grass beside the loop (avoidable, tempting) — the Wanderwood's table
for (cx, cy, rx, ry) in [(16.5, 20.5, 2.0, 0.9), (3.0, 10.5, 1.0, 2.0),
                         (11.0, 3.0, 2.2, 0.9), (26.5, 4.0, 1.0, 1.2)]:
    carve_blob(cx, cy, rx + 0.3, ry + 0.3)
    mk.blob(grass, W, H, cx, cy, rx, ry)
# re-seal the frame (the grass carves may have nicked it)
for y in range(H):
    for x in range(W):
        if (x < 2 or x >= W - 2 or y < 2 or y >= H - 2) and \
                not (x >= W - 2 and y in (16, 17, 8, 9)):
            tree[y * W + x] = 1
for i in range(W * H):
    if tree[i]:
        path[i] = 0
        grass[i] = 0
        pond[i] = 0
    if path[i] or pond[i]:
        grass[i] = 0
    if pond[i]:
        path[i] = 0

deco = mk.make_grid(W, H)
gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.55 else gr[0] for _ in range(W * H)]

m: dict = {
    "id": "pearlmoor_wanderwood_far", "display_name": "The Far Side",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/lowleaf-hollow-b.mp3",
}


def clear(x0, y0, w, h):
    for yy in range(y0, y0 + h):
        for xx in range(x0, x0 + w):
            i = yy * W + xx
            tree[i] = grass[i] = path[i] = pond[i] = 0


# ---- the LAUGH: a one-time band across the low road, just inside the trees ----
# (the band covers EVERY walkable tile of the road's cut at x=26, so it can't be
# walked round — and it's what makes the far side's crossing carry a beat)
for y in [yy for yy in range(12, 22) if not tree[yy * W + 26]]:
    m["triggers"].append({"id": f"far_laugh_{y}", "kind": "sign", "at": {"tx": 26, "ty": y},
                          "activation": "step_on", "ref": "sign.wander_far_laugh",
                          "sets_flags": ["flag:wander_far_laugh"],
                          "hidden_when_flag": "flag:wander_far_laugh"})

# ---- the LIFTING BENCH: a fallen-column bench + the cairn of harbour-stones ----
m["objects"].append({"id": "far_bench", "sprite": "solarium_column_fallen",
                     "at": {"tx": 20, "ty": 20}, "w": 3, "h": 1, "overhang": 0})
m["objects"].append({"id": "far_stones", "sprite": "windward_cairn",
                     "at": {"tx": 23, "ty": 18}, "w": 2, "h": 3, "overhang": 1})
clear(20, 20, 3, 1)
clear(23, 18, 2, 3)
for x in (20, 21, 22):
    m["triggers"].append({"id": f"far_bench_{x}", "kind": "sign", "at": {"tx": x, "ty": 20},
                          "activation": "interact", "ref": "sign.wander_far_bench"})

# ---- MAGS at her GRIDDLE ------------------------------------------------------
m["objects"].append({"id": "far_griddle", "sprite": "lowleaf_stall",
                     "at": {"tx": 9, "ty": 17}, "w": 2, "h": 2, "overhang": 1})
clear(9, 17, 2, 2)
m["npcs"].append({"id": "wander_mags", "at": {"tx": 11, "ty": 18}, "facing": "down",
                  "sprite": "npc_old_woman", "movement": "static",
                  "dialogue_ref": "script.wander_mags"})

# ---- the GLASS STEPS: sign on the near shore, cache on the islet ---------------
owed += pt.sign(m, deco, W, sid="wander_glass_steps", at=(7, 12))
# the stones that HOLD are flat grey slabs (plain `scree` ground tiles set into
# the base — no terrain, so no autotile ring); the ones that DON'T are round
# boulders sat on the water itself (water still gates the tile either way).
for k, (x, y) in enumerate(STONES):
    base[y * W + x] = gid(("scree0", "scree1", "scree2")[k % 3])
deco[11 * W + 14] = gid("greymoss_a")
for x, y in DECOYS:
    deco[y * W + x] = gid("boulder")         # round stones on water: they don't
owed += pt.cache(m, cid="wander_far_steps", at=(15, 12))

# ---- the ANSWERING LAMP in its hollow + p.'s carving -----------------------------
m["objects"].append({"id": "answering_lamp", "sprite": "tideglass_lens_lit",
                     "at": {"tx": 5, "ty": 3}, "w": 2, "h": 2, "overhang": 0})
clear(5, 3, 2, 2)
for x in (5, 6):
    m["triggers"].append({"id": f"answering_lamp_{x}", "kind": "script",
                          "at": {"tx": x, "ty": 4}, "activation": "interact",
                          "ref": "script.wander_answering_lamp"})
owed += pt.sign(m, deco, W, sid="wander_far_reassess", at=(8, 3))

# ---- the SUGAR STUMP ------------------------------------------------------------
m["objects"].append({"id": "sugar_stump", "sprite": "interior_table",
                     "at": {"tx": 14, "ty": 3}, "w": 2, "h": 2, "overhang": 0})
clear(14, 3, 2, 2)
for x in (14, 15):
    m["triggers"].append({"id": f"sugar_stump_{x}", "kind": "sign", "at": {"tx": x, "ty": 4},
                          "activation": "interact", "ref": "sign.wander_far_stump"})

# ---- story trees 5 + 6 (the Wanderwood's four carry on round here) --------------
for n, (x, y) in [(5, (19, 1)), (6, (23, 10))]:
    pt.crown_tree(m, oid=f"story_tree_{n}", sprite="tinderwick_tree", at=(x, y))
    m["triggers"].append({"id": f"story_{n}", "kind": "sign",
                          "at": {"tx": x + 1, "ty": y + 3}, "activation": "interact",
                          "ref": f"sign.wander_story_{n}"})
    for yy in range(y, y + 4):
        for xx in range(x, x + 3):
            tree[yy * W + xx] = 0
            grass[yy * W + xx] = 0

# glowshrooms strung through the dark
for (x, y, nm) in [(3, 15, "glowshroom_a"), (13, 20, "glowshroom_b"), (18, 6, "glowshroom_a"),
                   (27, 6, "glowshroom_b"), (3, 6, "glowshroom_b"), (24, 20, "glowshroom_a"),
                   (8, 9, "glowshroom_a"), (16, 2, "glowshroom_b")]:
    i = y * W + x
    if not tree[i] and not path[i] and not grass[i] and not pond[i] and not deco[i]:
        deco[i] = gid(nm)

# ---- encounters: the Wanderwood's own night table + dawn twin -------------------
NIGHT = [{"kin_id": 56, "weight": 30, "min_level": 14, "max_level": 16},   # Sporeling
         {"kin_id": 62, "weight": 25, "min_level": 14, "max_level": 16},   # Barkhelm
         {"kin_id": 38, "weight": 20, "min_level": 15, "max_level": 17},   # Mossglow
         {"kin_id": 105, "weight": 17, "min_level": 15, "max_level": 17},  # Snoozlet
         {"kin_id": 111, "weight": 8, "min_level": 15, "max_level": 17}]   # Spirlet (rare)
DAY = [{"kin_id": 56, "weight": 30, "min_level": 55, "max_level": 58},
       {"kin_id": 62, "weight": 25, "min_level": 56, "max_level": 59},
       {"kin_id": 38, "weight": 20, "min_level": 56, "max_level": 60},
       {"kin_id": 105, "weight": 17, "min_level": 57, "max_level": 60},
       {"kin_id": 111, "weight": 8, "min_level": 58, "max_level": 61}]
night = pt.zones_from_grid(grass, W, H, terrain="tall_grass", rate=0.1, table=NIGHT,
                           id_prefix="far")
for z in night:
    z["hidden_when_flag"] = "flag:dawn"
day = [{**z, "id": z["id"] + "_day", "table": DAY, "requires_flag": "flag:dawn"} for z in night]
for z in day:
    z.pop("hidden_when_flag", None)
m["encounters"] = night + day

# ---- the two roads back into the Wanderwood (mirrored rows, landing 1 inboard) ---
for y, wid in ((16, "to_wood"), (17, "to_wood_b"), (8, "to_wood_n"), (9, "to_wood_n_b")):
    m["warps"].append({"id": wid, "at": {"tx": W - 1, "ty": y}, "trigger": "step_on",
                       "to_map": "pearlmoor_wanderwood", "to": {"tx": 1, "ty": y},
                       "facing": "right", "transition": "fade"})

terrain_layers = [
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_pond", "role": "terrain", "terrain": "pond",
     "set": "vesper_overworld_set", "depth": 0, "data": pond},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": grass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]
m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

obj_cells = {(x, y) for o in m["objects"]
             for y in range(o["at"]["ty"], o["at"]["ty"] + o.get("h", 1))
             for x in range(o["at"]["tx"], o["at"]["tx"] + o.get("w", 1))}
npc_cells = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]}
trig_cells = {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.10,
                 avoid=obj_cells | npc_cells | trig_cells | {
                     (x, y) for y in range(H) for x in range(W)
                     if path[y * W + x] or tree[y * W + x] or grass[y * W + x]
                     or pond[y * W + x] or deco[y * W + x]})

# audit_flow WARNs, accepted by design: `free-pass` (the far side is a DISCOVERY
# pocket off an already-gated optional wood — the grass is there to wander into,
# never a toll; S5 is about recognition, not difficulty) and `loop` (no one-way
# ledge needed: the map IS one half of a loop — out the low road, back by the high
# road into the Wanderwood a few steps from the glade).
if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
