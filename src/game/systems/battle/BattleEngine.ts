/**
 * BattleEngine — scene-agnostic turn resolution.
 *
 * Holds the two active kin (player + foe), the player's Party, and (for trainer
 * fights) the foe's Party. Each public method resolves one player decision into
 * an ordered list of `BattleEvent`s that the scene narrates. The engine owns:
 *   - turn ordering (move priority, then speed, ties broken randomly),
 *   - damage + accuracy + crit via damage.ts,
 *   - a tiny effect layer: stat-stage changes (the common case) and a no-op for
 *     custom status strings (full status engine is out of scope),
 *   - faints and (trainer) the foe's auto-switch to its next kin,
 *   - the foe AI's move choice (simple: best-damage, occasional random),
 *   - wild catch + run.
 *
 * It deliberately does NOT touch Phaser; the BattleScene plays the events back.
 */
import type { Move } from '@game/data/dex';
import type { KinInstance } from '@game/systems/party/KinInstance';
import type { Party } from '@game/systems/party/Party';
import { computeDamage, rollHit } from './damage';
import { attemptCatch } from './catch';
import type { BattleAction, BattleEvent, Side } from './types';

export type BattleKind = 'wild' | 'trainer';

export interface EngineConfig {
  kind: BattleKind;
  playerParty: Party;
  /** Trainer's party (trainer battles) or a one-kin party (wild). */
  foeParty: Party;
  rng?: () => number;
}

export class BattleEngine {
  readonly kind: BattleKind;
  readonly playerParty: Party;
  readonly foeParty: Party;
  private readonly rng: () => number;

  /** Set true once a side has lost / fled / a catch succeeded. */
  ended = false;
  outcome: 'win' | 'lose' | 'caught' | 'fled' | null = null;
  caught: KinInstance | null = null;

  constructor(cfg: EngineConfig) {
    this.kind = cfg.kind;
    this.playerParty = cfg.playerParty;
    this.foeParty = cfg.foeParty;
    this.rng = cfg.rng ?? Math.random;
    this.player.resetBattleState();
    this.foe.resetBattleState();
  }

  get player(): KinInstance {
    return this.playerParty.active;
  }
  get foe(): KinInstance {
    return this.foeParty.active;
  }

  // --- Player-initiated actions -------------------------------------------

  /**
   * Resolve a full turn from the player's chosen action. Returns the narration
   * events; check `this.ended` / `this.outcome` afterwards.
   */
  takeTurn(action: BattleAction): BattleEvent[] {
    const events: BattleEvent[] = [];

    switch (action.kind) {
      case 'run':
        return this.resolveRun();
      case 'catch':
        return this.resolveCatch(action.itemId);
      case 'switch':
        // A switch takes the player's turn; the foe then attacks.
        if (this.playerParty.switchTo(action.partyIndex)) {
          events.push({ type: 'switch', side: 'player', incoming: this.player });
        }
        this.foeTurn(events);
        return events;
      case 'item':
        // Items are resolved by the scene (it owns inventory); engine just lets
        // the foe attack. The scene pushes its own item-used event beforehand.
        this.foeTurn(events);
        return events;
      case 'move':
        return this.resolveMoveTurn(action.moveIndex);
      default:
        return events;
    }
  }

  /** A turn where the player uses a move; ordering decides who strikes first. */
  private resolveMoveTurn(moveIndex: number): BattleEvent[] {
    const events: BattleEvent[] = [];
    const playerMove = this.player.moves[moveIndex];
    if (!playerMove || playerMove.charges <= 0) {
      events.push({ type: 'no-charges' });
      return events;
    }

    const foeKnown = this.chooseFoeMove();
    const playerFirst = this.playerGoesFirst(playerMove.move, foeKnown?.move ?? null);

    if (playerFirst) {
      this.useMove('player', moveIndex, events);
      if (!this.handleFaints(events) && foeKnown) this.foeAttack(events);
    } else if (foeKnown) {
      this.foeAttack(events);
      if (!this.handleFaints(events)) this.useMove('player', moveIndex, events);
    } else {
      this.useMove('player', moveIndex, events);
    }

    this.handleFaints(events);
    return events;
  }

  /** The foe takes a free turn (used after a player switch/item). */
  private foeTurn(events: BattleEvent[]): void {
    if (this.foe.isFainted) return;
    this.foeAttack(events);
    this.handleFaints(events);
  }

  // --- Move execution ------------------------------------------------------

  private useMove(side: Side, moveIndex: number, events: BattleEvent[]): void {
    const attacker = side === 'player' ? this.player : this.foe;
    const defender = side === 'player' ? this.foe : this.player;
    const known = attacker.moves[moveIndex];
    if (!known || known.charges <= 0) return;
    known.charges--;

    events.push({ type: 'move-used', side, move: known.move });

    if (!rollHit(known.move.accuracy, this.rng)) {
      events.push({ type: 'miss', side });
      return;
    }

    if (known.move.category === 'status') {
      this.applyEffect(side, known.move, events);
      return;
    }

    const result = computeDamage(attacker, defender, known.move, this.rng);
    defender.takeDamage(result.damage);
    events.push({
      type: 'damage',
      side: side === 'player' ? 'foe' : 'player',
      amount: result.damage,
      effectiveness: result.effectiveness,
      crit: result.crit,
    });

    // Damaging moves can also carry an on-hit effect (e.g. a stat drop).
    if (known.move.effect && result.effectiveness > 0) {
      this.applyEffect(side, known.move, events);
    }
  }

  /** The foe picks and uses a move. */
  private foeAttack(events: BattleEvent[]): void {
    const choice = this.chooseFoeMoveIndex();
    if (choice < 0) {
      // No usable move — a flavourless "struggles" message keeps the turn moving.
      events.push({ type: 'message', text: `${this.foe.displayName} has no moves left!` });
      return;
    }
    this.useMove('foe', choice, events);
  }

  /**
   * Apply a move's `effect`. PixelKin's data uses two well-defined shapes here:
   *   { stat, stages, to }       — a stat-stage change (atk/def/spa/spd/spe/spe)
   *   { status, chance?, to }    — a status condition (narrated only; the full
   *                                status engine is out of scope for the slice)
   * The optional `chance` (0–100) gates whether the effect fires.
   */
  private applyEffect(side: Side, move: Move, events: BattleEvent[]): void {
    const effect = move.effect;
    if (!effect) return;
    const chance = typeof effect.chance === 'number' ? (effect.chance as number) : 100;
    if (this.rng() * 100 >= chance) return;

    const to = (effect.to as string) ?? 'foe';
    const targetSide: Side = to === 'self' ? side : side === 'player' ? 'foe' : 'player';
    const target = targetSide === 'player' ? this.player : this.foe;

    if (typeof effect.stat === 'string' && typeof effect.stages === 'number') {
      const stat = effect.stat as keyof typeof target.stages;
      const delta = effect.stages as number;
      const before = target.stages[stat];
      target.stages[stat] = Math.max(-6, Math.min(6, before + delta));
      const applied = target.stages[stat] - before;
      if (applied !== 0) {
        events.push({ type: 'stat-change', side: targetSide, stat: String(stat), delta: applied });
      }
      return;
    }

    if (typeof effect.status === 'string') {
      // Narrate the condition; we don't run a turn-by-turn status engine yet.
      events.push({ type: 'status', side: targetSide, status: effect.status as string });
    }
  }

  // --- Faints & foe switching ---------------------------------------------

  /**
   * Emit faint events and handle the consequences. Returns true if the turn
   * should stop early (battle ended, or a side needs to send out a new kin).
   */
  private handleFaints(events: BattleEvent[]): boolean {
    let interrupted = false;

    if (this.foe.isFainted) {
      events.push({ type: 'faint', side: 'foe' });
      if (this.foeParty.allFainted) {
        this.ended = true;
        this.outcome = 'win';
        return true;
      }
      // Trainer: auto-send the next kin. (Wild has only one, so this is trainer.)
      if (this.foeParty.promoteToHealthy()) {
        this.foe.resetBattleState();
        events.push({ type: 'switch', side: 'foe', incoming: this.foe });
      }
      interrupted = true;
    }

    if (this.player.isFainted) {
      events.push({ type: 'faint', side: 'player' });
      if (this.playerParty.allFainted) {
        this.ended = true;
        this.outcome = 'lose';
        return true;
      }
      // The scene must prompt the player to choose a replacement.
      interrupted = true;
    }

    return interrupted;
  }

  /** Called by the scene after the player picks a replacement for a fainted kin. */
  sendOut(partyIndex: number): BattleEvent[] {
    const events: BattleEvent[] = [];
    if (this.playerParty.switchTo(partyIndex)) {
      events.push({ type: 'switch', side: 'player', incoming: this.player });
    } else if (this.player.isFainted) {
      this.playerParty.promoteToHealthy();
      events.push({ type: 'switch', side: 'player', incoming: this.player });
    }
    return events;
  }

  // --- Turn ordering -------------------------------------------------------

  private playerGoesFirst(playerMove: Move, foeMove: Move | null): boolean {
    const fp = foeMove?.priority ?? -99;
    if (playerMove.priority !== fp) return playerMove.priority > fp;
    if (this.player.spe !== this.foe.spe) return this.player.spe > this.foe.spe;
    return this.rng() < 0.5;
  }

  // --- Foe AI --------------------------------------------------------------

  private chooseFoeMove(): { move: Move; charges: number } | null {
    const i = this.chooseFoeMoveIndex();
    return i < 0 ? null : this.foe.moves[i];
  }

  /**
   * Pick the foe's move: usually the highest expected-damage option, with a
   * small chance of a random usable move so it isn't perfectly predictable.
   */
  private chooseFoeMoveIndex(): number {
    const usable = this.foe.moves
      .map((k, i) => ({ k, i }))
      .filter((x) => x.k.charges > 0);
    if (usable.length === 0) return -1;

    if (this.rng() < 0.2) {
      return usable[Math.floor(this.rng() * usable.length)].i;
    }

    let bestIndex = usable[0].i;
    let bestScore = -1;
    for (const { k, i } of usable) {
      let score: number;
      if (k.move.category === 'status') {
        score = 1; // low but non-zero so status moves still get used sometimes
      } else {
        const r = computeDamage(this.foe, this.player, k.move, () => 0.5);
        score = r.damage;
      }
      if (score > bestScore) {
        bestScore = score;
        bestIndex = i;
      }
    }
    return bestIndex;
  }

  // --- Catch & Run ---------------------------------------------------------

  private resolveCatch(itemId: string, lampBonus = 1.0): BattleEvent[] {
    const events: BattleEvent[] = [];
    events.push({ type: 'item-used', itemId });
    events.push({ type: 'catch-throw' });

    const result = attemptCatch(this.foe, lampBonus, this.rng);
    events.push({ type: 'catch-wobble', count: result.wobbles });

    if (result.caught) {
      events.push({ type: 'catch-success' });
      this.ended = true;
      this.outcome = 'caught';
      this.caught = this.foe;
      return events;
    }

    events.push({ type: 'catch-break' });
    // A failed catch costs the turn: the wild kin gets a free hit.
    this.foeTurn(events);
    return events;
  }

  /** Override the lamp bonus used for catch (the scene knows the item's value). */
  catchWithBonus(itemId: string, lampBonus: number): BattleEvent[] {
    return this.resolveCatch(itemId, lampBonus);
  }

  private resolveRun(): BattleEvent[] {
    const events: BattleEvent[] = [];
    if (this.kind === 'trainer') {
      events.push({ type: 'run-fail' });
      events.push({ type: 'message', text: "There's no running from a warden's challenge!" });
      return events;
    }

    // Speed-based flee odds (always at least a fair chance).
    const playerSpe = Math.max(1, this.player.spe);
    const foeSpe = Math.max(1, this.foe.spe);
    const odds = playerSpe >= foeSpe ? 1 : 0.4 + 0.5 * (playerSpe / foeSpe);

    if (this.rng() < odds) {
      events.push({ type: 'run-success' });
      this.ended = true;
      this.outcome = 'fled';
      return events;
    }

    events.push({ type: 'run-fail' });
    this.foeTurn(events);
    return events;
  }
}
