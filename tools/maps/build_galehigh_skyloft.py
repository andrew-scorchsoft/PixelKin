#!/usr/bin/env python3
"""
Galehigh Skyloft — the winch-festival venue + Mira's launch ledge
(walkthrough/03-north, Galehigh beat 5-6; the §5 shape-#5 loop's payoff map).

A wind-raked top terrace (~18x12) above the Kite-rising: reached ONLY by the
great winch (`galehigh_terraces.to_skyloft`, gated on flag:q_north_kite_blessed
— the festival flag, NEVER Updraft; spine §0 rule 1). Two wind-ward SIGHT
trainers (lv 29-31 — author TRAINERS to that band) hold the crossing; the
LAUNCH LEDGE at the head carries Mira's bond-test (script.lumenary_galehigh,
`blocked_ref: npc.mira_not_ready` until blessed, per the validation hooks).
Win -> TRAINERS['mira_vael'] grants `reward_flags: ['gleam:storm']` +
`reward_abilities: ['updraft_kite']` (the Lampwarden pattern — Reyl Wash is
the worked example); the glide down is the Gift's first taste.

Return half: `winch_down` at (9,10) lands ON the terraces' to_skyloft warp at
(21,18) — the mutual ladder-pair convention; audit_warps proves it.

Run:  ./venv/bin/python tools/maps/build_galehigh_skyloft.py
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 18, 12
rng = random.Random(57)
owed: list[str] = []

# ---- terrain ----------------------------------------------------------------------
glacier = mk.make_grid(W, H)
snowpatch = mk.make_grid(W, H)

# the crag enclosure: 2-deep north head, side walls, the south drop edge
mk.rect(glacier, W, H, 0, 0, W - 1, 1)
mk.rect(glacier, W, H, 0, 0, 1, H - 1)
mk.rect(glacier, W, H, 16, 0, 17, H - 1)
mk.rect(glacier, W, H, 0, H - 1, W - 1, H - 1)
# the launch-ledge NECK: shoulders close to a 2-wide head at x8..9
mk.rect(glacier, W, H, 2, 2, 7, 4)
mk.rect(glacier, W, H, 10, 2, 15, 4)

# the snowline dusts the loft (snow-over-grass blobs — context-correct)
for (bx, by, brx, bry) in [(4, 6, 1.8, 1.2), (13, 5.5, 1.6, 1.0), (8, 2.5, 1.4, 1.0),
                           (15, 9, 1.4, 1.0)]:
    mk.blob(snowpatch, W, H, bx, by, brx, bry)
for i in range(W * H):
    if glacier[i]:
        snowpatch[i] = 0

# ---- base: wind-raked grass with scree patches -------------------------------------
gg = [gid("grass0"), gid("grass1"), gid("grass2"), gid("grass3")]
base = [rng.choice(gg) if rng.random() < 0.5 else gg[0] for _ in range(W * H)]
for (sx, sy) in [(6, 9), (7, 9), (6, 10), (3, 8), (10, 5), (11, 5), (10, 6),
                 (8, 9), (9, 9), (10, 9), (8, 10), (9, 10), (10, 10)]:
    i = sy * W + sx
    if not glacier[i] and not snowpatch[i]:
        base[i] = gid(f"scree{rng.randrange(3)}")

terrain_layers = [
    {"name": "t_snowpatch", "role": "terrain", "terrain": "snowpatch",
     "set": "vesper_overworld_set", "depth": 0, "data": snowpatch},
    {"name": "t_glacier", "role": "terrain", "terrain": "glacierwall",
     "set": "vesper_overworld_set", "depth": 0, "data": glacier},
]

deco = mk.make_grid(W, H)

m: dict = {
    "id": "galehigh_skyloft", "display_name": "Galehigh Skyloft",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [
        # the winch's TOP STATION (the drum the rope rises to)
        {"id": "winch_top", "sprite": "galehigh_winch", "at": {"tx": 12, "ty": 6},
         "w": 4, "h": 5, "overhang": 3, "walk_under": True},
        # a festival kite snapping over the west pocket
        {"id": "kite_loft", "sprite": "galehigh_kite_pole_a", "at": {"tx": 2, "ty": 5},
         "w": 2, "h": 3, "overhang": 2, "walk_under": True},
    ],
    "warps": [
        # the winch ride back down — lands ON the terraces' to_skyloft warp
        # (the mutual pair convention; the engine never auto-fires on arrival)
        {"id": "winch_down", "at": {"tx": 9, "ty": 10}, "trigger": "step_on",
         "to_map": "galehigh_terraces", "to": {"tx": 21, "ty": 18}, "facing": "down",
         "transition": "fade"},
    ],
    "triggers": [
        # MIRA'S BOND-TEST at the launch ledge — bands the whole 2-wide neck
        # (hooks: blocked until blessed, in Mira's voice; hidden once Storm
        # relights so the loft stays free to revisit)
        {"id": "mira_battle_w", "kind": "cutscene", "at": {"tx": 8, "ty": 4},
         "activation": "step_on", "ref": "script.lumenary_galehigh", "once": True,
         "requires_flag": "flag:q_north_kite_blessed",
         "blocked_ref": "npc.mira_not_ready",
         "hidden_when_flag": "gleam:storm"},
        {"id": "mira_battle_e", "kind": "cutscene", "at": {"tx": 9, "ty": 4},
         "activation": "step_on", "ref": "script.lumenary_galehigh", "once": True,
         "requires_flag": "flag:q_north_kite_blessed",
         "blocked_ref": "npc.mira_not_ready",
         "hidden_when_flag": "gleam:storm"},
    ],
    "encounters": [],   # the loft is a trainer gauntlet, not a wild bed
    "npcs": [
        # Mira at the head, flying — pre-Gleam, then the send-off after
        {"id": "mira_vael", "at": {"tx": 8, "ty": 2}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "static",
         "dialogue_ref": "npc.mira_skyloft",
         "hidden_when_flag": "gleam:storm"},
        {"id": "mira_vael_after", "at": {"tx": 8, "ty": 2}, "facing": "down",
         "sprite": "npc_lampwarden", "movement": "look_around",
         "dialogue_ref": "npc.mira_skyloft_after",
         "requires_flag": "gleam:storm"},
    ],
    "gates": [],
    # spur maps reuse the parent loop + backdrops (Phase-0 reuse table; alt
    # variant windward-stair-b is available if the wiring agent wants contrast)
    "music": "assets/audio/music/galehigh-terraces-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/galehigh-terraces-a.webp",
        "assets/backgrounds/battle/galehigh-terraces-b.webp",
    ],
}
owed += ["script.lumenary_galehigh (Mira's bond-test battle; TRAINERS['mira_vael'] "
         "ace ~34, reward_flags ['gleam:storm'], reward_abilities ['updraft_kite'])",
         "npc.mira_not_ready", "npc.mira_skyloft", "npc.mira_skyloft_after"]

# the two wind-ward SIGHT trainers (lv 29-31) — their lines cover the crossing
owed += pt.trainer_beat(m, tid="skyloft_ward_a", at=(5, 6), facing="right",
                        sight=4, sprite="npc_woman")
owed += pt.trainer_beat(m, tid="skyloft_ward_b", at=(11, 8), facing="left",
                        sight=4, sprite="npc_man")

# a charge cache pays the west pocket (cache-variety: consumable up high)
owed += pt.cache(m, cid="skyloft_charge", at=(3, 9))

# boulders + wind-scoured scatter
for (x, y) in [(14, 5), (2, 8), (10, 9)]:
    deco[y * W + x] = gid("boulder")
object_cells = {(x, y) for o in m["objects"]
                for y in range(o["at"]["ty"], o["at"]["ty"] + o["h"])
                for x in range(o["at"]["tx"], o["at"]["tx"] + o["w"])}
point_cells = {(p["at"]["tx"], p["at"]["ty"])
               for p in m["npcs"] + m["triggers"] + m["warps"]}
covered = {(x, y) for y in range(H) for x in range(W)
           if glacier[y * W + x] or snowpatch[y * W + x]}
mk.scatter_decor(deco, base, W, H, rng, density=0.14,
                 avoid=covered | object_cells | point_cells)

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=4)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
