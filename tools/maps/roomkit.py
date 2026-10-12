#!/usr/bin/env python3
"""
roomkit — the interior composition toolkit (mapkit's indoor sibling).

Interiors were one faced square each: same-y rooms with AI props floating off
the walls. This kit makes an interior a COMPOSITION (docs/world/interiors.md):

  * `faced_room`      the SNES enclosure (cap row + visible north FACE,
                      banded sides, doormat exit) — the outer shell;
  * `partition_v/h`   INTERNAL walls in the same cap/face system, with door
                      gaps — a cottage becomes hearth-room + bed nook, an inn
                      grows a bunk room, a shrine gets side niches;
  * `place`           manifest-driven object placement (no hand-typed w/h);
  * `wall_mount`      flush furniture: wall pieces (hearth, bookcase, shelf,
                      dresser, stove, lamp rack — interiorforge.WALL_MOUNTED)
                      are drawn as pure front elevations and placed with their
                      TOP ROW OVER the wall FACE row (overhang=1, walk-under),
                      so they stand against the wall, never in front of it;
  * `runner`          the aisle tiles;
  * `finish`          write → render → audit_flow (reach) — the interior QA.

Tile indices match build_interior_walls.py's kits (warm + cool): the legacy
13 tiles, then the APPENDED wall-band blob + face ends (`appended_tiles()`),
which `finish` resolves from each wall tile's neighbourhood (`autotile_walls`).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public/assets/maps"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

# ---- the wall band blob set (shared with build_interior_walls.py) --------------
# A wall-top BAND tile is drawn from its neighbourhood: a lit lip on every SIDE
# whose neighbour is open (floor, doormat or a wall FACE), plus a corner NUB
# where a diagonal is open but both sides beside it are wall — the inner turn
# that joins two lips. The original 13-tile kit carried only the four single
# sides + four convex corners, so a divider meeting the ceiling showed the
# ceiling's lip running straight across its top, a room corner overshot into a
# "+" and a partition's far side had no edge at all. The full 47-shape blob is
# APPENDED after the original 13 (indices never move), then three FACE ends —
# the wall face with a shaded side where it stops in the open (a pillar front,
# a partition's free end, a doorway jamb).
_SIDE_ORDER = "nsew"
_CORNERS = (("ne", "n", "e"), ("nw", "n", "w"), ("se", "s", "e"), ("sw", "s", "w"))
# the original kit's band tiles, by (open sides) — kept at their old gids
_LEGACY_BANDS = {frozenset("s"): 6, frozenset("n"): 7, frozenset("e"): 8, frozenset("w"): 9,
                 frozenset("se"): 10, frozenset("sw"): 11, frozenset("ne"): 12, frozenset("nw"): 13}


def band_shapes():
    """Every (sides, nubs) band shape, in a FIXED order: [(name, sides, nubs)].
    The legacy eight are included (their gids come from _LEGACY_BANDS)."""
    out = []
    for mask in range(16):
        sides = frozenset(s for i, s in enumerate(_SIDE_ORDER) if mask >> i & 1)
        free = [c for c, a, b in _CORNERS if a not in sides and b not in sides]
        for nm in range(1 << len(free)):
            nubs = frozenset(c for i, c in enumerate(free) if nm >> i & 1)
            name = ("band_" + ("".join(s for s in _SIDE_ORDER if s in sides) or "x")
                    + "_" + ("".join(c for c, _, _ in _CORNERS if c in nubs) or "x"))
            out.append((name, sides, nubs))
    return out


def appended_tiles():
    """The tiles APPENDED after the legacy 13, in order: [(name, sides, nubs)]
    for the new band shapes, then the three face ends (sides/nubs None).
    Append-only: never reorder (every interior's gids ride these indices)."""
    new = [(n, s, b) for (n, s, b) in band_shapes()
           if not (s in _LEGACY_BANDS and not b)]
    return new + [("face_end_w", None, None), ("face_end_e", None, None),
                  ("face_end_ew", None, None)]


_APPENDED = appended_tiles()
TILE_COUNT = 13 + len(_APPENDED)
BAND_GID = {(s, frozenset()): g for s, g in _LEGACY_BANDS.items()}
for _i, (_n, _s, _b) in enumerate(_APPENDED):
    if _s is not None:
        BAND_GID[(_s, _b)] = 14 + _i
FACE_END_W, FACE_END_E, FACE_END_EW = TILE_COUNT - 2, TILE_COUNT - 1, TILE_COUNT
BAND_GIDS = set(BAND_GID.values())

# ---- the two wall/floor kits (same order: legacy 13 + the appended blob) -------
WARM_SET = {
    "name": "interior_set", "image": "assets/tilesets/interior_set.webp",
    "tile_width": 16, "tile_height": 16, "first_gid": 1, "columns": 8,
    "tile_count": TILE_COUNT,
}
COOL_SET = {
    "name": "interior_stone_set", "image": "assets/tilesets/interior_stone_set.webp",
    "tile_width": 16, "tile_height": 16, "first_gid": 1, "columns": 8,
    "tile_count": TILE_COUNT,
}
# gids = local index + 1
FLOOR, FLOOR_B, DOORMAT, FACE, WINDOW = 1, 2, 3, 4, 5
CAP_S, CAP_N, CAP_E, CAP_W = 6, 7, 8, 9
CAP_TL, CAP_TR, CAP_BL, CAP_BR = 10, 11, 12, 13
RUNNER, BANNER = 3, 5  # cool-set aliases
FACE_GIDS = {FACE, FACE_END_W, FACE_END_E, FACE_END_EW}

_MANIFEST = json.loads(
    (REPO / "public/assets/sprites/objects/objects.manifest.json").read_text())["objects"]
WALL_MOUNTED = {"hearth", "bookcase", "shelf", "dresser", "stove", "lamp_rack",
                # wall-HUNG (no floor contact; mount with solid=False — the
                # banners at the default face_row=1, kite_hung at face_row=0
                # so it clears a 3x3 altar beneath it)
                "banner_warm", "banner_ice", "kite_hung",
                # the Lamp-school's chalkboard (a solid wall piece, like the bookcase)
                "chalkboard",
                # the Wayward Arms' back-bar shelving + the stair to the rooms
                "bar_back", "stair_up"}


def grid(w, h, fill=0):
    return [fill] * (w * h)


def rect(g, w, x0, y0, x1, y1, val):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g[y * w + x] = val


# ---- the shell -----------------------------------------------------------------
def faced_room(W, H, door_x, floor_fill=FLOOR, floor_alt=FLOOR_B):
    """(base, over) layers for the SNES enclosure: cap+face north wall, banded
    sides/bottom with the lit lip facing the floor, checkered floor, doormat."""
    base = grid(W, H, floor_fill)
    over = grid(W, H, 0)
    for y in range(2, H - 1):
        for x in range(1, W - 1):
            if (x + y) % 2 == 0:
                base[y * W + x] = floor_alt
    for x in range(W):
        over[0 * W + x] = CAP_S
        over[1 * W + x] = FACE
    over[0 * W + 0] = CAP_TL
    over[0 * W + (W - 1)] = CAP_TR
    over[1 * W + 0] = CAP_E
    over[1 * W + (W - 1)] = CAP_W
    for y in range(2, H - 1):
        over[y * W + 0] = CAP_E
        over[y * W + (W - 1)] = CAP_W
    for x in range(W):
        over[(H - 1) * W + x] = CAP_N
    over[(H - 1) * W + 0] = CAP_BL
    over[(H - 1) * W + (W - 1)] = CAP_BR
    base[(H - 1) * W + door_x] = DOORMAT
    over[(H - 1) * W + door_x] = 0
    return base, over


def windows(over, W, cols, tile=WINDOW):
    """Window/banner insets on the top wall-FACE row (or a partition's face)."""
    for c in cols:
        over[1 * W + c] = tile


# ---- internal partitions ---------------------------------------------------------
def partition_v(over, W, x, y0, y1, *, lip="w", doors=()):
    """A vertical internal wall: one column of the dark wall-top band, the lit
    lip facing the `lip` side ('w' = the room to the west). `doors` rows stay
    open. Use it to split a bed nook, a bunk room, a storeroom off the room.

    Read as a real wall (2026-10): the column JOINS the wall above it — where
    the tile over its top is a wall FACE (the room's north face row, or a
    partition_h face), that face tile becomes band so the ceiling runs into
    the divider instead of passing behind it — and every segment's SOUTH end
    is a FACE tile, the front of the pillar, the way the north wall shows its
    face. Collision is unchanged (band and face both collide)."""
    cap = CAP_W if lip == "w" else CAP_E
    rows = [y for y in range(y0, y1 + 1) if y not in doors]
    for y in rows:
        over[y * W + x] = cap
    if rows and y0 - 1 >= 0 and over[(y0 - 1) * W + x] in (FACE, WINDOW):
        over[(y0 - 1) * W + x] = cap
    # the south end of each run (before a door gap, and the last one) shows
    # its FACE — unless the run runs straight into another wall band below
    # (the room's bottom wall): then it simply JOINS it, no face
    for y in rows:
        if y + 1 not in rows:
            i = (y + 1) * W + x
            if not (i < len(over) and over[i] in BAND_GIDS):
                over[y * W + x] = FACE
    # (the lips are drawn by autotile_walls() at finish time — `lip` only
    # picks the provisional tile; both sides of the wall get their edge)


def partition_h(base, over, W, y, x0, x1, *, doors=(), face=True):
    """A horizontal internal wall in the full north-wall system: the band row
    at `y-1`, the visible FACE at `y` (set face=False for a low divider that's
    band-only). `doors` columns stay open in both rows. The face row accepts
    `windows()`-style insets via direct assignment and `wall_mount(face_row=y)`."""
    for x in range(x0, x1 + 1):
        if x in doors:
            continue
        over[(y - 1) * W + x] = CAP_S
        if face:
            over[y * W + x] = FACE
    return y  # the face row (for wall_mount)


# ---- furniture -------------------------------------------------------------------
def spec(stem: str) -> dict:
    return _MANIFEST[f"interior_{stem}"]


def place(objects: list, stem: str, tx: int, ty: int, *, oid: str | None = None,
          solid: bool = True) -> dict:
    """Place a free-standing piece by manifest footprint (no hand-typed w/h)."""
    s = spec(stem)
    o = {"id": oid or stem, "sprite": f"interior_{stem}",
         "at": {"tx": tx, "ty": ty}, "w": s["tw"], "h": s["th"]}
    if not solid:
        o["solid"] = False
    objects.append(o)
    return o


def wall_mount(objects: list, stem: str, tx: int, *, face_row: int = 1,
               oid: str | None = None, solid: bool = True) -> dict:
    """Mount a WALL piece flush: top row drawn OVER the wall face (the face
    tile keeps colliding underneath), floor rows solid. The piece must be one
    of interiorforge.WALL_MOUNTED — its art has the cornice shadow + floor
    contact built in, so anywhere else it would read as a floating crate."""
    assert stem in WALL_MOUNTED, f"{stem} is not a wall-mounted piece"
    s = spec(stem)
    o = {"id": oid or stem, "sprite": f"interior_{stem}",
         "at": {"tx": tx, "ty": face_row}, "w": s["tw"], "h": s["th"],
         "overhang": 1, "walk_under": True}
    if not solid:
        o["solid"] = False
    objects.append(o)
    return o


def runner(base, W, x, y0, y1, tile=RUNNER):
    for y in range(y0, y1 + 1):
        base[y * W + x] = tile


def aisle_runner(objects: list, x: int, y0: int, y1: int) -> None:
    """A carpet AISLE up the hall: stacked `interior_rug_runner` 1x3 segments
    (the drawn deep-blue runner with diamond motifs; solid:false, walk-on).
    Prefer this over `runner()` for any aisle longer than a doormat — the
    doormat TILE repeated vertically reads as a ladder (hard black cell
    borders), which is exactly the dodgy-path look it replaces. Spans that
    aren't a multiple of 3 keep the remainder as plain floor at the door end."""
    seg = spec("rug_runner")["th"]
    y = y0
    while y + seg - 1 <= y1:
        place(objects, "rug_runner", x, y, oid=f"aisle_{y}", solid=False)
        y += seg


# ---- assembly + QA ----------------------------------------------------------------
def mapdef(id_, name, W, H, tileset, base, over, objects, warps, triggers, npcs, music):
    return {
        "id": id_, "display_name": name,
        "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "interior",
        "tilesets": [tileset],
        "layers": [
            {"name": "base", "role": "base", "depth": 0, "data": base},
            {"name": "walls", "role": "deco", "depth": 5, "data": over},
        ],
        "objects": objects,
        "warps": warps, "triggers": triggers, "encounters": [], "npcs": npcs,
        "gates": [], "music": music,
    }


def obj(id_, sprite, tx, ty, w, h, overhang=0, solid=True):
    """Raw object placement (legacy callers; prefer place()/wall_mount())."""
    o = {"id": id_, "sprite": sprite, "at": {"tx": tx, "ty": ty}, "w": w, "h": h}
    if overhang:
        o["overhang"] = overhang
    if not solid:
        o["solid"] = False
    return o


def dress_tower_stairs(m: dict) -> None:
    """A tower floor's `up_stairs` / `down_stairs` warps (the Beacon, the Old
    Light) get a real stair sprite on their pad: the UP-stair climbs the wall
    face from the pad (1x2, top row over the wall), the DOWN-stair is a
    stairwell sunk in the floor (1x1). Both non-solid — the step_on warp rides
    the pad as before. (A plain doormat square read as nothing in particular.)"""
    have = {o["id"] for o in m.get("objects", [])}
    for w in m.get("warps", []):
        x, y = w["at"]["tx"], w["at"]["ty"]
        if w["id"] == "up_stairs" and "stairs_up_sprite" not in have:
            m.setdefault("objects", []).append(
                {"id": "stairs_up_sprite", "sprite": "interior_stairs_up",
                 "at": {"tx": x, "ty": y - 1}, "w": 1, "h": 2, "solid": False})
        elif w["id"] == "down_stairs" and "stairs_down_sprite" not in have:
            m.setdefault("objects", []).append(
                {"id": "stairs_down_sprite", "sprite": "interior_stairs_down",
                 "at": {"tx": x, "ty": y}, "w": 1, "h": 1, "solid": False})


def autotile_walls(over: list, W: int, H: int) -> list:
    """Re-draw every wall tile from its neighbourhood (in place; returns over).

    BAND tiles (any cap/band gid) get the lit lip on each side that meets the
    open room (floor, doormat, or a wall FACE) and a corner nub where two walls
    meet around an open diagonal — so a divider JOINS the ceiling band (a T, no
    lip across its top), room corners turn instead of crossing, a partition
    shows its edge on BOTH sides and a free end wraps round. FACE tiles that
    stop in the open get a shaded side (the face end / pillar front). Windows,
    banners and any other overlay gid are left alone and count as face; out of
    bounds counts as wall. Collision is unchanged: every band/face shape collides."""
    def kind(x, y):
        if not (0 <= x < W and 0 <= y < H):
            return "band"
        g = over[y * W + x]
        if g == 0:
            return "open"
        return "band" if g in BAND_GIDS else "face"
    diag = {"ne": (1, -1), "nw": (-1, -1), "se": (1, 1), "sw": (-1, 1)}
    out = list(over)
    for y in range(H):
        for x in range(W):
            g = over[y * W + x]
            if g in BAND_GIDS:
                nb = {"n": kind(x, y - 1), "s": kind(x, y + 1),
                      "e": kind(x + 1, y), "w": kind(x - 1, y)}
                sides = frozenset(d for d, k in nb.items() if k != "band")
                nubs = frozenset(c for c, a, b in _CORNERS
                                 if a not in sides and b not in sides
                                 and kind(x + diag[c][0], y + diag[c][1]) != "band")
                out[y * W + x] = BAND_GID[(sides, nubs)]
            elif g in FACE_GIDS:
                ow, oe = kind(x - 1, y) == "open", kind(x + 1, y) == "open"
                out[y * W + x] = (FACE_END_EW if ow and oe else FACE_END_W if ow
                                  else FACE_END_E if oe else FACE)
    over[:] = out
    return over


def finish(m: dict, *, scale: int = 5) -> bool:
    """Write, render, and run the flow audit's reach check. Returns ok."""
    dress_tower_stairs(m)
    walls = next(l for l in m["layers"] if l["name"] == "walls")
    autotile_walls(walls["data"], m["width"], m["height"])
    path = MAPS / f"{m['id']}.json"
    path.write_text(json.dumps(m, indent=2) + "\n")
    out = Path("/tmp") / f"{m['id']}.png"
    subprocess.run([sys.executable, str(SCRIPTS / "render_map.py"), str(path),
                    "--output", str(out), "--scale", str(scale)], capture_output=True)
    aud = subprocess.run([sys.executable, str(REPO / "tools/maps/audit_flow.py"), m["id"]],
                         capture_output=True, text=True)
    print(aud.stdout.strip())
    print(f"  wrote {path.relative_to(REPO)}  ->  rendered {out}")
    return aud.returncode == 0


# legacy name (build_beacon.py imports it via build_interiors)
def write_and_render(m):
    finish(m)
