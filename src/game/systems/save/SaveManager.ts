/**
 * SaveManager — the single-slot persistence front door for PixelKin.
 *
 * Everything goes through the platform storage seam (`src/platform/storage.ts`),
 * never localStorage directly, so the eventual Capacitor port swaps the backend
 * and not a line of game logic. Two records live here:
 *
 *  - the game save (key `save:slot0`) — one `SaveGame` blob, encoded by SaveCodec.
 *  - settings (key `settings`) — shell chrome choice + a couple of audio prefs.
 *
 * The blob shape and migrations are SaveCodec's job; SaveManager only moves bytes.
 */
import { storage } from '@platform/storage';
import type { SaveGame, KinInstanceData, InventoryData } from './types';
import { SAVE_SCHEMA_VERSION } from './types';
import type { WorldSnapshot } from '@game/data/world/types';
import { SaveCodec } from './SaveCodec';

const SAVE_KEY = 'save:slot0';
const SETTINGS_KEY = 'settings';

/** Which DOM chrome wraps the canvas (see ShellManager). */
export type ShellMode = 'device' | 'overlay' | 'plain';

/** Player-facing preferences, persisted separately from the game save. */
export interface Settings {
  shell: ShellMode;
  controlsVisible: boolean;
  muted?: boolean;
}

/** The defaults a brand-new player gets before they touch the Settings menu. */
export const DEFAULT_SETTINGS: Settings = {
  shell: 'device',
  controlsVisible: true,
  muted: false,
};

export const SaveManager = {
  /** Persist the current game over the single slot. */
  async save(game: SaveGame): Promise<void> {
    await storage.set(SAVE_KEY, SaveCodec.serialize(game));
  },

  /** Load the saved game, or null if there is none / it failed validation. */
  async load(): Promise<SaveGame | null> {
    const raw = await storage.get(SAVE_KEY);
    if (raw === null) return null;
    return SaveCodec.deserialize(raw);
  },

  /** Whether a usable save exists (used to enable Title's "Continue"). */
  async hasSave(): Promise<boolean> {
    return (await this.load()) !== null;
  },

  /** Wipe the save slot (new game / debug). Leaves settings intact. */
  async clear(): Promise<void> {
    await storage.remove(SAVE_KEY);
  },

  /** Load settings, merged over defaults so missing/older fields fill in. */
  async loadSettings(): Promise<Settings> {
    const raw = await storage.get(SETTINGS_KEY);
    if (raw === null) return { ...DEFAULT_SETTINGS };
    try {
      const parsed = JSON.parse(raw) as Partial<Settings>;
      return { ...DEFAULT_SETTINGS, ...parsed };
    } catch {
      return { ...DEFAULT_SETTINGS };
    }
  },

  /** Persist settings (whole object — callers read-modify-write). */
  async saveSettings(settings: Settings): Promise<void> {
    await storage.set(SETTINGS_KEY, JSON.stringify(settings));
  },

  /**
   * Build a fresh SaveGame for a new playthrough. The orchestrator supplies the
   * starting world snapshot, the starter party, and the opening inventory; this
   * just stamps the envelope (schema version, timestamps, zeroed playtime).
   */
  newGame(
    world: WorldSnapshot,
    party: KinInstanceData[],
    inventory: InventoryData,
    money: number,
  ): SaveGame {
    return {
      schema_version: SAVE_SCHEMA_VERSION,
      saved_at: Date.now(),
      play_seconds: 0,
      world,
      party,
      inventory,
      money,
    };
  },
} as const;
