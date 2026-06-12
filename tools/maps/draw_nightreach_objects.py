#!/usr/bin/env python3
"""
draw_nightreach_objects — the W4 NIGHTREACH drawn object kit (the reverent
register: bone + deepBlue + telescope brass, the densest starfield in the
game, near-dawn pallor on the horizon).

Everything here is drawn in code in the deliberate cartridge register of
gbaforge/interiorforge — flat anchors, 1px ink lines, a few placed motifs —
so the star-temple's props sit ON the gold-grass hilltop without ringing.

THE TONE RULE (walkthrough 04-west + README §10, BINDING): Nightreach is the
eighth town — vast, lonely, wondrous, ZERO humour. Every piece is KEPT: the
watch-lamps are polished and waiting (not derelict), the banners hang straight,
the vigil lamps are small and brave under an enormous sky. The only warmth is
brass and the pale silver-gold of a watch-flame; everything else is bone stone
and deep indigo night.

Pieces:
  watch_lamp_dark  2x3  one of the seven Astral Walk watch-lamps, UNLIT: a bone
                        pillar, brass collar, faceted glass bell holding dark.
                        Grander than Pale Vault's 1x2 bracket — these are the
                        town's whole liturgy. (Dark/lit MapObject swap pair.)
  watch_lamp_lit   2x3  the same lamp answered: a pale silver-gold watch-flame
                        and a soft starlight halo.
  star_banner      1x2  temple-step dressing: an indigo banner on a brass-shod
                        pole, carrying a five-star constellation figure.
  vigil_lamp       1x2  a small standing star-lantern, lit — the Star-vigil's
                        hand-lamps set out along the temple steps.
  eyepiece         3x3  THE GREAT EYEPIECE (the Lumenary's interior focal): the
                        observatory telescope's lower barrel descending to a
                        brass eyepiece head over a stepped bone dais. Top-down-
                        frontal split per interiors.md (top surface + front
                        strip, 1px ink outline, contact shadow).
  starglint_a/b    1x1  the DENSE starfield glint decals — the windward glints'
                        denser sibling (a twinkle cluster, not a lone star),
                        scattered over the town's dark border canopy/cliff so
                        the map reads as the densest diamond starfield in the
                        game. Non-solid 1x1 objects, very low alpha.
  lumenary.png     6x7  drawn FALLBACK for the domed observatory hall (written
                        only if the image-gen hero master is absent — the
                        solarium-lumenary precedent).

Writes  assets/tilesets/nightreach/objects/*.png  -> nightreach_<stem> keys
Then run .claude/skills/generate-sprite-sheet/scripts/pack_objects.py.

Run:  ./venv/bin/python tools/maps/draw_nightreach_objects.py
"""
from __future__ import annotations

import numpy as np
from pathlib import Path

from interiorforge import (BRASS, INK, canvas, contact_shadow, fill, hx, img,
                           outline)

REPO = Path(__file__).resolve().parents[2]
NIGHTREACH = REPO / "assets" / "tilesets" / "nightreach" / "objects"

# ---- the W4 register (bone + deepBlue + telescope brass + starlight) ---------------
BONE = [hx("#5a5660"), hx("#8c8694"), hx("#b8b2ba"), hx("#dcd6d2"), hx("#f0ece2")]
INDIGO = [hx("#141a30"), hx("#1f2a4a"), hx("#2c3c66"), hx("#41548a")]
DARKGLASS = [hx("#10141f"), hx("#1b2436"), hx("#2c3a52")]   # a bell holding dark
FLAME = [hx("#b89a52"), hx("#e8d292"), hx("#fff4ce"), hx("#fffdf2")]  # watch-flame
STARPALE = (207, 232, 255)   # starlight white-blue (windward glint anchor)
STARDIM = (140, 170, 214)
BRASSC = [BRASS[0], BRASS[1], BRASS[2], BRASS[3]]


def _lamp_body(a):
    """The shared watch-lamp body on a 32x48 canvas: stepped bone base,
    slender pillar, brass collar, the faceted glass bell. Returns the bell's
    interior box (x0, y0, x1, y1) for the dark/lit variants to fill."""
    # stepped base (kept, swept)
    fill(a, 6, 42, 25, 46, BONE[1])
    a[42, 7:25] = BONE[3]
    outline(a, 6, 42, 25, 46, INK)
    fill(a, 9, 38, 22, 42, BONE[2])
    a[38, 10:22] = BONE[4]
    outline(a, 9, 38, 22, 42, INK)
    # the pillar
    fill(a, 13, 20, 18, 38, BONE[2])
    a[20:38, 13] = BONE[3]
    a[20:38, 18] = BONE[0]
    outline(a, 13, 20, 18, 38, INK)
    a[24, 14:18] = BONE[0]               # a course line
    a[31, 14:18] = BONE[0]
    # the brass collar the bell sits in
    fill(a, 10, 16, 21, 20, BRASSC[2])
    a[16, 11:21] = BRASSC[3]
    a[19, 11:21] = BRASSC[1]
    outline(a, 10, 16, 21, 20, INK)
    # the bell (faceted glass, drawn as the variant's box)
    fill(a, 9, 5, 22, 16, DARKGLASS[1])
    a[5:16, 9] = DARKGLASS[2]            # cold left gleam
    a[5:16, 22] = DARKGLASS[0]
    a[5, 9:23] = DARKGLASS[2]
    outline(a, 9, 5, 22, 16, INK)
    a[5:16, 15] = DARKGLASS[0]           # the facet seam
    # the brass crown + star finial
    fill(a, 12, 2, 19, 5, BRASSC[2])
    a[2, 13:19] = BRASSC[3]
    outline(a, 12, 2, 19, 5, INK)
    a[0:2, 15:17] = BRASSC[3]
    contact_shadow(a, 5, 26, 47)
    return (10, 6, 21, 14)


def watch_lamp_dark():
    a = canvas(2, 3)
    x0, y0, x1, y1 = _lamp_body(a)
    # the wick asleep, the glass holding only night
    a[(y0 + y1) // 2, (x0 + x1) // 2] = hx("#8c8678")
    return img(a)


def watch_lamp_lit():
    a = canvas(2, 3)
    x0, y0, x1, y1 = _lamp_body(a)
    cx = (x0 + x1) // 2
    # the watch-flame: pale silver-gold, narrow and steady
    fill(a, cx - 2, y0 + 1, cx + 2, y1 - 1, FLAME[1])
    fill(a, cx - 1, y0 + 2, cx + 1, y1 - 2, FLAME[2])
    a[y0 + 3:y1 - 2, cx] = FLAME[3]
    # glass warmed around it
    a[y0:y1 + 1, x0 - 1] = INDIGO[3]
    # a soft starlight halo above the finial (low alpha, over transparent)
    for (dx, dy) in ((-4, 2), (4, 2), (0, 0), (-7, 5), (7, 5)):
        x, y = 15 + dx, 1 + dy
        if a[y, x, 3] == 0:
            a[y, x] = np.array([*STARPALE, 120], np.int16)
    return img(a)


def star_banner():
    """1x2 temple-step banner: brass-shod pole, indigo banner, a five-star
    constellation figure stitched in pale thread."""
    a = canvas(1, 2)
    # the pole
    a[2:30, 7] = BRASSC[1]
    a[2:30, 8] = BRASSC[0]
    a[2, 6:10] = BRASSC[3]               # the cap
    fill(a, 5, 28, 10, 30, BONE[1])      # the foot
    outline(a, 5, 28, 10, 30, INK)
    # the cross-arm + hanging banner
    a[4, 2:14] = BRASSC[2]
    fill(a, 2, 5, 13, 22, INDIGO[1])
    a[5:23, 2] = INDIGO[2]
    a[5:23, 13] = INDIGO[0]
    outline(a, 2, 5, 13, 22, INK)
    a[22, 3:13:3] = INDIGO[0]            # the fringe
    # the constellation figure (five stars + thread lines)
    pts = [(5, 8), (9, 10), (7, 13), (4, 16), (10, 17)]
    for (x, y) in pts:
        a[y, x] = np.array([*STARPALE, 255], np.int16)
    a[11, 8] = np.array([*STARDIM, 200], np.int16)
    a[15, 6] = np.array([*STARDIM, 200], np.int16)
    contact_shadow(a, 4, 11, 31)
    return img(a)


def vigil_lamp():
    """1x2 a small standing star-lantern, lit — brave under a huge sky."""
    a = canvas(1, 2)
    # the stand
    a[18:28, 7] = BONE[1]
    a[18:28, 8] = BONE[0]
    fill(a, 4, 28, 11, 30, BONE[1])
    outline(a, 4, 28, 11, 30, INK)
    # the lantern box
    fill(a, 3, 8, 12, 18, INDIGO[1])
    outline(a, 3, 8, 12, 18, INK)
    fill(a, 5, 10, 10, 16, FLAME[1])
    fill(a, 6, 11, 9, 15, FLAME[2])
    a[12:15, 7] = FLAME[3]
    a[8, 5:11] = INDIGO[2]
    # brass hood + ring
    fill(a, 4, 5, 11, 8, BRASSC[2])
    a[5, 5:11] = BRASSC[3]
    outline(a, 4, 5, 11, 8, INK)
    a[2:5, 7:9] = BRASSC[1]
    contact_shadow(a, 3, 12, 31)
    return img(a)


def eyepiece():
    """3x3 THE GREAT EYEPIECE — the telescope's lower barrel descending out of
    the dome above to a brass eyepiece head over a stepped bone dais."""
    a = canvas(3, 3)
    # the stepped dais (top surface + front strip — the free-standing split)
    fill(a, 2, 34, 45, 41, BONE[2])      # top surface
    a[34, 3:45] = BONE[4]
    fill(a, 2, 41, 45, 46, BONE[1])      # front strip
    a[41, 3:45] = BONE[0]
    outline(a, 2, 34, 45, 46, INK)
    fill(a, 8, 28, 39, 34, BONE[2])      # upper step
    a[28, 9:39] = BONE[3]
    outline(a, 8, 28, 39, 34, INK)
    # the mount column
    fill(a, 20, 18, 27, 28, BRASSC[1])
    a[18:28, 20] = BRASSC[2]
    outline(a, 20, 18, 27, 28, INK)
    # the great barrel, descending from the upper-right (toward the dome slit)
    for step in range(16):
        x0 = 26 + step
        y0 = 16 - step
        if 0 <= y0 - 3 and x0 + 3 < 48:
            fill(a, x0, max(0, y0 - 3), min(47, x0 + 3), y0, INDIGO[2])
            a[max(0, y0 - 3), x0] = INDIGO[3]
            a[y0, min(47, x0 + 3)] = INDIGO[0]
    # barrel rings
    for step in (2, 8, 14):
        x0 = 26 + step
        y0 = 16 - step
        a[max(0, y0 - 3):y0 + 1, x0] = BRASSC[2]
    # the open aperture ring at the top corner
    a[0:3, 44:48] = BRASSC[1]
    a[0, 45:48] = BRASSC[3]
    # the eyepiece head: a brass drum facing the player, dark lens
    fill(a, 16, 8, 31, 20, BRASSC[2])
    a[8, 17:31] = BRASSC[3]
    a[19, 17:31] = BRASSC[0]
    outline(a, 16, 8, 31, 20, INK)
    fill(a, 20, 11, 27, 17, DARKGLASS[0])
    a[12, 21:23] = np.array([*STARPALE, 230], np.int16)   # a held star in the lens
    outline(a, 20, 11, 27, 17, INK)
    # the focus wheel + chart hooks
    fill(a, 12, 12, 15, 16, BRASSC[1])
    outline(a, 12, 12, 15, 16, INK)
    a[22, 6:12] = BRASSC[1]              # the seat rail west
    a[22:28, 6] = BRASSC[1]
    contact_shadow(a, 2, 45, 47)
    return img(a)


def glint(cores: list[tuple[int, int]], satellites: list[tuple[int, int]]):
    """A DENSE star-glint: a small twinkle cluster (the densest starfield in
    the game wants clusters, not lone points)."""
    a = np.zeros((16, 16, 4), dtype=np.uint8)
    for (cx, cy) in cores:
        a[cy, cx] = (*STARPALE, 235)
        for (dx, dy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if 0 <= cx + dx < 16 and 0 <= cy + dy < 16:
                a[cy + dy, cx + dx] = (*STARPALE, 110)
    for (sx, sy) in satellites:
        a[sy, sx] = (*STARDIM, 140)
    return Image_from(a)


def Image_from(a):
    from PIL import Image
    return Image.fromarray(a, "RGBA")


def lumenary_fallback():
    """6x7 drawn fallback for the domed observatory hall (only written if the
    image-gen hero master is absent — the solarium-lumenary precedent).
    A deep-indigo dome with a brass observing slit and the great barrel tip,
    on a bone drum over a pilastered temple face; tall brass double door at
    local cols 2-3, bottom row."""
    a = canvas(6, 7)
    W, H = 96, 112
    # temple body
    fill(a, 4, 56, 91, 109, BONE[2])
    outline(a, 4, 56, 91, 109, INK)
    # the drum cornice
    fill(a, 2, 48, 93, 57, BONE[1])
    a[48, 3:93] = BONE[3]
    outline(a, 2, 48, 93, 57, INK)
    # THE DOME (deep indigo, ribbed, starlit)
    for y in range(10, 48):
        t = (47 - y) / 38.0
        span = int(42 * (1 - t * t) ** 0.5) + 4
        fill(a, 48 - span, y, 47 + span, y, INDIGO[1])
        a[y, 48 - span] = INDIGO[3]
        a[y, 47 + span] = INDIGO[0]
    for rx in (20, 34, 61, 75):          # dome ribs
        a[14:48, rx] = INDIGO[2]
    outlineless_top = True
    # the observing SLIT, open, with the barrel tip looking out
    fill(a, 42, 10, 53, 34, DARKGLASS[0])
    outline(a, 42, 10, 53, 34, BRASSC[1])
    fill(a, 45, 14, 50, 22, BRASSC[2])   # the barrel tip
    a[14, 46:50] = BRASSC[3]
    a[22, 46:50] = BRASSC[0]
    # dome stars (the temple wears the sky)
    for (sx, sy) in ((26, 22), (66, 18), (74, 30), (22, 36), (60, 40), (33, 14)):
        a[sy, sx] = np.array([*STARPALE, 220], np.int16)
    # the crown finial
    a[4:10, 46:50] = BRASSC[1]
    a[4, 47:49] = BRASSC[3]
    a[2:4, 47:49] = np.array([*STARPALE, 235], np.int16)
    # face: pilasters + lit indigo windows + the tall brass double door
    for px in (8, 26, 68, 86):
        a[58:108, px] = BONE[3]
        a[58:108, px + 1] = BONE[0]
    for wx in (14, 74):                  # two tall windows, watch-flame lit
        fill(a, wx, 64, wx + 7, 80, INDIGO[1])
        fill(a, wx + 2, 67, wx + 5, 77, FLAME[1])
        a[70:75, wx + 3] = FLAME[2]
        outline(a, wx, 64, wx + 7, 80, INK)
    # the door (tiles 2-3: px 32..63), recessed, brass leaves
    fill(a, 33, 62, 62, 108, DARKGLASS[0])
    fill(a, 35, 64, 47, 108, BRASSC[1])
    fill(a, 48, 64, 60, 108, BRASSC[1])
    a[64:109, 47] = BRASSC[0]
    a[64:109, 48] = BRASSC[2]
    a[64, 35:61] = BRASSC[2]
    for dy in (70, 82, 94):              # door panels
        a[dy, 37:46] = BRASSC[0]
        a[dy, 50:59] = BRASSC[0]
    fill(a, 40, 86, 44, 87, BRASSC[3])   # pulls
    fill(a, 51, 86, 55, 87, BRASSC[3])
    outline(a, 33, 62, 62, 108, INK)
    # a swept bone step
    fill(a, 31, 109, 64, 111, BONE[3])
    outline(a, 31, 109, 64, 111, INK)
    # course lines on the body
    for cy in (72, 88, 102):
        a[cy, 5:8] = BONE[0]
        a[cy, 88:91] = BONE[0]
    contact_shadow(a, 4, 91, 110)
    return img(a)


def main() -> None:
    NIGHTREACH.mkdir(parents=True, exist_ok=True)
    out = [
        (NIGHTREACH / "watch_lamp_dark.png", watch_lamp_dark()),
        (NIGHTREACH / "watch_lamp_lit.png", watch_lamp_lit()),
        (NIGHTREACH / "star_banner.png", star_banner()),
        (NIGHTREACH / "vigil_lamp.png", vigil_lamp()),
        (NIGHTREACH / "eyepiece.png", eyepiece()),
        (NIGHTREACH / "starglint_a.png",
         glint([(4, 5), (11, 9)], [(8, 2), (13, 13), (2, 12)])),
        (NIGHTREACH / "starglint_b.png",
         glint([(10, 4), (5, 12)], [(13, 8), (2, 3), (8, 14)])),
    ]
    hall = NIGHTREACH / "lumenary.png"
    if not hall.exists():
        out.append((hall, lumenary_fallback()))
    for path, im in out:
        im.save(path)
        print(f"  wrote {path.relative_to(REPO)}  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
