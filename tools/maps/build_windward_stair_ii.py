#!/usr/bin/env python3
"""
Windward Stair II — the high crags (walkthrough/03-north, Windward beats 3-4;
kind route, region north, band 34-36).

Bare, bright, windy: full snow, glacier crag masses, the warmest colour gone.
Three signature touches (§8):
  1. THE CRAGS BAND — `flag:shortcut_windward` is set the moment you step off
     the arrival shelf (the §0 trap #2: this region opens the shortcut, this
     map closes the flag). The band covers the WHOLE walkable cut (the 2-wide
     choke at the shelf's head) so it cannot be walked around.
  2. THE DROP HOME — the SW shelf ledge straight above Galehigh: warp
     `shortcut_galehigh` (graph.ts verbatim, requires_flag
     flag:shortcut_windward) lands ON Galehigh's new `shortcut_stair` return
     warp at (21,3) — the mutual-pair convention. The crag-tender walks her
     rounds beside it (npc.windward_crag_tender — the walkthrough hook's
     "crag-tender near the shortcut ledge", verbatim).
  3. THE QUIET LEDGE — the N3 "Wren's Ribbon" payoff pocket (W side, off the
     lane behind a crag): the wrecked festival kite snagged on the rocks and a
     wordless interact (`script.place_ribbon`, requires flag:q_north_ribbon,
     sets flag:q_north_ribbon_placed). No dialogue by design.

Also here: the N2 "Aurora Sketcher" first viewpoint (`script.sketch_crag` at
the NE vista — requires flag:q_north_sketch, the quest-start flag the Pale
Vault giver sets, per the flag:q_<region>_<short> convention; sets
flag:q_north_sketch_1); the Updraft-gated `to_roost` lip (E) to Thunderroost
([MISSABLE] — signed hard); and the UNGATED `to_glacier` exit north (§0 trap
#1: no barrier between here and Pale Vault's town/Lumenary — N3 lands the
far side; landing coords are placeholders the engine no-ops until then).

Encounter picks (N5 mirrors into EXTRA_ENCOUNTERS): same four lines as
Stair I with the Frost-edge kin weighted UP as the glacier nears (Arc D):
#95 Glacewing and #89 Flintbeak lead, #45 Sparkrat / #98 Thrumble trail.

Suggested sign copy (sincere — the stair's ONE wry line lives on Stair I):
  sign.windward_roost  "THUNDERROOST. The storm-birds keep it. Mind the
                        nest — and the weather it dreams." (the [MISSABLE]
                        spur callout)

Run:  ./venv/bin/python tools/maps/build_windward_stair_ii.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 28, 24
rng = random.Random(62)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
glacier = mk.make_grid(W, H)
ice = mk.make_grid(W, H)        # frozen melt-pools near the glacier exit (the tease)
snowtrail = mk.make_grid(W, H)
frosttuft = mk.make_grid(W, H)

# BORDERS: glacier crag all round, 2 deep
mk.rect(glacier, W, H, 0, 0, W - 1, 1)
mk.rect(glacier, W, H, 0, 0, 1, H - 1)
mk.rect(glacier, W, H, 26, 0, 27, H - 1)
mk.rect(glacier, W, H, 0, 22, W - 1, H - 1)
# north exit gap to pale_vault_glacier (cols 20-21)
for y in (0, 1):
    glacier[y * W + 20] = 0
    glacier[y * W + 21] = 0
# south thermal notch — the arrival/return lip (cols 13-14, 1 deep so the
# border row stays solid behind the warp tiles)
glacier[22 * W + 13] = 0
glacier[22 * W + 14] = 0
# east roost lip notch (rows 9-10 stay open through the border at x26 only —
# the warp itself sits inside at (25,9); the notch reads as the crag parting)
glacier[9 * W + 26] = 0
glacier[10 * W + 26] = 0

# THE ARRIVAL SHELF: a walled pocket (rows 16-21, x10-17) with one 2-wide
# choke at its head — the crags band lives ON the choke
mk.rect(glacier, W, H, 9, 15, 9, 21)
mk.rect(glacier, W, H, 18, 15, 18, 21)
mk.rect(glacier, W, H, 9, 15, 18, 15)
for x in (13, 14):
    glacier[15 * W + x] = 0

# THE RIDGE splitting the field (gap at x13-14 carries the lane north; a
# one-way snow ledge at x18-20 drops the return back to the south strip —
# §3a rule 2, asymmetry by direction)
mk.rect(glacier, W, H, 2, 12, 25, 13)
for x in (13, 14, 18, 19, 20):
    glacier[12 * W + x] = 0
    glacier[13 * W + x] = 0

# the SOUTH STRIP (row 14, x2-25) joins the ridge gap, the shelf choke and the
# SW pocket; the pocket (the shortcut shelf, rows 16-21 x2-7) is entered at
# the (5-6,15) gap in its north wall
mk.rect(glacier, W, H, 8, 15, 8, 21)
mk.rect(glacier, W, H, 2, 15, 7, 15)
for x in (5, 6):
    glacier[15 * W + x] = 0

# CRAG MASSES in the north field (organic, §11 r2/r3)
mk.blob(glacier, W, H, 8, 5.5, 2.6, 2.0)
mk.blob(glacier, W, H, 17, 4.0, 2.2, 1.6)
mk.blob(glacier, W, H, 5, 10.0, 1.8, 1.2)

# frozen melt-pools by the north exit — the Pale Vault tease (walkable floor)
mk.blob(ice, W, H, 23.5, 2.5, 2.2, 1.4)
mk.blob(ice, W, H, 18.0, 2.0, 1.6, 1.0)

# ---- the lane (snowtrail on snow — context-correct) --------------------------------
mk.vline(snowtrail, W, H, 13, 12, 21)
mk.vline(snowtrail, W, H, 14, 12, 21)
mk.hline(snowtrail, W, H, 10, 13, 21)
mk.hline(snowtrail, W, H, 11, 13, 21)
mk.vline(snowtrail, W, H, 20, 0, 10)
mk.vline(snowtrail, W, H, 21, 0, 10)

# ---- encounter terrain -------------------------------------------------------------
# optional pockets: the south strip's east shelf + the NW fold
mk.blob(frosttuft, W, H, 21.5, 15.0, 3.0, 1.4)
mk.blob(frosttuft, W, H, 4.5, 3.5, 2.2, 1.4)
# MANDATORY crossing: the north corridor band (rows 6-7), wall-to-wall —
# everything north (the exit, the vista) is across it; the lane pauses
# through (§11 r7; glacier precedence trims it to the walkable corridor)
pt.mandatory_band(frosttuft, snowtrail, W, H, y0=6, y1=7, x0=2, x1=25)

# ---- precedence --------------------------------------------------------------------
for i in range(W * H):
    if glacier[i]:
        snowtrail[i] = 0
        frosttuft[i] = 0
        ice[i] = 0
    if snowtrail[i] or ice[i]:
        frosttuft[i] = 0

# ---- base: full snow ---------------------------------------------------------------
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_ice", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": ice},
    {"name": "t_snowtrail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": snowtrail},
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
]

m: dict = {
    "id": "windward_stair_ii", "display_name": "Windward Stair",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/windward-stair-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/windward-stair-a.webp",
        "assets/backgrounds/battle/windward-stair-b.webp",
    ],
}

deco = mk.make_grid(W, H)

# ---- the ridge ledge (one-way drop back to the south strip) ------------------------
pt.ledge_run(deco, W, H, 12, 18, 20, rng, family="snow")

# ---- warps (graph.ts ids verbatim) -------------------------------------------------
m["warps"] += [
    # SOUTH <-> windward_stair_i (the wind-gap thermal; the return glide is
    # gated too — you can only be up here with the kite). Stair I's pair lands
    # at (13,21)/(14,21), one tile inside these.
    {"id": "to_stair_i", "at": {"tx": 13, "ty": 22}, "trigger": "step_on",
     "to_map": "windward_stair_i", "to": {"tx": 8, "ty": 4}, "facing": "down",
     "requires_ability": "updraft_kite", "transition": "fade"},
    {"id": "to_stair_i_e", "at": {"tx": 14, "ty": 22}, "trigger": "step_on",
     "to_map": "windward_stair_i", "to": {"tx": 9, "ty": 4}, "facing": "down",
     "requires_ability": "updraft_kite", "transition": "fade"},
    # NORTH -> pale_vault_glacier (`to_glacier`, UNGATED — §0 trap #1; N3
    # authors the far side, landing is a placeholder until then)
    {"id": "to_glacier", "at": {"tx": 20, "ty": 0}, "trigger": "step_on",
     "to_map": "pale_vault_glacier", "to": {"tx": 14, "ty": 28}, "facing": "up",
     "transition": "fade"},
    {"id": "to_glacier_e", "at": {"tx": 21, "ty": 0}, "trigger": "step_on",
     "to_map": "pale_vault_glacier", "to": {"tx": 15, "ty": 28}, "facing": "up",
     "transition": "fade"},
    # EAST -> thunderroost (`to_roost`, Updraft-gated spur — lands ON the
    # roost's return warp, the mutual-pair convention)
    {"id": "to_roost", "at": {"tx": 25, "ty": 9}, "trigger": "step_on",
     "to_map": "thunderroost", "to": {"tx": 2, "ty": 6}, "facing": "right",
     "requires_ability": "updraft_kite",
     "blocked_ref": "sign.windward_roost", "transition": "fade"},
    # SW -> the DROP HOME (`shortcut_galehigh`, requires the crags flag) —
    # lands ON Galehigh's `shortcut_stair` return warp at (21,3)
    {"id": "shortcut_galehigh", "at": {"tx": 4, "ty": 21}, "trigger": "step_on",
     "to_map": "galehigh_terraces", "to": {"tx": 21, "ty": 3}, "facing": "down",
     "requires_flag": "flag:shortcut_windward", "transition": "fade"},
]

# ---- THE CRAGS BAND (§0 trap #2): the arrival shelf's whole walkable width --------
# (rows 16-21 x10-17 are the shelf; the band crosses row 19 wall-to-wall so a
# player stepping OFF the thermal cannot reach the crags around it)
for i, tx in enumerate(range(10, 18)):
    m["triggers"].append({
        "id": f"windward_crags_{i}", "kind": "script",
        "at": {"tx": tx, "ty": 19}, "activation": "step_on",
        "ref": "script.windward_crags", "once": True,
        "sets_flags": ["flag:shortcut_windward"],
        "hidden_when_flag": "flag:shortcut_windward"})
owed += ["script.windward_crags (sets flag:shortcut_windward; the 'now "
         "accessible' callout naming the Galehigh drop + Thunderroost)"]

# ---- the quiet ledge: N3 "Wren's Ribbon" (wordless by design) ----------------------
m["triggers"].append({
    "id": "ribbon_ledge", "kind": "script", "at": {"tx": 4, "ty": 10},
    "activation": "interact", "ref": "script.place_ribbon", "once": True,
    "requires_flag": "flag:q_north_ribbon",
    "sets_flags": ["flag:q_north_ribbon_placed"],
    "hidden_when_flag": "flag:q_north_ribbon_placed"})
owed += ["script.place_ribbon (wordless; sets flag:q_north_ribbon_placed)"]

# ---- the N2 sketch viewpoint (NE vista, across the band) ---------------------------
m["triggers"].append({
    "id": "sketch_viewpoint", "kind": "script", "at": {"tx": 24, "ty": 4},
    "activation": "interact", "ref": "script.sketch_crag", "once": True,
    "requires_flag": "flag:q_north_sketch",
    "sets_flags": ["flag:q_north_sketch_1"],
    "hidden_when_flag": "flag:q_north_sketch_1"})
owed += ["script.sketch_crag (requires flag:q_north_sketch — the Pale Vault "
         "giver's quest flag, N3 wires; sets flag:q_north_sketch_1)"]

# ---- objects -----------------------------------------------------------------------
m["objects"] += [
    # the wrecked festival kite on the quiet ledge (bespoke)
    {"id": "kite_wreck", "sprite": "windward_kite_wreck", "at": {"tx": 3, "ty": 8},
     "w": 2, "h": 2, "overhang": 0, "walk_under": False},
    # cairns marking the drop home and the exit lane
    {"id": "cairn_drop", "sprite": "windward_cairn", "at": {"tx": 2, "ty": 19},
     "w": 2, "h": 3, "overhang": 2, "walk_under": False},
    {"id": "cairn_exit", "sprite": "windward_cairn", "at": {"tx": 17, "ty": 8},
     "w": 2, "h": 3, "overhang": 2, "walk_under": False},
    # the roost thermal rising past the east lip
    {"id": "roost_updraft", "sprite": "windward_updraft", "at": {"tx": 26, "ty": 7},
     "w": 2, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
    # the shelf thermal the arrival rides (drawn over the south notch)
    {"id": "arrival_updraft", "sprite": "windward_updraft", "at": {"tx": 15, "ty": 20},
     "w": 2, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
    # a lamp post where the lane bends east
    {"id": "lamp_bend", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 9},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- signs -------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="windward_roost", at=(24, 10))

# ---- trainer beat (lv ~35-36 — N5 authors TRAINERS) --------------------------------
owed += pt.trainer_beat(m, tid="windward_cragwatch", at=(16, 11), facing="right",
                        sight=4, sprite="npc_woman")

# ---- the crag-tender's rounds (the witness beat for the crags band) ----------------
m["npcs"] += [
    {"id": "crag_tender_rounds", "at": {"tx": 5, "ty": 20}, "facing": "down",
     "sprite": "npc_old_woman", "movement": "look_around",
     "dialogue_ref": "npc.windward_crag_tender",
     "requires_flag": "flag:shortcut_windward"},
]

# ---- caches (variety: a valuable across the band, a consumable in the pocket) ------
owed += pt.cache(m, cid="windward_amber", at=(25, 3))    # Moth-amber, NE vista
owed += pt.cache(m, cid="windward_kit", at=(2, 16))      # consumable, SW pocket

# ---- encounters (band 34-36, Frost-edge weighted up — see docstring) ---------------
TABLE = [{"kin_id": 95, "weight": 25, "min_level": 35, "max_level": 36},
         {"kin_id": 89, "weight": 25, "min_level": 34, "max_level": 36},
         {"kin_id": 45, "weight": 20, "min_level": 34, "max_level": 36},
         {"kin_id": 98, "weight": 20, "min_level": 35, "max_level": 36},
         # N5 reconcile: Geolace (#74, Frost/Stone base) — the walkthrough's
         # "crag-climber" Stone note, and the geolace -> geodrake -> vaultclaw
         # line's only wild placement; rare on the high crags
         {"kin_id": 74, "weight": 10, "min_level": 34, "max_level": 36}]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
for i in range(W * H):
    if frosttuft[i]:
        (band_grid if (i // W) in (6, 7) else patch_grid)[i] = 1
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE, id_prefix="crag")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE, id_prefix="crossing")

# ---- scatter + boulders ------------------------------------------------------------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (glacier, ice, snowtrail, frosttuft))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
mk.scatter_decor(deco, base, W, H, rng, density=0.15, avoid=avoid)
for (x, y) in [(11, 3), (3, 6), (23, 8), (7, 9), (24, 14), (19, 17),
               (16, 17), (6, 17), (12, 2)]:
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
