#!/usr/bin/env python3
"""
underwaysforge — the LAST WATCH's own drawn kit (walkthrough/11 Part D, the Penumbra
Underways; review fix FD 2026-10-14: "stop reusing the Coldfog camp and doused lamps").

The watch is a handful of Hollowing folk living under the Ring to be near when it ends,
so everything is LIVED-IN and TENDED (story-bible: grief dressed as mercy; cute, sad,
never creepy). Drawn in the cartridge register of draw_mournfields_objects (flat
anchors, 1px ink, placed motifs), keyed to the basalt floor.

assets/tilesets/underways/objects -> underways_<stem>:
  bedroll        2x1  a grey wool roll on a rush mat, a folded spare at its head
  map_table      2x2  a trestle table, a chart of the Ring held down with stones, a
                      hooded candle stub (the watch's planning table)
  watch_bell     1x2  a little iron bell in a wooden frame, its pull-cord looped up
  ration_crates  2x2  two lashed crates, grey-wool tied tins on top
  kettle_shelf   2x2  a low plank shelf: the kettle, three cups, a tea caddy
  watch_rota     1x2  a slate on an easel, the watch-rota chalked in tallies
  masonry        2x2  fallen Spire masonry: two carved basalt blocks, a violet band
  root_curtain   2x2  the mountain's roots hanging down a wall face (walk-under)
  ring_lightwell 2x2  (the Ring's floor) an iron grate flush in the stone; far below,
                      a pale column and a small warm fire: the Underways, seen first

Run:  python3 tools/maps/underwaysforge.py
Then: ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import numpy as np

from draw_mournfields_objects import (BASALT, DARKGLASS, FLAME, IRON, POST, STARDIM,
                                      STARPALE, STONE, UNDER, VIOLET, WOOL, WOOLHEM)
from interiorforge import BRASS, INK, canvas, contact_shadow, fill, hx, img, outline

RUSH = [hx("#3a3420"), hx("#5c5232"), hx("#7c6e44")]
PARCH = [hx("#8a7c5c"), hx("#bcae86"), hx("#dccfa6")]
CRATE = [hx("#2e2418"), hx("#4e3c28"), hx("#6e563a"), hx("#8c7050")]
SLATE = [hx("#1c2028"), hx("#2c323e"), hx("#3c4452")]
CHALK = hx("#d8dce4")
ROOT = [hx("#1e1812"), hx("#3a2e22"), hx("#56442e"), hx("#6e5a3e")]
TEA = [hx("#3c2a3a"), hx("#5c4258"), hx("#7c5e78")]


def bedroll():
    a = canvas(2, 1)
    fill(a, 1, 8, 30, 14, RUSH[1])                     # the rush mat
    for x in range(2, 30, 3):
        a[8:15, x] = RUSH[0]
    a[8, 1:31] = RUSH[2]
    outline(a, 1, 8, 30, 14, INK)
    fill(a, 8, 4, 28, 12, WOOL[1])                     # the rolled blanket
    a[4, 9:28] = WOOL[3]
    a[5:7, 9:28] = WOOL[2]
    for x in (13, 19, 25):
        a[4:12, x] = WOOL[0]                           # the roll's folds
    a[11, 9:28] = WOOLHEM
    outline(a, 8, 3, 28, 12, INK)
    fill(a, 2, 5, 7, 11, WOOL[2])                      # the folded spare (a pillow)
    a[5, 3:7] = WOOL[3]
    a[10, 3:7] = WOOLHEM
    outline(a, 2, 4, 7, 11, INK)
    contact_shadow(a, 1, 30, 15)
    return img(a)


def map_table():
    a = canvas(2, 2)
    fill(a, 2, 12, 29, 17, POST[2])                    # the trestle top
    a[12, 2:30] = POST[3]
    a[17, 2:30] = POST[1]
    outline(a, 1, 11, 30, 18, INK)
    for x0 in (4, 25):                                 # the crossed trestle legs
        for i in range(11):
            a[19 + i, x0 + i // 3] = POST[1]
            a[19 + i, x0 + 3 - i // 3] = POST[1]
        a[29, x0 - 1:x0 + 5] = INK
    a[23, 5:28] = POST[0]                              # the stretcher
    fill(a, 6, 6, 23, 14, PARCH[1])                    # the chart, held flat
    a[6, 6:24] = PARCH[2]
    outline(a, 5, 5, 24, 15, INK)
    for t in np.linspace(0, 2 * np.pi, 40):            # the Ring, drawn on it
        x = int(round(14.5 + np.cos(t) * 6))
        y = int(round(10 + np.sin(t) * 3))
        a[y, x] = PARCH[0]
    a[9:12, 14:16] = VIOLET[1]                         # the Spire, inked dark
    a[13, 9] = FLAME[1]                                # a mouth marked in red
    a[13, 20] = FLAME[1]
    for (sx, sy) in ((5, 5), (24, 5), (5, 15)):        # the stones on the corners
        fill(a, sx - 1, sy - 1, sx + 1, sy, STONE[2])
        a[sy - 1, sx - 1] = STONE[3]
    fill(a, 25, 6, 28, 13, DARKGLASS[1])               # the hooded candle stub
    fill(a, 24, 4, 29, 10, WOOL[1])
    a[4, 25:29] = WOOL[2]
    outline(a, 24, 4, 29, 13, INK)
    a[11:13, 25:29] = FLAME[2]
    contact_shadow(a, 2, 29, 30)
    return img(a)


def watch_bell():
    a = canvas(1, 2)
    for x in (2, 13):                                  # the frame posts
        fill(a, x, 6, x + 1, 30, POST[1])
        a[6:31, x] = POST[2]
    fill(a, 1, 4, 14, 6, POST[2])                      # the crossbar
    a[4, 1:15] = POST[3]
    outline(a, 1, 4, 14, 6, INK)
    a[7:9, 7:9] = IRON[1]                              # the hanger
    for i, y in enumerate(range(9, 18)):               # the bell, flaring
        half = 2 + i // 2
        a[y, 8 - half:8 + half] = IRON[2] if i < 6 else IRON[3]
        a[y, 8 - half] = INK
        a[y, 8 + half - 1] = INK
    a[10:14, 6] = IRON[3]                              # its one dull shine
    a[18, 3:13] = INK
    a[18:20, 7:9] = BRASS[1]                           # the clapper
    for y in range(9, 26):                             # the pull-cord, looped up
        a[y, 12] = WOOLHEM
    a[25, 10:13] = WOOLHEM
    a[29:31, 0:16] = POST[0]
    contact_shadow(a, 0, 15, 31)
    return img(a)


def _crate(a, x0, y0, x1, y1):
    fill(a, x0, y0, x1, y1, CRATE[2])
    for y in range(y0 + 3, y1, 4):
        a[y, x0:x1 + 1] = CRATE[1]
    a[y0, x0:x1 + 1] = CRATE[3]
    a[y0:y1 + 1, x0 + 1] = CRATE[1]
    a[y0:y1 + 1, x1 - 1] = CRATE[1]
    outline(a, x0, y0, x1, y1, INK)


def ration_crates():
    a = canvas(2, 2)
    _crate(a, 1, 16, 16, 30)
    _crate(a, 15, 19, 30, 30)
    _crate(a, 4, 6, 17, 16)
    a[23, 1:31] = WOOLHEM                              # the lashing
    for (x, y) in ((20, 13), (25, 14)):                # tins, tied in grey wool
        fill(a, x, y, x + 4, y + 5, IRON[2])
        a[y, x:x + 5] = IRON[3]
        a[y + 3, x:x + 5] = WOOL[2]
        outline(a, x, y, x + 4, y + 5, INK)
    a[9:11, 8:14] = CHALK                              # chalked: FOR THE WATCH
    a[10, 9:13] = CRATE[2]
    contact_shadow(a, 1, 30, 31)
    return img(a)


def kettle_shelf():
    a = canvas(2, 2)
    for x in (2, 28):
        fill(a, x, 12, x + 1, 30, POST[1])
    for y in (12, 22):                                 # two planks
        fill(a, 1, y, 30, y + 2, POST[2])
        a[y, 1:31] = POST[3]
        outline(a, 1, y, 30, y + 2, INK)
    fill(a, 4, 3, 13, 11, IRON[1])                     # the kettle
    a[3, 6:12] = IRON[3]
    a[2, 8:10] = IRON[2]
    a[5:9, 14:16] = IRON[2]                            # spout
    a[1, 5:13] = IRON[0]                               # handle
    a[1:4, 5] = IRON[0]
    a[1:4, 12] = IRON[0]
    outline(a, 4, 3, 13, 11, INK)
    a[0, 15] = (*STARDIM, 200)                                # a breath of steam
    for i, x in enumerate((17, 21, 25)):               # three cups
        fill(a, x, 7, x + 2, 11, TEA[1 + i % 2])
        a[7, x:x + 3] = TEA[2]
        outline(a, x, 7, x + 2, 11, INK)
    fill(a, 6, 16, 12, 21, BRASS[1])                   # the tea caddy
    a[16, 6:13] = BRASS[2]
    outline(a, 6, 16, 12, 21, INK)
    fill(a, 17, 17, 26, 21, WOOL[1])                   # folded cloths
    a[17, 17:27] = WOOL[2]
    outline(a, 17, 17, 26, 21, INK)
    contact_shadow(a, 1, 30, 31)
    return img(a)


def watch_rota():
    a = canvas(1, 2)
    for (x0, x1) in ((3, 6), (12, 9)):                 # the easel legs
        for y in range(4, 31):
            x = int(round(x0 + (x1 - x0) * (y - 4) / 27))
            a[y, x] = POST[1]
    a[4:31, 8] = POST[0]
    fill(a, 1, 5, 14, 20, SLATE[1])                    # the slate
    a[5, 1:15] = SLATE[2]
    outline(a, 0, 4, 15, 21, INK)
    for r, y in enumerate((7, 10, 13, 16)):            # names + tallies
        a[y, 2:6] = CHALK
        for k in range(min(r + 2, 3)):
            a[y - 1:y + 1, 8 + k * 2] = CHALK
    a[18, 2:14] = CHALK                                # a line under: the watch holds
    contact_shadow(a, 2, 13, 31)
    return img(a)


def _block(a, x0, y0, x1, y1, band=None):
    """One fallen carved block: chipped corners, lit top, a crack, an optional band."""
    fill(a, x0, y0, x1, y1, STONE[1])
    a[y0:y0 + 2, x0:x1 + 1] = STONE[2]
    a[y0, x0:x1 + 1] = STONE[3]
    a[y0:y1 + 1, x1] = STONE[0]
    if band is not None:
        a[band, x0:x1 + 1] = VIOLET[1]
        a[band + 1, x0:x1 + 1] = VIOLET[0]
    outline(a, x0, y0, x1, y1, INK)
    for (cx, cy) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):   # chipped corners
        a[cy, cx] = 0
    cx = (x0 + x1) // 2
    for k in range(min(5, y1 - y0 - 2)):                       # the crack
        a[y0 + 2 + k, cx + (k % 2)] = INK


def masonry():
    a = canvas(2, 2)
    _block(a, 1, 16, 18, 29, band=21)                  # a lintel of the Spire, on its side
    _block(a, 15, 9, 27, 22, band=13)                  # a second, tilted against it
    _block(a, 20, 23, 29, 29)                          # a broken end
    for (x, y) in ((24, 30), (12, 30), (5, 14), (29, 21)):
        a[y, x] = STONE[2]                             # the chips
    a[11, 18] = (*STARDIM, 255)                        # a star-fleck in the carving
    a[18, 6] = (*STARDIM, 255)
    contact_shadow(a, 1, 29, 31)
    return img(a)


def root_curtain():
    a = canvas(2, 2)
    rng = np.random.default_rng(73)
    for x0 in range(2, 30, 4):                         # each root hangs to its own depth
        depth = int(rng.integers(8, 28))
        x = x0
        for y in range(0, depth):
            if y % 5 == 4:
                x += int(rng.integers(-1, 2))
            x = max(1, min(30, x))
            a[y, x] = ROOT[2]
            if y < 6:
                a[y, x - 1] = ROOT[1]
                a[y, x + 1] = ROOT[1]
        a[depth, x] = ROOT[3]
        if rng.random() < 0.4:                         # a pale root-tip glow, here and there
            a[depth, x] = (*STARDIM, 255)
    mask = a[..., 3] > 0
    for y in range(0, 32):
        for x in range(0, 31):
            if mask[y, x] and not mask[y, x + 1]:
                a[y, x + 1] = ROOT[0]              # the root's shadow side, one pixel
    return img(a)


def ring_lightwell():
    """2x2 a round iron grate flush in the Ring's stone; through it, far below, the
    Underways: a pale column of the Crown's light and a small orange fire beside it."""
    a = canvas(2, 2)
    cx, cy, r = 15.5, 15.5, 13.5
    for y in range(32):
        for x in range(32):
            d = np.hypot(x - cx, y - cy)
            if d <= r:
                a[y, x] = BASALT[0]
            elif d <= r + 1.6:
                a[y, x] = STONE[1] if y < cy else STONE[0]
            elif d <= r + 2.4:
                a[y, x] = INK
    for y in range(8, 24):                             # the column, far down
        for x in range(13, 19):
            if np.hypot(x - cx, y - cy) <= r:
                k = 0.85 if 14 <= x <= 17 else 0.5
                a[y, x, :3] = np.array(STARPALE) * k + a[y, x, :3] * (1 - k)
    for (x, y, c) in ((22, 20, FLAME[2]), (23, 20, FLAME[1]), (22, 21, FLAME[1]), (21, 20, FLAME[0]),
                      (22, 19, FLAME[3]), (21, 21, FLAME[1]), (23, 21, FLAME[0]), (22, 18, FLAME[2])):              # the watch-fire, tiny
        a[y, x] = c
    for v in range(5, 28, 5):                          # the grate bars
        for t in range(32):
            if np.hypot(v - cx, t - cy) <= r:
                a[t, v] = IRON[2]
                a[t, min(31, v + 1)] = IRON[0]
            if np.hypot(t - cx, v - cy) <= r:
                a[v, t] = IRON[2]
    for (x, y) in ((3, 4), (28, 6), (27, 27)):         # rivets on the rim stone
        a[y, x] = IRON[3]
    return img(a)


# ---- review fix FD2 (2026-10-14, expansion-panel Plan 4 r2 Part D: "B1's west bay and
# south gallery and F1's lower halls are still thin") — more of the watch's own life.

def hammock():
    """2x2 a grey-wool hammock slung between two root-wood posts, a spare blanket
    folded over its belly (walk-under top row)."""
    a = canvas(2, 2)
    for x in (2, 28):                                  # the posts
        fill(a, x, 6, x + 1, 30, POST[1])
        a[6:31, x] = POST[2]
        a[5, x - 1:x + 3] = POST[3]
        outline(a, x - 1, 5, x + 2, 6, INK)
    for x in range(4, 28):                             # the sag (a shallow catenary)
        t = (x - 16) / 12.0
        y = int(round(12 + 8 * (1 - t * t)))
        a[y - 2:y + 1, x] = WOOL[2]
        a[y - 3, x] = WOOL[3]
        a[y + 1, x] = WOOL[0]
        a[y + 2, x] = INK
        if x % 4 == 0:
            a[y - 1, x] = WOOL[1]                      # the weave
    for x in range(3, 6):                              # the ropes up to the posts
        a[9 + (x - 3), x] = WOOLHEM
        a[9 + (x - 3), 31 - x] = WOOLHEM
    fill(a, 12, 15, 20, 19, WOOL[1])                   # the folded spare
    a[15, 12:21] = WOOLHEM
    outline(a, 11, 14, 21, 20, INK)
    contact_shadow(a, 1, 30, 31)
    return img(a)


def name_slate():
    """1x2 a tall slate propped on a stone, chalked top to bottom with small names —
    everyone the watch remembers. The chalk is fresh: someone re-writes it."""
    a = canvas(1, 2)
    fill(a, 2, 2, 13, 26, SLATE[1])
    a[2, 2:14] = SLATE[2]
    a[3:26, 13] = SLATE[0]
    outline(a, 1, 1, 14, 27, INK)
    rng = np.random.default_rng(91)
    for y in range(4, 25, 2):                          # a column of names
        n = int(rng.integers(3, 8))
        x0 = int(rng.integers(3, 12 - n + 1))
        a[y, x0:x0 + n] = CHALK
        if rng.random() < 0.3:
            a[y, x0 + n - 1] = SLATE[2]                # a rubbed letter
    fill(a, 3, 27, 12, 30, STONE[1])                   # the propping stone
    a[27, 3:13] = STONE[2]
    outline(a, 2, 27, 13, 30, INK)
    a[29, 6:9] = (*FLAME[1][:3], 255)                  # a candle-stub at its foot
    a[28, 7] = FLAME[3]
    contact_shadow(a, 1, 14, 31)
    return img(a)


def _brazier(lit: bool):
    a = canvas(1, 2)
    for (x0, x1) in ((3, 1), (12, 14), (7, 7)):        # the tripod legs
        for y in range(16, 31):
            x = int(round(x0 + (x1 - x0) * (y - 16) / 14))
            a[y, x] = IRON[1]
    for i, y in enumerate(range(10, 17)):              # the iron bowl
        half = 7 - i // 2
        a[y, 8 - half:8 + half] = IRON[2] if i < 2 else IRON[1]
        a[y, 8 - half] = INK
        a[y, 8 + half - 1] = INK
    a[10, 1:15] = IRON[3]
    a[9, 1:15] = INK
    if lit:
        for (x, y, c) in ((7, 4, FLAME[3]), (8, 5, FLAME[2]), (6, 6, FLAME[2]), (9, 6, FLAME[1]),
                          (7, 7, FLAME[2]), (5, 8, FLAME[1]), (10, 8, FLAME[1]), (8, 8, FLAME[3]),
                          (6, 8, FLAME[2]), (9, 7, FLAME[2]), (8, 3, FLAME[1]), (4, 9, FLAME[0]),
                          (11, 9, FLAME[0])):
            a[y, x] = c
        a[9, 2:14] = FLAME[1]
    else:
        a[8, 3:13] = WOOL[1]                           # a heap of cold grey ash
        a[7, 5:11] = WOOL[2]
        a[6, 7:9] = WOOL[3]
        a[8, 6] = STONE[0]                             # one black coal, unburned
        a[7, 9] = STONE[0]
    contact_shadow(a, 0, 15, 31)
    return img(a)


def cold_brazier():
    """1x2 an iron brazier on a tripod, full of grey ash: lit after the dawn (twin)."""
    return _brazier(False)


def brazier_lit():
    return _brazier(True)


def hood_line():
    """2x2 a drying line between two staves, three spare grey-wool lamp-hoods hung on
    it to dry (the watch turns its lamps low with them), a drip on the floor."""
    a = canvas(2, 2)
    for x in (2, 28):
        fill(a, x, 4, x + 1, 30, POST[1])
        a[4:31, x] = POST[2]
        outline(a, x - 1, 3, x + 2, 4, INK)
    for x in range(3, 29):                             # the line, a slight sag
        t = (x - 16) / 13.0
        a[int(round(6 + 2 * (1 - t * t))), x] = WOOLHEM
    for i, cx in enumerate((8, 16, 24)):               # three hoods, each a little different
        top = 8 if i != 1 else 9
        for k, y in enumerate(range(top, top + 11)):
            half = 2 + k // 3
            a[y, cx - half:cx + half] = WOOL[1 + (i % 2)]
            a[y, cx - half] = INK
            a[y, cx + half - 1] = INK
        a[top + 10, cx - 5:cx + 5] = INK
        a[top + 9, cx - 4:cx + 4] = WOOLHEM            # the hem
        a[top + 1:top + 8, cx - 1] = WOOL[3]           # a crease of light
        a[top + 12 + i % 2, cx] = (*STARDIM, 255) if i != 2 else WOOL[2]   # a drip
    a[29, 14:19] = DARKGLASS[2]                        # the small wet patch
    a[30, 13:20] = DARKGLASS[1]
    contact_shadow(a, 1, 30, 31)
    return img(a)


def water_butt():
    """1x1 a hooped water-butt, a tin ladle hooked on its rim."""
    a = canvas(1, 1)
    fill(a, 2, 3, 13, 14, CRATE[2])
    a[3, 2:14] = DARKGLASS[2]                          # the water, dark
    a[4, 3:13] = DARKGLASS[1]
    for x in (5, 9):
        a[5:15, x] = CRATE[1]                          # staves
    for y in (6, 11):
        a[y, 2:14] = IRON[2]                           # the hoops
    outline(a, 1, 2, 14, 15, INK)
    a[1:6, 12] = IRON[3]                               # the ladle
    a[1, 10:13] = IRON[3]
    return img(a)


def firewood():
    """2x1 split root-wood and cut peat stacked against the cold, under a wool tarp."""
    a = canvas(2, 1)
    for row, y in enumerate((10, 6)):
        for i in range(6 - row):
            x0 = 2 + row * 3 + i * 5
            fill(a, x0, y, x0 + 4, y + 4, ROOT[2])
            a[y + 1:y + 4, x0 + 1:x0 + 4] = ROOT[3]   # the cut end
            a[y + 2, x0 + 2] = ROOT[1]                 # a ring
            outline(a, x0, y, x0 + 4, y + 4, INK)
    fill(a, 22, 3, 29, 9, WOOL[1])                     # the tarp, thrown back
    a[3, 22:30] = WOOL[2]
    outline(a, 21, 2, 30, 10, INK)
    contact_shadow(a, 1, 30, 15)
    return img(a)


FD2_PROPS = (("hammock", hammock), ("name_slate", name_slate), ("cold_brazier", cold_brazier),
             ("brazier_lit", brazier_lit), ("hood_line", hood_line), ("water_butt", water_butt),
             ("firewood", firewood))


def main() -> None:
    UNDER.mkdir(parents=True, exist_ok=True)
    for stem, fn in (("bedroll", bedroll), ("map_table", map_table), ("watch_bell", watch_bell),
                     ("ration_crates", ration_crates), ("kettle_shelf", kettle_shelf),
                     ("watch_rota", watch_rota), ("masonry", masonry),
                     ("root_curtain", root_curtain), ("ring_lightwell", ring_lightwell)) + FD2_PROPS:
        im = fn()
        path = UNDER / f"{stem}.png"
        im.save(path)
        print(f"  wrote {path}  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
