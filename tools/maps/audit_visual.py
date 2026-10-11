#!/usr/bin/env python3
"""audit_visual.py — measure the LOOK failures the other audits can't see.

audit_flow/warps/region prove a map PLAYS. This proves it doesn't read as the
"flat void + boxes" register the later regions slipped into (Saltreach Fen I,
Hushfrost Pass I), against the bar the South set (Tinderwick, Dimglass). Three
measurements, all from the shipped JSON + tileset sidecars:

  0. OBJECTS PER SCREEN — landmarks/props/buildings per 15x10 screen. The
     single best discriminator: the South's towns/routes carry 2-5, Saltreach
     Fen I carried 0.32. FAIL < 0.75, WARN < 1.5.
  1. BARE SQUARE (warn) — the largest square of tiles that are plain ground fill with
     no deco, no above-layer, no object, no NPC. A big one is a "flat void": the
     eye has nothing to read. (Screen is 15x10 tiles.)
  2. BOX POOLS — water bodies whose tiles fill their bounding box exactly (a
     ruler-drawn rectangle). Natural water is blob-shaped (level-design §11).
  3. SLABS — cliff/wall masses that are perfect rectangles, i.e. the "dropped
     slab" look (§11 rule 8); and BARE % — share of walkable-looking ground with
     nothing on it.

Calibrated 2026-10 against the shipped maps (South = the bar).

Usage: audit_visual.py [map_id ...] [--all] [--json] [--strict]
  --all     every town/route/hub map (interiors and caves are skipped —
            caves are judged by the cave rules, interiors by roomkit)
  --strict  exit 1 on any FAIL (for CI / finalize)
"""
import argparse, glob, json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public/assets/maps"
TILESETS = REPO / "public/assets/tilesets"

BARE_WARN = 7                        # largest bare square side, tiles (warn only)
POOL_MIN_AREA = 16                   # autotile corners round off smaller ponds; big boxes read ruled
OBJ_PER_SCREEN_WARN, OBJ_PER_SCREEN_FAIL = 1.5, 0.75   # landmarks/props per 15x10 screen
SLAB_MIN_AREA = 12
BARE_PCT_WARN = 0.55


def load_meta(m):
    """gid -> sidecar tile meta, across every tileset the map lists."""
    meta = {}
    for ts in m["tilesets"]:
        side = TILESETS / (ts["name"] + ".tileset.json")
        if not side.is_file():
            continue
        d = json.loads(side.read_text())
        for t in d["tiles"]:
            meta[ts["first_gid"] + t["index"]] = t
    return meta


def largest_square(mask, w, h):
    best, dp = 0, [[0] * (w + 1) for _ in range(h + 1)]
    for y in range(h):
        for x in range(w):
            if mask[y * w + x]:
                dp[y + 1][x + 1] = 1 + min(dp[y][x + 1], dp[y + 1][x], dp[y][x])
                best = max(best, dp[y + 1][x + 1])
    return best


def components(mask, w, h):
    seen, out = [False] * (w * h), []
    for i in range(w * h):
        if not mask[i] or seen[i]:
            continue
        stack, comp = [i], []
        seen[i] = True
        while stack:
            j = stack.pop(); comp.append(j)
            x, y = j % w, j // w
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                k = ny * w + nx
                if 0 <= nx < w and 0 <= ny < h and mask[k] and not seen[k]:
                    seen[k] = True; stack.append(k)
        out.append(comp)
    return out


def is_rect(comp, w):
    xs = [j % w for j in comp]; ys = [j // w for j in comp]
    bw, bh = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    return len(comp) == bw * bh and bw >= 2 and bh >= 2, (min(xs), min(ys), bw, bh)


def audit(map_id):
    m = json.loads((MAPS / f"{map_id}.json").read_text())
    w, h = m["width"], m["height"]
    meta = load_meta(m)
    layers = {l["name"]: l["data"] for l in m["layers"]}
    base = layers.get("base") or [0] * (w * h)
    deco = layers.get("deco") or [0] * (w * h)
    above = layers.get("above") or [0] * (w * h)
    covered = [False] * (w * h)
    for o in m.get("objects", []):
        at = o.get("at", {}); ox, oy = at.get("tx", 0), at.get("ty", 0)
        for yy in range(oy, oy + o.get("h", 1)):
            for xx in range(ox, ox + o.get("w", 1)):
                if 0 <= xx < w and 0 <= yy < h:
                    covered[yy * w + xx] = True
    for n in m.get("npcs", []):
        at = n.get("at") or n
        x, y = at.get("tx", at.get("x")), at.get("ty", at.get("y"))
        if isinstance(x, int) and isinstance(y, int) and 0 <= x < w and 0 <= y < h:
            covered[y * w + x] = True

    def role(i, layer=base):
        return meta.get(layer[i], {})

    ground = [False] * (w * h)
    bare = [False] * (w * h)
    water = [False] * (w * h)
    cliff_fill = [False] * (w * h)
    for i in range(w * h):
        t = role(i)
        r, auto = t.get("role"), t.get("autotile")
        terrain = t.get("terrain")
        if terrain == "water" or r == "water":
            water[i] = True
        if r == "cliff" and auto in (None, "fill"):
            cliff_fill[i] = True
        if r in ("ground", "sand", "path") and not t.get("collides"):
            ground[i] = True
            plain = auto in (None, "fill") and not t.get("encounter_terrain")
            if plain and not deco[i] and not above[i] and not covered[i]:
                bare[i] = True

    sq = largest_square(bare, w, h)
    pools = []
    for comp in components(water, w, h):
        ok, box = is_rect(comp, w)
        if ok and len(comp) >= POOL_MIN_AREA:
            pools.append(box)
    slabs = []
    for comp in components(cliff_fill, w, h):
        ok, box = is_rect(comp, w)
        if ok and len(comp) >= SLAB_MIN_AREA:
            slabs.append(box)
    gcount = sum(ground)
    bare_pct = (sum(bare) / gcount) if gcount else 0.0

    fails, warns = [], []
    if sq >= BARE_WARN:
        warns.append(f"large bare square {sq}x{sq} (warn >= {BARE_WARN})")
    ops = len(m.get("objects", [])) / max(1.0, (w * h) / 150.0)
    if ops < OBJ_PER_SCREEN_FAIL:
        fails.append(f"flat void: {ops:.2f} objects per screen (the South bar is 2-5; fail < "
                     f"{OBJ_PER_SCREEN_FAIL}) — add landmarks, props, buildings, crown trees, boulder clusters")
    elif ops < OBJ_PER_SCREEN_WARN:
        warns.append(f"sparse: {ops:.2f} objects per screen (warn < {OBJ_PER_SCREEN_WARN})")
    for (x, y, bw, bh) in pools:
        fails.append(f"box pool: water is a perfect {bw}x{bh} rectangle at ({x},{y}) — use mapkit.blob")
    for (x, y, bw, bh) in slabs:
        warns.append(f"slab: cliff fill is a perfect {bw}x{bh} rectangle at ({x},{y}) — boulder cluster "
                     f"or organic edge (level-design §11 r8)")
    if bare_pct >= BARE_PCT_WARN:
        warns.append(f"{bare_pct:.0%} of open ground is bare (warn >= {BARE_PCT_WARN:.0%})")
    return {"map": map_id, "kind": m.get("kind"), "objects_per_screen": round(ops, 2), "bare_square": sq, "bare_pct": round(bare_pct, 3),
            "box_pools": len(pools), "slabs": len(slabs), "fails": fails, "warns": warns}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("maps", nargs="*")
    p.add_argument("--all", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    a = p.parse_args()
    ids = a.maps
    if a.all or not ids:
        ids = sorted(Path(f).stem for f in glob.glob(str(MAPS / "*.json"))
                     if json.loads(Path(f).read_text()).get("kind") in ("town", "route", "hub"))
    res = [audit(i) for i in ids]
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        for r in res:
            tag = "FAIL" if r["fails"] else ("warn" if r["warns"] else "ok  ")
            print(f"{tag} {r['map']:<28} obj/screen {r['objects_per_screen']:>4}  bare-sq {r['bare_square']:>2}  bare {r['bare_pct']:.0%}  "
                  f"box-pools {r['box_pools']}  slabs {r['slabs']}")
            for f in r["fails"]:
                print("       FAIL", f)
            for wv in r["warns"]:
                print("       warn", wv)
        n = sum(1 for r in res if r["fails"])
        print(f"\n{len(res)} maps, {n} FAIL, {sum(1 for r in res if r['warns'] and not r['fails'])} warn-only")
    sys.exit(1 if a.strict and any(r["fails"] for r in res) else 0)


if __name__ == "__main__":
    main()
