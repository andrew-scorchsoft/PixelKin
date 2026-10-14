#!/usr/bin/env python3
"""
NPC footing audit — every placed NPC must STAND somewhere and be TALKABLE (CI gate).

Andrew was found standing IN THE SEA beside a pier on two maps: his anchor tile
was open water, so he floated on the waves and could only be reached by swimming.
None of the other audits look at where an NPC's feet are — audit_flow/journey
treat NPC bodies as blockers, not as content that has to read right. This does.

For every non-ambient NPC placement (`ambient: true` kin are set dressing the
engine never talks to — skipped, like worldmodel does):

  FOOTING   its anchor tile is in bounds and FOOT-STANDABLE in the engine model
            (worldmodel.MapModel): not solid (tile collision / an object's
            footprint), not ability-gated (water, deepwood, void ...), not a ledge.
  TALKABLE  the player can face it: at least one 4-neighbour tile is reachable
            from the map's entrances WITH ALL GIFTS — or, mirroring
            WorldScene.npcAcrossDesk, a reachable tile faces it across one or two
            desk-like object tiles (counter|desk|stall|altar|lectern).

Entrances = the `to` landing of every warp in any map that points here, the
world start, and every literal `{ op: 'travel', map, to }` in the content (the
Lantern-car / lift rides). A map nobody lands on falls back to its whole floor.

Deliberate exceptions (a cat on her cushion, a swim-to cache) live in ALLOW with
a one-line WHY. An ALLOW entry that no longer fires is reported as stale.

Run:   python3 tools/maps/audit_npc_footing.py            # whole world
       python3 tools/maps/audit_npc_footing.py <map_id>
Exit 1 on any violation.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from worldmodel import ALL_ABILITIES, DIRS, MapModel, load_world, parse_graph  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
CONTENT = REPO / "src/game/content"
DESK_SPRITE = re.compile(r"(counter|desk|stall|altar|lectern)")   # WorldScene.DESK_SPRITE
TRAVEL_RE = re.compile(
    r"op:\s*'travel',\s*map:\s*'([^']+)',\s*to:\s*\{\s*tx:\s*(\d+),\s*ty:\s*(\d+)")

# (map_id, npc_id) -> why its anchor may sit off foot-standable ground.
ALLOW: dict[tuple[str, str], str] = {
    ("georgina_cottage", "gloampurr_nook"):
        "Georgina's cat curled on her cushion (the `cat_cushion` bed object) — "
        "seated ON furniture by design, talked to from the floor beside it.",
    # Lane E (walkthrough/10 Part III — the deep backtrack): buoy-caches moored on
    # DEEP water, every neighbour deep, so only the Farlamp skiff rows up to them.
    ("gullcry_rock", "cache_gullcry_deep"): "a buoy-cache moored on the deep (skiff only, 10 Part III).",
    ("pearlmoor_quay", "cache_pearlmoor_deep"): "a buoy-cache moored on the deep (skiff only, 10 Part III).",
    ("dimglass_coast_ii", "cache_dimglass_deep"): "a buoy-cache moored on the deep (skiff only, 10 Part III).",
    ("vigil_hearthfall", "cache_hearthfall_deep"): "a buoy-cache moored on the deep (skiff only, 10 Part III).",
}


def travel_landings() -> dict[str, set[tuple[int, int]]]:
    out: dict[str, set[tuple[int, int]]] = {}
    for p in CONTENT.rglob("*.ts"):
        for mid, tx, ty in TRAVEL_RE.findall(p.read_text()):
            out.setdefault(mid, set()).add((int(tx), int(ty)))
    return out


def entrances(world: dict, mid: str, start: dict | None,
              travel: dict[str, set[tuple[int, int]]]) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set(travel.get(mid, set()))
    for m in world.values():
        for w in m.get("warps", []):
            if w.get("to_map") == mid and w.get("to"):
                out.add((w["to"]["tx"], w["to"]["ty"]))
    if start and start.get("start_map") == mid and start.get("start_at"):
        out.add((start["start_at"]["tx"], start["start_at"]["ty"]))
    return out


def footing_problem(model: MapModel, x: int, y: int) -> str | None:
    if not model.in_bounds(x, y):
        return "out of bounds"
    i = y * model.w + x
    if model.kit and (x, y) in model._span_at:
        return None
    if model.solid[i]:
        return "SOLID (tile collision or object footprint)"
    if model.ability[i]:
        return f"ability-gated ({model.ability[i]})"
    if model.ledge[i]:
        return "a ledge"
    return None


def desk_tiles(model: MapModel) -> set[tuple[int, int]]:
    out = set()
    for o in model.m.get("objects", []):
        if o.get("solid") is False or not DESK_SPRITE.search(o.get("sprite", "")):
            continue
        for ty in range(o["at"]["ty"], o["at"]["ty"] + o["h"]):
            for tx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
                out.add((tx, ty))
    return out


def talk_spots(model: MapModel, x: int, y: int, desks: set) -> set[tuple[int, int]]:
    """Tiles a player can stand on and Confirm to reach the NPC at (x, y)."""
    spots = set()
    for dx, dy in DIRS.values():
        spots.add((x + dx, y + dy))
        # across a desk: player at P faces D1 (desk); NPC at D1+d or D2+d (D2 desk)
        d1 = (x + dx, y + dy)
        if d1 in desks:
            spots.add((d1[0] + dx, d1[1] + dy))
            d2 = (d1[0] + dx, d1[1] + dy)
            if d2 in desks:
                spots.add((d2[0] + dx, d2[1] + dy))
    return spots


def audit_map(world, mid, start, travel) -> list[tuple[str, str, str]]:
    model = MapModel(world[mid])
    all_ab = set(ALL_ABILITIES)
    seeds = entrances(world, mid, start, travel)
    seeds = {s for s in seeds if model.standable(*s, abilities=all_ab)}
    if not seeds:   # nobody lands here (debug / unregistered): judge the whole floor
        seeds = {(x, y) for y in range(model.h) for x in range(model.w)
                 if model.standable(x, y, abilities=all_ab)}
    reach = set(model.bfs(list(seeds), abilities=all_ab))
    desks = desk_tiles(model)
    seen: set[tuple[str, tuple[int, int]]] = set()
    out = []
    for npc in model.npcs:
        x, y = npc["at"]["tx"], npc["at"]["ty"]
        key = (npc["id"], (x, y))
        if key in seen:
            continue
        seen.add(key)
        problems = []
        fp = footing_problem(model, x, y)
        if fp:
            problems.append(f"stands on {fp}")
        if not (talk_spots(model, x, y, desks) & reach):
            problems.append("UNTALKABLE (no reachable tile faces it, even with every Gift)")
        if problems:
            out.append((npc["id"], f"({x},{y})", "; ".join(problems)))
    return out


def main() -> int:
    world = load_world()
    try:
        start = parse_graph()
    except Exception:
        start = None
    travel = travel_landings()
    ids = [Path(a).stem for a in sys.argv[1:]] or sorted(world)
    bad, allowed = [], []
    hit_allow = set()
    for mid in ids:
        if mid not in world:
            print(f"unknown map {mid}")
            return 2
        for nid, at, why in audit_map(world, mid, start, travel):
            if (mid, nid) in ALLOW:
                hit_allow.add((mid, nid))
                allowed.append((mid, nid, at, ALLOW[(mid, nid)]))
            else:
                bad.append((mid, nid, at, why))
    for mid, nid, at, why in allowed:
        print(f"  allow  {mid}:{nid} {at} — {why}")
    stale = [k for k in ALLOW if k[0] in ids and k not in hit_allow]
    for mid, nid in stale:
        print(f"  WARN   stale ALLOW entry {mid}:{nid} (no longer fires — prune it)")
    for mid, nid, at, why in bad:
        print(f"  FAIL   {mid}:{nid} {at} — {why}")
    n = sum(len([p for p in world[m].get('npcs', []) if not p.get('ambient')]) for m in ids)
    print(f"NPC footing: {len(ids)} maps, {n} placements, {len(allowed)} allowed, "
          f"{len(bad)} FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
