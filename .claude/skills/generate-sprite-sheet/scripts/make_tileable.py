#!/usr/bin/env python3
"""
Make a flat FIELD tile (grass, floor, path, soil, sand, water) tile seamlessly.

Image models reliably draw a 1-2px lighter/darker rim around a tile (a baked-in
top-left light edge or a frame), even when told not to. On a large repeated field
that rim becomes a visible grid — the "gridded / poor" look. For a tile whose
interior is meant to be uniform, the fix is deterministic: overwrite the outer
ring of pixels with their inner neighbour so every edge matches the interior and
opposing edges agree → an invisible (toroidal) seam. Crisp pixels are preserved
(no blur) since we copy whole pixels.

This is ONLY for uniform field tiles. Do NOT run it on structural/edge tiles
(water_edge, cliff_edge, walls/roofs/doors with intentional borders) — it would
eat their designed edges.

Usage (from repo root):
    ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/make_tileable.py \
        assets/tilesets/_shared/grass.png [more.png ...] [--ring 1]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def _avg(a, b):
    return tuple((a[i] + b[i]) // 2 for i in range(len(a)))


def clamp_edges(img: Image.Image, ring: int) -> Image.Image:
    """Make a uniform field tile tile seamlessly.

    Two steps: (1) overwrite the outer `ring` with the adjacent inner line to kill
    the model's baked rim/vignette; (2) make OPPOSITE edges identical (average the
    top with the bottom, the left with the right) so a tile's right edge equals the
    next tile's left edge — a true toroidal seam. Step 2 is what the old 1px clamp
    was missing (clamping to the interior still left left≠right, so a faint grid
    remained). Whole-pixel ops only; for near-flat fills the averaging is invisible.
    """
    px = img.load()
    w, h = img.size
    if w <= 2 * ring or h <= 2 * ring:
        raise SystemExit(f"tile {w}x{h} too small for ring {ring}")
    # (1) kill the rim: outer ring ← adjacent inner line.
    for r in range(ring):
        for x in range(w):
            px[x, r] = px[x, ring]
            px[x, h - 1 - r] = px[x, h - 1 - ring]
    for c in range(ring):
        for y in range(h):
            px[c, y] = px[ring, y]
            px[w - 1 - c, y] = px[w - 1 - ring, y]
    # (2) toroidal: opposite outer lines made identical so the seam vanishes when tiled.
    for x in range(w):
        m = _avg(px[x, 0], px[x, h - 1]); px[x, 0] = m; px[x, h - 1] = m
    for y in range(h):
        m = _avg(px[0, y], px[w - 1, y]); px[0, y] = m; px[w - 1, y] = m
    return img


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tiles", nargs="+", help="tile PNG paths to make seamless (in place)")
    ap.add_argument("--ring", type=int, default=1, help="edge width to clamp (default 1)")
    args = ap.parse_args()

    for t in args.tiles:
        p = Path(t)
        img = Image.open(p).convert("RGBA")
        clamp_edges(img, args.ring).save(p)
        print(f"  seamless ring={args.ring} -> {p}")


if __name__ == "__main__":
    main()
