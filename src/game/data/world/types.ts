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
  | 'starreach' // step across short voids of pure dark (late game)
  // RESERVED (2026-10): DEEP water's gate. No Gift grants it yet — deep water
  // (the darker open sea, the `deepwater_set` accent family) stays out of reach
  // even with Tidecall, which swims the SHALLOWS. A future deep-swim mechanic
  // is one `reward_abilities: ['deepdive']` away.
  | 'deepdive';

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
  /** Dialogue shown when the warp is gated and the requirement is unmet — a
   *  diegetic "not yet" in a character's voice (mirror of EventTrigger.blocked_ref),
   *  e.g. the netmender's chained breakwater gate. Works on step_on and interact.
   *  A `script.*` ref plays as a cutscene instead (staged on flags — the wood
   *  gap's waiting wanderer). */
  blocked_ref?: string;
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
  /** Trigger removed once the flag is set (mirror of NpcPlacement.hidden_when_flag) —
   *  e.g. the pre-starter gate-warden band that stops fizzing once the Wayfaring begins. */
  hidden_when_flag?: WorldFlag;
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

// 'deep' = open sea, rowed in the Farlamp skiff (the deepwater_set tiles carry it).
export type EncounterTerrain = 'tall_grass' | 'water' | 'cave' | 'sand' | 'deep';

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
  /** Zone only rolls once this flag is held (e.g. a restored site's encounters
   *  blooming after `flag:met_hollowing`). Permanent table swaps ride a pair:
   *  one zone with `hidden_when_flag`, its successor with `requires_flag`. */
  requires_flag?: WorldFlag;
  /** Zone stops rolling once this flag is held (the swap's other half). */
  hidden_when_flag?: WorldFlag;
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
  /** Trainer line-of-sight, in tiles straight ahead along `facing`. When the
   *  player steps into the unobstructed line, the NPC alerts (!), walks up and
   *  runs its `dialogue_ref` script — the classic route-trainer challenge. */
  sight_range?: number;
  /** Sight engagement stops once this flag is set (the trainer is beaten). */
  defeated_flag?: WorldFlag;
  requires_flag?: WorldFlag; // only present once the flag is set
  hidden_when_flag?: WorldFlag; // removed once the flag is set
  /**
   * AMBIENT set-dressing, not a character: an overworld kin (or critter) that
   * idles/wanders near `at`, never collides, never talks, never runs a script,
   * and hops away when the player comes within 2 tiles. Spawned by the
   * Ambience system (systems/world/Ambience.ts), not as an Npc — so it can never
   * block a lane, swallow a Confirm, or be addressed by a cutscene. The map
   * audits (tools/maps/worldmodel.py) ignore ambient placements entirely.
   * `sprite` is normally `kin_<id>_overworld` (pick from the map's own table).
   */
  ambient?: boolean;
  /** Leash for `wander` (and ambient kin): never stray more than this many tiles
   *  (Chebyshev) from `at`. Omitted = unleashed for NPCs, 2 for ambient kin. */
  wander_radius?: number;
  /** Runs IN PLACE facing `facing` (a treadmill): the walk cycle loops but the
   *  NPC never leaves its tile. Pair with `movement: 'static'` so the audits
   *  still read the body as fixed geometry. He turns to face you while you
   *  talk, then picks his stride back up. */
  in_place_walk?: boolean;
}

// ---- Ambience (the "every screen moves" kit, WP0 2026-10) -------------------

/** A code-drawn particle family (no art needed — Ambience.ts draws each as 1–2px shapes). */
export type AmbienceParticleKind =
  | 'snow'
  | 'ash'
  | 'embers'
  | 'glowmotes'
  | 'spores'
  | 'spray'
  | 'motes' // drifting cold motes (Coldfog)
  | 'leaves'
  | 'starglint'
  | 'dust'; // dust motes in still air (the Old Light's window shafts)

/** One particle emitter. Every emitter shares ONE global cap (~40 alive). */
export interface AmbienceParticles {
  kind: AmbienceParticleKind;
  /** 0..1 share of the kind's base count (default 1). */
  density?: number;
  /**
   * Where particles spawn: 'screen' (the visible view — weather), 'water_edge'
   * (water tiles touching dry ground — sea spray) or a tile rect. Default per kind
   * ('spray' → 'water_edge', everything else → 'screen').
   */
  area?: 'screen' | 'water_edge' | { tx: number; ty: number; w: number; h: number };
}

/**
 * Optional per-map ambience block (`MapDefinition.ambience`). Everything here is
 * VISUAL/aural colour — it never touches collision, encounters, triggers or warps,
 * and everything degrades silently (no art required; a missing sfx is silence).
 * The Settings toggle "Ambient motion: Off" stills particles, streaks, birds and
 * bobbing for motion-sensitive players. Author it via tools/maps/add_world_craft.py
 * (per-region modules in tools/maps/worldcraft/) — docs/art-style.md §12b.
 */
export interface MapAmbience {
  particles?: AmbienceParticles[];
  /** A slow translucent drifting strip (fog / cloud shadow). */
  mist?: { color?: string; alpha?: number; speed?: number };
  /** A persistent full-screen colour wash so the region reads at a glance. */
  tint?: { color: string; alpha: number };
  /**
   * The falling-star streak (the game's motif). Default: ON for outdoor maps
   * (town/route/hub/water), OFF for interiors and caves. `false` opts out; an
   * object retunes the interval (seconds; min clamped to 20).
   */
  starfall?: boolean | { min_s?: number; max_s?: number };
  /** Gulls/birds: perched flocks that lift off as you approach + occasional fly-overs. */
  birds?: { kind?: 'gull' | 'bird'; flocks?: TileCoord[]; flyover?: boolean };
  /** Extra light pools beyond the sprite-keyed LIGHT_SOURCES table (a window, a campfire). */
  light_sources_extra?: { at: TileCoord; radius?: number; color?: string }[];
  /**
   * Sweeping light BEAMS (a relit lighthouse): a soft additive wedge from `from`
   * (tile coords; fractions allowed, e.g. tx 4.5 = a tile's left edge + 4.5 tiles)
   * whose far end swings to and fro between `a` and `b`, with a pool where it lands.
   * `period_s` = one full there-and-back (default 9); `width` = the far end's width
   * in tiles (default 3). With Ambient motion off it rests at the midpoint.
   */
  beams?: { from: TileCoord; a: TileCoord; b: TileCoord; period_s?: number; width?: number; color?: string }[];
  /** A quiet looped sfx bed under the music (sfx stem, e.g. 'amb-surf'); silent if missing. */
  sound_bed?: string;
  /** Footprints: 'auto' (sand/trail/snow-tagged terrain, default), 'all' (any open
   *  ground — a snowfield map whose base tiles carry no terrain tag) or 'none'. */
  footprints?: 'auto' | 'all' | 'none';
  /** Global gids lifted off their layer and bobbed 1px (buoys); `MapRenderer`. */
  bob_gids?: number[];
  /** Story-state overrides: the FIRST rule whose flag is held replaces this whole
   *  block (read on map entry) — the Fogwall's mist lifts after `flag:isles_dawn`. */
  when?: { flag: WorldFlag; ambience: MapAmbience }[];
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
   * Exception: a building sprite listed in `walk-behind.json` frees its top roof
   * row(s) so the player can slip along BEHIND the peak (CollisionGrid).
   */
  walk_under?: boolean;
  /**
   * Flag-gated SET DRESSING (the §8 null-lantern pattern for objects): the object
   * only DRAWS once the flag is set (`requires_flag`) / until it is (`hidden_when_flag`).
   * Visibility only — collision is flag-blind (CollisionGrid keeps every footprint),
   * so a swap pair (e.g. the Lowleaf Elder Bed, grey→green) MUST share the same
   * footprint and solidity. Re-evaluated live alongside flag-conditional NPCs.
   */
  requires_flag?: WorldFlag;
  hidden_when_flag?: WorldFlag;
  /**
   * Float on water with a slow 1px bob (boats, buoys, punts). Omitted = decided by
   * the terrain under the object's bottom (waterline) row; true/false overrides.
   */
  bob?: boolean;
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
  /** Optional ambience (particles, mist, tint, starfall, birds, light) — see MapAmbience. */
  ambience?: MapAmbience;
  /** Forced-movement zones: steep chutes, glare ice, ore-cart rails (the traversal kit). */
  flows?: FlowZone[];
  /** Axis-bound walkways: bridges (optionally passable UNDER), ladders, rope planks. */
  spans?: SpanZone[];
  /** Ramps a rider clears in one leap (only while riding a runner). */
  jumps?: JumpPad[];
  /** The map is ridden: holding the rented runner, the player rides at bike speed. */
  ride?: boolean;
}

/**
 * THE TRAVERSAL KIT (2026-10, docs/world/walkthrough/09-the-wild-ways.md §1).
 * Everything is MAP DATA (the shared overworld set is frozen); the art is the
 * `traverse_set` accent tileset. `tools/maps/worldmodel.py` mirrors every rule, so
 * the reach/flow/journey audits see the same world the player walks.
 */
export type TileRect = { tx: number; ty: number; w: number; h: number };

export type FlowKind =
  /** A steep chute: carried `dir` each step, left/right steers, never enterable moving against `dir`. */
  | 'slope'
  /** Glare ice: you keep sliding the way you stepped on until something stops you. */
  | 'ice'
  /** An ore-cart rail: carried `dir`, no steering, never enterable moving against `dir`. */
  | 'rail';

export interface FlowZone {
  id: string;
  kind: FlowKind;
  /** Covered tiles: a rect and/or an explicit list (the union). */
  rect?: TileRect;
  tiles?: TileCoord[];
  /** Carry direction (slope/rail). Ignored for ice. */
  dir?: Facing;
  /** Only active while this flag is held (a lever-switched junction). */
  requires_flag?: WorldFlag;
  /** Inactive once this flag is held (the other half of a switch pair). */
  hidden_when_flag?: WorldFlag;
}

export interface SpanZone {
  id: string;
  kind: 'bridge' | 'ladder' | 'plank';
  rect: TileRect;
  /** The walkable axis: 'h' = east–west deck, 'v' = north–south (ladders are 'v'). */
  axis: 'h' | 'v';
  /** A bridge you can also pass beneath, crossing the axis (the underpass). */
  under?: boolean;
}

export interface JumpPad {
  id: string;
  /** The ramp tile. Riding onto it heading `dir` launches the leap. */
  at: TileCoord;
  dir: Facing;
  /** Tiles travelled from the ramp to the landing (default 3). */
  length?: number;
}

/** A remembered rest point (inn / home / camp fire) — see WorldSnapshot.rest_points. */
export interface RestPoint {
  map: string;
  tx: number;
  ty: number;
  facing: Facing;
  /** Friendly place name (the map's display_name when banked). */
  label: string;
}

/** Persistent world progress, serialised through the platform storage seam (key 'world'). */
export interface WorldSnapshot {
  current_map: string;
  player: { tx: number; ty: number; facing: Facing };
  /**
   * Where a blackout (all kin fainted) wakes you: the last inn / home / camp you
   * rested at. Recorded by the `heal` cutscene op (every rest point heals), so a
   * defeat carries you back to the nearest warm hearth instead of all the way to
   * the start. Optional + falls back to the world start if you've never rested —
   * an additive field, no schema bump (the bond / battles_won precedent).
   */
  respawn?: { map: string; tx: number; ty: number; facing: Facing };
  /**
   * Every rest point the player has EVER rested at (one per map, latest coords,
   * oldest first) — the list SETTINGS → "Return to a rest point" travels to.
   * Banked alongside `respawn` by every resting `heal`; old saves seed it from
   * `respawn`. Additive + optional, no schema bump (the respawn precedent).
   */
  rest_points?: RestPoint[];
  abilities: AbilityId[];
  /** Unlocked warps/areas/honours and fired triggers. */
  flags: Record<WorldFlag, boolean>;
  /** Bumped when the schema changes, for save migrations. */
  schema_version: number;
}
