/**
 * Waystones — the Lanternway's fast-travel network (pause menu -> TRAVEL).
 *
 * Once the four-way hub at Vesper Crossroads opens (`flag:hub_unlocked` — the
 * diegetic moment every lantern-road finally connects), the apprentice can light
 * a waystone and step the lit road from any town they've reached to any other.
 * Each entry below is a TOWN or hub with a waystone-worthy anchor: a fixed,
 * walkable landing tile by its heart (the Lumenary door apron, or the town's
 * own waystone), plus the flag that proves the player has BEEN there.
 *
 * Data-driven by design: a destination is "known" iff its `visited_flag` is held,
 * and every town reuses its existing CHART discovery flag (`chart:<id>`, banked by
 * WorldScene.noteChartDiscovery on first footfall) — so the travel list fills in
 * for free as the player explores, with no new save field and no extra wiring.
 * (Dawnstead's chart is only discoverable once `flag:dawn` is held, which is the
 * same gate we'd want anyway — so its chart flag doubles as a dawn gate.)
 *
 * Authoring: cosy, a little melancholy, canon vocabulary only (kin, Lumenary,
 * Gleam, vesperlamp — never monster/gym/badge). Keep each `flavour` to one short
 * evocative line for the detail pane.
 */
import type { Facing } from '@game/data/world/types';
import type { Region } from '@game/data/world/graph';

export interface Waystone {
  id: string;
  /** Display name (the town as the player knows it). */
  name: string;
  /** Region group for the travel list. */
  region: Region;
  /** Destination map id (a registered map). */
  map: string;
  /** Where the lit road sets the player down — a proven-walkable anchor by the town's heart. */
  tx: number;
  ty: number;
  facing: Facing;
  /** Held iff the player has reached this place (its chart discovery flag). */
  visited_flag: string;
  /** One-line canon flavour for the detail pane. */
  flavour: string;
}

/**
 * The waystone-bearing towns of Vesperholm. Landing tiles are the towns' Lumenary
 * door aprons / waystone tiles — each is a proven warp destination the engine already
 * sets players down on, so it's walkable + spawn-safe by construction (and enterMap's
 * findSafeTile spirals to the nearest passable tile as a final belt-and-braces guard).
 */
export const WAYSTONES: readonly Waystone[] = [
  // ---- The South ------------------------------------------------------------
  {
    id: 'tinderwick',
    name: 'Tinderwick',
    region: 'south',
    map: 'tinderwick',
    tx: 19,
    ty: 8,
    facing: 'down',
    visited_flag: 'chart:tinderwick',
    flavour: 'The first lamp, kept burning at the dusk’s edge.',
  },
  {
    id: 'pearlmoor_quay',
    name: 'Pearlmoor Quay',
    region: 'south',
    map: 'pearlmoor_quay',
    tx: 14,
    ty: 7,
    facing: 'down',
    visited_flag: 'chart:pearlmoor-quay',
    flavour: 'The pearl-port that keeps the tide for a clock.',
  },
  {
    id: 'dawnstead',
    name: 'Dawnstead',
    region: 'south',
    map: 'dawnstead',
    tx: 15,
    ty: 28,
    facing: 'up',
    visited_flag: 'chart:dawnstead',
    flavour: 'The hamlet that waited longest, and woke to morning at last.',
  },
  // ---- The East -------------------------------------------------------------
  {
    id: 'lowleaf_hollow',
    name: 'Lowleaf Hollow',
    region: 'east',
    map: 'lowleaf_hollow',
    tx: 10,
    ty: 9,
    facing: 'down',
    visited_flag: 'chart:lowleaf-hollow',
    flavour: 'A forest town beneath a canopy that never sees noon.',
  },
  {
    id: 'cinderhead_mine',
    name: 'Cinderhead Mine',
    region: 'east',
    map: 'cinderhead_mine',
    tx: 12,
    ty: 9,
    facing: 'down',
    visited_flag: 'chart:cinderhead-mine',
    flavour: 'A mining town set into a hill of warm, breathing stone.',
  },
  // ---- The North ------------------------------------------------------------
  {
    id: 'galehigh_terraces',
    name: 'Galehigh Terraces',
    region: 'north',
    map: 'galehigh_terraces',
    tx: 9,
    ty: 18,
    facing: 'down',
    visited_flag: 'chart:galehigh-terraces',
    flavour: 'Wind-carved steps where the storms have made their home.',
  },
  {
    id: 'pale_vault_glacier',
    name: 'Pale Vault Glacier',
    region: 'north',
    map: 'pale_vault_glacier',
    tx: 14,
    ty: 9,
    facing: 'down',
    visited_flag: 'chart:pale-vault-glacier',
    flavour: 'A town of blue ice beneath a vault of frozen stars.',
  },
  // ---- The West -------------------------------------------------------------
  {
    id: 'sunken_solarium',
    name: 'Sunken Solarium',
    region: 'west',
    map: 'sunken_solarium',
    tx: 5,
    ty: 8,
    facing: 'down',
    visited_flag: 'chart:sunken-solarium',
    flavour: 'A sun-temple half-drowned, still warm with stored daylight.',
  },
  {
    id: 'nightreach_observatory',
    name: 'Nightreach Observatory',
    region: 'west',
    map: 'nightreach_observatory',
    tx: 15,
    ty: 10,
    facing: 'down',
    visited_flag: 'chart:nightreach-observatory',
    flavour: 'A star-watchers’ town under the clearest dark in Vesperholm.',
  },
  // ---- The Outer Ring -------------------------------------------------------
  {
    id: 'vesper_crossroads',
    name: 'Vesper Crossroads',
    region: 'outer',
    map: 'vesper_crossroads',
    tx: 9,
    ty: 17,
    facing: 'up',
    visited_flag: 'chart:vesper-crossroads',
    flavour: 'Where every lantern-road meets, and the Lanternway begins.',
  },
];

/** The flag that opens the TRAVEL option at all (the four-way hub connected). */
export const WAYSTONE_NETWORK_FLAG = 'flag:hub_unlocked';

/** Display order for the region groups in the travel list (matches the charts gallery). */
export const WAYSTONE_REGION_ORDER: readonly Region[] = ['south', 'east', 'north', 'west', 'outer', 'central'];
