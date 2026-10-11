#!/usr/bin/env python3
"""
add_hand_placed — the HAND-PLACED additions on shipped maps that no builder emits.

Shipped map JSONs grew content after their builders were last run: whole quest
lines, the postgame and a few tuning passes were wired as surgical JSON edits.
This runner owns all of it, as an idempotent, id-keyed upsert (the
add_peril_thread.py pattern), so `builder -> add_hand_placed -> add_peril_thread
-> add_world_craft -> vary_trees` reproduces every shipped map EXACTLY
(tools/maps/check_rebuild.py proves it). It runs FIRST of the runners: the later
ones re-dress what it places (world-craft swaps regional-cast sprites onto its
NPCs, vary_trees re-skins its trees).

What it owns (data: tools/maps/hand_placed_data.py, one entry per map):
  * the R3 Starfall Vigil host edits (VIGIL_SCARS: the gated step_on warp into
    each `vigil_*` annex + the dawn-only star-scar deco object) — formerly
    add_vigil_scars.py;
  * the R4 day-form zone pairs (`day`: every night zone listed gets
    `hidden_when_flag: flag:dawn` and a `<id>_day` twin — same rect/terrain/rate,
    the post-dawn table, `requires_flag: flag:dawn`);
  * zone-table / rate retunes made after the build (`patch` — the R5 dex sync,
    the 2026-10 coast easing): the in-map tables are the truth that
    build_species.py's EXTRA_ENCOUNTERS mirrors;
  * hand-added NPCs / objects / triggers / warps / zones (`npcs` ... `encounters`):
    the P1 letter recipients, Oriel's terrace set, the summit re-dress, the
    Spire's null-works, Andrew on his fences, the wick-purse caches, the egg
    trail, the Worry Club, the S4/S5 quest pieces, the dawn-relit lanterns ...
  * `signs`: (id, (x, y), ref) — the sign trigger + its deco tile.

An item may carry `_before: <id>` to be inserted ahead of that entry (list order
is shipped order). On an item that already exists, its `sprite` is left alone:
regional-cast swaps (add_world_craft) and tree crowns (vary_trees) own that field.

Run:  python3 tools/maps/add_hand_placed.py           # apply
      python3 tools/maps/add_hand_placed.py --check   # report drift, write nothing (exit 1)
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from hand_placed_data import PLACEMENTS  # noqa: E402

REPO = HERE.parents[1]
MAPS = REPO / "public" / "assets" / "maps"
INDEX = json.loads((REPO / "assets/tilesets/_shared/vesper_overworld.index.json").read_text())
SIGN_GID = INDEX["sign"] + 1          # every overworld map uses the shared set at first_gid 1
LISTS = ("objects", "warps", "npcs", "triggers", "encounters")
DAWN = "flag:dawn"

# R3 — the Starfall Vigils' host edits (walkthrough/06-postgame, "the chain master
# list"): host map -> (warp id, host tile, annex map, annex landing, reading flag,
# scar tile). The warp is gated on the reading with the watchers' sealed line; the
# scar is the optional non-solid deco object marking where the shard fell.
VIGIL_SCARS = [
    ("tinderwick", "to_vigil_hearth", (25, 7), "vigil_hearthfall", (11, 16),
     "flag:vigil_reading_1", (25, 8)),
    ("spore_grotto", "to_vigil_grove", (15, 9), "vigil_grovefall", (11, 16),
     "flag:vigil_reading_2", (15, 10)),
    ("thunderroost", "to_vigil_storm", (5, 2), "vigil_stormfall", (11, 16),
     "flag:vigil_reading_3", (5, 1)),
    ("sunvault_climb_ii", "to_vigil_sun", (27, 2), "vigil_sunfall", (11, 16),
     "flag:vigil_reading_4", (27, 1)),
    ("coldfog_marches_ii", "to_vigil_murk", (14, 23), "vigil_murkfall", (11, 16),
     "flag:vigil_reading_5", (14, 24)),
]


def vigil_items(host: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for h, wid, (hx, hy), annex, (ax, ay), flag, (sx, sy) in VIGIL_SCARS:
        if h != host:
            continue
        out.setdefault("warps", []).append({
            "id": wid, "at": {"tx": hx, "ty": hy}, "trigger": "step_on",
            "to_map": annex, "to": {"tx": ax, "ty": ay}, "facing": "up",
            "requires_flag": flag, "blocked_ref": "npc.vigil_scar_sealed",
            "transition": "fade"})
        out.setdefault("objects", []).append({
            "id": f"vigil_scar_{annex.split('_', 1)[1]}", "sprite": "vigil_star_scar",
            "at": {"tx": sx, "ty": sy}, "w": 1, "h": 1,
            "solid": False, "requires_flag": DAWN})
    return out


def upsert(lst: list, item: dict) -> bool:
    item = dict(item)
    before = item.pop("_before", None)
    for i, cur in enumerate(lst):
        if cur.get("id") == item["id"]:
            if "sprite" in cur:
                item["sprite"] = cur["sprite"]      # the later runners own the sprite
            if cur == item:
                return False
            lst[i] = item
            return True
    at = next((i for i, cur in enumerate(lst) if cur.get("id") == before), None)
    if before is not None and at is None:
        raise SystemExit(f"add_hand_placed: _before '{before}' not found for '{item['id']}'")
    lst.insert(len(lst) if at is None else at, item)
    return True


def apply(mid: str, spec: dict, write: bool) -> bool:
    path = MAPS / f"{mid}.json"
    m = json.loads(path.read_text())
    before = copy.deepcopy(m)
    zones = m.setdefault("encounters", [])

    # retunes on builder-owned entries (tables, rates, flags) — field-level
    for key, by_id in spec.get("patch", {}).items():
        for iid, fields in by_id.items():
            cur = next((x for x in m.get(key, []) if x.get("id") == iid), None)
            if cur is None:
                raise SystemExit(f"add_hand_placed: {mid} has no {key} '{iid}' to patch")
            cur.update(fields)

    # whole items (vigil host edits first: they predate the rest)
    items = vigil_items(mid)
    for key in LISTS:
        items.setdefault(key, []).extend(spec.get(key, []))
    for key in LISTS:
        for item in items[key]:
            upsert(m.setdefault(key, []), item)

    # R4 day-form pairs
    for zid, table in spec.get("day", {}).items():
        night = next((z for z in zones if z["id"] == zid), None)
        if night is None:
            raise SystemExit(f"add_hand_placed: {mid} has no zone '{zid}' for a day twin")
        night["hidden_when_flag"] = DAWN
        twin = {k: v for k, v in night.items() if k != "hidden_when_flag"}
        twin.update(id=f"{zid}_day", table=table, requires_flag=DAWN)
        upsert(zones, twin)

    if spec.get("signs"):
        W = m["width"]
        deco = next(l for l in m["layers"] if l.get("role") == "deco")["data"]
        for (sid, (x, y), ref) in spec["signs"]:
            deco[y * W + x] = SIGN_GID
            upsert(m.setdefault("triggers", []),
                   {"id": f"sign_{sid}", "kind": "sign", "at": {"tx": x, "ty": y},
                    "activation": "interact", "ref": ref})

    changed = m != before
    if changed and write:
        path.write_text(json.dumps(m, indent=2) + "\n")
    return changed


def main() -> int:
    check = "--check" in sys.argv
    hosts = {h for (h, *_rest) in VIGIL_SCARS}
    mids = list(PLACEMENTS) + sorted(hosts - set(PLACEMENTS))
    drift = [mid for mid in mids if apply(mid, PLACEMENTS.get(mid, {}), write=not check)]
    verb = "would change" if check else "updated"
    print(f"hand-placed: {verb} {len(drift)} map(s): {', '.join(drift) or '-'}")
    return 1 if drift and check else 0


if __name__ == "__main__":
    raise SystemExit(main())
