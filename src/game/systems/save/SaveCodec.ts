/**
 * SaveCodec — turns a SaveGame into JSON and back, with version validation and a
 * forward-compatible migration hook, plus the export/import file I/O that lets a
 * player rescue progress past a cleared browser.
 *
 * `serialize`/`deserialize` are the on-disk format SaveManager stores through the
 * platform seam. `exportToFile`/`importFromFile` are deliberate, user-initiated
 * DOM file operations (download blob / hidden file input) — that's the browser's
 * file system, not a localStorage bypass, so it stays inside the storage rules.
 *
 * Migrations: `MIGRATIONS[v]` upgrades a save FROM version v TO v+1. For schema 1
 * it's just identity; future bumps slot a step in here and `deserialize` walks the
 * chain up to `SAVE_SCHEMA_VERSION`.
 */
import type { SaveGame } from './types';
import { SAVE_SCHEMA_VERSION } from './types';

/** A raw, not-yet-validated save shape carrying at least a schema version. */
type RawSave = Partial<SaveGame> & { schema_version?: unknown };

/** Step a save from one schema version to the next. Keyed by the FROM version. */
type Migration = (raw: RawSave) => RawSave;

const MIGRATIONS: Record<number, Migration> = {
  // v1 is the first schema; no upgrades yet. Add `1: (s) => ({...})` etc. here.
};

function isFiniteNumber(v: unknown): v is number {
  return typeof v === 'number' && Number.isFinite(v);
}

/** Minimal structural check that a parsed object is a plausible SaveGame. */
function looksLikeSave(raw: RawSave): raw is SaveGame {
  return (
    isFiniteNumber(raw.schema_version) &&
    isFiniteNumber(raw.saved_at) &&
    isFiniteNumber(raw.play_seconds) &&
    typeof raw.world === 'object' &&
    raw.world !== null &&
    Array.isArray(raw.party) &&
    typeof raw.inventory === 'object' &&
    raw.inventory !== null
  );
}

export const SaveCodec = {
  /** Encode a SaveGame to the stored JSON string. */
  serialize(game: SaveGame): string {
    return JSON.stringify(game);
  },

  /**
   * Parse + validate + migrate stored JSON into a current-version SaveGame, or
   * null if the text is unparseable, the wrong shape, or a future version we
   * can't read.
   */
  deserialize(json: string): SaveGame | null {
    let raw: RawSave;
    try {
      raw = JSON.parse(json) as RawSave;
    } catch {
      return null;
    }
    if (typeof raw !== 'object' || raw === null) return null;

    let version = isFiniteNumber(raw.schema_version) ? raw.schema_version : NaN;
    if (!Number.isFinite(version)) return null;

    // A save newer than this build understands is refused rather than guessed at.
    if (version > SAVE_SCHEMA_VERSION) return null;

    // Walk migrations up to the current version.
    while (version < SAVE_SCHEMA_VERSION) {
      const step = MIGRATIONS[version];
      if (!step) return null; // gap in the chain — refuse rather than corrupt.
      raw = step(raw);
      version += 1;
      raw.schema_version = version;
    }

    return looksLikeSave(raw) ? raw : null;
  },

  /**
   * Trigger a browser download of the save as JSON (cookie-clear safety).
   * Filename like `pixelkin-save-2026-06-07.json`.
   */
  exportToFile(game: SaveGame, filename?: string): void {
    const name = filename ?? `pixelkin-save-${new Date().toISOString().slice(0, 10)}.json`;
    const blob = new Blob([this.serialize(game)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    // Defer revoke so the click's navigation has a chance to start.
    setTimeout(() => URL.revokeObjectURL(url), 0);
  },

  /**
   * Open a hidden file picker, read the chosen JSON, and validate it. Resolves
   * with the SaveGame, or null if the user cancels or the file is invalid.
   */
  importFromFile(): Promise<SaveGame | null> {
    return new Promise((resolve) => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'application/json,.json';
      input.style.display = 'none';

      let settled = false;
      const finish = (result: SaveGame | null): void => {
        if (settled) return;
        settled = true;
        if (input.parentNode) input.parentNode.removeChild(input);
        resolve(result);
      };

      input.addEventListener('change', () => {
        const file = input.files?.[0];
        if (!file) {
          finish(null);
          return;
        }
        const reader = new FileReader();
        reader.onload = () => {
          const text = typeof reader.result === 'string' ? reader.result : '';
          finish(this.deserialize(text));
        };
        reader.onerror = () => finish(null);
        reader.readAsText(file);
      });

      // If the dialog is dismissed, most browsers fire no event — surface the
      // cancel via the window regaining focus with no file chosen.
      window.addEventListener(
        'focus',
        () => {
          // Give the change event a tick to land before assuming cancellation.
          setTimeout(() => {
            if (!settled && !input.files?.length) finish(null);
          }, 300);
        },
        { once: true },
      );

      document.body.appendChild(input);
      input.click();
    });
  },
} as const;
