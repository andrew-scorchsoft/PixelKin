#!/usr/bin/env python3
"""
worldmodel — the shared movement/portal model behind the flow + region audits.

audit_warps.py answers "do the doors line up?"; the flow/region audits answer
"does the LEVEL play?" — and both need the same primitives: a per-map walkable
grid that understands tile collision, ability gates, one-way LEDGES, object
footprints and NPC bodies; warp tiles grouped into PORTALS (a wide entrance is
one logical door); BFS/shortest-path over the directed movement graph with
arbitrary avoid-sets; trainer SIGHT-LINE projection; and a regex parser for the
world graph in src/game/data/world/graph.ts.

Movement semantics mirror the engine (CollisionGrid/Player):
  * 4-directional, tile-to-tile; `above` layers never collide.
  * A tile with `requires_ability` is walkable only when that gift is held.
  * A `ledge` tile is hopped, never stood on: moving in its direction from the
    tile before it lands on the tile beyond it (one directed edge).
  * NPCs block their anchor tile (flag-pair swaps share a tile — dedupe).
  * THE TRAVERSAL KIT (2026-10, mirror of src/game/systems/world/Traversal.ts):
    `flows` (slope/rail: carried `dir`, never entered or left uphill, a slope
    steers left/right; ice: a step onto ice slides on to its stop — modelled as
    one macro move), `spans` (a deck tile is stood on regardless of its own
    collision and walked along its axis only; `under` lets you pass beneath it
    across the axis in one move), `jumps` (riders clear `length` tiles; a `ride`
    map is assumed ridden — its rental gate is the content's job). A lever-
    switched flow (`requires_flag`/`hidden_when_flag`) is modelled in BOTH
    switch states (the union), so reach reflects every lever setting.
"""
from __future__ import annotations

import json
import re
from collections import deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS_DIR = REPO / "public/assets/maps"
TILESETS_DIR = REPO / "public/assets/tilesets"
WALK_BEHIND_ROWS: dict[str, int] = json.loads(
    (REPO / "src/game/data/world/walk-behind.json").read_text())["rows"]


def solid_top(o: dict) -> int:
    """First footprint row that collides (mirror of CollisionGrid): walk-under
    objects free their overhang; buildings free their walk-behind roof peak."""
    ov = o.get("overhang", 0) or 0
    if o.get("walk_under"):
        return o["at"]["ty"] + ov
    return o["at"]["ty"] + min(WALK_BEHIND_ROWS.get(o.get("sprite", ""), 0), ov)
GRAPH_TS = REPO / "src/game/data/world/graph.ts"

DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
LEDGE_DIR = {"down": (0, 1), "up": (0, -1), "left": (-1, 0), "right": (1, 0),
             "s": (0, 1), "n": (0, -1), "w": (-1, 0), "e": (1, 0)}


def load_world() -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text()) for p in sorted(MAPS_DIR.glob("*.json"))}


class MapModel:
    """Movement + content model for one map JSON."""

    def __init__(self, m: dict):
        self.m = m
        self.id = m["id"]
        self.kind = m.get("kind", "")
        self.w, self.h = m["width"], m["height"]
        n = self.w * self.h
        self.solid = [False] * n
        self.ability = [None] * n      # requires_ability on a colliding tile
        self.ledge = [None] * n        # hop direction name, or None
        self.encounter = [False] * n   # encounter_terrain painted here

        sets = []
        for ts in m.get("tilesets", []):
            side = TILESETS_DIR / f"{ts['name']}.tileset.json"
            if not side.is_file():
                continue
            data = json.loads(side.read_text())
            tiles = {t.get("index", i): t for i, t in enumerate(data.get("tiles", []))}
            sets.append((ts.get("first_gid", 1), tiles))
        sets.sort(key=lambda s: -s[0])

        def meta(gid: int) -> dict:
            for first, tiles in sets:
                if gid >= first:
                    return tiles.get(gid - first, {})
            return {}

        for layer in m.get("layers", []):
            if layer.get("role") in ("above", "terrain"):
                continue
            for i, gid in enumerate(layer.get("data", [])):
                if not gid:
                    continue
                t = meta(gid)
                if t.get("ledge"):
                    self.ledge[i] = t["ledge"]
                if t.get("collides"):
                    if t.get("requires_ability"):
                        self.ability[i] = t["requires_ability"]
                    else:
                        self.solid[i] = True
                if t.get("encounter_terrain"):
                    self.encounter[i] = True

        # whole-object footprints block (walk-under overhang rows excepted)
        for o in m.get("objects", []):
            if o.get("solid") is False:
                continue
            top = solid_top(o)
            for ty in range(top, o["at"]["ty"] + o["h"]):
                for tx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
                    if 0 <= tx < self.w and 0 <= ty < self.h:
                        self.solid[ty * self.w + tx] = True

        # Doorways are WALK-ONTO: a transition:'door' warp frees its tile so the
        # player can step into the doorway even though it sits in a building's
        # footprint (mirror of CollisionGrid). Runs after the object loop so it
        # overrides the footprint — without it the audit thinks a step_on door is
        # an unreachable solid tile.
        for wp in m.get("warps", []):
            if wp.get("transition") == "door":
                at = wp["at"]
                if 0 <= at["tx"] < self.w and 0 <= at["ty"] < self.h:
                    self.solid[at["ty"] * self.w + at["tx"]] = False

        # AbilityGate rects flip their tiles to gated-walkable
        for g in m.get("gates", []):
            if g.get("effect") in ("make_passable", "remove_tile") and "rect" in g:
                r = g["rect"]
                for ty in range(r["ty"], r["ty"] + r["h"]):
                    for tx in range(r["tx"], r["tx"] + r["w"]):
                        if 0 <= tx < self.w and 0 <= ty < self.h:
                            i = ty * self.w + tx
                            if self.ability[i] == "deepdive":
                                continue   # a gate never softens DEEP water (CollisionGrid)
                            self.solid[i] = False
                            self.ability[i] = g.get("ability")

        # NPC bodies (dedupe flag-pair swaps sharing an anchor). Static bodies
        # are deliberate geometry (the gate-warden pattern); wanderers move, so
        # they never count as walls. Reach checks pass through ALL of them.
        # AMBIENT placements (`ambient: true` — grazing kin, WP0 world-craft) are
        # set dressing the engine never collides with or talks to, so the model
        # drops them entirely: never blockers, never "content" to reach.
        self.npc_tiles: set[tuple[int, int]] = set()
        self.static_npc_tiles: set[tuple[int, int]] = set()
        live_npcs = [n for n in m.get("npcs", []) if not n.get("ambient")]
        self.ambient_npcs = [n for n in m.get("npcs", []) if n.get("ambient")]
        for npc in live_npcs:
            at = (npc["at"]["tx"], npc["at"]["ty"])
            self.npc_tiles.add(at)
            if npc.get("movement", "static") == "static":
                self.static_npc_tiles.add(at)

        self.warps = m.get("warps", [])
        self.triggers = m.get("triggers", [])
        self.npcs = live_npcs

        # ---- the traversal kit (Traversal.ts) ----
        self.flows = m.get("flows", []) or []
        self.spans = m.get("spans", []) or []
        self.jumps = {(j["at"]["tx"], j["at"]["ty"]): j for j in (m.get("jumps", []) or [])}
        self.riding = bool(m.get("ride"))
        self.kit = bool(self.flows or self.spans or self.jumps)
        self._flow_tiles = []
        for f in self.flows:
            cells = set()
            r = f.get("rect")
            if r:
                cells |= {(x, y) for y in range(r["ty"], r["ty"] + r["h"])
                          for x in range(r["tx"], r["tx"] + r["w"])}
            cells |= {(t["tx"], t["ty"]) for t in f.get("tiles", []) or []}
            self._flow_tiles.append((f, cells))
        self._span_at = {}
        for sp in self.spans:
            r = sp["rect"]
            for y in range(r["ty"], r["ty"] + r["h"]):
                for x in range(r["tx"], r["tx"] + r["w"]):
                    self._span_at.setdefault((x, y), sp)
        # switch states to model: unconditional only, or every switch thrown
        self._states = [False, True] if any(
            f.get("requires_flag") or f.get("hidden_when_flag") for f in self.flows) else [False]

    @property
    def one_way(self) -> bool:
        """Any one-way feature: ledges, chutes, rails or ramps."""
        return any(self.ledge) or any(f.get("kind") in ("slope", "rail") for f in self.flows) \
            or bool(self.jumps)

    # ---- traversal kit helpers --------------------------------------------
    def flow_at(self, x: int, y: int, thrown: bool = False):
        for f, cells in reversed(self._flow_tiles):
            if (x, y) not in cells:
                continue
            if f.get("requires_flag") and not thrown:
                continue
            if f.get("hidden_when_flag") and thrown:
                continue
            return f
        return None

    def span_at(self, x: int, y: int):
        return self._span_at.get((x, y))

    @staticmethod
    def _along(sp, dx, dy) -> bool:
        return (dy == 0) if sp["axis"] == "h" else (dx == 0)

    def _ground_open(self, x, y, abilities, npc_block) -> bool:
        if not self.in_bounds(x, y):
            return False
        i = y * self.w + x
        if self.solid[i] or self.ledge[i]:
            return False
        if self.ability[i] is not None and self.ability[i] not in (abilities or set()):
            return False
        return not (npc_block and (x, y) in npc_block)

    def _enterable(self, x, y, dx, dy, abilities, npc_block, thrown) -> bool:
        if not self.in_bounds(x, y):
            return False
        f = self.flow_at(x, y, thrown)
        if f and f.get("kind") != "ice" and LEDGE_DIR.get(f.get("dir")) == (-dx, -dy):
            return False
        sp = self.span_at(x, y)
        if sp:
            return self._along(sp, dx, dy) and not (npc_block and (x, y) in npc_block)
        return self._ground_open(x, y, abilities, npc_block)

    def _plan(self, x, y, dx, dy, abilities, npc_block, thrown):
        """Traversal.plan: the tile a press toward (dx,dy) ends on, or None."""
        here = self.span_at(x, y)
        if here and not self._along(here, dx, dy):
            return None
        fh = self.flow_at(x, y, thrown)
        if fh and fh.get("kind") != "ice" and LEDGE_DIR.get(fh.get("dir")) == (-dx, -dy):
            return None
        tx, ty = x + dx, y + dy
        j = self.jumps.get((tx, ty)) if self.riding else None
        if j and LEDGE_DIR.get(j["dir"]) == (dx, dy):
            n = j.get("length", 3)
            lx, ly = tx + dx * (n - 1), ty + dy * (n - 1)
            if self._enterable(lx, ly, dx, dy, abilities, npc_block, thrown):
                return lx, ly
        sp = self.span_at(tx, ty)
        if sp:
            if self._along(sp, dx, dy):
                return None if (npc_block and (tx, ty) in npc_block) else (tx, ty)
            if not sp.get("under"):
                return None
            cx, cy = tx, ty
            while True:
                s2 = self.span_at(cx, cy)
                if not (s2 and s2.get("under") and not self._along(s2, dx, dy)):
                    break
                if not self._ground_open(cx, cy, abilities, npc_block):
                    return None
                cx, cy = cx + dx, cy + dy
            if self.span_at(cx, cy) or not self._enterable(cx, cy, dx, dy, abilities, npc_block, thrown):
                return None
            return cx, cy
        if not self._enterable(tx, ty, dx, dy, abilities, npc_block, thrown):
            return None
        return tx, ty

    def _slide(self, x, y, dx, dy, abilities, npc_block, thrown):
        """Glare ice: from a tile just stepped onto, slide on to where it stops."""
        seen = set()
        while self.flow_at(x, y, thrown) and self.flow_at(x, y, thrown).get("kind") == "ice":
            if (x, y) in seen:
                break
            seen.add((x, y))
            nxt = self._plan(x, y, dx, dy, abilities, npc_block, thrown)
            if nxt is None:
                break
            x, y = nxt
        return x, y

    def _kit_moves(self, x, y, abilities, npc_block):
        out = set()
        for thrown in self._states:
            def go(dx, dy):
                t = self._plan(x, y, dx, dy, abilities, npc_block, thrown)
                if t is None:
                    # a blocked press may still be a ledge hop
                    lx, ly = x + dx, y + dy
                    if self.in_bounds(lx, ly) and self.ledge[ly * self.w + lx] \
                            and LEDGE_DIR.get(self.ledge[ly * self.w + lx]) == (dx, dy) \
                            and self._ground_open(lx + dx, ly + dy, abilities, npc_block):
                        return lx + dx, ly + dy
                    return None
                if t != (x + dx, y + dy) and abs(t[0] - x) + abs(t[1] - y) > 1:
                    return t      # a leap / underpass lands where it lands
                return self._slide(t[0], t[1], dx, dy, abilities, npc_block, thrown)

            f = self.flow_at(x, y, thrown)
            if f and f.get("kind") in ("slope", "rail") and f.get("dir") in LEDGE_DIR:
                cdx, cdy = LEDGE_DIR[f["dir"]]
                carried = go(cdx, cdy)
                if carried is not None:
                    out.add(carried)
                    if f["kind"] == "slope":
                        for sdx, sdy in ((cdy, cdx), (-cdy, -cdx)):
                            t = go(sdx, sdy)
                            if t is not None:
                                out.add(t)
                    continue
            for dx, dy in DIRS.values():
                t = go(dx, dy)
                if t is not None:
                    out.add(t)
        return out

    # ---- cells -------------------------------------------------------------
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def standable(self, x: int, y: int, *, abilities: set[str] | None = None,
                  npc_block: set[tuple[int, int]] | None = None) -> bool:
        """Can the player occupy this tile? Ledges are hopped, never stood on."""
        if not self.in_bounds(x, y):
            return False
        if self.kit and (x, y) in self._span_at:
            return not (npc_block and (x, y) in npc_block)   # a deck ignores what's under it
        i = y * self.w + x
        if self.solid[i] or self.ledge[i]:
            return False
        if self.ability[i] is not None and self.ability[i] not in (abilities or set()):
            return False
        if npc_block and (x, y) in npc_block:
            return False
        return True

    def moves_from(self, x: int, y: int, *, abilities: set[str] | None = None,
                   npc_block: set[tuple[int, int]] | None = None):
        """Directed moves out of (x,y): plain steps + ledge hops (+ the kit)."""
        if self.kit:
            yield from self._kit_moves(x, y, abilities, npc_block)
            return
        for dname, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if not self.in_bounds(nx, ny):
                continue
            li = ny * self.w + nx
            ld = self.ledge[li]
            if ld is not None:
                # hop over the ledge tile iff we approach in its direction
                if LEDGE_DIR.get(ld) == (dx, dy):
                    lx, ly = nx + dx, ny + dy
                    if self.standable(lx, ly, abilities=abilities,
                                      npc_block=npc_block):
                        yield lx, ly
                continue
            if self.standable(nx, ny, abilities=abilities, npc_block=npc_block):
                yield nx, ny

    # ---- search ------------------------------------------------------------
    def bfs(self, starts, *, abilities: set[str] | None = None,
            avoid: set[tuple[int, int]] | None = None,
            npc_block: set[tuple[int, int]] | None = None) -> dict[tuple[int, int], int]:
        """Distance map from `starts` over the directed movement graph.
        `avoid` cells can be stood on as a START but never entered."""
        avoid = avoid or set()
        dist: dict[tuple[int, int], int] = {}
        q = deque()
        for s in starts:
            if self.standable(*s, abilities=abilities, npc_block=npc_block):
                dist[s] = 0
                q.append(s)
        while q:
            x, y = q.popleft()
            d = dist[(x, y)]
            for nxt in self.moves_from(x, y, abilities=abilities,
                                       npc_block=npc_block):
                if nxt in dist or nxt in avoid:
                    continue
                dist[nxt] = d + 1
                q.append(nxt)
        return dist

    def path(self, starts, goals, *, abilities: set[str] | None = None,
             avoid: set[tuple[int, int]] | None = None,
             npc_block: set[tuple[int, int]] | None = None) -> list[tuple[int, int]] | None:
        """One shortest path from any start to any goal, or None."""
        avoid = avoid or set()
        goals = set(goals)
        prev: dict[tuple[int, int], tuple[int, int] | None] = {}
        q = deque()
        for s in starts:
            if self.standable(*s, abilities=abilities, npc_block=npc_block):
                prev[s] = None
                q.append(s)
        while q:
            cur = q.popleft()
            if cur in goals:
                out = []
                node: tuple[int, int] | None = cur
                while node is not None:
                    out.append(node)
                    node = prev[node]
                return out[::-1]
            for nxt in self.moves_from(*cur, abilities=abilities,
                                       npc_block=npc_block):
                if nxt in prev or nxt in avoid:
                    continue
                prev[nxt] = cur
                q.append(nxt)
        return None

    # ---- portals -----------------------------------------------------------
    def portals(self) -> list[dict]:
        """Warps grouped into logical doors: same target map + adjacent tiles.
        Returns [{'to_map', 'ids', 'tiles', 'stand'}] where `stand` is the set
        of standable tiles a player occupies when using the portal (the warp
        tiles themselves for step_on; the facing-approach tile for interact)."""
        groups: list[dict] = []
        for wp in self.warps:
            at = (wp["at"]["tx"], wp["at"]["ty"])
            placed = False
            for g in groups:
                if g["to_map"] == wp["to_map"] and any(
                        abs(at[0] - t[0]) <= 1 and abs(at[1] - t[1]) <= 1
                        for t in g["tiles"]):
                    g["tiles"].add(at)
                    g["ids"].append(wp["id"])
                    g["warps"].append(wp)
                    placed = True
                    break
            if not placed:
                groups.append({"to_map": wp["to_map"], "ids": [wp["id"]],
                               "tiles": {at}, "warps": [wp]})
        for g in groups:
            stand = set()
            for wp in g["warps"]:
                at = (wp["at"]["tx"], wp["at"]["ty"])
                if wp.get("trigger") == "interact":
                    # player stands beside an interact warp (a door tile)
                    for dx, dy in DIRS.values():
                        n = (at[0] + dx, at[1] + dy)
                        if self.standable(*n, abilities=set(ALL_ABILITIES),
                                          npc_block=None):
                            stand.add(n)
                else:
                    stand.add(at)
            g["stand"] = stand
        return groups

    # ---- trainer sight -----------------------------------------------------
    def sight_tiles(self) -> dict[str, set[tuple[int, int]]]:
        """Per sight-trainer: the tiles their straight-ahead look covers
        (stopped by solid ground, like the engine's line check)."""
        out: dict[str, set[tuple[int, int]]] = {}
        for npc in self.npcs:
            rng = npc.get("sight_range")
            if not rng:
                continue
            dx, dy = DIRS.get(npc.get("facing", "down"), (0, 1))
            tiles = set()
            x, y = npc["at"]["tx"], npc["at"]["ty"]
            for _ in range(rng):
                x, y = x + dx, y + dy
                if not self.in_bounds(x, y) or self.solid[y * self.w + x]:
                    break
                tiles.add((x, y))
            out[npc["id"]] = tiles
        return out


ALL_ABILITIES = ("tidecall", "glimmerstep", "updraft_kite",
                 "emberward", "sunsketch", "starreach")


# ---- graph.ts parser ----------------------------------------------------------
_NODE_RE = re.compile(r"\{\s*map_id:\s*'([^']+)',\s*region:\s*'([^']+)'([^}]*)\}")
_EDGE_RE = re.compile(
    r"\{\s*from_map:\s*'([^']+)',\s*to_map:\s*'([^']+)',\s*via_warp:\s*'([^']+)'([^}]*)\}")


def parse_graph() -> dict:
    """Nodes/edges/hub out of graph.ts (the regular literal in VESPERHOLM_GRAPH)."""
    src = GRAPH_TS.read_text()
    nodes = []
    for mid, region, rest in _NODE_RE.findall(src):
        nodes.append({
            "map_id": mid, "region": region,
            "optional": "optional: true" in rest,
            "unlocked_by_flag": (re.search(r"unlocked_by_flag:\s*'([^']+)'", rest) or
                                 [None, None])[1],
        })
    edges = []
    for frm, to, via, rest in _EDGE_RE.findall(src):
        edges.append({
            "from_map": frm, "to_map": to, "via_warp": via,
            "requires_ability": (re.search(r"requires_ability:\s*'([^']+)'", rest) or
                                 [None, None])[1],
            "requires_flag": (re.search(r"requires_flag:\s*'([^']+)'", rest) or
                              [None, None])[1],
            "bidirectional": "bidirectional: true" in rest,
        })
    start = re.search(r"start_map:\s*'([^']+)'", src)
    start_at = re.search(r"start_at:\s*\{\s*tx:\s*(\d+),\s*ty:\s*(\d+)", src)
    return {"nodes": nodes, "edges": edges,
            "start_map": start.group(1) if start else None,
            "start_at": ({"tx": int(start_at.group(1)), "ty": int(start_at.group(2))}
                         if start_at else None)}
