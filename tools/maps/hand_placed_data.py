"""
hand_placed_data — the data add_hand_placed.py applies (see its docstring).

One entry per map id. Keys, in the order the runner applies them:
  "patch":  {list: {id: {field: value}}}  field retunes on BUILDER-emitted entries
            (night zone tables/rates synced after the build; dawn swap flags)
  npcs / objects / triggers / warps / encounters: whole hand-placed items
            (`_before: <id>` = insert ahead of that entry, so list order matches
            the shipped order)
  "day":    {night zone id: post-dawn table} — the R4 day-form twins
  "signs":  [(id, (x, y), "sign.ref")] — trigger `sign_<id>` + the sign deco tile

Extracted 2026-10 from the shipped maps (the shipped JSON is the truth), so a
rebuild reproduces them; from now on EDIT HERE (or in the owning builder), never
in a shipped map JSON — then run the runners and `tools/maps/check_rebuild.py`.
Zone tables are mirrored in tools/balance/build_species.py EXTRA_ENCOUNTERS.
"""


def T(*rows: tuple[int, int, int, int]) -> list[dict]:
    """An encounter table from (kin_id, weight, min_level, max_level) rows."""
    return [{"kin_id": k, "weight": w, "min_level": lo, "max_level": hi} for (k, w, lo, hi) in rows]


PLACEMENTS: dict[str, dict] = {
    "aurora_hollow": {
        "day": {
            "bed_a": T((86, 34, 57, 63), (78, 24, 57, 63), (87, 27, 58, 65), (73, 6, 62, 65), (84, 9, 57, 62)),
            "bed_b": T((86, 34, 57, 63), (78, 24, 57, 63), (87, 27, 58, 65), (73, 6, 62, 65), (84, 9, 57, 62)),
        },
    },
    "cinderhead_deep": {
        "patch": {
            "encounters": {
                "gallery_a": {"table": T((49, 45, 24, 26), (45, 35, 24, 26), (35, 20, 24, 26), (53, 25, 24, 26), (41, 15, 24, 26))},
                "far_side": {"table": T((49, 40, 25, 26), (45, 35, 25, 26), (35, 25, 25, 26), (53, 25, 25, 26), (41, 15, 25, 26))},
            },
        },
    },
    "cinderhead_deep_b1f": {
        "patch": {
            "encounters": {
                "b1f_gallery": {"table": T((49, 40, 25, 27), (45, 35, 25, 27), (35, 25, 25, 27), (44, 20, 25, 27), (69, 10, 25, 27))},
            },
        },
    },
    "cinderhead_deep_b2f": {
        "patch": {
            "encounters": {
                "b2f_heart": {"table": T((49, 40, 26, 27), (45, 35, 26, 27), (35, 25, 26, 27), (53, 20, 26, 27), (69, 12, 26, 27), (42, 8, 26, 27))},
            },
        },
        "npcs": [
            # a found cache
            {"id": "cache_cinderhead_alcove", "at": {"tx": 19, "ty": 11}, "facing": "down", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_cinderhead_alcove", "hidden_when_flag": "flag:picked_cinderhead_alcove", "requires_flag": "flag:lamplight_starlight"},
        ],
    },
    "cinderhead_mine": {
        "patch": {
            "encounters": {
                "gallery": {"table": T((49, 45, 22, 24), (45, 35, 22, 24), (35, 20, 22, 24), (41, 30, 22, 24), (44, 15, 22, 24))},
            },
        },
        "npcs": [
            # P1 postgame: a letter recipient (script.post_letter_*)
            {"id": "letter_otho", "at": {"tx": 14, "ty": 12}, "facing": "down", "sprite": "npc_lampwarden", "movement": "static", "dialogue_ref": "script.post_letter_cinderhead", "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_cinderhead"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 3, "ty": 13}, "facing": "left", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
        ],
    },
    "coldfog_marches_i": {
        "patch": {
            "objects": {
                "dead_lantern_0": {"hidden_when_flag": "flag:dawn"},
                "dead_lantern_1": {"hidden_when_flag": "flag:dawn"},
                "dead_lantern_2": {"hidden_when_flag": "flag:dawn"},
                "dead_lantern_3": {"hidden_when_flag": "flag:dawn"},
            },
        },
        "day": {
            "crossing_a": T((140, 22, 58, 65), (133, 24, 55, 62), (134, 20, 56, 63), (139, 14, 56, 63), (136, 12, 55, 61), (137, 8, 56, 62)),
            "bed_a": T((140, 22, 58, 65), (133, 24, 55, 62), (134, 20, 56, 63), (139, 14, 56, 63), (136, 12, 55, 61), (137, 8, 56, 62)),
            "bed_b": T((140, 22, 58, 65), (133, 24, 55, 62), (134, 20, 56, 63), (139, 14, 56, 63), (136, 12, 55, 61), (137, 8, 56, 62)),
            "bed_c": T((140, 22, 58, 65), (133, 24, 55, 62), (134, 20, 56, 63), (139, 14, 56, 63), (136, 12, 55, 61), (137, 8, 56, 62)),
            "gold_a": T((140, 50, 59, 65), (133, 30, 56, 62), (134, 20, 57, 63)),
        },
        "objects": [
            # dawn: the relit lanterns (swap pair with dead_lantern_*)
            {"id": "relit_lantern_0", "sprite": "saltreach_reed_lantern_lit", "at": {"tx": 7, "ty": 20}, "w": 1, "h": 2, "overhang": 1, "walk_under": True, "requires_flag": "flag:dawn"},
            {"id": "relit_lantern_1", "sprite": "saltreach_reed_lantern_lit", "at": {"tx": 10, "ty": 16}, "w": 1, "h": 2, "overhang": 1, "walk_under": True, "requires_flag": "flag:dawn"},
            {"id": "relit_lantern_2", "sprite": "saltreach_reed_lantern_lit", "at": {"tx": 7, "ty": 10}, "w": 1, "h": 2, "overhang": 1, "walk_under": True, "requires_flag": "flag:dawn"},
            {"id": "relit_lantern_3", "sprite": "saltreach_reed_lantern_lit", "at": {"tx": 10, "ty": 5}, "w": 1, "h": 2, "overhang": 1, "walk_under": True, "requires_flag": "flag:dawn"},
        ],
    },
    "coldfog_marches_ii": {
        "patch": {
            "objects": {
                "dead_lantern_0": {"hidden_when_flag": "flag:dawn"},
                "dead_lantern_1": {"hidden_when_flag": "flag:dawn"},
                "dead_lantern_2": {"hidden_when_flag": "flag:dawn"},
                "dead_lantern_3": {"hidden_when_flag": "flag:dawn"},
            },
        },
        "day": {
            "crossing_a": T((140, 20, 60, 65), (139, 22, 57, 64), (134, 20, 57, 64), (133, 12, 56, 63), (137, 10, 57, 63), (142, 8, 58, 64), (141, 8, 57, 63)),
            "bed_a": T((140, 20, 60, 65), (139, 22, 57, 64), (134, 20, 57, 64), (133, 12, 56, 63), (137, 10, 57, 63), (142, 8, 58, 64), (141, 8, 57, 63)),
            "bed_b": T((140, 20, 60, 65), (139, 22, 57, 64), (134, 20, 57, 64), (133, 12, 56, 63), (137, 10, 57, 63), (142, 8, 58, 64), (141, 8, 57, 63)),
            "bed_c": T((140, 20, 60, 65), (139, 22, 57, 64), (134, 20, 57, 64), (133, 12, 56, 63), (137, 10, 57, 63), (142, 8, 58, 64), (141, 8, 57, 63)),
            "bed_d": T((140, 20, 60, 65), (139, 22, 57, 64), (134, 20, 57, 64), (133, 12, 56, 63), (137, 10, 57, 63), (142, 8, 58, 64), (141, 8, 57, 63)),
        },
        "objects": [
            # dawn: the relit lanterns (swap pair with dead_lantern_*)
            {"id": "relit_lantern_0", "sprite": "saltreach_reed_lantern_lit", "at": {"tx": 22, "ty": 19}, "w": 1, "h": 2, "overhang": 1, "walk_under": True, "requires_flag": "flag:dawn"},
            {"id": "relit_lantern_1", "sprite": "saltreach_reed_lantern_lit", "at": {"tx": 18, "ty": 9}, "w": 1, "h": 2, "overhang": 1, "walk_under": True, "requires_flag": "flag:dawn"},
            {"id": "relit_lantern_2", "sprite": "saltreach_reed_lantern_lit", "at": {"tx": 4, "ty": 11}, "w": 1, "h": 2, "overhang": 1, "walk_under": True, "requires_flag": "flag:dawn"},
            {"id": "relit_lantern_3", "sprite": "saltreach_reed_lantern_lit", "at": {"tx": 21, "ty": 12}, "w": 1, "h": 2, "overhang": 1, "walk_under": True, "requires_flag": "flag:dawn"},
        ],
    },
    "dawnstead": {
        "encounters": [
            # the day-form capstone: Helixia (post-crown)
            {"id": "sunlit_verge_helixia", "terrain": "tall_grass", "rect": {"tx": 20, "ty": 13, "w": 6, "h": 6}, "encounter_rate": 0.01, "requires_flag": "flag:starfall_crown", "table": T((131, 1, 60, 62)), "_before": "sunlit_verge"},
        ],
        "npcs": [
            # the Starfall Vigils (postgame)
            {"id": "starfall_witness", "at": {"tx": 13, "ty": 11}, "facing": "down", "sprite": "star_watcher", "movement": "look_around", "dialogue_ref": "npc.starfall_witness", "requires_flag": "flag:dawn", "hidden_when_flag": "flag:starfall_begun"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 12, "ty": 23}, "facing": "down", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
        ],
    },
    "dimglass_coast": {
        "patch": {
            "encounters": {
                "grass_a": {"table": T((26, 55, 3, 5), (31, 30, 3, 5), (8, 15, 3, 5), (47, 8, 3, 5))},
                "grass_b": {"table": T((26, 55, 3, 5), (31, 30, 4, 5), (8, 15, 3, 5), (47, 8, 3, 5))},
                "grass_c": {"table": T((26, 55, 4, 5), (31, 30, 4, 5), (8, 15, 4, 5), (47, 8, 4, 5))},
                "grass_d": {"table": T((26, 55, 4, 5), (31, 30, 4, 5), (8, 15, 4, 5), (47, 8, 4, 5))},
                "bank_hollow": {"table": T((26, 40, 5, 6), (31, 35, 5, 6), (8, 25, 5, 6), (47, 8, 5, 6))},
                "crossing_a": {"encounter_rate": 0.08, "table": T((26, 55, 3, 5), (31, 30, 3, 5), (8, 15, 3, 5), (47, 8, 3, 5))},
                "crossing_b": {"encounter_rate": 0.08, "table": T((26, 55, 4, 5), (31, 30, 4, 5), (8, 15, 4, 5), (47, 8, 4, 5))},
                "tide_shallows": {"table": T((2, 100, 4, 6), (20, 30, 4, 6))},
            },
        },
        "day": {
            "grass_a": T((26, 45, 55, 60), (31, 30, 55, 62), (8, 25, 56, 62)),
            "grass_b": T((26, 45, 55, 60), (31, 30, 55, 62), (8, 25, 56, 62)),
            "grass_c": T((26, 45, 55, 60), (31, 30, 55, 62), (8, 25, 56, 62)),
            "grass_d": T((26, 45, 55, 60), (31, 30, 55, 62), (8, 25, 56, 62)),
            "bank_hollow": T((26, 45, 55, 60), (31, 30, 55, 62), (8, 25, 56, 62)),
            "crossing_a": T((26, 45, 55, 60), (31, 30, 55, 62), (8, 25, 56, 62)),
            "crossing_b": T((26, 45, 55, 60), (31, 30, 55, 62), (8, 25, 56, 62)),
            "tide_shallows": T((2, 70, 55, 62), (24, 30, 56, 63), (20, 20, 55, 62)),
        },
        "npcs": [
            # the easter-egg trail (S4)
            {"id": "egg_walker", "at": {"tx": 11, "ty": 3}, "facing": "down", "sprite": "fisher_woman", "movement": "look_around", "dialogue_ref": "npc.egg_hint_coast"},
            {"id": "egg_netmender", "at": {"tx": 4, "ty": 30}, "facing": "right", "sprite": "old_salt", "movement": "static", "dialogue_ref": "npc.egg_hint_flats"},
            # a found cache
            {"id": "cache_purse", "at": {"tx": 2, "ty": 2}, "facing": "down", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_dimglass_purse", "hidden_when_flag": "flag:picked_dimglass_purse"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 5, "ty": 31}, "facing": "down", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
            # the Worry Club (R9)
            {"id": "worry_pim", "at": {"tx": 12, "ty": 15}, "facing": "left", "sprite": "npc_man", "movement": "look_around", "dialogue_ref": "script.worry_pim"},
            # R9: Wink's Tin Rower auction
            {"id": "wink", "at": {"tx": 12, "ty": 30}, "facing": "left", "sprite": "npc_old_man", "movement": "look_around", "dialogue_ref": "script.wink_trade", "requires_flag": "flag:has_starter", "hidden_when_flag": "flag:has_tin_rower"},
        ],
        "signs": [
            ("wink", (12, 29), "sign.wink_auction"),
        ],
    },
    "dimglass_coast_ii": {
        "patch": {
            "encounters": {
                "dune_a": {"encounter_rate": 0.09, "table": T((26, 50, 8, 9), (31, 30, 8, 9), (27, 20, 9, 9), (47, 25, 8, 9))},
                "dune_b": {"encounter_rate": 0.09, "table": T((26, 50, 8, 9), (31, 30, 8, 9), (27, 20, 9, 9), (47, 25, 8, 9))},
                "dune_c": {"encounter_rate": 0.09, "table": T((26, 45, 9, 9), (31, 30, 9, 9), (27, 25, 9, 10), (47, 25, 9, 10))},
                "dune_crossing": {"encounter_rate": 0.09, "table": T((26, 45, 9, 10), (31, 30, 9, 10), (27, 25, 9, 10), (47, 25, 9, 10))},
                "gullcry_shallows": {"table": T((2, 100, 9, 11), (23, 25, 9, 11))},
            },
        },
        "day": {
            "dune_a": T((26, 40, 56, 61), (31, 30, 56, 63), (27, 30, 57, 63)),
            "dune_b": T((26, 40, 56, 61), (31, 30, 56, 63), (27, 30, 57, 63)),
            "dune_c": T((26, 40, 56, 61), (31, 30, 56, 63), (27, 30, 57, 63)),
            "dune_crossing": T((26, 40, 56, 61), (31, 30, 56, 63), (27, 30, 57, 63)),
            "gullcry_shallows": T((2, 70, 56, 63), (24, 30, 57, 64), (23, 20, 56, 63)),
        },
        "npcs": [
            # a found cache
            {"id": "cache_purse", "at": {"tx": 13, "ty": 25}, "facing": "down", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_flats_purse", "hidden_when_flag": "flag:picked_flats_purse"},
            # the flats' roadside rest (2026-10 easing)
            {"id": "cockler", "at": {"tx": 11, "ty": 28}, "facing": "down", "sprite": "fisher_woman", "movement": "static", "dialogue_ref": "script.flats_rest"},
            # the Worry Club (R9)
            {"id": "worry_gilly", "at": {"tx": 13, "ty": 28}, "facing": "left", "sprite": "npc_old_woman", "movement": "look_around", "dialogue_ref": "script.worry_gilly"},
        ],
    },
    "galehigh_terraces": {
        "day": {
            "verge_a": T((88, 30, 55, 60), (97, 25, 55, 61), (91, 30, 56, 62), (100, 15, 55, 61)),
            "verge_b": T((88, 30, 55, 60), (97, 25, 55, 61), (91, 30, 56, 62), (100, 15, 55, 61)),
            "crossing_a": T((88, 30, 55, 60), (97, 25, 55, 61), (91, 30, 56, 62), (100, 15, 55, 61)),
            "crossing_b": T((88, 30, 55, 60), (97, 25, 55, 61), (91, 30, 56, 62), (100, 15, 55, 61)),
        },
        "npcs": [
            # P1 postgame: a letter recipient (script.post_letter_*)
            {"id": "letter_mira", "at": {"tx": 14, "ty": 16}, "facing": "down", "sprite": "mira", "movement": "static", "dialogue_ref": "script.post_letter_galehigh", "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_galehigh"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 3, "ty": 14}, "facing": "left", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
        ],
    },
    "glowmoss_deep": {
        "npcs": [
            # a found cache
            {"id": "cache_glowmoss_sidecell", "at": {"tx": 12, "ty": 23}, "facing": "down", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_glowmoss_sidecell", "hidden_when_flag": "flag:picked_glowmoss_sidecell", "requires_flag": "flag:lamplight_brightlight"},
        ],
    },
    "gullcry_rock": {
        "patch": {
            "encounters": {
                "gullcry_surf": {"table": T((29, 40, 11, 13), (27, 30, 11, 13), (31, 30, 10, 12), (23, 20, 11, 13))},
            },
        },
        "day": {
            "gullcry_surf": T((29, 50, 58, 65), (27, 25, 58, 64), (31, 25, 57, 64), (23, 15, 58, 64)),
        },
    },
    "helia_vault": {
        "patch": {
            "encounters": {
                "shaft_a": {"table": T((117, 26, 47, 48), (118, 20, 47, 49), (115, 18, 47, 49), (104, 16, 48, 49), (116, 12, 48, 49), (121, 12, 48, 49))},
            },
        },
    },
    "duskapple_orchard": {
        # The kitchens (content/regions/kitchens.ts): Percy's moka brew-stand by the
        # courier's cart — a drawn prop (tools/maps/draw_moka_stall.py), optional colour.
        "objects": [
            {"id": "moka_stall", "sprite": "kitchens_moka_stall", "at": {"tx": 12, "ty": 10}, "w": 2, "h": 2, "overhang": 1},
        ],
        "npcs": [
            {"id": "percy", "at": {"tx": 14, "ty": 11}, "facing": "left", "sprite": "innkeeper", "movement": "static", "dialogue_ref": "script.moka_percy"},
        ],
    },
    "lowleaf_hollow": {
        "patch": {
            "encounters": {
                "fringe_a": {"table": T((56, 40, 18, 20), (67, 25, 18, 20), (38, 20, 18, 20), (62, 15, 18, 20), (65, 15, 18, 20))},
            },
        },
        "day": {
            "fringe_a": T((56, 28, 56, 62), (67, 28, 56, 63), (38, 22, 56, 63), (62, 14, 56, 62), (66, 8, 58, 65), (65, 12, 56, 63)),
        },
        "objects": [
            # The kitchens: Marisol's stall (chile strings, the comal) + her pozole pot
            {"id": "cantina_stall", "sprite": "kitchens_cantina_stall", "at": {"tx": 6, "ty": 26}, "w": 3, "h": 3, "overhang": 1},
            {"id": "pozole_pot", "sprite": "kitchens_pozole_pot", "at": {"tx": 10, "ty": 26}, "w": 2, "h": 2, "overhang": 1},
        ],
        "npcs": [
            # The kitchens: Marisol's kitchen (script.cantina_marisol)
            {"id": "marisol", "at": {"tx": 9, "ty": 27}, "facing": "down", "sprite": "market_trader", "movement": "static", "dialogue_ref": "script.cantina_marisol"},
            # P1 postgame: a letter recipient (script.post_letter_*)
            {"id": "letter_sable", "at": {"tx": 14, "ty": 15}, "facing": "down", "sprite": "npc_lampwarden", "movement": "static", "dialogue_ref": "script.post_letter_lowleaf", "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_lowleaf"},
            # E4: the hook to Georgina's side quest
            {"id": "georgina_hook", "at": {"tx": 12, "ty": 16}, "facing": "down", "sprite": "npc_old_woman", "movement": "look_around", "dialogue_ref": "script.georgina_hook", "requires_flag": "gleam:verdant", "hidden_when_flag": "flag:q_east_georgina"},
            # a found cache
            {"id": "cache_purse", "at": {"tx": 25, "ty": 27}, "facing": "down", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_lowleaf_purse", "hidden_when_flag": "flag:picked_lowleaf_purse"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 14, "ty": 28}, "facing": "down", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
        ],
    },
    "nightreach_observatory": {
        "npcs": [
            # P1 postgame: a letter recipient (script.post_letter_*)
            {"id": "letter_nessa", "at": {"tx": 24, "ty": 9}, "facing": "down", "sprite": "nessa", "movement": "static", "dialogue_ref": "script.post_letter_nightreach", "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_nightreach"},
            # Oriel's terrace set (postgame)
            {"id": "oriel_begin", "at": {"tx": 19, "ty": 4}, "facing": "up", "sprite": "npc_woman", "movement": "static", "dialogue_ref": "script.starfall_begins", "requires_flag": "flag:dawn", "hidden_when_flag": "flag:starfall_begun"},
            {"id": "oriel_read_1", "at": {"tx": 19, "ty": 4}, "facing": "up", "sprite": "npc_woman", "movement": "static", "dialogue_ref": "npc.oriel_read_1", "requires_flag": "flag:vigil_reading_1", "hidden_when_flag": "flag:vigil_reading_2"},
            {"id": "oriel_read_2", "at": {"tx": 19, "ty": 4}, "facing": "up", "sprite": "npc_woman", "movement": "static", "dialogue_ref": "npc.oriel_read_2", "requires_flag": "flag:vigil_reading_2", "hidden_when_flag": "flag:vigil_reading_3"},
            {"id": "oriel_read_3", "at": {"tx": 19, "ty": 4}, "facing": "up", "sprite": "npc_woman", "movement": "static", "dialogue_ref": "npc.oriel_read_3", "requires_flag": "flag:vigil_reading_3", "hidden_when_flag": "flag:vigil_reading_4"},
            {"id": "oriel_read_4", "at": {"tx": 19, "ty": 4}, "facing": "up", "sprite": "npc_woman", "movement": "static", "dialogue_ref": "npc.oriel_read_4", "requires_flag": "flag:vigil_reading_4", "hidden_when_flag": "flag:vigil_reading_5"},
            {"id": "oriel_read_5", "at": {"tx": 19, "ty": 4}, "facing": "up", "sprite": "npc_woman", "movement": "static", "dialogue_ref": "npc.oriel_read_5", "requires_flag": "flag:vigil_reading_5", "hidden_when_flag": "flag:vigil_5_kept"},
            {"id": "oriel_carry", "at": {"tx": 19, "ty": 4}, "facing": "up", "sprite": "npc_woman", "movement": "static", "dialogue_ref": "npc.oriel_carry", "requires_flag": "flag:vigil_5_kept", "hidden_when_flag": "flag:starfall_crown"},
            {"id": "oriel_epilogue", "at": {"tx": 19, "ty": 4}, "facing": "up", "sprite": "npc_woman", "movement": "static", "dialogue_ref": "npc.oriel_epilogue", "requires_flag": "flag:starfall_crown"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 15, "ty": 26}, "facing": "down", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
        ],
    },
    "pale_vault_glacier": {
        "day": {
            "hollow_a": T((72, 16, 57, 63), (81, 14, 57, 63), (71, 12, 56, 62), (86, 20, 57, 63), (80, 12, 56, 62), (87, 16, 59, 65)),
            "hollow_b": T((72, 16, 57, 63), (81, 14, 57, 63), (71, 12, 56, 62), (86, 20, 57, 63), (80, 12, 56, 62), (87, 16, 59, 65)),
            "crossing_a": T((72, 16, 57, 63), (81, 14, 57, 63), (71, 12, 56, 62), (86, 20, 57, 63), (80, 12, 56, 62), (87, 16, 59, 65)),
            "deepice": T((85, 25, 58, 64), (87, 45, 59, 65), (72, 30, 58, 64)),
        },
        "npcs": [
            # P1 postgame: a letter recipient (script.post_letter_*)
            {"id": "letter_ysolde", "at": {"tx": 17, "ty": 10}, "facing": "down", "sprite": "ysolde", "movement": "static", "dialogue_ref": "script.post_letter_pale_vault", "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_pale_vault"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 14, "ty": 26}, "facing": "down", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
            # 09 §C2 "Measured in Miles": the Reckoning-Works clerk who wandered all the
            # way down to town after the Paul story, watching the aurora from the west ledge
            {"id": "works_wander_hollis", "at": {"tx": 5, "ty": 18}, "facing": "up", "sprite": "npc_man", "movement": "static", "dialogue_ref": "script.works_wander_hollis", "requires_flag": "flag:q_works_story", "hidden_when_flag": "flag:works_found_hollis"},
        ],
    },
    "pearlmoor_breakwater": {
        "objects": [
            # S4: Paul and the dark lamp
            {"id": "dark_lamp", "sprite": "tideglass_wrecklamp_dark", "at": {"tx": 8, "ty": 25}, "w": 1, "h": 2, "overhang": 1},
        ],
        "npcs": [
            # S4: Paul and the dark lamp
            {"id": "paul_meet", "at": {"tx": 9, "ty": 25}, "facing": "down", "sprite": "booji_paul", "movement": "static", "dialogue_ref": "script.booji_paul", "requires_flag": "flag:q_south_booji", "hidden_when_flag": "flag:q_south_booji_met"},
            {"id": "paul_lamp", "at": {"tx": 9, "ty": 25}, "facing": "down", "sprite": "booji_paul", "movement": "static", "dialogue_ref": "script.booji_paul_lamp", "requires_flag": "flag:q_south_booji_met", "hidden_when_flag": "flag:q_south_wander"},
            {"id": "paul_lamp_back", "at": {"tx": 9, "ty": 25}, "facing": "down", "sprite": "booji_paul", "movement": "static", "dialogue_ref": "script.booji_paul_lamp", "requires_flag": "flag:q_south_wander_done"},
        ],
        "triggers": [
            # S4: the Chickenpig at the breakwater
            {"id": "chickenpig_leash_w", "kind": "cutscene", "at": {"tx": 8, "ty": 24}, "activation": "step_on", "ref": "script.booji_chickenpig", "requires_flag": "flag:q_south_booji_done", "hidden_when_flag": "flag:chickenpig_caught"},
            {"id": "chickenpig_leash_n", "kind": "cutscene", "at": {"tx": 9, "ty": 23}, "activation": "step_on", "ref": "script.booji_chickenpig", "requires_flag": "flag:q_south_booji_done", "hidden_when_flag": "flag:chickenpig_caught"},
            {"id": "chickenpig_after", "kind": "dialogue", "at": {"tx": 8, "ty": 26}, "activation": "interact", "ref": "npc.chickenpig_after", "requires_flag": "flag:chickenpig_caught"},
            # S5: Not All Who Wander
            {"id": "wander_note", "kind": "dialogue", "at": {"tx": 8, "ty": 25}, "activation": "interact", "ref": "npc.wander_note", "requires_flag": "flag:q_south_wander", "hidden_when_flag": "flag:q_south_wander_done"},
        ],
    },
    "pearlmoor_quay": {
        "patch": {
            "encounters": {
                "fringe_grass": {"table": T((26, 60, 8, 11), (31, 40, 9, 11), (5, 10, 9, 11))},
                "harbour_water_w": {"table": T((2, 45, 10, 12), (27, 35, 10, 12), (24, 20, 11, 12), (20, 20, 10, 12))},
                "harbour_water_e": {"table": T((2, 45, 10, 12), (27, 35, 10, 12), (24, 20, 11, 12), (20, 20, 10, 12))},
            },
        },
        "day": {
            "fringe_grass": T((26, 55, 56, 62), (31, 45, 56, 63)),
            "harbour_water_w": T((2, 40, 57, 64), (27, 30, 57, 64), (24, 30, 58, 64), (20, 15, 57, 64)),
            "harbour_water_e": T((2, 40, 57, 64), (27, 30, 57, 64), (24, 30, 58, 64), (20, 15, 57, 64)),
        },
        "npcs": [
            # P1 postgame: a letter recipient (script.post_letter_*)
            {"id": "letter_reyl", "at": {"tx": 13, "ty": 13}, "facing": "down", "sprite": "npc_lampwarden", "movement": "static", "dialogue_ref": "script.post_letter_pearlmoor", "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_pearlmoor"},
            # a found cache
            {"id": "cache_purse", "at": {"tx": 1, "ty": 17}, "facing": "down", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_pearlmoor_purse", "hidden_when_flag": "flag:picked_pearlmoor_purse"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 10, "ty": 17}, "facing": "down", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
        ],
    },
    "saltreach_fen_ii": {
        "patch": {
            "encounters": {
                "reed_a": {"table": T((59, 40, 17, 19), (60, 15, 18, 19), (47, 15, 17, 19))},
                "reed_b": {"table": T((59, 40, 17, 19), (60, 15, 18, 19), (47, 15, 17, 19))},
                "reed_c": {"table": T((59, 40, 17, 19), (60, 15, 18, 19), (47, 15, 17, 19))},
                "reed_d": {"table": T((59, 40, 17, 19), (60, 15, 18, 19), (47, 15, 17, 19))},
            },
        },
        "day": {
            "reed_a": T((59, 35, 56, 62), (60, 12, 57, 63), (67, 8, 57, 64)),
            "reed_b": T((59, 35, 56, 62), (60, 12, 57, 63), (67, 8, 57, 64)),
            "reed_c": T((59, 35, 56, 62), (60, 12, 57, 63), (67, 8, 57, 64)),
            "reed_d": T((59, 35, 56, 62), (60, 12, 57, 63), (67, 8, 57, 64)),
            "channels": T((31, 40, 56, 63), (27, 30, 56, 63), (60, 30, 57, 64)),
        },
    },
    "spore_grotto": {
        "patch": {
            "encounters": {
                "spore_a": {"table": T((57, 40, 21, 23), (56, 30, 21, 23), (67, 22, 22, 23), (58, 8, 22, 23), (65, 15, 21, 23))},
            },
        },
        "npcs": [
            # a found cache
            {"id": "cache_drop", "at": {"tx": 5, "ty": 8}, "facing": "down", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_grotto_drop", "hidden_when_flag": "flag:picked_grotto_drop"},
        ],
    },
    "sunkbell_shallows": {
        "patch": {
            "encounters": {
                "shallows": {"table": T((27, 35, 17, 19), (31, 30, 17, 19), (24, 20, 18, 20), (61, 15, 19, 20), (21, 8, 18, 20))},
            },
        },
        "day": {
            "shallows": T((27, 30, 56, 62), (31, 28, 56, 63), (24, 27, 57, 64), (61, 15, 58, 65)),
        },
    },
    "sunken_solarium": {
        "patch": {
            "encounters": {
                "garden_a": {"table": T((114, 28, 43, 45), (117, 14, 43, 46), (120, 12, 43, 46), (124, 10, 43, 46), (126, 10, 43, 46), (115, 8, 44, 46), (118, 8, 44, 46), (104, 6, 45, 46), (125, 6, 44, 46), (116, 4, 45, 46), (121, 3, 45, 46), (127, 3, 45, 46))},
                "garden_b": {"table": T((114, 28, 43, 45), (117, 14, 43, 46), (120, 12, 43, 46), (124, 10, 43, 46), (126, 10, 43, 46), (115, 8, 44, 46), (118, 8, 44, 46), (104, 6, 45, 46), (125, 6, 44, 46), (116, 4, 45, 46), (121, 3, 45, 46), (127, 3, 45, 46))},
                "crossing_a": {"table": T((105, 18, 42, 44), (111, 16, 42, 44), (103, 14, 42, 44), (114, 24, 42, 44), (117, 10, 42, 45), (120, 8, 43, 45), (124, 7, 43, 45), (126, 7, 43, 45), (106, 4, 44, 46), (121, 2, 44, 46))},
                "crossing_b": {"table": T((105, 18, 42, 44), (111, 16, 42, 44), (103, 14, 42, 44), (114, 24, 42, 44), (117, 10, 42, 45), (120, 8, 43, 45), (124, 7, 43, 45), (126, 7, 43, 45), (106, 4, 44, 46), (121, 2, 44, 46))},
            },
        },
        "npcs": [
            # P1 postgame: a letter recipient (script.post_letter_*)
            {"id": "letter_lucan", "at": {"tx": 11, "ty": 16}, "facing": "down", "sprite": "lucan", "movement": "static", "dialogue_ref": "script.post_letter_solarium", "requires_flag": "flag:q_post_letters", "hidden_when_flag": "flag:q_post_letter_solarium"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 28, "ty": 8}, "facing": "right", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
        ],
    },
    "thunderroost": {
        "day": {
            "roost_a": T((90, 20, 60, 65), (89, 40, 57, 63), (95, 30, 58, 64), (93, 10, 60, 65)),
        },
    },
    "tideglass_cavern": {
        "patch": {
            "encounters": {
                "glass_entry": {"table": T((26, 30, 20, 22), (24, 24, 21, 22), (27, 20, 21, 22), (50, 26, 20, 22))},
                "glass_hall_n": {"table": T((26, 30, 20, 22), (24, 24, 21, 24), (27, 20, 21, 24), (50, 26, 20, 23))},
                "glass_hall_e": {"table": T((26, 30, 20, 22), (24, 24, 21, 24), (27, 20, 21, 24), (50, 26, 20, 23))},
            },
        },
    },
    "tinderwick_beacon_top": {
        "npcs": [
            # the post-game wick case
            {"id": "post_wick_case", "at": {"tx": 4, "ty": 4}, "facing": "up", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_post_wick", "requires_flag": "flag:q_post_wick_asked", "hidden_when_flag": "flag:q_post_wick"},
        ],
    },
    "umbral_spire_f2": {
        "encounters": [
            # the Spire's weave bed
            {"id": "weave_bed", "terrain": "cave", "rect": {"tx": 12, "ty": 22, "w": 5, "h": 2}, "encounter_rate": 0.1, "table": T((147, 100, 52, 55))},
        ],
        "triggers": [
            # the Spire's null-works
            {"id": "nullworks_kin_0", "kind": "script", "at": {"tx": 8, "ty": 9}, "activation": "interact", "ref": "script.nullworks_nullmajor", "requires_flag": "flag:dawn", "hidden_when_flag": "flag:nullmajor_caught"},
            {"id": "nullworks_after_0", "kind": "dialogue", "at": {"tx": 8, "ty": 9}, "activation": "interact", "ref": "npc.nullworks_after", "requires_flag": "flag:nullmajor_caught"},
            {"id": "nullworks_kin_1", "kind": "script", "at": {"tx": 9, "ty": 9}, "activation": "interact", "ref": "script.nullworks_nullmajor", "requires_flag": "flag:dawn", "hidden_when_flag": "flag:nullmajor_caught"},
            {"id": "nullworks_after_1", "kind": "dialogue", "at": {"tx": 9, "ty": 9}, "activation": "interact", "ref": "npc.nullworks_after", "requires_flag": "flag:nullmajor_caught"},
        ],
    },
    "umbral_spire_summit": {
        "npcs": [
            # the Starfall Vigils (postgame)
            {"id": "vigil_ondra_summit", "at": {"tx": 10, "ty": 10}, "facing": "right", "sprite": "kite_weaver", "movement": "static", "dialogue_ref": "npc.vigil_ondra_summit", "requires_flag": "flag:vigil_5_kept", "hidden_when_flag": "flag:starfall_lesson"},
            {"id": "vigil_solenne_summit", "at": {"tx": 12, "ty": 10}, "facing": "right", "sprite": "sun_keeper", "movement": "static", "dialogue_ref": "npc.vigil_solenne_summit", "requires_flag": "flag:vigil_5_kept", "hidden_when_flag": "flag:starfall_lesson"},
            {"id": "vigil_mer_summit", "at": {"tx": 15, "ty": 9}, "facing": "left", "sprite": "hollowing_elder", "movement": "static", "dialogue_ref": "npc.vigil_mer_summit", "requires_flag": "flag:vigil_5_kept", "hidden_when_flag": "flag:starfall_lesson"},
            # the Last Lesson (postgame)
            {"id": "fenn_last_lesson", "at": {"tx": 11, "ty": 8}, "facing": "down", "sprite": "npc_mentor", "movement": "static", "dialogue_ref": "script.last_lesson_again", "requires_flag": "flag:starfall_crown"},
        ],
        "triggers": [
            # the Starfall Vigils (postgame)
            {"id": "starfall_round_0", "kind": "cutscene", "at": {"tx": 10, "ty": 7}, "activation": "interact", "ref": "script.starfall_round", "requires_flag": "flag:vigil_5_kept", "blocked_ref": "npc.starfall_round_waiting", "hidden_when_flag": "flag:starfall_lesson"},
            {"id": "starfall_round_1", "kind": "cutscene", "at": {"tx": 11, "ty": 7}, "activation": "interact", "ref": "script.starfall_round", "requires_flag": "flag:vigil_5_kept", "blocked_ref": "npc.starfall_round_waiting", "hidden_when_flag": "flag:starfall_lesson"},
            {"id": "starfall_round_2", "kind": "cutscene", "at": {"tx": 12, "ty": 7}, "activation": "interact", "ref": "script.starfall_round", "requires_flag": "flag:vigil_5_kept", "blocked_ref": "npc.starfall_round_waiting", "hidden_when_flag": "flag:starfall_lesson"},
            # the summit re-dress (postgame)
            {"id": "dawnbrael_wakes_0", "kind": "cutscene", "at": {"tx": 10, "ty": 7}, "activation": "interact", "ref": "cutscene.dawnbrael_wakes", "requires_flag": "flag:starfall_lesson", "hidden_when_flag": "flag:dawnbrael_caught"},
            {"id": "dawnbrael_wakes_1", "kind": "cutscene", "at": {"tx": 11, "ty": 7}, "activation": "interact", "ref": "cutscene.dawnbrael_wakes", "requires_flag": "flag:starfall_lesson", "hidden_when_flag": "flag:dawnbrael_caught"},
            {"id": "dawnbrael_wakes_2", "kind": "cutscene", "at": {"tx": 12, "ty": 7}, "activation": "interact", "ref": "cutscene.dawnbrael_wakes", "requires_flag": "flag:starfall_lesson", "hidden_when_flag": "flag:dawnbrael_caught"},
            {"id": "startender_named_0", "kind": "cutscene", "at": {"tx": 10, "ty": 7}, "activation": "interact", "ref": "cutscene.startender_named", "once": True, "requires_flag": "flag:dawnbrael_caught", "hidden_when_flag": "flag:starfall_crown"},
            {"id": "startender_named_1", "kind": "cutscene", "at": {"tx": 11, "ty": 7}, "activation": "interact", "ref": "cutscene.startender_named", "once": True, "requires_flag": "flag:dawnbrael_caught", "hidden_when_flag": "flag:starfall_crown"},
            {"id": "startender_named_2", "kind": "cutscene", "at": {"tx": 12, "ty": 7}, "activation": "interact", "ref": "cutscene.startender_named", "once": True, "requires_flag": "flag:dawnbrael_caught", "hidden_when_flag": "flag:starfall_crown"},
        ],
    },
    "vesper_crossroads": {
        "npcs": [
            # the easter-egg trail (S4)
            {"id": "egg_teller", "at": {"tx": 13, "ty": 9}, "facing": "left", "sprite": "star_watcher", "movement": "look_around", "dialogue_ref": "npc.egg_hint_crossroads"},
            # Andrew on his fence — wayfinding (script.andrew_road)
            {"id": "andrew_road", "at": {"tx": 3, "ty": 8}, "facing": "left", "sprite": "andrew_ward", "movement": "look_around", "dialogue_ref": "script.andrew_road"},
            # the Worry Club (R9)
            {"id": "worry_constance", "at": {"tx": 14, "ty": 5}, "facing": "left", "sprite": "npc_woman", "movement": "look_around", "dialogue_ref": "script.worry_constance"},
        ],
    },
    "wind_eye": {
        "day": {
            "ring_a": T((93, 25, 60, 65), (94, 40, 57, 63), (95, 35, 58, 64)),
            "ring_b": T((93, 25, 60, 65), (94, 40, 57, 63), (95, 35, 58, 64)),
            "bed_a": T((93, 25, 60, 65), (94, 40, 57, 63), (95, 35, 58, 64)),
        },
        "npcs": [
            # a found cache
            {"id": "cache_drop", "at": {"tx": 8, "ty": 15}, "facing": "down", "sprite": "item_cache", "movement": "static", "dialogue_ref": "script.pickup_windeye_drop", "hidden_when_flag": "flag:picked_windeye_drop"},
        ],
    },
    "windward_stair_i": {
        "day": {
            "verge_a": T((89, 30, 56, 62), (45, 20, 56, 62), (98, 15, 56, 61), (95, 10, 57, 63), (77, 10, 56, 61), (91, 15, 57, 63)),
            "ledge_a": T((89, 30, 56, 62), (45, 20, 56, 62), (98, 15, 56, 61), (95, 10, 57, 63), (77, 10, 56, 61), (91, 15, 57, 63)),
            "ledge_b": T((89, 30, 56, 62), (45, 20, 56, 62), (98, 15, 56, 61), (95, 10, 57, 63), (77, 10, 56, 61), (91, 15, 57, 63)),
            "crossing_a": T((89, 30, 56, 62), (45, 20, 56, 62), (98, 15, 56, 61), (95, 10, 57, 63), (77, 10, 56, 61), (91, 15, 57, 63)),
            "crossing_b": T((89, 30, 56, 62), (45, 20, 56, 62), (98, 15, 56, 61), (95, 10, 57, 63), (77, 10, 56, 61), (91, 15, 57, 63)),
        },
    },
    "windward_stair_ii": {
        "day": {
            "crag_a": T((95, 25, 57, 63), (89, 20, 56, 62), (45, 15, 56, 62), (98, 15, 57, 62), (74, 10, 56, 62), (91, 15, 57, 64)),
            "crag_b": T((95, 25, 57, 63), (89, 20, 56, 62), (45, 15, 56, 62), (98, 15, 57, 62), (74, 10, 56, 62), (91, 15, 57, 64)),
            "crossing_a": T((95, 25, 57, 63), (89, 20, 56, 62), (45, 15, 56, 62), (98, 15, 57, 62), (74, 10, 56, 62), (91, 15, 57, 64)),
            "crossing_b": T((95, 25, 57, 63), (89, 20, 56, 62), (45, 15, 56, 62), (98, 15, 57, 62), (74, 10, 56, 62), (91, 15, 57, 64)),
        },
    },
}

# The inn folk (2026-10, content/regions/innfolk.ts): Hesper Vane the Echo-Reader by
# the hearth in every inn (left of the fire; tiles proven not to block the room),
# and Ottilie Penn the Namewright at the lamp-school's bookcase.
_HESPER_SEATS = {
    "crossroads_inn": ("crossroads", 7, 3),
    "pearlmoor_inn": ("pearlmoor", 7, 3),
    "lowleaf_bower": ("lowleaf", 4, 3),
    "galehigh_inn": ("galehigh", 4, 3),
    "pale_vault_inn": ("pale_vault", 4, 3),
    "nightreach_inn": ("nightreach", 4, 3),
}
for _mid, (_inn, _x, _y) in _HESPER_SEATS.items():
    PLACEMENTS.setdefault(_mid, {}).setdefault("npcs", []).append(
        {"id": "hesper", "at": {"tx": _x, "ty": _y}, "facing": "right", "sprite": "pass_walker",
         "movement": "static", "dialogue_ref": f"script.hesper_{_inn}"})
PLACEMENTS.setdefault("wickstead_school", {}).setdefault("npcs", []).append(
    {"id": "namewright", "at": {"tx": 3, "ty": 2}, "facing": "down", "sprite": "npc_old_man",
     "movement": "static", "dialogue_ref": "script.namewright"})

# ---- Lane A (walkthrough/10 Part II, 2026-10): the Ashfall Shelf + Kiln Gully day-forms.
# After the dawn the ash-grass greens at the tips: Stonebark's line wakes as Rootwarden,
# and the storm-birds come down off Windward. Mirrored in build_species.py
# (ASHFALL_DAY_ENCOUNTERS). Zone ids are the builders' zone ids.
_ASH_DAY = T((46, 30, 56, 61), (49, 25, 56, 61), (90, 20, 57, 62), (102, 15, 57, 62), (64, 10, 58, 62))
PLACEMENTS["cinderwind_ashfall"] = {"day": {z: _ASH_DAY for z in (
    "ashfall_green_a", "ashfall_green_b", "ashfall_green_c", "ashfall_ash_a", "ashfall_ash_b")}}
_KILN_DAY = T((37, 25, 57, 63), (69, 25, 56, 62), (55, 20, 57, 63), (43, 20, 56, 62), (52, 10, 58, 63))
PLACEMENTS["cinderwind_kiln"] = {"day": {z: _KILN_DAY for z in ("kiln_hall", "kiln_rooms")}}

# ---- The Lumenary sparring partners (2026-10 economy review, content/sparring.ts):
# a hall apprentice who spars for a keeper-class purse once that hall's Gleam is
# relit (repeatable: the `spar` op rests them for 3 won battles). Off the aisle,
# beside the door side; tiles proven 4-way open and clear of warps/triggers/NPCs.
_SPAR_POSTS = {
    "tinderwick_lumenary": ("tinderwick", "gleam:ember", 3, 8),
    "pearlmoor_lumenary": ("pearlmoor", "gleam:tide", 3, 8),
    "lowleaf_lumenary": ("lowleaf", "gleam:verdant", 13, 7),
    "cinderhead_lumenary": ("cinderhead", "gleam:stone", 4, 9),
    "galehigh_lumenary": ("galehigh", "gleam:storm", 3, 8),
    "pale_vault_lumenary": ("pale_vault", "gleam:frost", 3, 8),
    "sunken_solarium_lumenary": ("sunken_solarium", "gleam:solar", 4, 6),
    "nightreach_lumenary": ("nightreach", "gleam:lunar", 3, 7),
}
for _mid, (_hall, _gleam, _x, _y) in _SPAR_POSTS.items():
    PLACEMENTS.setdefault(_mid, {}).setdefault("npcs", []).append(
        {"id": "hall_sparrer", "at": {"tx": _x, "ty": _y}, "facing": "right" if _x < 8 else "left",
         "sprite": "npc_man" if _hall in ("pearlmoor", "cinderhead", "sunken_solarium") else "npc_woman",
         "movement": "static", "requires_flag": _gleam, "dialogue_ref": f"script.spar_{_hall}"})
