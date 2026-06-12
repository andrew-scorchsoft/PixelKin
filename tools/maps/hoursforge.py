#!/usr/bin/env python3
"""
hoursforge — DRAWN object masters for the Three Hours shrine sites
(docs/world/walkthrough/07-the-three.md). The terrain-stays-drawn rule
extended to the sites' small hero props: every piece here is deterministic
PIL pixel-work on the world-palette ramps (assets/tilesets/world-palette.json),
so the kits are seamless with the gbaforge register and cost no image-gen.

Pieces (masters -> assets/tilesets/<area>/objects/<stem>.png, packed by
pack_objects.py into public/assets/sprites/objects/<area>_<stem>.webp):

  tideglass/  lens_cold + lens_lit        (2x2) the Lampwright's Relay lenses
              wreck                       (3x2) the old fisher's broken boat
              wrecklamp_dark + _lit       (1x2) the stern-lamp (S3's payoff)
              glass_spire                 (2x3) tideglass vein spire (dressing)
  hourfold/   brazier_lit + _snuffed      (2x3) the Unstruck Toll's vigil-braziers
  unrisen/    basin_dry + basin_filled    (2x1) the First-Light sun-basin (host-side)

Run:  ./venv/bin/python tools/maps/hoursforge.py
then  ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
T = 16

# world-palette ramps (outline -> dark -> mid -> light)
INK = (11, 16, 38)
INK2 = (26, 20, 48)
STONE = [(42, 44, 64), (74, 77, 102), (108, 111, 134), (154, 157, 180)]
WOOD = [(58, 36, 24), (122, 74, 40), (185, 118, 63), (224, 164, 102)]
TEAL = [(14, 42, 85), (31, 90, 160), (79, 180, 255), (159, 231, 255)]
FIRE = [(122, 42, 20), (200, 90, 34), (255, 138, 61), (255, 192, 112)]
BONE = [(122, 111, 90), (188, 174, 144), (230, 220, 192), (248, 242, 226)]
SNOW = [(127, 143, 176), (174, 191, 224), (216, 228, 246), (255, 255, 255)]
PALE = [(110, 150, 170), (160, 210, 220), (200, 240, 240), (240, 255, 255)]
GOLD = [(154, 111, 79), (224, 201, 140), (246, 236, 192), (255, 250, 230)]


def canvas(tw: int, th: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (tw * T, th * T), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def save(im: Image.Image, area: str, stem: str) -> None:
    out = REPO / "assets/tilesets" / area / "objects" / f"{stem}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    print(f"  drew {area}/{stem}.png {im.width}x{im.height}")


# ---- Tideglass: the relay lenses ---------------------------------------------------
def lens(lit: bool) -> Image.Image:
    im, d = canvas(2, 2)
    # pedestal: a low dark sea-stone block, bottom tile row
    d.rectangle([8, 22, 23, 30], fill=STONE[1], outline=INK)
    d.rectangle([6, 26, 25, 31], fill=STONE[0], outline=INK)
    d.line([8, 23, 23, 23], fill=STONE[2])
    # the standing sea-glass ring (a round lens held in a driftwood crutch)
    d.line([10, 22, 12, 16], fill=WOOD[1], width=2)
    d.line([21, 22, 19, 16], fill=WOOD[1], width=2)
    ring = TEAL if not lit else FIRE
    d.ellipse([9, 4, 22, 17], outline=INK, width=1)
    d.ellipse([10, 5, 21, 16], outline=ring[1], width=2)
    d.ellipse([12, 7, 19, 14], fill=(ring[2][0], ring[2][1], ring[2][2], 170))
    if lit:
        # the carried beam: a hot amber core + glints off the glass
        d.ellipse([14, 9, 17, 12], fill=FIRE[3])
        for (x, y) in [(8, 3), (23, 6), (11, 18), (20, 2)]:
            im.putpixel((x, y), TEAL[3] + (255,))
        d.point([(15, 8), (16, 13)], fill=(255, 255, 255, 255))
    else:
        # cold: one faint inner glint only
        d.point([(13, 8)], fill=TEAL[3] + (220,))
    return im


# ---- Tideglass: the wreck + the stern-lamp -----------------------------------------
def wreck() -> Image.Image:
    im, d = canvas(3, 2)
    # broken hull, beached at a tilt: planked side, snapped rail
    d.polygon([(2, 24), (8, 10), (38, 8), (45, 18), (43, 28), (4, 30)],
              fill=WOOD[1], outline=INK)
    for y in (14, 18, 22, 26):
        d.line([5, y + 2, 42, y], fill=WOOD[0])
    d.line([8, 10, 38, 8], fill=WOOD[2], width=2)            # gunwale highlight
    # the broken mast stump + a fallen spar
    d.rectangle([20, 2, 23, 10], fill=WOOD[0], outline=INK)
    d.line([24, 4, 30, 2], fill=WOOD[0], width=2)
    # hull breach: the dark tear that let the sea in
    d.polygon([(12, 20), (18, 16), (20, 26), (12, 28)], fill=INK)
    # teal glass-glint barnacle line at the waterline
    for x in range(6, 42, 6):
        im.putpixel((x, 29), TEAL[2] + (255,))
    return im


def wrecklamp(lit: bool) -> Image.Image:
    im, d = canvas(1, 2)
    # the bent stern-post, wedged in rock
    d.rectangle([6, 12, 9, 28], fill=WOOD[0], outline=INK)
    d.rectangle([2, 26, 13, 31], fill=STONE[0], outline=INK)  # the rocks
    d.rectangle([4, 25, 7, 28], fill=STONE[1])
    # the square stern-lamp hung from the post's crook
    d.line([7, 12, 7, 8], fill=INK2, width=2)
    d.rectangle([3, 2, 12, 11], fill=STONE[0], outline=INK)
    if lit:
        d.rectangle([5, 4, 10, 9], fill=FIRE[2])
        d.rectangle([6, 5, 9, 7], fill=FIRE[3])
        im.putpixel((7, 5), (255, 255, 255, 255))
        for (x, y) in [(1, 3), (14, 5), (2, 10)]:
            im.putpixel((x, y), FIRE[3] + (140,))
    else:
        d.rectangle([5, 4, 10, 9], fill=(INK2[0], INK2[1], INK2[2], 255))
        im.putpixel((7, 6), TEAL[1] + (255,))                 # the dead wick
    return im


def glass_spire() -> Image.Image:
    im, d = canvas(2, 3)
    # a leaning blade of tideglass catching the lamp
    d.polygon([(8, 2), (20, 10), (24, 44), (12, 46), (6, 20)],
              fill=TEAL[1], outline=INK)
    d.polygon([(10, 6), (16, 12), (18, 38), (13, 40)], fill=TEAL[2])
    d.line([11, 8, 14, 34], fill=TEAL[3])
    d.rectangle([6, 42, 26, 47], fill=STONE[0], outline=INK)
    im.putpixel((12, 10), (255, 255, 255, 255))
    return im


# ---- Hourfold: the vigil-braziers ---------------------------------------------------
def hour_brazier(lit: bool) -> Image.Image:
    im, d = canvas(2, 3)
    # cold-stone bowl on three legs (the pale_vault register)
    d.rectangle([6, 40, 25, 45], fill=STONE[0], outline=INK)      # plinth
    d.line([10, 34, 8, 40], fill=STONE[1], width=2)
    d.line([21, 34, 23, 40], fill=STONE[1], width=2)
    d.line([15, 34, 15, 40], fill=STONE[0], width=2)
    d.ellipse([4, 26, 27, 36], fill=STONE[1], outline=INK)        # the bowl
    d.ellipse([7, 28, 24, 33], fill=STONE[0])
    d.arc([4, 26, 27, 36], 180, 360, fill=STONE[2])
    if lit:
        # the blue-white vigil flame the Hour will not be seen by
        d.polygon([(15, 6), (20, 16), (18, 26), (12, 26), (10, 18)],
                  fill=PALE[1], outline=PALE[0])
        d.polygon([(15, 10), (17, 18), (15, 24), (13, 19)], fill=PALE[2])
        d.line([15, 13, 15, 21], fill=PALE[3], width=2)
        im.putpixel((15, 12), (255, 255, 255, 255))
        for (x, y) in [(8, 8), (23, 12), (5, 20)]:
            im.putpixel((x, y), PALE[3] + (150,))
    else:
        # snuffed: a thread of grey and the dark kept on purpose
        d.line([15, 14, 14, 20], fill=SNOW[0], width=1)
        d.point([(15, 12), (16, 10)], fill=SNOW[1] + (160,))
        d.ellipse([10, 29, 21, 33], fill=INK2)                    # cold coals
        d.point([(13, 30), (18, 31)], fill=STONE[1])
    return im


# ---- Unrisen: the First-Light basin (host-side, Sunken Solarium) --------------------
def basin(filled: bool) -> Image.Image:
    im, d = canvas(2, 1)
    d.ellipse([1, 2, 30, 15], fill=BONE[1], outline=INK)          # the rim
    d.ellipse([4, 4, 27, 13], fill=BONE[0], outline=INK2)         # inner lip
    if filled:
        d.ellipse([6, 5, 25, 12], fill=GOLD[2])
        d.ellipse([10, 6, 21, 10], fill=GOLD[3])
        im.putpixel((14, 7), (255, 255, 255, 255))
        for (x, y) in [(3, 1), (28, 3), (8, 15)]:
            im.putpixel((x, y), GOLD[3] + (160,))
    else:
        d.ellipse([6, 5, 25, 12], fill=(INK2[0], INK2[1], INK2[2], 255))
        d.arc([6, 5, 25, 12], 200, 320, fill=STONE[1])            # dry silt ring
        d.point([(12, 8), (19, 9)], fill=BONE[0])
    return im


def main() -> None:
    save(lens(False), "tideglass", "lens_cold")
    save(lens(True), "tideglass", "lens_lit")
    save(wreck(), "tideglass", "wreck")
    save(wrecklamp(False), "tideglass", "wrecklamp_dark")
    save(wrecklamp(True), "tideglass", "wrecklamp_lit")
    save(glass_spire(), "tideglass", "glass_spire")
    save(hour_brazier(True), "hourfold", "brazier_lit")
    save(hour_brazier(False), "hourfold", "brazier_snuffed")
    save(basin(False), "unrisen", "basin_dry")
    save(basin(True), "unrisen", "basin_filled")


if __name__ == "__main__":
    main()
