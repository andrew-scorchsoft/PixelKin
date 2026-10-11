"""CENTRAL world-craft placements (owned by this region's package).

PLACEMENTS: map id -> spec (keys documented in _kit.py). Applied by
`python3 tools/maps/add_world_craft.py --region central`.
"""
from __future__ import annotations

from ._kit import ambient_kin, gid, particles  # noqa: F401

PLACEMENTS: dict[str, dict] = {}
