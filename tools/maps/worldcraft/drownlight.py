"""DROWNLIGHT world-craft (walkthrough/11-the-hollowing-country.md Part B, lane N2):
the ambience of the tower above drownlight_beacon. Applied by
`python3 tools/maps/add_world_craft.py --region drownlight`.

The floors' structure (the light-wells, the glare, the cranks, the caches) lives in
their BUILDER (tools/maps/build_drownlight_tower.py). This module carries only what
world-craft owns: each floor's air. Dust hangs in the leaked light; each floor is a
shade colder than the one below; the lantern room warms once the lamp is relit.
(The foot's own `when` — the buoys and the beam waking — rides west.py's
drownlight_beacon row, the coldfog block it already owns.)
"""
from __future__ import annotations

from ._kit import particles

RELIT = "flag:drownlight_relit"
WARM = {"particles": [particles("dust", 0.7), particles("glowmotes", 0.4)],
        "tint": {"color": "#ffcf7a", "alpha": 0.08}}

PLACEMENTS: dict[str, dict] = {
    "drownlight_f1": {"ambience": {
        "particles": [particles("dust", 0.45)],
        "tint": {"color": "#55606e", "alpha": 0.12},
        "when": [{"flag": RELIT, "ambience": WARM}],
    }},
    "drownlight_f2": {"ambience": {
        "particles": [particles("dust", 0.4)],
        "tint": {"color": "#3c4a62", "alpha": 0.16},
        "when": [{"flag": RELIT, "ambience": WARM}],
    }},
    "drownlight_lantern": {"ambience": {
        "particles": [particles("dust", 0.3)],
        "tint": {"color": "#2a3348", "alpha": 0.18},
        "light_sources_extra": [{"at": {"tx": 7, "ty": 4}, "radius": 10, "color": "#c98a48"}],
        "when": [{"flag": RELIT, "ambience": {
            **WARM,
            "light_sources_extra": [{"at": {"tx": 7, "ty": 4}, "radius": 40, "color": "#ffe2a0"}],
        }}],
    }},
}
