#!/usr/bin/env python3
"""
Vigil V — Murkfall (`vigil_murkfall`) — "where the water forgot how to speak"
(walkthrough/06-postgame §STARFALL VIGILS, the one-shape annex; the one place
the chain turns quiet). A fold of the deep marsh where the Hollowing's drain
is HEALING: colour seeping back at the edges (grass patches in the blight),
one snuffed lantern-row relit, the last star-shard glowing in shallow black
water. Gentle staging — Arc B's last echo, not a haunted house.

The one shape: shard set-piece far end · Warden Mer posted before it behind
the un-walk-aroundable trial band (`script.vigil_murkfall`, hidden once
`flag:vigil_5_kept`) · three flag-disjoint keeper placements · two blighttuft
encounter zones in the 66-68 band (SOLARMOURN #128 / CINDERVAST #145 /
BOGVAST #146 very rare — the register ledger's mirror-axis trio) · one
starglass cache · NO rest point.

Stacks the `coldfog_set` ACCENT tileset (fogcrag border — the host cluster's
family). Host edit (add_vigil_scars.py): coldfog_marches_ii (14,23)
`to_vigil_murk`, `requires_flag: flag:vigil_reading_5`. Reuse:
coldfog-marches-a loop + backdrops (the host's keys).

audit_flow note — a one-portal dead-end annex: the screen IS the payoff
(§3a r5); the trial band rides the shard hollow's only mouth.

Run:  ./venv/bin/python tools/maps/build_vigil_murkfall.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 18
rng = random.Random(335)
owed: list[str] = []

ENTRY = (11, 16)          # coldfog_marches_ii's to_vigil_murk lands here
SHARD_AT = (11, 2)
KEEPER_AT = (11, 4)
BAND_Y, BAND_X = 6, (10, 13)
CACHE_AT = (20, 3)

COLDFOG_REF = mk.register_tileset(
    "coldfog_set", index=mk.REPO / "assets/tilesets/coldfog/coldfog_set.index.json")

# ---- terrain ------------------------------------------------------------------------
crag = mk.make_grid(W, H)      # fogcrag enclosure + the hollow's flanks
mk.rect(crag, W, H, 0, 0, W - 1, 1)
mk.rect(crag, W, H, 0, 0, 1, H - 1)
mk.rect(crag, W, H, 22, 0, 23, H - 1)
mk.rect(crag, W, H, 0, 16, W - 1, H - 1)
mk.organic_border(crag, W, H, depth=0,
                  bumps=[(2, 7, 1), (21, 14, 1), (6, 16, 1)], rng=rng)
mk.rect(crag, W, H, 2, 2, 9, 6)                # hollow west flank
mk.rect(crag, W, H, 14, 2, 18, 6)              # hollow east flank (the cache lane passes east)
crag[16 * W + 11] = 0                           # the entry seam (ENTRY)

# the black water: still pools, the shard's shallow one inside the hollow
murk = mk.make_grid(W, H)
murk[2 * W + 13] = 1                            # the shard's shallow (beside the set-piece)
murk[3 * W + 13] = 1
mk.blob(murk, W, H, 5.5, 12.5, 2.4, 1.7)        # west pool
mk.blob(murk, W, H, 17.0, 12.0, 2.0, 1.4)       # east pool
for i in range(W * H):
    if crag[i]:
        murk[i] = 0

# colour seeping back: living-grass patches in the blight (the healing edges)
heal = mk.make_grid(W, H)
mk.blob(heal, W, H, 11.5, 9.0, 2.4, 1.6)        # around the lantern-row lane
mk.blob(heal, W, H, 8.0, 14.0, 1.6, 1.2)
mk.blob(heal, W, H, 15.5, 8.0, 1.4, 1.1)

# the reed beds, waking (the 66-68 grind beds; two zones by design)
tuft = mk.make_grid(W, H)
mk.blob(tuft, W, H, 5.0, 9.5, 2.6, 1.9)
mk.blob(tuft, W, H, 18.0, 9.5, 2.4, 1.8)
for i in range(W * H):
    if crag[i] or murk[i]:
        tuft[i] = 0
for (x, y) in [(11, 14), (11, 15), (10, 14), (12, 14)]:
    tuft[y * W + x] = 0                         # keep the entry lane clear

terrain_layers = [
    {"name": "t_tuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": tuft},
    {"name": "t_murk", "role": "terrain", "terrain": "murk",
     "set": "vesper_overworld_set", "depth": 0, "data": murk},
    {"name": "t_fogcrag", "role": "terrain", "terrain": "fogcrag",
     "set": "coldfog_set", "depth": 0, "data": crag},
]

# ---- base: blight, healing — living grass blooming through the grey --------------------
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(bl) if rng.random() < 0.5 else bl[0] for _ in range(W * H)]
for i in range(W * H):
    if heal[i] and not crag[i] and not murk[i] and not tuft[i]:
        base[i] = rng.choice(gr)

m: dict = {
    "id": "vigil_murkfall", "display_name": "Murkfall",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref(), COLDFOG_REF],
    "objects": [
        # THE SHARD — glowing in shallow black water, the first thing to win
        {"id": "star_shard", "sprite": "vigil_star_shard",
         "at": {"tx": SHARD_AT[0], "ty": SHARD_AT[1]}, "w": 2, "h": 2, "overhang": 1},
        # THE RELIT ROW — the snuffed lantern-line, burning again (gentle; the
        # lit/dark pair shares footprint+solidity, the standing swap rule —
        # here always lit: this fold has already turned)
        {"id": "relit_lantern_a", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 9, "ty": 12}, "w": 1, "h": 2, "overhang": 1},
        {"id": "relit_lantern_b", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 13, "ty": 10}, "w": 1, "h": 2, "overhang": 1},
        {"id": "relit_lantern_c", "sprite": "saltreach_reed_lantern_lit",
         "at": {"tx": 9, "ty": 8}, "w": 1, "h": 2, "overhang": 1},
        # one still dark, at the fold's edge — the work isn't finished, only begun
        {"id": "dark_lantern", "sprite": "saltreach_reed_lantern_dark",
         "at": {"tx": 19, "ty": 14}, "w": 1, "h": 2, "overhang": 1},
    ],
    "warps": [
        # back along the jetty seam — lands ON coldfog_marches_ii's to_vigil_murk
        {"id": "to_coldfog", "at": {"tx": ENTRY[0], "ty": ENTRY[1]},
         "trigger": "step_on", "to_map": "coldfog_marches_ii", "to": {"tx": 14, "ty": 23},
         "facing": "up", "transition": "fade"},
    ],
    "triggers": [
        # THE TRIAL BAND — every walkable tile of the shard hollow's mouth
        *[{"id": f"vigil_trial_{i}", "kind": "cutscene",
           "at": {"tx": x, "ty": BAND_Y}, "activation": "step_on",
           "ref": "script.vigil_murkfall",
           "hidden_when_flag": "flag:vigil_5_kept"}
          for i, x in enumerate(range(BAND_X[0], BAND_X[1] + 1))],
    ],
    "encounters": [],
    "npcs": [
        # WARDEN MER — trial -> kept -> post-crown re-runnable bout
        {"id": "mer_trial", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.vigil_murkfall",
         "hidden_when_flag": "flag:vigil_5_kept"},
        {"id": "mer_kept", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "npc.vigil_murkfall_kept",
         "requires_flag": "flag:vigil_5_kept",
         "hidden_when_flag": "flag:starfall_crown"},
        {"id": "mer_bout", "at": {"tx": KEEPER_AT[0], "ty": KEEPER_AT[1]},
         "facing": "down", "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.vigil_murkfall_again",
         "requires_flag": "flag:starfall_crown"},
    ],
    "gates": [],
    # the one-shape reuse rule: the HOST's loop + backdrops
    "music": "assets/audio/music/coldfog-marches-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/coldfog-marches-a.webp",
        "assets/backgrounds/battle/coldfog-marches-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- the cache (starglass_shard x1), up the east bank lane -----------------------------
deco[4 * W + 19] = gid("boulder")
deco[5 * W + 21] = gid("boulder")
owed += pt.cache(m, cid="vigil_murk_glass", at=CACHE_AT)

# ---- encounters: the spec table VERBATIM (06-postgame, Vigil V hooks) ------------------
MURK_TABLE = [
    {"kin_id": 142, "weight": 27, "min_level": 66, "max_level": 68},  # Embergone (uncommon)
    {"kin_id": 138, "weight": 27, "min_level": 66, "max_level": 68},  # Voidmantle (uncommon)
    {"kin_id": 140, "weight": 25, "min_level": 66, "max_level": 68},  # Wisprestored (uncommon)
    {"kin_id": 128, "weight": 7, "min_level": 67, "max_level": 67},   # SOLARMOURN (very rare)
    {"kin_id": 145, "weight": 7, "min_level": 67, "max_level": 67},   # CINDERVAST (very rare)
    {"kin_id": 146, "weight": 7, "min_level": 68, "max_level": 68},   # BOGVAST (very rare)
]
m["encounters"] += pt.zones_from_grid(tuft, W, H, terrain="tall_grass",
                                      rate=0.12, table=MURK_TABLE, id_prefix="murk_bed")

# ---- the marsh, waking -------------------------------------------------------------------
avoid = {(x, BAND_Y) for x in range(BAND_X[0], BAND_X[1] + 1)}
avoid |= {ENTRY, KEEPER_AT, CACHE_AT}
avoid |= {(x, y) for o in m["objects"]
          for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
          for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
for (x, y, name) in [(7, 8, "greymoss_a"), (16, 14, "greymoss_b"), (4, 15, "g_pebble"),
                     (14, 8, "flowers"), (10, 10, "g_daisy"), (8, 11, "g_tuft"),
                     (20, 8, "greymoss_a"), (12, 12, "g_daisy")]:
    i = y * W + x
    if not (crag[i] or murk[i] or tuft[i]) and (x, y) not in avoid and deco[i] == 0:
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
