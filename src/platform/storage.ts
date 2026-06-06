/**
 * Persistence abstraction.
 *
 * The game only ever talks to this interface, never to localStorage directly.
 * On the web we back it with localStorage; when we wrap the build in Capacitor
 * for mobile we can swap in @capacitor/preferences behind the same interface
 * without touching a single line of game logic. Keeping every save/load behind
 * one async seam is the main thing that keeps the web -> mobile port cheap.
 */
export interface Storage {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
  remove(key: string): Promise<void>;
}

const PREFIX = 'pixelkin:';

class WebStorage implements Storage {
  async get(key: string): Promise<string | null> {
    try {
      return window.localStorage.getItem(PREFIX + key);
    } catch {
      // Private-mode browsers can throw on access; treat as "no save".
      return null;
    }
  }

  async set(key: string, value: string): Promise<void> {
    try {
      window.localStorage.setItem(PREFIX + key, value);
    } catch {
      /* Quota or private mode — saving silently no-ops for now. */
    }
  }

  async remove(key: string): Promise<void> {
    try {
      window.localStorage.removeItem(PREFIX + key);
    } catch {
      /* ignore */
    }
  }
}

/** The active storage backend. Swap this factory when adding a mobile target. */
export const storage: Storage = new WebStorage();
