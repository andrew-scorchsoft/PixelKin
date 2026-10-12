#!/usr/bin/env python3
"""
draw_warp_markers — the small "this is a way through" props, DRAWN IN CODE
(the gbaforge rule: no paid image-gen for small structural markers).

Every warp a player can step on mid-map must LOOK like a way through
(`tools/maps/audit_warp_markers.py`, a CI gate). Most already wear one — a
cave ladder tile, a winch, a headframe, the Old Light's stair sprites — and
these are the markers for the rest:

  cave_mouth       1x2  an arch into a rock wall (top) + its shadowed threshold
  cave_mouth_wide  2x2  the same for a two-tile opening
  side_mouth_e/_w  2x3  a passage running out through an EAST/WEST cave wall
  wood_arch        1x2  a leafy tunnel into a tree mass (a woodland path)
  steps_s          1x1  rock-cut steps going DOWN, south, into the gloom
  steps_n          1x2  rock-cut steps climbing NORTH into a wall
  ladder_up        1x1  the cave-ladder look as an object (for a flag-gated exit)
  mine_hatch       1x1  a timbered shaft-head in open ground, ladder going down
  rope_ladder      1x2  a rope ladder slung from the floor into a shaft
  lift_basket      1x1  the winch's lift platform, ropes rising off the top
  jetty            1x2  a plank jetty stub + mooring post (sand row, water row)
  pier_end         2x2  bollards on a pier's end + a moored skiff below
  sea_buoy         1x1  a lit channel buoy riding the swell
  vigil_seam       1x1  the Starfall Vigil seam OPEN — a standing slit of light
  trapdoor         1x1  an open floor hatch with the brass slide inside
  chute_mouth      1x1  the slide's brass spout at the tower foot
  updraft_vent     1x1  the swirl in the snow where a kite thermal lifts

Colours are sampled from the shared overworld set (cave wall, ladder wood,
holes, leaves) so the markers sit in each region's register; the warm lamp
and starlight accents match `draw_vigil_objects.py`.

Writes assets/tilesets/markers/objects/*.png — packed to `markers_<stem>` by
pack_objects.py.

Run:  python3 tools/maps/draw_warp_markers.py
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "markers" / "objects"


def hx(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


# sampled from vesper_overworld_set (cave_ladder_*, cavewall_edge_s, tree_*)
INK = hx("0c0a14")          # the dark of a hole
HOLE = hx("1e1c28")
ST_O = hx("100f16")         # stone outline
ST_D = hx("2b2839")
ST_M = hx("3b374d")
ST_L = hx("666081")
ST_H = hx("8d87ab")         # lit lip
STEP_H = hx("c4c0d8")       # a stair nosing catching the light
STEP_T = hx("8d87ab")       # a stair tread
FLOOR = hx("343045")
FLOOR_D = hx("292636")
WOOD_O = hx("3e3020")
WOOD_D = hx("76603e")
WOOD_L = hx("a88e60")
WOOD_H = hx("cdb27e")
ROPE = hx("c9b48a")
ROPE_D = hx("8f7a52")
LEAF_O = hx("0c1915")
LEAF_D = hx("122620")
LEAF_M = hx("276159")
LEAF_L = hx("357d77")
LEAF_H = hx("5aa394")
IRON = hx("2a2737")
IRON_L = hx("5d5777")
BRASS_O = hx("5a3e1a")
BRASS_D = hx("a8782e")
BRASS = hx("e0b45a")
BRASS_H = hx("fff0b0")
LAMP = hx("ffcf6b")
LAMP_D = hx("ff8a3d")
PALE = (224, 240, 255)      # starlight (draw_vigil_objects)
MID = (164, 192, 232)
DEEP = (104, 128, 178)
GOLD = (255, 230, 162)
RIPPLE = hx("8fc0ea")
RED = hx("c8483a")
RED_D = hx("8a2c2a")
BONE = hx("f5f0e1")
GLOAM = hx("c88ae0")        # Gloamwood's dusk-violet lantern
WIND_D = hx("4a5f94")       # the gust ink — reads on snow


class Canvas:
    def __init__(self, w: int, h: int):
        self.a = np.zeros((h, w, 4), dtype=np.uint8)
        self.w, self.h = w, h

    def put(self, x, y, rgb, alpha=255):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            if alpha >= 255 or self.a[y, x, 3] == 0:
                self.a[y, x] = (*rgb, alpha)
            else:   # alpha-over an existing pixel
                src = np.array(rgb, dtype=float)
                dst = self.a[y, x, :3].astype(float)
                k = alpha / 255.0
                self.a[y, x, :3] = (src * k + dst * (1 - k)).astype(np.uint8)
                self.a[y, x, 3] = max(self.a[y, x, 3], alpha)

    def rect(self, x0, y0, x1, y1, rgb, alpha=255):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, rgb, alpha)

    def hline(self, x0, x1, y, rgb, alpha=255):
        self.rect(x0, y, x1, y, rgb, alpha)

    def vline(self, x, y0, y1, rgb, alpha=255):
        self.rect(x, y0, x, y1, rgb, alpha)

    def get(self, x, y):
        return self.a[y, x]

    def image(self) -> Image.Image:
        return Image.fromarray(self.a, "RGBA")


# ---------------------------------------------------------------- arches ----

def _arch(c: Canvas, x0: int, x1: int, top: int, bottom: int, fade_from: int,
          rim: bool = True, leafy: bool = False) -> None:
    """A rounded-top opening: interior x0..x1, top row `top`, dark to `bottom`,
    fading out (alpha) below `fade_from` so it melts into the floor."""
    cx = (x0 + x1) / 2
    half = (x1 - x0) / 2 + 0.5
    inside = set()
    for y in range(top, bottom + 1):
        dy = y - top
        # rounded crown over the first ~4 rows
        if dy < 4:
            hw = half * math.sqrt(max(0.0, 1 - ((3.6 - dy) / 4.2) ** 2))
        else:
            hw = half
        for x in range(x0, x1 + 1):
            if abs(x + 0.5 - (cx + 0.5)) <= hw:
                inside.add((x, y))
    for (x, y) in inside:
        if y < fade_from:
            col = INK if y > top + 2 else HOLE
            c.put(x, y, col)
        else:
            k = (y - fade_from) / max(1, bottom - fade_from + 1)
            c.put(x, y, INK, int(225 * (1 - k)))
    if not rim:
        return
    # the rim: two rings of stone (or leaf) outside the opening — lit up-left,
    # shaded down-right — then an outline, so the arch reads at 1x
    def grow(src, excl):
        out = set()
        for (x, y) in src:
            if y >= fade_from - 1:
                continue
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)):
                p = (x + dx, y + dy)
                if p not in excl:
                    out.add(p)
        return out
    ring1 = grow(inside, inside)
    ring2 = grow(ring1, inside | ring1)
    outer = grow(ring2, inside | ring1 | ring2)
    for (x, y) in outer:
        c.put(x, y, LEAF_O if leafy else ST_O)
    for ring, inner in ((ring2, False), (ring1, True)):
        for (x, y) in sorted(ring):
            if leafy:
                col = (LEAF_H if (x + y) % 3 == 0 else LEAF_L) if x <= cx + 1 else LEAF_M
                if not inner:
                    col = LEAF_M if (x * 3 + y) % 4 else LEAF_D
            else:
                if y <= top + 1:
                    col = ST_H if inner else ST_L
                elif x < cx:
                    col = ST_H if inner else ST_L
                else:
                    col = ST_L if inner else ST_M
                if not inner and y > top + 1 and (y + x) % 5 == 0:
                    col = ST_D           # block joints (masonry read)
            c.put(x, y, col)
    if not leafy:
        kx = int(round(cx))
        c.rect(kx - 1, top - 3, kx, top - 2, ST_H)
        c.hline(kx - 2, kx + 1, top - 4, ST_O)


def _glint(c: Canvas, x: int, y: int, warm=True) -> None:
    """A far lamp deep inside the passage — 'this leads somewhere'."""
    core, rim = (LAMP, LAMP_D) if warm else (PALE, MID)
    c.put(x, y, core)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        c.put(x + dx, y + dy, rim, 110)


def cave_mouth() -> Image.Image:
    c = Canvas(16, 32)
    _arch(c, 3, 12, 4, 27, 17)
    _glint(c, 8, 11)
    # rubble at the threshold
    for (x, y, col) in [(2, 19, ST_L), (3, 19, ST_M), (13, 21, ST_L), (12, 22, ST_M)]:
        c.put(x, y, col)
    return c.image()


def cave_mouth_wide() -> Image.Image:
    c = Canvas(32, 32)
    _arch(c, 4, 27, 4, 27, 17)
    _glint(c, 15, 10)
    _glint(c, 20, 12)
    for (x, y, col) in [(3, 19, ST_L), (4, 20, ST_M), (28, 21, ST_L), (27, 22, ST_M)]:
        c.put(x, y, col)
    return c.image()


def wood_arch() -> Image.Image:
    c = Canvas(16, 32)
    _arch(c, 3, 12, 3, 28, 17, leafy=True)
    _glint(c, 8, 9)
    c.put(8, 9, GLOAM)
    c.put(7, 9, GLOAM, 110)
    c.put(9, 9, GLOAM, 110)
    # leaf tufts spilling over the crown
    for (x, y, col) in [(5, 1, LEAF_L), (6, 0, LEAF_H), (10, 1, LEAF_M), (11, 0, LEAF_L),
                        (2, 4, LEAF_L), (13, 5, LEAF_M), (1, 8, LEAF_M), (14, 9, LEAF_D)]:
        c.put(x, y, col)
    return c.image()


def side_mouth(east: bool) -> Image.Image:
    """2x3: col 0 = the floor you stand on, col 1 = the cave wall the passage
    runs out through. Drawn as the arch turned on its side (crown in the wall),
    so it reads as the same kind of mouth as the north-wall ones."""
    c = Canvas(48, 32)
    _arch(c, 6, 41, 6, 31, 18)
    _glint(c, 20, 11)
    _glint(c, 27, 13)
    img = c.image().transpose(Image.ROTATE_270)      # crown -> east
    return img if east else img.transpose(Image.FLIP_LEFT_RIGHT)


# ---------------------------------------------------------------- steps -----

def _treads(c: Canvas, x0: int, x1: int, y_top: int, n: int, step: int,
            lighten_up: bool) -> None:
    """n treads of `step` px from y_top down: lit nosing, tread, dark riser —
    high contrast so a stair reads as a stair (not a grille) at 1x."""
    for i in range(n):
        y = y_top + i * step
        depth = i / max(1, n - 1)
        k = 0.35 * ((1 - depth) if lighten_up else depth)   # deeper = darker
        def shade(col):
            return tuple(int(col[j] * (1 - k) + INK[j] * k) for j in range(3))
        c.hline(x0, x1, y, shade(STEP_H))
        for yy in range(y + 1, y + step - 1):
            c.hline(x0, x1, yy, shade(STEP_T))
        c.hline(x0, x1, y + step - 1, shade(ST_D))
        c.put(x0, y + 1, shade(ST_M))
        c.put(x1, y + 1, shade(ST_M))
    # rough cheek walls
    for y in range(y_top - 1, y_top + n * step):
        c.put(x0 - 1, y, ST_M)
        c.put(x0 - 2, y, ST_O)
        c.put(x1 + 1, y, ST_D)
        c.put(x1 + 2, y, ST_O)


def steps_s() -> Image.Image:
    """Steps going DOWN, south: bright lip at the top, sinking into the dark."""
    c = Canvas(16, 16)
    _treads(c, 3, 12, 1, 4, 4, lighten_up=False)
    c.hline(1, 14, 0, ST_O)
    return c.image()


def steps_n() -> Image.Image:
    """Steps climbing NORTH into a wall: the cut (top tile) + the foot (bottom)."""
    c = Canvas(16, 32)
    # the cut through the rock — dark cheeks rising
    c.rect(1, 0, 14, 1, ST_D)
    _treads(c, 3, 12, 3, 7, 4, lighten_up=True)
    # the foot spills onto the floor tile
    c.hline(1, 14, 30, ST_O, 160)
    c.hline(2, 13, 31, INK, 70)
    return c.image()


def ladder_up() -> Image.Image:
    """The shared cave_ladder_up look, as an OBJECT so a flag can gate it."""
    c = Canvas(16, 16)
    c.rect(2, 0, 13, 15, IRON)
    c.vline(4, 0, 15, WOOD_D)
    c.vline(11, 0, 15, WOOD_D)
    c.vline(5, 0, 15, WOOD_L)
    c.vline(12, 0, 15, WOOD_L)
    for y in (2, 6, 10, 14):
        c.hline(5, 11, y, WOOD_L)
        c.hline(5, 11, y + 1, WOOD_D)
    c.hline(2, 13, 0, ST_O)
    return c.image()


def mine_hatch() -> Image.Image:
    """A timbered shaft-head in open ground: frame, dark drop, ladder top."""
    c = Canvas(16, 16)
    c.rect(1, 2, 14, 15, WOOD_O)
    c.rect(2, 3, 13, 14, WOOD_D)
    c.hline(2, 13, 3, WOOD_H)           # lit top beam
    c.hline(2, 13, 4, WOOD_L)
    c.vline(2, 3, 14, WOOD_L)
    c.rect(4, 6, 11, 13, INK)           # the drop
    c.rect(4, 6, 11, 6, HOLE)
    c.vline(6, 6, 13, WOOD_D)           # ladder rails into the dark
    c.vline(9, 6, 13, WOOD_D)
    for y in (7, 10):
        c.hline(6, 9, y, WOOD_L)
    c.put(6, 12, WOOD_O)
    c.put(9, 12, WOOD_O)
    # corner posts + a hung lamp on the near-left post
    for x in (1, 13):
        c.rect(x, 0, x + 1, 3, WOOD_L)
        c.put(x, 0, WOOD_H)
    c.put(1, 4, LAMP)
    c.put(0, 4, LAMP_D, 140)
    return c.image()


def rope_ladder() -> Image.Image:
    """A rope ladder from an iron stake on the floor (bottom) up into the hole."""
    c = Canvas(16, 32)
    for y in range(0, 27):
        a = 255 if y > 5 else 90 + 30 * y
        c.put(4, y, ROPE, a)
        c.put(11, y, ROPE, a)
        c.put(5, y, ROPE_D, a)
        c.put(12, y, ROPE_D, a)
    for y in range(2, 26, 4):
        a = 255 if y > 5 else 120 + 25 * y
        c.hline(5, 10, y, WOOD_L, a)
        c.hline(5, 10, y + 1, WOOD_D, a)
    # the iron anchor ring + stake
    for (x, y) in [(6, 26), (7, 26), (8, 26), (9, 26), (5, 27), (10, 27),
                   (5, 28), (10, 28), (6, 29), (9, 29)]:
        c.put(x, y, IRON_L)
    c.rect(7, 27, 8, 30, IRON)
    c.put(7, 27, IRON_L)
    c.hline(5, 10, 31, INK, 90)
    return c.image()


def lift_basket() -> Image.Image:
    """The winch's lift: a plank platform with rails, ropes rising off the top."""
    c = Canvas(16, 16)
    c.rect(2, 6, 13, 15, WOOD_O)
    c.rect(3, 7, 12, 14, WOOD_L)
    for y in (9, 12):
        c.hline(3, 12, y, WOOD_D)
    c.hline(3, 12, 7, WOOD_H)
    for x in (2, 13):
        c.vline(x, 3, 15, WOOD_D)
    # ropes up to the winch
    for y in range(0, 7):
        c.put(3 + (1 if y > 4 else 0), y, ROPE)
        c.put(12 - (1 if y > 4 else 0), y, ROPE)
    c.put(7, 4, ROPE_D)
    c.put(8, 4, ROPE_D)
    c.hline(4, 11, 3, ROPE_D)
    c.put(7, 11, LAMP)
    return c.image()


# ---------------------------------------------------------------- water -----

def jetty() -> Image.Image:
    """Top tile on sand: the plank end + a mooring post. Bottom tile: planks out
    over the water on stilts, a ripple at their feet."""
    c = Canvas(16, 32)
    c.rect(3, 4, 12, 26, WOOD_O)
    c.rect(4, 4, 11, 25, WOOD_L)
    for y in range(7, 26, 4):
        c.hline(4, 11, y, WOOD_D)
    c.vline(7, 4, 25, WOOD_D)
    c.hline(4, 11, 4, WOOD_H)
    # stilts under the end
    c.rect(4, 26, 5, 28, WOOD_D)
    c.rect(10, 26, 11, 28, WOOD_D)
    for x in range(2, 14):
        if x % 3:
            c.put(x, 29, RIPPLE, 160)
    # mooring post with a rope coil
    c.rect(12, 1, 14, 9, WOOD_O)
    c.rect(12, 1, 13, 8, WOOD_L)
    c.put(12, 1, WOOD_H)
    for (x, y) in [(11, 6), (12, 6), (13, 6), (14, 6), (11, 7), (14, 7)]:
        c.put(x, y, ROPE)
    c.vline(13, 7, 13, ROPE_D)
    return c.image()


def pier_end() -> Image.Image:
    """2x2 over a 2-wide pier end: iron bollards on the end planks (top row),
    a skiff moored in the water below (bottom row)."""
    c = Canvas(32, 32)
    for bx in (2, 26):
        c.rect(bx, 6, bx + 3, 12, IRON)
        c.rect(bx, 6, bx + 3, 7, IRON_L)
        c.hline(bx - 1, bx + 4, 12, IRON)
        c.put(bx + 1, 6, BONE)
    # mooring lines slung down to the skiff
    for i, y in enumerate(range(10, 21)):
        c.put(6 + i // 2, y, ROPE)
        c.put(25 - i // 2, y, ROPE)
    # the skiff: pointed bow east, wood hull, thwart, a lamp at the stern
    for y in range(18, 29):
        dy = abs(y - 23)
        x0 = 7 + dy // 2
        x1 = 26 - dy
        c.hline(x0, x1, y, WOOD_O)
        if 18 < y < 28:
            c.hline(x0 + 1, x1 - 1, y, WOOD_D if y > 24 else WOOD_L)
    c.rect(10, 20, 22, 26, WOOD_D)
    c.rect(10, 20, 22, 20, WOOD_H)
    c.vline(16, 20, 26, WOOD_L)
    c.vline(17, 20, 26, WOOD_O)
    c.put(9, 22, LAMP)
    c.put(9, 21, LAMP_D, 160)
    for x in range(6, 30):
        if x % 4:
            c.put(x, 30, RIPPLE, 150)
    return c.image()


def sea_buoy() -> Image.Image:
    """A lit channel buoy — the sea-lane across to the rock."""
    c = Canvas(16, 16)
    for x in range(2, 14):
        if x % 3:
            c.put(x, 14, RIPPLE, 170)
    for (x, y) in [(3, 13), (12, 13), (1, 15), (14, 15)]:
        c.put(x, y, RIPPLE, 120)
    # body: a striped cone
    for y in range(6, 14):
        hw = 1 + (y - 6) // 2
        for x in range(8 - hw, 8 + hw):
            band = RED if ((y - 6) // 2) % 2 == 0 else BONE
            if x == 8 - hw:
                band = tuple(min(255, v + 30) for v in band)
            elif x == 7 + hw:
                band = RED_D if band == RED else hx("c8c2b0")
            c.put(x, y, band)
    c.hline(4, 11, 13, IRON)
    # the lamp + its glow
    c.rect(7, 3, 8, 5, LAMP)
    c.put(7, 2, IRON_L)
    c.put(8, 2, IRON_L)
    for (x, y) in [(6, 3), (9, 3), (6, 4), (9, 4), (7, 1), (8, 1)]:
        c.put(x, y, LAMP_D, 130)
    return c.image()


# ---------------------------------------------------------------- vigil -----

def vigil_seam() -> Image.Image:
    """The seam OPEN: a standing slit of starlight with a gold core — distinct
    from the shut `vigil_star_scar` (a faint crack, dawn-only)."""
    c = Canvas(16, 16)
    path = [(8, 1), (8, 2), (7, 3), (7, 4), (8, 5), (8, 6), (8, 7), (9, 8), (9, 9),
            (8, 10), (8, 11), (7, 12), (7, 13), (8, 14)]
    # halo
    for (x, y) in path:
        for dx in (-3, -2, 2, 3):
            c.put(x + dx, y, MID, 50 if abs(dx) == 3 else 90)
    for (x, y) in path:
        c.put(x - 1, y, PALE)
        c.put(x + 1, y, MID)
        c.put(x, y, GOLD)
    for (x, y) in [(8, 5), (9, 9), (7, 12)]:
        c.put(x, y, (255, 255, 255))
    # lips of the seam on the ground
    for (x, y) in [(5, 14), (6, 15), (10, 15), (11, 14)]:
        c.put(x, y, DEEP, 200)
    # motes rising out of it
    for (x, y, a) in [(4, 3, 170), (12, 6, 160), (3, 9, 130), (13, 1, 140)]:
        c.put(x, y, PALE, a)
    return c.image()


# ---------------------------------------------------------------- the slide -

def trapdoor() -> Image.Image:
    """An open floor hatch — lid thrown back, the brass chute curling down."""
    c = Canvas(16, 16)
    # the lid, flipped up against the north
    c.rect(2, 0, 13, 4, WOOD_O)
    c.rect(3, 0, 12, 3, WOOD_L)
    c.hline(3, 12, 0, WOOD_H)
    for x in (6, 9):
        c.vline(x, 0, 3, WOOD_D)
    c.put(4, 4, IRON_L)
    c.put(11, 4, IRON_L)
    # frame + the drop
    c.rect(1, 5, 14, 15, WOOD_O)
    c.rect(2, 6, 13, 14, WOOD_D)
    c.rect(4, 7, 11, 13, INK)
    # the brass chute lip curling away into the dark
    c.hline(4, 11, 7, BRASS_H)
    c.hline(4, 11, 8, BRASS)
    c.hline(5, 10, 9, BRASS_D)
    c.hline(6, 9, 10, BRASS_O)
    c.put(4, 9, BRASS_D)
    c.put(11, 9, BRASS_D)
    return c.image()


def chute_mouth() -> Image.Image:
    """The slide's brass spout coming out of the tower foot (from the west)."""
    c = Canvas(16, 16)
    # the pipe, running in from the west edge
    c.rect(0, 3, 7, 8, BRASS_O)
    c.rect(0, 4, 7, 7, BRASS)
    c.hline(0, 7, 4, BRASS_H)
    c.hline(0, 7, 7, BRASS_D)
    for x in (2, 6):
        c.put(x, 5, BRASS_O)
    # the bend down + flared mouth (opening faces south-east)
    c.rect(6, 5, 12, 13, BRASS_O)
    c.rect(7, 6, 11, 12, BRASS)
    c.vline(7, 6, 12, BRASS_H)
    c.rect(8, 9, 12, 14, BRASS_O)
    c.rect(9, 10, 11, 13, INK)
    c.put(8, 10, BRASS_D)
    c.hline(8, 12, 14, BRASS_D)
    # a little sand heap where riders land
    for (x, y) in [(10, 15), (11, 15), (12, 15), (13, 15), (13, 14)]:
        c.put(x, y, hx("e8d8a8"), 220)
    return c.image()


def updraft_vent() -> Image.Image:
    """Where the thermal lifts a kite: a swirl in the snow, gusts rising off it
    (the ground half of the `windward_updraft` column)."""
    c = Canvas(16, 16)
    cx, cy = 7.5, 11.0
    for t in range(0, 360, 6):
        r = math.radians(t)
        if 150 < t < 200:             # a break in the outer ring: it swirls
            continue
        x, y = cx + 6.5 * math.cos(r), cy + 3.2 * math.sin(r)
        c.put(round(x), round(y), WIND_D if t < 180 else DEEP)
        c.put(round(x), round(y) + 1, WIND_D, 150)
    for t in range(0, 300, 10):
        r = math.radians(t + 40)
        x, y = cx + 3.4 * math.cos(r), cy + 1.6 * math.sin(r)
        c.put(round(x), round(y), MID)
    c.put(8, 11, (255, 255, 255))
    # gusts rising off the swirl (brightest low, thinning as they climb)
    for x0, top in ((4, 3), (8, 1), (11, 4)):
        for i, y in enumerate(range(9, top - 1, -1)):
            x = x0 + (1 if (y // 2) % 2 else 0)
            c.put(x, y, DEEP if i < 3 else MID, max(110, 255 - 20 * i))
    return c.image()


MARKERS = {
    "updraft_vent": updraft_vent,
    "cave_mouth": cave_mouth,
    "cave_mouth_wide": cave_mouth_wide,
    "side_mouth_e": lambda: side_mouth(True),
    "side_mouth_w": lambda: side_mouth(False),
    "wood_arch": wood_arch,
    "steps_s": steps_s,
    "steps_n": steps_n,
    "ladder_up": ladder_up,
    "mine_hatch": mine_hatch,
    "rope_ladder": rope_ladder,
    "lift_basket": lift_basket,
    "jetty": jetty,
    "pier_end": pier_end,
    "sea_buoy": sea_buoy,
    "vigil_seam": vigil_seam,
    "trapdoor": trapdoor,
    "chute_mouth": chute_mouth,
}


def main() -> None:
    OBJDIR.mkdir(parents=True, exist_ok=True)
    for stem, fn in MARKERS.items():
        img = fn()
        assert img.width % 16 == 0 and img.height % 16 == 0, stem
        img.save(OBJDIR / f"{stem}.png")
    print(f"{len(MARKERS)} warp markers -> {OBJDIR.relative_to(REPO)} — now run pack_objects.py")


if __name__ == "__main__":
    main()
