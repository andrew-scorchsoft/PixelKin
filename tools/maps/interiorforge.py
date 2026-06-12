#!/usr/bin/env python3
"""
interiorforge — the DRAWN interior furniture kit (the gbaforge of furniture).

The first-generation furniture was AI-generated: single-tile-ish props at a
half-isometric angle that floated in front of the walls (the fireplace read as
a pot-belly stove; bookcases showed floor behind them). This module replaces
the lot with code-drawn pieces in the strict SNES interior projection, two
mount classes:

  WALL-MOUNTED (hearth, bookshelf, wares shelf, dresser, stove, lamp rack)
    Pure FRONT elevation, drawn edge-to-edge on the canvas with a cornice
    shadow at the top and a floor contact line at the bottom — designed to be
    placed with their TOP ROW OVERLAPPING the north wall's FACE row (roomkit
    `wall_mount`), so the piece reads as standing AGAINST the wall, never in
    front of it. No perspective top: the wall face supplies the depth.

  FREE-STANDING (beds, tables, counter, crates, barrels, altar, pew, …)
    The genre's top-down-frontal split: a TOP surface for most of the height,
    a short FRONT face strip at the bottom, 1px ink outline, contact shadow.

Palettes mirror build_interior_walls.py (warm wood/plaster, cool stone) so
furniture and architecture share one register. Deterministic; re-run freely.

Run:  ./venv/bin/python tools/maps/interiorforge.py     # write all masters
      (then .claude/skills/generate-sprite-sheet/scripts/pack_objects.py)

WARNING — running this REWRITES EVERY master in assets/tilesets/interior/
objects/, including pieces that gen_interior_object.py later re-rendered via
image-gen into the same paths (the shipped hero pieces). After adding a new
piece, `git checkout` any master you didn't mean to regenerate before packing
(N7 got bitten: a full re-run clobbered 19 image-gen masters with raw draws).

Writes assets/tilesets/interior/objects/<stem>.png (16px multiples) — packed
to `interior_<stem>` object keys.
"""
from __future__ import annotations

import numpy as np
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "interior" / "objects"


def hx(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)] + [255], dtype=np.int16)


# ---- the shared register (build_interior_walls.py palettes) -------------------
WOOD = [hx("#3a2418"), hx("#7a4a28"), hx("#b9763f"), hx("#e0a466")]
BONE = [hx("#7a6f5a"), hx("#bcae90"), hx("#e6dcc0"), hx("#f8f2e2")]
STONE = [hx("#2a2c40"), hx("#4a4d66"), hx("#6c6f86"), hx("#9a9db4")]
FIRE = [hx("#7a2a14"), hx("#c85a22"), hx("#ff8a3d"), hx("#ffc070")]
DEEPBLUE = hx("#13205a")
DIAMOND = hx("#9fe7ff")
INK = hx("#10121e")
BRASS = [hx("#5a431c"), hx("#9a7a30"), hx("#d8b256"), hx("#f4df9a")]
CLOTH_TEAL = [hx("#143c3c"), hx("#1f6a60"), hx("#37978a")]
CLOTH_WINE = [hx("#48182a"), hx("#7a2a44"), hx("#a84a62")]
LINEN = [hx("#bcae90"), hx("#e6dcc0"), hx("#f8f2e2")]


def canvas(tw: int, th: int):
    return np.zeros((th * 16, tw * 16, 4), dtype=np.int16)


def img(a) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def fill(a, x0, y0, x1, y1, c):
    a[y0:y1 + 1, x0:x1 + 1] = c


def outline(a, x0, y0, x1, y1, c):
    a[y0, x0:x1 + 1] = c
    a[y1, x0:x1 + 1] = c
    a[y0:y1 + 1, x0] = c
    a[y0:y1 + 1, x1] = c


def noise(a, x0, y0, x1, y1, amt, seed):
    rng = np.random.default_rng(seed)
    n = rng.integers(-amt, amt + 1, size=(y1 - y0 + 1, x1 - x0 + 1, 1))
    reg = a[y0:y1 + 1, x0:x1 + 1, :3]
    mask = a[y0:y1 + 1, x0:x1 + 1, 3:4] > 0
    a[y0:y1 + 1, x0:x1 + 1, :3] = np.clip(reg + n * mask, 0, 255)


def contact_shadow(a, x0, x1, y):
    """The 1px ink contact line a grounded piece needs (only over transparent)."""
    for x in range(x0, x1 + 1):
        if a[y, x, 3] == 0:
            a[y, x] = np.array([16, 18, 30, 140], np.int16)


# =============================================================================
#  WALL-MOUNTED pieces — pure front elevation, edge-to-edge
# =============================================================================
def _wall_top_shadow(a, w):
    a[0, :w] = INK                       # cornice contact (tucks under the face)
    a[1, :w, :3] = np.clip(a[1, :w, :3] - 26, 0, 255)


def _wall_floor_contact(a, w, h):
    a[h - 2, :w, :3] = np.clip(a[h - 2, :w, :3] - 30, 0, 255)
    a[h - 1, :w] = INK                   # floor contact line


def hearth() -> Image.Image:
    """3x3 chimney-breast fireplace: full-width fieldstone breast, a mantel
    shelf with candles, a wide arched firebox with a living fire. THE focal
    piece of a home — straight-on, flush to the wall."""
    a = canvas(3, 3)
    W, H = 48, 48
    fill(a, 0, 0, W - 1, H - 1, STONE[2])
    # fieldstone courses
    rng = np.random.default_rng(11)
    for y in range(0, H, 6):
        a[y, :W] = STONE[1]
    for y0 in range(0, H, 6):
        for off in rng.integers(2, W - 2, size=3):
            a[y0:y0 + 6, off] = STONE[1]
    noise(a, 0, 0, W - 1, H - 1, 6, 12)
    # mantel shelf
    fill(a, 0, 14, W - 1, 16, WOOD[2])
    a[14, :W] = WOOD[3]
    a[17, :W] = INK
    # candles on the mantel
    for cx in (8, 40):
        fill(a, cx - 1, 9, cx + 1, 13, BONE[3])
        a[8, cx] = FIRE[3]
        a[7, cx] = FIRE[2]
    # the firebox: wide arch
    fill(a, 8, 22, W - 9, H - 6, INK)
    a[20, 12:W - 12] = INK
    a[21, 10:W - 10] = INK
    # firebricks rim
    for x in range(8, W - 8):
        a[22, x] = STONE[0]
    # logs + fire
    fill(a, 16, H - 10, W - 17, H - 8, WOOD[1])
    a[H - 9, 14:W - 14] = WOOD[0]
    for (fx, fy, c) in ((20, 32, FIRE[1]), (24, 28, FIRE[2]), (28, 31, FIRE[1]),
                        (22, 25, FIRE[2]), (26, 24, FIRE[3]), (24, 33, FIRE[2]),
                        (18, 30, FIRE[2]), (30, 28, FIRE[2]), (25, 21, FIRE[3])):
        fill(a, fx - 1, fy, fx + 1, fy + 3, c)
    fill(a, 22, 29, 27, 36, FIRE[3])     # hot core
    # hearthstone lip at the floor
    fill(a, 4, H - 5, W - 5, H - 3, STONE[3])
    a[H - 5, 4:W - 4] = BONE[3]
    _wall_top_shadow(a, W)
    _wall_floor_contact(a, W, H)
    outline(a, 0, 0, W - 1, H - 1, INK)
    return img(a)


def _case(tw, th, seed):
    """A full-frame wooden case (the bookshelf/wares chassis)."""
    a = canvas(tw, th)
    W, H = tw * 16, th * 16
    fill(a, 0, 0, W - 1, H - 1, WOOD[1])
    noise(a, 0, 0, W - 1, H - 1, 5, seed)
    outline(a, 0, 0, W - 1, H - 1, INK)
    fill(a, 1, 1, W - 2, 2, WOOD[2])          # lit top rail
    a[1, 1:W - 1] = WOOD[3]
    for x in (1, W - 2):                       # side stiles
        a[3:H - 2, x] = WOOD[2]
    return a, W, H


def _shelf_rows(a, W, H, rows):
    ys = []
    inner_top, inner_bot = 4, H - 4
    step = (inner_bot - inner_top) // rows
    for r in range(rows):
        y0 = inner_top + r * step
        y1 = y0 + step - 1
        fill(a, 2, y0, W - 3, y1, WOOD[0])     # shadowed bay
        a[y1, 2:W - 2] = WOOD[2]               # the shelf board
        a[y1 - 1, 2:W - 2] = WOOD[3]
        ys.append((y0, y1))
    return ys


def bookshelf() -> Image.Image:
    """2x3 full-height bookcase, front-on, three bays of book spines."""
    a, W, H = _case(2, 3, 21)
    rng = np.random.default_rng(22)
    spines = [CLOTH_TEAL[1], CLOTH_WINE[1], BRASS[1], STONE[2], CLOTH_TEAL[2],
              CLOTH_WINE[2], BONE[1]]
    for (y0, y1) in _shelf_rows(a, W, H, 3):
        x = 3
        while x < W - 4:
            bw = int(rng.integers(2, 4))
            bh = int(rng.integers(7, min(10, y1 - y0)))
            c = spines[int(rng.integers(0, len(spines)))]
            fill(a, x, y1 - bh, x + bw - 1, y1 - 1, c)
            a[y1 - bh, x:x + bw] = np.clip(np.array(c) + 30, 0, 255)
            x += bw + (1 if rng.random() < 0.3 else 0)
    _wall_top_shadow(a, W)
    _wall_floor_contact(a, W, H)
    return img(a)


def shelf_wares() -> Image.Image:
    """2x3 shop shelf: jars, boxes and a lamp on three bays."""
    a, W, H = _case(2, 3, 31)
    rows = _shelf_rows(a, W, H, 3)
    (y0a, y1a), (y0b, y1b), (y0c, y1c) = rows
    # top bay: stout jars
    for cx in (7, 14, 22):
        fill(a, cx - 2, y1a - 7, cx + 2, y1a - 1, CLOTH_TEAL[1])
        fill(a, cx - 1, y1a - 9, cx + 1, y1a - 8, BONE[1])
        a[y1a - 7, cx - 2:cx + 3] = CLOTH_TEAL[2]
    # middle bay: crates/boxes
    for cx, cw in ((8, 8), (20, 7)):
        fill(a, cx - cw // 2, y1b - 6, cx + cw // 2, y1b - 1, WOOD[2])
        outline(a, cx - cw // 2, y1b - 6, cx + cw // 2, y1b - 1, WOOD[0])
    # bottom bay: a little brass lamp + folded cloth
    fill(a, 6, y1c - 6, 10, y1c - 1, BRASS[2])
    a[y1c - 7, 7:10] = BRASS[3]
    a[y1c - 5, 8] = FIRE[3]
    fill(a, 16, y1c - 4, 25, y1c - 1, CLOTH_WINE[1])
    a[y1c - 4, 16:26] = CLOTH_WINE[2]
    _wall_top_shadow(a, W)
    _wall_floor_contact(a, W, H)
    return img(a)


def dresser() -> Image.Image:
    """2x2 chest of drawers, front-on, a small candle-lamp on top."""
    a = canvas(2, 2)
    W, H = 32, 32
    fill(a, 0, 8, W - 1, H - 1, WOOD[1])
    noise(a, 0, 8, W - 1, H - 1, 5, 41)
    outline(a, 0, 8, W - 1, H - 1, INK)
    fill(a, 1, 9, W - 2, 10, WOOD[3])          # lit top
    for (y0, y1) in ((12, 19), (21, 28)):      # two drawers
        fill(a, 3, y0, W - 4, y1, WOOD[2])
        outline(a, 3, y0, W - 4, y1, WOOD[0])
        fill(a, W // 2 - 2, (y0 + y1) // 2, W // 2 + 1, (y0 + y1) // 2 + 1, BRASS[2])
    # candle-lamp on top
    fill(a, 22, 2, 26, 7, BRASS[1])
    a[2, 23:26] = BRASS[3]
    a[4, 24] = FIRE[3]
    a[3, 24] = FIRE[2]
    _wall_floor_contact(a, W, H)
    a[8, :W] = INK                              # its own top contact vs the wall
    return img(a)


def stove() -> Image.Image:
    """2x2 iron kitchen stove, front-on: pipe to the wall, fire slot, kettle."""
    a = canvas(2, 2)
    W, H = 32, 32
    fill(a, 12, 0, 17, 9, STONE[0])             # the pipe runs up the wall face
    a[0:10, 12] = INK
    a[0:10, 17] = INK
    fill(a, 2, 10, W - 3, H - 2, STONE[1])      # the iron body
    outline(a, 2, 10, W - 3, H - 2, INK)
    fill(a, 3, 11, W - 4, 13, STONE[3])         # lit hob top
    fill(a, 7, 18, W - 8, 24, INK)              # fire slot
    fill(a, 9, 20, W - 10, 23, FIRE[2])
    a[21, 12:18] = FIRE[3]
    a[26, 4:10] = STONE[0]                      # legs
    a[26, W - 10: W - 4] = STONE[0]
    # kettle on the hob
    fill(a, 20, 6, 26, 10, BRASS[1])
    a[6, 21:26] = BRASS[2]
    a[5, 23] = BRASS[3]
    _wall_top_shadow(a, W)
    _wall_floor_contact(a, W, H)
    return img(a)


def lamp_rack() -> Image.Image:
    """2x2 rack of hanging vesperlamps — the lamp-tender's trade on a wall."""
    a = canvas(2, 2)
    W, H = 32, 32
    fill(a, 0, 2, W - 1, 5, WOOD[1])            # the rail
    a[2, :W] = WOOD[3]
    a[5, :W] = INK
    noise(a, 0, 2, W - 1, 5, 4, 51)
    for cx in (6, 16, 26):
        a[6:9, cx] = BRASS[1]                   # hanging hooks
        fill(a, cx - 3, 9, cx + 3, 18, BRASS[1])  # lamp body
        outline(a, cx - 3, 9, cx + 3, 18, BRASS[0])
        fill(a, cx - 2, 11, cx + 2, 16, FIRE[2])  # glass + glow
        fill(a, cx - 1, 12, cx + 1, 14, FIRE[3])
        a[8, cx - 1:cx + 2] = BRASS[2]          # hood
        a[19, cx] = BRASS[2]                    # finial
        # glow halo on the wall behind
        for (gx, gy) in ((cx - 4, 13), (cx + 4, 13), (cx, 20)):
            if a[gy, gx, 3] == 0:
                a[gy, gx] = np.array([255, 192, 112, 60], np.int16)
    _wall_top_shadow(a, W)
    return img(a)


# =============================================================================
#  FREE-STANDING pieces — top surface + front face strip
# =============================================================================
def _bed(quilt) -> Image.Image:
    """2x3 bed, straight-on from above: headboard, pillow, quilt, footboard."""
    a = canvas(2, 3)
    W, H = 32, 48
    # headboard
    fill(a, 1, 0, W - 2, 6, WOOD[1])
    a[0, 1:W - 1] = WOOD[2]
    a[1, 2:W - 2] = WOOD[3]
    outline(a, 1, 0, W - 2, 6, INK)
    # mattress + linen
    fill(a, 2, 7, W - 3, H - 8, LINEN[1])
    outline(a, 2, 7, W - 3, H - 8, INK)
    # pillow
    fill(a, 6, 9, W - 7, 15, LINEN[2])
    outline(a, 6, 9, W - 7, 15, LINEN[0])
    a[10, 8:W - 8] = np.array([255, 255, 255, 255], np.int16)
    # quilt from mid-bed down, folded top edge, simple lattice
    fill(a, 3, 18, W - 4, H - 9, quilt[1])
    a[18, 3:W - 3] = quilt[2]
    a[19, 3:W - 3] = quilt[2]
    for y in range(21, H - 9, 5):
        a[y, 4:W - 4] = quilt[0]
    for x in range(6, W - 4, 7):
        a[21:H - 9, x] = quilt[0]
    outline(a, 3, 18, W - 4, H - 9, quilt[0])
    # footboard
    fill(a, 2, H - 7, W - 3, H - 3, WOOD[1])
    a[H - 7, 3:W - 3] = WOOD[3]
    outline(a, 2, H - 7, W - 3, H - 3, INK)
    contact_shadow(a, 2, W - 3, H - 2)
    return img(a)


def bed() -> Image.Image:
    return _bed(CLOTH_TEAL)


def bed_inn() -> Image.Image:
    return _bed(CLOTH_WINE)


def table_round() -> Image.Image:
    """2x2 round table: lit wooden top, short front face."""
    a = canvas(2, 2)
    W, H = 32, 32
    cx, cy, r = 15.5, 13, 12
    for y in range(H):
        for x in range(W):
            d = ((x - cx) ** 2 + ((y - cy) * 1.25) ** 2) ** 0.5
            if d <= r:
                a[y, x] = WOOD[2]
            if r - 1 <= d <= r:
                a[y, x] = INK
    fill(a, 8, 22, W - 9, 27, WOOD[1])          # front face / skirt
    a[27, 8:W - 8] = INK
    a[22, 8:W - 8] = WOOD[0]
    fill(a, 10, 8, 20, 12, WOOD[3])             # top sheen
    a[9, 12:19] = BONE[2]
    contact_shadow(a, 8, W - 9, 28)
    return img(a)


def table_long() -> Image.Image:
    """3x2 plank table for the inn's common room."""
    a = canvas(3, 2)
    W, H = 48, 32
    fill(a, 1, 4, W - 2, 20, WOOD[2])           # top
    for y in (9, 14):
        a[y, 2:W - 2] = WOOD[1]                 # plank seams
    a[5, 2:W - 2] = WOOD[3]
    outline(a, 1, 4, W - 2, 20, INK)
    fill(a, 3, 21, W - 4, 26, WOOD[1])          # front face
    a[26, 3:W - 3] = INK
    for x in (5, W - 7):                        # legs
        fill(a, x, 21, x + 2, 28, WOOD[1])
        a[28, x:x + 3] = INK
    contact_shadow(a, 3, W - 4, 29)
    return img(a)


def stool() -> Image.Image:
    """1x1 round stool."""
    a = canvas(1, 1)
    fill(a, 4, 4, 11, 9, WOOD[2])
    a[4, 5:11] = WOOD[3]
    outline(a, 4, 4, 11, 9, INK)
    fill(a, 5, 10, 6, 12, WOOD[1])
    fill(a, 9, 10, 10, 12, WOOD[1])
    contact_shadow(a, 4, 11, 13)
    return img(a)


def counter() -> Image.Image:
    """4x2 shop counter, straight-on: broad lit top, panelled front."""
    a = canvas(4, 2)
    W, H = 64, 32
    fill(a, 0, 6, W - 1, 14, WOOD[2])           # the top surface
    a[6, :W] = WOOD[3]
    a[7, :W] = WOOD[3]
    outline(a, 0, 6, W - 1, 14, INK)
    fill(a, 0, 15, W - 1, H - 3, WOOD[1])       # panelled front
    for x in range(0, W, 16):
        a[16:H - 3, x] = WOOD[0]
    a[20, :W] = WOOD[2]
    a[H - 3, :W] = INK
    noise(a, 0, 15, W - 1, H - 4, 4, 61)
    # goods on the counter: a scale-lamp + a ledger
    fill(a, 10, 2, 14, 7, BRASS[1])
    a[2, 11:14] = BRASS[3]
    fill(a, 44, 3, 52, 7, CLOTH_WINE[1])
    a[3, 44:53] = CLOTH_WINE[2]
    contact_shadow(a, 0, W - 1, H - 2)
    return img(a)


def rug() -> Image.Image:
    """3x2 bordered woven rug (walk-on; solid:false)."""
    a = canvas(3, 2)
    W, H = 48, 32
    fill(a, 1, 1, W - 2, H - 2, CLOTH_TEAL[1])
    outline(a, 1, 1, W - 2, H - 2, CLOTH_TEAL[0])
    outline(a, 3, 3, W - 4, H - 4, BONE[2])
    fill(a, 8, 8, W - 9, H - 9, CLOTH_TEAL[2])
    # diamond motif
    cx, cy = W // 2, H // 2
    for d in range(5):
        for (x, y) in ((cx - d, cy), (cx + d, cy), (cx, cy - d), (cx, cy + d)):
            a[y, x] = BONE[3] if d < 4 else CLOTH_TEAL[0]
    noise(a, 1, 1, W - 2, H - 2, 4, 71)
    return img(a)


def rug_runner() -> Image.Image:
    """1x3 vertical runner segment (tileable along the aisle; solid:false)."""
    a = canvas(1, 3)
    W, H = 16, 48
    fill(a, 1, 0, W - 2, H - 1, DEEPBLUE)
    a[:, 1] = STONE[0]
    a[:, W - 2] = STONE[0]
    a[:, 3] = DIAMOND * np.array([1, 1, 1, 0]) + np.array([0, 0, 0, 90])
    for y in range(4, H, 12):
        for d in range(3):
            a[y + d, 8 - d] = DIAMOND
            a[y + d, 8 + d] = DIAMOND
            a[y + 6 - d, 8 - d] = DIAMOND
            a[y + 6 - d, 8 + d] = DIAMOND
    noise(a, 1, 0, W - 2, H - 1, 3, 72)
    return img(a)


def crates() -> Image.Image:
    """2x2 stacked storeroom crates."""
    a = canvas(2, 2)
    W, H = 32, 32
    for (x0, y0, x1, y1, sd) in ((2, 14, 17, 29, 81), (14, 16, 29, 29, 82), (8, 2, 22, 15, 83)):
        fill(a, x0, y0, x1, y1, WOOD[2])
        outline(a, x0, y0, x1, y1, INK)
        a[y0 + 1, x0 + 1:x1] = WOOD[3]
        a[y0 + 2:y1, x0 + 1] = WOOD[1]
        # diagonal brace
        for d in range(min(x1 - x0, y1 - y0) - 3):
            a[y0 + 2 + d, x0 + 2 + d] = WOOD[1]
        noise(a, x0, y0, x1, y1, 4, sd)
    contact_shadow(a, 2, W - 3, 30)
    return img(a)


def barrels() -> Image.Image:
    """2x1 pair of stout barrels."""
    a = canvas(2, 1)
    W, H = 32, 16
    for cx in (7, 23):
        fill(a, cx - 6, 1, cx + 6, H - 2, WOOD[1])
        a[1, cx - 4:cx + 5] = WOOD[2]
        outline(a, cx - 6, 1, cx + 6, H - 2, INK)
        fill(a, cx - 5, 3, cx + 5, 5, WOOD[3])      # lid sheen
        for y in (6, 11):
            a[y, cx - 6:cx + 7] = BRASS[1]          # hoops
        a[3, cx - 3:cx + 4] = BONE[2]
    contact_shadow(a, 1, W - 2, H - 1)
    return img(a)


def sacks() -> Image.Image:
    """2x1 grain/wick sacks leaning together."""
    a = canvas(2, 1)
    W, H = 32, 16
    for (cx, top) in ((8, 3), (22, 5)):
        for y in range(top, H - 1):
            half = 6 - max(0, (top + 2 - y))
            fill(a, cx - half, y, cx + half, y, BONE[1])
        outline(a, cx - 6, top + 2, cx + 6, H - 2, BONE[0])
        a[top, cx - 1:cx + 2] = BONE[0]             # tied neck
        a[top + 1, cx - 2:cx + 3] = BONE[2]
        noise(a, cx - 6, top, cx + 6, H - 2, 6, cx)
    contact_shadow(a, 1, W - 2, H - 1)
    return img(a)


def plant() -> Image.Image:
    """1x1 potted fern — the corner-softener."""
    a = canvas(1, 1)
    fill(a, 5, 10, 10, 14, CLOTH_WINE[1])
    a[10, 5:11] = CLOTH_WINE[2]
    outline(a, 5, 10, 10, 14, INK)
    leaf = np.array([47, 122, 80, 255], np.int16)
    leaf_d = np.array([26, 77, 52, 255], np.int16)
    for (x, y) in ((7, 8), (8, 7), (6, 6), (9, 5), (5, 4), (10, 3), (7, 4), (8, 2),
                   (4, 7), (11, 6), (7, 6), (8, 5), (6, 3), (9, 8)):
        a[y, x] = leaf
        a[y + 1, x] = leaf_d
    contact_shadow(a, 5, 10, 15)
    return img(a)


def altar() -> Image.Image:
    """3x3 Lumenary lamp-shrine: two stone steps, a pedestal, the great lantern
    (straight-on; its glow halo overhangs into the wall face)."""
    a = canvas(3, 3)
    W, H = 48, 48
    # dais steps
    fill(a, 2, H - 10, W - 3, H - 6, STONE[2])
    a[H - 10, 3:W - 3] = STONE[3]
    outline(a, 2, H - 10, W - 3, H - 6, INK)
    fill(a, 7, H - 16, W - 8, H - 11, STONE[2])
    a[H - 16, 8:W - 8] = STONE[3]
    outline(a, 7, H - 16, W - 8, H - 11, INK)
    # pedestal
    fill(a, 18, H - 27, W - 19, H - 17, STONE[1])
    outline(a, 18, H - 27, W - 19, H - 17, INK)
    a[H - 27, 19:W - 19] = STONE[3]
    # the great lantern
    fill(a, 16, 6, W - 17, H - 28, BRASS[1])
    outline(a, 16, 6, W - 17, H - 28, BRASS[0])
    fill(a, 18, 9, W - 19, H - 31, FIRE[2])
    fill(a, 20, 11, W - 21, H - 34, FIRE[3])
    a[6, 20:W - 20] = BRASS[2]                   # hood
    a[4:6, 23:25] = BRASS[2]                     # ring
    # glow halo (soft, semi-transparent)
    for (gx, gy) in ((13, 12), (34, 12), (12, 18), (35, 18), (23, 3), (15, 5), (32, 5)):
        if a[gy, gx, 3] == 0:
            a[gy, gx] = np.array([255, 192, 112, 70], np.int16)
    # flanking candles on the lower step
    for cx in (8, 39):
        fill(a, cx - 1, H - 21, cx + 1, H - 17, BONE[3])
        a[H - 22, cx] = FIRE[3]
    contact_shadow(a, 2, W - 3, H - 5)
    return img(a)


def brazier() -> Image.Image:
    """1x2 standing brazier with a tall flame."""
    a = canvas(1, 2)
    W, H = 16, 32
    fill(a, 4, 14, 11, 18, BRASS[1])             # bowl
    a[14, 5:11] = BRASS[2]
    outline(a, 4, 14, 11, 18, BRASS[0])
    a[19:26, 7] = STONE[1]                       # stem
    a[19:26, 8] = STONE[0]
    fill(a, 4, 26, 11, 28, STONE[1])             # base
    a[28, 4:12] = INK
    # flame
    for (fx, fy, c) in ((7, 10, FIRE[2]), (8, 8, FIRE[3]), (6, 7, FIRE[2]),
                        (9, 11, FIRE[2]), (7, 5, FIRE[2]), (8, 4, FIRE[1])):
        fill(a, fx, fy, fx + 1, fy + 3, c)
    fill(a, 7, 10, 8, 13, FIRE[3])
    contact_shadow(a, 4, 11, 29)
    return img(a)


def pew() -> Image.Image:
    """3x1 shrine bench: seat top + front face."""
    a = canvas(3, 1)
    W, H = 48, 16
    fill(a, 1, 2, W - 2, 8, WOOD[2])             # seat
    a[2, 2:W - 2] = WOOD[3]
    outline(a, 1, 2, W - 2, 8, INK)
    fill(a, 2, 9, W - 3, 12, WOOD[1])            # front
    a[12, 2:W - 2] = INK
    for x in (4, W - 6):                         # feet
        fill(a, x, 12, x + 1, 13, WOOD[0])
    contact_shadow(a, 1, W - 2, 14)
    return img(a)


# =============================================================================
#  WALL-HUNG pieces — pure front elevation hung ON the wall (no floor contact).
#  Mount with roomkit.wall_mount(..., solid=False); the banners hang from the
#  cornice over the FACE row (face_row=1, the lamp_rack pattern), the kite hangs
#  HIGH over the cap band (face_row=0) so it clears a 3x3 altar beneath it.
# =============================================================================
ICE = [hx("#16304a"), hx("#2c5a86"), hx("#5e9cc8"), hx("#bfe6f6")]


def _banner(body, trim, emblem) -> Image.Image:
    """1x2 hung wall banner: rod under the cornice, swallowtail cloth, emblem."""
    a = canvas(1, 2)
    W = 16
    # the rod
    fill(a, 1, 2, W - 2, 4, WOOD[1])
    a[2, 1:W - 1] = WOOD[3]
    a[4, 1:W - 1] = INK
    # the cloth: straight drop, then a swallowtail notch
    fill(a, 3, 5, 12, 21, body[1])
    a[5:22, 3] = body[2]                         # lit selvedge
    a[5:22, 12] = body[0]
    for i, y in enumerate(range(22, 27)):        # the two tails
        fill(a, 3, y, 6 - i if 6 - i >= 3 else 3, y, body[1])
        fill(a, 9 + i if 9 + i <= 12 else 12, y, 12, y, body[1])
    a[6, 4:12] = trim                            # trim band under the rod
    a[20, 4:12] = body[0]
    # the emblem: a small lozenge
    for (dx, dy) in ((0, -3), (0, 3), (-2, 0), (2, 0), (-1, -1), (1, -1),
                     (-1, 1), (1, 1), (0, -2), (0, 2), (-1, 0), (0, 0), (1, 0),
                     (0, -1), (0, 1)):
        a[13 + dy, 7 + dx] = trim
    a[13, 7] = emblem
    a[12, 7] = emblem
    _wall_top_shadow(a, W)
    return img(a)


def banner_warm() -> Image.Image:
    """1x2 warm festival banner (kite-silk wine + brass) — the Storm hall."""
    return _banner(CLOTH_WINE, BRASS[3], FIRE[3])


def banner_ice() -> Image.Image:
    """1x2 pale glacier banner (aurora blues) — the Frost hall."""
    return _banner(ICE, ICE[3], BONE[3])


def kite_hung() -> Image.Image:
    """3x2 ceremonial diamond kite hung flat on the wall — the Kite-rising's
    spare flown sail, kept over the Storm altar between festivals."""
    a = canvas(3, 2)
    W, H = 48, 32
    cx, cy, rx, ry = 24, 16, 17, 12
    gold, gold_d = BRASS[3], BRASS[2]
    ember, ember_d = FIRE[2], FIRE[1]
    for y in range(H):
        for x in range(W):
            if abs(x - cx) / rx + abs(y - cy) / ry <= 1.0:
                if (x < cx) == (y < cy):
                    a[y, x] = gold if (x + y) % 7 else gold_d
                else:
                    a[y, x] = ember if (x + y) % 7 else ember_d
    # ink rim + crossed spars
    for y in range(H):
        for x in range(W):
            if a[y, x, 3] and (abs(x - cx) / rx + abs(y - cy) / ry > 0.88):
                a[y, x] = INK
    a[cy, cx - rx + 1:cx + rx] = WOOD[0]
    a[cy - ry + 1:cy + ry, cx] = WOOD[0]
    # centre boss + hanging cords up to the cornice
    fill(a, cx - 1, cy - 1, cx + 1, cy + 1, DIAMOND)
    a[cy, cx] = BONE[3]
    for x0 in (cx - 10, cx + 10):
        a[0:5, x0] = WOOD[0]
    # ribbon tails off the side vertices
    for (tx0, step) in ((cx - rx, -1), (cx + rx - 1, 1)):
        for i in range(4):
            yy = cy + 2 + i
            a[yy, tx0 + step * (i // 2)] = FIRE[3] if i % 2 else CLOTH_WINE[2]
    _wall_top_shadow(a, W)
    return img(a)


def oil_jars() -> Image.Image:
    """2x1 chandlery oil jars (the wick-trade wares)."""
    a = canvas(2, 1)
    W, H = 32, 16
    for (cx, c) in ((7, CLOTH_TEAL), (17, CLOTH_WINE), (26, CLOTH_TEAL)):
        fill(a, cx - 4, 4, cx + 4, H - 2, c[1])
        a[4, cx - 2:cx + 3] = c[2]
        outline(a, cx - 4, 4, cx + 4, H - 2, c[0])
        fill(a, cx - 1, 1, cx + 1, 3, BONE[1])   # cork
        a[7, cx - 3] = c[2]                      # glaze highlight
        a[8, cx - 3] = c[2]
    contact_shadow(a, 2, W - 3, H - 1)
    return img(a)


# =============================================================================
PIECES = {
    # wall-mounted (place with roomkit.wall_mount — top row over the wall face)
    "hearth": hearth, "bookcase": bookshelf, "shelf": shelf_wares,
    "dresser": dresser, "stove": stove, "lamp_rack": lamp_rack,
    # free-standing
    "bed": bed, "bed_inn": bed_inn, "table": table_round, "table_long": table_long,
    "stool": stool, "counter": counter, "rug": rug, "rug_runner": rug_runner,
    "crates": crates, "barrels": barrels, "sacks": sacks, "plant": plant,
    "altar": altar, "brazier": brazier, "pew": pew, "oil_jars": oil_jars,
    # wall-hung (wall_mount with solid=False; the kite mounts at face_row=0)
    "banner_warm": banner_warm, "banner_ice": banner_ice, "kite_hung": kite_hung,
}

# which stems are wall-mounted (roomkit reads this); the last three are
# wall-HUNG — no floor contact, always solid=False
WALL_MOUNTED = {"hearth", "bookcase", "shelf", "dresser", "stove", "lamp_rack",
                "banner_warm", "banner_ice", "kite_hung"}


def main() -> None:
    OBJDIR.mkdir(parents=True, exist_ok=True)
    for stem, fn in PIECES.items():
        im = fn()
        out = OBJDIR / f"{stem}.png"
        im.save(out)
        print(f"  drew {out.relative_to(REPO)}  ({im.width}x{im.height})")
    print(f"{len(PIECES)} furniture masters written — now run pack_objects.py")


if __name__ == "__main__":
    main()
