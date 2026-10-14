"""
farlamp_kit — the shared map kit of the Farlamp Isles (walkthrough/10 Part I).

Sea maps are mostly OPEN DEEP water (rowed in the Farlamp skiff, gated on
`deepdive`), with shallow shelves round every islet and coast (Tidecall swims
them). `mapkit.deep_water` is built for coasts — it cuts a shallow channel from
the main shore to every islet, which on an open sea would stripe the deep with
shallow ribbons — so the isles paint their own deep: every water cell more than
`shelf` tiles from dry ground (Chebyshev) is deep, nothing else.

`Sea` collects the presence grids + content for one map; `link()` stitches a
shared edge between two maps with a step_on warp on EVERY tile where both sides
are passable (landing one tile inboard, on the return warp's neighbour —
audit_warps' rule), mirrored both ways; `finish()` assembles the layers, paints
the deep and runs mapkit.finalize.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import mapkit as mk
from mapkit import gid

REPO = Path(__file__).resolve().parents[2]
FARLAMP_INDEX = REPO / "assets/tilesets/farlamp/farlamp_set.index.json"
MUSIC_SEA = "assets/audio/music/farlamp-sound.mp3"
SEA_BACKDROPS = ["assets/backgrounds/battle/farlamp-sea-a.webp"]
ISLE_BACKDROPS = ["assets/backgrounds/battle/farlamp-isle-a.webp"]

# ambience: the sea-fog that lies over the isles until the Farlamp burns again
# (the `when` rule — MapAmbience.when — swaps in the cleared block after the dawn)
def sea_ambience(*, heavy: bool = False, flocks=(), lights=()) -> dict:
    fog = {"mist": {"color": "#c8d4e4", "alpha": 0.34 if heavy else 0.16,
                    "speed": 5 if heavy else 8},
           "tint": {"color": "#16233c", "alpha": 0.30 if heavy else 0.16},
           "sound_bed": "amb-surf",
           "starfall": False if heavy else {"min_s": 50, "max_s": 110},
           "birds": {"kind": "gull", "flocks": [{"tx": x, "ty": y} for (x, y) in flocks],
                     "flyover": True}}
    if lights:
        fog["light_sources_extra"] = [{"at": {"tx": x, "ty": y}, "radius": r, "color": c}
                                      for (x, y, r, c) in lights]
    clear = {"mist": {"color": "#e8eef6", "alpha": 0.06, "speed": 10},
             "sound_bed": "amb-surf",
             "starfall": {"min_s": 40, "max_s": 90},
             "birds": {"kind": "gull", "flocks": [{"tx": x, "ty": y} for (x, y) in flocks],
                       "flyover": True}}
    if lights:
        clear["light_sources_extra"] = fog["light_sources_extra"]
    fog["when"] = [{"flag": "flag:isles_dawn", "ambience": clear}]
    return fog


class Sea:
    def __init__(self, mid: str, name: str, W: int, H: int, *, seed: int, kind: str = "route",
                 music: str = MUSIC_SEA, backdrops=None, sea: bool = True):
        self.id, self.name, self.W, self.H = mid, name, W, H
        self.rng = random.Random(seed)
        g = lambda: mk.make_grid(W, H)  # noqa: E731
        self.water = g()
        if sea:
            mk.rect(self.water, W, H, 0, 0, W - 1, H - 1)
        self.sand, self.tallgrass, self.dunegrass = g(), g(), g()
        self.cliff, self.tree, self.path, self.pond, self.ruin = g(), g(), g(), g(), g()
        self.deco, self.above = g(), g()
        self.no_deep: set[tuple[int, int]] = set()   # designed shallows
        self.pin: dict = {}
        self.m: dict = {
            "id": mid, "display_name": name, "width": W, "height": H,
            "tile_width": 16, "tile_height": 16, "kind": kind,
            "tilesets": [mk.shared_tileset_ref()],
            "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
            "gates": [], "music": music,
        }
        if backdrops:
            self.m["battle_backdrops"] = list(backdrops)
        self.owed: list[str] = []

    # ---- painting -------------------------------------------------------------
    def islet(self, cx, cy, rx, ry, *, grass: float = 0.0):
        """A sand islet carved out of the sea; `grass` (0..1) = the share of its
        radius that's green turf inside the sand rim."""
        W, H = self.W, self.H
        mk.blob(self.sand, W, H, cx, cy, rx, ry)
        # two or three offset lobes so no islet reads as a stamped plus-sign
        if rx >= 2 and ry >= 1.5:
            for _ in range(self.rng.choice((2, 3))):
                ox = self.rng.uniform(-0.55, 0.55) * rx
                oy = self.rng.uniform(-0.55, 0.55) * ry
                mk.blob(self.sand, W, H, cx + ox, cy + oy, rx * self.rng.uniform(0.45, 0.7),
                        ry * self.rng.uniform(0.5, 0.75))
        if grass > 0:
            inner = mk.make_grid(W, H)
            mk.blob(inner, W, H, cx, cy, rx * grass, ry * grass)
            for i, v in enumerate(inner):
                if v:
                    self.sand[i] = 0
                    self.water[i] = 0
        for i, v in enumerate(self.sand):
            if v:
                self.water[i] = 0

    def land(self, grid_painter):
        """Run `grid_painter(g)` on a fresh grid and make those cells dry turf."""
        g = mk.make_grid(self.W, self.H)
        grid_painter(g)
        for i, v in enumerate(g):
            if v:
                self.water[i] = 0
                self.sand[i] = 0
        return g

    def cell(self, x, y):
        return y * self.W + x

    def obj(self, oid, sprite, at, w, h, **kw):
        o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
        o.update(kw)
        self.m["objects"].append(o)
        return o

    def npc(self, nid, at, sprite, ref, *, facing="down", movement="static", **kw):
        n = {"id": nid, "at": {"tx": at[0], "ty": at[1]}, "facing": facing,
             "sprite": sprite, "movement": movement, "dialogue_ref": ref}
        n.update(kw)
        self.m["npcs"].append(n)
        return n

    def cache(self, cid, at, **kw):
        n = self.npc(f"cache_{cid}", at, "item_cache", f"script.pickup_{cid}",
                     hidden_when_flag=f"flag:picked_{cid}", **kw)
        self.owed.append(f"script.pickup_{cid}")
        return n

    def kin(self, nid, at, kin_id, radius=2, **kw):
        n = {"id": nid, "at": {"tx": at[0], "ty": at[1]}, "facing": "down",
             "sprite": f"kin_{kin_id}_overworld", "movement": "wander",
             "ambient": True, "wander_radius": radius}
        n.update(kw)
        self.m["npcs"].append(n)
        return n

    def sign(self, sid, at):
        self.deco[self.cell(*at)] = gid("sign")
        self.m["triggers"].append({"id": f"sign_{sid}", "kind": "sign",
                                   "at": {"tx": at[0], "ty": at[1]},
                                   "activation": "interact", "ref": f"sign.{sid}"})
        self.owed.append(f"sign.{sid}")

    def trainer(self, tid, at, facing, sprite, sight=1):
        flag = f"flag:{tid}_beaten"
        self.npc(tid, at, sprite, f"script.{tid}", facing=facing,
                 sight_range=sight, defeated_flag=flag, hidden_when_flag=flag)
        self.npc(f"{tid}_after", at, sprite, f"npc.{tid}_after", facing=facing,
                 movement="look_around", requires_flag=flag)
        self.owed += [f"script.{tid}", f"npc.{tid}_after", f"TRAINERS[{tid}]"]

    # ---- the model the edge linker reads --------------------------------------
    def dry(self, x, y) -> bool:
        i = self.cell(x, y)
        return not self.water[i]

    def passable(self, x, y) -> bool:
        i = self.cell(x, y)
        if self.cliff[i] or self.tree[i]:
            return False
        if self.deco[i] in (gid("boulder"), gid("sign")):
            return False
        for o in self.m["objects"]:
            if o.get("solid") is False:
                continue
            ox, oy = o["at"]["tx"], o["at"]["ty"]
            if ox <= x < ox + o["w"] and oy <= y < oy + o["h"]:
                return False
        return True

    # ---- deep water -------------------------------------------------------------
    def deep_grid(self, shelf: float = 1.5) -> list[int]:
        W, H = self.W, self.H
        dryc = [(i % W, i // W) for i in range(W * H) if not self.water[i] or self.pond[i]]
        deep = [0] * (W * H)
        if not dryc:
            return [1 if v else 0 for v in self.water]
        # Euclidean distance to the nearest dry cell: the shelf follows the
        # islet's own round shape instead of a Chebyshev box
        for i in range(W * H):
            if not self.water[i] or (i % W, i // W) in self.no_deep:
                continue
            x, y = i % W, i // W
            d2 = min((x - dx) ** 2 + (y - dy) ** 2 for (dx, dy) in dryc)
            if d2 > shelf * shelf:
                deep[i] = 1
        # no lone deep cells (the autotiler can't draw a 1-tile pit)
        for _ in range(2):
            for i in range(W * H):
                if deep[i]:
                    x, y = i % W, i // W
                    n = sum(1 for (nx, ny) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                            if not (0 <= nx < W and 0 <= ny < H) or deep[ny * W + nx])
                    if n < 2:
                        deep[i] = 0
        return deep

    # ---- assembly -----------------------------------------------------------------
    def assemble(self, *, shelf: float = 1.5, extra_layers=()):
        W, H = self.W, self.H
        # a strand that runs into the map border with no warp on it is just open
        # sea at the edge (validate_map: no warp-less passable border runs)
        warped = {(w["at"]["tx"], w["at"]["ty"]) for w in self.m["warps"]}
        for y in range(H):
            for x in range(W):
                if (x in (0, W - 1) or y in (0, H - 1)) and (x, y) not in warped:
                    i = self.cell(x, y)
                    if self.sand[i] and not self.water[i] and not self.cliff[i]:
                        self.water[i] = 1
        # tiny enclosed water pockets (1-3 cells) can't be drawn as a shore: fill them
        seen = [False] * (W * H)
        for i in range(W * H):
            if not self.water[i] or seen[i]:
                continue
            comp, stack, edge = [], [i], False
            seen[i] = True
            while stack:
                j = stack.pop()
                comp.append(j)
                x, y = j % W, j // W
                if x in (0, W - 1) or y in (0, H - 1):
                    edge = True
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < W and 0 <= ny < H and self.water[ny * W + nx] \
                            and not seen[ny * W + nx]:
                        seen[ny * W + nx] = True
                        stack.append(ny * W + nx)
            if len(comp) <= 3 and not edge:
                for j in comp:
                    self.water[j] = 0
                    self.sand[j] = 1
        for i in range(W * H):
            if self.water[i]:
                self.sand[i] = 1          # the sea lies over sand (a sand shore, context rule)
                self.tallgrass[i] = self.tree[i] = self.path[i] = self.cliff[i] = 0
            if self.cliff[i] or self.tree[i]:
                self.sand[i] = 0
                self.path[i] = 0
        gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
        base = [self.rng.choice(gg) if self.rng.random() < 0.5 else gg[0] for _ in range(W * H)]
        L = lambda n, t, d: {"name": n, "role": "terrain", "terrain": t,  # noqa: E731
                             "set": "vesper_overworld_set", "depth": 0, "data": d}
        layers = [{"name": "base", "role": "base", "depth": 0, "data": base},
                  L("t_ruin", "ruinfloor", self.ruin),
                  L("t_tallgrass", "tallgrass", self.tallgrass),
                  L("t_cliff", "cliff", self.cliff),
                  L("t_sand", "sand", self.sand),
                  L("t_dunegrass", "dunegrass", self.dunegrass),
                  L("t_pond", "pond", self.pond),
                  L("t_water", "water", self.water),
                  L("t_path", "trail" if any(self.sand) else "path", self.path),
                  L("t_tree", "tree", self.tree),
                  *extra_layers]
        deep = self.deep_grid(shelf)
        if any(deep):
            ref = mk.register_tileset("deepwater_set", index=mk.DEEPWATER_INDEX)
            self.m["tilesets"].append(ref)
            layers.append({"name": "t_deepwater", "role": "terrain", "terrain": "deepwater",
                           "set": "deepwater_set", "depth": 0, "data": deep})
        layers += [{"name": "deco", "role": "deco", "depth": 5, "data": self.deco},
                   {"name": "above", "role": "above", "depth": 20, "data": self.above}]
        self.m["layers"] = layers
        self.deep = deep
        return deep

    def use_farlamp_set(self):
        if not any(ts.get("name") == "farlamp_set" for ts in self.m["tilesets"]):
            self.m["tilesets"].append(mk.register_tileset("farlamp_set", index=FARLAMP_INDEX))

    def scatter(self, density=0.08):
        W, H = self.W, self.H
        objcells = {(x, y) for o in self.m["objects"]
                    for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                    for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
        busy = {(n["at"]["tx"], n["at"]["ty"]) for n in self.m["npcs"]} | \
               {(t["at"]["tx"], t["at"]["ty"]) for t in self.m["triggers"]} | \
               {(w["at"]["tx"], w["at"]["ty"]) for w in self.m["warps"]}
        covered = {(x, y) for y in range(H) for x in range(W)
                   if any(g[y * W + x] for g in (self.tree, self.path, self.sand, self.water,
                                                 self.deco, self.cliff, self.tallgrass,
                                                 self.pond, self.ruin))}
        base = next(ly for ly in self.m["layers"] if ly["role"] == "base")["data"]
        mk.scatter_decor(self.deco, base, W, H, self.rng, density=density,
                         avoid=covered | objcells | busy)

    def finalize(self, scale=3) -> bool:
        ok = mk.finalize(self.m, scale=scale, pin_base=self.pin or None)
        if self.owed:
            print("CONTENT OWED:", sorted(set(self.owed)))
        return ok


def edge_cells(s: Sea, edge: str, lo: int, hi: int):
    """(x, y) cells along an edge between indices lo..hi (inclusive)."""
    if edge == "n":
        return [(i, 0) for i in range(lo, hi + 1)]
    if edge == "s":
        return [(i, s.H - 1) for i in range(lo, hi + 1)]
    if edge == "w":
        return [(0, i) for i in range(lo, hi + 1)]
    return [(s.W - 1, i) for i in range(lo, hi + 1)]


INWARD = {"n": (0, 1), "s": (0, -1), "w": (1, 0), "e": (-1, 0)}
FACING_IN = {"n": "down", "s": "up", "w": "right", "e": "left"}


def warp(src: dict, wid, at, to_map, to, facing, **kw):
    w = {"id": wid, "at": {"tx": at[0], "ty": at[1]}, "trigger": "step_on",
         "to_map": to_map, "to": {"tx": to[0], "ty": to[1]}, "facing": facing,
         "transition": "fade"}
    w.update(kw)
    src.setdefault("warps", []).append(w)


def _shore(s: Sea, x: int, y: int) -> bool:
    if not s.water[s.cell(x, y)]:
        return False
    return any(0 <= x + dx < s.W and 0 <= y + dy < s.H and not s.water[s.cell(x + dx, y + dy)]
               for dx in (-1, 0, 1) for dy in (-1, 0, 1))


def link(a: Sea, ea: str, b: Sea, eb: str, *, a_lo: int, b_lo: int, n: int,
         prefix_a: str, prefix_b: str, also=None):
    """Stitch a's edge `ea` (indices a_lo..a_lo+n-1) to b's edge `eb` (b_lo..),
    tile for tile. A warp lands ONE tile inboard (on the return warp's
    neighbour), facing inward from the landing edge."""
    ca = edge_cells(a, ea, a_lo, a_lo + n - 1)
    cb = edge_cells(b, eb, b_lo, b_lo + n - 1)
    k = 0
    for (pa, pb) in zip(ca, cb):
        if not (a.passable(*pa) and b.passable(*pb)):
            continue
        ia, ib = INWARD[ea], INWARD[eb]
        la = (pa[0] + ia[0], pa[1] + ia[1])
        lb = (pb[0] + ib[0], pb[1] + ib[1])
        if not (a.passable(*la) and b.passable(*lb)):
            continue
        # a landing in the water right against dry land sits on a shore-edge tile,
        # and the autotiler's corner variants there are solid rock: don't land on one
        if _shore(a, *la) or _shore(b, *lb):
            continue
        # never land on another edge's row (a corner would land ON a third map's warp)
        if not (0 < la[0] < a.W - 1 and 0 < la[1] < a.H - 1 and
                0 < lb[0] < b.W - 1 and 0 < lb[1] < b.H - 1):
            continue
        warp(a.m, f"{prefix_a}_{k}", pa, b.id, lb, FACING_IN[eb])
        warp(b.m, f"{prefix_b}_{k}", pb, a.id, la, FACING_IN[ea])
        k += 1
    return k


def load_shipped(mid: str) -> dict:
    return json.loads((REPO / "public/assets/maps" / f"{mid}.json").read_text())
