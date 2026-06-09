#!/usr/bin/env python3
"""
Redraw the interior WALL kits as continuous architecture (and repack both sets).

The original wall masters were generated as single framed squares (with leftover
chroma fringes) — tiled, they read as "bordered squares", not walls. This script
replaces them with a drawn SNES-style wall SYSTEM, per docs/world/interiors.md:

  * a dark WALL-TOP band that frames the whole room (the wall seen from above),
    with a lit inner LIP on whichever side faces the floor — four directional
    tiles + four corner turns, so the lip line wraps the room unbroken;
  * a real FACE only on the north wall (plaster + wood wainscot for the warm kit,
    coursed stone for the cool kit), with a cornice shadow at the top and a
    skirting contact line at the floor;
  * WINDOW (warm: candle-lit panes) / BANNER (cool: deepBlue + diamond emblem)
    drawn as insets ON that face, not as standalone squares.

Writes the masters into assets/tilesets/interior/tiles_{warm,cool}/, rewrites
both manifests (13 tiles), and repacks interior_set + interior_stone_set.
build_interiors.py's faced_room() places them. Deterministic; safe to re-run.

Run:  python3 tools/maps/build_interior_walls.py   (then build_interiors.py)
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
INT = REPO / "assets" / "tilesets" / "interior"
PACK = REPO / ".claude/skills/generate-sprite-sheet/scripts/pack_tileset.py"


def hx(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)] + [255], dtype=np.int16)


def img(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def det(seed):
    return np.random.default_rng(seed)


# ---- palettes (world-palette.json ramps) -------------------------------------
WOOD = [hx("#3a2418"), hx("#7a4a28"), hx("#b9763f"), hx("#e0a466")]
BONE = [hx("#7a6f5a"), hx("#bcae90"), hx("#e6dcc0"), hx("#f8f2e2")]
STONE = [hx("#2a2c40"), hx("#4a4d66"), hx("#6c6f86"), hx("#9a9db4")]
FIRE = [hx("#7a2a14"), hx("#c85a22"), hx("#ff8a3d"), hx("#ffc070")]
DEEPBLUE = hx("#13205a")
DIAMOND = hx("#9fe7ff")
INKDARK = hx("#10121e")


# ---- the wall-TOP band (dark, seen from above) --------------------------------
def cap_base_warm(seed=3):
    """Dark wood planking, toroidal both axes (grain rows + staggered seams)."""
    a = np.zeros((16, 16, 4), np.int16)
    dark = np.array([30, 19, 11, 255], np.int16)
    grain = np.array([40, 26, 14, 255], np.int16)
    seam = np.array([20, 12, 7, 255], np.int16)
    rng = det(seed)
    for y in range(16):
        a[y, :] = grain if y % 4 == 1 else dark
    for y0, off in ((0, 3), (4, 11), (8, 6), (12, 14)):   # staggered plank ends
        for y in range(y0, y0 + 4):
            a[y % 16, off] = seam
    n = rng.integers(-4, 5, size=(16, 16, 1))
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    return a


def cap_base_cool(seed=5):
    """Dark slate stones, toroidal both axes."""
    a = np.zeros((16, 16, 4), np.int16)
    dark = np.array([26, 28, 44, 255], np.int16)
    seam = np.array([16, 18, 30, 255], np.int16)
    rng = det(seed)
    a[:, :] = dark
    for y in (3, 7, 11, 15):                              # courses
        a[y, :] = seam
    for (y0, off) in ((0, 5), (4, 12), (8, 2), (12, 9)):  # staggered joints
        for y in range(y0, min(y0 + 3, 16)):
            a[y, off] = seam
    n = rng.integers(-4, 5, size=(16, 16, 1))
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    return a


def with_lips(base, sides, mid, light, outline):
    """Add the lit inner lip on each side in `sides` ('n','s','e','w'):
    mid step, light edge, then a 1px dark contact outline at the very rim."""
    a = base.copy()
    for s in sides:
        if s == "s":
            a[13, :] = mid; a[14, :] = light; a[15, :] = outline
        elif s == "n":
            a[2, :] = mid; a[1, :] = light; a[0, :] = outline
        elif s == "e":
            a[:, 13] = mid; a[:, 14] = light; a[:, 15] = outline
        elif s == "w":
            a[:, 2] = mid; a[:, 1] = light; a[:, 0] = outline
    return a


# ---- the north-wall FACE -------------------------------------------------------
def face_warm(seed=7):
    """Plaster above a wood wainscot: cornice shadow top, skirting at the floor."""
    a = np.zeros((16, 16, 4), np.int16)
    rng = det(seed)
    a[0, :] = WOOD[0]                                   # cornice contact shadow
    a[1, :] = BONE[1]                                   # shaded plaster under it
    for y in range(2, 10):
        a[y, :] = BONE[2]
    n = rng.integers(-5, 6, size=(16, 16, 1))
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    for x in (4, 11):                                   # faint plaster joints
        a[2:10, x, :3] = np.clip(a[2:10, x, :3] - 10, 0, 255)
    a[10, :] = WOOD[3]                                  # wainscot rail (lit)
    for y in range(11, 14):
        a[y, :] = WOOD[1]
    for x in range(0, 16, 4):                           # wainscot panel seams
        a[11:14, x] = WOOD[0]
    a[12, :] = np.where((np.arange(16) % 4 != 0)[:, None], WOOD[2], a[12, :])
    a[14, :] = WOOD[1]                                  # skirting
    a[15, :] = WOOD[0]                                  # contact line at the floor
    return a


def face_cool(seed=9):
    """Coursed stone shrine wall: shadowed top course, carved seams, base course."""
    a = np.zeros((16, 16, 4), np.int16)
    rng = det(seed)
    for y in range(16):
        a[y, :] = STONE[1]
    n = rng.integers(-6, 7, size=(16, 16, 1))
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    a[0, :] = INKDARK                                   # cornice contact shadow
    a[1, :] = STONE[0]
    for y in (5, 10):                                   # course seams
        a[y, :] = STONE[0]
        a[y - 1, :, :3] = np.clip(a[y - 1, :, :3] + 14, 0, 255)   # lit course top
    for (y0, y1, off) in ((2, 5, 8), (6, 10, 3), (6, 10, 12), (11, 14, 6)):
        a[y0:y1, off] = STONE[0]                        # staggered block joints
    a[14, :] = STONE[0]                                 # base course
    a[15, :] = INKDARK                                  # contact line at the floor
    return a


def window_warm():
    """Candle-lit window inset on the warm face — the cosy glow from outside-in."""
    a = face_warm()
    x0, x1, y0, y1 = 4, 12, 2, 9
    a[y0:y1, x0:x1] = WOOD[0]                           # frame
    a[y0 + 1:y1 - 1, x0 + 1:x1 - 1] = FIRE[2]           # warm panes
    a[y0 + 1, x0 + 1:x1 - 1] = FIRE[3]                  # top glow
    a[y0 + 1:y1 - 1, (x0 + x1) // 2] = WOOD[0]          # mullion
    a[(y0 + y1) // 2, x0 + 1:x1 - 1] = WOOD[0]
    a[y1 - 1, x0:x1] = BONE[3]                          # sill
    return a


def banner_cool():
    """Hanging deepBlue banner with the diamond star emblem, on the stone face."""
    a = face_cool()
    x0, x1 = 5, 11
    a[1, x0 - 1:x1 + 1] = WOOD[1]                       # hanging rod
    for y in range(2, 12):
        a[y, x0:x1] = DEEPBLUE
    a[2, x0:x1, :3] = np.clip(DEEPBLUE[:3] + 24, 0, 255)
    for x in range(x0, x1):                             # fringe
        a[11, x] = DEEPBLUE if x % 2 else INKDARK
    cx, cy = (x0 + x1) // 2, 6                          # diamond emblem
    for (dx, dy) in ((0, -2), (0, 2), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0), (-2, 0), (2, 0), (0, -1), (0, 1), (-1, 0), (1, 0)):
        a[cy + dy, cx + dx] = DIAMOND
    a[cy, cx] = hx("#f8f2e2")
    return a


# ---- assemble both kits --------------------------------------------------------
KITS = {
    "tiles_warm": {
        "set_name": "interior_set",
        "cap": cap_base_warm(), "face": face_warm(), "accent": window_warm(),
        "accent_name": "window",
        "lip": (WOOD[1], WOOD[3], WOOD[0]),
    },
    "tiles_cool": {
        "set_name": "interior_stone_set",
        "cap": cap_base_cool(), "face": face_cool(), "accent": banner_cool(),
        "accent_name": "banner",
        "lip": (STONE[1], STONE[3], STONE[0]),
    },
}

# manifest order — build_interiors.py's constants must match (gid = index + 1)
ORDER = ["floor_fill", "floor_fill_b", "MAT", "face", "ACCENT",
         "cap_s", "cap_n", "cap_e", "cap_w",
         "cap_tl", "cap_tr", "cap_bl", "cap_br"]
LIPS = {"cap_s": "s", "cap_n": "n", "cap_e": "e", "cap_w": "w",
        "cap_tl": "se", "cap_tr": "sw", "cap_bl": "ne", "cap_br": "nw"}

for kit, spec in KITS.items():
    d = INT / kit
    mat_name = "doormat" if kit == "tiles_warm" else "runner"
    mid, light, outline = spec["lip"]
    spec["face_im"] = img(spec["face"])
    spec["face_im"].save(d / "face.png")
    img(spec["accent"]).save(d / f"{spec['accent_name']}.png")
    for nm, sides in LIPS.items():
        img(with_lips(spec["cap"], sides, mid, light, outline)).save(d / f"{nm}.png")
    tiles = []
    for nm in ORDER:
        if nm == "MAT":
            tiles.append({"file": f"{mat_name}.png"})
        elif nm == "ACCENT":
            tiles.append({"file": f"{spec['accent_name']}.png", "collides": True})
        elif nm.startswith("floor"):
            tiles.append({"file": f"{nm}.png"})
        else:
            tiles.append({"file": f"{nm}.png", "collides": True})
    manifest = {"name": spec["set_name"], "columns": 8, "tiles": tiles}
    (d / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    # remove superseded masters so the dir mirrors the manifest
    for old in ("wall_cap.png", "wall_face.png", "wall_corner.png", "wall_s.png"):
        if (d / old).exists():
            (d / old).unlink()
    print(f"{kit}: 13-tile wall system written")

for kit in KITS:
    res = subprocess.run([sys.executable, str(PACK), "--tiles-dir", str(INT / kit)],
                         capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stderr[-900:])
        sys.exit(1)
print("repacked interior_set + interior_stone_set")
