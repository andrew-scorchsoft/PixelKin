#!/usr/bin/env python3
"""
Validate a built map against the PixelKin quality standard (the Pokémon-era bar).

`render_map.py` lets you SEE a map; this MEASURES it, so "meets the standard" is a
gate, not an opinion. It reads the map JSON + its packed tileset sidecars and
checks the structural things that separate a polished handheld map from a bag of
isolated fills (docs/world/level-design.md, docs/art-style.md §11–§15):

  1. Layer discipline      base + deco + above present and used.
  2. Autotile vocabulary   the tilesets actually provide terrain/edge tiles.
  3. Meshing (the big one) terrain regions use edge/corner tiles at their
                           boundaries — not raw fill butting a foreign terrain
                           (the "tiles stand in isolation" problem).
  4. Water shorelines      water never meets land on a raw fill tile.
  5. Decoration density     the map isn't an empty field.
  6. Tree depth            tree bases have an above-layer canopy (walk-under).
  7. Solid border          non-warp map edges don't show the void.

Exit non-zero if any FAIL (use as a CI/authoring gate). Usage:
  validate_map.py public/assets/maps/tinderwick.json
  validate_map.py tinderwick            # bare id under public/assets/maps/
  validate_map.py <map> --json          # machine-readable report
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EDGE_ROLES = {"edge_n", "edge_e", "edge_s", "edge_w",
              "corner_nw", "corner_ne", "corner_se", "corner_sw",
              "inner_nw", "inner_ne", "inner_se", "inner_sw",
              "strip_h", "strip_v", "end_n", "end_e", "end_s", "end_w", "single"}


def find_repo_root(start: Path) -> Path:
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return start


def resolve_map(arg: str, repo: Path) -> Path:
    p = Path(arg)
    if p.is_file():
        return p
    cand = repo / "public" / "assets" / "maps" / f"{arg}.json"
    if cand.is_file():
        return cand
    raise SystemExit(f"Map not found: {arg}")


class Report:
    def __init__(self) -> None:
        self.checks: list[dict] = []

    def add(self, name: str, status: str, detail: str) -> None:
        self.checks.append({"check": name, "status": status, "detail": detail})

    @property
    def failed(self) -> bool:
        return any(c["status"] == "FAIL" for c in self.checks)


def main() -> int:
    p = argparse.ArgumentParser(description="Validate a map against the quality standard.")
    p.add_argument("map")
    p.add_argument("--json", action="store_true", help="Emit the report as JSON.")
    args = p.parse_args()

    repo = find_repo_root(Path.cwd().resolve())
    map_path = resolve_map(args.map, repo)
    m = json.loads(map_path.read_text())
    W, H = m["width"], m["height"]

    # Load sidecars -> per-gid (role, terrain, autotile, collides).
    gid_meta: dict[int, dict] = {}
    for ref in m["tilesets"]:
        side = (map_path.parents[2] / "tilesets" / f"{ref['name']}.tileset.json")
        if not side.is_file():
            side = repo / "public" / "assets" / "tilesets" / f"{ref['name']}.tileset.json"
        tiles = json.loads(side.read_text()).get("tiles", []) if side.is_file() else []
        by_index = {t["index"]: t for t in tiles}
        for local in range(ref["tile_count"]):
            gid_meta[ref["first_gid"] + local] = by_index.get(local, {})

    layers = {ly["name"]: ly for ly in m.get("layers", [])}
    by_role: dict[str, list] = {}
    for ly in m.get("layers", []):
        by_role.setdefault(ly.get("role", ly["name"]), []).append(ly)
    rep = Report()

    def meta(gid: int) -> dict:
        return gid_meta.get(gid, {})

    # --- 1. Layer discipline ---
    objs = m.get("objects", [])
    overhang_objs = any(o.get("overhang", 0) > 0 for o in objs)
    have = {r: (r in by_role and any(any(g > 0 for g in l["data"]) for l in by_role[r]))
            for r in ("base", "deco", "above")}
    if not have["base"]:
        rep.add("layers", "FAIL", "no populated 'base' layer")
    elif not have["deco"] and not objs:
        rep.add("layers", "WARN", "no decoration layer or objects — map will read as empty/flat")
    elif not have["above"] and not overhang_objs:
        rep.add("layers", "WARN", "no walk-under depth (no 'above' layer and no overhanging objects)")
    else:
        depth = "above layer" if have["above"] else "object overhangs"
        rep.add("layers", "PASS", f"base + deco + {depth} (walk-under depth) present")

    base = by_role.get("base", [{}])[0].get("data")

    # --- 2. Autotile vocabulary in the tilesets ---
    terrains = {meta(g).get("terrain") for g in gid_meta if meta(g).get("terrain")}
    have_edges = any(meta(g).get("autotile") in EDGE_ROLES for g in gid_meta)
    if not terrains:
        rep.add("autotile-vocab", "FAIL",
                "no tiles tagged with a `terrain` group — the tilesets provide no "
                "edge/corner autotile vocabulary (level-design Fork F). Maps built on "
                "this kit can only be blocky fills.")
    elif not have_edges:
        rep.add("autotile-vocab", "FAIL",
                f"terrains {sorted(terrains)} exist but NO edge/corner tiles (autotile "
                f"roles) are tagged — boundaries can't mesh.")
    else:
        rep.add("autotile-vocab", "PASS",
                f"terrains {sorted(terrains)} with edge/corner pieces present")

    # --- 3 & 4. Meshing: terrain boundaries must use edge tiles ---
    if base and terrains:
        def terr(x: int, y: int):
            if 0 <= x < W and 0 <= y < H:
                return meta(base[y * W + x]).get("terrain")
            return "__edge__"  # off-map = continuation (matches the autotiler), not a boundary
        raw_boundary = 0
        boundary_total = 0
        water_raw = 0
        for y in range(H):
            for x in range(W):
                g = base[y * W + x]
                t = meta(g).get("terrain")
                if not t:
                    continue
                if meta(g).get("encounter_terrain") == "tall_grass":
                    continue  # tall-grass is a flat encounter patch, not a bordered surface
                neigh = [terr(x, y - 1), terr(x + 1, y), terr(x, y + 1), terr(x - 1, y)]
                # off-map (__edge__) is continuation, not a boundary
                if any(nb != t and nb != "__edge__" for nb in neigh):
                    boundary_total += 1
                    role = meta(g).get("autotile")
                    if role not in EDGE_ROLES:  # boundary cell drawn with a non-edge tile
                        raw_boundary += 1
                        if t == "water":
                            water_raw += 1
        if boundary_total == 0:
            rep.add("meshing", "WARN", "no terrain boundaries found to check")
        else:
            pct = 100 * raw_boundary / boundary_total
            status = "PASS" if pct < 5 else ("WARN" if pct < 25 else "FAIL")
            rep.add("meshing", status,
                    f"{raw_boundary}/{boundary_total} ({pct:.0f}%) terrain-boundary cells "
                    f"use a RAW fill tile instead of an edge/corner tile")
            if water_raw:
                rep.add("water-shoreline", "FAIL",
                        f"{water_raw} water cells meet land without a shoreline edge tile")
    elif base:
        rep.add("meshing", "FAIL",
                "cannot check meshing — no terrain tags on the tiles this map uses")

    # --- 5. Decoration density ---
    if base:
        walkable = sum(1 for g in base if g > 0 and not meta(g).get("collides"))
        deco_cells = 0
        for ly in by_role.get("deco", []):
            deco_cells += sum(1 for g in ly["data"] if g > 0)
        # whole-structure objects (buildings/trees/lamps) also fill the scene
        obj_cells = sum(o.get("w", 0) * o.get("h", 0) for o in objs)
        filled = deco_cells + obj_cells
        ratio = filled / max(1, walkable)
        status = "PASS" if ratio >= 0.06 else "WARN"
        rep.add("decoration", status,
                f"deco props + objects cover {ratio*100:.0f}% of walkable ground "
                f"({deco_cells} props + {obj_cells} object tiles / {walkable} walkable)")

    # --- 6. Tree depth (base on deco, canopy on above) ---
    tree_bases = sum(1 for ly in by_role.get("deco", [])
                     for g in ly["data"] if meta(g).get("role") == "tree")
    above_cells = sum(1 for ly in by_role.get("above", []) for g in ly["data"] if g > 0)
    if tree_bases and not above_cells:
        rep.add("tree-depth", "WARN",
                f"{tree_bases} tree/tall tiles but the 'above' layer is empty — "
                f"no walk-under canopies (flat trees)")
    elif tree_bases:
        rep.add("tree-depth", "PASS", "tall objects use the above layer")

    # --- 6b. Variation: no long stamped run of one terrain tile (the repeat tell) ---
    if base:
        # Only EDGE/CORNER tiles should vary along a boundary — a uniform fill interior
        # (deep sea, big sand flat) is legitimately repetitive (and water animates), so
        # restrict the run check to autotile edge roles: that's the stamped-shoreline /
        # corduroy-tree-line tell, not flat ground.
        def longest_run(line: list[int]) -> int:
            best = run = 0
            for i in range(1, len(line)):
                g = line[i]
                is_edge = meta(g).get("autotile") in EDGE_ROLES
                same = g == line[i - 1] and g > 0 and is_edge
                run = run + 1 if same else 0
                best = max(best, run)
            return best + 1 if best else 0
        worst = 0
        for y in range(H):
            worst = max(worst, longest_run([base[y * W + x] for x in range(W)]))
        for x in range(W):
            worst = max(worst, longest_run([base[y * W + x] for y in range(H)]))
        limit = max(12, int(0.6 * max(W, H)))
        if worst > limit:
            rep.add("variation", "WARN",
                    f"a terrain tile repeats identically for {worst} cells in a row "
                    f"(>{limit}) — add edge/fill VARIANTS so it doesn't read as stamped")
        else:
            rep.add("variation", "PASS",
                    f"no terrain tile runs longer than {worst} identical cells (variants scatter)")

    # --- 7. Solid border on non-warp edges ---
    if base:
        warp_tiles = {(w["at"]["tx"], w["at"]["ty"]) for w in m.get("warps", [])}
        open_edge = 0
        for x in range(W):
            for y in (0, H - 1):
                g = base[y * W + x]
                if (g == 0 or not meta(g).get("collides")) and (x, y) not in warp_tiles:
                    open_edge += 1
        for y in range(H):
            for x in (0, W - 1):
                g = base[y * W + x]
                if (g == 0 or not meta(g).get("collides")) and (x, y) not in warp_tiles:
                    open_edge += 1
        rep.add("border", "PASS" if open_edge == 0 else "WARN",
                f"{open_edge} non-warp edge tiles are passable/empty (camera may show void)")

    # --- output ---
    if args.json:
        print(json.dumps({"map": str(map_path), "checks": rep.checks,
                          "passed": not rep.failed}, indent=2))
    else:
        print(f"Map quality report — {map_path.name}\n")
        icon = {"PASS": "✓", "WARN": "!", "FAIL": "✗"}
        for c in rep.checks:
            print(f"  [{icon[c['status']]}] {c['check']:<16} {c['detail']}")
        n_fail = sum(c["status"] == "FAIL" for c in rep.checks)
        n_warn = sum(c["status"] == "WARN" for c in rep.checks)
        print(f"\n{'FAIL' if rep.failed else 'PASS'} — {n_fail} failure(s), {n_warn} warning(s)")
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())
