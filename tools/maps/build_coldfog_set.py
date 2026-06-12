#!/usr/bin/env python3
"""
build_coldfog_set — the W3 COLDFOG accent tileset (`coldfog_set`).

The shared overworld set is FROZEN at 386 tiles (TILEFORGE 2026-06: "new needs
= accent sets or objects"), and the Coldfog cluster needs exactly one new
terrain family the shared set cannot give it: a wall/crag family whose rim
transitions are CONTEXT-CORRECT on BLIGHT ground. The shared `cliff` family
transitions to grass — on the drained marsh it rings every crag with a bright
teal-green line (the §11 r8 wrong-ground ring; CLAUDE.md: "painting one over
the wrong ground rings it with the wrong colour"). This accent set draws
`fogcrag`: the same drawn cliff-top/face ladder (lit lip → streaked face →
contact shadow — the level-design §11 rule-8 convention, kept exactly), with
every transition composed over `gbaforge.blight_fill` instead of grass.

This is the repo's first ACCENT set on the mapkit path: builders stack it via
`mk.register_tileset("coldfog_set", index=...)` (engine resolves gids by range,
MapLoader.ts; expand.mjs resolves the terrain by the layer's `set` name).

Writes:
  assets/tilesets/coldfog/set_tiles/*.png + tileset.manifest.json  (masters)
  public/assets/tilesets/coldfog_set.{webp,tileset.json}           (served)
  assets/tilesets/coldfog/coldfog_set.index.json                   (name->index)

Run:  ./venv/bin/python tools/maps/build_coldfog_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

import gbaforge
from gbaforge import sh, overlay_tile, img

REPO = Path(__file__).resolve().parents[2]
TILES_DIR = REPO / "assets" / "tilesets" / "coldfog" / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

CLIFF = gbaforge.CLIFF


def fogcrag_face(role: str, v: int = 0):
    """edge_s / corner_s* — the visible FACE over BLIGHT ground: lit lip,
    streaked face, dark contact seam, drained ground below (gbaforge's
    cliff_face_tile verbatim, with blight for grass)."""
    g = np.asarray(gbaforge.blight_fill(v).convert("RGBA")).astype(np.int16)
    a = np.asarray(gbaforge.cliff_top(v).convert("RGBA")).astype(np.int16).copy()
    LIP, FACE_END = 4, 12
    a[LIP, :, :3] = sh(CLIFF, 1.40, 16)                      # lit lip
    face = sh(CLIFF, 0.72)
    streak = sh(CLIFF, 0.56)
    for y in range(LIP + 1, FACE_END + 1):
        a[y, :, :3] = face
    x1, x2 = (3 + 3 * v) % 14 + 1, (10 + 3 * v) % 14 + 1
    for y in range(LIP + 1, 9):
        a[y, x1, :3] = streak
    for y in range(9, FACE_END + 1):
        a[y, x2, :3] = streak
    a[9, :, :3] = sh(CLIFF, 0.60)
    a[FACE_END + 1, :, :3] = sh(CLIFF, 0.34)                 # contact shadow
    a[FACE_END + 2:, :] = g[FACE_END + 2:, :]                # drained ground below
    if role == "corner_sw":
        a[:, :2] = g[:, :2]
        a[:, 2, :3] = sh(CLIFF, 0.45)
    if role == "corner_se":
        a[:, 14:] = g[:, 14:]
        a[:, 13, :3] = sh(CLIFF, 0.45)
    return img(a)


def fogcrag_tile(role: str, v: int = 0):
    """Any of the 13 roles for the fogcrag family (cliff over blight)."""
    if role == "fill":
        return gbaforge.cliff_top(v)
    if role in ("edge_s", "corner_sw", "corner_se"):
        return fogcrag_face(role, v)
    return overlay_tile(role, gbaforge.cliff_top(v), gbaforge.blight_fill(v),
                        sh(CLIFF, 0.45), shade_rgb=sh(CLIFF, 0.80))


NINE = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
        "corner_sw", "edge_s", "corner_se"]
INNER = ["inner_nw", "inner_ne", "inner_sw", "inner_se"]


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im, **extra):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": "cliff", "terrain": "fogcrag",
                      "autotile": extra.pop("autotile"), "collides": True, **extra})

    for role in NINE + INNER:
        add(f"fogcrag_{role}", fogcrag_tile(role, 0), autotile=role)
    for v in (1, 2):
        add(f"fogcrag_fill_v{v}", fogcrag_tile("fill", v), autotile="fill")
    add("fogcrag_edge_s_v1", fogcrag_tile("edge_s", 1), autotile="edge_s")

    manifest = {"name": "coldfog_set", "columns": 6, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n")
    (REPO / "assets/tilesets/coldfog/coldfog_set.index.json").write_text(
        json.dumps(index, indent=2) + "\n")
    print(f"coldfog_set: {len(tiles)} tiles -> {TILES_DIR}")

    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)],
                         capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
