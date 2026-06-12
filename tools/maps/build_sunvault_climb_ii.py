#!/usr/bin/env python3
"""
Sunvault Climb II — the sun-vine bridges (walkthrough/04-west "Sunvault Climb
I→II" beat 3; kind route, region west, band 47-48, the upper half). Living
sun-vine bridges climb to the observatory hill; the densest starfield in the
game sight-lines ahead (starglint decals at the north rim — the Arc D read:
six relit constellations overhead, the sky paling).

Three signature touches (§8):
  1. THE LIVING BRIDGES — two in-map sun-vine crossings (Sunsketch
     AbilityGates through the terrace walls, vine-gate art swapping
     withered->bloomed on gleam:solar — always bloomed in practice, since
     Sunsketch is the only way onto this map; the withered state is the
     honest pre-Gleam fiction).
  2. THE X3 VIEWPOINT TERRACE — the high star-reading terrace
     (script.chart_sunvault; "Charting the Dark" leg 1 — see the X3
     CONTRACT below).
  3. THE HELIA MOUTH — the sealed reliquary's door on the west wall
     (Sunsketch spur, §3a r8: signed, breadcrumbed, MISSABLE).
  4. THE VINE-SHADE REST TERRACE (W8 MIN-2 — the §3a mid-leg relief beat,
     the N6/N7 Windward rest-shelf precedent): a sun-vine arbor off the mid
     road shades a fallen-column seat at the end of the y17 jog (~halfway up
     the ~62-step climb, beside lamp_mid). Encounter-free open ground, NO
     heal — pressure relief, not an anchor; the jog now PAYS (§3a r4).

HANDSHAKE (W2-internal, built both sides): climb_i `to_climb_ii` at
(6,0)/(7,0) lands HERE at (6,26)/(7,26); our return pair `to_climb_i` at
(6,27)/(7,27) lands at climb_i (6,1)/(7,1) — both directions Sunsketch
(the vines are the boundary; graph.ts `to_climb_ii` bidirectional).
HANDSHAKE (W4, binding on the Nightreach builder): our `to_observatory`
warps at (22,0)/(23,0) land at nightreach_observatory (15,28)/(16,28) —
placeholder until W4 authors it (the engine no-ops). W4's map must keep
those landings WALKABLE (SOUTH-edge entry, width ≥17, the MAIN-PATH rim
approach, spine §0 rule 2) and its return pair must land at our
(22,1)/(23,1). UNGATED both ways.
SPUR (graph.ts verbatim): `to_helia` at (0,7)/(0,8), requires_ability
sunsketch (held — the §3 'now accessible' callout sign sits beside it),
landing helia_vault (23,10)/(23,11) ON its return pair, which lands back
at our (1,7)/(1,8).

X3 CONTRACT (binding on the W4 Nightreach builder): the junior watcher's
giver script (`script.chart_quest`) sets **flag:q_west_chart**; our
viewpoint trigger here requires it, runs `script.chart_sunvault` and sets
**flag:q_west_chart_1** (leg 1 of q_west_chart_1..3 -> q_west_chart_done;
the N2 sequential-sketch pattern).

THE VIGIL STRIKER (hooks verbatim): the old watcher's lost striker —
Nightreach lamp 1's collinear errand — is the NE-pocket cache here:
script.pickup_striker -> **flag:picked_striker** (band 48-50 ground, the
road the player walks anyway).

Trainer beat (route class, payout 16 x ace — wiring agent authors):
  sunvault_skywatcher "Sky-watcher Tam", 2 kin lv47-48, ace 48, payout 768.

Encounter picks (band 47-48, continuous with Climb I 46-47 and Nightreach
~48-52): the stage-2 Solar/Verdant roster leads; Lunveil/Lunvane bleed in
as the road nears Nightreach (their dex entries live there). Mirror into
EXTRA_ENCOUNTERS = wiring agent.

Suggested sign copy (wiring agent; sincere register):
  sign.sunvault_helia       "HELIA VAULT. A reliquary sealed by night-
                             flowers. What the Solarium drowned, this door
                             kept dry." (the 'now accessible (Sunsketch)'
                             callout + the spur warps' blocked_ref)
  sign.sunvault_observatory "NORTH — NIGHTREACH OBSERVATORY. The watchers
                             keep seven lamps for seven stars. Walk toward
                             the brightest sky in Vesperholm."

audit_flow notes — the NE striker pocket and the vine-gated amber shelf are
paid dead ends (§3a r4); the two band ledges compress the return (§3a r1/r2).

Run:  ./venv/bin/python tools/maps/build_sunvault_climb_ii.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 28
rng = random.Random(74)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
cliff = mk.make_grid(W, H)
ruin = mk.make_grid(W, H)
goldtuft = mk.make_grid(W, H)
deco = mk.make_grid(W, H)

# BORDERS
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.rect(cliff, W, H, 0, 26, W - 1, H - 1)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)
mk.rect(cliff, W, H, 28, 0, 29, H - 1)
mk.organic_border(cliff, W, H, depth=0,
                  bumps=[(12, 1, 2), (27, 13, 2), (1, 17, 2), (14, 26, 2),
                         (28, 22, 2), (1, 3, 2)],
                  rng=rng)
# SOUTH gap — the climb_i boundary (cols 6-7)
for y in (26, 27):
    for x in (6, 7):
        cliff[y * W + x] = 0
# NORTH gap — the Nightreach rim approach (cols 22-23)
for y in (0, 1):
    for x in (22, 23):
        cliff[y * W + x] = 0
# WEST gap — the Helia Vault mouth (rows 7-8)
for x in (0, 1):
    for y in (7, 8):
        cliff[y * W + x] = 0

# THE TERRACE BANDS: two cliff walls cut the climb into three zones; each is
# crossed only on a sun-vine bridge (Sunsketch gate) — the LIVING BRIDGES
mk.rect(cliff, W, H, 2, 19, 27, 20)           # band 1 (south/mid)
mk.blob(cliff, W, H, 20.0, 19.0, 1.8, 1.0)
mk.rect(cliff, W, H, 2, 11, 29, 12)           # band 2 (mid/upper)
mk.blob(cliff, W, H, 15.0, 11.5, 1.8, 1.0)
# bridge 1 pierce (cols 10-11) — the gate rides the cliff cells
for y in (19, 20):
    for x in (10, 11):
        pass                                   # cliff stays; the gate opens it
# bridge 2 pierce (cols 24-25) — same
# band LEDGES (the one-way returns): band 1 at x16-17, band 2 at x6-7
for x in (16, 17):
    cliff[19 * W + x] = 0
    cliff[20 * W + x] = 0
pt.ledge_run(deco, W, H, 19, 16, 17, rng, family="sand")
for x in (6, 7):
    cliff[11 * W + x] = 0
    cliff[12 * W + x] = 0
pt.ledge_run(deco, W, H, 11, 6, 7, rng, family="sand")

# THE X3 VIEWPOINT TERRACE (upper zone) — the star-reading high point
view = pt.Area(11, 3, 17, 8)
pt.terrace(cliff, deco, W, H, view, gap=(13, 14), gap_side="up", rim=1, rng=rng)
# THE NE STRIKER POCKET — a cliff finger shelters the old watcher's drop
# (entered off the north road at (24,3))
mk.rect(cliff, W, H, 24, 5, 27, 5)
mk.rect(cliff, W, H, 24, 2, 24, 5)
cliff[3 * W + 24] = 0                          # the pocket's mouth
# THE AMBER SHELF — sealed behind a 1-cell night-flower cut at (20,5)
mk.rect(cliff, W, H, 19, 2, 21, 5)
for (x, y) in ((20, 3), (20, 4)):
    cliff[y * W + x] = 0                      # shelf interior
cliff[5 * W + 20] = 1                          # the vine cut (gated below)

# ---- the garden-road (S-bends per §3a r11) ------------------------------------------
mk.rect(ruin, W, H, 6, 21, 7, 25)             # entry road north
mk.rect(ruin, W, H, 7, 21, 10, 22)            # east to bridge 1
mk.rect(ruin, W, H, 10, 18, 11, 22)           # bridge 1 approach + landing
mk.rect(ruin, W, H, 10, 13, 11, 18)           # mid road north
mk.rect(ruin, W, H, 11, 13, 25, 14)           # east to bridge 2
mk.rect(ruin, W, H, 24, 9, 25, 13)            # bridge 2 + landing
mk.rect(ruin, W, H, 9, 9, 25, 10)             # upper road west
mk.rect(ruin, W, H, 22, 2, 23, 9)             # north to the observatory
mk.rect(ruin, W, H, 2, 7, 8, 8)               # west to the Helia mouth
# jogs
mk.rect(ruin, W, H, 13, 17, 15, 17)
mk.rect(ruin, W, H, 18, 15, 20, 15)
mk.rect(ruin, W, H, 4, 22, 5, 23)

# ---- encounter terrain --------------------------------------------------------------
mk.blob(goldtuft, W, H, 18.0, 23.0, 3.0, 1.8)  # south garden (optional)
mk.blob(goldtuft, W, H, 4.5, 14.5, 2.0, 1.6)   # mid west pocket (optional)
mk.blob(goldtuft, W, H, 27.0, 8.0, 1.6, 1.2)   # upper east tuft
mk.blob(goldtuft, W, H, 5.5, 3.5, 2.2, 1.4)    # NW high garden (pays the pocket)
mk.blob(goldtuft, W, H, 3.0, 23.0, 1.8, 1.6)   # SW entry garden (pays the corner)
# MANDATORY crossing (§11 r7): mid zone, wall to wall, the road paused
pt.mandatory_band(goldtuft, ruin, W, H, y0=15, y1=16, x0=2, x1=27)

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if cliff[i]:
        ruin[i] = 0
        goldtuft[i] = 0
    if ruin[i]:
        goldtuft[i] = 0

# ---- base ---------------------------------------------------------------------------
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": ruin},
    {"name": "t_goldtuft", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": goldtuft},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

m: dict = {
    "id": "sunvault_climb_ii", "display_name": "Sunvault Climb",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [
        # the two LIVING BRIDGES — Sunsketch opens the cliff cells under the
        # vine-gate art (held by everyone here; the §5 'main-path bridges stay
        # simple' rule: a single bloom that stays open)
        {"id": "bridge_1", "ability": "sunsketch",
         "rect": {"tx": 10, "ty": 19, "w": 2, "h": 2}, "effect": "make_passable"},
        {"id": "bridge_2", "ability": "sunsketch",
         "rect": {"tx": 24, "ty": 11, "w": 2, "h": 2}, "effect": "make_passable"},
        # the amber shelf's night-flower cut (optional pocket)
        {"id": "amber_vines", "ability": "sunsketch",
         "rect": {"tx": 20, "ty": 5, "w": 1, "h": 1}, "effect": "make_passable"},
    ],
    "music": "assets/audio/music/sunvault-climb-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/sunvault-climb-a.webp",
        "assets/backgrounds/battle/sunvault-climb-b.webp",
    ],
}

# ---- warps (graph.ts edge ids verbatim) ---------------------------------------------
m["warps"] += [
    # SOUTH <-> sunvault_climb_i (both directions Sunsketch — the vines)
    {"id": "to_climb_i", "at": {"tx": 6, "ty": 27}, "trigger": "step_on",
     "to_map": "sunvault_climb_i", "to": {"tx": 6, "ty": 1}, "facing": "down",
     "requires_ability": "sunsketch",
     "blocked_ref": "sign.sunvault_vines", "transition": "fade"},
    {"id": "to_climb_i_e", "at": {"tx": 7, "ty": 27}, "trigger": "step_on",
     "to_map": "sunvault_climb_i", "to": {"tx": 7, "ty": 1}, "facing": "down",
     "requires_ability": "sunsketch",
     "blocked_ref": "sign.sunvault_vines", "transition": "fade"},
    # NORTH -> nightreach_observatory (`to_observatory`, UNGATED — the
    # MAIN-PATH rim approach; W4 authors the far side, landing is a
    # placeholder the engine no-ops; W4's return pair must land at our
    # (22,1)/(23,1))
    {"id": "to_observatory", "at": {"tx": 22, "ty": 0}, "trigger": "step_on",
     "to_map": "nightreach_observatory", "to": {"tx": 15, "ty": 28}, "facing": "up",
     "transition": "fade"},
    {"id": "to_observatory_e", "at": {"tx": 23, "ty": 0}, "trigger": "step_on",
     "to_map": "nightreach_observatory", "to": {"tx": 16, "ty": 28}, "facing": "up",
     "transition": "fade"},
    # WEST — the Helia Vault mouth (`to_helia`, Sunsketch — held; the
    # [MISSABLE] §3a r8 spur, signed beside it)
    {"id": "to_helia", "at": {"tx": 0, "ty": 7}, "trigger": "step_on",
     "to_map": "helia_vault", "to": {"tx": 23, "ty": 10}, "facing": "left",
     "requires_ability": "sunsketch",
     "blocked_ref": "sign.sunvault_helia", "transition": "door"},
    {"id": "to_helia_s", "at": {"tx": 0, "ty": 8}, "trigger": "step_on",
     "to_map": "helia_vault", "to": {"tx": 23, "ty": 11}, "facing": "left",
     "requires_ability": "sunsketch",
     "blocked_ref": "sign.sunvault_helia", "transition": "door"},
]

# ---- the bridge + shelf vine art (flag-pair swaps on gleam:solar) -------------------
m["objects"] += [
    {"id": "bridge_1_bloomed", "sprite": "sunvault_vine_gate_bloomed",
     "at": {"tx": 10, "ty": 18}, "w": 2, "h": 3, "solid": False,
     "requires_flag": "gleam:solar"},
    {"id": "bridge_1_withered", "sprite": "sunvault_vine_gate_withered",
     "at": {"tx": 10, "ty": 18}, "w": 2, "h": 3, "solid": False,
     "hidden_when_flag": "gleam:solar"},
    {"id": "bridge_2_bloomed", "sprite": "sunvault_vine_gate_bloomed",
     "at": {"tx": 24, "ty": 10}, "w": 2, "h": 3, "solid": False,
     "requires_flag": "gleam:solar"},
    {"id": "bridge_2_withered", "sprite": "sunvault_vine_gate_withered",
     "at": {"tx": 24, "ty": 10}, "w": 2, "h": 3, "solid": False,
     "hidden_when_flag": "gleam:solar"},
    {"id": "amber_vine_bloomed", "sprite": "sunvault_vine_v_bloomed",
     "at": {"tx": 20, "ty": 4}, "w": 1, "h": 3, "solid": False,
     "requires_flag": "gleam:solar"},
    {"id": "amber_vine_withered", "sprite": "sunvault_vine_v_withered",
     "at": {"tx": 20, "ty": 4}, "w": 1, "h": 3, "solid": False,
     "hidden_when_flag": "gleam:solar"},
]

# ---- THE X3 VIEWPOINT (the high terrace; contract in the docstring) -----------------
m["triggers"].append({
    "id": "chart_sunvault", "kind": "script", "at": {"tx": 14, "ty": 5},
    "activation": "interact", "ref": "script.chart_sunvault", "once": True,
    "requires_flag": "flag:q_west_chart",
    "sets_flags": ["flag:q_west_chart_1"],
    "hidden_when_flag": "flag:q_west_chart_1"})
owed += ["script.chart_sunvault (X3 leg 1 — the star-reading from the high "
         "terrace; requires flag:q_west_chart [set by W4's junior-watcher "
         "giver]; sets flag:q_west_chart_1)"]
# starglints over the terrace + the north rim (the densest-starfield read)
for n, (x, y) in enumerate([(12, 4), (16, 6), (21, 2), (25, 1), (18, 1),
                            (13, 7), (27, 3)]):
    m["objects"].append({
        "id": f"starglint_{n}", "sprite": rng.choice(
            ["windward_starglint_a", "windward_starglint_b"]),
        "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})

# ---- signs --------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="sunvault_helia", at=(2, 6))
owed += pt.sign(m, deco, W, sid="sunvault_observatory", at=(21, 3))

# ---- the vine-tender (hooks verbatim: near the bloomed bridge) ----------------------
m["npcs"].append({
    "id": "vine_tender", "at": {"tx": 9, "ty": 21}, "facing": "down",
    "sprite": "npc_old_woman", "movement": "static",
    "dialogue_ref": "npc.sunvault_vine_tender"})
owed += ["npc.sunvault_vine_tender (hooks verbatim: 'Forty years shut, and "
         "your little pocket of daylight woke them like they'd only dozed...')"]

# ---- trainer beat (posted at the mid road's head, facing down her column) ----------
owed += pt.trainer_beat(m, tid="sunvault_skywatcher", at=(10, 13), facing="down",
                        sight=4, sprite="npc_man")

# ---- caches -------------------------------------------------------------------------
owed += pt.cache(m, cid="striker", at=(26, 3))           # THE VIGIL STRIKER (NE
                                                         # pocket; Nightreach lamp 1)
owed += pt.cache(m, cid="sunvault_amber", at=(20, 3))    # Moth-amber, the vine shelf
owed += pt.cache(m, cid="sunvault_charge", at=(24, 23))  # a charge, south garden

# ---- encounters (band 47-48; the kindled roster leads, Lunar bleeds in) -------------
TABLE_SV2 = [
    {"kin_id": 115, "weight": 18, "min_level": 47, "max_level": 48},  # Solvyne
    {"kin_id": 118, "weight": 16, "min_level": 47, "max_level": 48},  # Helicore
    {"kin_id": 120, "weight": 12, "min_level": 47, "max_level": 48},  # Dawnfawn
    {"kin_id": 117, "weight": 10, "min_level": 47, "max_level": 48},  # Helibud
    {"kin_id": 104, "weight": 10, "min_level": 47, "max_level": 48},  # Goldmane
    {"kin_id": 126, "weight": 10, "min_level": 47, "max_level": 48},  # Lunveil
    {"kin_id": 116, "weight": 8, "min_level": 47, "max_level": 48},   # Auravane
    {"kin_id": 121, "weight": 6, "min_level": 47, "max_level": 48},   # Sunstag
    {"kin_id": 127, "weight": 4, "min_level": 48, "max_level": 48},   # Lunvane
]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if goldtuft[i]:
        (band_grid if (i // W) in (15, 16) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE_SV2, id_prefix="terrace")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE_SV2, id_prefix="crossing")

# ---- dressing -----------------------------------------------------------------------
m["objects"] += [
    {"id": "column_a", "sprite": "solarium_column", "at": {"tx": 14, "ty": 21},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_b", "sprite": "solarium_column", "at": {"tx": 19, "ty": 8},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_fallen_a", "sprite": "solarium_column_fallen",
     "at": {"tx": 3, "ty": 17}, "w": 3, "h": 1},
    {"id": "column_fallen_b", "sprite": "solarium_column_fallen",
     "at": {"tx": 25, "ty": 22}, "w": 3, "h": 1},
    {"id": "lamp_entry", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 4, "ty": 24}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_mid", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 12, "ty": 16}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_north", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 21, "ty": 6}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # THE VINE-SHADE REST TERRACE (W8 MIN-2): a living arbor — two ruin
    # columns carrying a bloomed sun-vine over the jog's mouth — and the
    # fallen column it shades, a seat at the climb's halfway breath.
    {"id": "rest_arbor_col_w", "sprite": "solarium_column",
     "at": {"tx": 13, "ty": 14}, "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "rest_arbor_col_e", "sprite": "solarium_column",
     "at": {"tx": 16, "ty": 14}, "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "rest_arbor_vine", "sprite": "sunvault_vine_h_bloomed",
     "at": {"tx": 14, "ty": 14}, "w": 3, "h": 1, "solid": False},
    {"id": "rest_seat", "sprite": "solarium_column_fallen",
     "at": {"tx": 13, "ty": 18}, "w": 3, "h": 1},
]
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (cliff, ruin, goldtuft))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
blooms = [gid("flowerbed_a"), gid("flowerbed_b")]
for y in range(H):
    for x in range(W):
        i = y * W + x
        if base[i] in gg and deco[i] == 0 and (x, y) not in avoid \
                and rng.random() < 0.12:
            deco[i] = rng.choice(blooms) if rng.random() < 0.5 else gid("boulder")
for (x, y) in [(3, 10), (27, 18), (15, 25), (8, 5), (27, 25)]:
    if (x, y) not in avoid and deco[y * W + x] == 0:
        deco[y * W + x] = gid("boulder")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
