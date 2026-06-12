#!/usr/bin/env python3
"""
draw_starglints — tiny transparent star-glint decals for the Wind-Eye oculus
(N6 POL-1): the void there is SKY seen through the mountain, not the
Penumbra's floorless dark, so a few faint stars sell the difference. The
shared set's void family is frozen (386 tiles) and its fill animation is the
anti-light wisp register — so these are 1x1 OBJECTS scattered sparsely over
the void cells (non-solid; the void collides on its own).

Two variants so the scatter doesn't repeat: each is one small cross-twinkle
plus one or two satellite points, very low alpha — a glimmer, not a skybox.

Writes assets/tilesets/windward/objects/starglint_{a,b}.png (16x16) — packed
to `windward_starglint_a/b` by pack_objects.py.

Run:  ./venv/bin/python tools/maps/draw_starglints.py
      ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import numpy as np
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "windward" / "objects"

PALE = (207, 232, 255)    # starlight white-blue
DIM = (140, 170, 214)     # the fainter satellites


def glint(cross_at: tuple[int, int], satellites: list[tuple[int, int]]) -> Image.Image:
    a = np.zeros((16, 16, 4), dtype=np.uint8)
    cx, cy = cross_at
    a[cy, cx] = (*PALE, 235)              # the twinkle core
    for (dx, dy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        a[cy + dy, cx + dx] = (*PALE, 120)
    for (sx, sy) in satellites:
        a[sy, sx] = (*DIM, 130)
    return Image.fromarray(a, "RGBA")


def main() -> None:
    OBJDIR.mkdir(parents=True, exist_ok=True)
    glint((5, 6), [(11, 11), (13, 3)]).save(OBJDIR / "starglint_a.png")
    glint((10, 9), [(3, 12)]).save(OBJDIR / "starglint_b.png")
    print(f"2 star-glint masters -> {OBJDIR.relative_to(REPO)} — now run pack_objects.py")


if __name__ == "__main__":
    main()
