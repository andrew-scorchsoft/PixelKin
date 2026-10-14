#!/usr/bin/env python3
"""
world_layout — the world-map model: does Vesperholm SPATIALLY align, and what
should the player's world-map screen draw?

Three jobs:

1. METRIC AUDIT — chain every straight edge link tile-accurately (A's exit tile
   and B's landing tile must be adjacent) and report how far each rim loop
   miscloses, in real tiles. This quantifies the "wormhole" feel: the Lanternway
   spokes are ~20-tile lanes between towns that sit 60–90 route-tiles apart, so
   a literal embedding is impossible — the world map must be SCHEMATIC (the
   genre convention) and the numbers here are the evidence.

2. RING LAYOUT — the canonical schematic: the atlas's "ring of valleys around
   the Umbral Spire", hand-authored node positions (area-level: towns, routes,
   dungeon mouths, landmark spurs) in a 220x140 virtual box. Every straight
   shipped link is checked against the layout's bearing; disagreements are
   reported with a suggested fix (move the gate edge, or accept the bend) so
   the map and the walked world converge over time instead of drifting.

3. OUTPUTS — renders the layout to tools/maps/out/world_layout.png (review
   artifact) and writes src/game/data/world/worldmap.json (nodes, roads, and a
   map-id -> node membership table) for the in-game WorldMapMenu.

Run from tools/maps/:  ../../venv/bin/python world_layout.py
(only the PNG render needs Pillow; everything else is stdlib).
"""
from __future__ import annotations

import json
import sys
from collections import deque

from worldmodel import GRAPH_TS, REPO, load_world

OUT_PNG = REPO / "tools/maps/out/world_layout.png"
OUT_JSON = REPO / "src/game/data/world/worldmap.json"

OVERWORLD_KINDS = {"town", "route", "hub"}
OPP = {"n": "s", "s": "n", "e": "w", "w": "e"}
STEP = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}

# ---------------------------------------------------------------------------
# THE HONEST NORTH-UP LAYOUT (2026-10 geometry fix). Node positions are no
# longer hand-placed on a schematic ring: they are the REAL centres of the maps
# as walked (world_geometry.py lays every outdoor map edge-to-edge at its true
# tile size), so the MAP screen draws exactly what the player walks — leave a
# map north and the next one IS north on the chart. Caves and landmarks that
# hang off a mid-map mouth sit at that mouth's tile in their host map. The
# world is tall (the long climb north), so the MAP screen fits the WIDTH and
# scrolls with the cursor (ui/WorldMapMenu.ts); `box` in worldmap.json gives
# the virtual size. Only the KIND of each node is authored here.
#   kind: town / route / dungeon / hub / landmark (landmarks draw as small dots)
# ---------------------------------------------------------------------------
NODE_KINDS: dict[str, str] = {
    # south
    "tinderwick": "town", "wickstead_green": "landmark", "dimglass_coast": "route",
    "dimglass_coast_ii": "route", "tideglass_cavern": "landmark", "gullcry_rock": "landmark",
    "pearlmoor_quay": "town", "pearlmoor_breakwater": "landmark", "pearlmoor_wanderwood": "landmark",
    "wayward_rise": "landmark",
    # Lane E (10 Part III): the bay under the beach + the drowned old town
    "tinderwick_bay": "route", "lowtinder": "town",
    "dawnstead": "town",
    # the hub + the bay road home + the mountain road
    "vesper_crossroads": "hub", "lanternway_tinderwick": "route",
    "wrackline_path": "route", "sounding_cave": "route", "lanternfall_road": "route",
    "umbral_approach": "route", "penumbra_ring": "route", "starwell": "landmark",
    "umbral_spire": "dungeon",
    # east
    "saltreach_fen_i": "route", "saltreach_fen_ii": "route", "sunkbell_shallows": "landmark",
    "lowleaf_hollow": "town", "lanternway_lowleaf": "route", "glowmoss_deep": "dungeon",
    "spore_grotto": "landmark", "cinderhead_mine": "town", "cinderhead_deep": "dungeon",
    # north
    "cinderwind_scarp": "route", "galehigh_terraces": "town", "lanternway_galehigh": "route",
    "wind_eye": "landmark", "windward_stair_i": "route", "windward_stair_ii": "route",
    "thunderroost": "landmark", "pale_vault_glacier": "town",
    "cinderwind_ashfall": "route", "cinderwind_kiln": "landmark",  # Lane A (walkthrough/10 Part II)
    # west
    "hushfrost_pass_i": "route", "hushfrost_pass_ii": "route", "aurora_hollow": "landmark",
    "sunken_solarium": "town", "unrisen_stair": "landmark", "sunvault_climb_i": "route",
    "sunvault_climb_ii": "route", "sunvault_climb_iii": "route", "sunvault_climb_iv": "route",
    "rimeway_ascent": "route", "rimeway_fold": "route", "rimeway_descent": "route",
    "helia_vault": "landmark", "nightreach_observatory": "town",
    "lanternway_nightreach": "route",
    # the marshes (off Nightreach)
    "coldfog_marches_ii": "route", "coldfog_marches_i": "route", "drownlight_beacon": "landmark",
    "hollowfen_stillworks": "landmark",
    "mourning_fields": "route",  # Lane N3 (walkthrough/11 Part C): the north loop
    # Lane N1 (11 Part A): the Hollowing's village, north of Coldfog I
    "stillwater": "town",
    # THE WILD WAYS — the Wick-Run (09 §2 A): Sunvault Climb I down the west flank to the sea
    "wickrun_crest": "route", "wickrun_chute": "route", "wickrun_trestles": "route",
    "wickrun_traverse": "route", "wickrun_lower": "route", "wickrun_foot": "route",
    # THE WILD WAYS — the Mirelights (east of Saltreach Fen I, over Ansel's ferry)
    "mirelight_landing": "route", "mirelight_glassmere": "route", "mirelight_chapel": "landmark",
    # THE FARLAMP ISLES (walkthrough/10 Part I, Lane C1): the sea south of the Point
    "farlamp_sound": "route", "farlamp_shelfwater": "route", "farlamp_fogwall": "route",
    "farlamp_gullwrack": "route", "farlamp_kelpcrown": "route", "driftholm": "town",
}
# places hung off a stacked interior chain, pinned near their anchor (tiles)
ANCHORED: dict[str, tuple[str, float, float]] = {
    "dawnstead": ("umbral_spire", 0.0, -22.0),   # the dawn town atop the mountain
}
BOX_W = 220            # virtual box width; height follows the world's aspect
MARGIN = 8             # virtual units of air round the drawing
NODES: dict[str, tuple[int, int, str]] = {}   # filled by compute_nodes()
BOX: dict[str, int] = {"width": BOX_W, "height": 140}


def compute_nodes(world: dict[str, dict]) -> None:
    """Fill NODES from the true walked layout (world_geometry.place)."""
    import world_geometry as wg
    straight, _bent, portal = wg.collect(world)
    pos, comp, _parent, _conf = wg.place(world, straight, "tinderwick")
    main = comp["tinderwick"]
    # components joined only by a lift/mouth (the Windward kite flight, cave
    # mouths) hang off it at their landing tile — never off a late shortcut
    wg.hang_components(world, pos, comp, portal)
    centre: dict[str, tuple[float, float]] = {}
    for mid, (x, y) in pos.items():
        if comp.get(mid) == main:
            centre[mid] = (x + world[mid]["width"] / 2, y + world[mid]["height"] / 2)
    # portal-only places with no straight links of their own (a cave, a lone
    # landmark) sit at their mouth tile in the host
    # interiors-free world: the Spire's upper floors are 'cave' kind too, so
    # collect() already listed their portals
    for _ in range(8):
        for r in portal:
            a, b = r["a"], r["b"]
            if a in centre and a in pos and b not in centre:
                centre[b] = (pos[a][0] + r["at"][0] + 0.5, pos[a][1] + r["at"][1] + 0.5)
                # its origin, so a cave chain (Glowmoss B1F -> Spore Grotto,
                # the Spire's floors -> Dawnstead) can keep hanging off it
                pos[b] = (pos[a][0] + r["at"][0] - r["to"][0], pos[a][1] + r["at"][1] - r["to"][1])
    # a place reached through a stacked interior chain (Dawnstead, off the
    # Spire's summit) has no meaningful offset of its own: pin it to its anchor
    for n, (anchor, dx, dy) in ANCHORED.items():
        if anchor in centre:
            centre[n] = (centre[anchor][0] + dx, centre[anchor][1] + dy)
    missing = [n for n in NODE_KINDS if n in world and n not in centre]
    for n in missing:
        print(f"  [W] unplaced     {n}: no straight link or placed portal reaches it")
    pts = [centre[n] for n in NODE_KINDS if n in centre]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    k = (BOX_W - 2 * MARGIN) / max(1.0, x1 - x0)
    BOX["height"] = int(round((y1 - y0) * k + 2 * MARGIN))
    for n, kind in NODE_KINDS.items():
        if n in centre:
            cx, cy = centre[n]
            NODES[n] = (int(round(MARGIN + (cx - x0) * k)), int(round(MARGIN + (cy - y0) * k)), kind)


# ---------------------------------------------------------------------------
# THE CLASSIC GRID (2026-10). The MAP screen is the genre's town map: every
# place is ONE same-size square on a coarse grid, roads are straight runs of
# cells with right-angle bends, and the land is drawn round them. Map SIZE no
# longer shows (a route was drawn as big as a town). The grid comes from the
# honest layout: snap each node to a GRID_U cell, nudge collisions to the
# nearest free cell, then squeeze long empty stretches to MAX_GAP cells so the
# chart isn't mostly sea. Order is kept, so north is still north — and
# grid_honesty() FAILs any walked link the grid would draw backwards.
# ---------------------------------------------------------------------------
GRID_U = 10         # virtual units per grid cell before squeezing
MAX_GAP = 2         # longest empty run kept between occupied rows/columns
KIND_PRIORITY = {"hub": 0, "town": 1, "dungeon": 2, "route": 3, "landmark": 4}
# hand-picked raw cells for a nudge the nearest-free rule gets wrong (it put
# the Stillworks on the Nightreach road)
GRID_PIN: dict[str, tuple[int, int]] = {"hollowfen_stillworks": (12, 7)}
GRID: dict[str, tuple[int, int]] = {}
GRID_SIZE: dict[str, int] = {"cols": 0, "rows": 0}
ROAD_PATHS: dict[tuple[str, str], list[list[int]]] = {}


def compute_grid() -> list[str]:
    notes: list[str] = []
    taken: dict[tuple[int, int], str] = {}
    raw: dict[str, tuple[int, int]] = {}
    order = sorted(NODES, key=lambda n: (KIND_PRIORITY[NODES[n][2]], n))
    for n in order:
        x, y, _k = NODES[n]
        fx, fy = x / GRID_U, y / GRID_U
        cell = GRID_PIN.get(n, (round(fx), round(fy)))
        if cell in taken:
            near = sorted(
                ((cx, cy) for cx in range(cell[0] - 3, cell[0] + 4) for cy in range(cell[1] - 3, cell[1] + 4)
                 if (cx, cy) not in taken),
                key=lambda c: ((c[0] - fx) ** 2 + (c[1] - fy) ** 2, c[1], c[0]))
            notes.append(f"{n} nudged {cell} -> {near[0]} (shared a cell with {taken[cell]})")
            cell = near[0]
        taken[cell] = n
        raw[n] = cell

    def squeeze(vals: list[int]) -> dict[int, int]:
        out: dict[int, int] = {}
        prev = None
        for v in sorted(set(vals)):
            out[v] = 1 if prev is None else out[prev] + min(v - prev, MAX_GAP)
            prev = v
        return out

    cx = squeeze([c[0] for c in raw.values()])
    cy = squeeze([c[1] for c in raw.values()])
    for n, (gx, gy) in raw.items():
        GRID[n] = (cx[gx], cy[gy])
    GRID_SIZE["cols"] = max(g[0] for g in GRID.values()) + 2
    GRID_SIZE["rows"] = max(g[1] for g in GRID.values()) + 2
    return notes


def route_roads() -> list[str]:
    """Lay every road as right-angle runs of cells: try the two L-bends, then
    the Z-bends through each row/column between, and keep the one that crosses
    the fewest other places (then the fewest cells already carrying a road)."""
    notes: list[str] = []
    node_at = {c: n for n, c in GRID.items()}
    used: set[tuple[int, int]] = set()

    def cells(pts: list[tuple[int, int]]) -> list[tuple[int, int]]:
        out = []
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            sx = (bx > ax) - (bx < ax)
            sy = (by > ay) - (by < ay)
            x, y = ax, ay
            while (x, y) != (bx, by):
                x, y = x + sx, y + sy
                out.append((x, y))
        return out

    order = sorted(ROADS, key=lambda r: (r[2] == "car", r[2] != "road"))
    for a, b, kind in order:
        if a not in GRID or b not in GRID:
            continue
        A, B = GRID[a], GRID[b]
        if kind == "car" or A[0] == B[0] or A[1] == B[1]:
            ROAD_PATHS[(a, b)] = [list(A), list(B)]
            if kind != "car":
                hits = [node_at[c] for c in cells([A, B])[:-1] if c in node_at]
                if hits:
                    notes.append(f"{a} - {b} runs through {', '.join(hits)}")
                used.update(cells([A, B]))
            continue
        cands = [[A, (B[0], A[1]), B], [A, (A[0], B[1]), B]]
        for mx in range(min(A[0], B[0]) + 1, max(A[0], B[0])):
            cands.append([A, (mx, A[1]), (mx, B[1]), B])
        for my in range(min(A[1], B[1]) + 1, max(A[1], B[1])):
            cands.append([A, (A[0], my), (B[0], my), B])

        def score(pts):
            cs = cells(pts)[:-1]
            return (sum(c in node_at for c in cs), sum(c in used for c in cs), len(pts))
        best = min(cands, key=score)
        hits = [node_at[c] for c in cells(best)[:-1] if c in node_at]
        if hits:
            notes.append(f"{a} - {b} runs through {', '.join(hits)}")
        used.update(cells(best))
        ROAD_PATHS[(a, b)] = [list(p) for p in best]
    return notes


def grid_honesty(links, member) -> list[str]:
    """The grid must still draw every walked straight link the way it's walked."""
    fails, seen = [], set()
    for a, b, exit_e, _pin, _spread in links:
        na, nb = member.get(a), member.get(b)
        if na is None or nb is None or na == nb or na not in GRID or nb not in GRID:
            continue
        if (na, nb, exit_e) in seen:
            continue
        seen.add((na, nb, exit_e))
        dx, dy = GRID[nb][0] - GRID[na][0], GRID[nb][1] - GRID[na][1]
        along = {"n": -dy, "s": dy, "e": dx, "w": -dx}[exit_e]
        if along <= 0:
            fails.append(f"grid reversed {a} exits {exit_e.upper()} but the grid puts {nb} at ({dx:+d},{dy:+d})")
    return fails


# Roads drawn between nodes. kind: 'road' (walked route), 'lane' (Lanternway
# spoke — abstracted country lane), 'gate' (Gift/flag-gated passage), 'pass'
# (through-cave passage). Derived links are verified against shipped warps.
ROADS: list[tuple[str, str, str]] = [
    # south
    ("tinderwick", "dimglass_coast", "road"),
    ("tinderwick", "wickstead_green", "road"),   # via Duskapple Orchard's west gap
    ("dimglass_coast", "dimglass_coast_ii", "road"),
    ("dimglass_coast_ii", "pearlmoor_quay", "road"),
    ("dimglass_coast", "tideglass_cavern", "gate"),
    ("dimglass_coast_ii", "tideglass_cavern", "gate"),
    ("dimglass_coast_ii", "gullcry_rock", "gate"),
    # Lane E (10 Part III): swum with Tidecall off the beach, then east
    ("tinderwick", "tinderwick_bay", "gate"),
    ("tinderwick_bay", "lowtinder", "gate"),
    ("pearlmoor_quay", "pearlmoor_breakwater", "gate"),
    ("pearlmoor_quay", "pearlmoor_wanderwood", "road"),   # up through the allotment
    ("pearlmoor_wanderwood", "wayward_rise", "road"),     # north out of the glade
    ("umbral_spire", "dawnstead", "gate"),
    # the bay road home (Saltreach Fen I's drowned road -> the Crossroads)
    ("saltreach_fen_i", "wrackline_path", "road"),
    ("wrackline_path", "sounding_cave", "pass"),
    ("sounding_cave", "lanternfall_road", "pass"),
    ("lanternfall_road", "vesper_crossroads", "road"),
    ("tinderwick", "lanternway_tinderwick", "lane"),
    ("lanternway_tinderwick", "vesper_crossroads", "lane"),
    # east
    ("pearlmoor_quay", "saltreach_fen_i", "road"),
    ("saltreach_fen_i", "saltreach_fen_ii", "gate"),
    ("saltreach_fen_ii", "sunkbell_shallows", "gate"),
    ("saltreach_fen_ii", "lowleaf_hollow", "road"),
    ("lowleaf_hollow", "lanternway_lowleaf", "lane"),
    ("lowleaf_hollow", "glowmoss_deep", "gate"),
    ("glowmoss_deep", "spore_grotto", "gate"),
    ("glowmoss_deep", "cinderhead_mine", "pass"),
    ("cinderhead_mine", "cinderhead_deep", "gate"),
    ("cinderhead_deep", "cinderwind_scarp", "pass"),
    # north
    ("cinderwind_scarp", "galehigh_terraces", "gate"),   # the rockfall (open once cleared)
    ("cinderwind_scarp", "cinderwind_ashfall", "road"),  # Lane A: up onto the Ashfall Shelf
    ("cinderwind_ashfall", "galehigh_terraces", "road"),
    ("cinderwind_ashfall", "cinderwind_kiln", "gate"),   # the kiln stack's thermal (Kite)
    ("cinderwind_ashfall", "windward_stair_i", "gate"),  # the Windward gap (Kite)
    ("galehigh_terraces", "lanternway_galehigh", "lane"),
    ("galehigh_terraces", "wind_eye", "gate"),
    ("galehigh_terraces", "windward_stair_i", "road"),
    ("windward_stair_i", "windward_stair_ii", "gate"),
    ("windward_stair_ii", "thunderroost", "gate"),
    ("windward_stair_ii", "pale_vault_glacier", "road"),
    ("windward_stair_ii", "galehigh_terraces", "gate"),  # late shortcut
    # west
    ("pale_vault_glacier", "hushfrost_pass_i", "road"),
    ("hushfrost_pass_i", "hushfrost_pass_ii", "gate"),
    ("hushfrost_pass_ii", "aurora_hollow", "gate"),
    ("hushfrost_pass_ii", "sunken_solarium", "road"),
    ("sunken_solarium", "unrisen_stair", "gate"),
    ("sunken_solarium", "sunvault_climb_i", "road"),
    ("sunvault_climb_i", "sunvault_climb_ii", "gate"),
    ("sunvault_climb_ii", "helia_vault", "gate"),
    ("sunvault_climb_ii", "sunvault_climb_iii", "road"),
    ("sunvault_climb_iii", "sunvault_climb_iv", "road"),
    ("sunvault_climb_iv", "nightreach_observatory", "road"),
    ("nightreach_observatory", "lanternway_nightreach", "lane"),
    # the marshes (off Nightreach's east fog gate)
    ("nightreach_observatory", "coldfog_marches_ii", "gate"),
    ("coldfog_marches_ii", "coldfog_marches_i", "gate"),
    ("coldfog_marches_i", "drownlight_beacon", "gate"),
    ("coldfog_marches_ii", "hollowfen_stillworks", "gate"),
    ("coldfog_marches_i", "stillwater", "road"),  # Lane N1 (11 Part A)
    # the Rimeway (09-the-wild-ways §2 C): Pale Vault -> the Fold -> the Rime Gate -> the marsh
    ("pale_vault_glacier", "rimeway_ascent", "road"),
    ("rimeway_ascent", "rimeway_fold", "road"),
    ("rimeway_fold", "rimeway_descent", "gate"),
    ("coldfog_marches_ii", "rimeway_descent", "road"),
    ("coldfog_marches_i", "mourning_fields", "road"),   # Lane N3: the north loop
    ("mourning_fields", "rimeway_descent", "road"),     # ...and its col road down
    ("stillwater", "mourning_fields", "road"),          # closes the north loop
    # THE WILD WAYS — the Wick-Run (one-way chutes; the Tallow Lift is the ride home)
    ("sunvault_climb_i", "wickrun_crest", "road"),
    ("wickrun_crest", "wickrun_chute", "road"),
    ("wickrun_chute", "wickrun_trestles", "road"),
    ("wickrun_trestles", "wickrun_traverse", "road"),
    ("wickrun_traverse", "wickrun_lower", "road"),
    ("wickrun_lower", "wickrun_foot", "road"),
    ("wickrun_foot", "pearlmoor_quay", "road"),      # the beach road round Lightkeeper's Point
    # THE WILD WAYS — the Mirelights: the ferry is flag-gated, the boards are walked
    ("saltreach_fen_i", "mirelight_landing", "gate"),
    ("mirelight_landing", "mirelight_glassmere", "road"),
    ("mirelight_glassmere", "mirelight_chapel", "road"),
    # THE FARLAMP ISLES (Lane C1): rowed from the Point's slip / the Wick-Run's beach
    # (gated on Ione's skiff); the fog lets you through to Driftholm only with the glass
    ("pearlmoor_quay", "farlamp_sound", "gate"),      # the Point's launch slip
    ("wickrun_foot", "farlamp_shelfwater", "gate"),
    ("farlamp_sound", "farlamp_shelfwater", "road"),
    ("farlamp_shelfwater", "farlamp_fogwall", "road"),
    ("farlamp_sound", "farlamp_gullwrack", "road"),
    ("farlamp_shelfwater", "farlamp_kelpcrown", "road"),
    ("farlamp_gullwrack", "farlamp_kelpcrown", "road"),
    ("farlamp_fogwall", "driftholm", "gate"),
    # THE LANTERN-CAR (rides, not roads) + the Cinderhead ore-hoist
    ("lanternway_lowleaf", "vesper_crossroads", "car"),
    ("lanternway_galehigh", "vesper_crossroads", "car"),
    ("lanternway_nightreach", "vesper_crossroads", "car"),
    ("cinderhead_deep", "vesper_crossroads", "car"),
    ("wickrun_foot", "wickrun_crest", "car"),        # the Tallow Lift
    # the mountain road
    ("vesper_crossroads", "umbral_approach", "gate"),
    ("umbral_approach", "penumbra_ring", "road"),
    ("penumbra_ring", "starwell", "gate"),
    ("penumbra_ring", "umbral_spire", "gate"),
]


def edges_of(m: dict, tx: int, ty: int, tol: int) -> set[str]:
    out = set()
    if ty <= tol:
        out.add("n")
    if ty >= m["height"] - 1 - tol:
        out.add("s")
    if tx <= tol:
        out.add("w")
    if tx >= m["width"] - 1 - tol:
        out.add("e")
    return out


def straight_links(world: dict[str, dict]):
    """All overworld straight edge links: (a, b, exit_edge, pin) — pin is B's
    origin relative to A in tiles, averaged over a funnelled multi-tile gate."""
    pins: dict[tuple[str, str, str], list[tuple[int, int]]] = {}
    for mid, m in sorted(world.items()):
        if m.get("kind") not in OVERWORLD_KINDS:
            continue
        for w in m.get("warps", []):
            dst = world.get(w.get("to_map", ""))
            if dst is None or dst.get("kind") not in OVERWORLD_KINDS:
                continue
            ax, ay = w["at"]["tx"], w["at"]["ty"]
            bx, by = w["to"]["tx"], w["to"]["ty"]
            a_edges = edges_of(m, ax, ay, 0)
            b_edges = edges_of(dst, bx, by, 2)
            exit_e = next((e for e in a_edges if OPP[e] in b_edges), None)
            if exit_e is None:
                continue
            sx, sy = STEP[exit_e]
            pins.setdefault((mid, w["to_map"], exit_e), []).append((ax + sx - bx, ay + sy - by))
    out = []
    for (a, b, e), ps in sorted(pins.items()):
        avg = (round(sum(p[0] for p in ps) / len(ps)), round(sum(p[1] for p in ps) / len(ps)))
        spread = max(abs(p[0] - avg[0]) + abs(p[1] - avg[1]) for p in ps)
        out.append((a, b, e, avg, spread))
    return out


def metric_audit(world, links) -> list[str]:
    """BFS the tile-accurate constraint graph; report loop misclosures."""
    adj: dict[str, list[tuple[str, tuple[int, int]]]] = {}
    for a, b, _e, pin, spread in links:
        if spread > 2:
            print(f"  [W] funnel      {a} -> {b}: warp pins spread {spread} tiles")
        adj.setdefault(a, []).append((b, pin))
        adj.setdefault(b, []).append((a, (-pin[0], -pin[1])))
    pos: dict[str, tuple[int, int]] = {}
    notes: list[str] = []
    seen: set[frozenset] = set()
    for root in ["tinderwick"] + sorted(adj):
        if root in pos or root not in adj:
            continue
        pos[root] = (0, 0)
        q = deque([root])
        while q:
            cur = q.popleft()
            for nxt, d in adj[cur]:
                want = (pos[cur][0] + d[0], pos[cur][1] + d[1])
                if nxt in pos:
                    dx, dy = want[0] - pos[nxt][0], want[1] - pos[nxt][1]
                    key = frozenset((cur, nxt))
                    if (abs(dx) > 2 or abs(dy) > 2) and key not in seen:
                        seen.add(key)
                        notes.append(f"{cur} <-> {nxt}: loop closes ({dx:+d},{dy:+d}) tiles off")
                else:
                    pos[nxt] = want
                    q.append(nxt)
    return notes


def bearing(a: str, b: str) -> str:
    ax, ay, _ = NODES[a]
    bx, by, _ = NODES[b]
    dx, dy = bx - ax, by - ay
    if abs(dx) >= abs(dy):
        return "e" if dx > 0 else "w"
    return "s" if dy > 0 else "n"


def memberships(world: dict[str, dict]) -> dict[str, str]:
    """Assign EVERY map id to the layout node whose place it belongs to, by
    walking the warp graph outward from the nodes (interiors -> their town,
    dungeon floors -> the mouth, annex scars -> their host)."""
    adj: dict[str, set[str]] = {}
    for mid, m in world.items():
        for w in m.get("warps", []):
            if w.get("to_map") in world:
                adj.setdefault(mid, set()).add(w["to_map"])
                adj.setdefault(w["to_map"], set()).add(mid)
    member = {mid: mid for mid in NODES if mid in world}
    q = deque(member)
    while q:
        cur = q.popleft()
        for nxt in sorted(adj.get(cur, ())):  # BFS: nearest node wins (sorted: seed-independent)
            if nxt not in member:
                member[nxt] = member[cur]
                q.append(nxt)
    missing = sorted(set(world) - set(member))
    for mid in missing:
        print(f"  [W] membership  {mid}: unreachable from any layout node")
    return member


def render(world) -> None:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("  [·] Pillow not installed — skipping the PNG render")
        return
    S = 5  # px per virtual unit
    PADX, PADY = 30, 26
    img = Image.new("RGB", (BOX["width"] * S + PADX * 2, BOX["height"] * S + PADY * 2), (11, 16, 38))
    dr = ImageDraw.Draw(img)
    fill = {"town": (244, 208, 110), "route": (123, 220, 107), "dungeon": (180, 160, 230),
            "hub": (255, 138, 61), "landmark": (159, 231, 255)}
    sizes = {"town": (16, 11), "route": (13, 9), "dungeon": (12, 9), "hub": (14, 11),
             "landmark": (7, 7)}

    def centre(n):
        x, y, _ = NODES[n]
        return (x * S + PADX, y * S + PADY)

    def dashed(p, q, color, w=2):
        n = max(1, int(((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2) ** 0.5 // 10))
        for i in range(0, n, 2):
            a = (p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n)
            b = (p[0] + (q[0] - p[0]) * (i + 1) / n, p[1] + (q[1] - p[1]) * (i + 1) / n)
            dr.line([a, b], fill=color, width=w)

    for a, b, kind in ROADS:
        pa, pb = centre(a), centre(b)
        if kind == "road":
            dr.line([pa, pb], fill=(200, 195, 215), width=3)
        elif kind == "lane":
            dashed(pa, pb, (255, 195, 120), 3)
        elif kind == "car":
            dashed(pa, pb, (120, 210, 255), 2)
        elif kind == "pass":
            dashed(pa, pb, (170, 150, 220), 3)
        else:
            dashed(pa, pb, (110, 120, 150), 2)

    for n, (x, y, kind) in NODES.items():
        if n not in world:
            continue
        w, h = sizes[kind]
        w, h = w * S // 2, h * S // 2
        cx, cy = centre(n)
        dr.rectangle((cx - w, cy - h, cx + w, cy + h), fill=fill[kind], outline=(11, 16, 38))
        label = world[n].get("display_name", n)
        dr.text((cx - len(label) * 3, cy + h + 2), label, fill=(245, 240, 225))

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PNG)
    print(f"  render -> {OUT_PNG.relative_to(REPO)}")


def main() -> int:
    world = load_world()
    compute_nodes(world)
    for note in compute_grid():
        print(f"  [·] grid        {note}")
    links = straight_links(world)
    fails: list[str] = []

    print("World layout — metric audit (tile-accurate chaining of straight links)")
    for note in metric_audit(world, links):
        print(f"  [·] misclosure  {note}")

    # ---- verify the ring layout against the shipped warps --------------------
    print("Ring layout — verifying the schematic against shipped warp geometry")
    road_set = {frozenset((a, b)) for a, b, _ in ROADS}
    member = memberships(world)
    bends: list[str] = []
    for a, b, exit_e, _pin, _spread in links:
        na, nb = member.get(a), member.get(b)
        if na is None or nb is None or na == nb:
            continue
        if na not in NODES or nb not in NODES:
            continue
        if frozenset((na, nb)) not in road_set:
            fails.append(f"missing road  {na} <-> {nb} (shipped warp {a} -> {b} has no road on the map)")
            continue
        want = bearing(na, nb)
        if want == OPP[exit_e]:
            fails.append(f"reversed      {a} exits {exit_e.upper()} but the map places "
                         f"{nb} to the {want.upper()} of {na}")
        elif want != exit_e:
            bends.append(f"{a} exits {exit_e.upper()}; the map road to {nb} runs {want.upper()} "
                         f"(road bends — fine, or re-edge the gate to {want.upper()})")
    for n in NODES:
        if n not in world:
            fails.append(f"ghost node    {n} has no shipped map JSON")
    for a, b, _ in ROADS:
        if a not in NODES or b not in NODES:
            fails.append(f"ghost road    {a} <-> {b} references an unknown node")

    for note in route_roads():
        print(f"  [·] grid road   {note}")
    fails += grid_honesty(links, member)
    for f in fails:
        print(f"  [F] {f}")
    for s in bends:
        print(f"  [·] bend        {s}")

    # ---- emit ------------------------------------------------------------------
    layout = {
        "box": dict(BOX),
        "grid": dict(GRID_SIZE),
        "nodes": [
            {"id": n, "x": x, "y": y, "gx": GRID[n][0], "gy": GRID[n][1], "kind": kind, "region": region_of(n),
             "name": world[n].get("display_name", n)}
            for n, (x, y, kind) in NODES.items() if n in world
        ],
        "roads": [{"a": a, "b": b, "kind": kind, "path": ROAD_PATHS.get((a, b), [])} for a, b, kind in ROADS
                  if a in world and b in world],
        "members": dict(sorted(member.items())),
    }
    text = json.dumps(layout, indent=2) + "\n"
    if "--check" in sys.argv:              # CI: fail if the shipped JSON is stale
        if not OUT_JSON.exists() or OUT_JSON.read_text() != text:
            fails.append(f"stale         {OUT_JSON.relative_to(REPO)} — re-run tools/maps/world_layout.py")
        else:
            print(f"  layout up to date: {OUT_JSON.relative_to(REPO)}")
    else:
        OUT_JSON.write_text(text)
        print(f"  layout -> {OUT_JSON.relative_to(REPO)}")
        render(world)
    for f in fails[-1:] if fails and fails[-1].startswith("stale") else []:
        print(f"  [F] {f}")
    print(f"{'FAIL' if fails else 'PASS'} — {len(fails)} failure(s), {len(bends)} bend note(s)")
    return 1 if fails else 0


_REGIONS: dict[str, str] = {}


def region_of(map_id: str) -> str:
    if not _REGIONS:
        import re
        for m in re.finditer(r"map_id:\s*'([^']+)'\s*,\s*region:\s*'([^']+)'", GRAPH_TS.read_text()):
            _REGIONS[m.group(1)] = m.group(2)
    return _REGIONS.get(map_id, "outer")


if __name__ == "__main__":
    sys.exit(main())
