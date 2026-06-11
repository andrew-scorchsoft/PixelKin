#!/usr/bin/env python3
"""
Cinderhead Deep — the deep galleries; the road on, and the shortcut home
(walkthrough/02-east). Glimmerstep mandatory, encounters at the region's
ceiling (band 24-27, §4 — the grind that closes the gap before Otho).

The Descent Vigil's lower leg (spine §5 shape #4): two vigil-miner SIGHT
trainers hold the chamber leg, and at mid-depth the still-lit **vigil-lamp**
waits to be carried back up to Otho (script.take_vigil_lamp ->
flag:q_east_vigil_lamp; gated on flag:q_east_vigil so it only appears once Otho
has asked). Three more beats: the **Crystoll void-gap** tease (`to_crystoll`,
Starreach — a late, signed [LATER] backtrack), the **sealed mine door** opened
from the inside (script.open_mine_shortcut -> flag:shortcut_mine, the
Cinderhead Deep -> Vesper Crossroads re-link, spine §0 rule 3), and the
**ungated gallery out to Galehigh** (`to_terraces`, the East->North handoff —
galehigh unauthored yet, a safe inert tease).

Branchy cave (§2a): A entry -> a LOOP (west gallery B -> vigil-lamp chamber C,
and a right spur straight to the east deep cavern D) -> the sealed far side E.
E is reachable only through the D->E choke, so the shortcut beat can't be
skipped. E3's Foreman's Ledger hides a gallery off B (a dead-end that pays).

Run:  ./venv/bin/python tools/maps/build_cinderhead_deep.py

audit_flow WAIVER — `loop` WARN may stand: the one-way feel is the sealed-door
re-link (set on first reaching E), the mid-dungeon requirement per §2a.
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 30, 26
rng = random.Random(94)
owed: list[str] = []

# ---- terrain: solid rock, the galleries carved out ------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 14, 1, 15, 5)                     # top throat in (from the mine; row 0 stays wall)
mk.blob(floor, W, H, 15.0, 3.5, 4.5, 2.2)              # A — entry chamber
# A -> B (west gallery): a left run down
mk.rect(floor, W, H, 7, 5, 12, 6)                      # A's west shoulder
mk.blob(floor, W, H, 7.5, 10.5, 4.2, 3.4)             # B — west gallery
mk.vline(floor, W, H, 8, 6, 8)                         # choke A-shoulder -> B
# B's dead-end ledger gallery (SW nub) — E3 pays here
mk.hline(floor, W, H, 9, 2, 5)                         # short west spur
mk.blob(floor, W, H, 2.5, 9.0, 1.6, 1.3)             # the ledger alcove
# B -> C (vigil-lamp chamber)
mk.vline(floor, W, H, 8, 13, 17)                       # choke B -> C
mk.blob(floor, W, H, 8.0, 20.0, 3.6, 2.8)            # C — vigil-lamp chamber
# A -> D (the right spur — the LOOP's other arm, §3a rule 1)
mk.rect(floor, W, H, 18, 4, 21, 5)                     # A's east shoulder
mk.vline(floor, W, H, 21, 5, 11)                       # right run down
mk.blob(floor, W, H, 23.0, 12.0, 5.0, 3.8)           # D — east deep cavern
# C -> D (closes the loop): an east hall that stays CLEAR of E (so E's only
# entrance is the D->E choke, where the sealed-door beat can't be skipped)
mk.hline(floor, W, H, 18, 11, 18)                      # C's east hall (north of E)
mk.vline(floor, W, H, 18, 12, 18)                      # up into D
# D -> E (the sealed far side) — a single choke (the shortcut beat sits here)
mk.vline(floor, W, H, 24, 15, 19)                      # choke D -> E
mk.blob(floor, W, H, 24.5, 21.5, 3.6, 2.6)           # E — the far-side chamber
mk.rect(floor, W, H, 27, 21, 29, 22)                   # E -> the gallery out to Galehigh

for i in range(W * H):                                  # carve the rock
    if floor[i]:
        wall[i] = 0

# ---- base + terrain layers ------------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.50 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco: sparse crystal light along the spine, rubble, the sealed door ---------
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


# the deep is darker than the mine — crystal veins only mark the three ways on
for (x, y, n) in [(14, 4, "glowshroom_a"), (8, 8, "glowshroom_b"), (8, 15, "glowshroom_a"),
                  (21, 8, "glowshroom_b"), (24, 12, "glowshroom_a"), (24, 18, "glowshroom_b"),
                  (8, 20, "glowshroom_a")]:
    put(x, y, n)
for (x, y) in [(11, 10), (5, 11), (20, 13), (26, 12), (10, 21), (23, 22)]:
    put(x, y, "boulder")
for (x, y) in [(13, 4), (6, 9), (9, 12), (22, 10), (25, 14), (8, 22), (16, 21), (3, 9)]:
    put(x, y, "g_pebble")
# the sealed mine door, in E's far wall (the shortcut opened from the inside)
put(26, 20, "sign")          # a notice by the sealed door (sign.cinderhead_sealed)

m: dict = {
    "id": "cinderhead_deep", "display_name": "Cinderhead Deep", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [],
    "warps": [
        # UP — back to the mine mouth (graph.ts `to_deep` return half)
        {"id": "to_mine", "at": {"tx": 14, "ty": 1}, "trigger": "step_on",
         "to_map": "cinderhead_mine", "to": {"tx": 13, "ty": 22}, "facing": "up",
         "transition": "fade"},
        {"id": "to_mine_e", "at": {"tx": 15, "ty": 1}, "trigger": "step_on",
         "to_map": "cinderhead_mine", "to": {"tx": 14, "ty": 22}, "facing": "up",
         "transition": "fade"},
        # OUT — the ungated gallery on to Galehigh (East->North handoff, graph.ts
        # `to_terraces`; galehigh unauthored — a safe inert tease for now)
        {"id": "to_terraces", "at": {"tx": 29, "ty": 21}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 1, "ty": 14}, "facing": "right",
         "transition": "fade"},
        {"id": "to_terraces_s", "at": {"tx": 29, "ty": 22}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 1, "ty": 15}, "facing": "right",
         "transition": "fade"},
        # SPUR — Crystoll Vault (graph.ts `to_crystoll`, Starreach — [LATER],
        # the void-gap signed so the come-back is explicit; crystoll unauthored)
        {"id": "to_crystoll", "at": {"tx": 27, "ty": 10}, "trigger": "step_on",
         "to_map": "crystoll_vault", "to": {"tx": 5, "ty": 8}, "facing": "up",
         "requires_ability": "starreach", "transition": "fade"},
        # SHORTCUT — the sealed door opened from the inside re-links to the hub
        # (graph.ts `shortcut_crossroads`, requires_flag set by the far-side beat)
        {"id": "shortcut_crossroads", "at": {"tx": 25, "ty": 22}, "trigger": "step_on",
         "to_map": "vesper_crossroads", "to": {"tx": 8, "ty": 16}, "facing": "up",
         "requires_flag": "flag:shortcut_mine", "transition": "fade"},
    ],
    "triggers": [
        # THE SEALED-DOOR BEAT — on the only choke into E (col 24, rows 15-19),
        # banded so it can't be walked around; sets flag:shortcut_mine and opens
        # the crossroads re-link. The cut's walkable cells are exactly col 24.
        *[{"id": f"open_shortcut_{ty}", "kind": "script", "at": {"tx": 24, "ty": ty},
           "activation": "step_on", "ref": "script.open_mine_shortcut", "once": True,
           "sets_flags": ["flag:shortcut_mine"],
           "hidden_when_flag": "flag:shortcut_mine"}
          for ty in (15, 16, 17, 18, 19)],
        {"id": "sign_sealed", "kind": "sign", "at": {"tx": 26, "ty": 20},
         "activation": "interact", "ref": "sign.cinderhead_sealed"},
    ],
    # band 24-27 (top of band, §4): #49 Gravelo, #45 Sparkrat, #35 Crystink.
    "encounters": [
        {"id": "gallery_b", "terrain": "cave", "rect": {"tx": 4, "ty": 8, "w": 8, "h": 6},
         "encounter_rate": 0.13,
         "table": [{"kin_id": 49, "weight": 45, "min_level": 24, "max_level": 26},
                   {"kin_id": 45, "weight": 35, "min_level": 24, "max_level": 27},
                   {"kin_id": 35, "weight": 20, "min_level": 25, "max_level": 27}]},
        {"id": "cavern_d", "terrain": "cave", "rect": {"tx": 18, "ty": 9, "w": 10, "h": 7},
         "encounter_rate": 0.13,
         "table": [{"kin_id": 49, "weight": 40, "min_level": 25, "max_level": 27},
                   {"kin_id": 45, "weight": 35, "min_level": 25, "max_level": 27},
                   {"kin_id": 35, "weight": 25, "min_level": 25, "max_level": 27}]},
        {"id": "chamber_c", "terrain": "cave", "rect": {"tx": 5, "ty": 18, "w": 7, "h": 5},
         "encounter_rate": 0.12,
         "table": [{"kin_id": 49, "weight": 45, "min_level": 24, "max_level": 26},
                   {"kin_id": 45, "weight": 30, "min_level": 24, "max_level": 26},
                   {"kin_id": 35, "weight": 25, "min_level": 24, "max_level": 26}]},
    ],
    "npcs": [
        # the still-lit VIGIL-LAMP at mid-depth (the Descent Vigil's turnaround) —
        # only present once Otho has sent you for it (flag:q_east_vigil); taking it
        # sets flag:q_east_vigil_lamp and the first visit ends here, carrying it up.
        {"id": "vigil_lamp", "at": {"tx": 8, "ty": 20}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.take_vigil_lamp",
         "requires_flag": "flag:q_east_vigil",
         "hidden_when_flag": "flag:q_east_vigil_lamp"},
        # E3 ledger — the old crew's ledger in B's dead-end alcove
        {"id": "cache_ledger", "at": {"tx": 2, "ty": 9}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_ledger",
         "requires_flag": "flag:q_east_ledger",
         "hidden_when_flag": "flag:q_east_ledger_found"},
        # a high-band crystal cache a choke away (the §4 grind reward)
        {"id": "cache_deepcrystal", "at": {"tx": 27, "ty": 14}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_deepcrystal",
         "hidden_when_flag": "flag:picked_deepcrystal"},
        # the far-side lone miner ("been meaning to clear that door for years")
        {"id": "sealed_miner", "at": {"tx": 23, "ty": 22}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.cinderhead_sealed_miner",
         "requires_flag": "flag:shortcut_mine"},
    ],
    "gates": [],
    "music": "assets/audio/music/cinderhead-mine-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/cinderhead-mine-a.webp",
        "assets/backgrounds/battle/cinderhead-mine-b.webp",
    ],
}

# the two vigil-miner SIGHT trainers (keeper class) holding the chamber leg:
# A on the A->B run (facing down its choke), B guarding the vigil-lamp approach.
owed += pt.trainer_beat(m, tid="gallery_miner_a", at=(8, 7), facing="down",
                        sight=4, sprite="npc_man")
owed += pt.trainer_beat(m, tid="gallery_miner_b", at=(8, 16), facing="down",
                        sight=4, sprite="npc_woman")

# the Crystoll void-gap sign (the [LATER] tease, §5 back-reference)
owed += pt.sign(m, deco, W, sid="cinderhead_crystoll", at=(27, 11))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
