#!/usr/bin/env python3
"""
Build the per-page Open Graph / social-share cards for the PixelKin site.

Each page gets a unique 1200x630 JPG: a pixel-art Vesperholm background master
(assets/img/og/src/<page>.webp) with the PixelKin wordmark + the page's title
composited on top, so branding stays crisp and consistent while the art is
unique per page. Output -> assets/img/og/<page>.jpg, picked up automatically by
includes/header.php (it maps each page's stem to og/<stem>.jpg, logo fallback).

Format note: og:image is JPG, not WebP — Facebook/LinkedIn still don't render
WebP link previews reliably (Twitter/X does). JPG is the safe cross-platform
default.

The background masters were generated once with the generate-image skill (dusk
pixel-art briefs, the hero scene as a palette reference). To re-render the text
without re-paying for generation, just edit PAGES below and re-run this. To make
a fresh background, regenerate the master into assets/img/og/src/<page>.webp.

Run from the web/ directory:  ../venv/bin/python tools/build_og_cards.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent          # web/
SRC = ROOT / "assets/img/og/src"
OUT = ROOT / "assets/img/og"
FONT = ROOT / "assets/fonts/PressStart2P-Regular.ttf"
WORDMARK = ROOT / "assets/img/logo-text.webp"

W, H = 1200, 630
AMBER = (255, 196, 120)
CYAN = (160, 224, 255)

# page stem (matches header.php's basename($page)) -> (TITLE, subtitle)
# A "\n" in the title forces a line break.
PAGES = {
    "index":     ("LANTERNS IN\nTHE DARK", "Free retro creature-collecting, in your browser"),
    "about":     ("ABOUT",        "A love letter to handheld-era collecting"),
    "story":     ("THE WORLD",    "Relight the sky over Vesperholm"),
    "creatures": ("THE KIN",      "150+ original creatures, a copy of nothing"),
    "faq":       ("FAQ",          "Everything you need to start playing"),
    "license":   ("LICENSING",    "PixelKin, by Scorchsoft"),
    "privacy":   ("PRIVACY",      "Your progress stays in your browser"),
    "terms":     ("TERMS OF USE", "Free to play, provided as is"),
}


def cover(im, w, h):
    """Resize-to-cover then centre-crop to exactly w x h."""
    iw, ih = im.size
    scale = max(w / iw, h / ih)
    im = im.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def main():
    wordmark = Image.open(WORDMARK).convert("RGBA")
    for page, (title, sub) in PAGES.items():
        bg = Image.open(SRC / f"{page}.webp").convert("RGB")
        card = cover(bg, W, H).convert("RGBA")

        # Left + bottom dark scrim for text legibility.
        for ramp, peak, axis in (("left", 200, "x"), ("bottom", 150, "y")):
            mask = Image.new("L", (W, H), 0)
            md = ImageDraw.Draw(mask)
            if axis == "x":
                for x in range(W):
                    md.line([(x, 0), (x, H)], fill=int(peak * max(0, 1 - x / (W * 0.62))))
            else:
                for y in range(H):
                    md.line([(0, y), (W, y)], fill=int(peak * max(0, (y - H * 0.45) / (H * 0.55))))
            dark = Image.new("RGBA", (W, H), (4, 8, 24, 0))
            dark.putalpha(mask)
            card = Image.alpha_composite(card, dark)

        draw = ImageDraw.Draw(card)
        MX = 70

        # Wordmark, top-left, with an amber underline accent.
        wm_w = 380
        wm = wordmark.resize((wm_w, round(wordmark.height * wm_w / wordmark.width)), Image.LANCZOS)
        card.alpha_composite(wm, (MX, 60))
        draw.rectangle([MX, 60 + wm.height + 16, MX + 300, 60 + wm.height + 20], fill=AMBER)

        # Title (pixel font, shadowed).
        lines = title.split("\n")
        tfont = ImageFont.truetype(str(FONT), 60 if len(lines) > 1 else 64)
        ty = 250
        for ln in lines:
            draw.text((MX + 4, ty + 4), ln, font=tfont, fill=(0, 0, 0))
            draw.text((MX, ty), ln, font=tfont, fill=AMBER)
            ty += tfont.size + 22

        # Subtitle (wrapped to fit).
        sfont = ImageFont.truetype(str(FONT), 19)
        sy, maxw = ty + 18, W - MX - 60
        words, line, wrapped = sub.split(), "", []
        for w in words:
            test = (line + " " + w).strip()
            if draw.textlength(test, font=sfont) <= maxw:
                line = test
            else:
                wrapped.append(line); line = w
        if line:
            wrapped.append(line)
        for ln in wrapped:
            draw.text((MX + 2, sy + 2), ln, font=sfont, fill=(0, 0, 0))
            draw.text((MX, sy), ln, font=sfont, fill=CYAN)
            sy += sfont.size + 12

        card.convert("RGB").save(OUT / f"{page}.jpg", quality=82, optimize=True)
        print(f"{page}.jpg")


if __name__ == "__main__":
    main()
