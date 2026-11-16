#!/usr/bin/env python3
"""
The Hartway (hartway_climb) — the old climbers' road up THE HARTSHOULDER, the
mountain behind Wayward Rise (2026-11, docs/world/walkthrough/12-the-hartway.md).

A STORY climb, walked with GREG (content/regions/hartway.ts): nobody goes up alone,
Greg goes first on the ridges, and once a ridge is behind you he fixes a ROPE LADDER
down the cliff so nobody has to do that again.

Tiers, bottom to top (south = lower, the facekit convention):
  T0  the Landing   (rows 44-47)  the steps up from hartway_foot land at (14,47)
  A   band A        (rows 39-43)  ROPE LADDER 1 at x8 — `flag:hart_ladder_1`
      THE STAIRCASE               a one-wide rock rib through the gulf (x19-27)
  T1  the Shelf     (rows 33-38)  the walkers' camp (a rest point)
  B   band B        (rows 28-32)  the iron ladder at x5 (always there);
                                  ROPE LADDER 2 at x24 — `flag:hart_ladder_2`
  U   the High Shelf (rows 14-27) west (x2-7) and east (x21-27) of THE GULF;
      THE WHITEBACK               the snow ridge across it (the story ridge)
  C   band C        (rows 12-13)  the safe trail's gap at x24-25
  S   THE SEAT      (rows 2-11)   the bench, the bothy the kin took back, the view

The two ridges are ordinary ground one tile wide inside `gulf` terrain (hartway_set:
the drop, solid). The two rope ladders are flag-gated `spans` (SpanZone.requires_flag)
with a matching flag-gated `hartway_rope_ladder` object, so art and collision appear
together the moment Greg kicks the ladder over the edge.

HANDSHAKES: the notch (14,48) `to_foot` -> hartway_foot (10,5); the foot's `to_climb`
lands at our (14,47). Both are mid-map portals (a mountain over other ground never
places in world_geometry).

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
c.put([(14, 48)], "=")                                  # the notch the steps drop out of

# band A + rope ladder 1 (gated: cells stay band; the span + object come below)
c.band(2, 27, 39, lip=2, face=3)
# band B + the iron ladder (always there)
c.band(2, 27, 28, lip=2, face=3)
c.ladder(5, 28, 32)
# band C: a low wall under the Seat, the safe trail's gap at x24-25
c.rect(2, 12, 27, 13, "#")

# THE GULF under the Staircase (east, through band A) and under the Whiteback
c.rect(19, 38, 27, 45, "G")
c.rect(8, 14, 20, 27, "G")
STAIRCASE = [(20, 45), (20, 44), (20, 43), (21, 43), (22, 43), (23, 43), (23, 42), (23, 41),
             (24, 41), (25, 41), (25, 40), (25, 39), (25, 38)]
WHITEBACK = ([(x, 22) for x in range(8, 14)] + [(13, 21), (13, 20)]
             + [(x, 20) for x in range(14, 21)])
c.put(STAIRCASE + WHITEBACK, "=")

# ---- the trodden line ----------------------------------------------------------------
c.rect(8, 46, 20, 46, "=").rect(14, 46, 14, 47, "=").rect(8, 44, 8, 46, "=")     # T0
c.rect(5, 36, 25, 36, "=").rect(25, 36, 25, 37, "=").rect(5, 33, 5, 36, "=")     # T1
c.rect(8, 36, 8, 38, "=").rect(24, 33, 24, 36, "=")
c.rect(5, 22, 7, 22, "=").rect(5, 22, 5, 27, "=")                                # U-west
c.rect(21, 20, 25, 20, "=").rect(24, 12, 25, 27, "=")                            # U-east + gap
c.rect(15, 9, 25, 9, "=").rect(24, 9, 25, 11, "=")                               # the Seat

# ---- frost-tuft (the encounter tile) ---------------------------------------------------
c.rect(2, 44, 5, 47, '"')                     # T0 west
c.rect(12, 33, 17, 34, '"')                   # T1, behind the camp
c.rect(14, 37, 18, 38, '"')                   # T1 south lip
c.rect(2, 14, 4, 19, '"')                     # the high shelf, west
c.rect(26, 14, 27, 18, '"')                   # the high shelf, east
c.rect(19, 2, 26, 5, '"')                     # THE HIGH GRASS above the Seat
# a few boulders on open ground
c.put([(10, 44), (22, 47), (3, 37), (20, 34), (3, 25), (22, 24), (11, 6), (3, 9)], "o")
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

# ---- the way down: the notch back to the foot ------------------------------------------
wm.add(m, wm.marker("steps_down", "steps_s", 14, 48))
m["warps"].append({"id": "to_foot", "at": {"tx": 14, "ty": 48}, "trigger": "step_on",
                   "to_map": "hartway_foot", "to": {"tx": 10, "ty": 5}, "facing": "down",
                   "transition": "fade"})

# ---- THE ROPE LADDERS (Greg fixes each once its ridge is behind you) -------------------
for n, (x, y0) in ((1, (8, 39)), (2, (24, 28))):
    flag = f"flag:hart_ladder_{n}"
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


greg("greg_t0", (21, 46), "left", "script.greg_t0", None, "flag:hart_p1_done")
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


beat("staircase", [(20, 46)], "script.hart_staircase", None, "flag:hart_p1_done")
beat("ladder_one", [(25, 37)], "script.hart_ladder_one", "flag:hart_p1_done", "flag:hart_ladder_1")
beat("chimney", [(5, 33)], "script.hart_chimney", "flag:hart_ladder_1", "flag:hart_b1_done")
beat("whiteback", [(7, 22)], "script.hart_whiteback", "flag:hart_b1_done", "flag:hart_p2_done")
beat("cornice", [(24, 11), (25, 11)], "script.hart_cornice", "flag:hart_ladder_2", "flag:hart_b3_done")

# ---- T1: the walkers' camp (a rest point) ----------------------------------------------
m["objects"].append({"id": "camp", "sprite": "hushfrost_walker_camp", "at": {"tx": 8, "ty": 32},
                     "w": 4, "h": 3, "overhang": 1})
for x in (9, 10):
    m["triggers"].append({"id": f"camp_rest_{x}", "kind": "script", "at": {"tx": x, "ty": 35},
                          "activation": "interact", "ref": "script.hartway_camp"})
owed.append("script.hartway_camp")

# ---- THE SEAT ---------------------------------------------------------------------------
m["objects"] += [
    {"id": "ruin_hut", "sprite": "hartway_ruin_hut", "at": {"tx": 4, "ty": 3}, "w": 4, "h": 4,
     "overhang": 2},
    {"id": "bench", "sprite": "hartway_bench", "at": {"tx": 13, "ty": 10}, "w": 2, "h": 1},
    {"id": "cairn_seat", "sprite": "windward_cairn", "at": {"tx": 17, "ty": 9}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "flags_seat", "sprite": "windward_prayer_flags", "at": {"tx": 9, "ty": 3}, "w": 4, "h": 2,
     "overhang": 2, "walk_under": True, "solid": False},
]
for x in (13, 14):
    m["triggers"].append({"id": f"seat_{x}", "kind": "cutscene", "at": {"tx": x, "ty": 10},
                          "activation": "interact", "ref": "script.hart_seat"})
m["triggers"].append({"id": "hut_door", "kind": "sign", "at": {"tx": 6, "ty": 7},
                      "activation": "interact", "ref": "sign.hartway_hut"})
owed += ["script.hart_seat", "sign.hartway_hut"]

# the bothy belongs to the mountain's kin now (ambient: greetable, never colliding)
for aid, kin, (x, y), r in [("amb_hut_a", 77, (9, 6), 2), ("amb_hut_b", 88, (3, 8), 2),
                            ("amb_seat", 80, (11, 8), 1), ("amb_shelf", 80, (16, 35), 2),
                            ("amb_high", 77, (3, 21), 1)]:
    m["npcs"].append({"id": aid, "at": {"tx": x, "ty": y}, "facing": "down",
                      "sprite": f"kin_{kin}_overworld", "movement": "wander",
                      "ambient": True, "wander_radius": r})

# ---- signs / caches ----------------------------------------------------------------------
owed += pt.sign(m, deco, W, sid="hartway_staircase", at=(18, 47))
owed += pt.sign(m, deco, W, sid="hartway_whiteback", at=(4, 23))
owed += pt.sign(m, deco, W, sid="hartway_seat", at=(23, 8))
owed += pt.cache(m, cid="hartway_shelf", at=(27, 34))
owed += pt.cache(m, cid="hartway_high", at=(2, 16))
owed += pt.cache(m, cid="hartway_seat", at=(26, 7))

# ---- dressing (a landmark on every screen) ------------------------------------------------
m["objects"] += [
    {"id": "cairn_t0", "sprite": "windward_cairn", "at": {"tx": 16, "ty": 43}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "pine_t0", "sprite": "hushfrost_snow_pine", "at": {"tx": 6, "ty": 44}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "pine_t1", "sprite": "hushfrost_snow_pine_big", "at": {"tx": 19, "ty": 32}, "w": 3, "h": 4,
     "overhang": 3, "walk_under": True},
    {"id": "rocks_t1", "sprite": "hushfrost_snow_boulders", "at": {"tx": 12, "ty": 37}, "w": 2, "h": 2},
    {"id": "dead_uw", "sprite": "hushfrost_dead_tree", "at": {"tx": 2, "ty": 23}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "cairn_uw", "sprite": "windward_cairn", "at": {"tx": 6, "ty": 18}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "flags_ue", "sprite": "windward_prayer_flags", "at": {"tx": 21, "ty": 16}, "w": 4, "h": 2,
     "overhang": 2, "walk_under": True, "solid": False},
    {"id": "drift_ue", "sprite": "hushfrost_snowdrift", "at": {"tx": 21, "ty": 24}, "w": 3, "h": 2},
    {"id": "pine_seat", "sprite": "hushfrost_snow_pine", "at": {"tx": 2, "ty": 2}, "w": 2, "h": 3,
     "overhang": 2, "walk_under": True},
    {"id": "rocks_seat", "sprite": "hushfrost_snow_boulders", "at": {"tx": 9, "ty": 9}, "w": 2, "h": 2},
]

# ---- encounters (band 19-22; the High Grass gains the fawns once the herd has passed) ------
def T(*r):
    return [{"kin_id": k, "weight": w_, "min_level": lo, "max_level": hi} for (k, w_, lo, hi) in r]


LOW = T((47, 28, 19, 20), (62, 24, 19, 20), (88, 22, 19, 21), (77, 16, 19, 21), (50, 10, 20, 21))
HIGH = T((77, 28, 20, 22), (80, 24, 20, 22), (83, 20, 20, 22), (88, 18, 20, 22), (74, 10, 21, 22))
PASTURE = T((77, 24, 20, 22), (80, 22, 20, 22), (83, 18, 20, 22), (88, 16, 20, 22), (120, 20, 21, 22))
low = mk.make_grid(W, H)
high = mk.make_grid(W, H)
grass = mk.make_grid(W, H)
for i in range(W * H):
    if g["tuft"][i]:
        y = i // W
        (grass if y <= 5 else high if y <= 27 else low)[i] = 1
m["encounters"] += pt.zones_from_grid(low, W, H, terrain="tall_grass", rate=0.09, table=LOW,
                                      id_prefix="low")
m["encounters"] += pt.zones_from_grid(high, W, H, terrain="tall_grass", rate=0.09, table=HIGH,
                                      id_prefix="high")
for z in pt.zones_from_grid(grass, W, H, terrain="tall_grass", rate=0.10, table=HIGH,
                            id_prefix="pasture"):
    m["encounters"].append({**z, "hidden_when_flag": "flag:hart_mist_seen"})
    m["encounters"].append({**z, "id": z["id"] + "_herd", "table": PASTURE,
                            "requires_flag": "flag:hart_mist_seen"})

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
    ok = mk.finalize(m, scale=3, pin_base=pin)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
