/**
 * BattleEngine — scene-agnostic turn resolution.
 *
 * Holds the two active kin (player + foe), the player's Party, and (for trainer
 * fights) the foe's Party. Each public method resolves one player decision into
 * an ordered list of `BattleEvent`s that the scene narrates. The engine owns:
 *   - turn ordering (move priority, then speed, ties broken randomly),
 *   - damage + accuracy + crit via damage.ts,
 *   - the full effect layer: stat stages, the seven canon status conditions
 *     (pre-move gates, end-of-turn chip, cures — docs/mechanics/03-moves.md),
 *     and the move riders (drain/recoil/flinch/heal/screen/hazard/pivot),
 *   - faints and (trainer) the foe's auto-switch to its next kin,
 *   - the foe AI's move choice ('basic' route-trainer pick, or 'smart' for
 *     Lampwardens and bosses — see TrainerDef.ai),
 *   - wild catch + run.
 *
 * It deliberately does NOT touch Phaser; the BattleScene plays the events back.
 */
import type { Move } from '@game/data/dex';
import type { KinInstance } from '@game/systems/party/KinInstance';
import type { Party } from '@game/systems/party/Party';
import type { KinStatus } from '@game/systems/save/types';
import { computeDamage, rollHit } from './damage';
import { attemptCatch } from './catch';
import type { BattleAction, BattleEvent, Side } from './types';

export type BattleKind = 'wild' | 'trainer';
export type AiLevel = 'basic' | 'smart';

export interface EngineConfig {
  kind: BattleKind;
  playerParty: Party;
  /** Trainer's party (trainer battles) or a one-kin party (wild). */
  foeParty: Party;
  /** Foe move selection: 'basic' (default) or 'smart' (warden/boss tier). */
  ai?: AiLevel;
  rng?: () => number;
}

// Status tuning (the exact numbers behind 03-moves.md's table).
const DRENCH_SKIP = 0.25;
const NUMB_SKIP = 0.25;
const CHILL_THAW = 0.2;
const DAZZLE_SELF_HIT = 1 / 3;
const SCORCH_CHIP = 1 / 16; // of max hp, per turn
const BLIGHT_CHIP = 1 / 16; // × stacks (escalating), per turn
const HAZARD_CHIP = 1 / 8; // caltrops, on switch-in
const SCREEN_MULT = 0.5;

/** Per-side battlefield state (screens up, hazards laid on that side's field). */
interface FieldSide {
  screens: { physical: number; special: number }; // turns remaining
  caltrops: boolean;
}

export class BattleEngine {
  readonly kind: BattleKind;
  readonly playerParty: Party;
  readonly foeParty: Party;
  private readonly ai: AiLevel;
  private readonly rng: () => number;

  private field: Record<Side, FieldSide> = {
    player: { screens: { physical: 0, special: 0 }, caltrops: false },
    foe: { screens: { physical: 0, special: 0 }, caltrops: false },
  };

  /** Set true once a side has lost / fled / a catch succeeded. */
  ended = false;
  outcome: 'win' | 'lose' | 'caught' | 'fled' | null = null;
  caught: KinInstance | null = null;

  constructor(cfg: EngineConfig) {
    this.kind = cfg.kind;
    this.playerParty = cfg.playerParty;
    this.foeParty = cfg.foeParty;
    this.ai = cfg.ai ?? 'basic';
    this.rng = cfg.rng ?? Math.random;
    this.player.resetBattleState(this.rng);
    this.foe.resetBattleState(this.rng);
  }

  get player(): KinInstance {
    return this.playerParty.active;
  }
  get foe(): KinInstance {
    return this.foeParty.active;
  }

  private kinOf(side: Side): KinInstance {
    return side === 'player' ? this.player : this.foe;
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
          this.player.resetBattleState(this.rng);
          events.push({ type: 'switch', side: 'player', incoming: this.player });
          this.applyEntryHazard('player', events);
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

    if (!this.handleFaints(events)) this.endOfTurn(events);
    return events;
  }

  /** The foe takes a free turn (used after a player switch/item). */
  private foeTurn(events: BattleEvent[]): void {
    if (!this.foe.isFainted) {
      this.foeAttack(events);
    }
    if (!this.handleFaints(events)) this.endOfTurn(events);
  }

  // --- Status: pre-move gate -------------------------------------------------

  /**
   * The status check before a kin may act. Returns true when the action is
   * blocked (and pushes the narration). Spends no move charges — a dozing kin
   * keeps its charge, like the classics.
   */
  private preMoveGate(side: Side, events: BattleEvent[]): boolean {
    const kin = this.kinOf(side);

    if (kin.flinched) {
      kin.flinched = false;
      events.push({ type: 'flinch', side });
      return true;
    }

    switch (kin.status) {
      case 'doze': {
        kin.dozeTurns--;
        if (kin.dozeTurns <= 0) {
          kin.cureStatus();
          events.push({ type: 'status-wake', side });
          return false;
        }
        events.push({ type: 'status-block', side, status: 'doze' });
        return true;
      }
      case 'chill': {
        if (this.rng() < CHILL_THAW) {
          kin.cureStatus();
          events.push({ type: 'status-thaw', side });
          return false;
        }
        events.push({ type: 'status-block', side, status: 'chill' });
        return true;
      }
      case 'numb': {
        if (this.rng() < NUMB_SKIP) {
          events.push({ type: 'status-block', side, status: 'numb' });
          return true;
        }
        return false;
      }
      case 'drench': {
        if (this.rng() < DRENCH_SKIP) {
          events.push({ type: 'status-block', side, status: 'drench' });
          return true;
        }
        return false;
      }
      case 'dazzle': {
        if (this.rng() < DAZZLE_SELF_HIT) {
          // A 40-power typeless hit against itself (own atk vs own def).
          const baseStep = Math.floor((2 * kin.level) / 5) + 2;
          const dmg = Math.max(
            1,
            Math.floor(Math.floor(Math.floor((baseStep * 40 * kin.atk) / kin.def) / 50) + 2),
          );
          kin.takeDamage(dmg);
          events.push({ type: 'confusion-hit', side, amount: dmg });
          return true;
        }
        return false;
      }
      default:
        return false;
    }
  }

  // --- Move execution ------------------------------------------------------

  private useMove(side: Side, moveIndex: number, events: BattleEvent[]): void {
    const attacker = this.kinOf(side);
    const defender = this.kinOf(side === 'player' ? 'foe' : 'player');
    const defenderSide: Side = side === 'player' ? 'foe' : 'player';
    const known = attacker.moves[moveIndex];
    if (!known || known.charges <= 0) return;

    if (this.preMoveGate(side, events)) return;
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
    let dealt = result.damage;
    // A screen on the defender's side halves that category's damage.
    const screens = this.field[defenderSide].screens;
    const screened =
      known.move.category === 'physical' ? screens.physical > 0 : screens.special > 0;
    if (screened && result.effectiveness > 0) dealt = Math.max(1, Math.floor(dealt * SCREEN_MULT));
    defender.takeDamage(dealt);
    events.push({
      type: 'damage',
      side: defenderSide,
      amount: dealt,
      effectiveness: result.effectiveness,
      crit: result.crit,
    });

    if (result.effectiveness > 0) {
      // An Ember hit thaws a chilled target (canon: 03-moves.md).
      if (defender.status === 'chill' && known.move.type === 'Ember' && dealt > 0) {
        defender.cureStatus();
        events.push({ type: 'status-thaw', side: defenderSide });
      }

      // Damage-fraction riders resolve off what was actually dealt.
      const effect = known.move.effect;
      if (typeof effect?.drain === 'number' && dealt > 0) {
        const healed = attacker.heal(Math.max(1, Math.floor(dealt * effect.drain)));
        if (healed > 0) events.push({ type: 'drain', side, amount: healed });
      }
      if (typeof effect?.recoil === 'number' && dealt > 0) {
        const recoil = Math.max(1, Math.floor(dealt * effect.recoil));
        attacker.takeDamage(recoil);
        events.push({ type: 'recoil', side, amount: recoil });
      }

      // Other on-hit riders (stat drops, status, flinch).
      if (effect && !defender.isFainted) this.applyEffect(side, known.move, events);
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
   * Apply a move's `effect` riders. The data's shapes (docs/mechanics/03-moves.md):
   *   { stat, stages, chance?, to }   — stat-stage change
   *   { status, chance?, to }         — one of the seven canon conditions
   *   { flinch: n }                   — n% chance the target flinches this turn
   *   { heal: f, to: 'self' }         — restore f × max hp ('needs' degrades to plain heal)
   *   { selfDoze: n }                 — Rest Up: full heal traded for n turns of doze
   *   { cure: true, to }              — cleanse the target's status
   *   { screen: 'physical'|'special', turns } — halve that damage on the user's side
   *   { hazard: 'caltrops' }          — lay caltrops on the opponent's field
   *   { pivot: true }                 — the user swaps out after the move
   * (drain/recoil/highCrit are resolved in useMove/damage.ts off the damage dealt.)
   */
  private applyEffect(side: Side, move: Move, events: BattleEvent[]): void {
    const effect = move.effect;
    if (!effect) return;
    const chance = typeof effect.chance === 'number' ? (effect.chance as number) : 100;
    if (this.rng() * 100 >= chance) return;

    const to = (effect.to as string) ?? 'foe';
    const targetSide: Side = to === 'self' ? side : side === 'player' ? 'foe' : 'player';
    const target = this.kinOf(targetSide);

    if (typeof effect.stat === 'string' && typeof effect.stages === 'number') {
      const stat = effect.stat as keyof typeof target.stages;
      const delta = effect.stages as number;
      const before = target.stages[stat];
      target.stages[stat] = Math.max(-6, Math.min(6, before + delta));
      const applied = target.stages[stat] - before;
      if (applied !== 0) {
        events.push({ type: 'stat-change', side: targetSide, stat: String(stat), delta: applied });
      }
    }

    if (typeof effect.selfDoze === 'number') {
      // Rest Up: trade consciousness for a full mend.
      const self = this.kinOf(side);
      self.cureStatus();
      const healed = self.heal(self.maxHp);
      if (healed > 0) events.push({ type: 'heal', side, amount: healed });
      self.status = 'doze';
      self.dozeTurns = Math.max(1, Math.floor(effect.selfDoze as number));
      events.push({ type: 'status', side, status: 'doze' });
    } else if (typeof effect.heal === 'number') {
      const healed = target.heal(Math.max(1, Math.floor(target.maxHp * (effect.heal as number))));
      if (healed > 0) events.push({ type: 'heal', side: targetSide, amount: healed });
    }

    if (typeof effect.status === 'string' && typeof effect.selfDoze !== 'number') {
      const applied = target.applyStatus(effect.status as KinStatus, this.rng);
      if (applied) {
        events.push({ type: 'status', side: targetSide, status: effect.status as string });
      }
    }

    if (typeof effect.flinch === 'number' && this.rng() * 100 < (effect.flinch as number)) {
      // Only bites if the target hasn't acted yet this turn; the flag clears at
      // end of turn either way.
      target.flinched = true;
    }

    if (effect.cure === true) {
      if (target.status !== 'none') {
        target.cureStatus();
        events.push({ type: 'status-cure', side: targetSide });
      }
    }

    if (typeof effect.screen === 'string' && typeof effect.turns === 'number') {
      const key = effect.screen === 'physical' ? 'physical' : 'special';
      this.field[side].screens[key] = Math.max(
        this.field[side].screens[key],
        effect.turns as number,
      );
      events.push({ type: 'screen-up', side, screen: key });
    }

    if (typeof effect.hazard === 'string') {
      const other: Side = side === 'player' ? 'foe' : 'player';
      if (!this.field[other].caltrops) {
        this.field[other].caltrops = true;
        events.push({ type: 'hazard-set', side: other });
      }
    }

    if (effect.pivot === true) {
      this.resolvePivot(side, events);
    }
  }

  /** Swap Out: the user retreats after striking. The foe AI picks a teammate;
   *  the player's choice is surfaced to the scene via the 'pivot' event. */
  private resolvePivot(side: Side, events: BattleEvent[]): void {
    const party = side === 'player' ? this.playerParty : this.foeParty;
    const healthyElsewhere = party.all.some((k, i) => !k.isFainted && i !== party.activeSlot);
    if (!healthyElsewhere) return;
    events.push({ type: 'pivot', side });
    if (side === 'foe') {
      const options = party.all
        .map((k, i) => ({ k, i }))
        .filter((x) => !x.k.isFainted && x.i !== party.activeSlot);
      const pick = options[Math.floor(this.rng() * options.length)];
      if (pick && party.switchTo(pick.i)) {
        this.foe.resetBattleState(this.rng);
        events.push({ type: 'switch', side: 'foe', incoming: this.foe });
        this.applyEntryHazard('foe', events);
      }
    }
    // The player's pivot switch is prompted by the scene (it owns the menu);
    // see BattleScene's handling of the 'pivot' event.
  }

  /** Called by the scene when the player resolves a pivot with a chosen teammate. */
  pivotSwitch(partyIndex: number): BattleEvent[] {
    const events: BattleEvent[] = [];
    if (this.playerParty.switchTo(partyIndex)) {
      this.player.resetBattleState(this.rng);
      events.push({ type: 'switch', side: 'player', incoming: this.player });
      this.applyEntryHazard('player', events);
    }
    return events;
  }

  // --- End of turn -----------------------------------------------------------

  /** One tidy place for everything that happens after both sides acted. */
  private endOfTurn(events: BattleEvent[]): void {
    if (this.ended) return;

    for (const side of ['player', 'foe'] as const) {
      const kin = this.kinOf(side);
      if (kin.isFainted) continue;

      if (kin.status === 'scorch') {
        const chip = Math.max(1, Math.floor(kin.maxHp * SCORCH_CHIP));
        kin.takeDamage(chip);
        events.push({ type: 'status-tick', side, status: 'scorch', amount: chip });
      } else if (kin.status === 'blight') {
        const chip = Math.max(1, Math.floor(kin.maxHp * BLIGHT_CHIP * Math.max(1, kin.blightStacks)));
        kin.blightStacks++;
        kin.takeDamage(chip);
        events.push({ type: 'status-tick', side, status: 'blight', amount: chip });
      }

      kin.flinched = false;

      // Screens burn down at end of turn.
      const screens = this.field[side].screens;
      for (const key of ['physical', 'special'] as const) {
        if (screens[key] > 0) {
          screens[key]--;
          if (screens[key] === 0) events.push({ type: 'screen-fade', side, screen: key });
        }
      }
    }

    this.handleFaints(events);
  }

  /** Caltrops bite whoever switches in on a seeded field. */
  private applyEntryHazard(side: Side, events: BattleEvent[]): void {
    if (!this.field[side].caltrops) return;
    const kin = this.kinOf(side);
    const chip = Math.max(1, Math.floor(kin.maxHp * HAZARD_CHIP));
    kin.takeDamage(chip);
    events.push({ type: 'hazard-hurt', side, amount: chip });
    this.handleFaints(events);
  }

  // --- Faints & foe switching ---------------------------------------------

  /**
   * Emit faint events and handle the consequences. Returns true if the turn
   * should stop early (battle ended, or a side needs to send out a new kin).
   */
  private handleFaints(events: BattleEvent[]): boolean {
    let interrupted = false;

    if (this.foe.isFainted && !this.ended) {
      events.push({ type: 'faint', side: 'foe' });
      if (this.foeParty.allFainted) {
        this.ended = true;
        this.outcome = 'win';
        return true;
      }
      // Trainer: auto-send the next kin. (Wild has only one, so this is trainer.)
      if (this.foeParty.promoteToHealthy()) {
        this.foe.resetBattleState(this.rng);
        events.push({ type: 'switch', side: 'foe', incoming: this.foe });
        this.applyEntryHazard('foe', events);
      }
      interrupted = true;
    }

    if (this.player.isFainted && !this.ended) {
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
      this.player.resetBattleState(this.rng);
      events.push({ type: 'switch', side: 'player', incoming: this.player });
      this.applyEntryHazard('player', events);
    } else if (this.player.isFainted) {
      this.playerParty.promoteToHealthy();
      this.player.resetBattleState(this.rng);
      events.push({ type: 'switch', side: 'player', incoming: this.player });
      this.applyEntryHazard('player', events);
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

  private chooseFoeMoveIndex(): number {
    return this.ai === 'smart' ? this.chooseSmartMoveIndex() : this.chooseBasicMoveIndex();
  }

  /**
   * Basic pick (route trainers, wild): usually the highest expected-damage
   * option, with a small chance of a random usable move so it isn't perfectly
   * predictable.
   */
  private chooseBasicMoveIndex(): number {
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

  /**
   * Warden/boss pick (TrainerDef.ai = 'smart'): plays the matchup, not just the
   * biggest number — never wastes a turn on an immune target, finishes a kill
   * when it can, and opens with its status/utility kit while the fight is young.
   */
  private chooseSmartMoveIndex(): number {
    const usable = this.foe.moves
      .map((k, i) => ({ k, i }))
      .filter((x) => x.k.charges > 0);
    if (usable.length === 0) return -1;

    let bestIndex = usable[0].i;
    let bestScore = -Infinity;
    for (const { k, i } of usable) {
      let score: number;
      if (k.move.category === 'status') {
        score = this.scoreSmartStatus(k.move);
      } else {
        const r = computeDamage(this.foe, this.player, k.move, () => 0.5);
        if (r.effectiveness === 0) {
          score = -1; // never thump an immune target
        } else {
          score = r.damage;
          if (r.damage >= this.player.hp) score *= 3; // take the KO when offered
        }
      }
      // A whisper of variance so two same-score moves don't always tie the same way.
      score += this.rng() * 0.5;
      if (score > bestScore) {
        bestScore = score;
        bestIndex = i;
      }
    }
    return bestIndex;
  }

  /** How much this status/utility move is worth right now, in damage-points. */
  private scoreSmartStatus(move: Move): number {
    const e = move.effect ?? {};
    const earlyFight = this.foe.hpRatio > 0.6;
    const benchmark = Math.max(8, Math.floor(this.player.maxHp / 6));

    // Afflicting a clean target early is worth about a strong hit.
    if (typeof e.status === 'string') {
      if (this.player.status !== 'none') return 0; // wasted — single-status rule
      return earlyFight ? benchmark * 1.4 : benchmark * 0.5;
    }
    // Screens/buffs open the fight; they're dead weight when desperate.
    if (typeof e.screen === 'string' || (typeof e.stat === 'string' && (e.to as string) === 'self')) {
      return earlyFight ? benchmark : 0;
    }
    // Heals matter when hurt.
    if (typeof e.heal === 'number' || typeof e.selfDoze === 'number') {
      return this.foe.hpRatio < 0.45 ? benchmark * 2 : 0;
    }
    // Debuffs are a mild early play.
    if (typeof e.stat === 'string') {
      return earlyFight ? benchmark * 0.8 : benchmark * 0.2;
    }
    return 1;
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

  /** Override the lamp bonus used for catch (the scene knows the charge's value). */
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
