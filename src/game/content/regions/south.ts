/**
 * SOUTH world-craft content (docs/reviews/world-craft-panel.md §6): this region's
 * package OWNS this file — new optional scripts + dialogue only, spread into the
 * registries via regions/index.ts. Map placements that reference these refs ride
 * tools/maps/worldcraft/south.py (run through tools/maps/add_world_craft.py).
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

export const SOUTH_SCRIPTS: ScriptRegistry = {};

export const SOUTH_DIALOGUE: DialogueRegistry = {};
