# Battle runtime — move learning & status conditions (plan)

The first-hour battle slice ships real turn order, damage, catch, run, faints,
trainer switching, XP and level-ups (`src/game/systems/battle/`, `party/`). Two
pieces were intentionally stubbed; this plans them so they land cleanly on the
existing engine rather than as bolt-ons. Neither changes balance data — they make
the already-authored move `effect`s and the dex `learnset` actually play.

## Part A — Move-learning prompt (replace the silent auto-replace)

**Today:** `KinInstance.learnMovesAt()` (KinInstance.ts) auto-overwrites move slot 0
when a kin already knows 4 and levels into a new move. The player never sees it and
can lose a move they wanted.

**Target:** the genre's classic prompt — *"Vulpyre wants to learn Ember Jab. Forget
which move? / Give up on Ember Jab."*

**Design**
1. **Make learning return a decision, don't take it.** Split `learnMovesAt`:
   - auto-add when there's a free slot (≤4), as now;
   - when full, collect the move into a `pending: Move[]` instead of replacing slot 0.
   `gainExp()` already returns `{ levelsGained, learned }`; extend to
   `{ levelsGained, learnedAuto: Move[], pending: Move[] }`. Add
   `KinInstance.replaceMove(slot: number, move: Move)` and `learnMove(move)` (free slot).
2. **Surface it where XP is awarded.** `BattleScene` (after the win/XP narration) and
   any future overworld XP source iterate `pending`: for each, run a new
   `ui/MoveLearnPrompt` and apply the player's choice, then persist the party.
3. **`ui/MoveLearnPrompt`** (built from the kit — Panel + DialogueBox + Menu, like
   `StarterSelect`): narrate the want-to-learn line, then a Menu of the 4 known moves
   (label = name, with type/power/charges) plus a "Give up on <move>" row; Confirm on a
   move ⇒ `replaceMove(slot, newMove)`, Cancel/give-up ⇒ skip. Promise-based
   `await new MoveLearnPrompt(scene, kin, newMove, sfx).run()`.
4. **Edge cases:** already-known move ⇒ skip silently; multiple `pending` in one battle
   ⇒ queue them; a fainted kin still learns; level-up that crosses several levels
   accumulates pending in learn order. Charges for a newly learned move start full.

**Touch points:** `systems/party/KinInstance.ts` (return shape + replaceMove), new
`ui/MoveLearnPrompt.ts`, `scenes/BattleScene.ts` (consume `pending`). No data changes.
Small, self-contained; ~half a day.

> **Head start (2026-06):** the Star-chart system (10-economy.md §6) already shipped
> `KinInstance.knowsMove/canStudy/learnMove/replaceMove` and a working "set one aside /
> give up" forget-flow in `ItemsMenu.studyChart()` — Part A should lift that flow into
> `MoveLearnPrompt` rather than rebuild it.

## Part B — Status condition engine (run, don't just narrate)

**Today:** `BattleEngine.applyEffect()` maps `{stat,stages}` effects (fully working) but
only *narrates* `{status}` effects. The canon statuses are already defined in
`docs/mechanics/03-moves.md` and used by ~a dozen authored moves
(`scorch/drench/numb/doze/blight/dazzle/chill`), and `04-capture.md` gives them a
`statusBonus` to catch rate. The save enum `KinStatus` (save/types.ts) is still the
generic placeholder set (`sleep/burn/...`) and must be aligned to canon.

**Canon effects (from 03-moves.md — implement exactly these):**

| Status | Effect |
|--------|--------|
| `scorch` | chip damage each turn (1/16 maxHp); halves physical Atk |
| `drench` | −Speed; occasional skip (act fails ~25%) |
| `numb` | −Speed; may be unable to act (~25%) |
| `doze` | asleep, cannot act 1–3 turns, then wakes |
| `blight` | escalating chip each turn (n/16, n++ per turn it persists) |
| `dazzle` | confusion: a chance each turn to hit *itself* instead |
| `chill` | frozen, cannot act until thawed (~20%/turn, or a fire/Ember hit thaws) |

**Design**
1. **Align the data model.** Change `KinStatus` (save/types.ts) to the canon union
   (`'none'|'scorch'|'drench'|'numb'|'doze'|'blight'|'dazzle'|'chill'`); bump
   `SAVE_SCHEMA_VERSION` and add a SaveCodec migration mapping the old placeholder
   names → canon (or → 'none' if unset). Status persists out of battle (a blighted kin
   stays blighted); volatile counters (doze turns, blight stacks) live in per-battle
   state like `stages`, reset by `resetBattleState()`.
2. **Apply on hit.** In `applyEffect`, map `effect.status` → `KinStatus`, and set it only
   if the target has no major status yet (single-status rule); emit the existing
   `status` event. `chance`/`to` already handled.
3. **Pre-move gate.** In `useMove`, before spending charges, run a status check for the
   actor: `doze` (decrement counter, maybe wake — if asleep, cancel the move),
   `chill` (maybe thaw, else cancel), `numb`/`drench` (chance to cancel), `dazzle`
   (chance to damage self instead of acting). Emit the right narration events
   (add `status-block`, `status-thaw`, `status-wake`, `confusion-hit` to `BattleEvent`).
4. **End-of-turn tick.** After both sides act in `resolveMoveTurn`/`foeTurn`, apply
   `scorch`/`blight` chip (emit `damage` events, then `handleFaints`). Add a single
   `endOfTurn(events)` phase so ordering is one place.
5. **Stat hooks.** `scorch` halves physical damage and `numb`/`drench` cut speed — apply
   in `damage.ts` / the `spe` getter via a status-aware modifier (mirror the stage
   multiplier the getters already use). Keep it in the derived getters so the foe AI's
   damage estimate sees it too.
6. **Catch + cure.** Feed `statusBonus` (04-capture.md) into `catch.ts`. `fullHeal()`
   already clears status; wire the Lumenary heal / future medicine + a faint-recovery
   path (Part of the UX fixes) to clear it. Switching out does NOT clear major status
   (matches genre); volatile counters reset on send-out via `resetBattleState`.

**Touch points:** `systems/save/types.ts` + `SaveCodec.ts` (enum + migration),
`systems/party/KinInstance.ts` (status field already there; add volatile counters +
status-aware stat mods), `systems/battle/BattleEngine.ts` (pre-move gate + endOfTurn),
`systems/battle/damage.ts` (scorch), `systems/battle/types.ts` (new events),
`systems/battle/catch.ts` (statusBonus), `scenes/BattleScene.ts` (narrate new events).

**Risks:** the Monte-Carlo balance sim (`tools/balance/`) does not model status, so
status moves are currently costed by proxy — re-run `simulate.mjs` after, and treat
status balance as a known approximation. Keep effects faithful to `03-moves.md` so the
docs stay the source of truth.

**Sequencing:** Part A first (small, isolated, high player value). Then Part B in the
order above (data model → apply → gate → tick → stat hooks → catch/cure), each step
independently testable in a wild battle. Roughly 1–1.5 days for B.
