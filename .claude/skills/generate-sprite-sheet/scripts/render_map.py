#!/usr/bin/env python3
"""
Composite an authored map into a PNG for visual QA — no browser needed.

A map is gid layers over packed tilesets (docs/world). To judge whether a map
meets the handheld-era quality bar (clean terrain borders, varied fills,
decoration, depth) you need to SEE it. This renders the map exactly as the engine
stacks it: each layer's gids cropped from its atlas and composited in depth
order. Animated tiles show their base frame.

Usage:
  render_map.py public/assets/maps/tinderwick.json --output /tmp/tinderwick.png --scale 4
  render_map.py tinderwick --output /tmp/t.png            # bare id -> public/assets/maps/<id>.json
  render_map.py <map> --layer deco                        # one layer in isolation
  render_map.py <map> --no-above                          # composite without the over-player layer
  render_map.py <map> --grid                              # overlay the 16px tile grid
  render_map.py <map> --list-layers                       # list layers and exit

This is the map-level twin of validate_sprites.py's by-eye check (docs/art-style
§15): a standing gate before a map is called done.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

SCRIPT_DIR = Path(__file__).resolve().parent


def find_repo_root(start: Path) -> Path:
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return start


def resolve_map(arg: str, repo: Path) -> Path:
    p = Path(arg)
    if p.is_file():
        return p
    cand = repo / "public" / "assets" / "maps" / f"{arg}.json"
    if cand.is_file():
        return cand
    raise SystemExit(f"Map not found: {arg} (tried {p} and {cand})")


def served_path(repo: Path, image: str) -> Path:
    """A map/tileset 'assets/...' path resolves under public/ at build time."""
    rel = image[len("public/"):] if image.startswith("public/") else image
    return repo / "public" / rel


def load_atlas(repo: Path, image: str) -> Image.Image | None:
    path = served_path(repo, image)
    if not path.is_file():
        return None
    return Image.open(path).convert("RGBA")


def main() -> int:
    p = argparse.ArgumentParser(description="Composite a map to a PNG for QA.")
    p.add_argument("map", help="Path to a map JSON, or a bare map id under public/assets/maps/.")
    p.add_argument("--output", help="Output PNG (default /tmp/<mapid>.png).")
    p.add_argument("--scale", type=int, default=4, help="Integer upscale, nearest (default 4).")
    p.add_argument("--layer", help="Render only the layer with this name.")
    p.add_argument("--no-above", action="store_true", help="Skip 'above' (over-player) layers.")
    p.add_argument("--grid", action="store_true", help="Overlay the 16px tile grid.")
    p.add_argument("--list-layers", action="store_true", help="List the map's layers and exit.")
    args = p.parse_args()

    repo = find_repo_root(Path.cwd().resolve())
    map_path = resolve_map(args.map, repo)
    m = json.loads(map_path.read_text())

    width, height = m["width"], m["height"]
    tw = m.get("tile_width", 16)
    th = m.get("tile_height", 16)

    layers = m.get("layers", [])
    if args.list_layers:
        for ly in sorted(layers, key=lambda x: x.get("depth", 0)):
            print(f"{ly['name']:<14} role={ly.get('role','?'):<10} depth={ly.get('depth',0)}")
        return 0

    # Build a gid -> (atlas, sx, sy, tile_w, tile_h) resolver from the tilesets.
    sets = []
    for ref in m["tilesets"]:
        atlas = load_atlas(repo, ref["image"])
        sets.append({
            "first_gid": ref["first_gid"],
            "count": ref["tile_count"],
            "columns": ref["columns"],
            "tw": ref.get("tile_width", tw),
            "th": ref.get("tile_height", th),
            "atlas": atlas,
            "name": ref["name"],
        })

    missing = [s["name"] for s in sets if s["atlas"] is None]
    if missing:
        print(f"warning: no atlas image for tileset(s) {missing}; "
              f"those tiles render as magenta placeholders.", file=sys.stderr)

    def blit_gid(canvas: Image.Image, gid: int, tx: int, ty: int) -> None:
        for s in sets:
            if s["first_gid"] <= gid < s["first_gid"] + s["count"]:
                local = gid - s["first_gid"]
                dx, dy = tx * tw, ty * th
                if s["atlas"] is None:
                    canvas.paste((255, 0, 255, 255), (dx, dy, dx + tw, dy + th))
                    return
                cx = (local % s["columns"]) * s["tw"]
                cy = (local // s["columns"]) * s["th"]
                tile = s["atlas"].crop((cx, cy, cx + s["tw"], cy + s["th"]))
                canvas.alpha_composite(tile, (dx, dy))
                return

    canvas = Image.new("RGBA", (width * tw, height * th), (0, 0, 0, 0))
    drawn = []
    for ly in sorted(layers, key=lambda x: x.get("depth", 0)):
        if ly.get("role") == "collision":
            continue
        if args.layer and ly["name"] != args.layer:
            continue
        if args.no_above and ly.get("role") == "above":
            continue
        data = ly["data"]
        for ty in range(height):
            for tx in range(width):
                gid = data[ty * width + tx]
                if gid and gid > 0:
                    blit_gid(canvas, gid, tx, ty)
        drawn.append(ly["name"])

    # Whole-structure objects (buildings, trees, lamps): composite each sprite at
    # its tile position over the ground (art-style §14b). Skipped if --layer isolates one.
    if not args.layer:
        for obj in m.get("objects", []):
            sp = served_path(repo, f"assets/sprites/objects/{obj['sprite']}.webp")
            if not sp.is_file():
                continue
            img = Image.open(sp).convert("RGBA")
            canvas.alpha_composite(img, (obj["at"]["tx"] * tw, obj["at"]["ty"] * th))

    # Flatten onto night-blue so transparency reads like the in-game backdrop.
    bg = Image.new("RGBA", canvas.size, (11, 16, 38, 255))
    bg.alpha_composite(canvas)
    out = bg.convert("RGB")

    if args.scale and args.scale > 1:
        out = out.resize((out.width * args.scale, out.height * args.scale), Image.NEAREST)

    if args.grid:
        d = ImageDraw.Draw(out)
        step_x, step_y = tw * args.scale, th * args.scale
        for x in range(0, out.width, step_x):
            d.line([(x, 0), (x, out.height)], fill=(255, 255, 255), width=1)
        for y in range(0, out.height, step_y):
            d.line([(0, y), (out.width, y)], fill=(255, 255, 255), width=1)

    out_path = Path(args.output) if args.output else Path("/tmp") / f"{m.get('id','map')}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path, format="PNG")
    print(json.dumps({
        "map": str(map_path),
        "output": str(out_path),
        "size": [out.width, out.height],
        "scale": args.scale,
        "layers_drawn": drawn,
        "missing_atlas": missing,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
