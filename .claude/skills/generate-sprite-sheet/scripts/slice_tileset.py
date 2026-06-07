#!/usr/bin/env python3
"""
Slice a painted tile BLOCK or SCENE into individual 16x16 tiles.

This is the "code does the layout" half of the new tile pipeline (docs/art-style
§11). An image model paints a *coherent* picture — a terrain patch with its
edges/corners, or a top-down area vignette — so neighbouring tiles are mutually
consistent in palette, light and value (which isolated per-tile generation can
never be). This script then cuts that picture onto the 16px grid.

Two modes:

  Grid slice (default) — cut an N x M block into N*M tiles, row-major:
      slice_tileset.py block.png --cols 6 --rows 6 --out assets/tilesets/foo
      slice_tileset.py block.png --cols 3 --rows 3 --terrain grass --layout edges9

  Harvest (--harvest) — slice a scene mockup, drop near-empty and duplicate
  cells, and keep the distinct tiles (good for fill variants + decoration):
      slice_tileset.py scene.png --cols 12 --rows 8 --harvest --out assets/tilesets/foo

The source is usually high-res (the model paints big); it is downscaled
pixel-art-aware to cols*16 x rows*16 before slicing. Pass --quantize-area /
--quantize-colors to snap every tile to a locked palette in the same step.

Outputs PNG tiles (NN_role.png) plus a draft `tileset.manifest.json` you then
hand-tune (set collision, encounter terrain, animation) before pack_tileset.py.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent

# Named autotile layouts: cell (row,col) -> role tag. The model can't reliably
# PAINT a correct 47-blob, but for small, regular arrangements a layout lets the
# slicer tag roles automatically. For anything else, slice generically and let
# the caller assign roles in the manifest.
LAYOUTS: dict[str, dict] = {
    # 3x3 nine-slice: outer corners + edges + centre fill (no inner corners).
    "edges9": {
        "cols": 3, "rows": 3,
        "roles": [
            "corner_nw", "edge_n", "corner_ne",
            "edge_w", "fill", "edge_e",
            "corner_sw", "edge_s", "corner_se",
        ],
    },
    # A horizontal A->B transition strip: pure A, the edge, pure B.
    "transition3": {"cols": 3, "rows": 1, "roles": ["fill_a", "edge", "fill_b"]},
    # An animation row: successive frames of one tile (water ripple, etc.).
    "anim4": {"cols": 4, "rows": 1, "roles": ["frame0", "frame1", "frame2", "frame3"]},
    "anim3": {"cols": 3, "rows": 1, "roles": ["frame0", "frame1", "frame2"]},
}


def resize_rgba_premul(src: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Downscale on premultiplied alpha so transparent RGB doesn't halo edges."""
    src = src.convert("RGBA")
    try:
        import numpy as np
    except ImportError:
        return src.resize(size, Image.LANCZOS)
    arr = np.asarray(src).astype(np.float32)
    a = arr[..., 3:4] / 255.0
    pm = np.concatenate([arr[..., :3] * a, arr[..., 3:4]], axis=-1).astype("uint8")
    resized = Image.fromarray(pm, "RGBA").resize(size, Image.LANCZOS)
    out = np.asarray(resized).astype(np.float32)
    oa = out[..., 3:4] / 255.0
    safe = np.where(oa > 0, oa, 1.0)
    rgb = np.clip(out[..., :3] / safe, 0, 255)
    return Image.fromarray(np.concatenate([rgb, out[..., 3:4]], axis=-1).astype("uint8"), "RGBA")


def tile_signature(tile: Image.Image, buckets: int = 6) -> tuple:
    """A coarse fingerprint for dedupe: downsample to 4x4 and bucket each channel."""
    small = tile.convert("RGBA").resize((4, 4), Image.BOX)
    px = list(small.getdata())
    step = 256 // buckets
    return tuple(
        (r // step, g // step, b // step, 1 if a > 32 else 0) for (r, g, b, a) in px
    )


def opaque_fraction(tile: Image.Image) -> float:
    a = tile.convert("RGBA").split()[3]
    px = list(a.getdata())
    return sum(1 for v in px if v > 32) / max(1, len(px))


def main() -> int:
    p = argparse.ArgumentParser(description="Slice a painted block/scene into 16x16 tiles.")
    p.add_argument("image", help="The painted block or scene PNG.")
    p.add_argument("--out", required=True, help="Output directory for tiles + manifest.")
    p.add_argument("--cols", type=int, help="Tiles across (required unless --layout sets it).")
    p.add_argument("--rows", type=int, help="Tiles down (required unless --layout sets it).")
    p.add_argument("--tile", type=int, default=16, help="Tile size in px (default 16).")
    p.add_argument("--terrain", help="Terrain group tag written into the manifest (e.g. grass).")
    p.add_argument("--layout", choices=sorted(LAYOUTS), help="Tag cells using a named autotile layout.")
    p.add_argument("--harvest", action="store_true",
                   help="Drop near-empty and duplicate cells; keep the distinct tiles.")
    p.add_argument("--min-opaque", type=float, default=0.08,
                   help="In --harvest, skip tiles less than this opaque fraction (default 0.08).")
    p.add_argument("--quantize-area", help="Snap each tile to areas.<AREA>.working_palette.")
    p.add_argument("--quantize-colors", help="Snap each tile to this comma-separated #rrggbb list.")
    p.add_argument("--name", help="Manifest set name (default: out dir name + _set).")
    args = p.parse_args()

    layout = LAYOUTS[args.layout] if args.layout else None
    cols = args.cols or (layout["cols"] if layout else None)
    rows = args.rows or (layout["rows"] if layout else None)
    if not cols or not rows:
        p.error("Provide --cols and --rows (or a --layout that defines them).")
    roles = list(layout["roles"]) if layout else None

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    t = args.tile

    src = Image.open(args.image).convert("RGBA")
    src = resize_rgba_premul(src, (cols * t, rows * t))

    # Optional palette snap, reusing the quantiser.
    palette = None
    if args.quantize_area or args.quantize_colors:
        sys.path.insert(0, str(SCRIPT_DIR))
        from quantize_to_palette import load_palette, quantize_image  # type: ignore

        class _A:  # tiny shim for load_palette's expected attrs
            area = args.quantize_area
            ramp = None
            colors = args.quantize_colors
        palette = load_palette(_A())

    manifest_tiles = []
    seen: dict[tuple, str] = {}
    written = 0
    for r in range(rows):
        for c in range(cols):
            cell = src.crop((c * t, r * t, (c + 1) * t, (r + 1) * t))
            if palette is not None:
                from quantize_to_palette import quantize_image  # type: ignore
                cell = quantize_image(cell, palette)

            if args.harvest:
                if opaque_fraction(cell) < args.min_opaque:
                    continue
                sig = tile_signature(cell)
                if sig in seen:
                    continue
                seen[sig] = "kept"

            role = roles[r * cols + c] if roles and r * cols + c < len(roles) else "tile"
            fname = f"{written:02d}_{role}.png"
            cell.save(out_dir / fname, format="PNG", optimize=True)
            entry: dict = {"file": fname, "role": role}
            if args.terrain:
                entry["terrain"] = args.terrain
            if roles:
                entry["autotile"] = role
            manifest_tiles.append(entry)
            written += 1

    set_name = args.name or (out_dir.name + "_set")
    manifest = {"name": set_name, "columns": 8, "tiles": manifest_tiles}
    (out_dir / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    print(json.dumps({
        "image": args.image,
        "out": str(out_dir),
        "grid": [cols, rows],
        "tiles_written": written,
        "harvested": bool(args.harvest),
        "layout": args.layout,
        "terrain": args.terrain,
        "quantized": bool(palette),
        "manifest": str(out_dir / "tileset.manifest.json"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
