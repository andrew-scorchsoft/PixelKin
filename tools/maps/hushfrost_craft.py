"""
hushfrost_craft — shared surface-craft for the two Hushfrost Pass builders
(R10 polish, 2026-10). The shared overworld set is FROZEN, so the pass breaks
its uniform snow with the DRAWN decal objects of draw_hushfrost_objects.py,
laid by these helpers:

  surface_decals(...)  every frost-tuft ENCOUNTER cell gets a `tuftbed_<mask>`
                       overlay (tufts on cold-shadow snow with a ragged snow rim
                       — still tile-aligned, so exactly the rolling cells read as
                       tuft); every TRUE-FILL glacier cell gets a `crest_<mask>`
                       (wind-packed snow on the bank top, ice scoured through);
                       straight south faces get `icicles_*`; and the snow ring
                       round each tuft band gets a few loose `tuft_*` (decor).
  decal / prop         one non-solid ground decal / one solid prop dict.
  carry_over(m, ...)   re-apply the shipped JSON's POST-BUILD additions (the R4
                       day-form zone pairs, the post-shipped tables, the Radiant
                       hollow cache, the runners' items) so a rebuild never
                       regresses them (CLAUDE.md "shipped map JSONs carry
                       post-build surgical additions" gotcha).

Every decal is `solid: false` (collision-, reachability- and audit-neutral); a
mist strip rides overhang = height so it drifts OVER the player.
"""
from __future__ import annotations

import json
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public" / "assets" / "maps"

N_, E_, S_, W_ = 1, 2, 4, 8


def _h(*k) -> int:
    return zlib.crc32(repr(k).encode()) & 0xffffffff


def decal(did: str, sprite: str, x: int, y: int, w: int, h: int, *, above: bool = False) -> dict:
    o = {"id": did, "sprite": f"hushfrost_{sprite}", "at": {"tx": x, "ty": y},
         "w": w, "h": h, "solid": False}
    if above:                       # the whole strip renders over the player
        o.update(overhang=h, walk_under=True)
    return o


def prop(pid: str, sprite: str, x: int, y: int, w: int, h: int, *,
         overhang: int = 0, **kw) -> dict:
    o = {"id": pid, "sprite": sprite, "at": {"tx": x, "ty": y}, "w": w, "h": h}
    if overhang:
        o.update(overhang=overhang, walk_under=True)
    o.update(kw)
    return o


def surface_decals(W: int, H: int, glacier: list, tuft: list, *, prefix: str,
                   reserved: set, tuft_ring: float = 0.22) -> list[dict]:
    def g(grid, x, y):
        return True if not (0 <= x < W and 0 <= y < H) else bool(grid[y * W + x])

    out: list[dict] = []
    for y in range(H):
        for x in range(W):
            if g(tuft, x, y):
                m = (N_ * g(tuft, x, y - 1) | E_ * g(tuft, x + 1, y) |
                     S_ * g(tuft, x, y + 1) | W_ * g(tuft, x - 1, y))
                sp = f"tuftbed_{m}"
                if m == 15:
                    sp += ["", "_v1", "_v2"][_h(prefix, x, y) % 3]
                out.append(decal(f"{prefix}_bed_{x}_{y}", sp, x, y, 1, 1))
    # crest: only TRUE fill (all 8 neighbours glacier) — never over a rim/face tile
    fill = [0] * (W * H)
    for y in range(H):
        for x in range(W):
            if all(g(glacier, x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                fill[y * W + x] = 1
    for y in range(H):
        for x in range(W):
            if fill[y * W + x]:
                m = (N_ * g(fill, x, y - 1) | E_ * g(fill, x + 1, y) |
                     S_ * g(fill, x, y + 1) | W_ * g(fill, x - 1, y))
                if m == 0:
                    continue        # a lone fill cell: a crust island reads as a ghost blob
                sp = f"crest_{m}"
                if m == 15:
                    sp += ["", "_v1", "_v2"][_h(prefix, "c", x, y) % 3]
                out.append(decal(f"{prefix}_crest_{x}_{y}", sp, x, y, 1, 1))
            # icicles on a straight south face (edge_s: N/W/E glacier, S open)
            elif (y + 1 < H and g(glacier, x, y) and not g(glacier, x, y + 1)
                  and g(glacier, x, y - 1) and g(glacier, x - 1, y) and g(glacier, x + 1, y)
                  and _h(prefix, "i", x, y) % 10 < 7):
                out.append(decal(f"{prefix}_ice_{x}_{y}", "icicles_" + "ab"[_h(x, y) % 2], x, y, 1, 1))
    # loose tufts fraying out of each band: open snow within 1-2 cells of a bed
    for y in range(H):
        for x in range(W):
            i = y * W + x
            if glacier[i] or tuft[i] or (x, y) in reserved:
                continue
            near = any(0 <= x + dx < W and 0 <= y + dy < H and tuft[(y + dy) * W + x + dx]
                       for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2))
            if near and (_h(prefix, "t", x, y) % 1000) / 1000 < tuft_ring:
                out.append(decal(f"{prefix}_tuft_{x}_{y}", "tuft_" + "abc"[_h(x, y, 1) % 3], x, y, 1, 1))
    return out


def carry_over(m: dict, *, keep_ids: set[str], keep_prefixes: tuple[str, ...] = ()) -> None:
    """Re-apply the shipped JSON's post-build additions onto a fresh build:
    the shipped encounter list verbatim (tables, flags, `_day` twins, rects),
    the shipped ambience, and
    every npc/object/trigger in `keep_ids` or under `keep_prefixes`."""
    path = MAPS / f"{m['id']}.json"
    if not path.exists():
        return
    old = json.loads(path.read_text())
    # the SHIPPED zone list is the truth: the wiring pass re-tabled zones and
    # merged pass II's pocket_b into a loose pocket_a rect after the build. The
    # rects are kept as shipped; every built zone must still sit inside one of
    # them (tile-bound tall_grass only rolls on painted cells, so a loose rect is
    # fine) — a zone that escapes is reported for hand-wiring, never auto-added.
    enc = [dict(e) for e in old.get("encounters", [])]

    def inside(a, b):
        return (b["tx"] <= a["tx"] and b["ty"] <= a["ty"] and
                a["tx"] + a["w"] <= b["tx"] + b["w"] and a["ty"] + a["h"] <= b["ty"] + b["h"])
    for e in m["encounters"]:
        if not any(inside(e["rect"], o["rect"]) for o in enc):
            print(f"  carry_over: built zone {e['id']} {e['rect']} escapes every shipped zone — WIRE IT")
    m["encounters"] = enc
    if "ambience" in old:
        m["ambience"] = old["ambience"]
    for key in ("npcs", "objects", "triggers"):
        ids = {o["id"] for o in m[key]}
        carried = []
        for o in old.get(key, []):
            if o["id"] in ids:
                continue
            if o["id"] in keep_ids or o["id"].startswith(keep_prefixes):
                carried.append(o)
        # objects go FIRST (ground decals like the crater sit under the props)
        m[key] = carried + m[key] if key == "objects" else m[key] + carried
