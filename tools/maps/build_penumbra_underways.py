#!/usr/bin/env python3
"""
The Penumbra Underways — the last road (walkthrough/11 Part D, Lane N3; kind cave,
region central, band 52-56, optional + endgame). Two portal floors under the
Penumbra Ring, a LOOP: down the Ring's south-west mouth, through the upper
galleries, down to the Last Watch, up again in the east galleries and out of the
Ring's south-east mouth. Both mouths sit beyond the Ring's starlit dark (Starreach)
and are gated `flag:hub_unlocked` + `starreach` with a blocked line besides.

  penumbra_underways     (F1, 30x22) "The Underways"
      Two halves split by the Ring's own foundations: the WEST galleries (in from
      the SW mouth; the watcher Odalie; a Starglass Shard in the side bay, whose
      rubble lip DROPS you one-way into the cistern hall, so the walk back up is by
      Odalie's cut) and the EAST galleries (out to the SE mouth; the watcher Hesk;
      the watch's long hall with its map table and stores). Neither half reaches the
      other except through B1.
  penumbra_underways_b1  (B1, 32x24) "The Underways — the Last Watch"
      The Hollowing's last watch keeps its fire here, under the Spire's roots: the
      watch-fire is a REST POINT (script.underways_watchfire_rest), Old Clemency keeps
      it (renamed from "Old Maudry", fix FD 2026-10-14: the name is Maudry Kell's),
      the watcher Bran holds the west gallery's choke. North of the fire the
      roots open on THE SPIRE'S SHAFT — the foot of a pit the Crown's light falls
      down from impossibly high (seen, never climbed: a solid prop, no warp). The
      LAST LUMEN DROP before the summit waits in the south-east pocket, THE WARM
      STONES, reached by the slump: its own bed is the only place the Embralux (#33)
      comes down before the dawn, with a deep Shutterwick (#179) bed.

Review fix FD (2026-10-14, docs/reviews/expansion-panel.md Plan 4 Part D): the floors
are re-carved as organic blob chambers from a solid wall grid (the glowmoss_deep
pattern) with 1-wide chokes; the moss beds are lobed and fringed in grey moss; the
watch is dressed in its own drawn kit (tools/maps/underwaysforge.py: bedrolls, map
table, watch-bell, ration crates, kettle shelf, watch-rota, fallen Spire masonry, root
curtains) instead of the Coldfog camp; every zone has a post-dawn `_day` twin; and the
Ring's light-well (build_penumbra_ring.py) shows the shaft and the fire from above.

Review fix FD2 (2026-10-14, Plan 4 r2 Part D): density in F1's lower halls and B1's west bay
+ south gallery (new drawn props: hammock, name_slate, cold_brazier/brazier_lit, hood_line,
water_butt, firewood); the south gallery now meets the watch's spur (a true loop); the Warm
Stones are the only wild JesterFull (#168); and once the watch is kept the three watchers
leave their posts for Clemency's fire (`gathered()`).

The strongest wild beds before Còr: the galleries roll Dark (cave, rect-wide),
the glow-moss beds roll Light — the two halves of the dark, side by side.
Never connected to the Umbral Spire: you always come back out into the Ring.

Warps (all mutual; the audit pairs them):
  F1 (3,1)/(4,1)   `to_ring_w`/`_e` -> penumbra_ring (4,31)/(5,31)   [Ring `to_underways_w` (4,32)/(5,32)]
  F1 (26,1)/(27,1) `to_ring_se`/`_e` -> penumbra_ring (22,31)/(23,31) [Ring `to_underways_e` (22,32)/(23,32)]
  F1 (6,18)  `ladder_down_w` <-> B1 (5,3)  `ladder_up_w`
  F1 (23,18) `ladder_down_e` <-> B1 (26,3) `ladder_up_e`

Levels: F1 52-55, B1 54-56 (day: 56-60). Mirrored in build_species.py (MOURNING_TABLES).

Run:  python3 tools/maps/build_penumbra_underways.py
"""
from __future__ import annotations

import random

import facekit as fk
import mapkit as mk
import patterns as pt
import warp_markers as wm
from mapkit import gid

MUSIC = "assets/audio/music/penumbra-underways.mp3"
BACKDROP = ["assets/backgrounds/battle/underways-a.webp"]
AMBIENCE = {"particles": [{"kind": "dust", "density": 0.35}, {"kind": "starglint", "density": 0.35}],
            "tint": {"color": "#0a0818", "alpha": 0.16}, "sound_bed": "amb-drips"}


def carve(W, H, chambers, lines, rng):
    """Organic chambers from a SOLID wall grid (the glowmoss_deep pattern; review FD
    2026-10-14: "carve organic chambers, not rectangles"): each chamber is a union of
    blobs, joined by 1-wide chokes (`lines`: ('h', y, x0, x1) / ('v', x, y0, y1) /
    ('r', x0, y0, x1, y1)). `rng` is unused (kept for call-site symmetry)."""
    wall = mk.make_grid(W, H)
    mk.rect(wall, W, H, 0, 0, W - 1, H - 1)
    floor = mk.make_grid(W, H)
    for blobs in chambers:
        for (cx, cy, rx, ry) in blobs:
            mk.blob(floor, W, H, cx, cy, rx, ry)
    for ln in lines:
        if ln[0] == "h":
            mk.hline(floor, W, H, ln[1], ln[2], ln[3])
        elif ln[0] == "v":
            mk.vline(floor, W, H, ln[1], ln[2], ln[3])
        else:
            mk.rect(floor, W, H, *ln[1:])
    for i in range(W * H):
        if floor[i]:
            wall[i] = 0
    return wall, floor


def moss_bed(moss, W, H, lobes):
    """A glow-moss bed as a union of offset lobes — never a ruled rectangle."""
    for (cx, cy, rx, ry) in lobes:
        mk.blob(moss, W, H, cx, cy, rx, ry)


def mapdict(mid, name, W, H, base, layers, deco):
    return {
        "id": mid, "display_name": name, "width": W, "height": H,
        "tile_width": 16, "tile_height": 16, "kind": "cave",
        "tilesets": [mk.shared_tileset_ref()],
        "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + layers +
                  [{"name": "deco", "role": "deco", "depth": 5, "data": deco},
                   {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
        "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
        "music": MUSIC, "battle_backdrops": list(BACKDROP), "ambience": dict(AMBIENCE),
    }


def ground(W, H, rng):
    bs = [gid("basalt0"), gid("basalt1"), gid("basalt2")]
    return [rng.choice(bs) if rng.random() < 0.5 else bs[0] for _ in range(W * H)]


def layers_for(wall, moss):
    return [
        {"name": "t_moss", "role": "terrain", "terrain": "glowmoss",
         "set": "vesper_overworld_set", "depth": 0, "data": moss},
        {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
         "set": "vesper_overworld_set", "depth": 0, "data": wall},
    ]


def obj(m, oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m["objects"].append(o)




def zones(m, W, H, moss, cave_table, moss_table, prefix, day_cave, day_moss, extra=()):
    """Night tables + their post-dawn twins (facekit.night_day: the night zone hides at
    flag:dawn, a `_day` twin with the day table appears). `extra` zones (a pocket's own
    bed) go FIRST and carry their own day table."""
    night_cave = [{"id": f"{prefix}_galleries", "terrain": "cave",
                   "rect": {"tx": 0, "ty": 0, "w": W, "h": H},
                   "encounter_rate": 0.07, "table": cave_table}]
    night_moss = pt.zones_from_grid(moss, W, H, terrain="tall_grass", rate=0.12,
                                    table=moss_table, id_prefix=f"{prefix}_moss")
    out = []
    for (z, day) in extra:
        out += fk.night_day([z], day)
    out += fk.night_day(night_cave, day_cave) + fk.night_day(night_moss, day_moss)
    m["encounters"] = out


def fringe(deco, wall, moss, W, H, rng, busy, keep):
    """Grey-moss fringe round every glow-moss bed (review FD: 'fringe them with
    greymoss') — the dead edge of the living moss."""
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            i = y * W + x
            if wall[i] or moss[i] or deco[i] or (x, y) in busy or (x, y) in keep:
                continue
            near = sum(moss[(y + dy) * W + x + dx] for dx in (-1, 0, 1) for dy in (-1, 0, 1))
            if near and rng.random() < 0.55:
                deco[i] = gid(rng.choice(("greymoss_a", "greymoss_b")))


def busy_tiles(m):
    busy = set()
    for o in m["objects"]:
        for dx in range(o["w"]):
            for dy in range(o["h"]):
                busy.add((o["at"]["tx"] + dx, o["at"]["ty"] + dy))
    busy |= {(p["at"]["tx"], p["at"]["ty"]) for p in m["npcs"] + m["triggers"] + m["warps"]}
    busy |= {(p["to"]["tx"], p["to"]["ty"]) for p in m["warps"]}
    return busy


def dress(m, W, H, wall, moss, deco, rng, keep, density=0.10):
    """Drained grit on the open floor (pebbles, greymoss, a rare glowshroom), never on a
    busy tile or the lanes in `keep`; then the grey-moss fringe on every bed."""
    busy = busy_tiles(m)
    fringe(deco, wall, moss, W, H, rng, busy, keep)
    bits = [gid("g_pebble"), gid("g_pebble"), gid("greymoss_a"), gid("glowshroom_a")]
    for y in range(H):
        for x in range(W):
            i = y * W + x
            if wall[i] or moss[i] or deco[i] or (x, y) in busy or (x, y) in keep:
                continue
            if rng.random() < density:
                deco[i] = rng.choice(bits)


def hooded_lamp(m, oid, at):
    """The watch's hooded lantern on its staff; unhooded after the dawn (same footprint)."""
    obj(m, oid, "underways_watch_lamp", at, 1, 2, overhang=1, hidden_when_flag="flag:dawn")
    obj(m, f"{oid}_lit", "underways_watch_lamp_lit", at, 1, 2, overhang=1, requires_flag="flag:dawn")


def prop(m, oid, stem, at, w, h, **kw):
    """A drawn watch prop (underwaysforge.py). 2-row props walk-under their top row."""
    if h > 1 and "overhang" not in kw:
        kw.update(overhang=1, walk_under=True)
    obj(m, oid, f"underways_{stem}", at, w, h, **kw)


def brazier(m, oid, at):
    """FD2: the watch's cold brazier (ash, a coal unburned); lit after the dawn (same footprint)."""
    prop(m, oid, "cold_brazier", at, 1, 2, hidden_when_flag="flag:dawn")
    prop(m, f"{oid}_lit", "brazier_lit", at, 1, 2, requires_flag="flag:dawn")


def gathered(m, posts, at_fire):
    """FD2: once the whole watch is kept (flag:underways_watch_kept) the watchers leave their
    posts and gather at Clemency's fire: each post's `_after` NPC hides, and a fire twin
    appears (`<tid>_fire`, script.<tid>_fire, dusk/dawn branches)."""
    for n in m["npcs"]:
        if n["id"] in {f"{t}_after" for t in posts}:
            n["hidden_when_flag"] = "flag:underways_watch_kept"
    for tid, (x, y), facing in at_fire:
        m["npcs"].append({"id": f"{tid}_fire", "at": {"tx": x, "ty": y}, "facing": facing,
                          "sprite": "hollowing_acolyte", "movement": "static",
                          "dialogue_ref": f"script.{tid}_fire",
                          "requires_flag": "flag:underways_watch_kept"})
    return [f"script.{tid}_fire" for tid, _, _ in at_fire]


def T(kin, w, lo, hi):
    return {"kin_id": kin, "weight": w, "min_level": lo, "max_level": hi}


# =============================================================================== tables
# Night (the Long Dusk): the strongest Dark/Light beds before Còr.
F1_CAVE = [T(138, 24, 52, 54), T(113, 18, 52, 54), T(143, 16, 52, 54),   # Voidmantle, Omenire, Whorlix
           T(15, 14, 53, 55), T(85, 14, 53, 55), T(135, 14, 53, 55)]     # Pyriven, Stillwarden, Liminalux
F1_MOSS = [T(127, 30, 52, 54), T(135, 25, 53, 55), T(107, 20, 53, 55),   # Lunvane, Liminalux, Lunarbel
           T(40, 15, 53, 55), T(140, 10, 54, 55)]                        # Lumenmoss, Wisprestored
B1_CAVE = [T(135, 24, 54, 56), T(138, 22, 54, 56), T(113, 16, 54, 56),   # Liminalux, Voidmantle, Omenire
           T(142, 14, 54, 56), T(143, 14, 54, 56), T(144, 6, 55, 56)]    # Embergone, Whorlix, Nullhusk
B1_MOSS = [T(40, 26, 54, 56), T(107, 22, 54, 56), T(127, 20, 54, 56),    # Lumenmoss, Lunarbel, Lunvane
           T(37, 14, 55, 56), T(135, 12, 54, 56), T(129, 6, 56, 56)]     # Prismara, Liminalux, Dawnwatcher
# THE WARM STONES (B1's south-east pocket, past the slump): the only ground where the
# EMBRALUX (#33, Ember/Light) comes down before the dawn, drawn to the watch's warmth,
# and the deep Shutterwick bed (#179). Unique to the Underways (review FD: creature value).
# FD2 (2026-10-14): and the ONLY wild JesterFull (#168, Light/Dark) in the world — a whole
# jest-house kin that wandered down to do its turn for the watch by the fire (rare).
B1_POCKET = [T(179, 34, 54, 56), T(180, 24, 54, 56), T(40, 20, 54, 56),  # Shutterwick, Lullwing, Lumenmoss
             T(135, 14, 54, 56), T(33, 8, 55, 56), T(168, 6, 55, 56)]    # Liminalux, EMBRALUX, JESTERFULL
# Day (flag:dawn): the dark lifts out of the galleries; the light kin stay, a band up.
F1_CAVE_DAY = [T(135, 26, 56, 59), T(107, 22, 56, 59), T(140, 20, 56, 59),
               T(85, 18, 56, 59), T(37, 14, 57, 59)]
F1_MOSS_DAY = [T(40, 32, 56, 59), T(127, 28, 56, 59), T(37, 24, 57, 59), T(129, 16, 58, 59)]
B1_CAVE_DAY = [T(135, 28, 57, 60), T(140, 24, 57, 60), T(37, 22, 57, 60),
               T(107, 20, 57, 60), T(33, 6, 59, 60)]
B1_MOSS_DAY = [T(40, 34, 57, 60), T(37, 26, 57, 60), T(127, 24, 57, 60), T(129, 16, 58, 60)]
B1_POCKET_DAY = [T(33, 30, 57, 60), T(179, 30, 57, 60), T(37, 22, 57, 60), T(40, 18, 57, 60),
                 T(168, 6, 58, 60)]


# =============================================================================== F1
LEDGE_F1 = (11, 10)


def build_f1() -> tuple[dict, list[str]]:
    W, H = 30, 22
    rng = random.Random(5201)
    chambers = [
        # ---- the WEST galleries (x 1-13) ----
        [(3.8, 2.6, 2.4, 1.9), (2.6, 4.2, 1.3, 1.4)],           # A the SW mouth's stair-foot
        [(6.2, 6.0, 3.6, 1.6), (4.0, 6.4, 2.0, 1.5)],           # B the first gallery
        [(11.6, 4.4, 1.6, 2.6), (11.2, 7.6, 1.4, 1.4)],         # C the side bay (the Starglass)
        [(6.8, 13.0, 4.6, 2.3), (3.2, 12.4, 1.6, 1.6),          # D the old cistern hall
         (10.4, 11.6, 1.3, 1.1)],
        [(2.8, 16.8, 1.7, 1.6)],                                # D' the watch's bed-nook
        [(7.0, 17.8, 2.6, 1.9), (5.6, 18.6, 1.6, 1.3)],         # E the ladder vault
        # ---- the EAST galleries (x 16-28) ----
        [(26.4, 2.8, 2.2, 1.9), (27.6, 4.6, 1.4, 1.4)],         # F the SE mouth's stair-foot
        [(23.6, 6.0, 4.0, 1.6), (20.6, 5.6, 1.6, 1.3)],         # G the long gallery
        [(21.0, 12.6, 4.8, 2.0), (17.6, 12.2, 1.6, 1.6)],       # H the watch's long hall
        [(27.4, 12.2, 1.6, 1.8)],                               # H' the east nook (the stores)
        [(23.6, 17.6, 2.8, 2.0), (25.8, 18.8, 1.4, 1.2)],       # I the ladder vault
        [(18.0, 17.2, 1.6, 2.2)],                               # J the moss pocket
    ]
    lines = [
        ("r", 3, 1, 4, 2),          # the SW stair throat (2 wide, the warp pair)
        ("v", 3, 4, 5),             # A -> B
        ("h", 6, 9, 10),            # B -> C (1-wide)
        ("h", 8, 3, 5),             # the cut's lip (you pass Odalie, never through her)
        ("v", 4, 8, 11),            # B -> D, the cut south (Odalie watches it)
        ("v", 11, 8, 9),            # C -> the LEDGE (11,10) -> D: one way down
        ("h", 16, 3, 4),            # D -> the bed-nook
        ("v", 7, 15, 16),           # D -> E (1-wide)
        ("r", 26, 1, 27, 2),        # the SE stair throat
        ("v", 26, 4, 5),            # F -> G
        ("v", 22, 8, 10),           # G -> H, the cut south (Hesk holds it)
        ("r", 23, 8, 23, 8),        # Hesk's post beside the cut
        ("h", 12, 25, 26),          # H -> the east nook
        ("v", 24, 14, 15),          # H -> I (1-wide)
        ("h", 17, 19, 21),          # I -> J
    ]
    wall, floor = carve(W, H, chambers, lines, rng)
    for y in range(H):                                 # the Ring's foundations split the halves
        for x in (14, 15):
            floor[y * W + x] = 0
    # the ledge cell is FLOOR under a south-hop ledge; its flanks are rock so it can't be
    # walked round (the one-way back into the cistern hall)
    lx, ly = LEDGE_F1
    floor[ly * W + lx] = 1
    for x in (lx - 1, lx + 1):
        floor[ly * W + x] = 0
    for i in range(W * H):
        wall[i] = 0 if floor[i] else 1
    moss = mk.make_grid(W, H)
    moss_bed(moss, W, H, [(11.6, 5.0, 1.3, 1.5), (12.2, 6.4, 0.9, 1.0)])     # the side bay
    moss_bed(moss, W, H, [(6.4, 13.0, 1.9, 1.0), (8.4, 13.8, 1.3, 0.9),
                          (5.0, 12.4, 1.0, 0.8)])                            # the cistern hall
    moss_bed(moss, W, H, [(18.0, 16.6, 1.0, 1.5), (18.4, 18.4, 0.9, 0.9)])   # the east pocket
    moss_bed(moss, W, H, [(24.6, 5.8, 1.6, 0.9), (26.0, 6.4, 1.0, 0.8)])     # the long gallery
    for i in range(W * H):
        if not floor[i]:
            moss[i] = 0
    moss[ly * W + lx] = 0
    deco = mk.make_grid(W, H)
    m = mapdict("penumbra_underways", "The Underways", W, H, ground(W, H, rng),
                layers_for(wall, moss), deco)
    owed: list[str] = []
    m["warps"] += [
        {"id": "to_ring_w", "at": {"tx": 3, "ty": 1}, "trigger": "step_on", "to_map": "penumbra_ring",
         "to": {"tx": 4, "ty": 31}, "facing": "up", "transition": "fade"},
        {"id": "to_ring_w_e", "at": {"tx": 4, "ty": 1}, "trigger": "step_on", "to_map": "penumbra_ring",
         "to": {"tx": 5, "ty": 31}, "facing": "up", "transition": "fade"},
        {"id": "to_ring_se", "at": {"tx": 26, "ty": 1}, "trigger": "step_on", "to_map": "penumbra_ring",
         "to": {"tx": 22, "ty": 31}, "facing": "up", "transition": "fade"},
        {"id": "to_ring_se_e", "at": {"tx": 27, "ty": 1}, "trigger": "step_on", "to_map": "penumbra_ring",
         "to": {"tx": 23, "ty": 31}, "facing": "up", "transition": "fade"},
    ]
    pt.cave_ladder(m, deco, W, kind="down", at=(6, 18), to_map="penumbra_underways_b1",
                   to=(5, 3), wid="ladder_down_w")
    pt.cave_ladder(m, deco, W, kind="down", at=(23, 18), to_map="penumbra_underways_b1",
                   to=(26, 3), wid="ladder_down_e")
    wm.add(m, wm.marker("stair_w", "steps_n", 3, 0), wm.marker("stair_w_e", "steps_n", 4, 0),
           wm.marker("stair_se", "steps_n", 26, 0), wm.marker("stair_se_e", "steps_n", 27, 0))
    # THE ONE-WAY (review FD #4): from the side bay a rubble lip drops you into the
    # cistern hall; the walk back up is by Odalie's cut, never the way you came.
    deco[ly * W + lx] = gid("scree_ledge_s")
    # the watchers (the last watch's outer posts)
    owed += pt.trainer_beat(m, tid="underways_watch_a", at=(4, 7), facing="down", sight=4,
                            sprite="hollowing_acolyte")
    owed += pt.trainer_beat(m, tid="underways_watch_c", at=(23, 8), facing="left", sight=2,
                            sprite="hollowing_acolyte")
    # FD2: once the watch is kept, Odalie and Hesk leave these posts for the fire (B1)
    gathered(m, ("underways_watch_a", "underways_watch_c"), ())
    owed += pt.cache(m, cid="underways_starglass", at=(12, 3))
    owed += pt.sign(m, deco, W, sid="underways_mouth", at=(6, 2))
    # ---- the watch's dressing (underwaysforge.py): lived-in, tended, never a guard-post
    hooded_lamp(m, "watch_lamp_a", (2, 3))
    hooded_lamp(m, "watch_lamp_c", (28, 4))
    hooded_lamp(m, "hall_lamp_0", (17, 11))
    hooded_lamp(m, "hall_lamp_1", (25, 11))
    prop(m, "w_roots_a", "root_curtain", (8, 4), 2, 2, solid=False)
    prop(m, "w_masonry", "masonry", (8, 6), 2, 2)
    prop(m, "w_rota", "watch_rota", (2, 5), 1, 2)
    prop(m, "w_crates", "ration_crates", (2, 11), 2, 2)
    prop(m, "w_bedroll_a", "bedroll", (2, 16), 2, 1)
    prop(m, "w_bedroll_b", "bedroll", (2, 17), 2, 1)
    prop(m, "w_kettle", "kettle_shelf", (9, 16), 2, 2)
    obj(m, "null_pool", "spire_null_pool", (9, 12), 2, 2)
    prop(m, "e_bell", "watch_bell", (24, 1), 1, 2)
    prop(m, "e_roots", "root_curtain", (19, 4), 2, 2, solid=False)
    prop(m, "e_masonry", "masonry", (26, 6), 2, 2)
    prop(m, "e_table", "map_table", (19, 13), 2, 2)
    prop(m, "e_crates", "ration_crates", (27, 11), 2, 2)
    prop(m, "e_bedroll", "bedroll", (27, 13), 2, 1)
    prop(m, "e_rota", "watch_rota", (22, 16), 1, 2)
    obj(m, "glowshrooms", "glowmoss_deep_glowshrooms_teal", (17, 18), 2, 2, solid=False)
    # FD2 (review r2: "F1's two lower halls are still thin"): the watch lives down here too
    brazier(m, "w_brazier", (7, 11))                       # the cistern hall's memorial corner
    prop(m, "w_names", "name_slate", (8, 11), 1, 2)
    prop(m, "w_hammock", "hammock", (8, 18), 2, 2)         # the ladder vault: a hammock, wood
    prop(m, "w_firewood", "firewood", (2, 18), 2, 1)       # stacked in the bed-nook's foot
    prop(m, "e_hoods", "hood_line", (20, 11), 2, 2)        # the long hall: hoods drying
    prop(m, "e_butt", "water_butt", (26, 12), 1, 1)
    prop(m, "e_firewood", "firewood", (22, 14), 2, 1)
    prop(m, "e_names", "name_slate", (25, 16), 1, 2)       # the east ladder vault
    prop(m, "e_hammock", "hammock", (25, 18), 2, 2)
    prop(m, "e_butt_b", "water_butt", (27, 19), 1, 1)
    for (x, y) in [(5, 3), (2, 13), (11, 4), (18, 12), (21, 19), (26, 19)]:
        if not wall[y * W + x] and not deco[y * W + x]:
            deco[y * W + x] = gid("boulder")
    zones(m, W, H, moss, F1_CAVE, F1_MOSS, "underways_f1", F1_CAVE_DAY, F1_MOSS_DAY)
    keep = {(x, y) for x in (3, 4, 26, 27) for y in (1, 2, 3)}
    keep |= {(4, y) for y in range(4, 12)} | {(22, y) for y in range(7, 12)}
    keep |= {(11, y) for y in range(7, 12)} | {(7, y) for y in range(14, 18)}
    keep |= {(24, y) for y in range(13, 17)} | {(x, 6) for x in range(8, 12)}
    dress(m, W, H, wall, moss, deco, rng, keep, density=0.16)
    return m, owed


# =============================================================================== B1
SLUMP_B1 = (25, 14)


def build_b1() -> tuple[dict, list[str]]:
    W, H = 32, 24
    rng = random.Random(5202)
    chambers = [
        [(5.4, 3.6, 2.8, 1.8), (7.6, 2.8, 1.4, 1.2)],           # the west ladder foot
        [(5.0, 8.0, 1.4, 2.6)],                                 # the west gallery (moss brush)
        [(5.0, 13.6, 3.6, 2.4), (2.8, 12.4, 1.5, 1.6)],         # the sleepers' alcove
        [(16.0, 12.6, 4.6, 3.3), (12.6, 11.4, 1.6, 1.8),        # THE LAST WATCH (the fire)
         (19.8, 15.0, 1.6, 1.4)],
        [(11.4, 8.6, 1.6, 1.3)],                                # the kettle nook (off the watch)
        [(16.0, 3.8, 4.2, 2.8), (12.8, 4.6, 1.4, 1.4),          # THE SHAFT CHAMBER (the vista)
         (19.4, 4.4, 1.4, 1.6)],
        [(26.4, 4.4, 2.8, 1.9), (28.4, 6.8, 1.2, 1.4)],         # the east ladder foot
        [(25.4, 9.6, 1.4, 3.2)],                                # the east cut
        [(27.4, 18.0, 2.8, 2.5), (25.8, 16.4, 1.4, 1.2)],       # THE WARM STONES (SE pocket)
        [(20.2, 19.8, 5.6, 1.5), (16.2, 19.2, 2.0, 1.3)],       # the south gallery
    ]
    lines = [
        ("v", 5, 5, 6), ("v", 5, 10, 11),      # west foot -> gallery -> alcove
        ("h", 13, 9, 11),                      # Bran's choke into the watch (1-wide)
        ("r", 15, 6, 16, 9),                   # the watch -> the shaft (the root neck, 2 wide)
        ("h", 9, 12, 12),                      # the watch -> the kettle nook
        ("h", 12, 21, 24),                     # the watch -> the east cut (1-wide)
        ("r", 25, 6, 25, 7),                   # the east foot -> the east cut
        ("r", 25, 12, 25, 13),                 # the east cut's foot, onto the slump
        ("r", 14, 1, 17, 4),                   # the shaft's own footprint
        ("v", 14, 16, 19),                     # the watch -> the south gallery (FD2: it
                                               # stopped a tile short; now a true loop)
        ("r", 24, 15, 26, 16),                 # the pocket's landing under the slump
    ]
    wall, floor = carve(W, H, chambers, lines, rng)
    # THE SLUMP (the loop): a rubble step from the east cut down into the warm stones;
    # its flanks are rock so it can't be walked round.
    sx, sy = SLUMP_B1
    floor[sy * W + sx] = 1
    for x in (sx - 1, sx + 1):
        floor[sy * W + x] = 0
    for i in range(W * H):
        wall[i] = 0 if floor[i] else 1
    moss = mk.make_grid(W, H)
    moss_bed(moss, W, H, [(5.0, 8.4, 1.1, 1.6), (5.6, 9.6, 0.8, 0.9)])       # the west gallery (a brush)
    moss_bed(moss, W, H, [(19.0, 20.0, 1.8, 0.8), (21.6, 19.6, 1.0, 0.7)])   # the south gallery
    moss_bed(moss, W, H, [(26.6, 4.8, 1.5, 0.8), (27.8, 5.6, 0.8, 0.8)])     # the east foot
    pocket = mk.make_grid(W, H)
    moss_bed(pocket, W, H, [(27.8, 18.0, 1.8, 1.4), (26.4, 19.2, 1.1, 0.9),
                            (29.0, 19.6, 0.8, 0.8)])                         # the warm stones' bed
    for i in range(W * H):
        if not floor[i]:
            moss[i] = 0
            pocket[i] = 0
    allmoss = [1 if (a or b) else 0 for a, b in zip(moss, pocket)]
    deco = mk.make_grid(W, H)
    m = mapdict("penumbra_underways_b1", "The Underways", W, H, ground(W, H, rng),
                layers_for(wall, allmoss), deco)
    m["display_name"] = "The Last Watch"
    owed: list[str] = []
    pt.cave_ladder(m, deco, W, kind="up", at=(5, 3), to_map="penumbra_underways",
                   to=(6, 18), wid="ladder_up_w")
    pt.cave_ladder(m, deco, W, kind="up", at=(26, 3), to_map="penumbra_underways",
                   to=(23, 18), wid="ladder_up_e")
    deco[sy * W + sx] = gid("scree_ledge_s")
    # THE SHAFT (the seen-before-reached view up; solid, no warp, no Spire link)
    obj(m, "spire_shaft", "underways_spire_shaft", (14, 1), 4, 4, overhang=1)
    for (x, y) in [(13, 4), (18, 4)]:
        deco[y * W + x] = gid("null_lantern")
    for tx in (14, 15, 16, 17):
        m["triggers"].append({"id": f"shaft_view_{tx}", "kind": "cutscene",
                              "at": {"tx": tx, "ty": 5}, "activation": "interact",
                              "ref": "script.underways_shaft_view"})
    owed.append("script.underways_shaft_view")
    obj(m, "crownlight", "spire_crownshaft", (14, 5), 3, 3, solid=False)
    prop(m, "shaft_roots_w", "root_curtain", (12, 2), 2, 2, solid=False)
    prop(m, "shaft_roots_e", "root_curtain", (18, 2), 2, 2, solid=False)
    # THE LAST WATCH: the fire (rest point), the keeper, the watch's things
    obj(m, "watch_camp", "penumbra_vigil_camp", (15, 11), 3, 2)
    for tx in (15, 16, 17):
        m["triggers"].append({"id": f"watchfire_{tx}", "kind": "cutscene", "at": {"tx": tx, "ty": 13},
                              "activation": "interact", "ref": "script.underways_watchfire_rest"})
    owed.append("script.underways_watchfire_rest")
    m["npcs"].append({"id": "clemency", "at": {"tx": 18, "ty": 12}, "facing": "left",
                      "sprite": "hollowing_elder", "movement": "static",
                      "dialogue_ref": "script.underways_clemency"})
    owed.append("script.underways_clemency")
    prop(m, "bedroll_a", "bedroll", (12, 15), 2, 1)
    prop(m, "bedroll_b", "bedroll", (17, 15), 2, 1)
    prop(m, "bedroll_c", "bedroll", (19, 14), 2, 1)
    prop(m, "watch_table", "map_table", (19, 10), 2, 2)
    prop(m, "watch_bell", "watch_bell", (20, 15), 1, 2)
    prop(m, "kettle", "kettle_shelf", (10, 7), 2, 2)
    hooded_lamp(m, "watch_lamp_n", (17, 9))
    obj(m, "blankets", "mournfields_blanket_stack", (12, 16), 2, 1)
    # the sleepers' alcove (kin the watch keeps asleep — awake after the dawn)
    for n, (kin, (x, y)) in enumerate([("nullmoth", (2, 12)), ("cindersob", (3, 14)),
                                       ("voidmantle", (6, 14))]):
        obj(m, f"sleeper_{n}", f"spire_sleeper_{kin}", (x, y), 2, 2, hidden_when_flag="flag:dawn")
        obj(m, f"sleeper_{n}_awake", f"spire_sleeper_{kin}_awake", (x, y), 2, 2, requires_flag="flag:dawn")
    # Bran holds the choke from the west gallery into the watch
    owed += pt.trainer_beat(m, tid="underways_watch_b", at=(12, 12), facing="down", sight=2,
                            sprite="hollowing_acolyte")
    # FD2: the watch KEPT changes the world — all three leave their posts for the fire
    owed += gathered(m, ("underways_watch_b",),
                     [("underways_watch_a", (14, 12), "right"),
                      ("underways_watch_b", (14, 13), "right"),
                      ("underways_watch_c", (16, 14), "up")])
    # the last Lumen Drop before the summit (the warm stones, round by the slump)
    owed += pt.cache(m, cid="underways_lumen", at=(29, 16))
    owed += pt.sign(m, deco, W, sid="underways_watch", at=(11, 10))
    owed += pt.sign(m, deco, W, sid="underways_warmstones", at=(27, 16))
    prop(m, "e_masonry", "masonry", (27, 6), 2, 2)
    prop(m, "s_masonry", "masonry", (17, 19), 2, 2)
    prop(m, "s_roots", "root_curtain", (22, 17), 2, 2, solid=False)
    obj(m, "glowshrooms", "glowmoss_deep_glowshrooms_teal", (8, 2), 2, 2, solid=False)
    obj(m, "warm_shrooms", "glowmoss_deep_glowshrooms_ember", (28, 20), 2, 2, solid=False)
    # FD2 (review r2: "B1's west bay and south gallery are still thin")
    prop(m, "wf_hoods", "hood_line", (6, 4), 2, 2)         # the west ladder foot
    prop(m, "wf_firewood", "firewood", (6, 2), 2, 1)
    prop(m, "wg_names", "name_slate", (4, 7), 1, 2)        # the west gallery's mouth
    prop(m, "al_butt", "water_butt", (3, 11), 1, 1)        # the sleepers' alcove
    brazier(m, "al_brazier", (8, 13))
    prop(m, "s_butt", "water_butt", (16, 18), 1, 1)        # the south gallery
    prop(m, "s_hoods", "hood_line", (20, 20), 2, 2)
    prop(m, "s_names", "name_slate", (22, 20), 1, 2)
    brazier(m, "s_brazier", (24, 19))                      # where it opens on the warm stones
    prop(m, "ef_butt", "water_butt", (28, 8), 1, 1)        # the east foot's nook
    for (x, y) in [(3, 4), (29, 8), (13, 18), (24, 21), (26, 9)]:
        if not wall[y * W + x] and not deco[y * W + x]:
            deco[y * W + x] = gid("boulder")
    pocket_zone = {"id": "underways_b1_warmstones", "terrain": "tall_grass",
                   "rect": {"tx": 24, "ty": 15, "w": 7, "h": 7}, "encounter_rate": 0.14,
                   "table": B1_POCKET}
    zones(m, W, H, moss, B1_CAVE, B1_MOSS, "underways_b1", B1_CAVE_DAY, B1_MOSS_DAY,
          extra=[(pocket_zone, B1_POCKET_DAY)])
    keep = {(5, y) for y in range(3, 12)} | {(x, 13) for x in range(8, 13)}
    keep |= {(x, 5) for x in range(13, 19)} | {(25, y) for y in range(6, 16)}
    keep |= {(x, 12) for x in range(20, 25)} | {(14, y) for y in range(15, 20)}
    keep |= {(15, y) for y in range(6, 10)} | {(16, y) for y in range(6, 10)}
    dress(m, W, H, wall, allmoss, deco, rng, keep)
    return m, owed


if __name__ == "__main__":
    ok = True
    for build in (build_f1, build_b1):
        m, owed = build()
        ok = mk.finalize(m, scale=3) and ok
        pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
