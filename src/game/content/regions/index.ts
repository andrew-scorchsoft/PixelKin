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
// The Wayward Arms (2026-10): the hotel on the rise north of the Wanderwood.
import { HOTEL_DIALOGUE, HOTEL_SCRIPTS } from './hotel';
// The kitchens (2026-10): Percy's moka brew-stand (Duskapple) + Marisol's kitchen (Lowleaf).
import { KITCHENS_DIALOGUE, KITCHENS_SCRIPTS } from './kitchens';
// Paul's House (2026-10): the Booji-Wooji Man's home on Wayward Rise.
import { PAUL_DIALOGUE, PAUL_SCRIPTS } from './paul';
// The Old Light, R10 (2026-10): the jest-house's regulars, props and Pip.
import { JESTHOUSE_DIALOGUE, JESTHOUSE_SCRIPTS } from './jesthouse';
// The inn folk (2026-10): Hesper the Echo-Reader (every inn) + Ottilie the Namewright.
import { INNFOLK_DIALOGUE, INNFOLK_SCRIPTS } from './innfolk';
// The Farlamp Isles (walkthrough/10 Part I) — Lane C1: the surface, Driftholm, the mainland hooks.
import { FARLAMP_DIALOGUE, FARLAMP_SCRIPTS } from './farlamp';
// Lane E (walkthrough/10 Part III): Lowtinder & Tinderwick Bay, the town under the bay.
import { LOWTINDER_DIALOGUE, LOWTINDER_SCRIPTS } from './lowtinder';
// Lane A (walkthrough/10 Part II): the Ashfall Shelf + Kiln Gully.
import { ASHFALL_DIALOGUE, ASHFALL_SCRIPTS } from './ashfall';
// The Farlamp Isles, lane C2 (2026-10): the Undertide + the Drowned Lamp.
import { UNDERTIDE_DIALOGUE, UNDERTIDE_SCRIPTS } from './undertide';
// The Lumenary sparring partners (2026-10 economy review).
import { SPARRING_DIALOGUE, SPARRING_SCRIPTS } from '../sparring';
// Lane N1 (11-the-hollowing-country.md Parts A + E): Stillwater + the late-north density.
import { STILLWATER_DIALOGUE, STILLWATER_SCRIPTS } from './stillwater';

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
  ...HOTEL_SCRIPTS,
  ...KITCHENS_SCRIPTS,
  ...PAUL_SCRIPTS,
  ...JESTHOUSE_SCRIPTS,
  ...INNFOLK_SCRIPTS,
  ...FARLAMP_SCRIPTS,
  ...LOWTINDER_SCRIPTS, // Lane E
  ...ASHFALL_SCRIPTS,
  ...UNDERTIDE_SCRIPTS,
  ...SPARRING_SCRIPTS,
  ...STILLWATER_SCRIPTS, // Lane N1
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
  ...HOTEL_DIALOGUE,
  ...KITCHENS_DIALOGUE,
  ...PAUL_DIALOGUE,
  ...JESTHOUSE_DIALOGUE,
  ...INNFOLK_DIALOGUE,
  ...FARLAMP_DIALOGUE,
  ...LOWTINDER_DIALOGUE, // Lane E
  ...ASHFALL_DIALOGUE,
  ...UNDERTIDE_DIALOGUE,
  ...SPARRING_DIALOGUE,
  ...STILLWATER_DIALOGUE, // Lane N1
};
