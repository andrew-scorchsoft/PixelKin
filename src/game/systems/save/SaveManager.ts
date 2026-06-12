/**
 * SaveManager — the multi-slot persistence front door for PixelKin.
 *
 * Everything goes through the platform storage seam (`src/platform/storage.ts`),
 * never localStorage directly, so the eventual Capacitor port swaps the backend
 * and not a line of game logic. The records that live here:
 *
 *  - the game saves (3 slots) — one `SaveGame` blob each, encoded by SaveCodec.
 *  - settings (key `settings`) — shell chrome choice + a couple of audio prefs.
 *
 * Slots, zero-migration: there are three save slots. Slot 0 (slot "1" to the
 * player) keeps the ORIGINAL key `save:slot0` untouched, so every existing save
 * IS slot 1 with no migration (the SaveCodec rename trap is the precedent for
 * never renaming a live key); slots 1 and 2 add `:slot1` / `:slot2` suffixes. An
 * "active slot" (set at the title, defaults to slot 0) decides which key all
 * save/load/clear/export/import operate on, so the in-game SAVE flow and autosave
 * (`persist()`) keep calling `save()`/`load()` unchanged — the public surface
 * WorldScene/SettingsMenu use never changed shape.
 *
 * The blob shape and migrations are SaveCodec's job; SaveManager only moves bytes.
 */
import { storage } from '@platform/storage';
import type { SaveGame, KinInstanceData, InventoryData } from './types';
import { SAVE_SCHEMA_VERSION } from './types';
import type { WorldSnapshot } from '@game/data/world/types';
import { SaveCodec } from './SaveCodec';

/** How many save slots the title offers. */
export const SAVE_SLOT_COUNT = 3;

/**
 * Storage key for a given slot. Slot 0 keeps the original `save:slot0` key for
 * zero-migration of existing saves; later slots append `:slotN`.
 */
function slotKey(slot: number): string {
  return slot === 0 ? 'save:slot0' : `save:slot0:slot${slot}`;
}

/** The active slot index (0-based). All un-suffixed ops target this slot. */
let activeSlot = 0;

const SETTINGS_KEY = 'settings';

/** Which DOM chrome wraps the canvas (see ShellManager). */
export type ShellMode = 'device' | 'overlay' | 'plain';

/** On-screen touch-control scale: 1 = compact, 2 = default, 3 = large. */
export type ControlSize = 1 | 2 | 3;

/** Player-facing preferences, persisted separately from the game save. */
export interface Settings {
  shell: ShellMode;
  controlsVisible: boolean;
  /** Size of the on-screen d-pad / A·B / Start cluster (1 small … 3 large). */
  controlSize?: ControlSize;
  muted?: boolean;
  /** Walk speed: true = always run (no need to hold B). */
  alwaysRun?: boolean;
  /** Dialogue typewriter pace. */
  textSpeed?: 'cosy' | 'brisk' | 'instant';
  /** Battle wait/tween pace: 'cosy' = full, 'swift' = half-length. */
  battlePace?: 'cosy' | 'swift';
  /** Stepped master volume for background music (OFF/LOW/MID/FULL). */
  musicVolume?: 'off' | 'low' | 'mid' | 'full';
  /** Stepped master volume for sound effects (OFF/LOW/MID/FULL). */
  sfxVolume?: 'off' | 'low' | 'mid' | 'full';
}

/** The defaults a brand-new player gets before they touch the Settings menu. */
export const DEFAULT_SETTINGS: Settings = {
  shell: 'device',
  controlsVisible: true,
  controlSize: 2,
  muted: false,
  alwaysRun: false,
  textSpeed: 'cosy',
  battlePace: 'cosy',
  musicVolume: 'full',
  sfxVolume: 'full',
};

export const SaveManager = {
  /** The active slot index (0-based). Slot 0 == the player's "Slot 1". */
  get activeSlot(): number {
    return activeSlot;
  },

  /**
   * Point all subsequent save/load/clear/export/import at a given slot. Set once
   * at the title before entering the world; clamped to a valid slot. Returns the
   * slot actually selected.
   */
  setActiveSlot(slot: number): number {
    activeSlot = Math.max(0, Math.min(SAVE_SLOT_COUNT - 1, Math.trunc(slot)));
    return activeSlot;
  },

  /** Persist the current game over the active slot. */
  async save(game: SaveGame): Promise<void> {
    await storage.set(slotKey(activeSlot), SaveCodec.serialize(game));
  },

  /** Load the active slot's save, or null if there is none / it failed validation. */
  async load(): Promise<SaveGame | null> {
    return this.loadSlot(activeSlot);
  },

  /** Load a specific slot's save, or null. Does not change the active slot. */
  async loadSlot(slot: number): Promise<SaveGame | null> {
    const raw = await storage.get(slotKey(slot));
    if (raw === null) return null;
    return SaveCodec.deserialize(raw);
  },

  /** Whether a usable save exists in the active slot (Title's "Continue"). */
  async hasSave(): Promise<boolean> {
    return (await this.load()) !== null;
  },

  /** Whether a usable save exists in a given slot. */
  async hasSaveInSlot(slot: number): Promise<boolean> {
    return (await this.loadSlot(slot)) !== null;
  },

  /**
   * Decode every slot in order (index 0..N-1), null where empty/invalid. The
   * title's slot picker reads this to render occupancy + per-slot summaries.
   */
  async loadAllSlots(): Promise<(SaveGame | null)[]> {
    const slots: (SaveGame | null)[] = [];
    for (let i = 0; i < SAVE_SLOT_COUNT; i++) slots.push(await this.loadSlot(i));
    return slots;
  },

  /** Wipe the active slot (new game / debug). Leaves settings intact. */
  async clear(): Promise<void> {
    await storage.remove(slotKey(activeSlot));
  },

  /** Wipe a specific slot. Leaves settings intact. */
  async clearSlot(slot: number): Promise<void> {
    await storage.remove(slotKey(slot));
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
      // A fresh register already knows the kin you start with.
      dex: {
        seen: [...new Set(party.map((k) => k.species_id))],
        caught: [...new Set(party.map((k) => k.species_id))],
      },
    };
  },
} as const;
