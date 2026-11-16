#!/usr/bin/env python3
"""Pack THE DEPOT — the ending's last scene, after the credits (content/cinematics.ts
ENDING_CREDITS): assets/backgrounds/cinematic/depot/depot-1..5.webp (image-gen masters;
2..5 are edits of 1 so the hall stays the same hall) -> public/assets/backgrounds/
cinematic/depot-01..05.webp at 240x160. Any black letterbox the model baked in is
trimmed, then the picture is cover-cropped to 3:2.

    python3 tools/assets/pack_depot_frames.py
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "assets/backgrounds/cinematic/depot"
OUT = REPO / "public/assets/backgrounds/cinematic"
for n in range(1, 6):
    im = Image.open(SRC / f"depot-{n}.webp").convert("RGB")
    a = np.asarray(im).astype(int).sum(axis=2)
    rows = np.where(a.mean(axis=1) > 24)[0]
    cols = np.where(a.mean(axis=0) > 24)[0]
    im = im.crop((cols.min(), rows.min(), cols.max() + 1, rows.max() + 1))
    w, h = im.size
    if w * 2 > h * 3:                       # too wide: trim the sides
        nw = h * 3 // 2
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:                                   # too tall: trim top and bottom
        nh = w * 2 // 3
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((240, 160), Image.LANCZOS).save(OUT / f"depot-{n:02d}.webp", "WEBP", quality=90, method=6)
    print(f"depot-{n:02d}.webp  <- {w}x{h}")
