#!/usr/bin/env python3
"""
Tileset packer for PixelKin.

The "code does the layout" half of tileset generation. `generate_sprite.py` makes the
individual 16x16 tiles for an area (see SKILL.md, the tile-set flow); this script packs a
directory of those tiles into a single atlas PNG and emits the tileset METADATA JSON the
game's map loader reads — carrying the per-tile `collides` / `requires_ability` /
`encounter_terrain` / `role` properties that drive collision, ability-gating, and
encounters (see src/game/data/world/types.ts and docs/world/README.md).

Generation (the model) and packing (this script) are intentionally separate, mirroring the
two-system principle in SKILL.md.

Manifest (optional) at <tiles-dir>/tileset.manifest.json controls tile order + properties:

  {
    "name": "tinderwick_set",
    "columns": 8,
    "tiles": [
      { "file": "ground.png", "role": "ground", "encounter_terrain": "tall_grass" },
      { "file": "path.png",   "role": "path" },
      { "file": "wall.png",   "role": "wall",  "collides": true },
      { "file": "water.png",  "role": "water", "collides": true,
        "requires_ability": "tidecall", "encounter_terrain": "water" }
    ]
  }

Without a manifest, every *.png in the directory is packed in sorted order with no
properties (you can add them to the emitted JSON by hand or via a manifest re-run).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image

# Per-tile property keys we carry into the tileset metadata (besides id/file/role).
PROPERTY_KEYS = ("collides", "requires_ability", "encounter_terrain")


def find_repo_root(start: Path) -> Path:
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return start


def load_tiles(tiles_dir: Path, manifest_path: Path) -> tuple[str, int | None, list[dict]]:
    """Return (name, columns_hint, tiles) where tiles are dicts with at least 'file'."""
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text())
        name = manifest.get("name") or f"{tiles_dir.name}_set"
        tiles = manifest.get("tiles", [])
        if not tiles:
            raise SystemExit(f"Manifest {manifest_path} has no 'tiles'.")
        return name, manifest.get("columns"), tiles
    # No manifest: pack every PNG, sorted, with no properties.
    pngs = sorted(p.name for p in tiles_dir.glob("*.png"))
    if not pngs:
        raise SystemExit(f"No .png tiles found in {tiles_dir} and no manifest at {manifest_path}.")
    return f"{tiles_dir.name}_set", None, [{"file": f, "role": Path(f).stem} for f in pngs]


def main() -> int:
    p = argparse.ArgumentParser(description="Pack an area's 16x16 tiles into an atlas + tileset metadata JSON.")
    p.add_argument("--tiles-dir", required=True, help="Directory of generated 16x16 tile PNGs (e.g. assets/tilesets/tinderwick).")
    p.add_argument("--manifest", help="Tile manifest JSON (default <tiles-dir>/tileset.manifest.json).")
    p.add_argument("--name", help="Tileset name (default from manifest, else '<dir>_set').")
    p.add_argument("--columns", type=int, help="Atlas columns (default from manifest, else 8).")
    p.add_argument("--tile-size", type=int, default=16, help="Tile size in px (default 16).")
    p.add_argument("--out-dir", help="Output dir for the atlas + metadata (default public/assets/tilesets).")
    args = p.parse_args()

    tiles_dir = Path(args.tiles_dir).expanduser().resolve()
    if not tiles_dir.is_dir():
        raise SystemExit(f"--tiles-dir not found: {tiles_dir}")
    manifest_path = Path(args.manifest).expanduser().resolve() if args.manifest \
        else tiles_dir / "tileset.manifest.json"

    name, cols_hint, tiles = load_tiles(tiles_dir, manifest_path)
    if args.name:
        name = args.name
    columns = args.columns or cols_hint or 8
    ts = args.tile_size

    repo = find_repo_root(Path.cwd().resolve())
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir \
        else repo / "public" / "assets" / "tilesets"
    out_dir.mkdir(parents=True, exist_ok=True)

    n = len(tiles)
    rows = math.ceil(n / columns)
    atlas = Image.new("RGBA", (columns * ts, rows * ts), (0, 0, 0, 0))

    warnings: list[str] = []
    meta_tiles: list[dict] = []
    for i, tile in enumerate(tiles):
        fpath = tiles_dir / tile["file"]
        if not fpath.is_file():
            raise SystemExit(f"Tile file missing: {fpath}")
        img = Image.open(fpath).convert("RGBA")
        if img.size != (ts, ts):
            warnings.append(f"{tile['file']} is {img.size}, expected {(ts, ts)}; resized (nearest).")
            img = img.resize((ts, ts), Image.NEAREST)
        if img.split()[3].getbbox() is None:
            warnings.append(f"{tile['file']} is fully transparent.")
        col, row = i % columns, i // columns
        atlas.alpha_composite(img, (col * ts, row * ts))
        entry = {"id": i, "file": tile["file"], "role": tile.get("role", Path(tile["file"]).stem)}
        for key in PROPERTY_KEYS:
            if key in tile and tile[key] not in (None, False):
                entry[key] = tile[key]
        meta_tiles.append(entry)

    atlas_path = out_dir / f"{name}.png"
    atlas.save(atlas_path, format="PNG", optimize=True)

    metadata = {
        "name": name,
        "image": f"{name}.png",
        "image_width": columns * ts,
        "image_height": rows * ts,
        "tile_width": ts,
        "tile_height": ts,
        "columns": columns,
        "tile_count": n,
        "tiles": meta_tiles,
    }
    meta_path = out_dir / f"{name}.tileset.json"
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n")

    summary = {
        "atlas": str(atlas_path),
        "metadata": str(meta_path),
        "name": name,
        "tile_count": n,
        "columns": columns,
        "rows": rows,
        "tiles": [{"id": t["id"], "role": t["role"]} for t in meta_tiles],
        "warnings": warnings,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
