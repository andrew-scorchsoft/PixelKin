#!/usr/bin/env python3
"""
sereforge — the DRAWN prop kit of the Sere (Galehigh's dry side) and the Rio Tower.

Kept in its OWN master folder (like paulforge/brewforge) so interiorforge's full
re-runs never touch it:

    assets/tilesets/sere/objects/<stem>.png   ->  packed as `sere_<stem>`

Projection matches the overworld kit: straight-on front elevation, top-left light,
a 1px ink outline, a soft contact shadow. Everything is drawn in code (rects /
polygons / discs) so it is crisp and deterministic; re-run freely. The Rio Tower
itself is an image-gen master (assets/tilesets/sere/objects/rio_tower.png, snapped
by tools/assets/snap_object.py) — this script never writes it.

  THE CALLING RODS:  rod_dark / rod_lit (1x3) — the storm-callers' copper masts
                     with a lamp-cage at the top; the same footprint so a flag swap
                     never changes collision.
  ROCK:              hoodoo (2x3) a wind-cut spire, butte (3x2) a low outcrop,
                     rock_pair (2x2) two boulders
  SCRUB:             thornbush (1x1), saltbush (1x1)
  CAMP:              tent (3x3), campfire (1x1), wagon (3x2), water_jars (2x1)
  RIM:               spyglass (1x2) the lookout glass, rim_post (1x1) a rope post
  INTERIOR:          vista (6x2) the Thunder Table's great window over the canyon,
                     storm_log (2x2) Calder's log on its lectern,
                     barometer (1x2) the storm-glass on the wall,
                     dish_counter (3x2) the kitchen pass ("counter" -> talk across it)

Run:  python3 tools/maps/sereforge.py [--only a,b]
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "sere" / "objects"

INK = (26, 16, 24, 255)
SHADOW = (20, 10, 16, 110)
COPPER = [(92, 44, 30), (150, 78, 44), (206, 122, 70), (246, 186, 120)]
ROCK = [(70, 34, 34), (118, 54, 42), (156, 76, 54), (196, 120, 80), (226, 176, 130)]
VIOLET = [(78, 46, 76), (112, 70, 100)]
SAGE = [(52, 62, 46), (84, 96, 66), (122, 134, 92), (170, 176, 126)]
WOOD = [(58, 36, 26), (96, 60, 38), (138, 92, 58), (180, 130, 84)]
CANVAS = [(150, 132, 112), (196, 178, 150), (232, 218, 190)]
STRIPE = [(140, 54, 44), (176, 72, 54)]
FIRE = [(255, 120, 40), (255, 186, 80), (255, 236, 170)]
LAMP_DARK = [(40, 40, 52), (66, 66, 80)]
LAMP_LIT = [(255, 170, 70), (255, 220, 140), (255, 250, 220)]
STONE = [(86, 80, 92), (124, 116, 124), (170, 160, 160)]
GLASS = [(40, 60, 90), (90, 130, 170), (190, 230, 250)]
SKY = [(14, 18, 44), (22, 32, 78), (34, 48, 104)]


def canvas(tw: int, th: int):
    im = Image.new("RGBA", (tw * 16, th * 16))
    return im, ImageDraw.Draw(im)


def c(rgb, a=255):
    return (*rgb, a)


def shadow(d, x0, y0, x1, y1):
    d.ellipse([x0, y0, x1, y1], fill=SHADOW)


# ---- the calling rods ------------------------------------------------------------
def _rod(lit: bool) -> Image.Image:
    im, d = canvas(1, 3)
    shadow(d, 2, 42, 13, 47)
    # cairn of stones at the foot
    for (x0, y0, x1, y1, k) in [(2, 38, 8, 45, 1), (7, 37, 13, 45, 0), (4, 34, 11, 40, 2)]:
        d.rectangle([x0, y0, x1, y1], fill=c(STONE[k]), outline=INK)
    # the copper mast
    d.rectangle([6, 9, 9, 35], fill=c(COPPER[1]), outline=INK)
    d.line([(7, 10), (7, 34)], fill=c(COPPER[3]))
    # the crossbar with its two little vanes
    d.rectangle([2, 15, 13, 16], fill=c(COPPER[2]), outline=INK)
    d.polygon([(1, 13), (3, 13), (3, 18), (1, 18)], fill=c(COPPER[0]), outline=INK)
    d.polygon([(12, 13), (14, 13), (14, 18), (12, 18)], fill=c(COPPER[0]), outline=INK)
    # the lamp-cage
    d.rectangle([4, 2, 11, 9], fill=c((LAMP_LIT if lit else LAMP_DARK)[0]), outline=INK)
    d.rectangle([6, 4, 9, 7], fill=c((LAMP_LIT if lit else LAMP_DARK)[1]))
    d.line([(7, 1), (8, 1)], fill=INK)
    for x in (5, 10):
        d.line([(x, 3), (x, 8)], fill=c(COPPER[0]))
    if lit:
        d.point((7, 5), fill=c(LAMP_LIT[2]))
        for (x, y, a) in [(2, 3, 150), (13, 4, 150), (1, 7, 90), (14, 9, 90), (7, 0, 170)]:
            d.point((x, y), fill=c(LAMP_LIT[1], a))
        # a little arc of storm-blue spark off the vane
        for (x, y) in [(0, 12), (15, 11)]:
            d.point((x, y), fill=c((170, 200, 255), 200))
    return im


def rod_dark() -> Image.Image:
    return _rod(False)


def rod_lit() -> Image.Image:
    return _rod(True)


# ---- rock ---------------------------------------------------------------------------
def _strata_fill(d, poly, x0, y0, x1, y1, bands):
    """Fill a polygon with horizontal strata (draw bands, clipped by a mask)."""
    mask = Image.new("L", (x1 + 1, y1 + 1), 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    layer = Image.new("RGBA", mask.size)
    ld = ImageDraw.Draw(layer)
    y = y0
    i = 0
    while y <= y1:
        h, col = bands[i % len(bands)]
        ld.rectangle([x0, y, x1, y + h - 1], fill=c(col))
        y += h
        i += 1
    return layer, mask


def hoodoo() -> Image.Image:
    im, d = canvas(2, 3)
    shadow(d, 4, 41, 28, 47)
    body = [(9, 44), (8, 30), (11, 22), (10, 14), (13, 10), (19, 10), (22, 14), (21, 22),
            (24, 30), (23, 44)]
    bands = [(3, ROCK[2]), (2, ROCK[3]), (3, ROCK[1]), (2, ROCK[4]), (4, ROCK[2]), (2, VIOLET[1])]
    layer, mask = _strata_fill(d, body, 0, 8, 31, 47, bands)
    im.paste(layer, (0, 0), mask)
    d.polygon(body, outline=INK)
    # the cap stone (harder, darker, wider)
    cap = [(7, 10), (9, 5), (16, 3), (24, 5), (26, 10), (20, 12), (12, 12)]
    d.polygon(cap, fill=c(ROCK[1]), outline=INK)
    d.line([(10, 6), (16, 4), (22, 6)], fill=c(ROCK[3]))
    # shade the right flank
    d.line([(21, 15), (22, 22), (22, 30), (21, 43)], fill=c(ROCK[0]))
    d.line([(10, 16), (10, 22)], fill=c(ROCK[4]))
    return im


def butte() -> Image.Image:
    im, d = canvas(3, 2)
    shadow(d, 2, 25, 46, 31)
    body = [(3, 29), (5, 14), (9, 9), (38, 8), (43, 13), (45, 29)]
    bands = [(2, ROCK[4]), (3, ROCK[2]), (2, ROCK[3]), (3, ROCK[1]), (4, ROCK[2]), (3, VIOLET[1]), (8, ROCK[1])]
    layer, mask = _strata_fill(d, body, 0, 8, 47, 31, bands)
    im.paste(layer, (0, 0), mask)
    d.polygon(body, outline=INK)
    d.line([(10, 9), (37, 9)], fill=c(ROCK[4]))
    d.line([(42, 13), (44, 28)], fill=c(ROCK[0]))
    return im


def rock_pair() -> Image.Image:
    im, d = canvas(2, 2)
    shadow(d, 2, 25, 30, 31)
    d.ellipse([2, 12, 19, 29], fill=c(ROCK[2]), outline=INK)
    d.ellipse([5, 14, 12, 20], fill=c(ROCK[3]))
    d.ellipse([15, 18, 29, 30], fill=c(ROCK[1]), outline=INK)
    d.ellipse([17, 20, 22, 24], fill=c(ROCK[2]))
    return im


# ---- scrub ----------------------------------------------------------------------------
def thornbush() -> Image.Image:
    im, d = canvas(1, 1)
    shadow(d, 2, 12, 14, 15)
    for (x0, y0, x1, y1, k) in [(1, 5, 9, 13, 1), (6, 4, 14, 13, 1), (3, 2, 11, 10, 2)]:
        d.ellipse([x0, y0, x1, y1], fill=c(SAGE[k]), outline=c(SAGE[0]))
    for (x, y) in [(4, 4), (9, 3), (12, 7), (6, 8), (2, 9)]:
        d.point((x, y), fill=c(SAGE[3]))
    for (x, y) in [(5, 6), (10, 9)]:
        d.point((x, y), fill=c((200, 90, 80)))      # a couple of dry red berries
    return im


def saltbush() -> Image.Image:
    im, d = canvas(1, 1)
    shadow(d, 3, 12, 13, 15)
    for i, x in enumerate(range(3, 14, 2)):
        top = 4 + (i % 3) * 2
        d.line([(8, 14), (x, top)], fill=c(WOOD[1]))
        d.point((x, top), fill=c(CANVAS[2]))
        d.point((x, top + 1), fill=c(SAGE[3]))
    return im


# ---- the drovers' camp -------------------------------------------------------------------
def tent() -> Image.Image:
    im, d = canvas(3, 3)
    shadow(d, 2, 40, 46, 47)
    body = [(4, 44), (24, 6), (44, 44)]
    d.polygon(body, fill=c(CANVAS[1]), outline=INK)
    # stripes down the canvas
    for i, x in enumerate(range(10, 40, 7)):
        d.line([(x, 44), (24, 8)], fill=c(STRIPE[i % 2]), width=2)
    d.polygon([(24, 6), (44, 44), (34, 44)], fill=c(CANVAS[0]))   # shaded flank
    # the door flap (dark), pegged open
    d.polygon([(18, 44), (24, 24), (30, 44)], fill=c((40, 26, 30)), outline=INK)
    d.line([(24, 24), (31, 40)], fill=c(CANVAS[2]))
    d.line([(24, 2), (24, 7)], fill=c(WOOD[0]))
    d.polygon([(24, 2), (30, 4), (24, 5)], fill=c(STRIPE[1]))     # pennant
    d.polygon(body, outline=INK)
    return im


def campfire() -> Image.Image:
    im, d = canvas(1, 1)
    for (x, y) in [(2, 12), (5, 14), (9, 14), (12, 12), (3, 10), (12, 9)]:
        d.ellipse([x - 2, y - 1, x + 2, y + 1], fill=c(STONE[1]), outline=INK)
    d.line([(4, 12), (11, 9)], fill=c(WOOD[0]), width=2)
    d.line([(4, 9), (11, 12)], fill=c(WOOD[1]), width=2)
    d.polygon([(5, 11), (8, 2), (11, 11)], fill=c(FIRE[0]))
    d.polygon([(6, 11), (8, 5), (10, 11)], fill=c(FIRE[1]))
    d.line([(8, 8), (8, 10)], fill=c(FIRE[2]))
    return im


def wagon() -> Image.Image:
    im, d = canvas(3, 2)
    shadow(d, 2, 26, 46, 31)
    d.rectangle([4, 12, 42, 22], fill=c(WOOD[2]), outline=INK)
    for x in range(8, 42, 6):
        d.line([(x, 13), (x, 21)], fill=c(WOOD[1]))
    d.line([(5, 13), (41, 13)], fill=c(WOOD[3]))
    # its load: jars + a rolled canvas
    d.ellipse([8, 4, 16, 13], fill=c((170, 96, 60)), outline=INK)
    d.ellipse([16, 6, 23, 13], fill=c((150, 84, 54)), outline=INK)
    d.rounded_rectangle([25, 6, 40, 12], 3, fill=c(CANVAS[1]), outline=INK)
    d.line([(26, 9), (39, 9)], fill=c(STRIPE[0]))
    for cx in (12, 36):
        d.ellipse([cx - 6, 18, cx + 6, 30], fill=c(WOOD[1]), outline=INK)
        d.ellipse([cx - 2, 22, cx + 2, 26], fill=c(WOOD[3]))
    d.line([(42, 18), (47, 16)], fill=c(WOOD[0]), width=2)          # the shaft
    return im


def water_jars() -> Image.Image:
    im, d = canvas(2, 1)
    shadow(d, 2, 12, 30, 15)
    for i, x in enumerate((3, 12, 21)):
        d.ellipse([x, 3, x + 8, 14], fill=c((178, 100, 64) if i % 2 == 0 else (156, 86, 56)), outline=INK)
        d.rectangle([x + 2, 1, x + 6, 3], fill=c((120, 66, 44)), outline=INK)
        d.point((x + 2, 6), fill=c((230, 170, 120)))
    return im


# ---- the rim ---------------------------------------------------------------------------
def spyglass() -> Image.Image:
    im, d = canvas(1, 2)
    shadow(d, 2, 28, 14, 31)
    for (x0, x1) in ((3, 8), (12, 8), (8, 8)):
        d.line([(x0, 30), (x1, 16)], fill=c(WOOD[1]), width=1)
    d.line([(2, 13), (14, 7)], fill=INK, width=4)
    d.line([(2, 13), (14, 7)], fill=c(COPPER[2]), width=2)
    d.ellipse([12, 5, 15, 9], fill=c(GLASS[2]), outline=INK)
    d.point((5, 11), fill=c(COPPER[3]))
    return im


def rim_post() -> Image.Image:
    im, d = canvas(1, 1)
    shadow(d, 4, 13, 12, 15)
    d.rectangle([6, 3, 9, 14], fill=c(WOOD[2]), outline=INK)
    d.line([(7, 4), (7, 13)], fill=c(WOOD[3]))
    d.line([(0, 6), (15, 7)], fill=c(CANVAS[0]), width=1)        # the rope
    return im


# ---- the Rio Tower's rooms ------------------------------------------------------------
def vista() -> Image.Image:
    """The Thunder Table's great window: three tall arched panes over the
    Thousandfold at dusk (strata, mesas, a far storm shelf), set in sandstone."""
    im, d = canvas(6, 2)
    d.rectangle([0, 0, 95, 31], fill=c((150, 96, 66)), outline=INK)
    for i in range(3):
        x0 = 3 + i * 31
        x1 = x0 + 27
        d.rectangle([x0, 4, x1, 29], fill=c(SKY[1]))
        d.rectangle([x0, 4, x1, 9], fill=c(SKY[0]))
        d.rectangle([x0, 14, x1, 16], fill=c(SKY[2]))
        # far canyon walls in strata
        for k, (yy, col) in enumerate([(17, ROCK[3]), (19, ROCK[1]), (21, ROCK[4]), (23, VIOLET[1]),
                                        (25, ROCK[2]), (27, VIOLET[0])]):
            d.rectangle([x0, yy, x1, yy + 1], fill=c(col))
        d.polygon([(x0 + 8, 29), (x0 + 13, 20), (x0 + 18, 29)], fill=c(VIOLET[0]))   # the gorge
        for (sx, sy) in [(x0 + 4, 6), (x0 + 17, 5), (x0 + 23, 8), (x0 + 10, 11)]:
            d.point((sx, sy), fill=c((220, 230, 255)))
        if i == 2:   # the storm shelf, far right
            d.ellipse([x0 + 10, 9, x1 + 4, 16], fill=c((54, 40, 70)))
            d.line([(x0 + 20, 15), (x0 + 18, 19), (x0 + 21, 21)], fill=c((210, 200, 255)))
        d.rectangle([x0, 4, x1, 29], outline=INK)
        d.line([(x0 + 14, 4), (x0 + 14, 29)], fill=c(WOOD[0]))
        # sill
        d.rectangle([x0 - 1, 29, x1 + 1, 31], fill=c((196, 146, 102)), outline=INK)
    return im


def storm_log() -> Image.Image:
    im, d = canvas(2, 2)
    shadow(d, 4, 26, 28, 31)
    d.polygon([(12, 30), (14, 16), (18, 16), (20, 30)], fill=c(WOOD[1]), outline=INK)
    d.polygon([(4, 12), (28, 12), (26, 19), (6, 19)], fill=c(WOOD[2]), outline=INK)
    d.rectangle([7, 6, 25, 14], fill=c(CANVAS[2]), outline=INK)    # the open log
    d.line([(16, 6), (16, 14)], fill=c(CANVAS[0]))
    for y in (8, 10, 12):
        d.line([(9, y), (14, y)], fill=c((90, 80, 90)))
        d.line([(18, y), (23, y)], fill=c((90, 80, 90)))
    d.line([(19, 9), (21, 11), (20, 12)], fill=c((80, 110, 200)))  # a little bolt doodle
    return im


def barometer() -> Image.Image:
    im, d = canvas(1, 2)
    d.rectangle([4, 1, 11, 28], fill=c(WOOD[1]), outline=INK)
    d.ellipse([3, 3, 12, 12], fill=c(CANVAS[2]), outline=INK)
    d.line([(7, 8), (10, 5)], fill=INK)
    d.rectangle([7, 14, 8, 26], fill=c(GLASS[1]), outline=INK)
    d.rectangle([7, 20, 8, 26], fill=c((200, 60, 60)))
    return im


def dish_hatch() -> Image.Image:
    """The kitchen pass: a tiled counter with a bell, steaming bowls and a slate."""
    im, d = canvas(3, 2)
    d.rectangle([0, 10, 47, 31], fill=c(WOOD[1]), outline=INK)
    d.rectangle([0, 8, 47, 13], fill=c((196, 146, 102)), outline=INK)   # the tiled top
    for x in range(4, 47, 6):
        d.line([(x, 9), (x, 12)], fill=c((150, 96, 66)))
    for x in range(3, 46, 8):
        d.line([(x, 16), (x, 29)], fill=c(WOOD[0]))
    # two bowls + steam, the service bell, a slate menu
    for bx in (6, 19):
        d.ellipse([bx, 3, bx + 9, 10], fill=c((170, 96, 60)), outline=INK)
        d.ellipse([bx + 2, 3, bx + 7, 6], fill=c((120, 70, 40)))
        d.point((bx + 3, 1), fill=c(CANVAS[2], 180))
        d.point((bx + 6, 0), fill=c(CANVAS[2], 140))
    d.polygon([(33, 10), (35, 4), (39, 4), (41, 10)], fill=c(COPPER[2]), outline=INK)
    d.point((37, 3), fill=c(COPPER[3]))
    d.rectangle([28, 16, 44, 26], fill=c((40, 44, 48)), outline=INK)
    for y in (18, 21, 24):
        d.line([(30, y), (41, y)], fill=c((200, 200, 190)))
    return im


PIECES = {
    "rod_dark": rod_dark, "rod_lit": rod_lit,
    "hoodoo": hoodoo, "butte": butte, "rock_pair": rock_pair,
    "thornbush": thornbush, "saltbush": saltbush,
    "tent": tent, "campfire": campfire, "wagon": wagon, "water_jars": water_jars,
    "spyglass": spyglass, "rim_post": rim_post,
    "vista": vista, "storm_log": storm_log, "barometer": barometer, "dish_counter": dish_hatch,
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
        print(f"  drew sere_{stem}  ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
