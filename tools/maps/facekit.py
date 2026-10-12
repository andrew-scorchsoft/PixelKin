#!/usr/bin/env python3
"""
facekit — draw a MOUNTAIN-FACE map as ASCII art, on mapkit + wildkit.

The Sunvault Climb rebuild and the Rimeway (09-the-wild-ways §2 S/C) are all
cliff bands, ladders, ledges and planks; drawing them cell by cell in Python
hides the shape. A builder here writes the map as rows of characters and
`paint()` turns them into terrain presence grids, pinned face tiles, ladder /
plank / deck spans and ledge deco — art and behaviour from the same source.

Legend (one char per tile):
  '#'  cliff terrain (the family's rim + lit lip: its south row is the LIP)
  'F'  a tall face row under the lip (wildkit face_<face>_*, solid; the last
       F row above open ground is drawn as the FOOT with its contact shadow)
  'H'  a ladder up a face row          'L'  a ladder up a cliff-terrain row
  'P'  a rope-plank over cliff terrain 'p'  a rope-plank over a face row
  'D'  a trestle deck over open ground (an UNDERPASS: walk the deck along its
       run, or pass beneath it across the run)
  '.'  open ground                     '='  the road (path family)
  '"'  encounter tuft (fill-only)      'v'  a one-way south ledge (hop down)
  'o'  a boulder on open ground        'i'  glare ice (an ice flow)
  'T'  tree / wall-mass terrain (the `mass` family, e.g. glacierwall)

Span runs: a ladder is a vertical run of H/L in one column; a plank/deck run
is horizontal if the cell has a same-kind neighbour left or right, else
vertical. Every run becomes one span (ids `<prefix>_<n>`, numbered in
reading order so a rebuild is stable).
"""
from __future__ import annotations

import random

import mapkit as mk
import wildkit as wk
from mapkit import gid

FACE = set("FHp")
OPEN = set('.="voiD')


class Canvas:
    """Compose the art with rect ops instead of typing rulers by hand."""

    def __init__(self, w: int, h: int, fill: str = "."):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    def rect(self, x0: int, y0: int, x1: int, y1: int, c: str) -> "Canvas":
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.g[y][x] = c
        return self

    def put(self, cells, c: str) -> "Canvas":
        for (x, y) in cells:
            self.g[y][x] = c
        return self

    def at(self, x: int, y: int) -> str:
        return self.g[y][x]

    def band(self, x0: int, x1: int, y0: int, *, lip: int = 2, face: int = 2) -> "Canvas":
        """A cliff band across x0..x1: `lip` rows of cliff terrain, `face` rows below."""
        self.rect(x0, y0, x1, y0 + lip - 1, "#")
        if face:
            self.rect(x0, y0 + lip, x1, y0 + lip + face - 1, "F")
        return self

    def ladder(self, x: int, y0: int, y1: int) -> "Canvas":
        """Rungs up the band cells of column x from y0..y1 (cliff->L, face->H)."""
        for y in range(y0, y1 + 1):
            c = self.g[y][x]
            self.g[y][x] = {"#": "L", "F": "H"}.get(c, c)
        return self

    def plank(self, cells) -> "Canvas":
        for (x, y) in cells:
            c = self.g[y][x]
            self.g[y][x] = "p" if c in "FH" else "P"
        return self

    def rows(self) -> list[str]:
        return ["".join(r) for r in self.g]

    def show(self) -> str:
        return "\n".join(f"{y:3d} {r}" for y, r in enumerate(self.rows()))


def grid_of(art: str) -> list[str]:
    rows = [r for r in art.strip("\n").split("\n")]
    w = len(rows[0])
    for n, r in enumerate(rows):
        if len(r) != w:
            raise SystemExit(f"facekit: row {n} is {len(r)} wide, expected {w}: {r!r}")
    return rows


def paint(m: dict, rows: list[str], *, deco: list, above: list, pin: dict,
          face: str = "gold", ledge: str = "sand", rng: random.Random,
          span_prefix: str = "") -> dict:
    """Paint the art. Returns presence grids {cliff, road, tuft, mass, ice} and
    the set of OPEN cells (walkable ground, for scatter/avoid bookkeeping)."""
    H = len(rows)
    W = len(rows[0])
    wk.use_traverse(m)
    g = {k: mk.make_grid(W, H) for k in ("cliff", "road", "tuft", "mass")}
    open_cells: set[tuple[int, int]] = set()
    ice_cells: set[tuple[int, int]] = set()

    def ch(x, y):
        return rows[y][x] if 0 <= x < W and 0 <= y < H else " "

    for y in range(H):
        for x in range(W):
            c = rows[y][x]
            i = y * W + x
            if c in "#LP":
                g["cliff"][i] = 1
            elif c == "T":
                g["mass"][i] = 1
            elif c in FACE:
                foot = ch(x, y + 1) not in FACE
                pin[(x, y)] = (f"face_{face}_foot" if foot
                               else f"face_{face}_{(x // 3 + y) % 2}")
            elif c == "=" or c == "D":
                g["road"][i] = 1
            elif c == '"':
                g["tuft"][i] = 1
            elif c == "v":
                deco[i] = gid(f"{ledge}_ledge_s" + rng.choice(["", "_v1"]))
            elif c == "o":
                deco[i] = gid("boulder")
            elif c == "i":
                ice_cells.add((x, y))
            if c in OPEN:
                open_cells.add((x, y))

    # ladders: vertical runs of H/L
    n = 0
    for x in range(W):
        y = 0
        while y < H:
            if rows[y][x] in "HL":
                y0 = y
                while y < H and rows[y][x] in "HL":
                    y += 1
                wk.ladder(m, deco, W, x=x, y0=y0, y1=y - 1, sid=f"{span_prefix}ladder_{n}")
                n += 1
            else:
                y += 1

    # planks + decks: runs
    def runs(kinds: str):
        seen: set[tuple[int, int]] = set()
        out = []
        for y in range(H):
            for x in range(W):
                if rows[y][x] not in kinds or (x, y) in seen:
                    continue
                horiz = ch(x - 1, y) in kinds or ch(x + 1, y) in kinds
                cells = []
                cx, cy = x, y
                while ch(cx, cy) in kinds:
                    cells.append((cx, cy))
                    if horiz:
                        cx += 1
                    else:
                        cy += 1
                seen.update(cells)
                out.append((cells, "h" if horiz else "v"))
        return out

    for k, (cells, axis) in enumerate(runs("Pp")):
        xs = [c[0] for c in cells]
        ys = [c[1] for c in cells]
        wk.plank(m, deco, W, rect=(min(xs), min(ys), max(xs) - min(xs) + 1,
                                   max(ys) - min(ys) + 1), axis=axis,
                 sid=f"{span_prefix}plank_{k}")
    for k, (cells, axis) in enumerate(runs("D")):
        xs = [c[0] for c in cells]
        ys = [c[1] for c in cells]
        wk.deck(m, above, W, rect=(min(xs), min(ys), max(xs) - min(xs) + 1,
                                   max(ys) - min(ys) + 1), axis=axis,
                sid=f"{span_prefix}deck_{k}", under=True, shade=deco)

    if ice_cells:
        # one flow per 4-connected sheet, in reading order
        left = set(ice_cells)
        k = 0
        while left:
            start = min(left, key=lambda c: (c[1], c[0]))
            comp, todo = set(), [start]
            while todo:
                c = todo.pop()
                if c in comp or c not in left:
                    continue
                comp.add(c)
                todo += [(c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)]
            left -= comp
            wk.ice(m, pin, comp, fid=f"{span_prefix}ice_{k}")
            k += 1

    g["open"] = open_cells
    g["ice"] = ice_cells
    return g


def ice_solve(rows: list[str], starts, exits, *, box: tuple[int, int, int, int]):
    """Check a glare-ice puzzle drawn in the art (a design aid; the audits'
    worldmodel is the authority). Inside `box` (x0,y0,x1,y1): 'i' slides,
    'o' and wall chars stop you, any other OPEN char is ground (one step).
    Returns (min_slides start->exit or None, trap cells — ice stops from which
    no start cell can be reached again)."""
    from collections import deque
    x0, y0, x1, y1 = box

    def free(x, y):
        return x0 <= x <= x1 and y0 <= y <= y1 and rows[y][x] in OPEN and rows[y][x] != "o"

    def moves(p):
        x, y = p
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if not free(nx, ny):
                continue
            slid = rows[ny][nx] == "i"
            while rows[ny][nx] == "i" and free(nx + dx, ny + dy):
                nx, ny = nx + dx, ny + dy
            yield (nx, ny), int(slid)

    parent: dict = {}

    def bfs(src, track=False):
        dist = {s: 0 for s in src}
        dq = deque(src)
        while dq:
            p = dq.popleft()
            for n, c in moves(p):
                nd = dist[p] + c
                if n not in dist or nd < dist[n]:
                    dist[n] = nd
                    if track:
                        parent[n] = p
                    (dq.appendleft if c == 0 else dq.append)(n)
        return dist

    d = bfs(list(starts), track=True)
    best = min((d[e] for e in exits if e in d), default=None)
    if best is not None and __import__("os").environ.get("ICE_PATH"):
        e = min((e for e in exits if e in d), key=lambda e: d[e])
        route = [e]
        while route[-1] in parent:
            route.append(parent[route[-1]])
        print("  route:", list(reversed(route)))
    traps = [p for p in d if rows[p[1]][p[0]] == "i" and not (bfs([p]).keys() & set(starts))]
    return best, traps


def busy_cells(m: dict) -> set[tuple[int, int]]:
    """Every tile an object, NPC, trigger or warp (or its landing) claims."""
    out = {(x, y) for o in m["objects"]
           for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
           for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
    out |= {(p["at"]["tx"], p["at"]["ty"]) for p in m["npcs"] + m["triggers"] + m["warps"]}
    out |= {(p["to"]["tx"], p["to"]["ty"]) for p in m["warps"] if p.get("to")}
    return out


def edge_warps(m: dict, *, wid: str, cells: list[tuple[int, int]], to_map: str,
               to: list[tuple[int, int]], facing: str, suffix: str = "_e", **kw) -> None:
    """A wide edge crossing: one step_on warp per tile (ids wid, wid+suffix,
    wid+suffix2...), landing tile for tile."""
    for n, ((x, y), (tx, ty)) in enumerate(zip(cells, to)):
        w = {"id": wid + ("" if n == 0 else suffix if n == 1 else f"{suffix}{n}"),
             "at": {"tx": x, "ty": y}, "trigger": "step_on", "to_map": to_map,
             "to": {"tx": tx, "ty": ty}, "facing": facing, "transition": "fade"}
        w.update(kw)
        m["warps"].append(w)


def night_day(zones: list[dict], day_table: list[dict]) -> list[dict]:
    """The night/day zone pairs (common.md §3, the wickrun_chute pattern)."""
    out = []
    for z in zones:
        z = dict(z)
        z["hidden_when_flag"] = "flag:dawn"
        out.append(z)
    for z in zones:
        d = {k: v for k, v in z.items() if k != "hidden_when_flag"}
        d.update(id=z["id"] + "_day", table=day_table, requires_flag="flag:dawn")
        out.append(d)
    return out
