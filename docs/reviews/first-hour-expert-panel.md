# PixelKin — First-Hour Expert Panel Review

> A convened review of PixelKin's **opening hour**: the cold open, Tinderwick,
> Dimglass Coast I→II, and Pearlmoor Quay — plus the core mechanics, the
> storytelling, and the moment-to-moment feel a brand-new player meets first.
>
> **Scope reviewed:** `docs/world/walkthrough/01-south.md` (the built worked
> example), the spine (`walkthrough/README.md`), the mechanics docs
> (`mechanics/00`–`05`), `story-bible.md`, and `VISION.md`. Findings are
> measured against the **vision** (`VISION.md`) and **canon** (`CLAUDE.md` Game
> canon) — nothing here proposes drifting from either; where a tempting idea
> *would* drift, the panel says so and self-corrects.
>
> **A note on "design vs build."** South is the game's *built worked example*,
> but parts of it are still spec (status conditions, the move-learn prompt, and
> creature **battle** sprites are not yet wired — see `CLAUDE.md`). Findings are
> tagged **[DESIGN]** (a polish/pacing call on the blueprint) or **[BUILD GAP]**
> (something the spec assumes that isn't live yet and will be felt in the first
> hour). Keep the two apart when triaging.

---

## How the review was run

We assembled a seven-person panel drawn from cartridge-era handheld RPG
disciplines, gave them the documents above, and ran the format the brief asked
for: **an audit first** (what's genuinely good, said plainly), **then an open
debate** on the contested calls, **then a prioritised findings list**. The panel
was instructed that PixelKin's vision — *cosy, nostalgic, collecting/exploration-
first, a copy of nothing* — is the fixed frame, not a thing up for negotiation.
Disagreements that couldn't be resolved against the vision are recorded as
**open questions** rather than smoothed over.

All panelist names and credits below are **original personas** standing in for
real handheld-RPG disciplines — described by *craft and era*, never by any
existing studio, person, or franchise, per `VISION.md`.

## The panel

| Panelist | Discipline | What they watch for |
|----------|------------|---------------------|
| **Mara Holloway** | Systems & battle design | the catch loop, type readability, the math a player *feels* |
| **Tomás Reic** | Narrative & quest design | tone, the pacing of reveals, whether attachment lands before the stakes |
| **Junko Adeyemi** | Pixel-art direction | 240×160 readability, palette discipline, sprite personality |
| **Per Lindqvist** | Chiptune / sequenced music | music-as-drama, register, loop craft, the *blip* |
| **Devs "Dee" Okonkwo** | Level & world design | route flow, "funnel with light," the backtrack web |
| **Grace Balmer** | UX, onboarding & accessibility | cognitive load, vocabulary, save cadence, the touch/mobile seam |
| **Ivo Castellan** | Producer / facilitator | scope, vision-alignment, "is this the game we said we were making" |

---

## Part 1 — The audit (what's working, keep it)

The panel was, to a person, positive on the **shape** of the opening. The
highlights everyone signed off on:

1. **The catch-first soft-gate is best-in-class onboarding.** Brisa won't hold
   the bond-test until the player has lamped one wild kin
   (`flag:caught_first_kin`). It turns "learn to catch" from a tutorial popup
   into a *diegetic errand the warden asks for*, and it quietly prevents a
   lone level-5 starter from walking into an ace-10 fight. **Mara:** "This is the
   genre's oldest lesson taught the genre's best way — by making you want to."

2. **The beacon loop fixes the classic first-gym cliff without a tutorial wall.**
   The Ember Gleam is *earned* by climbing the wick-locked beacon after a coast
   run that carries the party from 5 to ~7–8 against an ace of 10. The level
   on-ramp is hidden inside a story errand. **Dee:** "The lv-5-vs-10 gap is the
   single most common first-hour difficulty bug in this genre. They designed it
   out, and the fix *is* content."

3. **Tidecall reopening Gullcry Rock immediately is the core thrill, delivered
   early.** The player physically stands beside a gated, signed buoy-line on
   Dimglass II, can't reach it, earns Tidecall one town later, and the map
   *reopens itself within the hour.* **Everyone:** this is the exploration pillar
   working exactly as `VISION.md` wants, and teaching the "keep a mental list"
   habit the whole back half relies on.

4. **The Hollowing is seeded as a slow, wordless burn.** Cold-open cowled figure
   → the pinned letter on Dimglass (`sign.dimglass_pinned_letter`) → the old
   lamplighter's grave aside in `give_wick`. By the time the antagonist is
   *named* (East), the dread has been built, not dumped. **Tomás:** "Three quiet
   touches before a single line of exposition. That's discipline."

5. **The type triangle is GBC-clean.** Ember→Verdant→Tide is the only matchup
   logic the first hour demands; the two mirror axes (Solar↔Lunar, Light↔Dark)
   are correctly *reserved* for late/rare/legendary kin. Ten types + dual-typing
   reads as "simple to learn, deep to master." **Mara:** "Nothing in hour one
   asks the player to hold more than a rock-paper-scissors in their head. Good."

6. **The catch math is honest and *legible*.** Wobbles are cosmetic, derived
   from a single transparent `chance` — no hidden second roll. The
   weaken-then-catch loop (`hpTerm` roughly triples odds) is intact, and
   specialty lamps (Tide/Moss/Swift/Hearth…) tie catching power to *exploration*.
   **Mara:** "It simulates cleanly and it *feels* fair, which is rarer than it
   sounds."

7. **The tone holds the vision dead-on.** Festivals frame each Gleam as
   *belonging, not conquest* (Arc E); the Lantern-fair is named as the warmest
   set-piece of the opening; "lanterns in the dark" is felt, not stated. **Per:**
   "The minor→major Gleam swell — `silence` → warm `tint` + lamp sfx → `gleam`
   → festival crossfade — is the right emotional grammar. That's the moment the
   player remembers."

8. **Save-anywhere via the pause menu suits the target player.** A mid-thirties
   parent playing in fifteen-minute windows can stop on any tile. **Grace:**
   "Non-negotiable for this audience, and it's already there. Tick."

---

## Part 2 — The debate (where the panel disagreed)

The brief asked for a *debate*, and the opening hour produced four genuine ones.
These are recorded with the tension intact and a resolution only where the
vision settles it.

### Debate 1 — Is the "first hour" actually the first hour? (pacing)

**Ivo** opened with the scope question. The South region file is titled "the
opening hour and the first two Gleams," but the panel counted what's inside it:
a 4-panel cold open, starter choice + Wren, a verge catch, Brisa's hall errand,
a full coast route (Dimglass I), a beacon ascent with two sight trainers and a
bond-test, the `dusk_begins` set-piece, Fenn's Skyweave explanation, *then*
Dimglass II, *then* Pearlmoor's bell loop (a second route-back errand, a
breakwater with two more trainers, a second bond-test), Tidecall, the Gullcry
backtrack, and **two** festivals.

> **Dee:** "That's not an hour. That's two-and-a-half, comfortably three for a
> careful first-timer. Which is fine — but we should *call* the first hour the
> first hour. The honest 'first 60 minutes' ends somewhere around the **Ember
> Gleam at the beacon**. Everything from Dimglass II onward is hour two."
>
> **Tomás:** "Agreed, and it matters for *reveal pacing*. If `dusk_begins` is
> our load-bearing dread beat and it lands ~25–30 minutes in, the player has
> barely bonded with Tinderwick. The dread is real but the *attachment it's
> meant to threaten* is thin."
>
> **Mara:** "Counter — front-loading the inciting incident is correct. You don't
> want the stakes to arrive in hour three. The genre's best openings hit the
> 'something is wrong' note *early* precisely so the cosy exploration that
> follows has an undertow."
>
> **Grace:** "Both can be true. The beat can land early *and* land soft. The fix
> isn't to move it — it's to make sure the ten minutes *before* it earn a face
> and a place worth losing."

**Resolution (vision-aligned):** Keep `dusk_begins` where it is — early dread is
correct for the vision's "a little melancholy" undertow. But **the panel
recommends naming the true first-hour boundary at the Ember Gleam** for review,
QA, and marketing purposes, and **strengthening the 8–10 minutes of cosy
attachment before the omen** (see Finding F2). Do not re-pace the plot; deepen
the warmth it interrupts.

### Debate 2 — Is making the *first* Gleam an earned tower-ascent too much friction?

The beacon loop is the panel's favourite difficulty fix (audit #2) and its most
contested onboarding call.

> **Tomás:** "The first Gleam is the player's first *big win*. Right now it sits
> at the end of: catch a kin → hall errand → walk a whole route → fetch a key
> from an NPC → walk back → climb three floors → beat two trainers → beat the
> warden. That's a lot of homework before the first trophy. New players quit in
> the gap between 'I get it' and 'I won something.'"
>
> **Dee:** "It's a *loop*, though, and the loop is the game. Teaching the
> tease→errand→key→payoff grammar on the *first* Gleam means every later Gleam is
> legible. If the first one is handed over flat, you've taught nothing."
>
> **Mara:** "The level math needs the walk. Cut the loop and you're back to
> lv-5-vs-ace-10. The loop *is* the difficulty curve."
>
> **Grace:** "My worry isn't the loop's existence, it's its *length without a
> small win inside it*. The catch is a win. Is there a beat between 'get the
> wick-key' and 'beat the warden' that *feels* like progress? The two sight
> trainers on the stairs are it — but only if a first-timer can actually beat
> them. If they're a wall, the loop reads as a slog."

**Resolution:** Keep the loop — it's the right call and the vision rewards the
*walk*. But **guarantee the loop has internal wins** (the verge catch, a found
item on the coast, the first sight-trainer victory) spaced so the player is never
more than a few minutes from a hit of progress. **Tune the two beacon trainers
(Tansy/Cole, lv7–8) as confidence-builders, not gatekeepers.** (Finding F1.)

### Debate 3 — Two festivals in the first region: warmth or wallpaper?

> **Per:** "The Lantern-fair and the Tide-blessing are *both* in South, back to
> back. The first festival should be a lump-in-the-throat moment. If the second
> one a town later uses the same musical swell and the same flag-gated-townsfolk
> pattern, the player learns 'oh, this is just what winning looks like' — and
> the belonging beat becomes a UI convention."
>
> **Tomás:** "Arc E *wants* every town to have one, though. It's the spine's
> 'belonging not conquest' promise. You can't give the first region only one."
>
> **Junko:** "Then they have to *look and sound* unmistakably different. The
> Lantern-fair is warm amber and close; the Tide-blessing is cool moon-on-water
> and open. If the palette and the cue sell two different feelings, the pattern
> doesn't read as repetition — it reads as *a region with two moods*."

**Resolution:** Keep both (canon requires it). **Differentiate them hard on
palette, music register, and one signature interaction each** so the second
festival deepens rather than echoes (Finding F5). The vision's "delight" pillar
lives exactly here.

### Debate 4 — The dim-lamp opening vs. readability for a time-poor player

> **Grace:** "Lamplight tier one is 'Ember-glow — a candle's circle.' Cosy, yes.
> But our player is a tired adult who gets fifteen minutes. If hour one is also
> the *darkest* the lamp ever is, and they can't see the map, 'cosy' can tip into
> 'frustrating, where do I go.'"
>
> **Dee:** "The rule covers this — the critical path is *always* diegetically
> lit (lamp-posts, buoys, glowmoss), and South's overworld isn't even a 'dark'
> map; Lamplight's reveal-mask only applies to dark terrain like Tideglass
> Cavern. The opening town and coast are lit normally."
>
> **Grace:** "Then the risk is specifically the *first dark interior/landmark* a
> new player wanders into at Ember-glow with no frame of reference for why their
> sight is small. They won't read it as 'a tier' — they'll read it as 'broken.'"

**Resolution:** No change to Lamplight (it's additive/non-blocking by rule and
South's main path is lit). But **the first time the reveal-radius is ever small,
say so in one diegetic line** ("the lamp's young yet — it'll reach further as you
relight the sky") so a dim circle reads as *promise*, not *bug* (Finding F6).

---

## Part 3 — Findings & recommendations (prioritised)

Each finding: **what**, **why it matters to the vision**, **recommendation**,
and a **tag**. Ordered by impact on the first-hour experience.

### P0 — Address before the first hour ships as "representative"

**F0. Creature *battle* sprites are still placeholder squares. [BUILD GAP]**
Per `CLAUDE.md`, `CreatureSprites.ts` is unwired into title/starter/battle, so
the first wild battle, the starter, and Wren's partner currently render as
coloured boxes. The *entire* collecting/attachment pillar — the audit's reason
the game exists — does not yet visually land in the one place it matters most.
- *Why it matters:* Collecting is pillar #2; the first battle is the first
  promise of it. A box doesn't make a player fall in love with a kin.
- *Recommendation:* Wire `CreatureSprites` into the starter-select and battle
  scenes and ship at least the **hour-one cast** as real sprites — the three
  starters, the handful of South wild kin (Brinelet/Lumpin/Mooncatch/Glostern,
  #16/#10/#29 et al.), and Wren's starter. This is the highest-leverage visual
  fix in the project. **Junko** flags it as the panel's single biggest "the
  first hour undersells the game" item.

**F1. Guarantee internal wins inside the beacon loop; tune stair-trainers as
confidence-builders. [DESIGN]** (See Debate 2.)
- *Recommendation:* Audit the minute-by-minute reward spacing from
  `flag:caught_first_kin` to `beacon_battle`. Ensure a tangible win (catch /
  item cache / first sight-trainer KO) roughly every 2–3 minutes. Set Tansy/Cole
  to be beatable by a careful lv-7 starter-plus-one without grinding.

### P1 — High impact on first-hour quality

**F2. Earn 8–10 minutes of attachment before `dusk_begins`. [DESIGN]**
(See Debate 1.) The omen lands while Tinderwick is still a stranger.
- *Recommendation:* In the pre-omen window, give Tinderwick **one small, warm,
  specific human thread** the dark then threatens — the house parent/keepsake
  beat (S2 "A Letter for Fenn" already exists; consider surfacing its *opening*
  earlier), a named townsperson who reappears after the omen visibly shaken
  (the spine's "witness beat" pattern). Don't add plot; add a *face*.

**F3. Stagger the vocabulary load; give the vesperlamp a glossary. [DESIGN/UX]**
The first hour introduces, by the panel's count: *kin, Lumenary, Lampwarden,
Gleam, Lantern Gift, vesperlamp, kindling, Wayfaring, Skyweave, the Hollowing,
the Hearth,* and the *Lamplight* tiers. That's a lot of bespoke nouns for a
time-poor player who may return after a week away.
- *Why it matters:* The vision targets a player with *little time* and a *deep
  but specific* nostalgia. Re-teaching themselves the proper nouns each session
  is friction the cosy promise can't afford.
- *Recommendation:* (a) **Introduce terms only at first point of use** and never
  two new ones in the same line. (b) Add a **lightweight in-vesperlamp glossary**
  ("what was a Gleam again?") reachable from the pause menu — pure data, one
  entry unlocked per term as it's met. This *strengthens* the "the lamp is your
  companion device" fantasy rather than fighting it. **Grace** rates this the
  highest-value UX add in the opening.

**F4. The first hour leans on systems that aren't wired. Flag the dependency
loudly. [BUILD GAP]** Reyl (Pearlmoor, end of hour ~2) is written to lean on
`drench`/`doze`; the spine assumes **status conditions** and a **move-learn
prompt** are live from Pearlmoor on. Both are roadmapped, not built
(`battle-runtime-plan.md`).
- *Recommendation:* Treat status + the move-learn prompt as **first-arc blockers,
  not mid-game features** — they're needed *inside* the opening's second Gleam.
  Sequence them ahead of later content. Until then, ensure Reyl is winnable and
  legible without status (don't author a fight that *requires* `doze` before
  `doze` exists).

**F5. Make South's two festivals feel like two moods, not one template.
[DESIGN/ART/AUDIO]** (See Debate 3.)
- *Recommendation:* Lock distinct palettes (Lantern-fair = warm amber, close;
  Tide-blessing = cool moonlit, open), distinct music registers, and **one
  signature interaction each** (e.g. light-a-lantern vs. ring-the-bell, which
  the bell loop already gives you). Differentiate before the pattern repeats a
  third time in East.

### P2 — Polish that compounds

**F6. The first small reveal-radius needs one diegetic line of framing.
[DESIGN/UX]** (See Debate 4.) Make a dim lamp read as *promise*, not *bug*.

**F7. Two route-back errands in a row may read as one trick twice. [DESIGN]**
Both Gleams in South use the same loop *shape*: a warden asks → you fetch
something from **one screen back on the route you just walked** → you return.
Beacon = wick-key from Dimglass I; bell = net-floats from Dimglass II. The spine
*intends* shape variation across regions, but South's own two are nearly
identical grammar.
- *Recommendation:* Keep both (collinearity is a binding rule — errands must
  reuse walked ground). But **vary the verb**: the beacon is an ascent; let the
  bell loop *feel* like a different action (a breakwater walk over water with its
  own hazard/rhythm), not a second fetch-and-return. The bell loop's net-hand
  trainers and the seaward walk already help — lean into them so the player reads
  "a different kind of errand," not "the same errand by the sea."

**F8. Confirm every first-hour verb is first-class on touch. [UX/MOBILE]**
The vision is web-first, *mobile-ready as the same build*. The opening teaches
move/talk/interact/catch/menu — all must be taught in a way that reads identically
on a touch shell, not keyboard-first with touch bolted on.
- *Recommendation:* Walk the entire first hour on a touch shell and confirm:
  sign-interact, the catch throw, menu navigation, and the cutscene-skip (Cancel)
  all have an obvious, discoverable touch affordance. The `KEY_HINTS` ↔
  InputController sync (`CLAUDE.md`) is the place this drifts.

**F9. Wren's A2 battle is the first *trainer* fight — make sure it teaches, not
just happens. [DESIGN]** Wren is ~2 levels under the player and frames the fight
as "no Lamps, no stakes." Good. But it's also the player's first exposure to an
opponent *switching* and to type matchups under pressure.
- *Recommendation:* Make Wren's team a clean, *legible* teaching board — a single
  partner whose type the player's starter clearly beats or loses to, so the
  triangle clicks through play, not a menu. The low stakes are the safe place to
  let the player *feel* super-effective for the first time.

**F10. Audio: protect the first `blip` and the first Gleam swell. [AUDIO]**
**Per** flagged that the area music must ship in the richer `snes` register (per
`CLAUDE.md`), and the cold open / Gleam cues are the emotional spine of the hour.
- *Recommendation:* Prioritise, in order: (1) the UI confirm/cancel *blip* (the
  nostalgia tell fires on literally every menu press), (2) the catch/Lamp sfx,
  (3) the `gleam-emotional` swell, (4) the `coldopen-foreboding` cue. Everything
  else can lag; these four *are* the first hour's sound.

---

## Part 4 — Risk register & open questions

| # | Risk / question | Owner | Status |
|---|------------------|-------|--------|
| R1 | First battle renders placeholder squares (F0) | Art + Engine | **Open — P0** |
| R2 | Status + move-learn unbuilt but assumed by Gleam 2 (F4) | Engine | **Open — P1** |
| R3 | Vocabulary load may exceed a returning time-poor player (F3) | UX + Writing | Open — P1 |
| R4 | `dusk_begins` may outrun the player's attachment (F2) | Narrative | Open — debated, P1 |
| R5 | South's two loops share a shape (F7); does it generalise to East? | Level design | Open — P2 |
| Q1 | Where do we *officially* draw "the first hour"? Panel recommends **the Ember Gleam**. | Production | Decision needed |
| Q2 | Is starter-choice's *art* (the three on the logo) ready, or also placeholder? | Art | Verify (ties to F0) |

**Things the panel explicitly did NOT recommend changing** (to prevent
well-meaning drift): the early placement of the inciting incident; the existence
of the beacon/bell earned loops; the 10-type chart and mirror-axis reservations;
the catch math; save-anywhere; Lamplight's dim opening; or any canon vocabulary.
All of these are *working as the vision intends* — the recommendations above
deepen them, they don't replace them.

---

## Part 5 — Verdict

> **Ivo (closing):** "The bones are excellent and they're *the right bones for
> the game we said we were making.* The first-hour blueprint understands its
> player — the tired thirty-something who wants the 1999 feeling back — and it
> serves all four pillars: nostalgia in the register, collecting in the catch
> loop, exploration in the Tidecall reopening, delight in the festivals. The work
> that remains is **not redesign, it's realisation**: get real creature sprites
> into the first battle (P0), wire the systems the second Gleam already leans on
> (P1), and lighten the cognitive and pacing load around an otherwise strong
> opening (P1/P2). Do those and the first hour will do the one job a first hour
> has — make the player want the second."

**One-line summary:** *A genuinely well-designed cosy opening whose biggest risks
are build-state gaps (placeholder battle sprites; unbuilt status/move-learn) and
a few pacing/load refinements — not its design, which is on-vision and should be
protected.*

---

### Appendix — Findings at a glance

| ID | Finding | Tag | Priority |
|----|---------|-----|----------|
| F0 | Wire real creature battle sprites for the hour-one cast | BUILD GAP | **P0** |
| F1 | Internal wins inside the beacon loop; stair-trainers as confidence | DESIGN | **P0** |
| F2 | Earn attachment before `dusk_begins` | DESIGN | P1 |
| F3 | Stagger vocabulary; add a vesperlamp glossary | DESIGN/UX | P1 |
| F4 | Sequence status + move-learn ahead of Gleam 2 | BUILD GAP | P1 |
| F5 | Differentiate South's two festivals (mood, not template) | DESIGN/ART/AUDIO | P1 |
| F6 | Frame the first small reveal-radius diegetically | DESIGN/UX | P2 |
| F7 | Vary the *verb* of the two South earned loops | DESIGN | P2 |
| F8 | Confirm every first-hour verb is first-class on touch | UX/MOBILE | P2 |
| F9 | Make Wren's A2 battle a clean teaching board | DESIGN | P2 |
| F10 | Protect the first blip + the Gleam swell in audio priority | AUDIO | P2 |

*Prepared by the convened first-hour panel. Measured against `VISION.md` and the
`CLAUDE.md` Game canon; no recommendation herein requires a canon change.*
