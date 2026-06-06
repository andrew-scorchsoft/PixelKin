/**
 * The Vesperholm world graph: how maps connect, how connectivity CHANGES as Lantern
 * Gifts and progression flags are earned, and how the central Umbral Spire hub opens
 * its four cardinal approaches. See `docs/world/atlas.md` for the wiring this models.
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
 * The Vesperholm world graph instance. Outer-rim nodes are travelled clockwise early game;
 * the Vesper Crossroads connects the rim, and its spokes to the Umbral Spire open via the
 * `crown_*` flags. (Map JSON for most of these areas is authored over time — this graph is
 * the source of truth for connectivity and gating.)
 */
export const VESPERHOLM_GRAPH: WorldGraph = {
  start_map: 'tinderwick',
  start_at: { tx: 8, ty: 12 },
  nodes: [
    // Towns and the themed routes that connect them (routes carry the wild encounters
    // and most of the traversal gating — see docs/world/atlas.md §3).
    { map_id: 'tinderwick', region: 'south' },
    { map_id: 'dimglass_coast', region: 'south' }, // route: coast + grass
    { map_id: 'pearlmoor_quay', region: 'south' },
    { map_id: 'saltreach_fen', region: 'east' }, // route: marsh + water
    { map_id: 'lowleaf_hollow', region: 'east' }, // forest route + town
    { map_id: 'cinderhead_mine', region: 'east' }, // cave route + town
    { map_id: 'galehigh_terraces', region: 'north' },
    { map_id: 'windward_stair', region: 'north' }, // route: mountain
    { map_id: 'pale_vault_glacier', region: 'north' },
    { map_id: 'hushfrost_pass', region: 'west' }, // route: frozen + coldfog
    { map_id: 'sunken_solarium', region: 'west' },
    { map_id: 'sunvault_climb', region: 'west' }, // route: sun-garden
    { map_id: 'nightreach_observatory', region: 'west' },
    { map_id: 'coldfog_marches', region: 'outer' }, // route: blighted marsh
    { map_id: 'vesper_crossroads', region: 'outer' },
    { map_id: 'penumbra_ring', region: 'central' },
    { map_id: 'umbral_spire', region: 'central', unlocked_by_flag: 'flag:hub_unlocked' },
    { map_id: 'dawnstead', region: 'south', unlocked_by_flag: 'flag:dawn' },
  ],
  edges: [
    // Outer rim, clockwise: town -> route -> town. The route between two towns is its
    // own map, and the gift earned in/around a town opens the route beyond it.
    { from_map: 'tinderwick', to_map: 'dimglass_coast', via_warp: 'to_coast', bidirectional: true },
    { from_map: 'dimglass_coast', to_map: 'pearlmoor_quay', via_warp: 'to_quay', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'saltreach_fen', via_warp: 'to_fen', bidirectional: true },
    { from_map: 'saltreach_fen', to_map: 'lowleaf_hollow', via_warp: 'to_hollow', bidirectional: true },
    { from_map: 'lowleaf_hollow', to_map: 'cinderhead_mine', via_warp: 'to_mine', requires_ability: 'glimmerstep', bidirectional: true },
    { from_map: 'cinderhead_mine', to_map: 'galehigh_terraces', via_warp: 'to_terraces', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'windward_stair', via_warp: 'to_stair', bidirectional: true },
    { from_map: 'windward_stair', to_map: 'pale_vault_glacier', via_warp: 'to_glacier', requires_ability: 'updraft_kite', bidirectional: true },
    { from_map: 'pale_vault_glacier', to_map: 'hushfrost_pass', via_warp: 'to_pass', bidirectional: true },
    { from_map: 'hushfrost_pass', to_map: 'sunken_solarium', via_warp: 'to_solarium', requires_ability: 'emberward', bidirectional: true },
    { from_map: 'sunken_solarium', to_map: 'sunvault_climb', via_warp: 'to_climb', bidirectional: true },
    { from_map: 'sunvault_climb', to_map: 'nightreach_observatory', via_warp: 'to_observatory', requires_ability: 'sunsketch', bidirectional: true },
    { from_map: 'coldfog_marches', to_map: 'nightreach_observatory', via_warp: 'to_observatory_fog', requires_ability: 'emberward', bidirectional: true },
    // Rim spokes into the outer-ring hub.
    { from_map: 'tinderwick', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'pearlmoor_quay', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'lowleaf_hollow', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'galehigh_terraces', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    { from_map: 'nightreach_observatory', to_map: 'vesper_crossroads', via_warp: 'to_crossroads', bidirectional: true },
    // Hub -> centre, gated by the progressive crown flags.
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
