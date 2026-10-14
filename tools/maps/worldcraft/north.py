"""NORTH world-craft placements (owned by WP4 — the North regional package).

PLACEMENTS: map id -> spec (keys documented in _kit.py). Applied by
`python3 tools/maps/add_world_craft.py --region north`.

What this module does (docs/reviews/world-craft-panel.md §4 #2, §6 WP4):
  * Windward Stair I — the longest crossing in the game — stays the same length
    but becomes a journey: a cairn at every switchback that takes your stone
    (the summit cairn notices all four), wind-shrines, prayer-flag lines strung
    over the lane, a climbers' shelter halfway, kite wreckage, wind-bent pines
    and a lookout spyglass that shows a star falling towards the mountain.
  * Windward Stair II, Thunderroost, the Skyloft: props + weather.
  * Galehigh: leaf gusts, birds, wind-vane + kite rack; Pale Vault: snow, an
    aurora wash, ice lanterns, a herder's sled and fur rack; Còr's acolyte.
  * The regional cast (kite_weaver, kite_child, frost_herder, innkeeper,
    market_trader, lamplighter, hollowing_acolyte) swapped onto existing
    placements — ids and dialogue refs unchanged.
Nothing here changes an encounter table, trainer, warp or the main lane.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from ._kit import add_words, ambient_kin, lit, particles  # noqa: F401

MAPS = Path(__file__).resolve().parents[3] / "public" / "assets" / "maps"


def obj(oid, sprite, at, w, h, *, overhang=0, walk_under=None, solid=None, **flags):
    o = {"id": oid, "sprite": sprite, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    if overhang:
        o["overhang"] = overhang
    if walk_under is not None:
        o["walk_under"] = walk_under
    if solid is not None:
        o["solid"] = solid
    o.update(flags)
    return o


def flags_line(oid, at):
    """A prayer-flag line strung OVER the ground: draws above actors, never collides."""
    return obj(oid, "windward_prayer_flags", at, 4, 2, overhang=2, walk_under=True, solid=False)


def drift(oid, at):
    return obj(oid, "windward_snow_drift", at, 2, 1, solid=False)


def tall(oid, sprite, at, w=2, h=3):
    """A tall prop whose top rows you can walk behind; only the base row collides."""
    return obj(oid, sprite, at, w, h, overhang=h - 1, walk_under=True)


def recast(mid: str, **sprites: str) -> list[dict]:
    """Re-dress existing NPC placements with a regional-cast sheet (id/ref unchanged)."""
    path = MAPS / f"{mid}.json"
    m = json.loads(path.read_text()) if path.is_file() else {}
    out = []
    for n in m.get("npcs", []):
        if n["id"] in sprites:
            n = dict(n)
            n["sprite"] = sprites[n["id"]]
            out.append(n)
    missing = set(sprites) - {n["id"] for n in out}
    if missing:
        print(f"north.recast {mid}: no NPC ids {sorted(missing)} — skipped", file=sys.stderr)
    return out


def cutscene(tid, at, ref, **extra):
    t = {"id": tid, "kind": "script", "at": {"tx": at[0], "ty": at[1]}, "activation": "interact", "ref": ref}
    t.update(extra)
    return t


SNOW_WIND = [particles("snow", 0.6), particles("motes", 0.9)]
WIND_BED = "amb-wind"  # silent until rendered (Ambience tolerates a missing stem)

PLACEMENTS: dict[str, dict] = {
    # ------------------------------------------------------------------ the climb
    "windward_stair_i": {
        "ambience": {
            "particles": SNOW_WIND,
            "mist": {"color": "#e6eef8", "alpha": 0.1, "speed": 10},
            "starfall": {"min_s": 30, "max_s": 70},
            "birds": {"kind": "bird", "flocks": [{"tx": 20, "ty": 36}], "flyover": True},
            "light_sources_extra": [{"at": {"tx": 5, "ty": 30}, "radius": 12, "color": "#ffc46b"}],
            "sound_bed": WIND_BED,
        },
        "objects": [
            # the foot: a shrine under the cliff, flags over the first lane, a pine, a wreck
            tall("ww_shrine_foot", "windward_wind_shrine", (6, 32)),
            flags_line("ww_flags_foot", (8, 34)),
            tall("ww_pine_foot", "windward_bent_pine", (16, 33)),
            obj("ww_wreck_foot", "windward_kite_wreck_b", (16, 36), 2, 2),
            # the second shelf: the climbers' shelter (halfway) + flags over the lane
            obj("ww_shelter", "windward_rest_shelter", (4, 29), 4, 3, overhang=1),
            flags_line("ww_flags_mid", (9, 27)),
            # the kettle shelf
            flags_line("ww_flags_kettle", (15, 21)),
            drift("ww_drift_kettle_w", (2, 25)),
            drift("ww_drift_kettle_e", (12, 25)),
            # the fourth shelf
            tall("ww_shrine_ledge", "windward_wind_shrine", (2, 14)),
            tall("ww_pine_ledge", "windward_bent_pine", (20, 14)),
            obj("ww_wreck_ledge", "windward_kite_wreck_b", (2, 17), 2, 2),
            # the head: a pine, a shrine below the wind-gap, flags, drifts — and the
            # lookout (listed last: it was added after, and list order is shipped order)
            tall("ww_pine_head", "windward_bent_pine", (2, 7)),
            tall("ww_shrine_head", "windward_wind_shrine", (2, 4)),
            flags_line("ww_flags_head", (14, 6)),
            drift("ww_drift_head_a", (19, 9)),
            drift("ww_drift_head_b", (3, 12)),
            drift("ww_drift_head_c", (17, 12)),
            obj("ww_spyglass", "windward_spyglass", (10, 6), 2, 2),
        ],
        "triggers": [
            cutscene("ww_cairn_foot", (4, 34), "script.windward_cairn_foot"),
            cutscene("ww_cairn_kettle", (5, 22), "script.windward_cairn_kettle"),
            cutscene("ww_cairn_mid", (18, 25), "script.windward_cairn_mid"),
            cutscene("ww_cairn_head", (6, 7), "script.windward_cairn_head"),
            cutscene("ww_cairn_summit", (18, 7), "script.windward_cairn_summit"),
            cutscene("ww_shelter_sit", (4, 31), "script.windward_shelter"),
            cutscene("ww_shrine_foot_look", (6, 34), "script.windward_shrine"),
            cutscene("ww_shrine_head_look", (3, 6), "script.windward_shrine"),
            cutscene("ww_spyglass_look", (10, 7), "script.windward_spyglass"),
        ],
        "npcs": [
            ambient_kin("amb_flintbeak", (20, 34), 89, radius=1),
            ambient_kin("amb_chillpip", (5, 11), 77, radius=2),
            *recast("windward_stair_i", wind_pilgrim="pass_walker",
                    windward_galewatch="kite_weaver", windward_galewatch_after="kite_weaver"),
        ],
    },
    "windward_stair_ii": {
        "ambience": {
            "particles": [particles("snow", 0.8), particles("motes", 0.8)],
            "mist": {"color": "#e6eef8", "alpha": 0.12, "speed": 12},
            "starfall": {"min_s": 25, "max_s": 60},
            "birds": {"kind": "bird", "flyover": True},
            "sound_bed": WIND_BED,
        },
        "objects": [
            tall("w2_shrine", "windward_wind_shrine", (22, 17)),
            tall("w2_pine_e", "windward_bent_pine", (24, 18)),
            tall("w2_pine_n", "windward_bent_pine", (22, 2)),
            flags_line("w2_flags", (11, 16)),
            obj("w2_woodpile", "pale_vault_woodpile", (6, 18), 2, 2),
            drift("w2_drift_a", (20, 21)),
            drift("w2_drift_b", (3, 5)),
        ],
        "triggers": [cutscene("w2_shrine_look", (22, 19), "script.windward_shrine")],
        "npcs": [ambient_kin("amb_geolace", (21, 3), 74, radius=1)],
    },
    "thunderroost": {
        "ambience": {
            "particles": [particles("snow", 0.5), particles("motes", 1.0)],
            "tint": {"color": "#1b2440", "alpha": 0.16},
            "mist": {"color": "#9aa3b8", "alpha": 0.14, "speed": 16},
            "starfall": {"min_s": 25, "max_s": 55},
            "birds": {"kind": "bird", "flyover": True},
            "sound_bed": WIND_BED,
        },
        "objects": [
            tall("roost_rod", "windward_lightning_rod", (13, 2), 1, 3),
            obj("roost_struck", "windward_struck_rock", (12, 7), 2, 2),
            obj("roost_wreck", "windward_kite_wreck_b", (9, 8), 2, 2),
        ],
        "npcs": [ambient_kin("amb_strikeaven", (11, 5), 90, radius=1)],
    },
    "wind_eye": {
        "ambience": {
            "mist": {"color": "#e8f0ff", "alpha": 0.18, "speed": 8},
            "particles": [particles("motes", 0.8), particles("starglint", 0.4)],
        },
    },
    "pale_vault_undercroft": {
        "ambience": {
            "tint": {"color": "#a8f0d0", "alpha": 0.05},
            "particles": [particles("motes", 0.4)],
        },
    },
    # ------------------------------------------------------------------ Galehigh
    "galehigh_terraces": {
        "sprites": {"andrew_road": "andrew_cyclist"},  # Andrew in costume (his fence, his look)
        "ambience": {
            "particles": [particles("leaves", 0.8), particles("motes", 0.6)],
            "mist": {"color": "#2a3550", "alpha": 0.07, "speed": 6},  # cloud shadow
            "starfall": {"min_s": 40, "max_s": 80},
            "birds": {"kind": "bird", "flocks": [{"tx": 8, "ty": 3}], "flyover": True},
            "sound_bed": WIND_BED,
        },
        "objects": [
            tall("gh_wind_vane", "galehigh_wind_vane", (3, 2), 1, 3),
            obj("gh_kite_rack", "galehigh_kite_rack", (6, 2), 3, 2),
        ],
        "npcs": [
            ambient_kin("amb_sparrowcaw", (8, 6), 88, radius=2),
            ambient_kin("amb_cirruff", (27, 20), 91, radius=1),
            *recast("galehigh_terraces",
                    galehigh_kitehand="kite_weaver", galehigh_kitehand_after="kite_weaver",
                    festival_piper="market_trader", festival_kid="kite_child",
                    festival_goer="star_watcher", peril_notice_reader="kite_weaver",
                    kite_maker_lost="kite_weaver", kite_maker_build="kite_weaver",
                    kite_maker_after="kite_weaver", kite_maker_round="kite_weaver",
                    kite_maker_round_after="kite_weaver"),
        ],
    },
    # ------------------------------------------------------------------ Lane A
    # The Ashfall Shelf (walkthrough/10 Part II): ash on the wind, the brazier's
    # embers, cloud shadow; kin from the shelf's own table, off the lanes —
    # Stonebark (the shelf's rare) grazes by the lookout as a tease.
    "cinderwind_ashfall": {
        "ambience": {
            "particles": [particles("dust", 0.9), particles("embers", 0.3), particles("motes", 0.5)],
            "mist": {"color": "#3a3a46", "alpha": 0.06, "speed": 5},
            "starfall": {"min_s": 45, "max_s": 90},
            "birds": {"kind": "bird", "flocks": [{"tx": 12, "ty": 4}], "flyover": True},
            "sound_bed": WIND_BED,
        },
        "npcs": [
            ambient_kin("amb_gravelo", (13, 10), 49, radius=1),
            ambient_kin("amb_stonebark", (17, 6), 63, radius=1),
            ambient_kin("amb_flintbeak", (17, 16), 89, radius=1),
        ],
    },
    "cinderwind_kiln": {
        "ambience": {"particles": [particles("embers", 0.4), particles("dust", 0.5)],
                     "tint": {"color": "#ff9a50", "alpha": 0.04}},
    },
    "galehigh_skyloft": {
        "ambience": {
            "particles": [particles("leaves", 0.6), particles("motes", 1.0)],
            "starfall": {"min_s": 30, "max_s": 70},
            "birds": {"kind": "bird", "flyover": True},
            "sound_bed": WIND_BED,
        },
        "objects": [
            obj("sl_kite_rack", "galehigh_kite_rack", (4, 8), 3, 2),
            tall("sl_wind_vane", "galehigh_wind_vane", (16, 5), 1, 3),
        ],
        "npcs": recast("galehigh_skyloft", skyloft_ward_a="kite_weaver",
                       skyloft_ward_a_after="kite_weaver"),
    },
    "lanternway_galehigh": {
        "ambience": {"particles": [particles("leaves", 0.5), particles("motes", 0.5)],
                     "starfall": {"min_s": 35, "max_s": 75}},
        "npcs": [{"id": "lanternway_galehigh_lamplighter", "at": {"tx": 4, "ty": 10}, "facing": "right",
                  "sprite": "lamplighter", "dialogue_ref": "npc.lanternway_galehigh_lamplighter"}],
    },
    "galehigh_inn": {"npcs": recast("galehigh_inn", innkeeper="innkeeper", guest="pass_walker")},
    "galehigh_home": {"npcs": recast("galehigh_home", home_kid="kite_child")},
    "galehigh_kitemaker": {"npcs": recast("galehigh_kitemaker", keeper_kit="market_trader",
                                          keeper="market_trader")},
    "galehigh_lumenary": {"npcs": recast("galehigh_lumenary", hall_festival="kite_weaver")},
    # ------------------------------------------------------------------ Pale Vault
    "pale_vault_glacier": {
        "sprites": {"andrew_road": "andrew_frost"},  # Andrew in costume (his fence, his look)
        "ambience": {
            "particles": [particles("snow", 1.0), particles("starglint", 0.4)],
            "tint": {"color": "#7fe0c0", "alpha": 0.06},  # the aurora, always overhead
            "starfall": {"min_s": 25, "max_s": 55},
            "footprints": "all",
            "sound_bed": WIND_BED,
        },
        "objects": [
            obj("pv_fur_rack", "pale_vault_fur_rack", (2, 26), 2, 2),
            obj("pv_sled", "pale_vault_herder_sled", (9, 24), 2, 2),
            tall("pv_ice_lantern_w", "pale_vault_ice_lantern", (10, 12), 1, 2),
            tall("pv_ice_lantern_e", "pale_vault_ice_lantern", (22, 12), 1, 2),
            tall("pv_ice_lantern_s", "pale_vault_ice_lantern", (16, 25), 1, 2),
        ],
        "npcs": [
            ambient_kin("amb_snowcune", (20, 24), 80, radius=1),
            ambient_kin("amb_iceling", (28, 13), 71, radius=1),
            # Còr's people: one silent acolyte keeps the shelf with him (B3).
            {"id": "cor_acolyte", "at": {"tx": 2, "ty": 18}, "facing": "right",
             "sprite": "hollowing_acolyte", "dialogue_ref": "npc.cor_acolyte",
             "requires_flag": "flag:q_north_lampline", "hidden_when_flag": "flag:met_cor"},
            *recast("pale_vault_glacier",
                    townsfolk_inn="frost_herder", aurora_watcher_b="star_watcher",
                    vigil_keeper="lamplighter", vigil_keeper_after="lamplighter",
                    aurora_watcher_a="frost_herder", aurora_watcher_hours="frost_herder",
                    aurora_watcher_hours_after="frost_herder", gleam_kid="village_child"),
        ],
    },
    "pale_vault_inn": {"npcs": recast("pale_vault_inn", innkeeper="innkeeper", guest="frost_herder")},
    "pale_vault_home": {"npcs": recast("pale_vault_home", home_kid="village_child")},
    "pale_vault_lumenary": {"npcs": recast("pale_vault_lumenary", hall_festival="star_watcher")},
}


# ------------------------------------------------------------- AFTER-GLEAM
# Galehigh and Pale Vault answer their Gleams (src/game/content/regions/north.ts).
# Words only: `lit` twins share their original's tile, sheet and body; `talk`
# re-points keep the id (the Kite-rising / Aurora-watch actors, the shop's kit
# pair, the tallow-keeper's oil chain).
STORM, FROST = "gleam:storm", "gleam:frost"
add_words(PLACEMENTS, {
    "galehigh_terraces": {
        "after": [lit("terrace_farmer", STORM, "npc.galehigh_farmer_lit")],
        "talk": {"festival_piper": "script.galehigh_piper_staged",
                 "festival_kid": "script.galehigh_festival_kid_staged",
                 "festival_goer": "script.galehigh_festival_goer_staged"},
    },
    "galehigh_lumenary": {"after": [lit("hall_keeper", STORM, "npc.galehigh_hall_keeper_lit")]},
    "galehigh_inn": {"after": [lit("innkeeper", STORM, "script.galehigh_inn_rest_lit"),
                               lit("guest", STORM, "npc.galehigh_inn_guest_lit")]},
    "galehigh_home": {"after": [lit("home_elder", STORM, "npc.galehigh_home_elder_lit"),
                                lit("home_kid", STORM, "npc.galehigh_home_kid_lit")]},
    "galehigh_kitemaker": {"talk": {"keeper": "script.shop_galehigh_staged"}},
    "lanternway_galehigh": {"after": [lit("lanternway_galehigh_lamplighter", STORM,
                                          "npc.lanternway_galehigh_lamplighter_lit")]},
    "pale_vault_glacier": {
        "after": [lit("townsfolk_inn", FROST, "npc.pale_vault_townsfolk_lit")],
        "talk": {"aurora_watcher_b": "script.aurora_watcher_b_staged",
                 "tallow_keeper_after": "script.tallow_keeper_staged"},
    },
    "pale_vault_home": {"after": [lit("home_elder", FROST, "npc.pale_vault_home_elder_lit"),
                                  lit("home_kid", FROST, "npc.pale_vault_home_kid_lit")]},
    "pale_vault_inn": {"after": [lit("innkeeper", FROST, "script.pale_vault_inn_rest_lit"),
                                 lit("guest", FROST, "npc.pale_vault_inn_guest_lit")]},
    "pale_vault_lumenary": {"after": [lit("hall_keeper", FROST, "npc.pale_vault_hall_keeper_lit")]},
})
