#!/usr/bin/env python3
"""
build_deepwater_set — the DEEP WATER accent tileset (`deepwater_set`, 2026-10).

Shallow vs deep water. The shared `water` family is the SHALLOWS: Tidecall (the
Tide Gift, earned at Pearlmoor — the second town) lets you swim it. The open
sea beyond a coast's shallow shelf is DEEP: darker, a slower heavier swell, and
gated on `deepdive` — a RESERVED ability no Gift grants yet (types.ts), so
Tidecall can't carry a player out across open sea to doors and coasts the
journey hasn't reached yet. A future deep-swim mechanic is one
`reward_abilities: ['deepdive']` away; nothing here needs to change for it.

The shared overworld set is FROZEN (TILEFORGE 2026-06), so deep water is an
ACCENT set on the coldfog_set pattern: builders stack it with
`mk.register_tileset("deepwater_set", index=...)` and paint a terrain layer
`{"terrain": "deepwater", "set": "deepwater_set"}` over their water — the
autotiler draws deep→shallow transitions (deep cells only; the rim is the
shallow side showing through, with a soft mid-tone seam — no foam, deep meets
shallow under the surface).

Drawn in code (gbaforge's GBA-register grammar): a flat deep fill + sparse dim
swell marks that drift over 3 frames (1.1 s — slower than the shallows' 0.8 s,
so deep reads heavier), 13 transition roles, 2 still fill variants.

Writes:
  assets/tilesets/deepwater/set_tiles/*.png + tileset.manifest.json  (masters)
  public/assets/tilesets/deepwater_set.{webp,tileset.json}           (served)
  assets/tilesets/deepwater/deepwater_set.index.json                 (name->index)

Run:  python3 tools/maps/build_deepwater_set.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import gbaforge
from gbaforge import sh, flat, put, img, overlay_tile, WATER

REPO = Path(__file__).resolve().parents[2]
TILES_DIR = REPO / "assets" / "tilesets" / "deepwater" / "set_tiles"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"

DEEP = sh(WATER, 0.60)                    # the open sea: a step darker than the shallows
SWELL = [(2, 4), (10, 2), (7, 9), (13, 12), (3, 13)]   # long dim swell marks


def deep_fill(frame: int = 0):
    a = flat(DEEP)
    crest = sh(DEEP, 1.32, 4)
    trough = sh(DEEP, 0.78)
    for i, (x, y) in enumerate(SWELL):
        ph = (i + frame) % 3
        if ph == 0:
            put(a, [(x, y), (x + 1, y), (x + 2, y)], crest)
            put(a, [(x + 1, y + 1)], trough)
        elif ph == 1:
            put(a, [(x + 1, y), (x + 2, y)], sh(DEEP, 1.16, 2))
        # ph 2: the swell has sunk this frame
    return img(a)


def deep_edge(role: str):
    """Deep over shallow: the shallow side shows through where the role's mask
    says, with a soft 1px mid-tone seam (no foam — the shelf drops away)."""
    return overlay_tile(role, deep_fill(0), gbaforge.water_fill(0),
                        sh(WATER, 0.80), shade_rgb=sh(DEEP, 1.10))


NINE = ["corner_nw", "edge_n", "corner_ne", "edge_w", "fill", "edge_e",
        "corner_sw", "edge_s", "corner_se"]
INNER = ["inner_nw", "inner_ne", "inner_sw", "inner_se"]


def main() -> None:
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    for old in TILES_DIR.glob("*.png"):
        old.unlink()
    tiles: list[dict] = []
    index: dict[str, int] = {}

    def add(name: str, im, autotile: str | None, **extra):
        fn = f"{len(tiles):03d}_{name}.png"
        im.save(TILES_DIR / fn)
        index[name] = len(tiles)
        t = {"file": fn, "role": "water", "collides": True, "requires_ability": "deepdive",
             "encounter_terrain": "deep"}   # rowed sea encounters (10 §2)
        if autotile:                       # animation frames carry no terrain role
            t.update({"terrain": "deepwater", "autotile": autotile})
        tiles.append({**t, **extra})

    for role in NINE + INNER:
        add(f"deepwater_{role}", deep_fill(0) if role == "fill" else deep_edge(role),
            autotile=role)
    # the fill's animation frames (not autotile picks — frames only)
    a2 = len(tiles)
    add("deepwater_a2", deep_fill(1), autotile=None)
    add("deepwater_a3", deep_fill(2), autotile=None)
    tiles[index["deepwater_fill"]]["animation"] = {
        "frames": [index["deepwater_fill"], a2, a2 + 1], "duration_ms": 1100}

    manifest = {"name": "deepwater_set", "columns": 6, "tiles": tiles}
    (TILES_DIR / "tileset.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (REPO / "assets/tilesets/deepwater/deepwater_set.index.json").write_text(
        json.dumps(index, indent=2) + "\n")
    print(f"deepwater_set: {len(tiles)} tiles -> {TILES_DIR}")

    res = subprocess.run([sys.executable, str(SCRIPTS / "pack_tileset.py"),
                          "--tiles-dir", str(TILES_DIR)],
                         capture_output=True, text=True)
    print(res.stdout[-600:] if res.returncode == 0 else res.stderr[-1500:])
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
