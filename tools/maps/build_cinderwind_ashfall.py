#!/usr/bin/env python3
"""
The Ashfall Shelf — the main-path leg between Cinderwind Scarp and Galehigh
(walkthrough/10-the-farlamp-isles.md Part II; kind route, region north, band
30-33). At world (93,-231), directly north of the Scarp; 24x28.

Why it exists: after Otho the player walked three caves and then ONE map carried
the whole 28 -> 34 climb to Mira. The Scarp's east cut to Galehigh is now a
ROCKFALL (gated warps; the Galehigh haulers clear it the first time you arrive by
this road), so the way on is UP onto this shelf and round.

Daylight after the caves: a high shelf where Cinderhead's slag was tipped for a
century, so the grass grows grey out of the ash. Three signature touches (§8):
  1. THE HAULERS' CAMP — canvas lean-to and a lit brazier (the leg's REST POINT,
     script.ashfall_brazier_rest: heal, sleeps), Oda Kilnwright keeping it;
  2. THE OLD KILN STACK on the north cliff, its hot draught an updraft vent
     (`to_kiln`, Updraft Kite) up to Kiln Gully — seen now, earned after Mira;
  3. THE WINDWARD GAP in the east wall — a lookout over Windward Stair I and a
     Kite-gated crossing to it (`to_windward`), the second come-back.

Shape (rows top-down):
  * rows 0-2   the north mountain face; the kiln stack stands on its lip;
  * rows 3-12  THE TOP SHELF (ash): camp W, a full-height blighttuft crossing in
               the middle, the vent + the Windward lookout E;
  * rows 13-14 the shelf's cliff band: a 1-wide slag cut at x=4 (the climb, the
               ash-picker posted above it), the 2-wide descent at x=18-19 (the
               gale-watch posted at its head), and a LEDGE at x=11-12 dropping
               into the hidden SLAG NOOK;
  * rows 14-18 the slag nook (x 11-12): an ash-buried cache, seen from the
               shelf above, reached only by the drop; a second ledge (row 18)
               drops you out into the basin — the ledge loop;
  * rows 15-26 west: THE BASIN (green, from the Scarp; a mandatory grass band);
               east: THE GATE SHELF (green, to Galehigh), split by a cliff wall.
The way on is a loop (in at the basin, up the cut, east across the ash, down to
the gate shelf); the drop through the nook is the quick way back down.

Edges (world geometry, binding — docs/world/geometry.md):
  S  (5,27)/(6,27)  <-> cinderwind_scarp (5,0)/(6,0)       [`to_scarp` / Scarp `to_ashfall`]
  E  (23,25)/(23,26) <-> galehigh_terraces (0,7)/(0,8)     [`to_terraces` / Galehigh `to_ashfall`]
     (Ashfall rows 18-27 = Galehigh rows 0-9; offset 18)
  E  (23,7)/(23,8)  <-> windward_stair_i (0,29)/(0,30)     [`to_windward`, Updraft Kite]
     (Ashfall rows 0-17 = Windward rows 22-39; offset 22)
  portal: the vent (18,3) -> cinderwind_kiln (10,16)        [`to_kiln`, Updraft Kite]

Wild kin (lv 30-33): Gravelo, Sparkrat, Flintbeak, Galefox, Pyrolith and the
shelf's own rare, STONEBARK (#63, Verdant/Stone — never wild before: the grey
ash-grass is where it grows). Tables mirrored in build_species.py.

Run:  ./venv/bin/python tools/maps/build_cinderwind_ashfall.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
import warp_markers as wm
from mapkit import gid

W, H = 24, 28
rng = random.Random(231)
owed: list[str] = []

cliff = mk.make_grid(W, H)
tree = mk.make_grid(W, H)
path = mk.make_grid(W, H)
tallgrass = mk.make_grid(W, H)     # green encounter grass (basin, gate shelf)
ashtuft = mk.make_grid(W, H)       # blighttuft — the ash-grass encounter bed (top shelf)
deco = mk.make_grid(W, H)

# ---- enclosure ---------------------------------------------------------------------
mk.rect(cliff, W, H, 0, 0, W - 1, 2)                     # the north mountain face
mk.rect(cliff, W, H, 0, 0, 1, H - 1)                     # west: the mountain's flank
mk.rect(cliff, W, H, W - 2, 0, W - 1, 24)                # east: the drop to Windward/Galehigh
mk.organic_border(cliff, W, H, depth=0,
                  bumps=[(2, 9, 1), (2, 24, 1), (21, 4, 1), (13, 3, 1), (2, 3, 1)], rng=rng)
for y in (7, 8):                                         # the WINDWARD GAP (Kite crossing)
    for x in (W - 2, W - 1):
        cliff[y * W + x] = 0
mk.rect(tree, W, H, 0, H - 1, W - 1, H - 1)              # the Scarp's crest wood (continues it)
mk.organic_border(tree, W, H, depth=0, bumps=[(9, 27, 1), (2, 26, 1), (16, 27, 1)], rng=rng)
for x in (5, 6):                                         # SOUTH gap: down to the Scarp
    for y in (H - 2, H - 1):
        tree[y * W + x] = 0
for y in (25, 26):                                       # EAST gap: Galehigh's upper road
    for x in range(W - 3, W):
        cliff[y * W + x] = tree[y * W + x] = 0
for x in range(W - 3, W):                                 # the gate shelf's south lip
    cliff[(H - 1) * W + x] = 1
    tree[(H - 1) * W + x] = 0

# ---- the shelf band (rows 13-14) ----------------------------------------------------
mk.rect(cliff, W, H, 2, 13, 21, 14)
CUT_X = 4                                                # the slag cut — the climb (1 wide)
DESCENT = (18, 19)                                       # the way down to the gate shelf
NOOK = (11, 12)                                          # the ledge into the slag nook
for x in (CUT_X, *DESCENT, *NOOK):
    cliff[13 * W + x] = cliff[14 * W + x] = 0
pt.ledge_run(deco, W, H, 13, NOOK[0], NOOK[1], rng)      # shelf -> nook (one way)

# ---- the slag nook + the divider ------------------------------------------------------
mk.rect(cliff, W, H, 9, 15, 10, 18)                      # nook west wall
mk.rect(cliff, W, H, 13, 15, 14, 26)                     # nook east wall = basin/gate divider
mk.rect(cliff, W, H, 13, 14, 14, 14)
pt.ledge_run(deco, W, H, 18, NOOK[0], NOOK[1], rng)      # nook -> basin (one way)

# ---- lanes (green ground only; the ash keeps no road) --------------------------------
LANE = set()
for y in range(15, H):
    LANE |= {(5, y), (6, y)}                             # basin: up from the Scarp
LANE |= {(4, 15), (4, 16), (CUT_X, 13), (CUT_X, 14)}     # to the foot of the cut
for y in range(15, 27):
    LANE |= {(18, y), (19, y)}                           # gate shelf: down from the descent
for x in range(18, W):
    LANE |= {(x, 25), (x, 26)}                           # ...east to Galehigh
for (x, y) in LANE:
    path[y * W + x] = 1

# ---- encounter beds ------------------------------------------------------------------
pt.mandatory_band(tallgrass, path, W, H, y0=21, y1=22, x0=2, x1=12)     # the basin crossing
mk.blob(tallgrass, W, H, 16.2, 19.5, 1.3, 2.2)                         # gate shelf: optional
mk.blob(tallgrass, W, H, 3.2, 18.0, 1.3, 1.2)                          # basin west pocket
# the top shelf's full-height ash crossing (x 14-16) + a grind pocket by the camp
for y in range(3, 13):
    for x in (14, 15, 16):
        ashtuft[y * W + x] = 1
mk.blob(ashtuft, W, H, 6.0, 10.5, 2.2, 1.0)

for i in range(W * H):
    if cliff[i]:
        tree[i] = 0
    if cliff[i] or tree[i]:
        path[i] = tallgrass[i] = ashtuft[i] = 0
    if tallgrass[i] or ashtuft[i]:
        path[i] = 0

# ---- base: ash (blight) above the band, green below, slag (basalt) in the nook --------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
bl = [gid("blight0"), gid("blight1"), gid("blight2"), gid("blight3")]
base = []
for i in range(W * H):
    x, y = i % W, i // W
    # the ash stops at the shelf band (rows 13-14): the cut and the descent
    # carry the grey down their first step, then the green begins
    if y <= 13:
        base.append(rng.choice(bl) if rng.random() < 0.55 else bl[0])
    else:
        base.append(rng.choice(gg) if rng.random() < 0.5 else gg[0])

m: dict = {
    "id": "cinderwind_ashfall", "display_name": "The Ashfall Shelf",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": "assets/audio/music/cinderwind-ashfall.mp3",
    "battle_backdrops": ["assets/backgrounds/battle/ashfall-a.webp"],
}


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)


# ---- warps -----------------------------------------------------------------------------
KITE = {"requires_ability": "updraft_kite"}
m["warps"] += [
    {"id": "to_scarp", "at": {"tx": 5, "ty": H - 1}, "trigger": "step_on",
     "to_map": "cinderwind_scarp", "to": {"tx": 5, "ty": 1}, "facing": "down", "transition": "fade"},
    {"id": "to_scarp_e", "at": {"tx": 6, "ty": H - 1}, "trigger": "step_on",
     "to_map": "cinderwind_scarp", "to": {"tx": 6, "ty": 1}, "facing": "down", "transition": "fade"},
    {"id": "to_terraces", "at": {"tx": W - 1, "ty": 25}, "trigger": "step_on",
     "to_map": "galehigh_terraces", "to": {"tx": 1, "ty": 7}, "facing": "right", "transition": "fade"},
    {"id": "to_terraces_s", "at": {"tx": W - 1, "ty": 26}, "trigger": "step_on",
     "to_map": "galehigh_terraces", "to": {"tx": 1, "ty": 8}, "facing": "right", "transition": "fade"},
    {"id": "to_windward", "at": {"tx": W - 1, "ty": 7}, "trigger": "step_on",
     "to_map": "windward_stair_i", "to": {"tx": 1, "ty": 29}, "facing": "right",
     "transition": "fade", "blocked_ref": "npc.ashfall_windgap", **KITE},
    {"id": "to_windward_s", "at": {"tx": W - 1, "ty": 8}, "trigger": "step_on",
     "to_map": "windward_stair_i", "to": {"tx": 1, "ty": 30}, "facing": "right",
     "transition": "fade", "blocked_ref": "npc.ashfall_windgap", **KITE},
    {"id": "to_kiln", "at": {"tx": 18, "ty": 3}, "trigger": "step_on",
     "to_map": "cinderwind_kiln", "to": {"tx": 10, "ty": 16}, "facing": "up",
     "transition": "fade", "blocked_ref": "npc.ashfall_kiln_draught", **KITE},
]
owed += ["npc.ashfall_windgap", "npc.ashfall_kiln_draught"]

# ---- the top shelf ----------------------------------------------------------------------
# the old kiln stack on the cliff lip (walk-behind; its base row is the solid one)
obj("kiln_stack", "ashfall_kiln_stack", (19, 0), 2, 4, overhang=3, walk_under=True)
# the haulers' camp: lean-to + the brazier (the REST POINT — Confirm on any brazier tile)
obj("haulers_camp", "ashfall_haulers_camp", (2, 4), 3, 2)
obj("camp_brazier", "ashfall_brazier", (6, 3), 2, 3, overhang=2, walk_under=True)
m["triggers"].append({"id": "brazier_rest", "kind": "cutscene", "at": {"tx": 6, "ty": 5},
                      "activation": "interact", "ref": "script.ashfall_brazier_rest"})
owed.append("script.ashfall_brazier_rest")
obj("camp_cart", "cinderhead_ore_cart", (2, 7), 2, 2, overhang=1)
obj("shelf_slag_a", "ashfall_slag_heap", (9, 3), 3, 2)
obj("shelf_slag_b", "ashfall_slag_heap_b", (11, 9), 2, 2)
obj("shelf_slag_c", "ashfall_slag_heap_b", (19, 9), 2, 2)
obj("shelf_cullet", "ashfall_glass_cullet", (10, 6), 2, 2)
obj("nook_slag", "ashfall_slag_heap_b", (11, 16), 2, 2)
obj("shelf_lamp", "tinderwick_lamp_post", (8, 9), 1, 3, overhang=2, walk_under=True)
# the Windward lookout — a wind cairn on the gap, and the view (Confirm on the cairn)
obj("windward_cairn", "windward_cairn", (20, 5), 2, 3, overhang=2)
m["triggers"].append({"id": "windward_vista", "kind": "cutscene", "at": {"tx": 20, "ty": 7},
                      "activation": "interact", "ref": "script.ashfall_vista"})
owed.append("script.ashfall_vista")

# ---- the slag nook (the ash-buried cache) -----------------------------------------------
owed += pt.cache(m, cid="ashfall_nook", at=(12, 15))

# ---- the basin + the gate shelf ----------------------------------------------------------
obj("basin_slag", "ashfall_slag_heap", (8, 24), 3, 2)
obj("basin_rocks", "ashfall_rockfall_b", (2, 15), 2, 2)
obj("basin_lamp", "tinderwick_lamp_post", (7, 15), 1, 3, overhang=2, walk_under=True)
obj("basin_tree", "tinderwick_tree", (2, 22), 3, 4, overhang=3, walk_under=True)
obj("gate_slag", "ashfall_slag_heap", (15, 23), 3, 2)
obj("gate_cart", "cinderhead_ore_cart", (20, 17), 2, 2, overhang=1)
obj("gate_rocks", "ashfall_rockfall_b", (15, 15), 2, 2)
obj("gate_lamp", "tinderwick_lamp_post", (20, 22), 1, 3, overhang=2, walk_under=True)
owed += pt.cache(m, cid="ashfall_tin", at=(21, 20))
owed += pt.sign(m, deco, W, sid="cinderwind_ashfall", at=(7, 25))
owed += pt.sign(m, deco, W, sid="ashfall_gate", at=(21, 24))

# ---- trainers (route class; the beats ARE the chokes) -----------------------------------
# the ash-picker watches the head of the cut (every climber comes up his column)
owed += pt.trainer_beat(m, tid="ashfall_picker", at=(CUT_X, 9), facing="down", sight=3,
                        sprite="npc_man")
# the gale-watch holds the descent's head (both lanes of it pass her)
owed += pt.trainer_beat(m, tid="ashfall_galewatch", at=(20, 12), facing="left", sight=2,
                        sprite="kite_weaver")

# ---- NPCs at the camp ------------------------------------------------------------------
m["npcs"] += [
    # Oda Kilnwright — the kiln-wright's family; "The Last Pane" (flag-staged script)
    {"id": "oda_kilnwright", "at": {"tx": 8, "ty": 5}, "facing": "left",
     "sprite": "npc_old_woman", "movement": "static", "dialogue_ref": "script.oda_kilnwright"},
    # a hauler warming his hands — the camp's colour
    {"id": "camp_hauler", "at": {"tx": 5, "ty": 6}, "facing": "right",
     "sprite": "npc_man", "movement": "look_around", "dialogue_ref": "npc.ashfall_camp_hauler"},
]
owed += ["script.oda_kilnwright", "npc.ashfall_camp_hauler"]

# ---- encounters (band 30-33; the ash-grass and the green share one table) -----------------
TABLE = [
    {"kin_id": 49, "weight": 25, "min_level": 31, "max_level": 33},    # Gravelo — Stone
    {"kin_id": 45, "weight": 22, "min_level": 30, "max_level": 31},    # Sparkrat — Stone/Storm
    {"kin_id": 89, "weight": 20, "min_level": 30, "max_level": 32},    # Flintbeak — Storm
    {"kin_id": 101, "weight": 16, "min_level": 30, "max_level": 32},   # Galefox — Storm
    {"kin_id": 43, "weight": 12, "min_level": 32, "max_level": 33},    # Pyrolith — Ember/Stone
    {"kin_id": 63, "weight": 5, "min_level": 30, "max_level": 31},     # Stonebark — the shelf's rare
]
m["encounters"] = (
    pt.zones_from_grid(tallgrass, W, H, terrain="tall_grass", rate=0.10,
                       id_prefix="ashfall_green", table=TABLE)
    + pt.zones_from_grid(ashtuft, W, H, terrain="tall_grass", rate=0.10,
                         id_prefix="ashfall_ash", table=TABLE))

# ---- deco --------------------------------------------------------------------------------
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (cliff, tree, path, tallgrass, ashtuft, deco))}
avoid = covered | object_cells | point_cells | LANE
# ash-shelf scatter: grey moss, pebbles and a few boulders (scatter_decor only dresses grass)
ash_bits = [gid("greymoss_a"), gid("greymoss_b"), gid("g_pebble")]
for y in range(3, 13):
    for x in range(2, 22):
        if (x, y) not in avoid and rng.random() < 0.10 and (x, y) != (18, 4):
            deco[y * W + x] = rng.choice(ash_bits)
for (x, y) in [(12, 4), (17, 10), (3, 9)]:
    if (x, y) not in avoid:
        deco[y * W + x] = gid("boulder")
mk.scatter_decor(deco, base, W, H, rng, density=0.12, avoid=avoid)

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_tallgrass", "role": "terrain", "terrain": "tallgrass",
     "set": "vesper_overworld_set", "depth": 0, "data": tallgrass},
    {"name": "t_blighttuft", "role": "terrain", "terrain": "blighttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": ashtuft},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
    {"name": "t_tree", "role": "terrain", "terrain": "tree",
     "set": "vesper_overworld_set", "depth": 0, "data": tree},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    # warp markers: the kiln stack's thermal + the Windward gap's thermals (Kite-gated)
    wm.add(m, wm.marker("kiln_vent", "updraft_vent", 18, 3),
           wm.marker("windgap_vent", "updraft_vent", W - 1, 7),
           wm.marker("windgap_vent_s", "updraft_vent", W - 1, 8))
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
