#!/usr/bin/env python3
"""
build_stillwater_interior_set — Stillwater's SHUTTER-GREY interior kit
(walkthrough/11 Part A: the Hollowing's village).

A pixel transform of the warm `interior_set` with the IDENTICAL tile order, count
and per-tile metadata (the build_oldlight_sets.py / build_farlamp_interior_set.py
pattern), so Stillwater's rooms swap `interior_set` for `interior_shutter_set`
with zero gid changes:

  floors   grey-washed boards (the warm planks, drained and cooled)
  face     pale grey limewash over a slate wainscot
  bands    the wall-top, slate
  window   SHUTTERED: the warm pane drained to painted grey (the village keeps its
           windows closed; the warm note in these rooms is the hearth alone)
  mat      a grey wool mat

Readability is binding: every wall band stays darker than every floor fill.

Reads   public/assets/tilesets/interior_set.webp (+ sidecar)
Writes  assets/tilesets/stillwater/sets/interior_shutter_set.png   (master)
        public/assets/tilesets/interior_shutter_set.webp           (lossless, served)
        public/assets/tilesets/interior_shutter_set.tileset.json   (sidecar)
Deterministic; re-run freely.

Run:  python3 tools/maps/build_stillwater_interior_set.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_oldlight_sets import (load, assemble, saturate, hue_rotate, mul, lum,  # noqa: E402
                                 FLOORS, MAT, FACES, INSET, BANDS, SRC, seam_score)

REPO = Path(__file__).resolve().parents[2]
MASTERS = REPO / "assets" / "tilesets" / "stillwater" / "sets"
NAME = "interior_shutter_set"


def shutter(tiles):
    out = [t.copy() for t in tiles]
    for i in FLOORS:                                   # grey-washed boards
        t = saturate(out[i], 0.12)
        out[i] = mul(t, 0.9, 0.92, 1.0, add=(6, 8, 14))
    for i in FACES:                                    # pale grey limewash
        t = saturate(out[i], 0.1)
        out[i] = mul(t, 0.96, 0.98, 1.04, add=(4, 6, 10))
    for i in BANDS:                                    # slate wall-top
        t = hue_rotate(out[i], 200)
        out[i] = saturate(t, 0.18)
    out[INSET] = mul(saturate(out[INSET], 0.0), 0.72, 0.75, 0.84)   # shutters closed
    out[MAT] = saturate(out[MAT], 0.08)
    return out


def main() -> None:
    src, side = load("interior_set")
    tiles = shutter(src)
    for a, b in zip(tiles, src):
        a[..., 3] = b[..., 3]
        a[a[..., 3] == 0] = 0
    band = max(lum(tiles[i])[tiles[i][..., 3] > 0].mean() for i in BANDS)
    floor = min(lum(tiles[i]).mean() for i in FLOORS)
    assert band + 15 < floor, f"walls ({band:.0f}) too close to floors ({floor:.0f})"
    assert all(seam_score(tiles[i]) < 1.6 for i in FLOORS), "a floor fill shows its seam"
    im = assemble(tiles)
    MASTERS.mkdir(parents=True, exist_ok=True)
    im.save(MASTERS / f"{NAME}.png")
    out = SRC / f"{NAME}.webp"
    im.save(out, "WEBP", lossless=True, quality=100, method=6)
    back = np.asarray(Image.open(out).convert("RGBA"))
    assert (back == np.asarray(im)).all(), "WebP not lossless"
    side = dict(side)
    side["name"] = NAME
    side["image"] = f"assets/tilesets/{NAME}.webp"
    (SRC / f"{NAME}.tileset.json").write_text(json.dumps(side, indent=2) + "\n")
    print(f"  {NAME}  band lum {band:.0f} < floor lum {floor:.0f}")


if __name__ == "__main__":
    main()
