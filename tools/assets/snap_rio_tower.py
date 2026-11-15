#!/usr/bin/env python3
"""Snap the Rio Tower's image-gen master (assets/tilesets/sere/raw/rio_tower.png,
gpt-image native alpha) onto its object canvas: 5x11 tiles, the door centred on
col 2, hard alpha (no glow halo), so pack_objects.py packs `sere_rio_tower`.

    python3 tools/assets/snap_rio_tower.py
"""
from pathlib import Path
import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "assets/tilesets/sere/raw/rio_tower.png"
OUT = REPO / "assets/tilesets/sere/objects/rio_tower.png"
TW, TH = 5, 11

im = Image.open(SRC).convert("RGBA")
a = np.asarray(im)
ys, xs = np.where(a[..., 3] > 160)
im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
h = TH * 16
w = round(im.width * h / im.height)
im = im.resize((w, h), Image.BOX)
arr = np.asarray(im).copy()
arr[..., 3] = np.where(arr[..., 3] >= 140, 255, 0)
im = Image.fromarray(arr)
out = Image.new("RGBA", (TW * 16, TH * 16))
out.alpha_composite(im, ((TW * 16 - w) // 2, 0))
out.save(OUT)
print(f"rio_tower -> {OUT.relative_to(REPO)} ({out.size[0]}x{out.size[1]}, art {w}px wide)")
