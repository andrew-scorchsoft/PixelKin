#!/usr/bin/env python3
"""
wildkit — stamps for the TRAVERSAL KIT (09-the-wild-ways.md §1), on mapkit.

Each stamp paints the `traverse_set` art AND writes the matching map data
(`flows` / `spans` / `jumps`), so art and behaviour can never drift apart:

    import wildkit as wk
    wk.use_traverse(m)                       # stack traverse_set on the map
    pin = {}                                 # -> mk.finalize(m, pin_base=pin)
    wk.chute(m, pin, deco, W, cells, "down", fid="upper")
    wk.ice(m, pin, cells, fid="pond")
    wk.deck(m, layer, W, rect=(x, y, w, h), axis="h", under=True, sid="trestle")
    wk.ladder(m, deco, W, x=12, y0=8, y1=10, sid="pitch_a")
    wk.plank(m, deco, W, rect=(x, y, w, h), axis="v", sid="gap")
    wk.jump(m, deco, W, at=(9, 20), dir="down", length=3, jid="kicker")

Rules of thumb (level-design §3a + the kit):
  * a chute must END on flat ground (a landing / run-out) or a warp — never on
    a wall, or the rider stops against it with nowhere to go but sideways;
  * an underpass deck goes in the map's `above` layer (it hides you beneath it);
    a deck over a gap/water goes in `deco` (you're never under it);
  * a ladder's top and bottom tiles must be ordinary walkable ground;
  * ramps only launch RIDERS (`ride: true` maps) — on foot they're ground.
"""
from __future__ import annotations

from pathlib import Path

import mapkit as mk
from mapkit import gid

REPO = Path(__file__).resolve().parents[2]
TRAVERSE_INDEX = REPO / "assets/tilesets/traverse/traverse_set.index.json"
SET = "traverse_set"

Cells = "set[tuple[int, int]] | list[tuple[int, int]]"


def use_traverse(m: dict) -> dict:
    """Register traverse_set for this build and add it to the map's tilesets."""
    if not any(t["name"] == SET for t in m.get("tilesets", [])):
        m.setdefault("tilesets", []).append(mk.register_tileset(SET, index=TRAVERSE_INDEX))
    return m


def T(name: str) -> int:
    return gid(name, set=SET)


def _rect_of(cells) -> dict | None:
    """The cells as a rect, if they exactly fill one."""
    cells = set(cells)
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    if len(cells) == (x1 - x0 + 1) * (y1 - y0 + 1):
        return {"tx": x0, "ty": y0, "w": x1 - x0 + 1, "h": y1 - y0 + 1}
    return None


def _area(cells) -> dict:
    r = _rect_of(cells)
    if r:
        return {"rect": r}
    return {"tiles": [{"tx": x, "ty": y} for (x, y) in sorted(set(cells), key=lambda c: (c[1], c[0]))]}


DIRV = {"down": (0, 1), "up": (0, -1), "left": (-1, 0), "right": (1, 0)}


def chute(m: dict, pin: dict, deco: list, w: int, cells, dir: str, *, fid: str,
          berms: bool = True, chevrons: int = 5, flags: dict | None = None) -> None:
    """A steep wax-road chute carrying `dir`: chute fills pinned into base, plank
    berms on its side edges, a tallow chevron every `chevrons` rows down the
    middle, and the slope flow. `flags` (requires_flag/hidden_when_flag) for a
    switched chute."""
    cells = set(cells)
    vertical = dir in ("down", "up")
    for (x, y) in cells:
        v = (x * 7 + y * 3) % 2
        pin[(x, y)] = f"chute_v_{v}" if vertical else f"chute_h_{v}"
    if berms:
        for (x, y) in cells:
            if vertical:
                if (x - 1, y) not in cells:
                    deco[y * w + x] = T("berm_w")
                elif (x + 1, y) not in cells:
                    deco[y * w + x] = T("berm_e")
            else:
                if (x, y - 1) not in cells:
                    deco[y * w + x] = T("berm_n")
                elif (x, y + 1) not in cells:
                    deco[y * w + x] = T("berm_s")
    if chevrons:
        for (x, y) in cells:
            if deco[y * w + x]:
                continue
            along = y if vertical else x
            across = x if vertical else y
            sides = sorted(c[0] if vertical else c[1] for c in cells
                           if (c[1] == y if vertical else c[0] == x))
            mid = sides[len(sides) // 2] if sides else across
            if across == mid and along % chevrons == 0:
                deco[y * w + x] = T(f"chev_{dir}")
    flow = {"id": fid, "kind": "slope", "dir": dir, **_area(cells)}
    flow.update(flags or {})
    m.setdefault("flows", []).append(flow)


def ice(m: dict, pin: dict, cells, *, fid: str) -> None:
    """A sheet of glare ice (slide until something stops you)."""
    cells = set(cells)
    for (x, y) in cells:
        pin[(x, y)] = f"glare_{(x + y) % 2}"
    m.setdefault("flows", []).append({"id": fid, "kind": "ice", **_area(cells)})


def rail_flow(m: dict, cells, dir: str, *, fid: str, flags: dict | None = None) -> None:
    """An ore-cart rail carrying `dir` (paint the rail art yourself: rail_* tiles)."""
    flow = {"id": fid, "kind": "rail", "dir": dir, **_area(cells)}
    flow.update(flags or {})
    m.setdefault("flows", []).append(flow)


def deck(m: dict, layer: list, w: int, *, rect: tuple[int, int, int, int], axis: str,
         sid: str, under: bool = False, shade: list | None = None) -> None:
    """A trestle deck over `rect` walked along `axis`. `layer` is the `above`
    layer for an underpass (pass `shade=deco` to darken the road beneath), else
    `deco`."""
    x0, y0, rw, rh = rect
    for y in range(y0, y0 + rh):
        for x in range(x0, x0 + rw):
            if axis == "h":
                name = "deck_h_w" if x == x0 else "deck_h_e" if x == x0 + rw - 1 else "deck_h"
            else:
                name = "deck_v_n" if y == y0 else "deck_v_s" if y == y0 + rh - 1 else "deck_v"
            layer[y * w + x] = T(name)
            if shade is not None:
                shade[y * w + x] = T("under_shade")
    span = {"id": sid, "kind": "bridge", "axis": axis,
            "rect": {"tx": x0, "ty": y0, "w": rw, "h": rh}}
    if under:
        span["under"] = True
    m.setdefault("spans", []).append(span)


def ladder(m: dict, deco: list, w: int, *, x: int, y0: int, y1: int, sid: str) -> None:
    """A ladder up a cliff band from row y1 (bottom) to y0 (top), inclusive —
    the rungs' own tiles; the ground above y0 and below y1 must be walkable."""
    for y in range(y0, y1 + 1):
        deco[y * w + x] = T("ladder_top" if y == y0 else "ladder")
    m.setdefault("spans", []).append({"id": sid, "kind": "ladder", "axis": "v",
                                      "rect": {"tx": x, "ty": y0, "w": 1, "h": y1 - y0 + 1}})


def plank(m: dict, deco: list, w: int, *, rect: tuple[int, int, int, int], axis: str,
          sid: str) -> None:
    """A rope-plank walk over a gap, along `axis`."""
    x0, y0, rw, rh = rect
    for y in range(y0, y0 + rh):
        for x in range(x0, x0 + rw):
            deco[y * w + x] = T(f"plank_{axis}")
    m.setdefault("spans", []).append({"id": sid, "kind": "plank", "axis": axis,
                                      "rect": {"tx": x0, "ty": y0, "w": rw, "h": rh}})


def jump(m: dict, deco: list, w: int, *, at: tuple[int, int], dir: str, length: int = 3,
         jid: str) -> None:
    """A timber kicker: a rider meeting it heading `dir` clears `length` tiles."""
    deco[at[1] * w + at[0]] = T(f"ramp_{dir}")
    m.setdefault("jumps", []).append({"id": jid, "at": {"tx": at[0], "ty": at[1]},
                                      "dir": dir, "length": length})


def face_wall(pin: dict, *, x0: int, x1: int, y0: int, y1: int, family: str = "rock") -> None:
    """Rows y0..y1 of a TALL cliff face (below the cliff family's edge_s lip):
    mid-face rows, the last row the foot with its contact shadow. Solid."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            pin[(x, y)] = (f"face_{family}_foot" if y == y1
                           else f"face_{family}_{(x // 3 + y) % 2}")
