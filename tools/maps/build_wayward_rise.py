#!/usr/bin/env python3
"""
Wayward Rise (wayward_rise) — the green hilltop NORTH of the Wanderwood, and
the old country hotel that stands on it: THE WAYWARD ARMS (2026-10).

A quiet reward beyond S5. The Wanderwood itself only opens on the waystone's
word (`flag:q_south_wander_word`), so this hilltop is something you find by
wandering further than the quest asked: leave the glade by the narrow path
north of the glade lamp, and the trees give out onto a lamplit green.

  * THE WAYWARD ARMS (`wayward_hotel`, a generated 8x6 two-storey stone hotel:
    bay windows, dormers, two chimneys, a hanging sign of a crossed staff and
    lantern) on an apron under a low bluff. Inside (`wayward_arms`, its own
    builder): the free bar, the fireside snug, the corner chair — and the
    stranger standing beside it (script.wayward_stranger, content/regions/hotel.ts).
    The hotel is a REST POINT (the scene ends in a `heal`), so its door wears the
    rest-lantern (WorldScene.HEAL_ENTRANCE_MAPS).
  * the PUB GARDEN on the east lawn: festoon lanterns over two plank tables,
    a fenced flower garden; the WELL and the woodpile on the west side; a
    lily-dark pond with a boulder cluster in the south-west.
  * the lane: up from the wood's mouth (19-20, 21), bending west to the door,
    lamp-posted and signed.

No wild encounters: a quiet place, nothing fought here (and no battle
backdrops in maps.ts for that reason).

Wiring (compass-true, world_geometry): the Wanderwood's `to_rise(_e)` (19-20, 0)
lands HERE at (19-20, 20) facing up; our `to_wood(_e)` (19-20, 21) lands on the
wood's (19-20, 1) facing down. The map sits straight north of the wood at the
same world x (3), filling the strip between it and the Lowleaf lane (y -152..-130).
The hotel door (11-12, 8 — the art's door spans cols 3-4 of the 8-wide sprite,
so BOTH tiles enter) -> wayward_arms (10, 11); its doormat lands back on (11, 9).

Ambience is authored here (look-only; post-Chickenpig content, the Wickstead
precedent), with window light pools via `light_sources_extra`.

Run:  python3 tools/maps/build_wayward_rise.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 22
rng = random.Random(5150)
owed: list[str] = []

tree = mk.make_grid(W, H)
cliff = mk.make_grid(W, H)
path = mk.make_grid(W, H)
pond = mk.make_grid(W, H)

# ---- the enclosure: deep wood on three sides, the wood's mouth in the south ----------
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(2, 9, 2), (21, 6, 1), (2, 17, 1), (22, 14, 2)], rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)               # the Wanderwood's crown (south)
# the mouth down into the wood (cols 19-20) + soft shoulders
for y in range(H - 3, H):
    for x in (18, 19, 20, 21):
        if x in (19, 20) or y == H - 3:
            tree[y * W + x] = 0
# the wood closes in a little deeper behind the hotel (no bluff: a free-standing
# cliff mass on a green reads as a grey slab — level-design §11 r8)
mk.organic_border(tree, W, H, top=1, depth=3, bumps=[(4, 3, 1), (18, 3, 1)], rng=rng)

# ---- the hotel + its lane ------------------------------------------------------------
m: dict = {
    "id": "wayward_rise", "display_name": "Wayward Rise",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/lowleaf-hollow-b.mp3",
    "ambience": {
        "particles": [{"kind": "glowmotes", "density": 0.5},
                      {"kind": "leaves", "density": 0.25}],
        "mist": {"color": "#a8c8b0", "alpha": 0.05, "speed": 3},
        # the hotel's lit windows pool warm light on the green
        "light_sources_extra": [
            {"at": {"tx": 9, "ty": 8}, "radius": 2, "color": "#ffc070"},
            {"at": {"tx": 14, "ty": 8}, "radius": 2, "color": "#ffc070"},
            {"at": {"tx": 18, "ty": 6}, "radius": 2, "color": "#ffb060"},
        ],
    },
}
HOTEL_AT = (8, 3)
approach = pt.building(m, path, W, H, oid="hotel", sprite="wayward_hotel",
                       at=HOTEL_AT, overhang=3, door_col=3, to_map="wayward_arms",
                       to=(10, 11), apron_rows=2)
assert approach == (11, 9), approach
# the art's door spans BOTH cols 3-4: twin the door warp so either half enters
door = next(w for w in m["warps"] if w["id"] == "enter_hotel")
m["warps"].append({**door, "id": "enter_hotel_e", "at": {"tx": 12, "ty": 8}})


def lane(points):
    """A 2-wide 4-connected dirt lane through the waypoints (a 2x2 brush)."""
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        x, y = x0, y0
        while True:
            for dx in (0, 1):
                for dy in (0, 1):
                    if 0 <= x + dx < W and 0 <= y + dy < H:
                        path[(y + dy) * W + x + dx] = 1
            if (x, y) == (x1, y1):
                break
            if abs(x1 - x) >= abs(y1 - y):
                x += 1 if x1 > x else -1
            else:
                y += 1 if y1 > y else -1


# up from the wood's mouth, bending west to the hotel's apron
lane([(19, H - 1), (19, 13), (12, 13), (12, 11)])

# the dark pond in the south-west hollow (pond = Tidecall water: a look, not a road)
mk.blob(pond, W, H, 5.5, 16.0, 3.3, 2.4)

for i in range(W * H):
    if tree[i] or cliff[i]:
        pond[i] = 0
        path[i] = 0
    if pond[i]:
        path[i] = 0

terrain_layers = [
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_pond", "role": "terrain", "terrain": "pond",
     "set": "vesper_overworld_set", "depth": 0, "data": pond},
]

gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]
deco = mk.make_grid(W, H)

# ---- objects: crown trees, lamps, the pub garden, the well --------------------------
for oid, sprite, at in [
    ("tree_nw", "tinderwick_tree_b", (2, 2)),
    ("tree_w", "tinderwick_tree", (1, 11)),
    ("tree_ne", "tinderwick_tree", (19, 1)),
    ("tree_e", "tinderwick_tree_c", (21, 9)),
    ("tree_s", "tinderwick_tree_b", (12, 16)),
]:
    pt.crown_tree(m, oid=oid, sprite=sprite, at=at)
for oid, at in [("lamp_door", (7, 8)), ("lamp_bend", (17, 10)), ("lamp_mouth", (21, 17))]:
    m["objects"].append({"id": oid, "sprite": "tinderwick_lamp_post",
                         "at": {"tx": at[0], "ty": at[1]}, "w": 1, "h": 3, "overhang": 2,
                         "walk_under": True})
m["objects"] += [
    # the pub garden: festoon lanterns strung over two plank tables
    {"id": "festoon", "sprite": "pearlmoor_lantern_string", "at": {"tx": 17, "ty": 4},
     "w": 3, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "garden_table_a", "sprite": "wayward_garden_table", "at": {"tx": 16, "ty": 6},
     "w": 3, "h": 2},
    {"id": "garden_table_b", "sprite": "wayward_garden_table", "at": {"tx": 15, "ty": 16},
     "w": 3, "h": 2},
    # the west yard: the well, the woodpile, apple crates by the kitchen end
    {"id": "well", "sprite": "tinderwick_well", "at": {"tx": 4, "ty": 4},
     "w": 2, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "woodpile", "sprite": "tinderwick_woodpile", "at": {"tx": 5, "ty": 8},
     "w": 2, "h": 1},
    {"id": "crates", "sprite": "tinderwick_apple_crates", "at": {"tx": 6, "ty": 10},
     "w": 2, "h": 1},
]
# the garden plot under the bluff's east end: fenced, flowerbeds inside
mk.fence_run(deco, W, H, 16, 9, 20)
for x in (17, 18, 19):
    deco[8 * W + x] = gid("flowerbed_a") if x % 2 else gid("flowerbed_b")

# the lane sign + a boulder cluster on the pond's bank and under the bluff
owed += pt.sign(m, deco, W, sid="wayward_rise", at=(18, 16))
for (x, y) in [(3, 13), (7, 17), (8, 14), (2, 15), (5, 2), (17, 2), (10, 13)]:
    i = y * W + x
    if not (tree[i] or pond[i] or cliff[i] or path[i]):
        deco[i] = gid("boulder")

# ---- warps: the mouth back down into the Wanderwood ---------------------------------
for x, sfx in ((19, ""), (20, "_e")):
    m["warps"].append({"id": f"to_wood{sfx}", "at": {"tx": x, "ty": H - 1},
                       "trigger": "step_on", "to_map": "pearlmoor_wanderwood",
                       "to": {"tx": x, "ty": 1}, "facing": "down", "transition": "fade"})

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

obj_cells = {(x, y) for o in m["objects"]
             for y in range(o["at"]["ty"], o["at"]["ty"] + o.get("h", 1))
             for x in range(o["at"]["tx"], o["at"]["tx"] + o.get("w", 1))}
npc_cells = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.16,
                 avoid=obj_cells | npc_cells | {(x, y) for y in range(H) for x in range(W)
                                                if path[y * W + x] or tree[y * W + x]
                                                or cliff[y * W + x] or pond[y * W + x]},
                 flowers=0.35)

# audit_flow: one portal (the wood's mouth) + the hotel door — a cul-de-sac by
# design; its payoff is the hotel (a rest point and the stranger's scene).
if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
