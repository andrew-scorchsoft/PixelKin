"""WEST world-craft placements (owned by this region's package — R10, 2026-10).

PLACEMENTS: map id -> spec (keys documented in _kit.py). Applied by
`python3 tools/maps/add_world_craft.py --region west`.

What lives here (everything optional colour — nothing gates a lane or a warp):
  * AMBIENCE for every West map: Hushfrost snow + mist + live footprints in
    trackless snow, Aurora Hollow's green wash, Solarium/Sunvault sun-motes and
    a warm tint, Coldfog's thick mist + drained grey + cold motes and no birds,
    the Stillworks' dim, Nightreach's star-glints; the falling-star streak runs
    FREQUENT near the mountain (Coldfog / Drownlight / Nightreach, min_s 25).
  * the REGIONAL CAST: generic townsfolk re-sheeted to the West's own people
    (pass-walker, sun-keeper, star-watchers, lamplighter, innkeeper, frost-
    herders, the Hollowing elder) — ids/dialogue unchanged, every flag-variant
    of a family re-cast together so a swap never flickers.
  * W-2: Còr's silent figure on the Stillworks' far gantry (the band moves
    him; he is gone once flag:seen_stillworks is set).
  * W-4: the pass-walker's second post at Nightreach (the map is spread there).
  * ambient kin from each map's OWN encounter table.

Builder-owned R10 dressing (props, desolation reads, fall craters) lives in the
West builders; the Hushfrost pass-walker herself rides add_peril_thread.py.
"""
from __future__ import annotations

import json
from pathlib import Path

from ._kit import add_words, ambient_kin, gid, lit, particles  # noqa: F401

MAPS = Path(__file__).resolve().parents[3] / "public" / "assets" / "maps"


def recast(mid: str, sprites: dict[str, str]) -> list[dict]:
    """Copies of `mid`'s NPCs with their sprite swapped (id -> sheet). Reads the
    shipped JSON so every other field (flags, refs, sight) is kept verbatim —
    idempotent: re-running yields the same items. Missing ids are skipped."""
    m = json.loads((MAPS / f"{mid}.json").read_text())
    out = []
    for n in m.get("npcs", []):
        if n["id"] in sprites:
            c = dict(n)
            c["sprite"] = sprites[n["id"]]
            out.append(c)
    return out


SNOW = {
    "particles": [particles("snow", 1.0)],
    "mist": {"color": "#e6eef8", "alpha": 0.12, "speed": 6},
    "tint": {"color": "#a8c0e8", "alpha": 0.06},
    "footprints": "all",
    "starfall": {"min_s": 35, "max_s": 75},
}
COLDFOG = {
    "particles": [particles("motes", 0.9)],
    "mist": {"color": "#c9ced6", "alpha": 0.34, "speed": 4},
    "tint": {"color": "#7d8796", "alpha": 0.16},
    "starfall": {"min_s": 25, "max_s": 50},
}
SUN = {
    "particles": [particles("dust", 0.8), particles("glowmotes", 0.35)],
    "tint": {"color": "#ffd089", "alpha": 0.06},
}

PLACEMENTS: dict[str, dict] = {
    # ---- Hushfrost Pass I — the recomposed pass (build_hushfrost_pass_i.py R10)
    "hushfrost_pass_i": {
        # the camp fire's pool rides LIGHT_SOURCES.hushfrost_walker_camp (Ambience.ts)
        "ambience": dict(SNOW),
        "npcs": [ambient_kin("amb_blizzrhare", (26, 8), 81, radius=2),
                 *recast("hushfrost_pass_i", {
                     "hushfrost_lampman": "lamplighter", "hushfrost_lampman_after": "lamplighter",
                     "hushfrost_survivor": "frost_herder", "hushfrost_survivor_after": "frost_herder",
                 })],
    },
    "hushfrost_pass_ii": {
        "ambience": dict(SNOW),
        "npcs": [ambient_kin("amb_hushbore", (26, 3), 84, radius=1),
                 *recast("hushfrost_pass_ii", {
                     "hushfrost_thawtender": "frost_herder",
                     "hushfrost_thawtender_after": "frost_herder"})],
    },
    "aurora_hollow": {
        "ambience": {"particles": [particles("glowmotes", 0.5)],
                     "tint": {"color": "#a8f0d0", "alpha": 0.08}},
    },
    # ---- the Sunken Solarium + its Lumenary — sun-motes and a warm wash
    "sunken_solarium": {
        "ambience": dict(SUN),
        "npcs": recast("sunken_solarium", {
            "gleam_elder": "sun_keeper", "bread_sharer": "market_trader",
            "festival_kid": "village_child"}),
    },
    "sunken_solarium_lumenary": {
        "ambience": {"particles": [particles("dust", 0.5)],
                     "tint": {"color": "#ffd089", "alpha": 0.05}},
        "npcs": recast("sunken_solarium_lumenary", {"matron": "innkeeper"}),
    },
    # ---- the Sunvault Climb — heat-shimmer motes over the gold terraces
    "sunvault_climb_i": {
        "ambience": dict(SUN),
        "npcs": [*recast("sunvault_climb_i", {
            "sunvault_terracer": "hollow_gardener", "sunvault_terracer_after": "hollow_gardener",
            "sunvault_wayfarer": "road_courier"})],
    },
    "sunvault_climb_ii": {
        "ambience": dict(SUN),
        "npcs": recast("sunvault_climb_ii", {
            "vine_tender": "orchard_farmer",
            "sunvault_skywatcher": "star_watcher", "sunvault_skywatcher_after": "star_watcher"}),
    },
    "helia_vault": {
        "ambience": {"particles": [particles("dust", 0.6)],
                     "tint": {"color": "#ffcf7a", "alpha": 0.06}},
    },
    # unrisen_stair is a Three Hours site: its ambience is owned by worldcraft/central.py.
    # ---- the Coldfog detour — drained, misted, birdless; the streak falls often
    "coldfog_marches_i": {"ambience": dict(COLDFOG)},
    "coldfog_marches_ii": {"ambience": dict(COLDFOG)},
    "drownlight_beacon": {"ambience": dict(COLDFOG)},
    "hollowfen_stillworks": {
        "ambience": {"particles": [particles("dust", 0.35)],
                     "tint": {"color": "#202430", "alpha": 0.12}},
        "npcs": [
            # W-2: Còr on the far gantry, back turned, tending a collar. The band
            # (script.hollowfen_stillworks) walks him out; flag:seen_stillworks hides him.
            {"id": "stillworks_cor", "at": {"tx": 18, "ty": 4}, "facing": "up",
             "sprite": "warden_cor", "movement": "static",
             "dialogue_ref": "script.stillworks_cor_silent",
             "hidden_when_flag": "flag:seen_stillworks"},
            *recast("hollowfen_stillworks", {"husk_keeper": "hollowing_elder"}),
        ],
    },
    # ---- Nightreach — the densest sky: star-glints, frequent streaks
    "nightreach_observatory": {
        "ambience": {"particles": [particles("starglint", 1.0)],
                     "tint": {"color": "#9fb0e8", "alpha": 0.04},
                     "starfall": {"min_s": 25, "max_s": 55}},
        "npcs": [
            # W-4: the pass-walker walked on ahead; the watchers' table is here
            {"id": "passwalker_nightreach", "at": {"tx": 11, "ty": 22}, "facing": "down",
             "sprite": "pass_walker", "movement": "static",
             "dialogue_ref": "script.passwalker_nightreach",
             "requires_flag": "flag:q_west_passmap"},
            *recast("nightreach_observatory", {
                "junior_watcher_a": "star_watcher", "junior_watcher_a_after": "star_watcher",
                "junior_watcher_working": "star_watcher", "junior_watcher_done": "star_watcher",
                "junior_watcher_round": "star_watcher", "junior_watcher_after2": "star_watcher",
                "festival_lunar_b": "lamplighter"}),
        ],
    },
    "nightreach_inn": {
        "ambience": {"particles": [particles("dust", 0.4)]},
        "npcs": recast("nightreach_inn", {"innkeeper": "innkeeper"}),
    },
    "nightreach_home": {"ambience": {"particles": [particles("dust", 0.3)]}},
    "nightreach_lumenary": {
        "ambience": {"particles": [particles("starglint", 0.5), particles("dust", 0.3)]},
        "npcs": recast("nightreach_lumenary", {"hall_keeper": "lamplighter"}),
    },
    "lanternway_nightreach": {
        "ambience": {"particles": [particles("starglint", 0.8), particles("glowmotes", 0.3)],
                     "starfall": {"min_s": 30, "max_s": 60}},
    },
}


# ------------------------------------------------------------- AFTER-GLEAM
# The Solarium and Nightreach answer their Gleams (src/game/content/regions/west.ts).
# Words only: `lit` twins share their original's tile, sheet and body; `talk`
# re-points keep the id (the vigil warden's staged stage).
SOLAR, LUNAR = "gleam:solar", "gleam:lunar"
add_words(PLACEMENTS, {
    "sunken_solarium": {
        "after": [lit("festival_goer", SOLAR, "npc.solarium_festival_goer_lit"),
                  lit("bread_sharer", SOLAR, "npc.solarium_bread_lit"),
                  lit("festival_kid", SOLAR, "npc.solarium_kid_lit")],
        # shares its tile with troupe_stilts' pre-stage placement: re-point, don't twin
        "talk": {"solarium_witness": "script.solarium_witness_staged"},
    },
    "sunken_solarium_lumenary": {"after": [
        lit("matron", SOLAR, "script.solarium_rest_lit"),
        lit("prompter", SOLAR, "npc.solarium_prompter_lit"),
        lit("hall_keeper", SOLAR, "npc.solarium_hall_keeper_lit"),
    ]},
    "nightreach_observatory": {
        "after": [lit("watcher_steps_a", LUNAR, "npc.nightreach_watcher_steps_a_lit"),
                  lit("watcher_steps_b", LUNAR, "npc.nightreach_watcher_steps_b_lit")],
        "talk": {"star_vigil_warden_after": "script.star_vigil_warden_staged"},
    },
    "nightreach_home": {"after": [lit("home_elder", LUNAR, "npc.nightreach_home_elder_lit"),
                                  lit("home_kid", LUNAR, "npc.nightreach_home_kid_lit")]},
    "nightreach_inn": {"after": [lit("innkeeper", LUNAR, "script.nightreach_inn_rest_lit"),
                                 lit("guest", LUNAR, "npc.nightreach_inn_guest_lit"),
                                 lit("watcher_off_shift", LUNAR, "npc.nightreach_inn_watcher_lit")]},
    "nightreach_lumenary": {"after": [lit("hall_keeper", LUNAR, "npc.nightreach_hall_keeper_lit")]},
})
