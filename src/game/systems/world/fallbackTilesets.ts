/**
 * Built-in fallback tile behaviour — a DEV SAFETY NET only.
 *
 * Real tilesets ship a packed `*.tileset.json` sidecar (produced by the art
 * tooling) that defines each tile's collision / ability / animation. Until that
 * sidecar exists for a set, MapLoader synthesises a PackedTileset from this table
 * so the engine (collision, gating, walking) is fully testable against placeholder
 * swatch art. When the real sidecar lands it takes precedence and these entries are
 * ignored. Keyed by tileset name; values are sparse (only non-default tiles).
 *
 * Indices follow `public/assets/maps/tinderwick.json`'s gid usage (gid - first_gid):
 * 0 grass · 1 sea/water · 2 path · 3 floor · 4 flowers · 5 sign · 6 tree-top(above)
 * · 8 lamp · 9 door.
 */
import type { TileMeta } from './tileset';

export const FALLBACK_TILE_META: Record<string, TileMeta[]> = {
  tinderwick_set: [
    { index: 0, role: 'ground' },
    { index: 1, role: 'water', collides: true, encounter_terrain: 'water', requires_ability: 'tidecall' },
    { index: 2, role: 'path' },
    { index: 3, role: 'floor' },
    { index: 4, role: 'decor' },
    { index: 5, role: 'sign', collides: true },
    { index: 6, role: 'above' },
    { index: 8, role: 'lamp', collides: true },
    { index: 9, role: 'door' },
  ],
};
