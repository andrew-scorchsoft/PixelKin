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


TREE_DESIGNED = {"edge_n": ("N",), "edge_s": ("S",), "edge_w": ("W",), "edge_e": ("E",),
                 "corner_nw": ("N", "W"), "corner_ne": ("N", "E"),
                 "corner_sw": ("S", "W"), "corner_se": ("S", "E")}


def tree_edge_blend(im: Image.Image, role: str) -> Image.Image:
    """Mesh a painterly tree-mass EDGE master with the flat drawn fill: keep its
    designed (bubble-crown) side, ease the inner side into the fill's base tone."""
    a = np.asarray(im.convert("RGBA")).astype(np.float64).copy()
    base = np.array(sh(TREE, 0.60), dtype=np.float64)
    designed = TREE_DESIGNED.get(role, ())
    if not designed:
        return im
    for y in range(16):
        for x in range(16):
            d = min({"N": y, "S": 15 - y, "W": x, "E": 15 - x}[e] for e in designed)
            t = max(0.0, min(1.0, (d - 6) / 7.0))
            a[y, x, :3] = a[y, x, :3] * (1 - t) + base * t
    return img(a.astype(np.int16))


def _dilate(mask: np.ndarray, it: int) -> np.ndarray:
    """4-neighbour binary dilation, `it` iterations (no scipy dependency)."""
    m = mask.copy()
    for _ in range(it):
        up = np.roll(m, 1, 0); up[0, :] = False
        dn = np.roll(m, -1, 0); dn[-1, :] = False
        lf = np.roll(m, 1, 1); lf[:, 0] = False
        rt = np.roll(m, -1, 1); rt[:, -1] = False
        m = m | up | dn | lf | rt
    return m


def tree_grass_meld(im: Image.Image, role: str, grass_im: Image.Image | None = None,
                    it: int = 4, reach: int = 13) -> Image.Image:
    """Make a tree edge/corner tile meet surrounding grass SEAMLESSLY.

    The painterly bubble-crown masters bake a thin lit halo rim + a slightly-off
    'grass' strip onto their outward (grass-facing) side, so a tree border reads
    with a pale outline where it meets the open grass. This re-grounds that strip:
    the canopy silhouette (the dark leaf mass + the crown bumps sitting on it) is
    kept; every grass-side pixel OUTSIDE that silhouette is replaced with the real
    grass fill (a 1px feather softens the join). The canopy bumps become trees on
    grass, not trees in a pale frame."""
    designed = TREE_DESIGNED.get(role, ())
    if not designed:
        return im
    a = np.asarray(im.convert("RGBA")).astype(np.float64).copy()
    g = np.asarray((grass_im or grass_fill(0)).convert("RGBA")).astype(np.float64)
    # the canopy = the dark leaf mass, dilated to absorb the crown bumps that sit
    # on its grass-facing lip (the bumps are bright, so threshold-on-dark alone
    # would drop them; dilation re-attaches them to the mass behind them).
    canopy = _dilate(a[:, :, 1] < 74, it)
    # only touch the grass-side band (within `reach` of a designed outer edge) so
    # a stray light leaf-tick deep in the mass interior is never re-grassed.
    yy, xx = np.mgrid[0:16, 0:16]
    band = np.zeros((16, 16), bool)
    for e in designed:
        band |= {"N": yy, "S": 15 - yy, "W": xx, "E": 15 - xx}[e] < reach
    repl = band & ~canopy
    a[repl, :3] = g[repl, :3]
    feather = _dilate(repl, 1) & canopy & band
    a[feather, :3] = 0.5 * a[feather, :3] + 0.5 * g[feather, :3]
    # Tuck the crown's lit lip into the grass: on the S/E/W masters the bumps sit
    # flush to the tile edge, so a bump highlight lands right on the grass seam as
    # a faint dotted line. Ease the outermost ring (and half-ease the next one) of
    # each grass-facing side toward grass so the canopy nestles into the field.
    for e in designed:
        d = {"N": yy, "S": 15 - yy, "W": xx, "E": 15 - xx}[e]
        ring0 = d == 0
        ring1 = d == 1
        a[ring0, :3] = 0.4 * a[ring0, :3] + 0.6 * g[ring0, :3]
        a[ring1, :3] = 0.75 * a[ring1, :3] + 0.25 * g[ring1, :3]
    return img(a.astype(np.int16))


# ---- glowmoss cave (Glowmoss Deep & the eastern dark interiors) ----------------
# Palette: dusk-violet rock under bioluminescent moss — the East's "dewy
# bioluminescent dark" register (walkthrough/02-east, Arc D lighting note).
CAVE = (56, 52, 74)        # cave rock anchor
MOSS = (74, 168, 124)      # glowmoss green (the living light)

# Per-variant motif layouts for the cave floor: pebble 3-dot clusters + lone
# pale chips. Hand-placed like the grass layouts; nothing within 2px of a border.
CAVEFLOOR_LAYOUTS = [
    [(4, 4, "p"), (11, 7, "c"), (6, 12, "p"), (13, 13, "c")],
    [(3, 9, "p"), (9, 3, "c"), (12, 11, "p"), (6, 14, "c")],
    [(5, 6, "c"), (12, 4, "p"), (3, 12, "c"), (10, 12, "p")],
    [(8, 5, "p"), (3, 4, "c"), (12, 9, "c"), (6, 13, "p"), (13, 3, "c")],
]


def cavefloor_fill(v: int = 0) -> Image.Image:
    """Walkable cave floor: flat violet-dark rock + structured pebble motifs."""
    a = flat(sh(CAVE, 0.94))
    dark = sh(CAVE, 0.74)
    light = sh(CAVE, 1.22, 8)
    for (x, y, kind) in CAVEFLOOR_LAYOUTS[v % len(CAVEFLOOR_LAYOUTS)]:
        if kind == "p":
            put(a, [(x, y), (x + 2, y + 1), (x + 1, y + 2)], dark)   # pebble cluster
        else:
            put(a, [(x, y)], light)                                  # pale chip
    return img(a)


def _mound(a, cx, cy, mid, light, dark, glow):
    """One rounded glowmoss mound, ~6 wide x 4 tall, anchored at its base (cx, cy)."""
    body = [(cx - 2, cy), (cx - 1, cy), (cx, cy), (cx + 1, cy), (cx + 2, cy),
            (cx - 1, cy - 1), (cx, cy - 1), (cx + 1, cy - 1),
            (cx, cy - 2)]
    crown = [(cx - 1, cy - 2), (cx + 1, cy - 2), (cx, cy - 3)]
    base = [(cx - 2, cy + 1), (cx - 1, cy + 1), (cx, cy + 1), (cx + 1, cy + 1), (cx + 2, cy + 1)]
    put(a, body, mid)
    put(a, crown, light)
    put(a, base, dark)
    put(a, [(cx, cy - 1)], glow)   # the held light at the heart


def glowmoss_fill(v: int = 0) -> Image.Image:
    """The cave ENCOUNTER tile: glowing moss mounds over a darkened bed —
    hard-edged fill-only, same classic convention as tallgrass/dunegrass."""
    a = flat(sh(CAVE, 0.58))
    mid = sh(MOSS, 0.92)
    light = sh(MOSS, 1.35, 24)
    dark = sh(MOSS, 0.42)
    glow = (214, 244, 214)
    for (cx, cy) in TG_LAYOUTS[v % len(TG_LAYOUTS)]:
        _mound(a, cx, cy, mid, light, dark, glow)
    return img(a)


def cavewall_top(v: int = 0) -> Image.Image:
    """The wall-mass surface: deep void-dark rock (the unlit mass the lamp never
    reaches), a register well BELOW the walkable floor so rooms read as carved
    light, + sparse structured crack marks."""
    a = flat(sh(CAVE, 0.58))
    dark = sh(CAVE, 0.44)
    lit = sh(CAVE, 0.92, 4)
    for i, (x, y) in enumerate(CLIFF_TOP_LAYOUTS[v % len(CLIFF_TOP_LAYOUTS)]):
        put(a, [(x, y), (x + 1, y), (x + 2, y + 1)], dark)
        if i == 0:
            put(a, [(x + 3, y - 1)], lit)                  # one crystal glint
    return img(a)


def _cavewall_face(role: str, v: int = 0) -> Image.Image:
    """edge_s / corner_s*: the visible vertical FACE — lit lip, streaked rock
    face, dark contact seam, cave floor below (the interior-wall convention)."""
    g = np.asarray(cavefloor_fill(v).convert("RGBA")).astype(np.int16)
    a = np.asarray(cavewall_top(v).convert("RGBA")).astype(np.int16).copy()
    LIP, FACE_END = 4, 12
    a[LIP, :, :3] = sh(CAVE, 1.50, 18)                     # lit lip
    face = sh(CAVE, 0.96, 6)                               # lamp-caught rock face
    streak = sh(CAVE, 0.70)
    for y in range(LIP + 1, FACE_END + 1):
        a[y, :, :3] = face
    x1, x2 = (3 + 3 * v) % 14 + 1, (10 + 3 * v) % 14 + 1
    for y in range(LIP + 1, 9):
        a[y, x1, :3] = streak
    for y in range(9, FACE_END + 1):
        a[y, x2, :3] = streak
    a[9, :, :3] = sh(CAVE, 0.78)                           # bedding crack
    a[FACE_END + 1, :, :3] = sh(CAVE, 0.30)                # contact shadow
    a[FACE_END + 2:, :] = g[FACE_END + 2:, :]              # floor below
    if role == "corner_sw":
        a[:, :2] = g[:, :2]
        a[:, 2, :3] = sh(CAVE, 0.36)
    if role == "corner_se":
        a[:, 14:] = g[:, 14:]
        a[:, 13, :3] = sh(CAVE, 0.36)
    return img(a)


def cavewall_tile(role: str, v: int = 0) -> Image.Image:
    """Any of the 13 roles for the cavewall family (the cliff convention,
    indoors: fill = wall top; S edges = the face; N/W/E = rim transitions)."""
    if role == "fill":
        return cavewall_top(v)
    if role in ("edge_s", "corner_sw", "corner_se"):
        return _cavewall_face(role, v)
    return overlay_tile(role, cavewall_top(v), cavefloor_fill(v),
                        sh(CAVE, 0.34), shade_rgb=sh(CAVE, 0.46))


# ---- glowmoss-cave decor props (transparent, deco layer) ------------------------
def glowshroom(v: int = 0) -> Image.Image:
    """A small cluster of glowing cave-shrooms — the cave's light breadcrumb."""
    a = np.zeros((16, 16, 4), dtype=np.int16)
    cap = sh(MOSS, 1.30, 20)
    capd = sh(MOSS, 0.80)
    stem = (188, 184, 200)
    glow = (224, 248, 224)
    spots = [(6, 9)] if v % 2 == 0 else [(5, 8), (10, 11)]
    for (cx, cy) in spots:
        for (x, y) in [(cx - 1, cy), (cx, cy), (cx + 1, cy)]:
            a[y % 16, x % 16] = [*cap, 255]
        a[(cy - 1) % 16, cx % 16] = [*glow, 255]
        a[(cy + 1) % 16, cx % 16] = [*stem, 255]
        a[(cy + 1) % 16, (cx + 1) % 16] = [*capd, 255]
    return img(a)


def greymoss(v: int = 0) -> Image.Image:
    """A DRAINED moss tuft — the grey the Hollowing leaves behind (B2 set
    dressing). Same mound silhouette as glowmoss, all the light gone."""
    a = np.zeros((16, 16, 4), dtype=np.int16)
    mid = (104, 106, 112)
    dark = (66, 68, 76)
    anchors = [(6, 9), (11, 12)] if v % 2 == 0 else [(5, 11), (10, 8)]
    for (cx, cy) in anchors:
        for (x, y) in [(cx - 1, cy), (cx, cy), (cx + 1, cy), (cx, cy - 1)]:
            a[y % 16, x % 16] = [*mid, 255]
        for (x, y) in [(cx - 1, cy + 1), (cx, cy + 1), (cx + 1, cy + 1)]:
            a[y % 16, x % 16] = [*dark, 255]
    return img(a)


def null_lantern() -> Image.Image:
    """The Hollowing's null-lantern: a hooded lantern on a short stake, its
    pane dark — a held absence of light. 1-tile transparent prop (collides)."""
    a = np.zeros((16, 16, 4), dtype=np.int16)
    iron = (52, 50, 62)
    rim = (92, 90, 104)
    void = (16, 14, 24)
    # stake
    for y in range(10, 15):
        a[y, 7] = [*iron, 255]
        a[y, 8] = [*iron, 255]
    # lantern body 6x6 with a dark pane
    for y in range(3, 10):
        for x in range(5, 11):
            a[y, x] = [*iron, 255]
    for y in range(4, 9):
        for x in range(6, 10):
            a[y, x] = [*void, 255]
    # hood + hanging ring, faintly lit edges so it reads in the dark
    for x in range(5, 11):
        a[3, x] = [*rim, 255]
    a[2, 7] = [*rim, 255]
    a[2, 8] = [*rim, 255]
    a[9, 5] = [*rim, 255]
    a[9, 10] = [*rim, 255]
    return img(a)


def grass_ledge_s(v: int = 0) -> Image.Image:
    """A south-facing one-way LEDGE on grass: walk-on grass above, a lit lip,
    a short earthen face, contact shadow below — the genre's hop-down tile.
    The hop behaviour rides the sidecar's `ledge: "down"` meta, the art just
    has to read as 'a small drop, this way'. Variants shift the lip's nicks."""
    a = np.zeros((16, 16, 4), dtype=np.int16)
    grass_top = GRASS
    grass_dk = sh(GRASS, 0.82)
    lip = sh(GRASS, 1.32, 10)
    face = sh(PATH, 0.92)
    face_dk = sh(PATH, 0.66)
    shadow = sh(GRASS, 0.55)
    # walk-on grass above the lip
    for y in range(0, 7):
        for x in range(16):
            a[y, x] = [*grass_top, 255]
    for (x, y) in ([(3, 2), (9, 4), (13, 1)] if v % 2 == 0 else [(5, 1), (11, 3), (2, 5)]):
        a[y, x] = [*grass_dk, 255]
    # the lit lip, nicked so it doesn't read as a ruled line
    nicks = {4, 11} if v % 2 == 0 else {7, 13}
    for x in range(16):
        a[7, x] = [*(grass_dk if x in nicks else lip), 255]
    # the earthen face (the drop), darkening downward
    for y in range(8, 13):
        for x in range(16):
            a[y, x] = [*(face if y < 11 else face_dk), 255]
    for (x, y) in ([(2, 9), (8, 10), (13, 9)] if v % 2 == 0 else [(5, 9), (10, 10)]):
        a[y, x] = [*face_dk, 255]
    # contact shadow onto the grass below
    for y in range(13, 16):
        for x in range(16):
            a[y, x] = [*(shadow if y == 13 else grass_dk if y == 14 else grass_top), 255]
    return img(a)


def sand_ledge_s(v: int = 0) -> Image.Image:
    """The grass ledge's SAND-context sibling — a low dune bank with a lit
    crest, a short sandy face and a contact shadow, for one-way hops across
    tidal flats / dune routes (same `ledge: "down"` meta; context-correct
    family rule, level-design §11 rule 8)."""
    a = np.zeros((16, 16, 4), dtype=np.int16)
    sand_top = SAND
    sand_dk = sh(SAND, 0.84)
    lip = sh(SAND, 1.28, 12)
    face = sh(SAND, 0.78)
    face_dk = sh(SAND, 0.6)
    shadow = sh(SAND, 0.55)
    for y in range(0, 7):
        for x in range(16):
            a[y, x] = [*sand_top, 255]
    for (x, y) in ([(4, 2), (10, 4), (14, 1)] if v % 2 == 0 else [(6, 1), (12, 3), (3, 5)]):
        a[y, x] = [*sand_dk, 255]
    nicks = {5, 12} if v % 2 == 0 else {8, 14}
    for x in range(16):
        a[7, x] = [*(sand_dk if x in nicks else lip), 255]
    for y in range(8, 13):
        for x in range(16):
            a[y, x] = [*(face if y < 11 else face_dk), 255]
    for (x, y) in ([(3, 9), (9, 10), (14, 9)] if v % 2 == 0 else [(6, 9), (11, 10)]):
        a[y, x] = [*face_dk, 255]
    for y in range(13, 16):
        for x in range(16):
            a[y, x] = [*(shadow if y == 13 else sand_dk if y == 14 else sand_top), 255]
    return img(a)


def cave_ladder_down() -> Image.Image:
    """A ladder-pit: a dark floor opening with the ladder's top rungs showing —
    the cave-dungeon DESCENT verb (level-design §11a). Transparent prop laid on
    cavefloor; the warp rides the tile."""
    a = np.zeros((16, 16, 4), dtype=np.int16)
    void = (12, 10, 20)
    rimlit = sh(CAVE, 1.45, 12)
    rimdk = sh(CAVE, 0.55)
    rail = (168, 142, 96)
    raildk = (118, 96, 62)
    # the pit: a rounded 12x10 opening
    for y in range(4, 14):
        for x in range(2, 14):
            if (x in (2, 13) and y in (4, 13)):
                continue  # rounded corners
            a[y, x] = [*void, 255]
    # rim: lit on the N lip (light from above), dark on the S
    for x in range(3, 13):
        a[3, x] = [*rimlit, 255]
        a[14, x] = [*rimdk, 255]
    for y in range(4, 14):
        a[y, 1] = [*rimdk, 255]
        a[y, 14] = [*rimdk, 255]
    # the ladder's top: two rails + three rungs sinking into the dark
    for y in range(5, 13):
        a[y, 6] = [*(rail if y < 9 else raildk), 255]
        a[y, 9] = [*(rail if y < 9 else raildk), 255]
    for y in (6, 9, 12):
        for x in (7, 8):
            a[y, x] = [*(rail if y < 9 else raildk), 255]
    return img(a)


def cave_ladder_up() -> Image.Image:
    """A standing ladder against the rock — the matching ASCENT verb on the
    floor below. Transparent prop; the warp rides the tile."""
    a = np.zeros((16, 16, 4), dtype=np.int16)
    rail = (168, 142, 96)
    raildk = (118, 96, 62)
    rock = sh(CAVE, 0.75)
    # a shadowed rock back-plate so the ladder reads against any floor
    for y in range(1, 15):
        for x in range(4, 12):
            a[y, x] = [*rock, 255]
    # rails
    for y in range(1, 15):
        a[y, 5] = [*rail, 255]
        a[y, 10] = [*rail, 255]
    # rungs every 3px, darker toward the bottom
    for y in (2, 5, 8, 11, 14):
        for x in range(6, 10):
            a[y, x] = [*(rail if y < 9 else raildk), 255]
    return img(a)


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
        [cavefloor_fill(i) for i in range(4)],
        [glowmoss_fill(i) for i in range(4)],
        [cavewall_tile(r) for r in ("edge_n", "fill", "edge_s", "corner_sw")],
        [glowshroom(0), glowshroom(1), greymoss(0), null_lantern()],
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
