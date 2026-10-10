#!/usr/bin/env python3
"""
Duskapple Orchard (duskapple_orchard) — Tinderwick's old orchard, through the
hedge gap at the WEST end of the square (R8, 2026-10).

A small, SAFE-feeling side area that earns its walk:
  * the OPENING DETOUR — the trade-cart courier (Maudie) carted Fenn's satchel
    off from the store counter with her parcels, then threw a wheel here. The
    satchel waits on the cart's tail (the SAME `fenn_satchel` placement +
    `script.take_satchel` -> `flag:has_satchel` contract that used to live in
    the store); the keeper's errand line sends you WEST, and Andrew's WHERE
    NEXT? says the same. A short, obvious detour: the orchard is one screen
    from the square and the satchel sits a few steps off the central ride.
  * Wren (A1, pre-starter) — moved here from the town garden.
  * Old Wendel the orchard-keeper, and his apples that ripened by starlight.
  * a low-level tall-grass meadow (lv 2-4, the verge's own kin + a Glimflit)
    — a safe place for a struggling player to train before the coast. Pre-
    starter it's inert (wild encounters never fire with an empty party).
  * two caches: balms under the old tree (on the way), and a LUMEN DROP in
    the far SW corner past the meadow (off-lane: you went looking).
  * THE FALLEN STAR (R9, the peril thread — docs/world/walkthrough/
    08-the-peril-thread.md): three nights before the game opens a guttered
    star's cinder struck the north rows. Where the middle tree stood there is
    a scorched crater (`fallenstar_crater`, a drawn non-solid decal — the frozen
    tile set can't draw one) round a cold `fallenstar_cinder_star`, flanked by two CHARRED trees
    (`fallenstar_tree_charred`). A once-only step_on band at the mouth plays
    `script.orchard_first_sight`; Wendel + his granddaughter Tamsin carry the
    grief in flag-staged scripts. HEALING: `gleam:ember` -> shoots in the burn
    (closed nightflowers); `flag:dawn` -> they bloom, the charred trees leaf
    again (living-tree twins, same footprint), the cinder wakes into a star
    shard (same 2x2 footprint + solidity — collision is flag-blind).

Wiring: `to_tinderwick(_s)` (21, 8-9) -> tinderwick (0, 8-9) facing right;
tinderwick's `to_orchard(_s)` (0, 8-9) lands ON (21, 8-9). Landings sit on the
return warps (the engine never auto-fires a step_on warp on arrival).

Encounters are CURATED: mirrored as ORCHARD_ENCOUNTERS in
tools/balance/build_species.py (+ `duskapple_orchard` in CURATED_AREAS).

Run:  python3 tools/maps/build_duskapple_orchard.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 22, 18
rng = random.Random(8108)
owed: list[str] = []

tree = mk.make_grid(W, H)
path = mk.make_grid(W, H)
tallgrass = mk.make_grid(W, H)

# ---- the enclosure: deep hedge on every side but the east mouth -------------------
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(6, 2, 1), (2, 6, 1), (19, 3, 1), (20, 13, 1)], rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)          # south hedge (rows 16-17)
for y in (7, 8, 9, 10):                              # the east mouth (rows 8-9) + its shoulders
    for x in (19, 20, 21):
        if y in (8, 9) or x == 19:
            tree[y * W + x] = 0

# ---- the central ride: the cart-track from the mouth west, then a spur to the cart -
mk.rect(path, W, H, 3, 8, W - 1, 9)
mk.vline(path, W, H, 16, 10, 10)                     # spur down to the cart's tail

# ---- the SW meadow (the training patch): hard-edged tuft grass -------------------
mk.blob(tallgrass, W, H, 6.5, 12.5, 4.0, 2.0)
for (x, y) in ((3, 11), (10, 11), (3, 14), (10, 14)):
    tallgrass[y * W + x] = 0

# the cider pond, below the cart's turn (where the wheel went)
pond = mk.make_grid(W, H)
mk.rect(pond, W, H, 15, 13, 18, 15)

for i in range(W * H):
    if tree[i]:
        pond[i] = 0
        path[i] = 0
        tallgrass[i] = 0
    if path[i]:
        tallgrass[i] = 0

terrain_layers = [
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_pond", "role": "terrain", "terrain": "pond",
     "set": "vesper_overworld_set", "depth": 0, "data": pond},
]

gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]
deco = mk.make_grid(W, H)

m: dict = {
    "id": "duskapple_orchard", "display_name": "Duskapple Orchard",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/tinderwick-c.mp3",
}

# ---- the orchard rows: old fruit trees in a loose grid (walk-under crowns, solid
# trunk row) — alleys between them are the orchard's own lanes -----------------------
# apple_1 (7,2) was the tree the star struck — gone; the crater sits in its place.
for i, at in [(3, (17, 1)), (4, (11, 12))]:
    pt.crown_tree(m, oid=f"apple_{i}", sprite="tinderwick_tree", at=at)
# its two neighbours burned: CHARRED until the dawn, then leafed again (a swap
# pair on the SAME footprint/overhang/walk_under — collision is flag-blind).
for i, at in [(0, (3, 2)), (2, (11, 2))]:
    pt.crown_tree(m, oid=f"apple_{i}_charred", sprite="fallenstar_tree_charred", at=at)
    m["objects"][-1]["hidden_when_flag"] = "flag:dawn"
    pt.crown_tree(m, oid=f"apple_{i}", sprite="tinderwick_tree", at=at)
    m["objects"][-1]["requires_flag"] = "flag:dawn"

# the fallen star itself, seated where the first tree stood (solid 2x2) -- and,
# once the sky is whole, the same cinder woken into a star shard.
STAR = (7, 4)   # seated in the crater decal's pit
m["objects"].append({"id": "cinder_star", "sprite": "fallenstar_cinder_star",
                     "at": {"tx": STAR[0], "ty": STAR[1]}, "w": 2, "h": 2, "overhang": 1,
                     "hidden_when_flag": "flag:dawn"})
m["objects"].append({"id": "cinder_star_woken", "sprite": "vigil_star_shard",
                     "at": {"tx": STAR[0], "ty": STAR[1]}, "w": 2, "h": 2, "overhang": 1,
                     "requires_flag": "flag:dawn"})
# the shoots that come up in the burn once the Ember is relit, and their bloom
# at dawn (a `solid: False` 3x1 pair on the crater's south lip — never collides).
m["objects"].append({"id": "burn_shoots", "sprite": "solarium_nightflowers_closed",
                     "at": {"tx": 6, "ty": 6}, "w": 3, "h": 1, "solid": False, "requires_flag": "gleam:ember",
                     "hidden_when_flag": "flag:dawn"})
m["objects"].append({"id": "burn_bloom", "sprite": "solarium_nightflowers_bloomed",
                     "at": {"tx": 6, "ty": 6}, "w": 3, "h": 1, "solid": False, "requires_flag": "flag:dawn"})

# Wendel's apple stall (north side of the ride, east) and the courier's cart
# (south of the ride, at the end of its spur — it threw a wheel on the turn).
m["objects"].append({"id": "apple_stall", "sprite": "lowleaf_stall",
                     "at": {"tx": 14, "ty": 5}, "w": 2, "h": 2, "overhang": 1})
m["objects"].append({"id": "trade_cart", "sprite": "solarium_troupe_cart",
                     "at": {"tx": 15, "ty": 11}, "w": 3, "h": 2, "overhang": 1})
m["objects"].append({"id": "lamp_ride", "sprite": "tinderwick_lamp_post",
                     "at": {"tx": 10, "ty": 5}, "w": 1, "h": 3, "overhang": 2,
                     "walk_under": True})

# a slat fence along the meadow's top, gap left at the ride end so it's a field,
# not a pen (you step down into the grass from the ride)
mk.fence_run(deco, W, H, 4, 10, 8)

owed += pt.sign(m, deco, W, sid="duskapple_orchard", at=(18, 7))
# the variety rule: consumables on the way, the valuable off the lane
owed += pt.cache(m, cid="orchard_windfall", at=(12, 6))
owed += pt.cache(m, cid="orchard_drop", at=(2, 15))

# ---- the satchel errand: Fenn's satchel on the cart's tail (moved here from the
# store counter — same placement id + script + flag contract) ------------------------
m["npcs"].append({"id": "fenn_satchel", "at": {"tx": 16, "ty": 10}, "facing": "down",
                  "sprite": "item_cache", "movement": "static",
                  "dialogue_ref": "script.take_satchel",
                  "requires_flag": "flag:fenn_errand",
                  "hidden_when_flag": "flag:has_satchel"})

# Maudie the courier, beside her wheel-less cart (three flag-disjoint stages).
for nid, ref, req, hide in [
    ("courier", "npc.orchard_courier", None, "flag:fenn_errand"),
    ("courier_errand", "npc.orchard_courier_errand", "flag:fenn_errand", "flag:has_satchel"),
    ("courier_after", "npc.orchard_courier_after", "flag:has_satchel", None),
]:
    n = {"id": nid, "at": {"tx": 18, "ty": 11}, "facing": "left", "sprite": "npc_woman",
         "movement": "static", "dialogue_ref": ref}
    if req:
        n["requires_flag"] = req
    if hide:
        n["hidden_when_flag"] = hide
    m["npcs"].append(n)

# Old Wendel at his stall — and, once the sky is relit, his apples glow again.
m["npcs"].append({"id": "wendel", "at": {"tx": 16, "ty": 6}, "facing": "left",
                  "sprite": "npc_old_man", "movement": "look_around",
                  "dialogue_ref": "script.orchard_wendel", "hidden_when_flag": "flag:dawn"})
m["npcs"].append({"id": "wendel_dawn", "at": {"tx": 16, "ty": 6}, "facing": "left",
                  "sprite": "npc_old_man", "movement": "look_around",
                  "dialogue_ref": "npc.orchard_wendel_dawn", "requires_flag": "flag:dawn"})

# Tamsin, Wendel's granddaughter, at the crater's lip — one placement, a
# flag-staged script (shock -> fear after dusk_begins -> shoots -> the dawn).
m["npcs"].append({"id": "tamsin", "at": {"tx": 9, "ty": 6}, "facing": "left", "sprite": "npc_girl",
                  "movement": "static", "dialogue_ref": "script.orchard_tamsin"})

# FIRST SIGHT — a once-only band across the whole mouth (every walkable cell of
# the cut, x=20 rows 8-9), so nobody walks round it. Pure colour: it never gates.
for y in (8, 9):
    m["triggers"].append({"id": f"first_sight_{y}", "kind": "cutscene",
                          "at": {"tx": 20, "ty": y}, "activation": "step_on",
                          "ref": "script.orchard_first_sight", "once": True,
                          "sets_flags": ["flag:orchard_strike_seen"],
                          "hidden_when_flag": "flag:orchard_strike_seen"})

# Wren (A1) — the rival, "helping" with the cart until the Wayfaring begins.
m["npcs"].append({"id": "wren", "at": {"tx": 9, "ty": 7}, "facing": "down", "sprite": "wren",
                  "movement": "wander", "dialogue_ref": "npc.wren_intro",
                  "hidden_when_flag": "flag:has_starter"})

# ---- the meadow's tables: the journey band (lv 2-4, the verge's kin + a Glimflit)
# and its flag:dawn day-form twin (the R4 convention) ---------------------------------
NIGHT = [{"kin_id": 16, "weight": 45, "min_level": 2, "max_level": 4},
         {"kin_id": 10, "weight": 30, "min_level": 2, "max_level": 4},
         {"kin_id": 8, "weight": 17, "min_level": 3, "max_level": 4},
         {"kin_id": 5, "weight": 8, "min_level": 3, "max_level": 4}]
DAY = [{"kin_id": 16, "weight": 35, "min_level": 55, "max_level": 60},
       {"kin_id": 10, "weight": 25, "min_level": 55, "max_level": 58},
       {"kin_id": 8, "weight": 25, "min_level": 56, "max_level": 62},
       {"kin_id": 5, "weight": 15, "min_level": 56, "max_level": 60}]
for z in pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.08,
                            table=NIGHT, id_prefix="meadow"):
    day = dict(z, id=z["id"] + "_day", table=DAY, requires_flag="flag:dawn")
    z["hidden_when_flag"] = "flag:dawn"
    m["encounters"] += [z, day]

# ---- warps: the east mouth back to the square ----------------------------------------
for y, sfx in ((8, ""), (9, "_s")):
    m["warps"].append({"id": f"to_tinderwick{sfx}", "at": {"tx": W - 1, "ty": y},
                       "trigger": "step_on", "to_map": "tinderwick",
                       "to": {"tx": 0, "ty": y}, "facing": "right", "transition": "fade"})

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

obj_cells = {(x, y) for o in m["objects"]
             for y in range(o["at"]["ty"], o["at"]["ty"] + o.get("h", 1))
             for x in range(o["at"]["tx"], o["at"]["tx"] + o.get("w", 1))}
npc_cells = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.16,
                 avoid=obj_cells | npc_cells | {(x, y) for y in range(H) for x in range(W)
                                                if path[y * W + x] or tree[y * W + x]
                                                or tallgrass[y * W + x] or pond[y * W + x]},
                 flowers=0.35)
# a few windfall-heavy boulders where the old wall used to run
for (x, y) in ((2, 10), (19, 15), (13, 15)):
    if not (tree[y * W + x] or pond[y * W + x]):
        deco[y * W + x] = gid("boulder")

# ---- THE CRATER: a guttered star's strike where apple_1 stood ----------------------
# The strike is ONE drawn, non-solid ground decal (`fallenstar_crater`, 6x4: radial
# scorch, ash-earth bowl, lit lip, charred pit, cold cracks — see
# draw_fallenstar_objects.py); the frozen tile set's flat fills square off a blob
# and read as a texture error, not a fall. Here we only clear the decor under it
# and singe the grass round its rim (dead grey tufts + grit, no flowers), plus two
# thrown-up stones. Its own rng, so the rest of the orchard is unchanged.
crng = random.Random(9119)
CRATER_AT, CRATER_W, CRATER_H = (5, 3), 6, 4
under = {(x, y) for y in range(CRATER_AT[1], CRATER_AT[1] + CRATER_H)
         for x in range(CRATER_AT[0], CRATER_AT[0] + CRATER_W)}
for (x, y) in under:
    deco[y * W + x] = 0
ROCKS = ((5, 7), (11, 6))
for y in range(CRATER_AT[1] - 1, CRATER_AT[1] + CRATER_H + 2):
    for x in range(CRATER_AT[0] - 2, CRATER_AT[0] + CRATER_W + 2):
        if not (0 <= x < W and 0 <= y < H) or (x, y) in under or (x, y) in ROCKS:
            continue
        i = y * W + x
        if tree[i] or path[i]:
            continue
        r = crng.random()
        if r < 0.30:
            deco[i] = crng.choice([gid("greymoss_a"), gid("greymoss_b")])
        elif r < 0.45:
            deco[i] = gid("g_pebble")
        else:
            deco[i] = 0          # no flowers or daisies at the burn's edge
for (x, y) in ROCKS:          # thrown-up stones on the rim (solid, off the walk)
    deco[y * W + x] = gid("boulder")
# the decal goes FIRST so every other object (the cinder, the charred trunks)
# draws over it at the shared body depth
m["objects"].insert(0, {"id": "star_crater", "sprite": "fallenstar_crater",
                        "at": {"tx": CRATER_AT[0], "ty": CRATER_AT[1]},
                        "w": CRATER_W, "h": CRATER_H, "solid": False})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
