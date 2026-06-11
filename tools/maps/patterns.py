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
              rng: random.Random | None = None, family: str = "grass") -> None:
    """A south-hop ledge line (one-way shortcut down). Variants scattered so the
    lip doesn't read as a ruled line. `family` picks the context-correct art
    ('grass' on green, 'sand' = the dune bank on flats — §11 rule 8). Leave a
    GAP in the run where the long way round comes back up — a ledge with no gap
    is a wall with extra steps."""
    rng = rng or random.Random(0)
    tiles = [gid(f"{family}_ledge_s"), gid(f"{family}_ledge_s_v1")]
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
        # Doors are WALK-ONTO (step_on): the player steps into the doorway tile and
        # warps — the genre convention (level-design §11 rule 5b). The engine frees
        # this tile in collision (CollisionGrid frees `transition:'door'` warp tiles)
        # so it's reachable inside the building footprint, and a Confirm press at it
        # works too. A locked door carries requires_*/blocked_ref and answers a
        # walk-in with its "it's locked" line.
        m.setdefault("warps", []).append(
            {"id": f"enter_{oid}", "at": {"tx": door[0], "ty": door[1]},
             "trigger": "step_on", "to_map": to_map,
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


def gift_tease(m: dict, deco, w: int, *, wid: str, at: tuple[int, int],
               ability: str, to_map: str, to: tuple[int, int],
               trigger: str = "interact", facing: Facing = "up",
               sign_id: str | None = None, sign_at: tuple[int, int] | None = None,
               breadcrumbs: tuple[tuple[int, int], ...] = (),
               breadcrumb_tile: str = "buoy") -> list[str]:
    """A GATED SPUR TEASE (§3a rule 8 — gates rhyme with rewards): the visible,
    signed promise the player can't take yet. Stamps the `requires_ability`
    warp, an optional sign stating the why + the come-back, and a breadcrumb
    line (buoys/lamps) leading the eye to it. The target map may be unauthored
    (the engine no-ops the warp — a safe inert tease) but list it in graph.ts
    so the region audit tracks the promise. Returns the sign ref owed."""
    m.setdefault("warps", []).append(
        {"id": wid, "at": {"tx": at[0], "ty": at[1]}, "trigger": trigger,
         "to_map": to_map, "to": {"tx": to[0], "ty": to[1]}, "facing": facing,
         "requires_ability": ability, "transition": "door"})
    for (x, y) in breadcrumbs:
        deco[y * w + x] = gid(breadcrumb_tile)
    owed: list[str] = []
    if sign_id and sign_at:
        owed += sign(m, deco, w, sid=sign_id, at=sign_at)
    return owed


def cave_ladder(m: dict, deco, w: int, *, kind: str, at: tuple[int, int],
                to_map: str, to: tuple[int, int], wid: str | None = None) -> None:
    """One half of a dungeon FLOOR LINK (level-design §2a): the ladder tile +
    its step_on warp. kind 'down' stamps the pit (`cave_ladder_down`), 'up'
    the standing ladder (`cave_ladder_up`). The two halves MUST land ON each
    other — call this on each floor's builder with mirrored at/to and let
    `audit_warps` prove the pair (the engine never auto-fires a warp on
    arrival, so landing on the return warp is safe)."""
    assert kind in ("down", "up")
    deco[at[1] * w + at[0]] = gid(f"cave_ladder_{kind}")
    m.setdefault("warps", []).append(
        {"id": wid or f"ladder_{kind}", "at": {"tx": at[0], "ty": at[1]},
         "trigger": "step_on", "to_map": to_map,
         "to": {"tx": to[0], "ty": to[1]},
         "facing": "down" if kind == "down" else "up", "transition": "fade"})


def mandatory_band(tallgrass, path, w: int, h: int, *,
                   y0: int, y1: int, x0: int | None = None,
                   x1: int | None = None) -> None:
    """A MANDATORY encounter crossing (§11 rule 7): a full-corridor band of
    encounter terrain with the lane PAUSED through it, so the road itself
    rolls encounters — flanking patches stay optional. Call AFTER painting
    the path grid and BEFORE any precedence pass that clears grass under
    lanes (this stamp already resolves that conflict band-locally: inside
    the band, grass wins). Rows y0..y1 across columns x0..x1 (default: the
    full width; enclosure terrains painted later still claim their cells)."""
    x0 = 0 if x0 is None else x0
    x1 = w - 1 if x1 is None else x1
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            i = y * w + x
            tallgrass[i] = 1
            if path[i]:
                path[i] = 0


def report(owed: list[str]) -> None:
    """Print the registry entries this map still owes (call from the builder)."""
    print("content refs owed by this map (register in src/game/content/):")
    for ref in owed:
        print(f"  - {ref}")
