#!/usr/bin/env python3
"""
Shared map-builder toolkit for PixelKin overworld maps.

The convention the maps follow now: a map does NOT bake its own atlas. It REFERENCES
the shared `vesper_overworld_set` (built by build_shared_overworld.py) by name + first_gid
and paints terrain layers; the engine resolves gids across tilesets, and tools/autotile
meshes the terrain (with variant scatter) into the base layer. An area adds only its own
objects (buildings) + an optional small accent tileset at a higher first_gid.

This module centralises:
  * the shared set's TilesetRef + a `gid(name)` lookup into it,
  * grid painting helpers (rect / line / organic border / scatter decor),
  * `finalize()` — the standing build pipeline: write -> autotile expand -> strip terrain
    layers -> re-write -> render PNG -> validate. One call so every builder is turnkey.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import random

REPO = Path(__file__).resolve().parents[2]
SHARED = REPO / "assets/tilesets/_shared"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"
SHARED_FIRST_GID = 1

_INDEX = json.loads((SHARED / "vesper_overworld.index.json").read_text())
_SIDECAR = json.loads(
    (REPO / "public/assets/tilesets/vesper_overworld_set.tileset.json").read_text())


def gid(name: str) -> int:
    """Global tile id of a named shared tile (for direct base/deco placement)."""
    return SHARED_FIRST_GID + _INDEX[name]


def shared_tileset_ref() -> dict:
    """The TilesetRef every overworld map lists in `tilesets[]`."""
    return {
        "name": "vesper_overworld_set",
        "image": "assets/tilesets/vesper_overworld_set.webp",
        "tile_width": 16, "tile_height": 16,
        "first_gid": SHARED_FIRST_GID,
        "columns": _SIDECAR["columns"],
        "tile_count": _SIDECAR["tile_count"],
    }


# ---- grid helpers (presence grids: 1 = terrain here) -------------------------
def make_grid(w: int, h: int) -> list[int]:
    return [0] * (w * h)


def rect(g, w, h, x0, y0, x1, y1, val=1):
    for y in range(max(0, y0), min(h, y1 + 1)):
        for x in range(max(0, x0), min(w, x1 + 1)):
            g[y * w + x] = val


def hline(g, w, h, y, x0, x1, val=1):
    rect(g, w, h, x0, y, x1, y, val)


def vline(g, w, h, x, y0, y1, val=1):
    rect(g, w, h, x, y0, x, y1, val)


def organic_border(g, w, h, *, top=0, left=0, right=0, depth=2,
                   bumps=(), rng: random.Random | None = None):
    """A `depth`-deep border on the chosen sides, then a few inward `bumps`
    (x,y,r) blobs so the tree/cliff line reads organic, not a ruled box."""
    if top:
        rect(g, w, h, 0, 0, w - 1, depth - 1)
    if left:
        rect(g, w, h, 0, 0, depth - 1, h - 1)
    if right:
        rect(g, w, h, w - depth, 0, w - 1, h - 1)
    for (bx, by, br) in bumps:
        for y in range(by - br, by + br + 1):
            for x in range(bx - br, bx + br + 1):
                if 0 <= x < w and 0 <= y < h and (x - bx) ** 2 + (y - by) ** 2 <= br * br:
                    g[y * w + x] = 1


def scatter_decor(deco, base, w, h, rng, *, density=0.10, avoid=None):
    """Sprinkle sparse ground decor (pebble/tuft/daisy/patch) onto plain-grass cells —
    the Pokémon trick that breaks a flat fill grid. `avoid` = set of (x,y) to skip."""
    grass = {gid(n) for n in ("grass0", "grass1", "grass2", "grass3")}
    props = [gid("g_tuft"), gid("g_tuft"), gid("g_daisy"), gid("g_pebble"), gid("g_patch")]
    avoid = avoid or set()
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if base[i] in grass and deco[i] == 0 and (x, y) not in avoid \
                    and rng.random() < density:
                deco[i] = rng.choice(props)


# ---- the standing build pipeline --------------------------------------------
def finalize(m: dict, *, scale: int = 3, render: bool = True) -> bool:
    """Write the map, expand terrain -> base (variant autotiling), strip the terrain
    layers (runtime wants plain gids), re-write, render a QA PNG, and validate.
    Returns True iff validate_map passes."""
    map_path = REPO / "public/assets/maps" / f"{m['id']}.json"
    map_path.write_text(json.dumps(m, indent=2) + "\n")

    exp = subprocess.run(["node", str(REPO / "tools/autotile/expand.mjs"), str(map_path)],
                         capture_output=True, text=True)
    if exp.returncode != 0:
        print("EXPAND FAILED:\n", exp.stderr or exp.stdout)
        return False

    # strip terrain layers — the engine reads plain gids; terrain layers were authoring-only.
    m2 = json.loads(map_path.read_text())
    m2["layers"] = [ly for ly in m2["layers"] if ly.get("role") != "terrain"]
    map_path.write_text(json.dumps(m2, indent=2) + "\n")

    if render:
        out = Path("/tmp") / f"{m['id']}.png"
        subprocess.run([sys.executable, str(SCRIPTS / "render_map.py"), str(map_path),
                        "--output", str(out), "--scale", str(scale)], capture_output=True)
        print(f"  rendered -> {out}")

    val = subprocess.run([sys.executable, str(SCRIPTS / "validate_map.py"), str(map_path)],
                         capture_output=True, text=True)
    print(val.stdout)
    return val.returncode == 0
