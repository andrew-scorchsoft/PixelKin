#!/usr/bin/env python3
"""Pack the Rolling Thunder reel (the Rio Tower's Thunder Table, `frames` op):
assets/backgrounds/cinematic/thunder/{base,f2..f6}.webp (image-gen masters, 1264x848,
each an edit of `base` so the composition holds still while the storm rolls)
-> public/assets/backgrounds/cinematic/thunder-1..6.webp at 240x160.

    python3 tools/assets/pack_thunder_frames.py
"""
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "assets/backgrounds/cinematic/thunder"
OUT = REPO / "public/assets/backgrounds/cinematic"
for n, stem in enumerate(["base", "f2", "f3", "f4", "f5", "f6"], start=1):
    im = Image.open(SRC / f"{stem}.webp").convert("RGB").resize((240, 160), Image.LANCZOS)
    im.save(OUT / f"thunder-{n}.webp", "WEBP", quality=90, method=6)
    print(f"thunder-{n}.webp <- {stem}")
