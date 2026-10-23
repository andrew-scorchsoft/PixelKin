#!/usr/bin/env python3
"""
milagro_photo — a milagro card straight from its PHOTO (for cards the image model
won't recreate): perspective-flatten the card from four corner points picked on its
ref crop (assets/milagros/refs/<slug>.jpg), correct the room's warm cast (each
channel stretched so the white card edge reads white), and write the master
assets/milagros/<slug>.webp at the generated cards' 2:3 size.

    python3 tools/assets/milagro_photo.py            # every card in CORNERS
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "assets" / "milagros"
OUT_W, OUT_H = 682, 1024

# TL, TR, BR, BL in the ref crop's pixels (corners may sit just off the crop)
CORNERS = {
    "truthlie": [(20, 8), (648, 12), (650, 880), (20, 886)],
    "skin": [(82, 0), (668, 42), (682, 816), (45, 798)],
    "blissful": [(100, -5), (665, 95), (622, 905), (5, 800)],
    "loon": [(4, 6), (668, 8), (670, 894), (8, 894)],
    "taxi": [(20, 14), (626, 24), (640, 892), (14, 884)],
}


def coeffs(dst, src):
    """Perspective coefficients mapping output pixels (dst) back to input (src)."""
    a = []
    for (x, y), (u, v) in zip(dst, src):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = np.array(src).reshape(8)
    return np.linalg.solve(np.array(a, dtype=float), b)


def white_balance(im: Image.Image) -> Image.Image:
    a = np.asarray(im).astype(float)
    for c in range(3):
        hi = np.percentile(a[..., c], 99.2)
        lo = np.percentile(a[..., c], 0.5)
        a[..., c] = (a[..., c] - lo) / max(1.0, hi - lo) * 250
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def flatten(slug: str) -> None:
    ref = Image.open(SRC / "refs" / f"{slug}.jpg").convert("RGB")
    pad = 60   # room for corners that sit just off the crop (filled card-white)
    canvas = Image.new("RGB", (ref.width + pad * 2, ref.height + pad * 2), (238, 236, 230))
    canvas.paste(ref, (pad, pad))
    src = [(x + pad, y + pad) for x, y in CORNERS[slug]]
    dst = [(0, 0), (OUT_W, 0), (OUT_W, OUT_H), (0, OUT_H)]
    flat = canvas.transform((OUT_W, OUT_H), Image.PERSPECTIVE, coeffs(dst, src), Image.BICUBIC)
    white_balance(flat).save(SRC / f"{slug}.webp", quality=94)
    print(f"  flattened {slug}")


if __name__ == "__main__":
    for s in CORNERS:
        flatten(s)
