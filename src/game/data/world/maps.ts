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
}

export const MAP_REGISTRY: Record<string, MapRegistryEntry> = {
  tinderwick: {
    json: 'assets/maps/tinderwick.json',
    tilesets: { tinderwick_set: 'assets/tilesets/tinderwick_set.webp' },
    kind: 'town',
    music: 'assets/audio/music/tinderwick-a.mp3',
  },
  tinderwick_house: {
    json: 'assets/maps/tinderwick_house.json',
    tilesets: { tinderwick_house_set: 'assets/tilesets/tinderwick_house_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/tinderwick-b.mp3',
  },
  dimglass_coast: {
    json: 'assets/maps/dimglass_coast.json',
    tilesets: { dimglass_coast_set: 'assets/tilesets/dimglass_coast_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/dimglass-coast-a.mp3',
  },
  // Further areas are registered here as their JSON + tilesets are authored.
  // See docs/world/atlas.md for the full area list and their music/graphics briefs.
};
