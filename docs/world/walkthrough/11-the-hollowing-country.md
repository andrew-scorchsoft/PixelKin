# PixelKin Walkthrough — 11 · The Hollowing's Country (the late-game north, 2026-10)

> Region-crossing file under the [spine](./README.md); its §0 rules, §2 flags, §4 curve, §5
> optional web and §10 voice are binding. Geometry is binding: [`../geometry.md`](../geometry.md)
> (`world_geometry.py --check` must close). Scored in
> [`../../reviews/expansion-panel.md`](../../reviews/expansion-panel.md) (Plan 4). Canon vocabulary only.

## Why

The owner's read, confirmed by measurement: the early world is rich, but **the top of the map,
the late game, is thin**.
- **Coldfog Marches I/II:** 1–2 people each and no trainers.
- **Drownlight Beacon:** an 18×16 dead end with nobody in it.
- **Helia Vault** and the **Nightreach lane:** empty.
- **Sunvault:** four corridor maps.
- **The endgame road:** the Umbral Approach is one map, the Penumbra Ring has no wild kin, and
  only one Spire floor has encounters.
- **The antagonists are never met as people.** The story-bible's Hollowing are sympathetic
  ("not villains in capes"), yet the game only ever shows their works, never their homes.

This round adds a late-game region at the top of the world, about the size of the south round.

## The clear thread (binding)

Everything here is **optional and late**:
- The north opens at `gleam:solar` (Coldfog's existing gate). The tower's upper floors also need
  `emberward`.
- The Underways need `flag:hub_unlocked` + `starreach`.
- Nothing here connects to the Umbral Spire or grants a Gleam, a Gift or a crown.
- `audit_journey`'s golden thread must stay 40/40, in canon order, with the waves unchanged for
  every existing beat.
- Any new door hung on a quest step uses the ANY_OF "this step or a later milestone" rule.

---

## A · Stillwater — the Hollowing's village

**Lore.** Where the quieted go. North of the drained marsh, the Hollowing keep a village of
shuttered lamps, soft voices and sleeping kin, kept warm by hearths with their faces turned to the
wall. Its people are tired, grieving, kind, and certain the dark is mercy. They aren't evil and
they aren't stupid. Some of them are beginning to doubt.

**Map.** `stillwater`, town, 30×30, world `(48,-491)`, so its south edge meets Coldfog Marches I's
north edge (x 48–68). Interiors (roomkit, a muted shutter-grey kit):
- `stillwater_quiet_hall`: their meeting-house, with the shutter-wall and the names of the lamps
  they've put out.
- `stillwater_shutter`: the inn. It's a rest point and goes in HEAL_ENTRANCE_MAPS.
- `stillwater_lampmaker`: the dark-lamp maker, a former lamplighter.
- Two homes.

**People.** About 20, with Hollowing acolytes as the regional cast. You're tolerated, not attacked:
"you're the one relighting the sky." Three trainers who'd rather talk first.

**Side quests (3+, journal):**
1. **"A Light Left On":** a Hollowing child keeps one forbidden candle in a jar. Help them hide it,
   or help them show it to their mother. Both endings are kind.
2. **"The Way Home":** an acolyte, Tessaly, wants to go home to Pale Vault but can't face the road
   alone. Escort beats run through Coldfog. She reappears in Pale Vault (a placement through the
   owning runner, flag-gated). The reward is her old lamp.
3. **"The Shutter-wall":** read the names of the lamps put out, and find three of the matching
   cold lamps out in the north. A lore chain: why they did it, in their own words. **Never name
   Senna; Còr's past stays dosed.**

**After the dawn:** a few shutters open. A lamp in a window, a child at it. Quiet, not triumphant.

## B · The Drownlight — the first lamp the Hollowing put out

**Lore.** The Drownlight Beacon was the north coast's light. It was the Hollowing's first:
they shuttered it the winter Còr's grief became a philosophy (story-bible timeline, 20 → 11 years
ago). It is a solemn mirror of the Old Light: a tower climbed in the dark.

**Maps.** The existing `drownlight_beacon` (18×16) becomes the tower's foot: a ruined quay and the
door. Inside:
- `drownlight_f1` and `drownlight_f2` (lv 50–53): the climb.
- `drownlight_lantern`: the lantern room, with the Shutterkeeper.

The floors use **shutter puzzles** built on the existing data mechanics. A shutter is a
lever-style flag that swaps a light-beam object (`requires_flag`/`hidden_when_flag`). The beams
gate passage the way the Old Seams junctions do: walking through a beam is barred by an
AbilityGate-free blocked step band, or by flag-gated flows/objects. Every state must be solvable.

**Top: the Shutterkeeper** (Hollowing elder, keeper/warden-class, ace ~54), who shuttered it
herself. Win, and she does NOT relight it. She tells you why she put it out, and leaves the choice
for after the dawn. **After the dawn** you can relight it (a lamp beat, minor → major); the
coast's buoys wake (Ambience `when`). Rewards: a Lumen Drop, a Starglass Shard, the
**Shutter Charm** (a new conditional charge, ×2.5 on Dark-type kin; no price).

## C · The Mourning Fields — the loop

`mourning_fields`, route, 26×32, world `(68,-461)`. Its west edge meets Coldfog I's east edge;
its north edge meets Stillwater's south edge at x 68–78; its south edge meets **Rimeway Descent**'s
north edge. That makes the north a **loop** (Coldfog I → Stillwater → Mourning Fields → Coldfog I)
with a return compressor down to the Rimeway. The ground is the fallow fields the Hollowing
quieted: sleeping kin under grey blankets of coldfog, scarecrow lamp-posts, two acolyte sight
trainers, a seen-before-reached field shrine, a cache. Lv 48–52.

## D · The Penumbra Underways — the last road (endgame)

The genre's "last road" before the climax is missing. Two portal cave floors under the Penumbra
Ring, gated `flag:hub_unlocked` + `starreach`, optional but tempting:
- `penumbra_underways` and `penumbra_underways_b1`, lv 52–56.
- The strongest wild Dark/Light beds.
- The Hollowing's **last watch** (3 sight trainers).
- A rest point, and the last Lumen Drop before the summit.
- A seen-before-reached view up into the Spire's shaft.

It never connects to the Spire itself. You come back out into the Ring.

## E · Density on the existing late maps

Coldfog I/II gain Hollowing acolyte sight trainers (2 each), people (an elegiac fen-walker, a
Stillwater trader), and a Lamplight-starlight secret each. The Nightreach lane gets its
lamplighters. Sunvault Climb II–IV get a talkable climber each. All of this goes through the owning
builder or runner, and any pre-Chickenpig restrictions apply. `audit_visual` stays at 0 FAIL.

## F · Kin (#178–#180, region `north_hollow`, table-only like `isles`)

A small Hollowing family. All designs are original; avoid any existing franchise's names.
- #178: a lamp-snuffer cap kin (Dark/Ember) that kindles at lv 44 into #179, the shuttered
  lantern-keeper (Dark/Light).
- #180: a grey dream-moth that keeps sleeping kin asleep (Dark/Lunar), single stage.

They're wild in Stillwater's grey meadows, the Mourning Fields and the Drownlight floors. Every
kin goes through the roster pipeline and sim, with full art, cries and chatter.

## Audio

- `stillwater`: a hush-hymn, muted, a music-box with a felt damper.
- The Drownlight family: `drownlight-f1`, `drownlight-f2`, `drownlight-lantern`, built on one
  motif, darker as you climb, with the relight cue major. Use the music-cue-family skill.
- `mourning-fields`.
- `penumbra-underways`.

Every cue has a classic render and a remaster, except battles (classic-only, as house rule).

## Build contract

**Lanes:**
- **N1** = A + E (Coldfog/Nightreach lane/Sunvault density).
- **N2** = B.
- **N3** = C + D.
- **N4** = F (kin).

Each lane owns its own music and art. Scripts go in `content/regions/{stillwater,drownlight,
mournfields,underways}.ts`.

**Warps:**

| Seam | Owners | Detail |
|---|---|---|
| Stillwater ↔ Coldfog I | N1 owns both sides | Coldfog I's north edge, x 52–55 (two-tile or wider) |
| Stillwater ↔ Mourning Fields | Stillwater side N1, Mourning Fields side N3 | x 70–73 of world (Stillwater cols 22–25 ↔ MF cols 2–5). Each lane builds its own side to that column range. |
| Mourning Fields ↔ Coldfog I | N3 owns the MF side; N1 adds the matching Coldfog I east-edge warps | world rows y -450..-447 (Coldfog I rows 11–14 ↔ MF rows 11–14) |
| Mourning Fields ↔ Rimeway Descent | N3 owns both sides | MF south edge cols 10–13 ↔ Rimeway Descent north edge cols 16–19 |
| Drownlight foot ↔ F1 | N2 | |
| Penumbra Ring ↔ Underways | N3 | a mouth in the Ring, gated |

**Flags:**
- `flag:q_still_*` (Stillwater quests)
- `flag:drownlight_*`
- `flag:drownlight_keeper_beaten`
- `flag:drownlight_relit` (post-dawn)
- `flag:underways_*`

**Kin ids:** #178–#180, fixed.

**Levels:**
- Coldfog 46–50
- Stillwater 48–52
- Mourning Fields 48–52
- Drownlight 50–54
- Underways 52–56

All of these beds go in TREND_SKIP_AREAS.
