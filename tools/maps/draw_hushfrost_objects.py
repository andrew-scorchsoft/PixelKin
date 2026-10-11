#!/usr/bin/env python3
"""
draw_hushfrost_objects — the DRAWN ground-craft of Hushfrost Pass (R10 polish,
2026-10: the owner's "still reads a little flat" verdict). The shared overworld
set is FROZEN, so everything that breaks the uniform snow is a NON-SOLID
decal object laid over the terrain (objects body-depth, under actors) or an
above-player strip (overhang = height). Drawn in code (the gbaforge rule: no
paid image-gen for small structural ground marks) in the exact gbaforge snow /
ice / scree register so the decals sit flush on the tiles beneath.

  * tuftbed_<mask>[_vN] (16x16, opaque) — laid over every frost-tuft ENCOUNTER
    cell: the same blade-fan motif on a cold-shadow SNOW bed instead of the
    tile's grey slab, and on every side that meets open snow a ragged, wind-cut
    snow rim (inset 0-3px) so a band's outline breaks up. Still tile-aligned and
    still dense (the hard-edged encounter convention: you can see exactly which
    cells roll), it just stops reading as a grey rectangle. mask = which of
    N/E/S/W (1/2/4/8) neighbours are tuft too.
  * crest_<mask>[_vN] (16x16) — wind-packed snow lying on the glacier banks'
    plateau tops (laid only on true fill cells): crusted snow with scoured blue
    ice showing through, a lit cornice + shadow on open sides. Turns the flat
    blue stripes into snowbound ridges whose ice shows only at the flanks.
  * icicles_a/b (16x16) — icicles hung off a glacier face's lit lip (laid on
    straight edge_s cells): the face gains a fringe + drip shadow.
  * drift_a/b/c — wind-sculpted drift ridges: a lit windward crest, a blue
    lee-side shadow dithered out downwind. Free-form.
  * scree_a/b — exposed rock + scree where the wind has stripped the snow.
  * tracks_h / tracks_v / tracks_d — the boot-prints of earlier walkers.
  * tuft_a/b/c (16x16) — isolated frost-tufts loose on the snow (decor only —
    never encounter tiles) so a band frays out into its surroundings.
  * mist_a/b — a low mist strip that lies in the lee; placed with
    overhang = height so it drifts OVER the player (the depth cue).

Writes assets/tilesets/hushfrost/objects/*.png -> packed `hushfrost_<stem>` by
pack_objects.py. Deterministic (crc32 seeds).

Run:  python3 tools/maps/draw_hushfrost_objects.py
      ./venv/bin/python .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import math
import sys
import zlib
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gbaforge as gf  # noqa: E402

REPO = HERE.parents[1]
OBJDIR = REPO / "assets" / "tilesets" / "hushfrost" / "objects"

SNOW, ICE, SCREE = gf.SNOW, gf.ICE, gf.SCREE
sh = gf.sh
N, E, S, W = 1, 2, 4, 8


def _h(*k) -> int:
    return zlib.crc32(repr(k).encode()) & 0xffffffff


def canvas(w: int, h: int) -> np.ndarray:
    return np.zeros((h, w, 4), dtype=np.int16)


def px(a, x, y, rgb, alpha=255):
    h, w = a.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        a[y, x, :3] = rgb
        a[y, x, 3] = alpha


def save(a, name):
    OBJDIR.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA").save(OBJDIR / f"{name}.png")


def rim_depth(mask: int, seed: str, lo: int = 0, hi: int = 3) -> np.ndarray:
    """Per-pixel distance inset (0..3) for each OPEN side of a cell: a ragged,
    wind-cut profile; corners where two open sides meet are rounded."""
    d = np.zeros((16, 16), dtype=np.int16)
    prof = {}
    for side in (N, E, S, W):
        if mask & side:
            continue
        r = _h(seed, side)
        p = []
        cur = lo + 1 + (r & 1)
        for i in range(16):
            r = (r * 1103515245 + 12345) & 0x7fffffff
            step = (r >> 16) % 5
            if step == 0:
                cur = max(lo, cur - 1)
            elif step == 1:
                cur = min(hi, cur + 1)
            p.append(cur)
        prof[side] = p
    inside = np.zeros((16, 16), dtype=bool)
    for y in range(16):
        for x in range(16):
            out = False
            if N in prof and y < prof[N][x]:
                out = True
            if S in prof and 15 - y < prof[S][x]:
                out = True
            if W in prof and x < prof[W][y]:
                out = True
            if E in prof and 15 - x < prof[E][y]:
                out = True
            # round the convex corners
            for (sa, sb, cx, cy) in ((N, W, 0, 0), (N, E, 15, 0), (S, W, 0, 15), (S, E, 15, 15)):
                if sa in prof and sb in prof:
                    if abs(x - cx) + abs(y - cy) < 5 + lo:
                        out = True
            inside[y, x] = not out
    return inside


# ---- tuftbed: the encounter cells' snow-bed overlay -------------------------------
BED = (138, 154, 192)          # cold shadow-snow under the stalks (vs the grey slab)


def tuftbed(mask: int, v: int) -> np.ndarray:
    a = canvas(16, 16)
    a[..., :3] = BED
    a[..., 3] = 255
    dark = sh(ICE, 0.62)
    mid = sh(ICE, 1.22, 22)
    light = (236, 244, 252)
    # a few mottled shadow pixels in the bed
    r = _h("bedmottle", mask, v)
    for k in range(5):
        r = (r * 1103515245 + 12345) & 0x7fffffff
        x, y = (r >> 8) % 14 + 1, (r >> 16) % 14 + 1
        px(a, x, y, sh(BED, 0.86))
        px(a, x + 1, y, sh(BED, 0.86))
    inside = rim_depth(mask, ("tuft", mask, v))
    snow = np.asarray(gf.snow_fill(v % 4).convert("RGBA")).astype(np.int16)
    a[~inside] = snow[~inside]
    # 1px shadow just inside the rim (the bed sits a touch lower than the snow)
    for y in range(16):
        for x in range(16):
            if inside[y, x]:
                nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                if any(0 <= qx < 16 and 0 <= qy < 16 and not inside[qy, qx] for qx, qy in nb):
                    a[y, x, :3] = sh(BED, 0.84)
    t = np.zeros((16, 16, 4), dtype=np.int16)
    t[..., :3] = a[..., :3]
    t[..., 3] = 255
    for (cx, cy) in gf.TG_LAYOUTS[v % len(gf.TG_LAYOUTS)]:
        gf._fan(t, cx, cy, mid, light, dark)
    # stalks may lean onto the snow rim — that's the point (it frays the edge)
    return t


# ---- crest: snow lying on the glacier plateau tops --------------------------------
def crest(mask: int, v: int) -> np.ndarray:
    a = canvas(16, 16)
    inside = rim_depth(mask, ("crest", mask, v), lo=1, hi=4)
    snow = np.asarray(gf.snow_fill((v + 1) % 4).convert("RGBA")).astype(np.int16)
    crust = sh(SNOW, 1.06, 6)
    a[inside] = snow[inside]
    # frost-crust, not field snow: blend toward the ice so the bank top reads as
    # a hard, higher, colder surface (field snow at the foot stays the brightest)
    a[inside, :3] = (a[inside, :3] * 0.62 + np.array(ICE) * 0.38).astype(np.int16)
    # wind-scoured ice windows inside the crust (transparent -> blue ice below)
    r = _h("scour", mask, v)
    for k in range(1):
        r = (r * 1103515245 + 12345) & 0x7fffffff
        x, y = (r >> 8) % 10 + 3, (r >> 16) % 10 + 3
        ln = 2 + (r >> 4) % 2
        for i in range(ln):
            for (qx, qy) in ((x + i, y), (x + i, y + 1) if i % 2 else (x + i, y)):
                if 0 <= qx < 16 and 0 <= qy < 16:
                    a[qy, qx, 3] = 0
    # sparkle + crust highlight
    for (x, y) in ((4 + v, 3), (11, 9 - v), (6, 12)):
        if inside[y % 16, x % 16] and a[y % 16, x % 16, 3]:
            px(a, x % 16, y % 16, crust)
    # open sides: lit cornice lip on N/W (the lit side), blue shadow on S/E
    for y in range(16):
        for x in range(16):
            if not inside[y, x] or a[y, x, 3] == 0:
                continue
            up = y == 0 or not inside[y - 1, x]
            lf = x == 0 or not inside[y, x - 1]
            dn = y == 15 or not inside[y + 1, x]
            rt = x == 15 or not inside[y, x + 1]
            if (dn and not (mask & S)) or (rt and not (mask & E)):
                a[y, x, :3] = sh(ICE, 0.86)
            elif (up and not (mask & N)) or (lf and not (mask & W)):
                a[y, x, :3] = sh(SNOW, 1.08, 10)
    return a


# ---- icicles on a glacier face (edge_s: lip y4, face y5-12, contact y13) ----------
def icicles(v: int) -> np.ndarray:
    a = canvas(16, 16)
    lit = (226, 238, 250)
    pale = sh(ICE, 1.55, 20)
    blue = sh(ICE, 1.10)
    shade = sh(ICE, 0.62)
    xs = [1, 4, 6, 9, 12, 14] if v == 0 else [2, 3, 7, 10, 11, 13]
    lens = [5, 3, 7, 4, 6, 2] if v == 0 else [3, 6, 4, 7, 3, 5]
    for x, ln in zip(xs, lens):
        # snow cap on the lip
        px(a, x, 4, lit)
        px(a, x - 1, 4, lit)
        for k in range(ln):
            y = 5 + k
            px(a, x, y, pale if k < ln - 1 else blue)
            if k < ln - 2:
                px(a, x + 1, y, blue)
        # drip shadow on the face beside it
        px(a, x + 1, 5 + ln - 1, shade)
    return a


# ---- free-form ground decals ------------------------------------------------------
def drift(w: int, h: int, seed: str) -> np.ndarray:
    """A wind-sculpted drift ridge drawn as the GBA register draws relief: a
    curved white crest line, a lit windward band above it, and a blue lee
    shadow below that tapers at both ends and dithers out downwind — no body
    fill, the snow tile beneath IS the drift's slope."""
    a = canvas(w, h)
    r = _h(seed)
    white = (238, 244, 252)
    lit = sh(SNOW, 1.10, 12)
    lee = sh(SNOW, 0.74)
    lee2 = sh(SNOW, 0.84)
    amp = h * 0.28
    ph = ((r >> 3) & 7) / 7 * math.pi
    for x in range(1, w - 1):
        t = x / (w - 1)
        env = math.sin(t * math.pi)                     # 0 at the ends, 1 mid
        cy = int(round(h * 0.40 + amp * math.sin(t * math.pi * 1.3 + ph) * 0.6))
        px(a, x, cy, white)
        if env > 0.25:
            px(a, x, cy - 1, lit)
        if env > 0.6 and x % 3:
            px(a, x, cy - 2, lit)
        depth = int(round(1 + env * (h * 0.30)))
        for k in range(1, depth + 1):
            if k == depth and (x + k) % 2:
                continue
            px(a, x, cy + k, lee if k <= max(1, depth - 1) else lee2)
    return a


def scree(w: int, h: int, seed: str) -> np.ndarray:
    """Exposed rock + scree where the wind stripped the snow: a lobed patch of
    grey stone ground packed with lit-topped stones (some carrying snow lumps),
    a dithered snow lip so it sinks INTO the snow rather than sitting on it."""
    a = canvas(w, h)
    r = _h(seed)
    cx, cy, rx, ry = w / 2, h / 2, w / 2 - 1.5, h / 2 - 1.5
    lobes = [((r >> (4 * i)) & 15) / 15 * 0.35 for i in range(6)]

    def edge(x, y):
        ang = math.atan2(y - cy, x - cx)
        k = 1 - sum(l * math.cos((i + 2) * ang + i) for i, l in enumerate(lobes)) / 3
        nx, ny = (x - cx) / rx, (y - cy) / ry
        return (nx * nx + ny * ny) / (k * k)
    base = sh(SCREE, 1.16, 6)
    dk = sh(SCREE, 0.70)
    lt = sh(SCREE, 1.50, 14)
    snowlump = (226, 236, 248)
    for y in range(h):
        for x in range(w):
            e = edge(x + 0.5, y + 0.5)
            if e <= 0.80 or (e <= 1.0 and (x + y) % 2):
                px(a, x, y, base)
    rr = _h(seed, "stones")
    for k in range(int(w * h / 22)):
        rr = (rr * 1103515245 + 12345) & 0x7fffffff
        sx, sy = (rr >> 8) % (w - 3) + 1, (rr >> 16) % (h - 3) + 1
        if edge(sx + 0.5, sy + 0.5) > 0.85:
            continue
        size = 1 + (rr >> 4) % 3                      # 1-3 px wide stones
        for dx in range(size + 1):
            px(a, sx + dx, sy, lt)
            px(a, sx + dx, sy + 1, base if size > 1 else dk)
            px(a, sx + dx, sy + 2, dk)
        if size == 3 and (rr >> 6) % 2:
            for dx in range(1, size):
                px(a, sx + dx, sy - 1, snowlump)
    return a


def tracks(w: int, h: int, kind: str) -> np.ndarray:
    """Boot-prints of earlier walkers: paired dents, a blue shadow in each with
    a lit far rim, gently wandering — older ones half-filled (dithered)."""
    a = canvas(w, h)
    dent = sh(SNOW, 0.66)
    rim = sh(SNOW, 1.16, 16)
    steps = []
    if kind == "h":
        for i, x in enumerate(range(1, w - 2, 4)):
            y = 6 + (3 if i % 2 else 0) + (1 if (x // 12) % 2 else 0)
            steps.append((x, y))
    elif kind == "v":
        for i, y in enumerate(range(1, h - 2, 4)):
            x = 5 + (4 if i % 2 else 0) + (1 if (y // 12) % 2 else 0)
            steps.append((x, y))
    else:
        for i, t in enumerate(range(1, w - 2, 4)):
            steps.append((t + (2 if i % 2 else 0), h - 3 - t + (2 if i % 2 else 0) - 2))
    for i, (x, y) in enumerate(steps):
        faded = i % 5 == 4
        for (qx, qy) in ((x, y), (x + 1, y)):
            if not faded or (qx + qy) % 2:
                px(a, qx, qy, dent)
        px(a, x, y - 1, rim)
        px(a, x + 1, y - 1, rim)
    return a


def tuft(v: int) -> np.ndarray:
    a = canvas(16, 16)
    dark = sh(ICE, 0.62)
    mid = sh(ICE, 1.22, 22)
    light = (236, 244, 252)
    shadow = sh(SNOW, 0.80)
    anchors = [[(8, 11)], [(5, 10), (11, 13)], [(4, 12), (9, 9), (12, 13)]][v]
    for (cx, cy) in anchors:
        for dx in range(-3, 4):
            px(a, cx + dx, cy + 2, shadow)
        for dx in range(-2, 3):
            px(a, cx + dx, cy + 1, shadow)
        t = canvas(16, 16)
        gf._fan(t, cx, cy, mid, light, dark)
        # _fan writes rgb only — mark what it drew
        drawn = t[..., :3].sum(axis=2) > 0
        a[drawn, :3] = t[drawn, :3]
        a[drawn, 3] = 255
    return a


def mist(w: int, h: int, seed: str) -> np.ndarray:
    """A low lee-mist strip: soft pale bands, thinning at both ends (alpha only
    — it lies over the player, so it must never hide them)."""
    a = canvas(w, h)
    r = _h(seed)
    col = (232, 240, 250)
    for y in range(h):
        for x in range(w):
            end = min(x, w - 1 - x) / (w * 0.25)
            band = 0.55 + 0.45 * math.sin((x / w) * math.pi * 2 + ((r >> 3) & 7) + y * 0.35)
            vy = 1 - abs((y + 0.5) - h / 2) / (h / 2)
            al = 64 * min(1.0, end) * band * vy
            if al > 6:
                a[y, x, :3] = col
                a[y, x, 3] = int(al)
    return a


def main() -> None:
    n = 0
    for mask in range(16):
        save(tuftbed(mask, 0), f"tuftbed_{mask}")
        if mask:                      # (a lone crest cell is never laid)
            save(crest(mask, 0), f"crest_{mask}")
        n += 2 if mask else 1
    for v in (1, 2):
        save(tuftbed(15, v), f"tuftbed_15_v{v}")
        save(crest(15, v), f"crest_15_v{v}")
        n += 2
    for i, nm in enumerate(("a", "b")):
        save(icicles(i), f"icicles_{nm}")
    save(drift(48, 16, "drift_a"), "drift_a")
    save(drift(64, 32, "drift_b"), "drift_b")
    save(drift(32, 16, "drift_c"), "drift_c")
    save(scree(32, 32, "scree_a"), "scree_a")
    save(scree(48, 32, "scree_b"), "scree_b")
    save(tracks(64, 16, "h"), "tracks_h")
    save(tracks(16, 64, "v"), "tracks_v")
    save(tracks(48, 48, "d"), "tracks_d")
    for i, nm in enumerate(("a", "b", "c")):
        save(tuft(i), f"tuft_{nm}")
    save(mist(96, 16, "mist_a"), "mist_a")
    save(mist(64, 16, "mist_b"), "mist_b")
    print("drawn", n + 2 + 3 + 2 + 3 + 3 + 2, "decals ->", OBJDIR)


if __name__ == "__main__":
    main()
