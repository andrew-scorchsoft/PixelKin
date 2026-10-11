# PixelKin — Story Depth Panel (2026-10)

> A convened review of the **built story**, from the cold open to the Starfall, asking the
> owner's question: *is it dark and compelling all the way through, written to the standard of
> the great 16/32-bit-era story RPGs, and does it pull a millennial player on to the next stage?*
> The panel also asks a narrower question: **are the falling stars underused?**
>
> **Scope read:** `VISION.md`, `docs/world/story-bible.md`, `docs/world/cinematics.md`, the
> walkthrough spine + `01-south` (S4/S5), `06-postgame` (arc resolutions, Starfall),
> `08-the-peril-thread.md`; and the **shipped words**: `content/cinematics.ts` (cold open,
> ending), `content/scripts.ts` (the opening, `dusk_begins`, `give_wick`, every Gleam ceremony,
> `glowmoss_drained/relight`, `cor_appears`, `fenn_shared_past`, `wren_*`, `hollowfen_stillworks`,
> `great_null_named`, `fenn_counsel`, the acolytes, the summit chain, Dawnstead, the peril
> thread, S4/S5), `content/dialogue.ts` (pinned letters, Fenn C2, Wren A1–A3, Còr's quiet cast),
> `content/glossary.ts`, `content/portraits.ts`, `entities/Actor.ts` (emotes/actions) and the
> `CutsceneRunner` op list.
>
> **Hard constraint honoured throughout:** the path from New Game to the **Chickenpig** (S4,
> Pearlmoor breakwater) stays tutorial-length. Every South item below is a **line swap,
> an `if_flag` variant, or an optional NPC**. None adds a required step, page or input. §4.1
> proves this item by item.
>
> No other franchise is named. Craft is described by technique only.

---

## The panel

| Panellist | Lens | Asks |
|---|---|---|
| **Ines Calloway** | Scenario director: structure, acts, reversals | "Where does the story *turn*? What does the player lose?" |
| **Tobiah Rusk** | Character writer: arcs, wounds, motive | "Why does *this* person do *this*, and when did we learn it?" |
| **Hanne Okafor** | Dialogue and localisation-voice editor | "Does every line earn its page? Does each voice stay distinct?" |
| **Mikkel Strand** | World and lore designer: motifs, causality, timeline | "What do the objects *mean*, and do the numbers agree?" |
| **June Barrow** | Player experience and pacing: first-timers, older players | "Can Paul, aged 80, follow it, and will a tired 38-year-old press on?" |

---

## 1. The rubric

Ten criteria, each scored 1–10. The "9" column describes the bar that the era's best story
RPGs cleared.

| # | Criterion | What a 9 looks like |
|---|---|---|
| R1 | **Hook & inciting incident** | Within the first few minutes the player has felt a specific, personal wrongness, not just been told about a general one. One image they will still remember at the credits. |
| R2 | **Stakes & escalation** | The threat is causally legible: the player knows *what* is wrong, *who* is doing it, and *how*. It gets worse in steps the player can feel, with at least one moment where something the player made or loved is put at risk. |
| R3 | **Antagonist depth** | The antagonist has a wound, a philosophy and a cost. He is half-right in a way the player can't dismiss, and he is seen often enough to grow, not only at milestones. |
| R4 | **Mentor & rival arcs** | Each has a private wound planted early and paid off late. Their turns are motivated on-screen, and objects or lines planted in act one come back changed in act three. |
| R5 | **Emotional set-pieces & staging** | The big scenes are *performed* as well as narrated: sprites move, turn away and pause, and music and silence carry the weight. The player remembers the staging, not only the words. |
| R6 | **World tells story & motif** | The map itself testifies: marks, objects and recurring images (here, lanterns and falling stars) build meaning region by region, and the motif's final appearance reframes every earlier one. |
| R7 | **Dark-theme consistency** | Melancholy is sustained, not spiked. Humour sits in its own rooms and never steps on a grief beat. Hope is earned against a dark that stays real. |
| R8 | **Dialogue voice** | Every named character could be identified with the name tags hidden. There are no tics repeated across speakers, and emphasis is rationed. |
| R9 | **Ending payoff** | The climax answers the opening's question in the opening's terms. The epilogue lets the cast exhale, and nothing important is said twice. |
| R10 | **Pull-through** | Each region ends on an open question or image that makes "one more area" feel necessary, and the player always carries a mystery they want answered. |

---

## 2. Panel scores and debate

### 2.1 Individual scores

| Criterion | Calloway | Rusk | Okafor | Strand | Barrow | **Mean** |
|---|---|---|---|---|---|---|
| R1 Hook | 7 | 7 | 8 | 6 | 8 | **7.2** |
| R2 Stakes & escalation | 5 | 6 | 6 | 4 | 6 | **5.4** |
| R3 Antagonist | 8 | 9 | 8 | 7 | 8 | **8.0** |
| R4 Mentor & rival | 7 | 6 | 7 | 7 | 7 | **6.8** |
| R5 Set-pieces & staging | 8 | 7 | 8 | 7 | 7 | **7.4** |
| R6 World & motif | 6 | 6 | 6 | 5 | 7 | **6.0** |
| R7 Dark consistency | 6 | 7 | 6 | 6 | 8 | **6.6** |
| R8 Dialogue voice | 8 | 8 | 7 | 8 | 8 | **7.8** |
| R9 Ending payoff | 8 | 8 | 7 | 7 | 8 | **7.6** |
| R10 Pull-through | 6 | 6 | 6 | 6 | 5 | **5.8** |
| **Overall** | 6.9 | 7.0 | 6.9 | 6.3 | 7.2 | **6.9** |

### 2.2 What each panellist saw

**Calloway (structure).** *"The game has an excellent second act and a soft middle hinge."*
The B-arc escalation is honest (rumour → drained site → Còr → Stillworks → Null), and
`cor_appears` is the best-written scene in the game. But the story never **turns against the
player**. Every beat is something the player fixes, and no relit light is ever put back at
risk. In the era's great scenarios, the middle of the game takes something you were sure of.
Here, the closest thing is Wren walking off in the snow. *"Show me one night where the
player's own Ember stutters."*

**Rusk (character).** *"Còr is a 9. Wren is a 6 because Wren has no wound."* Every Spire
acolyte has a specific grief: Merrin's wicks, Tace's ferry, Ivorwen's four winters, Harl's
eight lamps, Sefa's north roads. Those five little scenes are the most era-true writing in the
build. Wren, the character the player spends the most time with, wobbles towards the Hollowing
for no reason we are shown: *"I keep doing the sums"* is an argument, not a wound. And Fenn's
C3 line *"we lost the same thing, in the same season. I will not tell you what"* is a promise
**the game never keeps**. A withheld secret that is never paid is a debt, not a mystery.

**Okafor (voice).** *"Lovely sentences, too many of them shaped the same way."* The best lines
land hard: Wendel's *"I've had a lifetime. It isn't."*, the glacier widow, Còr's *"a lamp asks
to be WATCHED"*, the Stillworks gauge *"Zero is what the light comes to."* But "held breath"
appears **15 times** across the content files, "weighed" 22 times (nearly every keeper's
intro), "courteous" 10 times, and capitals for emphasis appear in almost every scene. The
ending says *"not in a victory — in a morning"* twice within thirty seconds (`dawn_breaks`,
then `ENDING_CREDITS` panel 4). There are also **portrait bugs** that flatten key beats. Wren's
`soft` expression doesn't exist (two lines in `wren_nightreach` fall back to neutral). Reyl's
`grave` doesn't exist (`reyl_quest`). Nessa's whole `great_null_named` speech has no portrait
at all, although the comment above it promises her "haunted portrait-register". Otho, the
designed difficulty wall, has no portrait.

**Strand (lore).** *"The game never shows the player its own cause and effect."* Canon
(story-bible §3) says the Hollowing harvest kin light into null-lanterns, and that this is
what darkens the constellations. On screen, that link is stated **once**, by an unportraited
optional NPC on the flats (`npc.flats_sky_watcher`: *"snuff a kin's light and a star goes dark
with it"*). When the player wakes the Fennlight, no star returns. When the Null is named, no
one says where the falling cinders go. The falling stars are the best new image in the game,
but they appear in only two places (orchard, Hushfrost), plus a LORE line promising *"every
fall lands nearer the mountain"*, and **the mountain never answers that promise**. Four
separate "fallen sky" objects also don't know about each other: Dusk cinders, Starglass Shards
(sold for 1,500w as loot), the Starwell's *"star fell and did not go out"*, and the post-game
star-shards. The timeline drifts too: Fenn's "forty years" on the ladder, Còr's "twenty years"
of not looking, Reyl's "eleven winters" of the Dusk, Nessa's "two years" of scaffolding, and
"third star this month" against the lamplighter's "third one this season".

**Barrow (players).** *"Paul will be fine, and that's the achievement to protect."* The
opening is gentle: an optional tutorial offer, the gate-warden walking you back a step, Fenn
waving you over, and the orchard crater as the one mandatory dark image. That last is a
superb choice, because everyone sees it. `dusk_begins` is short and staged. Barrow's worries
are elsewhere. For a first-timer, **pull-through** drops at every crown hand-off: Gleam
ceremonies end with directions ("Galehigh's up the deep galleries"), not a question. And
much of the acting is **narrated rather than performed**: *"He presses your shoulder once,
the way he did at the waystone"* recurs three times, but the waystone scene never shows it.
Older players read every page, so a line describing an action they never saw costs trust.

### 2.3 The debate

**D1. Should the Hollowing *cause* the falling stars?**
- *Strand:* "Yes. Make the Great Null pull guttered stars down, so the orchard is Còr's doing.
  Then the motif has teeth."
- *Rusk:* "No. That makes the gentlest man in Vesperholm an orchard-burner. You'd trade a
  9-rated antagonist for a cause-and-effect diagram."
- *Calloway:* "Then keep the culpability **indirect**, which is what canon already says. Sleeping
  kin starve their stars, starving stars gutter, and some of what gutters falls."
- **Resolution (unanimous):** the falls are *consequences*, not weapons. They land nearer the
  mountain because guttered light goes **home to the Keystar**, the anchor it was lit from. Còr
  doesn't make them fall. He **walks out and fetches them**, a mourner gathering graves. The
  player's horror is not "he did this" but "he is *keeping* them". (Full proposal in §5.)

**D2. Is the comedy a tonal problem?** (The Old Light's joke-tower, the Booji-Wooji Man, Wink,
the sunshine-goth dragon-cat.)
- *Calloway:* "The era's best dark stories were full of farce. Comedy isn't the problem;
  *adjacency* is."
- *Barrow:* "The Old Light is the one comic quest on the required Tide path, and it's seven
  floors. Don't add a word to it."
- *Rusk:* "Every comic quest already has a grief core: Tam's unfinished joke card, Paul's dark
  lamp, Reyl's eleven winters. That's correct. Protect the core."
- **Resolution:** comedy stays. Two rules apply: no joke within a screen of a "light fails"
  beat, and every comic quest keeps one sincere line at its centre. Nothing new is added to
  the Old Light.

**D3. Does the midgame need a real reversal?**
- *Calloway:* "Take a Gleam away. Let a town the player saved go quiet."
- *Barrow:* "Taking things away from an 80-year-old who played for twenty hours is cruel, and
  it breaks 08's binding rule that your light heals."
- *Strand:* "Then make it **the Keystar faltering**, not Còr striking. The youngest star, which
  is yours, slips first. It's reversible, but the player watches the thing they made go dark
  for a heartbeat."
- **Resolution:** a reversible flicker (item W-1), followed by witnesses at home in Tinderwick.
  The dark gets a moment of real power without punishing anyone.

**D4. Should the Fenn–Còr loss be named?**
- *Strand:* "Naming it shrinks it."
- *Rusk:* "Never naming it means a promise broken in the last act. The era's best reveals were
  paid with an **object** planted hours earlier. The Starlamp is already that object. Fenn
  kept it 'forty years for one particular asking', and nobody asks why."
- *Okafor:* "Pay it in three small doses: a pronoun in the North, a question in the West, the
  object at the summit. Say the name only after dawn."
- **Resolution:** item X-1 (Senna and the Starlamp).

**D5. How much darker can the South get without getting longer?**
- *Barrow:* "Net-zero pages pre-Chickenpig. Swap, don't add."
- *Calloway:* "Then spend the swaps on three things: the falling motif in the cold open, Wren's
  wound, and the orchard echoed at the dusk omen."
- **Resolution:** items S-1 to S-3, with page counts proven in §4.1.

---

## 3. Consolidated verdict

**Overall 6.9 / 10. The prose is beautiful and the antagonist is excellent, but the darkness is
described more than suffered.**

What is already at the era standard (keep it, and protect it from "improvement"):
- **Còr** (`cor_appears`, `warden_cor_final`): grief dressed as mercy, written as an argument
  the player half-loses. The out-remembering is a genuine thesis climax.
- **The Spire acolytes**: five griefs in five fights. This is the strongest "every enemy is a
  person" sequence in the build.
- **The peril thread's faces**: Wendel, Tamsin, the fen mother, the quiet father, the ledger.
  Each one *heals* on a Gleam, which is exactly right.
- **Set-piece cadence**: silence → sting → tint → swell is applied consistently. The Pale Vault
  seven brackets and the Aurora-watch are quietly superb.

What holds the story below a 9:
1. **The cause is invisible.** The player is never shown that sleeping kin darken stars (R2, R6).
2. **Nothing is taken from the player.** The story has no turn against them (R2).
3. **Debts are never paid.** The Fenn–Còr secret is withheld, Wren has no wound, and the
   "nearer the mountain" promise goes unanswered (R4, R6).
4. **Acting is narrated.** 991 `say` steps sit against 4 `move` ops, 22 emotes and **one**
   `action`, and the player's action sheet (raise-lamp, gift, sit) goes unused (R5).
5. **Region exits close instead of open** (R10).

The fixes are cheap. Most are **line swaps and data**, and nothing below needs engine code
except where flagged.

---

## 4. Ranked improvements

### 4.0 Master ranking

Pre-CP means the item touches the path from New Game to the Chickenpig. Each region's
implementer takes their group from §4.2 onward.

| Rank | ID | Region | What | Effort | Pre-CP? |
|---|---|---|---|---|---|
| 1 | C-1 | Central | **The Cinder Hoard**: the falling-star payoff at the Spire, and the cinders waking at the relight | L | no |
| 2 | E-1 | East | **Show the cause**: waking the Fennlight brings a star back; the Hollowing drop a cinder | M | no |
| 3 | W-1 | West | **The Ember flickers**: the Keystar falters and the player's first Gleam goes dark for a heartbeat | M | no |
| 4 | X-1 | Cross | **Senna and the Starlamp**: pay off the Fenn–Còr loss through a planted object | M | no |
| 5 | N-1 | North | **Còr carries a cinder** at B3: the antagonist and the motif meet | S | no |
| 6 | S-1 | South | Cold-open line swap that plants the falling stars on frame one | S | **yes, net 0** |
| 7 | S-2 | South | Seed **Wren's wound** (Mum's quiet village) in one swapped line | S | **yes, net 0** |
| 8 | X-2 | Cross | **Sprite-acting pass** on 12 key scenes (face, emote, wait, player `raiseLamp`) | M | **yes, net 0 pages** |
| 9 | S-3 | South | Fix the `dusk_begins` voice slip and echo the orchard | S | **yes, net 0** |
| 10 | X-3 | Cross | Portrait fixes (Wren `soft`, Reyl `grave`, Nessa unportraited) plus an **Otho portrait** | S / M (art) | yes (Reyl fix only, 0 pages) |
| 11 | X-4 | Cross | **Crown interludes**: a short "meanwhile, at the mountain" vignette at each region seam | M | no |
| 12 | W-2 | West | Còr's **wordless West sighting** and cinder chips in the Stillworks lanterns | S | no |
| 13 | X-5 | Cross | **Phrase budget** pass (held breath / weighed / courteous / caps) and the Gleam refrain made deliberate | S | yes (swaps only) |
| 14 | S-4 | South | Upgrade **Fenn C2** on the flats: portrait plus the kin⇄star law said plainly | S | optional NPC |
| 15 | E-2 | East | Wren A3 staged, with Mum's letters | S | no |
| 16 | E-3 | East | Cinderhead: **Harl's eight door-hooks** and a cinder under the roof-fault | S | no |
| 17 | N-2 | North | Fenn C3 admits **"there were three of us on that ladder"** | S | no |
| 18 | N-3 | North | Wren A4 performed (turns away, sits) and names her mother | S | no |
| 19 | N-4 | North | One **live fall** across the Kite-rising sky, towards the mountain | S/M | no |
| 20 | W-3 | West | Nessa's question about "the third ladder" and the Ledger's **FELL** column | S | no |
| 21 | W-4 | West/North | Optional quest **"The Pass-walker's Map"**: plot the falls and find they converge | M | no |
| 22 | X-6 | Cross | **Timeline sheet**: reconcile 40 / 20 / 11 / 2 years and "this month" vs "this season" | S | yes (1 swap, inside S-3) |
| 23 | C-2 | Central | Dedupe the "not a victory, a morning" line; let the Null glow faintly at dawn | S | no |
| 24 | P-1 | Post-game | Còr's cinder **wakes gold** at Dawnstead; Fenn says Senna's name in the Last Lesson; Starfall contrast line | S | no |
| 25 | S-5 | South | Place the two **deferred peril placements** (S2 neighbour, S3 harbour notice) | S | optional |

**Per-region counts:** South 5 · East 3 · North 4 · West 4 · Central 2 · Post-game 1 ·
Cross-cutting 6 (= 25). Cross-cutting X-1 is executed as lines inside N-2, W-3, C-1 and P-1,
so those owners carry its words.

### 4.1 The Chickenpig budget: proof that pre-CP items add nothing required

The required path to the Chickenpig runs: cold open → Tinderwick → gate-warden →
Crossroads/Fenn → orchard satchel (orchard first-sight) → `intro_mentor` → verge catch →
Brisa → Dimglass I (Wren A2, `dusk_begins`, lamplighter) → Beacon → Dimglass II → Pearlmoor →
Reyl hook → Old Light → netmender → Lifting House → Paul → catch.

| Item | Scene touched | Required? | Pages before → after | New input / step? |
|---|---|---|---|---|
| S-1 | `COLDOPEN_SOUTH` beat 2 | yes (skippable) | 2 → 2 (line rewrite) | none |
| S-2 | `script.wren_dimglass` closing line | yes (sight trainer) | 1 → 1 (line rewrite) | none |
| S-3 | `script.dusk_begins` narrate 3 | yes | 3 → 3 (line rewrite) | none |
| X-2 | `intro_mentor`, `dusk_begins` | yes | intro_mentor 11 → 11 (merge two `say`s, add one narrate); dusk_begins 3 → 3 | none. Adds about 1.5 s of `face`/`wait` ops in total |
| X-3 | `reyl_quest` expr | yes | 0 change | none |
| X-5 | any South swaps | mixed | swap-only, never +pages | none |
| S-4 | `npc.flats_sky_watcher` | **optional** NPC | 2 → 3, optional only | none |
| S-5 | two new NPC/sign placements | **optional** | optional reads | none |

**Rule for South implementers:** a required South scene may change *words*, never *count*.
If a line is added, another is merged. Nothing is added to the Old Light or the Lifting House.

### 4.2 SOUTH (texture only before the Chickenpig)

**S-1 · Plant the falling stars on frame one** · `cinematics.ts` `COLDOPEN_SOUTH` beat 2 · S · pre-CP, net 0
*Why:* the game's best new image (a star that falls and burns an orchard) currently starts at
the orchard. The cold open should promise it, so that the orchard *confirms* it.
Replace the first line of beat 2:
> *"Then, one by one, the lights began to go out. Some only dimmed. Some, going out, fell."*

Optional, same page count: in beat 3, *"a child wakes to their Wayfaring"* →
*"a child wakes to their Wayfaring, a dead lamp-trimmer's brass in their pocket"*. This pays off
Gran's grandfather line (`npc` Gran, *"that old brass trimmer in his coat"*) for anyone who
talks to her.

**S-2 · Seed Wren's wound** · `script.wren_dimglass` (closing `say`) · S · pre-CP, net 0
*Why:* Wren's later wobble (A3/A4) has no personal cause. The ending already pays one off
that was never planted: *"A rival lit out for the coast road, to see a particular harbour in
daylight."* Replace *"Same road, different lamps. See you up the coast!"* with one page:
> **WREN** (neutral): *"Same road, different lamps. Mine runs on north — Mum's village is past
> Pearlmoor, and her letters have gone very short. See you up the coast!"*

**S-3 · Fix the omen's voice and echo the orchard** · `script.dusk_begins` narrate 3 · S · pre-CP, net 0
*Why:* *"That's the third star gone south of here this month"* is a person's speech in the
narrator's mouth, and it contradicts the lamplighter's *"third one this season"* (X-6). Every
player has already seen the crater (the satchel errand), so cash that image in. Replace with:
> *"You think of the orchard — the scorched ring, the cold stone in the ash. This one did not
> fall. Not this time. The Long Dusk is deepening, and it is coming closer."*

**S-4 · Make Fenn's C2 the law of the world** · `dialogue.ts` `npc.flats_sky_watcher` · S · optional NPC
*Why:* this is the only place the kin⇄star causality is stated, and it's unportraited and
throwaway. Add `portrait:'fenn'` (grave → warm) and the following lines (2 pages → 3, optional
talk only):
> **FENN** (grave): *"You saw it go. Then hear the old law plainly, child, because nobody says
> it plainly any more: every star up there has a kin down here carrying its spark."*
> **FENN** (grave): *"Put that kin to sleep and its star goes hungry. Starve a star long enough
> and it gutters — and sometimes what's left of it falls. Wendel's orchard was one."*
> **FENN** (warm): *"So we walk the other way. Wake what sleeps; relight what gutters.
> Pearlmoor keeps the second Gleam."*

**S-5 · Place the deferred peril beats** · `tinderwick` (`peril_neighbour`), `pearlmoor_quay`
(`sign_peril_pearlmoor_board`) per 08 §4 · S · optional
*Why:* the words are written and good (*"We look like a festival that forgot to start"*).
Placing them gives the South its own witnesses. The Pearlmoor notice (*"The villagers are
reported well. And very quiet."*) becomes **Wren's mother's village** once S-2 lands. Consider
one added line on the notice, `if_flag: flag:wren_dimglass_battled`: *"Among the listed
villages, one has been underlined twice, in pencil, by a different hand."*

### 4.3 EAST

**E-1 · Show the cause: a star comes back** · `script.glowmoss_relight` (+ a cinder object and
interact line at the drained site) · M · post-CP
*Why:* this is the first time the player undoes the Hollowing, and the game's law (S-4) should
become *visible* here. Insert after the Fennlight lifts (Glowmoss is a cave, so stage it
through a root-gap, as Cinderhead does with its roof-fault):
> *narrate:* *"Far above, through a split in the roots where the wood lets in the night, a
> small star you had not noticed was missing comes back — faint, then certain."*

and after the acolytes leave:
> *narrate:* *"Something drops from the last bundle as she goes: a dark stone the size of a
> plum, cold, faintly blue in its cracks. She does not come back for it."*

New interact (a `fallenstar_cinder_star` object reusing the orchard art): *"A star-cinder, like
the one in Wendel's orchard. The Hollowing were carrying it somewhere — carefully, the way you
carry something you mean to bury."* This is the first link between the Hollowing and the falls.

**E-2 · Wren A3 with a reason** · `npc.wren_glowmoss` → promote to a short script with sprite
acting · S
Replace line 3:
> **WREN** (unsure): *"...What if they're not wrong? Mum's village went quiet in the spring.
> She writes that nobody's hurt. She writes that it's peaceful. She used to write PAGES."*

Staging: `face wren up` (looking at the grey moss), `wait 600`, `emote ellipsis`, then the line.

**E-3 · Cinderhead: Harl's eight hooks and the roof-fault cinder** · `cinderhead` town plus
Otho's hall · S
*Why:* acolyte Harl (*"Carried my crew's lamps home the bad year — all eight of them"*) is a
Cinderhead man, but Cinderhead never mentions him. Plant it: eight brass door-hooks in a row
on one cottage terrace, seven with lamps and one empty, and a sign: *"The Grist-Gallery
crew. We dim for them at the Lamp-down. Harl keeps his own vigil, elsewhere."* At the Spire,
the player then recognises Harl. Separately, in `lumenary_cinderhead` the Stone Gleam is seen
*"through a fault in the cavern roof no miner ever marked"*. Put a small cinder at that fault's
foot (decal only), with a miner line: *"Came down through the fault the winter the bad year
started. We don't move it. Seemed rude."*

### 4.4 NORTH

**N-1 · Còr carries a cinder** · `script.cor_appears` · S
*Why:* this is where the antagonist and the motif should touch for the first time. Insert
before *"No — I will not fight you"* (the player now knows cinders from E-1):
> *narrate:* *"He turns something over in his gloved hand — a dark stone, cracked, faintly blue
> along the seams."*
> **CÒR** (gentle): *"They fall nearer every year, did you know? Nearer the mountain. Guttered
> stars, going home to the one light that still remembers them. I walk out and fetch them,
> when I can. Somebody ought to sit with them."*

Sprite: Còr `face` toward the dark valley during the line, back to the player for the
question.

**N-2 · Fenn C3: "three of us on that ladder"** (X-1 dose 1) · `script.fenn_shared_past` · S
Replace *"And then we lost the same thing, in the same season. I will not tell you what…"* with:
> **FENN** (grave): *"There were three of us on that ladder, once. Then there were two — and a
> star missing from the sky that we had named together. I will not tell you more. It is half
> his grief, and I do not lend out what is half another man's."*

**N-3 · Wren A4, performed** · `script.wren_pale_vault` · S
After the battle, in place of the narrated *"Wren looks at the undercroft door…"*:
`face wren up` → `wait 900` → `face wren left` → `emote ellipsis`, then:
> **WREN** (unsure): *"Mum's well, you know. Everyone in her village is well. Nobody there has
> lit a lamp since spring, and nobody minds. ...I mind. I think I mind."*

then the existing *"I need to walk a while."* and a `move wren` off-screen (the first time Wren
is *seen* to leave rather than told to).

**N-4 · One live fall** · `script.galehigh_kite_rising` · S/M
*Why:* every fall so far is aftermath. Show one happening, at the warmest festival, so it hurts.
At the crest of the Kite-rising: `flashColor #cfe8ff 200` → `cameraFocus` towards the
mountain (an off-centre `to` tile) → narrate:
> *"A streak of cold light crosses the whole sky above the kites, silent, and goes down
> somewhere past the north ridge — towards the mountain. Every kite-tail on the hill dips at
> once, as if the wind flinched."*

Then a single child's line: *"Was that one of OURS?"* The music doesn't stop. That is the cruelty.

### 4.5 WEST

**W-1 · The Ember flickers** · `script.great_null_named` (+ 3 Tinderwick witness stages keyed
`flag:great_null_known`) · M
*Why:* this is the story's turn against the player (D3). Insert after *"…aimed at the Keystar…"*
and before Nessa's *"I knew him, once"*:
> `silence 1200` → *narrate:* *"Far to the south, low on the rim of the world, the Ember — your
> first Gleam, the one you watched Brisa wake — stutters. Dims. Is gone for one long heartbeat."*
> `sfx world-star-gutter`, `tint #0b1026 0.5`, `shake 300`
> *narrate:* *"Then it catches again."*
> **NESSA** (haunted): *"The Keystar slipped. Only for a breath — but every star leans on it, and
> when it slips, the youngest slip first. Yours is the youngest in the sky."*

Witnesses (S-sized, post-CP): Brisa (*"The beacon went out on its own last night, for a breath. I
relit it with my hands shaking."*), Tamsin (*"The stone in the burn went cold again. Just for a
minute. Grandad sat down."*), the Tinderwick neighbour (*"Window lamps back in every house.
Don't tell me why. I know why."*). Under 08 these heal at `gleam:lunar`.

**W-2 · Còr in the West, wordless** · `hollowfen_stillworks` (+ one `npc` figure) · S
*Why:* Còr vanishes between the North and the summit, so give him one silent appearance. At the
Stillworks band, after the gauge line: `cameraFocus` a far gantry, where a cowled figure is
`move`d two tiles sweeping, stops, `face`s the player, bows (`wait 800`) and walks out of frame.
No words. Add to the lantern description:
> *"Each null-lantern's collar holds a chip of dark stone, cold, faintly blue in its cracks. Not
> fuel. Company."*

**W-3 · Nessa's question and the Ledger's second column** (X-1 dose 2) · `great_null_named`, `script.peril_ledger` · S
After *"I knew him, once. He was the gentlest of us."*:
> **NESSA** (haunted): *"Ask Fenn about the third ladder. ...No. Don't ask. He'll tell you when
> he can bear to."*

Ledger, stage `flag:great_null_known`: *"There's a mark I've started making beside some of the
names. FELL. Thirty-one of them, so far. All since the Dusk. All nearer the mountain."*

**W-4 · "The Pass-walker's Map"** (optional side quest) · `hushfrost_pass_i` pass-walker +
interact marks at known craters (orchard, Cinderhead fault, the Galehigh fall from N-4, Hushfrost,
Coldfog) · M
*Why:* this gives the motif a **collectible loop** without a new item system (flags only, the
P3 survey pattern). Each crater visited sets `flag:fall_seen_<n>`. With three or more, she
spreads the map: *"Draw a line through them. Go on. ...It's not a line. It's a spiral, and the
middle of it is the Spire."* Reward: one Starglass Shard and a LORE unlock (*"The Spiral of
Falls"*). This item is the motif's "aha" moment, ahead of the C-1 reveal.

### 4.6 CENTRAL

**C-1 · The Cinder Hoard** (rank 1) · a re-dressed Spire chamber (flag-free decor + signs) and
`script.keystar_relight` · L
*Why:* the LORE has promised since the orchard that *"every fall lands nearer the mountain"*.
The mountain must answer. Re-dress one mid-Spire gallery with rows of cinders on swept linen,
each with a paper tag (sign triggers). Band narration:
> *"Rows of dark stones on clean linen, each with a paper tag in a careful hand.
> DUSKAPPLE ORCHARD. HUSHFROST, FOURTH FALL. GALEHIGH, KITE-RISING NIGHT. Dozens. You find
> Wendel's without looking for it."*
> **WREN** (if joined): *"He's been... collecting them. Like a churchyard. ...He sweeps in here
> too, look."*

Then in `keystar_relight`, after *"The Keystar CATCHES"*:
> *narrate:* *"Far below, in the swept gallery, every cold stone on the linen begins — all at
> once, quietly — to glow."*

That one line reframes every crater in the game: they were never dead, only guttered.

**C-2 · Dedupe the morning, and let the Null stir** · `script.dawn_breaks` · S
Cut *"Not into a victory — into a morning. Dusk will come again…"* from `dawn_breaks`, because
the credits panel says it better thirty seconds later. Replace it with an image:
> *narrate:* *"Behind you, the Great Null stands silent in the first light — and deep in its
> cold housing, where he packed the fallen ones close, something answers the sun."*

This keeps the post-dawn **Nullmajor** (`script.nullworks_nullmajor`) consistent.

**X-1 dose 3, at the summit (Senna and the Starlamp)** · `script.keystar_relight`, between
the catch and Còr's *"There it is…"* · S
> *narrate:* *"Còr is staring at the empty starlamp in your hand."*
> **CÒR** (sorrowful): *"That cell. I know that brass. She filled it the winter we were
> apprentices — 'for the night we'll need it,' she said, and Fenn and I laughed at her."*
> **CÒR** (sorrowful): *"She kept the Ninth Lantern twenty years. The winter it failed, I sat by
> her lamp while it burned down, counting its hours and calling it hope."*
> **CÒR** (at_peace): *"...And he kept her light all this time, to spend on a morning. Of
> course he did."*

The second line **retro-explains** his existing climax line (*"standing at a window with a wick
in your hand, counting its hours and calling it hope"*), which turns from argument into memory.
Nobody dies on screen. It is a remembered loss, the register 08 already allows. Her name is
held back until P-1.

### 4.7 POST-GAME

**P-1 · The cinder wakes; the name is said** · `cutscene.cor_resolution`, the Last Lesson
(`script.starfall_round` / Fenn's lines), `npc.starfall_witness` · S
- Còr, after *"I'll be here to light it."*:
  > *narrate:* *"Beside his lamp sits a stone no bigger than a plum, glowing gold through every
  > crack."* **CÒR** (at_peace): *"Our star. Hers, and Fenn's, and mine. It came down the winter
  > Senna went. I carried it twenty years, cold. This morning it woke in my pocket."*
- Fenn, before his final battle: *"Senna would have wanted the last lesson to be a hard one.
  She always said the gentle ones get forgotten."*
- Starfall witness, so the motif closes its circle: *"Last time they fell, they came down cold
  and we were frightened of them. These come down warm. I've decided that's the same thing,
  forgiven."*

### 4.8 CROSS-CUTTING

**X-2 · The sprite-acting pass** (rank 8) · M · pre-CP touches are net 0 pages
*Why:* the era's great scenes were acted by 16-pixel sprites: a turn away, a pause, a nod. The
toolkit already has `face`, `move`, `emote` (alert, question, heart, ellipsis, sweat, sleep,
music, anger), `wait`, `cameraFocus` and `action` (player only, from `player_indi_actions`:
raiseLamp, toss, gift, sit, hurt). Today it uses 4 `move` ops and **1** `action` in the whole
game. Convert narrated acting into performance in these 12 scenes:
`intro_mentor`, `dusk_begins`, `beacon_battle`, `glowmoss_relight`, `cor_appears`,
`fenn_shared_past`, `wren_pale_vault`, the seven `light_lamp_*`, `great_null_named`,
`warden_cor_final`, `keystar_relight`, `dawn_breaks`. Rules:
- **Every lamp the player lights** gets `{op:'action', actor:'player', action:'raiseLamp'}`
  before the `world-lantern-light` sfx. This is free, and it makes the vesperlamp *physical*.
- **"He presses your shoulder once"** must be *shown* the first time. In `intro_mentor`, merge
  *"Mind you tend them both…"* and *"And fitting, is it not…"* into one `say`
  (*"Tend them both, and they will tend you. Fitting, is it not — every Wayfaring in
  Vesperholm begins at a crossroads."*), then add `move fenn` one tile, `face fenn` to player,
  and narrate *"He presses your shoulder once — warm, brief, certain."* The page count is
  unchanged (§4.1), and the three later callbacks now refer to something the player saw.
- Pauses: put a `wait 500–900` before any line that starts with *"..."*. The ellipsis is a
  stage direction, so honour it.

**X-3 · Portraits** (rank 10) · S (data) / M (Otho art)
- `wren_nightreach` uses `expr:'soft'` twice. Wren has no `soft` frame (neutral 0, eager 1,
  unsure 2, resolved 3). Either add a `soft` frame to `portraits/wren.png` and register it, or
  switch the lines to `resolved`.
- `reyl_quest` uses `expr:'grave'`. Reyl has no `grave` frame, so use `weathered`
  (pre-CP; no length change).
- `great_null_named`: add `portrait:'nessa'` (`haunted` for the Null lines, `reverent` for
  the closing look along the walk). The script's own comment promises this.
- **Otho Grist** has no portrait. He is the designed wall and the Stone Gleam's voice. Generate
  a 32×32 sheet (neutral / grave / proud) per `cinematics.md` §Portraits.

**X-4 · Crown interludes** (rank 11) · M
*Why:* pull-through. Each region currently ends on directions; it should end on an image.
At the **first entry** to the next region's opening map (the `ENTRY_TUTORIALS` once-only hook
pattern, so it is post-CP by construction), play a short in-world vignette made of letterbox,
tint, a `cameraFocus` on a distant tile and two narrate lines:
- Entering East (`saltreach_fen_i`): *"Far off, past the dark of the middle country, a single
  light moves up the mountain's flank — slow, careful, like somebody carrying a full cup."*
- Entering North: *"Somewhere on the mountain, a broom. You couldn't possibly hear it from
  here. You hear it anyway."*
- Entering West: *"Over the Spire, the sky has a shape cut out of it now — the exact size of
  one star."*
- Hub opening: the existing Penumbra beat.

(If a panel-based `CinematicScript` is preferred, note that the `cinematic` op currently hands
off and does not return to the world. Returning would need a small engine change, so the
in-world version is the data-only path.)

**X-5 · Phrase budget and the Gleam refrain** (rank 13) · S
- Cap **"held breath"** at 4 (keep it for Wren at Nightreach, Còr's valley, the Great Null and
  the Solarium arrival) and vary the other 11.
- **"weighed"** (22 uses) should not open a trainer's intro more than five times
  game-wide. Give each keeper class its own verb: tested, trimmed, sounded, read, warmed.
- Reserve **"courteous"** for Còr (10 uses at present).
- **Capitals for emphasis**: at most one per scene, never two in one line.
- **Make the Gleam refrain deliberate.** *"…remembers how to shine"* appears for Tide, Verdant
  and Frost. Use it for all eight Gleams (Ember, Stone, Storm, Solar and Lunar are reworded
  to fit), so that the Keystar's *"The sky remembers itself"* lands as the refrain's
  resolution.

**X-6 · Timeline sheet** (rank 22) · S
Add a short "Dates" block to `story-bible.md` and align the lines to it:
40 years on the ladder (Fenn, Còr, Senna as apprentices; the Starlamp filled) · 20 years
since the Ninth Lantern failed and Senna died (Còr's *"twenty years"*) · 11 winters of the Long
Dusk (Reyl, the ledger) · 2 years of the Great Null's scaffolding (Nessa). Fix *"this month"*
vs *"this season"* (taken care of by S-3's rewrite).

---

## 5. Falling stars as the through-line

**Verdict: underused.** The cinders are the game's most original image, and today they appear
in one mandatory scene, one optional crater, one LORE entry and a dawn swap. They should be the
recurring **dark rhyme** of the whole Wayfaring, in the way the lanterns are its warm one.

### 5.1 What a cinder *means* (canon-consistent with 08 and 06)

- **The law (said by Fenn, S-4):** every star has a kin carrying its spark. Put the kin to sleep
  and the star starves. A starved star gutters, and **sometimes its last cinder falls**.
- **Why nearer the mountain:** guttered light goes **home to the Keystar**, the anchor every
  constellation was lit from. As the Keystar weakens, its pull draws the falls in close, which
  is a spiral (W-4).
- **The Hollowing's relation:** indirect culpability (D1). Their sleeping kin starve the stars,
  and Còr, who cannot bear waste, **walks out and fetches the cinders home**, keeping them in the
  Spire like a swept churchyard (C-1). His null-lanterns each hold a chip of one, "not fuel,
  company" (W-2).
- **The personal root:** the first cinder Còr ever carried fell **the winter Senna died**. It was
  the star the three apprentices named together, and it is "the same thing, in the same season"
  that Fenn won't name (N-2 → X-1 → P-1).
- **What they turn out to be:** never dead, only guttered. At the relight, every cinder in the
  hoard glows (C-1). At dawn the world's cinders wake into star-shards (08, built). The
  post-game **Starfall** is the woken sky shedding *warm* shards (06), and the witness says so
  (P-1).

### 5.2 One fall per region (the escalation)

| Region | Beat | Status |
|---|---|---|
| South | Cold-open line (S-1) → orchard crater, mandatory (built) → `dusk_begins` echo (S-3) | swap-only |
| East | The acolyte's dropped cinder; the star returning over the Fennlight (E-1) · Cinderhead roof-fault cinder (E-3) | new |
| North | **Còr holds a cinder** (N-1) · a **live fall** over the Kite-rising (N-4) · Hushfrost crater (built) | new + built |
| West | Stillworks lantern chips (W-2) · Ledger's FELL column (W-3) · the Pass-walker's spiral (W-4) · **the Ember flickers** (W-1) | new |
| Central | **The Cinder Hoard** and the cinders glowing at the relight (C-1) · the Null answering the sun (C-2) | new |
| Post-game | Còr's cinder wakes gold; the Starfall contrast line (P-1) · orchard in flower (built) | new + built |

The escalation runs: told → seen after → seen held → seen *falling* → seen *counted* → seen
*kept* → seen *waking*. That is the motif's arc, and it is monotonic, as Arc B requires.

### 5.3 Housekeeping

- **Starglass Shards** (a 1,500w valuable, *"sky-fallen glass"*) currently compete with the
  motif. Re-describe them as pre-Dusk falls: *"From a fall long before the Dusk, when they
  still came down warm. Collectors pay handsomely; the old ones won't sell."*
- The **Starwell** (*"a star fell and did not go out"*) is the motif's exception that proves
  the rule. Give its sign one more clause: *"…the only one that never went cold. Nobody knows
  why. The Hollowing never touched it."*

---

## 6. Era-craft vignettes the toolkit can already stage

Each vignette is pure data, using existing ops. The `action` op is player-only until other
characters have action sheets.

1. **The shoulder** (`intro_mentor`): Fenn `move`s one tile in, `face`s the player, `wait 400`,
   then narrates the shoulder press. This is the gesture three later scenes call back to.
2. **Raising the lamp** (every lighting): `action player raiseLamp` → sfx → tint bloom. The
   vesperlamp stops being a menu word.
3. **The pause before the bad news** (`fenn_crossroads` line 1, `give_wick`, `fenn_shared_past`):
   `face` the speaker away from the player → `wait 700` → line → `face` back. Era players read
   a turned back as grief.
4. **Còr's back** (`warden_cor_final` opening): he starts `face up` (towards the Keystar) and
   only turns (`face down`) on *"You climbed kindly"*. It is one op, and it is the whole
   introduction.
5. **Wren leaves** (`wren_pale_vault`): two `face` changes, `emote ellipsis`, then `move` off
   through the snow, the first exit shown rather than told (N-3).
6. **The sweeping figure** (Stillworks, W-2): a silent `move` along a far gantry, a bow done as
   `wait`, and exit. Nothing is said.
7. **The kites dip** (N-4): `flashColor` + `cameraFocus` towards the mountain, held while the
   festival music *keeps playing*. Dread under joy.
8. **Tamsin's watering** (orchard, post-`gleam:ember`): `move tamsin` to the burn, `emote heart`,
   `move` back. It acts out *"I'm not allowed to water them."*
9. **The Ember goes out** (W-1): `cameraFocus` on a far tile in the south and hold; `silence`;
   gutter sting; `tint`; then the slow return of light. Done right, it is the scariest five
   seconds in the game.
10. **The memory on the ladder** (flashback, `fenn_shared_past`): `letterbox` → sepia `tint`
    (`#c8a878`, 0.35) → three narrate lines in the past tense (*"Three apprentices on a cold
    ladder. One steadying it. One naming the stars as they came loose. One at the top, filling
    a brass cell with starlight and laughing at the other two."*) → `tint` back → Fenn's next
    line. This is a flashback with no new art.
11. **The hoard wakes** (C-1/keystar): `cameraFocus` down the shaft towards the gallery tile,
    hold for one narrate line, then `cameraReset`. The camera *goes back to* the cinders.
12. **Two old men on the dawn road** (`dawn_breaks`): actually `move` Fenn up to the rail beside
    Còr, `face` both east, `wait 1200` with no line, then Fenn speaks. The silence is the
    reconciliation.
13. **Paul's chair** (S5, already strong): no change. It is the model for the rest. Its
    `silence` → stars going out → the bird flaring from the lamp is the best-acted scene in the
    South, and the house style should be measured against it.

---

## 7. Implementation notes for parallel implementers

- **Split by region** using §4.2–4.7. X-items have owners: X-2 and X-5 belong to whoever owns
  each scene, X-3 is one data pass plus an art task, X-4 needs one owner (it hooks
  `ENTRY_TUTORIALS`), and X-6 is a doc edit.
- **Staging discipline:** every new stage line uses the established
  `if_flag` + `unless_flag` pair, so that exactly one plays (the `andrew_hint` pattern).
- **Re-run `tools/maps/add_peril_thread.py`** after touching any peril map (W-1 witnesses, S-5,
  W-3), and the map audits after any new object or sign (C-1 gallery, E-3 hooks, E-1 cinder).
- **Copy-edit gate:** run the `copy-editing` skill over every new line. Keep canon vocabulary
  (kin, Gleam, Lumenary, vesperlamp, the Hollowing). No death on screen, no cartoon villainy.
  Còr is never gloated over.
- **The South rule bears repeating:** words may change, page counts may not, until the
  Chickenpig is in the lamp.
