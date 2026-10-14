#!/usr/bin/env python3
"""
build_farlamp_set — the Farlamp Isles' tiny ANIMATED accent tileset
(`farlamp_set`, walkthrough/10 Part I).

Objects can't animate, so the far lamp's BLINK is a tile: painted in a map's
`above` layer over the lamp-room of the `farlamp_skerry_light` object (tile col 1,
row 0 of its 3x3 footprint), it lights the dark glass beneath in a slow
on-on-off-off-off cycle. `blink_far` is the same light seen from the mainland —
a pinpoint on the Point's southern horizon, inside the fog bank.

Neither tile collides (both live in `above`, which the engine never reads for
collision). Drawn in code; re-run freely.

Writes:
  assets/tilesets/farlamp/set_tiles/*.png + tileset.manifest.json  (masters)
  public/assets/tilesets/farlamp_set.{webp,tileset.json}           (served)
  assets/tilesets/farlamp/farlamp_set.index.json                   (name->index)

Run:  python3 tools/maps/build_farlamp_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
TILES_DIR = REPO / "assets" / "tilesets" / "farlamp" / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

AMBER = (255, 184, 74)
CORE = (255, 236, 160)
WHITE = (255, 250, 230)


def blank() -> np.ndarray:
    return np.zeros((16, 16, 4), dtype=np.uint8)


def lamp(level: int) -> Image.Image:
    """The lamp-room glass lit (x 3-12, y 4-10 of tile (1,0) of the skerry:
    the object's x 19-28 minus 16). level 2 = full, 1 = waning."""
    a = blank()
    if level:
        col = CORE if level == 2 else AMBER
        a[4:11, 4:12] = (*col, 255)
        a[4:11, 7:9] = (*AMBER, 255)          # the mullion's glow edge
        a[5:7, 5:7] = (*WHITE, 255)
        if level == 2:                        # a short beam each side
            for x in range(0, 3):
                a[7, x] = (*CORE, 200 - x * 50)
                a[7, 15 - x] = (*CORE, 200 - x * 50)
    return Image.fromarray(a, "RGBA")


def far(level: int) -> Image.Image:
    """A distant pinpoint with a 1px cross halo."""
    a = blank()
    if level:
        a[7:9, 7:9] = (*CORE, 255)
        if level == 2:
            for (x, y) in ((6, 7), (6, 8), (9, 7), (9, 8), (7, 6), (8, 6), (7, 9), (8, 9)):
                a[y, x] = (*AMBER, 170)
            a[7, 4:6] = (*AMBER, 90)
            a[7, 10:12] = (*AMBER, 90)
    return Image.fromarray(a, "RGBA")


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    for old in TILES_DIR.glob("*.png"):
        old.unlink()
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im: Image.Image, **extra) -> int:
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": "decor", **extra})
        return len(tiles) - 1

    lit = add("blink_lamp", lamp(2))
    wane = add("blink_lamp_wane", lamp(1))
    dark = add("blink_lamp_dark", lamp(0))
    tiles[lit]["animation"] = {"frames": [lit, lit, wane, dark, dark, dark], "duration_ms": 3000}
    f_on = add("blink_far", far(2))
    f_wane = add("blink_far_wane", far(1))
    f_off = add("blink_far_dark", far(0))
    tiles[f_on]["animation"] = {"frames": [f_on, f_wane, f_off, f_off, f_off, f_off],
                                "duration_ms": 3000}

    manifest = {"name": "farlamp_set", "columns": 3, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (REPO / "assets/tilesets/farlamp/farlamp_set.index.json").write_text(
        json.dumps(index, indent=2) + "\n")
    print(f"farlamp_set: {len(tiles)} tiles -> {TILES_DIR}")
    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
