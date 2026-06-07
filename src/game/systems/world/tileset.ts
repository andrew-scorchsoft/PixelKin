/**
 * The packed tileset format — the contract between art tooling and the engine.
 *
 * `pack_tileset.py` assembles individual 16x16 master tiles into one atlas image
 * (lossless .webp under public/assets/tilesets/) plus a sidecar `<name>.tileset.json`
 * in this shape. The engine never reads tile *appearance* from the map JSON — only
 * gids — and reads every tile *behaviour* (collision, encounter terrain, ability
 * gating, animation) from here. Adding behaviour to a tile is a data edit to the
 * manifest, re-pack, done.
 */
import type { AbilityId, EncounterTerrain } from '@game/data/world/types';

/** A frame-cycling animation. Frame values are LOCAL 0-based tile indices in this set. */
export interface TileAnimation {
  frames: number[];
  duration_ms: number;
}

/**
 * Behaviour for one tile, keyed by its LOCAL 0-based index within the atlas
 * (row-major). The list is sparse — tiles with all-default behaviour are omitted.
 */
export interface TileMeta {
  index: number;
  /** Authoring role, informational: 'ground' | 'path' | 'water' | 'wall' | 'roof' | 'decor' ... */
  role?: string;
  /**
   * Autotile group this tile belongs to (e.g. 'grass', 'water', 'cliff'). Set on
   * the tiles of a 47-blob/9-slice set. Informational at runtime; read by
   * tools/autotile to expand a map's terrain layer. See docs/art-style.md §11.
   */
  terrain?: string;
  /** This tile's role within its terrain's blob set ('fill' | 'edge_n' | 'corner_nw' | 'inner_ne' | ...). */
  autotile?: string;
  /** Solid — the player cannot stand on it (walls, water without tidecall, etc.). */
  collides?: boolean;
  /** Marks this tile as a given encounter terrain (ties to EncounterZone.terrain). */
  encounter_terrain?: EncounterTerrain;
  /** Tile becomes passable only once this Lantern Gift is held. */
  requires_ability?: AbilityId;
  /** Optional frame-cycle (e.g. water ripple). Omitted = static. */
  animation?: TileAnimation;
}

/** The sidecar JSON emitted next to each packed atlas image. */
export interface PackedTileset {
  /** Set name; matches TilesetRef.name and the atlas/sidecar filename stem. */
  name: string;
  /** Served atlas path, e.g. 'assets/tilesets/tinderwick_set.webp'. */
  image: string;
  tile_width: number;
  tile_height: number;
  columns: number;
  tile_count: number;
  /** Sparse per-tile behaviour, keyed by local index. */
  tiles: TileMeta[];
}
