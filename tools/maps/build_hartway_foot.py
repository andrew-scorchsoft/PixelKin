#!/usr/bin/env python3
"""
Hartway Foot (hartway_foot) — the foot of THE HARTSHOULDER, the mountain behind
Wayward Rise, and the bottom of the old climbers' road up it: THE HARTWAY (2026-11,
docs/world/walkthrough/12-the-hartway.md).

A quiet threshold west of the Rise (post-Chickenpig by construction, like the Rise
itself). The road in from the Rise's new west mouth runs to the rope-warden's bothy
under the first crag, where rock steps go up to the climb proper (`hartway_climb`).

  * THE ROPE GATE — the steps (10,4) -> hartway_climb (14,47). The warden lets nobody
    up alone: "two on a rope, one with nerve, one with sense". The warp wants
    `flag:greg_roped`; its `blocked_ref` is the warden's own stage-aware script, and it
    opens the "find Greg" side quest (content/regions/hartway.ts).
  * HOLLIS the rope-warden at her bothy (a rest point: her fire) and, once found, GREG
    waiting by the steps (`greg_foot`, flag:greg_found .. flag:greg_roped).
  * two tall-grass beds (band 17-19), one cache, a lit sign on the lane.

Wiring (compass-true, world_geometry): the Rise's `to_hartway(_e)` (0,14)/(0,15) lands
HERE at (28,12)/(28,13) facing left; our `to_rise(_e)` (29,12)/(29,13) lands on the
Rise's (1,14)/(1,15) facing right. The map sits straight WEST of the Rise at world
(-27,-150): under the Wick-Run's trestles, over the far Wanderwood. The steps are a
mid-map portal (the climb is a mountain OVER this ground, so it never places).

Run:  python3 tools/maps/build_hartway_foot.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import warp_markers as wm
from mapkit import gid

W, H = 30, 20
rng = random.Random(1907)
owed: list[str] = []

tree = mk.make_grid(W, H)
cliff = mk.make_grid(W, H)
path = mk.make_grid(W, H)
tall = mk.make_grid(W, H)

# ---- the crag (north + west) and the wood (south + east) ---------------------------
mk.rect(cliff, W, H, 0, 0, W - 1, 4)                    # the first crag of the Hartshoulder
mk.rect(cliff, W, H, 0, 0, 2, H - 1)
for (bx, by, br) in [(4, 6, 2), (22, 5, 1), (26, 5, 2), (3, 12, 1), (17, 4, 1)]:
    mk.blob(cliff, W, H, bx, by, br, br)
cliff[4 * W + 10] = 0                                   # the notch the steps climb out of
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)
mk.rect(tree, W, H, W - 2, 0, W - 1, H - 1)
mk.organic_border(tree, W, H, depth=0,
                  bumps=[(27, 8, 2), (26, 16, 2), (12, 18, 2), (20, 18, 1), (5, 18, 2)], rng=rng)
for y in (12, 13):                                      # the mouth east to the Rise
    for x in (W - 3, W - 2, W - 1):
        tree[y * W + x] = 0

# ---- the lane: in from the Rise, west under the crag, north to the steps ------------
mk.rect(path, W, H, 11, 12, W - 1, 13)
mk.rect(path, W, H, 10, 5, 11, 13)

# ---- tall grass (hard-edged beds) ----------------------------------------------------
mk.blob(tall, W, H, 20.5, 15.5, 3.4, 1.4)
mk.blob(tall, W, H, 6.5, 14.5, 2.4, 1.6)
mk.blob(tall, W, H, 23, 9, 2.2, 1.2)

for i in range(W * H):
    if cliff[i]:
        tree[i] = 0
    if tree[i] or cliff[i]:
        path[i] = tall[i] = 0
    if path[i]:
        tall[i] = 0

m: dict = {
    "id": "hartway_foot", "display_name": "Hartway Foot",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/lowleaf-hollow-b.mp3",
    "ambience": {
        "particles": [{"kind": "glowmotes", "density": 0.35},
                      {"kind": "leaves", "density": 0.2}],
        "mist": {"color": "#a8b8d0", "alpha": 0.06, "speed": 4},
    },
}
deco = mk.make_grid(W, H)

# ---- the rope gate: rock steps up the crag -------------------------------------------
wm.add(m, wm.marker("steps_up", "steps_n", 10, 2))
m["warps"].append({"id": "to_climb", "at": {"tx": 10, "ty": 4}, "trigger": "step_on",
                   "to_map": "hartway_climb", "to": {"tx": 14, "ty": 47}, "facing": "up",
                   "transition": "fade", "requires_flag": "flag:greg_roped",
                   "blocked_ref": "script.hartway_gate"})
owed.append("script.hartway_gate")

# ---- the rope-warden's bothy + her fire (a rest point) -------------------------------
m["objects"] += [
    {"id": "bothy", "sprite": "farlamp_keeper_hut", "at": {"tx": 14, "ty": 5},
     "w": 4, "h": 4, "overhang": 2},
    {"id": "camp", "sprite": "sunvault_climbers_camp", "at": {"tx": 19, "ty": 8},
     "w": 3, "h": 2},
    {"id": "lamp_steps", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 4},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_mouth", "sprite": "tinderwick_lamp_post", "at": {"tx": 25, "ty": 9},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "cairn", "sprite": "windward_cairn", "at": {"tx": 6, "ty": 10},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "pine_a", "sprite": "windward_bent_pine", "at": {"tx": 5, "ty": 8},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "pine_b", "sprite": "windward_bent_pine", "at": {"tx": 23, "ty": 4},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "rocks_a", "sprite": "stillwater_crag_boulders", "at": {"tx": 14, "ty": 15},
     "w": 2, "h": 2},
    {"id": "rocks_b", "sprite": "stillwater_crag_boulders", "at": {"tx": 3, "ty": 9},
     "w": 2, "h": 2},
]
m["triggers"].append({"id": "bothy_door", "kind": "sign", "at": {"tx": 16, "ty": 9},
                      "activation": "interact", "ref": "sign.hartway_bothy"})
owed.append("sign.hartway_bothy")
for x in (19, 20, 21):
    m["triggers"].append({"id": f"camp_rest_{x}", "kind": "script", "at": {"tx": x, "ty": 10},
                          "activation": "interact", "ref": "script.hartway_foot_rest"})
owed.append("script.hartway_foot_rest")
for oid, sprite, at in [("tree_se", "tinderwick_tree", (23, 14)), ("tree_s", "tinderwick_tree", (15, 14)),
                        ("tree_sw", "tinderwick_tree", (8, 14))]:
    pt.crown_tree(m, oid=oid, sprite=sprite, at=at)

m["npcs"] += [
    # HOLLIS, the rope-warden (her whole chain is one stage-aware script)
    {"id": "hollis", "at": {"tx": 18, "ty": 10}, "facing": "down", "sprite": "pass_walker",
     "movement": "static", "dialogue_ref": "script.hartway_hollis"},
    # GREG, found and waiting to rope up
    {"id": "greg_foot", "at": {"tx": 9, "ty": 6}, "facing": "right", "sprite": "greg",
     "movement": "static", "dialogue_ref": "script.greg_rope_up",
     "requires_flag": "flag:greg_found", "hidden_when_flag": "flag:greg_roped"},
]
owed += ["script.hartway_hollis", "script.greg_rope_up"]

owed += pt.sign(m, deco, W, sid="hartway_foot", at=(24, 11))
owed += pt.sign(m, deco, W, sid="hartway_steps", at=(9, 5))
owed += pt.cache(m, cid="hartway_foot", at=(4, 16))

# ---- warps: the mouth back to the Rise ------------------------------------------------
for y, sfx in ((12, ""), (13, "_e")):
    m["warps"].append({"id": f"to_rise{sfx}", "at": {"tx": W - 1, "ty": y},
                       "trigger": "step_on", "to_map": "wayward_rise",
                       "to": {"tx": 1, "ty": y + 2}, "facing": "right", "transition": "fade"})

# ---- encounters (band 17-19) ----------------------------------------------------------
TABLE = [{"kin_id": k, "weight": w_, "min_level": lo, "max_level": hi} for (k, w_, lo, hi) in
         [(56, 28, 17, 18), (62, 26, 17, 19), (38, 18, 17, 19), (47, 18, 17, 19), (65, 10, 18, 19)]]
m["encounters"] += pt.zones_from_grid(tall, W, H, terrain="tall_grass", rate=0.10,
                                      table=TABLE, id_prefix="foot")

gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]
_solid = {(x, y) for o in m["objects"]
          for y in range(o["at"]["ty"], o["at"]["ty"] + o.get("h", 1))
          for x in range(o["at"]["tx"], o["at"]["tx"] + o.get("w", 1))}
for (x, y) in [(13, 10), (7, 11), (21, 11), (26, 14), (17, 16), (6, 5), (20, 6), (9, 17)]:
    i = y * W + x
    if not (tree[i] or cliff[i] or path[i] or tall[i]) and (x, y) not in _solid:
        deco[i] = gid("boulder")

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tall", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tall},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]
busy = _solid | {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"] + m["triggers"] + m["warps"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.14,
                 avoid=busy | {(x, y) for y in range(H) for x in range(W)
                               if path[y * W + x] or tree[y * W + x] or cliff[y * W + x]
                               or tall[y * W + x] or deco[y * W + x]},
                 flowers=0.25)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
