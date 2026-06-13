#!/usr/bin/env python3
"""
render_walkable — see what the COLLISION model thinks is walkable, over the art.

`render_map.py` draws a map's *art*; the flow/region audits compute reachability
but (a) grant every Lantern Gift, so they can't see a tile that's blocked at the
stage you reach it, and (b) trust a flag-gated warp to "open later" without
checking the flag actually makes its tile walkable. That blind spot let a real
softlock ship (Pearlmoor's breakwater causeway is a water-island reachable only
with Tidecall — but the Tide Gift is earned by ringing the bell ON it).

This tool closes the loop. It composites the SAME collision model the engine uses
(via worldmodel.MapModel — base+deco tile meta, object footprints, freed door
tiles, ability-gate rects; `above` layers never collide) on top of the rendered
art, and floods reachability from the map's real entrances. The overlay shows, per
tile: solid / ledge / ability-gated(by gift) / reachable-on-foot / reachable-only-
with-a-gift / ORPHAN (cut off even with every gift). It also prints a report and
flags two bug classes the older audits miss:

  * orphan      — a walkable pocket unreachable even holding all six Gifts
                  (cut off from every entrance: usually a tile/placement error).
  * softlock    — a warp gated by a FLAG with no ability requirement whose tile
                  you can only reach by USING a Gift. The quest opens the door,
                  but you physically need a Gift the quest never grants.

Usage:
  render_walkable.py pearlmoor_quay                 # overlay -> docs/maps/walkable/<id>.webp + report
  render_walkable.py pearlmoor_quay --scale 6
  render_walkable.py --all                          # every map: overlays + an aggregate report
  render_walkable.py --all --report-only            # just the report (no PNGs), CI-friendly
  render_walkable.py <id> --report-only

Exit code is non-zero if any softlock or orphan is found (so --all doubles as a gate).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from worldmodel import ALL_ABILITIES, MapModel, load_world, parse_graph  # noqa: E402

# An orphan pocket this size or larger is a genuine cut-off area (a likely bug);
# smaller ones are almost always decorative gaps behind the border treeline and
# are reported as "minor" (they don't fail the pass).
MAJOR_ORPHAN = 4

REPO = Path(__file__).resolve().parents[2]
MAPS_DIR = REPO / "public/assets/maps"
OUT_DIR = REPO / "docs/maps/walkable"
RENDER_MAP = REPO / ".claude/skills/generate-sprite-sheet/scripts/render_map.py"

# Gift -> the colour its gate paints (so you can read WHICH Gift a tile waits on).
ABILITY_TINT = {
    "tidecall": (60, 170, 255),     # water — blue
    "glimmerstep": (120, 230, 150),  # deepwood — green
    "updraft_kite": (180, 200, 255),  # sky — pale blue
    "emberward": (255, 150, 90),     # coldfog — ember
    "sunsketch": (255, 215, 90),     # sun-vine — gold
    "starreach": (200, 150, 255),    # void — violet
}
ABILITY_LETTER = {a: a[0].upper() for a in ALL_ABILITIES}


# --------------------------------------------------------------------------- #
# Reachability analysis (entrance-faithful; the engine-model lives in worldmodel)
# --------------------------------------------------------------------------- #
def inbound_landings(world: dict[str, dict], map_id: str,
                     start: dict | None = None) -> set[tuple[int, int]]:
    """Tiles the player MATERIALISES on when entering this map: the `to` target of
    every warp (in any map) that points here, plus the world start if applicable."""
    out: set[tuple[int, int]] = set()
    for m in world.values():
        for w in m.get("warps", []):
            if w.get("to_map") == map_id and w.get("to"):
                out.add((w["to"]["tx"], w["to"]["ty"]))
    if start and start.get("start_map") == map_id and start.get("start_at"):
        out.add((start["start_at"]["tx"], start["start_at"]["ty"]))
    return out


def clusters(tiles: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    """Group tiles into 4-adjacent pockets (for orphan severity)."""
    seen: set[tuple[int, int]] = set()
    out: list[set[tuple[int, int]]] = []
    for t in tiles:
        if t in seen:
            continue
        comp = {t}
        seen.add(t)
        q = deque([t])
        while q:
            cx, cy = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (cx + dx, cy + dy)
                if n in tiles and n not in seen:
                    seen.add(n)
                    comp.add(n)
                    q.append(n)
        out.append(comp)
    return out


def foot_components(model: MapModel) -> list[set[tuple[int, int]]]:
    """Connected pockets of on-foot-walkable tiles (undirected 4-adjacency).
    Ability-gated tiles are NOT walkable on foot, so they separate pockets —
    which is the whole point: each pocket is a place you can stand without a Gift."""
    seen: set[tuple[int, int]] = set()
    comps: list[set[tuple[int, int]]] = []
    for y in range(model.h):
        for x in range(model.w):
            if (x, y) in seen or not model.standable(x, y, abilities=set()):
                continue
            comp: set[tuple[int, int]] = set()
            q = deque([(x, y)])
            seen.add((x, y))
            while q:
                cx, cy = q.popleft()
                comp.add((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (cx + dx, cy + dy)
                    if n not in seen and model.standable(*n, abilities=set()):
                        seen.add(n)
                        q.append(n)
            comps.append(comp)
    return comps


def analyse(world: dict[str, dict], model: MapModel, start: dict | None = None) -> dict:
    """Reachability picture for one map. All flood/reach checks pass THROUGH NPCs
    (a static body is geometry, not a wall) to match the audits' reach semantics."""
    all_ab = set(ALL_ABILITIES)
    landings = inbound_landings(world, model.id, start)

    comps = foot_components(model)
    # The on-foot PLAY BODY: the largest pocket an entrance lands in (falls back to
    # the largest pocket). Anchoring the softlock check here — not on every landing —
    # is what stops a trap's own return-landing from masking the trap.
    landed = [c for c in comps if c & landings]
    main = max(landed, key=len) if landed else (max(comps, key=len) if comps else set())

    # ORPHANS use the TRUE entrances: every inbound landing (a map crossed THROUGH a
    # cave re-enters on a far shelf), flooded holding all Gifts. A tile walkable with
    # every Gift yet unreachable from any entrance is genuinely cut off.
    reach_all = set(model.bfs(list(landings) or list(main), abilities=all_ab))
    walkable_all = {
        (x, y)
        for y in range(model.h)
        for x in range(model.w)
        if model.standable(x, y, abilities=all_ab)
    }
    orphans = walkable_all - reach_all
    orphan_clusters = clusters(orphans)
    major_orphans = [c for c in orphan_clusters if len(c) >= MAJOR_ORPHAN]

    # SOFTLOCKS: a warp gated by a flag (no ability) whose stand tile you can only
    # reach by USING a Gift. Opening the flag won't make the water/void walkable.
    softlocks = []
    for wp in model.warps:
        if wp.get("requires_ability"):
            continue  # honestly ability-gated; not a softlock
        if not wp.get("requires_flag"):
            continue  # ungated foot exit — the old audits already cover these
        at = (wp["at"]["tx"], wp["at"]["ty"])
        if at in main:
            continue  # reachable on foot from the play body — fine
        # Which Gift (if any) would let you reach it from the play body? (i.e. it's
        # gated content the quest flag can't open.) None -> also fully cut off.
        gift = next((ab for ab in ALL_ABILITIES
                     if at in set(model.bfs(list(main), abilities={ab}))), None)
        softlocks.append({
            "warp": wp["id"], "to": wp.get("to_map"), "at": at,
            "flag": wp.get("requires_flag"), "needs_gift": gift,
        })

    return {
        "map": model.id, "kind": model.kind,
        "components": len(comps), "main_size": len(main),
        "main": main, "reach_all": reach_all, "walkable_all": walkable_all,
        "orphans": orphans, "orphan_clusters": orphan_clusters,
        "major_orphans": major_orphans, "softlocks": softlocks, "landings": landings,
    }


# --------------------------------------------------------------------------- #
# Overlay rendering
# --------------------------------------------------------------------------- #
def render_overlay(model: MapModel, info: dict, scale: int, out_path: Path) -> None:
    art_tmp = Path("/tmp") / f"_walk_art_{model.id}.png"
    subprocess.run(
        [sys.executable, str(RENDER_MAP), model.id,
         "--output", str(art_tmp), "--scale", str(scale)],
        check=True, capture_output=True,
    )
    base = Image.open(art_tmp).convert("RGBA")
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ts = 16 * scale

    main, reach_all, orphans = info["main"], info["reach_all"], info["orphans"]
    warp_tiles = {(w["at"]["tx"], w["at"]["ty"]): w for w in model.warps}
    softlock_tiles = {tuple(s["at"]) for s in info["softlocks"]}

    def cell(x, y):
        return (x * ts, y * ts, x * ts + ts, y * ts + ts)

    for y in range(model.h):
        for x in range(model.w):
            i = y * model.w + x
            box = cell(x, y)
            gated = model.ability[i]
            if model.solid[i] and not model.ledge[i]:
                d.rectangle(box, fill=(220, 40, 40, 90))            # solid — red
            elif model.ledge[i]:
                d.rectangle(box, fill=(255, 140, 0, 95))            # ledge — orange
            elif gated:
                r, g, b = ABILITY_TINT.get(gated, (160, 160, 160))
                d.rectangle(box, fill=(r, g, b, 70))                # gift-gated tile
                d.text((box[0] + 3, box[1] + 1), ABILITY_LETTER.get(gated, "?"),
                       fill=(255, 255, 255, 220))
            elif (x, y) in orphans:
                d.rectangle(box, fill=(255, 0, 220, 150))           # ORPHAN — magenta
            elif (x, y) in main:
                d.rectangle(box, fill=(60, 200, 90, 55))            # walk on foot — green
            elif (x, y) in reach_all:
                d.rectangle(box, fill=(240, 220, 60, 75))           # only via a Gift — yellow
            # else: void/unreachable non-walkable — leave art bare

    # static NPC bodies (deliberate geometry)
    for (nx, ny) in info.get("static_npcs", set()):
        cx, cy = nx * ts + ts // 2, ny * ts + ts // 2
        d.ellipse((cx - ts // 5, cy - ts // 5, cx + ts // 5, cy + ts // 5),
                  fill=(170, 90, 220, 230))

    # warps: blue box, RED if softlocked
    for (wx, wy), w in warp_tiles.items():
        box = cell(wx, wy)
        col = (255, 30, 30, 255) if (wx, wy) in softlock_tiles else (80, 160, 255, 255)
        d.rectangle((box[0] + 1, box[1] + 1, box[2] - 2, box[3] - 2),
                    outline=col, width=max(2, scale // 2))

    out = Image.alpha_composite(base, ov).convert("RGB")
    legend(out, scale)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # lossless webp keeps the flat overlay tints + legend text crisp, repo-light
    # (matches docs/maps/renders/).
    out.save(out_path, "WEBP", lossless=True, method=6)


def legend(img: Image.Image, scale: int) -> None:
    d = ImageDraw.Draw(img, "RGBA")
    rows = [
        ((60, 200, 90), "walk (on foot)"),
        ((240, 220, 60), "reachable only with a Gift"),
        ((60, 170, 255), "Gift-gated tile (water/void)"),
        ((255, 140, 0), "ledge (one-way)"),
        ((220, 40, 40), "solid"),
        ((255, 0, 220), "ORPHAN — cut off w/ all Gifts"),
        ((255, 30, 30), "softlocked warp (outline)"),
    ]
    pad, sw, lh = 6, 14, 18
    bw = 230
    bh = pad * 2 + lh * len(rows)
    x0, y0 = 4, img.height - bh - 4
    d.rectangle((x0, y0, x0 + bw, y0 + bh), fill=(10, 14, 30, 210))
    for i, (c, label) in enumerate(rows):
        yy = y0 + pad + i * lh
        d.rectangle((x0 + pad, yy + 2, x0 + pad + sw, yy + sw), fill=c + (255,))
        d.text((x0 + pad + sw + 6, yy), label, fill=(235, 235, 235, 255))


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #
def is_offender(info: dict) -> bool:
    return bool(info["softlocks"] or info["major_orphans"])


def report_line(info: dict) -> str:
    bits = [f"{info['map']:<26} {info['kind']:<9}"]
    for s in info["softlocks"]:
        g = f"needs {s['needs_gift']}" if s["needs_gift"] else "fully cut off"
        bits.append(f"SOFTLOCK[{s['warp']}->{s['to']} @ {s['at']} "
                    f"flag {s['flag']} but {g}]")
    if info["major_orphans"]:
        for c in sorted(info["major_orphans"], key=len, reverse=True):
            bits.append(f"ORPHAN x{len(c)} near {min(sorted(c))}")
    minor = [c for c in info["orphan_clusters"] if len(c) < MAJOR_ORPHAN]
    if minor:
        bits.append(f"(minor: {sum(len(c) for c in minor)} border-gap tiles)")
    return "  ".join(bits)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("map", nargs="?", help="map id (or path); omit with --all.")
    ap.add_argument("--all", action="store_true", help="process every shipped map.")
    ap.add_argument("--scale", type=int, default=4, help="overlay upscale (default 4).")
    ap.add_argument("--report-only", action="store_true", help="no PNGs, just the report.")
    ap.add_argument("--out", default=str(OUT_DIR), help="output dir for overlays.")
    args = ap.parse_args()

    world = load_world()
    try:
        start = parse_graph()
    except Exception:
        start = None
    if args.all:
        ids = sorted(world)
    elif args.map:
        ids = [Path(args.map).stem]
    else:
        ap.error("give a map id or --all")

    out_dir = Path(args.out)
    infos = []
    for mid in ids:
        if mid not in world:
            print(f"  ?? unknown map: {mid}", file=sys.stderr)
            continue
        model = MapModel(world[mid])
        info = analyse(world, model, start)
        info["static_npcs"] = model.static_npc_tiles
        infos.append(info)
        if not args.report_only:
            render_overlay(model, info, args.scale, out_dir / f"{mid}.webp")

    # report: offenders (softlock / major orphan) first; minor border gaps are noted
    print(f"\nWalkability pass — {len(infos)} map(s)\n" + "=" * 72)
    offenders = [i for i in infos if is_offender(i)]
    for info in offenders:
        print("  " + report_line(info))
    if not offenders:
        print("  no softlocks or major orphans found.")
    minor_only = [i for i in infos if not is_offender(i) and i["orphans"]]
    if minor_only:
        print(f"\n  ({len(minor_only)} map(s) with only minor border-gap tiles — harmless)")
    if not args.report_only:
        print(f"\noverlays -> {out_dir}")
    print("=" * 72)
    print(f"{len(offenders)} map(s) with REAL issues, {len(infos) - len(offenders)} ok.")
    return 1 if offenders else 0


if __name__ == "__main__":
    sys.exit(main())
