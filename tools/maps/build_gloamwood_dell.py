#!/usr/bin/env python3
"""
Gloamwood Dell (gloamwood_dell) — the home of the optional East side quest
"The Sunniest House in the Dark" (graph.ts `gloamwood_dell`, off lowleaf_hollow).

The darkest, deepest pocket of the hollow — and the cosiest. A tree-walled
glade where the green glow stops and Georgina, the Cat-keeper, has answered the
dark not with fear but with fairy-lights, glow-shrooms and a cottage full of
cats. A SAFE spur: no encounters, no trainers (the audit_flow free-pass/loop
WARNs are waived by design, the lanternway/gullcry precedent) — the reward is
the character, her dragon-cat, and the kitten she gifts you.

Layout: a single south path-mouth in from lowleaf_hollow (the `to_lowleaf`
return pair lands ON lowleaf's `to_gloamwood` tile), a lane up to Georgina's
cottage (the `lowleaf_cottage` art, door -> georgina_cottage), and a west nook
in the deepest dark where her bolted kitten Pim hides (the quest's fetch beat).

Wiring (graph.ts, both sides E): lowleaf_hollow `to_gloamwood` at (26,2) lands
HERE at (9,12); our `to_lowleaf` at (9,13) lands back ON (26,2) — the engine
never auto-fires a step_on warp on arrival, so landing on the source tile is
safe and within-1 for audit_warps.

Run:  ./venv/bin/python tools/maps/build_gloamwood_dell.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 18, 14
rng = random.Random(164)
owed: list[str] = []

# ---- terrain grids -----------------------------------------------------------------
tree = mk.make_grid(W, H)
path = mk.make_grid(W, H)

# the dark wood walls the dell on every side (deep organic border, §11)
mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                  bumps=[(4, 3, 2), (14, 4, 2), (3, 11, 2), (15, 10, 2)],
                  rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)   # the south treeline

# the south path-mouth (1-wide) — the way in from lowleaf
tree[12 * W + 9] = 0
tree[13 * W + 9] = 0

# the lane: up the centre from the mouth to the cottage door, a west spur to
# the kitten's dark nook
mk.vline(path, W, H, 9, 7, 12)        # the central lane
mk.hline(path, W, H, 7, 8, 9)         # connect the lane to the cottage apron
mk.hline(path, W, H, 10, 3, 9)        # the west spur to the kitten nook
mk.rect(path, W, H, 3, 9, 4, 10)      # the little nook clearing (SW dark corner)

# trees claim; the lane carves grass
for i in range(W * H):
    if tree[i]:
        path[i] = 0

terrain_layers = [
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
]

# ---- base + deco -------------------------------------------------------------------
gr = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gr) if rng.random() < 0.5 else gr[0] for _ in range(W * H)]

deco = mk.make_grid(W, H)
# Georgina's glow: shrooms strung through the dark like fairy-lights
for (x, y, n) in [(4, 8, "glowshroom_a"), (6, 9, "glowshroom_b"), (12, 8, "glowshroom_a"),
                  (13, 6, "glowshroom_b"), (11, 11, "glowshroom_a"), (5, 11, "glowshroom_b"),
                  (2, 9, "glowshroom_a"), (15, 8, "glowshroom_b")]:
    if deco[y * W + x] == 0 and not tree[y * W + x] and not path[y * W + x]:
        deco[y * W + x] = gid(n)

m: dict = {
    "id": "gloamwood_dell", "display_name": "Gloamwood Dell",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    # the spur reuses the parent area's loop (the reuse table; East forest theme)
    "music": "assets/audio/music/lowleaf-hollow-a.mp3",
}

# ---- Georgina's cottage (the lowleaf_cottage art; door -> georgina_cottage) ---------
# top-centre, backing onto the treeline; pt.building wires the door + carves the
# 2-row apron below it into `path` so the door sits in a glade, not a wall.
pt.building(m, path, W, H, oid="georgina_cottage", sprite="lowleaf_cottage",
            at=(6, 2), overhang=3, door_col=2,
            to_map="georgina_cottage", to=(8, 10))

# ---- the way back to lowleaf (the mutual pair; see module docstring) ----------------
m["warps"] += [
    {"id": "to_lowleaf", "at": {"tx": 9, "ty": 13}, "trigger": "step_on",
     "to_map": "lowleaf_hollow", "to": {"tx": 26, "ty": 2}, "facing": "down",
     "transition": "fade"},
]

# ---- the lost kitten Pim — the fetch beat, in the deepest dark of the nook ----------
# appears once Georgina has ASKED (q_east_georgina_met), gone once carried home.
m["npcs"] += [
    {"id": "lost_kitten", "at": {"tx": 3, "ty": 9}, "facing": "down",
     "sprite": "lost_kitten", "movement": "look_around",
     "dialogue_ref": "script.georgina_kitten_found",
     "requires_flag": "flag:q_east_georgina_met",
     "hidden_when_flag": "flag:q_east_georgina_kitten"},
]

# ---- the hand-lettered welcome sign by the path-mouth -------------------------------
owed += pt.sign(m, deco, W, sid="gloamwood_dell", at=(10, 11))

# ---- crown trees for depth inside the glade (§11 rule 2) ----------------------------
pt.crown_tree(m, oid="tree_a", sprite="tinderwick_tree", at=(2, 4))
pt.crown_tree(m, oid="tree_b", sprite="tinderwick_tree", at=(13, 9))
pt.crown_tree(m, oid="tree_c", sprite="tinderwick_tree", at=(14, 4))

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

building_cells = {(x, y) for o in m["objects"]
                  for y in range(o["at"]["ty"], o["at"]["ty"] + o.get("h", 1))
                  for x in range(o["at"]["tx"], o["at"]["tx"] + o.get("w", 1))}
mk.scatter_decor(deco, base, W, H, rng, density=0.10,
                 avoid=building_cells | {(x, y) for y in range(H) for x in range(W)
                                         if path[y * W + x] or tree[y * W + x]})

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
