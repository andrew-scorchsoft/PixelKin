#!/usr/bin/env python3
"""
build_brewfair_sets — the two re-skinned interior kits of the Wakeful Fair
(S7 "Just One More Cup"; maps by build_wakeful_fair.py, the furniture by brewforge.py).

Like the Old Light's floor sets (build_oldlight_sets.py) each is a pixel transform
of `interior_set` with the IDENTICAL tile order, count (55, 8 columns) and per-tile
metadata, so a roomkit map swaps `interior_set` for these with zero gid changes:

  brewfair_set   THE MARQUEE: honey plank floorboards, red-and-cream striped
                 canvas walls with a gold rope trim and a deep red skirt, the wall
                 tops a dark plum canvas edged in gold rope, a lantern inset.
  brewdream_set  THE BOTTOM OF THE CUP (the hallucination): the floor is crema
                 foam (bubbles), the "walls" are the coffee itself — dark liquid
                 with slow ripples, the autotiled lips turned into a foam shore —
                 and the north FACE is the porcelain wall of the cup with a gold
                 rim. The doormat tile becomes a GLOSSY CARAMEL SLICK: the map lays
                 it under its `ice` flows, so what's slippery looks slippery.

Readability is binding (collision is unchanged): every band tile stays darker and
more structured than every floor tile; floor fills stay seamless (periodic on 16px).

Reads   public/assets/tilesets/interior_set.webp (+ sidecar)
Writes  assets/tilesets/brewfair/sets/<name>.png   (master)
        public/assets/tilesets/<name>.webp         (lossless, served)
        public/assets/tilesets/<name>.tileset.json (source sidecar, name/image changed)
Deterministic; re-run freely.

Run:  python3 tools/maps/build_brewfair_sets.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_oldlight_sets import (BANDS, FACE, FACE_ENDS, FLOORS, INSET, MAT, SRC, T,  # noqa: E402
                                 assemble, load, lum)

REPO = Path(__file__).resolve().parents[2]
MASTERS = REPO / "assets" / "tilesets" / "brewfair" / "sets"


def rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float64)


def solid(col):
    t = np.zeros((T, T, 4), np.float64)
    t[..., :3] = rgb(col)
    t[..., 3] = 255
    return t


def put(t, x, y, col, k=1.0):
    if 0 <= x < T and 0 <= y < T:
        t[y, x, :3] = t[y, x, :3] * (1 - k) + rgb(col) * k


def lip_split(src):
    """The band tile's structure: True where the source draws its LIP (the bright
    copper edge), False on the dark wall-top fill — so the re-skin keeps every
    autotiled shape exactly."""
    L = lum(src)
    return L > 95


def shade_like(new_face, src_face, src_end):
    """Transfer a face-end's side shading onto a re-drawn face (per-pixel ratio)."""
    ratio = (lum(src_end) + 1) / (lum(src_face) + 1)
    out = new_face.copy()
    out[..., :3] = np.clip(new_face[..., :3] * ratio[..., None], 0, 255)
    return out


# ---- THE MARQUEE -----------------------------------------------------------------
def marquee_floor(variant: int):
    """Long honey floorboards running east-west: four boards a tile, a butt-joint
    on only every other board (staggered per variant), soft gaps — so the floor
    reads as planks, not brickwork."""
    t = solid("#b07a44")
    joints = [5, None, 12, None] if variant == 0 else [None, 9, None, 2]
    for b in range(4):
        y0 = b * 4
        base = ["#b07a44", "#aa7442", "#b47e48", "#a8723f"][(b + variant) % 4]
        for y in range(y0, y0 + 4):
            for x in range(T):
                put(t, x, y, base)
        for x in range(T):
            put(t, x, y0 + 3, "#8a5a30")               # the gap between boards
            put(t, x, y0, "#c08a50", 0.5)              # the lit board edge
        if joints[b] is not None:
            for y in range(y0, y0 + 3):
                put(t, joints[b], y, "#8a5a30")
        for x in range(T):                              # a little grain
            if (x * 7 + b * 5 + variant * 3) % 13 == 0:
                put(t, x, y0 + 1 + (x % 2), "#9c6838", 0.7)
    return t


def marquee_face(inset=False):
    """Striped canvas: red/cream (period 8, seamless), a gold rope along the top,
    a deep red skirt at the foot."""
    t = solid("#ffe8c8")
    for y in range(T):
        for x in range(T):
            if (x // 4) % 2 == 0:
                put(t, x, y, "#d8384a")
            if y > 4 and (x // 4) % 2 == 1 and (x % 4) == 3:
                put(t, x, y, "#e8d0b0")                 # a soft fold at each stripe edge
    for x in range(T):                                  # the rope trim
        put(t, x, 0, "#7a5a18")
        put(t, x, 1, "#e0a040" if x % 3 else "#f0d060")
        put(t, x, 2, "#c8962a" if x % 3 == 1 else "#7a5a18", 0.7)
    for y in range(11, T):                              # the skirt
        for x in range(T):
            put(t, x, y, "#8a1e2a" if y < 15 else "#4a0e18")
        for x in range(T):
            if y == 11:
                put(t, x, y, "#f0d060" if x % 4 == 1 else "#c8962a")
    if inset:                                           # a hanging lantern
        for y in range(2, 5):
            put(t, 7, y, "#3a2a1a"); put(t, 8, y, "#3a2a1a")
        for y in range(5, 10):
            for x in range(5, 11):
                put(t, x, y, "#ffc83a" if 6 <= x <= 9 and 6 <= y <= 8 else "#7a5a18")
        put(t, 7, 7, "#fff4b0"); put(t, 8, 6, "#fff4b0")
        for (x, y) in ((4, 7), (11, 7), (7, 10), (8, 4)):
            put(t, x, y, "#ffc83a", 0.35)
    return t


def marquee_band(src):
    """Dark plum canvas (a faint diagonal weave) edged in gold rope."""
    lip = lip_split(src)
    t = solid("#3a1420")
    for y in range(T):
        for x in range(T):
            if (x + y) % 4 == 0:
                put(t, x, y, "#4a1c2a")
            if lip[y, x]:
                L = lum(src)[y, x]
                put(t, x, y, "#f0d060" if L > 170 else "#c8962a" if L > 130 else "#8a6a20")
    return t


# ---- THE DREAM -------------------------------------------------------------------
BUBBLES = [(3, 4, 1.6), (11, 2, 1.0), (8, 9, 2.0), (14, 12, 1.2), (2, 13, 1.0), (12, 7, 0.8)]


def foam_floor(variant: int):
    t = solid("#e8d0a8" if variant == 0 else "#e2c89e")
    for bx, by, r in BUBBLES:
        bx = (bx + variant * 5) % T
        by = (by + variant * 3) % T
        for y in range(T + 4):
            for x in range(T + 4):
                for ox in (-T, 0, T):
                    for oy in (-T, 0, T):
                        d = math.hypot(x + ox - bx, y + oy - by)
                        if x < T and y < T and abs(d - r) < 0.55:
                            put(t, x, y, "#c8a878")
                        if x < T and y < T and abs(d - (r - 0.8)) < 0.4 and r > 1.1:
                            put(t, x, y, "#fff4dc")
    return t


def caramel_slick():
    """Glossy caramel crema: diagonal sheen streaks (period 8 → seamless)."""
    t = solid("#b87838")
    for y in range(T):
        for x in range(T):
            d = (x + y) % 8
            if d == 0:
                put(t, x, y, "#f0b870")
            elif d == 1:
                put(t, x, y, "#d89a50")
            elif d == 5:
                put(t, x, y, "#9a5e28")
    for (x, y) in ((2, 3), (10, 11), (13, 2)):
        put(t, x, y, "#fff0c8")
    return t


def porcelain_face(inset=False):
    t = solid("#f4f0e8")
    for y in range(T):
        for x in range(T):
            put(t, x, y, "#e4ded2", 0.4 * (y / T))
    for x in range(T):
        put(t, x, 0, "#c8962a"); put(t, x, 1, "#f0d060"); put(t, x, 2, "#c8962a", 0.5)
        put(t, x, T - 1, "#b8b0a4"); put(t, x, T - 2, "#d8d2c6")
    # a coffee drip down the porcelain, here and there (x 11; periodic = every tile)
    for y in range(3, 9):
        put(t, 11, y, "#6a3a1a"); put(t, 12, y, "#8a5a30", 0.6)
    put(t, 11, 9, "#6a3a1a"); put(t, 11, 10, "#6a3a1a", 0.5)
    if inset:                                           # an eye painted on the cup. it blinks.
        for y in range(5, 11):
            for x in range(3, 13):
                if ((x - 8) / 5) ** 2 + ((y - 8) / 2.6) ** 2 <= 1:
                    put(t, x, y, "#ffffff")
                if abs(((x - 8) / 5) ** 2 + ((y - 8) / 2.6) ** 2 - 1) < 0.25:
                    put(t, x, y, "#2a160c")
        for (x, y) in ((7, 7), (8, 7), (7, 8), (8, 8), (9, 8)):
            put(t, x, y, "#6a3a8a")
        put(t, 7, 7, "#ffffff")
    return t


def coffee_band(src):
    """The coffee itself: near-black brown, slow ripples; the lip becomes foam."""
    lip = lip_split(src)
    t = solid("#2a160c")
    for y in range(T):
        for x in range(T):
            if (y + round(1.4 * math.sin(x / 2.5 + y / 5.0))) % 6 == 0:
                put(t, x, y, "#4a2a16")
            if lip[y, x]:
                L = lum(src)[y, x]
                put(t, x, y, "#f0dcb8" if L > 150 else "#d8b080")
    return t


def build(name: str, floor_fn, mat_fn, face_fn, band_fn) -> None:
    src, side = load("interior_set")
    tiles = [t.copy() for t in src]
    tiles[FLOORS[0]] = floor_fn(0)
    tiles[FLOORS[1]] = floor_fn(1)
    if mat_fn:
        tiles[MAT] = mat_fn()
    face = face_fn(False)
    tiles[FACE] = face
    tiles[INSET] = face_fn(True)
    for i in FACE_ENDS:
        tiles[i] = shade_like(face, src[FACE], src[i])
    for i in BANDS:
        tiles[i] = band_fn(src[i])
    for a, b in zip(tiles, src):
        a[..., 3] = b[..., 3]
        a[a[..., 3] == 0] = 0
    # the re-drawn fills are fully opaque (the source doormat's soft, see-through
    # rim would draw a dark lattice across a whole slick of them)
    for i in (*FLOORS, MAT) if mat_fn else FLOORS:
        tiles[i][..., 3] = 255
    band = max(float(lum(tiles[i]).mean()) for i in BANDS)
    floor = min(float(lum(tiles[i]).mean()) for i in FLOORS)
    assert band < floor, f"{name}: a wall top reads lighter than the floor ({band} vs {floor})"
    im = assemble(tiles)
    MASTERS.mkdir(parents=True, exist_ok=True)
    im.save(MASTERS / f"{name}.png")
    out = SRC / f"{name}.webp"
    im.save(out, "WEBP", lossless=True, quality=100, method=6)
    back = np.asarray(Image.open(out).convert("RGBA"))
    assert (back == np.asarray(im)).all(), f"{name}: WebP not lossless"
    side = dict(side)
    side["name"] = name
    side["image"] = f"assets/tilesets/{name}.webp"
    (SRC / f"{name}.tileset.json").write_text(json.dumps(side, indent=2) + "\n")
    print(f"  {name}   band lum {band:.0f} < floor lum {floor:.0f}")


def main() -> None:
    build("brewfair_set", marquee_floor, None, marquee_face, marquee_band)
    build("brewdream_set", foam_floor, caramel_slick, porcelain_face, coffee_band)


if __name__ == "__main__":
    main()
