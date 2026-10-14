#!/usr/bin/env python3
"""
undertidekit — the shared toolkit behind the UNDERTIDE floors and the Drowned Lamp
(10-the-farlamp-isles.md Part I; build_undertide_*.py, build_farlamp_drowned.py).

A floor is authored on a char PLAN (one string per row) plus a few calls:

    '#' rock (cavewall)      '.' wet cave floor     ',' bare cave floor
    '~' the SURGE (churning white water — solid, the maze's walls)
    'o' the SHALLOWS (tidepool: swum with Tidecall, the water beds)
    '>' '<' '^' 'v'   a TIDE-RACE lane carrying that way (a kind:'rail' flow)
    'J'  a junction pool — give it its flows with `junction()`
    '=' dressed stone (the drowned lighthouse floor: ruinfloor)

`finish()` writes the standard cave layer stack:

    base (floor, wetstone/ruin pins, race art pins) -> t_tidepool -> t_surge
    -> t_cavewall -> deco -> above

Race cells count as SURGE for the autotiler (so the churn wraps a lane
seamlessly) and are pinned to their race art over it.

THE TIDE-RACE INVARIANT (the Old Seams one, generalised): `prove()` walks every
combination of the floor's bell flags. In EVERY state, every lane entered from
any free cell must END on a free cell (never stall in the race), and from every
free pocket the floor's home pocket must be reachable by riding races (no
softlock). Builders add their own puzzle assertions on top (`pocket_of`).
"""
from __future__ import annotations

import itertools
import random
from collections import deque
from pathlib import Path

import mapkit as mk
from mapkit import gid

REPO = Path(__file__).resolve().parents[2]
SET = "undertide_set"
INDEX = REPO / "assets/tilesets/undertide/undertide_set.index.json"

MUSIC = "assets/audio/music/undertide.mp3"
BACKDROPS = ["assets/backgrounds/battle/undertide-a.webp"]

DIRS = {">": "right", "<": "left", "^": "up", "v": "down"}
DAWN = "flag:isles_dawn"

# The DAY-FORM swap (the R4 pattern, the isles' own dawn): the woken forms of the
# same water — mirrored in build_species.py UNDERTIDE_DAY_SWAP (keep in step).
DAY_SWAP = {174: 175, 172: 173, 29: 30}


def day_table(rows: list) -> list:
    """The day-form twin of a (kin, weight, lo, hi) table: kindled forms, +1 level."""
    out: dict = {}
    for (k, w, lo, hi) in rows:
        d = DAY_SWAP.get(k, k)
        lo, hi = min(lo + 1, 67), min(hi + 1, 67)
        if d in out:                      # a kindled form already in the table: merge
            pw, plo, phi = out[d]
            out[d] = (pw + w, min(plo, lo), max(phi, hi))
        else:
            out[d] = (w, lo, hi)
    return [(k, w, lo, hi) for k, (w, lo, hi) in out.items()]
STEP = {"right": (1, 0), "left": (-1, 0), "down": (0, 1), "up": (0, -1)}
OPP = {"right": "left", "left": "right", "up": "down", "down": "up"}


def U(name: str) -> int:
    return gid(name, set=SET)


class Floor:
    def __init__(self, mid: str, name: str, plan: list[str], *, seed: int,
                 music: str = MUSIC, backdrops: list[str] | None = None, dark: bool = True):
        self.W, self.H = len(plan[0]), len(plan)
        assert all(len(r) == self.W for r in plan), [len(r) for r in plan]
        self.plan = [list(r) for r in plan]
        self.rng = random.Random(seed)
        self.m: dict = {
            "id": mid, "display_name": name,
            "width": self.W, "height": self.H, "tile_width": 16, "tile_height": 16,
            "kind": "cave",
            "tilesets": [mk.shared_tileset_ref()],
            "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
            "gates": [], "flows": [],
            "music": music, "battle_backdrops": list(backdrops or BACKDROPS),
        }
        self.m["tilesets"].append(mk.register_tileset(SET, index=INDEX))
        self.deco = mk.make_grid(self.W, self.H)
        self.above = mk.make_grid(self.W, self.H)
        self.pin: dict = {}
        self.owed: list[str] = []
        # race cell -> list of (dir, flags) (later entries win, as in Traversal.flowAt)
        self.rails: dict = {}
        self.solid_extra: set = set()     # object footprints (for the proof)
        self.home: tuple[int, int] | None = None
        for y, row in enumerate(self.plan):
            for x, c in enumerate(row):
                if c in DIRS:
                    self.rails.setdefault((x, y), []).append((DIRS[c], {}))

    # ---- queries ----------------------------------------------------------------
    def at(self, x: int, y: int) -> str:
        return self.plan[y][x]

    def cells(self, chars: str) -> list[tuple[int, int]]:
        return [(x, y) for y in range(self.H) for x in range(self.W) if self.plan[y][x] in chars]

    def is_race(self, c) -> bool:
        x, y = c
        return 0 <= x < self.W and 0 <= y < self.H and self.plan[y][x] in "><^vJ"

    def free(self, c) -> bool:
        """A cell you can stand or swim on freely (floor/shallows, no object body)."""
        x, y = c
        if not (0 <= x < self.W and 0 <= y < self.H):
            return False
        return self.plan[y][x] in ".,o=" and c not in self.solid_extra

    # ---- the lanes --------------------------------------------------------------------
    def junction(self, at, straight: str, turn: str, flag: str) -> None:
        """A junction pool: the current runs `straight` until `flag` is held,
        then `turn` (the turnout listed last wins)."""
        assert self.at(*at) == "J", (at, self.at(*at))
        self.rails[at] = [(straight, {"hidden_when_flag": flag}), (turn, {"requires_flag": flag})]

    def flow(self, at, d: str, flags: dict) -> None:
        """An extra switched flow on a race cell (listed after its plain one)."""
        self.rails.setdefault(at, []).append((d, dict(flags)))

    def _emit_flows(self) -> None:
        # group plain cells by (dir) into runs for compact data; switched cells
        # go one-per-flow, after the plain ones (so they win)
        plain: dict = {}
        switched = []
        for c, lst in sorted(self.rails.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            for i, (d, fl) in enumerate(lst):
                if fl:
                    switched.append((c, d, fl, i))
                else:
                    plain.setdefault(d, []).append(c)
        for d, cs in sorted(plain.items()):
            self.m["flows"].append({"id": f"race_{d}", "kind": "rail", "dir": d,
                                    "tiles": [{"tx": x, "ty": y} for (x, y) in cs]})
        for (c, d, fl, i) in switched:
            f = {"id": f"race_{c[0]}_{c[1]}_{d}", "kind": "rail", "dir": d,
                 "tiles": [{"tx": c[0], "ty": c[1]}]}
            f.update(fl)
            self.m["flows"].append(f)

    # ---- props ------------------------------------------------------------------------
    def obj(self, oid, sprite, at, w, h, *, solid_rows: int | None = None, **kw) -> None:
        o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
        o.update(kw)
        self.m["objects"].append(o)
        if o.get("solid") is False:
            return
        start = o.get("overhang", 0) if o.get("walk_under") else 0
        for dy in range(start, h):
            for dx in range(w):
                self.solid_extra.add((at[0] + dx, at[1] + dy))

    def bell(self, n: int, at, flag: str, ref: str) -> None:
        """A tide-bell (1x2: the crook walk-under, the post's foot solid) as a
        flag swap pair (still / swung) + the interact trigger on its foot."""
        x, y = at
        self.obj(f"bell_{n}", "undertide_bell", (x, y), 1, 2, overhang=1, walk_under=True,
                 hidden_when_flag=flag)
        self.obj(f"bell_{n}_rung", "undertide_bell_rung", (x, y), 1, 2, overhang=1,
                 walk_under=True, requires_flag=flag)
        self.m["triggers"].append({"id": f"bell_{n}", "kind": "script",
                                   "at": {"tx": x, "ty": y + 1}, "activation": "interact",
                                   "ref": ref})

    def post(self, n: int, at, flag: str) -> None:
        """A race-post beside a junction: white = straight on, red = the turn."""
        self.obj(f"post_{n}", "undertide_post_white", at, 1, 1, hidden_when_flag=flag)
        self.obj(f"post_{n}_red", "undertide_post_red", at, 1, 1, requires_flag=flag)

    def logbook(self, n: int, at) -> None:
        self.obj(f"logbook_{n}", "undertide_logbook", at, 1, 1)
        self.m["triggers"].append({"id": f"logbook_{n}", "kind": "script",
                                   "at": {"tx": at[0], "ty": at[1]}, "activation": "interact",
                                   "ref": f"script.undertide_log_{n}"})

    def cache(self, cid: str, at) -> None:
        self.m["npcs"].append({"id": f"cache_{cid}", "at": {"tx": at[0], "ty": at[1]},
                               "facing": "down", "sprite": "item_cache", "movement": "static",
                               "dialogue_ref": f"script.pickup_{cid}",
                               "hidden_when_flag": f"flag:picked_{cid}"})
        self.solid_extra.add(tuple(at))
        self.owed.append(f"script.pickup_{cid}")

    def trainer(self, tid: str, at, facing: str, sight: int, sprite: str) -> None:
        flag = f"flag:{tid}_beaten"
        self.m["npcs"].extend([
            {"id": tid, "at": {"tx": at[0], "ty": at[1]}, "facing": facing, "sprite": sprite,
             "movement": "static", "dialogue_ref": f"script.{tid}",
             "sight_range": sight, "defeated_flag": flag, "hidden_when_flag": flag},
            {"id": f"{tid}_after", "at": {"tx": at[0], "ty": at[1]}, "facing": facing,
             "sprite": sprite, "movement": "static", "dialogue_ref": f"npc.{tid}_after",
             "requires_flag": flag},
        ])
        self.solid_extra.add(tuple(at))

    def sign(self, sid: str, at) -> None:
        self.deco[at[1] * self.W + at[0]] = gid("sign")
        self.m["triggers"].append({"id": f"sign_{sid}", "kind": "sign",
                                   "at": {"tx": at[0], "ty": at[1]}, "activation": "interact",
                                   "ref": f"sign.{sid}"})
        self.solid_extra.add(tuple(at))

    def ladder(self, kind: str, at, to_map: str, to, wid: str | None = None) -> None:
        self.deco[at[1] * self.W + at[0]] = gid(f"cave_ladder_{kind}")
        self.m["warps"].append({"id": wid or f"ladder_{kind}", "at": {"tx": at[0], "ty": at[1]},
                                "trigger": "step_on", "to_map": to_map,
                                "to": {"tx": to[0], "ty": to[1]},
                                "facing": "down" if kind == "down" else "up",
                                "transition": "fade"})

    def edge_warp(self, wid: str, at, to_map: str, to, facing: str) -> None:
        self.m["warps"].append({"id": wid, "at": {"tx": at[0], "ty": at[1]},
                                "trigger": "step_on", "to_map": to_map,
                                "to": {"tx": to[0], "ty": to[1]}, "facing": facing,
                                "transition": "fade"})

    def put(self, x: int, y: int, name: str) -> None:
        self.deco[y * self.W + x] = U(name) if name in _IDX() else gid(name)

    def scatter(self, names: list[str], n: int, chars: str = ".", avoid: set | None = None) -> None:
        """Sprinkle decor on free floor, off every warp/trigger/NPC tile."""
        busy = set(avoid or ())
        for w in self.m["warps"]:
            busy.add((w["at"]["tx"], w["at"]["ty"]))
        for t in self.m["triggers"]:
            busy.add((t["at"]["tx"], t["at"]["ty"]))
        for p in self.m["npcs"]:
            busy.add((p["at"]["tx"], p["at"]["ty"]))
        cand = [c for c in self.cells(chars) if c not in busy and c not in self.solid_extra
                and not self.deco[c[1] * self.W + c[0]]]
        self.rng.shuffle(cand)
        for i, (x, y) in enumerate(cand[:n]):
            self.put(x, y, names[i % len(names)])


    # ---- pass 2: the surge dressed, the dawn's tide-lamps --------------------------
    def _footprint_ok(self, at, w, h, taken: set) -> bool:
        cells = [(at[0] + dx, at[1] + dy) for dy in range(h) for dx in range(w)]
        for (x, y) in cells:
            if not (0 <= x < self.W and 0 <= y < self.H):
                return False
            if self.plan[y][x] != "~" or (x, y) in taken:
                return False
        return True

    def _taken(self) -> set:
        t = set()
        for o in self.m["objects"]:
            for dy in range(o["h"]):
                for dx in range(o["w"]):
                    t.add((o["at"]["tx"] + dx, o["at"]["ty"] + dy))
        return t

    def tide_lamps(self, spacing: int = 6, flag: str = "flag:isles_dawn") -> int:
        """The keepers' tide-lamps along the races (1x2, on the surge right beside a
        lane): cold sea-glass until `flag`, then lit — a same-footprint flag swap."""
        taken = self._taken()
        lamps: list = []
        n = 0
        cells = sorted(self.rails, key=lambda c: (c[1], c[0]))
        for (x, y) in cells:
            for (bx, by) in ((x - 1, y), (x + 1, y), (x, y + 1)):
                top = (bx, by - 1)
                if not self._footprint_ok(top, 1, 2, taken):
                    continue
                if any(abs(bx - lx) + abs(by - ly) < spacing for (lx, ly) in lamps):
                    continue
                lamps.append((bx, by))
                for dy in (0, 1):
                    taken.add((bx, by - 1 + dy))
                n += 1
                self.m["objects"].append({"id": f"tidelamp_{n}", "sprite": "undertide_tidelamp",
                                          "at": {"tx": bx, "ty": by - 1}, "w": 1, "h": 2,
                                          "overhang": 1, "hidden_when_flag": flag})
                self.m["objects"].append({"id": f"tidelamp_{n}_lit", "sprite": "undertide_tidelamp_lit",
                                          "at": {"tx": bx, "ty": by - 1}, "w": 1, "h": 2,
                                          "overhang": 1, "requires_flag": flag})
                break
        return n

    # Each floor has its OWN surge palette (sprite, w, h, overhang) — the floors
    # read as different places, not one kit stamped four times.
    PALETTES = {
        "mouth": [("undertide_wreck", 2, 2, 1), ("undertide_stack", 1, 2, 1),
                  ("undertide_mast", 1, 3, 2), ("undertide_stack", 1, 2, 1)],
        "vaults": [("undertide_kelpcrown", 2, 1, 0), ("undertide_statue", 1, 2, 1),
                   ("undertide_kelpcrown", 2, 1, 0), ("undertide_stack", 1, 2, 1)],
        "galleries": [("undertide_bellframe", 2, 2, 1), ("undertide_chain", 1, 2, 1),
                      ("undertide_mast", 1, 3, 2), ("undertide_chain", 1, 2, 1)],
        "stair": [("undertide_stairfrag", 2, 1, 0), ("undertide_glassspire", 1, 2, 1),
                  ("undertide_lanternpost", 1, 2, 1), ("undertide_glassspire", 1, 2, 1)],
    }
    PROPS = PALETTES["mouth"]

    def dress_surge(self, per_screen: int = 3, gap: int = 2, palette: str = "mouth") -> int:
        """Break up the white water with this floor's own things (PALETTES),
        `per_screen` per 15x10 screen of surge, never on a lane or a pocket, `gap`
        tiles clear of each other."""
        self.PROPS = self.PALETTES[palette]
        taken = self._taken()
        placed: list = []
        n = 0
        for sy in range(0, self.H, 10):
            for sx in range(0, self.W, 15):
                cand = [(x, y) for y in range(sy, min(self.H, sy + 10))
                        for x in range(sx, min(self.W, sx + 15)) if self.plan[y][x] == "~"]
                self.rng.shuffle(cand)
                k = 0
                for (x, y) in cand:
                    if k >= per_screen:
                        break
                    sprite, w, h, ov = self.PROPS[(n + k + sx + sy) % len(self.PROPS)]
                    if not self._footprint_ok((x, y), w, h, taken):
                        continue
                    if any(abs(x - px) <= gap + 1 and abs(y - py) <= gap + 1 for (px, py) in placed):
                        continue
                    placed.append((x, y))
                    for dy in range(h):
                        for dx in range(w):
                            taken.add((x + dx, y + dy))
                    k += 1
                    self.m["objects"].append({"id": f"surge_{sprite[10:]}_{n + k}", "sprite": sprite,
                                              "at": {"tx": x, "ty": y}, "w": w, "h": h,
                                              "overhang": ov})
                n += k
        return n


    def organic_pools(self) -> int:
        """Round off the shallows (no box pools, no plus-signs): every pool is
        re-cut as the ellipse inscribed in its bounding box (3-wide pools just lose
        their corners) and stripped of one-tile tabs; the tidepool tiles' wide
        corner radius turns the stepped outline into a curve. Water only ever spreads onto plain floor —
        never onto an object, an NPC, a trigger, a warp or a tile beside a race.
        Call BEFORE prove() (it reshapes pockets)."""
        busy = set(self.solid_extra)
        for w in self.m["warps"]:
            busy.add((w["at"]["tx"], w["at"]["ty"]))
        for t in self.m["triggers"]:
            busy.add((t["at"]["tx"], t["at"]["ty"]))
        for n in self.m["npcs"]:
            busy.add((n["at"]["tx"], n["at"]["ty"]))
        for o in self.m["objects"]:
            for dy in range(o["h"]):
                for dx in range(o["w"]):
                    busy.add((o["at"]["tx"] + dx, o["at"]["ty"] + dy))

        def can_flood(x, y):
            return (1 <= x < self.W - 1 and 1 <= y < self.H - 1 and self.plan[y][x] == "."
                    and (x, y) not in busy
                    and not any(self.is_race((x + dx, y + dy)) for (dx, dy) in STEP.values()))

        comps, seen = [], set()
        for c in self.cells("o"):
            if c in seen:
                continue
            comp, q = {c}, [c]
            while q:
                x, y = q.pop()
                for (dx, dy) in STEP.values():
                    n = (x + dx, y + dy)
                    if n not in comp and 0 <= n[0] < self.W and 0 <= n[1] < self.H \
                            and self.plan[n[1]][n[0]] == "o":
                        comp.add(n)
                        q.append(n)
            seen |= comp
            comps.append(comp)
        changed = 0
        for comp in comps:
            xs = [x for x, _ in comp]
            ys = [y for _, y in comp]
            x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
            w, h = x1 - x0 + 1, y1 - y0 + 1
            if w < 3 or h < 2:
                continue
            cx, cy = (x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2
            target = {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
                      if ((x + 0.5 - cx) / (w / 2)) ** 2 + ((y + 0.5 - cy) / (h / 2)) ** 2 <= 1.0}
            if min(w, h) == 3:
                target -= {(x0, y0), (x1, y0), (x0, y1), (x1, y1)}
            for (x, y) in comp - target:
                self.plan[y][x] = "."
                changed += 1
            for (x, y) in target - comp:
                if can_flood(x, y):
                    self.plan[y][x] = "o"
                    changed += 1
            # a two-tile lobe off the longest side (off-centre): an uneven shore
            if max(w, h) >= 4:
                if w >= h:
                    mx = x0 + (w * 2) // 3 - 1
                    lobe = [(mx, y1 + 1), (mx + 1, y1 + 1)]
                else:
                    my = y0 + (h * 2) // 3 - 1
                    lobe = [(x1 + 1, my), (x1 + 1, my + 1)]
                if all(can_flood(x, y) for (x, y) in lobe):
                    for (x, y) in lobe:
                        self.plan[y][x] = "o"
                        changed += 1
            # prune stubs: a pool tile with one (or no) water neighbour reads as a tab
            while True:
                stubs = [(x, y) for (x, y) in self.cells("o")
                         if x0 - 1 <= x <= x1 + 1 and y0 - 1 <= y <= y1 + 1
                         and sum(self.plan[y + dy][x + dx] == "o" for (dx, dy) in STEP.values()) <= 1]
                if not stubs:
                    break
                for (x, y) in stubs:
                    self.plan[y][x] = "."
                    changed += 1
        return changed

    # ---- zones -------------------------------------------------------------------------
    def zone(self, zid: str, terrain: str, rect, table: list, rate: float = 0.1,
             day: list | None = None) -> None:
        """An encounter zone. With `day`, a NIGHT/DAY pair (the R4 day-form pattern):
        the night table hides at `flag:isles_dawn` and its `_day` twin rises with it."""
        x0, y0, x1, y1 = rect
        cells = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
        bad = [c for c in cells if self.is_race(c)]
        assert not bad, (zid, "a zone must never cover a tide-race lane", bad[:4])
        r = {"tx": x0, "ty": y0, "w": x1 - x0 + 1, "h": y1 - y0 + 1}
        z = {"id": zid, "terrain": terrain, "rect": r, "encounter_rate": rate, "table": table}
        if day is not None:
            z["hidden_when_flag"] = DAWN
        self.m["encounters"].append(z)
        if day is not None:
            self.m["encounters"].append({"id": zid + "_day", "terrain": terrain, "rect": dict(r),
                                         "encounter_rate": rate, "table": day,
                                         "requires_flag": DAWN})

    # ---- the proof ---------------------------------------------------------------------
    def flags(self) -> list[str]:
        fl = set()
        for lst in self.rails.values():
            for _, f in lst:
                fl |= {v for k, v in f.items() if k in ("requires_flag", "hidden_when_flag")}
        return sorted(fl)

    def flow_dir(self, c, state: dict):
        for d, fl in reversed(self.rails.get(c, [])):
            if "requires_flag" in fl and not state[fl["requires_flag"]]:
                continue
            if "hidden_when_flag" in fl and state[fl["hidden_when_flag"]]:
                continue
            return d
        return None

    def ride(self, start, state: dict):
        """Ride a lane from `start` (a race cell); returns the free cell it ends on."""
        c, seen = start, set()
        while (d := self.flow_dir(c, state)) is not None:
            assert c not in seen, ("race loop", c, state)
            seen.add(c)
            n = (c[0] + STEP[d][0], c[1] + STEP[d][1])
            if not self.free(n) and not self.is_race(n):
                raise AssertionError(f"{self.m['id']}: race stalls against rock at {c} -> {n} {state}")
            c = n
        assert self.free(c), (f"{self.m['id']}: race ends off a free cell", start, c, state)
        return c

    def pockets(self) -> dict:
        """Free cells -> pocket id (flood over free cells, 4-neighbour)."""
        pid, out = 0, {}
        for c in [(x, y) for y in range(self.H) for x in range(self.W)]:
            if c in out or not self.free(c):
                continue
            q = deque([c])
            out[c] = pid
            while q:
                x, y = q.popleft()
                for (dx, dy) in STEP.values():
                    n = (x + dx, y + dy)
                    if n not in out and self.free(n):
                        out[n] = pid
                        q.append(n)
            pid += 1
        return out

    def links(self, state: dict) -> dict:
        """pocket -> set of pockets a lane carries you to, in `state`."""
        pk = self.pockets()
        out: dict = {}
        for c, p in pk.items():
            for d, (dx, dy) in STEP.items():
                n = (c[0] + dx, c[1] + dy)
                if not self.is_race(n):
                    continue
                fd = self.flow_dir(n, state)
                if fd is None or fd == OPP[d]:
                    continue            # can't enter a lane against its current
                end = self.ride(n, state)
                out.setdefault(p, set()).add(pk[end])
        return out

    def states(self):
        fl = self.flags()
        for bits in itertools.product((False, True), repeat=len(fl)):
            yield dict(zip(fl, bits))

    def pocket_of(self, c) -> int:
        return self.pockets()[c]

    def prove(self) -> None:
        assert self.home is not None
        pk = self.pockets()
        home = pk[self.home]
        n = 0
        for st in self.states():
            ln = self.links(st)
            for p in set(pk.values()):
                seen, q = {p}, deque([p])
                while q:
                    a = q.popleft()
                    for b in ln.get(a, ()):
                        if b not in seen:
                            seen.add(b)
                            q.append(b)
                assert home in seen, (f"{self.m['id']}: SOFTLOCK — pocket {p} "
                                      f"(e.g. {next(c for c, v in pk.items() if v == p)}) "
                                      f"never races home in {st}")
            n += 1
        print(f"  tide-race proof: {n} bell state(s), every lane lands, every pocket races home")

    def reach(self, start, state: dict) -> set:
        ln = self.links(state)
        pk = self.pockets()
        s = pk[start]
        seen, q = {s}, deque([s])
        while q:
            a = q.popleft()
            for b in ln.get(a, ()):
                if b not in seen:
                    seen.add(b)
                    q.append(b)
        return seen

    # ---- write ---------------------------------------------------------------------
    def finish(self, *, floor_mix: float = 0.5) -> None:
        W, H = self.W, self.H
        cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
        base = [self.rng.choice(cf) if self.rng.random() < floor_mix else cf[0] for _ in range(W * H)]
        wall = mk.make_grid(W, H)
        surge = mk.make_grid(W, H)
        pool = mk.make_grid(W, H)
        ruin = mk.make_grid(W, H)
        for y in range(H):
            for x in range(W):
                c = self.plan[y][x]
                i = y * W + x
                if c == "#":
                    wall[i] = 1
                elif c in "~><^vJ":
                    surge[i] = 1
                elif c == "o":
                    pool[i] = 1
                elif c == "=":
                    ruin[i] = 1
                elif c == ".":
                    self.pin[(x, y)] = f"wetstone_{(x * 7 + y * 3) % 3}"
        for c, lst in self.rails.items():
            if self.plan[c[1]][c[0]] == "J":
                self.pin[c] = "race_fork"
            else:
                self.pin[c] = f"race_{lst[0][0]}"
        layers = [{"name": "base", "role": "base", "depth": 0, "data": base}]
        if any(ruin):
            layers.append({"name": "t_ruin", "role": "terrain", "terrain": "ruinfloor",
                           "set": "vesper_overworld_set", "depth": 0, "data": ruin})
        if any(pool):
            layers.append({"name": "t_tidepool", "role": "terrain", "terrain": "tidepool",
                           "set": SET, "depth": 0, "data": pool})
        if any(surge):
            layers.append({"name": "t_surge", "role": "terrain", "terrain": "surge",
                           "set": SET, "depth": 0, "data": surge})
        layers += [
            {"name": "t_cavewall", "role": "terrain", "terrain": "cavewall",
             "set": "vesper_overworld_set", "depth": 0, "data": wall},
            {"name": "deco", "role": "deco", "depth": 5, "data": self.deco},
            {"name": "above", "role": "above", "depth": 20, "data": self.above},
        ]
        self.m["layers"] = layers
        self._emit_flows()

    def build(self) -> int:
        ok = mk.finalize(self.m, scale=3, pin_base={k: v for k, v in self.pin.items()})
        if self.owed:
            print("CONTENT OWED:", sorted(set(self.owed)))
        print("PASS" if ok else "FAIL")
        return 0 if ok else 1


_IDX_CACHE: dict = {}


def _IDX() -> dict:
    if not _IDX_CACHE:
        import json
        _IDX_CACHE.update(json.loads(INDEX.read_text()))
    return _IDX_CACHE
