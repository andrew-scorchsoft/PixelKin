/**
 * KinInstance — a single owned/wild kin at runtime.
 *
 * Wraps a `Species` (from the dex) at a given level and tracks the things that
 * change in play: current hp, exp, the moves it actually knows (with remaining
 * charges) and a status. Derived stats (max hp, atk/def/...) are computed from
 * the species' base stats and the level using the classic handheld formula, so
 * a kin's power scales the way the genre's players expect.
 *
 * Level / stat formula (documented, intentionally simple — no IV/EV/nature):
 *   HP    = floor(2 * base.hp  * level / 100) + level + 10
 *   other = floor(2 * base.X   * level / 100) + 5
 * Exp-to-next uses a cubic curve: expForLevel(L) = L^3 (medium-fast-ish).
 *
 * It (de)serialises to `KinInstanceData` (save/types.ts) via `toData()` /
 * `KinInstance.fromData()`, so party state round-trips through a save unchanged.
 */
import type { Species, Move, Stats, Kindling } from '@game/data/dex';
import { SPECIES_BY_ID, MOVE_BY_ID } from '@game/data/dex';
import type { KinInstanceData, KinStatus } from '@game/systems/save/types';

export const MAX_MOVES = 4;
export const MAX_LEVEL = 100;

/** A known move plus how many charges (PP) it has left. */
export interface KnownMove {
  move: Move;
  charges: number;
}

/** Exp required to *reach* the given level (cubic). Level 1 = 0. */
export function expForLevel(level: number): number {
  return level * level * level;
}

/** The level a given total-exp value corresponds to. */
export function levelForExp(exp: number): number {
  let level = 1;
  while (level < MAX_LEVEL && exp >= expForLevel(level + 1)) level++;
  return level;
}

export class KinInstance {
  species: Species;
  nickname?: string;
  level: number;
  exp: number;
  hp: number;
  status: KinStatus;
  readonly moves: KnownMove[];
  readonly caughtAt?: { map: string; tx: number; ty: number };

  /** Live stat-stage modifiers for the *current battle* (not persisted). */
  readonly stages: Stats = { hp: 0, atk: 0, def: 0, spa: 0, spd: 0, spe: 0 };

  // Per-battle volatile status counters (not persisted; reset on send-out).
  /** Turns of doze left (rolled 1–3 when the status lands or battle starts). */
  dozeTurns = 0;
  /** Blight's escalating chip counter (damage = stacks/16 of max hp). */
  blightStacks = 0;
  /** Set when flinched this turn (skips the next action, then clears). */
  flinched = false;

  private constructor(
    species: Species,
    level: number,
    opts: {
      nickname?: string;
      exp?: number;
      hp?: number;
      status?: KinStatus;
      moves?: KnownMove[];
      caughtAt?: { map: string; tx: number; ty: number };
    } = {},
  ) {
    this.species = species;
    this.level = Math.max(1, Math.min(MAX_LEVEL, Math.floor(level)));
    this.nickname = opts.nickname;
    this.exp = opts.exp ?? expForLevel(this.level);
    this.status = opts.status ?? 'none';
    this.caughtAt = opts.caughtAt;
    this.moves = opts.moves ?? defaultMovesFor(species, this.level);
    this.hp = opts.hp ?? this.maxHp;
    this.hp = Math.max(0, Math.min(this.hp, this.maxHp));
  }

  // --- Factories -----------------------------------------------------------

  /** Build a fresh kin of `speciesId` at `level` with full hp and level-up moves. */
  static create(speciesId: number, level: number): KinInstance {
    const species = SPECIES_BY_ID.get(speciesId);
    if (!species) throw new Error(`Unknown species id ${speciesId}`);
    return new KinInstance(species, level);
  }

  /** Restore from persisted save data (round-trips with toData()). */
  static fromData(data: KinInstanceData): KinInstance {
    const species = SPECIES_BY_ID.get(data.species_id);
    if (!species) throw new Error(`Unknown species id ${data.species_id}`);
    const moves: KnownMove[] = [];
    for (const m of data.moves) {
      const move = MOVE_BY_ID.get(m.id);
      if (move) moves.push({ move, charges: Math.max(0, Math.min(m.charges, move.charges)) });
    }
    const inst = new KinInstance(species, data.level, {
      nickname: data.nickname,
      exp: data.exp,
      status: data.status ?? 'none',
      moves: moves.length > 0 ? moves : defaultMovesFor(species, data.level),
      caughtAt: data.caught_at,
    });
    inst.hp = Math.max(0, Math.min(data.hp, inst.maxHp));
    return inst;
  }

  /** Serialise to the persisted shape. */
  toData(): KinInstanceData {
    const data: KinInstanceData = {
      species_id: this.species.id,
      level: this.level,
      exp: this.exp,
      hp: this.hp,
      moves: this.moves.map((k) => ({ id: k.move.id, charges: k.charges })),
    };
    if (this.nickname) data.nickname = this.nickname;
    if (this.status !== 'none') data.status = this.status;
    if (this.caughtAt) data.caught_at = this.caughtAt;
    return data;
  }

  // --- Derived stats -------------------------------------------------------

  get displayName(): string {
    return this.nickname ?? this.species.name;
  }

  get maxHp(): number {
    return Math.floor((2 * this.species.stats.hp * this.level) / 100) + this.level + 10;
  }

  private otherStat(base: number): number {
    return Math.floor((2 * base * this.level) / 100) + 5;
  }

  /** Effective stat after applying this battle's stat-stage modifier. */
  private withStage(value: number, stage: number): number {
    // Classic +/-6 stage multiplier table, clamped.
    const s = Math.max(-6, Math.min(6, stage));
    const mult = s >= 0 ? (2 + s) / 2 : 2 / (2 - s);
    return Math.max(1, Math.floor(value * mult));
  }

  get atk(): number {
    const base = this.withStage(this.otherStat(this.species.stats.atk), this.stages.atk);
    // Scorch halves physical attack (canon: docs/mechanics/03-moves.md). Kept in
    // the getter so the foe AI's damage estimates see it too.
    return this.status === 'scorch' ? Math.max(1, Math.floor(base / 2)) : base;
  }
  get def(): number {
    return this.withStage(this.otherStat(this.species.stats.def), this.stages.def);
  }
  get spa(): number {
    return this.withStage(this.otherStat(this.species.stats.spa), this.stages.spa);
  }
  get spd(): number {
    return this.withStage(this.otherStat(this.species.stats.spd), this.stages.spd);
  }
  get spe(): number {
    const base = this.withStage(this.otherStat(this.species.stats.spe), this.stages.spe);
    // Numb and Drench both slow (canon: −Speed) — halved, like the classics.
    return this.status === 'numb' || this.status === 'drench'
      ? Math.max(1, Math.floor(base / 2))
      : base;
  }

  get isFainted(): boolean {
    return this.hp <= 0;
  }

  get hpRatio(): number {
    return this.maxHp <= 0 ? 0 : this.hp / this.maxHp;
  }

  // --- Mutators ------------------------------------------------------------

  /** Heal up to maxHp; returns hp actually restored. */
  heal(amount: number): number {
    const before = this.hp;
    this.hp = Math.min(this.maxHp, this.hp + Math.max(0, amount));
    return this.hp - before;
  }

  fullHeal(): void {
    this.hp = this.maxHp;
    this.status = 'none';
    for (const k of this.moves) k.charges = k.move.charges;
  }

  /** Apply damage; returns hp actually lost. Never goes below 0. */
  takeDamage(amount: number): number {
    const before = this.hp;
    this.hp = Math.max(0, this.hp - Math.max(0, Math.floor(amount)));
    return before - this.hp;
  }

  /** Reset per-battle volatile state (stat stages + status counters). Call when (un)sending out. */
  resetBattleState(rng: () => number = Math.random): void {
    this.stages.atk = 0;
    this.stages.def = 0;
    this.stages.spa = 0;
    this.stages.spd = 0;
    this.stages.spe = 0;
    this.flinched = false;
    this.blightStacks = this.status === 'blight' ? 1 : 0;
    // A kin that arrives already dozing gets a fresh 1–3 turn nap counter.
    this.dozeTurns = this.status === 'doze' ? 1 + Math.floor(rng() * 3) : 0;
  }

  /**
   * Apply a major status. The single-status rule: a kin already afflicted keeps
   * its current condition (returns false). Sets the volatile counters.
   */
  applyStatus(status: KinStatus, rng: () => number = Math.random): boolean {
    if (status === 'none' || this.status !== 'none') return false;
    this.status = status;
    if (status === 'doze') this.dozeTurns = 1 + Math.floor(rng() * 3);
    if (status === 'blight') this.blightStacks = 1;
    return true;
  }

  /** Clear any major status (cures, thaws, wakes). */
  cureStatus(): void {
    this.status = 'none';
    this.dozeTurns = 0;
    this.blightStacks = 0;
  }

  /**
   * Grant exp; level up (re-deriving stats and topping up the hp gain) and learn
   * new level-up moves as thresholds are crossed. Moves that fit a free slot are
   * learned automatically (`learned`); when all four slots are taken the move
   * lands in `pending` instead — the caller runs MoveLearnPrompt so the PLAYER
   * chooses what to set aside (never a silent overwrite).
   */
  gainExp(amount: number): {
    levelsGained: number;
    learned: Move[];
    pending: Move[];
    /** Set when a level threshold crossed this kin's kindling trigger — the
     *  caller runs KindlePrompt so the PLAYER witnesses (or defers) the kindle. */
    kindleReady: Kindling | null;
  } {
    if (amount <= 0 || this.level >= MAX_LEVEL)
      return { levelsGained: 0, learned: [], pending: [], kindleReady: null };
    const startLevel = this.level;
    this.exp += Math.floor(amount);
    const newLevel = levelForExp(this.exp);
    const learned: Move[] = [];
    const pending: Move[] = [];
    if (newLevel > startLevel) {
      const prevMax = this.maxHp;
      this.level = newLevel;
      // Carry the hp gain so a level-up feels like a small heal, not a reset.
      this.hp += this.maxHp - prevMax;
      for (let lv = startLevel + 1; lv <= newLevel; lv++) {
        for (const entry of this.species.learnset.levelup) {
          if (entry.level !== lv) continue;
          const move = MOVE_BY_ID.get(entry.move);
          if (!move || this.knowsMove(move.id) || pending.some((m) => m.id === move.id)) continue;
          if (this.learnMove(move)) learned.push(move);
          else pending.push(move);
        }
      }
    }
    return {
      levelsGained: newLevel - startLevel,
      learned,
      pending,
      kindleReady: newLevel > startLevel ? this.kindleReady() : null,
    };
  }

  // --- Kindling --------------------------------------------------------------

  /** The level-triggered kindling this kin currently qualifies for, if any. */
  kindleReady(): Kindling | null {
    const k = this.species.kindling;
    if (!k) return null;
    if (k.trigger.kind !== 'level') return null; // stone/bond/location/time go through items/scripts
    if (typeof k.trigger.level !== 'number' || this.level < k.trigger.level) return null;
    return SPECIES_BY_ID.has(k.into) ? k : null;
  }

  /** The kindling a Kindlestone-type item would fire on this kin, if any. */
  kindleByItem(itemId: string): Kindling | null {
    const k = this.species.kindling;
    if (!k || k.trigger.kind !== 'stone' || k.trigger.item !== itemId) return null;
    return SPECIES_BY_ID.has(k.into) ? k : null;
  }

  /**
   * Kindle into the next stage: swap the species, keep level/exp/nickname, carry
   * the hp *gain* (a kindle is a bloom, never a reset), and surface any kindling
   * moves the new form is due — returned like gainExp's learned/pending so the
   * caller can run the same MoveLearnPrompt flow.
   */
  applyKindle(kindling: Kindling): { learned: Move[]; pending: Move[] } {
    const next = SPECIES_BY_ID.get(kindling.into);
    const learned: Move[] = [];
    const pending: Move[] = [];
    if (!next) return { learned, pending };
    const prevMax = this.maxHp;
    this.species = next;
    this.hp = Math.min(this.maxHp, this.hp + Math.max(0, this.maxHp - prevMax));
    for (const id of next.learnset.kindling) {
      const move = MOVE_BY_ID.get(id);
      if (!move || this.knowsMove(move.id)) continue;
      if (this.learnMove(move)) learned.push(move);
      else pending.push(move);
    }
    return { learned, pending };
  }

  // --- Taught moves (Star-charts + the move-learn prompt share these) ----------

  knowsMove(moveId: string): boolean {
    return this.moves.some((k) => k.move.id === moveId);
  }

  /**
   * Whether this kin can study a Star-chart for `move`: it shares the move's
   * type, the move is Plain (any kin may read a plain figure), or the move is
   * already somewhere in its species learnset. Returns why not, for narration.
   */
  canStudy(move: Move): 'ok' | 'knows' | 'type' {
    if (this.knowsMove(move.id)) return 'knows';
    if (move.type === 'Plain') return 'ok';
    if (this.species.types.includes(move.type)) return 'ok';
    const ls = this.species.learnset;
    const inLearnset =
      ls.levelup.some((e) => e.move === move.id) ||
      ls.kindling.includes(move.id) ||
      ls.tutor.includes(move.id);
    return inLearnset ? 'ok' : 'type';
  }

  /** Learn into a free slot. Returns false when all four slots are taken. */
  learnMove(move: Move): boolean {
    if (this.knowsMove(move.id) || this.moves.length >= MAX_MOVES) return false;
    this.moves.push({ move, charges: move.charges });
    return true;
  }

  /** Overwrite a known-move slot (the "forget which?" choice). */
  replaceMove(slot: number, move: Move): void {
    if (slot < 0 || slot >= this.moves.length) return;
    this.moves[slot] = { move, charges: move.charges };
  }

}

/** The up-to-4 most recent level-up moves a species knows at `level`. */
export function defaultMovesFor(species: Species, level: number): KnownMove[] {
  const eligible = species.learnset.levelup
    .filter((e) => e.level <= level)
    .map((e) => MOVE_BY_ID.get(e.move))
    .filter((m): m is Move => !!m);
  // Keep the last MAX_MOVES learned (most recent / strongest), de-duplicated.
  const picked: Move[] = [];
  for (const m of eligible) {
    if (!picked.some((p) => p.id === m.id)) picked.push(m);
  }
  const last = picked.slice(-MAX_MOVES);
  return last.map((move) => ({ move, charges: move.charges }));
}
