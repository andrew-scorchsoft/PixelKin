#!/usr/bin/env python3
"""
milagro_lorecard — draws the printed STORY SLIP that comes in the Booji-Wooji Man's
box of milagro cards (the real one is a little printed card with a yellow border;
this is its Vesperholm version, the text from content/milagros.ts MILAGRO_LORE).
A typeset card, not a painting, so it's drawn in code: white stock, a thin
mustard double border, the title in mustard capitals, the body in small black type.

    python3 tools/assets/milagro_lorecard.py    # -> assets/milagros/lore.webp
                                               #    (then gen_milagros.py --pack)
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
W, H = 682, 1024
MUSTARD = (226, 170, 40)
INK = (24, 24, 30)
FONTS = "/usr/share/fonts/truetype/dejavu/"


def lore_text() -> str:
    src = (REPO / "src/game/content/milagros.ts").read_text()
    block = src[src.index("export const MILAGRO_LORE ="):]
    block = block[: block.index(";\n")]
    parts = re.findall(r"'((?:[^'\\]|\\.)*)'", block)
    return "".join(parts).replace("\\'", "'")


def wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if d.textlength(t, font=font) > width:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    return lines


def main() -> None:
    im = Image.new("RGB", (W, H), (252, 250, 244))
    d = ImageDraw.Draw(im)
    d.rectangle([22, 22, W - 23, H - 23], outline=MUSTARD, width=5)
    d.rectangle([34, 34, W - 35, H - 35], outline=MUSTARD, width=2)
    title = ImageFont.truetype(FONTS + "DejaVuSans-Bold.ttf", 46)
    for i, line in enumerate(("BOOJI-WOOJI MAN", "MILAGRO CARDS")):
        d.text((W / 2, 80 + i * 56), line, font=title, fill=MUSTARD, anchor="ma", stroke_width=1, stroke_fill=(150, 105, 20))
    body = ImageFont.truetype(FONTS + "DejaVuSans.ttf", 19)
    y = 230
    for para in re.split(r"(?<=\.) (?=These days|The cards are|He asks)", lore_text()):
        for line in wrap(d, para, body, W - 120):
            d.text((60, y), line, font=body, fill=INK)
            y += 25
        y += 12
    small = ImageFont.truetype(FONTS + "DejaVuSans.ttf", 15)
    d.rectangle([W / 2 - 22, H - 130, W / 2 + 22, H - 80], fill=(176, 40, 32))
    d.text((W / 2, H - 70), "A WAYFARING PRESS PRODUCTION", font=small, fill=INK, anchor="ma")
    out = REPO / "assets/milagros/lore.webp"
    im.save(out, quality=94)
    print(f"  drew {out.relative_to(REPO)}  (body ends at y={y})")


if __name__ == "__main__":
    main()
