# PixelKin Walkthrough — 06 · Post-game (after `flag:dawn`)

> Region file under the [spine](./README.md). Read its §0 rules, §2 flag strings, §3 arcs
> (incl. Arc A's Wren resolution and Arc D's celestial-calendar payoff), §4 curve (the
> lv55–65 rematch band), §7 template, §8 the day-forms proposal, and §10 voice first — they
> are binding here. Areas follow the §7 template exactly. Canon vocabulary only: **kin,
> Lumenary, Lampwarden, Gleam, Lantern Gift, vesperlamp, kindling, the Hollowing.**

## Region header

**The morning after the long night.** This is the only region played in true daylight — the
visual and emotional payoff of the whole Wayfaring. The Keystar is relit, the Penumbra is
gone, and Vesperholm has woken into its first dawn in years. Post-game delivers six things:
the epilogue town of **Dawnstead** (Tinderwick reborn in open sky, with the lullaby returned
in triumphant major); a fresh collecting hook in the **day-forms** of early kin that the
relit sky now wakes; the **late-backtrack landmarks** that only Starreach + dawn make worth a
return (**Crystoll Vault**, **Starwell**); the **Radiant-Lamplight backtracks** — the early
dark areas, re-walked with the vesperlamp at its brightest, finally giving up the optional
content that sat beyond your old reach (spine §5); the **gentle arc resolutions** — Wren at
peace in daylight (A6), and Warden Còr's quiet aftermath; and **the Starfall Vigils** — the
endgame challenge chain (the major section near the end of this file): five riddle-led trial
sites across the relit world, the game's first full-six-kin fights, and one ultimate trial at
the summit. No new Lantern Gifts: all six are already earned, so post-game is *collecting,
rematches, trials, and resolution*, not traversal.

- **Entry state:** the climax is done. Player at **~lv55+**, party of bonded kin, holding
  **all six Lantern Gifts** (Tidecall, Glimmerstep, Updraft Kite, Emberward, Sunsketch,
  Starreach), all eight Gleams, **`flag:keystar_relit`** and **`flag:dawn`** set, the
  vesperlamp at its brightest, and **Wren at your side** from the Spire. Reached via
  **`umbral_spire → dawnstead`** (`to_dawn`, `requires_flag: flag:dawn`).
- **What post-game gates open:** `flag:dawn` shows the `dawnstead` node and the
  `umbral_spire → dawnstead` road; it also keys the **day-form encounter swaps** mapwide.
  **Starreach** (held since Nightreach) is what makes the two `[LATER]`-tagged Crown
  landmarks — **Crystoll Vault** and **Starwell** — finally reachable.
- **Arc beats delivered:** **A6** (Wren resolved — Dawnstead; optional rematch) ·
  **Còr's resolution payoff** (the gentle aftermath — never a punished villain) ·
  **Arc D full payoff** (the dusk→dawn key arc resolves; true daylight; the vesperlamp at
  its brightest) · optional **Arc E capstone** (a region-wide *first-dawn* festival).
- **Arc-D lighting note:** every prior region opened a half-shade warmer than the last, from
  South's deep blue hour to West's near-dawn pallor. **Dawnstead breaks the scale: full
  `fire`-orange + `bone` daylight, open sky, warm shadows.** This is the only map where the
  lamp is a *keepsake*, not a necessity — the light is in the sky now. The bittersweet note
  the whole game has been tuning toward lands here: the cycle has resumed, which means **dusk
  will come again — and that is exactly the point.**
- **Cinematic staging (PLANNED — build from South per [`cinematics.md`](../cinematics.md) / §0.4).**
  Post-game is the **quiet exhale** after the climax — almost no spectacle, all warmth and faces.
  The whole region is the festival (a region-wide *first-dawn* `gleam-emotional` reprise in full
  major as the daytime bed). **A6 Wren** at peace in daylight: his steady/smiling **portrait**, an
  optional friendly rematch with none of the old edge. **Còr's resolution** is the toolkit's
  gentlest beat — Còr tending a single lamp off to one side on his **portrait** (grief eased, never
  punished); a short, unhurried, low-music exchange, a touch of warm `tint`. **Fenn** at peace,
  narrative only. The closing note (the cycle resumes; dusk will return) should land on a held beat
  — `narrate` over the open daylit sky, the bittersweet major chord — explicitly rhyming with the
  opening cold open so the game bookends. Assets owed: daytime/daylight Dawnstead backdrop + bed,
  Còr's "at peace" portrait expression, reuse of existing portraits.

---

### Dawnstead — *Tinderwick reborn in the first true daylight in years*

**At a glance** — `dawnstead` · town · south (near Tinderwick) · entry: in from `umbral_spire`
via `to_dawn` (`requires_flag: flag:dawn`); exit: same road back to the Spire / hub network ·
gate: **post-game (`flag:dawn`)** · Gleam: none (all eight held) · rec. level: 55–65.

1. **Main path** (a town to *walk*, not a route to clear — the victory lap):
   1. **Arrive into daylight.** Step out of the Spire road onto open, sunlit ground — the
      first scripted beat is simply the sky: warm shadows, blue-and-gold instead of blue
      hour, the lullaby swelling into its full major reprise. Let the player stand in it.
   2. **Recognise the town.** Dawnstead is Tinderwick's silhouette flooded with daylight —
      same cottage rooflines, same dock, now open-skied. The "is this *home*?" beat: it is,
      and it isn't, because the dark has lifted.
   3. **Find Fenn on the front.** Star-tender Fenn is here, no longer hurrying you anywhere —
      the mentor's arc settles into peace. (Narrative only; no gift, no flag owed here.)
   4. **Meet Wren in the sun (A6).** Wren is waiting by the water, at peace — the warm coda
      to the rival-friend arc. Talk first; the **optional rematch** is offered, not forced.
   5. **Find Còr tending a lamp (resolution payoff).** Quiet, off to one side — Còr, offered
      a place among the star-tenders again, is gently keeping a single lamp lit. Grief eased,
      not defeated. A short, unhurried exchange; never gloating, never punished.
   6. **Step into the sunlit verge — the day-forms.** The town's grass band, now in daylight,
      runs the **day-form encounter table** (see the next section): the same early kin you
      started with, woken bright by the relit sky. The fresh collecting hook starts here.
   7. **Optional first-dawn festival (Arc E capstone).** If staged, the whole town turns out —
      a region-wide *first-dawn* festival as the capstone to the eight town festivals: the
      thesis of "belonging, not conquest," now in daylight.

2. **Story beats**
   - **A6 — Wren resolved.** The competitive edge has softened into friendship; the moral
     question they carried is answered by the daylight around them.
     > Wren: "I spent the whole Wayfaring asking if the Hollowing had a point. Turns out they
     > did — and so did the dawn. Both true. Funny how that works." *(beat)* "One more battle?
     > For old times. Loser buys the lanterns."
   - **Còr's resolution payoff.** The villain undone, not destroyed — quietly returned to the
     work he once loved. Never cartoonish; grief eased.
     > Còr: "I wanted to spare everyone the dusk. I had forgotten that the lamp is for the
     > dark — not against it." *(tends the flame)* "It will fall again, you know. The night.
     > I find I no longer mind. I'll be here to light it."
   - **Arc D payoff — the dawn itself.** The lighting *is* the beat; let the reprise carry it.
     > Fenn: "First true morning in years. Don't waste it asking whether it'll last — it
     > won't. That's the bargain. Dusk for dawn, dawn for dusk. We tend the turning, that's
     > all." *(quiet)* "You did well, apprentice. Go and look at your sky."

3. **Mechanic introductions** — none new (no Gift, no Gleam). What's new is **day-form
   collecting** (the relit-sky encounter swap; below) and **rematches** at the lv55–65 band
   (Wren here; Lampwardens across the eight towns — spine §4).

4. **Optional content**
   - **Wren rematch** — `[MUST-DO]` the warm A6 coda; a lv55–65 friendly battle. Re-runnable
     flavour, no progression gate.
   - **Còr at the lamp** — `[MISSABLE]` easy to walk past if the player makes a beeline for
     the verge; it is the single most important resolution beat — flag it for the player.
   - **First-dawn festival** — `[MISSABLE]` the Arc E capstone set-piece; a flag-gated NPC
     swap + cutscene, not on any critical path.
   - **Day-form starter-line variant** — `[MISSABLE]` the sun-bright **Wickmoth** day-form
     (atlas card 14) is the signature catch that announces the whole day-form hook.

   **Named quests** (spine §5 kit; the post-game slate):
   - **P1 "First-Dawn Letters"** — giver: the **Waykeeper** (his daylight round) · steps:
     carry first-dawn letters out along the spokes — to Wren, to Fenn, and to the eight
     wardens' towns (each recipient a one-line daylight reaction; deliverable in any
     order, each its own boolean flag `flag:q_post_letter_*`) · reward: the Waykeeper's
     thanks + a keepsake stamp per quadrant · maps: every spoke town · `[MISSABLE]` —
     the Round re-used as the post-game's victory lap.
   - **P2 "A Wick for Còr"** — giver: **Fenn** · steps: take a wick **from the Tinderwick
     Beacon's lantern room** → carry it to **Còr at his lamp** · flags: `flag:q_post_wick`
     → `flag:q_post_wick_given` · reward: Còr's last line — and his lamp burning a shade
     warmer thereafter (deco swap) · maps: `tinderwick_beacon_top`, `dawnstead` ·
     `[MISSABLE]` — the game's first earned landmark closes its last arc.
   - **P3 "The Day-form Survey"** — giver: **Fenn** · steps: show him three caught
     day-forms (party checks via dialogue branches) · flags: `flag:q_post_survey(_done)` ·
     reward: a **Radiant-tier Lamplight tease** + his field-journal page · maps:
     `dawnstead` + the relit valleys · `[MISSABLE]`. *Counter note (spine §8): wants
     "3 of 3" — boolean fallback: Fenn asks for one named day-form at a time.*
   - *(Also cross-ref: **X1 "The Caretaker's Lamp"** (04-west) pays off here — with
     `flag:dawn` set, the caretaker's numbed kin is AWAKE at her side in Hushfrost II
     (NPC swap), the quietest echo of the whole B arc.)*

5. **Don't-miss callouts**
   - **Just stand in the daylight first.** The single payoff the game has spent the whole
     dusk earning — don't rush past the sky into the menus.
   - **Talk to Còr before anything else.** The resolution lands only if the player sees the
     gentle aftermath; it's the moral close of Arc B.
   - **Catch a day-form before you leave** — it seeds the post-`dawn` collecting loop that
     sends the player back out across the relit valleys.

6. **Validation hooks** (against built `dawnstead.json`)
   - **Map id / kind:** `dawnstead` · town · region `south`. Node carries
     **`unlocked_by_flag: flag:dawn`** (`graph.ts:116`) — must not render before dawn.
   - **Entry/exit:** in from `umbral_spire` via `to_dawn`, **`requires_flag: flag:dawn`**,
     bidir (`graph.ts:172`); the return road feeds back to the Spire / hub network. Agree the
     land-in coord with the Central writer's `umbral_spire` exit.
   - **Triggers / flags:** no new progression flags set here (`flag:dawn` is already set at the
     climax by the Central writer). A6 Wren rematch = trainer-battle cutscene with
     `reward_flags` bookkeeping only (re-runnable, no gate). Còr-resolution + first-dawn
     festival = `script`/`cutscene` triggers, flag-gated on `flag:dawn`, `once: true` where a
     one-shot reading is wanted (festival may re-fire as ambient).
   - **Encounters:** `tall_grass` (sunlit verge) running the **day-form table keyed on
     `flag:dawn`** — see the next section's hooks. Element-matched to Tinderwick's roster
     (Ember / Light), now in day-form. Level band 55–65 (§4 post-game).
   - **NPCs / Lumenary / festival:** Star-tender Fenn (peace, narrative only); **Wren** (A6,
     rematch trainer entry); **Warden Còr** (resolution payoff, tending a lamp). No Lumenary /
     no Gleam in Dawnstead. Dialogue/script refs (suggested): `npc.fenn_dawnstead`,
     `trainer.wren_rematch`, `cutscene.cor_resolution`, `cutscene.dawnstead_first_dawn`.

---

### The post-dawn world & day-forms — *the relit sky wakes new kin*

This is the **Arc D / celestial-calendar payoff** as a mapwide collecting layer. It is not a
single map: with `flag:dawn` set, the **encounter tables of the relit valleys change**, and
previously dark folds of the world brighten. Write it as the **permanent post-dawn swap**, not
a clock.

> **Scope (spine §8 ⚠️ PARTIAL).** Permanent post-dawn day-form table swaps are expressible
> **now** via flag-gated `EncounterZone`s keyed on **`flag:dawn`** (atlas §4: "the celestial
> calendar shifts tables as constellations relight"). **True day/night *cycling* is a
> post-MVP proposal** — do **not** author a time-of-day clock. A day-form is a **permanent
> alternate encounter entry** that becomes the active table once `flag:dawn` is set; it does
> not toggle back.

1. **Main path** (how the player engages it):
   1. **Notice the swap at Dawnstead.** The first day-form (sun-bright Wickmoth) appears in
      the sunlit verge — the hook is introduced where the daylight is.
   2. **Backtrack the relit valleys.** With the fast-travel hub wide open (`hub_unlocked`) and
      the Penumbra gone, the player re-walks earlier regions to find day-forms of their early
      kin under the now-warmer skies. The collecting loop *is* the post-game content.
   3. **Brightened dark folds.** Previously gloomy interiors and blighted edges (e.g. the once
      sickly Coldfog Marches) read warmer post-dawn; Light-typed kin, which thinned in drained
      areas (atlas §4), **bloom back** in relit ones — a visible, catchable sign of the win.
      The same flag drives the small human payoffs: **X1's caretaker** (Hushfrost II, 04-west)
      now sits beside her kin AWAKE (`flag:dawn` NPC swap) — author every region's post-dawn
      swap candidates as `flag:dawn`-keyed pairs like hers.

2. **Story beats** — Arc D's quiet aftermath, told through ecology rather than cutscene: the
   world the player healed is now *full of light to collect*. No new arc beats land here; this
   is the celestial calendar paying off as gameplay.
   > Field sign (Tinderwick verge, post-dawn): "The moths came out gold this morning. Nobody's
   > seen the like. Catch one — they won't keep; nothing does. That's why you catch it."

3. **Mechanic introductions** — **day-form collecting**: the same kin, a sun-woken variant,
   as a fresh dex layer. No engine change — pure flag-gated table data.

4. **Optional content**
   - **Day-form of the starter line / early kin** — `[MISSABLE]` the headline variants; the
     sun-bright Wickmoth is the announced example (atlas card 14).
   - **Light-kin re-bloom in former drained zones** — `[MISSABLE]` Coldfog Marches and other
     once-blighted edges now carry Light kin again; a satisfying contrast catch.

5. **Don't-miss callouts**
   - **The day-forms are the post-game's spine.** They're why a completionist re-walks the
     whole relit map after the credits — point the player at them from Dawnstead.

6. **Validation hooks**
   - **No new map.** Day-forms are **alternate `EncounterZone` entries on existing maps**
     (`tinderwick`, `dimglass_coast`, the relit valleys), **gated on `flag:dawn`**: when the
     flag is set, the day-form entry becomes the active table for that zone (permanent swap,
     no toggle). Reference: atlas §4 + spine §8 (⚠️ PARTIAL — permanent swap only, **no
     day/night cycle clock**).
   - **Element match:** each day-form matches its area's light (Ember/Light day-forms at
     Tinderwick/Dawnstead, etc.) per atlas §4 cohesion.
   - **Level band:** post-dawn encounters sit in the **55–65** band (§4) so the relit map is
     level-appropriate for a post-game party — no cliffs against earlier-region geometry.
   - **Light re-bloom:** raise Light-kin weights in formerly drained zones (e.g.
     `coldfog_marches_i/ii`) on `flag:dawn` — the inverse of the atlas §4 "Light kin thin in
     blighted areas" rule.

---

### Post-Crown collecting (Starreach backtracks) — *the late landmarks, finally worth the return*

With **Starreach** earned at Nightreach and the Crown complete, the two `[LATER]`-tagged
landmarks from earlier regions are now reachable. They were teased as backtrack bait the whole
game; post-game (or any time after Starreach) is when you cash them in. Both are
completionist destinations, reached through the now-open hub.

Both are **owned and fully spec'd on their home maps** — this section is the *journey* beat
(when you cash them in), not a second home for the data. Don't re-author their At-a-glance /
validation hooks here; cross-check them where they live:

- **Crystoll Vault** — a crystal-lit deep vault off the eastern mine. Reach `cinderhead_deep`
  (via the `flag:shortcut_mine` hub re-link, or the Glimmerstep mine route), then cross the
  **Starreach** void in. Reward: a rare **Stone/Light** kin. `[MUST-DO]` for completionists —
  the `[LATER]` teased back in East closes here. **Node + hooks owned by
  [`02-east.md`](./02-east.md)** (Cinderhead Deep; `cinderhead_deep → crystoll_vault`,
  `requires_ability: starreach`, `graph.ts:148`).
- **Starwell** — a near-legendary kin in the heart of the parted Penumbra. Through the open hub
  to `penumbra_ring`, then cross the final **Starreach** voids in; the game's standout optional
  catch. `[MUST-DO]` — the `[LATER]` teased from the West/endgame closes here. **Node + hooks
  owned by [`05-central-endgame.md`](./05-central-endgame.md)** (Penumbra Ring;
  `penumbra_ring → starwell`, `requires_ability: starreach`, `graph.ts:155`).

Neither is a soft-lock: Starreach is earned at Nightreach (and the Penumbra parts on
`hub_unlocked`), both well before either edge is crossed (spine §2). Keep any flavour in the
bittersweet-warm register; encounter band 55–65 (§4 post-game).

> **Other `[LATER]` content gated by Starreach + dawn.** Per the spine §5 Starreach row, the
> *only* two map landmarks that wait specifically on **Starreach** are **Crystoll Vault** and
> **Starwell** (both above). Every other spur/landmark in the world opens on an *earlier* Gift
> (Tidecall/Glimmerstep/Updraft Kite/Emberward/Sunsketch) and so is already cleared by entry
> here — there is no further Starreach-gated map content to backtrack for. What the rest of the
> post-game world offers is the **day-form re-walk** (previous section), not new gated rooms.

---

### Radiant-Lamplight backtracks — *the early dark, finally fully seen*

The day-form re-walk isn't the *only* reason to revisit. By post-game the vesperlamp sits at
**Radiant** (spine §5, eight Gleams) — its reveal-radius is at its widest — so the **dark areas
you first crept through at Ember-glow/Warmlight now give up the optional content that sat beyond
your old reach**. This is the deliberate counterpart to the front-loaded Lantern Gifts: the
discrete Gifts reopened the early map *as keys*; **Radiant Lamplight reopens it as sight**, and
because it's spread across every dark area, the late-game discovery thrill is everywhere, not
bottlenecked behind the two Starreach spurs.

1. **Main path** — none; this is pure optional collecting, available any time the lamp is bright
   enough but headlined here as the completionist's post-credits sweep.
2. **Mechanic** — **Lamplight (Radiant)**, the continuous axis from spine §5. *Additive, never
   blocking* — every one of these reveals is optional; nothing required was ever hidden.
3. **Where to return (each a Lamplight reveal, all `[MISSABLE]` — ALL FOUR BUILT 2026-06 as
   `flag:lamplight_<tier>`-gated caches: Tideglass (4,2) Starlight · Glowmoss Deep (12,23)
   Brightlight · Cinderhead Deep B2F (19,11) Starlight · Hushfrost I (7,8) Radiant):**
   - **Tideglass Cavern** (South) — first seen at Warmlight; at **Starlight+** a deeper nook and
     a hidden item resolve out of the dark.
   - **Glowmoss Deep / Spore Grotto** (East) — **Brightlight+** reveals glow-shadowed side-cells
     off the main glowmoss run.
   - **Cinderhead Mine / Deep** (East) — **Starlight/Radiant** lights the far galleries and a
     late alcove the cramped early visit kept hidden.
   - **Hushfrost Pass** (West) — **Radiant** picks out snow-hollow caches along the canyon walls.
   - *(Coldfog Marches resists Lamplight — its drained dark never brightens; its secrets stay on
     Emberward/Glimmerstep, not brightness. Spine §5 caveat.)*
4. **Validation hooks** — these are **optional `EncounterZone`/`EventTrigger` rewards on existing
   dark maps**, surfaced by a `reveal_at_tier` marker (spine §5 render feature), **not** new
   warps or flags. They must sit **off** the lit main route (which stays visible at any tier), so
   no required path ever depends on brightness. Reward band 55–65 (§4).

> **Tone.** Frame each reveal in the bittersweet-warm register: the lamp you carried through the
> long night is bright enough now to show you what the dark was always holding — *you didn't beat
> the dark, you out-shone it.*

---

### Arc resolutions (Wren, Còr) — *the warm coda*

Both human arcs close in Dawnstead, in daylight, in the same gentle register. (Staged inside
the Dawnstead section's main path; gathered here so the arc bookkeeping is in one place.)

1. **Main path** — encountered as the player crosses Dawnstead: Wren by the water (A6), Còr
   tending a lamp off to one side (resolution payoff). Neither is a wall; both are warmth.
2. **Story beats**
   - **A6 — Wren resolved (Arc A close).** At peace in daylight; the moral question answered;
     an **optional rematch** as the friendly capstone (lv55–65 per §4). The rival-friend
     becomes, simply, the friend.
   - **Còr's resolution payoff (Arc B close).** Offered a place among the star-tenders again
     at the climax, Còr is shown in gentle aftermath — quietly tending a lamp at Dawnstead (or
     the observatory). **Never a punished villain:** grief eased, not defeated. He understands,
     now, that the lamp is *for* the dark, not against it.
   - **(Arc C undertone.)** Fenn, who shared a star-tender past with Còr (spine §8 canon
     extension), is at peace too — the mentor's quiet hope vindicated without triumphalism.
3. **Mechanic introductions** — the **Wren rematch** (rematch curve, §4); no new systems.
4. **Optional content**
   - **Wren rematch** — `[MUST-DO]` the A6 capstone battle.
   - **Còr exchange** — `[MISSABLE]` but the emotional close of the whole antagonist arc;
     surface it to the player.
5. **Don't-miss callouts** — **see Còr before you leave Dawnstead** — the resolution is the
   point of the post-game's quieter half; missing it cheapens the climax's mercy.
6. **Validation hooks**
   - **Wren A6:** rematch trainer entry (`trainer.wren_rematch`) at lv55–65; trainer-battle
     cutscene with `reward_flags` bookkeeping only — re-runnable, **no progression gate**.
   - **Còr resolution:** `cutscene.cor_resolution` `script`/`cutscene` trigger on `dawnstead`,
     **flag-gated on `flag:dawn`**, `once: true`. Sets **no new flag** (resolution is narrative;
     `flag:keystar_relit` + `flag:dawn` already carry the state).
   - **Tone gate (spine §10):** copy-edit pass — Còr is never gloated over or imprisoned;
     canon vocabulary only; bittersweet-warm, never grim.

---

## THE STARFALL VIGILS — *the endgame challenge chain* (`flag:starfall_begun` → `flag:starfall_crown`)

**The new sky settles — and sheds.** With the Skyweave relit and the cycle resumed, the first
**starfall in living memory** crosses Vesperholm: star-shards shaken loose as the woken
constellations settle into their seats. Each fall lands somewhere out in the relit world, and
where a shard rests, the apex kin of that quadrant gather to it — and one of the **Vigilants**,
the generation of keepers who tended the lamps *before* the Long Dusk, comes out of retirement
to stand vigil over it. The chain: a **star-reading** (a riddle-clue in canon voice) names where
a shard fell → the named site **opens** (a small sealed annex off a shipped map) → inside wait
**apex-band wilds**, a **legendary-register catch**, and a **Vigilant trial** — the game's first
**full six-kin, smart-AI fights** — → keeping the vigil yields the shard, a one-per-game reward,
and the *next* reading. Five shards held → the **ultimate trial** unseals at the Umbral Spire's
summit: a back-to-back gauntlet ending in the hardest fight in the game — **Star-tender Fenn at
full strength** — and the catch of **Dawnbrael**, the first-morning kin.

**Why it exists (the design intent).** The rematch band (lv55–65) is post-game's on-ramp; the
Vigils are its **summit**: bands climb 58–60 → 66–68 → the summit at 68–70, so a player genuinely
levels *into* the chain (the apex-band wilds at each site are the designed grind bed — at
`bst·level/20`, one register kin pays ~1,600+ XP, and **catches pay like knock-outs**). The
readings re-tour the whole relit world (the §5 "old ground reopened" philosophy, one site per
quadrant + the outer marches, walked in the journey's original clockwise order), and every reward
is one-per-game and *worth the climb*. **Tone: post-dawn wonder, not grimness** — the trials are
a celebration of mastery, the old generation coming out into the morning to see what the long
night made. The readings and Vigilant lines are the one place post-game humour may glint
(British-dry, ~1 line in 6); Fenn's finale is **sincere throughout**.

> **Engine note (binding — everything below is existing data, no new mechanics).** Verified
> against the built engine: `TrainerDef.party` is an unbounded `TrainerKin[]` (Ysolde already
> ships five — **six-kin teams are a pure data edit**); consecutive battles are **sequential
> `battle` ops in one script** (`CutsceneRunner` runs them in order; **a loss aborts the rest of
> the script** — the standing convention, so rewards/flags authored *after* the last battle can
> never half-grant, and a blackout re-runs the gauntlet from its trigger); the `heal` op covers
> the between-bout trim; conditional charges support `any_status` and `first_turn`
> (`ChargeCondition` — there is **no level-based condition kind**, so charm designs below stay
> inside the existing kinds); `giveItem`/`giveMoney`/`setFlag` cover every reward. The whole
> chain is flags + warps + NPC/object swap pairs + `EventTrigger`s + trainer/item/script entries.

### How the chain runs — readings, sites, shards

1. **The opening.** With `flag:dawn` held, a witness NPC in Dawnstead points the player to
   Nightreach, where **Watcher Oriel** — *the junior watcher of X3/R5, promoted* (canon name
   locked here, the spine-§8 pattern) — reads the first fall from the telescope terrace:
   `cutscene.starfall_begins` sets **`flag:starfall_begun`** + **`flag:vigil_reading_1`**.
2. **Readings open sites.** Each Vigil site is a small new annex map whose host-map warp carries
   `requires_flag: flag:vigil_reading_<n>` (+ a `blocked_ref` tease line before the reading is
   held — the scar of starlight is *visible* post-dawn, sealed until read). Holding a reading is
   the only key; no Gift gates anything the player doesn't already hold.
3. **Sites pay three ways.** Apex-band wilds (the grind bed), a **legendary-register single** as
   the very-rare catch (the register ledger below), and the **Vigilant trial** — an unavoidable
   step_on trainer beat across the shard approach: full six kin, `ai:'smart'`, the new
   **`vigilant`** payout class.
4. **Keeping a vigil chains the trail.** The keeper's post-battle script grants the **Starfall
   Shard** (key item, stacks ×5), the site's one-per-game reward, sets
   **`flag:vigil_<n>_kept`**, and — reading the next fall in the shard's glint — sets
   **`flag:vigil_reading_<n+1>`**. Oriel's swap placements at Nightreach re-read any held
   reading, so a clue can never be lost.
5. **Five kept → the summit.** `flag:vigil_5_kept` unseals **the Last Lesson** at the Umbral
   Spire's summit (a flag-gated re-dress of the shipped climax map — no new map): three Vigilant
   rematches back-to-back, a heal, then **Fenn, ace 70**. Win → the Ninth Lantern takes the five
   shards → **Dawnbrael** wakes (one-off catch, lv 70) → the title beat sets
   **`flag:starfall_crown`**.
6. **After the crown.** Every Vigilant (and Fenn) swaps to a **re-runnable bout** placement —
   the standing post-game challenge circuit the chain leaves behind — and **Helixia** blooms
   into Dawnstead's sunlit verge (the day-form table's capstone, below).

**The chain at a glance:**

| # | Site (map id) | Host (one added warp) | Pairing | Band | Vigilant (ace) | Register catch | One-per-game reward |
|---|---|---|---|---|---|---|---|
| 1 | Hearthfall (`vigil_hearthfall`) | `tinderwick` — the bluff above the Beacon | Ember & Tide (southern crown) | 58–60 | **Wick-Mother Esra** (Embralux 60) | **Embralux** · **Tideveil** (water) | **Radiant Charm** (×3.0 vs any-status kin) |
| 2 | Grovefall (`vigil_grovefall`) | `spore_grotto` — the far cell | Verdant & Stone (eastern crown) | 60–62 | **Old Foreman Bramm** (Mycovast 62) | **Mycovast** | **Star-chart: Tremor Quake** (the Stone nuke never minted) |
| 3 | Stormfall (`vigil_stormfall`) | `thunderroost` — the upper ledge | Storm & Frost (northern crown) | 62–64 | **Ondra Vael** (Nullhusk 64) | **Nullhusk** | **the storm-tithe** (5,000w + Starglass ×2) |
| 4 | Sunfall (`vigil_sunfall`) | `sunvault_climb_ii` — behind the viewpoint | Solar & Lunar (western crown) | 64–66 | **Dame Solenne** (Helithorn 66) | **Helithorn** · **Dawnwatcher** | **Star-chart: Sunburst Nova** |
| 5 | Murkfall (`vigil_murkfall`) | `coldfog_marches_ii` — the drowned jetty | Light & Dark (the mirror axis) | 66–68 | **Warden Mer** (Bogvast 68) | **Bogvast** · **Cindervast** · **Solarmourn** | **Morrow Charm** (×3.0 first-turn) |
| ★ | The Last Lesson | `umbral_spire` summit (re-dress, no new map) | the whole sky | 67–70 | Ondra → Solenne → Mer → **Fenn** (Dawnwatcher 70) | **Dawnbrael** (lv 70, set-piece) | **Fenn's Field-Glass** + the **Star-tender** title beat |

**The flag table (exact strings — rule 3, every flag opened here is consumed here):**

| Flag | Set by | Consumed by |
|---|---|---|
| `flag:starfall_begun` | `cutscene.starfall_begins` (Nightreach terrace, requires `flag:dawn`) | Oriel/witness NPC swap pairs; LORE entry unlock |
| `flag:vigil_reading_1` | `cutscene.starfall_begins` | warp `tinderwick → vigil_hearthfall`; Oriel re-read placement |
| `flag:vigil_1_kept` | `script.vigil_hearthfall` (after Esra falls) | Esra's beaten-swap; gates nothing else (reading 2 is the chain) |
| `flag:vigil_reading_2` | `script.vigil_hearthfall` | warp `spore_grotto → vigil_grovefall`; Oriel re-read |
| `flag:vigil_2_kept` | `script.vigil_grovefall` | Bramm's beaten-swap |
| `flag:vigil_reading_3` | `script.vigil_grovefall` | warp `thunderroost → vigil_stormfall`; Oriel re-read |
| `flag:vigil_3_kept` | `script.vigil_stormfall` | Ondra's beaten-swap |
| `flag:vigil_reading_4` | `script.vigil_stormfall` | warp `sunvault_climb_ii → vigil_sunfall`; Oriel re-read |
| `flag:vigil_4_kept` | `script.vigil_sunfall` | Solenne's beaten-swap |
| `flag:vigil_reading_5` | `script.vigil_sunfall` | warp `coldfog_marches_ii → vigil_murkfall`; Oriel re-read |
| `flag:vigil_5_kept` | `script.vigil_murkfall` | **the summit trigger** (`requires_flag`); Mer's beaten-swap; Oriel's "sixth reading" placement |
| `flag:starfall_lesson` | `script.starfall_round` (after Fenn falls) | gates the Dawnbrael set-piece trigger (so a fled/KO'd Dawnbrael is re-approachable **without** re-fighting the Round) |
| `flag:starfall_crown` | `cutscene.startender_named` (after the Dawnbrael catch) | every re-runnable-bout swap; Helixia's Dawnstead verge entry; Oriel/Fenn epilogue placements; LORE "Star-tender" unlock |

*(The boolean chain is strict — reading N+1 only ever issues from kept N — so `flag:vigil_5_kept`
provably implies all five, the C3 "Long Round" pattern; no quest counter needed.)*

**The `vigilant` payout class (proposal, locked here).** A full-six smart-AI trial sits above a
warden and below Còr: **`vigilant` = 80w × ace** (10-economy §4's ladder extends route 16 →
keeper 20 → rival 24 → warden 60 → **vigilant 80** → cor 120; §9's "payout classes don't grow
past `cor`" invariant holds). Fenn's Last Lesson is priced like the mountain: **`cor` class,
120 × 70 = 8,400w**. The build must mirror the new class in all three economy homes
(`content/trainers.ts`/`economy.ts` ↔ `PAYOUT_RATE`/`BUILT_PAYOUTS` + a POSTGAME leg in
`tools/balance/progression.mjs` ↔ the 10-economy §4 table) and re-run the model. Post-crown
re-runnable bouts are **optional income outside the solvency legs** (model them as one-time).

**The register ledger (where every legendary-register single now lives).** The Vigils
deliberately mop up the E-tier singles the region builds left unplaced:

| Kin | Tier · type | Home |
|---|---|---|
| Embralux #33 | E · Ember/Light | **Hearthfall** bed (very rare, 60) + Esra's ace |
| Tideveil #34 | E · Tide/Light | **Hearthfall** water bed (very rare, 60) |
| Prismara #37 | E · Stone/Light | Crystoll Vault — **East writer's, untouched here** |
| Mycovast #70 | E · Verdant/Stone | **Grovefall** bed (very rare, 62) + Bramm's ace |
| Frostholm #73 | E · Frost/Light | Aurora Hollow (built, West) — untouched |
| Helithorn #119 | E · Solar | **Sunfall** bed (very rare, 66) + Solenne's ace |
| Solarmourn #128 | E · Solar | **Murkfall** bed (very rare, 67) — mourninglight blooming where the dark thins |
| Dawnwatcher #129 | E · Lunar/Light | **Sunfall** bed (very rare, 65); also Fenn's ace (battle) |
| Heliovast #130 | E · Solar | Helia Vault (built, West) — untouched |
| Helixia #131 | E · Solar | Fenn's team (battle); **catchable post-crown** in Dawnstead's verge (very rare, 60–62, `requires flag:starfall_crown`) |
| Lunaveil #132 | E · Lunar | **left for Starwell** (Central writer's "near-legendary" — a non-binding suggestion; this file places nothing there) |
| Nullhusk #144 | E · Storm/Dark | **Stormfall** bed (very rare, 64) + Ondra's ace |
| Cindervast #145 | E · Dark | **Murkfall** bed (very rare, 67) + Mer's team |
| Bogvast #146 | E · Dark | **Murkfall** bed (very rare, 68) + Mer's ace |
| Nullmajor #150 | F · Dark | **Còr's — Central writer's, untouched here** |
| Dawnbrael #151 | F · Solar/Light | **the Last Lesson's catch** (lv 70 set-piece) |

*(Pharolux #157 and Corolion #158/Dawnregent #159 stay kindling-only, per the roster canon. The
Vigilants' aces double as their site's bed catch by design — the trial proves you can face what
you came to catch.)*

---

### The opening — the first starfall (Dawnstead → Nightreach)

**At a glance** — no new map · NPC + cutscene wiring on `dawnstead` and `nightreach_observatory` ·
gate: `flag:dawn` · rec. level 55+ (the rematch band is the intended on-ramp).

1. **Main path**
   1. **A star falls — and nobody mourns it.** A flag-gated witness NPC in Dawnstead
      (`npc.starfall_witness`, `requires_flag: flag:dawn`, `hidden_when_flag:
      flag:starfall_begun`) has seen the first fall: not a constellation going out — the player
      has seen plenty of those — but something *shed*, trailing gold. Nightreach is beside itself.
   2. **Watcher Oriel, promoted.** At the Nightreach telescope terrace, the junior watcher of the
      Vigil of the Seven now keeps the great eyepiece herself. She read the fall; she'll read the
      rest. `cutscene.starfall_begins` (interact, `requires_flag: flag:dawn`, `once: true`) sets
      `flag:starfall_begun` + `flag:vigil_reading_1` and speaks **reading 1** (below).
2. **Story beats**
   > Oriel, at the eyepiece: *"All those years we watched the sky lose lights. Last night it
   > GAVE one back — shed it, like a tree sheds a leaf it's finished with. The old watchers used
   > to call them star-shards. The very old watchers used to call them invitations."*
   >
   > Oriel, handing over the first reading: *"I read where it fell. I'd fetch it myself, but
   > somebody promoted me, and now I'm not allowed anywhere with weather."*
   - **Cinematic staging** — small and warm: a `musicSting` + `flashColor` (the fall crossing the
     sky) over the terrace, then plain portrait dialogue. No letterbox; this is wonder, not dread.
3. **Mechanic introductions** — the chain's grammar: a *reading* is a key; Oriel is the home base
   who re-reads any held reading (her terrace placements swap flag-disjointly, the Fenn-waystone
   pattern: pre-chain → one per held reading → "carry the five up the mountain" on
   `flag:vigil_5_kept` → epilogue on `flag:starfall_crown`).
4. **Optional content** — none here; the opening is deliberately one warm beat.
5. **Don't-miss callouts** — Oriel's terrace is the chain's noticeboard: lost the thread? She
   repeats the current reading, verbatim, slightly wearily.
6. **Validation hooks**
   - **No new map.** `dawnstead`: add `npc.starfall_witness` (`requires_flag: flag:dawn`,
     `hidden_when_flag: flag:starfall_begun`). `nightreach_observatory`: Oriel's placement set on
     the telescope terrace — `cutscene.starfall_begins` (interact, `once: true`,
     `requires_flag: flag:dawn`, `hidden_when_flag: flag:starfall_begun`, sets
     `flag:starfall_begun` + `flag:vigil_reading_1`), plus the re-read/sixth/epilogue swap
     placements per the flag table (each pair `requires_flag`/`hidden_when_flag` disjoint).
   - **LORE:** add glossary entries **"The Starfall"** (`unlock_flag: flag:starfall_begun`) and
     **"The Vigilants"** (`unlock_flag: flag:vigil_1_kept`) — existing flags, no new wiring.

---

### The five Vigil sites — *the world re-toured at full lamp*

Every site is built to one shape (so the build agents can stamp it): a **single-screen annex map**
(~24×18, kind/tileset matching its host; music + `battle_backdrops` reuse the host's keys), entered
by **one added step_on warp** on the host map (the only edit a shipped map JSON takes, plus an
optional non-solid star-scar deco object gated `requires_flag: flag:dawn`). Inside: the **shard
set-piece** (a starglint object) at the far end; the **Vigilant** posted before it with a step_on
trial band across **every walkable approach tile** (the un-walk-aroundable rule); **two encounter
zones** in the site band; **one cache** (Starglass Shard, except Stormfall — its prize is the
jackpot); **no rest point** (the trial is meant to bite; the hub wheel is one warp away). Beaten,
each Vigilant swaps to a plain-dialogue placement; post-`flag:starfall_crown` they swap again to a
**re-runnable bout** (`script.vigil_<site>_again` — intro line → `battle` → thanks; payout each
time — the standing circuit).

The host-map warps carry a `blocked_ref` until their reading is held, in the watchers' voice
(suggested `npc.vigil_scar_sealed`): *"A seam of starlight, shut tight. Whatever fell here is
waiting to be read first."*

#### Vigil I — Hearthfall — *where the first lamp learned its name*

**At a glance** — `vigil_hearthfall` · annex off `tinderwick` (the NE bluff above the Beacon
door) · warp `to_vigil_hearth`, `requires_flag: flag:vigil_reading_1` · pairing: **Ember & Tide**
(the southern crown) · band **58–60** · keeper: **Wick-Mother Esra**, ace 60.

- **Reading 1 (Oriel):** *"The first came down in the south — where the first lamp learned its
  name. Climb past the lantern that taught the sky to answer; it fell on the bluff above, where
  even the gulls go quiet."*
- **The site:** a wind-bitten grass bluff over the sea — Tinderwick's rooftops below in full
  daylight, the Beacon's lantern room at your back. A shore strip gives the water zone (Tidecall
  held since forever). The first thing the player fought for, seen from above, in the morning.
- **The keeper:** **Wick-Mother Esra** — the candlemaker who taught Brisa Tallow to dip her first
  wick. Tiny, ancient, terrifyingly calm.
  > Esra, intro: *"I dipped Brisa's first wick when she came up to my elbow, dear. She vouches
  > for you. Wicks don't lie — but let's check."*
  > Esra, beaten: *"Steady as her best. Take the shard — and the charm; I pressed it for whoever
  > finally came."*
- **Rewards:** **Starfall Shard** ×1 · **Radiant Charm** (one-per-game conditional charge: ×3.0
  toward a kin afflicted by *any* status — the apex-band "afflict, then ask" catching lesson) ·
  reading 2 · Esra's payout **4,800w**.
- **Hooks:** trial script `script.vigil_hearthfall` = intro → `battle: vigilant_esra` → defeat
  line → `giveItem starfall_shard` → `giveItem radiant_charm` → `setFlag flag:vigil_1_kept` →
  `setFlag flag:vigil_reading_2` (reading-2 copy spoken by Esra reading the shard's glint).
  Encounters: `tall_grass` — Scorchwing (uncommon 58–60), Chandrek (uncommon 58–60), Wicklord
  (rare 59–60), **Embralux (very rare, 60)**; `water` — Prismare (uncommon 58–60), **Tideveil
  (very rare, 60)**. Cache: `starglass_shard`.

#### Vigil II — Grovefall — *under the hill, where the moss has opinions*

**At a glance** — `vigil_grovefall` · annex off `spore_grotto` (the far cell) · warp
`to_vigil_grove`, `requires_flag: flag:vigil_reading_2` · pairing: **Verdant & Stone** (the
eastern crown) · band **60–62** · keeper: **Old Foreman Bramm**, ace 62.

- **Reading 2 (Esra/Oriel):** *"The second went to earth in the east — under the hill, where the
  wood keeps its own weather and the moss has opinions. Bring a light. Bring patience. The grotto
  has both, and shares neither."*
- **The site:** a glowmoss cathedral-cell beyond the Spore Grotto, the shard seated in a fungal
  vault that has grown around it in a season (kind `cave`; glowmoss encounter tiles; Radiant
  Lamplight assumed — the lit lane stays visible regardless, spine §5).
- **The keeper:** **Old Foreman Bramm** — the foreman who taught Otho Grist the deep way; retired
  to the Hollow to grow things instead of cutting them.
  > Bramm, intro: *"Otho says you out-lasted him. Otho exaggerates. ...Show me he doesn't."*
  > Bramm, beaten: *"Hah. He doesn't. The deep way, walked all the way up. Take the chart — we
  > never minted a Stone figure; turns out the sky did it for us."*
- **Rewards:** **Starfall Shard** ×1 · **Star-chart: Tremor Quake** (the Stone nuke chart the
  Cinderhead pit-stores never stocked — find-first per 10-economy §6) · reading 3 · payout
  **4,960w**.
- **Hooks:** `script.vigil_grovefall` = intro → `battle: vigilant_bramm` → defeat → `giveItem
  starfall_shard` → `giveItem chart_tremor_quake` → `setFlag flag:vigil_2_kept` → `setFlag
  flag:vigil_reading_3`. Encounters (`cave`/glowmoss `tall_grass`): Fernlance (uncommon 60–62),
  Rootwarden (uncommon 60–62), Gravelo (uncommon 60–62), Mycelarch (rare 61–62), **Mycovast
  (very rare, 62)**. Cache: `starglass_shard`.

#### Vigil III — Stormfall — *the wind's spare pocket*

**At a glance** — `vigil_stormfall` · annex off `thunderroost` (the upper ledge) · warp
`to_vigil_storm`, `requires_flag: flag:vigil_reading_3` · pairing: **Storm & Frost** (the
northern crown) · band **62–64** · keeper: **Ondra Vael**, ace 64.

- **Reading 3:** *"The third went north, into the wind's spare pocket — the roost where storms go
  when they're off duty. Take the kite. Take a coat. Retrieve your own hat; I shan't fetch it."*
- **The site:** an aerie shelf above Thunderroost, scoured grass and hail-pitted stone, the shard
  crackling faintly in a nest of fulgurite (Updraft Kite held; band wilds run Storm/Frost).
- **The keeper:** **Ondra Vael** — Mira's grandmother, the first kite-flier of Galehigh, who
  retired the day she ran out of weather that frightened her.
  > Ondra, intro: *"Mira flies in what I called a light breeze at her age. Stand up straight —
  > the sky's sent us a present, and I open my own post."*
  > Ondra, beaten: *"HA! You'd have made a kite-flier. The aerie's tithed every storm since the
  > dawn broke — take it; I can't spend wind."*
- **Rewards:** **Starfall Shard** ×1 · **the storm-tithe** (the wick jackpot: `giveMoney 5000` +
  a `starglass_shard ×2` cache) · reading 4 · payout **5,120w**.
- **Hooks:** `script.vigil_stormfall` = intro → `battle: vigilant_ondra` → defeat → `giveItem
  starfall_shard` → `giveMoney 5000` → `setFlag flag:vigil_3_kept` → `setFlag
  flag:vigil_reading_4`. Encounters (`tall_grass`): Tempestail (uncommon 62–64), Vortavane
  (uncommon 62–64), Glacitern (uncommon 62–64), Strikeaven (rare 63–64), **Nullhusk (very rare,
  64)**. Cache: `starglass_shard` ×2 (the tithe's second half). *(Thunderroost's own prize stays
  the Tempest chart — don't duplicate it here.)*

#### Vigil IV — Sunfall — *where summer was put away for safekeeping*

**At a glance** — `vigil_sunfall` · annex off `sunvault_climb_ii` (behind the X3 viewpoint) ·
warp `to_vigil_sun`, `requires_flag: flag:vigil_reading_4` · pairing: **Solar & Lunar** (the
western crown) · band **64–66** · keeper: **Dame Solenne**, ace 66.

- **Reading 4:** *"The fourth fell where summer was put away for safekeeping — the high terraces
  that remembered daylight before the rest of us believed in it again."*
- **The site:** a golden terrace-garden fold above the climb, sun-vines blooming wild now the sky
  does the work; the shard rests in a cracked sun-basin, warm to look at. The one site played in
  *two* lights — daylight above, dreamlight pooling where the shard's glow meets the basin.
- **The keeper:** **Dame Solenne** — keeper of the last warm day before Lucan Pyre; taught him
  everything, including (she notes) the bowing.
  > Solenne, intro: *"I kept the last warm day for forty years, and now the mornings come free.
  > Indulge an old keeper — one encore, full light."*
  > Solenne, beaten: *"Curtain. ...Do you know, I don't mourn the last warm day any more. There
  > will be others. Take the figure — it's the sun's whole bow."*
- **Rewards:** **Starfall Shard** ×1 · **Star-chart: Sunburst Nova** (find-first nuke) · reading
  5 · payout **5,280w**.
- **Hooks:** `script.vigil_sunfall` = intro → `battle: vigilant_solenne` → defeat → `giveItem
  starfall_shard` → `giveItem chart_sunburst_nova` → `setFlag flag:vigil_4_kept` → `setFlag
  flag:vigil_reading_5`. Encounters (`tall_grass`): Sunstag (uncommon 64–66), Solreach (uncommon
  64–66), Crystalune (uncommon 64–66), Lunaquell (rare 64–66), **Dawnwatcher (very rare, 65)**,
  **Helithorn (very rare, 66)**. Cache: `starglass_shard`.

#### Vigil V — Murkfall — *where the water forgot how to speak*

**At a glance** — `vigil_murkfall` · annex off `coldfog_marches_ii` (the drowned jetty) · warp
`to_vigil_murk`, `requires_flag: flag:vigil_reading_5` · pairing: **Light & Dark** (the mirror
axis) · band **66–68** · keeper: **Warden Mer**, ace 68.

- **Reading 5:** *"The last fell where the water forgot how to speak. It is learning again — go
  gently into the murk; some of what you'll meet is still waking. And one of them has waited a
  long time to greet you."*
- **The site:** the one place the chain turns quiet — a fold of the deep marsh where the
  Hollowing's drain is *healing*: colour seeping back at the edges, one snuffed lantern-row relit,
  the shard glowing in shallow black water. The drained dark resisted Lamplight all game (spine
  §5 caveat); the shard is the first thing to win against it. Keep the staging gentle — this is
  Arc B's last echo, not a haunted house.
- **The keeper:** **Warden Mer** — a former Hollowing lantern-bearer, folded back among the
  star-tenders after the dawn (the Còr mercy, paid forward). She tends the healing marsh she once
  helped quiet. **Sincere throughout — no glint here.**
  > Mer, intro: *"I carried a null-lantern through this marsh once. I carry this now. Before I
  > hand the light back, I will know the hand I hand it to is steady."*
  > Mer, beaten: *"It holds. Brighter hands than mine ever were. ...The marsh thanks you. Both of
  > us do — both of me, perhaps."*
  > Mer, the pointer onward: *"The sixth never fell, you know. It's been waiting where the night
  > ended. Carry the five up the mountain — and ask the old man what he sees."*
- **Rewards:** **Starfall Shard** ×1 · **Morrow Charm** (one-per-game conditional charge: ×3.0 on
  the encounter's **first turn** — the gamble throw, "before the dark notices") · payout
  **5,440w**. *(No reading 6 — Mer's pointer and Oriel's `flag:vigil_5_kept` placement carry the
  player to the summit.)*
- **Hooks:** `script.vigil_murkfall` = intro → `battle: vigilant_mer` → defeat + pointer →
  `giveItem starfall_shard` → `giveItem morrow_charm` → `setFlag flag:vigil_5_kept`. Encounters
  (`tall_grass`, blighted-healing): Embergone (uncommon 66–68), Voidmantle (uncommon 66–68),
  Wisprestored (uncommon 66–68 — the Light blooming back, atlas §4 inverted), **Solarmourn (very
  rare, 67)**, **Cindervast (very rare, 67)**, **Bogvast (very rare, 68)**. Cache:
  `starglass_shard`.

---

### The Last Lesson — *the summit, the old man, the morning made flesh*

**At a glance** — `umbral_spire` summit, **re-dressed by flags — no new map** (flag-gated
MapObjects/NPCs keyed on `flag:dawn` + the chain flags; swap pairs share footprint+solidity) ·
trigger `requires_flag: flag:vigil_5_kept` · band **67–70** · the hardest fight in the game:
**Star-tender Fenn, ace 70** · sets `flag:starfall_lesson` → `flag:starfall_crown`.

1. **Main path**
   1. **The summit in daylight.** The climax dungeon, re-walked post-dawn: the null-lanterns
      cold, the basalt warm-edged, the Ninth Lantern's collar empty — five sockets, five shards
      in your satchel. (Pure flag-gated re-dress on the Central writer's shipped map; **build
      order: the five sites can ship before Central builds the Spire — the summit leg waits on
      it.**)
   2. **Three Vigilants, back to back — the gauntlet.** At the lantern, Ondra, Solenne and Mer
      have climbed ahead ("we came to watch; the watching turned into a queue"). The trigger
      (interact at the lantern, `requires_flag: flag:vigil_5_kept`, `hidden_when_flag:
      flag:starfall_lesson`) runs `script.starfall_round`: **`battle: vigilant_ondra_summit` →
      `battle: vigilant_solenne_summit` → `battle: vigilant_mer_summit` → `heal` → `battle:
      startender_fenn`**. A loss anywhere aborts the script (engine convention) — blackout,
      tithe, and the whole Round again; that is the intended shape of the ultimate.
   3. **Fenn, at full strength.** The heal is diegetic — Fenn trims your lamps himself: *"I'll
      want you at your best. I have waited a very long time to be allowed mine."* Then the old
      man's last lesson: six kin, lv 68–70, the whole night-to-dawn arc in one team, ending on
      **Dawnwatcher** — the kin he named, forty years ago, as a hope.
   4. **The shards seated — Dawnbrael wakes.** Win, and the script seats the five shards in the
      Ninth Lantern's collar (`setFlag flag:starfall_lesson`); the lantern takes them and the
      "sixth shard" answers — it never fell, because it is the morning itself: **Dawnbrael**
      (Solar/Light, the first-morning kin, **lv 70**) descends to the relit lantern. A separate
      one-off static catch `EventTrigger` (the Keylumen pattern), gated
      `requires_flag: flag:starfall_lesson` — so a fled or fainted Dawnbrael **returns with the
      next sunrise** (re-approach the lantern; no re-fighting the Round).
   5. **The title beat.** With Dawnbrael caught, `cutscene.startender_named` (`once: true`):
      Fenn gives the keepsake and the word — sets **`flag:starfall_crown`**. The apprentice who
      began with a satchel errand ends a **Star-tender**, named by the man who sent them out.
2. **Story beats** *(sincere throughout — the humour stopped at the marshes)*
   > Fenn, intro: *"No satchel this time. No errand. One lesson left, and it's the one I never
   > could teach you — what you do when the teacher steps aside. Everything I have, apprentice.
   > Show me everything you've become."*
   >
   > Fenn, beaten: *"...There it is. The whole sky in one steady lamp."*
   >
   > Fenn, the naming: *"I have nothing left to teach. Stand up straight, Star-tender — the
   > title was always going to be yours. I'm only the one saying it out loud."*
   - **Cinematic staging** — the Round stays plain (faces and battles); the seating of the
     shards gets the apex `gleam` cadence (held `silence` → warm `tint` → the lamp sfx →
     `gleam` → a major swell — the Keystar relight's quieter sibling); Dawnbrael's descent is a
     `flashColor` + `narrate`, not bombast; the naming lands on a held beat over the open summit
     sky, **explicitly rhyming with the satchel ceremony at the waystone** (the game's first
     gift and its last, same shape, same place in the heart).
3. **Mechanic introductions** — none. Six-kin smart teams, consecutive battles, the heal op, a
   static catch: every piece already exists. That's the point — the ultimate trial is the game's
   own systems at full lamp.
4. **Optional content** — post-`flag:starfall_crown`, Fenn's summit placement swaps to a
   **re-runnable Last Lesson** (`script.last_lesson_again` — the bout only, full payout; the old
   man will always have one more), and each Vigilant's site placement swaps to a re-runnable
   bout. `[MISSABLE]` by nature; the circuit is the standing endgame.
5. **Don't-miss callouts** — bring the **Radiant** and **Morrow Charms** for Dawnbrael (lv 70,
   F-tier: the chain's own rewards are its catching kit); the Round pays **~25,000w** on a full
   first clear — the end-tier chart fund.
6. **Validation hooks** — gathered in the chain master list below.

---

### Validation hooks — the chain master list (build agents copy verbatim)

- **New maps (5, all small annexes; register in `world/maps.ts`, nodes + edges in `graph.ts`):**
  `vigil_hearthfall`, `vigil_grovefall` (kind `cave`), `vigil_stormfall`, `vigil_sunfall`,
  `vigil_murkfall` — all `optional: true`, region matching their host (south / east / north /
  west / outer), node `reward` notes naming their register catch. Music + `battle_backdrops`
  reuse the host map's keys. **No rest points; one cache each; encounter tiles carry the
  `encounter_terrain` tag** (the standing tall-grass rule).
- **New edges (one added warp per shipped host map — the only host edits, plus an optional
  `flag:dawn`-gated star-scar deco object):**
  - `tinderwick → vigil_hearthfall` via `to_vigil_hearth`, `requires_flag: flag:vigil_reading_1`, bidir
  - `spore_grotto → vigil_grovefall` via `to_vigil_grove`, `requires_flag: flag:vigil_reading_2`, bidir
  - `thunderroost → vigil_stormfall` via `to_vigil_storm`, `requires_flag: flag:vigil_reading_3`, bidir
  - `sunvault_climb_ii → vigil_sunfall` via `to_vigil_sun`, `requires_flag: flag:vigil_reading_4`, bidir
  - `coldfog_marches_ii → vigil_murkfall` via `to_vigil_murk`, `requires_flag: flag:vigil_reading_5`, bidir
  - All five host warps carry `blocked_ref: npc.vigil_scar_sealed`; annex landings land ON their
    return warp (the audit_warps contract); exact host tiles are the builder's (walkable, off the
    lit lane) — bake both sides and run `audit_warps.py` + `audit_flow.py` + `audit_region.py`.
- **No new mechanics anywhere** (verified against the engine): six-kin parties are data
  (`TrainerKin[]` is unbounded); the gauntlet is sequential `battle` ops in one script (loss
  aborts before any reward step — author all grants after the final battle); `heal` op between
  bouts; conditional charges use existing `ChargeCondition` kinds only (`any_status`,
  `first_turn`); rewards via `giveItem`/`giveMoney`/`setFlag`; all gating via
  `requires_flag`/`hidden_when_flag` on warps/NPCs/objects/triggers.
- **New trainers (`content/trainers.ts` — all `ai: 'smart'`, all with `intro_ref`/`defeat_ref`
  per the lines above; class `vigilant` = 80w × ace except Fenn at `cor` 120):**

  | id | name · title | party (species_id · lv) | payout |
  |---|---|---|---|
  | `vigilant_esra` | WICK-MOTHER ESRA · Vigilant | 7·58, 12·58, 19·59, 43·59, 17·59, **33·60** | 4,800 |
  | `vigilant_bramm` | OLD FOREMAN BRAMM · Vigilant | 40·60, 64·60, 58·61, 52·61, 55·61, **70·62** | 4,960 |
  | `vigilant_ondra` | ONDRA VAEL · Vigilant | 102·62, 79·62, 96·63, 93·63, 82·63, **144·64** | 5,120 |
  | `vigilant_solenne` | DAME SOLENNE · Vigilant | 121·64, 110·64, 123·65, 127·65, 128·65, **119·66** | 5,280 |
  | `vigilant_mer` | WARDEN MER · Vigilant | 135·66, 138·66, 85·67, 140·67, 145·67, **146·68** | 5,440 |
  | `vigilant_ondra_summit` | ONDRA VAEL · Vigilant | 102·67, 79·67, 96·68, 93·68, 82·68, **144·69** | 5,520 |
  | `vigilant_solenne_summit` | DAME SOLENNE · Vigilant | 121·67, 110·67, 123·68, 127·68, 128·68, **119·69** | 5,520 |
  | `vigilant_mer_summit` | WARDEN MER · Vigilant | 135·68, 138·68, 85·68, 140·69, 145·69, **146·69** | 5,520 |
  | `startender_fenn` | STAR-TENDER FENN · Star-tender | 9·68, 107·68, 125·68, 87·69, 131·69, **129·70** | 8,400 |

  *(Fenn's six, read in order, are the game's arc: the small light first — Glimscout — then the
  moons — Lunarbel, Crystalune — the light that holds — Prismantus — the sun's spiral — Helixia —
  and the one he named as a hope: **Dawnwatcher**, ace 70. Music: Vigilants on
  `battle-nightfall`; Fenn on the Spire's boss cue if shipped, else `battle-veil`.)*
- **New items (`content/items.ts`):** `starfall_shard` (key; granted ×1 per site, never consumed
  — the summit script *seats* them narratively); `radiant_charm` (charge, `catch_bonus: 3.0`,
  `condition: { kind: 'any_status' }`, no price); `morrow_charm` (charge, `catch_bonus: 3.0`,
  `condition: { kind: 'first_turn' }`, no price); `chart_tremor_quake` (chart, `teach_move:
  tremor_quake`, 4,000w); `chart_sunburst_nova` (chart, `teach_move: sunburst_nova`, 4,000w);
  `fenns_glass` (key — "Fenn's Field-Glass", the keepsake). Both charts follow the
  `chart_tempest` find-first pattern; both moves exist in the 125-pool and are not
  signature-owned.
- **Scripts / cutscenes / dialogue refs:** `cutscene.starfall_begins`, `npc.starfall_witness`,
  `npc.vigil_scar_sealed`, `script.vigil_hearthfall` / `_grovefall` / `_stormfall` / `_sunfall` /
  `_murkfall` (+ their `_again` re-runnable variants post-crown), `script.starfall_round`,
  `cutscene.dawnbrael_wakes` (the static catch set-piece, `requires_flag: flag:starfall_lesson`,
  once on success), `cutscene.startender_named` (sets `flag:starfall_crown`), Oriel's terrace
  placement set (flag-disjoint per the flag table).
- **Summit re-dress (waits on Central building `umbral_spire`):** flag-gated MapObjects/NPCs only
  (swap pairs share footprint+solidity); the Round trigger at the Ninth Lantern (`interact`,
  `requires_flag: flag:vigil_5_kept`, `hidden_when_flag: flag:starfall_lesson`); the Dawnbrael
  trigger (`requires_flag: flag:starfall_lesson`); the naming cutscene (`once: true`). **The five
  Vigil sites have no dependency on Central and may ship first.**
- **Encounters:** mirror every annex table into `build_species.py EXTRA_ENCOUNTERS` AND add the
  five map ids to `CURATED_AREAS`; bed-band continuity 58–60 → 60–62 → 62–64 → 64–66 → 66–68
  (each annex sits 1 band above the last — the chain's own curve, no cliffs against host
  geometry since annexes are sealed behind readings). Helixia's post-crown Dawnstead verge entry
  (very rare, 60–62, `requires flag:starfall_crown`) rides the day-form table's flag-gated zone
  mechanism — one extra entry, no new wiring.
- **Economy (the three mirrored homes + the model):** add the `vigilant 80w` class to
  10-economy §4 and `PAYOUT_RATE`; add a POSTGAME leg to `progression.mjs` JOURNEY (one-time
  clears only; re-runnable bouts excluded from solvency); first-clear income ≈ 50,500w trainer
  payouts (25,600w across the five sites + 24,960w for the Round) + the 5,000w storm-tithe +
  ~9,000w in Starglass — the sink is end-tier charts and Dawnbrael's charges. `node tools/balance/progression.mjs` must PASS. No species/move edits → `validate.mjs`
  / `simulate.mjs` unaffected (re-run `validate.mjs` anyway after the EXTRA_ENCOUNTERS mirror).
- **Tone gate (spine §10):** canon vocabulary only; the Vigilants are celebration, never
  gatekeeping bitterness; Mer is the Hollowing's mercy paid forward (never a punished villain);
  the glint ratio holds (~1 in 6, none at Murkfall or the summit); run `copy-editing` on the
  readings and all keeper/Fenn dialogue before shipping.

---

## End of the Wayfaring

Post-game is the only region in true daylight: **Arc D resolves**, the vesperlamp at its
brightest, the lullaby returned in major. There is no hand-off — this is the last region file.
What it leaves open for the player is deliberate and endless-by-design: the **day-form re-walk**
of the relit valleys, the two Starreach landmarks (**Crystoll Vault**, **Starwell**), the
Lampwarden/Wren **rematches** at lv55–65, and above them **the Starfall Vigils** — the
riddle-led trial chain that climbs to the Last Lesson, the Star-tender naming, and the standing
re-runnable circuit it leaves behind. The closing note is the whole game's thesis, and the
binding tone for any post-game copy: **the cycle has resumed, dusk will come again, and that is
exactly the point.**
