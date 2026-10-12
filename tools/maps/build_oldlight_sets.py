#!/usr/bin/env python3
"""
build_oldlight_sets — the seven WARPED interior tilesets of the Old Light,
Mr. Punchwheel's joke tower (one per floor; the furniture is oldlightforge.py).

Each floor's set is a pixel transform of an existing interior kit with the
IDENTICAL tile order, count (55, 8 columns) and per-tile metadata, so a map
swaps `interior_set` / `interior_stone_set` for `oldlight_fN_set` with zero
gid changes (roomkit's FLOOR / FACE / band blob / face-end indices all hold).
The tower gets stranger the higher you climb:

  f1  warm   almost normal: a warm stage-light tint, confetti specks on the floor
  f2  cool   cooler, dimmer, every floor pattern trailing a faint "late" ghost
  f3  warm   the interval bar: candy-striped carpet with a slight wobble
  f4  cool   BACKWARDS: the whole wall system mirrored, palette turned inside out
  f5  cool   the gallery: a checker floor bent by a confident sinusoidal lie,
             gilded lips and cornice
  f6  warm   melancholy: desaturated, the floor lines sagging
  f7  warm   full derangement: pinwheel-swirled floors, hue-rotated walls,
             wobbling wall bands

Readability is binding (collision is unchanged): every band/face tile stays
DARKER and more structured than every floor tile, so a wall still reads as a
wall and a floor as walk-on ground. Floor fills stay seamless — every floor
transform is periodic on the 16px tile (or leaves the tile's edge ring alone),
and FLOOR / FLOOR_B share the same pattern phase.

Reads   public/assets/tilesets/interior_set.webp | interior_stone_set.webp (+ sidecars)
Writes  assets/tilesets/oldlight/sets/oldlight_fN_set.png         (master)
        public/assets/tilesets/oldlight_fN_set.webp               (lossless, served)
        public/assets/tilesets/oldlight_fN_set.tileset.json       (source sidecar,
                                                                    name/image changed)
Deterministic; re-run freely.

Run:  python3 tools/maps/build_oldlight_sets.py [--only 1,4,7]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roomkit as rk  # noqa: E402  (the shared tile order)

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "public" / "assets" / "tilesets"
MASTERS = REPO / "assets" / "tilesets" / "oldlight" / "sets"
T, COLS = 16, 8

# ---- tile classes (local index = gid - 1) ------------------------------------
FLOORS = (rk.FLOOR - 1, rk.FLOOR_B - 1)            # 0, 1
MAT = rk.DOORMAT - 1                                # 2 (doormat / cool runner)
FACE = rk.FACE - 1                                  # 3
INSET = rk.WINDOW - 1                               # 4 (window / cool banner)
FACE_ENDS = (rk.FACE_END_W - 1, rk.FACE_END_E - 1, rk.FACE_END_EW - 1)
FACES = (FACE,) + FACE_ENDS
BANDS = tuple(sorted(g - 1 for g in rk.BAND_GIDS))
N = rk.TILE_COUNT                                   # 55


# ---- io ------------------------------------------------------------------------
def load(name: str) -> tuple[list[np.ndarray], dict]:
    im = np.asarray(Image.open(SRC / f"{name}.webp").convert("RGBA")).astype(np.float64)
    tiles = []
    for i in range((im.shape[0] // T) * COLS):
        r, c = divmod(i, COLS)
        tiles.append(im[r * T:(r + 1) * T, c * T:(c + 1) * T].copy())
    side = json.loads((SRC / f"{name}.tileset.json").read_text())
    assert side["tile_count"] == N and side["columns"] == COLS, name
    return tiles, side


def assemble(tiles: list[np.ndarray]) -> Image.Image:
    rows = (len(tiles) + COLS - 1) // COLS
    out = np.zeros((rows * T, COLS * T, 4), np.float64)
    for i, t in enumerate(tiles):
        r, c = divmod(i, COLS)
        out[r * T:(r + 1) * T, c * T:(c + 1) * T] = t
    return Image.fromarray(np.clip(np.rint(out), 0, 255).astype(np.uint8), "RGBA")


# ---- colour helpers (operate on HxWx4 float arrays, alpha untouched) ------------
def lum(t):
    return 0.299 * t[..., 0] + 0.587 * t[..., 1] + 0.114 * t[..., 2]


def mul(t, r, g, b, add=(0, 0, 0)):
    o = t.copy()
    o[..., 0] = t[..., 0] * r + add[0]
    o[..., 1] = t[..., 1] * g + add[1]
    o[..., 2] = t[..., 2] * b + add[2]
    o[..., :3] = np.clip(o[..., :3], 0, 255)
    return o


def saturate(t, k):
    """k < 1 desaturates toward luminance, k > 1 boosts."""
    o = t.copy()
    L = lum(t)[..., None]
    o[..., :3] = np.clip(L + (t[..., :3] - L) * k, 0, 255)
    return o


def hue_rotate(t, deg, keep_lum=True):
    """Rotate hue about the grey axis (YIQ rotation) — luminance preserved, so
    a dark wall stays a dark wall whatever colour it turns."""
    th = math.radians(deg)
    c, s = math.cos(th), math.sin(th)
    rgb2yiq = np.array([[0.299, 0.587, 0.114], [0.596, -0.274, -0.322], [0.211, -0.523, 0.312]])
    yiq2rgb = np.linalg.inv(rgb2yiq)
    rot = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    m = yiq2rgb @ rot @ rgb2yiq
    o = t.copy()
    o[..., :3] = np.clip(t[..., :3] @ m.T, 0, 255)
    return o


def mix(a, b, k):
    o = a.copy()
    o[..., :3] = a[..., :3] * (1 - k) + b[..., :3] * k
    return o


def rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float64)


def paint(t, x, y, col, k=1.0):
    t[y, x, :3] = t[y, x, :3] * (1 - k) + col * k


def textured(t, col_a, col_b, pick, strength=0.55):
    """Recolour a floor with a two-colour pattern `pick(x, y) -> bool` while
    keeping the source's grain: each pixel takes its colour's value, shifted
    by the source pixel's deviation from the tile's mean luminance."""
    L = lum(t)
    dev = (L - L.mean())[..., None] * strength
    o = t.copy()
    for y in range(T):
        for x in range(T):
            base = col_a if pick(x, y) else col_b
            o[y, x, :3] = np.clip(base + dev[y, x], 0, 255)
    return o


def remap(t, fn):
    """Inverse-map warp within ONE tile: out(x, y) = src(fn(x, y)), wrapped
    toroidally (so a periodic fn keeps the tile seamless)."""
    o = t.copy()
    for y in range(T):
        for x in range(T):
            sx, sy = fn(x, y)
            o[y, x] = t[int(round(sy)) % T, int(round(sx)) % T]
    return o


# ---- the seven floors ------------------------------------------------------------
CONFETTI = [rgb("#e0483e"), rgb("#f6e6b8"), rgb("#4a8ad8"), rgb("#f0c838"), rgb("#58b868")]


def f1(src):
    """Almost normal: a warm stage-light tint + confetti specks on the floors."""
    out = [mul(t, 1.07, 1.0, 0.88, add=(10, 5, 0)) for t in src]
    rng = np.random.default_rng(101)
    for k, i in enumerate(FLOORS):
        t = out[i]
        for j in range(5):
            x, y = (int(v) for v in rng.integers(2, 14, size=2))
            col = CONFETTI[(j + 2 * k) % len(CONFETTI)]
            paint(t, x, y, col, 0.85)
            if j % 2:
                paint(t, x + 1, y, col, 0.85)
    return out


def f2(src):
    """Cooler, dimmer, and every pattern runs a little late: a ghost of itself
    trails two pixels behind on the floors and the banner."""
    out = [mul(t, 0.8, 0.88, 1.04) for t in src]
    for i in FLOORS:
        out[i] = mul(src[i], 0.92, 0.98, 1.1, add=(0, 2, 6))
    for i in FLOORS + (MAT,):
        t = out[i]
        ghost = np.roll(np.roll(t, 2, axis=0), 3, axis=1)   # toroidal: stays seamless
        out[i] = mix(t, mul(ghost, 0.8, 0.85, 1.05), 0.42)
    t = out[INSET]
    gh = np.roll(t, 2, axis=1)
    out[INSET] = mix(t, gh, 0.35)
    return out


def f3(src):
    """The interval bar: wine-and-cream candy-striped carpet, wobbling a
    pixel either way; the walls cosy and warm."""
    out = [mul(t, 1.06, 0.96, 0.86, add=(6, 0, 0)) for t in src]
    wine, cream = rgb("#9a3a44"), rgb("#e6c69a")
    def stripe(x, y):
        wob = round(1.2 * math.sin(2 * math.pi * y / 16))
        return ((x + wob + 2) % 8) < 4
    for i in FLOORS:
        out[i] = textured(out[i], wine, cream, stripe, strength=0.5)
        # a thin gold pin-stripe on the seam of each band
        for y in range(T):
            wob = round(1.2 * math.sin(2 * math.pi * y / 16))
            paint(out[i], (6 - wob) % T, y, rgb("#f0c060"), 0.55)
            paint(out[i], (14 - wob) % T, y, rgb("#f0c060"), 0.55)
    return out


_MIRROR = {"e": "w", "w": "e", "ne": "nw", "nw": "ne", "se": "sw", "sw": "se", "n": "n", "s": "s"}


def f4(src):
    """Backwards: the whole wall system mirrored left-for-right (each band
    tile becomes the flipped twin of its mirror shape, so the lips still meet
    the floor on the correct side), the faces and floors flipped, and the
    palette turned inside out — hues spun half-way round at the same value."""
    out = [t.copy() for t in src]
    by_shape = {(s, b): g - 1 for (s, b), g in rk.BAND_GID.items()}
    for (sides, nubs), idx in by_shape.items():
        ms = frozenset(_MIRROR[d] for d in sides)
        mn = frozenset(_MIRROR[c] for c in nubs)
        out[idx] = src[by_shape[(ms, mn)]][:, ::-1].copy()
    w, e, ew = FACE_ENDS
    out[w], out[e], out[ew] = src[e][:, ::-1].copy(), src[w][:, ::-1].copy(), src[ew][:, ::-1].copy()
    for i in FLOORS + (MAT, FACE, INSET):
        out[i] = src[i][:, ::-1].copy()
    out = [hue_rotate(t, 180) for t in out]
    out = [saturate(t, 1.5) for t in out]
    for i in FLOORS:
        # the floor's grain inverted (light knots go dark) about its own mean
        t = out[i]
        L = lum(t)[..., None]
        m = L.mean()
        t[..., :3] = np.clip(t[..., :3] - 1.4 * (L - m), 0, 255)
        out[i] = mul(t, 1.08, 1.04, 1.0)
    return out


def f5(src):
    """The gallery: a polished checker floor bent by a sinusoidal 'confident
    lie' (periodic on the tile, so it still tiles), gilded wall lips and a
    gold cornice line along the face."""
    out = [mul(t, 0.95, 0.95, 1.0) for t in src]
    ivory, slate = rgb("#e8dcc0"), rgb("#3c4058")
    def check(x, y):
        wx = x + 4 + 1.6 * math.sin(2 * math.pi * y / 16)
        wy = y + 4 + 1.6 * math.sin(2 * math.pi * x / 16 + 1.0)
        return (int(math.floor(wx / 8)) + int(math.floor(wy / 8))) % 2 == 0
    for i in FLOORS:
        out[i] = textured(out[i], ivory, slate, check, strength=0.35)
        # a gilt fleck at each warped crossing
        for (x, y) in ((4, 4), (12, 12)):
            paint(out[i], x, y, rgb("#f0c860"), 0.6)
    gold = [rgb("#5a431c"), rgb("#b98a2e"), rgb("#e8c060"), rgb("#fff0a8")]
    for i in BANDS:
        t = out[i]
        L = lum(t)
        hi = L > 95                     # the lit lip (the band body is dark)
        for y, x in zip(*np.nonzero(hi)):
            g = gold[min(3, int((L[y, x] - 95) / 30) + 1)]
            t[y, x, :3] = g
    for i in FACES + (INSET,):
        t = out[i]
        t[1, :, :3] = rgb("#e8c060")
        t[2, :, :3] = rgb("#7a5a20")
        # the banner/window inset gets a gold edge too
    return out


def f6(src):
    """Melancholy: the colour drained to a blue-grey, everything a shade
    dimmer, and the floor's lines sagging in the middle of every board."""
    out = [mul(saturate(t, 0.3), 0.84, 0.88, 0.98) for t in src]
    for i in FACES + (INSET,):
        out[i] = mul(out[i], 0.78, 0.82, 0.92)
    for i in FLOORS:
        t = out[i]
        for base in (2, 10):
            for x in range(T):
                y = base + round(3.0 * math.sin(math.pi * x / 15))
                t[y % T, x, :3] *= 0.6
                t[(y + 1) % T, x, :3] = np.clip(t[(y + 1) % T, x, :3] * 1.12, 0, 255)
    for i in FACES:
        # the wainscot droops too: a faint sagging shadow under the cornice
        t = out[i]
        for x in range(T):
            y = 4 + round(1.5 * math.sin(math.pi * (x % 16) / 15))
            t[y, x, :3] *= 0.86
    return out


def f7(src):
    """Full derangement: every floor tile a pinwheel swirled about its centre
    (the edge ring untouched, so it still tiles), walls hue-rotated and the
    wall bands wobbling — but bands stay dark and floors stay light."""
    out = [t.copy() for t in src]
    teal, plum, lemon = rgb("#3ab0a0"), rgb("#b04a9a"), rgb("#f0d860")
    for k, i in enumerate(FLOORS):
        t = out[i]
        cx = cy = 7.5
        # a pinwheel of sectors, then a swirl that winds them into a spiral
        def sector(x, y, k=k):
            a = math.atan2(y - cy, x - cx) + (math.pi / 4 if k else 0)
            return int(math.floor(a / (math.pi / 3))) % 2 == 0
        L = lum(t)
        dev = (L - L.mean())[..., None] * 0.4
        pin = t.copy()
        for y in range(T):
            for x in range(T):
                r = math.hypot(x - cx, y - cy)
                if r < 7.0:
                    base = teal if sector(x, y) else plum
                    if r < 1.6:
                        base = lemon
                    pin[y, x, :3] = np.clip(base + dev[y, x], 0, 255)
        def swirl(x, y):
            dx, dy = x - cx, y - cy
            r = math.hypot(dx, dy)
            if r >= 7.4:
                return x, y
            th = 2.4 * (1 - r / 7.4) ** 2
            c, s = math.cos(th), math.sin(th)
            return cx + dx * c - dy * s, cy + dx * s + dy * c
        sw = remap(pin, swirl)
        # lighten the whole floor so it never reads as wall
        out[i] = mul(sw, 1.12, 1.1, 1.1, add=(12, 12, 12))
    for i in BANDS:
        t = hue_rotate(out[i], 150)
        t = saturate(t, 1.8)
        # wobble: each column slides up or down a pixel (edge rows clamp)
        w = t.copy()
        for x in range(T):
            d = round(1.0 * math.sin(2 * math.pi * x / 16))
            for y in range(T):
                w[y, x] = t[min(T - 1, max(0, y - d)), x]
        out[i] = w
    for i in FACES + (INSET,):
        t = hue_rotate(out[i], 290)
        out[i] = saturate(t, 2.2)
    out[MAT] = saturate(hue_rotate(out[MAT], 200), 1.6)
    return out


FLOOR_SPECS = {
    1: ("interior_set", f1), 2: ("interior_stone_set", f2), 3: ("interior_set", f3),
    4: ("interior_stone_set", f4), 5: ("interior_stone_set", f5),
    6: ("interior_set", f6), 7: ("interior_set", f7),
}


def readability(tiles, n):
    """Binding guard: the brightest wall-top band must stay darker than the
    darkest floor fill (the face keeps its own structure)."""
    band = max(lum(tiles[i])[tiles[i][..., 3] > 0].mean() for i in BANDS)
    floor = min(lum(tiles[i]).mean() for i in FLOORS)
    assert band + 15 < floor, f"f{n}: walls ({band:.0f}) too close to floors ({floor:.0f})"
    return band, floor


def seam_score(t):
    """How loud the tile's wrap seam is next to its own interior: the mean
    step across the toroidal edge over the mean step between interior
    neighbours. ~1 or below = no visible grid when the fill is tiled."""
    c = t[..., :3]
    edge = (np.abs(c[0] - c[-1]).mean() + np.abs(c[:, 0] - c[:, -1]).mean()) / 2
    inner = (np.abs(np.diff(c, axis=0)).mean() + np.abs(np.diff(c, axis=1)).mean()) / 2
    return float(edge / max(inner, 1e-6))


def build(n: int) -> None:
    src_name, fn = FLOOR_SPECS[n]
    src, side = load(src_name)
    tiles = fn(src)
    assert len(tiles) == len(src)
    # alpha is never touched; the unused 56th slot stays clear
    for a, b in zip(tiles, src):
        a[..., 3] = b[..., 3]
        a[a[..., 3] == 0] = 0          # clear pixels carry no colour (WebP drops it)
    band, floor = readability(tiles, n)
    name = f"oldlight_f{n}_set"
    im = assemble(tiles)
    MASTERS.mkdir(parents=True, exist_ok=True)
    im.save(MASTERS / f"{name}.png")
    out = SRC / f"{name}.webp"
    im.save(out, "WEBP", lossless=True, quality=100, method=6)
    back = np.asarray(Image.open(out).convert("RGBA"))
    assert (back == np.asarray(im)).all(), f"{name}: WebP not lossless"
    side = dict(side)
    side["name"] = name
    side["image"] = f"assets/tilesets/{name}.webp"
    (SRC / f"{name}.tileset.json").write_text(json.dumps(side, indent=2) + "\n")
    seams = " ".join(f"{seam_score(tiles[i]):.2f}" for i in FLOORS)
    assert all(seam_score(tiles[i]) < 1.6 for i in FLOORS), f"{name}: a floor fill shows its seam"
    print(f"  {name}  <- {src_name}   band lum {band:.0f} < floor lum {floor:.0f}"
          f"   floor seam ratio {seams}")


def main() -> None:
    only = None
    if "--only" in sys.argv:
        only = {int(v) for v in sys.argv[sys.argv.index("--only") + 1].split(",")}
    for n in FLOOR_SPECS:
        if only is None or n in only:
            build(n)


if __name__ == "__main__":
    main()
