#!/usr/bin/env python3
"""Pack the Hartway's two picture reels (the `frames` op with captions, content/regions/
hartway.ts): assets/backgrounds/cinematic/hartway/{ridge-1..3,mist-1..5}.webp (image-gen
masters; ridge-2 and mist-2..5 are EDITS of ridge-1 / mist-1 so the view holds still while
the story moves) -> public/assets/backgrounds/cinematic/hartway-<name>.webp at 240x160.

    python3 tools/assets/pack_hartway_frames.py
"""
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "assets/backgrounds/cinematic/hartway"
OUT = REPO / "public/assets/backgrounds/cinematic"
for src in sorted(SRC.glob("*.webp")):
    im = Image.open(src).convert("RGB").resize((240, 160), Image.LANCZOS)
    im.save(OUT / f"hartway-{src.stem}.webp", "WEBP", quality=90, method=6)
    print(f"hartway-{src.stem}.webp")
