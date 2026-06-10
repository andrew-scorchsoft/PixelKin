/**
 * PixelKin map & world data schema.
 *
 * Maps are authored as our own typed JSON (NOT Tiled) and parsed straight into these
 * interfaces. JSON keys are snake_case, mirrored by a typed TS interface — matching the
 * creature `metadata.json` convention. The full conventions (layers, tile properties,
 * size caps, authoring flow) live in `docs/world/README.md`; a worked example map is at
 * `public/assets/maps/tinderwick.json` and a typed example is in `./examples.ts`.
 *
 * Tiles are 16x16 (see TILE_SIZE in `@game/config`). The viewport is 15x10 tiles.
 */

/** A grid coordinate in TILE units (not pixels). Multiply by TILE_SIZE for world px. */
export interface TileCoord {
  tx: number;
  ty: number;
}

/** Cardinal facing. Matches the human-overworld walk-sheet row order: down/left/right/up. */
export type Facing = 'down' | 'left' | 'right' | 'up';

/**
 * Traversal abilities — PixelKin's "Lantern Gifts", the original equivalents of the
 * genre's overworld field moves. Data-driven: a new gift is a union member + an ability
 * record, no engine change. See `docs/world/story-bible.md` §6.
 */
export type AbilityId =
  | 'glimmerstep' // enter shaded caves/woods too dark to walk
  | 'tidecall' // part moon-tides to cross shallow water
  | 'emberward' // push through the Hollowing's coldfog
  | 'updraft_kite' // ride thermals up terraces / glide gaps
  | 'sunsketch' // bloom shut sun-vines into bridges
  | 'starreach'; // step across short voids of pure dark (late game)

/** A stored world-state flag key, e.g. 'flag:hub_unlocked', 'warp:cave_b1_open'. */
export type WorldFlag = string;

// ---- Tilesets & layers ------------------------------------------------------

export interface TilesetRef {
  /** Tileset name; also the runtime image/texture key. */
  name: string;
  /** Atlas PNG under public/assets/tilesets/, e.g. 'tinderwick_set.png'. */
  image: string;
  /** Tile dimensions in px (16). */
  tile_width: number;
  tile_height: number;
  /** First global tile id this set occupies in a map's gid space. */
  first_gid: number;
  columns: number;
  tile_count: number;
}

export type LayerRole = 'base' | 'deco' | 'above' | 'collision';

export interface MapLayer {
  /** Layer name, e.g. 'base', 'deco', 'deco_2', 'above'. */
  name: string;
  role: LayerRole;
  /** Draw/depth order; higher renders later. 'above' layers sit above the player depth. */
  depth: number;
  /** Row-major tile gids (0 = empty). Length must equal map width * height. */
  data: number[];
}

// ---- Warps / events / encounters / npcs / gates -----------------------------

export type WarpTrigger = 'step_on' | 'interact';
export type WarpTransition = 'fade' | 'door' | 'instant';

export interface Warp {
  id: string; // unique within the map
  at: TileCoord; // tile the player triggers from
  trigger: WarpTrigger; // step onto the tile vs press interact (doors)
  to_map: string; // target MapDefinition.id
  to: TileCoord; // landing tile on the target map
  facing?: Facing; // player facing after the warp
  requires_ability?: AbilityId; // warp inactive until the gift is earned
  requires_flag?: WorldFlag; // warp inactive until the flag is set
  transition?: WarpTransition;
}

export type TriggerKind = 'sign' | 'dialogue' | 'script' | 'cutscene';
export type TriggerActivation = 'step_on' | 'interact';

export interface EventTrigger {
  id: string;
  kind: TriggerKind;
  at: TileCoord;
  activation: TriggerActivation;
  /** Reference into the dialogue/script registry, not inline text. */
  ref: string; // e.g. 'sign.tinderwick_dock', 'script.intro_mentor'
  once?: boolean; // fire at most once (tracked via a flag)
  requires_flag?: WorldFlag;
  /** Dialogue shown when requires_flag is unmet (a diegetic "not yet" beat
   *  instead of the generic hint), e.g. Brisa asking you to catch a kin first. */
  blocked_ref?: string;
  sets_flags?: WorldFlag[]; // flags set when this fires (progression)
}

export interface EncounterTableEntry {
  kin_id: number; // dex id, ties to assets/creatures/NNN_slug
  weight: number; // relative weight within the table
  min_level: number;
  max_level: number;
}

export type EncounterTerrain = 'tall_grass' | 'water' | 'cave' | 'sand';

export interface EncounterZone {
  id: string;
  terrain: EncounterTerrain;
  /** Region in tile units. Multiple zones per map allowed. */
  rect: { tx: number; ty: number; w: number; h: number };
  /** Per-step encounter chance, 0..1 (data-tunable per zone). */
  encounter_rate: number;
  table: EncounterTableEntry[];
  /** Some terrains only become enterable with a gift (e.g. water -> tidecall). */
  requires_ability?: AbilityId;
}

export type NpcMovement = 'static' | 'wander' | 'patrol' | 'look_around';

export interface NpcPlacement {
  id: string;
  at: TileCoord;
  facing: Facing;
  /** Walk-sheet texture key (human-overworld 3x4 sprite sheet). */
  sprite: string; // e.g. 'npc_mentor'
  movement: NpcMovement;
  patrol?: TileCoord[]; // waypoints for 'patrol'
  dialogue_ref?: string;
  requires_flag?: WorldFlag; // only present once the flag is set
  hidden_when_flag?: WorldFlag; // removed once the flag is set
}

export type AbilityGateEffect = 'make_passable' | 'remove_tile' | 'set_flag';

/**
 * A set of tiles only passable once a gift is earned.
 * - 'make_passable': tiles stop colliding while the ability is held.
 * - 'remove_tile': clear the tiles permanently (sets `sets_flag` so it stays cleared).
 * - 'set_flag': use the gift here to set a progression flag (e.g. light a beacon).
 */
export interface AbilityGate {
  id: string;
  ability: AbilityId;
  /** The gated region in tile units (preferred — matches warps/zones). */
  rect?: { tx: number; ty: number; w: number; h: number };
  /** Explicit tile list — legacy alternative to `rect`. One of the two is required. */
  tiles?: TileCoord[];
  effect: AbilityGateEffect;
  sets_flag?: WorldFlag;
}

export type MapKind = 'town' | 'route' | 'interior' | 'water' | 'cave' | 'hub';

/**
 * A whole multi-tile STRUCTURE placed as a single transparent sprite (a building,
 * big tree, lamp-post, sign) — not tiled (docs/art-style.md §14b). Drawn over the
 * ground; the top `overhang` rows render ABOVE the player (walk-behind eaves /
 * canopies), the rest below. Footprint cells collide unless `solid` is false.
 */
export interface MapObject {
  id: string;
  /** Object sprite texture key (packed by pack_objects.py, loaded in PreloadScene). */
  sprite: string;
  /** Top-left tile of the object's footprint. */
  at: TileCoord;
  /** Footprint size in tiles. */
  w: number;
  h: number;
  /** Top N rows that render over the player (overhanging roof/eave/canopy). Default 0. */
  overhang?: number;
  /** Whether the footprint blocks movement. Default true. */
  solid?: boolean;
  /**
   * If true, the `overhang` rows are PASSABLE (the player walks under them — tree
   * canopies, a lamp's arm). If false (default), the whole footprint is solid even
   * though the overhang rows still render over the player — buildings, where the
   * roof must draw above a player standing north of it but you can't walk into it.
   */
  walk_under?: boolean;
}

export interface MapDefinition {
  id: string; // 'tinderwick', matches the JSON filename stem
  display_name: string;
  /** Dimensions in tiles (soft caps: 64x64 overworld, ~32x32 interior; absolute 128x128). */
  width: number;
  height: number;
  tile_width: number; // 16
  tile_height: number; // 16
  /** Category — drives music defaults, encounter defaults, indoor lighting. */
  kind: MapKind;
  tilesets: TilesetRef[];
  layers: MapLayer[];
  /** Whole multi-tile structures placed as sprites (buildings, big trees, lamps). */
  objects?: MapObject[];
  warps: Warp[];
  triggers: EventTrigger[];
  encounters: EncounterZone[];
  npcs: NpcPlacement[];
  gates: AbilityGate[];
  /** Music key (mp3 in public/assets/audio/music/), keyed to the area's midi brief. */
  music?: string;
}

/** Persistent world progress, serialised through the platform storage seam (key 'world'). */
export interface WorldSnapshot {
  current_map: string;
  player: { tx: number; ty: number; facing: Facing };
  abilities: AbilityId[];
  /** Unlocked warps/areas/honours and fired triggers. */
  flags: Record<WorldFlag, boolean>;
  /** Bumped when the schema changes, for save migrations. */
  schema_version: number;
}
