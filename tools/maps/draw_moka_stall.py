#!/usr/bin/env python3
"""
draw_moka_stall — Bram's brew-stand in Duskapple Orchard (content/regions/kitchens.ts):
a 32x32 (2x2, overhang 1) drawn prop. A plank side-table with a squat iron burner,
the EIGHT-SIDED moka pot on it (faceted aluminium: boiler, screw waist, collector,
black handle, spout steaming), two enamel cups and a sack of beans under the table.

Drawn in code (the gbaforge rule: small structural props are drawn, not image-gen;
at 32px a downscaled render turned the pot to mush). The cantina's stall + pozole
pot are image-gen masters in the same folder.

Writes assets/tilesets/kitchens/objects/moka_stall.png -> packed to
`kitchens_moka_stall` by .claude/skills/generate-sprite-sheet/scripts/pack_objects.py.

Run:  python3 tools/maps/draw_moka_stall.py [--preview out.png]
"""
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OUT_PATH = REPO / "assets/tilesets/kitchens/objects/moka_stall.png"

W = H = 32
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
px = img.load()


def c(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


OUT = c('2a1c14')
WL, WM, WD = c('c08a52'), c('8f5c33'), c('5e3b22')
MO, MD, MM, ML, MH = c('23262e'), c('5d6470'), c('939ca8'), c('c9d1da'), c('f2f5f7')
BK, BK2 = c('17171c'), c('3a3a44')
FB, FO = c('6fb6ff'), c('ffb347')
IRON, IRON2 = c('2e3136'), c('4b5058')
CW, CR, CF, CS = c('e8e4d6'), c('3d6fb0'), c('4a2a18'), c('b9b4a4')
SK, SM, SD = c('b39565'), c('8a6c44'), c('5a4329')
BEAN = c('3b2416')
STEAM = c('d9dde6')


def put(x, y, col):
    if 0 <= x < W and 0 <= y < H:
        px[x, y] = col


def rect(x0, y0, x1, y1, col):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(x, y, col)


# ---- coffee sack under the table (behind the front legs) ----
rect(9, 25, 15, 31, SM)
rect(10, 24, 14, 24, SM)
rect(11, 23, 13, 23, SD)              # tied neck
rect(10, 26, 11, 30, SK)              # lit side
for (x, y) in [(13, 27), (14, 29), (12, 30)]:
    put(x, y, SD)
for x in range(9, 16):
    put(x, 31, SD)
for y in range(25, 32):
    put(8, y, OUT); put(16, y, OUT)
put(9, 24, OUT); put(15, 24, OUT); put(10, 23, OUT); put(14, 23, OUT)
for (x, y) in [(17, 31), (19, 31), (18, 30)]:
    put(x, y, BEAN)                   # spilled beans

# ---- table ----
rect(2, 19, 29, 19, WL)               # lit front edge of the top
rect(2, 18, 29, 18, WM)               # top surface (far edge)
rect(3, 17, 28, 17, WM)
rect(2, 20, 29, 21, WD)               # apron
for x in range(2, 30):
    put(x, 22, OUT)
for y in range(17, 23):
    put(1, y, OUT); put(30, y, OUT)
for x in range(2, 30):
    put(x, 16, OUT)
for x in (6, 13, 20, 26):             # plank seams on the apron
    put(x, 20, OUT)
# legs
for lx in (3, 27):
    rect(lx, 23, lx + 1, 31, WD)
    put(lx, 23, WM)
    for y in range(23, 32):
        put(lx - 1, y, OUT); put(lx + 2, y, OUT)

# ---- burner (squat iron ring) ----
rect(7, 14, 15, 15, IRON)
rect(8, 14, 14, 14, IRON2)
put(6, 14, OUT); put(6, 15, OUT); put(16, 14, OUT); put(16, 15, OUT)
for x in range(7, 16):
    put(x, 13, OUT)
# little flame peeking under the pot
put(9, 13, FB); put(13, 13, FB); put(11, 13, FO)

# ---- the eight-sided pot ----
# facet colours across the width: outline | dark | mid | light | HIGH | light | mid | dark | outline
def chamber_row(y, x0, x1):
    w = x1 - x0 + 1
    put(x0 - 1, y, MO); put(x1 + 1, y, MO)
    bands = [MD, MM, ML, MH, ML, MM, MD, MD]
    for i in range(w):
        put(x0 + i, y, bands[min(len(bands) - 1, i * len(bands) // w)])


# bottom (water) chamber: widest at the base, narrowing to the waist
for y, (x0, x1) in zip(range(8, 13), [(9, 13), (9, 13), (8, 14), (8, 14), (8, 14)]):
    chamber_row(y, x0, x1)
for x in range(8, 15):
    put(x, 12, MD)                    # base rim shadow
# safety valve nub on the left of the boiler
put(7, 10, MM); put(6, 10, MO)
# waist (the screw join)
rect(9, 7, 13, 7, MO)
put(10, 7, MD); put(11, 7, MM); put(12, 7, MD)
# top (collector) chamber: widening upward from the waist
for y, (x0, x1) in zip(range(3, 7), [(8, 14), (8, 14), (9, 13), (9, 13)]):
    chamber_row(y, x0, x1)
# lid + knob
rect(8, 2, 14, 2, MO)
rect(9, 2, 13, 2, MD)
put(11, 1, BK); put(10, 1, MO); put(12, 1, MO); put(11, 0, MO)
# pouring spout (left)
put(7, 3, ML); put(6, 3, MO); put(7, 2, MO)
# black handle (right)
for y in range(3, 9):
    put(16, y, BK)
put(15, 3, BK); put(15, 8, BK); put(17, 4, MO); put(17, 5, MO); put(17, 6, MO); put(17, 7, MO)
put(16, 4, BK2)

# ---- steam wisp off the spout ----
for (x, y) in [(5, 1), (4, 0), (6, 0)]:
    put(x, y, STEAM)

# ---- two enamel cups ----
for cx in (19, 24):
    rect(cx, 13, cx + 3, 15, CW)
    rect(cx, 13, cx + 3, 13, CR)       # blue rim
    rect(cx + 1, 13, cx + 2, 13, CF)   # coffee
    put(cx, 15, CS)
    put(cx + 4, 14, CW)                # handle
    for y in range(13, 16):
        put(cx - 1, y, OUT)
    put(cx + 4, 13, OUT); put(cx + 4, 15, OUT); put(cx + 5, 14, OUT)
    for x in range(cx, cx + 4):
        put(x, 12, OUT)
        put(x, 16, OUT)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT_PATH)
print(f"wrote {OUT_PATH.relative_to(REPO)}")
if "--preview" in sys.argv:
    dst = sys.argv[sys.argv.index("--preview") + 1]
    big = Image.new('RGBA', (W * 8, H * 8), (40, 60, 60, 255))
    big.alpha_composite(img.resize((W * 8, H * 8), Image.NEAREST))
    big.save(dst)
