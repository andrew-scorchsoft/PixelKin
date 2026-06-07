#!/usr/bin/env python3
"""
Character sprite packer for PixelKin (walk sheets + optional action sheets +
the shared emote sheet).

The "code does the layout" half of character-sprite generation, mirroring
pack_creatures.py / pack_tileset.py. Characters animate from up to three sheets,
all on the same 32×32 grid (docs/art-style.md §A / §A2 / §A3):

  Layer 1 — walk sheet     assets/trainers/<stem>.png          4×4 (128×128)  REQUIRED per character
  Layer 3 — action sheet   assets/trainers/<stem>_actions.png  4×2 (128×64)   OPTIONAL per character
  Layer 2 — emote sheet    assets/effects/emotes.png           4×2 (128×64)   ONE shared sheet, all characters

This script packs each master into a served, lossless-WebP spritesheet plus one
manifest the game loads.

Source (read-only masters, NOT served):

    assets/trainers/<stem>.png          # walk sheet, e.g. player_indi.png
    assets/trainers/<stem>_actions.png  # optional action sheet, e.g. player_indi_actions.png
    assets/effects/emotes.png           # the one shared emote/bubble sheet

Output (served — vite drops the public/ prefix at runtime):

    public/assets/sprites/trainers/<stem>.webp
    public/assets/sprites/trainers/<stem>_actions.webp   (if a master exists)
    public/assets/sprites/trainers/emotes.webp           (if a master exists)
    public/assets/sprites/trainers/trainers.manifest.json

Manifest shape (consumed by PreloadScene). Top-level frame_width/height/cols/rows
describe the walk sheets (back-compat); action/emote sheets carry their own grid:

  {
    "frame_width": 32, "frame_height": 32, "cols": 4, "rows": 4,
    "trainers": {
      "player_indi": {
        "path": "assets/sprites/trainers/player_indi.webp", "width": 128, "height": 128,
        "actions": { "path": "assets/sprites/trainers/player_indi_actions.webp",
                     "width": 128, "height": 64, "cols": 4, "rows": 2 }
      },
      "professor_fenn": { "path": "...professor_fenn.webp", "width": 128, "height": 128 }
    },
    "emotes": { "path": "assets/sprites/trainers/emotes.webp",
                "width": 128, "height": 64, "cols": 4, "rows": 2 }
  }

WebP is written LOSSLESS (lossless=True, quality=100, method=6) — lossy WebP
destroys the crisp 1px pixel-art edges. Each written file is decoded and asserted
to round-trip visually identical to its source, failing loudly otherwise.

Run from the repo root (no args packs everything):

    ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_trainers.py
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops

# Frame canvas (docs/art-style.md §4). Walk = 4×4, action/emote = 4×2.
FRAME_W, FRAME_H = 32, 32
WALK_COLS, WALK_ROWS = 4, 4
WALK_W, WALK_H = FRAME_W * WALK_COLS, FRAME_H * WALK_ROWS   # 128×128
ACTION_COLS, ACTION_ROWS = 4, 2
ACTION_W, ACTION_H = FRAME_W * ACTION_COLS, FRAME_H * ACTION_ROWS  # 128×64
EMOTE_COLS, EMOTE_ROWS = 4, 2
EMOTE_W, EMOTE_H = FRAME_W * EMOTE_COLS, FRAME_H * EMOTE_ROWS      # 128×64

ACTIONS_SUFFIX = "_actions"

REPO = Path(__file__).resolve().parents[4]
SRC_DIR = REPO / "assets" / "trainers"
EMOTE_SRC = REPO / "assets" / "effects" / "emotes.png"
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


def pack_sheet(master: Path, expect: tuple[int, int], hint: str) -> dict:
    """Load a master, assert its size, write a lossless WebP, return a manifest entry."""
    img = Image.open(master).convert("RGBA")
    if img.size != expect:
        raise SystemExit(
            f"FAIL {master.name}: expected {expect[0]}x{expect[1]} {hint}, got "
            f"{img.size[0]}x{img.size[1]} (see docs/art-style.md §A)"
        )
    out = OUT_DIR / f"{master.stem}.webp"
    img.save(out, "WEBP", lossless=True, quality=100, method=6)
    assert_lossless(img, out)
    return {
        "path": f"{SERVED_PREFIX}/{master.stem}.webp",
        "width": img.size[0],
        "height": img.size[1],
    }


def pack() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Walk sheets are every trainer master that isn't an action sheet.
    walk_masters = sorted(
        p for p in SRC_DIR.glob("*.png") if not p.stem.endswith(ACTIONS_SUFFIX)
    )
    if not walk_masters:
        raise SystemExit(f"No trainer walk-sheet masters found in {SRC_DIR}")

    entries: dict[str, dict] = {}
    for master in walk_masters:
        stem = master.stem
        entries[stem] = pack_sheet(master, (WALK_W, WALK_H), "4x4 walk sheet")
        print(f"  packed {stem:22s} -> {(OUT_DIR / f'{stem}.webp').relative_to(REPO)}")

        # Optional layer-3 action sheet for this character.
        action_master = SRC_DIR / f"{stem}{ACTIONS_SUFFIX}.png"
        if action_master.exists():
            a = pack_sheet(action_master, (ACTION_W, ACTION_H), "4x2 action sheet")
            a.update(cols=ACTION_COLS, rows=ACTION_ROWS)
            entries[stem]["actions"] = a
            print(f"  packed {action_master.stem:22s} -> {(OUT_DIR / f'{action_master.stem}.webp').relative_to(REPO)}")

    manifest: dict = {
        "frame_width": FRAME_W,
        "frame_height": FRAME_H,
        "cols": WALK_COLS,
        "rows": WALK_ROWS,
        "trainers": entries,
    }

    # Layer-2 shared emote sheet (one for the whole game).
    if EMOTE_SRC.exists():
        e = pack_sheet(EMOTE_SRC, (EMOTE_W, EMOTE_H), "4x2 emote sheet")
        e.update(cols=EMOTE_COLS, rows=EMOTE_ROWS)
        manifest["emotes"] = e
        print(f"  packed {'emotes':22s} -> {(OUT_DIR / 'emotes.webp').relative_to(REPO)}")
    else:
        print(f"  (no shared emote sheet at {EMOTE_SRC.relative_to(REPO)} — skipped)")

    (OUT_DIR / "trainers.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"  manifest -> {(OUT_DIR / 'trainers.manifest.json').relative_to(REPO)} "
          f"({len(entries)} trainers)")


if __name__ == "__main__":
    pack()
