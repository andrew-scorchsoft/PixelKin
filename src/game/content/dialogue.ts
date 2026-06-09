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
  // Star-tender Fenn — spoken to again after the intro cutscene. Warm, unhurried.
  'npc.mentor_intro': [
    { speaker: 'FENN', text: 'Steady now, apprentice. The dark is only the dark — it keeps no grudge.' },
    { speaker: 'FENN', text: 'Catch a kin in the verge by the north gate, then take its bond to Brisa. The Lumenary is the tall hall up the square.' },
    { speaker: 'FENN', text: 'Tend your lamp, and it tends you back. I will be along the coast road when you are ready.' },
  ],
  // The rival Wren — a fellow young Wayfarer in the plaza (A1). Warm and competitive;
  // by canon Wren takes the starter that beats yours along Ember->Verdant->Tide->Ember.
  'npc.wren_intro': [
    { speaker: 'WREN', text: 'You as well? Ha — Fenn sends us all out the same week. Good.' },
    { speaker: 'WREN', text: "Whatever partner you pick, I'm taking the one that gives you trouble. Only fair." },
    { speaker: 'WREN', text: "Race you to fill the whole map with light, then. Loser carries the lamp oil." },
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

  // --- Tinderwick general store (interior) ---
  'sign.tinderwick_shop_wares': [
    { text: 'TINDERWICK GENERAL STORE\nLamp oil, salve, spare wicks — all a Wayfarer needs for the dark road.' },
  ],
  'npc.tinderwick_shopkeeper': [
    { speaker: 'SHOPKEEPER', text: 'Welcome in, out of the dusk. Stocking up for your Wayfaring, are you?' },
    { speaker: 'SHOPKEEPER', text: 'Lamp oil keeps the vesperlamp bright; a salve mends a tired kin. Take what you need — the road north is long.' },
    { speaker: 'SHOPKEEPER', text: '(The counter is being restocked — wares open up properly once the shop system is wired.)' },
  ],

  // --- Tinderwick Lumenary (interior) ---
  'sign.tinderwick_lumenary_inside': [
    { text: 'THE EMBER LUMENARY\nHere the Ember constellation is tended. Bring a steady bond, and a steady hand.' },
  ],
  'npc.brisa_tallow': [
    { speaker: 'BRISA TALLOW', text: 'Mind the aisle, dear — step up to the altar when your kin is ready, and we shall light the sky together.' },
  ],

  // --- Dimglass Coast route ---
  'sign.dimglass_buoys': [
    { text: 'DIMGLASS COAST\nThe buoys offshore only answer a lit lamp. Gullcry Rock waits past the shallows.' },
  ],
  'sign.dimglass_cave': [
    { text: 'A dark mouth gapes in the cliff. Too deep to walk without a lantern that drinks the dark.' },
  ],
  'sign.dimglass_route': [
    { text: 'Keep to the lit lane. The grass is restless since the dusk — kin nest in it.' },
  ],
  'sign.dimglass_to_pearlmoor': [
    { text: 'NORTH: PEARLMOOR QUAY\nThe tidal flats lie ahead, where the lamps stand in the water.' },
  ],
  // The coast NPC is the rival Wren again (A2): canon has Wren's first friendly battle here.
  // Until the trainer-battle cutscene is wired, this lands the beat as a clear dialogue tease.
  'npc.dimglass_wayfarer': [
    { speaker: 'WREN', text: "Caught up already? You keep to the lamps, I'll cut through the grass — let's see who reaches Pearlmoor first." },
    { speaker: 'WREN', text: "When you're set, the two of us should battle proper. No Lamps, no stakes — just us and our partners." },
    { speaker: 'WREN', text: 'Did you see the sky a moment ago? A star just... went out. Gave me the shivers. Keep your lamp close out here.' },
  ],

  // --- Dimglass Coast II (the tidal flats) ---
  'sign.flats_gullcry': [
    { text: 'GULLCRY ROCK — past the buoy line.\nThe shallows answer only a Tidecall. Lamps out, Wayfarer.' },
  ],
  'sign.flats_cave': [
    { text: 'TIDEGLASS CAVERN\nDark past the third step. Without a Glimmerstep, the dark keeps it.' },
  ],
  'sign.flats_to_quay': [
    { text: 'NORTH: PEARLMOOR QUAY\nSee the lantern-strings on the masts? Nearly there.' },
  ],
  'npc.flats_wayfarer_a': [
    { speaker: 'MORROW', text: 'The flats look empty, but the dune grass is alive. Good place to toughen a young kin before the harbour.' },
  ],
  'npc.flats_wayfarer_b': [
    { speaker: 'ELSPETH', text: 'I run letters between the Lumenaries. Reyl Wash at Pearlmoor — now THERE is a battle worth the walk.' },
  ],
  // C2 — Fenn finds the player after `dusk_begins` and names the Skyweave
  // (walkthrough/01-south: this may land here at the head of II).
  'npc.flats_sky_watcher': [
    { speaker: 'STAR-TENDER FENN', text: 'You saw it too, then. The sky and the ground hold hands here, child — snuff a kin\'s light and a star goes dark with it.' },
    { speaker: 'STAR-TENDER FENN', text: 'That is what we walk against. Relight the constellations, one Gleam at a time. Pearlmoor keeps the second.' },
  ],

  // --- Pearlmoor Quay (town) ---
  'sign.pearlmoor_welcome': [
    { text: 'PEARLMOOR QUAY\nMind the wet boards. Lanterns strung mast to mast since the Long Dusk — the moon is our only other light.' },
  ],
  'sign.pearlmoor_lumenary': [
    { text: 'THE TIDE LUMENARY\nLampwarden Reyl Wash tends the Tide constellation. The door is open to all — no lit shallows needed.' },
  ],
  'sign.pearlmoor_harbour': [
    { text: 'THE HARBOUR SHALLOWS\nThe moon-water will not part for the unlit. Earn the Tidecall, and the islets and sea-shrine open to you.' },
  ],
  'sign.pearlmoor_shop': [
    { text: 'PEARLMOOR CHANDLERY\nNets, oil, salve, and tide-charms for the crossing. Step in out of the spray.' },
  ],
  'npc.pearlmoor_shopkeeper': [
    { speaker: 'CHANDLER', text: 'Welcome in off the boards. Restocking before you face Reyl, are you?' },
    { speaker: 'CHANDLER', text: "Bring a warm partner — an Ember or a leafy one. Reyl's whole crew runs Tide, and the triangle favours the prepared." },
    { speaker: 'CHANDLER', text: '(The counter is being restocked — wares open up properly once the shop system is wired.)' },
  ],
  'npc.reyl_wash': [
    { speaker: 'REYL WASH', text: 'Step up to the sea-altar when your bond is ready, Wayfarer. The Tide does not hurry, and neither shall we.' },
  ],
  'npc.pearlmoor_innkeep': [
    { speaker: 'INNKEEP', text: "Rest your feet, Wayfarer. The Tide-blessing's near — the whole quay hangs fresh lanterns for it." },
    { speaker: 'INNKEEP', text: 'They say when Reyl relights the Tide, the harbour shallows answer a lit lamp. Old ferryman magic. The moon listens to him.' },
  ],
  'npc.pearlmoor_fisher': [
    { speaker: 'FISHER', text: 'Tide-blessing tonight! We string the buoys, sing the old going-out song, and ask the sea to bring our lights home.' },
    { speaker: 'FISHER', text: 'Reyl tends the Lumenary up the boardwalk — tallest hall on the quay, you cannot miss its moon-lamp.' },
  ],
};

const FALLBACK: DialogueLine[] = [{ text: '...' }];

/** Resolve a dialogue ref to its pages, or a quiet fallback if unknown. */
export function getDialogue(ref: string | undefined): DialogueLine[] {
  if (!ref) return FALLBACK;
  return DIALOGUE[ref] ?? FALLBACK;
}
