#!/usr/bin/env python3
"""
Lanthorne Hollow — the crypt under the Drowned Chapel (09-the-wild-ways §2 B;
kind cave, dark, no encounters). Where the Mirelights' one true light sleeps.

A single flooded chamber: the stair down from the chapel door, a black pool
(DEEP — the last thing in the Mirelights no Gift can swim), ONE board across
it, and on the dais beyond, the great null-lantern with something asleep
inside. The Hollowing's early kindness: they put the fen's lamp to sleep so it
would never be hurt, and the sleep starved its star (cinder law rule 2). Wake
it (`script.mirelight_lanthorne`: the `legendaryBattle` set-piece, Lanthorne
#165 lv 45, cooldown 12 won battles) — and once it's yours the lantern stands
empty and the star over the fen burns a little brighter.

HANDSHAKE: `to_chapel` (9,12) <-> mirelight_chapel's door `to_hollow` (14,37)
(landing on its porch apron (14,38)); the chapel's door lands here at (9,11).

Run:  python3 tools/maps/build_lanthorne_hollow.py
"""
from __future__ import annotations

import random

import mapkit as mk
import mirelight_common as mc
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 18, 14
rng = random.Random(16504)
owed: list[str] = []

wall = [1] * (W * H)
water = mk.make_grid(W, H)
deco = mk.make_grid(W, H)


def carve(x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            wall[y * W + x] = 0


carve(5, 2, 12, 5)          # the dais
carve(3, 6, 14, 9)          # the pool's basin
carve(3, 10, 14, 12)        # the stair foot
carve(4, 5, 13, 5)
for y in range(6, 10):
    for x in range(3, 15):
        water[y * W + x] = 1
for (x, y) in [(3, 6), (14, 6), (3, 9), (14, 9)]:
    water[y * W + x] = 0
    wall[y * W + x] = 1

m: dict = {
    "id": "lanthorne_hollow", "display_name": "Lanthorne Hollow",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/mirelight.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/mirelight-b.webp"],
    "ambience": {"particles": [{"kind": "glowmotes", "density": 0.7}],
                 "tint": {"color": "#16304a", "alpha": 0.18}, "sound_bed": "amb-drips"},
}
wk.use_traverse(m)
obj = lambda *a, **k: mc.obj(m, *a, **k)  # noqa: E731

# the one board across the black pool
wk.plank(m, deco, W, rect=(9, 6, 1, 4), axis="v", sid="hollow_board")

# the stair up to the chapel
deco[12 * W + 9] = gid("cave_ladder_up")
m["warps"].append({"id": "to_chapel", "at": {"tx": 9, "ty": 12}, "trigger": "step_on",
                   "to_map": "mirelight_chapel", "to": {"tx": 14, "ty": 38},
                   "facing": "down", "transition": "fade"})

# the null-lantern (Lanthorne asleep inside) -> empty once it's woken and caught
obj("null_lantern", "mirelight_null_lantern_big", (8, 2), 2, 3, overhang=1,
    hidden_when_flag="flag:lanthorne_caught")
obj("null_lantern_empty", "glowmoss_deep_null_lantern_shrine", (8, 2), 2, 3, overhang=1,
    requires_flag="flag:lanthorne_caught")
# interact triggers sit ON the lantern's base row (faced from the dais floor below)
for x in (8, 9):
    m["triggers"].append({"id": f"lanthorne_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 4},
                          "activation": "interact", "ref": "script.mirelight_lanthorne",
                          "hidden_when_flag": "flag:lanthorne_caught"})
    m["triggers"].append({"id": f"lantern_empty_{x}", "kind": "script", "at": {"tx": x, "ty": 4},
                          "activation": "interact", "ref": "script.mirelight_lantern_empty",
                          "requires_flag": "flag:lanthorne_caught"})
owed += ["script.mirelight_lanthorne", "script.mirelight_lantern_empty"]

# the Hollowing's tending: doused null-lamps along the dais, offerings, a kept broom
for (x, y) in [(5, 2), (12, 2)]:
    deco[y * W + x] = gid("null_lantern")
for (x, y, n) in [(6, 4, "glowshroom_a"), (11, 3, "glowshroom_b"), (4, 11, "greymoss_a"),
                  (13, 10, "greymoss_b"), (5, 10, "g_pebble"), (12, 12, "g_pebble")]:
    deco[y * W + x] = gid(n)
obj("hollow_offerings", "hoard_niche_glow", (6, 2), 1, 2, overhang=1)
obj("hollow_broom", "hoard_broom", (11, 4), 1, 2, overhang=1, walk_under=True)
obj("hollow_shrooms", "glowmoss_deep_glowshrooms_teal", (3, 10), 2, 2, overhang=1, walk_under=True)
obj("hollow_shrooms_b", "glowmoss_deep_glowshrooms_teal", (13, 11), 2, 2, overhang=1,
    walk_under=True)
owed += pt.sign(m, deco, W, sid="lanthorne_hollow", at=(7, 11))

cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]
m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]
# the whole pool is deep: the board is the only way to the dais
mc.deep_layer(m, water, set(), W, H)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
