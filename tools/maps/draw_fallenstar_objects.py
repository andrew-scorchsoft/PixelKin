#!/usr/bin/env python3
"""
draw_fallenstar_objects — the FALLEN STAR set-pieces of the peril thread (R9,
docs/world/walkthrough/08-the-peril-thread.md): the orchard strike in Duskapple
Orchard and the second, colder fall on Hushfrost Pass. Drawn in code (the
gbaforge rule: no paid image-gen for small structural props):

  * cinder_star (32x32, 2x2) — the spent star that struck the orchard: a dark,
    fissured cinder half-sunk in its bowl, the cracks still holding a COLD
    blue-grey glow (no gold — the warm core the Starfall shards carry is
    exactly what has gone out of it). Solid scenery at the crater's heart.
    After `flag:dawn` it swaps for `vigil_star_shard` (same 2x2 footprint +
    solidity): it was never dead, only guttered.
  * crater (96x64, 6x4) — the STRIKE itself, a NON-SOLID ground decal laid
    over the grass (objects body-depth, under actors): a radial scorch with
    blast-streak fingers dithered into the grass, a bare ash-earth bowl with a
    lit north lip, a charred pit, cold cracks radiating from where the cinder
    sits, ember specks and thrown grit. Tiles can't draw this (the shared set
    is frozen and its fills square off a blob) — one drawn decal reads at a
    glance as "something fell here".
  * crater_snow (96x64, 6x4) — the same strike on snow (Hushfrost Pass): the
    singed-grass ring becomes a ring of melt-slush, same bowl/pit/cracks.
  * tree_charred (48x64, 3x4) — a burnt orchard tree: the served
    `tinderwick_tree` trunk + ground shadow re-coloured to charcoal under a
    DRAWN bare crown (forked limbs, a few scorched leaf-clumps, ember specks,
    ash flecks). Same footprint/overhang as the living tree, so the
    `flag:dawn` swap back to `tinderwick_tree` is collision-identical.

Writes assets/tilesets/fallenstar/objects/*.png — packed to `fallenstar_crater` /
`fallenstar_crater_snow` / `fallenstar_cinder_star` / `fallenstar_tree_charred` by
pack_objects.py. Deterministic (crc32 seeds).

Run:  python3 tools/maps/draw_fallenstar_objects.py
      python3 .claude/skills/generate-sprite-sheet/scripts/pack_objects.py
"""
from __future__ import annotations

import math
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
OBJDIR = REPO / "assets" / "tilesets" / "fallenstar" / "objects"

INK = (14, 10, 16, 255)
CH = [(30, 24, 28), (46, 38, 40), (66, 56, 54), (92, 80, 74)]   # charcoal ramp
EMBER = [(176, 74, 36), (226, 132, 58)]
ASH = (120, 112, 108)
COLD = [(70, 86, 118), (112, 132, 170), (168, 186, 214)]          # guttered starlight


def _h(*k) -> int:
    return zlib.crc32(repr(k).encode()) & 0xffffffff


def _put(px, w, h, x, y, rgba) -> None:
    if 0 <= x < w and 0 <= y < h:
        px[x, y] = rgba


def cinder_star() -> Image.Image:
    im = Image.new("RGBA", (32, 32))
    px = im.load()
    d = ImageDraw.Draw(im)
    # the bowl it sits in: ash-dark ellipse, lit lip on the north rim
    d.ellipse([3, 18, 28, 30], fill=(40, 34, 40, 255))
    d.ellipse([6, 20, 25, 29], fill=(26, 22, 28, 255))
    for x in range(8, 24):
        _put(px, 32, 32, x, 18, (96, 86, 88, 255))
    # the cinder: a lumpy, faceted stone, ink outline, charcoal body
    body = [(9, 25), (7, 19), (9, 12), (14, 8), (20, 9), (24, 13), (25, 20), (22, 25)]
    d.polygon(body, fill=INK)
    inner = [(10, 24), (8, 19), (10, 13), (14, 9), (20, 10), (23, 14), (24, 20), (21, 24)]
    d.polygon(inner, fill=(*CH[1], 255))
    # lit NW facet + shaded SE facet (the 3/4 light every prop shares)
    d.polygon([(10, 13), (14, 9), (17, 10), (13, 15), (9, 18)], fill=(*CH[2], 255))
    d.polygon([(19, 17), (23, 15), (24, 20), (21, 24), (17, 23)], fill=(*CH[0], 255))
    # the fissures: cold guttered light, brightest at the deepest seam
    cracks = [[(12, 12), (14, 15), (13, 18), (15, 21)],
              [(14, 15), (18, 14), (20, 17)],
              [(18, 14), (19, 11)],
              [(13, 18), (10, 20)]]
    for i, line in enumerate(cracks):
        d.line(line, fill=(*COLD[0], 255), width=1)
    for (x, y) in [(14, 15), (13, 17), (17, 14), (15, 20)]:
        _put(px, 32, 32, x, y, (*COLD[2 if (x + y) % 2 else 1], 255))
    # a faint cold halo + a couple of last motes lifting off
    for (x, y, a) in [(5, 10, 110), (27, 8, 100), (16, 4, 130), (26, 16, 80)]:
        _put(px, 32, 32, x, y, (*COLD[2], a))
    # ash scatter on the bowl floor
    for i in range(9):
        x = 6 + _h("ash", i) % 20
        y = 25 + _h("ashy", i) % 4
        if px[x, y][3] and px[x, y][:3] != INK[:3]:
            _put(px, 32, 32, x, y, (*ASH, 255))
    return im


GRASS = (43, 107, 101)          # grass0's flat fill — the dither partner at the rim
SCORCH = [(30, 44, 40), (38, 52, 46)]   # singed grass
SLUSH = [(84, 94, 116), (100, 110, 132)]  # melt-slush on snow
EARTH = [(58, 48, 46), (74, 62, 56), (96, 82, 72), (122, 106, 92)]   # bare ash-earth
PIT = [(18, 14, 20), (28, 22, 28)]


def crater(ring=SCORCH) -> Image.Image:
    W, H = 96, 64
    im = Image.new("RGBA", (W, H))
    px = im.load()
    cx, cy = 48.0, 31.0

    def ang_noise(a: float, freq: int, salt: str) -> float:
        # smooth periodic noise over the angle: blend of a few seeded sines
        v = 0.0
        for k in range(1, 4):
            ph = (_h(salt, k) % 628) / 100.0
            amp = ((_h(salt, k, "a") % 100) / 100.0) / k
            v += amp * math.sin(a * freq * k + ph)
        return v

    for y in range(H):
        for x in range(W):
            dx, dy = (x - cx) / 46.0, (y - cy) / 30.0
            r = math.hypot(dx, dy)
            a = math.atan2(dy, dx)
            # blast fingers: sharp angular spikes on the outer scorch
            spike = (max(0.0, ang_noise(a, 7, "spike")) * 0.22
                     + max(0.0, ang_noise(a, 13, "spike2")) * 0.14)
            r_out = 0.72 + spike + 0.06 * ang_noise(a, 3, "wob")
            if r > r_out:
                continue
            edge = r_out - r
            if edge < 0.05 and (x + y) % 2:          # dithered rim into the grass
                continue
            if r < 0.20:                              # the charred pit
                c = PIT[(x * 3 + y) % 2]
            elif r < 0.30:                            # inner bowl wall (shadowed south)
                c = EARTH[0] if dy > 0 else EARTH[1]
            elif r < 0.38:                            # the raised LIP — lit north, dark south
                c = EARTH[3] if dy < -0.05 else (EARTH[2] if dy < 0.12 else EARTH[0])
            elif r < 0.52:                            # thrown ash-earth apron
                c = EARTH[1] if _h("ap", x, y) % 5 else EARTH[2]
            else:                                     # singed grass, streaked
                c = ring[_h("sc", x // 2, y // 2) % 2]
                if _h("tuft", x, y) % 41 == 0:
                    c = EARTH[1]
            px[x, y] = (*c, 255)

    # cold cracks radiating out of the pit through the lip and apron
    for k in range(7):
        a = k * (2 * math.pi / 7) + ((_h("crk", k) % 60) / 100.0)
        length = 0.42 + (_h("crl", k) % 20) / 100.0
        x0, y0 = cx, cy
        for t in range(1, 40):
            f = t / 40.0 * length
            jx = ((_h("cj", k, t) % 3) - 1) * 0.6
            x1 = int(round(cx + math.cos(a) * f * 46.0 + jx))
            y1 = int(round(cy + math.sin(a) * f * 30.0))
            if 0 <= x1 < W and 0 <= y1 < H and px[x1, y1][3]:
                inner = f < 0.30
                px[x1, y1] = (*(COLD[1] if inner else (40, 36, 44)), 255)
    # a few embers still glowing in the apron + the singe, and thrown grit
    for i in range(16):
        x = _h("emx", i) % W
        y = _h("emy", i) % H
        if px[x, y][3] and px[x, y][:3] in ring + EARTH[:2]:
            px[x, y] = (*EMBER[i % 2], 255)
    for i in range(22):
        x = _h("gx", i) % W
        y = _h("gy", i) % H
        if px[x, y][3] and y + 1 < H:
            px[x, y] = (*EARTH[3], 255)
            if px[x, y + 1][3]:
                px[x, y + 1] = (*INK[:3], 255)
    return im


def tree_charred() -> Image.Image:
    src = Image.open(REPO / "public/assets/sprites/objects/tinderwick_tree.webp").convert("RGBA")
    W, H = src.size
    sp = src.load()
    out = Image.new("RGBA", (W, H))
    op = out.load()
    trunk_top = 44
    # 1) trunk + ground shadow from the living tree, re-coloured to charcoal
    for y in range(trunk_top, H):
        for x in range(W):
            r, g, b, a = sp[x, y]
            if a == 0:
                continue
            if r < 16 and g < 16 and b > 24:      # the ground-shadow ellipse
                if y >= 50:
                    op[x, y] = (r, g, b, a)
                continue
            if y < 54 and abs(x - W // 2) > 4:    # drop the green crown's lower rim
                continue
            lum = 0.3 * r + 0.55 * g + 0.15 * b
            op[x, y] = (*CH[max(0, min(3, int(lum / 22)))], a)

    # 2) the bare, burnt crown: recursive forks from the trunk top
    segs: list[tuple[float, float, float, float, int]] = []

    def branch(x, y, ang, length, width, depth, salt):
        if depth == 0 or length < 2:
            return
        x2 = x + math.cos(ang) * length
        y2 = y - math.sin(ang) * length
        segs.append((x, y, x2, y2, width))
        for i in range(2 if depth > 1 else 1):
            jitter = ((_h(salt, i, depth) % 100) / 100.0 - 0.5) * 0.5
            spread = 0.55 if i == 0 else -0.55
            branch(x2, y2, ang + spread + jitter, length * 0.72, max(1, width - 1),
                   depth - 1, salt * 7 + i + 1)

    cx = W // 2
    branch(cx, trunk_top + 1, math.pi / 2, 14, 3, 5, 1)
    branch(cx - 1, trunk_top - 4, math.pi / 2 + 0.75, 9, 2, 4, 2)
    branch(cx + 1, trunk_top - 6, math.pi / 2 - 0.8, 9, 2, 4, 3)
    d = ImageDraw.Draw(out)
    for (x1, y1, x2, y2, w) in segs:
        d.line([(x1, y1), (x2, y2)], fill=INK, width=w + 2)
    for (x1, y1, x2, y2, w) in segs:
        d.line([(x1, y1), (x2, y2)], fill=(*CH[1], 255), width=w)
    for (x1, y1, x2, y2, w) in segs:
        if w >= 2:
            d.line([(x1 - 1, y1 - 1), (x2 - 1, y2 - 1)], fill=(*CH[2], 255), width=1)

    # 3) clinging scorched leaf-clumps, a few ember specks, drifting ash
    tips = [(int(x2), int(y2)) for (_, _, x2, y2, w) in segs if w == 1]
    for i, (tx, ty) in enumerate(tips):
        if _h("clump", i) % 3 == 0 and 2 <= tx < W - 3 and 2 <= ty < trunk_top:
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 1], fill=INK)
            d.ellipse([tx - 1, ty - 1, tx + 1, ty], fill=(*CH[2], 255))
        if _h("ember", i) % 6 == 0 and 0 <= tx < W and 0 <= ty < H:
            op[tx, ty] = (*EMBER[_h("ec", i) % 2], 255)
    for i in range(10):
        x = 4 + _h("ashx", i) % (W - 8)
        y = 2 + _h("ashy", i) % (trunk_top - 6)
        if op[x, y][3] == 0:
            op[x, y] = (*ASH, 160)
    return out


def main() -> None:
    OBJDIR.mkdir(parents=True, exist_ok=True)
    crater().save(OBJDIR / "crater.png")
    crater(SLUSH).save(OBJDIR / "crater_snow.png")
    cinder_star().save(OBJDIR / "cinder_star.png")
    tree_charred().save(OBJDIR / "tree_charred.png")
    print(f"4 fallen-star masters -> {OBJDIR.relative_to(REPO)} — now run pack_objects.py")


if __name__ == "__main__":
    main()
