#!/usr/bin/env python3
"""
Tileset packer for PixelKin.

The "code does the layout" half of tileset generation. `generate_sprite.py` makes the
individual 16x16 tiles for an area (see SKILL.md, the tile-set flow); this script packs a
directory of those tiles into a single atlas image and emits the tileset SIDECAR JSON the
game's map loader reads.

Output contract — MUST satisfy `PackedTileset` in src/game/systems/world/tileset.ts:

    PackedTileset {
      name: string;
      image: string;          // served path, e.g. "assets/tilesets/tinderwick_set.webp"
      tile_width: number; tile_height: number;
      columns: number; tile_count: number;
      tiles: TileMeta[];      // SPARSE — only tiles with non-default behaviour
    }
    TileMeta {
      index: number;          // LOCAL 0-based tile index, row-major
      role?: string;
      collides?: boolean;
      encounter_terrain?: 'tall_grass'|'water'|'cave'|'sand';
      requires_ability?: 'glimmerstep'|'tidecall'|'emberward'|'updraft_kite'|'sunsketch'|'starreach';
      animation?: { frames: number[]; duration_ms: number };  // frames are LOCAL indices
    }

The atlas image is written as a LOSSLESS WebP to public/assets/tilesets/<name>.webp.
Lossless is mandatory: lossy WebP destroys the crisp 1px pixel-art edges the art bible
requires. The packer verifies the WebP round-trips byte-for-byte identical to the source
composite (decoded RGBA arrays compared) and fails loudly if it does not.

Generation (the model) and packing (this script) are intentionally separate, mirroring the
two-system principle in SKILL.md.

Manifest (recommended) at <tiles-dir>/tileset.manifest.json controls tile order + behaviour:

  {
    "name": "tinderwick_set",
    "columns": 8,
    "tiles": [
      { "file": "ground.png", "role": "ground", "encounter_terrain": "tall_grass" },
      { "file": "path.png",   "role": "path" },
      { "file": "wall.png",   "role": "wall",  "collides": true },
      { "file": "water.png",  "role": "water", "collides": true,
        "requires_ability": "tidecall", "encounter_terrain": "water",
        "animation": { "frames": [3, 11, 12], "duration_ms": 600 } }
    ]
  }

Tile ORDER in the manifest fixes the LOCAL index (0-based, row-major). A map JSON's gids
map to these indices via `gid - first_gid`. `animation.frames` are local indices too —
they may reference extra frame tiles packed later in the set.

Without a manifest, every *.png in the directory is packed in sorted order with no
behaviour (a bare passable visual set).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image

# Canonical enum values from src/game/data/world/types.ts — validated so a typo in a
# manifest fails here rather than silently producing a tile the engine ignores.
ENCOUNTER_TERRAINS = {"tall_grass", "water", "cave", "sand"}
ABILITIES = {"glimmerstep", "tidecall", "emberward", "updraft_kite", "sunsketch", "starreach"}


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


def build_tile_meta(index: int, tile: dict, n_tiles: int, warnings: list[str]) -> dict | None:
    """Build a sparse TileMeta entry for one tile, or None if it has all-default behaviour.

    The sidecar `tiles` list is SPARSE: a tile that is passable, non-encounter, ungated,
    static and unanimated contributes nothing (the engine defaults it). A `role` alone is
    informational and does NOT force an entry — but we keep it if any real behaviour or an
    explicit role is present, since roles aid debugging the atlas.
    """
    entry: dict = {"index": index}
    has_behaviour = False

    role = tile.get("role")
    if role:
        entry["role"] = role

    # Autotile tagging (informational at runtime; read by tools/autotile to expand
    # a map's terrain layer into the right blob tile). `terrain` = which material
    # group this tile belongs to; `autotile` = its role in that group's blob set
    # (fill / edge_n / corner_nw / inner_ne / ...). See docs/art-style.md §11.
    terrain_group = tile.get("terrain")
    if terrain_group:
        entry["terrain"] = terrain_group
    autotile = tile.get("autotile")
    if autotile:
        entry["autotile"] = autotile

    if tile.get("collides") is True:
        entry["collides"] = True
        has_behaviour = True

    terrain = tile.get("encounter_terrain")
    if terrain not in (None, False):
        if terrain not in ENCOUNTER_TERRAINS:
            raise SystemExit(
                f"Tile #{index} ({tile.get('file')}): encounter_terrain '{terrain}' is not "
                f"one of {sorted(ENCOUNTER_TERRAINS)}."
            )
        entry["encounter_terrain"] = terrain
        has_behaviour = True

    ability = tile.get("requires_ability")
    if ability not in (None, False):
        if ability not in ABILITIES:
            raise SystemExit(
                f"Tile #{index} ({tile.get('file')}): requires_ability '{ability}' is not "
                f"one of {sorted(ABILITIES)}."
            )
        entry["requires_ability"] = ability
        has_behaviour = True

    anim = tile.get("animation")
    if anim not in (None, False):
        frames = anim.get("frames")
        duration = anim.get("duration_ms")
        if not isinstance(frames, list) or not frames or not all(isinstance(f, int) for f in frames):
            raise SystemExit(
                f"Tile #{index} ({tile.get('file')}): animation.frames must be a non-empty "
                f"list of integer local indices."
            )
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise SystemExit(
                f"Tile #{index} ({tile.get('file')}): animation.duration_ms must be a positive number."
            )
        bad = [f for f in frames if f < 0 or f >= n_tiles]
        if bad:
            raise SystemExit(
                f"Tile #{index} ({tile.get('file')}): animation.frames {bad} are out of range "
                f"(set has {n_tiles} tiles, valid indices 0..{n_tiles - 1})."
            )
        entry["animation"] = {"frames": frames, "duration_ms": duration}
        has_behaviour = True

    # Keep the entry if it carries real behaviour OR an explicit role/terrain tag.
    if has_behaviour or role or terrain_group or autotile:
        return entry
    return None


def verify_lossless(atlas: Image.Image, webp_path: Path) -> None:
    """Decode the written WebP and assert it is VISUALLY lossless vs the composite.

    "Visually lossless" = the alpha channel matches everywhere, and RGB matches
    everywhere alpha > 0. RGB *under* fully-transparent pixels (alpha == 0) is
    never rendered, and lossless WebP is free to store any value there — comparing
    it would produce false failures. What matters for crisp pixel art is that every
    visible pixel round-trips exactly, which this checks.
    """
    decoded = Image.open(webp_path).convert("RGBA")
    src = atlas.convert("RGBA")
    if decoded.size != src.size:
        raise SystemExit(
            f"WebP verification FAILED for {webp_path}: size {decoded.size} != source {src.size}."
        )
    try:
        import numpy as np  # type: ignore
        a = np.asarray(src)
        b = np.asarray(decoded)
        if not np.array_equal(a[..., 3], b[..., 3]):
            raise SystemExit(
                f"WebP lossless verification FAILED for {webp_path}: alpha channel differs "
                f"(not lossless — crisp edges at risk)."
            )
        visible = a[..., 3] > 0
        if not np.array_equal(a[..., :3][visible], b[..., :3][visible]):
            raise SystemExit(
                f"WebP lossless verification FAILED for {webp_path}: visible RGB differs from "
                f"the source composite. Refusing to ship a lossy atlas (crisp pixel edges lost)."
            )
    except ImportError:
        # numpy missing: compare per-pixel, ignoring RGB under alpha==0.
        sp = list(src.getdata())
        dp = list(decoded.getdata())
        for (sr, sg, sb, sa), (dr, dg, db, da) in zip(sp, dp):
            if sa != da or (sa > 0 and (sr, sg, sb) != (dr, dg, db)):
                raise SystemExit(
                    f"WebP lossless verification FAILED for {webp_path}: a visible pixel differs."
                )


def main() -> int:
    p = argparse.ArgumentParser(
        description="Pack an area's 16x16 tiles into a lossless-WebP atlas + PackedTileset sidecar JSON."
    )
    p.add_argument("--tiles-dir", required=True,
                   help="Directory of generated 16x16 tile PNGs (e.g. assets/tilesets/tinderwick).")
    p.add_argument("--manifest", help="Tile manifest JSON (default <tiles-dir>/tileset.manifest.json).")
    p.add_argument("--name", help="Tileset name (default from manifest, else '<dir>_set').")
    p.add_argument("--columns", type=int, help="Atlas columns (default from manifest, else 8).")
    p.add_argument("--tile-size", type=int, default=16, help="Tile size in px (default 16).")
    p.add_argument("--out-dir", help="Output dir for the atlas + sidecar (default public/assets/tilesets).")
    p.add_argument("--image-prefix", default="assets/tilesets",
                   help="Served path prefix recorded in the sidecar 'image' field "
                        "(default 'assets/tilesets'; vite drops the public/ prefix at runtime).")
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
        if "file" not in tile:
            raise SystemExit(f"Tile #{i} in manifest has no 'file'.")
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
        meta = build_tile_meta(i, tile, n, warnings)
        if meta is not None:
            meta_tiles.append(meta)

    # Write the LOSSLESS WebP atlas (method=6 = best compression effort, still lossless).
    atlas_path = out_dir / f"{name}.webp"
    atlas.save(atlas_path, format="WEBP", lossless=True, quality=100, method=6)
    verify_lossless(atlas, atlas_path)

    image_ref = f"{args.image_prefix.rstrip('/')}/{name}.webp"
    metadata = {
        "name": name,
        "image": image_ref,
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
        "atlas_format": "webp-lossless",
        "lossless_verified": True,
        "sidecar": str(meta_path),
        "name": name,
        "image": image_ref,
        "tile_count": n,
        "columns": columns,
        "rows": rows,
        "behaviour_tiles": len(meta_tiles),
        "tiles": meta_tiles,
        "warnings": warnings,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
