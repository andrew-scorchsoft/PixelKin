#!/usr/bin/env python3
"""
lowtinderforge — the drowned old town's props (walkthrough/10 Part III: Lowtinder &
Tinderwick Bay). Drawn in code, DERIVED from Tinderwick's own masters so the old town
reads as the same town forty years under the water (the gbaforge rule: no paid
image-gen for structural props; the derivation keeps the house style exact).

Every piece is a pure function of its source master + a crc32 seed (deterministic):

  * roof_ridge   (48x32, 3x2)  — a cottage roof-peak showing above the tide, the
                                 waterline lapping its eaves. Tinderwick's sea + the bay.
  * roof_ridge_b (64x32, 4x2)  — the store's long roof, the same way under.
  * belltower    (32x64, 2x4)  — the drowned bell-tower's belfry: the chapel-style
                                 tower top (finial = a lamp, not a cross) standing out
                                 of the sea, its bell-arch EMPTY (the bell fell).
  * sunk_cottage (80x80, 5x5)  — a Tinderwick cottage, tide-stained to the sills,
                                 weed on the walls, dark glass, moss on the slates.
  * sunk_shop    (80x64, 5x4)  — the store, the same.
  * lamphouse    (80x80, 5x5)  — Grandmother Tallow's lamp-house: tide-stained below,
                                 but the upper windows WARM and a lamp at the gable
                                 (someone lives here). Door = col 2, like the cottage.
  * lampschool   (112x64, 7x4) — the old lamp-school, drowned (the Wickstead school's
                                 elder sister): stained walls, dark windows, empty cupola.
  * bell_frame   (32x48, 2x3)  — Tinderwick square's timber bell-gallows, EMPTY.
  * bell_hung    (32x48, 2x3)  — the same frame with the old town bell home in it
                                 (same footprint: the flag-swapped pair).
  * bell_sunk    (32x32, 2x2)  — the bell lying on its lip in the belfry pit, green
                                 with forty years of sea.
  * bell_raised  (32x32, 2x2)  — the bell hauled up onto the belfry floor, dripping.
  * tinder_light (64x112, 4x7) — the old Tinder Light on the outer reef: the beacon's
                                 tower, cold, cracked lantern, barnacled to the gallery.

Writes assets/tilesets/lowtinder/objects/*.png (packed by pack_objects.py to
`lowtinder_<stem>`).

Run:  python3 tools/maps/lowtinderforge.py
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import random
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "assets" / "tilesets"
OUT = SRC / "lowtinder" / "objects"

WATER = (45, 81, 117)
WATER_HI = (70, 119, 167)
WATER_MID = (59, 101, 144)
FOAM = (168, 200, 222)
INK = (14, 18, 26)
WEED = [(38, 74, 58), (52, 96, 70), (70, 118, 82)]
STAIN = (40, 66, 64)
BARNACLE = [(150, 156, 148), (112, 118, 112)]
MOSS = [(58, 104, 74), (78, 128, 84), (44, 86, 64)]
GLASS = [(22, 30, 44), (34, 46, 64), (60, 82, 106)]
BRONZE = [(70, 52, 30), (122, 86, 42), (176, 128, 58), (222, 176, 96)]
VERDI = [(52, 104, 92), (78, 140, 118), (112, 170, 140)]
TIMBER = [(48, 32, 22), (78, 54, 36), (112, 80, 52), (142, 106, 70)]


def rng(name: str) -> random.Random:
    return random.Random(zlib.crc32(name.encode()))


def load(area: str, stem: str) -> Image.Image:
    return Image.open(SRC / area / "objects" / f"{stem}.png").convert("RGBA")


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def is_window(px) -> bool:
    r, g, b, a = px
    return a > 0 and r > 170 and g > 100 and b < 120 and r - b > 90


def darken_windows(im: Image.Image, seed: str, keep_rows: range | None = None) -> None:
    """Warm lit glass -> dark drowned glass (a faint cold reflection kept)."""
    R = rng(seed)
    px = im.load()
    for y in range(im.height):
        if keep_rows is not None and y in keep_rows:
            continue
        for x in range(im.width):
            if is_window(px[x, y]):
                v = px[x, y]
                c = GLASS[0] if v[0] < 215 else GLASS[1]
                if R.random() < 0.08:
                    c = GLASS[2]
                px[x, y] = (*c, 255)


def tide_stain(im: Image.Image, line: int, seed: str, *, weed: float = 0.07,
               barn: float = 0.03, amount: float = 0.45) -> None:
    """Everything below `line` darkens toward the drowned green (a high-water
    mark you can read: a crisp darker band at the line itself), with weed
    strands hanging from the line and barnacle specks below it."""
    R = rng(seed)
    px = im.load()
    W, H = im.size
    for y in range(max(0, line), H):
        depth = min(1.0, (y - line + 2) / 18)
        for x in range(W):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            t = amount * (0.55 + 0.45 * depth)
            if y in (line, line + 1):
                t = min(0.85, t + 0.25)          # the tide-mark itself
            c = mix((r, g, b), STAIN, t)
            if R.random() < barn * depth:
                c = R.choice(BARNACLE)
            px[x, y] = (*c, a)
    # weed strands hanging off the tide-mark
    for x in range(W):
        if R.random() < weed and px[x, min(H - 1, line)][3] > 0:
            n = R.randint(2, 6)
            col = R.choice(WEED)
            for k in range(n):
                y = line + k
                if y < H and px[x, y][3] > 0:
                    px[x, y] = (*col, 255)


def moss(im: Image.Image, y0: int, y1: int, seed: str, density: float = 0.05) -> None:
    """Moss clumps on roof slates (blue-grey pixels only), clustered."""
    R = rng(seed)
    px = im.load()
    W = im.width
    seeds = [(R.randrange(W), R.randrange(y0, y1)) for _ in range(int(W * (y1 - y0) * density / 6))]
    for (cx, cy) in seeds:
        for _ in range(R.randint(3, 8)):
            x, y = cx + R.randint(-2, 2), cy + R.randint(-1, 1)
            if 0 <= x < W and y0 <= y < y1:
                r, g, b, a = px[x, y]
                if a > 0 and b > r + 10:          # slate, not timber/plaster
                    px[x, y] = (*R.choice(MOSS), a)


def waterline(im: Image.Image, top: int, seed: str) -> Image.Image:
    """Cut the sprite at `top` (a y in the image) and lay the sea over everything
    below it: the base water colour, a broken foam lip hugging the sprite where it
    meets the water, and a couple of ripple dashes. Only pixels of the sprite are
    covered (the rest stays transparent so the map's own water shows)."""
    R = rng(seed)
    out = im.copy()
    px = out.load()
    W, H = out.size
    for y in range(top, H):
        for x in range(W):
            if px[x, y][3] == 0:
                continue
            c = WATER if (x + y) % 7 else WATER_MID
            px[x, y] = (*c, 255)
    # foam lip along the cut, only where the sprite is
    for x in range(W):
        if px[x, top][3] > 0 and im.getpixel((x, max(0, top - 1)))[3] > 0:
            if R.random() < 0.8:
                px[x, top] = (*FOAM, 255)
            if R.random() < 0.3 and top + 1 < H:
                px[x, top + 1] = (*WATER_HI, 255)
    # ripple rings below
    for k in range(3):
        y = top + 3 + k * 3
        if y >= H:
            break
        x0 = R.randrange(2, max(3, W - 10))
        for x in range(x0, min(W, x0 + R.randint(4, 9))):
            if px[x, y][3] > 0:
                px[x, y] = (*WATER_HI, 255)
    # trim the sea away from the side columns where the sprite was transparent
    # above the line (so the waterline hugs the silhouette, not a box)
    return out


def ripple_ring(out: Image.Image, top: int, x0: int, x1: int, seed: str) -> None:
    """A soft water ring round the base where the cut sprite is narrower than
    its slot — drawn on the transparent margin so the object sits IN the sea."""
    R = rng(seed + "ring")
    px = out.load()
    W, H = out.size
    for y in range(top, H):
        for x in range(max(0, x0), min(W, x1)):
            if px[x, y][3] == 0 and (y == top or R.random() < 0.15):
                if y == top:
                    px[x, y] = (*FOAM, 180)


# ---------------------------------------------------------------------------- pieces
def emerge(crop: Image.Image, line: int, seed: str, gable: int = 7) -> Image.Image:
    """A roof coming up out of the sea: below the waterline the sprite is GONE
    (the map's own animated water shows through, never a static water box), and
    toward each end the waterline climbs (the gable ends dip under), so the
    visible slates make a ridge-shaped island, not a rectangle. A broken foam
    lip hugs the silhouette where it meets the water, with a ripple below."""
    R = rng(seed)
    W, H = crop.size
    out = crop.copy()
    px = out.load()
    cut = []
    for x in range(W):
        d = min(x, W - 1 - x)
        cut.append(line - max(0, gable - d))
    for x in range(W):
        for y in range(cut[x], H):
            px[x, y] = (0, 0, 0, 0)
    for x in range(W):
        y = cut[x]
        if 0 < y < H and crop.getpixel((x, y - 1))[3] > 0:
            if R.random() < 0.85:
                px[x, y] = (*FOAM, 230)
            if y + 1 < H and R.random() < 0.5:
                px[x, y + 1] = (*WATER_HI, 170)
    for k in range(2):                                   # a ripple dash below
        y = line + 3 + 3 * k
        if y < H:
            x0 = R.randrange(4, max(5, W - 14))
            for x in range(x0, x0 + R.randint(5, 10)):
                if x < W:
                    px[x, y] = (*WATER_HI, 150)
    return out


def roof_ridge() -> Image.Image:
    """The cottage roof's top: the ridge + chimney, the sea at its upper slates."""
    src = load("tinderwick", "cottage")
    crop = src.crop((16, 0, 64, 32))            # 48x32
    moss(crop, 0, 26, "ridge_moss", 0.12)
    tide_stain(crop, 18, "ridge_t", weed=0.15, barn=0.05, amount=0.4)
    return emerge(crop, 24, "ridge")


def roof_ridge_b() -> Image.Image:
    src = load("tinderwick", "shop")
    crop = src.crop((8, 0, 72, 32))             # the store's long roof, 64x32
    moss(crop, 0, 26, "ridgeb_moss", 0.12)
    tide_stain(crop, 17, "ridgeb_t", weed=0.15, barn=0.05, amount=0.4)
    return emerge(crop, 23, "ridgeb", gable=9)


def belltower() -> Image.Image:
    """The drowned bell-tower: a square stone shaft, an open belfry arch (the bell
    long fallen — the arch is EMPTY, black), a pyramidal slate cap with a little
    iron lamp-finial (Tinderwick's towers wear lamps, not vanes)."""
    R = rng("belltower")
    im = Image.new("RGBA", (32, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    STONE = [(54, 60, 72), (78, 86, 100), (100, 110, 126), (126, 136, 152)]
    x0, x1 = 6, 25
    # shaft
    d.rectangle([x0, 22, x1, 63], fill=STONE[1])
    d.line([(x0, 22), (x0, 63)], fill=STONE[3])
    d.line([(x0 + 1, 22), (x0 + 1, 63)], fill=STONE[2])
    d.line([(x1, 22), (x1, 63)], fill=STONE[0])
    d.line([(x1 - 1, 22), (x1 - 1, 63)], fill=STONE[0])
    # coursing
    for y in range(25, 64, 4):
        d.line([(x0 + 1, y), (x1 - 1, y)], fill=STONE[0])
        off = 3 if (y // 4) % 2 else 0
        for x in range(x0 + 2 + off, x1, 6):
            d.point([(x, y + 1), (x, y + 2)], fill=STONE[0])
    # cornice under the belfry
    d.rectangle([x0 - 2, 34, x1 + 2, 36], fill=STONE[2])
    d.line([(x0 - 2, 34), (x1 + 2, 34)], fill=STONE[3])
    d.line([(x0 - 2, 36), (x1 + 2, 36)], fill=INK)
    # belfry arch (empty)
    d.rectangle([11, 22, 20, 33], fill=INK)
    d.ellipse([11, 18, 20, 27], fill=INK)
    d.line([(10, 33), (21, 33)], fill=STONE[3])
    # the bell-beam, empty hook
    d.line([(12, 24), (19, 24)], fill=TIMBER[1])
    d.line([(15, 24), (15, 27)], fill=(90, 90, 100))
    # slate cap
    d.polygon([(x0 - 3, 22), (16, 5), (x1 + 3, 22)], fill=(52, 70, 96), outline=INK)
    for k in range(3):
        y = 10 + k * 4
        d.line([(16 - (y - 5), y), (16 + (y - 5), y)], fill=(40, 54, 76))
    d.line([(x0 - 1, 21), (16, 6)], fill=(84, 108, 140))
    # lamp finial (cold)
    d.line([(16, 1), (16, 5)], fill=INK)
    d.rectangle([14, 0, 18, 3], fill=(40, 46, 58), outline=INK)
    d.point([(16, 1)], fill=(110, 130, 150))
    moss(im, 5, 22, "towermoss", 0.25)
    tide_stain(im, 38, "tower", weed=0.25, barn=0.06, amount=0.55)
    return emerge(im, 52, "towerw", gable=0)


def stained_building(area: str, stem: str, line: int, seed: str, *,
                     keep_rows: range | None = None, roof_rows: tuple[int, int]) -> Image.Image:
    im = load(area, stem)
    darken_windows(im, seed, keep_rows)
    moss(im, roof_rows[0], roof_rows[1], seed + "m", 0.09)
    tide_stain(im, line, seed, weed=0.16, barn=0.05, amount=0.55)
    return im


def sunk_cottage() -> Image.Image:
    im = stained_building("tinderwick", "cottage", 50, "sunkc", roof_rows=(0, 44))
    return emerge(im, 68, "sunkcw", gable=0)          # the door half under the tide


def sunk_shop() -> Image.Image:
    im = stained_building("tinderwick", "shop", 38, "sunks", roof_rows=(0, 36))
    return emerge(im, 54, "sunksw", gable=0)


def old_cottage() -> Image.Image:
    """A cottage on the dry rise: high-water-marked to the sills, glass dark,
    but standing on its feet (no waterline cut)."""
    return stained_building("tinderwick", "cottage", 54, "oldc", roof_rows=(0, 44))


def lamphouse() -> Image.Image:
    """Lived in: the tide-mark stops below the UPPER windows (they stay warm);
    the lower glass is dark; a lit lamp hangs at the gable."""
    im = load("tinderwick", "cottage")
    # cottage windows sit around y 56..66 — keep a warm one upstairs: we leave
    # the windows lit and only stain/darken the lowest band (below y 64)
    darken_windows(im, "lamph", keep_rows=range(0, 64))
    moss(im, 0, 44, "lamphm", 0.05)
    tide_stain(im, 66, "lamph", weed=0.08, barn=0.03, amount=0.35)
    d = ImageDraw.Draw(im)
    # a hung lamp at the gable (bracket + glowing cage), right of the door
    x, y = 60, 46
    d.line([(x, y), (x + 5, y)], fill=TIMBER[0])
    d.line([(x + 5, y), (x + 5, y + 2)], fill=TIMBER[0])
    d.rectangle([x + 3, y + 3, x + 7, y + 8], fill=(60, 40, 24))
    d.rectangle([x + 4, y + 4, x + 6, y + 7], fill=(255, 196, 96))
    d.point([(x + 5, y + 5)], fill=(255, 240, 190))
    return im


def lampschool() -> Image.Image:
    im = load("wickstead", "school")
    darken_windows(im, "lschool")
    moss(im, 0, 34, "lschoolm", 0.10)
    tide_stain(im, 38, "lschool", weed=0.12, barn=0.05, amount=0.45)
    # the cupola's bell is gone (it rang the school in; the sea took it)
    px = im.load()
    for y in range(0, 24):
        for x in range(40, 72):
            r, g, b, a = px[x, y]
            if a and r > 150 and r - b > 60:
                px[x, y] = (*INK, 255)
    return im


def _bell(size: int, palette, seed: str, *, patina: float = 0.0) -> Image.Image:
    """A town bell drawn from scratch: crown loop, waist, flared lip, clapper."""
    R = rng(seed)
    w = size
    h = size
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = im.load()
    cx = (w - 1) / 2
    top, lip = 3, h - 3
    for y in range(top, lip + 1):
        t = (y - top) / (lip - top)
        # rounded shoulder, a slight waist, then the flare at the lip
        shoulder = (1 - (1 - min(1.0, t / 0.22)) ** 2)
        half = (w * 0.30) * shoulder + (w * 0.04) * t + (w * 0.17) * (t ** 4)
        half = max(1.0, half)
        for x in range(w):
            dx = x - cx
            if abs(dx) <= half:
                edge = abs(dx) > half - 1
                shade = 0.5 + 0.5 * (-dx / max(1, half))   # lit from the left
                i = 3 if shade > 0.85 else 2 if shade > 0.5 else 1 if shade > 0.2 else 0
                c = palette[0] if edge else palette[i]
                if patina and R.random() < patina * (0.4 + t):
                    c = R.choice(VERDI)
                px[x, y] = (*c, 255)
    # the lip band
    for x in range(w):
        if px[x, lip][3]:
            px[x, lip] = (*palette[0], 255)
        if px[x, lip - 2][3] and 0 < x < w - 1:
            px[x, lip - 2] = (*palette[3 if x < cx else 1], 255)
    # crown loop
    d = ImageDraw.Draw(im)
    d.ellipse([cx - 2, 0, cx + 2, 4], outline=palette[0])
    # clapper peeking under the lip
    d.ellipse([cx - 1, lip, cx + 1, lip + 2], fill=palette[0])
    return im


def bell_frame(with_bell: bool) -> Image.Image:
    """The square's timber bell-gallows: two posts, a cross-beam with a little
    shingle cap, a bench-stone foot. 32x48; bottom 16px = the solid foot."""
    im = Image.new("RGBA", (32, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # stone foot
    d.rectangle([3, 40, 28, 46], fill=(78, 84, 96))
    d.rectangle([3, 40, 28, 41], fill=(116, 124, 138))
    d.line([(3, 46), (28, 46)], fill=INK)
    # posts
    for x in (5, 24):
        d.rectangle([x, 8, x + 2, 41], fill=TIMBER[1])
        d.line([(x, 8), (x, 41)], fill=TIMBER[3])
        d.line([(x + 2, 8), (x + 2, 41)], fill=TIMBER[0])
    # braces
    d.line([(8, 14), (12, 10)], fill=TIMBER[2])
    d.line([(23, 14), (19, 10)], fill=TIMBER[2])
    # cross-beam + cap
    d.rectangle([3, 7, 28, 10], fill=TIMBER[2])
    d.line([(3, 7), (28, 7)], fill=TIMBER[3])
    d.line([(3, 10), (28, 10)], fill=TIMBER[0])
    d.polygon([(1, 7), (16, 1), (30, 7)], fill=(52, 70, 96), outline=INK)
    d.line([(4, 6), (16, 2)], fill=(84, 108, 140))
    # the hook
    d.line([(16, 10), (16, 13)], fill=INK)
    if with_bell:
        b = _bell(16, BRONZE, "hung", patina=0.05)
        im.alpha_composite(b, (8, 12))
        # a rope tail from the clapper
        d.line([(16, 30), (16, 38)], fill=(186, 160, 110))
        d.point([(16, 39)], fill=(140, 116, 80))
    else:
        # an old frayed rope end, tied off — the frame waiting
        d.line([(16, 13), (16, 18)], fill=(150, 128, 92))
        d.point([(15, 19), (17, 19)], fill=(150, 128, 92))
    return im


def bell_sunk() -> Image.Image:
    b = _bell(24, BRONZE, "sunk", patina=0.55)
    b = b.rotate(-78, resample=Image.NEAREST, expand=True)
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    # silt shadow
    d = ImageDraw.Draw(im)
    d.ellipse([2, 22, 30, 30], fill=(20, 26, 30, 160))
    im.alpha_composite(b, ((32 - b.width) // 2, 32 - b.height - 3))
    # weed tufts at the foot
    R = rng("sunkweed")
    px = im.load()
    for x in range(4, 28):
        if R.random() < 0.35:
            for k in range(R.randint(1, 4)):
                y = 29 - k
                px[x, y] = (*R.choice(WEED), 255)
    return im


def bell_raised() -> Image.Image:
    b = _bell(22, BRONZE, "raised", patina=0.30)
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([3, 25, 29, 31], fill=(20, 26, 30, 150))
    # puddle it dripped
    d.ellipse([6, 26, 26, 30], fill=(*WATER_MID, 200))
    im.alpha_composite(b, (5, 4))
    # chain up out of frame
    for y in range(0, 6):
        d.point([(16, y)], fill=(150, 150, 160) if y % 2 else (90, 90, 100))
    # drips
    for (x, y) in ((8, 27), (22, 24), (13, 29)):
        d.point([(x, y)], fill=(*FOAM, 255))
    return im


def bell_winch() -> Image.Image:
    """The old bell-winch on the belfry ledge: an A-frame of black timber, a
    rope drum, an iron crank with a keyhole boss, the chain running off the
    drum down over the lip toward the pit. 32x32."""
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([3, 25, 29, 31], fill=(16, 20, 26, 150))              # shadow
    for x0, x1 in ((4, 9), (27, 22)):                               # A-frame legs
        d.line([(x0, 28), (x1, 6)], fill=TIMBER[0], width=3)
        d.line([(x0 + 1, 28), (x1 + 1, 6)], fill=TIMBER[2])
    d.rectangle([8, 4, 24, 7], fill=TIMBER[1], outline=INK)          # cross-tree
    d.line([(9, 4), (23, 4)], fill=TIMBER[3])
    d.rectangle([9, 11, 23, 19], fill=TIMBER[1], outline=INK)        # the drum
    for x in range(11, 23, 3):
        d.line([(x, 12), (x, 18)], fill=(150, 128, 92))              # rope turns
    d.line([(9, 15), (23, 15)], fill=TIMBER[0])
    d.ellipse([22, 12, 28, 18], fill=(70, 74, 84), outline=INK)      # crank boss
    d.point([(25, 15)], fill=(20, 20, 24))                           # keyhole
    d.line([(25, 15), (29, 21)], fill=(110, 116, 128), width=2)      # crank arm
    d.rectangle([28, 20, 30, 23], fill=(70, 50, 34))                 # handle
    for y in range(19, 30, 2):                                       # chain off the drum
        d.point([(14, y)], fill=(150, 150, 160))
        d.point([(14, y + 1)], fill=(90, 90, 100))
    return im


def garden_door() -> Image.Image:
    """The lamp-school's back door, set into the classroom's north wall face:
    old green-painted boards, a round iron ring, moss creeping out from under
    it and a seam of pale green light (the garden beyond). 16x32: the top tile
    sits over the wall band, the bottom over the face row."""
    im = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([1, 6, 14, 31], fill=(40, 30, 24), outline=INK)       # the frame
    d.rectangle([3, 9, 12, 31], fill=(46, 84, 66))                   # boards
    for x in (5, 8, 11):
        d.line([(x, 9), (x, 31)], fill=(34, 64, 52))
    d.arc([3, 4, 12, 14], 180, 360, fill=(40, 30, 24))
    d.line([(3, 18), (12, 18)], fill=(30, 52, 42))
    d.ellipse([9, 19, 12, 22], outline=(120, 120, 128))             # iron ring
    for x in range(3, 13):                                           # the light seam
        d.point([(x, 30)], fill=(168, 230, 170))
    R = rng("gardendoor")
    for x in range(1, 15):                                           # moss creeping out
        if R.random() < 0.6:
            d.point([(x, 31)], fill=R.choice(MOSS))
        if R.random() < 0.25:
            d.point([(x, 29)], fill=R.choice(MOSS))
    return im


def tinder_light() -> Image.Image:
    """The old Tinder Light on its reef: the beacon tower, cold and cracked,
    barnacled from the waterline up; the gallery rail broken, no flame."""
    im = load("tinderwick", "beacon")
    px = im.load()
    W, H = im.size
    # douse every warm pixel (lantern + windows) to cold glass / soot
    R = rng("tinderlight")
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a and r > 150 and r - b > 60:
                px[x, y] = (*(GLASS[1] if y > 20 else GLASS[0]), a)
    # crack down the tower
    x = 30
    for y in range(26, 90):
        x += R.choice((-1, 0, 0, 1))
        if px[x, y][3]:
            px[x, y] = (*INK, 255)
    # break the gallery rail: knock out a few rail pixels on the right
    for y in range(20, 30):
        for x in range(44, 62):
            if px[x, y][3] and R.random() < 0.35:
                px[x, y] = (0, 0, 0, 0)
    moss(im, 0, 20, "tlm", 0.12)
    tide_stain(im, 70, "tinderl", weed=0.18, barn=0.07, amount=0.5)
    d = ImageDraw.Draw(im)
    # a rock footing where the tower meets its islet (it stands on the reef)
    for (cx, cy, r) in ((10, 106, 6), (22, 108, 5), (40, 107, 6), (53, 105, 5), (31, 109, 4)):
        d.ellipse([cx - r, cy - r + 2, cx + r, cy + r - 2], fill=(78, 84, 96), outline=INK)
        d.arc([cx - r + 1, cy - r + 3, cx + r - 2, cy + r - 3], 200, 300, fill=(126, 136, 152))
    return im


PIECES = {
    "roof_ridge": roof_ridge,
    "roof_ridge_b": roof_ridge_b,
    "belltower": belltower,
    "sunk_cottage": sunk_cottage,
    "sunk_shop": sunk_shop,
    "old_cottage": old_cottage,
    "lamphouse": lamphouse,
    "lampschool": lampschool,
    "bell_frame": lambda: bell_frame(False),
    "bell_hung": lambda: bell_frame(True),
    "bell_sunk": bell_sunk,
    "bell_raised": bell_raised,
    "tinder_light": tinder_light,
    "bell_winch": bell_winch,
    "garden_door": garden_door,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, fn in PIECES.items():
        im = fn()
        assert im.width % 16 == 0 and im.height % 16 == 0, (stem, im.size)
        im.save(OUT / f"{stem}.png")
        print(f"  drew lowtinder/{stem:14s} {im.width}x{im.height}")


if __name__ == "__main__":
    main()
