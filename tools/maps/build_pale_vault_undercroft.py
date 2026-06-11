#!/usr/bin/env python3
"""
Pale Vault Undercroft — the Lamp-Line trial (walkthrough/03-north, Pale Vault
beat 7; spine §5 earned-loop shape #6: ice lamp-line, a SINGLE-MAP trial).

One blue-ice floor under the Frost Lumenary: three stacked galleries joined by
1-wide chokes, walked as a descending S — and along the walked line, SEVEN
lamp-brackets lit IN ORDER. Each bracket is an interact script chained on the
previous flag (flag:q_north_lamp_1..7; the seventh also sets
flag:q_north_lamps_held); a still-dark bracket out of order answers with the
shared blocked line (npc.undercroft_bracket_cold). Lit brackets are the
MapObject flag-swap pair (dark hidden_when / lit requires — same footprint,
same solidity), so the vault visibly fills with pale aurora flame behind you:
the lamp-line IS the breadcrumb light (§3 "lead with light" — no shrooms).

Two frost-ward SIGHT trainers (lv 37-39, keeper class — TRAINERS defs land
with the wiring agent) hold the second and third galleries. Ysolde waits at
the HEART (the west chamber off gallery 3): her bond-test cutscene bands the
1-wide cut into the chamber — requires flag:q_north_lamps_held,
blocked_ref npc.ysolde_not_ready (her voice), hidden once gleam:frost.
TRAINERS['ysolde_frost']: reward_flags ['gleam:frost'] + reward_abilities
['emberward'] (the Lampwarden grant pattern — pure data; with gleam:storm
already held the ENGINE sets flag:crown_north, never hand-set).

Wires to: the town's undercroft arch door at (19,8) — our `to_town` warp at
(10,0) and that door land ON each other (the audited mutual pair; the engine
never auto-fires a step_on warp on arrival).

Encounters: cave zones (rect-wide), band 37-40 — one band deeper than the
hollows above (§2b r4): #84 Hushbore (Frost C — the silence-aura burrower;
this vault keeps its quiet), #83 Hushvole (A), #72 Glaceling (C, the glacier
ice-sprite), #85 Stillwarden (Frost/Dark D, rare). The heart rolls nothing.

audit_flow WAIVER — `loop` WARN accepted if raised: the Lamp-Line is canon-
locked as a single-map TRIAL (spine §5 shape #6), not a region dungeon; the
multi-floor ladder requirement (§2a) applies to dungeons, and the North's
return-compressor budget lives on Windward's shortcut. ZERO humour here.

Run:  ./venv/bin/python tools/maps/build_pale_vault_undercroft.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 18
rng = random.Random(73)
owed: list[str] = []

# ---- terrain: solid rock, galleries carved as rects + 1-wide chokes (the
# blob-edge adjacency trap — rects join, blobs lie) ----------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.vline(floor, W, H, 10, 0, 1)                     # entry shaft from the arch
mk.rect(floor, W, H, 2, 2, 16, 4)                   # GALLERY 1 (brackets 1-2)
mk.rect(floor, W, H, 17, 3, 17, 4)                  # E alcove (dead end pays: cache)
mk.vline(floor, W, H, 3, 5, 6)                      # choke 1 (W, 1-wide)
mk.rect(floor, W, H, 2, 7, 16, 8)                   # GALLERY 2 (brackets 3-4, ward A)
mk.vline(floor, W, H, 16, 9, 10)                    # choke 2 (E, 1-wide)
mk.rect(floor, W, H, 8, 11, 16, 13)                 # GALLERY 3 (brackets 5-6, ward B)
mk.rect(floor, W, H, 16, 14, 16, 15)                # S alcove (dead end pays: cache)
mk.rect(floor, W, H, 2, 11, 6, 15)                  # THE HEART (Ysolde, bracket 7)
mk.vline(floor, W, H, 7, 12, 13)                    # the heart's 1-wide cut (banded)
floor[5 * W + 12] = 1                               # 1-cell wall niches so the long
floor[9 * W + 6] = 1                                # south edges never run ruled

for i in range(W * H):
    if floor[i]:
        wall[i] = 0

# blue-ice sheets along the walked line ("ice + cavefloor mix")
ice = mk.make_grid(W, H)
mk.blob(ice, W, H, 8.0, 3.0, 3.2, 1.2)
mk.blob(ice, W, H, 9.0, 7.5, 3.6, 1.1)
mk.blob(ice, W, H, 12.5, 12.0, 2.6, 1.2)
mk.blob(ice, W, H, 4.0, 13.0, 1.8, 1.4)             # the heart's frozen floor
for i in range(W * H):
    if ice[i] and not floor[i]:
        ice[i] = 0

# ---- base + terrain layers ---------------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ice", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": ice},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

deco = mk.make_grid(W, H)

m: dict = {
    "id": "pale_vault_undercroft", "display_name": "Pale Vault Undercroft",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/pale-vault-glacier-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/pale-vault-glacier-a.webp",
        "assets/backgrounds/battle/pale-vault-glacier-b.webp",
    ],
}

# ---- THE SEVEN BRACKETS (descending line; dark/lit object swap pairs) --------------
# (x, ty) — each 1x2 object stands wall_mount style: top row over the wall
# face, base row in the gallery. Order follows the walked S.
BRACKETS = [
    (13, 1),   # 1 — gallery 1 east, first light past the door
    (5, 1),    # 2 — gallery 1 west, by the choke down
    (5, 6),    # 3 — gallery 2 west, off the choke
    (11, 6),   # 4 — gallery 2 mid
    (13, 10),  # 5 — gallery 3 east, off the second choke
    (9, 10),   # 6 — gallery 3 mid, past ward B's line
    (3, 10),   # 7 — the heart; its script also sets flag:q_north_lamps_held
]
for n, (bx, by) in enumerate(BRACKETS, start=1):
    flag = f"flag:q_north_lamp_{n}"
    prev = "flag:q_north_lampline" if n == 1 else f"flag:q_north_lamp_{n - 1}"
    m["objects"] += [
        {"id": f"bracket_{n}_dark", "sprite": "pale_vault_bracket_dark",
         "at": {"tx": bx, "ty": by}, "w": 1, "h": 2, "overhang": 1,
         "hidden_when_flag": flag},
        {"id": f"bracket_{n}_lit", "sprite": "pale_vault_bracket_lit",
         "at": {"tx": bx, "ty": by}, "w": 1, "h": 2, "overhang": 1,
         "requires_flag": flag},
    ]
    sets = [flag] + (["flag:q_north_lamps_held"] if n == 7 else [])
    m["triggers"].append({
        "id": f"light_lamp_{n}", "kind": "script",
        "at": {"tx": bx, "ty": by + 1}, "activation": "interact",
        "ref": f"script.light_lamp_{n}", "once": True,
        "requires_flag": prev, "blocked_ref": "npc.undercroft_bracket_cold",
        "sets_flags": sets, "hidden_when_flag": flag})
owed += [f"script.light_lamp_{n} (sets flag:q_north_lamp_{n}"
         + ("; the seventh also sets flag:q_north_lamps_held)" if n == 7 else ")")
         for n in range(1, 8)]
owed += ["npc.undercroft_bracket_cold (shared blocked line — the bracket "
         "before it is still dark)"]

# ---- warps (the mutual door pair with the town arch) -------------------------------
m["warps"].append(
    {"id": "to_town", "at": {"tx": 10, "ty": 0}, "trigger": "step_on",
     "to_map": "pale_vault_glacier", "to": {"tx": 19, "ty": 8}, "facing": "down",
     "transition": "door"})

# ---- the bond-test band (the heart's 1-wide cut — cannot be walked around) ---------
for i, ty in enumerate((12, 13)):
    m["triggers"].append({
        "id": f"lumenary_battle_{i}", "kind": "cutscene", "at": {"tx": 7, "ty": ty},
        "activation": "step_on", "ref": "script.lumenary_pale_vault", "once": True,
        "requires_flag": "flag:q_north_lamps_held",
        "blocked_ref": "npc.ysolde_not_ready",
        "hidden_when_flag": "gleam:frost"})
owed += ["script.lumenary_pale_vault (the bond-test: battle vs "
         "TRAINERS['ysolde_frost'] — warden class ai:'smart', ace ~40, payout "
         "60×ace, reward_flags ['gleam:frost'] + reward_abilities ['emberward']; "
         "the Gleam cadence: hold a silence, bloom the cool tint, fire gleam, "
         "crossfade to the Aurora-watch swell)",
         "TRAINERS['ysolde_frost']",
         "npc.ysolde_not_ready (bond-test blocked_ref, her voice)"]

# ---- the frost-ward sight trainers (geometry: galleries 2 and 3) -------------------
owed += pt.trainer_beat(m, tid="undercroft_ward_a", at=(15, 8), facing="left",
                        sight=4, sprite="npc_woman")
owed += pt.trainer_beat(m, tid="undercroft_ward_b", at=(9, 12), facing="right",
                        sight=4, sprite="npc_man")
owed += ["(undercroft_ward_a / undercroft_ward_b: keeper class, lv 37-39, "
         "payout 20×ace — defs land with the wiring agent)"]

# ---- Ysolde at the heart (post-Gleam she keeps her hall up top) --------------------
m["npcs"].append(
    {"id": "ysolde_vault", "at": {"tx": 4, "ty": 12}, "facing": "down",
     "sprite": "ysolde_frost", "movement": "static",
     "dialogue_ref": "npc.ysolde_vault",
     "hidden_when_flag": "gleam:frost"})
owed += ["npc.ysolde_vault (her waiting line at the heart; placement swaps to "
         "the Lumenary hall once gleam:frost is held)"]

# ---- caches (per-floor variety: a valuable + a consumable, both off-line) ----------
owed += pt.cache(m, cid="undercroft_amber", at=(17, 4))   # Moth-amber, E alcove
owed += pt.cache(m, cid="undercroft_balm", at=(16, 15))   # consumable, S alcove

# ---- encounters (cave, rect-wide; band 37-40, +1 over the hollows) -----------------
TABLE = [{"kin_id": 84, "weight": 35, "min_level": 37, "max_level": 40},
         {"kin_id": 83, "weight": 25, "min_level": 37, "max_level": 39},
         {"kin_id": 72, "weight": 25, "min_level": 37, "max_level": 40},
         {"kin_id": 85, "weight": 15, "min_level": 38, "max_level": 40}]
m["encounters"] += [
    {"id": "gallery_1", "terrain": "cave", "rect": {"tx": 2, "ty": 2, "w": 15, "h": 3},
     "encounter_rate": 0.08, "table": TABLE},
    {"id": "gallery_2", "terrain": "cave", "rect": {"tx": 2, "ty": 7, "w": 15, "h": 2},
     "encounter_rate": 0.06, "table": TABLE},
    {"id": "gallery_3", "terrain": "cave", "rect": {"tx": 8, "ty": 11, "w": 9, "h": 3},
     "encounter_rate": 0.08, "table": TABLE},
    # the heart rolls nothing — the trial's last room is the quiet answer
]

# ---- deco: rime, grey moss, stray pale pebbles (no fungus in an ice vault) ---------
for (x, y, n) in [(4, 3, "greymoss_a"), (12, 4, "greymoss_b"), (8, 8, "greymoss_a"),
                  (14, 7, "greymoss_b"), (10, 13, "greymoss_a"), (3, 14, "greymoss_b"),
                  (12, 5, "greymoss_b"), (6, 9, "greymoss_a")]:
    deco[y * W + x] = gid(n)
for (x, y) in [(7, 2), (15, 4), (4, 8), (12, 8), (15, 13), (5, 14), (11, 11)]:
    if deco[y * W + x] == 0:
        deco[y * W + x] = gid("g_pebble")
for (x, y) in [(2, 4), (16, 2), (8, 13), (2, 11)]:
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
