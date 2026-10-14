#!/usr/bin/env python3
"""
Driftholm — the island town of the Farlamp Isles (walkthrough/10 Part I, §3 I5 +
§4). World position (-83,-30), 32x30, north-up.

A town of lamp-keepers and kelp-farmers that hasn't seen a boat in eleven
winters. It lived in the Farlamp's light; when the deep came up and the lamp
drowned, the fog closed over it, and Driftholm kept small lamps alone and threw
letters into the sea (the five driftletters).

You arrive by sea from the Fogwall's lantern-buoy lane: the harbour opens across
the whole north edge (the seam with `farlamp_fogwall`'s south row — this builder
writes BOTH sides of it, mirrored from the Fogwall's own shipped south-edge
warps so the two never drift).

Three signature touches (level-design §8):
  1. THE WELL-STAIR (centre of the square): an old well-head whose south side is
     cut into steps — down to the Undertide's Bell Galleries. Chained shut until
     Elder Nan Creel opens it (`flag:q_isles_wellstair`; the warp at (16,12),
     contract, answers with her script until then).
  2. THE QUAY + BOATHOUSE: the harbour's stone quay with boats moored dry for
     eleven winters, the tarred boathouse at its west end.
  3. THE LAMP-STONE (TRAVEL waystone) by the quay steps — the way home is one
     menu away (content/waystones.ts).

Standing kit: the inn (rest point; `driftholm_inn` is in WorldScene's
HEAL_ENTRANCE_MAPS), the chandlery (shop; the Deep Charm after the isles'
dawn), the elder's house, the boathouse, the Letters Home writers, and keeper
Bram Fathom (the isles' super-trainer) on the quay's end. Day-forms after
`flag:isles_dawn`: the fog banks lift (hidden_when_flag), townsfolk move out
into the morning (flag-pair NPC swaps), `music_when` in maps.ts -> driftholm-dawn.

Run:  python3 tools/maps/build_driftholm.py   (after build_farlamp_isles.py)
"""
from __future__ import annotations

import sys

import mapkit as mk
from mapkit import gid
from farlamp_kit import Sea, sea_ambience, load_shipped, ISLE_BACKDROPS

W, H = 32, 30
DAWN = "flag:isles_dawn"
WELL = (15, 10)                 # 2x2 well-head; its stair = the warp tile below it
WELL_WARP = (16, 12)            # contract: to_wellstair @ (16,12) -> undertide_iii (15,28)
WELL_LANDING = (16, 13)         # contract: undertide_iii's return lands here, facing down

# building doors -> interior landings (each interior's builder pairs them back)
INN = (2, 11)                   # 6x6, 2-wide door at cols 2-3
CHANDLERY = (19, 9)             # 6x5, door col 3
ELDER = (14, 20)                # 7x4, door col 3
BOATHOUSE = (2, 5)              # 7x5, 2-wide door at cols 2-3
KEEPHOUSE = (8, 19)             # 5x7, door col 2 (Edda Quill's schoolhouse-home; not enterable)
COTTAGE_A = (23, 15)            # 5x5, door col 2 (Marra's; latched)
COTTAGE_B = (22, 21)            # 5x5, door col 2 (Hesk's; latched)


def door(at, col, h):
    return (at[0] + col, at[1] + h - 1)


def build() -> Sea:
    s = Sea("driftholm", "Driftholm", W, H, seed=1777, kind="town",
            music="assets/audio/music/driftholm.mp3", backdrops=ISLE_BACKDROPS, sea=False)
    # ---- the harbour + the island ---------------------------------------------
    mk.rect(s.water, W, H, 0, 0, W - 1, 5)
    mk.blob(s.water, W, H, 16, 6.2, 7.5, 1.6)           # the harbour's bite into the shore
    mk.blob(s.water, W, H, 27.5, 5.5, 3.0, 2.0)
    for (x, y) in [(x, y) for y in range(0, 10) for x in range(0, 10)]:
        if y >= 4:
            s.water[s.cell(x, y)] = 0                   # the boathouse spit (land)
    # the shore: a sand rim along the harbour, a stone quay over it
    for y in range(0, 12):
        for x in range(W):
            i = s.cell(x, y)
            if not s.water[i] and any(0 <= y + d < H and s.water[s.cell(x, y + d)]
                                      for d in (-1, -2)):
                s.sand[i] = 1
    # east: the cliffs over Kelpcrown's sound (no road there); west: the island's
    # wooded back; south: the crown wood
    for y in range(H):
        x0 = 29 if (y // 4) % 2 else 30
        for x in range(x0, W):
            s.cliff[s.cell(x, y)] = 1
            s.water[s.cell(x, y)] = 0
    s.organic = mk.make_grid(W, H)
    mk.organic_border(s.tree, W, H, left=1, depth=2,
                      bumps=[(1, 14, 2), (2, 22, 2), (1, 27, 2)], rng=s.rng)
    mk.rect(s.tree, W, H, 0, 27, W - 1, H - 1)
    for (bx, by, br) in ((4, 25, 2), (28, 25, 1)):
        mk.blob(s.tree, W, H, bx, by, br + 0.5, br)
    for y in range(0, 5):
        for x in range(0, 2):
            s.tree[s.cell(x, y)] = 0
    for y in range(5, 11):
        s.tree[s.cell(0, y)] = 1
    # ---- the lanes: the quay, the square, a lane to each door -------------------
    P = set()
    P |= {(x, 8) for x in range(9, 28)}                  # the quay
    P |= {(x, y) for y in range(12, 18) for x in range(12, 21)
          if ((x - 16) / 4.6) ** 2 + ((y - 14.5) / 3.0) ** 2 <= 1}   # the square
    P |= {(16, y) for y in range(9, 12)} | {(15, 12)}
    P |= {(x, 17) for x in range(4, 13)} | {(4, 18)}     # inn lane
    P |= {(x, 10) for x in range(4, 10)} | {(9, y) for y in range(8, 11)}  # boathouse apron
    P |= {(22, y) for y in range(14, 16)} | {(x, 15) for x in range(19, 23)}
    P |= {(17, y) for y in range(18, 24)}                # elder's lane
    P |= {(x, 20) for x in range(18, 26)} | {(25, y) for y in range(20, 21)}
    P |= {(24, y) for y in range(21, 28)} if False else set()
    P |= {(10, y) for y in range(18, 27)} if False else set()
    for (x, y) in P:
        i = s.cell(x, y)
        if not s.water[i] and not s.cliff[i]:
            s.path[i] = 1
            s.tree[i] = 0
            s.sand[i] = 0

    # ---- buildings ------------------------------------------------------------------
    def bld(oid, sprite, at, w, h, overhang, cols, to_map=None, to=None, locked=None):
        s.obj(oid, sprite, at, w, h, overhang=overhang)
        for c in cols:
            d = door(at, c, h)
            if to_map:
                s.m["warps"].append({"id": f"enter_{oid}" + (f"_{c}" if len(cols) > 1 else ""),
                                     "at": {"tx": d[0], "ty": d[1]}, "trigger": "step_on",
                                     "to_map": to_map, "to": {"tx": to[0], "ty": to[1]},
                                     "facing": "up", "transition": "door"})
            elif locked:
                s.m["triggers"].append({"id": f"door_{oid}", "kind": "sign",
                                        "at": {"tx": d[0], "ty": d[1]},
                                        "activation": "interact", "ref": locked})
                s.owed.append(locked)
            ap = (d[0], d[1] + 1)
            s.path[s.cell(*ap)] = 1
            s.tree[s.cell(*ap)] = 0
            s.sand[s.cell(*ap)] = 0
    bld("inn", "farlamp_inn", INN, 6, 6, 3, (2, 3), "driftholm_inn", (8, 10))
    bld("chandlery", "farlamp_chandlery", CHANDLERY, 6, 5, 2, (3,), "driftholm_chandlery", (7, 8))
    bld("elder", "farlamp_elder", ELDER, 7, 4, 2, (3,), "driftholm_elder", (7, 8))
    bld("boathouse", "farlamp_boathouse", BOATHOUSE, 7, 5, 2, (2, 3), "driftholm_boathouse", (8, 8))
    bld("keephouse", "farlamp_keephouse", KEEPHOUSE, 5, 7, 4, (2,), locked="sign.driftholm_schoolhouse")
    bld("cottage_a", "farlamp_cottage", COTTAGE_A, 5, 5, 2, (2,), locked="sign.driftholm_cottage_marra")
    bld("cottage_b", "farlamp_cottage_b", COTTAGE_B, 5, 5, 2, (2,), locked="sign.driftholm_cottage_hesk")
    # lanes into the south-side doors
    # (a south lane, row 26, joins the three south doors; two lanes drop to it
    # either side of the elder's house)
    for (x, y) in ([(x, 26) for x in range(9, 26)] + [(13, y) for y in range(18, 27)] +
                   [(21, y) for y in range(17, 27)] + [(x, 20) for x in range(21, 26)]):
        i = s.cell(x, y)
        if 0 <= x < W and 0 <= y < H and not s.cliff[i]:
            covered = any(o["at"]["tx"] <= x < o["at"]["tx"] + o["w"] and
                          o["at"]["ty"] <= y < o["at"]["ty"] + o["h"] for o in s.m["objects"])
            if not covered:
                s.path[i] = 1
                s.tree[i] = 0

    # ---- THE WELL-STAIR (contract) --------------------------------------------------
    s.obj("well_shut", "farlamp_well_shut", WELL, 2, 2, hidden_when_flag="flag:q_isles_wellstair")
    s.obj("well_open", "farlamp_well_open", WELL, 2, 2, requires_flag="flag:q_isles_wellstair")
    s.obj("well_steps", "markers_steps_s", WELL_WARP, 1, 1, solid=False,
          requires_flag="flag:q_isles_wellstair")
    s.m["warps"].append({"id": "to_wellstair", "at": {"tx": WELL_WARP[0], "ty": WELL_WARP[1]},
                         "trigger": "step_on", "to_map": "undertide_iii",
                         "to": {"tx": 15, "ty": 28}, "facing": "up", "transition": "fade",
                         "requires_flag": "flag:q_isles_wellstair",
                         "blocked_ref": "script.creel_well_locked"})
    s.owed.append("script.creel_well_locked")
    s.path[s.cell(*WELL_WARP)] = 1

    # ---- the lamp-stone (TRAVEL waystone) + the quay ---------------------------------
    s.obj("waystone", "farlamp_waystone", (12, 9), 1, 2)
    s.m["triggers"].append({"id": "waystone", "kind": "sign", "at": {"tx": 12, "ty": 10},
                            "activation": "interact", "ref": "sign.driftholm_waystone"})
    s.owed.append("sign.driftholm_waystone")
    for (oid, x, y) in (("boat_a", 11, 5), ("boat_b", 20, 5), ("boat_c", 24, 4)):
        s.obj(oid, "pearlmoor_boat", (x, y), 2, 3)
    s.obj("quay_lamp_a", "tinderwick_lamp_post", (14, 6), 1, 3, overhang=2, walk_under=True)
    s.obj("quay_lamp_b", "tinderwick_lamp_post", (23, 6), 1, 3, overhang=2, walk_under=True)
    s.obj("quay_bell", "pearlmoor_moorbell", (27, 6), 2, 3, overhang=1)
    s.obj("quay_pots", "pearlmoor_crab_pots", (18, 7), 1, 1)
    s.obj("quay_crates", "pearlmoor_fish_crates", (19, 7), 1, 1)
    s.obj("quay_net", "pearlmoor_net_rack", (25, 9), 2, 1)
    s.obj("spit_slip", "farlamp_slip", (8, 3), 2, 3, solid=False, bob=False)
    for x in (8, 9):
        for y in (3, 4, 5):
            s.water[s.cell(x, y)] = 0
            s.sand[s.cell(x, y)] = 1
    # the square: a fish stall, a lantern string, kelp racks along the west shore
    s.obj("square_stall", "pearlmoor_fish_stall", (12, 14), 3, 3, overhang=1)
    s.obj("square_lanterns", "pearlmoor_lantern_string", (17, 15), 3, 2, solid=False, overhang=2)
    s.obj("kelp_rack_a", "farlamp_kelp_rack", (2, 18), 2, 2)
    s.obj("kelp_rack_b", "farlamp_kelp_rack", (5, 20), 2, 2)
    s.obj("kelp_rack_c", "farlamp_kelp_rack", (27, 12), 2, 2)
    s.obj("lane_lamp_a", "tinderwick_lamp_post", (11, 17), 1, 3, overhang=2, walk_under=True)
    s.obj("lane_lamp_b", "tinderwick_lamp_post", (18, 17), 1, 3, overhang=2, walk_under=True)
    s.obj("tree_a", "tinderwick_tree_b", (26, 17), 3, 4, overhang=3, walk_under=True)
    s.obj("tree_b", "windward_bent_pine", (14, 24), 2, 3, overhang=2, walk_under=True)
    s.obj("tree_c", "windward_bent_pine", (6, 22), 2, 3, overhang=2, walk_under=True)
    s.obj("wood", "tinderwick_woodpile", (8, 16), 2, 1)
    s.sign("driftholm", (13, 11))
    # the harbour fog (lifts at the isles' dawn)
    for i, (x, y, big) in enumerate(((2, 0, 1), (13, 1, 0), (20, 0, 1), (26, 2, 0))):
        s.obj(f"fogbank_{i}", "farlamp_fogbank_a" if big else "farlamp_fogbank_b",
              (x, y), 4 if big else 3, 2, solid=False, hidden_when_flag=DAWN)

    # ---- people ------------------------------------------------------------------------
    N = s.npc
    # the arrival (I5): the first step off the quay steps — the whole town turns out.
    # A band across every walkable tile of the quay's landing row, once.
    for x in range(9, 28):
        if not s.passable(x, 8):          # lamp bases, the mooring bell: no dead band tiles
            continue
        s.m["triggers"].append({"id": f"arrival_{x}", "kind": "cutscene",
                                "at": {"tx": x, "ty": 8}, "activation": "step_on",
                                "ref": "script.driftholm_arrival",
                                "hidden_when_flag": "flag:q_isles_driftholm"})
    s.owed.append("script.driftholm_arrival")
    # Bram Fathom, keeper, on the quay's end by the mooring bell
    N("bram", (27, 9), "old_salt", "script.bram_fathom", facing="left")
    # the Letters Home writers (each reads her/his own letter back)
    N("marra_night", (4, 19), "fisher_woman", "script.letter_home_1", facing="right",
      movement="look_around", hidden_when_flag=DAWN)
    N("marra_day", (3, 4), "fisher_woman", "script.letter_home_1", facing="down",
      movement="look_around", requires_flag=DAWN)
    N("tobin", (13, 10), "lamplighter", "script.letter_home_2", facing="left")
    N("edda_night", (12, 26), "npc_woman", "script.letter_home_3", facing="up",
      movement="look_around", hidden_when_flag=DAWN)
    N("edda_day", (15, 16), "npc_woman", "script.letter_home_3", facing="down",
      movement="look_around", requires_flag=DAWN)
    N("hesk", (25, 26), "fisher_man", "script.letter_home_4", facing="up",
      movement="look_around")
    # the island's children: indoors-quiet before the dawn, out on the quay after
    N("child_night", (18, 13), "village_child", "npc.driftholm_child", facing="down",
      hidden_when_flag=DAWN)
    N("child_day", (21, 8), "village_child", "npc.driftholm_child_day", facing="down",
      movement="wander", wander_radius=2, requires_flag=DAWN)
    N("kelper", (6, 18), "fen_folk", "npc.driftholm_kelper", facing="left",
      movement="look_around")
    N("cat", (9, 15), "cottage_cat", "npc.driftholm_cat", facing="down")
    s.owed += ["script.bram_fathom", "script.letter_home_1", "script.letter_home_2",
               "script.letter_home_3", "script.letter_home_4", "npc.driftholm_child",
               "npc.driftholm_child_day", "npc.driftholm_kelper", "npc.driftholm_cat"]
    s.kin("amb_hermiwick", (4, 7), 174, radius=1)

    # ---- the Fogwall seam: mirror the Fogwall's own south-edge warps --------------------
    fog = load_shipped("farlamp_fogwall")
    for w in fog["warps"]:
        if w.get("to_map") == "driftholm":
            x = w["at"]["tx"]
            s.m["warps"].append({"id": f"to_fogwall_{x}", "at": {"tx": x, "ty": 0},
                                 "trigger": "step_on", "to_map": "farlamp_fogwall",
                                 "to": {"tx": x, "ty": fog["height"] - 2}, "facing": "up",
                                 "transition": "fade"})
    s.m["ambience"] = sea_ambience(flocks=[(5, 6), (26, 10)],
                                   lights=[(12, 9, 12, "#ffd089"), (16, 11, 14, "#ffb35a")])
    return s


if __name__ == "__main__":
    s = build()
    s.assemble()
    s.scatter(0.08)
    ok = s.finalize()
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
