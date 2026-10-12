#!/usr/bin/env python3
"""
Warp-marker audit — every warp a player can step on mid-map must LOOK like a
way through (CI gate).

An edge warp reads for free (the map runs off the screen there) and a door is
a door; every OTHER warp — a ladder, a shaft, a cave mouth, a stair, a pier's
end, a Vigil seam, the Old Light's slide — needs a visible marker, or a player
walks onto a plain floor tile and is whisked away (the owner's "are those two
corner squares stairs?").

A warp at (x, y) is MARKED when one of these is true:

  TILE    a marker tile sits under it in any non-above layer — the cave
          ladders, the traverse ladders, the seams shaft family.
  OBJECT  a marker object's footprint COVERS the warp tile, or its bottom row
          sits DIRECTLY NORTH of it (a winch, a headframe, an arch in the wall
          above). Marker objects are the `markers_*` set
          (tools/maps/draw_warp_markers.py) plus the named way-through sprites
          in MARKER_SPRITES — decoration (a tree, a crystal) never counts.

Flags: a warp gated `requires_flag: F` is only live once F is held, so a
marker that only appears with F (`requires_flag: F`) still marks it. A marker
that VANISHES on a flag (`hidden_when_flag: G`) only counts if a twin marker
with `requires_flag: G` takes over on the same warp. A marker gated on any
other flag does not count (it would be missing while the warp is live).

Run:   python3 tools/maps/audit_warp_markers.py           # whole world
       python3 tools/maps/audit_warp_markers.py <map_id>
Exit 1 on any unmarked warp (minus ALLOW, each entry with its WHY).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS_DIR = REPO / "public/assets/maps"
TILESETS_DIR = REPO / "public/assets/tilesets"
INDEXES = {
    "vesper_overworld_set": REPO / "assets/tilesets/_shared/vesper_overworld.index.json",
    "traverse_set": REPO / "assets/tilesets/traverse/traverse_set.index.json",
    "seams_set": REPO / "assets/tilesets/seams/seams_set.index.json",
}

# tile names (per tileset) that read as a way through on their own
MARKER_TILES = {
    "vesper_overworld_set": {"cave_ladder_down", "cave_ladder_up"},
    "traverse_set": {"ladder", "ladder_top"},
}
MARKER_TILE_PREFIX = {"seams_set": ("shaft_",)}

# named way-through sprites beyond the markers_* set
MARKER_SPRITES = {
    "interior_stairs_up", "interior_stairs_down",     # roomkit's stair dressing
    "galehigh_winch",                                 # the Skyloft winch
    "old_seams_headframe",                            # a pit-head over its shaft
    "windward_updraft",                               # the kite thermal you ride
}
MARKER_PREFIX = ("markers_",)

# (map_id, warp_id) -> WHY it may stay unmarked. Keep this tiny.
ALLOW: dict[tuple[str, str], str] = {}


def tile_names(m: dict) -> list[tuple[int, int, dict[int, str]]]:
    """[(first_gid, tile_count, local_index -> name)] for the map's tilesets."""
    out = []
    for ts in m.get("tilesets", []):
        idx_path = INDEXES.get(ts["name"])
        rev = {}
        if idx_path and idx_path.is_file():
            rev = {v: k for k, v in json.loads(idx_path.read_text()).items()}
        count = ts.get("tile_count")
        if count is None:
            side = TILESETS_DIR / f"{ts['name']}.tileset.json"
            count = json.loads(side.read_text()).get("tile_count", 0) if side.is_file() else 0
        out.append((ts.get("first_gid", 1), count, ts["name"], rev))
    return out


def tile_marks(m: dict, x: int, y: int) -> str | None:
    sets = tile_names(m)
    for layer in m.get("layers", []):
        if layer.get("role") == "above":
            continue
        gid = layer["data"][y * m["width"] + x]
        if not gid:
            continue
        for first, count, name, rev in sets:
            if first <= gid < first + count:
                tname = rev.get(gid - first, "")
                if tname in MARKER_TILES.get(name, ()) or \
                        tname.startswith(MARKER_TILE_PREFIX.get(name, ("\0",))):
                    return f"tile {tname}"
    return None


def is_marker_sprite(sprite: str) -> bool:
    return sprite in MARKER_SPRITES or sprite.startswith(MARKER_PREFIX)


def touches(o: dict, x: int, y: int) -> bool:
    ox, oy, w, h = o["at"]["tx"], o["at"]["ty"], o["w"], o["h"]
    if not (ox <= x < ox + w):
        return False
    return oy <= y < oy + h or oy + h == y          # covers, or directly north


def object_marks(m: dict, warp: dict) -> str | None:
    x, y = warp["at"]["tx"], warp["at"]["ty"]
    wflag = warp.get("requires_flag")
    cands = [o for o in m.get("objects", [])
             if is_marker_sprite(o["sprite"]) and touches(o, x, y)]
    live = [o for o in cands if o.get("requires_flag") in (None, wflag)]
    for o in live:
        g = o.get("hidden_when_flag")
        if g is None:
            return f"object {o['sprite']} ({o['id']})"
        twin = [t for t in cands if t.get("requires_flag") == g and not t.get("hidden_when_flag")]
        if twin:
            return f"object {o['sprite']} ({o['id']}) -> {twin[0]['sprite']} on {g}"
    return None


def audit(only: str | None = None) -> int:
    fails = 0
    checked = 0
    for p in sorted(MAPS_DIR.glob("*.json")):
        m = json.loads(p.read_text())
        if only and m["id"] != only:
            continue
        W, H = m["width"], m["height"]
        for w in m.get("warps", []):
            x, y = w["at"]["tx"], w["at"]["ty"]
            if x in (0, W - 1) or y in (0, H - 1) or w.get("transition") == "door":
                continue
            checked += 1
            how = tile_marks(m, x, y) or object_marks(m, w)
            key = (m["id"], w["id"])
            if how:
                continue
            if key in ALLOW:
                print(f"ALLOW {m['id']}:{w['id']} ({x},{y}) — {ALLOW[key]}")
                continue
            fails += 1
            gate = w.get("requires_flag") or w.get("requires_ability") or "-"
            print(f"FAIL  {m['id']}:{w['id']} ({x},{y}) -> {w['to_map']} [gate {gate}] "
                  f"has no visible marker (tile or object)")
    print(f"\nwarp markers: {checked} mid-map warps checked, {fails} unmarked")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(audit(sys.argv[1] if len(sys.argv) > 1 else None))
