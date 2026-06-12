#!/usr/bin/env python3
"""
Coldfog Marches II — deep coldfog (walkthrough/04-west "OUTER DETOUR" beat 3;
kind route, region outer, band 48-50, the drained heart of the marsh).

THE DREAD REGISTER, DEEPER (README §0 r2 + §10, atlas §4, Arc D): the drained
country itself — snuffed lanterns in rows, dead-still murk, ashen ex-Ember
kin. ZERO humour. NO living NPC walks this map: the only voices are a sign
the Hollowing posted, a camp nobody hurried away from, and the works' sealed
door. It does not lighten with Gleam-count; Lamplight does not bite here.

Three signature touches (§8):
  1. THE TENDED ROW — null-lantern racks and snuffed wayshrines flank the
     works' forecourt in clean, swept lines. Nothing is broken; everything is
     ASLEEP. (B4 shown-half staging: industry as mercy, never menace.)
  2. THE QUIETED CAMP — a wardens' camp with bedrolls rolled square, the
     fire-ring doused and swept, a hand-lantern set out neat. An interact
     line, no body, no struggle (kin and keepers alike just... went quiet).
  3. THE STILLED POND — a perfect small murk circle ringed in grey moss by
     the bank. Water that has stopped saying anything.

NO REST POINT (deliberate §2b r5 deviation, documented): the dread register
is the point — Coldfog is optional, late, and entered from the hub; the
Crossroads inn is 2 short legs back (I is one screen south of it). A heal
here would tell the player the fen is safe. It must not feel safe; it must
feel ASLEEP.
NO TRAINERS (the I-side note applies — hooks name zero; the §11 r7 gameplay
load is carried by the full-corridor blight crossing + the murk-priced finds).

HANDSHAKE (W3-internal, built both sides): I's `to_marsh_ii` at (8,0)/(9,0)
lands HERE at (24,24)/(25,24); our return pair `to_marsh_i` at (24,25)/(25,25)
lands at I's (8,1)/(9,1) — both directions Emberward (the deep fog is the
boundary; graph.ts:209), blocked_ref sign.coldfog_boundary.
HANDSHAKE (W3-internal, beacon): our `to_beacon` at (0,12)/(0,13) (Emberward,
graph.ts:226) lands at drownlight_beacon (16,7)/(16,8) ON its return pair
`to_marches` at (17,7)/(17,8), which lands back at our (1,12)/(1,13).
HANDSHAKE (W3-internal, stillworks): the works' DOOR — `to_stillworks` /
`to_stillworks_e` at (14,6)/(15,6) (step_on, transition door, on the facade's
visible double door), **requires_ability: glimmerstep** (the inner door,
graph.ts:227 — Emberward got you here at all), blocked_ref
npc.hollowfen_door. Lands at hollowfen_stillworks (11,19)/(12,19) ON its
return pair, which lands back at our (14,7)/(15,7) (the doorstep).
HANDSHAKE (W4, binding on the Nightreach builder): our `to_observatory_fog`
at (0,3)/(0,4) (Emberward both ways, graph.ts:210 — the back-door, NOT the
main path, spine §0 rule 2) lands at nightreach_observatory (28,14)/(28,15)
facing left — PLACEHOLDER until W4 authors it (the engine no-ops; same
contract style as W1's to_solarium). W4's map must be >=29 wide, keep those
east-edge landings WALKABLE, gate its side of the pair on Emberward, and its
return pair must land at our (1,3)/(1,4).

Encounter reconciliation (the W2 precedent — built map wins; the deeper six
of the 11 designed "coldfog_marches" rows; wiring agent mirrors into
EXTRA_ENCOUNTERS): #137 Nullmoth, #139 WispwaneNull, #141 Cindersob,
#142 Embergone (the hooks' named ashen ex-Ember), #134 Wispwane,
#138 Voidmantle (low weight here; its true bed is the Drownlight spur).
Light-kin ABSENT entirely on this map (atlas §4 — no gold echo survives this
deep). Murk carries NO encounter zone: the water is dead.

Suggested sign copy (wiring agent; sincere, elegiac, zero humour):
  sign.coldfog_works     "HOLLOWFEN STILLWORKS. Every lamp within is resting.
                          The Wardens of the Quiet ask that you not wake
                          them." (posted by the Hollowing — courteous, awful)
  sign.coldfog_beacon    "WEST — DROWNLIGHT BEACON. The light that kept the
                          fen-road drowned in its own keeping. No keeper
                          answers." (the spur's why + come-back, §3a r8)
  sign.coldfog_backdoor  "NORTH-WEST — NIGHTREACH, BY THE FOG ROAD. Short,
                          dark, and wrong. The stars go the long way round."
                          (the back-door is [MISSABLE] convenience — the main
                          path remains the rim, spine §0 rule 2)
  npc.hollowfen_door     (the works' locked-door line, pre-Glimmerstep): "The
                          seam of the door holds no handle. A thin grey light
                          breathes under it — a gap only a glimmer-step could
                          thread."
  npc.coldfog_quiet_camp "Two bedrolls, rolled square. The fire-ring is swept.
                          A lantern stands where a hand left it, wick cold.
                          Nobody hurried. That is somehow the worst of it."

audit_flow notes — the murk islet and the bank pocket are paid dead ends
(§3a r4); the bank's scree ledge is the one-way return past the crossing
(§3a r1/r2). The camp/backdoor pocket pays with the camp beat + the tonic
cache.

Run:  ./venv/bin/python tools/maps/build_coldfog_marches_ii.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 26
rng = random.Random(77)
owed: list[str] = []

COLDFOG_REF = mk.register_tileset(
    "coldfog_set", index=mk.REPO / "assets/tilesets/coldfog/coldfog_set.index.json")

# ---- terrain presence grids --------------------------------------------------------
crag = mk.make_grid(W, H)       # fogcrag walls (blight-context accent family)
murk = mk.make_grid(W, H)       # dead-still sheets + the stilled pond
blighttuft = mk.make_grid(W, H) # the drained beds
deco = mk.make_grid(W, H)

# BORDERS: fogcrag all round, 2 deep, organic bumps (§11 r2)
mk.rect(crag, W, H, 0, 0, W - 1, 1)
mk.rect(crag, W, H, 0, 24, W - 1, H - 1)
mk.rect(crag, W, H, 0, 0, 1, H - 1)
mk.rect(crag, W, H, 28, 0, 29, H - 1)
mk.organic_border(crag, W, H, depth=0,
                  bumps=[(6, 1, 2), (20, 1, 2), (1, 8, 2), (1, 19, 2),
                         (28, 7, 2), (28, 19, 2), (10, 24, 2), (18, 24, 2)],
                  rng=rng)
# SOUTH gap — the boundary with Marches I (cols 24-25)
for y in (23, 24, 25):
    for x in (24, 25):
        crag[y * W + x] = 0
# WEST gap, low — the Drownlight Beacon spur (rows 12-13)
for x in (0, 1):
    for y in (12, 13):
        crag[y * W + x] = 0
# WEST gap, high — the Nightreach back-door (rows 3-4)
for x in (0, 1):
    for y in (3, 4):
        crag[y * W + x] = 0

# THE EAST SHELF — the one-way return, ANCHORED to the border crag (§11 r8:
# never a free-standing slab mid-field; the hushfrost east-shelf pattern):
# climb in from the north gap by the NE bed, hop the scree ledge back south
# past the crossing (§3a r1/r2; §11 r3 elevation accent)
SHELF = pt.Area(22, 11, 27, 15)
pt.terrace(crag, deco, W, H, SHELF, gap=(24, 25), gap_side="up", rng=rng)
pt.ledge_run(deco, W, H, SHELF.y1, SHELF.x0 + 2, SHELF.x1 - 2, rng, family="scree")

# ---- dead water ---------------------------------------------------------------------
mk.blob(murk, W, H, 20.0, 18.0, 2.6, 1.6)              # the east sheet (islet cache)
mk.blob(murk, W, H, 6.5, 17.0, 3.0, 2.0)               # the west sheet
mk.blob(murk, W, H, 19.5, 9.5, 2.0, 1.7)               # THE STILLED POND (touch #3)
# the islet in the east sheet (dry ground under the wicks cache)
for (x, y) in [(20, 18), (21, 18)]:
    murk[y * W + x] = 0

# ---- encounter terrain --------------------------------------------------------------
# the MANDATORY crossing (§11 r7): rows 21-22 wall to wall — every road north
# from the boundary rolls it (no lane survives this deep to carve out)
mk.rect(blighttuft, W, H, 2, 21, 27, 22)
# optional deeper beds
mk.blob(blighttuft, W, H, 5.5, 5.0, 2.4, 1.6)          # NW, by the back-door
mk.blob(blighttuft, W, H, 23.0, 5.0, 2.6, 1.9)         # NE, off the forecourt
mk.blob(blighttuft, W, H, 17.0, 13.0, 1.8, 1.2)        # by the stilled pond
mk.blob(blighttuft, W, H, 12.5, 11.0, 1.9, 1.2)        # mid-field, by the wayshrine

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if crag[i]:
        murk[i] = 0
        blighttuft[i] = 0
    if murk[i]:
        blighttuft[i] = 0

# ---- base: blight everywhere (the drained heart — no living fringe) ------------------
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
base = [rng.choice(bl) if rng.random() < 0.55 else bl[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": blighttuft},
    {"name": "t_murk", "role": "terrain", "terrain": "murk",
     "set": "vesper_overworld_set", "depth": 0, "data": murk},
    {"name": "t_fogcrag", "role": "terrain", "terrain": "fogcrag",
     "set": "coldfog_set", "depth": 0, "data": crag},
]

m: dict = {
    "id": "coldfog_marches_ii", "display_name": "Coldfog Marches",
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
    # SOUTH <-> coldfog_marches_i (`to_marsh_ii` edge; Emberward both ways)
    {"id": "to_marsh_i", "at": {"tx": 24, "ty": 25}, "trigger": "step_on",
     "to_map": "coldfog_marches_i", "to": {"tx": 8, "ty": 1}, "facing": "down",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_boundary", "transition": "fade"},
    {"id": "to_marsh_i_e", "at": {"tx": 25, "ty": 25}, "trigger": "step_on",
     "to_map": "coldfog_marches_i", "to": {"tx": 9, "ty": 1}, "facing": "down",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_boundary", "transition": "fade"},
    # WEST low <-> drownlight_beacon (`to_beacon`, Emberward — the Dark spur)
    {"id": "to_beacon", "at": {"tx": 0, "ty": 12}, "trigger": "step_on",
     "to_map": "drownlight_beacon", "to": {"tx": 16, "ty": 7}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_beacon", "transition": "fade"},
    {"id": "to_beacon_s", "at": {"tx": 0, "ty": 13}, "trigger": "step_on",
     "to_map": "drownlight_beacon", "to": {"tx": 16, "ty": 8}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_beacon", "transition": "fade"},
    # WEST high -> nightreach_observatory (`to_observatory_fog`, Emberward —
    # the OPTIONAL back-door; placeholder landing, W4 lands it; see HANDSHAKE)
    {"id": "to_observatory_fog", "at": {"tx": 0, "ty": 3}, "trigger": "step_on",
     "to_map": "nightreach_observatory", "to": {"tx": 28, "ty": 14}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_backdoor", "transition": "fade"},
    {"id": "to_observatory_fog_s", "at": {"tx": 0, "ty": 4}, "trigger": "step_on",
     "to_map": "nightreach_observatory", "to": {"tx": 28, "ty": 15}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_backdoor", "transition": "fade"},
]

# ---- THE WORKS (the landmark — B4's shown half, seen before it's entered) ------------
# facade against the north border; its double door carries the Glimmerstep
# warps (level-design §11 r5b: the door tile IS the standable tile; a locked
# door answers a walk-in with its line, never silence)
m["objects"].append(
    {"id": "stillworks_front", "sprite": "coldfog_works_front",
     "at": {"tx": 12, "ty": 2}, "w": 6, "h": 5, "overhang": 2})
m["warps"] += [
    {"id": "to_stillworks", "at": {"tx": 14, "ty": 6}, "trigger": "step_on",
     "to_map": "hollowfen_stillworks", "to": {"tx": 11, "ty": 19}, "facing": "up",
     "requires_ability": "glimmerstep",
     "blocked_ref": "npc.hollowfen_door", "transition": "door"},
    {"id": "to_stillworks_e", "at": {"tx": 15, "ty": 6}, "trigger": "step_on",
     "to_map": "hollowfen_stillworks", "to": {"tx": 12, "ty": 19}, "facing": "up",
     "requires_ability": "glimmerstep",
     "blocked_ref": "npc.hollowfen_door", "transition": "door"},
]
owed += ["npc.hollowfen_door (the works' locked-door line — see docstring)"]

# the TENDED ROW (touch #1): racks + snuffed shrines flanking the forecourt
m["objects"] += [
    {"id": "rack_w", "sprite": "coldfog_null_rack",
     "at": {"tx": 6, "ty": 5}, "w": 4, "h": 2, "overhang": 1},
    {"id": "rack_e", "sprite": "coldfog_null_rack",
     "at": {"tx": 20, "ty": 5}, "w": 4, "h": 2, "overhang": 1},
    {"id": "shrine_road_a", "sprite": "glowmoss_deep_null_lantern_shrine",
     "at": {"tx": 8, "ty": 13}, "w": 2, "h": 3, "overhang": 2},
    {"id": "shrine_road_b", "sprite": "glowmoss_deep_null_lantern_shrine",
     "at": {"tx": 8, "ty": 9}, "w": 2, "h": 3, "overhang": 2},
    {"id": "shrine_road_c", "sprite": "glowmoss_deep_null_lantern_shrine",
     "at": {"tx": 13, "ty": 13}, "w": 2, "h": 3, "overhang": 2},
]
# dark reed-lanterns remembering the fen-road (walk-under, beside the way)
for n, (x, y) in enumerate([(22, 19), (18, 9), (4, 11), (21, 12)]):
    m["objects"].append(
        {"id": f"dead_lantern_{n}", "sprite": "saltreach_reed_lantern_dark",
         "at": {"tx": x, "ty": y}, "w": 1, "h": 2, "overhang": 1,
         "walk_under": True})

# THE QUIETED CAMP (touch #2): the vignette + its read
m["objects"].append(
    {"id": "quiet_camp", "sprite": "coldfog_quiet_camp",
     "at": {"tx": 4, "ty": 7}, "w": 3, "h": 2})
for i, tx in enumerate((4, 5, 6)):
    m["triggers"].append(
        {"id": f"quiet_camp_read_{i}", "kind": "dialogue",
         "at": {"tx": tx, "ty": 8}, "activation": "interact",
         "ref": "npc.coldfog_quiet_camp"})
owed += ["npc.coldfog_quiet_camp (the camp read — see docstring; grief, no body, no joke)"]

# ---- signs --------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="coldfog_works", at=(17, 8))      # the works' notice
owed += pt.sign(m, deco, W, sid="coldfog_beacon", at=(3, 11))     # the spur's why
owed += pt.sign(m, deco, W, sid="coldfog_backdoor", at=(3, 5))    # the wrong road
# (sign.coldfog_beacon / sign.coldfog_backdoor double as their warps' blocked_ref)

# ---- caches (variety: wicks on the dead islet, a consumable by the camp,
#      a valuable on the bank — the better finds off the lane) ------------------------
owed += pt.cache(m, cid="coldfog_drowned_wicks", at=(20, 18))   # loose wicks, murk islet
owed += pt.cache(m, cid="coldfog_camp_tonic", at=(3, 9))        # consumable, by the camp
owed += pt.cache(m, cid="coldfog_bank_charm", at=(24, 13))      # valuable, the shelf top

# ---- encounters (band 48-50; Light-kin ABSENT; murk carries nothing) -----------------
TABLE_II = [
    {"kin_id": 137, "weight": 26, "min_level": 48, "max_level": 50},  # Nullmoth
    {"kin_id": 139, "weight": 22, "min_level": 48, "max_level": 50},  # WispwaneNull
    {"kin_id": 141, "weight": 18, "min_level": 48, "max_level": 50},  # Cindersob
    {"kin_id": 142, "weight": 14, "min_level": 49, "max_level": 50},  # Embergone
    {"kin_id": 134, "weight": 12, "min_level": 49, "max_level": 50},  # Wispwane
    {"kin_id": 138, "weight": 8, "min_level": 49, "max_level": 50},   # Voidmantle
]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if blighttuft[i]:
        (band_grid if (i // W) in (21, 22) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE_II, id_prefix="crossing")
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE_II, id_prefix="bed")

# ---- drained dressing ----------------------------------------------------------------
# grey moss ringing the stilled pond (touch #3) + creeping the sheets' banks
for (x, y, n) in [(18, 9, "greymoss_a"), (22, 9, "greymoss_b"), (19, 12, "greymoss_a"),
                  (21, 8, "greymoss_b"), (4, 15, "greymoss_a"), (9, 18, "greymoss_b"),
                  (23, 13, "greymoss_a"), (27, 12, "greymoss_b"), (7, 14, "greymoss_a"),
                  (12, 9, "greymoss_b"), (24, 4, "greymoss_a"), (3, 20, "greymoss_b")]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid(n)
for (x, y) in [(10, 11), (17, 19), (26, 8), (5, 13), (13, 20), (22, 14), (8, 4),
               (26, 20), (16, 10)]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid("g_pebble")
for (x, y) in [(9, 20), (3, 16), (27, 5), (19, 20), (7, 11), (24, 9)]:
    if deco[y * W + x] == 0:
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
