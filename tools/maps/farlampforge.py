#!/usr/bin/env python3
"""
farlampforge — the DRAWN kit of the Farlamp Isles (walkthrough/10, Part I).

Small sea and island props for the isles' surface maps (build_farlamp_isles.py),
Driftholm (build_driftholm.py) and the mainland hooks on Lightkeeper's Point and
the Wick-Run Foot. Kept in its OWN master folder, like paulforge/gymforge, so no
other forge's full re-run ever touches it:

    assets/tilesets/farlamp/objects/<stem>.png   ->  packed as `farlamp_<stem>`

The Driftholm BUILDINGS (inn, chandlery, elder's house, boathouse, two cottages)
(+ the Gullwrack keeper's hut) are image-gen masters in the same folder (generated once with gpt-image-2.5's
native alpha and snapped to a tile multiple) — this script never rewrites them:
it only draws the stems listed in PIECES.

Projection matches the overworld objects: straight-on front elevation, roof/top
seen slightly from above, 1px ink outline, lit top-left, a hard contact shadow.

  buoy_lit / buoy_dark   1x2  the Fogwall's lantern-buoys (lane shown with the fog-glass)
  skerry_light           3x3  the far lamp on its skerry (the blink is an animated
                              tile drawn by build_farlamp_set.py over its lamp-room)
  fogbank_a / fogbank_b  4x2 / 3x2  translucent fog banks (hidden after the isles' dawn)
  hull                   3x2  Ione's lamp-boat, half-planked on trestles
  slip                   2x3  the launch slip's planked ramp (walk-on)
  kelp_rack              2x2  a kelp-drying frame hung with dark ribbons
  well_shut / well_open  2x2  Driftholm's well-stair: lid chained / lid off, steps down
  waystone               1x2  Driftholm's lamp-stone (the TRAVEL waystone)
  looking_glass          1x2  the Point's brass looking-glass on its tripod
  ruin_wall              3x2  a broken wall of the old keepers' quarter (Kelpcrown)
  ruin_pillar            1x2  a lone pillar stub with a lamp-bracket

Run:  python3 tools/maps/farlampforge.py [--only a,b]
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "farlamp" / "objects"

PAL = {
    "k": "#0e1220",  # ink
    "K": "#1c2233",  # deep shadow
    "s": "#3a4458",  # slate dark
    "S": "#59657c",  # slate
    "t": "#8a95aa",  # slate light
    "T": "#c4ccd8",  # stone highlight
    "w": "#d9dde2",  # whitewash
    "W": "#f1f2ee",  # whitewash lit
    "g": "#a7aeb8",  # whitewash shade
    "r": "#8c2b2b",  # buoy red dark
    "R": "#c84a3c",  # buoy red
    "e": "#e8735e",  # buoy red light
    "a": "#ffb84a",  # lamp amber
    "A": "#ffe08a",  # lamp core
    "o": "#c47a22",  # lamp amber dark
    "b": "#3b2618",  # wood dark
    "B": "#6a4528",  # wood
    "n": "#9a6a3c",  # wood light
    "N": "#c8925a",  # wood glint
    "i": "#2b2e3c",  # iron
    "I": "#4a4f63",  # iron mid
    "j": "#7d8399",  # iron light
    "c": "#b8892f",  # brass dark
    "C": "#e3b84c",  # brass
    "y": "#fff0b0",  # brass glint
    "v": "#1f3a2c",  # kelp dark
    "V": "#2f5a3e",  # kelp
    "x": "#4f8a5a",  # kelp light
    "m": "#3d6b4a",  # moss
    "M": "#5f9a5c",  # moss light
    "u": "#24304a",  # glass dark (unlit)
    "U": "#4a5d80",  # glass sheen (unlit)
    "q": "#0a0c14",  # shaft black
    "h": "#4d5a3a",  # turf dark
    "H": "#6f8048",  # turf
    "p": "#e88aa8",  # sea-pink flowers
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
    h, w = a.shape[:2]
    x0, x1 = max(0, x0), min(w - 1, x1)
    y0, y1 = max(0, y0), min(h - 1, y1)
    if x0 <= x1 and y0 <= y1:
        a[y0:y1 + 1, x0:x1 + 1] = rgba(PAL[ch])


def px(a, x, y, ch):
    if 0 <= y < a.shape[0] and 0 <= x < a.shape[1]:
        a[y, x] = rgba(PAL[ch])


def inked(a, x0, y0, x1, y1, fill, *, hi=None, lo=None):
    rect(a, x0, y0, x1, y1, "k")
    if x1 - x0 >= 2 and y1 - y0 >= 2:
        rect(a, x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)
        if hi:
            rect(a, x0 + 1, y0 + 1, x1 - 1, y0 + 1, hi)
        if lo:
            rect(a, x0 + 1, y1 - 1, x1 - 1, y1 - 1, lo)


def disc(a, cx, cy, r, ch):
    h, w = a.shape[:2]
    for y in range(max(0, int(cy - r - 1)), min(h, int(cy + r + 2))):
        for x in range(max(0, int(cx - r - 1)), min(w, int(cx + r + 2))):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                a[y, x] = rgba(PAL[ch])


def ellipse(a, cx, cy, rx, ry, ch):
    h, w = a.shape[:2]
    for y in range(max(0, int(cy - ry - 1)), min(h, int(cy + ry + 2))):
        for x in range(max(0, int(cx - rx - 1)), min(w, int(cx + rx + 2))):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                a[y, x] = rgba(PAL[ch])


def contact(a, x0, x1, y, al=140):
    for x in range(max(0, x0), min(a.shape[1], x1 + 1)):
        if a[y, x, 3] == 0:
            a[y, x] = [12, 16, 28, al]


def ripple(a, x0, x1, y):
    """A pale waterline ripple under something afloat."""
    for x in range(x0, x1 + 1):
        if 0 <= x < a.shape[1] and a[y, x, 3] == 0 and (x % 3) != 2:
            a[y, x] = [150, 190, 220, 200]


def img(a) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# =============================================================================
#  SEA PROPS
# =============================================================================
def _buoy(lit: bool):
    a = canvas(1, 2)
    # the float: a fat red/white drum riding the swell, rows 20-29
    ellipse(a, 7.5, 25, 6.5, 5, "k")
    ellipse(a, 7.5, 25, 5.5, 4, "R")
    rect(a, 2, 23, 13, 24, "w")          # the white band
    rect(a, 3, 23, 6, 23, "W")
    ellipse(a, 5, 22, 2, 1, "e")         # lit top-left of the drum
    rect(a, 3, 27, 12, 28, "r")          # the drum's shadowed belly
    ripple(a, 0, 15, 30)
    ripple(a, 2, 13, 31)
    # the mast + cage
    rect(a, 7, 9, 8, 20, "k")
    px(a, 7, 10, "j"); px(a, 7, 14, "j")
    inked(a, 4, 2, 11, 10, "I")
    if lit:
        rect(a, 5, 3, 10, 9, "a")
        rect(a, 6, 4, 9, 8, "A")
        px(a, 6, 4, "W")
    else:
        rect(a, 5, 3, 10, 9, "u")
        rect(a, 5, 3, 6, 5, "U")
    rect(a, 4, 6, 11, 6, "k")            # the cage bar across the glass
    rect(a, 7, 2, 8, 9, "k")
    inked(a, 5, 0, 10, 2, "S", hi="t")   # cap
    return img(a)


def buoy_lit():
    return _buoy(True)


def buoy_dark():
    return _buoy(False)


def skerry_light():
    """3x3: a stub lighthouse on a wet black skerry. The lamp-room glass sits
    wholly inside tile (1, 0) (x 19-28, y 4-10) so ONE animated tile from
    build_farlamp_set.py (`blink_lamp`, painted in the `above` layer over that
    tile) makes the far lamp blink."""
    a = canvas(3, 3)
    rng = random.Random(7)
    for x in range(0, 48):
        top = 35 + int(2.5 * abs((x - 24) / 24.0) ** 1.4 * 3) + rng.choice((0, 0, 1))
        rect(a, x, top, x, 44, "K")
        px(a, x, top, "s")
    rect(a, 4, 38, 43, 40, "s")
    for x in range(6, 44, 5):
        px(a, x, 37, "t")
    for (x, y) in ((8, 41), (9, 41), (30, 42), (38, 40)):
        px(a, x, y, "m")
    ripple(a, 0, 47, 45)
    ripple(a, 2, 45, 46)
    cx = 24
    for y in range(12, 39):
        half = 5 + (y - 12) // 6
        x0, x1 = cx - half, cx - 1 + half
        rect(a, x0, y, x1, y, "k")
        rect(a, x0 + 1, y, x1 - 1, y, "w")
        rect(a, x0 + 1, y, x0 + 2, y, "W")
        rect(a, x1 - 2, y, x1 - 1, y, "g")
    for y in (20, 21, 30, 31):
        half = 5 + (y - 12) // 6
        rect(a, cx + 1 - half, y, cx - 2 + half, y, "R")
    rect(a, cx - 2, 32, cx + 1, 38, "b")
    rect(a, cx - 1, 33, cx, 37, "B")
    rect(a, 16, 11, 31, 12, "k")
    rect(a, 17, 11, 30, 11, "j")
    inked(a, 19, 3, 28, 11, "I")
    rect(a, 20, 4, 27, 10, "u")
    rect(a, 20, 4, 21, 6, "U")
    rect(a, 23, 3, 24, 11, "k")
    stamp(a, [
        "....kkkk....",
        "..kkSSSSkk..",
        ".kSSttSSSSk.",
        "kkkkkkkkkkkk",
    ], 18, 0)
    return img(a)


def _fog(tw: int, th: int, seed: int):
    """A translucent fog bank: stacked soft lobes, alpha in hard steps (no
    smooth gradient, so it never picks up a chroma halo) and a dithered rim."""
    a = canvas(tw, th)
    W, H = tw * 16, th * 16
    rng = random.Random(seed)
    lobes = [(rng.uniform(6, W - 6), rng.uniform(H * 0.35, H * 0.7),
              rng.uniform(W * 0.16, W * 0.3), rng.uniform(H * 0.25, H * 0.42))
             for _ in range(5 + tw)]
    dens = np.zeros((H, W))
    for (cx, cy, rx, ry) in lobes:
        for y in range(H):
            for x in range(W):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d < 1.0:
                    dens[y, x] = max(dens[y, x], 1.0 - d)
    for y in range(H):
        for x in range(W):
            v = dens[y, x]
            if v <= 0.02:
                continue
            if v < 0.18 and (x + y) % 2:
                continue                       # dithered rim
            al = 70 if v < 0.18 else 110 if v < 0.45 else 150
            lit = 222 if y < H * 0.45 else 198
            a[y, x] = [lit - 30, lit - 14, lit, al]
    return img(a)


def fogbank_a():
    return _fog(4, 2, 11)


def fogbank_b():
    return _fog(3, 2, 23)


# =============================================================================
#  THE POINT + THE BOATYARD
# =============================================================================
def hull():
    """3x2: the Farlamp lamp-boat on trestles, half re-planked — new pale
    strakes over the old tarred ones, a bare prow-post waiting for its lamp."""
    a = canvas(3, 2)
    # trestles
    for x in (8, 38):
        rect(a, x, 22, x + 1, 30, "b"); rect(a, x + 1, 22, x + 1, 30, "B")
        rect(a, x - 3, 30, x + 4, 30, "b")
    # the hull in side profile (bow to the east)
    for x in range(2, 46):
        t = (x - 2) / 43
        keel = 22 - int(3 * (1 - (2 * t - 1) ** 2))
        top = 9 if x < 40 else 9 + (x - 40)
        rect(a, x, top, x, keel, "k")
        if x < 3 or x > 44:
            continue
        for y in range(top + 1, keel):
            band = (y - top) // 3
            new = x > 18 and band < 3
            ch = ("N" if band == 0 else "n") if new else ("b" if band % 2 else "B")
            a[y, x] = rgba(PAL[ch])
    rect(a, 3, 10, 44, 10, "n")             # the gunwale
    rect(a, 3, 9, 40, 9, "k")
    # the prow-post + an empty lamp-hook
    rect(a, 43, 2, 44, 10, "k"); px(a, 43, 3, "n")
    rect(a, 41, 2, 44, 2, "k"); rect(a, 41, 3, 41, 5, "i")
    inked(a, 39, 5, 43, 9, "u")
    # a pot of tar + a plank leaning on the far trestle
    inked(a, 18, 24, 23, 30, "i", hi="I")
    rect(a, 19, 24, 22, 24, "K")
    contact(a, 2, 46, 31)
    return img(a)


def slip():
    """2x3: a planked launch slip running down the beach into the sea —
    side rails, cross-planks lighter at the top (dry), wet and dark at the foot."""
    a = canvas(2, 3)
    H = 48
    for y in range(H):
        wet = y > 30
        rect(a, 2, y, 29, y, "b")
        if y % 4 != 3:
            rect(a, 3, y, 28, y, ("B" if wet else "n"))
            if not wet and y % 4 == 0:
                rect(a, 3, y, 28, y, "N")
        else:
            rect(a, 3, y, 28, y, "b")
    # the rails (iron, worn bright on top)
    rect(a, 7, 0, 8, H - 1, "i"); rect(a, 7, 0, 7, H - 1, "j")
    rect(a, 23, 0, 24, H - 1, "i"); rect(a, 23, 0, 23, H - 1, "j")
    rect(a, 0, 0, 1, H - 1, "k"); rect(a, 30, 0, 31, H - 1, "k")
    # a bollard + a coiled rope at the head
    inked(a, 0, 1, 4, 6, "I", hi="j")
    for (x, y) in ((27, 2), (28, 2), (29, 3), (26, 3), (27, 4), (28, 4)):
        px(a, x, y, "N")
    ripple(a, 0, 31, 40)
    ripple(a, 0, 31, 46)
    return img(a)


def kelp_rack():
    """2x2: a driftwood A-frame with long dark kelp ribbons drying on its bar."""
    a = canvas(2, 2)
    for (x0, x1) in ((3, 8), (28, 23)):
        for y in range(4, 31):
            x = x0 + (x1 - x0) * (y - 4) // 26
            rect(a, x, y, x + 1, y, "b"); px(a, x, y, "B")
    rect(a, 1, 4, 30, 5, "k"); rect(a, 2, 4, 29, 4, "n")
    rng = random.Random(5)
    for x in range(4, 28, 3):
        ln = rng.randint(12, 21)
        for y in range(6, 6 + ln):
            sway = int(1.3 * np.sin((y + x) / 3.0))
            px(a, x + sway, y, "V"); px(a, x + 1 + sway, y, "v")
            if y % 5 == 0:
                px(a, x + sway, y, "x")
    contact(a, 2, 29, 31)
    return img(a)


def _well(open_: bool):
    a = canvas(2, 2)
    # the round stone collar (front elevation, top seen from above)
    ellipse(a, 15.5, 13, 14, 9, "k")
    ellipse(a, 15.5, 13, 13, 8, "S")
    ellipse(a, 15.5, 12, 11, 6, "t")
    ellipse(a, 15.5, 13, 9, 5, "k")
    if open_:
        ellipse(a, 15.5, 13, 8, 4, "q")
        for i, y in enumerate((11, 13, 15)):         # steps spiralling down
            rect(a, 9 + i * 2, y, 14 + i * 2, y, "s")
            rect(a, 9 + i * 2, y, 14 + i * 2, y, "S") if i == 0 else None
        px(a, 21, 11, "a"); px(a, 21, 12, "o")       # a lamp hung inside
    else:
        ellipse(a, 15.5, 13, 8, 4, "B")
        for x in range(9, 23, 3):
            rect(a, x, 9, x, 17, "b")
        rect(a, 7, 12, 24, 13, "i"); rect(a, 7, 12, 24, 12, "j")   # the iron band
        inked(a, 14, 13, 17, 17, "c", hi="C")                       # the lock
    # the collar's front face (stone courses)
    for y in range(17, 29):
        half = 14 - max(0, (y - 24))
        rect(a, 16 - half, y, 15 + half, y, "k")
        rect(a, 17 - half, y, 14 + half, y, "S" if (y // 3) % 2 else "s")
    for y in range(18, 28, 3):
        for x in range(4, 28, 6):
            px(a, x + (y % 2) * 3, y, "k")
    rect(a, 4, 18, 27, 18, "t")
    # the windlass posts
    rect(a, 2, 2, 3, 20, "k"); rect(a, 28, 2, 29, 20, "k")
    px(a, 2, 3, "n"); px(a, 28, 3, "n")
    rect(a, 2, 2, 29, 3, "b"); rect(a, 3, 2, 28, 2, "n")
    contact(a, 2, 29, 29)
    return img(a)


def well_shut():
    return _well(False)


def well_open():
    return _well(True)


def waystone():
    """1x2: a standing lamp-stone, a lantern niche glowing in its face."""
    a = canvas(1, 2)
    stamp(a, [
        "....kkkkkk......",
        "...kTTttSSk.....",
        "..kTtttSSSSk....",
        "..ktttSSSSSk....",
    ], 1, 1)
    inked(a, 3, 4, 12, 28, "S", hi="t")
    rect(a, 3, 5, 4, 27, "t")
    rect(a, 11, 5, 11, 27, "s")
    inked(a, 5, 9, 10, 16, "k")
    rect(a, 6, 10, 9, 15, "a"); rect(a, 7, 11, 8, 14, "A")
    for y in (19, 23):
        rect(a, 5, y, 10, y, "s")
    rect(a, 2, 28, 13, 30, "k"); rect(a, 3, 28, 12, 29, "s")
    px(a, 4, 7, "m"); px(a, 5, 7, "M"); px(a, 10, 25, "m")
    contact(a, 2, 13, 31)
    return img(a)


def looking_glass():
    """1x2: a brass looking-glass on a tripod, aimed south at the fog."""
    a = canvas(1, 2)
    # tripod
    for (x0, x1) in ((7, 2), (8, 13), (7, 7)):
        for y in range(14, 30):
            x = x0 + (x1 - x0) * (y - 14) // 16
            px(a, x, y, "b"); px(a, x + 1, y, "B") if x0 != x1 else None
    inked(a, 5, 12, 10, 15, "c", hi="C")
    # the tube, foreshortened, eyepiece up-left, objective down-right
    for i in range(10):
        x, y = 3 + i, 4 + i // 2
        rect(a, x, y, x, y + 3, "k")
        rect(a, x, y + 1, x, y + 2, "C" if i < 7 else "c")
    px(a, 4, 5, "y"); px(a, 5, 5, "y")
    inked(a, 11, 7, 14, 12, "c", hi="C")
    px(a, 12, 9, "U"); px(a, 13, 10, "u")
    contact(a, 1, 14, 31)
    return img(a)


def ruin_wall():
    """3x2: a broken wall of the old keepers' quarter — dressed stone with a
    gap-toothed top, an empty window, moss and a kelp-strand over it."""
    a = canvas(3, 2)
    rng = random.Random(31)
    tops = [6 + int(5 * abs(np.sin(x / 7.0))) + rng.choice((0, 0, 2)) for x in range(48)]
    for x in range(1, 47):
        rect(a, x, tops[x], x, 29, "k")
        rect(a, x, tops[x] + 1, x, 28, "S")
        px(a, x, tops[x] + 1, "t")
    for y in range(10, 29, 4):
        for x in range(2, 46):
            if (x + (y // 4) * 4) % 9 == 0:
                rect(a, x, y, x, y + 3, "s")
        rect(a, 2, y, 45, y, "s")
    inked(a, 18, 12, 27, 23, "K")             # the empty window
    rect(a, 19, 13, 26, 13, "s")
    rect(a, 18, 12, 27, 12, "t")
    for (x, y) in ((4, 10), (5, 10), (6, 11), (36, 9), (37, 9), (41, 12), (30, 26), (31, 26)):
        px(a, x, y, "m"); px(a, x, y + 1, "M")
    for y in range(9, 22):                    # a kelp strand hung over the sill
        px(a, 33 + (y % 3 == 0), y, "V")
    contact(a, 1, 46, 30)
    contact(a, 1, 46, 31, 80)
    return img(a)


def ruin_pillar():
    a = canvas(1, 2)
    inked(a, 3, 6, 12, 29, "S", hi="t")
    rect(a, 3, 5, 12, 6, "k")
    stamp(a, ["..kk.kkk..", ".ktt.tSSk."], 3, 3)
    for y in range(10, 29, 5):
        rect(a, 4, y, 11, y, "s")
    rect(a, 11, 12, 14, 12, "i"); rect(a, 14, 12, 14, 16, "i")   # an empty lamp-bracket
    px(a, 5, 8, "m"); px(a, 6, 8, "M"); px(a, 4, 20, "m")
    contact(a, 2, 13, 30)
    return img(a)


PIECES = {
    "buoy_lit": buoy_lit, "buoy_dark": buoy_dark, "skerry_light": skerry_light,
    "fogbank_a": fogbank_a, "fogbank_b": fogbank_b,
    "hull": hull, "slip": slip, "kelp_rack": kelp_rack,
    "well_shut": well_shut, "well_open": well_open,
    "waystone": waystone, "looking_glass": looking_glass,
    "ruin_wall": ruin_wall, "ruin_pillar": ruin_pillar,
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
        print(f"  drew farlamp_{stem}  ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
