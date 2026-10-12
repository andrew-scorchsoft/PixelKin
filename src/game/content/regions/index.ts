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
// The Wild Ways (09-the-wild-ways.md): one module per new area.
import { WICKRUN_DIALOGUE, WICKRUN_SCRIPTS } from './wickrun';
import { MIRELIGHT_DIALOGUE, MIRELIGHT_SCRIPTS } from './mirelight';
import { RIMEWAY_DIALOGUE, RIMEWAY_SCRIPTS } from './rimeway';
import { OLDSEAMS_DIALOGUE, OLDSEAMS_SCRIPTS } from './oldseams';
import { SUNVAULT_DIALOGUE, SUNVAULT_SCRIPTS } from './sunvault';
import { RECKONWORKS_DIALOGUE, RECKONWORKS_SCRIPTS } from './reckonworks';

export const REGION_EXTRA_SCRIPTS: ScriptRegistry = {
  ...SOUTH_SCRIPTS,
  ...EAST_SCRIPTS,
  ...NORTH_SCRIPTS,
  ...WEST_SCRIPTS,
  ...CENTRAL_SCRIPTS,
  ...SCHOOL_SCRIPTS,
  ...WICKRUN_SCRIPTS,
  ...MIRELIGHT_SCRIPTS,
  ...RIMEWAY_SCRIPTS,
  ...OLDSEAMS_SCRIPTS,
  ...SUNVAULT_SCRIPTS,
  ...RECKONWORKS_SCRIPTS,
};

export const REGION_EXTRA_DIALOGUE: DialogueRegistry = {
  ...SOUTH_DIALOGUE,
  ...EAST_DIALOGUE,
  ...NORTH_DIALOGUE,
  ...WEST_DIALOGUE,
  ...CENTRAL_DIALOGUE,
  ...SCHOOL_DIALOGUE,
  ...WICKRUN_DIALOGUE,
  ...MIRELIGHT_DIALOGUE,
  ...RIMEWAY_DIALOGUE,
  ...OLDSEAMS_DIALOGUE,
  ...SUNVAULT_DIALOGUE,
  ...RECKONWORKS_DIALOGUE,
};
