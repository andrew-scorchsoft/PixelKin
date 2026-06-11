#!/usr/bin/env python3
"""
Pale Vault Glacier — the North's aurora-lit ice town + approach (walkthrough/
03-north "Pale Vault Glacier"; Lumenary 6: Ysolde Frost — her bond-test waits
at the heart of the UNDERCROFT, never in town).

Arc D: the lonely aurora — bone snow, blue ice sheets, glacier crag, the
lowest emotional point of the region's road. Three signature touches (§8):
  1. THE UNDERCROFT DOOR beneath the Lumenary, blue ice beside it with the
     seven dark brackets sensed through it (signed) — the earned-loop tease
     (spine §5 shape #6: ice lamp-line, single-map trial);
  2. THE DRAINED-VISTA SHELF on the lane south of town — the quiet glacier
     pocket where Còr appears in person (B3, the game's emotional spine);
     grey moss, ice spires, stillness. Subtle: NO null-lantern props (that
     reveal is B4's, West);
  3. THE AURORA-WATCH on the festival ice — a frozen lake east of town ringed
     with pale-flame braziers, the town standing in silence, lamps lit.

§0 TRAP #1 (binding): the Lumenary is reachable WITHOUT Emberward — the
south entry, the lane, the town and the Lumenary door carry NO gate of any
kind. Emberward gates only the optional deep-ice back-fold (SE) and, onward,
Hushfrost I→II (West's map).

The earned loop — "The Lamp-Line" (§5 shape #6): script.ysolde_quest at the
undercroft door -> flag:q_north_lampline; the stormwood cache in the approach
hollows (flag:picked_stormwood, visible only once the loop runs) ->
script.render_oil at the tallow-keeper's doused camp -> flag:q_north_aurora_oil
(the camp's hearth relights — a MapObject flag-swap pair); the undercroft door
consumes the flag (blocked line in Ysolde's voice).

Story bands on the oil leg (both compute their cut from the painted grids —
the Tide-blessing lesson: band the WHOLE walkable cut, but ONLY walkable
cells):
  B3  script.cor_appears (= cutscene.cor_appears) on the row-18 choke (the
      lane + the shelf mouth — the only way south), requires
      flag:q_north_lampline so it fires ON the oil leg, sets flag:met_cor.
  C3  script.fenn_shared_past (= cutscene.fenn_shared_past) on the row-20
      lane choke immediately after, requires flag:met_cor (narrative only —
      flag:fenn_c3 just retires the band + Fenn's placement).
  A4  Wren's wobble at the undercroft door: sight-trainer placement
      `wren_pale_vault` (requires flag:met_cor — raw from Còr's words), the
      hard rival battle at/above player level (TRAINERS def = wiring agent).
      NO beaten after-swap: Wren walks off unsure (the staging is the
      argument; Mira's N3 ribbon quest at Galehigh carries the aftermath).

N2 "The Aurora Sketcher" (giver here, per the hooks): script.sketch_quest at
the festival ice sets flag:q_north_sketch; the chain is SEQUENTIAL (one
requires_flag per trigger): Windward II's crag viewpoint (already built)
requires q_north_sketch -> sets _1; the glacier-shore viewpoint here requires
_1 -> sets _2; the festival-ice viewpoint requires _2 -> sets _3; the
sketcher's reward placement requires _3 -> script.sketch_done gives the
Aurora Charm + sets flag:q_north_sketch_done.

Wires to: windward_stair_ii `to_glacier` lands (14,28)/(15,28) — our return
pair `to_windward` at (14,29)/(15,29) lands one tile inside its exit at
(20,1)/(21,1). `to_pass` west (hushfrost_pass_i — W1 authors the far side;
landing (30,10)/(30,11) is a placeholder the engine no-ops; W1's return pair
must land at our (1,10)/(1,11)). The undercroft arch door at (19,8) and the
undercroft's entry warp land ON each other (the mutual pair).

Encounter picks (the walkthrough's Frostkit/Auralisk/Snowtoll are atlas
flavour names with no species rows — documented deviation, the N1 Kiteling
precedent): hollows band 36-40 = #72 Glaceling (Frost C, the glacier
ice-sprite), #81 Blizzrhare (Frost C, the snow-vortex hare), #86 Prismcub
(Light/Frost A — its dex entry NAMES Pale Vault Glacier), #95 Glacewing
(Storm/Frost C, the N2 continuity), #87 Prismantus (D, rare). The
Emberward-gated deep-ice fold runs rarer/deeper 38-40: Stillwarden #85,
Prismantus #87, Glaceling #72.

Suggested sign copy (the wiring agent writes dialogue.ts; ZERO humour in
this cluster — the Aurora-watch is a silent vigil):
  sign.pale_vault_welcome    "PALE VAULT GLACIER. The vault keeps its quiet —
                              walk softly, and keep your lamp close."
  sign.pale_vault_undercroft "The Lumenary undercroft. Through the blue ice,
                              seven dark brackets descend into the glacier."
  sign.pale_vault_pass       "WEST — HUSHFROST PASS. Coldfog holds the far
                              throat; only a warded flame walks through."
  sign.pale_vault_deepice    "The deep ice. The glacier closes this fold to
                              any flame that cannot ward itself."
                              (the Emberward tease — also the warp-less gate's
                              blocked line; [MISSABLE] once Emberward is held)

audit_flow note — town maps have no loop requirement; the hollows ledge at
row 21 (east) is the one-way return-compressor for the festival fold.

Run:  ./venv/bin/python tools/maps/build_pale_vault_glacier.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 32, 30
rng = random.Random(71)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
glacier = mk.make_grid(W, H)    # crag walls, the choke masses, pocket rims
ice = mk.make_grid(W, H)        # walkable blue ice: the festival lake, sheets, the fold
snowtrail = mk.make_grid(W, H)  # the lit lanes
frosttuft = mk.make_grid(W, H)  # encounter hollows + the mandatory crossing
deco = mk.make_grid(W, H)

# BORDERS: glacier crag all round, 2 deep
mk.rect(glacier, W, H, 0, 0, W - 1, 1)              # north
mk.rect(glacier, W, H, 0, 0, 1, H - 1)              # west
mk.rect(glacier, W, H, 30, 0, 31, H - 1)            # east
mk.rect(glacier, W, H, 0, 28, W - 1, H - 1)         # south
# organic bumps so the rim never reads ruled (§11 r2)
mk.organic_border(glacier, W, H, depth=0,
                  bumps=[(6, 2, 2), (20, 2, 2), (28, 2, 2), (2, 21, 2),
                         (30, 8, 2), (2, 6, 2), (29, 27, 2), (8, 28, 2)],
                  rng=rng)
# south entry gap from Windward (cols 14-15; landing (14,28)/(15,28) walkable,
# our return warps ON rows 29)
for y in (28, 29):
    for x in (14, 15):
        glacier[y * W + x] = 0
# west exit gap to Hushfrost (rows 10-11)
for x in (0, 1):
    for y in (10, 11):
        glacier[y * W + x] = 0

# THE ROW 17-20 CHOKE BELT: glacier masses pinch the map between town and the
# hollows so the lane (cols 14-15) + the shelf mouth are the ONLY way south —
# the B3/C3 bands cannot be walked around (audit_flow proves the cut).
mk.rect(glacier, W, H, 16, 16, 29, 20)              # east mass (the lake's south wall)
mk.rect(glacier, W, H, 2, 16, 13, 17)               # west mass, north rim
mk.rect(glacier, W, H, 11, 19, 13, 20)              # west mass, south block
glacier[18 * W + 12] = 0                            # the shelf mouth pierces at row 18
glacier[18 * W + 13] = 0
# THE DRAINED-VISTA SHELF (B3): a quiet pocket carved out of the west mass
for y in range(17, 21):
    for x in range(3, 11):
        glacier[y * W + x] = 0
mk.rect(glacier, W, H, 2, 21, 2, 21)                # round the shelf's SW lip
glacier[18 * W + 11] = 0                            # mouth throat (x11, row 18)
mk.rect(glacier, W, H, 11, 16, 11, 17)
# re-seal the shelf's south rim (no second way out — the bands own the cut)
mk.rect(glacier, W, H, 3, 21, 10, 21)

# NW SHORE POCKET (the sketch-shore viewpoint) framed under the pass lane
mk.rect(glacier, W, H, 7, 12, 9, 15)                # its east rim
mk.rect(glacier, W, H, 2, 16, 9, 16)                # shared rim with the shelf belt

# THE FESTIVAL LAKE (east): walkable blue ice, blob-shaped (§11 r4)
mk.blob(ice, W, H, 24.5, 12.5, 4.2, 2.6)
mk.blob(ice, W, H, 22.0, 14.0, 2.2, 1.6)
# the ice window beside the undercroft arch (the seven-brackets tease) —
# a shaped 2-deep sheet, not a radius-1 plus (§11 r4)
mk.rect(ice, W, H, 21, 6, 22, 7)
ice[6 * W + 23] = 1
# the NW shore sheet the viewpoint overlooks
mk.blob(ice, W, H, 3.5, 13.5, 2.0, 1.5)
# THE DEEP-ICE FOLD (SE, Emberward): an ice throat off the east hollow into a
# walled pocket — the gate rect rides the pure-ice throat (CLAUDE.md gotcha)
mk.rect(glacier, W, H, 25, 22, 25, 27)              # the fold's west wall…
mk.rect(glacier, W, H, 26, 22, 30, 22)              # …its north wall
for y in range(23, 28):
    for x in range(26, 30):
        glacier[y * W + x] = 0                      # the pocket interior
for y in (24, 25):
    glacier[y * W + 25] = 0                         # the throat pierces the west wall
mk.rect(ice, W, H, 26, 23, 29, 27)                  # deep-ice floor
mk.rect(ice, W, H, 25, 24, 25, 25)                  # (throat tiles, gated below)

# ---- lanes (snowtrail on snow — context-correct) -----------------------------------
mk.vline(snowtrail, W, H, 14, 10, 29)               # the main lane, entry -> town
mk.vline(snowtrail, W, H, 15, 10, 29)
mk.hline(snowtrail, W, H, 9, 4, 27)                 # town street (north row)
mk.rect(snowtrail, W, H, 8, 8, 10, 8)               # forecourt jogs so the street's
mk.rect(snowtrail, W, H, 21, 8, 22, 8)              # north edge never runs ruled
mk.hline(snowtrail, W, H, 10, 2, 26)                # town street / pass lane row
mk.hline(snowtrail, W, H, 11, 1, 13)                # pass lane (south row)
mk.hline(snowtrail, W, H, 12, 16, 20)               # east lane to the festival ice
mk.hline(snowtrail, W, H, 13, 16, 20)

# ---- encounter terrain -------------------------------------------------------------
# sheltered hollows (optional patches, band 36-40)
mk.blob(frosttuft, W, H, 5.5, 23.0, 2.4, 1.4)       # W hollow (above the camp)
mk.blob(frosttuft, W, H, 20.0, 25.5, 3.2, 1.8)      # E hollow
mk.blob(frosttuft, W, H, 9.0, 26.5, 1.8, 1.2)       # camp-side tuft
# the MANDATORY crossing (§11 r7): rows 22-23 wall to wall, the lane paused
pt.mandatory_band(frosttuft, snowtrail, W, H, y0=22, y1=23, x0=2, x1=29)
# the deep-ice fold's rare bed rolls rect-wide (cave terrain) — no tuft needed

# ---- precedence (one family per cell; structure wins) ------------------------------
for i in range(W * H):
    if glacier[i]:
        ice[i] = 0
        snowtrail[i] = 0
        frosttuft[i] = 0
    if ice[i]:
        snowtrail[i] = 0
        frosttuft[i] = 0
    if snowtrail[i]:
        frosttuft[i] = 0

# ---- base: bone snow ---------------------------------------------------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ice", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": ice},
    {"name": "t_snowtrail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": snowtrail},
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
]

m: dict = {
    "id": "pale_vault_glacier", "display_name": "Pale Vault Glacier",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [
        # the deep-ice fold's throat — Emberward force-gates the pure-ice strip
        # (optional back-fold ONLY; never the town or Lumenary — §0 rule 1)
        {"id": "deepice_fold", "ability": "emberward",
         "rect": {"tx": 25, "ty": 24, "w": 1, "h": 2}, "effect": "make_passable"},
    ],
    "music": "assets/audio/music/pale-vault-glacier-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/pale-vault-glacier-a.webp",
        "assets/backgrounds/battle/pale-vault-glacier-b.webp",
    ],
}

# ---- buildings (the bespoke pale_vault object set; doors are walk-onto) ------------
path_for_aprons = snowtrail  # aprons carve into the lane grid
# Ysolde's Frost Lumenary, axial at the head of the main lane (§3a r3: seen
# from the south entry). NOT ability-gated; starter-gated like every Lumenary.
pt.building(m, path_for_aprons, W, H, oid="lumenary", sprite="pale_vault_lumenary",
            at=(11, 3), overhang=3, door_col=3,
            to_map="pale_vault_lumenary", to=(8, 11))
m["warps"][-1].update({"id": "to_lumenary", "requires_flag": "flag:has_starter",
                       "blocked_ref": "door.locked_lumenary"})
# the inn (rest point) west, a home east
pt.building(m, path_for_aprons, W, H, oid="inn", sprite="pale_vault_inn",
            at=(3, 4), overhang=2, door_col=2,
            to_map="pale_vault_inn", to=(7, 9))
m["warps"][-1]["id"] = "to_inn"
pt.building(m, path_for_aprons, W, H, oid="home", sprite="pale_vault_home",
            at=(24, 4), overhang=2, door_col=2,
            to_map="pale_vault_home", to=(6, 7))
m["warps"][-1]["id"] = "to_home"
# THE UNDERCROFT ARCH beneath the Lumenary's east shoulder: its door carries
# the gated step_on warp (the Lamp-Line's lock; blocked in Ysolde's voice)
pt.building(m, path_for_aprons, W, H, oid="undercroft_arch",
            sprite="pale_vault_undercroft_arch", at=(18, 6), overhang=1,
            door_col=1, to_map="pale_vault_undercroft", to=(10, 0))
m["warps"][-1].update({"id": "to_undercroft",
                       "requires_flag": "flag:q_north_aurora_oil",
                       "blocked_ref": "npc.ysolde_door_unlit"})

# ---- objects: braziers, the camp swap pair, spires, lamps --------------------------
m["objects"] += [
    # Aurora-watch braziers ringing the festival ice (pale cold flames)
    {"id": "brazier_nw", "sprite": "pale_vault_brazier", "at": {"tx": 20, "ty": 9},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "brazier_ne", "sprite": "pale_vault_brazier", "at": {"tx": 27, "ty": 8},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "brazier_s", "sprite": "pale_vault_brazier", "at": {"tx": 21, "ty": 14},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    # the tallow-keeper's camp: doused -> lit by the oil errand (the MapObject
    # flag-swap pair — same footprint, same solidity; CLAUDE.md gotcha)
    {"id": "tallow_camp_doused", "sprite": "pale_vault_camp_doused",
     "at": {"tx": 4, "ty": 24}, "w": 3, "h": 2, "overhang": 0,
     "hidden_when_flag": "flag:q_north_aurora_oil"},
    {"id": "tallow_camp_lit", "sprite": "pale_vault_camp_lit",
     "at": {"tx": 4, "ty": 24}, "w": 3, "h": 2, "overhang": 0,
     "requires_flag": "flag:q_north_aurora_oil"},
    # ice spires: the drained shelf's vista dressing + the shore pocket
    {"id": "spires_shelf", "sprite": "pale_vault_ice_spire", "at": {"tx": 3, "ty": 17},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "spires_shore", "sprite": "pale_vault_ice_spire", "at": {"tx": 5, "ty": 11},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "spires_gate", "sprite": "pale_vault_ice_spire", "at": {"tx": 28, "ty": 20},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    # lamp posts beside (never on) the lit lanes
    # (trunks land at ty+2 — keep every base BESIDE a lane, never on it)
    {"id": "lamp_entry", "sprite": "tinderwick_lamp_post", "at": {"tx": 13, "ty": 24},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_street", "sprite": "tinderwick_lamp_post", "at": {"tx": 17, "ty": 6},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_pass", "sprite": "tinderwick_lamp_post", "at": {"tx": 10, "ty": 6},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_lane", "sprite": "tinderwick_lamp_post", "at": {"tx": 13, "ty": 12},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- the hollows ledge (one-way hop down off the festival lane, §3a r1/r2) ---------
pt.ledge_run(deco, W, H, 21, 17, 20, rng, family="snow")

# ---- warps (graph.ts edge ids verbatim) --------------------------------------------
m["warps"] += [
    # SOUTH <-> windward_stair_ii (its `to_glacier` pair lands (14,28)/(15,28),
    # one tile inside our return warps; we land one tile inside its exit)
    {"id": "to_windward", "at": {"tx": 14, "ty": 29}, "trigger": "step_on",
     "to_map": "windward_stair_ii", "to": {"tx": 20, "ty": 1}, "facing": "down",
     "transition": "fade"},
    {"id": "to_windward_e", "at": {"tx": 15, "ty": 29}, "trigger": "step_on",
     "to_map": "windward_stair_ii", "to": {"tx": 21, "ty": 1}, "facing": "down",
     "transition": "fade"},
    # WEST -> hushfrost_pass_i (`to_pass`, UNGATED — the West hand-off; W1
    # authors the far side, landing is a placeholder the engine no-ops; W1's
    # return pair must land at our (1,10)/(1,11))
    {"id": "to_pass", "at": {"tx": 0, "ty": 10}, "trigger": "step_on",
     "to_map": "hushfrost_pass_i", "to": {"tx": 30, "ty": 10}, "facing": "left",
     "transition": "fade"},
    {"id": "to_pass_s", "at": {"tx": 0, "ty": 11}, "trigger": "step_on",
     "to_map": "hushfrost_pass_i", "to": {"tx": 30, "ty": 11}, "facing": "left",
     "transition": "fade"},
]

# ---- story bands (compute the cut from the grids — band ONLY walkable cells) -------
def walkable_row(y: int, x0: int, x1: int) -> list[int]:
    return [x for x in range(x0, x1 + 1) if not glacier[y * W + x]]

# B3 — Còr appears (the row-18 cut: the lane + the shelf mouth). Fires only on
# the oil leg (requires q_north_lampline); once; the flag pair retires it.
for i, tx in enumerate(walkable_row(18, 11, 15)):
    m["triggers"].append({
        "id": f"cor_appears_{i}", "kind": "cutscene", "at": {"tx": tx, "ty": 18},
        "activation": "step_on", "ref": "script.cor_appears", "once": True,
        "requires_flag": "flag:q_north_lampline",
        "sets_flags": ["flag:met_cor"],
        "hidden_when_flag": "flag:met_cor"})
owed += ["script.cor_appears (= cutscene.cor_appears; B3 — Còr in person, NO "
         "battle; letterbox + near-silence + cameraFocus the shelf; sets "
         "flag:met_cor)"]

# C3 — Fenn, on Còr's heels (the row-20 lane choke; requires met_cor)
for i, tx in enumerate(walkable_row(20, 14, 15)):
    m["triggers"].append({
        "id": f"fenn_shared_past_{i}", "kind": "cutscene",
        "at": {"tx": tx, "ty": 20}, "activation": "step_on",
        "ref": "script.fenn_shared_past", "once": True,
        "requires_flag": "flag:met_cor",
        "sets_flags": ["flag:fenn_c3"],
        "hidden_when_flag": "flag:fenn_c3"})
owed += ["script.fenn_shared_past (= cutscene.fenn_shared_past; C3 — two "
         "faces and the quiet, no music swell; sets flag:fenn_c3)"]

# ---- the sketch viewpoints (sequential chain — see the module docstring) -----------
m["triggers"] += [
    {"id": "sketch_shore", "kind": "script", "at": {"tx": 3, "ty": 14},
     "activation": "interact", "ref": "script.sketch_shore", "once": True,
     "requires_flag": "flag:q_north_sketch_1",
     "sets_flags": ["flag:q_north_sketch_2"],
     "hidden_when_flag": "flag:q_north_sketch_2"},
    {"id": "sketch_festival", "kind": "script", "at": {"tx": 25, "ty": 13},
     "activation": "interact", "ref": "script.sketch_festival", "once": True,
     "requires_flag": "flag:q_north_sketch_2",
     "sets_flags": ["flag:q_north_sketch_3"],
     "hidden_when_flag": "flag:q_north_sketch_3"},
]
owed += ["script.sketch_shore (requires q_north_sketch_1; sets _2)",
         "script.sketch_festival (requires q_north_sketch_2; sets _3)"]

# ---- signs -------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="pale_vault_welcome", at=(13, 26))
owed += pt.sign(m, deco, W, sid="pale_vault_undercroft", at=(21, 8))
owed += pt.sign(m, deco, W, sid="pale_vault_pass", at=(3, 9))
owed += pt.sign(m, deco, W, sid="pale_vault_deepice", at=(28, 21))

# ---- caches (variety: quest kindling, consumable, loose wicks, valuable) -----------
owed += pt.cache(m, cid="stormwood", at=(10, 26))        # the Lamp-Line kindling
for npc in m["npcs"]:
    if npc["id"] == "cache_stormwood":
        npc["requires_flag"] = "flag:q_north_lampline"
owed += pt.cache(m, cid="pale_vault_balm", at=(22, 26))  # consumable, E hollow
owed += pt.cache(m, cid="pale_vault_wicks", at=(28, 15)) # loose wicks, lake shore
owed += pt.cache(m, cid="pale_vault_shard", at=(29, 26)) # Starglass Shard, deep ice
owed += pt.cache(m, cid="pale_vault_charge", at=(9, 3))  # a charge, the back strip
                                                         # (pays the off-lane pocket
                                                         # behind the buildings)

# ---- encounters (band 36-40, continuous with Windward 34-36 / Hushfrost ~40) -------
TABLE = [{"kin_id": 72, "weight": 28, "min_level": 36, "max_level": 39},
         {"kin_id": 81, "weight": 24, "min_level": 36, "max_level": 39},
         {"kin_id": 86, "weight": 20, "min_level": 36, "max_level": 38},
         {"kin_id": 95, "weight": 18, "min_level": 37, "max_level": 40},
         {"kin_id": 87, "weight": 10, "min_level": 38, "max_level": 40}]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if frosttuft[i]:
        (band_grid if (i // W) in (22, 23) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE, id_prefix="hollow")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE, id_prefix="crossing")
# the deep-ice fold: rarer, deeper, rect-wide (cave terrain rolls on the ice)
m["encounters"].append({
    "id": "deepice", "terrain": "cave",
    "rect": {"tx": 26, "ty": 24, "w": 4, "h": 4}, "encounter_rate": 0.10,
    "table": [{"kin_id": 85, "weight": 40, "min_level": 38, "max_level": 40},
              {"kin_id": 87, "weight": 35, "min_level": 38, "max_level": 40},
              {"kin_id": 72, "weight": 25, "min_level": 38, "max_level": 40}]})

# ---- NPCs --------------------------------------------------------------------------
m["npcs"] += [
    # --- Ysolde at the undercroft door (hook -> waiting; once the oil is
    # rendered she has gone below — the undercroft heart holds her) ---------------
    {"id": "ysolde_quest", "at": {"tx": 18, "ty": 9}, "facing": "down",
     "sprite": "ysolde_frost", "movement": "static",
     "dialogue_ref": "script.ysolde_quest",
     "hidden_when_flag": "flag:q_north_lampline"},
    {"id": "ysolde_waiting", "at": {"tx": 18, "ty": 9}, "facing": "down",
     "sprite": "ysolde_frost", "movement": "static",
     "dialogue_ref": "npc.ysolde_waiting",
     "requires_flag": "flag:q_north_lampline",
     "hidden_when_flag": "flag:q_north_aurora_oil"},
    # --- A4: Wren's wobble at the undercroft door (the hard rival battle;
    # appears after Còr's words; NO after-swap — Wren walks off unsure) -----------
    {"id": "wren_pale_vault", "at": {"tx": 19, "ty": 9}, "facing": "down",
     "sprite": "wren", "movement": "static",
     "dialogue_ref": "script.wren_pale_vault",
     "requires_flag": "flag:met_cor",
     "sight_range": 3, "defeated_flag": "flag:wren_pale_vault_battled",
     "hidden_when_flag": "flag:wren_pale_vault_battled"},
    # --- B3 staging: the still figure on the drained shelf during the window ----
    {"id": "cor_figure", "at": {"tx": 6, "ty": 18}, "facing": "down",
     "sprite": "cor", "movement": "static",
     "dialogue_ref": "npc.cor_quiet",
     "requires_flag": "flag:q_north_lampline",
     "hidden_when_flag": "flag:met_cor"},
    # --- C3 staging: Fenn beside the lane while the beat pends ------------------
    {"id": "fenn_c3", "at": {"tx": 13, "ty": 20}, "facing": "right",
     "sprite": "npc_mentor", "movement": "static",
     "dialogue_ref": "script.fenn_shared_past",
     "requires_flag": "flag:met_cor",
     "hidden_when_flag": "flag:fenn_c3"},
    # --- the tallow-keeper at her doused camp (the oil errand) ------------------
    {"id": "tallow_keeper_doused", "at": {"tx": 7, "ty": 25}, "facing": "down",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "npc.tallow_keeper_doused",
     "hidden_when_flag": "flag:picked_stormwood"},
    {"id": "tallow_keeper_render", "at": {"tx": 7, "ty": 25}, "facing": "down",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "script.render_oil",
     "requires_flag": "flag:picked_stormwood",
     "hidden_when_flag": "flag:q_north_aurora_oil"},
    {"id": "tallow_keeper_after", "at": {"tx": 7, "ty": 25}, "facing": "down",
     "sprite": "npc_old_woman", "movement": "look_around",
     "dialogue_ref": "npc.tallow_keeper_after",
     "requires_flag": "flag:q_north_aurora_oil"},
    # --- the Aurora-watch on the festival ice (Arc E: stillness, lamps lit) -----
    {"id": "vigil_keeper", "at": {"tx": 23, "ty": 11}, "facing": "up",
     "sprite": "npc_old_man", "movement": "static",
     "dialogue_ref": "script.pale_vault_aurora_watch",
     "hidden_when_flag": "flag:aurora_watch_seen"},
    {"id": "vigil_keeper_after", "at": {"tx": 23, "ty": 11}, "facing": "up",
     "sprite": "npc_old_man", "movement": "static",
     "dialogue_ref": "npc.vigil_keeper_after",
     "requires_flag": "flag:aurora_watch_seen"},
    {"id": "aurora_watcher_a", "at": {"tx": 25, "ty": 12}, "facing": "up",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.aurora_watcher_a"},
    {"id": "aurora_watcher_b", "at": {"tx": 26, "ty": 14}, "facing": "up",
     "sprite": "npc_man", "movement": "static",
     "dialogue_ref": "npc.aurora_watcher_b"},
    # --- N2 "The Aurora Sketcher" (giver -> working -> reward -> after) ---------
    {"id": "sketcher_quest", "at": {"tx": 22, "ty": 11}, "facing": "right",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "script.sketch_quest",
     "hidden_when_flag": "flag:q_north_sketch"},
    {"id": "sketcher_working", "at": {"tx": 22, "ty": 11}, "facing": "right",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.sketcher_working",
     "requires_flag": "flag:q_north_sketch",
     "hidden_when_flag": "flag:q_north_sketch_3"},
    {"id": "sketcher_done", "at": {"tx": 22, "ty": 11}, "facing": "right",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "script.sketch_done",
     "requires_flag": "flag:q_north_sketch_3",
     "hidden_when_flag": "flag:q_north_sketch_done"},
    {"id": "sketcher_after", "at": {"tx": 22, "ty": 11}, "facing": "right",
     "sprite": "npc_woman", "movement": "look_around",
     "dialogue_ref": "npc.sketcher_after",
     "requires_flag": "flag:q_north_sketch_done"},
    # --- witness beat (standing kit): the town reacts to the B3 beat ------------
    {"id": "pale_vault_witness", "at": {"tx": 17, "ty": 10}, "facing": "left",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.pale_vault_witness",
     "requires_flag": "flag:met_cor"},
    # --- ambient + the Gleam's festival payoff (the town answers the win) -------
    {"id": "townsfolk_inn", "at": {"tx": 8, "ty": 10}, "facing": "down",
     "sprite": "npc_man", "movement": "look_around",
     "dialogue_ref": "npc.pale_vault_townsfolk"},
    {"id": "gleam_watcher", "at": {"tx": 24, "ty": 14}, "facing": "up",
     "sprite": "npc_girl", "movement": "static",
     "dialogue_ref": "npc.pale_vault_gleam_watcher",
     "requires_flag": "gleam:frost"},
    {"id": "gleam_kid", "at": {"tx": 16, "ty": 11}, "facing": "up",
     "sprite": "npc_child", "movement": "wander",
     "dialogue_ref": "npc.pale_vault_gleam_kid",
     "requires_flag": "gleam:frost"},
]
owed += ["script.ysolde_quest (sets flag:q_north_lampline)",
         "npc.ysolde_waiting", "npc.ysolde_door_unlit (undercroft door blocked_ref)",
         "script.wren_pale_vault (A4; battle vs TRAINERS['wren_pale_vault'] — "
         "rival class, at/above player level ~38-39, payout 24×ace; sets "
         "flag:wren_pale_vault_battled; afterward Wren walks off unsure — "
         "deliberately NO beaten after-placement)",
         "TRAINERS['wren_pale_vault']", "npc.cor_quiet",
         "npc.tallow_keeper_doused",
         "script.render_oil (requires picked_stormwood; sets flag:q_north_aurora_oil)",
         "npc.tallow_keeper_after",
         "script.pale_vault_aurora_watch (= cutscene.pale_vault_aurora_watch; "
         "silent vigil — silence + slow tint as each lamp lights; sets "
         "flag:aurora_watch_seen)",
         "npc.vigil_keeper_after", "npc.aurora_watcher_a", "npc.aurora_watcher_b",
         "script.sketch_quest (N2 giver; sets flag:q_north_sketch)",
         "npc.sketcher_working",
         "script.sketch_done (requires q_north_sketch_3; gives the Aurora Charm; "
         "sets flag:q_north_sketch_done)",
         "npc.sketcher_after", "npc.pale_vault_witness", "npc.pale_vault_townsfolk",
         "npc.pale_vault_gleam_watcher", "npc.pale_vault_gleam_kid"]

# ---- drained-shelf dressing (B3: grey, quiet — NO null-lantern props) --------------
for (x, y, n) in [(5, 19, "greymoss_a"), (8, 18, "greymoss_b"), (4, 20, "greymoss_b"),
                  (9, 19, "greymoss_a"), (7, 20, "greymoss_b")]:
    deco[y * W + x] = gid(n)

# ---- scatter decor + boulders ------------------------------------------------------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (glacier, ice, snowtrail, frosttuft))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
mk.scatter_decor(deco, base, W, H, rng, density=0.15, avoid=avoid)
for (x, y) in [(9, 5), (22, 4), (29, 5), (3, 12), (12, 14), (18, 15),
               (3, 22), (12, 27), (24, 27), (17, 24), (29, 17)]:
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
