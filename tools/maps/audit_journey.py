#!/usr/bin/env python3
"""
Journey audit — replays the WHOLE game at TILE level, cold open to dawn, and
proves every route the journey needs is walkable for a player holding only what
they have earned so far.

The other audits leave two gaps this one closes:
  * audit_region's PROGRESSION credits a grant once its MAP is reachable — not
    the NPC/trigger/cache that actually hands it over. A prop sealing a warden's
    dais inside an otherwise-reachable hall passes it.
  * audit_flow's REACH holds ALL six Gifts. A story band or cache reachable only
    with a Gift the journey grants LATER passes it ("the path is blocked until you
    happen to have Emberward").

How it works (engine-faithful; worldmodel.MapModel is the collision model):

  STATE    the set of reached tiles (map, tx, ty) + held Lantern Gifts + flags.
  START    graph.ts start_map/start_at (the cold open's arrival), nothing held.
  WALK     4-way steps, one-way ledge hops, Gift-gated tiles only with the Gift,
           object footprints solid (doors freed), STATIC NPC bodies solid while
           present (requires_flag/hidden_when_flag), and pushback bands (a live
           step_on trigger whose script moves the player and doesn't retire
           itself — the Tinderwick gate warden) solid.
  WARPS    step_on (fires on walking ONTO the tile; landing on one doesn't fire),
           interact (from a 4-neighbour), doors (walk-onto, freed tile); each
           honours requires_ability/requires_flag; unregistered targets no-op.
           Landings spiral to the nearest passable tile like findSafeTile.
           Waystone TRAVEL (hub_unlocked + the chart flag) also lands you.
  GRANTS   CONTENT granularity, read from the real content (node dumps the TS
           registries via journey_content.mjs): an NPC fires when a 4-neighbour
           is reached (a sight-trainer also when its sight line is), a step_on
           trigger when its tile is, an interact trigger from a 4-neighbour — and
           only while present + live under the held flags. Its script is
           evaluated op-by-op with if_flag/unless_flag guards: setFlag, battle ->
           the trainer's reward_flags + reward_abilities, legendaryBattle ->
           caughtFlag, pay -> flag, askName matches, run, every choice branch.
           Engine-set flags too: trigger sets_flags, sight trainers'
           defeated_flag, chart:* on first footfall, the entry tutorials, the
           crown-interlude seen flags, flag:caught_first_kin (a party + a reached
           encounter tile), and FlagStore.derive (crown_*, hub_unlocked,
           lamplight_*, q_post_letters_all). Iterates to a fixed point; each
           round of new keys is a WAVE.
  ORDER    each golden-thread beat must be reachable holding ONLY the Gifts the
           walkthrough grants before it: the replay is re-run with the Gift set
           capped at each canon prefix; a beat that only appears with a LATER
           Gift is a FAIL (the "prop blocks the path until you have a Gift" case).
  CONTENT  every non-ambient NPC / trigger / sign / item_cache on every map must
           be reached while live at some point in the full replay (FAIL), except
           ALLOW_UNREACHED (each entry says WHY). Content whose requires_flag is
           never granted is reported DORMANT (WARN). A final fresh walk with the
           end-state keys flags content that was reachable during the journey
           but is sealed off at the end (an NPC that appears later in a lane).
  MAPS     every registered graph node is reached, except ALLOW_UNREACHED_MAPS.

Run:  python3 tools/maps/audit_journey.py            # full report, exit 1 on FAIL
      python3 tools/maps/audit_journey.py --waves    # + every wave's grants in full
      python3 tools/maps/audit_journey.py --grants   # + the content that grants each key
      python3 tools/maps/audit_journey.py --all      # every FAIL (default caps at 25)
Needs node + the repo's esbuild (npm ci) for the content dump; otherwise stdlib.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from fnmatch import fnmatch
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from worldmodel import ALL_ABILITIES, DIRS, MapModel, load_world, parse_graph  # noqa: E402

REPO = Path(__file__).resolve().parents[2]

# ---- canon (walkthrough README §2 golden thread + §5 Gift cadence) -----------
CANON_GIFTS = ["tidecall", "glimmerstep", "updraft_kite", "emberward",
               "sunsketch", "starreach"]

# Golden-thread key -> how many canon Gifts the player may hold when it is
# earned (the prefix of CANON_GIFTS), and the CONTENT that must grant it
# (map id + npc/trigger id; '*' = any content on that map, 'engine' = derived).
# A key earned only with a LATER Gift than its prefix allows is a FAIL.
GOLDEN: list[tuple[str, int, str]] = [
    # (key, gift prefix, granting content "map:kind:id" — fnmatch glob)
    ("flag:fenn_errand", 0, "vesper_crossroads:npc:fenn_pre"),
    ("flag:has_satchel", 0, "duskapple_orchard:npc:fenn_satchel"),
    ("flag:has_vesperlamp", 0, "vesper_crossroads:npc:fenn_ready"),
    ("flag:has_starter", 0, "vesper_crossroads:npc:fenn_ready"),
    ("flag:caught_first_kin", 0, "*:engine:wild-catch"),
    ("flag:has_beacon_wick", 0, "dimglass_coast:npc:witness"),  # the lamplighter
    ("gleam:ember", 0, "tinderwick_beacon_top:trigger:beacon_battle"),
    ("flag:dusk_begins", 0, "dimglass_coast:trigger:dusk_begins_*"),
    ("flag:q_south_bell", 0, "pearlmoor_lumenary:npc:reyl_quest"),
    ("flag:q_south_jest_done", 0, "pearlmoor_oldlight_top:trigger:*"),
    ("flag:q_south_has_rope", 0, "pearlmoor_quay:npc:netmender_floats"),
    ("flag:q_south_bell_rung", 0, "pearlmoor_breakwater:trigger:ring_moorbell_*"),
    ("gleam:tide", 0, "pearlmoor_lumenary:trigger:lumenary_battle*"),
    ("tidecall", 0, "pearlmoor_lumenary:trigger:lumenary_battle*"),
    ("flag:crown_south", 0, "engine:derive"),
    ("gleam:verdant", 1, "lowleaf_lumenary:trigger:lumenary_battle*"),
    ("glimmerstep", 1, "lowleaf_lumenary:trigger:lumenary_battle*"),
    ("flag:met_hollowing", 2, "glowmoss_deep:trigger:glowmoss_relight*"),
    ("gleam:stone", 2, "cinderhead_lumenary:trigger:lumenary_battle*"),
    ("flag:crown_east", 2, "engine:derive"),
    ("flag:shortcut_mine", 2, "cinderhead_deep:trigger:open_shortcut_*"),
    ("flag:q_north_kite_blessed", 2, "galehigh_terraces:npc:winch_keeper_fly"),
    ("gleam:storm", 2, "galehigh_skyloft:trigger:mira_battle_*"),
    ("updraft_kite", 2, "galehigh_skyloft:trigger:mira_battle_*"),
    ("flag:shortcut_windward", 3, "windward_stair_ii:trigger:windward_crags_*"),
    ("flag:met_cor", 3, "pale_vault_glacier:trigger:cor_appears_*"),
    ("flag:q_north_lampline", 3, "pale_vault_glacier:npc:ysolde_quest"),
    ("flag:q_north_lamps_held", 3, "pale_vault_undercroft:trigger:light_lamp_*"),
    ("gleam:frost", 3, "pale_vault_undercroft:trigger:lumenary_battle_*"),
    ("emberward", 3, "pale_vault_undercroft:trigger:lumenary_battle_*"),
    ("flag:crown_north", 3, "engine:derive"),
    ("gleam:solar", 4, "sunken_solarium:npc:lucan_ready"),
    ("sunsketch", 4, "sunken_solarium:npc:lucan_ready"),
    ("flag:great_null_known", 5, "nightreach_observatory:trigger:light_lamp_*"),
    ("gleam:lunar", 5, "nightreach_lumenary:trigger:lumenary_battle_*"),
    ("starreach", 5, "nightreach_lumenary:trigger:lumenary_battle_*"),
    ("flag:crown_west", 5, "engine:derive"),
    ("flag:hub_unlocked", 6, "engine:derive"),
    ("flag:keystar_relit", 6, "umbral_spire_summit:trigger:keystar_relight_*"),
    ("flag:dawn", 6, "umbral_spire_summit:trigger:dawn_breaks_*"),
]

# ---- deliberate blocks (allow-lists) -------------------------------------------
# The replay runs to the post-game, so most deliberate blocks need NO entry: a
# Gift-gated tease (the Starreach void crossings, the Crystoll gap, Gullcry's
# surf, the `emberward` coldfog dead-end at coldfog_marches_i -> ii) simply opens
# once the replay holds that Gift, and the ORDER check only holds golden-thread
# beats to the canon Gift prefix. A warp to an UNREGISTERED map (cinderhead_deep
# -> crystoll_vault today) is an engine no-op and is reported as an inert tease.
# An entry here is only for something that must stay unreachable even at the
# end. Keys: maps by id; content as "map:npc:id" / "map:trigger:id" /
# "map:warp:id". Every entry says WHY — a deliberate block, never an accident.
ALLOW_UNREACHED_MAPS: dict[str, str] = {
}
ALLOW_UNREACHED: dict[str, str] = {
}

# Engine-derived flags (FlagStore.derive) — never set by content.
DERIVED_CROWNS = [
    ("flag:crown_south", "gleam:ember", "gleam:tide"),
    ("flag:crown_east", "gleam:verdant", "gleam:stone"),
    ("flag:crown_north", "gleam:storm", "gleam:frost"),
    ("flag:crown_west", "gleam:solar", "gleam:lunar"),
]
LAMPLIGHT = [("flag:lamplight_warmlight", 2), ("flag:lamplight_brightlight", 4),
             ("flag:lamplight_starlight", 6), ("flag:lamplight_radiant", 8)]
POST_LETTERS = ["wren", "fenn", "tinderwick", "pearlmoor", "lowleaf", "cinderhead",
                "galehigh", "pale_vault", "solarium", "nightreach"]
# WorldScene.ENTRY_TUTORIALS (mirrored — the engine hook, not map JSON)
ENTRY_TUTORIALS = [
    {"map": "tinderwick", "script": "script.tutorial_offer",
     "seen": "flag:tutorial_offered", "unless": "flag:has_starter"},
    {"map": "lanternway_tinderwick", "script": "script.catch_tutorial",
     "seen": "flag:catch_tutorial_seen", "requires": "flag:has_starter"},
]
try:  # seed: the map-level grant table audit_region replays
    from audit_region import GRANTS as REGION_GRANTS  # noqa: E402
except Exception:  # pragma: no cover - keep the journey audit standalone
    REGION_GRANTS = {}
PARTY = "@party"   # pseudo-flag: the player holds at least one kin


def load_content() -> dict:
    try:
        out = subprocess.run(["node", str(REPO / "tools/maps/journey_content.mjs"),
                              "--root", str(REPO)],
                             check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as e:
        err = getattr(e, "stderr", "") or str(e)
        sys.exit(f"audit_journey: could not dump content via node "
                 f"(run `npm ci` first?)\n{err}")
    return json.loads(out.stdout)


# ---- script evaluation -----------------------------------------------------
class Scripts:
    def __init__(self, content: dict):
        self.scripts = content["scripts"]
        self.trainers = content["trainers"]
        self._moves_player: dict[str, bool] = {}

    def effects(self, ref: str | None, flags: set[str]) -> tuple[set[str], set[str]]:
        """(new flags, new abilities) a script grants when run with `flags` held.
        Choice branches are ALL taken (the player can pick each on a revisit);
        battles/legendaries/pays are assumed won/caught/affordable."""
        got_f: set[str] = set()
        got_a: set[str] = set()
        if not ref or ref not in self.scripts:
            return got_f, got_a
        held = set(flags)
        self._run(self.scripts[ref], held, got_f, got_a, depth=0)
        return got_f, got_a

    def _run(self, steps, held, got_f, got_a, depth):
        if depth > 12:
            return True
        for s in steps:
            if s.get("if_flag") and s["if_flag"] not in held:
                continue
            if s.get("unless_flag") and s["unless_flag"] in held:
                continue
            op = s["op"]

            def add(f):
                if f not in held:
                    held.add(f)
                    got_f.add(f)
            if op == "setFlag" and s.get("value", True) is not False:
                add(s["flag"])
            elif op == "pay":
                add(s["flag"])
            elif op == "askName":
                for mt in s.get("matches", []):
                    add(mt["flag"])
            elif op == "legendaryBattle":
                add(s["caughtFlag"])
            elif op in ("giveStarter", "giveKin"):
                add(PARTY)
            elif op == "giveItem" or op == "ensureItem":
                add(f"item:{s['item']}")
            elif op == "battle":
                t = self.trainers.get(s["trainer"], {})
                for f in t.get("reward_flags", []):
                    add(f)
                for a in t.get("reward_abilities", []):
                    if a not in held:
                        held.add(a)
                        got_a.add(a)
            elif op == "run":
                sub = self.scripts.get(s["ref"])
                if sub is not None and not self._run(sub, held, got_f, got_a, depth + 1):
                    return False
            elif op == "choice":
                branch_sets = []
                for o in s.get("options", []):
                    if o.get("if_flag") and o["if_flag"] not in held:
                        continue
                    if o.get("unless_flag") and o["unless_flag"] in held:
                        continue
                    h2 = set(held)
                    self._run(o.get("ops", []), h2, got_f, got_a, depth + 1)
                    branch_sets.append(h2)
                for h2 in branch_sets:
                    held |= h2
            elif op == "cinematic":
                return False   # nothing after a cinematic op plays
        return True

    def moves_player(self, ref: str | None, depth=0) -> bool:
        if not ref or ref not in self.scripts or depth > 12:
            return False
        if ref in self._moves_player:
            return self._moves_player[ref]
        hit = False
        stack = list(self.scripts[ref])
        while stack and not hit:
            s = stack.pop()
            if s["op"] == "move" and s.get("actor") == "player":
                hit = True
            elif s["op"] == "run":
                hit = self.moves_player(s["ref"], depth + 1)
            elif s["op"] == "choice":
                for o in s.get("options", []):
                    stack.extend(o.get("ops", []))
        self._moves_player[ref] = hit
        return hit


# ---- per-map static data ----------------------------------------------------
class MapData:
    def __init__(self, m: dict):
        self.mm = MapModel(m)
        mm = self.mm
        self.id = mm.id
        self.step_warps: dict[tuple[int, int], dict] = {}
        self.adj_warps: dict[tuple[int, int], list[dict]] = defaultdict(list)
        for w in mm.warps:
            at = (w["at"]["tx"], w["at"]["ty"])
            if w.get("trigger", "step_on") == "step_on":
                self.step_warps.setdefault(at, w)
            if w.get("trigger") == "interact" or w.get("transition") == "door":
                for dx, dy in DIRS.values():
                    self.adj_warps[(at[0] + dx, at[1] + dy)].append(w)
        self.ability_tiles: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for i, ab in enumerate(mm.ability):
            if ab:
                self.ability_tiles[ab].append((i % mm.w, i // mm.w))
        self.sight = mm.sight_tiles()
        self.npcs = mm.npcs
        self.triggers = mm.triggers
        self.zones = m.get("encounters", [])


def npc_present(n: dict, flags: set[str]) -> bool:
    if n.get("requires_flag") and n["requires_flag"] not in flags:
        return False
    if n.get("hidden_when_flag") and n["hidden_when_flag"] in flags:
        return False
    return True


def trigger_present(t: dict, flags: set[str]) -> bool:
    return not (t.get("hidden_when_flag") and t["hidden_when_flag"] in flags)


def trigger_live(t: dict, flags: set[str]) -> bool:
    if not trigger_present(t, flags):
        return False
    if t.get("requires_flag") and t["requires_flag"] not in flags:
        return False
    return True


def ckey(mid: str, kind: str, cid: str) -> str:
    return f"{mid}:{kind}:{cid}"


# ---- the replay ---------------------------------------------------------------
class Replay:
    def __init__(self, world, graph, content, scripts: Scripts, maps: dict[str, MapData],
                 gift_cap: set[str] | None = None):
        self.world, self.graph, self.content = world, graph, content
        self.S = scripts
        self.maps = maps
        self.registered = set(content["registered"])
        self.gift_cap = gift_cap
        self.flags: set[str] = set()
        self.abilities: set[str] = set()       # usable for movement
        self.granted_abilities: set[str] = set()
        self.walked: dict[str, set] = defaultdict(set)
        self.landed: dict[str, set] = defaultdict(set)
        self.first_wave_map: dict[str, int] = {}
        self.q: deque = deque()
        self.wave = 0
        self.grant_log: dict[str, dict] = {}   # key -> {wave, by, gifts, flags}
        self.content_reached: dict[str, int] = {}   # ckey -> wave reached while live
        self.blockers: dict[str, set] = {}
        self.ever_barrier: dict[str, set] = defaultdict(set)
        self.used_warps: set[tuple[str, str]] = set()
        self.chart_of_map: dict[str, list[str]] = defaultdict(list)
        for c in content["charts"]:
            for mid in c["maps"]:
                self.chart_of_map[mid].append(f"chart:{c['id']}")

    # -- dynamic per-map geometry -------------------------------------------
    def compute_blockers(self, mid: str) -> set[tuple[int, int]]:
        md = self.maps[mid]
        out = set()
        for n in md.npcs:
            if n.get("movement", "static") == "static" and npc_present(n, self.flags):
                out.add((n["at"]["tx"], n["at"]["ty"]))
        for t in md.triggers:
            if t.get("activation") != "step_on" or not trigger_live(t, self.flags):
                continue
            if t.get("kind") not in ("script", "cutscene"):
                continue
            if not self.S.moves_player(t.get("ref")):
                continue
            f, _ = self.S.effects(t.get("ref"), self.flags)
            after = self.flags | f | set(t.get("sets_flags", []))
            if t.get("once"):
                continue
            if trigger_live(t, after):   # doesn't retire itself -> a pushback band
                out.add((t["at"]["tx"], t["at"]["ty"]))
                self.ever_barrier[mid].add((t["at"]["tx"], t["at"]["ty"]))
        return out

    def warp_ok(self, w: dict) -> bool:
        if w.get("requires_ability") and w["requires_ability"] not in self.abilities:
            return False
        if w.get("requires_flag") and w["requires_flag"] not in self.flags:
            return False
        return w["to_map"] in self.maps and w["to_map"] in self.registered

    # -- reachability ---------------------------------------------------------
    def landing(self, mid: str, tx: int, ty: int) -> tuple[int, int] | None:
        mm = self.maps[mid].mm
        cx = min(max(tx, 0), mm.w - 1)
        cy = min(max(ty, 0), mm.h - 1)
        if mm.standable(cx, cy, abilities=self.abilities):
            return cx, cy
        for r in range(1, max(mm.w, mm.h)):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if mm.standable(cx + dx, cy + dy, abilities=self.abilities):
                        return cx + dx, cy + dy
        return None

    def visit(self, mid: str, x: int, y: int, landed: bool):
        bucket = self.landed if landed else self.walked
        if (x, y) in bucket[mid]:
            return
        bucket[mid].add((x, y))
        if mid not in self.first_wave_map:
            self.first_wave_map[mid] = self.wave
        self.q.append((mid, x, y, landed))

    def warp_to(self, w: dict):
        tgt = w["to_map"]
        land = self.landing(tgt, w["to"]["tx"], w["to"]["ty"])
        if land:
            self.visit(tgt, land[0], land[1], True)

    def expand(self, mid, x, y, landed):
        md = self.maps[mid]
        w = md.step_warps.get((x, y))
        if w is not None and not landed and self.warp_ok(w):
            self.used_warps.add((mid, w["id"]))
            self.warp_to(w)
            return
        blk = self.blockers.get(mid)
        if blk is None:
            blk = self.blockers[mid] = self.compute_blockers(mid)
        for nx, ny in md.mm.moves_from(x, y, abilities=self.abilities, npc_block=blk):
            self.visit(mid, nx, ny, False)
        for aw in md.adj_warps.get((x, y), ()):
            if self.warp_ok(aw):
                self.used_warps.add((mid, aw["id"]))
                self.warp_to(aw)

    def drain(self):
        while self.q:
            self.expand(*self.q.popleft())

    def reached(self, mid: str, t: tuple[int, int]) -> bool:
        return t in self.walked[mid] or t in self.landed[mid]

    def requeue_near(self, mid: str, tiles):
        """Re-expand reached nodes within 2 steps of tiles whose rules changed."""
        w, l = self.walked[mid], self.landed[mid]
        if not w and not l:
            return
        for (tx, ty) in tiles:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if abs(dx) + abs(dy) > 2:
                        continue
                    p = (tx + dx, ty + dy)
                    if p in w:
                        self.q.append((mid, p[0], p[1], False))
                    if p in l:
                        self.q.append((mid, p[0], p[1], True))

    # -- content ---------------------------------------------------------------
    def npc_reach(self, md: MapData, n: dict) -> bool:
        x, y = n["at"]["tx"], n["at"]["ty"]
        if any(self.reached(md.id, (x + dx, y + dy)) for dx, dy in DIRS.values()):
            return True
        return any(self.reached(md.id, t) for t in md.sight.get(n["id"], ()))

    def trigger_reach(self, md: MapData, t: dict) -> bool:
        at = (t["at"]["tx"], t["at"]["ty"])
        if t.get("activation") == "step_on" and at not in self.ever_barrier[md.id]:
            return self.reached(md.id, at)
        # interact — or a pushback band, which fires as you try to step onto it
        return any(self.reached(md.id, (at[0] + dx, at[1] + dy)) for dx, dy in DIRS.values())

    def harvest(self) -> list[tuple[str, str]]:
        """All (key, granted_by) the reached, live content would grant now."""
        out: list[tuple[str, str]] = []
        F = self.flags
        for mid, md in self.maps.items():
            if mid not in self.first_wave_map:
                continue
            for n in md.npcs:
                if not npc_present(n, F) or not self.npc_reach(md, n):
                    continue
                k = ckey(mid, "npc", n["id"])
                self.content_reached.setdefault(k, self.wave)
                ref = n.get("dialogue_ref") or ""
                # an NPC only RUNS its ref as a cutscene when it's a script.* key
                fl, ab = self.S.effects(ref if ref.startswith("script.") else None, F)
                if n.get("defeated_flag") and n.get("sight_range"):
                    fl.add(n["defeated_flag"])
                out += [(f, k) for f in fl] + [(a, k) for a in ab]
            for t in md.triggers:
                if not trigger_present(t, F) or not self.trigger_reach(md, t):
                    continue
                k = ckey(mid, "trigger", t["id"])
                if not trigger_live(t, F):
                    continue
                self.content_reached.setdefault(k, self.wave)
                fl, ab = (self.S.effects(t.get("ref"), F)
                          if t.get("kind") in ("script", "cutscene") else (set(), set()))
                fl |= set(t.get("sets_flags", []))
                if t.get("once"):
                    fl.add(f"trigger:{t['id']}")
                out += [(f, k) for f in fl] + [(a, k) for a in ab]
            # engine hooks on first footfall
            for cf in self.chart_of_map.get(mid, []):
                out.append((cf, f"{mid}:engine:chart"))
            for tut in ENTRY_TUTORIALS:
                if tut["map"] != mid:
                    continue
                if tut.get("requires") and tut["requires"] not in F:
                    continue
                if tut.get("unless") and tut["unless"] in F:
                    continue
                fl, ab = self.S.effects(tut["script"], F)
                fl.add(tut["seen"])
                out += [(f, f"{mid}:engine:tutorial") for f in fl]
                out += [(a, f"{mid}:engine:tutorial") for a in ab]
            # a wild catch: party + a reached, rolling encounter tile
            if PARTY in F and "flag:caught_first_kin" not in F and self.encounter_reached(md):
                out.append(("flag:caught_first_kin", f"{mid}:engine:wild-catch"))
        for it in self.content["interludes"]:
            if all(r in F for r in it["requires"]):
                out.append((it["seen_flag"], "engine:interlude"))
        # FlagStore.derive
        held = F | {k for k, _ in out}
        for crown, a, b in DERIVED_CROWNS:
            if a in held and b in held:
                out.append((crown, "engine:derive"))
                held.add(crown)
        if all(c in held for c, _, _ in DERIVED_CROWNS):
            out.append(("flag:hub_unlocked", "engine:derive"))
        if all(f"flag:q_post_letter_{x}" in held for x in POST_LETTERS):
            out.append(("flag:q_post_letters_all", "engine:derive"))
        g = sum(1 for f in held if f.startswith("gleam:"))
        for f, need in LAMPLIGHT:
            if g >= need:
                out.append((f, "engine:derive"))
        return [(k, by) for k, by in out if k not in F and k not in self.granted_abilities]

    def encounter_reached(self, md: MapData) -> bool:
        mm = md.mm
        for z in md.zones:
            if z.get("requires_flag") and z["requires_flag"] not in self.flags:
                continue
            if z.get("hidden_when_flag") and z["hidden_when_flag"] in self.flags:
                continue
            if z.get("requires_ability") and z["requires_ability"] not in self.abilities:
                continue
            r = z["rect"]
            tile_bound = z.get("terrain") in ("tall_grass", "water")
            for ty in range(r["ty"], r["ty"] + r["h"]):
                for tx in range(r["tx"], r["tx"] + r["w"]):
                    if not self.reached(md.id, (tx, ty)):
                        continue
                    if tile_bound and not (mm.in_bounds(tx, ty) and mm.encounter[ty * mm.w + tx]):
                        continue
                    return True
        return False

    # -- the fixed point ---------------------------------------------------------
    def run(self, max_waves: int = 400):
        st = self.graph["start_at"]
        self.visit(self.graph["start_map"], st["tx"], st["ty"], True)
        self.waves: list[dict] = []
        while True:
            self.drain()
            new = self.harvest()
            if not new:
                break
            maps_before = set(self.first_wave_map)
            self.wave += 1
            if self.wave > max_waves:
                break
            new_flags, new_abs = set(), set()
            for k, by in new:
                (new_abs if k in ALL_ABILITIES else new_flags).add(k)
                g = self.grant_log.setdefault(k, {"wave": self.wave, "by": by, "by_all": [],
                                                  "gifts": sorted(self.abilities),
                                                  "held": len(self.flags)})
                if by not in g["by_all"]:
                    g["by_all"].append(by)
            self.granted_abilities |= new_abs
            usable = {a for a in new_abs if self.gift_cap is None or a in self.gift_cap}
            old_flags = set(self.flags)
            self.flags |= new_flags
            self.flags |= {a for a in new_abs}   # gifts double as held keys
            self.abilities |= usable
            # rules changed -> re-open the frontier near every affected tile
            for mid, md in self.maps.items():
                if mid not in self.first_wave_map:
                    continue
                dirty = []
                for a in usable:
                    dirty += md.ability_tiles.get(a, [])
                old_blk = self.blockers.get(mid)
                newb = self.compute_blockers(mid)
                self.blockers[mid] = newb
                if old_blk is not None:
                    dirty += list(old_blk - newb)
                for at, w in md.step_warps.items():
                    if self._gate_newly_open(w, old_flags, usable):
                        dirty.append(at)
                for at, ws in md.adj_warps.items():
                    if any(self._gate_newly_open(w, old_flags, usable) for w in ws):
                        dirty.append(at)
                if dirty:
                    self.requeue_near(mid, dirty)
            # waystone travel (pause menu TRAVEL, once the hub is open)
            if "flag:hub_unlocked" in self.flags:
                for ws in self.content["waystones"]:
                    if ws["visited_flag"] in self.flags and ws["map"] in self.maps:
                        land = self.landing(ws["map"], ws["tx"], ws["ty"])
                        if land:
                            self.visit(ws["map"], land[0], land[1], True)
            self.drain()
            self.waves.append({
                "wave": self.wave,
                "granted": sorted(new_flags | new_abs),
                "maps": sorted(set(self.first_wave_map) - maps_before),
            })
        return self

    def _gate_newly_open(self, w, old_flags, new_abs) -> bool:
        ra, rf = w.get("requires_ability"), w.get("requires_flag")
        if not ra and not rf:
            return False
        was = (not ra or (ra in self.abilities and ra not in new_abs)) and \
              (not rf or rf in old_flags)
        return self.warp_ok(w) and not was


# ---- reporting -------------------------------------------------------------------
def all_content(maps: dict[str, MapData]):
    for mid, md in maps.items():
        for n in md.npcs:
            yield ckey(mid, "npc", n["id"]), n, "npc"
        for t in md.triggers:
            yield ckey(mid, "trigger", t["id"]), t, "trigger"


def main() -> int:
    t0 = time.time()
    verbose_waves = "--waves" in sys.argv
    show_grants = "--grants" in sys.argv
    world = load_world()
    graph = parse_graph()
    content = load_content()
    scripts = Scripts(content)
    maps = {mid: MapData(m) for mid, m in world.items()}

    full = Replay(world, graph, content, scripts, maps).run()
    fails: list[str] = []
    warns: list[str] = []
    infos: list[str] = []

    # ---- wave table -----------------------------------------------------------
    print(f"Journey audit — {len(maps)} maps, start "
          f"{graph['start_map']}@({graph['start_at']['tx']},{graph['start_at']['ty']})\n")
    print(f"  {'wave':>4}  {'gifts':<7} newly granted (key flags)  ->  newly reached maps")
    interesting = lambda k: (k.startswith("gleam:") or k in ALL_ABILITIES or  # noqa: E731
                             k in {g for g, _, _ in GOLDEN})
    for w in full.waves:
        keys = [k for k in w["granted"] if interesting(k)]
        if not keys and not w["maps"] and not verbose_waves:
            continue
        shown = w["granted"] if verbose_waves else keys
        gifts = sum(1 for a in CANON_GIFTS if full.grant_log.get(a, {}).get("wave", 1e9) <= w["wave"])
        print(f"  {w['wave']:>4}  {gifts}/6     {', '.join(shown) or '·'}"
              + (f"  ->  {', '.join(w['maps'])}" if w["maps"] else ""))
    print(f"\n  fixed point after {full.wave} waves; {len(full.flags)} flags, "
          f"{len(full.granted_abilities)}/6 Gifts, {len(full.first_wave_map)} maps reached")

    # ---- golden thread: granted, by the right content, in canon Gift order -----
    missing = [k for k, _, _ in GOLDEN if k not in full.grant_log]
    for k in missing:
        fails.append(f"golden thread: '{k}' is never granted")
    for a in CANON_GIFTS:
        if a not in full.grant_log:
            fails.append(f"Lantern Gift '{a}' is never granted")
    for k, _, expect in GOLDEN:
        if k not in full.grant_log:
            continue
        by_all = full.grant_log[k]["by_all"]
        if not any(fnmatch(b, expect) for b in by_all):
            warns.append(f"'{k}' first granted by {', '.join(by_all)}, expected {expect} "
                         f"(grant moved? update GOLDEN)")
        if ":engine:" in expect or expect.startswith("engine:"):
            continue
        # the CANON grantor itself must be reached while live — a second grantor
        # elsewhere must not mask a sealed warden/dais/band
        if not any(fnmatch(c, expect) for c in full.content_reached):
            fails.append(f"golden thread: '{k}' — its canon grantor {expect} is never "
                         f"reached while live")
    # the region audit's map-level GRANTS table, now checked at content level:
    # every key it names must be granted by content ON that map
    for gmap, keys in REGION_GRANTS.items():
        for k in keys:
            g = full.grant_log.get(k)
            if g is None:
                fails.append(f"'{k}' (audit_region.GRANTS @ {gmap}) is never granted")
            elif not any(b.split(":")[0] in (gmap, "engine") for b in g["by_all"]):
                infos.append(f"'{k}': audit_region.GRANTS credits {gmap}, but the content "
                             f"that grants it is {', '.join(g['by_all'])}")
    # canon order: re-run capped at each Gift prefix
    order_ok = 0
    for level in range(len(CANON_GIFTS)):
        need = [(k, lv) for k, lv, _ in GOLDEN if lv == level and k in full.grant_log]
        if not need:
            continue
        cap = set(CANON_GIFTS[:level])
        capped = Replay(world, graph, content, scripts, maps, gift_cap=cap).run()
        expect_of = {k: e for k, _, e in GOLDEN}
        for k, lv in need:
            if k in capped.grant_log:
                order_ok += 1
                continue
            g = full.grant_log[k]
            later = [a for a in g["gifts"] if a not in cap]
            where = ""
            for ck, item, kind in all_content(maps):
                if not fnmatch(ck, expect_of[k]):
                    continue
                mid = ck.split(":")[0]
                where = (f"; with only the canon Gifts its grantor {ck} is out of reach: "
                         + (describe_unreached(capped, maps[mid], item, kind)
                            if mid in capped.first_wave_map else f"map '{mid}' never reached"))
                break
            fails.append(f"ORDER: '{k}' (canon: holding only "
                         f"{'+'.join(CANON_GIFTS[:lv]) or 'no Gifts'}) is unreachable without "
                         f"{'+'.join(later) or 'a later Gift'} — the full replay grants it "
                         f"via {g['by']} at wave {g['wave']}{where}")
    order_ok += sum(1 for k, lv, _ in GOLDEN if lv == len(CANON_GIFTS) and k in full.grant_log)

    # ---- maps ------------------------------------------------------------------
    registered = set(content["registered"])
    node_ids = [n["map_id"] for n in graph["nodes"]]
    for mid in node_ids:
        if mid not in maps or mid not in registered:
            continue
        if mid not in full.first_wave_map and mid not in ALLOW_UNREACHED_MAPS:
            fails.append(f"map '{mid}' is never reached by the journey")
    stale_maps = [m for m in ALLOW_UNREACHED_MAPS if m in full.first_wave_map]
    for m in stale_maps:
        warns.append(f"ALLOW_UNREACHED_MAPS['{m}'] is reached now — drop the entry")

    # ---- content ------------------------------------------------------------------
    fresh = Replay(world, graph, content, scripts, maps)
    fresh.flags = set(full.flags)
    fresh.abilities = set(full.granted_abilities)
    st = graph["start_at"]
    fresh.visit(graph["start_map"], st["tx"], st["ty"], True)
    for ws in content["waystones"]:
        if ws["visited_flag"] in fresh.flags and ws["map"] in maps:
            land = fresh.landing(ws["map"], ws["tx"], ws["ty"])
            if land:
                fresh.visit(ws["map"], land[0], land[1], True)
    fresh.drain()

    n_content = n_reached = 0
    dormant, superseded, dead_tiles, sealed_late = [], [], [], []

    def geo(r: Replay, mid: str, item: dict, kind: str) -> bool:
        md = maps[mid]
        return r.npc_reach(md, item) if kind == "npc" else r.trigger_reach(md, item)

    # band siblings: the same beat stamped on several tiles (map + ref)
    band_hit: set[tuple[str, str]] = set()
    for k, item, kind in all_content(maps):
        mid = k.split(":")[0]
        if kind == "trigger" and mid in full.first_wave_map and geo(full, mid, item, kind):
            band_hit.add((mid, item.get("ref", "")))
    for k, item, kind in all_content(maps):
        mid = k.split(":")[0]
        n_content += 1
        if k in full.content_reached:
            n_reached += 1
            present = (npc_present(item, full.flags) if kind == "npc"
                       else trigger_live(item, full.flags))
            if present and not geo(fresh, mid, item, kind) and k not in ALLOW_UNREACHED:
                sealed_late.append(k)
            continue
        if mid not in full.first_wave_map:
            continue  # the map itself fails above
        if geo(full, mid, item, kind):
            # walkable to, but never while live: the over-approximate flag replay
            # granted its hidden_when_flag no later than its requires_flag
            superseded.append(k)
            continue
        if k in ALLOW_UNREACHED:
            continue
        if item.get("requires_flag") and item["requires_flag"] not in full.flags:
            dormant.append(f"{k} (needs {item['requires_flag']})")
            continue
        if kind == "trigger" and (mid, item.get("ref", "")) in band_hit:
            dead_tiles.append(f"{k}@({item['at']['tx']},{item['at']['ty']})")
            continue
        why = describe_unreached(full, maps[mid], item, kind)
        fails.append(f"content unreached: {k} @({item['at']['tx']},{item['at']['ty']}) — {why}")
    for k, why in ALLOW_UNREACHED.items():
        if k in full.content_reached:
            warns.append(f"ALLOW_UNREACHED['{k}'] is reached now — drop the entry")
    if dormant:
        warns.append(f"{len(dormant)} dormant item(s) — requires_flag never granted by any "
                     f"reachable content: " + "; ".join(sorted(dormant)))
    if dead_tiles:
        warns.append(f"{len(dead_tiles)} dead band tile(s) — a step_on tile on solid ground "
                     f"(the band's other tiles fire the beat; drop or move these): "
                     + ", ".join(sorted(dead_tiles)))
    if superseded:
        infos.append(f"{len(superseded)} item(s) walkable but never live in the replay "
                     f"(flag order superseded them): " + ", ".join(sorted(superseded)))
    for k in sealed_late:
        warns.append(f"sealed at the end: {k} was reachable during the journey but not "
                     f"with the end-state keys (a later NPC/band in the lane?)")

    # ---- warps: every authored exit is actually USABLE by the end ---------------
    n_warps = n_used = 0
    teases, dead_twins = [], []
    for mid, md in maps.items():
        if mid not in full.first_wave_map:
            continue
        twin_used = {}
        for p in md.mm.portals():
            used = any((mid, i) in full.used_warps for i in p["ids"])
            for i in p["ids"]:
                twin_used[i] = used
        for w in md.mm.warps:
            n_warps += 1
            k = f"{mid}:warp:{w['id']}"
            if (mid, w["id"]) in full.used_warps:
                n_used += 1
                continue
            if w["to_map"] not in maps or w["to_map"] not in registered:
                teases.append(f"{k}->{w['to_map']}")
                continue
            if k in ALLOW_UNREACHED:
                continue
            rf = w.get("requires_flag")
            if rf and rf not in full.flags:
                warns.append(f"dormant warp {k} -> {w['to_map']}: requires {rf}, never granted")
                continue
            at = (w["at"]["tx"], w["at"]["ty"])
            if twin_used.get(w["id"]):
                dead_twins.append(f"{k}@{at}")   # its portal's other tile works
                continue
            cells = [at] if w.get("trigger", "step_on") == "step_on" else []
            if w.get("trigger") == "interact" or w.get("transition") == "door":
                cells += [(at[0] + dx, at[1] + dy) for dx, dy in DIRS.values()]
            why = describe_cells(full, md, cells)
            ra = w.get("requires_ability")
            if ra and ra not in full.abilities:
                why = f"warp needs {ra} (never usable); " + why
            fails.append(f"warp unusable: {k} @{at} -> {w['to_map']} — {why}")
    for k in ALLOW_UNREACHED:
        if ":warp:" in k and tuple(k.split(":warp:")) in full.used_warps:
            warns.append(f"ALLOW_UNREACHED['{k}'] is used now — drop the entry")
    if dead_twins:
        warns.append(f"{len(dead_twins)} dead warp tile(s) — never steppable, but the same "
                     f"portal's other tile works: " + ", ".join(sorted(dead_twins)))
    if teases:
        infos.append(f"{len(teases)} warp(s) to unregistered maps (engine no-ops — inert "
                     f"teases): " + ", ".join(sorted(teases)))

    # ---- grants report ----------------------------------------------------------------
    if show_grants:
        print("\n  key grants (wave, content, Gifts held):")
        for k, lv, _ in GOLDEN:
            g = full.grant_log.get(k)
            if g:
                print(f"    {k:<28} w{g['wave']:<4} {g['by']:<55} "
                      f"[{'+'.join(g['gifts']) or '-'}]")

    print(f"\n  golden thread: {len(GOLDEN) - len(missing)}/{len(GOLDEN)} granted, "
          f"{order_ok} in canon Gift order")
    print(f"  content: {n_reached}/{n_content} NPCs/triggers reached while live "
          f"({len(dormant)} dormant, {len(ALLOW_UNREACHED)} allow-listed)")
    for i in infos:
        print(f"  [·] {i}")
    for w in warns:
        print(f"  [!] {w}")
    if missing:
        # the journey broke: name the FIRST broken beat and why its grantor is out
        # of reach — everything after it is downstream noise
        first = next(g for g in GOLDEN if g[0] in missing)
        key, _, expect = first
        print(f"\n  ROOT CAUSE — the journey stops at '{key}' (canon grantor {expect}):")
        hits = [(k, item, kind) for k, item, kind in all_content(maps) if fnmatch(k, expect)]
        for k, item, kind in hits[:6]:
            mid = k.split(":")[0]
            if mid not in full.first_wave_map:
                print(f"    {k}: its map '{mid}' is never reached")
                continue
            live = (npc_present(item, full.flags) if kind == "npc"
                    else trigger_live(item, full.flags))
            gate = "" if live else f" [not live: requires {item.get('requires_flag')}]"
            print(f"    {k} @({item['at']['tx']},{item['at']['ty']}){gate} — "
                  f"{describe_unreached(full, maps[mid], item, kind)}")
        if not hits:
            print("    (no content matches the canon grantor — was it renamed? update GOLDEN)")
    # direct findings first (they name tiles/objects); cascades after
    prio = ("ORDER:", "content unreached:", "warp unusable:", "golden thread: '")
    fails.sort(key=lambda f: next((i for i, p in enumerate(prio) if f.startswith(p)), len(prio)))
    cap = None if "--all" in sys.argv else 25
    shown = fails if cap is None else fails[:cap]
    for f in shown:
        print(f"  [✗] {f}")
    if cap is not None and len(fails) > cap:
        print(f"  … {len(fails) - cap} more (downstream of the above; --all lists them)")
    dt = time.time() - t0
    print(f"\n{'FAIL' if fails else 'PASS'} — {len(fails)} failure(s), "
          f"{len(warns)} warning(s)  ({dt:.1f}s)")
    return 1 if fails else 0


def describe_unreached(r: Replay, md: MapData, item: dict, kind: str) -> str:
    """Why can't the replay reach this content? Name what blocks its approach."""
    x, y = item["at"]["tx"], item["at"]["ty"]
    cells = [(x, y)] if kind == "trigger" and item.get("activation") == "step_on" else \
        [(x + dx, y + dy) for dx, dy in DIRS.values()]
    if kind == "npc":
        cells += sorted(md.sight.get(item["id"], ()))
    return describe_cells(r, md, cells)


def describe_cells(r: Replay, md: MapData, cells) -> str:
    mm = md.mm
    reasons = []
    for c in cells:
        if not mm.in_bounds(*c):
            continue
        i = c[1] * mm.w + c[0]
        if mm.solid[i]:
            obj = next((o["id"] for o in mm.m.get("objects", [])
                        if o.get("solid") is not False
                        and o["at"]["tx"] <= c[0] < o["at"]["tx"] + o["w"]
                        and o["at"]["ty"] <= c[1] < o["at"]["ty"] + o["h"]), None)
            reasons.append(f"{c} solid ({'object ' + repr(obj) if obj else 'tile'})")
        elif mm.ledge[i]:
            reasons.append(f"{c} ledge")
        elif mm.ability[i] and mm.ability[i] not in r.abilities:
            reasons.append(f"{c} needs {mm.ability[i]}")
        elif c in r.blockers.get(md.id, set()):
            reasons.append(f"{c} held by a static NPC/pushback band")
        elif not r.reached(md.id, c):
            reasons.append(f"{c} walkable but cut off from every reached tile")
    return "; ".join(reasons) or "no approach tile"


if __name__ == "__main__":
    sys.exit(main())
