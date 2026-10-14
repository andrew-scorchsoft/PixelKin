#!/usr/bin/env python3
"""
Kiln Gully — the old lamp-glass kiln in the Ashfall Shelf's cliff
(walkthrough/10-the-farlamp-isles.md Part II; kind cave, region north, optional,
band 33-35). A portal map: the hot draught off the shelf's old kiln stack is an
updraft vent (`to_kiln`, Updraft Kite), so you see it on the way to Mira and
come back once she has given you the Kite.

Lore (story-bible §11-12 safe): Cinderhead fired the lamp-glass for half the
valleys. The Kilnwright family ran this kiln until the Long Dusk, when the
lamp-oil stopped coming up the haulers' road and the fire was let go. Oda
Kilnwright still keeps the camp on the shelf below. One pane — the last ever
drawn here — was left on the drying rack.

Shape: the gully mouth (S, where the thermal sets you down) -> a 2-wide neck ->
THE KILN HALL (the cold beehive furnace top-centre, the focal point; glass racks
and cullet heaps) with two side rooms off its south wall: the west STORE (the
Star-chart: Shardstorm) and the east DRYING LOFT (the Last Pane, `flag:q_north_pane`).
A Beacon charge sits in the hall's NE corner. Wild kin roll rect-wide (cave).

Warps: `to_shelf` (10,17)/(11,17) on the gully mouth -> cinderwind_ashfall (18,4),
beside the vent you rode up. The Ashfall's `to_kiln` lands here at (10,16).

Run:  ./venv/bin/python tools/maps/build_cinderwind_kiln.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 22, 18
rng = random.Random(335)
owed: list[str] = []

wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)
floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 9, 12, 12, 16)        # the gully mouth
mk.rect(floor, W, H, 10, 17, 11, 17)       # ...open to the shelf below
mk.rect(floor, W, H, 10, 9, 11, 12)        # the neck
mk.rect(floor, W, H, 3, 2, 18, 9)          # THE KILN HALL
mk.rect(floor, W, H, 3, 9, 4, 11)          # west store door
mk.rect(floor, W, H, 1, 11, 5, 15)         # the west store
mk.rect(floor, W, H, 17, 9, 18, 11)        # east loft door
mk.rect(floor, W, H, 16, 11, 20, 15)       # the drying loft
# (third pass) THE LOOP: the side rooms join the gully mouth along row 14, so the
# kiln is a ring — hall -> store -> gully -> loft -> hall — not three dead ends.
mk.rect(floor, W, H, 5, 14, 9, 14)         # store <-> gully
mk.rect(floor, W, H, 12, 14, 16, 14)       # gully <-> loft
# THE GLASS-BLOWERS' ALCOVE: walled off from the hall by a rack (seen over it, from
# the hall), reached only by the cullet crawl up from the store (x=1, rows 6-10).
mk.rect(floor, W, H, 1, 3, 2, 5)           # the alcove
mk.rect(floor, W, H, 1, 6, 1, 10)          # the crawl
for i in range(W * H):
    if floor[i]:
        wall[i] = 0

cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.45 else cf[0] for _ in range(W * H)]
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


m: dict = {
    "id": "cinderwind_kiln", "display_name": "Kiln Gully",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [], "objects": [], "warps": [], "triggers": [], "encounters": [],
    "npcs": [], "gates": [],
    "music": "assets/audio/music/cinderhead-mine-b.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/kiln-a.webp"],
}


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


m["warps"] += [
    {"id": "to_shelf", "at": {"tx": 10, "ty": H - 1}, "trigger": "step_on",
     "to_map": "cinderwind_ashfall", "to": {"tx": 18, "ty": 4}, "facing": "down",
     "transition": "fade"},
    {"id": "to_shelf_e", "at": {"tx": 11, "ty": H - 1}, "trigger": "step_on",
     "to_map": "cinderwind_ashfall", "to": {"tx": 18, "ty": 4}, "facing": "down",
     "transition": "fade"},
]

# the hall: the cold beehive furnace is the focal point, top-centre
obj("kiln_furnace", "ashfall_kiln_furnace", (9, 2), 4, 3, overhang=1)
obj("rack_w", "ashfall_glass_rack", (3, 3), 3, 2)        # the alcove's screen
obj("rack_e", "ashfall_glass_rack", (14, 2), 3, 2)
obj("cullet_w", "ashfall_glass_cullet", (4, 7), 2, 2)
obj("cullet_e", "ashfall_glass_cullet", (15, 7), 2, 2)
obj("store_crates", "ashfall_slag_heap_b", (1, 14), 2, 2)
obj("store_cart", "cinderhead_ore_cart", (3, 12), 2, 2, overhang=1)
# the hall's centre: a cullet-and-crystal island you walk round (the furnace's apron)
obj("hall_crystal", "cinderhead_crystal_cluster", (11, 6), 2, 2, overhang=1)
obj("hall_cullet", "ashfall_glass_cullet", (9, 6), 2, 2)
obj("hall_slag", "ashfall_slag_heap_b", (6, 5), 2, 2)
obj("loft_rack", "ashfall_glass_rack", (18, 11), 3, 2)
# THE LAST PANE on the loft's drying rack (seen across the loft; gone once taken)
obj("last_pane", "ashfall_pane_frame", (20, 13), 1, 2, solid=False,
    hidden_when_flag="flag:q_north_pane")
m["triggers"] += [
    {"id": "take_pane", "kind": "cutscene", "at": {"tx": 20, "ty": 14},
     "activation": "interact", "ref": "script.kiln_last_pane",
     "hidden_when_flag": "flag:q_north_pane"},
    {"id": "furnace_lore", "kind": "cutscene", "at": {"tx": 10, "ty": 4},
     "activation": "interact", "ref": "script.kiln_furnace_lore"},
    {"id": "rack_lore", "kind": "dialogue", "at": {"tx": 5, "ty": 3},
     "activation": "interact", "ref": "npc.kiln_rack_lore"},
]
owed += ["script.kiln_last_pane", "script.kiln_furnace_lore", "npc.kiln_rack_lore"]
owed += pt.sign(m, deco, W, sid="kiln_tally", at=(12, 13))

owed += pt.cache(m, cid="kiln_beacon", at=(18, 3))       # the hall's NE corner
owed += pt.cache(m, cid="kiln_chart", at=(1, 4))         # the alcove: Shardstorm (seen first)

for (x, y, n) in [(3, 5, "boulder"), (3, 2, "boulder"), (17, 6, "boulder"), (9, 14, "g_pebble"),
                  (12, 15, "g_pebble"), (7, 8, "g_pebble"), (13, 7, "glowshroom_a"),
                  (5, 12, "g_pebble"), (16, 14, "boulder"), (8, 4, "glowshroom_b")]:
    put(x, y, n)

TABLE = [
    {"kin_id": 36, "weight": 30, "min_level": 33, "max_level": 35},    # Lumecite — Stone/Light
    {"kin_id": 69, "weight": 22, "min_level": 33, "max_level": 35},    # Riddlestone — Stone
    {"kin_id": 54, "weight": 18, "min_level": 33, "max_level": 33},    # Orebound — Stone
    {"kin_id": 43, "weight": 15, "min_level": 34, "max_level": 35},    # Pyrolith — Ember/Stone
    {"kin_id": 15, "weight": 10, "min_level": 34, "max_level": 35},    # Pyriven — Ember/Dark
    {"kin_id": 17, "weight": 8, "min_level": 34, "max_level": 35},     # Scorchwing — the kiln's signature
    {"kin_id": 37, "weight": 3, "min_level": 35, "max_level": 35},     # Prismara — very rare
]
m["encounters"] = [
    {"id": "kiln_hall", "terrain": "cave", "rect": {"tx": 3, "ty": 5, "w": 16, "h": 5},
     "encounter_rate": 0.10, "table": TABLE},
    {"id": "kiln_rooms", "terrain": "cave", "rect": {"tx": 1, "ty": 11, "w": 20, "h": 5},
     "encounter_rate": 0.08, "table": TABLE},
]

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
