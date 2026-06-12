#!/usr/bin/env python3
"""
audit_spatial — does the WORLD'S GEOMETRY make sense?

audit_warps proves each door pair exists and lands safely; this audit proves the
links are spatially coherent: walking off one map's edge should put you on an
EDGE of the neighbour, facing INWARD at the landing, near where you left — and
the two directions of every link must mirror each other (if A's east road lands
on B's west edge, B's west road must land back on A's east edge).

Authoring conventions this encodes (learned from the shipped maps):
  * `facing` points INWARD from the LANDING edge (n→down, s→up, w→right,
    e→left) — not "continue the exit direction". On a straight link the two
    coincide; on a bent Lanternway spoke only the landing-inward rule holds.
  * Links may be STRAIGHT (opposite edges), BENT (perpendicular — a long road
    that turns, e.g. galehigh S ↔ crossroads W), or a RING U-TURN (same edge
    both sides — only sensible into an annulus map like penumbra_ring, whose
    outer edge is "outside the ring" from every approach). Bends/U-turns are
    reported as info so a new one is a conscious choice, never an accident.
  * CAVE maps land you mid-floor by design (mouths, ladders, the mine
    shortcut) — exempt from edge logic.

Checks:
  [F] edge-landing   a non-cave link must land on (within 2 tiles of) an edge
                     of the target — mid-map landings tear the world.
  [F] facing         arrival facing must point inward from the landing edge.
  [F] mirror         the reverse direction must use the mirrored edge pair,
                     and all links between the same two maps must agree.
  [W] round-trip     leave A, return through B's nearest portal back: you
                     should land within DRIFT_TOL tiles laterally of where you
                     left (silent teleports along the shared edge).
  [·] bends/U-turns and unit-embedding loop misclosures (roads bend) — info.
"""
from __future__ import annotations

import sys
from worldmodel import load_world

DRIFT_TOL = 3          # tiles of lateral drift allowed on a round trip
EDGE_TOL = 2           # landing may sit up to this far inboard of the edge
OPP = {"n": "s", "s": "n", "e": "w", "w": "e"}
INWARD = {"n": "down", "s": "up", "w": "right", "e": "left"}
STEP = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}


def edges_of(m: dict, tx: int, ty: int, tol: int = 0) -> set[str]:
    """Which border(s) of map `m` is (tx,ty) on (or within `tol` tiles of)?"""
    out = set()
    if ty <= tol:
        out.add("n")
    if ty >= m["height"] - 1 - tol:
        out.add("s")
    if tx <= tol:
        out.add("w")
    if tx >= m["width"] - 1 - tol:
        out.add("e")
    return out


def main() -> int:
    world = load_world()
    fails: list[str] = []
    warns: list[str] = []
    infos: list[str] = []

    # ---- collect edge links (border warp, not a door, both maps outdoors) ---
    links = []  # (src_id, warp, exit_edge, land_edge|None)
    for mid, m in sorted(world.items()):
        if m.get("kind") in ("interior", "cave"):
            continue
        for w in m.get("warps", []):
            if w.get("transition") == "door":
                continue
            dst = world.get(w.get("to_map", ""))
            if dst is None or dst.get("kind") in ("interior", "cave"):
                continue
            src_edges = edges_of(m, w["at"]["tx"], w["at"]["ty"])
            if not src_edges:
                continue  # interior-style placement (e.g. a cave mouth pad)
            dst_edges = edges_of(dst, w["to"]["tx"], w["to"]["ty"], tol=EDGE_TOL)
            label = f"{mid}:{w['id']} -> {w['to_map']}"

            if not dst_edges:
                fails.append(f"edge-landing  {label}: lands mid-map at "
                             f"({w['to']['tx']},{w['to']['ty']})")
                continue

            # corner tiles sit on two edges; prefer the straight reading
            exit_e = next((e for e in src_edges if OPP[e] in dst_edges),
                          sorted(src_edges)[0])
            land_e = OPP[exit_e] if OPP[exit_e] in dst_edges else sorted(dst_edges)[0]
            links.append((mid, w, exit_e, land_e))

            if w.get("facing") and w["facing"] != INWARD[land_e]:
                fails.append(f"facing        {label}: lands on the {land_e.upper()} edge "
                             f"so should face '{INWARD[land_e]}', has '{w['facing']}'")

    # ---- per-pair shape agreement + mirror symmetry --------------------------
    pair_shape: dict[tuple[str, str], set[tuple[str, str]]] = {}
    for mid, w, exit_e, land_e in links:
        pair_shape.setdefault((mid, w["to_map"]), set()).add((exit_e, land_e))

    for (a, b), shapes in sorted(pair_shape.items()):
        if len(shapes) > 1:
            pretty = ", ".join(f"{x.upper()}->{y.upper()}" for x, y in sorted(shapes))
            fails.append(f"mirror        {a} -> {b} links disagree on geometry: {pretty}")
    for (a, b), shapes in sorted(pair_shape.items()):
        if len(shapes) != 1:
            continue
        exit_e, land_e = next(iter(shapes))
        rev = pair_shape.get((b, a))
        if rev and len(rev) == 1:
            r_exit, r_land = next(iter(rev))
            if (r_exit, r_land) != (land_e, exit_e):
                fails.append(f"mirror        {a} <-> {b}: forward is "
                             f"{exit_e.upper()}->{land_e.upper()} but the return is "
                             f"{r_exit.upper()}->{r_land.upper()} "
                             f"(expected {land_e.upper()}->{exit_e.upper()})")
        if a < b:  # describe each undirected link once
            if land_e == OPP[exit_e]:
                pass  # straight — the silent default
            elif land_e == exit_e:
                infos.append(f"ring U-turn   {a} {exit_e.upper()} <-> {b} {land_e.upper()} "
                             f"(same edge both sides — annulus/abstracted road)")
            else:
                infos.append(f"bent road     {a} exits {exit_e.upper()}, arrives on "
                             f"{b}'s {land_e.upper()} edge (long road that turns)")

    # ---- round-trip lateral drift --------------------------------------------
    for mid, w, exit_e, land_e in links:
        if land_e != OPP[exit_e]:
            continue  # drift is only meaningful on straight links
        dst = world[w["to_map"]]
        lat = 0 if exit_e in ("n", "s") else 1
        src_lat = (w["at"]["tx"], w["at"]["ty"])[lat]
        land = (w["to"]["tx"], w["to"]["ty"])
        returns = [r for r in dst.get("warps", [])
                   if r.get("to_map") == mid and r.get("transition") != "door"
                   and land_e in edges_of(dst, r["at"]["tx"], r["at"]["ty"], tol=EDGE_TOL)]
        if not returns:
            continue
        r = min(returns, key=lambda r: abs(r["at"]["tx"] - land[0]) + abs(r["at"]["ty"] - land[1]))
        back = (r["to"]["tx"], r["to"]["ty"])[lat]
        drift = abs(back - src_lat)
        if drift > DRIFT_TOL:
            warns.append(f"round-trip    {mid}:{w['id']} -> {w['to_map']}: leave at lateral "
                         f"{src_lat}, the trip back lands at {back} ({drift} tiles of drift)")

    # ---- unit-step embedding (informational) ----------------------------------
    adj: dict[str, dict[str, str]] = {}
    for (a, b), shapes in pair_shape.items():
        if len(shapes) == 1:
            exit_e, land_e = next(iter(shapes))
            if land_e == OPP[exit_e]:
                adj.setdefault(a, {})[b] = exit_e
    pos: dict[str, tuple[int, int]] = {}
    seen_loops: set[frozenset] = set()
    for root in sorted(adj):
        if root in pos:
            continue
        pos[root] = (0, 0)
        stack = [root]
        while stack:
            cur = stack.pop()
            for nxt, d in adj.get(cur, {}).items():
                dx, dy = STEP[d]
                want = (pos[cur][0] + dx, pos[cur][1] + dy)
                if nxt in pos:
                    off = abs(want[0] - pos[nxt][0]) + abs(want[1] - pos[nxt][1])
                    key = frozenset((cur, nxt))
                    if off and key not in seen_loops:
                        seen_loops.add(key)
                        infos.append(f"embedding     loop closing {cur} -> {nxt} is {off} "
                                     f"unit(s) off square (roads bend; informational)")
                else:
                    pos[nxt] = want
                    stack.append(nxt)

    # ---- report ----------------------------------------------------------------
    print(f"Spatial audit — {len(links)} overworld edge links across "
          f"{len({m for m, *_ in links})} maps")
    for f in fails:
        print(f"  [F] {f}")
    for w in warns:
        print(f"  [W] {w}")
    if not fails and not warns:
        print("  [✓] every overworld link lands on a neighbouring edge, facing inward,"
              " with mirrored geometry both ways and no lateral teleports")
    for i in infos:
        print(f"  [·] {i}")
    print(f"{'FAIL' if fails else 'PASS'} — {len(fails)} failure(s), {len(warns)} warning(s), "
          f"{len(infos)} note(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
