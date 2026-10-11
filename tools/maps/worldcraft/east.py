"""EAST world-craft placements (owned by this region's package — WP3).

PLACEMENTS: map id -> spec (keys documented in _kit.py). Applied by
`python3 tools/maps/add_world_craft.py --region east`.

What rides here (the recomposed Saltreach Fen I's props/beats live in its
builder; this module only layers on top of the shipped JSONs):
  * ambience for every East map — fen mist + spray, Lowleaf glowmotes/spores,
    Glowmoss deep motes + a green-gold wash, Spore Grotto spores, Cinderhead
    ash/embers + drips; ambient kin from each map's OWN encounter table;
  * the regional cast swap (fen_folk, hollow_gardener, miner_*, hollowing_*,
    innkeeper, market_trader, lamplighter) — sprite field only, ids/refs kept;
  * Fen II / Sunkbell / Lanternway props (lighter lift, decor only, non-solid
    in water so Tidecall swims are never blocked);
  * story placements: E-1 the acolyte's dropped cinder (Glowmoss), E-2 Wren's
    acted A3 (script ref swap), E-3 Harl's eight hooks + the roof-fault cinder
    (Cinderhead), the B1F acolyte at a doused lantern, the B2F miner.
"""
from __future__ import annotations

import json
from pathlib import Path

from ._kit import ambient_kin, gid, particles  # noqa: F401

_MAPS = Path(__file__).resolve().parents[3] / "public" / "assets" / "maps"


def restyle(mid: str, changes: dict[str, dict]) -> list[dict]:
    """Copies of the shipped NPCs `changes` names, with the given fields
    replaced (a sprite swap / ref swap that keeps id, tile and flags)."""
    m = json.loads((_MAPS / f"{mid}.json").read_text())
    out = []
    for n in m.get("npcs", []):
        if n["id"] in changes:
            c = dict(n)
            c.update(changes[n["id"]])
            out.append(c)
    missing = set(changes) - {n["id"] for n in out}
    if missing:
        raise SystemExit(f"east.restyle: {mid} has no NPC(s) {sorted(missing)}")
    return out


def sprite(*ids: str, to: str) -> dict[str, dict]:
    return {i: {"sprite": to} for i in ids}


def obj(oid, spr, at, w, h, **kw) -> dict:
    o = {"id": oid, "sprite": spr, "at": {"tx": at[0], "ty": at[1]}, "w": w, "h": h}
    o.update(kw)
    return o


def decor(oid, spr, at, w, h) -> dict:
    """Non-solid set-dressing (reeds, lily-pads, drowned lamps): never blocks."""
    kw = {"solid": False}
    if h > 1 and spr not in ("saltreach_lilypads", "saltreach_punt"):
        kw.update(overhang=h - 1, walk_under=True)
    return obj(oid, spr, at, w, h, **kw)


def npc(nid, at, spr, ref, facing="down", **kw) -> dict:
    n = {"id": nid, "at": {"tx": at[0], "ty": at[1]}, "facing": facing, "sprite": spr,
         "movement": "static", "dialogue_ref": ref}
    n.update(kw)
    return n


FEN_AMB = {
    "particles": [particles("spray", 0.5), particles("glowmotes", 0.35)],
    "mist": {"color": "#a8c8c0", "alpha": 0.16, "speed": 6},
    "starfall": {"min_s": 45, "max_s": 100},
    "sound_bed": "amb-marsh",
}

PLACEMENTS: dict[str, dict] = {
    # --- Saltreach Fen I: the richness pilot. Props/beats ride its builder; here
    # the air (mist, spray, motes), the herons on the open flat, and two of the
    # fen's own kin grazing off the lane.
    "saltreach_fen_i": {
        "ambience": {**FEN_AMB, "birds": {"kind": "bird", "flocks": [{"tx": 25, "ty": 24}],
                                          "flyover": True},
                     "bob_gids": [gid("buoy")]},
        "npcs": [ambient_kin("amb_dewling", (24, 23), 59, radius=2),
                 ambient_kin("amb_poolfrond", (4, 33), 60, radius=1)],
    },
    # --- Saltreach Fen II: the moon-channels — reeds and pads round the square
    # pond corners, eel traps, a drowned lamp pair, the fisher's punt.
    "saltreach_fen_ii": {
        "ambience": {**FEN_AMB, "bob_gids": [gid("buoy")]},
        "objects": [
            decor("lily_a", "saltreach_lilypads", (8, 17), 2, 2),
            decor("lily_b", "saltreach_lilypads", (24, 18), 2, 2),
            decor("lily_c", "saltreach_lilypads", (5, 31), 2, 2),
            decor("lily_d", "saltreach_lilypads", (20, 34), 2, 2),
            decor("lily_e", "saltreach_lilypads", (26, 10), 2, 2),
            decor("reeds_a", "saltreach_cattails", (9, 11), 2, 2),
            decor("reeds_b", "saltreach_cattails", (17, 11), 2, 2),
            decor("reeds_c", "saltreach_cattails", (2, 25), 2, 2),
            decor("reeds_d", "saltreach_cattails", (13, 26), 2, 2),
            decor("reeds_e", "saltreach_cattails", (8, 37), 2, 2),
            decor("reeds_f", "saltreach_cattails", (22, 37), 2, 2),
            decor("reeds_g", "saltreach_cattails", (28, 13), 2, 2),
            decor("reeds_h", "saltreach_cattails", (3, 3), 2, 2),
            decor("reeds_i", "saltreach_cattails", (13, 19), 2, 2),
            decor("reeds_j", "saltreach_cattails", (20, 21), 2, 2),
            decor("isle_stooks", "saltreach_reed_stooks", (14, 21), 2, 2),
            decor("eel_trap_a", "saltreach_eel_trap", (20, 12), 2, 2),
            decor("eel_trap_b", "saltreach_eel_trap", (11, 31), 2, 2),
            decor("drowned_lamp_a", "saltreach_sunken_lamp", (24, 20), 1, 3),
            decor("drowned_lamp_b", "saltreach_sunken_lamp", (27, 22), 1, 3),
            decor("fisher_punt", "saltreach_punt", (22, 28), 2, 3),
            decor("fisher_moorings", "saltreach_mooring_posts", (21, 25), 1, 2),
        ],
        "npcs": restyle("saltreach_fen_ii", {
            **sprite("fen_fisher", "fen_fisher_wait", "fen_fisher_report", "fen_fisher_after",
                     to="fen_folk"),
            **sprite("reed_lamplighter", "reed_lamplighter_after", to="lamplighter"),
        }) + [ambient_kin("amb_lumpin", (9, 40), 31, radius=2),
              ambient_kin("amb_brineroll", (12, 5), 27, radius=2)],
    },
    # --- Sunkbell Shallows: the half-flooded shrine — drowned lamps leading in,
    # pads on the still water, reeds at the steps.
    "sunkbell_shallows": {
        "ambience": {**FEN_AMB, "particles": [particles("spray", 0.35),
                                              particles("glowmotes", 0.5)],
                     "mist": {"color": "#b8d4e0", "alpha": 0.2, "speed": 4}},
        "objects": [
            decor("lily_a", "saltreach_lilypads", (3, 10), 2, 2),
            decor("lily_b", "saltreach_lilypads", (15, 3), 2, 2),
            decor("lily_c", "saltreach_lilypads", (8, 12), 2, 2),
            decor("reeds_a", "saltreach_cattails", (13, 5), 2, 2),
            decor("reeds_b", "saltreach_cattails", (2, 3), 2, 2),
            decor("drowned_lamp_a", "saltreach_sunken_lamp", (5, 9), 1, 3),
            decor("drowned_lamp_b", "saltreach_sunken_lamp", (16, 9), 1, 3),
            decor("moorings", "saltreach_mooring_posts", (6, 11), 1, 2),
        ],
    },
    # --- Lowleaf Hollow: the Bloom — glowmotes and drifting spores over the
    # festival; the town's own kin drifting by the ferns; the regional cast.
    "lowleaf_hollow": {
        "ambience": {"particles": [particles("glowmotes", 0.9), particles("spores", 0.4)],
                     "starfall": {"min_s": 50, "max_s": 110}, "sound_bed": "amb-crickets"},
        "npcs": restyle("lowleaf_hollow", {
            **sprite("kilner_pre", "kilner_fire", "kilner_after", to="hollow_gardener"),
            **sprite("stall_quest", "stall_waiting", "stall_reward", "stall_after",
                     to="market_trader"),
            **sprite("fern_kid", to="village_child"),
            **sprite("bloom_crier", to="road_courier"),
            **sprite("bloom_warden_a", "bloom_warden_a_after", to="fen_folk"),
        }) + [ambient_kin("amb_fennlight", (3, 17), 67, radius=1),
              ambient_kin("amb_sporeling", (24, 28), 65, radius=2)],
    },
    "lowleaf_bower": {
        "npcs": restyle("lowleaf_bower", sprite("bower_keeper", to="innkeeper")),
    },
    # --- Lanternway (Lowleaf spoke): lamps along the lit road + two old trees.
    "lanternway_lowleaf": {
        "ambience": {"particles": [particles("glowmotes", 0.4)]},
        "objects": [
            obj("spoke_lamp_a", "tinderwick_lamp_post", (12, 8), 1, 3, overhang=2, walk_under=True),
            obj("spoke_lamp_b", "tinderwick_lamp_post", (8, 22), 1, 3, overhang=2, walk_under=True),
            obj("spoke_tree_a", "tinderwick_tree", (2, 13), 3, 4, overhang=3, walk_under=True),
            obj("spoke_tree_b", "tinderwick_tree", (20, 22), 3, 4, overhang=3, walk_under=True),
            decor("spoke_reeds_a", "saltreach_cattails", (5, 15), 2, 2),
            decor("spoke_reeds_b", "saltreach_cattails", (15, 19), 2, 2),
            decor("spoke_stooks", "saltreach_reed_stooks", (10, 25), 2, 2),
        ],
    },
    "lanternway_undercut": {
        "ambience": {"particles": [particles("dust", 0.4)], "sound_bed": "amb-drips"},
    },
    # --- Glowmoss Deep: the first dungeon — motes in a green-gold wash; the
    # cast swap (the Hollowing in its own robes); E-1's dropped cinder (seen
    # after the relight; wakes to a shard at dawn); E-2 Wren acted.
    "glowmoss_deep": {
        "ambience": {"particles": [particles("glowmotes", 0.8)],
                     "tint": {"color": "#9fe8b8", "alpha": 0.06}, "sound_bed": "amb-drips"},
        "npcs": restyle("glowmoss_deep", {
            **sprite("acolyte_a", "acolyte_b", to="hollowing_acolyte"),
            **sprite("cowled_figure", to="hollowing_elder"),
            **sprite("glowmoss_keeper_a", "glowmoss_keeper_a_after", to="hollow_gardener"),
            **sprite("glowmoss_keeper_b", "glowmoss_keeper_b_after", to="lamplighter"),
            "wren_glowmoss": {"dialogue_ref": "script.wren_glowmoss"},
        }) + [ambient_kin("amb_glimmoth", (7, 20), 56, radius=1)],
        "objects": [
            obj("acolyte_cinder", "fallenstar_cinder_star", (20, 8), 2, 2, solid=False,
                requires_flag="flag:met_hollowing", hidden_when_flag="flag:dawn"),
            obj("acolyte_cinder_woken", "vigil_star_shard", (20, 8), 2, 2, solid=False,
                requires_flag="flag:dawn"),
            # E-1: the star that comes back, seen through the root-gap over the chamber
            obj("root_gap_star", "penumbra_starglint_bright_a", (19, 5), 1, 1, solid=False,
                requires_flag="flag:glowmoss_star_back"),
            obj("root_gap_star_b", "nightreach_starglint_a", (21, 4), 1, 1, solid=False,
                requires_flag="flag:glowmoss_star_back"),
        ],
        "triggers": [
            {"id": "acolyte_cinder", "kind": "script", "at": {"tx": 20, "ty": 9},
             "activation": "interact", "ref": "script.glowmoss_cinder"},
            {"id": "acolyte_cinder_e", "kind": "script", "at": {"tx": 21, "ty": 9},
             "activation": "interact", "ref": "script.glowmoss_cinder"},
        ],
    },
    # --- Glowmoss B1F: an acolyte sits with a doused null-lantern (after the
    # relight; gone by dawn); a Fennlight drifts by the ladder.
    "glowmoss_deep_b1f": {
        "ambience": {"particles": [particles("glowmotes", 0.6)],
                     "tint": {"color": "#9fe8b8", "alpha": 0.05}, "sound_bed": "amb-drips"},
        "objects": [obj("doused_lantern", "glowmoss_deep_null_lantern_shrine", (9, 9), 2, 3,
                        overhang=1)],
        "npcs": [npc("b1f_acolyte", (9, 12), "hollowing_acolyte", "script.b1f_acolyte",
                     facing="up", requires_flag="flag:met_hollowing",
                     hidden_when_flag="flag:dawn"),
                 ambient_kin("amb_fennlight", (20, 5), 67, radius=1)],
    },
    "spore_grotto": {
        "ambience": {"particles": [particles("spores", 1.0), particles("glowmotes", 0.3)],
                     "sound_bed": "amb-drips"},
        "npcs": [ambient_kin("amb_sporeling", (13, 7), 65, radius=1)],
    },
    "gloamwood_dell": {
        "ambience": {"particles": [particles("glowmotes", 0.6)],
                     "starfall": {"min_s": 40, "max_s": 90}},
    },
    # --- Cinderhead Mine: ash + embers under the lamps, the cast in pit-gear,
    # E-3: Harl's eight hooks (seven lamps, one empty) on the west terrace and
    # the roof-fault cinder with the miner who won't move it.
    "cinderhead_mine": {
        "ambience": {"particles": [particles("ash", 0.6), particles("embers", 0.3)],
                     "sound_bed": "amb-drips",
                     "light_sources_extra": [{"at": {"tx": 23, "ty": 11}, "radius": 14,
                                              "color": "#9fc4ff"}]},
        "npcs": restyle("cinderhead_mine", {
            **sprite("vigil_miner_a", to="miner_man"),
            **sprite("vigil_miner_b", to="miner_woman"),
            **sprite("vigil_cook", to="innkeeper"),
            **sprite("provisioner_kit", "provisioner", to="market_trader"),
        }) + [npc("fault_miner", (24, 12), "miner_woman", "script.cinderhead_fault_miner",
                  facing="left", movement="look_around")],
        "objects": [
            # the miners' row cottages replace the Tinderwick stand-ins (same footprint)
            obj("cottage_a", "cinderhead_miner_cottage", (2, 15), 5, 5, overhang=3),
            obj("cottage_b", "cinderhead_miner_cottage", (20, 3), 5, 5, overhang=3),
            obj("harl_hooks", "cinderhead_lamp_hooks", (7, 18), 5, 2, overhang=1,
                walk_under=True),
            obj("fault_cinder", "fallenstar_cinder_star", (22, 10), 2, 2, solid=False,
                hidden_when_flag="flag:dawn"),
            obj("fault_cinder_woken", "vigil_star_shard", (22, 10), 2, 2, solid=False,
                requires_flag="flag:dawn"),
        ],
        "triggers": [
            {"id": "harl_hooks", "kind": "sign", "at": {"tx": 9, "ty": 19},
             "activation": "interact", "ref": "sign.cinderhead_hooks"},
            {"id": "fault_cinder", "kind": "script", "at": {"tx": 22, "ty": 11},
             "activation": "interact", "ref": "script.cinderhead_fault_cinder"},
        ],
    },
    "cinderhead_deep": {
        "ambience": {"particles": [particles("ash", 0.5), particles("embers", 0.2)],
                     "sound_bed": "amb-drips"},
        "npcs": restyle("cinderhead_deep", {
            **sprite("sealed_miner", to="npc_old_man"),
            **sprite("gallery_miner_a", "gallery_miner_a_after", to="miner_man"),
        }),
    },
    "cinderhead_deep_b1f": {
        "ambience": {"particles": [particles("ash", 0.4), particles("embers", 0.2)],
                     "sound_bed": "amb-drips"},
        "npcs": restyle("cinderhead_deep_b1f",
                        sprite("gallery_miner_b", "gallery_miner_b_after", to="miner_woman")),
    },
    # --- Cinderhead Deep B2F: the third gallery — Cass, who comes down to listen
    # to the vigil-lamp, and an abandoned ore-cart.
    "cinderhead_deep_b2f": {
        "ambience": {"particles": [particles("embers", 0.35), particles("ash", 0.3)],
                     "sound_bed": "amb-drips"},
        "objects": [obj("b2f_ore_cart", "cinderhead_ore_cart", (7, 12), 2, 2, overhang=1,
                        walk_under=True)],
        "npcs": [npc("b2f_miner", (15, 12), "miner_woman", "script.b2f_miner", facing="left")],
    },
}
