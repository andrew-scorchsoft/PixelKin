#!/usr/bin/env python3
"""
drownlightforge — THE DROWNLIGHT's drawn kit (walkthrough/11-the-hollowing-country.md
Part B, lane N2): the first lamp the Hollowing put out, climbed in the dark.

Two outputs, both deterministic (re-run freely):

1. THREE COLD INTERIOR SETS (the Old Light pattern, build_oldlight_sets.py): pixel
   transforms of `interior_stone_set` with the IDENTICAL tile order/count/metadata,
   so roomkit's FLOOR/FACE/band gids hold. Each floor is colder and darker than the
   one below — the tower gets quieter as you climb.

     drownlight_f1_set       The Oil Stores: OILED DEAL BOARDS (two joint layouts,
                             oil rings), a sea-green damp line on the faces
     drownlight_f2_set       The Lens Gallery: bluer, dimmer walls; PALE POLISHED
                             FLAGS on a half-tile offset, FLOOR_B with a brass star
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


def boards(t, joints, tones, stains):
    """F1's floor (fix pass B): OILED TIMBER BOARDS laid east-west — the stores were
    floored in deal so a dropped can wouldn't crack the flags. Board seams on rows
    1/5/9/13 (never on the tile's edge, so the fill wraps without a grid), one butt
    joint per board at `joints[b]`, a tone per board, dark oil rings at `stains`.
    The source's grain is kept, softened."""
    L = ols.lum(t)
    dev = (L - L.mean()) * 0.3
    o = t.copy()
    for y in range(T):
        b = ((y - 2) % T) // 4
        for x in range(T):
            col = np.array(tones[b], np.float64)
            if y % 4 == 1:
                col = col * 0.55                               # the seam between boards
            elif x == joints[b]:
                col = col * 0.74                               # a butt joint
            elif (y % 4 == 3 and (x * 5 + b * 3) % 11 < 4):
                col = col * 1.05                               # a run of grain
            elif y % 4 == 2:
                col = col * 1.08                               # the board's lit edge
            o[y, x, :3] = np.clip(col + dev[y, x], 0, 255)
    for (cx, cy, r) in stains:
        for y in range(T):
            for x in range(T):
                dx = min(abs(x - cx), T - abs(x - cx))
                dy = min(abs(y - cy), T - abs(y - cy))
                if dx * dx + dy * dy <= r * r:
                    o[y, x, :3] *= 0.84
    return o


def flags_inlaid(t, inlay: bool):
    """F2's floor (fix pass B): PALE POLISHED FLAGS, the lens-room's — 8px slabs on a
    half-tile offset (the grout crosses mid-tile, so the fill never shows a tile
    grid), every so often a little brass compass-star let in at the crossing where
    the keepers set the lens trestles."""
    L = ols.lum(t)
    dev = (L - L.mean()) * 0.22
    o = t.copy()
    slab = np.array((128, 138, 156), np.float64)
    for y in range(T):
        for x in range(T):
            col = slab * (1.0 + 0.03 * (((x // 8) + (y // 8)) % 2))
            if x == 7 or y == 7:
                col = slab * 0.66
            elif x in (8, 0) or y in (8, 0):
                col = slab * 1.07                              # the polished arris
            o[y, x, :3] = np.clip(col + dev[y, x], 0, 255)
    if inlay:
        b, bl, bd = np.array(BRASS, np.float64), np.array(BRASS_LT, np.float64), np.array(BRASS_DK, np.float64)
        for (x, y) in ((7, 4), (7, 5), (7, 9), (7, 10), (4, 7), (5, 7), (9, 7), (10, 7)):
            o[y, x, :3] = b
        for (x, y) in ((7, 3), (7, 11), (3, 7), (11, 7)):
            o[y, x, :3] = bd
        for (x, y) in ((6, 6), (8, 6), (6, 8), (8, 8)):
            o[y, x, :3] = bd
        for (x, y) in ((7, 6), (6, 7), (8, 7), (7, 8)):
            o[y, x, :3] = bl
        o[7, 7, :3] = (255, 240, 190)
    return o


def f1(src):
    """The Oil Stores: oiled deal boards underfoot; a damp line on the cold faces."""
    out = [ols.mul(ols.saturate(t, 0.55), 0.9, 0.97, 1.0, add=(0, 4, 4)) for t in src]
    tones = ((112, 96, 80), (100, 86, 72), (118, 102, 84), (106, 92, 78))
    # long boards: only every other board butts in a given tile (-1 = runs through)
    out[FLOORS[0]] = boards(src[FLOORS[0]], (3, -1, 11, -1), tones, ((10, 10, 2.2),))
    out[FLOORS[1]] = boards(src[FLOORS[1]], (-1, 6, -1, 13), tones, ((4, 4, 1.6),))
    for i in FACES + (INSET,):
        t = out[i]
        for x in range(T):  # the sea-green damp line, an uneven tide-mark low on the face
            y = 12 + (1 if (x * 7) % 5 == 0 else 0)
            t[y, x, :3] = t[y, x, :3] * 0.55 + np.array((60, 96, 88)) * 0.45
            t[y + 1, x, :3] *= 0.8
    return out


def f2(src):
    """The Lens Gallery: bluer, dimmer walls; pale polished flags underfoot (FLOOR
    plain, FLOOR_B with the brass compass-star — the builder sets the stars)."""
    out = [ols.mul(ols.saturate(t, 0.5), 0.74, 0.84, 1.0) for t in src]
    out[FLOORS[0]] = flags_inlaid(src[FLOORS[0]], False)
    out[FLOORS[1]] = flags_inlaid(src[FLOORS[1]], True)
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
    # the louvre tell (fix pass B: made BIG enough to read at 1x): a pennant on a
    # tall staff (white at rest, red thrown) AND the housing's tell-window in the
    # same colour, so the state reads whichever bit the player looks at
    rect(a, 12, 15, 12, 28, IRON_DK)
    flag = RED if thrown else WHITE
    flag_dk = (130, 36, 32) if thrown else (170, 170, 160)
    for y in range(15, 22):
        for x in range(13, 13 + max(1, 4 - abs(y - 18))):
            px(a, x, y, flag)
    for y in (20, 21):
        px(a, 13, y, flag_dk)
    rect(a, 6, 22, 9, 26, IRON_DK)
    rect(a, 7, 23, 8, 25, flag)
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


# =====================================================================================
# 3. THE LIGHTHOUSE KIT (fix pass B, 2026-10): the working gear of a keepers' tower,
#    so the floors stop reading as a house. Front projection, drawn in code.
#      cistern       2x2  a riveted oil cistern: domed top, hoop bands, a sight-glass
#                         with amber oil in it, a brass tap over a drip tray (F1)
#      oil_cans      1x1  three filler cans with long spouts (F1)
#      weights       1x3  the clockwork's weight-shaft foot: a timber chute on the wall,
#                         two chains coming down it, the cast weight at rest (F1)
#      clockwork     2x2  the turning-gear: a chain drum, a brass gear train, the
#                         governor's fan on top (F2 — it turned the lens)
#      lectern       1x2  the keeper's log-lectern: the log open on a slant (F1/F2)
#      foghorn       2x2  a brass foghorn on its bellows-box, a hand crank (F2)
#      buoy_repair   2x2  a channel buoy on its side on trestles, its lamp-cage off (F1)
#      lens_rack     2x2  a rack of prism segments, slotted like plates (F2)
#      grind_bench   2x2  the lens-grinding bench: wheel, clamp, grit pot (F2)
#      rope_coil     1x1  a coil of tarred rope (F1)
# =====================================================================================
COPPER = (150, 92, 62)
COPPER_LT = (196, 132, 92)
COPPER_DK = (96, 56, 40)
OIL = (214, 150, 54)
GLASS = (150, 196, 210)
GLASS_LT = (214, 238, 244)
ROPE = (158, 128, 84)
ROPE_DK = (104, 80, 52)
ROPE_LT = (196, 168, 116)
BUOY_RED = (178, 58, 50)
BUOY_RED_DK = (116, 36, 34)
GRIT = (176, 170, 160)


def cylinder(a, x0, y0, x1, y1, base, lt, dk):
    """A front-on vertical cylinder: a lit stripe a third in, darkening to both edges."""
    w = x1 - x0 + 1
    for x in range(x0, x1 + 1):
        u = (x - x0 + 0.5) / w
        col = lt if 0.22 < u < 0.38 else (dk if u < 0.1 or u > 0.78 else base)
        rect(a, x, y0, x, y1, col)


def ellipse(a, cx, cy, rx, ry, rgb, alpha=255):
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                px(a, x, y, rgb, alpha)


def shadow(a, x0, x1, y, alpha=90):
    rect(a, x0, y, x1, y, (0, 0, 0), alpha)


def cistern():
    a = clear(2, 2)
    cylinder(a, 5, 6, 26, 27, COPPER, COPPER_LT, COPPER_DK)
    ellipse(a, 15.5, 6, 11, 3.6, COPPER_DK)                    # the dome
    ellipse(a, 15.5, 5.6, 10, 2.8, COPPER)
    ellipse(a, 13, 4.6, 4, 1.2, COPPER_LT)
    rect(a, 14, 0, 17, 3, IRON_DK)                             # filler neck + cap
    rect(a, 15, 0, 16, 2, IRON_LT)
    for y in (11, 21):                                         # hoop bands + rivets
        rect(a, 5, y, 26, y + 1, IRON_DK)
        rect(a, 5, y, 26, y, IRON)
        for x in range(7, 26, 4):
            px(a, x, y, IRON_LT)
    rect(a, 6, 10, 8, 26, IRON_DK)                             # the sight-glass
    rect(a, 7, 11, 7, 25, (40, 34, 30))
    rect(a, 7, 17, 7, 25, OIL)
    px(a, 7, 17, (250, 214, 120))
    rect(a, 15, 14, 21, 18, (222, 214, 190))                   # the stencilled label
    rect(a, 16, 15, 20, 15, INK)
    rect(a, 16, 17, 18, 17, INK)
    rect(a, 23, 23, 28, 24, BRASS_DK)                          # the tap
    rect(a, 23, 23, 27, 23, BRASS_LT)
    rect(a, 27, 25, 28, 26, BRASS)
    rect(a, 24, 29, 30, 30, IRON_DK)                           # drip tray
    rect(a, 25, 29, 29, 29, IRON)
    px(a, 27, 28, OIL)
    shadow(a, 5, 26, 28)
    shadow(a, 4, 30, 31, 70)
    outline(a)
    save(a, "cistern")


def oil_cans():
    a = clear()
    for (x0, h, col) in ((1, 9, BRASS_DK), (6, 11, COPPER), (11, 8, IRON)):
        lt = BRASS if col == BRASS_DK else (COPPER_LT if col == COPPER else IRON_LT)
        dk = (80, 56, 30) if col == BRASS_DK else (COPPER_DK if col == COPPER else IRON_DK)
        y0 = 15 - h
        cylinder(a, x0, y0, x0 + 3, 14, col, lt, dk)
        rect(a, x0, y0, x0 + 3, y0, dk)
        rect(a, x0 + 1, y0 - 2, x0 + 2, y0 - 1, dk)            # the cap
        for k in range(3):                                     # the long spout
            px(a, x0 + 4 + k, y0 + 2 - k, dk)
    shadow(a, 1, 14, 15)
    outline(a)
    save(a, "oil_cans")


def weights():
    """1x3: the foot of the weight-shaft — a timber chute set into the wall (the top
    tile sits over the wall face), two chains, the cast weight at rest on its block."""
    a = clear(1, 3)
    rect(a, 2, 0, 13, 37, WOOD_DK)                             # the chute
    rect(a, 3, 0, 12, 37, (34, 30, 30))
    rect(a, 2, 0, 2, 37, WOOD)
    rect(a, 13, 0, 13, 37, WOOD)
    for y in (4, 16, 28):                                      # iron straps
        rect(a, 2, y, 13, y, IRON)
    for cx in (5, 10):                                         # two chains
        for y in range(0, 34):
            px(a, cx, y, IRON_LT if y % 3 == 0 else (IRON if y % 3 == 1 else IRON_DK))
    rect(a, 3, 34, 12, 41, IRON_DK)                            # the cast weight
    rect(a, 4, 35, 11, 40, IRON)
    rect(a, 4, 35, 11, 35, IRON_LT)
    rect(a, 6, 37, 9, 38, BRASS_DK)                            # its stamped plate
    rect(a, 1, 42, 14, 45, WOOD_DK)                            # the rest-block
    rect(a, 2, 42, 13, 42, WOOD_LT)
    rect(a, 2, 43, 13, 44, WOOD)
    shadow(a, 1, 14, 46)
    outline(a)
    save(a, "weights")


def gear(a, cx, cy, r, teeth, col, lt, dk):
    disc(a, cx, cy, r + 1, dk)
    for k in range(teeth):
        th = k / teeth * 2 * math.pi
        tx, ty = cx + (r + 1.2) * math.cos(th), cy + (r + 1.2) * math.sin(th)
        rect(a, int(tx - 0.5), int(ty - 0.5), int(tx), int(ty), dk)
    disc(a, cx, cy, r, col)
    disc(a, cx - 0.6, cy - 0.6, r * 0.55, lt)
    disc(a, cx, cy, r * 0.3, dk)


def clockwork():
    a = clear(2, 2)
    rect(a, 3, 8, 28, 28, IRON_DK)                             # the frame
    rect(a, 4, 9, 27, 27, (52, 56, 70))
    rect(a, 4, 9, 27, 9, IRON_LT)
    for x in (4, 27):
        rect(a, x, 9, x, 29, IRON)
    cylinder(a, 6, 17, 17, 25, WOOD, WOOD_LT, WOOD_DK)          # the chain drum
    for y in range(17, 26, 2):
        rect(a, 6, y, 17, y, IRON)                             # chain wound round it
    for y in range(26, 31):
        px(a, 9, y, IRON_LT if y % 2 else IRON_DK)              # chain running down
    gear(a, 21.5, 20.5, 4.2, 10, BRASS, BRASS_LT, BRASS_DK)     # the gear train
    gear(a, 14.5, 12.5, 3.0, 8, BRASS, BRASS_LT, BRASS_DK)
    rect(a, 15, 2, 16, 8, IRON)                                # the governor
    rect(a, 9, 3, 14, 4, IRON_LT)                              # its fan vanes
    rect(a, 17, 3, 22, 4, IRON_LT)
    rect(a, 9, 5, 14, 5, IRON_DK)
    rect(a, 17, 5, 22, 5, IRON_DK)
    disc(a, 15.5, 2, 1.4, BRASS)
    rect(a, 2, 29, 29, 30, IRON_DK)                            # the plinth
    rect(a, 3, 29, 28, 29, IRON)
    shadow(a, 2, 29, 31)
    outline(a)
    save(a, "clockwork")


def lectern():
    a = clear(1, 2)
    rect(a, 6, 16, 9, 28, WOOD_DK)                             # post
    rect(a, 7, 16, 8, 28, WOOD)
    rect(a, 3, 28, 12, 30, WOOD_DK)                            # foot
    rect(a, 4, 28, 11, 28, WOOD_LT)
    for y in range(6, 16):                                     # the slant top
        rect(a, 1, y, 14, y, WOOD_DK if y in (6, 15) else WOOD)
    rect(a, 2, 4, 7, 12, (236, 230, 210))                      # the open log
    rect(a, 8, 4, 13, 12, (224, 218, 196))
    rect(a, 7, 4, 8, 12, (170, 160, 140))
    for y in (6, 8, 10):
        rect(a, 3, y, 6, y, (110, 104, 96))
        rect(a, 9, y, 12, y, (110, 104, 96))
    rect(a, 3, 13, 12, 13, (150, 40, 40))                      # the ribbon
    rect(a, 12, 1, 13, 3, BRASS)                               # a pen in its well
    px(a, 13, 0, INK)
    shadow(a, 3, 12, 31)
    outline(a)
    save(a, "lectern")


def foghorn():
    a = clear(2, 2)
    rect(a, 3, 18, 22, 28, IRON_DK)                            # the bellows-box
    rect(a, 4, 19, 21, 27, IRON)
    rect(a, 4, 19, 21, 19, IRON_LT)
    for x in range(6, 21, 4):
        px(a, x, 23, IRON_LT)
    for y in range(20, 27, 2):                                 # leather pleats
        rect(a, 23, y, 26, y, WOOD_DK)
        rect(a, 23, y + 1, 26, y + 1, WOOD)
    disc(a, 8, 23, 2.2, BRASS_DK)                              # the hand-crank
    rect(a, 8, 23, 12, 23, IRON_LT)
    rect(a, 12, 21, 13, 23, WOOD_LT)
    # the horn: a brass flare rising up and right from the box
    for i in range(0, 15):
        cx = 13 + i * 0.95
        cy = 17 - i * 0.75
        r = 1.4 + (i / 14) ** 2.2 * 6.2
        disc(a, cx, cy, r, BRASS_DK)
        disc(a, cx - 0.4, cy - 0.5, max(r - 1, 0.6), BRASS)
    disc(a, 26.2, 6.6, 6.2, BRASS_DK)                          # the bell mouth
    disc(a, 26.2, 6.6, 5.0, (60, 44, 24))
    disc(a, 26.2, 6.6, 3.2, (32, 24, 16))
    for k in range(12):
        th = k / 12 * 2 * math.pi
        px(a, int(26.2 + 5.6 * math.cos(th)), int(6.6 + 5.6 * math.sin(th)), BRASS_LT)
    rect(a, 15, 12, 17, 12, BRASS_LT)
    rect(a, 2, 29, 23, 30, WOOD_DK)                            # the skid
    rect(a, 3, 29, 22, 29, WOOD)
    shadow(a, 2, 27, 31)
    outline(a)
    save(a, "foghorn")


def buoy_repair():
    a = clear(2, 2)
    for x0 in (4, 22):                                         # the trestles
        rect(a, x0, 18, x0 + 5, 19, WOOD_LT)
        rect(a, x0, 20, x0 + 5, 20, WOOD_DK)
        for (lx, d) in ((x0, -1), (x0 + 5, 1)):
            for y in range(21, 30):
                px(a, lx + d * ((y - 21) // 4), y, WOOD_DK)
    # the buoy on its side: a red/white striped barrel, a cone end to the right
    for x in range(3, 25):
        stripe = ((x - 3) // 5) % 2
        base, dk = ((BUOY_RED, BUOY_RED_DK) if stripe == 0 else ((216, 214, 204), (150, 148, 140)))
        rect(a, x, 9, x, 18, base)
        rect(a, x, 9, x, 10, tuple(min(255, c + 30) for c in base))
        rect(a, x, 16, x, 18, dk)
    for i, x in enumerate(range(25, 30)):                      # the cone
        rect(a, x, 10 + i, x, 17 - i, BUOY_RED)
        px(a, x, 17 - i, BUOY_RED_DK)
    rect(a, 2, 11, 3, 16, IRON_DK)                             # the open hatch
    # its lamp-cage, set down beside it on the floor
    rect(a, 12, 22, 19, 29, IRON_DK)
    rect(a, 13, 23, 18, 28, (40, 44, 56))
    for x in (13, 15, 17):
        rect(a, x, 22, x, 29, IRON_LT)
    rect(a, 14, 25, 16, 27, GLOW_DK)                           # a dull spare bulb-glass
    rect(a, 15, 20, 16, 21, IRON)
    rect(a, 22, 26, 28, 26, IRON_LT)                           # a spanner on the floor
    rect(a, 21, 25, 22, 27, IRON_LT)
    shadow(a, 3, 29, 30)
    outline(a)
    save(a, "buoy_repair")


def prism(a, x0, y0, h, tint=0):
    """One curved prism segment standing on edge: a pale cyan sliver with bright ribs."""
    for y in range(h):
        bow = int(round(1.6 * math.sin(math.pi * y / max(h - 1, 1))))
        x = x0 + bow
        rect(a, x, y0 + y, x + 2, y0 + y, GLASS)
        px(a, x, y0 + y, GLASS_LT)
        if (y + tint) % 4 == 0:
            rect(a, x, y0 + y, x + 2, y0 + y, GLASS_LT)
        px(a, x + 3, y0 + y, LENS_DK)


def lens_rack():
    a = clear(2, 2)
    rect(a, 2, 24, 29, 29, WOOD_DK)                            # the base
    rect(a, 3, 24, 28, 25, WOOD_LT)
    rect(a, 3, 26, 28, 28, WOOD)
    rect(a, 2, 3, 3, 29, WOOD_DK)                              # the end posts
    rect(a, 28, 3, 29, 29, WOOD_DK)
    rect(a, 2, 3, 29, 4, WOOD)                                 # the top rail
    rect(a, 2, 3, 29, 3, WOOD_LT)
    rect(a, 4, 5, 27, 23, (36, 40, 54))                        # the dark back-board
    for y in (9, 15):
        rect(a, 4, y, 27, y, (46, 50, 66))
    for i, x in enumerate(range(5, 27, 4)):                    # six slotted prisms
        h = 17 - (i % 3) * 2
        prism(a, x, 24 - h, h, i)
        rect(a, x, 24, x + 3, 24, WOOD_DK)                     # its slot
    shadow(a, 2, 29, 30)
    outline(a)
    save(a, "lens_rack")


def grind_bench():
    a = clear(2, 2)
    rect(a, 1, 12, 30, 15, WOOD_DK)                            # the bench top
    rect(a, 2, 12, 29, 13, WOOD_LT)
    rect(a, 2, 14, 29, 14, WOOD)
    for x in (3, 27):                                          # legs
        rect(a, x, 16, x + 1, 29, WOOD_DK)
    rect(a, 3, 24, 28, 25, WOOD)                               # the stretcher
    rect(a, 12, 26, 19, 28, IRON_DK)                           # the treadle
    rect(a, 15, 16, 16, 26, IRON)                              # its rod
    disc(a, 8.5, 7.5, 6.5, STONE_DK)                           # the grinding wheel
    disc(a, 8.5, 7.5, 5.5, GRIT)
    disc(a, 8, 7, 3.2, STONE_LT)
    disc(a, 8.5, 7.5, 1.2, IRON_DK)
    rect(a, 7, 11, 10, 12, IRON)                               # its axle block
    # a lens blank in the clamp, the clamp screw, the grit pot
    rect(a, 17, 9, 25, 11, IRON_DK)
    ellipse(a, 21, 7.5, 3.6, 2.6, GLASS)
    ellipse(a, 20.4, 7, 1.8, 1.2, GLASS_LT)
    rect(a, 25, 8, 27, 8, BRASS)
    rect(a, 26, 4, 29, 11, COPPER_DK)                          # the grit pot
    rect(a, 27, 5, 28, 6, GRIT)
    shadow(a, 1, 30, 30)
    outline(a)
    save(a, "grind_bench")


def rope_coil():
    a = clear()
    for r, col in ((6.6, ROPE_DK), (5.8, ROPE), (4.4, ROPE_DK), (3.6, ROPE), (2.2, ROPE_DK), (1.4, (60, 46, 30))):
        ellipse(a, 8, 10, r, r * 0.62, col)
    for k in range(14):                                        # the lay of the strands
        th = k / 14 * 2 * math.pi
        px(a, int(8 + 5.2 * math.cos(th)), int(10 + 3.2 * math.sin(th)), ROPE_LT)
    for y in range(2, 8):                                      # the free end over the top
        px(a, 12 + (y % 2), y, ROPE)
        px(a, 13 + (y % 2), y, ROPE_DK)
    shadow(a, 2, 14, 15)
    outline(a)
    save(a, "rope_coil")


def notice():
    """1x1 wall-hung: the keepers' enamel CRANK NOTICE (clarity, fix pass B) — a cream
    plate with a little crank-wheel and the two pennants, white and red, side by side."""
    a = clear()
    rect(a, 1, 2, 14, 14, IRON_DK)
    rect(a, 2, 3, 13, 13, (226, 220, 198))
    rect(a, 2, 3, 13, 4, (36, 64, 96))                         # the enamel header band
    disc(a, 5.5, 9, 2.6, IRON_DK)                              # a crank-wheel
    disc(a, 5.5, 9, 1.4, BRASS)
    rect(a, 9, 7, 9, 12, IRON_DK)                              # two pennant staffs
    rect(a, 12, 7, 12, 12, IRON_DK)
    rect(a, 10, 7, 11, 8, WHITE)
    px(a, 10, 9, WHITE)
    rect(a, 13, 7, 13, 9, RED)
    rect(a, 7, 1, 8, 2, IRON_LT)                               # the nail
    outline(a)
    save(a, "notice")


KIT = (cistern, oil_cans, weights, clockwork, lectern, foghorn, buoy_repair, lens_rack,
       grind_bench, rope_coil, notice)


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
    for fn in KIT:
        fn()


if __name__ == "__main__":
    main()
