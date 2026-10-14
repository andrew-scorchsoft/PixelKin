#!/usr/bin/env python3
"""
build_mournfields_set — the Mourning Fields' accent tileset (`mournfields_set`).

The shared overworld set is FROZEN (TILEFORGE 2026-06: "new needs = accent sets or
objects"), and the Fields need one family it cannot give: harvest STUBBLE that sits on
BLIGHT ground with a real edge. The shared `goldgrass0-3` are bare fills with no
transition, so the old plots were painted as flat mustard rectangles (the 2026-10-14
independent review, Part C fix 1). This set draws `stubble`:

  * a grey-gold cut-stubble fill (four motif layouts — rows of cut stalks, never noise),
    deliberately less saturated than the West's sun-garden gold: these fields were left
    standing when the light went;
  * `stubble_drill` / `stubble_drill_v1` — the same ground with two ploughed drill-furrows,
    which the builder lays as deliberate drill ROWS (pinned over the expanded fill);
  * the full 13-role + strip transition onto BLIGHT, rimmed by a 1px line of turned earth
    and a soft shade inside it (the §11 "context-correct" rule: stubble meets the drained
    ground it actually sits on, never grass).

Writes:
  assets/tilesets/mournfields/set_tiles/*.png + tileset.manifest.json  (masters)
  public/assets/tilesets/mournfields_set.{webp,tileset.json}           (served)
  assets/tilesets/mournfields/mournfields_set.index.json               (name->index)

Run:  python3 tools/maps/build_mournfields_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import gbaforge
from gbaforge import flat, img, overlay_tile, put, sh

REPO = Path(__file__).resolve().parents[2]
TILES_DIR = REPO / "assets" / "tilesets" / "mournfields" / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

STUBBLE = (128, 116, 76)        # grey-gold harvest stubble (dimmer than the West's GOLD)
EARTH = (70, 62, 50)            # turned soil: the drill furrows + the plot's rim

# Cut-stalk motif layouts (x, y, kind): 's' = a 1x2 stalk stub with a lit tip,
# 'p' = a fallen straw (2px diagonal), 'd' = a pale chaff dot. Hand-placed in loose
# ROWS (a field is sown in rows), nothing within 1px of the border so every variant
# tiles seamlessly against every other.
STALKS = [
    [(2, 3, "s"), (6, 3, "s"), (10, 3, "s"), (13, 4, "d"), (4, 9, "s"), (8, 9, "s"),
     (12, 9, "s"), (3, 13, "p"), (9, 13, "d")],
    [(3, 2, "d"), (5, 5, "s"), (9, 5, "s"), (13, 5, "s"), (2, 11, "s"), (6, 11, "s"),
     (10, 11, "s"), (12, 13, "p")],
    [(2, 4, "s"), (7, 4, "s"), (12, 3, "p"), (4, 10, "s"), (9, 10, "s"), (13, 10, "s"),
     (6, 14, "d")],
    [(4, 2, "p"), (3, 7, "s"), (7, 7, "s"), (11, 7, "s"), (2, 12, "d"), (5, 13, "s"),
     (10, 13, "s"), (13, 13, "d")],
]


def _stalks(a, layout):
    dark = sh(STUBBLE, 0.70)
    tip = sh(STUBBLE, 1.30, 14)
    pale = sh(STUBBLE, 1.16, 8)
    for (x, y, kind) in layout:
        if kind == "s":
            put(a, [(x, y + 1), (x, y + 2)], dark)
            put(a, [(x, y)], tip)
        elif kind == "p":
            put(a, [(x, y), (x + 1, y + 1)], pale)
        else:
            put(a, [(x, y)], pale)


def stubble_fill(v: int = 0):
    a = flat(STUBBLE)
    _stalks(a, STALKS[v % len(STALKS)])
    return img(a)


def stubble_drill(v: int = 0):
    """Two ploughed drills across the tile: dark furrow, lit ridge-lip above it."""
    a = flat(STUBBLE)
    furrow = EARTH
    lip = sh(STUBBLE, 1.22, 10)
    deep = sh(EARTH, 0.80)
    for y0 in (4, 12):
        put(a, [(x, y0 - 1) for x in range(16)], lip)
        put(a, [(x, y0) for x in range(16)], furrow)
        put(a, [(x, y0 + 1) for x in range(16)], sh(STUBBLE, 0.78))
        # clods in the furrow, offset per variant so drill rows don't stripe
        for x in ((2, 9, 13) if v == 0 else (5, 11)):
            put(a, [(x, y0)], deep)
    stalks = [(3, 7, "s"), (8, 7, "s"), (12, 6, "d")] if v == 0 else \
             [(5, 6, "d"), (10, 7, "s"), (14, 7, "s")]
    _stalks(a, stalks + [(4, 14, "d")] if v == 0 else stalks)
    return img(a)


def stubble_tile(role: str, v: int = 0):
    if role == "fill":
        return stubble_fill(v)
    return overlay_tile(role, stubble_fill(v), gbaforge.blight_fill(v),
                        EARTH, shade_rgb=sh(STUBBLE, 0.86))


ROLES = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
         "corner_sw", "edge_s", "corner_se", "strip_h", "strip_v",
         "inner_nw", "inner_ne", "inner_sw", "inner_se"]


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    for old in TILES_DIR.glob("*.png"):
        old.unlink()
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im, autotile: str | None):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        entry = {"file": fn, "role": "ground", "collides": False}
        if autotile:
            entry.update(terrain="stubble", autotile=autotile)
        tiles.append(entry)

    for role in ROLES:
        add(f"stubble_{role}", stubble_tile(role, 0), role)
    for v in (1, 2, 3):
        add(f"stubble_fill_v{v}", stubble_fill(v), "fill")
    # drills are NOT tagged into the family (the autotiler would scatter them):
    # the builder pins them as deliberate rows over the expanded fill.
    add("stubble_drill", stubble_drill(0), None)
    add("stubble_drill_v1", stubble_drill(1), None)

    manifest = {"name": "mournfields_set", "columns": 6, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (REPO / "assets/tilesets/mournfields/mournfields_set.index.json").write_text(
        json.dumps(index, indent=2) + "\n")
    print(f"mournfields_set: {len(tiles)} tiles -> {TILES_DIR}")
    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
