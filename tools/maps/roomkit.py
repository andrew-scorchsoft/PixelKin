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

Tile indices match build_interior_walls.py's 13-tile kits (warm + cool).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public/assets/maps"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

# ---- the two wall/floor kits (13 tiles each, same order) ----------------------
WARM_SET = {
    "name": "interior_set", "image": "assets/tilesets/interior_set.webp",
    "tile_width": 16, "tile_height": 16, "first_gid": 1, "columns": 8, "tile_count": 13,
}
COOL_SET = {
    "name": "interior_stone_set", "image": "assets/tilesets/interior_stone_set.webp",
    "tile_width": 16, "tile_height": 16, "first_gid": 1, "columns": 8, "tile_count": 13,
}
# gids = local index + 1
FLOOR, FLOOR_B, DOORMAT, FACE, WINDOW = 1, 2, 3, 4, 5
CAP_S, CAP_N, CAP_E, CAP_W = 6, 7, 8, 9
CAP_TL, CAP_TR, CAP_BL, CAP_BR = 10, 11, 12, 13
RUNNER, BANNER = 3, 5  # cool-set aliases

_MANIFEST = json.loads(
    (REPO / "public/assets/sprites/objects/objects.manifest.json").read_text())["objects"]
WALL_MOUNTED = {"hearth", "bookcase", "shelf", "dresser", "stove", "lamp_rack"}


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
    open. Use it to split a bed nook, a bunk room, a storeroom off the room."""
    cap = CAP_W if lip == "w" else CAP_E
    for y in range(y0, y1 + 1):
        if y in doors:
            continue
        over[y * W + x] = cap


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


def finish(m: dict, *, scale: int = 5) -> bool:
    """Write, render, and run the flow audit's reach check. Returns ok."""
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
