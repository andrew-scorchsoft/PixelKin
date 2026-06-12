#!/usr/bin/env python3
"""
Penumbra Ring — the last dark, crossed on starlight (walkthrough
05-central-endgame "Penumbra Ring"; kind route (barrier), region central,
NO encounters — kin refuse the dark; rec. level ~52, pure traversal).

THE THRESHOLD REGISTER (README §10 + 05's Arc D note, BINDING): near-total
black, the lamp-glow the only colour within. ZERO humour — awe and held
breath. No NPCs walk the Ring; the only voices are two signs and the
threshold narration.

THE RECESSION IS FLAG-FREE DESIGN (orchestrator contract + spine §0 r2): by
the time the player can ENTER at all (`flag:hub_unlocked` gates the only
door), all four `crown_*` wedges have burned back — so the receded Penumbra
is simply the map's open basalt ground, rimmed by the void family; the only
remaining dark is the final crossings. No entered-edge logic, no flag-gated
tint: the design IS the recession.

Three signature touches (§8):
  1. THE SPIRE SEEN BEFORE WALKED (§3a r3) — the Umbral Spire's silhouette
     mass rises off the north rim from the moment the chasm bank is reached;
     the to_spire gate sits at its foot.
  2. THE SAFE LINE — sparse warm way-lamps (the only colour in the map) mark
     the walked S-bend lane between the void fields (§3a breadcrumb); the
     line STOPS at the chasm bank, where Còr's null-lanterns take over at the
     forecourt ("the safe line ends where his begins").
  3. WALKING ON STARS — the void tiles self-gate on Starreach (tileset
     metadata, the water/tidecall pattern — VERIFIED: void_* carry
     `requires_ability: starreach` + `collides`), and fallen-star glints
     mark the crossing lines, so stepping onto nothing reads as stepping
     onto starlight.

S-BENDS (§3a r11): entry apron -> WEST squeeze (the east wall finger) ->
EAST lane (west void field A, the islet cache in it) -> open relief rows ->
EAST lane again past the west void field B -> the bank -> the full-width
final chasm crossed on Starreach. With Starreach held the void fields
THEMSELVES are the return compressor (§3a r1/r2): the first pass follows the
lamps; the return can cut straight across the dark. (No ledge — the
asymmetry is the Gift, documented for the flow audit's `loop` WARN.)

validate_map `variation` WARN — waived: the >20-cell identical run is the
final chasm's `void_fill` row. The frozen shared set ships no void fill
VARIANTS by design (void_a2/a3 are the fill's ANIMATION frames, the
anti-light wisp register) — at runtime the chasm shimmers on a 1100ms
3-frame cycle, so the "stamped" read the check guards against never shows.

audit_flow waivers (documented per the skill contract):
  * `free-pass` / encounter checks — the Ring is canonically encounter-free
    (05 §6: "No encounter zones — kin refuse the dark"); the §11 r7 gameplay
    load is carried by the Starreach void crossings + the priced pockets.
  * `loop` — see above: the void fields are the earned return; a ledge or
    flag-shortcut would be redundant on a map the Gift already compresses.

PAID POCKETS (§3a r4 — the orchestrator contract applies off-path-pays even
here, overriding 05 §4's "no items" prose; deviation documented in the C1
report): the void-ringed ISLET in field A (a Starglass Shard — starlight
made stone, the of-the-place valuable) and the void-sealed SE pocket
(loose wicks). Both are Starreach-priced.

HANDSHAKE (verified + re-aimed, both sides edited): the crossroads'
`to_penumbra`/`to_penumbra_e` at crossroads (9,17)/(10,17) now land HERE at
(13,33)/(14,33) facing up, ON our return pair `to_crossroads`/`_e`, which
lands back at crossroads (9,17)/(10,17) facing up. (The old placeholder
landing (10,2) faced down at the north edge — it would have put the Spire
BEHIND the player; the seam flip is deliberate: the fade is a step through
the fog-wall, and the look-up moment demands the Spire at the top of the
map. build_crossroads.py + vesper_crossroads.json updated in this slot.)
HANDSHAKE (C2, binding on the Spire builder): our `to_spire`/`to_spire_e`
door warps at (13,5)/(14,5) (step_on, transition door, on the silhouette's
visible gate, requires_ability starreach per graph.ts:251) land at
umbral_spire (13,30)/(14,30) facing up — PLACEHOLDER until C2 authors it
(the engine no-ops; the coldfog->nightreach contract style). C2's map must
keep those landings WALKABLE and its return pair must land at our
(13,6)/(14,6) (the doorstep row), facing down.
HANDSHAKE (C1-internal, built both sides): our `to_starwell`/`to_starwell_s`
at (27,13)/(27,14) (Starreach, graph.ts:235) land at starwell (0,8)/(0,9)
ON its return pair, which lands back at our (27,13)/(27,14).

Story band: `script.penumbra_threshold` (atmosphere only — narrate +
silence; NO progression flag) on the entry choke's two walkable cells.
`flag:penumbra_threshold_seen` is PRESENTATIONAL bookkeeping only (the
standing once-only band mechanism, the `flag:gift_first_*` precedent) —
05 §6's "no flags set" means no *progression* flags, and nothing consumes
this one.

Suggested copy (wiring agent C3; sincere, elegiac, zero humour):
  script.penumbra_threshold  narrate: "The dark here has edges. It has
                             drawn back from the roads you lit — and what
                             is left of it does not want you." + a held
                             silence. No flag a gate would read.
  sign.penumbra_ascent       "THE NINTH LANTERN. The road up is starlight
                             or nothing. Lamps out of respect; hearts lit
                             out of spite." (the 'now accessible' callout
                             at the bank, where the ascent first becomes
                             steppable)
  sign.penumbra_starwell     "EAST — THE STARWELL. Where a star fell and
                             did not go out. Step soft on the dark."
                             (the X3 chart's tease-closer made ground truth)
  npc.penumbra_tended_row    (the NW forecourt wing's read): "Two null-
                             lanterns, tended and swept, holding no light
                             with great care. Someone still walks this row."
  npc.penumbra_snuffed_shrine (the west squeeze's read): "A wayshrine of the
                             old inward road. Its lamp was not broken — it
                             was put out, gently, the way you'd close a
                             sleeping kin's door."
  script.pickup_penumbra_shard  Starglass Shard (valuable) + the find line
  script.pickup_penumbra_wicks  loose wicks (~600w, giveMoney) + the find line

Run:  ./venv/bin/python tools/maps/build_penumbra_ring.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 28, 34
rng = random.Random(151)
owed: list[str] = []

# ---- terrain presence grids ---------------------------------------------------------
wall = mk.make_grid(W, H)   # basaltwall masses
void = mk.make_grid(W, H)   # the remaining dark (self-gates on Starreach)
deco = mk.make_grid(W, H)

# BORDERS: basaltwall all round; the north rim runs 5 deep (the Spire's roots)
mk.rect(wall, W, H, 0, 0, W - 1, 4)            # north rim (rows 0-4)
mk.rect(wall, W, H, 0, 32, W - 1, 33)          # south (rows 32-33)
mk.rect(wall, W, H, 0, 0, 1, H - 1)            # west
mk.rect(wall, W, H, 26, 0, 27, H - 1)          # east
mk.organic_border(wall, W, H, depth=0,
                  bumps=[(1, 7, 2), (1, 17, 2), (1, 27, 2),
                         (26, 7, 2), (26, 21, 2), (7, 32, 2), (19, 32, 2)],
                  rng=rng)
# SOUTH gap — the entry from the crossroads (cols 13-14)
for y in (32, 33):
    for x in (13, 14):
        wall[y * W + x] = 0
# EAST gap — the Starwell mouth (rows 13-14)
for x in (26, 27):
    for y in (13, 14):
        wall[y * W + x] = 0

# F1 — the east wall finger that folds the lane west (§3a r11 bend 1)
mk.rect(wall, W, H, 9, 27, 25, 28)

# ---- the remaining dark --------------------------------------------------------------
# THE FINAL CHASM: full width between the bank and the Spire's forecourt
mk.rect(void, W, H, 2, 9, 25, 11)
# field B (west, mid-north): folds the lane east toward the Starwell turn
mk.blob(void, W, H, 7.0, 14.0, 6.0, 2.8)
# the Starwell strait: two starlit steps east of the lane
mk.rect(void, W, H, 24, 12, 25, 16)
# field A (west, mid-south): folds the lane east; holds the ISLET cache
mk.blob(void, W, H, 7.0, 21.5, 5.5, 3.0)
# the SE void-sealed pocket (sealed by F1 / the south border / the east border)
mk.blob(void, W, H, 21.5, 30.0, 2.8, 2.2)
mk.rect(void, W, H, 24, 29, 25, 31)
# the SW receded wedge at the threshold (the recession, read at a glance)
mk.blob(void, W, H, 4.0, 30.0, 2.5, 2.0)

# the ISLET (field A) and the pocket's dry cells — cleared ground in the dark
for (x, y) in [(6, 21), (7, 21), (21, 30), (22, 30)]:
    void[y * W + x] = 0

# ---- precedence ----------------------------------------------------------------------
for i in range(W * H):
    if wall[i]:
        void[i] = 0

terrain_layers = [
    {"name": "t_void", "role": "terrain", "terrain": "void",
     "set": "vesper_overworld_set", "depth": 0, "data": void},
    {"name": "t_basaltwall", "role": "terrain", "terrain": "basaltwall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- base: basalt everywhere (the burned-back ground) --------------------------------
bs = [gid("basalt0"), gid("basalt1"), gid("basalt2")]
base = [rng.choice(bs) if rng.random() < 0.5 else bs[0] for _ in range(W * H)]

m: dict = {
    "id": "penumbra_ring", "display_name": "Penumbra Ring",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/penumbra-ring-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/penumbra-ring-a.webp",
        "assets/backgrounds/battle/penumbra-ring-b.webp",
    ],
}

# ---- warps (graph.ts edge ids verbatim) ----------------------------------------------
m["warps"] += [
    # SOUTH <-> vesper_crossroads (`to_penumbra` edge; the only door in)
    {"id": "to_crossroads", "at": {"tx": 13, "ty": 33}, "trigger": "step_on",
     "to_map": "vesper_crossroads", "to": {"tx": 9, "ty": 17}, "facing": "up",
     "transition": "fade"},
    {"id": "to_crossroads_e", "at": {"tx": 14, "ty": 33}, "trigger": "step_on",
     "to_map": "vesper_crossroads", "to": {"tx": 10, "ty": 17}, "facing": "up",
     "transition": "fade"},
    # EAST <-> starwell (`to_starwell`, Starreach — the landmark, graph.ts:235)
    {"id": "to_starwell", "at": {"tx": 27, "ty": 13}, "trigger": "step_on",
     "to_map": "starwell", "to": {"tx": 0, "ty": 8}, "facing": "right",
     "requires_ability": "starreach", "transition": "fade"},
    {"id": "to_starwell_s", "at": {"tx": 27, "ty": 14}, "trigger": "step_on",
     "to_map": "starwell", "to": {"tx": 0, "ty": 9}, "facing": "right",
     "requires_ability": "starreach", "transition": "fade"},
    # NORTH -> umbral_spire (`to_spire`, Starreach, graph.ts:251) — the gate
    # doors on the silhouette's visible arch; PLACEHOLDER landing, C2 lands it
    # (see HANDSHAKE in the docstring; the engine no-ops until authored).
    {"id": "to_spire", "at": {"tx": 13, "ty": 5}, "trigger": "step_on",
     "to_map": "umbral_spire", "to": {"tx": 13, "ty": 30}, "facing": "up",
     "requires_ability": "starreach", "transition": "door"},
    {"id": "to_spire_e", "at": {"tx": 14, "ty": 5}, "trigger": "step_on",
     "to_map": "umbral_spire", "to": {"tx": 14, "ty": 30}, "facing": "up",
     "requires_ability": "starreach", "transition": "door"},
]

# ---- THE SPIRE, SEEN BEFORE WALKED (touch #1) -----------------------------------------
# The silhouette mass rides the north rim; its bottom row is the gate row
# (y5, ground), so the to_spire doors sit ON the visible arch (§11 r5b).
m["objects"].append(
    {"id": "spire_silhouette", "sprite": "penumbra_spire_silhouette",
     "at": {"tx": 9, "ty": 0}, "w": 10, "h": 6, "overhang": 5})
# Còr's null-lanterns flank the forecourt — the safe line ends where his begins
deco[7 * W + 10] = gid("null_lantern")
deco[7 * W + 17] = gid("null_lantern")
# …and the TENDED ROW on the forecourt's west wing (the B-arc dread, gentle:
# someone still walks this row — and pays the NW pocket per §3a r4)
deco[6 * W + 3] = gid("null_lantern")
deco[6 * W + 5] = gid("null_lantern")
m["triggers"].append(
    {"id": "penumbra_tended_row", "kind": "dialogue",
     "at": {"tx": 4, "ty": 7}, "activation": "interact",
     "ref": "npc.penumbra_tended_row"})
owed += ["npc.penumbra_tended_row (the tended-row read — see docstring)"]

# THE SNUFFED WAYSHRINE on the old inward road (west squeeze; pays the SW
# strip per §3a r4 — a lore payoff, not an item, keeping 05 §4's spirit)
m["objects"].append(
    {"id": "snuffed_shrine", "sprite": "glowmoss_deep_null_lantern_shrine",
     "at": {"tx": 2, "ty": 26}, "w": 2, "h": 3, "overhang": 2})
for i, tx in enumerate((2, 3)):
    m["triggers"].append(
        {"id": f"snuffed_shrine_read_{i}", "kind": "dialogue",
         "at": {"tx": tx, "ty": 29}, "activation": "interact",
         "ref": "npc.penumbra_snuffed_shrine"})
owed += ["npc.penumbra_snuffed_shrine (the wayshrine read — see docstring)"]

# ---- THE SAFE LINE (touch #2): warm way-lamps marking the walked S-bend ---------------
for n, (x, y) in enumerate([
        (15, 29),   # beside the entry gap (trunk 15,31)
        (5, 25),    # into the west squeeze (trunk 5,27)
        (12, 23),   # the crossover row (trunk 12,25)
        (16, 18),   # the lane past field A (trunk 16,20)
        (15, 15),   # the lane past field B (trunk 15,17)
        (16, 10),   # the bank, where the line stops (trunk 16,12)
]):
    m["objects"].append(
        {"id": f"way_lamp_{n}", "sprite": "penumbra_way_lamp",
         "at": {"tx": x, "ty": y}, "w": 1, "h": 3, "overhang": 2,
         "walk_under": True})

# ---- WALKING ON STARS (touch #3): glints on the Starreach crossing lines --------------
def glint(gx: int, gy: int, variant: str) -> None:
    assert void[gy * W + gx], f"starglint ({gx},{gy}) must sit on a void cell"
    m["objects"].append(
        {"id": f"starglint_{gx}_{gy}", "sprite": f"penumbra_starglint_bright_{variant}",
         "at": {"tx": gx, "ty": gy}, "w": 1, "h": 1, "solid": False,
         "walk_under": True})

glint(14, 9, "a")    # the chasm crossing line, under the gate
glint(15, 10, "b")
glint(14, 11, "a")
glint(20, 9, "b")    # a far fallen star on the chasm's east reach
glint(24, 13, "b")   # the Starwell strait
glint(25, 14, "a")
glint(11, 21, "b")   # the islet approach (field A)
glint(9, 22, "a")
glint(20, 29, "b")   # the SE pocket's dark

# ---- the threshold narrate-band (atmosphere only — see docstring) ---------------------
for i, tx in enumerate((13, 14)):
    m["triggers"].append(
        {"id": f"penumbra_threshold_{i}", "kind": "script",
         "at": {"tx": tx, "ty": 32}, "activation": "step_on",
         "ref": "script.penumbra_threshold",
         "sets_flags": ["flag:penumbra_threshold_seen"],
         "hidden_when_flag": "flag:penumbra_threshold_seen"})
owed += ["script.penumbra_threshold (narrate + silence; atmosphere only — see docstring)"]

# ---- signs (the why + the come-back, §3a r8) ------------------------------------------
owed += pt.sign(m, deco, W, sid="penumbra_ascent", at=(18, 12))    # the bank callout
owed += pt.sign(m, deco, W, sid="penumbra_starwell", at=(21, 16))  # the landmark turn

# ---- paid pockets (§3a r4 — both Starreach-priced; see docstring deviation note) ------
owed += pt.cache(m, cid="penumbra_shard", at=(6, 21))    # Starglass Shard, the islet
owed += pt.cache(m, cid="penumbra_wicks", at=(21, 30))   # loose wicks, the SE pocket

# ---- drained dressing (sparse — the register is emptiness, coldfog II's weight) -------
for (x, y, n) in [(4, 6, "greymoss_a"), (22, 7, "greymoss_b"), (3, 13, "greymoss_a"),
                  (12, 17, "greymoss_b"), (23, 22, "greymoss_a"), (9, 25, "greymoss_b"),
                  (17, 26, "greymoss_a"), (11, 30, "greymoss_b")]:
    if deco[y * W + x] == 0 and not wall[y * W + x] and not void[y * W + x]:
        deco[y * W + x] = gid(n)
for (x, y) in [(20, 6), (6, 8), (19, 17), (3, 18), (14, 21), (22, 25), (10, 29),
               (17, 30), (5, 13), (21, 12)]:
    if deco[y * W + x] == 0 and not wall[y * W + x] and not void[y * W + x]:
        deco[y * W + x] = gid("g_pebble")
# a boulder cluster as the mid-field outcrop (never a wall slab — §11 r8)
for (x, y) in [(3, 17), (4, 18), (23, 25), (24, 26), (23, 26)]:
    if deco[y * W + x] == 0 and not wall[y * W + x] and not void[y * W + x]:
        deco[y * W + x] = gid("boulder")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + \
    terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
