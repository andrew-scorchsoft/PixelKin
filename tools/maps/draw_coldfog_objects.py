#!/usr/bin/env python3
"""
draw_coldfog_objects — the W3 COLDFOG drawn object kit (the dread register).

The Coldfog Marches / Drownlight Beacon / Hollowfen Stillworks cluster needs a
bespoke prop set (CLAUDE.md: generate or draw — never reuse another town's
hall). Everything here is drawn in code in the deliberate cartridge register of
gbaforge/interiorforge — flat anchors, 1px ink lines, a few placed motifs —
keyed to gbaforge's BLIGHT/MURK anchors so the props sit ON the drained ground
without ringing.

THE TONE RULE (walkthrough README §10 + 04-west, BINDING): the Hollowing's
works are grief dressed as mercy — TENDED, never broken. Every piece is clean,
straight, cared-for: polished brass collars on dead lanterns, a swept plinth
under the draining engine, bedrolls rolled and stacked square. Nothing burnt,
nothing smashed, no skulls, no menace — the horror is the CARE. The only warm
colour in the whole kit is the faint brass of the fittings; every glass is
lightless.

Pieces:
  null_rack    4x2  rows of dead null-lanterns on an iron gantry (the works'
                    galleries; also II's roadside racks)
  works_front  6x5  the Hollowfen Stillworks facade (the landmark on Coldfog
                    II; double door at local cols 2-3, bottom row)
  null_engine  6x5  the light-draining machinery — the works' centrepiece: a
                    bell of held dark on a swept plinth, cradle pipes feeding
                    lantern cradles, a gauge resting at zero. Merciful-and-
                    wrong: it reads as a FONT, not a weapon.
  lighthouse   4x7  the Drownlight Beacon tower — snuffed lamp room, waterline
                    stain, a door swollen shut
  quiet_camp   3x2  a quieted camp vignette: bedrolls rolled square, a doused
                    fire-ring, a hand-lantern set out neat (nobody hurried)

Writes  assets/tilesets/coldfog/objects/*.png  -> coldfog_<stem> manifest keys
Then run .claude/skills/generate-sprite-sheet/scripts/pack_objects.py.

Run:  ./venv/bin/python tools/maps/draw_coldfog_objects.py
"""
from __future__ import annotations

import numpy as np
from pathlib import Path

from interiorforge import (BRASS, INK, canvas, contact_shadow, fill, hx, img,
                           outline)

REPO = Path(__file__).resolve().parents[2]
COLDFOG = REPO / "assets" / "tilesets" / "coldfog" / "objects"

# ---- the W3 register (keyed to gbaforge BLIGHT (90,96,92) / MURK (52,64,72)) -------
IRON = [hx("#1c2026"), hx("#343a44"), hx("#4c545e"), hx("#6a7280")]    # tended iron
SLATE = [hx("#252a36"), hx("#3a4150"), hx("#525a6c"), hx("#737c90")]   # works slate
PALE = [hx("#7e8480"), hx("#9aa09a"), hx("#b8bdb6")]                   # ash-pale stone
DARKGLASS = [hx("#10141c"), hx("#1c2430"), hx("#2c3a4a")]              # lightless glass
WICK = hx("#8c8678")                                                   # the grey wick
BRASSC = [BRASS[0], BRASS[1], hx("#b89a48")]                           # dimmed brass


def _hang_lantern(a, cx, top):
    """One dead null-lantern: a bell of dark glass under a polished brass
    collar, the grey wick just visible. 7px wide, 10px tall from `top`."""
    a[top:top + 2, cx] = IRON[2]                       # the hook
    fill(a, cx - 2, top + 2, cx + 2, top + 3, BRASSC[2])   # the tended collar
    a[top + 2, cx - 1:cx + 2] = BRASSC[1]
    fill(a, cx - 3, top + 4, cx + 3, top + 8, DARKGLASS[1])
    a[top + 4:top + 9, cx - 3] = DARKGLASS[2]          # a cold left gleam
    a[top + 9, cx - 2:cx + 3] = DARKGLASS[0]           # the bell's foot
    a[top + 6, cx] = WICK                              # the wick, asleep


def null_rack():
    """4x2 a gantry of four dead null-lanterns — the Stillworks' galleries in
    one piece. Iron rail, square posts, every bell dark, every collar bright."""
    a = canvas(4, 2)
    # posts + rail
    fill(a, 2, 6, 4, 29, IRON[1])
    a[6:30, 2] = IRON[2]
    fill(a, 59, 6, 61, 29, IRON[1])
    a[6:30, 59] = IRON[2]
    fill(a, 0, 4, 63, 6, IRON[2])                      # the rail
    a[4, 0:64] = IRON[3]
    outline(a, 0, 4, 63, 6, INK)
    # feet
    fill(a, 0, 28, 6, 29, IRON[0])
    fill(a, 57, 28, 63, 29, IRON[0])
    # four bells, evenly tended
    for cx in (10, 24, 39, 53):
        _hang_lantern(a, cx, 7)
    contact_shadow(a, 1, 62, 30)
    return img(a)


def works_front():
    """6x5 the Hollowfen Stillworks facade: a long low null-works hall, slate
    roof, iron-banded face, a lintel row of dark port-lights, one tall double
    door (local cols 2-3, bottom row). Clean lines, swept step — tended."""
    a = canvas(6, 5)
    # hall body
    fill(a, 2, 26, 93, 77, SLATE[1])
    outline(a, 2, 26, 93, 77, INK)
    # the shallow slate roof + cornice
    fill(a, 0, 14, 95, 27, SLATE[2])
    a[14, 0:96] = SLATE[3]
    a[26, 0:96] = SLATE[0]
    outline(a, 0, 14, 95, 27, INK)
    for rx in range(8, 96, 12):                        # roof seams, dead straight
        a[15:26, rx] = SLATE[1]
    # iron bands down the face
    for px in (8, 28, 66, 86):
        a[28:77, px] = IRON[1]
        a[28:77, px + 1] = IRON[0]
    # the lintel row of port-lights — every one dark
    for cx in range(14, 84, 10):
        fill(a, cx, 32, cx + 4, 36, DARKGLASS[1])
        a[32, cx + 1:cx + 4] = DARKGLASS[2]
        outline(a, cx, 32, cx + 4, 36, IRON[0])
    # the tall double door (tiles 2-3: px 32..63), recessed, brass-fitted
    fill(a, 34, 42, 61, 76, DARKGLASS[0])              # recess
    fill(a, 36, 44, 47, 76, IRON[1])                   # left leaf
    fill(a, 48, 44, 59, 76, IRON[1])
    a[44:77, 47] = IRON[0]
    a[44:77, 48] = IRON[2]
    a[44, 36:60] = IRON[2]
    fill(a, 44, 58, 51, 59, BRASSC[2])                 # the polished pull-bar
    fill(a, 52, 58, 59, 59, BRASSC[1])
    outline(a, 34, 42, 61, 76, INK)
    # a swept stone step under the door
    fill(a, 32, 77, 63, 79, PALE[1])
    a[77, 33:63] = PALE[2]
    outline(a, 32, 77, 63, 79, INK)
    # two wall-bracket null-lanterns flanking the door
    for cx in (22, 73):
        _hang_lantern(a, cx, 46)
    contact_shadow(a, 2, 93, 78)
    return img(a)


def null_engine():
    """6x5 the draining machinery — the Great Null's working model. A bell of
    HELD DARK on a swept stepped plinth; brass cradle-pipes curve down into two
    lantern cradles; the gauge face rests at zero. It reads as a font someone
    polishes every day — merciful, and wrong."""
    a = canvas(6, 5)
    # swept stepped plinth
    fill(a, 6, 66, 89, 77, PALE[1])
    a[66, 7:89] = PALE[2]
    outline(a, 6, 66, 89, 77, INK)
    fill(a, 14, 58, 81, 66, SLATE[1])
    a[58, 15:81] = SLATE[2]
    outline(a, 14, 58, 81, 66, INK)
    # the bell of held dark (an inverted glass dome, lightless)
    for y in range(14, 58):
        t = (y - 14) / 43.0
        span = int(26 * (t ** 0.5)) + 6
        fill(a, 48 - span, y, 47 + span, y, DARKGLASS[1])
        a[y, 48 - span] = DARKGLASS[2]
        a[y, 47 + span] = DARKGLASS[0]
    # the dark inside the dark: the held null, denser at the heart
    fill(a, 38, 30, 57, 52, DARKGLASS[0])
    a[34:50, 46:50] = hx("#070a10")
    # brass crown-collar + finial — tended daily
    fill(a, 40, 10, 55, 14, BRASSC[2])
    a[10, 41:55] = BRASSC[1]
    outline(a, 40, 10, 55, 14, INK)
    a[6:10, 46:50] = BRASSC[1]
    a[6, 47:49] = BRASSC[2]
    # cradle-pipes arcing down into the side cradles
    for step in range(14):                              # left pipe
        x = 21 - step
        y = 30 + (step * step) // 7
        a[y:y + 3, x] = BRASSC[1]
        a[y, x] = BRASSC[2]
    for step in range(14):                              # right pipe
        x = 74 + step
        y = 30 + (step * step) // 7
        a[y:y + 3, x] = BRASSC[1]
        a[y, x] = BRASSC[2]
    # the two lantern cradles, each holding one small dark lamp
    for cx in (8, 80):
        fill(a, cx, 56, cx + 7, 65, IRON[1])
        a[56, cx + 1:cx + 7] = IRON[2]
        outline(a, cx, 56, cx + 7, 65, INK)
        fill(a, cx + 2, 58, cx + 5, 62, DARKGLASS[1])
        a[60, cx + 3] = WICK
    # the gauge face, resting at zero (needle straight down)
    fill(a, 43, 60, 52, 65, PALE[2])
    outline(a, 43, 60, 52, 65, IRON[0])
    a[62:65, 47] = IRON[0]                              # the needle: zero
    contact_shadow(a, 6, 89, 78)
    return img(a)


def lighthouse():
    """4x7 the Drownlight Beacon: a snuffed lighthouse on the dead shallows.
    Pale courses gone grey, a waterline stain climbing the base, the lamp room
    glass dark, the gallery rail intact — nothing broken, only out."""
    a = canvas(4, 7)
    # tower body, tapering
    for y in range(34, 104):
        t = (y - 34) / 70.0
        half = int(14 + 8 * t)
        fill(a, 32 - half, y, 31 + half, y, PALE[1])
        a[y, 32 - half] = PALE[2]
        a[y, 31 + half] = PALE[0]
    # stone courses (straight, kept)
    for cy in range(40, 100, 9):
        t = (cy - 34) / 70.0
        half = int(14 + 8 * t) - 1
        a[cy, 32 - half:32 + half] = PALE[0]
    # the waterline stain (the drowned base)
    stain = np.array([58, 66, 70, 255], np.int16)
    for y in range(90, 104):
        half = int(14 + 8 * ((y - 34) / 70.0)) - 1
        a[y, 33 - half:31 + half, :3] = (a[y, 33 - half:31 + half, :3] * 0.55
                                         + stain[:3] * 0.45).astype(np.int16)
    # gallery deck + rail
    fill(a, 10, 30, 53, 34, SLATE[1])
    a[30, 11:53] = SLATE[2]
    outline(a, 10, 30, 53, 34, INK)
    for rx in range(12, 52, 4):
        a[24:30, rx] = IRON[2]
    a[24, 11:53] = IRON[2]
    # the lamp room — glass DARK
    fill(a, 18, 10, 45, 24, DARKGLASS[1])
    a[10:24, 19] = DARKGLASS[2]
    for mx in (26, 37):
        a[10:24, mx] = IRON[1]
    outline(a, 18, 10, 45, 24, INK)
    a[16, 31] = WICK                                    # the great wick, asleep
    # the cap + vane
    fill(a, 16, 6, 47, 10, SLATE[2])
    outline(a, 16, 6, 47, 10, INK)
    a[2:6, 31:33] = IRON[2]
    # the door, swollen shut (no light under it)
    fill(a, 26, 88, 37, 103, IRON[1])
    a[88, 27:37] = IRON[2]
    outline(a, 26, 88, 37, 103, INK)
    a[94, 34] = BRASSC[1]                               # the one dull fitting
    contact_shadow(a, 12, 51, 104)
    return img(a)


def quiet_camp():
    """3x2 the quieted camp: two bedrolls rolled SQUARE and stacked, a doused
    fire-ring swept of embers, a hand-lantern set out neat on a flat stone.
    Nobody hurried. Nobody was hurt. That's the unsettling part."""
    a = canvas(3, 2)
    # the swept ground-cloth
    fill(a, 2, 14, 45, 29, SLATE[1])
    a[14, 3:45] = SLATE[2]
    outline(a, 2, 14, 45, 29, INK)
    # two bedrolls, rolled square, stacked at the left
    for (bx, by) in ((5, 17), (5, 23)):
        fill(a, bx, by, bx + 13, by + 4, PALE[1])
        a[by, bx + 1:bx + 13] = PALE[2]
        a[by:by + 5, bx + 3] = PALE[0]                  # the tie
        a[by:by + 5, bx + 10] = PALE[0]
        outline(a, bx, by, bx + 13, by + 4, INK)
    # the fire-ring, doused and swept (grey ash, no char)
    for (dx, dy) in ((0, -4), (3, -3), (4, 0), (3, 3), (0, 4), (-3, 3), (-4, 0), (-3, -3)):
        fill(a, 30 + dx, 21 + dy, 31 + dx, 22 + dy, IRON[2])
    fill(a, 29, 20, 32, 23, hx("#5e605c"))              # cold ash
    a[21, 30:32] = hx("#777a74")
    # the hand-lantern on its flat stone, set out neat
    fill(a, 39, 22, 44, 25, PALE[1])
    outline(a, 39, 22, 44, 25, INK)
    fill(a, 40, 16, 43, 21, DARKGLASS[1])
    a[15, 41:43] = BRASSC[1]
    a[18, 41] = WICK
    contact_shadow(a, 3, 44, 30)
    return img(a)


def main() -> None:
    COLDFOG.mkdir(parents=True, exist_ok=True)
    out = [
        (COLDFOG / "null_rack.png", null_rack()),
        (COLDFOG / "works_front.png", works_front()),
        (COLDFOG / "null_engine.png", null_engine()),
        (COLDFOG / "lighthouse.png", lighthouse()),
        (COLDFOG / "quiet_camp.png", quiet_camp()),
    ]
    for path, im in out:
        im.save(path)
        print(f"  wrote {path.relative_to(REPO)}  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
