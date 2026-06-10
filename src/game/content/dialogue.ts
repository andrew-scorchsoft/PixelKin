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
  // --- The opening errand (Fenn at the Crossroads waystone) ---
  // Fenn mid-errand: spoken to again before the satchel comes home.
  'npc.fenn_waiting': [
    { speaker: 'FENN', text: 'The general store, dear apprentice — my satchel is on the counter, where I left it like a fool. The keeper will know it.' },
    { speaker: 'FENN', text: 'I shall mind the waystone. It is good company, for a stone.' },
  ],
  // Fenn after the ceremony: the waystone send-off, until the story moves him on.
  'npc.fenn_waystone_after': [
    { speaker: 'FENN', text: 'Steady now, apprentice. The dark is only the dark — it keeps no grudge.' },
    { speaker: 'FENN', text: 'Catch a kin in the verge by the north gate, then take its bond to Brisa. The Lumenary is the tall hall up the square.' },
    { speaker: 'FENN', text: 'Tend your lamp, and it tends you back. I will be along the coast road when you are ready.' },
  ],
  // The north gate-warden, once the Wayfaring has begun (the pre-starter warning
  // is script.gate_warden; this is the well-wisher swap, stood aside by the verge).
  'npc.gatewarden_after': [
    { speaker: 'GATE-WARDEN', text: 'A lamp and a friend — NOW you look like a Wayfarer. The road north is yours.' },
    { speaker: 'GATE-WARDEN', text: 'Mind the verge grass as you go. Restless, but generous — a careful apprentice walks out of it with a second friend.' },
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
    { text: 'NORTH: the coast road, past the gate. EAST: the Lanternway, to the Star-tender\'s waystone. South, the sea sleeps under the Long Dusk.' },
  ],
  'sign.tinderwick_lanternway': [
    { text: 'EAST: THE LANTERNWAY\nEvery lit road in Vesperholm meets at the Vesper Crossroads. Keep to the lamps.' },
  ],

  // --- Apprentice's house interior ---
  'sign.house_shelf': [
    { text: 'A row of spare wicks and an old field-journal. Pages of half-lit constellations.' },
  ],
  'npc.house_parent': [
    { speaker: 'GRAN', text: 'Off on your Wayfaring at last. Star-tender Fenn left word — he is out at the Crossroads waystone, east along the Lanternway.' },
    { speaker: 'GRAN', text: 'Keep to the lit road, love. And come home warm.' },
  ],

  // --- Tinderwick general store (interior) ---
  'sign.tinderwick_shop_wares': [
    { text: 'TINDERWICK GENERAL STORE\nLamp oil, salve, spare wicks — all a Wayfarer needs for the dark road.' },
  ],
  // The keeper before the Wayfaring begins — points the player east to Fenn.
  'npc.tinderwick_keeper_early': [
    { speaker: 'SHOPKEEPER', text: 'Looking for the Star-tender? You just missed him — went east along the Lanternway at first bell. Said the Crossroads waystone wanted tending.' },
    { speaker: 'SHOPKEEPER', text: 'Seemed in a hurry to be waiting for someone, if you take my meaning.' },
  ],
  // The keeper during the satchel errand (Fenn has asked; the satchel sits by the counter).
  'npc.tinderwick_keeper_errand': [
    { speaker: 'SHOPKEEPER', text: "His satchel? There by the counter, dear — he'd forget his own lamp if it weren't lit. Take it out to him." },
    { speaker: 'SHOPKEEPER', text: 'And tell him the trade-cart is late again. He likes knowing things.' },
  ],
  // The trading keeper — appears once the kit script has run (flag:tinderwick_kit);
  // their placement ref is script.shop_tinderwick (these lines, then the counter).
  'npc.tinderwick_shopkeeper': [
    { speaker: 'SHOPKEEPER', text: 'How is the kit holding up? A lamp catches a kin; the balm mends one. Use them well.' },
    { speaker: 'SHOPKEEPER', text: 'And the counter is open, dear — wicks for wares, wares for wicks. Have a look.' },
  ],

  // --- Tinderwick Lumenary hall (interior) + the Beacon quest stages ---
  'sign.tinderwick_lumenary_inside': [
    { text: 'THE EMBER LUMENARY\nThe hall keeps the rite; the OLD BEACON on the east bluff keeps the light. One key serves both.' },
  ],
  'npc.brisa_tallow': [
    { speaker: 'BRISA TALLOW', text: 'Mind the aisle, dear — step up when your kin is ready, and we shall light the sky together.' },
  ],
  // Stage 3: the wick-key is home — Brisa heads for the lantern room.
  'npc.brisa_meet_beacon': [
    { speaker: 'BRISA TALLOW', text: 'The wick-key, home at last! Oh, well WALKED, dear.' },
    { speaker: 'BRISA TALLOW', text: 'The beacon foot door stands on the east bluff, past the Lumenary. It answers your key now — climb to the lantern. I shall be waiting at the top.' },
  ],
  // Stage 4: post-Gleam, back in the hall, festival outside.
  'npc.brisa_after': [
    { speaker: 'BRISA TALLOW', text: 'Hear the square? They rang the fair-bell the moment the Ember stood up. That dance is yours, dear.' },
    { speaker: 'BRISA TALLOW', text: 'When your feet itch again — the coast road runs north past the flats to Pearlmoor. Reyl Wash keeps the Tide. Tell the old ferryman I sent you.' },
  ],
  // --- The Beacon (interiors) ---
  'sign.beacon_door': [
    { text: 'THE OLD BEACON\nThe foot door is wick-locked. Its key walked away down the coast road, years ago.' },
  ],
  'sign.beacon_floor_i': [
    { text: 'Stair-litany, floor the first: "A flame is carried, never kept."' },
  ],
  'sign.beacon_floor_ii': [
    { text: 'Stair-litany, floor the second: "The dark is only the dark. Climb."' },
  ],
  'npc.beacon_keeper_a_after': [
    { speaker: 'TANSY', text: 'Up you go, then. Mind Cole on the next floor — and mind the litany. It helps, truly.' },
  ],
  'npc.beacon_keeper_b_after': [
    { speaker: 'COLE', text: 'The lantern room is just above. Three hundred years that wick waited... go on. Make it four hundred and none.' },
  ],
  // Brisa's "not yet" — the bond-test waits until the player has caught a wild kin
  // (the catch-first soft gate; blocked_ref on the lumenary_battle trigger).
  'npc.brisa_not_ready': [
    { speaker: 'BRISA TALLOW', text: 'Eager, dear — I do like that. But a Wayfaring is walked with friends you CHOOSE, not only the one you were given.' },
    { speaker: 'BRISA TALLOW', text: 'Go catch a wild kin in the verge by the north gate — the grass is generous tonight. Then come light the sky with me.' },
  ],
  // Lantern-fair! Festival NPCs appear in the square once the Ember Gleam is lit
  // (requires_flag 'gleam:ember') — Arc E: a Gleam is belonging, not conquest.
  'npc.fair_piper': [
    { speaker: 'FAIR PIPER', text: 'Hear the square tonight! Brisa rang the fair-bell the moment the Ember stood back up in the sky.' },
    { speaker: 'FAIR PIPER', text: 'Your doing, was it? Then the first dance is yours, Wayfarer. The Long Dusk can sit this one out.' },
  ],
  'npc.fair_kid': [
    { speaker: 'LANTERN KID', text: 'Look UP, look up! That one, the warm one — Gran says it went dark before I was even born!' },
    { speaker: 'LANTERN KID', text: 'When I get my vesperlamp, I am going to relight a WHOLE sky. Maybe two skies.' },
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
  // An early Hollowing SEED — a weather-worn notice nailed to a coast post. Courteous,
  // sorrowful, unsigned (the name scratched out): the player meets the Hollowing's
  // *voice* long before its face (B2, East). Foreboding only — never explained here.
  'sign.dimglass_pinned_letter': [
    { text: "A notice, rain-warped and nailed to a leaning post. The hand is careful, almost kind:" },
    { text: '"Friends of the coast — grieve no more for the lights that fail. The dark is not your enemy. It is only rest, come early. Let it in, and be at peace."' },
    { text: 'The signature has been scratched away to bare wood. Below it, in a different, shakier hand: "DO NOT LISTEN."' },
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
  'sign.pearlmoor_lanternway': [
    { text: 'WEST: THE LANTERNWAY\nThe lit road to the Vesper Crossroads, where every way in Vesperholm meets.' },
  ],
  'sign.pearlmoor_to_fen': [
    { text: 'EAST: SALTREACH FEN\nThe fen-road sleeps unlit. When the southern crown stands whole, the east wakes.' },
  ],
  'sign.pearlmoor_shop': [
    { text: 'PEARLMOOR CHANDLERY\nNets, oil, salve, and tide-charms for the crossing. Step in out of the spray.' },
  ],
  // The trading chandler — appears once the crossing-kit has been given;
  // their placement ref is script.shop_pearlmoor (these lines, then the counter).
  'npc.pearlmoor_shopkeeper': [
    { speaker: 'CHANDLER', text: "Bright lamps hold their catch — worth it for the harbour kin. Reyl's whole crew runs Tide; the triangle favours the prepared." },
    { speaker: 'CHANDLER', text: 'The counter is open — salves, lamps, and a few Star-charts off the last cart. Wicks well spent, Wayfarer.' },
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
  // Tide-blessing festival NPCs — appear on the quay once 'gleam:tide' is lit.
  'npc.blessing_elder': [
    { speaker: 'QUAY ELDER', text: 'The Tide stands up over the water again. Sixty years I waited to see the going-out song sung under it.' },
    { speaker: 'QUAY ELDER', text: 'Tides go out so they can come back. Reyl always says it. Tonight, child, you brought one back.' },
  ],
  'npc.blessing_kid': [
    { speaker: 'NET-MENDER', text: 'The shallows are ANSWERING! Watch — every buoy lights when the moon-water moves. The old folk are crying. Happy crying!' },
    { speaker: 'NET-MENDER', text: 'They say the Wayfarer who relit it can walk the harbour water now. Gullcry Rock, the sea-shrine, all of it. Imagine!' },
  ],

  // --- Dimglass Coast: the witness (appears after flag:dusk_begins, B1) -------
  'npc.dimglass_witness': [
    { speaker: 'OLD LAMPLIGHTER', text: 'You stood under it too, did you. One breath it was there — the next, a hole in the sky shaped like a star.' },
    { speaker: 'OLD LAMPLIGHTER', text: 'Third one this season, south of here. Towns gone quiet, lamps unlit... Walk careful, young one. And walk LIT.' },
  ],

  // --- Gullcry Rock (Tidecall spur — the backtrack payoff) --------------------
  'sign.gullcry_rock': [
    { text: 'GULLCRY ROCK\nThe sea-birds kept this light when no one else could reach it. Tread kindly — the harbour-lights nest in the spray.' },
  ],

  // --- Vesper Crossroads (the Lanternway hub) ---------------------------------
  'sign.crossroads': [
    { text: 'VESPER CROSSROADS\nAll the Lanternway meets here. SOUTH-WEST: Tinderwick. SOUTH-EAST: Pearlmoor Quay. The other roads sleep, unlit.' },
  ],
  'sign.crossroads_spire': [
    { text: 'The inward road. Eight braziers stand cold around its gate — one for each constellation. The mountain waits.' },
  ],
  'npc.lanternway_keeper': [
    { speaker: 'WAYKEEPER', text: 'Every road in Vesperholm touches this stone sooner or later. I keep the lamps lit on the two that still walk.' },
    { speaker: 'WAYKEEPER', text: 'When more Gleams stand up in the sky, more roads wake. That is how the Lanternway has always worked.' },
    { speaker: 'WAYKEEPER', text: 'The inward road? Eight Gleams, Wayfarer. Eight. Do not hurry the dark.' },
  ],
};

const FALLBACK: DialogueLine[] = [{ text: '...' }];

/** Resolve a dialogue ref to its pages, or a quiet fallback if unknown. */
export function getDialogue(ref: string | undefined): DialogueLine[] {
  if (!ref) return FALLBACK;
  return DIALOGUE[ref] ?? FALLBACK;
}
