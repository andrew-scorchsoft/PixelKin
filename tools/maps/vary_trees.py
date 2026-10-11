#!/usr/bin/env python3
"""
Re-skin the overworld's free-standing trees so one design isn't repeated 76 times.

Every `tinderwick_tree` placement (and any already-varied `tinderwick_tree_b/_c`)
in public/assets/maps/*.json gets its sprite picked deterministically from a hash
of (map id, tx, ty): ~50% the base tree, ~25% `tinderwick_tree_b` (round orchard
crown), ~25% `tinderwick_tree_c` (tall crown with a hung lantern). The three
masters share the exact 48x64 canvas, overhang 3 and trunk row, so ONLY the
`sprite` field changes: collision, warps and audits are untouched.

Idempotent: a re-run picks the same variant for the same tile. Placements owned
by a post-build script (tools/maps/worldcraft/*.py) are mirrored there with the
same `tree_variant()` pick, so `add_world_craft.py --check` stays at 0 drift.

    python3 tools/maps/vary_trees.py           # write
    python3 tools/maps/vary_trees.py --check   # exit 1 if any map would change
"""
from __future__ import annotations

import json
import sys
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public" / "assets" / "maps"
FAMILY = ("tinderwick_tree", "tinderwick_tree_b", "tinderwick_tree_c")


def tree_variant(map_id: str, tx: int, ty: int) -> str:
    h = zlib.crc32(f"{map_id}:{tx}:{ty}".encode()) % 4
    return FAMILY[0] if h < 2 else FAMILY[1] if h == 2 else FAMILY[2]


def main() -> int:
    check = "--check" in sys.argv
    changed = 0
    counts = {k: 0 for k in FAMILY}
    for path in sorted(MAPS.glob("*.json")):
        text = path.read_text()
        data = json.loads(text)
        hit = False
        for o in data.get("objects") or []:
            if o.get("sprite") not in FAMILY:
                continue
            want = tree_variant(path.stem, o["at"]["tx"], o["at"]["ty"])
            counts[want] += 1
            if o["sprite"] != want:
                o["sprite"] = want
                hit = True
        if hit:
            changed += 1
            if check:
                print(f"  drift {path.stem}")
            else:
                path.write_text(json.dumps(data, indent=2) + ("\n" if text.endswith("\n") else ""))
                print(f"  varied {path.stem}")
    print(f"  {sum(counts.values())} trees: " + ", ".join(f"{k}={v}" for k, v in counts.items())
          + f"; {changed} map(s) {'would change' if check else 'changed'}")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
