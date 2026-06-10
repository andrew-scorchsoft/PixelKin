#!/usr/bin/env python3
"""Snap portrait-bust masters to 32x32 frames and assemble horizontal strips.

Each character gets ONE horizontal strip PNG (width = 32 * frameCount, height = 32),
transparent, with frame index = expression (per src/game/content/portraits.ts).
Busts are head-and-shoulders, so we anchor the TOP of the trimmed art near the
top of the 32px frame (heads line up) and center horizontally — consistent
framing/scale across all frames of a character.
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MASTERS = os.path.join(HERE, "_masters")
OUT_DIR = os.path.join(HERE, "..", "..", "public", "assets", "portraits")
OUT_DIR = os.path.normpath(OUT_DIR)

SIZE = 32
# Bust fills the frame nicely; small top pad so the head isn't jammed to the edge.
TOP_PAD = 1
# Fraction of the 32px the trimmed art should occupy in its larger dimension.
FILL = (SIZE - TOP_PAD) / SIZE

# character -> ordered list of (expression-suffix) matching the frame index order.
STRIPS = {
    "fenn": ["neutral", "warm", "grave", "smile"],
    "wren": ["neutral", "eager", "unsure"],
    "brisa": ["neutral", "warm", "proud"],
    "reyl": ["neutral", "weathered", "proud"],
    "lamplighter": ["neutral", "grave"],
    "hearthkeeper": ["neutral", "warm"],
    "cor": ["neutral", "grave"],
}


def alpha_bbox(im):
    a = im.split()[-1]
    return a.getbbox()


def snap_frame(path):
    """Trim to alpha bbox, scale to fill, paste top-anchored & h-centered on 32x32."""
    im = Image.open(path).convert("RGBA")
    bbox = alpha_bbox(im)
    if bbox:
        im = im.crop(bbox)
    w, h = im.size
    # Scale so the larger dimension fits FILL*SIZE (busts are ~square; head-led).
    target = FILL * SIZE
    scale = target / max(w, h)
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    im = im.resize((nw, nh), Image.LANCZOS)
    # Harden alpha edges (no semi-transparent halo from downscale).
    r, g, b, a = im.split()
    a = a.point(lambda v: 255 if v >= 128 else 0)
    im = Image.merge("RGBA", (r, g, b, a))
    frame = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    x = (SIZE - nw) // 2          # horizontally centered
    y = TOP_PAD                   # top-anchored (heads align across frames)
    # If a bust is shorter than the frame, that's fine — shoulders fade at bottom.
    frame.alpha_composite(im, (x, y))
    return frame


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    for char, exprs in STRIPS.items():
        frames = []
        for expr in exprs:
            p = os.path.join(MASTERS, f"{char}_{expr}.png")
            if not os.path.exists(p):
                raise SystemExit(f"missing master: {p}")
            frames.append(snap_frame(p))
        strip = Image.new("RGBA", (SIZE * len(frames), SIZE), (0, 0, 0, 0))
        for i, fr in enumerate(frames):
            strip.alpha_composite(fr, (i * SIZE, 0))
        out = os.path.join(OUT_DIR, f"{char}.png")
        strip.save(out)
        print(f"{out}  {strip.width}x{strip.height}  ({len(frames)} frames: {exprs})")


if __name__ == "__main__":
    build()
