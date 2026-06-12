#!/usr/bin/env python3
"""
add_vigil_scars — the ONLY host-map edits the Starfall Vigils make
(walkthrough/06-postgame, "the chain master list"): each shipped host gains

  * ONE added step_on warp into its `vigil_*` annex, gated
    `requires_flag: flag:vigil_reading_<n>` with the watchers' sealed line
    (`blocked_ref: npc.vigil_scar_sealed`), and
  * the optional non-solid star-scar deco object (`vigil_star_scar`,
    `requires_flag: flag:dawn`) marking where the shard fell.

Surgical JSON edits (NOT a builder re-run): several hosts carry post-build
hand-curation (R5 encounter sync etc.), so we never regenerate them. The
script is idempotent — re-running replaces its own entries and nothing else.

Run:  ./venv/bin/python tools/maps/add_vigil_scars.py
      (then audit: ./venv/bin/python tools/maps/audit_warps.py <host> ...)
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAPS = REPO / "public" / "assets" / "maps"

# host map -> (warp id, host tile, annex map, annex landing, arrive-facing,
#              reading flag, scar tile)
SCARS = [
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


def main() -> None:
    for host, wid, (hx, hy), annex, (ax, ay), flag, (sx, sy) in SCARS:
        path = MAPS / f"{host}.json"
        m = json.loads(path.read_text())

        warps = [w for w in m.get("warps", []) if w["id"] != wid]
        warps.append({
            "id": wid, "at": {"tx": hx, "ty": hy}, "trigger": "step_on",
            "to_map": annex, "to": {"tx": ax, "ty": ay}, "facing": "up",
            "requires_flag": flag, "blocked_ref": "npc.vigil_scar_sealed",
            "transition": "fade",
        })
        m["warps"] = warps

        scar_id = f"vigil_scar_{annex.split('_', 1)[1]}"
        objs = [o for o in m.get("objects", []) if o["id"] != scar_id]
        objs.append({
            "id": scar_id, "sprite": "vigil_star_scar",
            "at": {"tx": sx, "ty": sy}, "w": 1, "h": 1,
            "solid": False, "requires_flag": "flag:dawn",
        })
        m["objects"] = objs

        path.write_text(json.dumps(m, indent=2) + "\n")
        print(f"{host}: +warp {wid} ({hx},{hy}) -> {annex} ({ax},{ay}), "
              f"+scar {scar_id} ({sx},{sy})")


if __name__ == "__main__":
    main()
