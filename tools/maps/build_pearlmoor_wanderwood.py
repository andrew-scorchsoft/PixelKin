#!/usr/bin/env python3
"""
The Wanderwood (pearlmoor_wanderwood) — the heart of S5 "Not All Who Wander".

The old wood above Pearlmoor that Paul has walked for sixty-odd years. Its
shape IS the theme ("Coming Round", level-design §2b r1): from the south hub
two arms (west + east) loop up round a central tree mass and meet again at the
GLADE, so whichever way you wander you arrive — and a central path that looks
like the short way dead-ends at a story tree + a cache (you come back round).

Content, all optional colour except the glade:
  * Four carved "story trees" (`sign.wander_story_1..4`) — Abdul's line in S4:
    four stories about himself, all different, all true.
  * WANDERER HOB on the east arm (not lost; everything else moved).
  * A cache on the central dead-end (`script.pickup_wanderwood_cache`).
  * Tall grass on both arms — a small night table (17-20) + its dawn twin,
    mirrored in build_species WANDERWOOD_ENCOUNTERS (CURATED_AREAS). Spirlet,
    the first stage of Omenire's line, is the rare find.
  * The GLADE: the mossheart tree, the glade lamp (dark -> lit swap on
    `flag:q_south_wander_lamp`), and Paul (`script.wander_glade`: the
    Chickenpig leads against Omenire, then the cup).

Wiring: the allotment's gated `to_wood(_e)` (9-10,0) lands HERE at (13-14,22);
our `to_allotment(_e)` (13-14,23) lands on the allotment's (9-10,1).

Run:  python3 tools/maps/build_pearlmoor_wanderwood.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 28, 24
rng = random.Random(113)
owed: list[str] = []

# Start SOLID wood and carve the walk out of it: winding trails stamped as
# overlapping blobs along waypoint polylines (organic, never ruled corridors).
tree = [1] * (W * H)
path = mk.make_grid(W, H)
grass = mk.make_grid(W, H)   # tall grass (the encounter terrain)


def carve_blob(cx, cy, rx, ry=None):
    g = mk.make_grid(W, H)
    mk.blob(g, W, H, cx, cy, rx, ry if ry is not None else rx)
    for i, v in enumerate(g):
        if v:
            tree[i] = 0


def trail(points, r=1.25, lane=True):
    """Carve a winding trail through `points` (blob-stamped), and lay a 4-connected
    dirt lane down its centre when `lane`."""
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


HUB = (13.5, 19.0)
# the south mouth + hub clearing
for y in range(20, H):
    for x in (13, 14):
        tree[y * W + x] = 0
mk.rect(path, W, H, 13, 19, 13, H - 1)
carve_blob(13.5, 19.0, 3.4, 1.8)
# the WEST arm and the EAST arm wind up round the central mass to the glade
trail([(13, 19), (9, 19), (5, 17), (4, 13), (6, 10), (4, 7), (7, 5), (10, 5)])
trail([(14, 19), (18, 19), (22, 17), (23, 13), (21, 10), (23, 7), (20, 5), (17, 5)])
# the GLADE (top-centre) — both arms arrive here
carve_blob(13.5, 4.6, 6.2, 2.9)
# the "short cut" that isn't: hub north into the central mass, a dead end
trail([(13, 18), (13, 15), (12, 13)], r=1.0)
carve_blob(12.8, 11.6, 2.0, 1.6)
# story clearings, each off its arm
carve_blob(7.6, 14.2, 1.9, 2.3)
carve_blob(19.6, 14.2, 1.9, 2.3)
# keep the glade sealed from the dead end (row 8 stays wood across the middle)
for x in range(9, 19):
    tree[8 * W + x] = 1

# a solid 2-deep frame (the mouth excepted)
for y in range(H):
    for x in range(W):
        if (x < 2 or x >= W - 2 or y < 2 or y >= H - 2) and not (x in (13, 14) and y >= 20):
            tree[y * W + x] = 1

# tall grass beside the arms (avoidable, tempting)
for (cx, cy, rx, ry) in [(3.6, 12.5, 1.3, 2.4), (7.5, 18.4, 1.8, 1.0),
                         (23.4, 12.5, 1.3, 2.4), (19.5, 18.4, 1.8, 1.0),
                         (5.0, 6.2, 1.4, 1.0), (22.0, 6.2, 1.4, 1.0)]:
    mk.blob(grass, W, H, cx, cy, rx, ry)
for i in range(W * H):
    if tree[i]:
        path[i] = 0
        grass[i] = 0
    if path[i]:
        grass[i] = 0

terrain_layers = [
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": grass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]

gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.55 else gr[0] for _ in range(W * H)]
deco = mk.make_grid(W, H)

m: dict = {
    "id": "pearlmoor_wanderwood", "display_name": "The Wanderwood",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/lowleaf-hollow-b.mp3",
}

# ---- the glade: mossheart tree, the glade lamp (dark/lit swap), Paul ---------------
m["objects"].append({"id": "mossheart", "sprite": "glowmoss_deep_mossheart_tree",
                     "at": {"tx": 12, "ty": 1}, "w": 3, "h": 4, "overhang": 2})
for oid, spr, req, hide in [
    ("glade_lamp_dark", "nightreach_watch_lamp_dark", None, "flag:q_south_wander_lamp"),
    ("glade_lamp_lit", "nightreach_watch_lamp_lit", "flag:q_south_wander_lamp", None),
]:
    o = {"id": oid, "sprite": spr, "at": {"tx": 16, "ty": 2}, "w": 2, "h": 3, "overhang": 1}
    if req:
        o["requires_flag"] = req
    if hide:
        o["hidden_when_flag"] = hide
    m["objects"].append(o)
for x in (16, 17):
    m["triggers"].append({"id": f"glade_lamp_{x}", "kind": "sign", "at": {"tx": x, "ty": 4},
                          "activation": "interact", "ref": "sign.wander_glade_lamp",
                          "requires_flag": "flag:q_south_wander_lamp"})
m["npcs"].append({"id": "paul_glade", "at": {"tx": 11, "ty": 5}, "facing": "down",
                  "sprite": "booji_paul", "movement": "static",
                  "dialogue_ref": "script.wander_glade",
                  "requires_flag": "flag:q_south_wander",
                  "hidden_when_flag": "flag:q_south_wander_done"})

# ---- the four story trees (carved crown trees; read at the trunk) -------------------
for n, (x, y) in enumerate([(6, 12), (18, 12), (7, 2), (10, 9)], start=1):
    pt.crown_tree(m, oid=f"story_tree_{n}", sprite="tinderwick_tree", at=(x, y))
    m["triggers"].append({"id": f"story_{n}", "kind": "sign",
                          "at": {"tx": x + 1, "ty": y + 3}, "activation": "interact",
                          "ref": f"sign.wander_story_{n}"})
    for yy in range(y, y + 4):        # the crown tree sits on carved ground
        for xx in range(x, x + 3):
            tree[yy * W + xx] = 0
            grass[yy * W + xx] = 0

# ---- Wanderer Hob (east arm), the cache (the dead-end's payoff) ---------------------
for nid, ref, req, hide in [
    ("hob", "npc.wanderwood_hob", None, "flag:q_south_wander_lamp"),
    ("hob_done", "npc.wanderwood_hob_done", "flag:q_south_wander_lamp", None),
]:
    n = {"id": nid, "at": {"tx": 24, "ty": 12}, "facing": "left", "sprite": "npc_man",
         "movement": "look_around", "dialogue_ref": ref}
    if req:
        n["requires_flag"] = req
    if hide:
        n["hidden_when_flag"] = hide
    m["npcs"].append(n)
owed += pt.cache(m, cid="wanderwood_cache", at=(14, 11))

# ---- glowshrooms strung through the dark (the deep-wood light) ----------------------
for (x, y, nm) in [(3, 7, "glowshroom_a"), (9, 15, "glowshroom_b"), (16, 15, "glowshroom_a"),
                   (22, 7, "glowshroom_b"), (8, 4, "glowshroom_a"), (17, 4, "glowshroom_b"),
                   (11, 12, "glowshroom_a"), (19, 12, "glowshroom_b")]:
    i = y * W + x
    if not tree[i] and not path[i] and not grass[i]:
        deco[i] = gid(nm)

# ---- encounters: night table + its dawn twin (R4 day-form convention) ---------------
NIGHT = [{"kin_id": 56, "weight": 30, "min_level": 17, "max_level": 19},   # Sporeling
         {"kin_id": 62, "weight": 25, "min_level": 17, "max_level": 19},   # Barkhelm
         {"kin_id": 38, "weight": 20, "min_level": 18, "max_level": 20},   # Mossglow
         {"kin_id": 105, "weight": 17, "min_level": 18, "max_level": 20},  # Snoozlet
         {"kin_id": 111, "weight": 8, "min_level": 18, "max_level": 20}]   # Spirlet (rare)
DAY = [{"kin_id": 56, "weight": 30, "min_level": 55, "max_level": 58},
       {"kin_id": 62, "weight": 25, "min_level": 56, "max_level": 59},
       {"kin_id": 38, "weight": 20, "min_level": 56, "max_level": 60},
       {"kin_id": 105, "weight": 17, "min_level": 57, "max_level": 60},
       {"kin_id": 111, "weight": 8, "min_level": 58, "max_level": 61}]
night = pt.zones_from_grid(grass, W, H, terrain="tall_grass", rate=0.1, table=NIGHT,
                           id_prefix="wood")
for z in night:
    z["hidden_when_flag"] = "flag:dawn"
day = [{**z, "id": z["id"] + "_day", "table": DAY, "requires_flag": "flag:dawn"} for z in night]
for z in day:
    z.pop("hidden_when_flag", None)
m["encounters"] = night + day

# ---- the way back down ------------------------------------------------------------
for x, sfx in ((13, ""), (14, "_e")):
    m["warps"].append({"id": f"to_allotment{sfx}", "at": {"tx": x, "ty": H - 1}, "trigger": "step_on",
                       "to_map": "pearlmoor_allotment", "to": {"tx": x - 4, "ty": 1},
                       "facing": "down", "transition": "fade"})

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

obj_cells = {(x, y) for o in m["objects"]
             for y in range(o["at"]["ty"], o["at"]["ty"] + o.get("h", 1))
             for x in range(o["at"]["tx"], o["at"]["tx"] + o.get("w", 1))}
npc_cells = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.10,
                 avoid=obj_cells | npc_cells | {(x, y) for y in range(H) for x in range(W)
                                                if path[y * W + x] or tree[y * W + x]
                                                or grass[y * W + x]})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
