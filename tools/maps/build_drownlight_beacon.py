#!/usr/bin/env python3
"""
Drownlight Beacon — the snuffed lighthouse (walkthrough/04-west §4 optional:
"spur off coldfog_marches_ii, requires_ability: emberward; reward: rare DARK
kin in a snuffed lighthouse. [MISSABLE]"; kind route (spur), region outer,
band 48-50, one screen).

THE LONELIEST PLACE IN THE GAME (the dread register at its quietest): a
drowned-dark tower base on a spit in the dead shallows. No NPC. No music
change, no warmth, no humour. The light that kept the fen-road is out; the
door is swollen shut; nobody answers. Everything is still TENDED-looking —
nothing broken (README §10: grief dressed as mercy) — just... out.

Three signature touches (§8):
  1. THE TOWER ITSELF (drawn kit: coldfog_lighthouse) — dark lamp room,
     waterline stain, the door swollen shut with its read (npc.drownlight_door).
  2. THE DEAD SHALLOWS AS THE WORLD'S EDGE — murk to every horizon except the
     entry crag; off-map is continuation (more drowned fen, forever).
  3. THE KEEPER'S CACHE — one paid find on a murk islet (Tidecall-priced,
     §3a r4): what the last keeper left, set out neat.

HANDSHAKE (W3-internal, built both sides): II's `to_beacon`/`to_beacon_s` at
(0,12)/(0,13) land HERE at (16,7)/(16,8) ON our return pair `to_marches` /
`to_marches_s` at (17,7)/(17,8), which lands back at II's (1,12)/(1,13) —
both directions Emberward (graph.ts:226), blocked_ref sign.coldfog_beacon
(authored on II; this side reuses it for symmetry).

Encounter reconciliation (the W2 precedent): the RARE DARK bed —
#138 Voidmantle (Dark, rare — its designed coldfog_marches row lands here,
the spur its rarity earns), #135 Liminalux (Dark/Light, very_rare — the
threshold-kin; a snuffed lighthouse is the game's most liminal ground),
#137 Nullmoth, #134 Wispwane. Band 48-50. Murk: NO zone (dead water).
Wiring agent mirrors into EXTRA_ENCOUNTERS.

audit_flow waiver — `loop`: a one-screen in-and-out SPUR by design
(level-design §2a late-landmark tier: "compact"; the §3a r1 loop lives at the
REGION scale — hub -> marches -> beacon -> back is the priced detour). Same
waiver class as the East's first-dungeon note in build_glowmoss_deep.py.

Suggested copy (wiring agent; zero humour):
  npc.drownlight_door  "The door has swollen shut against its frame. Salt and
                        years hold it better than any lock. High above, the
                        lamp room keeps its dark."

Run:  ./venv/bin/python tools/maps/build_drownlight_beacon.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 18, 16
rng = random.Random(78)
owed: list[str] = []

COLDFOG_REF = mk.register_tileset(
    "coldfog_set", index=mk.REPO / "assets/tilesets/coldfog/coldfog_set.index.json")

# ---- terrain presence grids --------------------------------------------------------
crag = mk.make_grid(W, H)       # the entry-side crag + a north anchor
murk = mk.make_grid(W, H)       # the dead shallows — the world's edge here
blighttuft = mk.make_grid(W, H) # the rare Dark bed
deco = mk.make_grid(W, H)

# EAST border crag (the gate side, continuous with II's west wall) + a north lip
mk.rect(crag, W, H, 16, 0, 17, H - 1)
mk.rect(crag, W, H, 0, 0, W - 1, 0)
mk.organic_border(crag, W, H, depth=0,
                  bumps=[(16, 3, 2), (9, 0, 2), (16, 12, 2)], rng=rng)
# the gate gap (rows 7-8)
for x in (16, 17):
    for y in (7, 8):
        crag[y * W + x] = 0

# the dead shallows: south, west and north-west margins drown (off-map = more
# of the same, forever)
mk.rect(murk, W, H, 0, 12, W - 1, H - 1)
mk.rect(murk, W, H, 0, 0, 1, H - 1)
mk.blob(murk, W, H, 1.5, 4.0, 2.6, 2.6)
mk.blob(murk, W, H, 4.0, 13.0, 4.0, 2.4)
mk.blob(murk, W, H, 12.0, 13.5, 4.4, 2.6)
mk.blob(murk, W, H, 1.0, 9.5, 2.2, 1.8)
mk.blob(murk, W, H, 8.5, 1.5, 2.0, 1.2)
# the spit stays dry: carve the walked ground back out of the water
for (cx, cy, rx, ry) in [(11.0, 8.0, 4.5, 2.2), (6.0, 6.5, 3.5, 2.6),
                         (4.5, 9.5, 2.5, 1.8)]:
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if 0 <= x < W and 0 <= y < H and \
                    ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                murk[y * W + x] = 0
# the keeper's islet (the paid cache, Tidecall-priced — a true islet, water
# on every side)
for (x, y) in [(11, 13), (12, 13)]:
    murk[y * W + x] = 0

# ---- the rare Dark bed (small, hot — §3a r12: optional patches run hot) -------------
mk.blob(blighttuft, W, H, 8.5, 5.0, 2.2, 1.3)          # at the tower's foot
mk.blob(blighttuft, W, H, 12.5, 6.5, 1.6, 1.1)         # the spit-side pocket

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if crag[i]:
        murk[i] = 0
        blighttuft[i] = 0
    if murk[i]:
        blighttuft[i] = 0

# ---- base: blight (the drowned ground) ----------------------------------------------
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
    "id": "drownlight_beacon", "display_name": "Drownlight Beacon",
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

# ---- warps (graph.ts `to_beacon` edge, both directions Emberward) -------------------
m["warps"] += [
    {"id": "to_marches", "at": {"tx": 17, "ty": 7}, "trigger": "step_on",
     "to_map": "coldfog_marches_ii", "to": {"tx": 1, "ty": 12}, "facing": "right",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_beacon", "transition": "fade"},
    {"id": "to_marches_s", "at": {"tx": 17, "ty": 8}, "trigger": "step_on",
     "to_map": "coldfog_marches_ii", "to": {"tx": 1, "ty": 13}, "facing": "right",
     "requires_ability": "emberward",
     "blocked_ref": "sign.coldfog_beacon", "transition": "fade"},
]

# ---- the tower (touch #1) ------------------------------------------------------------
m["objects"].append(
    {"id": "drownlight_tower", "sprite": "coldfog_lighthouse",
     "at": {"tx": 3, "ty": 1}, "w": 4, "h": 7, "overhang": 4})
# the swollen door's read (the only voice on the map)
for i, tx in enumerate((4, 5)):
    m["triggers"].append(
        {"id": f"drownlight_door_{i}", "kind": "dialogue",
         "at": {"tx": tx, "ty": 7}, "activation": "interact",
         "ref": "npc.drownlight_door"})
owed += ["npc.drownlight_door (the swollen-shut door read — see docstring)"]

# one dark reed-lantern where the fen-road once landed (the keeper's last)
m["objects"].append(
    {"id": "dead_lantern", "sprite": "saltreach_reed_lantern_dark",
     "at": {"tx": 13, "ty": 6}, "w": 1, "h": 2, "overhang": 1,
     "walk_under": True})

# ---- the keeper's cache (touch #3 — the ONE paid find, on the islet) ----------------
owed += pt.cache(m, cid="coldfog_keepers_cache", at=(11, 13))

# ---- encounters (the rare Dark bed; band 48-50; murk dead) ---------------------------
TABLE_BEACON = [
    {"kin_id": 138, "weight": 30, "min_level": 49, "max_level": 50},  # Voidmantle
    {"kin_id": 137, "weight": 35, "min_level": 48, "max_level": 49},  # Nullmoth
    {"kin_id": 134, "weight": 22, "min_level": 48, "max_level": 50},  # Wispwane
    {"kin_id": 135, "weight": 8, "min_level": 49, "max_level": 50},   # Liminalux
]
m["encounters"] += pt.zones_from_grid(blighttuft, W, H, terrain="tall_grass",
                                      rate=0.14, table=TABLE_BEACON, id_prefix="bed")

# ---- drained dressing ----------------------------------------------------------------
for (x, y, n) in [(7, 9, "greymoss_a"), (11, 10, "greymoss_b"), (3, 8, "greymoss_a"),
                  (13, 9, "greymoss_b"), (8, 3, "greymoss_b"), (14, 4, "greymoss_a"),
                  (2, 11, "greymoss_b"), (12, 11, "greymoss_a")]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid(n)
for (x, y) in [(9, 9), (12, 5), (7, 11), (14, 10), (10, 3), (3, 10)]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid("g_pebble")
for (x, y) in [(8, 10), (14, 7), (10, 4), (2, 6)]:
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
