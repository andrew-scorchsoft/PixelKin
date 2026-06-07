#!/usr/bin/env python3
"""
Generate a single transparent interior FURNITURE object master (docs/world/interiors.md §1,
art-style §I/§14b). Objects are whole multi-tile transparent sprites packed by pack_objects.py.

generate-image (Google Nano) has no native alpha, so we render the brief on a flat MAGENTA
chroma field (art-style §6), key the magenta out, autocrop, then snap onto an exact WxH
tile-multiple canvas (bottom-centred, with `--top-pad` rows reserved on top for a roof/lamp
overhang). Composites the result over a checkerboard at /tmp for a clean-transparency eyeball.

  python3 tools/maps/gen_interior_object.py --stem altar --w 3 --h 3 --top-pad 1 \
      --subject "a warm lamp-shrine altar ..."

Writes assets/tilesets/interior/objects/<stem>.png  (16px-multiple, transparent).
"""
from __future__ import annotations
import argparse, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
GEN = REPO / ".claude/skills/generate-image/scripts/generate.py"
OBJDIR = REPO / "assets/tilesets/interior/objects"
PY = sys.executable

MAGENTA = (255, 0, 255)
STYLE = ("Original 16-bit SNES-era top-down RPG pixel-art furniture sprite, chunky pixels, "
         "dark-ink outline, top-left light source, GBC-restrained palette, NO text. "
         "The ENTIRE background is FLAT PURE MAGENTA #FF00FF (no shadow, no gradient, no "
         "checkerboard) so it can be keyed out; keep magenta OUT of the object's own colours. "
         "A single object centred, drawn whole, viewed from the same gentle top-down angle as a "
         "classic RPG room. ")


def key_and_snap(raw: Path, w_tiles: int, h_tiles: int, top_pad: int) -> Image.Image:
    im = Image.open(raw).convert("RGBA")
    px = im.load()
    W, H = im.size
    # key out near-magenta
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if r > 150 and b > 150 and g < 110:
                px[x, y] = (0, 0, 0, 0)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    tw, th = w_tiles * 16, h_tiles * 16
    body_h = th - top_pad * 16
    # scale to fit within (tw, body_h) preserving aspect
    sc = min(tw / im.width, body_h / im.height)
    nw, nh = max(1, round(im.width * sc)), max(1, round(im.height * sc))
    im = im.resize((nw, nh), Image.NEAREST if sc >= 1 else Image.LANCZOS)
    # re-binarise alpha after lanczos
    if sc < 1:
        a = im.split()[3].point(lambda v: 255 if v >= 128 else 0)
        im.putalpha(a)
    canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ox = (tw - im.width) // 2
    oy = th - im.height  # bottom-anchored (footprint sits at the bottom rows)
    canvas.alpha_composite(im, (ox, oy))
    return canvas


def checker(im: Image.Image, scale: int = 6) -> Image.Image:
    big = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    bg = Image.new("RGBA", big.size)
    c = 12 * scale
    for y in range(0, big.height, c):
        for x in range(0, big.width, c):
            shade = 200 if ((x // c + y // c) % 2 == 0) else 150
            for yy in range(y, min(y + c, big.height)):
                for xx in range(x, min(x + c, big.width)):
                    bg.putpixel((xx, yy), (shade, shade, shade, 255))
    bg.alpha_composite(big)
    return bg.convert("RGB")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stem", required=True)
    ap.add_argument("--w", type=int, required=True)
    ap.add_argument("--h", type=int, required=True)
    ap.add_argument("--top-pad", type=int, default=0, help="transparent tile rows reserved on top")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--provider", default="google")
    args = ap.parse_args()

    OBJDIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.png"
        prompt = STYLE + args.subject
        r = subprocess.run([PY, str(GEN), "--prompt", prompt, "--output", str(raw),
                            "--provider", args.provider], capture_output=True, text=True)
        if not raw.exists():
            print(r.stdout[-2000:]); print(r.stderr[-2000:]); return 1
        out = OBJDIR / f"{args.stem}.png"
        snapped = key_and_snap(raw, args.w, args.h, args.top_pad)
        snapped.save(out)
        checker(snapped).save(f"/tmp/obj_{args.stem}.png")
        print(f"  wrote {out.relative_to(REPO)}  ({args.w*16}x{args.h*16})  preview /tmp/obj_{args.stem}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
