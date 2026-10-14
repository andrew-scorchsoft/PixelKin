"""OUTER world-craft placements: the Farlamp Isles' UNDERTIDE and the Drowned Lamp
(10-the-farlamp-isles.md Part I, lane C2). Applied by
`python3 tools/maps/add_world_craft.py --region outer`.

The caves' structure (the surge dressing, the tide-lamps, the islets, the niche)
lives in their BUILDERS (tools/maps/build_undertide_*.py, build_farlamp_drowned.py);
this module carries what world-craft owns: each map's ambience (with its
story-state swap once `flag:isles_dawn` is held — the isles' own morning reaches
even down here) and the ambient kin that graze the galleries (each from the map's
own table: Hermiwick and Fogwisp by night; at the isles' dawn the hermit-crabs
give way to their kindled Beaconclaw, the woken forms of the same water).
"""
from __future__ import annotations

from ._kit import ambient_kin, particles

DAWN = "flag:isles_dawn"

# The Undertide by night: a dark sea-cave, spray off the surge, a few glowmotes.
# After the dawn: the tide-lamps lit, a warmer wash, more light in the air.
def _cave(tint: str, alpha: float, spray: float = 0.5, motes: float = 0.3) -> dict:
    return {
        "particles": [particles("spray", spray), particles("glowmotes", motes)],
        "tint": {"color": tint, "alpha": alpha},
        "sound_bed": "amb-surf",
        "when": [{"flag": DAWN, "ambience": {
            "particles": [particles("spray", spray), particles("glowmotes", motes + 0.4)],
            "tint": {"color": "#3a2a10", "alpha": 0.06},
            "sound_bed": "amb-surf",
        }}],
    }


def _hermit(nid: str, at: tuple[int, int], radius: int = 2) -> list[dict]:
    """A Hermiwick by night and, at the isles' dawn, a Beaconclaw in its place."""
    return [ambient_kin(nid, at, 174, radius=radius, hidden=DAWN),
            ambient_kin(nid + "_dawn", at, 175, radius=radius, requires=DAWN)]


PLACEMENTS: dict[str, dict] = {
    "undertide_i": {
        "ambience": _cave("#0a2a3a", 0.12, spray=0.6),
        "npcs": [
            *_hermit("amb_ut1_hermit_w", (6, 10)),
            ambient_kin("amb_ut1_fogwisp_ne", (27, 6), 176, radius=2),
            *_hermit("amb_ut1_hermit_s", (12, 25)),
        ],
    },
    "undertide_ii": {
        "ambience": _cave("#0a3030", 0.12, spray=0.4, motes=0.4),
        "npcs": [
            *_hermit("amb_ut2_hermit_walk", (3, 24)),
            ambient_kin("amb_ut2_fogwisp_e", (27, 5), 176, radius=2),
            ambient_kin("amb_ut2_fogwisp_h", (13, 13), 176, radius=1),
        ],
    },
    "undertide_iii": {
        "ambience": _cave("#0a2238", 0.14),
        "npcs": [
            *_hermit("amb_ut3_hermit_eg", (24, 13)),
            ambient_kin("amb_ut3_fogwisp_nw", (4, 4), 176, radius=2),
            ambient_kin("amb_ut3_fogwisp_dg", (13, 4), 176, radius=1),
        ],
    },
    "undertide_iv": {
        "ambience": _cave("#081c30", 0.18, spray=0.4, motes=0.5),
        "npcs": [
            *_hermit("amb_ut4_hermit_t3", (19, 14)),
            ambient_kin("amb_ut4_fogwisp_n1", (3, 20), 176, radius=1),
            *_hermit("amb_ut4_hermit_t5", (12, 28), radius=3),
        ],
    },
    # The Drowned Lamp: cold and dim until the relight; then the lamp-room warms
    # (its music swaps through maps.ts music_when) and a Beaconclaw comes up out of
    # the moat to sit in the light.
    "farlamp_drowned": {
        "ambience": {
            "particles": [particles("glowmotes", 0.3)],
            "tint": {"color": "#04101e", "alpha": 0.4},
            "sound_bed": "amb-surf",
            "when": [{"flag": DAWN, "ambience": {
                "particles": [particles("glowmotes", 0.8), particles("dust", 0.4)],
                "tint": {"color": "#ffd890", "alpha": 0.08},
                "light_sources_extra": [{"at": {"tx": 10, "ty": 8}, "radius": 72, "color": "#ffd890"}],
                "sound_bed": "amb-surf",
            }}],
        },
        "npcs": [
            ambient_kin("amb_fd_beaconclaw", (5, 12), 175, radius=1, requires=DAWN),
        ],
    },
}
