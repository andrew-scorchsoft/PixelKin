#!/usr/bin/env python3
"""Back-fill tree-mass NUB tiles into already-shipped maps.

The shared overworld set gained the protrusion roles the 13-slice family lacked —
`end_n/s/w/e`, `strip_h/v`, `single` (drawn by gbaforge.tree_nub) — so a thin tree
spur rounds on every exposed side instead of stamping a flat edge/fill stub. New
and rebuilt maps pick these up automatically through the autotiler
(tools/autotile/expand.mjs + blob.mjs). But shipped maps have their `terrain`
layer STRIPPED (mapkit.finalize bakes gids then drops it), so they can't simply be
re-expanded.

This tool re-derives the tree presence grid from each map's baked base layer,
re-runs the SAME blob classifier, and swaps in the nub gid ONLY where a cell now
classifies as a nub role (every other cell is left exactly as it was — no churn,
fully idempotent). Mirrors blob.mjs::classify; keep them in sync.

    ./venv/bin/python tools/maps/apply_tree_nubs.py            # patch all maps
    ./venv/bin/python tools/maps/apply_tree_nubs.py --dry-run  # report only
    ./venv/bin/python tools/maps/apply_tree_nubs.py tinderwick # one map (bare id)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public/assets/maps"
MANIFEST = REPO / "assets/tilesets/_shared/vesper_overworld/tileset.manifest.json"
NUB_ROLES = {"end_n", "end_s", "end_w", "end_e", "strip_h", "strip_v", "single"}


def classify(n, e, s, w, ne, se, sw, nw):
    """Role for one cell from its 8 same-terrain neighbours (mirror of blob.mjs)."""
    orth = n + e + s + w
    if orth == 4:
        if not nw:
            return "inner_nw"
        if not ne:
            return "inner_ne"
        if not se:
            return "inner_se"
        if not sw:
            return "inner_sw"
        return "fill"
    if orth == 3:
        if not n:
            return "edge_n"
        if not e:
            return "edge_e"
        if not s:
            return "edge_s"
        if not w:
            return "edge_w"
    if orth == 2:
        if not n and not w:
            return "corner_nw"
        if not n and not e:
            return "corner_ne"
        if not s and not e:
            return "corner_se"
        if not s and not w:
            return "corner_sw"
        if not n and not s:
            return "strip_h"
        if not e and not w:
            return "strip_v"
    if orth == 1:
        if s:
            return "end_n"
        if n:
            return "end_s"
        if e:
            return "end_w"
        if w:
            return "end_e"
    return "single"


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    ids = [a for a in argv if not a.startswith("--")]
    man = json.loads(MANIFEST.read_text())["tiles"]
    set_count = len(man)  # the overworld set's true tile count (grew when nubs landed)
    tree_idx = {i for i, t in enumerate(man) if t.get("terrain") == "tree"}
    role_idx = {t["autotile"]: i for i, t in enumerate(man)
                if t.get("terrain") == "tree" and t.get("autotile")}
    missing = NUB_ROLES - role_idx.keys()
    if missing:
        print(f"tileset lacks nub roles {sorted(missing)} — rebuild the set first")
        return 1

    paths = ([MAPS / f"{i}.json" for i in ids] if ids
             else sorted(MAPS.glob("*.json")))
    total = 0
    for mp in paths:
        m = json.loads(mp.read_text())
        ts = [t for t in m.get("tilesets", []) if "overworld" in t["name"]]
        if not ts:
            continue
        fg = ts[0]["first_gid"]
        # The engine resolves a gid by `first_gid <= gid < first_gid + tile_count`
        # (MapLoader), so a stale tile_count baked when the set was smaller would
        # leave the new nub gids unresolved (they'd render empty). Re-pin it to the
        # set's real count. Safe here: every overworld map uses a single tileset,
        # so widening the range can't collide with an accent set's first_gid.
        count_fixed = ts[0].get("tile_count") != set_count
        if count_fixed and not dry:
            ts[0]["tile_count"] = set_count
        base = next((l for l in m["layers"]
                     if l.get("role") == "base" or l["name"] == "base"), None)
        if not base:
            continue
        W, H, data = m["width"], m["height"], base["data"]

        def istree(x, y, oob=True):
            if not (0 <= x < W and 0 <= y < H):
                return oob  # 'continue' edge mode — off-map reads as same terrain
            g = data[y * W + x]
            return g > 0 and (g - fg) in tree_idx

        changes = 0
        roles: dict[str, int] = {}
        for y in range(H):
            for x in range(W):
                if not istree(x, y, False):
                    continue
                role = classify(
                    istree(x, y - 1), istree(x + 1, y), istree(x, y + 1), istree(x - 1, y),
                    istree(x + 1, y - 1), istree(x + 1, y + 1),
                    istree(x - 1, y + 1), istree(x - 1, y - 1))
                if role not in NUB_ROLES:
                    continue
                want = role_idx[role] + fg
                if data[y * W + x] != want:
                    if not dry:
                        data[y * W + x] = want
                    changes += 1
                    roles[role] = roles.get(role, 0) + 1
        if changes or count_fixed:
            total += changes
            note = f"{changes:3} cells {roles}" if changes else "  (tile_count only)"
            print(f"{mp.name:28} {note}")
            if not dry:
                # match the mapkit/expand writer (indent=2) so the diff is just
                # the handful of changed lines, not a reformat of the file.
                mp.write_text(json.dumps(m, indent=2) + "\n")
    verb = "would patch" if dry else "patched"
    print(f"{verb} {total} nub cell(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
