#!/usr/bin/env python3
"""
build_farlamp_interior_set — the Farlamp Isles' SEA-WASHED interior kit.

A pixel transform of the warm `interior_set` with the IDENTICAL tile order,
count and per-tile metadata (the build_oldlight_sets.py pattern), so the isles'
rooms swap `interior_set` for `interior_sea_set` with zero gid changes:

  floors   bleached grey-blue driftwood planks (the warm boards, salt-silvered)
  face     whitewashed plaster over a sea-green wainscot
  bands    the dark wall-top, cooled toward slate
  window   kept lamp-lit (the warm panes are the room's one warm note)
  mat      a blue rope mat

Readability is binding: every wall band stays darker than every floor fill.

Reads   public/assets/tilesets/interior_set.webp (+ sidecar)
Writes  assets/tilesets/farlamp/sets/interior_sea_set.png   (master)
        public/assets/tilesets/interior_sea_set.webp         (lossless, served)
        public/assets/tilesets/interior_sea_set.tileset.json (sidecar)
Deterministic; re-run freely.

Run:  python3 tools/maps/build_farlamp_interior_set.py
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
MASTERS = REPO / "assets" / "tilesets" / "farlamp" / "sets"
NAME = "interior_sea_set"


def sea(tiles):
    out = [t.copy() for t in tiles]
    for i in FLOORS:                                   # salt-silvered driftwood
        t = hue_rotate(out[i], 160)
        t = saturate(t, 0.2)
        out[i] = mul(t, 0.98, 1.0, 1.0, add=(16, 18, 18))
    for i in FACES:                                    # whitewash + sea-green wainscot
        t = hue_rotate(out[i], 140)
        t = saturate(t, 0.45)
        out[i] = mul(t, 0.94, 1.02, 0.98, add=(4, 8, 6))
    for i in BANDS:                                    # the wall-top, slate-cool
        t = hue_rotate(out[i], 165)
        out[i] = saturate(t, 0.3)
    out[MAT] = saturate(hue_rotate(out[MAT], 175), 0.55)
    # INSET (the lamp-lit window) is left warm on purpose
    return out


def main() -> None:
    src, side = load("interior_set")
    tiles = sea(src)
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
