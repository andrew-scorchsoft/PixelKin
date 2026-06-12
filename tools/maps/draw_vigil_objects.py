#!/usr/bin/env python3
"""
draw_vigil_objects — the Starfall Vigil set-pieces (R3, walkthrough/06-postgame
§STARFALL VIGILS), drawn in code (the gbaforge rule: no paid image-gen for
small structural props):

  * star_shard (32x32, 2x2 tiles) — the fallen star-shard each Vigil site
    guards: a faceted starlight crystal leaning in a small impact crater,
    warm gold core under pale blue-white faces, a few twinkles. Solid
    scenery (the set-piece at the far end of every `vigil_*` annex).
  * star_scar (16x16, 1x1) — the host-map "seam of starlight, shut tight":
    the non-solid deco object each shipped host gains, gated
    `requires_flag: flag:dawn` (visible only once the sky is back).

Writes assets/tilesets/vigil/objects/*.png — packed to `vigil_star_shard` /
`vigil_star_scar` by pack_objects.py.

Run:  ./venv/bin/python tools/maps/draw_vigil_objects.py
      ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import numpy as np
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "vigil" / "objects"

# starlight palette (matches draw_starglints + the dusk register)
PALE = (224, 240, 255)     # lit face
MID = (164, 192, 232)      # shade face
DEEP = (104, 128, 178)     # outline / dark facet
GOLD = (255, 230, 162)     # the warm core
GOLDDIM = (214, 178, 110)
CRATER = (66, 62, 74)      # impact bowl
CRATERLIP = (118, 112, 122)
GLOW = (200, 224, 255)


def _put(a, x, y, rgb, alpha=255):
    if 0 <= x < a.shape[1] and 0 <= y < a.shape[0]:
        a[y, x] = (*rgb, alpha)


def star_shard() -> Image.Image:
    a = np.zeros((32, 32, 4), dtype=np.uint8)

    # impact crater bowl (bottom third) — lip lit on the north rim
    for y in range(23, 30):
        half = [5, 7, 8, 8, 8, 7, 5][y - 23]
        for x in range(16 - half, 16 + half):
            _put(a, x, y, CRATER)
    for x in range(11, 21):
        _put(a, x, 23, CRATERLIP)
    _put(a, 10, 24, CRATERLIP)
    _put(a, 21, 24, CRATERLIP)

    # the shard: a tall faceted crystal, leaning a touch west, seated in the bowl.
    # Column spans per row: (x0, x1) inclusive; tip at y=3, foot buried at y=26.
    spans = {
        3: (15, 15), 4: (14, 16), 5: (14, 16), 6: (13, 17), 7: (13, 17),
        8: (12, 18), 9: (12, 18), 10: (12, 18), 11: (11, 18), 12: (11, 18),
        13: (11, 19), 14: (10, 19), 15: (10, 19), 16: (10, 19), 17: (10, 18),
        18: (11, 18), 19: (11, 17), 20: (11, 17), 21: (12, 16), 22: (12, 16),
        23: (13, 15), 24: (13, 15), 25: (14, 15), 26: (14, 14),
    }
    for y, (x0, x1) in spans.items():
        for x in range(x0, x1 + 1):
            # facet split: lit west face, shaded east face, dark outline
            if x == x0 or x == x1 or y in (3, 26):
                _put(a, x, y, DEEP)
            elif x <= x0 + (x1 - x0) // 2:
                _put(a, x, y, PALE)
            else:
                _put(a, x, y, MID)
    # the warm core seam (the morning held inside)
    for y in range(7, 23):
        _put(a, 14 if y < 15 else 13, y, GOLD)
    _put(a, 14, 12, GOLDDIM)
    _put(a, 13, 19, GOLDDIM)

    # glints riding the lit edge
    for (x, y) in [(15, 4), (12, 9), (10, 15)]:
        _put(a, x, y, (255, 255, 255))

    # halo twinkles (soft, off-body)
    for (x, y, al) in [(7, 6, 150), (24, 9, 150), (5, 18, 120), (26, 20, 120)]:
        _put(a, x, y, GLOW, al)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            _put(a, x + dx, y + dy, GLOW, 70)

    # faint ground-glow pooling at the crater floor
    for (x, y) in [(13, 27), (16, 27), (15, 28)]:
        _put(a, x, y, GLOW, 90)
    return Image.fromarray(a, "RGBA")


def star_scar() -> Image.Image:
    """A shut seam of starlight in the ground — diagonal crack, faint glints."""
    a = np.zeros((16, 16, 4), dtype=np.uint8)
    seam = [(3, 12), (4, 11), (5, 11), (6, 10), (7, 9), (8, 8), (9, 8),
            (10, 7), (11, 6), (12, 5)]
    for i, (x, y) in enumerate(seam):
        bright = i in (3, 6)
        _put(a, x, y, PALE if bright else MID, 235 if bright else 180)
    # the seam's dark underside (the shut lip)
    for (x, y) in [(4, 12), (6, 11), (8, 9), (10, 8), (12, 6)]:
        _put(a, x, y, DEEP, 140)
    # two gold pin-glints where the light leaks
    _put(a, 6, 9, GOLD, 200)
    _put(a, 11, 5, GOLDDIM, 170)
    # satellite twinkles
    _put(a, 13, 11, GLOW, 120)
    _put(a, 2, 6, GLOW, 110)
    return Image.fromarray(a, "RGBA")


def main() -> None:
    OBJDIR.mkdir(parents=True, exist_ok=True)
    star_shard().save(OBJDIR / "star_shard.png")
    star_scar().save(OBJDIR / "star_scar.png")
    print(f"2 vigil masters -> {OBJDIR.relative_to(REPO)} — now run pack_objects.py")


if __name__ == "__main__":
    main()
