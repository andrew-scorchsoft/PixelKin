"""Helpers for the per-region world-craft modules (tools/maps/worldcraft/<region>.py).

A module's `PLACEMENTS` maps a shipped map id to a spec:

    {
      "ambience": {...},      # MapDefinition.ambience — REPLACES the map's whole block
      "npcs":     [...],      # upserted by id (ambient kin via `ambient_kin`)
      "objects":  [...],      # upserted by id
      "triggers": [...],      # upserted by id (non-sign triggers)
      "signs":    [(id, (x, y), "sign.ref"), ...],  # trigger + the sign deco tile
    }

Pre-Chickenpig maps (PRE_CHICKENPIG) accept ONLY "ambience" and ambient NPCs —
the runner refuses anything else there (the world-craft panel's hard rule).
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
INDEX = json.loads((REPO / "assets/tilesets/_shared/vesper_overworld.index.json").read_text())


def gid(name: str) -> int:
    """Global gid of a shared-overworld tile by name (every overworld map uses the
    shared set at first_gid 1) — e.g. gid("buoy") for `ambience.bob_gids`."""
    return INDEX[name] + 1


def ambient_kin(nid: str, at: tuple[int, int], kin_id: int, *, radius: int = 2,
                requires: str | None = None, hidden: str | None = None) -> dict:
    """An AMBIENT kin placement: grazes within `radius` of `at`, never collides,
    never talks, hops away from the player. Pick `kin_id` from the map's OWN
    encounter table, and put `at` OFF the walking lane."""
    n = {"id": nid, "at": {"tx": at[0], "ty": at[1]}, "facing": "down",
         "sprite": f"kin_{kin_id}_overworld", "movement": "wander",
         "ambient": True, "wander_radius": radius}
    if requires:
        n["requires_flag"] = requires
    if hidden:
        n["hidden_when_flag"] = hidden
    return n


def particles(kind: str, density: float | None = None, area=None) -> dict:
    p: dict = {"kind": kind}
    if density is not None:
        p["density"] = density
    if area is not None:
        p["area"] = area
    return p


# The pre-Chickenpig path (world-craft panel §4 hard rule): visual/ambient/feel
# changes ONLY — the runner refuses non-ambient NPCs, objects, triggers or signs.
PRE_CHICKENPIG = {
    "tinderwick", "tinderwick_house", "tinderwick_shop", "tinderwick_lumenary",
    "tinderwick_beacon_i", "tinderwick_beacon_ii", "tinderwick_beacon_top",
    "duskapple_orchard", "lanternway_tinderwick", "vesper_crossroads", "crossroads_inn",
    "dimglass_coast", "dimglass_coast_ii", "tideglass_cavern",
    "pearlmoor_quay", "pearlmoor_inn", "pearlmoor_shop", "pearlmoor_lumenary",
    "pearlmoor_lifting_house", "pearlmoor_point", "pearlmoor_breakwater",
    *(f"pearlmoor_oldlight_{n}" for n in (1, 2, 3, 4, 5, 6, "top")),
}

# Keys the engine reads from MapDefinition.ambience (data/world/types.ts MapAmbience).
AMBIENCE_KEYS = {"particles", "mist", "tint", "starfall", "birds", "light_sources_extra",
                 "sound_bed", "footprints", "bob_gids"}
PARTICLE_KINDS = {"snow", "ash", "embers", "glowmotes", "spores", "spray", "motes",
                  "leaves", "starglint", "dust"}
