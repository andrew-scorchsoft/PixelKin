#!/usr/bin/env python3
"""
Trainer / human walk-sheet packer for PixelKin.

The "code does the layout" half of character-sprite generation, mirroring
pack_creatures.py / pack_tileset.py. The masters under assets/trainers/ are
3x4 walk sheets (32x32 frames, 96x128 total) per docs/art-style.md §A:
rows = down/left/right/up, cols = idle/step-1/step-2. This script packs each
master into a served, lossless-WebP spritesheet plus one manifest the game loads.

Source (read-only masters, NOT served):

    assets/trainers/<stem>.png        # e.g. player_indi.png, professor_fenn.png

Output (served — vite drops the public/ prefix at runtime):

    public/assets/sprites/trainers/<stem>.webp
    public/assets/sprites/trainers/trainers.manifest.json

Manifest shape (consumed by PreloadScene):

  {
    "frame_width": 32, "frame_height": 32, "cols": 3, "rows": 4,
    "trainers": {
      "player_indi":    { "path": "assets/sprites/trainers/player_indi.webp",    "width": 96, "height": 128 },
      "professor_fenn": { "path": "assets/sprites/trainers/professor_fenn.webp", "width": 96, "height": 128 }
    }
  }

WebP is written LOSSLESS (lossless=True, quality=100, method=6) — lossy WebP
destroys the crisp 1px pixel-art edges. Each written file is decoded and asserted
to round-trip visually identical to its source, failing loudly otherwise.

Run from the repo root (no args packs every trainer master):

    ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_trainers.py
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops

# Human walk-sheet canvas standard (docs/art-style.md §4 / §A).
FRAME_W, FRAME_H, COLS, ROWS = 32, 32, 3, 4
SHEET_W, SHEET_H = FRAME_W * COLS, FRAME_H * ROWS

REPO = Path(__file__).resolve().parents[4]
SRC_DIR = REPO / "assets" / "trainers"
OUT_DIR = REPO / "public" / "assets" / "sprites" / "trainers"
SERVED_PREFIX = "assets/sprites/trainers"


def assert_lossless(src: Image.Image, dst_path: Path) -> None:
    """Decode the written WebP and assert it is pixel-identical to the source."""
    got = Image.open(dst_path).convert("RGBA")
    if got.size != src.size:
        raise SystemExit(f"FAIL {dst_path.name}: size {got.size} != source {src.size}")
    diff = ImageChops.difference(src, got).getbbox()
    if diff is not None:
        raise SystemExit(f"FAIL {dst_path.name}: WebP is not lossless (diff bbox {diff})")


def pack() -> None:
    masters = sorted(SRC_DIR.glob("*.png"))
    if not masters:
        raise SystemExit(f"No trainer masters found in {SRC_DIR}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    entries: dict[str, dict] = {}

    for master in masters:
        stem = master.stem
        img = Image.open(master).convert("RGBA")
        if img.size != (SHEET_W, SHEET_H):
            raise SystemExit(
                f"FAIL {master.name}: expected {SHEET_W}x{SHEET_H} 3x4 walk sheet, got "
                f"{img.size[0]}x{img.size[1]} (see docs/art-style.md §A)"
            )
        out = OUT_DIR / f"{stem}.webp"
        img.save(out, "WEBP", lossless=True, quality=100, method=6)
        assert_lossless(img, out)
        entries[stem] = {
            "path": f"{SERVED_PREFIX}/{stem}.webp",
            "width": img.size[0],
            "height": img.size[1],
        }
        print(f"  packed {stem:16s} -> {out.relative_to(REPO)}")

    manifest = {
        "frame_width": FRAME_W,
        "frame_height": FRAME_H,
        "cols": COLS,
        "rows": ROWS,
        "trainers": entries,
    }
    (OUT_DIR / "trainers.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"  manifest -> {(OUT_DIR / 'trainers.manifest.json').relative_to(REPO)} ({len(entries)} trainers)")


if __name__ == "__main__":
    pack()
