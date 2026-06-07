/**
 * Damage maths — the genre's standard formula, trimmed to PixelKin's scope.
 *
 *   base   = floor( floor( floor(2*L/5 + 2) * power * A/D ) / 50 ) + 2
 *   damage = floor( base * STAB * typeEff * crit * variance )
 *
 * where A/D is atk/def for physical moves and spa/spd for special moves, STAB
 * is 1.5 when the move's type is one of the attacker's types, crit is 1.5 (with
 * a 1/16 chance), and variance is a uniform 0.85–1.00 roll. Type effectiveness
 * comes from the shared chart via `typeEffectiveness` so it always agrees with
 * the data and the balance tooling.
 */
import type { Move, MoveType } from '@game/data/dex';
import { typeEffectiveness } from '@game/data/dex';
import type { KinInstance } from '@game/systems/party/KinInstance';

export const CRIT_CHANCE = 1 / 16;
const CRIT_MULT = 1.5;
const STAB_MULT = 1.5;

export interface DamageResult {
  /** Final damage dealt (>= 0). */
  damage: number;
  /** Type-effectiveness multiplier (0, 0.25, 0.5, 1, 2, 4). */
  effectiveness: number;
  /** Whether this hit critically. */
  crit: boolean;
}

/** STAB multiplier: 1.5 if the move shares a type with the attacker. */
function stab(attacker: KinInstance, moveType: MoveType): number {
  if (moveType === 'Plain') return 1;
  return attacker.species.types.includes(moveType) ? STAB_MULT : 1;
}

/**
 * Compute the damage `move` deals from `attacker` to `defender`.
 * Pass `rng` for deterministic tests (defaults to Math.random).
 */
export function computeDamage(
  attacker: KinInstance,
  defender: KinInstance,
  move: Move,
  rng: () => number = Math.random,
): DamageResult {
  const effectiveness = typeEffectiveness(move.type, defender.species.types);

  if (move.category === 'status' || move.power <= 0 || effectiveness === 0) {
    return { damage: 0, effectiveness, crit: false };
  }

  const physical = move.category === 'physical';
  const atk = physical ? attacker.atk : attacker.spa;
  const def = physical ? defender.def : defender.spd;

  const level = attacker.level;
  const baseStep = Math.floor((2 * level) / 5) + 2;
  let base = Math.floor((Math.floor((baseStep * move.power * atk) / def)) / 50) + 2;

  const crit = rng() < CRIT_CHANCE;
  const variance = 0.85 + rng() * 0.15;
  base = base * stab(attacker, move.type) * effectiveness * (crit ? CRIT_MULT : 1) * variance;

  return { damage: Math.max(1, Math.floor(base)), effectiveness, crit };
}

/** Roll whether a move with `accuracy` (0–100; 0 means "always hits"/self) lands. */
export function rollHit(accuracy: number, rng: () => number = Math.random): boolean {
  if (accuracy <= 0 || accuracy >= 100) return true;
  return rng() * 100 < accuracy;
}
