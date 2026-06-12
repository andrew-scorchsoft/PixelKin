#!/usr/bin/env python3
"""
Tideglass Cavern — the South's long-teased landmark, finally built
(walkthrough/07-the-three §4: Site I of the Three Hours; also pays the
standing obligations from 01-south: quest S3's wreck-lamp trigger, the atlas
card's signature rare water kin, and the spine §5 Lamplight Starlight nook).

A sea-cave of smoothed glass: black water pools (sunpool), walls veined with
translucent teal (ice painted as TIDEGLASS shelves/veins), the lit lane
glowmoss-veined. Three signature touches (§8):
  1. THE WRECK at the far end — the old fisher's boat, its stern-lamp cold
     (S3 pays here: relighting it sets flag:q_south_wrecklamp_lit).
  2. THE LAMPWRIGHT'S RELAY — three standing sea-glass lenses lit in verse
     order (amber/west shelf -> low/mid-pool islet -> deep/stair seam); the
     ordered light-chain puzzle (the Helia flag-chained-interacts grammar).
  3. THE STAIR SEAM — the glass stair down to tideglass_gallery (B1F), sealed
     until lens C rings (`requires_flag: flag:three_dusk_lens_c`).

ENTRY (both pinned by shipped host warps, audit_warps proves the pair):
  dimglass_coast_ii `to_tideglass` (2,13) -> lands (4,8); return `to_coast_ii`
  at (4,9). dimglass_coast `to_tideglass` (2,11) -> lands (5,8); return
  `to_coast` at (5,9). Host facings fixed left->right (interior opens east);
  the two return pads sit side by side on the mouth's south wall.

THE RELAY (one-flag-per-trigger; the solarium Lit-Stage encoding):
  wreck-lamp  interact, requires flag:q_south_wrecklamp (the fisher's tale —
              WITHOUT this gate a lamp lit before the tale would stack two
              old-fisher placements at the inn; see the S3 compatibility note
              in the Hours report), blocked_ref npc.tideglass_wrecklamp_cold,
              ref script.tideglass_wrecklamp -> sets flag:q_south_wrecklamp_lit
              (consumed by the inn's old_fisher_thanks stage, SHIPPED).
  verse       inert twin sign.tideglass_verse until the lamp burns; live
              trigger requires flag:q_south_wrecklamp_lit ->
              script.three_dusk_verse (the SCRIPT must if_flag-guard on
              flag:three_dusk_rumour and only then set flag:three_dusk_verse —
              EventTrigger carries ONE requires_flag; wiring-pass note).
  lens A/B/C  interact chain: A requires flag:three_dusk_verse, B requires _a,
              C requires _b; each blocked_ref npc.tideglass_lens_cold (the
              wrong-order/cold line), each sets its flag; cold->lit object
              swap pairs key the same flags. lens C opens the stair seam.

STARLIGHT NOOK — [LATER: Lamplight >= Starlight]: the NW fold's Starglass
Shard cache is gated on `flag:lamplight_starlight` (forward wiring: Lamplight
has no engine axis yet; the future Lamplight pass owns setting it — a safe
inert reveal, never a gate on anything required).

ENCOUNTERS (walkthrough hooks): cave band 20-24 (Tide register, the South's
backtrack bed), water 21-24 in the Tidecall side-pool, and the atlas-promised
SIGNATURE RARE as the very-rare water row — #30 GLOSTRAEL, the Glostern
line's middle form (seeds Pharolux's living-lighthouse legend two doors from
where players caught Glostern). The CURATED_AREAS + EXTRA_ENCOUNTERS mirror
in tools/balance/build_species.py = the trio wiring pass (the solarium
precedent — that file is the species package's lane).

audit_flow WAIVERS — `loop` WARN accepted: a spur landmark micro-dungeon (the
gullcry/helia tier); the mouth is its own compressed return. `free-pass` WARN
accepted: there is no end-to-end crossing to guard — both exits are the same
mouth; the cave-terrain bed rolls rect-wide across the walked hall, and the
relay/wreck content is the destination, not a corridor.

Run:  ./venv/bin/python tools/maps/build_tideglass_cavern.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 26, 20
rng = random.Random(160)
owed: list[str] = []

# ---- terrain: solid glass-rock, rooms carved ----------------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)


def carve(x0, y0, x1, y1):
    mk.rect(wall, W, H, x0, y0, x1, y1, 0)


carve(3, 5, 8, 9)          # ENTRY CHAMBER (mouth pads on its south wall)
carve(4, 4, 4, 4)          # the nook's 1-wide choke
carve(3, 2, 5, 3)          # THE STARLIGHT NOOK (deeper fold, NW)
carve(9, 3, 22, 16)        # THE MAIN HALL
carve(23, 3, 24, 6)        # the wreck bay (far NE end)
carve(3, 12, 7, 16)        # THE WEST SHELF (lens A's tideglass shelf)
carve(8, 13, 8, 14)        # shelf link into the hall
carve(23, 13, 23, 16)      # the stair seam bay (SE)

# ---- the black water pool (sunpool: Tidecall rides the tiles) -----------------------
pool = mk.make_grid(W, H)
mk.blob(pool, W, H, 13.5, 11.5, 3.4, 2.5)
# the mid-pool ISLET (lens B's stand) carved back out of the water
for (ix, iy) in ((13, 11), (14, 11), (13, 12), (14, 12)):
    pool[iy * W + ix] = 0

# ---- tideglass veins (ice painted as glass pads + the pool's glass basin) -----------
glass = mk.make_grid(W, H)
mk.rect(glass, W, H, 3, 12, 6, 14)          # the west shelf's tideglass pad
mk.rect(glass, W, H, 21, 3, 24, 4)          # the wreck bay's glass bed
mk.rect(glass, W, H, 22, 14, 23, 16)        # the stair seam's glass floor
mk.blob(glass, W, H, 10.0, 5.0, 1.6, 1.2)   # a vein pooling in the hall NW
# the black pool sits IN a tideglass basin: ring every pool cell (and the
# islet) with glass so the water's rim reads as smoothed glass, not raw rock
for y in range(H):
    for x in range(W):
        if pool[y * W + x]:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and not pool[ny * W + nx]:
                        glass[ny * W + nx] = 1

# ---- the glowmoss-veined lit lane (visual only — no tall_grass zone) ----------------
moss = mk.make_grid(W, H)
mk.blob(moss, W, H, 7.0, 7.5, 1.6, 1.0)     # out of the mouth
mk.blob(moss, W, H, 17.5, 7.0, 1.8, 1.0)    # the hall lane's lit vein
mk.blob(moss, W, H, 19.5, 12.5, 1.4, 1.0)   # bending toward the seam
mk.blob(moss, W, H, 7.5, 15.5, 1.2, 0.8)    # the shelf approach

# ---- precedence ---------------------------------------------------------------------
for i in range(W * H):
    if wall[i]:
        pool[i] = glass[i] = moss[i] = 0
    if pool[i]:
        glass[i] = moss[i] = 0
    if glass[i]:
        moss[i] = 0

# ---- base: cave glass-rock ----------------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_glass", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": glass},
    {"name": "t_moss", "role": "terrain", "terrain": "glowmoss",
     "set": "vesper_overworld_set", "depth": 0, "data": moss},
    {"name": "t_pool", "role": "terrain", "terrain": "sunpool",
     "set": "vesper_overworld_set", "depth": 0, "data": pool},
    {"name": "t_wall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco: glints, shrooms, the stair, signs ----------------------------------------
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


# glow-shroom breadcrumbs leading with light (§3): mouth -> hall -> seam
for (x, y, n) in [(3, 7, "glowshroom_a"), (7, 5, "glowshroom_b"),
                  (11, 4, "glowshroom_a"), (17, 9, "glowshroom_b"),
                  (20, 12, "glowshroom_a"), (21, 16, "glowshroom_b")]:
    put(x, y, n)
# wave-worn boulders + pale pebbles breaking the floors
for (x, y) in [(10, 14), (18, 4), (9, 9), (16, 15)]:
    put(x, y, "boulder")
for (x, y) in [(6, 6), (12, 6), (15, 8), (19, 10), (10, 16), (24, 4), (5, 14)]:
    put(x, y, "g_pebble")
# THE STAIR SEAM down to the Gallery
STAIR = (23, 15)
put(*STAIR, "cave_ladder_down")

# ---- assemble -----------------------------------------------------------------------
m: dict = {
    "id": "tideglass_cavern", "display_name": "Tideglass Cavern",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    # the spur reuses the parent coast loop's sparsest variant (the reuse table)
    "music": "assets/audio/music/dimglass-coast-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/tideglass-gallery-a.webp",
    ],
}

# ---- THE WRECK + the stern-lamp (S3 pays) -------------------------------------------
m["objects"] += [
    {"id": "wreck", "sprite": "tideglass_wreck",
     "at": {"tx": 20, "ty": 3}, "w": 3, "h": 2},
    # the stern-lamp: dark -> lit on S3's flag (same footprint + solidity)
    {"id": "wrecklamp_lit", "sprite": "tideglass_wrecklamp_lit",
     "at": {"tx": 23, "ty": 4}, "w": 1, "h": 2, "overhang": 1,
     "requires_flag": "flag:q_south_wrecklamp_lit"},
    {"id": "wrecklamp_dark", "sprite": "tideglass_wrecklamp_dark",
     "at": {"tx": 23, "ty": 4}, "w": 1, "h": 2, "overhang": 1,
     "hidden_when_flag": "flag:q_south_wrecklamp_lit"},
    # tideglass spires catching the lamp (the cavern's signature dressing)
    {"id": "spire_hall", "sprite": "tideglass_glass_spire",
     "at": {"tx": 9, "ty": 3}, "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "spire_pool", "sprite": "tideglass_glass_spire",
     "at": {"tx": 16, "ty": 3}, "w": 2, "h": 3, "overhang": 2, "walk_under": True},
]
m["triggers"] += [
    # the relight (interact on the lamp's foot; player stands south, faces up).
    # Gated on the fisher's tale (S3 stage order — see the docstring note).
    {"id": "wrecklamp", "kind": "script", "at": {"tx": 23, "ty": 5},
     "activation": "interact", "ref": "script.tideglass_wrecklamp", "once": True,
     "requires_flag": "flag:q_south_wrecklamp",
     "blocked_ref": "npc.tideglass_wrecklamp_cold",
     "sets_flags": ["flag:q_south_wrecklamp_lit"],
     "hidden_when_flag": "flag:q_south_wrecklamp_lit"},
    # once it burns: the kept light, re-readable
    {"id": "wrecklamp_lit", "kind": "dialogue", "at": {"tx": 23, "ty": 5},
     "activation": "interact", "ref": "npc.tideglass_wrecklamp_lit",
     "requires_flag": "flag:q_south_wrecklamp_lit"},
]
owed += ["script.tideglass_wrecklamp (S3's shipped beat: relight the stern-lamp "
         "— quiet, no fanfare; sfx world-lantern-light; sets "
         "flag:q_south_wrecklamp_lit, consumed by the inn's old_fisher_thanks)",
         "npc.tideglass_wrecklamp_cold (blocked: a cold stern-lamp wedged in the "
         "rocks — it keeps a story you haven't been told)",
         "npc.tideglass_wrecklamp_lit (the kept light, burning)"]

# ---- THE VERSE (the wreck-lamp's etched glass hood) ---------------------------------
VERSE = (19, 6)
put(*VERSE, "sign")
m["triggers"] += [
    {"id": "verse_dark", "kind": "sign", "at": {"tx": VERSE[0], "ty": VERSE[1]},
     "activation": "interact", "ref": "sign.tideglass_verse",
     "hidden_when_flag": "flag:q_south_wrecklamp_lit"},
    # ONE requires_flag per trigger: the live plaque keys on the lamp; the
    # SCRIPT must if_flag-guard on flag:three_dusk_rumour before setting
    # flag:three_dusk_verse (wiring-pass note in the report).
    {"id": "verse_lit", "kind": "script", "at": {"tx": VERSE[0], "ty": VERSE[1]},
     "activation": "interact", "ref": "script.three_dusk_verse",
     "requires_flag": "flag:q_south_wrecklamp_lit"},
]
owed += ["sign.tideglass_verse (inert twin: etched writing, unreadable in this "
         "light)",
         "script.three_dusk_verse (requires the rumour via if_flag; the verse: "
         "'Last light first; the low light after; the deep light once the "
         "others hold.' — sets flag:three_dusk_verse)"]

# ---- THE LAMPWRIGHT'S RELAY (lens A west shelf / B islet / C stair seam) ------------
LENSES = [
    ("a", (4, 13), "flag:three_dusk_verse", "flag:three_dusk_lens_a"),
    ("b", (13, 11), "flag:three_dusk_lens_a", "flag:three_dusk_lens_b"),
    ("c", (19, 14), "flag:three_dusk_lens_b", "flag:three_dusk_lens_c"),
]
for tag, (lx, ly), req, sets in LENSES:
    m["objects"] += [
        {"id": f"lens_{tag}_lit", "sprite": "tideglass_lens_lit",
         "at": {"tx": lx, "ty": ly}, "w": 2, "h": 2,
         "requires_flag": sets},
        {"id": f"lens_{tag}_cold", "sprite": "tideglass_lens_cold",
         "at": {"tx": lx, "ty": ly}, "w": 2, "h": 2,
         "hidden_when_flag": sets},
    ]
    m["triggers"].append(
        {"id": f"lens_{tag}", "kind": "script", "at": {"tx": lx, "ty": ly + 1},
         "activation": "interact", "ref": f"script.three_dusk_lens_{tag}",
         "once": True, "requires_flag": req,
         "blocked_ref": "npc.tideglass_lens_cold",
         "sets_flags": [sets], "hidden_when_flag": sets})
owed += ["script.three_dusk_lens_a (the amber lens takes the wreck-lamp's beam "
         "one span deeper; sets flag:three_dusk_lens_a)",
         "script.three_dusk_lens_b (sets flag:three_dusk_lens_b)",
         "script.three_dusk_lens_c (a low note rings through the floor; the "
         "stair seam breathes open; sets flag:three_dusk_lens_c)",
         "npc.tideglass_lens_cold (blocked/wrong-order: the sea-glass stays "
         "cold under your lamp)"]

# ---- warps --------------------------------------------------------------------------
m["warps"] += [
    # the mouth's two return pads (south wall of the entry chamber) — each
    # host landing sits ON its own return (audit_warps round trip)
    {"id": "to_coast_ii", "at": {"tx": 4, "ty": 9}, "trigger": "step_on",
     "to_map": "dimglass_coast_ii", "to": {"tx": 2, "ty": 13}, "facing": "right",
     "transition": "door"},
    {"id": "to_coast", "at": {"tx": 5, "ty": 9}, "trigger": "step_on",
     "to_map": "dimglass_coast", "to": {"tx": 2, "ty": 11}, "facing": "right",
     "transition": "door"},
    # THE STAIR SEAM — sealed until lens C rings (the relay's lock)
    {"id": "stair_down", "at": {"tx": STAIR[0], "ty": STAIR[1]},
     "trigger": "step_on", "to_map": "tideglass_gallery", "to": {"tx": 14, "ty": 3},
     "facing": "down", "requires_flag": "flag:three_dusk_lens_c",
     "blocked_ref": "npc.tideglass_stair_sealed", "transition": "fade"},
]
owed += ["npc.tideglass_stair_sealed ('A seam in the glass breathes cold air. "
         "It is not open.' — hooks verbatim)"]

# ---- THE STARLIGHT NOOK ([LATER: Lamplight >= Starlight]) ---------------------------
owed += pt.cache(m, cid="tideglass_starshard", at=(4, 2))
m["npcs"][-1]["requires_flag"] = "flag:lamplight_starlight"   # the Lamplight
# pass owns setting this (no engine axis yet — a safe inert reveal)
owed += pt.sign(m, deco, W, sid="tideglass_nook", at=(3, 5))

# ---- caches (variety: consumable + loose wicks; the shard above is the valuable) ----
owed += pt.cache(m, cid="tideglass_balm", at=(3, 16))
owed += pt.cache(m, cid="tideglass_wicks", at=(24, 6))

# ---- the mouth sign -----------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="tideglass_mouth", at=(3, 9))

# ---- encounters (cave 20-24 Tide; water 21-24 + the signature rare) -----------------
CAVE = [{"kin_id": 26, "weight": 30, "min_level": 20, "max_level": 22},
        {"kin_id": 31, "weight": 26, "min_level": 20, "max_level": 23},
        {"kin_id": 24, "weight": 24, "min_level": 21, "max_level": 24},
        {"kin_id": 27, "weight": 20, "min_level": 21, "max_level": 24}]
WATER = [{"kin_id": 27, "weight": 36, "min_level": 21, "max_level": 24},
         {"kin_id": 24, "weight": 30, "min_level": 21, "max_level": 24},
         {"kin_id": 29, "weight": 24, "min_level": 22, "max_level": 24},
         # the atlas-promised signature rare: Glostrael, the lighthouse line's
         # middle form (very-rare row)
         {"kin_id": 30, "weight": 5, "min_level": 22, "max_level": 24}]
m["encounters"] += [
    {"id": "glass_entry", "terrain": "cave", "rect": {"tx": 3, "ty": 5, "w": 6, "h": 5},
     "encounter_rate": 0.10,
     "table": [dict(t, max_level=min(t["max_level"], 22)) for t in CAVE]},
    {"id": "glass_hall_n", "terrain": "cave", "rect": {"tx": 9, "ty": 3, "w": 10, "h": 5},
     "encounter_rate": 0.10, "table": CAVE},
    {"id": "glass_hall_e", "terrain": "cave", "rect": {"tx": 18, "ty": 8, "w": 5, "h": 5},
     "encounter_rate": 0.10, "table": CAVE},
]
m["encounters"] += pt.zones_from_grid(pool, W, H, terrain="water", rate=0.07,
                                      table=WATER, id_prefix="tidepool")
for z in m["encounters"]:
    if z["id"].startswith("tidepool"):
        z["requires_ability"] = "tidecall"   # belt + braces: the tiles gate anyway

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
