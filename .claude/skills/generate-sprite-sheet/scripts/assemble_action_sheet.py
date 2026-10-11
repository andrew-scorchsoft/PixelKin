#!/usr/bin/env python3
"""
Assemble a human action sheet (docs/art-style.md §A2) from individual poses.

Image models are weak at multi-pose grids, so the ROBUST way to build a
`human-actions` sheet is the two-system principle: generate each pose as a single
`human-pose` sprite (reliable), then let CODE lay them out. This script composes
16 single 32×32 pose PNGs, in cell order, into one 4×4 (128×128) sheet ready for
pack_trainers.py. (Exactly 8 poses still builds the legacy 4×2 / 128×64 sheet —
the engine plays the first five actions from it and no-ops the acting poses.)

Cell order (must match Actor.HUMAN_ACTION_FRAMES):

    0 raise-start  1 raise-hold  2 toss-wind  3 toss-throw
    4 gift-raise   5 gift-cast   6 sit        7 hurt
    8 bow-nod      9 bow-deep   10 laugh     11 laugh-belly
   12 shock       13 sad        14 kneel     15 turn-away

Each input must already be a 32×32 transparent PNG (the output of
`generate_sprite.py --type human-pose`, which snaps to that canvas, bottom-centre).

Usage (inputs in cell order):

    ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/assemble_action_sheet.py \
      --output assets/trainers/player_indi_actions.png \
      pose00.png pose01.png ... pose15.png
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

FRAME = 32
COLS = 4
CELLS = 16          # the 4×4 acting sheet (2026-10)
LEGACY_CELLS = 8    # the original 4×2 sheet


def assemble(inputs: list[str], output: str) -> None:
    if len(inputs) not in (CELLS, LEGACY_CELLS):
        raise SystemExit(f"need exactly {CELLS} (or legacy {LEGACY_CELLS}) pose images "
                         f"in cell order, got {len(inputs)}")
    rows = len(inputs) // COLS
    sheet = Image.new("RGBA", (FRAME * COLS, FRAME * rows), (0, 0, 0, 0))
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
    p = argparse.ArgumentParser(description="Assemble 16 single poses into a 4x4 human action sheet.")
    p.add_argument("poses", nargs="+", help="16 (or legacy 8) pose PNGs in cell order (32x32 each).")
    p.add_argument("--output", required=True, help="Output action-sheet PNG (128x128; 128x64 legacy).")
    args = p.parse_args()
    assemble(args.poses, args.output)
