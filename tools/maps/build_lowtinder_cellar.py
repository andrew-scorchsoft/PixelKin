#!/usr/bin/env python3
"""
The Bell Cellar — two floors under Lowtinder's lamp-house (walkthrough/10 Part III,
Lane E). A region side-dungeon on the §2a ladder: B1 (the cellars) -> B2 (the
belfry pit), joined by a mutual ladder pair.

  lowtinder_cellar     (B1, 24x20) "The Bell Cellar"
      The old lamp-house cellars and the vaults the town kept its oil, rope and
      winter stores in — flooded knee-deep in places (murk pools, Tidecall), dry
      enough elsewhere. The WINCH-KEY hangs in the far store (flag:lowtinder_winch_key,
      a cache); a lamp-keeper holds the store passage. Ladder down (SE).
  lowtinder_cellar_b2  (B2, 24x22) "The Bell Cellar — the Belfry Pit"
      The drowned bell-tower's foot: the town bell lies on its lip in the silt at
      the pit's heart (lowtinder_bell_sunk), the old bell-winch on the north ledge.
      With the winch-key the bell comes up (script.lowtinder_raise_bell ->
      flag:q_lowtinder_bell; the object pair swaps to lowtinder_bell_raised, same
      2x2 footprint + solidity). A LUMEN DROP waits in the south vault. In the NW
      corner the old bell-shaft — which the new town's well was sunk straight down
      — climbs up into TINDERWICK'S SQUARE (script.lowtinder_well_climb, a one-way
      `travel`: the well's the way out, never the way in).

Levels: B1 19-22, B2 20-23 (cave rolls rect-wide). Mirrored in build_species.py.

Run:  python3 tools/maps/build_lowtinder_cellar.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import warp_markers as wm
from mapkit import gid

CF = None


def floor_base(W, H, rng):
    cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
    return [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]


def carve(W, H, rooms, rng):
    """Rect rooms (overlapping corridors keep the joins honest — the build-map
    rule), then each room's walls ROUGHENED with a few small blobs so the
    cellars read as old stone eaten by the sea, not a ruled box."""
    wall = mk.make_grid(W, H)
    mk.rect(wall, W, H, 0, 0, W - 1, H - 1)
    floor = mk.make_grid(W, H)
    for (x0, y0, x1, y1) in rooms:
        mk.rect(floor, W, H, x0, y0, x1, y1)
    for (x0, y0, x1, y1) in rooms:
        if (x1 - x0) < 3 or (y1 - y0) < 2:
            continue                                  # leave corridors as cut
        for _ in range(2):
            side = rng.choice("nsew")
            if side in "ns":
                cx, cy = rng.randint(x0 + 1, x1 - 1), (y0 if side == "n" else y1)
            else:
                cx, cy = (x0 if side == "w" else x1), rng.randint(y0 + 1, y1 - 1)
            for y in range(cy - 1, cy + 2):
                for x in range(cx - 1, cx + 2):
                    if 1 <= x <= W - 2 and 1 <= y <= H - 2 and abs(x - cx) + abs(y - cy) <= 1:
                        floor[y * W + x] = 1
    for i in range(W * H):
        if floor[i]:
            wall[i] = 0
    return wall, floor


def mapdict(mid, name, W, H, base, layers, deco, objects, warps, triggers, encounters, npcs, music):
    return {
        "id": mid, "display_name": name, "width": W, "height": H,
        "tile_width": 16, "tile_height": 16, "kind": "cave",
        "tilesets": [mk.shared_tileset_ref()],
        "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + layers +
                  [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
                   {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
        "objects": objects, "warps": warps, "triggers": triggers, "encounters": encounters,
        "npcs": npcs, "gates": [], "music": music,
    }


# =============================================================================== B1
def build_b1() -> dict:
    W, H = 24, 20
    rng = random.Random(1140)
    ENTRY = (3, 1)            # the steps up to Lowtinder (lands at (3,2))
    LADDER_DOWN = (20, 16)    # pairs with B2's ladder_up
    rooms = [
        (2, 1, 4, 3),         # the stair foot
        (1, 3, 8, 7),         # the lamp-house cellar (oil jars, the first pool)
        (8, 5, 15, 6),        # the vault passage east
        (14, 2, 21, 7),       # the rope store (north-east)
        (5, 8, 6, 12),        # the drop south out of the first cellar
        (2, 12, 12, 16),      # the winter store (south-west, flooded)
        (12, 14, 18, 15),     # the low passage east
        (17, 10, 22, 17),     # the ladder vault (south-east)
        (18, 7, 19, 10),      # rope store -> ladder vault
        (9, 9, 12, 12),       # a side bay off the winter store (the key's nook)
    ]
    wall, floor = carve(W, H, rooms, rng)
    murk = mk.make_grid(W, H)
    mk.blob(murk, W, H, 6.5, 14.4, 3.4, 1.7)       # the winter store's flood
    mk.blob(murk, W, H, 3.0, 5.2, 1.7, 1.3)        # the first pool (lamp-house cellar)
    mk.blob(murk, W, H, 20.5, 4.8, 1.3, 1.7)
    for i in range(W * H):
        if not floor[i]:
            murk[i] = 0
    base = floor_base(W, H, rng)
    layers = [
        {"name": "t_murk", "role": "terrain", "terrain": "murk",
         "set": "vesper_overworld_set", "depth": 0, "data": murk},
        {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
         "set": "vesper_overworld_set", "depth": 0, "data": wall},
    ]
    deco = mk.make_grid(W, H)
    deco[LADDER_DOWN[1] * W + LADDER_DOWN[0]] = gid("cave_ladder_down")
    for (x, y) in [(7, 4), (1, 7), (15, 2), (21, 7), (12, 16), (22, 11), (2, 16), (10, 9)]:
        if floor[y * W + x] and not murk[y * W + x]:
            deco[y * W + x] = gid("boulder")
    for (x, y, n) in [(4, 6, "glowshroom_a"), (16, 6, "glowshroom_b"), (19, 13, "glowshroom_a"),
                      (11, 12, "glowshroom_b")]:
        if floor[y * W + x] and not murk[y * W + x]:
            deco[y * W + x] = gid(n)
    sign_xy = (4, 2)
    deco[sign_xy[1] * W + sign_xy[0]] = gid("sign")
    objects = [
        {"id": "jars", "sprite": "interior_barrels", "at": {"tx": 7, "ty": 3}, "w": 2, "h": 1},
        {"id": "crates", "sprite": "interior_crates", "at": {"tx": 14, "ty": 2}, "w": 2, "h": 2},
        {"id": "sacks", "sprite": "interior_sacks", "at": {"tx": 20, "ty": 2}, "w": 2, "h": 1},
        {"id": "store_crates", "sprite": "interior_crates", "at": {"tx": 2, "ty": 12}, "w": 2, "h": 2},
        {"id": "dead_lamp_a", "sprite": "coldfog_doused_lamp", "at": {"tx": 8, "ty": 4}, "w": 1, "h": 3,
         "overhang": 2, "walk_under": True},
        {"id": "dead_lamp_b", "sprite": "coldfog_doused_lamp", "at": {"tx": 17, "ty": 9}, "w": 1, "h": 3,
         "overhang": 2, "walk_under": True},
        {"id": "pots", "sprite": "pearlmoor_crab_pots", "at": {"tx": 16, "ty": 2}, "w": 1, "h": 1},
        {"id": "netrack", "sprite": "pearlmoor_net_rack", "at": {"tx": 18, "ty": 2}, "w": 2, "h": 1},
        {"id": "store_sacks", "sprite": "interior_sacks", "at": {"tx": 9, "ty": 15}, "w": 2, "h": 1},
        {"id": "posts", "sprite": "saltreach_mooring_posts", "at": {"tx": 21, "ty": 11}, "w": 1, "h": 2},
    ]
    warps = [
        {"id": "to_lowtinder", "at": {"tx": ENTRY[0], "ty": ENTRY[1]}, "trigger": "step_on",
         "to_map": "lowtinder", "to": {"tx": 19, "ty": 7}, "facing": "up", "transition": "fade"},
        {"id": "ladder_down", "at": {"tx": LADDER_DOWN[0], "ty": LADDER_DOWN[1]}, "trigger": "step_on",
         "to_map": "lowtinder_cellar_b2", "to": {"tx": 19, "ty": 3}, "facing": "down", "transition": "fade"},
    ]
    triggers = [
        {"id": "sign_cellar", "kind": "sign", "at": {"tx": sign_xy[0], "ty": sign_xy[1]},
         "activation": "interact", "ref": "sign.lowtinder_cellar"},
    ]
    encounters = [
        {"id": "cellar_b1", "terrain": "cave", "rect": {"tx": 0, "ty": 0, "w": W, "h": H},
         "encounter_rate": 0.07,
         "table": [{"kin_id": 20, "weight": 30, "min_level": 19, "max_level": 21},
                   {"kin_id": 13, "weight": 25, "min_level": 19, "max_level": 22},
                   {"kin_id": 41, "weight": 20, "min_level": 20, "max_level": 22},
                   {"kin_id": 31, "weight": 18, "min_level": 20, "max_level": 22},
                   {"kin_id": 14, "weight": 5, "min_level": 21, "max_level": 22}]},
    ]
    m = mapdict("lowtinder_cellar", "The Bell Cellar", W, H, base, layers, deco, objects,
                warps, triggers, encounters, [], "assets/audio/music/bell-cellar.mp3")
    owed = []
    # the lamp-keeper's ghost-shift: holds the passage to the rope store
    owed += pt.trainer_beat(m, tid="lt_cellar_keeper", at=(13, 6), facing="left", sight=4,
                            sprite="miner_man")
    # THE WINCH-KEY, hung in the winter store's side bay (a key, not a cache sprite)
    m["npcs"].append(
        {"id": "winch_key", "at": {"tx": 11, "ty": 10}, "facing": "down", "sprite": "item_cache",
         "movement": "static", "dialogue_ref": "script.lowtinder_winch_key",
         "hidden_when_flag": "flag:lowtinder_winch_key"})
    owed += pt.cache(m, cid="cellar_oil", at=(21, 3))
    wm.add(m, wm.marker("cellar_up", "steps_n", ENTRY[0], ENTRY[1] - 1))
    m["ambience"] = {"particles": [{"kind": "dust", "density": 0.4}, {"kind": "motes", "density": 0.3}],
                     "tint": {"color": "#10203a", "alpha": 0.10}}
    pt.report(owed)
    return m


# =============================================================================== B2
def build_b2() -> dict:
    W, H = 24, 22
    rng = random.Random(1141)
    LADDER_UP = (19, 3)
    WELL = (3, 2)             # the old bell-shaft's foot: the rope up to Tinderwick
    BELL = (11, 10)           # 2x2, the bell in the pit (and raised)
    rooms = [
        (16, 1, 21, 5),       # the ladder landing (north-east)
        (13, 4, 16, 5),       # gallery west
        (2, 1, 12, 5),        # the north ledge (the winch, the shaft)
        (5, 6, 18, 14),       # THE BELFRY PIT
        (3, 14, 6, 19),       # the south-west stair
        (6, 17, 13, 20),      # the south vault (the Lumen Drop)
        (18, 9, 21, 17),      # the east gallery
        (14, 16, 20, 17),     # east -> south vault
    ]
    wall, floor = carve(W, H, rooms, rng)
    murk = mk.make_grid(W, H)
    mk.blob(murk, W, H, 12.0, 11.0, 4.6, 2.9)      # the pit's black water round the bell
    mk.blob(murk, W, H, 7.0, 8.0, 1.4, 1.0)
    mk.blob(murk, W, H, 16.5, 8.5, 1.4, 1.2)
    for i in range(W * H):
        if not floor[i]:
            murk[i] = 0
    for (x, y) in [(x, y) for y in range(BELL[1], BELL[1] + 2) for x in range(BELL[0], BELL[0] + 2)]:
        murk[y * W + x] = 0
    for y in range(6, BELL[1]):                    # a dry spit out to the bell from the ledge
        murk[y * W + BELL[0]] = 0
        murk[y * W + BELL[0] + 1] = 0
    base = floor_base(W, H, rng)
    layers = [
        {"name": "t_murk", "role": "terrain", "terrain": "murk",
         "set": "vesper_overworld_set", "depth": 0, "data": murk},
        {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
         "set": "vesper_overworld_set", "depth": 0, "data": wall},
    ]
    deco = mk.make_grid(W, H)
    deco[LADDER_UP[1] * W + LADDER_UP[0]] = gid("cave_ladder_up")
    for (x, y) in [(6, 13), (17, 6), (20, 11), (4, 16), (12, 19), (9, 2), (21, 16), (14, 8)]:
        if floor[y * W + x] and not murk[y * W + x]:
            deco[y * W + x] = gid("boulder")
    for (x, y, n) in [(16, 3, "glowshroom_a"), (5, 7, "glowshroom_b"), (19, 14, "glowshroom_a"),
                      (8, 18, "glowshroom_b"), (2, 4, "glowshroom_a"), (9, 20, "glowshroom_a"),
                      (4, 19, "glowshroom_b")]:
        if floor[y * W + x] and not murk[y * W + x]:
            deco[y * W + x] = gid(n)
    objects = [
        {"id": "bell_sunk", "sprite": "lowtinder_bell_sunk", "at": {"tx": BELL[0], "ty": BELL[1]},
         "w": 2, "h": 2, "hidden_when_flag": "flag:q_lowtinder_bell"},
        {"id": "bell_raised", "sprite": "lowtinder_bell_raised", "at": {"tx": BELL[0], "ty": BELL[1]},
         "w": 2, "h": 2, "requires_flag": "flag:q_lowtinder_bell"},
        # the old bell-winch on the north ledge, over the pit
        {"id": "winch", "sprite": "lowtinder_bell_winch", "at": {"tx": 10, "ty": 3}, "w": 2, "h": 2},
        # the rope up the old shaft (the well) — a marker, never solid
        {"id": "shaft_rope", "sprite": "markers_rope_ladder", "at": {"tx": WELL[0], "ty": WELL[1] - 1},
         "w": 1, "h": 2, "solid": False, "bob": False},
        {"id": "beam_a", "sprite": "interior_crates", "at": {"tx": 19, "ty": 9}, "w": 2, "h": 2},
        {"id": "vault_barrels", "sprite": "interior_barrels", "at": {"tx": 11, "ty": 20}, "w": 2, "h": 1},
        {"id": "dead_lamp_n", "sprite": "coldfog_doused_lamp", "at": {"tx": 7, "ty": 1}, "w": 1, "h": 3,
         "overhang": 2, "walk_under": True},
        {"id": "dead_lamp_e", "sprite": "coldfog_doused_lamp", "at": {"tx": 20, "ty": 13}, "w": 1, "h": 3,
         "overhang": 2, "walk_under": True},
        {"id": "pit_posts_w", "sprite": "saltreach_mooring_posts", "at": {"tx": 6, "ty": 9}, "w": 1, "h": 2},
        {"id": "pit_posts_e", "sprite": "saltreach_mooring_posts", "at": {"tx": 17, "ty": 11}, "w": 1, "h": 2},
        {"id": "anchor", "sprite": "pearlmoor_anchor", "at": {"tx": 15, "ty": 18}, "w": 2, "h": 2},
    ]
    warps = [
        {"id": "ladder_up", "at": {"tx": LADDER_UP[0], "ty": LADDER_UP[1]}, "trigger": "step_on",
         "to_map": "lowtinder_cellar", "to": {"tx": 20, "ty": 16}, "facing": "down", "transition": "fade"},
    ]
    triggers = [
        # the winch: the bell-raising scene (needs the winch-key; speaks otherwise)
        {"id": "bell_winch", "kind": "script", "at": {"tx": 10, "ty": 4},
         "activation": "interact", "ref": "script.lowtinder_winch"},
        # the bell itself (read it before, after)
        {"id": "bell_read", "kind": "script", "at": {"tx": BELL[0], "ty": BELL[1] + 1},
         "activation": "interact", "ref": "script.lowtinder_bell_read"},
        # the old shaft: climb the rope up into Tinderwick's square (one-way)
        {"id": "well_climb", "kind": "script", "at": {"tx": WELL[0], "ty": WELL[1]},
         "activation": "interact", "ref": "script.lowtinder_well_climb"},
    ]
    encounters = [
        {"id": "cellar_b2", "terrain": "cave", "rect": {"tx": 0, "ty": 0, "w": W, "h": H},
         "encounter_rate": 0.07,
         "table": [{"kin_id": 13, "weight": 25, "min_level": 20, "max_level": 23},
                   {"kin_id": 41, "weight": 25, "min_level": 20, "max_level": 23},
                   {"kin_id": 31, "weight": 20, "min_level": 21, "max_level": 23},
                   {"kin_id": 27, "weight": 20, "min_level": 21, "max_level": 23},
                   {"kin_id": 14, "weight": 8, "min_level": 22, "max_level": 23}]},
    ]
    m = mapdict("lowtinder_cellar_b2", "The Bell Cellar — the Belfry Pit", W, H, base, layers, deco,
                objects, warps, triggers, encounters, [], "assets/audio/music/bell-cellar.mp3")
    owed = []
    owed += pt.cache(m, cid="belfry_lumen", at=(7, 19))      # the Lumen Drop (south vault)
    owed += pt.cache(m, cid="belfry_ledge", at=(21, 15))     # the east gallery's balms
    m["ambience"] = {"particles": [{"kind": "dust", "density": 0.35}, {"kind": "motes", "density": 0.4}],
                     "tint": {"color": "#0c1830", "alpha": 0.12},
                     "light_sources_extra": [{"at": {"tx": 3, "ty": 1}, "radius": 14, "color": "#cfe0ff"}]}
    pt.report(owed)
    return m


if __name__ == "__main__":
    ok = True
    for build in (build_b1, build_b2):
        ok = mk.finalize(build(), scale=3) and ok
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
