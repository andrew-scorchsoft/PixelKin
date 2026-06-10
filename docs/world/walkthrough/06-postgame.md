# PixelKin Walkthrough — 06 · Post-game (after `flag:dawn`)

> Region file under the [spine](./README.md). Read its §0 rules, §2 flag strings, §3 arcs
> (incl. Arc A's Wren resolution and Arc D's celestial-calendar payoff), §4 curve (the
> lv55–65 rematch band), §7 template, §8 the day-forms proposal, and §10 voice first — they
> are binding here. Areas follow the §7 template exactly. Canon vocabulary only: **kin,
> Lumenary, Lampwarden, Gleam, Lantern Gift, vesperlamp, kindling, the Hollowing.**

## Region header

**The morning after the long night.** This is the only region played in true daylight — the
visual and emotional payoff of the whole Wayfaring. The Keystar is relit, the Penumbra is
gone, and Vesperholm has woken into its first dawn in years. Post-game delivers five things:
the epilogue town of **Dawnstead** (Tinderwick reborn in open sky, with the lullaby returned
in triumphant major); a fresh collecting hook in the **day-forms** of early kin that the
relit sky now wakes; the **late-backtrack landmarks** that only Starreach + dawn make worth a
return (**Crystoll Vault**, **Starwell**); the **Radiant-Lamplight backtracks** — the early
dark areas, re-walked with the vesperlamp at its brightest, finally giving up the optional
content that sat beyond your old reach (spine §5); and the **gentle arc resolutions** — Wren at
peace in daylight (A6), and Warden Còr's quiet aftermath. No new Lantern Gifts: all six are
already earned, so post-game is *collecting, rematches, and resolution*, not traversal.

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
3. **Where to return (each a `[LATER: Lamplight ≥ tier]` reveal, all `[MISSABLE]`):**
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

## End of the Wayfaring

Post-game is the only region in true daylight: **Arc D resolves**, the vesperlamp at its
brightest, the lullaby returned in major. There is no hand-off — this is the last region file.
What it leaves open for the player is deliberate and endless-by-design: the **day-form re-walk**
of the relit valleys, the two Starreach landmarks (**Crystoll Vault**, **Starwell**), and the
Lampwarden/Wren **rematches** at lv55–65. The closing note is the whole game's thesis, and the
binding tone for any post-game copy: **the cycle has resumed, dusk will come again, and that is
exactly the point.**
