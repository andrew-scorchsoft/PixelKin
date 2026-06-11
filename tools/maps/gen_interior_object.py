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
_BASE = ("Original 16-bit SNES-era RPG pixel-art furniture sprite, chunky pixels, "
         "dark-ink outline, top-left light source, GBC-restrained palette, NO text. "
         "The ENTIRE background is FLAT PURE MAGENTA #FF00FF (no shadow, no gradient, no "
         "checkerboard) so it can be keyed out; keep magenta OUT of the object's own colours. ")
# Two projections (docs/world/interiors.md §1):
#   topdown — free-standing pieces: visible top surface + short front face.
#   front   — WALL-MOUNTED pieces: a strict straight-on FRONT ELEVATION (like a
#             doll's-house wall): absolutely NO isometric or 3/4 angle, NO top
#             surface visible, NO perspective — and the piece must fill the
#             frame EDGE TO EDGE so it sits flush against the room's wall.
STYLE = {
    "topdown": _BASE + ("A single object drawn whole, viewed from the gentle top-down-with-"
                        "a-hint-of-front angle of a classic RPG room interior: most of the "
                        "sprite is the object's TOP surface, with a short front face strip "
                        "at the bottom. "),
    "front": _BASE + ("A single piece of furniture drawn as a strict STRAIGHT-ON FRONT "
                      "ELEVATION, dead-centre eye level, zero perspective — NOT isometric, "
                      "NOT three-quarter view, no visible top surface, no side faces, no "
                      "floor. It stands against a wall, so the artwork must FILL THE FRAME "
                      "EDGE TO EDGE horizontally and reach the very bottom of the frame "
                      "(its feet/base at the bottom edge). "),
}


def key_and_snap(raw: Path, w_tiles: int, h_tiles: int, top_pad: int,
                 fill: bool = False) -> Image.Image:
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
    if fill:
        # wall-elevation pieces must span the canvas edge-to-edge (flush mount):
        # resize exactly, accepting the small aspect stretch
        im = im.resize((tw, body_h),
                       Image.NEAREST if tw >= im.width else Image.LANCZOS)
        if tw < im.width:
            al = im.split()[3].point(lambda v: 255 if v >= 128 else 0)
            im.putalpha(al)
        canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        canvas.alpha_composite(im, (0, th - body_h))
        return canvas
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
    ap.add_argument("--projection", choices=("topdown", "front"), default="topdown",
                    help="'front' = strict wall-elevation (wall-mounted pieces)")
    ap.add_argument("--outdir", default=None,
                    help="write somewhere other than the live masters dir (A/B trials)")
    args = ap.parse_args()

    outdir = Path(args.outdir) if args.outdir else OBJDIR
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.png"
        prompt = STYLE[args.projection] + args.subject
        r = subprocess.run([PY, str(GEN), "--prompt", prompt, "--output", str(raw),
                            "--provider", args.provider], capture_output=True, text=True)
        if not raw.exists():
            print(r.stdout[-2000:]); print(r.stderr[-2000:]); return 1
        out = outdir / f"{args.stem}.png"
        snapped = key_and_snap(raw, args.w, args.h, args.top_pad,
                               fill=(args.projection == "front"))
        snapped.save(out)
        checker(snapped).save(f"/tmp/obj_{args.stem}.png")
        shown = out.relative_to(REPO) if out.is_relative_to(REPO) else out
        print(f"  wrote {shown}  ({args.w*16}x{args.h*16})  preview /tmp/obj_{args.stem}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
