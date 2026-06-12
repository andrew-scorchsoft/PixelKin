#!/usr/bin/env python3
"""
Nightreach Observatory — the hilltop star-temple town (walkthrough/04-west
"Nightreach Observatory"; Lumenary 8: Nessa Cole — her bond-test waits under
the great eyepiece INSIDE the hall, at the end of the Vigil of the Seven).

Arc D: the densest `diamond` starfield in the game — bone + deepBlue,
telescope brass, near-dawn pallor on the north horizon (the dome wears the
sky; star-glint clusters thicken toward the north rim). The most "sky-forward"
town; the register is reverent, vast, lonely, wondrous — ZERO humour anywhere
near the vigil, the lamps or Nessa (the cluster's ONE dry line lives with the
inn guest, see build_nightreach_interiors.py).

Three signature touches (§8):
  1. THE ASTRAL WALK — seven watch-lamps in a deliberate horseshoe arc up the
     temple terrace (the spine §5 shape-#8 earned loop: ceremony walk, the
     capstone). Dark/lit MapObject swap pairs (the Pale Vault undercroft
     lamp-line pattern at grander scale — 2x3 bespoke watch-lamps), each lamp
     an interact script chained on the previous flag (flag:q_west_lamp_1..7);
     the sky above is lit, the lamps below are not, and the walk closes that
     distance one remembrance at a time.
  2. THE DOME — the image-gen hero observatory (6x8) at the terrace head,
     axial with the south entry (§3a r3: seen from the rim gate the moment
     you arrive). Its eyepiece chancel is the interior; the eighth watch-lamp
     stands beside it indoors and lights itself on gleam:lunar.
  3. THE STAR-VIGIL STEPS — the festival glimmering across the temple steps:
     star banners, small lit vigil lamps, watchers standing silent under
     seven relit constellations, waiting for the eighth.

§0 TRAP (binding): the town and the Lumenary carry NO ability gate of any
kind — the rim approach (south, from Sunvault II) is UNGATED, the hall door
is starter-gated like every Lumenary. Emberward gates only the OPTIONAL
Coldfog back-door on the east edge (spine §0 rule 2: the fog road is the
wrong way in, the rim is the main path).

THE VIGIL OF THE SEVEN (hooks verbatim):
  script.nessa_quest (interior, the eyepiece) -> flag:q_west_vigil;
  the striker cache on sunvault_climb_ii (flag:picked_striker, BUILT by W2)
  unlocks lamp 1; lamp scripts chain flag:q_west_lamp_1..7 (each requires the
  previous lamp; out-of-order lamps answer with npc.watch_lamp_cold, lamp 1
  with npc.watch_lamp_unstruck — the striker ask); lamps 5/6/7 carry the
  C4/A5/B4 cluster:
    LAMP 5 (Frost)  — C4 Fenn's counsel  (script.fenn_counsel; Fenn waits
                      there, flag-staggered, and stays after — he does not
                      march with you, he sends you up clear-eyed).
    LAMP 6 (Storm)  — A5 Wren resolved   (script.wren_nightreach; optional
                      friendly battle vs TRAINERS['wren_nightreach']; the
                      script mentions the ribbon IF flag:q_north_ribbon_placed
                      — N3's payoff, a conditional line, wiring agent).
    LAMP 7 (Solar)  — B4 the Great Null named (script.great_null_named at the
                      great telescope; Nessa stands there once lamp 6 is lit).
                      The trigger sets flag:q_west_lamp_7 +
                      flag:q_west_vigil_kept + flag:great_null_known (+
                      flag:q_west_vigil, so the chain is closed even for a
                      player who never took the hook — no double-Nessa state).
  Nessa's bond-test (interior) requires flag:q_west_vigil_kept, blocked_ref
  npc.nessa_not_ready. Win -> reward_flags ['gleam:lunar'] +
  reward_abilities ['starreach']; the ENGINE derives flag:crown_west and
  (last quadrant) flag:hub_unlocked — never hand-set.

DOCUMENTED DEVIATION (schema: one requires_flag per trigger): the hooks ask
each lamp to require its gleam:* AND the previous lamp; the chain flag is the
one encoded (the ember->solar order is the chain itself, and on the main path
every gleam is necessarily held — this is the eighth town). The one reachable
edge case is a fog-road sequence-breaker without gleam:solar lighting lamp 7
early; harmless to progression (crown_west still waits on both Gleams in the
engine), and the wiring agent may open script.great_null_named with a
conditional guard if cutscene conditionals land. Mirrors the Pale Vault
undercroft chain's encoding exactly.

X3 "CHARTING THE DARK" (giver here; W2/W3 contracts honoured):
  junior_watcher_a's beaten swap IS the giver (the hooks' "post-walk, her
  swap NPC"): script.chart_quest -> flag:q_west_chart; Sunvault II's terrace
  viewpoint (BUILT) requires it -> _1; OUR roof-terrace viewpoint
  (script.chart_observatory, the NE terrace rim) requires _1 -> _2; her done
  stage requires _2 ONLY (script.chart_done — the finished chart NAMES
  STARWELL, the Penumbra tease-closer) -> q_west_chart_done. Coldfog's cairn
  leg (_3, BUILT) stays OPTIONAL — never required, per W3's contract.
R5 "A CHART FOR THE WAYKEEPER" (the Round, leg 5 — wakes with the spoke):
  post-chart she entrusts a fresh star-chart (script.round_chart_take ->
  flag:q_round_chart_taken); THE DELIVERY SIDE IS THE CROSSROADS WAYKEEPER —
  wiring note: the Waykeeper needs a flag-staggered pair (take ->
  script.round_chart_deliver sets flag:q_round_chart; he hangs it on the
  Waystone) — NOT built here (the crossroads edit in this change is the
  nightreach spoke ONLY).

HANDSHAKES (all three contracts verbatim):
  (a) W2 sunvault_climb_ii `to_observatory` lands at OUR (15,28)/(16,28) —
      south-edge entry, walkable; our return pair `to_climb_ii`/`_e` at
      (15,29)/(16,29) lands sunvault (22,1)/(23,1). UNGATED both ways.
  (b) W3 coldfog_marches_ii `to_observatory_fog` lands at OUR (28,14)/(28,15)
      facing left — east edge, map 30 wide; our return pair `to_coldfog`/`_s`
      at (29,14)/(29,15) lands coldfog (1,3)/(1,4), requires_ability emberward
      (gated OUR side too, per the contract), blocked_ref
      sign.nightreach_fogroad. A blight fringe stains the gate mouth (Arc D:
      the fog road is drained ground; it does not brighten).
  (c) Lanternway spoke `to_crossroads`/`_s` at (4,29)/(5,29) lands
      vesper_crossroads (3,1)/(4,1) — the crossroads' new NW-corner spoke
      (its side gleam:lunar-gated per the Galehigh pattern; see
      build_crossroads.py). Crossroads' `to_nightreach`/`_e` land at OUR
      (4,28)/(5,28).

Encounter picks (band 48-52, approach grass ONLY — none in town; continuous
with Sunvault II 47-48; the walkthrough's Astrowl/Dreamoth/Tessel are atlas
flavour names with no species rows — the N1 Kiteling / Pale Vault precedent,
documented): #105 Snoozlet + #111 Spirlet (the A-stage Lunar beds — both dex
entries NAME Nightreach), #106 Drowshorn + #112 Nightwraith (their stage-2
forms, WEIGHTED UP per the brief), #126 Lunveil + #127 Lunvane (the W2 bridge
pair, continuous with Sunvault), #124 Petalune ("flits between the telescope
domes"), and THE RARE: #129 Dawnwatcher (Lunar/Light E — its dex entry says
the observatory was BUILT to watch for it; the spur-spike precedent, weight 3,
lv 51-52). #132 Lunaveil (E, also names the dome) is deliberately LEFT
UNPLACED — its entry has Nessa still tracking it; it reads as a post-dawn /
Central-writer payoff, not a town wild.

Trainer beats (keeper class, 20 x ace — defs land with the wiring agent):
  junior_watcher_a "Junior Watcher Lira", lv 49-50, ace 50, payout 1000 (the
    X3 giver after she's beaten); junior_watcher_b "Junior Watcher Os", lv
    50-51, ace 51, payout 1020. Wren (A5, optional friendly): rival class,
    ~2 under the player (~50), ace 50, payout 1200. Nessa: warden, ace 52,
    payout 3120. Mirror all four into BUILT_PAYOUTS (progression.mjs).

Suggested sign copy (wiring agent; sincere, reverent, zero humour):
  sign.nightreach_welcome    "NIGHTREACH OBSERVATORY. The sky is closest
                              here. Walk softly — the watchers are counting."
  sign.nightreach_walk       "THE ASTRAL WALK. Seven watch-lamps for seven
                              stars. Lit in the order they came home:
                              ember-light first, sun-light last."
  sign.nightreach_fogroad    "EAST — THE FOG ROAD. Short, dark, and wrong.
                              Only a warded flame holds the coldfog off."
  sign.nightreach_lanternway "SOUTH — THE LANTERNWAY. Every lit road in
                              Vesperholm meets at the Waystone."
  npc.watch_lamp_unstruck    "The first watch-lamp waits, polished and cold.
                              Its wick wants the old watcher's striker — the
                              one lost on the Sunvault road."
  npc.watch_lamp_cold        "This lamp keeps its place in the order. An
                              earlier watch-fire is still dark."

audit_flow notes — the NE roof-terrace pocket (X3 viewpoint + shard cache)
and the east fog pocket are paid dead ends (§3a r4); the terrace's east scree
ledge is the one-way hop home past the walk (§3a r1/r2 — first pass climbs
the steps, the return is a hop). Town maps carry no loop requirement.

Run:  ./venv/bin/python tools/maps/build_nightreach.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 30
rng = random.Random(78)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
cliff = mk.make_grid(W, H)      # border crags + the terrace face
ruin = mk.make_grid(W, H)       # bone paving: terrace floor, steps, lanes
goldtuft = mk.make_grid(W, H)   # the approach encounter beds
deco = mk.make_grid(W, H)

# BORDERS: crag all round, 2 deep, organic bumps (§11 r2) — bumps avoid the
# dome cols (13-18) and every gap
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.rect(cliff, W, H, 0, 28, W - 1, H - 1)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)
mk.rect(cliff, W, H, 28, 0, 29, H - 1)
mk.organic_border(cliff, W, H, depth=0,
                  bumps=[(6, 1, 2), (24, 1, 2), (1, 6, 2), (28, 8, 2),
                         (1, 22, 2), (28, 24, 2), (10, 28, 2), (24, 28, 2)],
                  rng=rng)
# SOUTH gap A — the Sunvault rim approach (cols 15-16; W2 lands (15,28)/(16,28))
for y in (28, 29):
    for x in (15, 16):
        cliff[y * W + x] = 0
# SOUTH gap B — the Lanternway spoke (cols 4-5)
for y in (28, 29):
    for x in (4, 5):
        cliff[y * W + x] = 0
# EAST gap — the Coldfog back-door (rows 14-15; W3 lands (28,14)/(28,15))
for x in (28, 29):
    for y in (14, 15):
        cliff[y * W + x] = 0

# THE TEMPLE TERRACE: the town's elevation accent (§11 r3) — a raised bone
# platform across the north, its face the rows 12-13 crag band, pierced by
# the STEPS (cols 15-16, axial with the entry + the dome door) and the
# one-way SCREE LEDGE at cols 21-23 (the §3a r1/r2 return hop)
mk.rect(cliff, W, H, 2, 12, W - 3, 13)
for y in (12, 13):
    for x in (15, 16):
        cliff[y * W + x] = 0            # the steps
    for x in (21, 22, 23):
        cliff[y * W + x] = 0            # the ledge cut
pt.ledge_run(deco, W, H, 13, 21, 23, rng, family="scree")

# terrace floor: bone paving wall-to-wall behind the face (rows 2-11), the
# steps' throat (rows 12-13 at the gap), the ledge lip row 12
mk.rect(ruin, W, H, 2, 2, W - 3, 11)
mk.rect(ruin, W, H, 15, 12, 16, 13)
mk.rect(ruin, W, H, 21, 12, 23, 12)
# bite the paving's SW/SE corners so the slab never reads ruled (§11 r4)
for (bx, by) in [(2, 10), (3, 11), (27, 10), (27, 11), (2, 11), (26, 11)]:
    ruin[by * W + bx] = 0

# ---- the town lanes (bone paving on gold grass) -------------------------------------
mk.rect(ruin, W, H, 15, 14, 16, 27)     # the main lane: steps -> rim gate
mk.rect(ruin, W, H, 4, 20, 26, 21)      # the town street (inn west, home east)
mk.rect(ruin, W, H, 4, 22, 5, 27)       # the Lanternway leg (street -> spoke)
mk.rect(ruin, W, H, 17, 14, 27, 15)     # the east lane -> the fog gate
mk.rect(ruin, W, H, 12, 16, 15, 16)     # forecourt jog under the steps (west)
mk.rect(ruin, W, H, 16, 17, 19, 17)     # forecourt jog (east) — the steps
                                        # court never runs ruled

# ---- encounter terrain (approach ONLY — none in town/terrace) -----------------------
mk.blob(goldtuft, W, H, 8.5, 24.5, 3.2, 1.9)    # SW bed (optional, pays the spoke corner)
mk.blob(goldtuft, W, H, 23.0, 24.0, 3.0, 1.8)   # SE bed (optional; wicks cache)
mk.blob(goldtuft, W, H, 26.0, 18.0, 1.8, 1.4)   # east verge by the fog lane
# the MANDATORY crossing (§11 r7): rows 25-26 wall to wall, both lanes paused
pt.mandatory_band(goldtuft, ruin, W, H, y0=25, y1=26, x0=2, x1=27)

# ---- precedence (structure wins) ----------------------------------------------------
for i in range(W * H):
    if cliff[i]:
        ruin[i] = 0
        goldtuft[i] = 0
    if ruin[i]:
        goldtuft[i] = 0

# ---- base: gold grass (continuous with Sunvault) + the blight stain at the
# fog gate (Arc D: the fog road's mouth is drained ground and stays so) ---------------
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
for y in range(H):
    for x in range(W):
        if ((x - 28.0) / 3.4) ** 2 + ((y - 14.5) / 3.0) ** 2 <= 1.0:
            base[y * W + x] = rng.choice(bl)

terrain_layers = [
    {"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": ruin},
    {"name": "t_goldtuft", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": goldtuft},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

m: dict = {
    "id": "nightreach_observatory", "display_name": "Nightreach Observatory",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/nightreach-observatory-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/nightreach-observatory-a.webp",
        "assets/backgrounds/battle/nightreach-observatory-b.webp",
    ],
}

# ---- buildings ----------------------------------------------------------------------
# THE DOME (image-gen hero, 6x8) at the terrace head, axial with the entry
# (§3a r3). Starter-gated like every Lumenary — NEVER ability-gated (§0 r1).
pt.building(m, ruin, W, H, oid="lumenary", sprite="nightreach_lumenary",
            at=(13, 2), overhang=4, door_col=2,
            to_map="nightreach_lumenary", to=(8, 11))
m["warps"][-1].update({"id": "to_lumenary", "requires_flag": "flag:has_starter",
                       "blocked_ref": "door.locked_lumenary"})
m["warps"].append({"id": "to_lumenary_e", "at": {"tx": 16, "ty": 9},
                   "trigger": "step_on", "to_map": "nightreach_lumenary",
                   "to": {"tx": 8, "ty": 11}, "facing": "up",
                   "transition": "door", "requires_flag": "flag:has_starter",
                   "blocked_ref": "door.locked_lumenary"})
# the inn (rest point) on the west street, a watcher's home east — the
# Galehigh highland-stone masters are the register reuse (wind-braced stone
# on a high hilltop; the brief's bespoke list is dome/lamps/eyepiece/
# dressing — reuse everywhere else)
pt.building(m, ruin, W, H, oid="inn", sprite="galehigh_inn",
            at=(4, 15), overhang=2, door_col=2,
            to_map="nightreach_inn", to=(7, 10))
m["warps"][-1]["id"] = "to_inn"
pt.building(m, ruin, W, H, oid="home", sprite="galehigh_cottage",
            at=(22, 15), overhang=2, door_col=2,
            to_map="nightreach_home", to=(6, 8))
m["warps"][-1]["id"] = "to_home"

# ---- warps (graph.ts edge ids verbatim) ---------------------------------------------
m["warps"] += [
    # SOUTH A <-> sunvault_climb_ii (the MAIN-PATH rim, UNGATED; W2 contract)
    {"id": "to_climb_ii", "at": {"tx": 15, "ty": 29}, "trigger": "step_on",
     "to_map": "sunvault_climb_ii", "to": {"tx": 22, "ty": 1}, "facing": "down",
     "transition": "fade"},
    {"id": "to_climb_ii_e", "at": {"tx": 16, "ty": 29}, "trigger": "step_on",
     "to_map": "sunvault_climb_ii", "to": {"tx": 23, "ty": 1}, "facing": "down",
     "transition": "fade"},
    # SOUTH B <-> vesper_crossroads (`to_crossroads` — the Lanternway spoke;
    # the crossroads side is gleam:lunar-gated, the Galehigh pattern)
    {"id": "to_crossroads", "at": {"tx": 4, "ty": 29}, "trigger": "step_on",
     "to_map": "vesper_crossroads", "to": {"tx": 3, "ty": 1}, "facing": "down",
     "transition": "fade"},
    {"id": "to_crossroads_s", "at": {"tx": 5, "ty": 29}, "trigger": "step_on",
     "to_map": "vesper_crossroads", "to": {"tx": 4, "ty": 1}, "facing": "down",
     "transition": "fade"},
    # EAST <-> coldfog_marches_ii (`to_observatory_fog`'s return — Emberward
    # OUR side too, per the W3 contract; the OPTIONAL back-door)
    {"id": "to_coldfog", "at": {"tx": 29, "ty": 14}, "trigger": "step_on",
     "to_map": "coldfog_marches_ii", "to": {"tx": 1, "ty": 3}, "facing": "right",
     "requires_ability": "emberward",
     "blocked_ref": "sign.nightreach_fogroad", "transition": "fade"},
    {"id": "to_coldfog_s", "at": {"tx": 29, "ty": 15}, "trigger": "step_on",
     "to_map": "coldfog_marches_ii", "to": {"tx": 1, "ty": 4}, "facing": "right",
     "requires_ability": "emberward",
     "blocked_ref": "sign.nightreach_fogroad", "transition": "fade"},
]

# ---- THE ASTRAL WALK: seven watch-lamps in a horseshoe up the terrace ---------------
# (tx, ty) of each 2x3 lamp; the arc runs west foot -> west rise -> NW crown
# -> dome west shoulder -> dome east shoulder (FENN) -> NE court (WREN) ->
# the great telescope's threshold (NESSA names the Great Null).
LAMPS = [
    (8, 9),    # 1 — Ember   (west of the steps court; wants the striker)
    (4, 6),    # 2 — Tide    (west rise)
    (4, 2),    # 3 — Verdant (northwest crown)
    (10, 3),   # 4 — Stone   (the dome's west shoulder)
    (20, 3),   # 5 — Frost   — C4 FENN'S COUNSEL
    (24, 5),   # 6 — Storm   — A5 WREN RESOLVED (+ optional friendly battle)
    (20, 8),   # 7 — Solar   — B4 THE GREAT NULL NAMED (the telescope's side)
]
LAMP_REFS = {5: "script.fenn_counsel", 6: "script.wren_nightreach",
             7: "script.great_null_named"}
for n, (lx, ly) in enumerate(LAMPS, start=1):
    flag = f"flag:q_west_lamp_{n}"
    prev = "flag:picked_striker" if n == 1 else f"flag:q_west_lamp_{n - 1}"
    blocked = "npc.watch_lamp_unstruck" if n == 1 else "npc.watch_lamp_cold"
    ref = LAMP_REFS.get(n, f"script.west_lamp_{n}")
    sets = [flag]
    if n == 7:
        # the seventh lamp closes the vigil AND names the Great Null (B4);
        # it also sets the hook flag so the chain is self-closing (docstring)
        sets += ["flag:q_west_vigil_kept", "flag:great_null_known",
                 "flag:q_west_vigil"]
    m["objects"] += [
        {"id": f"watch_lamp_{n}_dark", "sprite": "nightreach_watch_lamp_dark",
         "at": {"tx": lx, "ty": ly}, "w": 2, "h": 3, "overhang": 2,
         "hidden_when_flag": flag},
        {"id": f"watch_lamp_{n}_lit", "sprite": "nightreach_watch_lamp_lit",
         "at": {"tx": lx, "ty": ly}, "w": 2, "h": 3, "overhang": 2,
         "requires_flag": flag},
    ]
    kind = "cutscene" if n in LAMP_REFS else "script"
    for col, suffix in ((lx, "a"), (lx + 1, "b")):
        m["triggers"].append({
            "id": f"light_lamp_{n}_{suffix}", "kind": kind,
            "at": {"tx": col, "ty": ly + 2}, "activation": "interact",
            "ref": ref, "once": True,
            "requires_flag": prev, "blocked_ref": blocked,
            "sets_flags": sets, "hidden_when_flag": flag})
owed += [f"script.west_lamp_{n} (lamp {n} of the Vigil — its constellation's "
         f"remembrance; sets flag:q_west_lamp_{n})" for n in (1, 2, 3, 4)]
owed += [
    "script.fenn_counsel (= cutscene.fenn_counsel; C4 at lamp 5 — the Keystar "
    "must be OUT-REMEMBERED, not destroyed; portrait + quiet, no swell; sets "
    "flag:q_west_lamp_5)",
    "script.wren_nightreach (A5 at lamp 6 — Wren resolved, warm; OPTIONAL "
    "friendly battle vs TRAINERS['wren_nightreach'] (rival, ace ~50, payout "
    "1200, no progression gate); mention the ribbon IF "
    "flag:q_north_ribbon_placed — N3's payoff; sets flag:q_west_lamp_6)",
    "TRAINERS['wren_nightreach']",
    "script.great_null_named (= cutscene.great_null_named; B4 at lamp 7, the "
    "great telescope — letterbox, low uneasy bed, Nessa's haunted portrait, "
    "silence + a single cold tint on 'aimed at the Keystar'; let it sit; sets "
    "flag:q_west_lamp_7 + flag:q_west_vigil_kept + flag:great_null_known + "
    "flag:q_west_vigil)",
    "npc.watch_lamp_unstruck (lamp 1 blocked_ref — the striker ask)",
    "npc.watch_lamp_cold (shared blocked_ref — an earlier lamp is dark)",
]

# ---- the C4 / A5 / B4 staging NPCs (flag-staggered, beside their lamps) -------------
m["npcs"] += [
    # FENN at lamp 5 (appears once lamp 4 is lit; stays after his counsel —
    # he sends you up clear-eyed, he does not march with you)
    {"id": "fenn_counsel", "at": {"tx": 22, "ty": 4}, "facing": "left",
     "sprite": "npc_mentor", "movement": "static",
     "dialogue_ref": "npc.fenn_waits",
     "requires_flag": "flag:q_west_lamp_4",
     "hidden_when_flag": "flag:q_west_lamp_5"},
    {"id": "fenn_after", "at": {"tx": 22, "ty": 4}, "facing": "left",
     "sprite": "npc_mentor", "movement": "static",
     "dialogue_ref": "npc.fenn_after",
     "requires_flag": "flag:q_west_lamp_5"},
    # WREN sitting under lamp 6 (easy again; appears once lamp 5 is lit)
    {"id": "wren_return", "at": {"tx": 23, "ty": 7}, "facing": "up",
     "sprite": "wren", "movement": "static",
     "dialogue_ref": "npc.wren_waits",
     "requires_flag": "flag:q_west_lamp_5",
     "hidden_when_flag": "flag:q_west_lamp_6"},
    {"id": "wren_after", "at": {"tx": 23, "ty": 7}, "facing": "up",
     "sprite": "wren", "movement": "look_around",
     "dialogue_ref": "npc.wren_nightreach_after",
     "requires_flag": "flag:q_west_lamp_6",
     "hidden_when_flag": "gleam:lunar"},
    # NESSA at the seventh lamp (the great telescope) between lamps 6 and 7
    {"id": "nessa_at_seven", "at": {"tx": 22, "ty": 9}, "facing": "left",
     "sprite": "nessa_cole", "movement": "static",
     "dialogue_ref": "npc.nessa_at_seven",
     "requires_flag": "flag:q_west_lamp_6",
     "hidden_when_flag": "flag:q_west_lamp_7"},
]
owed += ["npc.fenn_waits (under lamp 5, before the counsel)",
         "npc.fenn_after (he stays under the densest stars)",
         "npc.wren_waits (sitting under lamp 6, easy again)",
         "npc.wren_nightreach_after ('let's go light the last one')",
         "npc.nessa_at_seven (not looking up from the eyepiece she carried out)"]

# ---- the junior-watcher sight trainers (geometry: the walk's two courts) ------------
owed += pt.trainer_beat(m, tid="junior_watcher_a", at=(8, 5), facing="down",
                        sight=4, sprite="npc_woman")
owed += pt.trainer_beat(m, tid="junior_watcher_b", at=(26, 7), facing="left",
                        sight=4, sprite="npc_man")
owed += ["(junior_watcher_a 'Lira' lv 49-50 ace 50 payout 1000; "
         "junior_watcher_b 'Os' lv 50-51 ace 51 payout 1020 — keeper class, "
         "defs land with the wiring agent; mirror into BUILT_PAYOUTS)"]

# ---- X3 + R5: the junior watcher's flag-staggered ladder (one tile) -----------------
# her beaten swap IS the X3 giver (hooks verbatim) — rewire the stamped after
# placement, then stack the working/done/Round stages on the same tile
for npc in m["npcs"]:
    if npc["id"] == "junior_watcher_a_after":
        npc["dialogue_ref"] = "script.chart_quest"
        npc["hidden_when_flag"] = "flag:q_west_chart"
m["npcs"] += [
    {"id": "junior_watcher_working", "at": {"tx": 8, "ty": 5}, "facing": "down",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.junior_watcher_working",
     "requires_flag": "flag:q_west_chart",
     "hidden_when_flag": "flag:q_west_chart_2"},
    {"id": "junior_watcher_done", "at": {"tx": 8, "ty": 5}, "facing": "down",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "script.chart_done",
     "requires_flag": "flag:q_west_chart_2",
     "hidden_when_flag": "flag:q_west_chart_done"},
    {"id": "junior_watcher_round", "at": {"tx": 8, "ty": 5}, "facing": "down",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "script.round_chart_take",
     "requires_flag": "flag:q_west_chart_done",
     "hidden_when_flag": "flag:q_round_chart_taken"},
    {"id": "junior_watcher_after2", "at": {"tx": 8, "ty": 5}, "facing": "down",
     "sprite": "npc_woman", "movement": "look_around",
     "dialogue_ref": "npc.junior_watcher_after",
     "requires_flag": "flag:q_round_chart_taken"},
]
# the roof-terrace viewpoint (X3 leg 2) — the NE terrace rim, starlit
m["triggers"].append({
    "id": "chart_observatory", "kind": "script", "at": {"tx": 26, "ty": 3},
    "activation": "interact", "ref": "script.chart_observatory", "once": True,
    "requires_flag": "flag:q_west_chart_1",
    "sets_flags": ["flag:q_west_chart_2"],
    "hidden_when_flag": "flag:q_west_chart_2"})
owed += [
    "script.chart_quest (X3 giver — 'Charting the Dark'; sets flag:q_west_chart)",
    "npc.junior_watcher_working",
    "script.chart_observatory (X3 leg 2 — the roof-terrace reading; requires "
    "flag:q_west_chart_1 [Sunvault, BUILT]; sets flag:q_west_chart_2)",
    "script.chart_done (requires _2 only — Coldfog's _3 stays OPTIONAL per "
    "W3's contract; the finished chart NAMES STARWELL; reward + sets "
    "flag:q_west_chart_done)",
    "script.round_chart_take (R5 — she entrusts a fresh star-chart; sets "
    "flag:q_round_chart_taken; DELIVERY = the crossroads Waykeeper, wiring "
    "note: his flag-staggered pair sets flag:q_round_chart — not built here)",
    "npc.junior_watcher_after",
]

# ---- the Star-vigil on the temple steps (Arc E — belonging as witness) --------------
m["npcs"] += [
    # the vigil-warden keeps the steps; her cutscene is the festival's frame
    {"id": "star_vigil_warden", "at": {"tx": 13, "ty": 15}, "facing": "up",
     "sprite": "npc_lampwarden", "movement": "static",
     "dialogue_ref": "script.nightreach_star_vigil",
     "hidden_when_flag": "flag:star_vigil_seen"},
    {"id": "star_vigil_warden_after", "at": {"tx": 13, "ty": 15}, "facing": "up",
     "sprite": "npc_lampwarden", "movement": "static",
     "dialogue_ref": "npc.star_vigil_warden_after",
     "requires_flag": "flag:star_vigil_seen"},
    # watchers standing silent, faces up (the grandest, most reverent festival)
    {"id": "watcher_steps_a", "at": {"tx": 18, "ty": 16}, "facing": "up",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "npc.nightreach_watcher_steps_a"},
    {"id": "watcher_steps_b", "at": {"tx": 12, "ty": 18}, "facing": "up",
     "sprite": "npc_boy", "movement": "static",
     "dialogue_ref": "npc.nightreach_watcher_steps_b"},
    # Arc E payoff: the town answers the eighth Gleam (standing kit)
    # C2 "The Inn's Empty Lamps" (Central wiring): the WEST token giver —
    # the Star-vigil line first, the last lamp-token once the chain reaches her.
    {"id": "festival_lunar_a", "at": {"tx": 17, "ty": 14}, "facing": "up",
     "sprite": "npc_girl", "movement": "wander",
     "dialogue_ref": "script.token_west",
     "requires_flag": "gleam:lunar",
     "hidden_when_flag": "flag:q_token_west"},
    {"id": "festival_lunar_a_after", "at": {"tx": 17, "ty": 14}, "facing": "up",
     "sprite": "npc_girl", "movement": "wander",
     "dialogue_ref": "npc.nightreach_festival_a",
     "requires_flag": "flag:q_token_west"},
    {"id": "festival_lunar_b", "at": {"tx": 14, "ty": 17}, "facing": "up",
     "sprite": "npc_man", "movement": "static",
     "dialogue_ref": "npc.nightreach_festival_b",
     "requires_flag": "gleam:lunar"},
    # witness beat (standing kit): the town reacts to the naming (B4)
    {"id": "nightreach_witness", "at": {"tx": 18, "ty": 21}, "facing": "left",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.nightreach_witness",
     "requires_flag": "flag:great_null_known"},
]
owed += [
    "script.nightreach_star_vigil (= cutscene.nightreach_star_vigil; the "
    "silent night-long watch — silence-led, each watcher's lamp a small "
    "flashColor; sets flag:star_vigil_seen)",
    "npc.star_vigil_warden_after",
    "npc.nightreach_watcher_steps_a", "npc.nightreach_watcher_steps_b",
    "npc.nightreach_festival_a (requires gleam:lunar)",
    "npc.nightreach_festival_b (requires gleam:lunar)",
    "npc.nightreach_witness (requires flag:great_null_known — the naming "
    "lands on a person)",
]

# ---- signs --------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="nightreach_welcome", at=(17, 27))
owed += pt.sign(m, deco, W, sid="nightreach_walk", at=(13, 13))
owed += pt.sign(m, deco, W, sid="nightreach_fogroad", at=(26, 13))
owed += pt.sign(m, deco, W, sid="nightreach_lanternway", at=(6, 27))
# (sign.nightreach_fogroad doubles as the fog warps' blocked_ref)

# ---- caches (variety: a valuable up top, loose wicks in the grass, a charge
# by the fog road — the better finds off the lane) ------------------------------------
owed += pt.cache(m, cid="nightreach_shard", at=(27, 2))    # Starglass Shard,
                                                           # the roof-terrace pocket
owed += pt.cache(m, cid="nightreach_wicks", at=(24, 24))   # loose wicks, SE bed
owed += pt.cache(m, cid="nightreach_charge", at=(27, 17))  # a charge, fog verge

# ---- encounters (band 48-52, approach grass ONLY; picks in the docstring) -----------
TABLE_NR = [
    {"kin_id": 106, "weight": 16, "min_level": 48, "max_level": 51},  # Drowshorn
    {"kin_id": 112, "weight": 16, "min_level": 49, "max_level": 51},  # Nightwraith
    {"kin_id": 105, "weight": 14, "min_level": 48, "max_level": 50},  # Snoozlet
    {"kin_id": 111, "weight": 14, "min_level": 48, "max_level": 50},  # Spirlet
    {"kin_id": 126, "weight": 13, "min_level": 48, "max_level": 51},  # Lunveil
    {"kin_id": 124, "weight": 12, "min_level": 48, "max_level": 50},  # Petalune
    {"kin_id": 127, "weight": 8, "min_level": 50, "max_level": 52},   # Lunvane
    {"kin_id": 129, "weight": 3, "min_level": 51, "max_level": 52},   # Dawnwatcher
]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if goldtuft[i]:
        (band_grid if (i // W) in (25, 26) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE_NR, id_prefix="verge")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE_NR, id_prefix="crossing")

# ---- temple-step + town dressing ----------------------------------------------------
m["objects"] += [
    # star banners flanking the steps' foot and the street's head
    {"id": "banner_steps_w", "sprite": "nightreach_star_banner",
     "at": {"tx": 13, "ty": 14}, "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "banner_steps_e", "sprite": "nightreach_star_banner",
     "at": {"tx": 18, "ty": 14}, "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "banner_terrace_w", "sprite": "nightreach_star_banner",
     "at": {"tx": 12, "ty": 10}, "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "banner_terrace_e", "sprite": "nightreach_star_banner",
     "at": {"tx": 19, "ty": 10}, "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    # the Star-vigil's small lit vigil lamps along the steps court
    {"id": "vigil_steps_a", "sprite": "nightreach_vigil_lamp",
     "at": {"tx": 14, "ty": 16}, "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "vigil_steps_b", "sprite": "nightreach_vigil_lamp",
     "at": {"tx": 17, "ty": 16}, "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "vigil_street_a", "sprite": "nightreach_vigil_lamp",
     "at": {"tx": 10, "ty": 19}, "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "vigil_street_b", "sprite": "nightreach_vigil_lamp",
     "at": {"tx": 21, "ty": 19}, "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    # lamp posts beside (never on) the walked lanes
    {"id": "lamp_entry", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 14, "ty": 25}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_spoke", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 3, "ty": 24}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_fog", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 24, "ty": 12}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- THE DENSEST STARFIELD: glint clusters over the dark crags, thickening
# toward the north rim (near-dawn pallor lives at the horizon line) -------------------
GLINTS = [(3, 0), (8, 0), (11, 1), (19, 0), (23, 1), (27, 0), (6, 1), (25, 0),
          (1, 3), (0, 8), (1, 12), (28, 4), (29, 9), (28, 11),
          (0, 17), (29, 20), (1, 26), (28, 26), (12, 29), (20, 29)]
for i, (sx, sy) in enumerate(GLINTS):
    dense = i < 14  # the north + flank rows take the dense clusters
    m["objects"].append({
        "id": f"starglint_{i}",
        "sprite": (f"nightreach_starglint_{'a' if i % 2 else 'b'}" if dense
                   else rng.choice(["windward_starglint_a", "windward_starglint_b"])),
        "at": {"tx": sx, "ty": sy}, "w": 1, "h": 1, "solid": False})

# ---- scatter + boulders (goldgrass scatter is hand-rolled — the Sunvault way) -------
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
                and rng.random() < 0.13:
            deco[i] = rng.choice(blooms) if rng.random() < 0.4 else gid("g_pebble")
for (x, y) in [(3, 17), (9, 17), (20, 23), (3, 27), (26, 22), (12, 23),
               (27, 27), (8, 27)]:
    if (x, y) not in avoid and deco[y * W + x] == 0:
        deco[y * W + x] = gid("boulder")
# the inn's FENCED STAR-GARDEN (§11 r5: every town keeps one fenced garden;
# it also pays the west pocket behind the inn — §3a r4): night-blooms under
# the watchers' windows, a balm cache among them, a fence along the south
for (x, y) in [(2, 14), (3, 14), (2, 15), (3, 15), (2, 16)]:
    deco[y * W + x] = blooms[(x + y) % 2]
mk.fence_run(deco, W, H, 2, 17, 3)
owed += pt.cache(m, cid="nightreach_balm", at=(3, 16))  # consumable, the garden
# grey moss creeps the blight stain at the fog gate (the drained seam)
for (x, y, n) in [(26, 16, "greymoss_a"), (27, 13, "greymoss_b"),
                  (25, 16, "greymoss_b")]:
    if (x, y) not in avoid and deco[y * W + x] == 0:
        deco[y * W + x] = gid(n)

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
