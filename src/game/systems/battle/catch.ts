/**
 * Catch maths — coaxing a wild kin into your Lamp.
 *
 * Uses the genre's classic shake-check, adapted to PixelKin's data:
 *   a = ((3*maxHp - 2*hp) / (3*maxHp)) * catchRate * lampBonus
 *   b = floor(1048560 / floor(sqrt(floor(sqrt(floor(16711680 / a))))))
 * then four shake checks each succeed with probability b/65535. All four → the
 * kin is caught; otherwise it breaks free after that many wobbles. A weakened or
 * higher-rate kin (Lamp bonus from the item's `catch_bonus`) catches more often.
 * Catching is WILD-only — the engine never offers it in a trainer battle.
 */
import type { KinInstance } from '@game/systems/party/KinInstance';

export interface CatchResult {
  caught: boolean;
  /** Number of wobbles shown before resolving (0–3 on a break, 4 on a catch). */
  wobbles: number;
}

/**
 * Status multiplier (docs/mechanics/04-capture.md): a kin held still by Doze or
 * Chill is far easier to coax in (×2.5); any other affliction helps a little (×1.5).
 */
export function statusBonus(target: KinInstance): number {
  switch (target.status) {
    case 'doze':
    case 'chill':
      return 2.5;
    case 'none':
      return 1.0;
    default:
      return 1.5;
  }
}

/**
 * Resolve one Lamp throw. `lampBonus` is the charge's `catch_bonus` (a plain
 * vesperlamp throw = 1.0). Pass `rng` for deterministic tests.
 */
export function attemptCatch(
  target: KinInstance,
  lampBonus: number,
  rng: () => number = Math.random,
): CatchResult {
  const maxHp = target.maxHp;
  const hp = Math.max(1, target.hp);
  // Clamp to >= 1 so a data error (catchRate 0) can't make a kin uncatchable or
  // divide by zero below.
  const rate = Math.max(1, target.species.catchRate);

  const a =
    ((3 * maxHp - 2 * hp) / (3 * maxHp)) * rate * Math.max(0.1, lampBonus) * statusBonus(target);

  // A guaranteed catch when a >= 255 (very weak / very catchable).
  if (a >= 255) return { caught: true, wobbles: 4 };

  const inner = Math.floor(16711680 / a); // 255^3
  const b = Math.floor(1048560 / Math.floor(Math.sqrt(Math.floor(Math.sqrt(inner)))));

  let wobbles = 0;
  for (let i = 0; i < 4; i++) {
    if (Math.floor(rng() * 65536) < b) {
      wobbles++;
    } else {
      return { caught: false, wobbles };
    }
  }
  return { caught: true, wobbles: 4 };
}
