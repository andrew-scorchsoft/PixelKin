/**
 * FlagStore — the single owner of world progression flags.
 *
 * Flags are the game's memory: "talked to the mentor", "has the vesperlamp", "earned
 * the Ember Gleam", "this once-trigger has fired". Everything that gates content
 * (warps, triggers, NPC visibility, encounters) reads flags through here, and only
 * triggers/cutscenes/battles write them. Backed by the same `Record<WorldFlag,bool>`
 * that lives in WorldSnapshot, so saving is just handing this map over.
 */
import type { WorldFlag } from '@game/data/world/types';

/**
 * The Skyweave Crown's derived flags. A quadrant's crown is HELD, never set by
 * content: it derives from its two Gleams, and the hub from all four crowns
 * (walkthrough spine §2 — "engine-set, do not hand-set"). Deriving inside the
 * store means every write path (trigger, battle, script) and every loaded save
 * heals itself; content must never list these in sets_flags/reward_flags.
 */
const CROWNS: Array<[WorldFlag, WorldFlag, WorldFlag]> = [
  ['flag:crown_south', 'gleam:ember', 'gleam:tide'],
  ['flag:crown_east', 'gleam:verdant', 'gleam:stone'],
  ['flag:crown_north', 'gleam:storm', 'gleam:frost'],
  ['flag:crown_west', 'gleam:solar', 'gleam:lunar'],
];
const HUB_FLAG: WorldFlag = 'flag:hub_unlocked';

/**
 * Derived "all of a set held" flags: the engine raises the target flag once every
 * member is held, the same self-healing pattern as the crowns. Content must never
 * hand-set the target — it's a function of its members.
 *
 * `flag:q_post_letters_all` follows P1's ten first-dawn letter flags. The journal's
 * N-of-M counter reads progress live off the prefix (see countHeld), but the
 * Waykeeper's "all ten delivered" acknowledgement wants a single gateable flag — a
 * normal `requires_flag` NPC — so we derive it here rather than teach the engine a
 * counting gate. (Order is irrelevant: a player delivers the letters any way they like.)
 */
const POST_LETTER_FLAGS: WorldFlag[] = [
  'flag:q_post_letter_wren',
  'flag:q_post_letter_fenn',
  'flag:q_post_letter_tinderwick',
  'flag:q_post_letter_pearlmoor',
  'flag:q_post_letter_lowleaf',
  'flag:q_post_letter_cinderhead',
  'flag:q_post_letter_galehigh',
  'flag:q_post_letter_pale_vault',
  'flag:q_post_letter_solarium',
  'flag:q_post_letter_nightreach',
];
const POST_LETTERS_ALL: WorldFlag = 'flag:q_post_letters_all';

export class FlagStore {
  private flags: Record<WorldFlag, boolean>;

  constructor(initial: Record<WorldFlag, boolean> = {}) {
    this.flags = { ...initial };
    this.derive();
  }

  get(flag: WorldFlag): boolean {
    return this.flags[flag] === true;
  }

  set(flag: WorldFlag, value = true): void {
    this.flags[flag] = value;
    if (value) this.derive();
  }

  /**
   * Count held flags whose key starts with `prefix` — the save-compatible N-of-M
   * quest counter (no schema change: the booleans we already persist ARE the count).
   * Used by the journal to show a quest's progress (e.g.
   * `countHeld('flag:q_post_letter_')` → "n/10 letters"). Be careful with prefixes
   * that are themselves a substring of another flag — pass the trailing separator
   * (the underscore above) so `flag:q_post_letters` isn't miscounted as a letter.
   */
  countHeld(prefix: string): number {
    let n = 0;
    for (const key in this.flags) {
      if (this.flags[key] === true && key.startsWith(prefix)) n++;
    }
    return n;
  }

  /** Crowns follow Gleam pairs; the hub follows the four crowns; the post-letters
   *  "all" flag follows its ten members. Idempotent — safe to run on every write/load. */
  private derive(): void {
    for (const [crown, a, b] of CROWNS) {
      if (this.flags[a] === true && this.flags[b] === true) this.flags[crown] = true;
    }
    if (CROWNS.every(([crown]) => this.flags[crown] === true)) {
      this.flags[HUB_FLAG] = true;
    }
    if (POST_LETTER_FLAGS.every((f) => this.flags[f] === true)) {
      this.flags[POST_LETTERS_ALL] = true;
    }
  }

  setMany(flags: WorldFlag[] | undefined, value = true): void {
    if (!flags) return;
    for (const f of flags) this.set(f, value);
  }

  /** Convenience for "once" triggers: an implicit per-id flag. */
  triggerFired(id: string): boolean {
    return this.get(`trigger:${id}`);
  }

  markTriggerFired(id: string): void {
    this.set(`trigger:${id}`);
  }

  /** Snapshot for saving (a copy, so callers can't mutate internals). */
  snapshot(): Record<WorldFlag, boolean> {
    return { ...this.flags };
  }
}
