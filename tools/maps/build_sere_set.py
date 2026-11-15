#!/usr/bin/env python3
"""
build_sere_set — the Sere's accent tileset (`sere_set`): Galehigh's dry side, the
rain-shadow desert east of the terraces, and the rim of the Thousandfold canyon.

The shared overworld set is FROZEN (TILEFORGE 2026-06: "new needs = accent sets or
objects") and has no desert: its `sand` is the pale beach of the South coast and its
`cliff` is blue-grey mountain stone. A desert needs its OWN ground so every edge is
context-correct (level-design §11: a family meets the ground it actually sits on).
Every tile is DRAWN (gbaforge grammar: flat dusk-palette base + deliberate motif
layouts, never noise), all against one ground, `sere` (dusk-ochre sand):

  * `sere`       base fill, four ripple layouts (the builder scatters them as base)
  * `seretrail`  the packed drovers' track (13 roles + strips + inners) over sere
  * `hardpan`    cracked clay pans (13 + strips + inners) over sere
  * `redrock`    the mesa wall — the cliff convention: fill = plateau TOP, S edges =
                 the visible FACE in STRATA BANDS (rust / ochre / bone / violet),
                 N/W/E = rim transitions against sere. Collides.
  * `canyon`     THE THOUSANDFOLD: the drop. Fill = the violet deep with faint far
                 strata; every edge falls away from the sand rim in layered bands
                 (lit lip, rust, ochre, bone, violet, dark) — a thousand folds of
                 stone. Collides.
  * `serescrub`  dry sage-scrub, the desert's encounter tile (fill-only, hard-edged,
                 encounter_terrain tall_grass — the dunegrass convention)
  * `sere_ledge_s` a dune bank (one-way hop, ledge:'down')

Writes:
  assets/tilesets/sere/set_tiles/*.png + tileset.manifest.json   (masters)
  public/assets/tilesets/sere_set.{webp,tileset.json}             (served)
  assets/tilesets/sere/sere_set.index.json                        (name -> index)

Tile ORDER is stable: append new tiles at the end, never insert (maps bake gids).

Run:  python3 tools/maps/build_sere_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

import gbaforge as gf
from gbaforge import flat, img, overlay_tile, put, sh, overlay_mask, _border_of, _fan, _ledge_s

REPO = Path(__file__).resolve().parents[2]
TILES_DIR = REPO / "assets" / "tilesets" / "sere" / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

SERE = (178, 118, 78)        # dusk-ochre desert sand (warmer + darker than the beach)
TRAIL = (122, 82, 60)        # the drovers' packed track
CLAY = (150, 96, 70)         # hardpan clay
ROCK = (138, 66, 52)         # redrock plateau top
DEEP = (38, 24, 46)          # the canyon's violet deep
SCRUB = (96, 104, 70)        # dry sage

# strata ladder (lip -> deep), the canyon's and the mesa face's shared bands
STRATA = [(232, 196, 150), (176, 82, 58), (150, 66, 50), (204, 138, 82), (214, 182, 140),
          (122, 70, 96), (160, 74, 56), (96, 52, 78), (70, 40, 66), (52, 32, 58)]

RIPPLES = [
    [(2, 4, 5), (8, 9, 6), (3, 13, 4)],
    [(5, 2, 6), (1, 8, 4), (9, 12, 5)],
    [(7, 5, 5), (2, 10, 6), (10, 14, 4)],
    [(3, 3, 4), (9, 7, 5), (5, 12, 6)],
]


def sere_fill(v: int = 0):
    """Dusk sand + wind ripples (short lit/dark dash pairs) + one pebble."""
    a = flat(SERE)
    dark = sh(SERE, 0.86)
    lit = sh(SERE, 1.12, 6)
    for (x, y, n) in RIPPLES[v % len(RIPPLES)]:
        put(a, [(x + i, y) for i in range(n)], dark)
        put(a, [(x + i + 1, y - 1) for i in range(n - 2)], lit)
    px, py = [(12, 3), (13, 11), (12, 1), (13, 14)][v % 4]
    put(a, [(px, py)], sh(SERE, 0.70))
    return img(a)


def trail_fill(v: int = 0):
    a = flat(TRAIL)
    dark = sh(TRAIL, 0.82)
    lit = sh(TRAIL, 1.16, 4)
    for i, (x, y) in enumerate(gf.PATH_LAYOUTS[v % len(gf.PATH_LAYOUTS)]):
        put(a, [(x, y), (x + 1, y)], dark if i % 2 == 0 else lit)
    return img(a)


CRACKS = [
    [[(2, 3), (3, 4), (4, 4), (5, 5), (5, 6)], [(9, 8), (10, 9), (11, 9), (12, 10)], [(4, 11), (5, 12), (6, 12)]],
    [[(3, 9), (4, 8), (5, 8), (6, 7)], [(10, 3), (10, 4), (11, 5), (12, 5)], [(8, 12), (9, 13), (10, 13)]],
    [[(6, 2), (6, 3), (7, 4), (8, 4)], [(2, 12), (3, 12), (4, 13)], [(11, 8), (12, 9), (12, 10), (13, 11)]],
]


def hardpan_fill(v: int = 0):
    a = flat(CLAY)
    dark = sh(CLAY, 0.66)
    lit = sh(CLAY, 1.18, 8)
    for crack in CRACKS[v % len(CRACKS)]:
        put(a, crack, dark)
        x, y = crack[0]
        put(a, [(x, y - 1)], lit)
    return img(a)


def redrock_top(v: int = 0):
    a = flat(ROCK)
    dark = sh(ROCK, 0.80)
    lit = sh(ROCK, 1.26, 10)
    for i, (x, y) in enumerate(gf.CLIFF_TOP_LAYOUTS[v % len(gf.CLIFF_TOP_LAYOUTS)]):
        put(a, [(x, y), (x + 1, y), (x + 2, y + 1)], dark)
        if i == 0:
            put(a, [(x + 3, y - 1)], lit)
    return img(a)


def redrock_face(role: str, v: int = 0):
    """edge_s / corner_s*: plateau lip, then a FACE of horizontal strata bands
    (the canyon's colours, so a mesa reads as a piece broken off the Thousandfold),
    a contact shadow and sand below."""
    g = np.asarray(sere_fill(v).convert("RGBA")).astype(np.int16)
    a = np.asarray(redrock_top(v).convert("RGBA")).astype(np.int16).copy()
    bands = [STRATA[0], STRATA[1], STRATA[1], STRATA[3], STRATA[3], STRATA[4],
             STRATA[2], STRATA[2], STRATA[5], STRATA[6]]
    for i, y in enumerate(range(3, 13)):
        a[y, :, :3] = bands[i]
    # a couple of short vertical weathering streaks (partial, never a grate)
    for (x, y0, y1) in ([(3, 5, 8), (11, 8, 11)] if v % 2 == 0 else [(6, 4, 7), (13, 9, 12)]):
        for y in range(y0, y1 + 1):
            a[y, x, :3] = sh(tuple(int(c) for c in a[y, x, :3]), 0.74)
    a[13, :, :3] = (40, 22, 30)                                 # contact shadow
    a[14:, :] = g[14:, :]
    if role == "corner_sw":
        a[:, :2] = g[:, :2]
        a[:, 2, :3] = sh(ROCK, 0.5)
    if role == "corner_se":
        a[:, 14:] = g[:, 14:]
        a[:, 13, :3] = sh(ROCK, 0.5)
    return img(a)


def redrock_tile(role: str, v: int = 0):
    if role == "fill":
        return redrock_top(v)
    if role in ("edge_s", "corner_sw", "corner_se"):
        return redrock_face(role, v)
    return overlay_tile(role, redrock_top(v), sere_fill(v), sh(ROCK, 0.48),
                        shade_rgb=sh(ROCK, 0.82))


def canyon_fill(v: int = 0):
    """The deep: the FAR walls of the Thousandfold seen across the gulf — wide,
    dim strata bands (violet / dusk-rust / plum), a ledge-line of lit dashes on
    each, and on one layout the pale thread of the long-dry riverbed far below.
    Bands repeat every 16px so a field of them reads as a cliff a mile off."""
    a = flat(DEEP)
    bands = [(0, 3, (66, 38, 64)), (3, 5, (104, 56, 58)), (5, 6, (140, 84, 70)),
             (6, 9, (58, 34, 60)), (9, 11, (92, 54, 76)), (11, 12, (124, 74, 72)),
             (12, 16, (44, 28, 52))]
    for (y0, y1, col) in bands:
        a[y0:y1, :, :3] = col
    lit = (164, 104, 84)
    lays = [[(1, 4, 5), (9, 10, 4)], [(6, 4, 6), (0, 10, 3), (12, 10, 3)],
            [(3, 4, 4), (10, 4, 3), (5, 10, 5)], [(11, 4, 5), (2, 10, 6)]]
    for (x, y, n) in lays[v % len(lays)]:
        put(a, [((x + i) % 16, y) for i in range(n)], lit)
    for (x, y) in [(3, 7), (12, 13), (8, 1)][: 2 + v % 2]:
        put(a, [(x, y)], (30, 18, 36))                       # shadow pocks
    if v == 3:   # the dry river's thread
        put(a, [(x, 14 if x < 8 else 13) for x in range(16)], (120, 104, 128))
    return img(a)


def canyon_tile(role: str, v: int = 0):
    """Every edge falls away from the sand rim in strata bands: the rim's lit
    lip, then rust, ochre, bone and violet, darkening into the deep."""
    if role == "fill":
        return canyon_fill(v)
    m = overlay_mask(role, 3, 3)           # True = sand (outer) shows
    a = np.asarray(canyon_fill(v).convert("RGBA")).astype(np.int16).copy()
    o = np.asarray(sere_fill(v).convert("RGBA")).astype(np.int16)
    a[m] = o[m]
    seen = m.copy()
    ring = _border_of(m)
    sand_rim = _border_of(~m) & m          # sand px touching the drop: a dark lip
    for k in range(len(STRATA)):
        if not ring.any():
            break
        col = STRATA[k]
        a[ring & ~seen, :3] = col
        seen |= ring
        ring = _border_of(seen) & ~seen
    a[sand_rim, :3] = sh(SERE, 0.70)
    return img(a)


def scrub_fill(v: int = 0):
    """Dry sage over sere: wind-bent grey-green fans (the encounter tile)."""
    a = flat(sh(SERE, 0.86))
    mid = SCRUB
    light = sh(SCRUB, 1.35, 16)
    dark = sh(SCRUB, 0.55)
    for (cx, cy) in gf.TG_LAYOUTS[v % len(gf.TG_LAYOUTS)]:
        _fan(a, cx, cy, mid, light, dark)
    return img(a)


def sere_ledge(v: int = 0):
    return _ledge_s(SERE, sh(SERE, 0.86), sh(SERE, 1.20, 12),
                    sh(SERE, 0.72), sh(SERE, 0.56), sh(SERE, 0.52), v)


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

    # the ground (base fills; also the `sere` terrain fill for completeness)
    for v in range(4):
        add(f"sere{v}", sere_fill(v), role="sand")
    # the drovers' track
    for r in ROLES:
        add(f"seretrail_{r}", overlay_tile(r, trail_fill(0), sere_fill(0), sh(TRAIL, 0.66),
                                           shade_rgb=sh(TRAIL, 1.12, 4)) if r != "fill" else trail_fill(0),
            role="path", terrain="seretrail", autotile=r)
    for v in (1, 2):
        add(f"seretrail_fill_v{v}", trail_fill(v), role="path", terrain="seretrail", autotile="fill")
    # hardpan
    for r in ROLES:
        add(f"hardpan_{r}", overlay_tile(r, hardpan_fill(0), sere_fill(0), sh(CLAY, 0.62),
                                         r=5, shade_rgb=sh(CLAY, 1.10, 4)) if r != "fill" else hardpan_fill(0),
            role="sand", terrain="hardpan", autotile=r)
    for v in (1, 2):
        add(f"hardpan_fill_v{v}", hardpan_fill(v), role="sand", terrain="hardpan", autotile="fill")
    # the mesa wall
    for r in ROLES:
        add(f"redrock_{r}", redrock_tile(r, 0), role="cliff", terrain="redrock", autotile=r,
            collides=True)
    for v in (1, 2):
        add(f"redrock_fill_v{v}", redrock_tile("fill", v), role="cliff", terrain="redrock",
            autotile="fill", collides=True)
    add("redrock_edge_s_v1", redrock_tile("edge_s", 1), role="cliff", terrain="redrock",
        autotile="edge_s", collides=True)
    # THE THOUSANDFOLD
    for r in ROLES:
        add(f"canyon_{r}", canyon_tile(r, 0), role="void", terrain="canyon", autotile=r,
            collides=True)
    for v in (1, 2, 3):
        add(f"canyon_fill_v{v}", canyon_fill(v), role="void", terrain="canyon",
            autotile="fill", collides=True)
    # the scrub (encounter tile, fill-only — hard-edged like every encounter bed)
    for v in range(3):
        add(f"serescrub_fill{'' if v == 0 else f'_v{v}'}", scrub_fill(v), role="ground",
            terrain="serescrub", autotile="fill", encounter_terrain="tall_grass")
    # the dune bank
    add("sere_ledge_s", sere_ledge(0), role="ledge", ledge="down")
    add("sere_ledge_s_v1", sere_ledge(1), role="ledge", ledge="down")

    manifest = {"name": "sere_set", "columns": 8, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (REPO / "assets/tilesets/sere/sere_set.index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"sere_set: {len(tiles)} tiles -> {TILES_DIR}")
    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
