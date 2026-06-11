#!/usr/bin/env python3
"""
Thunderroost — the Updraft-gated spur off Windward Stair II (walkthrough/
03-north, Windward §4; atlas: "rare Storm/Flying kin + item"). Kind route,
ONE screen (§2a late-spur tier) — a crag pinnacle the storm-birds keep,
[MISSABLE] by design: open the moment you reach the crags, a dead end you
must CHOOSE to fly to (signed hard on Stair II).

§3a braided-reward: the whole map is payoff — the AERIE (the bespoke nest
centrepiece) sits at the head with the frosttuft roost-bed around it (the
rare table), and the item cache hides behind a boulder choke in the east
pocket. The updraft column rises at the west lip you arrived by.

THE RARE STORM KIN (N5 mirrors into EXTRA_ENCOUNTERS): #90 Strikeaven
(Storm, the Sparrowcaw line's apex — THE storm-bird, the "Storm/Flying"
read) at weight 15, lv 36-37: the only authored wild bed for the apex bird.
Backed by #89 Flintbeak (its own mid stage — the roost is the line's home)
and #95 Glacewing. Spur tables may spike (§2b r4 — priced detours).

Cache note for the wiring agent: the spur's "item" should be worth the
flight — a Storm Star-chart or a valuable (10-economy cache-variety tier).

Reuse (P0.D table): windward-stair-a loop + windward-stair-a/b backdrops.

audit_flow note — a one-portal dead-end spur: no through-pair, so the loop
check does not apply; the screen IS the idea (§3a r5).

Run:  ./venv/bin/python tools/maps/build_thunderroost.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 16, 12
rng = random.Random(64)
owed: list[str] = []

# ---- terrain -----------------------------------------------------------------------
glacier = mk.make_grid(W, H)
frosttuft = mk.make_grid(W, H)

# the pinnacle's crag enclosure (2 deep, organic), the west arrival lip open
mk.rect(glacier, W, H, 0, 0, W - 1, 1)
mk.rect(glacier, W, H, 0, 0, 1, H - 1)
mk.rect(glacier, W, H, 14, 0, 15, H - 1)
mk.rect(glacier, W, H, 0, 10, W - 1, H - 1)
mk.organic_border(glacier, W, H, depth=0,
                  bumps=[(2, 2, 2), (13, 10, 2), (3, 10, 1)], rng=rng)
for y in (5, 6, 7):                       # the west lip (the thermal arrival)
    glacier[y * W + 1] = 0
glacier[5 * W + 2] = 0
glacier[6 * W + 2] = 0
glacier[7 * W + 2] = 0

# the roost-bed: frost-tufts ringing the aerie
mk.blob(frosttuft, W, H, 7.5, 6.0, 3.4, 1.8)
mk.blob(frosttuft, W, H, 5.5, 4.5, 1.8, 1.2)

# ---- precedence --------------------------------------------------------------------
for i in range(W * H):
    if glacier[i]:
        frosttuft[i] = 0

# ---- base: wind-scoured snow -------------------------------------------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
]

m: dict = {
    "id": "thunderroost", "display_name": "Thunderroost",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [
        # THE AERIE — the storm-birds' nest at the pinnacle's head (bespoke)
        {"id": "aerie", "sprite": "windward_aerie", "at": {"tx": 6, "ty": 2},
         "w": 3, "h": 3, "overhang": 1, "walk_under": False},
        # the thermal you rode up, streaming past the lip
        {"id": "lip_updraft", "sprite": "windward_updraft", "at": {"tx": 0, "ty": 4},
         "w": 2, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
    ],
    "warps": [
        # the glide back — lands ON Stair II's `to_roost` warp (mutual pair)
        {"id": "to_stair_ii", "at": {"tx": 2, "ty": 6}, "trigger": "step_on",
         "to_map": "windward_stair_ii", "to": {"tx": 25, "ty": 9}, "facing": "left",
         "transition": "fade"},
    ],
    "triggers": [], "encounters": [], "npcs": [], "gates": [],
    # spur reuse (P0.D): the wind country's loop + backdrops
    "music": "assets/audio/music/windward-stair-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/windward-stair-a.webp",
        "assets/backgrounds/battle/windward-stair-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- the item, behind a boulder choke in the east pocket ---------------------------
deco[4 * W + 11] = gid("boulder")
deco[6 * W + 12] = gid("boulder")
owed += pt.cache(m, cid="roost_prize", at=(12, 3))

# ---- encounters (the roost-bed — see docstring) ------------------------------------
TABLE = [{"kin_id": 90, "weight": 15, "min_level": 36, "max_level": 37},
         {"kin_id": 89, "weight": 45, "min_level": 34, "max_level": 36},
         {"kin_id": 95, "weight": 40, "min_level": 35, "max_level": 36}]
bed_grid = mk.make_grid(W, H)
for i in range(W * H):
    if frosttuft[i]:
        bed_grid[i] = 1
m["encounters"] += pt.zones_from_grid(bed_grid, W, H, terrain="tall_grass",
                                      rate=0.12, table=TABLE, id_prefix="roost")

# ---- wind-scoured dressing ---------------------------------------------------------
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
for (x, y, name) in [(4, 8, "boulder"), (10, 8, "greymoss_a"), (3, 3, "greymoss_b"),
                     (12, 7, "greymoss_a"), (9, 3, "greymoss_b")]:
    i = y * W + x
    if not glacier[i] and not frosttuft[i] and (x, y) not in object_cells | point_cells \
            and deco[i] == 0:
        deco[i] = gid(name)

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=5)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
