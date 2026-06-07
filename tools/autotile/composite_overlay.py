#!/usr/bin/env python3
"""
Composite a seamless autotile (9-slice + strips) for a FLAT terrain that sits over
another flat terrain (e.g. dirt-path-on-grass, tall-grass-on-grass).

Why: AI-generating each cell of a simple flat transition gives mismatched dirt,
per-tile banding, and junction tiles that don't match the strips. For a flat
"inner over outer" surface the reliable answer is deterministic compositing from
two UNIFORM fills: the dirt/blades is identical in every piece, the grass edge is
a controlled subtle dither, and the result is inherently seamless (16 % 4 == 0, so
the Bayer dither tiles; uniform fills tile by construction). Junctions match the
strips because they share the same dirt fill.

Use this for flat transitions. Keep AI per-cell generation for ORGANIC transitions
(foam shorelines, tree canopy, cliff faces) where real drawn detail matters.

Usage:
  composite_overlay.py INNER.png OUTER.png OUTDIR [--depth 3]
    INNER = the terrain body fill (dirt / blades), uniform & tileable
    OUTER = what shows on the edges (grass), uniform & tileable
Writes: corner_nw/edge_n/corner_ne/edge_w/fill/edge_e/corner_sw/edge_s/corner_se
        + strip_h + strip_v, named "<i>_<role>.png" for slice-compatible consumers.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]  # /16
# active outer edges per role: which sides show the OUTER (grass) surface
ROLES = {
    "corner_nw": ("N", "W"), "edge_n": ("N",), "corner_ne": ("N", "E"),
    "edge_w": ("W",), "fill": (), "edge_e": ("E",),
    "corner_sw": ("S", "W"), "edge_s": ("S",), "corner_se": ("S", "E"),
    "strip_h": ("N", "S"), "strip_v": ("W", "E"),
}
ORDER = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
         "corner_sw", "edge_s", "corner_se", "strip_h", "strip_v"]


def dist(edge, x, y, w, h):
    return {"N": y, "S": h - 1 - y, "W": x, "E": w - 1 - x}[edge]


def is_outer(edges, x, y, w, h, t):
    """True => paint OUTER (grass) here. Solid for the outer (t-2) px, then a 2px
    Bayer dither, then INNER. d = depth from the nearest active edge."""
    if not edges:
        return False
    d = min(dist(e, x, y, w, h) for e in edges)
    if d <= t - 2:
        return True
    b = BAYER[y % 4][x % 4] / 16.0
    if d == t - 1:
        return b < 0.7
    if d == t:
        return b < 0.3
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("inner"); ap.add_argument("outer"); ap.add_argument("outdir")
    ap.add_argument("--depth", type=int, default=3, help="grass edge depth in px (default 3)")
    a = ap.parse_args()
    inner = Image.open(a.inner).convert("RGBA"); outer = Image.open(a.outer).convert("RGBA")
    w, h = inner.size; ip, op = inner.load(), outer.load()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    for i, role in enumerate(ORDER):
        edges = ROLES[role]; im = Image.new("RGBA", (w, h)); px = im.load()
        for y in range(h):
            for x in range(w):
                px[x, y] = op[x, y] if is_outer(edges, x, y, w, h, a.depth) else ip[x, y]
        im.save(out / f"{i:02d}_{role}.png")
    print(f"  composited {len(ORDER)} tiles -> {out}")


if __name__ == "__main__":
    main()
