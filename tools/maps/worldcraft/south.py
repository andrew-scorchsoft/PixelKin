"""SOUTH world-craft placements (owned by WP2 — the South, ambient only).

PLACEMENTS: map id -> spec (keys documented in _kit.py). Applied by
`python3 tools/maps/add_world_craft.py --region south`.

The South is the pre-Chickenpig path: ambience blocks + ambient kin ONLY (the
runner enforces it). No encounter, trainer, trigger, warp or walkable change.
"""
from __future__ import annotations

from ._kit import ambient_kin, gid, particles  # noqa: F401

PLACEMENTS: dict[str, dict] = {
    # THE PILOT (world-craft panel §5). The first route + first grass: sea spray
    # on the east shore, the buoys riding the swell, gulls on the dune shelf,
    # the falling-star streak (its story debut is script.dusk_begins), lamp pools
    # on its 4 lamp posts (automatic: LIGHT_SOURCES keys tinderwick_lamp_post),
    # and one Brinelet (#26, the coast's commonest kin) grazing the seaward
    # shelf east of the lane — off the walking line, leashed to 1 tile.
    "dimglass_coast": {
        "ambience": {
            "particles": [particles("spray", 0.8)],
            "starfall": {"min_s": 40, "max_s": 90},
            "birds": {"kind": "gull", "flocks": [{"tx": 12, "ty": 7}], "flyover": True},
            "bob_gids": [gid("buoy")],
            "sound_bed": "amb-surf",
        },
        "npcs": [ambient_kin("amb_brinelet", (12, 5), 26, radius=1)],
    },
}
