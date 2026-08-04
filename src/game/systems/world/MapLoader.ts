/**
 * Loads a map and its tilesets into a runtime model the engine can render and query.
 *
 * Source of truth is the map JSON (a `MapDefinition` — layers, warps, triggers,
 * encounters, npcs, gates) plus, per tileset, a packed `*.tileset.json` sidecar
 * (`PackedTileset` — per-tile collision / ability / animation). The atlas image
 * and sidecar are produced by the art tooling; until they exist the renderer falls
 * back to drawn swatches and we use a small built-in behaviour table so the engine
 * is fully testable without art. The map JSON is never hand-fed appearance — only gids.
 */
import { MAP_REGISTRY } from '@game/data/world/maps';
import type { MapDefinition, TilesetRef, EncounterTerrain } from '@game/data/world/types';
import type { PackedTileset, TileMeta } from './tileset';
import { FALLBACK_TILE_META } from './fallbackTilesets';
import { GAME_VERSION } from '@game/version';

export interface ResolvedTileset {
  ref: TilesetRef;
  packed: PackedTileset;
  /** True if the packed sidecar was real (vs synthesised fallback). */
  real: boolean;
}

export interface GidLookup {
  tileset: ResolvedTileset;
  /** 0-based local index within that tileset. */
  local: number;
  meta: TileMeta;
}

export class RuntimeMap {
  constructor(
    readonly def: MapDefinition,
    readonly tilesets: ResolvedTileset[],
  ) {}

  get width(): number {
    return this.def.width;
  }
  get height(): number {
    return this.def.height;
  }

  inBounds(tx: number, ty: number): boolean {
    return tx >= 0 && ty >= 0 && tx < this.width && ty < this.height;
  }

  /** Resolve a global tile id to its tileset + local index + behaviour meta. */
  lookupGid(gid: number): GidLookup | null {
    if (gid <= 0) return null;
    for (const ts of this.tilesets) {
      const start = ts.ref.first_gid;
      const end = start + ts.ref.tile_count;
      if (gid >= start && gid < end) {
        const local = gid - start;
        const meta = ts.packed.tiles.find((t) => t.index === local) ?? { index: local };
        return { tileset: ts, local, meta };
      }
    }
    return null;
  }

  /** Gids stacked at a tile across all non-`above` layers (bottom→top). */
  gidsAt(tx: number, ty: number, includeAbove = false): number[] {
    if (!this.inBounds(tx, ty)) return [];
    const i = ty * this.width + tx;
    const out: number[] = [];
    for (const layer of this.def.layers) {
      if (!includeAbove && layer.role === 'above') continue;
      const gid = layer.data[i] ?? 0;
      if (gid > 0) out.push(gid);
    }
    return out;
  }

  /**
   * True if any tile stacked at (tx,ty) is tagged as this encounter terrain. The
   * tileset sidecar is the authority on terrain (maps carry only gids), so this
   * is how the engine asks "am I standing in water / tall grass?" — used by the
   * EncounterSystem's tile-bound roll and by WorldScene to decide the player is
   * swimming rather than walking.
   */
  hasTerrainAt(tx: number, ty: number, terrain: EncounterTerrain): boolean {
    for (const gid of this.gidsAt(tx, ty)) {
      if (this.lookupGid(gid)?.meta.encounter_terrain === terrain) return true;
    }
    return false;
  }
}

async function fetchJson<T>(path: string): Promise<T | null> {
  try {
    // Paths are relative ('assets/...'); they resolve against the document base,
    // which works under both the dev server and the './'-based static build.
    //
    // Cache-busting (maps + tileset sidecars are FETCHED, not bundled, so Vite's
    // content-hash asset pipeline doesn't version them):
    //  • Production — key the URL to the game version, so cutting a release busts
    //    every player's stale cached map/tileset while staying cacheable within a
    //    version. Bumping GAME_VERSION is the release's cache-bust.
    //  • Dev — revalidate on every fetch, so editing a map/tileset JSON is picked
    //    up the next time the map loads (re-enter the map) without a hard refresh.
    const dev = import.meta.env.DEV;
    const url = dev ? path : `${path}${path.includes('?') ? '&' : '?'}v=${encodeURIComponent(GAME_VERSION)}`;
    const res = await fetch(url, dev ? { cache: 'no-cache' } : undefined);
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

/** Derive the sidecar path from an atlas image path: `..._set.webp` -> `..._set.tileset.json`. */
function sidecarPath(image: string): string {
  return image.replace(/\.(webp|png)$/i, '.tileset.json');
}

async function resolveTileset(ref: TilesetRef): Promise<ResolvedTileset> {
  const packed = await fetchJson<PackedTileset>(sidecarPath(ref.image));
  if (packed) return { ref, packed, real: true };

  // No sidecar yet — synthesise one from the built-in fallback table (dev safety net).
  const fallbackTiles = FALLBACK_TILE_META[ref.name] ?? [];
  const synthesised: PackedTileset = {
    name: ref.name,
    image: ref.image,
    tile_width: ref.tile_width,
    tile_height: ref.tile_height,
    columns: ref.columns,
    tile_count: ref.tile_count,
    tiles: fallbackTiles,
  };
  return { ref, packed: synthesised, real: false };
}

export async function loadMap(mapId: string): Promise<RuntimeMap> {
  const entry = MAP_REGISTRY[mapId];
  if (!entry) throw new Error(`Unknown map id: ${mapId}`);

  const def = await fetchJson<MapDefinition>(entry.json);
  if (!def) throw new Error(`Failed to load map JSON: ${entry.json}`);

  // Cheap integrity guard: each layer's data must cover the whole grid.
  const expected = def.width * def.height;
  for (const layer of def.layers) {
    if (layer.data.length !== expected) {
      throw new Error(
        `Map ${mapId} layer "${layer.name}" has ${layer.data.length} tiles, expected ${expected}.`,
      );
    }
  }

  const tilesets = await Promise.all(def.tilesets.map(resolveTileset));
  return new RuntimeMap(def, tilesets);
}
