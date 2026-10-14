#!/usr/bin/env python3
"""
drownlightforge — THE DROWNLIGHT's drawn kit (walkthrough/11-the-hollowing-country.md
Part B, lane N2): the first lamp the Hollowing put out, climbed in the dark.

Two outputs, both deterministic (re-run freely):

1. THREE COLD INTERIOR SETS (the Old Light pattern, build_oldlight_sets.py): pixel
   transforms of `interior_stone_set` with the IDENTICAL tile order/count/metadata,
   so roomkit's FLOOR/FACE/band gids hold. Each floor is colder and darker than the
   one below — the tower gets quieter as you climb.

     drownlight_f1_set       The Oil Stores: slate flagstones, salt-crust specks,
                             a sea-green damp line on the faces
     drownlight_f2_set       The Lens Gallery: bluer, dimmer, the flags worn smooth
     drownlight_lantern_set  The Lantern Room: near-black blue stone, a faint
                             brass lip on the walls (the room was made for light)

   Writes assets/tilesets/drownlight/sets/<name>.png (master) +
          public/assets/tilesets/<name>.webp + .tileset.json (lossless, served).

2. OBJECT MASTERS in assets/tilesets/drownlight/objects/ (packed by
   pack_objects.py -> `drownlight_*`), drawn in code in the gbaforge register
   (flat anchors, 1px ink, deliberate motifs — never noise):

     well / well_lit         a light-well's grated mouth in a wall face (1x1);
                             lit = the banked lamp's light leaking through it
     glare_h / glare_v       the leak itself across a doorway (1x1, translucent):
                             _h runs side to side (a doorway in a N/S wall),
                             _v falls top to bottom (a doorway in an E/W wall)
     crank / crank_on        a shutter-crank on the wall (1x2: the wheel over
                             the face, the housing on the floor); WHITE flag =
                             the louvre at rest, RED = thrown (the post tell)
     great_lamp / _lit       the Drownlight's great lamp (4x4): iron shutters
                             bolted shut round the lens / folded open, blazing
     cot                     the keepers' iron cot, grey blanket (1x2) — rest
     slate                   a chalk slate of names, wall-hung (2x1)
     shutter_plate           a labelled spare shutter, wall-hung (1x1)
     lens_spare              the spare lens in its cradle (2x2)
     lighthouse_lit          the coldfog lighthouse, its lamp room ALIGHT (4x7;
                             drawn from the served coldfog_lighthouse — the
                             post-dawn twin on the foot map)

Run:  python3 tools/maps/drownlightforge.py      (then pack_objects.py)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_oldlight_sets as ols  # noqa: E402  (shared load/assemble/colour helpers)

REPO = Path(__file__).resolve().parents[2]
BASE = REPO / "assets" / "tilesets" / "drownlight"
SETS = BASE / "sets"
OBJ = BASE / "objects"
SERVED = REPO / "public" / "assets" / "tilesets"
T = 16

# ---- palette ------------------------------------------------------------------------
INK = (14, 16, 24)
IRON = (62, 68, 82)
IRON_LT = (110, 118, 136)
IRON_DK = (34, 38, 50)
RUST = (122, 74, 52)
BRASS = (190, 146, 70)
BRASS_LT = (236, 200, 120)
BRASS_DK = (116, 82, 40)
STONE = (118, 126, 134)
STONE_LT = (162, 170, 176)
STONE_DK = (70, 76, 86)
GLOW = (255, 222, 140)
GLOW_HOT = (255, 248, 220)
GLOW_DK = (226, 160, 72)
LENS = (96, 132, 150)
LENS_LT = (168, 204, 214)
LENS_DK = (44, 62, 78)
WOOL = (126, 128, 138)
WOOL_LT = (164, 166, 176)
WOOL_DK = (84, 86, 98)
WOOD = (98, 72, 52)
WOOD_LT = (138, 104, 72)
WOOD_DK = (62, 44, 32)
CHALK = (226, 228, 222)
SLATE = (40, 46, 54)
RED = (196, 62, 52)
WHITE = (232, 232, 222)


# =====================================================================================
# 1. the three cold sets
# =====================================================================================
FLOORS, MAT, FACES, BANDS, INSET = ols.FLOORS, ols.MAT, ols.FACES, ols.BANDS, ols.INSET


def _specks(t, pts, col, k):
    for (x, y) in pts:
        ols.paint(t, x, y, np.array(col, np.float64), k)


def f1(src):
    """The Oil Stores: slate-cold, a salt crust on the flags, a damp line on the faces."""
    out = [ols.mul(ols.saturate(t, 0.55), 0.9, 0.97, 1.0, add=(0, 4, 4)) for t in src]
    for i in FLOORS:
        out[i] = ols.mul(ols.saturate(src[i], 0.35), 0.86, 0.94, 0.94, add=(4, 8, 8))
        _specks(out[i], ((3, 5), (4, 5), (11, 2), (12, 12), (6, 13), (13, 8)), (226, 232, 226), 0.55)
    for i in FACES + (INSET,):
        t = out[i]
        for x in range(T):  # the sea-green damp line, an uneven tide-mark low on the face
            y = 12 + (1 if (x * 7) % 5 == 0 else 0)
            t[y, x, :3] = t[y, x, :3] * 0.55 + np.array((60, 96, 88)) * 0.45
            t[y + 1, x, :3] *= 0.8
    return out


def f2(src):
    """The Lens Gallery: bluer, dimmer, the flags worn smooth (half the grain)."""
    out = [ols.mul(ols.saturate(t, 0.5), 0.74, 0.84, 1.0) for t in src]
    for i in FLOORS:
        t = ols.mul(ols.saturate(src[i], 0.3), 0.78, 0.86, 0.98, add=(0, 4, 10))
        L = ols.lum(t)[..., None]
        m = L.mean()
        t[..., :3] = np.clip(t[..., :3] - 0.45 * (L - m), 0, 255)   # worn smooth
        _specks(t, ((5, 4), (12, 10), (2, 12)), (196, 214, 232), 0.4)
        out[i] = t
    for i in FACES + (INSET,):
        t = out[i]
        for x in range(T):
            y = 11 + (1 if (x * 5) % 7 == 0 else 0)
            t[y, x, :3] = t[y, x, :3] * 0.6 + np.array((50, 80, 96)) * 0.4
    return out


def lantern(src):
    """The Lantern Room: near-black blue stone; a faint brass lip on the walls
    (the room was built to hold light, and remembers)."""
    out = [ols.mul(ols.saturate(t, 0.45), 0.64, 0.72, 0.92) for t in src]
    for i in FLOORS:
        t = ols.mul(ols.saturate(src[i], 0.25), 0.7, 0.76, 0.9, add=(0, 2, 8))
        _specks(t, ((7, 7), (8, 8), (15, 0)), (210, 180, 120), 0.35)   # old wax drips
        out[i] = t
    brass = np.array(BRASS, np.float64)
    for i in BANDS:
        t = out[i]
        L = ols.lum(t)
        for y, x in zip(*np.nonzero(L > 70)):
            t[y, x, :3] = t[y, x, :3] * 0.55 + brass * 0.45
    return out


SET_SPECS = {"drownlight_f1_set": f1, "drownlight_f2_set": f2, "drownlight_lantern_set": lantern}


def build_set(name: str, fn) -> None:
    src, side = ols.load("interior_stone_set")
    tiles = fn(src)
    for a, b in zip(tiles, src):
        a[..., 3] = b[..., 3]
        a[a[..., 3] == 0] = 0
    band, floor = ols.readability(tiles, name)
    for i in FLOORS:
        assert ols.seam_score(tiles[i]) < 1.6, f"{name}: a floor fill shows its seam"
    im = ols.assemble(tiles)
    SETS.mkdir(parents=True, exist_ok=True)
    im.save(SETS / f"{name}.png")
    out = SERVED / f"{name}.webp"
    im.save(out, "WEBP", lossless=True, quality=100, method=6)
    back = np.asarray(Image.open(out).convert("RGBA"))
    assert (back == np.asarray(im)).all(), f"{name}: WebP not lossless"
    side = dict(side, name=name, image=f"assets/tilesets/{name}.webp")
    (SERVED / f"{name}.tileset.json").write_text(json.dumps(side, indent=2) + "\n")
    print(f"  {name}: band lum {band:.0f} < floor lum {floor:.0f}")


# =====================================================================================
# 2. objects
# =====================================================================================
def clear(w=1, h=1):
    return np.zeros((h * T, w * T, 4), dtype=np.int16)


def px(a, x, y, rgb, alpha=255):
    h, w = a.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        a[y, x, :3] = rgb
        a[y, x, 3] = alpha


def blend(a, x, y, rgb, alpha):
    """Composite a translucent pixel over what's there (alpha 0..255)."""
    h, w = a.shape[:2]
    if not (0 <= x < w and 0 <= y < h):
        return
    sa = alpha / 255.0
    da = a[y, x, 3] / 255.0
    oa = sa + da * (1 - sa)
    if oa <= 0:
        return
    for c in range(3):
        a[y, x, c] = int((rgb[c] * sa + a[y, x, c] * da * (1 - sa)) / oa)
    a[y, x, 3] = int(oa * 255)


def rect(a, x0, y0, x1, y1, rgb, alpha=255):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(a, x, y, rgb, alpha)


def disc(a, cx, cy, r, rgb, alpha=255):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r:
                px(a, x, y, rgb, alpha)


def outline(a, rgb=INK):
    h, w = a.shape[:2]
    op = a[..., 3] > 200
    pts = []
    for y in range(h):
        for x in range(w):
            if op[y, x]:
                continue
            for (nx, ny) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < w and 0 <= ny < h and op[ny, nx]:
                    pts.append((x, y))
                    break
    for (x, y) in pts:
        if a[y, x, 3] < 120:
            px(a, x, y, rgb)


def save(a, stem):
    OBJ.mkdir(parents=True, exist_ok=True)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")
    assert im.width % T == 0 and im.height % T == 0, stem
    im.save(OBJ / f"{stem}.png")
    print(f"  object drownlight_{stem}  {im.width}x{im.height}")


# ---- the light-well mouth --------------------------------------------------------------
def well(lit: bool):
    a = clear()
    disc(a, 8, 8, 6.6, IRON_DK)
    disc(a, 8, 8, 5.6, IRON)
    disc(a, 8, 8, 4.4, GLOW if lit else (12, 14, 22))
    if lit:
        disc(a, 8, 8, 2.6, GLOW_HOT)
    else:
        px(a, 6, 6, LENS_DK)
        px(a, 7, 6, (40, 52, 70))
    for x in (6, 8, 10):                       # the grating bars
        for y in range(4, 13):
            if (x - 8) ** 2 + (y - 8) ** 2 <= 20:
                px(a, x, y, IRON_DK if not lit else BRASS_DK)
    for y in (6, 10):
        for x in range(4, 13):
            if (x - 8) ** 2 + (y - 8) ** 2 <= 20:
                px(a, x, y, IRON_DK if not lit else BRASS_DK)
    for (x, y) in ((4, 4), (11, 4), (4, 11), (11, 11)):   # rivets
        px(a, x, y, IRON_LT)
    px(a, 6, 3, IRON_LT)
    outline(a)
    if lit:  # a soft halo spilling onto the wall
        for y in range(16):
            for x in range(16):
                d = math.hypot(x + 0.5 - 8, y + 0.5 - 8)
                if 6.8 < d < 8.2 and a[y, x, 3] == 0:
                    blend(a, x, y, GLOW, 90)
    save(a, "well_lit" if lit else "well")


# ---- the glare across a doorway ---------------------------------------------------------
def glare(axis: str):
    """A sheet of light crossing the gap: bright core lines, a soft veil, motes.
    Seamless along its own axis so a two-tile doorway reads as one shaft."""
    a = clear()
    for i in range(16):          # along the travel of the light
        for j in range(16):      # across the sheet
            d = abs(j + 0.5 - 8)
            if d < 1.2:
                col, al = GLOW_HOT, 235
            elif d < 2.6:
                col, al = GLOW_HOT, 175
            elif d < 4.6:
                col, al = GLOW, 120
            elif d < 7.0:
                col, al = GLOW, 55
            else:
                col, al = GLOW_DK, 22
            x, y = (i, j) if axis == "h" else (j, i)
            px(a, x, y, col, al)
    # dust motes caught in it (fixed layout, tiles seamlessly along the axis)
    for (i, j) in ((2, 4), (6, 11), (10, 3), (13, 12), (4, 9), (12, 7)):
        x, y = (i, j) if axis == "h" else (j, i)
        px(a, x, y, (255, 255, 240), 220)
    save(a, f"glare_{axis}")


# ---- the shutter-crank -------------------------------------------------------------------
def crank(thrown: bool):
    a = clear(1, 2)
    # the bracket plate on the wall face (top tile)
    rect(a, 3, 1, 12, 14, IRON_DK)
    rect(a, 4, 2, 11, 13, IRON)
    # the wheel
    disc(a, 8, 8, 5.4, IRON_DK)
    disc(a, 8, 8, 4.4, BRASS_DK)
    disc(a, 8, 8, 3.4, (0, 0, 0), 0)
    for y in range(16):
        for x in range(16):
            if (x + 0.5 - 8) ** 2 + (y + 0.5 - 8) ** 2 <= 3.4 ** 2:
                px(a, x, y, IRON)
    ang0 = math.pi / 4 if thrown else 0.0
    for k in range(4):           # four spokes
        th = ang0 + k * math.pi / 2
        for r in range(0, 5):
            px(a, int(round(8 + r * math.cos(th) - 0.5)), int(round(8 + r * math.sin(th) - 0.5)), BRASS_LT)
    disc(a, 8, 8, 1.2, BRASS)
    # the handle knob on the rim
    th = ang0 + math.pi * 0.25
    hx, hy = int(round(8 + 4.6 * math.cos(th))), int(round(8 + 4.6 * math.sin(th)))
    rect(a, hx - 1, hy - 1, hx, hy, WOOD_LT)
    # the housing on the floor (bottom tile): an iron box, chain running up
    rect(a, 4, 18, 11, 29, IRON_DK)
    rect(a, 5, 19, 10, 28, IRON)
    rect(a, 5, 19, 10, 19, IRON_LT)
    for y in range(14, 19):
        px(a, 7, y, IRON_LT if y % 2 else IRON_DK)
        px(a, 8, y, IRON_DK if y % 2 else IRON_LT)
    # the louvre tell: a little pennant on the housing (white at rest, red thrown)
    rect(a, 12, 18, 12, 27, IRON_DK)
    flag = RED if thrown else WHITE
    for y in range(18, 22):
        for x in range(13, 13 + (22 - y)):
            px(a, x, y, flag)
    rect(a, 4, 30, 11, 30, (0, 0, 0), 90)   # contact shadow
    outline(a)
    save(a, "crank_on" if thrown else "crank")


# ---- the great lamp -----------------------------------------------------------------------
def great_lamp(lit: bool):
    """4x4: a plinth with a gallery rail, the octagonal lamp-house above. Shut:
    iron shutters bolted round the lens, a thread of light at the seams. Lit:
    the shutters folded back like wings, the lens blazing."""
    a = clear(4, 4)
    W = 64
    # plinth (bottom 1.5 tiles)
    rect(a, 8, 44, 55, 61, STONE_DK)
    rect(a, 9, 45, 54, 60, STONE)
    for x in range(10, 54, 8):
        rect(a, x, 46, x, 59, STONE_DK)
    rect(a, 9, 45, 54, 46, STONE_LT)
    # gallery rail
    rect(a, 4, 38, 59, 43, IRON_DK)
    rect(a, 5, 39, 58, 42, IRON)
    rect(a, 5, 39, 58, 39, IRON_LT)
    for x in range(6, 58, 4):
        rect(a, x, 32, x, 38, IRON_DK)
    rect(a, 5, 31, 58, 32, IRON)
    # the lamp-house
    body = (14, 8, 49, 36)
    if lit:
        rect(a, body[0], body[1], body[2], body[3], GLOW)
        for y in range(body[1], body[3] + 1):
            for x in range(body[0], body[2] + 1):
                d = math.hypot(x - 31.5, y - 22)
                if d < 9:
                    px(a, x, y, GLOW_HOT)
                elif d < 13:
                    px(a, x, y, (255, 236, 176))
        for x in (20, 26, 37, 43):                       # glazing bars (brass)
            rect(a, x, body[1], x, body[3], BRASS_DK)
        rect(a, body[0], 21, body[2], 21, BRASS_DK)
        # lens rings
        for r in (5, 8):
            for k in range(48):
                t = k / 48 * 2 * math.pi
                px(a, int(31.5 + r * math.cos(t)), int(22 + r * math.sin(t)), (255, 255, 255))
        # the shutters folded open like wings
        for side in (-1, 1):
            x0 = body[0] - 7 if side < 0 else body[2] + 2
            rect(a, x0, body[1] + 2, x0 + 5, body[3] - 2, IRON_DK)
            rect(a, x0 + 1, body[1] + 3, x0 + 4, body[3] - 3, IRON)
            for y in range(body[1] + 5, body[3] - 3, 4):
                rect(a, x0 + 1, y, x0 + 4, y, IRON_LT)
        # rays
        for (dx, dy) in ((-1, -1), (1, -1), (-1, 0.4), (1, 0.4)):
            for r in range(22, 31):
                x = int(31.5 + dx * r)
                y = int(22 + dy * r * 0.55)
                if a[y, x, 3] == 0 if 0 <= y < 64 and 0 <= x < 64 else False:
                    px(a, x, y, GLOW, 150)
    else:
        rect(a, body[0], body[1], body[2], body[3], IRON_DK)
        # the shutters: six iron leaves with louvre slats
        for i, x0 in enumerate(range(body[0] + 1, body[2], 6)):
            rect(a, x0, body[1] + 1, x0 + 4, body[3] - 1, IRON if i % 2 else (72, 78, 94))
            for y in range(body[1] + 3, body[3] - 1, 3):
                rect(a, x0, y, x0 + 4, y, IRON_DK)
                rect(a, x0, y - 1, x0 + 4, y - 1, IRON_LT)
        # bolts + the cross-bar
        rect(a, body[0], 21, body[2], 22, RUST)
        rect(a, body[0], 21, body[2], 21, (160, 104, 72))
        for x in (16, 31, 47):
            rect(a, x, 20, x + 1, 23, IRON_LT)
        # a thread of banked light at the seams (the lamp is low, never out)
        for x in (19, 25, 31, 37, 43):
            for y in range(body[1] + 2, body[3] - 1):
                if y % 4 != 0:
                    px(a, x, y, (150, 110, 60))
        px(a, 31, 22, GLOW_DK)
    # the roof
    for y in range(0, 9):
        half = 6 + y * 2
        rect(a, 32 - half, y, 31 + half, y, IRON_DK if y in (0, 8) else (BRASS_DK if lit else IRON))
    rect(a, 30, 0, 33, 2, BRASS if lit else IRON_LT)
    rect(a, body[0] - 2, 8, body[2] + 2, 8, IRON_DK)
    rect(a, 8, 62, 55, 63, (0, 0, 0), 80)
    outline(a)
    save(a, "great_lamp_lit" if lit else "great_lamp")


def cot():
    """A narrow iron cot seen from above: a thin iron rail round a grey blanket,
    a dented pillow, brass knobs on the four posts."""
    a = clear(1, 2)
    rect(a, 2, 2, 13, 29, IRON_DK)            # the rail (1px frame)
    rect(a, 3, 3, 12, 28, WOOL)               # mattress under the blanket
    rect(a, 4, 4, 11, 9, (204, 202, 194))     # pillow
    rect(a, 5, 5, 10, 5, (226, 224, 216))
    rect(a, 4, 9, 11, 9, (160, 158, 152))
    rect(a, 3, 11, 12, 28, WOOL)              # the blanket, turned down
    rect(a, 3, 11, 12, 12, WOOL_LT)
    for y in (17, 23):
        rect(a, 3, y, 12, y, WOOL_DK)
    rect(a, 3, 27, 12, 28, WOOL_DK)
    for (x, y) in ((2, 2), (13, 2), (2, 29), (13, 29)):   # post knobs
        rect(a, x - 1, y - 1, x, y, BRASS)
    rect(a, 3, 30, 12, 30, (0, 0, 0), 80)     # floor shadow
    outline(a)
    save(a, "cot")


def pane(lit: bool):
    """A storm-pane of the lantern's glazing, hung on the wall face (1x1):
    dark sea-glass with a salt bloom; lit = the dawn coming through it."""
    a = clear()
    rect(a, 1, 1, 14, 14, IRON_DK)
    rect(a, 2, 2, 13, 13, (196, 214, 226) if lit else (30, 42, 60))
    if lit:
        rect(a, 2, 9, 13, 13, (236, 200, 150))
        rect(a, 2, 11, 13, 13, (250, 222, 170))
    else:
        for (x, y) in ((4, 4), (5, 5), (10, 3), (11, 4), (12, 5)):
            px(a, x, y, (64, 90, 112))
        for (x, y) in ((3, 12), (4, 11), (6, 12), (12, 12), (11, 11)):
            px(a, x, y, (150, 160, 166))                # the salt bloom
    rect(a, 7, 2, 8, 13, IRON)                          # glazing bars
    rect(a, 2, 7, 13, 8, IRON)
    px(a, 4, 3, (255, 255, 255) if lit else (120, 150, 170))
    outline(a)
    save(a, "pane_lit" if lit else "pane")


def slate():
    a = clear(2, 1)
    rect(a, 1, 2, 30, 14, WOOD_DK)
    rect(a, 2, 3, 29, 13, SLATE)
    # rows of chalk names: short strokes, deliberately unreadable at 1x
    rows = ((4, (3, 9, 11, 16, 18, 25)), (7, (3, 7, 9, 17, 19, 27)), (10, (3, 12, 14, 20, 22, 26)))
    for (y, xs) in rows:
        for k in range(0, len(xs), 2):
            rect(a, xs[k], y, xs[k + 1], y, CHALK)
    for (x, y) in ((27, 5), (6, 12)):
        px(a, x, y, CHALK)
    rect(a, 15, 0, 16, 2, IRON_LT)          # the nail + string
    outline(a)
    save(a, "slate")


def shutter_plate():
    a = clear()
    rect(a, 2, 1, 13, 14, IRON_DK)
    rect(a, 3, 2, 12, 13, IRON)
    for y in range(4, 13, 3):
        rect(a, 3, y, 12, y, IRON_DK)
        rect(a, 3, y - 1, 12, y - 1, IRON_LT)
    rect(a, 5, 6, 10, 9, (222, 214, 190))   # the neat paper label
    rect(a, 6, 7, 9, 7, INK)
    rect(a, 6, 8, 8, 8, INK)
    outline(a)
    save(a, "shutter_plate")


def lens_spare():
    a = clear(2, 2)
    rect(a, 3, 24, 28, 29, WOOD_DK)          # cradle
    rect(a, 4, 25, 27, 28, WOOD)
    rect(a, 4, 25, 27, 25, WOOD_LT)
    rect(a, 6, 29, 7, 31, WOOD_DK)
    rect(a, 24, 29, 25, 31, WOOD_DK)
    disc(a, 16, 13, 11.5, BRASS_DK)
    disc(a, 16, 13, 10.5, LENS_DK)
    for r, col in ((9.0, LENS), (6.5, LENS_DK), (5.0, LENS), (2.5, LENS_LT)):
        disc(a, 16, 13, r, col)
    for k in range(10):                      # the stepped prism rings
        t = k / 10 * 2 * math.pi
        px(a, int(16 + 8 * math.cos(t)), int(13 + 8 * math.sin(t)), LENS_LT)
    px(a, 12, 8, (240, 250, 252))
    px(a, 13, 8, (240, 250, 252))
    outline(a)
    save(a, "lens_spare")


def lighthouse_lit():
    src = Image.open(REPO / "public/assets/sprites/objects/coldfog_lighthouse.webp").convert("RGBA")
    a = np.asarray(src).astype(np.int16).copy()
    h, w = a.shape[:2]
    # the lamp room's dark panes (the navy block near the top) -> warm glass
    for y in range(4, 26):
        for x in range(10, 54):
            r, g, b, al = a[y, x]
            if al > 0 and b > r and r < 70 and g < 80:     # the dark glazing
                d = math.hypot(x - 31.5, y - 15)
                a[y, x, :3] = GLOW_HOT if d < 5 else (GLOW if d < 11 else GLOW_DK)
    # beams sweeping out either side of the lamp room: a widening wedge from the
    # glass to the sprite's edge, fading as it goes
    rows = [y for y in range(4, 26) if a[y, 31, 3] > 0 and tuple(a[y, 31, :3]) in (GLOW, GLOW_HOT, GLOW_DK)]
    cy = (min(rows) + max(rows)) / 2 if rows else 15
    for side in (-1, 1):
        for x in range(w):
            dx = (x - 31.5) * side
            if dx < 12:
                continue
            spread = 2 + (dx - 12) * 0.28
            for y in range(int(cy - spread), int(cy + spread) + 1):
                if 0 <= y < h and a[y, x, 3] < 40:
                    core = abs(y - cy) < spread * 0.35
                    a[y, x, :3] = GLOW_HOT if core else GLOW
                    a[y, x, 3] = int(max(24, (170 if core else 110) - (dx - 12) * 6))
    save(a, "lighthouse_lit")


def main():
    for name, fn in SET_SPECS.items():
        build_set(name, fn)
    well(False)
    well(True)
    glare("h")
    glare("v")
    crank(False)
    crank(True)
    great_lamp(False)
    great_lamp(True)
    cot()
    pane(False)
    pane(True)
    slate()
    shutter_plate()
    lens_spare()
    lighthouse_lit()


if __name__ == "__main__":
    main()
