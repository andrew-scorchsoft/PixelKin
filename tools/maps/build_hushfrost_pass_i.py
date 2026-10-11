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
  4. THE SHELTER NOOK (W8 MIN-2 — the §3a mid-leg relief beat, the N6/N7
     Windward rest-shelf precedent): an ice-spire windbreak + a lamp tucked
     against the mid chamber's east side, just past the mid crossing
     (~halfway up the ~60-step leg). Encounter-free open snow, NO heal —
     the lonely register holds; this is pressure relief, not an anchor.

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


R10 RECOMPOSE (2026-10, the world-craft panel's "grey-slab maze" finding):
the banks, lane and encounter beds keep their topology, warps, trainers,
caches and contracts, but every ruled rectangle is gone. The two banks are
wind-carved ridges of varying width (blob chains), the trodden lane meanders
1-2 tiles wide, the frost-tuft hollows and both mandatory crossings have
ragged organic outlines (area kept within +-15% of the shipped 80 tiles, same
tables), the lane is gone (trackless snow: lamps, cairns and live footprints carry
the way), an ice pool and drift props break the open snow, and every
screen has a focal point from the West prop kit: the FROZEN FALLS (north),
wind-carved outcrops, the ice-locked cart (SW), cairns at the turns and the
PASS-WALKER'S CAMP beside the fallen-star crater. The crater, cinder and the
pass-walker ride tools/maps/add_peril_thread.py (re-run it after this
builder); the R4 day-form zones and the Radiant hollow cache are post-build
additions re-applied from the shipped JSON after a rebuild (they live in the
JSON, not here).

Run:  ./venv/bin/python tools/maps/build_hushfrost_pass_i.py
"""
from __future__ import annotations
import math
import random
import mapkit as mk
import patterns as pt
from mapkit import gid
import hushfrost_craft as hc

W, H = 32, 28
rng = random.Random(74)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
glacier = mk.make_grid(W, H)    # canyon walls + the two wind-carved banks
cliff = mk.make_grid(W, H)      # (unused: the snow register keeps to glacier rims)
snowtrail = mk.make_grid(W, H)  # the trodden lane (meandering, 1-2 wide)
frosttuft = mk.make_grid(W, H)  # encounter hollows + the mandatory crossings
snowpatch = mk.make_grid(W, H)  # wind-drifted snow (texture, no gameplay)
ice = mk.make_grid(W, H)        # the frozen pool under the falls (walkable)
deco = mk.make_grid(W, H)


def stroke(g, pts, r, val=1):
    """Stamp discs of radius r along a polyline (dense) — an organic lane/ridge."""
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(bx - ax, by - ay) * 4))
        for k in range(n + 1):
            px, py = ax + (bx - ax) * k / n, ay + (by - ay) * k / n
            for y in range(int(py - r) - 1, int(py + r) + 2):
                for x in range(int(px - r) - 1, int(px + r) + 2):
                    if 0 <= x < W and 0 <= y < H and \
                            (x + 0.5 - px) ** 2 + (y + 0.5 - py) ** 2 <= r * r:
                        g[y * W + x] = val


# BORDERS: glacier crag all round, 2 deep, organic bumps (§11 r2)
mk.rect(glacier, W, H, 0, 0, W - 1, 1)              # north
mk.rect(glacier, W, H, 0, 26, W - 1, H - 1)         # south
mk.rect(glacier, W, H, 0, 0, 1, H - 1)              # west
mk.rect(glacier, W, H, 30, 0, 31, H - 1)            # east
mk.organic_border(glacier, W, H, depth=0,
                  bumps=[(7, 1, 2), (27, 1, 2), (1, 21, 2), (12, 27, 2), (23, 26, 2),
                         (30, 22, 2), (1, 8, 2), (30, 4, 1), (5, 26, 1)],
                  rng=rng)

# THE TWO BANKS — wind-carved ridges, not slabs: blob chains of varying width
# (S-bend rule §3a r11: the canyon still folds the path 4 times).
BANK_A = {1: (20, 23), 2: (20, 24), 3: (20, 24), 4: (19, 23), 5: (20, 22), 6: (21, 22),
          7: (20, 23), 8: (19, 23), 9: (18, 23), 10: (18, 22), 11: (19, 22), 12: (20, 23),
          13: (21, 23), 14: (21, 24), 15: (20, 24), 16: (20, 23), 17: (20, 22), 18: (20, 23),
          19: (21, 22)}                           # bank A — passage runs SOUTH of it
BANK_B = {8: (8, 9), 9: (7, 9), 10: (8, 10), 11: (8, 10), 12: (7, 10), 13: (6, 9), 14: (7, 9),
          15: (8, 10), 16: (8, 10), 17: (9, 10), 18: (8, 10), 19: (7, 9), 20: (6, 9),
          21: (6, 8), 22: (7, 9), 23: (8, 10), 24: (8, 10), 25: (8, 10)}  # bank B — passage N of it
for bank in (BANK_A, BANK_B):
    for y, (x0, x1) in bank.items():
        mk.hline(glacier, W, H, y, x0, x1)

# sealed crag pockets (the audit_flow dead-end rule — paid nothing), now organic
mk.blob(glacier, W, H, 4.5, 2.8, 3.2, 1.6)        # NW shelf above the high lane
mk.blob(glacier, W, H, 12.0, 2.4, 4.6, 1.3)       # north strip over bank B's head
mk.blob(glacier, W, H, 27.5, 25.0, 2.8, 1.4)      # SE strip under the wall-hollow

# EAST gap from the glacier (rows 10-11; landings (30,10)/(30,11) walkable,
# our return warps ON x31) + WEST gap — the coldfog throat (rows 14-15)
for (x, y) in [(30, 10), (31, 10), (30, 11), (31, 11), (0, 14), (1, 14), (0, 15), (1, 15)]:
    glacier[y * W + x] = 0

# ---- the wind-blown terrace (elevation accent + the one-way return, §11 r3) --------
mk.hline(glacier, W, H, 16, 13, 19)     # north rim (gap carved below)
mk.vline(glacier, W, H, 13, 16, 18)     # west rim
mk.vline(glacier, W, H, 19, 16, 18)     # east rim
for x in (15, 16):
    glacier[16 * W + x] = 0             # the climb-in gap
for y in (17, 18):
    for x in range(14, 19):
        glacier[y * W + x] = 0          # keep the shelf itself open (bank A bulge)
pt.ledge_run(deco, W, H, 19, 14, 18, rng, family="snow")  # the one-way hop down

# ---- no trodden lane: the pass is trackless snow. The lamps, cairns and the
# player's own footprints (ambience footprints:'all', worldcraft/west.py) carry
# the way — the old 2-wide grey snowtrail read as ruled slabs.

# ---- encounter terrain (hard-edged fill, organic outline) --------------------------
# sheltered snow-hollows (optional pockets, rate 0.11)
mk.blob(frosttuft, W, H, 25.5, 4.6, 1.8, 1.1)       # NE hollow (off the entry)
mk.blob(frosttuft, W, H, 27.8, 5.6, 1.6, 1.1)
mk.blob(frosttuft, W, H, 27.0, 18.0, 1.8, 1.6)      # SE wall-hollow (the missable)
mk.blob(frosttuft, W, H, 28.3, 19.9, 1.3, 1.1)
mk.blob(frosttuft, W, H, 26.0, 20.0, 1.0, 0.7)
mk.blob(frosttuft, W, H, 16.0, 17.8, 2.4, 1.2)      # ON the terrace (priced pocket)
mk.blob(frosttuft, W, H, 4.6, 19.6, 1.8, 1.1)       # SW hollow under bank B
mk.blob(frosttuft, W, H, 5.6, 21.0, 1.6, 1.0)
# MANDATORY crossings (§11 r7): every open cell of the corridor between the
# banks, rows 13-14 (mid) / 10-11 (west), plus a ragged lip so the edge isn't ruled.
band = mk.make_grid(W, H)
TOP_UP = {9, 10, 14, 15, 19}          # columns whose band reaches a row higher
BOT_DN = {11, 12, 16, 17}              # ...or a row lower (a ragged, wind-cut edge)
for x in range(7, 23):
    for y in range(13 - (x in TOP_UP), 15 + (x in BOT_DN)):
        band[y * W + x] = 1
for x in range(2, 9):
    for y in range(10 - (x in {3, 4}), 12 + (x in {2, 7})):
        band[y * W + x] = 1
for i in range(W * H):
    if band[i] and not glacier[i]:
        frosttuft[i] = 1
        snowtrail[i] = 0

# ---- the frozen pool (texture: walkable floor, no gameplay) ------------------------
# (the falls carry their own frozen plunge-pool in the art). R10 polish: two
# wind-cleared ice sheets break the open snow — NW under the high lane, and E by
# the cairn bend (walkable floor: the lane is unchanged).
mk.blob(ice, W, H, 4.4, 6.6, 1.7, 0.9)
mk.blob(ice, W, H, 26.8, 14.4, 1.3, 0.8)

# ---- precedence (structure wins; lane wins over tufts; texture loses to all) -------
for i in range(W * H):
    if glacier[i] or cliff[i]:
        snowtrail[i] = frosttuft[i] = snowpatch[i] = ice[i] = 0
    if snowtrail[i]:
        frosttuft[i] = 0
    if snowtrail[i] or frosttuft[i] or ice[i]:
        snowpatch[i] = 0
    if snowtrail[i] or frosttuft[i]:
        ice[i] = 0

# ---- base: bone snow ---------------------------------------------------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_snowpatch", "role": "terrain", "terrain": "snowpatch",
     "set": "vesper_overworld_set", "depth": 0, "data": snowpatch},
    {"name": "t_ice", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": ice},
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
    {"id": "to_glacier", "at": {"tx": 31, "ty": 10}, "trigger": "step_on",
     "to_map": "pale_vault_glacier", "to": {"tx": 1, "ty": 10}, "facing": "right",
     "transition": "fade"},
    {"id": "to_glacier_s", "at": {"tx": 31, "ty": 11}, "trigger": "step_on",
     "to_map": "pale_vault_glacier", "to": {"tx": 1, "ty": 11}, "facing": "right",
     "transition": "fade"},
    {"id": "to_pass_ii", "at": {"tx": 0, "ty": 14}, "trigger": "step_on",
     "to_map": "hushfrost_pass_ii", "to": {"tx": 28, "ty": 19}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.hushfrost_coldfog", "transition": "fade"},
    {"id": "to_pass_ii_s", "at": {"tx": 0, "ty": 15}, "trigger": "step_on",
     "to_map": "hushfrost_pass_ii", "to": {"tx": 28, "ty": 20}, "facing": "left",
     "requires_ability": "emberward",
     "blocked_ref": "sign.hushfrost_coldfog", "transition": "fade"},
]


def obj(oid, sprite, x, y, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": x, "ty": y}, "w": w, "h": h}
    o.update(kw)
    return o


# ---- objects -----------------------------------------------------------------------
m["objects"] += [
    # lamp posts beside (never on) the lit lane — sparse: the lonely register
    obj("lamp_entry", "tinderwick_lamp_post", 27, 8, 1, 3, overhang=2, walk_under=True),
    obj("lamp_corridor", "tinderwick_lamp_post", 13, 19, 1, 3, overhang=2, walk_under=True),
    obj("lamp_north", "tinderwick_lamp_post", 6, 3, 1, 3, overhang=2, walk_under=True),
    obj("lamp_throat", "tinderwick_lamp_post", 5, 12, 1, 3, overhang=2, walk_under=True),
    # ice spires flanking the coldfog throat + the entry (Pale Vault carried on)
    obj("spires_throat", "pale_vault_ice_spire", 1, 11, 2, 3, overhang=2, walk_under=True),
    obj("spires_entry", "pale_vault_ice_spire", 28, 13, 2, 3, overhang=2, walk_under=True),
    # THE SHELTER NOOK (W8 MIN-2): ice-spire windbreak + its lamp, no heal
    obj("spires_shelter_w", "pale_vault_ice_spire", 13, 7, 2, 3, overhang=2, walk_under=True),
    obj("spires_shelter_e", "pale_vault_ice_spire", 16, 7, 2, 3, overhang=2, walk_under=True),
    obj("lamp_shelter", "tinderwick_lamp_post", 15, 8, 1, 3, overhang=2, walk_under=True),
    # R10 — the pass reads as a PLACE: one focal point per screen.
    # The frozen falls pour out of the north crag into their ice pool (the
    # mid chamber's landmark, seen from the whole north half).
    obj("frozen_falls", "hushfrost_frozen_falls", 17, 1, 3, 4),
    # wind-carved outcrops (boulder clusters, never cliff slabs — §11 r8)
    obj("outcrop_north", "hushfrost_rock_outcrop_a", 13, 4, 3, 2),
    obj("outcrop_ne", "hushfrost_rock_outcrop_b", 25, 2, 2, 2),
    obj("outcrop_ne_b", "hushfrost_rock_outcrop_b", 28, 7, 2, 2),
    obj("outcrop_south", "hushfrost_rock_outcrop_a", 11, 24, 3, 2),
    # the ice-locked cart in the SW drift — somebody's load, left to the cold
    obj("iced_cart", "hushfrost_iced_cart", 2, 24, 3, 2),
    # drifts banked against the windward walls
    obj("drift_mid", "hushfrost_snowdrift", 16, 11, 3, 2),
    obj("drift_se", "hushfrost_snowdrift", 27, 22, 3, 2),
    # cairns at the turns (the pass-walkers' waymarks)
    obj("cairn_bend", "windward_cairn", 25, 12, 2, 3, overhang=2, walk_under=True),
    obj("cairn_throat", "windward_cairn", 5, 7, 2, 3, overhang=2, walk_under=True),
    # THE PASS-WALKER'S CAMP beside the fallen star (her peril NPC stands at (21,22))
    obj("walker_camp", "hushfrost_walker_camp", 22, 23, 4, 3),
]

# ---- signs -------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="hushfrost_marker", at=(27, 12))   # THE one dry line
owed += pt.sign(m, deco, W, sid="hushfrost_coldfog", at=(2, 13))   # sincere gate
# the falls nook pays (§3a r4): read the frozen falls, one quiet line
m["triggers"].append({"id": "falls_read", "kind": "script", "at": {"tx": 18, "ty": 4},
                      "activation": "interact", "ref": "script.hushfrost_falls"})

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

# ---- caches (variety: loose wicks + consumable + the missable valuable) ------------
owed += pt.cache(m, cid="hushfrost_wicks", at=(28, 5))
owed += pt.cache(m, cid="hushfrost_balm", at=(17, 18))
owed += pt.cache(m, cid="hushfrost_shard", at=(28, 19))

# ---- encounters (band 40-42; tables are the shipped ones, re-applied post-build) ---
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
        (band_grid if band[i] else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE, id_prefix="hollow")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE, id_prefix="crossing")
print("frosttuft tiles:", sum(frosttuft), "(shipped 80; keep 68-92)")

# ---- throat dressing: grey moss where the fog gnaws (B-arc whisper) ----------------
for (x, y, n) in [(1, 13, "greymoss_a"), (2, 17, "greymoss_b"), (1, 16, "greymoss_a"),
                  (4, 16, "greymoss_b"), (2, 18, "greymoss_a"), (1, 12, "greymoss_b")]:
    if deco[y * W + x] == 0 and not glacier[y * W + x]:
        deco[y * W + x] = gid(n)

# ---- scatter: loose stones on the open snow (never on lane/beds/objects) -----------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (glacier, cliff, snowtrail, frosttuft, ice))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
# keep clear: the crater (add_peril_thread), the pass-walker, the landings
reserved = {(x, y) for x in range(15, 21) for y in range(22, 26)} | {(21, 22)} | \
           {(30, 10), (30, 11), (1, 14), (1, 15), (24, 21), (25, 21)}
avoid = covered | object_cells | point_cells | reserved
for (x, y) in [(24, 4), (18, 4), (5, 9), (2, 21), (24, 24), (19, 9), (29, 16),
               (23, 19), (16, 20), (6, 19), (10, 8), (26, 15), (20, 7)]:
    if (x, y) not in avoid and deco[y * W + x] == 0:
        deco[y * W + x] = gid("boulder")
pebble = [gid("g_pebble")]
for y in range(H):
    for x in range(W):
        if (x, y) not in avoid and deco[y * W + x] == 0 and rng.random() < 0.06:
            deco[y * W + x] = rng.choice(pebble)

# ground decals (id, sprite, x, y, w, h): wind-sculpted drift ridges with their
# blue lee shadows, rock + scree where the wind stripped the snow, the boot-prints
# of earlier walkers along the way you'll go (all solid:false).
GROUND = [
    ("hf1_drift_nw", "drift_b", 8, 5, 4, 2), ("hf1_drift_mid", "drift_a", 11, 10, 3, 1),
    ("hf1_drift_entry", "drift_b", 25, 9, 4, 2), ("hf1_drift_s", "drift_a", 12, 22, 3, 1),
    ("hf1_drift_sw", "drift_c", 3, 22, 2, 1), ("hf1_drift_se", "drift_c", 25, 16, 2, 1),
    ("hf1_drift_n", "drift_c", 3, 8, 2, 1),
    ("hf1_scree_n", "scree_b", 12, 6, 3, 2), ("hf1_scree_c", "scree_a", 11, 17, 2, 2),
    ("hf1_scree_sw", "scree_a", 5, 22, 2, 2),
    ("hf1_tracks_entry", "tracks_h", 24, 11, 4, 1), ("hf1_tracks_s", "tracks_h", 17, 21, 4, 1),
    ("hf1_tracks_c", "tracks_v", 12, 16, 1, 4), ("hf1_tracks_n", "tracks_h", 8, 7, 4, 1),
]
# low lee-mist strips that drift OVER the player (overhang = height)
MIST = [("hf1_mist_n", "mist_a", 7, 4, 6, 1), ("hf1_mist_s", "mist_b", 10, 23, 4, 1),
        ("hf1_mist_e", "mist_b", 24, 13, 4, 1)]
# solid props — ONLY on ground that was already solid (bank tops, the borders) or
# in dead corners off every lane; pines on the south border are FOREGROUND crowns
# you walk under (trunk on the crag, crown over the snow).
PROPS = [
    hc.prop("hf1_pine_n1", "hushfrost_snow_pine_big", 8, 0, 3, 4, overhang=3),
    hc.prop("hf1_pine_n2", "hushfrost_snow_pine", 2, 1, 2, 3, overhang=2),
    hc.prop("hf1_pine_a1", "hushfrost_snow_pine", 21, 5, 2, 3, overhang=2),
    hc.prop("hf1_pine_a2", "hushfrost_snow_pine_big", 21, 13, 3, 4, overhang=3),
    hc.prop("hf1_pine_b1", "hushfrost_snow_pine", 7, 12, 2, 3, overhang=2),
    hc.prop("hf1_pine_b2", "hushfrost_snow_pine", 7, 20, 2, 3, overhang=2),
    hc.prop("hf1_pine_e1", "hushfrost_snow_pine", 30, 16, 2, 3, overhang=2),
    hc.prop("hf1_pine_w1", "hushfrost_snow_pine", 0, 5, 2, 3, overhang=2),
    hc.prop("hf1_pine_s1", "hushfrost_snow_pine_big", 5, 23, 3, 4, overhang=3),
    hc.prop("hf1_deadtree", "hushfrost_dead_tree", 21, 17, 2, 3, overhang=2),
    hc.prop("hf1_icicle_crag", "hushfrost_icicle_outcrop", 3, 3, 3, 2),
    hc.prop("hf1_boulders_n", "hushfrost_snow_boulders", 10, 4, 2, 2, overhang=1),
    hc.prop("hf1_shrub_nw", "hushfrost_frozen_shrub", 2, 5, 1, 1),
    hc.prop("hf1_shrub_s", "hushfrost_frozen_shrub", 12, 23, 1, 1),
    hc.prop("hf1_shrub_ne", "hushfrost_frozen_shrub", 24, 8, 1, 1),
]

# ---- R10 POLISH: the pass reads as a high mountain pass at night ------------------
# (the owner's "still flat in places" verdict: uniform pale snow, grey tuft slabs,
# flat blue bank stripes). Everything here is a drawn decal (solid:false — the
# lanes, sight lines and reachability are untouched) or a prop on ground that was
# already solid / off every lane (audit_flow + render_walkable prove it).
m["objects"] = hc.surface_decals(W, H, glacier, frosttuft, prefix="hf1",
                                 reserved=object_cells | point_cells | reserved) + \
    [hc.decal(*d) for d in GROUND] + m["objects"] + PROPS + \
    [hc.decal(*d, above=True) for d in MIST]
hc.carry_over(m, keep_ids={"cache_hushfrost_hollow"}, keep_prefixes=("peril_", "amb_"))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
