#!/usr/bin/env python3
"""
paulforge — the DRAWN furniture + wall-hangings of Paul's house on Wayward Rise
(the Booji-Wooji Man's home; builders build_paul_house*.py, content
src/game/content/regions/paul.ts).

interiorforge's sibling, kept in its OWN file and its OWN master folder so it
never clobbers the shared interior kit (or the image-gen hero masters in it):

    assets/tilesets/paul/objects/<stem>.png   ->  packed as `paul_<stem>`

The exterior pieces in the same folder (house, bike, washing_line) are
image-gen masters (gpt-image-2.5, native alpha, snapped to 16px multiples) and
are NOT written here — this script only ever writes the stems in PIECES.

Two mount classes (the interiorforge convention):

  WALL-HUNG  (1 row tall, placed ON the north wall's FACE row, solid:false):
    frames, paintings, the pin-board, the WANTED poster, the paddle, antlers,
    beadwork, Lottie's drawings. Drawn to sit inside the 16px face band.
  FREE-STANDING (top-down-frontal, ink outline, contact shadow):
    the shirt rack, coat stand, carved antelope, tea bench, gym kit, trunk,
    globe, rugby ball, syrup table, the Chickenpig plush.

Every small piece is an ASCII pixel map (one char = one pixel, `.` = clear) so
the art is crisp, legible and diffable; the paintings are drawn in code.
Deterministic; re-run freely.

Run:  python3 tools/maps/paulforge.py [--only a,b]
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "paul" / "objects"

PAL = {
    "k": "#10121e",  # ink
    "x": "#2a2a34",  # near-black (crayon, iron)
    "w": "#3a2418", "W": "#7a4a28", "o": "#b9763f", "O": "#e0a466",   # wood
    "g": "#5a431c", "G": "#d8b256", "y": "#f4df9a",                    # brass
    "q": "#bcae90", "p": "#e6dcc0", "P": "#f8f2e2",                    # paper/linen
    "R": "#7a2020", "r": "#c83a3a", "f": "#ff8a3d", "F": "#ffc070",    # reds/fire
    "B": "#1c2e5a", "b": "#3a6ab0", "c": "#9fd0ea", "n": "#f0f4f8",    # blues/snow
    "T": "#1f6a60", "t": "#37978a",                                    # teal
    "E": "#1f4a24", "e": "#3f8a3a", "l": "#8ac850",                    # greens
    "M": "#b04a78", "m": "#e87aa8",                                    # pinks
    "v": "#5a3a8a", "V": "#2e2050",                                    # purples
    "u": "#c89a58", "U": "#8a6234",                                    # cork / leather
    "s": "#6c6f86", "S": "#3a3d52",                                    # stone/iron
    "h": "#f2d8b8", "H": "#d0a47c",                                    # the Chickenpig's cream
    "z": "#f0c838",                                                    # crayon yellow
}


def rgba(hexs: str, alpha: int = 255):
    return [int(hexs[i:i + 2], 16) for i in (1, 3, 5)] + [alpha]


def canvas(tw: int, th: int) -> np.ndarray:
    return np.zeros((th * 16, tw * 16, 4), dtype=np.int16)


def stamp(a: np.ndarray, rows: list[str], ox: int = 0, oy: int = 0) -> None:
    """Paint an ASCII pixel map onto `a` at (ox, oy); `.` and ` ` are clear."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in ". ":
                continue
            yy, xx = oy + y, ox + x
            if 0 <= yy < a.shape[0] and 0 <= xx < a.shape[1]:
                a[yy, xx] = rgba(PAL[ch])


def rect(a, x0, y0, x1, y1, ch):
    a[y0:y1 + 1, x0:x1 + 1] = rgba(PAL[ch])


def box(a, x0, y0, x1, y1, ch):
    c = rgba(PAL[ch])
    a[y0, x0:x1 + 1] = c
    a[y1, x0:x1 + 1] = c
    a[y0:y1 + 1, x0] = c
    a[y0:y1 + 1, x1] = c


def px(a, x, y, ch):
    if 0 <= y < a.shape[0] and 0 <= x < a.shape[1]:
        a[y, x] = rgba(PAL[ch])


def contact(a, x0, x1, y):
    for x in range(x0, x1 + 1):
        if a[y, x, 3] == 0:
            a[y, x] = [16, 18, 30, 140]


def img(a) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# =============================================================================
#  FRAMES — every wall-hung piece sits inside the 16px wall-face band
# =============================================================================
def frame(tw: int, *, wood="o", lip="O", back="B", y0=1, y1=14) -> np.ndarray:
    """A hung picture frame across `tw` tiles: ink rim, a 1px moulding, a
    backing field; returns the canvas (inner field is x 2..W-3, y0+2..y1-2)."""
    a = canvas(tw, 1)
    W = tw * 16
    rect(a, 0, y0, W - 1, y1, "k")
    rect(a, 1, y0 + 1, W - 2, y1 - 1, wood)
    a[y0 + 1, 1:W - 1] = rgba(PAL[lip])       # lit top moulding
    rect(a, 2, y0 + 2, W - 3, y1 - 2, back)
    return a


SHIRT = [
    ".SSS..SSS.",
    "SSSSddSSSS",
    "SSSSSSSSSS",
    "ddSSSSSSdd",
    "..SSSSSS..",
    "..SSSSSS..",
    "..SSSSSS..",
    "..dddddd..",
]


def shirt(a, ox, oy, body: str, dark: str, emblem=None, stripes: str | None = None):
    rows = [r.replace("S", body).replace("d", dark) for r in SHIRT]
    if stripes:
        rows = [r if i % 2 == 0 or i == 0 else r.replace(body, stripes) for i, r in enumerate(rows)]
    stamp(a, rows, ox, oy)
    if emblem:
        stamp(a, emblem, ox + 3, oy + 3)


def framed_shirt(body, dark, emblem=None, stripes=None, back="B"):
    a = frame(1, back=back)
    shirt(a, 3, 4, body, dark, emblem, stripes)
    return img(a)


def shirt_race():   # the race he didn't finish: a red shirt with a race bib
    return framed_shirt("r", "R", ["nnnn", "nxxn", "nnnn"])


def shirt_sun():    # mustard, a little sun
    return framed_shirt("z", "u", [".ff.", "ffff", ".ff."])


def shirt_ferry():  # the one swapped with a stranger on a ferry: teal + a wave
    return framed_shirt("t", "T", ["....", "n.n.", ".n.n"])


def shirt_leaf():   # the maple country: white, a red leaf
    return framed_shirt("n", "q", [".rr.", "rrrr", ".rr."], back="V")


def shirt_stripe():  # the cape country: a green-and-gold hooped rugby jersey
    return framed_shirt("e", "E", None, stripes="z", back="V")


def shirt_star():   # purple, a gold star — "the one from the festival nobody remembers"
    return framed_shirt("v", "V", [".z..", "zzzz", ".zz."])


def shirt_boat():   # orange, a little white sail
    return framed_shirt("f", "R", [".n..", ".nn.", "nnnn"], back="V")


def shirt_gym():    # the gym: navy, a white dumbbell
    return framed_shirt("b", "B", ["....", "nnnn", "...."], back="V")


# =============================================================================
#  PAINTINGS — drawn in code (inner field ~28x10)
# =============================================================================
def painting_cape():
    """The far-south cape: a flat-topped mountain at sunset over the sea."""
    a = frame(2, wood="g", lip="G", back="v")
    W = 32
    for y, ch in ((3, "v"), (4, "M"), (5, "m"), (6, "f"), (7, "F")):
        a[y, 2:W - 2] = rgba(PAL[ch])
    # the sun sinking to the right of the mountain
    for (x, y) in ((25, 6), (26, 6), (24, 7), (25, 7), (26, 7), (27, 7)):
        px(a, x, y, "y")
    # the flat-topped mountain (a long table of rock), slopes either side
    for y in range(5, 11):
        half = 0 if y == 5 else (y - 5)
        x0, x1 = 9 - half, 20 + half
        a[y, max(2, x0):min(W - 2, x1 + 1)] = rgba(PAL["V"])
    a[5, 9:21] = rgba(PAL["M"])                     # sunset light on the table-top
    # the sea + the sun's road on it
    a[10:13, 2:W - 2] = rgba(PAL["B"])
    a[11, 2:W - 2] = rgba(PAL["b"])
    for x in (24, 25, 26, 27):
        px(a, x, 10, "F")
    for x in (25, 26):
        px(a, x, 11, "F")
    return img(a)


def painting_cape_day():
    """The far-south cape on a SUNNY day: the flat-topped mountain over a blue bay."""
    a = frame(2, wood="o", lip="O", back="c")
    W = 32
    for y, ch in ((3, "b"), (4, "b"), (5, "c"), (6, "c"), (7, "n")):
        a[y, 2:W - 2] = rgba(PAL[ch])
    for (x, y) in ((25, 3), (26, 3), (25, 4), (26, 4)):
        px(a, x, y, "z")
    for y in range(5, 10):
        half = 0 if y == 5 else (y - 5)
        x0, x1 = 8 - half, 19 + half
        a[y, max(2, x0):min(W - 2, x1 + 1)] = rgba(PAL["s"])
    a[5, 8:20] = rgba(PAL["n"])                      # the cloud "tablecloth" on top
    a[6, 9:18] = rgba(PAL["n"])
    a[9, 2:W - 2] = rgba(PAL["e"])                  # the green slopes of the town
    a[10:13, 2:W - 2] = rgba(PAL["b"])
    a[11, 2:W - 2] = rgba(PAL["c"])
    for x in (6, 14, 23):
        px(a, x, 10, "n")                            # little white sails
    return img(a)


def painting_lake():
    """The maple country: a snowy lake under a night sky, pines on the shore."""
    a = frame(2, wood="o", lip="O", back="B")
    W = 32
    for (x, y) in ((4, 3), (11, 4), (18, 3), (26, 4), (22, 5)):
        px(a, x, y, "n")
    # far snowy hills
    for x in range(2, W - 2):
        top = 6 + (1 if (x // 5) % 2 else 0)
        a[top:9, x] = rgba(PAL["n"])
        a[8, x] = rgba(PAL["c"])
    # the frozen lake
    a[9:13, 2:W - 2] = rgba(PAL["c"])
    a[10, 2:W - 2] = rgba(PAL["b"])
    a[12, 2:W - 2] = rgba(PAL["b"])
    # pines
    for cx in (5, 9, 23, 27):
        for i, y in enumerate(range(4, 10)):
            w = i // 2
            a[y, cx - w:cx + w + 1] = rgba(PAL["E"])
        px(a, cx, 3, "E")
        px(a, cx, 10, "w")
    return img(a)


def painting_protea():
    """The cape country's great pink flower."""
    a = frame(1, wood="g", lip="G", back="p")
    stamp(a, [
        "....m.m.m...",
        "...mMmMmMm..",
        "..mMhhhhhMm.",
        "..MhhhhhhhM.",
        "..mMhhhhhMm.",
        "...mMmMmMm..",
        "..e..ee..e..",
        "...eeEEee...",
        ".....EE.....",
    ], 2, 3)
    return img(a)


def beadwork():
    """A beaded panel from the cape country, hung from a little rod."""
    a = canvas(1, 1)
    rect(a, 2, 1, 13, 1, "W")
    px(a, 1, 1, "w"), px(a, 14, 1, "w")
    stamp(a, [
        "rrzzbbzzrr",
        "rzzbnnbzzr",
        "zzbnxxnbzz",
        "zbnxeexnbz",
        "zzbnxxnbzz",
        "rzzbnnbzzr",
        "rrzzbbzzrr",
        "n.r.z.b.e.",
        ".x.r.z.b.e",
    ], 3, 3)
    return img(a)


def pinboard():
    """Cork pin-board crowded with travel tickets, postcards and a photo."""
    a = canvas(2, 1)
    W = 32
    rect(a, 0, 1, W - 1, 14, "k")
    rect(a, 1, 2, W - 2, 13, "W")
    rect(a, 2, 3, W - 3, 12, "u")
    rng = np.random.default_rng(7)
    for _ in range(18):
        x, y = int(rng.integers(2, W - 2)), int(rng.integers(3, 13))
        px(a, x, y, "U")
    # postcard (sea + sky), a red ticket, a gold ticket, a photo, a blue ticket
    rect(a, 3, 4, 9, 8, "n"); rect(a, 4, 5, 8, 6, "c"); rect(a, 4, 7, 8, 7, "b")
    rect(a, 11, 4, 16, 6, "r"); px(a, 12, 5, "n"); px(a, 14, 5, "n")
    rect(a, 18, 5, 23, 7, "z"); px(a, 19, 6, "x"); px(a, 21, 6, "x")
    rect(a, 24, 3, 29, 9, "n"); rect(a, 25, 4, 28, 7, "e"); px(a, 26, 5, "F")
    rect(a, 10, 8, 15, 11, "b"); px(a, 11, 9, "n"); px(a, 13, 10, "n")
    rect(a, 17, 9, 22, 11, "m")
    rect(a, 3, 10, 8, 11, "t")
    for (x, y) in ((6, 4), (13, 4), (20, 5), (26, 3), (12, 8), (19, 9), (5, 10)):
        px(a, x, y, "r" if (x + y) % 2 else "z")
    return img(a)


def wanted():
    """The WANTED poster from 'a far-off bureau'. He swears it's a joke."""
    a = canvas(1, 1)
    stamp(a, [
        "................",
        ".kkkkkkrkkkkkkk.",
        ".kPPPPPPPPPPPPk.",
        ".kPrRrRrRrRrRPk.",
        ".kPPPPPPPPPPPPk.",
        ".kPPPqqqqqqPPPk.",
        ".kPPPqHqqHqPPPk.",
        ".kPPPqkhhkqPPPk.",
        ".kPPPqhhhhqPPPk.",
        ".kPPPqHkkHqPPPk.",
        ".kPPPPqhhqPPPPk.",
        ".kPPPPPPPPPPPPk.",
        ".kPqqqqPPqqqPPk.",
        ".kPqqqPPPPPrrPk.",
        ".kPPPPPPPPPrrPk.",
        ".kkkkkkkkkkkkkk.",
    ])
    return img(a)


def antlers():
    """A great spread of palmate antlers on a wooden shield (the maple country)."""
    a = canvas(2, 1)
    stamp(a, [
        "................................",
        "..q.q.q...............q.q.q.....",
        "..qqqqq.q...........q.qqqqq.....",
        "...qqqqqqq.........qqqqqqq......",
        "....Uqqqqq.........qqqqqU.......",
        "......Uqqqq.......qqqqU.........",
        "........UUqq.....qqUU...........",
        "..........UqWWWWWqU.............",
        "...........kWoooWk..............",
        "...........kWoOoWk..............",
        "...........kWoooWk..............",
        "............kWoWk...............",
        ".............kWk................",
        "..............k.................",
    ], 3, 1)
    return img(a)


def paddle():
    """A painted canoe paddle hung on two pegs (the maple country)."""
    a = canvas(2, 1)
    stamp(a, [
        "................................",
        "................................",
        "...w....................w.......",
        "...w....................w.......",
        "..kkkkkkkkkkkkkkkkkkk..kkkkk....",
        "..kOoooooooooooooooookkrrrrrk...",
        "..kOooooooooooooooooooOrrrrrrk..",
        "..koWWWWWWWWWWWWWWWWWWonnnnnnk..",
        "..kkkkkkkkkkkkkkkkkkkkkrrrrrrk..",
        "......................krrrrrk...",
        ".......................kkkkk....",
    ], 0, 3)
    return img(a)


# =============================================================================
#  LOTTIE'S DRAWINGS — crayon on paper, taped to the attic wall
# =============================================================================
PAPER = [
    "..yy........yy..",
    ".yyHHHHHHHHHHyy.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".HPPPPPPPPPPPPU.",
    ".UUUUUUUUUUUUUU.",
]
CP = [  # the Chickenpig in crayon: comb, cream body, red wing, green sickles
    "..rr.....",
    ".rrr...e.",
    ".mmmm.ee.",
    "mmmmmmme.",
    "mxmmrrmm.",
    "Mmmmrrmm.",
    ".mmmmmm..",
    ".x..x....",
]
GIRL = [
    "r.h.r",
    ".hhh.",
    "..h..",
    ".mmm.",
    "mmmmm",
    ".x.x.",
]


def paper():
    a = canvas(1, 1)
    stamp(a, PAPER, 0, 1)
    return a


def cp_drawing_a():  # the Chickenpig under a big crayon sun
    a = paper()
    stamp(a, CP, 3, 5)
    stamp(a, [".zz", "zzz", "zz."], 11, 3)
    a[13, 2:15] = rgba(PAL["l"])
    return img(a)


def cp_drawing_b():  # the Chickenpig surrounded by hearts
    a = paper()
    stamp(a, CP, 4, 5)
    for (x, y) in ((2, 3), (12, 3), (12, 9)):
        stamp(a, ["r.r", "rrr", ".r."], x, y)
    return img(a)


def cp_drawing_c():  # Lottie and the Chickenpig, holding hands (well, wing)
    a = paper()
    stamp(a, GIRL, 2, 6)
    stamp(a, CP, 7, 5)
    px(a, 7, 9, "x")
    a[13, 2:15] = rgba(PAL["l"])
    return img(a)


def cp_drawing_d():  # a rainbow over a VERY big Chickenpig
    a = paper()
    for i, ch in enumerate("rze"):
        a[3 + i, 3 + i:13 - i] = rgba(PAL[ch])
        px(a, 2 + i, 4 + i, ch), px(a, 13 - i, 4 + i, ch)
    big = [row.replace(".", ".") for row in CP]
    stamp(a, big, 4, 6)
    return img(a)


def drawing_bike():  # (before) Grandad on his bike, very fast
    a = paper()
    stamp(a, [
        "....h.....",
        "...xhx....",
        "....b.....",
        "...b.b....",
        ".xx...xx..",
        "x..x.x..x.",
        ".xx...xx..",
    ], 3, 5)
    for y in (6, 8, 10):
        a[y, 2:4] = rgba(PAL["q"])
    return img(a)


def drawing_sea():  # (before) the quay, a boat, the dark lamp
    a = paper()
    stamp(a, [
        "........z.",
        "........x.",
        "...r....x.",
        "..rr....x.",
        ".UUUU...x.",
        "bbbbbbbbbb",
        "b.b.b.b.b.",
    ], 3, 4)
    return img(a)


# =============================================================================
#  FREE-STANDING — top-down-frontal, ink outline, contact shadow
# =============================================================================
def shirt_rack():
    """3x2 clothes rail of t-shirts — the T-SHIRT MUSEUM's working stock."""
    a = canvas(3, 2)
    W, H = 48, 32
    rect(a, 2, 3, 3, 28, "W"); rect(a, 44, 3, 45, 28, "W")
    a[3:29, 2] = rgba(PAL["O"]); a[3:29, 44] = rgba(PAL["O"])
    rect(a, 1, 2, 46, 3, "G"); a[2, 1:47] = rgba(PAL["y"]); a[4, 2:46] = rgba(PAL["k"])
    cols = [("r", "R"), ("z", "u"), ("t", "T"), ("n", "q"), ("e", "E"), ("m", "M")]
    for i, (body, dark) in enumerate(cols):
        x = 5 + i * 6 + (1 if i > 2 else 0)
        px(a, x + 4, 5, "x"); px(a, x + 4, 6, "x")
        rows = [r.replace("S", body).replace("d", dark) for r in SHIRT]
        tall = rows[:4] + rows[4:7] + rows[4:7] + rows[7:]
        stamp(a, tall, x, 7)
        if i == 4:
            for yy in range(8, 18, 2):
                for xx in range(x, x + 10):
                    if a[yy, xx, 3] and a[yy, xx, 0] == int(PAL["e"][1:3], 16):
                        a[yy, xx] = rgba(PAL["z"])
    # feet
    rect(a, 0, 28, 6, 29, "w"); rect(a, 41, 28, 47, 29, "w")
    a[28, 0:7] = rgba(PAL["W"]); a[28, 41:48] = rgba(PAL["W"])
    contact(a, 0, 6, 30); contact(a, 41, 47, 30)
    return img(a)


# ---- THE THREE RAILS (2026-10): every shirt Paul owns is OUT, IN or NEVER ------
# Each rail wears a colour-coded card hung from its bar (green OUT / amber IN /
# red NEVER) so the three read apart at a glance and invite a closer look; the
# NEVER rail is roped off and padlocked, which is exactly why you'll touch it.
GLYPH = {
    "O": ["###", "#.#", "#.#", "#.#", "###"],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"],
    "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "E": ["###", "#..", "##.", "#..", "###"],
    "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "!": ["#", "#", "#", ".", "#"],
}


def word(a, text: str, ox: int, oy: int, ch: str) -> None:
    x = ox
    for c in text:
        g = GLYPH[c]
        stamp(a, [r.replace("#", ch) for r in g], x, oy)
        x += len(g[0]) + 1


def word_w(text: str) -> int:
    return sum(len(GLYPH[c][0]) + 1 for c in text) - 1


def crowned(a, text: str, paper: str, ink: str, *, post: str = "G") -> Image.Image:
    """Lift a 3x2 rail onto a 3x3 canvas with its category board standing on
    the bar (the top row is the object's overhang, drawn over the floor behind)."""
    out = canvas(3, 3)
    out[16:, :] = a
    w = word_w(text) + 6
    x0 = 24 - w // 2
    for x in (x0 + 3, x0 + w - 4):                           # two little posts
        rect(out, x, 13, x, 17, post)
    rect(out, x0, 2, x0 + w - 1, 13, "k")
    rect(out, x0 + 1, 3, x0 + w - 2, 12, paper)
    out[3, x0 + 1:x0 + w - 1] = rgba(PAL["P"])               # a lit top edge
    word(out, text, x0 + 3, 5, ink)
    return img(out)


def rail(a, *, post="W", lit="O", bar="G", bar_lit="y") -> None:
    rect(a, 2, 3, 3, 28, post); rect(a, 44, 3, 45, 28, post)
    a[3:29, 2] = rgba(PAL[lit]); a[3:29, 44] = rgba(PAL[lit])
    rect(a, 1, 2, 46, 3, bar); a[2, 1:47] = rgba(PAL[bar_lit]); a[4, 2:46] = rgba(PAL["k"])
    rect(a, 0, 28, 6, 29, "w"); rect(a, 41, 28, 47, 29, "w")
    a[28, 0:7] = rgba(PAL[post]); a[28, 41:48] = rgba(PAL[post])
    contact(a, 0, 6, 30); contact(a, 41, 47, 30)


def hung_shirt(a, x, body, dark, *, long=True, rows=None):
    px(a, x + 4, 5, "x"); px(a, x + 4, 6, "x")
    rows = rows or [r.replace("S", body).replace("d", dark) for r in SHIRT]
    if long:
        rows = rows[:4] + rows[4:7] + rows[4:7] + rows[7:]
    stamp(a, rows, x, 7)


def rack_out():
    """OUT: neat, bright, collared — safe to be seen in. Green card."""
    a = canvas(3, 2)
    rail(a)
    for i, (body, dark) in enumerate([("b", "B"), ("n", "q"), ("z", "u"), ("t", "T")]):
        x = 5 + i * 10
        hung_shirt(a, x, body, dark)
        px(a, x + 4, 8, "k"); px(a, x + 5, 8, "k")          # a proper collar
        for yy in (11, 14, 17):                               # buttons
            px(a, x + 4, yy, dark)
    return crowned(a, "OUT", "l", "E")


def rack_in():
    """IN: faded, baggy, holey — house only. A worn wooden rail, slippers under. Amber card."""
    a = canvas(3, 2)
    rail(a, post="w", lit="W", bar="W", bar_lit="O")
    cols = [("q", "U"), ("c", "b"), ("m", "M"), ("s", "S")]
    for i, (body, dark) in enumerate(cols):
        x = 5 + i * 10
        hung_shirt(a, x, body, dark)
        if i == 0:                                            # the load-bearing hole
            a[13, x + 4] = rgba(PAL["w"]); a[13, x + 5] = rgba(PAL["w"]); a[14, x + 5] = rgba(PAL["w"])
        if i == 1:                                            # pyjama stripes
            for yy in range(9, 19, 3):
                for xx in range(x + 2, x + 8):
                    if a[yy, xx, 3]:
                        a[yy, xx] = rgba(PAL["n"])
        if i == 3:                                            # paint splats
            px(a, x + 3, 12, "z"); px(a, x + 6, 15, "r"); px(a, x + 5, 10, "e")
    # a pair of slippers under the rail
    stamp(a, ["MMMm.MMMm", "MMMM.MMMM"], 19, 25)
    return crowned(a, "IN", "F", "U", post="W")


def rack_never():
    """NEVER: loud, lurid, banned — roped off and padlocked. Red card."""
    a = canvas(3, 2)
    rail(a, post="S", lit="s", bar="S", bar_lit="s")
    cols = [("l", "E"), ("m", "M"), ("x", "k"), ("f", "R")]
    for i, (body, dark) in enumerate(cols):
        x = 5 + i * 10
        hung_shirt(a, x, body, dark)
    word(a, "NO", 26, 14, "n")                                # the one that just says NO
    for yy in range(10, 19, 2):                               # zigzags on the lime one
        px(a, 7 + (yy // 2) % 3, yy, "z"); px(a, 10 - (yy // 2) % 3, yy + 1, "z")
    stamp(a, [".zz.", "zffz", ".zz."], 18, 12)                # a cheese-bun on the pink one
    # the velvet rope across the front, slung between brass posts
    for x in (0, 47):
        rect(a, x, 18, x, 27, "G"); px(a, x, 17, "y")
    for x in range(1, 47):
        sag = 20 + int(3 * (1 - ((x - 24) / 23) ** 2))
        px(a, x, sag, "r"); px(a, x, sag + 1, "R")
    # the padlock where the rope meets the rail post
    stamp(a, [".kk.", "k..k", "GGGG", "GkGG", "GGGG"], 41, 20)
    return crowned(a, "NEVER!", "r", "n", post="S")


def coat_stand():
    """1x2 coat stand: a plaid lumber-jacket and a bobble hat (maple country)."""
    a = canvas(1, 2)
    stamp(a, [
        "......nr........",
        ".....rrrr.......",
        "....rnnnnr......",
        "....rrrrrr......",
        "......WW........",
        "...xrrrrrrx.....",
        "..rrkrrkrrkr....",
        "..rkkkkkkkkr....",
        "..rrkrrkrrkr....",
        "..rrkrrkrrkr....",
        "..kkkkkkkkkk....",
        "..rrkrrkrrkr....",
        "..rrkrrkrrkr....",
        "..rkkkkkkkkr....",
        "..rrkrrkrrkr....",
        "...rkrrkrrk.....",
        "...rkrrkrrk.....",
        "....kkkkkk......",
        "......WW........",
        "......WW........",
        "......WW........",
        "......WW........",
        "......WW........",
        "......WW........",
        "......WW........",
        "......WW........",
        "......WW........",
        "...wWWWWWWw.....",
        "..wWWWWWWWWw....",
        "..kkkkkkkkkk....",
    ], 1, 1)
    contact(a, 2, 13, 31)
    return img(a)


def antelope():
    """1x2 carved wooden antelope with long spiral horns, on a plinth (the cape)."""
    a = canvas(1, 2)
    stamp(a, [
        ".....w....w.....",
        "......w..w......",
        ".....w..w.......",
        "......w..w......",
        ".....w..w.......",
        "......ww........",
        "......ww........",
        "......Woo.......",
        ".....oWWo.......",
        "....oWWW........",
        "...WWkWW........",
        "..WWWWW.........",
        "..wWWW..........",
        "....WWo.........",
        "....WWWooooooo..",
        "....WWWWWWWWWWo.",
        "....WWWWWWWWWWW.",
        "....wWWWWWWWWWw.",
        ".....wwWWWWWww..",
        ".....W.W...W.W..",
        ".....W.W...W.W..",
        ".....W.W...W.W..",
        ".....w.w...w.w..",
        "..kkkkkkkkkkkkk.",
        "..oOOOOOOOOOOOo.",
        "..wWWWWWWWWWWWw.",
        "..wWWWWWWWWWWWw.",
        "..wwwwwwwwwwwww.",
        "..kkkkkkkkkkkkk.",
    ], 0, 2)
    contact(a, 2, 14, 31)
    return img(a)


def tea_bench():
    """2x2 kitchen bench: the kettle, a red tin of red-bush tea, two mugs."""
    a = canvas(2, 2)
    W, H = 32, 32
    rect(a, 0, 8, W - 1, H - 2, "k")
    rect(a, 1, 9, W - 2, 21, "o")
    a[9, 1:W - 1] = rgba(PAL["O"])
    rect(a, 1, 22, W - 2, H - 3, "W")
    a[22, 1:W - 1] = rgba(PAL["k"])
    for x0 in (2, 16):
        box(a, x0 + 1, 24, x0 + 12, H - 4, "w")
        px(a, x0 + 6, 26, "G"); px(a, x0 + 7, 26, "G")
    # the kettle (iron, a brass knob) + a curl of steam
    stamp(a, [
        "...nn....",
        "....n....",
        "...nn....",
        "....G....",
        "..kkkkk..",
        ".kSssSSkk",
        "kSsSSSSSk",
        "kSSSSSSkk",
        "kSSSSSSk.",
        ".kkkkkk..",
    ], 3, 6)
    # the red tin with a gold band
    stamp(a, [
        "kkkkkk",
        "krrrRk",
        "kzzzzk",
        "krrrRk",
        "krrrRk",
        "kkkkkk",
    ], 14, 10)
    # two mugs
    for x, c in ((21, "t"), (26, "r")):
        stamp(a, [r.replace("c", c) for r in ["kkkk.", "kcckk", "kcck.k", "kcckk", "kkkk."]], x, 11)
    contact(a, 0, W - 1, H - 1)
    return img(a)


def gym_kit():
    """1x1 by the door: the bike helmet on top of the gym bag."""
    a = canvas(1, 1)
    stamp(a, [
        "................",
        "................",
        ".....kkkkkk.....",
        "....krrxrrxk....",
        "...krrrrrrrrk...",
        "...kRrrrrrrRk...",
        "...kkRRRRRRkk...",
        "..kBBBBBBBBBBk..",
        ".kBbbbbbbbbbbBk.",
        ".kbbbbbbbbbbbbk.",
        ".knnnnnnnnnnnnk.",
        ".kbbbbbbbbbbbbk.",
        ".kBbbbbbbbbbbBk.",
        "..kkkkkkkkkkkk..",
    ], 0, 1)
    contact(a, 1, 14, 15)
    return img(a)


def trunk():
    """2x1 travel trunk, plastered in stickers from everywhere."""
    a = canvas(2, 1)
    W = 32
    rect(a, 1, 1, W - 2, 14, "k")
    rect(a, 2, 2, W - 3, 5, "w")
    a[2, 2:W - 2] = rgba(PAL["W"])
    rect(a, 2, 6, W - 3, 13, "W")
    a[6, 2:W - 2] = rgba(PAL["k"])
    for x in (2, W - 3):
        rect(a, x, 2, x, 13, "G")
    for x in (9, 22):
        rect(a, x, 2, x + 1, 13, "U")
    for (x0, y0, c) in ((4, 8, "z"), (12, 7, "r"), (16, 9, "c"), (24, 8, "e"), (13, 11, "n")):
        rect(a, x0, y0, x0 + 3, y0 + 2, c)
    px(a, 15, 4, "G"); px(a, 16, 4, "G")
    contact(a, 1, W - 2, 15)
    return img(a)


def globe():
    """1x1 a little globe on a brass stand (oceans, and somewhere to go)."""
    a = canvas(1, 1)
    stamp(a, [
        "......kkkk......",
        "....kkbbbbkG....",
        "...kbbeebbbkG...",
        "...kbeeebbuk.G..",
        "..kbbbeebbuubG..",
        "..kbbbbbbbbbbG..",
        "..kbbbbbuubbbG..",
        "...kbbbbuubbkG..",
        "...kbebbbbbk.G..",
        "....kkbbbbkkG...",
        "......kkkkGG....",
        ".......GG.......",
        ".......gG.......",
        ".....gGGGGg.....",
        ".....kkkkkk.....",
    ], 0, 0)
    contact(a, 4, 11, 15)
    return img(a)


def rugby_stand():
    """1x1 an oval leather ball on a little wooden kicking-tee (the cape)."""
    a = canvas(1, 1)
    stamp(a, [
        "................",
        "......kkkk......",
        ".....kuuOuk.....",
        "....kuuuOuuk....",
        "....kuunnnuk....",
        "....kuuunuuk....",
        "....kuunnnuk....",
        "....kUuuuuUk....",
        "....kUUuuUUk....",
        ".....kUUUUk.....",
        "......kkkk......",
        ".....wWWWWw.....",
        "....wWWOOWWw....",
        "....kkkkkkkk....",
    ], 0, 1)
    contact(a, 3, 12, 15)
    return img(a)


def syrup_table():
    """1x1 side table: a tin of maple syrup (red leaf label) and a tin mug."""
    a = canvas(1, 1)
    stamp(a, [
        "...kkkk.........",
        "...ksssk........",
        "..kssssk........",
        "..kPPPPk..kkkk..",
        "..kPrrPk..knnkk.",
        "..kPrrPk..knnk.k",
        "..kPPPPk..knnkk.",
        "..kkkkkk..kkkk..",
        ".kkkkkkkkkkkkkk.",
        ".kOOOOOOOOOOOOk.",
        ".koooooooooooook",
        "..kWWWWWWWWWWk..",
        "...w.......w....",
        "...w.......w....",
        "...k.......k....",
    ], 0, 0)
    contact(a, 1, 14, 15)
    return img(a)


def plush():
    """1x1 the Chickenpig PLUSH — Lottie's, after the catch."""
    a = canvas(1, 1)
    stamp(a, [
        "......rr........",
        ".....rrrr.......",
        "....khhhhk...ee.",
        "...khhhhhhk.eEe.",
        "...khxhhxhk.ee..",
        "...khhmmhhk.eE..",
        "...khmxxmhkre...",
        "..khhhmmhhrrr...",
        "..khhhhhhhhrr...",
        "..kHhhhhhhhHk...",
        "..kHhhHHhhhHk...",
        "...kHHkkHHHk....",
        "....kk..kkk.....",
    ], 0, 2)
    contact(a, 2, 12, 15)
    return img(a)


PIECES = {
    # wall-hung (face row, solid:false)
    "wanted": wanted, "pinboard": pinboard, "painting_cape": painting_cape,
    "painting_lake": painting_lake, "painting_cape_day": painting_cape_day,
    "shirt_star": shirt_star, "shirt_boat": shirt_boat, "painting_protea": painting_protea,
    "beadwork": beadwork, "antlers": antlers, "paddle": paddle,
    "shirt_race": shirt_race, "shirt_sun": shirt_sun, "shirt_ferry": shirt_ferry,
    "shirt_leaf": shirt_leaf, "shirt_stripe": shirt_stripe, "shirt_gym": shirt_gym,
    "cp_drawing_a": cp_drawing_a, "cp_drawing_b": cp_drawing_b,
    "cp_drawing_c": cp_drawing_c, "cp_drawing_d": cp_drawing_d,
    "drawing_bike": drawing_bike, "drawing_sea": drawing_sea,
    # free-standing
    "shirt_rack": shirt_rack, "rack_out": rack_out, "rack_in": rack_in,
    "rack_never": rack_never, "coat_stand": coat_stand, "antelope": antelope,
    "tea_bench": tea_bench, "gym_kit": gym_kit, "trunk": trunk, "globe": globe,
    "rugby_stand": rugby_stand, "syrup_table": syrup_table, "plush": plush,
}


def main() -> None:
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    OBJDIR.mkdir(parents=True, exist_ok=True)
    for stem, fn in PIECES.items():
        if only is not None and stem not in only:
            continue
        im = fn()
        assert im.width % 16 == 0 and im.height % 16 == 0, stem
        im.save(OBJDIR / f"{stem}.png")
        print(f"  drew paul_{stem}  ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
