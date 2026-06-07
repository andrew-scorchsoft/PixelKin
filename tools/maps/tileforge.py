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
