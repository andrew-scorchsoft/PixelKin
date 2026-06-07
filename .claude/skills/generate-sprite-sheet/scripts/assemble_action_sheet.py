#!/usr/bin/env python3
"""
Assemble a human action sheet (docs/art-style.md §A2) from individual poses.

Image models are weak at multi-pose grids, so the ROBUST way to build a
`human-actions` sheet is the two-system principle: generate each pose as a single
`human-pose` sprite (reliable), then let CODE lay them out. This script composes
exactly 8 single 32×32 pose PNGs, in cell order, into one 4×2 (128×64) sheet
ready for pack_trainers.py.

Cell order (must match Actor.HUMAN_ACTION_FRAMES):

    0 raise-start  1 raise-hold  2 toss-wind  3 toss-throw
    4 gift-raise   5 gift-cast   6 sit        7 hurt

Each input must already be a 32×32 transparent PNG (the output of
`generate_sprite.py --type human-pose`, which snaps to that canvas, bottom-centre).

Usage (inputs in cell order):

    ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/assemble_action_sheet.py \
      --output assets/trainers/player_indi_actions.png \
      pose0.png pose1.png pose2.png pose3.png pose4.png pose5.png pose6.png pose7.png
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

FRAME = 32
COLS, ROWS = 4, 2
CELLS = COLS * ROWS  # 8


def assemble(inputs: list[str], output: str) -> None:
    if len(inputs) != CELLS:
        raise SystemExit(f"need exactly {CELLS} pose images (cell order), got {len(inputs)}")
    sheet = Image.new("RGBA", (FRAME * COLS, FRAME * ROWS), (0, 0, 0, 0))
    for i, path in enumerate(inputs):
        img = Image.open(path).convert("RGBA")
        if img.size != (FRAME, FRAME):
            raise SystemExit(
                f"FAIL {path}: pose must be {FRAME}x{FRAME} (generate with --type human-pose), "
                f"got {img.size[0]}x{img.size[1]}"
            )
        c, r = i % COLS, i // COLS
        sheet.alpha_composite(img, (c * FRAME, r * FRAME))
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"  assembled {len(inputs)} poses -> {out}  ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Assemble 8 single poses into a 4x2 human action sheet.")
    p.add_argument("poses", nargs="+", help="8 pose PNGs in cell order (32x32 each).")
    p.add_argument("--output", required=True, help="Output action-sheet PNG (128x64).")
    args = p.parse_args()
    assemble(args.poses, args.output)
