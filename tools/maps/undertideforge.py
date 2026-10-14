#!/usr/bin/env python3
"""
undertideforge — the UNDERTIDE's drawn kit (10-the-farlamp-isles.md Part I, lane C2).

The Undertide is the sea-cave maze under the Farlamp Isles; the Drowned Lamp is
the sunken lighthouse floor at its bottom. The shared overworld set is FROZEN,
so the sea-cave's own surfaces live in an accent set on the seams_set pattern
(`undertide_set`), and its props are object masters in their OWN folder
(`assets/tilesets/undertide/objects/`, packed by pack_objects.py -> `undertide_*`).

Everything is DRAWN in code in gbaforge's register (flat anchors, 1px ink,
deliberate repeated motifs — never noise).

Tiles (`undertide_set`):
  tidepool_<role>   calm sea shallows over wet cave floor (13 roles + strips +
                    ends + single): swum with Tidecall, rolls `water` encounters.
  surge_<role>      the SURGE: white water churning over a drop (collides,
                    never swum) — the walls of the tide-race maze.
  race_<dir>        a TIDE-RACE lane: calmer water with current chevrons that
                    drift `dir` (3 frames). A `kind:'rail'` flow rides on it.
                    Swum like the shallows; builders keep water zones off it.
  race_fork         a junction pool: a slow swirl (the bells swing its current).
  wetstone_0..2     barnacled wet cave floor (ground).
  barnacle_a/b, shell_a, wrack_a, glass_a/b   floor decor overlays.

Objects (`undertide_*`, 16px multiples):
  bell / bell_rung        a tide-bell on a barnacled post (1x2)
  post_white / post_red   a race-post: white pennant = the current runs on,
                          red = it turns (1x1) — the junction tell
  logbook                 a sea-chest with the keeper's sodden logbook (1x1)
  fogglass / fogglass_empty   the keeper's fog-glass on its stand (1x2)
  lamp_dark / lamp_lit    THE FARLAMP: the drowned lamp-house lantern (4x5)
  camp                    the keeper's dry-ledge camp (2x2)
  kelp                    a tall kelp frond (1x2, walk-under)
  pillar                  a fallen length of lighthouse masonry (2x3)
  glassheap               a heap of drowned lamp-glass (2x1)
  wreck / stack / kelpcrown / mast   things breaking the surge (2x2, 1x2, 2x1, 1x3)
  tidelamp / tidelamp_lit the race-marking lamps; lit once `flag:isles_dawn` (1x2)
  niche                   a keeper's dry niche in the rock — IV's rest point (2x2)

Run:  python3 tools/maps/undertideforge.py      (then pack_objects.py)
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

import gbaforge
from gbaforge import sh, flat, put, img, CAVE

REPO = Path(__file__).resolve().parents[2]
BASE = REPO / "assets" / "tilesets" / "undertide"
TILES_DIR = BASE / "set_tiles"
OBJ_DIR = BASE / "objects"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

INK = (16, 18, 28)
SEA = (40, 98, 118)            # lit sea-cave water
SEA_DK = (28, 70, 92)
SEA_LT = (92, 168, 176)
FOAM = (220, 238, 234)
SURGE = (22, 48, 66)           # the dark churn
SURGE_LT = (64, 120, 138)
CHEV = (150, 220, 214)         # current chevrons
WET = (52, 56, 72)             # wet cave stone
BARN = (176, 168, 150)         # barnacle shell
BARN_DK = (110, 102, 92)
KELP = (64, 112, 70)
KELP_LT = (112, 160, 92)
KELP_DK = (34, 66, 44)
BRASS = (196, 150, 70)
BRASS_LT = (240, 204, 120)
BRASS_DK = (122, 84, 40)
IRON = (70, 74, 88)
IRON_LT = (120, 126, 142)
IRON_DK = (40, 42, 54)
WOOD = (104, 74, 50)
WOOD_DK = (66, 46, 32)
WOOD_LT = (146, 108, 72)
STONE = (150, 144, 128)
STONE_LT = (196, 190, 172)
STONE_DK = (92, 88, 80)
GLOW = (255, 226, 140)
GLOW_HOT = (255, 248, 214)
GLASS = (120, 170, 186)
GLASS_LT = (196, 232, 236)
RED = (196, 62, 52)


def clear(w: int = 16, h: int = 16) -> np.ndarray:
    return np.zeros((h, w, 4), dtype=np.int16)


def px(a, x, y, rgb, alpha=255):
    h, w = a.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        a[y, x, :3] = rgb
        a[y, x, 3] = alpha


def rect(a, x0, y0, x1, y1, rgb, alpha=255):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(a, x, y, rgb, alpha)


def ellipse(a, cx, cy, rx, ry, rgb, alpha=255):
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                px(a, x, y, rgb, alpha)


def outline(a, rgb=INK):
    """1px ink round every opaque region (the GBA object convention)."""
    h, w = a.shape[:2]
    op = a[..., 3] > 0
    out = []
    for y in range(h):
        for x in range(w):
            if op[y, x]:
                continue
            for (nx, ny) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < w and 0 <= ny < h and op[ny, nx]:
                    out.append((x, y))
                    break
    for (x, y) in out:
        px(a, x, y, rgb)


def to_im(a) -> Image.Image:
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# ---- masks for every blob role (incl. ends + single) -------------------------------
OPEN = {
    "corner_nw": "NW", "edge_n": "N", "corner_ne": "NE", "edge_w": "W", "fill": "",
    "edge_e": "E", "corner_sw": "SW", "edge_s": "S", "corner_se": "SE",
    "strip_h": "NS", "strip_v": "WE", "end_n": "NWE", "end_s": "SWE",
    "end_w": "WNS", "end_e": "ENS", "single": "NSWE",
}
INNER = ["inner_nw", "inner_ne", "inner_sw", "inner_se"]
ROLES = list(OPEN) + INNER


def mask(role: str, t: int = 3, r: int = 4) -> np.ndarray:
    """True = OUTER (the floor round the water). Open sides `t` deep, convex
    corners rounded with radius r."""
    if role in INNER:
        return gbaforge.overlay_mask(role, t, 3)
    sides = OPEN[role]
    m = np.zeros((16, 16), dtype=bool)
    for y in range(16):
        for x in range(16):
            d = {"N": y, "S": 15 - y, "W": x, "E": 15 - x}
            if any(d[s] < t for s in sides):
                m[y, x] = True
    for (ev, eh) in (("N", "W"), ("N", "E"), ("S", "W"), ("S", "E")):
        if ev in sides and eh in sides:
            cy = t + r - 1 if ev == "N" else 15 - t - r + 1
            cx = t + r - 1 if eh == "W" else 15 - t - r + 1
            for y in range(16):
                for x in range(16):
                    qy = y < t + r if ev == "N" else y > 15 - t - r
                    qx = x < t + r if eh == "W" else x > 15 - t - r
                    if qx and qy and (x - cx) ** 2 + (y - cy) ** 2 > r * r:
                        m[y, x] = True
    return m


def ring(m: np.ndarray) -> np.ndarray:
    """Inner px 4-adjacent to the outer region."""
    return gbaforge._border_of(m)


# ---- floors ------------------------------------------------------------------------
WET_LAYOUTS = [
    [(3, 4, "b"), (11, 9, "s"), (6, 12, "c"), (13, 2, "c")],
    [(10, 3, "b"), (3, 10, "c"), (12, 12, "s"), (6, 6, "c")],
    [(5, 3, "s"), (12, 6, "c"), (4, 13, "b"), (10, 11, "c")],
]


def wetstone(v: int = 0) -> Image.Image:
    """Barnacled wet sea-cave floor: the cave rock gone blue-wet, a barnacle
    cluster, a salt streak, pale chips."""
    a = flat(sh(WET, 1.0))
    dark = sh(WET, 0.72)
    light = sh(WET, 1.35, 8)
    for (x, y, k) in WET_LAYOUTS[v % 3]:
        if k == "b":
            put(a, [(x, y), (x + 2, y), (x + 1, y + 1)], BARN_DK)
            put(a, [(x + 1, y)], BARN)
        elif k == "s":
            put(a, [(x, y), (x + 1, y), (x + 2, y + 1)], light)
        else:
            put(a, [(x, y)], light)
            put(a, [(x + 1, y + 1)], dark)
    return img(a)


def floor_im(v: int = 0) -> Image.Image:
    return gbaforge.cavefloor_fill(v)


# ---- water -------------------------------------------------------------------------
POOL_DASHES = [(2, 3), (10, 5), (5, 9), (12, 12), (1, 13)]


def pool_fill(frame: int = 0, v: int = 0) -> np.ndarray:
    a = flat(SEA)
    light = SEA_LT
    faint = sh(SEA, 1.22, 6)
    dashes = POOL_DASHES if v == 0 else [(x ^ 7, (y + 5) % 15) for (x, y) in POOL_DASHES]
    for i, (x, y) in enumerate(dashes):
        ph = (i + frame) % 3
        if ph == 0:
            put(a, [(x, y), (x + 1, y)], light)
        elif ph == 1:
            put(a, [(x + 1, y), (x + 2, y)], faint)
    return a


def pool_tile(role: str, frame: int = 0) -> Image.Image:
    """Shallows over wet floor: floor lip, a scalloped foam line, a pale ring."""
    if role == "fill":
        return img(pool_fill(frame))
    m = mask(role)
    a = pool_fill(frame)
    o = np.asarray(wetstone(0).convert("RGBA")).astype(np.int16)
    a[m] = o[m]
    foam = ring(m)
    shallow = ring(m | foam)
    a[shallow & ~m & ~foam, :3] = sh(SEA, 1.45, 22)
    fy, fx = np.where(foam)
    for (y, x) in zip(fy, fx):
        a[y, x, :3] = sh(SEA, 1.5, 26) if (x + y) % 5 == 4 else FOAM
    lip = ring(~m) & m
    a[lip, :3] = sh(WET, 0.62)
    return img(a)


CRESTS = [[(2, 3), (9, 6), (4, 11), (12, 13)], [(6, 2), (13, 8), (1, 9), (8, 13)],
          [(11, 1), (3, 6), (10, 10), (5, 14)]]


def surge_fill(frame: int = 0, v: int = 0) -> np.ndarray:
    """The churn: dark sea with curled white crests that roll over 3 frames."""
    a = flat(SURGE)
    put(a, [((x * 5 + y * 3 + v) % 16, (y * 7 + x + v * 3) % 16)
            for (x, y) in [(1, 2), (5, 4), (3, 9), (11, 12), (9, 1)]], sh(SURGE, 0.7))
    for i, (x, y) in enumerate(CRESTS[(frame + v) % 3]):
        put(a, [(x, y + 1), (x + 1, y), (x + 2, y), (x + 3, y + 1)], SURGE_LT)
        put(a, [(x + 1, y), (x + 2, y)], FOAM)
        if i % 2 == 0:
            put(a, [(x + 3, y + 2)], sh(FOAM, 0.8))
    return a


def surge_tile(role: str, frame: int = 0, v: int = 0) -> Image.Image:
    """Surge over cave floor: the floor's lit lip, then a thick broken foam
    collar where the churn slaps the rock."""
    if role == "fill":
        return img(surge_fill(frame))
    m = mask(role, t=3, r=4)
    a = surge_fill(frame, v)
    frame = frame + 2 * v
    o = np.asarray(floor_im(0).convert("RGBA")).astype(np.int16)
    a[m] = o[m]
    collar = ring(m)
    collar2 = ring(m | collar)
    fy, fx = np.where(collar)
    for (y, x) in zip(fy, fx):
        a[y, x, :3] = FOAM if (x * 3 + y + frame) % 4 else SURGE_LT
    fy, fx = np.where(collar2 & ~m)
    for (y, x) in zip(fy, fx):
        if (x + y * 2 + frame) % 3 == 0:
            a[y, x, :3] = FOAM
        else:
            a[y, x, :3] = SURGE_LT
    lip = ring(~m) & m
    a[lip, :3] = sh(CAVE, 1.55, 18)
    return img(a)


def race_tile(direction: str, frame: int = 0) -> Image.Image:
    """A tide-race lane: water a shade brighter than the shallows, two rows of
    chevrons pointing `direction`, drifting a third of a tile per frame."""
    a = flat(sh(SEA, 1.08, 4))
    put(a, [(1, 1), (14, 6), (7, 14)], sh(SEA, 0.82))
    shift = (frame * 5) % 16
    chev = [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)]       # a '>' pointing right
    for (cx, cy) in ((2, 2), (10, 10)):
        for (dx, dy) in chev:
            x, y = (cx + dx + shift) % 16, cy + dy
            put(a, [(x, y)], CHEV)
            put(a, [((x - 1) % 16, y)], sh(CHEV, 0.62))
    im = img(a)
    rot = {"right": 0, "down": -90, "left": 180, "up": 90}[direction]
    return im.rotate(rot) if rot else im


def race_fork(frame: int = 0) -> Image.Image:
    """A junction pool: a slow swirl round a calm eye."""
    a = flat(sh(SEA, 1.02, 2))
    for k in range(28):
        th = k / 28 * 2 * math.pi + frame * 2 * math.pi / 3
        rr = 2.5 + k * 0.17
        x, y = int(round(7.5 + rr * math.cos(th))), int(round(7.5 + rr * math.sin(th)))
        px(a, x, y, CHEV if k % 4 else FOAM)
    put(a, [(7, 7), (8, 8)], SEA_LT)
    return img(a)


# ---- decor overlays ------------------------------------------------------------------
def deco_barnacle(v: int) -> Image.Image:
    a = clear()
    pts = [(4, 6), (7, 5), (6, 8), (10, 9), (9, 12)] if v == 0 else [(9, 4), (5, 9), (8, 10), (11, 11)]
    for (x, y) in pts:
        rect(a, x - 1, y - 1, x + 1, y, BARN)
        px(a, x, y - 1, (230, 222, 204))
        px(a, x, y, BARN_DK)
        px(a, x - 1, y + 1, sh(WET, 0.5), 160)
        px(a, x + 1, y + 1, sh(WET, 0.5), 160)
    return to_im(a)


def deco_shell() -> Image.Image:
    a = clear()
    ellipse(a, 7.5, 9, 3.2, 2.4, (220, 186, 170))
    for x in (5, 7, 9):
        px(a, x, 8, (180, 132, 120))
        px(a, x, 10, (180, 132, 120))
    px(a, 7, 11, (150, 104, 96))
    rect(a, 4, 12, 11, 12, sh(WET, 0.55), 140)
    return to_im(a)


def deco_wrack() -> Image.Image:
    """Stranded sea-wrack: a coil of dark kelp left by the tide."""
    a = clear()
    for k in range(16):
        x = 3 + k * 10 // 16
        y = 9 + int(2.2 * math.sin(k * 0.9))
        px(a, x, y, KELP)
        px(a, x, y + 1, KELP_DK)
    for (x, y) in ((6, 7), (9, 12), (12, 8)):
        px(a, x, y, KELP_LT)
    return to_im(a)


def deco_glass(v: int) -> Image.Image:
    """Drowned lamp-glass: shards of the old lens, glinting."""
    a = clear()
    shards = [[(3, 9), (4, 8), (5, 9), (4, 10)], [(9, 5), (10, 4), (11, 5), (11, 6), (10, 6)],
              [(10, 11), (11, 10), (12, 11)]] if v == 0 else \
        [[(5, 5), (6, 4), (7, 5), (6, 6)], [(8, 11), (9, 10), (10, 10), (10, 11), (9, 12)]]
    for s in shards:
        for i, (x, y) in enumerate(s):
            px(a, x, y, GLASS_LT if i == 1 else GLASS)
        x, y = s[0]
        px(a, x, y + 2, sh(WET, 0.5), 120)
    return to_im(a)


# ---- objects ----------------------------------------------------------------------
def obj_bell(rung: bool) -> Image.Image:
    """A tide-bell (16x32): a barnacled post with a crook, a bronze bell hung from
    it. Rung: the bell swung out, with ring-arcs."""
    a = clear(16, 32)
    rect(a, 3, 6, 5, 30, WOOD)
    rect(a, 3, 6, 3, 30, WOOD_LT)
    rect(a, 5, 6, 5, 30, WOOD_DK)
    rect(a, 3, 5, 12, 6, WOOD)                       # the crook arm
    rect(a, 3, 5, 12, 5, WOOD_LT)
    for (x, y) in ((4, 22), (3, 25), (5, 27), (4, 28)):
        px(a, x, y, BARN)                            # barnacles at the waterline
    rect(a, 2, 29, 6, 31, sh(WET, 0.7))
    off = 1 if rung else 0
    cx = 9 + off
    px(a, 10, 7, IRON_DK)
    px(a, 10 + off // 2, 8, IRON_DK)
    for y in range(9, 18):                           # the bell body flares
        half = 2 + (y - 9) * 3 // 9
        for x in range(cx - half, cx + half + 1):
            c = BRASS_LT if x == cx - half + 1 else (BRASS_DK if x >= cx + half - 1 else BRASS)
            px(a, x, y, c)
    rect(a, cx - 5, 17, cx + 5, 17, BRASS_DK)
    px(a, cx, 18, IRON_DK)                           # the clapper
    px(a, cx, 19, IRON)
    for (x, y) in ((cx - 1, 12), (cx + 1, 14)):
        px(a, x, y, sh(KELP, 0.9))                   # a little verdigris
    outline(a)
    if rung:                                         # the note, rolling out
        for (x, y) in ((14, 9), (15, 10), (15, 11), (15, 12), (14, 13),
                       (13, 11), (12, 20), (13, 21), (14, 21), (15, 20), (6, 21), (7, 22)):
            px(a, x, y, CHEV)
    return to_im(a)


def obj_post(red: bool) -> Image.Image:
    """A race-post (16x16): a striped marker pole with a pennant. White: the race
    runs straight on. Red: the race turns."""
    a = clear()
    rect(a, 7, 2, 8, 14, IRON_LT)
    rect(a, 8, 2, 8, 14, IRON)
    for y in (5, 9):
        rect(a, 7, y, 8, y + 1, RED if red else (232, 232, 224))
    col = RED if red else (240, 240, 232)
    dk = sh(col, 0.7)
    for i in range(5):                               # the pennant
        rect(a, 9, 2 + i // 2, 9 + 4 - i, 2 + i // 2, col)
    px(a, 9, 4, dk)
    px(a, 10, 4, dk)
    rect(a, 5, 14, 10, 15, BARN_DK)
    px(a, 6, 14, BARN)
    px(a, 9, 14, BARN)
    outline(a)
    return to_im(a)


def obj_logbook() -> Image.Image:
    """A barnacled sea-chest with the keeper's logbook lying open on its lid."""
    a = clear()
    rect(a, 2, 7, 13, 14, WOOD)
    rect(a, 2, 7, 13, 7, WOOD_LT)
    rect(a, 2, 14, 13, 14, WOOD_DK)
    rect(a, 2, 10, 13, 10, IRON)
    px(a, 7, 11, BRASS)
    px(a, 8, 11, BRASS_DK)
    for (x, y) in ((3, 13), (12, 12), (4, 12)):
        px(a, x, y, BARN)
    rect(a, 3, 3, 7, 6, (226, 214, 184))             # the open book
    rect(a, 8, 3, 12, 6, (214, 200, 168))
    rect(a, 7, 3, 8, 6, (150, 120, 90))
    for y in (4, 5):
        rect(a, 4, y, 6, y, (122, 112, 104))
        rect(a, 9, y, 11, y, (122, 112, 104))
    outline(a)
    return to_im(a)


def obj_fogglass(empty: bool) -> Image.Image:
    """The keeper's fog-glass on a stone stand (16x32): a brass-bound lens that
    holds a little light of its own. Empty: the cradle alone."""
    a = clear(16, 32)
    rect(a, 4, 18, 11, 29, STONE)
    rect(a, 4, 18, 4, 29, STONE_LT)
    rect(a, 11, 18, 11, 29, STONE_DK)
    rect(a, 2, 28, 13, 30, STONE_DK)
    rect(a, 3, 16, 12, 18, STONE_LT)
    for (x, y) in ((5, 26), (9, 23), (10, 27)):
        px(a, x, y, BARN)
    rect(a, 4, 14, 11, 15, BRASS_DK)                 # the cradle
    px(a, 4, 13, BRASS)
    px(a, 11, 13, BRASS)
    if not empty:
        ellipse(a, 7.5, 9, 4.6, 4.6, BRASS)
        ellipse(a, 7.5, 9, 3.6, 3.6, GLASS)
        ellipse(a, 6.8, 8.2, 1.6, 1.6, GLASS_LT)
        px(a, 9, 11, (232, 248, 248))
    outline(a)
    if not empty:
        for (x, y) in ((1, 5), (14, 6), (2, 12), (13, 2)):
            px(a, x, y, GLASS_LT, 200)
    return to_im(a)


def obj_lamp(lit: bool) -> Image.Image:
    """THE FARLAMP (64x80): the drowned lamp-house lantern, fallen to the floor
    of its own tower — an iron gallery-ring on a stone plinth, the great
    faceted lens housing above, its cupola crowned with a vane. Dark: green
    sea-glass, weed and barnacles, a cold heart. Lit: the lens full of warm
    light, the facets blazing, rays out through the panes."""
    W, H = 64, 80
    a = clear(W, H)
    # plinth
    rect(a, 8, 64, 55, 77, STONE)
    rect(a, 8, 64, 55, 65, STONE_LT)
    rect(a, 8, 76, 55, 77, STONE_DK)
    for x in range(8, 56, 8):
        rect(a, x, 66, x, 75, STONE_DK)
    for (x, y) in ((11, 72), (20, 74), (43, 70), (50, 75), (30, 76)):
        px(a, x, y, BARN)
        px(a, x + 1, y, BARN_DK)
    # gallery ring (iron rail)
    rect(a, 4, 58, 59, 63, IRON)
    rect(a, 4, 58, 59, 58, IRON_LT)
    rect(a, 4, 63, 59, 63, IRON_DK)
    for x in range(6, 59, 5):
        rect(a, x, 52, x, 58, IRON_DK)
    rect(a, 4, 51, 59, 52, IRON)
    # lantern housing: an octagon of glass panes between iron mullions
    glass = GLASS if not lit else (255, 214, 120)
    glass_lt = GLASS_LT if not lit else GLOW_HOT
    for y in range(18, 51):
        inset = max(0, 6 - (y - 18)) if y < 24 else (max(0, (y - 45)) if y > 45 else 0)
        x0, x1 = 12 + inset, 51 - inset
        for x in range(x0, x1 + 1):
            c = glass
            if (x - 12) % 10 in (0, 1):
                c = IRON_DK if not lit else BRASS_DK
            elif lit and abs(x - 31.5) < 8 and abs(y - 34) < 9:
                c = GLOW_HOT
            elif lit and abs(x - 31.5) < 14:
                c = GLOW
            elif not lit and (x + y) % 9 == 0:
                c = sh(GLASS, 0.75)
            px(a, x, y, c)
    for y in (24, 45):
        rect(a, 12, y, 51, y, IRON if not lit else BRASS)
    # the lens itself: concentric facets
    for k, rr in enumerate((11, 8, 5)):
        for t in range(48):
            th = t / 48 * 2 * math.pi
            x, y = 31.5 + rr * math.cos(th), 34 + rr * 1.1 * math.sin(th)
            px(a, int(x), int(y), (glass_lt if k % 2 == 0 else (BRASS if lit else sh(GLASS, 0.6))))
    if lit:
        ellipse(a, 31.5, 34, 3.6, 3.8, (255, 255, 240))
    else:
        ellipse(a, 31.5, 34, 3.2, 3.4, sh(GLASS, 0.5))
    # cupola + vane
    for y in range(8, 18):
        half = 6 + (y - 8) * 2
        rect(a, 32 - half, y, 31 + half, y, IRON if not lit else BRASS_DK)
        px(a, 32 - half, y, IRON_LT if not lit else BRASS)
    rect(a, 30, 2, 33, 8, IRON_DK)
    rect(a, 27, 3, 36, 4, IRON_LT)
    px(a, 37, 3, IRON_LT)
    # the sea's claim: weed + barnacles (dark) — kept, lighter, when lit
    weed = [(13, 46, 7), (19, 48, 5), (47, 47, 6), (52, 44, 8), (40, 49, 4)]
    for (x, y, n) in weed:
        for k in range(n):
            px(a, x + (k % 2), y + k, KELP if not lit else KELP_DK)
            px(a, x + 1 - (k % 2), y + k, KELP_DK)
    for (x, y) in ((14, 20), (49, 22), (16, 60), (45, 61), (24, 60), (36, 62), (55, 59)):
        px(a, x, y, BARN)
        px(a, x, y + 1, BARN_DK)
    outline(a)
    if lit:
        for (dx, dy) in ((-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)):
            for k in range(4):
                x = int(31.5 + dx * (24 + k * 2))
                y = int(34 + dy * (6 + k * 3))
                px(a, x, y, GLOW, 220 - k * 40)
    return to_im(a)


def obj_seadoor(open_: bool) -> Image.Image:
    """A barnacled iron sea-door (32x32) set in a stone arch. Open: swung in on
    a lit room."""
    a = clear(32, 32)
    for y in range(32):
        for x in range(32):
            d = math.hypot(x - 15.5, max(0, 16 - y))
            if (x < 4 or x > 27 or (y < 16 and d > 12)) and d <= 16:
                px(a, x, y, STONE if (x + y) % 7 else STONE_DK)
    for x in range(32):
        for y in range(32):
            d = math.hypot(x - 15.5, max(0, 16 - y))
            if 3 <= x <= 28 and (y >= 16 or d <= 12):
                if open_:
                    c = (64, 54, 46) if y > 20 else (92, 78, 60)
                    if 6 <= x <= 25 and y >= 10:
                        c = (150, 120, 70) if (x + y) % 5 else (180, 146, 86)
                    px(a, x, y, c)
                elif 4 <= x <= 27:
                    c = IRON if (x - 4) % 6 else IRON_DK
                    if y in (14, 24):
                        c = IRON_LT
                    px(a, x, y, c)
    if open_:
        rect(a, 4, 12, 6, 31, IRON_DK)               # the swung leaf, edge-on
    else:
        for (x, y) in ((7, 28), (9, 27), (22, 29), (24, 26), (12, 30), (19, 30), (26, 20)):
            px(a, x, y, BARN)
            px(a, x + 1, y, BARN_DK)
        ellipse(a, 20.5, 20.5, 1.6, 1.6, BRASS)      # the wheel-boss
        rect(a, 17, 20, 24, 20, BRASS_DK)
        rect(a, 20, 17, 20, 24, BRASS_DK)
    outline(a)
    return to_im(a)


def obj_camp() -> Image.Image:
    """The keeper's dry-ledge camp (32x32): an oilskin bedroll, a tin kettle on
    a little driftwood fire in a ring of stones, a crate."""
    a = clear(32, 32)
    rect(a, 2, 4, 14, 10, WOOD)                      # crate
    rect(a, 2, 4, 14, 4, WOOD_LT)
    rect(a, 2, 7, 14, 7, WOOD_DK)
    rect(a, 8, 4, 8, 10, WOOD_DK)
    rect(a, 4, 16, 27, 24, (128, 96, 64))            # bedroll (oilskin)
    rect(a, 4, 16, 27, 16, (168, 132, 88))
    rect(a, 4, 16, 9, 24, (172, 66, 56))             # a red blanket fold
    rect(a, 22, 17, 26, 22, (214, 204, 184))          # the pillow
    for t in range(12):                              # ring of stones round the fire
        th = t / 12 * 2 * math.pi
        x, y = 23 + 5 * math.cos(th), 7 + 3.2 * math.sin(th)
        px(a, int(x), int(y), STONE_LT if t % 2 else STONE)
    ellipse(a, 23, 7, 2.4, 1.6, (232, 120, 52))
    px(a, 23, 6, GLOW)
    px(a, 22, 5, GLOW_HOT)
    rect(a, 21, 1, 25, 4, IRON_LT)                   # the kettle
    rect(a, 21, 4, 25, 4, IRON_DK)
    outline(a)
    return to_im(a)


def obj_kelp() -> Image.Image:
    """A tall kelp frond (16x32) rising off the wet floor, bladders and all."""
    a = clear(16, 32)
    for strand, (x0, ph) in enumerate(((6, 0.0), (9, 1.4), (4, 2.6))):
        top = 3 + strand * 4
        for y in range(top, 31):
            x = x0 + int(round(1.6 * math.sin(y * 0.35 + ph)))
            px(a, x, y, KELP if strand != 1 else KELP_LT)
            px(a, x + 1, y, KELP_DK)
            if (y + strand) % 6 == 0:
                px(a, x - 1, y, KELP_LT)
                px(a, x + 2, y + 1, (150, 140, 70))    # a bladder
    rect(a, 3, 30, 12, 31, sh(WET, 0.6))
    outline(a, (14, 26, 22))
    return to_im(a)


def obj_pillar() -> Image.Image:
    """A fallen length of the lighthouse's masonry (32x48): dressed stone courses,
    weed down its side, barnacles at its foot."""
    a = clear(32, 48)
    for y in range(6, 46):
        for x in range(5, 27):
            c = STONE
            if (y - 6) % 8 == 0:
                c = STONE_DK
            elif ((x - 5 + (8 if ((y - 6) // 8) % 2 else 0)) % 16) == 0:
                c = STONE_DK
            elif x < 8:
                c = STONE_LT
            elif x > 23:
                c = sh(STONE, 0.78)
            px(a, x, y, c)
    for x in range(5, 27):                           # the broken top
        for y in range(0, 6 + (x * 7) % 3):
            if y >= 3 + ((x * 5) % 4):
                px(a, x, y, STONE_LT)
    for k in range(18):
        px(a, 22 + (k % 2), 14 + k, KELP)
        px(a, 23 - (k % 2), 14 + k, KELP_DK)
    for (x, y) in ((7, 42), (11, 44), (18, 43), (24, 41), (14, 40)):
        px(a, x, y, BARN)
        px(a, x + 1, y, BARN_DK)
    outline(a)
    return to_im(a)


def obj_glassheap() -> Image.Image:
    """A heap of drowned lamp-glass panes (32x16), green with the sea."""
    a = clear(32, 16)
    for (x0, y0, x1, y1) in ((3, 9, 12, 14), (9, 6, 18, 13), (16, 8, 27, 14), (12, 3, 19, 9)):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px(a, x, y, GLASS if (x + y) % 5 else GLASS_LT)
        rect(a, x0, y0, x1, y0, GLASS_LT)
        rect(a, x0, y1, x1, y1, sh(GLASS, 0.6))
    for (x, y) in ((6, 12), (21, 11), (14, 7)):
        px(a, x, y, KELP)
    outline(a)
    return to_im(a)



# ---- PASS 2: things breaking the white water --------------------------------------
def foam_base(a, x0, x1, y):
    """A ring of broken white water where a thing stands in the surge."""
    for x in range(x0, x1 + 1):
        if (x * 3 + y) % 4:
            px(a, x, y, FOAM)
        px(a, x, y + 1, SURGE_LT if x % 3 else FOAM)


def obj_wreck() -> Image.Image:
    """A wreck's bones (32x32): the curved ribs of a little lamp-boat and a
    stove-in strake of planking, standing out of the surge."""
    a = clear(32, 32)
    for i, x0 in enumerate((5, 11, 17, 23)):          # ribs, leaning
        h = 25 - abs(i - 1.5) * 4
        for k in range(int(h)):
            y = 27 - k
            x = x0 + int(round((k / h) ** 2 * (5 if i < 2 else -5)))
            px(a, x, y, WOOD)
            px(a, x + 1, y, WOOD_DK)
            if k == int(h) - 1:
                px(a, x, y - 1, WOOD_LT)
    for x in range(3, 29):                            # the strake, broken
        y = 22 + (x - 3) // 9
        if 13 <= x <= 15:
            continue
        rect(a, x, y, x, y + 2, WOOD_LT if x % 5 else WOOD_DK)
        px(a, x, y + 3, WOOD_DK)
    for (x, y) in ((6, 24), (19, 25), (24, 25), (9, 26), (27, 23)):
        px(a, x, y, BARN)
    for k in range(6):
        px(a, 20 + (k % 2), 14 + k, KELP)
    outline(a)
    foam_base(a, 1, 30, 29)
    return to_im(a)


def obj_stack() -> Image.Image:
    """A sea-stack (16x32): a knuckle of black rock with a barnacled waist and a
    white collar where the churn hits it."""
    a = clear(16, 32)
    for y in range(4, 29):
        half = 3 + (y - 4) * 3 // 25
        if y < 8:
            half = 2 + (y - 4) // 2
        for x in range(8 - half, 8 + half):
            c = sh(CAVE, 0.95)
            if x <= 8 - half + 1:
                c = sh(CAVE, 1.35, 10)
            elif x >= 8 + half - 2:
                c = sh(CAVE, 0.6)
            if (x * 5 + y * 3) % 11 == 0:
                c = sh(CAVE, 0.5)
            px(a, x, y, c)
    for (x, y) in ((6, 20), (9, 22), (7, 24), (10, 25), (5, 26), (8, 26)):
        px(a, x, y, BARN)
        px(a, x, y + 1, BARN_DK)
    for (x, y) in ((7, 9), (9, 13)):
        px(a, x, y, sh(KELP, 0.8))
    outline(a)
    foam_base(a, 2, 13, 29)
    return to_im(a)


def obj_kelpcrown() -> Image.Image:
    """A kelp crown (32x16): a raft of floating kelp riding the churn, bladders
    glinting."""
    a = clear(32, 16)
    for k in range(5):
        cy = 6 + (k % 3) * 2
        for t in range(26):
            x = 3 + t
            y = cy + int(round(1.5 * math.sin(t * 0.5 + k)))
            if 2 < x < 29:
                px(a, x, y, KELP if k % 2 else KELP_LT)
                px(a, x, y + 1, KELP_DK)
    for (x, y) in ((8, 5), (14, 9), (21, 6), (25, 10), (11, 11)):
        px(a, x, y, (176, 164, 84))
        px(a, x + 1, y, (120, 110, 56))
    outline(a, (12, 28, 26))
    foam_base(a, 2, 29, 13)
    return to_im(a)


def obj_mast() -> Image.Image:
    """A drowned mast (16x48): a broken barnacled spar standing out of the sea,
    its yard askew, a rag of pennant still on it."""
    a = clear(16, 48)
    rect(a, 7, 6, 8, 44, WOOD)
    rect(a, 7, 6, 7, 44, WOOD_LT)
    rect(a, 8, 6, 8, 44, WOOD_DK)
    for x in range(2, 15):                             # the yard, askew
        y = 12 + (x - 2) // 5
        px(a, x, y, WOOD_DK)
        px(a, x, y - 1, WOOD)
    for k in range(10):                                # a hanging stay
        px(a, 3 + k // 4, 13 + k, (150, 132, 100))
    for i in range(4):                                 # the rag of pennant
        rect(a, 9, 4 + i // 2, 9 + 4 - i, 4 + i // 2, RED)
    for y in (30, 33, 36, 38, 40, 42):
        px(a, 7 + (y % 2), y, BARN)
    for k in range(8):
        px(a, 8 + (k % 2), 34 + k, KELP)
    rect(a, 6, 2, 9, 3, WOOD_DK)                        # the snapped top
    px(a, 7, 1, WOOD)
    outline(a)
    foam_base(a, 3, 12, 45)
    return to_im(a)


def obj_tidelamp(lit: bool) -> Image.Image:
    """A tide-lamp (16x32): the keepers' small iron lamps on barnacled posts
    that marked the races. Dark: cold sea-glass. Lit (after the isles' dawn):
    a warm flame and a halo."""
    a = clear(16, 32)
    rect(a, 7, 12, 8, 29, IRON)
    rect(a, 7, 12, 7, 29, IRON_LT)
    for (x, y) in ((7, 24), (8, 26), (7, 27)):
        px(a, x, y, BARN)
    rect(a, 4, 4, 11, 11, IRON_DK)                     # the lantern cage
    rect(a, 5, 5, 10, 10, (255, 214, 120) if lit else sh(GLASS, 0.7))
    if lit:
        rect(a, 6, 6, 9, 9, GLOW)
        rect(a, 7, 7, 8, 8, GLOW_HOT)
    else:
        px(a, 6, 6, GLASS_LT)
    rect(a, 5, 2, 10, 3, IRON)                         # the cap
    px(a, 7, 1, IRON_DK)
    px(a, 8, 1, IRON_DK)
    outline(a)
    if lit:
        for (x, y) in ((2, 7), (13, 7), (7, 0), (3, 3), (12, 3), (3, 12), (12, 12)):
            px(a, x, y, GLOW, 170)
    foam_base(a, 3, 12, 30)
    return to_im(a)


def obj_niche() -> Image.Image:
    """A keeper's dry niche (32x32): a bunk cut into the rock, a blanket, a
    hook with a little lamp, a water-cask."""
    a = clear(32, 32)
    rect(a, 2, 6, 29, 22, sh(CAVE, 0.55))              # the cut niche
    rect(a, 2, 6, 29, 7, sh(CAVE, 0.4))
    rect(a, 4, 14, 22, 20, WOOD)                        # the bunk
    rect(a, 4, 14, 22, 14, WOOD_LT)
    rect(a, 5, 12, 21, 16, (92, 120, 150))              # a blue blanket
    rect(a, 5, 12, 9, 15, (214, 204, 184))              # pillow
    rect(a, 4, 21, 22, 22, WOOD_DK)
    rect(a, 24, 9, 24, 13, IRON_DK)                     # lamp hook
    rect(a, 23, 13, 26, 16, IRON_DK)
    rect(a, 24, 14, 25, 15, GLOW)
    ellipse(a, 26.5, 24.5, 3.2, 4.2, WOOD)              # the cask
    rect(a, 23, 22, 29, 22, IRON)
    rect(a, 23, 26, 29, 26, IRON)
    outline(a)
    return to_im(a)


# ---- build ------------------------------------------------------------------------
NAMES = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
         "corner_sw", "edge_s", "corner_se", "inner_nw", "inner_ne", "inner_sw",
         "inner_se", "strip_h", "strip_v", "end_n", "end_s", "end_w", "end_e", "single"]


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    OBJ_DIR.mkdir(parents=True, exist_ok=True)
    for old in TILES_DIR.glob("*.png"):
        old.unlink()
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im, role: str, **extra):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": role, **extra})

    WATER = {"collides": True, "requires_ability": "tidecall", "encounter_terrain": "water"}
    for r in NAMES:
        add(f"tidepool_{r}", pool_tile(r), "water", terrain="tidepool", autotile=r, **WATER)
    for r in NAMES:
        add(f"surge_{r}", surge_tile(r), "wall", terrain="surge", autotile=r, collides=True)
    # animation frames (fills + the edge collars breathe)
    for fam, fn in (("tidepool", pool_tile), ("surge", surge_tile)):
        for r in NAMES:
            base = index[f"{fam}_{r}"]
            meta = {k: v for k, v in tiles[base].items() if k not in ("file", "autotile", "terrain")}
            add(f"{fam}_{r}_a2", fn(r, 1), **meta)
            add(f"{fam}_{r}_a3", fn(r, 2), **meta)
            tiles[base]["animation"] = {"frames": [base, index[f"{fam}_{r}_a2"], index[f"{fam}_{r}_a3"]],
                                        "duration_ms": 1100 if fam == "tidepool" else 650}
    # races: swum like the shallows (Tidecall; the `water` tag is what puts the
    # player in the swim sheet). Builders keep every water ZONE off the lanes, so
    # the races are travel and the pools are the beds.
    RACE = {"collides": True, "requires_ability": "tidecall", "encounter_terrain": "water",
            "terrain": "surge"}   # one sea with the churn (no autotile role: never auto-picked)
    for d in ("up", "down", "left", "right"):
        add(f"race_{d}", race_tile(d, 0), "water", **RACE)
        add(f"race_{d}_a2", race_tile(d, 1), "water", **RACE)
        add(f"race_{d}_a3", race_tile(d, 2), "water", **RACE)
        b = index[f"race_{d}"]
        tiles[b]["animation"] = {"frames": [b, b + 1, b + 2], "duration_ms": 220}
    add("race_fork", race_fork(0), "water", **RACE)
    add("race_fork_a2", race_fork(1), "water", **RACE)
    add("race_fork_a3", race_fork(2), "water", **RACE)
    b = index["race_fork"]
    tiles[b]["animation"] = {"frames": [b, b + 1, b + 2], "duration_ms": 400}
    for v in range(3):
        add(f"wetstone_{v}", wetstone(v), "ground")
    add("barnacle_a", deco_barnacle(0), "decor")
    add("barnacle_b", deco_barnacle(1), "decor")
    add("shell_a", deco_shell(), "decor")
    add("wrack_a", deco_wrack(), "decor")
    add("glass_a", deco_glass(0), "decor")
    add("glass_b", deco_glass(1), "decor")
    # fill VARIANTS (APPENDED — never insert above: gids are baked into maps).
    # The autotiler scatters among same-role tiles, so a wide churn never stamps.
    for v in (1, 2):
        add(f"surge_fill_v{v}", img(surge_fill(0, v)), "wall", terrain="surge",
            autotile="fill", collides=True)
        add(f"surge_fill_v{v}_a2", img(surge_fill(1, v)), "wall", collides=True)
        add(f"surge_fill_v{v}_a3", img(surge_fill(2, v)), "wall", collides=True)
        b = index[f"surge_fill_v{v}"]
        tiles[b]["animation"] = {"frames": [b, b + 1, b + 2], "duration_ms": 650 + 60 * v}
    for r in ("edge_n", "edge_s", "edge_w", "edge_e"):
        add(f"surge_{r}_v1", surge_tile(r, 0, 1), "wall", terrain="surge", autotile=r,
            collides=True)
        add(f"surge_{r}_v1_a2", surge_tile(r, 1, 1), "wall", collides=True)
        add(f"surge_{r}_v1_a3", surge_tile(r, 2, 1), "wall", collides=True)
        b = index[f"surge_{r}_v1"]
        tiles[b]["animation"] = {"frames": [b, b + 1, b + 2], "duration_ms": 700}
    for v in (1,):
        add(f"tidepool_fill_v{v}", img(pool_fill(0, v)), "water", terrain="tidepool",
            autotile="fill", **WATER)
        add(f"tidepool_fill_v{v}_a2", img(pool_fill(1, v)), "water", **WATER)
        add(f"tidepool_fill_v{v}_a3", img(pool_fill(2, v)), "water", **WATER)
        b = index[f"tidepool_fill_v{v}"]
        tiles[b]["animation"] = {"frames": [b, b + 1, b + 2], "duration_ms": 1200}

    objs = {
        "bell": obj_bell(False), "bell_rung": obj_bell(True),
        "post_white": obj_post(False), "post_red": obj_post(True),
        "logbook": obj_logbook(),
        "fogglass": obj_fogglass(False), "fogglass_empty": obj_fogglass(True),
        "lamp_dark": obj_lamp(False), "lamp_lit": obj_lamp(True),
        "camp": obj_camp(), "kelp": obj_kelp(), "pillar": obj_pillar(),
        "glassheap": obj_glassheap(),
        # pass 2: things in the surge, the dawn's tide-lamps, the IV rest niche
        "wreck": obj_wreck(), "stack": obj_stack(), "kelpcrown": obj_kelpcrown(),
        "mast": obj_mast(), "tidelamp": obj_tidelamp(False), "tidelamp_lit": obj_tidelamp(True),
        "niche": obj_niche(),
    }
    for stem, im in objs.items():
        im.save(OBJ_DIR / f"{stem}.png")
    print(f"objects -> {OBJ_DIR} ({len(objs)}; run pack_objects.py)")

    manifest = {"name": "undertide_set", "columns": 10, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (BASE / "undertide_set.index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"undertide_set: {len(tiles)} tiles -> {TILES_DIR}")
    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
