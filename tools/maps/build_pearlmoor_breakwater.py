#!/usr/bin/env python3
"""
Build Pearlmoor Breakwater — the Causeway Bell's walk (walkthrough/01-south,
spine §5 shape #2) — on the SHARED overworld set.

A south-exposed stone causeway out over the black harbour: the moor-gate end
joins Pearlmoor Quay's south-east root (gated on `flag:q_south_has_rope`, the
netmender's rope), and the silent MOOR-BELL SHRINE stands on the wide platform
at the far end. Walked ON FOOT the whole way (spine §0 rule 1 — no Tidecall
content anywhere on it): the causeway is carved sand/boards, never gated water.

The walk itself is the 12->14 on-ramp toward Reyl's ace 16: two net-hand SIGHT
trainers (Maren, Cob) hold one-tile boulder chokes so the crossing is mandatory
(level-design §3a "trainers are geometry"), lantern posts pace the legs, two
caches pay the seaward edges, and `script.ring_moorbell` at the shrine sets
`flag:q_south_bell_rung` — the flag Reyl's bond-test waits on.

Flow-audit notes (design intent, not debt):
  * the route is deliberately a corridor — it is a breakwater; the §2b loop
    lives at region scale (quay -> flats errand -> quay -> causeway -> bell).
  * trainer chokes at (5,7) and (7,12) are single-tile by design; their
    trainers face straight up those columns (sight 3) so there is no free pass.

Run:  python3 tools/maps/build_pearlmoor_breakwater.py   (after build_pearlmoor.py)
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 12, 28
rng = random.Random(23)

# ---- terrain presence grids -------------------------------------------------
# Black water everywhere; the causeway is CARVED out of it as a sand/stone
# ribbon (dock boards + boulder riprap on the deco pass), so it is walkable on
# foot and never inherits the water tiles' Tidecall gate.
water = mk.make_grid(W, H)
mk.rect(water, W, H, 0, 0, W - 1, H - 1)

sand = mk.make_grid(W, H)
mk.rect(sand, W, H, 4, 0, 7, 7)        # north leg, off the quay root
mk.rect(sand, W, H, 3, 8, 8, 11)       # the elbow platform (Maren's post)
mk.rect(sand, W, H, 6, 12, 9, 17)      # east leg (Cob's post)
mk.rect(sand, W, H, 4, 18, 8, 20)      # the jog back west
mk.rect(sand, W, H, 3, 21, 9, 26)      # the Moor-bell shrine platform
for i in range(len(sand)):             # causeway tiles displace the sea
    if sand[i]:
        water[i] = 0

# the walked lane: worn boards/trail snaking leg to leg, paused at the chokes
path = mk.make_grid(W, H)
mk.vline(path, W, H, 5, 1, 6)
mk.vline(path, W, H, 6, 1, 6)
mk.hline(path, W, H, 9, 5, 7)          # across the elbow
mk.vline(path, W, H, 7, 10, 11)        # down to choke 2
mk.vline(path, W, H, 7, 13, 14)        # east leg (Cob stands at (7,15))
mk.vline(path, W, H, 8, 13, 16)
mk.hline(path, W, H, 18, 5, 7)         # the jog west
mk.vline(path, W, H, 5, 18, 20)
mk.vline(path, W, H, 5, 24, 25)        # the shrine approach (bell base at row 23)
mk.vline(path, W, H, 6, 24, 25)

# ---- base = sea-toned scatter; terrain layers mesh over it -------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_sand", "role": "terrain", "terrain": "sand",
     "set": "vesper_overworld_set", "depth": 0, "data": sand},
    {"name": "t_water", "role": "terrain", "terrain": "water",
     "set": "vesper_overworld_set", "depth": 0, "data": water},
    # trail expands LAST so the lane stays continuous over the causeway bed
    {"name": "t_path", "role": "terrain", "terrain": "trail",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
]

# ---- objects: the bell, lantern posts pacing the walk ------------------------
objects = [
    # THE MOOR-BELL SHRINE — the loop's earned landmark, top-centre of the
    # south platform (2x3 object; base row solid, crown renders above).
    {"id": "moorbell", "sprite": "pearlmoor_moorbell", "at": {"tx": 5, "ty": 21},
     "w": 2, "h": 3, "overhang": 1},
    # lantern posts (1x3, walk-under) pacing the legs — the lit lane convention
    {"id": "lamp_a", "sprite": "tinderwick_lamp_post", "at": {"tx": 7, "ty": 1},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_b", "sprite": "tinderwick_lamp_post", "at": {"tx": 3, "ty": 7},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # "the elbow lantern" (Maren's line) on the platform's seaward corner
    {"id": "lamp_c", "sprite": "tinderwick_lamp_post", "at": {"tx": 8, "ty": 8},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_d", "sprite": "tinderwick_lamp_post", "at": {"tx": 9, "ty": 13},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_e", "sprite": "tinderwick_lamp_post", "at": {"tx": 4, "ty": 16},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # the shrine's flanking lamps
    {"id": "lamp_f", "sprite": "tinderwick_lamp_post", "at": {"tx": 3, "ty": 21},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_g", "sprite": "tinderwick_lamp_post", "at": {"tx": 8, "ty": 21},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]
building_cells = {(x, y) for o in objects
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}

# ---- deco: boards, riprap chokes, buoys, signs --------------------------------
deco = mk.make_grid(W, H)
# worked boards (dock over SAND -> walkable) along the lane's straights
for (x, y) in [(5, 2), (6, 2), (5, 4), (6, 4), (7, 13), (8, 13), (7, 14),
               (5, 24), (6, 24)]:
    deco[y * W + x] = gid("dock")
# the entrance shoulders: only the lane columns open at the north edge
for (x, y) in [(4, 0), (7, 0)]:
    deco[y * W + x] = gid("boulder")
# CHOKE 1 (end of the north leg): only (5,7) passes — Maren faces up it
for (x, y) in [(4, 7), (6, 7), (7, 7)]:
    deco[y * W + x] = gid("boulder")
# CHOKE 2 (elbow -> east leg): only (7,12) passes — Cob faces up it
for (x, y) in [(6, 12), (8, 12), (9, 12)]:
    deco[y * W + x] = gid("boulder")
# riprap along the seaward edges (never choking a route)
for (x, y) in [(4, 4), (3, 10), (9, 16), (4, 19), (9, 22), (3, 25), (7, 26)]:
    deco[y * W + x] = gid("boulder")
# the harbour's buoy line drifting past the causeway
for (x, y) in [(1, 3), (10, 6), (0, 11), (11, 14), (1, 17), (10, 20), (2, 24), (10, 26)]:
    deco[y * W + x] = gid("buoy")

owed: list[str] = []

# ---- the two net-hand SIGHT trainers (mandatory crossings) --------------------
# Maren guards choke 1 from the elbow; Cob guards choke 2 from the east leg.
m_npcs: list[dict] = []
owed += pt.trainer_beat({"npcs": m_npcs}, tid="net_hand_a", at=(5, 10), facing="up",
                        sight=3, sprite="npc_woman")
owed += pt.trainer_beat({"npcs": m_npcs}, tid="net_hand_b", at=(7, 15), facing="up",
                        sight=3, sprite="npc_man")

# ---- caches (the standing kit; off the lane, on the seaward edges) ------------
cache_map = {"npcs": m_npcs}
owed += pt.cache(cache_map, cid="breakwater_balm", at=(3, 8))
owed += pt.cache(cache_map, cid="breakwater_charge", at=(9, 17))

# ---- signs ---------------------------------------------------------------------
sign_map: dict = {"triggers": []}
owed += pt.sign(sign_map, deco, W, sid="breakwater_mid", at=(8, 11))
owed += pt.sign(sign_map, deco, W, sid="moorbell_shrine", at=(7, 23))

# ---- assemble -------------------------------------------------------------------
m = {
    "id": "pearlmoor_breakwater", "display_name": "Pearlmoor Breakwater",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers +
              [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
               {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
    "objects": objects,
    "warps": [
        # Back through the moor-gate onto the quay's breakwater root, landing ON
        # its (gated) to_breakwater pair — the engine never auto-fires on arrival.
        {"id": "to_quay_w", "at": {"tx": 5, "ty": 0}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 24, "ty": 23}, "facing": "up",
         "transition": "fade"},
        {"id": "to_quay_e", "at": {"tx": 6, "ty": 0}, "trigger": "step_on",
         "to_map": "pearlmoor_quay", "to": {"tx": 25, "ty": 23}, "facing": "up",
         "transition": "fade"},
    ],
    "triggers": sign_map["triggers"] + [
        # THE MOOR-BELL — interact at the bell's base tiles; ringing it opens
        # the Tide-blessing (and Reyl's bond-test waits on this exact flag).
        {"id": "ring_moorbell_w", "kind": "cutscene", "at": {"tx": 5, "ty": 23},
         "activation": "interact", "ref": "script.ring_moorbell", "once": True,
         "sets_flags": ["flag:q_south_bell_rung"],
         "hidden_when_flag": "flag:q_south_bell_rung"},
        {"id": "ring_moorbell_e", "kind": "cutscene", "at": {"tx": 6, "ty": 23},
         "activation": "interact", "ref": "script.ring_moorbell", "once": True,
         "sets_flags": ["flag:q_south_bell_rung"],
         "hidden_when_flag": "flag:q_south_bell_rung"},
    ],
    # No encounters: the breakwater is a pure on-foot walk (no Tidecall content,
    # spine §0 rule 1) — its battles are the two posted net-hands.
    "encounters": [],
    "npcs": m_npcs,
    "gates": [],
    "music": "assets/audio/music/dimglass-coast-a.mp3",
}

if __name__ == "__main__":
    pt.report(owed)
    ok = mk.finalize(m, scale=3)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
