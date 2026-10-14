#!/usr/bin/env python3
"""
Lowtinder — the drowned old town (walkthrough/10 Part III, Lane E).

World (28,24), 26x28: east of Tinderwick Bay, under the bluff the new town moved up
onto the winter the water rose (about forty years ago — story-bible §12, the same
winter the Sunken Solarium flooded). The tide went out of it, mostly: a tidal SHELF
of salt-turf, sand and old cobbles, half-sunk houses standing in flooded yards, a
canal that used to be the high street, and on the one dry rise under the bluff, the
old LAMP-HOUSE where Grandmother Ottery Tallow — Brisa's grandmother, Lowtinder's
last Lampwarden — never left.

Three signature touches:
  1. THE UPPER STREET (the dry rise, rows 2-8): the old town's last dry street,
     under the bluff. Its south side is the old ROOF-LINE — a run of sand banks
     you hop DOWN (one-way, row 9) into the lower town; the way back up is the
     landing slope in the west. So the streets LOOP (§3a rule 1): landing ->
     upper street -> drop -> lower street -> back round. The Bell Cellar's steps
     go down beside the lamp-house; the cellar's far end climbs up Tinderwick's
     own well (the big loop home).
  2. THE DROWNED HIGH STREET: a canal (Tidecall water) from the lower street to
     the sea; half-sunk houses stand in its flooded yards.
  3. THE OLD LAMP-SCHOOL (south-east): its moss-garden room (lowtinder_school ->
     lowtinder_school_garden) opens only to Brightlight (4 Gleams).

Levels 18-21 (sea-grass beds + the canal); EMBRIFT (#14, never wild before) is the
Lowtinder rare — the Ember town's drowned hearths. Mirrored in build_species.py.

Wiring: west edge rows 15-16 <-> tinderwick_bay (27, y). Doors: the lamp-house
(lowtinder_lamphouse), the lamp-school (lowtinder_school). Steps -> lowtinder_cellar.

Run:  python3 tools/maps/build_lowtinder.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import warp_markers as wm
from mapkit import gid

W, H = 26, 28
rng = random.Random(1986)
WEST_ROWS = range(15, 17)   # the swim in from Tinderwick Bay's net-hand channel

# ---- terrain ---------------------------------------------------------------------
water = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 4, 2, 21)                # the bay, west
mk.blob(water, W, H, 1.0, 5.0, 2.2, 2.0)
mk.blob(water, W, H, 1.5, 21.0, 3.5, 3.0)
mk.rect(water, W, H, 0, 24, W - 1, H - 1)        # the sea, south
mk.blob(water, W, H, 6.0, 23.5, 3.5, 1.8)
mk.blob(water, W, H, 23.0, 23.0, 3.2, 2.0)
mk.rect(water, W, H, 24, 9, W - 1, 23)           # the sea, east
mk.blob(water, W, H, 24.5, 14.0, 2.0, 4.0)
mk.rect(water, W, H, 10, 14, 11, 23)             # the drowned high street (canal)
mk.blob(water, W, H, 13.5, 17.6, 3.2, 1.3)       # the sunk store's flooded yard
mk.blob(water, W, H, 4.0, 18.6, 3.2, 1.3)        # the west cottage's flooded yard

cliff = mk.make_grid(W, H)
mk.rect(cliff, W, H, 0, 0, W - 1, 1)             # the bluff (Tinderwick is up there)
mk.blob(cliff, W, H, 24.5, 2.0, 1.6, 1.0)          # the bluff steps down to the east sea
for i in range(W * H):
    if cliff[i]:
        water[i] = 0

path = mk.make_grid(W, H)                         # old cobbles (ruinfloor)
mk.rect(path, W, H, 3, 6, 7, 7)                   # the landing quay
mk.rect(path, W, H, 8, 7, 21, 8)                  # the upper street
mk.vline(path, W, H, 14, 6, 7)                    # lamp-house doorstep
mk.rect(path, W, H, 3, 12, 22, 13)                # the lower street (E-W)
mk.vline(path, W, H, 4, 8, 12)                    # landing slope -> lower street
mk.vline(path, W, H, 19, 14, 21)                  # down to the school door
mk.rect(path, W, H, 17, 21, 21, 22)               # the school yard
for i in range(W * H):
    if water[i] or cliff[i]:
        path[i] = 0

# sand: the shore strips round every water body + the bluff foot + a few flats
sand = mk.make_grid(W, H)
for y in range(H):
    for x in range(W):
        if water[y * W + x]:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if 0 <= x + dx < W and 0 <= y + dy < H:
                        sand[(y + dy) * W + x + dx] = 1
mk.rect(sand, W, H, 0, 2, W - 1, 2)
mk.blob(sand, W, H, 7.0, 3.5, 2.5, 1.2)
mk.blob(sand, W, H, 21.0, 19.0, 2.0, 1.5)
mk.blob(sand, W, H, 15.0, 10.5, 3.0, 1.0)

seagrass = mk.make_grid(W, H)                     # sea-grass beds (the shelf's tall grass)
mk.blob(seagrass, W, H, 6.5, 15.5, 2.3, 1.4)      # west yard bed
mk.blob(seagrass, W, H, 16.5, 20.0, 1.5, 1.6)     # by the sunk store
mk.blob(seagrass, W, H, 19.5, 4.3, 2.4, 1.2)      # up on the rise, past the lamp-house
mk.blob(seagrass, W, H, 8.0, 10.6, 2.6, 1.0)      # under the roof-line
for i in range(W * H):
    if water[i] or cliff[i] or path[i]:
        seagrass[i] = 0

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
terrain_layers = [
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_seagrass", "role": "terrain", "terrain": "dunegrass",
     "set": "vesper_overworld_set", "depth": 0, "data": seagrass},
    {"name": "t_path", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

# ---- objects ---------------------------------------------------------------------
LAMPHOUSE = (12, 2)        # 5x5, door col 2 -> (14, 6)
SCHOOL = (16, 17)          # 7x4, door col 3 -> (19, 20)


def o(oid, sprite, x, y, w, h, **kw):
    d = {"id": oid, "sprite": sprite, "at": {"tx": x, "ty": y}, "w": w, "h": h}
    d.update(kw)
    return d


objects = [
    o("lamphouse", "lowtinder_lamphouse", LAMPHOUSE[0], LAMPHOUSE[1], 5, 5, overhang=3),
    o("lampschool", "lowtinder_lampschool", SCHOOL[0], SCHOOL[1], 7, 4, overhang=2),
    # the dry rise's other house, high-water-marked to the sills
    o("old_cottage", "lowtinder_old_cottage", 17, 2, 5, 5, overhang=3),
    # the half-sunk town: houses standing in their flooded yards
    o("sunk_cottage_w", "lowtinder_sunk_cottage", 2, 15, 5, 5, overhang=3),
    o("sunk_shop_c", "lowtinder_sunk_shop", 12, 15, 5, 4, overhang=2),
    o("ridge_s1", "lowtinder_roof_ridge", 13, 24, 3, 2),
    o("ridge_s2", "lowtinder_roof_ridge_b", 1, 25, 4, 2),
    o("ridge_s3", "lowtinder_roof_ridge", 20, 25, 3, 2),
    o("belltower_e", "lowtinder_belltower", 24, 18, 2, 4, overhang=3),
    # the old street lamps, long cold (one still lit, by the lamp-house: hers)
    o("lamp_cold_a", "saltreach_sunken_lamp", 7, 9, 1, 3, overhang=2, walk_under=True),
    o("lamp_cold_b", "saltreach_sunken_lamp", 9, 13, 1, 3, overhang=2, walk_under=True),
    o("lamp_cold_c", "saltreach_sunken_lamp", 23, 10, 1, 3, overhang=2, walk_under=True),
    o("lamp_hers", "tinderwick_lamp_post", 11, 6, 1, 3, overhang=2, walk_under=True),
    # bluff-foot trees + the old town's clutter
    o("tree_a", "tinderwick_tree_b", 0, 0, 3, 4, overhang=3, walk_under=True),
    o("tree_b", "tinderwick_tree", 8, 0, 3, 4, overhang=3, walk_under=True),
    o("tree_c", "tinderwick_tree_c", 23, 3, 3, 4, overhang=3, walk_under=True),
    o("wreck", "pearlmoor_wreck_ribs", 7, 24, 3, 2),
    o("punt", "saltreach_punt", 0, 21, 2, 3),
    o("beached", "coldfog_beached_boat", 20, 9, 3, 2),
    o("anchor", "pearlmoor_anchor", 16, 9, 2, 2),
    o("pots_a", "pearlmoor_crab_pots", 3, 9, 1, 1),
    o("crates_a", "pearlmoor_fish_crates", 6, 9, 1, 1),
    o("netrack", "saltreach_net_rack", 6, 20, 3, 2),
    o("posts_a", "saltreach_mooring_posts", 9, 17, 1, 2),
    o("posts_b", "saltreach_mooring_posts", 12, 21, 1, 2),
    o("woodpile", "tinderwick_woodpile", 18, 13, 2, 1),
    o("eeltrap", "saltreach_eel_trap", 22, 15, 2, 2),
    o("driftwood", "pearlmoor_driftwood", 15, 23, 2, 1),
    o("notice", "tinderwick_notice_board", 9, 3, 2, 2, overhang=1),
    # the tide's leavings on the cobbles (review 2026-10: the streets read dry) —
    # non-solid puddle decals drawn in lowtinderforge.py
    o("puddle_1", "lowtinder_puddle_a", 6, 12, 2, 1, solid=False),
    o("puddle_2", "lowtinder_puddle_c", 13, 13, 2, 1, solid=False),
    o("puddle_3", "lowtinder_puddle_b", 20, 12, 1, 1, solid=False),
    o("puddle_4", "lowtinder_puddle_a", 16, 8, 2, 1, solid=False),
    o("puddle_5", "lowtinder_puddle_b", 10, 7, 1, 1, solid=False),
    o("puddle_6", "lowtinder_puddle_c", 18, 22, 2, 1, solid=False),
    o("puddle_7", "lowtinder_puddle_b", 4, 9, 1, 1, solid=False),
    o("puddle_8", "lowtinder_puddle_a", 4, 6, 2, 1, solid=False),
    # THE TIDE WAS HERE (review 2026-10 round 2: the streets still read dry):
    # wet-sand tint where the water just left, strand-lines of wrack along the
    # high-water mark, stranded shells and a starfish, and the old cart ruts in
    # the cobbles brimming with seawater. All non-solid decals (lowtinderforge.py).
    o("wet_1", "lowtinder_wet_a", 6, 2, 2, 2, solid=False),
    o("wet_2", "lowtinder_wet_b", 8, 10, 2, 2, solid=False),
    o("wet_3", "lowtinder_wet_a", 14, 9, 2, 2, solid=False),
    o("wet_4", "lowtinder_wet_b", 20, 17, 2, 2, solid=False),
    o("wet_5", "lowtinder_wet_a", 9, 19, 2, 2, solid=False),
    o("wet_6", "lowtinder_wet_b", 14, 21, 2, 2, solid=False),
    o("wet_7", "lowtinder_wet_a", 22, 13, 2, 2, solid=False),
    o("wet_8", "lowtinder_wet_b", 3, 3, 2, 2, solid=False),
    o("wrack_1", "lowtinder_wrack_a", 3, 14, 2, 1, solid=False),
    o("wrack_2", "lowtinder_wrack_b", 12, 19, 2, 1, solid=False),
    o("wrack_3", "lowtinder_wrack_a", 21, 18, 2, 1, solid=False),
    o("wrack_4", "lowtinder_wrack_b", 6, 22, 2, 1, solid=False),
    o("wrack_5", "lowtinder_wrack_a", 15, 23, 2, 1, solid=False),
    o("wrack_6", "lowtinder_wrack_b", 18, 10, 2, 1, solid=False),
    o("shells_1", "lowtinder_shells_a", 8, 21, 1, 1, solid=False),
    o("shells_2", "lowtinder_shells_b", 13, 10, 1, 1, solid=False),
    o("shells_3", "lowtinder_shells_a", 22, 20, 1, 1, solid=False),
    o("shells_4", "lowtinder_shells_b", 3, 8, 1, 1, solid=False),
    o("ruts_1", "lowtinder_ruts", 9, 12, 2, 1, solid=False),
    o("ruts_2", "lowtinder_ruts", 18, 13, 2, 1, solid=False),
    o("ruts_3", "lowtinder_ruts", 12, 7, 2, 1, solid=False),
    o("ruts_4", "lowtinder_ruts", 19, 16, 2, 1, solid=False),
]

# ---- deco ------------------------------------------------------------------------
deco = mk.make_grid(W, H)
# THE ROOF-LINE: the upper street's south lip is a run of sand banks you hop down
# (one-way) into the lower town; the landing slope (cols 3-5) is the way back up.
pt.ledge_run(deco, W, H, 9, 6, 22, rng, family="sand")
for x in (16, 17, 20, 21, 22):                    # (objects stand on these lip cells)
    pass
for (x, y) in [(3, 3), (21, 6), (12, 11), (23, 21), (8, 22), (17, 22), (3, 11),
               (14, 10), (22, 17), (13, 22), (1, 2), (22, 3), (5, 3),
               (0, 2), (25, 3), (25, 4), (25, 5), (25, 7), (25, 8), (24, 8)]:
    if not (water[y * W + x] or cliff[y * W + x] or path[y * W + x]) and deco[y * W + x] == 0:
        deco[y * W + x] = gid("boulder")
for (x, y) in [(1, 9), (10, 25), (18, 26), (24, 25), (25, 12)]:
    deco[y * W + x] = gid("buoy")
sign_xy = (6, 5)
deco[sign_xy[1] * W + sign_xy[0]] = gid("sign")
sign2_xy = (20, 14)
deco[sign2_xy[1] * W + sign2_xy[0]] = gid("sign")

# ---- the map ---------------------------------------------------------------------
lamp_door = (LAMPHOUSE[0] + 2, LAMPHOUSE[1] + 4)       # (14, 6)
school_door = (SCHOOL[0] + 3, SCHOOL[1] + 3)          # (19, 20)
CELLAR = (19, 7)                                       # the steps down, on the upper street

m = {
    "id": "lowtinder", "display_name": "Lowtinder", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        {"id": f"to_bay_{y}", "at": {"tx": 0, "ty": y}, "trigger": "step_on",
         "to_map": "tinderwick_bay", "to": {"tx": 27, "ty": y}, "facing": "left",
         "transition": "fade"}
        for y in WEST_ROWS
    ] + [
        {"id": "to_lamphouse", "at": {"tx": lamp_door[0], "ty": lamp_door[1]}, "trigger": "step_on",
         "to_map": "lowtinder_lamphouse", "to": {"tx": 7, "ty": 9}, "facing": "up", "transition": "door"},
        {"id": "to_school", "at": {"tx": school_door[0], "ty": school_door[1]}, "trigger": "step_on",
         "to_map": "lowtinder_school", "to": {"tx": 8, "ty": 10}, "facing": "up", "transition": "door"},
        {"id": "to_cellar", "at": {"tx": CELLAR[0], "ty": CELLAR[1]}, "trigger": "step_on",
         "to_map": "lowtinder_cellar", "to": {"tx": 3, "ty": 2}, "facing": "down", "transition": "fade"},
    ],
    "triggers": [
        {"id": "sign_landing", "kind": "sign", "at": {"tx": sign_xy[0], "ty": sign_xy[1]},
         "activation": "interact", "ref": "sign.lowtinder_landing"},
        {"id": "sign_school", "kind": "sign", "at": {"tx": sign2_xy[0], "ty": sign2_xy[1]},
         "activation": "interact", "ref": "sign.lowtinder_school"},
        {"id": "read_notice", "kind": "dialogue", "at": {"tx": 9, "ty": 4},
         "activation": "interact", "ref": "npc.lowtinder_notice"},
    ],
    "encounters": [],
    "npcs": [],
    "gates": [],
    "music": "assets/audio/music/lowtinder.mp3",
    "ambience": {
        "particles": [{"kind": "spray", "density": 0.3}, {"kind": "glowmotes", "density": 0.35},
                      {"kind": "motes", "density": 0.3}],
        "mist": {"color": "#bcd4f0", "alpha": 0.07, "speed": 3},
        "light_sources_extra": [{"at": {"tx": 14, "ty": 5}, "radius": 16},
                                {"at": {"tx": 11, "ty": 7}, "radius": 9}],
        "bob_gids": [gid("buoy")],
        "sound_bed": "amb-surf",
    },
}

TABLE = [{"kin_id": 11, "weight": 30, "min_level": 18, "max_level": 20},
         {"kin_id": 42, "weight": 25, "min_level": 18, "max_level": 20},
         {"kin_id": 21, "weight": 20, "min_level": 18, "max_level": 20},
         {"kin_id": 16, "weight": 15, "min_level": 17, "max_level": 18},
         {"kin_id": 14, "weight": 7, "min_level": 20, "max_level": 21}]
m["encounters"] += pt.zones_from_grid(seagrass, W, H, terrain="tall_grass", rate=0.10,
                                      table=TABLE, id_prefix="lt_grass")
m["encounters"].append(
    {"id": "lt_canal", "terrain": "water", "rect": {"tx": 0, "ty": 0, "w": W, "h": H},
     "encounter_rate": 0.07, "requires_ability": "tidecall",
     "table": [{"kin_id": 27, "weight": 35, "min_level": 18, "max_level": 20},
                   {"kin_id": 21, "weight": 30, "min_level": 18, "max_level": 20},
                   {"kin_id": 24, "weight": 25, "min_level": 18, "max_level": 20},
                   {"kin_id": 14, "weight": 5, "min_level": 20, "max_level": 21}]})

owed: list[str] = []
# a mudlark on the lower street (route), watching west along the cobbles
owed += pt.trainer_beat(m, tid="lt_mudlark", at=(16, 12), facing="left", sight=4, sprite="fisher_man")
# a lamp-keeper on the upper street (keeper), watching the cobbles to the cellar
owed += pt.trainer_beat(m, tid="lt_lampwright", at=(21, 8), facing="left", sight=3, sprite="lamplighter")
# caches: balms by the landing, a rooftop find on the rise (seen from below, reached
# along the upper street), and a lamp-oil purse in the west yard
owed += pt.cache(m, cid="lowtinder_landing", at=(3, 7))
owed += pt.cache(m, cid="lowtinder_rooftop", at=(22, 4))
owed += pt.cache(m, cid="lowtinder_yard", at=(8, 19))
m["npcs"] += [
    # an old tide-woman resting on the lower street's steps (lore)
    {"id": "lt_tidewife", "at": {"tx": 8, "ty": 13}, "facing": "down", "sprite": "fisher_woman",
     "movement": "look_around", "dialogue_ref": "script.lowtinder_tidewife"},
    # ambient kin from the map's own table, off the lanes
    {"id": "amb_tallowcrest", "at": {"tx": 21, "ty": 15}, "facing": "down", "sprite": "kin_11_overworld",
     "movement": "wander", "ambient": True, "wander_radius": 1},
    {"id": "amb_tidmaren", "at": {"tx": 5, "ty": 22}, "facing": "down", "sprite": "kin_21_overworld",
     "movement": "wander", "ambient": True, "wander_radius": 1},
]
wm.add(m, wm.marker("cellar_steps", "steps_s", CELLAR[0], CELLAR[1]))

if __name__ == "__main__":
    pt.report(owed)
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
