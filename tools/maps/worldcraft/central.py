"""CENTRAL world-craft placements (owned by this region's package: the climax and
after — Penumbra Ring, Starwell, the Umbral Spire floors, the Three Hours sites,
Dawnstead and the five Starfall Vigils).

PLACEMENTS: map id -> spec (keys documented in _kit.py). Applied by
`python3 tools/maps/add_world_craft.py --region central`.

Structural changes (the Cinder Hoard room, the Ring's memorial lamps and the
gone-quiet, the vigils' prop kits, the Unrisen Stair's water, the Starwell's
dressing) live in their BUILDERS — this module carries only ambience, sprite
swaps on maps whose shipped JSON outruns its builder (f1/f2/summit/Dawnstead),
and the summit's two staging NPCs for the climax scenes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from ._kit import ambient_kin, gid, particles  # noqa: F401

MAPS = Path(__file__).resolve().parents[3] / "public" / "assets" / "maps"


def _swap(mid: str, nid: str, **changes) -> dict:
    """The shipped NPC placement `nid` on `mid`, with `changes` applied — so a
    sprite swap keeps every other field (ids/dialogue_refs/flags) byte-identical.
    Idempotent: re-reading an already-swapped map returns the same dict."""
    path = MAPS / f"{mid}.json"
    npc = None
    if path.is_file():
        npc = next((n for n in json.loads(path.read_text()).get("npcs", []) if n["id"] == nid), None)
    if npc is None:
        # A rebuilt map can lack a post-build NPC until its own runner re-adds it:
        # skip (the runner drops None) rather than crash the whole region at import.
        print(f"worldcraft.central: {mid} has no NPC '{nid}' yet — swap skipped", file=sys.stderr)
        return None  # type: ignore[return-value]
    return {**npc, **changes}


# ---- the ambience register, by place --------------------------------------------------
# The falls are DENSEST at the Ring (min_s 20, the engine's clamp): every fall
# lands nearer the mountain (story-bible §11). After flag:dawn the engine warms
# every streak to gold automatically.
SPIRE_AIR = {
    "particles": [particles("glowmotes", 0.45), particles("dust", 0.3)],
    "mist": {"color": "#0d0b1c", "alpha": 0.22, "speed": 3},
    "tint": {"color": "#08061a", "alpha": 0.16},
}

PLACEMENTS: dict[str, dict] = {
    # THE PENUMBRA RING — near-void mist, a dim tint, the densest starfall.
    "penumbra_ring": {
        "ambience": {
            "particles": [particles("starglint", 0.7), particles("dust", 0.35)],
            "mist": {"color": "#120e24", "alpha": 0.34, "speed": 3},
            "tint": {"color": "#0a0818", "alpha": 0.2},
            "starfall": {"min_s": 20, "max_s": 38},
        },
    },
    # THE STARWELL — the one star that never went cold: star-motes over the pool.
    "starwell": {
        "ambience": {
            "particles": [particles("starglint", 0.8), particles("motes", 0.4)],
            "tint": {"color": "#0c1030", "alpha": 0.12},
            "starfall": {"min_s": 24, "max_s": 50},
        },
    },
    # THE SPIRE — glowmotes in the dark climb; the falls go quiet indoors.
    "umbral_spire": {"ambience": SPIRE_AIR,
                     "npcs": [_swap("umbral_spire", "hollowing_acolyte_a", sprite="hollowing_acolyte"),
                              _swap("umbral_spire", "hollowing_acolyte_a_after", sprite="hollowing_acolyte")]},
    "umbral_spire_f2": {"ambience": SPIRE_AIR,
                        "npcs": [_swap("umbral_spire_f2", n, sprite=s) for n, s in (
                            ("hollowing_acolyte_b", "hollowing_acolyte"),
                            ("hollowing_acolyte_b_after", "hollowing_acolyte"),
                            ("hollowing_acolyte_c", "hollowing_elder"),
                            ("hollowing_acolyte_c_after", "hollowing_elder"))]},
    "umbral_spire_f3": {"ambience": {**SPIRE_AIR,
                                     "particles": [particles("glowmotes", 0.5),
                                                   particles("starglint", 0.3)]}},
    # THE SUMMIT — the open sky over the Great Null; starglint, a thinner tint.
    # Two staging placements for the climax scenes (X-2 / vignette 12):
    #   fenn_dawn  — climbs the dawn road in script.dawn_breaks and takes the rail
    #                beside Còr; parked in the dawn road's 2-wide gate chamber
    #                (never the 1-wide road) until the player reaches Dawnstead.
    #   fenn_round — stands for the Last Lesson (script.starfall_round says
    #                Senna's name with him), the vigilants' own flag window.
    "umbral_spire_summit": {
        "ambience": {
            "particles": [particles("starglint", 0.6), particles("glowmotes", 0.3)],
            "tint": {"color": "#0a0a22", "alpha": 0.1},
        },
        "npcs": [
            {"id": "fenn_dawn", "at": {"tx": 17, "ty": 19}, "facing": "up",
             "sprite": "npc_mentor", "movement": "static",
             "dialogue_ref": "npc.fenn_summit_dawn",
             "requires_flag": "flag:keystar_relit",
             "hidden_when_flag": "flag:dawnstead_arrived"},
            {"id": "fenn_round", "at": {"tx": 13, "ty": 13}, "facing": "up",
             "sprite": "npc_mentor", "movement": "static",
             "dialogue_ref": "npc.fenn_summit_round",
             "requires_flag": "flag:vigil_5_kept",
             "hidden_when_flag": "flag:starfall_lesson"},
            _swap("umbral_spire_summit", "vigil_ondra_summit", sprite="kite_weaver"),
            _swap("umbral_spire_summit", "vigil_solenne_summit", sprite="sun_keeper"),
            _swap("umbral_spire_summit", "vigil_mer_summit", sprite="hollowing_elder"),
        ],
    },
    # DAWNSTEAD — the first true morning: warm motes, a gold wash, birds about.
    "dawnstead": {
        "ambience": {
            "particles": [particles("motes", 0.6), particles("leaves", 0.25)],
            "tint": {"color": "#ffd089", "alpha": 0.08},
            "birds": {"kind": "bird", "flocks": [{"tx": 22, "ty": 14}, {"tx": 6, "ty": 25}],
                      "flyover": True},
            "starfall": {"min_s": 30, "max_s": 70},
        },
        "npcs": [
            _swap("dawnstead", "dawn_baker", sprite="market_trader"),
            _swap("dawnstead", "dawn_kid", sprite="village_child"),
            _swap("dawnstead", "starfall_witness", sprite="star_watcher"),
            _swap("dawnstead", "dawn_piper", sprite="innkeeper"),
        ],
    },
    # THE THREE HOURS — each site in its own register.
    "tideglass_cavern": {   # pre-Chickenpig: ambience only (the runner enforces it)
        "ambience": {"particles": [particles("glowmotes", 0.4), particles("spray", 0.5)],
                     "tint": {"color": "#0a2238", "alpha": 0.1}},
    },
    "tideglass_gallery": {
        "ambience": {"particles": [particles("glowmotes", 0.6)],
                     "mist": {"color": "#0d2a40", "alpha": 0.2, "speed": 2},
                     "tint": {"color": "#08203a", "alpha": 0.14}},
    },
    "pale_vault_hourfold": {
        "ambience": {"particles": [particles("snow", 0.35), particles("starglint", 0.4)],
                     "tint": {"color": "#1a2a4a", "alpha": 0.12}},
    },
    "unrisen_stair": {
        "ambience": {"particles": [particles("motes", 0.6), particles("dust", 0.25)],
                     "tint": {"color": "#ffcf7a", "alpha": 0.06},
                     "starfall": {"min_s": 35, "max_s": 80}},
    },
    # THE STARFALL VIGILS — the woken sky shedding warm shards; each in its element.
    "vigil_hearthfall": {
        "ambience": {"particles": [particles("embers", 0.35), particles("spray", 0.6)],
                     "birds": {"kind": "gull", "flocks": [{"tx": 16, "ty": 9}], "flyover": True},
                     "bob_gids": [gid("buoy")],
                     "starfall": {"min_s": 22, "max_s": 45}},
    },
    "vigil_grovefall": {
        "ambience": {"particles": [particles("spores", 0.5), particles("glowmotes", 0.4)],
                     "tint": {"color": "#0e2a1c", "alpha": 0.1}},
    },
    "vigil_stormfall": {
        "ambience": {"particles": [particles("snow", 0.6), particles("dust", 0.3)],
                     "mist": {"color": "#c8d4f0", "alpha": 0.12, "speed": 9},
                     "starfall": {"min_s": 22, "max_s": 45}},
    },
    "vigil_sunfall": {
        "ambience": {"particles": [particles("motes", 0.7), particles("embers", 0.2)],
                     "tint": {"color": "#ffcf7a", "alpha": 0.08},
                     "starfall": {"min_s": 22, "max_s": 45}},
    },
    "vigil_murkfall": {
        "ambience": {"particles": [particles("spores", 0.35), particles("glowmotes", 0.3)],
                     "mist": {"color": "#3a4a40", "alpha": 0.26, "speed": 3},
                     "tint": {"color": "#16241c", "alpha": 0.1},
                     "starfall": {"min_s": 22, "max_s": 45}},
    },
}
