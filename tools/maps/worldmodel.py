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
"""
from __future__ import annotations

import json
import re
from collections import deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS_DIR = REPO / "public/assets/maps"
TILESETS_DIR = REPO / "public/assets/tilesets"
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
            top = o["at"]["ty"] + (o.get("overhang", 0) if o.get("walk_under") else 0)
            for ty in range(top, o["at"]["ty"] + o["h"]):
                for tx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
                    if 0 <= tx < self.w and 0 <= ty < self.h:
                        self.solid[ty * self.w + tx] = True

        # AbilityGate rects flip their tiles to gated-walkable
        for g in m.get("gates", []):
            if g.get("effect") in ("make_passable", "remove_tile") and "rect" in g:
                r = g["rect"]
                for ty in range(r["ty"], r["ty"] + r["h"]):
                    for tx in range(r["tx"], r["tx"] + r["w"]):
                        if 0 <= tx < self.w and 0 <= ty < self.h:
                            i = ty * self.w + tx
                            self.solid[i] = False
                            self.ability[i] = g.get("ability")

        # NPC bodies (dedupe flag-pair swaps sharing an anchor). Static bodies
        # are deliberate geometry (the gate-warden pattern); wanderers move, so
        # they never count as walls. Reach checks pass through ALL of them.
        self.npc_tiles: set[tuple[int, int]] = set()
        self.static_npc_tiles: set[tuple[int, int]] = set()
        for npc in m.get("npcs", []):
            at = (npc["at"]["tx"], npc["at"]["ty"])
            self.npc_tiles.add(at)
            if npc.get("movement", "static") == "static":
                self.static_npc_tiles.add(at)

        self.warps = m.get("warps", [])
        self.triggers = m.get("triggers", [])
        self.npcs = m.get("npcs", [])

    # ---- cells -------------------------------------------------------------
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def standable(self, x: int, y: int, *, abilities: set[str] | None = None,
                  npc_block: set[tuple[int, int]] | None = None) -> bool:
        """Can the player occupy this tile? Ledges are hopped, never stood on."""
        if not self.in_bounds(x, y):
            return False
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
        """Directed moves out of (x,y): plain steps + ledge hops."""
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
