#!/usr/bin/env python3
"""
draw_penumbra_objects — the C1 PENUMBRA drawn object kit (the threshold
register: near-black basalt + a cold violet rim + the one warm colour in the
map, lamp-gold. ZERO humour — awe and held breath).

Everything is drawn in code in the deliberate cartridge register of
gbaforge/interiorforge (flat anchors, 1px ink lines, placed motifs) so the
pieces sit on the drawn basalt ground without ringing. AI image-gen is for
hero buildings; a silhouette and a basin of light are exactly the shapes
code draws best (and null-toned consistency matters more than painterliness
here — the orchestrator contract names these four pieces).

Pieces:
  way_lamp          1x3  the SAFE-LINE lamp-post (the §3a breadcrumb): a
                         null-dark wrought post carrying the only warm colour
                         in the Penumbra — a small gold flame in a glass cell.
                         The 1x3 lamp-post convention (trunk beside the lane,
                         never ON it; no 1-tile lamps).
  spire_silhouette  10x6 THE LOOK-UP MOMENT: the Umbral Spire's foot and
                         rising silhouette at the north rim — seen before it
                         is walked (level-design §3a r3). A dead mountain-
                         Lumenary: flat void-black mass, one cold violet rim,
                         angular built shoulders going to stone, and the tall
                         dark gate at local cols 4-5 (the to_spire doors).
                         Two faint star-points above the peak — the Crown
                         completing overhead.
  starwell_basin    4x4  THE HERO: the well of fallen starlight. Top-down-
                         frontal split (interiors.md convention): a bone-
                         basalt rimmed pool holding pooled white-cyan
                         starlight, twinkles in the water, a stone front
                         face with a spill of glow at its foot.
  starglint_bright_a/b 1x1 the brighter siblings of the nightreach glints —
                         fallen-star points for the Starwell floor and the
                         Starreach crossing lines (non-solid decals).

Writes  assets/tilesets/penumbra/objects/*.png -> penumbra_<stem> keys.
Then run .claude/skills/generate-sprite-sheet/scripts/pack_objects.py.

Run:  ./venv/bin/python tools/maps/draw_penumbra_objects.py
"""
from __future__ import annotations

import numpy as np
from pathlib import Path
from PIL import Image

from interiorforge import canvas, contact_shadow, fill, hx, img, outline

REPO = Path(__file__).resolve().parents[2]
PENUMBRA = REPO / "assets" / "tilesets" / "penumbra" / "objects"

# ---- the C1 register (void-black basalt + cold violet + the one warm gold) ---------
INKV = hx("#07080e")                                   # deeper than INK — void-black
BASALT = [hx("#0c0e16"), hx("#161a26"), hx("#232838"), hx("#303852")]
VIOLET = [hx("#3a3658"), hx("#4a4470"), hx("#5d5490")]  # the cold rim light
BONE = [hx("#5a5660"), hx("#8c8694"), hx("#b8b2ba"), hx("#dcd6d2")]
LAMP = [hx("#8a5a28"), hx("#d29a4a"), hx("#f4d292"), hx("#fff2d0")]  # the only warmth
POOL = [hx("#1f2a4a"), hx("#41548a"), hx("#9ec8f0"), hx("#dcecff"), hx("#fffdf2")]
STARPALE = (207, 232, 255)
STARDIM = (140, 170, 214)


def way_lamp() -> Image.Image:
    """1x3 the safe-line lamp: null-dark post, one warm flame."""
    a = canvas(1, 3)
    # stepped dark foot (kept, swept — someone still tends this line)
    fill(a, 4, 43, 11, 46, BASALT[1])
    a[43, 5:11] = BASALT[3]
    outline(a, 4, 43, 11, 46, INKV)
    # the post, violet-edged
    a[16:43, 7] = BASALT[2]
    a[16:43, 8] = BASALT[1]
    a[16:43, 6] = VIOLET[0]
    # the cross-arm hook
    a[15, 5:11] = BASALT[2]
    # the lantern cell: dark frame, warm glass
    fill(a, 3, 4, 12, 15, BASALT[1])
    outline(a, 3, 4, 12, 15, INKV)
    fill(a, 5, 6, 10, 13, LAMP[1])
    fill(a, 6, 7, 9, 12, LAMP[2])
    a[8:12, 7] = LAMP[3]
    a[8:12, 8] = LAMP[3]
    # the crown finial
    fill(a, 6, 1, 9, 4, BASALT[2])
    a[1, 7:9] = VIOLET[1]
    # a soft warm halo (low alpha, over transparent only)
    for (dx, dy) in ((-3, 2), (3, 2), (-4, 7), (4, 7), (0, -1)):
        x, y = 7 + dx, 4 + dy
        if 0 <= x < 16 and 0 <= y < 48 and a[y, x, 3] == 0:
            a[y, x] = np.array([*LAMP[2][:3], 110], np.int16)
    contact_shadow(a, 3, 12, 47)
    return img(a)


def spire_silhouette() -> Image.Image:
    """10x6 the Umbral Spire seen before it is walked — a silhouette, not a
    building: flat void-black, one cold violet rim, the gate at tiles 4-5."""
    a = canvas(10, 6)
    W, H = 160, 96
    cx = 80
    # ---- the rising mass: a tall spire profile with angular built shoulders.
    # half-width by row: narrow tip -> stepped shoulders -> full-width foot.
    for y in range(H):
        t = y / (H - 1)
        half = int(6 + 71 * (t ** 1.6))
        # angular shoulder steps (built once, mountain now)
        if 22 <= y < 34:
            half = max(half, 26)
        if 46 <= y < 58:
            half = max(half, 48)
        if y >= 70:
            half = 80
        x0, x1 = max(0, cx - half), min(W - 1, cx + half - 1)
        fill(a, x0, y, x1, y, BASALT[0])
        # the cold violet rim, east flank only (the one light that touches it)
        a[y, x1] = VIOLET[1]
        if y > 8:
            a[y, x0] = INKV
    # tip masonry: a dead lantern-crown at the peak (the Ninth Lantern)
    fill(a, cx - 4, 0, cx + 3, 6, BASALT[1])
    outline(a, cx - 4, 0, cx + 3, 6, INKV)
    a[2, cx - 2:cx + 2] = BASALT[0]      # the dark where a flame should stand
    # faint course lines on the shoulders (drawn structure, not noise)
    for (sy, sx0, sx1) in ((28, cx - 22, cx + 21), (52, cx - 44, cx + 43),
                           (76, cx - 70, cx + 69)):
        a[sy, sx0:sx1] = BASALT[1]
    # two star-points above the shoulders — the Crown completing overhead
    for (sx, sy) in ((cx - 30, 12), (cx + 36, 20)):
        a[sy, sx] = np.array([*STARPALE, 200], np.int16)
        a[sy, sx - 1] = np.array([*STARDIM, 110], np.int16)
        a[sy, sx + 1] = np.array([*STARDIM, 110], np.int16)
    # ---- THE GATE (local tiles 4-5: px 64..95): a tall pointed arch of
    # deeper dark; the seam of light under it is all the welcome you get.
    gx0, gx1 = 64, 95
    for y in range(60, 96):
        inset = max(0, (66 - y) * 2) if y < 66 else 0
        fill(a, gx0 + 6 + inset, y, gx1 - 6 - inset, y, INKV)
    outline(a, gx0 + 6, 66, gx1 - 6, 95, BASALT[2])
    fill(a, gx0 + 7, 67, gx1 - 7, 94, INKV)
    a[94, gx0 + 10:gx1 - 9] = VIOLET[0]   # the hair-thin seam at the foot
    # jamb stones
    for jy in (72, 82, 92):
        a[jy, gx0 + 6] = BASALT[3]
        a[jy, gx1 - 6] = BASALT[3]
    contact_shadow(a, 0, W - 1, H - 1)
    return img(a)


def starwell_basin() -> Image.Image:
    """4x4 the well of fallen starlight — top surface (the pool in its rim)
    + a stone front face, per the free-standing top-down-frontal split."""
    a = canvas(4, 4)
    cx, cy = 32, 26           # pool centre (top surface)
    # ---- the rim: an elliptical bone-basalt ring
    for y in range(64):
        for x in range(64):
            dx, dy = (x - cx) / 30.0, (y - cy) / 22.0
            r = dx * dx + dy * dy
            if r <= 1.0:
                a[y, x] = (*BASALT[2][:3], 255)
    # ---- the pool: pooled starlight, banded radially (drawn, not noisy)
    for y in range(64):
        for x in range(64):
            dx, dy = (x - cx) / 24.0, (y - cy) / 17.0
            r = dx * dx + dy * dy
            if r <= 1.0:
                c = POOL[1] if r > 0.62 else POOL[2] if r > 0.30 else \
                    POOL[3] if r > 0.10 else POOL[4]
                a[y, x] = (*c[:3], 255)
    # rim lip: lit on the north inner edge, ink on the outer
    for x in range(64):
        for y in range(64):
            dx, dy = (x - cx) / 30.0, (y - cy) / 22.0
            r = dx * dx + dy * dy
            if 0.86 <= r <= 1.0 and y < cy:
                a[y, x] = (*BONE[1][:3], 255)
    # outer ink edge of the ring
    for y in range(64):
        for x in range(64):
            if a[y, x, 3] and (x == 0 or y == 0 or not a[y, max(0, x - 1), 3]
                               or not a[y, min(63, x + 1), 3]
                               or not a[max(0, y - 1), x, 3]):
                a[y, x] = (*INKV[:3], 255)
    # ---- the front face: the basin wall's south courses
    fill(a, 6, 44, 57, 56, BASALT[1])
    a[44, 7:57] = BONE[0]
    a[50, 7:57] = BASALT[0]
    outline(a, 6, 44, 57, 56, INKV)
    for fx in (16, 32, 47):
        a[45:56, fx] = BASALT[0]
    # the glow spilling under the south face (the well leaks light)
    a[56, 14:50] = (*POOL[2][:3], 255)
    for (dx2, dy2) in ((12, 58), (51, 58), (20, 60), (44, 60), (32, 61)):
        if a[dy2, dx2, 3] == 0:
            a[dy2, dx2] = np.array([*STARPALE, 120], np.int16)
    # ---- twinkles in the water
    for (sx, sy, al) in ((26, 20, 255), (40, 30, 235), (33, 14, 220),
                         (22, 31, 200), (44, 19, 200)):
        a[sy, sx] = np.array([*STARPALE, al], np.int16)
        for (ddx, ddy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            a[sy + ddy, sx + ddx] = np.array([*STARPALE, 100], np.int16)
    contact_shadow(a, 6, 57, 57)
    return img(a)


def glint_bright(cores: list[tuple[int, int]],
                 satellites: list[tuple[int, int]]) -> Image.Image:
    """1x1 a FALLEN-star glint — brighter than the nightreach sky decals:
    a full-strength core with 2px cross arms."""
    a = np.zeros((16, 16, 4), dtype=np.uint8)
    for (cx, cy) in cores:
        a[cy, cx] = (*STARPALE, 255)
        for d in (1, 2):
            al = 170 if d == 1 else 90
            for (dx, dy) in ((-d, 0), (d, 0), (0, -d), (0, d)):
                if 0 <= cx + dx < 16 and 0 <= cy + dy < 16:
                    a[cy + dy, cx + dx] = (*STARPALE, al)
    for (sx, sy) in satellites:
        a[sy, sx] = (*STARDIM, 150)
    return Image.fromarray(a, "RGBA")


def main() -> None:
    PENUMBRA.mkdir(parents=True, exist_ok=True)
    out = [
        (PENUMBRA / "way_lamp.png", way_lamp()),
        (PENUMBRA / "spire_silhouette.png", spire_silhouette()),
        (PENUMBRA / "starwell_basin.png", starwell_basin()),
        (PENUMBRA / "starglint_bright_a.png",
         glint_bright([(6, 7)], [(12, 12), (11, 3)])),
        (PENUMBRA / "starglint_bright_b.png",
         glint_bright([(10, 9)], [(3, 4), (4, 13)])),
    ]
    for path, im in out:
        im.save(path)
        print(f"  wrote {path.relative_to(REPO)}  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
