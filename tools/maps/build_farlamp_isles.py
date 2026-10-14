#!/usr/bin/env python3
"""
The Farlamp Isles — the SEA and the two wild ISLES (walkthrough/10 Part I, §4).
Driftholm is its own builder (build_driftholm.py); the Undertide caves are Lane
C2's (they meet these maps at the contract cave mouths).

Five maps at their exact world positions (world_geometry, north-up):

  farlamp_sound       (-21,-69) 27x33  the deep under the lighthouse. North edge
                      x0-19 = Lightkeeper's Point's south edge (the launch slip);
                      west edge rows 3-32 = the Shelfwater's east; south = Gullwrack.
  farlamp_shelfwater  (-51,-66) 30x30  reef flats + the sunken hull. North edge =
                      the Wick-Run Foot's beach (the second launch); west = the
                      Fogwall; south = Kelpcrown.
  farlamp_fogwall     (-83,-66) 32x36  the sea-fog. A turn-round band at row 13
                      until `flag:q_isles_fogglass`; with the glass a lantern-buoy
                      lane leads south to Driftholm. The far lamp blinks here.
  farlamp_gullwrack   (-21,-36) 27x34  gull-cliffs, ledges, sea-grass, the keeper's
                      hut (rest point), the Undertide I mouth (13,9).
  farlamp_kelpcrown   (-51,-36) 30x34  the old keepers' quarter in ruins, kelp
                      terraces, Tidecall pools, the Undertide II mouth (10,9).

The sea is rowed: open water is DEEP (the `deepdive` the Farlamp skiff grants);
every islet and coast keeps a two-tile shallow shelf (Tidecall). Density rule
(the expansion panel, v2): every 15x10 screen carries an islet, a wreck, a
trainer, a buoy-cache or an ambient kin.

Run:  python3 tools/maps/build_farlamp_isles.py
"""
from __future__ import annotations

import sys

import mapkit as mk
import warp_markers as wm
from mapkit import gid
from farlamp_kit import (Sea, link, warp, sea_ambience, SEA_BACKDROPS, ISLE_BACKDROPS,
                         MUSIC_SEA)
from patterns import zones_from_grid

AFLOAT = "flag:q_isles_afloat"
GLASS = "flag:q_isles_fogglass"
DAWN = "flag:isles_dawn"


def T(*rows):
    return [{"kin_id": k, "weight": w, "min_level": lo, "max_level": hi} for (k, w, lo, hi) in rows]


# ---- encounter tables (mirrored in build_species.py EXTRA_ENCOUNTERS) ---------------
TABLES = {
    "farlamp_sound": {
        "deep": T((172, 35, 58, 61), (174, 20, 58, 60), (28, 15, 59, 61), (22, 12, 58, 61),
                  (30, 10, 59, 61), (32, 8, 58, 60)),
        "water": T((172, 40, 58, 60), (32, 30, 58, 60), (61, 30, 58, 60)),
        "grass": T((174, 45, 58, 60), (95, 30, 58, 61), (46, 25, 58, 60)),
    },
    "farlamp_shelfwater": {
        "deep": T((172, 35, 59, 62), (174, 20, 59, 61), (61, 15, 60, 62), (32, 15, 59, 62),
                  (28, 10, 60, 62), (173, 5, 61, 62)),
        "water": T((172, 40, 59, 61), (61, 30, 59, 61), (174, 30, 59, 61)),
    },
    "farlamp_fogwall": {
        "deep": T((176, 35, 60, 63), (172, 25, 60, 62), (85, 15, 61, 63), (79, 10, 60, 63),
                  (22, 10, 60, 62), (173, 5, 62, 63)),
        "water": T((176, 45, 60, 62), (172, 35, 60, 62), (85, 20, 61, 63)),
    },
    "farlamp_gullwrack": {
        "grass": T((174, 30, 60, 62), (95, 20, 60, 62), (76, 15, 60, 62), (52, 15, 60, 62),
                   (46, 15, 61, 62), (175, 5, 62, 62)),
        "water": T((172, 40, 60, 62), (28, 30, 60, 62), (30, 30, 60, 62)),
        "deep": T((172, 45, 60, 62), (174, 25, 60, 62), (28, 20, 60, 62), (30, 10, 61, 62)),
    },
    "farlamp_kelpcrown": {
        "grass": T((174, 25, 60, 63), (61, 20, 60, 62), (64, 15, 61, 63), (55, 15, 60, 62),
                   (36, 15, 60, 62), (175, 10, 62, 63)),
        "water": T((172, 35, 60, 62), (32, 35, 60, 62), (173, 15, 61, 63), (61, 15, 60, 62)),
        "deep": T((172, 45, 60, 63), (174, 25, 60, 62), (32, 20, 60, 62), (173, 10, 62, 63)),
    },
}


def sea_zones(s: Sea, *, deep_rate=0.06, water_rate=0.08, grass_rate=0.10):
    t = TABLES[s.id]
    zs = []
    if "deep" in t:
        zs.append({"id": f"{s.id}_deep", "terrain": "deep",
                   "rect": {"tx": 0, "ty": 0, "w": s.W, "h": s.H},
                   "encounter_rate": deep_rate, "requires_ability": "deepdive", "table": t["deep"]})
    if "water" in t:
        zs.append({"id": f"{s.id}_shallows", "terrain": "water",
                   "rect": {"tx": 0, "ty": 0, "w": s.W, "h": s.H},
                   "encounter_rate": water_rate, "requires_ability": "tidecall", "table": t["water"]})
    if "grass" in t and any(s.tallgrass):
        zs += zones_from_grid(s.tallgrass, s.W, s.H, terrain="tall_grass", rate=grass_rate,
                              table=t["grass"], id_prefix=f"{s.id}_grass")
    s.m["encounters"] = zs


def boulders(s: Sea, cells):
    for (x, y) in cells:
        s.deco[s.cell(x, y)] = gid("boulder")


def sea_rocks(s: Sea, cx, cy, n=3, spread=1.6):
    """A cluster of sea-stacks: boulders standing in the water (they collide)."""
    placed = 0
    for _ in range(40):
        if placed >= n:
            break
        x = int(round(cx + s.rng.uniform(-spread, spread)))
        y = int(round(cy + s.rng.uniform(-spread, spread)))
        if 0 < x < s.W - 1 and 0 < y < s.H - 1 and s.water[s.cell(x, y)] \
                and not s.deco[s.cell(x, y)]:
            s.deco[s.cell(x, y)] = gid("boulder")
            placed += 1


def tufts(s: Sea, grid, blobs):
    """Organic encounter grass: each (cx, cy, r) is a cluster of 3 small blobs."""
    for (cx, cy, r) in blobs:
        for _ in range(3):
            mk.blob(grid, s.W, s.H, cx + s.rng.uniform(-r * 0.6, r * 0.6),
                    cy + s.rng.uniform(-r * 0.4, r * 0.4),
                    r * s.rng.uniform(0.5, 0.8), r * s.rng.uniform(0.35, 0.6))


def blooms(s: Sea, cells):
    for (x, y) in cells:
        if not s.water[s.cell(x, y)] and not s.deco[s.cell(x, y)]:
            s.deco[s.cell(x, y)] = gid("flowerbed_a" if (x + y) % 2 else "flowerbed_b")


def skerry(s: Sea, cx, cy, rx=1.3, ry=0.9):
    """A black rock skerry: a scrap of shingle crowned with boulders."""
    s.islet(cx, cy, rx, ry)
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if 0 <= x < s.W and 0 <= y < s.H and not s.water[s.cell(x, y)] \
                    and (x + y) % 2 == 0:
                s.deco[s.cell(x, y)] = gid("boulder")


def sea_buoys(s: Sea, cells, prefix="buoy"):
    for i, (x, y) in enumerate(cells):
        s.obj(f"{prefix}_{i}", "markers_sea_buoy", (x, y), 1, 1, solid=False)


# =============================================================================
#  FARLAMP SOUND
# =============================================================================
def build_sound() -> Sea:
    s = Sea("farlamp_sound", "Farlamp Sound", 27, 33, seed=1772,
            backdrops=SEA_BACKDROPS)
    W, H = s.W, s.H
    # the mainland's sea-cliffs down the east side (the Dimglass headland's foot)
    def east(g):
        mk.rect(g, W, H, 25, 4, 26, H - 1)
        for (cx, cy, rx, ry) in ((24.6, 9, 1.4, 3.2), (24.4, 19, 1.6, 2.6), (24.8, 27, 1.2, 3.0)):
            mk.blob(g, W, H, cx, cy, rx, ry)
    cl = s.land(east)
    for i, v in enumerate(cl):
        if v:
            s.cliff[i] = 1
    # a sand strip at the cliff foot (the sea needs a sand shore), wider in two coves
    for y in range(5, H):
        for x in range(W - 1, 0, -1):
            if not s.cliff[s.cell(x, y)]:
                s.sand[s.cell(x, y)] = 1
                s.water[s.cell(x, y)] = 0
                break
    mk.blob(s.sand, W, H, 22.6, 14, 1.8, 2.4)                 # the cove (a cache)
    mk.blob(s.sand, W, H, 22.8, 24, 1.3, 1.6)
    for i, v in enumerate(s.sand):
        if v and not s.cliff[i]:
            s.water[i] = 0

    # A: Gannet Stack — a turfed stack, nesting gulls, a cache
    s.islet(5, 6.5, 3.2, 2.4, grass=0.5)
    # B: the wreck bar — a long sand bar, the ribs of a lost lamp-tender
    s.islet(17, 7.5, 3.6, 1.6)
    # C: Cormorant Holm — the boat-trainer's islet, a tall-grass heart
    s.islet(6.5, 17, 4.6, 3.3, grass=0.62)
    # D: the reef — little sand bars under the old buoy line
    for (cx, cy, rx, ry) in ((15, 14.4, 1.4, 0.9), (18.5, 16.5, 1.2, 0.8), (13, 21, 1.3, 0.9)):
        s.islet(cx, cy, rx, ry)
    # F: Tern Islet — the bent pine and the Sound's sign
    s.islet(9, 27, 4.2, 2.8, grass=0.55)
    # G: the anchor rock
    s.islet(19.5, 27.5, 2.4, 1.8)
    tufts(s, s.tallgrass, [(6.5, 17, 2.6)])
    blooms(s, [(8, 26), (10, 26), (6, 28), (3, 16), (9, 15)])
    for i in range(W * H):
        if s.water[i] or s.sand[i]:
            s.tallgrass[i] = 0

    boulders(s, [(3, 6), (4, 5), (7, 7), (15, 14), (18, 16), (12, 21), (21, 27), (20, 28),
                 (25, 3), (24, 2), (11, 28)])
    # the Quay's harbour wall runs on into the sea over the NE corner — nothing to
    # row into there (world_geometry: the Quay's last rows overlap ours as sea)
    for (x, y) in ((20, 0), (21, 1), (23, 0), (26, 1)):
        s.deco[s.cell(x, y)] = gid("buoy")

    s.obj("gannet_nest_a", "pearlmoor_gull_nest", (5, 5), 1, 1, solid=False)
    s.obj("gannet_nest_b", "pearlmoor_gull_nest", (6, 7), 1, 1, solid=False)
    s.cache("sound_stack", (4, 7))
    s.obj("wreck_ribs", "pearlmoor_wreck_ribs", (16, 7), 3, 2)
    s.obj("wreck_drift", "pearlmoor_driftwood", (19, 8), 2, 1, solid=False)
    s.kin("amb_tidwraith", (14, 8), 22, radius=1)
    s.trainer("sound_oarsman", (10, 18), "right", "fisher_man")
    s.obj("oarsman_boat", "pearlmoor_rowboat", (11, 19), 2, 2)
    s.obj("holm_crates", "pearlmoor_crab_pots", (4, 18), 1, 1)
    # the old buoy line across the reef — dark since the Long Dusk
    for i, (x, y) in enumerate(((12, 11), (16, 12), (20, 14), (16, 19), (11, 23))):
        s.obj(f"old_buoy_{i}", "farlamp_buoy_dark", (x, y - 1), 1, 2, solid=False)
    s.cache("sound_cove", (22, 14))
    s.obj("cove_drift", "pearlmoor_driftwood", (22, 16), 2, 1, solid=False)
    s.kin("amb_hermiwick", (22, 24), 174, radius=1)
    s.obj("tern_pine", "windward_bent_pine", (7, 25), 2, 3, overhang=2, walk_under=True)
    s.sign("farlamp_sound", (10, 28))
    s.obj("tern_net", "pearlmoor_net_rack", (11, 26), 2, 1)
    s.kin("amb_fathomote", (5, 28), 172, radius=1)
    s.obj("anchor_rock", "pearlmoor_anchor", (18, 26), 2, 2)
    sea_buoys(s, [(2, 12), (21, 21), (4, 31), (14, 31), (24, 30)])
    for (cx, cy, n) in ((1.5, 2.5, 2), (12, 3, 3), (2, 22, 3), (16, 30, 2), (22, 10.5, 2)):
        sea_rocks(s, cx, cy, n)
    s.m["ambience"] = sea_ambience(flocks=[(5, 6), (17, 7), (24, 12)])
    return s


# =============================================================================
#  THE SHELFWATER
# =============================================================================
def build_shelfwater() -> Sea:
    s = Sea("farlamp_shelfwater", "The Shelfwater", 30, 30, seed=1773,
            backdrops=SEA_BACKDROPS)
    W, H = s.W, s.H
    # the reef flats: a scatter of sand bars over a wide SHALLOW shelf (Tidecall)
    bars = [(6, 7, 1.6, 1.0), (9.5, 9.5, 1.2, 0.8), (4.5, 11, 1.3, 0.9), (11, 5.5, 1.2, 0.8),
            (24, 23, 1.3, 0.9), (26.5, 20, 1.0, 0.7), (21.5, 26, 1.4, 0.8)]
    for (cx, cy, rx, ry) in bars:
        s.islet(cx, cy, rx, ry)
    for y in range(3, 14):
        for x in range(2, 14):
            if ((x - 7.5) / 6.2) ** 2 + ((y - 8.5) / 5.0) ** 2 <= 1:
                s.no_deep.add((x, y))
    for y in range(18, 29):
        for x in range(19, 29):
            if ((x - 24) / 5.2) ** 2 + ((y - 23.5) / 4.6) ** 2 <= 1:
                s.no_deep.add((x, y))
    # the hull bank: where the lamp-tender HERON went down, her stern still out
    s.islet(20.5, 10.5, 3.0, 1.8, grass=0.0)
    # Skerry of the Oar: the boat-trainer's grassed islet
    s.islet(11, 20, 3.8, 2.6, grass=0.6)
    # the kelp holm, south-west
    s.islet(5, 23, 3.2, 2.2, grass=0.5)
    boulders(s, [(6, 6), (10, 10), (4, 12), (19, 11), (13, 21), (9, 19), (3, 22), (27, 20),
                 (25, 24), (16, 2), (1, 16)])
    s.obj("heron_stern", "coldfog_beached_boat", (19, 9), 3, 2)
    s.cache("shelf_hull", (22, 11))
    s.obj("heron_mast", "pearlmoor_wreck_ribs", (22, 8), 3, 2, solid=False)
    s.trainer("shelf_kelper", (13, 19), "right", "fisher_woman")
    s.obj("kelper_rack", "farlamp_kelp_rack", (9, 19), 2, 2)
    s.obj("kelp_rack_b", "farlamp_kelp_rack", (4, 22), 2, 2)
    s.cache("shelf_holm", (6, 23))
    s.kin("amb_hermiwick", (24, 22), 174, radius=1)
    s.kin("amb_lumplass", (5, 11), 32, radius=1)
    s.obj("reef_pots", "pearlmoor_crab_pots", (7, 7), 1, 1)
    s.obj("reef_drift", "pearlmoor_driftwood", (21, 26), 2, 1, solid=False)
    for i, (x, y) in enumerate(((15, 6), (17, 15), (8, 15), (14, 26))):
        s.obj(f"old_buoy_{i}", "farlamp_buoy_dark", (x, y - 1), 1, 2, solid=False)
    sea_buoys(s, [(2, 2), (27, 4), (26, 13), (2, 27), (17, 22)])
    for (cx, cy, n) in ((24, 3, 3), (15, 11, 2), (28, 16, 2), (18, 19, 3), (2, 18, 2), (13, 27, 2)):
        sea_rocks(s, cx, cy, n)
    s.m["ambience"] = sea_ambience(flocks=[(20, 10), (11, 20), (5, 23)])
    return s


# =============================================================================
#  THE FOGWALL
# =============================================================================
TURN_ROW = 13
FOG_RETURN = (29, 7)          # where the fog turns you round: back by the east edge


def build_fogwall() -> Sea:
    s = Sea("farlamp_fogwall", "The Fogwall", 32, 36, seed=1774, backdrops=SEA_BACKDROPS)
    W, H = s.W, s.H
    s.use_farlamp_set()
    # north of the fog's edge: a few black rocks, a dark buoy line, a warning sign
    s.islet(24, 6, 2.4, 1.5)          # the warning rock (a shingle bank, a sign)
    skerry(s, 9, 4.5)
    skerry(s, 16, 9.5, 1.0, 0.8)
    # south: skerries the lit lane threads, one shingle islet with a cache
    s.islet(7, 22, 2.2, 1.5)
    skerry(s, 25, 25)
    skerry(s, 10, 30)
    skerry(s, 4, 27, 1.0, 0.8)
    skerry(s, 27, 19, 1.0, 0.8)
    # the south-east corner is reef: nothing rows out there (Kelpcrown's coast)
    def reef(g):
        mk.rect(g, W, H, 30, 29, 31, H - 1)
        mk.blob(g, W, H, 30.5, 31, 1.8, 3.4)
    cl = s.land(reef)
    for i, v in enumerate(cl):
        if v:
            s.cliff[i] = 1
    for y in range(27, H):
        for x in range(26, W):
            i = s.cell(x, y)
            if not s.cliff[i] and any(s.cliff[s.cell(min(W - 1, x + d), y)] for d in (1, 2)):
                s.sand[i] = 1
                s.water[i] = 0
    boulders(s, [(23, 7), (7, 21)])
    for (cx, cy, n) in ((3, 3, 3), (13, 6, 2), (29, 11, 2), (2, 19, 3), (12, 16, 2),
                        (22, 31, 3), (6, 34, 2)):
        sea_rocks(s, cx, cy, n)
    s.sign("fogwall_warning", (25, 6))
    s.obj("warning_wreck", "pearlmoor_driftwood", (8, 5), 2, 1, solid=False)
    s.kin("amb_fogwisp", (15, 10), 176, radius=1)

    # THE FAR LAMP: the skerry light + its blink (an animated tile, `above` layer)
    SK = (16, 17)
    s.obj("far_lamp", "farlamp_skerry_light", SK, 3, 3, overhang=1)
    s.above[s.cell(SK[0] + 1, SK[1])] = gid("blink_lamp", set="farlamp_set")
    # the turn-round band: every tile of row TURN_ROW, gone once you hold the glass
    for x in range(W):
        if s.water[s.cell(x, TURN_ROW)]:
            s.m["triggers"].append({"id": f"fog_turn_{x}", "kind": "cutscene",
                                    "at": {"tx": x, "ty": TURN_ROW}, "activation": "step_on",
                                    "ref": "script.fogwall_turned", "hidden_when_flag": GLASS})
    s.owed.append("script.fogwall_turned")
    # the lantern-buoy lane (dark until the fog-glass reads it; then lit)
    lane = [(27, 12), (24, 15), (21, 18), (21, 22), (17, 24), (13, 26), (14, 30), (17, 33)]
    for i, (x, y) in enumerate(lane):
        s.obj(f"lane_buoy_{i}", "farlamp_buoy_dark", (x, y - 1), 1, 2, solid=False,
              hidden_when_flag=GLASS)
        s.obj(f"lane_buoy_{i}_lit", "farlamp_buoy_lit", (x, y - 1), 1, 2, solid=False,
              requires_flag=GLASS)
    # fog banks over the deep (they lift with the isles' dawn)
    for i, (x, y, big) in enumerate(((2, 9, 1), (19, 2, 0), (3, 15, 0), (24, 18, 1),
                                     (1, 26, 1), (20, 29, 0), (26, 33, 0), (5, 33, 1),
                                     (10, 12, 1), (27, 0, 0), (13, 21, 0), (7, 17, 1))):
        s.obj(f"fogbank_{i}", "farlamp_fogbank_a" if big else "farlamp_fogbank_b",
              (x, y), 4 if big else 3, 2, solid=False, hidden_when_flag=DAWN)
    s.kin("amb_fathomote", (26, 25), 172, radius=1)
    s.cache("fog_reef", (7, 22))
    s.m["ambience"] = sea_ambience(heavy=True, flocks=[(24, 6)],
                                   lights=[(SK[0] + 1, SK[1], 26, "#ffd089")])
    return s


# =============================================================================
#  GULLWRACK ISLE
# =============================================================================
GULL_HUT = (5, 20)            # 4x4 keeper's hut; door tile (7, 23)
GULL_HUT_DOOR = (GULL_HUT[0] + 2, GULL_HUT[1] + 3)
GULL_MOUTH = (13, 9)          # contract: to_undertide @ (13,9), landing (13,10)


def build_gullwrack() -> Sea:
    s = Sea("farlamp_gullwrack", "Gullwrack Isle", 27, 34, seed=1775,
            backdrops=ISLE_BACKDROPS)
    W, H = s.W, s.H

    def body(g):
        mk.blob(g, W, H, 13, 17.5, 10.2, 11.6)
        mk.blob(g, W, H, 6, 24, 4.0, 4.4)
        mk.blob(g, W, H, 19, 25, 4.4, 3.6)
    s.land(body)
    # beaches: a sand rim all round, wider coves east (the landing) and south-west
    rim = mk.make_grid(W, H)
    for y in range(H):
        for x in range(W):
            i = s.cell(x, y)
            if s.water[i]:
                continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and s.water[s.cell(x + dx, y + dy)]
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                rim[i] = 1
    mk.blob(rim, W, H, 21.5, 15, 2.2, 3.4)
    mk.blob(rim, W, H, 4.5, 15, 1.8, 2.6)
    for i, v in enumerate(rim):
        if v and not s.water[i]:
            s.sand[i] = 1
    # the gull-cliffs: the island's high north end (plateau tops, the lit FACE south)
    mk.blob(s.cliff, W, H, 13, 6.2, 7.6, 2.9)
    for i in range(W * H):
        if s.cliff[i]:
            s.sand[i] = 0
            s.water[i] = 0
    for x in (12, 13, 14):                # keep the cave's floor clear below the face
        s.cliff[s.cell(x, 9)] = 0
        s.cliff[s.cell(x, 10)] = 0
    # the mainland's sea-cliffs, east edge
    for y in range(3, H):
        x0 = 24 if (y // 4) % 3 == 1 else 25
        for x in range(x0, W):
            s.cliff[s.cell(x, y)] = 1
            s.water[s.cell(x, y)] = 0
            s.sand[s.cell(x, y)] = 0
        s.sand[s.cell(x0 - 1, y)] = 1
        s.water[s.cell(x0 - 1, y)] = 0
    # the path: the east landing up to the cave, down to the hut
    for (x, y) in ([(x, 11) for x in range(12, 21)] + [(13, 10)] +
                   [(17, y) for y in range(11, 21)] + [(x, 20) for x in range(8, 18)] +
                   [(8, 21), (8, 22), (8, 23), (8, 24), (7, 24)]):
        i = s.cell(x, y)
        if not s.water[i] and not s.cliff[i]:
            s.path[i] = 1
            s.sand[i] = 0
    # sea-grass: the tall meadow west of the lane + a band on the south spur
    tufts(s, s.tallgrass, [(9.5, 14.5, 3.4), (19.5, 25.5, 2.8), (12.5, 25.5, 2.0),
                           (20.5, 14, 1.6)])
    for i in range(W * H):
        if s.water[i] or s.sand[i] or s.path[i] or s.cliff[i]:
            s.tallgrass[i] = 0
    # a one-way ledge: the high meadow (rows 12-16) hops down to the hut fields
    for x in range(4, 12):
        if not s.water[s.cell(x, 17)] and not s.sand[s.cell(x, 17)]:
            s.deco[s.cell(x, 17)] = gid("grass_ledge_s")
            s.tallgrass[s.cell(x, 17)] = 0
    s.deco[s.cell(5, 17)] = gid("grass_ledge_s_v1")

    # the cave mouth (contract) + marker; gulls on the cliffs
    wm.add(s.m, wm.marker("undertide_mouth", "cave_mouth", GULL_MOUTH[0], GULL_MOUTH[1] - 1))
    warp(s.m, "to_undertide", GULL_MOUTH, "undertide_i", (15, 26), "up")
    s.m["warps"][-1]["transition"] = "fade"
    s.obj("cliff_nest_a", "pearlmoor_gull_nest", (8, 7), 1, 1, solid=False)
    s.obj("cliff_nest_b", "pearlmoor_gull_nest", (18, 6), 1, 1, solid=False)
    s.obj("cliff_nest_c", "pearlmoor_gull_nest", (11, 4), 1, 1, solid=False)
    # the keeper's hut (rest point) + its lamp, nets, a bench
    s.obj("keeper_hut", "farlamp_keeper_hut", GULL_HUT, 4, 4, overhang=2)
    warp(s.m, "to_hut", GULL_HUT_DOOR, "gullwrack_hut", (5, 7), "up", transition="door")
    s.obj("hut_lamp", "tinderwick_lamp_post", (10, 21), 1, 3, overhang=2, walk_under=True)
    s.obj("hut_nets", "pearlmoor_net_rack", (2, 23), 2, 1)
    s.obj("hut_pots", "pearlmoor_crab_pots", (10, 24), 1, 1)
    s.sign("gullwrack_hut", (9, 23))
    # landing + south shore dressing
    s.obj("landing_boat", "pearlmoor_rowboat", (22, 17), 2, 2)
    s.obj("landing_drift", "pearlmoor_driftwood", (21, 11), 2, 1, solid=False)
    s.obj("spur_pine", "windward_bent_pine", (19, 22), 2, 3, overhang=2, walk_under=True)
    s.obj("spur_ribs", "pearlmoor_wreck_ribs", (13, 29), 3, 2)
    s.cache("gull_spur", (22, 26))
    s.cache("gull_meadow", (5, 13))
    boulders(s, [(7, 11), (19, 13), (15, 22), (4, 27), (23, 21), (2, 3), (22, 2), (8, 31)])
    s.kin("amb_hermiwick", (16, 27), 174, radius=1)
    s.kin("amb_fathomote", (3, 19), 172, radius=1)
    s.obj("meadow_tree", "tinderwick_tree_b", (13, 13), 3, 4, overhang=3, walk_under=True)
    s.obj("cliff_pine", "windward_bent_pine", (4, 9), 2, 3, overhang=2, walk_under=True)
    s.obj("hut_tree", "tinderwick_tree_b", (1, 19), 3, 4, overhang=3, walk_under=True)
    s.obj("hut_wood", "tinderwick_woodpile", (11, 22), 2, 1)
    blooms(s, [(6, 11), (8, 10), (15, 17), (19, 18), (11, 19), (3, 25), (14, 23), (16, 24),
               (22, 23), (7, 18), (18, 12)])
    for (cx, cy, n) in ((3, 6, 3), (23, 4, 2), (1, 13, 2), (11, 32, 3), (19, 31, 2)):
        sea_rocks(s, cx, cy, n)
    sea_buoys(s, [(4, 2), (17, 1), (1, 9), (22, 31), (1, 30)])
    s.m["ambience"] = sea_ambience(flocks=[(10, 6), (17, 5), (21, 16)],
                                   lights=[])
    return s


# =============================================================================
#  KELPCROWN ISLE
# =============================================================================
KELP_MOUTH = (10, 9)          # contract: to_undertide @ (10,9), landing (10,10)


def build_kelpcrown() -> Sea:
    s = Sea("farlamp_kelpcrown", "Kelpcrown Isle", 30, 34, seed=1776,
            backdrops=ISLE_BACKDROPS)
    W, H = s.W, s.H

    def body(g):
        mk.blob(g, W, H, 15, 18.5, 11.4, 12.2)
        mk.blob(g, W, H, 9, 26, 5.2, 4.0)
        mk.blob(g, W, H, 23, 11, 4.0, 4.2)
    s.land(body)
    # the west edge is reef + cliff (Driftholm's coast beyond — nothing rows there)
    edge = [2 if (y // 5) % 3 == 1 else 1 for y in range(H)]
    for y in range(H):
        for x in range(0, edge[y] + 1):
            s.cliff[s.cell(x, y)] = 1
            s.water[s.cell(x, y)] = 0
        s.sand[s.cell(edge[y] + 1, y)] = 1
        s.water[s.cell(edge[y] + 1, y)] = 0
    rim = mk.make_grid(W, H)
    for y in range(H):
        for x in range(2, W):
            i = s.cell(x, y)
            if s.water[i] or s.cliff[i]:
                continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and s.water[s.cell(x + dx, y + dy)]
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                rim[i] = 1
    mk.blob(rim, W, H, 25.5, 19, 2.0, 3.2)        # the east landing
    mk.blob(rim, W, H, 15, 29.5, 3.0, 1.6)
    for i, v in enumerate(rim):
        if v and not s.water[i]:
            s.sand[i] = 1
    # the cave ridge, north-west (the Undertide II mouth under its face)
    mk.blob(s.cliff, W, H, 9.5, 6.5, 5.4, 2.6)
    mk.blob(s.cliff, W, H, 6.2, 5.4, 1.6, 1.2)
    mk.blob(s.cliff, W, H, 12.6, 4.6, 1.4, 1.1)
    for i in range(W * H):
        if s.cliff[i]:
            s.sand[i] = 0
            s.water[i] = 0
    for x in (9, 10, 11):
        s.cliff[s.cell(x, 9)] = 0
        s.cliff[s.cell(x, 10)] = 0
    # the old keepers' quarter: worn flagstones east of the ridge
    mk.blob(s.ruin, W, H, 19.5, 11.5, 4.4, 3.2)
    # kelp terraces: two benches stepping down south-west, hopped by ledges
    for (y, x0, x1) in ((19, 4, 12), (24, 5, 13)):
        for x in range(x0, x1 + 1):
            i = s.cell(x, y)
            if not s.water[i] and not s.sand[i] and not s.cliff[i]:
                s.deco[i] = gid("grass_ledge_s_v1" if x % 4 == 0 else "grass_ledge_s")
    for (y, x) in ((19, 8), (24, 9)):           # each bench keeps a gap (the way back up)
        s.deco[s.cell(x, y)] = 0
    tufts(s, s.tallgrass, [(7.5, 16.5, 3.0), (8.5, 21.6, 3.2), (9.5, 27, 3.0), (25, 12, 1.5)])
    # the Tidecall pools: freshwater-and-sea pools the tide fills (pond = water over grass)
    for (cx, cy, rx, ry) in ((20.5, 21.5, 2.6, 1.7), (19, 22.6, 1.8, 1.2), (22, 20.6, 1.4, 1.1),
                             (12.2, 14.2, 1.5, 1.1), (11.2, 15, 1.1, 0.9)):
        mk.blob(s.pond, W, H, cx, cy, rx, ry)
    # the lane: east landing -> the ruins -> the ridge mouth; a branch south
    for (x, y) in ([(x, 18) for x in range(15, 26)] + [(15, y) for y in range(11, 18)] +
                   [(x, 11) for x in range(10, 15)] + [(10, 10)] +
                   [(15, y) for y in range(19, 28)] + [(x, 28) for x in range(12, 16)]):
        i = s.cell(x, y)
        if not s.water[i] and not s.cliff[i] and not s.pond[i]:
            s.path[i] = 1
            s.sand[i] = 0
    for i in range(W * H):
        if s.water[i] or s.sand[i] or s.path[i] or s.cliff[i] or s.pond[i] or s.ruin[i]:
            s.tallgrass[i] = 0
        if s.pond[i]:
            s.ruin[i] = 0

    wm.add(s.m, wm.marker("undertide_mouth", "cave_mouth", KELP_MOUTH[0], KELP_MOUTH[1] - 1))
    warp(s.m, "to_undertide", KELP_MOUTH, "undertide_ii", (14, 28), "up")
    # the ruins
    s.obj("ruin_wall_a", "farlamp_ruin_wall", (17, 8), 3, 2)
    s.obj("ruin_wall_b", "farlamp_ruin_wall", (21, 13), 3, 2)
    s.obj("ruin_pillar_a", "farlamp_ruin_pillar", (17, 12), 1, 2)
    s.obj("ruin_pillar_b", "farlamp_ruin_pillar", (23, 9), 1, 2)
    s.obj("ruin_pillar_c", "farlamp_ruin_pillar", (20, 11), 1, 2)
    s.cache("kelpcrown_purse", (22, 10))
    s.sign("kelpcrown_ruins", (19, 15))
    # the kelp terraces
    s.obj("terrace_rack_a", "farlamp_kelp_rack", (4, 15), 2, 2)
    s.obj("terrace_rack_b", "farlamp_kelp_rack", (11, 21), 2, 2)
    s.obj("terrace_rack_c", "farlamp_kelp_rack", (5, 26), 2, 2)
    s.cache("kelp_terrace", (12, 26))
    # the pools: a stepping-cache on the pool's island tongue (Tidecall to reach)
    s.cache("kelp_pool", (21, 21))
    s.kin("amb_hermiwick", (25, 15), 174, radius=1)
    s.kin("amb_tidalarch", (18, 24), 61, radius=1)
    s.obj("landing_boat", "pearlmoor_rowboat", (26, 22), 2, 2)
    s.obj("landing_pots", "pearlmoor_crab_pots", (24, 20), 1, 1)
    s.obj("south_ribs", "pearlmoor_wreck_ribs", (18, 29), 3, 2)
    s.obj("crown_pine", "windward_bent_pine", (24, 26), 2, 3, overhang=2, walk_under=True)
    boulders(s, [(14, 7), (5, 11), (25, 7), (7, 30), (13, 31)])
    s.obj("ridge_pine", "windward_bent_pine", (4, 9), 2, 3, overhang=2, walk_under=True)
    s.obj("pool_tree", "tinderwick_tree_b", (16, 22), 3, 4, overhang=3, walk_under=True)
    s.obj("ruin_tree", "tinderwick_tree_b", (24, 14), 3, 4, overhang=3, walk_under=True)
    blooms(s, [(13, 18), (17, 17), (19, 16), (12, 12), (23, 17), (21, 25), (18, 26), (10, 24)])
    for (cx, cy, n) in ((4, 3, 2), (21, 3, 3), (28, 9, 2), (26, 31, 3), (5, 32, 2)):
        sea_rocks(s, cx, cy, n)
    sea_buoys(s, [(5, 2), (16, 1), (27, 3), (28, 31), (22, 32)])
    s.m["ambience"] = sea_ambience(flocks=[(9, 5), (24, 24)])
    return s


# =============================================================================
#  the seams + the mainland side
# =============================================================================
# Lightkeeper's Point's south edge (row 13, x 0-19) <-> the Sound's north edge;
# the Wick-Run Foot's south edge (row 29) <-> the Shelfwater's north edge. The
# mainland builders own their side (build_pearlmoor_point.py / build_wickrun_foot.py
# import these and add the AFLOAT-gated warps); every tile of both seams is water.
POINT_SEAM = range(0, 20)
FOOT_SEAM = range(1, 29)


def mainland_seams(sound: Sea, shelf: Sea) -> None:
    for x in POINT_SEAM:
        warp(sound.m, f"to_point_{x}", (x, 0), "pearlmoor_point", (x, 12), "up")
    for x in FOOT_SEAM:
        warp(shelf.m, f"to_foot_{x}", (x, 0), "wickrun_foot", (x, 28), "up")


def build_all():
    sound, shelf, fog = build_sound(), build_shelfwater(), build_fogwall()
    gull, kelp = build_gullwrack(), build_kelpcrown()
    mainland_seams(sound, shelf)
    # Sound west (rows 3-32) <-> Shelfwater east (rows 0-29)
    link(sound, "w", shelf, "e", a_lo=3, b_lo=0, n=30, prefix_a="to_shelf", prefix_b="to_sound")
    # Shelfwater west <-> Fogwall east (rows 0-29)
    link(shelf, "w", fog, "e", a_lo=0, b_lo=0, n=30, prefix_a="to_fogwall", prefix_b="to_shelf")
    # Sound south <-> Gullwrack north (x 0-26)
    link(sound, "s", gull, "n", a_lo=0, b_lo=0, n=27, prefix_a="to_gullwrack", prefix_b="to_sound")
    # Shelfwater south <-> Kelpcrown north (x 0-29)
    link(shelf, "s", kelp, "n", a_lo=0, b_lo=0, n=30, prefix_a="to_kelpcrown", prefix_b="to_shelf")
    # Gullwrack west <-> Kelpcrown east (rows 0-33)
    link(gull, "w", kelp, "e", a_lo=0, b_lo=0, n=34, prefix_a="to_kelpcrown", prefix_b="to_gullwrack")
    # Fogwall south <-> Driftholm north: build_driftholm.py owns BOTH sides of this
    # seam (it reads the Fogwall's shipped south row), so Driftholm rebuilds alone.
    return [sound, shelf, fog, gull, kelp]


def fog_seam_cells(fog: Sea):
    return [x for x in range(fog.W) if fog.passable(x, fog.H - 1) and fog.passable(x, fog.H - 2)]


DRIFTHOLM_SEAM = range(4, 28)   # Driftholm's harbour mouth: open sea across these columns


if __name__ == "__main__":
    maps = build_all()
    fog = maps[2]
    for x in DRIFTHOLM_SEAM:
        if fog.passable(x, fog.H - 1) and fog.passable(x, fog.H - 2):
            warp(fog.m, f"to_driftholm_{x}", (x, fog.H - 1), "driftholm", (x, 1), "down")
    ok = True
    for s in maps:
        s.assemble()
        sea_zones(s)
        s.scatter(0.10)
        print(f"== {s.id}")
        ok = s.finalize() and ok
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
