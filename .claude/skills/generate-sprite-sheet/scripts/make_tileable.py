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


def clamp_edges(img: Image.Image, ring: int) -> Image.Image:
    """Replace the outer `ring` rows/cols on every side with the adjacent inner line."""
    px = img.load()
    w, h = img.size
    if w <= 2 * ring or h <= 2 * ring:
        raise SystemExit(f"tile {w}x{h} too small for ring {ring}")
    # Top & bottom rows ← first/last interior row.
    for r in range(ring):
        for x in range(w):
            px[x, r] = px[x, ring]
            px[x, h - 1 - r] = px[x, h - 1 - ring]
    # Left & right cols ← first/last interior col (after rows are fixed, so corners agree).
    for c in range(ring):
        for y in range(h):
            px[c, y] = px[ring, y]
            px[w - 1 - c, y] = px[w - 1 - ring, y]
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
