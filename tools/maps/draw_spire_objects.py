#!/usr/bin/env python3
"""
draw_spire_objects — the C2 UMBRAL SPIRE drawn object kit (the climax
register: the penumbra palette carried indoors — void-black basalt, the cold
violet rim, the Crown's pale starlight falling through the open shafts. ZERO
humour — the darkest place in the game under the greatest light).

Everything is drawn in code in the cartridge register of gbaforge/
interiorforge (flat anchors, 1px ink lines, placed motifs), like the C1
penumbra kit it extends: code draws bells, basins and light better and more
null-consistently than image-gen, and these pieces must sit on the drawn
basalt ground without ringing.

Pieces:
  great_null        8x6  THE HERO — the coldfog null_engine's terrible elder:
                         a vast bell of held dark on an angular basalt cradle,
                         its mouth tilted UP at the sky (trained on the
                         Keystar). Drawn SAD, not evil: the metal is swept and
                         tended, the gauge at its foot is polished and rests
                         at zero, thin anti-light wisps rise from the mouth.
                         The horror is the care (the Stillworks read, scaled).
  null_pool         2x2  a null-lantern pool: where the anti-light leaks and
                         settles — a basalt-rimmed basin of pure held dark
                         (the starwell basin's inverse), a faint violet sheen
                         the only thing moving in it. Solid dressing.
  crownshaft        3x3  the open-shaft skylight: a column of the completing
                         Skyweave Crown's pale light falling through the dead
                         mountain onto the floor — a soft star-lit pool decal
                         (non-solid, walk-on; the look-up moments stand here).
  keystar_dais      3x2  the Keylumen set-piece anchor: a low star-etched
                         basalt dais before the Great Null, its centre socket
                         holding the one waiting glimmer at the summit.
  sleeper_*         2x2  the drained kin asleep in the null-works' alcoves —
                         the hushfrost numbed_kin precedent: REAL packed kin
                         overworld masters desaturated into the grey register
                         (grief dressing, never battles). Three Dark-register
                         kin whose drained forms ARE the Hollowing's roster:
                           #137 Nullmoth, #141 Cindersob, #138 Voidmantle.
                         Each ships a `_awake` twin (the original warm art,
                         untouched) for the postgame flag:dawn data flip —
                         same footprint, same solidity (the hushfrost pattern).

Writes  assets/tilesets/spire/objects/*.png -> spire_<stem> keys.
Then run .claude/skills/generate-sprite-sheet/scripts/pack_objects.py.

Run:  ./venv/bin/python tools/maps/draw_spire_objects.py
"""
from __future__ import annotations

import numpy as np
from pathlib import Path
from PIL import Image

from interiorforge import canvas, contact_shadow, fill, hx, img, outline

REPO = Path(__file__).resolve().parents[2]
SPIRE = REPO / "assets" / "tilesets" / "spire" / "objects"
CREATURES = REPO / "assets" / "creatures"

# ---- the C1/C2 register (void-black basalt + cold violet + pale Crown-light) -------
INKV = hx("#07080e")                                   # void-black
BASALT = [hx("#0c0e16"), hx("#161a26"), hx("#232838"), hx("#303852")]
VIOLET = [hx("#3a3658"), hx("#4a4470"), hx("#5d5490")]  # the cold rim light
BONE = [hx("#5a5660"), hx("#8c8694"), hx("#b8b2ba"), hx("#dcd6d2")]
POOL = [hx("#1f2a4a"), hx("#41548a"), hx("#9ec8f0"), hx("#dcecff"), hx("#fffdf2")]
STARPALE = (207, 232, 255)
STARDIM = (140, 170, 214)

# the sleeping-grey ramp (the numbed register: cool grey, faintly violet)
SLEEP_DARK = (16, 18, 30)
SLEEP_PALE = (148, 144, 162)


def great_null() -> Image.Image:
    """8x6 the Great Null — a vast bell of held dark trained on the sky.
    Read order: angular cradle shoulders -> the bell's black dome with one
    cold violet rim -> the upturned mouth and its rising wisps -> the tended
    foot (polished gauge at zero, swept arcs). Sad, careful, terrible."""
    a = canvas(8, 6)
    W, H = 128, 96
    cx = 64

    # ---- the cradle: two angular basalt pylons + the yoke beam ----------------
    for (px0, px1) in ((10, 30), (97, 117)):
        fill(a, px0, 34, px1, 88, BASALT[1])
        outline(a, px0, 34, px1, 88, INKV)
        a[34, px0 + 1:px1] = BASALT[3]                  # lit cap course
        a[58, px0 + 1:px1] = BASALT[0]                  # a course line
        a[74, px0 + 1:px1] = BASALT[0]
    # the yoke beam carrying the bell
    fill(a, 14, 46, 113, 52, BASALT[2])
    outline(a, 14, 46, 113, 52, INKV)
    a[47, 15:113] = BASALT[3]

    # ---- the bell: a great dark dome, mouth tilted up-back --------------------
    bcx, bcy, brx, bry = cx, 44, 40, 34
    for y in range(H):
        for x in range(W):
            dx, dy = (x - bcx) / brx, (y - bcy) / bry
            if dx * dx + dy * dy <= 1.0:
                a[y, x] = (*BASALT[0][:3], 255)
    # the mouth: an upturned ellipse of deeper dark near the crown
    for y in range(H):
        for x in range(W):
            dx, dy = (x - bcx) / 26.0, (y - 16) / 7.0
            if dx * dx + dy * dy <= 1.0:
                a[y, x] = (*INKV[:3], 255)
    # the mouth's inner lip — the one cold rim the dark allows
    for x in range(bcx - 26, bcx + 26):
        dy = 7.0 * (1 - ((x - bcx) / 26.0) ** 2) ** 0.5
        y = int(16 + dy)
        if a[y, x, 3]:
            a[y, x] = (*VIOLET[1][:3], 255)
    # the bell's east rim light + west ink edge (the penumbra convention)
    for y in range(H):
        xs = [x for x in range(W) if a[y, x, 3] and
              ((x - bcx) / brx) ** 2 + ((y - bcy) / bry) ** 2 <= 1.0]
        if xs:
            a[y, max(xs)] = (*VIOLET[1][:3], 255)
            a[y, min(xs)] = (*INKV[:3], 255)
    # faint banding on the bell — drawn structure, not noise
    for by in (36, 52, 66):
        for x in range(W):
            dx = (x - bcx) / (brx - 3)
            dy = (by - bcy) / (bry - 3)
            if dx * dx + dy * dy <= 1.0 and a[by, x, 3]:
                a[by, x] = (*BASALT[1][:3], 255)
    # three thin anti-light wisps rising from the mouth (held dark, leaking up)
    for (wx, h0) in ((bcx - 14, 12), (bcx + 2, 9), (bcx + 16, 13)):
        for y in range(h0):
            yy = 14 - y
            if 0 <= yy < H and a[yy, wx, 3] == 0:
                al = max(40, 130 - y * 9)
                a[yy, wx] = np.array([*VIOLET[0][:3], al], np.int16)

    # ---- the tended foot -------------------------------------------------------
    fill(a, 30, 80, 97, 92, BASALT[1])
    outline(a, 30, 80, 97, 92, INKV)
    a[80, 31:97] = BASALT[3]
    for fx2 in (46, 64, 82):
        a[81:92, fx2] = BASALT[0]
    # the polished gauge, resting at zero (the Stillworks motif, kept dear)
    fill(a, 58, 82, 69, 90, BASALT[2])
    outline(a, 58, 82, 69, 90, INKV)
    for gx in range(60, 68):
        a[84, gx] = BONE[2]
    a[86, 60] = BONE[3]                                  # the needle, hard left: zero
    a[86, 61] = BONE[2]
    # swept arcs at the foot — someone still tends this terrible thing
    for (sy, sx0, sx1) in ((93, 36, 56), (94, 60, 84)):
        for x in range(sx0, sx1, 3):
            if a[sy, x, 3] == 0:
                a[sy, x] = np.array([*BASALT[2][:3], 140], np.int16)
    # two dead lanterns flanking the foot
    for lx in (24, 100):
        a[70:80, lx + 1] = BASALT[2]
        fill(a, lx - 1, 64, lx + 3, 70, BASALT[1])
        outline(a, lx - 1, 64, lx + 3, 70, INKV)
        a[66, lx:lx + 3] = (*INKV[:3], 255)              # dark where flame should be
    contact_shadow(a, 10, 117, 95)
    return img(a)


def null_pool() -> Image.Image:
    """2x2 a null-lantern pool — the starwell basin's inverse: a basalt rim
    holding pure settled dark, one faint violet sheen moving in it."""
    a = canvas(2, 2)
    cx, cy = 16, 14
    # the rim ring
    for y in range(32):
        for x in range(32):
            dx, dy = (x - cx) / 15.0, (y - cy) / 11.0
            if dx * dx + dy * dy <= 1.0:
                a[y, x] = (*BASALT[2][:3], 255)
    # the pool of held dark
    for y in range(32):
        for x in range(32):
            dx, dy = (x - cx) / 12.0, (y - cy) / 8.5
            if dx * dx + dy * dy <= 1.0:
                a[y, x] = (*INKV[:3], 255)
    # north inner lip lit bone-grey; outer ink edge
    for x in range(32):
        for y in range(32):
            dx, dy = (x - cx) / 15.0, (y - cy) / 11.0
            r = dx * dx + dy * dy
            if 0.80 <= r <= 1.0 and y < cy:
                a[y, x] = (*BASALT[3][:3], 255)
    for y in range(32):
        for x in range(32):
            if a[y, x, 3] and (x == 0 or y == 0 or not a[y, max(0, x - 1), 3]
                               or not a[y, min(31, x + 1), 3]
                               or not a[max(0, y - 1), x, 3]):
                a[y, x] = (*INKV[:3], 255)
    # the one violet sheen — the only thing moving in it
    a[13, 12:16] = (*VIOLET[1][:3], 255)
    a[16, 18:21] = (*VIOLET[0][:3], 255)
    # the front face courses
    fill(a, 6, 24, 25, 29, BASALT[1])
    outline(a, 6, 24, 25, 29, INKV)
    a[24, 7:25] = BASALT[0]
    contact_shadow(a, 6, 25, 30)
    return img(a)


def crownshaft() -> Image.Image:
    """3x3 the Crown-light shaft decal: the completing Skyweave falling
    through an open shaft — a pale pooled light with a soft rising column.
    Non-solid, walk-on (the look-up moments stand in it)."""
    a = np.zeros((48, 48, 4), dtype=np.uint8)
    cx, cy = 24, 34
    # the floor pool, radially banded alpha (drawn, not noisy)
    for y in range(48):
        for x in range(48):
            dx, dy = (x - cx) / 19.0, (y - cy) / 10.0
            r = dx * dx + dy * dy
            if r <= 1.0:
                al = 92 if r <= 0.30 else 62 if r <= 0.65 else 34
                a[y, x] = (*STARPALE, al)
    # the falling column (very soft, two alpha steps, narrowing upward)
    for y in range(0, 34):
        half = 6 + int(5 * (y / 34.0))
        for x in range(cx - half, cx + half + 1):
            al = 26 if abs(x - cx) < half - 3 else 14
            if a[y, x, 3] < al:
                a[y, x] = (*STARPALE, al)
    # star-points in the pool
    for (sx, sy, al) in ((20, 31, 230), (29, 36, 210), (24, 39, 190), (33, 31, 170)):
        a[sy, sx] = (*STARPALE, al)
        for (ddx, ddy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            a[sy + ddy, sx + ddx] = (*STARDIM, 90)
    return Image.fromarray(a, "RGBA")


def keystar_dais() -> Image.Image:
    """3x2 the Keystar dais — a low star-etched basalt step before the Great
    Null; the socket at its heart holds the one waiting glimmer."""
    a = canvas(3, 2)
    # the top slab
    fill(a, 2, 4, 45, 18, BASALT[2])
    outline(a, 2, 4, 45, 18, INKV)
    a[5, 3:45] = BASALT[3]
    # the etched eight-point star (bone inlay)
    scx, scy = 24, 11
    for d in range(1, 7):
        for (dx, dy) in ((d, 0), (-d, 0), (0, d), (0, -d)):
            y, x = scy + dy, scx + dx
            if 5 <= y <= 17:
                a[y, x] = (*BONE[1][:3], 255)
    for d in range(1, 4):
        for (dx, dy) in ((d, d), (-d, d), (d, -d), (-d, -d)):
            a[scy + dy, scx + dx] = (*BONE[0][:3], 255)
    # the socket + the waiting glimmer
    fill(a, 22, 9, 26, 13, INKV)
    a[11, 24] = (*POOL[4][:3], 255)
    a[10, 24] = (*POOL[2][:3], 200)
    a[12, 24] = (*POOL[2][:3], 200)
    # the front face
    fill(a, 2, 19, 45, 28, BASALT[1])
    outline(a, 2, 19, 45, 28, INKV)
    a[19, 3:45] = BONE[0]
    for fx in (13, 24, 35):
        a[20:28, fx] = BASALT[0]
    contact_shadow(a, 2, 45, 29)
    return img(a)


def sleeper(slug: str) -> tuple[Image.Image, Image.Image]:
    """The numbed precedent: a real packed kin's overworld master desaturated
    into the sleeping-grey register (+ the untouched original as its
    postgame `_awake` twin). Returns (sleeping, awake)."""
    src = Image.open(CREATURES / slug / "overworld.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    lum = (0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]) / 255.0
    lum = lum ** 1.15                                    # settle the highlights
    out = arr.copy()
    for c in range(3):
        out[..., c] = SLEEP_DARK[c] + (SLEEP_PALE[c] - SLEEP_DARK[c]) * lum
    out[..., 3] = arr[..., 3]
    sleeping = Image.fromarray(out.astype(np.uint8), "RGBA")
    return sleeping, src


def main() -> None:
    SPIRE.mkdir(parents=True, exist_ok=True)
    out: list[tuple[Path, Image.Image]] = [
        (SPIRE / "great_null.png", great_null()),
        (SPIRE / "null_pool.png", null_pool()),
        (SPIRE / "crownshaft.png", crownshaft()),
        (SPIRE / "keystar_dais.png", keystar_dais()),
    ]
    for slug, stem in (("137_nullmoth", "sleeper_nullmoth"),
                       ("141_cindersob", "sleeper_cindersob"),
                       ("138_voidmantle", "sleeper_voidmantle")):
        sleeping, awake = sleeper(slug)
        out.append((SPIRE / f"{stem}.png", sleeping))
        out.append((SPIRE / f"{stem}_awake.png", awake))
    for path, im in out:
        im.save(path)
        print(f"  wrote {path.relative_to(REPO)}  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
