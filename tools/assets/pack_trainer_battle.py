#!/usr/bin/env python3
"""
pack_trainer_battle.py — trainer battle sprite masters -> served WebP + key list.

  assets/trainers/battle/<key>.png  (64×64 masters, see briefs.json there)
    -> public/assets/sprites/trainer_battle/<key>.webp   (lossless, HARD alpha)
    -> src/game/data/trainer-battle.json                 (the keys PreloadScene loads)

Image-gen output carries soft alpha (gpt-image tops out at ~253); the battle screen
is crisp pixel art, so alpha is snapped to 0/255 at 128. Idempotent; run after any
master changes. `--check` exits 1 if the served set or key list is stale (CI-friendly).
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MASTERS = ROOT / "assets/trainers/battle"
SERVED = ROOT / "public/assets/sprites/trainer_battle"
KEYS = ROOT / "src/game/data/trainer-battle.json"


def packed(png: Path) -> bytes:
    im = Image.open(png).convert("RGBA")
    if im.size != (64, 64):
        raise SystemExit(f"{png.name}: {im.size}, expected 64x64")
    a = np.array(im)
    a[..., 3] = np.where(a[..., 3] >= 128, 255, 0).astype(np.uint8)
    a[a[..., 3] == 0] = 0
    buf = io.BytesIO()
    Image.fromarray(a).save(buf, "WEBP", lossless=True, quality=100, method=6)
    return buf.getvalue()


def main() -> int:
    check = "--check" in sys.argv
    masters = sorted(MASTERS.glob("*.png"))
    keys = [p.stem for p in masters]
    stale = []
    SERVED.mkdir(parents=True, exist_ok=True)
    for p in masters:
        data = packed(p)
        out = SERVED / f"{p.stem}.webp"
        if not out.exists() or out.read_bytes() != data:
            stale.append(out.name)
            if not check:
                out.write_bytes(data)
    text = json.dumps({"keys": keys}, indent=1) + "\n"
    if not KEYS.exists() or KEYS.read_text() != text:
        stale.append(KEYS.name)
        if not check:
            KEYS.write_text(text)
    if check:
        if stale:
            print("STALE trainer battle sprites:", ", ".join(stale))
            return 1
        print(f"trainer battle sprites current ({len(keys)})")
        return 0
    print(f"packed {len(keys)} trainer battle sprites ({len(stale)} written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
