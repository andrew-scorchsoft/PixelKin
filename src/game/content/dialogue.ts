/**
 * Dialogue registry — all sign / NPC / incidental text, keyed by the `ref` strings
 * maps use (EventTrigger.ref, NpcPlacement.dialogue_ref). Adding lines is a data
 * edit here, never engine code. Keep the voice cosy and a little melancholy —
 * "lanterns in the dark" — and use canon vocabulary (kin, Lumenary, Gleam,
 * Lantern Gift, vesperlamp), never generic monster/gym/badge.
 */
import type { DialogueLine, DialogueRegistry } from './types';

export const DIALOGUE: DialogueRegistry = {
  'sign.tinderwick_dock': [
    { text: 'TINDERWICK DOCKS\nMind the lanterns — the tide comes in quiet since the Long Dusk.' },
  ],
  'npc.mentor_intro': [
    { speaker: 'MENTOR', text: 'There you are, apprentice. The sky lost another light last night.' },
    { speaker: 'MENTOR', text: 'Take your vesperlamp. A kin will walk with you. Tend the dark, and it tends you back.' },
  ],
  'npc.child_lanterns': [
    { speaker: 'CHILD', text: "I counted the lamps! Three went out by the quay. Will you light them again?" },
  ],

  // --- Tinderwick town signs ---
  'sign.tinderwick_square': [
    { text: 'TINDERWICK SQUARE\nWares and warm lamps within. Mind the step.' },
  ],
  'sign.tinderwick_lumenary': [
    { text: 'TINDERWICK LUMENARY\nLampwarden Brisa Tallow tends the Ember light. Bring a kin and a steady hand.' },
  ],
  'sign.tinderwick_mentor': [
    { text: 'The lit path runs north to the coast. South, the sea sleeps under the Long Dusk.' },
  ],

  // --- Apprentice's house interior ---
  'sign.house_shelf': [
    { text: 'A row of spare wicks and an old field-journal. Pages of half-lit constellations.' },
  ],
  'npc.house_parent': [
    { speaker: 'GRAN', text: 'Off on your Wayfaring at last. Keep your vesperlamp trimmed, and come home warm.' },
  ],

  // --- Dimglass Coast route ---
  'sign.dimglass_buoys': [
    { text: 'DIMGLASS COAST\nThe buoys offshore only answer a lit lamp. Gullcry Rock waits past the shallows.' },
  ],
  'sign.dimglass_shore': [
    { text: 'A dark mouth gapes in the cliff. Too deep to walk without a lantern that drinks the dark.' },
  ],
  'sign.dimglass_route': [
    { text: 'Keep to the lit lane. The grass is restless since the dusk — kin nest in it.' },
  ],
  'sign.dimglass_to_pearlmoor': [
    { text: 'NORTH: PEARLMOOR QUAY\nThe tidal flats lie ahead, where the lamps stand in the water.' },
  ],
  'npc.dimglass_wayfarer': [
    { speaker: 'WAYFARER', text: 'Cosy night for a walk, if you keep to the lamps. Watch the grass — Brinelets are quick.' },
    { speaker: 'WAYFARER', text: 'Those buoys? They light a path over the shallows, once your lamp can call the tide.' },
  ],
};

const FALLBACK: DialogueLine[] = [{ text: '...' }];

/** Resolve a dialogue ref to its pages, or a quiet fallback if unknown. */
export function getDialogue(ref: string | undefined): DialogueLine[] {
  if (!ref) return FALLBACK;
  return DIALOGUE[ref] ?? FALLBACK;
}
