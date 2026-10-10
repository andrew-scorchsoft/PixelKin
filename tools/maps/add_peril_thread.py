#!/usr/bin/env python3
"""
add_peril_thread — the PERIL THREAD's surgical placements on shipped maps (R9,
docs/world/walkthrough/08-the-peril-thread.md).

The thread's first beat (the fallen star in Duskapple Orchard) lives in that
map's own builder (`build_duskapple_orchard.py`). Every LATER beat sits on a
shipped map whose JSON carries post-build additions its builder doesn't (see
CLAUDE.md), so they are applied here instead: an idempotent, id-keyed upsert of
NPCs / objects / sign triggers (+ the sign's deco tile), the add_vigil_scars.py
pattern. Re-run it after ANY rebuild of one of these maps.

Every beat is OPTIONAL COLOUR: nothing here gates a warp, blocks a lane or sets a
progression flag. Escalation and healing ride flags the journey already sets
(gleam:*, flag:met_cor, flag:great_null_known, flag:keystar_relit, flag:dawn)
through flag-staged scripts (if_flag / unless_flag), plus same-footprint object
swap pairs (collision is flag-blind).

Run:  python3 tools/maps/add_peril_thread.py           # apply
      python3 tools/maps/add_peril_thread.py --check   # report drift, write nothing
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public" / "assets" / "maps"
INDEX = json.loads((REPO / "assets/tilesets/_shared/vesper_overworld.index.json").read_text())
SIGN_GID = INDEX["sign"] + 1          # every overworld map uses the shared set at first_gid 1


def npc(nid, at, sprite, ref, facing="down", requires=None, hidden=None):
    n = {"id": nid, "at": {"tx": at[0], "ty": at[1]}, "facing": facing, "sprite": sprite,
         "movement": "static", "dialogue_ref": ref}
    if requires:
        n["requires_flag"] = requires
    if hidden:
        n["hidden_when_flag"] = hidden
    return n


def obj(oid, sprite, at, w, h, **kw):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    return o


# map id -> {"npcs": [...], "objects": [...], "objects_first": [...], "signs": [(id, at, ref)],
#            "clear_deco": [(x0, y0, w, h)]}
PLACEMENTS: dict[str, dict] = {
    # S3 — the harbour notice on Pearlmoor Quay, beside the harbour sign by the
    # south landing (the tide-lamps on the north shore failing).
    "pearlmoor_quay": {
        "signs": [("sign_peril_pearlmoor_board", (17, 16), "sign.peril_pearlmoor_board")],
    },
    # E1 — the fen family leaving (Saltreach Fen I, by the landing). Bundles go
    # once the Verdant Gleam is relit: they unpacked. Non-solid, so the swap
    # can't leave an invisible wall.
    "saltreach_fen_i": {
        "npcs": [npc("peril_fen_leaver", (5, 41), "npc_parent", "script.peril_fen_leaver",
                     facing="right")],
        "objects": [obj("peril_fen_bundles", "interior_sacks", (6, 41), 2, 1, solid=False,
                        hidden_when_flag="gleam:verdant")],
    },
    # N1 — the Hollowing's gentle notice on Galehigh's plaza, and a weaver who
    # can't decide whether to tear it down.
    "galehigh_terraces": {
        "signs": [("peril_quiet_notice", (8, 20), "sign.peril_quiet_notice")],
        "npcs": [npc("peril_notice_reader", (9, 20), "npc_woman", "script.peril_notice_reader",
                     facing="left")],
    },
    # N2 — the SECOND FALL: a fresh crater in the snow of Hushfrost Pass (the
    # orchard's kit: crater decal + cold cinder, waking to a shard at dawn), and
    # a pass-walker who has started counting.
    "hushfrost_pass_i": {
        "objects_first": [obj("peril_star_crater", "fallenstar_crater_snow", (15, 22), 6, 4,
                              solid=False)],
        "objects": [obj("peril_cinder_star", "fallenstar_cinder_star", (17, 23), 2, 2,
                        overhang=1, hidden_when_flag="flag:dawn"),
                    obj("peril_cinder_star_woken", "vigil_star_shard", (17, 23), 2, 2,
                        overhang=1, requires_flag="flag:dawn")],
        "clear_deco": [(15, 22, 6, 4)],
        "npcs": [npc("peril_hushfrost_counter", (21, 22), "npc_old_woman",
                     "script.peril_hushfrost_counter", facing="left")],
    },
    # W1 — the family who chose the quiet (Sunvault Climb I, by the gorge mouth):
    # they put their own brazier out. It is lit again once the Solar Gleam is
    # (same 2x3 footprint + solidity).
    "sunvault_climb_i": {
        "objects": [obj("peril_quiet_brazier", "solarium_brazier_dead", (24, 6), 2, 3,
                        overhang=1, hidden_when_flag="gleam:solar"),
                    obj("peril_quiet_brazier_lit", "solarium_brazier_lit", (24, 6), 2, 3,
                        overhang=1, requires_flag="gleam:solar")],
        "npcs": [npc("peril_quiet_family", (26, 8), "npc_parent", "script.peril_quiet_family",
                     facing="left")],
    },
    # W2 — the Ledger of Lights at Nightreach: the count that only ever went up.
    "nightreach_observatory": {
        "npcs": [npc("peril_ledger_keeper", (9, 23), "npc_old_man", "script.peril_ledger",
                     facing="down")],
    },
    # C1 — the gone-quiet, come to the ring to see the Spire for themselves.
    "penumbra_ring": {
        "npcs": [npc("peril_gone_quiet", (21, 19), "npc_woman", "script.peril_gone_quiet",
                     facing="up")],
    },
    # P1 — the bookend: Maudie in Dawnstead, with the orchard's news (sends the
    # post-game player home to see the crater flower).
    "dawnstead": {
        "npcs": [npc("peril_maudie_dawn", (11, 15), "npc_woman", "npc.peril_maudie_dawn",
                     facing="down", requires="flag:dawn")],
    },
}


def upsert(lst: list, item: dict, *, first: bool = False) -> bool:
    for i, cur in enumerate(lst):
        if cur.get("id") == item["id"]:
            if cur == item:
                return False
            lst[i] = item
            return True
    if first:
        lst.insert(0, item)
    else:
        lst.append(item)
    return True


def apply(mid: str, spec: dict) -> bool:
    path = MAPS / f"{mid}.json"
    m = json.loads(path.read_text())
    W = m["width"]
    changed = False
    deco = next(l for l in m["layers"] if l.get("role") == "deco")["data"]
    for item in spec.get("objects_first", []):
        changed |= upsert(m.setdefault("objects", []), item, first=True)
    for item in spec.get("objects", []):
        changed |= upsert(m.setdefault("objects", []), item)
    for item in spec.get("npcs", []):
        changed |= upsert(m.setdefault("npcs", []), item)
    for (x0, y0, w, h) in spec.get("clear_deco", []):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if deco[y * W + x]:
                    deco[y * W + x] = 0
                    changed = True
    for (sid, (x, y), ref) in spec.get("signs", []):
        if deco[y * W + x] != SIGN_GID:
            deco[y * W + x] = SIGN_GID
            changed = True
        changed |= upsert(m.setdefault("triggers", []),
                          {"id": f"sign_{sid}", "kind": "sign", "at": {"tx": x, "ty": y},
                           "activation": "interact", "ref": ref})
    if changed and "--check" not in sys.argv:
        path.write_text(json.dumps(m, indent=2) + "\n")
    return changed


def main() -> int:
    drift = [mid for mid, spec in PLACEMENTS.items() if apply(mid, spec)]
    verb = "would change" if "--check" in sys.argv else "updated"
    print(f"peril thread: {verb} {len(drift)} map(s): {', '.join(drift) or '-'}")
    return 1 if drift and "--check" in sys.argv else 0


if __name__ == "__main__":
    raise SystemExit(main())
