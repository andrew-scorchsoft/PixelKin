#!/usr/bin/env python3
"""
The Wick-Run: the Traverse (09-the-wild-ways §2 A; kind route, region west,
band 47-49, `ride: true`). Here the old wax road stops falling straight and
cuts WEST across the mountain's flank — the long sideways leg that carries the
run from under the Sunvault round to the sea-facing slope.

One idea per screen (§3a r5):
  1. THE ROCK GARDEN (east): a broad chute carrying you west (`slope dir:left`)
     strewn with stoppers — boulders that rose out of the wax-road when the
     carts stopped. You can't brake uphill (east), so you steer up and down
     between them; clip one and you stop dead. It funnels to one gap.
  2. THE CART WRECK (south pocket): steer DOWN off the garden onto a flat
     shelf where a wax-cart left the road in the last season the wax ran —
     grass, and something the carters never came back for (a Beacon charge).
  3. THE RAMP LINE (west): the funnel feeds two kickers — one clears a
     rockfall across the road, then the road turns DOWN and a second kicker
     clears a boulder bank — and you land on the run-out to the lower run.

One-way: the garden and the ramp line are a single west-carrying chute from
the entry pad's edge to the turn; the turn is a down chute to the run-out.

HANDSHAKE: east `to_trestles`/`_s` (29,14)/(29,15) <-> wickrun_trestles'
`to_traverse` (0,38)/(0,39) (each lands ON the other); south `to_lower`/`_e`
(8,29)/(9,29) -> wickrun_lower (8,0)/(9,0), whose return warps land ON these.
Geometry: x -57..-27, y -170..-140.

Run:  python3 tools/maps/build_wickrun_traverse.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 30, 30
rng = random.Random(9064)
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


carve(29, 14, 29, 15)        # the road in from the trestles
carve(25, 12, 28, 17)        # the entry pad
carve(13, 7, 24, 20)         # 1. the rock garden
carve(14, 21, 22, 25)        # 2. the cart-wreck shelf
carve(9, 14, 12, 15)         # 3. the funnel + the ramp line
carve(3, 14, 8, 15)          #    the rockfall, cleared by the first kicker
carve(3, 16, 6, 25)          #    the turn down + the boulder bank
carve(2, 26, 13, 28)         #    the run-out
carve(8, 29, 9, 29)          #    the road on to the lower run
for (x, y) in OPEN:
    tree[y * W + x] = 0

pin: dict = {}
m: dict = {
    "id": "wickrun_traverse", "display_name": "The Wick-Run",
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


# ---- 1. the rock garden: a west-carrying chute with stoppers -------------------
GARDEN = cells(13, 7, 24, 20)
wk.chute(m, pin, deco, W, GARDEN | cells(9, 14, 12, 15), "left", fid="garden", chevrons=4)
# stoppers: never two in a column within a row of each other, so every stop
# leaves a sidestep up or down (no pockets — the trap check in the lane notes)
STOPPERS = [(22, 8), (18, 8), (15, 10), (21, 11), (17, 12), (23, 14), (19, 15),
            (15, 17), (21, 18), (17, 19), (14, 13), (22, 20)]
for (x, y) in STOPPERS:
    deco[y * W + x] = gid("boulder")

# ---- 3. the ramp line --------------------------------------------------------------
# kicker one: west off the funnel over the rockfall at x7 onto x6
wk.chute(m, pin, deco, W, cells(5, 14, 6, 15), "left", fid="rockfall_landing", chevrons=0)
for y in (14, 15):
    wk.jump(m, deco, W, at=(8, y), dir="left", length=3, jid=f"rockfall_kicker_{y}")
    deco[y * W + 7] = gid("boulder")
    pin.pop((8, y), None)
for (x, y) in cells(7, 14, 8, 15):
    pin[(x, y)] = f"chute_h_{(x + y) % 2}"
# the turn: carried down the west wall; the boulder bank's flanks are wall, so
# you only ever meet kicker two head-on
BANK_WALL = cells(3, 19, 3, 22) | cells(6, 19, 6, 22)
TURN = (cells(3, 14, 4, 15) | cells(3, 16, 6, 25)) - BANK_WALL
for (x, y) in BANK_WALL:
    tree[y * W + x] = 1
    OPEN.discard((x, y))
wk.chute(m, pin, deco, W, TURN, "down", fid="turn_down", chevrons=4)
for x in (4, 5):
    wk.jump(m, deco, W, at=(x, 20), dir="down", length=3, jid=f"bank_kicker_{x}")
    deco[21 * W + x] = gid("boulder")

# ---- flat ground ------------------------------------------------------------------
LANE = cells(25, 13, 28, 16) | {(29, 14), (29, 15)} | cells(15, 21, 21, 22) \
    | cells(2, 26, 13, 27) | {(8, 28), (9, 28), (8, 29), (9, 29)}
for (x, y) in LANE:
    if (x, y) in OPEN and (x, y) not in pin:
        path[y * W + x] = 1

# grass: the wreck shelf's floor, the run-out's east end
for (x, y) in cells(14, 23, 22, 25) | cells(11, 26, 13, 28) | cells(2, 27, 4, 28):
    tallgrass[y * W + x] = 1
for i in range(W * H):
    x, y = i % W, i // W
    if (x, y) not in OPEN or (x, y) in pin or deco[i]:
        tallgrass[i] = 0
    if tallgrass[i] or (x, y) in pin:
        path[i] = 0

# ---- warps -------------------------------------------------------------------------
for i, y in enumerate((14, 15)):
    m["warps"].append({"id": "to_trestles" + ("_s" if i else ""), "at": {"tx": 29, "ty": y},
                       "trigger": "step_on", "to_map": "wickrun_trestles",
                       "to": {"tx": 0, "ty": y + 24}, "facing": "right", "transition": "fade"})
for i, x in enumerate((8, 9)):
    m["warps"].append({"id": "to_lower" + ("_e" if i else ""), "at": {"tx": x, "ty": H - 1},
                       "trigger": "step_on", "to_map": "wickrun_lower",
                       "to": {"tx": x, "ty": 0}, "facing": "down", "transition": "fade"})

# ---- 2. the wreck + landmarks ------------------------------------------------------
obj("cart_wreck", "wickrun_wax_cart_wreck", (17, 22), 2, 2)
obj("wreck_barrels", "wickrun_wax_barrels", (20, 24), 2, 1)
owed += pt.cache(m, cid="wickrun_wreck", at=(19, 23))
for i, (lx, ly) in enumerate([(25, 11), (28, 15), (14, 21), (10, 24), (2, 24), (9, 11)]):
    obj(f"run_lamp_{i}", "tinderwick_lamp_post", (lx, ly), 1, 3, overhang=2, walk_under=True)
obj("lift_pylon", "wickrun_lift_pylon", (26, 3), 1, 4, overhang=3, walk_under=True)
obj("pad_pine", "windward_bent_pine", (27, 11), 2, 3, overhang=2, walk_under=True)
obj("runout_tree", "tinderwick_tree_b", (11, 25), 3, 4, overhang=3, walk_under=True)
obj("runout_crates", "pearlmoor_fish_crates", (6, 28), 1, 1)

# ---- trainer, sign ------------------------------------------------------------------
owed += pt.trainer_beat(m, tid="runner_pip", at=(26, 12), facing="down", sight=5,
                        sprite="npc_boy")
owed += pt.sign(m, deco, W, sid="wickrun_traverse", at=(25, 17))

# Run tables (shared shape down the whole run, bands rising): the run-only kin
# lead, with the Sunvault's lighter Solar/Verdant regulars. Average BST is kept
# on the dex's level trend so the progression model's wild-XP fit isn't tilted
# (tools/balance/progression.mjs `fit`) — the heavy hitters stay rare.
TABLE = [
    {"kin_id": 11, "weight": 24, "min_level": 47, "max_level": 49},  # Tallowcrest (run-only)
    {"kin_id": 6, "weight": 25, "min_level": 47, "max_level": 49},  # Wickmere (run-only)
    {"kin_id": 115, "weight": 14, "min_level": 47, "max_level": 49},  # Solvyne
    {"kin_id": 120, "weight": 12, "min_level": 47, "max_level": 49},  # Dawnfawn
    {"kin_id": 117, "weight": 12, "min_level": 47, "max_level": 49},  # Helibud
    {"kin_id": 19, "weight": 9, "min_level": 48, "max_level": 49},  # Warmantis (run-only)
    {"kin_id": 12, "weight": 4, "min_level": 49, "max_level": 49},  # Chandrek (rare)
]
DAY = [
    {"kin_id": 11, "weight": 22, "min_level": 57, "max_level": 63},  # Tallowcrest
    {"kin_id": 6, "weight": 20, "min_level": 57, "max_level": 63},  # Wickmere
    {"kin_id": 19, "weight": 16, "min_level": 58, "max_level": 63},  # Warmantis
    {"kin_id": 115, "weight": 14, "min_level": 57, "max_level": 63},  # Solvyne
    {"kin_id": 120, "weight": 12, "min_level": 57, "max_level": 63},  # Dawnfawn
    {"kin_id": 12, "weight": 8, "min_level": 59, "max_level": 63},  # Chandrek
    {"kin_id": 7, "weight": 8, "min_level": 60, "max_level": 63},  # Wicklord (day only)
]
night = pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                           id_prefix="traverse", table=TABLE)
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
