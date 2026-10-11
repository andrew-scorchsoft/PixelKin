/**
 * The world-craft regional content hook (WP0): each region's package owns ONE
 * module here (south/east/north/west/central) so parallel packages never touch the
 * shared registries. `content/scripts.ts` and `content/dialogue.ts` spread these
 * at the END of their registries (the OLDLIGHT_SCRIPTS precedent) — a regional ref
 * must be NEW, never an override of an existing one.
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';
import { SOUTH_DIALOGUE, SOUTH_SCRIPTS } from './south';
import { EAST_DIALOGUE, EAST_SCRIPTS } from './east';
import { NORTH_DIALOGUE, NORTH_SCRIPTS } from './north';
import { WEST_DIALOGUE, WEST_SCRIPTS } from './west';
import { CENTRAL_DIALOGUE, CENTRAL_SCRIPTS } from './central';
import { SCHOOL_DIALOGUE, SCHOOL_SCRIPTS } from './school';

export const REGION_EXTRA_SCRIPTS: ScriptRegistry = {
  ...SOUTH_SCRIPTS,
  ...EAST_SCRIPTS,
  ...NORTH_SCRIPTS,
  ...WEST_SCRIPTS,
  ...CENTRAL_SCRIPTS,
  ...SCHOOL_SCRIPTS,
};

export const REGION_EXTRA_DIALOGUE: DialogueRegistry = {
  ...SOUTH_DIALOGUE,
  ...EAST_DIALOGUE,
  ...NORTH_DIALOGUE,
  ...WEST_DIALOGUE,
  ...CENTRAL_DIALOGUE,
  ...SCHOOL_DIALOGUE,
};
