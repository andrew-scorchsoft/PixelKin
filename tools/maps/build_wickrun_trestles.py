#!/usr/bin/env python3
"""
The Wick-Run: the Trestles (09-the-wild-ways §2 A; kind route, region west,
band 47-48, `ride: true`). The run's middle: the old wax road spirals round a
knoll and crosses ITSELF on a timber trestle.

One idea per screen (§3a r5):
  1. THE SLALOM (rows 0-14): the road widens under the shelf and the Runners
     have staked it with wax barrels — three barrier lines with the gap on
     alternating sides. You can't brake uphill, so you steer: right, left, right.
  2. THE TRESTLE-HEAD (rows 15-20): a flat landing (a Runner, grass, a sign),
     then the drop onto the boards. You ride the trestle OVER the gully...
  3. THE HAIRPIN (rows 21-37): ...off its foot onto the knoll landing, round
     the knoll (dry lane + grass, the second Runner), back up the inside of the
     bend, and the road dives west UNDER the very trestle you just rode
     (`spans[] under:true`; the deck sits in the `above` layer, shade below).
  4. THE STEPS (rows 23-40, west): three terraces dropped by one-way LEDGES,
     the hop-off on alternating ends (fence + boulders bar the rest) — the run
     zig-zags down to the traverse. A Runner's dropped purse waits in a nook.

One-way: the slalom is a full-width chute band (nothing below can climb it),
the turn under the trestle is a west-carrying chute (nothing west of the
trestle can ride back east), and the terraces drop by ledges.

HANDSHAKE: north `to_chute`/`_e` (23,0)/(24,0) <-> wickrun_chute's
`to_trestles` (4,43)/(5,43) (each lands ON the other); west `to_traverse`/`_s`
(0,38)/(0,39) -> wickrun_traverse (29,14)/(29,15), whose return warps land ON
these. Geometry: x -27..1, y -194..-150.

Run:  python3 tools/maps/build_wickrun_trestles.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 28, 44
rng = random.Random(9063)
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


carve(23, 0, 24, 0)          # the road in from the chute
carve(19, 1, 26, 3)          # the entry landing
carve(14, 4, 25, 14)         # 1. the slalom
carve(5, 15, 25, 18)         # 2. the trestle-head landing
carve(12, 19, 13, 20)        #    the drop onto the boards
carve(12, 28, 13, 29)        #    the gully floor under the deck (the underpass)
carve(14, 24, 24, 27)        # 3. the top of the bend
carve(14, 28, 16, 29)        #    the turn in under the trestle
carve(21, 24, 24, 31)        #    the outside line round the knoll
carve(12, 32, 24, 37)        #    the knoll landing at the trestle's foot
carve(7, 28, 11, 29)         #    out from under, west
carve(1, 26, 6, 30)          # 4. terrace one
carve(1, 23, 3, 25)          #    the purse nook
carve(1, 31, 6, 31)          #    ledge line one
carve(1, 32, 9, 34)          #    terrace two
carve(1, 35, 9, 35)          #    ledge line two
carve(1, 36, 9, 40)          #    terrace three (the run-out)
carve(0, 38, 0, 39)          #    the road on to the traverse
for (x, y) in OPEN:
    tree[y * W + x] = 0

pin: dict = {}
m: dict = {
    "id": "wickrun_trestles", "display_name": "The Wick-Run",
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


# ---- 1. the slalom: a full-width chute staked with barrel barriers -------------
wk.chute(m, pin, deco, W, cells(14, 4, 25, 14), "down", fid="slalom", chevrons=4)
for i, (x0, y) in enumerate([(14, 7), (16, 7), (18, 7), (20, 7),       # gap east
                             (18, 10), (20, 10), (22, 10), (24, 10),   # gap west
                             (14, 13), (16, 13), (18, 13)]):           # gap east
    deco[y * W + x0] = deco[y * W + x0 + 1] = 0     # no chevron under a barrel
    obj(f"slalom_barrels_{i}", "wickrun_wax_barrels", (x0, y), 2, 1)

# ---- 2. the trestle-head + the drop + THE TRESTLE --------------------------------
wk.chute(m, pin, deco, W, cells(12, 19, 13, 20), "down", fid="drop", chevrons=0)
DECK = (12, 21, 2, 11)                      # x 12-13, rows 21-31
wk.deck(m, above, W, rect=DECK, axis="v", under=True, sid="trestle", shade=deco)
# the bend: in under the deck heading west, carried on out the far side
wk.chute(m, pin, deco, W, cells(14, 28, 16, 29), "left", fid="turn_under", chevrons=0)
wk.chute(m, pin, deco, W, cells(7, 28, 11, 29), "left", fid="out_west", chevrons=3)

# ---- 4. the steps: ledges with the hop-off on alternating ends -----------------
pt.ledge_run(deco, W, H, 31, 1, 2, rng)                 # terrace one drops at the WEST end
for x in range(3, 7):
    deco[31 * W + x] = gid("boulder")
pt.ledge_run(deco, W, H, 35, 8, 9, rng)                 # terrace two drops at the EAST end
mk.fence_run(deco, W, H, 1, 35, 7)

# ---- flat ground: lanes on the landings ------------------------------------------
LANE = (cells(20, 0, 25, 3) | cells(9, 15, 25, 18) | cells(12, 28, 13, 29)
        | cells(14, 24, 22, 27) | cells(21, 28, 22, 31) | cells(12, 32, 22, 34)
        | cells(1, 26, 6, 30) | cells(1, 32, 9, 34) | cells(0, 36, 9, 39))
LANE -= {(23, 0)}
for (x, y) in LANE:
    if (x, y) in OPEN:
        path[y * W + x] = 1
path[0 * W + 23] = path[0 * W + 24] = 1

# grass: the trestle-head's west end, the knoll's outside verge (a dry lane is
# left beside it), the knoll landing's south corner, and terrace three's east end
for (x, y) in cells(5, 15, 8, 18) | cells(23, 25, 24, 31) | cells(17, 35, 24, 37) \
        | cells(6, 38, 9, 40):
    tallgrass[y * W + x] = 1
for i in range(W * H):
    x, y = i % W, i // W
    if (x, y) not in OPEN or (x, y) in pin or deco[i]:
        tallgrass[i] = 0
    if tallgrass[i] or (x, y) in pin:
        path[i] = 0

# ---- warps -------------------------------------------------------------------------
for i, x in enumerate((23, 24)):
    m["warps"].append({"id": "to_chute" + ("_e" if i else ""), "at": {"tx": x, "ty": 0},
                       "trigger": "step_on", "to_map": "wickrun_chute",
                       "to": {"tx": x - 19, "ty": 43}, "facing": "up", "transition": "fade"})
for i, y in enumerate((38, 39)):
    m["warps"].append({"id": "to_traverse" + ("_s" if i else ""), "at": {"tx": 0, "ty": y},
                       "trigger": "step_on", "to_map": "wickrun_traverse",
                       "to": {"tx": 29, "ty": y - 24}, "facing": "left", "transition": "fade"})

# ---- landmarks --------------------------------------------------------------------
# the run's lantern line (verges + landings), the Tallow Lift's pylons striding
# down the knoll beside the road, crown trees on the knoll and the bends
for i, (lx, ly) in enumerate([(19, 1), (26, 1), (25, 15), (15, 15), (14, 32),
                              (24, 24), (1, 36), (3, 27)]):
    obj(f"run_lamp_{i}", "tinderwick_lamp_post", (lx, ly), 1, 3, overhang=2, walk_under=True)
obj("lift_pylon_a", "wickrun_lift_pylon", (20, 32), 1, 4, overhang=3, walk_under=True)
obj("lift_pylon_b", "wickrun_lift_pylon", (5, 37), 1, 4, overhang=3, walk_under=True)
obj("knoll_tree", "tinderwick_tree_b", (17, 28), 3, 4, overhang=3, walk_under=True)
obj("knoll_pine", "windward_bent_pine", (19, 25), 2, 3, overhang=2, walk_under=True)
obj("head_tree", "tinderwick_tree_c", (22, 15), 3, 4, overhang=3, walk_under=True)
obj("steps_pine", "windward_bent_pine", (4, 32), 2, 3, overhang=2, walk_under=True)
obj("head_barrels", "wickrun_wax_barrels", (18, 18), 2, 1)
obj("knoll_crates", "pearlmoor_fish_crates", (24, 33), 1, 1)
obj("steps_barrels", "wickrun_wax_barrels", (7, 32), 2, 1)
for (x, y) in [(20, 36), (13, 36), (2, 40), (8, 30), (19, 2)]:
    if (x, y) in OPEN and not deco[y * W + x]:
        deco[y * W + x] = gid("boulder")

# ---- trainers, cache, sign --------------------------------------------------------
owed += pt.trainer_beat(m, tid="runner_tamsin", at=(9, 17), facing="right", sight=4,
                        sprite="npc_girl")
owed += pt.trainer_beat(m, tid="runner_ossie", at=(24, 29), facing="left", sight=3,
                        sprite="npc_boy")
owed += pt.cache(m, cid="wickrun_purse", at=(2, 24))
owed += pt.sign(m, deco, W, sid="wickrun_trestle", at=(11, 18))
owed += pt.sign(m, deco, W, sid="wickrun_steps", at=(7, 27))

# Run tables (shared shape down the whole run, bands rising): the run-only kin
# lead, with the Sunvault's lighter Solar/Verdant regulars. Average BST is kept
# on the dex's level trend so the progression model's wild-XP fit isn't tilted
# (tools/balance/progression.mjs `fit`) — the heavy hitters stay rare.
TABLE = [
    {"kin_id": 11, "weight": 24, "min_level": 47, "max_level": 48},  # Tallowcrest (run-only)
    {"kin_id": 6, "weight": 25, "min_level": 47, "max_level": 48},  # Wickmere (run-only)
    {"kin_id": 115, "weight": 14, "min_level": 47, "max_level": 48},  # Solvyne
    {"kin_id": 120, "weight": 12, "min_level": 47, "max_level": 48},  # Dawnfawn
    {"kin_id": 117, "weight": 12, "min_level": 47, "max_level": 48},  # Helibud
    {"kin_id": 19, "weight": 9, "min_level": 48, "max_level": 48},  # Warmantis (run-only)
    {"kin_id": 12, "weight": 4, "min_level": 48, "max_level": 48},  # Chandrek (rare)
]
DAY = [
    {"kin_id": 11, "weight": 22, "min_level": 56, "max_level": 63},  # Tallowcrest
    {"kin_id": 6, "weight": 20, "min_level": 56, "max_level": 63},  # Wickmere
    {"kin_id": 19, "weight": 16, "min_level": 57, "max_level": 63},  # Warmantis
    {"kin_id": 115, "weight": 14, "min_level": 56, "max_level": 63},  # Solvyne
    {"kin_id": 120, "weight": 12, "min_level": 56, "max_level": 63},  # Dawnfawn
    {"kin_id": 12, "weight": 8, "min_level": 58, "max_level": 63},  # Chandrek
    {"kin_id": 7, "weight": 8, "min_level": 59, "max_level": 63},  # Wicklord (day only)
]
night = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                           id_prefix="trestle", table=TABLE)
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
                      if any(g[y * W + x] for g in (tree, path, tallgrass, deco, above))}
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
