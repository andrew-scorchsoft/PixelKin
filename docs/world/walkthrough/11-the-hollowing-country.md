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

**BUILT (Lane N1, 2026-10).** `tools/maps/build_stillwater.py` (+ `build_stillwater_interiors.py`,
the shutter-grey kit `build_stillwater_interior_set.py`, the `flagway` lane family
`build_stillwater_set.py`, drawn props `stillwaterforge.py`, five image-gen buildings in
`assets/tilesets/stillwater/objects/`). Content: `content/regions/stillwater.ts`.
- **Layout:** the Still Water (its own drawn `mere` family: a stone-lipped, reed-fringed shore,
  water still enough to hold stars, a walk-on jetty with the last fishing punt) under the north
  crags, its shore walk lined with shuttered lamp-posts; the Quiet Hall on the square, the Shutter (inn) west, the dark-lamp
  maker east, two homes south; grey meadows NW/NE/S + the lampmaker's yard (#178's bed); wash-lines, woodpiles and
  crag boulders dress the yards and the rim. The village lamp-stone on the square is a TRAVEL
  waystone (`content/waystones.ts`, gated `chart:stillwater`).
  Seams: south cols 4-7 ⇄ Coldfog I; south cols 22-25 → `mourning_fields` (2-5, 1).
- **People (~20 incl. rooms):** Elder Ashe, Keeper Wenna (the hall), Osric the lamp-maker
  (shop `stillwater_lampmaker`, incl. the Hooded Lamp), Maren + Linnet, Tessaly, Grete, Odo,
  Lisbet, Corwen (the doubter), Hallam, Nell, Margery + Edwy, the innkeeper. Three trainers who
  talk first (choice → battle): Gethin (ace 50), Vesna (51), Grisel (52), keeper class.
- **Quests:** *A Light Left On* (`flag:q_still_candle*` — Linnet's candle to the willow hollow or
  to Maren; a Starglass Shard either way); *The Way Home* (`flag:q_still_tessaly*` — she waits
  in Coldfog I, then Coldfog II, then home at Pale Vault `pale_vault_glacier` (6,22) via
  `hand_placed_data.py`; reward: **Tessaly's Lamp**, ONE reusable keepsake charge, ×3.0 on a
  kin below 25% HP); *The Shutter-wall* (`flag:q_still_wall`, three cold lamps: Coldfog I `named_lamp_1`,
  Coldfog II `named_lamp_2`, Stillwater's far shore; a Lumen Drop + 1,500w; Wenna names
  whichever lamps are still missing).
- **Hearths:** every Stillwater hearth (the inn, both homes) is BANKED behind a louvred
  fire-screen (`stillwater_hearth_banked`), its "face to the wall"; the open hearth swaps back
  in at `flag:dawn` (a same-footprint flag pair). Home A (Margery + Edwy) is a wide hearth-room
  with two chairs backed to the hearth and Old Bracken's basket by the bed; home B (Maren +
  Linnet) is tall, with Linnet's own walled room and the candle shelf (once Maren has seen it).
- **After the dawn:** two shore lamps open and lit (flag-pair objects), home B's upstairs
  window opens with a lamp and a child at it (`stillwater_window_lit`), the mist thins
  (ambience `when`), the meadows' day-forms rise, every resident gets a dawn line, the hearths open.
- **Wild levels:** every line at 46+ wears its kindled form (Voidmantle, Liminalux, Embergone,
  Omenire) in Stillwater and both Coldfog marshes, wild AND in the acolytes' parties; Coldfog I's
  gold pocket is the half-lit bed (Liminalux, Voidmantle, the lone Wisprestored). The base
  Mothdim/Flutterwane now live only in Glowmoss Deep's drained chamber (lv 18-21, after the
  null-lantern is relit), below their kindling.
- **Music:** `stillwater` (classic chip, snes register, 72 BPM 3/4 D minor) + remaster.
  Backdrop `stillwater-a.webp`; chart `stillwater` (unlocks the LORE entry).

## B · The Drownlight — the first lamp the Hollowing put out

**Lore.** The Drownlight Beacon was the north coast's light. It was the Hollowing's first:
they shuttered it the winter Còr's grief became a philosophy (story-bible timeline, 20 → 11 years
ago). It is a solemn mirror of the Old Light: a tower climbed in the dark.

**Maps.** The existing `drownlight_beacon` (18×16) becomes the tower's foot: a ruined quay and the
door. Inside:
- `drownlight_f1` and `drownlight_f2` (lv 50–53): the climb. **Final forms only** at this band,
  in the wild AND on the acolytes' teams: F1 is Shutterwick (#179) / Voidmantle / Lullwing (#180) /
  Stillwarden / Liminalux; F2 adds Prismantus; the foot's blight-tuft beds are Voidmantle /
  Shutterwick / Lullwing / Liminalux (no Mothdim, Nullmoth or Wispwane past their kindling).
- `drownlight_lantern`: the lantern room, with the Shutterkeeper.

The floors use **shutter puzzles** built on the existing data mechanics. A shutter is a
lever-style flag that swaps a light-beam object (`requires_flag`/`hidden_when_flag`). The beams
gate passage the way the Old Seams junctions do: walking through a beam is barred by an
AbilityGate-free blocked step band, or by flag-gated flows/objects. Every state must be solvable.

**Top: the Shutterkeeper** (Hollowing elder, keeper/warden-class, ace ~54), who shuttered it
herself. Win, and she does NOT relight it. She tells you why she put it out, and leaves the choice
for after the dawn. **After the dawn** you can relight it (a lamp beat, minor → major) — only
once she has told her tale (the lamp waits on `flag:drownlight_keeper_beaten`); the coast's buoys
wake and the beam sweeps the shallows from the foot (Ambience `when` + `beams`). Rewards: a Lumen
Drop, a Starglass Shard, and the **Shutter Charm**: the first shutter's own latch, ONE per game
and REUSABLE (`reusable: true`, never spent), a conditional charge ×2.5 on Dark-type kin; no price.

## C · The Mourning Fields — the loop

`mourning_fields`, route, 26×32, world `(68,-461)`. Its west edge meets Coldfog I's east edge;
its north edge meets Stillwater's south edge at x 68–78; its south edge meets **Rimeway Descent**'s
north edge. That makes the north a **loop** (Coldfog I → Stillwater → Mourning Fields → Coldfog I)
with a return compressor down to the Rimeway. The ground is the fallow fields the Hollowing
quieted: sleeping kin under grey blankets of coldfog, scarecrow lamp-posts, two acolyte sight
trainers, a seen-before-reached field shrine, a cache. Lv 48–52.

**Built (Lane N3):** `tools/maps/build_mourning_fields.py`; scripts in
`content/regions/mournfields.ts`; props drawn by `tools/maps/draw_mournfields_objects.py`.
The bank (row 10) is a scree ledge across the west half: hop down from the Stillwater road
straight to the Coldfog gate; going up means east across the barley-drift crossing to the one
walk-up (x 17, guarded by Ines) and back west. The shrine shelf is entered by the drop from
the upper terrace and left by a ledge. The sleepers and the scarecrow-lamps have `flag:dawn`
twins. Acolytes: Ines (ace 50), Corran (ace 51). Rimeway Descent's north road (cols 16–19)
is the col.

**Second review pass (2026-10-14):** the south crossing is a lobed drift (both edges wave, every
column a contiguous wall-to-wall run, so it stays mandatory); the plots step one tile at a time
and the stubble family's convex corners are rounded (r 7). The **Brook Piece**, the fifth name on
the shrine board, is a bramble-walled nook in the col's west corner: seen from the Rimeway road,
reached only through the long grass and under the snow pine. The field-tender's own old Hushvole,
Tussock, sleeps there (a `flag:dawn` twin), with a marker stone and a Hearth Coal. The **Harvest
Knot** (terrace cache) is a toggle key item (`flag:harvest_knot_hung`, encounter ×0.25, the
strongest damper; key, so never sold). At dawn the shrine swaps to `field_shrine_lit` (all five
candles burning, a light pool), and the shrine and the tender each get a dawn line.

## D · The Penumbra Underways — the last road (endgame)

The genre's "last road" before the climax is missing. Two portal cave floors under the Penumbra
Ring, gated `flag:hub_unlocked` + `starreach`, optional but tempting:
- `penumbra_underways` and `penumbra_underways_b1`, lv 52–56.
- The strongest wild Dark/Light beds.
- The Hollowing's **last watch** (3 sight trainers).
- A rest point, and the last Lumen Drop before the summit.
- A seen-before-reached view up into the Spire's shaft.

It never connects to the Spire itself. You come back out into the Ring.

**Built (Lane N3):** `tools/maps/build_penumbra_underways.py` (+ two mouths in
`build_penumbra_ring.py`); scripts in `content/regions/underways.ts`. A loop: in by the Ring's
SW mouth (4–5,32), down the west galleries (Odalie, ace 54; a Starglass Shard), down to B1,
the Last Watch (Bran, ace 55; Old Clemency; the watch-fire rest point; the view up the Spire's
shaft, a solid prop), and up through the east galleries (Hesk, ace 56) to the SE mouth
(22–23,32). Both mouths stand on islets in the starlit dark and are gated `flag:hub_unlocked`
+ `starreach`. The last Lumen Drop is in B1's south-east pocket (the slump drops into it).

**Review fix FD (2026-10-14).** The watch-fire's keeper is **Old Clemency**, who taught Còr his
letters (she was "Old Maudry"; the name belongs to Maudry Kell, the Drownlight's Shutterkeeper,
who met Còr as a stranger). Both floors are re-carved as organic chambers with 1-wide chokes and
dressed in the watch's own drawn kit (`tools/maps/underwaysforge.py`: bedrolls, a map table, a
watch-bell, ration crates, a kettle shelf, a watch-rota, fallen Spire masonry, root curtains). F1's
side bay ends in a rubble lip that drops one-way into the cistern hall, so the walk back is by
Odalie's cut. B1's south-east pocket is **the Warm Stones**: its own bed (Shutterwick #179,
Lullwing, Lumenmoss, Liminalux, a rare **Embralux #33**, the only pre-dawn Embralux ground, and a
rare **JesterFull #168**, its ONLY wild home anywhere: a whole jest-house kin come down to do its
turn for the watch), signed and mentioned by Clemency. Every zone has a post-dawn `_day` twin (56–60). Signposts: Andrew's
Crown-stage hint adds a P.S. once `flag:hub_unlocked`; the mouths' "not yet" is a script; and the
Ring's south strip has an iron **light-well** (9–10,30–31) looking down on the shaft's pale column and
the watch's fire, seen before reached. Any of these opens the JOURNAL's **The Last Watch**
(`flag:q_underways`, kept at `flag:underways_watch_kept` once Clemency hears you met all three
watchers) and the LORE entry "the Last Watch". **Fix FD2 (2026-10-14):** keeping the watch changes
the world: Clemency rings the watch-bell and Odalie, Bran and Hesk leave their posts (empty from
then on) to sit at her fire, with dusk and dawn lines (`script.underways_watch_*_fire`). The lower
halls and B1's west bay and south gallery gained the watch's hammocks, a slate of names, cold
braziers (lit at dawn), hoods drying, water-butts and firewood; B1's south gallery now joins the
watch on foot (the spur stopped a tile short), so the Warm Stones are a loop, not a drop.

## E · Density on the existing late maps

Coldfog I/II gain Hollowing acolyte sight trainers (2 each), people (an elegiac fen-walker, a
Stillwater trader), and a Lamplight-starlight secret each. The Nightreach lane gets its
lamplighters. Sunvault Climb II–IV get a talkable climber each. All of this goes through the owning
builder or runner, and any pre-Chickenpig restrictions apply. `audit_visual` stays at 0 FAIL.

**BUILT (Lane N1, 2026-10).** Coldfog I (`build_coldfog_marches_i.py`): the north gap to
Stillwater, the east edge rows 11-14 → `mourning_fields` (1, y), sight acolytes Brin (10,8)
and Fenwick (16,14), Sefton the Stillwater trader (shop `stillwater_trader`) at the gap, a
fen-walker, the Wayfare Lamp, Tessaly's first stop, a `flag:lamplight_starlight` cache.
Coldfog II (`build_coldfog_marches_ii.py`): sight acolytes Odran (25,12) and Marrow (7,12),
a mourner at the quieted camp, the Market Lamp, Tessaly's second stop, a Starlight cache.
The Nightreach lane's two lamplighters and a talkable climber on Sunvault Climb II-IV ride
`hand_placed_data.py` (`_N1_NPCS`). Coldfog trainers ace 48-50, keeper class.

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
