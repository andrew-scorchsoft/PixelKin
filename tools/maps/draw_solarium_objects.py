#!/usr/bin/env python3
"""
draw_solarium_objects — the W2 SOLARIUM + SUNVAULT drawn object kits.

The Sunken Solarium / Sunvault Climb / Helia Vault cluster needs a bespoke
prop set (CLAUDE.md: generate or draw — never reuse another town's hall). The
STATE-PAIR pieces (dead/lit braziers, closed/bloomed night-flowers, withered/
bloomed sun-vines, dim/alight sun-mirror) are drawn in code so each pair locks
the same footprint + silhouette (the flag-swap rule: collision is flag-blind),
in the deliberate cartridge register of gbaforge/interiorforge — flat anchors,
1px ink lines, a few placed motifs, never jitter noise. The one image-gen hero
piece (the Solar Lumenary hall, 6x6) is generated separately; this script
draws a fallback for it only if the gen master is absent.

Palette: gbaforge's WEST anchors (GOLD sun-grass, RUIN bone paving) + the
interiorforge BRASS/FIRE register — stored daylight reads as warm brass-gold,
the long dusk as the deepBlue surround.

Writes  assets/tilesets/solarium/objects/*.png   -> solarium_<stem> keys
        assets/tilesets/sunvault/objects/*.png   -> sunvault_<stem> keys
Then run .claude/skills/generate-sprite-sheet/scripts/pack_objects.py.

Run:  ./venv/bin/python tools/maps/draw_solarium_objects.py
"""
from __future__ import annotations

import numpy as np
from pathlib import Path

from interiorforge import (BRASS, FIRE, INK, canvas, contact_shadow, fill, hx,
                           img, outline)

REPO = Path(__file__).resolve().parents[2]
SOLARIUM = REPO / "assets" / "tilesets" / "solarium" / "objects"
SUNVAULT = REPO / "assets" / "tilesets" / "sunvault" / "objects"

# ---- the W2 register ---------------------------------------------------------------
GOLDL = [hx("#5e5226"), hx("#94803e"), hx("#bda74e"), hx("#e8d27a")]   # sun-gold
RUINS = [hx("#6e6452"), hx("#a4987c"), hx("#cfc2a2"), hx("#ece2c6")]   # bone paving
VINE = [hx("#23402e"), hx("#3c6a44"), hx("#5e9458"), hx("#8cc070")]    # living vine
VINEDRY = [hx("#3a3530"), hx("#5a5244"), hx("#7a6f58")]                # withered vine
PETAL = [hx("#caa43e"), hx("#f0d068"), hx("#ffeea6")]                  # night-flower gold
CLOTH = [hx("#48182a"), hx("#7a2a44"), hx("#a84a62")]                  # troupe wine-cloth
TEAL = [hx("#143c3c"), hx("#1f6a60"), hx("#37978a")]                   # troupe teal
GLOW = np.array([255, 214, 128, 80], np.int16)                         # daylight halo


def halo(a, pts, c=GLOW):
    for (gx, gy) in pts:
        if 0 <= gy < a.shape[0] and 0 <= gx < a.shape[1] and a[gy, gx, 3] == 0:
            a[gy, gx] = c


# =====================================================================================
#  SOLARIUM — the drowned sun-garden + the Heliarium stage
# =====================================================================================
def brazier(lit: bool):
    """2x3 stage brazier: a wide gold bowl on a fluted ruin column. The Lit
    Stage chain's swap pair — same silhouette, the flame is the only change."""
    a = canvas(2, 3)
    W, H = 32, 48
    # plinth + fluted column
    fill(a, 10, 40, 21, 44, RUINS[1])
    a[40, 11:21] = RUINS[2]
    outline(a, 10, 40, 21, 44, INK)
    fill(a, 13, 28, 18, 39, RUINS[1])
    a[28:40, 14] = RUINS[2]
    a[28:40, 17] = RUINS[0]
    # the bowl
    fill(a, 6, 22, 25, 27, BRASS[1])
    a[22, 7:25] = BRASS[2]
    a[23, 8:24] = BRASS[3] if lit else BRASS[2]
    outline(a, 6, 22, 25, 27, BRASS[0])
    # bowl feet
    a[27:29, 7] = BRASS[0]
    a[27:29, 24] = BRASS[0]
    if lit:
        # the tall stored-daylight flame
        fill(a, 12, 12, 19, 21, FIRE[2])
        fill(a, 13, 8, 18, 18, FIRE[2])
        fill(a, 14, 6, 17, 16, FIRE[3])
        fill(a, 15, 10, 16, 20, hx("#ffe9b0"))
        a[4:6, 15] = FIRE[3]
        a[7, 13] = FIRE[1]
        a[9, 18] = FIRE[1]
        halo(a, [(9, 14), (22, 14), (8, 20), (23, 20), (11, 7), (20, 7),
                 (15, 2), (16, 2), (5, 23), (26, 23)])
    else:
        # dead coals + a sleeping glimmer (never relight-able by plain flame)
        fill(a, 12, 19, 19, 21, hx("#2c2620"))
        a[19, 13:19] = hx("#443a2e")
        a[20, 15] = GOLDL[1]
    contact_shadow(a, 6, 25, 45)
    return img(a)


def nightflowers(bloomed: bool):
    """3x1 night-flower row along the stage rim — the purely visual Sunsketch
    FORESHADOW (each brazier lighting blooms one row; no Gift required).
    Non-solid set dressing; same footprint both states."""
    a = canvas(3, 1)
    rng_x = [4, 14, 24, 34, 43]
    for i, cx in enumerate(rng_x):
        # stem + leaves
        a[11:15, cx] = VINE[1]
        a[12, cx - 1] = VINE[2]
        a[13, cx + 1] = VINE[2]
        if bloomed:
            # open gold bloom: petal ring + bright heart
            for (dx, dy) in ((-1, -1), (0, -2), (1, -1), (-2, 0), (2, 0),
                             (-1, 1), (1, 1), (0, 2)):
                y, x = 8 + dy, cx + dx
                if 0 <= y < 16 and 0 <= x < 48:
                    a[y, x] = PETAL[1]
            a[8, cx] = PETAL[2]
            a[6, cx] = GLOW
        else:
            # shut bud, drooped
            a[9:12, cx] = VINEDRY[1]
            a[8, cx] = PETAL[0]
            a[9, cx + 1] = VINEDRY[2]
    for cx in rng_x:
        if a[15, cx, 3] == 0:
            a[15, cx] = np.array([16, 18, 30, 110], np.int16)
    return img(a)


def column():
    """1x3 broken colonnade column — the drowned garden's vertical ruin accent
    (walk-under top row)."""
    a = canvas(1, 3)
    # broken crown (jagged top)
    fill(a, 3, 8, 12, 11, RUINS[2])
    a[6:9, 4] = RUINS[2]
    a[5:9, 9] = RUINS[2]
    a[7:9, 11] = RUINS[1]
    # shaft with flutes + gold overgrowth
    fill(a, 4, 12, 11, 40, RUINS[1])
    a[12:41, 5] = RUINS[2]
    a[12:41, 9] = RUINS[0]
    a[20, 6:9] = GOLDL[1]
    a[30, 5:7] = GOLDL[1]
    outline(a, 4, 12, 11, 40, INK)
    # base
    fill(a, 2, 41, 13, 44, RUINS[1])
    a[41, 3:13] = RUINS[2]
    outline(a, 2, 41, 13, 44, INK)
    contact_shadow(a, 2, 13, 45)
    return img(a)


def column_fallen():
    """3x1 toppled column drum, half in the gold grass."""
    a = canvas(3, 1)
    fill(a, 2, 4, 43, 11, RUINS[1])
    a[4, 3:43] = RUINS[2]
    a[5, 3:43] = RUINS[2]
    # drum joints
    for x in (12, 24, 35):
        a[4:12, x] = RUINS[0]
    # broken end
    a[4:12, 43] = RUINS[0]
    a[6:10, 44] = RUINS[1]
    outline(a, 2, 4, 43, 11, INK)
    # gold overgrowth lapping the stone
    a[11, 6:10] = GOLDL[2]
    a[11, 28:33] = GOLDL[2]
    a[3, 18] = GOLDL[1]
    contact_shadow(a, 2, 44, 12)
    return img(a)


def stage_arch():
    """5x3 the Heliarium proscenium: two pillars + a broken gold lintel with a
    sun-disc at its crown — the stage's walk-under backdrop."""
    a = canvas(5, 3)
    W, H = 80, 48
    # pillars
    for px in (4, 68):
        fill(a, px, 12, px + 7, 43, RUINS[1])
        a[12:44, px + 1] = RUINS[2]
        a[12:44, px + 6] = RUINS[0]
        outline(a, px, 12, px + 7, 43, INK)
        fill(a, px - 2, 40, px + 9, 43, RUINS[1])
        outline(a, px - 2, 40, px + 9, 43, INK)
    # the lintel (broken at the east end)
    fill(a, 4, 6, 60, 13, RUINS[2])
    a[6, 5:60] = RUINS[3]
    outline(a, 4, 6, 60, 13, INK)
    a[7:13, 60] = RUINS[1]          # the break
    a[8:12, 62] = RUINS[0]
    fill(a, 64, 8, 75, 13, RUINS[2])  # the fallen-back fragment over the east pillar
    outline(a, 64, 8, 75, 13, INK)
    # the sun-disc at the crown
    for (dx, dy) in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, -1), (-1, 1), (1, 1)):
        a[6 + dy, 32 + dx] = BRASS[2]
    a[5:8, 31:34] = BRASS[3]
    a[6, 32] = hx("#ffeea6")
    halo(a, [(28, 3), (36, 3), (32, 1), (26, 7), (38, 7)])
    # gold overgrowth on the pillar feet
    a[43, 6:10] = GOLDL[2]
    a[43, 70:74] = GOLDL[2]
    contact_shadow(a, 2, 13, 44)
    contact_shadow(a, 66, 77, 44)
    return img(a)


def troupe_cart():
    """3x2 the Last-Warm-Day troupe's caravan cart: wine-cloth canopy, gold
    trim, a hung lantern — their whole theatre in one wagon."""
    a = canvas(3, 2)
    # wheels
    for wx in (6, 38):
        fill(a, wx, 22, wx + 5, 27, hx("#3a2418"))
        a[23:27, wx + 2] = hx("#7a4a28")
        outline(a, wx, 22, wx + 5, 27, INK)
    # bed
    fill(a, 2, 18, 45, 23, hx("#7a4a28"))
    a[18, 3:45] = hx("#b9763f")
    outline(a, 2, 18, 45, 23, INK)
    # canopy (wine cloth, gold trim, patched)
    fill(a, 4, 4, 43, 17, CLOTH[1])
    a[4, 5:43] = CLOTH[2]
    a[5, 5:43] = CLOTH[2]
    a[16, 5:43] = CLOTH[0]
    outline(a, 4, 4, 43, 17, INK)
    a[8, 9:39] = GOLDL[2]            # the gold trim band
    fill(a, 30, 10, 35, 14, TEAL[1])  # the teal patch
    a[10, 31:35] = TEAL[2]
    # the sun-disc painted on the canopy
    a[11:14, 14:17] = BRASS[3]
    a[12, 12] = BRASS[2]
    a[12, 18] = BRASS[2]
    # hung lantern at the tail
    a[7:9, 44] = BRASS[1]
    a[9:12, 43:46] = BRASS[2]
    a[10, 44] = FIRE[3]
    contact_shadow(a, 2, 45, 28)
    return img(a)


def costume_rack():
    """2x2 the troupe's costume rack: hung festival costumes + a spare gilt
    sun-mask — the X2 quest's visual rhyme."""
    a = canvas(2, 2)
    # frame
    a[4, 2:30] = hx("#7a4a28")
    a[5, 2:30] = hx("#3a2418")
    a[4:28, 2] = hx("#7a4a28")
    a[4:28, 29] = hx("#7a4a28")
    fill(a, 1, 27, 4, 29, hx("#3a2418"))
    fill(a, 28, 27, 31, 29, hx("#3a2418"))
    # hung costumes
    fill(a, 5, 6, 11, 20, CLOTH[1])
    a[6, 6:11] = CLOTH[2]
    a[19, 6:11] = CLOTH[0]
    fill(a, 13, 6, 19, 22, TEAL[1])
    a[6, 14:19] = TEAL[2]
    a[21, 14:19] = TEAL[0]
    fill(a, 21, 6, 26, 18, GOLDL[2])
    a[6, 22:26] = GOLDL[3]
    a[17, 22:26] = GOLDL[1]
    # the spare sun-mask hung on the end post
    a[8:12, 27:31] = BRASS[2]
    a[9, 28] = INK
    a[9, 30] = INK
    a[11, 28:31] = BRASS[3]
    contact_shadow(a, 1, 31, 30)
    return img(a)


def sun_mask():
    """1x1 the troupe's gilt sun-mask, sunk in the flooded side room (X2's
    dive-cache dressing — non-solid silt glint). A TILTED OVAL half-buried
    in a silt drift (W8 MIN-3: the old square face read as an unresolved
    placeholder glyph at map scale — round silhouette, buried lower lip,
    petal-glint rays say 'a dropped treasure', not 'a missing sprite')."""
    a = canvas(1, 1)
    # the mask: a tilted gilt oval, brow lifted out of the silt
    spans = {4: (7, 11), 5: (6, 12), 6: (5, 13), 7: (5, 13), 8: (5, 13),
             9: (6, 12), 10: (7, 11)}
    for y, (x0, x1) in spans.items():
        a[y, x0:x1] = BRASS[2]
    # rim light along the upper-left arc; shaded under-curve
    a[4, 7:10] = BRASS[3]
    a[5, 6] = BRASS[3]
    a[6, 5] = BRASS[3]
    a[9, 7:12] = BRASS[1]
    a[10, 7:11] = BRASS[0]
    # eye holes on the tilt + the quiet smile
    a[6, 7] = INK
    a[7, 10] = INK
    a[8, 6:9] = BRASS[0]
    # the silt drift swallowing the mask's lower lip (bone-paving register)
    a[10, 4:13] = RUINS[2]
    a[11, 3:14] = RUINS[1]
    a[12, 5:12] = RUINS[1]
    a[11, 5:9] = RUINS[2]
    contact_shadow(a, 3, 13, 13)
    # ray stubs catching the lamp — the glint that says LOOK
    a[3, 6] = PETAL[1]
    a[2, 10] = PETAL[2]
    a[5, 13] = PETAL[1]
    halo(a, [(4, 1), (12, 2), (14, 6), (2, 5)])
    return img(a)


def lumenary_fallback():
    """6x6 drawn fallback for the Solar Lumenary hall (only written if the
    image-gen master is absent — see gen_solarium_lumenary.py)."""
    a = canvas(6, 6)
    W, H = 96, 96
    # hall body
    fill(a, 6, 34, 89, 89, RUINS[1])
    outline(a, 6, 34, 89, 89, INK)
    # roof: a shallow gold dome over a bone cornice
    fill(a, 4, 26, 91, 35, RUINS[2])
    outline(a, 4, 26, 91, 35, INK)
    for y in range(8, 26):
        span = int(38 * (1 - ((25 - y) / 18) ** 2) ** 0.5) + 6
        fill(a, 48 - span, y, 47 + span, y, GOLDL[2])
        a[y, 48 - span] = GOLDL[0]
        a[y, 47 + span] = GOLDL[0]
    a[8:26:3, 20:76] = GOLDL[3]      # dome ribs (light bands)
    # the sun-disc finial
    a[3:7, 46:50] = BRASS[3]
    a[4, 44] = BRASS[2]
    a[4, 51] = BRASS[2]
    # face: pilasters + the tall door + lit windows
    for px in (10, 42, 52, 84):
        a[36:88, px] = RUINS[2]
        a[36:88, px + 1] = RUINS[0]
    fill(a, 44, 56, 51, 87, hx("#2c2620"))     # door recess
    fill(a, 45, 58, 50, 87, BRASS[1])
    a[58, 46:50] = BRASS[2]
    outline(a, 44, 56, 51, 87, INK)
    for wx in (18, 66):
        fill(a, wx, 48, wx + 11, 66, FIRE[3])
        a[49, wx + 1:wx + 11] = hx("#ffe9b0")
        outline(a, wx, 48, wx + 11, 66, INK)
    # gold overgrowth at the foot
    a[88, 12:24] = GOLDL[2]
    a[88, 70:82] = GOLDL[2]
    contact_shadow(a, 6, 89, 90)
    return img(a)


# =====================================================================================
#  SUNVAULT — sun-vine bridges, the mirror flower, the reliquary
# =====================================================================================
def _vine_cell(a, x, y, alive: bool, w=16):
    """One braided vine cell into array a at px offset (x,y)."""
    P = VINE if alive else VINEDRY
    a[y + 2:y + 14, x + 6] = P[1]
    a[y + 2:y + 14, x + 9] = P[1]
    a[y + 4, x + 6:x + 10] = P[2]
    a[y + 9, x + 6:x + 10] = P[2]
    a[y + 6, x + 4] = P[2]
    a[y + 11, x + 11] = P[2]
    if alive:
        a[y + 4, x + 3] = PETAL[1]
        a[y + 10, x + 12] = PETAL[1]
        a[y + 7, x + 7:x + 9] = PETAL[2]
    else:
        a[y + 7, x + 7] = VINEDRY[2]


def vine_v(alive: bool, cells: int):
    """1xN vertical sun-vine span (withered/bloomed pair, same footprint)."""
    a = canvas(1, cells)
    for i in range(cells):
        _vine_cell(a, 0, i * 16, alive)
    # anchor knots top + bottom
    a[0:2, 5:11] = (VINE if alive else VINEDRY)[0]
    a[cells * 16 - 2:cells * 16, 5:11] = (VINE if alive else VINEDRY)[0]
    if alive:
        halo(a, [(2, 8), (13, 8), (2, cells * 16 - 9), (13, cells * 16 - 9)])
    return img(a)


def vine_h(alive: bool):
    """3x1 horizontal sun-vine span."""
    a = canvas(3, 1)
    P = VINE if alive else VINEDRY
    a[6, 2:46] = P[1]
    a[9, 2:46] = P[1]
    for x in range(6, 44, 7):
        a[4 + (x // 7 % 2) * 7, x] = P[2]
        a[7, x] = P[2]
        a[8, x + 3] = P[2]
    if alive:
        for x in (10, 24, 38):
            a[5, x] = PETAL[1]
            a[10, x + 3] = PETAL[2]
        halo(a, [(4, 2), (28, 2), (44, 12)])
    a[5:11, 0:2] = P[0]
    a[5:11, 46:48] = P[0]
    return img(a)


def vine_gate(alive: bool):
    """2x3 the boundary gorge bridge (Sunvault I->II): the grand double-braid
    that 'died when the long night fell' and blooms open with Sunsketch."""
    a = canvas(2, 3)
    for i in range(3):
        _vine_cell(a, 0, i * 16, alive)
        _vine_cell(a, 16, i * 16, alive)
    P = VINE if alive else VINEDRY
    # the cross-laced boards (a real bridge, not just vines)
    for y in (10, 24, 38):
        a[y, 3:29] = RUINS[1] if alive else VINEDRY[0]
        a[y + 1, 3:29] = RUINS[0] if alive else VINEDRY[0]
    a[0:3, 2:30] = P[0]
    a[45:48, 2:30] = P[0]
    if alive:
        for (x, y) in ((4, 6), (27, 14), (4, 30), (27, 34)):
            a[y, x] = PETAL[1]
        halo(a, [(1, 4), (30, 4), (1, 43), (30, 43), (15, 0), (16, 0)])
    return img(a)


def mirror(alight: bool):
    """1x2 the sun-mirror flower (Helia's redirect beat): a great dish-bloom
    that bends a pocket of daylight to a vine you can't reach."""
    a = canvas(1, 2)
    # stem + leaves
    a[18:28, 7] = VINE[1]
    a[18:28, 8] = VINE[0]
    a[21, 5:7] = VINE[2]
    a[24, 9:11] = VINE[2]
    fill(a, 5, 27, 10, 29, VINE[0])
    # the dish bloom
    for (x0, y0, x1, y1, c) in ((3, 6, 12, 13, PETAL[0]),
                                (4, 7, 11, 12, PETAL[1])):
        fill(a, x0, y0, x1, y1, c)
    outline(a, 3, 6, 12, 13, INK)
    if alight:
        fill(a, 6, 8, 9, 11, hx("#ffeea6"))
        a[9, 7] = PETAL[2]
        a[10, 10] = PETAL[2]
        # the bent beam glancing off the dish (up-right)
        a[4, 13] = GLOW
        a[2, 15] = GLOW
        halo(a, [(1, 5), (14, 5), (7, 2), (8, 2), (0, 10), (15, 10)])
    else:
        fill(a, 6, 8, 9, 11, PETAL[0])
        a[9, 7] = GOLDL[1]
    contact_shadow(a, 4, 11, 30)
    return img(a)


def reliquary():
    """3x3 the Helia Vault reliquary: a sealed gold shrine-case, the most
    concentrated pocket of stored daylight in Vesperholm (Heliovast's seal)."""
    a = canvas(3, 3)
    W, H = 48, 48
    # stepped plinth
    fill(a, 4, 38, 43, 43, RUINS[1])
    a[38, 5:43] = RUINS[2]
    outline(a, 4, 38, 43, 43, INK)
    # the case
    fill(a, 10, 12, 37, 37, BRASS[1])
    a[12:38, 11] = BRASS[2]
    a[12:38, 36] = BRASS[0]
    outline(a, 10, 12, 37, 37, INK)
    # gable
    for i in range(6):
        a[11 - i, 14 + i:34 - i] = BRASS[2]
    a[5, 23:25] = BRASS[3]
    # the sun-door: a sealed disc with rays
    for (dx, dy) in ((-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, -2), (-2, 2), (2, 2)):
        a[24 + dy, 23 + dx] = BRASS[3]
    fill(a, 21, 22, 25, 26, hx("#ffeea6"))
    a[24, 23] = hx("#fff8da")
    # the seal-bands
    a[16, 12:36] = BRASS[0]
    a[32, 12:36] = BRASS[0]
    halo(a, [(8, 18), (39, 18), (8, 30), (39, 30), (23, 2), (24, 2)])
    # gold overgrowth on the plinth
    a[43, 8:13] = GOLDL[2]
    a[43, 34:39] = GOLDL[2]
    contact_shadow(a, 4, 43, 44)
    return img(a)


# =====================================================================================
def main() -> None:
    SOLARIUM.mkdir(parents=True, exist_ok=True)
    SUNVAULT.mkdir(parents=True, exist_ok=True)
    out: list[tuple[Path, object]] = [
        (SOLARIUM / "brazier_dead.png", brazier(False)),
        (SOLARIUM / "brazier_lit.png", brazier(True)),
        (SOLARIUM / "nightflowers_closed.png", nightflowers(False)),
        (SOLARIUM / "nightflowers_bloomed.png", nightflowers(True)),
        (SOLARIUM / "column.png", column()),
        (SOLARIUM / "column_fallen.png", column_fallen()),
        (SOLARIUM / "stage_arch.png", stage_arch()),
        (SOLARIUM / "troupe_cart.png", troupe_cart()),
        (SOLARIUM / "costume_rack.png", costume_rack()),
        (SOLARIUM / "sun_mask.png", sun_mask()),
        (SUNVAULT / "vine_v_withered.png", vine_v(False, 3)),
        (SUNVAULT / "vine_v_bloomed.png", vine_v(True, 3)),
        (SUNVAULT / "vine_far_withered.png", vine_v(False, 4)),
        (SUNVAULT / "vine_far_bloomed.png", vine_v(True, 4)),
        (SUNVAULT / "vine_h_withered.png", vine_h(False)),
        (SUNVAULT / "vine_h_bloomed.png", vine_h(True)),
        (SUNVAULT / "vine_gate_withered.png", vine_gate(False)),
        (SUNVAULT / "vine_gate_bloomed.png", vine_gate(True)),
        (SUNVAULT / "mirror_dim.png", mirror(False)),
        (SUNVAULT / "mirror_alight.png", mirror(True)),
        (SUNVAULT / "reliquary.png", reliquary()),
    ]
    # the image-gen hero piece's drawn fallback (never clobber a gen master)
    hall = SOLARIUM / "lumenary.png"
    if not hall.exists():
        out.append((hall, lumenary_fallback()))
    for path, im in out:
        im.save(path)
        print(f"  wrote {path.relative_to(REPO)}  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
