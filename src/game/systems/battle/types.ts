/**
 * Battle types — the data the engine and the scene pass around.
 *
 * The engine is intentionally scene-agnostic: it resolves a turn into a list of
 * `BattleEvent`s (a tiny narration script) that the scene plays back as text,
 * sfx and HP-bar tweens. This keeps the combat maths testable and the UI thin.
 */
import type { KinInstance } from '@game/systems/party/KinInstance';
import type { Move } from '@game/data/dex';

/** Which side a combatant is on. */
export type Side = 'player' | 'foe';

/** A player's chosen action for the turn. */
export type BattleAction =
  | { kind: 'move'; moveIndex: number }
  | { kind: 'switch'; partyIndex: number }
  | { kind: 'item'; itemId: string }
  | { kind: 'catch'; itemId: string }
  | { kind: 'run' };

/**
 * One narratable beat of a turn. The scene renders these in order: show the
 * message, play the sfx, tween the affected side's HP bar to its new value.
 */
export type BattleEvent =
  | { type: 'message'; text: string }
  | { type: 'move-used'; side: Side; move: Move }
  | { type: 'damage'; side: Side; amount: number; effectiveness: number; crit: boolean }
  | { type: 'miss'; side: Side }
  | { type: 'no-charges' }
  | { type: 'stat-change'; side: Side; stat: string; delta: number }
  | { type: 'status'; side: Side; status: string }
  | { type: 'faint'; side: Side }
  | { type: 'switch'; side: Side; incoming: KinInstance }
  | { type: 'item-used'; itemId: string; healed?: number }
  | { type: 'catch-throw' }
  | { type: 'catch-wobble'; count: number }
  | { type: 'catch-success' }
  | { type: 'catch-break' }
  | { type: 'run-success' }
  | { type: 'run-fail' };

/** Effectiveness multiplier buckets, for messaging/sfx selection. */
export function effectivenessLabel(mult: number): 'none' | 'not' | 'normal' | 'super' {
  if (mult === 0) return 'none';
  if (mult < 1) return 'not';
  if (mult > 1) return 'super';
  return 'normal';
}
