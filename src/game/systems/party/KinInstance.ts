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
import type { Species, Move, Stats } from '@game/data/dex';
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
  readonly species: Species;
  nickname?: string;
  level: number;
  exp: number;
  hp: number;
  status: KinStatus;
  readonly moves: KnownMove[];
  readonly caughtAt?: { map: string; tx: number; ty: number };

  /** Live stat-stage modifiers for the *current battle* (not persisted). */
  readonly stages: Stats = { hp: 0, atk: 0, def: 0, spa: 0, spd: 0, spe: 0 };

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
    return this.withStage(this.otherStat(this.species.stats.atk), this.stages.atk);
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
    return this.withStage(this.otherStat(this.species.stats.spe), this.stages.spe);
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

  /** Reset per-battle volatile state (stat stages). Call when (un)sending out. */
  resetBattleState(): void {
    this.stages.atk = 0;
    this.stages.def = 0;
    this.stages.spa = 0;
    this.stages.spd = 0;
    this.stages.spe = 0;
  }

  /**
   * Grant exp; level up (re-deriving stats and topping up the hp gain) and learn
   * new level-up moves as thresholds are crossed. Returns the levels gained and
   * the moves newly learned, so the caller can narrate them.
   */
  gainExp(amount: number): { levelsGained: number; learned: Move[] } {
    if (amount <= 0 || this.level >= MAX_LEVEL) return { levelsGained: 0, learned: [] };
    const startLevel = this.level;
    this.exp += Math.floor(amount);
    const newLevel = levelForExp(this.exp);
    const learned: Move[] = [];
    if (newLevel > startLevel) {
      const prevMax = this.maxHp;
      this.level = newLevel;
      // Carry the hp gain so a level-up feels like a small heal, not a reset.
      this.hp += this.maxHp - prevMax;
      for (let lv = startLevel + 1; lv <= newLevel; lv++) {
        learned.push(...this.learnMovesAt(lv));
      }
    }
    return { levelsGained: newLevel - startLevel, learned };
  }

  /** Learn (auto, oldest-replaced) any level-up moves taught at `level`. */
  private learnMovesAt(level: number): Move[] {
    const learned: Move[] = [];
    for (const entry of this.species.learnset.levelup) {
      if (entry.level !== level) continue;
      const move = MOVE_BY_ID.get(entry.move);
      if (!move) continue;
      if (this.moves.some((k) => k.move.id === move.id)) continue;
      if (this.moves.length < MAX_MOVES) {
        this.moves.push({ move, charges: move.charges });
      } else {
        // Replace the first slot (simple auto-learn; a proper UI prompt is later).
        this.moves[0] = { move, charges: move.charges };
      }
      learned.push(move);
    }
    return learned;
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
