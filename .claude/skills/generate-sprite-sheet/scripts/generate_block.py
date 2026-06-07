#!/usr/bin/env python3
"""
Generate a painted tile BLOCK (terrain family / scene mockup / animation strip).

This is the generation half of the new tile pipeline (docs/art-style §11). Unlike
generate_sprite.py — which snaps one asset onto one tiny canvas — a block is a
COHERENT multi-tile picture the model paints in one go (so the tiles in it line
up and share colours), kept at full resolution for slice_tileset.py to cut.

  Terrain family (slice into an autotile set):
    generate_block.py --type terrain-block --subject "lush blue-hour meadow grass" \
        --cols 6 --rows 6 --area tinderwick --output /tmp/grass_block.png

  Scene mockup (harvest cohesive fills + decoration):
    generate_block.py --type scene-mockup --subject "blue-hour coastal village green" \
        --cols 12 --rows 8 --area tinderwick --output /tmp/scene.png

  Animation strip (slice into water/lamp frames):
    generate_block.py --type tile-anim --subject "deep blue sea water" \
        --cols 3 --rows 1 --area tinderwick --output /tmp/water_anim.png

Then run slice_tileset.py on the output. Blocks are opaque scenes (no
transparency / chroma-key — that is only for cut-out sprites).
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from generate_sprite import generate_source, load_specs, nearest_aspect  # noqa: E402


def main() -> int:
    specs = load_specs()
    blocks = specs.get("_blocks", {})

    p = argparse.ArgumentParser(description="Generate a painted tile block to slice.")
    p.add_argument("--type", choices=sorted(blocks), required=True, help="Block template.")
    p.add_argument("--subject", required=True, help="What to paint (the terrain / scene / tile).")
    p.add_argument("--output", required=True, help="Output .png (kept at full resolution).")
    p.add_argument("--cols", type=int, required=True, help="Logical tiles across.")
    p.add_argument("--rows", type=int, required=True, help="Logical tiles down.")
    p.add_argument("--tile", type=int, default=16, help="Tile size in px (default 16).")
    p.add_argument("--area", help="Area name (adds the shared area-style cohesion clause).")
    p.add_argument("--palette", help="Shared palette description (with --area).")
    p.add_argument("--provider", choices=["google", "openai"], default="google")
    p.add_argument("--max-retries", type=int, default=2)
    p.add_argument("--reference", action="append", metavar="PATH",
                   help="Reference image for cohesion (repeatable).")
    args = p.parse_args()

    block = blocks[args.type]
    fields = {
        "subject": args.subject.strip(),
        "tile": args.tile,
        "cols": args.cols,
        "rows": args.rows,
        "canvas_w": args.cols * args.tile,
        "canvas_h": args.rows * args.tile,
        "originality": specs["_originality"],
    }
    style = specs["_block_style"].format(**fields)
    body = block["prompt"].format(**fields)
    prompt = f"{style}\n\n{body}"
    if args.area and args.palette and specs.get("_area_style"):
        prompt += "\n\n" + specs["_area_style"].format(area=args.area, palette=args.palette)

    out_path = Path(args.output).expanduser().resolve()
    if out_path.suffix.lower() != ".png":
        p.error("Output must be a .png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    aspect = nearest_aspect(fields["canvas_w"], fields["canvas_h"])
    # Blocks are opaque scenes: no native-transparent request, no chroma-key.
    gen = generate_source(prompt, aspect, provider=args.provider,
                          native_transparent=False, max_retries=args.max_retries,
                          out_png=out_path, references=args.reference)

    print(json.dumps({
        "path": str(out_path),
        "type": args.type,
        "grid": [args.cols, args.rows],
        "tile": args.tile,
        "area": args.area,
        "provider": gen.get("provider") or args.provider,
        "model": gen.get("model"),
        "next": f"slice_tileset.py {out_path} --out <dir> --cols {args.cols} --rows {args.rows}"
                + (f" --quantize-area {args.area}" if args.area else ""),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
