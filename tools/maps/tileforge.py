#!/usr/bin/env python3
"""
tileforge — reusable 16×16 tile-seam helpers (the rim/seam cure, importable).

The model bakes a 1px ink rim + a vignette into every generated tile; tiled, that
rim becomes the grid. These helpers turn a raw tile into a seamless autotile piece:

  deborder(im, role)  strip the rim on every side EXCEPT the designed transition
                      side(s) for that autotile role, then seam the tiling axis.
  jitter / roll       cheap deterministic VARIANTS (value-jitter a fill, phase-roll
                      an edge) so a role doesn't stamp one tile across a whole run.

Both the shared-set builder and any area/biome builder import these — so the cure
lives in one place. Pure functions, no side effects (safe to import).
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image

# Sides each autotile role keeps as a DESIGNED transition (everything else is rim).
KEEP = {
    "edge_n": {"N"}, "edge_s": {"S"}, "edge_w": {"W"}, "edge_e": {"E"},
    "corner_nw": {"N", "W"}, "corner_ne": {"N", "E"},
    "corner_se": {"S", "E"}, "corner_sw": {"S", "W"},
    "strip_h": {"N", "S"}, "strip_v": {"E", "W"}, "fill": set(),
}
H_TILE = {"edge_n", "edge_s", "strip_h", "fill"}   # repeats left↔right
V_TILE = {"edge_w", "edge_e", "strip_v", "fill"}   # repeats top↔bottom


def load(p: Path | str) -> Image.Image:
    """16×16 RGBA; only resample (NEAREST) if not already 16×16 — a same-size
    LANCZOS pass softens crisp edges and can reintroduce a faint rim."""
    im = Image.open(p).convert("RGBA")
    return im if im.size == (16, 16) else im.resize((16, 16), Image.NEAREST)


def _img(a: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def deborder(im: Image.Image, role: str) -> Image.Image:
    """Strip the baked rim on non-transition sides, then seam the tiling axis."""
    a = np.asarray(im.convert("RGBA")).astype(np.int16).copy()
    keep = KEEP.get(role, set())
    if "N" not in keep: a[0, :, :] = a[1, :, :]
    if "S" not in keep: a[-1, :, :] = a[-2, :, :]
    if "W" not in keep: a[:, 0, :] = a[:, 1, :]
    if "E" not in keep: a[:, -1, :] = a[:, -2, :]
    if role in H_TILE:
        m = (a[:, 0, :] + a[:, -1, :]) // 2
        a[:, 0, :] = m; a[:, -1, :] = m
    if role in V_TILE:
        m = (a[0, :, :] + a[-1, :, :]) // 2
        a[0, :, :] = m; a[-1, :, :] = m
    return _img(a)


def jitter(im: Image.Image, seed: int, amt: int = 9) -> Image.Image:
    """Per-pixel value jitter on opaque pixels — a different-but-same fill variant."""
    a = np.asarray(im.convert("RGBA")).astype(np.int16).copy()
    noise = np.random.default_rng(seed).integers(-amt, amt + 1, size=a.shape[:2])
    for c in range(3):
        a[..., c] = a[..., c] + noise
    return _img(a)


def roll(im: Image.Image, dx: int = 0, dy: int = 0) -> Image.Image:
    """Phase-shift the texture (e.g. move a foam crest along a shore) → edge variant.
    Roll a DEBORDERED (toroidal) tile so the shift stays seamless."""
    a = np.asarray(im.convert("RGBA"))
    return Image.fromarray(np.roll(np.roll(a, dx, axis=1), dy, axis=0))


def flip_h(im: Image.Image) -> Image.Image:
    return im.transpose(Image.FLIP_LEFT_RIGHT)


def whole_downscale(src_path: Path | str, role: str = "fill") -> Image.Image:
    """The fill cure: downscale a LARGE continuous swatch to 16px (averages out any
    residual vignette), then deborder. Use on a flat-lit full-bleed field render."""
    big = Image.open(src_path).convert("RGBA")
    return deborder(big.resize((16, 16), Image.LANCZOS), role)


# ---------------------------------------------------------------------------
# Texture & vocabulary helpers (the "composition standard" kit — level-design §11)
# Deterministic pixel passes that lift a flat family to the handheld bar without
# an API call: blade texture on ground fills, readable tall-grass tufts, cliff
# value lift + strata, highlight de-glow, 13-piece inner corners, and the small
# drawn props (fence/boulder/flowerbed) every decorated map needs.
# ---------------------------------------------------------------------------

def _arr(im: Image.Image) -> np.ndarray:
    return np.asarray(im.convert("RGBA")).astype(np.int16).copy()


def _hex(h: str) -> list[int]:
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)] + [255]


def grade(im: Image.Image, mul: float = 1.0, add: int = 0) -> Image.Image:
    """Flat value grade (multiply + offset) on RGB — the cliff-face lift."""
    a = _arr(im)
    a[..., :3] = np.clip(a[..., :3] * mul + add, 0, 255)
    return _img(a)


def flatten_vignette(im: Image.Image, radius: int = 3, strength: float = 1.0) -> Image.Image:
    """Remove the per-tile low-frequency gradient (the baked vignette) that turns a
    tiled fill into a visible grid: high-pass the tile against a TOROIDAL box blur,
    then restore the original mean. Detail survives; the lighting bow does not.
    This is the joints cure for fills — deborder only fixes the outer ring."""
    a = _arr(im)
    rgb = a[..., :3].astype(np.float64)
    lp = np.zeros_like(rgb)
    n = 0
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            lp += np.roll(np.roll(rgb, dy, axis=0), dx, axis=1)
            n += 1
    lp /= n
    mean = rgb.reshape(-1, 3).mean(0)
    flat = rgb - strength * (lp - mean)
    a[..., :3] = np.clip(flat, 0, 255)
    return _img(a)


def flatten_axis(im: Image.Image, axis: str, radius: int = 3) -> Image.Image:
    """flatten_vignette restricted to ONE axis — the joints cure for EDGE tiles.
    An edge tile keeps a designed gradient ACROSS the transition, but along its
    tiling axis the lighting must be flat or repeats show joints. axis='h' for
    tiles that repeat left-right (edge_n/s, strip_h): flattens the per-COLUMN
    mean profile (toroidal); axis='v' for top-bottom repeats (edge_w/e, strip_v)."""
    a = _arr(im)
    rgb = a[..., :3].astype(np.float64)
    ax = 1 if axis == "h" else 0
    prof = rgb.mean(axis=1 - ax)                       # (16, 3) per-col or per-row means
    lp = np.zeros_like(prof)
    for d in range(-radius, radius + 1):
        lp += np.roll(prof, d, axis=0)
    lp /= (2 * radius + 1)
    corr = prof - lp                                   # the lighting bow along the axis
    if ax == 1:
        rgb -= corr[np.newaxis, :, :]
    else:
        rgb -= corr[:, np.newaxis, :]
    a[..., :3] = np.clip(rgb, 0, 255)
    return _img(a)


def flip_v(im: Image.Image) -> Image.Image:
    return im.transpose(Image.FLIP_TOP_BOTTOM)


def key_alpha(im: Image.Image, rgb=(255, 255, 255), tol: int = 28) -> Image.Image:
    """Key a baked background colour to transparency (e.g. a prop generated on an
    opaque white card — the 'white bag' look when stamped on grass)."""
    a = _arr(im)
    d = np.abs(a[..., :3] - np.array(rgb, dtype=np.int16)).sum(-1)
    a[..., 3] = np.where(d <= tol * 3, 0, a[..., 3])
    return _img(a)


def deglow(im: Image.Image, thresh: int = 190, k: float = 0.55) -> Image.Image:
    """Compress highlights above `thresh` — kills the baked luminous rim that
    image-gen leaves on pale materials (sand) without touching the body."""
    a = _arr(im)
    lum = a[..., :3].mean(-1, keepdims=True)
    a[..., :3] = np.clip(a[..., :3] - np.maximum(0, lum - thresh) * k, 0, 255)
    return _img(a)


def texture_grass(base: Image.Image, seed: int, density: int = 7) -> Image.Image:
    """Sparse 2-px blade dashes (dark + occasional light) over a flat ground fill —
    the difference between 'untextured void' and 'grass'. Toroidal-safe."""
    a = _arr(base)
    mean = a[..., :3].reshape(-1, 3).mean(0)
    dark = np.clip(mean * 0.82, 0, 255).astype(int)
    light = np.clip(mean * 1.16 + 6, 0, 255).astype(int)
    rng = np.random.default_rng(seed)
    for _ in range(density):
        x, y = int(rng.integers(0, 16)), int(rng.integers(0, 16))
        a[y, x, :3] = dark
        a[(y - 1) % 16, x, :3] = dark if rng.random() < 0.5 else light
    for _ in range(2):
        x, y = int(rng.integers(0, 16)), int(rng.integers(0, 16))
        a[y, x, :3] = light
    return _img(a)


def tallgrass_tuft(base: Image.Image, phase: int = 0) -> Image.Image:
    """The readable encounter tile: staggered blade-fan clumps over a darkened bed,
    colours derived from the ground so the dusk hue holds. Hard-edged by design —
    classic handheld tall grass has NO transition ring; ship fill(+variants) only."""
    a = _arr(base)
    a[..., :3] = (a[..., :3] * 0.74).astype(int)
    mean = a[..., :3].reshape(-1, 3).mean(0)
    out = np.clip(mean * 0.40, 0, 255).astype(int)
    mid = np.clip(mean * 1.65 + 8, 0, 255).astype(int)
    light = np.clip(mean * 2.15 + 18, 0, 255).astype(int)

    def clump(cx, cy):
        for (x, y) in [(cx, cy), (cx, cy - 1), (cx - 1, cy), (cx + 1, cy),
                       (cx - 2, cy + 1), (cx + 2, cy + 1), (cx - 1, cy - 2), (cx + 1, cy - 2)]:
            a[y % 16, x % 16, :3] = mid
        for (x, y) in [(cx, cy - 3), (cx - 2, cy - 1), (cx + 2, cy - 1)]:
            a[y % 16, x % 16, :3] = light
        for (x, y) in [(cx - 1, cy + 2), (cx, cy + 2), (cx + 1, cy + 2)]:
            a[y % 16, x % 16, :3] = out

    rng = np.random.default_rng(97 + phase)
    for (cx, cy) in ((4, 5), (12, 5), (8, 12), (0, 12)):
        jx, jy = int(rng.integers(-2, 3)), int(rng.integers(-1, 2))
        clump((cx + jx) % 16, cy + jy)
    return _img(a)


def match_green_to(im: Image.Image, target_rgb, min_greenness: int = 14) -> Image.Image:
    """Selectively recolor green-dominant pixels (the baked daylight-green grass
    border many generated transition tiles carry) toward OUR ground tone,
    preserving each pixel's relative shading. The cure for edge tiles whose
    grass side glows lime against the dusk-teal field."""
    a = _arr(im)
    rgb = a[..., :3].astype(np.float64)
    greenness = rgb[..., 1] - (rgb[..., 0] + rgb[..., 2]) / 2
    mask = greenness > min_greenness
    if mask.any():
        t = np.array(target_rgb, dtype=np.float64)
        lum = rgb.mean(-1, keepdims=True)
        src_lum = rgb[mask].mean()
        shaded = t[np.newaxis, np.newaxis, :] * (lum / max(src_lum, 1.0))
        out = np.where(mask[..., np.newaxis], 0.15 * rgb + 0.85 * shaded, rgb)
        a[..., :3] = np.clip(out, 0, 255)
    return _img(a)


def cliff_strata(im: Image.Image, seed: int = 3) -> Image.Image:
    """Two darker strata seams + a lit chip line above each — makes a lifted rock
    face read as stratified stone instead of amplified noise."""
    a = _arr(im)
    rng = np.random.default_rng(seed)
    for sy in (5, 11):
        y = (sy + int(rng.integers(-1, 2))) % 16
        a[y, :, :3] = (a[y, :, :3] * 0.78).astype(int)
        a[(y - 1) % 16, :, :3] = np.clip(a[(y - 1) % 16, :, :3] * 1.08 + 3, 0, 255)
    return _img(a)


def cliff_wall_edge(face: Image.Image, ground_rgb, side: str) -> Image.Image:
    """A complete top-down cliff WALL tile for a mass boundary: lit rim at the top
    of the face, rock body, dark contact seam, then ground. `side` is the open
    direction ('s' = the classic south face; 'w'/'e' = side walls). This is what
    makes a rock mass read as HEIGHT instead of a texture slab (art-style §14)."""
    a = _arr(face)
    g = np.array(list(ground_rgb) + [255], dtype=np.int16)

    def lit(row):
        a[row, :, :3] = np.clip(a[row, :, :3] * 1.45 + 14, 0, 255)

    def dark(row):
        a[row, :, :3] = (a[row, :, :3] * 0.45).astype(int)

    if side == "s":
        lit(0); lit(1)
        dark(13)
        a[14, :] = g; a[15, :] = g
    elif side == "w":
        a[:, 0] = g; a[:, 1] = g
        a[:, 2, :3] = (a[:, 2, :3] * 0.45).astype(int)
        a[:, 3, :3] = np.clip(a[:, 3, :3] * 1.3 + 10, 0, 255)
    elif side == "e":
        a[:, 15] = g; a[:, 14] = g
        a[:, 13, :3] = (a[:, 13, :3] * 0.45).astype(int)
        a[:, 12, :3] = np.clip(a[:, 12, :3] * 1.3 + 10, 0, 255)
    return _img(a)


def inner_corner(fill: Image.Image, outer: Image.Image, which: str, r: int = 5) -> Image.Image:
    """13-piece completion: an inner (concave) corner = the fill with the `which`
    diagonal bitten by the matching OUTER corner's designed transition curve."""
    f, o = _arr(fill), _arr(outer)
    for y in range(16):
        for x in range(16):
            if which == "nw": d = (r - x) + (r - y)
            elif which == "ne": d = (x - (15 - r)) + (r - y)
            elif which == "sw": d = (r - x) + (y - (15 - r))
            else: d = (x - (15 - r)) + (y - (15 - r))
            if d >= 2:
                f[y, x] = o[y, x]
            elif d >= 0:
                f[y, x] = (f[y, x] + o[y, x]) // 2
    return _img(f)


_WOOD = [_hex("#3a2418"), _hex("#7a4a28"), _hex("#b9763f"), _hex("#e0a466")]
_STONE = [_hex("#2a2c40"), _hex("#4a4d66"), _hex("#6c6f86"), _hex("#9a9db4")]


def draw_fence_h() -> Image.Image:
    """Post + two horizontal slats spanning the tile (wraps left-right) — a run of
    these is a fence line; cap each end with draw_fence_post()."""
    a = np.zeros((16, 16, 4), np.int16)
    o, d, m, l = _WOOD
    for y, c in ((6, m), (7, d), (10, m), (11, d)):
        a[y, :, :] = c
    a[5, :, :] = l
    a[9, :, :] = l
    for x in (7, 8):
        for y in range(3, 14):
            a[y, x] = m if y < 8 else d
        a[3, x] = l
        a[13, x] = o
    for x in (6, 9):
        a[3, x] = o; a[4, x] = o
    return _img(a)


def draw_fence_post() -> Image.Image:
    """A single picket — stack vertically for a N-S fence run, or use as an end cap."""
    a = np.zeros((16, 16, 4), np.int16)
    o, d, m, l = _WOOD
    for x in (7, 8):
        for y in range(3, 14):
            a[y, x] = m if y < 8 else d
        a[3, x] = l
        a[13, x] = o
    for x in (6, 9):
        a[3, x] = o; a[4, x] = o
    return _img(a)


def draw_boulder() -> Image.Image:
    """A 1-tile rock (deco, collides): outline ring, lit top-left, shadowed
    bottom-right, soft contact shadow — the 4-step ladder on a prop."""
    a = np.zeros((16, 16, 4), np.int16)
    o, d, m, l = _STONE
    cx, cy, r = 8, 9, 5.4
    for y in range(16):
        for x in range(16):
            dd = ((x - cx) ** 2 + (y - cy + (x - cx) * 0.1) ** 2) ** 0.5
            if dd < r:
                if dd > r - 1.2: a[y, x] = o
                elif (x - cx) - (y - cy) > 2: a[y, x] = l
                elif (y - cy) + (x - cx) > 2.2: a[y, x] = d
                else: a[y, x] = m
    a[8, 6] = d; a[9, 7] = d; a[7, 9] = d
    for x in range(4, 13):
        a[14, x] = [10, 12, 24, 90]
    return _img(a)


def draw_flowerbed(seed: int = 0) -> Image.Image:
    """A cluster of dusk blooms (bone / fire / diamond accents + leaf bases) —
    the garden/verge filler the reference maps scatter everywhere."""
    a = np.zeros((16, 16, 4), np.int16)
    rng = np.random.default_rng(seed + 40)
    bone, fire, dia = _hex("#f5f0e1"), _hex("#ff8a3d"), _hex("#9fe7ff")
    leaf = _hex("#2f6a5a")
    cols = [bone, bone, fire, dia]
    for _ in range(6):
        x, y = int(rng.integers(2, 14)), int(rng.integers(2, 14))
        c = cols[int(rng.integers(0, len(cols)))]
        for (dx, dy) in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            a[(y + dy) % 16, (x + dx) % 16] = c
        a[y, x] = _hex("#f6d36b")
        a[(y + 2) % 16, x] = leaf
    return _img(a)
