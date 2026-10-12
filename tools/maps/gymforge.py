#!/usr/bin/env python3
"""
gymforge — the DRAWN kit of the Lifting House, Pearlmoor's gym (builder:
build_interiors.build_lifting_house / build_lifting_house_b1).

The house is two floors: the street-level CARDIO hall you walk into
(treadmills, bikes, rowers — Andy is always on a treadmill) and the WEIGHTS
floor down the stairs (bench presses west, squat racks east, the dumbbell
rack under the mirrors). Kept in its OWN master folder, like paulforge, so the
shared interior kit (and interiorforge's full re-runs) never touch it:

    assets/tilesets/gym/objects/<stem>.png   ->  packed as `gym_<stem>`

Projection matches the interior kit: straight-on, top-down-frontal, 1px ink
outline, a soft contact shadow on the floor row. Every piece is drawn in code
(rects/lines/discs) so it is crisp and deterministic; re-run freely.

  FREE-STANDING (solid):   treadmill_belt_s + treadmill_console_s (a 1x3
                           machine in two parts, console at the NEAR end so
                           the runner faces the camera; he stands ON the belt),
                           bike, rower, bench_press, squat_rack, dumbbell_rack,
                           plate_tree, kettlebells, water_cooler
  FLOOR (solid:false):     mat (2x2 rubber tile, tiles seamlessly)
  WALL-HUNG (face row, solid:false): mirror

Run:  python3 tools/maps/gymforge.py [--only a,b]
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "gym" / "objects"

PAL = {
    "k": "#10121e",  # ink
    "i": "#2b2e3c",  # iron (dark)
    "I": "#4a4f63",  # iron (mid)
    "j": "#7d8399",  # iron (light / chrome edge)
    "J": "#c9cfdc",  # chrome glint
    "b": "#161820",  # rubber black
    "B": "#262935",  # rubber lit
    "d": "#20232e",  # belt
    "D": "#33374a",  # belt slat
    "r": "#8a2228",  # upholstery red (shadow)
    "R": "#c23a3a",  # upholstery red
    "s": "#e26a5a",  # upholstery red highlight
    "u": "#1f4f8a",  # bumper-plate blue
    "U": "#3a7bc8",
    "y": "#c89a20",  # bumper-plate yellow
    "Y": "#f0c840",
    "g": "#2f7a3a",  # bumper-plate green
    "G": "#4fae58",
    "w": "#5a3a22",  # platform wood dark
    "W": "#9a6a3c",  # platform wood
    "o": "#c08a52",  # platform wood light
    "l": "#38e07a",  # console LED green
    "L": "#ff6a3a",  # console LED orange
    "c": "#8fc8ea",  # mirror glass
    "C": "#d8f0ff",  # mirror sheen
    "n": "#5d93b8",  # mirror glass shadow
    "a": "#a8dcf0",  # water (cooler bottle)
    "A": "#e8f8ff",
    "p": "#e8e4dc",  # plastic white
    "P": "#b8b2a6",
}


def rgba(hexs: str, alpha: int = 255):
    return np.array([int(hexs[i:i + 2], 16) for i in (1, 3, 5)] + [alpha], dtype=np.int16)


def canvas(tw: int, th: int) -> np.ndarray:
    return np.zeros((th * 16, tw * 16, 4), dtype=np.int16)


def rect(a, x0, y0, x1, y1, ch):
    """Filled rect, inclusive, clipped to the canvas."""
    h, w = a.shape[:2]
    x0, x1 = max(0, x0), min(w - 1, x1)
    y0, y1 = max(0, y0), min(h - 1, y1)
    if x0 <= x1 and y0 <= y1:
        a[y0:y1 + 1, x0:x1 + 1] = rgba(PAL[ch])


def box(a, x0, y0, x1, y1, ch):
    rect(a, x0, y0, x1, y0, ch)
    rect(a, x0, y1, x1, y1, ch)
    rect(a, x0, y0, x0, y1, ch)
    rect(a, x1, y0, x1, y1, ch)


def inked(a, x0, y0, x1, y1, fill, *, hi=None, lo=None):
    """An ink-outlined block: fill, optional 1px highlight (top/left) and
    shadow (bottom/right) inside the outline."""
    rect(a, x0, y0, x1, y1, "k")
    if x1 - x0 >= 2 and y1 - y0 >= 2:
        rect(a, x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)
        if hi and x1 - x0 >= 3:
            rect(a, x0 + 1, y0 + 1, x1 - 1, y0 + 1, hi)
        if lo and y1 - y0 >= 3:
            rect(a, x0 + 1, y1 - 1, x1 - 1, y1 - 1, lo)


def px(a, x, y, ch):
    h, w = a.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        a[y, x] = rgba(PAL[ch])


def disc(a, cx, cy, r, ch):
    h, w = a.shape[:2]
    for y in range(max(0, int(cy - r - 1)), min(h, int(cy + r + 2))):
        for x in range(max(0, int(cx - r - 1)), min(w, int(cx + r + 2))):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                a[y, x] = rgba(PAL[ch])


def ring_disc(a, cx, cy, r, fill, hi=None):
    """An inked disc (outline ring + fill + a top-left highlight arc)."""
    disc(a, cx, cy, r, "k")
    disc(a, cx, cy, r - 1, fill)
    if hi:
        for y in range(int(cy - r), int(cy + 1)):
            for x in range(int(cx - r), int(cx + 1)):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if r - 2.2 <= d <= r - 1.2:
                    px(a, x, y, hi)


def contact(a, x0, x1, y, alpha=90):
    """Soft floor shadow under a piece (on the canvas's bottom rows)."""
    h = a.shape[0]
    for yy, al in ((y, alpha), (y - 1, alpha // 2)):
        if 0 <= yy < h:
            for x in range(max(0, x0), min(a.shape[1], x1 + 1)):
                if a[yy, x, 3] == 0:
                    a[yy, x] = [8, 8, 16, al]


def img(a) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# =============================================================================
#  CARDIO (the street-level hall)
# =============================================================================




def treadmill_console_s():
    """1x1 the treadmill's head seen from BEHIND (the console at the near end,
    so the runner faces the camera): the back of the panel with its vents,
    twin uprights, handrails, and the motor hood the belt runs into."""
    a = canvas(1, 1)
    # motor hood at the base of the tile, on the floor
    inked(a, 1, 10, 14, 15, "I", hi="j", lo="i")
    rect(a, 3, 12, 12, 12, "i")
    # uprights
    rect(a, 2, 4, 3, 10, "k"); rect(a, 12, 4, 13, 10, "k")
    px(a, 2, 5, "j"); px(a, 12, 5, "j")
    # the back of the console panel (vents, no readout)
    inked(a, 1, 0, 14, 5, "i", hi="I")
    for x in range(4, 12, 2):
        rect(a, x, 2, x, 3, "b")
    # handrails
    rect(a, 0, 6, 1, 7, "k"); rect(a, 14, 6, 15, 7, "k")
    px(a, 0, 6, "j"); px(a, 15, 6, "j")
    contact(a, 1, 14, 15)
    return img(a)


def treadmill_belt_s():
    """1x2 the running deck for a console-at-the-near-end machine: the end
    roller at the FAR (north) end, the deck running down into the console."""
    a = canvas(1, 2)
    H = 32
    inked(a, 1, 1, 14, H - 1, "I", hi="j", lo="i")
    rect(a, 3, 3, 12, H - 1, "d")
    for y in range(5, H, 4):
        rect(a, 3, y, 12, y, "D")
    rect(a, 2, 2, 2, H - 1, "j")
    rect(a, 13, 2, 13, H - 1, "i")
    rect(a, 3, 2, 12, 2, "i")  # the far roller cap
    return img(a)


def bike():
    """2x2 an upright exercise bike in side profile (facing west): the heavy
    flywheel, the frame, the saddle, the bars with a small console."""
    a = canvas(2, 2)
    # base stabilisers
    inked(a, 2, 27, 29, 30, "i", hi="I")
    rect(a, 3, 31, 6, 31, "k"); rect(a, 25, 31, 28, 31, "k")
    # flywheel (front, west)
    ring_disc(a, 9, 19, 7, "I", hi="j")
    disc(a, 9, 19, 2, "k"); px(a, 9, 19, "j")
    # flywheel guard (red shell over the top half)
    for y in range(11, 17):
        for x in range(2, 17):
            if (x - 9) ** 2 + (y - 19) ** 2 <= 64 and a[y, x, 3] > 0 and y < 15:
                a[y, x] = rgba(PAL["R"]) if y > 11 else rgba(PAL["s"])
    # main frame tube: flywheel hub -> under saddle, and up to the bars
    for t in range(0, 15):
        px(a, 10 + t, 24 - t // 2, "k"); px(a, 10 + t, 23 - t // 2, "I")
    rect(a, 22, 9, 24, 26, "k"); rect(a, 23, 9, 23, 26, "I")
    # pedal crank
    disc(a, 19, 21, 2, "k"); rect(a, 17, 23, 18, 24, "k"); rect(a, 20, 18, 21, 19, "k")
    # saddle
    inked(a, 19, 6, 29, 9, "b", hi="B")
    # handlebar post + bars + console (front)
    rect(a, 6, 3, 8, 12, "k"); rect(a, 7, 4, 7, 12, "I")
    inked(a, 3, 0, 13, 4, "i", hi="I")
    px(a, 6, 2, "l"); px(a, 7, 2, "l"); px(a, 9, 2, "L")
    rect(a, 1, 5, 6, 6, "k"); px(a, 1, 5, "j")
    contact(a, 1, 30, 31)
    return img(a)


def rower():
    """3x1 a rowing machine in side profile: the fan housing at the west end,
    the long monorail, the sliding seat, the foot stretchers, the handle."""
    a = canvas(3, 1)
    W = 48
    # monorail
    inked(a, 8, 10, W - 2, 12, "I", hi="j")
    rect(a, W - 4, 13, W - 2, 15, "k")
    # fan housing
    ring_disc(a, 7, 8, 7, "i", hi="I")
    for ang in range(0, 360, 60):
        import math
        x = 7 + round(3 * math.cos(math.radians(ang)))
        y = 8 + round(3 * math.sin(math.radians(ang)))
        px(a, x, y, "j")
    disc(a, 7, 8, 1, "k")
    rect(a, 2, 14, 12, 15, "k")
    # foot stretchers
    inked(a, 14, 4, 18, 10, "b", hi="B")
    # handle + chain
    rect(a, 13, 6, 13, 7, "k"); rect(a, 11, 5, 12, 8, "k")
    # seat
    inked(a, 28, 6, 35, 9, "b", hi="B")
    rect(a, 30, 10, 33, 10, "k")
    contact(a, 1, W - 1, 15)
    return img(a)


def water_cooler():
    """1x2 the water cooler: the blue bottle on a white stand, two taps."""
    a = canvas(1, 2)
    # bottle
    inked(a, 4, 0, 11, 11, "a", hi="A")
    rect(a, 6, 2, 6, 9, "A")
    rect(a, 5, 4, 10, 4, "n")
    # stand
    inked(a, 2, 12, 13, 29, "p", hi="p", lo="P")
    rect(a, 4, 15, 5, 16, "u"); rect(a, 10, 15, 11, 16, "R")
    rect(a, 3, 20, 12, 20, "P")
    contact(a, 1, 14, 31)
    return img(a)


# =============================================================================
#  WEIGHTS (downstairs)
# =============================================================================
def _plate_edge(a, x, y0, y1, fill, hi):
    """A bumper plate seen edge-on on a bar: a tall inked slab."""
    inked(a, x, y0, x + 3, y1, fill)
    rect(a, x + 1, y0 + 1, x + 1, y1 - 1, hi)


def _barbell(a, y, x0, x1, plates=(("u", "U"), ("y", "Y"))):
    """A loaded barbell across the canvas at row y: chrome shaft, collars,
    plates stacked on each sleeve (outermost last)."""
    rect(a, x0, y - 1, x1, y + 1, "k")
    rect(a, x0 + 1, y, x1 - 1, y, "j")
    px(a, (x0 + x1) // 2, y, "J")
    n = len(plates)
    for i, (f, h) in enumerate(plates):
        hgt = 6 - i  # outer plates a touch smaller
        _plate_edge(a, x0 + 1 + i * 4, y - hgt, y + hgt, f, h)
        _plate_edge(a, x1 - 4 - i * 4, y - hgt, y + hgt, f, h)
    rect(a, x0 + 1 + n * 4, y - 2, x0 + 2 + n * 4, y + 2, "k")
    rect(a, x1 - 3 - n * 4, y - 2, x1 - 2 - n * 4, y + 2, "k")


def bench_press():
    """3x3 a flat bench press: the racked, loaded bar on its uprights at the
    head (north), the long red pad running toward you, the iron feet."""
    a = canvas(3, 3)
    W, H = 48, 48
    # uprights (behind the bar)
    for x in (13, 33):
        inked(a, x, 2, x + 2, 22, "I", hi="j")
    # J-hooks
    rect(a, 12, 8, 16, 9, "k"); rect(a, 32, 8, 36, 9, "k")
    # the bar, loaded, racked across the top
    _barbell(a, 8, 0, W - 1)
    # the base frame of the uprights
    inked(a, 11, 20, 37, 23, "i", hi="I")
    # the bench pad, running south
    inked(a, 18, 18, 30, 40, "R", hi="s", lo="r")
    rect(a, 19, 21, 19, 38, "s")
    rect(a, 18, 29, 30, 29, "k")  # the seam between back pad and seat
    # bench legs + feet
    inked(a, 21, 41, 27, 43, "i")
    inked(a, 15, 43, 33, 45, "I", hi="j")
    contact(a, 14, 34, H - 1)
    return img(a)


def squat_rack():
    """3x3 a power rack (the squat cage): four posts with holes, the top
    crossmembers and pull-up bar, a loaded bar on the J-hooks at shoulder
    height, the safety arms, the wooden lifting platform underfoot."""
    a = canvas(3, 3)
    W, H = 48, 48
    # the platform (wood centre, rubber wings) on the floor rows
    inked(a, 2, 36, W - 3, 46, "b", hi="B")
    inked(a, 13, 36, W - 14, 46, "W", hi="o", lo="w")
    rect(a, 23, 37, 24, 45, "w")
    # rear posts (shorter, set in — the depth cue)
    for x in (10, 35):
        inked(a, x, 0, x + 2, 36, "i")
    # front posts
    for x in (6, 39):
        inked(a, x, 2, x + 3, 44, "I", hi="j")
        for y in range(6, 42, 4):
            px(a, x + 2, y, "k")
    # top crossmember + pull-up bar
    inked(a, 6, 0, 42, 3, "i", hi="I")
    rect(a, 8, 5, 40, 5, "k"); rect(a, 9, 5, 39, 5, "j")
    # safety arms (low)
    rect(a, 5, 30, 43, 31, "k"); rect(a, 6, 30, 42, 30, "j")
    # the bar on the hooks
    rect(a, 5, 16, 10, 17, "k"); rect(a, 38, 16, 43, 17, "k")
    _barbell(a, 15, 0, W - 1, plates=(("u", "U"), ("g", "G"), ("y", "Y")))
    contact(a, 2, W - 3, H - 1)
    return img(a)


def dumbbell_rack():
    """3x2 a two-tier dumbbell rack: hex dumbbells in pairs, light to heavy
    (west to east), on an iron A-frame."""
    a = canvas(3, 2)
    W, H = 48, 32
    # frame
    inked(a, 1, 8, 3, 29, "I", hi="j")
    inked(a, W - 4, 8, W - 2, 29, "I", hi="j")
    # tiers (the top tier set back = higher)
    inked(a, 1, 10, W - 2, 12, "i", hi="I")
    inked(a, 1, 22, W - 2, 24, "i", hi="I")
    # dumbbells: (head half-size) grows along the row
    def bell(cx, cy, s):
        rect(a, cx - s - 3, cy - 1, cx + s + 3, cy, "k")          # handle shadow
        rect(a, cx - 2, cy - 1, cx + 2, cy - 1, "j")              # handle
        for hx in (cx - s - 3, cx + 3):
            inked(a, hx, cy - s - 1, hx + s, cy + 1, "b", hi="B")
    x = 6
    for i, s in enumerate((2, 2, 3, 3, 3)):
        bell(x + s + 3, 9 - s // 2, s)
        x += 2 * s + 6 + 2
    x = 6
    for i, s in enumerate((3, 3, 4, 4)):
        bell(x + s + 3, 21 - s // 2, s)
        x += 2 * s + 6 + 2
    # feet
    rect(a, 0, 29, 5, 30, "k"); rect(a, W - 6, 29, W - 1, 30, "k")
    contact(a, 1, W - 2, H - 1)
    return img(a)


def plate_tree():
    """1x2 the plate tree: an iron post with bumper plates hung on its pegs."""
    a = canvas(1, 2)
    H = 32
    inked(a, 6, 1, 9, 28, "I", hi="j")
    for cy, f, h, r in ((8, "u", "U", 5), (17, "g", "G", 5), (24, "y", "Y", 4)):
        ring_disc(a, 7.5, cy, r + 0.5, f, hi=h)
        disc(a, 7.5, cy, 1.2, "k")
    inked(a, 2, 28, 13, 30, "i", hi="I")
    contact(a, 1, 14, H - 1)
    return img(a)


def kettlebells():
    """1x1 three kettlebells, small to large."""
    a = canvas(1, 1)
    for cx, cy, r in ((3.5, 11, 2.5), (8.5, 10.5, 3), (13, 10, 3.2)):
        ring_disc(a, cx, cy, r + 0.5, "b", hi="B")
        # the handle arch
        rect(a, int(cx - r + 1), int(cy - r - 3), int(cx + r - 1), int(cy - r - 3), "k")
        rect(a, int(cx - r + 1), int(cy - r - 3), int(cx - r + 1), int(cy - r), "k")
        rect(a, int(cx + r - 1), int(cy - r - 3), int(cx + r - 1), int(cy - r), "k")
    contact(a, 0, 15, 15)
    return img(a)


def mat():
    """2x2 a rubber gym-floor mat (solid:false). Seamless when laid side by
    side: each 16px square carries the same soft bevel and fleck pattern."""
    a = canvas(2, 2)
    rng = np.random.default_rng(16)
    flecks = [(int(x), int(y)) for x, y in rng.integers(2, 14, size=(7, 2))]
    for ty in range(2):
        for tx in range(2):
            ox, oy = tx * 16, ty * 16
            rect(a, ox, oy, ox + 15, oy + 15, "B")
            rect(a, ox + 1, oy + 1, ox + 14, oy + 14, "b")
            rect(a, ox, oy, ox + 15, oy, "I")      # the lit seam
            rect(a, ox, oy, ox, oy + 15, "i")
            for fx, fy in flecks:
                px(a, ox + fx, oy + fy, "B")
    return img(a)


def mirror():
    """2x1 a gym mirror on the wall FACE (wall-hung, solid:false): a chrome
    frame, cool glass, two diagonal sheens."""
    a = canvas(2, 1)
    W = 32
    inked(a, 1, 1, W - 2, 14, "c", hi="j", lo="j")
    box(a, 1, 1, W - 2, 14, "k")
    rect(a, 2, 2, W - 3, 2, "J")
    rect(a, 2, 13, W - 3, 13, "n")
    for d in range(0, 8):
        px(a, 6 + d, 11 - d, "C"); px(a, 7 + d, 11 - d, "C")
        px(a, 17 + d, 11 - d, "C")
    return img(a)


PIECES = {
    "treadmill_console_s": treadmill_console_s, "treadmill_belt_s": treadmill_belt_s,
    "bike": bike, "rower": rower, "water_cooler": water_cooler,
    "bench_press": bench_press, "squat_rack": squat_rack,
    "dumbbell_rack": dumbbell_rack, "plate_tree": plate_tree,
    "kettlebells": kettlebells, "mat": mat, "mirror": mirror,
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
        print(f"  drew gym_{stem}  ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
