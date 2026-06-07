/**
 * Save data shapes — the persisted envelope around the canonical WorldSnapshot.
 *
 * `WorldSnapshot` (in data/world/types.ts) stays the single source of truth for
 * world position / abilities / flags; this wraps it with the player's party and
 * inventory into one serialisable `SaveGame`. Everything is written through the
 * platform storage seam only (src/platform/storage.ts), and can be exported /
 * imported as JSON so progress survives a cleared browser.
 */
import type { WorldSnapshot } from '@game/data/world/types';

/** The current schema version — bump and add a migration in SaveCodec when shapes change. */
export const SAVE_SCHEMA_VERSION = 1;

export type KinStatus = 'none' | 'sleep' | 'burn' | 'freeze' | 'paralysis' | 'poison';

/** A single owned kin, serialised. Resolves its species via SPECIES_BY_ID (dex.ts). */
export interface KinInstanceData {
  species_id: number;
  nickname?: string;
  level: number;
  exp: number;
  /** Current hp (max is derived from species stats + level at runtime). */
  hp: number;
  /** Up to 4 known moves, with remaining charges (move ids resolve via MOVE_BY_ID). */
  moves: { id: string; charges: number }[];
  status?: KinStatus;
  caught_at?: { map: string; tx: number; ty: number };
}

/** Item id -> count. Item definitions live in content/items.ts. */
export interface InventoryData {
  items: Record<string, number>;
}

/** The full save blob persisted under storage key 'save:slot0'. */
export interface SaveGame {
  schema_version: number;
  saved_at: number; // epoch ms
  play_seconds: number;
  world: WorldSnapshot;
  party: KinInstanceData[]; // first entry is the battle lead
  box?: KinInstanceData[]; // overflow storage (later)
  inventory: InventoryData;
}
