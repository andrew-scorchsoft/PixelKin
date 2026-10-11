#!/usr/bin/env python3
"""defringe.py — remove the magenta chroma-key halo from sprite MASTERS, losslessly.

Older sprites were generated on a flat magenta (#FF00FF) field and keyed out.
The key left two kinds of residue around every silhouette:
  1. faint partial-alpha pixels (alpha 1-127) whose RGB is still magenta — a pink
     glow wherever the sprite sits on a light ground or is scaled;
  2. opaque edge pixels tinted pink/lavender — a visible pink outline.
This pass (a) snaps alpha to 0/255 (the art bible: no semi-transparent pixels),
then (b) recolours any pink pixel within 2px of transparency to the sprite's own
dark outline ink (the most common dark, non-pink edge colour), so the design is
untouched — only the halo goes. Interior pinks (a petal, a blush) are kept.

gpt-image-2.5 (the 2026-10 default) has native alpha, so new art doesn't need
this; it's for the back catalogue. Run on masters, then re-pack:
  ./venv/bin/python tools/assets/defringe.py assets/creatures/*/*.png
  ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_creatures.py
Prints a per-file report; --check measures without writing.
"""
import argparse, sys
from collections import Counter
from PIL import Image

CUT = 128
EDGE_DEPTH = 2


def is_pink(r, g, b):
    """Chroma residue: near-MAGENTA hue (red ~= blue, green suppressed). Design
    pinks (petals, blush, coral) lean red (r >> b) and are left alone."""
    return r > 150 and b > 140 and g < 0.82 * min(r, b) and abs(r - b) < 60


def defringe(im: Image.Image):
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    partial = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if 0 < a < CUT:
                px[x, y] = (0, 0, 0, 0); partial += 1
            elif a >= CUT and a != 255:
                px[x, y] = (r, g, b, 255)
    solid = lambda x, y: 0 <= x < w and 0 <= y < h and px[x, y][3] == 255
    # distance (in steps) from transparency, up to EDGE_DEPTH
    dist = {}
    frontier = [(x, y) for y in range(h) for x in range(w)
                if solid(x, y) and any(not solid(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for p in frontier:
        dist[p] = 1
    for d in range(2, EDGE_DEPTH + 1):
        nxt = []
        for (x, y) in frontier:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if solid(*q) and q not in dist:
                    dist[q] = d; nxt.append(q)
        frontier = nxt
    inks = Counter()
    for (x, y), d in dist.items():
        r, g, b, _ = px[x, y]
        if d == 1 and not is_pink(r, g, b) and (0.3 * r + 0.59 * g + 0.11 * b) < 70:
            inks[(r, g, b)] += 1
    ink = inks.most_common(1)[0][0] if inks else (36, 22, 52)
    pink = 0
    for (x, y), d in dist.items():
        r, g, b, _ = px[x, y]
        if is_pink(r, g, b):
            px[x, y] = (*ink, 255); pink += 1
    return im, partial, pink


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--check", action="store_true", help="measure only, don't write")
    a = ap.parse_args()
    tp = tk = 0
    for f in a.files:
        src = Image.open(f)
        out, partial, pink = defringe(src)
        tp += partial; tk += pink
        if partial or pink:
            print(f"{f}: dropped {partial} faint px, re-inked {pink} pink edge px")
            if not a.check:
                out.save(f, optimize=True)
    print(f"total: {tp} faint px dropped, {tk} pink edge px re-inked across {len(a.files)} files")


if __name__ == "__main__":
    sys.exit(main())
