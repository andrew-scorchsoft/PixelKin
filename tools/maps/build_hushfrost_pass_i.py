#!/usr/bin/env python3
"""
Hushfrost Pass I — the snow canyon (walkthrough/04-west "Hushfrost Pass I→II"
beat 1-2; kind route, region west, band 40-42).

Arc D: the loneliest leg of the game — you step off Pale Vault's aurora ice
into a snowed canyon, deepBlue ice walls, your lamp the only warmth; the cold
still presses but the light is *less lonely* than the glacier. Lone-bell-voice
register. Three signature touches (§8):
  1. THE COLDFOG THROAT (west) — the canyon's far throat choked with the
     Hollowing's mist, grey moss creeping at its lip: the first place
     Emberward is REQUIRED (the genre's earned crossing, paid one region
     after the Gift). Gated warp pair + the sincere sign; the pass-tender
     stands at the lip with the walkthrough's hook line.
  2. THE SHELTERED SNOW-HOLLOWS — frosttuft pockets tucked out of the wind
     (the cold roster's beds), one hiding the §4 [MISSABLE] cache in the
     SE wall-hollow beyond the lamp's easy reach (authored toward the
     Lamplight axis — optional only).
  3. THE WIND-BLOWN TERRACE — the mid-canyon snow shelf (the §11 r3
     elevation accent): climb in from the north, hop the south ledge back
     down (§3a r1 — the route's one-way earned return).

HANDSHAKE (N3, binding): pale_vault_glacier `to_pass` warps at (0,10)/(0,11)
land HERE at (30,10)/(30,11) — both walkable; our return pair `to_glacier`
at (31,10)/(31,11) lands at glacier (1,10)/(1,11). Boundary `to_pass_ii`
(graph.ts verbatim, requires_ability emberward — held on entry to the West)
at the throat (0,14)/(0,15), landing hushfrost_pass_ii (28,19)/(28,20)
(W1 authors both sides; pass_ii return pair lands at our (1,14)/(1,15)).

Trainer beats (progression.mjs Hushfrost leg, route class — the wiring agent
authors TRAINERS + payout 16 x ace):
  hushfrost_lampman   "Coldfog lampman", 2 kin lv41 — tends a failing lamp at
                      the west chamber, eyeing the fog. payout 656.
  hushfrost_survivor  "Pass survivor", 1 kin lv42 — wrapped in furs on the
                      south corridor, walking OUT of the cold. payout 672.

Encounter picks (the hooks name flavour reads with no designed rows — the N1
Kiteling precedent; mapped to real species, band 40-42, continuous with Pale
Vault 36-40):
  ice-burrower (Frost)     -> #84 Hushbore (the literal burrowing ice-rodent;
                              its silence aura IS the hush of the pass)
  frost-wisp (Frost/Light) -> #86 Prismcub (the only wild Frost/Light line;
                              prism-fur scattering aurora light)
  + NEWLY PLACED (previously unplaced kin): #78 Crystarn (Chillpip's mid
    stage — Windward continuity), #75 Geodrake (Geolace's mid stage,
    Windward II continuity), #82 Vortexlope (Blizzrhare's KINDLED form —
    the glacier's hares grown into blizzard-speed adults, rare)
  + continuity: #81 Blizzrhare, #95 Glacewing (their Pale Vault bands walk
    east into the canyon).
  Mirror into EXTRA_ENCOUNTERS (tools/balance/build_species.py) = wiring agent.

Suggested sign copy (the wiring agent writes dialogue.ts; the cold register
allows AT MOST one dry line — it's the marker; the coldfog sign is sincere):
  sign.hushfrost_marker  "HUSHFROST PASS. Pale Vault: behind you. The warmth:
                          allegedly ahead. The pass-tender counts anyone who
                          reads this aloud as company, and thanks them."
  sign.hushfrost_coldfog "The coldfog holds the throat. No ordinary flame
                          walks through — only a warded one. Beyond, the
                          canyon thins toward a remembered warmth."
                          (sincere — the boundary gate's why; also the
                          to_pass_ii blocked_ref, though Emberward is held
                          on any legitimate arrival)

audit_flow notes — the terrace ledge is the route's one-way return (§3a r1);
the SE wall-hollow cache is a paid dead end by design (§3a r4).

Run:  ./venv/bin/python tools/maps/build_hushfrost_pass_i.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 32, 28
rng = random.Random(74)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
glacier = mk.make_grid(W, H)    # canyon walls + the two banks
cliff = mk.make_grid(W, H)      # the wind-blown terrace rim (stone register)
snowtrail = mk.make_grid(W, H)  # the trodden lane
frosttuft = mk.make_grid(W, H)  # encounter hollows + the mandatory crossings
deco = mk.make_grid(W, H)

# BORDERS: glacier crag all round, 2 deep, organic bumps (§11 r2)
mk.rect(glacier, W, H, 0, 0, W - 1, 1)              # north
mk.rect(glacier, W, H, 0, 26, W - 1, H - 1)         # south
mk.rect(glacier, W, H, 0, 0, 1, H - 1)              # west
mk.rect(glacier, W, H, 30, 0, 31, H - 1)            # east
mk.organic_border(glacier, W, H, depth=0,
                  bumps=[(7, 1, 2), (18, 2, 2), (27, 1, 2), (1, 21, 2),
                         (12, 27, 2), (23, 26, 2), (30, 22, 2), (1, 8, 2)],
                  rng=rng)
# EAST gap from the glacier (rows 10-11; landings (30,10)/(30,11) walkable,
# our return warps ON x31)
for x in (30, 31):
    for y in (10, 11):
        glacier[y * W + x] = 0
# WEST gap — the coldfog throat (rows 14-15)
for x in (0, 1):
    for y in (14, 15):
        glacier[y * W + x] = 0

# THE TWO BANKS (S-bend rule §3a r11: the canyon folds the path 4 times)
mk.rect(glacier, W, H, 21, 2, 22, 19)   # bank A — passage runs SOUTH of it
mk.rect(glacier, W, H, 8, 8, 9, 25)     # bank B — passage runs NORTH of it

# seal the empty crag pockets the carve left (audit_flow dead-end rule: a
# detour either PAYS or doesn't exist — these three paid nothing)
mk.rect(glacier, W, H, 2, 2, 7, 4)      # NW shelf above the high lane
mk.rect(glacier, W, H, 8, 2, 16, 3)     # north strip over bank B's head
mk.rect(glacier, W, H, 24, 24, 29, 25)  # SE strip under the wall-hollow

# ---- the wind-blown terrace (elevation accent + the one-way return, §11 r3) --------
# Climb in from the NORTH gap, loot the shelf, hop the south ledge back down
# onto the south corridor — returning travellers skip the climb. Hand-rolled
# in the SNOW register (pt.terrace stamps the grass-context cliff + grass
# ledge — wrong family here): glacier rim, snow_ledge_s lip.
mk.hline(glacier, W, H, 16, 13, 19)     # north rim (gap carved below)
mk.vline(glacier, W, H, 13, 16, 18)     # west rim
mk.vline(glacier, W, H, 19, 16, 18)     # east rim
for x in (15, 16):
    glacier[16 * W + x] = 0             # the climb-in gap
pt.ledge_run(deco, W, H, 19, 14, 18, rng, family="snow")  # the one-way hop down

# ---- the lane (snowtrail on snow — context-correct) --------------------------------
mk.hline(snowtrail, W, H, 10, 26, 29)               # entry shelf rows
mk.hline(snowtrail, W, H, 11, 26, 29)
mk.vline(snowtrail, W, H, 25, 10, 20)               # bend 1: south past bank A
mk.vline(snowtrail, W, H, 26, 10, 20)
mk.hline(snowtrail, W, H, 21, 12, 25)               # the south corridor (wind-blown)
mk.hline(snowtrail, W, H, 22, 12, 25)
mk.vline(snowtrail, W, H, 11, 6, 22)                # bend 2: north up the mid chamber
mk.vline(snowtrail, W, H, 12, 6, 22)
mk.hline(snowtrail, W, H, 5, 3, 11)                 # bend 3: west over bank B's head
mk.hline(snowtrail, W, H, 6, 3, 11)
mk.vline(snowtrail, W, H, 3, 6, 15)                 # bend 4: south down the west chamber
mk.vline(snowtrail, W, H, 4, 6, 15)
mk.hline(snowtrail, W, H, 14, 1, 4)                 # the throat approach
mk.hline(snowtrail, W, H, 15, 1, 4)

# ---- encounter terrain -------------------------------------------------------------
# sheltered snow-hollows (optional pockets, rate 0.11)
mk.blob(frosttuft, W, H, 26.5, 5.0, 2.8, 1.6)       # NE hollow (off the entry)
mk.blob(frosttuft, W, H, 26.5, 18.5, 2.6, 2.4)      # SE wall-hollow (the missable)
mk.blob(frosttuft, W, H, 16.0, 17.8, 2.4, 1.2)      # ON the terrace (priced pocket)
mk.blob(frosttuft, W, H, 5.0, 20.0, 2.2, 1.6)       # SW hollow under bank B
# MANDATORY crossings (§11 r7): full-corridor bands, the lane paused through
pt.mandatory_band(frosttuft, snowtrail, W, H, y0=13, y1=14, x0=10, x1=20)  # mid leg
pt.mandatory_band(frosttuft, snowtrail, W, H, y0=10, y1=11, x0=2, x1=7)    # west leg

# ---- precedence (structure wins; lane wins over tufts) -----------------------------
for i in range(W * H):
    if glacier[i] or cliff[i]:
        snowtrail[i] = 0
        frosttuft[i] = 0
    if snowtrail[i]:
        frosttuft[i] = 0

# ---- base: bone snow ---------------------------------------------------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_snowtrail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": snowtrail},
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
]

m: dict = {
    "id": "hushfrost_pass_i", "display_name": "Hushfrost Pass",
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
    # EAST <-> pale_vault_glacier (the N3 handshake — see module docstring)
    {"id": "to_glacier", "at": {"tx": 31, "ty": 10}, "trigger": "step_on",
     "to_map": "pale_vault_glacier", "to": {"tx": 1, "ty": 10}, "facing": "right",
     "transition": "fade"},
    {"id": "to_glacier_s", "at": {"tx": 31, "ty": 11}, "trigger": "step_on",
     "to_map": "pale_vault_glacier", "to": {"tx": 1, "ty": 11}, "facing": "right",
     "transition": "fade"},
    # WEST — THE COLDFOG THROAT -> hushfrost_pass_ii (`to_pass_ii`,
    # requires_ability emberward — the first place the Gift is REQUIRED)
    {"id": "to_pass_ii", "at": {"tx": 0, "ty": 14}, "trigger": "step_on",
     "to_map": "hushfrost_pass_ii", "to": {"tx": 28, "ty": 19}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.hushfrost_coldfog", "transition": "fade"},
    {"id": "to_pass_ii_s", "at": {"tx": 0, "ty": 15}, "trigger": "step_on",
     "to_map": "hushfrost_pass_ii", "to": {"tx": 28, "ty": 20}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.hushfrost_coldfog", "transition": "fade"},
]

# ---- objects: lamps beside the lane (the only warmth), the throat dressing ---------
m["objects"] += [
    # lamp posts beside (never on) the lit lane — sparse: the lonely register
    {"id": "lamp_entry", "sprite": "tinderwick_lamp_post", "at": {"tx": 27, "ty": 8},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_corridor", "sprite": "tinderwick_lamp_post", "at": {"tx": 13, "ty": 19},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_north", "sprite": "tinderwick_lamp_post", "at": {"tx": 6, "ty": 3},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_throat", "sprite": "tinderwick_lamp_post", "at": {"tx": 5, "ty": 12},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # ice spires flanking the coldfog throat (the Pale Vault register carried on)
    {"id": "spires_throat", "sprite": "pale_vault_ice_spire", "at": {"tx": 1, "ty": 11},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "spires_entry", "sprite": "pale_vault_ice_spire", "at": {"tx": 28, "ty": 13},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- signs -------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="hushfrost_marker", at=(27, 12))   # THE one dry line
owed += pt.sign(m, deco, W, sid="hushfrost_coldfog", at=(2, 13))   # sincere gate

# ---- trainer beats (sight trainers ARE geometry; wiring agent authors) -------------
owed += pt.trainer_beat(m, tid="hushfrost_lampman", at=(3, 17), facing="up",
                        sight=3, sprite="npc_man")
owed += pt.trainer_beat(m, tid="hushfrost_survivor", at=(14, 21), facing="right",
                        sight=4, sprite="npc_woman")

# ---- the pass-tender at the throat (walkthrough hook, ref verbatim) ----------------
m["npcs"].append(
    {"id": "hushfrost_pass_tender", "at": {"tx": 2, "ty": 16}, "facing": "up",
     "sprite": "npc_old_man", "movement": "static",
     "dialogue_ref": "npc.hushfrost_pass_tender"})
owed += ["npc.hushfrost_pass_tender (the hook line: the fog 'wasn't here last "
         "winter'; mind the kin on the far side — they've gone quiet)"]

# ---- caches (variety: loose wicks + consumable + the missable valuable) ------------
owed += pt.cache(m, cid="hushfrost_wicks", at=(28, 5))    # loose wicks (~300), NE hollow
owed += pt.cache(m, cid="hushfrost_balm", at=(17, 18))    # consumable, ON the terrace
owed += pt.cache(m, cid="hushfrost_shard", at=(28, 19))   # Starglass Shard — the §4
                                                          # [MISSABLE] SE wall-hollow
                                                          # (a Lamplight-flavoured nook)

# ---- encounters (band 40-42, continuous with Pale Vault 36-40 / pass II 40-42) -----
TABLE = [{"kin_id": 84, "weight": 24, "min_level": 40, "max_level": 42},
         {"kin_id": 78, "weight": 20, "min_level": 40, "max_level": 42},
         {"kin_id": 75, "weight": 16, "min_level": 40, "max_level": 41},
         {"kin_id": 81, "weight": 14, "min_level": 40, "max_level": 41},
         {"kin_id": 86, "weight": 10, "min_level": 40, "max_level": 41},
         {"kin_id": 95, "weight": 8, "min_level": 40, "max_level": 41},
         {"kin_id": 82, "weight": 8, "min_level": 41, "max_level": 42}]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if frosttuft[i]:
        (band_grid if (i // W) in (13, 14, 10, 11) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE, id_prefix="hollow")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE, id_prefix="crossing")

# ---- throat dressing: grey moss where the fog gnaws (B-arc whisper, no props) ------
for (x, y, n) in [(1, 13, "greymoss_a"), (2, 17, "greymoss_b"), (1, 16, "greymoss_a"),
                  (4, 16, "greymoss_b")]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid(n)

# ---- scatter + boulders ------------------------------------------------------------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (glacier, cliff, snowtrail, frosttuft))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
mk.scatter_decor(deco, base, W, H, rng, density=0.15, avoid=avoid)
for (x, y) in [(24, 4), (29, 7), (18, 4), (14, 8), (5, 8), (2, 21),
               (13, 24), (24, 24), (28, 23), (19, 9), (6, 24)]:
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
