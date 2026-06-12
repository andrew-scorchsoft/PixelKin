#!/usr/bin/env python3
"""
Hollowfen Stillworks — the derelict null-works (walkthrough/04-west, the B4
SET-PIECE's shown half; kind cave (landmark), region outer, band 48-51,
level-design §2a LATE-LANDMARK tier: compact, 1 floor / 2 rooms, the prize a
gate beyond the obvious).

WHAT THIS ROOM HAS TO DO (binding tone — README §10 + 04-west §2): show the
Hollowing at scale, and make it read MERCIFUL-AND-WRONG. Not capes — industry.
Not evil — care. Rows of dead null-lanterns hang on swept gantries; the
draining machinery is a polished font with its gauge resting at zero; every
lamp in here is SLEEPING, NOT DEAD, and someone clearly still dusts the
collars. The horror is the tenderness. Grief at scale, never cruelty; the kin
are asleep, never harmed; ZERO humour.

Composition (the merciful-and-wrong staging):
  ROOM 1 — THE GALLERY (south): the long hall the door opens into. Four
    null-lantern racks in two clean rows, a swept centre aisle, the
    husk-keeper standing among the racks like a sexton among graves. NO
    encounters here — you walk among sleeping lamps in silence.
  THE CHOKE (centre): a 2-wide passage; the B4 NARRATIVE BAND sits on it
    (every walkable tile of the cut — it cannot be walked around). It sets
    NO progression flag: `flag:great_null_known` is Nessa's, at Nightreach
    (hooks verbatim: the detour is optional, the flag can't depend on it).
    The band's local once-flag is bookkeeping only.
  ROOM 2 — THE MACHINE ROOM (north): the works' centrepiece against the far
    wall — the null-engine, a bell of held dark on cradle-pipes (drawn kit:
    coldfog_null_engine) — a dead-still murk sump where the drained fen
    seeps in, the works' store alcove (the valuable cache), and the BLIGHT
    BEDS at the engine's foot where the one thing still awake in the
    building sleeps lightly: the CHARGED HUSK.

THE CHARGED HUSK (hooks: "a powerful Storm/Dark 'charged husk' kin... as a
low-weight/static reward"): #143 WHORLIX (Storm/Dark, tier C — the roster's
one Storm/Dark, its only designed habitat row IS coldfog_marches). The engine
has no wild-static battle mechanic, so the closest data-true staging is the
W2 pattern: a TINY dedicated bed at the engine's foot (the husk's cradle,
4 cells, hot rate) where Whorlix carries the table — findable like a static,
catchable like a wild. The gallery-side bed runs the works' general roster
with Whorlix at low weight. Wiring agent mirrors into EXTRA_ENCOUNTERS.

HANDSHAKE (W3-internal, built both sides): II's `to_stillworks`/`_e` door
warps at (14,6)/(15,6) (Glimmerstep — the INNER door; Emberward got you into
Coldfog II at all; graph.ts:227) land HERE at (11,19)/(12,19), within 1 of
our return pair `to_marches`/`to_marches_e` at (11,20)/(12,20), which lands
back at II's doorstep (14,7)/(15,7).

audit_flow waiver — `loop`: a compact in-and-out landmark by design (§2a
late-spur tier — the glowmoss_deep waiver class; the loop lives at region
scale). Story band proven by the choke check.

Suggested copy (wiring agent; the hooks' line VERBATIM in the keeper's
mouth; zero humour):
  npc.hollowfen_husk_keeper  "Every lamp in here is sleeping, not dead.
    That's the horror of it — and the mercy he believes in. One day the
    whole sky's meant to look like this room."
  script.hollowfen_stillworks  (the B4 band — realises the hooks' ref
    `cutscene.hollowfen_stillworks` in the engine's convention: trigger kind
    'cutscene', ref 'script.*' — the glowmoss_drained precedent. Staging per
    docs/world/cinematics.md "a light fails": letterbox + silence as the
    machine room opens; NO sting resolve; narrate the rows of sleeping
    lanterns; end on the gauge at zero. Sets flag:seen_stillworks only —
    NEVER flag:great_null_known.)
  script.pickup_coldfog_works_store  (the store alcove valuable)

Run:  ./venv/bin/python tools/maps/build_hollowfen_stillworks.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 22
rng = random.Random(79)
owed: list[str] = []

# ---- carve the works from solid rock/wall -------------------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)                # wall everywhere…

floor = mk.make_grid(W, H)                             # …the carved works
mk.rect(floor, W, H, 4, 2, 19, 8)                      # ROOM 2 — the machine room
mk.rect(floor, W, H, 11, 9, 12, 10)                    # THE CHOKE (2 wide — the band)
mk.rect(floor, W, H, 4, 11, 19, 16)                    # ROOM 1 — the gallery
mk.rect(floor, W, H, 10, 17, 13, 19)                   # the vestibule
mk.rect(floor, W, H, 11, 20, 12, 20)                   # the doorway (return warps)
mk.rect(floor, W, H, 2, 4, 3, 6)                       # the works' store alcove (W)
for i in range(W * H):
    if floor[i]:
        wall[i] = 0

# ---- the dead sump (murk seeping in, NE of the machine room) ------------------------
murk = mk.make_grid(W, H)
mk.blob(murk, W, H, 18.0, 6.0, 1.7, 1.4)
for i in range(W * H):
    if murk[i] and not floor[i]:
        murk[i] = 0

# ---- the blight beds (the fen through the floor) ------------------------------------
cradle = mk.make_grid(W, H)                            # the husk's cradle (4 cells)
for (x, y) in [(10, 7), (11, 7), (12, 7), (13, 7)]:
    cradle[y * W + x] = 1
works_bed = mk.make_grid(W, H)                         # the general works bed (W side)
mk.blob(works_bed, W, H, 6.0, 5.0, 1.8, 1.4)
for g in (cradle, works_bed):
    for i in range(W * H):
        if g[i] and (not floor[i] or murk[i]):
            g[i] = 0

# ---- base + terrain layers -----------------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]

blighttuft = mk.make_grid(W, H)
for i in range(W * H):
    if cradle[i] or works_bed[i]:
        blighttuft[i] = 1

terrain_layers = [
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": blighttuft},
    {"name": "t_murk", "role": "terrain", "terrain": "murk",
     "set": "vesper_overworld_set", "depth": 0, "data": murk},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

m: dict = {
    "id": "hollowfen_stillworks", "display_name": "Hollowfen Stillworks",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/coldfog-marches-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/coldfog-marches-a.webp",
        "assets/backgrounds/battle/coldfog-marches-b.webp",
    ],
}

# ---- warps (the door pair back to Coldfog II) ----------------------------------------
m["warps"] += [
    {"id": "to_marches", "at": {"tx": 11, "ty": 20}, "trigger": "step_on",
     "to_map": "coldfog_marches_ii", "to": {"tx": 14, "ty": 7}, "facing": "down",
     "transition": "door"},
    {"id": "to_marches_e", "at": {"tx": 12, "ty": 20}, "trigger": "step_on",
     "to_map": "coldfog_marches_ii", "to": {"tx": 15, "ty": 7}, "facing": "down",
     "transition": "door"},
]

# ---- ROOM 1: the gallery — racks in clean rows, the keeper among them ----------------
m["objects"] += [
    {"id": "rack_nw", "sprite": "coldfog_null_rack",
     "at": {"tx": 5, "ty": 11}, "w": 4, "h": 2, "overhang": 1},
    {"id": "rack_ne", "sprite": "coldfog_null_rack",
     "at": {"tx": 15, "ty": 11}, "w": 4, "h": 2, "overhang": 1},
    {"id": "rack_sw", "sprite": "coldfog_null_rack",
     "at": {"tx": 6, "ty": 14}, "w": 4, "h": 2, "overhang": 1},
    {"id": "rack_se", "sprite": "coldfog_null_rack",
     "at": {"tx": 14, "ty": 14}, "w": 4, "h": 2, "overhang": 1},
]
m["npcs"].append(
    {"id": "husk_keeper", "at": {"tx": 13, "ty": 13}, "facing": "left",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "npc.hollowfen_husk_keeper"})
owed += ["npc.hollowfen_husk_keeper (the hooks' 'sleeping, not dead' line "
         "VERBATIM — the sexton among graves; zero humour)"]

# ---- THE CHOKE: the B4 narrative band (every walkable tile of the cut) ---------------
for i, tx in enumerate((11, 12)):
    m["triggers"].append(
        {"id": f"stillworks_reveal_{i}", "kind": "cutscene",
         "at": {"tx": tx, "ty": 9}, "activation": "step_on",
         "ref": "script.hollowfen_stillworks", "once": True,
         "sets_flags": ["flag:seen_stillworks"],
         "hidden_when_flag": "flag:seen_stillworks"})
owed += ["script.hollowfen_stillworks (the B4 band — atmosphere/foreshadow "
         "ONLY; sets flag:seen_stillworks, NEVER flag:great_null_known — "
         "that is Nessa's at Nightreach; cinematics 'a light fails' cadence)"]

# ---- ROOM 2: the machine room — the engine against the far wall ----------------------
m["objects"] += [
    # the centrepiece: top rows over the wall face, flush (the wall_mount read)
    {"id": "null_engine", "sprite": "coldfog_null_engine",
     "at": {"tx": 9, "ty": 1}, "w": 6, "h": 5, "overhang": 2},
    # one shrine in the west bay (a lamp brought in for its rest)
    {"id": "shrine_bay", "sprite": "glowmoss_deep_null_lantern_shrine",
     "at": {"tx": 5, "ty": 2}, "w": 2, "h": 3, "overhang": 2},
    # the intake rack on the east bay — lamps waiting their turn at the engine
    {"id": "rack_intake", "sprite": "coldfog_null_rack",
     "at": {"tx": 15, "ty": 2}, "w": 4, "h": 2, "overhang": 1},
]
# the engine's read (interact at its foot — the gauge at zero)
for i, tx in enumerate((11, 12)):
    m["triggers"].append(
        {"id": f"engine_read_{i}", "kind": "dialogue",
         "at": {"tx": tx, "ty": 5}, "activation": "interact",
         "ref": "npc.hollowfen_engine"})
owed += ["npc.hollowfen_engine (the gauge-at-zero read: a font someone "
         "polishes daily; merciful and wrong)"]

# ---- the store alcove cache (the works' valuable) ------------------------------------
owed += pt.cache(m, cid="coldfog_works_store", at=(2, 5))

# ---- encounters ----------------------------------------------------------------------
# the husk's cradle: Whorlix-led, hot, 4 cells — the static-read reward
TABLE_HUSK = [
    {"kin_id": 143, "weight": 55, "min_level": 50, "max_level": 51},  # WHORLIX
    {"kin_id": 137, "weight": 45, "min_level": 48, "max_level": 50},  # Nullmoth
]
# the works' general bed: the deep roster, Whorlix rare
TABLE_WORKS = [
    {"kin_id": 137, "weight": 40, "min_level": 48, "max_level": 50},  # Nullmoth
    {"kin_id": 139, "weight": 28, "min_level": 48, "max_level": 50},  # WispwaneNull
    {"kin_id": 142, "weight": 20, "min_level": 49, "max_level": 50},  # Embergone
    {"kin_id": 143, "weight": 12, "min_level": 50, "max_level": 51},  # Whorlix
]
m["encounters"] += pt.zones_from_grid(cradle, W, H, terrain="tall_grass",
                                      rate=0.18, table=TABLE_HUSK,
                                      id_prefix="cradle", min_cells=2)
m["encounters"] += pt.zones_from_grid(works_bed, W, H, terrain="tall_grass",
                                      rate=0.10, table=TABLE_WORKS,
                                      id_prefix="works")

# ---- dressing: grey moss in the seams, swept floor otherwise -------------------------
deco = mk.make_grid(W, H)
for (x, y, n) in [(4, 8, "greymoss_a"), (16, 8, "greymoss_b"), (19, 6, "greymoss_a"),
                  (5, 13, "greymoss_b"), (18, 13, "greymoss_a"), (4, 16, "greymoss_b"),
                  (13, 17, "greymoss_a"), (15, 4, "greymoss_b")]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid(n)
for (x, y) in [(7, 8), (14, 12), (10, 16), (17, 15), (4, 4), (19, 12)]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid("g_pebble")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
