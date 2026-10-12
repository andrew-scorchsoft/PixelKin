#!/usr/bin/env python3
"""
render_world — every outdoor map rendered and stitched at its TRUE walked position.

world_geometry.py proves the world closes (rectangles + links); world_layout.py draws
the schematic MAP screen. This draws the real thing: each map's art pasted where
world_geometry places it, north up, so you can see how routes run into each other.
Caves/interiors entered by a mid-map door or mouth are PORTALS, not edge links, so
they are not on the stitch — pass `--sheet` for a labelled contact sheet of those.

  python3 tools/maps/render_world.py                       # -> tools/maps/out/world_full.png + world_overview.png
  python3 tools/maps/render_world.py --highlight wickrun_ sunvault_climb   # orange-outline these id prefixes
  python3 tools/maps/render_world.py --sheet "The Old Seams:old_seams_i,old_seams_ii,old_seams_iii" \\
                                     --sheet "Paul's house:paul_house_1,paul_house_2,paul_house_3"

Renders each map via the generate-sprite-sheet skill's render_map.py at 1 px/px
(16 px tiles), so the full image is ~3.4k x 7.9k; the overview is a 1/3 downscale.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
RENDER = REPO / ".claude/skills/generate-sprite-sheet/scripts/render_map.py"
MAPS = REPO / "public/assets/maps"
OUT = REPO / "tools/maps/out"
T = 16
PAD = 24
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def render(mid: str, tmp: Path) -> Image.Image:
    p = tmp / f"{mid}.png"
    if not p.exists():
        subprocess.run([sys.executable, str(RENDER), mid, "--output", str(p), "--scale", "1"],
                       check=True, capture_output=True)
    return Image.open(p).convert("RGB")


def name_of(mid: str) -> str:
    return json.loads((MAPS / f"{mid}.json").read_text()).get("display_name", mid)


def stitch(geo: dict, tmp: Path, highlight: list[str]) -> Image.Image:
    new = lambda m: any(m.startswith(h) for h in highlight)
    x0 = min(x for x, _ in geo["pos"].values())
    y0 = min(y for _, y in geo["pos"].values())
    w = max(x + geo["size"][m][0] for m, (x, _) in geo["pos"].items()) - x0
    h = max(y + geo["size"][m][1] for m, (_, y) in geo["pos"].items()) - y0
    img = Image.new("RGB", (w * T + 2 * PAD, h * T + 2 * PAD), (14, 16, 30))
    dr = ImageDraw.Draw(img)
    f = font(22)
    boxes = {}
    for m, (x, y) in geo["pos"].items():
        art = render(m, tmp)
        px, py = (x - x0) * T + PAD, (y - y0) * T + PAD
        img.paste(art, (px, py))
        boxes[m] = (px, py, px + art.width, py + art.height)
    for m, (a, b, c, e) in boxes.items():
        dr.rectangle((a, b, c - 1, e - 1), outline=(255, 150, 40) if new(m) else (230, 230, 240),
                     width=3 if new(m) else 1)
    for m, (a, b, _, _) in boxes.items():
        label = name_of(m) + ("  ★ new" if new(m) else "")
        dr.rectangle((a + 4, b + 4, a + 14 + dr.textlength(label, font=f), b + 34), fill=(0, 0, 0))
        dr.text((a + 9, b + 7), label, font=f, fill=(255, 190, 90) if new(m) else (255, 255, 255))
    return img


def sheet(rows: list[tuple[str, list[str]]], tmp: Path) -> Image.Image:
    g = 24
    built = []
    for title, ids in rows:
        cells = []
        for m in ids:
            short = name_of(m).split(" — ")[-1].split(": ")[-1]
            cells.append((short, render(m, tmp)))
        built.append((title, cells))
    width = max(sum(i.width for _, i in c) + g * (len(c) + 1) for _, c in built)
    height = sum(max(i.height for _, i in c) + 90 for _, c in built) + g
    img = Image.new("RGB", (width, height), (14, 16, 30))
    dr = ImageDraw.Draw(img)
    y = g
    for title, cells in built:
        dr.text((g, y), title, font=font(26), fill=(255, 190, 90))
        y += 40
        x = g
        for short, art in cells:
            f = font(20)
            while dr.textlength(short, font=f) > art.width and f.size > 11:
                f = font(f.size - 1)
            dr.text((x, y), short, font=f, fill=(255, 255, 255))
            img.paste(art, (x, y + 26))
            x += art.width + g
        y += max(i.height for _, i in cells) + 50
    return img


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--highlight", nargs="*", default=[], help="map-id prefixes to outline")
    ap.add_argument("--sheet", action="append", default=[],
                    help='"Row title:id,id,..." — a contact-sheet row of portal maps (repeatable)')
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        geo_path = tmp / "geo.json"
        subprocess.run([sys.executable, str(REPO / "tools/maps/world_geometry.py"), "--no-png",
                        "--json", str(geo_path)], check=True, capture_output=True)
        img = stitch(json.loads(geo_path.read_text()), tmp, a.highlight)
        img.save(a.out / "world_full.png", optimize=True)
        img.resize((img.width // 3, img.height // 3), Image.LANCZOS).save(
            a.out / "world_overview.png", optimize=True)
        print(f"wrote {a.out / 'world_full.png'} {img.size} + world_overview.png")
        if a.sheet:
            rows = [(s.split(":", 1)[0], s.split(":", 1)[1].split(",")) for s in a.sheet]
            sheet(rows, tmp).save(a.out / "world_portals.png", optimize=True)
            print(f"wrote {a.out / 'world_portals.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
