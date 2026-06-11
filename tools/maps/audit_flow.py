#!/usr/bin/env python3
"""
Flow audit — measures whether a map PLAYS, not just whether it renders.

validate_map.py judges the picture (layers, meshing, decoration); audit_warps.py
judges the doors. This audits the LEVEL DESIGN between them — the structural
§3a pass from docs/world/level-design.md, executed instead of eyeballed:

  REACH        every NPC, trigger and portal is reachable from the map's doors
               (with all Lantern Gifts — gated content counts; orphaned content
               is a FAIL, it can never fire).
  CHOKE        step_on story triggers (`script.*`) actually sit on chokes: a
               trigger band a player can walk around will silently skip a beat.
  FREE PASS    a route/cave can't be crossed door-to-door while dodging every
               encounter tile, every sight-trainer's line AND every story
               trigger (level-design §11 rule 7: routes carry gameplay).
  LOOP         the §3a "loops, not corridors" rule: one-way ledges/shortcuts
               that compress the return trip. Reported per portal pair.
  DEAD ENDS    every off-lane pocket pays (cache/NPC/sign/encounter/warp) —
               §3a rule 4: an empty detour teaches players not to explore.
  SCREENS      per 15×10 screenful: walkable screens with nothing in them
               (no NPC/trigger/warp/object/encounter/ledge) read as filler —
               §3a rule 5: one idea per screen.

FAIL = broken (unreachable content). WARN = the design rule is violated; fix it
or justify it in the builder. Interiors only run REACH (they're rooms, not
levels). Usage:
    audit_flow.py                  # the whole authored world
    audit_flow.py <map_id> ...     # focus maps
    audit_flow.py <map_id> --json  # machine-readable
"""
from __future__ import annotations

import json
import sys

from worldmodel import ALL_ABILITIES, MapModel, load_world, parse_graph

SCREEN_W, SCREEN_H = 15, 10
GIFTS = set(ALL_ABILITIES)


def cluster(cells: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    out, seen = [], set()
    for c in cells:
        if c in seen:
            continue
        blob, stack = set(), [c]
        seen.add(c)
        while stack:
            x, y = stack.pop()
            blob.add((x, y))
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in cells and n not in seen:
                    seen.add(n)
                    stack.append(n)
        out.append(blob)
    return out


def audit_map(mm: MapModel, start_at: tuple[int, int] | None) -> list[dict]:
    checks: list[dict] = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    portals = mm.portals()
    anchors: list[set] = [p["stand"] for p in portals if p["stand"]]
    if start_at:
        anchors.append({start_at})
    if not anchors:
        add("reach", "WARN", "map has no portals and no spawn — nothing to audit from")
        return checks

    all_starts = set().union(*anchors)
    reach = mm.bfs(all_starts, abilities=GIFTS)

    # ---- REACH: NPCs, triggers, portals --------------------------------------
    def adjacent_reachable(x, y):
        return any((x + dx, y + dy) in reach
                   for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))

    orphans = []
    for npc in mm.npcs:
        x, y = npc["at"]["tx"], npc["at"]["ty"]
        if (x, y) not in reach and not adjacent_reachable(x, y):
            orphans.append(f"npc '{npc['id']}' at ({x},{y})")
    for trg in mm.triggers:
        x, y = trg["at"]["tx"], trg["at"]["ty"]
        if (x, y) not in reach and not adjacent_reachable(x, y):
            orphans.append(f"trigger '{trg['id']}' at ({x},{y})")
    for p in portals:
        if len(portals) + (1 if start_at else 0) < 2:
            break
        others = set().union(*(a for a in anchors if a != p["stand"]))
        if others and not (mm.bfs(others, abilities=GIFTS).keys() & p["stand"]):
            orphans.append(f"portal -> {p['to_map']} ({sorted(p['tiles'])[0]})")
    if orphans:
        add("reach", "FAIL", "unreachable content (even with all Gifts): "
            + "; ".join(orphans[:6]) + ("…" if len(orphans) > 6 else ""))
    else:
        add("reach", "PASS",
            f"{len(mm.npcs)} NPCs, {len(mm.triggers)} triggers, "
            f"{len(portals)} portals all reachable")

    if mm.kind == "interior":
        return checks

    # the "through pair": the two most-separated portal groups (the level's axis)
    pair = None
    if len(anchors) >= 2:
        best = -1
        for i in range(len(anchors)):
            di = mm.bfs(anchors[i], abilities=GIFTS)
            for j in range(len(anchors)):
                if i == j:
                    continue
                ds = [di[t] for t in anchors[j] if t in di]
                if ds and min(ds) > best:
                    best, pair = min(ds), (anchors[i], anchors[j])

    # ---- CHOKE: story step_on triggers must not be walkable-around ----------
    # A story band guards the portal it sits nearest (the gate-warden pattern);
    # if no portal is within reach of the band, it guards the map's long axis.
    story = {}
    for trg in mm.triggers:
        ref = trg.get("ref", "")
        if trg.get("activation") == "step_on" and ref.startswith("script."):
            story.setdefault(ref, set()).add((trg["at"]["tx"], trg["at"]["ty"]))
    if story and pair:
        bypassed = []
        for ref, tiles in story.items():
            guarded = None
            for a in anchors:
                d = min(abs(t[0] - s[0]) + abs(t[1] - s[1])
                        for t in tiles for s in a)
                if d <= 3 and (guarded is None or d < guarded[1]):
                    guarded = (a, d)
            if guarded:
                others = [a for a in anchors if a is not guarded[0]]
                src = set().union(*others) if others else set()
                if src and mm.path(src, guarded[0], avoid=tiles,
                                   npc_block=mm.static_npc_tiles):
                    bypassed.append(ref)
            elif mm.path(pair[0], pair[1], avoid=tiles,
                         npc_block=mm.static_npc_tiles):
                bypassed.append(ref)
        if bypassed:
            add("choke", "WARN", "story trigger(s) can be walked around: "
                + ", ".join(sorted(bypassed)))
        else:
            add("choke", "PASS", f"{len(story)} story trigger band(s) sit on true chokes")

    # ---- FREE PASS + safe lane (routes/caves) --------------------------------
    if mm.kind in ("route", "cave") and pair:
        sights = set().union(*mm.sight_tiles().values()) if mm.sight_tiles() else set()
        enc = {(i % mm.w, i // mm.w) for i, e in enumerate(mm.encounter) if e}
        story_tiles = set().union(*story.values()) if story else set()
        gauntlet = enc | sights | story_tiles
        free = mm.path(pair[0], pair[1], avoid=gauntlet,
                       npc_block=mm.static_npc_tiles)
        if free:
            add("free-pass", "WARN",
                "the map can be crossed end-to-end dodging every encounter tile, "
                "sight line and story trigger — §11 rule 7: a route carries gameplay")
        else:
            add("free-pass", "PASS", "no zero-gameplay path across the map")
        if enc:
            safe = mm.path(pair[0], pair[1], avoid=enc)
            add("safe-lane", "INFO",
                ("a no-encounter lane exists (early-route friendly)" if safe
                 else "every crossing rolls encounters (mid/late-route pacing)"))

    # ---- LOOP: return-trip asymmetry -----------------------------------------
    has_ledge = any(mm.ledge[i] for i in range(mm.w * mm.h))
    if mm.kind in ("route", "cave") and pair:
        d_fwd = min((mm.bfs(pair[0], abilities=GIFTS).get(t, 10**9) for t in pair[1]),
                    default=10**9)
        d_back = min((mm.bfs(pair[1], abilities=GIFTS).get(t, 10**9) for t in pair[0]),
                     default=10**9)
        lo, hi = min(d_fwd, d_back), max(d_fwd, d_back)
        if has_ledge and lo < hi:
            add("loop", "PASS",
                f"one-way ledges make the trips asymmetric: {hi} steps the long "
                f"way, {lo} with the hops ({100 * lo // max(1, hi)}%)")
        elif has_ledge:
            add("loop", "INFO", "ledges present but both directions walk the same "
                "distance — check the hops actually cut a fold")
        else:
            add("loop", "WARN", "no one-way ledge/shortcut — the map walks back "
                "exactly as it walked in (§3a rule 1: loops, not corridors)")

    # ---- DEAD ENDS pay --------------------------------------------------------
    if pair:
        lane: set[tuple[int, int]] = set()
        for i in range(len(anchors)):
            for j in range(i + 1, len(anchors)):
                p = mm.path(anchors[i], anchors[j], abilities=GIFTS)
                if p:
                    lane.update(p)
        if lane:
            off = {c for c, d in mm.bfs(lane, abilities=GIFTS).items() if d >= 4}
            payoff_pts = set()
            for npc in mm.npcs:
                payoff_pts.add((npc["at"]["tx"], npc["at"]["ty"]))
            for trg in mm.triggers:
                payoff_pts.add((trg["at"]["tx"], trg["at"]["ty"]))
            for wp in mm.warps:
                payoff_pts.add((wp["at"]["tx"], wp["at"]["ty"]))
            enc = {(i % mm.w, i // mm.w) for i, e in enumerate(mm.encounter) if e}
            unpaid = []
            for blob in cluster(off):
                if len(blob) < 10:
                    continue
                ring = {(x + dx, y + dy) for x, y in blob
                        for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
                if not (ring & payoff_pts) and not (blob & enc):
                    xs = [c[0] for c in blob]
                    ys = [c[1] for c in blob]
                    unpaid.append(f"({min(xs)},{min(ys)})–({max(xs)},{max(ys)})")
            if unpaid:
                add("dead-ends", "WARN",
                    f"{len(unpaid)} off-lane pocket(s) with NO payoff "
                    f"(§3a rule 4 — every detour pays): {', '.join(unpaid[:3])}")
            else:
                add("dead-ends", "PASS", "every sizeable off-lane pocket pays")

    # ---- SCREENS: one idea per screenful --------------------------------------
    if mm.w * mm.h >= 2 * SCREEN_W * SCREEN_H:
        interest = set()
        for npc in mm.npcs:
            interest.add((npc["at"]["tx"], npc["at"]["ty"]))
        for trg in mm.triggers:
            interest.add((trg["at"]["tx"], trg["at"]["ty"]))
        for wp in mm.warps:
            interest.add((wp["at"]["tx"], wp["at"]["ty"]))
        for o in mm.m.get("objects", []):
            interest.add((o["at"]["tx"], o["at"]["ty"]))
        for i, e in enumerate(mm.encounter):
            if e:
                interest.add((i % mm.w, i // mm.w))
        for i, l in enumerate(mm.ledge):
            if l:
                interest.add((i % mm.w, i // mm.w))
        dull = []
        for sy in range(0, mm.h, SCREEN_H):
            for sx in range(0, mm.w, SCREEN_W):
                cells = [(x, y) for y in range(sy, min(sy + SCREEN_H, mm.h))
                         for x in range(sx, min(sx + SCREEN_W, mm.w))]
                walk = sum(1 for c in cells if c in reach)
                if walk < len(cells) * 0.25:
                    continue  # mostly enclosure — scenery is allowed to be scenery
                if not any(c in interest for c in cells):
                    dull.append(f"screen({sx // SCREEN_W},{sy // SCREEN_H})")
        if dull:
            add("screens", "WARN",
                f"{len(dull)} walkable screenful(s) carry no idea — no NPC/trigger/"
                f"warp/object/encounter/ledge (§3a rule 5): {', '.join(dull[:4])}")
        else:
            add("screens", "PASS", "every walkable screenful carries something")

    return checks


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    world = load_world()
    graph = parse_graph()
    focus = args if args else sorted(world.keys())

    reports = {}
    any_fail = False
    for mid in focus:
        if mid not in world:
            print(f"unknown map: {mid}", file=sys.stderr)
            return 2
        mm = MapModel(world[mid])
        start = None
        if graph.get("start_map") == mid and graph.get("start_at"):
            start = (graph["start_at"]["tx"], graph["start_at"]["ty"])
        checks = audit_map(mm, start)
        reports[mid] = checks
        any_fail |= any(c["status"] == "FAIL" for c in checks)

    if as_json:
        print(json.dumps(reports, indent=2))
    else:
        icon = {"PASS": "✓", "WARN": "!", "FAIL": "✗", "INFO": "·"}
        for mid, checks in reports.items():
            print(f"\nFlow audit — {mid} ({world[mid].get('kind', '?')})")
            for c in checks:
                print(f"  [{icon[c['status']]}] {c['check']:<10} {c['detail']}")
        n_fail = sum(c["status"] == "FAIL" for cs in reports.values() for c in cs)
        n_warn = sum(c["status"] == "WARN" for cs in reports.values() for c in cs)
        print(f"\n{'FAIL' if any_fail else 'PASS'} — {n_fail} failure(s), "
              f"{n_warn} design warning(s) across {len(reports)} map(s)")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
