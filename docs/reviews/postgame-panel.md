# PixelKin — R5 Expert Panel: The Post-game (Dawnstead, the Starfall Vigils, day-forms)

> A convened, independent review of PixelKin's **post-game** — everything gated behind
> `flag:dawn`: the epilogue town of **Dawnstead** (R2), the **day-form** collecting layer
> and the Radiant-Lamplight backtracks, the arc resolutions (Wren A6, Còr's quiet
> aftermath), and **the Starfall Vigils** (R3) — the five riddle-led trial sites, the
> Last Lesson summit Round, the Star-tender naming, and the Dawnbrael catch.
>
> Judged against the binding acceptance spec `walkthrough/06-postgame.md` (its flag table
> and validation hooks are BINDING; the verbatim-quoted keeper/Fenn/Wren/Còr/Oriel lines
> are canon), the spine §10 voice contract (bittersweet-warm, ~1-in-6 glint, sincerity at
> Murkfall + the summit, Còr/Mer never punished), `story-bible.md` §3/§7, `cinematics.md`,
> and `10-economy.md` §4/§9. **The central-endgame and north panels set the bar and the
> findings discipline** (central found a kindness MAJOR; north found copy-paste interiors)
> — this panel hunted for the same classes of bug with the same rigour, and owed the §10
> tone gate from R3.

## The panel

| Panelist | Discipline | Watches for |
|----------|------------|-------------|
| **Devs "Dee" Okonkwo** | Progression / flow design | dead-ends, flag logic, blackout recovery, the loss-aborts gauntlet shape |
| **Mara Holloway** | Systems & balance | the 58→70 bands vs the rematch on-ramp, vigilant payouts, Dawnbrael's catch kit |
| **Tomás Reic** | Narrative & tone | canon vocab, bittersweet-warm, Còr/Mer never punished, the glint ratio, sincerity |
| **Ivo Castellan** | Producer / returning player | can a returning player find the chain? is Còr surfaced? day-form discoverability |

## How it was run

Evidence was **gathered, not assumed**. The whole post-game flag chain was traced
setter-to-consumer across map JSON + TS: `flag:dawn` → Dawnstead beats → the day-form/
Helixia table → the P1–P3 quest flags → the full Vigil chain (`starfall_begun` →
`vigil_reading_n`/`vigil_n_kept` strict boolean ladder → `vigil_5_kept` → `starfall_lesson`
→ `dawnbrael_caught` → `starfall_crown`). Every Oriel placement and every Vigil-site
trial/kept/again swap was checked for flag-disjointness; the summit re-dress was confirmed
to coexist with the shipped climax (`cor_answered`); the `legendaryBattle`/`cooldownRef`
path for Dawnbrael was read against the engine's `CutsceneRunner`; all ten P1 letter
recipients were located in their host maps; the readings + every keeper/Fenn/Wren/Còr/Oriel
line were read as prose against the spec's verbatim quotes; `npm run typecheck` and
`node tools/balance/progression.mjs` were run for the gate verdict.

---

## Part 1 — The audit (what's working, keep it)

1. **The Vigil flag chain is a strict, un-skippable boolean ladder, and it traces clean.**
   Reading *n+1* only ever issues from kept *n* (`script.vigil_<site>` sets both `vigil_n_kept`
   and `vigil_reading_<n+1>` after the battle), so `flag:vigil_5_kept` provably implies all
   five — the C3 "Long Round" pattern, no quest counter. The summit Round
   (`requires_flag: flag:vigil_5_kept`, `hidden_when_flag: flag:starfall_lesson`) → Dawnbrael
   (`requires_flag: flag:starfall_lesson`, `hidden_when_flag: flag:dawnbrael_caught`) →
   the naming (`requires_flag: flag:dawnbrael_caught`, `hidden_when_flag: flag:starfall_crown`,
   `once: true`) is a hard-gated, provably-ordered, re-fire-proof sequence sharing the lantern
   tiles 10–12,7 — each disjoint from the next on its own output flag. **Dee:** "I tried to
   break the order on paper and couldn't. Reading-from-kept is the whole spine, and it holds."

2. **A loss anywhere in the gauntlet is clean and retry-safe — exactly the engine convention.**
   `script.starfall_round` runs `vigilant_ondra_summit → solenne_summit → mer_summit → heal →
   startender_fenn` as sequential `battle` ops; every grant/`setFlag` sits *after* the last
   battle, and the runner aborts the script on a loss (`CutsceneRunner` `case 'battle'`:
   "a lost trainer battle aborts the scene"). So a wipe banks nothing, the blackout fires, and
   the whole Round re-runs from its trigger — the intended shape of the ultimate. The diegetic
   `heal` before Fenn is correctly placed.

3. **The ending never strands.** Dawnbrael is a `legendaryBattle` with `cooldownBattles: 0`
   (infinite free retries) and a `cooldownRef` (`npc.dawnbrael_resting`) that exists and reads
   right ("raise the lamp again, and it will answer with the next light"). The catch sets
   `flag:dawnbrael_caught` via the op's `caughtFlag`; a fled/KO'd Dawnbrael is re-approachable
   **without** re-fighting the Round (it gates on `starfall_lesson`, already held). The chain's
   own reward charms (Radiant ×3.0 any-status, Morrow ×3.0 first-turn) are the designed catch
   kit for the lv70 F-tier. **Mara:** "Catch-gated but unwallable, with the kit handed to you
   two sites earlier. Correct."

4. **Watcher Oriel is a faultless noticeboard — eight flag-disjoint placements, one tile.**
   `oriel_begin` (`flag:dawn` → `starfall_begun`) → five re-read placements each keyed
   `requires flag:vigil_reading_n` / `hidden_when flag:vigil_reading_n+1` (so the terrace always
   shows exactly the current clue) → `oriel_carry` (`vigil_5_kept` → `starfall_crown`) →
   `oriel_epilogue` (terminal). A clue can never be lost; a returning player who forgot the
   thread gets it re-read verbatim. The opening cutscene is wired as Oriel's `dialogue_ref`
   (interact), setting `starfall_begun` + `vigil_reading_1` inside the script — the right
   equivalent of the spec's "interact, requires `flag:dawn`, once."

5. **Every flag in the 06-postgame table opens AND closes where the table says.** Spot-traced:
   all ten P1 letter flags are *set* in `script.post_letter_*` and *consumed* by a
   `hidden_when_flag` on the recipient's placement in its host map (Wren/Fenn in `dawnstead`,
   then `tinderwick`/`pearlmoor_quay`/`lowleaf_hollow`/`cinderhead_mine`/`galehigh_terraces`/
   `pale_vault_glacier`/`sunken_solarium`/`nightreach_observatory`). P2 (`q_post_wick` →
   `q_post_wick_given`) runs Beacon cache → Còr hand-in → deco swap. P3 (`q_post_survey`
   1→2→3→`_done`) is a clean chained survey. The R2 additions beyond the table
   (`cor_greeted`, `wren_a6`, `dawnstead_arrived`/`_festival`, the `picked_*` caches) each
   have a consumer or are deliberately terminal; `cor_greeted` is set by the cutscene
   *trigger's* `sets_flags` (whole-cut band, tiles 3–4 × 20–22) and gates its own hide — the
   script itself correctly sets no progression flag, per the spec.

6. **The summit re-dress coexists with the shipped climax without collision.** The climax
   `warden_cor_final` beats (gated `cor_answered`) and the post-game Round (gated
   `vigil_5_kept`) share the summit map but are flag-disjoint; `warden_cor`'s climax NPC hides
   on `cor_answered`. The post-game layer is pure flag-gated re-dress, exactly as the spec's
   "no new map" contract requires.

7. **Balance is on the curve, and the on-ramp is real.** `progression.mjs` PASSES with the
   POSTGAME leg: The Last Lesson (Fenn, ace 70) lands at the L67 checkpoint, payout 8,400
   (`cor` 120 × 70). The chain's bands climb 58–60 → 60–62 → 62–64 → 64–66 → 66–68 → summit
   67–70, each annex one band above the last, and each site ships an apex-band wild bed as the
   designed grind floor so a ~L55 post-climax party levels *into* the chain. The new `vigilant`
   class (80w × ace) sits correctly between warden (60) and cor (120). **Mara:** "The ladder
   extends cleanly and the wilds are the warm-up. No cliff."

8. **The writing is the post-game's whole point, and it lands.** Dawnstead's arrival is the
   sky first ("Morning. Not lamplight, not moonrise... morning, blue and gold"); Fenn's Arc-D
   line is verbatim and at peace; **Wren's A6** and **Còr's resolution** are the spec lines
   word-for-word, Còr "never gloating, never punished" ("the lamp is *for* the dark — not
   against it... It will fall again. I find I no longer mind"). The Vigils are post-dawn
   wonder: the keepers are five retired griefs-turned-joys, each tied to a warden they taught
   (Esra→Brisa, Bramm→Otho, Ondra→Mira, Solenne→Lucan, Mer the Hollowing mercy paid forward).
   The glint holds ~1 in 6 (Oriel "not allowed anywhere with weather"; Bramm "Otho exaggerates";
   Ondra "I can't spend wind") and **Murkfall + the summit are sincere throughout** — Mer
   carries no joke, Fenn's finale rhymes the satchel ceremony ("No satchel this time. No
   errand... Show me everything you've become"). The Star-tender naming is the bookend the
   whole game was tuning toward. **Tomás:** "This is the warm exhale the spec asked for. Mer is
   the quietest, bravest beat in the post-game, and the chain knows not to crack a joke at it."

9. **Canon vocabulary is clean and `typecheck` is green.** No "monster/gym/badge" or any
   franchise term in the new player-facing text; "kin / Lumenary / Gleam / Lantern Gift /
   vesperlamp / kindling / the Hollowing / Hearth" used correctly throughout. Wickmoth (kin 16)
   is the headline day-form in Dawnstead's verge as the spec's atlas-card-14 example; Helixia
   (131) rides the post-crown verge zone (`requires_flag: flag:starfall_crown`). `npm run
   typecheck` passes clean.

---

## Part 2 — Findings ledger

### BLOCKER
*(none)*

### MAJOR

- **MAJ-1 — Every Vigilant's intro AND defeat line displays TWICE in a row, because the
  `script.vigil_*` `say` ops and the trainer's `intro_ref`/`defeat_ref` carry the *identical*
  string.** *Evidence:* `script.vigil_hearthfall` (scripts.ts:3309) speaks Esra's intro
  "I dipped Brisa's first wick when she came up to my elbow…" via a `say`, then runs
  `{ op: 'battle', trainer: 'vigilant_esra' }`; the BattleScene independently renders the
  trainer's `intro_ref` `trainer.vigilant_esra.intro` (trainers.ts:881) — which is the **same
  line verbatim** (BattleScene.ts:212 reads `intro_ref`; :703 reads `defeat_ref`). The script's
  post-battle `say` (scripts.ts:3311, "Steady as her best. Take the shard…") likewise duplicates
  `trainer.vigilant_esra.defeat`. This repeats for **all nine vigil trainers** (`vigilant_esra/
  bramm/ondra/solenne/mer`, the three `_summit` variants, and `startender_fenn`): the player
  reads each keeper's intro twice, fights, then reads the defeat twice. *(The `_summit`
  trainers' refs differ slightly from `script.starfall_round`, so those double less exactly,
  but Fenn's intro is word-for-word in both scripts.ts:3445 and `trainer.startender_fenn.intro`.)*
  *Why MAJOR, not MINOR:* it's the single most visible "built fast" tell across the *entire*
  flagship chain — the doubling fires on every one of the game's hardest, most ceremonial
  fights, and it undercuts the carefully-staged keeper voice the spec spent its prose budget
  on. It's the post-game's analogue of the north panel's copy-paste interiors. *Why not a
  BLOCKER:* purely cosmetic — no soft-lock, no balance effect, completion unaffected.
  *Established convention (the fix model):* the shipped in-script trainers do NOT duplicate —
  `script.flats_trainer_a` says MORROW's *cutscene* line ("Hold up there, Wayfarer! The flats
  test every lamp…") while `trainer.flats_wayfarer_a.intro` is a **distinct** battle shout
  ("Hold there, friend. Two lamps on a dark flat…"); `warden_cor` does the same (the climax
  speech lives in `script.warden_cor_final`; `trainer.warden_cor.intro` is a short, different
  battle line "Let the lamps make the argument"). *Proposed fix (one of, NOT built — it's a
  multi-entry structural change, outside the "inline MINOR only" remit):* (a) **preferred** —
  give each `vigilant_*`/`startender_fenn` def a short *distinct* battle intro/defeat shout
  (the warden_cor model), keeping the spec's verbatim keeper lines in the script as the
  cutscene context; **or** (b) drop the duplicated `say` ops from the scripts and let the
  trainer refs carry the (verbatim) lines — simpler, but loses the pre-battle framing beat and
  moves canon lines out of the script. Option (a) matches every other boss/route trainer in the
  game and is the recommendation.

### MINOR

- **MIN-1 — No LORE-codex entry for Dawnbrael or the day-forms — the one collecting hook with
  no permanent re-readable trace.** *Evidence:* `glossary.ts` adds `first_dawn`, `the_starfall`,
  `the_vigilants`, `star_tender` (all flag-keyed, on-voice) — but nothing for **Dawnbrael**
  (the first-morning kin, the chain's crown catch) or the **day-form** layer (the spec calls
  day-forms "the post-game's spine"). A returning, time-poor player who caught Dawnbrael or a
  day-form has no codex line to re-read them from. *Spec:* 06-postgame headlines day-forms as
  the post-game's collecting spine; the dawn/Starfall/Vigilant/Star-tender quartet is otherwise
  the model. *(This is the exact gap the north panel flagged for its festivals — a recurring
  series weakness, so MINOR not MAJOR.)* *Fix (data-only, no new wiring):* add a `day_forms`
  entry (`unlock_flag: flag:dawn` — the field-sign voice is already written: "the moths came
  out gold this morning… they won't keep; nothing does. That's why you catch it") and a
  `dawnbrael` entry (`unlock_flag: flag:dawnbrael_caught`, or `flag:starfall_crown`). Both reuse
  flags the chain already raises.

- **MIN-2 — The Wren rematch's "loser buys the lanterns" + `payout: 1488` is a tiny tonal/
  economy wrinkle.** *Evidence:* `script.wren_dawnstead` has Wren say "Loser buys the lanterns"
  (the friendly stakes), but the rematch pays the player 1,488w (`wren_rematch`, rival 24 × ace
  62) on a win like any trainer. Harmless and consistent with how every friendly battle pays,
  and the spec explicitly wants the rematch re-runnable with `reward_flags` bookkeeping only —
  but a literal-minded player notices Wren paying *them* after joking that the *loser* buys.
  *Fix (optional):* none required; flagged only because the line invites the reading. A
  one-line defeat tweak ("…the lanterns are on me, then") would close it, but it's taste, not a
  bug — left alone per the "don't rewrite working lines" remit.

### POLISH

- **POL-1 — The Dawnstead day-form encounter zone carries no `requires_flag: flag:dawn`.**
  *Evidence:* `dawnstead.json` `sunlit_verge` (the day-form table) has no flag gate; only the
  Helixia overlay zone gates on `starfall_crown`. *Assessment:* harmless — the `dawnstead` node
  itself is `unlocked_by_flag: flag:dawn`, so the table is unreachable pre-dawn regardless. The
  spec's "gated on `flag:dawn`" is satisfied at the node level. Noted only so a future reader
  doesn't "fix" the absent gate; no change needed.

- **POL-2 — The Dawnbrael catch and the title-naming share the lantern tiles 10–12,7 as two
  `interact` triggers (`dawnbrael_wakes` then `startender_named`).** *Evidence:*
  umbral_spire_summit.json:460–533. *Assessment:* correct and disjoint — `dawnbrael_wakes` hides
  exactly when `dawnbrael_caught` is set, which is the same flag `startender_named` requires, so
  they never co-fire. Flagged for completeness; the layering is sound.

### PRAISE
*(carried in Part 1; the standouts: the strict reading-from-kept boolean ladder, the
loss-aborts gauntlet, the never-stranding Dawnbrael catch with its handed-down charm kit, the
faultless eight-placement Oriel noticeboard, and the sincerity discipline at Mer + the summit.)*

---

## Part 3 — The three weakest things (mandatory)

1. **The doubled Vigilant intro/defeat lines (MAJ-1).** Every ceremonial keeper fight in the
   flagship chain shows its intro twice and its defeat twice, because the script `say` and the
   trainer `_ref` carry the identical string. The most visible polish gap in the post-game, and
   the only thing here that reads as "built fast." A distinct-battle-shout pass (the warden_cor
   model) fixes it across nine trainers without touching the spec's verbatim keeper lines.

2. **No codex trace for Dawnbrael or the day-forms (MIN-1).** The post-game's headline
   collecting hook and its crown catch leave nothing for a returning player to re-read — the
   same gap the north panel flagged for its festivals. Two flag-keyed glossary entries, no new
   wiring, closes it.

3. **The Wren "loser buys the lanterns" / pays-you-anyway wrinkle (MIN-2).** A featherweight
   tonal seam on an otherwise word-perfect A6 coda; noted, not worth rewriting a working line.

---

## Part 4 — Verdict & consistency check

**Verdict: SHIP-READY (fix-then-ship on MAJ-1 at leisure).** `typecheck` is green and
`progression.mjs` PASSES; the entire post-game flag chain traces clean setter-to-consumer with
the Vigil ladder provably strict, the gauntlet loss-safe, the Dawnbrael catch never-stranding,
and the summit re-dress collision-free with the shipped climax; all ten letter recipients exist;
the swap placements are flag-disjoint throughout. **Nothing here blocks completion or balance.**
The one MAJOR (MAJ-1) is a cosmetic double-dialogue affecting every Vigil fight — a data-only
fix on nine trainer defs, recommended but not built (it's a multi-entry structural change,
outside the inline-MINOR remit).

**The tone gate (owed from R3) passes.** Canon vocabulary only; the Vigilants are celebration,
never gatekeeping bitterness; Mer is the Hollowing's mercy paid forward and Còr is the gentlest
beat in the toolkit — neither gloated over nor punished; the glint holds ~1 in 6 and falls
silent at Murkfall and the summit exactly as spec'd; Fenn's finale is sincere throughout and
bookends the cold open. The spec's verbatim-quoted lines (Fenn's Arc-D counsel, Wren's A6, Còr's
resolution, every reading, every keeper intro/defeat) were checked against the build and match.
**No inline copy fixes were needed** — the transcription is clean (em-dashes and spacing
consistent with surrounding content, no register slips, no typos found). Per the remit, no
working line was rewritten for taste, and no canon line had drifted.

**What the post-game did better than the prior regions:**
- **The flag engineering.** The reading-from-kept boolean ladder + the loss-aborts Round +
  the never-stranding catch + the flag-disjoint Oriel noticeboard is the most carefully-wired
  optional chain in the game, and the panel could not find a dead-end or a double-fire in it.
- **Sincerity discipline at scale.** The chain sustains the ~1-in-6 glint across five sites
  and then *stops it dead* for Mer and Fenn — a harder calibration than any single prior
  set-piece, executed cleanly.

**What the prior regions did better:**
- **Trainer dialogue hygiene.** South/East/North/West/Central in-script trainers never doubled
  their lines (the `flats`/`warden_cor` distinct-shout convention); the Vigils regressed it
  across the whole chain (MAJ-1).
- **Codex footprint.** Central closed the north panel's festival-codex gap for its endgame
  terms; the post-game reopens a smaller version of it for Dawnbrael + day-forms (MIN-1).

**Consistency with the prior panels:** this review applied the same evidence-gathered
discipline (flag-trace + balance gate + typecheck + prose read against verbatim canon). It found
**no BLOCKER**, one MAJOR (a cosmetic doubling, not an engine gap), and otherwise confirms the
post-game as a sound, warm, completable coda that delivers the spec's six promises and the
bittersweet thesis: *the cycle has resumed, dusk will come again, and that is exactly the point.*

*All panelist names are original personas standing in for handheld-RPG disciplines, per
VISION.md — described by craft and era, never by any existing studio or person.*
