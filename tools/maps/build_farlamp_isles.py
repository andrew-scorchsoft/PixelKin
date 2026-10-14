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
import patterns as pt
from patterns import zones_from_grid

AFLOAT = "flag:q_isles_afloat"
GLASS = "flag:q_isles_fogglass"
DAWN = "flag:isles_dawn"


def T(*rows):
    return [{"kin_id": k, "weight": w, "min_level": lo, "max_level": hi} for (k, w, lo, hi) in rows]


# ---- encounter tables (mirrored in build_species.py EXTRA_ENCOUNTERS) ---------------
TABLES = {
    # Post-game levels (the player crosses at L69+, the Undertide runs 63-68).
    # The isles' own family is met KINDLED out here — Fathomere (#173, kindles
    # at 40) and Beaconclaw (#175, at 42) are the common sea-kin; their base
    # forms Fathomote (#172) and Hermiwick (#174) are the rare finds (a wild
    # lv-60 base form would have kindled twenty levels ago).
    "farlamp_sound": {
        "deep": T((173, 35, 62, 65), (175, 15, 62, 64), (28, 15, 63, 65), (22, 12, 62, 65),
                  (30, 8, 63, 65), (172, 5, 62, 63), (174, 5, 62, 63)),
        "water": T((173, 35, 62, 64), (32, 30, 62, 64), (61, 30, 62, 64), (172, 5, 62, 63)),
        "grass": T((175, 40, 62, 64), (96, 25, 62, 65), (46, 25, 62, 64), (95, 5, 62, 63),
                   (174, 5, 62, 63)),
    },
    "farlamp_shelfwater": {
        "deep": T((173, 35, 63, 66), (175, 15, 63, 65), (61, 15, 64, 66), (32, 15, 63, 66),
                  (28, 10, 64, 66), (172, 5, 63, 64), (174, 5, 63, 64)),
        "water": T((173, 40, 63, 65), (61, 30, 63, 65), (175, 25, 63, 65), (172, 5, 63, 64)),
    },
    "farlamp_fogwall": {
        "deep": T((176, 35, 64, 67), (173, 25, 64, 66), (85, 15, 65, 67), (79, 10, 64, 67),
                  (22, 10, 64, 66), (172, 5, 64, 65)),
        "water": T((176, 45, 64, 66), (173, 35, 64, 66), (85, 15, 65, 67), (172, 5, 64, 65)),
    },
    "farlamp_gullwrack": {
        "grass": T((175, 30, 64, 66), (96, 20, 64, 66), (76, 15, 64, 66), (52, 15, 64, 66),
                   (46, 15, 65, 66), (174, 5, 64, 65)),
        "water": T((173, 40, 64, 66), (28, 30, 64, 66), (61, 22, 64, 66), (30, 8, 65, 66),
                   (172, 5, 64, 65)),
        "deep": T((173, 45, 64, 66), (175, 25, 64, 66), (28, 20, 64, 66), (30, 10, 65, 66)),
    },
    "farlamp_kelpcrown": {
        "grass": T((175, 25, 64, 67), (61, 20, 64, 66), (64, 15, 65, 67), (55, 15, 64, 66),
                   (37, 15, 64, 66), (174, 10, 64, 65)),
        "water": T((173, 35, 64, 66), (32, 35, 64, 66), (61, 25, 64, 66), (172, 5, 64, 65)),
        "deep": T((173, 45, 64, 67), (175, 25, 64, 66), (32, 20, 64, 66), (172, 10, 64, 65)),
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
    grass = [1 if (a or b) else 0 for a, b in zip(s.tallgrass, s.dunegrass)]
    if "grass" in t and any(grass):
        zs += zones_from_grid(grass, s.W, s.H, terrain="tall_grass", rate=grass_rate,
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


def lane(s: Sea, pts):
    """A walked lane through waypoints: each leg runs along x then y, so many
    waypoints read as a meandering path, never one ruled L."""
    cells = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        sx = 1 if x1 >= x0 else -1
        for x in range(x0, x1 + sx, sx):
            cells.append((x, y0))
        sy = 1 if y1 >= y0 else -1
        for y in range(y0, y1 + sy, sy):
            cells.append((x1, y))
    for (x, y) in cells:
        i = s.cell(x, y)
        if not s.water[i] and not s.cliff[i] and not s.pond[i]:
            s.path[i] = 1
            s.sand[i] = 0
            s.tallgrass[i] = 0
            s.dunegrass[i] = 0


def outcrop(s: Sea, x, y, shape="L"):
    """A boulder outcrop (a cluster, never a lone stone): 3-4 boulders."""
    cells = {"L": [(0, 0), (1, 0), (0, 1)], "J": [(0, 0), (1, 0), (1, 1)],
             "T": [(0, 0), (1, 0), (2, 0), (1, 1)], "S": [(0, 0), (1, 0), (1, 1), (2, 1)],
             "O": [(0, 0), (1, 0), (0, 1), (1, 1)]}[shape]
    for (dx, dy) in cells:
        i = s.cell(x + dx, y + dy)
        if not s.path[i]:
            s.deco[i] = gid("boulder")
            s.tallgrass[i] = 0


def dunes(s: Sea, blobs):
    """Blown-sand patches inland with tufted dune-grass in them (the sand-
    context encounter grass): a sea-isle's own texture, not a mainland meadow."""
    for (cx, cy, rx, ry, grassy) in blobs:
        g = mk.make_grid(s.W, s.H)
        mk.blob(g, s.W, s.H, cx, cy, rx, ry)
        for i, v in enumerate(g):
            if v and not s.water[i] and not s.cliff[i] and not s.path[i] and not s.pond[i]:
                s.sand[i] = 1
                s.tallgrass[i] = 0
        if grassy:
            g2 = mk.make_grid(s.W, s.H)
            mk.blob(g2, s.W, s.H, cx, cy, rx * 0.6, ry * 0.6)
            for i, v in enumerate(g2):
                if v and s.sand[i] and not s.water[i]:
                    s.dunegrass[i] = 1


def blooms(s: Sea, cells):
    for (x, y) in cells:
        if not s.water[s.cell(x, y)] and not s.deco[s.cell(x, y)]:
            s.deco[s.cell(x, y)] = gid("flowerbed_a" if (x + y) % 2 else "flowerbed_b")


def skerry(s: Sea, cx, cy, rx=1.3, ry=0.9):
    """A black rock skerry: no beach at all, just a knot of rock standing out of
    a shallow flat (so it never reads as another sand islet)."""
    for y in range(int(cy - ry - 2), int(cy + ry + 3)):
        for x in range(int(cx - rx - 2), int(cx + rx + 3)):
            if not (0 < x < s.W - 1 and 0 < y < s.H - 1):
                continue
            d = ((x - cx) / (rx + 0.5)) ** 2 + ((y - cy) / (ry + 0.5)) ** 2
            if d <= 1.0 and s.water[s.cell(x, y)] and s.rng.random() < 0.62:
                s.deco[s.cell(x, y)] = gid("boulder")
            if d <= 2.3:
                s.no_deep.add((x, y))


def _segd(x, y, a, b):
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L))
    return ((x - ax - t * dx) ** 2 + (y - ay - t * dy) ** 2) ** 0.5


def bar(s: Sea, pts, *, r=0.8, shoal=2.4, grass=False):
    """A long sand BAR along a polyline (a reef flat, not a round blob): sand
    within `r` of the line, a designed shallow flat (never deep) within `shoal`.
    `grass` greens the bar's spine (a holm with turf on its back)."""
    segs = list(zip(pts, pts[1:]))
    for y in range(1, s.H - 1):
        for x in range(1, s.W - 1):
            d = min(_segd(x, y, a, b) for a, b in segs)
            i = s.cell(x, y)
            if d <= r:
                s.water[i] = 0
                s.sand[i] = 0 if (grass and d <= r - 0.9) else 1
            if d <= shoal:
                s.no_deep.add((x, y))


def reef(s: Sea, pts, *, step=2, gaps=(), shoal=1.6):
    """A REEF LINE: black rocks stood along a polyline in the water every `step`
    tiles over a shallow flat, broken by `gaps` (the channels you row through)."""
    cells = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        n = max(1, int(4 * max(abs(bx - ax), abs(by - ay))))
        for k in range(n):
            c = (round(ax + (bx - ax) * k / n), round(ay + (by - ay) * k / n))
            if c not in cells:
                cells.append(c)
    last = tuple(round(v) for v in pts[-1])
    if last not in cells:
        cells.append(last)
    for k, (x, y) in enumerate(cells):
        for yy in range(y - int(shoal), y + int(shoal) + 1):
            for xx in range(x - int(shoal), x + int(shoal) + 1):
                if 0 <= xx < s.W and 0 <= yy < s.H and (xx - x) ** 2 + (yy - y) ** 2 <= shoal ** 2:
                    s.no_deep.add((xx, yy))
        if k % step or any(abs(x - gx) + abs(y - gy) <= 1 for (gx, gy) in gaps):
            continue
        if 0 < x < s.W - 1 and 0 < y < s.H - 1 and s.water[s.cell(x, y)]:
            s.deco[s.cell(x, y)] = gid("boulder")


def strand(s: Sea, rate=0.22):
    """Strand litter on open sand (shells, kelp wrack, shingle) so a bar reads
    as a beach the tide works, not a blank tan slab — never on a lane, a body
    or a trigger/warp tile."""
    W, H = s.W, s.H
    busy = {(o["at"]["tx"] + dx, o["at"]["ty"] + dy) for o in s.m["objects"]
            for dx in range(o["w"]) for dy in range(o["h"])}
    busy |= {(n["at"]["tx"], n["at"]["ty"]) for n in s.m["npcs"]}
    busy |= {(t["at"]["tx"], t["at"]["ty"]) for t in s.m["triggers"]}
    busy |= {(w["at"]["tx"], w["at"]["ty"]) for w in s.m["warps"]}
    kinds = ("farlamp_strand_shells", "farlamp_strand_wrack", "farlamp_strand_shingle")
    k = 0
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            i = s.cell(x, y)
            if not s.sand[i] or s.water[i] or s.path[i] or s.deco[i] or s.dunegrass[i] \
                    or (x, y) in busy:
                continue
            if s.rng.random() < rate:
                s.obj(f"strand_{k}", kinds[s.rng.randrange(3)], (x, y), 1, 1, solid=False)
                k += 1


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
    s.islet(5, 6.5, 3.2, 2.4)
    mk.rect(s.cliff, W, H, 3, 4, 6, 6)                       # the stack itself: a sheer block
    mk.blob(s.cliff, W, H, 4.6, 4.8, 2.2, 1.2)
    for i, v in enumerate(s.cliff):
        if v:
            s.sand[i] = 0
            s.water[i] = 0
    # B: the wreck bar — a long sand bar, the ribs of a lost lamp-tender
    bar(s, [(13.4, 8.4), (16.5, 7.2), (20.6, 7.6)], r=1.15, shoal=2.6)
    # C: Cormorant Holm — the boat-trainer's islet, a tall-grass heart
    s.islet(6.5, 17, 4.6, 3.3, grass=0.62)
    # D: THE RING — a reef ring of black rocks and bars round a shallow lagoon
    # (the Sound's designed loop): row in by the north gap or the south-west
    # gap, round the lagoon, out the other. The old buoy line marks both gaps.
    import math
    ring = [(16 + 4.2 * math.cos(a), 18 + 3.8 * math.sin(a))
            for a in [k * math.pi / 8 for k in range(17)]]
    bar(s, [(20.2, 16.4), (20.2, 18.6)], r=0.7, shoal=0)        # the ring's east bar
    bar(s, [(14.6, 21.8), (17.4, 21.8)], r=0.7, shoal=0)        # the south bar
    reef(s, ring, step=1, gaps=[(16, 14), (12, 20), (12, 21)], shoal=1.0)
    for y in range(15, 22):
        for x in range(12, 21):
            if ((x - 16) / 3.4) ** 2 + ((y - 18) / 3.2) ** 2 <= 1:
                s.no_deep.add((x, y))
    # F: Tern Islet — the bent pine and the Sound's sign
    s.islet(9, 27, 4.2, 2.8, grass=0.55)
    # G: the anchor rock (a black skerry, not another sand blob)
    skerry(s, 19.5, 27.5, 2.2, 1.4)
    tufts(s, s.tallgrass, [(6.5, 17, 2.6)])
    blooms(s, [(8, 26), (10, 26), (6, 28), (3, 16), (9, 15)])
    for i in range(W * H):
        if s.water[i] or s.sand[i]:
            s.tallgrass[i] = 0

    boulders(s, [(7, 7), (2, 7), (21, 27), (20, 28),
                 (25, 3), (24, 2), (11, 28)])
    # the Quay's harbour wall runs on into the sea over the NE corner — nothing to
    # row into there (world_geometry: the Quay's last rows overlap ours as sea)
    for (x, y) in ((20, 0), (21, 1), (23, 0), (26, 1)):
        s.deco[s.cell(x, y)] = gid("buoy")

    s.obj("gannet_nest_a", "pearlmoor_gull_nest", (5, 5), 1, 1, solid=False)
    s.obj("gannet_nest_b", "pearlmoor_gull_nest", (4, 4), 1, 1, solid=False)
    s.cache("sound_stack", (4, 7))
    s.obj("wreck_ribs", "pearlmoor_wreck_ribs", (16, 7), 3, 2)
    s.obj("wreck_drift", "pearlmoor_driftwood", (19, 8), 2, 1, solid=False)
    s.kin("amb_tidwraith", (14, 8), 22, radius=1)
    s.trainer("sound_oarsman", (10, 18), "right", "fisher_man")
    s.obj("oarsman_boat", "pearlmoor_rowboat", (11, 19), 2, 2)
    s.obj("holm_crates", "pearlmoor_crab_pots", (4, 18), 1, 1)
    # the old buoy line across the reef — dark since the Long Dusk
    for i, (x, y) in enumerate(((12, 11), (15, 13), (17, 13), (12, 23), (11, 25))):
        s.obj(f"old_buoy_{i}", "farlamp_buoy_dark", (x, y - 1), 1, 2, solid=False)
    s.kin("amb_lagoon", (16, 22), 173, radius=1)              # a Fathomere on the ring's bar
    s.cache("sound_cove", (22, 14))
    s.obj("cove_drift", "pearlmoor_driftwood", (22, 16), 2, 1, solid=False)
    s.kin("amb_beaconclaw", (22, 24), 175, radius=1)
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
    # THE SHELF CHANNEL (the designed shape): two long reef bars run NW-SE in
    # parallel over a shallow flat, a rowing channel between them — the old
    # lamp-tenders' road out of the Foot, still buoyed. Their tails are broken
    # into rock so the channel opens both ways.
    bar(s, [(3, 5.5), (8, 4.2), (12.5, 5.2)], r=0.85, shoal=2.2, grass=False)
    bar(s, [(3.5, 11.2), (8.5, 9.6), (13.2, 10.8)], r=0.95, shoal=2.2)
    reef(s, [(13.5, 5.6), (16.5, 7.4)], step=1, shoal=1.2)
    reef(s, [(14.2, 11.2), (16.4, 13.4)], step=1, shoal=1.2)
    for y in range(5, 11):
        for x in range(2, 16):
            s.no_deep.add((x, y))
    # THE SE FLAT: a long hooked bar (the Salvager's) round a shallow bight,
    # with a second wreck — the cutter GANNET's ribs — beached on its hook
    bar(s, [(19, 27), (22.5, 24.2), (26.5, 22.4), (27.4, 19.2)], r=1.0, shoal=2.6)
    bar(s, [(21.5, 20.6), (23.6, 19.6)], r=0.7, shoal=1.6)
    reef(s, [(18.4, 22.0), (20.2, 18.8)], step=1, shoal=1.0)
    # the hull bank: where the lamp-tender HERON went down, her stern still out
    s.islet(20.5, 10.5, 3.0, 1.8, grass=0.0)
    # Skerry of the Oar: the boat-trainer's grassed islet
    s.islet(11, 20, 3.8, 2.6, grass=0.6)
    # the kelp holm, south-west
    bar(s, [(2.4, 24.0), (5.0, 22.6), (7.6, 23.4)], r=1.5, shoal=2.0, grass=True)
    boulders(s, [(19, 11), (13, 21), (9, 19), (3, 22), (16, 2), (1, 16)])
    s.obj("heron_stern", "coldfog_beached_boat", (19, 9), 3, 2)
    s.cache("shelf_hull", (22, 11))
    s.obj("heron_mast", "pearlmoor_wreck_ribs", (22, 8), 3, 2, solid=False)
    s.trainer("shelf_kelper", (13, 19), "right", "fisher_woman")
    s.obj("kelper_rack", "farlamp_kelp_rack", (9, 19), 2, 2)
    s.obj("kelp_rack_b", "farlamp_kelp_rack", (4, 22), 2, 2)
    s.cache("shelf_holm", (6, 23))
    s.kin("amb_lumplass", (6, 10), 32, radius=1)
    s.kin("amb_beaconclaw", (9, 4), 175, radius=1)
    # the channel's buoys, both mouths and the bend
    for i, (x, y) in enumerate(((2, 8), (9, 7), (16, 9), (17, 15), (14, 26))):
        s.obj(f"old_buoy_{i}", "farlamp_buoy_dark", (x, y - 1), 1, 2, solid=False)
    # the SE flat: the GANNET's ribs on the hook, the Salvager working them
    s.obj("gannet_ribs", "pearlmoor_wreck_ribs", (25, 20), 3, 2)
    s.obj("salvager_boat", "pearlmoor_rowboat", (19, 24), 2, 2)
    s.trainer("shelf_salvager", (23, 23), "left", "fisher_man")
    s.obj("salvager_pots", "pearlmoor_crab_pots", (24, 23), 1, 1)
    s.obj("salvager_drift", "pearlmoor_driftwood", (26, 22), 2, 1, solid=False)
    s.kin("amb_hermiwick", (22, 20), 175, radius=1)
    sea_buoys(s, [(2, 2), (27, 4), (26, 13), (2, 27), (17, 22)])
    for (cx, cy, n) in ((24, 3, 3), (28, 16, 2), (2, 18, 2), (13, 27, 2), (8, 27, 2)):
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
    skerry(s, 10, 3.5)
    skerry(s, 16, 9.5, 1.0, 0.8)
    # NW: the wreck of the GREYLAG, a fog-pilot's cutter run up on a shingle bar —
    # you can land on it, and her pilot never left
    bar(s, [(2.6, 9.6), (5.5, 8.4), (8.6, 9.0)], r=1.05, shoal=2.2)
    # THE TEETH (the designed shape): a chain of black skerries and reef that
    # arcs down the lamp's west side from the fog's edge to Driftholm's harbour
    # mouth — the shoal the lamp-boy poles along at dusk to trim the watch-light
    for (cx, cy, rx, ry) in ((11.5, 15.0, 1.1, 0.7), (8.4, 18.6, 1.2, 0.8),
                             (8.0, 25.6, 1.0, 0.7), (11.0, 31.6, 1.3, 0.8)):
        skerry(s, cx, cy, rx, ry)
    reef(s, [(13.5, 14.2), (11.5, 15.0), (8.4, 18.6), (7.0, 22.0)], step=2, shoal=1.3)
    reef(s, [(7.0, 22.0), (8.0, 25.6), (9.6, 28.6), (11.0, 31.6), (12.5, 34.6)], step=2,
         gaps=[(9, 28)], shoal=1.3)
    # south: skerries the lit lane threads, one shingle islet with a cache
    s.islet(7, 22, 2.2, 1.5)
    for i in range(W * H):                # the Teeth's rocks give way to its one shingle islet
        if not s.water[i] and s.deco[i] == gid("boulder"):
            s.deco[i] = 0
    skerry(s, 25, 25)
    skerry(s, 3, 28, 1.0, 0.8)
    skerry(s, 27, 19, 1.0, 0.8)
    # the south-east corner is reef: nothing rows out there (Kelpcrown's coast)
    def se_reef(g):
        mk.rect(g, W, H, 30, 29, 31, H - 1)
        mk.blob(g, W, H, 30.5, 31, 1.8, 3.4)
    cl = s.land(se_reef)
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
    s.obj("warning_wreck", "pearlmoor_driftwood", (9, 5), 2, 1, solid=False)
    # the GREYLAG on her bar, her pilot still aboard
    s.obj("greylag_hull", "coldfog_beached_boat", (2, 8), 3, 2)
    s.obj("greylag_ribs", "pearlmoor_wreck_ribs", (7, 7), 3, 2, solid=False)
    s.trainer("fog_pilot", (6, 9), "down", "fisher_woman")
    s.obj("willa_coracle", "pearlmoor_rowboat", (8, 10), 2, 2)
    s.kin("amb_fogwisp", (22, 6), 176, radius=1)

    # THE FAR LAMP: the skerry light + its blink (an animated tile, `above` layer)
    SK = (16, 17)
    s.obj("far_lamp", "farlamp_skerry_light", SK, 3, 3, overhang=1)
    s.above[s.cell(SK[0] + 1, SK[1])] = gid("blink_lamp", set="farlamp_set")
    # the watch-light answers Confirm from any side of its rock (its solid rows)
    for (x, y) in ((SK[0] + dx, SK[1] + dy) for (dx, dy) in ((0, 1), (2, 1), (0, 2), (1, 2), (2, 2))):
        s.m["triggers"].append({"id": f"watch_light_{x}_{y}", "kind": "cutscene",
                                "at": {"tx": x, "ty": y}, "activation": "interact",
                                "ref": "script.fogwall_watch_light"})
    s.owed.append("script.fogwall_watch_light")
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
    for i, (x, y, big) in enumerate(((0, 12, 1), (19, 2, 0), (3, 15, 0), (24, 18, 1),
                                     (1, 25, 1), (20, 29, 0), (26, 33, 0), (4, 32, 1),
                                     (13, 11, 1), (27, 0, 0), (13, 21, 0), (1, 19, 1))):
        s.obj(f"fogbank_{i}", "farlamp_fogbank_a" if big else "farlamp_fogbank_b",
              (x, y), 4 if big else 3, 2, solid=False, hidden_when_flag=DAWN)
    s.kin("amb_fathomere", (8, 22), 173, radius=1)
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
    """Gullwrack Isle — gull-cliffs, ledges, tall sea-grass (walkthrough/10 §4).
    A TALL, NARROW isle hugging the mainland's sea-cliffs, opening west like a
    claw round a gull-loud cove. Its signature is HEIGHT, in three tiers: the
    high gull-cliffs (nests on top), the GULL WALK (a grass ledge between the
    two cliff bands, climbed from the east beach, running out along the headland
    to look down on the SEA ARCH), and the lower face with the Undertide I mouth.
    South of that, the HIGH MEADOW (a cliff-rimmed sea-grass shelf you climb into
    from the north and hop out of by its south ledge) and the KEEPER'S BOTHY on
    the cove's south lobe (rest point). Nesting rocks stand in the cove."""
    s = Sea("farlamp_gullwrack", "Gullwrack Isle", 27, 34, seed=1775,
            backdrops=ISLE_BACKDROPS)
    W, H = s.W, s.H

    def body(g):
        mk.blob(g, W, H, 15.5, 18.5, 6.8, 13.0)       # the spine
        mk.rect(g, W, H, 8, 2, 22, 10)                 # the cliffs' footing
        mk.blob(g, W, H, 8.5, 6.8, 4.2, 3.0)           # the gull headland, NW
        mk.blob(g, W, H, 6.5, 23.5, 4.3, 4.4)          # the bothy lobe, SW
        mk.rect(g, W, H, 8, 18, 12, 23)
        mk.blob(g, W, H, 19, 27, 4.4, 4.0)             # the south fields
    s.land(body)
    mk.blob(s.water, W, H, 3.5, 14.5, 4.2, 3.3)            # the cove bites in, west
    mk.blob(s.water, W, H, 12.5, 31.5, 2.2, 1.4)           # a south inlet
    rim = mk.make_grid(W, H)
    for y in range(H):
        for x in range(W):
            i = s.cell(x, y)
            if s.water[i]:
                continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and s.water[s.cell(x + dx, y + dy)]
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                rim[i] = 1
    mk.blob(rim, W, H, 21.8, 15, 2.2, 3.2)
    for i, v in enumerate(rim):
        if v and not s.water[i]:
            s.sand[i] = 1
    # THE TIERS. Upper: the gull-cliffs proper (rows 2-3). Lower: the long face
    # from the headland to the cave (rows 6-8). Between them, the gull walk.
    mk.rect(s.cliff, W, H, 9, 2, 20, 3)
    mk.blob(s.cliff, W, H, 14.5, 2.2, 6.4, 1.2)
    mk.rect(s.cliff, W, H, 9, 4, 12, 4)                     # a buttress steps the walk in
    mk.rect(s.cliff, W, H, 5, 6, 17, 8)
    mk.rect(s.cliff, W, H, 5, 9, 10, 9)                     # the headland's face runs deeper
    mk.blob(s.cliff, W, H, 11, 7.2, 7.4, 1.4)
    for i in range(W * H):
        if s.cliff[i]:
            s.sand[i] = 0
            s.water[i] = 0
    for y in range(H):
        for x in range(W):
            if y < 2 or (y < 4 and not 9 <= x <= 20):
                s.cliff[s.cell(x, y)] = 0
            if y == 5 or (y == 4 and not 9 <= x <= 12) or (y == 9 and x >= 11):
                s.cliff[s.cell(x, y)] = 0
            if x >= 18 and 4 <= y <= 9:
                s.cliff[s.cell(x, y)] = 0
    for x in (12, 13, 14):                # keep the cave's floor clear below the face
        s.cliff[s.cell(x, 9)] = 0
        s.cliff[s.cell(x, 10)] = 0
    # the mainland's sea-cliffs, east edge (Dimglass Coast's west wall)
    for y in range(3, H):
        x0 = 24 if (y // 4) % 3 == 1 else 25
        for x in range(x0, W):
            s.cliff[s.cell(x, y)] = 1
            s.water[s.cell(x, y)] = 0
            s.sand[s.cell(x, y)] = 0
        s.sand[s.cell(x0 - 1, y)] = 1
        s.water[s.cell(x0 - 1, y)] = 0
    # the gull walk is turf, not beach
    for y in (4, 5):
        for x in range(5, 23):
            if not s.water[s.cell(x, y)]:
                s.sand[s.cell(x, y)] = 0
    # THE HIGH MEADOW (the third tier)
    pt.terrace(s.cliff, s.deco, W, H, pt.Area(13, 16, 23, 25), gap=(17, 18), gap_side="up",
               rim=2, rng=s.rng)
    for y in range(16, 26):
        for x in range(13, 24):
            s.sand[s.cell(x, y)] = 0
    tufts(s, s.tallgrass, [(18, 20.5, 2.6), (10.6, 14.0, 2.2), (11.5, 26.0, 2.0)])
    dunes(s, [(20, 28.3, 3.0, 1.6, True), (7.5, 21.5, 1.8, 1.2, False), (17.5, 12.5, 1.6, 1.0, False)])
    # the lanes: the east landing west to the cave; up to the gull walk; a fork
    # into the meadow; south-west down to the bothy
    lane(s, [(23, 15), (20, 15), (20, 13), (16, 13), (16, 11), (13, 11), (13, 10)])
    lane(s, [(20, 13), (21, 13), (21, 6), (20, 6), (20, 5), (18, 5)])
    lane(s, [(16, 13), (16, 15), (17, 15), (17, 16)])
    lane(s, [(16, 15), (12, 15), (12, 18), (9, 18), (9, 21), (8, 21), (8, 24), (7, 24)])
    for i in range(W * H):
        if s.water[i] or s.sand[i] or s.path[i] or s.cliff[i]:
            s.tallgrass[i] = 0

    # the cave mouth (contract) + marker
    wm.add(s.m, wm.marker("undertide_mouth", "cave_mouth", GULL_MOUTH[0], GULL_MOUTH[1] - 1))
    warp(s.m, "to_undertide", GULL_MOUTH, "undertide_i", (15, 26), "up")
    # THE SEA ARCH off the headland's tip: row through it (its legs stand on rock)
    s.obj("sea_arch", "farlamp_sea_arch", (1, 6), 3, 3, walk_under=True, solid=False)
    boulders(s, [(1, 7), (1, 8), (3, 7), (3, 8)])
    # nests on both cliff tiers, nesting rocks in the cove
    for i, (x, y) in enumerate(((10, 2), (13, 2), (17, 2), (20, 3), (7, 6), (15, 6))):
        s.obj(f"cliff_nest_{i}", "pearlmoor_gull_nest", (x, y), 1, 1, solid=False)
    s.obj("nest_rock_a", "farlamp_nest_rock", (2, 12), 2, 2)
    s.obj("nest_rock_b", "farlamp_nest_rock", (5, 15), 2, 2)
    s.obj("nest_rock_c", "farlamp_nest_rock", (1, 30), 2, 2)
    s.cache("gull_spur", (6, 5))
    # the keeper's bothy (rest point) + its lamp, nets, woodpile
    s.obj("keeper_hut", "farlamp_keeper_hut", GULL_HUT, 4, 4, overhang=2)
    warp(s.m, "to_hut", GULL_HUT_DOOR, "gullwrack_hut", (5, 7), "up", transition="door")
    s.obj("hut_lamp", "tinderwick_lamp_post", (10, 22), 1, 3, overhang=2, walk_under=True)
    s.obj("hut_nets", "pearlmoor_net_rack", (3, 25), 2, 1)
    s.obj("hut_pots", "pearlmoor_crab_pots", (10, 25), 1, 1)
    s.obj("hut_wood", "tinderwick_woodpile", (10, 20), 2, 1)
    s.sign("gullwrack_hut", (9, 24))
    # the high meadow: a bent pine, the meadow cache
    s.obj("meadow_pine", "windward_bent_pine", (20, 18), 2, 3, overhang=2, walk_under=True)
    s.cache("gull_meadow", (15, 22))
    # the east landing + the south shore
    s.obj("landing_boat", "pearlmoor_rowboat", (22, 17), 2, 2)
    s.obj("landing_drift", "pearlmoor_driftwood", (21, 11), 2, 1, solid=False)
    s.obj("spur_ribs", "pearlmoor_wreck_ribs", (17, 30), 3, 2)
    s.obj("cove_pine", "windward_bent_pine", (9, 10), 2, 3, overhang=2, walk_under=True)
    s.obj("south_tree", "tinderwick_tree_b", (12, 27), 3, 4, overhang=3, walk_under=True)
    for (x, y, sh) in ((10, 16, "L"), (19, 10, "J"), (4, 27, "O"), (22, 22, "L"),
                       (15, 25, "J"), (14, 29, "T")):
        outcrop(s, x, y, sh)
    s.kin("amb_beaconclaw", (18, 28), 175, radius=1)
    s.kin("amb_fathomere", (5, 27), 173, radius=1)
    s.kin("amb_frigalance", (18, 21), 96, radius=1)
    s.kin("amb_gullwalk", (14, 4), 76, radius=1)
    blooms(s, [(10, 12), (15, 17), (11, 19), (3, 24), (14, 24), (16, 24),
               (19, 12), (10, 28), (16, 4), (19, 4), (7, 5)])
    for (cx, cy, n) in ((6, 1, 2), (1, 21, 2), (11, 33, 3), (21, 32, 2), (5, 18, 2)):
        sea_rocks(s, cx, cy, n)
    sea_buoys(s, [(4, 1), (18, 1), (1, 11), (23, 31), (4, 32)])
    s.m["ambience"] = sea_ambience(flocks=[(10, 3), (17, 3), (4, 7), (3, 14), (18, 20)])
    return s


# =============================================================================
#  KELPCROWN ISLE
# =============================================================================
KELP_MOUTH = (10, 9)          # contract: to_undertide @ (10,9), landing (10,10)


def build_kelpcrown() -> Sea:
    """Kelpcrown Isle — the old keepers' quarter in ruins (walkthrough/10 §4).
    LOW and WIDE, shaped like its name: a crown. A long band of land across the
    north (a low brow of rock over the Undertide II mouth, the keepers' quarter
    of broken walls east), and three points running south — the kelp-terraced
    west arm, the DROWNED COURTYARD on the middle tongue (its gate, pillars and
    pool on land; its far half and a broken arch standing in the lagoon), and
    the east arm with the landing — with two shallow LAGOONS between them."""
    s = Sea("farlamp_kelpcrown", "Kelpcrown Isle", 30, 34, seed=1776,
            backdrops=ISLE_BACKDROPS)
    W, H = s.W, s.H

    def body(g):
        mk.blob(g, W, H, 16, 9.5, 12.8, 4.8)        # the crown's band
        mk.blob(g, W, H, 6.3, 20.5, 3.4, 9.0)       # the west point
        mk.blob(g, W, H, 15, 17.0, 2.9, 5.2)        # the middle tongue (the courtyard)
        mk.blob(g, W, H, 24.3, 19.5, 3.4, 8.0)      # the east point
        mk.blob(g, W, H, 7.5, 28.5, 3.2, 2.2)       # the west point's foot
    s.land(body)
    # the lagoons between the points stay shallow (Tidecall swims them)
    for y in range(12, 28):
        for x in range(8, 23):
            s.no_deep.add((x, y))
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
    mk.blob(rim, W, H, 26.2, 19.5, 1.6, 3.0)      # the east landing
    for i, v in enumerate(rim):
        if v and not s.water[i]:
            s.sand[i] = 1
    # the brow: a low run of rock over the Undertide II mouth
    mk.blob(s.cliff, W, H, 9.6, 6.7, 4.4, 2.1)
    mk.blob(s.cliff, W, H, 6.6, 6.0, 1.9, 1.3)
    mk.blob(s.cliff, W, H, 12.8, 5.8, 1.7, 1.2)
    for i in range(W * H):
        if s.cliff[i]:
            s.sand[i] = 0
            s.water[i] = 0
    for x in range(3, 16):
        s.cliff[s.cell(x, 9)] = 0
    for x in (9, 10, 11):
        s.cliff[s.cell(x, 10)] = 0
    # the keepers' quarter (north-east) and the drowned courtyard (the tongue)
    mk.blob(s.ruin, W, H, 21, 8.6, 4.6, 2.4)
    mk.rect(s.ruin, W, H, 13, 13, 17, 19)
    # the courtyard's pool: the sea came up through its flags
    mk.blob(s.pond, W, H, 15, 16.8, 1.3, 1.2)
    # kelp terraces down the west point: two benches hopped by ledges
    for (y, x0, x1) in ((19, 3, 9), (24, 3, 10)):
        for x in range(x0, x1 + 1):
            i = s.cell(x, y)
            if not s.water[i] and not s.sand[i] and not s.cliff[i]:
                s.deco[i] = gid("grass_ledge_s_v1" if x % 4 == 0 else "grass_ledge_s")
    for (y, x) in ((19, 6), (24, 6)):           # each bench keeps a gap (the way back up)
        s.deco[s.cell(x, y)] = 0
    tufts(s, s.tallgrass, [(6.0, 16.0, 2.4), (6.5, 21.6, 2.6), (7.5, 26.6, 2.4),
                           (24.5, 16.0, 1.6), (4.5, 11.2, 1.6)])
    # the lanes: east landing up the east point, west along the band to the brow;
    # the courtyard gate; down the west point
    lane(s, [(26, 19), (25, 19), (25, 13), (21, 13), (21, 12), (15, 12), (15, 11),
             (10, 11), (10, 10)])
    lane(s, [(15, 12), (15, 14)])
    lane(s, [(10, 11), (7, 11), (7, 13), (5, 13), (5, 17), (6, 17), (6, 21), (5, 21),
             (5, 23), (6, 23), (6, 27), (7, 27)])
    dunes(s, [(24.6, 25.0, 1.8, 1.4, True), (6.0, 30.4, 2.0, 1.0, True)])
    # the pool-cache islet in the east lagoon
    bar(s, [(18.2, 25.0), (19.2, 25.0)], r=0.6, shoal=0)
    for i in range(W * H):
        if s.water[i] or s.sand[i] or s.path[i] or s.cliff[i] or s.pond[i] or s.ruin[i]:
            s.tallgrass[i] = 0
        if s.pond[i]:
            s.ruin[i] = 0

    wm.add(s.m, wm.marker("undertide_mouth", "cave_mouth", KELP_MOUTH[0], KELP_MOUTH[1] - 1))
    warp(s.m, "to_undertide", KELP_MOUTH, "undertide_ii", (14, 28), "up")
    # the keepers' quarter: broken walls and standing pillars
    s.obj("ruin_wall_a", "farlamp_ruin_wall", (17, 6), 3, 2)
    s.obj("ruin_wall_b", "farlamp_ruin_wall", (23, 7), 3, 2)
    s.obj("ruin_pillar_a", "farlamp_ruin_pillar", (21, 6), 1, 2)
    s.obj("ruin_pillar_b", "farlamp_ruin_pillar", (18, 9), 1, 2)
    s.obj("ruin_pillar_c", "farlamp_ruin_pillar", (26, 9), 1, 2)
    s.cache("kelpcrown_purse", (24, 10))
    s.sign("kelpcrown_ruins", (20, 11))
    # THE DROWNED COURTYARD: walls with a gate on the north, pillars round the
    # pool, and its south half under the lagoon — a broken arch and two pillars
    # standing in the water where the courtyard used to go on
    s.obj("court_wall_w", "farlamp_ruin_wall", (12, 13), 3, 2)
    s.obj("court_wall_e", "farlamp_ruin_wall", (16, 13), 3, 2)
    s.obj("court_pillar_w", "farlamp_ruin_pillar", (13, 16), 1, 2)
    s.obj("court_pillar_e", "farlamp_ruin_pillar", (17, 16), 1, 2)
    s.obj("drowned_arch", "farlamp_broken_arch", (14, 22), 3, 3, walk_under=True, solid=False)
    boulders(s, [(14, 23), (14, 24), (16, 23), (16, 24)])
    s.obj("drowned_pillar_a", "farlamp_ruin_pillar", (11, 21), 1, 2)
    s.obj("drowned_pillar_b", "farlamp_ruin_pillar", (19, 20), 1, 2)
    s.kin("amb_tidalarch", (15, 19), 61, radius=1)
    # the kelp terraces
    s.obj("terrace_rack_a", "farlamp_kelp_rack", (7, 14), 2, 2)
    s.obj("terrace_rack_b", "farlamp_kelp_rack", (3, 21), 2, 2)
    s.obj("terrace_rack_c", "farlamp_kelp_rack", (7, 25), 2, 2)
    s.cache("kelp_terrace", (8, 28))
    s.cache("kelp_pool", (18, 25))
    s.kin("amb_beaconclaw", (25, 16), 175, radius=1)
    s.kin("amb_fathomere", (4, 26), 173, radius=1)
    s.obj("landing_boat", "pearlmoor_rowboat", (27, 21), 2, 2)
    s.obj("landing_pots", "pearlmoor_crab_pots", (26, 17), 1, 1)
    s.obj("south_ribs", "pearlmoor_wreck_ribs", (16, 29), 3, 2)
    s.obj("crown_pine", "windward_bent_pine", (23, 23), 2, 3, overhang=2, walk_under=True)
    s.obj("ridge_pine", "windward_bent_pine", (4, 8), 2, 3, overhang=2, walk_under=True)
    s.obj("east_tree", "tinderwick_tree_b", (21, 14), 3, 4, overhang=3, walk_under=True)
    for (x, y, sh) in ((8, 31, "J"), (26, 13, "J"), (3, 12, "S"), (27, 7, "L")):
        outcrop(s, x, y, sh)
    blooms(s, [(13, 18), (17, 18), (12, 11), (23, 17), (8, 17), (20, 11), (4, 23), (22, 10)])
    for (cx, cy, n) in ((4, 3, 2), (21, 3, 3), (12, 30, 2), (26, 31, 3), (5, 32, 2)):
        sea_rocks(s, cx, cy, n)
    sea_buoys(s, [(5, 2), (16, 1), (27, 3), (28, 30), (21, 32)])
    s.m["ambience"] = sea_ambience(flocks=[(9, 5), (24, 24), (15, 25)])
    return s


# =============================================================================
#  the seams + the mainland side
# =============================================================================
# Lightkeeper's Point's south edge <-> the Sound's north edge, and the Wick-Run
# Foot's south edge <-> the Shelfwater's north edge — through the two launch
# SLIPS only (their planks run down to the map edge): you put out from a slip and
# come home to it. The rest of both seams is open deep water with no warp (the
# mainland's harbour shallows). The mainland builders own their side
# (build_pearlmoor_point.py / build_wickrun_foot.py: AFLOAT-gated warps on the
# slip's last plank, with a "no boat" line).
POINT_SEAM = (6, 7)       # the Point's launch slip (its planks run to the edge)
FOOT_SEAM = (9, 10)       # the Wick-Run Foot's slip


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
    for s in maps:
        s.assemble()
        sea_zones(s)
        s.scatter(0.10)
        strand(s)
    # The five maps warp into each other, and each finalize() audits its warps
    # against the OTHERS' shipped JSON — so write them all once first (silently),
    # then finalize for real against a consistent set.
    import copy
    import json as _json
    for s in maps:
        (mk.REPO / "public/assets/maps" / f"{s.id}.json").write_text(
            _json.dumps(copy.deepcopy(s.m), indent=2) + "\n")
    ok = True
    for s in maps:
        print(f"== {s.id}")
        ok = s.finalize() and ok
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
