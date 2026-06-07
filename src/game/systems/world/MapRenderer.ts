/**
 * Renders a RuntimeMap as Phaser tilemap layers built from our gid arrays.
 *
 * We do NOT use Tiled. Each `MapLayer`'s row-major gids are written into a blank
 * Phaser layer; each `TilesetRef` is registered at its `first_gid` so gids resolve
 * to the right atlas. Layer depths come from the data (base 0, deco ~5, above ~20),
 * and the player is given a depth between deco and above by WorldScene.
 *
 * Texture sourcing is tolerant: if a real atlas .webp is present it's loaded; if not
 * (art not generated yet) a coloured swatch atlas is generated at runtime so the
 * whole engine stays testable. Either way the gids/behaviour are identical.
 */
import Phaser from 'phaser';
import { TILE_SIZE, COLORS } from '@game/config';
import type { RuntimeMap, ResolvedTileset } from './MapLoader';
import type { TileMeta } from './tileset';

/** A placed tile that cycles through frames (water ripple, lamp flicker, glowmoss). */
export interface AnimatedTilePlacement {
  tile: Phaser.Tilemaps.Tile;
  /** Global gids to cycle through, in order. */
  frames: number[];
  /** Milliseconds each frame is shown. */
  frameMs: number;
}

export interface MapRenderResult {
  tilemap: Phaser.Tilemaps.Tilemap;
  layers: Phaser.Tilemaps.TilemapLayer[];
  /** Layers whose role is 'above' — drawn over the player. */
  aboveLayers: Phaser.Tilemaps.TilemapLayer[];
  /** Placed tiles that cycle frames; driven by `tickAnimatedTiles` each frame. */
  animatedTiles: AnimatedTilePlacement[];
  pixelWidth: number;
  pixelHeight: number;
}

/**
 * Advance animated tiles to the frame for `timeMs` (call once per frame from the
 * owning scene's update). Frames are derived from each tile's
 * `animation.frames`/`duration_ms` in the tileset sidecar; the cycle is purely a
 * function of wall-clock time, so all tiles of a kind ripple in sync.
 */
export function tickAnimatedTiles(animated: AnimatedTilePlacement[], timeMs: number): void {
  for (const a of animated) {
    const idx = Math.floor(timeMs / a.frameMs) % a.frames.length;
    const gid = a.frames[idx];
    if (a.tile.index !== gid) a.tile.index = gid;
  }
}

const ROLE_COLORS: Record<string, string> = {
  ground: COLORS.grass,
  grass: COLORS.grass,
  grass_dark: '#4a9a55',
  path: '#b9763f',
  soil: '#6b4a3a',
  sand: '#e8d8a8',
  floor: '#caa978',
  water: COLORS.water,
  wall: '#6c6f86',
  cliff: '#6c6f86',
  cliff_edge: '#3b3e55',
  roof: COLORS.fire,
  door: '#3f2a22',
  sign: '#b9763f',
  fence: '#8a5a34',
  decor: COLORS.diamond,
  lamp: COLORS.fire,
  above: '#2f6b3a',
};

function roleColor(meta: TileMeta): string {
  if (meta.role && ROLE_COLORS[meta.role]) return ROLE_COLORS[meta.role];
  return COLORS.deepBlue;
}

/** Make a swatch atlas texture for a tileset that has no real image yet. */
function generatePlaceholderAtlas(scene: Phaser.Scene, ts: ResolvedTileset): void {
  const key = ts.ref.name;
  if (scene.textures.exists(key)) return;

  const cols = ts.ref.columns;
  const rows = Math.max(1, Math.ceil(ts.ref.tile_count / cols));
  const tw = ts.ref.tile_width;
  const th = ts.ref.tile_height;

  const canvas = scene.textures.createCanvas(key, cols * tw, rows * th);
  const ctx = canvas?.getContext();
  if (!ctx || !canvas) return;

  for (let local = 0; local < ts.ref.tile_count; local++) {
    const cx = (local % cols) * tw;
    const cy = Math.floor(local / cols) * th;
    const meta = ts.packed.tiles.find((t) => t.index === local) ?? { index: local };
    ctx.fillStyle = roleColor(meta);
    ctx.fillRect(cx, cy, tw, th);
    // subtle inner border so the tile grid reads while debugging
    ctx.strokeStyle = 'rgba(0,0,0,0.25)';
    ctx.lineWidth = 1;
    ctx.strokeRect(cx + 0.5, cy + 0.5, tw - 1, th - 1);
  }
  canvas.refresh();
}

/** Load the real atlas image if present; resolve true on success, false on error. */
function tryLoadAtlas(scene: Phaser.Scene, ts: ResolvedTileset): Promise<boolean> {
  return new Promise((resolve) => {
    if (scene.textures.exists(ts.ref.name)) {
      resolve(true);
      return;
    }
    const key = ts.ref.name;
    const onFile = (fileKey: string): void => {
      if (fileKey === key) {
        cleanup();
        resolve(true);
      }
    };
    const onError = (file: Phaser.Loader.File): void => {
      if (file.key === key) {
        cleanup();
        resolve(false);
      }
    };
    const cleanup = (): void => {
      scene.load.off(Phaser.Loader.Events.FILE_COMPLETE, onFile);
      scene.load.off(Phaser.Loader.Events.FILE_LOAD_ERROR, onError);
    };
    scene.load.on(Phaser.Loader.Events.FILE_COMPLETE, onFile);
    scene.load.on(Phaser.Loader.Events.FILE_LOAD_ERROR, onError);
    scene.load.image(key, ts.ref.image);
    scene.load.start();
  });
}

export async function renderMap(scene: Phaser.Scene, map: RuntimeMap): Promise<MapRenderResult> {
  // Ensure every tileset has a texture (real atlas, else generated swatches).
  for (const ts of map.tilesets) {
    const loaded = ts.real ? await tryLoadAtlas(scene, ts) : false;
    if (!loaded) generatePlaceholderAtlas(scene, ts);
  }

  const tilemap = scene.make.tilemap({
    tileWidth: TILE_SIZE,
    tileHeight: TILE_SIZE,
    width: map.width,
    height: map.height,
  });

  const tilesetObjs = map.tilesets.map((ts) =>
    tilemap.addTilesetImage(
      ts.ref.name,
      ts.ref.name,
      ts.ref.tile_width,
      ts.ref.tile_height,
      0,
      0,
      ts.ref.first_gid,
    ),
  ).filter((t): t is Phaser.Tilemaps.Tileset => t !== null);

  const layers: Phaser.Tilemaps.TilemapLayer[] = [];
  const aboveLayers: Phaser.Tilemaps.TilemapLayer[] = [];
  const animatedTiles: AnimatedTilePlacement[] = [];

  for (const layerDef of map.def.layers) {
    if (layerDef.role === 'collision') continue; // logical only, never drawn
    const layer = tilemap.createBlankLayer(layerDef.name, tilesetObjs, 0, 0);
    if (!layer) continue;
    layer.setDepth(layerDef.depth);
    for (let ty = 0; ty < map.height; ty++) {
      for (let tx = 0; tx < map.width; tx++) {
        const gid = layerDef.data[ty * map.width + tx] ?? 0;
        if (gid <= 0) continue;
        const tile = layer.putTileAt(gid, tx, ty);
        // Register any frame-cycling tile (water ripple, lamp flicker, …). Frame
        // indices in the sidecar are local; convert to global gids here.
        const look = map.lookupGid(gid);
        const anim = look?.meta.animation;
        if (tile && look && anim && anim.frames.length > 1 && anim.duration_ms > 0) {
          animatedTiles.push({
            tile,
            frames: anim.frames.map((f) => look.tileset.ref.first_gid + f),
            frameMs: anim.duration_ms / anim.frames.length,
          });
        }
      }
    }
    layers.push(layer);
    if (layerDef.role === 'above') aboveLayers.push(layer);
  }

  const pixelWidth = map.width * TILE_SIZE;
  const pixelHeight = map.height * TILE_SIZE;
  return { tilemap, layers, aboveLayers, animatedTiles, pixelWidth, pixelHeight };
}
