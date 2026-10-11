"""Per-region world-craft placements (one module per region package — WP2..WP6).

Each module defines `PLACEMENTS: dict[map_id, spec]`, applied idempotently to the
SHIPPED map JSONs by `tools/maps/add_world_craft.py`. See `_kit.py` for helpers
and the spec keys, and docs/art-style.md §12b for the ambience block itself.
"""
