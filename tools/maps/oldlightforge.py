#!/usr/bin/env python3
"""
oldlightforge — the DRAWN kit of the Old Light, Mr. Punchwheel's seven-floor
joke tower on Pearlmoor Point (the Causeway Bell quest; content
src/game/content/oldlight.ts).

Mr. Punchwheel is a clockwork brass joke-machine with a variety-show MC's
manners, so the tower is furnished like a backstage that has been left alone
with him for too long: props, gags, laugh-track dolls and a tea-urn that
smiles. The floors warp as you climb (build_oldlight_sets.py does the walls
and floors); this script draws the FURNITURE. Kept in its OWN master folder,
like gymforge/paulforge, so interiorforge's full re-runs never touch it:

    assets/tilesets/oldlight/objects/<stem>.png   ->  packed as `oldlight_<stem>`

Projection matches the interior kit: straight-on, top-down-frontal, 1px ink
outline, a soft contact shadow on the floor row of every free-standing piece.
Wall-hung pieces sit inside the 16px wall-FACE band with no floor contact;
the one wall-MOUNTED piece (the funhouse mirror) is a front elevation whose
top row is drawn over the wall face (placed overhang 1 + walk_under, like
roomkit.wall_mount). Every piece is drawn in code (ASCII pixel maps + masks)
so it is crisp and deterministic; re-run freely.

  FREE-STANDING (solid):   jack_box 1x1, rubber_chickens 1x2, pie_table 2x1,
                           clown_shoes 2x1, joke_lectern 1x2, mallet 1x2,
                           laugh_dolls 2x2, laugh_meter 1x2, teacups 1x2,
                           unicycle 1x2, spring_can 1x1, upside_chair 1x1,
                           spotlight 1x2, cog_heap 2x1, tea_urn 2x2
  FLOOR DECALS (solid:false, no shadow): whoopee 1x1, banana 1x1, confetti 1x1
  WALL-HUNG (face row, solid:false):     mask_wall 1x1, applause_sign 2x1,
                                         bunting 2x1, clock_backwards 1x1
  WALL-MOUNTED (overhang 1, walk_under): funhouse_mirror 1x2

Run:  python3 tools/maps/oldlightforge.py [--only a,b]
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "oldlight" / "objects"

# warm brass / varnish / red-and-cream circus palette (world-palette ramps)
PAL = {
    "k": "#10121e",  # ink
    "x": "#2a2a34",  # near-black (iron, open mouths)
    "i": "#3a3d52", "I": "#6c6f86", "j": "#a8acc0", "J": "#e4e8f2",   # iron/steel
    "g": "#5a431c", "G": "#b98a2e", "y": "#e8c060", "Y": "#fff0a8",   # brass
    "w": "#3a2418", "W": "#7a4a28", "o": "#b9763f", "O": "#e0a466",   # varnished wood
    "R": "#7a1e24", "r": "#c8343a", "s": "#f06a5a",                   # circus red
    "q": "#bcae90", "p": "#e6dcc0", "P": "#fbf5e6", "n": "#ffffff",   # cream / white
    "B": "#1c2e5a", "b": "#3a6ab0", "c": "#9fd0ea",                   # blues
    "E": "#1f5a2a", "e": "#3f9a44", "l": "#9ad850",                   # greens
    "z": "#f0c838", "Z": "#b88a18",                                   # rubber yellow
    "f": "#ff8a3d", "F": "#c85a22",                                   # orange
    "m": "#f08ab0", "M": "#b04a78",                                   # pinks
    "v": "#7a4aaa", "V": "#3e2460",                                   # purples
    "h": "#f6d2a8", "H": "#d09a70",                                   # doll porcelain
    "a": "#5ac8b8", "A": "#1f6a60",                                   # teal
}


def rgba(hexs: str, alpha: int = 255):
    return np.array([int(hexs[i:i + 2], 16) for i in (1, 3, 5)] + [alpha], dtype=np.int16)


def canvas(tw: int, th: int) -> np.ndarray:
    return np.zeros((th * 16, tw * 16, 4), dtype=np.int16)


def px(a, x, y, ch):
    h, w = a.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        a[y, x] = rgba(PAL[ch])


def rect(a, x0, y0, x1, y1, ch):
    h, w = a.shape[:2]
    x0, x1 = max(0, x0), min(w - 1, x1)
    y0, y1 = max(0, y0), min(h - 1, y1)
    if x0 <= x1 and y0 <= y1:
        a[y0:y1 + 1, x0:x1 + 1] = rgba(PAL[ch])


def stamp(a, rows, ox=0, oy=0, *, flip=False):
    """Paint an ASCII pixel map at (ox, oy); `.`/space are clear."""
    for y, row in enumerate(rows):
        if flip:
            row = row[::-1]
        for x, ch in enumerate(row):
            if ch not in ". ":
                px(a, ox + x, oy + y, ch)


def shape(a, inside, fill, *, hi=None, lo=None, ink="k", box=None):
    """Draw a mask-defined blob: `inside(x, y)` -> bool. Ink outline on the
    edge pixels, a lit rim just inside the up/left edge, a shade rim just
    inside the down/right edge — the house lighting (top-left key)."""
    h, w = a.shape[:2]
    x0, y0, x1, y1 = box or (0, 0, w - 1, h - 1)
    m = np.zeros((h + 2, w + 2), bool)
    for y in range(max(0, y0), min(h, y1 + 1)):
        for x in range(max(0, x0), min(w, x1 + 1)):
            m[y + 1, x + 1] = bool(inside(x, y))
    core = m.copy()
    core[1:-1, 1:-1] = (m[1:-1, 1:-1] & m[:-2, 1:-1] & m[2:, 1:-1]
                        & m[1:-1, :-2] & m[1:-1, 2:])
    for y in range(h):
        for x in range(w):
            if not m[y + 1, x + 1]:
                continue
            if not core[y + 1, x + 1]:
                px(a, x, y, ink or fill)
                continue
            ch = fill
            if hi and (not core[y, x + 1] or not core[y + 1, x]):
                ch = hi
            if lo and (not core[y + 2, x + 1] or not core[y + 1, x + 2]):
                ch = lo
            px(a, x, y, ch)


def ellipse(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0


def contact(a, x0, x1, y, alpha=100):
    """Soft floor shadow on the canvas's bottom rows (only into clear pixels)."""
    h, w = a.shape[:2]
    for yy, al in ((y, alpha), (y - 1, alpha // 2)):
        if 0 <= yy < h:
            for x in range(max(0, x0), min(w, x1 + 1)):
                if a[yy, x, 3] == 0:
                    a[yy, x] = [10, 8, 20, al]


def img(a) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# a tiny 3x5 sign font (L is 2 wide so APPLAUSE fits a 2-tile box sign)
FONT = {
    "A": ["010", "101", "111", "101", "101"], "P": ["110", "101", "110", "100", "100"],
    "L": ["10", "10", "10", "10", "11"], "U": ["101", "101", "101", "101", "111"],
    "S": ["011", "100", "010", "001", "110"], "E": ["111", "100", "110", "100", "111"],
    "H": ["101", "101", "111", "101", "101"],
    "1": ["01", "11", "01", "01", "01"], "2": ["110", "001", "010", "100", "111"],
    "3": ["110", "001", "010", "001", "110"], "9": ["010", "101", "011", "001", "110"],
    "6": ["011", "100", "110", "101", "010"],
}


def text(a, s, x, y, ch, gap=1):
    for c in s:
        g = FONT[c]
        for yy, row in enumerate(g):
            for xx, b in enumerate(row):
                if b == "1":
                    px(a, x + xx, y + yy, ch)
        x += len(g[0]) + gap
    return x


def gear(a, cx, cy, r, teeth, *, fill="y", hi="Y", lo="G", hole=True, phase=0.0):
    """A brass cog: a disc with square teeth, inked, lit top-left, a recessed
    hub ring and a dark axle hole."""
    def inside(x, y):
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy)
        if d <= r - 1.0:
            return True
        if d > r + 1.6:
            return False
        for t in range(teeth):
            ang = phase + 2 * math.pi * t / teeth
            along = dx * math.cos(ang) + dy * math.sin(ang)
            perp = -dx * math.sin(ang) + dy * math.cos(ang)
            if along > 0 and abs(perp) <= 1.7:
                return True
        return False
    shape(a, inside, fill, hi=hi, lo=lo, ink="k",
          box=(int(cx - r - 3), int(cy - r - 3), int(cx + r + 3), int(cy + r + 3)))
    if hole:
        for y in range(int(cy - r), int(cy + r + 1)):
            for x in range(int(cx - r), int(cx + r + 1)):
                d = math.hypot(x - cx, y - cy)
                if d <= max(0.8, r * 0.2):
                    px(a, x, y, "k")
                elif r > 4 and abs(d - r * 0.5) < 0.5:
                    px(a, x, y, lo)


# =============================================================================
#  FREE-STANDING
# =============================================================================
def jack_box():
    """1x1 a sprung jack-in-the-box: harlequin box, the lid flung back, a
    coiled spring and a grinning jester head still wobbling."""
    a = canvas(1, 1)
    stamp(a, [
        "..z..........z..",
        "..kr........bk..",
        "...krr....bbk...",
        "...kkrrrbbbbk...",
        "...kPPPPPPPPk...",
        "...kPkPPPPkPk...",
        "...kmPPssPPmk...",
        "...kPkxxxxkPk...",
        "....kPkrrkPk....",
        ".....kkjjkk..kk.",
        "......kIjk..kGGk",
        "..kxxxxjjxxxxkk.",
        "..krrPPrrPPrrk..",
        "..kPPrrPPrrPPk..",
        "..kggggggggggk..",
    ])
    contact(a, 2, 15, 15)
    return img(a)


CHICKEN = [
    "f.f.f..",
    ".fff...",
    "..f....",
    "..f....",
    ".kkkk..",
    "kzzzzk.",
    "kzzzzzk",
    "kzzzzZk",
    "kZzzzZk",
    ".kzzZk.",
    "..kzk..",
    "..kzk..",
    ".kzzzk.",
    "rkxzzk.",
    "rkzzk..",
    ".kffk..",
    "..f....",
]


def rubber_chickens():
    """1x2 a bentwood hat-stand hung with rubber chickens, upside down by
    their feet, beaks to the floor."""
    a = canvas(1, 2)
    # the pole + knob + the hook arm
    rect(a, 7, 2, 8, 27, "k"); rect(a, 7, 3, 7, 27, "o"); rect(a, 8, 3, 8, 27, "W")
    stamp(a, ["..kk..", ".kOok.", ".kowk.", "..kk.."], 5, 0)
    rect(a, 1, 4, 14, 4, "k"); rect(a, 2, 4, 13, 4, "W")
    px(a, 1, 3, "k"); px(a, 14, 3, "k")
    stamp(a, CHICKEN, 0, 5)
    stamp(a, CHICKEN, 9, 5, flip=True)
    # one more on the floor, flat on its back, feet in the air
    stamp(a, [
        "........f.f.",
        "..kkkk..ff..",
        "rkxzzzkkzzk.",
        ".kffzzzzzzzk",
        "..kkkkkkkkk.",
    ], 4, 25)
    # the stand's feet
    stamp(a, ["kkkkk", "kWWWk"], 0, 28)
    stamp(a, ["kk", "Wk"], 14, 28)
    contact(a, 0, 15, 31)
    return img(a)


def _pie(a, cx, cy, eaten=False):
    shape(a, ellipse(cx, cy, 4.6, 2.9), "o", hi="O", lo="W")
    if eaten:
        # the empty tin: a crumb or two, the dented foil
        shape(a, ellipse(cx, cy, 3.2, 1.6), "j", hi="J", lo="I", ink=None)
        px(a, cx - 1, cy, "O"); px(a, cx + 2, cy - 1, "O")
        return
    shape(a, ellipse(cx, cy - 0.4, 3.4, 1.9), "P", hi="n", lo="q", ink=None)
    px(a, cx, cy - 2, "n"); px(a, cx - 1, cy - 1, "n"); px(a, cx + 1, cy - 1, "n")
    px(a, cx, cy - 1, "z")


def pie_table():
    """2x1 a little table under a red-checked cloth with custard pies ready
    to throw — one tin already empty (somebody got it)."""
    a = canvas(2, 1)
    # the cloth (top surface + front drop with the check)
    rect(a, 1, 2, 30, 12, "k")
    rect(a, 2, 3, 29, 8, "P")
    for x in range(2, 30):
        for y in range(3, 9):
            if (x // 3 + y // 3) % 2 == 0:
                px(a, x, y, "s")
    rect(a, 2, 9, 29, 11, "r")
    for x in range(2, 30, 3):
        rect(a, x, 9, x, 11, "P")
    rect(a, 2, 11, 29, 11, "R")
    # scalloped hem
    for x in range(1, 31, 3):
        px(a, x + 1, 12, "r"); px(a, x, 12, "k"); px(a, x + 2, 12, "k")
    # legs peeking out
    rect(a, 3, 13, 4, 14, "w"); rect(a, 27, 13, 28, 14, "w")
    _pie(a, 7, 5)
    _pie(a, 16, 6)
    _pie(a, 25, 5, eaten=True)
    contact(a, 1, 30, 15)
    return img(a)


SHOE = [
    "........kkkkk...",
    "..kkkk.kssrrrk..",
    ".kxxxxkssrrrrrk.",
    ".kqppqksrrrPrrrk",
    ".krrrzrzrrrrrrrk",
    ".krrrrzrrrPrrrRk",
    ".krrrzrzrrrrrrRk",
    ".kRrrrrrrrrrrRRk",
    ".kpppppppppppppk",
    "..kkkkkkkkkkkkk.",
]


def clown_shoes():
    """2x1 a pair of enormous clown shoes, toes splayed, laces undone."""
    a = canvas(2, 1)
    stamp(a, SHOE, 0, 5, flip=True)
    stamp(a, SHOE, 16, 4)
    # a dangling lace
    px(a, 10, 15, "z"); px(a, 11, 14, "z"); px(a, 21, 14, "z")
    contact(a, 0, 31, 15)
    return img(a)


def joke_lectern():
    """1x2 a varnished lectern buried under an enormous open joke-book, a red
    ribbon hanging out and a big grin drawn on the page."""
    a = canvas(1, 2)
    # the book (wider than the lectern)
    stamp(a, [
        ".kkkkkkk.kkkkkk.",
        "kPPPPPPPkPPPPPPk",
        "kPqqqqPPkPqqqqPk",
        "kPPPPPPPkPPPPPPk",
        "kPqqqqqPkPkPPkPk",
        "kPPPPPPPkPPPPPPk",
        "kPqqqqqPkrrrrrrk",
        "kPPPPPPPkPrnnrPk",
        "kPqqqqqPkPPrrPPk",
        "kpppppppkpppppk.",
        ".kkkkkkkkkkkkkk.",
    ], 0, 3)
    # page curl + ribbon
    px(a, 15, 12, "k"); px(a, 14, 13, "P")
    rect(a, 10, 14, 10, 18, "r"); px(a, 9, 19, "r"); px(a, 11, 19, "R")
    # lectern: slanted top lip, the post, the foot
    stamp(a, [
        ".kkkkkkkkkkkkkk.",
        "kOOOOOOOOOOOOOOk",
        ".kWWWWWWWWWWWWk.",
        "...kkkkkkkkkk...",
        "....kWOOOoWk....",
        "....kWOooWWk....",
        "....kWOooWWk....",
        "....kWOooWWk....",
        "....kWOooWWk....",
        "....kWOooWWk....",
        "....kWOooWWk....",
        "....kWyyyyWk....",
        "....kWOooWWk....",
        "...kkkkkkkkkk...",
        "..kOOOOOOOOOOk..",
        "..kwwwwwwwwwwk..",
        "...kkkkkkkkkk...",
    ], 0, 14)
    contact(a, 1, 14, 31)
    return img(a)


def mallet():
    """1x2 a giant cartoon mallet leaning on its handle, brass-banded barrel
    head, a sticking-plaster on the striking face."""
    a = canvas(1, 2)
    # the handle (drawn first, the head over it)
    for t in range(0, 19):
        x = 8 - t * 5 // 18
        y = 12 + t
        px(a, x - 1, y, "k"); px(a, x, y, "O"); px(a, x + 1, y, "o"); px(a, x + 2, y, "k")
    rect(a, 2, 30, 5, 30, "k")
    # the barrel body (bulging top/bottom) between two end faces
    shape(a, lambda x, y: 2 <= x <= 13 and (1 <= y <= 11 or (4 <= x <= 11 and y in (0, 12))),
          "o", hi="O", lo="W", box=(0, 0, 15, 13))
    for y in (4, 8):
        for x in range(3, 13):
            if tuple(a[y, x, :3]) == tuple(rgba(PAL["o"])[:3]):
                px(a, x, y, "W")
    for x in (5, 10):
        for y in range(1, 12):
            if a[y, x, 3] and tuple(a[y, x, :3]) != tuple(rgba(PAL["k"])[:3]):
                px(a, x, y, "y" if y < 4 else "G" if y < 10 else "g")
    for cx in (1.5, 13.5):
        shape(a, ellipse(cx, 6, 1.9, 5.6), "O", ink="k", box=(0, 0, 15, 13))
        px(a, round(cx), 6, "o")
    # a sticking-plaster on the right face
    stamp(a, ["m", "P", "m"], 14, 5)
    px(a, 13, 6, "m"); px(a, 15, 6, "m")
    contact(a, 0, 7, 31)
    return img(a)


DOLL = [
    "..kkkkk..",
    ".kHHHHHk.",
    "kHhhhhhHk",
    "khkhhhkhk",
    "kkhkhkhkk",
    "khmxxxmhk",
    "khhxrxhhk",
    ".khhxhhk.",
    "..kkkkk..",
]


def laugh_dolls():
    """2x2 the laugh track: a bench of three clockwork laughing dolls, mouths
    wide open, eyes screwed shut, brass keys in their backs."""
    a = canvas(2, 2)
    # the bench (seat + front rail + legs)
    rect(a, 0, 19, 31, 21, "k"); rect(a, 1, 20, 30, 20, "O")
    rect(a, 1, 21, 30, 23, "k"); rect(a, 2, 22, 29, 22, "W")
    for x in (2, 28):
        rect(a, x, 24, x + 1, 29, "k"); px(a, x, 24, "W")
    rect(a, 15, 24, 16, 29, "k")
    dolls = [(1, 5, "r", "R", "y"), (11, 2, "b", "B", "o"), (21, 5, "e", "E", "M")]
    for i, (ox, oy, body, dark, hair) in enumerate(dolls):
        # brass winding key out to the side
        kx = ox + (9 if i != 0 else -1)
        stamp(a, ["G.G", "GGG", ".G."] if i else ["G.G", "GGG", ".G."], kx - (1 if i else 0), oy + 10)
        head = [r.replace("H", "W" if hair == "o" else hair.upper() if False else "H") for r in DOLL]
        stamp(a, DOLL, ox, oy)
        # hair colour
        for y in range(oy, oy + 3):
            for x in range(ox, ox + 9):
                if a[y, x, 3] and tuple(a[y, x, :3]) == tuple(rgba(PAL["H"])[:3]):
                    px(a, x, y, hair)
        # body: dress with a frilled collar, arms flung up laughing
        stamp(a, [
            ".kPnPnPk.",
            "k" + body * 7 + "k",
            "k" + body + dark + body * 3 + dark + body + "k",
            "k" + body * 7 + "k",
            ".k" + body * 5 + "k.",
            ".kkkkkkk.",
        ], ox, oy + 9)
        px(a, ox - 1, oy + 8, "h"); px(a, ox + 9, oy + 8, "h")
        px(a, ox - 1, oy + 9, "k"); px(a, ox + 9, oy + 9, "k")
        # legs dangling over the bench front
        legs_y = oy + 15
        for lx in (ox + 2, ox + 5):
            rect(a, lx, legs_y, lx + 1, 24 if oy + 15 < 24 else legs_y, "P")
            rect(a, lx, 24, lx + 1, 25, "x")
    # the "HA HA" in the air
    text(a, "HA", 1, 0, "r")
    text(a, "HA", 24, 0, "r")
    contact(a, 0, 31, 31)
    return img(a)


def laugh_meter():
    """1x2 a brass laugh-meter on a stand: a half-moon dial (green, yellow,
    red), the needle jammed hard past the red UPROAR stop, sparks flying."""
    a = canvas(1, 2)
    cx, cy = 7.5, 11.0
    shape(a, lambda x, y: ((x - cx) / 7.6) ** 2 + ((y - cy) / 10.0) ** 2 <= 1 and y <= 13,
          "G", hi="y", lo="g", box=(0, 0, 15, 14))
    face = lambda x, y: ((x - cx) / 5.8) ** 2 + ((y - cy) / 8.0) ** 2 <= 1 and y <= 10
    for y in range(0, 12):
        for x in range(16):
            if not face(x, y):
                continue
            d = math.sqrt(((x - cx) / 5.8) ** 2 + ((y - cy) / 8.0) ** 2)
            th = math.degrees(math.atan2(cy - y, x - cx))
            ch = "P"
            if d >= 0.74:
                ch = "e" if th > 125 else "z" if th > 60 else "r"
            elif d >= 0.6 and int(th) % 30 < 8:
                ch = "q"
            px(a, x, y, ch)
    # the needle: pivot to the far right, bent over the stop
    for (x, y) in ((8, 10), (9, 10), (10, 9), (11, 9), (12, 8), (13, 8), (14, 7)):
        px(a, x, y, "k")
        px(a, x, y - 1, "x") if x in (10, 12) else None
    px(a, 15, 6, "k")
    px(a, 7, 10, "x"); px(a, 7, 11, "k"); px(a, 8, 11, "k")
    # sparks
    for (x, y) in ((15, 3), (13, 2), (15, 6)):
        px(a, x, y, "Y")
    px(a, 14, 4, "f")
    # the label plate: UPROAR as three red bars
    rect(a, 3, 13, 12, 17, "k"); rect(a, 4, 14, 11, 16, "r")
    rect(a, 4, 14, 11, 14, "s")
    for x in (5, 7, 9):
        px(a, x, 15, "P"); px(a, x + 1, 15, "P")
    # the stand
    rect(a, 7, 18, 8, 26, "k"); rect(a, 7, 18, 7, 26, "G")
    stamp(a, [
        "....kkkkkkk.....",
        "...kGyyyyyGk....",
        "..kGGGGGGGGGk...",
        ".kgkkkkkkkkkgk..",
        ".kk.........kk..",
    ], 0, 26)
    contact(a, 0, 15, 31)
    return img(a)


CUP = {
    "a": ["kPPPPPk", "kPbbbPkk", ".kPPPk.k", "..kkk.."],
    "b": ["kmmmmmk", "kmPPPmkk", ".kmmmk.k", "..kkk.."],
    "c": ["knnnnnk", "knGGGnkk", ".knnnk.k", "..kkk.."],
}


def teacups():
    """1x2 a tottering tower of teacups on saucers — each one a little off
    the last, the top one holding a tiny teapot."""
    a = canvas(1, 2)
    y = 26
    xs = [4, 5, 3, 4, 6, 5, 3]
    kinds = "abcabca"
    for i, x in enumerate(xs):
        # saucer
        rect(a, x - 1, y + 3, x + 7, y + 3, "k"); rect(a, x, y + 3, x + 6, y + 3, "q")
        stamp(a, CUP[kinds[i]], x, y - 1)
        y -= 4
        if y < 2:
            break
    # the teapot on top
    stamp(a, [
        "...kk...",
        "..kGGk..",
        ".kPPPPk.",
        "kkPbbPkk",
        "k.kPPk.k",
        "...kk...",
    ], 4, 0)
    contact(a, 1, 14, 31)
    return img(a)


def unicycle():
    """1x2 a red unicycle parked upright in a little wooden wheel-stand."""
    a = canvas(1, 2)
    # saddle
    stamp(a, [
        "...kkkkkkkk.....",
        "..krsssrrrrk....",
        "..krrrrrrrRk....",
        "...kkkRRkkk.....",
    ], 1, 1)
    # seat post + fork
    rect(a, 7, 5, 8, 14, "k"); px(a, 7, 6, "J"); rect(a, 7, 7, 7, 14, "j")
    rect(a, 4, 14, 11, 15, "k"); rect(a, 5, 14, 10, 14, "r")
    rect(a, 4, 15, 4, 22, "k"); rect(a, 11, 15, 11, 22, "k")
    # wheel
    cx, cy, r = 7.5, 22.0, 6.4
    shape(a, ellipse(cx, cy, r, r), "x", ink="k", box=(0, 14, 15, 31))
    shape(a, ellipse(cx, cy, r - 1.3, r - 1.3), "i", ink="I", box=(0, 14, 15, 31))
    for ang in range(0, 360, 45):
        for t in (1, 2, 3, 4):
            px(a, round(cx + t * math.cos(math.radians(ang))),
               round(cy + t * math.sin(math.radians(ang))), "j")
    px(a, 7, 22, "y"); px(a, 8, 22, "y")
    # pedals
    rect(a, 2, 24, 4, 24, "k"); rect(a, 11, 19, 13, 19, "k")
    # the wooden stand clamp
    stamp(a, [
        "kWk..........kWk",
        "kOk..........kOk",
        "kOkkkkkkkkkkkkOk",
        "kOOOOOOOOOOOOOOk",
        "kkkkkkkkkkkkkkkk",
    ], 0, 25)
    contact(a, 0, 15, 31)
    return img(a)


SNAKE = {"r": ("r", "P"), "e": ("e", "z"), "v": ("v", "m")}


def spring_can():
    """1x1 a can of 'mixed nuts' that is, as ever, spring snakes — the lid
    popped clean off, two striped snakes boinging out with googly eyes."""
    a = canvas(1, 1)
    snakes = [(4.5, 1, "r", "P", 0.0), (10.5, 0, "e", "z", 2.2)]
    for (x0, top, c1, c2, ph) in snakes:
        for y in range(top + 4, 11):
            x = round(x0 + 1.4 * math.sin(y * 1.1 + ph))
            px(a, x - 1, y, "k"); px(a, x + 2, y, "k")
            ch = c1 if (y // 2) % 2 else c2
            px(a, x, y, ch); px(a, x + 1, y, ch)
        hx = round(x0 + 1.4 * math.sin((top + 4) * 1.1 + ph)) - 1
        stamp(a, [
            "nn.nn",
            "nk.kn",
            "k" + c1 * 3 + "k",
            ".kkk.",
        ], hx - 1 + 1 - 1, top)
        px(a, hx + 1, top + 2, c1)
    # can
    stamp(a, [
        ".kkkkkkkkkk.",
        "kjJjjjjjjjik",
        "kbbbbbbbbbbk",
        "kbPrPrPrPrbk",
        "kbbbbbbbbbbk",
        ".kkkkkkkkkk.",
    ], 2, 9)
    # the lid, flipped off to the side
    stamp(a, ["kk..", "kjk.", ".kjk", "..kk"], 0, 4)
    contact(a, 2, 13, 15)
    return img(a)


def upside_chair():
    """1x1 a perfectly good chair, standing on its head (the back of it on
    the floor, all four legs in the air)."""
    a = canvas(1, 1)
    up = canvas(1, 1)
    far = [
        "...kk.........",
        "...kwk........",
        "...kwk........",
        "...kwk........",
        "...kwk........",
        "...kwk........",
        "...kwkkkkkkkk.",
        "...kwwwwwwwwk.",
        "...kkkkkkkkkk.",
        "...kwk.....kwk",
        "...kwk.....kwk",
        "...kwk.....kwk",
        "...kkk.....kkk",
    ]
    near = [
        "kk...........",
        "kOk..........",
        "kWk..........",
        "kok..........",
        "kWk..........",
        "kWkkkkkkkkkk.",
        "kssssssssssk.",
        "krrrrrrrrrRk.",
        "kkkkkkkkkkkk.",
        "kWk......kWk.",
        "kWk......kWk.",
        "kWk......kWk.",
        "kok......kok.",
        "kkk......kkk.",
    ]
    stamp(up, far, 2, 0)
    stamp(up, near, 1, 1)
    a[:15] = up[14::-1]
    contact(a, 1, 14, 15)
    return img(a)


def spotlight():
    """1x2 a theatre spotlight on a tripod, barn-doors open, lens lit."""
    a = canvas(1, 2)
    stamp(a, [
        "...k......k.....",
        "..kik....kik....",
        ".kxkkkkkkkkxk...",
        ".kiiiiiiiiikYk..",
        "kxiIIIIIIiikYYk.",
        "kxiiiiiiiiikYYk.",
        "kxiiiiiiiiikYYk.",
        ".kiiiiiiiiikYk..",
        ".kxkkkkkkkkxk...",
        "..kik....kik....",
        "...k..kk..k.....",
        "......kGk.......",
    ], 0, 2)
    # lens glint, vents on the barrel
    px(a, 12, 6, "n")
    for x in (4, 6, 8):
        px(a, x, 9, "x")
    # yoke + pole
    rect(a, 3, 8, 3, 13, "G"); rect(a, 2, 8, 2, 13, "k")
    rect(a, 6, 14, 7, 23, "k"); px(a, 6, 15, "j"); rect(a, 6, 16, 6, 23, "I")
    # the light: a soft warm cone spilling off to the right (low alpha)
    for t in range(1, 6):
        for dy in range(-t // 2 - 1, t // 2 + 2):
            x, y = 14 + t // 2, 7 + dy
            if 0 <= x < 16 and a[y, x, 3] == 0:
                a[y, x] = [255, 240, 168, 70]
    # tripod
    stamp(a, [
        ".....kkkk.......",
        "....kjkkjk......",
        "...kjk..kjk.....",
        "..kjk....kjk....",
        ".kjk......kjk...",
        "kkk........kkk..",
    ], 0, 24)
    contact(a, 0, 14, 31)
    return img(a)


def cog_heap():
    """2x1 a heap of spare brass cogs (and a stray spring) swept into a pile."""
    a = canvas(2, 1)
    gear(a, 23.0, 7.0, 5.6, 6, fill="G", hi="y", lo="g", phase=0.25)
    gear(a, 10.0, 7.0, 6.6, 7)
    gear(a, 18.0, 12.0, 3.2, 4, fill="o", hi="O", lo="W", phase=0.4)
    gear(a, 3.0, 12.5, 2.6, 4, fill="G", hi="y", lo="g", phase=0.1)
    # a spring lying in the heap
    for x in range(24, 31):
        px(a, x, 14, "k"); px(a, x, 13, "j" if x % 2 else "I")
    contact(a, 0, 31, 15)
    return img(a)


def tea_urn():
    """2x2 the Old Light's tea-urn automaton: a proper brass urn with a little
    face (dial eyes, a moustache), steam from the lid, a tap with a drip, and
    a cup waiting on each side. The tower's rest point."""
    a = canvas(2, 2)
    # steam wisps (soft)
    for (x, y) in ((15, 0), (16, 1), (15, 2), (17, 0), (18, 2)):
        a[y, x] = [255, 255, 255, 120]
    # lid + knob
    stamp(a, [
        "......kk......",
        ".....kyGk.....",
        "...kkkkkkkk...",
        "..kyyyyyyGGk..",
    ], 9, 2)
    # body: a rounded brass barrel
    shape(a, lambda x, y: (((x - 15.5) / 9.4) ** 2 + ((y - 15.5) / 11) ** 4 <= 1.0)
          and 6 <= y <= 24, "G", hi="y", lo="g", box=(4, 5, 27, 25))
    # brass bands
    for y in (9, 21):
        for x in range(7, 25):
            if a[y, x, 3] and tuple(a[y, x, :3]) not in (tuple(rgba(PAL["k"])[:3]),):
                px(a, x, y, "g")
    # a vertical sheen
    for y in range(10, 21):
        px(a, 10, y, "Y") if y % 3 else None
    # the face: two dial eyes, rosy cheeks, a curled moustache, a smile
    for ex in (12, 19):
        stamp(a, [".kk.", "kPPk", "kPkk", ".kk."], ex - 1, 11)
    px(a, 11, 15, "s"); px(a, 21, 15, "s")
    stamp(a, ["kk.kk.kk", ".kkkkkk."], 12, 15)
    stamp(a, ["kx..xk"[::1]], 13, 17)
    px(a, 14, 18, "k"); px(a, 15, 18, "k"); px(a, 16, 18, "k"); px(a, 17, 18, "k")
    # the tap + a drip
    stamp(a, ["kkkkk", "kjJjk", ".kkjk", "...kk"], 14, 21)
    px(a, 17, 25, "c")
    # stubby feet + the base tray
    rect(a, 3, 26, 28, 28, "k"); rect(a, 4, 26, 27, 26, "y"); rect(a, 4, 27, 27, 27, "G")
    for x in (6, 24):
        rect(a, x, 29, x + 2, 30, "k"); px(a, x + 1, 29, "g")
    # a cup and saucer each side, on the tray
    for cx in (2, 24):
        stamp(a, ["kPPPPk", "kPbPPkk", ".kPPk.k", "kkkkkk"], cx, 22)
    contact(a, 1, 30, 31)
    return img(a)


# =============================================================================
#  FLOOR DECALS (walk-on, solid:false, no contact shadow)
# =============================================================================
def whoopee():
    """1x1 a whoopee cushion lying in wait."""
    a = canvas(1, 1)
    shape(a, ellipse(6.5, 9, 5.5, 3.8), "m", hi="P", lo="M", box=(0, 3, 14, 14))
    stamp(a, ["kkk.", "kmMk", "kkk."], 11, 8)
    px(a, 15, 9, "k")
    # tiny 'pfft' lines
    px(a, 4, 3, "P"); px(a, 7, 2, "P"); px(a, 10, 3, "P")
    return img(a)


def banana():
    """1x1 a banana peel, splayed flat, its tips gone brown."""
    a = canvas(1, 1)
    stamp(a, [
        "......kk........",
        "......kwk.......",
        ".....kzzk.......",
        ".....kzzk.......",
        "....kzppzk......",
        "...kzpppPzk.....",
        "..kzzpppPzzk....",
        ".kzzkzppzkzzk...",
        "kzzk.kzzk.kzzk..",
        "kzk..kzzk..kzzk.",
        "kZk..kzZk...kZzk",
        "kwk...kZk....kwk",
        ".k....kwk.....k.",
        "......kk........",
    ], 0, 1)
    return img(a)


def confetti():
    """1x1 a sprinkle of confetti and a curl of paper streamer."""
    a = canvas(1, 1)
    rng = np.random.default_rng(7)
    cols = ["r", "z", "b", "e", "m", "f", "a", "P"]
    spots = [(1, 2), (5, 1), (10, 3), (14, 1), (3, 7), (8, 6), (12, 8),
             (2, 12), (6, 13), (11, 12), (14, 14), (7, 10), (13, 5)]
    for i, (x, y) in enumerate(spots):
        ch = cols[i % len(cols)]
        px(a, x, y, ch)
        if rng.random() < 0.5:
            px(a, x + 1, y, ch)
        else:
            px(a, x, y + 1, ch)
    # streamer curl
    for (x, y) in ((4, 9), (5, 9), (6, 8), (7, 8), (8, 9), (8, 10), (9, 11), (10, 10)):
        px(a, x, y, "b")
    return img(a)


def _wax(flip: bool):
    a = canvas(1, 1)
    # a thin wash of polish over the whole tile (reads as a wet sheen on any
    # floor pattern) + two hard diagonal glints, one long, one short
    a[:, :] = rgba("#dff4ff", 70)
    long_ = [(2 + i, 12 - i) for i in range(8)]
    short = [(9 + i, 14 - i) for i in range(4)]
    for (x, y) in long_ + short:
        if flip:
            x = 15 - x
        a[y, x] = rgba("#ffffff", 220)
        if 0 <= y + 1 < 16:
            a[y + 1, x] = rgba("#bfe6ff", 150)
    return img(a)


def wax_shine():
    """1x1 a freshly waxed floor: a cool sheen + glints (F5's glare-ice lane)."""
    return _wax(False)


def wax_shine_b():
    """1x1 the same polish, glints mirrored (alternate so the lane never tiles)."""
    return _wax(True)


# =============================================================================
#  WALL-HUNG (face row, solid:false) — drawn inside the 16px wall-face band
# =============================================================================
def mask_wall():
    """1x1 comedy and tragedy, hung together on a red ribbon."""
    a = canvas(1, 1)
    # ribbon + nail
    px(a, 7, 0, "k")
    rect(a, 4, 1, 11, 1, "r"); px(a, 7, 1, "R")
    # tragedy (behind, silver, frowning) right
    stamp(a, [
        ".kkkkkk.",
        "kJjjjjjk",
        "kjxjjxjk",
        "kjxjjxjk",
        "kjcjjjjk",
        "kjxxxxjk",
        "kxjjjjxk",
        ".kjjjjk.",
        "..kkkk..",
    ], 8, 3)
    # comedy (front, gold, grinning) left
    stamp(a, [
        ".kkkkkk.",
        "kYyyyyyk",
        "kykyykyk",
        "kxyyyyxk",
        "kyyyyyyk",
        "kxyyyyxk",
        "kyxxxxyk",
        ".kyxxyk.",
        "..kkkk..",
    ], 1, 3)
    return img(a)


def applause_sign():
    """2x1 the lit APPLAUSE box sign, bulbs round the frame, on two chains."""
    a = canvas(2, 1)
    # chains
    for x in (6, 25):
        px(a, x, 0, "j"); px(a, x, 1, "I")
    rect(a, 0, 2, 31, 14, "k")
    rect(a, 1, 3, 30, 13, "R")
    rect(a, 1, 4, 30, 12, "Y")
    rect(a, 1, 5, 30, 11, "z")
    rect(a, 1, 4, 30, 4, "Y")
    # bulbs along the frame
    for x in range(2, 30, 3):
        px(a, x, 3, "Y"); px(a, x + 1, 13, "Y")
    # the word
    text(a, "APPLAUSE", 1, 6, "R")
    return img(a)


def bunting():
    """2x1 striped pennant bunting looped across the wall face."""
    a = canvas(2, 1)
    W = 32
    def sag(x):
        return round(2 + 3.0 * math.sin(math.pi * x / (W - 1)))
    for x in range(W):
        px(a, x, sag(x), "q")
    flags = [("r", "P"), ("b", "P"), ("z", "r"), ("e", "P"), ("m", "P")]
    for i, x0 in enumerate(range(1, W - 4, 6)):
        c1, c2 = flags[i % len(flags)]
        top = sag(x0 + 2) + 1
        for dy in range(0, 8):
            half = 2 - dy * 2 // 7
            for dx in range(-half, half + 1):
                x = x0 + 2 + dx
                edge = abs(dx) == half or dy == 0
                px(a, x, top + dy, "k" if edge and dy != 0 else (c1 if (x // 1) % 2 else c2))
        px(a, x0 + 2, top + 8, "k")
    return img(a)


def clock_backwards():
    """1x1 a wall clock with its numbers the wrong way round (21 at the top)
    and a little red arrow insisting the hands go anticlockwise."""
    a = canvas(1, 1)
    shape(a, ellipse(7.5, 7.5, 7.5, 7.5), "G", hi="y", lo="g", box=(0, 0, 15, 15))
    for y in range(16):
        for x in range(16):
            if ((x - 7.5) ** 2 + (y - 7.5) ** 2) <= 5.6 ** 2:
                px(a, x, y, "P")
    text(a, "21", 5, 2, "x")
    px(a, 2, 8, "x"); px(a, 13, 8, "x"); px(a, 8, 13, "x")
    # hands
    rect(a, 7, 8, 8, 9, "k")
    px(a, 6, 9, "k"); px(a, 5, 10, "k")
    px(a, 9, 7, "r"); px(a, 10, 6, "r")
    # the backwards arrow, bottom-left
    px(a, 4, 11, "r"); px(a, 5, 12, "r"); px(a, 3, 11, "r"); px(a, 4, 10, "r")
    return img(a)


# =============================================================================
#  WALL-MOUNTED (top row over the wall face; overhang 1, walk_under)
# =============================================================================
def funhouse_mirror():
    """1x2 a funhouse mirror in a bulb-studded carnival frame; the glass
    ripples and the reflection is a long, thin, very surprised wayfarer."""
    a = canvas(1, 2)
    # frame (rounded top), red with gold edge
    shape(a, lambda x, y: 1 <= x <= 14 and 0 <= y <= 28 and not
          (y < 3 and (x - 7.5) ** 2 / 42 + (y - 3) ** 2 / 9 > 1), "r", hi="s", lo="R",
          box=(0, 0, 15, 29))
    # the glass: rippling cool bands
    for y in range(3, 26):
        off = round(1.2 * math.sin(y / 2.2))
        for x in range(3, 13):
            if (x - 7.5) ** 2 / 20 + (y - 4) ** 2 / 4 > 1 and y < 4:
                continue
            band = (x + off) % 5
            px(a, x, y, "c" if band in (0, 1) else "a" if band == 2 else "J")
    # the stretched reflection: a tall wobbly figure
    for y in range(7, 24):
        off = round(1.5 * math.sin(y / 2.0))
        px(a, 7 + off, y, "B"); px(a, 8 + off, y, "B")
    shape(a, ellipse(7.5 + round(1.5 * math.sin(3)), 5.5, 1.6, 2.2), "h", ink="B",
          box=(4, 2, 11, 9))
    # gold bulbs round the frame
    for y in range(4, 27, 4):
        px(a, 1, y, "Y"); px(a, 14, y, "Y")
    for x in (4, 7, 11):
        px(a, x, 1, "Y")
    # feet on the floor row
    stamp(a, ["kGk......kGk", "kkk......kkk"], 2, 28)
    rect(a, 2, 27, 13, 27, "k"); rect(a, 3, 27, 12, 27, "G")
    contact(a, 1, 14, 31)
    return img(a)


# =============================================================================
#  THE HERO PIECE — Mr. Punchwheel himself (free-standing, solid)
# =============================================================================
def punchwheel_drum():
    """4x5 MR. PUNCHWHEEL: Tam Wash's clockwork joke-engine, set where the
    lamp used to be. A great varnished drum studded with brass pegs and
    punched joke-cards turns on a wooden frame; cogs mesh at its left end, a
    crank waits at its right, a red bellows wheezes underneath, three tin
    lamplighters stand on the top rail, and over it all a cheeky brass grin
    plate (dial eyes, a waxed moustache) beams at whoever is listening."""
    a = canvas(4, 5)
    W_, H_ = 64, 80
    # --- the frame: two wooden uprights + a plinth --------------------------
    for x0 in (4, 56):
        rect(a, x0, 22, x0 + 3, 72, "k")
        rect(a, x0 + 1, 23, x0 + 1, 71, "O")
        rect(a, x0 + 2, 23, x0 + 2, 71, "o")
        # brass bracket where the axle sits
        rect(a, x0 - 1, 38, x0 + 4, 44, "k"); rect(a, x0, 39, x0 + 3, 43, "G")
        rect(a, x0, 39, x0 + 3, 39, "y")
    # the top rail (the tin lamplighters stand on it)
    rect(a, 2, 20, 61, 24, "k"); rect(a, 3, 21, 60, 21, "O")
    rect(a, 3, 22, 60, 23, "o"); rect(a, 3, 23, 60, 23, "W")
    for x in range(6, 60, 8):
        px(a, x, 22, "y")                              # brass rivets
    # plinth (bottom row = floor contact)
    rect(a, 1, 70, 62, 77, "k")
    rect(a, 2, 71, 61, 71, "O"); rect(a, 2, 72, 61, 74, "o")
    rect(a, 2, 75, 61, 76, "W")
    rect(a, 2, 73, 61, 73, "G")                        # a brass inlay line
    for x in range(5, 60, 6):
        px(a, x, 73, "y")
    # --- the bellows under the drum ------------------------------------------
    for i, y in enumerate(range(56, 69, 2)):
        inset = 2 if i % 2 else 0
        rect(a, 18 + inset, y, 45 - inset, y + 1, "k")
        rect(a, 19 + inset, y, 44 - inset, y, "r" if i % 2 else "s")
        rect(a, 19 + inset, y + 1, 44 - inset, y + 1, "R")
    rect(a, 16, 54, 47, 56, "k"); rect(a, 17, 55, 46, 55, "o")   # top board
    rect(a, 16, 68, 47, 70, "k"); rect(a, 17, 69, 46, 69, "W")   # bottom board
    # --- the drum --------------------------------------------------------------
    dx0, dx1, dy0, dy1 = 10, 53, 29, 53
    cy = (dy0 + dy1) / 2
    ry = (dy1 - dy0) / 2
    # body: shaded by height (a horizontal cylinder lit from above)
    for y in range(dy0, dy1 + 1):
        t = (y - dy0) / (dy1 - dy0)
        ch = "O" if t < 0.18 else "o" if t < 0.55 else "W" if t < 0.85 else "w"
        rect(a, dx0, y, dx1, y, ch)
    rect(a, dx0, dy0 - 1, dx1, dy0 - 1, "k"); rect(a, dx0, dy1 + 1, dx1, dy1 + 1, "k")
    # punched joke-cards wrapped round the drum (cream, with holes); squashed
    # near the top/bottom where the drum turns away from us
    cards = [(13, 0), (21, 1), (29, 0), (37, 1), (45, 0)]
    for (cx0, ph) in cards:
        top, bot = dy0 + 3 + ph * 2, dy1 - 4 + ph
        rect(a, cx0, top, cx0 + 5, bot, "k")
        rect(a, cx0 + 1, top + 1, cx0 + 4, bot - 1, "P")
        rect(a, cx0 + 1, top + 1, cx0 + 4, top + 1, "n")
        rect(a, cx0 + 4, top + 2, cx0 + 4, bot - 1, "q")
        # the card turns away from us top and bottom: shade the ends
        rect(a, cx0 + 1, bot - 3, cx0 + 4, bot - 1, "q")
        rect(a, cx0 + 1, bot - 1, cx0 + 4, bot - 1, "H")
        for y in range(top + 3, bot - 1, 3):
            px(a, cx0 + 1 + ((y + cx0) % 3), y, "x")
            if (y + ph) % 2:
                px(a, cx0 + 3, y + 1, "x")
    # brass pegs studded between the cards
    for x in range(12, 53, 4):
        for y in range(dy0 + 2, dy1 - 1, 4):
            if a[y, x, 0] == rgba(PAL["P"])[0] or a[y, x, 0] == rgba(PAL["k"])[0]:
                continue
            px(a, x, y, "Y" if y < cy else "y")
            px(a, x, y + 1, "g")
    # brass hoops round each end of the drum
    for x0 in (dx0 + 1, dx1 - 3):
        for y in range(dy0, dy1 + 1):
            t = (y - dy0) / (dy1 - dy0)
            px(a, x0, y, "Y" if t < 0.3 else "y" if t < 0.6 else "G")
            px(a, x0 + 1, y, "y" if t < 0.3 else "G" if t < 0.6 else "g")
            px(a, x0 + 2, y, "k" if y in (dy0, dy1) else "g")
    # end caps (the drum's round faces, seen almost edge-on)
    shape(a, ellipse(dx0 - 1, cy, 2.6, ry + 0.8), "G", hi="y", lo="g",
          box=(dx0 - 5, dy0 - 2, dx0 + 1, dy1 + 2))
    shape(a, ellipse(dx1 + 1, cy, 2.6, ry + 0.8), "G", hi="y", lo="g",
          box=(dx1 - 1, dy0 - 2, dx1 + 5, dy1 + 2))
    # axle stubs into the brackets
    px(a, 7, 41, "x"); px(a, 8, 41, "x"); px(a, 55, 41, "x"); px(a, 56, 41, "x")
    # --- cogs meshing at the left end ------------------------------------------
    gear(a, 8.0, 54.0, 5.4, 7, phase=0.2)
    gear(a, 15.0, 62.0, 3.6, 6, fill="G", hi="y", lo="g", phase=0.5)
    gear(a, 6.0, 64.5, 2.6, 5, fill="o", hi="O", lo="W", phase=0.0)
    # --- the crank at the right end ---------------------------------------------
    stamp(a, [
        "kkk.....",
        "kjJk....",
        ".kjJk...",
        "..kjJk..",
        "...kjJk.",
        "....kjkk",
        ".....krk",
        ".....krk",
        ".....krk",
        ".....kRk",
        "......k.",
    ], 56, 42)
    # --- three tin lamplighters on the top rail ---------------------------------
    for i, fx in enumerate((8, 48)):
        _tin_lamplighter(a, fx, 7, raise_left=(i == 1))
    # --- the brass grin plate (Mr. Punchwheel's face), centre top ----------------
    face = lambda x, y: ((x - 31.5) / 13.5) ** 2 + ((y - 11.5) / 10.5) ** 2 <= 1.0
    shape(a, face, "G", hi="y", lo="g", box=(16, 0, 47, 23))
    # a polished highlight crescent
    for y in range(3, 9):
        px(a, 22 + (y - 3) // 2, y, "Y")
    # dial eyes
    for ex in (26, 37):
        stamp(a, [".kkk.", "kPPPk", "kPkPk", "kPPkk", ".kkk."], ex - 2, 6)
    # rosy cheeks
    px(a, 21, 13, "s"); px(a, 22, 13, "s"); px(a, 41, 13, "s"); px(a, 42, 13, "s")
    # waxed moustache curling up at the tips
    stamp(a, [
        "w..............w",
        "ww............ww",
        ".wwww......wwww.",
        "..wWWww..wwWWw..",
    ], 24, 11)
    # the big cheeky grin (open, with a row of brass teeth)
    stamp(a, [
        "kk..........kk",
        ".kkkkkkkkkkkk.",
        ".knnnnnnnnnnk.",
        "..kxxxxxxxxk..",
        "...kkrrrrkk...",
        ".....kkkk.....",
    ], 25, 15)
    # a brass winding key in the top of his head
    stamp(a, ["kk.kk", "kykyk", ".kGk."], 29, 0)
    # the third tin lamplighter stands on the plinth, minding the bellows
    _tin_lamplighter(a, 48, 58)
    # --- floor contact ------------------------------------------------------
    contact(a, 0, 63, 79, alpha=110)
    return img(a)


def _tin_lamplighter(a, ox, oy, *, raise_left=False, small=False):
    """A wee tin lamplighter figure (6-7px wide) holding up a lit lamp-pole."""
    if small:
        stamp(a, [
            ".Y....",
            "kyk...",
            ".k.kk.",
            "..kjjk",
            "..kJjk",
            ".kbbbk",
        ], ox, oy)
        return
    fig = [
        "....Y..",
        "...kyk.",
        "....k..",
        "..kkk.k",
        ".kxxxkk",
        "..kJjkk",
        "..kjjk.",
        ".kbBbbk",
        "kjbbbbk",
        ".kbbbk.",
        ".kbkbk.",
        ".kk.kk.",
    ]
    stamp(a, fig, ox, oy, flip=raise_left)
    # brass winding key in the back
    px(a, ox + (7 if not raise_left else -1), oy + 8, "G")


# =============================================================================
#  THE GALLERY OF CONFIDENT FACTS (F5) — wall-hung 1x2 paintings
# =============================================================================
def _frame(a, *, gilt=True):
    """Cord + nail + a 14x24 frame; returns the picture box (x0,y0,x1,y1)."""
    # nail and picture cord
    px(a, 7, 0, "k"); px(a, 8, 0, "k")
    for t in range(0, 4):
        px(a, 6 - t, 1 + t // 1 if t < 3 else 3, "q")
        px(a, 9 + t, 1 + t // 1 if t < 3 else 3, "q")
    x0, y0, x1, y1 = 1, 4, 14, 28
    rect(a, x0, y0, x1, y1, "k")
    if gilt:
        rect(a, x0 + 1, y0 + 1, x1 - 1, y1 - 1, "G")
        rect(a, x0 + 1, y0 + 1, x1 - 1, y0 + 1, "Y")
        rect(a, x0 + 1, y0 + 1, x0 + 1, y1 - 1, "y")
        rect(a, x0 + 1, y1 - 1, x1 - 1, y1 - 1, "g")
        rect(a, x1 - 1, y0 + 2, x1 - 1, y1 - 1, "g")
        # ornate corner knobs
        for (cx, cy) in ((x0 + 1, y0 + 1), (x1 - 1, y0 + 1), (x0 + 1, y1 - 1), (x1 - 1, y1 - 1)):
            px(a, cx, cy, "Y")
    else:
        rect(a, x0 + 1, y0 + 1, x1 - 1, y1 - 1, "W")
        rect(a, x0 + 1, y0 + 1, x1 - 1, y0 + 1, "o")
        rect(a, x0 + 1, y0 + 1, x0 + 1, y1 - 1, "o")
        rect(a, x0 + 1, y1 - 1, x1 - 1, y1 - 1, "w")
        rect(a, x1 - 1, y0 + 2, x1 - 1, y1 - 1, "w")
    # inner ink line
    rect(a, x0 + 2, y0 + 2, x1 - 2, y1 - 2, "k")
    # the little brass caption plate under it
    rect(a, 5, 29, 10, 31, "k"); rect(a, 6, 30, 9, 30, "y")
    return (x0 + 3, y0 + 3, x1 - 3, y1 - 3)   # 3..12 x 7..25


def painting_reyl():
    """PORTRAIT OF REYL WASH, AGED 9, AS A LIGHTHOUSE: a red-and-cream
    striped tower whose lamp room is a gap-toothed boy's grinning face,
    a red dome hat on top, beams shining out of his ears."""
    a = canvas(1, 2)
    x0, y0, x1, y1 = _frame(a)
    rect(a, x0, y0, x1, y1, "B")
    px(a, 4, 22, "c"); px(a, 11, 20, "c")
    rect(a, x0, y1 - 1, x1, y1, "b")              # sea
    px(a, 4, y1 - 1, "c"); px(a, 11, y1, "c")
    # the beams (soft yellow wedges either side of the lamp room)
    for (x, y) in ((3, 12), (3, 13), (4, 12), (4, 13), (3, 14),
                   (12, 12), (12, 13), (11, 12), (11, 13), (12, 11)):
        px(a, x, y, "y")
    px(a, 3, 13, "Y"); px(a, 12, 12, "Y")
    # the tower: banded, widening toward the rock
    for y in range(17, y1 - 1):
        half = 1 if y < 21 else 2
        ch = "r" if ((y - 17) // 2) % 2 == 0 else "P"
        rect(a, 7 - half, y, 8 + half, y, ch)
        px(a, 7 - half - 1, y, "k"); px(a, 8 + half + 1, y, "k")
    # gallery rail
    rect(a, 4, 16, 11, 16, "k"); rect(a, 5, 16, 10, 16, "j")
    # the lamp room = his face
    rect(a, 5, 11, 10, 15, "h")
    px(a, 6, 12, "k"); px(a, 9, 12, "k")          # eyes
    px(a, 5, 14, "s"); px(a, 10, 14, "s")         # freckly cheeks
    rect(a, 6, 14, 9, 14, "k"); px(a, 8, 14, "n") # grin, one tooth missing
    px(a, 7, 15, "H"); px(a, 8, 15, "H")
    # the red dome roof as a hat, with a vane and his hair sticking out
    rect(a, 5, 10, 10, 10, "k")
    rect(a, 6, 9, 9, 9, "r"); px(a, 5, 9, "k"); px(a, 10, 9, "k")
    rect(a, 7, 8, 8, 8, "R")
    px(a, 7, 7, "k"); px(a, 8, 6, "y")
    px(a, 4, 11, "w"); px(a, 11, 11, "w")         # tufts
    return img(a)


def painting_tuesday():
    """A MAP OF TUESDAY: a parchment chart of an island shaped like a 'T',
    a dotted route, an X, and a compass point."""
    a = canvas(1, 2)
    x0, y0, x1, y1 = _frame(a)
    rect(a, x0, y0, x1, y1, "c")                  # sea
    for (x, y) in ((4, 22), (11, 24), (10, 8)):
        px(a, x, y, "b")
    # the T-shaped island
    shape(a, lambda x, y: (4 <= x <= 11 and 9 <= y <= 12) or (6 <= x <= 9 and 12 <= y <= 22),
          "p", hi="P", lo="q", ink="o", box=(x0, y0, x1, y1))
    # dotted route + the X
    for (x, y) in ((5, 11), (7, 11), (8, 13), (8, 15), (7, 17), (8, 19)):
        px(a, x, y, "r")
    px(a, 7, 21, "R"); px(a, 8, 20, "R"); px(a, 8, 21, "R"); px(a, 7, 20, "R")
    # a tiny tree, a compass point
    px(a, 10, 10, "e"); px(a, 10, 11, "w")
    px(a, 11, 18, "k"); px(a, 11, 17, "r"); px(a, 10, 19, "k"); px(a, 12, 19, "k"); px(a, 11, 20, "k")
    return img(a)


def painting_stars():
    """PICTURES OF VESPERHOLM FROM ABOVE THE STARS: entirely black. (A faint
    sheen says it is, technically, paint.)"""
    a = canvas(1, 2)
    x0, y0, x1, y1 = _frame(a)
    rect(a, x0, y0, x1, y1, "x")
    rect(a, x0, y0, x1, y0, "k")
    # a glossy sheen stroke top-left, so it reads as a painted canvas
    px(a, x0 + 1, y0 + 2, "i"); px(a, x0 + 2, y0 + 1, "i"); px(a, x0 + 1, y0 + 3, "i")
    return img(a)


def painting_sea():
    """THE SEA (SMALL): a big cream canvas and, in the middle of it, the sea —
    about two waves' worth."""
    a = canvas(1, 2)
    x0, y0, x1, y1 = _frame(a)
    rect(a, x0, y0, x1, y1, "P")
    rect(a, x0, y1, x1, y1, "p")
    # the sea itself
    stamp(a, [
        ".kkk.",
        "kbcbk",
        "kBbbk",
        ".kkk.",
    ], 5, 14)
    px(a, 7, 15, "n")
    # a tiny boat bobbing on it
    px(a, 8, 13, "w")
    return img(a)


def painting_gerald():
    """KIN No. 0, 'GERALD': medium, Gerald-coloured, mostly Gerald — an
    unremarkable beige blob with dot eyes, looking pleased to be discovered."""
    a = canvas(1, 2)
    x0, y0, x1, y1 = _frame(a)
    rect(a, x0, y0, x1, y1, "e")
    rect(a, x0, 20, x1, y1, "E")                  # a horizon of grass
    shape(a, ellipse(7.5, 17.5, 3.6, 4.4), "H", hi="h", lo="o",
          box=(x0, y0, x1, y1))
    px(a, 6, 16, "k"); px(a, 9, 16, "k")         # dot eyes
    px(a, 7, 18, "k"); px(a, 8, 18, "k")         # a contented little mouth
    px(a, 6, 22, "k"); px(a, 9, 22, "k")         # two stubby feet
    # a tiny gold "No. 0" rosette in the corner, because it's official
    px(a, 11, 8, "y"); px(a, 10, 8, "r"); px(a, 11, 9, "r")
    return img(a)


def painting_ferry():
    """TAM AND REYL WASH, FERRY 'SAME TIDE TOMORROW': the one true picture. A
    finer dark-wood frame with a thin gilt slip; a little ferry on a night
    sea, its bow lamp warm, two small figures aboard, a star overhead."""
    a = canvas(1, 2)
    x0, y0, x1, y1 = _frame(a, gilt=False)
    # thin gilt slip inside the wood
    rect(a, x0 - 1, y0 - 1, x1 + 1, y0 - 1, "y")
    rect(a, x0 - 1, y0 - 1, x0 - 1, y1 + 1, "G")
    rect(a, x0 - 1, y1 + 1, x1 + 1, y1 + 1, "g")
    rect(a, x1 + 1, y0, x1 + 1, y1 + 1, "g")
    # night sky (graded) and sea
    for y in range(y0, y1 + 1):
        rect(a, x0, y, x1, y, "x" if y < 10 else "B" if y < 12 or y > 18 else "b")
    for (x, y) in ((4, 8), (9, 10), (11, 8), (3, 12)):
        px(a, x, y, "c")
    px(a, 6, 9, "Y")                              # the one bright star
    # gentle wave crests
    for (x, y) in ((4, 23), (5, 23), (7, 25), (8, 25), (6, 21)):
        px(a, x, y, "c")
    # the ferry: a little cabin with a lit window, two figures on deck
    # (Tam's red scarf), and the bow lamp up on its pole
    stamp(a, [
        "......Y.",
        ".....YnY",
        ".PP...w.",
        ".Py.h.w.",
        "OOOOrhwO",
        "kOOOOOok",
        ".kWWWWk.",
        "..kkkk..",
    ], 4, 13)
    for (x, y, ch) in ((10, 21, "y"), (9, 22, "G"), (10, 23, "y"), (9, 24, "g"), (10, 25, "g")):
        px(a, x, y, ch)
    return img(a)


# =============================================================================
#  THE STAGE — wall-hung velvet curtain swags (used as a mirrored pair)
# =============================================================================
def stage_curtain():
    """1x2 a red velvet theatre curtain, gathered to the LEFT and tied back
    with a gold rope and tassel, under a fringed pelmet."""
    a = canvas(1, 2)
    # the curtain body: drapes from the full top width, sweeping to the
    # left edge where it's tied at y=18, then falling straight to the hem
    def inside(x, y):
        if y < 3 or y > 30:
            return False
        if y <= 18:
            edge = 15 - (y - 3) * 10 / 15      # right edge sweeps left
            return x <= edge
        return x <= 5 + (y - 18) * 0.25
    for y in range(3, 31):
        for x in range(16):
            if not inside(x, y):
                continue
            ch = "R" if (x % 4 == 3) else "r" if (x % 4 in (1, 2)) else "s"
            if not inside(x + 1, y):
                ch = "k"
            px(a, x, y, ch)
    # pleat shadow under the tie-back
    rect(a, 0, 19, 4, 19, "R")
    # gold rope + tassel at the tie
    rect(a, 0, 17, 6, 18, "k"); rect(a, 0, 17, 5, 17, "y"); rect(a, 0, 18, 5, 18, "G")
    stamp(a, [
        ".kk.",
        "kyGk",
        ".kk.",
        "kyyk",
        "kyGk",
        "kGgk",
        ".kk.",
    ], 5, 18)
    # the pelmet across the top with a gold fringe
    rect(a, 0, 0, 15, 3, "k"); rect(a, 0, 1, 15, 2, "R"); rect(a, 0, 1, 15, 1, "r")
    for x in range(0, 16):
        px(a, x, 4, "y" if x % 2 == 0 else "G")
        if x % 2 == 0:
            px(a, x, 5, "G")
    # the hem
    rect(a, 0, 31, 6, 31, "y")
    return img(a)


def stage_curtain_r():
    """1x2 the mirror twin: gathered to the RIGHT."""
    return stage_curtain().transpose(Image.FLIP_LEFT_RIGHT)



PIECES = {
    # free-standing (solid)
    "jack_box": jack_box, "rubber_chickens": rubber_chickens, "pie_table": pie_table,
    "clown_shoes": clown_shoes, "joke_lectern": joke_lectern, "mallet": mallet,
    "laugh_dolls": laugh_dolls, "laugh_meter": laugh_meter, "teacups": teacups,
    "unicycle": unicycle, "spring_can": spring_can, "upside_chair": upside_chair,
    "spotlight": spotlight, "cog_heap": cog_heap, "tea_urn": tea_urn,
    # floor decals (solid:false, no shadow)
    "whoopee": whoopee, "banana": banana, "confetti": confetti,
    "wax_shine": wax_shine, "wax_shine_b": wax_shine_b,
    # wall-hung (face row, solid:false)
    "mask_wall": mask_wall, "applause_sign": applause_sign, "bunting": bunting,
    "clock_backwards": clock_backwards,
    # wall-mounted (overhang 1, walk_under)
    "funhouse_mirror": funhouse_mirror,
    # the hero piece (free-standing, solid)
    "punchwheel_drum": punchwheel_drum,
    # the F5 gallery + the stage (wall-hung, solid:false)
    "painting_reyl": painting_reyl, "painting_tuesday": painting_tuesday,
    "painting_stars": painting_stars, "painting_sea": painting_sea,
    "painting_gerald": painting_gerald, "painting_ferry": painting_ferry,
    "stage_curtain": stage_curtain, "stage_curtain_r": stage_curtain_r,
}

# the placement contract (w, h in tiles) — asserted on every draw
FOOTPRINT = {
    "jack_box": (1, 1), "rubber_chickens": (1, 2), "pie_table": (2, 1),
    "clown_shoes": (2, 1), "joke_lectern": (1, 2), "mallet": (1, 2),
    "laugh_dolls": (2, 2), "laugh_meter": (1, 2), "teacups": (1, 2),
    "unicycle": (1, 2), "spring_can": (1, 1), "upside_chair": (1, 1),
    "spotlight": (1, 2), "cog_heap": (2, 1), "tea_urn": (2, 2),
    "whoopee": (1, 1), "banana": (1, 1), "confetti": (1, 1),
    "wax_shine": (1, 1), "wax_shine_b": (1, 1),
    "mask_wall": (1, 1), "applause_sign": (2, 1), "bunting": (2, 1),
    "clock_backwards": (1, 1), "funhouse_mirror": (1, 2),
    "punchwheel_drum": (4, 5),
    "painting_reyl": (1, 2), "painting_tuesday": (1, 2), "painting_stars": (1, 2),
    "painting_sea": (1, 2), "painting_gerald": (1, 2), "painting_ferry": (1, 2),
    "stage_curtain": (1, 2), "stage_curtain_r": (1, 2),
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
        tw, th = FOOTPRINT[stem]
        assert im.size == (tw * 16, th * 16), (stem, im.size)
        im.save(OBJDIR / f"{stem}.png")
        print(f"  drew oldlight_{stem}  ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
