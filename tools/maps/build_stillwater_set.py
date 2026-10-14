#!/usr/bin/env python3
"""
build_stillwater_set — Stillwater's accent tileset (`stillwater_set`).

The shared overworld set is FROZEN, and Stillwater needs one family it cannot
give: a village LANE whose transitions are context-correct on BLIGHT ground.
The shared `path` rings itself with green grass on the drained ground and
`ruinfloor` with gold — both wrong (CLAUDE.md: "painting one over the wrong
ground rings it with the wrong colour"). This draws `flagway`: swept pale-grey
flagstones, laid square and kept clean (the Hollowing's tended register), with
every transition composed over `gbaforge.blight_fill` (the build_coldfog_set.py
pattern, verbatim in method).

Writes:
  assets/tilesets/stillwater/set_tiles/*.png + tileset.manifest.json  (masters)
  public/assets/tilesets/stillwater_set.{webp,tileset.json}           (served)
  assets/tilesets/stillwater/stillwater_set.index.json                (name->index)

Run:  python3 tools/maps/build_stillwater_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import gbaforge
from gbaforge import sh, overlay_tile, img, flat, put

REPO = Path(__file__).resolve().parents[2]
TILES_DIR = REPO / "assets" / "tilesets" / "stillwater" / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

FLAG = (128, 132, 138)          # swept pale-grey flagstone (cooler + lighter than BLIGHT)

# deliberate joint layouts per variant (the gbaforge rule: motifs, never noise)
LAYOUTS = [
    [("h", 0, 7, 16), ("v", 7, 0, 7), ("v", 11, 8, 16), ("d", 3, 3), ("d", 13, 12)],
    [("h", 0, 8, 16), ("v", 4, 0, 8), ("v", 12, 0, 8), ("v", 8, 9, 16), ("d", 2, 12)],
    [("h", 0, 5, 16), ("h", 0, 12, 16), ("v", 9, 0, 5), ("v", 5, 6, 12), ("v", 12, 13, 16)],
]


def flagway_fill(v: int = 0):
    a = flat(FLAG)
    joint = sh(FLAG, 0.74)
    lit = sh(FLAG, 1.12, 6)
    for item in LAYOUTS[v % len(LAYOUTS)]:
        if item[0] == "h":
            _, x0, y, x1 = item
            put(a, [(x, y) for x in range(x0, x1)], joint)
            put(a, [(x, y + 1) for x in range(x0, x1, 3) if y + 1 < 16], lit)
        elif item[0] == "v":
            _, x, y0, y1 = item
            put(a, [(x, y) for y in range(y0, min(y1, 16))], joint)
        else:
            _, x, y = item
            put(a, [(x, y), (x + 1, y)], sh(FLAG, 0.88))
    return img(a)


def flagway_tile(role: str, v: int = 0):
    if role == "fill":
        return flagway_fill(v)
    return overlay_tile(role, flagway_fill(v), gbaforge.blight_fill(v),
                        sh(FLAG, 0.50), shade_rgb=sh(FLAG, 0.84))


ROLES = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
         "corner_sw", "edge_s", "corner_se", "strip_h", "strip_v",
         "inner_nw", "inner_ne", "inner_sw", "inner_se"]


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im, autotile: str):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": "path", "terrain": "flagway",
                      "autotile": autotile, "collides": False})

    for role in ROLES:
        add(f"flagway_{role}", flagway_tile(role, 0), role)
    for v in (1, 2):
        add(f"flagway_fill_v{v}", flagway_tile("fill", v), "fill")

    manifest = {"name": "stillwater_set", "columns": 6, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (REPO / "assets/tilesets/stillwater/stillwater_set.index.json").write_text(
        json.dumps(index, indent=2) + "\n")
    print(f"stillwater_set: {len(tiles)} tiles -> {TILES_DIR}")
    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
