#!/usr/bin/env python3
"""
Coldfog Marches I — the blighted marsh (walkthrough/04-west "OUTER DETOUR —
Coldfog Marches I → II" beat 1; kind route, region outer, band 46-48, the
shallower half of the ~46-50 detour).

THE DREAD REGISTER (binding — README §0 rule 2 + §10, 04-west Arc D): the one
DRAINED area in Vesperholm. Desaturated, quiet, no festival warmth, ZERO
humour anywhere on this map. It stays dark regardless of Gleam-count, and the
vesperlamp's Lamplight does NOT push the fog back (spine §5 caveat) — its
secrets lean on Emberward/Tidecall, never on brightness. The Hollowing here is
grief dressed as mercy: nothing burnt, nothing broken — lanterns turned down,
lantern by lantern, and kin asleep, never harmed.

Three signature touches (§8):
  1. THE ROAD THAT FORGETS — the crossroads' warm lane (grass fringe, real
     path tiles) dissolves at the blight line; north of it NO lane survives.
     The old road is remembered only by its dark reed-lanterns and one snuffed
     wayshrine, marching into the fog. (Context-correct families: `path`
     transitions to grass, so the path family simply ENDS where the grass
     does — the seam is the story.)
  2. THE WITHERED GOLD PATCH (east edge) — one dying echo of the Solarium's
     stored daylight: a fading goldgrass pocket whose bed carries the lone
     Light-kin exception (Wisprestored, weight 5 — atlas §4: Light-kin
     thinned/absent in drained areas; the row's habitat demands a coldfog
     placement, so it survives ONLY here, barely).
  3. THE BRAVEST VIEWPOINT (NE bluff) — X3 "Charting the Dark"'s optional
     third star-reading: a survey cairn on a scree-lipped bluff over the deep
     fog. The §11 elevation accent, the §3a r1 loop (climb the long way west,
     hop the scree ledge home), and the quest anchor in one.

HANDSHAKE (vesper_crossroads, ALREADY BUILT — verified, no crossroads edit
needed): crossroads' `to_marsh`/`to_marsh_e` at (9,0)/(10,0) land HERE at
(8,28) (both, facing up) — our south opening is exactly (8,29)/(9,29), so the
landing sits within 1 of the return pair. Our `to_crossroads`/`to_crossroads_e`
land at crossroads (9,1)/(10,1), each within 1 of its to_marsh tile. Ungated
both ways (graph.ts:236).
HANDSHAKE (W3-internal): our `to_marsh_ii` at (8,0)/(9,0) (Emberward, held —
blocked_ref sign.coldfog_boundary, the sincere gate) lands at
coldfog_marches_ii (24,24)/(25,24), within 1 of II's return pair `to_marsh_i`
at (24,25)/(25,25), which lands back at our (8,1)/(9,1).

X3 CONTRACT (binding with W2/W4): W4's junior-watcher giver sets
flag:q_west_chart; our cairn trigger requires it, runs script.chart_coldfog
and sets flag:q_west_chart_3 (the OPTIONAL "bravest" leg — W4's done-stage
must not hard-require _3, or must call it out; hooks list this leg as
optional). Mirrors sunvault_climb_ii's chart_sunvault trigger verbatim.

(SUPERSEDED 2026-10 by walkthrough/11 Part E: two Hollowing acolytes now keep this road — see the density block below.) NO TRAINERS (deliberate §11 r7 deviation, documented): the walkthrough's
Coldfog hooks name zero trainers — nobody keeps a road through a drained
land; the dread register would not survive a cheery route battle. The
mandatory blight-bed crossing (rows 12-13, full corridor) keeps the route
from being a free pass; the §3a r9 geometry beat is carried by the terrain.

NO REST POINT either (see build_coldfog_marches_ii.py's note — §2b r5
justified: optional late detour, the Crossroads inn sits 2 short legs back).

Encounter reconciliation (the W2 precedent: built map wins; the 11 designed
"coldfog_marches" species rows split I/II by band — wiring agent mirrors into
EXTRA_ENCOUNTERS, tools/balance/build_species.py):
  I (band 46-48, this map): #136 Mothdim (Dark, common), #133 Flutterwane
    (Dark/Light, uncommon), #137 Nullmoth (Dark), #134 Wispwane (Dark/Light),
    #141 Cindersob (Dark/Ember — the ashen ex-Ember read, foreshadowed at
    Hushfrost's blight fingers).
  GOLD patch bed: Mothdim/Flutterwane + #140 Wisprestored (pure Light) at
    weight 5 — the atlas §4 numbed exception; everywhere else Light is absent.
  (II takes the deeper six — see its builder; Drownlight takes the rare Dark
   bed with #138 Voidmantle + #135 Liminalux; the Stillworks takes #143
   Whorlix, the Storm/Dark "charged husk".)
Murk shallows carry NO encounter zone at all — the water is DEAD (no foam,
no life, no animation: gbaforge murk is drawn still by design).

Suggested sign copy (wiring agent; sincere, elegiac, zero humour):
  sign.coldfog_marches   "COLDFOG MARCHES. The lamps here have been put to
                          sleep. Travellers are asked to let them rest."
  sign.coldfog_boundary  "Deep coldfog past this stone. No ordinary flame
                          keeps. A warded ember walks where the fog is
                          thickest." (also the I<->II warps' blocked_ref)
  npc.coldfog_marsh_hermit (hooks VERBATIM flavour): "They didn't burn it.
    They didn't break it. They just... turned the light down, lantern by
    lantern, until the whole fen forgot it was ever lit. Kindest thing, they
    said. Kindest thing."
  script.chart_coldfog   (X3 leg 3 — a star-reading over the one place the
                          sky gives nothing back; sets flag:q_west_chart_3)

audit_flow notes — the gold-patch pocket and the murk islet are paid dead
ends (§3a r4: the Light bed; the valuable cache); the bluff ledge is the
one-way return (§3a r1/r2). Murk-gated content is priced on Tidecall (held
long since).

Run:  ./venv/bin/python tools/maps/build_coldfog_marches_i.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 30
rng = random.Random(76)
owed: list[str] = []

# the COLDFOG accent set (build_coldfog_set.py): `fogcrag` = the cliff family
# with BLIGHT-context rims — the shared `cliff` would ring teal-green here
COLDFOG_REF = mk.register_tileset(
    "coldfog_set", index=mk.REPO / "assets/tilesets/coldfog/coldfog_set.index.json")

# ---- terrain presence grids --------------------------------------------------------
cliff = mk.make_grid(W, H)      # the map-edge walls + the bluff
tree = mk.make_grid(W, H)       # the LIVING south fringe's wood (the seam)
murk = mk.make_grid(W, H)       # dead-still shallows (Tidecall-gated, lifeless)
blighttuft = mk.make_grid(W, H) # the drained encounter beds
goldtuft = mk.make_grid(W, H)   # the withered gold bed (the Light exception)
path = mk.make_grid(W, H)       # the lane — FRINGE ONLY (the road that forgets)
deco = mk.make_grid(W, H)

# BORDERS: grey stone crags N/W/E (2 deep, organic bumps §11 r2); the south
# border is the LIVING tree-line (the crossroads seam, §2b r6)
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.rect(cliff, W, H, 0, 0, 1, H - 1)
mk.rect(cliff, W, H, 18, 0, 19, H - 1)
mk.organic_border(cliff, W, H, depth=0,
                  bumps=[(1, 6, 2), (1, 16, 2), (1, 23, 2), (18, 12, 2),
                         (18, 22, 2), (5, 1, 2), (14, 1, 2)],
                  rng=rng)
mk.rect(tree, W, H, 0, 27, W - 1, H - 1)
mk.organic_border(tree, W, H, depth=0,
                  bumps=[(3, 27, 2), (15, 27, 2)], rng=rng)
# SOUTH gap — down to Marches II (2026-10 geometry fix: the marshes hang off
# Nightreach, so this green hollow — the one pocket the fog never reached — is
# entered from the deep marsh BELOW it, not from the Crossroads)
for (x, y) in [(8, 27), (9, 27), (8, 28), (9, 28), (8, 29), (9, 29)]:
    tree[y * W + x] = 0
# the old road NORTH is lost in the fog now (the north gap stays shut — the
# dead reed-lanterns march up to the fog wall and stop); the Drownlight Beacon
# spur opens off the WEST flank instead (rows 4-5)
for y in (4, 5):
    for x in (0, 1, 2, 3):
        cliff[y * W + x] = 0
# THE HOLLOWING'S COUNTRY (walkthrough/11 Part E, 2026-10): the old road north
# was never lost — it was LED. The north gap opens at cols 4-7 (world x 52-55) up
# to Stillwater, the Hollowing's village; the east flank opens at rows 11-14
# (world y -450..-447) onto the Mourning Fields (Lane N3's map: the engine no-ops
# those warps until it lands). Both seams are this lane's (N1) per the contract.
for y in range(0, 4):
    for x in (4, 5, 6, 7):
        cliff[y * W + x] = 0
for y in range(11, 15):
    for x in (16, 17, 18, 19):
        cliff[y * W + x] = 0

# THE BLUFF (NE) — X3's bravest viewpoint: cliff rim, scree ledge lip, west climb
BLUFF = pt.Area(11, 3, 17, 9)
pt.terrace(cliff, deco, W, H, BLUFF, gap=(5, 6), gap_side="left", rng=rng)
# the terrace's south lip in the SCREE register (grey — green ledges would lie
# on drained ground); re-stamp over what terrace() placed
pt.ledge_run(deco, W, H, BLUFF.y1, BLUFF.x0 + 2, BLUFF.x1 - 2, rng, family="scree")

# ---- the dead shallows (murk — water-over-blight, NO life, NO zone) ----------------
mk.blob(murk, W, H, 5.0, 18.5, 3.0, 2.2)               # west pool
mk.blob(murk, W, H, 2.9, 20.4, 1.2, 0.8)               #  (R10: ragged lobes — never a
mk.blob(murk, W, H, 7.0, 16.6, 1.0, 0.7)               #   ruled box, audit_visual)
mk.blob(murk, W, H, 14.5, 17.5, 2.8, 1.9)              # east pool (the islet cache)
mk.blob(murk, W, H, 12.4, 18.7, 0.9, 0.7)
mk.blob(murk, W, H, 4.5, 8.5, 2.6, 2.0)                # north-west pool
mk.blob(murk, W, H, 6.6, 9.8, 1.1, 0.7)
mk.blob(murk, W, H, 12.5, 22.5, 1.7, 1.2)              # fringe-line pool
# the islet (dry ground under the valuable cache — priced on Tidecall)
for (x, y) in [(14, 17), (15, 17)]:
    murk[y * W + x] = 0

# ---- the lane: fringe only (it ENDS at the blight line — touch #1) ------------------
mk.vline(path, W, H, 8, 23, 29)
mk.vline(path, W, H, 9, 23, 29)
mk.rect(path, W, H, 7, 24, 8, 24)                      # one last tired jog
# (north of row 23 the road is gone — reed-lanterns remember it instead)

# ---- encounter terrain ---------------------------------------------------------------
# the MANDATORY crossing (§11 r7): full corridor, rows 12-13 (no lane to pause —
# the road itself is gone; the fog bed IS the road)
mk.rect(blighttuft, W, H, 2, 12, 17, 13)
# R10: a wind-cut, ragged edge (not a ruled bar) — the corridor stays fully banded
for (x, y) in []:  # (no additions: a row-classified band must not grow into the beds)
    blighttuft[y * W + x] = 1
for (x, y) in [(2, 13), (17, 12), (6, 12), (10, 13), (14, 12)]:  # notches only
    blighttuft[y * W + x] = 0
# optional beds: south of the crossing + under the bluff
mk.blob(blighttuft, W, H, 13.0, 21.0, 2.4, 1.4)
mk.blob(blighttuft, W, H, 6.0, 14.5, 2.0, 1.3)
mk.blob(blighttuft, W, H, 13.5, 10.5, 1.8, 1.1)
# the withered gold patch (east edge; the bed inside it)
gold = mk.make_grid(W, H)
mk.blob(gold, W, H, 16.5, 19.0, 2.4, 1.9)
mk.blob(gold, W, H, 17.5, 21.0, 1.5, 1.2)
mk.blob(goldtuft, W, H, 16.5, 19.0, 1.4, 1.0)

# ---- the blight mask: everything north of the living fringe -------------------------
blight = mk.make_grid(W, H)
mk.rect(blight, W, H, 0, 0, W - 1, 23)
# the blight BITES into the fringe (organic seam, §11 r4 — never a ruled line)
mk.blob(blight, W, H, 4.0, 24.5, 2.6, 1.5)
mk.blob(blight, W, H, 12.5, 24.0, 2.2, 1.3)
mk.blob(blight, W, H, 17.0, 24.5, 1.8, 1.2)

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if cliff[i] or tree[i]:
        for g in (murk, blighttuft, goldtuft, path, gold):
            g[i] = 0
    if murk[i]:
        blighttuft[i] = 0
        goldtuft[i] = 0
        path[i] = 0
    if path[i]:
        blighttuft[i] = 0
        goldtuft[i] = 0
    if goldtuft[i] or gold[i]:
        blighttuft[i] = 0

# ---- base: blight north, living grass fringe south, the gold echo east --------------
gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = mk.make_grid(W, H)
for i in range(W * H):
    if gold[i]:
        base[i] = rng.choice(gg) if rng.random() < 0.55 else gg[0]
    elif blight[i]:
        base[i] = rng.choice(bl) if rng.random() < 0.55 else bl[0]
    else:
        base[i] = rng.choice(gr) if rng.random() < 0.5 else gr[0]

terrain_layers = [
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": blighttuft},
    {"name": "t_goldtuft", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": goldtuft},
    {"name": "t_murk", "role": "terrain", "terrain": "murk",
     "set": "vesper_overworld_set", "depth": 0, "data": murk},
    {"name": "t_fogcrag", "role": "terrain", "terrain": "fogcrag",
     "set": "coldfog_set", "depth": 0, "data": cliff},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]

m: dict = {
    "id": "coldfog_marches_i", "display_name": "Coldfog Marches",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref(), COLDFOG_REF],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/coldfog-marches-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/coldfog-marches-a.webp",
        "assets/backgrounds/battle/coldfog-marches-b.webp",
    ],
}

# ---- warps (graph.ts edge ids verbatim) ---------------------------------------------
m["warps"] += [
    # SOUTH <-> coldfog_marches_ii (`to_marsh_ii`, Emberward HELD both ways —
    # the deep-fog boundary; the sign states the why, §3a r8)
    {"id": "to_marsh_ii", "at": {"tx": 8, "ty": 29}, "trigger": "step_on",
     "to_map": "coldfog_marches_ii", "to": {"tx": 24, "ty": 1}, "facing": "down",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_boundary", "transition": "fade"},
    {"id": "to_marsh_ii_e", "at": {"tx": 9, "ty": 29}, "trigger": "step_on",
     "to_map": "coldfog_marches_ii", "to": {"tx": 25, "ty": 1}, "facing": "down",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_boundary", "transition": "fade"},
    # WEST high <-> drownlight_beacon (`to_beacon`, Emberward — the Dark spur)
    {"id": "to_beacon", "at": {"tx": 0, "ty": 4}, "trigger": "step_on",
     "to_map": "drownlight_beacon", "to": {"tx": 16, "ty": 7}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_beacon", "transition": "fade"},
    {"id": "to_beacon_s", "at": {"tx": 0, "ty": 5}, "trigger": "step_on",
     "to_map": "drownlight_beacon", "to": {"tx": 16, "ty": 8}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_beacon", "transition": "fade"},
]

# ---- the Hollowing's Country seams (walkthrough/11 build contract) ------------------
for x in (4, 5, 6, 7):
    m["warps"].append({"id": f"to_stillwater_{x}", "at": {"tx": x, "ty": 0},
                       "trigger": "step_on", "to_map": "stillwater",
                       "to": {"tx": x, "ty": 28}, "facing": "up", "transition": "fade"})
for y in (11, 12, 13, 14):
    m["warps"].append({"id": f"to_mourning_{y}", "at": {"tx": W - 1, "ty": y},
                       "trigger": "step_on", "to_map": "mourning_fields",
                       "to": {"tx": 1, "ty": y}, "facing": "right", "transition": "fade"})

# ---- the road that forgets: dark reed-lanterns remember the lane --------------------
for n, (x, y) in enumerate([(7, 20), (10, 16), (7, 10), (10, 5)]):
    m["objects"].append(
        {"id": f"dead_lantern_{n}", "sprite": "saltreach_reed_lantern_dark",
         "at": {"tx": x, "ty": y}, "w": 1, "h": 2, "overhang": 1,
         "walk_under": True})
# one snuffed wayshrine where the road finally gives up
m["objects"].append(
    {"id": "wayshrine_null", "sprite": "glowmoss_deep_null_lantern_shrine",
     "at": {"tx": 11, "ty": 18}, "w": 2, "h": 3, "overhang": 2})

# ---- R10: DESOLATION, AUTHORED (world-craft panel §4 #5) -------------------------
# Not empty — emptied. What the drained marsh lost is left where it was put
# down: a table laid for three in a cottage with no walls, a boat pulled up
# out of water that no longer moves, doused lamp-posts that take your flame for
# a breath and gutter (Coldfog resists Lamplight — saying so makes it felt),
# the Hollowing's gentle notice, a willow that has forgotten what green was.
# Every one is optional colour: interacts only, nothing gates.
m["objects"] += [
    {"id": "set_table", "sprite": "coldfog_set_table", "at": {"tx": 2, "ty": 21},
     "w": 4, "h": 3},
    {"id": "beached_boat", "sprite": "coldfog_beached_boat", "at": {"tx": 2, "ty": 15},
     "w": 3, "h": 2},
    {"id": "doused_lamp_a", "sprite": "coldfog_doused_lamp", "at": {"tx": 8, "ty": 14},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "doused_lamp_b", "sprite": "coldfog_doused_lamp", "at": {"tx": 16, "ty": 7},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "quiet_notice", "sprite": "coldfog_hollowing_notice", "at": {"tx": 11, "ty": 21},
     "w": 1, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "drained_willow", "sprite": "coldfog_dead_willow", "at": {"tx": 15, "ty": 23},
     "w": 3, "h": 4, "overhang": 2, "walk_under": True},
]
m["triggers"] += [
    {"id": "set_table_read", "kind": "script", "at": {"tx": 3, "ty": 23},
     "activation": "interact", "ref": "script.coldfog_set_table"},
    {"id": "set_table_read_b", "kind": "script", "at": {"tx": 4, "ty": 23},
     "activation": "interact", "ref": "script.coldfog_set_table"},
    {"id": "boat_read", "kind": "script", "at": {"tx": 3, "ty": 16},
     "activation": "interact", "ref": "script.coldfog_boat"},
    {"id": "doused_lamp_a_relight", "kind": "script", "at": {"tx": 8, "ty": 16},
     "activation": "interact", "ref": "script.coldfog_relight"},
    {"id": "doused_lamp_b_relight", "kind": "script", "at": {"tx": 16, "ty": 9},
     "activation": "interact", "ref": "script.coldfog_relight"},
    {"id": "quiet_notice_read", "kind": "script", "at": {"tx": 11, "ty": 22},
     "activation": "interact", "ref": "script.coldfog_notice"},
]
# the one living voice on the fringe: a hollow-eyed villager who walks the
# blight line and answers in half-sentences (gone home at dawn)
m["npcs"].append(
    {"id": "hollow_villager", "at": {"tx": 13, "ty": 25}, "facing": "left",
     "sprite": "fen_folk", "movement": "wander", "wander_radius": 2,
     "dialogue_ref": "script.coldfog_villager", "hidden_when_flag": "flag:dawn"})

# ---- the bravest viewpoint (X3 leg 3 — the survey cairn on the bluff) ---------------
m["objects"].append(
    {"id": "chart_cairn", "sprite": "windward_cairn",
     "at": {"tx": 14, "ty": 5}, "w": 2, "h": 3, "overhang": 1})
m["triggers"].append(
    {"id": "chart_coldfog", "kind": "script", "at": {"tx": 14, "ty": 7},
     "activation": "interact", "ref": "script.chart_coldfog", "once": True,
     "requires_flag": "flag:q_west_chart",
     "sets_flags": ["flag:q_west_chart_3"],
     "hidden_when_flag": "flag:q_west_chart_3"})
owed += ["script.chart_coldfog (X3 leg 3, OPTIONAL/bravest — a star-reading "
         "over the one sky that gives nothing back; sets flag:q_west_chart_3; "
         "W4's done-stage must treat _3 as the optional leg)"]

# ---- the marsh-hermit (hooks: npc.coldfog_marsh_hermit, at the works' edge) ---------
# Posted at the deep-fog boundary — the last living voice before the works'
# drained country; his line is the B4 entry-tone (grief dressed as mercy).
m["npcs"].append(
    {"id": "marsh_hermit", "at": {"tx": 9, "ty": 3}, "facing": "left",
     "sprite": "npc_old_man", "movement": "static",
     "dialogue_ref": "npc.coldfog_marsh_hermit"})
owed += ["npc.coldfog_marsh_hermit (hooks ref VERBATIM — the 'kindest thing' "
         "line; zero humour)"]

# ---- the Hollowing's Country density (walkthrough/11 Part E) ------------------------
# Two acolytes keep the road north (sight trainers, keeper class — they ask first,
# in their scripts); a Stillwater trader at the north gap (the marsh has no rest,
# so she sells what the road needs); an elegiac fen-walker on the living fringe;
# the first of the Shutter-wall's three cold lamps; Tessaly's first escort stop;
# and a Lamplight-STARLIGHT secret: the one nook bright enough lamplight can find.
owed += pt.trainer_beat(m, tid="coldfog_acolyte_north", at=(10, 8), facing="down",
                        sight=4, sprite="hollowing_acolyte")
owed += pt.trainer_beat(m, tid="coldfog_acolyte_east", at=(16, 14), facing="left",
                        sight=4, sprite="hollowing_elder")
m["npcs"] += [
    {"id": "still_trader", "at": {"tx": 10, "ty": 3}, "facing": "left",
     "sprite": "market_trader", "movement": "static",
     "dialogue_ref": "script.still_trader"},
    {"id": "fen_walker", "at": {"tx": 8, "ty": 24}, "facing": "down",
     "sprite": "pass_walker", "movement": "wander", "wander_radius": 2,
     "dialogue_ref": "script.coldfog_fen_walker"},
    {"id": "tessaly_fog1", "at": {"tx": 7, "ty": 22}, "facing": "down",
     "sprite": "fen_folk", "movement": "static", "dialogue_ref": "script.still_tessaly_fog1",
     "requires_flag": "flag:q_still_tessaly", "hidden_when_flag": "flag:q_still_tessaly_fog1"},
    {"id": "cache_coldfog_starlight", "at": {"tx": 2, "ty": 19}, "facing": "down",
     "sprite": "item_cache", "movement": "static",
     "dialogue_ref": "script.pickup_coldfog_starlight",
     "requires_flag": "flag:lamplight_starlight",
     "hidden_when_flag": "flag:picked_coldfog_starlight"},
]
m["objects"].append(
    {"id": "named_lamp_1", "sprite": "coldfog_doused_lamp", "at": {"tx": 16, "ty": 18},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True})
m["triggers"].append(
    {"id": "named_lamp_1_read", "kind": "script", "at": {"tx": 15, "ty": 20},
     "activation": "interact", "ref": "script.still_coldlamp_1"})
owed += ["script.still_trader", "script.coldfog_fen_walker", "script.still_tessaly_fog1",
         "script.pickup_coldfog_starlight", "script.still_coldlamp_1"]

# ---- signs --------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="coldfog_marches", at=(10, 24))   # the blight line
owed += pt.sign(m, deco, W, sid="coldfog_boundary", at=(10, 25))
owed += pt.sign(m, deco, W, sid="coldfog_beacon", at=(2, 3))      # the beacon spur's why (west gap)  # the sincere gate (down to the deep marsh)
# (sign.coldfog_boundary doubles as the to_marsh_ii warps' blocked_ref)

# ---- caches (variety rule: one consumable off-lane, the valuable behind murk) -------
owed += pt.cache(m, cid="coldfog_embergloss", at=(4, 25))     # consumable, fringe wood
owed += pt.cache(m, cid="coldfog_murk_pearl", at=(15, 17))    # valuable, the dead islet
                                                              # (Tidecall-priced, §3a r4)

# ---- encounters (band 46-48; murk carries NOTHING — the water is dead) --------------
# 2026-10 (Part A review): at 46+ every line wears its KINDLED form (Mothdim/
# Nullmoth -> Voidmantle, Flutterwane/Wispwane -> Liminalux, Cindersob -> Embergone);
# the base forms survive only in the gold pocket, below their kindling levels.
TABLE_I = [
    {"kin_id": 138, "weight": 30, "min_level": 46, "max_level": 48},  # Voidmantle
    {"kin_id": 135, "weight": 26, "min_level": 46, "max_level": 48},  # Liminalux
    {"kin_id": 113, "weight": 16, "min_level": 47, "max_level": 48},  # Omenire
    {"kin_id": 142, "weight": 14, "min_level": 46, "max_level": 48},  # Embergone
    {"kin_id": 180, "weight": 14, "min_level": 46, "max_level": 48},  # Lullwing, down from the village
]
TABLE_GOLD = [
    # the one patch the fog never drained: the YOUNG still hatch here, kept small
    {"kin_id": 133, "weight": 38, "min_level": 19, "max_level": 21},  # Flutterwane (kindles 22)
    {"kin_id": 136, "weight": 37, "min_level": 17, "max_level": 19},  # Mothdim (kindles 20)
    {"kin_id": 140, "weight": 5, "min_level": 47, "max_level": 48},   # Wisprestored —
    # the LONE Light exception (w<=5): the Solarium's dying echo, only here
]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if blighttuft[i]:
        (band_grid if (i // W) in (12, 13) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE_I, id_prefix="crossing")
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE_I, id_prefix="bed")
m["encounters"] += pt.zones_from_grid(goldtuft, W, H, terrain="tall_grass",
                                      rate=0.12, table=TABLE_GOLD, id_prefix="gold")

# ---- drained dressing: grey moss creeping, listless pebbles -------------------------
for (x, y, n) in [(3, 21, "greymoss_a"), (7, 17, "greymoss_b"), (12, 19, "greymoss_a"),
                  (16, 16, "greymoss_b"), (4, 11, "greymoss_b"), (11, 11, "greymoss_a"),
                  (6, 6, "greymoss_a"), (12, 3, "greymoss_b"), (16, 11, "greymoss_a"),
                  (3, 15, "greymoss_b")]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid(n)
for (x, y) in [(5, 22), (10, 19), (3, 13), (15, 15), (6, 9), (11, 9), (16, 22),
               (13, 24), (4, 5)]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid("g_pebble")
for (x, y) in [(4, 16), (12, 8), (16, 13), (5, 25), (14, 23)]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid("boulder")

# R10: the drained ground keeps its litter — grey moss and loose stones scattered
# (seeded, off every structure) so the blight reads as weathered, not blank.
_busy = {(x, y) for y in range(H) for x in range(W)
         if any(g[y * W + x] for g in (cliff, tree, murk, blighttuft, goldtuft, path, gold))}
_busy |= {(x, y) for o in m["objects"]
          for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
          for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
_busy |= {(p["at"]["tx"], p["at"]["ty"]) for p in m["npcs"] + m["triggers"] + m["warps"]}
_litter = [gid("greymoss_a"), gid("greymoss_b"), gid("g_pebble")]
for y in range(2, 24):
    for x in range(2, 18):
        if (x, y) not in _busy and deco[y * W + x] == 0 and rng.random() < 0.10:
            deco[y * W + x] = rng.choice(_litter)

# ---- scatter on the LIVING fringe only (grass cells; the blight stays drab) ---------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (cliff, tree, murk, blighttuft, goldtuft,
                                         path, blight, gold))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
mk.scatter_decor(deco, base, W, H, rng, density=0.15, avoid=avoid)

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
