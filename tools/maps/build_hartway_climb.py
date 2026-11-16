#!/usr/bin/env python3
"""
The Hartway (hartway_climb) — the climbers' road over THE HARTSHOULDER, the last
pitch of the Windward pass: from the high crags (windward_stair_ii) up and over to
Pale Vault (2026-11, docs/world/walkthrough/12-the-hartway.md). MAIN PATH, and it
SLOTS INTO the pass by its edges: the road out of the crags comes round the shoulder
and walks in at the foot (west edge, rows 45-46); the Seat's trail walks out to Pale
Vault at the top (west edge, rows 9-10). No steps, no portal, no closed road.

A STORY climb, walked with GREG (content/regions/hartway.ts): nobody goes up alone,
Greg goes first on the ridges, and once a ridge is behind you he fixes a ROPE LADDER
down the cliff so nobody has to do that again.

Tiers, bottom to top (south = lower, the facekit convention):
  T0  the Landing   (rows 44-47)  the road in from the crags (west edge, rows 45-46)
  A   band A        (rows 39-43)  ROPE LADDER 1 at x8 — `flag:hart_ladder_1`
      THE STAIRCASE               a one-wide rock rib through the gulf (x19-27)
  T1  the Shelf     (rows 33-38)  the walkers' camp (a rest point)
  B   band B        (rows 28-32)  the iron ladder at x5 (always there);
                                  ROPE LADDER 2 at x24 — `flag:hart_ladder_2`
  U   the High Shelf (rows 14-27) west (x2-7) and east (x21-27) of THE GULF;
      THE WHITEBACK               the snow ridge across it (the story ridge)
  C   band C        (rows 12-13)  the safe trail's gap at x24-25
  S   THE SEAT      (rows 2-11)   the bench, the bothy the kin took back, the view,
                                  and the safe trail west into Pale Vault (rows 9-10)

THE RIDGES CANNOT BE WALKED. The Staircase and the Whiteback are solid `gulf` cells
wearing a pinned CREST tile (hartway_set `crest_*`): a two-pixel line of snow on a fin
of rock, far narrower than a pair of boots. The only way along one is the `edge`
cutscene op, roped to Greg — so without him the mountain stops you at the first ridge,
and nobody needs a gate. The two rope ladders are flag-gated `spans` with a matching
flag-gated `hartway_rope_ladder` object: art and collision appear together the moment
Greg kicks the ladder over the edge, and from then on nobody edges a ridge again.

  ladders hang on `flag:hart_rope_1/2` — DERIVED (FlagStore ANY_OF): Greg's own
  `flag:hart_ladder_n`, OR any milestone from beyond the pass. A save that crossed
  before the Hartway existed finds the ladders already fixed (never locked out), and
  can still fetch Greg from Galehigh to hear the story.

HANDSHAKES (edge links — the map PLACES in world_geometry):
  west edge rows 45-46  <->  windward_stair_ii east edge (37,16)/(37,17)
  west edge rows 9-10   <->  pale_vault_glacier east edge (31,10)/(31,11)

Run:  python3 tools/maps/build_hartway_climb.py [--show]
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
import warp_markers as wm
from mapkit import gid

W, H = 30, 52
rng = random.Random(1911)
owed: list[str] = []

HART_REF = mk.register_tileset(
    "hartway_set", index=mk.REPO / "assets/tilesets/hartway/hartway_set.index.json")

c = fk.Canvas(W, H, ".")
c.rect(0, 0, W - 1, 1, "#").rect(0, 0, 1, H - 1, "#").rect(28, 0, 29, H - 1, "#")
c.rect(0, 48, W - 1, H - 1, "#")

# band A + rope ladder 1 (gated: cells stay band; the span + object come below)
c.band(2, 27, 39, lip=2, face=3)
# band B + the iron ladder (always there)
c.band(2, 27, 28, lip=2, face=3)
c.ladder(5, 28, 32)
# band C: a low wall under the Seat's two ends, the safe trail's gap at x24-25. Between
# them the Seat's south edge IS the drop: the bench looks straight out over the gulf.
c.rect(2, 12, 27, 13, "#")

# THE GULF under the Staircase (east, through band A) and under the Whiteback (which
# runs on up to the Seat's lip). Ragged outlines, never ruled boxes; the ridges are a
# white crest (plain snow + footprints), not a paved road.
c.rect(19, 38, 27, 45, "G")
c.rect(8, 12, 20, 27, "G")
c.put([(8, 14), (9, 14), (19, 14), (20, 14), (20, 15), (8, 26), (8, 27), (9, 27), (20, 26),
       (20, 27), (8, 17), (20, 23)], ".")              # snow bites back into the rim
c.put([(7, 24), (7, 25)], "G")                         # ...and the drop bites into the shelf
# The two ridges, as the cells they cross IN ORDER, shelf to shelf (first and last are
# the shelf tiles they leave from and land on). They stay gulf: see `crest` below.
STAIRCASE = [(21, 46), (21, 45), (21, 44), (21, 43), (22, 43), (23, 43), (23, 42), (23, 41),
             (24, 41), (25, 41), (25, 40), (25, 39), (25, 38), (25, 37)]
WHITEBACK = ([(7, 22)] + [(x, 22) for x in range(8, 14)] + [(13, 21)]
             + [(x, 20) for x in range(13, 22)])

# ---- the trodden line ----------------------------------------------------------------
c.rect(0, 45, 7, 46, "=").rect(8, 46, 21, 46, "=").rect(8, 44, 8, 46, "=")        # T0: in by the west edge
c.rect(5, 36, 25, 36, "=").rect(25, 36, 25, 37, "=").rect(5, 33, 5, 36, "=")     # T1
c.rect(8, 36, 8, 38, "=").rect(24, 33, 24, 36, "=")
c.rect(5, 22, 7, 22, "=").rect(5, 22, 5, 27, "=")                                # U-west
c.rect(21, 20, 25, 20, "=").rect(24, 12, 25, 27, "=")                            # U-east + gap
c.rect(0, 9, 3, 10, "=").rect(4, 9, 25, 9, "=").rect(24, 9, 25, 11, "=")         # the Seat + the trail out west

# ---- frost-tuft (the encounter tile) ---------------------------------------------------
c.rect(2, 47, 7, 47, '"').rect(10, 44, 13, 45, '"')   # T0: under the lane, and a bank by the pegs
c.rect(12, 33, 17, 34, '"')                   # T1, behind the camp
c.rect(14, 37, 18, 38, '"')                   # T1 south lip
c.rect(2, 14, 4, 19, '"')                     # the high shelf, west
c.rect(26, 14, 27, 18, '"')                   # the high shelf, east
c.rect(19, 2, 26, 5, '"')                     # THE HIGH GRASS above the Seat
# a few boulders on open ground
c.put([(3, 44), (24, 47), (3, 37), (20, 34), (3, 25), (22, 24), (14, 4), (3, 11)], "o")
rows = c.rows()
prows = [r.replace("G", " ") for r in rows]   # facekit ignores the gulf (its own terrain)

m: dict = {
    "id": "hartway_climb", "display_name": "The Hartway",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref(), HART_REF],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/windward-stair-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/windward-stair-a.webp",
        "assets/backgrounds/battle/windward-stair-b.webp",
    ],
    "ambience": {
        "particles": [{"kind": "snow", "density": 0.5}, {"kind": "motes", "density": 0.5}],
        "mist": {"color": "#e6eef8", "alpha": 0.08, "speed": 9},
        "footprints": "all",
        "starfall": {"min_s": 30, "max_s": 70},
        "birds": {"kind": "bird", "flyover": True},
        "sound_bed": "amb-wind",
    },
}
deco = mk.make_grid(W, H)
above = mk.make_grid(W, H)
pin: dict = {}
g = fk.paint(m, prows, deco=deco, above=above, pin=pin, face="ice", ledge="snow", rng=rng)
gulf = mk.make_grid(W, H)
for y in range(H):
    for x in range(W):
        if rows[y][x] == "G":
            gulf[y * W + x] = 1

# ---- the edges: the road in at the foot, the trail out at the top -------------------------
for k, (hy, sy) in enumerate(((45, 16), (46, 17))):
    m["warps"].append({"id": "to_crags" + ("_s" if k else ""), "at": {"tx": 0, "ty": hy},
                       "trigger": "step_on", "to_map": "windward_stair_ii",
                       "to": {"tx": 36, "ty": sy}, "facing": "left", "transition": "fade"})
for k, (hy, gy) in enumerate(((9, 10), (10, 11))):
    m["warps"].append({"id": "to_vault" + ("_s" if k else ""), "at": {"tx": 0, "ty": hy},
                       "trigger": "step_on", "to_map": "pale_vault_glacier",
                       "to": {"tx": 30, "ty": gy}, "facing": "left", "transition": "fade"})

# ---- THE CREST: one pinned tile per ridge cell (solid; crossed only by the `edge` op) ------
def crest(path):
    d = {(0, -1): "n", (0, 1): "s", (-1, 0): "w", (1, 0): "e"}
    for i in range(1, len(path) - 1):
        (x, y) = path[i]
        ends = "".join(sorted(d[(q[0] - x, q[1] - y)] for q in (path[i - 1], path[i + 1])))
        name = {"ns": "crest_ns", "ew": "crest_ew", "en": "crest_ne", "nw": "crest_nw",
                "es": "crest_se", "sw": "crest_sw"}[ends]
        if i == 1 or i == len(path) - 2:                 # an end: drawn over the gulf's rim
            shelf = path[0] if i == 1 else path[-1]
            name = {"n": "crest_ns_head", "s": "crest_ns_foot", "w": "crest_ew_west",
                    "e": "crest_ew_east"}[d[(shelf[0] - x, shelf[1] - y)]]
        assert rows[y][x] == "G", (x, y)
        pin[(x, y)] = name


crest(STAIRCASE)
crest(WHITEBACK)

# ---- THE ROPE LADDERS (Greg fixes each once its ridge is behind you) -------------------
for n, (x, y0) in ((1, (8, 39)), (2, (24, 28))):
    flag = f"flag:hart_rope_{n}"
    m.setdefault("spans", []).append({"id": f"rope_ladder_{n}", "kind": "ladder", "axis": "v",
                                      "rect": {"tx": x, "ty": y0, "w": 1, "h": 5},
                                      "requires_flag": flag})
    m["objects"].append({"id": f"rope_ladder_{n}", "sprite": "hartway_rope_ladder",
                         "at": {"tx": x, "ty": y0}, "w": 1, "h": 5, "solid": False,
                         "requires_flag": flag})

# ---- GREG, stage by stage (flag pairs; one Greg on the map at a time) ------------------
def greg(gid_: str, at, facing, ref, req=None, hide=None):
    n = {"id": gid_, "at": {"tx": at[0], "ty": at[1]}, "facing": facing, "sprite": "greg",
         "movement": "static", "dialogue_ref": ref}
    if req:
        n["requires_flag"] = req
    if hide:
        n["hidden_when_flag"] = hide
    m["npcs"].append(n)


# the foot: Hollis the rope-warden keeps the Landing; Greg waits by her once he's said yes
m["npcs"] += [
    {"id": "hollis", "at": {"tx": 14, "ty": 45}, "facing": "down", "sprite": "pass_walker",
     "movement": "static", "dialogue_ref": "script.hartway_hollis"},
    {"id": "greg_foot", "at": {"tx": 15, "ty": 45}, "facing": "down", "sprite": "greg",
     "movement": "static", "dialogue_ref": "script.greg_rope_up",
     "requires_flag": "flag:greg_found", "hidden_when_flag": "flag:greg_roped"},
]
owed += ["script.hartway_hollis", "script.greg_rope_up"]
greg("greg_t0", (22, 46), "left", "script.greg_t0", "flag:greg_roped", "flag:hart_p1_done")
greg("greg_t1", (26, 36), "left", "script.greg_wait", "flag:hart_p1_done", "flag:hart_ladder_1")
greg("greg_t1b", (6, 34), "left", "script.greg_t1b", "flag:hart_ladder_1", "flag:hart_b1_done")
greg("greg_uw", (6, 23), "right", "script.greg_uw", "flag:hart_b1_done", "flag:hart_p2_done")
greg("greg_ue", (23, 21), "left", "script.greg_wait", "flag:hart_p2_done", "flag:hart_ladder_2")
greg("greg_ue2", (25, 26), "up", "script.greg_ue2", "flag:hart_ladder_2", "flag:hart_b3_begun")
greg("greg_seat", (22, 10), "right", "script.greg_wait", "flag:hart_b3_begun", "flag:hart_b3_done")
greg("greg_bench", (15, 10), "down", "script.greg_bench", "flag:hart_b3_done")
owed += ["script.greg_t0", "script.greg_wait", "script.greg_t1b", "script.greg_uw",
         "script.greg_ue2", "script.greg_bench"]


def beat(tid: str, cells, ref: str, req=None, hide=None):
    """A story band: one step_on cutscene tile per cell of the cut."""
    for k, (x, y) in enumerate(cells):
        t = {"id": tid if k == 0 else f"{tid}_{k}", "kind": "cutscene",
             "at": {"tx": x, "ty": y}, "activation": "step_on", "ref": ref}
        if req:
            t["requires_flag"] = req
        if hide:
            t["hidden_when_flag"] = hide
        m["triggers"].append(t)
    owed.append(ref)


# the foot of the Staircase: with Greg, the crossing; without him, the warden's voice
beat("staircase", [(21, 46)], "script.hart_staircase", "flag:greg_roped", "flag:hart_p1_done")
beat("staircase_alone", [(21, 46)], "script.hartway_gate", None, "flag:greg_roped")
beat("ladder_one", [(25, 37)], "script.hart_ladder_one", "flag:hart_p1_done", "flag:hart_ladder_1")
beat("chimney", [(5, 33)], "script.hart_chimney", "flag:hart_ladder_1", "flag:hart_b1_done")
beat("whiteback", [(7, 22)], "script.hart_whiteback", "flag:hart_b1_done", "flag:hart_p2_done")
beat("cornice", [(24, 11), (25, 11)], "script.hart_cornice", "flag:hart_ladder_2", "flag:hart_b3_done")

# ---- T1: the walkers' camp (a rest point) ----------------------------------------------
m["objects"].append({"id": "camp", "sprite": "hushfrost_walker_camp", "at": {"tx": 8, "ty": 32},
                     "w": 4, "h": 3, "overhang": 1})
for x in (8, 9, 10, 11):
    m["triggers"].append({"id": f"camp_rest_{x}", "kind": "script", "at": {"tx": x, "ty": 35},
                          "activation": "interact", "ref": "script.hartway_camp"})
owed.append("script.hartway_camp")

# ---- THE SEAT ---------------------------------------------------------------------------
m["objects"] += [
    {"id": "ruin_hut", "sprite": "hartway_ruin_hut", "at": {"tx": 8, "ty": 5}, "w": 4, "h": 4,
     "overhang": 2},
    {"id": "spyglass", "sprite": "windward_spyglass", "at": {"tx": 20, "ty": 10}, "w": 2, "h": 2,
     "overhang": 1, "walk_under": True},
    {"id": "bench", "sprite": "hartway_bench", "at": {"tx": 13, "ty": 10}, "w": 2, "h": 1},
    {"id": "cairn_seat", "sprite": "windward_cairn", "at": {"tx": 17, "ty": 9}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "flags_seat", "sprite": "windward_prayer_flags", "at": {"tx": 4, "ty": 3}, "w": 4, "h": 2,
     "overhang": 2, "walk_under": True, "solid": False},
]
for x in (13, 14):
    m["triggers"].append({"id": f"seat_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 10},
                          "activation": "interact", "ref": "script.hart_seat"})
m["triggers"].append({"id": "hut_door", "kind": "sign", "at": {"tx": 10, "ty": 9},
                      "activation": "interact", "ref": "sign.hartway_hut"})
owed += ["script.hart_seat", "sign.hartway_hut"]

# the bothy belongs to the mountain's kin now (ambient: greetable, never colliding)
for aid, kin, (x, y), r in [("amb_hut_a", 77, (12, 7), 1), ("amb_hut_b", 88, (3, 6), 2),
                            ("amb_seat", 80, (15, 7), 1), ("amb_shelf", 80, (16, 35), 2),
                            ("amb_high", 77, (3, 21), 1)]:
    m["npcs"].append({"id": aid, "at": {"tx": x, "ty": y}, "facing": "down",
                      "sprite": f"kin_{kin}_overworld", "movement": "wander",
                      "ambient": True, "wander_radius": r})

# ---- signs / caches ----------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="hartway_staircase", at=(18, 47))
owed += pt.sign(m, deco, W, sid="hartway_whiteback", at=(4, 23))
owed += pt.sign(m, deco, W, sid="hartway_seat", at=(23, 8))
owed += pt.sign(m, deco, W, sid="hartway_foot", at=(6, 44))
owed += pt.sign(m, deco, W, sid="hartway_top", at=(5, 8))
owed += pt.cache(m, cid="hartway_shelf", at=(27, 34))
owed += pt.cache(m, cid="hartway_high", at=(2, 16))
owed += pt.cache(m, cid="hartway_seat", at=(26, 3))       # in the high grass: a detour that pays
# the rope ladders' pegs, before the ladders: a seeded lock, not a false lead
owed += pt.sign(m, deco, W, sid="hartway_pegs", at=(9, 44))
m["triggers"].append({"id": "sign_hartway_pegs_high", "kind": "sign", "at": {"tx": 26, "ty": 26},
                      "activation": "interact", "ref": "sign.hartway_pegs"})
deco[26 * W + 26] = gid("sign")

# ---- dressing (a landmark on every screen) ------------------------------------------------
m["objects"] += [
    {"id": "pine_landing", "sprite": "windward_bent_pine", "at": {"tx": 16, "ty": 43}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "pine_t1", "sprite": "hushfrost_snow_pine_big", "at": {"tx": 19, "ty": 32}, "w": 3, "h": 4,
     "overhang": 3, "walk_under": True},
    {"id": "rocks_t1", "sprite": "hushfrost_snow_boulders", "at": {"tx": 12, "ty": 37}, "w": 2, "h": 2},
    {"id": "dead_uw", "sprite": "hushfrost_dead_tree", "at": {"tx": 2, "ty": 23}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "struck_uw", "sprite": "windward_struck_rock", "at": {"tx": 6, "ty": 18}, "w": 2, "h": 2},
    {"id": "outcrop_uw", "sprite": "hushfrost_rock_outcrop_a", "at": {"tx": 5, "ty": 15}, "w": 3, "h": 2},
    {"id": "pine_ue", "sprite": "windward_bent_pine", "at": {"tx": 26, "ty": 21}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "woodpile_t1", "sprite": "pale_vault_woodpile", "at": {"tx": 22, "ty": 34}, "w": 2, "h": 2},
    {"id": "flags_ue", "sprite": "windward_prayer_flags", "at": {"tx": 21, "ty": 16}, "w": 4, "h": 2,
     "overhang": 2, "walk_under": True, "solid": False},
    {"id": "drift_ue", "sprite": "hushfrost_snowdrift", "at": {"tx": 21, "ty": 24}, "w": 3, "h": 2},
    {"id": "pine_seat", "sprite": "hushfrost_snow_pine", "at": {"tx": 2, "ty": 2}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "rocks_seat", "sprite": "hushfrost_snow_boulders", "at": {"tx": 5, "ty": 6}, "w": 2, "h": 2},
]

# ---- encounters (the high crags' own table, 35-36; night/day pairs) ------------------------
def T(*r):
    return [{"kin_id": k, "weight": w_, "min_level": lo, "max_level": hi} for (k, w_, lo, hi) in r]


NIGHT = T((95, 25, 35, 36), (89, 25, 35, 36), (45, 20, 35, 36), (98, 20, 35, 36), (74, 10, 35, 36))
DAY = T((95, 25, 57, 63), (89, 20, 56, 62), (45, 15, 56, 62), (98, 15, 57, 62), (74, 10, 56, 62),
        (91, 15, 57, 64))
# THE HIGH GRASS above the Seat: the herd leaves its fawns here
FAWN_NIGHT = NIGHT + T((120, 15, 36, 36))
FAWN_DAY = DAY + T((120, 12, 57, 63))
crag = mk.make_grid(W, H)
grass = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        (grass if i // W <= 5 else crag)[i] = 1
m["encounters"] += fk.night_day(
    pt.zones_from_grid(crag, W, H, terrain="tall_grass", rate=0.09, table=NIGHT, id_prefix="crag"), DAY)
m["encounters"] += fk.night_day(
    pt.zones_from_grid(grass, W, H, terrain="tall_grass", rate=0.10, table=FAWN_NIGHT,
                       id_prefix="pasture"), FAWN_DAY)

sn = [gid("snow0"), gid("snow1"), gid("snow2"), gid("snow3")]
base = [rng.choice(sn) if rng.random() < 0.5 else sn[0] for _ in range(W * H)]

m["layers"] = [
    {"name": "base", "role": "base", "depth": 0, "data": base},
    {"name": "t_gulf", "role": "terrain", "terrain": "gulf",
     "set": "hartway_set", "depth": 0, "data": gulf},
    {"name": "t_trail", "role": "terrain", "terrain": "snowtrail",
     "set": "vesper_overworld_set", "depth": 0, "data": g["road"]},
    {"name": "t_tuft", "role": "terrain", "terrain": "frosttuft",
     "set": "vesper_overworld_set", "depth": 0, "data": g["tuft"]},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": g["cliff"]},
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": above},
]

if __name__ == "__main__":
    import sys
    if "--show" in sys.argv:
        print("\n".join(f"{y:3d} {r}" for y, r in enumerate(rows)))
    # three far-off lights in the drop (deliberate, never scattered)
    pin.update({(11, 17): "gulf_town", (17, 25): "gulf_lane", (26, 44): "gulf_lane"})
    ok = mk.finalize(m, scale=3, pin_base=pin)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
