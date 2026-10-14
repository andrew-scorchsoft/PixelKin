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
      the SW mouth; the watcher Odalie; a Starglass Shard in the side bay) and the
      EAST galleries (out to the SE mouth; the watcher Hesk). Neither half reaches
      the other except through B1.
  penumbra_underways_b1  (B1, 32x24) "The Underways — the Last Watch"
      The Hollowing's last watch keeps its fire here, under the Spire's roots: the
      watch-fire is a REST POINT (script.underways_watchfire_rest), Old Maudry keeps
      it, the watcher Bran holds the west gallery's choke. North of the fire the
      roots open on THE SPIRE'S SHAFT — the foot of a pit the Crown's light falls
      down from impossibly high (seen, never climbed: a solid prop, no warp). The
      LAST LUMEN DROP before the summit waits in the south-east pocket.

The strongest wild beds before Còr: the galleries roll Dark (cave, rect-wide),
the glow-moss beds roll Light — the two halves of the dark, side by side.
Never connected to the Umbral Spire: you always come back out into the Ring.

Warps (all mutual; the audit pairs them):
  F1 (3,1)/(4,1)   `to_ring_w`/`_e` -> penumbra_ring (4,31)/(5,31)   [Ring `to_underways_w` (4,32)/(5,32)]
  F1 (26,1)/(27,1) `to_ring_se`/`_e` -> penumbra_ring (22,31)/(23,31) [Ring `to_underways_e` (22,32)/(23,32)]
  F1 (6,18)  `ladder_down_w` <-> B1 (5,3)  `ladder_up_w`
  F1 (23,18) `ladder_down_e` <-> B1 (26,3) `ladder_up_e`

Levels: F1 52-55, B1 54-56. Mirrored in build_species.py (UNDERWAYS_TABLES).

Run:  python3 tools/maps/build_penumbra_underways.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import warp_markers as wm
from mapkit import gid

MUSIC = "assets/audio/music/penumbra-underways.mp3"
BACKDROP = ["assets/backgrounds/battle/underways-a.webp"]
AMBIENCE = {"particles": [{"kind": "dust", "density": 0.35}, {"kind": "starglint", "density": 0.35}],
            "tint": {"color": "#0a0818", "alpha": 0.16}, "sound_bed": "amb-drips"}


def carve(W, H, rooms, rng):
    """Rect rooms, each roughened with two small bites so the galleries read as
    worked rock settling, never a ruled box (the Bell Cellar's carve)."""
    wall = mk.make_grid(W, H)
    mk.rect(wall, W, H, 0, 0, W - 1, H - 1)
    floor = mk.make_grid(W, H)
    for (x0, y0, x1, y1) in rooms:
        mk.rect(floor, W, H, x0, y0, x1, y1)
    for (x0, y0, x1, y1) in rooms:
        if (x1 - x0) < 3 or (y1 - y0) < 2:
            continue
        for _ in range(2):
            side = rng.choice("nsew")
            if side in "ns":
                cx, cy = rng.randint(x0 + 1, x1 - 1), (y0 if side == "n" else y1)
            else:
                cx, cy = (x0 if side == "w" else x1), rng.randint(y0 + 1, y1 - 1)
            for y in range(cy - 1, cy + 2):
                for x in range(cx - 1, cx + 2):
                    if 1 <= x <= W - 2 and 1 <= y <= H - 2 and abs(x - cx) + abs(y - cy) <= 1:
                        floor[y * W + x] = 1
    for i in range(W * H):
        if floor[i]:
            wall[i] = 0
    return wall, floor


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


def zones(m, W, H, moss, cave_table, moss_table, prefix):
    out = [{"id": f"{prefix}_galleries", "terrain": "cave", "rect": {"tx": 0, "ty": 0, "w": W, "h": H},
            "encounter_rate": 0.07, "table": cave_table}]
    out += pt.zones_from_grid(moss, W, H, terrain="tall_grass", rate=0.12, table=moss_table,
                              id_prefix=f"{prefix}_moss")
    m["encounters"] = out


def dress(m, W, H, wall, moss, deco, rng, keep):
    """Drained dressing on the open floor (greymoss, grit, a rare glowshroom) and
    crag-bits on the wall tops, never on a busy tile or the lanes in `keep`."""
    busy = {(o["at"]["tx"] + dx, o["at"]["ty"] + dy) for o in m["objects"]
            for dx in range(o["w"]) for dy in range(o["h"])}
    busy |= {(p["at"]["tx"], p["at"]["ty"]) for p in m["npcs"] + m["triggers"] + m["warps"]}
    busy |= {(p["to"]["tx"], p["to"]["ty"]) for p in m["warps"]}
    bits = [gid("greymoss_a"), gid("greymoss_b"), gid("g_pebble"), gid("g_pebble"), gid("glowshroom_a")]
    for y in range(H):
        for x in range(W):
            i = y * W + x
            if wall[i] or moss[i] or deco[i] or (x, y) in busy or (x, y) in keep:
                continue
            if rng.random() < 0.16:
                deco[i] = rng.choice(bits)


# =============================================================================== F1
F1_CAVE = [
    {"kin_id": 138, "weight": 24, "min_level": 52, "max_level": 54},  # Voidmantle
    {"kin_id": 113, "weight": 18, "min_level": 52, "max_level": 54},  # Omenire
    {"kin_id": 143, "weight": 16, "min_level": 52, "max_level": 54},  # Whorlix
    {"kin_id": 15, "weight": 14, "min_level": 53, "max_level": 55},   # Pyriven
    {"kin_id": 85, "weight": 14, "min_level": 53, "max_level": 55},   # Stillwarden
    {"kin_id": 135, "weight": 14, "min_level": 53, "max_level": 55},  # Liminalux
]
F1_MOSS = [
    {"kin_id": 127, "weight": 30, "min_level": 52, "max_level": 54},  # Lunvane
    {"kin_id": 135, "weight": 25, "min_level": 53, "max_level": 55},  # Liminalux
    {"kin_id": 107, "weight": 20, "min_level": 53, "max_level": 55},  # Lunarbel
    {"kin_id": 40, "weight": 15, "min_level": 53, "max_level": 55},   # Lumenmoss (never wild before)
    {"kin_id": 140, "weight": 10, "min_level": 54, "max_level": 55},  # Wisprestored
]
B1_CAVE = [
    {"kin_id": 135, "weight": 24, "min_level": 54, "max_level": 56},  # Liminalux
    {"kin_id": 138, "weight": 22, "min_level": 54, "max_level": 56},  # Voidmantle
    {"kin_id": 113, "weight": 16, "min_level": 54, "max_level": 56},  # Omenire
    {"kin_id": 142, "weight": 14, "min_level": 54, "max_level": 56},  # Embergone
    {"kin_id": 143, "weight": 14, "min_level": 54, "max_level": 56},  # Whorlix
    {"kin_id": 144, "weight": 6, "min_level": 55, "max_level": 56},   # Nullhusk (the deep's rare)
]
B1_MOSS = [
    {"kin_id": 40, "weight": 26, "min_level": 54, "max_level": 56},   # Lumenmoss
    {"kin_id": 107, "weight": 22, "min_level": 54, "max_level": 56},  # Lunarbel
    {"kin_id": 127, "weight": 20, "min_level": 54, "max_level": 56},  # Lunvane
    {"kin_id": 37, "weight": 14, "min_level": 55, "max_level": 56},   # Prismara
    {"kin_id": 135, "weight": 12, "min_level": 54, "max_level": 56},  # Liminalux
    {"kin_id": 129, "weight": 6, "min_level": 56, "max_level": 56},   # Dawnwatcher (the moss's rare)
]


def build_f1() -> tuple[dict, list[str]]:
    W, H = 30, 22
    rng = random.Random(5201)
    rooms = [
        # ---- the WEST galleries (x 1-13) ----
        (2, 1, 6, 5),         # the SW mouth's stair-foot
        (2, 5, 9, 8),         # the first gallery
        (9, 6, 12, 7),        # east spur to the side bay
        (10, 3, 13, 9),       # the side bay (the Starglass, behind a moss bed)
        (4, 8, 4, 11),        # the 1-wide cut south (Odalie watches it)
        (2, 11, 11, 15),      # the old cistern hall
        (4, 15, 9, 19),       # the ladder vault (down to the Last Watch)
        # ---- the EAST galleries (x 16-28) ----
        (24, 1, 28, 4),       # the SE mouth's stair-foot
        (21, 4, 28, 7),       # the long gallery
        (21, 7, 22, 12),      # the cut south
        (16, 11, 26, 14),     # the doused-lamp hall
        (20, 14, 26, 19),     # the ladder vault
        (17, 15, 19, 19),     # a moss pocket west of the vault
    ]
    wall, floor = carve(W, H, rooms, rng)
    for y in range(H):                                 # the Ring's foundations split the halves
        for x in (14, 15):
            wall[y * W + x] = 1
            floor[y * W + x] = 0
    moss = mk.make_grid(W, H)
    mk.blob(moss, W, H, 11.0, 6.0, 1.6, 1.4)          # the side bay's moss (Starglass behind)
    mk.blob(moss, W, H, 7.0, 13.2, 2.4, 1.3)          # the cistern hall's bed
    mk.blob(moss, W, H, 18.0, 17.0, 1.4, 2.0)          # the east moss pocket
    mk.blob(moss, W, H, 24.5, 5.6, 1.8, 1.1)          # the long gallery
    for i in range(W * H):
        if not floor[i]:
            moss[i] = 0
    deco = mk.make_grid(W, H)
    m = mapdict("penumbra_underways", "The Underways", W, H, ground(W, H, rng),
                layers_for(wall, moss), deco)
    owed: list[str] = []
    ring_gate = {"requires_flag": "flag:hub_unlocked", "requires_ability": "starreach"}
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
    del ring_gate
    pt.cave_ladder(m, deco, W, kind="down", at=(6, 18), to_map="penumbra_underways_b1",
                   to=(5, 3), wid="ladder_down_w")
    pt.cave_ladder(m, deco, W, kind="down", at=(23, 18), to_map="penumbra_underways_b1",
                   to=(26, 3), wid="ladder_down_e")
    wm.add(m, wm.marker("stair_w", "steps_n", 3, 0), wm.marker("stair_w_e", "steps_n", 4, 0),
           wm.marker("stair_se", "steps_n", 26, 0), wm.marker("stair_se_e", "steps_n", 27, 0))
    # the watchers (the last watch's outer posts)
    owed += pt.trainer_beat(m, tid="underways_watch_a", at=(4, 7), facing="down", sight=4,
                            sprite="hollowing_acolyte")
    owed += pt.trainer_beat(m, tid="underways_watch_c", at=(23, 8), facing="left", sight=2,
                            sprite="hollowing_acolyte")
    owed += pt.cache(m, cid="underways_starglass", at=(12, 4))
    owed += pt.sign(m, deco, W, sid="underways_mouth", at=(6, 2))
    # dressing: the watch's hooded lamps, doused lamps down the east hall, the cistern
    obj(m, "watch_lamp_a", "underways_watch_lamp", (2, 5), 1, 2, overhang=1, hidden_when_flag="flag:dawn")
    obj(m, "watch_lamp_a_lit", "underways_watch_lamp_lit", (2, 5), 1, 2, overhang=1, requires_flag="flag:dawn")
    obj(m, "watch_lamp_c", "underways_watch_lamp", (28, 5), 1, 2, overhang=1, hidden_when_flag="flag:dawn")
    obj(m, "watch_lamp_c_lit", "underways_watch_lamp_lit", (28, 5), 1, 2, overhang=1, requires_flag="flag:dawn")
    for n, x in enumerate((17, 20, 23, 26)):
        obj(m, f"doused_{n}", "coldfog_doused_lamp", (x, 10), 1, 3, overhang=2, walk_under=True)
    obj(m, "null_rack", "coldfog_null_rack", (7, 11), 4, 2, overhang=1)
    obj(m, "null_pool", "spire_null_pool", (9, 14), 2, 2)
    obj(m, "glowshrooms", "glowmoss_deep_glowshrooms_teal", (17, 18), 2, 2, solid=False)
    obj(m, "bedrolls", "coldfog_quiet_camp", (24, 15), 3, 2)
    for (x, y) in [(8, 5), (2, 15), (11, 11), (26, 7), (16, 14), (21, 19)]:
        if not wall[y * W + x]:
            deco[y * W + x] = gid("boulder")
    for (x, y) in [(6, 5), (12, 9), (25, 4), (16, 11)]:
        if not wall[y * W + x] and not deco[y * W + x]:
            deco[y * W + x] = gid("null_lantern")
    zones(m, W, H, moss, F1_CAVE, F1_MOSS, "underways_f1")
    keep = {(x, y) for x in (3, 4, 26, 27) for y in (1, 2, 3)}
    keep |= {(4, y) for y in range(7, 12)} | {(21, y) for y in range(7, 13)} | {(22, y) for y in range(7, 13)}
    dress(m, W, H, wall, moss, deco, rng, keep)
    return m, owed


# =============================================================================== B1
def build_b1() -> tuple[dict, list[str]]:
    W, H = 32, 24
    rng = random.Random(5202)
    rooms = [
        (3, 2, 8, 6),         # the west ladder foot
        (4, 6, 6, 12),        # the west gallery, south
        (2, 11, 9, 16),       # the sleepers' alcove + Bran's choke
        (9, 13, 12, 14),      # Bran's choke (2 wide)
        (12, 9, 20, 17),      # THE LAST WATCH (the fire, Maudry)
        (14, 6, 18, 9),       # north: the roots open on the shaft
        (12, 1, 20, 6),       # THE SHAFT CHAMBER (the vista)
        (20, 12, 24, 13),     # east out of the watch
        (23, 3, 29, 9),       # the east ladder foot
        (24, 9, 26, 13),      # the east ladder cut
        (13, 17, 15, 21),     # south out of the watch
        (15, 19, 27, 21),     # the south gallery
        (24, 15, 29, 21),     # the SE pocket (the Lumen Drop) + its moss
        (25, 13, 25, 15),     # the slump: east cut -> the pocket (down only)
    ]
    wall, floor = carve(W, H, rooms, rng)
    moss = mk.make_grid(W, H)
    mk.blob(moss, W, H, 5.0, 9.5, 1.2, 2.2)           # the west gallery (a mandatory brush)
    mk.blob(moss, W, H, 27.0, 17.0, 2.0, 1.8)          # the SE pocket's bed
    mk.blob(moss, W, H, 19.5, 20.2, 2.4, 0.9)          # the south gallery
    mk.blob(moss, W, H, 26.5, 6.5, 1.8, 1.2)           # the east foot
    for i in range(W * H):
        if not floor[i]:
            moss[i] = 0
    deco = mk.make_grid(W, H)
    m = mapdict("penumbra_underways_b1", "The Underways", W, H, ground(W, H, rng),
                layers_for(wall, moss), deco)
    m["display_name"] = "The Last Watch"
    owed: list[str] = []
    pt.cave_ladder(m, deco, W, kind="up", at=(5, 3), to_map="penumbra_underways",
                   to=(6, 18), wid="ladder_up_w")
    pt.cave_ladder(m, deco, W, kind="up", at=(26, 3), to_map="penumbra_underways",
                   to=(23, 18), wid="ladder_up_e")
    # THE SLUMP (the loop): a rubble step from the east cut drops into the SE pocket —
    # the Lumen Drop is seen from the cut and reached by the drop; the way back is round
    # by the south gallery and the watch.
    deco[14 * W + 25] = gid("scree_ledge_s")
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
    # THE LAST WATCH: the fire (rest point), Maudry, the watch's bedrolls
    obj(m, "watch_camp", "penumbra_vigil_camp", (15, 11), 3, 2)
    for tx in (15, 16, 17):
        m["triggers"].append({"id": f"watchfire_{tx}", "kind": "cutscene", "at": {"tx": tx, "ty": 13},
                              "activation": "interact", "ref": "script.underways_watchfire_rest"})
    owed.append("script.underways_watchfire_rest")
    obj(m, "bedrolls", "coldfog_quiet_camp", (12, 15), 3, 2)
    obj(m, "blankets", "mournfields_blanket_stack", (18, 15), 2, 1)
    obj(m, "watch_lamp_n", "underways_watch_lamp", (13, 9), 1, 2, overhang=1, hidden_when_flag="flag:dawn")
    obj(m, "watch_lamp_n_lit", "underways_watch_lamp_lit", (13, 9), 1, 2, overhang=1, requires_flag="flag:dawn")
    obj(m, "watch_lamp_e", "underways_watch_lamp", (20, 9), 1, 2, overhang=1, hidden_when_flag="flag:dawn")
    obj(m, "watch_lamp_e_lit", "underways_watch_lamp_lit", (20, 9), 1, 2, overhang=1, requires_flag="flag:dawn")
    m["npcs"].append({"id": "maudry", "at": {"tx": 18, "ty": 12}, "facing": "left",
                      "sprite": "hollowing_elder", "movement": "static",
                      "dialogue_ref": "script.underways_maudry"})
    owed.append("script.underways_maudry")
    # the sleepers' alcove (kin the watch keeps asleep — awake after the dawn)
    for n, (kin, (x, y)) in enumerate([("nullmoth", (2, 12)), ("cindersob", (2, 14)),
                                       ("voidmantle", (7, 11))]):
        obj(m, f"sleeper_{n}", f"spire_sleeper_{kin}", (x, y), 2, 2, hidden_when_flag="flag:dawn")
        obj(m, f"sleeper_{n}_awake", f"spire_sleeper_{kin}_awake", (x, y), 2, 2, requires_flag="flag:dawn")
    # Bran holds the choke from the west gallery into the watch
    owed += pt.trainer_beat(m, tid="underways_watch_b", at=(12, 12), facing="down", sight=2,
                            sprite="hollowing_acolyte")
    # the last Lumen Drop before the summit (the SE pocket, round by the south gallery)
    owed += pt.cache(m, cid="underways_lumen", at=(28, 16))
    owed += pt.sign(m, deco, W, sid="underways_watch", at=(12, 9))
    obj(m, "null_pool", "spire_null_pool", (22, 19), 2, 2)
    obj(m, "glowshrooms", "glowmoss_deep_glowshrooms_teal", (8, 3), 2, 2, solid=False)
    for (x, y) in [(3, 5), (29, 8), (12, 17), (25, 21), (24, 19)]:
        if not wall[y * W + x] and not deco[y * W + x]:
            deco[y * W + x] = gid("boulder")
    zones(m, W, H, moss, B1_CAVE, B1_MOSS, "underways_b1")
    keep = {(5, y) for y in range(3, 12)} | {(x, y) for x in range(9, 13) for y in (13, 14)}
    keep |= {(x, 5) for x in range(13, 19)} | {(26, y) for y in range(3, 14)}
    dress(m, W, H, wall, moss, deco, rng, keep)
    return m, owed


if __name__ == "__main__":
    ok = True
    for build in (build_f1, build_b1):
        m, owed = build()
        ok = mk.finalize(m, scale=3) and ok
        pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
