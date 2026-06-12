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
# The canonical ring layout (atlas §1: rim clockwise around the central Spire,
# Crossroads as the inner hub). Coordinates are node CENTRES in a 220x140
# virtual box (x right, y down) — the in-game screen draws this 1:1 inside its
# panel. Hand-authored: edit here to retune the world map's look.
#   kind: town / route / dungeon / hub / landmark (landmarks draw as small dots)
# ---------------------------------------------------------------------------
NODES: dict[str, tuple[int, int, str]] = {
    # --- central spine ------------------------------------------------------
    "umbral_spire": (110, 50, "dungeon"),
    "penumbra_ring": (110, 68, "route"),
    "starwell": (128, 60, "landmark"),
    "vesper_crossroads": (110, 88, "hub"),
    # --- south (bottom of the ring, west -> east) ---------------------------
    "dawnstead": (56, 128, "town"),
    "tinderwick": (80, 122, "town"),
    "dimglass_coast": (101, 127, "route"),
    "dimglass_coast_ii": (122, 127, "route"),
    "tideglass_cavern": (111, 137, "landmark"),
    "gullcry_rock": (133, 137, "landmark"),
    "pearlmoor_quay": (144, 121, "town"),
    "pearlmoor_breakwater": (152, 132, "landmark"),
    # --- east (right side, bottom -> top) -----------------------------------
    "saltreach_fen_i": (166, 110, "route"),
    "saltreach_fen_ii": (174, 92, "route"),
    "sunkbell_shallows": (190, 99, "landmark"),
    "lowleaf_hollow": (175, 72, "town"),
    "glowmoss_deep": (174, 53, "dungeon"),
    "spore_grotto": (191, 48, "landmark"),
    "cinderhead_mine": (166, 35, "town"),
    "cinderhead_deep": (148, 26, "dungeon"),
    # --- north (top, east -> west) -------------------------------------------
    "galehigh_terraces": (128, 20, "town"),
    "wind_eye": (139, 8, "landmark"),
    "windward_stair_i": (107, 16, "route"),
    "windward_stair_ii": (88, 13, "route"),
    "thunderroost": (97, 4, "landmark"),
    "pale_vault_glacier": (66, 17, "town"),
    # --- west (left side, top -> bottom; the Sunvault stair CLIMBS back north
    # to Nightreach, matching the shipped warp edges) --------------------------
    "hushfrost_pass_i": (46, 25, "route"),
    "hushfrost_pass_ii": (34, 41, "route"),
    "aurora_hollow": (18, 33, "landmark"),
    "sunken_solarium": (28, 58, "town"),
    "unrisen_stair": (12, 52, "landmark"),
    "sunvault_climb_i": (20, 110, "route"),
    "sunvault_climb_ii": (28, 92, "route"),
    "helia_vault": (12, 86, "landmark"),
    "nightreach_observatory": (36, 74, "town"),
    # --- outer marches (between Nightreach and the hub) -----------------------
    "coldfog_marches_ii": (58, 82, "route"),
    "coldfog_marches_i": (64, 102, "route"),
    "drownlight_beacon": (46, 92, "landmark"),
    "hollowfen_stillworks": (68, 68, "landmark"),
    # --- the Lanternway spoke lanes (real maps, build_lanternway.py) ----------
    "lanternway_tinderwick": (95, 106, "route"),
    "lanternway_pearlmoor": (128, 104, "route"),
    "lanternway_lowleaf": (144, 79, "route"),
    "lanternway_galehigh": (124, 54, "route"),
    "lanternway_nightreach": (80, 76, "route"),
}

# Roads drawn between nodes. kind: 'road' (walked route), 'lane' (Lanternway
# spoke — abstracted country lane), 'gate' (Gift/flag-gated passage), 'pass'
# (through-cave passage). Derived links are verified against shipped warps.
ROADS: list[tuple[str, str, str]] = [
    # south rim
    ("tinderwick", "dimglass_coast", "road"),
    ("dimglass_coast", "dimglass_coast_ii", "road"),
    ("dimglass_coast_ii", "pearlmoor_quay", "road"),
    ("dimglass_coast", "tideglass_cavern", "gate"),
    ("dimglass_coast_ii", "tideglass_cavern", "gate"),
    ("dimglass_coast_ii", "gullcry_rock", "gate"),
    ("pearlmoor_quay", "pearlmoor_breakwater", "gate"),
    ("umbral_spire", "dawnstead", "gate"),
    # east rim
    ("pearlmoor_quay", "saltreach_fen_i", "road"),
    ("saltreach_fen_i", "saltreach_fen_ii", "gate"),
    ("saltreach_fen_ii", "sunkbell_shallows", "gate"),
    ("saltreach_fen_ii", "lowleaf_hollow", "road"),
    ("lowleaf_hollow", "glowmoss_deep", "gate"),
    ("glowmoss_deep", "spore_grotto", "gate"),
    ("glowmoss_deep", "cinderhead_mine", "pass"),
    ("cinderhead_mine", "cinderhead_deep", "gate"),
    ("cinderhead_deep", "galehigh_terraces", "pass"),
    # north rim
    ("galehigh_terraces", "wind_eye", "gate"),
    ("galehigh_terraces", "windward_stair_i", "road"),
    ("windward_stair_i", "windward_stair_ii", "gate"),
    ("windward_stair_ii", "thunderroost", "gate"),
    ("windward_stair_ii", "pale_vault_glacier", "road"),
    ("windward_stair_ii", "galehigh_terraces", "gate"),  # late shortcut
    # west rim
    ("pale_vault_glacier", "hushfrost_pass_i", "road"),
    ("hushfrost_pass_i", "hushfrost_pass_ii", "gate"),
    ("hushfrost_pass_ii", "aurora_hollow", "gate"),
    ("hushfrost_pass_ii", "sunken_solarium", "road"),
    ("sunken_solarium", "unrisen_stair", "gate"),
    ("sunken_solarium", "sunvault_climb_i", "road"),
    ("sunvault_climb_i", "sunvault_climb_ii", "gate"),
    ("sunvault_climb_ii", "helia_vault", "gate"),
    ("sunvault_climb_ii", "nightreach_observatory", "road"),
    # outer marches
    ("nightreach_observatory", "coldfog_marches_ii", "gate"),
    ("coldfog_marches_ii", "coldfog_marches_i", "gate"),
    ("coldfog_marches_i", "vesper_crossroads", "road"),
    ("coldfog_marches_ii", "drownlight_beacon", "gate"),
    ("coldfog_marches_ii", "hollowfen_stillworks", "gate"),
    # the Lanternway spokes (the hub-and-wheel) — each spoke is two hops
    # through its real lane map (build_lanternway.py)
    ("tinderwick", "lanternway_tinderwick", "lane"),
    ("lanternway_tinderwick", "vesper_crossroads", "lane"),
    ("pearlmoor_quay", "lanternway_pearlmoor", "lane"),
    ("lanternway_pearlmoor", "vesper_crossroads", "lane"),
    ("lowleaf_hollow", "lanternway_lowleaf", "lane"),
    ("lanternway_lowleaf", "vesper_crossroads", "lane"),
    ("galehigh_terraces", "lanternway_galehigh", "lane"),
    ("lanternway_galehigh", "vesper_crossroads", "lane"),
    ("nightreach_observatory", "lanternway_nightreach", "lane"),
    ("lanternway_nightreach", "vesper_crossroads", "lane"),
    ("cinderhead_deep", "vesper_crossroads", "gate"),  # late mine shortcut
    # the centre
    ("vesper_crossroads", "penumbra_ring", "gate"),
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
        for nxt in adj.get(cur, ()):  # BFS: nearest node wins
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
    img = Image.new("RGB", (220 * S + PADX * 2, 140 * S + PADY * 2), (11, 16, 38))
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

    for f in fails:
        print(f"  [F] {f}")
    for s in bends:
        print(f"  [·] bend        {s}")

    # ---- emit ------------------------------------------------------------------
    layout = {
        "nodes": [
            {"id": n, "x": x, "y": y, "kind": kind, "region": region_of(n),
             "name": world[n].get("display_name", n)}
            for n, (x, y, kind) in NODES.items() if n in world
        ],
        "roads": [{"a": a, "b": b, "kind": kind} for a, b, kind in ROADS
                  if a in world and b in world],
        "members": member,
    }
    OUT_JSON.write_text(json.dumps(layout, indent=2) + "\n")
    print(f"  layout -> {OUT_JSON.relative_to(REPO)}")
    render(world)
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
