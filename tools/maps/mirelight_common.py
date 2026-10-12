"""
mirelight_common — shared pieces for the Mirelights builders (09-the-wild-ways §2 B):
the Glassmere's DEEP water, the false-light plank WALKS, the encounter tables.

The Glassmere is a drowned field: a shallow shelf (Tidecall swims it) rings every
bit of walkable shore, and everything past it is DEEP (the reserved `deepdive`
Gift no one holds) — so by the time you get here (lv ~40, every early Gift in
hand) the water is a wall again and the only ways across are the old boards.

A WALK is one rope-plank span (`wildkit.plank`) out over the deep. Every walk
has a blue will-light hung at its far end — the lights lie, they all look the
same. Through the Frostglass Lens (the ferry's price, so always held out here)
the old causeway-reeds at each walk's MOUTH show the truth: a LIT reed marks a
real board-walk, a DEAD reed a lie. A false walk stops short over the deep; its
last board gives way (a step_on beat: `script.mirelight_dunk_<id>` — narrated,
then a `travel` back to the walk's mouth).
"""
from __future__ import annotations

import mapkit as mk
import wildkit as wk
from mapkit import gid

LENS = "flag:has_frostglass_lens"
DEEP_INDEX = mk.REPO / "assets/tilesets/deepwater/deepwater_set.index.json"


def obj(m, oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    m.setdefault("objects", []).append(o)
    return o


def deep_layer(m: dict, pond: list, walk: set, W: int, H: int, *,
               shallow: set = frozenset(), deep_extra: set = frozenset()) -> list:
    """Mark the mere DEEP: every pond cell NOT within one tile (8-way) of WALKABLE
    dry ground (`walk`) — a tree border is not a shore, so the deep runs right up
    to the woods and no shelf sneaks round a channel's end. `shallow` keeps
    designed swim lanes (currents); `deep_extra` forces cells deep. Adds the
    deepwater_set ref + a terrain layer (call after the other terrain layers are
    in m["layers"]). Returns the deep grid."""
    deep = [0] * (W * H)
    for y in range(H):
        for x in range(W):
            i = y * W + x
            if not pond[i] or (x, y) in shallow:
                continue
            near = any((x + dx, y + dy) in walk for dx in (-1, 0, 1) for dy in (-1, 0, 1))
            if not near or (x, y) in deep_extra:
                deep[i] = 1
    if not any(t["name"] == "deepwater_set" for t in m["tilesets"]):
        m["tilesets"].append(mk.register_tileset("deepwater_set", index=DEEP_INDEX))
    last = max(i for i, ly in enumerate(m["layers"]) if ly.get("role") in ("terrain", "base"))
    m["layers"].insert(last + 1, {"name": "t_deepwater", "role": "terrain",
                                  "terrain": "deepwater", "set": "deepwater_set",
                                  "depth": 0, "data": deep})
    return deep


DIRV = {"right": (1, 0), "left": (-1, 0), "down": (0, 1), "up": (0, -1)}
FACE_BACK = {"right": "right", "left": "left", "down": "down", "up": "up"}


def walk(m: dict, deco: list, W: int, *, wid: str, mouth: tuple[int, int], dir: str,
         length: int, true: bool, dunks: list, light: bool = True,
         reed_side: int = -1) -> list[tuple[int, int]]:
    """A plank walk out from dry `mouth` heading `dir` for `length` tiles.
    TRUE: the planks must land on dry ground (the caller carves it).
    FALSE: the last plank is the board that gives way — a step_on trigger runs
    script.mirelight_dunk_<wid>, recorded in `dunks` as (wid, map, mouth, dir)
    so the content module can stage it. Lights: a blue will-light on the water
    beside the far end; with the Lens, a lit/dead causeway-reed beside the mouth
    on side `reed_side` (-1 = left/up of the axis, +1 = right/down)."""
    dx, dy = DIRV[dir]
    cells = [(mouth[0] + dx * k, mouth[1] + dy * k) for k in range(1, length + 1)]
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    axis = "h" if dy == 0 else "v"
    wk.plank(m, deco, W, rect=(min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1),
             axis=axis, sid=wid)
    end = cells[-1]
    # the reed at the mouth: beside it, perpendicular to the walk (1x2, base row
    # level with the mouth) — through the lens: lit = true, dead = a lie
    if axis == "h":
        rx, ry = mouth[0], mouth[1] + (1 if reed_side > 0 else -2) - (0 if reed_side > 0 else 0)
        rx, ry = mouth[0], (mouth[1] + 1) if reed_side > 0 else (mouth[1] - 2)
    else:
        rx, ry = (mouth[0] + 1) if reed_side > 0 else (mouth[0] - 1), mouth[1] - 1
    obj(m, f"{wid}_reed", "saltreach_reed_lantern_lit" if true else "saltreach_reed_lantern_dark",
        (rx, ry), 1, 2, overhang=1, walk_under=True, solid=False, requires_flag=LENS)
    if light:
        # the will-light: just past the end for a lie (it's what you were
        # following), above the last board for a true walk
        lx, ly = ((end[0] + dx, end[1] + dy) if not true
                  else (end[0], end[1] + 1) if axis == "h" else (end[0] + 1, end[1]))
        obj(m, f"{wid}_light", "mirelight_marsh_light", (lx, ly), 1, 1, solid=False)
    if not true:
        m.setdefault("triggers", []).append(
            {"id": f"dunk_{wid}", "kind": "cutscene", "at": {"tx": end[0], "ty": end[1]},
             "activation": "step_on", "ref": f"script.mirelight_dunk_{wid}"})
        dunks.append((wid, m["id"], mouth, dir))
    return cells


def current(m: dict, cells, dir: str, *, fid: str) -> None:
    """A Glassmere CURRENT: a one-way slope flow over shallow (Tidecall) water —
    swim into it and the mere carries you `dir`; you can't swim back up it."""
    m.setdefault("flows", []).append({"id": fid, "kind": "slope", "dir": dir,
                                      **wk._area(set(cells))})


def zones(m: dict, grass: list, W: int, H: int, *, prefix: str, night: list, day: list,
          rate: float = 0.1) -> None:
    import patterns as pt
    nz = pt.zones_from_grid(grass, W, H, terrain="tall_grass", rate=rate,
                            id_prefix=prefix, table=night)
    for z in nz:
        z["hidden_when_flag"] = "flag:dawn"
    dz = [{**z, "id": z["id"] + "_day", "table": day, "requires_flag": "flag:dawn"}
          for z in pt.zones_from_grid(grass, W, H, terrain="tall_grass", rate=rate,
                                      id_prefix=prefix, table=day)]
    for z in dz:
        z.pop("hidden_when_flag", None)
    m["encounters"] = nz + dz


# ---- the tables (mirrored in build_species.py _MIRE_TABLES -> EXTRA_ENCOUNTERS) ----
# Tidwraith #22, Lumplass #32 and Lampling #148 are the Mirelights' own (rare:
# the grown D-tier forms are the trainers'); the fen's tide-lights fill the rest,
# at the lv-40 beds' strength. By day (the R4 convention) the SAME species wake,
# +17 levels and four wider. (kin, weight, night min, night max)
_NIGHT = {
    "landing": [(31, 30, 38, 40), (67, 24, 38, 41), (27, 22, 38, 40), (60, 16, 39, 40),
                (22, 8, 39, 41)],
    "glassmere": [(31, 30, 40, 42), (21, 24, 40, 42), (29, 22, 40, 41), (22, 9, 40, 42),
                  (32, 9, 41, 42), (148, 6, 42, 42)],
    "chapel": [(31, 28, 41, 43), (67, 22, 41, 42), (21, 20, 41, 43), (32, 12, 41, 43),
               (22, 9, 41, 43), (148, 9, 43, 43)],
}
DAY_SHIFT = 17


def _table(rows, shift=0, widen=0):
    return [{"kin_id": k, "weight": w, "min_level": lo + shift, "max_level": hi + shift + widen}
            for (k, w, lo, hi) in rows]


LANDING_NIGHT = _table(_NIGHT["landing"])
GLASSMERE_NIGHT = _table(_NIGHT["glassmere"])
CHAPEL_NIGHT = _table(_NIGHT["chapel"])
LANDING_DAY = _table(_NIGHT["landing"], DAY_SHIFT, 4)
GLASSMERE_DAY = _table(_NIGHT["glassmere"], DAY_SHIFT, 4)
CHAPEL_DAY = _table(_NIGHT["chapel"], DAY_SHIFT, 4)

MIRE_AMB = {
    "particles": [{"kind": "glowmotes", "density": 0.55}, {"kind": "spray", "density": 0.3}],
    "mist": {"color": "#9fc4d8", "alpha": 0.2, "speed": 5},
    "tint": {"color": "#1c3550", "alpha": 0.12},
    "starfall": {"min_s": 40, "max_s": 90},
    "sound_bed": "amb-marsh",
}
