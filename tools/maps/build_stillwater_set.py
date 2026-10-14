#!/usr/bin/env python3
"""
build_stillwater_set — Stillwater's accent tileset (`stillwater_set`).

The shared overworld set is FROZEN, and Stillwater needs one family it cannot
give: a village LANE whose transitions are context-correct on BLIGHT ground.
The shared `path` rings itself with green grass on the drained ground and
`ruinfloor` with gold — both wrong (CLAUDE.md: "painting one over the wrong
ground rings it with the wrong colour"). This draws `flagway`: swept pale-grey
flagstones, laid square and kept clean (the Hollowing's tended register), with
every transition composed over `gbaforge.blight_fill` (the build_coldfog_set.py
pattern, verbatim in method).

Writes:
  assets/tilesets/stillwater/set_tiles/*.png + tileset.manifest.json  (masters)
  public/assets/tilesets/stillwater_set.{webp,tileset.json}           (served)
  assets/tilesets/stillwater/stillwater_set.index.json                (name->index)

Run:  python3 tools/maps/build_stillwater_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

import gbaforge
from gbaforge import sh, overlay_tile, img, flat, put

# the mere's nub roles (a thin spur's tip / a lone cell): the open sides, so
# gbaforge.overlay_mask rounds them like any other corner (this process only)
for _r, _e in {"end_n": ("N", "W", "E"), "end_s": ("S", "W", "E"),
               "end_w": ("W", "N", "S"), "end_e": ("E", "N", "S"),
               "single": ("N", "S", "W", "E")}.items():
    gbaforge.ROLES_OUTER.setdefault(_r, _e)

REPO = Path(__file__).resolve().parents[2]
TILES_DIR = REPO / "assets" / "tilesets" / "stillwater" / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

FLAG = (128, 132, 138)          # swept pale-grey flagstone (cooler + lighter than BLIGHT)

# deliberate joint layouts per variant (the gbaforge rule: motifs, never noise)
LAYOUTS = [
    [("h", 0, 7, 16), ("v", 7, 0, 7), ("v", 11, 8, 16), ("d", 3, 3), ("d", 13, 12)],
    [("h", 0, 8, 16), ("v", 4, 0, 8), ("v", 12, 0, 8), ("v", 8, 9, 16), ("d", 2, 12)],
    [("h", 0, 5, 16), ("h", 0, 12, 16), ("v", 9, 0, 5), ("v", 5, 6, 12), ("v", 12, 13, 16)],
]


def flagway_fill(v: int = 0):
    a = flat(FLAG)
    joint = sh(FLAG, 0.74)
    lit = sh(FLAG, 1.12, 6)
    for item in LAYOUTS[v % len(LAYOUTS)]:
        if item[0] == "h":
            _, x0, y, x1 = item
            put(a, [(x, y) for x in range(x0, x1)], joint)
            put(a, [(x, y + 1) for x in range(x0, x1, 3) if y + 1 < 16], lit)
        elif item[0] == "v":
            _, x, y0, y1 = item
            put(a, [(x, y) for y in range(y0, min(y1, 16))], joint)
        else:
            _, x, y = item
            put(a, [(x, y), (x + 1, y)], sh(FLAG, 0.88))
    return img(a)


def flagway_tile(role: str, v: int = 0):
    if role == "fill":
        return flagway_fill(v)
    return overlay_tile(role, flagway_fill(v), gbaforge.blight_fill(v),
                        sh(FLAG, 0.50), shade_rgb=sh(FLAG, 0.84))


ROLES = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
         "corner_sw", "edge_s", "corner_se", "strip_h", "strip_v",
         "inner_nw", "inner_ne", "inner_sw", "inner_se"]

# ---- THE STILL WATER (2026-10 fix pass): `mere` --------------------------------------
# The village's mere drawn as its own family so it never reads as a stepped box:
# the shore bites deep into every edge cell (t=6) with wide rounded corners (r=6),
# a 2px pale stone LIP on the land side (laid stones, dark joints), a dark reflection
# of that lip on the water side, and a near-black water so still it holds a few
# stars. Collision mirrors the shared `murk` (water, Tidecall-swimmable) so every
# audit sees the same mere it always did.
MERE = (38, 46, 60)
MERE_T, MERE_R = 6, 6
STARS = [[(3, 4), (12, 10)], [(9, 3), (5, 12)], [(13, 6)]]
STONE = [(92, 96, 98), (128, 132, 132), (156, 160, 158), (54, 58, 62)]


def mere_fill(v: int = 0):
    a = flat(MERE)
    put(a, [(x, y) for (x, y) in [(2, 9), (3, 9), (10, 14), (11, 14)]], sh(MERE, 1.22, 4))
    for (x, y) in STARS[v % len(STARS)]:
        put(a, [(x, y)], (176, 186, 204))
        put(a, [(x + 1, y), (x - 1, y)], sh(MERE, 1.5, 10))
    return img(a)


def mere_tile(role: str, v: int = 0):
    if role == "fill":
        return mere_fill(v)
    m = gbaforge.overlay_mask(role, MERE_T, MERE_R)          # True = land
    a = np.asarray(mere_fill(v).convert("RGBA")).astype(np.int16).copy()
    o = np.asarray(gbaforge.blight_fill(v).convert("RGBA")).astype(np.int16)
    a[m] = o[m]
    water = ~m
    near1 = gbaforge._dilate(water, 1) & m                    # land px touching water
    near2 = gbaforge._dilate(water, 2) & m & ~near1
    for (y, x) in zip(*np.where(near2)):                      # the stone lip, back row
        a[y, x, :3] = STONE[1] if (x // 3 + y // 3) % 2 else STONE[0]
    for (y, x) in zip(*np.where(near1)):                      # the lip's lit front row
        a[y, x, :3] = STONE[3] if (x + y) % 4 == 0 else STONE[2]
    r1 = gbaforge._dilate(m, 1) & water                       # the lip's shadow on the water
    r2 = gbaforge._dilate(m, 2) & water & ~r1                 # ...and its faint reflection
    a[r1, :3] = (14, 16, 22)
    for (y, x) in zip(*np.where(r2)):
        if (x + y) % 3:
            a[y, x, :3] = sh(MERE, 1.45, 8)
    return img(a)


def jetty_tile(base_im, end: bool = False):
    """Boards over the water, 10px wide down the middle of the cell (the jetty
    runs north-south). `end` adds the two mooring posts at its tip."""
    a = np.asarray(base_im.convert("RGBA")).astype(np.int16).copy()
    BO = [(46, 38, 32), (84, 72, 60), (112, 98, 82), (136, 122, 104)]
    x0, x1 = 3, 12
    a[:, x0 - 1, :3] = (14, 16, 22)                           # the boards' shadow on the water
    a[:, x1 + 1, :3] = (14, 16, 22)
    for y in range(16):
        a[y, x0:x1 + 1, :3] = BO[2]
        a[y, x0, :3] = BO[3]
        a[y, x1, :3] = BO[1]
        if y % 4 == 3:
            a[y, x0:x1 + 1, :3] = BO[0]                       # plank joints
        if y % 4 == 1:
            a[y, x0 + 2, :3] = BO[1]                          # nail heads
            a[y, x1 - 2, :3] = BO[1]
    if end:
        for px in (x0 - 2, x1 + 1):
            a[0:6, px:px + 2, :3] = BO[0]
            a[0, px:px + 2, :3] = BO[3]
            a[6, px:px + 2, :3] = (14, 16, 22)
    return img(a)


def mere_reeds(v: int = 0):
    """A transparent DECO tuft of grey reeds + a stone or two, for the land cells
    on the mere's shore (and only there — the builder places them)."""
    a = np.zeros((16, 16, 4), np.int16)
    R = [(70, 78, 70), (104, 112, 98), (140, 146, 128)]
    blades = [(3, 14, 6), (5, 14, 9), (7, 14, 5), (10, 14, 8), (12, 14, 6)] if v == 0 else \
             [(2, 14, 7), (4, 14, 10), (8, 14, 6), (11, 14, 9), (13, 14, 5)]
    for (x, y, h) in blades:
        for k in range(h):
            xx = x + (1 if k > h * 0.6 and x % 2 else 0)
            a[y - k, xx] = list(R[1 if k < h - 2 else 2]) + [255]
            if k == 0:
                a[y, xx] = list(R[0]) + [255]
        a[y - h, x + (1 if x % 2 else 0)] = [168, 150, 112, 255]   # a seed-head
    a[15, 1:15] = [40, 46, 42, 120]                               # soft ground shadow
    return img(a)


# ---- THE CRAG'S FACE (2026-10, r2 review): `fogface` ------------------------------
# The coldfog_set `fogcrag` face is one tile tall (lip -> 8px face -> shadow), which on
# Stillwater's bowl of crags read as a flat blanket with battlement stubs. These two
# tiles stack into a TWO-tile face (level-design §11 r8, kept exactly: plateau top ->
# lit lip -> streaked face -> contact shadow -> drained ground), pinned by the builder
# over the crag's last two rows wherever the face runs at least three cells wide.
# Same CLIFF palette as fogcrag, so the 1-tile corners meet it cleanly.
CLIFF = gbaforge.CLIFF
FACE_ROWS = 24                       # the face, upper-tile row 6 to the toe (both tiles)
FACE_ROW0 = 6                        # f[0] sits on the upper tile's row 6
FACE_LIPS = (4, 5, 6)                # the lip's pixel row: varied so the rim never rules
# per-variant rock slabs: (crack columns, jog rows) — a crack jogs one pixel sideways
# at each jog row so it reads as split rock, never a ruled plank seam
FACE_CRACKS = [
    [(3, (6, 15)), (9, (3, 12, 19)), (13, (9, 17))],
    [(5, (4, 13, 20)), (11, (8, 16))],
    [(2, (10, 18)), (7, (5, 14)), (12, (2, 11, 20))],
]
# short ledges (x0, x1, face-row): a lit top pixel over a dark undercut
FACE_LEDGES = [
    [(4, 8, 7), (10, 13, 14), (1, 3, 19)],
    [(6, 10, 10), (12, 15, 4), (1, 4, 17)],
    [(3, 6, 12), (8, 11, 3), (13, 15, 18)],
]


def _face_px(v: int):
    """The whole two-tile face as one 16 x FACE_ROWS RGB array: lit high, dark at
    the toe; jogged cracks with a lamp-lit edge; short chipped ledges."""
    f = np.zeros((FACE_ROWS, 16, 3), dtype=np.int16)
    for y in range(FACE_ROWS):
        k = 0.86 - 0.24 * (y / (FACE_ROWS - 1))            # light falls off down the face
        f[y, :] = sh(CLIFF, k)
    for (x, jogs) in FACE_CRACKS[v % len(FACE_CRACKS)]:
        cx = x
        for y in range(FACE_ROWS):
            if y in jogs:
                cx = cx + (1 if (cx + y) % 2 else -1)
                cx = max(1, min(14, cx))
            k = 0.86 - 0.24 * (y / (FACE_ROWS - 1))
            f[y, cx] = sh(CLIFF, k * 0.66)
            f[y, cx + 1] = sh(CLIFF, min(1.2, k * 1.16), 4)
    for (x0, x1, y) in FACE_LEDGES[v % len(FACE_LEDGES)]:
        k = 0.86 - 0.24 * (y / (FACE_ROWS - 1))
        f[y, x0:x1] = sh(CLIFF, k * 1.26, 6)
        f[y + 1, x0:x1] = sh(CLIFF, k * 0.62)
    return f


def fogface_upper(v: int = 0, lip: int = 5):
    """The top half of a two-tile face: plateau top, the lit lip (at pixel row `lip`
    — the builder walks neighbours through 4/5/6 so the rim wanders), the face begins."""
    a = np.asarray(gbaforge.cliff_top(v).convert("RGBA")).astype(np.int16).copy()
    a[lip, :, :3] = sh(CLIFF, 1.40, 16)                     # lit lip
    a[lip + 1, :, :3] = sh(CLIFF, 1.08, 6)                  # the lip's rounded shoulder
    f = _face_px(v)
    a[lip + 2:16, :, :3] = f[lip + 2 - FACE_ROW0:16 - FACE_ROW0]
    return img(a)


def fogface_lower(v: int = 0):
    """The foot of a two-tile face: face runs on, darkens to its toe, contact shadow,
    then the drained ground below."""
    g = np.asarray(gbaforge.blight_fill(v).convert("RGBA")).astype(np.int16)
    a = np.asarray(gbaforge.cliff_top(v).convert("RGBA")).astype(np.int16).copy()
    f = _face_px(v)
    off = 16 - FACE_ROW0                                    # rows drawn by the upper tile
    a[0:12, :, :3] = f[off:off + 12]
    a[12, :, :3] = sh(CLIFF, 0.50)                          # the toe
    a[13, :, :3] = sh(CLIFF, 0.32)                          # contact shadow
    a[14:, :] = g[14:, :]
    for x in ((2 + 7 * v) % 15, (9 + 4 * v) % 15):          # a fallen chip at the foot
        a[14, x, :3] = sh(CLIFF, 0.80)
    return img(a)


# ---- COLDFOG I's DEAD POOLS (2026-10, r2 review): `murkpool` ----------------------
# The shared `murk` is a 9-slice with no inner corners, so every pool painted with it
# had to stay a convex box (the review's "filled rectangles"). This is the same dead
# water (gbaforge.MURK, no foam, no light) as a FULL family — inner corners, nubs,
# strips — with a deep shore bite (t=5) and wide rounded corners (r=5), so a pool can
# be any lobed blob. Mud-dark wet ground and a broken grey scum line, exactly the
# murk_edge register. Collision mirrors `murk` (water, Tidecall-swimmable, no zone).
POOL_T, POOL_R = 4, 7


def murkpool_tile(role: str, v: int = 0):
    fill = gbaforge.murk_fill(v)
    if role == "fill":
        return fill
    m = gbaforge.overlay_mask(role, POOL_T, POOL_R)          # True = land
    a = np.asarray(fill.convert("RGBA")).astype(np.int16).copy()
    o = np.asarray(gbaforge.blight_fill(v).convert("RGBA")).astype(np.int16)
    a[m] = o[m]
    water = ~m
    scum = gbaforge._dilate(m, 1) & water                     # water px touching land
    shallow = gbaforge._dilate(m, 2) & water & ~scum
    wet1 = gbaforge._dilate(water, 1) & m                     # land px touching water
    wet2 = gbaforge._dilate(water, 2) & m & ~wet1
    MURK = gbaforge.MURK
    a[shallow, :3] = sh(MURK, 1.30, 8)
    for (y, x) in zip(*np.where(scum)):
        a[y, x, :3] = sh(MURK, 1.08, 4) if (x + 2 * y) % 5 == 4 else (112, 120, 114)
    a[wet1, :3] = (np.clip(a[wet1, :3] * 0.62, 0, 255)).astype(np.int16)   # black mud
    a[wet2, :3] = (np.clip(a[wet2, :3] * 0.84, 0, 255)).astype(np.int16)   # damp
    return img(a)


def fogface_end(im, side: str, half: str):
    """A face tile at the run's west/east end: the outer two pixels give back to the
    drained ground behind a dark rim (the fogcrag corner_sw/se convention)."""
    a = np.asarray(im.convert("RGBA")).astype(np.int16).copy()
    g = np.asarray(gbaforge.blight_fill(1).convert("RGBA")).astype(np.int16)
    rows = slice(0, 16) if half == "lower" else slice(0, 16)
    if side == "w":
        a[rows, :2] = g[rows, :2]
        a[rows, 2, :3] = sh(CLIFF, 0.45)
        a[rows, 3, :3] = np.minimum(a[rows, 3, :3] + 14, 255)   # the rounded shoulder
    else:
        a[rows, 14:] = g[rows, 14:]
        a[rows, 13, :3] = sh(CLIFF, 0.45)
        a[rows, 12, :3] = (a[rows, 12, :3] * 0.85).astype(np.int16)
    if half == "lower":
        a[14:, :] = g[14:, :]                                    # the ground runs on below
    return img(a)


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im, autotile: str):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": "path", "terrain": "flagway",
                      "autotile": autotile, "collides": False})

    for role in ROLES:
        add(f"flagway_{role}", flagway_tile(role, 0), role)
    for v in (1, 2):
        add(f"flagway_fill_v{v}", flagway_tile("fill", v), "fill")

    # APPENDED (2026-10 fix pass) — the mere family, its jetty and its reeds.
    # Never insert above this line: the flagway gids are pinned in the map.
    def add_mere(name: str, im, autotile: str, **meta):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        t = {"file": fn, "role": "water", "terrain": "mere", "autotile": autotile,
             "collides": True, "requires_ability": "tidecall"}
        t.update(meta)
        tiles.append(t)

    for role in ROLES + ["end_n", "end_s", "end_w", "end_e", "single"]:
        add_mere(f"mere_{role}", mere_tile(role if role != "single" else "single", 0), role)
    for v in (1, 2):
        add_mere(f"mere_fill_v{v}", mere_tile("fill", v), "fill")
    for name, im in [("mere_jetty_root", jetty_tile(mere_tile("edge_s", 0))),
                     ("mere_jetty", jetty_tile(mere_fill(1))),
                     ("mere_jetty_end", jetty_tile(mere_fill(2), end=True))]:
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": "path", "terrain": "jetty", "collides": False})
    for v in (0, 1):
        name = f"mere_reeds_{'ab'[v]}"
        fn = f"{len(tiles):03d}_{name}.png"
        mere_reeds(v).save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": "deco", "collides": False})

    # APPENDED (2026-10, r2 review) — the crag's two-tile face (pinned, not autotiled):
    # three crack layouts (c0-c2), each upper in three lip heights (l4-l6).
    def add_face(name: str, im):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": "cliff", "terrain": "fogcrag", "collides": True})

    for v in (0, 1, 2):
        for lip in FACE_LIPS:
            add_face(f"fogface_upper_c{v}_l{lip}", fogface_upper(v, lip))
        add_face(f"fogface_lower_c{v}", fogface_lower(v))
    # the face's two ends: the crag's west/east side turns back into the drained ground
    for side in ("w", "e"):
        for half, fn_ in (("upper", fogface_upper), ("lower", fogface_lower)):
            add_face(f"fogface_{half}_{side}", fogface_end(fn_(1), side, half))

    # APPENDED (2026-10, r2 review) — Coldfog I's lobed dead pools (`murkpool`).
    for role in ROLES + ["end_n", "end_s", "end_w", "end_e", "single"]:
        add_mere(f"murkpool_{role}", murkpool_tile(role, 0), role, terrain="murkpool")
    add_mere("murkpool_fill_v1", murkpool_tile("fill", 1), "fill", terrain="murkpool")

    manifest = {"name": "stillwater_set", "columns": 6, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (REPO / "assets/tilesets/stillwater/stillwater_set.index.json").write_text(
        json.dumps(index, indent=2) + "\n")
    print(f"stillwater_set: {len(tiles)} tiles -> {TILES_DIR}")
    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
