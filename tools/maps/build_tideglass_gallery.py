#!/usr/bin/env python3
"""
Tideglass Gallery — the cavern's B1F: one small chamber where the relayed
beam pools, and the DUSK HOUR waits (walkthrough/07-the-three §4 — the
game's first legendaryBattle site; the glowmoss_deep_b1f floor pattern).

Stair pairing (audited): cavern (23,15) stair_down -> lands ON this floor's
stair_up at (14,3), and back. The approach to the Hour is a 1-wide glass
spit (x4-7, y9) so the staging cannot be walked around; GLOAMBER itself is
the interact placement `hour_dusk` (sprite kin_160_overworld — lazy
creature-sprite path, placeholder until #160 is packed by the species
package), hidden for good once flag:three_dusk_caught is set.

NO encounter zones — the Hour's room is quiet (hooks verbatim). Trainer-free.

The set-piece script (wiring pass, content/scripts.ts — hooks VERBATIM):
  'script.three_dusk_battle': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'The glass warms. Something that has carried the
      evening a long time lifts its head.' },
    { op: 'letterbox', on: false },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    { op: 'legendaryBattle', name: 'three_dusk', kin: 160, level: 38,
      caughtFlag: 'flag:three_dusk_caught', cooldownBattles: 10,
      cooldownRef: 'npc.three_dusk_resting', terrain: 'cave' },
  ]

audit_flow WAIVER — `loop`/dead-end WARNs accepted: a single-chamber shrine
floor (the beacon-top tier); the stair is its own return.

Run:  ./venv/bin/python tools/maps/build_tideglass_gallery.py
"""
from __future__ import annotations
import random
import mapkit as mk
from mapkit import gid

W, H = 18, 14
rng = random.Random(161)

STAIR_UP = (14, 3)        # pairs with tideglass_cavern's stair_down at (23,15)
HOUR_AT = (2, 9)          # the far ledge, beyond the 1-wide glass spit

# ---- terrain: solid glass-rock, the gallery carved ----------------------------------
wall = mk.make_grid(W, H)
mk.rect(wall, W, H, 0, 0, W - 1, H - 1)


def carve(x0, y0, x1, y1):
    mk.rect(wall, W, H, x0, y0, x1, y1, 0)


carve(12, 2, 15, 5)        # the stair room
carve(13, 6, 14, 7)        # the descent throat
carve(8, 8, 15, 11)        # the beam-pool antechamber
carve(4, 9, 7, 9)          # THE GLASS SPIT (1-wide — the un-walk-aroundable approach)
carve(2, 8, 3, 10)         # the Hour's far ledge

# the pooled relayed light: a sunpool lobe + tideglass sheen around the ledge
pool = mk.make_grid(W, H)
mk.blob(pool, W, H, 11.0, 11.0, 1.8, 1.0)
glass = mk.make_grid(W, H)
mk.rect(glass, W, H, 2, 8, 3, 10)          # the ledge is solid tideglass
mk.rect(glass, W, H, 4, 9, 7, 9)           # ...so is the spit
mk.blob(glass, W, H, 9.5, 8.5, 1.4, 1.0)
moss = mk.make_grid(W, H)
for (x, y) in [(12, 8), (14, 10), (9, 11), (13, 5)]:
    moss[y * W + x] = 1

for i in range(W * H):
    if wall[i]:
        pool[i] = glass[i] = moss[i] = 0
    if pool[i]:
        glass[i] = moss[i] = 0
    if glass[i]:
        moss[i] = 0

cf = [gid("cavefloor0"), gid("cavefloor1"), gid("cavefloor2"), gid("cavefloor3")]
base = [rng.choice(cf) if rng.random() < 0.55 else cf[0] for _ in range(W * H)]

terrain_layers = [
    {"name": "t_glass", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": glass},
    {"name": "t_moss", "role": "terrain", "terrain": "glowmoss",
     "set": "vesper_overworld_set", "depth": 0, "data": moss},
    {"name": "t_pool", "role": "terrain", "terrain": "sunpool",
     "set": "vesper_overworld_set", "depth": 0, "data": pool},
    {"name": "t_wall", "role": "terrain", "terrain": "cavewall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

deco = mk.make_grid(W, H)
deco[STAIR_UP[1] * W + STAIR_UP[0]] = gid("cave_ladder_up")
# the gallery is nearly bare — two glints, one shroom (the beam does the talking)
deco[8 * W + 9] = gid("g_pebble")
deco[10 * W + 15] = gid("glowshroom_b")
deco[5 * W + 12] = gid("g_pebble")

m: dict = {
    "id": "tideglass_gallery", "display_name": "Tideglass Gallery",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "cave",
    "tilesets": [mk.shared_tileset_ref()],
    "layers": [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
        {"name": "deco", "role": "deco", "depth": 5, "data": deco},
        {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
    ],
    "objects": [
        # one tideglass spire over the pooled light — the chamber's only landmark
        {"id": "spire", "sprite": "tideglass_glass_spire",
         "at": {"tx": 10, "ty": 8}, "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    ],
    "warps": [
        # the stair back up — lands ON the cavern's stair seam (mutual pair)
        {"id": "stair_up", "at": {"tx": STAIR_UP[0], "ty": STAIR_UP[1]},
         "trigger": "step_on", "to_map": "tideglass_cavern", "to": {"tx": 23, "ty": 15},
         "facing": "up", "transition": "fade"},
    ],
    "triggers": [],
    "encounters": [],   # the Hour's room is quiet (hooks verbatim)
    "npcs": [
        # THE DUSK HOUR — a long, low shape that has been waiting for someone
        # to bring the evening's ember back to it. Interact -> the set-piece.
        {"id": "hour_dusk", "at": {"tx": HOUR_AT[0], "ty": HOUR_AT[1]},
         "facing": "right", "sprite": "kin_160_overworld", "movement": "static",
         "dialogue_ref": "script.three_dusk_battle",
         "hidden_when_flag": "flag:three_dusk_caught"},
    ],
    "gates": [],
    "music": "assets/audio/music/dimglass-coast-c.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/tideglass-gallery-a.webp",
    ],
}

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    print("content refs owed by this map (register in src/game/content/):")
    for ref in ["script.three_dusk_battle (the op VERBATIM in the docstring; "
                "sets flag:three_dusk_caught via the op)",
                "npc.three_dusk_resting (the {remaining} cooldown hint — "
                "07-the-three §7 verbatim)"]:
        print(f"  - {ref}")
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
