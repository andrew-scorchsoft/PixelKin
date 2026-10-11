/**
 * NORTH world-craft content (docs/reviews/world-craft-panel.md §6): this region's
 * package OWNS this file — new optional scripts + dialogue only, spread into the
 * registries via regions/index.ts. Map placements that reference these refs ride
 * tools/maps/worldcraft/north.py (run through tools/maps/add_world_craft.py).
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

export const NORTH_SCRIPTS: ScriptRegistry = {};

export const NORTH_DIALOGUE: DialogueRegistry = {};
