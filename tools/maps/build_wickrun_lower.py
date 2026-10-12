#!/usr/bin/env python3
"""
The Wick-Run: the Lower Run (09-the-wild-ways §2 A; kind route, region west,
band 48-50, `ride: true`). The fast bottom half of the old wax road, where the
carts used to pick up the speed that carried them to the sea.

One idea per screen (§3a r5):
  1. THE LONG STRAIGHT (rows 0-17): the run's fastest drop. A kicker in the
     middle of the road clears a boulder pair (or steer round it), and a
     SIDE-kicker off the east verge clears a crevice onto a high ledge you can
     see from the straight — the carters' old brake-hut shelf, a ramp-only cache.
  2. THE STEPS (rows 18-23): two one-way ledge lines across a flat shelf —
     hop, hop — onto...
  3. THE CROSS-SLOPE (rows 24-25): a fast `slope dir:right` straight east
     across the mountain, round the corner and down the second straight
     (another kicker), to...
  4. THE RUNNERS' CAMP (rows 37-39): the last landing — racks, a brazier,
     barrels, and ROOK, the Runners' captain, who stands where every rider must
     pass to reach the final drop to the foot.

One-way: the long straight is a full-width chute band below the entry landing;
the steps are ledges; the cross-slope and the second straight carry you on.

HANDSHAKE: north `to_traverse`/`_e` (8,0)/(9,0) <-> wickrun_traverse's
`to_lower` (8,29)/(9,29) (each lands ON the other); south `to_foot`/`_e`
(20,43)/(21,43) -> wickrun_foot (14,0)/(15,0), whose return warps land ON these.
Geometry: x -57..-29, y -140..-96.

Run:  python3 tools/maps/build_wickrun_lower.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 28, 44
rng = random.Random(9065)
owed: list[str] = []

tree = mk.make_grid(W, H)
path = mk.make_grid(W, H)
tallgrass = mk.make_grid(W, H)
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)

mk.rect(tree, W, H, 0, 0, W - 1, H - 1)
OPEN: set[tuple[int, int]] = set()


def cells(x0, y0, x1, y1):
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}


def carve(x0, y0, x1, y1):
    OPEN.update(cells(x0, y0, x1, y1))


carve(8, 0, 9, 0)            # the road in from the traverse
carve(5, 1, 12, 3)           # the entry landing
carve(6, 4, 11, 17)          # 1. the long straight
carve(13, 11, 16, 14)        #    the brake-hut shelf (ramp-only)
carve(15, 15, 15, 17)        #    the shelf's drain back into the run
carve(4, 18, 17, 23)         # 2. the steps
carve(4, 24, 19, 25)         # 3. the cross-slope
carve(6, 26, 14, 30)         #    the old cart siding below the cross-slope
carve(20, 24, 23, 36)        #    the second straight
carve(8, 37, 25, 39)         # 4. the Runners' camp
carve(20, 40, 21, 43)        #    the final drop + the road to the foot
for (x, y) in OPEN:
    tree[y * W + x] = 0

pin: dict = {}
m: dict = {
    "id": "wickrun_lower", "display_name": "The Wick-Run",
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


# ---- 1. the long straight + its two kickers ---------------------------------------
wk.chute(m, pin, deco, W, cells(6, 4, 11, 17), "down", fid="long_straight", chevrons=4)
for x in (8, 9):                                   # mid-road: clear the boulder pair
    wk.jump(m, deco, W, at=(x, 10), dir="down", length=3, jid=f"straight_kicker_{x}")
    deco[11 * W + x] = gid("boulder")
wk.jump(m, deco, W, at=(11, 13), dir="right", length=3, jid="shelf_kicker")
wk.chute(m, pin, deco, W, cells(15, 15, 15, 17), "down", fid="shelf_drain",
         berms=False, chevrons=2)

# ---- 2. the steps: two full-width ledge lines -------------------------------------
pt.ledge_run(deco, W, H, 20, 4, 17, rng)
pt.ledge_run(deco, W, H, 23, 4, 17, rng)

# ---- 3. the cross-slope + the second straight -------------------------------------
wk.chute(m, pin, deco, W, cells(4, 24, 19, 25), "right", fid="cross_slope", chevrons=4)
wk.chute(m, pin, deco, W, cells(20, 24, 23, 36), "down", fid="second_straight", chevrons=4)
for x in (21, 22):
    wk.jump(m, deco, W, at=(x, 30), dir="down", length=3, jid=f"second_kicker_{x}")
    deco[31 * W + x] = gid("boulder")
wk.chute(m, pin, deco, W, cells(20, 40, 21, 42), "down", fid="final_drop", chevrons=0)

# ---- flat ground ------------------------------------------------------------------
LANE = cells(6, 1, 11, 3) | cells(13, 12, 15, 13) | cells(8, 18, 15, 19) \
    | cells(6, 21, 15, 22) | cells(9, 37, 23, 38) | {(8, 0), (9, 0), (20, 43), (21, 43)}
for (x, y) in LANE:
    if (x, y) in OPEN and (x, y) not in pin:
        path[y * W + x] = 1
# grass: the steps' west ends, the camp's west lawn
for (x, y) in cells(4, 18, 7, 19) | cells(4, 21, 6, 22) | cells(16, 21, 17, 22) \
        | cells(8, 37, 11, 39) | cells(7, 27, 13, 30):
    tallgrass[y * W + x] = 1
for i in range(W * H):
    x, y = i % W, i // W
    if (x, y) not in OPEN or (x, y) in pin or deco[i]:
        tallgrass[i] = 0
    if tallgrass[i] or (x, y) in pin or deco[i]:
        path[i] = 0

# ---- warps -------------------------------------------------------------------------
for i, x in enumerate((8, 9)):
    m["warps"].append({"id": "to_traverse" + ("_e" if i else ""), "at": {"tx": x, "ty": 0},
                       "trigger": "step_on", "to_map": "wickrun_traverse",
                       "to": {"tx": x, "ty": 29}, "facing": "up", "transition": "fade"})
for i, x in enumerate((20, 21)):
    m["warps"].append({"id": "to_foot" + ("_e" if i else ""), "at": {"tx": x, "ty": H - 1},
                       "trigger": "step_on", "to_map": "wickrun_foot",
                       "to": {"tx": x - 6, "ty": 0}, "facing": "down", "transition": "fade"})

# ---- landmarks ----------------------------------------------------------------------
for i, (lx, ly) in enumerate([(5, 1), (12, 1), (5, 8), (12, 5), (18, 18), (24, 27),
                              (19, 33), (25, 37)]):
    obj(f"run_lamp_{i}", "tinderwick_lamp_post", (lx, ly), 1, 3, overhang=2, walk_under=True)
obj("brake_hut", "wickrun_runner_rack", (13, 11), 2, 2)          # the carters' old rack
obj("shelf_barrels", "wickrun_wax_barrels", (13, 14), 2, 1)
obj("lift_pylon_a", "wickrun_lift_pylon", (17, 8), 1, 4, overhang=3, walk_under=True)
obj("lift_pylon_b", "wickrun_lift_pylon", (24, 20), 1, 4, overhang=3, walk_under=True)
obj("lift_pylon_c", "wickrun_lift_pylon", (26, 33), 1, 4, overhang=3, walk_under=True)
obj("steps_tree", "tinderwick_tree_c", (1, 17), 3, 4, overhang=3, walk_under=True)
obj("steps_pine", "windward_bent_pine", (16, 18), 2, 3, overhang=2, walk_under=True)
# the Runners' camp
obj("camp_rack", "wickrun_runner_rack", (12, 37), 2, 2)
obj("camp_fire", "solarium_brazier_lit", (15, 36), 2, 3, overhang=1)
obj("camp_barrels", "wickrun_wax_barrels", (17, 39), 2, 1)
obj("camp_wood", "tinderwick_woodpile", (9, 39), 2, 1)
obj("camp_wreck", "wickrun_wax_cart_wreck", (23, 38), 2, 2)
obj("camp_tree", "tinderwick_tree_b", (5, 34), 3, 4, overhang=3, walk_under=True)
# the old cart siding: steer DOWN off the cross-slope onto the grass where the
# empties waited for the lift (a wreck, the siding's lamp, the rare Chandrek)
obj("siding_wreck", "wickrun_wax_cart_wreck", (12, 28), 2, 2)
obj("siding_lamp", "tinderwick_lamp_post", (6, 26), 1, 3, overhang=2, walk_under=True)
obj("siding_barrels", "wickrun_wax_barrels", (9, 30), 2, 1)
obj("siding_pine", "windward_bent_pine", (15, 27), 2, 3, overhang=2, walk_under=True)

# ---- trainers, caches, signs ---------------------------------------------------------
owed += pt.trainer_beat(m, tid="runner_rook", at=(24, 37), facing="left", sight=4,
                        sprite="road_courier")
owed += pt.cache(m, cid="wickrun_brake_hut", at=(15, 12))
owed += pt.sign(m, deco, W, sid="wickrun_lower", at=(6, 2))
owed += pt.sign(m, deco, W, sid="wickrun_camp", at=(19, 39))

# Run tables (shared shape down the whole run, bands rising): the run-only kin
# lead, with the Sunvault's lighter Solar/Verdant regulars. Average BST is kept
# on the dex's level trend so the progression model's wild-XP fit isn't tilted
# (tools/balance/progression.mjs `fit`) — the heavy hitters stay rare.
TABLE = [
    {"kin_id": 11, "weight": 24, "min_level": 48, "max_level": 50},  # Tallowcrest (run-only)
    {"kin_id": 6, "weight": 25, "min_level": 48, "max_level": 50},  # Wickmere (run-only)
    {"kin_id": 115, "weight": 14, "min_level": 48, "max_level": 50},  # Solvyne
    {"kin_id": 120, "weight": 12, "min_level": 48, "max_level": 50},  # Dawnfawn
    {"kin_id": 117, "weight": 12, "min_level": 48, "max_level": 50},  # Helibud
    {"kin_id": 19, "weight": 9, "min_level": 49, "max_level": 50},  # Warmantis (run-only)
    {"kin_id": 12, "weight": 4, "min_level": 50, "max_level": 50},  # Chandrek (rare)
]
DAY = [
    {"kin_id": 11, "weight": 22, "min_level": 57, "max_level": 64},  # Tallowcrest
    {"kin_id": 6, "weight": 20, "min_level": 57, "max_level": 64},  # Wickmere
    {"kin_id": 19, "weight": 16, "min_level": 58, "max_level": 64},  # Warmantis
    {"kin_id": 115, "weight": 14, "min_level": 57, "max_level": 64},  # Solvyne
    {"kin_id": 120, "weight": 12, "min_level": 57, "max_level": 64},  # Dawnfawn
    {"kin_id": 12, "weight": 8, "min_level": 59, "max_level": 64},  # Chandrek
    {"kin_id": 7, "weight": 8, "min_level": 60, "max_level": 64},  # Wicklord (day only)
]
night = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                           id_prefix="lower", table=TABLE)
for z in night:
    z["hidden_when_flag"] = "flag:dawn"
day = [{**z, "id": z["id"] + "_day", "table": DAY, "requires_flag": "flag:dawn"}
       for z in night]
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
