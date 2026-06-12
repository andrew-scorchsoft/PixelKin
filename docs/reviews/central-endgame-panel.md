# PixelKin — C5 Expert Panel: The Central / Endgame Region

> A convened, independent review of PixelKin's **Central quadrant and the game's
> climax** (commits `2e87850` / `2aee6f7` / `fc01343`, plus the crown-derivation fix
> `723ee4d`): Vesper Crossroads (endgame hub layer), Penumbra Ring, Starwell, the
> four-floor Umbral Spire (`umbral_spire` → `_f2` → `_f3` → `_summit`), the C3 content
> (the Còr summit scene, the keystar relight, dawn-break, `ENDING_CREDITS`, the five
> acolytes, the three C-quests, Lunaveil). The three uncommitted optional maps
> (tideglass / hourfold / unrisen_stair) being built by another agent were **ignored**
> entirely — only committed Central content was reviewed.
>
> Judged against the binding acceptance specs: `walkthrough/05-central-endgame.md`
> (the **Climax & Resolution** section is BINDING — out-remembered not defeated;
> signature lines; mercy answered with mercy), `story-bible.md` §3/§7, `cinematics.md`,
> README §0, `level-design.md` §2a (Spire tier), `10-economy.md` §4/§9. **The N6 and
> W7 panels' findings discipline is the floor** — and W7 found a game-breaking blocker,
> so this panel hunted for the same class of bug with the same rigour.

## The panel

| Panelist | Discipline | Watches for |
|----------|------------|-------------|
| **Devs "Dee" Okonkwo** | Climax/level design | the ascent shape, the look-up moments, un-walk-aroundability, the shaft compressor |
| **Tomás Reic** | Narrative direction | does out-remembering land; is Còr's unbeaten-ness preserved; the credits' taste; humour firewall |
| **Mara Holloway** | Systems & balance | the acolyte ramp, Còr as final boss, the catch-gated ending, the Radiant Lamp economy |
| **Ivo Castellan** | Producer / first-time player | the walk from hub to credits, the breather, soft-locks, "do I understand I can Continue?" |

## How it was run

Evidence was **gathered, not assumed**. All six committed Central maps + the
crossroads re-rendered (`/tmp/c5/*.png`) and eyeballed against `level-design.md` §11
and the lamp-glow register; `audit_region central`, `audit_flow` (all 7 maps),
`audit_warps` run and read critically; **the entire endgame flag chain traced
end-to-end across map JSON + TS** (crown derivation → `hub_unlocked` → Penumbra →
Spire floors → `seen_great_null` → `cor_answered` → `keystar_relit` → `dawn` → the
cinematic op → Title → Continue); the persist-before-cinematic guarantee verified in
`WorldScene.startCinematic`; the blackout/respawn path read in source; the **Keylumen
catchRate-6 climax wall computed with the engine's actual `attemptCatch` formula**;
`progression.mjs` / `validate.mjs` / `simulate.mjs` run for the balance verdict; and the
**full climax script read as prose** (`script.warden_cor_final`, `keystar_relight`,
`dawn_breaks`, `ENDING_CREDITS`, all five acolytes) against the binding signature lines.

---

## Part 1 — The audit (what's working, keep it)

1. **The climax IS the inverse of a boss spectacle, exactly as the spec demands — and
   it lands.** `script.warden_cor_final` (scripts.ts:2694–2734) stages the confrontation
   with `silence` and portraits, not bombast. Còr makes his case at full strength
   ("I am not cruel, apprentice. I only want the grieving to stop"), the battle is the
   *form* not the *win* ("His kin sleep where they fell — unhurt, every one… He is not
   beaten. Nothing about him is beaten"), and the resolution is the **out-remembering**:
   every constellation named back at him in one rising passage, each with its town's
   specific festival memory (EMBER = the coast fair, TIDE = the moor-bell, … LUNAR = the
   all-night watch), closing on the kin — "Every one of them a goodbye waiting to happen.
   Every one of them worth it. Every one." Còr's certainty does **not** shatter: "It goes
   the way ice goes at the first thaw — quietly, from underneath, into something that
   moves again." **Tomás:** "This is the best-written scene in the game, full stop. The
   spine said 'remember louder than he can grieve' and the script *does it* — the player
   doesn't argue, they remember, and you can feel the difference."

2. **Còr's unbeaten-ness is preserved and mercy is answered with mercy.** The script is
   emphatic that the battle proves nothing ("you understand by now that the battle proves
   nothing. I have lost arguments before. Grief always loses the argument — and then it
   stays anyway"); Còr is **not destroyed** — he "steps aside from his own great work,"
   and in `script.dawn_breaks` Fenn climbs the dawn road and offers him a place back
   ("You read the same sky I did, old friend. There's still a lamp lit for you. …Come
   down and tend it with me"), and Còr "follows his friend down toward the morning,
   leaving the Great Null to the swallows and the rust." Story-bible §3/§7 honoured to
   the letter.

3. **The binding signature lines all appear — near-verbatim.** Spec line "I had hoped
   you'd be tired enough to agree with me… I am not cruel" → scripts.ts:2700 verbatim.
   "You're not arguing with me. You're *remembering* at me… I had forgotten it was worth
   the ache" → scripts.ts:2726–2727 verbatim. "Not into a victory — into a morning. Dusk
   will come again…" → scripts.ts:2785 verbatim. Fenn's "There's still a lamp lit for you"
   → scripts.ts:2781 verbatim. Fenn's C4 "remember louder than he can grieve" →
   scripts.ts:2405. Wren's "never again / never at all" → scripts.ts:2417. The acceptance
   spec's tone contract is met by the actual content.

4. **The crown-derivation BLOCKER from the W7 panel is properly fixed (commit 723ee4d).**
   `FlagStore.ts:19–52`: a single `deriveCrowns()` pass, correct mappings (south=ember+tide,
   east=verdant+stone, north=storm+frost, west=solar+lunar), `hub_unlocked` from all four
   crowns, **runs on every truthy `set()` AND in the constructor (loaded saves self-heal)**,
   idempotent. The legacy hand-set `crown_south` double-set is **gone** (trainers.ts now
   carries only `reward_flags:['gleam:ember']`/`['gleam:tide']`). And — addressing W7's
   MIN-1 — the invariant is now **CI-gated**: `validate.mjs` errors if any content lists a
   derived flag in `sets_flags`/`reward_flags` and tripwires that `deriveCrowns` still
   exists ("the game cannot be completed without it"); `audit_region` independently
   re-derives the hub. **Mara:** "W7's wall is gone and it's now untrippable. Belt and
   braces. This is how you respond to a blocker."

5. **The summit flag chain is hard-gated, banded across whole cuts, and re-fire-proof.**
   On `umbral_spire_summit.json` the four beats are each a 3-tile band (`great_null_reveal_0/1`,
   `cor_final_0/1/2`, `keystar_relight_0/1/2`, `dawn_breaks_0/1/2`), every one `once:true`
   AND `hidden_when_flag` = its own output flag, so the whole walkable cut is covered (the
   CLAUDE.md "band the whole cut, not one tile" steer is honoured) and **nothing can
   re-fire after dawn**. The order is provably enforced: keystar `requires_flag:cor_answered`,
   dawn `requires_flag:keystar_relit`. `audit_flow umbral_spire_summit`: "3 story trigger
   band(s) sit on true chokes." The Còr battle is inside the `cor_final` cutscene — a loss
   aborts the script before `cor_answered` banks (WorldScene.ts:449–450 "Only bank progress
   if the scene actually finished"), so a defeat is clean and retry-safe.

6. **The persist-before-cinematic guarantee is real, and Continue resumes post-dawn.**
   `script.dawn_breaks` sets `flag:dawn` **itself** via an explicit `setFlag` op
   (scripts.ts:2775) *before* the `cinematic` op (because the cinematic hand-over never
   returns, so the trigger's `sets_flags` can't be relied on — comment 2767–2770 is
   honest about why). `WorldScene.startCinematic` (566–573) does `await this.persist()`
   **first**, then `scene.start('Cinematic')`. So the autosave snapshot — taken on the
   summit with `flag:dawn` held — means a Continue after the credits lands back on the
   summit with the `to_dawn` warps to Dawnstead open. `ENDING_CREDITS.next = Title`. The
   player can absolutely Continue afterwards. **Ivo:** "The single scariest thing in an
   endgame — saving across the point of no return — is handled correctly. Verified, not
   asserted."

7. **The ending cannot be RNG-walled.** `flag:keystar_relit` is banked by the trigger's
   `sets_flags` **only when the cutscene completes** — and a failed Keylumen catch returns
   `false` (CutsceneRunner.ts:228–231), aborting before the gleam/banking. But the catch
   has **`cooldownBattles: 0`** (infinite free retries), the kin **can't flee**, and Fenn's
   **Starlamp** (`catch_bonus: 255` = guaranteed) is routed to it un-missably via Wren's
   join band. So the ending advances only on a catch, but the catch is functionally
   guaranteed and never strands. The dawn beat (`requires_flag:keystar_relit`) is unskippable
   but unwallable. Exactly the "the climax never strands" contract (scripts.ts:2737–2739).

8. **The maps read, and the Arc-D paradox is felt.** Crossroads = the warmest screen in
   the game (a four-way wheel of brown lanes, golden lamp-posts, festival sparkle-motes
   for the Lampling trail, the Hearth pool). Penumbra Ring = near-total black with the
   lamp-glow the only colour and pure-black void pools for the Starreach crossings — the
   single most "lanterns in the dark" screen in the game, with the Spire silhouette
   looming at the top. The four Spire floors = black basalt, snuffed **null-lanterns**
   (dark globes that locally suck the reveal-pools back), the **null-works** rows, drained
   Dark-kin silhouettes on F2, and — the thesis — **open sky-shafts showing the completed
   Crown's starfield overhead** (the "look up" beats, scripted in `spire_crown_1/2`). The
   summit shows the **Great Null** as a vast dark sphere over an altar. Starwell is a warm
   star-pool with ice-crystal accents — visually distinct from the Spire's null-dark.
   **Dee:** "The greatest light over the darkest place, made literal. The shafts sell it."

9. **The acolytes are five small griefs, not five mooks.** Each (Merrin the chandler,
   Tace the ferryman, Ivorwen the widow, Harl the miner, Sefa whose wife lit the north
   roads) is a *person* doing a careful terrible kindness, with a gentle ask and a
   sad-not-bitter defeat ("Still burning. All of yours, still burning. …the gate was never
   locked"). Zero humour, zero mook energy — the dungeon's emotional texture is exactly
   "sad people doing a careful, terrible kindness" (story-bible §7). **Tomás:** "Five
   variations on the same grief, each specific. The ferryman's 'you're the sort who docks
   at the dark jetty and lights it anyway' is a whole character in one line."

10. **Balance is on the curve and the final-boss design is right.** `progression.mjs` /
    `validate.mjs` (162 species, 0/0) / `simulate.mjs` (exit 0) all PASS. Acolyte ramp
    lands 52→55; Còr's ace 56 at +3 over the L53 checkpoint — *gentler* than the two
    hardest gym wardens (Lucan/Nessa +4), correct because Còr's pressure is **team depth**
    (six kin, smart AI), not a level cliff. His ace **Nullmajor** (#150, F-tier Dark
    sweeper, uncatchable) closes on its signature **`hollowing_hymn`** (120 BP Dark special,
    −1 spa to foe), led by **Omenire** carrying **`lull`** (100% doze) and a blight ladder
    throughout — Dark/Lunar pressure + a doze/blight threat, exactly as spec'd. Satisfying
    and winnable for a prepared ~L53–55 party. **Mara:** "A team-depth boss a notch under
    the stretch wardens is the right top rung. The Hollowing Hymn ace is a proper closer."

11. **The Lampling and the three C-quests are complete and on-voice.** Lampling (#148,
    Light, the hub-only mascot) is quested via `lampling_trail` (the guttering-lamp trail,
    "The trail was never a chase. It was an introduction"). C2 hangs four festival tokens
    in fixed S→E→N→W order → the **Radiant Lamp** (×3.5, quest-only). C3 closes the
    Waykeeper's Round with the **Way-lamp** keepsake + a Lamplight tease. All flags
    (`q_central_trail(_done)`, `q_central_tokens(_done)`, `q_central_round_done`) set and
    consumed cleanly.

12. **Central added its own LORE-codex footprint — the gap the North panel flagged is
    closed here.** `glossary.ts` gains `great_null`, `keystar`, `penumbra`, `ninth_lantern`,
    `keylumen`, `first_dawn` (keyed to `flag:dawn`), each keyed to a flag the climax already
    raises — no new story wiring. On-voice ("the Great Null… Còr means it kindly. That is
    the most frightening thing about it").

---

## Part 2 — Findings ledger

### BLOCKER
*(none)*

### MAJOR

- **MAJ-1 — A party-wipe anywhere in the four-floor Spire respawns the player at the
  GLOBAL start town (Tinderwick), with no heal point anywhere in the Spire — a long,
  demoralising re-traverse at the game's hardest sustained run.**
  *Evidence:* `WorldScene.blackout()` (WorldScene.ts:786–801) full-heals, docks the 10%
  tithe, then `enterMap(VESPERHOLM_GRAPH.start_map, …start_at)` — the **global** start, i.e.
  the opening coast town. Grep confirms **no inn / `heal` op / rest NPC** in any of the four
  `umbral_spire*` maps. So a wipe on the summit (after five acolyte fights + the Còr battle)
  dumps the player back in Tinderwick; recovery is: fast-travel spoke → Crossroads → cross
  the Penumbra Ring (Starreach voids) → re-enter the Spire → **re-climb all four floors**
  (F1→F2→F3→summit). The F3 `shaft_down` compressor (`flag:spire_shaft`) shortens the
  *descent* but does nothing for the post-wipe *ascent*. This is not a soft-lock (full heal,
  all warps open, the Crossroads inn resupplies) — but it is a real first-time-player wall at
  the climax, and it is inconsistent with the otherwise-meticulous "the climax never strands"
  care everywhere else in this region.
  *Why MAJOR not MINOR:* the endgame is the *one true difficulty ramp* (spec §at-a-glance) —
  precisely where a wipe is most likely — and the punishment (a multi-screen re-traverse
  through a barrier zone) is the harshest backtrack in the game, landed on the player at the
  emotional peak. A determined player isn't blocked, but the moment-to-moment cost of a
  single loss is steep enough to sour the climax.
  *Fix (small, data-only, one of):* (a) add a one-off rest/heal NPC or `heal` step_on at the
  Spire entrance (`umbral_spire` F1, e.g. "a dead Lumenary's vestry, warm enough to mend a
  lamp"), so a re-climb starts from a healed F1 rather than the global start; **or** (b) give
  the blackout a region-aware respawn — wake at the nearest healed waypoint (the Crossroads
  inn) rather than `start_map`. Option (a) is the cheapest and keeps the Spire as the no-shop
  vigil it's meant to be while removing the cross-region trudge. Either keeps full completion
  intact; both are leisure fixes (the game is winnable as-is).

### MINOR

- **MIN-1 — The Keylumen climax catch (catchRate 6) is a real grind *if* the player has
  spent the Starlamp earlier and brings no status.** *Evidence:* `species/149_keylumen.json`
  catchRate 6; the relight is a `legendaryBattle` (scripts.ts:2749). Computed with the engine's
  actual `attemptCatch` (catch.ts) at ~L55 (maxHp≈165): **Radiant Lamp ×3.5 + doze at red HP ≈
  4–5 throws** (acceptable); **Radiant + no status ≈ 11–12 throws**; **plain lamp + no status ≈
  40 throws** (grindy). The **Starlamp** (`catch_bonus:255`) makes it a **guaranteed 1-throw**,
  and it's the intended tool — un-missably delivered via Wren's join band, with Fenn's "Spend it
  nowhere else." So the *designed* path is clean. The risk is a player who (legitimately) spends
  the Starlamp on **Lunaveil** at Starwell first (Starwell sits after the Crossroads, so the
  Starlamp is in hand for it) and then meets Keylumen with only the Radiant Lamp. Because
  `cooldownBattles:0` and the kin can't flee, even the worst case is "throw repeatedly," not a
  wall — but a no-status attempt is a tedious tail on the game's apex beat. *(Note: the brief's
  premise that **Lunaveil** is catchRate 6 is a data mismatch — Lunaveil is catchRate **24**
  (Radiant+doze ≈ 1 throw); catchRate 6 belongs to Keylumen and the uncatchable Nullmajor. So the
  "spent the Starlamp on Lunaveil" path is itself cheap — Lunaveil never needed the Starlamp.)*
  *Fix (optional):* either nudge Keylumen's catchRate up a tier (e.g. 12–20) so the *fallback*
  (Radiant + doze) is a comfortable 2–3 throws, **or** lean harder on signposting — a one-line
  reminder at the dais if the Starlamp is already spent ("you spent the starlight; the lamp will
  have to ask the long way") so the grind reads as a *consequence*, not a bug. Lowest priority —
  the intended path is guaranteed.

- **MIN-2 — Doc/data drift: the kin count is 162 (and the credits say so), but README /
  CLAUDE.md still say "159 kin."** *Evidence:* `ls species/*.json` = **162**; `validate.mjs`
  reports "162 species"; `ENDING_CREDITS` credits "The 162 kin of Vesperholm" (cinematics.ts:163)
  — which is **correct against the data**. But `CLAUDE.md` ("Roster: 159 kin") and `README.md`
  ("all 159 kin") are stale, and `07-the-three.md:588` already flags the discrepancy. The credits
  aren't wrong; the canon docs are. *Fix:* reconcile README/CLAUDE.md to 162 (doc-only), or, if
  159 is the intended "register" count and the extra 3 are special/legendary, add a one-line note.
  Not a Central bug — surfaced here because the credits roll is the first place the real number is
  player-facing.

### POLISH

- **POL-1 — C4 (Fenn's counsel) and A5 (Wren's join) can be walked around on the Crossroads
  plaza.** *Evidence:* `audit_flow vesper_crossroads`: "story trigger(s) can be walked around:
  script.fenn_wave, script.wren_joins." This is **by design and correct** — C4 is explicitly
  optional in the spec, and the load-bearing gift (the Starlamp) rides Wren's join band on the
  **inward road** (the true choke into the Penumbra), so it can't be missed even if a player
  skips the plaza talk. The warning is the audit being conservative about a deliberately-optional
  beat. *Fix:* none needed; noted only so a future reader doesn't "fix" the intentional optionality.
  (If desired, a one-line comment on the trigger or a spec note would silence the future question.)

- **POL-2 — The Keylumen codex entry says "It was never caught. It was asked, and it answered,"
  but mechanically Keylumen IS a catch (`legendaryBattle`, sets `keylumen_caught`).** *Evidence:*
  glossary.ts:222 vs scripts.ts:2749. This is deliberate framing (the catch *is* the asking, and
  the narration leans into it — "regarding your lamp the way a kin regards a door held open"), and
  it's lovely writing. The only friction is a completionist reading the codex line literally while
  holding Keylumen in the party. *Fix:* none required; the tension is intentional and well-handled.
  Flagged for completeness only.

### PRAISE
*(carried in Part 1; the standouts: the out-remembering scene as the best writing in the game,
Còr's preserved unbeaten-ness + Fenn's mercy, the verified persist-before-cinematic guarantee,
the now-untrippable crown derivation with CI gate, and the five-grief acolyte run.)*

---

## Part 3 — The three weakest things (mandatory)

1. **The Spire blackout dumps you at the global start town with no in-Spire heal (MAJ-1).**
   The one place the endgame's care slips: a single party-wipe at the climax costs the harshest
   re-traverse in the game (Tinderwick → spoke → Crossroads → Penumbra → re-climb four floors),
   and the shaft compressor doesn't help the re-ascent. Not a lock, but the steepest moment-to-
   moment penalty in the game, landed at the emotional peak. A one-NPC heal at the Spire entrance
   fixes it.

2. **The fallback Keylumen catch is a grind if the Starlamp's been spent (MIN-1).** The intended
   path (Starlamp) is a guaranteed 1-throw, but a player who used the Starlamp on Lunaveil and
   arrives statusless faces ~11–40 throws on the game's apex beat. Free infinite retries keep it
   from being a wall, but it's the one spot where the climax's pacing can sag. A catchRate nudge
   or a signpost line closes it.

3. **The roster count is out of sync between the data (162, which the credits correctly use) and
   the canon docs (159) (MIN-2).** Harmless to play but the first player-facing number is now the
   credits' "162 kin," contradicting README/CLAUDE.md. A returning developer will trip on it. A
   one-line doc reconcile in the same spirit as "keep the docs current."

---

## Part 4 — Verdict & consistency check

**Verdict: SHIP-READY (fix-then-ship on MAJ-1 at leisure).** Every balance and flow gate
passes; the crown-derivation blocker the W7 panel found is fixed *and* CI-gated against
recurrence; the entire endgame flag chain traces clean setter-to-consumer with the summit beats
hard-gated, whole-cut-banded, and re-fire-proof; the persist-before-cinematic guarantee is
verified (Continue resumes post-dawn); the ending is catch-gated but functionally guaranteed and
never strands. **Nothing here blocks completion.** The one MAJOR (MAJ-1, the punishing Spire
respawn) is a data-only pacing fix, not a bug the game ships broken with — it's the gap between
"winnable" and "kind," and this region has earned the right to be kind at its own climax.

**The narrative is the high point of the project.** The out-remembering scene executes the
binding spec — *remember louder than he can grieve* — as actual playable text; Còr is preserved
unbeaten and offered mercy; the ENDING_CREDITS epilogue bookends the cold open in past tense,
remembers every town by its festival, walks the two star-tenders down "one ladder's width apart,"
and closes on the thesis ("not in a victory — in a morning. Dusk will come again"). Zero humour
leaked into the climax. The credits roll is tasteful and restrained.

**What Central did better than South/East/North/West:**
- **The emotional payoff.** The out-remembering scene is a clear half-step above the West's
  seven-lamp remembrance (which was itself above North's Còr/Fenn/Wren cluster) — because it's
  the cash-out of *all* of it, and the writing knows exactly how to spend it (silence, then the
  constellations named back, then the kin).
- **The climax engineering.** The persist-before-cinematic + catch-gated-but-never-stranding +
  whole-cut-banded summit chain is the most carefully-wired sequence in the game, and the panel
  could not find a soft-lock in it.
- **Responding to the prior panel.** W7's blocker isn't just fixed — it's made *untrippable*
  with a CI gate (`validate.mjs` tripwire) and an independent re-derivation in `audit_region`.
  That is the right way to clear a blocker: fix it, then make the class of bug impossible.

**What the prior regions did better:**
- **Kindness on a loss.** South/East/North/West never asked the player to re-cross a barrier zone
  after a wipe — their heal spacing kept recovery local. Central's no-shop vigil is thematically
  right but goes one step too far by sending a wipe all the way home (MAJ-1).
- **Catch-rate generosity at set-pieces.** The earlier regions' reward catches (Tide Charm,
  conditional charms) made their prize kin comfortable; Keylumen's catchRate 6 leans entirely on
  the Starlamp being saved (MIN-1) — a tighter margin than precedent.

**Consistency with the three prior panels:** this review applied the same evidence-gathered
discipline (render + audit + flag-trace + balance gates + prose read). It found **no BLOCKER**
(unlike W7), one MAJOR (a pacing/kindness gap, not an engine gap), and otherwise confirms the
region as the creative summit of the game. The crown fix means the W7 wall is closed; the
endgame the W7 panel said "sits behind a dead gate" is now fully reachable and ships sound.

*All panelist names are original personas standing in for handheld-RPG disciplines, per
VISION.md — described by craft and era, never by any existing studio or person.*
