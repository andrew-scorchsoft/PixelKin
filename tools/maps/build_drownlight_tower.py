#!/usr/bin/env python3
"""
THE DROWNLIGHT — the first lamp the Hollowing put out (walkthrough/11-the-hollowing-
country.md Part B, lane N2). The tower above `drownlight_beacon` (its foot: the ruined
quay + the door, build_drownlight_beacon.py):

  drownlight_f1       The Oil Stores    lv 50-52  in from the foot's door; up NE
  drownlight_f2       The Lens Gallery  lv 51-53  dn NE / up NW (the up-stair from
                                                  F1 wants EMBERWARD: coldfog pools
                                                  in the stairwell)
  drownlight_lantern  The Lantern Room            dn NW — the SHUTTERKEEPER

Fourteen winters ago — three before the sky went dark — the Drownlight's keeper
banked its lamp low and bolted iron shutters round it. A keeper never kills a
lamp, so it still burns, behind iron; and its light still runs down the tower
through the keepers' old LIGHT-WELLS (the mirror-shafts that carried lamplight
down to warm each floor at night). After so long in the dark, that leak is a
GLARE no eye will walk through.

THE SHUTTER PUZZLE (the Old Seams/Undertide invariant). A SHUTTER-CRANK on a wall
swings one louvre: with its flag unset the light pours down one well, thrown it
pours down another. Each lit well blazes across ONE doorway; walking into the
glare is a pushback band (a step_on cutscene per doorway cell that steps you back
the way you came — audit_journey models it as a barrier). Every doorway has
exactly ONE source (a step_on tile carries one trigger: a requires_flag one stays
present when unmet, so it would swallow a second). The glare and the well's mouth
are flag-swapped objects (visual only — the bands are the collision).

`prove()` runs on every floor, on the REAL tile grid (walls, solid objects, NPC
bodies, beam cells), over every shutter state:
  * from every (position, state) reachable from the entrance, the entrance and
    the floor's goal stay reachable (cranking allowed) — NEVER a softlock;
  * a MONOTONIC solution exists (each crank thrown at most once, unset -> set) —
    what audit_journey's add-only flag replay can follow;
  * every cache/NPC/crank face is reachable in some state;
  * no crank face, landing or push target is ever a beam cell.

  F1 (teaching):  S1 (west store) swings the glare E-door <-> W-door; S2 (hall)
                  swings it store/stair-door <-> nook-door. Solution: S2, W, N.
                  The nook (the Starglass Shard) is dark only before S2 is thrown.
  F2 (the gallery ring): A (arrival) d <-> a, B (east gallery) b <-> c,
                  C (south gallery) e <-> f. The direct way north is double-
                  barred; you go round the south to open it: a, B, b, C, b, a,
                  A, d, e (+ the Lumen Drop in the west gallery, before C).

Run:  python3 tools/maps/build_drownlight_tower.py
"""
from __future__ import annotations

import itertools
from collections import deque
from pathlib import Path

from roomkit import (COOL_SET, CAP_S, DOORMAT, FACE, FLOOR, FLOOR_B, finish, mapdef,
                     place, wall_mount)

REPO = Path(__file__).resolve().parents[2]
FOOT_DOOR = ((4, 7), (5, 7))       # the tower door on drownlight_beacon (both art tiles)
MUSIC = "assets/audio/music/drownlight-{}.mp3"
BACKDROP = "assets/backgrounds/battle/drownlight-a.webp"
BACKDROP_LANTERN = "assets/backgrounds/battle/drownlight-lantern-a.webp"
F = "flag:drownlight_shutter_{}"

# ---- the wild tables (MIRRORED in tools/balance/build_species.py DROWNLIGHT_TABLES;
# keep both in step). Dark/Light/Frost of the north + the Hollowing's own family
# (#178 the snuffer-cap, #179 the shuttered lantern-keeper, #180 the dream-moth —
# lane N4's kin). (kin, weight, lo, hi)
TABLES = {
    "drownlight_f1": [(137, 24, 50, 51), (136, 14, 50, 51), (134, 18, 50, 52),
                      (85, 14, 51, 52), (178, 22, 50, 52), (180, 8, 51, 52)],
    "drownlight_f2": [(138, 20, 51, 53), (135, 8, 52, 53), (87, 14, 51, 53),
                      (85, 12, 51, 53), (178, 20, 51, 53), (180, 18, 51, 53),
                      (179, 8, 53, 53)],
}


def tileset(name: str) -> dict:
    if not (REPO / f"public/assets/tilesets/{name}.tileset.json").is_file():
        return COOL_SET
    return dict(COOL_SET, name=name, image=f"assets/tilesets/{name}.webp")


class Floor:
    """A tower floor on a char plan ('#' wall, '.' floor) + roomkit furniture."""

    def __init__(self, mid, name, plan, ts, music, backdrop):
        self.W, self.H = len(plan[0]), len(plan)
        assert all(len(r) == self.W for r in plan), [len(r) for r in plan]
        self.plan = plan
        self.mid = mid
        W, H = self.W, self.H
        self.base = [FLOOR if (x + y) % 2 else FLOOR_B for y in range(H) for x in range(W)]
        self.over = [0] * (W * H)
        for y in range(H):
            for x in range(W):
                if plan[y][x] != "#":
                    continue
                below = y + 1 < H and plan[y + 1][x] != "#"
                above = y == 0 or plan[y - 1][x] == "#"
                self.over[y * W + x] = FACE if (below and above) else CAP_S
        self.objects, self.warps, self.triggers, self.npcs = [], [], [], []
        self.m = mapdef(mid, name, W, H, tileset(ts), self.base, self.over,
                        self.objects, self.warps, self.triggers, self.npcs, music)
        self.m["battle_backdrops"] = [backdrop]
        self.solid: set = set()          # object/NPC bodies (for the proof)
        self.doors: dict = {}            # door id -> [(cell, push_to)]
        self.cranks: dict = {}           # crank id -> (face tile, unset door, set door)
        self.must_reach: list = []       # (label, tile adjacent-reach)
        self.entry = None
        self.goal = None

    # ---- queries ---------------------------------------------------------------
    def open(self, c) -> bool:
        x, y = c
        return 0 <= x < self.W and 0 <= y < self.H and self.plan[y][x] != "#" \
            and c not in self.solid

    # ---- furniture -------------------------------------------------------------
    def obj(self, oid, sprite, at, w, h, *, solid_rows=None, **kw):
        o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
        o.update(kw)
        self.objects.append(o)
        if o.get("solid") is False:
            return o
        start = o.get("overhang", 0) if o.get("walk_under") else 0
        for dy in range(start, h):
            for dx in range(w):
                self.solid.add((at[0] + dx, at[1] + dy))
        return o

    def piece(self, stem, at, oid=None, solid=True):
        o = place(self.objects, stem, at[0], at[1], oid=oid, solid=solid)
        if solid:
            for dy in range(o["h"]):
                for dx in range(o["w"]):
                    self.solid.add((at[0] + dx, at[1] + dy))
        return o

    def mount(self, stem, x, face_row, oid=None, solid=True):
        o = wall_mount(self.objects, stem, x, face_row=face_row, oid=oid, solid=solid)
        if solid:
            for dy in range(1, o["h"]):
                for dx in range(o["w"]):
                    self.solid.add((x + dx, face_row + dy))
        return o

    def read(self, tid, at, ref, kind="sign"):
        self.triggers.append({"id": tid, "kind": kind, "at": {"tx": at[0], "ty": at[1]},
                              "activation": "interact", "ref": ref})

    def cache(self, cid, at):
        self.npcs.append({"id": f"cache_{cid}", "at": {"tx": at[0], "ty": at[1]},
                          "facing": "down", "sprite": "item_cache", "movement": "static",
                          "dialogue_ref": f"script.pickup_{cid}",
                          "hidden_when_flag": f"flag:picked_{cid}"})
        self.solid.add(tuple(at))
        self.must_reach.append((f"cache {cid}", at))

    def trainer(self, tid, at, facing, sight, sprite="hollowing_acolyte"):
        flag = f"flag:{tid}_beaten"
        self.npcs += [
            {"id": tid, "at": {"tx": at[0], "ty": at[1]}, "facing": facing, "sprite": sprite,
             "movement": "static", "dialogue_ref": f"script.{tid}", "sight_range": sight,
             "defeated_flag": flag, "hidden_when_flag": flag},
            {"id": f"{tid}_after", "at": {"tx": at[0], "ty": at[1]}, "facing": facing,
             "sprite": sprite, "movement": "look_around", "dialogue_ref": f"npc.{tid}_after",
             "requires_flag": flag},
        ]
        self.solid.add(tuple(at))
        self.must_reach.append((f"trainer {tid}", at))

    def zone(self, zid, rect, rate=0.06):
        x0, y0, x1, y1 = rect
        self.m["encounters"].append({
            "id": zid, "terrain": "cave",
            "rect": {"tx": x0, "ty": y0, "w": x1 - x0 + 1, "h": y1 - y0 + 1},
            "encounter_rate": rate,
            "table": [{"kin_id": k, "weight": w, "min_level": lo, "max_level": hi}
                      for (k, w, lo, hi) in TABLES[self.mid]]})

    # ---- the shutter kit -------------------------------------------------------
    def door(self, did, cells, axis, well):
        """A doorway that can carry glare: `cells` = [(cell, push_to)] in walk
        order; `axis` 'h' (light runs side to side: a gap in an N/S wall) or 'v';
        `well` = the light-well's mouth on the wall beside/above it."""
        self.doors[did] = {"cells": cells, "axis": axis, "well": well}

    def crank(self, n, at, unset_door, set_door, label):
        """A shutter-crank 1x2 on a wall face (`at` = the face tile; its foot is
        the floor tile below, where the trigger sits). Flag F(n)."""
        x, y = at
        fl = F.format(n)
        for sprite, cond in (("drownlight_crank", "hidden_when_flag"),
                             ("drownlight_crank_on", "requires_flag")):
            self.obj(f"crank_{n}" + ("_on" if cond == "requires_flag" else ""), sprite,
                     (x, y), 1, 2, overhang=1, walk_under=True, **{cond: fl})
        self.read(f"crank_{n}", (x, y + 1), f"script.drownlight_crank_{n}", kind="cutscene")
        self.cranks[n] = {"face": (x, y + 2), "unset": unset_door, "set": set_door,
                          "label": label}

    def wire(self):
        """Lay each door's glare + well (both states) and its pushback bands."""
        for n, c in self.cranks.items():
            fl = F.format(n)
            for state, did in (("unset", c["unset"]), ("set", c["set"])):
                d = self.doors[did]
                cond = {"hidden_when_flag": fl} if state == "unset" else {"requires_flag": fl}
                anti = {"requires_flag": fl} if state == "unset" else {"hidden_when_flag": fl}
                wx, wy = d["well"]
                self.obj(f"well_{did}_lit", "drownlight_well_lit", (wx, wy), 1, 1,
                         solid=False, **cond)
                self.obj(f"well_{did}", "drownlight_well", (wx, wy), 1, 1, solid=False, **anti)
                for i, ((cx, cy), _push) in enumerate(d["cells"]):
                    self.obj(f"glare_{did}_{i}", f"drownlight_glare_{d['axis']}", (cx, cy),
                             1, 1, solid=False, **cond)
                    t = {"id": f"glare_{did}_{i}", "kind": "cutscene",
                         "at": {"tx": cx, "ty": cy}, "activation": "step_on",
                         "ref": f"script.drownlight_glare_{self.short}_{did}{i}"}
                    t.update(cond)
                    self.triggers.append(t)

    # ---- the proof -------------------------------------------------------------
    def beams(self, st: dict) -> set:
        out = set()
        for n, c in self.cranks.items():
            did = c["set"] if st[n] else c["unset"]
            out |= {cell for (cell, _p) in self.doors[did]["cells"]}
        return out

    def reach(self, start, st) -> set:
        bl = self.beams(st)
        seen, q = {start}, deque([start])
        while q:
            x, y = q.popleft()
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + d[0], y + d[1])
                if n not in seen and self.open(n) and n not in bl:
                    seen.add(n)
                    q.append(n)
        return seen

    def prove(self):
        names = sorted(self.cranks)
        # sanity: crank faces / push targets / landing never on a beam cell
        all_beams = {cell for d in self.doors.values() for (cell, _p) in d["cells"]}
        for n, c in self.cranks.items():
            assert c["face"] not in all_beams and self.open(c["face"]), (self.mid, n, c["face"])
        for did, d in self.doors.items():
            for (cell, push) in d["cells"]:
                assert self.open(cell), (self.mid, did, cell)
                assert self.open(push) and push not in all_beams, (self.mid, did, push)
                assert abs(cell[0] - push[0]) + abs(cell[1] - push[1]) == 1, (did, cell, push)
        assert self.entry not in all_beams and self.goal not in all_beams

        def nodes_from(start, st0, mono=False):
            """Every (tile, state) reachable: walk within the state's open region,
            crank at any crank face in it (mono: only ever unset -> set)."""
            seen: set = set()
            q = deque([(start, tuple(st0[k] for k in names))])
            while q:
                pos, bits = q.popleft()
                if (pos, bits) in seen:
                    continue
                region = self.reach(pos, dict(zip(names, bits)))
                seen |= {(r, bits) for r in region}
                for i, n in enumerate(names):
                    face = self.cranks[n]["face"]
                    if face in region and not (mono and bits[i]):
                        b2 = list(bits)
                        b2[i] = not b2[i]
                        if (face, tuple(b2)) not in seen:
                            q.append((face, tuple(b2)))
            return seen

        start = {k: False for k in names}
        full = nodes_from(self.entry, start)
        tiles = {p for (p, _b) in full}
        assert self.goal in tiles, f"{self.mid}: goal unreachable"
        # every reached (tile, state): the entrance AND the goal stay reachable
        checked = {}
        for (pos, bits) in full:
            key = (frozenset(self.reach(pos, dict(zip(names, bits)))), bits)
            if key in checked:
                continue
            sub = nodes_from(pos, dict(zip(names, bits)))
            got = {p for (p, _b) in sub}
            ok = self.entry in got and self.goal in got
            checked[key] = ok
            assert ok, f"{self.mid}: SOFTLOCK at {pos} {dict(zip(names, bits))}"
        mono = nodes_from(self.entry, start, mono=True)
        assert self.goal in {p for (p, _b) in mono}, f"{self.mid}: no monotonic solution"
        mono_tiles = {p for (p, _b) in mono}
        for label, (x, y) in self.must_reach:
            adj = {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}
            assert adj & mono_tiles, f"{self.mid}: {label} unreachable (monotonic)"
        print(f"  shutter proof {self.mid}: {2 ** len(names)} states, {len(checked)} regions "
              f"checked — no softlock, goal + entrance always reachable, monotonic solution ok")

    def done(self):
        self.wire()
        self.prove()
        return self.m


# =====================================================================================
# F1 — THE OIL STORES
# =====================================================================================
F1_PLAN = [
    "######################",
    "######################",
    "###.......##.......###",
    "##........##........##",
    "##..................##",
    "##........##........##",
    "##........##........##",
    "#######.########.#####",
    "#######.########.#####",
    "######..............##",
    "######..............##",
    "#...##..............##",
    "#...................##",
    "#...##..............##",
    "##..##..............##",
    "######################",
]


def floor_1():
    fl = Floor("drownlight_f1", "The Drownlight — The Oil Stores", F1_PLAN,
               "drownlight_f1_set", MUSIC.format("f1"), BACKDROP)
    fl.short = "f1"
    W, H = fl.W, fl.H
    # the street door (the foot's quay) — walk onto the doormat
    fl.base[(H - 1) * W + 11] = DOORMAT
    fl.over[(H - 1) * W + 11] = 0
    fl.warps.append({"id": "to_foot", "at": {"tx": 11, "ty": H - 1}, "trigger": "step_on",
                     "to_map": "drownlight_beacon", "to": {"tx": 4, "ty": 8},
                     "facing": "down", "transition": "door"})
    fl.entry = (11, H - 2)
    # the up-stair (NE) wants Emberward: coldfog pools in the stairwell
    fl.base[2 * W + 18] = DOORMAT
    fl.warps.append({"id": "up_stairs", "at": {"tx": 18, "ty": 2}, "trigger": "step_on",
                     "to_map": "drownlight_f2", "to": {"tx": 19, "ty": 3}, "facing": "down",
                     "transition": "fade", "requires_ability": "emberward",
                     "blocked_ref": "sign.drownlight_stair_fog"})
    fl.goal = (18, 3)
    # ---- the doors that can carry glare --------------------------------------
    fl.door("E", [((16, 7), (16, 6)), ((16, 8), (16, 9))], "h", (15, 8))
    fl.door("W", [((7, 7), (7, 6)), ((7, 8), (7, 9))], "h", (6, 8))
    fl.door("N", [((10, 4), (9, 4)), ((11, 4), (12, 4))], "v", (10, 3))
    fl.door("K", [((4, 12), (3, 12)), ((5, 12), (6, 12))], "v", (4, 11))
    fl.crank(1, (4, 1), "E", "W", "the store crank")
    fl.crank(2, (10, 8), "N", "K", "the hall crank")
    # ---- THE WEST STORE (oil, wick, the keepers' patience) -------------------
    fl.mount("shelf", 8, 1, oid="wick_shelf")
    fl.read("wick_shelf_read", (8, 3), "sign.drownlight_wick_shelf")
    fl.piece("oil_jars", (2, 6), oid="oil_jars")
    fl.read("oil_jars_read", (2, 6), "sign.drownlight_oil_jars")
    fl.piece("barrels", (8, 6), oid="barrels")
    fl.trainer("drownlight_acolyte_odell", (6, 3), "down", 3)
    # ---- THE STAIR ROOM ------------------------------------------------------
    fl.mount("lamp_rack", 13, 1, oid="lamp_rack")
    fl.read("lamp_rack_read", (13, 2), "sign.drownlight_lamp_rack")
    fl.obj("lens_spare", "drownlight_lens_spare", (18, 5), 2, 2)
    fl.read("lens_spare_read", (18, 5), "sign.drownlight_lens_spare")
    fl.obj("shutter_plate_n", "drownlight_shutter_plate", (15, 1), 1, 1, solid=False)
    fl.read("shutter_plate_n_read", (15, 1), "sign.drownlight_shutter_plate")
    # ---- THE HALL (the keepers' mess) ----------------------------------------
    fl.obj("names_slate", "drownlight_slate", (12, 8), 2, 1, solid=False)
    for x in (12, 13):
        fl.read(f"slate_{x}", (x, 8), "script.drownlight_slate_keepers", kind="cutscene")
    fl.mount("stove", 17, 8, oid="kept_stove")
    fl.read("stove_read", (17, 9), "sign.drownlight_stove")
    fl.piece("table", (8, 11), oid="mess_table")
    fl.piece("stool", (7, 12), oid="stool_w")
    fl.piece("stool", (10, 12), oid="stool_e")
    fl.read("mess_table_read", (8, 11), "sign.drownlight_mess_table")
    fl.piece("desk", (16, 13), oid="log_desk")
    for x in (16, 17):
        fl.read(f"log_{x}", (x, 13), "script.drownlight_log", kind="cutscene")
    fl.piece("crates", (18, 11), oid="crates")
    # THE NOOK — dark only before the hall crank is thrown
    fl.cache("drownlight_shard", (2, 13))
    fl.piece("sacks", (1, 11), oid="nook_sacks")
    # the first-steps beat: once, on the row in from the door
    fl.triggers.append({"id": "first_steps", "kind": "cutscene", "at": {"tx": 11, "ty": 13},
                        "activation": "step_on", "ref": "script.drownlight_first_steps",
                        "hidden_when_flag": "flag:drownlight_entered"})
    for x in (10, 12):
        fl.triggers.append({"id": f"first_steps_{x}", "kind": "cutscene",
                            "at": {"tx": x, "ty": 13}, "activation": "step_on",
                            "ref": "script.drownlight_first_steps",
                            "hidden_when_flag": "flag:drownlight_entered"})
    fl.zone("store", (2, 2, 9, 6))
    fl.zone("stair_room", (12, 2, 19, 6))
    fl.zone("hall", (6, 9, 19, 14), rate=0.05)
    return fl.done()


# =====================================================================================
# F2 — THE LENS GALLERY
# =====================================================================================
F2_PLAN = [
    "######################",
    "######################",
    "##....##......##....##",
    "#.....##......##.....#",
    "#....................#",
    "#.....##......##.....#",
    "#.....##......##.....#",
    "###.##############.###",
    "###.##############.###",
    "#.....##......##.....#",
    "#.....##......##.....#",
    "#....................#",
    "#.....##......##.....#",
    "#.....##......##.....#",
    "##....##......##....##",
    "######################",
]


def floor_2():
    fl = Floor("drownlight_f2", "The Drownlight — The Lens Gallery", F2_PLAN,
               "drownlight_f2_set", MUSIC.format("f2"), BACKDROP)
    fl.short = "f2"
    W = fl.W
    fl.base[2 * W + 19] = DOORMAT
    fl.warps.append({"id": "down_stairs", "at": {"tx": 19, "ty": 2}, "trigger": "step_on",
                     "to_map": "drownlight_f1", "to": {"tx": 18, "ty": 3}, "facing": "down",
                     "transition": "fade"})
    fl.entry = (19, 3)
    fl.base[2 * W + 2] = DOORMAT
    fl.warps.append({"id": "up_stairs", "at": {"tx": 2, "ty": 2}, "trigger": "step_on",
                     "to_map": "drownlight_lantern", "to": {"tx": 3, "ty": 3}, "facing": "down",
                     "transition": "fade"})
    fl.goal = (2, 3)
    fl.door("d", [((14, 4), (13, 4)), ((15, 4), (16, 4))], "v", (14, 3))
    fl.door("e", [((6, 4), (5, 4)), ((7, 4), (8, 4))], "v", (6, 3))
    fl.door("a", [((18, 7), (18, 6)), ((18, 8), (18, 9))], "h", (19, 8))
    fl.door("c", [((3, 7), (3, 6)), ((3, 8), (3, 9))], "h", (2, 8))
    fl.door("b", [((14, 11), (13, 11)), ((15, 11), (16, 11))], "v", (14, 10))
    fl.door("f", [((6, 11), (5, 11)), ((7, 11), (8, 11))], "v", (6, 10))
    fl.crank("a", (17, 1), "d", "a", "the arrival crank")
    fl.crank("b", (17, 8), "b", "c", "the east gallery crank")
    fl.crank("c", (11, 8), "e", "f", "the south gallery crank")
    # ---- ARRIVAL (NE): the keepers' watch-cot — the tower's rest point -------
    fl.obj("watch_cot", "drownlight_cot", (20, 5), 1, 2)
    for y in (5, 6):
        fl.read(f"cot_{y}", (20, y), "script.drownlight_cot", kind="cutscene")
    fl.obj("shutter_plate_ne", "drownlight_shutter_plate", (18, 1), 1, 1, solid=False)
    fl.read("shutter_plate_ne_read", (18, 1), "sign.drownlight_shutter_plate_b")
    # ---- THE LENS STORE (north-middle) ---------------------------------------
    fl.obj("lens_store", "drownlight_lens_spare", (10, 2), 2, 2)
    fl.read("lens_store_read", (10, 3), "sign.drownlight_lens_store")
    fl.read("lens_store_read_b", (11, 3), "sign.drownlight_lens_store")
    fl.mount("bookcase", 8, 1, oid="log_case")
    fl.read("log_case_read", (8, 3), "script.drownlight_log_two", kind="cutscene")
    fl.read("log_case_read_b", (9, 3), "script.drownlight_log_two", kind="cutscene")
    # ---- THE STAIR ROOM (NW) ---------------------------------------------------
    fl.obj("names_slate", "drownlight_slate", (4, 1), 2, 1, solid=False)
    for x in (4, 5):
        fl.read(f"slate_{x}", (x, 1), "script.drownlight_slate_shutters", kind="cutscene")
    fl.piece("oil_jars", (1, 6), oid="oil_jars")
    # ---- THE EAST GALLERY (SE) ------------------------------------------------
    fl.trainer("drownlight_acolyte_prue", (20, 10), "left", 4)
    fl.piece("crates", (19, 13), oid="crates")
    # ---- THE SOUTH GALLERY ------------------------------------------------------
    fl.trainer("drownlight_acolyte_hask", (9, 13), "up", 2)
    fl.piece("pew", (11, 13), oid="watch_bench")
    fl.read("watch_bench_read", (12, 13), "sign.drownlight_watch_bench")
    fl.obj("gallery_lens", "drownlight_lens_spare", (12, 9), 2, 2)
    fl.read("gallery_lens_read", (12, 10), "sign.drownlight_gallery_lens")
    fl.piece("sacks", (16, 14), oid="se_sacks")
    fl.piece("sacks", (1, 10), oid="sw_sacks")
    # ---- THE WEST GALLERY (SW) — the Lumen Drop, before C is thrown -----------
    fl.cache("drownlight_drop", (2, 13))
    fl.obj("shutter_plate_sw", "drownlight_shutter_plate", (1, 8), 1, 1, solid=False)
    fl.read("shutter_plate_sw_read", (1, 8), "sign.drownlight_shutter_plate_c")
    fl.piece("barrels", (4, 13), oid="barrels")
    fl.zone("ne", (16, 2, 20, 6))
    fl.zone("nm", (8, 2, 13, 6))
    fl.zone("nw", (1, 2, 5, 6))
    fl.zone("se", (16, 9, 20, 14))
    fl.zone("s", (8, 9, 13, 14))
    fl.zone("sw", (1, 9, 5, 14))
    m = fl.done()
    return m


# =====================================================================================
# THE LANTERN ROOM — the Shutterkeeper
# =====================================================================================
LANTERN_PLAN = [
    "################",
    "################",
    "###..........###",
    "##............##",
    "#..............#",
    "#..............#",
    "#..............#",
    "#..............#",
    "#..............#",
    "#..............#",
    "##............##",
    "################",
]


def lantern():
    fl = Floor("drownlight_lantern", "The Drownlight — The Lantern Room", LANTERN_PLAN,
               "drownlight_lantern_set", MUSIC.format("lantern"), BACKDROP_LANTERN)
    fl.short = "lantern"
    W = fl.W
    fl.base[2 * W + 3] = DOORMAT
    fl.warps.append({"id": "down_stairs", "at": {"tx": 3, "ty": 2}, "trigger": "step_on",
                     "to_map": "drownlight_f2", "to": {"tx": 2, "ty": 3}, "facing": "down",
                     "transition": "fade"})
    fl.entry = (3, 3)
    # THE GREAT LAMP: banked behind its shutters; alight after the relight
    for sprite, cond in (("drownlight_great_lamp", {"hidden_when_flag": "flag:drownlight_relit"}),
                         ("drownlight_great_lamp_lit", {"requires_flag": "flag:drownlight_relit"})):
        fl.obj(sprite[11:], sprite, (6, 3), 4, 4, overhang=1, walk_under=True, **cond)
    for x in (6, 7, 8, 9):
        fl.read(f"lamp_{x}", (x, 6), "script.drownlight_lamp", kind="cutscene")
    fl.goal = (7, 7)
    # the lantern's glazing: storm-panes all round the wall face (dawn through
    # them once the lamp is relit — the sky is awake by then)
    for x in (5, 8, 12):
        for sprite, cond in (("drownlight_pane", {"hidden_when_flag": "flag:dawn"}),
                             ("drownlight_pane_lit", {"requires_flag": "flag:dawn"})):
            fl.obj(f"pane_{x}" + ("_lit" if "requires_flag" in cond else ""), sprite, (x, 1),
                   1, 1, solid=False, **cond)
    for (x, y) in ((1, 3), (14, 3)):
        for sprite, cond in (("drownlight_pane", {"hidden_when_flag": "flag:dawn"}),
                             ("drownlight_pane_lit", {"requires_flag": "flag:dawn"})):
            fl.obj(f"pane_{x}_{y}" + ("_lit" if "requires_flag" in cond else ""), sprite,
                   (x, y), 1, 1, solid=False, **cond)
    fl.read("pane_read", (8, 1), "script.drownlight_pane", kind="cutscene")
    # THE SHUTTERKEEPER: before the bout / after it (staged on the dawn + the relight)
    fl.npcs += [
        {"id": "shutterkeeper", "at": {"tx": 8, "ty": 8}, "facing": "up",
         "sprite": "hollowing_elder", "movement": "static",
         "dialogue_ref": "script.drownlight_keeper",
         "hidden_when_flag": "flag:drownlight_keeper_beaten"},
        {"id": "shutterkeeper_after", "at": {"tx": 8, "ty": 8}, "facing": "up",
         "sprite": "hollowing_elder", "movement": "static",
         "dialogue_ref": "script.drownlight_keeper_after",
         "requires_flag": "flag:drownlight_keeper_beaten"},
    ]
    fl.solid.add((8, 8))
    fl.must_reach.append(("the Shutterkeeper", (8, 8)))
    # she greets you once from the stairhead (a band on both walkable tiles off the pad)
    for (x, y) in ((2, 3), (4, 3), (3, 4)):
        fl.triggers.append({"id": f"keeper_hail_{x}_{y}", "kind": "cutscene",
                            "at": {"tx": x, "ty": y}, "activation": "step_on",
                            "ref": "script.drownlight_keeper_hail",
                            "hidden_when_flag": "flag:drownlight_keeper_hailed"})
    # her corner: the chair, the little table, the wicks she still trims
    fl.piece("armchair", (11, 8), oid="keeper_chair")
    fl.piece("table", (12, 8), oid="keeper_table")
    fl.read("keeper_table_read", (12, 8), "sign.drownlight_keeper_table")
    fl.read("keeper_table_read_b", (13, 8), "sign.drownlight_keeper_table")
    fl.obj("names_slate", "drownlight_slate", (10, 1), 2, 1, solid=False)
    fl.obj("keeper_cot", "drownlight_cot", (13, 5), 1, 2)
    fl.read("keeper_cot_read", (13, 5), "sign.drownlight_keeper_cot")
    for x in (10, 11):
        fl.read(f"slate_{x}", (x, 1), "script.drownlight_slate_lost", kind="cutscene")
    fl.piece("oil_jars", (2, 9), oid="wick_basket")
    fl.read("wick_basket_read", (2, 9), "sign.drownlight_wick_basket")
    fl.obj("shutter_plate", "drownlight_shutter_plate", (13, 2), 1, 1, solid=False)
    fl.piece("plant", (2, 5), oid="sea_pink")
    fl.read("sea_pink_read", (2, 5), "sign.drownlight_sea_pink")
    return fl.done()


def all_maps():
    return [floor_1(), floor_2(), lantern()]


if __name__ == "__main__":
    ok = True
    for m in all_maps():
        ok = finish(m) and ok
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
