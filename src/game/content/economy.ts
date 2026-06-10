/**
 * Economy constants & helpers — the single place the wick economy's tuning
 * lives in code. The design (rationale, full price list, payout classes, the
 * per-region earnings budget) is docs/mechanics/10-economy.md; the numbers
 * here must match it, and any change here must re-run the progression model
 * (`node tools/balance/progression.mjs`) so the curve stays validated.
 *
 * The currency is the WICK: waxed, brass-capped lamp-wicks, bundled and traded
 * — the one thing everyone in a darkened land always needs. Tinderwick minted
 * the custom (and took its name from it).
 */
import type { ItemDef, TrainerDef } from './types';

/** A new Wayfarer's pocket wicks (counted out by the keeper at home). */
export const STARTING_WICKS = 250;

/** Shops buy back at half price (classic genre rate, easy to reason about). */
export const SELL_RATE = 0.5;

/**
 * What a shop pays for one of `def`. Valuables carry an explicit `sell`;
 * anything else sellable derives from price. No price and no sell = the shop
 * won't take it (key items, quest charms).
 */
export function sellValue(def: ItemDef): number {
  if (def.sell !== undefined) return def.sell;
  if (def.price !== undefined) return Math.max(1, Math.floor(def.price * SELL_RATE));
  return 0;
}

/** Wicks a defeated trainer pays (authored per-trainer; absent = none). */
export function trainerPayout(def: TrainerDef | undefined): number {
  return def?.payout ?? 0;
}

/**
 * The kind light that carries a fainted party home keeps a tithe of your
 * wicks (10%, rounded down — gentle, but losing is never free).
 */
export const FAINT_TITHE_RATE = 0.1;

export function faintTithe(wicks: number): number {
  return Math.max(0, Math.floor(wicks * FAINT_TITHE_RATE));
}

/** Display helper: "1,240w" reads cleanly in the 240px-wide UI. */
export function formatWicks(amount: number): string {
  return `${amount.toLocaleString('en-GB')}w`;
}
