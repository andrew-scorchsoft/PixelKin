#!/usr/bin/env python3
"""
draw_mournfields_objects — Lane N3's drawn object kit (walkthrough/11 Parts C + D):
the MOURNING FIELDS (the fallow fields the Hollowing quieted) and the PENUMBRA
UNDERWAYS (the Hollowing's last watch, under the Ring).

Drawn in code in the cartridge register of draw_coldfog_objects / draw_spire_objects
(flat anchors, 1px ink, placed motifs), keyed to the blight/basalt grounds so the props
sit on them without ringing. THE TONE RULE (story-bible: the Hollowing is grief dressed
as mercy): everything here is TENDED. The sleeping kin are tucked in, not hurt; the
blankets are folded square; the scarecrow-lamps are hooded with care. Cute, sad, never
creepy.

Mourning Fields (assets/tilesets/mournfields/objects -> mournfields_<stem>):
  sleeper_<kin>       2x2  a field kin asleep under a grey coldfog blanket (the kin's own
                           packed overworld master, sleep-greyed, the blanket drawn over
                           it) + `_awake` twin (post-dawn: the kin in its own colours, the
                           blanket folded at its side) — same footprint and solidity.
  scarecrow_lamp      1x3  a lamp-post dressed as a scarecrow: a grey field-coat on the
                           crossbar, a lantern for a head with its hood drawn down
                           + `_lit` twin (post-dawn: the hood thrown back, the lamp warm).
  field_shrine        3x3  the field shrine: a little gabled wayside house on a stone
                           step, its candles put out in a neat row, folded blankets left
                           as offerings. Seen from the lower field long before it's reached.
  stook               1x2  a sheaf-stook of the last harvest, never brought in (grey-gold).
  blanket_stack       2x1  coldfog blankets folded square on a flat stone, ready.

Penumbra Underways (assets/tilesets/underways/objects -> underways_<stem>):
  spire_shaft         4x4  THE VIEW UP: the foot of the Umbral Spire's shaft — a round
                           pit of held dark with the Crown's pale light falling into it
                           from far above. SOLID (it is a drop, and it leads nowhere you
                           may go). A look, never a way.
  watch_lamp          1x2  the last watch's hooded lantern on a staff: a slit of light.
  watch_lamp_lit      1x2  post-dawn twin: the hood thrown back.

Run:  python3 tools/maps/draw_mournfields_objects.py
Then: python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import numpy as np
from pathlib import Path
from PIL import Image

from interiorforge import BRASS, INK, canvas, contact_shadow, fill, hx, img, outline

REPO = Path(__file__).resolve().parents[2]
FIELDS = REPO / "assets" / "tilesets" / "mournfields" / "objects"
UNDER = REPO / "assets" / "tilesets" / "underways" / "objects"
CREATURES = REPO / "assets" / "creatures"

# ---- the register (keyed to gbaforge BLIGHT (90,96,92) / BASALT) -------------------
WOOL = [hx("#3c4048"), hx("#5a606a"), hx("#7c838c"), hx("#a2a8ae")]    # coldfog blanket
WOOLHEM = hx("#8e8478")                                                # the warm-grey hem
POST = [hx("#2a2420"), hx("#4a3e34"), hx("#6c5a48"), hx("#8c7660")]    # weathered wood
STRAW = [hx("#4e4632"), hx("#76683e"), hx("#9c8a52"), hx("#bba86a")]   # grey-gold straw
COAT = [hx("#3a3028"), hx("#5a4a3a"), hx("#7a6650")]                   # patched field-coat
STONE = [hx("#3a3e44"), hx("#585e66"), hx("#7a8088"), hx("#9aa0a6")]
DARKGLASS = [hx("#10141c"), hx("#1c2430"), hx("#2c3a4a")]
IRON = [hx("#1c2026"), hx("#343a44"), hx("#4c545e"), hx("#6a7280")]
FLAME = [hx("#7a3a14"), hx("#d0782c"), hx("#ffb45a"), hx("#ffe2a0")]
BASALT = [hx("#0c0e16"), hx("#161a26"), hx("#232838"), hx("#303852")]
VIOLET = [hx("#3a3658"), hx("#4a4470"), hx("#5d5490")]
STARPALE = (207, 232, 255)
STARDIM = (140, 170, 214)
SLEEP_DARK = (22, 24, 34)
SLEEP_PALE = (150, 148, 160)

SLEEPERS = (("105_snoozlet", "snoozlet"), ("136_mothdim", "mothdim"),
            ("083_hushvole", "hushvole"), ("065_glowsip", "glowsip"))


def _kin(slug: str) -> np.ndarray:
    src = Image.open(CREATURES / slug / "overworld.png").convert("RGBA")
    if src.size != (32, 32):
        src = src.resize((32, 32), Image.NEAREST)
    return np.array(src, dtype=np.int16)


def _grey(a: np.ndarray) -> np.ndarray:
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    lum = lum ** 1.15
    out = a.copy()
    for c in range(3):
        out[..., c] = SLEEP_DARK[c] + (SLEEP_PALE[c] - SLEEP_DARK[c]) * lum
    return out


def _bbox(a: np.ndarray):
    ys, xs = np.nonzero(a[..., 3] > 40)
    return xs.min(), ys.min(), xs.max(), ys.max()


def sleeper(slug: str) -> tuple[Image.Image, Image.Image]:
    """The kin asleep, sleep-greyed, a coldfog blanket tucked over its lower half:
    the blanket HUGS the kin's own silhouette (its mask, grown a pixel), so the head
    and ears stay out on top and it reads as tucked in, never boxed. A warm-grey hem,
    soft fold lines. The awake twin: the kin in its own colours, the blanket folded."""
    kin = _kin(slug)
    a = kin.copy()
    sleeping = _grey(a)
    x0, y0, x1, y1 = _bbox(a)
    cut = y0 + int((y1 - y0 + 1) * 0.46)
    mid = (x0 + x1) / 2.0
    half = (x1 - x0) / 2.0 + 1.5
    bot = min(30, y1 + 1)
    # a soft MOUND, not a box: the top edge arcs down toward the sides
    blanket = np.zeros((32, 32), dtype=bool)
    for x in range(32):
        t = (x - mid) / half
        if abs(t) > 1.0:
            continue
        top = cut + int(round(4.0 * t * t))
        side_lift = 1 if abs(t) > 0.85 else 0
        for y in range(top, bot + 1 - side_lift):
            blanket[y, x] = True
    QUILT = [hx("#3e3a4c"), hx("#625e74"), hx("#78748c"), hx("#9c98ae")]
    STITCH = hx("#a8927c")
    for y in range(32):
        for x in range(32):
            if not blanket[y, x]:
                continue
            check = ((x // 4) + ((y - cut) // 4)) % 2
            col = QUILT[2] if check else QUILT[1]
            if not blanket[y - 1, x]:
                col = QUILT[3]                       # the lit top edge
            elif y == bot or not blanket[min(31, y + 1), x]:
                col = STITCH if x % 2 else QUILT[0]  # the stitched, scalloped hem
            elif (x - int(mid)) % 8 == 0:
                col = QUILT[0]                       # a quilting seam
            sleeping[y, x] = col
    edge = np.zeros_like(blanket)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        edge |= np.roll(np.roll(blanket, dy, 0), dx, 1)
    mask = a[..., 3] > 40
    for y in range(32):
        for x in range(32):
            if edge[y, x] and not blanket[y, x] and not (mask[y, x] and y < cut + 4):
                sleeping[y, x] = INK
    contact_shadow(sleeping, max(0, int(mid - half)), min(31, int(mid + half)), min(31, bot + 1))

    awake = a.copy()
    fy = min(29, y1 - 1)
    fill(awake, 23, fy - 2, 30, fy, QUILT[1])
    for x in range(23, 31, 4):
        awake[fy - 1, x:x + 2] = QUILT[2]
    awake[fy - 2, 23:31] = QUILT[3]
    awake[fy, 23:31] = STITCH
    outline(awake, 22, fy - 3, 31, fy + 1, INK)
    return img(sleeping), img(awake)


def scarecrow_lamp(lit: bool) -> Image.Image:
    """1x3 a lamp-post dressed as a scarecrow: the post, a crossbar with a grey
    field-coat hung on it (sleeves out along the bar, ragged hem, straw at the cuffs
    and collar), and for a head a round lantern with its wool hood drawn down — the
    Hollowing's mercy. Lit: the hood thrown back round the shoulders, the lamp warm."""
    a = canvas(1, 3)
    # the post
    fill(a, 7, 12, 8, 46, POST[1])
    a[12:47, 7] = POST[2]
    a[45:47, 5:11] = POST[0]
    # the crossbar
    a[17, 0:16] = POST[3]
    a[18, 0:16] = POST[1]
    # the coat: shoulders on the bar, sleeves hanging off each end, body narrowing
    for y in range(18, 36):
        half = 4 if y < 21 else 3 + (y - 21) // 6
        x0, x1 = 7 - half, 8 + half
        a[y, x0:x1 + 1] = COAT[1]
        a[y, x0] = INK
        a[y, x1] = INK
    a[19:35, 6] = COAT[2]
    a[20:35, 7:9] = COAT[0]                             # the open front
    for y in (22, 26, 30):
        a[y, 9] = IRON[3]
    # ragged hem
    for x in range(4, 12):
        if x % 2:
            a[35, x] = COAT[1]
            a[36, x] = INK
        else:
            a[35, x] = INK
    a[35:38, 6] = STRAW[2]
    a[35:37, 10] = STRAW[1]
    # sleeves down from the crossbar ends, straw at the cuffs
    for sx in (0, 13):
        fill(a, sx, 18, sx + 2, 25, COAT[1])
        a[18:26, sx] = INK if sx == 0 else COAT[2]
        a[18:26, sx + 2] = INK if sx == 13 else COAT[2]
        a[26, sx:sx + 3] = STRAW[2]
        a[27, sx + 1] = STRAW[1]
    # straw at the collar
    a[17, 5] = STRAW[3]
    a[17, 10] = STRAW[3]
    # the lantern head (round)
    for y in range(4, 16):
        for x in range(2, 14):
            dx, dy = (x - 7.5) / 5.0, (y - 10) / 5.5
            if dx * dx + dy * dy <= 1.0:
                if lit:
                    a[y, x] = FLAME[2] if dx * dx + dy * dy > 0.35 else FLAME[3]
                else:
                    a[y, x] = WOOL[1] if dx > -0.4 else WOOL[2]
            elif dx * dx + dy * dy <= 1.35:
                a[y, x] = INK
    # a wide straw hat over the lantern (the scarecrow's)
    a[3, 1:15] = STRAW[2]
    a[4, 0:16] = STRAW[1]
    a[3, 1] = INK
    a[3, 14] = INK
    a[4, 0] = INK
    a[4, 15] = INK
    fill(a, 5, 0, 10, 2, STRAW[2])
    a[0, 5:11] = INK
    a[1:3, 5] = STRAW[3]
    a[2, 5:11] = hx("#6a5a7a")                         # the hat-band
    if lit:
        a[9:12, 6:10] = hx("#fff6dc")
        # the hood, thrown back over the shoulders
        fill(a, 3, 15, 12, 17, WOOL[1])
        a[15, 3:13] = WOOL[2]
        outline(a, 2, 14, 13, 17, INK)
        a[16, 7] = WOOL[0]
    else:
        a[8:14, 6] = WOOL[0]                           # a fold in the hood
        a[8:14, 9] = WOOL[0]
        a[14, 4:12] = WOOLHEM                          # the hem, tied
        a[15, 5:11] = FLAME[0]                         # the faintest line of glow beneath
    contact_shadow(a, 5, 10, 47)
    return img(a)


def field_shrine() -> Image.Image:
    """3x3 the field shrine: a little gabled wayside house on a stone step. Inside,
    a row of candles put out with care; at its foot, two folded blankets left as
    offerings, and a sprig of grey-gold straw tied with ribbon."""
    a = canvas(3, 3)
    # the stone step
    fill(a, 4, 36, 43, 44, STONE[1])
    a[36, 5:43] = STONE[3]
    a[37, 5:43] = STONE[2]
    for sx in (14, 26, 36):
        a[38:45, sx] = STONE[0]
    outline(a, 4, 36, 43, 44, INK)
    # the house body (posts + back wall)
    fill(a, 10, 16, 37, 35, POST[1])
    for py in range(18, 35, 4):
        a[py, 11:37] = POST[0]
    fill(a, 13, 19, 34, 33, hx("#1a1c24"))            # the niche, dark
    outline(a, 13, 19, 34, 33, INK)
    a[16:36, 10] = POST[2]
    a[16:36, 37] = POST[0]
    outline(a, 10, 16, 37, 35, INK)
    # the gable roof (grey shingle)
    for y in range(4, 18):
        half = 4 + (y - 4) * 3 // 2
        x0, x1 = max(0, 24 - half), min(47, 23 + half)
        a[y, x0:x1 + 1] = STONE[1] if (y % 3) else STONE[0]
        a[y, x0] = INK
        a[y, x1] = INK
    a[3, 22:26] = INK
    for y in range(5, 17, 3):
        a[y, 18:30] = STONE[2]
    a[17, 2:46] = INK
    a[16, 3:45] = STONE[0]
    # the ridge finial: a little iron star, unlit
    a[1:4, 23:25] = IRON[3]
    a[2, 22:26] = IRON[3]
    # the candles, put out neat (five, grey wax, a thread of wick each)
    for i, cx in enumerate((16, 20, 24, 28, 32)):
        h = 5 + (i % 2)
        fill(a, cx - 1, 32 - h, cx, 32, hx("#9c9890"))
        a[32 - h, cx - 1:cx + 1] = hx("#bcb8ae")
        a[31 - h, cx] = hx("#4a463e")
    a[33, 14:34] = BRASS[0]                            # the brass candle-board
    # the offerings at the foot: folded blankets + a tied straw sprig
    fill(a, 6, 38, 15, 42, WOOL[1])
    a[38, 6:16] = WOOL[2]
    a[40, 6:16] = WOOL[0]
    a[42, 6:16] = WOOLHEM
    outline(a, 6, 37, 15, 43, INK)
    fill(a, 33, 39, 41, 42, WOOL[2])
    a[39, 33:42] = WOOL[3]
    a[42, 33:42] = WOOLHEM
    outline(a, 33, 38, 41, 43, INK)
    for sx in range(24, 30):
        a[39:43, sx] = STRAW[2] if sx % 2 else STRAW[1]
    a[40, 23:31] = hx("#8a7aa8")                       # the ribbon
    contact_shadow(a, 4, 43, 45)
    return img(a)


def stook() -> Image.Image:
    """1x2 a stook of sheaves from the last harvest, never brought in."""
    a = canvas(1, 2)
    for y in range(4, 29):
        w = 2 + (y - 4) * 5 // 24
        x0, x1 = 8 - w, 7 + w
        for x in range(x0, x1 + 1):
            a[y, x] = STRAW[(x + y // 3) % 3 + 1] if (x - x0) % 3 else STRAW[1]
        a[y, x0] = INK
        a[y, x1] = INK
    a[3, 7:9] = INK
    a[2, 6] = STRAW[3]
    a[1, 9] = STRAW[3]
    a[2, 8] = STRAW[2]
    a[14:16, 3:13] = hx("#5a5040")                     # the binding band
    a[28, 3:13] = STRAW[0]
    a[29, 2:14] = INK
    contact_shadow(a, 2, 13, 30)
    return img(a)


def blanket_stack() -> Image.Image:
    """2x1 coldfog blankets folded square on a flat stone, ready for the night."""
    a = canvas(2, 1)
    fill(a, 2, 11, 29, 14, STONE[1])
    a[11, 2:30] = STONE[2]
    outline(a, 2, 11, 29, 14, INK)
    for i, (y0, col) in enumerate(((7, WOOL[1]), (3, WOOL[2]))):
        x0, x1 = 5 + i * 2, 26 - i * 2
        fill(a, x0, y0, x1, y0 + 3, col)
        a[y0, x0:x1 + 1] = WOOL[3] if i else WOOL[2]
        a[y0 + 3, x0:x1 + 1] = WOOLHEM
        outline(a, x0, y0, x1, y0 + 4, INK)
    contact_shadow(a, 2, 29, 15)
    return img(a)


# ---- the Underways ---------------------------------------------------------------
def spire_shaft() -> Image.Image:
    """4x4 the foot of the Umbral Spire's shaft: a round pit of held dark ringed in
    worked basalt, and the Crown's pale light falling down it from impossibly high —
    a soft column narrowing into the pit, star-points drifting in it, a faint pool of
    light far down. A look up, never a way up."""
    a = np.zeros((64, 64, 4), dtype=np.float32)
    cx, cy, rx, ry = 32, 46, 28, 14
    for y in range(64):
        for x in range(64):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            r = dx * dx + dy * dy
            if r <= 1.0:
                if r > 0.66:
                    a[y, x] = BASALT[2]
                elif r > 0.56:
                    a[y, x] = VIOLET[0]
                else:
                    t = r / 0.56                       # deeper toward the middle
                    a[y, x, :3] = np.array(BASALT[0][:3]) * (1 - t) + np.array(BASALT[1][:3]) * t
                    a[y, x, 3] = 255
            elif r <= 1.14:
                a[y, x] = INK
    for ang in range(0, 360, 24):                      # the rim's block seams
        t = np.radians(ang)
        for k in (0.84, 0.92, 1.0):
            x = int(round(cx + np.cos(t) * rx * k))
            y = int(round(cy + np.sin(t) * ry * k))
            if 0 <= x < 64 and 0 <= y < 64 and a[y, x, 3] > 0:
                a[y, x] = BASALT[1]
    for x in range(cx - 22, cx + 23):                  # the lit near lip
        dy = ry * np.sqrt(max(0.0, 1 - ((x - cx) / rx) ** 2))
        y = int(cy + dy) - 1
        a[y, x] = BASALT[3]
    # the falling light: a column whose width narrows as it falls into the pit
    sp = np.array(STARPALE, dtype=np.float32)
    for y in range(0, 54):
        half = 9 - 4 * (y / 54.0)
        for x in range(64):
            d = abs(x - cx) / half
            if d > 1.0:
                continue
            k = (0.42 if d < 0.5 else 0.22) * (1.0 if y < 40 else 1.3)
            if a[y, x, 3] > 0:
                a[y, x, :3] = sp * k + a[y, x, :3] * (1 - k)
            else:
                a[y, x] = (*sp, 255 * k * 0.9)
    for y in range(44, 52):                            # the pool far down
        for x in range(cx - 8, cx + 9):
            dx, dy = (x - cx) / 8.0, (y - 48) / 3.0
            if dx * dx + dy * dy <= 1:
                a[y, x, :3] = sp * 0.5 + a[y, x, :3] * 0.5
    for (sx, sy) in ((30, 5), (35, 12), (28, 19), (33, 27), (30, 34), (36, 41), (27, 47)):
        a[sy, sx] = (*STARPALE, 255)
        for (ddx, ddy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if a[sy + ddy, sx + ddx, 3] < 200:
                a[sy + ddy, sx + ddx] = (*STARDIM, 170)
    return img(a)


def watch_lamp(lit: bool) -> Image.Image:
    """1x2 the last watch's lantern on its staff, the hood drawn down to a slit —
    enough to see a face by, no more. Lit twin: the hood thrown back."""
    a = canvas(1, 2)
    fill(a, 7, 10, 8, 30, POST[1])
    a[10:31, 7] = POST[2]
    a[29:31, 5:11] = POST[0]
    a[9, 5:11] = IRON[2]                               # the hook arm
    fill(a, 4, 11, 11, 20, DARKGLASS[1])
    outline(a, 3, 10, 12, 21, INK)
    if lit:
        a[12:20, 5:11] = FLAME[2]
        a[14:18, 6:10] = FLAME[3]
    else:
        fill(a, 3, 8, 12, 19, WOOL[1])                 # the hood
        a[8, 4:12] = WOOL[2]
        a[19, 3:13] = WOOLHEM
        outline(a, 3, 8, 12, 19, INK)
        a[20, 5:11] = FLAME[1]                         # the slit of light
        a[21, 6:10] = FLAME[0]
    a[7, 7:9] = BRASS[2]
    contact_shadow(a, 5, 10, 31)
    return img(a)


def main() -> None:
    FIELDS.mkdir(parents=True, exist_ok=True)
    UNDER.mkdir(parents=True, exist_ok=True)
    out: list[tuple[Path, Image.Image]] = [
        (FIELDS / "scarecrow_lamp.png", scarecrow_lamp(False)),
        (FIELDS / "scarecrow_lamp_lit.png", scarecrow_lamp(True)),
        (FIELDS / "field_shrine.png", field_shrine()),
        (FIELDS / "stook.png", stook()),
        (FIELDS / "blanket_stack.png", blanket_stack()),
        (UNDER / "spire_shaft.png", spire_shaft()),
        (UNDER / "watch_lamp.png", watch_lamp(False)),
        (UNDER / "watch_lamp_lit.png", watch_lamp(True)),
    ]
    for slug, stem in SLEEPERS:
        sleeping, awake = sleeper(slug)
        out.append((FIELDS / f"sleeper_{stem}.png", sleeping))
        out.append((FIELDS / f"sleeper_{stem}_awake.png", awake))
    for path, im in out:
        im.save(path)
        print(f"  wrote {path.relative_to(REPO)}  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
