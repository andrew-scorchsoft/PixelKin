#!/usr/bin/env python3
"""
traversal_reach — the Python half of the traversal-kit parity gate.

For every map that uses the kit (flows/spans/jumps) — plus the synthetic fixture
check_traversal.mjs passes on stdin — print JSON: the map's base walkable grid
(standable with every Gift, decks excluded so the JS side sees raw ground), its
NPC bodies, its starts (warp landings + walkable warp tiles) and the tiles the
worldmodel's BFS reaches from them. check_traversal.mjs re-walks the same grid
with the ENGINE's Traversal.ts and FAILs on any difference.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from worldmodel import MapModel, load_world  # noqa: E402

GIFTS = {"tidecall", "glimmerstep", "updraft_kite", "emberward", "sunsketch", "starreach"}


def dump(m: dict) -> dict:
    mm = MapModel(m)
    ground = [[mm._ground_open(x, y, GIFTS, None) for x in range(mm.w)] for y in range(mm.h)]
    starts = []
    for w in m.get("warps", []):
        at = (w["at"]["tx"], w["at"]["ty"])
        if mm.standable(*at, abilities=GIFTS):
            starts.append(at)
    for s in m.get("_starts", []):
        starts.append(tuple(s))
    starts = sorted(set(starts))
    reach = sorted(mm.bfs(starts, abilities=GIFTS, npc_block=mm.static_npc_tiles))
    return {"id": m["id"], "w": mm.w, "h": mm.h, "ground": ground,
            "npcs": sorted(mm.static_npc_tiles), "starts": starts, "reach": reach,
            "flows": m.get("flows", []), "spans": m.get("spans", []),
            "jumps": m.get("jumps", []), "ride": bool(m.get("ride"))}


def main() -> int:
    out = []
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            for m in json.loads(raw):
                out.append(dump(m))
    for mid, m in load_world().items():
        if m.get("flows") or m.get("spans") or m.get("jumps"):
            out.append(dump(m))
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
