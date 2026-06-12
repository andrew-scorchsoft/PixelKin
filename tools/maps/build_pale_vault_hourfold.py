#!/usr/bin/env python3
"""
The Hourfold — Midnight in the deep ice (walkthrough/07-the-three §5: Site II
of the Three Hours). An annex off pale_vault_glacier's Emberward deep-ice
fold; the host edit is ONE warp (`to_hourfold`, sealed behind
flag:three_mid_snuffer — Ysolde's Vigil Snuffer, wiring pass).

A band colder and dimmer than the glacier: bone snow, terraced blue ice, the
aurora the only wayfinding. Three signature touches (§8):
  1. THE LEDGE DESCENT — three tiers dropped by one-way snow ledges; TWO
     FALSE LINES (x13-14 on tier 1, x15-16 on tier 2) shunt into walled
     pockets whose only way out is the east re-climb corridor back to the
     mouth — a wrong drop costs the walk, never progress. The TRUE line runs
     UNDER THE BRIGHTEST RIBBONS: blue ice strips painted down the floor mark
     the honest drops (x6-7, then x4-5).
  2. THE UNSTRUCK TOLL — three vigil-braziers on the bottom shelf, SNUFFED in
     aurora order east -> centre -> west (the game's one inverted light verb).
     Flag-chained interacts; a wrong-order press answers with the blocked
     line ("the flame leans away from the snuffer") and NOTHING resets — the
     braziers stay out once snuffed (flags persist; hooks verbatim, §5
     callout: the cooldown is the real cost, the re-climb is short).
  3. THE HOLLOWING'S SHADOW — one weathered null-lantern at the mouth,
     half-reclaimed by ice. No script touches it.

THE TOLL (one-flag-per-trigger; the solarium Lit-Stage encoding):
  brazier_east   requires flag:three_mid_snuffer (held to be here — consumed
                 per spine §0 r3) -> script.three_mid_brazier_a -> _a
  brazier_centre requires _a -> script.three_mid_brazier_b -> _b
  brazier_west   requires _b -> script.three_mid_brazier_c -> _c
  all three      blocked_ref npc.hourfold_flame_leans (the wrong-order line)
  lit -> snuffed object swaps key the same flags (same footprint+solidity).
NOCTILUNE (`hour_midnight`, sprite kin_161_overworld) resolves on the far
west end of the shelf once _c is held; interact -> script.three_midnight_battle.

The set-piece op (wiring pass, content/scripts.ts — hooks VERBATIM):
  { op: 'legendaryBattle', name: 'three_midnight', kin: 161, level: 48,
    caughtFlag: 'flag:three_mid_caught', cooldownBattles: 14,
    cooldownRef: 'npc.three_midnight_resting', terrain: 'cave' }

ENCOUNTERS: sparse cave 44-48 (deep-ice register, a touch above the North
curve by design — the hooks' "a place you return TO"): Stillwarden #85,
Prismantus #87, Glaceling #72. CURATED_AREAS/EXTRA_ENCOUNTERS mirror =
wiring pass (the solarium precedent). Trainer-free.

audit_flow WAIVER — `free-pass` WARN accepted if raised: a shrine spur, not
a through-route; the toll and the Hour are the destination.

Run:  ./venv/bin/python tools/maps/build_pale_vault_hourfold.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 20
rng = random.Random(161)
owed: list[str] = []

MOUTH = (17, 2)            # to_glacier pad; host to_hourfold lands ON it

# ---- terrain: glacier walls; tiers, pockets and the corridor carved -----------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)


def carve(x0, y0, x1, y1):
    mk.rect(wall, W, H, x0, y0, x1, y1, 0)


carve(3, 2, 19, 5)         # TIER 1 (+ the mouth room, NE)
carve(20, 3, 20, 16)       # THE RE-CLIMB CORRIDOR (east, 1-wide — the honest
carve(20, 2, 20, 2)        # long way down AND the short way back up)
carve(21, 9, 21, 9)        # a breather alcove (breaks the corridor wall's run)
# tier boundary B1 (y6) stays wall except the ledge cells (deco below)
carve(3, 7, 10, 11)        # TIER 2 (west half; the false-line pocket is split off)
carve(3, 9, 19, 11)        # tier 2's full lower rows
carve(12, 7, 19, 7)        # POCKET P1 (the false drops' shunt shelf)
carve(6, 6, 7, 6)          # TRUE ledge cells pierce B1...
carve(13, 6, 14, 6)        # ...and the FALSE ones
# tier boundary B2 (y12) stays wall except its ledge cells
carve(4, 12, 5, 12)        # TRUE ledge cells pierce B2...
carve(15, 12, 16, 12)      # ...and the FALSE ones
carve(3, 13, 12, 17)       # TIER 3 — the bottom shelf (the toll + the Hour)
carve(14, 13, 19, 14)      # POCKET P2 (behind tier 2's false line; the cache)
carve(14, 16, 19, 17)      # tier 3's east apron joining the corridor
# re-seal the pocket dividers the broad carves opened
mk.rect(wall, W, H, 11, 7, 11, 8)      # P1's west wall
mk.rect(wall, W, H, 12, 8, 19, 8)      # P1's floor wall (drops land IN P1)
mk.rect(wall, W, H, 13, 13, 13, 14)    # P2's west wall
mk.rect(wall, W, H, 14, 15, 19, 15)    # P2's floor wall

# ---- the aurora ribbons (blue ice strips marking the TRUE line) ---------------------
ice = mk.make_grid(W, H)
mk.rect(ice, W, H, 6, 2, 7, 5)         # tier 1: the ribbon over the true drop
mk.rect(ice, W, H, 6, 7, 7, 8)         # ...landing pool
mk.rect(ice, W, H, 4, 9, 5, 11)        # tier 2: the ribbon bends west
mk.rect(ice, W, H, 4, 13, 6, 14)       # ...and kneels onto the shelf
mk.blob(ice, W, H, 9.0, 16.0, 1.6, 1.0)  # the water-ice the verse names

# ---- frost tufts (dressing only — no tall_grass zone, so they never roll) -----------
tuft = mk.make_grid(W, H)
for (x, y) in [(4, 3), (16, 4), (9, 10), (18, 11), (11, 16), (17, 17)]:
    tuft[y * W + x] = 1

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if wall[i]:
        ice[i] = tuft[i] = 0
    if ice[i]:
        tuft[i] = 0

# ---- base: bone snow ----------------------------------------------------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ice", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": ice},
    {"name": "t_tuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": tuft},
    {"name": "t_wall", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco: the ledge lines, the dead null-lantern, scatter --------------------------
deco = mk.make_grid(W, H)
# B1 ledges: TRUE under the ribbon (x6-7), FALSE into P1 (x13-14)
pt.ledge_run(deco, W, H, 6, 6, 7, rng, family="snow")
pt.ledge_run(deco, W, H, 6, 13, 14, rng, family="snow")
# B2 ledges: TRUE under the bent ribbon (x4-5), FALSE into P2 (x15-16)
pt.ledge_run(deco, W, H, 12, 4, 5, rng, family="snow")
pt.ledge_run(deco, W, H, 12, 15, 16, rng, family="snow")
# the Hollowing's shadow: one dead null-lantern at the fold mouth (no script)
deco[3 * W + 19] = gid("null_lantern")
# grey moss + pebbles in the cold
for (x, y, n) in [(5, 4, "greymoss_a"), (15, 5, "greymoss_b"), (8, 9, "greymoss_b"),
                  (18, 10, "greymoss_a"), (10, 14, "greymoss_b"), (16, 13, "greymoss_a")]:
    deco[y * W + x] = gid(n)
for (x, y) in [(10, 3), (17, 9), (6, 10), (8, 16), (18, 16), (15, 7), (12, 15), (21, 9)]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid("g_pebble")
for (x, y) in [(12, 4), (8, 11), (19, 17)]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid("boulder")

# ---- assemble -----------------------------------------------------------------------
m: dict = {
    "id": "pale_vault_hourfold", "display_name": "The Hourfold",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    # the fold reuses the glacier loop's sparsest variant (the undercroft's cue)
    "music": "assets/audio/music/pale-vault-glacier-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/hourfold-a.webp",
    ],
}

# ---- THE UNSTRUCK TOLL: three vigil-braziers, snuffed east -> centre -> west --------
BRAZIERS = [
    ("east", (11, 14), "flag:three_mid_snuffer", "flag:three_mid_brazier_a", "a"),
    ("centre", (7, 14), "flag:three_mid_brazier_a", "flag:three_mid_brazier_b", "b"),
    ("west", (3, 14), "flag:three_mid_brazier_b", "flag:three_mid_brazier_c", "c"),
]
for name, (bx, by), req, sets, tag in BRAZIERS:
    m["objects"] += [
        {"id": f"brazier_{name}_lit", "sprite": "hourfold_brazier_lit",
         "at": {"tx": bx, "ty": by}, "w": 2, "h": 3, "overhang": 1,
         "hidden_when_flag": sets},
        {"id": f"brazier_{name}_snuffed", "sprite": "hourfold_brazier_snuffed",
         "at": {"tx": bx, "ty": by}, "w": 2, "h": 3, "overhang": 1,
         "requires_flag": sets},
    ]
    m["triggers"].append(
        {"id": f"brazier_{name}", "kind": "script", "at": {"tx": bx, "ty": by + 2},
         "activation": "interact", "ref": f"script.three_mid_brazier_{tag}",
         "once": True, "requires_flag": req,
         "blocked_ref": "npc.hourfold_flame_leans",
         "sets_flags": [sets], "hidden_when_flag": sets})
owed += ["script.three_mid_brazier_a (the east flame goes under the Vigil "
         "Snuffer; sets flag:three_mid_brazier_a)",
         "script.three_mid_brazier_b (sets flag:three_mid_brazier_b)",
         "script.three_mid_brazier_c (the last light out; hold the longest "
         "silence in the game, then the far shelf resolves; sets "
         "flag:three_mid_brazier_c)",
         "npc.hourfold_flame_leans ('the flame leans away from the snuffer' — "
         "the wrong-order line, hooks verbatim)"]

# ---- the aurora verse (names the order: east, the water-ice, west) ------------------
owed += pt.sign(m, deco, W, sid="hourfold_aurora", at=(9, 17))

# ---- THE STILL HOUR -----------------------------------------------------------------
m["npcs"].append(
    {"id": "hour_midnight", "at": {"tx": 3, "ty": 17}, "facing": "right",
     "sprite": "kin_161_overworld", "movement": "static",
     "dialogue_ref": "script.three_midnight_battle",
     "requires_flag": "flag:three_mid_brazier_c",
     "hidden_when_flag": "flag:three_mid_caught"})
owed += ["script.three_midnight_battle (silence 1200 -> narrate 'The dark does "
         "not deepen. It straightens, as if relieved of a stoop.' -> "
         "sting-hour -> battle-hours -> the op VERBATIM in the docstring)",
         "npc.three_midnight_resting (the {remaining} cooldown hint — §7 verbatim)"]

# ---- the cache (MISSABLE, behind tier 2's false ledge line — the §5 nugget) ---------
owed += pt.cache(m, cid="hourfold_amber", at=(18, 14))

# ---- warps --------------------------------------------------------------------------
m["warps"].append(
    # back out to the glacier's deep-ice fold — lands ON the host's to_hourfold
    {"id": "to_glacier", "at": {"tx": MOUTH[0], "ty": MOUTH[1]}, "trigger": "step_on",
     "to_map": "pale_vault_glacier", "to": {"tx": 26, "ty": 27}, "facing": "up",
     "transition": "door"})

# ---- encounters (sparse cave 44-48 — the deep-ice register) -------------------------
TABLE = [{"kin_id": 85, "weight": 40, "min_level": 44, "max_level": 48},
         {"kin_id": 87, "weight": 35, "min_level": 44, "max_level": 47},
         {"kin_id": 72, "weight": 25, "min_level": 44, "max_level": 46}]
m["encounters"] += [
    {"id": "fold_tiers", "terrain": "cave", "rect": {"tx": 3, "ty": 7, "w": 8, "h": 5},
     "encounter_rate": 0.08, "table": TABLE},
    {"id": "fold_shelf", "terrain": "cave", "rect": {"tx": 5, "ty": 16, "w": 8, "h": 2},
     "encounter_rate": 0.08, "table": TABLE},
]

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
