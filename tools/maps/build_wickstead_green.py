#!/usr/bin/env python3
"""
Wickstead Green (wickstead_green) — the village LAMP-SCHOOL's green, one step
WEST of Duskapple Orchard (2026-10, the tutorial zone).

An OPTIONAL, SAFE side area for a first-timer (or anyone who's been away a
while) to learn how Vesperholm works from friendly people, in-world:

  * THE LAMP-SCHOOL (`wickstead_school`, a generated 7x4 schoolhouse with a
    bell-cupola) under a low bluff — inside, a teacher per desk/corner teaches
    one mechanic each (types at the chalkboard, catching, statuses, kindling &
    bond, the Hearth with the Hearthkeeper herself, resting).
  * the schoolyard's OUTDOOR lessons: Wayfarer Esk by the pond (Lantern Gifts
    — the pond IS the lesson: night-water you'll cross with Tidecall one day),
    Bunce at the tuck-shop stall (wicks, shops, selling, Star-charts), and the
    pupil Odo (the JOURNAL / MAP / LORE / REGISTER menus).
  * a fenced school garden, a woodpile and a well; the notice board carries the
    day's timetable (a map of who teaches what).

Reachable from the very start (the orchard's west mouth is ungated), and SAFE:
no encounter zones here at all; the only wild grass on the way is the
orchard's own lv 2-4 meadow, which is OFF the central ride (and inert before
the starter — wild encounters never fire with an empty party). Nothing here
gates anything: the golden thread never comes this way.

Wiring: `to_orchard(_s)` (23, 8-9) -> duskapple_orchard (0, 8-9) facing right;
the orchard's `to_wickstead(_s)` (0, 8-9) lands ON (23, 8-9) facing left.
Compass-true: you walk WEST out of the orchard and arrive on this map's EAST
edge. The school door (10, 6) -> wickstead_school (8, 10); its doormat lands
back on the door's apron (10, 7).

Ambience is authored here (not via worldcraft/<region>.py) so the new area is
complete in one builder; it's look-only and the map is post-Chickenpig content.

Run:  python3 tools/maps/build_wickstead_green.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 18
rng = random.Random(4417)
owed: list[str] = []

tree = mk.make_grid(W, H)
cliff = mk.make_grid(W, H)
path = mk.make_grid(W, H)
pond = mk.make_grid(W, H)

# ---- the enclosure: deep tree border, a low bluff behind the school, east mouth -----
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(2, 4, 2), (21, 3, 2), (2, 15, 2), (21, 14, 2)], rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)                 # south wood (rows 16-17)
# the elevation accent: a low bluff the school is tucked under (the cliff family's
# top = plateau, its S edge = the lit face), organic along its foot
mk.rect(cliff, W, H, 6, 0, 14, 1)
mk.blob(cliff, W, H, 10, 1.6, 3.6, 1.1)
for i in range(W * H):
    if cliff[i]:
        tree[i] = 0
# the east mouth back to the orchard (rows 8-9) + its shoulders
for y in (7, 8, 9, 10):
    for x in (21, 22, 23):
        if y in (8, 9) or x == 21:
            tree[y * W + x] = 0

# ---- the school + its lanes --------------------------------------------------------
m: dict = {
    "id": "wickstead_green", "display_name": "Wickstead Green",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/tinderwick-a.mp3",
    "ambience": {
        "particles": [{"kind": "glowmotes", "density": 0.4},
                      {"kind": "leaves", "density": 0.3}],
    },
}
SCHOOL_AT = (7, 3)
approach = pt.building(m, path, W, H, oid="school", sprite="wickstead_school",
                       at=SCHOOL_AT, overhang=2, to_map="wickstead_school", to=(8, 10),
                       apron_rows=1)
assert approach == (10, 7), approach
# the main street: from the east mouth west along the school front to the notice board
mk.rect(path, W, H, 4, 8, W - 1, 9)
# a spur down to the pond's edge (the Lantern-Gift lesson)
mk.vline(path, W, H, 9, 10, 12)

# the school pond — NIGHT-WATER (pond = Tidecall-gated tiles): the lesson's prop
mk.rect(pond, W, H, 3, 11, 7, 13)       # the drawn pond family reads best as a clean basin

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

# ---- objects: crown trees on the tree-line, lamps on the lanes, yard props ----------
for oid, sprite, at in [
    ("tree_w", "tinderwick_tree", (0, 3)),
    ("tree_ne", "tinderwick_tree", (19, 0)),
    ("tree_sw", "tinderwick_tree", (0, 12)),
    ("tree_se", "tinderwick_tree", (21, 12)),
    ("tree_yard", "tinderwick_tree", (10, 13)),   # the yard's shade tree
]:
    pt.crown_tree(m, oid=oid, sprite=sprite, at=at)
for oid, at in [("lamp_school", (6, 4)), ("lamp_mouth", (19, 5)), ("lamp_pond", (10, 9))]:
    m["objects"].append({"id": oid, "sprite": "tinderwick_lamp_post",
                         "at": {"tx": at[0], "ty": at[1]}, "w": 1, "h": 3, "overhang": 2,
                         "walk_under": True})
# the tuck-shop stall (Bunce: wicks & shops), the woodpile, the well, the notice board
m["objects"] += [
    {"id": "tuck_stall", "sprite": "lowleaf_stall", "at": {"tx": 15, "ty": 5},
     "w": 2, "h": 2, "overhang": 1},
    {"id": "woodpile", "sprite": "tinderwick_woodpile", "at": {"tx": 14, "ty": 4},
     "w": 2, "h": 1},
    {"id": "well", "sprite": "tinderwick_well", "at": {"tx": 19, "ty": 10},
     "w": 2, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "timetable", "sprite": "tinderwick_notice_board", "at": {"tx": 4, "ty": 5},
     "w": 2, "h": 2, "overhang": 1},
    {"id": "apple_crates", "sprite": "tinderwick_apple_crates", "at": {"tx": 13, "ty": 10},
     "w": 2, "h": 1},
]

# the notice board reads as the day's timetable (both its body tiles)
for x in (4, 5):
    m["triggers"].append({"id": f"timetable_{x}", "kind": "sign", "at": {"tx": x, "ty": 6},
                          "activation": "interact", "ref": "sign.school_timetable"})
owed.append("sign.school_timetable")
owed += pt.sign(m, deco, W, sid="wickstead_green", at=(21, 7))
# the detour under the bluff pays: the school's lost-property box (a balm and a
# mitten nobody has claimed since the dusk fell)
owed += pt.cache(m, cid="school_lost_property", at=(17, 3))

# the school garden: slat fences + end posts, beds inside, open on its west side
mk.fence_run(deco, W, H, 14, 12, 17)
mk.fence_run(deco, W, H, 14, 14, 17)
deco[13 * W + 17] = gid("fence_post")
for (x, y) in [(15, 13), (16, 13)]:
    deco[y * W + x] = gid("flowerbed_a") if (x + y) % 2 else gid("flowerbed_b")
deco[13 * W + 14] = gid("flowers")
# a boulder cluster on the pond's far bank, and two by the bluff's foot
for (x, y) in [(3, 10), (8, 14), (2, 13), (5, 3), (15, 3)]:
    if not (tree[y * W + x] or pond[y * W + x] or cliff[y * W + x] or path[y * W + x]):
        deco[y * W + x] = gid("boulder")

# ---- the people of the green ----------------------------------------------------------
m["npcs"] += [
    # LANTERN GIFTS — a wayfarer back for a visit, at the pond's edge (the lesson's prop)
    {"id": "teacher_gifts", "at": {"tx": 8, "ty": 12}, "facing": "left",
     "sprite": "pass_walker", "movement": "static", "dialogue_ref": "script.school_gifts"},
    # WICKS & SHOPS — the tuck-shop trader at her stall
    {"id": "teacher_wicks", "at": {"tx": 17, "ty": 6}, "facing": "down",
     "sprite": "market_trader", "movement": "static", "dialogue_ref": "script.school_wicks"},
    # THE MENUS — a pupil who knows his pack better than his sums
    {"id": "pupil_menus", "at": {"tx": 16, "ty": 10}, "facing": "down",
     "sprite": "village_child", "movement": "look_around", "dialogue_ref": "script.school_menus"},
    # colour: a kite-flying pupil skiving off in the yard
    {"id": "pupil_kite", "at": {"tx": 6, "ty": 15}, "facing": "down",
     "sprite": "kite_child", "movement": "wander", "dialogue_ref": "npc.school_yard_kid"},
]

# ---- warps: the east mouth back to the orchard -----------------------------------------
for y, sfx in ((8, ""), (9, "_s")):
    m["warps"].append({"id": f"to_orchard{sfx}", "at": {"tx": W - 1, "ty": y},
                       "trigger": "step_on", "to_map": "duskapple_orchard",
                       "to": {"tx": 0, "ty": y}, "facing": "right", "transition": "fade"})

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

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
