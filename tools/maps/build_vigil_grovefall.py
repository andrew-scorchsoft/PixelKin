#!/usr/bin/env python3
"""
Vigil II — Grovefall (`vigil_grovefall`) — "under the hill, where the moss has
opinions" (walkthrough/06-postgame §STARFALL VIGILS, the one-shape annex). A
glowmoss cathedral-cell beyond the Spore Grotto: the second star-shard seated
in a fungal vault that grew around it in a season. Kind `cave`.

The one shape: shard set-piece far end · Old Foreman Bramm posted before it
behind the un-walk-aroundable trial band (`script.vigil_grovefall`, hidden
once `flag:vigil_2_kept`) · three flag-disjoint keeper placements · two
glowmoss encounter zones in the 60-62 band (MYCOVAST #70 very rare — the
register ledger's eastern single) · one starglass cache · NO rest point.

Rooms are carved as overlapping RECTs joined by explicit corridors (the
blob-edge-adjacency gotcha). Host edit (add_vigil_scars.py): spore_grotto
(15,9) `to_vigil_grove`, `requires_flag: flag:vigil_reading_2`. Reuse:
lowleaf-hollow-c loop + glowmoss-deep backdrops (the host's keys).

audit_flow note — a one-portal dead-end annex: the screen IS the payoff
(§3a r5); the trial band rides the vault's only mouth.

Run:  ./venv/bin/python tools/maps/build_vigil_grovefall.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 18
rng = random.Random(332)
owed: list[str] = []

ENTRY = (11, 16)          # spore_grotto's to_vigil_grove lands here
SHARD_AT = (11, 2)
KEEPER_AT = (11, 4)
BAND_Y, BAND_X = 6, (10, 13)
CACHE_AT = (19, 4)

# ---- terrain: rooms carved from solid rock -------------------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 8, 12, 15, 15)            # entry chamber
floor[16 * W + 11] = 1                          # the seam in (ENTRY)
mk.rect(floor, W, H, 11, 7, 12, 12)            # the rising throat
mk.rect(floor, W, H, 3, 7, 10, 10)             # west bed hall
mk.rect(floor, W, H, 13, 8, 20, 11)            # east bed hall
mk.rect(floor, W, H, 10, 2, 13, 6)             # the VAULT (alcove + its mouth row)
mk.vline(floor, W, H, 19, 4, 8)                # the cache spur, off the east hall
floor[4 * W + 20] = 1                           # a breath beside the prize
for i in range(W * H):
    if floor[i]:
        wall[i] = 0

# the two glowmoss beds (the 60-62 grind beds; two zones by design)
glow = mk.make_grid(W, H)
mk.blob(glow, W, H, 6.0, 8.5, 2.8, 1.7)
mk.blob(glow, W, H, 16.5, 9.5, 2.6, 1.7)
for i in range(W * H):
    if glow[i] and not floor[i]:
        glow[i] = 0
glow[8 * W + 19] = 0                            # keep the cache spur's mouth clear

terrain_layers = [
    {"name": "t_glowmoss", "role": "terrain", "terrain": "glowmoss",
     "set": "vesper_overworld_set", "depth": 0, "data": glow},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]

m: dict = {
    "id": "vigil_grovefall", "display_name": "Grovefall",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [
        # THE SHARD — seated in the vault the moss built for it
        {"id": "star_shard", "sprite": "vigil_star_shard",
         "at": {"tx": SHARD_AT[0], "ty": SHARD_AT[1]}, "w": 2, "h": 2},
        # the ember-capped huddle grown up the vault's east wall
        {"id": "vault_shrooms", "sprite": "glowmoss_deep_glowshrooms_ember",
         "at": {"tx": 13, "ty": 2}, "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    ],
    "warps": [
        # back through the seam — lands ON spore_grotto's to_vigil_grove
        {"id": "to_spore_grotto", "at": {"tx": ENTRY[0], "ty": ENTRY[1]},
         "trigger": "step_on", "to_map": "spore_grotto", "to": {"tx": 15, "ty": 9},
         "facing": "left", "transition": "fade"},
    ],
    "triggers": [
        # THE TRIAL BAND — every walkable tile of the vault mouth
        *[{"id": f"vigil_trial_{i}", "kind": "cutscene",
           "at": {"tx": x, "ty": BAND_Y}, "activation": "step_on",
           "ref": "script.vigil_grovefall",
           "hidden_when_flag": "flag:vigil_2_kept"}
          for i, x in enumerate(range(BAND_X[0], BAND_X[1] + 1))],
    ],
    "encounters": [],
    "npcs": [
        # OLD FOREMAN BRAMM — trial -> kept -> post-crown re-runnable bout
        {"id": "bramm_trial", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "script.vigil_grovefall",
         "hidden_when_flag": "flag:vigil_2_kept"},
        {"id": "bramm_kept", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.vigil_grovefall_kept",
         "requires_flag": "flag:vigil_2_kept",
         "hidden_when_flag": "flag:starfall_crown"},
        {"id": "bramm_bout", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "script.vigil_grovefall_again",
         "requires_flag": "flag:starfall_crown"},
    ],
    "gates": [],
    # the one-shape reuse rule: the HOST's loop + backdrops
    "music": "assets/audio/music/lowleaf-hollow-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/glowmoss-deep-a.webp",
        "assets/backgrounds/battle/glowmoss-deep-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- the cache (starglass_shard x1), behind a boulder pinch in the spur --------------
deco[4 * W + 20] = gid("boulder")
owed += pt.cache(m, cid="vigil_grove_glass", at=CACHE_AT)

# ---- encounters: the spec table VERBATIM (06-postgame, Vigil II hooks) ---------------
GROVE_TABLE = [
    {"kin_id": 68, "weight": 28, "min_level": 60, "max_level": 62},  # Fernlance (uncommon)
    {"kin_id": 64, "weight": 27, "min_level": 60, "max_level": 62},  # Rootwarden (uncommon)
    {"kin_id": 49, "weight": 22, "min_level": 60, "max_level": 62},  # Gravelo (uncommon)
    {"kin_id": 58, "weight": 15, "min_level": 61, "max_level": 62},  # Mycelarch (rare)
    {"kin_id": 70, "weight": 8, "min_level": 62, "max_level": 62},   # MYCOVAST (very rare)
]
m["encounters"] += pt.zones_from_grid(glow, W, H, terrain="tall_grass",
                                      rate=0.12, table=GROVE_TABLE, id_prefix="grove_bed")

# ---- the grotto's light -----------------------------------------------------------------
avoid = {(x, BAND_Y) for x in range(BAND_X[0], BAND_X[1] + 1)}
avoid |= {ENTRY, KEEPER_AT, CACHE_AT}
avoid |= {(x, y) for o in m["objects"]
          for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
          for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
for (x, y, name) in [(4, 7, "glowshroom_a"), (9, 12, "glowshroom_b"), (14, 11, "glowshroom_a"),
                     (20, 9, "glowshroom_b"), (10, 5, "glowshroom_a"), (13, 14, "greymoss_a"),
                     (3, 10, "greymoss_b"), (18, 8, "g_pebble"), (8, 14, "g_pebble")]:
    i = y * W + x
    if floor[i] and not glow[i] and (x, y) not in avoid and deco[i] == 0:
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
