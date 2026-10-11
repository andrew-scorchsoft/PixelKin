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
  * pre-Chickenpig maps take ONLY "ambience" + ambient NPCs (the hard rule);
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
REGIONS = ("south", "east", "north", "west", "central")
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


def lint(mid: str, m: dict, spec: dict) -> list[str]:
    errs: list[str] = []
    amb = spec.get("ambience")
    if amb is not None:
        for k in amb:
            if k not in AMBIENCE_KEYS:
                errs.append(f"{mid}: unknown ambience key '{k}'")
        for p in amb.get("particles", []):
            if p.get("kind") not in PARTICLE_KINDS:
                errs.append(f"{mid}: unknown particle kind '{p.get('kind')}'")
    extra = set(spec) - {"ambience", "npcs", "objects", "triggers", "signs"}
    if extra:
        errs.append(f"{mid}: unknown spec keys {sorted(extra)}")
    if mid in PRE_CHICKENPIG:
        for key in ("objects", "triggers", "signs"):
            if spec.get(key):
                errs.append(f"{mid}: pre-Chickenpig map — '{key}' not allowed (ambience + ambient kin only)")
        for n in spec.get("npcs", []):
            if not n.get("ambient"):
                errs.append(f"{mid}: pre-Chickenpig map — NPC '{n['id']}' must be ambient")
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
    return errs


def apply(mid: str, spec: dict, write: bool) -> tuple[bool, list[str]]:
    path = MAPS / f"{mid}.json"
    if not path.is_file():
        return False, [f"{mid}: no shipped map JSON"]
    m = json.loads(path.read_text())
    errs = lint(mid, m, spec)
    if errs:
        return False, errs
    changed = False
    if "ambience" in spec:
        if m.get("ambience") != spec["ambience"]:
            m["ambience"] = spec["ambience"]
            changed = True
    for key in ("objects", "npcs", "triggers"):
        for item in spec.get(key, []):
            changed |= upsert(m.setdefault(key, []), item)
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
