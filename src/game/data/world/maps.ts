/**
 * Map registry: maps each area id to the runtime assets the loader/preloader need
 * (the map JSON, its tileset atlases, and its music loop). Adding an area is a data edit
 * here plus a node in `./graph.ts` — see `docs/world/README.md` for the full flow.
 *
 * Asset paths are relative (vite `base: './'` for the Capacitor port), served from
 * `public/assets/`.
 */
import type { MapKind } from './types';

export interface MapRegistryEntry {
  /** Path to the map JSON under public/assets/maps/. */
  json: string;
  /** Tileset image keys -> atlas PNG paths under public/assets/tilesets/. */
  tilesets: Record<string, string>;
  kind: MapKind;
  /** mp3 loop under public/assets/audio/music/ (optional). */
  music?: string;
  /**
   * Battle-backdrop variants (240x160 WebP under public/assets/backgrounds/battle/).
   * One is picked at random when a battle starts on this map, so fights here have a
   * sense of place instead of flat black, and don't all look identical. Omit to fall
   * back to the plain night fill. See docs/art-style.md ("Battle backdrops").
   */
  battle_backdrops?: string[];
}

export const MAP_REGISTRY: Record<string, MapRegistryEntry> = {
  tinderwick: {
    json: 'assets/maps/tinderwick.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'town',
    music: 'assets/audio/music/tinderwick-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/tinderwick-a.webp',
      'assets/backgrounds/battle/tinderwick-b.webp',
    ],
  },
  tinderwick_house: {
    json: 'assets/maps/tinderwick_house.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/tinderwick-b.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/tinderwick-house-a.webp',
      'assets/backgrounds/battle/tinderwick-house-b.webp',
    ],
  },
  tinderwick_shop: {
    json: 'assets/maps/tinderwick_shop.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/tinderwick-b.mp3',
  },
  tinderwick_lumenary: {
    json: 'assets/maps/tinderwick_lumenary.json',
    tilesets: { interior_stone_set: 'assets/tilesets/interior_stone_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/tinderwick-a.mp3',
  },
  dimglass_coast: {
    json: 'assets/maps/dimglass_coast.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/dimglass-coast-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/dimglass-coast-a.webp',
      'assets/backgrounds/battle/dimglass-coast-b.webp',
    ],
  },
  dimglass_coast_ii: {
    json: 'assets/maps/dimglass_coast_ii.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/dimglass-coast-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/dimglass-coast-a.webp',
      'assets/backgrounds/battle/dimglass-coast-b.webp',
    ],
  },
  pearlmoor_quay: {
    json: 'assets/maps/pearlmoor_quay.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'town',
    music: 'assets/audio/music/dimglass-coast-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/pearlmoor-quay-a.webp',
      'assets/backgrounds/battle/pearlmoor-quay-b.webp',
    ],
  },
  pearlmoor_lumenary: {
    json: 'assets/maps/pearlmoor_lumenary.json',
    tilesets: { interior_stone_set: 'assets/tilesets/interior_stone_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/dimglass-coast-a.mp3',
  },
  pearlmoor_shop: {
    json: 'assets/maps/pearlmoor_shop.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/dimglass-coast-a.mp3',
  },
  pearlmoor_inn: {
    json: 'assets/maps/pearlmoor_inn.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/dimglass-coast-a.mp3',
  },
  gullcry_rock: {
    json: 'assets/maps/gullcry_rock.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/dimglass-coast-a.mp3',
    // open-sea spur: the harbour backdrops carry the same moon-on-water read
    battle_backdrops: [
      'assets/backgrounds/battle/pearlmoor-quay-a.webp',
      'assets/backgrounds/battle/pearlmoor-quay-b.webp',
    ],
  },
  vesper_crossroads: {
    json: 'assets/maps/vesper_crossroads.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'hub',
    music: 'assets/audio/music/tinderwick-a.mp3',
  },
  // Further areas are registered here as their JSON + tilesets are authored.
  // See docs/world/atlas.md for the full area list and their music/graphics briefs.
};

/** Every distinct battle-backdrop image across the registry (for preloading). */
export function allBattleBackdrops(): string[] {
  const seen = new Set<string>();
  for (const entry of Object.values(MAP_REGISTRY)) {
    for (const path of entry.battle_backdrops ?? []) seen.add(path);
  }
  return [...seen];
}

/**
 * Pick a battle backdrop for a map (random variant), or null if the map has none
 * — in which case the battle keeps its plain night fill.
 */
export function resolveBattleBackdrop(mapId: string | undefined): string | null {
  const variants = (mapId && MAP_REGISTRY[mapId]?.battle_backdrops) || [];
  if (variants.length === 0) return null;
  return variants[Math.floor(Math.random() * variants.length)];
}
