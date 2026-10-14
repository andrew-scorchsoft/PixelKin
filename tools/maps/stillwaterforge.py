#!/usr/bin/env python3
"""
stillwaterforge — the DRAWN kit of Stillwater, the Hollowing's village
(walkthrough/11 Part A). Its OWN master folder (like farlampforge/paulforge), so
no other forge's full re-run ever touches it:

    assets/tilesets/stillwater/objects/<stem>.png  ->  packed as `stillwater_<stem>`

The five BUILDINGS in the same folder (quiet_hall, inn, lampmaker, home_a,
home_b) are image-gen masters (gpt-image-2.5 native alpha, front projection,
snapped to a tile multiple) — this script never rewrites them; it only draws the
stems in PIECES.

THE TONE RULE (the Coldfog register, binding): the Hollowing keep their village
the way they keep their lamps: TENDED. Shutters are painted, blankets folded,
nothing broken, nothing menacing. Grey wool, pale stone, iron, a little dim brass.
The only warm colour is behind a shutter that has been opened (after the dawn),
and the one forbidden candle in a jar.

  shut_lamp      1x3  a lamp-post whose lantern is boxed in by two closed grey shutters
  open_lamp      1x3  the same post after the dawn: the shutters swung open, a warm flame
  blanket_kin    2x1  a sleeping kin under a folded grey blanket (ears + tail-tip show)
  blanket_kin_b  2x1  a smaller one, curled the other way
  candle_jar     1x1  the forbidden candle: a stub burning in a stoppered jar
  window_lit     2x2  home_b's upstairs window OPENED, lit, a child at it (post-dawn overlay)
  shutter_wall   4x2  (interior, wall-hung) the shutter-wall: a wall of grey shutters,
                      each with a lamp's name painted small, a dried sprig tucked in one
  hood_rack      2x2  (interior, wall-hung) a rack of hooded dark lamps, capped and tagged
  lamp_bench     2x1  (interior) the lamp-maker's bench: hoods, caps, a half-made shutter
  wool_basket    1x1  (interior) a basket of grey wool / folded blankets

Run:  python3 tools/maps/stillwaterforge.py [--only a,b]
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

from interiorforge import (INK, canvas, contact_shadow, fill, hx, img, outline)

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "assets" / "tilesets" / "stillwater" / "objects"

IRON = [hx("#1c2026"), hx("#343a44"), hx("#4c545e"), hx("#6a7280")]
SHUT = [hx("#3e4452"), hx("#5a6172"), hx("#7a8194"), hx("#9aa1b2")]   # painted shutter grey
WOOL = [hx("#4a4c56"), hx("#6a6c78"), hx("#8c8e9a"), hx("#b0b2bc")]   # grey blanket wool
PALE = [hx("#7e8480"), hx("#9aa09a"), hx("#b8bdb6")]
BRASS = [hx("#5a4a2a"), hx("#8a7440"), hx("#b89a58")]                # dimmed brass
FLAME = [hx("#c85a22"), hx("#ff9a3d"), hx("#ffd27a"), hx("#fff3c8")]
GLOW = hx("#ffcf7a")
GLASS = [hx("#1c2430"), hx("#2c3a4a"), hx("#4a5d70"), hx("#9ab8c0")]
FUR = [hx("#3a3446"), hx("#5a5068"), hx("#7a6e8a")]                    # a dark kin's fur
WOOD = [hx("#2e2620"), hx("#4a3e34"), hx("#6a5a4a")]                  # grey-weathered wood


def _post(a, top: int):
    """The iron post + foot of a 1x3 lamp (16x48), lantern head above `top`."""
    fill(a, 7, top, 8, 44, IRON[1])
    a[top:45, 7] = IRON[2]
    fill(a, 5, 44, 10, 46, IRON[0])
    a[44, 5:11] = IRON[2]
    outline(a, 5, 44, 10, 46, INK)
    contact_shadow(a, 4, 11, 47)


def shut_lamp():
    a = canvas(1, 3)
    _post(a, 16)
    # the lantern box: a cap, then two shutters closed over the glass
    fill(a, 4, 2, 11, 3, IRON[2])                       # the cap
    a[1, 6:10] = IRON[3]
    fill(a, 3, 4, 12, 15, SHUT[1])
    fill(a, 3, 4, 7, 15, SHUT[1])
    a[4:16, 7] = SHUT[0]                                # the meeting line
    a[4:16, 8] = SHUT[0]
    for y in (6, 9, 12):                                # louvres
        a[y, 4:7] = SHUT[2]
        a[y, 9:12] = SHUT[2]
    a[4:16, 3] = SHUT[3]                                # lit left edge
    a[10, 6] = BRASS[2]                                 # the latch, closed
    a[10, 9] = BRASS[1]
    outline(a, 3, 4, 12, 15, INK)
    outline(a, 4, 1, 11, 3, INK)
    return img(a)


def open_lamp():
    a = canvas(1, 3)
    _post(a, 16)
    fill(a, 5, 2, 10, 3, IRON[2])
    a[1, 6:10] = IRON[3]
    outline(a, 5, 1, 10, 3, INK)
    # the glass, lit
    fill(a, 5, 4, 10, 15, FLAME[2])
    fill(a, 6, 6, 9, 13, FLAME[3])
    a[8:12, 7:9] = FLAME[1]
    a[12, 7:9] = FLAME[0]
    outline(a, 5, 4, 10, 15, INK)
    # the two shutters swung open, hanging at the sides (edge-on, thin)
    fill(a, 1, 4, 3, 15, SHUT[1])
    a[4:16, 1] = SHUT[3]
    fill(a, 12, 4, 14, 15, SHUT[0])
    a[4:16, 14] = SHUT[1]
    outline(a, 1, 4, 3, 15, INK)
    outline(a, 12, 4, 14, 15, INK)
    return img(a)


def _blanket(a, x0, x1, top, ears_left: bool):
    """A humped grey blanket over a sleeping kin, folded hem along the bottom."""
    w = x1 - x0
    for x in range(x0, x1 + 1):
        t = (x - x0) / max(1, w)
        h = int(round(7 * (1 - (2 * t - 1) ** 2))) + 3     # a soft hump
        y0 = top + 7 - h + 3
        fill(a, x, y0, x, 13, WOOL[1])
        a[y0, x] = WOOL[3]
        if y0 + 1 <= 13:
            a[y0 + 1, x] = WOOL[2]
        a[y0 - 1, x] = INK
    fill(a, x0, 12, x1, 13, WOOL[0])                    # the folded hem
    a[12, x0:x1 + 1] = WOOL[2]
    for x in range(x0 + 2, x1 - 1, 4):                  # a soft weave
        a[10, x] = WOOL[0]
    a[11:14, x0] = INK
    a[11:14, x1] = INK
    a[14, x0:x1 + 1] = INK
    # who's under it: ears on one end, a tail-tip on the other
    ex = x0 + 3 if ears_left else x1 - 6
    tx = x1 + 1 if ears_left else x0 - 3

    def ridge(x):
        t = (x - x0) / max(1, w)
        return top + 7 - (int(round(7 * (1 - (2 * t - 1) ** 2))) + 3) + 3

    for dx in (0, 3):
        x = ex + dx
        y = ridge(x) - 1                                 # just above the blanket's edge
        fill(a, x, y - 2, x + 1, y, FUR[1])
        a[y - 2, x + 1] = FUR[2]
        a[y - 3, x:x + 2] = INK
        a[y - 2:y + 1, x - 1] = INK
        a[y - 2:y + 1, x + 2] = INK
    fill(a, tx, 11, tx + 2, 13, FUR[1])
    a[11, tx:tx + 3] = FUR[2]
    outline(a, tx, 10, tx + 2, 13, INK)


def blanket_kin():
    a = canvas(2, 1)
    _blanket(a, 4, 26, 0, True)
    contact_shadow(a, 3, 29, 15)
    return img(a)


def blanket_kin_b():
    a = canvas(2, 1)
    _blanket(a, 7, 24, 1, False)
    contact_shadow(a, 3, 28, 15)
    return img(a)


def candle_jar():
    a = canvas(1, 1)
    # a warm halo first (soft, behind)
    for (x, y) in ((4, 4), (11, 4), (3, 7), (12, 7), (4, 10), (11, 10)):
        a[y, x] = hx("#ffcf7a")
        a[y, x, 3] = 110
    fill(a, 5, 4, 10, 14, GLASS[2])
    a[5:14, 5] = GLASS[3]
    fill(a, 6, 3, 9, 3, WOOD[2])                        # the stopper
    fill(a, 7, 9, 8, 13, PALE[2])                       # the stub
    a[8, 7] = FLAME[1]
    a[7, 7:9] = FLAME[2]
    a[6, 7] = FLAME[3]
    outline(a, 5, 4, 10, 14, INK)
    outline(a, 6, 2, 9, 3, INK)
    contact_shadow(a, 4, 11, 15)
    return img(a)


def window_lit():
    """A 2x2 overlay placed at home_b's tile (0,2): its upstairs-left window
    (local px x12-20, y10-18) OPENED — shutters folded back, a lamp lit, a small
    head at the glass. Aligned to that one master's window; nothing else uses it."""
    a = canvas(2, 2)
    x0, y0, x1, y1 = 12, 10, 20, 18
    fill(a, x0, y0, x1, y1, FLAME[2])
    fill(a, x0 + 1, y0 + 1, x1 - 1, y1 - 1, FLAME[3])
    a[y0:y1 + 1, 16] = WOOD[1]                          # mullion
    a[14, x0:x1 + 1] = WOOD[1]
    fill(a, x0 + 1, y1 - 3, x0 + 3, y1 - 1, FUR[1])     # a small head at the glass
    a[y1 - 4, x0 + 1:x0 + 4] = FUR[0]
    outline(a, x0 - 1, y0 - 1, x1 + 1, y1 + 1, INK)
    fill(a, x0 - 6, y0 - 1, x0 - 2, y1 + 1, SHUT[1])   # shutters folded back
    fill(a, x1 + 2, y0 - 1, x1 + 6, y1 + 1, SHUT[1])
    for y in (y0 + 1, y0 + 4, y0 + 7):
        a[y, x0 - 5:x0 - 2] = SHUT[2]
        a[y, x1 + 3:x1 + 6] = SHUT[2]
    outline(a, x0 - 6, y0 - 1, x0 - 2, y1 + 1, INK)
    outline(a, x1 + 2, y0 - 1, x1 + 6, y1 + 1, INK)
    return img(a)


def shutter_wall():
    """4x2 wall-hung: a board of small grey shutters, a name painted on each."""
    a = canvas(4, 2)
    fill(a, 1, 1, 62, 30, WOOD[0])
    outline(a, 0, 0, 63, 31, INK)
    k = 0
    for row, y in enumerate((3, 17)):
        for x in range(3, 60, 10):
            fill(a, x, y, x + 7, y + 11, SHUT[1 + (k % 2)])
            a[y, x:x + 8] = SHUT[3]
            for yy in (y + 3, y + 6):
                a[yy, x + 1:x + 7] = SHUT[0]
            # the painted name: a tiny pale scrawl
            a[y + 9, x + 1:x + 2 + (k * 3) % 5 + 2] = PALE[2]
            outline(a, x, y, x + 7, y + 11, INK)
            k += 1
    # a dried sprig tucked into one shutter (someone remembers)
    a[18:24, 45] = hx("#6a7a4a")
    a[19, 46] = hx("#8a9a5a")
    a[21, 44] = hx("#8a9a5a")
    return img(a)


def hood_rack():
    """2x2 wall-hung: a rail of capped, hooded lamps, each with a paper tag."""
    a = canvas(2, 2)
    fill(a, 1, 3, 30, 4, IRON[2])
    outline(a, 0, 2, 31, 5, INK)
    for cx in (5, 13, 21, 28):
        a[6:8, cx] = IRON[2]
        fill(a, cx - 3, 8, cx + 2, 9, IRON[2])           # the hood
        fill(a, cx - 3, 10, cx + 2, 16, GLASS[0])
        a[10:17, cx - 3] = GLASS[1]
        outline(a, cx - 3, 8, cx + 2, 16, INK)
        fill(a, cx - 1, 18, cx + 1, 21, PALE[2])          # a paper tag
        a[17, cx] = PALE[0]
    fill(a, 2, 24, 29, 27, WOOD[1])                       # a shelf of caps below
    a[24, 2:30] = WOOD[2]
    for cx in (6, 12, 18, 24):
        fill(a, cx, 21, cx + 3, 23, IRON[1])
        outline(a, cx, 21, cx + 3, 23, INK)
    outline(a, 2, 24, 29, 27, INK)
    return img(a)


def lamp_bench():
    a = canvas(2, 1)
    fill(a, 1, 5, 30, 8, WOOD[2])
    a[5, 1:31] = PALE[1]
    fill(a, 2, 9, 4, 14, WOOD[1])
    fill(a, 27, 9, 29, 14, WOOD[1])
    outline(a, 1, 5, 30, 8, INK)
    # on top: a hood, a cap, and a small half-made shutter
    fill(a, 4, 1, 9, 4, IRON[2]); outline(a, 4, 1, 9, 4, INK)
    fill(a, 12, 2, 15, 4, IRON[1]); outline(a, 12, 2, 15, 4, INK)
    fill(a, 19, 0, 26, 4, SHUT[1]); a[2, 20:26] = SHUT[0]; outline(a, 19, 0, 26, 4, INK)
    contact_shadow(a, 1, 30, 15)
    return img(a)


def wool_basket():
    a = canvas(1, 1)
    fill(a, 2, 8, 13, 14, WOOD[1])
    for x in range(3, 13, 2):
        a[9:14, x] = WOOD[2]
    outline(a, 2, 8, 13, 14, INK)
    fill(a, 3, 4, 12, 7, WOOL[2])
    a[4, 4:12] = WOOL[3]
    a[6, 3:13] = WOOL[1]
    outline(a, 3, 3, 12, 8, INK)
    contact_shadow(a, 2, 13, 15)
    return img(a)


PIECES = {
    "shut_lamp": shut_lamp, "open_lamp": open_lamp, "blanket_kin": blanket_kin,
    "blanket_kin_b": blanket_kin_b, "candle_jar": candle_jar, "window_lit": window_lit,
    "shutter_wall": shutter_wall, "hood_rack": hood_rack, "lamp_bench": lamp_bench,
    "wool_basket": wool_basket,
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    want = [s for s in args.only.split(",") if s] or list(PIECES)
    OUT.mkdir(parents=True, exist_ok=True)
    for stem in want:
        im = PIECES[stem]()
        im.save(OUT / f"{stem}.png")
        print(f"  wrote stillwater/objects/{stem}.png  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
