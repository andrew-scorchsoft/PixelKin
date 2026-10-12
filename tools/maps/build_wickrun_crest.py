#!/usr/bin/env python3
"""
The Wick-Run Crest — the top station of the old wax road (09-the-wild-ways §2 A;
kind route, region west, NO encounters — it's a station, not a road).

Before the Long Dusk the Sunvault chandleries rendered sun-vine tallow up here
and ran the wax DOWN the mountain on carts to Pearlmoor's quays; the empties came
back up on the Tallow Lift. The vines shut, the vats cooled, the lift's brake was
chained at this end. Now the Runners race the chute on rented runner-wheels.

Three signature touches (§8):
  1. THE TALLOW LIFT's top house (east): reaching it frees the brake
     (`flag:tallow_lift_freed`) — from then on the lift runs both ways, and
     the foot station far below (closed to anyone who came from the bottom)
     opens. The see-it-early / opened-from-above promise.
  2. THE RENTAL (centre): Pell the wheelwright rents runners (300w; free once
     you hold the Runner's Ribbon). No runner, no run: the start-gate lane
     south is gated on `flag:wickrun_riding`.
  3. THE CHANDLERY'S cold hearth (west): a rest point — the last warm fire
     before a long way down.

HANDSHAKE: north `to_sunvault`/`_e` (14,0)/(15,0) <-> sunvault_climb_i's south
`to_wickrun`/`_e` (14,25)/(15,25); south `to_chute`/`_e` (10,27)/(11,27) ->
wickrun_chute (13,0)/(14,0); its `to_crest`/`_e` land here ON (10,27)/(11,27).
Geometry (docs/world/geometry.md): placed at x -5..25, y -266..-238.

Run:  python3 tools/maps/build_wickrun_crest.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 30, 28
rng = random.Random(9061)
owed: list[str] = []

tree = mk.make_grid(W, H)
cliff = mk.make_grid(W, H)
path = mk.make_grid(W, H)
gold = mk.make_grid(W, H)
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)

# The enclosure: the Sunvault's rock wall north (its stair comes down through a
# notch), the wooded flanks, and the DROP south — the mountain falls away below
# the start gate, so the south edge is cliff with the one lane cut through it.
mk.rect(cliff, W, H, 0, 0, W - 1, 1)
mk.organic_border(tree, W, H, left=1, right=1, depth=2,
                  bumps=[(1, 6, 2), (28, 4, 1), (1, 17, 2), (28, 18, 2)], rng=rng)
for y in (19, 20):                          # the lip + its face...
    mk.hline(cliff, W, H, y, 0, W - 1)
for y in range(21, H):                      # ...and the forest far below
    mk.hline(tree, W, H, y, 0, W - 1)
for x in (14, 15):                         # the notch from the Sunvault
    cliff[0 * W + x] = cliff[1 * W + x] = 0
for y in range(19, H):                      # the start lane through the drop
    for x in (9, 10, 11, 12):
        cliff[y * W + x] = 0
        tree[y * W + x] = 0
for y in range(20, H):
    for x in (9, 12):
        tree[y * W + x] = 1                 # pines hem the lane as it drops

# Gold sun-garden grass on the high shelf (the Sunvault's register).
mk.blob(gold, W, H, 6.0, 12.0, 3.4, 2.4)
mk.blob(gold, W, H, 22.0, 15.5, 3.0, 2.0)

LANE: set[tuple[int, int]] = set()
for y in range(0, 10):
    LANE |= {(14, y), (15, y)}             # down from the notch
for x in range(6, 25):
    LANE |= {(x, 10), (x, 11)}             # the plaza road
for y in range(10, 14):
    LANE |= {(22, y), (23, y)}             # to the lift house
for y in range(10, 18):
    LANE |= {(10, y), (11, y)}             # to the start gate
LANE |= {(x, y) for y in (16, 17) for x in range(6, 18)}   # the start apron
for y in range(18, H):
    LANE |= {(10, y), (11, y)}             # the start lane
for (x, y) in LANE:
    path[y * W + x] = 1
for i in range(W * H):
    if path[i] or tree[i] or cliff[i]:
        gold[i] = 0
    if tree[i] or cliff[i]:
        path[i] = 0

m: dict = {
    "id": "wickrun_crest", "display_name": "Wick-Run Crest",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/wickrun.mp3",
    "ride": True,
}
wk.use_traverse(m)
pin: dict = {}


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


# ---- warps ------------------------------------------------------------------
for i, x in enumerate((14, 15)):
    m["warps"].append({"id": "to_sunvault" + ("_e" if i else ""), "at": {"tx": x, "ty": 0},
                       "trigger": "step_on", "to_map": "sunvault_climb_i",
                       "to": {"tx": x, "ty": 25}, "facing": "up", "transition": "fade"})
for i, x in enumerate((10, 11)):
    m["warps"].append({"id": "to_chute" + ("_e" if i else ""), "at": {"tx": x, "ty": H - 1},
                       "trigger": "step_on", "to_map": "wickrun_chute",
                       "to": {"tx": x + 3, "ty": 0}, "facing": "down", "transition": "fade",
                       "requires_flag": "flag:wickrun_riding",
                       "blocked_ref": "npc.wickrun_gate_blocked"})
owed.append("npc.wickrun_gate_blocked")

# ---- 1. the Tallow Lift's top house (east) ----------------------------------
# (the lift house: 4x4, a solid building; you work the brake from its front)
LX, LY = 21, 10
obj("lift_top", "wickrun_lift_house_top", (LX, LY), 4, 4, overhang=2)
for tx in range(LX, LX + 4):
    m["triggers"].append({"id": f"lift_top_{tx}", "kind": "cutscene",
                          "at": {"tx": tx, "ty": LY + 3}, "activation": "interact",
                          "ref": "script.tallow_lift_top"})
owed.append("script.tallow_lift_top")
LANE |= {(x, LY + 4) for x in range(LX, LX + 4)}
for x in range(LX, LX + 4):
    path[(LY + 4) * W + x] = 1
    tree[(LY + 4) * W + x] = 0
obj("lift_lamp", "tinderwick_lamp_post", (26, 11), 1, 3, overhang=2, walk_under=True)
obj("lift_pylon", "wickrun_lift_pylon", (26, 5), 1, 4, overhang=3, walk_under=True)

# ---- 2. the rental ----------------------------------------------------------
obj("runner_rack", "wickrun_runner_rack", (12, 13), 2, 2)
m["npcs"].append({"id": "pell", "at": {"tx": 15, "ty": 14}, "facing": "down",
                  "sprite": "npc_man", "movement": "static",
                  "dialogue_ref": "script.wickrun_rental"})
owed.append("script.wickrun_rental")
m["npcs"].append({"id": "runner_kid", "at": {"tx": 18, "ty": 16}, "facing": "left",
                  "sprite": "npc_boy", "movement": "wander", "wander_radius": 2,
                  "dialogue_ref": "npc.wickrun_runner_kid"})
owed.append("npc.wickrun_runner_kid")

# ---- 3. the chandlery ruin + its cold hearth (a rest point) ------------------
obj("chandlery", "wickrun_chandlery_ruin", (2, 3), 5, 4, overhang=2)
obj("chandlery_hearth", "solarium_brazier_lit", (8, 7), 2, 3, overhang=1)
m["triggers"].append({"id": "chandlery_rest", "kind": "cutscene", "at": {"tx": 8, "ty": 9},
                      "activation": "interact", "ref": "script.wickrun_crest_rest"})
owed.append("script.wickrun_crest_rest")
obj("wax_barrels", "wickrun_wax_barrels", (4, 8), 2, 1)
obj("wax_pile", "tinderwick_woodpile", (2, 13), 2, 1)

# ---- the start gate + the view down ------------------------------------------
owed += pt.sign(m, deco, W, sid="wickrun_crest", at=(13, 16))
obj("start_lamp_w", "tinderwick_lamp_post", (8, 17), 1, 3, overhang=2, walk_under=True)
obj("start_lamp_e", "tinderwick_lamp_post", (13, 17), 1, 3, overhang=2, walk_under=True)
for x in (10, 11):
    deco[18 * W + x] = wk.T("chev_down")
# the start gate's arch over the lane (decor: its posts stand in the pines)
obj("start_gate", "wickrun_start_gate", (9, 19), 3, 2, overhang=1, solid=False)
obj("crest_tree_a", "tinderwick_tree_c", (24, 2), 3, 4, overhang=3, walk_under=True)
obj("crest_tree_b", "tinderwick_tree_b", (3, 15), 3, 4, overhang=3, walk_under=True)
obj("crest_pine", "windward_bent_pine", (25, 15), 2, 3, overhang=2, walk_under=True)
for (x, y) in [(19, 3), (6, 2), (27, 8), (20, 17), (4, 11)]:
    if not path[y * W + x]:
        deco[y * W + x] = gid("boulder")

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
golds = [gid(f"goldgrass{i}") for i in range(4)]
for i in range(W * H):
    if gold[i]:
        base[i] = rng.choice(golds)          # gold sun-garden grass is a fill, not a family
m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": above},
]

covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (tree, cliff, path, deco))}
cells = {(x, y) for o in m["objects"]
         for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
         for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.10, avoid=covered | cells | busy | LANE)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3, pin_base=pin)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
