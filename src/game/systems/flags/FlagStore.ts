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

export class FlagStore {
  private flags: Record<WorldFlag, boolean>;

  constructor(initial: Record<WorldFlag, boolean> = {}) {
    this.flags = { ...initial };
  }

  get(flag: WorldFlag): boolean {
    return this.flags[flag] === true;
  }

  set(flag: WorldFlag, value = true): void {
    this.flags[flag] = value;
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
