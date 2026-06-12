#!/usr/bin/env python3
"""
Aurora Hollow — the ice grotto under aurora light (walkthrough/04-west,
Hushfrost §4; atlas §3 spurs: "spur off Hushfrost II, Emberward; reward:
rare Frost/Light kin + item"). Kind cave, ONE floor — the §2a late-spur
tier: compact, the prize a choke beyond the obvious. [MISSABLE] — Emberward
is held the moment the player reaches Hushfrost II, so it's open at once;
the §3 "now accessible" sign stands at its mouth on pass II.

The prettiest small map in the West: a vaulted blue-ice chamber where the
aurora pools UNDER the ice — drawn aurora veils hang from the vault, glints
(ours + the Windward starglints) scatter the floor, and the kin bed grows in
the lit frost. Composition: a south entry chamber, a 2-wide throat into THE
VAULT, two 1-wide-choke alcoves that pay (§3a r4), and the north APSE — the
deepest pocket, holding the X1 aurora-oil and the rare bed. Rooms and chokes
are RECTS that overlap (the blob-adjacency trap).

WIRING (graph.ts `to_aurora`, both sides W1): pass_ii's mouth warps at
(14,2)/(15,2) land HERE at (9,13)/(10,13) — ON our return pair `to_pass_ii_w`
/ wait, ids: our return warps `to_hushfrost` at (9,14)/(10,14) land at
pass_ii (14,3)/(15,3), one tile inside its mouth (the engine never auto-fires
a step_on warp on arrival, so landing one tile north of ours is safe — and
(9,13)/(10,13) sit within 1 of the return pair, per audit_warps).

X1: the aurora-oil cache (`flag:picked_aurora_oil`, the stormwood pattern —
the cache shows only once the caretaker has ASKED, flag:q_west_caretaker;
script gives the existing `aurora_oil` key item). The hollow's own §4 reward
("rare Frost/Light kin + ITEM") is the unconditional starlamp-charge cache —
quest or no quest, the detour pays.

Encounter picks (the hooks: "rare Frost/Light kin at low weight"; band
40-42, the spur may sit at the band's top — §2b r4 priced detour):
  #86 Prismcub / #87 Prismantus — the canon Frost/Light prism-bear line
  #78 Crystarn — the iridescent snow-bird, aurora-light scatterer
  #73 FROSTHOLM (NEWLY PLACED — previously unplaced): the apex of the
      ice-sprite line, "accumulated centuries of ice, starlight and
      AURORA-GLOW"; its only wild bed in the game, very rare (weight 6,
      lv 42, catchRate 24 — the hollow's true prize). First E-tier kin
      with a wild row; documented deviation (the spur-spike rule prices it).
  Mirror into EXTRA_ENCOUNTERS (tools/balance/build_species.py) = wiring agent.

audit_flow WAIVER — `loop` WARN if raised: a one-portal landmark pocket has
no through-pair; the journey out is the walk home (the wind_eye precedent,
§2a late-spur tier stays compact).

Run:  ./venv/bin/python tools/maps/build_aurora_hollow.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 16
rng = random.Random(76)
owed: list[str] = []

# ---- carve the grotto from solid glacier -------------------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 7, 10, 12, 13)        # south entry chamber
mk.rect(floor, W, H, 9, 8, 10, 10)         # throat up into the vault (2-wide)
mk.rect(floor, W, H, 4, 4, 15, 8)          # THE VAULT — the aurora chamber
mk.hline(floor, W, H, 6, 2, 4)             # west choke (1-wide, overlaps the vault)
mk.rect(floor, W, H, 2, 4, 3, 5)           # west alcove (dead end, pays: charge)
mk.hline(floor, W, H, 5, 15, 17)           # east choke (1-wide)
mk.rect(floor, W, H, 16, 3, 17, 5)         # east alcove (dead end, pays: valuable)
mk.vline(floor, W, H, 9, 2, 4)             # apse throat (1-wide)
mk.vline(floor, W, H, 10, 2, 4)
mk.rect(floor, W, H, 7, 2, 12, 3)          # THE APSE — the oil + the rare bed

for i in range(W * H):
    if floor[i]:
        wall[i] = 0
# the south mouth: entry gap (cols 9-10) through the border to the return warps
for y in (13, 14):
    wall[y * W + 9] = 0
    wall[y * W + 10] = 0
floor[14 * W + 9] = 1
floor[14 * W + 10] = 1

# ---- the ice floor (walkable blue ice pooling under the vault) ---------------------
ice = mk.make_grid(W, H)
mk.blob(ice, W, H, 9.5, 5.5, 4.6, 2.2)     # the vault's frozen pool
mk.blob(ice, W, H, 9.5, 2.8, 2.4, 1.2)     # the apse sheet
mk.blob(ice, W, H, 13.5, 7.0, 1.8, 1.0)
for i in range(W * H):
    if wall[i]:
        ice[i] = 0

# ---- the kin bed (frosttuft, fill-only encounter tile) -----------------------------
frosttuft = mk.make_grid(W, H)
mk.blob(frosttuft, W, H, 5.5, 7.2, 2.0, 1.2)    # vault SW bed
mk.blob(frosttuft, W, H, 8.0, 2.5, 1.6, 0.9)    # the apse bed (the rare pocket)
mk.blob(frosttuft, W, H, 14.0, 4.5, 1.4, 0.9)   # vault NE bed
for i in range(W * H):
    if wall[i] or ice[i]:
        frosttuft[i] = 0

# ---- base: bone snow (the grotto floor between the ice sheets) ---------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ice", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": ice},
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_wall", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

m: dict = {
    "id": "aurora_hollow", "display_name": "Aurora Hollow",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    # spur maps reuse the parent area's loop + backdrops (the P0.D reuse table:
    # aurora_hollow -> hushfrost-pass-a/b, "aurora baked into both variants")
    "music": "assets/audio/music/hushfrost-pass-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/hushfrost-pass-a.webp",
        "assets/backgrounds/battle/hushfrost-pass-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- warps (the mutual pair with pass_ii's mouth — see module docstring) -----------
m["warps"] += [
    {"id": "to_hushfrost", "at": {"tx": 9, "ty": 14}, "trigger": "step_on",
     "to_map": "hushfrost_pass_ii", "to": {"tx": 14, "ty": 3}, "facing": "down",
     "transition": "door"},
    {"id": "to_hushfrost_e", "at": {"tx": 10, "ty": 14}, "trigger": "step_on",
     "to_map": "hushfrost_pass_ii", "to": {"tx": 15, "ty": 3}, "facing": "down",
     "transition": "door"},
]

# ---- the aurora dressing (drawn veils + glints; the vault's whole point) -----------
m["objects"] += [
    # veils hang from the vault — walk-under light curtains
    {"id": "veil_w", "sprite": "hushfrost_aurora_veil", "at": {"tx": 5, "ty": 3},
     "w": 3, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
    {"id": "veil_e", "sprite": "hushfrost_aurora_veil", "at": {"tx": 11, "ty": 4},
     "w": 3, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
    {"id": "veil_apse", "sprite": "hushfrost_aurora_veil", "at": {"tx": 8, "ty": 1},
     "w": 3, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
    # glints pooled on the floor (ours, green-cold + the Windward starglints)
    {"id": "glint_a", "sprite": "hushfrost_aurora_glint_a", "at": {"tx": 6, "ty": 5},
     "w": 1, "h": 1, "solid": False, "walk_under": True},
    {"id": "glint_b", "sprite": "hushfrost_aurora_glint_b", "at": {"tx": 12, "ty": 6},
     "w": 1, "h": 1, "solid": False, "walk_under": True},
    {"id": "glint_c", "sprite": "hushfrost_aurora_glint_a", "at": {"tx": 10, "ty": 3},
     "w": 1, "h": 1, "solid": False, "walk_under": True},
    {"id": "starglint_a", "sprite": "windward_starglint_a", "at": {"tx": 8, "ty": 7},
     "w": 1, "h": 1, "solid": False, "walk_under": True},
    {"id": "starglint_b", "sprite": "windward_starglint_b", "at": {"tx": 14, "ty": 5},
     "w": 1, "h": 1, "solid": False, "walk_under": True},
    {"id": "starglint_c", "sprite": "windward_starglint_a", "at": {"tx": 4, "ty": 8},
     "w": 1, "h": 1, "solid": False, "walk_under": True},
    # ice spires framing the entry throat
    {"id": "spires_throat", "sprite": "pale_vault_ice_spire", "at": {"tx": 11, "ty": 8},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- caches ------------------------------------------------------------------------
# THE X1 AURORA-OIL (the stormwood pattern: appears once the caretaker asks)
owed += pt.cache(m, cid="aurora_oil", at=(11, 2))
for npc in m["npcs"]:
    if npc["id"] == "cache_aurora_oil":
        npc["requires_flag"] = "flag:q_west_caretaker"
# the hollow's own §4 item reward (unconditional — the detour always pays)
owed += pt.cache(m, cid="aurora_charge", at=(2, 4))       # a strong charge, W alcove
owed += pt.cache(m, cid="aurora_shard", at=(17, 3))       # Starglass Shard, E alcove

# ---- encounters (the rare Frost/Light bed; spur spike to the band top) -------------
TABLE = [{"kin_id": 86, "weight": 32, "min_level": 40, "max_level": 42},
         {"kin_id": 78, "weight": 28, "min_level": 40, "max_level": 42},
         {"kin_id": 87, "weight": 22, "min_level": 41, "max_level": 42},
         {"kin_id": 73, "weight": 6, "min_level": 42, "max_level": 42},
         {"kin_id": 84, "weight": 12, "min_level": 40, "max_level": 42}]
m["encounters"] += pt.zones_from_grid(frosttuft, W, H, terrain="tall_grass",
                                      rate=0.12, table=TABLE, id_prefix="bed")

# ---- glowing dressing on the walls' feet -------------------------------------------
for (x, y, n) in [(4, 4, "glowshroom_a"), (15, 8, "glowshroom_b"), (7, 8, "greymoss_a"),
                  (12, 2, "glowshroom_a")]:
    if deco[y * W + x] == 0 and not wall[y * W + x]:
        deco[y * W + x] = gid(n)

# ---- sparse boulders (a grotto, not a field — no grass scatter underground) --------
for (x, y) in [(5, 4), (13, 8), (8, 11), (16, 4)]:
    if deco[y * W + x] == 0 and not wall[y * W + x] and not frosttuft[y * W + x]:
        deco[y * W + x] = gid("boulder")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
