#!/usr/bin/env python3
"""
Shared map-builder toolkit for PixelKin overworld maps.

The convention the maps follow now: a map does NOT bake its own atlas. It REFERENCES
the shared `vesper_overworld_set` (built by build_shared_overworld.py) by name + first_gid
and paints terrain layers; the engine resolves gids across tilesets, and tools/autotile
meshes the terrain (with variant scatter) into the base layer. An area adds only its own
objects (buildings) + an optional small accent tileset at a higher first_gid.

This module centralises:
  * the shared set's TilesetRef + a `gid(name)` lookup into it,
  * grid painting helpers (rect / line / organic border / scatter decor),
  * `finalize()` — the standing build pipeline: write -> autotile expand -> strip terrain
    layers -> re-write -> render PNG -> validate. One call so every builder is turnkey.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import random

REPO = Path(__file__).resolve().parents[2]
SHARED = REPO / "assets/tilesets/_shared"
SCRIPTS = REPO / ".claude/skills/generate-sprite-sheet/scripts"
SHARED_FIRST_GID = 1

_INDEX = json.loads((SHARED / "vesper_overworld.index.json").read_text())
_SIDECAR = json.loads(
    (REPO / "public/assets/tilesets/vesper_overworld_set.tileset.json").read_text())

# Registered tilesets: name -> (first_gid, name->local-index map, sidecar).
# The shared overworld set is always registered; ACCENT sets join via
# register_tileset() so an area can stack its own kit at a higher first_gid
# (the engine resolves gids across tilesets by range — MapLoader.ts).
_TILESETS: dict[str, tuple[int, dict, dict]] = {
    "vesper_overworld_set": (SHARED_FIRST_GID, _INDEX, _SIDECAR),
}


def register_tileset(name: str, *, index: dict | str | Path | None = None,
                     first_gid: int | None = None) -> dict:
    """Register an ACCENT tileset for this build and return its TilesetRef.

    `index` maps tile names -> local indices (a dict, or a path to an index
    JSON like the shared set's). Without one, tiles are addressable only by
    local index via `gid_at()`. `first_gid` defaults to stacking directly
    above every set registered so far. The returned ref goes in the map's
    `tilesets[]` (alongside `shared_tileset_ref()`); `gid()` then resolves
    names across every registered set.
    """
    side_path = REPO / "public/assets/tilesets" / f"{name}.tileset.json"
    side = json.loads(side_path.read_text())
    if first_gid is None:
        first_gid = next_first_gid()
    if isinstance(index, (str, Path)):
        index = json.loads(Path(index).read_text())
    _TILESETS[name] = (first_gid, index or {}, side)
    return {
        "name": name,
        "image": f"assets/tilesets/{name}.webp",
        "tile_width": side.get("tile_width", 16),
        "tile_height": side.get("tile_height", 16),
        "first_gid": first_gid,
        "columns": side["columns"],
        "tile_count": side["tile_count"],
    }


def next_first_gid() -> int:
    """The first free gid above every registered set (stack accents here)."""
    return max(fg + side["tile_count"] for fg, _, side in _TILESETS.values())


def gid(name: str, set: str | None = None) -> int:
    """Global tile id of a named tile. Searches the shared set first, then
    every registered accent set; pass `set=` to disambiguate a name that
    exists in more than one kit."""
    if set is not None:
        fg, index, _ = _TILESETS[set]
        return fg + index[name]
    for fg, index, _ in _TILESETS.values():
        if name in index:
            return fg + index[name]
    raise KeyError(f"tile '{name}' not in any registered tileset "
                   f"({', '.join(_TILESETS)})")


def gid_at(set: str, local_index: int) -> int:
    """Global id of a tile addressed by local index in a registered set."""
    return _TILESETS[set][0] + local_index


def shared_tileset_ref() -> dict:
    """The TilesetRef every overworld map lists in `tilesets[]`."""
    return {
        "name": "vesper_overworld_set",
        "image": "assets/tilesets/vesper_overworld_set.webp",
        "tile_width": 16, "tile_height": 16,
        "first_gid": SHARED_FIRST_GID,
        "columns": _SIDECAR["columns"],
        "tile_count": _SIDECAR["tile_count"],
    }


# ---- grid helpers (presence grids: 1 = terrain here) -------------------------
def make_grid(w: int, h: int) -> list[int]:
    return [0] * (w * h)


def rect(g, w, h, x0, y0, x1, y1, val=1):
    for y in range(max(0, y0), min(h, y1 + 1)):
        for x in range(max(0, x0), min(w, x1 + 1)):
            g[y * w + x] = val


def hline(g, w, h, y, x0, x1, val=1):
    rect(g, w, h, x0, y, x1, y, val)


def vline(g, w, h, x, y0, y1, val=1):
    rect(g, w, h, x, y0, x, y1, val)


def organic_border(g, w, h, *, top=0, left=0, right=0, depth=2,
                   bumps=(), rng: random.Random | None = None):
    """A `depth`-deep border on the chosen sides, then a few inward `bumps`
    (x,y,r) blobs so the tree/cliff line reads organic, not a ruled box."""
    if top:
        rect(g, w, h, 0, 0, w - 1, depth - 1)
    if left:
        rect(g, w, h, 0, 0, depth - 1, h - 1)
    if right:
        rect(g, w, h, w - depth, 0, w - 1, h - 1)
    for (bx, by, br) in bumps:
        for y in range(by - br, by + br + 1):
            for x in range(bx - br, bx + br + 1):
                if 0 <= x < w and 0 <= y < h and (x - bx) ** 2 + (y - by) ** 2 <= br * br:
                    g[y * w + x] = 1


def blob(g, w, h, cx, cy, rx, ry=None, val=1):
    """An elliptical organic patch — the shape encounter grass / terraces / bays
    want instead of a ruled rect (level-design §11: 'regions, not rectangles')."""
    ry = ry if ry is not None else rx
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if 0 <= x < w and 0 <= y < h and \
                    ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                g[y * w + x] = val


def fence_run(deco, w, h, x0, y, x1):
    """A W-E fence line: slat tiles capped with end posts (collides via tileset)."""
    for x in range(x0, x1 + 1):
        deco[y * w + x] = gid("fence_h")
    deco[y * w + x0] = gid("fence_post")
    deco[y * w + x1] = gid("fence_post")


def scatter_decor(deco, base, w, h, rng, *, density=0.10, avoid=None, flowers=0.12):
    """Sprinkle sparse ground decor (pebble/tuft/daisy/patch + occasional flowerbed)
    onto plain-grass cells — the Pokémon trick that breaks a flat fill grid.
    `avoid` = set of (x,y) to skip; `flowers` = share of picks that bloom."""
    grass = {gid(n) for n in ("grass0", "grass1", "grass2", "grass3")}
    props = [gid("g_tuft"), gid("g_tuft"), gid("g_daisy"), gid("g_pebble"), gid("g_patch")]
    blooms = [gid("flowerbed_a"), gid("flowerbed_b")]
    avoid = avoid or set()
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if base[i] in grass and deco[i] == 0 and (x, y) not in avoid \
                    and rng.random() < density:
                deco[i] = rng.choice(blooms) if rng.random() < flowers else rng.choice(props)


# ---- deep water (2026-10) ----------------------------------------------------
DEEPWATER_INDEX = REPO / "assets/tilesets/deepwater/deepwater_set.index.json"


def deep_water(m: dict, *, shelf: int = 2, keep=(), keep_rects=(), deep_cols=None) -> int:
    """Mark a sea map's OPEN water DEEP (the darker `deepwater_set` family, gated
    on the reserved `deepdive` — Tidecall swims the shallows only).

    The map's `water` terrain layers are read; every water cell more than
    `shelf` tiles (Chebyshev) from dry ground becomes deep, EXCEPT:
      * cells within 1 of a warp/trigger/NPC placed on water, plus a shallow
        channel from the main shore to it (so nothing designed is cut off);
      * a shallow channel from the main shore to every islet (dry ground not
        connected to the main shore by land);
      * `keep` cells / `keep_rects` (x0, y0, x1, y1) — designed swim lanes.
    `deep_cols` (x0, x1): every water cell in these columns is deep regardless
    of the shelf — for two maps whose seas share real ground (the bay between
    Dimglass Coast II and the breakwater), so it's walkable in at most one.
    The map edge is NOT dry ground — the sea runs on off-map. Adds a terrain
    layer + the accent set ref; call before finalize(). Returns deep-cell count."""
    from collections import deque
    W, H = m["width"], m["height"]
    water = [0] * (W * H)
    for ly in m["layers"]:
        if ly.get("role") == "terrain" and ly.get("terrain") == "water":
            for i, v in enumerate(ly["data"]):
                if v:
                    water[i] = 1
    for ly in m["layers"]:            # anything painted OVER water after it wins
        if ly.get("role") == "terrain" and ly.get("terrain") not in ("water", "deepwater"):
            seen_water = False
            for l2 in m["layers"]:
                if l2 is ly:
                    break
                if l2.get("terrain") == "water":
                    seen_water = True
            if seen_water:
                for i, v in enumerate(ly["data"]):
                    if v:
                        water[i] = 0
    INF = 10 ** 6
    dist = [0 if not water[i] else INF for i in range(W * H)]
    q = deque(i for i in range(W * H) if not water[i])
    while q:
        i = q.popleft()
        x, y = i % W, i // W
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H:
                    j = ny * W + nx
                    if dist[j] > dist[i] + 1:
                        dist[j] = dist[i] + 1
                        q.append(j)
    deep = [1 if water[i] and (dist[i] > shelf or
                               (deep_cols and deep_cols[0] <= i % W <= deep_cols[1]))
            else 0 for i in range(W * H)]
    if not any(deep):
        return 0

    def clear(x, y, r=1):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if 0 <= x + dx < W and 0 <= y + dy < H:
                    deep[(y + dy) * W + x + dx] = 0

    # dry components: the main shore = the largest; the rest are islets
    comp = [-1] * (W * H)
    sizes = []
    for i in range(W * H):
        if water[i] or comp[i] >= 0:
            continue
        c = len(sizes)
        comp[i] = c
        stack, n = [i], 0
        while stack:
            k = stack.pop()
            n += 1
            kx, ky = k % W, k // W
            for nx, ny in ((kx + 1, ky), (kx - 1, ky), (kx, ky + 1), (kx, ky - 1)):
                if 0 <= nx < W and 0 <= ny < H:
                    j = ny * W + nx
                    if not water[j] and comp[j] < 0:
                        comp[j] = c
                        stack.append(j)
        sizes.append(n)
    main = max(range(len(sizes)), key=lambda c: sizes[c]) if sizes else -1

    def channel_to(targets):
        """Shallow BFS channel (through water) from the main shore to targets."""
        tset = set(targets)
        prev = {}
        dq = deque()
        for i in range(W * H):
            if comp[i] == main:
                dq.append(i)
                prev[i] = None
        hit = None
        while dq:
            i = dq.popleft()
            if i in tset:
                hit = i
                break
            x, y = i % W, i // W
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < W and 0 <= ny < H:
                    j = ny * W + nx
                    if j not in prev and (water[j] or j in tset):
                        prev[j] = i
                        dq.append(j)
        while hit is not None:
            clear(hit % W, hit // W)
            hit = prev[hit]

    for c in range(len(sizes)):
        if c != main:
            channel_to([i for i in range(W * H) if comp[i] == c])
    spots = [(w["at"]["tx"], w["at"]["ty"]) for w in m.get("warps", [])]
    spots += [(t["at"]["tx"], t["at"]["ty"]) for t in m.get("triggers", [])]
    spots += [(n["at"]["tx"], n["at"]["ty"]) for n in m.get("npcs", []) if not n.get("ambient")]
    for (x, y) in spots:
        if 0 <= x < W and 0 <= y < H and water[y * W + x]:
            clear(x, y)
            channel_to([y * W + x])
    for (x, y) in keep:
        clear(x, y, 0)
    for (x0, y0, x1, y1) in keep_rects:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                clear(x, y, 0)
    if not any(deep):
        return 0
    if not any(ts.get("name") == "deepwater_set" for ts in m["tilesets"]):
        m["tilesets"].append(register_tileset("deepwater_set", index=DEEPWATER_INDEX))
    else:
        register_tileset("deepwater_set", index=DEEPWATER_INDEX,
                         first_gid=next(ts["first_gid"] for ts in m["tilesets"]
                                        if ts.get("name") == "deepwater_set"))
    layer = {"name": "t_deepwater", "role": "terrain", "terrain": "deepwater",
             "set": "deepwater_set", "depth": 0, "data": deep}
    # after every terrain layer, so it writes over the shallows it replaces
    last = max(i for i, ly in enumerate(m["layers"]) if ly.get("role") in ("terrain", "base"))
    m["layers"].insert(last + 1, layer)
    return sum(deep)


# ---- the standing build pipeline --------------------------------------------
def finalize(m: dict, *, scale: int = 3, render: bool = True,
             pin_base: dict[tuple[int, int], str] | None = None) -> bool:
    """Write the map, expand terrain -> base (variant autotiling), strip the terrain
    layers (runtime wants plain gids), re-write, render a QA PNG, validate, run the
    cross-map WARP AUDIT (wide-entrance coverage, landings, round trips) and the
    FLOW AUDIT (reachability, choke triggers, free-pass, loops, dead-end payoff,
    screen pacing — the executable §3a pass). Returns True iff validate_map,
    audit_warps AND audit_flow all pass (flow WARNs don't fail; flow FAILs do)."""
    map_path = REPO / "public/assets/maps" / f"{m['id']}.json"
    map_path.write_text(json.dumps(m, indent=2) + "\n")

    exp = subprocess.run(["node", str(REPO / "tools/autotile/expand.mjs"), str(map_path)],
                         capture_output=True, text=True)
    if exp.returncode != 0:
        print("EXPAND FAILED:\n", exp.stderr or exp.stdout)
        return False

    # strip terrain layers — the engine reads plain gids; terrain layers were authoring-only.
    m2 = json.loads(map_path.read_text())
    m2["layers"] = [ly for ly in m2["layers"] if ly.get("role") != "terrain"]
    # `pin_base`: {(x, y): tile name} written over the EXPANDED base — for the few
    # cells a shipped map hand-picked (a variant, a mown tile) that the autotiler
    # wouldn't choose, so a rebuild reproduces the shipped map exactly.
    if pin_base:
        base = next(ly for ly in m2["layers"] if ly.get("role") == "base")["data"]
        for (x, y), name in pin_base.items():
            base[y * m2["width"] + x] = gid(name)
    map_path.write_text(json.dumps(m2, indent=2) + "\n")

    if render:
        out = Path("/tmp") / f"{m['id']}.png"
        subprocess.run([sys.executable, str(SCRIPTS / "render_map.py"), str(map_path),
                        "--output", str(out), "--scale", str(scale)], capture_output=True)
        print(f"  rendered -> {out}")

    val = subprocess.run([sys.executable, str(SCRIPTS / "validate_map.py"), str(map_path)],
                         capture_output=True, text=True)
    print(val.stdout)

    # cross-map warp audit, focused on this map (tools/maps/audit_warps.py)
    aud = subprocess.run([sys.executable, str(REPO / "tools/maps/audit_warps.py"), m["id"]],
                         capture_output=True, text=True)
    print(aud.stdout)

    # flow audit — the executable level-design pass (tools/maps/audit_flow.py)
    flow = subprocess.run([sys.executable, str(REPO / "tools/maps/audit_flow.py"), m["id"]],
                          capture_output=True, text=True)
    print(flow.stdout)
    return val.returncode == 0 and aud.returncode == 0 and flow.returncode == 0
