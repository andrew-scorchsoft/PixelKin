"""vigil_dress.py — the shared WORLD-CRAFT dressing pass for the five Starfall
Vigil annexes (2026-10, the Central package; world-craft panel §6 WP6).

The vigils shipped as bare arenas (0.69 props per screen, 56-72% bare ground —
audit_visual FAIL/warn). Each builder now hands this module its own prop kit
(the HOST region's objects, reused: a vigil reads as a fold of the place it
opens off) plus a keeper's camp, and a deterministic deco drift over the open
ground. Placement is explicit (the builder names every tile, so lanes and the
trial band are designed, not rolled); `dress` refuses a prop whose footprint
lands on terrain, another object, a warp/trigger/NPC tile or the avoid set, so a
bad coordinate fails the build instead of shipping a sealed lane.

    from vigil_dress import dress
    dress(m, deco, W, H, rng, blocked=[cliff, water, tuft], props=[...],
          drift=["g_daisy", "g_pebble"], density=0.22, avoid={...})
"""
from __future__ import annotations

import random

from mapkit import gid


def _cells(o: dict) -> set[tuple[int, int]]:
    return {(o["at"]["tx"] + dx, o["at"]["ty"] + dy)
            for dx in range(o["w"]) for dy in range(o["h"])}


def dress(m: dict, deco: list[int], W: int, H: int, rng: random.Random, *,
          blocked: list[list[int]], props: list[dict], drift: list[str],
          density: float, avoid: set[tuple[int, int]] | None = None,
          drift_area: tuple[int, int, int, int] | None = None) -> None:
    """Place `props` (MapObject dicts) after checking each footprint, then drift
    `drift` deco names over plain open ground at `density`."""
    avoid = set(avoid or ())
    points = {(p["at"]["tx"], p["at"]["ty"])
              for p in m["npcs"] + m["triggers"] + m["warps"]}
    taken = set().union(*(_cells(o) for o in m["objects"])) if m["objects"] else set()

    def terrain(x: int, y: int) -> bool:
        return any(g[y * W + x] for g in blocked)

    for p in props:
        cells = _cells(p)
        for (x, y) in cells:
            if not (0 <= x < W and 0 <= y < H):
                raise SystemExit(f"vigil_dress: {p['id']} leaves the map at {(x, y)}")
            # a prop's overhang rows may hang over a cliff top; its BASE row may not
            base_row = p["at"]["ty"] + p["h"] - 1
            if y == base_row and terrain(x, y):
                raise SystemExit(f"vigil_dress: {p['id']} base sits on terrain at {(x, y)}")
            if (x, y) in taken or (x, y) in points or (x, y) in avoid:
                raise SystemExit(f"vigil_dress: {p['id']} overlaps a busy tile at {(x, y)}")
        m["objects"].append(p)
        taken |= cells

    x0, y0, x1, y1 = drift_area or (0, 0, W - 1, H - 1)
    names = [gid(n) for n in drift]
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            i = y * W + x
            if deco[i] or terrain(x, y) or (x, y) in taken or (x, y) in points \
                    or (x, y) in avoid:
                continue
            if rng.random() < density:
                deco[i] = rng.choice(names)


def prop(oid: str, sprite: str, at: tuple[int, int], w: int, h: int, **kw) -> dict:
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    return o


# the reusable pieces (manifest footprints)
def tree(oid, at):        return prop(oid, "tinderwick_tree", at, 3, 4, overhang=3, walk_under=True)
def lamp(oid, at):        return prop(oid, "tinderwick_lamp_post", at, 1, 3, overhang=2, walk_under=True)
def camp(oid, at):        return prop(oid, "penumbra_vigil_camp", at, 3, 2)
def scar(oid, at):        return prop(oid, "vigil_star_scar", at, 1, 1, solid=False, walk_under=True)
