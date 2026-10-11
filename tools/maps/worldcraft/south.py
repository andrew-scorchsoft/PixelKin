"""SOUTH world-craft placements (WP2 — the South).

PLACEMENTS: map id -> spec (keys documented in _kit.py). Applied by
`python3 tools/maps/add_world_craft.py --region south`.

The South up to the Chickenpig is the 80-year-old's tutorial: it must not get
one step longer or harder. On those maps (PRE_CHICKENPIG) this module only
adds ambience, ambient kin, CAST swaps (`sprites`: an existing NPC id -> a
regional sheet; ids/dialogue untouched) and PROPS that the runner PROVES are
off-lane (prove_off_lane: no lane/encounter/approach tile, reachability
unchanged, no walk longer). No encounter, trainer, trigger, warp or rate change.

Post-Chickenpig South ground (Gullcry Rock, the Pearlmoor spoke, the
Wanderwood) takes richer, optional set dressing and inspect-only finds.
"""
from __future__ import annotations

from ._kit import add_words, ambient_kin, gid, lit, particles  # noqa: F401

SURF = "amb-surf"
BUOY = [gid("buoy")]
QUIET = particles("dust", 0.35)  # interior motes in the lamp-light


def prop(oid: str, sprite: str, at: tuple[int, int], w: int, h: int, *, overhang: int = 0,
         walk_under: bool = False, solid: bool = True) -> dict:
    o: dict = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    if overhang:
        o["overhang"] = overhang
    if walk_under:
        o["walk_under"] = True
    if not solid:
        o["solid"] = False
    return o


def inspect(tid: str, at: tuple[int, int], ref: str) -> dict:
    """An inspect-only find: interact (facing) with a prop/rock tile reads a line."""
    return {"id": tid, "kind": "dialogue", "at": {"tx": at[0], "ty": at[1]},
            "activation": "interact", "ref": ref}


def same(sprite: str, *ids: str) -> dict[str, str]:
    """Cast swap for every flag-staged placement of one character."""
    return {i: sprite for i in ids}


def interior(*parts: dict) -> dict:
    return {"ambience": {"particles": list(parts) or [QUIET]}}


PLACEMENTS: dict[str, dict] = {
    # ---------------------------------------------------------------- Tinderwick
    # Home: chimney smoke + lamp pools ride the sprite tables; this adds the
    # doorstep glows, fireflies over the field, the beach gulls, and the props a
    # lamp-tending village keeps — a well, a notice board, a woodpile by the
    # lower cottage, a rowing boat, crab pots and a net rack on the sand.
    "tinderwick": {
        "ambience": {
            "particles": [particles("glowmotes", 0.35), particles("leaves", 0.25)],
            "birds": {"kind": "gull", "flocks": [{"tx": 20, "ty": 20}], "flyover": True},
            "light_sources_extra": [
                {"at": {"tx": 5, "ty": 8}, "radius": 11},
                {"at": {"tx": 19, "ty": 8}, "radius": 14},
                {"at": {"tx": 6, "ty": 17}, "radius": 10},
            ],
            "bob_gids": BUOY,
            "sound_bed": SURF,
        },
        "objects": [
            prop("wc_well", "tinderwick_well", (17, 10), 2, 3, overhang=1, walk_under=True),
            prop("wc_notice", "tinderwick_notice_board", (10, 4), 2, 2, overhang=1),
            prop("wc_woodpile", "tinderwick_woodpile", (10, 17), 2, 1),
            prop("wc_rowboat", "pearlmoor_rowboat", (6, 20), 2, 2),
            prop("wc_crabpots", "pearlmoor_crab_pots", (9, 21), 1, 1),
            prop("wc_netrack", "pearlmoor_net_rack", (12, 20), 2, 1),
        ],
        "npcs": [ambient_kin("amb_tallowpup", (24, 20), 10, radius=1),
                 ambient_kin("amb_wickmoth", (5, 12), 16, radius=1)],
        "sprites": {
            **same("lamplighter", "gatewarden_pre", "gatewarden_post"),
            "fair_piper": "market_trader",
            "fair_kid": "village_child",
            "peril_neighbour": "orchard_farmer",
        },
    },
    "tinderwick_house": interior(particles("dust", 0.3), particles("embers", 0.25, {"tx": 1, "ty": 1, "w": 4, "h": 2})),
    "tinderwick_shop": interior(),
    "tinderwick_lumenary": interior(particles("embers", 0.4), QUIET),
    "tinderwick_beacon_i": interior(particles("embers", 0.3), QUIET),
    "tinderwick_beacon_ii": interior(particles("embers", 0.3), QUIET),
    "tinderwick_beacon_top": interior(particles("embers", 0.5), particles("starglint", 0.4)),

    # ----------------------------------------------------------- Duskapple Orchard
    # Falling leaves, and the crater's cold haze: blue-grey motes hang over the
    # scorched ring with a cold pool at its heart (the cinder, not a fire).
    "duskapple_orchard": {
        "ambience": {
            "particles": [particles("leaves", 0.6),
                          particles("motes", 0.8, {"tx": 5, "ty": 3, "w": 6, "h": 4}),
                          particles("glowmotes", 0.25)],
            "light_sources_extra": [{"at": {"tx": 8, "ty": 5}, "radius": 22, "color": "#8fa6d6"}],
        },
        "objects": [prop("wc_apples", "tinderwick_apple_crates", (14, 3), 2, 1)],
        "npcs": [ambient_kin("amb_glimflit", (16, 3), 8, radius=1),
                 ambient_kin("amb_tallowpup", (12, 14), 10, radius=1)],
        "sprites": {
            **same("road_courier", "courier", "courier_errand", "courier_after"),
            **same("orchard_farmer", "wendel", "wendel_dawn"),
        },
    },

    # --------------------------------------------------------- the Lanternway home
    # A safe night road: fireflies, two grazing kin off the lane, and the
    # falling stars tuned more often here — these are the night roads.
    "lanternway_tinderwick": {
        "ambience": {
            "particles": [particles("glowmotes", 0.6)],
            "starfall": {"min_s": 25, "max_s": 55},
        },
        "npcs": [ambient_kin("amb_wickmoth", (4, 3), 16, radius=2),
                 ambient_kin("amb_tallowpup", (19, 9), 10, radius=2)],
        "sprites": {"lane_traveler": "pass_walker"},
    },

    # --------------------------------------------------------- the Crossroads hub
    "vesper_crossroads": {
        "ambience": {
            "particles": [particles("glowmotes", 0.3)],
            "light_sources_extra": [
                {"at": {"tx": 12, "ty": 9}, "radius": 18, "color": "#9fe7ff"},  # the waystone
                {"at": {"tx": 15, "ty": 15}, "radius": 12},                     # inn doorstep
            ],
        },
        "sprites": {
            **same("kite_child", "waystone_kid", "waystone_kid_kite",
                   "kid_trail", "kid_trail_during", "kid_trail_done"),
            "egg_teller": "star_watcher",
        },
    },
    "crossroads_inn": {
        **interior(particles("dust", 0.3), particles("embers", 0.2)),
        "sprites": same("innkeeper", "innkeeper_pre", "innkeeper_ask", "innkeeper_waiting",
                        "innkeeper_hang", "innkeeper_done"),
    },

    # ------------------------------------------------------------ Dimglass Coast
    # THE PILOT (world-craft panel §5) — sea spray on the east shore, the buoys
    # riding the swell, gulls on the dune shelf, one Brinelet grazing off-lane.
    # + the regional cast: the old lamplighter now wears his own sheet.
    "dimglass_coast": {
        "ambience": {
            "particles": [particles("spray", 0.8)],
            "starfall": {"min_s": 40, "max_s": 90},
            "birds": {"kind": "gull", "flocks": [{"tx": 12, "ty": 7}], "flyover": True},
            "bob_gids": BUOY,
            "sound_bed": SURF,
        },
        "npcs": [ambient_kin("amb_brinelet", (12, 5), 26, radius=1)],
        "sprites": {
            **same("lamplighter", "witness", "witness_after"),
            "egg_netmender": "old_salt",
            "egg_walker": "fisher_woman",
        },
    },
    # The tidal flats: the bare sand gets a beached boat, driftwood, a net rack,
    # an old anchor and crab pots — all off the dry lane; the cockler's driftwood
    # fire finally glows.
    "dimglass_coast_ii": {
        "ambience": {
            "particles": [particles("spray", 0.6),
                          particles("embers", 0.5, {"tx": 11, "ty": 28, "w": 3, "h": 2})],
            "birds": {"kind": "gull", "flocks": [{"tx": 12, "ty": 9}], "flyover": True},
            "light_sources_extra": [{"at": {"tx": 12, "ty": 29}, "radius": 15, "color": "#ff9a4a"}],
            "bob_gids": BUOY,
            "sound_bed": SURF,
        },
        "objects": [
            prop("wc_rowboat", "pearlmoor_rowboat", (12, 4), 2, 2),
            prop("wc_driftwood", "pearlmoor_driftwood", (3, 19), 2, 1),
            prop("wc_netrack", "pearlmoor_net_rack", (9, 29), 2, 1),
            prop("wc_anchor", "pearlmoor_anchor", (2, 3), 2, 2, overhang=1),
            prop("wc_crabpots", "pearlmoor_crab_pots", (12, 8), 1, 1),
        ],
        "npcs": [ambient_kin("amb_pebbit", (4, 25), 47, radius=1),
                 ambient_kin("amb_brineroll", (12, 16), 27, radius=1)],
        "sprites": {
            **same("fisher_man", "wayfarer_a", "wayfarer_a_after"),
            **same("road_courier", "wayfarer_b", "wayfarer_b_after"),
            "cockler": "fisher_woman",
        },
    },

    # ------------------------------------------------------------- Pearlmoor Quay
    # The harbour: a fish stall with a lantern under its awning, a string of
    # festival lanterns over the west sand, a net rack, crab pots and crates;
    # lamp pools at the three doors (the moon-lamp's cool one at the hall), gulls,
    # spray and the buoys riding. The fisher no longer borrows Wren's face.
    "pearlmoor_quay": {
        "ambience": {
            "particles": [particles("spray", 0.5)],
            "birds": {"kind": "gull", "flocks": [{"tx": 24, "ty": 16}], "flyover": True},
            "light_sources_extra": [
                {"at": {"tx": 13, "ty": 7}, "radius": 15, "color": "#9fe7ff"},
                {"at": {"tx": 22, "ty": 12}, "radius": 10},
                {"at": {"tx": 5, "ty": 12}, "radius": 10},
            ],
            "bob_gids": BUOY,
            "sound_bed": SURF,
        },
        "objects": [
            prop("wc_fishstall", "pearlmoor_fish_stall", (24, 4), 3, 3, overhang=1, walk_under=True),
            prop("wc_crabpots", "pearlmoor_crab_pots", (21, 15), 1, 1),
            prop("wc_crates", "pearlmoor_fish_crates", (19, 14), 1, 1),
            prop("wc_lanterns", "pearlmoor_lantern_string", (7, 15), 3, 2, overhang=1, walk_under=True,
                 solid=False),  # strung overhead: you walk beneath the lanterns
        ],
        "npcs": [ambient_kin("amb_lumpin", (16, 17), 31, radius=2),
                 ambient_kin("amb_brinelet", (23, 6), 26, radius=1)],
        "sprites": {
            "fisher": "fisher_man",
            "blessing_elder": "old_salt",
            "blessing_kid": "village_child",
            "oldlight_hint_beach": "fisher_woman",
        },
    },
    "pearlmoor_inn": {
        **interior(particles("dust", 0.3), particles("embers", 0.2)),
        "sprites": {"innkeep": "innkeeper",
                    **same("old_salt", "old_fisher_pre", "old_fisher_tale", "old_fisher_wait",
                           "old_fisher_thanks", "old_fisher_after"),
                    "fisher": "fisher_man"},
    },
    "pearlmoor_shop": interior(),
    "pearlmoor_lumenary": interior(particles("motes", 0.5)),
    "pearlmoor_lifting_house": interior(particles("dust", 0.45)),
    "pearlmoor_point": {
        "ambience": {
            "particles": [particles("spray", 0.6)],
            "birds": {"kind": "gull", "flocks": [{"tx": 3, "ty": 9}], "flyover": True},
            "sound_bed": SURF,
        },
    },
    # The Old Light: dust in the window shafts, the same length and difficulty.
    **{f"pearlmoor_oldlight_{n}": interior(particles("dust", 0.6))
       for n in (1, 2, 3, 4, 5, 6, "top")},
    # The breakwater: full spray, gulls on the stones, buoys, the net-hands in oilskins.
    "pearlmoor_breakwater": {
        "ambience": {
            "particles": [particles("spray", 1.0)],
            "birds": {"kind": "gull", "flocks": [{"tx": 4, "ty": 20}], "flyover": True},
            "bob_gids": BUOY,
            "sound_bed": SURF,
        },
        "sprites": {
            **same("fisher_woman", "net_hand_a", "net_hand_a_after"),
            **same("fisher_man", "net_hand_b", "net_hand_b_after"),
        },
    },
    "pearlmoor_allotment": {
        "ambience": {"particles": [particles("leaves", 0.3), particles("glowmotes", 0.3)]},
    },

    # ============================================== post-Chickenpig South ground
    # Gullcry Rock (Tidecall spur): was sand + boulders and nothing to read. Now a
    # wreck's ribs half-sunk in the sand, an old anchor, gull nests, driftwood —
    # the rock the gulls are named for — and a Glostern grazing the far side.
    "gullcry_rock": {
        "ambience": {
            "particles": [particles("spray", 1.0)],
            "mist": {"color": "#cfe0ff", "alpha": 0.07, "speed": 6},
            "birds": {"kind": "gull", "flocks": [{"tx": 6, "ty": 5}, {"tx": 10, "ty": 7}], "flyover": True},
            "bob_gids": BUOY,
            "sound_bed": SURF,
        },
        "objects": [
            prop("wc_wreck", "pearlmoor_wreck_ribs", (4, 3), 3, 2, overhang=1),
            prop("wc_anchor", "pearlmoor_anchor", (9, 3), 2, 2, overhang=1),
            prop("wc_nest_e", "pearlmoor_gull_nest", (11, 6), 1, 1),
            prop("wc_nest_w", "pearlmoor_gull_nest", (3, 7), 1, 1),
            prop("wc_driftwood", "pearlmoor_driftwood", (7, 8), 2, 1),
        ],
        "triggers": [inspect("wc_read_wreck", (5, 4), "npc.gullcry_wreck")],
        "npcs": [ambient_kin("amb_glostern", (10, 5), 29, radius=1)],
    },
    # The Pearlmoor spoke (§4 #8): optional, inspect-only — three wrack finds on
    # Wrackline, the sounding stone in the cave that points at its own hidden nook.
    "wrackline_path": {
        "ambience": {
            "particles": [particles("spray", 0.5)],
            "birds": {"kind": "gull", "flocks": [{"tx": 4, "ty": 3}], "flyover": True},
            "sound_bed": SURF,
        },
        "objects": [
            prop("wc_crabpots", "pearlmoor_crab_pots", (6, 2), 1, 1),
            prop("wc_driftwood", "pearlmoor_driftwood", (2, 22), 2, 1),
            prop("wc_nest", "pearlmoor_gull_nest", (11, 20), 1, 1),
        ],
        "triggers": [
            inspect("wc_wrack_pots", (6, 2), "npc.wrack_find_pots"),
            inspect("wc_wrack_drift", (2, 22), "npc.wrack_find_drift"),
            inspect("wc_wrack_nest", (11, 20), "npc.wrack_find_nest"),
        ],
        "npcs": [ambient_kin("amb_lumpin", (11, 3), 31, radius=2)],
    },
    "sounding_cave": {
        "ambience": {"particles": [particles("motes", 0.5)]},
        "triggers": [inspect("wc_sounding_stone", (7, 15), "npc.sounding_stone")],
        "npcs": [ambient_kin("amb_oreling", (5, 16), 53, radius=1)],
    },
    "lanternfall_road": {
        "ambience": {
            "particles": [particles("glowmotes", 0.4)],
            "starfall": {"min_s": 25, "max_s": 55},
        },
        "npcs": [ambient_kin("amb_oreling", (12, 3), 53, radius=2)],
        "sprites": same("lamplighter", "lanternfall_warden", "lanternfall_warden_after"),
    },
    # The Wanderwood (S5): spores and fireflies under the canopy; the far wood
    # gets a wayfarers' board by the waystone path and Mags' woodpile.
    "pearlmoor_wanderwood": {
        "ambience": {
            "particles": [particles("spores", 0.5), particles("glowmotes", 0.4)],
            "mist": {"color": "#a8c8b0", "alpha": 0.06, "speed": 4},
        },
        "npcs": [ambient_kin("amb_sporeling", (20, 13), 56, radius=1)],
        # Review 2026-10: the wood read sparse (1.34 props/screen). Six crown trees on
        # ground proven off every lane/approach (prove_off_lane); variants = vary_trees' pick.
        "objects": [
            {"id": "wander_tree_1", "sprite": "tinderwick_tree", "at": {"tx": 11, "ty": 5}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
            {"id": "wander_tree_2", "sprite": "tinderwick_tree_b", "at": {"tx": 24, "ty": 2}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
            {"id": "wander_tree_3", "sprite": "tinderwick_tree_c", "at": {"tx": 2, "ty": 12}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
            {"id": "wander_tree_4", "sprite": "tinderwick_tree", "at": {"tx": 16, "ty": 8}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
            {"id": "wander_tree_5", "sprite": "tinderwick_tree", "at": {"tx": 25, "ty": 12}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
            {"id": "wander_tree_6", "sprite": "tinderwick_tree", "at": {"tx": 17, "ty": 17}, "w": 3, "h": 4, "overhang": 3, "walk_under": True},
        ],
    },
    "pearlmoor_wanderwood_far": {
        "ambience": {
            "particles": [particles("spores", 0.5), particles("glowmotes", 0.4)],
            "mist": {"color": "#a8c8b0", "alpha": 0.06, "speed": 4},
        },
        "objects": [
            prop("wc_board", "tinderwick_notice_board", (22, 2), 2, 2, overhang=1),
            prop("wc_woodpile", "tinderwick_woodpile", (13, 18), 2, 1),
        ],
        "triggers": [inspect("wc_read_board", (22, 3), "npc.wanderwood_board")],
        "npcs": [ambient_kin("amb_snoozlet", (17, 4), 105, radius=1)],
    },
}


# ------------------------------------------------------------- AFTER-GLEAM
# The South answers its Gleams (src/game/content/regions/south.ts). Words only:
# `lit` twins share their original's tile, sheet and body; `talk` re-points keep
# the id (shops, staged chains, cutscene actors). Allowed on pre-Chickenpig maps.
EMBER, TIDE = "gleam:ember", "gleam:tide"
add_words(PLACEMENTS, {
    "tinderwick": {"after": [lit("gatewarden_post", EMBER, "npc.gatewarden_after_lit",
                                 implies="flag:has_starter")]},
    "tinderwick_shop": {"talk": {"shopkeeper": "script.shop_tinderwick_staged"}},
    "vesper_crossroads": {"talk": {"waykeeper": "script.waykeeper_staged"}},
    "crossroads_inn": {"talk": {"innkeeper_pre": "script.inn_rest_crossroads_early"}},
    # witness_after shares its tile with the pre-wick witness: re-point, don't twin
    "dimglass_coast": {"talk": {"witness_after": "script.dimglass_witness_staged",
                                "wren_after": "script.wren_dimglass_staged"}},
    "dimglass_coast_ii": {"talk": {"wayfarer_b_after": "script.flats_wayfarer_b_staged",
                                   "sky_watcher_after": "script.flats_sky_watcher_staged"}},
    "pearlmoor_quay": {"after": [lit("fisher", TIDE, "npc.pearlmoor_fisher_lit")]},
    "pearlmoor_inn": {"after": [lit("fisher", TIDE, "npc.pearlmoor_fisher_inn_lit"),
                                lit("innkeep", TIDE, "script.pearlmoor_inn_rest_lit")]},
    "pearlmoor_shop": {"talk": {"chandler": "script.shop_pearlmoor_staged"}},
    "pearlmoor_lifting_house": {"after": [lit("andrew", TIDE, "npc.booji_andrew_lit")]},
})
