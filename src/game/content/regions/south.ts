/**
 * SOUTH world-craft content (docs/reviews/world-craft-panel.md §6): this region's
 * package OWNS this file — new optional scripts + dialogue only, spread into the
 * registries via regions/index.ts. Map placements that reference these refs ride
 * tools/maps/worldcraft/south.py (run through tools/maps/add_world_craft.py).
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

export const SOUTH_SCRIPTS: ScriptRegistry = {};

export const SOUTH_DIALOGUE: DialogueRegistry = {
  // --- Gullcry Rock (post-Chickenpig Tidecall spur): the wreck on the sand ---
  'npc.gullcry_wreck': [
    { text: 'The ribs of a small boat, sunk to the gunwales in sand. Someone painted a lamp on her bow, once.' },
    { text: 'The gulls have made a nest of her. They seem to think that is what she was for all along.' },
  ],
  // --- Wrackline Path (§4 #8): three inspect-only finds in the wrack --------
  'npc.wrack_find_pots': [
    { text: 'Crab pots, washed up and stacked by a tidy stranger. One still holds a very offended crab.' },
    { text: 'You leave it be. It has had a long night too.' },
  ],
  'npc.wrack_find_drift': [
    { text: 'Driftwood, worn silver. Someone has scratched a tally into it: one mark for every star gone dark this winter.' },
    { text: 'The marks stop halfway along, as if whoever kept count decided they would rather not.' },
  ],
  'npc.wrack_find_nest': [
    { text: 'A gull\'s nest of kelp and string. Woven through it, a scrap of lantern-ribbon from some Pearlmoor festival.' },
  ],
  // --- Sounding Cave (§4 #8): the sounding stone answers -------------------
  'npc.sounding_stone': [
    { text: 'You knock on the stone. The cave knocks back — three times, then once, from somewhere above and to the north.' },
    { text: 'Echoes don\'t usually point. This one does: up the narrow way, into the little high chamber.' },
  ],
  // --- The Wanderwood (S5): the wayfarers' board -------------------------------
  'npc.wanderwood_board': [
    { text: 'A wayfarers\' board, mossy at the corners. FOUND: one glove, left. LOST: one glove, left. Same handwriting.' },
    { text: 'Under them, newer: "If you are lost, stand still and somebody kind will come by. They always have so far."' },
  ],
};
