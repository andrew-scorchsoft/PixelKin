/**
 * The Vesperholm world graph: how maps connect, how connectivity CHANGES as Lantern
 * Gifts and progression flags are earned, and how the central Umbral Spire hub opens
 * its four cardinal approaches. See `docs/world/atlas.md` §1 + §3 for the wiring (the
 * full route network — segments, spurs, landmarks, shortcuts) this models.
 *
 * Structure (classic town -> route -> town): main inter-town routes are split into named
 * SEGMENTS (e.g. dimglass_coast_i/ii) with the gift-gate on a segment boundary; each
 * region has an optional SPUR (dead-end with a reward, often behind a later gift so you
 * backtrack); a few signature LANDMARKS are bigger optional micro-dungeons; and a couple
 * of late SHORTCUTS re-link a route to the hub once opened from the far side.
 */
import type { AbilityId, TileCoord, WorldFlag } from './types';

/** Where a node sits relative to the central hub (drives the 4-way unlock). */
export type Region = 'north' | 'south' | 'east' | 'west' | 'central' | 'outer';

/** A node = one map in the world. */
export interface AreaNode {
  map_id: string; // -> MapDefinition.id
  region: Region;
  /** Node only reachable / shown once this flag is satisfied (optional). */
  unlocked_by_flag?: WorldFlag;
  /** Optional/side content (a spur or landmark), not on the critical path. */
  optional?: boolean;
  /** For optional nodes: a short note on the reward hidden there (rare kin / item). */
  reward?: string;
}

/**
 * A directed connection between two maps, gated independently of geometry so connectivity
 * can be reasoned about. An edge becomes traversable only once its requirements are met —
 * this is how the map opens up as gifts/flags are earned.
 */
export interface WorldEdge {
  from_map: string;
  to_map: string;
  via_warp: string; // the Warp.id on from_map that realises this edge
  requires_ability?: AbilityId; // blocked until this gift is earned
  requires_flag?: WorldFlag; // blocked until this flag is set
  bidirectional: boolean;
}

export interface HubApproach {
  region: Region;
  /** The flag (set when that quadrant's constellations relight) that opens this approach. */
  opens_flag: WorldFlag;
}

export interface WorldGraph {
  start_map: string;
  start_at: TileCoord;
  nodes: AreaNode[];
  edges: WorldEdge[];
  /**
   * The central region, initially unreachable. Each cardinal approach opens when its flag
   * is set; the hub is fully 4-way once all four are set (which sets `flag:hub_unlocked`).
   */
  hub: {
    map_id: string;
    approaches: HubApproach[];
  };
}

/**
 * The Vesperholm world graph instance — the source of truth for connectivity and gating.
 * Map JSON for most of these areas is authored over time; this graph defines the shape.
 */
export const VESPERHOLM_GRAPH: WorldGraph = {
  start_map: 'tinderwick',
  start_at: { tx: 6, ty: 17 }, // on the lane just outside the player's cottage door, facing up
  nodes: [
    // ---- South: Tinderwick -> Dimglass Coast (2 segments) -> Pearlmoor Quay ----------
    { map_id: 'tinderwick', region: 'south' },
    { map_id: 'tinderwick_house', region: 'south' }, // interior: the apprentice's cottage
    { map_id: 'tinderwick_shop', region: 'south' }, // interior: the general store
    { map_id: 'tinderwick_lumenary', region: 'south' }, // interior: the Ember Lumenary hall (Brisa Tallow)
    { map_id: 'tinderwick_beacon_i', region: 'south' }, // interior: the old beacon, stair floor I (wick-key gated)
    { map_id: 'tinderwick_beacon_ii', region: 'south' }, // interior: the old beacon, stair floor II
    { map_id: 'tinderwick_beacon_top', region: 'south' }, // interior: the lantern room — the Ember bond-test
    { map_id: 'dimglass_coast', region: 'south' }, // route segment I: cliff path + shore (authored)
    { map_id: 'dimglass_coast_ii', region: 'south' }, // route: tidal flats
    { map_id: 'gullcry_rock', region: 'south', optional: true, reward: 'rare sea-bird kin + a Tide charm' },
    { map_id: 'tideglass_cavern', region: 'south', optional: true, reward: 'landmark micro-dungeon; a signature rare water kin' },
    { map_id: 'pearlmoor_quay', region: 'south' },
    { map_id: 'pearlmoor_breakwater', region: 'south' }, // the Causeway Bell's foot causeway (Moor-bell shrine)
    { map_id: 'pearlmoor_lumenary', region: 'south' }, // interior: the Tide Lumenary (Reyl Wash)
    { map_id: 'pearlmoor_shop', region: 'south' }, // interior: the port chandlery
    { map_id: 'pearlmoor_inn', region: 'south' }, // interior: the quayside inn
    // ---- East: Saltreach Fen (2 segments) -> Lowleaf forest -> Cinderhead cave -------
    { map_id: 'saltreach_fen_i', region: 'east' }, // route: open marsh
    { map_id: 'saltreach_fen_ii', region: 'east' }, // route: deep channels
    { map_id: 'sunkbell_shallows', region: 'east', optional: true, reward: 'rare Tide kin + item cache in a flooded shrine' },
    { map_id: 'lowleaf_hollow', region: 'east' }, // forest town + Lumenary
    { map_id: 'lowleaf_lumenary', region: 'east' }, // interior: the Verdant Lumenary (Sable Quill)
    { map_id: 'lowleaf_bower', region: 'east' }, // interior: the festival guest-bower (rest point)
    { map_id: 'glowmoss_deep', region: 'east' }, // forest interior (Glimmerstep)
    { map_id: 'glowmoss_deep_b1f', region: 'east' }, // the lower maze floor (ladder pair)
    { map_id: 'spore_grotto', region: 'east', optional: true, reward: 'rare Bug/Verdant kin + item' },
    { map_id: 'cinderhead_mine', region: 'east' }, // cave town + Lumenary (mine mouth)
    { map_id: 'cinderhead_lumenary', region: 'east' }, // interior: the Stone Lumenary (Otho Grist)
    { map_id: 'cinderhead_deep', region: 'east' }, // deep cave (Glimmerstep): the fork floor -> Galehigh
    { map_id: 'cinderhead_deep_b1f', region: 'east' }, // the descent's middle floor (gallery-miner B, the ledger)
    { map_id: 'cinderhead_deep_b2f', region: 'east' }, // the third gallery: the vigil-lamp (deepest)
    { map_id: 'crystoll_vault', region: 'east', optional: true, reward: 'late backtrack (Starreach): rare Stone/Light kin' },
    // ---- North: Galehigh -> Windward Stair (2 segments) -> Pale Vault ---------------
    { map_id: 'galehigh_terraces', region: 'north' },
    { map_id: 'galehigh_skyloft', region: 'north' }, // the winch-festival top terrace: Mira's launch-ledge bond-test (Lumenary 5's venue)
    { map_id: 'galehigh_lumenary', region: 'north' }, // interior: the Storm hall (festival home — the battle is at the skyloft)
    { map_id: 'galehigh_inn', region: 'north' }, // interior: the terrace inn (rest point)
    { map_id: 'galehigh_home', region: 'north' }, // interior: a wind-break cottage
    { map_id: 'galehigh_kitemaker', region: 'north' }, // interior: the kite-maker's workshop (shop)
    { map_id: 'windward_stair_i', region: 'north' }, // route: lower switchbacks
    { map_id: 'windward_stair_ii', region: 'north' }, // route: high crags
    { map_id: 'thunderroost', region: 'north', optional: true, reward: 'rare Storm/Flying kin + item' },
    { map_id: 'wind_eye', region: 'north', optional: true, reward: 'landmark sky-grotto; a unique Storm kin' },
    { map_id: 'pale_vault_glacier', region: 'north' },
    { map_id: 'pale_vault_undercroft', region: 'north' }, // the Lamp-Line trial: Ysolde's bond-test at its heart (Lumenary 6's venue)
    { map_id: 'pale_vault_lumenary', region: 'north' }, // interior: the Frost hall (the Aurora-watch's home — the battle is in the undercroft)
    { map_id: 'pale_vault_inn', region: 'north' }, // interior: the glacier inn (rest point)
    { map_id: 'pale_vault_home', region: 'north' }, // interior: an ice-block cottage
    // ---- West: Hushfrost Pass (2 seg) -> Solarium -> Sunvault Climb (2 seg) -> Nightreach
    { map_id: 'hushfrost_pass_i', region: 'west' }, // route: snow canyon
    { map_id: 'hushfrost_pass_ii', region: 'west' }, // route: coldfog throat
    { map_id: 'aurora_hollow', region: 'west', optional: true, reward: 'rare Frost/Light kin + item' },
    { map_id: 'sunken_solarium', region: 'west' },
    { map_id: 'sunken_solarium_lumenary', region: 'west' }, // interior: the Solar hall (the troupe's green-room + the rest point — the battle is on the lit stage outdoors)
    { map_id: 'sunvault_climb_i', region: 'west' }, // route: overgrown terraces
    { map_id: 'sunvault_climb_ii', region: 'west' }, // route: sun-vine bridges
    { map_id: 'helia_vault', region: 'west', optional: true, reward: 'rare Solar kin + item in a sealed reliquary' },
    { map_id: 'nightreach_observatory', region: 'west' },
    // ---- Outer: Coldfog Marches (2 segments) + the hub ------------------------------
    { map_id: 'coldfog_marches_i', region: 'outer' }, // route: blighted marsh
    { map_id: 'coldfog_marches_ii', region: 'outer' }, // route: deep coldfog
    { map_id: 'drownlight_beacon', region: 'outer', optional: true, reward: 'rare Dark kin in a snuffed lighthouse' },
    { map_id: 'hollowfen_stillworks', region: 'outer', optional: true, reward: "landmark micro-dungeon: a derelict Hollowing null-works; a powerful Storm/Dark 'charged husk' kin" },
    { map_id: 'vesper_crossroads', region: 'outer' },
    // ---- Central: Penumbra Ring -> Umbral Spire (+ a late landmark) -> Dawnstead -----
    { map_id: 'penumbra_ring', region: 'central' },
    { map_id: 'starwell', region: 'central', optional: true, reward: 'post-Crown landmark (Starreach): a near-legendary kin' },
    { map_id: 'umbral_spire', region: 'central', unlocked_by_flag: 'flag:hub_unlocked' },
    { map_id: 'dawnstead', region: 'south', unlocked_by_flag: 'flag:dawn' },
  ],
  edges: [
    // ---- Tinderwick interiors (door warps, both ways) --------------------------------
    { from_map: 'tinderwick', to_map: 'tinderwick_house', via_warp: 'to_house', bidirectional: true },
    { from_map: 'tinderwick', to_map: 'tinderwick_shop', via_warp: 'to_shop', bidirectional: true },
    { from_map: 'tinderwick', to_map: 'tinderwick_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    // The old beacon on the NE bluff — the earned first Gleam: door opens with the
    // wick-key from the Dimglass lamplighter, the floors carry wick-tender trainers,
    // and Brisa's bond-test waits in the lantern room at the top.
    { from_map: 'tinderwick', to_map: 'tinderwick_beacon_i', via_warp: 'to_beacon', requires_flag: 'flag:has_beacon_wick', bidirectional: true },
    { from_map: 'tinderwick_beacon_i', to_map: 'tinderwick_beacon_ii', via_warp: 'up_stairs', bidirectional: true },
    { from_map: 'tinderwick_beacon_ii', to_map: 'tinderwick_beacon_top', via_warp: 'up_stairs', bidirectional: true },

    // ---- Pearlmoor Quay interiors (door warps, both ways) ----------------------------
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_shop', via_warp: 'to_shop', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_inn', via_warp: 'to_inn', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    // The Causeway Bell: the moor-gate opens with the netmender's rope (the
    // earned second-Gleam loop; Reyl's bond-test waits on flag:q_south_bell_rung).
    { from_map: 'pearlmoor_quay', to_map: 'pearlmoor_breakwater', via_warp: 'to_breakwater', requires_flag: 'flag:q_south_has_rope', bidirectional: true },

    // ---- Main rim, clockwise: town -> route segment -> ... -> town -------------------
    { from_map: 'tinderwick', to_map: 'dimglass_coast', via_warp: 'to_coast', bidirectional: true },
    // The canon segment chain: Dimglass I -> the tidal flats of Dimglass II -> Pearlmoor.
    // II is the South spine's level bridge (~8-10 band + two route-trainer beats) and the
    // home of both gift-gated spurs (Gullcry Rock / Tideglass Cavern).
    { from_map: 'dimglass_coast', to_map: 'dimglass_coast_ii', via_warp: 'to_coast_ii', bidirectional: true },
    { from_map: 'dimglass_coast_ii', to_map: 'pearlmoor_quay', via_warp: 'to_quay', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'saltreach_fen_i', via_warp: 'to_fen', bidirectional: true },
    { from_map: 'saltreach_fen_i', to_map: 'saltreach_fen_ii', via_warp: 'to_fen_ii', requires_ability: 'tidecall', bidirectional: true },
    { from_map: 'saltreach_fen_ii', to_map: 'lowleaf_hollow', via_warp: 'to_hollow', bidirectional: true },
    // Lowleaf interiors (door warps, both ways)
    { from_map: 'lowleaf_hollow', to_map: 'lowleaf_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'lowleaf_hollow', to_map: 'lowleaf_bower', via_warp: 'to_bower', bidirectional: true },
    { from_map: 'lowleaf_hollow', to_map: 'glowmoss_deep', via_warp: 'to_deepwood', requires_ability: 'glimmerstep', bidirectional: true },
    { from_map: 'glowmoss_deep', to_map: 'cinderhead_mine', via_warp: 'to_mine', bidirectional: true },
    { from_map: 'cinderhead_mine', to_map: 'cinderhead_lumenary', via_warp: 'to_lumenary', bidirectional: true },
    { from_map: 'cinderhead_mine', to_map: 'cinderhead_deep', via_warp: 'to_deep', requires_ability: 'glimmerstep', bidirectional: true },
    { from_map: 'cinderhead_deep', to_map: 'galehigh_terraces', via_warp: 'to_terraces', bidirectional: true },
    // Galehigh interiors (door warps, both ways) + the Kite-Rising Winch: the
    // skyloft is gated by the FESTIVAL flag (the earned loop, spine §5 shape #5)
    // — never by Updraft Kite (§0 rule 1; Updraft is Mira's reward).
    { from_map: 'galehigh_terraces', to_map: 'galehigh_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'galehigh_inn', via_warp: 'to_inn', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'galehigh_home', via_warp: 'to_home', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'galehigh_kitemaker', via_warp: 'to_shop', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'galehigh_skyloft', via_warp: 'to_skyloft', requires_flag: 'flag:q_north_kite_blessed', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'windward_stair_i', via_warp: 'to_stair', bidirectional: true },
    { from_map: 'windward_stair_i', to_map: 'windward_stair_ii', via_warp: 'to_stair_ii', requires_ability: 'updraft_kite', bidirectional: true },
    { from_map: 'windward_stair_ii', to_map: 'pale_vault_glacier', via_warp: 'to_glacier', bidirectional: true },
    // Pale Vault interiors (door warps, both ways) + the Lamp-Line: the
    // undercroft door takes the aurora-oil (the earned loop, spine §5 shape
    // #6) — NEVER an ability gate (§0 rule 1: Ysolde is reachable on foot).
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_inn', via_warp: 'to_inn', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_home', via_warp: 'to_home', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'pale_vault_undercroft', via_warp: 'to_undercroft', requires_flag: 'flag:q_north_aurora_oil', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'hushfrost_pass_i', via_warp: 'to_pass', bidirectional: true },
    { from_map: 'hushfrost_pass_i', to_map: 'hushfrost_pass_ii', via_warp: 'to_pass_ii', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'hushfrost_pass_ii', to_map: 'sunken_solarium', via_warp: 'to_solarium', bidirectional: true },
    // The Solar hall is starter-gated like every Lumenary door (NEVER Sunsketch — §0 rule 1).
    { from_map: 'sunken_solarium', to_map: 'sunken_solarium_lumenary', via_warp: 'to_lumenary', requires_flag: 'flag:has_starter', bidirectional: true },
    { from_map: 'sunken_solarium', to_map: 'sunvault_climb_i', via_warp: 'to_climb', bidirectional: true },
    { from_map: 'sunvault_climb_i', to_map: 'sunvault_climb_ii', via_warp: 'to_climb_ii', requires_ability: 'sunsketch', bidirectional: true },
    { from_map: 'sunvault_climb_ii', to_map: 'nightreach_observatory', via_warp: 'to_observatory', bidirectional: true },
    // Coldfog detour (off the hub), then onward to Nightreach from its blighted side.
    { from_map: 'coldfog_marches_i', to_map: 'coldfog_marches_ii', via_warp: 'to_marsh_ii', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'coldfog_marches_ii', to_map: 'nightreach_observatory', via_warp: 'to_observatory_fog', requires_ability: 'emberward', bidirectional: true },

    // ---- Optional spurs (dead-ends with rewards; several need a later gift) ----------
    { from_map: 'dimglass_coast_ii', to_map: 'gullcry_rock', via_warp: 'to_gullcry', requires_ability: 'tidecall', bidirectional: true },
    { from_map: 'dimglass_coast_ii', to_map: 'tideglass_cavern', via_warp: 'to_tideglass', requires_ability: 'glimmerstep', bidirectional: true },
    { from_map: 'saltreach_fen_ii', to_map: 'sunkbell_shallows', via_warp: 'to_sunkbell', requires_ability: 'tidecall', bidirectional: true },
    { from_map: 'glowmoss_deep', to_map: 'glowmoss_deep_b1f', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'glowmoss_deep_b1f', to_map: 'spore_grotto', via_warp: 'to_grotto', requires_ability: 'glimmerstep', bidirectional: true },
    // Cinderhead Deep is a 3-floor ladder maze (the Descent Vigil); the vigil-lamp sits on b2f.
    { from_map: 'cinderhead_deep', to_map: 'cinderhead_deep_b1f', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'cinderhead_deep_b1f', to_map: 'cinderhead_deep_b2f', via_warp: 'ladder_down', bidirectional: true },
    { from_map: 'cinderhead_deep', to_map: 'crystoll_vault', via_warp: 'to_crystoll', requires_ability: 'starreach', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'wind_eye', via_warp: 'to_windeye', requires_ability: 'updraft_kite', bidirectional: true },
    { from_map: 'windward_stair_ii', to_map: 'thunderroost', via_warp: 'to_roost', requires_ability: 'updraft_kite', bidirectional: true },
    { from_map: 'hushfrost_pass_ii', to_map: 'aurora_hollow', via_warp: 'to_aurora', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'sunvault_climb_ii', to_map: 'helia_vault', via_warp: 'to_helia', requires_ability: 'sunsketch', bidirectional: true },
    { from_map: 'coldfog_marches_ii', to_map: 'drownlight_beacon', via_warp: 'to_beacon', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'coldfog_marches_ii', to_map: 'hollowfen_stillworks', via_warp: 'to_stillworks', requires_ability: 'glimmerstep', bidirectional: true },
    { from_map: 'penumbra_ring', to_map: 'starwell', via_warp: 'to_starwell', requires_ability: 'starreach', bidirectional: true },

    // ---- Lanternway spokes: rim towns <-> the outer-ring hub --------------------------
    { from_map: 'tinderwick', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'lowleaf_hollow', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'nightreach_observatory', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'vesper_crossroads', to_map: 'coldfog_marches_i', via_warp: 'to_marsh', bidirectional: true },

    // ---- Late shortcuts: open from the far side, then permanently re-link to the hub --
    { from_map: 'windward_stair_ii', to_map: 'galehigh_terraces', via_warp: 'shortcut_galehigh', requires_flag: 'flag:shortcut_windward', bidirectional: true },
    { from_map: 'cinderhead_deep', to_map: 'vesper_crossroads', via_warp: 'shortcut_crossroads', requires_flag: 'flag:shortcut_mine', bidirectional: true },

    // ---- Hub -> centre, gated by the progressive crown flags -------------------------
    { from_map: 'vesper_crossroads', to_map: 'penumbra_ring', via_warp: 'to_penumbra', requires_flag: 'flag:hub_unlocked', bidirectional: true },
    { from_map: 'penumbra_ring', to_map: 'umbral_spire', via_warp: 'to_spire', requires_ability: 'starreach', bidirectional: true },
    { from_map: 'umbral_spire', to_map: 'dawnstead', via_warp: 'to_dawn', requires_flag: 'flag:dawn', bidirectional: true },
  ],
  hub: {
    map_id: 'vesper_crossroads',
    approaches: [
      { region: 'south', opens_flag: 'flag:crown_south' },
      { region: 'east', opens_flag: 'flag:crown_east' },
      { region: 'north', opens_flag: 'flag:crown_north' },
      { region: 'west', opens_flag: 'flag:crown_west' },
    ],
  },
};
