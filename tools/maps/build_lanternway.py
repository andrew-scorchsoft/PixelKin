#!/usr/bin/env python3
"""
The Lanternway — the five spoke LANE maps (graph.ts `lanternway_*`, kind `route`).

Phase 1 of the topology fix (2026-06): the spokes between the rim towns and the
Vesper Crossroads used to be zero-length edge-warps — walking E,E from Tinderwick
teleported you ~90 route-tiles, the "wormhole" that broke players' mental map.
Each spoke is now a real country-lane map that BENDS VISIBLY inside itself, so
every transition is locally truthful and the hub's gates radiate by true bearing
(the crossroads' Galehigh/Nightreach gates swap roads: NW vertical road -> the
due-north Galehigh spoke, west road -> the due-west Nightreach spoke).

Identity (atlas §3 "Lanternway"): hedged, lantern-lined country lanes — safe lit
ground, NO wild encounters (canon: "the lit east lane is safe", the opening
errand walks the Tinderwick spoke pre-starter) and no trainers. Each lane gets
the kit instead: lamp-posts pacing the lane, a milestone sign at the bend, one
cache in an off-lane pocket (variety rule), and one accent (pond / outcrop /
crown trees) so no screen is flat (§11).

Gating note: a spoke's Gleam gate lives on the CROSSROADS-side warp into the
lane (the Waykeeper's "not yet"); the town side stays open — one-way return
compression, the standing per-town rule.

audit_flow WAIVER — `free-pass` and `loop` WARNs accepted on ALL five lanes:
the Lanternway is canon SAFE ground (no encounters, no trainers, no story
chokes — "keep to the lamps"), so end-to-end free passage IS the design; and a
lane is a connector, not a level — the §3a loop rule belongs to the routes it
links, not to the lit road between them.

Run:  ./venv/bin/python tools/maps/build_lanternway.py   (from the repo root)
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

GRASS = ("grass0", "grass1", "grass2", "grass3")


def base_grid(W, H, rng):
    gg = [gid(n) for n in GRASS]
    return [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]


def punch(tree, W, H, cells):
    for (x, y) in cells:
        tree[y * W + x] = 0


def lamp(oid, tx, ty):
    return {"id": oid, "sprite": "tinderwick_lamp_post", "at": {"tx": tx, "ty": ty},
            "w": 1, "h": 3, "overhang": 2, "walk_under": True}


def tree_obj(oid, tx, ty):
    return {"id": oid, "sprite": "tinderwick_tree", "at": {"tx": tx, "ty": ty},
            "w": 3, "h": 4, "overhang": 3, "walk_under": True}


def object_cells(objects):
    return {(x, y) for o in objects
            for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
            for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}


def build_h_lane(*, map_id, display, seed, w_rows, e_rows, bend_x,
                 w_warps, e_warps, sign_id, cache_id, cache_at, pocket,
                 accent, lamps, trees, owed):
    """A horizontal lane: enters on the W edge rows `w_rows`, runs east, turns
    at `bend_x` and leaves on the E edge rows `e_rows` — the visible bend that
    absorbs the spoke's compass turn."""
    W, H = 24, 18
    rng = random.Random(seed)

    tree = mk.make_grid(W, H)
    mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=2,
                      bumps=[(5, 1, 1), (12, 1, 2), (19, 1, 1),
                             (4, H - 2, 2), (15, H - 2, 1)])
    mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)

    # the lane: west run -> bend column -> east run
    path = mk.make_grid(W, H)
    wy, ey = w_rows[0], e_rows[0]
    for y in w_rows:
        mk.hline(path, W, H, y, 0, bend_x + 1)
    for x in (bend_x, bend_x + 1):
        mk.vline(path, W, H, x, min(wy, ey), max(wy, ey) + 1)
    for y in e_rows:
        mk.hline(path, W, H, y, bend_x, W - 1)

    # the cache pocket: a small clearing carved off the lane
    px0, py0, px1, py1 = pocket
    for y in range(py0, py1 + 1):
        for x in range(px0, px1 + 1):
            tree[y * W + x] = 0

    # punch the borders where the lane leaves
    punch(tree, W, H, [(x, y) for y in w_rows for x in (0, 1)])
    punch(tree, W, H, [(x, y) for y in e_rows for x in (W - 1, W - 2)])

    pond = mk.make_grid(W, H)
    if accent == "pond":
        mk.blob(pond, W, H, bend_x - 5, max(w_rows[1], e_rows[1]) + 3, 1.7, 1.2)
        for i in range(W * H):
            if pond[i]:
                tree[i] = 0
    elif accent == "outcrop":
        pass  # boulders go on deco below

    for i in range(W * H):  # the lane wins over everything
        if path[i]:
            tree[i] = 0
            pond[i] = 0

    base = base_grid(W, H, rng)
    objects = [lamp(f"lamp_{i}", x, y) for i, (x, y) in enumerate(lamps)]
    objects += [tree_obj(f"crown_{i}", x, y) for i, (x, y) in enumerate(trees)]

    deco = mk.make_grid(W, H)
    if accent == "outcrop":
        for (x, y) in [(bend_x - 4, 4), (bend_x - 3, 4), (bend_x - 4, 5)]:
            deco[y * W + x] = gid("boulder")
    for (x, y) in [(2, w_rows[0] - 2), (W - 4, e_rows[1] + 2)]:
        if 0 <= y < H and not tree[y * W + x] and not path[y * W + x]:
            deco[y * W + x] = gid("flowerbed_a") if (x + y) % 2 else gid("flowerbed_b")

    m = {
        "id": map_id, "display_name": display, "width": W, "height": H,
        "tile_width": 16, "tile_height": 16, "kind": "route",
        "tilesets": [mk.shared_tileset_ref()],
        "layers": [{"name": "base", "role": "base", "depth": 0, "data": base},
                   {"name": "t_tree", "role": "terrain", "terrain": "tree",
                    "set": "vesper_overworld_set", "depth": 0, "data": tree},
                   {"name": "t_pond", "role": "terrain", "terrain": "pond",
                    "set": "vesper_overworld_set", "depth": 0, "data": pond},
                   {"name": "t_path", "role": "terrain", "terrain": "path",
                    "set": "vesper_overworld_set", "depth": 0, "data": path},
                   {"name": "deco", "role": "deco", "depth": 5, "data": deco},
                   {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
        "objects": objects,
        "warps": w_warps + e_warps,
        "triggers": [], "encounters": [], "npcs": [], "gates": [],
        "music": "assets/audio/music/tinderwick-a.mp3",
    }
    owed += pt.sign(m, deco, W, sid=sign_id, at=(bend_x + 2, min(wy, ey) + 2 if wy != ey else wy + 2))
    owed += pt.cache(m, cid=cache_id, at=cache_at)

    covered = {(x, y) for y in range(H) for x in range(W)
               if tree[y * W + x] or pond[y * W + x] or path[y * W + x] or deco[y * W + x]}
    mk.scatter_decor(deco, base, W, H, rng, density=0.12,
                     avoid=covered | object_cells(objects) | {cache_at})
    return m


def build_v_lane(*, map_id, display, seed, n_cols, s_cols, n_warps, s_warps,
                 sign_id, cache_id, cache_at, pocket, lamps, trees, owed):
    """A vertical lane (the due-north Galehigh spoke): a NARROW straight climb
    with a waist — deep tree flanks so no empty off-lane field reads as an
    unpaid pocket; the one clearing is the cache's."""
    W, H = 14, 24
    rng = random.Random(seed)

    tree = mk.make_grid(W, H)
    mk.organic_border(tree, W, H, top=1, left=1, right=1, depth=3,
                      bumps=[(3, 1, 1), (10, 1, 1), (2, 7, 2), (11, 9, 2),
                             (2, 15, 2), (11, 18, 2)])
    mk.rect(tree, W, H, 0, H - 2, W - 1, H - 1)

    path = mk.make_grid(W, H)
    for x in n_cols:
        mk.vline(path, W, H, x, 0, H - 1)
    px0, py0, px1, py1 = pocket
    for y in range(py0, py1 + 1):
        for x in range(px0, px1 + 1):
            tree[y * W + x] = 0
    punch(tree, W, H, [(x, y) for x in n_cols for y in (0, 1)])
    punch(tree, W, H, [(x, y) for x in s_cols for y in (H - 1, H - 2)])
    for i in range(W * H):
        if path[i]:
            tree[i] = 0

    base = base_grid(W, H, rng)
    objects = [lamp(f"lamp_{i}", x, y) for i, (x, y) in enumerate(lamps)]
    objects += [tree_obj(f"crown_{i}", x, y) for i, (x, y) in enumerate(trees)]

    deco = mk.make_grid(W, H)
    # the climb's outcrop accent, west of the waist
    for (x, y) in [(3, 12), (4, 12), (3, 13)]:
        deco[y * W + x] = gid("boulder")

    m = {
        "id": map_id, "display_name": display, "width": W, "height": H,
        "tile_width": 16, "tile_height": 16, "kind": "route",
        "tilesets": [mk.shared_tileset_ref()],
        "layers": [{"name": "base", "role": "base", "depth": 0, "data": base},
                   {"name": "t_tree", "role": "terrain", "terrain": "tree",
                    "set": "vesper_overworld_set", "depth": 0, "data": tree},
                   {"name": "t_path", "role": "terrain", "terrain": "path",
                    "set": "vesper_overworld_set", "depth": 0, "data": path},
                   {"name": "deco", "role": "deco", "depth": 5, "data": deco},
                   {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)}],
        "objects": objects,
        "warps": n_warps + s_warps,
        "triggers": [], "encounters": [], "npcs": [], "gates": [],
        "music": "assets/audio/music/tinderwick-a.mp3",
    }
    owed += pt.sign(m, deco, W, sid=sign_id, at=(n_cols[1] + 2, 11))
    owed += pt.cache(m, cid=cache_id, at=cache_at)

    covered = {(x, y) for y in range(H) for x in range(W)
               if tree[y * W + x] or path[y * W + x] or deco[y * W + x]}
    mk.scatter_decor(deco, base, W, H, rng, density=0.12,
                     avoid=covered | object_cells(objects) | {cache_at})
    return m


def W_(wid, tx, ty, to_map, to, facing, **kw):
    w = {"id": wid, "at": {"tx": tx, "ty": ty}, "trigger": "step_on",
         "to_map": to_map, "to": {"tx": to[0], "ty": to[1]}, "facing": facing,
         "transition": "fade"}
    w.update(kw)
    return w


def main() -> int:
    owed: list[str] = []
    maps = []

    # 1 · Tinderwick spoke — leaves the town east, the lane bends NORTH-EAST up
    # to the hub (the ring bearing): enter low on the W edge, leave high on the E.
    maps.append(build_h_lane(
        map_id="lanternway_tinderwick", display="Lanternway · Tinderwick Spoke",
        seed=61, w_rows=(12, 13), e_rows=(5, 6), bend_x=14,
        w_warps=[W_("to_tinderwick", 0, 12, "tinderwick", (26, 16), "left"),
                 W_("to_tinderwick_s", 0, 13, "tinderwick", (26, 16), "left")],
        e_warps=[W_("to_crossroads", 23, 5, "vesper_crossroads", (0, 8), "right"),
                 W_("to_crossroads_s", 23, 6, "vesper_crossroads", (0, 9), "right")],
        sign_id="lanternway_tinderwick", cache_id="lane_tinderwick",
        cache_at=(20, 14), pocket=(18, 13, 21, 15),
        accent="pond", lamps=[(4, 10), (13, 8), (20, 3)], trees=[(5, 2), (17, 14)],
        owed=owed))

    # 2 · Pearlmoor spoke — leaves the hub east, bends SOUTH-EAST down to the
    # quay: enter high on the W edge, leave low on the E.
    maps.append(build_h_lane(
        map_id="lanternway_pearlmoor", display="Lanternway · Pearlmoor Spoke",
        seed=62, w_rows=(5, 6), e_rows=(12, 13), bend_x=9,
        w_warps=[W_("to_crossroads", 0, 5, "vesper_crossroads", (19, 8), "left"),
                 W_("to_crossroads_s", 0, 6, "vesper_crossroads", (19, 9), "left")],
        e_warps=[W_("to_pearlmoor", 23, 12, "pearlmoor_quay", (1, 12), "right"),
                 W_("to_pearlmoor_s", 23, 13, "pearlmoor_quay", (1, 12), "right")],
        sign_id="lanternway_pearlmoor", cache_id="lane_pearlmoor",
        cache_at=(19, 4), pocket=(17, 3, 20, 5),
        accent="pond", lamps=[(4, 3), (12, 8), (20, 10)], trees=[(15, 1), (4, 13)],
        owed=owed))

    # 3 · Lowleaf spoke — leaves the hub east, climbs NORTH-EAST to the Bloom:
    # enter low on the W edge, leave high on the E.
    maps.append(build_h_lane(
        map_id="lanternway_lowleaf", display="Lanternway · Lowleaf Spoke",
        seed=63, w_rows=(12, 13), e_rows=(4, 5), bend_x=13,
        w_warps=[W_("to_crossroads", 0, 12, "vesper_crossroads", (19, 3), "left"),
                 W_("to_crossroads_s", 0, 13, "vesper_crossroads", (19, 4), "left")],
        e_warps=[W_("to_lowleaf", 23, 4, "lowleaf_hollow", (1, 14), "right"),
                 W_("to_lowleaf_s", 23, 5, "lowleaf_hollow", (1, 15), "right")],
        sign_id="lanternway_lowleaf", cache_id="lane_lowleaf",
        cache_at=(11, 9), pocket=(10, 8, 12, 10),
        accent="outcrop", lamps=[(4, 10), (14, 7), (20, 2)], trees=[(8, 14), (18, 12)],
        owed=owed))

    # 4 · Galehigh spoke — DUE NORTH out of the hub (the re-edged gate): a
    # straight lamplit climb, galehigh's cliff country closing in.
    maps.append(build_v_lane(
        map_id="lanternway_galehigh", display="Lanternway · Galehigh Spoke",
        seed=64, n_cols=(6, 7), s_cols=(6, 7),
        n_warps=[W_("to_galehigh", 6, 0, "galehigh_terraces", (15, 30), "up"),
                 W_("to_galehigh_e", 7, 0, "galehigh_terraces", (16, 30), "up")],
        s_warps=[W_("to_crossroads", 6, 23, "vesper_crossroads", (3, 1), "down"),
                 W_("to_crossroads_e", 7, 23, "vesper_crossroads", (4, 1), "down")],
        sign_id="lanternway_galehigh", cache_id="lane_galehigh",
        cache_at=(10, 5), pocket=(9, 4, 11, 6),
        lamps=[(4, 4), (9, 14), (4, 19)], trees=[(9, 19)],
        owed=owed))

    # 5 · Nightreach spoke — the observatory road drops SOUTH into the lane,
    # which bends EAST to the hub's west gate (the re-edged side).
    maps.append(build_h_lane(
        map_id="lanternway_nightreach", display="Lanternway · Nightreach Spoke",
        seed=65, w_rows=(12, 13), e_rows=(12, 13), bend_x=4,
        w_warps=[],  # the west run is replaced by the NORTH drop below
        e_warps=[W_("to_crossroads", 23, 12, "vesper_crossroads", (1, 3), "right"),
                 W_("to_crossroads_s", 23, 13, "vesper_crossroads", (1, 4), "right")],
        sign_id="lanternway_nightreach", cache_id="lane_nightreach",
        cache_at=(19, 4), pocket=(17, 3, 20, 5),
        accent="outcrop", lamps=[(7, 9), (14, 9), (20, 9)], trees=[(9, 2), (15, 14)],
        owed=owed))
    # graft the north drop onto the nightreach lane (vertical leg cols 4-5)
    n = maps[-1]
    W, H = n["width"], n["height"]
    tree_l = next(l for l in n["layers"] if l["name"] == "t_tree")["data"]
    path_l = next(l for l in n["layers"] if l["name"] == "t_path")["data"]
    for x in (4, 5):
        for y in range(0, 14):
            path_l[y * W + x] = 1
            tree_l[y * W + x] = 0
    for x in (4, 5):
        for y in (0, 1):
            tree_l[y * W + x] = 0
    # the W-edge stub the template punched isn't a road here — regrow the border
    for y in (12, 13):
        for x in (0, 1):
            tree_l[y * W + x] = 1
            path_l[y * W + x] = 0
    n["warps"] = [W_("to_nightreach", 4, 0, "nightreach_observatory", (4, 28), "up"),
                  W_("to_nightreach_e", 5, 0, "nightreach_observatory", (5, 28), "up")] + n["warps"]

    ok = True
    for m in maps:
        print(f"=== {m['id']} ===")
        ok = mk.finalize(m, scale=3) and ok
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
