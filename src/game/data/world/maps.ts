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
    // Lampwarden 1 (Ember) Gleam battle happens here — shrine-interior backdrop.
    battle_backdrops: [
      'assets/backgrounds/battle/tinderwick-lumenary-a.webp',
      'assets/backgrounds/battle/tinderwick-lumenary-b.webp',
    ],
  },
  // The old beacon — the earned first Gleam: wick-key gated ascent, wick-tender
  // sight trainers on the stairs, Brisa's bond-test in the lantern room.
  tinderwick_beacon_i: {
    json: 'assets/maps/tinderwick_beacon_i.json',
    tilesets: { interior_stone_set: 'assets/tilesets/interior_stone_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/tinderwick-a.mp3',
  },
  tinderwick_beacon_ii: {
    json: 'assets/maps/tinderwick_beacon_ii.json',
    tilesets: { interior_stone_set: 'assets/tilesets/interior_stone_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/tinderwick-a.mp3',
  },
  tinderwick_beacon_top: {
    json: 'assets/maps/tinderwick_beacon_top.json',
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
  // The Causeway Bell's walk: the foot causeway out to the Moor-bell shrine
  // (gated on the netmender's rope; reuses Pearlmoor's music + backdrops).
  pearlmoor_breakwater: {
    json: 'assets/maps/pearlmoor_breakwater.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
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
    // Lampwarden 2 (Tide) Gleam battle happens here — shrine-interior backdrop.
    battle_backdrops: [
      'assets/backgrounds/battle/pearlmoor-lumenary-a.webp',
      'assets/backgrounds/battle/pearlmoor-lumenary-b.webp',
    ],
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
  // East: the first true cave dungeon — the hollow's dark interior past Lowleaf
  // (Glimmerstep-gated on Lowleaf's `to_deepwood` warp; B2 first Hollowing contact).
  // The track is "Deep Glimmer", the Lowleaf brief's deep-interior variant.
  glowmoss_deep: {
    json: 'assets/maps/glowmoss_deep.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    music: 'assets/audio/music/lowleaf-hollow-c.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/glowmoss-deep-a.webp',
      'assets/backgrounds/battle/glowmoss-deep-b.webp',
    ],
  },
  // The lower floor (ladder pair from the SE alcove) — the dungeon-scale
  // ladder's first taught descent; holds the Spore Grotto's true mouth.
  glowmoss_deep_b1f: {
    json: 'assets/maps/glowmoss_deep_b1f.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    music: 'assets/audio/music/lowleaf-hollow-c.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/glowmoss-deep-a.webp',
      'assets/backgrounds/battle/glowmoss-deep-b.webp',
    ],
  },
  // Spore Grotto — the Glowmoss complex's deep spur (off B1F): the rare bed.
  spore_grotto: {
    json: 'assets/maps/spore_grotto.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    music: 'assets/audio/music/lowleaf-hollow-c.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/glowmoss-deep-a.webp',
      'assets/backgrounds/battle/glowmoss-deep-b.webp',
    ],
  },
  // Saltreach Fen I — the marsh route east of Pearlmoor (the pattern-library
  // showcase: ledged bank, plank causeways, paint-derived reed zones).
  saltreach_fen_i: {
    json: 'assets/maps/saltreach_fen_i.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/saltreach-fen-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/saltreach-fen-a.webp',
      'assets/backgrounds/battle/saltreach-fen-b.webp',
    ],
  },
  // Saltreach Fen II — the deep channels: Tidecall load-bearing, the E1
  // lantern-reed line, the Sunkbell turn-off, the treeline to Lowleaf.
  saltreach_fen_ii: {
    json: 'assets/maps/saltreach_fen_ii.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/saltreach-fen-b.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/saltreach-fen-a.webp',
      'assets/backgrounds/battle/saltreach-fen-b.webp',
    ],
  },
  // Sunkbell Shallows — the drowned-shrine spur off Fen II (Tidecall, MISSABLE).
  sunkbell_shallows: {
    json: 'assets/maps/sunkbell_shallows.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/saltreach-fen-c.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/saltreach-fen-a.webp',
      'assets/backgrounds/battle/saltreach-fen-b.webp',
    ],
  },
  // Lowleaf Hollow — the fern town mid-Glowmoss-Bloom (Lumenary 3, Verdant).
  lowleaf_hollow: {
    json: 'assets/maps/lowleaf_hollow.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'town',
    music: 'assets/audio/music/lowleaf-hollow-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/lowleaf-hollow-a.webp',
      'assets/backgrounds/battle/lowleaf-hollow-b.webp',
    ],
  },
  lowleaf_lumenary: {
    json: 'assets/maps/lowleaf_lumenary.json',
    tilesets: { interior_stone_set: 'assets/tilesets/interior_stone_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/lowleaf-hollow-b.mp3',
    // Lampwarden 3 (Verdant) Gleam battle happens here — moss-garden hall backdrop.
    battle_backdrops: [
      'assets/backgrounds/battle/lowleaf-lumenary-a.webp',
      'assets/backgrounds/battle/lowleaf-lumenary-b.webp',
    ],
  },
  lowleaf_bower: {
    json: 'assets/maps/lowleaf_bower.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/lowleaf-hollow-b.mp3',
  },
  // Cinderhead Mine — the gem-mine settlement (Lumenary 4, Stone: Otho Grist);
  // the Lamp-down vigil festival + the Descent Vigil earned loop (the §4 wall).
  cinderhead_mine: {
    json: 'assets/maps/cinderhead_mine.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    music: 'assets/audio/music/cinderhead-mine-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/cinderhead-mine-a.webp',
      'assets/backgrounds/battle/cinderhead-mine-b.webp',
    ],
  },
  cinderhead_lumenary: {
    json: 'assets/maps/cinderhead_lumenary.json',
    tilesets: { interior_stone_set: 'assets/tilesets/interior_stone_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/cinderhead-mine-b.mp3',
    // Lampwarden 4 (Stone) Gleam battle happens here — mine-hall backdrop.
    battle_backdrops: [
      'assets/backgrounds/battle/cinderhead-mine-a.webp',
      'assets/backgrounds/battle/cinderhead-mine-b.webp',
    ],
  },
  // Cinderhead Deep — a 3-floor ladder MAZE (the Descent Vigil, level-design §2a).
  // Upper = the fork: the sealed-door shortcut (flag:shortcut_mine), the Crystoll
  // [LATER] tease, the ungated gallery to Galehigh, and the ladder down. The
  // vigil-lamp waits on b2f (the "third gallery").
  cinderhead_deep: {
    json: 'assets/maps/cinderhead_deep.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    music: 'assets/audio/music/cinderhead-mine-c.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/cinderhead-mine-a.webp',
      'assets/backgrounds/battle/cinderhead-mine-b.webp',
    ],
  },
  cinderhead_deep_b1f: {
    json: 'assets/maps/cinderhead_deep_b1f.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    music: 'assets/audio/music/cinderhead-mine-c.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/cinderhead-mine-a.webp',
      'assets/backgrounds/battle/cinderhead-mine-b.webp',
    ],
  },
  cinderhead_deep_b2f: {
    json: 'assets/maps/cinderhead_deep_b2f.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    music: 'assets/audio/music/cinderhead-mine-c.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/cinderhead-mine-a.webp',
      'assets/backgrounds/battle/cinderhead-mine-b.webp',
    ],
  },
  // Galehigh Terraces — the North's cliff-farm town (Lumenary 5, Storm: Mira
  // Vael) under the Kite-rising; the Kite-Rising Winch earned loop hauls the
  // player up to the skyloft for the bond-test at the launch ledge.
  galehigh_terraces: {
    json: 'assets/maps/galehigh_terraces.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'town',
    music: 'assets/audio/music/galehigh-terraces-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/galehigh-terraces-a.webp',
      'assets/backgrounds/battle/galehigh-terraces-b.webp',
    ],
  },
  galehigh_skyloft: {
    json: 'assets/maps/galehigh_skyloft.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    // spur maps reuse the parent loop + backdrops (the Phase-0 reuse table)
    music: 'assets/audio/music/galehigh-terraces-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/galehigh-terraces-a.webp',
      'assets/backgrounds/battle/galehigh-terraces-b.webp',
    ],
  },
  galehigh_lumenary: {
    json: 'assets/maps/galehigh_lumenary.json',
    tilesets: { interior_stone_set: 'assets/tilesets/interior_stone_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/galehigh-terraces-b.mp3',
  },
  galehigh_inn: {
    json: 'assets/maps/galehigh_inn.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/galehigh-terraces-b.mp3',
  },
  galehigh_home: {
    json: 'assets/maps/galehigh_home.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/galehigh-terraces-b.mp3',
  },
  galehigh_kitemaker: {
    json: 'assets/maps/galehigh_kitemaker.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/galehigh-terraces-b.mp3',
  },
  // Windward Stair I → II — the North's great switchback climb (band 34-36);
  // the I→II wind-gap is the Updraft Kite boundary, and reaching the II crags
  // sets flag:shortcut_windward (the drop home to Galehigh).
  windward_stair_i: {
    json: 'assets/maps/windward_stair_i.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/windward-stair-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/windward-stair-a.webp',
      'assets/backgrounds/battle/windward-stair-b.webp',
    ],
  },
  windward_stair_ii: {
    json: 'assets/maps/windward_stair_ii.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/windward-stair-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/windward-stair-a.webp',
      'assets/backgrounds/battle/windward-stair-b.webp',
    ],
  },
  // The wind country's Updraft spurs reuse the stair loop + backdrops (the
  // Phase-0 reuse table): the Wind-Eye sky-grotto (unique Storm kin) off
  // Galehigh, and Thunderroost (the storm-birds' aerie) off Windward II.
  wind_eye: {
    json: 'assets/maps/wind_eye.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    music: 'assets/audio/music/windward-stair-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/windward-stair-a.webp',
      'assets/backgrounds/battle/windward-stair-b.webp',
    ],
  },
  thunderroost: {
    json: 'assets/maps/thunderroost.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'route',
    music: 'assets/audio/music/windward-stair-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/windward-stair-a.webp',
      'assets/backgrounds/battle/windward-stair-b.webp',
    ],
  },
  // Pale Vault Glacier — the North's aurora-lit ice town (Lumenary 6, Frost:
  // Ysolde Frost) under the Aurora-watch; the Lamp-Line earned loop sends the
  // player down the undercroft to light seven brackets before the bond-test
  // at the vault's heart. B3 (Còr in person), C3 (Fenn's confession) and A4
  // (Wren's wobble) all land on this ice.
  pale_vault_glacier: {
    json: 'assets/maps/pale_vault_glacier.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'town',
    music: 'assets/audio/music/pale-vault-glacier-a.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/pale-vault-glacier-a.webp',
      'assets/backgrounds/battle/pale-vault-glacier-b.webp',
    ],
  },
  pale_vault_undercroft: {
    json: 'assets/maps/pale_vault_undercroft.json',
    tilesets: { vesper_overworld_set: 'assets/tilesets/vesper_overworld_set.webp' },
    kind: 'cave',
    // the trial reuses the parent loop's sparsest variant + backdrops
    music: 'assets/audio/music/pale-vault-glacier-c.mp3',
    battle_backdrops: [
      'assets/backgrounds/battle/pale-vault-glacier-a.webp',
      'assets/backgrounds/battle/pale-vault-glacier-b.webp',
    ],
  },
  pale_vault_lumenary: {
    json: 'assets/maps/pale_vault_lumenary.json',
    tilesets: { interior_stone_set: 'assets/tilesets/interior_stone_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/pale-vault-glacier-b.mp3',
  },
  pale_vault_inn: {
    json: 'assets/maps/pale_vault_inn.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/pale-vault-glacier-b.mp3',
  },
  pale_vault_home: {
    json: 'assets/maps/pale_vault_home.json',
    tilesets: { interior_set: 'assets/tilesets/interior_set.webp' },
    kind: 'interior',
    music: 'assets/audio/music/pale-vault-glacier-b.mp3',
  },
  // Further areas are registered here as their JSON + tilesets are authored.
  // See docs/world/atlas.md for the full area list and their music/graphics briefs.
  // Their battle backdrops are already rendered — see UPCOMING_BATTLE_BACKDROPS below.
};

/**
 * Battle backdrops for the upcoming atlas areas (4-14), rendered ahead of the maps
 * themselves (240x160 WebP under public/assets/backgrounds/battle/, a/b variants per
 * area, following docs/art-style.md "Battle backdrops"). Keyed by the area's planned
 * snake_case map id. When you author one of these maps, just spread the matching entry
 * onto its registry block above — `battle_backdrops: UPCOMING_BATTLE_BACKDROPS.lowleaf_hollow`
 * — so the art wires up without retyping paths. Once a map moves into MAP_REGISTRY with
 * its backdrops set, drop its key here to avoid drift.
 */
export const UPCOMING_BATTLE_BACKDROPS: Record<string, string[]> = {
  sunken_solarium: [
    'assets/backgrounds/battle/sunken-solarium-a.webp',
    'assets/backgrounds/battle/sunken-solarium-b.webp',
  ],
  nightreach_observatory: [
    'assets/backgrounds/battle/nightreach-observatory-a.webp',
    'assets/backgrounds/battle/nightreach-observatory-b.webp',
  ],
  coldfog_marches: [
    'assets/backgrounds/battle/coldfog-marches-a.webp',
    'assets/backgrounds/battle/coldfog-marches-b.webp',
  ],
  vesper_crossroads: [
    'assets/backgrounds/battle/vesper-crossroads-a.webp',
    'assets/backgrounds/battle/vesper-crossroads-b.webp',
  ],
  penumbra_ring: [
    'assets/backgrounds/battle/penumbra-ring-a.webp',
    'assets/backgrounds/battle/penumbra-ring-b.webp',
  ],
  umbral_spire: [
    'assets/backgrounds/battle/umbral-spire-a.webp',
    'assets/backgrounds/battle/umbral-spire-b.webp',
  ],
  dawnstead: [
    'assets/backgrounds/battle/dawnstead-a.webp',
    'assets/backgrounds/battle/dawnstead-b.webp',
  ],
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
