#!/usr/bin/env python3
"""
fix_purple_rim.py — clean the purple/mauve silhouette RIM old chroma-keyed sprites carry.

Sprites generated on a magenta key (before gpt-image-2.5's native alpha) were
downscaled with the key still blended into their outermost pixels: the rim reads as
a purple hue around the character in-game (the owner spotted it on the player).
defringe.py only catches strongly pink pixels; this pass catches the subtler purple/
mauve cast on the outer rim and re-tints each such pixel as a DARKER shade of the
colour just inside it (hair gets a dark-brown edge, a coat a dark-green one), falling
back to the house ink. Lossless and local; never touch native-alpha art with it.

  python3 tools/assets/fix_purple_rim.py assets/trainers/player_indi.png [...]
  (then re-pack: pack_trainers.py / pack_creatures.py)
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

INK = (30, 21, 46)


def fix(src: Path) -> int:
    a = np.array(Image.open(src).convert("RGBA")).astype(float)
    op = a[..., 3] > 0
    tr = ~op
    nb = np.zeros_like(op)
    nb[1:] |= tr[:-1]; nb[:-1] |= tr[1:]; nb[:, 1:] |= tr[:, :-1]; nb[:, :-1] |= tr[:, 1:]
    edge, inner = op & nb, op & ~nb
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    cast = edge & (r - g > 15) & (b - g > 5) & (b > 0.55 * r)
    H, W = op.shape
    for y, x in zip(*np.nonzero(cast)):
        cols = [a[y + dy, x + dx, :3] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                if 0 <= y + dy < H and 0 <= x + dx < W and inner[y + dy, x + dx] and not cast[y + dy, x + dx]]
        a[y, x, :3] = np.mean(cols, 0) * 0.5 if cols else INK
    Image.fromarray(a.astype(np.uint8)).save(src)
    return int(cast.sum())


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(f"{f}: re-tinted {fix(Path(f))} rim px")
