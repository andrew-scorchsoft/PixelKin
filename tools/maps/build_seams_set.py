#!/usr/bin/env python3
"""
build_seams_set — the OLD SEAMS accent tileset (`seams_set`, 2026-10).

The Old Seams (docs/world/walkthrough/09-the-wild-ways.md §2 D) are the sealed
deep workings under Cinderhead. The shared overworld set is FROZEN, and the
traverse_set is shared by every Wild Ways lane, so the Seams' own surfaces live
in this accent set on the deepwater_set pattern: builders stack it with
`mk.register_tileset("seams_set", index=...)`, paint a terrain layer
`{"terrain": "shaft", "set": "seams_set"}` and pin the rest by name.

Drawn in code in gbaforge's GBA register (flat dusk anchors, 1px ink,
deliberate repeated motifs — never noise):

  shaft_<role>        an OPEN SHAFT (13 autotile roles + strips; collides): a
                      pit dropping into the dark. The far (north) lip shows the
                      shaft's back wall falling away; far below, the cinder
                      seams glow — three frames of slow breath on the fill (the
                      coal is Emberroot's breath, cinder law rule 5).
  cinder_0..2         cinder-coal floor: warm black stone with banked glints.
  scree_v_0/1         a cinder-scree SLOPE running N-S (a `kind:'slope'` flow
                      rides on these): loose black grit raked downhill.
  scree_h_0/1         ... running E-W.
  vein_a, vein_b      a glowing crack in the floor (decor overlay).
  srail_*             ore-cart rails on ballast, drawn on true pixel rings so
                      the quarter-turns read cleanly at 16px (the traverse_set
                      originals are rough): h, v, the four curves
                      (ne/nw/se/sw = the two edges the track reaches), the
                      eight junctions `tee_<h|v>_<curve>` (a straight with a
                      turnout peeling off it), and four buffer stops
                      `end_<side>` (the line runs in from the opposite side).

Writes:
  assets/tilesets/seams/set_tiles/*.png + tileset.manifest.json   (masters)
  public/assets/tilesets/seams_set.{webp,tileset.json}             (served)
  assets/tilesets/seams/seams_set.index.json                       (name->index)

Run:  python3 tools/maps/build_seams_set.py
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

import gbaforge
from gbaforge import sh, flat, put, img, CAVE

REPO = Path(__file__).resolve().parents[2]
BASE = REPO / "assets" / "tilesets" / "seams"
TILES_DIR = BASE / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

INK = (20, 16, 26)
COAL = (34, 30, 40)            # cinder-coal: warm black stone
EMBER = (214, 104, 46)         # a banked glint
EMBER_HOT = (250, 176, 92)
DEEP = (10, 8, 14)             # the shaft's bottomless dark
IRON = (92, 96, 110)
IRON_LT = (156, 162, 176)
IRON_DK = (58, 60, 72)
TIE = (96, 70, 48)
TIE_DK = (66, 48, 34)
BALLAST = (44, 40, 52)


def clear() -> np.ndarray:
    return np.zeros((16, 16, 4), dtype=np.int16)


def px(a, x, y, rgb, alpha=255):
    if 0 <= x < 16 and 0 <= y < 16:
        a[y, x, :3] = rgb
        a[y, x, 3] = alpha


def to_im(a) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# ---- the open shaft ----------------------------------------------------------
GLINT_SETS = [[(4, 5), (12, 11)], [(10, 3), (2, 12), (13, 14)], [(7, 13)]]


def shaft_fill(frame: int = 0, v: int = 0) -> Image.Image:
    """The pit: near-black with one faint far stratum and a few far-down cinder
    glints that breathe over three frames (sparse, so a wide shaft never reads
    as a dotted grid)."""
    a = flat(DEEP)
    put(a, [(1, 8), (2, 8), (6, 9), (7, 9), (8, 9), (13, 7), (14, 7)], sh(DEEP, 1.9, 4))
    for i, (x, y) in enumerate(GLINT_SETS[v % 3]):
        ph = (i + frame) % 3
        if ph == 0:
            put(a, [(x, y)], EMBER)
        elif ph == 1:
            put(a, [(x, y)], sh(EMBER, 0.45))
    return img(a)


def shaft_tile(role: str) -> Image.Image:
    """Shaft over cave floor. The floor (outer) keeps a lit lip all round;
    wherever the floor sits ABOVE the pit, the pit's back wall drops away below
    the lip — a 7px rock face fading into the dark (so a shaft reads as a HOLE,
    never as a raised black slab)."""
    floor = gbaforge.cavefloor_fill(0)
    mask = gbaforge.overlay_mask(role)                     # True = floor
    a = np.asarray(shaft_fill(0).convert("RGBA")).astype(np.int16).copy()
    o = np.asarray(floor.convert("RGBA")).astype(np.int16)
    a[mask] = o[mask]
    lip = sh(CAVE, 1.55, 18)
    face = [sh(CAVE, 1.05, 6), sh(CAVE, 0.94, 2), sh(CAVE, 0.82), sh(CAVE, 0.68),
            sh(CAVE, 0.54), sh(CAVE, 0.40), sh(CAVE, 0.26)]
    rim = np.zeros((16, 16), dtype=bool)
    for x in range(16):
        for y in range(16):
            if mask[y, x]:
                continue
            if y > 0 and mask[y - 1, x]:                   # floor above: the back wall
                for k, c in enumerate(face):
                    yy = y + k
                    if yy < 16 and not mask[yy, x]:
                        a[yy, x, :3] = c
                        if x % 6 == 2 and 1 <= k <= 4:
                            a[yy, x, :3] = sh(c, 0.72)     # streaks down the face
                rim[y - 1, x] = True
            for (nx, ny) in ((x - 1, y), (x + 1, y), (x, y + 1)):
                if 0 <= nx < 16 and 0 <= ny < 16 and mask[ny, nx]:
                    rim[ny, nx] = True                     # the floor's edge pixel
    a[rim, :3] = lip
    return img(a)


# ---- cinder floor + scree -------------------------------------------------------
CINDER_LAYOUTS = [
    [(3, 4), (11, 2), (7, 9), (13, 12), (2, 13)],
    [(5, 2), (12, 6), (2, 9), (9, 13), (14, 14)],
    [(8, 3), (3, 7), (12, 10), (6, 14), (14, 1)],
]


def cinder_fill(v: int = 0) -> Image.Image:
    """Walkable cinder-coal floor: warm black, chip clusters, a banked glint."""
    a = flat(COAL)
    chip = sh(COAL, 1.55, 10)
    dark = sh(COAL, 0.62)
    for i, (x, y) in enumerate(CINDER_LAYOUTS[v % 3]):
        put(a, [(x, y), (x + 1, y + 1)], dark)
        put(a, [(x + 1, y)], chip)
        if i == v % 5:
            put(a, [(x + 2, y + 1)], EMBER)
    return img(a)


def scree_v(v: int = 0) -> Image.Image:
    """Cinder scree raked downhill: loose grit streaks along the fall line, a
    few hot chips tumbling (the motion motif, as on the wax-road)."""
    a = flat(sh(COAL, 1.18, 6))
    streak = sh(COAL, 0.64)
    lit = sh(COAL, 1.75, 14)
    layout = ([(3, 1), (11, 4), (6, 9), (13, 11), (1, 12)],
              [(9, 0), (4, 5), (12, 8), (7, 12), (2, 3)])[v % 2]
    for (x, y) in layout:
        for k in range(4):
            put(a, [(x, y + k)], streak)
        put(a, [(x + 1, y + 3)], lit)                     # grit piling at the streak's foot
    put(a, [((5 + 7 * v) % 16, (13 + 5 * v) % 16)], EMBER)
    return img(a)


def scree_h(v: int = 0) -> Image.Image:
    return scree_v(v).rotate(-90, expand=False)


def vein(v: int = 0) -> Image.Image:
    """A glowing cinder crack across the floor (overlay)."""
    a = clear()
    path = ([(1, 9), (2, 9), (3, 8), (4, 8), (5, 8), (6, 7), (7, 7), (8, 8), (9, 8),
             (10, 9), (11, 9), (12, 8), (13, 7), (14, 7)],
            [(3, 2), (4, 3), (4, 4), (5, 5), (6, 6), (6, 7), (7, 8), (8, 9), (8, 10),
             (9, 11), (10, 12), (11, 13), (12, 13)])[v % 2]
    for i, (x, y) in enumerate(path):
        px(a, x, y, EMBER_HOT if i % 4 == 1 else EMBER)
        px(a, x, y + 1, sh(EMBER, 0.45), 200)              # the crack's shadow lip
    return to_im(a)


# ---- rails on true pixel rings ----------------------------------------------------
# Straight rails sit on columns 5-6 and 10-11 (lit, then shade) — the quarter-turns
# put those same rails on rings about the shared tile corner, so every joint meets.
def _straight(a, axis: str, lo: int = 0, hi: int = 16) -> None:
    for t in range(lo, hi):
        for c in range(3, 13):
            x, y = (c, t) if axis == "v" else (t, c)
            if a[y, x, 3] == 0:
                px(a, x, y, BALLAST, 150)
    for t in range(lo, hi):
        if (t - 1) % 4 in (0, 1):                          # sleepers every 4px
            for c in range(3, 13):
                x, y = (c, t) if axis == "v" else (t, c)
                px(a, x, y, TIE if (t - 1) % 4 == 0 else TIE_DK)
    for t in range(lo, hi):
        for c, col in ((5, IRON_LT), (6, IRON_DK), (10, IRON_LT), (11, IRON_DK)):
            x, y = (c, t) if axis == "v" else (t, c)
            px(a, x, y, col)


CORNER = {"ne": (16, 0), "nw": (0, 0), "se": (16, 16), "sw": (0, 16)}


def _curve(a, arms: str) -> None:
    """A quarter-turn joining the two edges in `arms` (ballast, radial ties,
    then the two rails as 1px-precise rings: lit outer half, shade inner)."""
    cx, cy = CORNER[arms]
    pts = [(x, y, math.hypot(x + 0.5 - cx, y + 0.5 - cy),
            math.atan2(abs(y + 0.5 - cy), abs(x + 0.5 - cx))) for y in range(16) for x in range(16)]
    for (x, y, d, th) in pts:
        if 3 <= d < 13 and a[y, x, 3] == 0:
            px(a, x, y, BALLAST, 150)
    for k in (15, 45, 75):
        tk = math.radians(k)
        for (x, y, d, th) in pts:
            if 3 <= d < 13 and abs(th - tk) * d < 1.05:
                px(a, x, y, TIE if th < tk else TIE_DK)
    for (x, y, d, th) in pts:
        for r0 in (4, 9):
            if r0 + 1 <= d < r0 + 2:
                px(a, x, y, IRON_LT)
            elif r0 <= d < r0 + 1:
                px(a, x, y, IRON_DK)


def rail_straight(axis: str) -> Image.Image:
    a = clear()
    _straight(a, axis)
    return to_im(a)


def rail_curve(arms: str) -> Image.Image:
    a = clear()
    _curve(a, arms)
    return to_im(a)


def rail_tee(axis: str, arms: str) -> Image.Image:
    """A junction: the straight line with a turnout `arms` peeling off it; the
    turnout is drawn over the straight so the point blades read."""
    a = clear()
    _straight(a, axis)
    _curve(a, arms)
    return to_im(a)


def rail_end(side: str) -> Image.Image:
    """A buffer stop: the line runs in from the opposite side, a timber beam
    with a red-painted face across the track at `side`, on platform floor."""
    a = clear()
    axis = "v" if side in "ns" else "h"
    lo, hi = {"n": (6, 16), "s": (0, 10), "w": (6, 16), "e": (0, 10)}[side]
    _straight(a, axis, lo, hi)
    beam = {"n": 5, "s": 10, "w": 5, "e": 10}[side]
    for c in range(2, 14):
        for k in (0, 1):
            t = beam + k if side in "ns" else beam + k
            x, y = (c, t) if axis == "v" else (t, c)
            px(a, x, y, (176, 64, 50) if k == (1 if side in "nw" else 0) else TIE_DK)
    for c in (2, 13):
        for k in range(-1, 3):
            t = beam + k
            x, y = (c, t) if axis == "v" else (t, c)
            px(a, x, y, TIE_DK)
    return to_im(a)


# ---- the first star (object, 4x4) -------------------------------------------------
STAR_OUT = REPO / "assets/tilesets/old_seams/objects/first_star.png"
ROCK = (58, 48, 54)
ROCK_LT = (104, 86, 82)
ROCK_DK = (32, 26, 32)


def first_star() -> Image.Image:
    """The first star that ever fell, as the mountain keeps it: a warm cracked
    orb half-sunk in a mound of root-rock, the roots running out across the
    floor with fire in their seams. 64x64 (4x4 tiles; maps give it overhang 2)."""
    S = 64
    a = np.zeros((S, S, 4), dtype=np.int16)

    def p(x, y, rgb, al=255):
        if 0 <= x < S and 0 <= y < S:
            a[y, x, :3] = rgb
            a[y, x, 3] = al

    cx, cy = 32, 30
    # a soft halo of warmth round the orb
    for y in range(S):
        for x in range(S):
            d = math.hypot(x - cx, (y - cy) * 1.1)
            if 13 <= d < 21 and (x + y) % 2 == 0:
                p(x, y, (214, 104, 46), int(110 * (21 - d) / 8))
    # the roots: thick tapering strokes out to the footprint's edges
    roots = [((32, 46), (2, 60)), ((32, 46), (62, 58)), ((26, 44), (0, 40)),
             ((38, 44), (63, 38)), ((30, 48), (20, 63)), ((36, 48), (46, 63))]
    for (x0, y0), (x1, y1) in roots:
        n = int(math.hypot(x1 - x0, y1 - y0))
        nx, ny = -(y1 - y0) / n, (x1 - x0) / n           # unit normal: roots wander
        for i in range(n + 1):
            t = i / n
            wob = 2.2 * math.sin(t * 6.0 + x1) * t
            x = round(x0 + (x1 - x0) * t + nx * wob)
            y = round(y0 + (y1 - y0) * t + ny * wob)
            r = 3.4 - 2.2 * t
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    if dx * dx + dy * dy <= r * r:
                        p(x + dx, y + dy, ROCK_LT if dy < -r / 2 else (ROCK if dy < r / 2 else ROCK_DK))
            if i % 7 in (2, 3) and t < 0.8:
                p(x, y, EMBER)                       # fire in the root's seam
    # the mound the orb sits in
    for y in range(S):
        for x in range(S):
            d = ((x - 32) / 21) ** 2 + ((y - 44) / 12) ** 2
            if d <= 1:
                c = ROCK_LT if y < 38 else (ROCK if d < 0.7 else ROCK_DK)
                h = ((x * 73856093) ^ (y * 19349663)) % 17
                if h == 0:
                    c = sh(ROCK_LT, 1.25, 8)               # lit knuckles of rock
                elif h in (5, 11) and y > 40:
                    c = ROCK_DK                            # cracks
                elif h == 3 and y > 42:
                    c = EMBER                              # the coal breathing in the mound
                if d > 0.86:
                    c = ROCK_DK                            # the mound's dark outline
                p(x, y, c)
    # the orb: white-hot heart, gold, ember rim; its lower third under the crust
    for y in range(S):
        for x in range(S):
            d = math.hypot(x - cx, y - cy)
            if d <= 12:
                k = d / 12
                c = ((255, 244, 214) if k < 0.3 else (252, 206, 120) if k < 0.6
                     else (244, 152, 72) if k < 0.85 else (196, 84, 40))
                p(x, y, c)
    for y in range(cy + 5, cy + 13):                 # the crust that holds it
        for x in range(cx - 12, cx + 13):
            if math.hypot(x - cx, y - cy) <= 12.5 and (y > cy + 7 or (x + y) % 3 == 0):
                p(x, y, ROCK if (x * 3 + y) % 5 else ROCK_LT)
    for (x0, y0, dx, dy, n) in [(26, 25, 1, 1, 6), (37, 23, -1, 1, 5), (30, 36, 1, 0, 6)]:
        for i in range(n):
            p(x0 + dx * i, y0 + dy * i, (255, 252, 236))  # light breaking through the cracks
    p(cx - 4, cy - 6, (255, 255, 255))
    p(cx - 3, cy - 6, (255, 255, 255))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


NINE = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
        "corner_sw", "edge_s", "corner_se"]
INNER = ["inner_nw", "inner_ne", "inner_sw", "inner_se"]
STRIPS = ["strip_h", "strip_v"]


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    for old in TILES_DIR.glob("*.png"):
        old.unlink()
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im, role: str, **extra):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": role, **extra})

    for r in NINE + INNER + STRIPS:
        add(f"shaft_{r}", shaft_fill(0) if r == "fill" else shaft_tile(r), "wall",
            collides=True, terrain="shaft", autotile=r)
    # two more fill variants (different glint layouts; the autotiler scatters
    # among same-role tiles) — each fill breathes over three frames
    for v in (1, 2):
        add(f"shaft_fill_v{v}", shaft_fill(0, v), "wall", collides=True,
            terrain="shaft", autotile="fill")
    for v in (0, 1, 2):
        name = "shaft_fill" if v == 0 else f"shaft_fill_v{v}"
        add(f"shaft_v{v}_a2", shaft_fill(1, v), "wall", collides=True)
        add(f"shaft_v{v}_a3", shaft_fill(2, v), "wall", collides=True)
        tiles[index[name]]["animation"] = {
            "frames": [index[name], index[f"shaft_v{v}_a2"], index[f"shaft_v{v}_a3"]],
            "duration_ms": 1400 + 200 * v}
    for v in range(3):
        add(f"cinder_{v}", cinder_fill(v), "ground")
    for v in (0, 1):
        add(f"scree_v_{v}", scree_v(v), "path")
    for v in (0, 1):
        add(f"scree_h_{v}", scree_h(v), "path")
    add("vein_a", vein(0), "decor")
    add("vein_b", vein(1), "decor")
    add("srail_h", rail_straight("h"), "decor")
    add("srail_v", rail_straight("v"), "decor")
    for arms in ("ne", "nw", "se", "sw"):
        add(f"srail_{arms}", rail_curve(arms), "decor")
    for axis in ("h", "v"):
        for arms in ("ne", "nw", "se", "sw"):
            add(f"srail_tee_{axis}_{arms}", rail_tee(axis, arms), "decor")
    for s in "nsew":
        add(f"srail_end_{s}", rail_end(s), "decor")

    first_star().save(STAR_OUT)
    print(f"object -> {STAR_OUT} (run pack_objects.py)")

    manifest = {"name": "seams_set", "columns": 8, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (BASE / "seams_set.index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"seams_set: {len(tiles)} tiles -> {TILES_DIR}")
    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
