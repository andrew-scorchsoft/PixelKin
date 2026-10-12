#!/usr/bin/env python3
"""
world_geometry — lay the ACTUAL maps out edge-to-edge and see if the world closes.

audit_spatial checks each link locally (lands on an edge, faces inward,
mirrors); world_layout draws the SCHEMATIC ring the MAP screen shows. Neither
answers the playtest question "when I walk north, am I really going north of
where I was?". This tool does: every outdoor map is a rectangle of its true
tile size, and every STRAIGHT edge link (leave A's north edge -> arrive on B's
south edge) pins B against A at the exact tile offset of the warp. Breadth-first
from the start town gives each map one global position; every further link is a
CONSTRAINT that either agrees (the loop closes) or doesn't (a contradiction, in
tiles). Rectangles that land on top of each other are overlaps.

  * interiors are excluded; caves join only through edge-to-edge links (a cave
    entered by a mid-map mouth is a PORTAL — drawn dotted, never placing);
  * BENT links (leave north, arrive on a west edge) don't place either — they
    are drawn dashed and listed, because the walker's compass turns on them;
  * the spanning tree prefers rim roads over the Lanternway lanes (lanes cost
    more), so a misclosure shows up on the lane/hub link that can't fit;
  * maps not reachable through straight links form separate components, laid
    out in a strip below the main one.

It also cross-checks every straight link's walked bearing against the in-game
MAP screen (src/game/data/world/worldmap.json): if you walk off the north edge
but the MAP draws the neighbour to the east, that is reported.

Outputs:
  --png PATH          whole-world render (default tools/maps/out/world_geometry.png)
  --south-png PATH    zoomed early-game render (default ..._south.png)
  --json PATH         global placements + bearings (for text audits)
  --check             exit 1 on any contradiction / overlap / MAP-bearing clash
Run from anywhere:  python3 tools/maps/world_geometry.py   (Pillow for PNGs)
"""
from __future__ import annotations

import argparse
import heapq
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from worldmodel import GRAPH_TS, REPO, load_world  # noqa: E402

OUT_DIR = REPO / "tools/maps/out"
WORLDMAP_JSON = REPO / "src/game/data/world/worldmap.json"
OPP = {"n": "s", "s": "n", "e": "w", "w": "e"}
EDGE_TOL = 2           # a landing may sit this far inboard of its edge
CLOSE_TOL = 3          # a loop misclosing by <= this many tiles still "closes"
LANE_COST = 8          # spanning-tree weight of a Lanternway / hub link

REGION_COL = {
    "south": (232, 160, 72), "east": (110, 190, 110), "north": (120, 170, 230),
    "west": (190, 140, 220), "central": (220, 220, 140), "outer": (150, 150, 150),
    None: (200, 200, 200),
}

SOUTH_SET = [
    "tinderwick", "duskapple_orchard", "dimglass_coast", "dimglass_coast_ii",
    "pearlmoor_quay", "pearlmoor_breakwater", "pearlmoor_point", "pearlmoor_allotment",
    "pearlmoor_wanderwood", "pearlmoor_wanderwood_far", "lanternway_tinderwick",
    "lanternway_lowleaf", "lanternway_galehigh", "lanternway_nightreach",
    "vesper_crossroads", "wrackline_path", "sounding_cave", "lanternfall_road",
    "gullcry_rock", "saltreach_fen_i",
]


def regions() -> dict[str, str]:
    txt = GRAPH_TS.read_text()
    return dict(re.findall(r"map_id: '([a-z0-9_]+)', region: '([a-z]+)'", txt))


def edges_of(m: dict, tx: int, ty: int, tol: int = 0) -> set[str]:
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


def link_cost(a: str, b: str) -> int:
    """Spanning-tree weight: rim roads first, the first-hour Tinderwick spoke
    next, other Lanternway lanes / hub links after, the Sounding Cave (the
    hidden underpass of the Pearlmoor road) last — so a misclosure surfaces on
    the link a player is least likely to hold in their head."""
    pair = (a, b)
    if "sounding_cave" in pair:
        return 50
    if "lanternway_tinderwick" in pair:
        return 2
    if any(x.startswith("lanternway_") or x == "vesper_crossroads" for x in pair):
        return LANE_COST
    return 1


def collect(world: dict) -> tuple[list[dict], list[dict], list[dict]]:
    """-> straight, bent, portal link lists (each one warp)."""
    straight, bent, portal = [], [], []
    for mid, m in sorted(world.items()):
        if m.get("kind") == "interior":
            continue
        for w in m.get("warps", []):
            # door-transition warps count too when BOTH ends sit on a map edge
            # (a cave mouth cut into the map border, e.g. the Sounding Cave);
            # a door in mid-map falls out below as a portal.
            dst = world.get(w.get("to_map", ""))
            if dst is None or dst.get("kind") == "interior":
                continue
            ax, ay = w["at"]["tx"], w["at"]["ty"]
            bx, by = w["to"]["tx"], w["to"]["ty"]
            rec = {"a": mid, "b": w["to_map"], "id": w["id"], "at": (ax, ay), "to": (bx, by)}
            se = edges_of(m, ax, ay)
            de = edges_of(dst, bx, by, tol=EDGE_TOL)
            if not se or not de:
                portal.append(rec)
                continue
            exit_e = next((e for e in sorted(se) if OPP[e] in de), sorted(se)[0])
            land_e = OPP[exit_e] if OPP[exit_e] in de else sorted(de)[0]
            rec["exit"], rec["land"] = exit_e, land_e
            if land_e != OPP[exit_e]:
                bent.append(rec)
                continue
            A, B = m, dst
            if exit_e == "n":
                off = (ax - bx, -B["height"])
            elif exit_e == "s":
                off = (ax - bx, A["height"])
            elif exit_e == "e":
                off = (A["width"], ay - by)
            else:
                off = (-B["width"], ay - by)
            rec["off"] = off
            straight.append(rec)
    return straight, bent, portal


def place(world: dict, straight: list[dict], root: str):
    """Dijkstra spanning tree over straight links -> (pos, comp, conflicts)."""
    adj: dict[str, list[tuple[str, tuple[int, int], dict]]] = {}
    for r in straight:
        adj.setdefault(r["a"], []).append((r["b"], r["off"], r))
        adj.setdefault(r["b"], []).append((r["a"], (-r["off"][0], -r["off"][1]), r))
    pos: dict[str, tuple[int, int]] = {}
    comp: dict[str, int] = {}
    parent: dict[str, str | None] = {}
    order = [root] + sorted(m for m in adj if m != root)
    cid = 0
    for start in order:
        if start in pos:
            continue
        heap = [(0, start, (0, 0), None)]
        while heap:
            d, cur, p, par = heapq.heappop(heap)
            if cur in pos:
                continue
            pos[cur], comp[cur], parent[cur] = p, cid, par
            for nxt, off, r in adj.get(cur, []):
                if nxt not in pos:
                    w = link_cost(cur, nxt)
                    heapq.heappush(heap, (d + w, nxt, (p[0] + off[0], p[1] + off[1]), cur))
        cid += 1

    # every straight link is a constraint; report those that don't close
    conflicts = []
    seen = set()
    for r in straight:
        a, b = r["a"], r["b"]
        if comp.get(a) != comp.get(b):
            continue
        want = (pos[a][0] + r["off"][0], pos[a][1] + r["off"][1])
        err = (want[0] - pos[b][0], want[1] - pos[b][1])
        mag = abs(err[0]) + abs(err[1])
        key = (min(a, b), max(a, b), r["exit"] if a < b else OPP[r["exit"]])
        if mag > CLOSE_TOL and key not in seen:
            seen.add(key)
            conflicts.append({**r, "err": err, "mag": mag})
    return pos, comp, parent, conflicts


GIFTS = {"tidecall", "glimmerstep", "updraft_kite", "emberward", "sunsketch", "starreach"}
_MODELS: dict = {}


def _open_cells(world, mid):
    """DRY GROUND a player can stand on (every land Gift held) — border trees,
    cliffs and walls are not ground two maps can fight over, and neither is
    water: two maps showing the same bay (Dimglass II and the breakwater) are
    one sea seen twice, not a contradiction."""
    if mid not in _MODELS:
        from worldmodel import MapModel
        mm = MapModel(world[mid])
        land = GIFTS - {"tidecall", "starreach"}   # water + starlit void aren't ground
        _MODELS[mid] = {(x, y) for y in range(mm.h) for x in range(mm.w)
                        if mm.standable(x, y, abilities=land)}
    return _MODELS[mid]


def hang_components(world, pos, comp, portal, root="tinderwick"):
    """Join components reached only through a mid-map lift or mouth (the
    Windward kite flight, cave mouths) to the root's: shift the whole component
    so its landing tile sits on the host's mouth tile. Late SHORTCUT warps
    (`shortcut_*`) never place a component — they're return compressors, not
    the way the land lies. Returns the (a, b) map pairs joined by a portal (a
    lift's two ends may honestly overlap — the climb happens between them)."""
    main = comp[root]
    joins = sorted((r for r in portal if not r["id"].startswith("shortcut")),
                   key=lambda r: (r["a"], r["id"]))
    for _ in range(12):
        moved = False
        for r in joins:
            a, b = r["a"], r["b"]
            if comp.get(a) != main or b not in pos or comp.get(b) == main:
                continue
            want = (pos[a][0] + r["at"][0] - r["to"][0], pos[a][1] + r["at"][1] - r["to"][1])
            dx, dy = want[0] - pos[b][0], want[1] - pos[b][1]
            old = comp[b]
            for mid in list(pos):
                if comp.get(mid) == old:
                    pos[mid] = (pos[mid][0] + dx, pos[mid][1] + dy)
                    comp[mid] = main
            moved = True
        if not moved:
            break
    return {frozenset((r["a"], r["b"])) for r in portal}


def overlaps(world, pos, comp, exempt=frozenset()):
    """Rectangles on top of each other. Two kinds are NOT contradictions:
    a CAVE under a surface map (caves are underground — Glowmoss Deep under the
    Gloamwood dell), and overlap made only of ground neither map lets you stand
    on (shared border woods, shared open sea). Only cells walkable in BOTH maps
    count."""
    ids = sorted(pos)
    out = []
    for i, a in enumerate(ids):
        ax, ay = pos[a]
        aw, ah = world[a]["width"], world[a]["height"]
        for b in ids[i + 1:]:
            if comp[a] != comp[b] or frozenset((a, b)) in exempt:
                continue
            bx, by = pos[b]
            bw, bh = world[b]["width"], world[b]["height"]
            ix = min(ax + aw, bx + bw) - max(ax, bx)
            iy = min(ay + ah, by + bh) - max(ay, by)
            if ix > 0 and iy > 0:
                ka, kb = world[a].get("kind"), world[b].get("kind")
                if (ka == "cave") != (kb == "cave"):
                    continue                      # underground: a cave under ground
                oa, ob = _open_cells(world, a), _open_cells(world, b)
                both = sum(1 for gy in range(max(ay, by), min(ay + ah, by + bh))
                           for gx in range(max(ax, bx), min(ax + aw, bx + bw))
                           if (gx - ax, gy - ay) in oa and (gx - bx, gy - by) in ob)
                if both:
                    out.append((a, b, both, min(len(oa), len(ob)) or 1))
    return out


def map_screen_clashes(straight):
    """Straight links whose walked edge disagrees with the MAP screen's bearing."""
    if not WORLDMAP_JSON.is_file():
        return []
    wm = json.loads(WORLDMAP_JSON.read_text())
    nodes = {n["id"]: (n["x"], n["y"]) for n in wm["nodes"]}
    member = wm.get("members", {})
    out, seen = [], set()
    for r in straight:
        na, nb = member.get(r["a"], r["a"]), member.get(r["b"], r["b"])
        if na == nb or na not in nodes or nb not in nodes:
            continue
        key = (min(na, nb), max(na, nb))
        if key in seen:
            continue
        dx = nodes[nb][0] - nodes[na][0]
        dy = nodes[nb][1] - nodes[na][1]
        e = r["exit"]
        along = {"n": -dy, "s": dy, "e": dx, "w": -dx}[e]
        across = abs(dx) if e in "ns" else abs(dy)
        if along <= 0 or across > 2 * along:
            seen.add(key)
            drawn = ("E" if dx > 0 else "W") if abs(dx) >= abs(dy) else ("S" if dy > 0 else "N")
            out.append((r["a"], r["b"], e.upper(), drawn, (dx, dy)))
    return out


def bearing(dx: float, dy: float) -> str:
    import math
    if dx == 0 and dy == 0:
        return "-"
    ang = (math.degrees(math.atan2(-dy, dx)) + 360) % 360  # 0=E, 90=N
    names = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
    return names[int((ang + 22.5) // 45) % 8]


# ---------------------------------------------------------------------------
def render(world, reg, pos, comp, straight, bent, portal, conflicts, path,
           subset=None, scale=3):
    from PIL import Image, ImageDraw, ImageFont
    ids = [m for m in pos if subset is None or m in subset]
    if not ids:
        return
    # lay components out: main (comp of tinderwick) at top, others in a strip below
    main = comp.get("tinderwick", 0)
    gpos = {}
    minx = min(pos[m][0] for m in ids if comp[m] == main)
    maxx = max(pos[m][0] + world[m]["width"] for m in ids if comp[m] == main)
    maxy = max(pos[m][1] + world[m]["height"] for m in ids if comp[m] == main)
    miny = min(pos[m][1] for m in ids if comp[m] == main)
    for m in ids:
        if comp[m] == main:
            gpos[m] = pos[m]
    cursor_x, strip_y, strip_h = minx, maxy + 20, 0
    for c in sorted({comp[m] for m in ids} - {main}):
        members = [m for m in ids if comp[m] == c]
        cx0 = min(pos[m][0] for m in members)
        cy0 = min(pos[m][1] for m in members)
        cw = max(pos[m][0] + world[m]["width"] for m in members) - cx0
        ch = max(pos[m][1] + world[m]["height"] for m in members) - cy0
        if cursor_x + cw > max(maxx, minx + 400):
            cursor_x, strip_y, strip_h = minx, strip_y + strip_h + 12, 0
        for m in members:
            gpos[m] = (pos[m][0] - cx0 + cursor_x, pos[m][1] - cy0 + strip_y)
        cursor_x += cw + 12
        strip_h = max(strip_h, ch)
    X0 = min(p[0] for p in gpos.values()) - 6
    Y0 = min(p[1] for p in gpos.values()) - 6
    X1 = max(gpos[m][0] + world[m]["width"] for m in gpos) + 6
    Y1 = max(gpos[m][1] + world[m]["height"] for m in gpos) + 6
    W, H = (X1 - X0) * scale, (Y1 - Y0) * scale + 64
    img = Image.new("RGB", (W, H), (18, 20, 34))
    dr = ImageDraw.Draw(img, "RGBA")
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", min(13, max(9, scale * 2)))
    except OSError:
        font = ImageFont.load_default()

    def P(m, tx, ty):
        return ((gpos[m][0] + tx + 0.5 - X0) * scale, (gpos[m][1] + ty + 0.5 - Y0) * scale)

    bad = {c["a"] for c in conflicts} | {c["b"] for c in conflicts}
    if comp:
        dr.line([(0, (maxy + 10 - Y0) * scale), (W, (maxy + 10 - Y0) * scale)],
                fill=(80, 80, 100), width=1)
        dr.text((6, (maxy + 12 - Y0) * scale), "unanchored components (reached only via "
                "portals / bent links — position here is arbitrary):", fill=(160, 160, 180), font=font)
    for m in gpos:
        x, y = gpos[m]
        col = REGION_COL.get(reg.get(m), REGION_COL[None])
        box = [(x - X0) * scale, (y - Y0) * scale,
               (x + world[m]["width"] - X0) * scale - 1, (y + world[m]["height"] - Y0) * scale - 1]
        dr.rectangle(box, fill=col + (70,), outline=(255, 60, 60) if m in bad else col,
                     width=3 if m in bad else 1)
        kind = world[m].get("kind", "")
        label = m + (" (cave)" if kind == "cave" else "")
        dr.text((box[0] + 3, box[1] + 2), label, fill=(240, 240, 240), font=font)

    def drawn(rec):
        return rec["a"] in gpos and rec["b"] in gpos

    for r in straight:
        if drawn(r):
            dr.ellipse([*(v - scale for v in P(r["a"], *r["at"])),
                        *(v + scale for v in P(r["a"], *r["at"]))], fill=(255, 255, 255, 200))
    for r in bent:
        if drawn(r):
            a, b = P(r["a"], *r["at"]), P(r["b"], *r["to"])
            _dash(dr, a, b, (255, 170, 40, 220), scale)
    for r in portal:
        if drawn(r) and r["a"] < r["b"]:
            a, b = P(r["a"], *r["at"]), P(r["b"], *r["to"])
            _dash(dr, a, b, (150, 150, 170, 150), scale, dot=True)
    for c in conflicts:
        if drawn(c):
            a, b = P(c["a"], *c["at"]), P(c["b"], *c["to"])
            dr.line([a, b], fill=(255, 50, 50, 255), width=max(2, scale))
    legend = ["rectangles = real maps at true tile size, butted edge-to-edge by their warps",
              "white dot = straight edge link  ·  RED line/outline = a link whose loop doesn't close",
              "orange dashed = bent link (compass turns)  ·  grey dotted = mid-map cave mouth / portal",
              "regions: south=orange east=green north=blue west=purple central=yellow outer=grey"]
    for i, t in enumerate(legend):
        dr.text((6, H - 58 + i * 14), t, fill=(220, 220, 220), font=font)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _dash(dr, a, b, col, scale, dot=False):
    import math
    L = math.dist(a, b)
    if L == 0:
        return
    seg = scale * (1 if dot else 3)
    n = int(L // (seg * 2)) + 1
    for i in range(n):
        t0, t1 = (2 * i * seg) / L, min(1, (2 * i + 1) * seg / L)
        dr.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                 (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                fill=col, width=max(1, scale // 2))


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--png", type=Path, default=OUT_DIR / "world_geometry.png")
    ap.add_argument("--south-png", type=Path, default=OUT_DIR / "world_geometry_south.png")
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    world = load_world()
    reg = regions()
    straight, bent, portal = collect(world)
    pos, comp, parent, conflicts = place(world, straight, "tinderwick")
    # overlaps are checked across the WHOLE world: components hung off their
    # lifts/mouths first, so the far side is checked against the near side
    hpos, hcomp = dict(pos), dict(comp)
    lifted = hang_components(world, hpos, hcomp, portal)
    ovl = overlaps(world, hpos, hcomp, exempt=lifted)
    clashes = map_screen_clashes(straight)

    main_c = comp.get("tinderwick")
    placed_main = sorted(m for m in pos if comp[m] == main_c)
    outdoor = sorted(m for m, d in world.items() if d.get("kind") != "interior")
    print(f"World geometry — {len(outdoor)} non-interior maps, {len(straight)} straight / "
          f"{len(bent)} bent / {len(portal)} portal links")
    print(f"  main component (from tinderwick): {len(placed_main)} maps; "
          f"{len({comp[m] for m in pos}) - 1} other component(s); "
          f"{len([m for m in outdoor if m not in pos])} maps with no straight link")

    def cen(m):
        return (pos[m][0] + world[m]["width"] / 2, pos[m][1] + world[m]["height"] / 2)

    print("\n  Placement (tile origin, main component), placed-from, and bearing FROM tinderwick:")
    t = cen("tinderwick")
    for m in placed_main:
        c = cen(m)
        print(f"    {m:28s} ({pos[m][0]:5d},{pos[m][1]:5d})  <- {str(parent[m]):26s} {bearing(c[0]-t[0], c[1]-t[1]):>2}"
              f"  {abs(c[0]-t[0]):4.0f} E/W, {abs(c[1]-t[1]):4.0f} N/S tiles")

    print(f"\n  [{'F' if conflicts else '✓'}] loop closure — {len(conflicts)} link(s) "
          f"off by > {CLOSE_TOL} tiles:")
    for c in sorted(conflicts, key=lambda c: -c["mag"]):
        print(f"    {c['a']}:{c['id']} -> {c['b']} ({c['exit'].upper()} edge): the walked "
              f"world wants {c['b']} {c['err'][0]:+d},{c['err'][1]:+d} tiles from where the "
              f"rest of the network puts it")
    print(f"  [{'F' if ovl else '✓'}] overlaps — {len(ovl)}:")
    for a, b, area, small in sorted(ovl, key=lambda o: -o[2] / o[3]):
        print(f"    {a} ∩ {b}: {area} tiles ({100*area/small:.0f}% of the smaller map)")
    print(f"  [{'F' if clashes else '✓'}] MAP-screen bearing vs walked edge — {len(clashes)}:")
    for a, b, walked, drawn_d, d in clashes:
        print(f"    {a} -> {b}: you leave by the {walked} edge, the MAP draws it {drawn_d} "
              f"(node delta {d[0]:+d},{d[1]:+d})")
    print(f"  [·] bent links (compass turns mid-road) — {len(bent)}:")
    for r in bent:
        if r["a"] < r["b"]:
            print(f"    {r['a']} exits {r['exit'].upper()} -> arrives on {r['b']}'s "
                  f"{r['land'].upper()} edge")

    if args.json:
        args.json.write_text(json.dumps({
            "pos": pos, "comp": comp,
            "size": {m: [world[m]["width"], world[m]["height"]] for m in pos},
            "links": [{k: v for k, v in r.items() if k != "off"} for r in straight + bent],
            "conflicts": [{k: c[k] for k in ("a", "b", "id", "exit", "err", "mag")} for c in conflicts],
        }, indent=1))
    if not (args.no_png or args.check):        # --check is a pure gate: no files written
        try:
            render(world, reg, pos, comp, straight, bent, portal, conflicts, args.png, scale=6)
            render(world, reg, pos, comp, straight, bent, portal, conflicts, args.south_png,
                   subset=set(SOUTH_SET), scale=8)
            print(f"\n  wrote {args.png}\n  wrote {args.south_png}")
        except ImportError:
            print("  (Pillow missing — no PNGs)")
    bad = bool(conflicts or ovl or clashes)
    print(f"\n{'FAIL' if bad else 'PASS'} — {len(conflicts)} misclosure(s), {len(ovl)} overlap(s), "
          f"{len(clashes)} MAP-screen clash(es)")
    return 1 if (args.check and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
