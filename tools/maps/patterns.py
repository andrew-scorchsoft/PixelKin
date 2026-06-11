#!/usr/bin/env python3
"""
patterns — parametric map STAMPS on top of mapkit (quality baked in, lines out).

Each stamp encodes a binding design rule from docs/world/level-design.md /
the walkthrough spine's standing kit, so a builder applies the rule instead of
re-deriving it. The goal: a route builder reads as a list of *decisions*
("a grass band here, a trainer beat there, a ledge shortcut down this terrace"),
not coordinate bookkeeping.

What the stamps return matters: content stamps (trainer_beat, cache, sign)
APPEND the placements to the map dict and RETURN the registry refs the author
still owes (scripts/dialogue/trainers are TypeScript registries this tool can't
write). Print them at build time; the build isn't done until they exist.

Encounter zones come FROM THE PAINT: `zones_from_grid` turns each connected
painted blob into a loose bounding-box zone — safe because the engine only
fires tile-bound terrains (tall_grass/water) ON matching painted tiles
(EncounterSystem.TILE_BOUND). No more hand-measured rects drifting from art.
"""
from __future__ import annotations
import json
import random
from pathlib import Path
from mapkit import gid

Facing = str  # 'up' | 'down' | 'left' | 'right'

_REPO = Path(__file__).resolve().parents[2]
_OBJECTS = json.loads(
    (_REPO / "public/assets/sprites/objects/objects.manifest.json").read_text())["objects"]


# ---- areas: name a region of the map, apply things to it ------------------------
class Area:
    """A named rect handle — 'define an area and apply patterns to it'."""

    def __init__(self, x0: int, y0: int, x1: int, y1: int):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1

    def inset(self, n: int = 1) -> "Area":
        return Area(self.x0 + n, self.y0 + n, self.x1 - n, self.y1 - n)

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2

    def cells(self):
        for y in range(self.y0, self.y1 + 1):
            for x in range(self.x0, self.x1 + 1):
                yield x, y


# ---- encounter zones from the paint ---------------------------------------------
def zones_from_grid(grid, w: int, h: int, *, terrain: str, rate: float, table,
                    id_prefix: str = "zone", min_cells: int = 4) -> list[dict]:
    """Connected painted blobs -> one EncounterZone (bounding box) each.

    The rect may loosely cover unpainted cells — the engine only rolls
    tile-bound terrains on painted tiles, so the paint stays the truth. Blobs
    under `min_cells` are merged into their nearest big sibling's box (stray
    tufts shouldn't make confetti zones)."""
    seen = [False] * (w * h)
    blobs: list[list[tuple[int, int]]] = []
    for sy in range(h):
        for sx in range(w):
            i = sy * w + sx
            if not grid[i] or seen[i]:
                continue
            stack, cells = [(sx, sy)], []
            seen[i] = True
            while stack:
                x, y = stack.pop()
                cells.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    j = ny * w + nx
                    if 0 <= nx < w and 0 <= ny < h and grid[j] and not seen[j]:
                        seen[j] = True
                        stack.append((nx, ny))
            blobs.append(cells)

    big = [b for b in blobs if len(b) >= min_cells]
    small = [b for b in blobs if len(b) < min_cells]
    # fold each small blob into the nearest big one's box
    for s in small:
        if not big:
            big.append(s)
            continue
        sx = sum(c[0] for c in s) / len(s)
        sy = sum(c[1] for c in s) / len(s)
        nearest = min(big, key=lambda b: (sum(c[0] for c in b) / len(b) - sx) ** 2 +
                                         (sum(c[1] for c in b) / len(b) - sy) ** 2)
        nearest.extend(s)

    zones = []
    for n, cells in enumerate(big):
        xs = [c[0] for c in cells]
        ys = [c[1] for c in cells]
        zones.append({
            "id": f"{id_prefix}_{chr(ord('a') + n)}",
            "terrain": terrain,
            "rect": {"tx": min(xs), "ty": min(ys),
                     "w": max(xs) - min(xs) + 1, "h": max(ys) - min(ys) + 1},
            "encounter_rate": rate,
            "table": table,
        })
    return zones


# ---- ledges & terraces ------------------------------------------------------------
def ledge_run(deco, w: int, h: int, y: int, x0: int, x1: int,
              rng: random.Random | None = None) -> None:
    """A south-hop ledge line (one-way shortcut down). Variants scattered so the
    lip doesn't read as a ruled line. Leave a GAP in the run where the long way
    round comes back up — a ledge with no gap is a wall with extra steps."""
    rng = rng or random.Random(0)
    tiles = [gid("grass_ledge_s"), gid("grass_ledge_s_v1")]
    for x in range(x0, x1 + 1):
        deco[y * w + x] = rng.choice(tiles)


def terrace(cliff_grid, deco, w: int, h: int, area: Area, *,
            gap: tuple[int, int], gap_side: Facing = "up", rim: int = 2,
            rng: random.Random | None = None) -> None:
    """A WALKABLE raised bank — the classic route-depth shape: walk the long
    way up and in through the `gap`, explore the shelf, hop the south LEDGE
    back down. Built as a cliff RIM (`rim` deep — every cliff tile collides)
    around `area`'s north/west/east sides, the south row replaced by a
    one-way ledge line, the interior left open ground. `gap` = the open
    columns (gap_side 'up') or rows ('left'/'right') where the route climbs in."""
    for d in range(rim):
        for x in range(area.x0, area.x1 + 1):
            cliff_grid[(area.y0 + d) * w + x] = 1  # north rim
        for y in range(area.y0, area.y1):
            cliff_grid[y * w + (area.x0 + d)] = 1  # west rim
            cliff_grid[y * w + (area.x1 - d)] = 1  # east rim
    ledge_run(deco, w, h, area.y1, area.x0 + rim, area.x1 - rim, rng)
    if gap_side == "up":
        for x in range(gap[0], gap[1] + 1):
            for d in range(rim):
                cliff_grid[(area.y0 + d) * w + x] = 0
    elif gap_side == "left":
        for y in range(gap[0], gap[1] + 1):
            for d in range(rim):
                cliff_grid[y * w + (area.x0 + d)] = 0
    elif gap_side == "right":
        for y in range(gap[0], gap[1] + 1):
            for d in range(rim):
                cliff_grid[y * w + (area.x1 - d)] = 0
    else:  # 'down' — an opening in the ledge itself
        for x in range(gap[0], gap[1] + 1):
            deco[area.y1 * w + x] = 0


# ---- content stamps (append placements, return the refs you owe) ------------------
def trainer_beat(m: dict, *, tid: str, at: tuple[int, int], facing: Facing,
                 sight: int = 4, sprite: str = "npc_man",
                 after_movement: str = "look_around") -> list[str]:
    """A SIGHT-trainer beat (spine kit): the challenge NPC + its beaten swap,
    wired to the standing flag/script conventions. Post them in a corridor's
    end row facing down their column so the crossing is unavoidable.
    Returns the registry refs the author must create:
      script.<tid> (scripts.ts: say -> battle -> say -> setFlag)
      npc.<tid>_after (dialogue.ts), and TRAINERS[<tid>] (trainers.ts, payout
      = class rate x ace per 10-economy §4)."""
    flag = f"flag:{tid}_beaten"
    m.setdefault("npcs", []).extend([
        {"id": tid, "at": {"tx": at[0], "ty": at[1]}, "facing": facing,
         "sprite": sprite, "movement": "static",
         "dialogue_ref": f"script.{tid}",
         "sight_range": sight, "defeated_flag": flag,
         "hidden_when_flag": flag},
        {"id": f"{tid}_after", "at": {"tx": at[0], "ty": at[1]}, "facing": facing,
         "sprite": sprite, "movement": after_movement,
         "dialogue_ref": f"npc.{tid}_after",
         "requires_flag": flag},
    ])
    return [f"script.{tid}", f"npc.{tid}_after", f"TRAINERS[{tid!r}]"]


def cache(m: dict, *, cid: str, at: tuple[int, int]) -> list[str]:
    """An item cache (spine kit + the cache-variety rule: per map mix
    consumables with ONE valuable and/or a loose-wicks find; the better ones
    off the lane). Returns the script ref the author must create:
      script.pickup_<cid> (give -> say the find -> setFlag flag:picked_<cid>)."""
    m.setdefault("npcs", []).append(
        {"id": f"cache_{cid}", "at": {"tx": at[0], "ty": at[1]}, "facing": "down",
         "sprite": "item_cache", "movement": "static",
         "dialogue_ref": f"script.pickup_{cid}",
         "hidden_when_flag": f"flag:picked_{cid}"})
    return [f"script.pickup_{cid}"]


def sign(m: dict, deco, w: int, *, sid: str, at: tuple[int, int]) -> list[str]:
    """A reading sign: the deco tile + its interact trigger.
    Returns the dialogue ref to author: sign.<sid>."""
    deco[at[1] * w + at[0]] = gid("sign")
    m.setdefault("triggers", []).append(
        {"id": f"sign_{sid}", "kind": "sign", "at": {"tx": at[0], "ty": at[1]},
         "activation": "interact", "ref": f"sign.{sid}"})
    return [f"sign.{sid}"]


def building(m: dict, path_grid, w: int, h: int, *, oid: str, sprite: str,
             at: tuple[int, int], overhang: int, door_col: int | None = None,
             to_map: str | None = None, to: tuple[int, int] = (0, 0),
             apron_rows: int = 2) -> tuple[int, int]:
    """A whole-object STRUCTURE (art-style §14b + level-design §11 rule 5):
    the building object (footprint from the objects manifest — no hand-typed
    w/h), its door warp into `to_map` (landing `to`, paired by the interior's
    builder), and a path APRON carved `apron_rows` deep below the door so the
    building sits in a town, not on a field. Returns the door's approach tile
    (one row below the door) for lanes/NPCs to aim at."""
    spec = _OBJECTS[sprite]
    tw, th = spec["tw"], spec["th"]
    dc = door_col if door_col is not None else tw // 2
    door = (at[0] + dc, at[1] + th - 1)
    approach = (door[0], door[1] + 1)
    m.setdefault("objects", []).append(
        {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]},
         "w": tw, "h": th, "overhang": overhang})
    if to_map:
        m.setdefault("warps", []).append(
            {"id": f"enter_{oid}", "at": {"tx": door[0], "ty": door[1]},
             "trigger": "interact", "to_map": to_map,
             "to": {"tx": to[0], "ty": to[1]}, "facing": "up", "transition": "door"})
    if path_grid is not None:
        for dy in range(apron_rows):
            for x in range(at[0], at[0] + tw):
                y = approach[1] + dy
                if 0 <= x < w and 0 <= y < h:
                    path_grid[y * w + x] = 1
    return approach


def crown_tree(m: dict, *, oid: str, sprite: str, at: tuple[int, int],
               overhang: int | None = None) -> None:
    """A walk-under crown tree object (footprint + overhang from the manifest;
    §11 rule 2: borders and big trees are OBJECTS with real shape, not tiles)."""
    spec = _OBJECTS[sprite]
    m.setdefault("objects", []).append(
        {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]},
         "w": spec["tw"], "h": spec["th"],
         "overhang": overhang if overhang is not None else max(1, spec["th"] - 1),
         "walk_under": True})


def report(owed: list[str]) -> None:
    """Print the registry entries this map still owes (call from the builder)."""
    print("content refs owed by this map (register in src/game/content/):")
    for ref in owed:
        print(f"  - {ref}")
