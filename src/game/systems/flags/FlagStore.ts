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

export class FlagStore {
  private flags: Record<WorldFlag, boolean>;

  constructor(initial: Record<WorldFlag, boolean> = {}) {
    this.flags = { ...initial };
    this.deriveCrowns();
  }

  get(flag: WorldFlag): boolean {
    return this.flags[flag] === true;
  }

  set(flag: WorldFlag, value = true): void {
    this.flags[flag] = value;
    if (value) this.deriveCrowns();
  }

  /** Crowns follow Gleam pairs; the hub follows the four crowns. Idempotent. */
  private deriveCrowns(): void {
    for (const [crown, a, b] of CROWNS) {
      if (this.flags[a] === true && this.flags[b] === true) this.flags[crown] = true;
    }
    if (CROWNS.every(([crown]) => this.flags[crown] === true)) {
      this.flags[HUB_FLAG] = true;
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
