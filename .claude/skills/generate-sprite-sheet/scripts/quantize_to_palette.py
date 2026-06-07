#!/usr/bin/env python3
"""
Snap a sprite/tile's colours to a locked palette.

The #1 cause of a "washed-out, incoherent" tile set is colour drift: the image
model paints each asset in slightly different, low-contrast hues. This tool maps
every opaque pixel to its nearest colour in a fixed palette, so a whole set
shares exactly one set of colours with the value contrast we designed in.

Palette sources (pick one):
  --area NAME        use areas.<NAME>.working_palette from world-palette.json
  --ramp NAME [...]  use one or more ramps.<NAME> from world-palette.json
  --colors "#rrggbb,#rrggbb,..."   an explicit comma-separated list

Examples:
  quantize_to_palette.py grass.png --area tinderwick
  quantize_to_palette.py *.png --area tinderwick                 # whole set
  quantize_to_palette.py cliff.png --ramp stone ink
  quantize_to_palette.py x.png --colors "#1a1430,#3f7a44,#9ff07a" --output y.png

Transparency is preserved: fully transparent pixels stay transparent; partly
transparent pixels keep their alpha and get their RGB quantised. By default it
edits the file(s) in place; pass --output for a single-file copy.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent


def find_repo_root(start: Path) -> Path:
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return start


def palette_path() -> Path:
    repo = find_repo_root(Path.cwd().resolve())
    return repo / "assets" / "tilesets" / "world-palette.json"


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Bad hex colour: {h!r}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def load_palette(args: argparse.Namespace) -> list[tuple[int, int, int]]:
    if args.colors:
        return [hex_to_rgb(c) for c in args.colors.split(",") if c.strip()]
    data = json.loads(palette_path().read_text())
    hexes: list[str] = []
    if args.area:
        area = data.get("areas", {}).get(args.area)
        if not area:
            raise SystemExit(f"Area '{args.area}' not in world-palette.json")
        wp = area.get("working_palette")
        if not wp:
            raise SystemExit(
                f"Area '{args.area}' has no working_palette; add one or use --ramp/--colors."
            )
        hexes += wp
    for ramp in args.ramp or []:
        steps = data.get("ramps", {}).get(ramp)
        if not steps:
            raise SystemExit(f"Ramp '{ramp}' not in world-palette.json ramps")
        hexes += steps
    if not hexes:
        raise SystemExit("Provide a palette: --area, --ramp, or --colors.")
    # de-dupe, keep order
    seen: dict[str, None] = {}
    for h in hexes:
        seen.setdefault(h.lower(), None)
    return [hex_to_rgb(h) for h in seen]


def quantize_image(img: Image.Image, palette: list[tuple[int, int, int]]) -> Image.Image:
    import numpy as np

    rgba = np.asarray(img.convert("RGBA")).astype(np.int16)
    rgb = rgba[..., :3]
    a = rgba[..., 3]
    pal = np.asarray(palette, dtype=np.int16)  # (P,3)

    # Nearest palette colour by squared distance, weighted toward luma so value
    # (the contrast we care about) dominates the match a little.
    w = np.array([0.9, 1.2, 0.7], dtype=np.float32)  # R,G,B perceptual-ish weights
    flat = rgb.reshape(-1, 3).astype(np.float32)
    d = (((flat[:, None, :] - pal[None, :, :].astype(np.float32)) ** 2) * w).sum(axis=2)
    idx = d.argmin(axis=1)
    out_rgb = pal[idx].reshape(rgb.shape).astype(np.uint8)

    out = np.dstack([out_rgb, a.astype(np.uint8)])
    # Keep fully-transparent pixels truly clear (rgb irrelevant, but tidy = 0).
    clear = a == 0
    out[clear] = (0, 0, 0, 0)
    return Image.fromarray(out, "RGBA")


def main() -> int:
    p = argparse.ArgumentParser(description="Quantise image colours to a locked palette.")
    p.add_argument("files", nargs="+", help="PNG file(s) to quantise.")
    p.add_argument("--area", help="Use areas.<AREA>.working_palette from world-palette.json.")
    p.add_argument("--ramp", action="append", help="Use ramps.<NAME> (repeatable).")
    p.add_argument("--colors", help="Explicit comma-separated #rrggbb list.")
    p.add_argument("--output", help="Write here instead of in place (single input only).")
    args = p.parse_args()

    if args.output and len(args.files) != 1:
        p.error("--output only works with a single input file.")

    palette = load_palette(args)
    for f in args.files:
        src = Path(f)
        img = Image.open(src).convert("RGBA")
        out = quantize_image(img, palette)
        dst = Path(args.output) if args.output else src
        out.save(dst, format="PNG", optimize=True)
        print(f"quantised {src.name} -> {dst} ({len(palette)} colours)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
