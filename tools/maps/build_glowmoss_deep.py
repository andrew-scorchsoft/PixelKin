#!/usr/bin/env python3
"""
Glowmoss Deep — the East's first true cave dungeon (walkthrough/02-east, B2).

The hollow's dark, breathing interior past Lowleaf — only walkable because the
player now holds Glimmerstep (the gate rides Lowleaf's `to_deepwood` warp, graph.ts).
Branchy chambers joined by 1-tile chokes (level-design Fork A cave pattern), built
on the shared set's NEW glowmoss-cave families (gbaforge-drawn: cavefloor /
cavewall faces / glowmoss encounter mounds).

The spine, south→east: entry chamber → glowmoss chamber (sight keeper A on the
corridor) → THE DRAINED SITE (B2: gentle acolytes, the sleeping Fennlight, the
null-lantern, the distant cowled figure) → the relight choke (sets
flag:met_hollowing) → east gallery (sight keeper B) → out to Cinderhead Mine.
Spurs: a NW alcove (Moth-amber, the region's valuable cache) and the SE
Spore Grotto mouth (Glimmerstep warp tease + sign).

Run:  python3 tools/maps/build_glowmoss_deep.py   (after build_shared_overworld.py)

audit_flow WAIVER — `loop` WARN accepted: this is the East's FIRST dungeon
(level-design §2a — the story set-piece tier; the one-way drop/shortcut loop
is the MID-dungeon requirement, arriving with Cinderhead Deep). Same waiver
applies to the B1F floor below.
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 30, 28
rng = random.Random(67)

# ---- terrain: solid wall mass, rooms carved as organic blobs -------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)                # rock everywhere…

floor = mk.make_grid(W, H)                             # …the carved rooms
mk.blob(floor, W, H, 8.0, 22.5, 4.5, 3.0)              # A — entry chamber (S)
mk.rect(floor, W, H, 7, 24, 8, 27)                     # entry throat to the S edge
mk.vline(floor, W, H, 8, 17, 19)                       # choke A→B (1-wide)
mk.blob(floor, W, H, 8.0, 12.5, 5.5, 3.8)              # B — glowmoss chamber
mk.vline(floor, W, H, 5, 8, 9)                         # choke B→NW alcove (1-wide)
mk.blob(floor, W, H, 4.5, 5.5, 2.5, 2.0)               # NW alcove (Moth-amber)
mk.hline(floor, W, H, 12, 12, 15)                      # choke B→C (1-wide) — B2 beat
mk.blob(floor, W, H, 17.5, 9.5, 4.0, 3.2)              # C — THE DRAINED SITE
mk.hline(floor, W, H, 10, 21, 24)                      # choke C→D (1-wide) — the relight
mk.blob(floor, W, H, 25.5, 13.5, 3.0, 4.4)             # D — east gallery
mk.vline(floor, W, H, 25, 17, 19)                      # choke D→SE alcove (1-wide)
mk.blob(floor, W, H, 25.0, 21.5, 2.4, 1.8)             # SE alcove (Spore Grotto mouth)
mk.rect(floor, W, H, 27, 13, 29, 14)                   # exit gallery to the E edge

for i in range(W * H):                                  # carve the rock
    if floor[i]:
        wall[i] = 0

# glowmoss (the cave encounter terrain) — shaped patches across the walked lanes
glow = mk.make_grid(W, H)
mk.blob(glow, W, H, 7.5, 12.5, 3.5, 2.0)               # B: dense glow-grass on the lane
mk.blob(glow, W, H, 25.5, 15.5, 2.2, 2.0)              # D: gallery moss
mk.blob(glow, W, H, 25.0, 21.0, 1.8, 1.3)              # SE alcove: the spur's rarer bed
for i in range(W * H):                                  # moss only grows on open floor
    if glow[i] and not floor[i]:
        glow[i] = 0
# C is the DRAINED site: no living moss there (grey decor instead, no encounters)
for y in range(5, 14):
    for x in range(13, 23):
        glow[y * W + x] = 0

# ---- base + terrain layers -----------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_glowmoss", "role": "terrain", "terrain": "glowmoss",
     "set": "vesper_overworld_set", "depth": 0, "data": glow},
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco: shrooms (light breadcrumbs), grey moss, boulders, the null-lantern ---
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


# glow-shroom breadcrumbs along the walked spine (lead with light, §3)
for (x, y, n) in [(6, 24, "glowshroom_a"), (8, 20, "glowshroom_a"),
                  (6, 16, "glowshroom_b"), (11, 14, "glowshroom_a"), (12, 11, "glowshroom_b"),
                  (4, 10, "glowshroom_a"), (3, 6, "glowshroom_b"),
                  (24, 12, "glowshroom_a"), (27, 15, "glowshroom_b"),
                  (24, 20, "glowshroom_b"), (26, 22, "glowshroom_a")]:
    put(x, y, n)
# the drained site: every tuft grey, nothing glows (B2 set dressing)
for (x, y, n) in [(15, 8, "greymoss_a"), (16, 11, "greymoss_b"), (20, 12, "greymoss_b"),
                  (20, 11, "greymoss_a"), (18, 12, "greymoss_b"), (14, 10, "greymoss_b"),
                  (19, 7, "greymoss_a"), (16, 7, "greymoss_b")]:
    put(x, y, n)
# wave-worn boulders breaking the chamber floors
for (x, y) in [(5, 21), (11, 23), (4, 12), (12, 15), (26, 17), (27, 11), (23, 21)]:
    put(x, y, "boulder")
# stray pale pebbles
for (x, y) in [(9, 24), (6, 13), (9, 14), (26, 14), (24, 15), (16, 12), (20, 9), (3, 5)]:
    put(x, y, "g_pebble")
# signs: the mouth (entry) + the Spore Grotto turn-off (tease, signed)
SIGN_MOUTH = (6, 22)
SIGN_GROTTO = (24, 22)
put(*SIGN_MOUTH, "sign")
put(*SIGN_GROTTO, "sign")
# the SE alcove's LADDER-PIT down to B1F (the dungeon-scale ladder, §11a) —
# the Spore Grotto's true mouth now sits a floor below.
LADDER_DOWN = (25, 23)
deco[LADDER_DOWN[1] * W + LADDER_DOWN[0]] = gid("cave_ladder_down")

# ---- assemble --------------------------------------------------------------------
m = {
    "id": "glowmoss_deep", "display_name": "Glowmoss Deep", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    # Generated-object set-dressing (packed via pack_objects.py — image-gen is
    # for OBJECTS, terrain stays drawn): the mossheart tree is chamber B's living
    # landmark; the NULL-LANTERN SHRINE is the drained site's centrepiece (the
    # relight script cameraFocuses it); the shroom clusters bookend the spine.
    "objects": [
        {"id": "mossheart", "sprite": "glowmoss_deep_mossheart_tree",
         "at": {"tx": 9, "ty": 8}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
        {"id": "null_lantern_shrine", "sprite": "glowmoss_deep_null_lantern_shrine",
         "at": {"tx": 18, "ty": 7}, "w": 2, "h": 3, "overhang": 1, "walk_under": False},
        {"id": "shrooms_entry", "sprite": "glowmoss_deep_glowshrooms_teal",
         "at": {"tx": 9, "ty": 21}, "w": 2, "h": 2, "overhang": 1, "walk_under": True},
        {"id": "shrooms_gallery", "sprite": "glowmoss_deep_glowshrooms_ember",
         "at": {"tx": 25, "ty": 12}, "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    ],
    "warps": [
        # South throat back to Lowleaf Hollow (2-wide: a warp on EVERY open tile).
        # Lowleaf is unauthored yet — inert tease until its builder pairs the landing.
        {"id": "to_lowleaf_w", "at": {"tx": 7, "ty": 27}, "trigger": "step_on",
         "to_map": "lowleaf_hollow", "to": {"tx": 14, "ty": 1}, "facing": "down",
         "transition": "fade"},
        {"id": "to_lowleaf_e", "at": {"tx": 8, "ty": 27}, "trigger": "step_on",
         "to_map": "lowleaf_hollow", "to": {"tx": 15, "ty": 1}, "facing": "down",
         "transition": "fade"},
        # East gallery out to the Cinderhead mine mouth (graph.ts `to_mine`, ungated).
        {"id": "to_mine", "at": {"tx": 29, "ty": 13}, "trigger": "step_on",
         "to_map": "cinderhead_mine", "to": {"tx": 1, "ty": 12}, "facing": "right",
         "transition": "fade"},
        {"id": "to_mine_s", "at": {"tx": 29, "ty": 14}, "trigger": "step_on",
         "to_map": "cinderhead_mine", "to": {"tx": 1, "ty": 13}, "facing": "right",
         "transition": "fade"},
        # The ladder down to B1F — lands ON the lower floor's up-ladder (the
        # audited mutual pair; the engine never auto-fires a warp on arrival).
        {"id": "ladder_down", "at": {"tx": LADDER_DOWN[0], "ty": LADDER_DOWN[1]},
         "trigger": "step_on", "to_map": "glowmoss_deep_b1f", "to": {"tx": 19, "ty": 4},
         "facing": "down", "transition": "fade"},
    ],
    "triggers": [
        {"id": "sign_mouth", "kind": "sign",
         "at": {"tx": SIGN_MOUTH[0], "ty": SIGN_MOUTH[1]},
         "activation": "interact", "ref": "sign.glowmoss_mouth"},
        {"id": "sign_grotto", "kind": "sign",
         "at": {"tx": SIGN_GROTTO[0], "ty": SIGN_GROTTO[1]},
         "activation": "interact", "ref": "sign.glowmoss_grotto"},
        # B2 — first Hollowing contact: fires on the only choke into the drained
        # site (can't be walked around). The acolytes, the sleeping kin, the
        # distant cowled figure (the Còr foreshadow — no battle, no name said twice).
        # The true cut is the x=14 column, rows 10-12 (audit_flow proved a single
        # tile here was bypassable) — band the whole column, gate-warden style;
        # the flag pair hides the band after the first fire.
        *[{"id": f"drained_site_{ty}", "kind": "cutscene", "at": {"tx": 14, "ty": ty},
           "activation": "step_on", "ref": "script.glowmoss_drained", "once": True,
           "sets_flags": ["flag:seen_drained_site"],
           "hidden_when_flag": "flag:seen_drained_site"}
          for ty in (10, 11, 12)],
        # The null-lantern restoration — on the only choke OUT of the site east,
        # so no player can tunnel to Cinderhead past it (walkthrough §5 callout).
        {"id": "glowmoss_relight", "kind": "script", "at": {"tx": 22, "ty": 10},
         "activation": "step_on", "ref": "script.glowmoss_relight", "once": True,
         "sets_flags": ["flag:met_hollowing"]},
    ],
    # Cave band 20-22 (walkthrough hooks), rate 0.12 — denser, claustrophobic
    # (level-design Fork E). #56 Sporeling (Verdant), #38 Mossglow (Light/Verdant
    # — the glowing moss kin), #67 Fennlight (Verdant/Light, the town signature).
    # The DRAINED site has no zone at all: the moss is grey, the kin are gone —
    # that absence IS the Hollowing. Once the null-lantern is relit
    # (flag:met_hollowing) the chamber wakes: a quiet flag-gated cave-floor bed
    # blooms in (EncounterZone.requires_flag) — life seeping back, not a thicket.
    "encounters": [
        {"id": "drained_woken", "terrain": "cave", "rect": {"tx": 14, "ty": 6, "w": 8, "h": 7},
         "encounter_rate": 0.06, "requires_flag": "flag:met_hollowing",
         "table": [{"kin_id": 38, "weight": 55, "min_level": 20, "max_level": 22},
                   {"kin_id": 67, "weight": 45, "min_level": 21, "max_level": 22}]},
        {"id": "glow_b", "terrain": "tall_grass", "rect": {"tx": 4, "ty": 11, "w": 8, "h": 4},
         "encounter_rate": 0.12,
         "table": [{"kin_id": 56, "weight": 45, "min_level": 20, "max_level": 22},
                   {"kin_id": 38, "weight": 30, "min_level": 20, "max_level": 22},
                   {"kin_id": 67, "weight": 25, "min_level": 20, "max_level": 22}]},
        {"id": "glow_d", "terrain": "tall_grass", "rect": {"tx": 23, "ty": 14, "w": 6, "h": 4},
         "encounter_rate": 0.12,
         "table": [{"kin_id": 56, "weight": 45, "min_level": 20, "max_level": 22},
                   {"kin_id": 38, "weight": 30, "min_level": 20, "max_level": 22},
                   {"kin_id": 67, "weight": 25, "min_level": 21, "max_level": 22}]},
        # The grotto-mouth alcove: the deeper bed — a low-weight Sporemid is the
        # "something older grows down here" read on the spur's doorstep.
        {"id": "glow_grotto", "terrain": "tall_grass", "rect": {"tx": 23, "ty": 20, "w": 5, "h": 3},
         "encounter_rate": 0.10,
         "table": [{"kin_id": 56, "weight": 45, "min_level": 21, "max_level": 22},
                   {"kin_id": 38, "weight": 25, "min_level": 21, "max_level": 22},
                   {"kin_id": 57, "weight": 15, "min_level": 21, "max_level": 22},
                   {"kin_id": 67, "weight": 15, "min_level": 21, "max_level": 22}]},
    ],
    "npcs": [
        # --- sight keepers (level-design §11 rule 7; keeper class, 10-economy §4) ---
        # A: posted at the head of the A→B corridor, facing down his own column —
        # the climb into the glowmoss chamber is unavoidable.
        {"id": "glowmoss_keeper_a", "at": {"tx": 8, "ty": 15}, "facing": "down",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "script.glowmoss_keeper_a",
         "sight_range": 4, "defeated_flag": "flag:glowmoss_keeper_a_beaten",
         "hidden_when_flag": "flag:glowmoss_keeper_a_beaten"},
        {"id": "glowmoss_keeper_a_after", "at": {"tx": 8, "ty": 15}, "facing": "down",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.glowmoss_keeper_a_after",
         "requires_flag": "flag:glowmoss_keeper_a_beaten"},
        # B: watches the mouth of the relight choke from the east gallery —
        # stepping out of the drained site walks straight into her line.
        {"id": "glowmoss_keeper_b", "at": {"tx": 24, "ty": 14}, "facing": "up",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "script.glowmoss_keeper_b",
         "sight_range": 4, "defeated_flag": "flag:glowmoss_keeper_b_beaten",
         "hidden_when_flag": "flag:glowmoss_keeper_b_beaten"},
        {"id": "glowmoss_keeper_b_after", "at": {"tx": 24, "ty": 14}, "facing": "up",
         "sprite": "npc_woman", "movement": "look_around",
         "dialogue_ref": "npc.glowmoss_keeper_b_after",
         "requires_flag": "flag:glowmoss_keeper_b_beaten"},
        # --- the drained site cast (B2) — all withdraw once the lantern is relit ---
        {"id": "acolyte_a", "at": {"tx": 16, "ty": 9}, "facing": "right",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "npc.glowmoss_acolyte_a",
         "hidden_when_flag": "flag:met_hollowing"},
        {"id": "acolyte_b", "at": {"tx": 19, "ty": 10}, "facing": "up",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.glowmoss_acolyte_b",
         "hidden_when_flag": "flag:met_hollowing"},
        {"id": "cowled_figure", "at": {"tx": 20, "ty": 7}, "facing": "down",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.glowmoss_cowled",
         "hidden_when_flag": "flag:met_hollowing"},
        # the sleeping luminous kin (a dimmed Fennlight) → the woken one, by flag pair
        {"id": "sleeping_fennlight", "at": {"tx": 17, "ty": 8}, "facing": "down",
         "sprite": "fennlight_dim", "movement": "static",
         "dialogue_ref": "npc.glowmoss_sleeper",
         "hidden_when_flag": "flag:met_hollowing"},
        {"id": "woken_fennlight", "at": {"tx": 17, "ty": 8}, "facing": "down",
         "sprite": "fennlight_dim", "movement": "look_around",
         "dialogue_ref": "npc.glowmoss_woken",
         "requires_flag": "flag:met_hollowing"},
        # A3 — Wren, shaken, just past the site (dialogue-only; the battle is South's)
        {"id": "wren_glowmoss", "at": {"tx": 27, "ty": 16}, "facing": "left",
         "sprite": "wren", "movement": "static",
         "dialogue_ref": "npc.wren_glowmoss",
         "requires_flag": "flag:met_hollowing"},
        # --- item caches (spine kit: 2-3 per map, one VALUABLE, one loose-wicks) ---
        {"id": "cache_amber", "at": {"tx": 4, "ty": 5}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_glowmoss_amber",
         "hidden_when_flag": "flag:picked_glowmoss_amber"},
        {"id": "cache_balm", "at": {"tx": 4, "ty": 14}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_glowmoss_balm",
         "hidden_when_flag": "flag:picked_glowmoss_balm"},
        {"id": "cache_wicks", "at": {"tx": 27, "ty": 10}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": "script.pickup_glowmoss_wicks",
         "hidden_when_flag": "flag:picked_glowmoss_wicks"},
    ],
    "gates": [],
    "music": "assets/audio/music/lowleaf-hollow-c.mp3",
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
