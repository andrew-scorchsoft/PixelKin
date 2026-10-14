#!/usr/bin/env python3
"""
add_world_craft — the WORLD-CRAFT surgical runner (docs/reviews/world-craft-panel.md
§6). Applies each region package's placements to the SHIPPED map JSONs: an
idempotent, id-keyed upsert in the add_peril_thread.py pattern, because shipped
JSONs carry post-build additions their builders don't (CLAUDE.md gotcha).

Placements live in one module per region — tools/maps/worldcraft/<region>.py —
so parallel packages never edit the same file. Each module's PLACEMENTS maps a
map id to a spec (keys in worldcraft/_kit.py):

    "ambience": {...}   REPLACES the map's MapDefinition.ambience block
    "npcs" / "objects" / "triggers": upserted by id
    "signs": [(id, (x, y), "sign.ref")]  trigger + the sign deco tile

Guards (a violation is an ERROR and nothing is written):
  * unknown ambience keys / particle kinds (typos would silently do nothing);
  * pre-Chickenpig maps take ONLY "ambience", ambient NPCs, "sprites" (cast swaps
    on existing NPC ids), "after"/"talk" (post-Gleam WORDS: a same-tile flag-pair
    twin, or a dialogue re-point — no body moves) and "objects" that PROVE off-lane
    (prove_off_lane: no lane/encounter/approach tile, reachability unchanged, no
    walk longer);
  * an "after" twin needs an original with no other hide flag and no requires
    flag the Gleam doesn't imply (else use "talk" + a staged script);
  * an ambient kin must stand on foot-walkable ground (no Gifts), never on a
    warp or trigger tile, inside the map.

Run (from the repo root):
    python3 tools/maps/add_world_craft.py                 # apply every region
    python3 tools/maps/add_world_craft.py --region south  # one region's module
    python3 tools/maps/add_world_craft.py --check         # report drift, write nothing (exit 1 on drift)
Then re-run the map audits (audit_flow/audit_warps/audit_region/audit_spatial,
render_walkable --report-only) — ambient kin are invisible to all of them.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from worldmodel import MapModel  # noqa: E402
from worldcraft._kit import AMBIENCE_KEYS, PARTICLE_KINDS, PRE_CHICKENPIG, gid  # noqa: E402

REPO = HERE.parents[1]
MAPS = REPO / "public" / "assets" / "maps"
REGIONS = ("south", "east", "north", "west", "central", "outer",  # outer: the Farlamp Isles' Undertide (lane C2)
           "drownlight")  # lane N2: the Drownlight tower (walkthrough/11 Part B)
SIGN_GID = gid("sign")


def upsert(lst: list, item: dict) -> bool:
    for i, cur in enumerate(lst):
        if cur.get("id") == item["id"]:
            if cur == item:
                return False
            lst[i] = item
            return True
    lst.append(item)
    return True


LANE_TERRAINS = {"path", "trail", "dawnpath", "snowtrail"}
ALL_GIFTS = {"tidecall", "glimmerstep", "emberward", "updraft_kite", "starreach", "sunsketch"}


def _terrain_meta(m: dict) -> dict[int, dict]:
    meta: dict[int, dict] = {}
    for ts in m.get("tilesets", []):
        side = MAPS.parent / "tilesets" / f"{ts['name']}.tileset.json"
        if side.is_file():
            for t in json.loads(side.read_text())["tiles"]:
                meta[ts.get("first_gid", 1) + t["index"]] = t
    return meta


def is_flag_swap(a: dict, b: dict) -> bool:
    """A visibility swap pair (CLAUDE.md: same footprint + solidity, one shown by
    `requires_flag`, the other hidden by the same flag) is meant to share tiles."""
    fa = a.get("requires_flag") or a.get("hidden_when_flag")
    flips = (a.get("requires_flag") and a.get("requires_flag") == b.get("hidden_when_flag")) or \
            (a.get("hidden_when_flag") and a.get("hidden_when_flag") == b.get("requires_flag"))
    same = (a["at"] == b["at"] and a.get("w") == b.get("w") and a.get("h") == b.get("h")
            and bool(a.get("solid", True)) == bool(b.get("solid", True)))
    return bool(fa and flips and same)


def overlaps(o: dict, others: list[dict]) -> str | None:
    """Id of the first object in `others` whose whole drawn rect meets `o`'s
    (flag-swap twins excepted — they share a footprint by design)."""
    ax, ay = o["at"]["tx"], o["at"]["ty"]
    for p in others:
        if p["id"] == o["id"] or is_flag_swap(o, p):
            continue
        bx, by = p["at"]["tx"], p["at"]["ty"]
        if ax < bx + p["w"] and bx < ax + o["w"] and ay < by + p["h"] and by < ay + o["h"]:
            return p["id"]
    return None


def prove_off_lane(mid: str, m: dict, objects: list[dict]) -> list[str]:
    """Pre-Chickenpig PROPS: prove an object set changes nothing about play.

    Every footprint tile must avoid lanes (path/trail art), encounter tiles,
    warps, triggers, NPC posts and the 4 tiles around anything you talk to;
    and with the props in, (a) the foot- and all-Gift-reachable sets lose only
    the footprint itself and (b) no warp-to-warp / warp-to-content walk gets a
    single step longer. A violation is an ERROR (nothing is written)."""
    errs: list[str] = []
    W = m["width"]
    meta = _terrain_meta(m)
    base = next((l["data"] for l in m["layers"] if l.get("role") == "base"), [])
    new_ids = {o["id"] for o in objects}
    # BEFORE is the shipped map exactly as it is — never with a replaced object
    # removed (that let a spec "prove" a shrunk or de-solidified shop harmless).
    old = m
    new = dict(m, objects=[o for o in m.get("objects", []) if o["id"] not in new_ids] + list(objects))
    before, after = MapModel(old), MapModel(new)
    busy = {(w["at"]["tx"], w["at"]["ty"]) for w in m.get("warps", [])}
    talk = {(t["at"]["tx"], t["at"]["ty"]) for t in m.get("triggers", [])}
    talk |= {(n["at"]["tx"], n["at"]["ty"]) for n in m.get("npcs", []) if not n.get("ambient")}
    near = {(x + dx, y + dy) for (x, y) in talk | busy for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))}
    foot: set[tuple[int, int]] = set()
    for o in objects:
        if o.get("solid") is False:
            # Not collision — but a drawn prop over a warp/trigger hides it.
            for ty in range(o["at"]["ty"], o["at"]["ty"] + o["h"]):
                for tx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
                    if (tx, ty) in busy or (tx, ty) in talk:
                        errs.append(f"{mid}: non-solid prop '{o['id']}' draws over a warp/trigger/NPC at {(tx, ty)}")
            continue
        top = o["at"]["ty"] + (o.get("overhang", 0) if o.get("walk_under") else 0)
        for ty in range(top, o["at"]["ty"] + o["h"]):
            for tx in range(o["at"]["tx"], o["at"]["tx"] + o["w"]):
                foot.add((tx, ty))
    for o in objects:
        clash = overlaps(o, [p for p in old.get("objects", []) if p["id"] != o["id"]])
        if clash:
            errs.append(f"{mid}: prop '{o['id']}' overlaps existing object '{clash}'")
    for (x, y) in sorted(foot):
        if not before.in_bounds(x, y):
            errs.append(f"{mid}: prop tile {(x, y)} out of bounds")
            continue
        i = y * W + x
        if meta.get(base[i], {}).get("terrain") in LANE_TERRAINS:
            errs.append(f"{mid}: prop tile {(x, y)} sits on a lane (path/trail)")
        # Open DEEP sea rolls rowed encounters everywhere (10 §2): a buoy on it
        # hides no bed the way a prop on a grass patch would.
        deep_only = all(meta.get(l["data"][i], {}).get("encounter_terrain") in (None, "deep")
                        for l in m["layers"] if l.get("data"))
        if before.encounter[i] and not deep_only:
            errs.append(f"{mid}: prop tile {(x, y)} covers an encounter tile")
        if (x, y) in near:
            errs.append(f"{mid}: prop tile {(x, y)} on/next to a warp, trigger or NPC post")
    if errs:
        return errs
    starts = sorted(busy)
    goals = sorted(busy | talk)
    # The DRY-LANE proof: the walk that dodges every encounter tile, sight line
    # and step-on story band (the "unbroken dry lane" the easing promised) must
    # survive too — no prop may push a player into grass or a trainer's eye.
    hot = {(i % W, i // W) for i, e in enumerate(before.encounter) if e}
    for tiles in before.sight_tiles().values():
        hot |= tiles
    hot |= {(t["at"]["tx"], t["at"]["ty"]) for t in m.get("triggers", [])
            if t.get("activation") == "step_on"}
    for s in starts:
        db = before.bfs([s], abilities=set(), avoid=hot)
        da = after.bfs([s], abilities=set(), avoid=hot)
        for g in starts:
            if g in db and (g not in da or da[g] > db[g]):
                errs.append(f"{mid}: props close/lengthen the dry lane {s}->{g} ({db[g]} -> {da.get(g)})")
                return errs
    for gifts in (set(), ALL_GIFTS):
        rb = before.bfs(starts, abilities=gifts)
        ra = after.bfs(starts, abilities=gifts)
        lost = set(rb) - set(ra) - foot
        if lost:
            errs.append(f"{mid}: props cut off {len(lost)} reachable tile(s), e.g. {sorted(lost)[:3]}")
        for s in starts:
            db = before.bfs([s], abilities=gifts)
            da = after.bfs([s], abilities=gifts)
            for g in goals:
                # content tiles are often solid (an NPC body): measure to the nearest
                # neighbour you'd stand on to talk/step.
                cand = [g] + [(g[0] + dx, g[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                b = min((db[c] for c in cand if c in db), default=None)
                a = min((da[c] for c in cand if c in da), default=None)
                if b is not None and (a is None or a > b):
                    errs.append(f"{mid}: props lengthen the walk {s}->{g} ({b} -> {a}) with gifts={sorted(gifts)}")
                    return errs
    return errs


def lint(mid: str, m: dict, spec: dict) -> list[str]:
    errs: list[str] = []
    amb = spec.get("ambience")
    if amb is not None:
        # a story-state override (`when`: [{flag, ambience}]) is linted like the block itself
        for blk in [amb] + [r.get("ambience", {}) for r in amb.get("when", [])]:
            for k in blk:
                if k not in AMBIENCE_KEYS:
                    errs.append(f"{mid}: unknown ambience key '{k}'")
            for p in blk.get("particles", []):
                if p.get("kind") not in PARTICLE_KINDS:
                    errs.append(f"{mid}: unknown particle kind '{p.get('kind')}'")
    extra = set(spec) - {"ambience", "npcs", "objects", "triggers", "signs", "sprites", "after", "talk"}
    if extra:
        errs.append(f"{mid}: unknown spec keys {sorted(extra)}")
    spec_ids = {o["id"] for o in spec.get("objects", [])}
    shipped = [o for o in m.get("objects", []) if o["id"] not in spec_ids]
    for o in spec.get("objects", []):
        clash = overlaps(o, shipped + [p for p in spec["objects"] if p["id"] != o["id"]])
        if clash:
            errs.append(f"{mid}: object '{o['id']}' overlaps object '{clash}'")
    ids = {n["id"] for n in m.get("npcs", [])}
    for nid, sprite in spec.get("sprites", {}).items():
        if nid not in ids:
            errs.append(f"{mid}: sprite swap for unknown NPC '{nid}'")
        if str(sprite).startswith("kin_") or sprite == "item_cache":
            errs.append(f"{mid}: sprite swap '{nid}' -> '{sprite}' is not a person sheet")
    if mid in PRE_CHICKENPIG:
        for key in ("triggers", "signs"):
            if spec.get(key):
                errs.append(f"{mid}: pre-Chickenpig map — '{key}' not allowed (ambience, cast swaps, off-lane props only)")
        shipped_npcs = {n["id"]: n for n in m.get("npcs", [])}
        for n in spec.get("npcs", []):
            if not n.get("ambient"):
                errs.append(f"{mid}: pre-Chickenpig map — NPC '{n['id']}' must be ambient")
            old_n = shipped_npcs.get(n["id"])
            if old_n is not None and not old_n.get("ambient"):
                errs.append(f"{mid}: pre-Chickenpig map — '{n['id']}' would REPLACE a story NPC "
                            f"(use the `sprites` key for a cast swap)")
        shipped_objs = {o["id"]: o for o in m.get("objects", [])}
        to_prove = []
        for o in spec.get("objects", []):
            old_o = shipped_objs.get(o["id"])
            if old_o is None:
                to_prove.append(o)   # a NEW prop: must prove it changes nothing
                continue
            same_but_sprite = {k: v for k, v in old_o.items() if k != "sprite"} == \
                              {k: v for k, v in o.items() if k != "sprite"}
            if not same_but_sprite:
                errs.append(f"{mid}: pre-Chickenpig map — shipped object '{o['id']}' may only change "
                            f"its sprite (same footprint/solidity/flags)")
        # A sprite-only re-skin of a shipped object changes no tile, so only NEW
        # props need the off-lane proof (a shop has always covered its own door).
        if to_prove:
            errs += prove_off_lane(mid, m, to_prove)
    model = MapModel(m)
    busy = {(w["at"]["tx"], w["at"]["ty"]) for w in m.get("warps", [])}
    busy |= {(t["at"]["tx"], t["at"]["ty"]) for t in m.get("triggers", [])}
    for n in spec.get("npcs", []):
        if not n.get("ambient"):
            continue
        at = (n["at"]["tx"], n["at"]["ty"])
        if not model.standable(*at, abilities=set()):
            errs.append(f"{mid}: ambient '{n['id']}' at {at} is not foot-walkable")
        if at in busy:
            errs.append(f"{mid}: ambient '{n['id']}' at {at} sits on a warp/trigger tile")
        if not str(n.get("sprite", "")).startswith("kin_"):
            errs.append(f"{mid}: ambient '{n['id']}' should use a kin_<id>_overworld sprite")
    errs += lint_words(mid, m, spec)
    return errs


# ------------------------------------------------------------ AFTER-GLEAM words
# "after": the flag-pair twin; "talk": a dialogue re-point (worldcraft/_kit.py).
# Both change WORDS only: same tile, body, facing, movement — so both are legal on
# pre-Chickenpig maps. Applied to the spec's own NPC items (so a module-authored
# NPC never fights its own upsert) and, for builder/hand-placed NPCs, to the map.

def lit_pair(orig: dict, a: dict) -> tuple[dict, dict]:
    """(the shipped NPC hidden once `flag` is held, its `<id>_lit` twin shown then)."""
    o = dict(orig)
    o["hidden_when_flag"] = a["flag"]
    t = {k: v for k, v in orig.items() if k != "hidden_when_flag"}
    t["id"] = f"{orig['id']}_lit"
    t["dialogue_ref"] = a["ref"]
    t["requires_flag"] = a["flag"]
    return o, t


def lint_words(mid: str, m: dict, spec: dict) -> list[str]:
    errs: list[str] = []
    npcs = {n["id"]: n for n in m.get("npcs", [])}
    npcs.update({n["id"]: n for n in spec.get("npcs", [])})
    after = spec.get("after", [])
    talk = spec.get("talk", {})
    for a in after:
        nid, flag = a["npc"], a["flag"]
        n = npcs.get(nid)
        if n is None:
            errs.append(f"{mid}: after-twin for unknown NPC '{nid}'")
            continue
        if nid in talk:
            errs.append(f"{mid}: '{nid}' has both an after-twin and a talk re-point — pick one")
        if n.get("ambient") or n.get("sight_range") or n.get("sprite") == "item_cache":
            errs.append(f"{mid}: '{nid}' is ambient/a trainer/a cache — not a talk NPC")
        if n.get("hidden_when_flag") not in (None, flag):
            errs.append(f"{mid}: '{nid}' already hides on '{n['hidden_when_flag']}' — use `talk`")
        if n.get("requires_flag") not in (None, a.get("implies")):
            errs.append(f"{mid}: '{nid}' requires '{n['requires_flag']}' — pass implies= if "
                        f"'{flag}' guarantees it, else use `talk`")
        tid = f"{nid}_lit"
        if tid in npcs and npcs[tid].get("requires_flag") != flag:
            errs.append(f"{mid}: twin id '{tid}' is already a different NPC")
        if not a["ref"].startswith(("npc.", "script.")):
            errs.append(f"{mid}: after-twin '{nid}' ref '{a['ref']}' is not npc.*/script.*")
    for nid, ref in talk.items():
        n = npcs.get(nid)
        if n is None:
            errs.append(f"{mid}: talk re-point for unknown NPC '{nid}'")
        elif n.get("ambient") or n.get("sight_range") or n.get("sprite") == "item_cache":
            errs.append(f"{mid}: '{nid}' is ambient/a trainer/a cache — not a talk NPC")
        if not str(ref).startswith("script."):
            errs.append(f"{mid}: talk re-point '{nid}' -> '{ref}' must be a staged script.*")
    return errs


def words_on_spec(spec: dict) -> tuple[dict, set[str]]:
    """Apply after/talk to the spec's own NPC items; return (spec, ids handled)."""
    after = {a["npc"]: a for a in spec.get("after", [])}
    talk = spec.get("talk", {})
    done: set[str] = set()
    out = []
    for n in spec.get("npcs", []):
        if n["id"] in after:
            out += list(lit_pair(n, after[n["id"]]))
            done.add(n["id"])
        elif n["id"] in talk:
            out.append(dict(n, dialogue_ref=talk[n["id"]]))
            done.add(n["id"])
        else:
            out.append(n)
    if "npcs" in spec:
        spec = dict(spec, npcs=out)
    return spec, done


def words_on_map(m: dict, spec: dict, done: set[str]) -> bool:
    changed = False
    lst = m.setdefault("npcs", [])
    for nid, ref in spec.get("talk", {}).items():
        if nid in done:
            continue
        for n in lst:
            if n["id"] == nid and n.get("dialogue_ref") != ref:
                n["dialogue_ref"] = ref
                changed = True
    for a in spec.get("after", []):
        if a["npc"] in done:
            # upserted from the spec: just keep the twin right after its original
            # (a fresh rebuild and the shipped map must agree on list order)
            i = next(i for i, n in enumerate(lst) if n["id"] == a["npc"])
            j = next(j for j, n in enumerate(lst) if n["id"] == f"{a['npc']}_lit")
            if j != i + 1:
                t = lst.pop(j)
                lst.insert(i + 1 if j > i else i, t)
                changed = True
            continue
        i = next(i for i, n in enumerate(lst) if n["id"] == a["npc"])
        o, t = lit_pair(lst[i], a)
        if lst[i] != o:
            lst[i] = o
            changed = True
        j = next((j for j, n in enumerate(lst) if n["id"] == t["id"]), None)
        if j is None:
            lst.insert(i + 1, t)
            changed = True
        elif lst[j] != t:
            lst[j] = t
            changed = True
    return changed


def apply(mid: str, spec: dict, write: bool) -> tuple[bool, list[str]]:
    path = MAPS / f"{mid}.json"
    if not path.is_file():
        return False, [f"{mid}: no shipped map JSON"]
    m = json.loads(path.read_text())
    # Region helpers return None for an NPC a rebuilt map doesn't carry yet.
    spec = {k: ([x for x in v if x is not None] if isinstance(v, list) else v) for k, v in spec.items()}
    errs = lint(mid, m, spec)
    if errs:
        return False, errs
    spec, words_done = words_on_spec(spec)
    changed = False
    if "ambience" in spec:
        if m.get("ambience") != spec["ambience"]:
            m["ambience"] = spec["ambience"]
            changed = True
    for key in ("objects", "npcs", "triggers"):
        for item in spec.get(key, []):
            changed |= upsert(m.setdefault(key, []), item)
    for n in m.get("npcs", []):
        new = spec.get("sprites", {}).get(n["id"])
        if new and n.get("sprite") != new:
            n["sprite"] = new
            changed = True
    # after the cast swaps, so a twin always wears its original's final sheet
    changed |= words_on_map(m, spec, words_done)
    if spec.get("signs"):
        W = m["width"]
        deco = next(l for l in m["layers"] if l.get("role") == "deco")["data"]
        for (sid, (x, y), ref) in spec["signs"]:
            if deco[y * W + x] != SIGN_GID:
                deco[y * W + x] = SIGN_GID
                changed = True
            changed |= upsert(m.setdefault("triggers", []),
                              {"id": f"sign_{sid}", "kind": "sign", "at": {"tx": x, "ty": y},
                               "activation": "interact", "ref": ref})
    if changed and write:
        path.write_text(json.dumps(m, indent=2) + "\n")
    return changed, []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--region", choices=REGIONS, action="append")
    ap.add_argument("--check", action="store_true", help="report drift, write nothing")
    args = ap.parse_args()
    regions = args.region or list(REGIONS)
    drift: list[str] = []
    errors: list[str] = []
    for r in regions:
        mod = importlib.import_module(f"worldcraft.{r}")
        for mid, spec in getattr(mod, "PLACEMENTS", {}).items():
            changed, errs = apply(mid, spec, write=not args.check)
            errors += errs
            if changed:
                drift.append(f"{r}:{mid}")
    for e in errors:
        print(f"ERROR {e}")
    verb = "would change" if args.check else "updated"
    print(f"world-craft: {verb} {len(drift)} map(s): {', '.join(drift) or '-'}")
    if errors:
        return 2
    return 1 if drift and args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
