#!/usr/bin/env python3
"""
The Mourning Fields — the fallow fields the Hollowing quieted (walkthrough/11
Part C, Lane N3; kind route, region outer, band 48-52, optional + late).
World (68,-461), 26x32: Stillwater above, Coldfog Marches I to the west, the
Rimeway's col below. It closes the north into a LOOP (Coldfog I -> Stillwater
-> the Fields -> Coldfog I) and drops a return road south to the Rimeway.

Lore: this was Stillwater's farmland. When the Hollowing came, the harvest was
left standing in the stook and the field-kin were put to sleep where they lay —
not hurt: TUCKED IN, under grey blankets woven from the coldfog itself, and
watched over every evening. The scarecrows are lamp-posts in field-coats, their
lanterns hooded "so the light won't wake them". Grief dressed as mercy, the
dread register of the Marches, but tender: nothing broken, nothing burnt.

Three signature touches (§8):
  1. THE SLEEPERS' FIELD — kin asleep under coldfog blankets in the long fallow
     plot, a field-tender who tucks them in at dusk; after the dawn they wake
     (each sleeper has an `_awake` twin at flag:dawn, blanket folded beside it).
  2. THE FIELD SHRINE on the east shelf — seen from the walk-up and the whole
     lower field, reached only by the drop from the upper terrace (then a ledge
     out): a wayside house whose candles were put out one by one.
  3. THE SCARECROW-LAMPS — lanterns hooded in wool, unhooded after the dawn.

Shape (rows top-down):
  * row 0-1    the north mouth (cols 2-5) up to Stillwater; fog-crag elsewhere;
  * rows 2-9   THE UPPER TERRACE: the hay plot, the first sleepers, a grind bed
               east; the acolyte Ines posted at the head of the walk-up;
  * row 10-11  THE BANK: a scree ledge across the west half (x 2-15, hop down
               only; it jogs down a row at x 7-11, a bramble on each corner) —
               the QUICK way from Stillwater to the Coldfog gate; the
               east half is a fog-crag terrace (rows 10-11) with ONE walk-up at
               x=17 and the drop onto the shrine shelf at x 21-22;
  * rows 11-21 west: the Coldfog gate meadow (rows 11-14 at x=0), walled in by
               the bank (north), the barley-drift crossing (x 9-10, east) and
               the south crossing; middle: the sleepers' field; east: the shelf;
  * rows 19-25 the south crossing (full width, blight-tuft, a lobed drift — both
               edges wave): the Rimeway road must pass it;
  * rows 24-31 the col: drifts blowing in from the Rimeway, the last plot, the acolyte Corran on
               the road, the south mouth (cols 10-13) down to the Rimeway.
The FOLD: from the Coldfog gate the way up to Stillwater runs EAST across the
crossing to the walk-up at x=17 and back WEST along the upper terrace; going
the other way you just hop the bank.

Edges (world geometry, binding — docs/world/geometry.md; contract in 11 §Build):
  N  (2..5,0)    <-> stillwater (22..25,29)       [`to_stillwater`; lands Stillwater (22..25,28)]
  W  (0,11..14)  <-> coldfog_marches_i (19,11..14) [`to_coldfog`; lands Coldfog I (18,11..14)]
  S  (10..13,31) <-> rimeway_descent (16..19,0)   [`to_rimeway`; lands Rimeway (16..19,1)]
Stillwater's and Coldfog I's sides are Lane N1's (they land here at (2..5,1)
and (1,11..14)); the Rimeway's side is in build_rimeway_descent.py.

Wild kin (lv 48-52 at night; the day-forms at flag:dawn, 56-62). The Hollowing
family #178-#180 (Lane N4) joins the tables when its species files exist; the north
mouth's verge is a deliberately LOW bed (Dousecap 42-44, under its kindle level).
Tables mirrored in build_species.py (MOURNING_TABLES).

2026-10-14 review pass (expansion-panel.md, Part C): lobed stubble plots on the
`mournfields_set` accent family (build_mournfields_set.py) with pinned drill/swathe
layouts, a jogged bank, blobbed crossings, soft-wool sleepers, a stile/plough/stair,
and Fields-only finds (Lumen Drop, Lullwool Charms, a Harvest Knot).
Second pass (the independent r2): the lobed crossing, one-tile plot steps + rounded
stubble corners, the Brook Piece nook (Tussock, a marker stone, a Hearth Coal), the
shrine's dawn twin (all five candles), and the Harvest Knot as a toggle key item.

Run:  python3 tools/maps/build_mourning_fields.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 26, 32
rng = random.Random(461)
owed: list[str] = []

COLDFOG_REF = mk.register_tileset(
    "coldfog_set", index=mk.REPO / "assets/tilesets/coldfog/coldfog_set.index.json")
# the Fields' own accent set (build_mournfields_set.py): harvest STUBBLE with a real
# edge onto blight + ploughed drill tiles — the 2026-10-14 review's "mustard rectangles"
FIELDS_REF = mk.register_tileset(
    "mournfields_set",
    index=mk.REPO / "assets/tilesets/mournfields/mournfields_set.index.json")


def species_exists(kid: int) -> bool:
    return any((mk.REPO / "src/game/data/species").glob(f"{kid:03d}_*.json"))


cliff = mk.make_grid(W, H)       # fog-crag: the border + the east terrace
tuft = mk.make_grid(W, H)        # blight-tuft encounter beds
stubble = mk.make_grid(W, H)     # the fallow plots (mournfields_set `stubble` family)
deco = mk.make_grid(W, H)

# ---- enclosure ---------------------------------------------------------------------
mk.rect(cliff, W, H, 0, 0, W - 1, 1)                  # north
mk.rect(cliff, W, H, 0, 0, 1, H - 1)                  # west
mk.rect(cliff, W, H, W - 2, 0, W - 1, H - 1)          # east (the land falls away)
mk.rect(cliff, W, H, 0, H - 2, W - 1, H - 1)          # south (the col's lip)
for (x, y) in [(2, 2), (8, 2), (9, 2), (23, 2), (22, 2), (23, 3), (2, 9), (2, 15),
               (2, 16), (23, 19), (23, 20), (23, 24), (2, 28), (3, 29), (2, 29),
               (6, 29), (7, 29), (17, 29), (18, 29), (22, 29), (21, 29), (23, 28), (23, 29)]:
    cliff[y * W + x] = 1
for x in (2, 3, 4, 5):                                 # N mouth -> Stillwater
    for y in (0, 1, 2):
        cliff[y * W + x] = 0
for y in (11, 12, 13, 14):                             # W gate -> Coldfog I
    for x in (0, 1):
        cliff[y * W + x] = 0
for x in (10, 11, 12, 13):                             # S mouth -> the Rimeway
    for y in (H - 2, H - 1):
        cliff[y * W + x] = 0

# ---- the bank (rows 10-11) + the east terrace (rows 10-11) ----------------------------
# Not one ruled line (review fix 2): the bank JOGS — row 10 under the north mouth, a
# step down to row 11 where the barley-drift begins, back up to row 10 by the sleepers'
# field. Ledges are solid but for the hop, so each jog seals itself (no walk-round);
# a bramble sits on the lip at each of the two corners.
WALKUP = 17
SHELF_DROP = (21, 22)
BANK = [(x, 10) for x in range(2, 7)] + [(x, 11) for x in range(7, 12)] + \
       [(x, 10) for x in range(12, 16)]
for (x, y) in BANK:
    deco[y * W + x] = gid("scree_ledge_s" + rng.choice(["", "_v1"]))
mk.rect(cliff, W, H, 16, 10, W - 1, 11)
for y in (10, 11):
    cliff[y * W + WALKUP] = 0
    for x in SHELF_DROP:
        cliff[y * W + x] = 0
for x in SHELF_DROP:
    deco[11 * W + x] = gid("scree_ledge_s" + rng.choice(["", "_v1"]))

# ---- the shrine shelf (x 20-23, rows 12-18): fenced west, a ledge out south ----------
for y in range(12, 19):
    deco[y * W + 19] = gid("fence_post")
for x in (20, 21, 22):
    deco[18 * W + x] = gid("scree_ledge_s" + rng.choice(["", "_v1"]))
deco[18 * W + 23] = gid("fence_post")

# ---- the plots (stubble) -------------------------------------------------------------
# Lobed, not ruled (review fix 1): each plot is a union of blobs, painted as the
# `stubble` family so it meets the blight with a turned-earth rim; inside, the fill is
# PINNED in a per-plot motif (swathes / drill rows), never scattered.
# Row spans {y: (x0, x1)}, drawn by hand so every plot has a lobe, a bite and a
# lean of its own (the family's rounded corners do the rest).
PLOTS = {
    # 2026-10-14 second pass: every step is ONE tile (a staircase reads as a curve once
    # the family's convex corners are rounded), no one-tile tongues, no flat run > 3.
    "hay": {3: (9, 12), 4: (8, 13), 5: (7, 14), 6: (7, 14), 7: (8, 13)},
    "sleepers": {14: (14, 16), 15: (13, 17), 16: (12, 18), 17: (12, 18), 18: (12, 18),
                 19: (13, 18), 20: (14, 17)},
    "west": {17: (3, 6), 18: (2, 7), 19: (2, 7), 20: (3, 6)},
    "col": {25: (17, 21), 26: (16, 22), 27: (16, 22), 28: (18, 21)},
    # THE BROOK PIECE (the fifth name on the shrine board): the bramble-walled nook in
    # the col's west corner, seen from the Rimeway road, reached only under the pine.
    "brook": {26: (4, 7), 27: (4, 7), 28: (4, 7)},
}
plot_of: dict[int, str] = {}
for name, spans in PLOTS.items():
    for y, (x0, x1) in spans.items():
        for x in range(x0, x1 + 1):
            stubble[y * W + x] = 1
            plot_of[y * W + x] = name
mk.fence_run(deco, W, H, 7, 8, 9)
mk.fence_run(deco, W, H, 11, 8, 13)                   # the stile at x=10
mk.fence_run(deco, W, H, 12, 13, 15)                  # gate at x 16 (the walk-up path)
mk.fence_run(deco, W, H, 2, 16, 6)
mk.fence_run(deco, W, H, 16, 24, 20)                  # the col plot's top, open at the drift

# ---- encounter beds ------------------------------------------------------------------
# The two crossings are BLOBBED (review fix 4) but stay unbroken: every row of the
# barley-drift overlaps the next, and the south crossing never thins below two rows,
# so neither can be walked round. Hard-edged tuft fill only (the classic convention).
DRIFT_OFF = [0, 0, 1, 1, 0, -1, -1, 0, 0, 1]          # rows 12..21
for k, y in enumerate(range(12, 22)):
    off = DRIFT_OFF[k]
    x0, x1 = 9 + off, 10 + off + (1 if y % 3 == 0 else 0)
    mk.rect(tuft, W, H, max(8, x0), y, min(11, x1), y)
# the south crossing (2026-10-14 second pass): not a ruled bar with rounded ends but
# a drift with LOBES on both edges — its top swells up toward the drift and the far
# east, its bottom sags into the col in three bellies — every run at least two
# columns long (no one-column spikes), never thinner than two rows, and every column
# a contiguous run wall to wall, so it can't be walked round.
CROSS_TOP = [21, 21, 22, 22, 22, 21, 21, 20, 20, 21, 21, 22, 22, 22, 21, 21, 20, 19,
             19, 21, 22, 22]                           # x = 2..23
CROSS_BOT = [23, 24, 24, 24, 23, 23, 24, 24, 25, 25, 24, 23, 23, 23, 23, 22, 22, 23,
             23, 23, 24, 24]
cross = mk.make_grid(W, H)
for k, x in enumerate(range(2, 24)):
    assert CROSS_BOT[k] - CROSS_TOP[k] >= 1, x
    mk.rect(tuft, W, H, x, CROSS_TOP[k], x, CROSS_BOT[k])
    mk.rect(cross, W, H, x, CROSS_TOP[k], x, CROSS_BOT[k])
mk.blob(tuft, W, H, 20.5, 4.8, 2.2, 1.6)               # upper terrace grind bed (optional)
mk.blob(tuft, W, H, 4.2, 6.2, 2.3, 1.5)                # the north mouth's verge: the low Dousecap bed
mk.blob(tuft, W, H, 2.8, 7.4, 1.2, 1.0)

# ---- precedence ------------------------------------------------------------------------
for i in range(W * H):
    if cliff[i]:
        tuft[i] = stubble[i] = 0
        deco[i] = 0
    if tuft[i]:
        stubble[i] = 0
for (x, y) in BANK:                                     # the bank tiles stay ledges
    tuft[y * W + x] = stubble[y * W + x] = 0

# ---- base --------------------------------------------------------------------------------
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
base = []
for i in range(W * H):
    base.append(rng.choice(bl) if rng.random() < 0.5 else bl[0])

# the deliberate fill layouts (pinned over the autotiler's fill cells)
FILL = ["stubble_fill", "stubble_fill_v1", "stubble_fill_v2", "stubble_fill_v3"]


def _plot_fill(name: str, x: int, y: int) -> str:
    if name == "hay":                      # cut swathes running on the diagonal
        return FILL[(x + 2 * y) % 4]
    if name == "sleepers":                 # drill rows, the ridges between in all four cuts
        return ("stubble_drill", "stubble_drill_v1")[(y // 2) % 2] if y % 2 == 0 \
            else FILL[(x // 2 + y) % 4]
    if name == "west":                     # drill rows on the other phase
        return "stubble_drill_v1" if y % 2 else FILL[(x + y // 2) % 4]
    return FILL[(x - y) % 4]               # the col plot: swathes the other way


pin: dict[tuple[int, int], str] = {}
for i, name in plot_of.items():
    x, y = i % W, i // W
    if not stubble[i]:
        continue
    if all(0 <= x + dx < W and 0 <= y + dy < H and stubble[(y + dy) * W + x + dx]
           for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
        pin[(x, y)] = _plot_fill(name, x, y)

m: dict = {
    "id": "mourning_fields", "display_name": "The Mourning Fields",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref(), COLDFOG_REF, FIELDS_REF],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/mourning-fields.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/mourning-fields-a.webp"],
    "ambience": {"particles": [{"kind": "motes", "density": 0.7}],
                 "mist": {"color": "#c9ced6", "alpha": 0.30, "speed": 3},
                 "tint": {"color": "#7d8796", "alpha": 0.14},
                 "starfall": {"min_s": 30, "max_s": 60},
                 "when": [{"flag": "flag:dawn", "ambience": {
                     "particles": [{"kind": "motes", "density": 0.5}],
                     "tint": {"color": "#c8a870", "alpha": 0.06}}}]},
}


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


# ---- warps ---------------------------------------------------------------------------
fk.edge_warps(m, wid="to_stillwater", cells=[(x, 0) for x in (2, 3, 4, 5)],
              to_map="stillwater", to=[(x, 28) for x in (22, 23, 24, 25)], facing="up")
fk.edge_warps(m, wid="to_coldfog", cells=[(0, y) for y in (11, 12, 13, 14)],
              to_map="coldfog_marches_i", to=[(18, y) for y in (11, 12, 13, 14)],
              facing="left", suffix="_s")
fk.edge_warps(m, wid="to_rimeway", cells=[(x, H - 1) for x in (10, 11, 12, 13)],
              to_map="rimeway_descent", to=[(x, 1) for x in (16, 17, 18, 19)], facing="down")

# ---- THE SLEEPERS (touch #1): asleep pre-dawn, awake (blanket folded) after ------------
SLEEPERS = [("snoozlet", (12, 15)), ("mothdim", (15, 15)), ("hushvole", (13, 18)),
            ("glowsip", (16, 18)), ("snoozlet", (15, 3)), ("hushvole", (18, 5)),
            ("mothdim", (3, 19)), ("glowsip", (19, 26))]
for n, (kin, (x, y)) in enumerate(SLEEPERS):
    obj(f"sleeper_{n}", f"mournfields_sleeper_{kin}", (x, y), 2, 2,
        hidden_when_flag="flag:dawn", bob=True)        # the slow 1px rise and fall of breath
    obj(f"sleeper_{n}_awake", f"mournfields_sleeper_{kin}_awake", (x, y), 2, 2,
        requires_flag="flag:dawn")

# ---- THE SCARECROW-LAMPS (touch #3) ------------------------------------------------------
SCARECROWS = [(6, 4), (14, 5), (8, 13), (18, 17), (4, 25), (15, 27), (22, 21)]
for n, (x, y) in enumerate(SCARECROWS):
    for state, flag in (("", "hidden_when_flag"), ("_lit", "requires_flag")):
        obj(f"scarecrow_{n}{state or '_dark'}", f"mournfields_scarecrow_lamp{state}",
            (x, y - 2), 1, 3, overhang=2, walk_under=True, **{flag: "flag:dawn"})

# ---- THE FIELD SHRINE (touch #2): seen from below, reached from above ---------------------
# the second dawn change (2026-10-14 second pass): all five field-candles burn again
# after flag:dawn — a flag-swapped twin on the same footprint + solidity
obj("field_shrine", "mournfields_field_shrine", (21, 13), 3, 3, hidden_when_flag="flag:dawn")
obj("field_shrine_lit", "mournfields_field_shrine_lit", (21, 13), 3, 3,
    requires_flag="flag:dawn")
for tx in (21, 22, 23):
    m["triggers"].append({"id": f"shrine_read_{tx}", "kind": "cutscene",
                          "at": {"tx": tx, "ty": 16}, "activation": "interact",
                          "ref": "script.mournfields_shrine"})
owed.append("script.mournfields_shrine")
owed += pt.cache(m, cid="mournfields_shelf", at=(23, 12))
owed += pt.cache(m, cid="mournfields_plot", at=(2, 20))    # the west plot's corner
# seen from the whole lower field across the crag, reached only up the one stair
owed += pt.cache(m, cid="mournfields_terrace", at=(23, 9))

# ---- stooks, blankets, the field furniture ------------------------------------------------
for n, (x, y) in enumerate([(8, 3), (11, 3), (9, 5), (12, 6), (17, 14),
                            (6, 17), (7, 19), (17, 25), (23, 25)]):
    obj(f"stook_{n}", "mournfields_stook", (x, y), 1, 2, overhang=1)
obj("blankets_a", "mournfields_blanket_stack", (13, 12), 2, 1)
obj("blankets_b", "mournfields_blanket_stack", (5, 12), 2, 1)
obj("notice", "coldfog_hollowing_notice", (18, 12), 1, 2, overhang=1)
m["triggers"].append({"id": "notice_read", "kind": "dialogue", "at": {"tx": 18, "ty": 13},
                      "activation": "interact", "ref": "sign.mournfields_notice"})
owed.append("sign.mournfields_notice")
obj("quiet_camp", "coldfog_quiet_camp", (2, 3), 3, 2)
obj("dead_willow", "coldfog_dead_willow", (21, 2), 3, 4, overhang=3, walk_under=True)
obj("col_pine", "hushfrost_snow_pine", (2, 26), 2, 3, overhang=2, walk_under=True)
obj("col_drift", "hushfrost_snowdrift", (19, 29 - 1), 3, 2)
obj("col_drift_b", "hushfrost_drift_a", (14, 29), 3, 1, solid=False)
obj("col_drift_c", "hushfrost_drift_c", (4, 29), 2, 1, solid=False)   # blown into the nook
obj("doused_lamp_a", "coldfog_doused_lamp", (8, 27), 1, 3, overhang=2, walk_under=True)

# ---- THE BROOK PIECE (2026-10-14 second pass, Exploration): the fifth field on the
# shrine board, and the only one with no road to it. A bramble-walled nook in the col's
# west corner: seen from the whole Rimeway road over its hedge, reached only through
# the long grass and under the snow pine's skirts (the trunk + the scarecrow seal the
# rest). Inside: the field-tender's own old kin, asleep alone under the best blanket,
# her marker stone, and what she left there.
BROOK_HEDGE = [(5, 25), (6, 25), (7, 25), (8, 25), (8, 26), (8, 27), (8, 28)]
for n, (x, y) in enumerate(BROOK_HEDGE):
    obj(f"brook_hedge_{n}", "mournfields_bramble", (x, y), 1, 1)
obj("brook_sleeper", "mournfields_sleeper_hushvole", (6, 26), 2, 2,
    hidden_when_flag="flag:dawn", bob=True)
obj("brook_sleeper_awake", "mournfields_sleeper_hushvole_awake", (6, 26), 2, 2,
    requires_flag="flag:dawn")
for (tx, ty) in ((6, 27), (7, 27)):
    m["triggers"].append({"id": f"brook_sleeper_{tx}", "kind": "cutscene",
                          "at": {"tx": tx, "ty": ty}, "activation": "interact",
                          "ref": "script.mournfields_brook_sleeper"})
owed.append("script.mournfields_brook_sleeper")
owed += pt.sign(m, deco, W, sid="mournfields_brook", at=(5, 26))
owed += pt.cache(m, cid="mournfields_brook", at=(7, 28))
# the plot furniture (review fix 1): a stile in the hay plot's fence, a plough left in
# the west plot's last drill; the bank's lip (fix 2): a bramble at each jog
obj("hay_stile", "mournfields_stile", (10, 7), 1, 2, solid=False)
obj("west_plough", "mournfields_plough", (5, 21), 2, 1)
obj("bank_bramble_w", "mournfields_bramble", (7, 10), 1, 1)
obj("bank_bramble_e", "mournfields_bramble", (11, 10), 1, 1)
# the ONE walk-up, stood on a landmark: stone steps cut in the crag, a rope rail, and
# beside it the only lantern in the Fields left with its hood up a slit
obj("bank_stair", "mournfields_bank_stair", (WALKUP, 10), 1, 2, solid=False)
obj("stair_lamp", "underways_watch_lamp", (16, 9), 1, 2, overhang=1, walk_under=True)

# ---- signs ----------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="mourning_fields", at=(3, 15))
owed += pt.sign(m, deco, W, sid="mournfields_col", at=(9, 28))

# ---- trainers (route class; the beats ARE the chokes) ------------------------------------
# Ines holds the head of the walk-up: everyone coming up x=17 steps onto (17,9)
owed += pt.trainer_beat(m, tid="mournfields_ines", at=(18, 9), facing="left", sight=2,
                        sprite="hollowing_acolyte")
# Corran stands beside the Rimeway road, looking across its whole width
owed += pt.trainer_beat(m, tid="mournfields_corran", at=(14, 26), facing="left", sight=4,
                        sprite="hollowing_acolyte")

# ---- people -------------------------------------------------------------------------------
m["npcs"] += [
    {"id": "field_tender", "at": {"tx": 14, "ty": 17}, "facing": "down",
     "sprite": "hollowing_elder", "movement": "static",
     "dialogue_ref": "script.mournfields_tender"},
    {"id": "gate_walker", "at": {"tx": 6, "ty": 13}, "facing": "left",
     "sprite": "pass_walker", "movement": "look_around",
     "dialogue_ref": "script.mournfields_walker"},
]
owed += ["script.mournfields_tender", "script.mournfields_walker"]

# ---- encounters --------------------------------------------------------------------------
NIGHT = [
    {"kin_id": 138, "weight": 22, "min_level": 49, "max_level": 51},  # Voidmantle
    {"kin_id": 113, "weight": 18, "min_level": 48, "max_level": 50},  # Omenire
    {"kin_id": 85, "weight": 16, "min_level": 49, "max_level": 51},   # Stillwarden
    {"kin_id": 125, "weight": 14, "min_level": 48, "max_level": 50},  # Crystalune
    {"kin_id": 58, "weight": 12, "min_level": 49, "max_level": 51},   # Mycelarch (the fallow's own)
    {"kin_id": 142, "weight": 10, "min_level": 50, "max_level": 52},  # Embergone
    {"kin_id": 135, "weight": 6, "min_level": 51, "max_level": 52},   # Liminalux
]
DAY = [
    {"kin_id": 127, "weight": 22, "min_level": 56, "max_level": 61},  # Lunvane
    {"kin_id": 58, "weight": 18, "min_level": 56, "max_level": 61},   # Mycelarch
    {"kin_id": 125, "weight": 16, "min_level": 57, "max_level": 62},  # Crystalune
    {"kin_id": 107, "weight": 14, "min_level": 57, "max_level": 62},  # Lunarbel
    {"kin_id": 140, "weight": 14, "min_level": 56, "max_level": 61},  # Wisprestored (woken)
    {"kin_id": 9, "weight": 10, "min_level": 57, "max_level": 62},    # Glimscout
    {"kin_id": 129, "weight": 6, "min_level": 60, "max_level": 62},   # Dawnwatcher
]
# The Hollowing family (Lane N4, #178-#180): the grey dream-moth keeps the field-kin
# asleep; the shuttered lantern-keeper walks the rows. Joins once the species exist.
if species_exists(180):
    NIGHT.append({"kin_id": 180, "weight": 14, "min_level": 48, "max_level": 51})
if species_exists(179):
    NIGHT.append({"kin_id": 179, "weight": 8, "min_level": 50, "max_level": 52})
# The north mouth's verge is a deliberately LOW bed (review fix 6): Dousecap kindles at
# 44, so it lives here at 42-44 — the snuffers nest in the stubble by the Stillwater
# road, the lampmaker's-yard band — with young Lullwing and Shutterwick.
DOUSE = [
    {"kin_id": 178, "weight": 60, "min_level": 42, "max_level": 44},  # Dousecap
    {"kin_id": 180, "weight": 25, "min_level": 46, "max_level": 48},  # Lullwing
    {"kin_id": 179, "weight": 15, "min_level": 47, "max_level": 49},  # Shutterwick
]
band = mk.make_grid(W, H)
patch = mk.make_grid(W, H)
verge = mk.make_grid(W, H)
for i in range(W * H):
    if tuft[i]:
        x, y = i % W, i // W
        if (8 <= x <= 11 and 12 <= y <= 21) or cross[i]:
            band[i] = 1
        elif x <= 6 and y <= 8:
            verge[i] = 1
        else:
            patch[i] = 1
zones = pt.zones_from_grid(patch, W, H, terrain="tall_grass", rate=0.11, table=NIGHT,
                           id_prefix="fields")
zones += pt.zones_from_grid(band, W, H, terrain="tall_grass", rate=0.08, table=NIGHT,
                            id_prefix="crossing")
zones += pt.zones_from_grid(verge, W, H, terrain="tall_grass", rate=0.12, table=DOUSE,
                            id_prefix="verge")
m["encounters"] = fk.night_day(zones, DAY)

# ---- dressing ------------------------------------------------------------------------------
avoid = fk.busy_cells(m)
avoid |= {(x, y) for y in range(H) for x in range(W)
          if cliff[y * W + x] or tuft[y * W + x] or deco[y * W + x]}
avoid |= {(x, 0) for x in range(2, 6)} | {(x, 1) for x in range(2, 6)}
avoid |= {(x, y) for x in range(10, 14) for y in range(24, 32)}       # the Rimeway road
avoid |= {(WALKUP, y) for y in range(8, 14)} | {(16, 13), (16, 12)}
avoid |= set(BANK) | {(x, 9) for x in range(2, 16)}                  # the bank's lip
# the Brook Piece's one way in (grass -> under the pine -> the nook): never a boulder
avoid |= {(x, y) for x in range(2, 8) for y in range(24, 30)}
# the plots' fringe: a tuft on every other cell of blight that rings a plot
for y in range(H):
    for x in range(W):
        i = y * W + x
        if stubble[i] or cliff[i] or tuft[i] or deco[i] or (x, y) in avoid:
            continue
        if any(0 <= x + dx < W and 0 <= y + dy < H and stubble[(y + dy) * W + x + dx]
               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) and (x + y) % 2 == 0:
            deco[i] = gid("g_tuft")
avoid |= {(x, y) for y in range(H) for x in range(W) if deco[y * W + x]}
avoid |= {(x, y) for x in range(20, 24) for y in range(12, 18)}       # the shrine shelf
litter = [gid("greymoss_a"), gid("greymoss_b"), gid("g_pebble"), gid("g_tuft")]
for y in range(H):
    for x in range(W):
        if (x, y) in avoid:
            continue
        r = rng.random()
        if stubble[y * W + x]:
            if r < 0.22:
                deco[y * W + x] = gid("g_pebble") if r < 0.08 else 0
        elif r < 0.03:
            deco[y * W + x] = gid("boulder")
        elif r < 0.20:
            deco[y * W + x] = rng.choice(litter)
crag_bits = [gid("boulder"), gid("greymoss_a"), gid("greymoss_b"), gid("g_pebble")]
for y in range(H):
    for x in range(W):
        i = y * W + x
        if cliff[i] and deco[i] == 0 and (x, y) not in fk.busy_cells(m) and rng.random() < 0.18:
            deco[i] = rng.choice(crag_bits)

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_stubble", "role": "terrain", "terrain": "stubble",
     "set": "mournfields_set", "depth": 0, "data": stubble},
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": tuft},
    {"name": "t_fogcrag", "role": "terrain", "terrain": "fogcrag",
     "set": "coldfog_set", "depth": 0, "data": cliff},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3, pin_base=pin)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
