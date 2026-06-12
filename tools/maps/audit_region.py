#!/usr/bin/env python3
"""
Region audit — validates the SCENE, not the map: how maps chain into routes,
regions, and the opening world. The per-map tools (validate_map, audit_flow,
audit_warps) can all pass while the region they form is broken — a declared
edge with no warp behind it, a level band that jumps 6 levels across a border,
a region that's a pure corridor, a Gift wave that never unlocks its area.

What it checks (docs/world/level-design.md §2b — the region is the level):

  GRAPH SYNC    graph.ts ⇄ map JSON: every declared edge's via_warp exists on
                its from_map and targets its to_map (FAIL); bidirectional edges
                have a return warp (FAIL); authored warps to authored maps that
                have NO declared edge are flagged (WARN — undeclared geometry).
  PROGRESSION   replays the journey: starting at start_map with nothing, expand
                reachability wave by wave as Gifts/flags are earned where the
                walkthrough grants them (the table below). Every non-postgame
                node must unlock by the final wave (FAIL), and the report shows
                WHICH wave opens each area — the "map reopening itself" curve.
  LEVEL BANDS   encounter bands of authored, connected maps must STEP, not jump:
                a border where min-levels differ by more than 4 is a difficulty
                cliff (WARN). Optional spurs are allowed to spike (they're paid
                detours). Prints the band table per region.
  TOPOLOGY      per region: corridor or circuit? Counts independent cycles in
                the overworld subgraph (interiors excluded). A region with no
                cycle and no one-way shortcut plays as a hallway walked twice
                (WARN, §3a rule 1 at region scale).
  TRAVEL        per authored route map: the door-to-door walking distance in
                steps (its "length"), so a region's leg budget is visible
                against the heal anchors (towns) on either side. INFO.

Run:  ./venv/bin/python tools/maps/audit_region.py            # whole world
      ./venv/bin/python tools/maps/audit_region.py --json
Exit 1 on FAIL.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict

from worldmodel import ALL_ABILITIES, MapModel, load_world, parse_graph

# Where the journey grants each Gift / story flag (walkthrough spine §2 + §5;
# update here if the canon grant points ever move). A flag/ability is "earned"
# once its source map becomes reachable in the simulation.
GRANTS: dict[str, list[str]] = {
    "vesper_crossroads": ["flag:has_starter"],          # the waystone ceremony
    "dimglass_coast": ["flag:has_beacon_wick"],         # the lamplighter's key
    "tinderwick_beacon_top": ["gleam:ember"],           # the earned first Gleam
    # The Causeway Bell loop: the netmender hands the bell-rope on the quay
    # (after the net-floats errand on Dimglass II — both reachable on foot).
    "pearlmoor_quay": ["flag:q_south_has_rope"],
    "pearlmoor_breakwater": ["flag:q_south_bell_rung"],  # the Moor-bell rung
    "pearlmoor_lumenary": ["tidecall", "gleam:tide", "flag:crown_south"],
    "lowleaf_hollow": ["glimmerstep", "gleam:verdant"],
    "cinderhead_mine": ["gleam:stone", "flag:crown_east"],
    "cinderhead_deep": ["flag:shortcut_mine"],
    # The Kite-Rising Winch loop: the kite chain + festival blessing happen in
    # town; Mira's bond-test at the skyloft then grants the Gleam + the Gift.
    "galehigh_terraces": ["flag:q_north_kite_blessed"],
    "galehigh_skyloft": ["updraft_kite", "gleam:storm"],
    "windward_stair_ii": ["flag:shortcut_windward"],
    # The Lamp-Line loop: the oil errand happens in town/the hollows; Ysolde's
    # bond-test at the undercroft's heart then grants the Gleam + the Gift.
    "pale_vault_glacier": ["flag:q_north_lampline", "flag:q_north_aurora_oil"],
    "pale_vault_undercroft": ["flag:q_north_lamps_held", "emberward",
                              "gleam:frost", "flag:crown_north"],
    "sunken_solarium": ["sunsketch", "gleam:solar"],
    "nightreach_observatory": ["starreach", "gleam:lunar", "flag:crown_west",
                               "flag:hub_unlocked"],
    "umbral_spire": ["flag:dawn"],
    # H1 (the Three Hours): the Lampwright's Relay completes inside the cavern
    # (the rumour itself comes from the Pearlmoor netmender — wiring pass).
    "tideglass_cavern": ["flag:q_south_wrecklamp_lit", "flag:three_dusk_lens_c"],
}
# ---- The Three Hours (walkthrough/07-the-three) — the unlock chains' keys
# ride the existing grant points (rumours in the host towns; Ysolde's Vigil
# Snuffer below the vault; Lucan's phial + the basin pour at the Solarium).
GRANTS["pearlmoor_quay"].append("flag:three_dusk_rumour")
GRANTS["pale_vault_glacier"].append("flag:three_mid_rumour")
GRANTS["pale_vault_undercroft"].append("flag:three_mid_snuffer")
GRANTS["nightreach_observatory"].append("flag:three_dawn_rumour")
GRANTS["sunken_solarium"] += ["flag:three_dawn_phial", "flag:three_dawn_poured"]
POSTGAME_FLAGS = {"flag:dawn"}


def main() -> int:
    as_json = "--json" in sys.argv
    world = load_world()
    graph = parse_graph()
    nodes = {n["map_id"]: n for n in graph["nodes"]}
    edges = graph["edges"]
    checks: list[dict] = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    # ---- GRAPH SYNC -----------------------------------------------------------
    sync_fails, undeclared = [], []
    declared = set()
    for e in edges:
        declared.add((e["from_map"], e["to_map"]))
        if e["bidirectional"]:
            declared.add((e["to_map"], e["from_map"]))
        src = world.get(e["from_map"])
        if src is None:
            continue  # unauthored map — the graph is ahead of the content, fine
        warp = next((w for w in src.get("warps", []) if w["id"] == e["via_warp"]), None)
        if warp is None:
            sync_fails.append(f"edge {e['from_map']} -> {e['to_map']}: warp "
                              f"'{e['via_warp']}' not on the map")
        elif warp["to_map"] != e["to_map"]:
            sync_fails.append(f"edge {e['from_map']} -> {e['to_map']}: warp "
                              f"'{e['via_warp']}' actually targets '{warp['to_map']}'")
        if e["bidirectional"] and e["to_map"] in world:
            back = [w for w in world[e["to_map"]].get("warps", [])
                    if w["to_map"] == e["from_map"]]
            if not back:
                sync_fails.append(f"edge {e['from_map']} <-> {e['to_map']}: no return "
                                  f"warp on '{e['to_map']}'")
    for mid, m in world.items():
        for w in m.get("warps", []):
            if w["to_map"] in world and (mid, w["to_map"]) not in declared \
                    and mid != w["to_map"]:
                undeclared.append(f"{mid} -> {w['to_map']} (warp '{w['id']}')")
    if sync_fails:
        add("graph-sync", "FAIL", "; ".join(sync_fails[:6]))
    else:
        add("graph-sync", "PASS",
            f"{len(edges)} declared edges all backed by warps where authored")
    if undeclared:
        add("graph-sync", "WARN",
            "authored connections missing from graph.ts: " + "; ".join(sorted(set(undeclared))[:6]))

    # ---- PROGRESSION: the unlock waves ----------------------------------------
    have: set[str] = set()
    reachable = {graph["start_map"]}
    wave_of = {graph["start_map"]: 0}
    wave = 0
    while True:
        grown = True
        while grown:  # expand with current keys
            grown = False
            for e in edges:
                pairs = [(e["from_map"], e["to_map"])]
                if e["bidirectional"]:
                    pairs.append((e["to_map"], e["from_map"]))
                for a, b in pairs:
                    if a not in reachable or b in reachable:
                        continue
                    need = [x for x in (e["requires_ability"], e["requires_flag"]) if x]
                    node_flag = nodes.get(b, {}).get("unlocked_by_flag")
                    if node_flag:
                        need.append(node_flag)
                    if all(k in have for k in need):
                        reachable.add(b)
                        wave_of[b] = wave
                        grown = True
        new_keys = {k for mid in reachable for k in GRANTS.get(mid, [])} - have
        if "flag:hub_unlocked" not in have and \
                {"flag:crown_south", "flag:crown_east", "flag:crown_north",
                 "flag:crown_west"} <= (have | new_keys):
            new_keys.add("flag:hub_unlocked")
        if not new_keys:
            break
        have |= new_keys
        wave += 1

    locked = [n["map_id"] for n in graph["nodes"]
              if n["map_id"] not in reachable
              and nodes[n["map_id"]].get("unlocked_by_flag") not in POSTGAME_FLAGS]
    if locked:
        add("progression", "FAIL",
            f"never unlocks under the canon grant order: {', '.join(locked)}")
    else:
        by_wave = defaultdict(list)
        for mid, wv in wave_of.items():
            by_wave[wv].append(mid)
        add("progression", "PASS",
            f"all {len(reachable)} non-postgame nodes unlock across {wave} waves "
            f"(wave 0 opens {len(by_wave[0])} maps)")

    # ---- LEVEL BANDS across borders --------------------------------------------
    def band(m: dict) -> tuple[int, int] | None:
        lvls = [(t["min_level"], t["max_level"])
                for z in m.get("encounters", []) for t in z.get("table", [])]
        if not lvls:
            return None
        return min(lo for lo, _ in lvls), max(hi for _, hi in lvls)

    cliffs, rows = [], []
    seen_pairs = set()
    for e in edges:
        a, b = e["from_map"], e["to_map"]
        if (a, b) in seen_pairs or (b, a) in seen_pairs:
            continue
        seen_pairs.add((a, b))
        if a not in world or b not in world:
            continue
        ba, bb = band(world[a]), band(world[b])
        if ba is None or bb is None:
            continue
        step = max(bb[0] - ba[1], ba[0] - bb[1])  # gap between the bands
        rows.append(f"{a} {ba[0]}-{ba[1]} ↔ {b} {bb[0]}-{bb[1]}")
        optional = nodes.get(a, {}).get("optional") or nodes.get(b, {}).get("optional")
        if step > 4 and not optional:
            cliffs.append(f"{a} ({ba[0]}-{ba[1]}) ↔ {b} ({bb[0]}-{bb[1]})")
    if cliffs:
        add("level-bands", "WARN",
            "difficulty cliff at border(s): " + "; ".join(cliffs))
    elif rows:
        add("level-bands", "PASS",
            f"{len(rows)} encounter borders step gently (≤4 levels)")

    # ---- TOPOLOGY per region -----------------------------------------------------
    interiors = {mid for mid, m in world.items() if m.get("kind") == "interior"}
    by_region = defaultdict(set)
    for n in graph["nodes"]:
        if n["map_id"] not in interiors:
            by_region[n["region"]].add(n["map_id"])

    # An edge is BACKED once every AUTHORED side carries its warp (unauthored
    # maps get the graph-sync benefit of the doubt). Used by the ring fallback
    # below so a region's circuit only counts when it is actually walkable —
    # e.g. the West's ring closed the day W4 landed the Nightreach hub spoke.
    def edge_backed(e) -> bool:
        src = world.get(e["from_map"])
        if src is not None:
            w = next((w for w in src.get("warps", []) if w["id"] == e["via_warp"]), None)
            if w is None or w["to_map"] != e["to_map"]:
                return False
        if e["bidirectional"] and e["to_map"] in world:
            if not any(w["to_map"] == e["from_map"]
                       for w in world[e["to_map"]].get("warps", [])):
                return False
        return True

    # bridges of the warp-backed overworld graph (an edge NOT on any cycle);
    # a member with a non-bridge edge sits on a real cross-region circuit.
    ring_adj = defaultdict(set)
    for e in edges:
        a, b = e["from_map"], e["to_map"]
        if a in interiors or b in interiors or not edge_backed(e):
            continue
        ring_adj[a].add(b)
        ring_adj[b].add(a)
    disc: dict[str, int] = {}
    low: dict[str, int] = {}
    bridges: set[frozenset] = set()
    counter = [0]

    def find_bridges(root: str) -> None:
        stack = [(root, None, iter(sorted(ring_adj[root])))]
        disc[root] = low[root] = counter[0]
        counter[0] += 1
        while stack:
            node, parent, it = stack[-1]
            advanced = False
            for nxt in it:
                if nxt == parent:
                    continue
                if nxt in disc:
                    low[node] = min(low[node], disc[nxt])
                    continue
                disc[nxt] = low[nxt] = counter[0]
                counter[0] += 1
                stack.append((nxt, node, iter(sorted(ring_adj[nxt]))))
                advanced = True
                break
            if not advanced:
                stack.pop()
                if stack:
                    pnode = stack[-1][0]
                    low[pnode] = min(low[pnode], low[node])
                    if low[node] > disc[pnode]:
                        bridges.add(frozenset((pnode, node)))

    for root in sorted(ring_adj):
        if root not in disc:
            find_bridges(root)

    def on_ring(member: str) -> bool:
        return any(frozenset((member, nb)) not in bridges for nb in ring_adj[member])

    for region, members in sorted(by_region.items()):
        if len(members) < 3:
            continue
        # a region's circuit may close through a GATEWAY outside it (the hub's
        # Lanternway spokes) — include any external node tied to ≥2 members
        touch = defaultdict(set)
        for e in edges:
            a, b = e["from_map"], e["to_map"]
            if a in members and b not in members:
                touch[b].add(a)
            if b in members and a not in members:
                touch[a].add(b)
        extended = members | {n for n, ms in touch.items() if len(ms) >= 2}
        sub = [e for e in edges
               if e["from_map"] in extended and e["to_map"] in extended
               and (e["from_map"] in members or e["to_map"] in members)]
        # components among members touched by sub-edges
        adj = defaultdict(set)
        for e in sub:
            adj[e["from_map"]].add(e["to_map"])
            adj[e["to_map"]].add(e["from_map"])
        comp = 0
        seen: set[str] = set()
        for mname in extended:
            if mname in seen or mname not in adj:
                continue
            comp += 1
            stack = [mname]
            while stack:
                cur = stack.pop()
                if cur in seen:
                    continue
                seen.add(cur)
                stack.extend(adj[cur])
        pairs = {frozenset((e["from_map"], e["to_map"])) for e in sub}
        cycles = len(pairs) - len(seen) + comp
        if cycles > 0:
            add("topology", "PASS",
                f"region '{region}': {len(members)} nodes, {cycles} loop(s)")
        else:
            # the ring fallback: no internal loop, but a member may sit on a
            # WARP-BACKED circuit that closes beyond the region's border (the
            # Lanternway ring — e.g. nightreach -> crossroads -> coldfog I/II
            # -> nightreach). That is §2b r1's "close through the hub" shape;
            # it only counts once every authored side has its warp.
            riders = sorted(mname for mname in members if on_ring(mname))
            if riders:
                add("topology", "PASS",
                    f"region '{region}': {len(members)} nodes, circuit closes "
                    f"through the outer ring via {', '.join(riders)}")
            else:
                add("topology", "WARN",
                    f"region '{region}' is a pure corridor ({len(members)} nodes, no "
                    f"loop) — plan a late shortcut/spur re-link (§3a rule 1 at scene scale)")

    # ---- TRAVEL: door-to-door length of each authored route ----------------------
    lengths = []
    for mid, m in sorted(world.items()):
        if m.get("kind") not in ("route", "cave"):
            continue
        mm = MapModel(m)
        ports = [p for p in mm.portals() if p["stand"]]
        best = 0
        for i in range(len(ports)):
            d = mm.bfs(ports[i]["stand"], abilities=set(ALL_ABILITIES))
            for j in range(len(ports)):
                if i != j:
                    ds = [d[t] for t in ports[j]["stand"] if t in d]
                    if ds:
                        best = max(best, min(ds))
        if best:
            lengths.append(f"{mid} ≈{best} steps")
    if lengths:
        add("travel", "INFO", "route legs door-to-door: " + "; ".join(lengths))

    # ---- output -------------------------------------------------------------------
    failed = any(c["status"] == "FAIL" for c in checks)
    if as_json:
        print(json.dumps({"checks": checks, "passed": not failed}, indent=2))
    else:
        icon = {"PASS": "✓", "WARN": "!", "FAIL": "✗", "INFO": "·"}
        print(f"Region audit — {len(world)} authored maps, "
              f"{len(graph['nodes'])} graph nodes\n")
        for c in checks:
            print(f"  [{icon[c['status']]}] {c['check']:<12} {c['detail']}")
        n_fail = sum(c["status"] == "FAIL" for c in checks)
        n_warn = sum(c["status"] == "WARN" for c in checks)
        print(f"\n{'FAIL' if failed else 'PASS'} — {n_fail} failure(s), {n_warn} warning(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
