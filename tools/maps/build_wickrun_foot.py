#!/usr/bin/env python3
"""
The Wick-Run Foot — the bottom of the old wax road, at the sea west of
Lightkeeper's Point (09-the-wild-ways §2 A; kind route, region SOUTH, NO
encounters — it's reachable on foot from Pearlmoor at lv ~14).

Before the Long Dusk the wax-carts ran out of the chute here, the wax went by
barrow along the beach road to Pearlmoor's quays, and the empties rode the
Tallow Lift back up the mountain. Now it's a quiet yard of cold barrels, a
lift-house whose car hangs far up at the crest, and — on a good night — the
Runners screaming down the last drop to the finish.

Three signature touches (§8):
  1. THE FINISH (north): the run's last chute drops out of the forest under a
     finish arch; its final row is a step_on band (`script.wickrun_finish`) —
     the clock stops, the tier ribbons pay out once each, the runner is handed
     in. Nobody walks UP into it: it's a chute (one-way, like the whole run).
  2. THE TALLOW LIFT's foot station (east): the lift-keeper and the brakeman's
     sign. Until someone frees the brake at the crest the car's up top and the
     lift won't run — the see-it-early promise for South-era players. Once
     freed, it rides you to the crest (`script.tallow_lift_foot`, `travel`).
  3. THE WAX-YARD (west): barrels, a wrecked cart, the Runners' rack — and the
     yard bench by the lift (a rest point).

HANDSHAKE: north `to_lower`/`_e` (14,0)/(15,0) <-> wickrun_lower's `to_foot`
(20,43)/(21,43) (each lands ON the other — and nothing in the yard can reach
them: the last drop is a chute); east `to_point`/`_s` (29,21)/(29,22) <->
pearlmoor_point's west beach `to_wickrun`/`_s` (0,8)/(0,9) (each lands ON the
other). Geometry: x -51..-21, y -96..-66.

Run:  python3 tools/maps/build_wickrun_foot.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 30, 30
rng = random.Random(9066)
owed: list[str] = []

tree = mk.make_grid(W, H)
path = mk.make_grid(W, H)
sand = mk.make_grid(W, H)
water = mk.make_grid(W, H)
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)


def cells(x0, y0, x1, y1):
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}


# ---- the land: forest on the mountain's foot (north + west), the sea south ---------
mk.rect(tree, W, H, 0, 0, W - 1, 8)                 # the mountain's wooded skirt
mk.organic_border(tree, W, H, left=1, right=1, depth=2,
                  bumps=[(2, 10, 2), (27, 10, 2), (1, 17, 1), (28, 16, 2)], rng=rng)
mk.blob(tree, W, H, 6.0, 9.0, 3.5, 1.4)             # the forest spills into the yard
mk.blob(tree, W, H, 25.5, 9.5, 3.0, 1.6)
for (x, y) in cells(14, 0, 15, 1) | cells(14, 2, 16, 8):
    tree[y * W + x] = 0                              # the last drop
for (x, y) in cells(20, 9, 23, 13) | cells(19, 13, 25, 15):
    tree[y * W + x] = 0                              # the lift-house plot
for y in range(18, H):                              # the shore: no trees on the beach
    for x in range(W):
        if 2 <= x < W - 2 or (y > 20 and x >= 2):
            tree[y * W + x] = 0
# the beach + the sea
mk.rect(sand, W, H, 2, 20, W - 1, H - 1)
mk.blob(sand, W, H, 8.0, 19.6, 5.0, 1.2)
mk.rect(water, W, H, 0, 25, W - 1, H - 1)
mk.blob(water, W, H, 5.0, 24.3, 3.5, 1.6)
mk.blob(water, W, H, 18.5, 24.2, 4.0, 1.2)
mk.rect(water, W, H, W - 1, 23, W - 1, H - 1)       # the point's west tip, next door
for (x, y) in cells(26, 20, W - 1, 22):             # the beach road east stays dry
    water[y * W + x] = 0
for i in range(W * H):
    if water[i]:
        sand[i] = 1
        tree[i] = 0
    if tree[i]:
        sand[i] = 0

# ---- paths: finish apron, the lane down through the yard -----------------------
LANE = cells(14, 9, 16, 10) | cells(9, 11, 21, 11) | cells(15, 12, 15, 18) \
    | cells(16, 13, 21, 13) | {(14, 0), (15, 0), (14, 1), (15, 1)}
for (x, y) in LANE:
    if not tree[y * W + x] and not water[y * W + x]:
        path[y * W + x] = 1
        sand[y * W + x] = 0

pin: dict = {}
m: dict = {
    "id": "wickrun_foot", "display_name": "Wick-Run Foot",
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


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


# ---- 1. the last drop + THE FINISH ------------------------------------------------
wk.chute(m, pin, deco, W, cells(14, 2, 16, 8), "down", fid="last_drop", chevrons=3)
for (x, y) in cells(14, 2, 16, 8):
    path[y * W + x] = 0
for x in range(14, 17):
    m["triggers"].append({"id": f"finish_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 8},
                          "activation": "step_on", "ref": "script.wickrun_finish"})
owed.append("script.wickrun_finish")
obj("finish_arch", "wickrun_start_gate", (14, 7), 3, 2, overhang=1, solid=False)
obj("finish_lamp_w", "tinderwick_lamp_post", (12, 8), 1, 3, overhang=2, walk_under=True)
obj("finish_lamp_e", "tinderwick_lamp_post", (18, 8), 1, 3, overhang=2, walk_under=True)

# ---- warps ---------------------------------------------------------------------------
for i, x in enumerate((14, 15)):
    m["warps"].append({"id": "to_lower" + ("_e" if i else ""), "at": {"tx": x, "ty": 0},
                       "trigger": "step_on", "to_map": "wickrun_lower",
                       "to": {"tx": x + 6, "ty": 43}, "facing": "up", "transition": "fade"})
for i, y in enumerate((21, 22)):
    m["warps"].append({"id": "to_point" + ("_s" if i else ""), "at": {"tx": W - 1, "ty": y},
                       "trigger": "step_on", "to_map": "pearlmoor_point",
                       "to": {"tx": 0, "ty": y - 13}, "facing": "right", "transition": "fade"})

# ---- 2. the Tallow Lift's foot station ------------------------------------------------
LX, LY = 20, 9                       # 4x4; art in cols 0-2, rows 0-1 are only the cable
obj("lift_foot", "wickrun_lift_house_foot", (LX, LY), 4, 4, overhang=2, walk_under=True)
m["triggers"].append({"id": "lift_foot_door", "kind": "cutscene",
                      "at": {"tx": LX + 1, "ty": LY + 3}, "activation": "interact",
                      "ref": "script.tallow_lift_foot"})
owed.append("script.tallow_lift_foot")
m["npcs"].append({"id": "lift_keeper", "at": {"tx": 24, "ty": 13}, "facing": "left",
                  "sprite": "old_salt", "movement": "static",
                  "dialogue_ref": "script.tallow_lift_foot"})
owed += pt.sign(m, deco, W, sid="wickrun_foot_lift", at=(19, 12))
obj("lift_pylon_a", "wickrun_lift_pylon", (22, 4), 1, 4, overhang=3, walk_under=True)
obj("lift_pylon_b", "wickrun_lift_pylon", (24, 0), 1, 4, overhang=3, walk_under=True)

# ---- 3. the wax-yard + the bench ------------------------------------------------------
obj("yard_bench", "interior_pew", (16, 15), 3, 1)
m["triggers"].append({"id": "yard_bench", "kind": "cutscene", "at": {"tx": 17, "ty": 15},
                      "activation": "interact", "ref": "script.wickrun_foot_rest"})
owed.append("script.wickrun_foot_rest")
obj("runner_rack", "wickrun_runner_rack", (10, 9), 2, 2)
obj("yard_barrels_a", "wickrun_wax_barrels", (4, 12), 2, 1)
obj("yard_barrels_b", "wickrun_wax_barrels", (6, 12), 2, 1)
obj("yard_barrels_c", "wickrun_wax_barrels", (4, 15), 2, 1)
obj("yard_wreck", "wickrun_wax_cart_wreck", (8, 14), 2, 2)
obj("yard_wood", "tinderwick_woodpile", (11, 16), 2, 1)
obj("yard_crates", "pearlmoor_fish_crates", (3, 17), 1, 1)
obj("yard_crates_b", "pearlmoor_fish_crates", (12, 13), 1, 1)
mk.fence_run(deco, W, H, 3, 19, 9)
obj("yard_lamp", "tinderwick_lamp_post", (7, 15), 1, 3, overhang=2, walk_under=True)
obj("shore_lamp", "tinderwick_lamp_post", (22, 18), 1, 3, overhang=2, walk_under=True)
obj("yard_tree", "tinderwick_tree_b", (24, 14), 3, 4, overhang=3, walk_under=True)
obj("yard_pine", "windward_bent_pine", (2, 12), 2, 3, overhang=2, walk_under=True)
# the barrow-stand where the wax was loaded for the beach road east
obj("barrow_barrels", "wickrun_wax_barrels", (19, 17), 2, 1)
obj("barrow_crates", "pearlmoor_fish_crates", (21, 17), 1, 1)
obj("shore_pine", "windward_bent_pine", (12, 17), 2, 3, overhang=2, walk_under=True)
m["npcs"].append({"id": "rook_foot", "at": {"tx": 13, "ty": 12}, "facing": "down",
                  "sprite": "road_courier", "movement": "look_around",
                  "requires_flag": "flag:runner_rook_beaten",
                  "dialogue_ref": "script.rook_foot"})
owed.append("script.rook_foot")
m["npcs"].append({"id": "wax_yard_hand", "at": {"tx": 5, "ty": 14}, "facing": "right",
                  "sprite": "fisher_woman", "movement": "look_around",
                  "dialogue_ref": "npc.wickrun_yard_hand"})
owed.append("npc.wickrun_yard_hand")
owed += pt.sign(m, deco, W, sid="wickrun_foot", at=(13, 10))
for (x, y) in [(6, 22), (13, 21), (26, 24), (11, 26), (21, 27)]:
    if water[y * W + x]:
        deco[y * W + x] = gid("buoy")
    elif not path[y * W + x]:
        deco[y * W + x] = gid("boulder")

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": above},
]

covered = set(pin) | {(x, y) for y in range(H) for x in range(W)
                      if any(g[y * W + x] for g in (tree, path, sand, water, deco))}
objcells = {(x, y) for o in m["objects"]
            for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
            for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.10, avoid=covered | objcells | busy)

if __name__ == "__main__":
    mk.deep_water(m)
    ok = mk.finalize(m, scale=3, pin_base=pin)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
