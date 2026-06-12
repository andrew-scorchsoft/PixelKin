# PixelKin Walkthrough — 07 · The Three Hours (legendary triad — MAIN-GAME optional)

> Region-crossing file under the [spine](./README.md). Read its §0 rules, §2 flag strings,
> §4 curve, §5 (earned loops, Lamplight, the optional-content web), §7 template and §10 voice
> first — all binding here. Mechanics ground: [`02-stats-and-balance.md`](../../mechanics/02-stats-and-balance.md)
> (E-tier), [`04-capture.md`](../../mechanics/04-capture.md) (the four-shake roll),
> and the **`legendaryBattle` cutscene op** (`LegendaryBattleStep`, `src/game/content/types.ts`)
> — every set-piece below is written verbatim against that op. Canon vocabulary only:
> **kin, Lumenary, Lampwarden, Gleam, Lantern Gift, vesperlamp, kindling, the Hollowing.**
>
> **Scope and ownership.** This file owns: the triad **#160–#162**, their three sites
> (one new-map annex per region quadrant, plus the long-owed **Tideglass Cavern** build),
> their unlock chains (`flag:three_*`), puzzles, fights, and cooldowns. It does **not**
> touch [`06-postgame.md`](./06-postgame.md): the Starfall Vigils own the post-`dawn`
> challenge chain; the Hours are **mid-to-late MAIN-GAME optional content** — different
> sites, different bands, different rewards, different register (see the non-overlap
> checklist at the end). Existing region files keep ownership of their host maps; this
> file adds, per host, exactly the one-warp/one-NPC edits listed in its hooks (the same
> convention the Vigils use).

## Design intent (the player promise)

Three legendary kin, each at the end of an **earned offshoot** — a side-quest-shaped unlock
chain, then one real approach puzzle (a different verb per site), then the hardest wild fight
the player has met at that point of the journey. **Quite difficult relative to where you are;
never impossible.** The fight is a *chance, not a gift*: a failed catch (KO or flee) makes the
Hour withdraw for a **battles-won cooldown** with a diegetic hint — a real cost, never a nag.
All of it optional; nothing on the main path ever requires an Hour.

| # | Kin | Hour | Types | Site (annex of) | Reachable from ~ | Fight | Cooldown |
|---|-----|------|-------|-----------------|------------------|-------|----------|
| 160 | **Gloamber** | Dusk — the First Hour | Ember/Dark | **Tideglass Cavern** (Dimglass II, South) | Glimmerstep (~lv 22) | **lv 38** | 10 won |
| 161 | **Noctilune** | Midnight — the Still Hour | Lunar/Dark | **the Hourfold** (Pale Vault deep ice, North) | post-Frost Gleam (~lv 40) | **lv 48** | 14 won |
| 162 | **Erstmorn** | Dawn-that-was — the Lost Hour | Solar/Light | **the Unrisen Stair** (Sunken Solarium, West) | post-Lunar Gleam (~lv 52) | **lv 55** | 18 won |

---

## 1. The triad in the Skyweave — *the Hours of the turning*

The Skyweave holds the eight anchor-constellations: the **places** of the sky. The Hours are
its **turning**: the three watch-spirits of the cycle itself — dusk, midnight, and dawn — the
keepers of the wheel the Skyweave was woven around. For as long as people tended the light,
the Hours passed through Vesperholm unseen, each handing the sky to the next: Gloamber drew
the curtain, Noctilune kept the watch, Erstmorn opened the morning.

Then the Long Dusk fell, and **the wheel jammed**:

- **Gloamber** has carried an evening it was never allowed to put down. The First Hour grew
  heavy, went to ground, and banked the day's last ember where the dark couldn't reach it.
- **Noctilune** stands a watch with no relief. The Still Hour is the one the Hollowing
  half-worship — proof, they say, that the dark can be gentle. It has never once answered them.
- **Erstmorn** waits, **half-finished**, where the morning was meant to land. The Lost Hour
  is the ache of the whole game made into a creature: a dawn sketched and never painted in.

This is why the triad matters to the main story without gating it: Còr wants to stop the
wheel forever; the Hours *are* the wheel. Meeting Erstmorn before the Spire is deliberate
foreshadowing — the wheel still wants to turn; the climax is the player finishing the job.

**Tone (binding).** Awe and ache. Meeting an Hour is mythic — staged with `silence`,
`letterbox`, a single sting, never spectacle for its own sake. **No humour at the sites.**
One dry line is permitted per unlock chain, on the rumour-giver only (written below). The
Hollowing are never present at a site; Noctilune's section carries their *shadow* only.

---

## 2. The kin (dossiers for the species pipeline)

All three: **tier E** · **BST 558** · **catchRate 24** · `rarity: very_rare` →
**`scripted: true`, `encounters: []`** (the generator derives this exactly as it does for
Lunaveil/Keylumen — a scripted legendary never enters open tables). EPS lands inside the
E-band (~591–613); `validate.mjs` is the gate. Stats below are the **exact deterministic
output** of `build_species.py make_stats(role, 558, name)` — no stat override needed.
Distinct shapes by design: one tank, one wall, one speedster.

### #160 Gloamber — *the Dusk Hour* (Ember/Dark · Special Tank)

- **Stats:** hp 112 · atk 50 · def 78 · spa 123 · spd 100 · spe 95 (BST 558)
- **Ability:** `nightfall` (on switch-in: night — the First Hour draws the curtain) ·
  hidden `emberheart` (Ember ×1.5 below half — the banked coal flares when pressed).
  *(CANON override; the generator's Ember-E default is `daybringer`, wrong for a dusk kin.)*
- **Battle kit (as met, lv 38 — all from the existing 125-move pool, no signature moves):**
  `scorch_veil` · `hearth_pulse` · `mend` · `gloomswell`. The rare combo IS the signature:
  a 112/100 special tank that scorches, heals half, and answers with Dark — the hearth that
  will not go out. Pinned learnset rows: 1 `cinder_spit` · 9 `scorch_veil` · 13 `hearth_pulse`
  · 24 `mend` · 31 `gloomswell` · 44 `sunflare_burst` · 52 `voidburst` (post-catch growth).
- **Catch design:** scorch is its own tool, so bring `chill`/`doze` for the ×2.5 status
  bonus; its `mend` punishes slow whittling — the lesson is *commit*.
- **Dex (canon voice):** "The First Hour — the keeper of dusk, grown heavy with an evening it
  has never been allowed to put down. Lamp-tenders say every wick in Vesperholm is lit from
  the one coal it carries, at one remove or another."
- **Category:** Dusk Hour Kin · **size** 170 cm · **weight** 88 kg · **habitat** south
- **Art block** (drives `gen_creature.py`):
  - *silhouette:* "A long, low lynx-like beast, heavy-lidded and patient, built close to the
    ground like something settling in for the night. A banked mane of small, steady flame-tongues
    runs low along the neck and shoulders — embers, not fire. At its chest, a locket of teal
    sea-glass holds one bright coal. The tail ends in a slow curl of pale smoke. Reads at 64px
    as a dark animal carrying one precious light."
  - *palette:* "Charcoal-violet fur deepening to ink (#1a1430) along the spine like a sky losing
    its light; ember amber (#ff8a3d) and rose for the banked mane; diamond-teal sea-glass locket;
    a faint dusk-rose gradient on the brow and flanks."
  - *direction:* "The moment of lamp-lighting as an animal. Heavy, warm at the core, unhurried —
    the dusk as a keeper, not a threat. The single chest-coal must read as the brightest pixel
    on the sprite."

### #161 Noctilune — *the Still Hour* (Lunar/Dark · Physical Wall)

- **Stats:** hp 106 · atk 78 · def 136 · spa 48 · spd 95 · spe 95 (BST 558)
- **Ability:** `mirrorlight` (reflects the first status — midnight gives back what it is
  given) · hidden `nightsight`. *(CANON override; the Lunar-E default `nightfall` is already
  Gloamber's curtain — Midnight doesn't bring the night, it IS the night.)*
- **Battle kit (as met, lv 48):** `lull` · `bulwark` · `nightfall_veil` · `shadow_rend`.
  Pinned rows: 1 `moon_nip` · 13 `moonshard` · 24 `lull` · 30 `bulwark` · 38 `nightfall_veil`
  · 46 `shadow_rend` · 54 `eclipse_wave` (post-catch growth).
- **Catch design:** `mirrorlight` bounces your FIRST status move — the puzzle inside the
  fight. Burn the reflect on something cheap, *then* land the doze/chill; def 136 +
  `bulwark` makes the physical whittle a war of patience.
- **Dex:** "The Still Hour — the keeper of midnight, standing the same unrelieved watch since
  the night stopped turning. The Hollowing call it proof that the dark can be gentle;
  Noctilune, for its part, has never once answered them."
- **Category:** Midnight Hour Kin · **size** 260 cm · **weight** 420 kg · **habitat** north
- **Art block:**
  - *silhouette:* "A huge pangolin-like sentinel, its overlapping scales panes of midnight-blue
    glass, each pane holding exactly one star-speck. Standing, it reads as a hooded watchman;
    curled, as a dark moonless disc. A small unstruck bell of dark ice hangs at its throat.
    Eyes are two thin silver crescents. At 64px it should read like a piece of the midnight
    sky knelt down to wait."
  - *palette:* "Night (#0b1026) and deepBlue (#13205a) scale-panes; diamond (#9fe7ff)
    star-specks, one per scale; pale moon-grey underbelly and claws; the throat-bell a darker,
    colder blue than everything around it."
  - *direction:* "The deep of night as armour. Utterly still until it isn't. No menace —
    endurance. The unstruck bell is the motif: midnight is the hour no bell marks."

### #162 Erstmorn — *the Lost Hour* (Solar/Light · Utility / Speedster)

- **Stats:** hp 79 · atk 84 · def 84 · spa 84 · spd 84 · spe 143 (BST 558)
- **Ability:** `daybringer` (on switch-in: sun — it carries its own morning, because the sky
  won't supply one) · hidden `sunsoak`. *(Generator defaults for Solar-E — no override.)*
- **Battle kit (as met, lv 55):** `dazzle_flash` · `sun_nap` · `light_pulse` · `sunburst_nova`.
  The rare combo: `daybringer` + `sun_nap` — it heals half under a sun only it remembers —
  on a spe-143 frame. Pinned rows: 1 `sun_jab` · 13 `glint_ray` · 22 `daybeam` ·
  28 `dazzle_flash` · 36 `sun_nap` · 44 `light_pulse` · 52 `sunburst_nova`.
- **Catch design:** the hardest of the three — it outspeeds everything, dazzles your
  accuracy, and naps the chip damage back. Doze is the honest road; the player who saved a
  guaranteed Starlamp all game finally has its moment (never required).
- **Dex:** "The Lost Hour — the keeper of a dawn that has not come, waiting half-finished
  where the morning was meant to land. Those who meet it say the worst part is its patience:
  it does not doubt the sunrise, and it will not be told the years."
- **Category:** Dawn Hour Kin · **size** 200 cm · **weight** 64 kg · **habitat** west
- **Art block:**
  - *silhouette:* "A tall, slender hare of pale gold light, mid-stride even when standing.
    Long ears trail behind it like horizon ribbons. Parts of its outline are UNFINISHED — one
    hindquarter and the tip of one ear fade into faint sketch-lines of light, as if the painter
    stopped at the moment the dawn did. The missing parts must read as waiting, not wounded."
  - *palette:* "Bone (#f5f0e1) and pale gold body; a sunrise gradient of rose and amber along
    the spine and ear-ribbons; the unfinished edges in faint diamond-cyan (#9fe7ff)
    sketch-lines over transparency."
  - *direction:* "An unfinished sunrise as a creature — fast, gentle, heartbreaking. The
    emotional apex of the triad: in the Long Dusk it is incomplete by definition, and the
    sprite should make the player want to fix that."

> **Forward hook (non-binding, no wiring, owned by nobody yet):** post-`flag:dawn`, Erstmorn
> is the one Hour whose ache resolves — in real daylight it is *finished*. A future post-game
> pass MAY pick this up (a dawn-form sprite swap); this file deliberately wires nothing.

---

## 3. The shared grammar (binding on all three sites)

1. **Offshoot, not stop.** Each site is an annex off a shipped region — a one-warp host edit,
   a small new map, no main-path change. Each is `[LATER]`-tagged from its host region's
   optional content and **trainer-free** (no trainer NPCs, no payouts; the catch is the
   reward — catches already pay XP like knock-outs).
2. **Side-quest-shaped unlock.** A rumour-giver opens the chain (`flag:three_*_rumour`), 2–3
   steps follow the spine §5 named-quest format, and the final flag unseals the approach.
   Every flag opened is consumed (spine §0 rule 3). Collinearity rule honoured: every errand
   sits on ground the main path already walks at that band.
3. **One puzzle verb per site, engine-expressible today.** Dusk = an ordered **light relay**
   (flag-chained interacts, the Helia/Walk-of-the-Seven precedent). Midnight = a one-way
   **ledge descent** plus an inverted chain — for once, you **snuff** lights. Dawn = a
   **Sunsketch bloom route** (sequential + redirect, the spine §5 "expressible now" set).
   Hints are always diegetic (a verse, the aurora, the basin) — puzzles are readable, never
   obtuse.
4. **The fight is the `legendaryBattle` op, verbatim.** Staged by an interact NPC placement
   using the kin's packed overworld view (`kin_<id>_overworld`), carrying
   `hidden_when_flag: <caughtFlag>` (the op's own caught-check is the belt-and-braces). The
   kin cannot flee; the player may. **KO or player-flee = withdrawal**: `cooldownBattles`
   WON battles before it returns, with the `cooldownRef` resting line (the `{remaining}`
   hint) playing from the same trigger. Escalation across the triad: **10 → 14 → 18**.
5. **Staging cadence (per [`cinematics.md`](../cinematics.md)):** approach in the area bed →
   `letterbox` + `silence` at the threshold → one `narrate` line → `musicSting` →
   the shared triad battle bed → the op. After a catch: hold a beat of quiet, then the area
   bed returns warmer (`musicCrossfade`). Never a fanfare — an Hour joining you is a vow,
   not a victory.
6. **Assets owed (shared):** one battle bed `battle-hours` (*generate-midi: boss preset ·
   slow, vast, 3/4 like a great clock under the music · low tri-bass pendulum + sparse bell
   "hour-marks" + a patient minor lead that resolves one chord further each loop · ~76 BPM ·
   loop*) and one sting `sting-hour` (a single deep bell-toll with a long shimmer tail).
   Battle backdrops per site listed in each section.

**LORE codex (data, no new wiring):** add glossary entry **"The Three Hours"**
(`unlock_flag: flag:three_dusk_rumour`) — the netmender's rumour is the world learning the
word — and **"The Hours' Withdrawal"** (`unlock_flag: flag:three_dusk_caught`, any-Hour
variant acceptable).

---

## 4. Site I — Tideglass Cavern — *the Dusk Hour below the glass* (South)

The long-teased South landmark finally pays. This section is also the **build spec for
`tideglass_cavern` itself** — the node and Glimmerstep edge have shipped in `graph.ts`
since launch (`graph.ts:84`, `graph.ts:214`), the `to_tideglass` warp already stands on
`dimglass_coast_ii`, and three standing obligations land here: the atlas card's
**signature rare water kin**, quest **S3's wreck-lamp trigger** (01-south), and the spine
§5 **Lamplight Starlight nook**.

**At a glance** — `tideglass_cavern` (main floor) + `tideglass_gallery` (B1F, NEW) · cave
landmark · south · entry: `dimglass_coast_ii` via `to_tideglass`
(**`requires_ability: glimmerstep`**, shipped) · Hour fight **lv 38** · cavern bed 20–24 ·
first reachable ~lv 22 (post-Lowleaf backtrack — the fight is meant to loom over that visit).

1. **Main path**
   1. **The cavern at last.** A sea-cave of smoothed glass: black water pools, walls run with
      veins of translucent teal that catch and bend the lamp (`diamond` glints on `ink`).
      Dark terrain — Lamplight applies; the lit lane is glowmoss-veined glass.
   2. **The wreck and the lamp (S3 pays).** At the far end, the old fisher's wrecked boat,
      its wreck-lamp cold. Relighting it is S3's shipped beat (`flag:q_south_wrecklamp_lit`).
   3. **The verse.** With the wreck-lamp burning AND the netmender's rumour heard, its glass
      hood reads as etched writing (`script.three_dusk_verse`): *"Last light first; the low
      light after; the deep light once the others hold."* Sets `flag:three_dusk_verse`.
   4. **The Lampwright's Relay (the puzzle).** Three standing sea-glass lenses: the **amber
      lens** on the west shelf, the **low lens** on the mid-pool islet, the **deep lens** by
      the stair seam. Lit in verse order, each carries the wreck-lamp's beam one span deeper;
      out of order, the glass stays cold (inert/live flag-pair placements). `lens_c` rings a
      low note through the floor and the stair seam breathes open.
   5. **Down to the Gallery.** A glass stair to `tideglass_gallery` (B1F): one small chamber
      where the relayed beam pools — and in the pooled light, a long, low shape that has been
      waiting for someone to bring the evening's ember back to it. The fight.
2. **Story beats** — none of the main arcs land here (a landmark, not a plot stop). The one
   note is the Hour itself: dusk as a *keeper*, the first proof the night has tenders of its
   own.
   - **Cinematic staging:** threshold of the Gallery → `letterbox` + `silence 900` →
     `narrate: "The glass warms. Something that has carried the evening a long time lifts
     its head."` → `sting-hour` → `battle-hours` → the op.
3. **Mechanic introductions** — the triad grammar itself: the relay (flag-chained interacts),
   the legendary withdraw/cooldown loop, and the "chance, not gift" catch framing.
4. **Optional content**
   - **The cavern bed** — `[MUST-DO once inside]` Tide kin, band 20–24, `cave`/`water`
     zones; the atlas-promised **signature rare water kin** as the very-rare row (suggest,
     non-binding: the Glostern line's middle form — it seeds Pharolux's "living lighthouse"
     legend two doors from where players caught Glostern).
   - **Starlight nook** — `[LATER: Lamplight ≥ Starlight]` the spine §5 reveal: a deeper
     fold off the main floor with a hidden item (suggest a Starglass Shard) — also S3's
     "deeper page".
   - **H1 quest (the unlock chain)** — see Named quests below.
5. **Don't-miss callouts** — light the wreck-lamp BEFORE puzzling at the lenses (the relay
   needs a source); the cavern at ~22 is a fine catching trip even if you shelve the Hour
   for later — the Gallery will keep.

   **Named quests** (spine §5 format):
   - **H1 "The Hour Below"** — giver: the **Pearlmoor netmender** (post `gleam:verdant`,
     i.e. Glimmerstep held) · steps: hear the rumour (`script.netmender_hours` →
     `flag:three_dusk_rumour`) → light the wreck-lamp (S3's shipped trigger — collinear
     reuse, no new ground) → read the verse (`flag:three_dusk_verse`) → run the relay →
     face the Hour · reward: the **chance at Gloamber** (no item — the Hour is the prize) ·
     maps: `pearlmoor_quay`, `tideglass_cavern`, `tideglass_gallery` · `[LATER: Glimmerstep]`.
     The chain's one permitted dry line, the netmender's:
     > "There's a low singing in the cliff at lamp-lighting time. Could be the tide.
     > Tide's never once kept a tune before, mind."

6. **Validation hooks** (against built `tideglass_cavern.json` / `tideglass_gallery.json`)
   - **Map ids / kind:** `tideglass_cavern` (cave, ~26×20) + `tideglass_gallery` (cave,
     ~18×14, NEW node + ladder-pair edges in `graph.ts`, the `glowmoss_deep_b1f` pattern).
     Region `south`. Both `dark` (Lamplight maps).
   - **Entry/exit:** in from `dimglass_coast_ii` via `to_tideglass`
     (`requires_ability: glimmerstep`, bidir — **shipped**; the built map must land the
     player at the already-pinned coord `{tx:4, ty:8}` beside a return warp,
     `audit_warps` convention). `tideglass_cavern ↔ tideglass_gallery` via
     `stair_down`/`stair_up` step_on pair landing on each other; `stair_down`
     **`requires_flag: flag:three_dusk_lens_c`** with `blocked_ref:
     npc.tideglass_stair_sealed` ("A seam in the glass breathes cold air. It is not open.").
   - **Triggers / flags (opened ⇒ consumed):**
     | Flag | Set by | Consumed by |
     |---|---|---|
     | `flag:three_dusk_rumour` | `script.netmender_hours` (Pearlmoor) | verse plaque `requires_flag`; netmender swap pair |
     | `flag:three_dusk_verse` | `script.three_dusk_verse` (requires `flag:q_south_wrecklamp_lit` + rumour) | lens A live-placement `requires_flag` |
     | `flag:three_dusk_lens_a/_b/_c` | `script.three_dusk_lens_a/_b/_c` (each requires the previous; inert twins `hidden_when_flag`-swapped) | next lens in chain; `_c` → the stair warp gate |
     | `flag:three_dusk_caught` | the `legendaryBattle` op | `hidden_when_flag` on the Hour placement; LORE unlock |
   - **The set-piece (verbatim, `content/scripts.ts`):**
     ```ts
     'script.three_dusk_battle': [
       { op: 'letterbox', on: true },
       { op: 'silence', ms: 900 },
       { op: 'narrate', text: 'The glass warms. Something that has carried the evening a long time lifts its head.' },
       { op: 'letterbox', on: false },
       { op: 'musicSting', key: 'sting-hour' },
       { op: 'music', key: 'battle-hours' },
       { op: 'legendaryBattle',
         name: 'three_dusk', kin: 160, level: 38,
         caughtFlag: 'flag:three_dusk_caught',
         cooldownBattles: 10,
         cooldownRef: 'npc.three_dusk_resting',
         terrain: 'cave' },
     ]
     ```
     Staged by NPC placement `hour_dusk` (sprite `kin_160_overworld`, interact →
     `script.three_dusk_battle`, `hidden_when_flag: flag:three_dusk_caught`) on the
     Gallery's far ledge — the approach is a 1-wide glass spit, so the trigger cannot be
     walked around (`audit_flow`).
   - **Encounters:** `tideglass_cavern` only — `cave` band 20–24 (Tide), `water` band 21–24
     (Tidecall side-pool), very-rare signature row per §4 above. `tideglass_gallery`
     carries **no encounter zones** (the Hour's room is quiet). On build, add both map ids
     to `CURATED_AREAS` and mirror the final tables into `EXTRA_ENCOUNTERS`
     (`build_species.py`). **#160 itself takes NO encounter row** — `scripted: true`,
     `encounters: []` (the Lunaveil/Keylumen convention, verified).
   - **NPCs / signs:** the netmender swap pair (Pearlmoor, host edit); the three lens
     placements (inert/live pairs); the verse plaque (`sign.tideglass_verse` inert twin
     before its requires are met); `hour_dusk`. **Trainer-free.**
   - **Battle backdrop:** new 240×160 WebP `tideglass_gallery` (pooled teal light on black
     glass) under `public/assets/backgrounds/battle/`, listed on both maps.

---

## 5. Site II — the Hourfold — *Midnight in the deep ice* (North)

**At a glance** — `pale_vault_hourfold` (NEW, ~24×20, cave/ice) · annex off
`pale_vault_glacier`'s Emberward-gated **deep-ice back-folds** (03-north owns the fold
ground; this file adds one warp) · entry: `to_hourfold`, **`requires_ability: emberward`**
+ **`requires_flag: flag:three_mid_snuffer`** (`blocked_ref: npc.hourfold_sealed`) · Hour
fight **lv 48** · first reachable ~lv 40 (post-Frost Gleam) · `dark` map, runs a band
colder and dimmer than the glacier.

1. **Main path**
   1. **The rumour at the Aurora-watch.** The festival's **aurora-watcher** (post
      `gleam:frost`) has noticed the sky behaving oddly over one fold of the deep ice
      (`script.aurorawatcher_hours` → `flag:three_mid_rumour`). The chain's permitted dry
      line, hers:
      > "The aurora bends round that fold like it's queuing. Forty years I've watched the
      > sky. It has never once queued for me."
   2. **Ysolde's snuffer.** Ysolde Frost knows what keeps a vigil there — and what it asks.
      She hands over the **Vigil Snuffer** (key item; `script.ysolde_snuffer`, requires the
      rumour → `flag:three_mid_snuffer`):
      > Ysolde: "You have spent the whole road lighting things. The Still Hour will want to
      > see that you understand the other half of tending."
   3. **The descent (the traversal cost).** Inside the fold, terraced blue ice drops by
      **one-way ledges** (the shipped ledge-hop mechanic). Three tiers, two false lines: a
      wrong drop shunts you to the mouth to re-climb. Aurora-light through the ice is the
      wayfinding (the true line runs *under* the brightest ribbons).
   4. **The Unstruck Toll (the puzzle, inverted).** The bottom shelf holds **three
      vigil-braziers**, burning blue-white — and the Hour will not be seen by their light.
      The aurora overhead names the order (`sign.hourfold_aurora`: *"the ribbon kneels east,
      then over the water-ice, then west"*). Snuff east → centre → west with the Vigil
      Snuffer (flag-chained interacts, inert/live pairs; wrong order: "the flame leans away
      from the snuffer"). For once in the whole game, the player puts lights out — the
      Hollowing's temptation made playable for three tiles, and answered: this dark is
      *kept*, not surrendered.
   5. **The watch witnessed.** With all three out, the far shelf resolves: a vast curled
      disc of midnight-blue glass unrolls into a sentinel. The fight.
2. **Story beats** — the Hollowing's shadow, never their presence: a single weathered
   null-lantern stands at the fold mouth, long dead, half-reclaimed by ice (deco object —
   the engine's `null_lantern`). No script touches it; players who notice understand whom
   midnight has been refusing.
   - **Cinematic staging:** on the last snuff → `silence 1200` (the longest held quiet in
     the game so far) → `narrate: "The dark does not deepen. It straightens, as if relieved
     of a stoop."` → `sting-hour` → `battle-hours` → the op.
3. **Mechanic introductions** — the snuff inversion (interacts that *remove* light), ledge
   wayfinding by aurora, and the escalated cooldown (14).
4. **Optional content**
   - **Fold bed** — sparse `cave` encounters, band 44–48 (deep-ice register: the
     undercroft's Frost families fit) — deliberately a touch above the North curve; the
     fold is a place you return *to*, not through.
   - **One cache** — `[MISSABLE]` off the second tier behind a false ledge line (suggest a
     valuable — Moth-amber — the §5 kit's "nugget" read).
   - **H2 quest** — below.
5. **Don't-miss callouts** — the braziers stay out once snuffed (flags persist): the
   re-climb after a failed catch is short, the cooldown is the real cost. Read the aurora
   before the ledges, not after.

   **Named quests:**
   - **H2 "The Longest Watch"** — giver: the **aurora-watcher** (Pale Vault, post
     `gleam:frost`) · steps: rumour (`flag:three_mid_rumour`) → Ysolde's snuffer
     (`flag:three_mid_snuffer`) → descend the fold, still the toll, witness the watch ·
     reward: the **chance at Noctilune** · maps: `pale_vault_glacier`,
     `pale_vault_hourfold` · `[LATER: Emberward]` (in-region; held by then on the main path).

6. **Validation hooks**
   - **Map id / kind:** `pale_vault_hourfold` · cave (ice) · region `north` · NEW node +
     edge in `graph.ts` (`pale_vault_glacier → pale_vault_hourfold`, via `to_hourfold`,
     `requires_ability: emberward`, bidir). Host edit: the one warp on
     `pale_vault_glacier`'s deep-ice fold (agree the coord with the North writer's deep-ice
     ground) + the aurora-watcher placement pair.
   - **Warps:** `to_hourfold` step_on, `requires_ability: emberward`,
     `requires_flag: flag:three_mid_snuffer`, `blocked_ref: npc.hourfold_sealed` ("The fold
     is shut fast with ice that has opinions about visitors. Something in there is not
     ready to be looked at."). Landing on/beside the return warp; every walkable tile of
     the fold mouth warps (`audit_warps`).
   - **Triggers / flags (opened ⇒ consumed):**
     | Flag | Set by | Consumed by |
     |---|---|---|
     | `flag:three_mid_rumour` | `script.aurorawatcher_hours` | Ysolde's script `requires_flag`; watcher swap pair |
     | `flag:three_mid_snuffer` | `script.ysolde_snuffer` (gives key item `vigil_snuffer`) | `to_hourfold` warp gate; brazier interacts |
     | `flag:three_mid_brazier_a/_b/_c` | `script.three_mid_brazier_*` (ordered chain, inert/live pairs) | next brazier; `_c` reveals the Hour placement (`requires_flag`) |
     | `flag:three_mid_caught` | the op | `hidden_when_flag` on `hour_midnight` |
   - **The op (verbatim):**
     ```ts
     { op: 'legendaryBattle',
       name: 'three_midnight', kin: 161, level: 48,
       caughtFlag: 'flag:three_mid_caught',
       cooldownBattles: 14,
       cooldownRef: 'npc.three_midnight_resting',
       terrain: 'cave' },
     ```
     Staged by `hour_midnight` (sprite `kin_161_overworld`, interact, `requires_flag:
     flag:three_mid_brazier_c`, `hidden_when_flag: flag:three_mid_caught`) on the far
     shelf; the approach is the bottom shelf's single span (un-walk-aroundable).
   - **Ledges:** one-way `ledge` tiles per the shipped CollisionGrid/ledge-hop mechanic;
     `audit_flow` must PASS (the shunt-to-mouth lines are designed loops, not dead ends).
   - **Encounters:** `cave` 44–48; on build → `CURATED_AREAS` + `EXTRA_ENCOUNTERS` mirror.
     #161: `scripted: true`, no rows. **Trainer-free.**
   - **Battle backdrop:** new `hourfold` WebP (aurora ribbons through black ice).

---

## 6. Site III — the Unrisen Stair — *the Dawn that waited* (West)

**At a glance** — `unrisen_stair` (NEW, ~20×26 vertical, ruin) · annex off
`sunken_solarium`'s deepest fold (one host warp; 04-west owns the ruin) · entry:
`to_unrisen`, **`requires_ability: sunsketch`** + **`requires_flag: flag:three_dawn_poured`**
(`blocked_ref: npc.unrisen_sealed`) · Hour fight **lv 55** · chain opens post
`gleam:lunar` (~lv 52, the Spire approach) · the hardest and last of the three, met on
purpose *just before the end*.

1. **Main path**
   1. **Nessa's reading.** After her Gleam, Nessa Cole keeps hearing something through the
      great telescope that isn't a star (`script.nessa_hours` → `flag:three_dawn_rumour`).
      Sincere, not dry — she is the haunted one:
      > Nessa: "Every chart says the morning bell should hang due west of here. There is no
      > morning bell. There has been no morning. And yet three nights running I have heard
      > a bell that hasn't rung — *waiting* makes a sound, you know, if it goes on long
      > enough."
   2. **Lucan's phial.** The keeper of the last warm day holds the only daylight old enough
      to matter: the **First-Light Phial**, drawn the morning before the Long Dusk fell
      (`script.lucan_phial`, requires the rumour → `flag:three_dawn_phial`). The chain's
      permitted dry line, his:
      > "I kept the last warm day for forty years. Apparently somebody kept the last
      > *morning* and never thought to mention it. Theatrical of them. I approve."
   3. **The basin.** At the Solarium's deepest fold, a dry sun-basin before a sealed
      processional stair that once greeted the sunrise. Pour the phial
      (`script.three_dawn_basin` → `flag:three_dawn_poured`); the basin holds one cupful of
      morning, and the first sun-vine on the stair stirs.
   4. **The Bloom Ascent (the puzzle).** The stair climbs in three flights over still black
      water, crossable only by sun-vine. **Sequential bloom:** the basin's light lets you
      bloom vine A; from A's landing you reach the **sun-mirror flower**, which bends the
      pocket of daylight across the water to the far vine (**redirect**, the spine §5
      grammar); vine B opens the east flight to the head terrace. Main-path-simple it is
      not — and it doesn't have to be: nothing required lives here.
   5. **The Hour of the dawn that hasn't come.** On the head terrace, where the first light
      was meant to land, something half-finished stands facing east. It has been facing
      east for years. The fight.
2. **Story beats** — **the climax foreshadow (the point of placing it here).** The staging
   script sets `flag:three_dawn_met` before the op, win or withdraw — consumed by one
   optional Fenn placement at Vesper Crossroads (his C4 counsel ground):
   > Fenn (requires `flag:three_dawn_met`): "So you found the third watch. Still facing
   > east, was it? …Then it has never stopped believing the wheel can turn. Neither have I.
   > Go and prove the pair of us right."
   - **Cinematic staging:** entering the head terrace → `letterbox` + `silence 1200` → a slow
     warm `tint` blooms from the Hour outward (the false dawn — the same warm wash the
     climax will earn for real) → `narrate: "For one held breath, the stair remembers what
     it was for."` → `sting-hour` → `battle-hours` → the op. **This beat must visually rhyme
     with the Keystar relight** — same tint family, a fraction of the strength.
3. **Mechanic introductions** — the Sunsketch puzzle dimension in full (sequential +
   redirect), and the longest cooldown (18) — by now withdrawal genuinely stings.
4. **Optional content**
   - **No encounter zones.** The stair is processional-quiet; wild kin keep a respectful
     distance (the inverse of the Penumbra's refusal — here they *defer*). Pure approach.
   - **One cache** — `[MISSABLE]` a Starglass Shard in a fallen capital off flight two.
   - **H3 quest** — below.
5. **Don't-miss callouts** — come BEFORE the Spire. The encounter is written to make the
   climax land harder; post-climax it still works, but the foreshadow becomes an echo.

   **Named quests:**
   - **H3 "The Unrisen Stair"** — giver: **Nessa Cole** (Nightreach, post `gleam:lunar`) ·
     steps: rumour (`flag:three_dawn_rumour`) → Lucan's phial (`flag:three_dawn_phial`;
     the hub wheel makes the Solarium leg a short walk — collinear by `hub_unlocked`-era
     geometry) → pour the basin (`flag:three_dawn_poured`) → climb the bloom route ·
     reward: the **chance at Erstmorn** · maps: `nightreach_observatory`,
     `sunken_solarium`, `unrisen_stair` · `[LATER: Sunsketch]` (held since the Solarium).

6. **Validation hooks**
   - **Map id / kind:** `unrisen_stair` · ruin (kind `route`/interior per the Solarium's
     register) · region `west` · NEW node + edge (`sunken_solarium → unrisen_stair`, via
     `to_unrisen`, `requires_ability: sunsketch`, bidir). Host edits: the one warp + basin
     trigger on `sunken_solarium` (coords agreed with the West writer), Nessa/Lucan script
     placements (swap pairs) on their shipped maps.
   - **Warps:** `to_unrisen` step_on, `requires_ability: sunsketch`, `requires_flag:
     flag:three_dawn_poured`, `blocked_ref: npc.unrisen_sealed` ("A stair behind the seal,
     climbing toward nothing the sky currently offers. The basin before it is dry.").
   - **Triggers / flags (opened ⇒ consumed):**
     | Flag | Set by | Consumed by |
     |---|---|---|
     | `flag:three_dawn_rumour` | `script.nessa_hours` | Lucan's script `requires_flag`; Nessa swap pair |
     | `flag:three_dawn_phial` | `script.lucan_phial` (gives key item `first_light_phial`) | basin trigger `requires_flag` |
     | `flag:three_dawn_poured` | `script.three_dawn_basin` | `to_unrisen` warp gate; bloom gate A `requires_flag` |
     | `flag:three_dawn_bloom_a/_b` | bloom interacts (each an `AbilityGate make_passable` chain step keyed `sunsketch` + the previous flag; the mirror-flower interact sets `_b`) | next flight's gate; `_b` → head terrace |
     | `flag:three_dawn_met` | `script.three_dawn_battle` (before the op, win or withdraw) | Fenn's optional Crossroads line |
     | `flag:three_dawn_caught` | the op | `hidden_when_flag` on `hour_dawn` |
   - **The op (verbatim):**
     ```ts
     { op: 'legendaryBattle',
       name: 'three_dawn', kin: 162, level: 55,
       caughtFlag: 'flag:three_dawn_caught',
       cooldownBattles: 18,
       cooldownRef: 'npc.three_dawn_resting' },
     ```
     *(No `terrain` — the stair is no encounter ground; conditional charges read plain
     here, which is intended: the last Hour offers no shortcuts.)* Staged by `hour_dawn`
     (sprite `kin_162_overworld`, interact, `hidden_when_flag: flag:three_dawn_caught`) at
     the head terrace's centre; the terrace mouth is a single bloomed span
     (un-walk-aroundable).
   - **Encounters:** none. #162: `scripted: true`, no rows. **Trainer-free.**
   - **Battle backdrop:** new `unrisen_stair` WebP (a pale processional stair against
     near-dawn pallor — the warmest backdrop in the main game, a half-shade short of
     Dawnstead's).

---

## 7. Withdrawal — the cooldowns and the resting lines

The cost of a miss is **battles WON**, not time — the player goes back out into the world
and earns the return. Escalation: **Dusk 10 · Midnight 14 · Dawn 18.** The hint plays from
the staging trigger via `cooldownRef`; `{remaining}` is replaced by the engine with the
victories still owed. Ache register — a hint, never a nag (`content/dialogue.ts`,
verbatim):

```ts
'npc.three_dusk_resting': [
  { text: 'The lenses hold your own lamp-light and nothing else. The Dusk Hour has folded itself back into the seam between the days — win {remaining} more battles, and the glass may warm to you again.' },
],
'npc.three_midnight_resting': [
  { text: 'The fold is only ice and aurora tonight. Midnight has kept its watch longer than anyone alive; it can outlast you without noticing — {remaining} battles won, and it may consent to be witnessed again.' },
],
'npc.three_dawn_resting': [
  { text: 'The basin stands dry and the stair unrisen. The Hour that has waited years for its morning can wait a little longer than you — {remaining} more battles won, and it may risk believing again.' },
],
```

---

## 8. Pipeline notes — how #160–#162 are appended (the verified #152–#159 path)

The trio takes the **species-pipeline lane alone** — one package touching only
`docs/mechanics/concepts/selected.json`, `tools/balance/build_species.py`, the generated
data, and the regenerated docs. Maps/scripts/dialogue (everything above) follow as separate
content packages against this spec.

1. **Append three concepts to `docs/mechanics/concepts/selected.json`** — the exact path
   Pharolux/Corolion/Dawnregent took (`X-*` concept ids, `dex_id` continuing the appended
   range; **later ids never renumber 1–151**): `X-GLOAMBER` → `dex_id: 160`,
   `X-NOCTILUNE` → 161, `X-ERSTMORN` → 162. Each entry: `tier: "E"`,
   `rarity: "very_rare"`, single-stage `line` (`stage: 1`, `kindles_into: null` — mirror
   Lunaveil's shape), `region` south/north/west respectively, roles **Special Tank /
   Physical Wall / Utility / Speedster**, and the §2 dossier text in
   `concept`/`visual`/`hook`/`size_cm`/`weight_kg`. `tier E + very_rare` ⇒ the generator
   sets **`scripted: true` and `encounters: []` automatically** (verified against
   Lunaveil/Keylumen/Dawnbrael) — no encounter wiring in the species package.
2. **No `gen_moves.py` change.** All three kits draw from the existing 125-move pool; **no
   new moves, no `SIGNATURE_MOVES` rows** (the signature-exclusion invariant in
   `autobuild.mjs`/`chart_check.mjs` is untouched — the "signature feel" is rare *combos*,
   per the dossiers).
3. **`build_species.py` CANON overrides** (the Vulpyre/Cloverkit worked pattern): pin
   `ability`/`hidden_ability` for **gloamber** (`nightfall`/`emberheart`) and **noctilune**
   (`mirrorlight`/`nightsight`) — Erstmorn matches the Solar-E generator defaults
   (`daybringer`/`sunsoak`) and needs no ability override — plus the §2 dex
   entries/categories/sizes for all three. To pin the **as-met kits**, extend the CANON
   apply with an optional `levelup` key (honoured exactly like the existing `signature`
   insertion — a few lines in the same style) carrying the §2 learnset rows; otherwise the
   deterministic generator ladder is acceptable and the staged kit note in each site spec
   should be relaxed to "the four most recent levelup moves at the staging level". Stats
   need **no** override — the §2 lines are the generator's own output for these names.
4. **Rebuild + validate:** `python3 tools/balance/build_species.py` →
   `python3 tools/balance/gen_docs.py` (the dex doc gains the three), then ALL gates:
   `node tools/balance/validate.mjs` (schema, E-band EPS, catchRate clamp — 24 is the
   E/very-rare clamp output, matching the register kin) · `node tools/balance/simulate.mjs`
   (exit-codes; if an Hour flags as an outlier, tune the kit before waiving anything) ·
   `node tools/balance/chart_check.mjs` (unchanged but cheap) ·
   `node tools/balance/progression.mjs` (no prices/payouts/trainers change — sites are
   trainer-free — but the model must still PASS untouched).
5. **Keep the mirrors in sync:** no `moves.json`/chart edits ⇒ no `03-moves.md`/
   `01-type-system.md` work. `dex.md` regen covers the roster docs. CLAUDE.md's "159 kin"
   canon line becomes 162 **in the species package's commit** (per "Keeping docs current").
6. **Assets:** `./venv/bin/python tools/assets/gen_creature.py 160` (then 161, 162) renders
   the 5 standard views from each species `art` block (§2 blocks are written to drive it;
   `--provider openai` if Google is spend-capped), then
   `./venv/bin/python tools/assets/pack_creatures.py`. Sprites lazy-load by dex id
   (`CreatureSprites`), so battle/party/dex views need **zero engine edits**; the
   placeholder path covers any gap until packed.
7. **Map packages (separate, against this spec):** `build-map` skill per annex
   (`tideglass_cavern`+`tideglass_gallery`, `pale_vault_hourfold`, `unrisen_stair`);
   register nodes/edges in `graph.ts` + `maps.ts`; full `finalize()` audit stack
   (`render_map` · `validate_map` · `audit_warps` · `audit_flow`) and
   `audit_region` after the graph edits; on Tideglass's build, add its map ids to
   `CURATED_AREAS` and mirror the bed into `EXTRA_ENCOUNTERS`.

---

## 9. Non-overlap with the Starfall Vigils (checked, binding)

Verified against [`06-postgame.md`](./06-postgame.md)'s Vigils section — **no collisions**:

- **Sites disjoint:** Hours at `tideglass_gallery` (off Dimglass II) / `pale_vault_hourfold`
  (off the glacier) / `unrisen_stair` (off the Solarium ruin). Vigils at the Tinderwick
  bluff / Spore Grotto / Thunderroost / `sunvault_climb_ii` / `coldfog_marches_ii` / the
  Spire summit. No shared host edit, no shared annex.
- **Bands disjoint:** 38 / 48 / 55 (main game) vs the Vigils' 58–70 (post-`dawn`).
- **Kin disjoint:** #160–#162 are NEW; the Vigils' register ledger places only the existing
  E/F singles (#33–#151) and stays untouched. Starwell's "near-legendary" (Central
  writer's) is likewise untouched.
- **Rewards disjoint:** the Hours grant no charms, charts, or wicks — the catch is the
  entire prize. The Vigils' one-per-game reward table is unaffected.
- **Flags disjoint:** `flag:three_*` vs `flag:vigil_*`/`flag:starfall_*`.
- **Register disjoint:** main-game **awe + ache** (the night's own keepers, met in the
  dark) vs the Vigils' post-dawn wonder and trial-circuit warmth.
- **Mechanic disjoint:** the Hours are the game's `legendaryBattle`-op debut (wild
  set-piece + cooldown); the Vigils are six-kin trainer gauntlets. Dawnbrael's summit
  catch remains the Vigils' own set-piece.

## 10. Originality audit (per `VISION.md`)

The Hours are a triad of **personified watches of the night** — dusk, midnight, and a dawn
that never came — original to PixelKin's Long Dusk cosmology (story-bible §2's "cycle of
dusk and dawn" made into kin). *Gloamber, Noctilune, Erstmorn*, the *Hourfold*, the
*Unrisen Stair*, the *Lampwright's Relay*, the *Unstruck Toll*, the *First-Light Phial* and
the *Vigil Snuffer* are all coined here. Silhouettes (an ember-locket lynx, a star-paned
glass pangolin-sentinel, an unfinished hare of light) are described by mood and form only
and echo no other franchise's beasts, birds, or trio structure; the triad's logic (the
jammed wheel of the day) is the game's own. Canon vocabulary throughout; describe by genre,
never by brand.
