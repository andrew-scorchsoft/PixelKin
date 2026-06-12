#!/usr/bin/env python3
"""
Windward Stair I — the great switchback climb (walkthrough/03-north, Windward
beat 1-2; kind route, region north, band 34-36).

Arc D: climbing out of Galehigh's last warmth into the high blue — the map is
a GRADIENT: snowpatch-dusted grass at the foot (continuing Galehigh's snowline
top band seam-for-seam), bare scree through the middle switchbacks, full snow
on the high leg. Three signature touches (§8):
  1. THE S-BEND CLIMB — four cliff/glacier banks fold the path 4 times
     (§3a rule 11), each bend a beat: a frosttuft crossing, a trainer's line,
     the kettle camp, the wind-gap. The kettle camp on leg 3 is the §2b
     MID-CLIMB REST SHELF (N6 MIN-2): the crag-tender's lit camp + kettle,
     a wrecked kite, the lamp-post and the wind-cairn clustered under bank C
     — a sheltered, encounter-free beat at the ~halfway mark of the climb;
  2. WIND-CAIRNS — the bespoke lamp-topped waymarkers marking each bend
     (assets/tilesets/windward/objects);
  3. THE WIND-GAP — the climb ends at a void chasm with a 2-tile promontory:
     the first place Updraft Kite is REQUIRED (the genre's earned crossing).
     The updraft column object rises beside the tongue.

Asymmetry by direction (§3a rule 2): every bank carries a one-way ledge
segment (scree_ledge_s / snow_ledge_s) so the return trip drops in seconds
what the climb earned in minutes.

HANDSHAKE (N1, binding): galehigh `to_stair` lands here at (14,38)/(15,38) —
the map is 40 tall with those tiles walkable; our return pair at (14,39)/(15,39)
lands at galehigh (14,1)/(15,1). Boundary `to_stair_ii` (graph.ts verbatim) is
Updraft-gated at the promontory tip (8,3)/(9,3), landing stair_ii (13,21)/(14,21).

N1 "The Crag-tender's Kettle" — the giver camps on the upper switchbacks
(leg 3): script.kettle_quest sets flag:q_north_kettle; the wind-burnt
ledge-herb cache lives on Galehigh's high terrace (N1's builder, post-Updraft,
flag:picked_ledge_herb); script.kettle_done (requires the herb via the
placement) gives the Warm Flask + sets flag:q_north_kettle_done only (N7
POL-2: it no longer re-sets flag:q_north_kettle — nothing consumes it, and
the NPC states key on picked_ledge_herb / q_north_kettle_done, so both orders
hold: herb-first skips straight to kettle_done, quest-first runs the chain).
The kite-maker flag-pair pattern keeps the states mutually exclusive. Her
standing line ref npc.windward_crag_tender (the walkthrough hook, verbatim) is
her after-state here and her shortcut-ledge rounds placement on Stair II.

Encounter picks (no pre-designed rows — N5 mirrors into EXTRA_ENCOUNTERS):
walkthrough's "crag-climber ram / slate-wing moth / gust-finch" mapped to real
species at band 34-36: #89 Flintbeak (Storm, the gust-finch line's mid stage —
continues Galehigh's Sparrowcaw verges), #45 Sparkrat (Stone/Storm — the only
Stone/Storm line, the crag-climber), #98 Thrumble (Storm, Thrumvane's mid
stage), #95 Glacewing (Storm/Frost, low weight — the slate-wing flier and the
glacier foreshadow). Bands roll at 0.05 (mandatory), pockets at 0.11 (§3a r12).
The SE FOOT VERGE rolls its own gentler band 32-34 (N6 MIN-3: softens the
literal Galehigh 28-30 border step to +2 for a player who skips the skyloft
wards) on the three common Storm-country lines only — the Frost edge
(Glacewing/Chillpip) still starts on the cold upper ledges. Mirrored into
EXTRA_ENCOUNTERS as min 32 for flintbeak/sparkrat/thrumble.

Suggested sign copy (the wiring agent writes dialogue.ts; humour sheet — the
distance-marker is the cluster's ONE wry line, politely exhausted):
  sign.windward_marker   "WINDWARD STAIR — Galehigh: 412 steps down. Pale
                          Vault: a good deal more up. The Stair Warden counted
                          once, in better weather, and asks that you not make
                          him do it again."
  sign.windward_windgap  "The stair ends here; the wind goes on. Only a kin
                          that rides the thermals crosses the gap." (sincere —
                          the boundary gate's why + come-back; also the
                          to_stair_ii blocked_ref)

audit_flow WAIVER — the void chasm cells become standable pockets only under
starreach (late-game; every gift is held in the audit), so any dead-end/screen
WARN inside the chasm is a starreach curiosity, not a route fail.

Run:  ./venv/bin/python tools/maps/build_windward_stair_i.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 24, 40
rng = random.Random(61)
owed: list[str] = []

# ---- terrain presence grids --------------------------------------------------------
glacier = mk.make_grid(W, H)    # high crag walls + the upper banks (snow register)
cliff = mk.make_grid(W, H)      # the lower banks + lower side walls (stone register)
void = mk.make_grid(W, H)       # the wind-gap chasm at the head of the climb
snowpatch = mk.make_grid(W, H)  # the snowline gradient (foot + mid-leg dustings)
snowtrail = mk.make_grid(W, H)  # the trodden lane (snow context)
frosttuft = mk.make_grid(W, H)  # the encounter tile (bands + ledge pockets)

# SIDE BORDERS: stone faces below the snowline, glacier above (the gradient)
mk.rect(cliff, W, H, 0, 26, 1, H - 1)
mk.rect(cliff, W, H, 22, 26, 23, H - 1)
mk.rect(glacier, W, H, 0, 0, 1, 25)
mk.rect(glacier, W, H, 22, 0, 23, 25)

# BOTTOM BORDER: glacier crag with the Galehigh gap at cols 14-15 (seam: the
# snowtrail continues Galehigh's top-band lane tile-for-tile)
mk.rect(glacier, W, H, 0, 38, W - 1, H - 1)
for y in (38, 39):
    glacier[y * W + 14] = 0
    glacier[y * W + 15] = 0

# TOP: glacier rim + THE WIND-GAP void chasm (rows 2-4), the 2-wide walkable
# promontory tongue at x8-9 rows 3-4 jutting into it
mk.rect(glacier, W, H, 0, 0, W - 1, 1)
mk.rect(void, W, H, 2, 2, 21, 4)
for y in (3, 4):
    void[y * W + 8] = 0
    void[y * W + 9] = 0

# THE FOUR BANKS (S-bend rule: each bank folds the path; gap = the climb,
# cleared 3-wide segment + ledge deco = the one-way hop home)
mk.rect(cliff, W, H, 2, 32, 21, 33)      # bank A — gap W (x3-4), ledge x6-8
for x in (3, 4, 6, 7, 8):
    cliff[32 * W + x] = 0
    cliff[33 * W + x] = 0
mk.rect(cliff, W, H, 2, 26, 21, 27)      # bank B — gap E (x18-19), ledge x9-11
for x in (18, 19, 9, 10, 11):
    cliff[26 * W + x] = 0
    cliff[27 * W + x] = 0
mk.rect(glacier, W, H, 2, 19, 21, 20)    # bank C — gap W (x5-6), ledge x14-16
for x in (5, 6, 14, 15, 16):
    glacier[19 * W + x] = 0
    glacier[20 * W + x] = 0
mk.rect(glacier, W, H, 2, 13, 21, 14)    # bank D — gap E (x16-17), ledge x8-10
for x in (16, 17, 8, 9, 10):
    glacier[13 * W + x] = 0
    glacier[14 * W + x] = 0

# ---- the snowline gradient ---------------------------------------------------------
# Stair I is STONE — snow arrives only at the top leg (the II crags carry the
# first real snow, walkthrough beat 3). snowpatch (snow-over-GRASS) is used
# ONLY on grass context: the Galehigh entry seam, so the gap continues N1's
# snowline top band tile-for-tile (§2b rule 6).
mk.blob(snowpatch, W, H, 14.5, 38.0, 4.0, 2.2)
mk.blob(snowpatch, W, H, 13.0, 37.0, 2.2, 1.2)

# ---- the lane (context-correct: path on grass, snowtrail on snow) ------------------
path = mk.make_grid(W, H)
mk.vline(snowtrail, W, H, 14, 36, 39)               # the entry throat (snow seam)
mk.vline(snowtrail, W, H, 15, 36, 39)
mk.vline(path, W, H, 14, 34, 35)
mk.vline(path, W, H, 15, 34, 35)
mk.hline(path, W, H, 35, 4, 15)                     # leg 1 bend west (grass)
mk.hline(path, W, H, 36, 4, 13)
mk.vline(snowtrail, W, H, 16, 8, 12)                # leg 5: bank-D gap up (snow)
mk.vline(snowtrail, W, H, 17, 8, 12)
mk.hline(snowtrail, W, H, 7, 9, 17)                 # plateau bend to the tongue
mk.hline(snowtrail, W, H, 8, 9, 17)
mk.vline(snowtrail, W, H, 8, 3, 7)                  # the promontory approach
mk.vline(snowtrail, W, H, 9, 3, 7)

# ---- encounter terrain -------------------------------------------------------------
# optional ledge pockets (rate 0.11): leg 2 east shelf, leg 4 mid shelf, and
# the SE foot verge (pays the off-lane pocket east of the entry — §3a rule 4)
mk.blob(frosttuft, W, H, 10.5, 30.0, 3.0, 1.4)
mk.blob(frosttuft, W, H, 10.0, 16.5, 3.2, 1.4)
mk.blob(frosttuft, W, H, 19.0, 35.5, 2.0, 1.3)
# MANDATORY crossings (§11 r7): full-corridor bands, the lane paused through
pt.mandatory_band(frosttuft, snowtrail, W, H, y0=23, y1=24, x0=2, x1=21)   # leg 3
pt.mandatory_band(frosttuft, snowtrail, W, H, y0=10, y1=11, x0=2, x1=21)   # leg 5

# ---- precedence (structure wins; lane wins over ground dusting) --------------------
for i in range(W * H):
    if glacier[i] or cliff[i] or void[i]:
        snowpatch[i] = 0
        snowtrail[i] = 0
        frosttuft[i] = 0
        path[i] = 0
    if snowtrail[i] or path[i]:
        snowpatch[i] = 0
        frosttuft[i] = 0
    if frosttuft[i]:
        snowpatch[i] = 0

# ---- base: the climb gradient (grass -> scree -> snow) -----------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
sc = [gid("scree0"), gid("scree1"), gid("scree2")]
sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = mk.make_grid(W, H)
for y in range(H):
    for x in range(W):
        if y >= 34:
            base[y * W + x] = rng.choice(gg) if rng.random() < 0.5 else gg[0]
        elif y >= 13:
            base[y * W + x] = rng.choice(sc) if rng.random() < 0.55 else sc[0]
        else:
            base[y * W + x] = rng.choice(sn) if rng.random() < 0.5 else sn[0]

terrain_layers = [
    {"name": "t_snowpatch", "role": "terrain", "terrain": "snowpatch",
     "set": "vesper_overworld_set", "depth": 0, "data": snowpatch},
    {"name": "t_snowtrail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": snowtrail},
    {"name": "t_path", "role": "terrain", "terrain": "path",
     "set": "vesper_overworld_set", "depth": 0, "data": path},
    {"name": "t_frosttuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": frosttuft},
    {"name": "t_void", "role": "terrain", "terrain": "void",
     "set": "vesper_overworld_set", "depth": 0, "data": void},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
    {"name": "t_cliff", "role": "terrain", "terrain": "cliff",
     "set": "vesper_overworld_set", "depth": 0, "data": cliff},
]

m: dict = {
    "id": "windward_stair_i", "display_name": "Windward Stair",
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

# ---- one-way ledge segments on every bank (the return compressors) -----------------
pt.ledge_run(deco, W, H, 32, 6, 8, rng, family="scree")    # bank A hop
pt.ledge_run(deco, W, H, 26, 9, 11, rng, family="scree")   # bank B hop
pt.ledge_run(deco, W, H, 19, 14, 16, rng, family="scree")  # bank C hop
pt.ledge_run(deco, W, H, 13, 8, 10, rng, family="snow")    # bank D hop

# ---- warps (graph.ts ids verbatim) -------------------------------------------------
m["warps"] += [
    # SOUTH <-> galehigh_terraces (the N1 handshake: their `to_stair` lands at
    # our (14,38)/(15,38); we land one tile inside their gate at (14,1)/(15,1))
    {"id": "to_galehigh", "at": {"tx": 14, "ty": 39}, "trigger": "step_on",
     "to_map": "galehigh_terraces", "to": {"tx": 14, "ty": 1}, "facing": "down",
     "transition": "fade"},
    {"id": "to_galehigh_e", "at": {"tx": 15, "ty": 39}, "trigger": "step_on",
     "to_map": "galehigh_terraces", "to": {"tx": 15, "ty": 1}, "facing": "down",
     "transition": "fade"},
    # THE WIND-GAP -> windward_stair_ii (graph `to_stair_ii`, Updraft-gated —
    # the first place the Gift is REQUIRED; both tongue-tip tiles warp)
    {"id": "to_stair_ii", "at": {"tx": 8, "ty": 3}, "trigger": "step_on",
     "to_map": "windward_stair_ii", "to": {"tx": 13, "ty": 21}, "facing": "up",
     "requires_ability": "updraft_kite",
     "blocked_ref": "sign.windward_windgap", "transition": "fade"},
    {"id": "to_stair_ii_e", "at": {"tx": 9, "ty": 3}, "trigger": "step_on",
     "to_map": "windward_stair_ii", "to": {"tx": 14, "ty": 21}, "facing": "up",
     "requires_ability": "updraft_kite",
     "blocked_ref": "sign.windward_windgap", "transition": "fade"},
]

# ---- objects: cairns at the bends, lamps by the lane, the updraft column -----------
m["objects"] += [
    # wind-cairn waymarkers (bespoke) — one per bend the eye needs
    {"id": "cairn_foot", "sprite": "windward_cairn", "at": {"tx": 4, "ty": 32},
     "w": 2, "h": 3, "overhang": 2, "walk_under": False},
    {"id": "cairn_mid", "sprite": "windward_cairn", "at": {"tx": 17, "ty": 24},
     "w": 2, "h": 3, "overhang": 2, "walk_under": False},
    {"id": "cairn_kettle", "sprite": "windward_cairn", "at": {"tx": 4, "ty": 21},
     "w": 2, "h": 3, "overhang": 2, "walk_under": False},
    {"id": "cairn_head", "sprite": "windward_cairn", "at": {"tx": 5, "ty": 5},
     "w": 2, "h": 3, "overhang": 2, "walk_under": False},
    {"id": "cairn_head_e", "sprite": "windward_cairn", "at": {"tx": 18, "ty": 5},
     "w": 2, "h": 3, "overhang": 2, "walk_under": False},
    # the updraft column rising out of the chasm beside the tongue
    {"id": "windgap_updraft", "sprite": "windward_updraft", "at": {"tx": 10, "ty": 1},
     "w": 2, "h": 3, "overhang": 3, "solid": False, "walk_under": True},
    # THE REST SHELF (leg 3, ~halfway): the crag-tender's lit kettle camp,
    # a wrecked kite beside it, the lamp-post tucked against bank C — with
    # the wind-cairn west, a sheltered clearing the climb pauses in
    {"id": "kettle_camp", "sprite": "pale_vault_camp_lit", "at": {"tx": 8, "ty": 21},
     "w": 3, "h": 2},
    {"id": "kettle_kite_wreck", "sprite": "windward_kite_wreck",
     "at": {"tx": 13, "ty": 21}, "w": 2, "h": 2},
    # lamp posts beside (never on) the lane
    {"id": "lamp_foot", "sprite": "tinderwick_lamp_post", "at": {"tx": 12, "ty": 32},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_kettle", "sprite": "tinderwick_lamp_post", "at": {"tx": 11, "ty": 20},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
    {"id": "lamp_head", "sprite": "tinderwick_lamp_post", "at": {"tx": 13, "ty": 5},
     "w": 1, "h": 3, "overhang": 2, "walk_under": True},
]

# ---- signs -------------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="windward_marker", at=(16, 25))   # THE wry line
owed += pt.sign(m, deco, W, sid="windward_windgap", at=(6, 6))    # sincere gate

# ---- trainer beats (sight trainers ARE geometry, lv ~34-36 — N5 authors) -----------
owed += pt.trainer_beat(m, tid="windward_craghand", at=(19, 30), facing="left",
                        sight=4, sprite="npc_man")
owed += pt.trainer_beat(m, tid="windward_galewatch", at=(18, 17), facing="left",
                        sight=4, sprite="npc_woman")

# ---- the crag-tender's kettle camp (N1 quest, leg 3) -------------------------------
# kite-maker flag-pair pattern: ask -> (herb picked on Galehigh) -> done -> after
m["npcs"] += [
    {"id": "crag_tender_ask", "at": {"tx": 7, "ty": 22}, "facing": "down",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "script.kettle_quest",
     "hidden_when_flag": "flag:picked_ledge_herb"},
    {"id": "crag_tender_done", "at": {"tx": 7, "ty": 22}, "facing": "down",
     "sprite": "npc_old_woman", "movement": "static",
     "dialogue_ref": "script.kettle_done",
     "requires_flag": "flag:picked_ledge_herb",
     "hidden_when_flag": "flag:q_north_kettle_done"},
    {"id": "crag_tender_after", "at": {"tx": 7, "ty": 22}, "facing": "down",
     "sprite": "npc_old_woman", "movement": "look_around",
     "dialogue_ref": "npc.windward_crag_tender",
     "requires_flag": "flag:q_north_kettle_done"},
    # a descending wind-pilgrim on the foot leg (ambient warmth, Arc D voice)
    {"id": "wind_pilgrim", "at": {"tx": 8, "ty": 37}, "facing": "right",
     "sprite": "npc_man", "movement": "look_around",
     "dialogue_ref": "npc.windward_pilgrim"},
]
owed += ["script.kettle_quest (sets flag:q_north_kettle)",
         "script.kettle_done (gives the Warm Flask; sets "
         "flag:q_north_kettle_done)",
         "npc.windward_crag_tender", "npc.windward_pilgrim"]

# ---- caches (variety rule: consumable + loose wicks + a valuable) ------------------
owed += pt.cache(m, cid="windward_balm", at=(20, 31))    # consumable, leg-2 pocket
owed += pt.cache(m, cid="windward_wicks", at=(3, 37))    # loose wicks, foot corner
owed += pt.cache(m, cid="windward_shard", at=(4, 9))     # valuable, behind the high band

# ---- encounters (band 34-36; the foot verge 32-34 — see module docstring) ----------
TABLE = [{"kin_id": 89, "weight": 35, "min_level": 34, "max_level": 36},
         {"kin_id": 45, "weight": 25, "min_level": 34, "max_level": 36},
         {"kin_id": 98, "weight": 20, "min_level": 34, "max_level": 35},
         {"kin_id": 95, "weight": 10, "min_level": 35, "max_level": 36},
         # N5 reconcile: Chillpip (#77, Frost base) — the chillpip -> crystarn
         # -> glacitern line had no wild placement; the first cold ledges are
         # where the Frost edge starts (pairs with Glacewing's low weight)
         {"kin_id": 77, "weight": 10, "min_level": 34, "max_level": 35}]
# the SE foot verge (the FIRST grass off the Galehigh gap): one band gentler,
# the common Storm-country lines only — no Frost foreshadows down here
TABLE_VERGE = [{"kin_id": 89, "weight": 40, "min_level": 32, "max_level": 34},
               {"kin_id": 45, "weight": 35, "min_level": 32, "max_level": 34},
               {"kin_id": 98, "weight": 25, "min_level": 32, "max_level": 34}]
band_grid = mk.make_grid(W, H)
patch_grid = mk.make_grid(W, H)
verge_grid = mk.make_grid(W, H)
for i in range(W * H):
    if frosttuft[i]:
        y = i // W
        if y in (23, 24, 10, 11):
            band_grid[i] = 1
        elif y >= 34:                     # the foot verge rows (grass context)
            verge_grid[i] = 1
        else:
            patch_grid[i] = 1
m["encounters"] += pt.zones_from_grid(verge_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE_VERGE, id_prefix="verge")
m["encounters"] += pt.zones_from_grid(patch_grid, W, H, terrain="tall_grass",
                                      rate=0.11, table=TABLE, id_prefix="ledge")
m["encounters"] += pt.zones_from_grid(band_grid, W, H, terrain="tall_grass",
                                      rate=0.05, table=TABLE, id_prefix="crossing")

# ---- scatter + boulders ------------------------------------------------------------
covered = {(x, y) for y in range(H) for x in range(W)
           if any(g[y * W + x] for g in (glacier, cliff, void, snowpatch,
                                         snowtrail, path, frosttuft))}
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
avoid = covered | object_cells | point_cells
mk.scatter_decor(deco, base, W, H, rng, density=0.15, avoid=avoid)
for (x, y) in [(20, 36), (6, 30), (13, 29), (3, 24), (19, 16), (5, 15),
               (12, 9), (19, 8), (3, 11), (20, 22)]:
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
