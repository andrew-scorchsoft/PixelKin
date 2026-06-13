#!/usr/bin/env python3
"""
Cinderhead Mine — the abandoned gem-mine settlement at the mine mouth
(walkthrough/02-east; Lumenary 4: Otho Grist, Stone — the deliberate WALL).

The East's second Lumenary and the curve's one designed wall (§4): a miners'
town carved into the rock, lit by fire-lamps and crystal-vein gleam, mid the
**Lamp-down vigil** (Arc E — the most melancholy festival: lamps lowered
together to honour the dark, then raised again). Three signature touches (§8):
  1. THE LOWERED LAMPS — the vigil hangs unfinished; the town's lamps stay
     down until the old crew's vigil-lamp comes up from the deep (dialogue +
     the post-Gleam payoff NPCs that answer once the Stone is relit);
  2. OTHO'S HALL at the mine mouth — squat, stone, the tallest worked thing in
     a town that trusts what endures the dark;
  3. THE DARK `to_deep` MOUTH gaping at the town's back — Glimmerstep-gated,
     signed, the way down to the Descent Vigil.

The earned loop — "The Descent Vigil" (spine §5 shape #4, the HEAVY loop, the
§4 wall made diegetic): Otho's hook in his hall (script.otho_quest ->
flag:q_east_vigil) sends the player DOWN cinderhead_deep through the 24-27
galleries (two vigil-miner sight trainers) to carry the still-lit vigil-lamp
back up (flag:q_east_vigil_lamp); only then does his bond-test open
(requires_flag, blocked in his voice) and the Stone Gleam relight
(gleam:stone -> the engine derives flag:crown_east, East's second quadrant).

Entry west from Glowmoss Deep (`to_mine` lands {1,12}/{1,13}); the way down is
`to_deep` (Glimmerstep, graph.ts:166). Kind `cave` — cavewall border, carved
settlement floor, a rough working gallery in the NE (the mine-mouth encounter
bed, band 22-24).

Run:  ./venv/bin/python tools/maps/build_cinderhead_mine.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 28, 24
rng = random.Random(91)
owed: list[str] = []

# ---- terrain: solid rock, the settlement carved out -----------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

floor = mk.make_grid(W, H)
mk.rect(floor, W, H, 2, 3, 25, 20)                     # the main cavern floor
mk.rect(floor, W, H, 0, 12, 2, 13)                     # west throat in (from the Deepwood)
mk.rect(floor, W, H, 13, 20, 14, 23)                   # south throat down (the to_deep mouth, 2-wide)
# NOTE: no free-standing cavewall masses mid-floor — a wall slab in open ground
# reads as dodgy graphics (level-design §11 r8). Outcrops are boulder/ore-cart
# CLUSTERS (deco + objects) instead, which read as a worked mine, not a void.

for i in range(W * H):                                  # carve the rock
    if floor[i]:
        wall[i] = 0

# the rough WORKING GALLERY (NE) — its own cave encounter bed (rect-wide roll)
gallery = mk.make_grid(W, H)
mk.rect(gallery, W, H, 18, 4, 25, 9)
for i in range(W * H):                                  # only where it's open floor
    if gallery[i] and not floor[i]:
        gallery[i] = 0

# ---- base + terrain layers ------------------------------------------------------
cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

# ---- deco: crystal-vein gleam, fire-lamps, cart rubble, signs --------------------
deco = mk.make_grid(W, H)


def put(x, y, name):
    deco[y * W + x] = gid(name)


# crystal-vein gleam leads the eye along the walked spine (lead with light, §3)
for (x, y, n) in [(2, 12, "glowshroom_a"), (5, 11, "glowshroom_b"), (9, 12, "glowshroom_a"),
                  (13, 6, "glowshroom_b"), (16, 11, "glowshroom_a"), (13, 18, "glowshroom_b"),
                  (21, 7, "glowshroom_a"), (23, 9, "glowshroom_b"), (19, 5, "glowshroom_a")]:
    put(x, y, n)
# wave-worn boulders + cart rubble breaking the floor
for (x, y) in [(6, 16), (10, 18), (17, 17), (22, 12), (4, 7), (24, 16), (16, 5)]:
    put(x, y, "boulder")
for (x, y) in [(8, 14), (12, 16), (15, 13), (20, 18), (5, 18), (18, 8), (23, 6), (11, 6)]:
    put(x, y, "g_pebble")

# ---- objects: the town ----------------------------------------------------------
objects = [
    # Otho's Stone Lumenary — the mine-mouth hall with its timber HEADFRAME tower
    # (bespoke Cinderhead master: stone hall + pit-winch derrick, generated art)
    {"id": "lumenary", "sprite": "cinderhead_lumenary", "at": {"tx": 9, "ty": 2},
     "w": 6, "h": 7, "overhang": 4},
    # miners' cottages cut into the rock
    {"id": "cottage_a", "sprite": "tinderwick_cottage", "at": {"tx": 2, "ty": 15},
     "w": 5, "h": 5, "overhang": 3},
    {"id": "cottage_b", "sprite": "tinderwick_cottage", "at": {"tx": 20, "ty": 3},
     "w": 5, "h": 5, "overhang": 3},
    # worked-mine props: ore-carts on the floor + glowing crystal outcrops (the
    # deep-earth gleam) where the old slabs were — clusters, never a wall slab
    {"id": "ore_cart_a", "sprite": "cinderhead_ore_cart", "at": {"tx": 7, "ty": 7},
     "w": 2, "h": 2, "overhang": 0},
    {"id": "ore_cart_b", "sprite": "cinderhead_ore_cart", "at": {"tx": 19, "ty": 16},
     "w": 2, "h": 2, "overhang": 0},
    {"id": "crystal_a", "sprite": "cinderhead_crystal_cluster", "at": {"tx": 21, "ty": 15},
     "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "crystal_b", "sprite": "cinderhead_crystal_cluster", "at": {"tx": 5, "ty": 9},
     "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    {"id": "crystal_c", "sprite": "cinderhead_crystal_cluster", "at": {"tx": 24, "ty": 8},
     "w": 2, "h": 2, "overhang": 1, "walk_under": True},
    # fire-lamp posts (1x3 — never 1-tile lamps), lowered-vigil flavour in dialogue
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 11, "ty": 10},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 16, "ty": 14},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 7, "ty": 12},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_d", "sprite": "tinderwick_lamp_post", "at": {"tx": 22, "ty": 17},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]

m: dict = {
    "id": "cinderhead_mine", "display_name": "Cinderhead Mine", "width": W, "height": H,
    "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": objects,
    "warps": [
        # WEST — back out to Glowmoss Deep (graph.ts `to_mine` return half; the
        # engine never auto-fires on arrival, so landing near it is safe)
        {"id": "to_glowmoss", "at": {"tx": 0, "ty": 12}, "trigger": "step_on",
         "to_map": "glowmoss_deep", "to": {"tx": 28, "ty": 13}, "facing": "left",
         "transition": "fade"},
        {"id": "to_glowmoss_s", "at": {"tx": 0, "ty": 13}, "trigger": "step_on",
         "to_map": "glowmoss_deep", "to": {"tx": 28, "ty": 14}, "facing": "left",
         "transition": "fade"},
        # SOUTH — the dark way down (graph.ts `to_deep`, Glimmerstep, held since
        # Lowleaf; §0 rule 1 — Stone grants no Gift, so this is legal to gate)
        {"id": "to_deep", "at": {"tx": 13, "ty": 23}, "trigger": "step_on",
         "to_map": "cinderhead_deep", "to": {"tx": 13, "ty": 2}, "facing": "down",
         "requires_ability": "glimmerstep", "blocked_ref": "sign.cinderhead_deep_mouth",
         "transition": "fade"},
        {"id": "to_deep_e", "at": {"tx": 14, "ty": 23}, "trigger": "step_on",
         "to_map": "cinderhead_deep", "to": {"tx": 14, "ty": 2}, "facing": "down",
         "requires_ability": "glimmerstep", "blocked_ref": "sign.cinderhead_deep_mouth",
         "transition": "fade"},
        # Otho's hall. The door art sits OFF-CENTRE (cols 3-4) on the south face;
        # the Lumenary nameplate (sign_cinderhead_lumenary at (13,9)) stands in front
        # of the right half, so the entrance is the single open left tile (12,8) —
        # a deliberate sign-guided entrance, not a two-tile straddle.
        {"id": "to_lumenary", "at": {"tx": 12, "ty": 8}, "trigger": "step_on",
         "to_map": "cinderhead_lumenary", "to": {"tx": 8, "ty": 10}, "facing": "down",
         "transition": "door"},
    ],
    "triggers": [],
    "encounters": [
        # the mine-mouth working gallery (NE) — band 22-24, rate 0.12 (§4: do not
        # under-level the mine). #49 Gravelo (Stone), #45 Sparkrat (Stone/Storm),
        # #35 Crystink (Stone/Light — the crystal-lantern "Glowpan" read).
        {"id": "gallery", "terrain": "cave", "rect": {"tx": 18, "ty": 4, "w": 8, "h": 6},
         "encounter_rate": 0.12,
         "table": [{"kin_id": 49, "weight": 45, "min_level": 22, "max_level": 24},
                   {"kin_id": 45, "weight": 35, "min_level": 22, "max_level": 24},
                   {"kin_id": 35, "weight": 20, "min_level": 22, "max_level": 24}]},
    ],
    "npcs": [
        # --- the Lamp-down vigil (UNCONDITIONAL — the vigil is underway on arrival;
        #     it cannot CLOSE until the vigil-lamp comes up, so the lamps stay low) -
        {"id": "vigil_elder", "at": {"tx": 13, "ty": 12}, "facing": "down",
         "sprite": "npc_old_man", "movement": "static",
         "dialogue_ref": "npc.vigil_elder"},
        {"id": "vigil_miner_a", "at": {"tx": 10, "ty": 14}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.vigil_miner_a"},
        {"id": "vigil_miner_b", "at": {"tx": 17, "ty": 11}, "facing": "left",
         "sprite": "npc_woman", "movement": "static",
         "dialogue_ref": "npc.vigil_miner_b"},
        # the vigil-fire cook = the town's REST point (script ends in `heal`, the
        # standing kit; a mine-mouth hearth instead of an inn)
        {"id": "vigil_cook", "at": {"tx": 6, "ty": 11}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.cinderhead_rest"},
        # --- post-Gleam festival payoff (Arc E: the town visibly answers the win) -
        # C2 "The Inn's Empty Lamps" (Central wiring): the EAST token giver —
        # festival line first, the lamp-token once the chain reaches him.
        {"id": "vigil_raised_a", "at": {"tx": 15, "ty": 13}, "facing": "left",
         "sprite": "npc_old_man", "movement": "look_around",
         "dialogue_ref": "script.token_east",
         "requires_flag": "gleam:stone",
         "hidden_when_flag": "flag:q_token_east"},
        {"id": "vigil_raised_a_after", "at": {"tx": 15, "ty": 13}, "facing": "left",
         "sprite": "npc_old_man", "movement": "look_around",
         "dialogue_ref": "npc.vigil_raised_a",
         "requires_flag": "flag:q_token_east"},
        {"id": "vigil_raised_b", "at": {"tx": 11, "ty": 12}, "facing": "right",
         "sprite": "npc_child", "movement": "wander",
         "dialogue_ref": "npc.vigil_raised_b",
         "requires_flag": "gleam:stone"},
        # --- E3 "The Foreman's Ledger" — the lone miner by the deep mouth (giver;
        #     the ledger itself is recovered a gallery down in cinderhead_deep) ----
        {"id": "ledger_miner", "at": {"tx": 12, "ty": 19}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "script.ledger_quest",
         "hidden_when_flag": "flag:q_east_ledger"},
        {"id": "ledger_miner_wait", "at": {"tx": 12, "ty": 19}, "facing": "right",
         "sprite": "npc_man", "movement": "static",
         "dialogue_ref": "npc.ledger_waiting",
         "requires_flag": "flag:q_east_ledger",
         "hidden_when_flag": "flag:q_east_ledger_found"},
        {"id": "ledger_miner_done", "at": {"tx": 12, "ty": 19}, "facing": "right",
         "sprite": "npc_man", "movement": "look_around",
         "dialogue_ref": "script.ledger_reward",
         "requires_flag": "flag:q_east_ledger_found",
         "hidden_when_flag": "flag:q_east_ledger_done"},
        {"id": "ledger_miner_after", "at": {"tx": 12, "ty": 19}, "facing": "right",
         "sprite": "npc_man", "movement": "look_around",
         "dialogue_ref": "npc.ledger_after",
         "requires_flag": "flag:q_east_ledger_done"},
        # --- the provisioner (kit -> open counter, the standing pattern) ----------
        {"id": "provisioner_kit", "at": {"tx": 18, "ty": 12}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.shop_kit_cinderhead",
         "hidden_when_flag": "flag:cinderhead_kit"},
        {"id": "provisioner", "at": {"tx": 18, "ty": 12}, "facing": "down",
         "sprite": "npc_shopkeeper", "movement": "static",
         "dialogue_ref": "script.shop_cinderhead",
         "requires_flag": "flag:cinderhead_kit"},
        # Wren is gone east by now (A3 landed at Glowmoss Deep) — a miner mentions it
        {"id": "deep_warden", "at": {"tx": 14, "ty": 18}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.cinderhead_deep_warden"},
    ],
    "gates": [],
    "music": "assets/audio/music/cinderhead-mine-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/cinderhead-mine-a.webp",
        "assets/backgrounds/battle/cinderhead-mine-b.webp",
    ],
}

# signs: the welcome, the deep mouth (the blocked_ref line), the hall
owed += pt.sign(m, deco, W, sid="cinderhead_welcome", at=(3, 12))
owed += pt.sign(m, deco, W, sid="cinderhead_deep_mouth", at=(15, 20))
owed += pt.sign(m, deco, W, sid="cinderhead_lumenary", at=(13, 9))

# caches (variety rule: a valuable crystal off the lane, loose wicks, a balm)
owed += pt.cache(m, cid="cinderhead_crystal", at=(24, 5))   # the working gallery's prize
owed += pt.cache(m, cid="cinderhead_wicks", at=(4, 4))      # a takings-tin in the NW pocket (pays the detour)
owed += pt.cache(m, cid="cinderhead_balm", at=(23, 18))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
