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
  // v1 → v2: the wick economy lands. Pre-economy saves get the new-game purse
  // (they never had a chance to earn, so zero would feel like a fine).
  1: (raw) => ({ ...raw, money: 250 }),

  // v2 → v3: canon status names, lamp charges, and the register (dex progress).
  //  - KinStatus placeholders → the canon seven (docs/mechanics/03-moves.md).
  //  - Lamp items become charges for the one vesperlamp (the device itself is a
  //    key item now): bright_lamp → glow_charge, radiant_lamp → beacon_charge,
  //    spare vesperlamps → glow_charges (one stays as the device).
  //  - `dex` seeded from owned kin (you have certainly seen what walks with you).
  2: (raw) => {
    const statusMap: Record<string, string> = {
      sleep: 'doze',
      burn: 'scorch',
      freeze: 'chill',
      paralysis: 'numb',
      poison: 'blight',
    };
    const fixKin = <T extends { status?: string }>(k: T): T => {
      if (k.status && statusMap[k.status]) return { ...k, status: statusMap[k.status] as T['status'] };
      return k;
    };
    const party = Array.isArray(raw.party) ? raw.party.map(fixKin) : raw.party;
    const box = Array.isArray(raw.box) ? raw.box.map(fixKin) : raw.box;

    const items: Record<string, number> = { ...(raw.inventory?.items ?? {}) };
    const renames: Record<string, string> = { bright_lamp: 'glow_charge', radiant_lamp: 'beacon_charge' };
    for (const [from, to] of Object.entries(renames)) {
      if (items[from]) {
        items[to] = (items[to] ?? 0) + items[from];
        delete items[from];
      }
    }
    if ((items['vesperlamp'] ?? 0) > 1) {
      items['glow_charge'] = (items['glow_charge'] ?? 0) + items['vesperlamp'] - 1;
      items['vesperlamp'] = 1;
    }

    const owned = [...(party ?? []), ...(box ?? [])]
      .map((k) => (k as { species_id?: number }).species_id)
      .filter((id): id is number => typeof id === 'number');
    const dedupe = [...new Set(owned)];

    return {
      ...raw,
      party,
      box,
      inventory: { items },
      dex: { seen: dedupe, caught: dedupe },
    };
  },
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
    raw.inventory !== null &&
    isFiniteNumber(raw.money) &&
    typeof raw.dex === 'object' &&
    raw.dex !== null
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
