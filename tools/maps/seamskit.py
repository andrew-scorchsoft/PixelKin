#!/usr/bin/env python3
"""
seamskit — the small shared toolkit behind the Old Seams floors
(09-the-wild-ways §2 D; build_old_seams_*.py, build_emberroot_heart.py).

A floor is authored as two presence grids on mapkit — `wall` (cavewall rock) and
`shaft` (an open pit, the `seams_set` autotile family) — plus the traversal kit
(wildkit planks/ladders/slopes, seams_set rails). `finish()` turns them into the
standard cave layer stack:

    base (cave floor, cinder pins)  ->  t_shaft (shaft | wall)  ->  t_cavewall
    ->  deco  ->  above

The shaft layer's presence includes the rock so a pit running into a wall
reads as one dark drop (the wall layer then paints over its own cells).

Encounter zones come in night/day pairs (the Wild Ways convention: the night
zone hides at `flag:dawn`, its `_day` twin rises with it, lv 55-65).
"""
from __future__ import annotations

import random
from pathlib import Path

import mapkit as mk
from mapkit import gid

REPO = Path(__file__).resolve().parents[2]
SEAMS_INDEX = REPO / "assets/tilesets/seams/seams_set.index.json"
SEAMS = "seams_set"

MUSIC = "assets/audio/music/old-seams.mp3"
BACKDROPS = ["assets/backgrounds/battle/old-seams-a.webp",
             "assets/backgrounds/battle/old-seams-b.webp"]


def use_seams(m: dict) -> None:
    """Stack seams_set on the map (after any other accent set)."""
    if not any(t["name"] == SEAMS for t in m.get("tilesets", [])):
        m.setdefault("tilesets", []).append(mk.register_tileset(SEAMS, index=SEAMS_INDEX))


def S(name: str) -> int:
    return gid(name, set=SEAMS)


def grid(w: int, h: int) -> list[int]:
    return mk.make_grid(w, h)


def fill(g: list[int], w: int, x0: int, y0: int, x1: int, y1: int, v: int = 1) -> None:
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g[y * w + x] = v


def cells(x0: int, y0: int, x1: int, y1: int) -> set[tuple[int, int]]:
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}


def finish(m: dict, w: int, h: int, *, wall: list[int], shaft: list[int], deco: list[int],
           above: list[int], rng: random.Random, floor_mix: float = 0.5) -> None:
    """Write the layer stack (see module doc)."""
    cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
    base = [rng.choice(cf) if rng.random() < floor_mix else cf[0] for _ in range(w * h)]
    pit = [1 if (shaft[i] or wall[i]) else 0 for i in range(w * h)]
    layers = [{"name": "base", "role": "base", "depth": 0, "data": base}]
    if any(shaft):
        layers.append({"name": "t_shaft", "role": "terrain", "terrain": "shaft",
                       "set": SEAMS, "depth": 0, "data": pit})
    layers += [
        {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
         "set": "vesper_overworld_set", "depth": 0, "data": wall},
        {"name": "deco", "role": "deco", "depth": 5, "data": deco},
        {"name": "above", "role": "above", "depth": 20, "data": above},
    ]
    m["layers"] = layers


def zone_pair(m: dict, zid: str, rect: tuple[int, int, int, int], night: list, day: list,
              rate: float = 0.11) -> None:
    """A cave encounter zone (rect-wide roll) + its flag:dawn day twin."""
    x0, y0, x1, y1 = rect
    r = {"tx": x0, "ty": y0, "w": x1 - x0 + 1, "h": y1 - y0 + 1}
    m.setdefault("encounters", []).extend([
        {"id": zid, "terrain": "cave", "rect": r, "encounter_rate": rate,
         "table": night, "hidden_when_flag": "flag:dawn"},
        {"id": zid + "_day", "terrain": "cave", "rect": dict(r), "encounter_rate": rate,
         "table": day, "requires_flag": "flag:dawn"},
    ])


def T(*rows):
    """(kin, weight, lo, hi) rows -> an encounter table."""
    return [{"kin_id": k, "weight": wt, "min_level": lo, "max_level": hi}
            for (k, wt, lo, hi) in rows]


def obj(m: dict, oid: str, sprite: str, at: tuple[int, int], w: int, h: int, **kw) -> None:
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m.setdefault("objects", []).append(o)


def lever(m: dict, n: int, at: tuple[int, int]) -> None:
    """A yard lever (traverse_lever_off/_on, 1x2: handle walk-under, base solid)
    as a flag-visibility swap pair + the interact trigger on its base tile that
    throws it (script.seams_lever_<n> flips flag:seams_lever_<n>)."""
    flag = f"flag:seams_lever_{n}"
    x, y = at
    obj(m, f"lever_{n}", "traverse_lever_off", (x, y), 1, 2, overhang=1, walk_under=True,
        hidden_when_flag=flag)
    obj(m, f"lever_{n}_on", "traverse_lever_on", (x, y), 1, 2, overhang=1, walk_under=True,
        requires_flag=flag)
    m.setdefault("triggers", []).append(
        {"id": f"lever_{n}", "kind": "script", "at": {"tx": x, "ty": y + 1},
         "activation": "interact", "ref": f"script.seams_lever_{n}"})


def point_stand(m: dict, n: int, at: tuple[int, int]) -> None:
    """A junction's point-stand (traverse_switch_a = straight, _b = turnout),
    swapped on lever n's flag. Solid 1x1 (they share the footprint)."""
    flag = f"flag:seams_lever_{n}"
    obj(m, f"points_{n}", "traverse_switch_a", at, 1, 1, hidden_when_flag=flag)
    obj(m, f"points_{n}_on", "traverse_switch_b", at, 1, 1, requires_flag=flag)
