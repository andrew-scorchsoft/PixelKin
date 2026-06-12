#!/usr/bin/env python3
"""
Helia Vault — the sealed reliquary, promoted to a SUNSKETCH PUZZLE
micro-dungeon (walkthrough/04-west "Sunvault Climb" §4 + spine §5
"Sunsketch as an optional light-puzzle"; kind cave, region west, optional
spur off sunvault_climb_ii, band 47-50). The West's signature Solar reward,
EARNED, not merely gated — and the region's kit-breaker: no other map in
Vesperholm is a chained-bloom vault. The timed-bloom variant is SKIPPED
(canon fallback — spine §8: sequential/redirect are expressible now; timed
needs a small engine addition).

THE PUZZLE (4 steps: 3 sequential blooms + 1 redirect — spine §5 verbatim,
"bloom a vine to reach a sunnier ledge, from which you bloom the next"):
  step 1  the antechamber's double vine (G1) — bloom-on-step band
          script.helia_bloom_1 on the 1-wide root cells; Sunsketch
          AbilityGate opens the wall cut; the vine art swaps withered->
          bloomed on flag:helia_bloom_1.
  step 2  the gold-lit ledge room's north vine (G2) — same grammar, from
          the SUNNIER ledge (a goldgrass pocket: the light you stand in is
          the light you bloom with). script.helia_bloom_2.
  step 3  the high gallery's west vine (G3) — script.helia_bloom_3.
  step 4  THE REDIRECT: the FAR VINE hangs across a 4-tile chasm no pocket
          of daylight can reach directly. The SUN-MIRROR FLOWER on the east
          spur (interact script.helia_mirror -> flag:helia_mirror_bent;
          dim->alight object swap) bends the daylight to it; only then does
          the root band at (5,7) bloom it (script.helia_bloom_far requires
          flag:helia_mirror_bent, blocked_ref npc.helia_far_vine ->
          flag:helia_far_bloomed, the vine's withered->bloomed swap).
ENCODING NOTE: steps 1-3 ride Sunsketch AbilityGates (held by everyone here
— the to_helia warp requires it), so their SEQUENCE is enforced by pure
geometry (each root is only reachable across the previous vine); the bloom
bands give the verb its beat and the flag-swaps make the map remember
(§3a r10). Step 4's PASSAGE also rides a Sunsketch gate (spine §8: "chains
of AbilityGate cover sequential/redirect NOW" — collision cannot key on a
flag, and a same-map warp pair fails the worldmodel's portal-reach check),
so the REDIRECT'S LOCK is on the REWARD, where the schema supports flags:
the relic cache AND Heliovast's reliquary bed both require
flag:helia_far_bloomed — a player who tiptoes a withered vine finds the
vault dark and the reliquary sealed (the tease); only bent daylight wakes
it. The root band narrates the lock on every early attempt.

HANDSHAKE (W2-internal, built both sides): climb_ii `to_helia` at (0,7)/(0,8)
lands HERE at (23,10)/(23,11) ON our return pair `to_climb_ii`/`_s`, which
lands back at climb_ii (1,7)/(1,8). Both Sunsketch (the mouth's seal).

THE PRIZE (hooks: "rare Solar kin + item in a sealed reliquary"):
  * #130 HELIOVAST — its dex entry NAMES this map ("Sealed inside the Helia
    Vault... the most concentrated pocket of stored daylight"): the
    reliquary chamber's rare wild bed (the aurora_hollow/Frostholm
    spur-spike precedent; first wild placement of the E-tier single).
    (#131 Helixia, "the Vault's guardian", stays unplaced — a postgame/
    scripted hook for 06; #128 Solarmourn belongs to the Solarium's
    constellation lore, not a wild row.)
  * the reliquary cache (script.pickup_helia_relic — suggest a SOLAR
    STAR-CHART, the aspirational sink, + the find written in the vault's
    hush). Mirror Heliovast's row into EXTRA_ENCOUNTERS = wiring agent.

Suggested copy (wiring agent):
  sign.helia_entry    "The Helia Vault. What the Solarium could not keep
                       dry, the keepers sealed here — and the seals are
                       flowers." (antechamber)
  npc.helia_far_vine  "The great vine sleeps beyond your pocket of
                       daylight. Something here must bend the light."
                       (the far-vine warps' blocked_ref)
  script.helia_mirror "The dish-bloom turns. Somewhere deeper, gold light
                       lands where your hands cannot." (sets
                       flag:helia_mirror_bent)

audit_flow notes — a spur dead-end map by design: the far-vine warp pair IS
the compressed return (one step back across the chasm once bent); the
mirror spur and ledge-room beds pay their pockets (§3a r4).

Run:  ./venv/bin/python tools/maps/build_helia_vault.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 22
rng = random.Random(76)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
wall = mk.make_grid(W, H)       # cavewall — the vault is carved OUT of it
ruin = mk.make_grid(W, H)       # the worked reliquary paving
goldtuft = mk.make_grid(W, H)   # the sun-shaft encounter beds
deco = mk.make_grid(W, H)

# the vault is solid rock; rooms are carved
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

def carve(x0, y0, x1, y1):
    mk.rect(wall, W, H, x0, y0, x1, y1, 0)

carve(17, 8, 22, 13)            # ROOM A — the antechamber
carve(11, 8, 15, 13)            # ROOM B — the gold-lit ledge room
carve(10, 2, 16, 6)             # ROOM C — the high gallery
carve(17, 3, 21, 4)             # the mirror spur (east)
carve(4, 2, 8, 6)               # ROOM D — the west landing
carve(5, 7, 5, 7)               # the far-vine root alcove (deliberate step)
carve(3, 12, 9, 18)             # THE RELIQUARY CHAMBER (across the chasm)
# the entry mouth (east edge, rows 10-11)
carve(23, 10, 23, 11)
# G1 / G2 / G3 stay WALL — the Sunsketch gates open them under the vine art
# G1: (16,10),(16,11) · G2: (13,7) · G3: (9,4)
# THE FAR CHASM x3-9 y8-11 stays wall except the far vine's column (col 5),
# which the fourth gate opens under the vine_far art

# ---- paving + sun shafts ------------------------------------------------------------
mk.rect(ruin, W, H, 17, 10, 23, 11)           # antechamber walk
mk.rect(ruin, W, H, 11, 10, 16, 11)           # through G1 into room B
mk.rect(ruin, W, H, 13, 7, 13, 9)             # up through G2
mk.rect(ruin, W, H, 11, 4, 13, 6)             # gallery walk
mk.rect(ruin, W, H, 8, 4, 10, 4)              # through G3 west
mk.rect(ruin, W, H, 17, 3, 21, 4)             # the mirror spur
mk.rect(ruin, W, H, 5, 5, 5, 7)               # to the far-vine root
mk.rect(ruin, W, H, 4, 12, 8, 17)             # the reliquary floor
# the sunnier ledges (goldgrass pockets — painted into base below)
gold = mk.make_grid(W, H)
mk.blob(gold, W, H, 12.5, 12.0, 1.8, 1.4)     # room B's sun shaft
mk.blob(gold, W, H, 6.0, 3.0, 1.8, 1.2)       # room D's sun shaft
mk.blob(gold, W, H, 15.0, 3.0, 1.6, 1.0)      # gallery shaft
mk.blob(goldtuft, W, H, 12.5, 12.5, 1.3, 1.0) # room B bed
mk.blob(goldtuft, W, H, 6.0, 3.0, 1.3, 0.9)   # room D bed

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if wall[i]:
        ruin[i] = 0
        goldtuft[i] = 0
        gold[i] = 0
    if ruin[i]:
        goldtuft[i] = 0

# ---- base: cave rock, gold light pooling in the shafts ------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
gg = [gid("goldgrass0"), gid("goldgrass1"), gid("goldgrass2"), gid("goldgrass3")]
base = mk.make_grid(W, H)
for i in range(W * H):
    if gold[i]:
        base[i] = rng.choice(gg) if rng.random() < 0.55 else gg[0]
    else:
        base[i] = rng.choice(cf) if rng.random() < 0.5 else cf[0]

terrain_layers = [
    {"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": ruin},
    {"name": "t_goldtuft", "role": "terrain", "terrain": "goldtuft",
     "set": "vesper_overworld_set", "depth": 0, "data": goldtuft},
    {"name": "t_wall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

m: dict = {
    "id": "helia_vault", "display_name": "Helia Vault",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [
        # the three sequential blooms (Sunsketch — held; sequence enforced by
        # geometry, beat given by the bloom bands below)
        {"id": "vine_1", "ability": "sunsketch",
         "rect": {"tx": 16, "ty": 10, "w": 1, "h": 2}, "effect": "make_passable"},
        {"id": "vine_2", "ability": "sunsketch",
         "rect": {"tx": 13, "ty": 7, "w": 1, "h": 1}, "effect": "make_passable"},
        {"id": "vine_3", "ability": "sunsketch",
         "rect": {"tx": 9, "ty": 4, "w": 1, "h": 1}, "effect": "make_passable"},
        # the far vine's column (the redirect's crossing — see ENCODING NOTE)
        {"id": "vine_far", "ability": "sunsketch",
         "rect": {"tx": 5, "ty": 8, "w": 1, "h": 4}, "effect": "make_passable"},
    ],
    # helia reuses the Climb's loop + backdrops (the reuse table): the spur is
    # the Climb's own deep pocket
    "music": "assets/audio/music/sunvault-climb-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/sunvault-climb-a.webp",
        "assets/backgrounds/battle/sunvault-climb-b.webp",
    ],
}

# ---- warps --------------------------------------------------------------------------
m["warps"] += [
    # EAST <-> sunvault_climb_ii (the mouth; Sunsketch both ways)
    {"id": "to_climb_ii", "at": {"tx": 23, "ty": 10}, "trigger": "step_on",
     "to_map": "sunvault_climb_ii", "to": {"tx": 1, "ty": 7}, "facing": "right",
     "requires_ability": "sunsketch",
     "blocked_ref": "sign.sunvault_helia", "transition": "door"},
    {"id": "to_climb_ii_s", "at": {"tx": 23, "ty": 11}, "trigger": "step_on",
     "to_map": "sunvault_climb_ii", "to": {"tx": 1, "ty": 8}, "facing": "right",
     "requires_ability": "sunsketch",
     "blocked_ref": "sign.sunvault_helia", "transition": "door"},
]

# THE FAR VINE'S ROOT BAND — the redirect's beat: blocked in the vault's
# voice until the mirror bends the light; then the bloom (and the wake)
m["triggers"].append({
    "id": "helia_bloom_far", "kind": "script", "at": {"tx": 5, "ty": 7},
    "activation": "step_on", "ref": "script.helia_bloom_far", "once": True,
    "requires_flag": "flag:helia_mirror_bent",
    "blocked_ref": "npc.helia_far_vine",
    "sets_flags": ["flag:helia_far_bloomed"],
    "hidden_when_flag": "flag:helia_far_bloomed"})
owed += ["npc.helia_far_vine (the root band's blocked_ref — copy in the "
         "docstring)",
         "script.helia_bloom_far (requires flag:helia_mirror_bent; the bent "
         "daylight lands and the great vine wakes — sets "
         "flag:helia_far_bloomed)"]

# ---- the bloom-on-step bands (the verb's beat; §3a chokes by construction) ----------
for n, cells in enumerate([[(17, 10), (17, 11)], [(13, 8)], [(10, 4)]], start=1):
    for i, (tx, ty) in enumerate(cells):
        m["triggers"].append({
            "id": f"helia_bloom_{n}_{i}", "kind": "script",
            "at": {"tx": tx, "ty": ty}, "activation": "step_on",
            "ref": f"script.helia_bloom_{n}", "once": True,
            "sets_flags": [f"flag:helia_bloom_{n}"],
            "hidden_when_flag": f"flag:helia_bloom_{n}"})
owed += ["script.helia_bloom_1 (raise the lamp; the double vine unfurls — "
         "sets flag:helia_bloom_1)",
         "script.helia_bloom_2 (from the sunnier ledge — sets flag:helia_bloom_2)",
         "script.helia_bloom_3 (sets flag:helia_bloom_3)"]

# ---- THE SUN-MIRROR FLOWER (the redirect beat) --------------------------------------
m["objects"] += [
    {"id": "mirror_alight", "sprite": "sunvault_mirror_alight",
     "at": {"tx": 20, "ty": 2}, "w": 1, "h": 2,
     "requires_flag": "flag:helia_mirror_bent"},
    {"id": "mirror_dim", "sprite": "sunvault_mirror_dim",
     "at": {"tx": 20, "ty": 2}, "w": 1, "h": 2,
     "hidden_when_flag": "flag:helia_mirror_bent"},
]
m["triggers"].append({
    "id": "helia_mirror", "kind": "script", "at": {"tx": 20, "ty": 3},
    "activation": "interact", "ref": "script.helia_mirror", "once": True,
    "sets_flags": ["flag:helia_mirror_bent"],
    "hidden_when_flag": "flag:helia_mirror_bent"})
owed += ["script.helia_mirror (bend the daylight — copy in the docstring; "
         "sets flag:helia_mirror_bent)"]

# ---- the vines (withered -> bloomed swaps; same footprint, non-solid art) -----------
VINES = [
    ("vine_1a", "sunvault_vine_h", (15, 10), 3, 1, "flag:helia_bloom_1"),
    ("vine_1b", "sunvault_vine_h", (15, 11), 3, 1, "flag:helia_bloom_1"),
    ("vine_2", "sunvault_vine_v", (13, 6), 1, 3, "flag:helia_bloom_2"),
    ("vine_3", "sunvault_vine_h", (8, 4), 3, 1, "flag:helia_bloom_3"),
    ("vine_far", "sunvault_vine_far", (5, 8), 1, 4, "flag:helia_far_bloomed"),
]
for vid, stem, (vx, vy), vw, vh, flag in VINES:
    m["objects"] += [
        {"id": f"{vid}_bloomed", "sprite": f"{stem}_bloomed",
         "at": {"tx": vx, "ty": vy}, "w": vw, "h": vh, "solid": False,
         "requires_flag": flag},
        {"id": f"{vid}_withered", "sprite": f"{stem}_withered",
         "at": {"tx": vx, "ty": vy}, "w": vw, "h": vh, "solid": False,
         "hidden_when_flag": flag},
    ]

# ---- THE RELIQUARY ------------------------------------------------------------------
m["objects"] += [
    {"id": "reliquary", "sprite": "sunvault_reliquary",
     "at": {"tx": 4, "ty": 13}, "w": 3, "h": 3, "overhang": 1},
    {"id": "column_a", "sprite": "solarium_column", "at": {"tx": 18, "ty": 8},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_b", "sprite": "solarium_column", "at": {"tx": 8, "ty": 12},
     "w": 1, "h": 3, "overhang": 1, "walk_under": True},
    {"id": "column_fallen", "sprite": "solarium_column_fallen",
     "at": {"tx": 14, "ty": 13}, "w": 3, "h": 1},
]
owed += pt.cache(m, cid="helia_relic", at=(5, 17))      # THE PRIZE (Solar
                                                        # Star-chart suggested)
# the prize is the REDIRECT'S lock: sealed until the bent daylight wakes it
m["npcs"][-1]["requires_flag"] = "flag:helia_far_bloomed"
owed += pt.cache(m, cid="helia_charge", at=(18, 3))     # the mirror spur pays
                                                        # double (§3a r4)
owed += pt.sign(m, deco, W, sid="helia_entry", at=(21, 9))

# ---- encounters ---------------------------------------------------------------------
# the sun-shaft beds (47-49) — the Solar register in the vault's hush
TABLE_HELIA = [
    {"kin_id": 117, "weight": 22, "min_level": 47, "max_level": 48},  # Helibud
    {"kin_id": 118, "weight": 20, "min_level": 47, "max_level": 49},  # Helicore
    {"kin_id": 115, "weight": 18, "min_level": 47, "max_level": 49},  # Solvyne
    {"kin_id": 104, "weight": 16, "min_level": 48, "max_level": 49},  # Goldmane
    {"kin_id": 116, "weight": 12, "min_level": 48, "max_level": 49},  # Auravane
    {"kin_id": 121, "weight": 12, "min_level": 48, "max_level": 49},  # Sunstag
]
m["encounters"] += pt.zones_from_grid(goldtuft, W, H, terrain="tall_grass",
                                      rate=0.12, table=TABLE_HELIA, id_prefix="shaft")
# THE RELIQUARY BED — Heliovast's only wild row (cave terrain rolls
# rect-wide; the spur-spike precedent: priced by the puzzle, 48-50)
m["encounters"].append({
    "id": "reliquary", "terrain": "cave",
    "rect": {"tx": 3, "ty": 15, "w": 7, "h": 4}, "encounter_rate": 0.10,
    # the bed wakes WITH the far vine (the redirect's lock): dark and silent
    # until the bent daylight lands
    "requires_flag": "flag:helia_far_bloomed",
    "table": [{"kin_id": 118, "weight": 34, "min_level": 48, "max_level": 50},
              {"kin_id": 115, "weight": 28, "min_level": 48, "max_level": 49},
              {"kin_id": 104, "weight": 26, "min_level": 48, "max_level": 50},
              {"kin_id": 130, "weight": 12, "min_level": 49, "max_level": 50}]})

# ---- dressing: boulders in the worked dark ------------------------------------------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (wall, ruin, goldtuft))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
for (x, y) in [(19, 12), (12, 5), (4, 5), (7, 16), (15, 9), (11, 13)]:
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
