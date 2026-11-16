#!/usr/bin/env python3
"""
build_hartway_set — the Hartway's accent tileset (`hartway_set`): the DROP beside a
mountain ridge.

The shared overworld set is FROZEN and has no "nothing under you" tile it is safe to
use outdoors (`void` is Starreach ground, `canyon` is the Sere's red strata). The
Hartway's two ridges — the Staircase and the Whiteback — are one tile wide with the
night on both sides, so they need their own gulf, drawn against the alpine ground it
actually sits in (`snow`, the shared North family):

  * `gulf`   THE DROP. Fill = the night air over the valleys: near-black violet with dim
             far-ridge dashes. Edges follow the cliff convention: under any snow to the
             NORTH a full rock FACE (lit lip, streaked stone, a caught snow ledge), on the
             south rim only a thin cornice, a few px of rock at the sides. Collides.
  * `gulf_town` / `gulf_lane`  two far-off lights, PINNED by a builder (mk.finalize
             pin_base), never scattered.

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


def gulf_fill(v: int = 0, lamps: str | None = None):
    """Night air over the valleys: dim far-ridge dashes (a slope a mile below), never
    noise. `lamps` adds a deliberate far-off light — 'town' (a small warm cluster) or
    'lane' (three lamps on a road) — for the few cells a builder PINS; the scattered
    fill variants are lampless, so the dark never reads as a field of eyes."""
    a = flat(DEEP)
    dim = (42, 38, 78)
    dimmer = (28, 25, 56)
    for i, (x, y, n) in enumerate(FAR[v % len(FAR)]):
        put(a, [((x + k) % 16, y) for k in range(n)], dim if i == 0 else dimmer)
        put(a, [((x + k + 1) % 16, y + 1) for k in range(max(1, n - 2))], dimmer)
    if lamps == "town":
        put(a, [(6, 9), (8, 10), (7, 11)], (236, 170, 92))
        put(a, [(5, 10), (9, 9), (9, 11)], (176, 112, 70))
    elif lamps == "lane":
        put(a, [(4, 12), (8, 9), (12, 6)], (214, 150, 86))
    return img(a)


# the rock of the Hartshoulder under the snow (the reel's ridge: dark warm stone)
ROCK = [(92, 74, 92), (78, 60, 78), (66, 50, 68), (56, 42, 62), (48, 36, 58),
        (40, 30, 52), (33, 26, 48), (27, 22, 44), (22, 18, 40)]


def gulf_tile(role: str, v: int = 0):
    """The drop, drawn the way the house draws height (cliff = top + visible FACE):

      * snow ABOVE a gulf pixel (the north rim, and the ground under a ridge):
        a FACE — a 2px lit snow lip, then streaked rock darkening into the deep,
        with a small snow ledge caught on it. This is what makes a ridge a fin.
      * snow BELOW (the south rim): only a thin cornice — you are looking over it.
      * snow to the SIDE: a few px of rock.
    """
    if role == "fill":
        return gulf_fill(v)
    m = overlay_mask(role, 3, 3)           # True = snow (outer) shows
    a = np.asarray(gulf_fill(v).convert("RGBA")).astype(np.int16).copy()
    o = np.asarray(gf.snow_fill(v).convert("RGBA")).astype(np.int16)
    H, W = m.shape
    for y in range(H):
        for x in range(W):
            if m[y, x]:
                a[y, x] = o[y, x]
                continue
            up = next((d for d in range(1, 17) if y - d >= 0 and m[y - d, x]), None)
            dn = next((d for d in range(1, 4) if y + d < H and m[y + d, x]), None)
            side = min([d for d in range(1, 5)
                        if (x - d >= 0 and m[y, x - d]) or (x + d < W and m[y, x + d])] or [9])
            if up is not None:
                if up <= 2:
                    col = (232, 238, 250) if up == 1 else (158, 172, 208)     # the lip
                else:
                    k = min(len(ROCK) - 1, (up - 3) * len(ROCK) // 11)
                    col = ROCK[k]
                    if (x * 5 + v * 3) % 7 == 2 and up > 3:                    # weathering streak
                        col = sh(col, 0.80)
                    if up in (7, 8) and (x + v * 4) % 16 in (3, 4, 5, 11, 12): # a caught ledge of snow
                        col = (150, 166, 204) if up == 7 else sh(col, 0.72)
                a[y, x, :3] = col
            elif dn is not None:
                a[y, x, :3] = (214, 224, 244) if dn == 1 else (58, 54, 92)     # cornice + its shadow
            elif side <= 3:
                a[y, x, :3] = ROCK[min(len(ROCK) - 1, 2 + side * 2)]
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
    # APPENDED: the two far-off lights (never scattered — a builder pins them, a few a map)
    add("gulf_town", gulf_fill(1, "town"), role="void", collides=True)
    add("gulf_lane", gulf_fill(2, "lane"), role="void", collides=True)

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
