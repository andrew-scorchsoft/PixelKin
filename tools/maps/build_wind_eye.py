#!/usr/bin/env python3
"""
Wind-Eye — the landmark sky-grotto micro-dungeon off Galehigh (walkthrough/
03-north, Galehigh §4; atlas: "sky-grotto micro-dungeon; a unique Storm kin").
Updraft-gated at the Galehigh side (`to_windeye`, N1's gift_tease — the
[MISSABLE] signature optional reward). Kind cave, ONE floor — the §2a
late-spur tier: compact, but the prize sits a gate beyond the obvious.

Composition: the thermal sets you down in a south entry chamber; a 1-wide
throat opens into THE EYE — a sky-open central chamber around a void oculus
(the wind's eye itself), snow blown in across the floor, frost-tufts growing
in it, updraft columns rising through the opening. Rooms and chokes are
RECTS that overlap (the blob-adjacency trap) and both dead-ends pay (§3a r4):
a west alcove (charge cache) and an east alcove (valuable). The rare bed
(the deepest frosttuft pocket, past the eye's 1-wide north throat) carries
the prize.

THE UNIQUE STORM KIN (no pre-designed rows; N5 mirrors into
EXTRA_ENCOUNTERS): #93 Cumulance (Storm/Light, the cloud-mantle apex of the
Cirruff line) at weight 10, lv 36 — appears in NO other authored map table,
so the Wind-Eye is the only place to meet one; Light ties the lamp canon to
the sky-grotto. Backed by #94 Hailwhirr / #95 Glacewing at the spur band.
Spur tables may spike past the route band (§2b r4 — priced detours).

Reuse (P0.D table): windward-stair-a loop + windward-stair-a/b backdrops.

audit_flow note — `loop` WARN waived if raised: a one-portal landmark pocket
has no through-pair; the journey out is the glide home (the §2a late-spur
tier explicitly stays compact).

Run:  ./venv/bin/python tools/maps/build_wind_eye.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 20
rng = random.Random(63)
owed: list[str] = []

# ---- carve the grotto from solid rock ----------------------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 7, 14, 12, 17)        # entry chamber (the thermal shelf)
mk.vline(floor, W, H, 9, 11, 14)           # throat up to the eye (1-wide)
mk.rect(floor, W, H, 4, 4, 15, 11)         # THE EYE — the sky-open chamber
mk.hline(floor, W, H, 8, 2, 4)             # west choke (1-wide, overlaps chamber)
mk.rect(floor, W, H, 2, 6, 3, 9)           # west alcove (dead end, pays)
mk.hline(floor, W, H, 6, 15, 17)           # east choke (1-wide, overlaps chamber)
mk.rect(floor, W, H, 16, 4, 17, 7)         # east alcove (dead end, pays)
mk.vline(floor, W, H, 12, 2, 4)            # north throat (1-wide)
mk.rect(floor, W, H, 10, 2, 14, 3)         # the rare bed pocket (the prize)

for i in range(W * H):
    if floor[i]:
        wall[i] = 0

# the OCULUS: a void opening in the chamber's heart — ringed by a walkway
void = mk.make_grid(W, H)
mk.blob(void, W, H, 9.5, 7.5, 2.6, 1.9)
mk.blob(void, W, H, 8.5, 7.0, 1.8, 1.4)
for i in range(W * H):
    if void[i] and not floor[i]:
        void[i] = 0

# snow blown in through the eye (base tiles under the ring + the bed)
snowcells = mk.make_grid(W, H)
mk.blob(snowcells, W, H, 9.5, 7.5, 4.6, 3.4)
mk.rect(snowcells, W, H, 10, 2, 14, 3)

# frost-tufts growing in the blown snow (the encounter tile, fill-only)
frosttuft = mk.make_grid(W, H)
mk.blob(frosttuft, W, H, 6.0, 9.5, 1.8, 1.3)     # SW ring patch
mk.blob(frosttuft, W, H, 13.0, 5.0, 1.7, 1.1)    # NE ring patch
mk.rect(frosttuft, W, H, 10, 2, 14, 3)           # the rare bed
for i in range(W * H):
    if frosttuft[i] and (not floor[i] or void[i]):
        frosttuft[i] = 0
    if snowcells[i] and not floor[i]:
        snowcells[i] = 0

# ---- base: cave floor, snow where the sky reaches ----------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = mk.make_grid(W, H)
for i in range(W * H):
    if snowcells[i]:
        base[i] = rng.choice(sn) if rng.random() < 0.5 else sn[0]
    else:
        base[i] = rng.choice(cf) if rng.random() < 0.55 else cf[0]

terrain_layers = [
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_void", "role": "terrain", "terrain": "void",
     "set": "vesper_overworld_set", "depth": 0, "data": void},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

m: dict = {
    "id": "wind_eye", "display_name": "The Wind-Eye",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [
        # updraft columns rising through the eye (non-solid, drawn over)
        {"id": "eye_updraft_w", "sprite": "windward_updraft", "at": {"tx": 6, "ty": 5},
         "w": 2, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
        {"id": "eye_updraft_e", "sprite": "windward_updraft", "at": {"tx": 11, "ty": 8},
         "w": 2, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
        # a cairn keeping the entry shelf (someone tends even this place)
        {"id": "cairn_entry", "sprite": "windward_cairn", "at": {"tx": 11, "ty": 14},
         "w": 2, "h": 3, "overhang": 2, "walk_under": False},
    ],
    "warps": [
        # the glide back down — lands beside Galehigh's `to_windeye` warp at
        # (28,2); their warp lands at our (9,16), one tile north of this
        {"id": "to_galehigh", "at": {"tx": 9, "ty": 17}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 28, "ty": 3}, "facing": "down",
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

# ---- the paid dead-ends -------------------------------------------------------------
owed += pt.cache(m, cid="windeye_charge", at=(2, 7))     # Beacon charge, W alcove
owed += pt.cache(m, cid="windeye_glass", at=(17, 5))     # Starglass valuable, E alcove

# ---- encounters (the spur prize — see docstring) -----------------------------------
TABLE = [{"kin_id": 93, "weight": 10, "min_level": 36, "max_level": 36},
         {"kin_id": 94, "weight": 50, "min_level": 34, "max_level": 36},
         {"kin_id": 95, "weight": 40, "min_level": 35, "max_level": 36}]
bed_grid = mk.make_grid(W, H)
ring_grid = mk.make_grid(W, H)
for i in range(W * H):
    if frosttuft[i]:
        (bed_grid if i // W <= 3 else ring_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(ring_grid, W, H, terrain="tall_grass",
                                      rate=0.10, table=TABLE, id_prefix="ring")
m["encounters"] += pt.zones_from_grid(bed_grid, W, H, terrain="tall_grass",
                                      rate=0.13, table=TABLE, id_prefix="bed")

# ---- grotto dressing: grey moss + boulders (no living glowmoss up here) ------------
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
for (x, y, name) in [(4, 5, "greymoss_a"), (14, 10, "greymoss_b"), (8, 11, "greymoss_a"),
                     (3, 9, "greymoss_b"), (16, 7, "greymoss_a"), (7, 15, "greymoss_b"),
                     (15, 4, "boulder"), (5, 10, "boulder"), (12, 16, "boulder"),
                     (2, 6, "boulder")]:
    i = y * W + x
    if floor[i] and not frosttuft[i] and not void[i] \
            and (x, y) not in object_cells | point_cells and deco[i] == 0:
        deco[i] = gid(name)

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
