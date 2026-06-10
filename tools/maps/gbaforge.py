#!/usr/bin/env python3
"""
gbaforge — deterministic, *structured* GBA-register terrain tiles.

Why this exists: the first-generation fills were AI renders cured with seam
passes. They tiled, but up close they read as random per-pixel NOISE — speckle
grass, gravel paths, slate-static cliffs. Cartridge-era ground art is the
opposite: a FLAT base colour carrying a few deliberate, repeated MOTIFS
(grass ticks, dot clusters, strata lines), with crisp 1px-bordered rounded
transitions. Structure, not noise — that's most of what "looks like a GBA
game" means for terrain.

This module DRAWS those tiles in code:
  * grass / path / sand fills: flat base + hand-placed motif marks (variants
    are alternative motif layouts, never jitter noise)
  * tall grass: bold staggered blade-fans over a darkened bed (encounter tile)
  * path / sand transitions: rounded-corner composites over grass with a crisp
    1px dark border + soft inner shading (all 13 roles + strips)
  * water: flat animated fill (drifting light dashes) + scalloped foam
    shoreline against sand
  * cliff: flat strata face, lit plateau rim, walled S/W/E edges

Palette anchors are SAMPLED from the existing set (the dusk mood is canon);
shades are fixed ratios of the anchor so families stay in harmony.

Used by build_shared_overworld.py as a name-keyed override in its write loop —
tile order/indices never change, so existing maps pick the art up for free.

Preview:  ./venv/bin/python tools/maps/gbaforge.py /tmp/gbaforge_preview.png
"""
from __future__ import annotations

import numpy as np
from PIL import Image

# ---- palette anchors (sampled from the proven set; dusk canon) ---------------
GRASS = (43, 107, 101)
PATH = (116, 99, 70)
SAND = (208, 183, 142)     # slightly muted vs the old glowy beach
WATER = (45, 81, 117)
CLIFF = (84, 96, 112)
TREE = (31, 64, 54)


def sh(rgb, k: float, add: int = 0):
    """Shade an anchor: multiply + bias, clamped."""
    return tuple(int(max(0, min(255, c * k + add))) for c in rgb)


def flat(rgb) -> np.ndarray:
    a = np.zeros((16, 16, 4), dtype=np.int16)
    a[..., :3] = rgb
    a[..., 3] = 255
    return a


def img(a: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def put(a, pts, rgb):
    for (x, y) in pts:
        a[y % 16, x % 16, :3] = rgb


# ---- grass ------------------------------------------------------------------
# Motif: a small two-blade "tick" (the classic ground mark) + lone light dots.
TICK = [(0, 1), (1, 0), (2, 1), (3, 0)]          # ~4x2 zigzag mark

# Per-variant motif layouts (x, y, kind). Hand-placed: no row/col alignment,
# nothing within 2px of the border (keeps every variant seam-free by design).
GRASS_LAYOUTS = [
    [(3, 3, "t"), (10, 6, "t"), (5, 11, "t"), (12, 13, "d")],
    [(8, 2, "t"), (2, 8, "t"), (11, 10, "t"), (5, 14, "d"), (13, 4, "d")],
    [(5, 4, "t"), (12, 7, "d"), (3, 12, "t"), (9, 12, "t")],
    [(2, 5, "d"), (9, 4, "t"), (4, 9, "t"), (11, 13, "t"), (13, 2, "d")],
]


def grass_fill(v: int = 0) -> Image.Image:
    a = flat(GRASS)
    dark = sh(GRASS, 0.82)
    light = sh(GRASS, 1.14, 4)
    for (x, y, kind) in GRASS_LAYOUTS[v % len(GRASS_LAYOUTS)]:
        if kind == "t":
            put(a, [(x + dx, y + dy) for (dx, dy) in TICK], dark)
        else:
            put(a, [(x, y)], light)
    return img(a)


# ---- tall grass (encounter tile) ---------------------------------------------
def _fan(a, cx, cy, mid, light, dark):
    """One bold blade-fan clump, ~7 wide x 6 tall, anchored at its base (cx, cy)."""
    body = [(cx - 2, cy), (cx - 1, cy), (cx, cy), (cx + 1, cy), (cx + 2, cy),
            (cx - 1, cy - 1), (cx, cy - 1), (cx + 1, cy - 1),
            (cx - 3, cy - 1), (cx + 3, cy - 1),
            (cx - 2, cy - 2), (cx, cy - 2), (cx + 2, cy - 2),
            (cx, cy - 3)]
    tips = [(cx, cy - 4), (cx - 2, cy - 3), (cx + 2, cy - 3),
            (cx - 3, cy - 2), (cx + 3, cy - 2)]
    base = [(cx - 1, cy + 1), (cx, cy + 1), (cx + 1, cy + 1)]
    put(a, body, mid)
    put(a, tips, light)
    put(a, base, dark)


TG_LAYOUTS = [  # blade-fan base anchors per variant (staggered rows)
    [(4, 6), (12, 7), (8, 13)],
    [(5, 7), (12, 5), (3, 13), (11, 14)],
    [(4, 5), (11, 7), (7, 12), (14, 13)],
    [(6, 6), (13, 6), (3, 12), (10, 13)],
]


def tallgrass_fill(v: int = 0) -> Image.Image:
    a = flat(sh(GRASS, 0.72))
    mid = sh(GRASS, 1.12, 4)
    light = sh(GRASS, 1.45, 16)
    dark = sh(GRASS, 0.45)
    for (cx, cy) in TG_LAYOUTS[v % len(TG_LAYOUTS)]:
        _fan(a, cx, cy, mid, light, dark)
    return img(a)


def dunegrass_fill(v: int = 0) -> Image.Image:
    """Tall DRY grass on the tidal flats: pale wind-bent tussocks over a damp
    sand bed. Same hard-edged encounter-tile convention as tallgrass, sand
    context — so a crossing on the dunes doesn't ring itself with green."""
    a = flat(sh(SAND, 0.80))
    mid = sh(PATH, 1.30, 10)
    light = sh(PATH, 1.70, 26)
    dark = sh(PATH, 0.62)
    for (cx, cy) in TG_LAYOUTS[v % len(TG_LAYOUTS)]:
        _fan(a, cx, cy, mid, light, dark)
    return img(a)


# ---- path & sand fills --------------------------------------------------------
PATH_LAYOUTS = [
    [(4, 4), (11, 7), (6, 12), (13, 2)],
    [(3, 9), (9, 3), (13, 12), (7, 14)],
    [(5, 6), (12, 9), (2, 13), (10, 5)],
]
SAND_LAYOUTS = [
    [(4, 5), (11, 3), (7, 10), (13, 13)],
    [(3, 11), (9, 6), (13, 8), (5, 2)],
    [(6, 4), (12, 11), (2, 7), (9, 14)],
]


def path_fill(v: int = 0) -> Image.Image:
    a = flat(PATH)
    dark = sh(PATH, 0.84)
    light = sh(PATH, 1.12, 4)
    for i, (x, y) in enumerate(PATH_LAYOUTS[v % len(PATH_LAYOUTS)]):
        put(a, [(x, y), (x + 1, y)], dark if i % 2 == 0 else light)
    return img(a)


def sand_fill(v: int = 0) -> Image.Image:
    a = flat(SAND)
    dark = sh(SAND, 0.88)
    for (x, y) in SAND_LAYOUTS[v % len(SAND_LAYOUTS)]:
        put(a, [(x, y), (x + 2, y + 1), (x + 1, y + 2)], dark)  # 3-dot cluster
    return img(a)


# ---- rounded-corner overlay machinery -----------------------------------------
# Mask semantics: True = OUTER terrain (what the family sits on) shows here.
ROLES_OUTER = {
    "corner_nw": ("N", "W"), "edge_n": ("N",), "corner_ne": ("N", "E"),
    "edge_w": ("W",), "fill": (), "edge_e": ("E",),
    "corner_sw": ("S", "W"), "edge_s": ("S",), "corner_se": ("S", "E"),
    "strip_h": ("N", "S"), "strip_v": ("W", "E"),
}
INNER_Q = {"inner_nw": (0, 0), "inner_ne": (1, 0), "inner_sw": (0, 1), "inner_se": (1, 1)}


def overlay_mask(role: str, t: int = 3, r: int = 3) -> np.ndarray:
    """16x16 bool mask, True = outer terrain. Convex corners are rounded with
    radius r; inner_* roles bite a rounded notch of radius t into the corner."""
    m = np.zeros((16, 16), dtype=bool)
    if role in INNER_Q:
        qx, qy = INNER_Q[role]
        cx = t if qx == 0 else 15 - t
        cy = t if qy == 0 else 15 - t
        for y in range(16):
            for x in range(16):
                in_q = (x < t if qx == 0 else x > 15 - t) and (y < t if qy == 0 else y > 15 - t)
                if in_q and (x - cx) ** 2 + (y - cy) ** 2 >= t * t:
                    m[y, x] = True
        return m
    edges = ROLES_OUTER[role]
    if not edges:
        return m
    for y in range(16):
        for x in range(16):
            d = {"N": y, "S": 15 - y, "W": x, "E": 15 - x}
            if min(d[e] for e in edges) < t:
                m[y, x] = True
    # round convex corners (two adjacent active edges)
    pairs = [p for p in (("N", "W"), ("N", "E"), ("S", "W"), ("S", "E"))
             if p[0] in edges and p[1] in edges]
    for (ev, eh) in pairs:
        cy = t + r - 1 if ev == "N" else 15 - t - r + 1
        cx = t + r - 1 if eh == "W" else 15 - t - r + 1
        for y in range(16):
            for x in range(16):
                qy = y < t + r if ev == "N" else y > 15 - t - r
                qx = x < t + r if eh == "W" else x > 15 - t - r
                if qx and qy and (x - cx) ** 2 + (y - cy) ** 2 > r * r:
                    m[y, x] = True
    return m


def _border_of(mask: np.ndarray) -> np.ndarray:
    """Inner pixels 4-adjacent to an outer pixel (the 1px transition line)."""
    inner = ~mask
    b = np.zeros_like(mask)
    up = np.roll(mask, 1, 0); up[0, :] = False
    dn = np.roll(mask, -1, 0); dn[-1, :] = False
    lf = np.roll(mask, 1, 1); lf[:, 0] = False
    rt = np.roll(mask, -1, 1); rt[:, -1] = False
    b[inner & (up | dn | lf | rt)] = True
    return b


def overlay_tile(role: str, inner_im: Image.Image, outer_im: Image.Image,
                 border_rgb, t: int = 3, r: int = 3,
                 shade_rgb=None) -> Image.Image:
    """Compose one transition tile: inner terrain over outer, crisp 1px border,
    optional 1px shade just inside the border (reads as the lip of the cut)."""
    m = overlay_mask(role, t, r)
    a = np.asarray(inner_im.convert("RGBA")).astype(np.int16).copy()
    o = np.asarray(outer_im.convert("RGBA")).astype(np.int16)
    a[m] = o[m]
    b = _border_of(m)
    a[b, :3] = border_rgb
    if shade_rgb is not None:
        sb = _border_of(m | b)
        a[sb & ~m & ~b, :3] = shade_rgb
    return img(a)


def overlay_family(inner_fn, outer_fn, border_rgb, shade_rgb=None,
                   t: int = 3, r: int = 3) -> dict:
    """All 13 roles + strips. inner_fn/outer_fn: variant index -> fill Image."""
    fam = {}
    roles = list(ROLES_OUTER.keys()) + list(INNER_Q.keys())
    for role in roles:
        fam[role] = overlay_tile(role, inner_fn(0), outer_fn(0), border_rgb,
                                 t=t, r=r, shade_rgb=shade_rgb)
    return fam


# ---- water -------------------------------------------------------------------
# Fill: flat deep water + sparse 2px light dashes; 3 animation frames drift them.
WATER_DASHES = [(3, 3), (11, 6), (6, 10), (13, 13), (1, 14)]


def water_fill(frame: int = 0) -> Image.Image:
    a = flat(WATER)
    light = sh(WATER, 1.35, 10)
    faint = sh(WATER, 1.18, 6)
    for i, (x, y) in enumerate(WATER_DASHES):
        ph = (i + frame) % 3
        if ph == 0:
            put(a, [(x, y), (x + 1, y)], light)
        elif ph == 1:
            put(a, [(x + 1, y), (x + 2, y)], faint)
        # ph == 2: dash dark (gone) this frame
    return img(a)


def water_edge(role: str, outer_im: Image.Image | None = None,
               t: int = 3, r: int = 3, phase: int = 0) -> Image.Image:
    """Shoreline tile: sand (or given outer fill) above a scalloped 1px foam line,
    1px pale shallow, then open water. Edge roles only; fill handled separately."""
    outer = outer_im if outer_im is not None else sand_fill(0)
    m = overlay_mask(role, t, r)
    a = np.asarray(water_fill(0).convert("RGBA")).astype(np.int16).copy()
    o = np.asarray(outer.convert("RGBA")).astype(np.int16)
    a[m] = o[m]
    foam = _border_of(m)            # water px touching land
    shallow = _border_of(m | foam)  # next ring in
    wet = _border_of(~(m))          # land px touching water -> wet sand
    a[shallow & ~m & ~foam, :3] = sh(WATER, 1.5, 26)
    # scallop the foam: skip every 5th px along its run so the line breathes
    fy, fx = np.where(foam)
    for (y, x) in zip(fy, fx):
        if (x + y + 2 * phase) % 5 == 4:
            a[y, x, :3] = sh(WATER, 1.5, 26)
        else:
            a[y, x, :3] = (228, 234, 236)
    wm = wet & m
    a[wm, :3] = (np.clip(a[wm, :3] * 0.82, 0, 255)).astype(np.int16)
    return img(a)


# ---- cliff -------------------------------------------------------------------
# The interior-wall convention, outdoors (art-style §14): a cliff mass is a
# PLATEAU TOP you look down on, with a visible vertical FACE on its south
# boundary (lit lip -> shaded face -> dark contact -> ground). N/W/E boundaries
# are rim transitions against the ground (no face — those sides point away).
CLIFF_TOP_LAYOUTS = [
    [(4, 4), (11, 7), (6, 12)],
    [(9, 3), (3, 9), (12, 12)],
    [(6, 6), (12, 4), (4, 13)],
]


def cliff_top(v: int = 0) -> Image.Image:
    """The plateau surface: flat rock-top + sparse structured crack marks."""
    a = flat(sh(CLIFF, 1.04, 4))
    dark = sh(CLIFF, 0.84)
    lit = sh(CLIFF, 1.22, 8)
    for i, (x, y) in enumerate(CLIFF_TOP_LAYOUTS[v % len(CLIFF_TOP_LAYOUTS)]):
        put(a, [(x, y), (x + 1, y), (x + 2, y + 1)], dark)   # crack mark
        if i == 0:
            put(a, [(x + 3, y - 1)], lit)                     # one chip glint
    return img(a)


def cliff_face_tile(role: str, v: int = 0) -> Image.Image:
    """edge_s / corner_s*: plateau lip, then the vertical face (streaked), dark
    contact seam, ground. The vertical light ladder IS the height cue."""
    g = np.asarray(grass_fill(v).convert("RGBA")).astype(np.int16)
    a = np.asarray(cliff_top(v).convert("RGBA")).astype(np.int16).copy()
    LIP, FACE_END = 4, 12
    a[LIP, :, :3] = sh(CLIFF, 1.40, 16)                      # lit lip
    face = sh(CLIFF, 0.72)
    streak = sh(CLIFF, 0.56)
    for y in range(LIP + 1, FACE_END + 1):
        a[y, :, :3] = face
    # two PARTIAL vertical cracks (staggered, half-height — full-height bars
    # read as a grate) + one bedding crack
    x1, x2 = (3 + 3 * v) % 14 + 1, (10 + 3 * v) % 14 + 1
    for y in range(LIP + 1, 9):
        a[y, x1, :3] = streak
    for y in range(9, FACE_END + 1):
        a[y, x2, :3] = streak
    a[9, :, :3] = sh(CLIFF, 0.60)
    a[FACE_END + 1, :, :3] = sh(CLIFF, 0.34)                 # contact shadow
    a[FACE_END + 2:, :] = g[FACE_END + 2:, :]                # ground below
    if role == "corner_sw":
        a[:, :2] = g[:, :2]
        a[:, 2, :3] = sh(CLIFF, 0.45)
    if role == "corner_se":
        a[:, 14:] = g[:, 14:]
        a[:, 13, :3] = sh(CLIFF, 0.45)
    return img(a)


def cliff_tile(role: str, v: int = 0) -> Image.Image:
    """Any of the 13 roles + strips for the cliff family."""
    if role == "fill":
        return cliff_top(v)
    if role in ("edge_s", "corner_sw", "corner_se"):
        return cliff_face_tile(role, v)
    # rim transitions (plateau against ground) for N/W/E + inner corners + strips
    return overlay_tile(role, cliff_top(v), grass_fill(v),
                        sh(CLIFF, 0.45), shade_rgb=sh(CLIFF, 0.80))


# ---- tree canopy (terrain mass fill) -------------------------------------------
def tree_fill(v: int = 0) -> Image.Image:
    """Structured canopy: staggered rows of round leaf-clump bumps (lit crown arc,
    dark crease under) over a deep base — the classic hedge/forest mass texture.
    Toroidal by construction (bump centres on a fixed staggered lattice)."""
    # The mass is UNDERCANOPY: the bumpy edge tiles + crown objects carry the
    # shape, so the fill stays dark and calm — sparse light leaf-ticks only.
    a = flat(sh(TREE, 0.60))
    leaf = sh(TREE, 1.22, 4)
    deep = sh(TREE, 0.40)
    for (x, y, kind) in GRASS_LAYOUTS[v % len(GRASS_LAYOUTS)]:
        if kind == "t":
            put(a, [(x + dx, y + dy) for (dx, dy) in TICK], leaf)
        else:
            put(a, [(x, y), (x + 1, y)], deep)
    return img(a)


def tree_edge_blend(im: Image.Image, role: str) -> Image.Image:
    """Mesh a painterly tree-mass EDGE master with the flat drawn fill: keep its
    designed (bubble-crown) side, ease the inner side into the fill's base tone."""
    a = np.asarray(im.convert("RGBA")).astype(np.float64).copy()
    base = np.array(sh(TREE, 0.60), dtype=np.float64)
    designed = {"edge_n": ("N",), "edge_s": ("S",), "edge_w": ("W",), "edge_e": ("E",),
                "corner_nw": ("N", "W"), "corner_ne": ("N", "E"),
                "corner_sw": ("S", "W"), "corner_se": ("S", "E")}.get(role, ())
    if not designed:
        return im
    for y in range(16):
        for x in range(16):
            d = min({"N": y, "S": 15 - y, "W": x, "E": 15 - x}[e] for e in designed)
            t = max(0.0, min(1.0, (d - 6) / 7.0))
            a[y, x, :3] = a[y, x, :3] * (1 - t) + base * t
    return img(a.astype(np.int16))


# ---- preview ------------------------------------------------------------------
def _preview(out_path: str) -> None:
    rows = [
        [grass_fill(i) for i in range(4)],
        [tallgrass_fill(i) for i in range(4)],
        [path_fill(i) for i in range(3)] + [sand_fill(0)],
        [overlay_tile(r, path_fill(0), grass_fill(0), sh(PATH, 0.55),
                      shade_rgb=sh(PATH, 0.9)) for r in
         ("corner_nw", "edge_n", "fill", "inner_se")],
        [water_fill(i) for i in range(3)] + [water_edge("edge_n")],
        [cliff_tile(r) for r in ("edge_n", "fill", "edge_s", "corner_sw")],
        [dunegrass_fill(i) for i in range(4)],
    ]
    S = 6
    W = max(len(r) for r in rows)
    sheet = Image.new("RGBA", (W * 17 * S, len(rows) * 17 * S), (24, 26, 32, 255))
    for ry, row in enumerate(rows):
        for rx, t in enumerate(row):
            sheet.paste(t.resize((16 * S, 16 * S), Image.NEAREST), (rx * 17 * S, ry * 17 * S))
    sheet.save(out_path)
    print(f"preview -> {out_path}")


if __name__ == "__main__":
    import sys
    _preview(sys.argv[1] if len(sys.argv) > 1 else "/tmp/gbaforge_preview.png")
