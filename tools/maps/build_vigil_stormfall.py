#!/usr/bin/env python3
"""
Vigil III — Stormfall (`vigil_stormfall`) — "the wind's spare pocket"
(walkthrough/06-postgame §STARFALL VIGILS, the one-shape annex). An aerie
shelf above Thunderroost: scoured grass and hail-pitted stone, the third
star-shard crackling in a nest of fulgurite (a boulder ring on scree).

The one shape: shard set-piece far end · Ondra Vael posted before it behind
the un-walk-aroundable trial band (`script.vigil_stormfall`, hidden once
`flag:vigil_3_kept`) · three flag-disjoint keeper placements · two frosttuft
encounter zones in the 62-64 band (NULLHUSK #144 very rare — the register
ledger's northern single) · one cache (`starglass_shard` x2 — the
storm-tithe's second half; the script also pays the 5,000w jackpot) · NO
rest point.

Host edit (add_vigil_scars.py): thunderroost (5,2) `to_vigil_storm`,
`requires_flag: flag:vigil_reading_3`. Reuse: windward-stair-a loop +
backdrops (the host's keys).

audit_flow note — a one-portal dead-end annex: the screen IS the payoff
(§3a r5); the trial band rides the nest shelf's only mouth.

Run:  ./venv/bin/python tools/maps/build_vigil_stormfall.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 18
rng = random.Random(333)
owed: list[str] = []

ENTRY = (11, 16)          # thunderroost's to_vigil_storm lands here
SHARD_AT = (11, 2)
KEEPER_AT = (11, 4)
BAND_Y, BAND_X = 6, (10, 13)
CACHE_AT = (20, 12)

# ---- terrain ------------------------------------------------------------------------
glacier = mk.make_grid(W, H)   # the crag enclosure + the nest shelf's flanks
mk.rect(glacier, W, H, 0, 0, W - 1, 1)
mk.rect(glacier, W, H, 0, 0, 1, H - 1)
mk.rect(glacier, W, H, 22, 0, 23, H - 1)
mk.rect(glacier, W, H, 0, 16, W - 1, H - 1)
mk.organic_border(glacier, W, H, depth=0,
                  bumps=[(2, 9, 1), (21, 13, 2), (8, 16, 1), (21, 3, 1)], rng=rng)
mk.rect(glacier, W, H, 2, 2, 9, 6)             # nest shelf, west flank
mk.rect(glacier, W, H, 14, 2, 21, 6)           # nest shelf, east flank
glacier[16 * W + 11] = 0                        # the entry seam (ENTRY)

# the cache pocket: a boulder-choked notch in the east crag (carved back out)
for (x, y) in [(20, 12), (20, 13), (19, 13)]:
    glacier[y * W + x] = 0

# the roost-beds: scoured frost-tufts, two beds (two zones by design)
tuft = mk.make_grid(W, H)
mk.blob(tuft, W, H, 6.0, 11.0, 2.8, 2.0)
mk.blob(tuft, W, H, 16.0, 10.0, 2.6, 1.8)
for i in range(W * H):
    if glacier[i]:
        tuft[i] = 0
for (x, y) in [(11, 14), (11, 15), (12, 14), (10, 14)]:
    tuft[y * W + x] = 0                         # keep the entry lane clear

terrain_layers = [
    {"name": "t_tuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": tuft},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
]

# ---- base: wind-scoured snow, hail-pitted with scree -----------------------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]
scree = [gid("scree0"), gid("scree1"), gid("scree2")]
pits = mk.make_grid(W, H)                       # the hail-pitted stone aprons
mk.blob(pits, W, H, 11.5, 3.5, 2.8, 2.0)        # the nest shelf floor is bare stone
mk.blob(pits, W, H, 12.5, 9.0, 2.0, 1.4)
mk.blob(pits, W, H, 4.0, 14.5, 1.6, 1.1)
for i in range(W * H):
    if pits[i] and not glacier[i] and not tuft[i]:
        base[i] = rng.choice(scree)

m: dict = {
    "id": "vigil_stormfall", "display_name": "Stormfall",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [
        # THE SHARD — crackling in its fulgurite nest
        {"id": "star_shard", "sprite": "vigil_star_shard",
         "at": {"tx": SHARD_AT[0], "ty": SHARD_AT[1]}, "w": 2, "h": 2, "overhang": 1},
        # the old fliers' cairn on the shelf approach (the wind country's marker)
        {"id": "shelf_cairn", "sprite": "windward_cairn", "at": {"tx": 4, "ty": 9},
         "w": 1, "h": 2},
    ],
    "warps": [
        # the drop back to the roost — lands ON thunderroost's to_vigil_storm
        {"id": "to_thunderroost", "at": {"tx": ENTRY[0], "ty": ENTRY[1]},
         "trigger": "step_on", "to_map": "thunderroost", "to": {"tx": 5, "ty": 2},
         "facing": "down", "transition": "fade"},
    ],
    "triggers": [
        # THE TRIAL BAND — every walkable tile of the nest shelf's mouth
        *[{"id": f"vigil_trial_{i}", "kind": "cutscene",
           "at": {"tx": x, "ty": BAND_Y}, "activation": "step_on",
           "ref": "script.vigil_stormfall",
           "hidden_when_flag": "flag:vigil_3_kept"}
          for i, x in enumerate(range(BAND_X[0], BAND_X[1] + 1))],
    ],
    "encounters": [],
    "npcs": [
        # ONDRA VAEL — trial -> kept -> post-crown re-runnable bout
        {"id": "ondra_trial", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.vigil_stormfall",
         "hidden_when_flag": "flag:vigil_3_kept"},
        {"id": "ondra_kept", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "npc.vigil_stormfall_kept",
         "requires_flag": "flag:vigil_3_kept",
         "hidden_when_flag": "flag:starfall_crown"},
        {"id": "ondra_bout", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_woman", "movement": "static",
         "dialogue_ref": "script.vigil_stormfall_again",
         "requires_flag": "flag:starfall_crown"},
    ],
    "gates": [],
    # the one-shape reuse rule: the HOST's loop + backdrops
    "music": "assets/audio/music/windward-stair-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/windward-stair-a.webp",
        "assets/backgrounds/battle/windward-stair-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- the cache (starglass_shard x2 — the tithe's second half) -------------------------
deco[12 * W + 19] = gid("boulder")              # the pocket's pinch
owed += pt.cache(m, cid="vigil_storm_tithe", at=CACHE_AT)

# the fulgurite nest: a boulder ring around the shard's shelf
for (x, y) in [(10, 2), (13, 3), (10, 5), (14, 7), (9, 7)]:
    if not glacier[y * W + x]:
        deco[y * W + x] = gid("boulder")

# ---- encounters: the spec table VERBATIM (06-postgame, Vigil III hooks) ---------------
STORM_TABLE = [
    {"kin_id": 102, "weight": 28, "min_level": 62, "max_level": 64},  # Tempestail (uncommon)
    {"kin_id": 99, "weight": 27, "min_level": 62, "max_level": 64},   # Vortavane (uncommon)
    {"kin_id": 79, "weight": 22, "min_level": 62, "max_level": 64},   # Glacitern (uncommon)
    {"kin_id": 90, "weight": 15, "min_level": 63, "max_level": 64},   # Strikeaven (rare)
    {"kin_id": 144, "weight": 8, "min_level": 64, "max_level": 64},   # NULLHUSK (very rare)
]
m["encounters"] += pt.zones_from_grid(tuft, W, H, terrain="tall_grass",
                                      rate=0.12, table=STORM_TABLE, id_prefix="storm_bed")

# ---- wind-scoured dressing --------------------------------------------------------------
avoid = {(x, BAND_Y) for x in range(BAND_X[0], BAND_X[1] + 1)}
avoid |= {ENTRY, KEEPER_AT, CACHE_AT}
avoid |= {(x, y) for o in m["objects"]
          for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
          for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
for (x, y, name) in [(7, 8, "greymoss_a"), (15, 13, "greymoss_b"), (3, 12, "g_pebble"),
                     (17, 7, "g_pebble"), (9, 13, "greymoss_a"), (13, 12, "g_pebble"),
                     (6, 15, "boulder"), (18, 14, "boulder")]:
    i = y * W + x
    if not glacier[i] and not tuft[i] and (x, y) not in avoid and deco[i] == 0:
        deco[i] = gid(name)

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
