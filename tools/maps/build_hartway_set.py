#!/usr/bin/env python3
"""
build_hartway_set — the Hartway's accent tileset (`hartway_set`): the DROP beside a
mountain ridge.

The shared overworld set is FROZEN and has no "nothing under you" tile it is safe to
use outdoors (`void` is Starreach ground, `canyon` is the Sere's red strata). The
Hartway's two ridges — the Staircase and the Whiteback — are one tile wide with the
night on both sides, so they need their own gulf, drawn against the alpine ground it
actually sits in (`snow`, the shared North family):

  * `gulf`   THE DROP. Fill = the night air over the valleys: near-black violet, a few
             dim slope lines far below and (one layout) two warm lamp pixels — a town,
             a very long way down. Every edge falls away from the snow rim: lit lip,
             blue shade, then rock bands darkening into the deep. Collides.

Writes:
  assets/tilesets/hartway/set_tiles/*.png + tileset.manifest.json   (masters)
  public/assets/tilesets/hartway_set.{webp,tileset.json}             (served)
  assets/tilesets/hartway/hartway_set.index.json                     (name -> index)

Tile ORDER is stable: append new tiles at the end, never insert (maps bake gids).

Run:  python3 tools/maps/build_hartway_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

import gbaforge as gf
from gbaforge import flat, img, put, sh, overlay_mask, _border_of

REPO = Path(__file__).resolve().parents[2]
TILES_DIR = REPO / "assets" / "tilesets" / "hartway" / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

DEEP = (17, 14, 36)          # the night under the ridge
# the fall, rim -> deep: snow lip, snow shade, then the mountain's own stone
FALL = [(226, 234, 248), (150, 166, 204), (104, 100, 124), (82, 76, 104),
        (62, 56, 86), (46, 40, 70), (32, 27, 54), (24, 20, 44)]

FAR = [
    [(2, 5, 4), (10, 11, 3)],
    [(7, 3, 5), (1, 12, 3)],
    [(4, 8, 6), (12, 2, 2)],
    [(9, 6, 4), (3, 13, 5)],
]


def gulf_fill(v: int = 0):
    """Night air: dim far-slope dashes; layout 3 carries two lamp pixels (a town)."""
    a = flat(DEEP)
    dim = (30, 27, 58)
    dimmer = (23, 20, 46)
    for i, (x, y, n) in enumerate(FAR[v % len(FAR)]):
        put(a, [((x + k) % 16, y) for k in range(n)], dim if i == 0 else dimmer)
    if v == 3:
        put(a, [(6, 10)], (236, 170, 92))
        put(a, [(8, 11)], (198, 132, 76))
    return img(a)


def gulf_tile(role: str, v: int = 0):
    if role == "fill":
        return gulf_fill(v)
    m = overlay_mask(role, 3, 3)           # True = snow (outer) shows
    a = np.asarray(gulf_fill(v).convert("RGBA")).astype(np.int16).copy()
    o = np.asarray(gf.snow_fill(v).convert("RGBA")).astype(np.int16)
    a[m] = o[m]
    seen = m.copy()
    ring = _border_of(m)
    snow_rim = _border_of(~m) & m          # snow px touching the drop: a shaded lip
    for k in range(len(FALL)):
        if not ring.any():
            break
        a[ring & ~seen, :3] = FALL[k]
        seen |= ring
        ring = _border_of(seen) & ~seen
    a[snow_rim, :3] = sh(gf.SNOW, 0.80)
    return img(a)


ROLES = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
         "corner_sw", "edge_s", "corner_se", "strip_h", "strip_v",
         "inner_nw", "inner_ne", "inner_sw", "inner_se"]


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    for old in TILES_DIR.glob("*.png"):
        old.unlink()
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name, im, *, role="ground", terrain=None, autotile=None, **meta):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        e = {"file": fn, "role": role, "collides": bool(meta.pop("collides", False))}
        if terrain:
            e.update(terrain=terrain, autotile=autotile)
        e.update(meta)
        tiles.append(e)

    for r in ROLES:
        add(f"gulf_{r}", gulf_tile(r, 0), role="void", terrain="gulf", autotile=r, collides=True)
    for v in (1, 2, 3):
        add(f"gulf_fill_v{v}", gulf_fill(v), role="void", terrain="gulf", autotile="fill",
            collides=True)

    manifest = {"name": "hartway_set", "columns": 8, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (REPO / "assets/tilesets/hartway/hartway_set.index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"hartway_set: {len(tiles)} tiles -> {TILES_DIR}")
    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
