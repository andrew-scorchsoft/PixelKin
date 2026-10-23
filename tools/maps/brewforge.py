#!/usr/bin/env python3
"""
brewforge — the DRAWN kit of the Wakeful Fair, the great coffee festival in the
marquee on Wayward Rise (S7 "Just One More Cup"; builders build_wakeful_fair.py,
content src/game/content/regions/brewfair.ts).

Kept in its OWN master folder, like gymforge/paulforge, so the shared interior kit
(and interiorforge's full re-runs) never touch it:

    assets/tilesets/brewfair/objects/<stem>.png   ->  packed as `brewfair_<stem>`

Projection matches the interior kit: straight-on, top-down-frontal, a 1px ink
outline, a soft contact shadow on the floor row. Every piece is drawn in code
(rects/lines/discs) so it's crisp and deterministic; re-run freely.

  STALLS (3x2, solid):     stall_<kind> — a plank counter (the top surface + a
                           cloth skirt in the stall's colour wearing its icon)
                           with that brewer's kit standing on it. The keeper
                           stands BEHIND it (north); "stall" in the name lets
                           WorldScene's DESK_SPRITE talk across it.
                           kinds: ember pourover press coldbrew sandpot latte
                           mushroom decaf siphon frost dawn midnight nothing
  CENTREPIECE:             grand_urn / grand_urn_awake (4x4, the same footprint:
                           the awake one SINGS — a flag swap, collision unchanged),
                           urn_puddle (1x1, non-solid: the swirl you fall into)
  FURNITURE:               cupping_table 3x2, roaster 3x3, stage 4x2, trophy 1x2,
                           bean_sacks 2x1, aboard 1x1, cup_tower 1x2, cot 1x2,
                           water_table 2x1, tent_pole 1x2, rope_post 1x1
  WALL-HUNG (face row, solid:false): bunting 3x1, banner_<kind> 3x1
  EXTERIOR:                marquee 7x5 (the big striped tent, door on col 3)
  THE DREAM (wakeful_fair_dream): sugar_cube 1x1, bean 1x1, spoon 3x1,
                           teacup 2x2, bottomless 3x3, dream_door 1x2

Run:  python3 tools/maps/brewforge.py [--only a,b] [--preview out.png]
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "brewfair" / "objects"

PAL = {
    "k": "#1a1018",  # ink
    # plank wood (counter tops, tables, stage)
    "w": "#4a2c1a", "W": "#7a4a2a", "o": "#a8703e", "O": "#d09a5c",
    # coffee
    "c": "#2a160c", "C": "#4a2a16", "e": "#8a5a30", "E": "#d8b080", "f": "#f0dcb8",
    # copper / brass
    "p": "#6a3018", "P": "#a85a2a", "q": "#e08a4a", "Q": "#ffc890",
    "b": "#7a5a18", "B": "#c8962a", "g": "#f0d060", "G": "#fff4b0",
    # steel / chrome / glass
    "s": "#3a3e4c", "S": "#6a7084", "t": "#a8b0c0", "T": "#e8eef8",
    "l": "#7ab0c8", "L": "#c8e8f4",  # glass tint + glint
    # cloth / paint
    "r": "#8a1e2a", "R": "#d8384a", "y": "#ffe8c8",  # festival red + cream stripe
    "n": "#1c2a5a", "N": "#3a5aa8",  # navy
    "v": "#4a2a6a", "V": "#8a5ac8",  # violet (siphon)
    "m": "#2a5a2a", "M": "#5a9a48",  # moss green
    "h": "#a83a6a", "H": "#f08ab8",  # latte pink
    "i": "#3a6a8a", "I": "#a8dcf0", "j": "#f4fcff",  # frost
    "a": "#c87818", "A": "#ffc83a",  # dawn gold
    "u": "#14122a", "U": "#2c2a5a",  # midnight indigo
    "x": "#6a6870", "X": "#a8a6ae",  # decaf grey
    "z": "#b85a18", "Z": "#f09a48",  # sand-pot orange
    "d": "#c8a060", "D": "#ecd08c",  # sand
    "F": "#2a8aa0", "K": "#6ad0d8",  # cold-brew teal
    # sugar / porcelain / foam
    "1": "#ffffff", "2": "#e8e4dc", "3": "#b8b0a4", "4": "#7a7068",
    # flame
    "5": "#3a6aff", "6": "#a8d0ff", "7": "#ff7a2a", "8": "#ffd040",
    # tent canvas
    "9": "#5a1420", "0": "#c8b89a",
}


def rgba(hexs: str, alpha: int = 255):
    return np.array([int(hexs[i:i + 2], 16) for i in (1, 3, 5)] + [alpha], dtype=np.int16)


def canvas(tw: int, th: int) -> np.ndarray:
    return np.zeros((th * 16, tw * 16, 4), dtype=np.int16)


def rect(a, x0, y0, x1, y1, ch, alpha=255):
    h, w = a.shape[:2]
    x0, x1 = max(0, x0), min(w - 1, x1)
    y0, y1 = max(0, y0), min(h - 1, y1)
    if x0 <= x1 and y0 <= y1:
        a[y0:y1 + 1, x0:x1 + 1] = rgba(PAL[ch], alpha)


def px(a, x, y, ch, alpha=255):
    h, w = a.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        a[y, x] = rgba(PAL[ch], alpha)


def hline(a, x0, x1, y, ch):
    rect(a, min(x0, x1), y, max(x0, x1), y, ch)


def vline(a, x, y0, y1, ch):
    rect(a, x, min(y0, y1), x, max(y0, y1), ch)


def line(a, x0, y0, x1, y1, ch):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        px(a, round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), ch)


def inked(a, x0, y0, x1, y1, fill, *, hi=None, lo=None):
    """An ink-outlined block: fill, an optional 1px highlight (top) and shadow
    (bottom) inside the outline."""
    rect(a, x0, y0, x1, y1, "k")
    if x1 - x0 >= 2 and y1 - y0 >= 2:
        rect(a, x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)
        if hi:
            rect(a, x0 + 1, y0 + 1, x1 - 1, y0 + 1, hi)
        if lo and y1 - y0 >= 3:
            rect(a, x0 + 1, y1 - 1, x1 - 1, y1 - 1, lo)


def ellipse(a, cx, cy, rx, ry, ch, alpha=255):
    h, w = a.shape[:2]
    for y in range(max(0, int(cy - ry - 1)), min(h, int(cy + ry + 2))):
        for x in range(max(0, int(cx - rx - 1)), min(w, int(cx + rx + 2))):
            if ((x - cx) / max(rx, 0.5)) ** 2 + ((y - cy) / max(ry, 0.5)) ** 2 <= 1.0:
                a[y, x] = rgba(PAL[ch], alpha)


def inked_ellipse(a, cx, cy, rx, ry, fill, hi=None):
    ellipse(a, cx, cy, rx, ry, "k")
    ellipse(a, cx, cy, rx - 1, ry - 1, fill)
    if hi:
        ellipse(a, cx - rx * 0.3, cy - ry * 0.35, max(rx * 0.3, 0.6), max(ry * 0.25, 0.6), hi)


def contact(a, x0, x1, y, alpha=90):
    """Soft floor shadow under a piece (on the canvas's bottom rows)."""
    h = a.shape[0]
    for yy, al in ((y, alpha), (y - 1, alpha // 2)):
        if 0 <= yy < h:
            for x in range(max(0, x0), min(a.shape[1], x1 + 1)):
                if a[yy, x, 3] == 0:
                    a[yy, x] = [10, 6, 12, al]


def steam(a, x, y, n=3):
    """A small curl of steam rising from (x, y) (semi-transparent)."""
    for i in range(n * 3):
        yy = y - i
        xx = x + round(math.sin(i * 0.9) * 1.2)
        px(a, xx, yy, "1", alpha=150 - i * 12 if 150 - i * 12 > 40 else 40)


def img(a) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# ---- tiny glyphs (stall icons, 9x9; '#' = ink colour, '+' = light) -----------------
ICONS = {
    "ember": ["....+....", "...+#+...", "..+###+..", "..#####..", ".#######.",
              ".##+#+##.", "..#####..", "...###...", "........."],          # flame
    "pourover": ["#########", ".#######.", "..#####..", "...###...", "....#....",
                 "...###...", "..#...#..", "..#...#..", "..#####.."],      # cone on a carafe
    "press": ["...###...", "....#....", ".#######.", ".#.....#.", ".#+++++#.",
              ".#+++++#.", ".#+++++#.", ".#######.", "........."],         # press pot
    "coldbrew": ["....#....", "...###...", "...###...", "..#####..", "..##+##..",
                 ".###+###.", ".#######.", "..#####..", "........."],      # drop
    "sandpot": ["#........", ".#.......", "..#####..", "..#+++#..", ".#######.",
                ".#######.", "..#####..", "...###...", "........."],       # long-handled pot
    "latte": [".##...##.", "####.####", "#########", "#########", ".#######.",
              "..#####..", "...###...", "....#....", "........."],         # heart
    "mushroom": ["..#####..", ".###+###.", "###+####+", "#########", "...###...",
                 "...###...", "...###...", "..#####..", "........."],      # mushroom
    "decaf": ["#####....", "...#.....", "..#......", ".#.......", "#####.###",
              "........#", ".......#.", "......#..", "......###"],         # z z
    "siphon": ["..#####..", "..#+++#..", "...#+#...", "....#....", "...###...",
               "..#+++#..", ".#+++++#.", "..#####..", "...#.#..."],        # siphon globes
    "frost": ["....#....", ".#..#..#.", "..#.#.#..", "...###...", "#########",
              "...###...", "..#.#.#..", ".#..#..#.", "....#...."],         # snowflake
    "dawn": ["....#....", ".#..#..#.", "..#####..", ".#######.", "####+####",
             ".#######.", "..#####..", ".#..#..#.", "....#...."],          # sun
    "midnight": ["...###...", "..##.....", ".##......", ".##......", ".##......",
                 ".##......", "..##.....", "...###.+.", "......+++"],      # crescent + star
    "nothing": ["..#####..", ".#.....#.", ".....###.", "....##...", "....#....",
                "....#....", ".........", "....#....", "........."],       # ?
}


def icon(a, x0, y0, kind, ink, light="1"):
    for dy, row in enumerate(ICONS[kind]):
        for dx, c in enumerate(row):
            if c == "#":
                px(a, x0 + dx, y0 + dy, ink)
            elif c == "+":
                px(a, x0 + dx, y0 + dy, light)


# =============================================================================
#  STALLS — a 3x2 counter; the kit stands on the top surface (y <= 15)
# =============================================================================
#   skirt colours by stall: (dark, light, icon ink, pattern)
SKIRTS = {
    "ember": ("r", "R", "g", "stripe"), "pourover": ("0", "y", "W", "plain"),
    "press": ("n", "N", "y", "stripe"), "coldbrew": ("F", "K", "1", "wave"),
    "sandpot": ("z", "Z", "y", "diamond"), "latte": ("h", "H", "1", "scallop"),
    "mushroom": ("m", "M", "y", "plain"), "decaf": ("x", "X", "4", "plain"),
    "siphon": ("v", "V", "L", "stripe"), "frost": ("i", "I", "j", "wave"),
    "dawn": ("a", "A", "1", "rays"), "midnight": ("u", "U", "g", "stars"),
    "nothing": ("V", "K", "R", "check"),
}


def counter(a, kind):
    """The shared counter: plank top (y 14..18) and a cloth skirt (y 19..29)."""
    W = a.shape[1]
    dk, lt, ink, pat = SKIRTS[kind]
    # top surface (seen from above-front): ink rim, warm planks, a lit front edge
    inked(a, 0, 14, W - 1, 19, "o", hi="O")
    for x in (12, 27, 39):
        vline(a, x, 15, 18, "W")
    hline(a, 1, W - 2, 18, "W")
    # skirt
    inked(a, 1, 19, W - 2, 29, lt)
    hline(a, 2, W - 3, 28, dk)
    for x in range(2, W - 2):
        for y in range(20, 28):
            if pat == "stripe" and (x // 4) % 2 == 0:
                px(a, x, y, dk)
            elif pat == "wave" and (y - 20) == round(2 + 1.5 * math.sin(x / 2.5)):
                px(a, x, y, dk)
            elif pat == "diamond" and abs((x % 8) - 4) + abs((y - 20) % 8 - 4) == 3:
                px(a, x, y, dk)
            elif pat == "scallop" and y == 20 + (0 if x % 6 in (2, 3) else 1):
                px(a, x, y, dk)
            elif pat == "rays" and (x - W // 2) != 0 and abs((y - 31) * 3 // (x - W // 2 or 1)) in (1, 3):
                px(a, x, y, dk)
            elif pat == "stars" and (x * 7 + y * 13) % 23 == 0:
                px(a, x, y, "g")
            elif pat == "check" and ((x // 3) + (y // 3)) % 2 == 0:
                px(a, x, y, dk)
    # the icon plaque in the middle of the skirt
    cx = W // 2 - 5
    inked(a, cx - 1, 19, cx + 10, 29, dk)
    icon(a, cx + 1, 20, kind, ink)
    contact(a, 0, W - 1, 31)
    contact(a, 0, W - 1, 30, alpha=60)


def stall_ember():
    """The Ember roast: a copper-topped espresso machine, a bean grinder, cups."""
    a = canvas(3, 2)
    counter(a, "ember")
    # machine body
    inked(a, 4, 3, 25, 15, "S", hi="t", lo="s")
    inked(a, 3, 1, 26, 4, "P", hi="q")          # copper top rail
    for x in (8, 14, 20):                        # three cups warming on top
        rect(a, x, 0, x + 2, 1, "1")
    # group heads + portafilters
    for gx in (8, 18):
        rect(a, gx, 8, gx + 4, 9, "k")
        rect(a, gx + 1, 10, gx + 3, 10, "s")
        rect(a, gx + 5, 9, gx + 7, 9, "k")       # handle
        rect(a, gx + 1, 13, gx + 3, 15, "1")     # cup under
        vline(a, gx + 2, 11, 12, "C")            # the pour
    rect(a, 13, 5, 15, 6, "g")                   # pressure dial
    px(a, 14, 5, "r")
    # grinder
    inked(a, 30, 9, 36, 15, "s", hi="S")
    for y in range(2, 9):
        rect(a, 31 - (8 - y) // 3, y, 35 + (8 - y) // 3, y, "l")
    rect(a, 30, 2, 36, 4, "C")                   # beans in the hopper
    px(a, 32, 3, "e"); px(a, 34, 2, "e")
    # tiny cups + saucers
    for x in (39, 43):
        rect(a, x, 12, x + 2, 14, "1")
        hline(a, x - 1, x + 3, 15, "2")
    steam(a, 10, 7, 2)
    steam(a, 20, 7, 2)
    return img(a)


def stall_pourover():
    """The pour-over bar: a wooden stand with two cones over glass carafes, a
    gooseneck kettle, a tiny scale."""
    a = canvas(3, 2)
    counter(a, "pourover")
    inked(a, 3, 3, 33, 6, "W", hi="o")           # stand crossbar
    for x in (4, 31):
        rect(a, x, 6, x + 1, 15, "w")
    for cx in (11, 24):
        for i, y in enumerate(range(0, 6)):      # the white cones
            hline(a, cx - 5 + i, cx + 5 - i, y, "1" if i < 4 else "2")
        hline(a, cx - 6, cx + 6, 0, "k")
        rect(a, cx - 3, 8, cx + 3, 15, "l")      # carafe
        rect(a, cx - 2, 12, cx + 2, 14, "C")     # coffee in it
        px(a, cx - 2, 9, "L")
        hline(a, cx - 3, cx + 3, 7, "s")
        vline(a, cx, 6, 7, "C")                  # the drip
    # gooseneck kettle
    inked(a, 37, 7, 45, 15, "t", hi="T", lo="S")
    for i in range(6):
        px(a, 36 - i, 8 - i // 2, "s")           # the swan neck
    px(a, 30, 5, "s")
    rect(a, 40, 5, 42, 6, "k")                   # lid knob
    return img(a)


def stall_press():
    """The press pots: three glass cylinders with plunger rods."""
    a = canvas(3, 2)
    counter(a, "press")
    for i, x in enumerate((4, 17, 30)):
        inked(a, x, 4, x + 11, 15, "l")
        rect(a, x + 1, 8 + i, x + 10, 14, "C")    # coffee (pressed lower each time)
        rect(a, x + 1, 7 + i, x + 10, 7 + i, "e")  # the plunger mesh
        rect(a, x + 2, 5, x + 2, 13, "L")
        inked(a, x, 2, x + 11, 4, "s", hi="S")    # lid
        vline(a, x + 5, 0, 2, "S"); vline(a, x + 6, 0, 2, "S")
        rect(a, x + 4, 0, x + 7, 0, "k")          # knob
        rect(a, x + 11, 6, x + 13, 12, "k")       # handle
        rect(a, x + 12, 7, x + 12, 11, "s")
    return img(a)


def stall_coldbrew():
    """Cold brew: a tall drip tower (a globe of water, a slow coil, a flask) and
    a row of dark bottles. It takes eighteen hours. Tidwell will tell you."""
    a = canvas(3, 2)
    counter(a, "coldbrew")
    inked(a, 4, 0, 26, 2, "w", hi="W")            # tower top beam
    for x in (4, 25):
        rect(a, x, 2, x + 1, 15, "w")
    inked_ellipse(a, 15, 4, 5, 3, "L")             # the water globe
    px(a, 13, 3, "1")
    vline(a, 15, 7, 8, "K")                        # the drip
    for i in range(3):                             # the slow coil
        hline(a, 11, 19, 9 + i, "l" if i % 2 else "K")
    inked(a, 12, 12, 18, 15, "C")                  # the flask
    for x in (31, 35, 39, 43):                     # the bottles
        inked(a, x, 6, x + 3, 15, "c")
        rect(a, x + 1, 4, x + 2, 6, "k")
        px(a, x + 1, 8, "F")
        rect(a, x + 1, 10, x + 2, 11, "y")         # label
    return img(a)


def stall_sandpot():
    """The sand pot: a copper tray of hot sand, three long-handled pots buried to
    their waists, a tall brass mill. Grandmother Ilka reads the grounds."""
    a = canvas(3, 2)
    counter(a, "sandpot")
    inked(a, 2, 9, 30, 15, "D", hi="d")           # sand tray
    rect(a, 2, 13, 30, 15, "P")
    hline(a, 3, 29, 13, "q")
    for x in (5, 14, 23):
        inked(a, x, 6, x + 5, 11, "P", hi="q")    # pot belly
        line(a, x + 5, 7, x + 9, 3, "b")           # long handle
        line(a, x + 6, 7, x + 10, 3, "B")
        hline(a, x, x + 5, 6, "k")
    for dx, dy in ((8, 4), (17, 3), (26, 4)):
        steam(a, dx, dy, 1)
    # the tall brass mill
    inked(a, 35, 3, 41, 15, "B", hi="g", lo="b")
    for y in (6, 10):
        hline(a, 36, 40, y, "b")
    line(a, 38, 3, 44, 0, "k")                     # crank
    rect(a, 43, 0, 45, 1, "w")
    return img(a)


def stall_latte():
    """Latte art: cups showing hearts and leaves, a steel milk jug, a little
    chalkboard with a heart drawn on it."""
    a = canvas(3, 2)
    counter(a, "latte")
    for i, x in enumerate((3, 13, 23)):
        inked_ellipse(a, x + 4, 11, 5, 3, "E")    # cup top (foam)
        rect(a, x, 12, x + 8, 15, "1")             # cup body
        hline(a, x, x + 8, 15, "2")
        if i == 0:                                  # heart
            px(a, x + 3, 10, "e"); px(a, x + 5, 10, "e")
            hline(a, x + 3, x + 5, 11, "e"); px(a, x + 4, 12, "e")
        elif i == 1:                                # leaf (it's always a leaf)
            vline(a, x + 4, 9, 12, "e")
            for d in (1, 2):
                px(a, x + 4 - d, 10 + d // 2, "e"); px(a, x + 4 + d, 10 + d // 2, "e")
        else:                                       # a wobbly attempt at a face
            px(a, x + 3, 10, "e"); px(a, x + 5, 10, "e"); hline(a, x + 3, x + 5, 12, "e")
    # milk jug
    inked(a, 33, 6, 39, 15, "t", hi="T", lo="S")
    px(a, 32, 6, "t"); px(a, 31, 5, "t")
    rect(a, 40, 8, 41, 12, "k")
    # chalkboard
    inked(a, 41, 1, 47, 9, "s")
    px(a, 43, 4, "H"); px(a, 45, 4, "H"); hline(a, 43, 45, 5, "H"); px(a, 44, 6, "H")
    vline(a, 42, 9, 15, "w"); vline(a, 46, 9, 15, "w")
    return img(a)


def stall_mushroom():
    """Mushroom brew: an earthenware pot, a basket of brown caps, moss, a jar of
    something nobody asks about."""
    a = canvas(3, 2)
    counter(a, "mushroom")
    inked(a, 4, 5, 16, 15, "e", hi="E", lo="C")   # earthen pot
    hline(a, 3, 17, 5, "k")
    rect(a, 6, 3, 14, 4, "C")
    steam(a, 8, 2, 1); steam(a, 12, 2, 1)
    # basket of caps
    inked(a, 20, 10, 32, 15, "o", hi="O")
    for x in range(21, 32, 2):
        vline(a, x, 11, 14, "W")
    for cx, cy in ((23, 8), (27, 7), (30, 9)):
        inked_ellipse(a, cx, cy, 3, 2, "W", hi="O")
        vline(a, cx, cy + 2, cy + 3, "y")
    # moss tuft + the jar
    for x in range(34, 39):
        px(a, x, 14 - (x % 2), "M"); px(a, x, 15, "m")
    inked(a, 40, 6, 46, 15, "l")
    rect(a, 41, 9, 45, 14, "M")
    rect(a, 40, 4, 46, 6, "w")
    return img(a)


def stall_decaf():
    """Decaf: one grey pot, an empty bowl, a single wilting flower in a jar, and
    a tiny handwritten sign that just says 'please'."""
    a = canvas(3, 2)
    counter(a, "decaf")
    inked(a, 8, 6, 17, 15, "X", hi="2", lo="x")   # the one pot
    px(a, 7, 8, "X"); px(a, 6, 7, "X")
    rect(a, 11, 4, 14, 5, "x")
    inked(a, 21, 10, 31, 15, "2", hi="1", lo="3")   # an empty bowl (nobody's had any)
    rect(a, 23, 10, 29, 11, "3")
    # wilting flower
    inked(a, 36, 10, 40, 15, "l")
    vline(a, 38, 4, 10, "m")
    line(a, 38, 4, 41, 6, "m")
    px(a, 42, 7, "H"); px(a, 41, 7, "h"); px(a, 42, 8, "h")
    # the sign
    inked(a, 43, 8, 47, 13, "2")
    hline(a, 44, 46, 10, "4")
    return img(a)


def stall_siphon():
    """The Siphon Lab: two vacuum brewers — a top globe, a round bottom globe, a
    blue burner flame — plus a stray flask that bubbles for no reason."""
    a = canvas(3, 2)
    counter(a, "siphon")
    for cx in (9, 26):
        inked(a, cx - 4, 0, cx + 4, 5, "L")       # top chamber (glass)
        rect(a, cx - 3, 3, cx + 3, 4, "e")         # coffee rising into it
        px(a, cx - 3, 1, "1")
        vline(a, cx, 6, 7, "S")                    # the tube
        inked_ellipse(a, cx, 10, 5, 4, "L")        # bottom globe (glass)
        ellipse(a, cx, 11.5, 3.5, 1.5, "l")        # the water left in it
        px(a, cx - 2, 8, "1")
        rect(a, cx - 4, 6, cx - 4, 13, "S")        # the clamp stand
        px(a, cx, 14, "5"); px(a, cx - 1, 15, "6"); px(a, cx + 1, 15, "6")  # flame
    # the bubbling flask
    inked(a, 38, 9, 45, 15, "l")
    rect(a, 40, 5, 43, 9, "l"); rect(a, 40, 5, 43, 5, "k")
    rect(a, 39, 11, 44, 14, "V")
    for bx, by in ((41, 3), (43, 1), (40, 0)):
        px(a, bx, by, "V")
    return img(a)


def stall_frost():
    """The frost-brew: a pot furred with frost, a bowl of ice, a snowflake doily."""
    a = canvas(3, 2)
    counter(a, "frost")
    inked(a, 5, 4, 17, 15, "I", hi="j", lo="i")
    for x in range(6, 17, 3):
        px(a, x, 5, "1"); px(a, x + 1, 6, "1")
    rect(a, 9, 2, 13, 3, "i")
    # breath of cold, not steam
    for i in range(6):
        px(a, 20 + i, 6 - (i % 2), "I", alpha=140)
    inked_ellipse(a, 28, 13, 6, 3, "j")            # bowl of ice
    for cx in (25, 28, 31):
        rect(a, cx, 10, cx + 2, 12, "I")
        px(a, cx, 10, "1")
    # doily snowflake
    icon(a, 37, 6, "frost", "I", "1")
    return img(a)


def stall_dawn():
    """The Dawnbean: a golden pot that glows, a sunburst stand, cups that catch the
    light. It is said to taste like morning. Nobody here remembers morning."""
    a = canvas(3, 2)
    counter(a, "dawn")
    for ang in range(0, 360, 30):                   # the glow
        r0, r1 = 7, 11
        x0 = 16 + r0 * math.cos(math.radians(ang)); y0 = 8 + r0 * math.sin(math.radians(ang))
        x1 = 16 + r1 * math.cos(math.radians(ang)); y1 = 8 + r1 * math.sin(math.radians(ang))
        if y1 < 15:
            line(a, round(x0), round(y0), round(x1), round(y1), "A")
    inked(a, 11, 4, 21, 15, "A", hi="G", lo="a")
    rect(a, 14, 2, 18, 3, "a")
    px(a, 10, 7, "a"); px(a, 9, 6, "a")
    for x in (28, 34, 40):
        rect(a, x, 11, x + 3, 15, "1")
        rect(a, x + 1, 11, x + 2, 11, "A")
    return img(a)


def stall_midnight():
    """Midnight Oil: a black pot that seems to swallow the lamplight, a crescent on
    a stand, and little stars that sit on the counter like crumbs."""
    a = canvas(3, 2)
    counter(a, "midnight")
    inked(a, 6, 4, 17, 15, "u", hi="U")
    rect(a, 9, 2, 14, 3, "U")
    px(a, 5, 7, "u"); px(a, 4, 6, "u")
    # crescent on a little stand
    for y in range(0, 10):
        for x in range(22, 32):
            if (x - 27) ** 2 + (y - 5) ** 2 <= 20 and not (x - 29) ** 2 + (y - 4) ** 2 <= 14:
                px(a, x, y, "g")
    vline(a, 26, 10, 15, "b")
    hline(a, 24, 28, 15, "b")
    for sx, sy in ((36, 12), (41, 14), (44, 10), (38, 8)):
        px(a, sx, sy, "G"); px(a, sx - 1, sy, "g"); px(a, sx + 1, sy, "g")
        px(a, sx, sy - 1, "g"); px(a, sx, sy + 1, "g")
    return img(a)


def stall_nothing():
    """The Stall That Isn't There: a counter in colours that don't go together,
    drawn half-transparent, a pot with an eye on it. Only the very caffeinated
    can see it (requires flag:brew_buzzing)."""
    a = canvas(3, 2)
    counter(a, "nothing")
    inked(a, 15, 3, 31, 15, "K", hi="1", lo="F")
    for x in range(16, 31):                         # stripes that wobble
        px(a, x, 8 + round(math.sin(x) * 2), "V")
    inked_ellipse(a, 23, 9, 3, 2, "1")              # the eye
    px(a, 23, 9, "k"); px(a, 24, 9, "k")
    rect(a, 20, 1, 26, 2, "R")
    # dissolve: every third pixel becomes see-through (it isn't there, mostly)
    h, w = a.shape[:2]
    for y in range(h):
        for x in range(w):
            if a[y, x, 3] > 0 and (x * 3 + y * 5) % 7 == 0:
                a[y, x, 3] = 70
    return img(a)


# =============================================================================
#  THE GRAND URN — the fair's centrepiece (4x4). Awake = it sings (seeing stage)
# =============================================================================
def _urn(awake: bool):
    a = canvas(4, 4)
    W = 64
    # the round dais
    inked_ellipse(a, 32, 56, 30, 7, "o", hi="O")
    ellipse(a, 32, 58, 27, 4, "W")
    hline(a, 6, 58, 56, "W")
    # body: a bulbous copper urn
    for y in range(14, 52):
        t = (y - 14) / 38.0
        rx = 14 + 9 * math.sin(math.pi * min(t * 1.1, 1.0))
        ellipse_row = int(round(rx))
        rect(a, 32 - ellipse_row, y, 32 + ellipse_row, y, "k")
        rect(a, 32 - ellipse_row + 1, y, 32 + ellipse_row - 1, y, "P")
        # shading: lit left, dark right
        rect(a, 32 - ellipse_row + 2, y, 32 - ellipse_row + 4, y, "q")
        rect(a, 32 + ellipse_row - 4, y, 32 + ellipse_row - 1, y, "p")
    for y in (22, 40):                               # brass bands
        hline(a, 10, 54, y, "B"); hline(a, 10, 54, y + 1, "b")
        for x in range(8, 57):
            if a[y, x, 3] == 0 or (a[y, x, :3] == rgba(PAL["k"])[:3]).all():
                pass
    # re-ink the band ends so they sit inside the silhouette
    for y in range(14, 52):
        row = np.where(a[y, :, 3] > 0)[0]
        if len(row):
            a[y, row[0]] = rgba(PAL["k"]); a[y, row[-1]] = rgba(PAL["k"])
    # neck + lid + finial
    inked(a, 22, 9, 42, 14, "P", hi="q", lo="p")
    inked_ellipse(a, 32, 8, 12, 3, "B", hi="g")
    inked(a, 30, 1, 34, 6, "B", hi="g")
    inked_ellipse(a, 32, 1, 3, 2, "g")
    # handles
    for side in (-1, 1):
        x0 = 32 + side * 22
        for i in range(8):
            px(a, x0 + side * (2 if 2 < i < 6 else 1), 20 + i, "k")
            px(a, x0 + side * (1 if 2 < i < 6 else 0), 20 + i, "b")
    # the tap + the waiting cup
    inked(a, 29, 44, 35, 47, "B", hi="g")
    rect(a, 33, 47, 34, 49, "k")
    inked(a, 30, 50, 37, 54, "1")
    rect(a, 31, 51, 36, 51, "C")
    if awake:
        # eyes, eyebrows, a singing mouth, notes
        for ex in (24, 38):
            inked_ellipse(a, ex, 28, 4, 3, "1")
            rect(a, ex - 1, 27, ex, 29, "k")
            line(a, ex - 4, 23, ex + 3, 22 if ex < 32 else 24, "k")
        inked_ellipse(a, 31, 36, 5, 3, "c")
        ellipse(a, 31, 37, 3, 1, "R")
        for nx, ny in ((6, 10), (52, 6), (56, 18), (4, 24)):
            rect(a, nx, ny, nx + 2, ny + 1, "G")
            vline(a, nx + 2, ny - 5, ny, "G")
            px(a, nx + 3, ny - 5, "G"); px(a, nx + 4, ny - 4, "G")
    else:
        # a stamped crest: a steaming cup
        inked(a, 26, 28, 37, 36, "B", hi="g")
        rect(a, 28, 30, 35, 34, "1")
        rect(a, 36, 31, 38, 33, "k")
        steam(a, 31, 27, 1)
    steam(a, 32, 0, 1)
    contact(a, 4, 60, 63)
    return img(a)


def grand_urn():
    return _urn(False)


def grand_urn_awake():
    return _urn(True)


def urn_puddle():
    """1x1 a coffee puddle swirling into a spiral of crema — the way in."""
    a = canvas(1, 1)
    inked_ellipse(a, 8, 9, 7, 5, "C")
    for i in range(40):
        t = i / 40 * 4 * math.pi
        r = 0.3 + i * 0.13
        px(a, round(8 + r * math.cos(t)), round(9 + r * 0.7 * math.sin(t)), "E" if i % 3 else "f")
    return img(a)


# =============================================================================
#  FURNITURE
# =============================================================================
def cupping_table():
    """3x2 the cupping table: a long plank table, two rows of small bowls, the
    deep slurping spoons laid out with professional menace."""
    a = canvas(3, 2)
    W = 48
    inked(a, 0, 6, W - 1, 20, "o", hi="O", lo="W")
    for x in (2, W - 4):
        rect(a, x, 21, x + 2, 29, "w")
    rect(a, 18, 21, 29, 23, "W")
    for row, y in enumerate((9, 15)):
        for i in range(6):
            x = 3 + i * 7 + (row * 3)
            if x + 5 >= W:
                continue
            inked_ellipse(a, x + 2, y, 3, 2, "1")
            ellipse(a, x + 2, y, 1.6, 0.9, "C")
    for x in (6, 20, 34):
        line(a, x, 2, x + 5, 5, "t")
        inked_ellipse(a, x, 2, 2, 1.5, "T")
    contact(a, 0, W - 1, 31)
    return img(a)


def roaster():
    """3x3 the big drum roaster: a black drum with a brass face, a hopper on
    top, a chimney pipe, and the round cooling tray with beans going round."""
    a = canvas(3, 3)
    W, H = 48, 48
    inked(a, 4, 16, 34, 40, "s", hi="S", lo="k")   # body
    inked_ellipse(a, 19, 27, 10, 9, "B", hi="g")   # brass drum face
    ellipse(a, 19, 27, 6, 5, "c")
    rect(a, 16, 26, 22, 28, "C")
    px(a, 18, 24, "7"); px(a, 21, 25, "8")         # the glow behind the window
    for y in range(4, 16):                          # hopper
        hw = 3 + (15 - y) // 2
        rect(a, 19 - hw, y, 19 + hw, y, "k")
        rect(a, 19 - hw + 1, y, 19 + hw - 1, y, "t" if y < 8 else "S")
    rect(a, 14, 4, 24, 6, "C")
    inked(a, 30, 0, 34, 16, "s", hi="S")            # chimney
    for i in range(3):
        px(a, 32 + i % 2, 0 - i, "1", alpha=120)
    for x in (6, 30):                                # legs
        rect(a, x, 40, x + 2, 45, "k")
    # cooling tray (front right)
    inked_ellipse(a, 40, 38, 7, 4, "t", hi="T")
    ellipse(a, 40, 38, 5, 2.5, "e")
    for bx, by in ((37, 38), (40, 37), (43, 38), (39, 39), (42, 39)):
        px(a, bx, by, "C")
    rect(a, 38, 42, 42, 45, "k")
    steam(a, 40, 34, 1)
    contact(a, 2, 47, 47)
    return img(a)


def stage():
    """4x2 the Championship stage: a low plank platform, a red skirt, a gold cup
    emblem, two little steps."""
    a = canvas(4, 2)
    W = 64
    inked(a, 0, 4, W - 1, 13, "o", hi="O", lo="W")
    for x in range(8, W, 12):
        vline(a, x, 5, 12, "W")
    inked(a, 1, 13, W - 2, 28, "R")
    for x in range(2, W - 2):
        if (x // 4) % 2 == 0:
            vline(a, x, 14, 27, "r")
    inked(a, 26, 14, 37, 27, "r")
    inked(a, 28, 16, 35, 22, "B", hi="g")            # the gold cup emblem
    rect(a, 31, 23, 32, 24, "B"); rect(a, 29, 25, 34, 25, "B")
    contact(a, 0, W - 1, 31)
    return img(a)


def trophy():
    """1x2 the Golden Cup on its plinth — a coffee cup, but gold, but enormous."""
    a = canvas(1, 2)
    inked(a, 3, 22, 12, 30, "w", hi="W")
    inked(a, 4, 6, 11, 15, "B", hi="g", lo="b")
    rect(a, 11, 8, 13, 12, "k"); rect(a, 12, 9, 12, 11, "B")
    rect(a, 5, 6, 10, 7, "C")
    rect(a, 6, 16, 9, 19, "B"); hline(a, 4, 11, 20, "b"); hline(a, 4, 11, 21, "B")
    px(a, 5, 8, "G")
    steam(a, 7, 5, 1)
    contact(a, 2, 13, 31)
    return img(a)


def bean_sacks():
    """2x1 two burlap sacks, one slumped, beans spilling."""
    a = canvas(2, 1)
    inked(a, 1, 3, 14, 14, "O", hi="D", lo="o")
    rect(a, 4, 3, 11, 4, "o")
    inked(a, 15, 5, 30, 14, "D", hi="f", lo="o")
    for x, y in ((5, 8), (9, 10), (20, 9), (25, 8)):
        rect(a, x, y, x + 2, y, "W")               # stamped marks
    for x, y in ((14, 15), (17, 14), (19, 15), (31, 15)):
        px(a, x, y, "C")
    contact(a, 0, 31, 15)
    return img(a)


def aboard():
    """1x1 an A-frame chalkboard: TODAY: EVERYTHING (as squiggles)."""
    a = canvas(1, 1)
    line(a, 3, 15, 6, 1, "w"); line(a, 12, 15, 9, 1, "w")
    inked(a, 3, 2, 12, 12, "s")
    for y, (x0, x1) in ((4, (5, 10)), (6, (5, 8)), (8, (5, 11)), (10, (6, 9))):
        hline(a, x0, x1, y, "y" if y != 8 else "H")
    return img(a)


def cup_tower():
    """1x2 a tower of stacked paper cups taller than is sensible."""
    a = canvas(1, 2)
    for i, y in enumerate(range(4, 30, 3)):
        inked(a, 4, y, 11, y + 3, "1" if i % 2 else "y")
    inked(a, 3, 29, 12, 31, "2")
    return img(a)


def cot():
    """1x2 a canvas camp-cot in the Quiet Tent, a folded blanket at the foot."""
    a = canvas(1, 2)
    inked(a, 1, 2, 14, 28, "0", hi="y")
    inked(a, 3, 3, 12, 8, "1")                       # pillow
    inked(a, 2, 20, 13, 27, "N", hi="N")
    hline(a, 3, 12, 23, "n")
    for x in (1, 13):
        rect(a, x, 29, x + 1, 31, "k")
    return img(a)


def water_table():
    """2x1 the water table: a jug, a stack of cups, nobody queuing at all."""
    a = canvas(2, 1)
    inked(a, 0, 6, 31, 11, "o", hi="O")
    for x in (2, 28):
        rect(a, x, 12, x + 1, 15, "w")
    inked(a, 4, 0, 11, 8, "l")
    rect(a, 5, 3, 10, 7, "L")
    rect(a, 12, 2, 13, 5, "k")
    for i in range(3):
        rect(a, 18 + i * 4, 2, 20 + i * 4, 6, "1")
    return img(a)


def tent_pole():
    """1x2 a striped marquee pole with a brass cap and a guy-rope fan above."""
    a = canvas(1, 2)
    for y in range(2, 30):
        rect(a, 6, y, 9, y, "R" if (y // 3) % 2 else "y")
    vline(a, 5, 2, 29, "k"); vline(a, 10, 2, 29, "k")
    inked(a, 5, 0, 10, 2, "B", hi="g")
    inked(a, 4, 28, 11, 31, "w", hi="W")
    line(a, 7, 1, 0, 4, "0"); line(a, 8, 1, 15, 4, "0")
    return img(a)


def rope_post():
    """1x1 a brass queue post, the red rope sagging off to the east."""
    a = canvas(1, 1)
    inked(a, 5, 2, 8, 13, "B", hi="g")
    inked_ellipse(a, 6.5, 2, 2, 1.5, "g")
    inked(a, 3, 13, 10, 15, "b")
    for x in range(8, 16):
        px(a, x, 5 + round(math.sin((x - 8) / 8 * math.pi) * 2), "R")
        px(a, x, 6 + round(math.sin((x - 8) / 8 * math.pi) * 2), "r")
    return img(a)


# ---- wall-hung (sit on the FACE row) ----------------------------------------------
def bunting():
    """3x1 a sagging string of triangular pennants in festival colours."""
    a = canvas(3, 1)
    cols = ["R", "A", "N", "M", "H", "V"]
    for x in range(48):
        px(a, x, 2 + round(math.sin(x / 47 * math.pi) * 3), "0")
    for i in range(7):
        x0 = 1 + i * 7
        y0 = 3 + round(math.sin((x0 + 2) / 47 * math.pi) * 3)
        c = cols[i % len(cols)]
        for r in range(7):
            hline(a, x0 + r // 2, x0 + 5 - r // 2, y0 + r, c)
        px(a, x0 + 2, y0 + 6, "k")
    return img(a)


def _banner(kind: str):
    """3x1 a cloth banner in the stall's colour, its icon in the middle,
    hung from a brass rod (sits on the wall FACE above that stall's keeper)."""
    a = canvas(3, 1)
    dk, lt, ink, _ = SKIRTS[kind]
    hline(a, 0, 47, 1, "b"); hline(a, 0, 47, 2, "B")
    inked(a, 3, 2, 44, 13, lt)
    for x in range(4, 44, 4):                       # a zig-zag hem
        px(a, x, 13, dk); px(a, x + 1, 12, dk)
    inked(a, 18, 2, 29, 13, dk)
    icon(a, 19, 3, kind, ink)
    return img(a)


# ---- the exterior -------------------------------------------------------------------
def marquee():
    """7x5 THE WAKEFUL FAIR: a great red-and-cream striped marquee with three
    peaks (flags on the poles), a scalloped gold-trimmed valance, bunting, a
    hanging cup sign over the door, and the door itself on col 3 (the flaps tied
    back, warm light and the shapes of a crowd inside)."""
    a = canvas(7, 5)
    W, H = 112, 80
    # walls (y 36..77): vertical stripes, shaded towards the bottom
    for x in range(2, W - 2):
        stripe = "R" if (x // 7) % 2 == 0 else "y"
        for y in range(36, 77):
            c = stripe
            if y > 70 and stripe == "y":
                c = "0"
            if y > 70 and stripe == "R":
                c = "r"
            px(a, x, y, c)
    vline(a, 1, 36, 77, "k"); vline(a, W - 2, 36, 77, "k")
    hline(a, 1, W - 2, 77, "k")
    # roof: three peaks — a tent outline drawn as stripes converging to each apex
    peaks = [(22, 10, 24), (56, 2, 34), (90, 10, 24)]   # (apex x, apex y, half-width)
    for ax, ay, hw in peaks:
        for y in range(ay, 37):
            t = (y - ay) / (36 - ay)
            half = int(round(hw * t)) + 1
            for x in range(ax - half, ax + half + 1):
                if 0 <= x < W:
                    # stripes fan out from the apex
                    sx = (x - ax) / max(t, 0.05)
                    c = "R" if int((sx + 200) // 7) % 2 == 0 else "y"
                    if t > 0.85:
                        c = "r" if c == "R" else "0"
                    px(a, x, y, c)
            px(a, ax - half - 1, y, "k"); px(a, ax + half + 1, y, "k")
        # pole + flag
        vline(a, ax, ay - 8, ay, "k")
        for r in range(5):
            hline(a, ax + 1, ax + 6 - r, ay - 8 + r, "A" if ax == 56 else "N")
    # the valance: scallops along the eave
    for x in range(0, W):
        sc = (x // 8) % 2
        depth = 4 - abs((x % 8) - 4) // 1
        for y in range(36, 36 + max(depth, 1) + 2):
            px(a, x, y, "R" if sc == 0 else "y")
        px(a, x, 36 + max(depth, 1) + 2, "b")
    hline(a, 0, W - 1, 35, "B"); hline(a, 0, W - 1, 34, "k")
    # bunting across the front
    cols = ["A", "N", "M", "H", "V", "R"]
    for i in range(14):
        x0 = 2 + i * 8
        y0 = 46 + round(math.sin(x0 / W * math.pi) * 3)
        for r in range(5):
            hline(a, x0 + r // 2, x0 + 4 - r // 2, y0 + r, cols[i % 6])
    # the door (col 3 = x 48..63): tied-back flaps, warm interior, a crowd
    inked(a, 47, 54, 64, 79, "c")
    rect(a, 49, 58, 62, 79, "e")
    rect(a, 50, 62, 61, 79, "E")
    for cx, h in ((52, 70), (56, 68), (60, 71)):        # heads in the crowd
        inked_ellipse(a, cx, h, 2, 2, "C")
        rect(a, cx - 2, h + 2, cx + 2, 79, "C")
    for side in (46, 63):                                # the flaps, tied back
        for y in range(52, 79):
            px(a, side, y, "y"); px(a, side + (1 if side == 63 else -1), y, "R")
        rect(a, side - 1, 64, side + 1, 65, "B")
    # the hanging cup sign over the door
    vline(a, 52, 38, 41, "k"); vline(a, 59, 38, 41, "k")
    inked(a, 49, 41, 62, 52, "w", hi="W")
    rect(a, 52, 44, 58, 49, "1")
    rect(a, 59, 45, 60, 48, "k")
    steam(a, 55, 43, 1)
    # guy ropes and pegs at the sides
    line(a, 1, 40, 0, 78, "0"); line(a, W - 2, 40, W - 1, 78, "0")
    # lanterns on the corners
    for lx in (8, W - 10):
        inked(a, lx, 50, lx + 3, 55, "A", hi="G")
    contact(a, 0, W - 1, 79)
    return img(a)


# =============================================================================
#  THE DREAM — the bottom of the cup
# =============================================================================
def sugar_cube():
    """1x1 a sugar cube the size of a trunk; sparkles. It is very firm."""
    a = canvas(1, 1)
    inked(a, 1, 3, 14, 14, "1", lo="3")
    rect(a, 2, 4, 13, 6, "2")                         # the lit top face
    rect(a, 12, 4, 13, 13, "2")
    for x, y in ((4, 9), (8, 11), (10, 8), (5, 12)):
        px(a, x, y, "3")
    px(a, 3, 4, "G"); px(a, 12, 2, "G")
    contact(a, 0, 15, 15)
    return img(a)


def bean():
    """1x1 a coffee bean the size of a boulder."""
    a = canvas(1, 1)
    inked_ellipse(a, 8, 8, 6.5, 5.5, "C", hi="e")
    line(a, 5, 4, 11, 12, "c")
    line(a, 6, 4, 12, 12, "k")
    contact(a, 1, 14, 15)
    return img(a)


def spoon():
    """3x1 a giant silver teaspoon lying in the foam."""
    a = canvas(3, 1)
    inked_ellipse(a, 9, 8, 8, 5, "t", hi="T")
    ellipse(a, 10, 9, 5, 2.5, "S")
    inked(a, 16, 6, 46, 10, "t", hi="T", lo="S")
    rect(a, 40, 6, 46, 10, "B")
    contact(a, 0, 47, 15)
    return img(a)


def teacup():
    """2x2 a teacup floating on its side, larger than it should be, smiling."""
    a = canvas(2, 2)
    inked_ellipse(a, 15, 18, 13, 11, "1", hi="1")
    ellipse(a, 15, 20, 10, 7, "2")
    inked_ellipse(a, 13, 9, 9, 4, "C")
    ellipse(a, 12, 9, 6, 2, "e")
    rect(a, 27, 14, 30, 22, "k"); rect(a, 28, 15, 29, 21, "1")
    for x in (10, 18):
        px(a, x, 18, "k"); px(a, x, 19, "k")
    line(a, 11, 23, 17, 23, "k")
    hline(a, 3, 27, 27, "H")
    contact(a, 2, 29, 31)
    return img(a)


def bottomless():
    """3x3 the Bottomless Cup: a vast dark cup brimming, a whirl in the coffee,
    a ring of foam, steam like a crown. Something hums inside it."""
    a = canvas(3, 3)
    inked(a, 4, 16, 43, 43, "1", lo="3")
    rect(a, 5, 38, 42, 42, "2")
    for x in range(5, 43):
        px(a, x, 44 - (1 if 8 < x < 40 else 0), "2")
    inked_ellipse(a, 24, 16, 21, 7, "f")
    ellipse(a, 24, 16, 18, 5, "C")
    for i in range(70):
        t = i / 70 * 5 * math.pi
        r = 0.5 + i * 0.25
        px(a, round(24 + r * math.cos(t)), round(16 + r * 0.28 * math.sin(t)), "E" if i % 4 else "f")
    rect(a, 43, 22, 47, 34, "k"); rect(a, 44, 23, 46, 33, "1"); rect(a, 44, 26, 45, 30, "k")
    hline(a, 8, 40, 30, "R"); hline(a, 8, 40, 31, "r")
    for sx in (12, 24, 36):
        steam(a, sx, 9, 3)
    contact(a, 2, 47, 47)
    return img(a)


def plaque():
    """1x1 a small brass plaque on the Quiet Tent's wall, a tin cup engraved on it
    (the cup record — whose, the medic will tell you)."""
    a = canvas(1, 1)
    inked(a, 2, 3, 13, 12, "B", hi="g", lo="b")
    rect(a, 5, 5, 9, 9, "t")
    rect(a, 10, 6, 11, 8, "k")
    hline(a, 5, 9, 5, "T")
    hline(a, 4, 11, 11, "b")
    return img(a)


def dream_door():
    """1x2 a door standing on its own in the foam (its frame, ajar, warm light
    through the gap) — the way back to the fair. It looks a little embarrassed."""
    a = canvas(1, 2)
    inked(a, 1, 1, 14, 31, "W", hi="o")
    inked(a, 3, 3, 12, 31, "C")
    rect(a, 4, 4, 8, 31, "8")                         # warm light through the gap
    rect(a, 4, 4, 5, 31, "Q")
    inked(a, 8, 3, 13, 31, "w", hi="W")               # the door leaf, ajar
    px(a, 9, 18, "g")
    return img(a)


STALL_KINDS = ["ember", "pourover", "press", "coldbrew", "sandpot", "latte", "mushroom",
               "decaf", "siphon", "frost", "dawn", "midnight", "nothing"]
BANNER_KINDS = ["pourover", "sandpot", "coldbrew", "siphon", "midnight", "frost", "dawn",
                "mushroom", "latte", "ember", "press", "decaf"]

PIECES = {f"stall_{k}": globals()[f"stall_{k}"] for k in STALL_KINDS}
PIECES.update({f"banner_{k}": (lambda k=k: _banner(k)) for k in BANNER_KINDS})
PIECES.update({
    "grand_urn": grand_urn, "grand_urn_awake": grand_urn_awake, "urn_puddle": urn_puddle,
    "cupping_table": cupping_table, "roaster": roaster, "stage": stage, "trophy": trophy,
    "bean_sacks": bean_sacks, "aboard": aboard, "cup_tower": cup_tower, "cot": cot,
    "water_table": water_table, "tent_pole": tent_pole, "rope_post": rope_post,
    "bunting": bunting, "marquee": marquee,
    "sugar_cube": sugar_cube, "bean": bean, "spoon": spoon, "teacup": teacup,
    "bottomless": bottomless, "dream_door": dream_door, "plaque": plaque,
})


def preview(out: Path) -> None:
    """Every piece on a warm floor, 4x — for eyeballing."""
    ims = [(k, PIECES[k]()) for k in PIECES]
    pad, colw = 4, 0
    rows, row, x, y, rh = [], [], 0, 0, 0
    W = 600
    pos = []
    for k, im in ims:
        if x + im.width + pad > W:
            x, y, rh = 0, y + rh + pad, 0
        pos.append((x, y, im))
        x += im.width + pad
        rh = max(rh, im.height)
    H = y + rh
    sheet = Image.new("RGBA", (W, H), (150, 110, 70, 255))
    for x, y, im in pos:
        sheet.alpha_composite(im, (x, y))
    sheet.resize((W * 3, H * 3), Image.NEAREST).save(out)


def main() -> None:
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    if "--preview" in sys.argv:
        preview(Path(sys.argv[sys.argv.index("--preview") + 1]))
        return
    OBJDIR.mkdir(parents=True, exist_ok=True)
    for stem, fn in PIECES.items():
        if only is not None and stem not in only:
            continue
        im = fn()
        assert im.width % 16 == 0 and im.height % 16 == 0, stem
        im.save(OBJDIR / f"{stem}.png")
        print(f"  drew brewfair_{stem}  ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
