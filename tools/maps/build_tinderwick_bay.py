#!/usr/bin/env python3
"""
Tinderwick Bay — the sea under the home town's beach (walkthrough/10 Part III, Lane E).

World (0,24), 28x28, directly SOUTH of Tinderwick: its top row is the sea the
beach looks out on, so every open column of Tinderwick's bottom row swims straight
down into this map (Tidecall, gift 2 — the first reason to walk back to the start).

What's out here (three signature touches):
  1. THE DROWNED STREET. A line of roof-ridges and chimney rubble standing out of
     the shallows, continuing the ones the beach can see — old Tinderwick, forty
     years under. You swim its lanes east to Lowtinder (east edge, rows 6-13).
  2. TWO SKERRIES worth stopping on: Gull Shoal (west — sea-grass, a lamp-diver,
     a balm tin) and Tidepool Skerry (centre — rock-pools, a net-hand, and a
     Star-chart wedged behind the boulders, off the lane).
  3. THE OUTER REEF, seen from the first swim and earned at the end: past a lip
     of reef rocks (row 19) the water goes DEEP (rows 20+, the `deepwater_set`
     family; rowed in the Farlamp skiff, `deepdive`). On the far islet stands the
     old TINDER LIGHT, cold — the lamp Grandmother Tallow kept before the water
     rose. Her post-game reef scene lands there (content/regions/lowtinder.ts),
     and a skiff-only cache waits on the west skerry.

Levels: shallows 17-20 (Tide kin; Tidmaren the swimmer rare), sea-grass 17-19,
the deep reef 58-62 (post-game). Mirrored in build_species.py EXTRA_ENCOUNTERS.

audit_flow WARN (justified): `loop` — a sea route walks back the way it swam in; the
bay's return compressor is the Bell Cellar's climb up Tinderwick's well (one map over).

Run:  python3 tools/maps/build_tinderwick_bay.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 28, 28
rng = random.Random(2410)
REEF_ROW = 20                 # rows >= this are the outer deep (skiff only)

# Tinderwick's bottom-row columns its drowned roofs/tower cover (build_tinderwick
# SEA_SOLID_COLS): no swim warp there — the rubble continues into our row 0.
TW_SOLID = {5, 6, 7, 8, 11, 12, 13, 14, 16, 17, 18, 19, 20}
SWIM_COLS = range(21, 28)     # build_tinderwick.SWIM_COLS — the swim-off columns
EAST_ROWS = range(6, 14)      # the swim east into Lowtinder (its west edge)

# ---- terrain ---------------------------------------------------------------------
water = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 0, W - 1, H - 1)
sand = mk.make_grid(W, H)
mk.blob(sand, W, H, 4.5, 7.0, 3.4, 2.3)          # Gull Shoal (west)
mk.blob(sand, W, H, 2.5, 9.0, 1.4, 1.0)
mk.blob(sand, W, H, 17.5, 13.5, 3.8, 2.6)        # Tidepool Skerry (centre)
mk.blob(sand, W, H, 21.0, 15.0, 1.8, 1.3)
mk.blob(sand, W, H, 20.5, 24.5, 4.6, 2.3)        # the Tinder Light's reef islet
mk.blob(sand, W, H, 5.0, 24.0, 1.7, 1.3)         # the west reef skerry (skiff cache)
mk.blob(sand, W, H, 24.0, 2.5, 1.6, 1.2)         # a tiny sand-bar by the tower
for i in range(W * H):
    if sand[i]:
        water[i] = 0
# (sand only on the skerries: the shared sand family edges onto grass — the
# Gullcry skerry look, a weedy lip where the islet meets the sea)
pool = mk.make_grid(W, H)                          # the skerry's rock-pools
mk.blob(pool, W, H, 16.5, 13.5, 1.2, 0.8)
seagrass = mk.make_grid(W, H)                      # Gull Shoal's sea-grass bed
mk.blob(seagrass, W, H, 3.6, 7.4, 1.8, 1.1)
for i in range(W * H):
    if not sand[i]:
        seagrass[i] = 0

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
terrain_layers = [
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_seagrass", "role": "terrain", "terrain": "dunegrass",
     "set": "vesper_overworld_set", "depth": 0, "data": seagrass},
    {"name": "t_pool", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": pool},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
]

# ---- objects: the drowned street, a wreck, the Tinder Light ------------------------
objects = [
    # the drowned street, running on from the beach's ridges (south-east lanes)
    {"id": "ridge_a", "sprite": "lowtinder_roof_ridge", "at": {"tx": 7, "ty": 2}, "w": 3, "h": 2},
    {"id": "ridge_b", "sprite": "lowtinder_roof_ridge_b", "at": {"tx": 12, "ty": 5}, "w": 4, "h": 2},
    {"id": "ridge_c", "sprite": "lowtinder_roof_ridge", "at": {"tx": 9, "ty": 9}, "w": 3, "h": 2},
    {"id": "ridge_d", "sprite": "lowtinder_roof_ridge", "at": {"tx": 21, "ty": 7}, "w": 3, "h": 2},
    {"id": "ridge_e", "sprite": "lowtinder_roof_ridge_b", "at": {"tx": 4, "ty": 14}, "w": 4, "h": 2},
    {"id": "ridge_f", "sprite": "lowtinder_roof_ridge", "at": {"tx": 24, "ty": 16}, "w": 3, "h": 2},
    {"id": "wreck", "sprite": "pearlmoor_wreck_ribs", "at": {"tx": 10, "ty": 16}, "w": 3, "h": 2},
    # THE OLD TINDER LIGHT on the far reef (4x7; only its base row is solid)
    {"id": "tinder_light", "sprite": "lowtinder_tinder_light", "at": {"tx": 20, "ty": 18},
     "w": 4, "h": 7, "overhang": 6},
]

# ---- deco: chimney rubble under the beach's roofs, buoys, reef lip, rocks ----------
deco = mk.make_grid(W, H)
for x in (19, 20):                                    # the bell-tower's footing rubble
    deco[0 * W + x] = gid("boulder")
# the buoy lane: from the beach, down the drowned street, east to Lowtinder
for (x, y) in [(14, 1), (17, 3), (19, 5), (23, 10), (26, 6), (26, 13)]:
    deco[y * W + x] = gid("buoy")
# the reef lip: rocks along row 19 with swim gaps (the deep beyond is SEEN early)
for x in (0, 1, 3, 6, 7, 12, 13, 15, 26, 27):
    deco[19 * W + x] = gid("boulder")
# skerry rocks (the chart cache hides behind the east cluster)
for (x, y) in [(19, 12), (20, 12), (15, 15), (22, 14), (21, 13),
               (6, 6), (2, 6), (7, 8),
               (17, 25), (24, 23), (23, 26), (4, 23)]:
    if not water[y * W + x]:
        deco[y * W + x] = gid("boulder")
# a couple of scattered rocks in open water break up the shallows
for (x, y) in [(2, 3), (25, 1), (15, 9), (1, 12), (24, 11), (8, 18)]:
    deco[y * W + x] = gid("boulder")
sign_xy = (14, 13)
deco[sign_xy[1] * W + sign_xy[0]] = gid("sign")

# ---- the map ---------------------------------------------------------------------
m = {
    "id": "tinderwick_bay", "display_name": "Tinderwick Bay", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # back up onto Tinderwick's sea row (landing ON its return warp)
        {"id": f"to_tinderwick_{x}", "at": {"tx": x, "ty": 0}, "trigger": "step_on",
         "to_map": "tinderwick", "to": {"tx": x, "ty": 23}, "facing": "up",
         "transition": "fade"}
        for x in SWIM_COLS
    ] + [
        {"id": f"to_lowtinder_{y}", "at": {"tx": W - 1, "ty": y}, "trigger": "step_on",
         "to_map": "lowtinder", "to": {"tx": 0, "ty": y}, "facing": "right",
         "transition": "fade"}
        for y in EAST_ROWS
    ],
    "triggers": [
        {"id": "sign_skerry", "kind": "sign", "at": {"tx": sign_xy[0], "ty": sign_xy[1]},
         "activation": "interact", "ref": "sign.tinderwick_bay"},
        # the reef's cold lamp, read from its islet
        {"id": "tinder_light_read", "kind": "script", "at": {"tx": 21, "ty": 24},
         "activation": "interact", "ref": "script.lowtinder_tinder_light"},
    ],
    "encounters": [
        {"id": "bay_shallows", "terrain": "water", "rect": {"tx": 0, "ty": 0, "w": W, "h": REEF_ROW},
         "encounter_rate": 0.08, "requires_ability": "tidecall",
         "table": [{"kin_id": 26, "weight": 30, "min_level": 17, "max_level": 19},
                   {"kin_id": 23, "weight": 25, "min_level": 17, "max_level": 19},
                   {"kin_id": 27, "weight": 20, "min_level": 18, "max_level": 20},
                   {"kin_id": 24, "weight": 15, "min_level": 18, "max_level": 20},
                   {"kin_id": 21, "weight": 6, "min_level": 19, "max_level": 20}]},
        {"id": "shoal_seagrass", "terrain": "tall_grass", "rect": {"tx": 1, "ty": 6, "w": 6, "h": 3},
         "encounter_rate": 0.10,
         "table": [{"kin_id": 20, "weight": 40, "min_level": 17, "max_level": 19},
                   {"kin_id": 26, "weight": 30, "min_level": 17, "max_level": 18},
                   {"kin_id": 31, "weight": 20, "min_level": 18, "max_level": 19},
                   {"kin_id": 13, "weight": 10, "min_level": 18, "max_level": 19}]},
        # the outer reef: rowed water, post-game (deep terrain rolls only on the
        # deepwater tiles — the engine's 'deep' tile-bound terrain)
        {"id": "reef_deep", "terrain": "deep", "rect": {"tx": 0, "ty": REEF_ROW, "w": W, "h": H - REEF_ROW},
         "encounter_rate": 0.08,
         "table": [{"kin_id": 28, "weight": 28, "min_level": 58, "max_level": 61},
                   {"kin_id": 25, "weight": 20, "min_level": 58, "max_level": 61},
                   {"kin_id": 22, "weight": 20, "min_level": 58, "max_level": 61},
                   {"kin_id": 172, "weight": 15, "min_level": 58, "max_level": 60},
                   {"kin_id": 174, "weight": 12, "min_level": 58, "max_level": 60},
                   {"kin_id": 30, "weight": 5, "min_level": 60, "max_level": 62}]},
    ],
    "npcs": [],
    "gates": [],
    "music": "assets/audio/music/lowtinder.mp3",
    "ambience": {
        "particles": [{"kind": "spray", "density": 0.7}, {"kind": "glowmotes", "density": 0.2}],
        "mist": {"color": "#cfe0ff", "alpha": 0.06, "speed": 5},
        "birds": {"kind": "gull", "flocks": [{"tx": 5, "ty": 7}, {"tx": 18, "ty": 13}], "flyover": True},
        "light_sources_extra": [{"at": {"tx": 21, "ty": 21}, "radius": 18, "color": "#8fa6d6"}],
        "bob_gids": [gid("buoy")],
        "sound_bed": "amb-surf",
    },
}

owed: list[str] = []
# two swimmer-route trainers, each on a skerry facing the water lane it watches
owed += pt.trainer_beat(m, tid="bay_diver", at=(6, 7), facing="right", sight=4, sprite="fen_folk")
owed += pt.trainer_beat(m, tid="bay_nethand", at=(16, 12), facing="up", sight=4, sprite="fisher_woman")
# caches (variety: a consumable on the shoal, the valuable off the lane, and a
# skiff-only find on the west reef skerry — Deep backtrack #5)
owed += pt.cache(m, cid="bay_shoal", at=(2, 8))
owed += pt.cache(m, cid="bay_skerry_chart", at=(21, 14))
owed += pt.cache(m, cid="bay_reef", at=(5, 24))
# Grandmother Tallow on her reef, only while she's been rowed out (the scene's
# `travel` re-enters the map so this placement spawns — Lottie's trick).
m["npcs"].append(
    {"id": "ottery_reef", "at": {"tx": 18, "ty": 24}, "facing": "right", "sprite": "npc_old_woman",
     "movement": "static", "dialogue_ref": "script.lowtinder_reef_ottery",
     "requires_flag": "flag:lowtinder_at_reef"})


def deep_layer(m: dict) -> None:
    """Rows >= REEF_ROW of open water are DEEP — the outer reef, no shallow
    channels (mk.deep_water would carve one to every islet, and the reef islets
    are the point of rowing). Above the lip stays Tidecall-shallow."""
    mk.register_tileset("deepwater_set", index=mk.DEEPWATER_INDEX)
    m["tilesets"].append(mk.register_tileset("deepwater_set", index=mk.DEEPWATER_INDEX))
    deep = [1 if (water[i] and i // W >= REEF_ROW) else 0 for i in range(W * H)]
    layer = {"name": "t_deepwater", "role": "terrain", "terrain": "deepwater",
             "set": "deepwater_set", "depth": 0, "data": deep}
    last = max(i for i, ly in enumerate(m["layers"]) if ly.get("role") in ("terrain", "base"))
    m["layers"].insert(last + 1, layer)


if __name__ == "__main__":
    deep_layer(m)
    pt.report(owed)
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
