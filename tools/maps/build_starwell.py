#!/usr/bin/env python3
"""
Starwell — the well of fallen starlight (walkthrough 05-central-endgame,
Penumbra Ring §4; atlas §3 landmark row "Starwell · landmark (post-Crown) ·
Penumbra Ring · Starreach · a near-legendary kin"). One screen, kind route
(an open-air shrine under the great dark, not a cave), region central,
`optional: true` in graph.ts. NO wild encounters, NO trainers, NO people —
the SILENCE register: the quietest, most beautiful small map in the game.

THE KIN — Lunaveil #132 (Lunar, E-tier, the near-legendary): the decision
chain, documented per the C1 contract —
  * 05 §4/§6: Starwell rewards "a near-legendary kin (post-Crown)", encoded
    as "a fixed/low-weight EncounterZone or one-off EventTrigger per atlas §3".
  * The W4 builder (build_nightreach.py) deliberately LEFT #132 unplaced:
    "its entry has Nessa still tracking it; it reads as a post-dawn /
    Central-writer payoff, not a town wild."
  * 06-postgame's unplaced-register table: "Lunaveil #132 · left for
    Starwell (Central writer's 'near-legendary')."
  * X3 "Charting the Dark" (04-west) rewards the chart that NAMES Starwell —
    the tease this map closes.
  * The species file: `scripted: true`, `encounters: []` — the scripted-
    legendary convention; it must NOT enter an open table. So: a fixed
    EventTrigger set-piece via the `legendaryBattle` op (LegendaryBattleStep,
    content/types.ts — catch joins the party/Hearth via the normal path; a
    KO/flee withdraws it for N WON battles, the right shape for a [MUST-DO]
    one-off: missable never, lost-forever never). Level 54: above the ~52
    entry band, under Keylumen's 55 — the Spire ramp untouched.
The trigger band is the basin's south face (interact, all four tiles),
`hidden_when_flag: flag:lunaveil_caught` (the caughtFlag gates the staging
trigger too, per the types.ts worked example); a post-catch read takes the
same tiles on `requires_flag` so the well still answers afterwards.

Suggested content (wiring agent C3; the cooldown values are the types.ts
worked example's, tuned to the endgame):
  script.starwell_lunaveil   narrate (the pool stirs; a vast wing crosses
                             the starlight) -> silence -> musicSting ->
                             { op: 'legendaryBattle', name: 'lunaveil',
                               kin: 132, level: 54,
                               caughtFlag: 'flag:lunaveil_caught',
                               cooldownBattles: 12,
                               cooldownRef: 'npc.starwell_still' }
  npc.starwell_still         "The pool lies flat. Whatever rose from it has
                             sunk deep again; the starlight will not give it
                             up for {remaining} more battles yet."
  npc.starwell_after         (post-catch): "The well holds only starlight
                             now — and holds it gladly. The water is warm."
  script.pickup_starwell_amber  Moth-amber (valuable) + the find line

Three signature touches (§8):
  1. THE WELL ITSELF — the drawn basin hero piece, pooled white-cyan light
     in a bone-basalt rim, set in a frozen pool of ICE (fallen light,
     crystallised at the edges) — the one bright thing in the whole dark.
  2. FALLEN STARS — bright starglint decals across the ice and floor (the
     nightreach sky decals' grounded siblings): the sky came DOWN here.
  3. THE CRACK IT FELL THROUGH — a thin void crescent merged into the NE
     rim, rimming the bright pool with the dark it answered.

HANDSHAKE (C1-internal, built both sides): our `to_penumbra`/`to_penumbra_s`
at (0,8)/(0,9) (Starreach both ways — the graph.ts:235 bidir edge) land at
penumbra_ring (27,13)/(27,14) ON its `to_starwell` pair, which lands back ON
ours. Entered walking east, left walking west — seam continuity kept.

audit_flow waivers: `loop` — a one-screen sanctuary spur enters and leaves
by its one mouth (the §2a "landmark" tier; nothing to compress).
"""
from __future__ import annotations
import random
import mapkit as mk
import patterns as pt
from mapkit import gid

W, H = 20, 18
rng = random.Random(132)
owed: list[str] = []

wall = mk.make_grid(W, H)
void = mk.make_grid(W, H)
ice = mk.make_grid(W, H)
deco = mk.make_grid(W, H)

# BORDERS: basaltwall all round, organically bitten (§11 r2)
mk.rect(wall, W, H, 0, 0, W - 1, 1)
mk.rect(wall, W, H, 0, 16, W - 1, H - 1)
mk.rect(wall, W, H, 0, 0, 1, H - 1)
mk.rect(wall, W, H, 18, 0, 19, H - 1)
mk.organic_border(wall, W, H, depth=0,
                  bumps=[(6, 1, 2), (14, 16, 2), (18, 13, 2), (6, 16, 2)],
                  rng=rng)
# WEST gap — the mouth from the Penumbra Ring (rows 8-9)
for x in (0, 1):
    for y in (8, 9):
        wall[y * W + x] = 0

# THE CRACK IT FELL THROUGH (touch #3): a void crescent on the NE rim
mk.blob(void, W, H, 16.0, 3.0, 3.0, 2.0)
mk.blob(void, W, H, 12.5, 2.0, 2.2, 1.4)

# THE FROZEN POOL (touch #1): fallen light, crystallised — walkable ice
mk.blob(ice, W, H, 11.0, 9.0, 4.4, 3.2)

# precedence: wall > void > ice
for i in range(W * H):
    if wall[i]:
        void[i] = 0
        ice[i] = 0
    if void[i]:
        ice[i] = 0

terrain_layers = [
    {"name": "t_ice", "role": "terrain", "terrain": "ice",
     "set": "vesper_overworld_set", "depth": 0, "data": ice},
    {"name": "t_void", "role": "terrain", "terrain": "void",
     "set": "vesper_overworld_set", "depth": 0, "data": void},
    {"name": "t_basaltwall", "role": "terrain", "terrain": "basaltwall",
     "set": "vesper_overworld_set", "depth": 0, "data": wall},
]

bs = [gid("basalt0"), gid("basalt1"), gid("basalt2")]
base = [rng.choice(bs) if rng.random() < 0.5 else bs[0] for _ in range(W * H)]

m: dict = {
    "id": "starwell", "display_name": "Starwell",
    "width": W, "height": H, "tile_width": 16, "tile_height": 16, "kind": "route",
    "tilesets": [mk.shared_tileset_ref()],
    "objects": [], "warps": [], "triggers": [], "encounters": [], "npcs": [],
    "gates": [],
    "music": "assets/audio/music/penumbra-ring-a.mp3",
    "battle_backdrops": [
        "assets/backgrounds/battle/penumbra-ring-a.webp",
        "assets/backgrounds/battle/penumbra-ring-b.webp",
    ],
}

# ---- warps (graph.ts `to_starwell` edge, our return half) ----------------------------
m["warps"] += [
    {"id": "to_penumbra", "at": {"tx": 0, "ty": 8}, "trigger": "step_on",
     "to_map": "penumbra_ring", "to": {"tx": 27, "ty": 13}, "facing": "left",
     "requires_ability": "starreach", "transition": "fade"},
    {"id": "to_penumbra_s", "at": {"tx": 0, "ty": 9}, "trigger": "step_on",
     "to_map": "penumbra_ring", "to": {"tx": 27, "ty": 14}, "facing": "left",
     "requires_ability": "starreach", "transition": "fade"},
]

# ---- THE WELL (touch #1): the hero basin on the pool's north shore --------------------
m["objects"].append(
    {"id": "starwell_basin", "sprite": "penumbra_starwell_basin",
     "at": {"tx": 9, "ty": 5}, "w": 4, "h": 4, "overhang": 2})
# the Lunaveil set-piece band: the basin's whole south face (see docstring)
for i, tx in enumerate((9, 10, 11, 12)):
    m["triggers"].append(
        {"id": f"starwell_kin_{i}", "kind": "script",
         "at": {"tx": tx, "ty": 9}, "activation": "interact",
         "ref": "script.starwell_lunaveil",
         "hidden_when_flag": "flag:lunaveil_caught"})
    m["triggers"].append(
        {"id": f"starwell_after_{i}", "kind": "dialogue",
         "at": {"tx": tx, "ty": 9}, "activation": "interact",
         "ref": "npc.starwell_after",
         "requires_flag": "flag:lunaveil_caught"})
owed += [
    "script.starwell_lunaveil (legendaryBattle: kin 132 lv 54 — see docstring)",
    "npc.starwell_still (the cooldown hint, {remaining})",
    "npc.starwell_after (the post-catch read)",
]

# standing stones of crystallised light flank the pool (frost-register reuse)
m["objects"] += [
    {"id": "light_spire_w", "sprite": "pale_vault_ice_spire",
     "at": {"tx": 5, "ty": 4}, "w": 2, "h": 3, "overhang": 2},
    {"id": "light_spire_e", "sprite": "pale_vault_ice_spire",
     "at": {"tx": 15, "ty": 9}, "w": 2, "h": 3, "overhang": 2},
]

# the last two lamps of the safe line flank the mouth — then the well takes over
for n, (x, y) in enumerate([(2, 4), (2, 10)]):
    m["objects"].append(
        {"id": f"way_lamp_{n}", "sprite": "penumbra_way_lamp",
         "at": {"tx": x, "ty": y}, "w": 1, "h": 3, "overhang": 2,
         "walk_under": True})

# ---- FALLEN STARS (touch #2): bright glints on ice + floor, dim ones beyond -----------
def glint(gx: int, gy: int, sprite: str) -> None:
    m["objects"].append(
        {"id": f"starglint_{gx}_{gy}", "sprite": sprite,
         "at": {"tx": gx, "ty": gy}, "w": 1, "h": 1, "solid": False,
         "walk_under": True})

glint(13, 8, "penumbra_starglint_bright_a")   # on the pool ice
glint(10, 11, "penumbra_starglint_bright_b")
glint(8, 7, "penumbra_starglint_bright_a")
glint(12, 11, "penumbra_starglint_bright_b")
glint(6, 12, "nightreach_starglint_a")        # fading outward onto the basalt
glint(15, 6, "nightreach_starglint_b")
glint(16, 12, "nightreach_starglint_a")
glint(4, 8, "nightreach_starglint_b")
glint(14, 2, "penumbra_starglint_bright_b")   # one in the crack it fell through

# ---- the one paid pocket (§3a r4): Moth-amber behind the SW bump ----------------------
owed += pt.cache(m, cid="starwell_amber", at=(3, 14))

# ---- quiet dressing -------------------------------------------------------------------
for (x, y, n) in [(5, 7, "greymoss_a"), (14, 13, "greymoss_b"), (8, 13, "greymoss_a"),
                  (16, 7, "greymoss_b")]:
    if deco[y * W + x] == 0 and not wall[y * W + x] and not void[y * W + x] \
            and not ice[y * W + x]:
        deco[y * W + x] = gid(n)
for (x, y) in [(7, 3), (3, 6), (15, 14), (10, 14), (17, 5), (4, 12)]:
    if deco[y * W + x] == 0 and not wall[y * W + x] and not void[y * W + x] \
            and not ice[y * W + x]:
        deco[y * W + x] = gid("g_pebble")
for (x, y) in [(6, 14), (16, 4)]:
    if deco[y * W + x] == 0 and not wall[y * W + x] and not void[y * W + x] \
            and not ice[y * W + x]:
        deco[y * W + x] = gid("boulder")

m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + \
    terrain_layers + [
    {"name": "deco", "role": "deco", "depth": 5, "data": deco},
    {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
]

if __name__ == "__main__":
    ok = mk.finalize(m, scale=3)
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
