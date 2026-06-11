#!/usr/bin/env python3
"""
Galehigh Terraces — the North's cliff-farm town + route (walkthrough/03-north;
Lumenary 5: Mira Vael, Storm — the bond-test itself waits at the SKYLOFT launch
ledge, never in town).

Arc D: the FIRST COLOUR in screens — you step out of Cinderhead's ink-black
gallery onto stepped cliff-farms catching the last fire-orange sunset; the
Kite-rising festival is in full swing. Three signature touches (§8):
  1. THE GREAT WINCH on the festival terrace — the earned-loop centrepiece
     (spine §5 shape #5): idle until the town blesses your kite, then it hauls
     you up to `galehigh_skyloft`;
  2. STEPPED TERRACES — three elevation bands (lower town -> festival -> upper
     route) joined by switchback gaps, hopped back down by one-way ledges; the
     snowLINE creeps over the top band (snowpatch + snowtrail lane +
     glacierwall crags — Galehigh is where the North's snow register starts);
  3. KITES EVERYWHERE — the bespoke galehigh object set (wind-break cottages,
     kite-maker's workshop, kite poles, wind-bent crops, pulley baskets).

The earned loop — "The Kite-Rising Winch" (§5 shape #5, NEVER Updraft-gated,
spine §0 rule 1): script.mira_quest (the entry band — Mira shouts the hook
down) -> flag:q_north_kite; the kite-maker's three chained caches
flag:picked_kite_a/b/c (each pick reveals the next) -> script.kite_built ->
flag:q_north_kite_ready; the winch-keeper flies it with the town
(script.galehigh_kite_rising, the festival cutscene) ->
flag:q_north_kite_blessed; the winch warp `to_skyloft` consumes that flag.

Updraft Kite is the REWARD, not the gate: the high NE terrace (the Wind-Eye
mouth `to_windeye`, the ledge-herb cache for N1 "The Crag-tender's Kettle",
a hidden valuable) sits behind an updraft AbilityGate — optional only, signed.

Wires to: cinderhead_deep `to_terraces` lands {1,14}/{1,15} (our return warps
to_cinderhead at {0,14}/{0,15} -> deep {26,12}/{26,13}); `to_stair` north
(windward_stair_i — N2 authors the far side; its return pair must land at our
(14,1)/(15,1)); `to_crossroads` south (the Lanternway spoke, lands crossroads
{1,3}/{1,4}); `shortcut_galehigh` (Windward II's late drop) should land on the
upper route around (18..21, 3) — N2's builder owns that warp's far half.

Suggested sign copy (the wiring agent writes dialogue.ts; humour sheet: signs
are this town's ONE wry line, dry and warm — sign.galehigh_winch carries it):
  sign.galehigh_welcome    "GALEHIGH TERRACES — the last fire before the
                            climb. Mind the gusts."
  sign.galehigh_winch      "KITE-RISING WINCH. Riders ascend at their own joy.
                            The Festival Committee asks that you wave back."
  sign.galehigh_high_ledges "The high terraces only open to a kin that rides
                            the thermals." (the Updraft tease — sincere)
  sign.galehigh_windeye    "The Wind-Eye. On a clear dusk the updraft column
                            sings." (the [MISSABLE] landmark callout — sincere)
  sign.galehigh_lanternway "LANTERNWAY — south to Vesper Crossroads."

Run:  ./venv/bin/python tools/maps/build_galehigh_terraces.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 32, 32
rng = random.Random(53)
owed: list[str] = []

# ---- terrain presence grids ------------------------------------------------------
glacier = mk.make_grid(W, H)    # high crag walls + the high-terrace rims (snow context)
cliff = mk.make_grid(W, H)      # terrace banks in the grass register
tree = mk.make_grid(W, H)       # the lower valley's wooded enclosure (S + lower E)
snowpatch = mk.make_grid(W, H)  # the snowline creeping over the top band
snowtrail = mk.make_grid(W, H)  # the trodden lane where it crosses the snow
tallgrass = mk.make_grid(W, H)  # encounter verges + the mandatory upper band
path = mk.make_grid(W, H)       # the lit lanes

# TOP BORDER: glacier crag wall, 2 deep, the exit gap to Windward at cols 14-15
mk.rect(glacier, W, H, 0, 0, W - 1, 1)
for y in (0, 1):
    glacier[y * W + 14] = 0
    glacier[y * W + 15] = 0
# EAST CRAG behind the high terrace
mk.rect(glacier, W, H, 30, 0, 31, 11)
# HIGH NE TERRACE rims (glacier — it sits in the snowline): west rim with the
# thermal-column gap (covered by the updraft AbilityGate), south rim over the
# festival terrace. Interior x25..29, y2..9.
mk.rect(glacier, W, H, 23, 2, 24, 11)
for y in (5, 6):
    glacier[y * W + 23] = 0
    glacier[y * W + 24] = 0
mk.rect(glacier, W, H, 23, 10, 29, 11)

# the SNOWLINE: the whole top band + the high terrace, organic southern edge
mk.rect(snowpatch, W, H, 0, 0, W - 1, 4)
mk.rect(snowpatch, W, H, 23, 0, 31, 11)
for (bx, by, brx, bry) in [(4, 5, 1.5, 1.0), (10, 5, 1.2, 0.8), (19, 5, 1.5, 1.0)]:
    mk.blob(snowpatch, W, H, bx, by, brx, bry)

# WEST BORDER: the mountain face, entry gap from Cinderhead Deep at rows 14-15
mk.rect(cliff, W, H, 0, 2, 1, H - 1)
for y in (14, 15):
    cliff[y * W + 0] = 0
    cliff[y * W + 1] = 0

# MID BANK: upper route (rows 2-9) over the festival terrace (rows 12-20)
mk.rect(cliff, W, H, 0, 10, 22, 11)
for x in (14, 15):                                  # the switchback gap
    cliff[10 * W + x] = 0
    cliff[11 * W + x] = 0
for x in (16, 17, 18):                              # the one-way ledge segment
    cliff[10 * W + x] = 0
    cliff[11 * W + x] = 0

# ENTRY THROAT: a narrow cliff canyon in from the deep (rows 14-15 only), so
# the mira_quest band at x=4 is a true choke (band the WHOLE walkable cut)
mk.rect(cliff, W, H, 2, 12, 5, 13)
mk.rect(cliff, W, H, 2, 16, 5, 20)

# LOWER BANK: festival terrace over the lower town (rows 23-28)
mk.rect(cliff, W, H, 0, 21, W - 1, 22)
for x in (15, 16):                                  # the lane gap down to town
    cliff[21 * W + x] = 0
    cliff[22 * W + x] = 0
for x in (18, 19, 20):                              # the one-way ledge segment
    cliff[21 * W + x] = 0
    cliff[22 * W + x] = 0

# BOTTOM + LOWER-EAST BORDER: the wooded valley side, organic
mk.rect(tree, W, H, 0, 29, W - 1, H - 1)
mk.rect(tree, W, H, 30, 12, 31, H - 1)
mk.organic_border(tree, W, H, depth=0,
                  bumps=[(3, 29, 2), (9, 30, 2), (22, 30, 2), (29, 29, 2),
                         (30, 15, 2)], rng=rng)
for y in (29, 30, 31):                              # the Lanternway road gap south
    tree[y * W + 15] = 0
    tree[y * W + 16] = 0

# ---- lanes -----------------------------------------------------------------------
mk.hline(path, W, H, 14, 1, 5)                      # the entry throat lane
mk.hline(path, W, H, 15, 1, 5)
mk.rect(path, W, H, 8, 18, 19, 19)                  # the lumenary/winch front street
mk.rect(path, W, H, 13, 13, 19, 17)                 # the festival square
mk.rect(path, W, H, 20, 18, 22, 18)                 # the winch platform
mk.vline(path, W, H, 14, 5, 12)                     # the upper switchback (grass leg)
mk.vline(path, W, H, 15, 5, 12)
mk.vline(snowtrail, W, H, 14, 0, 4)                 # the lane where it crosses snow
mk.vline(snowtrail, W, H, 15, 0, 4)
mk.vline(path, W, H, 15, 19, 28)                    # the lane down to the lower town
mk.vline(path, W, H, 16, 19, 28)
mk.hline(path, W, H, 27, 7, 23)                     # lower town street (north row)
mk.hline(path, W, H, 28, 3, 28)                     # lower town street (south row)
mk.vline(path, W, H, 15, 28, H - 1)                 # the Lanternway south
mk.vline(path, W, H, 16, 28, H - 1)

# ---- encounter terrain -----------------------------------------------------------
# lower-terrace verges (the kite-cache ground, band 28-30) — optional patches
mk.blob(tallgrass, W, H, 8, 25, 1.4, 1.5)
mk.blob(tallgrass, W, H, 19, 25, 1.8, 1.5)
# the MANDATORY upper crossing (§11 rule 7): full-corridor band rows 5-6, the
# lane paused through it — the climb to Windward itself rolls encounters
pt.mandatory_band(tallgrass, path, W, H, y0=5, y1=6, x0=2, x1=22)

# ---- precedence (one family per cell; structure wins over ground) ------------------
for i in range(W * H):
    if cliff[i] and tree[i]:
        tree[i] = 0
    if glacier[i]:
        snowpatch[i] = 0
    if tallgrass[i] and (cliff[i] or glacier[i] or tree[i] or snowpatch[i]):
        tallgrass[i] = 0
    if path[i] and (cliff[i] or glacier[i] or tree[i]):
        path[i] = 0
    if snowtrail[i] and glacier[i]:
        snowtrail[i] = 0
    if snowpatch[i] and (path[i] or snowtrail[i]):
        snowpatch[i] = 0

# ---- base ------------------------------------------------------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
# the scree shelf on the upper route's west pocket ("scree on the high ledges")
for sy in range(7, 10):
    for sx in range(3, 8):
        i = sy * W + sx
        if not (cliff[i] or tallgrass[i] or path[i] or snowpatch[i]):
            base[i] = gid(f"scree{rng.randrange(3)}")

terrain_layers = [
    {"name": "t_snowpatch", "role": "terrain", "terrain": "snowpatch",
     "set": "vesper_overworld_set", "depth": 0, "data": snowpatch},
    {"name": "t_snowtrail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": snowtrail},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
]

# ---- the map skeleton (stamps append into it) -------------------------------------
m: dict = {
    "id": "galehigh_terraces", "display_name": "Galehigh Terraces",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "town",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [
        # the thermal column up to the high terrace — Updraft Kite force-gates
        # the rim gap (optional shelf only; never the main path — §0 rule 1)
        {"id": "high_terrace_thermal", "ability": "updraft_kite",
         "rect": {"tx": 23, "ty": 5, "w": 2, "h": 2}, "effect": "make_passable"},
    ],
    "music": "assets/audio/music/galehigh-terraces-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/galehigh-terraces-a.webp",
        "assets/backgrounds/battle/galehigh-terraces-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- buildings (the bespoke galehigh object set; doors are walk-onto) --------------
# Mira's Storm hall on the festival terrace (the arch straddles cols 2-3)
pt.building(m, path, W, H, oid="lumenary", sprite="galehigh_lumenary",
            at=(7, 12), overhang=3, door_col=2,
            to_map="galehigh_lumenary", to=(8, 11))
m["warps"][-1].update({"id": "to_lumenary", "requires_flag": "flag:has_starter",
                       "blocked_ref": "door.locked_lumenary"})
m["warps"].append({"id": "to_lumenary_e", "at": {"tx": 10, "ty": 17},
                   "trigger": "step_on", "to_map": "galehigh_lumenary",
                   "to": {"tx": 8, "ty": 11}, "facing": "up",
                   "requires_flag": "flag:has_starter",
                   "blocked_ref": "door.locked_lumenary", "transition": "door"})

# lower town: the inn (rest point), the kite-maker's workshop, a home
pt.building(m, path, W, H, oid="inn", sprite="galehigh_inn",
            at=(2, 23), overhang=2, door_col=2,
            to_map="galehigh_inn", to=(7, 10))
m["warps"][-1]["id"] = "to_inn"
pt.building(m, path, W, H, oid="kitemaker", sprite="galehigh_shop",
            at=(10, 23), overhang=1, door_col=3,
            to_map="galehigh_kitemaker", to=(7, 9))
m["warps"][-1]["id"] = "to_shop"
pt.building(m, path, W, H, oid="home", sprite="galehigh_cottage",
            at=(24, 23), overhang=2, door_col=2,
            to_map="galehigh_home", to=(6, 8))
m["warps"][-1]["id"] = "to_home"

# THE GREAT WINCH on the festival terrace; the platform below it carries the
# festival-flag-gated warp up to the skyloft
m["objects"].append({"id": "great_winch", "sprite": "galehigh_winch",
                     "at": {"tx": 20, "ty": 13}, "w": 4, "h": 5,
                     "overhang": 3, "walk_under": True})

# kite decor, terrace-farm props, lamps, crown trees
m["objects"] += [
    {"id": "kite_plaza_w", "sprite": "galehigh_kite_pole_a", "at": {"tx": 13, "ty": 13},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "kite_plaza_e", "sprite": "galehigh_kite_pole_b", "at": {"tx": 17, "ty": 13},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "kite_town", "sprite": "galehigh_kite_pole_b", "at": {"tx": 18, "ty": 23},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "kite_upper", "sprite": "galehigh_kite_pole_a", "at": {"tx": 18, "ty": 2},
     "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    # the farm shelf on the festival terrace's east pocket
    {"id": "basket_a", "sprite": "galehigh_pulley_basket", "at": {"tx": 24, "ty": 13},
     "w": 2, "h": 2, "overhang": 0},
    {"id": "crops_a", "sprite": "galehigh_crop_rows", "at": {"tx": 27, "ty": 13},
     "w": 2, "h": 2, "overhang": 0},
    {"id": "crops_b", "sprite": "galehigh_crop_rows", "at": {"tx": 24, "ty": 15},
     "w": 2, "h": 2, "overhang": 0},
    {"id": "crops_c", "sprite": "galehigh_crop_rows", "at": {"tx": 10, "ty": 8},
     "w": 2, "h": 2, "overhang": 0},
    {"id": "basket_b", "sprite": "galehigh_pulley_basket", "at": {"tx": 26, "ty": 17},
     "w": 2, "h": 2, "overhang": 0},
    # lamp posts beside (never on) the lit lanes
    {"id": "lamp_switchback", "sprite": "tinderwick_lamp_post", "at": {"tx": 13, "ty": 7},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_plaza", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 16},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_town", "sprite": "tinderwick_lamp_post", "at": {"tx": 17, "ty": 24},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    # crown trees on the wooded valley border
    {"id": "tree_a", "sprite": "tinderwick_tree", "at": {"tx": 1, "ty": 28}, "w": 3, "h": 4,
     "overhang": 3, "walk_under": True},
    {"id": "tree_b", "sprite": "tinderwick_tree", "at": {"tx": 24, "ty": 28}, "w": 3, "h": 4,
     "overhang": 3, "walk_under": True},
    {"id": "tree_c", "sprite": "tinderwick_tree", "at": {"tx": 28, "ty": 17}, "w": 3, "h": 4,
     "overhang": 3, "walk_under": True},
    {"id": "tree_d", "sprite": "tinderwick_tree", "at": {"tx": 8, "ty": 29}, "w": 3, "h": 4,
     "overhang": 3, "walk_under": True},
]

# ---- the fenced garden (§11 rule 5: a town, not a lawn) ----------------------------
mk.fence_run(deco, W, H, 21, 23, 23)
mk.fence_run(deco, W, H, 21, 25, 23)
for gx in (21, 22, 23):
    deco[24 * W + gx] = gid("flowerbed_a") if gx % 2 else gid("flowerbed_b")

# ---- one-way ledges (the terraces remember you've won them) ------------------------
pt.ledge_run(deco, W, H, 10, 16, 18, rng)           # upper route -> festival hop
pt.ledge_run(deco, W, H, 21, 18, 20, rng)           # festival -> lower town hop

# ---- warps (graph.ts edge ids verbatim) --------------------------------------------
m["warps"] += [
    # WEST <-> cinderhead_deep (`to_terraces` lands {1,14}/{1,15}; we land one
    # tile inside its warp pair at {27,12}/{27,13})
    {"id": "to_cinderhead", "at": {"tx": 0, "ty": 14}, "trigger": "step_on",
     "to_map": "cinderhead_deep", "to": {"tx": 26, "ty": 12}, "facing": "left",
     "transition": "fade"},
    {"id": "to_cinderhead_s", "at": {"tx": 0, "ty": 15}, "trigger": "step_on",
     "to_map": "cinderhead_deep", "to": {"tx": 26, "ty": 13}, "facing": "left",
     "transition": "fade"},
    # NORTH -> windward_stair_i (graph `to_stair`, ungated; N2 authors the far
    # side — its return pair must land at our (14,1)/(15,1))
    {"id": "to_stair", "at": {"tx": 14, "ty": 0}, "trigger": "step_on",
     "to_map": "windward_stair_i", "to": {"tx": 14, "ty": 38}, "facing": "up",
     "transition": "fade"},
    {"id": "to_stair_e", "at": {"tx": 15, "ty": 0}, "trigger": "step_on",
     "to_map": "windward_stair_i", "to": {"tx": 15, "ty": 38}, "facing": "up",
     "transition": "fade"},
    # SOUTH -> the Lanternway spoke (graph `to_crossroads`; the hub's return
    # half wakes with gleam:storm — the R4 "[wakes with spoke]" pattern)
    {"id": "to_crossroads", "at": {"tx": 15, "ty": 31}, "trigger": "step_on",
     "to_map": "vesper_crossroads", "to": {"tx": 1, "ty": 3}, "facing": "right",
     "transition": "fade"},
    {"id": "to_crossroads_e", "at": {"tx": 16, "ty": 31}, "trigger": "step_on",
     "to_map": "vesper_crossroads", "to": {"tx": 1, "ty": 4}, "facing": "right",
     "transition": "fade"},
    # THE WINCH up to the skyloft — festival-flag-gated, NEVER Updraft (§0 r1)
    {"id": "to_skyloft", "at": {"tx": 21, "ty": 18}, "trigger": "step_on",
     "to_map": "galehigh_skyloft", "to": {"tx": 9, "ty": 10}, "facing": "up",
     "requires_flag": "flag:q_north_kite_blessed",
     "blocked_ref": "npc.winch_not_ready", "transition": "fade"},
    # THE DROP-HOME THERMAL back up to the Windward II crags (the return half
    # of `shortcut_galehigh` — N2's drop warp lands ON this tile; the ride up
    # opens with the same flag, set on first reaching the crags)
    {"id": "shortcut_stair", "at": {"tx": 21, "ty": 3}, "trigger": "step_on",
     "to_map": "windward_stair_ii", "to": {"tx": 4, "ty": 20}, "facing": "up",
     "requires_flag": "flag:shortcut_windward", "transition": "fade"},
]

# the Wind-Eye mouth on the high terrace (the gated spur promise, §3a rule 8)
# — target unauthored (safe inert tease until N2 builds it; declared in graph.ts)
owed += pt.gift_tease(m, deco, W, wid="to_windeye", at=(28, 2),
                      ability="updraft_kite", to_map="wind_eye", to=(9, 16),
                      trigger="step_on", facing="up",
                      sign_id="galehigh_windeye", sign_at=(27, 3))
for wp in m["warps"]:
    if wp["id"] == "to_windeye":
        wp["blocked_ref"] = "sign.galehigh_windeye"

# ---- story band: Mira shouts the hook down (covers the WHOLE walkable cut) ---------
for i, ty in enumerate((14, 15)):
    m["triggers"].append({
        "id": f"mira_quest_{i}", "kind": "cutscene", "at": {"tx": 4, "ty": ty},
        "activation": "step_on", "ref": "script.mira_quest", "once": True,
        "sets_flags": ["flag:q_north_kite"],
        "hidden_when_flag": "flag:q_north_kite"})
owed += ["script.mira_quest (sets flag:q_north_kite)"]

# ---- signs (refs owed; suggested copy in the module docstring) ---------------------
# NOT on the x=6 connector column — a sign there seals the entry throat
# (audit_flow caught it; the Pearlmoor west-spoke lesson)
owed += pt.sign(m, deco, W, sid="galehigh_welcome", at=(6, 19))
owed += pt.sign(m, deco, W, sid="galehigh_winch", at=(19, 17))
owed += pt.sign(m, deco, W, sid="galehigh_high_ledges", at=(22, 8))
owed += pt.sign(m, deco, W, sid="galehigh_lanternway", at=(17, 27))

# ---- trainer beats on the upper route (sight trainers ARE geometry) ----------------
owed += pt.trainer_beat(m, tid="galehigh_kitehand", at=(15, 2), facing="down",
                        sight=4, sprite="npc_woman")
owed += pt.trainer_beat(m, tid="galehigh_terracer", at=(20, 8), facing="left",
                        sight=4, sprite="npc_man")

# ---- caches ------------------------------------------------------------------------
# the kite-maker's chained errand (rule 3: a boolean chain — each pick reveals
# the next cache; picked_kite_c is consumed by script.kite_built)
owed += pt.cache(m, cid="kite_a", at=(8, 25))            # the spar, west verge
owed += pt.cache(m, cid="kite_b", at=(20, 25))           # the sail, east verge
owed += pt.cache(m, cid="kite_c", at=(27, 15))           # the tail, the farm shelf
for npc in m["npcs"]:
    if npc["id"] == "cache_kite_b":
        npc["requires_flag"] = "flag:picked_kite_a"
    if npc["id"] == "cache_kite_c":
        npc["requires_flag"] = "flag:picked_kite_b"
# cache variety: loose wicks off the lane, a valuable on the scree shelf, and
# the two high-terrace prizes (post-Updraft, both [MISSABLE] — walkthrough §4)
owed += pt.cache(m, cid="galehigh_wicks", at=(2, 28))    # takings-tin, SW corner
owed += pt.cache(m, cid="galehigh_amber", at=(4, 8))     # moth-amber, scree shelf
owed += pt.cache(m, cid="ledge_herb", at=(26, 5))        # N1 "The Crag-tender's Kettle"
owed += pt.cache(m, cid="galehigh_high", at=(29, 8))     # the hidden high valuable

# ---- encounters (band 28-30, continuous with Cinderhead Deep's 24-27) --------------
# walkthrough kin: "Kiteling" (the paper-glider bird -> #88 Sparrowcaw, Storm),
# Thrumvane (#97, Storm), Cirruff (#91, Storm/Light)
TABLE = [{"kin_id": 88, "weight": 40, "min_level": 28, "max_level": 30},
         {"kin_id": 97, "weight": 35, "min_level": 28, "max_level": 30},
         {"kin_id": 91, "weight": 25, "min_level": 28, "max_level": 30}]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if tallgrass[i]:
        (band_grid if 5 <= i // W <= 6 else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE, id_prefix="verge")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.055, table=TABLE, id_prefix="crossing")

# ---- NPCs --------------------------------------------------------------------------
m["npcs"] += [
    # --- the Kite-rising, in full swing on arrival (Arc E — unconditional) ----------
    {"id": "festival_piper", "at": {"tx": 14, "ty": 17}, "facing": "down",
     "sprite": "npc_shopkeeper", "movement": "look_around",
     "dialogue_ref": "npc.galehigh_festival_piper"},
    {"id": "festival_kid", "at": {"tx": 16, "ty": 18}, "facing": "up",
     "sprite": "npc_child", "movement": "wander",
     "dialogue_ref": "npc.galehigh_festival_kid"},
    {"id": "festival_goer", "at": {"tx": 12, "ty": 18}, "facing": "right",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.galehigh_festival_goer"},
    # witness beat: a festival-goer reacts once Mira's hook lands
    {"id": "quest_witness", "at": {"tx": 18, "ty": 17}, "facing": "left",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "npc.galehigh_quest_witness",
     "requires_flag": "flag:q_north_kite"},
    # Wren at the festival — the A4 foreshadow line; gone north once Storm relights
    {"id": "wren", "at": {"tx": 15, "ty": 14}, "facing": "down", "sprite": "wren",
     "movement": "wander", "dialogue_ref": "npc.wren_galehigh",
     "hidden_when_flag": "gleam:storm"},
    # --- the winch-keeper (the festival fly beat lives on him) ----------------------
    {"id": "winch_keeper_wait", "at": {"tx": 22, "ty": 18}, "facing": "left",
     "sprite": "npc_man", "movement": "static",
     "dialogue_ref": "npc.winch_keeper_wait",
     "hidden_when_flag": "flag:q_north_kite_ready"},
    {"id": "winch_keeper_fly", "at": {"tx": 22, "ty": 18}, "facing": "left",
     "sprite": "npc_man", "movement": "static",
     "dialogue_ref": "script.galehigh_kite_rising",
     "requires_flag": "flag:q_north_kite_ready",
     "hidden_when_flag": "flag:q_north_kite_blessed"},
    {"id": "winch_keeper_after", "at": {"tx": 22, "ty": 18}, "facing": "left",
     "sprite": "npc_man", "movement": "static",
     "dialogue_ref": "npc.winch_keeper_after",
     "requires_flag": "flag:q_north_kite_blessed"},
    # --- the kite-maker at her stall (errand giver -> builder -> the R4 leg) --------
    {"id": "kite_maker_lost", "at": {"tx": 17, "ty": 25}, "facing": "left",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.kite_maker_lost",
     "hidden_when_flag": "flag:picked_kite_c"},
    {"id": "kite_maker_build", "at": {"tx": 17, "ty": 25}, "facing": "left",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "script.kite_built",
     "requires_flag": "flag:picked_kite_c",
     "hidden_when_flag": "flag:q_north_kite_ready"},
    {"id": "kite_maker_after", "at": {"tx": 17, "ty": 25}, "facing": "left",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.kite_maker_after",
     "requires_flag": "flag:q_north_kite_ready",
     "hidden_when_flag": "gleam:storm"},
    # R4 "A Kite for the Waystone Kid" — wakes with the spoke (gleam:storm)
    {"id": "kite_maker_round", "at": {"tx": 17, "ty": 25}, "facing": "left",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "script.round_kite",
     "requires_flag": "gleam:storm",
     "hidden_when_flag": "flag:q_round_kite"},
    {"id": "kite_maker_round_after", "at": {"tx": 17, "ty": 25}, "facing": "left",
     "sprite": "npc_woman", "movement": "static",
     "dialogue_ref": "npc.kite_maker_round_after",
     "requires_flag": "flag:q_round_kite"},
    # --- Mira in town after the Gleam (then the N3 ribbon giver after met_cor) ------
    {"id": "mira_after", "at": {"tx": 15, "ty": 16}, "facing": "down",
     "sprite": "npc_lampwarden", "movement": "look_around",
     "dialogue_ref": "npc.mira_galehigh_after",
     "requires_flag": "gleam:storm", "hidden_when_flag": "flag:met_cor"},
    {"id": "mira_ribbon", "at": {"tx": 15, "ty": 16}, "facing": "down",
     "sprite": "npc_lampwarden", "movement": "static",
     "dialogue_ref": "script.ribbon_quest",
     "requires_flag": "flag:met_cor", "hidden_when_flag": "flag:q_north_ribbon"},
    {"id": "mira_ribbon_after", "at": {"tx": 15, "ty": 16}, "facing": "down",
     "sprite": "npc_lampwarden", "movement": "look_around",
     "dialogue_ref": "npc.mira_ribbon_after",
     "requires_flag": "flag:q_north_ribbon"},
    # --- ambient + post-Gleam festival payoff (the town answers the win) ------------
    {"id": "terrace_farmer", "at": {"tx": 26, "ty": 14}, "facing": "left",
     "sprite": "npc_old_man", "movement": "static",
     "dialogue_ref": "npc.galehigh_farmer"},
    {"id": "gleam_kid", "at": {"tx": 14, "ty": 18}, "facing": "up",
     "sprite": "npc_girl", "movement": "wander",
     "dialogue_ref": "npc.galehigh_gleam_kid",
     "requires_flag": "gleam:storm"},
    {"id": "gleam_farmer", "at": {"tx": 11, "ty": 19}, "facing": "right",
     "sprite": "npc_man", "movement": "look_around",
     "dialogue_ref": "npc.galehigh_gleam_farmer",
     "requires_flag": "gleam:storm"},
]
owed += ["npc.galehigh_festival_piper", "npc.galehigh_festival_kid",
         "npc.galehigh_festival_goer", "npc.galehigh_quest_witness",
         "npc.wren_galehigh", "npc.winch_keeper_wait",
         "script.galehigh_kite_rising (= cutscene.galehigh_kite_rising; "
         "sets flag:q_north_kite_blessed)",
         "npc.winch_keeper_after", "npc.winch_not_ready (winch warp blocked_ref)",
         "npc.kite_maker_lost", "script.kite_built (sets flag:q_north_kite_ready)",
         "npc.kite_maker_after", "script.round_kite (R4; sets flag:q_round_kite)",
         "npc.kite_maker_round_after", "npc.mira_galehigh_after",
         "script.ribbon_quest (N3; sets flag:q_north_ribbon)",
         "npc.mira_ribbon_after", "npc.galehigh_farmer",
         "npc.galehigh_gleam_kid", "npc.galehigh_gleam_farmer"]

# ---- scatter decor (avoid everything placed) ---------------------------------------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (tree, cliff, glacier, snowpatch,
                                         snowtrail, tallgrass, path))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
mk.scatter_decor(deco, base, W, H, rng, density=0.15, avoid=avoid)
# boulders breaking the upper snow/scree ground + the town corners
for (x, y) in [(9, 3), (3, 4), (21, 4), (27, 7), (7, 20), (22, 27)]:
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
