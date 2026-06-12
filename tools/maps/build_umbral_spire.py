#!/usr/bin/env python3
"""
Umbral Spire — the ascent of the Ninth Lantern (walkthrough
05-central-endgame "Umbral Spire" + "Climax & Resolution"; atlas card 13;
level-design §2a SPIRE tier: 4+ floors, each floor ONE BEAT of the climb).

Four floors, all kind `cave`, all on the penumbra register (basalt +
basaltwall + void; the C1 kit + the bespoke `spire` kit from
draw_spire_objects.py). NO WILD ENCOUNTERS ANYWHERE (atlas card 13:
"scripted encounters only" — the Hollowing acolyte keepers ARE the
encounters). ZERO humour; the acolyte battles are small griefs, the kin
asleep in the alcoves are never battles. The darkest place in the game,
under the greatest light: the Skyweave Crown completes overhead, read
through the open-shaft crownshaft light and the look-up bands.

    umbral_spire         (this trunk node)  — THE GATEHOUSE: the dead
                         Lumenary's gate floor. Beat: crossing the threshold.
    umbral_spire_f2      — THE NULL-WORKS: rooms-joined-by-chokes maze
                         (the cinderhead pattern), the drained kin asleep
                         in the alcoves. Beat: seeing what the mercy costs.
    umbral_spire_f3      — THE HIGH GALLERY: the hardest keeper pair, the
                         wind above the world, the rest-ledge breather.
                         Beat: pressure, then one quiet breath.
    umbral_spire_summit  — THE GREAT NULL: Còr, the Keystar relight, the
                         dawn. Beat: the answer.

LEVEL CURVE (data-locked to 05 §3): acolyte a lv52-53 (gatehouse) ->
b lv53 / c lv54 (null-works) -> d/e lv54-55 the pair (high gallery) ->
Còr ace ~56, Keylumen ~55 (summit). Drained Dark kin throughout.

MUSIC (deviation from the orchestrator's "umbral-spire-a all floors",
checked as instructed): three Spire cues exist. umbral-spire-b "The Black
Ascent" is the deliberately UNRESOLVED dread/climb loop (music-direction
§18 Option B — "the pure dread/ascent loop for the climb itself");
umbral-spire-a "Crown of Null" is the STRUCTURED CLIMAX piece (intro ->
loop -> minor-major resolve — exactly 05 §6's "structured boss track").
So the ascent floors run -b and the summit runs -a, and the withheld
resolution lands where the walkthrough wants it. umbral-spire-c "First
True Dawn" is the relight-resolution cue — C3's to stage inside
script.keystar_relight / script.dawn_breaks (the `music` op), not a map
track.

LADDERS: the cave_ladder convention throughout (mutual step_on pairs
landing ON each other; `cave_ladder_up/_down` tiles telegraph the warp) —
chosen over beacon-style interior stairs because the Spire is a mapkit
cave lineage (basalt terrain, carved rooms), not a roomkit interior.
    f1 (6,6)  <-> f2 (25,21)      f2 (26,6) <-> f3 (21,17)
    f3 (8,5)  <-> summit (5,19)

THE SHAFT (the §2b return compressor + the central-region loop): the
spire's open core, seeded on F1 (the void pool + the dark hoist lip at
(20,9), blocked_ref'd) and OPENED from F3's rest-ledge — the breather
band `script.spire_wind` sets `flag:spire_shaft` (the sealed-door-
opened-from-inside pattern, flag:shortcut_mine's class), after which the
F3 lip (3,12) and the F1 lip (20,9) are a mutual Starlight descent/ascent
pair gated on that flag. It compresses the re-climb (there is no rest
past the Crossroads — a sanctioned quick exit keeps "go back for
Starwell/Crystoll" honest) and it closes the central region's topology
loop (spire -> f2 -> f3 -> spire), clearing audit_region's corridor WARN.
The flag opens AND closes in this file (spine §0 r3); it gates only the
optional shortcut, never the main path (05's §0 trap 1 respected: the
main path needs nothing not already held).

HANDSHAKE (C1, honoured verbatim): penumbra_ring's to_spire/to_spire_e
door warps land HERE at (13,30)/(14,30) facing up, ON our return pair
to_penumbra/to_penumbra_e, which lands back at penumbra (13,6)/(14,6)
(its doorstep row), facing down.

HANDSHAKE (P1, the post-game contract — documented, not authored): the
summit's to_dawn/to_dawn_e step_on warps at (16,20)/(17,20) — the foot
of the dawn road descending the summit's east shoulder, BEHIND the dais
chain so reaching it threads every climax band —
(`requires_flag: flag:dawn`, blocked_ref npc.dawn_road_waits) land at
dawnstead (15,28)/(16,28) facing up — PLACEHOLDER until the post-game
writer authors dawnstead (the engine no-ops; the coldfog->nightreach
contract style). P1's map must keep those landings WALKABLE and put its
return pair to umbral_spire_summit ON (or within 1 of) them, landing
back at our (16,20)/(17,20) facing down. graph.ts's to_dawn edge now
rides umbral_spire_summit (the warp lives at the peak, where the dawn
breaks — 05 §1 beat 7).

THE SUMMIT CHAIN (the once+ordering encoding, the Nightreach lamp-chain
precedent: once + requires_flag(prev) + sets_flags(own) +
hidden_when_flag(own); a lost battle aborts the cutscene so sets_flags/
once are NOT banked — retry-safe, verified in WorldScene.handleTrigger):
  1. script.great_null     step_on band, the entry corridor's full cut
                           (11,17)+(11,18)
                           — the B5 reveal (seen, not re-explained: the
                           player has held flag:great_null_known since
                           Nightreach). Sets flag:seen_great_null
                           (presentational only).
  2. script.warden_cor_final  step_on band, the dais nook's OUTER row
                           (10-12,10) — Còr's case, the battle as form
                           (TRAINERS['warden_cor'], ai smart, ace ~56,
                           Dark/Lunar pressure + doze; reward_flags
                           bookkeeping only). Completion sets
                           flag:cor_answered.
  3. script.keystar_relight  INTERACT at the dais front (10-12,7),
                           requires flag:cor_answered — the Keylumen
                           set-piece (the legendaryBattle/set-piece op,
                           ~lv55, NEVER a wild roll), the apex gleam
                           cadence, minor->major. Sets flag:keystar_relit.
  4. script.dawn_breaks    step_on band, the dais nook's INNER row
                           (10-12,9), requires flag:keystar_relit —
                           fires as you turn and walk back into the
                           world. Sets flag:dawn. (Silent on the way in:
                           a step_on band with unmet requires and no
                           blocked_ref does nothing.)
Both progression flags use the exact spine §2 strings and no other map
sets them. The two bands + the Còr band sit on the nook's only cut
(walls flank cols 10-12 at rows 6-10) — audit_flow proves all of them
un-walk-aroundable.

C3 WIRING CHECKLIST (every ref this cluster owes, with its hook):
  trainers (TRAINERS[...], payout = keeper class 20 x ace, 10-economy §4;
  mirror into BUILT_PAYOUTS; drained Dark teams, "gentle, not cruel"):
    hollowing_acolyte_a   gatehouse, lv52-53 (suggest payout 1060)
    hollowing_acolyte_b   null-works, lv53   (suggest payout 1060)
    hollowing_acolyte_c   null-works, lv54   (suggest payout 1080)
    hollowing_acolyte_d   high gallery, lv54-55 (suggest payout 1100)
    hollowing_acolyte_e   high gallery, lv54-55 (suggest payout 1100)
      (these five realise the hooks' `trainer.hollowing_acolytes_spire`)
    warden_cor            summit, ace ~56, ai 'smart', payout 6720
                          (realises `trainer.warden_cor_final`)
  scripts (scripts.ts; trigger kind 'cutscene'/'script', ref 'script.*' —
  the engine convention for the hooks' `cutscene.*` refs):
    script.hollowing_acolyte_a..e  (say -> battle -> say -> setFlag; each
                          one a person — grief dressed as mercy)
    script.great_null     (realises `cutscene.great_null`: letterbox +
                          silence; the device SEEN at last; no progression
                          flag — sets flag:seen_great_null)
    script.warden_cor_final (THE scene: his case at full strength, the
                          battle as form, the out-remembering; portraits
                          grave/gentle/sorrowful/at_peace)
    script.keystar_relight (realises `cutscene.keystar_relight`: the
                          Keylumen set-piece catch + the apex gleam
                          ceremony; minor->major; suggest the
                          umbral-spire-c cue here)
    script.dawn_breaks    (realises `cutscene.dawn_breaks`: silence ->
                          slow warm tint -> the dawnbreak panels)
    script.spire_crown_1  (gatehouse look-up: the Crown through the open
                          shaft — atmosphere only)
    script.spire_crown_2  (null-works look-up #2)
    script.spire_wind     (the high-gallery breather: the wind above the
                          world + kindling the shaft hoist; sets
                          flag:spire_shaft — see THE SHAFT above)
    script.pickup_spire_gatehouse  (cache: suggest a Star-tonic class
                          consumable — there is no shop on the mountain)
    script.pickup_spire_landing    (THE one [MISSABLE] hidden side-landing
                          item, 05 §4 — suggest a valuable + the best
                          pre-summit heal)
    script.pickup_spire_gallery    (cache: loose wicks or a revive-class
                          medicine before the keeper pair)
  dialogue (dialogue.ts):
    npc.wren_spire_f1/_f2/_f3/_summit  (realise `npc.wren_spire`: the
                          A5->A6 side-by-side, one line per floor; AT MOST
                          one wry-warm beat across the four — suggest it
                          lives in _f1; _f3 and _summit stay sincere)
    npc.hollowing_acolyte_a..e_after   (beaten swaps — each still believes,
                          softer now)
    npc.spire_sleeper     (the alcove read: asleep, not dead — grief)
    npc.spire_sleeper_awake (the postgame flag:dawn flip, hushfrost
                          numbed_kin pattern)
    npc.cor_summit        (belt-and-braces interact line pre-battle; the
                          band normally fires first)
    npc.cor_after         (Còr undone, not destroyed — remembering)
    npc.spire_shaft_dark  (the F1 lip before F3 opens it: "the hoist-lamp
                          is dark; the starlight will not bear you yet")
    npc.dawn_road_waits   (the to_dawn blocked line pre-dawn)

Suggested copy (C3; sincere, elegiac; the ONE wry-warm beat marked):
  npc.wren_spire_f1     "So this is where the dusk lives. ...It's tidier
                        than I expected. [wry-warm] Stay close — I didn't
                        climb all this way to lose you in the dark."
  npc.wren_spire_f2     "They tuck them in. Look — they SWEEP in here.
                        Sad, isn't it. ...Doesn't make them right. Keep
                        climbing."
  npc.wren_spire_f3     "Listen. Wind, this deep in the mountain. The sky
                        is just up there, and it's FULL of your lamps."
  npc.wren_spire_summit "I'm right here. Whatever he says — and he'll say
                        it kindly — you remember louder. Go on."
  script.spire_wind     narrate: the shaft opens to the night; every
                        constellation you have relit hangs in the column
                        of air. You kindle the old hoist-lamp; far below,
                        a thread of starlight steadies. (sets
                        flag:spire_shaft)
  script.great_null     narrate: a bell of held dark, vast and patient,
                        aimed at the one star that lets the others
                        rekindle. The gauge at its foot rests at zero.
                        Someone has swept the floor.

audit_flow waivers (documented per the skill contract):
  * free-pass / encounter checks — canonically encounter-free (atlas card
    13 "scripted encounters only"); the §11 r7 load is the keeper sight
    lines, which DO seal every floor crossing.
  * loop (f1/f3/summit) — each floor is ONE BEAT of a climb (§2a Spire
    tier); the loop lives at cluster scale (the F3->F1 shaft compressor)
    and at region scale (audit_region's central cycle). f2 carries a real
    in-floor loop (R1->R2->R3->R4->R1, the void-braid corridor).

Run:  ./venv/bin/python tools/maps/build_umbral_spire.py
"""
from __future__ import annotations
import random
import shutil
import subprocess
import sys
from pathlib import Path

import mapkit as mk
import patterns as pt
from mapkit import gid

REPO = Path(__file__).resolve().parents[2]
OUT = Path("/tmp/c2")

MUSIC_ASCENT = "assets/audio/music/umbral-spire-b.mp3"   # The Black Ascent
MUSIC_SUMMIT = "assets/audio/music/umbral-spire-a.mp3"   # Crown of Null
BACKDROPS = [
    "assets/backgrounds/battle/umbral-spire-a.webp",
    "assets/backgrounds/battle/umbral-spire-b.webp",
]

owed: list[str] = []


def base_floor(W: int, H: int, rng: random.Random) -> list[int]:
    bs = [gid("basalt0"), gid("basalt1"), gid("basalt2")]
    return [rng.choice(bs) if rng.random() < 0.5 else bs[0] for _ in range(W * H)]


def mapdef(mid: str, name: str, W: int, H: int, *, music: str) -> dict:
    return {
        "id": mid, "display_name": name, "width": W, "height": H,
        "tile_width": 16, "tile_height": 16, "kind": "cave",
        "tilesets": [mk.shared_tileset_ref()],
        "objects": [], "warps": [], "triggers": [], "encounters": [],
        "npcs": [], "gates": [],
        "music": music,
        "battle_backdrops": list(BACKDROPS),
    }


def layers(m: dict, base, wall, void, deco, W: int, H: int) -> None:
    terrain = []
    if any(void):
        terrain.append({"name": "t_void", "role": "terrain", "terrain": "void",
                        "set": "vesper_overworld_set", "depth": 0, "data": void})
    terrain.append({"name": "t_basaltwall", "role": "terrain",
                    "terrain": "basaltwall", "set": "vesper_overworld_set",
                    "depth": 0, "data": wall})
    m["layers"] = [{"name": "base", "role": "base", "depth": 0, "data": base}] + \
        terrain + [
        {"name": "deco", "role": "deco", "depth": 5, "data": deco},
        {"name": "above", "role": "above", "depth": 20, "data": mk.make_grid(W, H)},
    ]


def crownshaft(m: dict, n: str, at: tuple[int, int]) -> None:
    """The open-shaft skylight decal — non-solid, walk-on (player over it)."""
    m["objects"].append(
        {"id": f"crownshaft_{n}", "sprite": "spire_crownshaft",
         "at": {"tx": at[0], "ty": at[1]}, "w": 3, "h": 3,
         "solid": False, "walk_under": True})


def glint(m: dict, at: tuple[int, int], variant: str) -> None:
    m["objects"].append(
        {"id": f"starglint_{at[0]}_{at[1]}",
         "sprite": f"penumbra_starglint_bright_{variant}",
         "at": {"tx": at[0], "ty": at[1]}, "w": 1, "h": 1,
         "solid": False, "walk_under": True})


def sleeper(m: dict, n: str, sprite_stem: str, at: tuple[int, int]) -> None:
    """A drained kin asleep in its alcove + the postgame flag:dawn flip
    (the hushfrost numbed_kin pattern: same footprint, same solidity;
    flag-gated state listed FIRST so flag-blind QA renders show the
    pre-dawn state on top). Interact reads on the front (bottom) row."""
    m["objects"] += [
        {"id": f"sleeper_{n}_awake", "sprite": f"spire_{sprite_stem}_awake",
         "at": {"tx": at[0], "ty": at[1]}, "w": 2, "h": 2,
         "requires_flag": "flag:dawn"},
        {"id": f"sleeper_{n}", "sprite": f"spire_{sprite_stem}",
         "at": {"tx": at[0], "ty": at[1]}, "w": 2, "h": 2,
         "hidden_when_flag": "flag:dawn"},
    ]
    for i, tx in enumerate((at[0], at[0] + 1)):
        m["triggers"] += [
            {"id": f"sleeper_{n}_read_{i}", "kind": "dialogue",
             "at": {"tx": tx, "ty": at[1] + 1}, "activation": "interact",
             "ref": "npc.spire_sleeper", "hidden_when_flag": "flag:dawn"},
            {"id": f"sleeper_{n}_awake_read_{i}", "kind": "dialogue",
             "at": {"tx": tx, "ty": at[1] + 1}, "activation": "interact",
             "ref": "npc.spire_sleeper_awake", "requires_flag": "flag:dawn"},
        ]


def moss_and_stone(m: dict, deco, wall, void, W: int, H: int, spots, pebbles) -> None:
    for (x, y, n) in spots:
        if deco[y * W + x] == 0 and not wall[y * W + x] and not void[y * W + x]:
            deco[y * W + x] = gid(n)
    for (x, y) in pebbles:
        if deco[y * W + x] == 0 and not wall[y * W + x] and not void[y * W + x]:
            deco[y * W + x] = gid("g_pebble")


# ======================================================================================
# FLOOR 1 — umbral_spire: THE GATEHOUSE (the dead Lumenary's gate floor)
# ======================================================================================
def build_f1() -> dict:
    W, H = 28, 32
    rng = random.Random(513)
    wall = mk.make_grid(W, H)
    mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

    floor = mk.make_grid(W, H)
    mk.rect(floor, W, H, 12, 26, 15, 30)      # vestibule (the gate lands here)
    mk.rect(floor, W, H, 13, 22, 14, 25)      # choke A — the first look-up
    mk.rect(floor, W, H, 5, 15, 22, 21)       # THE GATE HALL
    mk.rect(floor, W, H, 3, 17, 4, 19)        # west alcove (cache pocket)
    mk.vline(floor, W, H, 9, 12, 14)          # choke B — acolyte a's watch
    mk.rect(floor, W, H, 4, 5, 23, 11)        # THE NULL-WORKS ANTECHAMBER
    for i in range(W * H):
        if floor[i]:
            wall[i] = 0

    # the spire's open core: the void shaft pool (NE of the antechamber);
    # the dark hoist lip below it is the F3 shortcut's other half
    void = mk.make_grid(W, H)
    mk.rect(void, W, H, 19, 6, 21, 8)
    for i in range(W * H):
        if void[i] and wall[i]:
            void[i] = 0

    m = mapdef("umbral_spire", "Umbral Spire", W, H, music=MUSIC_ASCENT)

    # ---- warps -----------------------------------------------------------------
    m["warps"] += [
        # SOUTH <-> penumbra_ring (graph `to_spire` return half; the C1
        # handshake: their landing IS our return pair)
        {"id": "to_penumbra", "at": {"tx": 13, "ty": 30}, "trigger": "step_on",
         "to_map": "penumbra_ring", "to": {"tx": 13, "ty": 6}, "facing": "down",
         "transition": "door"},
        {"id": "to_penumbra_e", "at": {"tx": 14, "ty": 30}, "trigger": "step_on",
         "to_map": "penumbra_ring", "to": {"tx": 14, "ty": 6}, "facing": "down",
         "transition": "door"},
        # the shaft ascent (sealed until F3 kindles the hoist — see docstring)
        {"id": "shaft_up", "at": {"tx": 20, "ty": 9}, "trigger": "step_on",
         "to_map": "umbral_spire_f3", "to": {"tx": 3, "ty": 12}, "facing": "down",
         "requires_flag": "flag:spire_shaft",
         "blocked_ref": "npc.spire_shaft_dark", "transition": "fade"},
    ]
    deco = mk.make_grid(W, H)
    pt.cave_ladder(m, deco, W, kind="up", at=(6, 6),
                   to_map="umbral_spire_f2", to=(25, 21), wid="ladder_up")

    # ---- the first look-up (the Crown through the open shaft; choke A) ----------
    for i, tx in enumerate((13, 14)):
        m["triggers"].append(
            {"id": f"spire_crown_1_{i}", "kind": "script",
             "at": {"tx": tx, "ty": 23}, "activation": "step_on",
             "ref": "script.spire_crown_1", "once": True,
             "sets_flags": ["flag:spire_crown_1_seen"],
             "hidden_when_flag": "flag:spire_crown_1_seen"})
    owed.append("script.spire_crown_1 (look-up #1 — atmosphere only)")

    # ---- acolyte a holds choke B (posted two rows past the mouth, facing
    # down the 1-wide corridor — the beacon convention: the sight line seals
    # the crossing, the body never seals the lane) -------------------------------
    owed.extend(pt.trainer_beat(m, tid="hollowing_acolyte_a", at=(9, 10),
                                facing="down", sight=5, sprite="npc_woman"))

    # ---- Wren #1, just inside the gate (A5->A6 side-by-side) --------------------
    m["npcs"].append(
        {"id": "wren_f1", "at": {"tx": 17, "ty": 20}, "facing": "left",
         "sprite": "wren", "movement": "static",
         "dialogue_ref": "npc.wren_spire_f1"})
    owed.append("npc.wren_spire_f1 (the one [wry-warm] beat lives here)")

    # ---- the gatehouse cache (west alcove; no shop on the mountain) -------------
    owed.extend(pt.cache(m, cid="spire_gatehouse", at=(3, 18)))

    # ---- dressing: the dead Lumenary, tended -----------------------------------
    m["objects"] += [
        {"id": "rack_w", "sprite": "coldfog_null_rack",
         "at": {"tx": 5, "ty": 15}, "w": 4, "h": 2, "overhang": 1},
        {"id": "rack_e", "sprite": "coldfog_null_rack",
         "at": {"tx": 17, "ty": 15}, "w": 4, "h": 2, "overhang": 1},
        {"id": "shrine_works", "sprite": "glowmoss_deep_null_lantern_shrine",
         "at": {"tx": 11, "ty": 3}, "w": 2, "h": 3, "overhang": 2},
        {"id": "pool_hall", "sprite": "spire_null_pool",
         "at": {"tx": 19, "ty": 18}, "w": 2, "h": 2},
        {"id": "pool_works", "sprite": "spire_null_pool",
         "at": {"tx": 6, "ty": 8}, "w": 2, "h": 2},
    ]
    crownshaft(m, "hall", (12, 17))
    crownshaft(m, "works", (15, 6))
    for (x, y, v) in [(19, 7, "a"), (21, 6, "b"), (20, 8, "a"), (13, 18, "b")]:
        glint(m, (x, y), v)
    deco[21 * W + 12] = gid("null_lantern")   # Còr's lanterns flank the gate hall
    deco[21 * W + 15] = gid("null_lantern")
    moss_and_stone(m, deco, wall, void, W, H,
                   [(6, 17, "greymoss_a"), (16, 19, "greymoss_b"),
                    (21, 16, "greymoss_a"), (5, 10, "greymoss_b"),
                    (17, 10, "greymoss_a"), (13, 27, "greymoss_b")],
                   [(8, 19, ), (11, 16), (18, 21), (10, 7), (22, 10), (12, 29)])

    base = base_floor(W, H, rng)
    layers(m, base, wall, void, deco, W, H)
    return m


# ======================================================================================
# FLOOR 2 — umbral_spire_f2: THE NULL-WORKS (the maze; the sleeping kin)
# ======================================================================================
def build_f2() -> dict:
    W, H = 30, 26
    rng = random.Random(514)
    wall = mk.make_grid(W, H)
    mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

    floor = mk.make_grid(W, H)
    mk.rect(floor, W, H, 22, 18, 27, 23)      # R1 — arrival (ladder from F1)
    mk.hline(floor, W, H, 20, 18, 21)         # C1
    mk.rect(floor, W, H, 10, 16, 17, 23)      # R2 — south gallery
    mk.hline(floor, W, H, 22, 6, 9)           # C_s — the hidden side-landing spur
    mk.rect(floor, W, H, 3, 20, 5, 23)        # the side landing ([MISSABLE] cache)
    mk.vline(floor, W, H, 12, 12, 15)         # C2 — acolyte b's watch
    mk.rect(floor, W, H, 6, 5, 18, 11)        # R3 — THE NULL-WORKS HALL
    mk.rect(floor, W, H, 7, 4, 8, 4)          # alcove niches (the sleeping kin)
    mk.rect(floor, W, H, 12, 4, 13, 4)
    mk.rect(floor, W, H, 16, 4, 17, 4)
    mk.hline(floor, W, H, 8, 19, 21)          # C3 — look-up #2's choke
    mk.rect(floor, W, H, 22, 5, 27, 11)       # R4 — upper landing (ladder to F3)
    mk.vline(floor, W, H, 24, 12, 17)         # C4 — the void-braid loop back to R1
    for i in range(W * H):
        if floor[i]:
            wall[i] = 0

    # the braid: C4's middle runs over the open core — crossed on starlight
    void = mk.make_grid(W, H)
    for y in range(13, 17):
        void[y * W + 24] = 1

    m = mapdef("umbral_spire_f2", "Umbral Spire — Null-Works", W, H,
               music=MUSIC_ASCENT)

    deco = mk.make_grid(W, H)
    pt.cave_ladder(m, deco, W, kind="down", at=(25, 21),
                   to_map="umbral_spire", to=(6, 6), wid="ladder_down")
    pt.cave_ladder(m, deco, W, kind="up", at=(26, 6),
                   to_map="umbral_spire_f3", to=(21, 17), wid="ladder_up")

    # ---- look-up #2: the open core. Banded on BOTH ways up to R4 — the C3
    # choke AND the void-braid's two basalt mouths (the braid IS the open
    # core, so the look-up reads true from either crossing; one shared flag,
    # whichever fires first hides the rest) ------------------------------------------
    for i, at in enumerate(((20, 8), (24, 12), (24, 17))):
        m["triggers"].append(
            {"id": f"spire_crown_2_{i}", "kind": "script",
             "at": {"tx": at[0], "ty": at[1]}, "activation": "step_on",
             "ref": "script.spire_crown_2", "once": True,
             "sets_flags": ["flag:spire_crown_2_seen"],
             "hidden_when_flag": "flag:spire_crown_2_seen"})
    owed.append("script.spire_crown_2 (look-up #2 — atmosphere only)")

    # ---- the keepers of the works ------------------------------------------------
    owed.extend(pt.trainer_beat(m, tid="hollowing_acolyte_b", at=(12, 9),
                                facing="down", sight=5, sprite="npc_man"))
    owed.extend(pt.trainer_beat(m, tid="hollowing_acolyte_c", at=(24, 8),
                                facing="left", sight=4, sprite="npc_old_woman"))

    # ---- the drained kin asleep in the alcoves (grief, never battles) ------------
    sleeper(m, "a", "sleeper_nullmoth", (7, 4))
    sleeper(m, "b", "sleeper_cindersob", (12, 4))
    sleeper(m, "c", "sleeper_voidmantle", (16, 4))
    owed.append("npc.spire_sleeper (+ npc.spire_sleeper_awake — the postgame "
                "flag:dawn flip, hushfrost pattern)")

    # ---- Wren #2 ------------------------------------------------------------------
    m["npcs"].append(
        {"id": "wren_f2", "at": {"tx": 15, "ty": 17}, "facing": "up",
         "sprite": "wren", "movement": "static",
         "dialogue_ref": "npc.wren_spire_f2"})
    owed.append("npc.wren_spire_f2")

    # ---- the ONE [MISSABLE] hidden side-landing item (05 §4) ----------------------
    owed.extend(pt.cache(m, cid="spire_landing", at=(4, 21)))

    # ---- dressing ------------------------------------------------------------------
    m["objects"] += [
        {"id": "rack_s", "sprite": "coldfog_null_rack",
         "at": {"tx": 13, "ty": 18}, "w": 4, "h": 2, "overhang": 1},
        {"id": "rack_n", "sprite": "coldfog_null_rack",
         "at": {"tx": 22, "ty": 5}, "w": 4, "h": 2, "overhang": 1},
        {"id": "pool_works", "sprite": "spire_null_pool",
         "at": {"tx": 8, "ty": 8}, "w": 2, "h": 2},
    ]
    crownshaft(m, "hall", (15, 8))
    crownshaft(m, "arrival", (24, 19))
    for (x, y, v) in [(24, 13, "a"), (24, 15, "b"), (24, 16, "a"),
                      (11, 19, "b"), (26, 20, "a")]:
        glint(m, (x, y), v)
    moss_and_stone(m, deco, wall, void, W, H,
                   [(7, 10, "greymoss_a"), (16, 10, "greymoss_b"),
                    (11, 22, "greymoss_a"), (23, 10, "greymoss_b"),
                    (4, 22, "greymoss_a"), (17, 21, "greymoss_b")],
                   [(10, 10), (14, 11), (23, 22), (16, 22), (7, 22), (26, 9)])

    base = base_floor(W, H, rng)
    layers(m, base, wall, void, deco, W, H)
    return m


# ======================================================================================
# FLOOR 3 — umbral_spire_f3: THE HIGH GALLERY (the pair; the breather)
# ======================================================================================
def build_f3() -> dict:
    W, H = 26, 22
    rng = random.Random(515)
    wall = mk.make_grid(W, H)
    mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

    floor = mk.make_grid(W, H)
    mk.rect(floor, W, H, 18, 14, 23, 19)      # R1 — arrival (ladder from F2)
    mk.hline(floor, W, H, 16, 12, 17)         # C1
    mk.rect(floor, W, H, 10, 9, 11, 16)       # THE CLIMB — the 2-wide gallery
    mk.rect(floor, W, H, 5, 4, 16, 8)         # R3 — the antechamber (ladder up)
    mk.hline(floor, W, H, 12, 5, 9)           # C2 — the breather's way in
    mk.rect(floor, W, H, 2, 9, 4, 14)         # R4 — THE REST-LEDGE
    for i in range(W * H):
        if floor[i]:
            wall[i] = 0

    # the open shaft at the ledge's shoulder (the spire's core, again)
    void = mk.make_grid(W, H)
    mk.rect(void, W, H, 2, 9, 3, 11)

    m = mapdef("umbral_spire_f3", "Umbral Spire — High Gallery", W, H,
               music=MUSIC_ASCENT)

    deco = mk.make_grid(W, H)
    pt.cave_ladder(m, deco, W, kind="down", at=(21, 17),
                   to_map="umbral_spire_f2", to=(26, 6), wid="ladder_down")
    pt.cave_ladder(m, deco, W, kind="up", at=(8, 5),
                   to_map="umbral_spire_summit", to=(5, 19), wid="ladder_up")
    # the shaft descent — opened by the breather band below (see docstring)
    m["warps"].append(
        {"id": "shaft_down", "at": {"tx": 3, "ty": 12}, "trigger": "step_on",
         "to_map": "umbral_spire", "to": {"tx": 20, "ty": 9}, "facing": "down",
         "requires_flag": "flag:spire_shaft", "transition": "fade"})

    # ---- the breather band (pressure-then-relief; NO heal — the walkthrough's
    # "no rest past the Crossroads" honoured: the pocket is emotional, plus the
    # shaft compressor it kindles). Covers the 1-wide C2 cut at the ledge's
    # mouth, within guard-reach of the shaft portal so the audit proves the
    # band seals it. ------------------------------------------------------------------
    for i, tx in enumerate((5, 6, 7)):
        m["triggers"].append(
            {"id": f"spire_wind_{i}", "kind": "script",
             "at": {"tx": tx, "ty": 12}, "activation": "step_on",
             "ref": "script.spire_wind", "once": True,
             "sets_flags": ["flag:spire_shaft"],
             "hidden_when_flag": "flag:spire_shaft"})
    owed.append("script.spire_wind (the wind above the world; sets flag:spire_shaft)")

    # ---- the Ninth Lantern's dedication plaque (the antechamber's east end
    # pays — §3a rule 4; suggest: "THE NINTH LANTERN — first lit when the
    # eight were named; tended so the one star that wakes the others is
    # never alone." C3 keeps it elegiac.) ----------------------------------------------
    owed.extend(pt.sign(m, deco, W, sid="spire_lantern", at=(15, 5)))

    # ---- the hardest keeper pair, posted over the 2-wide climb (each seals
    # one column; together the crossing is unavoidable) ------------------------------
    owed.extend(pt.trainer_beat(m, tid="hollowing_acolyte_d", at=(10, 6),
                                facing="down", sight=5, sprite="npc_old_man"))
    owed.extend(pt.trainer_beat(m, tid="hollowing_acolyte_e", at=(11, 6),
                                facing="down", sight=5, sprite="npc_woman"))

    # ---- Wren #3, at the ledge ------------------------------------------------------
    m["npcs"].append(
        {"id": "wren_f3", "at": {"tx": 4, "ty": 13}, "facing": "left",
         "sprite": "wren", "movement": "static",
         "dialogue_ref": "npc.wren_spire_f3"})
    owed.append("npc.wren_spire_f3")

    # ---- the gallery cache (before the pair; the last find before the summit) ------
    owed.extend(pt.cache(m, cid="spire_gallery", at=(5, 4)))

    # ---- dressing: the wind above the world — starglint density rising --------------
    m["objects"].append(
        {"id": "shrine_gallery", "sprite": "glowmoss_deep_null_lantern_shrine",
         "at": {"tx": 6, "ty": 2}, "w": 2, "h": 3, "overhang": 2})
    crownshaft(m, "ante", (12, 4))
    crownshaft(m, "climb", (9, 10))
    crownshaft(m, "arrival", (19, 15))
    for (x, y, v) in [(2, 10, "a"), (3, 9, "b"), (2, 11, "b"), (6, 12, "a"),
                      (10, 13, "b"), (15, 16, "a"), (20, 18, "b"), (14, 6, "a"),
                      (7, 7, "b")]:
        glint(m, (x, y), v)
    moss_and_stone(m, deco, wall, void, W, H,
                   [(6, 7, "greymoss_a"), (15, 7, "greymoss_b"),
                    (19, 18, "greymoss_a"), (5, 13, "greymoss_b")],
                   [(13, 16), (22, 15), (10, 15), (16, 5), (4, 10)])
    for (x, y) in [(18, 14), (23, 19)]:
        if deco[y * W + x] == 0:
            deco[y * W + x] = gid("boulder")

    base = base_floor(W, H, rng)
    layers(m, base, wall, void, deco, W, H)
    return m


# ======================================================================================
# SUMMIT — umbral_spire_summit: THE GREAT NULL (Còr; the Keystar; the dawn)
# ======================================================================================
def build_summit() -> dict:
    W, H = 24, 24
    rng = random.Random(516)
    wall = mk.make_grid(W, H)
    mk.rect(wall, W, H, 0, 0, W - 1, H - 1)

    floor = mk.make_grid(W, H)
    mk.rect(floor, W, H, 10, 6, 12, 10)       # the dais nook (the chain's choke)
    mk.hline(floor, W, H, 9, 13, 16)          # the dawn shoulder (off the dais row)
    mk.vline(floor, W, H, 16, 10, 18)         # the dawn road, descending east
    mk.rect(floor, W, H, 16, 19, 17, 20)      # ...its gate chamber (P1's door)
    mk.rect(floor, W, H, 4, 11, 14, 16)       # THE SUMMIT PLATFORM
    mk.rect(floor, W, H, 2, 18, 7, 22)        # arrival chamber (ladder from F3)
    mk.hline(floor, W, H, 18, 8, 10)          # the approach corridor
    mk.vline(floor, W, H, 11, 17, 18)         # ...its turn up onto the platform
    for i in range(W * H):
        if floor[i]:
            wall[i] = 0

    void = mk.make_grid(W, H)                  # no open core at the peak — sky above

    m = mapdef("umbral_spire_summit", "Umbral Spire — Summit", W, H,
               music=MUSIC_SUMMIT)

    deco = mk.make_grid(W, H)
    pt.cave_ladder(m, deco, W, kind="down", at=(5, 19),
                   to_map="umbral_spire_f3", to=(8, 5), wid="ladder_down")
    # the dawn road — P1's contract (see docstring); gated on the climax.
    # It descends BEHIND the dais chain (the shoulder branches off the nook's
    # inner row), so reaching it threads every summit band — the audit proves
    # the whole chain un-walk-aroundable.
    m["warps"] += [
        {"id": "to_dawn", "at": {"tx": 16, "ty": 20}, "trigger": "step_on",
         "to_map": "dawnstead", "to": {"tx": 15, "ty": 28}, "facing": "up",
         "requires_flag": "flag:dawn", "blocked_ref": "npc.dawn_road_waits",
         "transition": "fade"},
        {"id": "to_dawn_e", "at": {"tx": 17, "ty": 20}, "trigger": "step_on",
         "to_map": "dawnstead", "to": {"tx": 16, "ty": 28}, "facing": "up",
         "requires_flag": "flag:dawn", "blocked_ref": "npc.dawn_road_waits",
         "transition": "fade"},
    ]
    owed.append("npc.dawn_road_waits (the to_dawn blocked line pre-dawn)")

    # ---- 1. the reveal: the Great Null SEEN (B5; the entry corridor's cut) ---------
    for i, at in enumerate(((11, 17), (11, 18))):
        m["triggers"].append(
            {"id": f"great_null_reveal_{i}", "kind": "cutscene",
             "at": {"tx": at[0], "ty": at[1]}, "activation": "step_on",
             "ref": "script.great_null", "once": True,
             "sets_flags": ["flag:seen_great_null"],
             "hidden_when_flag": "flag:seen_great_null"})
    owed.append("script.great_null (the B5 reveal — letterbox + silence)")

    # ---- 2. Còr (the dais nook's OUTER row — every walkable tile of the cut) -------
    for i, tx in enumerate((10, 11, 12)):
        m["triggers"].append(
            {"id": f"cor_final_{i}", "kind": "cutscene",
             "at": {"tx": tx, "ty": 10}, "activation": "step_on",
             "ref": "script.warden_cor_final", "once": True,
             "sets_flags": ["flag:cor_answered"],
             "hidden_when_flag": "flag:cor_answered"})
    owed.append("script.warden_cor_final + TRAINERS['warden_cor'] "
                "(ace ~56, ai smart, payout 6720; reward_flags bookkeeping only)")

    # ---- 3. the Keylumen set-piece (INTERACT at the dais front) ---------------------
    for i, tx in enumerate((10, 11, 12)):
        m["triggers"].append(
            {"id": f"keystar_relight_{i}", "kind": "cutscene",
             "at": {"tx": tx, "ty": 7}, "activation": "interact",
             "ref": "script.keystar_relight", "once": True,
             "requires_flag": "flag:cor_answered",
             "sets_flags": ["flag:keystar_relit"],
             "hidden_when_flag": "flag:keystar_relit"})
    owed.append("script.keystar_relight (the Keylumen set-piece catch ~lv55; "
                "sets flag:keystar_relit; suggest the umbral-spire-c cue)")

    # ---- 4. dawn breaks (the nook's INNER row, crossed walking back out;
    # silent inbound — requires unmet + step_on + no blocked_ref) ---------------------
    for i, tx in enumerate((10, 11, 12)):
        m["triggers"].append(
            {"id": f"dawn_breaks_{i}", "kind": "cutscene",
             "at": {"tx": tx, "ty": 9}, "activation": "step_on",
             "ref": "script.dawn_breaks", "once": True,
             "requires_flag": "flag:keystar_relit",
             "sets_flags": ["flag:dawn"],
             "hidden_when_flag": "flag:dawn"})
    owed.append("script.dawn_breaks (sets flag:dawn — silence -> slow warm tint)")

    # ---- Còr, courteous and sad, between you and the device -------------------------
    m["npcs"] += [
        {"id": "warden_cor", "at": {"tx": 11, "ty": 8}, "facing": "down",
         "sprite": "warden_cor", "movement": "static",
         "dialogue_ref": "npc.cor_summit",
         "hidden_when_flag": "flag:cor_answered"},
        # undone, not destroyed — he steps aside and remembers (post-game
        # carries him down to the star-tenders; C3/P-writers may move him)
        {"id": "warden_cor_after", "at": {"tx": 14, "ty": 12}, "facing": "left",
         "sprite": "warden_cor", "movement": "static",
         "dialogue_ref": "npc.cor_after", "requires_flag": "flag:cor_answered"},
    ]
    owed.append("npc.cor_summit + npc.cor_after")

    # ---- Wren, at the summit's edge (the side-by-side beat's last placement) --------
    m["npcs"].append(
        {"id": "wren_summit", "at": {"tx": 4, "ty": 13}, "facing": "up",
         "sprite": "wren", "movement": "static",
         "dialogue_ref": "npc.wren_spire_summit"})
    owed.append("npc.wren_spire_summit")

    # ---- the Great Null + the dais ----------------------------------------------------
    m["objects"] += [
        # the hero: drawn rows 0-5 over the north wall, solid rows 4-5 (its
        # plinth is the wall itself — the hollowfen null_engine staging, scaled)
        {"id": "great_null", "sprite": "spire_great_null",
         "at": {"tx": 8, "ty": 0}, "w": 8, "h": 6, "overhang": 4},
        {"id": "keystar_dais", "sprite": "spire_keystar_dais",
         "at": {"tx": 10, "ty": 6}, "w": 3, "h": 2, "overhang": 1},
    ]
    deco[11 * W + 9] = gid("null_lantern")    # his anti-light ring at the nook mouth
    deco[11 * W + 13] = gid("null_lantern")

    # ---- the peak under the completing Crown ------------------------------------------
    crownshaft(m, "west", (5, 12))
    crownshaft(m, "east", (11, 13))
    crownshaft(m, "south", (8, 14))
    for (x, y, v) in [(7, 11, "a"), (12, 12, "b"), (16, 12, "a"), (5, 16, "b"),
                      (13, 16, "a"), (14, 9, "a"), (16, 16, "b"), (17, 19, "a"),
                      (3, 21, "b"), (6, 21, "a")]:
        glint(m, (x, y), v)
    moss_and_stone(m, deco, wall, void, W, H,
                   [(4, 11, "greymoss_a"), (16, 14, "greymoss_b"),
                    (3, 20, "greymoss_a")],
                   [(6, 15), (3, 18), (8, 12), (12, 16)])

    base = base_floor(W, H, rng)
    layers(m, base, wall, void, deco, W, H)
    return m


# ======================================================================================
if __name__ == "__main__":
    builders = [build_f1, build_f2, build_f3, build_summit]
    ok = True
    OUT.mkdir(exist_ok=True)
    for b in builders:
        m = b()
        good = mk.finalize(m, scale=3)
        ok = ok and good
        png = Path("/tmp") / f"{m['id']}.png"
        if png.exists():
            shutil.copy(png, OUT / png.name)
    # the cross-floor warp pass (every pair now exists on disk; penumbra's
    # to_spire landing is re-proven against the authored gatehouse too)
    aud = subprocess.run(
        [sys.executable, str(REPO / "tools/maps/audit_warps.py"),
         "umbral_spire", "umbral_spire_f2", "umbral_spire_f3",
         "umbral_spire_summit", "penumbra_ring"],
        capture_output=True, text=True)
    print(aud.stdout)
    ok = ok and aud.returncode == 0
    pt.report(owed)
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
