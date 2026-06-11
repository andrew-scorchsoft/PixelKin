#!/usr/bin/env python3
"""
Warp audit — the cross-map half of map validation.

validate_map.py judges ONE map (layers, meshing, borders). This audits the
CONNECTIONS, which only exist between maps:

  COVERAGE    A wide entrance warps on EVERY walkable tile of its opening — a
              2-3 tile gap with one warp strands the player on the silent tiles.
              (Each map-edge run of unconditionally-walkable border tiles must
              be all-warp or no-warp; no-warp runs are reported as validate_map
              already warns of them.)
  LANDING     Every warp's target map exists (else INFO: an inert tease, which
              the engine no-ops), the landing tile is in bounds and walkable
              (ability-gated counts as walkable — you could only have arrived
              holding the gift), and it isn't a step_on warp to a THIRD map.
  ROUND TRIP  Within 1 tile of the landing there is a warp leading back to the
              source map — you can always go back the way you came. Landing ON
              the return warp is the preferred classic pattern (the engine does
              not auto-fire step_on warps on arrival; enterMap places, it does
              not step).

Run:  ./venv/bin/python tools/maps/audit_warps.py            # whole world
      ./venv/bin/python tools/maps/audit_warps.py <map_id>   # findings touching one map
Exit code 1 if any FAIL.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS_DIR = REPO / "public/assets/maps"
TILESETS_DIR = REPO / "public/assets/tilesets"


def load_world() -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text()) for p in sorted(MAPS_DIR.glob("*.json"))}


class Walkability:
    """Per-map walkable grid from tile collision + object footprints.
    walkable=True; gated tiles (requires_ability) are walkable-with-gift."""

    def __init__(self, m: dict):
        self.w, self.h = m["width"], m["height"]
        solid = [False] * (self.w * self.h)
        gated = [False] * (self.w * self.h)

        # gid -> (collides, requires_ability) across the map's tilesets
        sets = []
        for ts in m.get("tilesets", []):
            side = TILESETS_DIR / f"{ts['name']}.tileset.json"
            if not side.is_file():
                continue
            data = json.loads(side.read_text())
            tiles = {t.get("index", i): t for i, t in enumerate(data.get("tiles", []))}
            sets.append((ts.get("first_gid", 1), data.get("tile_count", len(tiles)), tiles))
        sets.sort(key=lambda s: -s[0])

        def tile_meta(gid: int):
            for first, count, tiles in sets:
                if gid >= first:
                    return tiles.get(gid - first, {})
            return {}

        for layer in m.get("layers", []):
            if layer.get("role") == "above":
                continue
            for i, gid in enumerate(layer.get("data", [])):
                if not gid:
                    continue
                meta = tile_meta(gid)
                if meta.get("collides"):
                    if meta.get("requires_ability"):
                        gated[i] = True
                    else:
                        solid[i] = True
                elif meta.get("role") == "floor":
                    # a floor tile (dock board) over a gated surface stays gated
                    # (CollisionGrid keys on the surface gid) — leave as-is
                    pass

        for o in m.get("objects", []):
            if o.get("solid") is False:
                continue
            top = o["at"]["ty"] + (o.get("overhang", 0) if o.get("walk_under") else 0)
            for ty in range(top, o["at"]["ty"] + o["h"]):
                for tx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
                    if 0 <= tx < self.w and 0 <= ty < self.h:
                        solid[ty * self.w + tx] = True

        # Doorways are walk-onto: a transition:'door' warp frees its tile (mirror
        # of CollisionGrid) so a door inside a building footprint reads walkable.
        for wp in m.get("warps", []):
            if wp.get("transition") == "door":
                at = wp["at"]
                if 0 <= at["tx"] < self.w and 0 <= at["ty"] < self.h:
                    solid[at["ty"] * self.w + at["tx"]] = False

        # AbilityGates flip their rect's tiles to gated-walkable
        for g in m.get("gates", []):
            if g.get("effect") in ("make_passable", "remove_tile") and "rect" in g:
                r = g["rect"]
                for ty in range(r["ty"], r["ty"] + r["h"]):
                    for tx in range(r["tx"], r["tx"] + r["w"]):
                        if 0 <= tx < self.w and 0 <= ty < self.h:
                            i = ty * self.w + tx
                            solid[i] = False
                            gated[i] = True
        self.solid, self.gated = solid, gated

    def in_bounds(self, tx, ty):
        return 0 <= tx < self.w and 0 <= ty < self.h

    def open_tile(self, tx, ty):
        """Unconditionally walkable."""
        i = ty * self.w + tx
        return self.in_bounds(tx, ty) and not self.solid[i] and not self.gated[i]

    def walkable_any(self, tx, ty):
        """Walkable, possibly behind an ability gate."""
        return self.in_bounds(tx, ty) and not self.solid[ty * self.w + tx]


def audit(world: dict[str, dict], focus: str | None = None):
    walk = {mid: Walkability(m) for mid, m in world.items()}
    fails, warns, infos = [], [], []

    def rec(level, source, msg):
        if focus and focus not in msg and source != focus:
            return
        (fails if level == "FAIL" else warns if level == "WARN" else infos).append(
            f"  [{level[0] if level != 'FAIL' else '✗'}] {source}: {msg}")

    for mid, m in world.items():
        wk = walk[mid]
        warps = m.get("warps", [])
        step_at = {(w["at"]["tx"], w["at"]["ty"]): w for w in warps if w.get("trigger") == "step_on"}

        # ---- DOOR CONVENTION: doors are WALK-ONTO (step_on) ----
        # The player just walks into the doorway tile (which the engine frees in
        # collision); pressing Confirm at it also works, and a locked door answers
        # with its blocked_ref. A door left on 'interact' breaks the convention.
        for w in warps:
            if w.get("transition") == "door" and w.get("trigger") != "step_on":
                rec("FAIL", mid, f"door warp '{w['id']}' is '{w.get('trigger')}' — "
                    f"doors are walk-onto (step_on) by convention (level-design §11 r5b)")

        # ---- COVERAGE: edge runs of open tiles must be all-warp or no-warp ----
        edges = [("N", [(x, 0) for x in range(wk.w)]), ("S", [(x, wk.h - 1) for x in range(wk.w)]),
                 ("W", [(0, y) for y in range(wk.h)]), ("E", [(wk.w - 1, y) for y in range(wk.h)])]
        for name, cells in edges:
            run = []
            for (tx, ty) in cells + [(-9, -9)]:
                if wk.open_tile(tx, ty):
                    run.append((tx, ty))
                    continue
                if run:
                    warped = [c for c in run if c in step_at]
                    if warped and len(warped) < len(run):
                        missing = [c for c in run if c not in step_at]
                        rec("FAIL", mid, f"{name} edge opening {run[0]}–{run[-1]} is "
                            f"{len(run)} tiles wide but only {len(warped)} have warps "
                            f"(missing {missing}) — wide entrances warp on every tile")
                    elif not warped:
                        rec("WARN", mid, f"{name} edge has a warp-less open run "
                            f"{run[0]}–{run[-1]} (validate_map border warning)")
                run = []

        # ---- LANDING + ROUND TRIP ----
        for w in warps:
            wid, to_map = w["id"], w["to_map"]
            if to_map not in world:
                rec("INFO", mid, f"warp '{wid}' -> '{to_map}' (unauthored — inert tease)")
                continue
            twk = walk[to_map]
            land = (w["to"]["tx"], w["to"]["ty"])
            if not twk.in_bounds(*land):
                rec("FAIL", mid, f"warp '{wid}' lands OUT OF BOUNDS at {land} on '{to_map}'")
                continue
            if not twk.walkable_any(*land):
                rec("FAIL", mid, f"warp '{wid}' lands on a SOLID tile {land} on '{to_map}'")
            tsteps = {(x["at"]["tx"], x["at"]["ty"]): x for x in world[to_map].get("warps", [])
                      if x.get("trigger") == "step_on"}
            on = tsteps.get(land)
            if on and on["to_map"] not in (mid, to_map):
                rec("WARN", mid, f"warp '{wid}' lands ON warp '{on['id']}' -> "
                    f"'{on['to_map']}' (a third map) at {land} on '{to_map}'")
            back = [x for x in world[to_map].get("warps", []) if x["to_map"] == mid
                    and abs(x["at"]["tx"] - land[0]) <= 1 and abs(x["at"]["ty"] - land[1]) <= 1]
            if not back:
                rec("FAIL", mid, f"warp '{wid}' -> '{to_map}' {land} has NO return warp "
                    f"to '{mid}' within 1 tile of the landing")

    return fails, warns, infos


def main():
    focus = sys.argv[1] if len(sys.argv) > 1 else None
    world = load_world()
    fails, warns, infos = audit(world, focus)
    print(f"Warp audit — {len(world)} maps" + (f" (focus: {focus})" if focus else ""))
    for line in fails + warns + infos:
        print(line)
    print(f"{'FAIL' if fails else 'PASS'} — {len(fails)} failure(s), "
          f"{len(warns)} warning(s), {len(infos)} tease(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
