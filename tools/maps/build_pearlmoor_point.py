#!/usr/bin/env python3
"""
Lightkeeper's Point (pearlmoor_point) — R9 "The Old Light".

A small headland off the WEST beach of Pearlmoor Quay: the quay's sand strip
runs out past the purse-cache rocks onto a grassy point with the sea on two
sides. On it stands Pearlmoor's second lighthouse, THE OLD LIGHT — which hasn't
shone in eleven winters. Where its lamp should be sits a grinning brass
ear-trumpet: MR. PUNCHWHEEL, Tam Wash's clockwork joke-engine. The quay calls it
the Guffaw. The tower (`pearlmoor_oldlight_1..6/_top`, build_pearlmoor_oldlight.py)
is the middle leg of the Causeway Bell chain (walkthrough/01-south.md).

Also here: the shuttered WASH FERRY-HOUSE (boarded window, a mailbox stuffed
with eleven winters of quay newsletters), a sea-view bench, the jest-house sign,
a small cache on the sand behind the tower, and Nettie Fret (the Worry Club's
Pearlmoor member — `script.worry_nettie`, authored elsewhere).

A SAFE spur (no encounters, no trainers — the allotment precedent).

Wiring:
  quay `to_point` (0,15-17)  ->  HERE (18,7-9) facing left; our `to_quay`
  (19,7-9) -> quay (1,15-16) facing right (the purse cache sits on (1,17)).
  The Old Light door (3,7) -> pearlmoor_oldlight_1 (7,9); gated on
  flag:q_south_bell with `door.oldlight_locked` (the brass-nose line). The top
  floor's SLIDE lands on (7,8); the brass chute-mouth at (7,7) climbs back up
  (gated flag:q_south_jest_done — the round-trip pair the warp audit wants).
  After gleam:tide the tower shows LIT (oldlight_dark/oldlight_lit swap, same
  footprint).

Run:  python3 tools/maps/build_pearlmoor_point.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 14
rng = random.Random(9119)
owed: list[str] = []

tree = mk.make_grid(W, H)
water = mk.make_grid(W, H)
sand = mk.make_grid(W, H)
path = mk.make_grid(W, H)

# ---- the sea: west tip + the whole south side -------------------------------
mk.rect(water, W, H, 0, 0, 0, H - 1)
mk.rect(water, W, H, 0, 11, W - 1, H - 1)
mk.blob(water, W, H, 2.5, 12.5, 2.5, 1.6)
mk.blob(water, W, H, 16, 12.2, 3.0, 1.4)
# the beach ring the sea laps onto (water needs a SAND shore — context rule)
mk.rect(sand, W, H, 1, 1, 1, 10)
mk.rect(sand, W, H, 1, 9, W - 1, 10)
mk.blob(sand, W, H, 9, 9.4, 3.2, 1.0)
# two small bays bite into the beach (an organic shore, not a ruled edge)
mk.blob(water, W, H, 4.5, 10.6, 1.7, 0.8)
mk.blob(water, W, H, 16.5, 10.7, 1.6, 0.8)

# ---- the land's back: a tree mass along the north and the east shoulder -------
mk.organic_border(tree, W, H, top=1, depth=2,
                  bumps=[(10, 2, 1), (17, 2, 1)], rng=rng)
mk.rect(tree, W, H, 16, 0, W - 1, 6)       # east shoulder above the entrance
mk.rect(tree, W, H, 10, 0, W - 1, 2)       # the wood crowds in behind the ferry-house
for x in range(2, 7):                       # the tower stands proud of the trees
    tree[0 * W + x] = 0
    tree[1 * W + x] = 0
# the east mouth (rows 7-9) stays open to the quay's beach
for y in (7, 8, 9):
    for x in (W - 2, W - 1):
        tree[y * W + x] = 0

# ---- the lane: east mouth -> ferry-house -> the Old Light's door ----------------
mk.rect(path, W, H, 3, 8, W - 1, 8)
mk.rect(path, W, H, 13, 7, 13, 7)          # the ferry-house step (shuttered)

for i in range(W * H):
    if water[i]:
        sand[i] = 1          # the sea lies OVER sand: its shore pieces meet sand, never grass
        tree[i] = 0
        path[i] = 0
    if tree[i]:
        sand[i] = 0
        path[i] = 0

terrain_layers = [
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]
deco = mk.make_grid(W, H)

m: dict = {
    "id": "pearlmoor_point", "display_name": "Lightkeeper's Point",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/pearlmoor-quay-b.mp3",
}

# ---- THE OLD LIGHT (5x8; the door is the art's col 1) -----------------------------
TOWER = (2, 0)
DOOR = (TOWER[0] + 1, TOWER[1] + 7)        # (3,7)
for oid, sprite, flagk in (("oldlight", "pearlmoor_oldlight_dark", "hidden_when_flag"),
                           ("oldlight_lit", "pearlmoor_oldlight_lit", "requires_flag")):
    m["objects"].append({"id": oid, "sprite": sprite,
                         "at": {"tx": TOWER[0], "ty": TOWER[1]}, "w": 5, "h": 8,
                         "overhang": 5, flagk: "gleam:tide"})
m["warps"].append({"id": "to_oldlight", "at": {"tx": DOOR[0], "ty": DOOR[1]},
                   "trigger": "step_on", "to_map": "pearlmoor_oldlight_1",
                   "to": {"tx": 7, "ty": 9}, "facing": "up", "transition": "door",
                   "requires_flag": "flag:q_south_bell",
                   "blocked_ref": "door.oldlight_locked"})

# the slide's brass chute-mouth at the tower foot (non-solid prop; its warp
# climbs back up the chute once the act is done — gated, with a line)
m["objects"].append({"id": "chute_mouth", "sprite": "solarium_sun_mask",
                     "at": {"tx": 7, "ty": 7}, "w": 1, "h": 1, "solid": False})
m["warps"].append({"id": "up_chute", "at": {"tx": 7, "ty": 7}, "trigger": "step_on",
                   "to_map": "pearlmoor_oldlight_top", "to": {"tx": 7, "ty": 8},
                   "facing": "up", "transition": "fade",
                   "requires_flag": "flag:q_south_jest_done",
                   "blocked_ref": "sign.oldlight_chute"})

# ---- the Wash ferry-house (shuttered: no door warp, the door just answers) -------
m["objects"].append({"id": "ferryhouse", "sprite": "pearlmoor_ferryhouse",
                     "at": {"tx": 11, "ty": 3}, "w": 5, "h": 5, "overhang": 2})
m["triggers"].append({"id": "ferryhouse_door", "kind": "sign",
                      "at": {"tx": 13, "ty": 7}, "activation": "interact",
                      "ref": "sign.wash_ferryhouse"})
owed.append("sign.wash_ferryhouse")
# (13,7) is in the house footprint (solid) — the player reads it from (13,8)
owed += pt.sign(m, deco, W, sid="wash_mailbox", at=(16, 7))
owed += pt.sign(m, deco, W, sid="oldlight", at=(6, 9))

# ---- the sea-view bench + Nettie, the cache behind the tower ------------------------
m["objects"].append({"id": "bench", "sprite": "interior_pew",
                     "at": {"tx": 9, "ty": 10}, "w": 3, "h": 1})
m["triggers"].append({"id": "bench_view", "kind": "sign", "at": {"tx": 10, "ty": 10},
                      "activation": "interact", "ref": "sign.point_bench"})
owed.append("sign.point_bench")
m["npcs"].append({"id": "worry_nettie", "at": {"tx": 13, "ty": 10}, "facing": "up",
                  "sprite": "npc_woman", "movement": "look_around",
                  "dialogue_ref": "script.worry_nettie"})
owed += pt.cache(m, cid="point_rocks", at=(1, 2))

# lamps on the lane + a crown tree for depth
for i, x in enumerate((9,)):
    m["objects"].append({"id": f"lamp_{i}", "sprite": "tinderwick_lamp_post",
                         "at": {"tx": x, "ty": 5}, "w": 1, "h": 3, "overhang": 2,
                         "walk_under": True})
# (no crown tree: the meadow between tower and house stays open ground)

# offshore: the Point's own buoy line (dark — the Old Light's job, once)
for (x, y) in [(5, 12), (11, 13), (15, 12), (18, 13)]:
    deco[y * W + x] = gid("buoy")
for (x, y) in [(1, 10), (18, 10), (19, 10), (8, 10)]:
    deco[y * W + x] = gid("boulder")

# ---- warps: the beach road back to the quay (every walkable edge tile) -------------
for y, ly in ((7, 15), (8, 16), (9, 16)):
    m["warps"].append({"id": f"to_quay_{y}", "at": {"tx": W - 1, "ty": y},
                       "trigger": "step_on", "to_map": "pearlmoor_quay",
                       "to": {"tx": 1, "ty": ly}, "facing": "right",
                       "transition": "fade"})

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
                                                or sand[y * W + x] or water[y * W + x]})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
