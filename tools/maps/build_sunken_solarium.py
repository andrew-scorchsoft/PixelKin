#!/usr/bin/env python3
"""
Sunken Solarium — the drowned sun-garden where warmth is remembered
(walkthrough/04-west "Sunken Solarium"; kind route/ruin, region west, band
42-46; Lumenary 7: Lucan Pyre, Solar — THE LIT STAGE earned loop, spine §5
shape #7 "flooded gathering"). The Arc D pivot: the first real warmth since
the south.

Three signature touches (§8):
  1. THE HELIARIUM STAGE — a sunken performance terrace at the garden's
     heart: broken proscenium arch, THREE DEAD BRAZIERS, the Last-Warm-Day
     troupe waiting in costume beside it. The Gleam is earned by relighting
     it, spark by spark, out of the flooded halls.
  2. THE FLOODED INNER HALLS — knee-deep night-water (sunpool, Tidecall HELD
     since Pearlmoor: the old Gift made load-bearing, spine §5) over drowned
     ruin paving, colonnade stumps, the sunmote phials glinting on islets and
     far-shore pockets, two troupe-player sight trainers working the lanes.
  3. THE LAST-WARM-DAY TERRACE — the festival on the sunlit NW terrace under
     the gen'd Solar Lumenary hall: stored-daylight lanterns, warm bread,
     belonging before the bond-test.

§0 TRAP #1 (binding, hooks verbatim): the Lumenary + Lucan are reachable
WITHOUT Sunsketch — the dry causeway (entry rows 8-9 -> the garden -> the
stage's north face) carries ZERO gates. Sunsketch gates only the ONWARD
sunvault_climb_i->ii boundary + Helia Vault (both off-map) and the optional
in-ruin back-fold pocket (W garden). The flooded halls use Tidecall (held).

HANDSHAKE (W1, verified): hushfrost_pass_ii `to_solarium` at (0,8)/(0,9)
lands HERE at (30,8)/(30,9) — width 31, EAST-edge entry, landings ON our
return pair `to_pass_ii`/`to_pass_ii_s`, which land at hushfrost (1,8)/(1,9).
HANDSHAKE (W2-internal, built both sides): our `to_climb`/`to_climb_s` at
(0,28)/(0,29) land at sunvault_climb_i (28,14)/(28,15); its return pair at
(29,14)/(29,15) lands at our (1,28)/(1,29). UNGATED both ways.
INTERIOR: the hall door is TWO tiles wide in the gen art -> two door warps
(5,7)/(6,7) -> sunken_solarium_lumenary (8,11), starter-gated like every
Lumenary (graph.ts gains the node + `to_lumenary` edge).

THE LIT STAGE chain (hooks verbatim; one-flag-per-trigger ENCODING NOTE):
EventTrigger carries a single requires_flag, so "each brazier requires its
mote + the previous brazier" is encoded TRANSITIVELY — each next phial only
appears once the previous brazier burns (diegetic: every lighting wakes the
next glimmer in the drowned halls), so brazier N's mote-flag implies
brazier N-1. The chain, in order:
  script.lucan_quest                      -> flag:q_west_stage
  cache sunmote_1 (requires q_west_stage) -> script.sunmote_1 -> flag:q_west_mote_1
  brazier_1 (requires q_west_mote_1)      -> script.brazier_1 -> flag:q_west_brazier_1
  cache sunmote_2 (requires brazier_1)    -> script.sunmote_2 -> flag:q_west_mote_2
  brazier_2 (requires q_west_mote_2)      -> script.brazier_2 -> flag:q_west_brazier_2
  cache sunmote_3 (requires brazier_2)    -> script.sunmote_3 -> flag:q_west_mote_3
  brazier_3 (requires q_west_mote_3)      -> script.brazier_3 -> flag:q_west_stage_lit
Brazier dead->lit object swaps + the three NIGHT-FLOWER rows along the stage
rim bloom per lighting (pure visual Sunsketch FORESHADOW — no Sunsketch
required; the pale_vault bracket flag-pair pattern, same footprint+solidity).
Lucan's bond-test: interact trigger centre-stage, requires
flag:q_west_stage_lit, blocked_ref npc.lucan_not_ready, hidden at gleam:solar
-> script.lumenary_solarium (battle vs TRAINERS['lucan_pyre'], warden class
ai:'smart', ace 46, payout 60x46=2760, reward_flags ['gleam:solar'],
reward_abilities ['sunsketch'] — the engine alone sets crown_west, at
Nightreach, never here).

X2 "The Troupe's Sun-mask" (hooks verbatim): giver = the troupe player's
post-stage swap NPC -> script.mask_quest -> flag:q_west_mask; the gilt mask
sank in the SE flooded side room (Tidecall dive — the chamber's only mouth
is under water) -> script.pickup_sun_mask -> flag:picked_sun_mask; return ->
script.mask_done gives the SUN CHARM + flag:q_west_mask_found. Every
flag:q_west_* opened here is consumed here (spine §0 rule 3).

Encounter design — THE 24 DESIGNED ROWS RECONCILED: species data carries 24
sunken_solarium rows (the generator placed them all as terrain 'water',
bands 38-50). We keep ALL 24 kin and split them by each kin's dex habitat —
dry garden (goldtuft) vs flooded halls (sunpool water) — and clamp levels to
the walkthrough band 42-46 (continuous with Hushfrost 40-42 / Sunvault
46-48; stage-2/3 forms return at full strength on the Climb). The
EXTRA_ENCOUNTERS mirror in tools/balance/build_species.py = wiring agent.

Trainer beats (route class, payout 16 x ace — wiring agent authors):
  troupe_player_a "Troupe Player Lyra"  2 kin lv43-44, ace 44, payout 704
  troupe_player_b "Troupe Player Orsino" 2 kin lv44-45, ace 45, payout 720

HUMOUR NOTE (the sanctioned warm-wry register — 2 of the cluster's 3 lines
live here, both troupe, both gentle bathos; the Last-Warm-Day itself stays
bittersweet-sacred):
  npc.troupe_stilts      "Forty years we've staged 'The Sun Returns'. One
                          night soon I'd like the title to stop being the
                          ambitious part."
  npc.troupe_mask_after  "You dredged my face out of a drowned cellar and
                          I've never looked better. That's theatre."

Suggested sign copy (wiring agent writes dialogue.ts):
  sign.solarium_welcome  "THE SUNKEN SOLARIUM. The sun drowned here, they
                          say. Listen close: it's only sleeping."
  sign.solarium_halls    "The flooded halls. The moon-tide parts for a
                          called tide — what drowned here waits for you."
                          (the Tidecall 'old Gift in service' callout)
  sign.solarium_backfold "Night-flowers seal this fold. A pocket of daylight
                          would wake them." (the Sunsketch tease + comeback)
  sign.solarium_climb    "WEST — THE SUNVAULT CLIMB. The garden-roads rise
                          toward the stars from here."

audit_flow notes — the shelf cache, mote pockets, back-fold and mask chamber
are paid dead ends by design (§3a r4); the halls ring the stage with two
lanes (loop). The festival terrace + stage own their screens (§3a r5).

Run:  ./venv/bin/python tools/maps/build_sunken_solarium.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 31, 34
rng = random.Random(72)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
cliff = mk.make_grid(W, H)      # basin walls + chokes + pocket rims (the ruin's bones)
ruin = mk.make_grid(W, H)       # ruinfloor: causeway, stage, the halls' paving
pool = mk.make_grid(W, H)       # sunpool: the flooded halls (Tidecall rides the tiles)
goldtuft = mk.make_grid(W, H)   # the gold encounter beds + mandatory bands
deco = mk.make_grid(W, H)

# BORDERS: the sunken basin — cliff all round, 2 deep, organic bumps (§11 r2)
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.rect(cliff, W, H, 0, 32, W - 1, H - 1)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)
mk.rect(cliff, W, H, 29, 0, 30, H - 1)
mk.organic_border(cliff, W, H, depth=0,
                  bumps=[(8, 1, 2), (18, 1, 2), (1, 13, 2), (1, 22, 2),
                         (29, 18, 2), (12, 32, 2), (20, 33, 2)],
                  rng=rng)
# EAST gap — the W1 handshake (rows 8-9; landings (30,8)/(30,9) stay walkable)
for x in (29, 30):
    for y in (8, 9):
        cliff[y * W + x] = 0
# WEST gap — the Sunvault exit (rows 28-29)
for x in (0, 1):
    for y in (28, 29):
        cliff[y * W + x] = 0

# THE ENTRY CHOKES: cliff masses pinch the east entry into the rows 8-9
# causeway (the arrival band cannot be walked around)
mk.rect(cliff, W, H, 20, 2, 30, 7)            # NE mass
mk.rect(cliff, W, H, 22, 10, 30, 12)          # SE mass under the causeway (row 13
                                              # stays open: the shelf's approach)
mk.blob(cliff, W, H, 21.0, 7.0, 1.6, 1.1)     # organic bumps off the masses
mk.blob(cliff, W, H, 24.0, 12.0, 1.6, 0.9)
# THE TERRACE PINCH: the festival terrace is entered only via rows 8-9 at
# x13-14 (the Last-Warm-Day band owns that cut)
mk.rect(cliff, W, H, 14, 2, 15, 7)
# THE EXIT CHOKES: the west leg to the Climb runs x2-7 (band rows 26-27)
mk.rect(cliff, W, H, 8, 25, 9, 31)            # east wall of the exit leg
mk.blob(cliff, W, H, 8.5, 24.5, 1.4, 1.0)

# ---- THE EAST SHELF (elevation accent §11 r3 + the one-way return §3a r1/r2) -------
shelf = pt.Area(23, 14, 28, 19)
pt.terrace(cliff, deco, W, H, shelf, gap=(25, 26), gap_side="up", rim=1, rng=rng)
# (interior x24-27 y15-18; ledge along y19 hops down into the halls; climbed
# from the garden via cols 25-26 at y14)

# ---- lanes / paving (ruinfloor — the drowned garden's bones) ------------------------
mk.rect(ruin, W, H, 18, 8, 30, 9)             # the entry causeway
mk.rect(ruin, W, H, 2, 8, 17, 9)              # the garden road west to the terrace
mk.rect(ruin, W, H, 16, 10, 17, 19)           # the lane south to the stage
# THE HELIARIUM STAGE platform
mk.rect(ruin, W, H, 11, 13, 19, 18)
# THE FLOODED INNER HALLS' paving field (pools carve into it below)
mk.rect(ruin, W, H, 2, 20, 28, 31)
mk.blob(ruin, W, H, 5.0, 19.0, 2.0, 1.2)      # the field laps up at the garden seam
mk.blob(ruin, W, H, 24.0, 20.0, 2.0, 1.0)

# ---- the flooded halls (sunpool = water-over-ruin; Tidecall rides the tiles) -------
mk.blob(pool, W, H, 8.5, 23.5, 3.2, 2.2)      # Pool A (west)
mk.blob(pool, W, H, 16.0, 25.5, 4.4, 2.8)     # Pool B (central)
mk.blob(pool, W, H, 24.0, 24.0, 3.6, 2.6)     # Pool C (east, the mask room's water)
# islets (the fen precedent): dry cells carved back out of the water
for (ix, iy) in ((8, 23), (9, 23)):           # Pool A islet — sunmote_1
    pool[iy * W + ix] = 0
for (ix, iy) in ((15, 25), (16, 25)):         # Pool B islet — a charge cache
    pool[iy * W + ix] = 0
# THE MOTE POCKET south of Pool B (far shore — swim to it)
mk.rect(cliff, W, H, 13, 28, 13, 31)
mk.rect(cliff, W, H, 19, 28, 19, 31)
for y in (29, 30):
    for x in (14, 15, 16, 17, 18):
        pool[y * W + x] = 0                   # the pocket floor stays dry
        cliff[y * W + x] = 0
# seal the pocket's south rim against the border
mk.rect(cliff, W, H, 14, 31, 18, 31)
# THE MASK CHAMBER (X2, SE): its only mouth opens under Pool C's south lobe
mk.rect(cliff, W, H, 22, 27, 22, 32)          # west wall
mk.rect(cliff, W, H, 28, 27, 28, 32)          # east wall
mk.rect(cliff, W, H, 23, 31, 27, 31)          # south wall (border meets it)
for y in (28, 29, 30):
    for x in (23, 24, 25, 26, 27):
        pool[y * W + x] = 0
        cliff[y * W + x] = 0
mk.rect(cliff, W, H, 23, 28, 23, 28)          # round the mouth to cols 24-27
mk.rect(cliff, W, H, 27, 28, 27, 28)
# the mouth's water sill: the chamber is entered ONLY through Pool C
for x in (24, 25, 26):
    pool[27 * W + x] = 1
    ruin[27 * W + x] = 1                      # (water-over-ruin context)

# ---- THE BACK-FOLD (Sunsketch, optional — the gentle first puzzle taste) -----------
mk.rect(cliff, W, H, 2, 13, 6, 18)            # the west-garden fold massif
for y in (15, 16, 17):
    for x in (3, 4, 5):
        cliff[y * W + x] = 0                  # pocket interior
# the 1-tile night-flower cut at (6,16) — gated below, vine drawn over it
cliff[16 * W + 6] = 1

# ---- encounter terrain (goldtuft) ---------------------------------------------------
mk.blob(goldtuft, W, H, 5.0, 11.5, 2.4, 1.3)  # west-garden patch (optional)
mk.blob(goldtuft, W, H, 21.0, 16.5, 2.0, 1.4) # east-garden patch by the shelf
# MANDATORY crossings (§11 r7): the garden band + the exit leg, lanes paused
pt.mandatory_band(goldtuft, ruin, W, H, y0=10, y1=11, x0=2, x1=21)
pt.mandatory_band(goldtuft, ruin, W, H, y0=26, y1=27, x0=2, x1=7)

# ---- precedence (structure wins; one family per cell) -------------------------------
for i in range(W * H):
    if cliff[i]:
        ruin[i] = 0
        pool[i] = 0
        goldtuft[i] = 0
    if pool[i]:
        ruin[i] = 0
        goldtuft[i] = 0
    if ruin[i]:
        goldtuft[i] = 0

# ---- base: gold grass (the West's remembered light) ---------------------------------
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": ruin},
    {"name": "t_goldtuft", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": goldtuft},
    {"name": "t_pool", "role": "terrain", "terrain": "sunpool",
     "set": "vesper_overworld_set", "depth": 0, "data": pool},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

m: dict = {
    "id": "sunken_solarium", "display_name": "Sunken Solarium",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [
        # the back-fold's night-flower cut — Sunsketch force-gates the 1-tile
        # cliff cell; the vine object is the visual (optional ONLY: never the
        # Lumenary, §0 rule 1)
        {"id": "backfold_vines", "ability": "sunsketch",
         "rect": {"tx": 6, "ty": 16, "w": 1, "h": 1}, "effect": "make_passable"},
    ],
    "music": "assets/audio/music/sunken-solarium-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/sunken-solarium-a.webp",
        "assets/backgrounds/battle/sunken-solarium-b.webp",
    ],
}

# ---- the Lumenary hall (gen'd hero piece; the door art is two tiles wide) ----------
pt.building(m, ruin, W, H, oid="lumenary", sprite="solarium_lumenary",
            at=(3, 2), overhang=3, door_col=2,
            to_map="sunken_solarium_lumenary", to=(8, 11))
m["warps"][-1].update({"id": "to_lumenary", "requires_flag": "flag:has_starter",
                       "blocked_ref": "door.locked_lumenary"})
m["warps"].append({"id": "to_lumenary_e", "at": {"tx": 6, "ty": 7},
                   "trigger": "step_on", "to_map": "sunken_solarium_lumenary",
                   "to": {"tx": 8, "ty": 11}, "facing": "up",
                   "transition": "door", "requires_flag": "flag:has_starter",
                   "blocked_ref": "door.locked_lumenary"})

# ---- THE HELIARIUM STAGE dressing ---------------------------------------------------
m["objects"] += [
    # the broken proscenium on the platform's north rim
    {"id": "stage_arch", "sprite": "solarium_stage_arch",
     "at": {"tx": 13, "ty": 11}, "w": 5, "h": 3, "overhang": 2},
    # THE THREE BRAZIERS (dead -> lit, the Lit Stage swap pairs; same
    # footprint + solidity — collision is flag-blind)
    {"id": "brazier_1_lit", "sprite": "solarium_brazier_lit",
     "at": {"tx": 11, "ty": 13}, "w": 2, "h": 3, "overhang": 1,
     "requires_flag": "flag:q_west_brazier_1"},
    {"id": "brazier_1_dead", "sprite": "solarium_brazier_dead",
     "at": {"tx": 11, "ty": 13}, "w": 2, "h": 3, "overhang": 1,
     "hidden_when_flag": "flag:q_west_brazier_1"},
    {"id": "brazier_2_lit", "sprite": "solarium_brazier_lit",
     "at": {"tx": 18, "ty": 13}, "w": 2, "h": 3, "overhang": 1,
     "requires_flag": "flag:q_west_brazier_2"},
    {"id": "brazier_2_dead", "sprite": "solarium_brazier_dead",
     "at": {"tx": 18, "ty": 13}, "w": 2, "h": 3, "overhang": 1,
     "hidden_when_flag": "flag:q_west_brazier_2"},
    {"id": "brazier_3_lit", "sprite": "solarium_brazier_lit",
     "at": {"tx": 15, "ty": 14}, "w": 2, "h": 3, "overhang": 1,
     "requires_flag": "flag:q_west_stage_lit"},
    {"id": "brazier_3_dead", "sprite": "solarium_brazier_dead",
     "at": {"tx": 15, "ty": 14}, "w": 2, "h": 3, "overhang": 1,
     "hidden_when_flag": "flag:q_west_stage_lit"},
    # THE NIGHT-FLOWER ROWS along the stage rim — closed -> bloomed per
    # lighting (visual Sunsketch foreshadow; non-solid set dressing)
    {"id": "flowers_1_bloom", "sprite": "solarium_nightflowers_bloomed",
     "at": {"tx": 11, "ty": 18}, "w": 3, "h": 1, "solid": False,
     "requires_flag": "flag:q_west_brazier_1"},
    {"id": "flowers_1_closed", "sprite": "solarium_nightflowers_closed",
     "at": {"tx": 11, "ty": 18}, "w": 3, "h": 1, "solid": False,
     "hidden_when_flag": "flag:q_west_brazier_1"},
    {"id": "flowers_2_bloom", "sprite": "solarium_nightflowers_bloomed",
     "at": {"tx": 17, "ty": 18}, "w": 3, "h": 1, "solid": False,
     "requires_flag": "flag:q_west_brazier_2"},
    {"id": "flowers_2_closed", "sprite": "solarium_nightflowers_closed",
     "at": {"tx": 17, "ty": 18}, "w": 3, "h": 1, "solid": False,
     "hidden_when_flag": "flag:q_west_brazier_2"},
    {"id": "flowers_3_bloom", "sprite": "solarium_nightflowers_bloomed",
     "at": {"tx": 14, "ty": 12}, "w": 3, "h": 1, "solid": False,
     "requires_flag": "flag:q_west_stage_lit"},
    {"id": "flowers_3_closed", "sprite": "solarium_nightflowers_closed",
     "at": {"tx": 14, "ty": 12}, "w": 3, "h": 1, "solid": False,
     "hidden_when_flag": "flag:q_west_stage_lit"},
    # the Last-Warm-Day's lit terrace brazier (always warm — the festival's
    # stored-daylight lanterns; the THREE quest braziers are the dead ones)
    {"id": "brazier_festival", "sprite": "solarium_brazier_lit",
     "at": {"tx": 12, "ty": 2}, "w": 2, "h": 3, "overhang": 1},
    # the troupe's wagon + costume rack beside the stage (their whole theatre)
    {"id": "troupe_cart", "sprite": "solarium_troupe_cart",
     "at": {"tx": 7, "ty": 14}, "w": 3, "h": 2},
    {"id": "costume_rack", "sprite": "solarium_costume_rack",
     "at": {"tx": 8, "ty": 17}, "w": 2, "h": 2},
]

# the brazier interact triggers (the chain — see the module docstring).
# Each sits ON its brazier's bottom footprint row: interact fires on the
# tile the player FACES (WorldScene.interact -> tileAhead), so standing
# before the brazier and pressing Confirm pours the phial.
for n, (bx, by, req, sets) in enumerate([
        (11, 15, "flag:q_west_mote_1", "flag:q_west_brazier_1"),
        (18, 15, "flag:q_west_mote_2", "flag:q_west_brazier_2"),
        (15, 16, "flag:q_west_mote_3", "flag:q_west_stage_lit")], start=1):
    m["triggers"].append({
        "id": f"brazier_{n}", "kind": "script", "at": {"tx": bx, "ty": by},
        "activation": "interact", "ref": f"script.brazier_{n}", "once": True,
        "requires_flag": req, "blocked_ref": "npc.solarium_brazier_dead",
        "sets_flags": [sets], "hidden_when_flag": sets})
owed += ["script.brazier_1 (pour the phial; the west row of night-flowers "
         "blooms; sets flag:q_west_brazier_1)",
         "script.brazier_2 (sets flag:q_west_brazier_2)",
         "script.brazier_3 (the stage lights whole; the troupe takes it; the "
         "festival crests — minor->major per cinematics.md; sets "
         "flag:q_west_stage_lit)",
         "npc.solarium_brazier_dead (blocked line: cold drowned daylight)"]

# THE BOND-TEST — centre-stage, in front of where ready-Lucan stands
m["triggers"].append({
    "id": "lucan_bond_test", "kind": "cutscene", "at": {"tx": 14, "ty": 17},
    "activation": "interact", "ref": "script.lumenary_solarium", "once": True,
    "requires_flag": "flag:q_west_stage_lit",
    "blocked_ref": "npc.lucan_not_ready",
    "hidden_when_flag": "gleam:solar"})
owed += ["script.lumenary_solarium (the bond-test ON the lit stage: battle vs "
         "TRAINERS['lucan_pyre'] — warden class ai:'smart', ace 46, payout "
         "2760, reward_flags ['gleam:solar'], reward_abilities ['sunsketch']; "
         "theatrical and warm; the Gleam cadence minor->major)",
         "TRAINERS['lucan_pyre']",
         "npc.lucan_not_ready (bond-test blocked_ref, his voice: 'the stage "
         "is dark and the daylight's drowned — fetch it up, spark by spark')"]

# ---- Lucan's placements (hook -> waiting -> ready -> after) -------------------------
m["npcs"] += [
    {"id": "lucan_quest", "at": {"tx": 9, "ty": 16}, "facing": "right",
     "sprite": "lucan_pyre", "movement": "static",
     "dialogue_ref": "script.lucan_quest",
     "hidden_when_flag": "flag:q_west_stage"},
    {"id": "lucan_waiting", "at": {"tx": 9, "ty": 16}, "facing": "right",
     "sprite": "lucan_pyre", "movement": "static",
     "dialogue_ref": "npc.lucan_waiting",
     "requires_flag": "flag:q_west_stage",
     "hidden_when_flag": "flag:q_west_stage_lit"},
    {"id": "lucan_ready", "at": {"tx": 14, "ty": 16}, "facing": "down",
     "sprite": "lucan_pyre", "movement": "static",
     "dialogue_ref": "script.lumenary_solarium",
     "requires_flag": "flag:q_west_stage_lit",
     "hidden_when_flag": "gleam:solar"},
    {"id": "lucan_after", "at": {"tx": 14, "ty": 16}, "facing": "down",
     "sprite": "lucan_pyre", "movement": "static",
     "dialogue_ref": "npc.lucan_after",
     "requires_flag": "gleam:solar"},
]
owed += ["script.lucan_quest (the hook, his voice: 'A bond that remembers the "
         "sun! Then prove the memory...' — sets flag:q_west_stage)",
         "npc.lucan_waiting", "npc.lucan_after (the Solar Gleam festival payoff)"]

# ---- the troupe beside the stage (witness beats + the X2 chain) ---------------------
m["npcs"] += [
    # the waiting troupe (pre-lit) -> the post-stage swap (the X2 giver)
    {"id": "troupe_player", "at": {"tx": 8, "ty": 19}, "facing": "right",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.troupe_waiting",
     "hidden_when_flag": "flag:q_west_stage_lit"},
    {"id": "troupe_mask_quest", "at": {"tx": 8, "ty": 19}, "facing": "right",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "script.mask_quest",
     "requires_flag": "flag:q_west_stage_lit",
     "hidden_when_flag": "flag:q_west_mask"},
    {"id": "troupe_mask_waiting", "at": {"tx": 8, "ty": 19}, "facing": "right",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.troupe_mask_waiting",
     "requires_flag": "flag:q_west_mask",
     "hidden_when_flag": "flag:picked_sun_mask"},
    {"id": "troupe_mask_done", "at": {"tx": 8, "ty": 19}, "facing": "right",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "script.mask_done",
     "requires_flag": "flag:picked_sun_mask",
     "hidden_when_flag": "flag:q_west_mask_found"},
    {"id": "troupe_mask_after", "at": {"tx": 8, "ty": 19}, "facing": "right",
     "sprite": "npc_woman", "movement": "look_around",
     "dialogue_ref": "npc.troupe_mask_after",
     "requires_flag": "flag:q_west_mask_found"},
    # the stilt-walker (humour slot; swaps to a stage witness once it lights)
    {"id": "troupe_stilts", "at": {"tx": 10, "ty": 19}, "facing": "up",
     "sprite": "npc_man", "movement": "look_around",
     "dialogue_ref": "npc.troupe_stilts",
     "hidden_when_flag": "flag:q_west_stage_lit"},
    {"id": "solarium_witness", "at": {"tx": 10, "ty": 19}, "facing": "up",
     "sprite": "npc_man", "movement": "static",
     "dialogue_ref": "npc.solarium_witness",
     "requires_flag": "flag:q_west_stage_lit"},
]
owed += ["npc.troupe_waiting (in costume beside the dark stage)",
         "script.mask_quest (X2 giver; sets flag:q_west_mask)",
         "npc.troupe_mask_waiting",
         "script.mask_done (requires flag:picked_sun_mask; gives the SUN CHARM "
         "— conditional charge, suggest x2.5 on Solar-met kin, the Aurora "
         "Charm pattern; sets flag:q_west_mask_found)",
         "npc.troupe_mask_after (HUMOUR slot 2 — copy in the docstring)",
         "npc.troupe_stilts (HUMOUR slot 1 — copy in the docstring)",
         "npc.solarium_witness (the witness beat: the troupe takes the stage)"]

# ---- THE SUNMOTE PHIALS (the chain's caches — hand-rolled so the flags match
# the hooks VERBATIM: flag:q_west_mote_1..3) -----------------------------------------
for n, (cx, cy, req) in enumerate([
        (8, 23, "flag:q_west_stage"),          # Pool A islet
        (16, 30, "flag:q_west_brazier_1"),     # the far-shore pocket past Pool B
        (24, 23, "flag:q_west_brazier_2")],    # Pool C shore-islet, by the chamber
        start=1):
    m["npcs"].append({
        "id": f"cache_sunmote_{n}", "at": {"tx": cx, "ty": cy}, "facing": "down",
        "sprite": "item_cache", "movement": "static",
        "dialogue_ref": f"script.sunmote_{n}",
        "requires_flag": req,
        "hidden_when_flag": f"flag:q_west_mote_{n}"})
owed += ["script.sunmote_1 (the phial glints on the islet; sets flag:q_west_mote_1)",
         "script.sunmote_2 (sets flag:q_west_mote_2 — appears once brazier 1 "
         "burns: every lighting wakes the next glimmer)",
         "script.sunmote_3 (sets flag:q_west_mote_3)"]
# Pool C's mote sits on a dry shore-islet: carve it out of the pool (this runs
# AFTER the precedence pass, so re-assert the ruin paving under the islet)
for (ix, iy) in ((24, 23), (25, 23)):
    pool[iy * W + ix] = 0
    ruin[iy * W + ix] = 1

# ---- the X2 mask cache + chamber dressing ------------------------------------------
m["npcs"].append({
    "id": "cache_sun_mask", "at": {"tx": 25, "ty": 30}, "facing": "down",
    "sprite": "item_cache", "movement": "static",
    "dialogue_ref": "script.pickup_sun_mask",
    "requires_flag": "flag:q_west_mask",
    "hidden_when_flag": "flag:picked_sun_mask"})
owed += ["script.pickup_sun_mask (the gilt mask out of the silt; sets "
         "flag:picked_sun_mask)"]
m["objects"] += [
    {"id": "mask_glint", "sprite": "solarium_sun_mask",
     "at": {"tx": 26, "ty": 30}, "w": 1, "h": 1, "solid": False},
    {"id": "chamber_column", "sprite": "solarium_column",
     "at": {"tx": 23, "ty": 28}, "w": 1, "h": 3, "overhang": 1, "walk_under": True},
]

# ---- THE BACK-FOLD vines + reward ---------------------------------------------------
m["objects"] += [
    {"id": "backfold_vine_bloomed", "sprite": "sunvault_vine_h_bloomed",
     "at": {"tx": 5, "ty": 16}, "w": 3, "h": 1, "solid": False,
     "requires_flag": "gleam:solar"},
    {"id": "backfold_vine_withered", "sprite": "sunvault_vine_h_withered",
     "at": {"tx": 5, "ty": 16}, "w": 3, "h": 1, "solid": False,
     "hidden_when_flag": "gleam:solar"},
]
owed += pt.cache(m, cid="solarium_shard", at=(4, 16))   # Starglass Shard (valuable)
owed += pt.sign(m, deco, W, sid="solarium_backfold", at=(7, 14))

# ---- story bands (compute the cut from the grids; band ONLY walkable cells) --------
# Arc D arrival — the first warmth since the south (the causeway choke)
for i, ty in enumerate((8, 9)):
    m["triggers"].append({
        "id": f"solarium_arrival_{i}", "kind": "cutscene",
        "at": {"tx": 26, "ty": ty}, "activation": "step_on",
        "ref": "script.solarium_arrival", "once": True,
        "sets_flags": ["flag:solarium_arrived"],
        "hidden_when_flag": "flag:solarium_arrived"})
owed += ["script.solarium_arrival (= cutscene.solarium_arrival; Arc D pivot — "
         "the gold light after the cold; warm tint + the music crossfade; "
         "sets flag:solarium_arrived)"]
# Arc E — the Last-Warm-Day fills the terrace (the x13-14 pinch, rows 8-9)
for i, (tx, ty) in enumerate(((13, 8), (13, 9), (14, 8), (14, 9))):
    if cliff[ty * W + tx]:
        continue
    m["triggers"].append({
        "id": f"last_warm_day_{i}", "kind": "cutscene",
        "at": {"tx": tx, "ty": ty}, "activation": "step_on",
        "ref": "script.solarium_last_warm_day", "once": True,
        "sets_flags": ["flag:last_warm_day_seen"],
        "hidden_when_flag": "flag:last_warm_day_seen"})
owed += ["script.solarium_last_warm_day (= cutscene.solarium_last_warm_day per "
         "the hooks; Arc E — bittersweet-SACRED, no humour: stored-daylight "
         "lanterns, warm bread, 'we keep spending warm days until one sticks'; "
         "sets flag:last_warm_day_seen)"]

# ---- the festival terrace NPCs ------------------------------------------------------
m["npcs"] += [
    {"id": "festival_goer", "at": {"tx": 11, "ty": 5}, "facing": "down",
     "sprite": "npc_old_man", "movement": "static",
     "dialogue_ref": "npc.solarium_festival_goer"},
    {"id": "bread_sharer", "at": {"tx": 12, "ty": 8}, "facing": "left",
     "sprite": "npc_woman", "movement": "look_around",
     "dialogue_ref": "npc.solarium_bread"},
    {"id": "festival_kid", "at": {"tx": 10, "ty": 7}, "facing": "down",
     "sprite": "npc_child", "movement": "wander",
     "dialogue_ref": "npc.solarium_kid"},
    # the Gleam's festival payoff (the town answers the win — standing kit)
    {"id": "gleam_watcher", "at": {"tx": 12, "ty": 6}, "facing": "up",
     "sprite": "npc_girl", "movement": "static",
     "dialogue_ref": "npc.solarium_gleam_watcher",
     "requires_flag": "gleam:solar"},
    {"id": "gleam_elder", "at": {"tx": 9, "ty": 5}, "facing": "down",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "npc.solarium_gleam_elder",
     "requires_flag": "gleam:solar"},
]
owed += ["npc.solarium_festival_goer (the signature line: 'we just keep "
         "spending warm days until one of them sticks')",
         "npc.solarium_bread", "npc.solarium_kid",
         "npc.solarium_gleam_watcher (requires gleam:solar)",
         "npc.solarium_gleam_elder (requires gleam:solar)"]

# ---- trainer beats (the water lanes, lv 43-45) --------------------------------------
owed += pt.trainer_beat(m, tid="troupe_player_a", at=(12, 20), facing="right",
                        sight=4, sprite="npc_man")
owed += pt.trainer_beat(m, tid="troupe_player_b", at=(21, 27), facing="left",
                        sight=4, sprite="npc_woman")

# ---- signs --------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="solarium_welcome", at=(27, 7))
owed += pt.sign(m, deco, W, sid="solarium_halls", at=(15, 19))
owed += pt.sign(m, deco, W, sid="solarium_climb", at=(3, 25))

# ---- caches (variety rule: consumable + valuable + loose wicks) ---------------------
owed += pt.cache(m, cid="solarium_balm", at=(4, 12))      # consumable, west garden
owed += pt.cache(m, cid="solarium_amber", at=(26, 16))    # Moth-amber, ON the shelf
owed += pt.cache(m, cid="solarium_wicks", at=(17, 4))     # loose wicks — pays the
                                                          # off-lane pocket north of
                                                          # the causeway (§3a r4)
owed += pt.cache(m, cid="solarium_charge", at=(15, 24))   # a charge, Pool B islet

# ---- colonnade + garden dressing ----------------------------------------------------
m["objects"] += [
    {"id": "column_a", "sprite": "solarium_column", "at": {"tx": 19, "ty": 6},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_b", "sprite": "solarium_column", "at": {"tx": 10, "ty": 12},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_c", "sprite": "solarium_column", "at": {"tx": 20, "ty": 21},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_fallen_a", "sprite": "solarium_column_fallen",
     "at": {"tx": 4, "ty": 21}, "w": 3, "h": 1},
    {"id": "column_fallen_b", "sprite": "solarium_column_fallen",
     "at": {"tx": 17, "ty": 22}, "w": 3, "h": 1},
    {"id": "column_fallen_c", "sprite": "solarium_column_fallen",
     "at": {"tx": 4, "ty": 30}, "w": 3, "h": 1},
    # lamp posts beside (never on) the walked lanes (trunks land at ty+2)
    {"id": "lamp_garden", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 10, "ty": 9}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_stage", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 18, "ty": 9}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_exit", "sprite": "tinderwick_lamp_post",
     "at": {"tx": 3, "ty": 29}, "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- warps (graph.ts edge ids verbatim) ---------------------------------------------
m["warps"] += [
    # EAST <-> hushfrost_pass_ii (the W1 handshake; UNGATED)
    {"id": "to_pass_ii", "at": {"tx": 30, "ty": 8}, "trigger": "step_on",
     "to_map": "hushfrost_pass_ii", "to": {"tx": 1, "ty": 8}, "facing": "right",
     "transition": "fade"},
    {"id": "to_pass_ii_s", "at": {"tx": 30, "ty": 9}, "trigger": "step_on",
     "to_map": "hushfrost_pass_ii", "to": {"tx": 1, "ty": 9}, "facing": "right",
     "transition": "fade"},
    # WEST -> sunvault_climb_i (`to_climb`, UNGATED — the lower terraces need
    # no Gift; the I->II boundary is what Sunsketch gates)
    {"id": "to_climb", "at": {"tx": 0, "ty": 28}, "trigger": "step_on",
     "to_map": "sunvault_climb_i", "to": {"tx": 28, "ty": 14}, "facing": "left",
     "transition": "fade"},
    {"id": "to_climb_s", "at": {"tx": 0, "ty": 29}, "trigger": "step_on",
     "to_map": "sunvault_climb_i", "to": {"tx": 28, "ty": 15}, "facing": "left",
     "transition": "fade"},
]

# ---- encounters (band 42-46; the 24 designed rows split dry/flooded) ----------------
# DRY OUTER (the garden bands + patches): the young roster, 42-44
TABLE_DRY = [
    {"kin_id": 105, "weight": 18, "min_level": 42, "max_level": 44},  # Snoozlet
    {"kin_id": 111, "weight": 16, "min_level": 42, "max_level": 44},  # Spirlet
    {"kin_id": 103, "weight": 14, "min_level": 42, "max_level": 44},  # Gilpaw
    {"kin_id": 114, "weight": 14, "min_level": 42, "max_level": 44},  # Sunsprout
    {"kin_id": 117, "weight": 10, "min_level": 42, "max_level": 45},  # Helibud
    {"kin_id": 120, "weight": 8, "min_level": 43, "max_level": 45},   # Dawnfawn
    {"kin_id": 124, "weight": 7, "min_level": 43, "max_level": 45},   # Petalune
    {"kin_id": 126, "weight": 7, "min_level": 43, "max_level": 45},   # Lunveil
    {"kin_id": 106, "weight": 4, "min_level": 44, "max_level": 46},   # Drowshorn
    {"kin_id": 121, "weight": 2, "min_level": 44, "max_level": 46},   # Sunstag
]
# DRY INNER (the west/east garden patches): the kindled roster bleeds in, 43-46
TABLE_DRY_INNER = [
    {"kin_id": 114, "weight": 16, "min_level": 43, "max_level": 45},
    {"kin_id": 117, "weight": 14, "min_level": 43, "max_level": 46},
    {"kin_id": 120, "weight": 12, "min_level": 43, "max_level": 46},
    {"kin_id": 124, "weight": 10, "min_level": 43, "max_level": 46},
    {"kin_id": 126, "weight": 10, "min_level": 43, "max_level": 46},
    {"kin_id": 115, "weight": 8, "min_level": 44, "max_level": 46},   # Solvyne
    {"kin_id": 118, "weight": 8, "min_level": 44, "max_level": 46},   # Helicore
    {"kin_id": 104, "weight": 6, "min_level": 45, "max_level": 46},   # Goldmane
    {"kin_id": 125, "weight": 6, "min_level": 44, "max_level": 46},   # Crystalune
    {"kin_id": 116, "weight": 4, "min_level": 45, "max_level": 46},   # Auravane
    {"kin_id": 121, "weight": 3, "min_level": 45, "max_level": 46},   # Sunstag
    {"kin_id": 127, "weight": 3, "min_level": 45, "max_level": 46},   # Lunvane
]
# THE FLOODED HALLS (sunpool, Tidecall held): the drowned-light roster, 43-46
TABLE_WATER = [
    {"kin_id": 108, "weight": 26, "min_level": 43, "max_level": 45},  # Solunet
    {"kin_id": 122, "weight": 22, "min_level": 43, "max_level": 46},  # Solray
    {"kin_id": 109, "weight": 16, "min_level": 44, "max_level": 46},  # Tidalune
    {"kin_id": 112, "weight": 12, "min_level": 44, "max_level": 46},  # Nightwraith
    {"kin_id": 110, "weight": 7, "min_level": 45, "max_level": 46},   # Lunaquell
    {"kin_id": 113, "weight": 6, "min_level": 45, "max_level": 46},   # Omenire
    {"kin_id": 107, "weight": 6, "min_level": 45, "max_level": 46},   # Lunarbel
    {"kin_id": 123, "weight": 5, "min_level": 45, "max_level": 46},   # Solreach
]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if goldtuft[i]:
        (band_grid if (i // W) in (10, 11, 26, 27) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE_DRY_INNER,
                                      id_prefix="garden")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE_DRY,
                                      id_prefix="crossing")
m["encounters"] += pt.zones_from_grid(pool, W, H, terrain="water",
                                      rate=0.07, table=TABLE_WATER,
                                      id_prefix="halls")
for z in m["encounters"]:
    if z["id"].startswith("halls"):
        z["requires_ability"] = "tidecall"     # hooks verbatim (belt + braces:
                                               # the sunpool tiles gate anyway)

# ---- garden dressing: gold blooms + boulders (gold ground has no green scatter) ----
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (cliff, ruin, pool, goldtuft))}
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
        if base[i] in (gg[0], gg[1], gg[2], gg[3]) and deco[i] == 0 \
                and (x, y) not in avoid and rng.random() < 0.13:
            deco[i] = rng.choice(blooms) if rng.random() < 0.3 else gid("boulder") \
                if rng.random() < 0.25 else rng.choice(blooms)
for (x, y) in [(18, 4), (2, 11), (22, 15), (10, 31), (20, 30), (3, 20)]:
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
