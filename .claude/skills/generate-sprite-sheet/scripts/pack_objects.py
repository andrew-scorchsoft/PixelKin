#!/usr/bin/env python3
"""
Object packer — whole multi-tile STRUCTURE sprites (buildings, big trees, lamps).

The structure analogue of pack_tileset/pack_trainers (art-style.md §14b). Each
object is ONE transparent sprite drawn whole (not tiled); maps place it via a
`MapObject` and the engine splits it at its overhang. This packs every object
master into a served lossless-WebP + one manifest the game preloads.

Source (masters, NOT served):  assets/tilesets/<area>/objects/<stem>.png
Output (served):               public/assets/sprites/objects/<area>_<stem>.webp
                               public/assets/sprites/objects/objects.manifest.json

Masters must be sized to an exact 16px tile multiple (so MapObject w/h match the
sprite). Run from repo root (no args packs every object):

    ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageChops

REPO = Path(__file__).resolve().parents[4]
SRC_GLOB = "assets/tilesets/*/objects/*.png"
OUT_DIR = REPO / "public" / "assets" / "sprites" / "objects"
SERVED_PREFIX = "assets/sprites/objects"


def assert_lossless(src: Image.Image, dst: Path) -> None:
    got = Image.open(dst).convert("RGBA")
    if got.size != src.size:
        raise SystemExit(f"FAIL {dst.name}: size {got.size} != {src.size}")
    if ImageChops.difference(src, got).getbbox() is not None:
        raise SystemExit(f"FAIL {dst.name}: WebP not lossless")


def pack() -> None:
    masters = sorted(REPO.glob(SRC_GLOB))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    entries: dict[str, dict] = {}
    for master in masters:
        area = master.parent.parent.name           # assets/tilesets/<area>/objects/<stem>.png
        key = f"{area}_{master.stem}"
        img = Image.open(master).convert("RGBA")
        if img.width % 16 or img.height % 16:
            raise SystemExit(
                f"FAIL {master}: {img.size} is not a 16px tile multiple (see art-style §14b)")
        out = OUT_DIR / f"{key}.webp"
        img.save(out, "WEBP", lossless=True, quality=100, method=6)
        assert_lossless(img, out)
        entries[key] = {
            "path": f"{SERVED_PREFIX}/{key}.webp",
            "width": img.width, "height": img.height,
            "tw": img.width // 16, "th": img.height // 16,
        }
        print(f"  packed {key:24s} {img.width}x{img.height} -> {out.relative_to(REPO)}")
    (OUT_DIR / "objects.manifest.json").write_text(
        json.dumps({"objects": entries}, indent=2) + "\n")
    print(f"  manifest -> {len(entries)} objects")


if __name__ == "__main__":
    pack()
