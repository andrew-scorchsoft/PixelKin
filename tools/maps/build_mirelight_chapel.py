#!/usr/bin/env python3
"""
The Mirelights: the Drowned Chapel (09-the-wild-ways §2 B; kind route, region
east, bands 41-43). The causeway-village's bell-chapel, standing up to its door
in the mere, and the old sunk street that runs to it between two banks.

Three signature touches (level-design §8):
  1. OVER, THEN UNDER: you come off the Glassmere onto the high west bank and
     cross the sunk street on a timber TRESTLE (an underpass deck, `above`
     layer). From the deck you can SEE Tobin in the street's north end below
     you (§3a r3) — but there's no way down from the deck. You go on: the
     east bank, a LADDER down its cliff, the lower meadow, into the sunk street
     — and walk north along it UNDER the trestle you just crossed.
  2. TOBIN, found: alive, lost, sheepish (he followed the wrong lights and
     couldn't find the true boards back). He's pried at the chapel door and
     run from what's inside; finding him opens the quest's last door.
  3. THE CHAPEL: a 5x5 drowned bell-chapel on its own islet; its flooded porch
     has one board (a 1-tile plank span through the baked-in water row) up to
     the door, which leads down into LANTHORNE HOLLOW (the null-lantern).

Plus the sympathetic acolyte posted at the ladder's foot (the Hollowing tend
the sleeping light; they don't guard it with cruelty) whose camp on the east
bank is the Mirelights' rest point.

HANDSHAKE: west `to_glassmere`/`_s` (0,9)/(0,10) <-> mirelight_glassmere
(29,9)/(29,10); the chapel door (14,37) <-> lanthorne_hollow (9,11) (portal).
Geometry: x 119..149, y -116..-72.

Run:  python3 tools/maps/build_mirelight_chapel.py
"""
from __future__ import annotations

import random

import mapkit as mk
import mirelight_common as mc
import patterns as pt
import wildkit as wk
from mapkit import gid

W, H = 30, 44
rng = random.Random(16503)
owed: list[str] = []

tree = mk.make_grid(W, H)
cliff = mk.make_grid(W, H)
pond = mk.make_grid(W, H)
grass = mk.make_grid(W, H)
path = mk.make_grid(W, H)
street = mk.make_grid(W, H)     # the sunk street (ruinfloor)
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)

# ---- the enclosure ------------------------------------------------------------------
mk.organic_border(tree, W, H, top=1, right=1, depth=3,
                  bumps=[(6, 3, 1), (22, 3, 2), (28, 16, 2), (28, 34, 2)], rng=rng)
mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)
for y in range(2, H - 2):
    if y not in (9, 10):
        tree[y * W + 0] = 1
# the west bank's top ends at the Glassmere entry: wood above it
mk.blob(tree, W, H, 3.0, 4.0, 3.0, 1.6)

# ---- the banks and the sunk street ------------------------------------------------------
STREET_X = (13, 15)
mk.rect(cliff, W, H, 11, 3, 12, 18)          # the west bank's east wall
mk.rect(cliff, W, H, 16, 3, 17, 24)          # the east bank's west wall
mk.rect(cliff, W, H, 0, 17, 12, 18)          # the west bank's south drop (no way down)
mk.rect(cliff, W, H, 16, 23, W - 1, 24)      # the east bank's south drop (the ladder)
for y in range(3, 34):
    for x in range(STREET_X[0], STREET_X[1] + 1):
        street[y * W + x] = 1
        tree[y * W + x] = 0
for y in range(0, 3):                        # the street runs on north into the wood
    for x in range(STREET_X[0], STREET_X[1] + 1):
        tree[y * W + x] = 1

# ---- the lower meadow + the chapel's islet ----------------------------------------------
mk.blob(pond, W, H, 14.0, 35.5, 6.4, 3.6)     # the mere round the chapel
mk.blob(pond, W, H, 22.5, 33.0, 5.2, 4.6)
mk.rect(pond, W, H, 17, 26, 27, 29)            # the moat under the ladder shelf
mk.rect(tree, W, H, 28, 25, W - 1, H - 1)       # the wood closes the east side
mk.blob(pond, W, H, 4.2, 21.6, 2.9, 1.6)
mk.blob(pond, W, H, 6.6, 22.8, 1.8, 1.2)
CHAPEL = (12, 33)                             # 5x5: door col 2 row 3, porch row 4
for y in range(CHAPEL[1], CHAPEL[1] + 5):
    for x in range(CHAPEL[0], CHAPEL[0] + 5):
        pond[y * W + x] = 0

LANE = set()


def lane(x0, y0, x1, y1):
    for y in range(min(y0, y1), max(y0, y1) + 1):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            LANE.add((x, y))


lane(0, 9, 10, 10)          # off the Glassmere onto the west bank
lane(18, 9, 22, 10)         # off the trestle onto the east bank
lane(22, 10, 22, 22)        # down the east bank to the ladder head
lane(22, 22, 24, 22)
lane(16, 25, 24, 25)        # the ladder shelf (one row: the acolyte's eye)
lane(8, 30, 14, 30)         # the street's mouth round the islet's west side
lane(8, 30, 8, 40)
lane(8, 40, 14, 40)
lane(14, 39, 14, 40)        # up to the chapel porch
lane(13, 38, 15, 38)        # the porch apron
for (x, y) in LANE:
    path[y * W + x] = 1
    pond[y * W + x] = 0
    tree[y * W + x] = 0
# the street's mouth at the bottom joins the lower meadow (rows 25-33)
for y in range(25, 34):
    for x in range(STREET_X[0], STREET_X[1] + 1):
        pond[y * W + x] = 0

# reed beds: the east bank's, the meadow's, and the street's full-width band
mk.blob(grass, W, H, 25.0, 6.5, 2.6, 2.0)
mk.blob(grass, W, H, 25.5, 17.0, 2.4, 2.2)
mk.blob(grass, W, H, 5.0, 27.5, 3.2, 2.0)
mk.blob(grass, W, H, 4.0, 36.0, 2.4, 2.4)
for y in (20, 21):
    for x in range(STREET_X[0], STREET_X[1] + 1):
        grass[y * W + x] = 1
        street[y * W + x] = 0
mk.blob(grass, W, H, 6.0, 12.0, 2.4, 1.6)
for i in range(W * H):
    if tree[i] or cliff[i]:
        pond[i] = grass[i] = path[i] = street[i] = 0
    if pond[i] or path[i]:
        grass[i] = 0
    if pond[i]:
        street[i] = 0

m: dict = {
    "id": "mirelight_chapel", "display_name": "The Drowned Chapel",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/mirelight.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/mirelight-a.webp",
                         "assets/backgrounds/battle/mirelight-b.webp"],
    "ambience": {**mc.MIRE_AMB, "bob_gids": [gid("buoy")]},
}
wk.use_traverse(m)
obj = lambda *a, **k: mc.obj(m, *a, **k)  # noqa: E731

# ---- 1. the trestle (over) + the ladder (round and down) -------------------------------
wk.deck(m, above, W, rect=(11, 9, 7, 2), axis="h", sid="chapel_trestle", under=True,
        shade=deco)
wk.ladder(m, deco, W, x=24, y0=23, y1=24, sid="chapel_ladder")

# ---- warps --------------------------------------------------------------------------
for i, y in enumerate((9, 10)):
    m["warps"].append({"id": "to_glassmere" + ("_s" if i else ""), "at": {"tx": 0, "ty": y},
                       "trigger": "step_on", "to_map": "mirelight_glassmere",
                       "to": {"tx": 29, "ty": y}, "facing": "left", "transition": "fade"})
# ---- 3. the chapel: its porch board + the door down to the null-lantern ------------------
cx, cy = CHAPEL
obj("chapel", "mirelight_drowned_chapel", CHAPEL, 5, 5, overhang=2)
# The door's own tile is the art's row 3, but row 4 (the flooded porch, baked into
# the sprite) stands between it and the islet — so the walk-onto door warp sits ON
# the porch step at the door's foot (the engine frees it; the audits want a landing
# within one tile of the return, and a span inside a solid footprint confuses them).
door = (cx + 2, cy + 4)
m["warps"].append({"id": "to_hollow", "at": {"tx": door[0], "ty": door[1]},
                   "trigger": "step_on", "to_map": "lanthorne_hollow",
                   "to": {"tx": 9, "ty": 11}, "facing": "up", "transition": "door",
                   "requires_flag": "flag:mirelight_tobin_found",
                   "blocked_ref": "npc.mirelight_chapel_door"})
owed.append("npc.mirelight_chapel_door")
m["triggers"].append({"id": "chapel_bell", "kind": "script", "at": {"tx": cx + 3, "ty": cy + 4},
                      "activation": "interact", "ref": "script.mirelight_chapel_bell"})
owed.append("script.mirelight_chapel_bell")

# ---- 2. Tobin, in the street's north end (seen from the trestle) ------------------------
m["npcs"].append({"id": "tobin", "at": {"tx": 14, "ty": 5}, "facing": "down",
                  "sprite": "village_child", "movement": "look_around",
                  "dialogue_ref": "script.mirelight_tobin",
                  "hidden_when_flag": "flag:mirelight_tobin_found"})
owed.append("script.mirelight_tobin")
obj("tobin_lamp", "coldfog_doused_lamp", (15, 3), 1, 3, overhang=2, walk_under=True)
owed += pt.cache(m, cid="mire_street_tin", at=(13, 3))

# ---- the acolyte at the ladder's foot + his camp (the rest point) ------------------------
owed += pt.trainer_beat(m, tid="mire_acolyte", at=(16, 26), facing="up", sight=1,
                        sprite="hollowing_acolyte")
obj("acolyte_camp", "coldfog_quiet_camp", (19, 13), 3, 2)
m["triggers"].append({"id": "acolyte_camp_rest", "kind": "cutscene", "at": {"tx": 20, "ty": 15},
                      "activation": "interact", "ref": "script.mirelight_camp_rest"})
owed.append("script.mirelight_camp_rest")

# ---- dressing ----------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="mirelight_chapel", at=(7, 8))
owed += pt.cache(m, cid="mire_meadow_charge", at=(2, 39))
owed += pt.cache(m, cid="mire_bank_balm", at=(2, 15))       # the west bank's far corner pays
obj("south_stooks", "saltreach_reed_stooks", (19, 40), 2, 2, overhang=1, walk_under=True)
obj("south_traps", "saltreach_eel_trap", (24, 40), 2, 2, overhang=1, walk_under=True, solid=False)
obj("south_moorings", "saltreach_mooring_posts", (5, 40), 1, 2, overhang=1, walk_under=True)
obj("south_lamp", "coldfog_doused_lamp", (11, 38), 1, 3, overhang=2, walk_under=True)
pt.crown_tree(m, oid="willow_w", sprite="coldfog_dead_willow", at=(3, 12))
pt.crown_tree(m, oid="willow_e", sprite="coldfog_dead_willow", at=(25, 9))
pt.crown_tree(m, oid="tree_m", sprite="tinderwick_tree_c", at=(1, 30))
pt.crown_tree(m, oid="tree_e", sprite="tinderwick_tree_b", at=(19, 18))
for k, (x, y) in enumerate([(20, 31), (24, 35), (18, 38), (10, 34), (26, 30), (21, 27), (5, 21)]):
    obj(f"will_light_{k}", "mirelight_marsh_light", (x, y), 1, 1, solid=False)
obj("drowned_lamp_a", "saltreach_sunken_lamp", (17, 32), 1, 3, overhang=2, walk_under=True, solid=False)
obj("drowned_lamp_b", "saltreach_sunken_lamp", (11, 36), 1, 3, overhang=2, walk_under=True, solid=False)
obj("drowned_lamp_c", "saltreach_sunken_lamp", (25, 36), 1, 3, overhang=2, walk_under=True, solid=False)
obj("reeds_a", "saltreach_cattails", (9, 32), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_b", "saltreach_cattails", (19, 35), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_c", "saltreach_cattails", (27, 20), 2, 2, overhang=1, walk_under=True, solid=False)
obj("reeds_d", "saltreach_cattails", (4, 6), 2, 2, overhang=1, walk_under=True, solid=False)
obj("lily_a", "saltreach_lilypads", (22, 30), 2, 2, solid=False)
obj("lily_b", "saltreach_lilypads", (15, 38), 2, 2, solid=False)
obj("street_stooks", "saltreach_reed_stooks", (13, 14), 2, 2, overhang=1, walk_under=True)
obj("bank_stooks", "saltreach_reed_stooks", (8, 4), 2, 2, overhang=1, walk_under=True)
obj("bank_lamp", "saltreach_reed_lantern_lit", (10, 7), 1, 2, overhang=1, walk_under=True)
obj("east_lamp", "saltreach_reed_lantern_lit", (18, 7), 1, 2, overhang=1, walk_under=True)
obj("meadow_cart", "coldfog_beached_boat", (3, 33), 3, 2)
for (x, y) in [(6, 15), (26, 13), (20, 4), (2, 25), (10, 26), (27, 26)]:
    i = y * W + x
    if not (path[i] or pond[i] or tree[i] or grass[i] or cliff[i] or street[i]):
        deco[i] = gid("boulder")
m["npcs"].append({"id": "amb_lumplass", "at": {"tx": 5, "ty": 24}, "facing": "down",
                  "sprite": "kin_32_overworld", "movement": "wander", "ambient": True,
                  "wander_radius": 1})

mc.zones(m, grass, W, H, prefix="chapel", night=mc.CHAPEL_NIGHT, day=mc.CHAPEL_DAY)

gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_ruinfloor", "role": "terrain", "terrain": "ruinfloor",
     "set": "vesper_overworld_set", "depth": 0, "data": street},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": grass},
    {"name": "t_pond", "role": "terrain", "terrain": "pond",
     "set": "vesper_overworld_set", "depth": 0, "data": pond},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": above},
]
WALK = {(x, y) for y in range(H) for x in range(W)
        if not (tree[y * W + x] or pond[y * W + x] or cliff[y * W + x])}
mc.deep_layer(m, pond, WALK, W, H)

covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (tree, path, grass, pond, deco, cliff, street))}
objcells = {(x, y) for o in m["objects"]
            for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
            for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
busy = {(n["at"]["tx"], n["at"]["ty"]) for n in m["npcs"]} | \
       {(t["at"]["tx"], t["at"]["ty"]) for t in m["triggers"]}
mk.scatter_decor(deco, base, W, H, rng, density=0.12, flowers=0.03,
                 avoid=covered | objcells | busy | LANE)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
