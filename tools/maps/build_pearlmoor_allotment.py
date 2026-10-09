#!/usr/bin/env python3
"""
Hillside Allotments (pearlmoor_allotment) — the way up to S5 "Not All Who Wander".

Up the hill behind Pearlmoor Quay, through the gap between the Lumenary and the
Lifting House: Rod and Anth's veg plot (the allotment Rod brags about in
`script.booji_rod`), and at the top, where the old wood begins, a lichened
WAYSTONE with the last word of a famous line worn away. Typing that word
(`script.wander_stone`, askName store:false) sets `flag:q_south_wander_word`
and opens the gated gap behind the stone into `pearlmoor_wanderwood`.

A SAFE spur (no encounters, no trainers — the gloamwood_dell precedent): it's
always walkable, so a player who wanders up before the quest finds the plot,
Anth, and the stone as a tease.

Wiring:
  quay `to_allotment(_e)` (17-18,0) -> HERE (9-10,14);  our `to_quay(_e)`
  (9-10,15) -> quay (17-18,1). Landings sit within 1 of the return warps.
  `to_wood(_e)` (9-10,0) -> wanderwood (13-14,22), gated on the word flag with
  `blocked_ref: sign.wander_gap`; the wood's `to_allotment(_e)` lands on (9-10,1).

Run:  python3 tools/maps/build_pearlmoor_allotment.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 16
rng = random.Random(4163)
owed: list[str] = []

tree = mk.make_grid(W, H)
path = mk.make_grid(W, H)

# the old wood crowds the hilltop (deep top band) and walls the sides
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(3, 3, 1), (16, 3, 1), (2, 13, 1), (17, 12, 1)], rng=rng)
mk.rect(tree, W, H, 0, 2, W - 1, 2)          # the wood's edge: a third row up top
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)  # south treeline (the quay's back fence)

# the south mouth down to the quay, and the lane up the hill
for y in (14, 15):
    for x in (9, 10):
        tree[y * W + x] = 0
mk.rect(path, W, H, 9, 3, 10, 15)

# the GAP behind the waystone — open ground the trees will only let you through
# once the stone has its word (the warp is flag-gated; the tiles stay walkable)
for y in (0, 1, 2):
    for x in (9, 10):
        tree[y * W + x] = 0
# (no trodden path through it — it should read as a close, untried gap)

# the waystone's footing (rows 1-3 under the cairn; the object is solid)
for y in (1, 2):
    for x in (11, 12):
        tree[y * W + x] = 0

# the plot path: a spur west off the lane to Rod & Anth's gate
mk.hline(path, W, H, 9, 7, 8)

for i in range(W * H):
    if tree[i]:
        path[i] = 0

terrain_layers = [
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]

gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]
deco = mk.make_grid(W, H)

m: dict = {
    "id": "pearlmoor_allotment", "display_name": "Hillside Allotments",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/pearlmoor-quay-b.mp3",
}

# ---- Rod & Anth's plot: fenced top and bottom, crop rows inside ------------------
mk.fence_run(deco, W, H, 2, 5, 7)
mk.fence_run(deco, W, H, 2, 12, 7)
for i, (x, y) in enumerate([(3, 6), (5, 6), (3, 9), (5, 9)]):
    m["objects"].append({"id": f"crops_{i}", "sprite": "galehigh_crop_rows",
                         "at": {"tx": x, "ty": y}, "w": 2, "h": 2, "overhang": 0})
# the east plot (a neighbour's, half-dug)
mk.fence_run(deco, W, H, 13, 11, 17)
m["objects"].append({"id": "crops_e", "sprite": "galehigh_crop_rows",
                     "at": {"tx": 14, "ty": 9}, "w": 2, "h": 2, "overhang": 0})
m["objects"].append({"id": "potting_stall", "sprite": "lowleaf_stall",
                     "at": {"tx": 14, "ty": 5}, "w": 2, "h": 2, "overhang": 1})

# ---- the waystone (the S5 lock) ---------------------------------------------------
m["objects"].append({"id": "waystone", "sprite": "windward_cairn",
                     "at": {"tx": 11, "ty": 1}, "w": 2, "h": 3, "overhang": 1})
for x in (11, 12):
    m["triggers"].append({"id": f"waystone_{x}", "kind": "cutscene",
                          "at": {"tx": x, "ty": 3}, "activation": "interact",
                          "ref": "script.wander_stone"})

# ---- lane lighting + a crown tree for depth ----------------------------------------
m["objects"].append({"id": "lamp_lane", "sprite": "tinderwick_lamp_post",
                     "at": {"tx": 11, "ty": 10}, "w": 1, "h": 3, "overhang": 2,
                     "walk_under": True})
pt.crown_tree(m, oid="tree_a", sprite="tinderwick_tree", at=(15, 2))

owed += pt.sign(m, deco, W, sid="pearlmoor_allotment", at=(8, 10))
# the potting-stall corner's payoff: something left under the bench
owed += pt.cache(m, cid="allotment_bench", at=(16, 8))

# ---- Anth, tending the marrows (three flag-disjoint stages, one tile) --------------
for nid, ref, req, hide in [
    ("anth", "npc.allotment_anth", None, "flag:q_south_wander"),
    ("anth_wander", "npc.allotment_anth_wander", "flag:q_south_wander", "flag:q_south_wander_done"),
    ("anth_done", "npc.allotment_anth_done", "flag:q_south_wander_done", None),
]:
    n = {"id": nid, "at": {"tx": 7, "ty": 8}, "facing": "left", "sprite": "npc_old_woman",
         "movement": "look_around", "dialogue_ref": ref}
    if req:
        n["requires_flag"] = req
    if hide:
        n["hidden_when_flag"] = hide
    m["npcs"].append(n)

# ---- warps ---------------------------------------------------------------------------
for x, sfx in ((9, ""), (10, "_e")):
    m["warps"].append({"id": f"to_quay{sfx}", "at": {"tx": x, "ty": 15}, "trigger": "step_on",
                       "to_map": "pearlmoor_quay", "to": {"tx": x + 8, "ty": 1},
                       "facing": "down", "transition": "fade"})
    m["warps"].append({"id": f"to_wood{sfx}", "at": {"tx": x, "ty": 0}, "trigger": "step_on",
                       "to_map": "pearlmoor_wanderwood", "to": {"tx": x + 4, "ty": 22},
                       "facing": "up", "transition": "fade",
                       "requires_flag": "flag:q_south_wander_word",
                       "blocked_ref": "sign.wander_gap"})

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

obj_cells = {(x, y) for o in m["objects"]
             for y in range(o["at"]["ty"], o["at"]["ty"] + o.get("h", 1))
             for x in range(o["at"]["tx"], o["at"]["tx"] + o.get("w", 1))}
mk.scatter_decor(deco, base, W, H, rng, density=0.08,
                 avoid=obj_cells | {(7, 8)} | {(x, y) for y in range(H) for x in range(W)
                                               if path[y * W + x] or tree[y * W + x]
                                               or 2 <= x <= 7 and 5 <= y <= 12})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
