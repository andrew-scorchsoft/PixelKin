#!/usr/bin/env python3
"""
Emberroot's Heart — the bottom of the Old Seams (09-the-wild-ways §2 D; kind
cave, region east, no encounters). The legendary's room.

At the root of Cinderhead the mountain is built around THE FIRST STAR THAT EVER
FELL — so long ago it was never a "fall" in anyone's memory. It is not a cold
cinder: it never guttered. It sits half-sunk in a mound of root-rock, warm as a
banked hearth, and the cinder-coal the miners dig is its breath, cooling very
slowly in the stone (cinder law rule 5). Its kin, EMBERROOT (#166, Stone/Ember),
sleeps curled at its foot.

The room is one beat (07-the-three's set-piece grammar): step down off the
foremen's last ladder and the band across the nook mouth stages the awe
(`script.emberroot_heart_enter`, once); Emberroot at the star's foot runs the
`legendaryBattle` (lv 46, cooldown 12 won battles, `npc.emberroot_resting`).
The star itself answers Confirm (`script.emberroot_star`), before and after.
A cache in the west fold keeps the Foreman's Ledger's LAST PAGE — the one
"past the lamp's reach" (02-east E3).

The way in is gated a floor up on the derived Lamplight tier (old_seams_iii
`to_heart`, `flag:lamplight_starlight` — six Gleams), so this is a return trip.

HANDSHAKE: `ladder_up` (9,3) <-> old_seams_iii's `to_heart` (14,26).

Run:  python3 tools/maps/build_emberroot_heart.py
"""
from __future__ import annotations

import random

import mapkit as mk
import patterns as pt
import seamskit as sk
from mapkit import gid

W, H = 20, 16
rng = random.Random(16604)
owed: list[str] = []

wall = sk.grid(W, H)
shaft = sk.grid(W, H)
deco = sk.grid(W, H)
above = sk.grid(W, H)
sk.fill(wall, W, 0, 0, W - 1, H - 1)

FLOOR = {(x, y) for y in range(H) for x in range(W)
         if ((x - 9.5) / 8.2) ** 2 + ((y - 8.9) / 5.6) ** 2 <= 1.0}
FLOOR |= sk.cells(8, 2, 10, 3)                   # the nook under the last ladder
FLOOR = {(x, y) for (x, y) in FLOOR if 1 <= x < W - 1 and 1 <= y < H - 1}
for (x, y) in FLOOR:
    wall[y * W + x] = 0

m: dict = {
    "id": "emberroot_heart", "display_name": "Emberroot's Heart",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [], "gates": [],
    "music": sk.MUSIC, "battle_backdrops": list(sk.BACKDROPS),
}
sk.use_seams(m)

pin = {(x, y): f"cinder_{(x * 5 + y * 3) % 3}" for (x, y) in FLOOR}
pt.cave_ladder(m, deco, W, kind="up", at=(9, 3), to_map="old_seams_iii", to=(14, 26))

# ---- the first star, and the one who sleeps at its foot --------------------------
sk.obj(m, "first_star", "old_seams_first_star", (8, 6), 4, 4, overhang=2)
m["npcs"].append({"id": "emberroot", "at": {"tx": 9, "ty": 10}, "facing": "down",
                  "sprite": "kin_166_overworld", "movement": "static",
                  "dialogue_ref": "script.emberroot_wake",
                  "hidden_when_flag": "flag:emberroot_caught"})
for x in range(8, 12):
    m["triggers"].append({"id": f"first_star_{x}", "kind": "script", "at": {"tx": x, "ty": 9},
                          "activation": "interact", "ref": "script.emberroot_star"})
# the awe beat: every walkable tile of the nook's mouth (it can't be walked round)
for x in range(W):
    if (x, 4) in FLOOR:
        m["triggers"].append({"id": f"heart_enter_{x}", "kind": "cutscene",
                              "at": {"tx": x, "ty": 4}, "activation": "step_on",
                              "ref": "script.emberroot_heart_enter",
                              "sets_flags": ["flag:emberroot_heart_seen"],
                              "hidden_when_flag": "flag:emberroot_heart_seen"})
owed += ["script.emberroot_wake", "script.emberroot_star", "script.emberroot_heart_enter",
         "npc.emberroot_resting"]

# ---- the roots of the room: veins running out from the star -----------------------
for (oid, at) in [("vein_w", (4, 9)), ("vein_e", (14, 8)), ("vein_s", (11, 12)),
                  ("vein_sw", (5, 12))]:
    sk.obj(m, oid, "old_seams_cinder_vein", at, 2, 2, solid=False)
sk.obj(m, "crystal_w", "cinderhead_crystal_cluster", (2, 6), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "crystal_e", "cinderhead_crystal_cluster", (16, 10), 2, 2, overhang=1, walk_under=True)
sk.obj(m, "props_nook", "old_seams_timber_props", (10, 2), 2, 2, overhang=1, walk_under=True)
for (x, y, n) in [(7, 8, "vein_a"), (12, 7, "vein_b"), (6, 6, "vein_b"), (13, 11, "vein_a"),
                  (8, 12, "vein_b"), (15, 6, "vein_a"), (3, 11, "vein_b"), (16, 12, "vein_a"),
                  (10, 13, "vein_b")]:
    deco[y * W + x] = sk.S(n)

owed += pt.cache(m, cid="seams_ledger_page", at=(2, 9))

sk.finish(m, W, H, wall=wall, shaft=shaft, deco=deco, above=above, rng=rng, floor_mix=0.3)

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3, pin_base=pin)
    if owed:
        print("CONTENT OWED:", owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
