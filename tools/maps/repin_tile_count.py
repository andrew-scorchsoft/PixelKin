#!/usr/bin/env python3
"""Re-pin the shared overworld set's baked `tile_count` in every consuming map.

Every map bakes a `tile_count` into its `vesper_overworld_set` tileset ref, and
the engine (MapLoader) resolves a gid only when
`first_gid <= gid < first_gid + tile_count` — so after the shared set GROWS
(tiles are always APPENDED, never inserted), a stale count leaves the new gids
unresolved and they render empty (this bit the tree nubs). This generalises the
re-pin loop that lived in apply_tree_nubs.py: it walks every map JSON under
public/assets/maps/, finds the shared-set ref, and pins its `tile_count` to the
manifest's true count. Safe by construction: every overworld map uses the shared
set as its single (or lowest) tileset, and widening the range is collision-free
as long as no accent set's first_gid falls inside it — which this tool VERIFIES
before writing (it fails loudly rather than shadowing an accent set).

    ./venv/bin/python tools/maps/repin_tile_count.py            # re-pin all maps
    ./venv/bin/python tools/maps/repin_tile_count.py --dry-run  # report only
    ./venv/bin/python tools/maps/repin_tile_count.py tinderwick # one map (bare id)

Run it after EVERY rebuild of the shared set that appended tiles.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public/assets/maps"
MANIFEST = REPO / "assets/tilesets/_shared/vesper_overworld/tileset.manifest.json"


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    ids = [a for a in argv if not a.startswith("--")]
    man = json.loads(MANIFEST.read_text())
    set_name = man["name"]
    set_count = len(man["tiles"])

    paths = ([MAPS / f"{i}.json" for i in ids] if ids
             else sorted(MAPS.glob("*.json")))
    pinned = skipped = 0
    for mp in paths:
        m = json.loads(mp.read_text())
        refs = m.get("tilesets", [])
        ts = next((t for t in refs if t["name"] == set_name), None)
        if ts is None:
            continue
        # collision check: widening must not swallow another set's gid range.
        clash = [t["name"] for t in refs if t is not ts
                 and ts["first_gid"] <= t["first_gid"] < ts["first_gid"] + set_count]
        if clash:
            print(f"{mp.name:28} FAIL: widening {set_name} to {set_count} would "
                  f"shadow accent set(s) {clash} — re-stack their first_gid first")
            return 1
        old = ts.get("tile_count")
        if old == set_count:
            skipped += 1
            continue
        if not dry:
            ts["tile_count"] = set_count
            # match the mapkit/expand writer (indent=2): the diff stays one line.
            mp.write_text(json.dumps(m, indent=2) + "\n")
        pinned += 1
        print(f"{mp.name:28} tile_count {old} -> {set_count}")
    verb = "would re-pin" if dry else "re-pinned"
    print(f"{verb} {pinned} map(s); {skipped} already current ({set_name} = {set_count} tiles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
