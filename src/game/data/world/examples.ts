/**
 * A typed example map, used as a compile-time smoke test for the map schema (it is checked
 * by `npm run typecheck` via `satisfies MapDefinition`) and as a reference for authors.
 * The runtime-loaded equivalent lives at `public/assets/maps/tinderwick.json`.
 *
 * This is a tiny 4x3 stub (not the real Tinderwick) — just enough to exercise every part
 * of the schema: layers, a warp, a trigger, an encounter zone, an NPC, and an ability gate.
 */
import type { MapDefinition } from './types';

export const EXAMPLE_MAP = {
  id: 'example_stub',
  display_name: 'Example Stub',
  width: 4,
  height: 3,
  tile_width: 16,
  tile_height: 16,
  kind: 'town',
  tilesets: [
    {
      name: 'tinderwick_set',
      image: 'assets/tilesets/tinderwick_set.png',
      tile_width: 16,
      tile_height: 16,
      first_gid: 1,
      columns: 8,
      tile_count: 32,
    },
  ],
  layers: [
    { name: 'base', role: 'base', depth: 0, data: [1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1] },
    { name: 'above', role: 'above', depth: 20, data: [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0] },
  ],
  warps: [
    {
      id: 'to_coast',
      at: { tx: 3, ty: 1 },
      trigger: 'step_on',
      to_map: 'dimglass_coast',
      to: { tx: 1, ty: 1 },
      facing: 'right',
      transition: 'fade',
    },
  ],
  triggers: [
    {
      id: 'sign_dock',
      kind: 'sign',
      at: { tx: 1, ty: 0 },
      activation: 'interact',
      ref: 'sign.tinderwick_dock',
    },
  ],
  encounters: [
    {
      id: 'verge_grass',
      terrain: 'tall_grass',
      rect: { tx: 0, ty: 2, w: 4, h: 1 },
      encounter_rate: 0.12,
      table: [
        { kin_id: 1, weight: 60, min_level: 2, max_level: 4 },
        { kin_id: 2, weight: 40, min_level: 2, max_level: 4 },
      ],
    },
  ],
  npcs: [
    {
      id: 'mentor',
      at: { tx: 2, ty: 1 },
      facing: 'down',
      sprite: 'npc_mentor',
      movement: 'static',
      dialogue_ref: 'npc.mentor_intro',
    },
  ],
  gates: [
    {
      id: 'dock_tide',
      ability: 'tidecall',
      tiles: [{ tx: 0, ty: 2 }],
      effect: 'make_passable',
    },
  ],
} satisfies MapDefinition;
