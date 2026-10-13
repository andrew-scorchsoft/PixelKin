/**
 * What's new: the player-facing changelog, read by the in-game "the world has
 * changed" notice (WorldScene.showVersionNotice) AND rendered as the website's
 * changelog page (web/site.mjs → pixelk.in/changelog). The single source is
 * `data/changelog.json`, newest first: one entry per version ("major.minor", as
 * version.ts), each with a date and a few short notes. A version with nothing to
 * tell simply has no entry. Keep each note short, warm and in-canon (kin, Gleams,
 * the Wayfaring, the vesperlamp): it's read by the fire, not a patch log.
 *
 * The in-game notice stays SHORT however long the log grows: a returning player
 * hears how many updates they missed and only the latest few notes, then gets
 * pointed at the full list on the website (`summariseSince`).
 *
 * NO SPOILERS for the hidden, real-people content (owner's rule, 2026-10): this
 * log is read by the very people those places were built for, in the game and on
 * the website. Never mention Paul or anything of his: the Booji-Wooji Man / S4–S5
 * line, the Chickenpig, the Lifting House (it's Paul's gym), Paul's house on
 * Wayward Rise, the Wayward Arms hotel, the Reckoning Works' walking-man story,
 * nor the beacon-road man with the case. Changes there ship SILENTLY; announce
 * only general things.
 */
import changelog from '@game/data/changelog.json';
import { compareVersions } from '@game/version';

export interface ChangelogEntry {
  version: string;
  /** ISO date the version shipped (optional for the oldest entries). */
  date?: string;
  notes: string[];
}

/** Every entry, newest first. */
export const CHANGELOG: readonly ChangelogEntry[] = [...(changelog.entries as ChangelogEntry[])]
  .sort((a, b) => compareVersions(b.version, a.version));

/** Where the full log lives (the website's changelog page). */
export const CHANGELOG_URL = 'pixelk.in/changelog';

/** How many notes the in-game notice reads before pointing at the website. */
export const NOTICE_NOTES = 3;

/** The entries a returning player missed: every version newer than `from`, up to `current`, newest first. */
export function entriesSince(from: string, current: string): ChangelogEntry[] {
  return CHANGELOG.filter(
    (e) => e.notes.length > 0 && compareVersions(e.version, from) > 0 && compareVersions(e.version, current) <= 0,
  );
}

export interface ChangeSummary {
  /** How many versions with notes the player missed. */
  updates: number;
  /** How many notes those versions carry in all. */
  total: number;
  /** The newest `limit` notes. */
  latest: string[];
  /** True when there are notes beyond `latest` (so point at the full log). */
  more: boolean;
}

/** A compact summary of what a returning player missed: counts + the newest few notes. */
export function summariseSince(from: string, current: string, limit = NOTICE_NOTES): ChangeSummary {
  const entries = entriesSince(from, current);
  const all = entries.flatMap((e) => e.notes);
  return { updates: entries.length, total: all.length, latest: all.slice(0, limit), more: all.length > limit };
}
