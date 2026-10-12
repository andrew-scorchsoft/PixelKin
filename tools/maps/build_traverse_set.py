#!/usr/bin/env python3
"""
build_traverse_set — the TRAVERSAL KIT accent tileset (`traverse_set`, 2026-10).

The art half of the traversal kit (docs/world/walkthrough/09-the-wild-ways.md §1):
the BEHAVIOUR lives in map data (`flows`/`spans`/`jumps`), never in tile meta, so
these tiles carry no collision of their own except the multi-row cliff faces.
Every piece is drawn in code in gbaforge's GBA register — flat dusk anchors,
1px ink, deliberate repeated motifs — so it sits on the shared set without
ringing.

Families (names in assets/tilesets/traverse/traverse_set.index.json):
  chute_v_0/1, chute_h_0/1   the Wick-Run's packed wax-road: deep cart ruts along
                             the fall line (a slope flow rides on these)
  chev_down/left/right/up    painted tallow chevrons (overlay) — "this way, fast"
  berm_w/e/n/s               plank berm boards along a chute's side (overlay)
  ramp_down/left/right/up    a timber kicker (overlay; a `jumps[]` pad)
  deck_h, deck_h_w, deck_h_e  a trestle deck running E–W (+ end posts)
  deck_v, deck_v_n, deck_v_s  a trestle deck running N–S (+ end posts)
  under_shade                the shadow a deck throws on the road beneath (overlay)
  ladder, ladder_top         a timber ladder pinned to a cliff face (overlay;
                             a `spans[] kind:'ladder'`)
  plank_h, plank_v           rope-and-slat walks over a gap (overlay)
  rail_h, rail_v, rail_ne/nw/se/sw, rail_tee_n/s/e/w, rail_end_n/s/e/w
                             ore-cart rails on ballast (overlay; `kind:'rail'` flows)
  glare_0/1                  glare ice — polished, streaked (`kind:'ice'` flows)
  face_rock_0/1, face_rock_foot   a cliff FACE row for multi-row walls (collides)
  face_gold_0/1, face_gold_foot   ... warm sandstone (the Sunvault face)
  face_ice_0/1, face_ice_foot     ... blue glacier ice (the Rimeway)

Objects (flag-swappable, so they're objects not tiles), drawn here too:
  assets/tilesets/traverse/objects/lever_off.png, lever_on.png  (1x2)
  ore_cart.png (1x1), switch_a.png / switch_b.png (1x1 junction point-stands)
Then: pack_objects.py (manifest keys traverse_<stem>).

Run:  python3 tools/maps/build_traverse_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from gbaforge import sh, flat, put, img, PATH, CLIFF, GOLD, ICE, CAVE

REPO = Path(__file__).resolve().parents[2]
BASE = REPO / "assets" / "tilesets" / "traverse"
TILES_DIR = BASE / "set_tiles"
OBJ_DIR = BASE / "objects"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

WAX = (122, 96, 66)          # the wax-road's packed, tallow-darkened earth
TIMBER = (138, 102, 64)      # trestle / berm / ladder wood
TIMBER_LT = sh(TIMBER, 1.30, 10)
TIMBER_DK = sh(TIMBER, 0.62)
INK = (24, 20, 30)
TALLOW = (226, 206, 150)     # chevron paint: rendered tallow, the run's marker
IRON = (92, 96, 110)
IRON_LT = (150, 156, 170)
ROPE = (176, 150, 104)
SANDSTONE = sh(GOLD, 1.18, 18)


def clear() -> np.ndarray:
    return np.zeros((16, 16, 4), dtype=np.int16)


def px(a, x, y, rgb, alpha=255):
    if 0 <= x < 16 and 0 <= y < 16:
        a[y, x, :3] = rgb
        a[y, x, 3] = alpha


def rot(im: Image.Image, k: int) -> Image.Image:
    """Rotate by k quarter-turns clockwise (k in 0..3)."""
    return im.rotate(-90 * k, expand=False)


# ---- the wax-road chute ---------------------------------------------------------
def chute_v(v: int = 0) -> Image.Image:
    """The wax road: packed, tallow-darkened earth, scored by short downhill
    skid-streaks (the motion motif) and a little grit — never full-height ruts,
    which tile into plank stripes."""
    a = flat(WAX)
    streak = sh(WAX, 0.70)
    lit = sh(WAX, 1.18, 6)
    layout = ([(3, 1), (11, 4), (6, 9), (13, 11), (2, 13)],
              [(9, 0), (4, 5), (12, 8), (7, 12), (1, 9)])[v % 2]
    for (x, y) in layout:
        for k in range(4):
            put(a, [(x, y + k)], streak)
        put(a, [(x + 1, y)], lit)                    # the streak's lit head
    for (x, y) in ([(8, 3), (14, 14), (1, 6)], [(14, 3), (3, 15), (10, 6)])[v % 2]:
        put(a, [(x, y)], sh(WAX, 0.82))
        put(a, [(x, y - 1)], sh(WAX, 1.16, 4))
    return img(a)


def chute_h(v: int = 0) -> Image.Image:
    return rot(chute_v(v), 1)


def chevron(k: int) -> Image.Image:
    """A painted tallow chevron pointing down (k quarter-turns for the others)."""
    a = clear()
    for i in range(5):
        px(a, 3 + i, 5 + i, TALLOW, 220)
        px(a, 12 - i, 5 + i, TALLOW, 220)
        px(a, 3 + i, 6 + i, sh(TALLOW, 0.8), 160)
        px(a, 12 - i, 6 + i, sh(TALLOW, 0.8), 160)
    return rot(img(a), k)


def berm(side: str) -> Image.Image:
    """Plank berm boards along a chute's west side (rotated for the others)."""
    a = clear()
    for y in range(16):
        for x in range(0, 4):
            c = TIMBER_LT if x == 3 else (TIMBER if x > 0 else TIMBER_DK)
            if y % 8 == 7:
                c = TIMBER_DK                        # board joint
            px(a, x, y, c)
        px(a, 4, y, INK, 120)                        # shadow the board throws
    for y in (2, 10):
        px(a, 1, y, IRON_LT)                         # nail heads
    k = {"w": 0, "n": 1, "e": 2, "s": 3}[side]
    return rot(img(a), k)


def ramp(k: int) -> Image.Image:
    """A timber kicker rising toward the bottom edge (the leap's direction = down);
    rotated k quarter-turns for the others. Lighter planks toward the lip."""
    a = clear()
    for y in range(3, 15):
        t = (y - 3) / 11
        c = sh(TIMBER, 0.75 + 0.6 * t, int(10 * t))
        for x in range(2, 14):
            px(a, x, y, c)
        if y % 3 == 0:
            for x in range(2, 14):
                px(a, x, y, sh(c, 0.75))             # plank seams
    for y in range(3, 15):
        px(a, 1, y, TIMBER_DK)
        px(a, 14, y, TIMBER_DK)
    for x in range(2, 14):
        px(a, x, 14, TALLOW)                         # the painted lip
        px(a, x, 15, INK, 140)
    return rot(img(a), k)


# ---- trestle decks --------------------------------------------------------------
def deck_v(end: str | None = None) -> Image.Image:
    """A N–S trestle deck: cross-planks + side rails; opaque (it hides the road
    beneath when drawn in the `above` layer)."""
    a = flat(TIMBER)
    for y in range(16):
        if y % 4 == 3:
            a[y, 2:14, :3] = TIMBER_DK                # plank gaps
        elif y % 4 == 0:
            a[y, 2:14, :3] = TIMBER_LT
    for y in range(16):
        a[y, 0:2, :3] = sh(TIMBER, 0.48)             # rails
        a[y, 14:16, :3] = sh(TIMBER, 0.48)
        a[y, 1, :3] = TIMBER_LT
        a[y, 14, :3] = TIMBER_LT
    if end in ("n", "s"):
        y = 0 if end == "n" else 15
        a[y, :, :3] = INK
        for x in (0, 1, 14, 15):
            yy = range(0, 4) if end == "n" else range(12, 16)
            for y2 in yy:
                a[y2, x, :3] = sh(TIMBER, 0.38)      # end posts
    return img(a)


def deck_h(end: str | None = None) -> Image.Image:
    im = rot(deck_v({"w": "n", "e": "s"}.get(end) if end else None), 1)
    if end == "w":
        im = rot(deck_v("s"), 1)
    elif end == "e":
        im = rot(deck_v("n"), 1)
    return im


def under_shade() -> Image.Image:
    a = clear()
    a[:, :, :3] = (10, 8, 18)
    a[:, :, 3] = 90
    return img(a)


# ---- ladders and planks ------------------------------------------------------------
def ladder(top: bool = False) -> Image.Image:
    a = clear()
    for y in range(16):
        px(a, 4, y, TIMBER)
        px(a, 11, y, TIMBER)
        px(a, 3, y, TIMBER_DK, 200)
        px(a, 12, y, INK, 120)
    for y in (1, 5, 9, 13):
        for x in range(5, 11):
            px(a, x, y, TIMBER_LT)
            px(a, x, y + 1, TIMBER_DK)
    if top:
        for x in (4, 11):
            px(a, x, 0, IRON_LT)
            px(a, x - 1 if x == 4 else x + 1, 0, IRON)   # hooks over the lip
    return img(a)


def plank(axis: str) -> Image.Image:
    """Rope-and-slat walk running N–S ('v'); rotated for 'h'. Gaps show the drop."""
    a = clear()
    for y in range(16):
        px(a, 2, y, ROPE)
        px(a, 13, y, ROPE)
        px(a, 1, y, sh(ROPE, 0.6), 200)
    for y in range(0, 16, 4):
        for x in range(3, 13):
            px(a, x, y, TIMBER_LT if x % 5 else TIMBER)
            px(a, x, y + 1, TIMBER)
            px(a, x, y + 2, TIMBER_DK)
    im = img(a)
    return rot(im, 1) if axis == "h" else im


# ---- ore-cart rails ---------------------------------------------------------------
def _rails(a, segs):
    """segs: subset of 'n','s','e','w' — which edges the track reaches."""
    tie = sh(TIMBER, 0.70)
    c = 8
    # ties (sleepers)
    if "n" in segs or "s" in segs:
        ys = [y for y in range(1, 16, 4) if ("n" in segs or y >= c) and ("s" in segs or y <= c)]
        for y in ys:
            for x in range(3, 13):
                px(a, x, y, tie)
                px(a, x, y + 1, sh(tie, 0.7))
    if "e" in segs or "w" in segs:
        xs = [x for x in range(1, 16, 4) if ("w" in segs or x >= c) and ("e" in segs or x <= c)]
        for x in xs:
            for y in range(3, 13):
                px(a, x, y, tie)
                px(a, x + 1, y, sh(tie, 0.7))
    # rails (two lines per arm, iron with a lit top edge)
    for arm in segs:
        if arm in "ns":
            ys = range(0, 9) if arm == "n" else range(7, 16)
            for y in ys:
                for x, col in ((5, IRON_LT), (10, IRON_LT)):
                    px(a, x, y, col)
                    px(a, x + 1, y, IRON)
        else:
            xs = range(0, 9) if arm == "w" else range(7, 16)
            for x in xs:
                for y, col in ((5, IRON_LT), (10, IRON_LT)):
                    px(a, x, y, col)
                    px(a, x, y + 1, IRON)


def _curve(a, arms: str) -> None:
    """A quarter-turn between two arms (e.g. 'ne'): rails as arcs about the
    tile corner the two arms share, ties radial."""
    import math
    cx = 16 if "e" in arms else 0
    cy = 0 if "n" in arms else 16
    tie = sh(TIMBER, 0.70)
    # sleepers: short radial strokes across the track band
    for deg in (15, 45, 75):
        t = math.radians(deg)
        for r in range(4, 13):
            x = cx + (-1 if cx else 1) * r * math.cos(t)
            y = cy + (1 if cy == 0 else -1) * r * math.sin(t)
            px(a, int(round(x)), int(round(y)), tie)
    for r, col in ((5.5, IRON_LT), (10.5, IRON_LT)):
        for i in range(0, 91):
            t = math.radians(i)
            x = cx + (-1 if cx else 1) * r * math.cos(t)
            y = cy + (1 if cy == 0 else -1) * r * math.sin(t)
            px(a, int(round(x)), int(round(y)), col)
            px(a, int(round(x)) + (1 if cx == 0 else -1), int(round(y)), IRON)


def rail(segs: str) -> Image.Image:
    a = clear()
    if len(segs) == 2 and set(segs) not in ({"n", "s"}, {"e", "w"}):
        _curve(a, segs)
    elif len(segs) == 3:
        straight = "ns" if "n" in segs and "s" in segs else "ew"
        branch = (set(segs) - set(straight)).pop()
        _rails(a, straight)
        # the branch peels off the line's first-named side
        _curve(a, (straight[0] if straight == "ew" else straight[1]) + branch
               if straight == "ew" else branch + straight[0])
    else:
        _rails(a, segs)
    return img(a)


def rail_end(side: str) -> Image.Image:
    """A buffer stop: the line runs in from the opposite side and ends at `side`."""
    opp = {"n": "s", "s": "n", "e": "w", "w": "e"}[side]
    a = clear()
    _rails(a, opp + side)
    # the buffer beam across the track at the `side` end
    if side in "ns":
        y = 2 if side == "n" else 13
        for x in range(3, 13):
            px(a, x, y, TIMBER_DK)
            px(a, x, y + (1 if side == "n" else -1), (168, 64, 52))
    else:
        x = 2 if side == "w" else 13
        for y in range(3, 13):
            px(a, x, y, TIMBER_DK)
            px(a, x + (1 if side == "w" else -1), y, (168, 64, 52))
    return img(a)


# ---- glare ice --------------------------------------------------------------------
def glare(v: int = 0) -> Image.Image:
    base = sh(ICE, 1.08, 10)
    a = flat(base)
    streak = sh(ICE, 1.45, 30)
    deep = sh(ICE, 0.86)
    for i, (x, y) in enumerate(([(2, 3), (9, 8), (4, 13)], [(7, 2), (1, 9), (11, 12)])[v % 2]):
        for k in range(4):
            put(a, [(x + k, y - k // 2)], streak)        # a long diagonal glint
        put(a, [(x + 1, y + 1), (x + 2, y + 1)], deep)
    put(a, [(13, 4) if v == 0 else (14, 15)], (240, 248, 255))
    return img(a)


# ---- multi-row cliff faces --------------------------------------------------------
def face(anchor, v: int = 0, foot: bool = False) -> Image.Image:
    """A mid-face row of a tall wall: no lip (the lip is the family's edge_s), a
    vertical streak ladder, one bedding seam. `foot` ends in the contact shadow."""
    a = flat(sh(anchor, 0.72))
    streak = sh(anchor, 0.56)
    lit = sh(anchor, 0.92, 6)
    x1, x2 = (3 + 5 * v) % 14 + 1, (10 + 5 * v) % 14 + 1
    for y in range(0, 9):
        a[y, x1, :3] = streak
        a[y, x1 + 1, :3] = lit
    for y in range(7, 16):
        a[y, x2, :3] = streak
    a[(6 + 4 * v) % 14, :, :3] = sh(anchor, 0.60)       # bedding seam
    if foot:
        a[12:14, :, :3] = sh(anchor, 0.50)
        a[14:, :, :3] = sh(anchor, 0.32)                # the contact shadow
    return img(a)


# ---- objects ---------------------------------------------------------------------
def lever(on: bool) -> Image.Image:
    """1x2 (16x32): a mine lever on an iron base; the handle thrown left/right."""
    a = np.zeros((32, 16, 4), dtype=np.int16)

    def p(x, y, rgb, al=255):
        if 0 <= x < 16 and 0 <= y < 32:
            a[y, x, :3] = rgb
            a[y, x, 3] = al

    for y in range(22, 31):
        for x in range(3, 13):
            p(x, y, IRON if y > 22 else IRON_LT)
    for x in range(2, 14):
        p(x, 31, INK, 160)
    # the handle: a diagonal shaft from the base pivot (8,22)
    dx = 1 if on else -1
    for i in range(12):
        p(8 + dx * (i // 2), 21 - i, TIMBER_DK if i % 3 == 0 else TIMBER)
    hx, hy = 8 + dx * 6, 9
    for yy in range(hy - 2, hy + 1):
        for xx in range(hx - 1, hx + 2):
            p(xx, yy, (196, 60, 48) if on else (120, 120, 132))
    p(8, 22, IRON_LT)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def ore_cart() -> Image.Image:
    a = clear()
    for y in range(4, 12):
        for x in range(2, 14):
            px(a, x, y, IRON if y > 4 else IRON_LT)
    for x in range(3, 13):
        px(a, x, 5, (38, 34, 42))                        # cinder-coal heaped inside
        if x % 3 == 0:
            px(a, x, 4, (60, 52, 58))
    for y in range(6, 11):
        px(a, 2, y, sh(IRON, 0.7))
        px(a, 13, y, sh(IRON, 0.7))
    for cx in (4, 11):
        for y in range(11, 15):
            for x in range(cx - 1, cx + 2):
                px(a, x, y, (30, 28, 36))
        px(a, cx, 12, IRON_LT)
    return img(a)


def switch_stand(branch: bool) -> Image.Image:
    """A junction's point-stand: a little iron post with a painted disc —
    straight (white) or branch (red)."""
    a = clear()
    for y in range(6, 15):
        px(a, 7, y, IRON)
        px(a, 8, y, IRON_LT if y < 8 else IRON)
    disc = (196, 60, 48) if branch else (226, 222, 210)
    for y in range(1, 7):
        for x in range(5, 11):
            if (x - 7.5) ** 2 + (y - 3.5) ** 2 <= 7:
                px(a, x, y, disc)
    for x in range(5, 11):
        px(a, x, 15, INK, 120)
    return img(a)


# ---------------------------------------------------------------------------------
def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    OBJ_DIR.mkdir(parents=True, exist_ok=True)
    for old in TILES_DIR.glob("*.png"):
        old.unlink()
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im: Image.Image, role: str, **extra) -> None:
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        tiles.append({"file": fn, "role": role, **extra})

    for v in (0, 1):
        add(f"chute_v_{v}", chute_v(v), "path")
    for v in (0, 1):
        add(f"chute_h_{v}", chute_h(v), "path")
    for k, d in enumerate(("down", "left", "up", "right")):
        add(f"chev_{d}", chevron(k), "decor")
    for s in ("w", "n", "e", "s"):
        add(f"berm_{s}", berm(s), "decor")
    for k, d in enumerate(("down", "left", "up", "right")):
        add(f"ramp_{d}", ramp(k), "decor")
    add("deck_v", deck_v(), "decor")
    add("deck_v_n", deck_v("n"), "decor")
    add("deck_v_s", deck_v("s"), "decor")
    add("deck_h", deck_h(), "decor")
    add("deck_h_w", deck_h("w"), "decor")
    add("deck_h_e", deck_h("e"), "decor")
    add("under_shade", under_shade(), "decor")
    add("ladder", ladder(), "decor")
    add("ladder_top", ladder(top=True), "decor")
    add("plank_v", plank("v"), "decor")
    add("plank_h", plank("h"), "decor")
    for name, segs in (("rail_h", "ew"), ("rail_v", "ns"), ("rail_ne", "ne"), ("rail_nw", "nw"),
                       ("rail_se", "se"), ("rail_sw", "sw"), ("rail_tee_n", "ewn"),
                       ("rail_tee_s", "ews"), ("rail_tee_e", "nse"), ("rail_tee_w", "nsw")):
        add(name, rail(segs), "decor")
    for s in "nsew":
        add(f"rail_end_{s}", rail_end(s), "decor")
    for v in (0, 1):
        add(f"glare_{v}", glare(v), "ground")
    for fam, anchor in (("rock", CLIFF), ("gold", SANDSTONE), ("ice", ICE)):
        for v in (0, 1):
            add(f"face_{fam}_{v}", face(anchor, v), "wall", collides=True)
        add(f"face_{fam}_foot", face(anchor, 0, foot=True), "wall", collides=True)

    manifest = {"name": "traverse_set", "columns": 8, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (BASE / "traverse_set.index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"traverse_set: {len(tiles)} tiles -> {TILES_DIR}")

    lever(False).save(OBJ_DIR / "lever_off.png")
    lever(True).save(OBJ_DIR / "lever_on.png")
    ore_cart().save(OBJ_DIR / "ore_cart.png")
    switch_stand(False).save(OBJ_DIR / "switch_a.png")
    switch_stand(True).save(OBJ_DIR / "switch_b.png")
    print(f"objects -> {OBJ_DIR} (run pack_objects.py)")

    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)], capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
