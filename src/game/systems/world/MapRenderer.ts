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
import { getAmbientMotion } from '@game/ui/preferences';

/** A placed tile that cycles through frames (water ripple, lamp flicker, glowmoss). */
export interface AnimatedTilePlacement {
  tile: Phaser.Tilemaps.Tile;
  /** Global gids to cycle through, in order. */
  frames: number[];
  /** Milliseconds each frame is shown. */
  frameMs: number;
  /** Per-tile clock offset (ms) so a sea glitters instead of blinking in lockstep. */
  phase: number;
}

export interface MapRenderResult {
  tilemap: Phaser.Tilemaps.Tilemap;
  layers: Phaser.Tilemaps.TilemapLayer[];
  /** Layers whose role is 'above' — drawn over the player. */
  aboveLayers: Phaser.Tilemaps.TilemapLayer[];
  /** Placed tiles that cycle frames; driven by `tickAnimatedTiles` each frame. */
  animatedTiles: AnimatedTilePlacement[];
  /** Whole-structure object sprites (buildings, trees, lamps) — destroy on teardown. */
  objects: Phaser.GameObjects.Image[];
  /** Tiles lifted off their layer to bob (MapAmbience.bob_gids) — destroy on teardown. */
  bobbers: Phaser.GameObjects.Image[];
  pixelWidth: number;
  pixelHeight: number;
}

/** Depths for object halves: body just below the player (~10), overhang above the `above` layer (20). */
const OBJECT_BODY_DEPTH = 9;
const OBJECT_OVERHANG_DEPTH = 21;

/**
 * Objects that float: a slow 1px sine bob on their sprites (boats, buoys). Keyed by
 * sprite-name pattern so every harbour gets it with no map edit. Visual only — the
 * footprint (collision) never moves. Stilled by Settings → Ambient motion: Off.
 */
const OBJECT_BOB: { match: RegExp; px: number; ms: number }[] = [
  { match: /(^|_)boat(_|$)/, px: 1, ms: 1700 },
  { match: /(^|_)buoy(_|$)/, px: 1, ms: 1300 },
];

/** Start the 1px bob on a sprite (random start so a harbour never moves in unison). */
function addBob(scene: Phaser.Scene, img: Phaser.GameObjects.Image, px: number, ms: number): void {
  scene.tweens.add({
    targets: img,
    y: img.y - px,
    duration: ms,
    yoyo: true,
    repeat: -1,
    ease: 'Sine.inOut',
    delay: Math.floor(Math.random() * ms),
  });
}

/**
 * Make sure the tileset texture behind `gid` has a named 16×16 frame for it (a
 * packed atlas is loaded as ONE image, so per-tile frames are added on demand).
 * Returns the texture key + frame name, or null for an unresolvable gid. Used by
 * the bob lift below and by Ambience (the tall-grass legs overlay re-draws the
 * real grass tile over an actor's legs, so it needs no art of its own).
 */
export function ensureTileFrame(
  scene: Phaser.Scene,
  map: RuntimeMap,
  gid: number,
): { key: string; frame: string } | null {
  const look = map.lookupGid(gid);
  if (!look) return null;
  const ref = look.tileset.ref;
  const key = ref.name;
  if (!scene.textures.exists(key)) return null;
  const local = gid - ref.first_gid;
  const frame = `t${local}`;
  const tex = scene.textures.get(key);
  if (!tex.has(frame)) {
    const cx = (local % ref.columns) * ref.tile_width;
    const cy = Math.floor(local / ref.columns) * ref.tile_height;
    tex.add(frame, 0, cx, cy, ref.tile_width, ref.tile_height);
  }
  return { key, frame };
}

/**
 * Place each whole-structure object (art-style §14b) as one transparent sprite,
 * split so the top `overhang` rows render over the player (walk-behind eaves /
 * canopies) and the rest below. Footprint collision is handled by CollisionGrid.
 */
function renderObjects(scene: Phaser.Scene, map: RuntimeMap): Phaser.GameObjects.Image[] {
  const out: Phaser.GameObjects.Image[] = [];
  for (const obj of map.def.objects ?? []) {
    if (!scene.textures.exists(obj.sprite)) continue; // art not packed yet — collision still applies
    const px = obj.at.tx * TILE_SIZE;
    const py = obj.at.ty * TILE_SIZE;
    const wpx = obj.w * TILE_SIZE;
    const hpx = obj.h * TILE_SIZE;
    const overhangPx = (obj.overhang ?? 0) * TILE_SIZE;

    const body = scene.add.image(px, py, obj.sprite).setOrigin(0, 0).setDepth(OBJECT_BODY_DEPTH);
    if (overhangPx > 0) body.setCrop(0, overhangPx, wpx, hpx - overhangPx);
    // Carry the placement def so the owning scene can re-evaluate flag-gated
    // objects (MapObject.requires_flag / hidden_when_flag) when flags change.
    body.setData('object_def', obj);
    out.push(body);
    const bob = getAmbientMotion() ? OBJECT_BOB.find((b) => b.match.test(obj.sprite)) : undefined;

    if (overhangPx > 0) {
      const over = scene.add.image(px, py, obj.sprite).setOrigin(0, 0).setDepth(OBJECT_OVERHANG_DEPTH);
      over.setCrop(0, 0, wpx, overhangPx);
      over.setData('object_def', obj);
      out.push(over);
      if (bob) addBob(scene, over, bob.px, bob.ms);
    }
    if (bob) addBob(scene, body, bob.px, bob.ms);
  }
  return out;
}

/**
 * Advance animated tiles to the frame for `timeMs` (call once per frame from the
 * owning scene's update). Frames are derived from each tile's
 * `animation.frames`/`duration_ms` in the tileset sidecar; the cycle is a function
 * of wall-clock time plus each tile's `phase` (hashed from its x,y), so a sea
 * glitters out of lockstep instead of blinking all at once.
 */
export function tickAnimatedTiles(animated: AnimatedTilePlacement[], timeMs: number): void {
  for (const a of animated) {
    const idx = Math.floor((timeMs + a.phase) / a.frameMs) % a.frames.length;
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
          const frameMs = anim.duration_ms / anim.frames.length;
          animatedTiles.push({
            tile,
            frames: anim.frames.map((f) => look.tileset.ref.first_gid + f),
            frameMs,
            // A cheap spatial hash → a whole-frame-ish offset per tile, so the
            // ripple travels across the water rather than strobing in unison.
            phase: Math.floor((((tx * 7 + ty * 13) % 11) / 11) * anim.duration_ms),
          });
        }
      }
    }
    layers.push(layer);
    if (layerDef.role === 'above') aboveLayers.push(layer);
  }

  const objects = renderObjects(scene, map);
  const bobbers = liftBobTiles(scene, map, layers);

  const pixelWidth = map.width * TILE_SIZE;
  const pixelHeight = map.height * TILE_SIZE;
  return { tilemap, layers, aboveLayers, animatedTiles, objects, bobbers, pixelWidth, pixelHeight };
}

/**
 * MapAmbience.bob_gids: lift each matching (non-animated) tile off its layer into
 * an Image at the same spot and depth, then bob it 1px — buoys riding the swell.
 * The tile's collision/terrain is untouched (the engine reads those from the map
 * data, never the drawn layer). No-op with ambient motion off or no texture.
 */
function liftBobTiles(
  scene: Phaser.Scene,
  map: RuntimeMap,
  layers: Phaser.Tilemaps.TilemapLayer[],
): Phaser.GameObjects.Image[] {
  const out: Phaser.GameObjects.Image[] = [];
  const gids = new Set(map.def.ambience?.bob_gids ?? []);
  if (gids.size === 0 || !getAmbientMotion()) return out;
  for (const layer of layers) {
    layer.forEachTile((tile) => {
      if (!gids.has(tile.index)) return;
      const tf = ensureTileFrame(scene, map, tile.index);
      if (!tf) return;
      const img = scene.add
        .image(tile.pixelX, tile.pixelY, tf.key, tf.frame)
        .setOrigin(0, 0)
        .setDepth(layer.depth + 0.01);
      layer.removeTileAt(tile.x, tile.y);
      addBob(scene, img, 1, 1100 + Math.floor(Math.random() * 500));
      out.push(img);
    });
  }
  return out;
}
