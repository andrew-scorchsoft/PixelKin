"""Helpers for the per-region world-craft modules (tools/maps/worldcraft/<region>.py).

A module's `PLACEMENTS` maps a shipped map id to a spec:

    {
      "ambience": {...},      # MapDefinition.ambience — REPLACES the map's whole block
      "npcs":     [...],      # upserted by id (ambient kin via `ambient_kin`)
      "objects":  [...],      # upserted by id
      "triggers": [...],      # upserted by id (non-sign triggers)
      "signs":    [(id, (x, y), "sign.ref"), ...],  # trigger + the sign deco tile
      "after":    [lit(id, "gleam:x", "npc.ref"), ...],  # post-Gleam flag-pair twins
      "talk":     {npc_id: "script.ref"},   # re-point an NPC's dialogue (keeps id/tile/flags)
    }

Pre-Chickenpig maps (PRE_CHICKENPIG) accept ONLY "ambience", ambient NPCs, "sprites"
(cast swaps on existing NPC ids), "after"/"talk" (words only) and "objects" the
runner PROVES off-lane — the runner refuses anything else there (the world-craft
panel's hard rule).

AFTER-GLEAM (2026-10): "after" turns one NPC into a visibility swap pair — the
shipped placement gains `hidden_when_flag: <flag>` and a twin `<id>_lit` (same
tile, sprite, facing, movement, solidity) with `requires_flag: <flag>` reads the
new line. "talk" re-points an NPC whose flags are already spoken for (a staged
chain, a shop, an actor some cutscene addresses by id) at a region script that
stages its own pages with `if_flag`/`unless_flag`. Both change WORDS only — no
tile, body or warp moves — so both are allowed on pre-Chickenpig maps too. The
new lines/scripts live in src/game/content/regions/<region>.ts.
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


def lit(nid: str, flag: str, ref: str, *, implies: str | None = None) -> dict:
    """A post-Gleam flag-pair twin for NPC `nid` (see the module docstring).
    `implies`: the shipped NPC's own `requires_flag`, acknowledged as implied by
    `flag` (the twin drops it — e.g. every Ember holder has `flag:has_starter`)."""
    a = {"npc": nid, "flag": flag, "ref": ref}
    if implies:
        a["implies"] = implies
    return a


def add_words(placements: dict[str, dict], words: dict[str, dict]) -> None:
    """Merge a module's AFTER-GLEAM table ({map: {"after": [...], "talk": {...}}})
    into its PLACEMENTS, so the word changes sit in one block per region."""
    for mid, w in words.items():
        spec = placements.setdefault(mid, {})
        for key, val in w.items():
            if key == "after":
                spec["after"] = list(spec.get("after", [])) + list(val)
            elif key == "talk":
                spec["talk"] = {**spec.get("talk", {}), **val}
            else:
                raise KeyError(f"add_words: {mid}: unknown key {key!r}")


def particles(kind: str, density: float | None = None, area=None) -> dict:
    p: dict = {"kind": kind}
    if density is not None:
        p["density"] = density
    if area is not None:
        p["area"] = area
    return p


# The pre-Chickenpig path (world-craft panel §4 hard rule): visual/ambient/feel
# changes ONLY — the runner refuses non-ambient NPCs, triggers and signs, and
# admits a prop only through prove_off_lane (add_world_craft.py).
PRE_CHICKENPIG = {
    "tinderwick", "tinderwick_house", "tinderwick_shop", "tinderwick_lumenary",
    "tinderwick_beacon_i", "tinderwick_beacon_ii", "tinderwick_beacon_top",
    "duskapple_orchard", "lanternway_tinderwick", "vesper_crossroads", "crossroads_inn",
    "dimglass_coast", "dimglass_coast_ii", "tideglass_cavern",
    "pearlmoor_quay", "pearlmoor_inn", "pearlmoor_shop", "pearlmoor_lumenary",
    "pearlmoor_lifting_house", "pearlmoor_lifting_house_b1", "pearlmoor_point", "pearlmoor_breakwater",
    *(f"pearlmoor_oldlight_{n}" for n in (1, 2, 3, 4, 5, 6, "top")),
}

# Keys the engine reads from MapDefinition.ambience (data/world/types.ts MapAmbience).
AMBIENCE_KEYS = {"particles", "mist", "tint", "starfall", "birds", "light_sources_extra",
                 "sound_bed", "footprints", "bob_gids"}
PARTICLE_KINDS = {"snow", "ash", "embers", "glowmotes", "spores", "spray", "motes",
                  "leaves", "starglint", "dust"}
