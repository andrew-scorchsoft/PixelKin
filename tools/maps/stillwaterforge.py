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
  -- the 2026-10 fix pass --
  hearth_banked  3x3  (interior, wall) interior_hearth with a louvred fire-screen
                      latched over it: the hearth "with its face to the wall"
                      (flag-paired with the open hearth, which returns at dawn)
  waystone       1x2  the village lamp-stone (TRAVEL), its lantern shuttered
  crag_boulders  2x2  slate boulders for the crag rim
  wash_line      3x2  grey blankets aired on a line between two posts
  woodpile       2x1  a tidy log stack under a slate hood
  punt           2x1  the last fishing punt, moored on the mere
  kin_basket     2x1  (interior) home A: Old Bracken asleep in his basket
  spinning_wheel 2x2  (interior) home B: Maren's wheel, grey wool on the distaff
  candle_sill    1x1  (interior) home B: the candle kept on the child's shelf
  old_chairs     2x1  (interior) home A: two chairs with their backs to the hearth

Run:  python3 tools/maps/stillwaterforge.py [--only a,b]
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

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
    """4x2 wall-hung: a board of small PAINTED, LOUVRED grey shutters (pale paint,
    slatted, each with a little brass name-plate), a few dried sprigs tucked into
    the louvres. Pale on purpose: it must read as painted wood, never as black
    window glass (the 2026-10 review)."""
    a = canvas(4, 2)
    BOARD = [hx("#3a3632"), hx("#5e5850"), hx("#7c756a")]           # weathered rail
    fill(a, 0, 0, 63, 31, BOARD[1])
    a[0, 0:64] = BOARD[2]
    for y in (15, 16):                                             # the middle rail
        a[y, 0:64] = BOARD[0]
    outline(a, 0, 0, 63, 31, INK)
    PAINT = [hx("#5c6478"), hx("#7c8498"), hx("#9ea6b8"), hx("#c4cad6")]  # painted shutter
    k = 0
    for y in (2, 18):
        for x in range(2, 62, 10):
            w, h = 8, 12
            shade = 0 if k % 3 else 1                              # not all freshly painted
            fill(a, x, y, x + w - 1, y + h - 1, PAINT[1 + shade])
            a[y:y + h, x] = PAINT[3]                               # lit stile
            a[y:y + h, x + w - 1] = PAINT[0]
            a[y, x:x + w] = PAINT[3]
            # the louvres: slat (pale) over shadow (dark), every 2px below the plate
            for yy in range(y + 4, y + h - 1, 2):
                a[yy, x + 1:x + w - 1] = PAINT[2 + shade]
                a[yy + 1, x + 1:x + w - 1] = PAINT[0]
            # the name-plate: a small brass slip with a painted scrawl
            fill(a, x + 1, y + 1, x + w - 2, y + 2, BRASS[2])
            a[y + 2, x + 2:x + 3 + (k * 3) % 4] = BRASS[0]
            outline(a, x, y, x + w - 1, y + h - 1, INK)
            k += 1
    # dried sprigs tucked into three of the louvres (someone remembers)
    for (sx, sy) in ((26, 7), (45, 22), (6, 23)):
        a[sy:sy + 5, sx] = hx("#6a7a4a")
        a[sy + 1, sx + 1] = hx("#9aaa62")
        a[sy + 3, sx - 1] = hx("#9aaa62")
        a[sy, sx] = hx("#c8b070")
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


# ---- the 2026-10 fix pass (Part A review): hearths, homes, the yards, the mere ----
def _ink_rim(a):
    """Ink every opaque pixel that touches transparency (a crisp silhouette)."""
    op = a[..., 3] > 0
    edge = np.zeros_like(op)
    edge[1:, :] |= ~op[:-1, :]
    edge[:-1, :] |= ~op[1:, :]
    edge[:, 1:] |= ~op[:, :-1]
    edge[:, :-1] |= ~op[:, 1:]
    edge[0, :] = edge[-1, :] = True
    edge[:, 0] = edge[:, -1] = True
    a[op & edge] = INK


def hearth_banked():
    """3x3 WALL piece, the SAME footprint + silhouette as interior_hearth: the
    village's hearth with its face to the wall — the firebox closed by a painted,
    louvred fire-screen, latched; only a thread of ember-light at the seams, the
    mantel candles snuffed. (The open hearth swaps back in at flag:dawn.)"""
    src = Image.open(REPO / "assets/tilesets/interior/objects/hearth.png").convert("RGBA")
    a = np.asarray(src).astype("int16").copy()
    # the mantel candles snuffed first (their warm halos go cold grey)
    top_rows = a[:26]
    flame = (top_rows[..., 0] > 200) & (top_rows[..., 1] > 140) & (top_rows[..., 2] < 150)
    top_rows[flame] = np.array([206, 200, 186, 255], np.int16)   # bare wax, no flame
    glow = (top_rows[..., 0] > 140) & (top_rows[..., 0] > top_rows[..., 2] + 30) & ~flame
    top_rows[glow, :3] = (top_rows[glow, :3] * np.array([0.62, 0.72, 0.95])).astype(np.int16) + 18
    PAINT = [hx("#4a5062"), hx("#666e82"), hx("#8a92a6"), hx("#b0b8c8")]
    cx, top, bot, x0, x1 = 23.5, 29, 45, 12, 35
    cells = []
    for y in range(top, bot + 1):
        for x in range(x0, x1 + 1):
            if y < 34 and (x - cx) ** 2 / 12.5 ** 2 + (y - 34) ** 2 / 5.5 ** 2 > 1:
                continue
            cells.append((y, x))
            a[y, x] = PAINT[1]
    for y in range(top + 6, bot - 1, 2):                     # the louvres
        for x in range(x0 + 1, x1):
            if (y, x) in cells:
                a[y, x] = PAINT[2]
                a[y + 1, x] = PAINT[0]
    for y in range(top, bot + 1):                            # where the leaves meet
        a[y, 23] = PAINT[0]
        a[y, 24] = PAINT[3]
    a[38:40, 22] = BRASS[2]                                  # the latch, shut
    a[38:40, 25] = BRASS[1]
    cs = set(cells)
    for (y, x) in cells:                                     # ink rim of the screen
        if (y - 1, x) not in cs or (y, x - 1) not in cs or (y, x + 1) not in cs:
            a[y, x] = INK
    for x in range(x0 + 1, x1):                              # banked: a thread of ember-light
        a[bot, x] = FLAME[1] if x % 3 else FLAME[0]
    return img(a)


def waystone():
    """1x2 the village's lamp-stone (TRAVEL): a squat pale stone with a small
    shuttered lantern set in its head — the waystone kept the Hollowing way."""
    a = canvas(1, 2)
    fill(a, 3, 11, 12, 29, PALE[1])
    a[11:30, 3] = PALE[2]
    a[11:30, 12] = PALE[0]
    for y in (16, 22, 27):
        a[y, 4:12] = PALE[0]
    fill(a, 4, 2, 11, 10, IRON[2])                           # the lantern box
    fill(a, 5, 4, 10, 9, SHUT[2])
    a[4:10, 7:9] = SHUT[0]
    a[6, 5:7] = SHUT[3]
    a[6, 9:11] = SHUT[3]
    a[8, 7] = BRASS[2]
    outline(a, 4, 2, 11, 10, INK)
    a[1, 6:10] = IRON[3]
    outline(a, 3, 11, 12, 29, INK)
    contact_shadow(a, 2, 13, 30)
    return img(a)


def crag_boulders():
    """2x2 a slate boulder cluster for the crag rim (cool grey, frost-flecked)."""
    a = canvas(2, 2)
    SL = [hx("#2c3038"), hx("#4a5058"), hx("#6a7078"), hx("#8e949a")]
    for (bx, by, rx, ry) in ((10, 18, 9, 9), (22, 21, 8, 8), (16, 26, 8, 4)):
        for y in range(32):
            for x in range(32):
                d = (x - bx) ** 2 / rx ** 2 + (y - by) ** 2 / ry ** 2
                if d <= 1:
                    c = SL[1]
                    if d > 0.75:
                        c = SL[0]
                    elif (y - by) < -ry * 0.3 and (x - bx) < rx * 0.35:
                        c = SL[3] if d < 0.35 else SL[2]
                    a[y, x] = c
    for (x, y) in ((6, 12), (9, 11), (20, 16), (24, 15), (14, 22), (25, 23)):
        a[y, x] = hx("#c8ccd2")                               # frost flecks
    _ink_rim(a)
    contact_shadow(a, 3, 29, 31)
    return img(a)


def _sag(x):
    return int(round(3 * (1 - ((x - 24) / 21) ** 2)))


def wash_line():
    """3x2 a wash-line between two posts: grey blankets aired over it (the
    sleepers' blankets, washed and folded back every morning)."""
    a = canvas(3, 2)
    for px in (2, 44):
        fill(a, px, 4, px + 1, 29, WOOD[1])
        a[4:30, px] = WOOD[2]
        fill(a, px - 1, 3, px + 2, 3, WOOD[0])
        contact_shadow(a, px - 1, px + 2, 30)
    for x in range(4, 44):                                    # the line, a soft sag
        a[6 + _sag(x), x] = IRON[1]
    for (x0, x1, c) in ((7, 18, WOOL[2]), (21, 30, WOOL[1]), (33, 41, WOOL[3])):
        for x in range(x0, x1 + 1):
            y = 7 + _sag(x)
            fill(a, x, y, x, y + 12, c)
            a[y, x] = WOOL[3]
            a[y + 12, x] = WOOL[0]
            a[y + 13, x] = INK
        for x in range(x0 + 2, x1, 3):
            a[12 + _sag(x), x] = WOOL[0]
        for x in (x0, x1):
            y = 7 + _sag(x)
            a[y:y + 13, x] = INK
    return img(a)


def woodpile():
    """2x1 a tidy stack of grey-weathered logs under a little slate hood."""
    a = canvas(2, 1)
    for row, y in enumerate((10, 6)):
        for k in range(4 - row):
            x = 2 + row * 3 + k * 7
            fill(a, x, y, x + 5, y + 4, WOOD[1])
            fill(a, x + 1, y + 1, x + 3, y + 3, WOOD[2])
            a[y + 2, x + 2] = WOOD[0]
            outline(a, x, y, x + 5, y + 4, INK)
    fill(a, 1, 2, 30, 4, IRON[2])
    a[2, 1:31] = IRON[3]
    outline(a, 0, 1, 31, 4, INK)
    contact_shadow(a, 1, 30, 15)
    return img(a)


def punt():
    """2x1 a small grey punt moored on the mere, a hooded lamp on its prow —
    the last boat of the fishing village the mere used to be."""
    a = canvas(2, 1)
    for x in range(2, 30):
        t = abs(x - 16) / 14
        y0 = 4 + int(round(4 * t * t))
        fill(a, x, y0, x, 11, hx("#7c746a"))
        a[y0, x] = hx("#a89e92")
        a[11, x] = WOOD[0]
    fill(a, 7, 6, 24, 9, WOOD[0])                            # the well of the boat
    a[7, 7:25] = hx("#1c2430")
    for x in (12, 19):
        a[5:10, x] = WOOD[2]                                 # thwarts
    _ink_rim(a)
    fill(a, 26, 1, 28, 5, IRON[2])                           # the hooded prow-lamp
    outline(a, 26, 1, 28, 5, INK)
    for x in range(3, 29):                                   # still water, a faint ring
        a[12, x] = hx("#0e1218")
        if x % 4 == 0:
            a[13, x] = hx("#3a4656")
    return img(a)


def kin_basket():
    """2x1 Old Bracken's basket: a wide wicker bed, a big grey old kin asleep in
    it under a blanket, grey muzzle on the rim (home A's story prop)."""
    a = canvas(2, 1)
    fill(a, 2, 8, 29, 14, WOOD[1])
    for x in range(3, 29, 2):
        a[9:14, x] = WOOD[2]
    a[8, 2:30] = WOOD[2]
    outline(a, 2, 8, 29, 14, INK)
    for x in range(5, 23):                                    # the sleeper's grey back
        h = int(round(5 * (1 - ((x - 13) / 9) ** 2)))
        fill(a, x, 8 - h, x, 8, FUR[1])
        a[8 - h, x] = FUR[2]
        a[7 - h, x] = INK
    fill(a, 22, 4, 27, 8, PALE[1])                            # a grey-white muzzle on the rim
    outline(a, 21, 3, 28, 8, INK)
    a[5, 26] = INK
    a[6, 23:25] = INK                                         # a closed eye
    fill(a, 6, 6, 17, 8, WOOL[2])                             # the blanket over its haunch
    a[6, 6:18] = WOOL[3]
    a[8, 6:18] = WOOL[0]
    return img(a)


def spinning_wheel():
    """2x2 Maren's spinning wheel, grey wool on the distaff (home B's prop)."""
    import math
    a = canvas(2, 2)
    cx, cy, r = 12, 12, 9
    for t in range(0, 180, 30):
        for k in range(-r + 1, r):
            x = int(round(cx + k * math.cos(math.radians(t))))
            y = int(round(cy + k * math.sin(math.radians(t))))
            a[y, x] = WOOD[1]
    for t in range(0, 360, 3):
        x = int(round(cx + r * math.cos(math.radians(t))))
        y = int(round(cy + r * math.sin(math.radians(t))))
        a[y, x] = WOOD[2]
        a[y + 1, x] = WOOD[0]
    fill(a, 11, 11, 13, 13, BRASS[1])
    a[13:24, 12] = WOOD[0]                                    # the upright
    fill(a, 4, 23, 28, 25, WOOD[1])                           # the bench
    a[23, 4:29] = WOOD[2]
    outline(a, 4, 23, 28, 25, INK)
    for x in (6, 26):
        fill(a, x, 26, x + 1, 30, WOOD[0])
    a[4:23, 25] = WOOD[0]                                     # the distaff
    fill(a, 23, 6, 27, 16, WOOL[2])
    a[6, 23:28] = WOOL[3]
    a[11, 23:28] = WOOL[1]
    outline(a, 23, 6, 27, 16, INK)
    contact_shadow(a, 3, 29, 31)
    return img(a)


def candle_sill():
    """1x1 a candle-jar on a little shelf by the child's bed: the candle kept,
    safely, once her mother has seen it (home B, flag:q_still_candle_shown)."""
    a = canvas(1, 1)
    fill(a, 1, 12, 14, 13, WOOD[2])
    a[14, 1:15] = WOOD[0]
    outline(a, 1, 12, 14, 14, INK)
    for (x, y) in ((3, 2), (12, 2), (2, 6), (13, 6)):
        a[y, x] = GLOW
        a[y, x, 3] = 120
    fill(a, 5, 3, 10, 11, GLASS[2])
    a[4:11, 5] = GLASS[3]
    fill(a, 7, 7, 8, 11, PALE[2])
    a[6, 7:9] = FLAME[2]
    a[5, 7] = FLAME[3]
    outline(a, 5, 3, 10, 11, INK)
    return img(a)


def old_chairs():
    """2x1 two old high-backed chairs with their BACKS to the hearth — the way the
    village sits (home A); a grey shawl over one."""
    a = canvas(2, 1)
    for x0 in (2, 18):
        fill(a, x0, 1, x0 + 10, 9, WOOD[1])
        a[1, x0:x0 + 11] = WOOD[2]
        fill(a, x0 + 2, 3, x0 + 8, 8, hx("#4a5062"))
        outline(a, x0, 1, x0 + 10, 9, INK)
        fill(a, x0, 10, x0 + 10, 12, WOOD[2])
        outline(a, x0, 10, x0 + 10, 12, INK)
        for x in (x0 + 1, x0 + 9):
            a[13:15, x] = WOOD[0]
    fill(a, 19, 2, 27, 6, WOOL[2])                            # the shawl
    a[6, 19:28:2] = WOOL[0]
    a[2, 19:28] = WOOL[3]
    contact_shadow(a, 1, 30, 15)
    return img(a)


def stove_banked():
    """2x2 WALL piece, the SAME footprint + silhouette as interior_stove: the cook-
    stove banked for the Long Dusk — its firebox shut behind a louvred iron door,
    latched, only a hair of ember at the sill; the kettle left cold on the plate.
    (Home A: the open stove swaps back in at flag:dawn, with its hearth.)"""
    src = Image.open(REPO / "assets/tilesets/interior/objects/stove.png").convert("RGBA")
    a = np.asarray(src).astype("int16").copy()
    hot = (a[..., 0] > 150) & (a[..., 1] > 50) & (a[..., 2] < 110) & (a[..., 3] > 0)
    ys, xs = np.where(hot[16:])                              # the firebox (lower half)
    y0, y1, x0, x1 = 16 + ys.min(), 16 + ys.max(), xs.min(), xs.max()
    fill(a, x0, y0, x1, y1, IRON[1])                         # the iron door, shut
    for y in range(y0 + 1, y1, 2):                           # louvres
        a[y, x0 + 1:x1] = IRON[2]
    a[y0, x0:x1 + 1] = IRON[3]                               # lit top edge of the door
    a[y0:y1 + 1, (x0 + x1) // 2] = IRON[0]                   # where its leaves meet
    a[(y0 + y1) // 2, (x0 + x1) // 2 - 1:(x0 + x1) // 2 + 2] = BRASS[2]   # the latch
    outline(a, x0 - 1, y0 - 1, x1 + 1, y1 + 1, INK)
    for x in range(x0 + 1, x1, 2):                           # banked: an ember hair at the sill
        a[y1 + 1, x] = FLAME[0]
    warm = (a[..., 0] > a[..., 2] + 60) & (a[..., 1] > 60) & (a[..., 3] > 0)
    warm[y1 + 1:, :] = False                                 # (keep the ember hair)
    warm[16:, :] &= False                                    # only the kettle, up top
    a[warm, :3] = (a[warm, :3] * np.array([0.70, 0.74, 0.86])).astype(np.int16)  # cold brass
    return img(a)


# ---- the r2 review: the Quiet Hall's lower half, dressed ----------------------------
def lectern():
    """1x2 (interior) the reading lectern: a slanted desk on one post, the ledger of
    put-out lamps open on it, a ribbon marker; a hooded reading-lamp, capped."""
    a = canvas(1, 2)
    fill(a, 7, 14, 8, 27, WOOD[1])                            # the post
    a[14:28, 7] = WOOD[2]
    fill(a, 4, 27, 11, 29, WOOD[1]); outline(a, 4, 27, 11, 29, INK)   # the foot
    outline(a, 6, 14, 9, 27, INK)
    for y in range(6, 14):                                    # the slanted desk
        x0, x1 = 1 + (13 - y) // 3, 14 - (13 - y) // 3
        a[y, x0:x1 + 1] = WOOD[2] if y > 7 else WOOD[1]
    fill(a, 3, 7, 12, 11, PALE[2])                            # the open ledger
    a[7:12, 7] = PALE[0]                                      # its gutter
    for y in (8, 10):
        a[y, 4:7] = PALE[0]
        a[y, 9:12] = PALE[0]
    a[11:15, 10] = hx("#7a4a4a")                             # a ribbon marker
    outline(a, 1, 6, 14, 13, INK)
    fill(a, 11, 1, 14, 5, IRON[2]); a[1, 11:15] = IRON[3]     # the hooded lamp, capped
    outline(a, 11, 1, 14, 5, INK)
    contact_shadow(a, 3, 12, 30)
    return img(a)


def shutter_box():
    """1x1 (interior) a box of spare shutters, painted and stacked on edge — the
    village keeps them ready, the way other villages keep candles."""
    a = canvas(1, 1)
    fill(a, 1, 7, 14, 14, WOOD[1]); a[7, 1:15] = WOOD[2]
    outline(a, 1, 7, 14, 14, INK)
    for n, x in enumerate((3, 6, 9, 12)):                     # shutters on edge
        top = 2 + (n % 2)
        fill(a, x - 1, top, x + 1, 8, SHUT[1 + n % 2])
        a[top + 2, x - 1:x + 2] = SHUT[0]
        a[top + 4, x - 1:x + 2] = SHUT[0]
        outline(a, x - 1, top, x + 1, 8, INK)
    contact_shadow(a, 1, 14, 15)
    return img(a)


def sprig_basket():
    """1x1 (interior) a shallow basket of dried sprigs — one is tucked into the
    shutter-wall for every lamp put out; the rest wait here."""
    a = canvas(1, 1)
    fill(a, 2, 9, 13, 14, WOOD[1])
    for x in range(3, 13, 2):
        a[10:14, x] = WOOD[2]
    outline(a, 2, 9, 13, 14, INK)
    STEM = [hx("#5a5a44"), hx("#7a7a5a"), hx("#a09a74")]
    for (x, h, lean) in [(4, 6, -1), (6, 8, 0), (8, 7, 1), (10, 6, 1), (12, 5, 0)]:
        for k in range(h):
            xx = x + (lean if k > h // 2 else 0)
            a[9 - k, xx] = STEM[1]
        a[9 - h, x + lean] = STEM[2]                         # a dry seed-head
        a[10 - h, x + lean] = STEM[0]
    contact_shadow(a, 2, 13, 15)
    return img(a)


PIECES.update({
    "lectern": lectern, "shutter_box": shutter_box, "sprig_basket": sprig_basket,
    "stove_banked": stove_banked,
    "hearth_banked": hearth_banked, "waystone": waystone, "crag_boulders": crag_boulders,
    "wash_line": wash_line, "woodpile": woodpile, "punt": punt, "kin_basket": kin_basket,
    "spinning_wheel": spinning_wheel, "candle_sill": candle_sill, "old_chairs": old_chairs,
})


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
