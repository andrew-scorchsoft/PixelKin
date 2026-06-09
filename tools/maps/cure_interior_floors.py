#!/usr/bin/env python3
"""
Cure the interior FLOOR masters of their baked per-tile borders, then repack.

The generated floor fills (tiles_warm/tiles_cool floor_fill*.png) carry a baked
vignette + rim that tiles into a visible grid — the same disease the overworld
fills had (the "joints" look, worst on the Lumenary stone). Same cure as the
shared set: tileforge.flatten_vignette (toroidal high-pass, keeps detail + mean)
followed by deborder("fill"). Idempotent — safe to re-run; edits the MASTERS in
assets/tilesets/interior/ and repacks both served sets.

Run:  python3 tools/maps/cure_interior_floors.py
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from tileforge import load, deborder, flatten_vignette

REPO = Path(__file__).resolve().parents[2]
INT = REPO / "assets" / "tilesets" / "interior"
PACK = REPO / ".claude/skills/generate-sprite-sheet/scripts/pack_tileset.py"

for kit in ("tiles_warm", "tiles_cool"):
    for name in ("floor_fill.png", "floor_fill_b.png"):
        p = INT / kit / name
        cured = deborder(flatten_vignette(load(p)), "fill")
        cured.save(p)
        print(f"cured {kit}/{name}")

for kit in ("tiles_warm", "tiles_cool"):
    res = subprocess.run([sys.executable, str(PACK), "--tiles-dir", str(INT / kit)],
                         capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stderr[-800:])
        sys.exit(1)
print("repacked interior_set + interior_stone_set")
