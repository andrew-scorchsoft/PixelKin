#!/usr/bin/env python3
"""
Hushfrost Pass II — the coldfog throat (walkthrough/04-west "Hushfrost Pass
I→II" beat 3-4; kind route, region west, band 40-42, the colder half).

Past the Emberward burn the route runs through thinning fog: the first numbed
ex-Ember kin appear near the mist, and the far mouth glows faintly gold —
the Sunken Solarium's stored daylight, sight-lined as the destination
(§3a r3). Three signature touches (§8):
  1. THE CARETAKER'S SHELTER (X1 quest anchor, the B-arc's quietest beat):
     a stone shelter south of the low road where the caretaker sits with a
     numbed, sleeping kin the coldfog touched — a HEARTHKIT gone grey (the
     species whose dex entry IS her line: "it used to glow like a hearth").
     Zero humour anywhere near it; the beat is sacred.
  2. THE FIRST COLDFOG FINGERS — two small blight pockets at the eastern
     edges where the fog gnaws the snow (SPARING: full blight belongs to
     Coldfog Marches; here it's foreshadow). The numbed roster beds there.
  3. THE GOLD MOUTH — a dusting of sun-warmed grass around the west exit,
     the first warm colour in many screens, pulling the player on.

HANDSHAKE (W1-internal, built both sides): pass_i `to_pass_ii` warps at
(0,14)/(0,15) land HERE at (28,19)/(28,20); our return pair `to_pass_i` at
(29,19)/(29,20) lands pass_i (1,14)/(1,15) — both directions Emberward-gated
(the fog is the boundary; graph.ts `to_pass_ii` bidirectional).
HANDSHAKE (W2, binding on the Solarium builder): our `to_solarium` warps at
(0,8)/(0,9) land at sunken_solarium (30,8)/(30,9) — placeholder until W2
authors it (the engine no-ops). W2's map must keep those landings WALKABLE
(width ≥31, entry on its EAST edge) and its return pair must land at our
(1,8)/(1,9). Mirror of the N3→W1 contract.
SPUR (graph.ts verbatim): `to_aurora` at the north grotto mouth (14,2)/(15,2),
requires_ability emberward (held — the §3 "now accessible" callout sign sits
beside it), landing aurora_hollow (9,13)/(10,13); the hollow's return pair
lands at our (14,3)/(15,3).

X1 "The Caretaker's Lamp" (spine §5 kit; flags verbatim from the hooks):
  ask    script.caretaker_quest -> sets flag:q_west_caretaker
  wait   npc.numbed_kin_caretaker (the walkthrough's hook ref — her line)
  done   script.caretaker_done (requires flag:picked_aurora_oil, the cache
         in Aurora Hollow) -> gives the Bright Lamp + sets
         flag:q_west_caretaker_done. NOTE for the wiring agent: the item id
         must NOT be `bright_lamp` (SaveCodec migrates that legacy id to
         glow_charge) — use e.g. `caretaker_lamp`, display name "Bright Lamp".
  after  npc.caretaker_after (the kin sleeps EASIER, not awake — B-arc weight)
  Her lamp by the kin is the pale_vault bracket flag-swap pair: dark until
  q_west_caretaker_done, lit after (same footprint+solidity).

THE POSTGAME SWAP (06-postgame cross-ref — a pure data flip on flag:dawn):
  object numbed_kin       (hushfrost_numbed_kin, the grey drained Hearthkit)
         hidden_when_flag: flag:dawn
  object numbed_kin_awake (hushfrost_numbed_kin_awake, the original warm art)
         requires_flag:    flag:dawn
  Same 2x2 footprint, same solidity (collision is flag-blind). The interact
  triggers on its front row swap the same way: npc.numbed_kin_sleeping <->
  npc.numbed_kin_awake. Nothing else is needed: when 06-postgame sets
  flag:dawn the kin wakes, already in place.

Trainer beat (progression.mjs leg, route class — wiring agent authors):
  hushfrost_thawtender "Thaw-tender", 2 kin lv42 — sweeping fog-rime off the
  gold mouth's lane, the first warm soul since the glacier. payout 672.

Encounter picks (real species mapped per the hooks; band 40-42):
  numbed ex-Ember (Frost/Dark read) -> #85 Stillwarden (the canon Frost/Dark
    silence-burrower — "where it rests, no sound exists") + #141 Cindersob
    (Dark/Ember, "the hollowed remnant of a once-warm hearth companion" —
    the literal numbed ex-Ember, foreshadowing the Coldfog roster) in the
    BLIGHT pockets only, low weight.
  + the pass roster walking west: #84 Hushbore, #78 Crystarn, and NEWLY
    PLACED kindled forms #96 Frigalance (Glacewing's apex) and #79 Glacitern
    (Crystarn's apex) at rare weight — the colder half runs older kin.
  Mirror into EXTRA_ENCOUNTERS (tools/balance/build_species.py) = wiring agent.

Suggested sign copy (wiring agent; ZERO humour on this map — the caretaker
beat owns the register):
  sign.hushfrost_aurora  "AURORA HOLLOW. The lights pool under the ice here.
                          A warded flame may walk in and look up." (the §3
                          'now accessible (Emberward, held)' callout; also
                          the spur warps' blocked_ref)
  sign.hushfrost_gold    "WEST — THE SUNKEN SOLARIUM. That gold on the fog
                          is stored daylight. Walk toward the warmth."

audit_flow notes — the spur pocket and shelter pocket are paid dead ends by
design (§3a r4: the grotto mouth + X1; the caches). The blight fingers bed
the numbed roster (encounter payoff).

Run:  ./venv/bin/python tools/maps/build_hushfrost_pass_ii.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 28
rng = random.Random(75)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
glacier = mk.make_grid(W, H)    # canyon walls + the central wall band
blight = mk.make_grid(W, H)     # the coldfog-touched ground (SPARING)
blighttuft = mk.make_grid(W, H) # the numbed encounter beds (inside blight)
goldgrass = mk.make_grid(W, H)  # the gold mouth dusting (west exit)
snowtrail = mk.make_grid(W, H)  # the trodden lane
frosttuft = mk.make_grid(W, H)  # the mandatory crossing + pockets
deco = mk.make_grid(W, H)

# BORDERS: glacier crag all round, 2 deep, organic bumps (§11 r2)
mk.rect(glacier, W, H, 0, 0, W - 1, 1)
mk.rect(glacier, W, H, 0, 26, W - 1, H - 1)
mk.rect(glacier, W, H, 0, 0, 1, H - 1)
mk.rect(glacier, W, H, 28, 0, 29, H - 1)
mk.organic_border(glacier, W, H, depth=0,
                  bumps=[(6, 1, 2), (22, 1, 2), (1, 5, 2), (28, 12, 2),
                         (9, 26, 2), (24, 27, 2), (1, 23, 2)],
                  rng=rng)
# EAST gap — the boundary with pass_i (rows 19-20)
for x in (28, 29):
    for y in (19, 20):
        glacier[y * W + x] = 0
# WEST gap — the gold mouth to the Solarium (rows 8-9)
for x in (0, 1):
    for y in (8, 9):
        glacier[y * W + x] = 0
# NORTH gap — the Aurora Hollow grotto mouth (cols 14-15 through the crag)
for y in (2,):
    glacier[y * W + 14] = 0
    glacier[y * W + 15] = 0

# THE CENTRAL WALL BAND: the canyon pinches the map into a low road (south)
# and a high road (north), joined ONLY by the west link — the §3a fold
mk.rect(glacier, W, H, 7, 11, 29, 17)
# organic bumps off the band so its edges never run ruled (§11 r2/r4)
mk.blob(glacier, W, H, 10.0, 10.5, 1.8, 1.2)
mk.blob(glacier, W, H, 19.0, 17.5, 1.8, 1.2)
mk.blob(glacier, W, H, 14.0, 11.0, 1.6, 1.1)
# THE EAST SHELF (§3a r1/r2 — the one-way return): coming back from the gold
# mouth, drop off the high road down a snow shelf to the low road by the fog
# boundary, skipping the link + the crossing the outbound trip earned
for y in range(11, 18):
    for x in (24, 25, 26):
        glacier[y * W + x] = 0
# the spur pocket (north, off the high road) is carved INTO the crag
for y in range(3, 8):
    for x in range(12, 18):
        glacier[y * W + x] = 0
# the shelter pocket hangs south of the low road
for y in range(22, 25):
    for x in range(11, 21):
        glacier[y * W + x] = 0

# ---- lanes (snowtrail on snow) -----------------------------------------------------
mk.hline(snowtrail, W, H, 19, 4, 27)                # the low road (entry, fog-side)
mk.hline(snowtrail, W, H, 20, 4, 27)
mk.vline(snowtrail, W, H, 4, 10, 19)                # the west link (south->north)
mk.vline(snowtrail, W, H, 5, 10, 19)
mk.hline(snowtrail, W, H, 8, 1, 22)                 # the high road (to the gold mouth)
mk.hline(snowtrail, W, H, 9, 1, 22)
mk.vline(snowtrail, W, H, 14, 3, 8)                 # the grotto approach
mk.vline(snowtrail, W, H, 15, 3, 8)
# jogs so the long roads never run ruled (the glacier forecourt trick)
mk.rect(snowtrail, W, H, 10, 18, 12, 18)
mk.rect(snowtrail, W, H, 17, 21, 19, 21)
mk.rect(snowtrail, W, H, 8, 10, 10, 10)
mk.rect(snowtrail, W, H, 18, 7, 20, 7)

# ---- the coldfog fingers (blight — SPARING; the first cold fingers only) -----------
mk.blob(blight, W, H, 25.0, 22.5, 2.8, 1.8)         # SE finger, by the fog boundary
mk.blob(blight, W, H, 25.5, 9.0, 2.6, 1.4)          # NE finger, high-road dead end
# numbed beds inside them (blighttuft = the encounter tile)
mk.blob(blighttuft, W, H, 25.0, 22.5, 1.8, 1.1)
mk.blob(blighttuft, W, H, 25.5, 9.0, 1.6, 0.9)

# ---- the gold mouth (the Solarium sight-line — warmth at the far exit) -------------
mk.blob(goldgrass, W, H, 1.5, 8.5, 2.6, 2.2)
mk.blob(goldgrass, W, H, 3.0, 10.0, 1.6, 1.2)

# ---- encounter terrain -------------------------------------------------------------
mk.blob(frosttuft, W, H, 9.0, 20.0, 2.4, 1.4)       # low-road pocket (optional)
mk.blob(frosttuft, W, H, 13.5, 5.0, 1.8, 1.2)       # spur-pocket bed (optional)
# the MANDATORY crossing on the west link (§11 r7): wall to wall
pt.mandatory_band(frosttuft, snowtrail, W, H, y0=13, y1=14, x0=2, x1=6)

# the east shelf's one-way lip (snow register; hop down to the low road)
pt.ledge_run(deco, W, H, 17, 24, 26, rng, family="snow")

# ---- precedence --------------------------------------------------------------------
for i in range(W * H):
    if glacier[i]:
        for g in (blight, blighttuft, goldgrass, snowtrail, frosttuft):
            g[i] = 0
    if snowtrail[i]:
        blighttuft[i] = 0
        frosttuft[i] = 0
        # the lane stays trodden through the gold dusting and the fog ground
        blight[i] = 0
        goldgrass[i] = 0
    if blighttuft[i]:
        frosttuft[i] = 0
    if blight[i] or goldgrass[i]:
        frosttuft[i] = 0

# ---- base: bone snow, with the blight fingers + the gold mouth painted IN ----------
# (blight0-3 and goldgrass0-3 are BASE ground families like snow0-3, not
# autotile terrains — they paint into the base layer directly)
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = mk.make_grid(W, H)
for i in range(W * H):
    if blight[i]:
        base[i] = rng.choice(bl) if rng.random() < 0.55 else bl[0]
    elif goldgrass[i]:
        base[i] = rng.choice(gg) if rng.random() < 0.55 else gg[0]
    else:
        base[i] = rng.choice(sn) if rng.random() < 0.5 else sn[0]

terrain_layers = [
    {"name": "t_snowtrail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": snowtrail},
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": blighttuft},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
]

m: dict = {
    "id": "hushfrost_pass_ii", "display_name": "Hushfrost Pass",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/hushfrost-pass-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/hushfrost-pass-a.webp",
        "assets/backgrounds/battle/hushfrost-pass-b.webp",
    ],
}

# ---- warps (graph.ts edge ids verbatim) --------------------------------------------
m["warps"] += [
    # EAST <-> hushfrost_pass_i (both directions burn the fog: emberward)
    {"id": "to_pass_i", "at": {"tx": 29, "ty": 19}, "trigger": "step_on",
     "to_map": "hushfrost_pass_i", "to": {"tx": 1, "ty": 14}, "facing": "right",
     "requires_ability": "emberward",
     "blocked_ref": "sign.hushfrost_coldfog", "transition": "fade"},
    {"id": "to_pass_i_s", "at": {"tx": 29, "ty": 20}, "trigger": "step_on",
     "to_map": "hushfrost_pass_i", "to": {"tx": 1, "ty": 15}, "facing": "right",
     "requires_ability": "emberward",
     "blocked_ref": "sign.hushfrost_coldfog", "transition": "fade"},
    # WEST -> sunken_solarium (`to_solarium`, UNGATED — W2 authors the far
    # side; landing is a placeholder the engine no-ops until then; W2's
    # return pair must land at our (1,8)/(1,9))
    {"id": "to_solarium", "at": {"tx": 0, "ty": 8}, "trigger": "step_on",
     "to_map": "sunken_solarium", "to": {"tx": 30, "ty": 8}, "facing": "left",
     "transition": "fade"},
    {"id": "to_solarium_s", "at": {"tx": 0, "ty": 9}, "trigger": "step_on",
     "to_map": "sunken_solarium", "to": {"tx": 30, "ty": 9}, "facing": "left",
     "transition": "fade"},
    # NORTH — the Aurora Hollow grotto mouth (`to_aurora`, Emberward — held;
    # the [MISSABLE] spur opens the moment you reach the fog)
    {"id": "to_aurora", "at": {"tx": 14, "ty": 2}, "trigger": "step_on",
     "to_map": "aurora_hollow", "to": {"tx": 9, "ty": 13}, "facing": "up",
     "requires_ability": "emberward",
     "blocked_ref": "sign.hushfrost_aurora", "transition": "door"},
    {"id": "to_aurora_e", "at": {"tx": 15, "ty": 2}, "trigger": "step_on",
     "to_map": "aurora_hollow", "to": {"tx": 10, "ty": 13}, "facing": "up",
     "requires_ability": "emberward",
     "blocked_ref": "sign.hushfrost_aurora", "transition": "door"},
]

# ---- THE CARETAKER'S SHELTER (X1 — see module docstring) ---------------------------
m["objects"] += [
    # the shelter hut (bespoke hushfrost object; solid, roof overhang)
    {"id": "caretaker_shelter", "sprite": "hushfrost_shelter",
     "at": {"tx": 11, "ty": 20}, "w": 4, "h": 4, "overhang": 2},
    # the numbed sleeping kin <-> the awake kin (THE POSTGAME FLAG FLIP —
    # same footprint, same solidity; flag:dawn is set by 06-postgame). The
    # flag-gated state is listed FIRST so QA renders (flag-blind) show the
    # default pre-dawn state on top; the engine filters by flags either way.
    {"id": "numbed_kin_awake", "sprite": "hushfrost_numbed_kin_awake",
     "at": {"tx": 17, "ty": 22}, "w": 2, "h": 2,
     "requires_flag": "flag:dawn"},
    {"id": "numbed_kin", "sprite": "hushfrost_numbed_kin",
     "at": {"tx": 17, "ty": 22}, "w": 2, "h": 2,
     "hidden_when_flag": "flag:dawn"},
    # her lamp by the kin: dark until the aurora-oil fills it (X1's payoff)
    {"id": "caretaker_lamp_lit", "sprite": "pale_vault_bracket_lit",
     "at": {"tx": 20, "ty": 21}, "w": 1, "h": 2, "overhang": 1,
     "walk_under": True, "requires_flag": "flag:q_west_caretaker_done"},
    {"id": "caretaker_lamp_dark", "sprite": "pale_vault_bracket_dark",
     "at": {"tx": 20, "ty": 21}, "w": 1, "h": 2, "overhang": 1,
     "walk_under": True, "hidden_when_flag": "flag:q_west_caretaker_done"},
]
# the kin's voice — interact triggers on its front row, swapped on flag:dawn
for i, tx in enumerate((17, 18)):
    m["triggers"] += [
        {"id": f"numbed_kin_sleeping_{i}", "kind": "dialogue",
         "at": {"tx": tx, "ty": 23}, "activation": "interact",
         "ref": "npc.numbed_kin_sleeping", "hidden_when_flag": "flag:dawn"},
        {"id": f"numbed_kin_awake_{i}", "kind": "dialogue",
         "at": {"tx": tx, "ty": 23}, "activation": "interact",
         "ref": "npc.numbed_kin_awake", "requires_flag": "flag:dawn"},
    ]
# the caretaker: ask -> waiting -> done -> after (the kite-maker flag-pair
# pattern; she never leaves the kin's side)
m["npcs"] += [
    {"id": "caretaker_quest", "at": {"tx": 16, "ty": 23}, "facing": "right",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "script.caretaker_quest",
     "hidden_when_flag": "flag:q_west_caretaker"},
    {"id": "caretaker_waiting", "at": {"tx": 16, "ty": 23}, "facing": "right",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "npc.numbed_kin_caretaker",
     "requires_flag": "flag:q_west_caretaker",
     "hidden_when_flag": "flag:picked_aurora_oil"},
    {"id": "caretaker_done", "at": {"tx": 16, "ty": 23}, "facing": "right",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "script.caretaker_done",
     "requires_flag": "flag:picked_aurora_oil",
     "hidden_when_flag": "flag:q_west_caretaker_done"},
    {"id": "caretaker_after", "at": {"tx": 16, "ty": 23}, "facing": "right",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "npc.caretaker_after",
     "requires_flag": "flag:q_west_caretaker_done"},
]
owed += ["script.caretaker_quest (X1 giver; sets flag:q_west_caretaker — "
         "grief register, zero humour)",
         "npc.numbed_kin_caretaker (the hook ref VERBATIM: 'It used to glow "
         "like a hearth. Now it just sleeps...')",
         "script.caretaker_done (requires flag:picked_aurora_oil; gives the "
         "Bright Lamp — item id `caretaker_lamp`, NOT `bright_lamp` (SaveCodec "
         "rename collision); sets flag:q_west_caretaker_done; the kin sleeps "
         "EASIER, not awake)",
         "npc.caretaker_after",
         "npc.numbed_kin_sleeping (a grey Hearthkit; no sound comes from it)",
         "npc.numbed_kin_awake (POSTGAME, flag:dawn — the quietest B-arc echo)"]

# ---- other objects: lamps, the grotto dressing, throat spires ----------------------
m["objects"] += [
    {"id": "lamp_low_road", "sprite": "tinderwick_lamp_post", "at": {"tx": 22, "ty": 17},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_link", "sprite": "tinderwick_lamp_post", "at": {"tx": 2, "ty": 16},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_gold", "sprite": "tinderwick_lamp_post", "at": {"tx": 5, "ty": 5},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # aurora light spilling from the grotto mouth (the drawn veil decal)
    {"id": "aurora_spill", "sprite": "hushfrost_aurora_veil", "at": {"tx": 13, "ty": 0},
     "w": 3, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
    {"id": "spires_mouth", "sprite": "pale_vault_ice_spire", "at": {"tx": 16, "ty": 1},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "spires_fog", "sprite": "pale_vault_ice_spire", "at": {"tx": 26, "ty": 17},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- signs (ZERO humour on this map) -----------------------------------------------
owed += pt.sign(m, deco, W, sid="hushfrost_aurora", at=(16, 4))
owed += pt.sign(m, deco, W, sid="hushfrost_gold", at=(3, 7))

# ---- trainer beat ------------------------------------------------------------------
owed += pt.trainer_beat(m, tid="hushfrost_thawtender", at=(8, 8), facing="right",
                        sight=4, sprite="npc_woman")

# ---- caches (variety: consumable in the spur pocket, valuable behind blight) -------
owed += pt.cache(m, cid="hushfrost_warm_balm", at=(12, 4))   # consumable, spur pocket
owed += pt.cache(m, cid="hushfrost_amber", at=(26, 8))       # Moth-amber, NE blight
                                                             # finger (off-lane payoff)

# ---- encounters --------------------------------------------------------------------
# the pass roster, colder half: older kin, two NEWLY PLACED kindled apexes
TABLE = [{"kin_id": 84, "weight": 24, "min_level": 40, "max_level": 42},
         {"kin_id": 78, "weight": 20, "min_level": 41, "max_level": 42},
         {"kin_id": 81, "weight": 14, "min_level": 40, "max_level": 42},
         {"kin_id": 86, "weight": 12, "min_level": 40, "max_level": 42},
         {"kin_id": 96, "weight": 9, "min_level": 41, "max_level": 42},
         {"kin_id": 79, "weight": 9, "min_level": 41, "max_level": 42},
         {"kin_id": 85, "weight": 12, "min_level": 41, "max_level": 42}]
# the numbed beds (blighttuft): the Hollowing-touched roster, foreshadow only
TABLE_NUMBED = [{"kin_id": 85, "weight": 45, "min_level": 41, "max_level": 42},
                {"kin_id": 141, "weight": 30, "min_level": 40, "max_level": 42},
                {"kin_id": 84, "weight": 25, "min_level": 40, "max_level": 42}]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if frosttuft[i]:
        (band_grid if (i // W) in (13, 14) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE, id_prefix="pocket")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE, id_prefix="crossing")
m["encounters"] += pt.zones_from_grid(blighttuft, W, H, terrain="tall_grass",
                                      rate=0.12, table=TABLE_NUMBED,
                                      id_prefix="numbed")

# ---- fog dressing: grey moss creeping along the blight rims ------------------------
for (x, y, n) in [(22, 21, "greymoss_a"), (27, 21, "greymoss_b"), (23, 24, "greymoss_a"),
                  (23, 8, "greymoss_b"), (27, 10, "greymoss_a"), (26, 19, "greymoss_b")]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid(n)

# ---- scatter + boulders ------------------------------------------------------------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (glacier, blight, blighttuft, goldgrass,
                                         snowtrail, frosttuft))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
mk.scatter_decor(deco, base, W, H, rng, density=0.15, avoid=avoid)
for (x, y) in [(7, 5), (20, 4), (24, 3), (8, 22), (22, 24), (3, 21),
               (10, 10), (19, 6), (6, 18)]:
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
