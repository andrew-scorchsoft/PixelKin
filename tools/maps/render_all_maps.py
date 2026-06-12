#!/usr/bin/env python3
"""
Batch-render all maps in public/assets/maps/ to WebP for documentation.
Outputs to docs/maps/renders/<mapid>.webp at scale 2.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent.parent
RENDER_SCRIPT = REPO / ".claude/skills/generate-sprite-sheet/scripts/render_map.py"
MAPS_DIR = REPO / "public/assets/maps"
OUT_DIR = REPO / "docs/maps/renders"
PYTHON = sys.executable

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    maps = sorted(MAPS_DIR.glob("*.json"))
    print(f"Rendering {len(maps)} maps to {OUT_DIR} ...")

    ok, failed = [], []
    for mp in maps:
        map_id = mp.stem
        tmp_png = OUT_DIR / f"{map_id}.png"
        out_webp = OUT_DIR / f"{map_id}.webp"

        result = subprocess.run(
            [PYTHON, str(RENDER_SCRIPT), str(mp), "--output", str(tmp_png), "--scale", "2"],
            capture_output=True, text=True, cwd=str(REPO),
        )
        if result.returncode != 0 or not tmp_png.is_file():
            print(f"  FAIL {map_id}: {result.stderr.strip()}")
            failed.append(map_id)
            continue

        # Convert PNG -> WebP and remove the PNG
        from PIL import Image
        img = Image.open(tmp_png).convert("RGB")
        img.save(out_webp, format="WEBP", quality=85, method=4)
        tmp_png.unlink()

        meta = json.loads(result.stdout) if result.stdout.strip() else {}
        size = meta.get("size", [0, 0])
        missing = meta.get("missing_atlas", [])
        warn = f" (missing: {missing})" if missing else ""
        print(f"  ok  {map_id:40s} {size[0]}×{size[1]}{warn}")
        ok.append(map_id)

    print(f"\nDone: {len(ok)} rendered, {len(failed)} failed.")
    if failed:
        print("Failed:", failed)
        sys.exit(1)

if __name__ == "__main__":
    main()
