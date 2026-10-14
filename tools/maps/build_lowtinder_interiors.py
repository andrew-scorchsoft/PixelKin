#!/usr/bin/env python3
"""
Lowtinder interiors (walkthrough/10 Part III, Lane E; docs/world/interiors.md, roomkit):

  * lowtinder_lamphouse — Grandmother Ottery Tallow's dry upper floor of the old
    lamp-house. Warm register, cosy and cluttered: the hearth is the focal wall
    piece, her armchair pulled up to it, the lamp-rack of the town's old lamps she
    still trims, a bed nook behind a partition, oil jars by the stair up from the
    flooded ground floor. The town's LAST REST POINT down here (her script runs
    the `heal` op — `content/regions/lowtinder.ts`).
  * lowtinder_school — the old lamp-school's classroom: desks in rows facing the
    chalkboard, the lamp-rack the children practised trimming on, a bookcase of
    wick-primers. Its back door (north wall, `lowtinder_garden_door`) opens on the
    moss-garden only to BRIGHTLIGHT (`flag:lamplight_brightlight`, 4 Gleams); before
    that it speaks (`door.lowtinder_garden_dark`).
  * lowtinder_school_garden — the moss-garden room, built as a small CAVE floor on
    the shared set so it can carry real glowmoss (the encounter tile): the glass
    roof fell in long ago and the moss took the room, lit by its own glow and the
    old lamps. MOSSMANTLE (#39, never wild before) lives here.

Run:  python3 tools/maps/build_lowtinder_interiors.py
"""
from __future__ import annotations

import random

import mapkit as mk
from mapkit import gid
from roomkit import (WARM_SET, faced_room, windows, partition_v, place, wall_mount,
                     mapdef, finish)


def build_lamphouse():
    W, H = 14, 11
    door_x = W // 2  # tx 7
    base, over = faced_room(W, H, door_x)
    windows(over, W, [4, 10])
    # the bed nook, east, behind a partition (entered from the south)
    partition_v(over, W, 10, 1, 5, lip="w")
    objects: list = []
    wall_mount(objects, "hearth", 5)                       # the focal piece
    wall_mount(objects, "lamp_rack", 1, solid=False)       # the town's old lamps, still trimmed
    wall_mount(objects, "shelf", 8)
    place(objects, "armchair", 4, 4)                        # hers, by the fire
    place(objects, "rug", 5, 5, solid=False)
    place(objects, "table", 2, 6, oid="table_round")
    place(objects, "stool", 4, 7, oid="stool_a")
    place(objects, "oil_jars", 1, 9)
    place(objects, "barrels", 11, 8)
    place(objects, "plant", 8, 9)
    # the nook: her bed, a dresser, a plant
    place(objects, "bed", 11, 2)
    place(objects, "plant", 12, 6, oid="plant_nook")
    warps = [
        {"id": "to_lowtinder", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "lowtinder", "to": {"tx": 14, "ty": 7}, "facing": "down", "transition": "door"},
    ]
    triggers = [
        {"id": "read_rack", "kind": "script", "at": {"tx": 1, "ty": 2}, "activation": "interact",
         "ref": "script.lowtinder_lamp_rack"},
        {"id": "read_shelf", "kind": "sign", "at": {"tx": 8, "ty": 3}, "activation": "interact",
         "ref": "sign.lowtinder_lamphouse_shelf"},
    ]
    npcs = [
        # Grandmother Ottery Tallow (one script, staged inside with if/unless —
        # the first meeting, the bell, the rest, the reef). Absent only while
        # she's been rowed out to her reef (flag:lowtinder_at_reef).
        {"id": "ottery", "at": {"tx": 5, "ty": 6}, "facing": "down", "sprite": "ottery",
         "movement": "look_around", "dialogue_ref": "script.lowtinder_ottery",
         "hidden_when_flag": "flag:lowtinder_at_reef"},
    ]
    return mapdef("lowtinder_lamphouse", "The Old Lamp-house", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/interior-hearth.mp3")


def build_school():
    W, H = 16, 12
    door_x = W // 2  # tx 8
    base, over = faced_room(W, H, door_x)
    windows(over, W, [3, 13])
    # the teacher's store, west, behind a partition
    partition_v(over, W, 4, 1, 4, lip="e")
    objects: list = []
    wall_mount(objects, "chalkboard", 9)                     # the focal wall (cols 9-12)
    wall_mount(objects, "lamp_rack", 5, solid=False)          # the practice lamps
    wall_mount(objects, "bookcase", 1)                        # wick-primers (store)
    # the back door to the moss-garden, set into the wall face (non-solid art;
    # the step_on door warp frees its tile)
    objects.append({"id": "garden_door", "sprite": "lowtinder_garden_door",
                    "at": {"tx": door_x, "ty": 0}, "w": 1, "h": 2, "solid": False})
    # desks in rows, facing the board
    for i, (x, y) in enumerate([(6, 5), (10, 5), (6, 7), (10, 7), (13, 7)]):
        place(objects, "desk", x, y, oid=f"desk_{i}")
        place(objects, "stool", x, y + 1, oid=f"stool_{i}")
    place(objects, "crates", 1, 6, oid="store_crates")
    place(objects, "oil_jars", 1, 9)
    place(objects, "plant", 14, 2)
    place(objects, "plant", 14, 10, oid="plant_s")
    warps = [
        {"id": "to_lowtinder", "at": {"tx": door_x, "ty": H - 1}, "trigger": "step_on",
         "to_map": "lowtinder", "to": {"tx": 19, "ty": 21}, "facing": "down", "transition": "door"},
        # the moss-garden: only to Brightlight (the Lamplight tier at 4 Gleams)
        {"id": "to_garden", "at": {"tx": door_x, "ty": 1}, "trigger": "step_on",
         "to_map": "lowtinder_school_garden", "to": {"tx": 8, "ty": 8}, "facing": "up",
         "transition": "door", "requires_flag": "flag:lamplight_brightlight",
         "blocked_ref": "door.lowtinder_garden_dark"},
    ]
    triggers = [
        {"id": "read_board", "kind": "script", "at": {"tx": 10, "ty": 2}, "activation": "interact",
         "ref": "script.lowtinder_chalkboard"},
        {"id": "read_primers", "kind": "sign", "at": {"tx": 1, "ty": 3}, "activation": "interact",
         "ref": "sign.lowtinder_primers"},
    ]
    npcs = [
        # the lamp-school's purse (a find in the teacher's store)
        {"id": "cache_school_purse", "at": {"tx": 2, "ty": 5}, "facing": "down", "sprite": "item_cache",
         "movement": "static", "dialogue_ref": "script.pickup_lowtinder_school_purse",
         "hidden_when_flag": "flag:picked_lowtinder_school_purse"},
    ]
    return mapdef("lowtinder_school", "The Old Lamp-school", W, H, WARM_SET,
                  base, over, objects, warps, triggers, npcs,
                  "assets/audio/music/interior-study.mp3")


def build_garden() -> dict:
    """The moss-garden: a cave-kind floor on the shared set (glowmoss is the
    encounter tile), so it can glow. 16x10 — a full screen wide (review 2026-10:
    the old 12x10 left a black void beside it). The glass roof fell in long ago;
    the moss took the room, the children's desks and all."""
    W, H = 16, 10
    DOOR = 8
    rng = random.Random(3939)
    wall = mk.make_grid(W, H)
    mk.rect(wall, W, H, 0, 0, W - 1, H - 1)
    floor = mk.make_grid(W, H)
    mk.rect(floor, W, H, 2, 2, 13, 8)
    mk.blob(floor, W, H, 7.5, 4.5, 6.2, 3.0)
    mk.vline(floor, W, H, DOOR, 8, 9)               # the doorway, south
    for i in range(W * H):
        if floor[i]:
            wall[i] = 0
    moss = mk.make_grid(W, H)
    mk.blob(moss, W, H, 7.5, 4.2, 5.0, 2.3)
    mk.blob(moss, W, H, 11.5, 6.6, 1.6, 1.0)
    for i in range(W * H):
        if not floor[i]:
            moss[i] = 0
    for y in (6, 7, 8):                              # a clear path in from the door
        moss[y * W + DOOR] = 0
    cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
    base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]
    deco = mk.make_grid(W, H)
    for (x, y, n) in [(2, 2, "glowshroom_a"), (13, 3, "glowshroom_b"), (3, 7, "glowshroom_b"),
                      (13, 7, "glowshroom_a"), (6, 8, "glowshroom_a")]:
        if floor[y * W + x] and not moss[y * W + x]:
            deco[y * W + x] = gid(n)
    m = {
        "id": "lowtinder_school_garden", "display_name": "The Moss-garden",
        "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
        "tilesets": [mk.shared_tileset_ref()],
        "layers": [{"name": "base", "role": "base", "depth": 0, "data": base},
                   {"name": "t_moss", "role": "terrain", "terrain": "glowmoss",
                    "set": "vesper_overworld_set", "depth": 0, "data": moss},
                   {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
                    "set": "vesper_overworld_set", "depth": 0, "data": wall},
                   {"name": "deco", "role": "deco", "depth": 5, "data": deco},
                   {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
        "objects": [
            {"id": "old_lamp_w", "sprite": "saltreach_sunken_lamp", "at": {"tx": 2, "ty": 3},
             "w": 1, "h": 3, "overhang": 2, "walk_under": True},
            {"id": "old_lamp_e", "sprite": "tinderwick_lamp_post", "at": {"tx": 13, "ty": 4},
             "w": 1, "h": 3, "overhang": 2, "walk_under": True},
            {"id": "shrooms", "sprite": "glowmoss_deep_glowshrooms_teal", "at": {"tx": 11, "ty": 1},
             "w": 2, "h": 2, "overhang": 1, "walk_under": True},
            {"id": "shrooms_w", "sprite": "glowmoss_deep_glowshrooms_teal", "at": {"tx": 4, "ty": 1},
             "w": 2, "h": 2, "overhang": 1, "walk_under": True},
            # the children's desks, mossed over where they stood
            {"id": "desk_a", "sprite": "interior_desk", "at": {"tx": 10, "ty": 7}, "w": 2, "h": 1},
            {"id": "stool_a", "sprite": "interior_stool", "at": {"tx": 12, "ty": 8}, "w": 1, "h": 1},
            {"id": "puddle_g", "sprite": "lowtinder_puddle_a", "at": {"tx": 4, "ty": 7}, "w": 2, "h": 1,
             "solid": False},
        ],
        "warps": [
            {"id": "to_school", "at": {"tx": DOOR, "ty": 9}, "trigger": "step_on",
             "to_map": "lowtinder_school", "to": {"tx": 8, "ty": 2}, "facing": "down",
             "transition": "door"},
        ],
        "triggers": [
            {"id": "read_plaque", "kind": "sign", "at": {"tx": 3, "ty": 2}, "activation": "interact",
             "ref": "sign.lowtinder_garden"},
        ],
        "encounters": [
            {"id": "moss_garden", "terrain": "tall_grass", "rect": {"tx": 1, "ty": 1, "w": 14, "h": 8},
             "encounter_rate": 0.14,
             "table": [{"kin_id": 39, "weight": 40, "min_level": 24, "max_level": 27},
                       {"kin_id": 6, "weight": 35, "min_level": 24, "max_level": 26},
                       {"kin_id": 21, "weight": 25, "min_level": 24, "max_level": 26}]},
        ],
        "npcs": [
            {"id": "cache_garden_drop", "at": {"tx": 9, "ty": 7}, "facing": "down", "sprite": "item_cache",
             "movement": "static", "dialogue_ref": "script.pickup_lowtinder_garden",
             "hidden_when_flag": "flag:picked_lowtinder_garden"},
            {"id": "amb_mossmantle", "at": {"tx": 5, "ty": 3}, "facing": "down", "sprite": "kin_39_overworld",
             "movement": "wander", "ambient": True, "wander_radius": 1},
        ],
        "gates": [],
        "music": "assets/audio/music/lowtinder.mp3",
        "ambience": {"particles": [{"kind": "spores", "density": 0.6}, {"kind": "glowmotes", "density": 0.5}],
                     "light_sources_extra": [{"at": {"tx": 8, "ty": 4}, "radius": 34, "color": "#9fe0a8"}]},
    }
    return m


if __name__ == "__main__":
    ok = True
    for m in (build_lamphouse(), build_school()):
        ok = finish(m) and ok
    ok = mk.finalize(build_garden(), scale=4) and ok
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
