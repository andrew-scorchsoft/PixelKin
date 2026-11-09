/**
 * Dialogue registry — all sign / NPC / incidental text, keyed by the `ref` strings
 * maps use (EventTrigger.ref, NpcPlacement.dialogue_ref). Adding lines is a data
 * edit here, never engine code. Keep the voice cosy and a little melancholy —
 * "lanterns in the dark" — and use canon vocabulary (kin, Lumenary, Gleam,
 * Lantern Gift, vesperlamp), never generic monster/gym/badge.
 */
import type { DialogueLine, DialogueRegistry } from './types';
import { OLDLIGHT_DIALOGUE } from './oldlight';
import { REGION_EXTRA_DIALOGUE } from './regions';

export const DIALOGUE: DialogueRegistry = {
  // --- Georgina's cottage (gloamwood_dell) — ambient cats + a hand-lettered sign ---
  'npc.georgina_waiting': [
    { speaker: 'GEORGINA', portrait: 'georgina', expr: 'sunny', text: "Seen my Pim? [[The darkest corner of the dell]] — she likes a brood. Kettle's on!" },
  ],
  'npc.gloampurr_nook': [
    { text: 'The house Gloampurr glows in her cushion. One gold eye judges you, and shuts.' },
  ],
  'npc.cottage_cat_a': [
    { text: 'A round tabby snores like a tiny kettle. Its blanket: "MITTENS — DO NOT MOVE".' },
  ],
  'npc.cottage_cat_b': [
    { text: 'A soot-black cat holds your eye and pushes a thimble off the shelf. Job done.' },
  ],
  'sign.gloamwood_dell': [
    { text: "GEORGINA'S — mind the cats!\nDarkest dell, brightest welcome. Wipe your boots." },
  ],
  // The blocked east path before the quest starts (warp blocked_ref).
  'sign.lowleaf_gloamwood': [
    { text: 'The brambles east are pitch-dark and thick. Someone lives back there, mind.' },
  ],
  // (R8: no longer posted in Tinderwick — the shore sign came down. Kept as the
  // worked ref in data/world/examples.ts.)
  'sign.tinderwick_dock': [
    { text: 'TINDERWICK DOCKS\nMind the lanterns. The tide comes in quiet now.' },
  ],
  // --- The opening errand (Fenn at the Crossroads waystone) ---
  // Fenn mid-errand: spoken to again before the satchel comes home.
  'npc.fenn_waiting': [
    { speaker: 'FENN', text: '[[The general store]], dear apprentice — my satchel. The keeper will know.' },
    { speaker: 'FENN', text: 'I shall mind the waystone. It is good company, for a stone.' },
  ],
  // Fenn after the ceremony: the waystone send-off, until the story moves him on.
  'npc.fenn_waystone_after': [
    { speaker: 'FENN', text: 'Steady, apprentice. The dark is only the dark — it keeps no grudge.' },
    { speaker: 'FENN', text: '[[Catch a kin]] in the north verge: tire it, [[raise your LAMP]]. Then see Brisa.' },
    { speaker: 'FENN', text: 'Tend your lamp, and it tends you back. I will be along the coast road.' },
  ],
  // The north gate-warden, once the Wayfaring has begun (the pre-starter warning
  // is script.gate_warden; this is the well-wisher swap, stood aside by the verge).
  'npc.gatewarden_after': [
    { speaker: 'GATE-WARDEN', text: 'A lamp and a friend — NOW you look like a Wayfarer. The road north is yours.' },
    { speaker: 'GATE-WARDEN', text: 'The verge grass is restless, but generous. Go find a second friend.' },
    { speaker: 'GATE-WARDEN', text: "Your journey lives in your lamp's memory. [[Press a copy in SETTINGS]] now and then." },
  ],
  // The rival Wren — a fellow young Wayfarer in the plaza (A1). Warm and competitive;
  // Wren's partner is a Glimflit (Light), not one of the starter trio (every Wren team
  // leads with the Glimflit line).
  // R8: Wren mills about Duskapple Orchard now (not the town garden).
  'npc.wren_intro': [
    { speaker: 'WREN', text: "Shh — I'm minding the courier's cart. Mostly by eating the windfalls." },
    { speaker: 'WREN', text: 'You as well? Ha — Fenn sends us all out the same week. Good.' },
    { speaker: 'WREN', text: "Mine's already picked me — a little Glimflit. Trouble enough for anyone." },
    { speaker: 'WREN', text: "Race you to fill the whole map with light. Loser carries the lamp oil." },
  ],

  // --- Tinderwick town signs ---
  // R8: the store moved down the lower-left lane and wears its own board; the
  // old TINDERWICK SQUARE sign by the square is gone.
  'sign.tinderwick_store': [
    { text: 'TINDERWICK GENERAL STORE\nWares and warm lamps within. Mind the step.' },
  ],
  'sign.tinderwick_orchard': [
    { text: '[[WEST: DUSKAPPLE ORCHARD]]\nThrough the hedge gap. Mind the windfalls.' },
    { text: '[[BEYOND: WICKSTEAD]]\nThe lamp-school. New to the road? Start here.' },
  ],
  'sign.tinderwick_lumenary': [
    { text: 'TINDERWICK LUMENARY\nLampwarden Brisa Tallow. Bring a kin.' },
  ],
  'sign.tinderwick_mentor': [
    { text: '[[N]]: the coast road. [[E]]: the Lanternway, to the waystone. W: the orchard.' },
  ],
  'sign.tinderwick_lanternway': [
    { text: '[[EAST: THE LANTERNWAY]]\nEvery lit road meets at the Vesper Crossroads.' },
  ],

  // --- Apprentice's house interior ---
  'sign.house_shelf': [
    { text: 'Spare wicks and an old field-journal. Pages of half-lit constellations.' },
  ],
  // Talking to the coast-keeper directly, and the gated north warps' blocked line.
  'npc.coast_keeper_gate': [
    { speaker: 'COAST-KEEPER', text: 'Not yet, apprentice. [[Light Brisa\'s Beacon]] first, on Tinderwick\'s bluff.' },
  ],
  'npc.house_parent': [
    { speaker: 'GRAN', text: 'Your Wayfaring at last, love — dark valleys, their kin, a sky to relight.' },
    { speaker: 'GRAN', text: 'Fenn waits at [[the Crossroads waystone]] — [[east, the Lanternway]].' },
    { speaker: 'GRAN', text: 'Keep to the lamps, love. And come home warm.' },
  ],
  // G4/F2 — the warm beat before the road: starter chosen, omen not yet fallen.
  // A keepsake and a specific human detail, so `dusk_begins` threatens a FACE.
  'npc.house_parent_warm': [
    { speaker: 'GRAN', text: 'Let me look at you. A lamp, a friend at your heel — HIS apprentice all right.' },
    { speaker: 'GRAN', text: 'Your grandfather trimmed that square\'s lamps forty years, singing to the stubborn wicks.' },
    { text: 'She folds your fingers round his worn brass wick-trimmer, and pats them shut.', style: 'narrate' },
    { speaker: 'GRAN', text: 'Carry it, and sing to the stubborn ones. Now: [[north past the gate]].' },
    { speaker: 'GRAN', text: 'Kin puzzling you? [[The lamp-school at Wickstead]], west past the orchard.' },
  ],
  'npc.house_parent_wait': [
    { speaker: 'GRAN', text: 'Found him? [[The tidal flats]], love, by the buoys. The untidy one watching the sky.' },
  ],
  'npc.house_parent_after': [
    { speaker: 'GRAN', text: '"Some of them are even yours." I read it again and laughed. That man.' },
    { speaker: 'GRAN', text: 'The kettle knows your cup now, love. It\'s never further than this kitchen.' },
  ],

  // --- Tinderwick general store (interior) ---
  'sign.tinderwick_shop_wares': [
    { text: 'TINDERWICK GENERAL STORE\nOil, salve, spare wicks — all a Wayfarer needs.' },
  ],
  // The keeper before the Wayfaring begins — points the player east to Fenn.
  'npc.tinderwick_keeper_early': [
    { speaker: 'SHOPKEEPER', text: 'The Star-tender? Gone [[east along the Lanternway]] to [[the Crossroads waystone]].' },
  ],
  // The keeper during the satchel errand (Fenn has asked). R8: the satchel isn't
  // on the counter any more — the trade-cart courier swept it up with her parcels
  // and threw a wheel in Duskapple Orchard, west of the square. The keeper names
  // the direction AND the landmark (the hedge gap, the cart) so nobody wanders.
  'npc.tinderwick_keeper_errand': [
    { speaker: 'SHOPKEEPER', text: "His satchel? The trade-cart courier swept it up with her parcels at first bell." },
    { speaker: 'SHOPKEEPER', text: "She went [[WEST, through the hedge]] to [[Duskapple Orchard]]. Three-wheeled cart." },
    { speaker: 'SHOPKEEPER', text: "Take it out to him. He'd forget his own lamp if it weren't lit." },
  ],
  // The trading keeper — appears once the kit script has run (flag:tinderwick_kit);
  // their placement ref is script.shop_tinderwick (these lines, then the counter).
  'npc.tinderwick_shopkeeper': [
    { speaker: 'SHOPKEEPER', text: 'A charge brightens your lamp for one throw; a balm mends a weary kin.' },
    { speaker: 'SHOPKEEPER', text: 'The counter is open, dear. Wicks are coin in every town under the dusk.' },
  ],

  // --- Tinderwick Lumenary hall (interior) + the Beacon quest stages ---
  'sign.tinderwick_lumenary_inside': [
    { text: 'THE EMBER LUMENARY\nThe rite is here; the light is [[the BEACON, east bluff]].' },
  ],
  'npc.brisa_tallow': [
    { speaker: 'BRISA TALLOW', text: 'Mind the aisle, dear — step up when your kin is ready, and we\'ll light the sky.' },
  ],
  // Stage 3: the wick-key is home — Brisa heads for the lantern room.
  'npc.brisa_meet_beacon': [
    { speaker: 'BRISA TALLOW', text: 'The wick-key, home at last! Oh, well WALKED, dear.' },
    { speaker: 'BRISA TALLOW', text: '[[The beacon door]], on the east bluff, takes your key now. [[Climb to the lantern]].' },
  ],
  // Stage 4: post-Gleam, back in the hall, festival outside.
  'npc.brisa_after': [
    { speaker: 'BRISA TALLOW', text: 'Hear the square? The fair-bell rang the moment the Ember stood. Go dance.' },
    { speaker: 'BRISA TALLOW', text: 'Next: [[north up the coast road to Pearlmoor]]. Reyl Wash keeps the Tide.' },
  ],
  // --- The Beacon (interiors) ---
  'sign.beacon_door': [
    { text: 'THE OLD BEACON\nWick-locked. Its key walked away up the coast road.' },
  ],
  'sign.beacon_floor_i': [
    { text: 'Stair-litany, floor the first: "A flame is carried, never kept."' },
  ],
  'sign.beacon_floor_ii': [
    { text: 'Stair-litany, floor the second: "The dark is only the dark. Climb."' },
  ],
  'npc.beacon_keeper_a_after': [
    { speaker: 'TANSY', text: 'Up you go. Mind Cole on the next floor — and mind the litany. It helps, truly.' },
  ],
  'npc.beacon_keeper_b_after': [
    { speaker: 'COLE', text: 'The lantern room is just above. Three hundred years that wick waited. Go on.' },
  ],
  // Brisa's "not yet" — the bond-test waits until the player has caught a wild kin
  // (the catch-first soft gate; blocked_ref on the lumenary_battle trigger).
  'npc.brisa_not_ready': [
    { speaker: 'BRISA TALLOW', text: 'Eager, dear — I like that. But a Wayfaring is walked with friends you CHOOSE.' },
    { speaker: 'BRISA TALLOW', text: '[[Catch a wild kin]] in [[the verge by the north gate]]. Then come light the sky.' },
  ],
  // Lantern-fair! Festival NPCs appear in the square once the Ember Gleam is lit
  // (requires_flag 'gleam:ember') — Arc E: a Gleam is belonging, not conquest.
  'npc.fair_piper': [
    { speaker: 'FAIR PIPER', text: 'Hear the square! Brisa rang the fair-bell the moment the Ember stood back up.' },
    { speaker: 'FAIR PIPER', text: 'Your doing? Then the first dance is yours. The Long Dusk can sit this one out.' },
  ],
  'npc.fair_kid': [
    { speaker: 'LANTERN KID', text: 'Look UP! The warm one — Gran says it went dark before I was even born!' },
    { speaker: 'LANTERN KID', text: 'When I get my vesperlamp, I\'ll relight a WHOLE sky. Maybe two.' },
  ],

  // --- Duskapple Orchard (R8) — through the hedge gap west of the square ---
  'sign.duskapple_orchard': [
    { text: "DUSKAPPLE ORCHARD\nDon't shake the trees — they're resting." },
  ],
  // Maudie the trade-cart courier — three flag-disjoint stages on one tile.
  'npc.orchard_courier': [
    { speaker: 'MAUDIE', text: "Don't mind me, love. A courier, her parcels and three wheels. Had four this morning." },
    { speaker: 'MAUDIE', text: "The wheelwright's coming up from the coast. Until then I'm an orchard ornament." },
  ],
  'npc.orchard_courier_errand': [
    { speaker: 'MAUDIE', text: "Fenn's satchel? Oh, STARS — I swept it up! Thought it heavy for candles." },
    { speaker: 'MAUDIE', text: "It's [[on the tailboard]], front of the cart. [[Take it to him]], with my apologies." },
  ],
  'npc.orchard_courier_after': [
    { speaker: 'MAUDIE', text: "Still three wheels. I've named the missing one. It knows what it did." },
  ],
  // Old Wendel, the orchard-keeper. A gentle wink for anyone who remembers the
  // village differently — and a plain pointer at the meadow for a tired Wayfarer.
  'npc.orchard_wendel': [
    { speaker: 'OLD WENDEL', text: "Duskapples. Once they glowed on the bough, and you picked by their light." },
    { speaker: 'OLD WENDEL', text: "Since the stars began going out they ripen dim. Still sweet. Sweet goes last." },
    { speaker: 'OLD WENDEL', text: "Folk say there was never an orchard here. I planted it. Memory grows over things." },
    { speaker: 'OLD WENDEL', text: "Kin need toughening? [[The long grass past the fence]] is full of gentle ones." },
  ],
  'npc.orchard_wendel_dawn': [
    { speaker: 'OLD WENDEL', text: "Look at them! Glowing on the bough again, every one. I knew they'd remember how." },
    { speaker: 'OLD WENDEL', text: "The two in the burn leafed out overnight, and the star's woken. I've stopped asking why." },
    { speaker: 'OLD WENDEL', text: "Take your pick, Wayfarer. Pick by their light." },
  ],

  // --- Dimglass Coast route ---
  'sign.dimglass_buoys': [
    { text: 'DIMGLASS COAST\nThe buoys answer a lit lamp. [[Gullcry Rock]] lies beyond.' },
  ],
  'sign.dimglass_cave': [
    { text: 'A dark mouth in the cliff. Too deep without a lantern that drinks the dark.' },
  ],
  'sign.dimglass_route': [
    { text: 'Keep to the lit lane. Kin nest in the restless grass.' },
  ],
  // An early Hollowing SEED — a weather-worn notice nailed to a coast post. Courteous,
  // sorrowful, unsigned (the name scratched out): the player meets the Hollowing's
  // *voice* long before its face (B2, East). Foreboding only — never explained here.
  'sign.dimglass_pinned_letter': [
    { text: "A notice, rain-warped and nailed to a post. The hand is careful, almost kind:" },
    { text: '"Friends — grieve no more for the lights that fail. The dark is only rest, come early. Let it in."' },
    { text: 'The signature is scratched away. Below, in a shakier hand: "DO NOT LISTEN."' },
  ],
  'sign.dimglass_to_pearlmoor': [
    { text: '[[NORTH: PEARLMOOR QUAY]]\nPast the flats, where lamps stand in the water.' },
  ],
  // R9 — the nameless toy-trader's auction board, beside his toy case on the south sand.
  'sign.wink_auction': [
    { text: "WIND-UPS — TOYS, TALES, TRADES\nLOT 1: ONE (1) WIND-UP FERRYMAN, TIN, WORKING." },
    { text: 'BOUND FOR THE PEARLMOOR TIDE-AUCTION.\nRESERVE: 12,000 WICKS. STORIES CONSIDERED.' },
  ],
  // --- New Pearlmoor <-> Crossroads route: signs + beaten-trainer lines ---
  'sign.wrackline_view': [
    { text: 'WRACKLINE PATH\nHome to [[the crossroads]], by [[the Sounding Cave]].' },
    { text: 'OVER the trestle, round the strand, UNDER it. [[The cave is at the cut\'s head.]]' },
  ],
  'sign.wrackline_cave': [
    { text: 'THE SOUNDING CAVE\nThey say it answers if you call. They say don\'t.' },
  ],
  'sign.sounding_mouth': [
    { text: 'Cut in the rock: "Be lit. The dark in here is only dark — but a lot of it."' },
  ],
  'sign.lanternfall_view': [
    { text: 'LANTERNFALL ROAD\nDown the steps; [[follow the lamps to the crossroads]].' },
    { text: 'The lit drop east is the quick way DOWN. Back up, the ramps zig-zag.' },
  ],
  'sign.lanternfall_hub': [
    { text: '[[VESPER CROSSROADS]] below.\nWhere all the lit roads meet.' },
    // The loop closes HERE for most first-timers: they left the hub southward,
    // walked the whole coast, and arrive back at it from the far side. Name it as
    // the design it is (level-design §2b rule 1) so it reads as a shortcut earned
    // rather than a wrong turn walked.
    { text: 'You have been here before. Every road comes round.\nNot lost: the short way home.' },
  ],
  'npc.wrackline_drifter_after': [
    { speaker: 'DRIFTER OSK', text: 'Go on — the cave\'s waiting. I\'ll be here, drifting. It\'s in the name.' },
  ],
  'npc.lanternfall_warden_after': [
    { speaker: 'LAMP-KEEPER NELL', text: 'Lit and tested. [[The crossroads]] is just down the steps — mind the grass.' },
  ],
  // The coast NPC is the rival Wren again (A2): canon has Wren's first friendly battle here.
  // Until the trainer-battle cutscene is wired, this lands the beat as a clear dialogue tease.
  'npc.dimglass_wayfarer': [
    { speaker: 'WREN', text: "You keep to the lamps, I'll cut through the grass — first to [[Pearlmoor]] wins." },
    { speaker: 'WREN', text: "When you're set, we battle proper. No Lamps, no stakes — just us and our partners." },
    { speaker: 'WREN', text: 'Did you see the sky? A star just... went out. Keep your lamp close out here.' },
  ],

  // --- Dimglass Coast II (the tidal flats) ---
  'sign.flats_gullcry': [
    { text: 'GULLCRY ROCK\nThe shallows past the buoys answer only a Tidecall.' },
  ],
  'sign.flats_cave': [
    { text: 'TIDEGLASS CAVERN\nWithout a Glimmerstep, the dark keeps it.' },
  ],
  'sign.flats_to_quay': [
    { text: '[[NORTH: PEARLMOOR QUAY]]\nSee the lantern-strings on the masts? Nearly there.' },
  ],
  'npc.flats_wayfarer_a': [
    { speaker: 'MORROW', text: 'The dune grass is alive. Good place to toughen a young kin.' },
  ],
  'npc.flats_wayfarer_b': [
    { speaker: 'ELSPETH', text: 'I run letters between Lumenaries. Reyl Wash at Pearlmoor — THERE\'S a battle.' },
  ],
  // C2 — Fenn finds the player after `dusk_begins` and names the Skyweave
  // (walkthrough/01-south: this may land here at the head of II).
  'npc.flats_sky_watcher': [
    { speaker: 'STAR-TENDER FENN', portrait: 'fenn', expr: 'grave', text: 'You saw it go. Hear the old law, child: every star has a kin below carrying its spark.' },
    { speaker: 'STAR-TENDER FENN', portrait: 'fenn', expr: 'grave', text: 'Put that kin to sleep and its star starves, and gutters — sometimes falls. Like Wendel\'s.' },
    { speaker: 'STAR-TENDER FENN', portrait: 'fenn', expr: 'warm', text: 'So we walk the other way. Wake what sleeps. [[Pearlmoor]] keeps the next Gleam.' },
  ],
  // Fenn on the flats once Gran's letter is delivered (S2 closed).
  'npc.flats_sky_watcher_after': [
    { speaker: 'STAR-TENDER FENN', text: 'Did she laugh? ...Good. A laugh in a dark kitchen is worth two relit stars.' },
    { speaker: 'STAR-TENDER FENN', text: 'The next Gleam: [[Reyl Wash, top of Pearlmoor Quay]]. He reads water as I read sky.' },
  ],

  // --- Pearlmoor Quay (town) ---
  'sign.pearlmoor_welcome': [
    { text: 'PEARLMOOR QUAY\nMind the wet boards and the mast-lanterns.' },
  ],
  'sign.pearlmoor_lumenary': [
    { text: 'THE TIDE LUMENARY\nLampwarden Reyl Wash. The door is open to all.' },
  ],
  // R9 — the west-beach waymark to Lightkeeper's Point (the exit is just the beach's
  // far-left edge, easy to miss; this points the way to the Old Light).
  'sign.pearlmoor_point_way': [
    { text: '[[WEST: LIGHTKEEPER\'S POINT]]\nThe Old Light. Follow the beach path to its end.' },
  ],
  'sign.pearlmoor_harbour': [
    { text: 'THE HARBOUR SHALLOWS\nThe moon-water parts only for a Tidecall.' },
  ],
  'sign.pearlmoor_lanternway': [
    { text: '[[W: Lightkeeper\'s Point]].\n[[E: the Crossroads]], by Saltreach Fen.' },
  ],
  'sign.pearlmoor_to_fen': [
    { text: '[[EAST: SALTREACH FEN]]\nIts drowned road bends round the bay, toward home.' },
  ],
  'sign.pearlmoor_shop': [
    { text: 'PEARLMOOR CHANDLERY\nNets, oil, salve and tide-charms.' },
  ],
  // The trading chandler — appears once the crossing-kit has been given;
  // their placement ref is script.shop_pearlmoor (these lines, then the counter).
  'npc.pearlmoor_shopkeeper': [
    { speaker: 'CHANDLER', text: "Bright lamps hold their catch. Reyl's crew runs Tide — come prepared." },
    { speaker: 'CHANDLER', text: 'Counter\'s open — salves, lamps, a few Star-charts off the last cart.' },
  ],
  'npc.reyl_wash': [
    { speaker: 'REYL WASH', text: 'Step up to the sea-altar when your bond is ready. The Tide does not hurry.' },
  ],
  // The bond-test trigger's "not yet" (blocked_ref) — Reyl's voice, until the bell rings.
  'npc.reyl_blocked': [
    { speaker: 'REYL WASH', text: 'The blessing waits on the moor-bell. [[The Old Light]] first, [[west along the beach]] — then the rope, then the bell.' },
  ],
  // Reyl mid-quest: the hook is given, the bell still silent.
  'npc.reyl_waiting': [
    { speaker: 'REYL WASH', text: 'Still quiet out there. [[The Old Light]] first, then [[the netmender]], then the bell.' },
    { speaker: 'REYL WASH', text: 'No hurry. Tides go out so they can come back. The quay\'s listening for that bell.' },
  ],
  // Reyl post-Gleam, back in the hall while the blessing runs outside.
  'npc.reyl_after': [
    { speaker: 'REYL WASH', text: 'Hear them on the water? Sixty voices, none in a hurry. The blessing is yours.' },
    { speaker: 'REYL WASH', text: 'The Tidecall opens [[the islets, the sea-shrine, the fen-road east]], and Gullcry Rock.' },
  ],
  // --- The netmender (quay) — the Causeway Bell's keeper, then S1's giver ----
  'npc.netmender_pre': [
    { speaker: 'NETMENDER', text: 'Mind the coils. Nets to mend, floats gone missing, and a bell-rope to carry.' },
    { speaker: 'NETMENDER', text: 'The moor-gate stays chained till the bell rings. [[See Reyl Wash]], top of the quay. He decides who carries my rope.' },
  ],
  // R9: the floats stage now points UP the Old Light (it shows until
  // flag:q_south_jest_done — so an old save holding the floats climbs too).
  'npc.netmender_floats': [
    { speaker: 'NETMENDER', text: 'Reyl sent you? The rope\'s ready — but my FLOATS went missing, up the Old Light.' },
    { speaker: 'NETMENDER', text: '[[Climb the Old Light]] to the top — [[west along the beach]]. Then the rope is yours.' },
    { speaker: 'NETMENDER', text: '...I\'d like to know what you find up there. I\'ve wondered eleven winters.' },
  ],
  'npc.netmender_sent': [
    { speaker: 'NETMENDER', text: 'The moor-gate\'s open — [[south end of the quay]]. Hang the rope and [[ring it LOUD]].' },
    { speaker: 'NETMENDER', text: 'Give Maren and Cob my regards. By which I mean: beat them politely.' },
  ],
  'npc.netmender_rung': [
    { speaker: 'NETMENDER', text: 'The whole QUAY heard it. My splice, your hands — that bell will swing a century.' },
    { speaker: 'NETMENDER', text: '[[Reyl]] walked into his hall the moment it rang. Go on.' },
  ],
  'npc.netmender_buoys_wait': [
    { speaker: 'NETMENDER', text: 'Quay-outward: [[near, middle, then the last buoy]]. In ORDER, or it\'s a scatter.' },
  ],
  'npc.netmender_done': [
    { speaker: 'NETMENDER', text: 'I count them every night. Near, middle, far. A body does not tire of counting to three.' },
  ],
  // The chained moor-gate (warp blocked_ref) — her voice, before the rope is earned.
  'npc.netmender_gate': [
    { speaker: 'NETMENDER', text: 'Chained. No one walks out to a silent bell without MY rope on their shoulder.' },
    { speaker: 'NETMENDER', text: '[[Reyl Wash]] sends you [[up the Old Light]], west along the beach. Then the rope\'s yours.' },
  ],
  // S1's buoys, refused out of order (trigger blocked_refs on Dimglass II).
  'npc.buoy_dark': [
    { text: 'The buoy rocks on its chain, wick drowned. Not yours to meddle with, unasked.', style: 'narrate' },
  ],
  'npc.buoy_order': [
    { text: 'This wick is sound, but the nearer buoys sit dark. [[Light them quay-outward]].', style: 'narrate' },
  ],
  'npc.pearlmoor_innkeep': [
    { speaker: 'INNKEEP', text: "Rest your feet. The quay's hanging fresh lanterns for the Tide-blessing." },
    { speaker: 'INNKEEP', text: 'They say when Reyl relights the Tide, the shallows answer a lit lamp.' },
  ],
  'npc.pearlmoor_fisher': [
    { speaker: 'FISHER', text: 'Tide-blessing soon! We ask the sea to bring our lights home.' },
    { speaker: 'FISHER', text: 'Reyl\'s Lumenary is [[up the boardwalk]] — the tallest hall, with the moon-lamp.' },
  ],
  // --- The old fisher (quayside inn) — S3's giver, then keeper of the promise --
  'npc.old_fisher_pre': [
    { speaker: 'OLD FISHER', text: 'A dry corner and a warm tin. The sea and I are square these days. Mostly.' },
    { speaker: 'OLD FISHER', text: 'Ring that moor-bell and I might tell you the story the quay thinks I made up.' },
  ],
  'npc.old_fisher_wait': [
    { speaker: 'OLD FISHER', text: '[[Tideglass Cavern]], off the flats. Your lamp can\'t walk it yet — it wants [[the GLIMMERSTEP]].' },
    { speaker: 'OLD FISHER', text: 'No hurry. Just remember an old man\'s stern-lamp.' },
  ],
  'npc.old_fisher_after': [
    { speaker: 'OLD FISHER', text: 'Forty years they smiled at their boots at that story. Now they ask for it. Thank you.' },
  ],
  // Tide-blessing festival NPCs — appear on the quay once 'gleam:tide' is lit.
  'npc.blessing_elder': [
    { speaker: 'QUAY ELDER', text: 'The Tide stands over the water again. Sixty years I waited to sing under it.' },
    { speaker: 'QUAY ELDER', text: 'Tides go out so they can come back. Tonight, child, you brought one back.' },
  ],
  'npc.blessing_kid': [
    { speaker: 'DECKHAND', text: 'The shallows are ANSWERING! Every buoy lights up. The old folk are happy-crying!' },
    { speaker: 'DECKHAND', text: 'They say you can walk the harbour water now. Gullcry Rock — imagine!' },
  ],
  // A third blessing voice by the jetty — the going-out song, named and human.
  'npc.blessing_singer': [
    { speaker: 'BOAT-SINGER', text: '"Tides go out so they can come back—" sing it with me. You\'ve the right.' },
    { speaker: 'BOAT-SINGER', text: 'My mother led this song thirty years, eleven of them dark. I sing it under a LIT sky.' },
  ],
  // --- The breakwater (the Causeway Bell's walk) -------------------------------
  'sign.breakwater_gate': [
    { text: 'THE MOOR-GATE\nBell-business and net-hands only.' },
  ],
  'sign.breakwater_mid': [
    { text: 'Cut in stone: "The sea is patient. Be lit, and be more patient."' },
  ],
  'sign.moorbell_shrine': [
    { text: 'THE MOOR-BELL SHRINE\nRung to open the Tide-blessing.' },
  ],
  'npc.net_hand_a_after': [
    { speaker: 'MAREN', text: 'Weighed and steady, I said. The wind\'s kinder past the elbow lantern. Mostly.' },
  ],
  'npc.net_hand_b_after': [
    { speaker: 'COB', text: 'A week of mending, lost to a bell I could hear from my bunk. Worth it. WORTH IT.' },
  ],

  // --- The Lifting House (S4 "The Booji-Wooji Man") — the quayside gym --------
  'sign.lifting_house_rules': [
    { text: 'HOUSE RULES\n1. Put the stones back.\n2. Spot whoever asks.\n3. If PAUL offers you advice, take it. If he offers you a story, count your pockets after.' },
  ],
  'npc.booji_andy_wait': [
    { speaker: 'ANDY', text: '[[Abdul first, by the bikes]] — he\'s seen where the old man goes. Then [[Sid downstairs]], if you can get three words out of him.' },
    { speaker: 'ANDY', text: 'And if you find Paul — ask him about the Registry. For all of us. Mostly for me.' },
  ],
  'npc.booji_andy_after': [
    { speaker: 'ANDY', text: 'Every dusk he doesn\'t come in, I tell a new lifter about him. Every dusk he DOES, I pretend I never talk about him at all.' },
    { speaker: 'ANDY', text: 'Anyway. As I was saying. The treadmill. The knee. Have I told you about the knee?' },
  ],
  'npc.booji_abdul_pre': [
    { speaker: 'ABDUL', text: 'Stones don\'t lift themselves. ...That\'s it. That\'s the whole wisdom.' },
  ],
  'npc.booji_abdul_after': [
    { speaker: 'ABDUL', text: 'Do I carry my lamp, or does my lamp carry me... Three dusks that\'s kept me up. Tell the old man thanks for nothing.' },
  ],
  'npc.booji_sid_pre': [
    { speaker: 'SID', text: '...' },
    { text: 'He nods at the stones. For Sid, this counts as a conversation.' },
  ],
  'npc.booji_sid_after': [
    { speaker: 'SID', text: '...Did he do the thing where he answers with a question?' },
    { speaker: 'SID', text: '...Yeah. He does the thing.' },
  ],
  'npc.booji_paul_after': [
    { speaker: 'PAUL', text: 'Still here. Still not telling. The cup of something stands as promised — some night.' },
    { speaker: 'PAUL', text: 'Keep the folio somewhere it doesn\'t belong. Things like that go stale on a shelf.' },
  ],
  // Andrew — the OTHER bench guy (two separate lifters; Andy talks, Andrew lifts).
  'npc.booji_andrew': [
    { speaker: 'ANDREW', text: 'Can\'t talk long. Mid-set. The bench waits for no man.' },
    { speaker: 'ANDREW', text: 'Paul spotted me once. Didn\'t say a word the whole set. Best lifting I\'ve ever done. Make of that what you will.' },
  ],
  // Rod — the house's strongest, and its oldest. An allotment-keeper of seventy-two
  // who presses the big harbour-stone clean overhead. Points the player on to Paul
  // (out at the breakwater), and seeds the Chickenpig WITHOUT naming it.
  // Rod's spiel moved to `script.booji_rod` (it now starts the quest). The line
  // below is the dark lamp's "nobody home yet" beat — the breakwater-end trigger's
  // blocked_ref, replacing the engine's generic "not time yet" hint and pointing a
  // lost Wayfarer back to the Lifting House.
  'npc.dark_lamp_cold': [
    { text: 'The dark lamp stands cold at the breakwater\'s end, entirely uninterested in you.', style: 'narrate' },
    { text: 'An old strongman keeps it company — but only for one the Lifting House sends. [[Ask the lifters at the gym]].' },
  ],
  // The Chickenpig at Paul's dark lamp (post-S4 set-piece catch).
  'npc.chickenpig_shy': [
    { text: 'The chicken-pig tucks its head under its wing, asleep. Come back after [[{remaining} more wins]].' },
  ],
  // --- S5 "Not All Who Wander" (Paul's second story) --------------------------
  'npc.wander_note': [
    { text: 'A scrap of sailcloth is tied to the dark lamp. On it, in a big unhurried hand:\nGONE WANDERING. NOT LOST. — P.' },
  ],
  'npc.wander_chickenpig_missing': [
    { speaker: 'PAUL', text: 'Ah — {name}. You found the last word. ...But no bird-pig, or it\'s too tired to stand.' },
    { speaker: 'PAUL', text: '[[Bring it here in your lamp, rested]]. This bit is ITS business. I\'m good at waiting.' },
  ],
  'sign.pearlmoor_allotment': [
    { text: 'HILLSIDE ALLOTMENTS\nPlot 4: R. & A.\nSQUIRRELS WILL BE PROSECUTED.' },
  ],
  'npc.allotment_anth': [
    { speaker: 'ANTH', text: 'One of Rod\'s lot from the Lifting House? Mind the marrows — he talks to them. Only ones that don\'t answer back.' },
    { speaker: 'ANTH', text: 'Seventy-two and he presses harbour-stones. Can lift a mooring-block, can\'t lift a teapot. Mind the squirrels. They bite.' },
  ],
  'npc.allotment_anth_wander': [
    { speaker: 'ANTH', text: 'After the old wood? Paul went up that way not an hour since, whistling. Never been lost a day in his life. He just... goes.' },
    { speaker: 'ANTH', text: '[[The stone at the top]] wants a word. I never could remember the end of it. Rod says it\'s the most important word in the world. Rod also says that about turnips.' },
  ],
  'npc.allotment_anth_done': [
    { speaker: 'ANTH', text: 'Paul came down the hill with a rooster-pig\'s tail-feather in his hat, grinning like a boy. Wouldn\'t say why. Never does.' },
    { speaker: 'ANTH', text: 'Forty years I\'ve known him, and that\'s the first time he came DOWN that hill looking like he\'d found something rather than left it. Ta.' },
  ],
  'npc.wanderwood_hob': [
    { speaker: 'WANDERER HOB', text: 'I am NOT lost. I know exactly where I am: HERE. Everything else keeps moving.' },
    { speaker: 'WANDERER HOB', text: 'These paths go round on themselves. Old Paul says that\'s the point. I say it\'s the THIRD TIME I\'ve passed this tree.' },
  ],
  'npc.wanderwood_hob_done': [
    { speaker: 'WANDERER HOB', text: 'A lamp just lit itself in the middle of the wood. In THIS dark. ...Right. I\'m going home. Which way is home?' },
  ],
  'sign.wander_story_1': [
    { text: 'Carved into the bark, low down, in a child\'s careful hand:\nP. WALKED HERE AGED TEN LOOKING FOR A LOST GOAT. FOUND THE GOAT. KEPT WALKING.' },
  ],
  'sign.wander_story_2': [
    { text: 'Carved deep, years later:\nP. CAME UP HERE WITH A BROKEN HEART AND LEFT IT UNDER THIS TREE. THE TREE SEEMS TO BE DOING ALL RIGHT.' },
  ],
  'sign.wander_story_3': [
    { text: 'Carved in big proud letters:\nP. CARRIED A HARBOUR-STONE TO THE TOP OF THIS HILL FOR A BET WITH HIMSELF. WON. LOST. CALLED IT A DRAW.' },
  ],
  'sign.wander_story_4': [
    { text: 'Carved small, and steady:\nP. SAT HERE THE NIGHT THE DUSK CAME DOWN AND DECIDED NOT TO BE AFRAID OF IT. TOOK A WHILE. WORTH IT.' },
  ],
  'sign.wander_glade_lamp': [
    { text: 'The glade lamp burns a warm, faintly ridiculous morning-gold. Nobody lit it. Somebody crowed at it until it gave in.' },
  ],
  'npc.chickenpig_after': [
    { text: 'Only the dark lamp now, and the old man\'s company. In your lamp, a rooster-pig practises being right about the morning.' },
  ],
  // --- S5: the Far Side (pearlmoor_wanderwood_far) — the wood's optional loop ----
  // All discovery, no gating: things Paul would recognise, in the wood's voice.
  'sign.wander_far_post': [
    { text: 'Driftwood nailed to a trunk, pointing west:\nTHE FAR SIDE. LONGER WAY ROUND. BETTER WAY ROUND. — p.' },
  ],
  'sign.wander_far_laugh': [
    { text: 'Somewhere through the trees, somebody LAUGHS — a great, helpless, unholy bellow, far longer than any joke deserves.' },
    { text: 'It shakes a roost of sleepy kin out of the branches, stops... and starts again, worse. One last snort. Quiet.' },
    { text: 'You have the strong feeling you were meant to hear it.' },
  ],
  'sign.wander_far_bench': [
    { text: 'A fallen column worn into a bench, beside a cairn of hand-polished harbour-stones.' },
    { text: 'Scratched into the bench, in a big unhurried hand:\n80 IN THREE YEARS? — p.' },
    { text: 'Underneath, in a younger, cheekier hand:\nWHY STOP THERE. 140.' },
    { text: 'And under THAT, the big hand, pressed nearly through:\nGOOD. THAT\'S THE NEXT SIXTY-THREE YEARS SORTED. — p.' },
  ],
  'sign.wander_glass_steps': [
    { text: 'THE GLASS STEPS\nThe flat grey ones hold. The round ones roll, and you get wet, and everybody laughs.\n— p. went first.' },
  ],
  'sign.wander_far_reassess': [
    { text: 'Cut into the hollow tree by the brass lamp, in a big unhurried hand:\nIT ANSWERS EVERYTHING. IT IS SURE OF EVERYTHING.\nCHECK EVERYTHING.' },
    { text: 'Below, smaller, like an afterthought that turned out to be the point:\nASK IT AGAIN NEXT YEAR. REASSESS. — p.' },
  ],
  'sign.wander_far_stump': [
    { text: 'A sawn stump, honey-smooth. Pressed into the rings with a hot nail: a neat TRIANGLE and an UMBRELLA, all spokes and trouble.' },
    { text: 'Beside them, in the big hand:\nLANTERN FAIR, THE SUGAR-CUT GAME. THE LAD DREW THE UMBRELLA. I SWAPPED HIM MY TRIANGLE.\nTIP: LICK THE EDGES. — p.' },
  ],
  'sign.wander_story_5': [
    { text: 'Another carved tree, the letters silver with age:\nP. PLAYED THE LANTERN FAIR\'S LONG GAME "FOR HIMSELF." LOST EVERY HAND HE COULD HAVE WON. STOOD IN FRONT OF A STRANGER WHEN THE SHOVING STARTED.' },
    { text: 'SPENT HIS LAST WICK BUYING THE STRANGER A SAFER PLACE IN THE QUEUE. THE STRANGER WON. P. SAID HE\'D HAD HIS TURN — THEIRS WAS JUST STARTING.' },
    { text: 'Squeezed in underneath, much smaller:\n(HE\'LL TELL YOU HE\'S NO ACTOR. HE\'LL BE LYING.)' },
  ],
  'sign.wander_story_6': [
    { text: 'The last carved tree, down a side path, as if it didn\'t want a fuss:\nP. CROSSED TWO SEAS WITH A FRIEND\'S BOOK IN HIS BAG. READ IT IN A SUNNY PORT WHERE NOBODY KNEW HIS NAME. WROTE IN EVERY MARGIN.' },
    { text: 'SENT IT HOME. ALL THE NOTES WERE KIND. THE LONGEST SAID: GOOD — NOW CHECK IT STILL WORKS NEXT YEAR. THE FRIEND ADDED A WHOLE NEW CHAPTER.' },
  ],

  // --- Dimglass Coast: the witness (appears after flag:dusk_begins, B1) -------
  'npc.dimglass_witness': [
    { speaker: 'OLD LAMPLIGHTER', text: 'You stood under it too. One breath it was there — the next, a star-shaped hole.' },
    { speaker: 'OLD LAMPLIGHTER', text: 'Third this season. Towns gone quiet, lamps unlit. Walk careful. And walk LIT.' },
  ],

  // --- Gullcry Rock (Tidecall spur — the backtrack payoff) --------------------
  'sign.gullcry_rock': [
    { text: 'GULLCRY ROCK\nThe sea-birds kept this light alone.' },
  ],

  // --- Glowmoss Deep (East — the first cave dungeon, B2) ----------------------
  'sign.glowmoss_mouth': [
    { text: 'GLOWMOSS DEEP\nWalk soft — and lend the moss your light.' },
  ],
  'sign.glowmoss_grotto': [
    { text: '[[LOWER GALLERIES — ladder down]]\nCount your turns. The deep won\'t.' },
  ],
  'sign.glowmoss_b1f_grotto': [
    { text: '[[SPORE GROTTO, through here.]]\nThe beds answer only a Glimmerstep.' },
  ],
  'npc.glowmoss_keeper_a_after': [
    { speaker: 'DELL', text: 'The nursery beds are the brightest in years... all but the grey chamber.' },
    { speaker: 'DELL', text: 'We don\'t speak of the grey chamber. You\'ll walk through it — keep your lamp CLOSE.' },
  ],
  'npc.glowmoss_keeper_b_after': [
    { speaker: 'MIRREL', text: 'The mine road is [[east, past the gallery moss]]. Old Otho keeps the Stone light.' },
    { speaker: 'MIRREL', text: 'The cowled ones... They were GENTLE. That is the part I cannot sit with.' },
  ],
  // The acolytes at the drained site (pre-restoration; kind, never cruel).
  'npc.glowmoss_acolyte_a': [
    { speaker: 'ACOLYTE', text: 'She is not hurt. She is resting. Does the quiet not look gentle, after the flickering?' },
  ],
  'npc.glowmoss_acolyte_b': [
    { speaker: 'ACOLYTE', text: 'Warden Còr says the dark asks nothing. No more failing, no more grief. We help tired lights lie down.' },
    { speaker: 'ACOLYTE', text: 'You think us unkind. Everyone does, at first.' },
  ],
  'npc.glowmoss_cowled': [
    { text: 'The cowled figure regards you from deep in its hood. It says nothing.', style: 'narrate' },
    { text: 'It bows slightly, as if in apology. There is no unkindness in it. That\'s worse.', style: 'narrate' },
  ],
  // The sleeping luminous kin → the woken one (the flag-pair swap).
  'npc.glowmoss_sleeper': [
    { text: 'The Fennlight lies curled in the dead moss, its glow rising and falling like breath.', style: 'narrate' },
    { text: 'It will not wake.', style: 'narrate' },
  ],
  'npc.glowmoss_woken': [
    { text: 'The Fennlight turns in the air, trailing light like pollen. The moss follows.', style: 'narrate' },
  ],
  // A3 — Wren, shaken, past the drained site. The first crack in the rivalry's
  // brightness; sympathy for the Hollowing voiced, then carried away unsettled.
  'npc.wren_glowmoss': [
    { speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'You woke it up. Good. I think.' },
    { speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'They APOLOGISED. Who apologises while they... do that?' },
    { speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: '...What if they\'re right? Nothing got hurt. It was just quiet.' },
    { speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Forget it. Race you to the mine. ...Not racing. Walk with me?' },
  ],

  // --- Saltreach Fen I (the marsh route) ----------------------------------------
  'npc.fen_warden': [
    { speaker: 'FEN-WARDEN', text: "Mind the planks after dark. The fen's friendly, but it doesn't like to be hurried." },
    { speaker: 'FEN-WARDEN', text: 'The eastern woods have gone quiet. Like a room somebody\'s just left.' },
  ],
  'npc.fen_wader_a_after': [
    { speaker: 'MARIGOLD', text: 'The reeds north run over the causeway — no way round but through.' },
  ],
  'npc.fen_courier_b_after': [
    { speaker: 'OSPREY', text: 'The bank east of the causeway is worth the climb. The hop down saves the walk back!' },
  ],
  'sign.spore_grotto': [
    { text: 'SPORE GROTTO\nWhat grows down here grew before lamps.' },
  ],
  'sign.fen_landing': [
    { text: 'SALTREACH FEN\nPlanks hold the road. [[North to Lowleaf Hollow]].' },
  ],
  'sign.fen_channel': [
    { text: 'DEEP CHANNEL\nPlanks end. The still water answers Tidecall.' },
  ],
  'sign.fen_boundary': [
    { text: 'FEN BOUNDARY\nNo planks beyond: cross by Tidecall or turn back dry.' },
  ],

  // --- Saltreach Fen II (deep channels — Tidecall load-bearing) -----------------
  'sign.fen_ii_landing': [
    { text: 'SALTREACH DEEPS\nTidecall water. [[North by the reed-lights to Lowleaf]].' },
  ],
  'sign.sunkbell_turnoff': [
    { text: '[[EAST, OVER WATER: SUNKBELL]]\nThe drowned shrine. Follow the buoys.' },
  ],
  'sign.fen_ii_treeline': [
    { text: '[[NORTH: LOWLEAF HOLLOW]]\nFollow the green glow and the piping.' },
  ],
  // E1 "The Quiet Reeds" — the fisher's waiting/closing stages.
  'npc.fen_fisher_wait': [
    { speaker: 'FEN FISHER', text: '[[Near reed, mid-water, then the far one]] by the treeline. Home outward.' },
    { speaker: 'FEN FISHER', text: 'Thank you, tide-walker. The fen notices who tends it.' },
  ],
  'npc.fen_fisher_after': [
    { speaker: 'FEN FISHER', text: 'Two of three standing, and the fish coming back. I watch the far dark one, mind.' },
  ],
  // The reeds, refused or revisited (trigger blocked_refs / post states).
  'npc.reed_unasked': [
    { text: 'A dark lantern-reed. Somebody\'s tended light — not yours to touch, unasked.', style: 'narrate' },
  ],
  'npc.reed_order': [
    { text: 'This wick is sound, but the nearer reeds sit dark. [[Light from home outward]].', style: 'narrate' },
  ],
  'npc.reed_lit_a': [
    { text: 'The near lantern-reed burns amber and steady over the black water.', style: 'narrate' },
  ],
  'npc.reed_lit_b': [
    { text: 'The mid-water reed glows warm. Silver shapes circle it like a sigh let out.', style: 'narrate' },
  ],
  'npc.reed_dark_third': [
    { text: 'The far reed stands dark. Your flame would not take, and will not take twice.', style: 'narrate' },
    { text: 'The fen is very quiet here.', style: 'narrate' },
  ],
  'npc.reed_lamplighter_after': [
    { speaker: 'TARN', text: 'Reed-line\'s brightest all season — your doing. [[The treeline\'s just north]].' },
  ],

  'npc.bloom_warden_a_after': [
    { speaker: 'IVY', text: 'Fennlight drift in for the Bloom. To ask one home, a charged lamp asks nicer.' },
  ],
  'npc.bloom_warden_b_after': [
    { speaker: 'FERN', text: 'Sable watched your bout from her doorway. She\'ll deny it to her last breath.' },
  ],
  'npc.cottage_latched': [
    { text: 'Latched, glowmoss through the handle. Everyone\'s outside dancing.', style: 'narrate' },
  ],

  // --- Sunkbell Shallows (the flooded shrine spur) -------------------------------
  'sign.sunkbell_shrine': [
    { text: 'SUNKBELL SHALLOWS\nThey rang the bell till the water reached the rope.' },
  ],
  'sign.sunkbell_bell': [
    { text: 'The verdigris bell hangs silent over its reflection, a second bell ringing nothing.', style: 'narrate' },
    { text: 'Rare kin circle the drowned steps. The niches kept dry what pilgrims left.', style: 'narrate' },
  ],

  // --- Lowleaf Hollow (the Glowmoss Bloom) ---------------------------------------
  'sign.lowleaf_welcome': [
    { text: 'LOWLEAF HOLLOW\nMind the moss — it\'s older than the town.' },
  ],
  'sign.lowleaf_lumenary': [
    { text: 'THE VERDANT LUMENARY\nLampwarden Sable Quill. Knock soft.' },
  ],
  // The pinned letter — the first whisper of Còr's voice (B2 foreshadow; the
  // exact courteous text from the walkthrough; unsigned, never explained here).
  'sign.cor_letter': [
    { text: 'A letter pinned to the notice-board, unsigned, in a careful, courteous hand:' },
    { text: '"To whoever tends these lamps after me: do not grieve the dark. It asks nothing of you, and it never leaves."' },
    { text: 'Nobody will say who pinned it. Someone has drawn a small worried face in the corner.' },
  ],
  'sign.lowleaf_deepwood': [
    { text: '[[NORTH: GLOWMOSS DEEP]]\nTrue dark. Without a Glimmerstep, it keeps itself.' },
  ],
  'sign.lowleaf_lanternway': [
    { text: '[[WEST: THE LANTERNWAY]]\nUnder-Lane, Lantern-car, down to the Crossroads.' },
  ],
  // The Elder Bed (interact states ride the trigger chain; see build_lowleaf).
  'npc.elder_bed_cold': [
    { text: 'The Elder Bed. Up close the grey is worse — moss like burnt paper, its light gone to ash.', style: 'narrate' },
    { text: 'It is not dead. It is waiting, the way a cold hearth waits.', style: 'narrate' },
  ],
  'npc.elder_bed_green': [
    { text: 'The Elder Bed burns green-gold, crowned for the festival. The moss remembers you.', style: 'narrate' },
  ],
  // Festival voices. The fencer line is the B-arc fence (BINDING: nobody in
  // town names the Hollowing as a *presence* — escalation stays monotonic).
  'npc.bloom_fencer': [
    { speaker: 'FESTIVAL AUNTIE', text: 'The Elder Bed? Not the Hollowing, love — a tired bed after a cold spring. Beds have bad years.' },
    { speaker: 'FESTIVAL AUNTIE', text: '...Eat a moss-cake. You\'re too thin to be worrying about moss.' },
  ],
  'npc.bloom_piper': [
    { speaker: 'BLOOM PIPER', text: 'The Bloom wants ROUNDS! Nobody can sulk in six-eight time. That\'s science.' },
    { speaker: 'BLOOM PIPER', text: 'The ring turns round the Elder Bed. Always has. ESPECIALLY this year.' },
  ],
  'npc.bloom_kid_a': [
    { speaker: 'MOSS KID', text: 'I caught a glow-mote! Whisper a wish and the moss keeps it FOR you!' },
    { speaker: 'MOSS KID', text: 'I wished for a Fennlight. Don\'t tell the moss I told you.' },
  ],
  'npc.bloom_kid_b': [
    { speaker: 'FERN KID', text: 'The deep wood\'s RIGHT THERE and nobody lets me LOOK. When I get my lamp I\'ll walk it!' },
    { speaker: 'FERN KID', text: '...Can your lamp already do that? Walk it a LITTLE? I\'ll watch from here.' },
  ],
  // The kindling explainer (the starter kindles ~16–20; canon verb: KINDLE).
  'npc.kindle_elder': [
    { speaker: 'BLOOM ELDER', text: 'Your lead kin\'s banked too bright for its little lamp, dear. A kindling\'s coming.' },
    { speaker: 'BLOOM ELDER', text: '[[When it asks, let it]]. Same light, more of it. It stays who it was — with more room.' },
  ],
  // Wren in town — still BRIGHT (A3, the shaken beat, lands in the Deep).
  'npc.wren_lowleaf': [
    { speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'There you are! Four moss-cakes, and you\'re doing ERRANDS. At a festival!' },
    { speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'The warden here would rather battle than talk. My kind. Race you to the Gleam!' },
  ],
  // The kilner's flag stages around script.kiln_relight.
  'npc.kilner_cold': [
    { speaker: 'KILNER', text: 'A festival with a cold kiln is a song with no drum. Every dry stick\'s gone.' },
    { speaker: 'KILNER', text: '[[Dry fen-wood under the fringe ferns, east of town]]. Fetch it, and I owe you the festival.' },
  ],
  'npc.kilner_after': [
    { speaker: 'KILNER', text: 'Hear her roar? Best burn in nine Blooms. And the old bed took the spore like it was waiting.' },
  ],
  // The stall-keeper's waiting/after stages (E2 rides script.stall_quest/_reward).
  'npc.stall_waiting': [
    { speaker: 'STALL-KEEPER', text: '[[Three bundles, by the glow-beds in the Deep]]! If something\'s sitting on one, be FIRM.' },
  ],
  'npc.stall_after': [
    { speaker: 'STALL-KEEPER', text: 'Sold out twice on your bundles. The Fennlight in the fringe grass, remember.' },
  ],
  // Sable's "not yet" (the bond-test blocked_ref) + her hall stages.
  'npc.sable_not_ready': [
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: 'Oh — not yet. Please. I won\'t test a bond over a grey bed.' },
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: '[[Warm the old moss]] first. [[The kilner]] will know what it needs.' },
  ],
  'npc.sable_waiting': [
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: '[[The kilner, by the square]]. I\'d walk you, but everyone would TALK to me.' },
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'The moss doesn\'t hurry. You needn\'t either.' },
  ],
  'npc.sable_ready': [
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'The bed blooms. The hollow\'s an octave brighter. [[Step up to the moss-dais]].' },
  ],
  'npc.sable_after': [
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'The Verdant stands. My hall-moss won\'t settle about it. Nor will I, quietly.' },
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'Your Glimmerstep opens [[the Spore Grotto]] and [[Tideglass Cavern]]. Dark places keep the best gardens.' },
  ],
  // The provisioner's counter line (script.shop_lowleaf opens the ShopMenu).
  'npc.lowleaf_provisioner': [
    { speaker: 'PROVISIONER', text: 'Balms, charges, and Verdant charts. The deep wood won\'t forgive an empty satchel.' },
    { speaker: 'PROVISIONER', text: 'Festival prices! Same as regular. It\'s the SPIRIT of the thing.' },
  ],
  // The guest-bower (interior): a Bloom guest by the long table.
  'npc.bower_guest': [
    { speaker: 'BLOOM GUEST', text: 'Fen mud to the knee twice a year, happily. Nowhere else does the LIGHT smell green.' },
  ],
  // The mapwide "now accessible" crier (post-Gleam, the §5 callout).
  'npc.bloom_crier': [
    { speaker: 'BLOOM CRIER', text: 'Hear it! The Verdant stands, the Bloom is crowned, the Wayfarer\'s lamp walks the dark!' },
    { speaker: 'BLOOM CRIER', text: 'A Glimmerstep opens [[the deep wood north]], the Spore Grotto, and [[Tideglass Cavern]]!' },
  ],

  // The waystation inn (crossroads_inn interior) — the welcome shingle.
  'sign.crossroads_inn': [
    { text: 'THE WAYSTATION INN\nA warm bed. The kettle is always on.' },
  ],
  // --- Vesper Crossroads (the Lanternway hub) ---------------------------------
  'sign.crossroads': [
    { text: 'VESPER CROSSROADS\nWEST: Tinderwick. NORTH-WEST: [[the bay road to Pearlmoor]]. NORTH: mountain road (shut). EAST: [[the Lantern-car]].' },
  ],
  'sign.crossroads_spire': [
    { text: 'The inward road. Eight cold braziers ring its gate. The mountain waits.' },
  ],
  'npc.lanternway_keeper': [
    { speaker: 'WAYKEEPER', text: 'Every road touches this stone sooner or later. I keep the lamps lit on them.' },
    // The come-round framing, from the one person whose whole job is the roads.
    { speaker: 'WAYKEEPER', text: 'You\'ll walk far out and come back in at a gate you know. Not wrong — the valleys curve.' },
    { speaker: 'WAYKEEPER', text: 'Each Gleam wakes more roads — and more [[Lantern-car lines]], on the east platform.' },
    { speaker: 'WAYKEEPER', text: 'The inward road? Eight Gleams, Wayfarer. Do not hurry the dark.' },
  ],
  // The Lowleaf spoke — sleeping until the Verdant Gleam wakes it (its
  // blocked_ref below), then a lit road east-north to the Bloom.
  // --- The Lanternway lane milestones (one sign per spoke lane map; the
  // bend's marker stone — each names both ends so the turn never disorients).
  'sign.lanternway_tinderwick': [
    { text: 'THE LANTERNWAY\n[[W: Tinderwick]]. [[E: the Crossroads]] and Fenn. No wild kin.' },
  ],
  // --- Opening wayfinding: gentle hints that Fenn is east at the crossroads
  // and the Lanternway is safe, so the walk to the ceremony never confuses or
  // frightens a brand-new player. Both gone once 'flag:has_starter' is set.
  'npc.tinderwick_fenn_hint': [
    { speaker: 'TOWNSWOMAN', text: "Off to find Fenn? He's [[east down the Lanternway]], at [[the Crossroads waystone]]." },
  ],
  'npc.lane_fenn_hint': [
    { speaker: 'WAYFARER', text: '[[The waystone\'s just ahead]]. An old Star-tender\'s pacing there — waiting on you.' },
    { speaker: 'WAYFARER', text: 'Easy lane. The lamps see off anything with teeth.' },
  ],
  'sign.lanternway_pearlmoor': [
    { text: 'LANTERNWAY: PEARLMOOR\n[[W: the Crossroads]]. [[E: the quay]]. Smell the salt?' },
  ],
  'sign.lanternway_lowleaf': [
    { text: 'LANTERNWAY: LOWLEAF\n[[Take the Under-Lane]]; the shelf above runs east.' },
  ],
  'sign.lanternway_undercut': [
    { text: 'THE UNDER-LANE\nThe lane you walked in on runs over your head.' },
  ],
  'sign.lanternway_galehigh': [
    { text: 'LANTERNWAY: GALEHIGH\n[[N: the terraces]]. [[S: the Lantern-car]].' },
  ],
  'sign.lanternway_nightreach': [
    { text: "LANTERNWAY: NIGHTREACH\n[[E: the observatory]]. [[N: the Lantern-car]]." },
  ],
  // The Pearlmoor spoke — sleeping until the Tide Gleam wakes it (the same
  // earned return-compressor as every other town spoke): the first journey to
  // the quay is the coast road, the lane home is the reward for relighting it.
  'npc.waykeeper_pearlmoor_gate': [
    { speaker: 'WAYKEEPER', text: 'The bay road sleeps yet — its lamps answer the Tide, and the Tide is still dark.' },
    { speaker: 'WAYKEEPER', text: 'Take [[the coast road north of Tinderwick]]. Relight the Tide; this road brings you home.' },
  ],

  // The onward roads are shut to a Wayfarer with no kin yet — the opening's
  // soft wall, pointing a brand-new player back to Fenn at the Waystone (the
  // north marsh road gates on flag:has_starter, so this only ever fires pre-kin).
  // The inward (Spire) road's "not yet" — fires until all eight Gleams stand
  // (flag:hub_unlocked). Echoes sign.crossroads_spire so a new player learns it
  // is the endgame road, never the way out of the opening.
  'crossroads.spire_not_yet': [
    { text: 'The inward road runs to the dark mountain. It opens when [[all eight Gleams]] are lit.' },
  ],

  // Swimming the shallows into DEEP water (the darker sea): Tidecall stills the
  // shallows, not the deep. Played once per map visit (WorldScene.onBump).
  'world.too_steep': [
    { text: "Too steep to climb back up. The only way on is down." },
  ],
  'world.too_deep': [
    { text: 'Too deep to swim — the current pulls toward open sea. Back to the shallows.' },
  ],

  // --- Locked-door lines (a gated door warp's blocked_ref) ---
  // Doors are walk-onto: stepping into a locked one (or pressing Confirm at it)
  // plays these instead of barring the way in silence. Keep the canon voice.
  'door.locked_lumenary': [
    { text: "The Lumenary's shut. No Lampwarden lights a hall for a kinless Wayfarer. [[Find a friend first]]." },
  ],
  'door.locked_beacon': [
    { text: 'Locked fast. It wants a wick-key — [[the Dimglass lamplighter]] keeps one.' },
  ],
  'door.locked_glimmerstep': [
    { text: 'The gap breathes cold dark. Without [[the Glimmerstep]], the cave keeps its counsel.' },
  ],

  // ===========================================================================
  // CINDERHEAD MINE — the Stone wall (walkthrough/02-east; Otho Grist, Stone)
  // ===========================================================================
  'sign.cinderhead_welcome': [
    { text: 'CINDERHEAD MINE\nWe lower the lamps to remember why we carry them.' },
  ],
  'sign.cinderhead_deep_mouth': [
    { text: '[[THE DEEP GALLERIES — down this mouth.]]\nNo Glimmerstep, no descent.' },
  ],
  'sign.cinderhead_lumenary': [
    { text: 'STONE LUMENARY — Otho Grist.\nHere, light is not given. It is kept.' },
  ],
  'sign.cinderhead_sealed': [
    { text: 'SEALED — foreman\'s orders.\nBarred from the OTHER side. The bar lifts from there.' },
  ],
  'sign.cinderhead_crystoll': [
    { text: 'CRYSTOLL VAULT\nOnly a Starreach steps a gap like this.' },
  ],
  // the Lamp-down vigil (unconditional — the vigil is underway on arrival)
  'npc.vigil_elder': [
    { speaker: 'VIGIL ELDER', text: 'We lower the lamps to remember why we carry them. Then we light them again.' },
    { speaker: 'VIGIL ELDER', text: "But the vigil can't CLOSE till the old crew's lamp comes up from [[the third gallery]]." },
  ],
  'npc.vigil_miner_a': [
    { speaker: 'MINER', text: "Cowled folk came through, talking gentle about letting the dark just... be. We showed them out." },
    { speaker: 'MINER', text: 'A miner doesn\'t surrender to the dark. A miner KEEPS a light in it. That\'s the whole of us.' },
  ],
  'npc.vigil_miner_b': [
    { speaker: 'MINER', text: "Mind Otho. Fair as a plumb-line, twice as hard. You won't out-hit his kin. Out-LAST them." },
  ],
  // post-Gleam payoff (Arc E: the town answers the win — the lamps are up)
  'npc.vigil_raised_a': [
    { speaker: 'VIGIL ELDER', text: 'Lamps risen, the Stone overhead. The vigil is CLOSED. We won\'t forget the hand that carried it.' },
  ],
  'npc.vigil_raised_b': [
    { speaker: 'PIT-CHILD', text: 'The lamps went UP! All at once, like a sunrise made of lanterns! Did you SEE?' },
  ],
  'npc.cinderhead_deep_warden': [
    { speaker: 'DEEP-WARDEN', text: "The forest Wayfarer — Wren? — went down ahead, quiet. That drained wood shook the bright out of them." },
  ],
  // Otho's giver stages (his hall) — the Descent Vigil loop's grammar
  'npc.otho_waiting': [
    { speaker: 'OTHO GRIST', portrait: 'otho', expr: 'neutral', text: 'The vigil-lamp is [[THREE galleries down]]. [[Bring it up]]. Then we talk.' },
  ],
  'npc.otho_ready': [
    { speaker: 'OTHO GRIST', portrait: 'otho', expr: 'warm', text: 'You carried it up still lit. ...Then we are ready. [[Step to the aisle]].' },
  ],
  'npc.otho_after': [
    { speaker: 'OTHO GRIST', portrait: 'otho', expr: 'warm', text: 'The Stone is yours. [[Galehigh]] waits up the deep and out the far side.' },
  ],
  'npc.otho_not_ready': [
    { speaker: 'OTHO GRIST', portrait: 'otho', expr: 'grave', text: "No vigil-lamp, no bond-test. I must see your lamp cross the dark. [[Down you go.]]" },
  ],
  // E3 The Foreman's Ledger
  'npc.ledger_waiting': [
    { speaker: 'LONE MINER', text: '[[Side gallery off the west chamber]] — that\'s where it fell. Mind; it bites this deep.' },
  ],
  'npc.ledger_after': [
    { speaker: 'LONE MINER', text: 'The whole crew, written down and remembered. You\'ve given an old hand his sleep.' },
  ],
  'npc.cinderhead_sealed_miner': [
    { speaker: 'OLD HOIST-HAND', text: "Meant to clear that door for years. Now the cart-line runs straight to the Crossroads." },
  ],
  'npc.cinderhead_provisioner': [
    { speaker: 'PIT-PROVISIONER', text: 'Balms, charges, a chart or two for the deep. What does the dark owe you today?' },
  ],
  // the two vigil-miner sight trainers, beaten
  'npc.gallery_miner_a_after': [
    { speaker: 'DRUSE', text: 'Lamp\'s two chambers down. Carry it gentle. Hobb\'s on the last neck — he\'ll want a bout.' },
  ],
  'npc.gallery_miner_b_after': [
    { speaker: 'HOBB', text: 'The vigil-lamp\'s just beyond. Lift it slow. A flame that kept this long has earned it.' },
  ],
  'sign.crossroads_mineshortcut': [
    { text: 'CINDERHEAD CART-HOIST\nRuns once the sealed gallery door opens.' },
  ],

  // ===========================================================================
  // THE NORTH — Galehigh Terraces (walkthrough/03-north). Voice: the last warm
  // colour before the cold leg; the Kite-rising is the game's humour-warmest
  // beat (the winch notice is the town's ONE wry sign).
  // ===========================================================================
  'sign.galehigh_welcome': [
    { text: 'GALEHIGH TERRACES\nThe last fire before the climb. Mind the gusts.' },
  ],
  'sign.galehigh_winch': [
    { text: 'THE KITE-RISING WINCH\nRiders ascend at their own joy. Please wave back.' },
  ],
  'sign.galehigh_high_ledges': [
    { text: 'The high terraces open only to a thermal-rider. The wind takes nobody it hasn\'t met.' },
  ],
  'sign.galehigh_windeye': [
    { text: 'THE WIND-EYE\nThe updraft sings on a clear dusk. A sky-kin nests at the eye.' },
    { text: 'Only a kite-rider reaches the eye.' },
  ],
  'sign.galehigh_lanternway': [
    { text: '[[SOUTH: THE LANTERNWAY]]\nTo the Lantern-car and the Crossroads.' },
  ],
  'npc.waystone_kid_kite': [
    { speaker: 'WAYSTONE KID', text: 'LOOK at it go! LAMPS on the tail! Gran says I\'ll light the whole Lanternway. GOOD.' },
    { speaker: 'WAYSTONE KID', text: 'The string hand is everything. A Wayfarer told me. It was you. I\'m telling everyone.' },
  ],
  // The festival, pre-Gleam (warm, communal, a little daft — the build-up).
  'npc.galehigh_festival_piper': [
    { speaker: 'FESTIVAL PIPER', text: 'A reel for the Rising! I play to the kites. The dancers just benefit.' },
    { speaker: 'FESTIVAL PIPER', text: 'Mira\'s up at the launch ledge. She talks about the wind like other folk do a sister.' },
  ],
  'npc.galehigh_festival_kid': [
    { speaker: 'FESTIVAL KID', text: 'NINE lamps on my tail. Talo\'s has six. Not a contest, Gran says. She counted though.' },
  ],
  'npc.galehigh_festival_goer': [
    { speaker: 'FESTIVAL-GOER', text: 'Gran says the stars need a ladder of little lights home. I just like the hill with all of us on it.' },
  ],
  'npc.galehigh_quest_witness': [
    { speaker: 'TERRACE AUNTIE', text: 'Mira shouted the asking down from the ledge? She answers letters off the cliff.' },
    { speaker: 'TERRACE AUNTIE', text: '[[The kite-maker]] next, love — [[lower terrace, the orange silk]]. Her kite blew to bits.' },
  ],
  // Arc A foreshadow — Wren at the festival, bright on top, quieter underneath.
  // (A4 lands at Pale Vault; this only plants the doubt.)
  'npc.wren_galehigh': [
    { speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'This festival is RIDICULOUS. Three kites, a gust-cake, and one new grandmother.' },
    { speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: '...A trader said the Hollowing\'s quiet towns sound peaceful. No more goodbyes. ...Not the worst thing, is it?' },
    { speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Forget I said it. Race you up the Stair — when the wind lets you.' },
  ],
  // The winch-keeper's three stages + the winch warp's "not yet".
  'npc.winch_keeper_wait': [
    { speaker: 'WINCH-KEEPER', text: 'This drum hauls riders up only at the Rising, for a kite the town has flown. Festival law.' },
    { speaker: 'WINCH-KEEPER', text: 'Want up to Mira? [[See the kite-maker]], lower terrace. She needs the errand.' },
  ],
  'npc.winch_not_ready': [
    { speaker: 'WINCH-KEEPER', text: 'Easy! Blessed kites only. [[Kite-maker\'s stall]], then the Rising. THEN the sky.' },
  ],
  'npc.winch_keeper_after': [
    { speaker: 'WINCH-KEEPER', text: 'Up you go, any time. You waved back on the first ride. You\'re in the GOOD ledger.' },
  ],
  // The kite-maker's stages (lost → built → festival → the Round leg).
  'npc.kite_maker_lost': [
    { speaker: 'KITE-MAKER', text: 'My best kite, in three pieces. One squall. ONE. Thirty years of knots, and the sky helped itself.' },
    { speaker: 'KITE-MAKER', text: '[[Search the lower terraces]] for lantern-orange silk. I miss it terribly.' },
  ],
  'npc.kite_maker_after': [
    { speaker: 'KITE-MAKER', text: 'She flies TRUE. [[To the winch terrace]] before the Rising peaks!' },
  ],
  'npc.kite_maker_round_after': [
    { speaker: 'KITE-MAKER', text: 'Tell the waystone kid: the string hand is everything. The kite knows the rest.' },
  ],
  // Mira's town stages (post-Gleam callouts → the N3 ribbon-giver swap).
  'npc.mira_galehigh_after': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'The wind kept you three places: [[the WIND-EYE]], [[THUNDERROOST]], and the drop-ledge home.' },
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'Mind the Storm\'s manners — a numbed kin is a fouled string. Carry balms.' },
  ],
  'npc.mira_ribbon_after': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: '[[The quiet ledge, west of the second stair]]. No note. The wind will mind it.' },
  ],
  'npc.mira_skyloft': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'Don\'t fight the wind. Ask it to lift you, and thank it. [[Step up to the ledge]].' },
  ],
  'npc.mira_skyloft_after': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: '[[Off the ledge and glide LONG]] — that\'s the Updraft Kite. And promise me [[the Wind-Eye]].' },
  ],
  'npc.mira_not_ready': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'neutral', text: 'Not yet — the town flies FIRST. [[Raise a kite with them]] at the Rising.' },
  ],
  // Ambient town + interiors.
  'npc.galehigh_farmer': [
    { speaker: 'TERRACE FARMER', text: 'Everything here grows bent — crops, fences, farmers. The bend SHOWS you the wind.' },
  ],
  'npc.galehigh_gleam_kid': [
    { speaker: 'TERRACE KID', text: 'The STORM one! Right overhead! Gran says the kites showed it the way.' },
  ],
  'npc.galehigh_gleam_farmer': [
    { speaker: 'TERRACE FARMER', text: 'Five constellations up, ours among them. I find I stand a bit straighter.' },
  ],
  'npc.galehigh_hall_keeper': [
    { speaker: 'HALL-KEEPER', text: 'Mira? The Lampwarden isn\'t in her hall, dear — she\'s in the SKY.' },
    { speaker: 'HALL-KEEPER', text: 'The Storm Gleam is met [[up the winch]], and the winch answers the festival. [[Fly a kite]] first.' },
  ],
  'npc.galehigh_hall_festival': [
    { speaker: 'HALL WARDEN', text: 'The Storm stands, and the banners haven\'t hung still since. We wrote the good line tonight.' },
  ],
  'npc.galehigh_inn_guest': [
    { speaker: 'INN GUEST', text: 'I asked for the room out of the wind. She laughed for some time. There is no such room.' },
  ],
  'npc.galehigh_home_elder': [
    { speaker: 'TERRACE ELDER', text: 'I flew my first Rising seventy years gone. The wind is the one thing the dusk never quieted.' },
  ],
  'npc.galehigh_home_kid': [
    { speaker: 'TERRACE KID', text: 'When I\'m big I\'ll ride the winch AND a storm-bird. Da says one impossible thing a year. Da is slow.' },
  ],
  'npc.galehigh_shopkeeper': [
    { speaker: 'KITE-KEEPER', text: 'Storm charts here. Stock balms too: [[Pale Vault keeps no counter]]. Terrible shopping.' },
  ],
  // Sight-trainer after-states.
  'npc.galehigh_kitehand_after': [
    { speaker: 'PERRIN', text: 'The wind still approves of you. The third gust bites, but it means well.' },
  ],
  'npc.galehigh_terracer_after': [
    { speaker: 'SORREL', text: 'The cabbages will forget the bout if I do. My regards to the wind-gap.' },
  ],
  'npc.skyloft_ward_a_after': [
    { speaker: 'TAMSIN', text: 'The ledge is yours. Mind the west rail — the wind uses it as a door.' },
  ],
  'npc.skyloft_ward_b_after': [
    { speaker: 'BRAN', text: 'The wind said yes to you. It doesn\'t say it twice.' },
  ],

  // ===========================================================================
  // THE NORTH — Windward Stair I → II. Quiet transit, Arc D pacing: the warmth
  // handed over to the high blue. The distance-marker is the cluster's one wry
  // line; everything past the wind-gap runs sincere.
  // ===========================================================================
  'sign.windward_marker': [
    { text: 'WINDWARD STAIR\nGalehigh: 412 steps down. Pale Vault: more.' },
    { text: 'The stair-warden counted once, and asks that you not make him do it again.' },
  ],
  'sign.windward_windgap': [
    { text: 'THE WIND-GAP\nOnly a thermal-rider crosses.' },
  ],
  'sign.windward_roost': [
    { text: 'THUNDERROOST\nThe storm-birds keep it. Mind the nest.' },
  ],
  'npc.windward_pilgrim': [
    { speaker: 'PILGRIM', text: 'Every year I walk up for the Aurora-watch. Nobody speaks for an hour. The only crowd I can bear.' },
    { speaker: 'PILGRIM', text: 'I think Pale Vault is where the ground stops insisting.' },
  ],
  // The crag-tender — N1's keeper (post-kettle on Stair I) and the shortcut
  // ledge's rounds (Stair II); one ref serves both placements by design.
  'npc.windward_crag_tender': [
    { speaker: 'CRAG-TENDER', text: 'The kettle\'s always on, child — that\'s the whole ministry. Sip the flask when the cold bites.' },
    { speaker: 'CRAG-TENDER', text: 'If your lamp gutters, [[step off that ledge]] — a short glide home to Galehigh.' },
  ],
  'npc.windward_craghand_after': [
    { speaker: 'EDDA', text: 'Rest at the bends, climb between. The crag-tender\'s kettle is two switchbacks up.' },
  ],
  'npc.windward_galewatch_after': [
    { speaker: 'ROWAN', text: 'The wind-gap\'s ahead — the stair just stops. You\'ve the look of a thermal-rider now.' },
  ],
  'npc.windward_cragwatch_after': [
    { speaker: 'MERLE', text: '[[The glacier\'s down the far slope]]. Walk in quiet. Pale Vault hears everything.' },
  ],

  // ===========================================================================
  // THE NORTH — Pale Vault Glacier + the Undercroft. The lonely aurora; the
  // B3/C3/A4 cluster lands here. ZERO humour past the inn (the one permitted
  // dry line below); the Aurora-watch is a silent vigil.
  // ===========================================================================
  'sign.pale_vault_welcome': [
    { text: 'PALE VAULT GLACIER\nWalk softly; keep your lamp close.' },
  ],
  'sign.pale_vault_undercroft': [
    { text: 'THE UNDERCROFT\nSeven dark brackets. The door answers [[aurora-oil]] alone.' },
  ],
  'sign.pale_vault_pass': [
    { text: '[[WEST: HUSHFROST PASS]]\nOnly a warded flame walks through.' },
  ],
  'sign.pale_vault_deepice': [
    { text: 'THE DEEP ICE\nClosed to any flame that cannot ward itself.' },
  ],
  // Ysolde's stages + the Lamp-Line's blocked lines (all in her voice or the
  // vault's).
  'npc.ysolde_waiting': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'The oil first. [[The tallow-keeper, south camp]], renders it — once her hearth is woken.' },
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'There is no hurry. The brackets can be dark one evening more. Not two.' },
  ],
  'npc.ysolde_door_unlit': [
    { speaker: 'YSOLDE FROST', text: 'The vault answers aurora-oil, not eagerness. [[The tallow-keeper, south camp]].' },
  ],
  'npc.ysolde_vault': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Walk the line slowly. It is the meaning that must not be hurried.' },
  ],
  'npc.ysolde_not_ready': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'Brackets behind you hold their dark. [[Walk back and light them]].' },
  ],
  'npc.ysolde_hall_after': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'warm', text: 'The vault is lit. I keep going down just to look. Do not tell the town.' },
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Your Emberward opens [[the Hushfrost throat, west]], and our [[deep ice]]. Then the Solarium.' },
  ],
  'npc.undercroft_bracket_cold': [
    { text: 'The bracket is cold. A line lights in order — [[nearest the door first]].', style: 'narrate' },
  ],
  'npc.undercroft_ward_a_after': [
    { speaker: 'SELA', text: 'The line remembers every hand that lights it. Walk on, and keep your order.' },
  ],
  'npc.undercroft_ward_b_after': [
    { speaker: 'ORRIN', text: 'Ysolde waits at the heart. She\'s waited years for a flame like yours.' },
  ],
  // The tallow-keeper's stages around script.render_oil.
  'npc.tallow_keeper_doused': [
    { speaker: 'TALLOW-KEEPER', text: 'Nothing\'s on, child. The storm doused my hearth. Now the vault waits on ME.' },
    { speaker: 'TALLOW-KEEPER', text: '[[Storm-felled wood]] would wake it — it drifts up against this camp, just yonder.' },
  ],
  'npc.tallow_keeper_after': [
    { speaker: 'TALLOW-KEEPER', text: 'The pans run pale and bright. [[Seven brackets, in ORDER]]. A promise kept one lamp at a time.' },
  ],
  // B3's quiet cast: the figure before the scene, the witness after.
  'npc.cor_quiet': [
    { text: 'The figure on the shelf does not turn. The cold off the valley below is not weather.', style: 'narrate' },
    { text: 'It waits — courteously, patiently — as if it were you who asked to speak.', style: 'narrate' },
  ],
  'npc.pale_vault_witness': [
    { speaker: 'GLACIER WIDOW', text: 'He buried two of ours the winter the dusk fell, and wept where he thought nobody watched. That is the trouble with Còr. He MEANS it.' },
    { speaker: 'GLACIER WIDOW', text: 'Nobody here joined him. But nobody laughs at the ones who did, either.' },
  ],
  // The Aurora-watch's keepers and watchers.
  'npc.vigil_keeper_after': [
    { speaker: 'VIGIL-KEEPER', text: 'You stood well. The watch is older than the dusk. The standing IS the keeping.' },
  ],
  'npc.aurora_watcher_a': [
    { speaker: 'WATCHER', text: 'We hold our lamps and the sky walks over us. Other towns find it cold. We find them loud.' },
  ],
  'npc.aurora_watcher_b': [
    { speaker: 'WATCHER', text: 'The aurora is the one light the dusk never took. We hold our lamps up so it knows.' },
  ],
  'npc.pale_vault_townsfolk': [
    { speaker: 'GLACIER-DWELLER', text: 'We don\'t shout here. The glacier carries a whisper, and keeps it. The ice is listening.' },
  ],
  'npc.pale_vault_inn_guest': [
    { speaker: 'INN GUEST', text: 'Quietest inn in Vesperholm. The ice creaks once a night. We all look forward to it.' },
  ],
  'npc.pale_vault_home_elder': [
    { speaker: 'GLACIER ELDER', text: 'Lonely? Child, the aurora crosses my window every night. Cold, yes. Alone, never.' },
  ],
  'npc.pale_vault_home_kid': [
    { speaker: 'GLACIER KID', text: 'I can hear the undercroft through the floor. Lately it hums SOMETHING.' },
  ],
  'npc.pale_vault_hall_keeper': [
    { speaker: 'HALL-KEEPER', text: 'Ysolde\'s [[at the undercroft door]], looking at the dark brackets. She\'ll know you\'re coming.' },
  ],
  'npc.pale_vault_hall_festival': [
    { speaker: 'OIL-WARDEN', text: 'The hall smells of aurora-oil again. Ysolde\'s read one ledger page four times.' },
  ],
  'npc.pale_vault_gleam_watcher': [
    { speaker: 'YOUNG WATCHER', text: 'The whole northern crown, over our ice. EVERY lamp on the line lit. Never in my lifetime.' },
  ],
  'npc.pale_vault_gleam_kid': [
    { speaker: 'GLACIER KID', text: 'The undercroft hums a CHORD now. The ice is happy. No one is arguing.' },
  ],
  // N2's giver between viewpoints, and after.
  'npc.sketcher_working': [
    { speaker: 'SKETCHER', text: '[[The crag above the wind-gap, the glacier shore, the festival ice]] — in order. Look long.' },
  ],
  'npc.sketcher_after': [
    { speaker: 'SKETCHER', text: 'Forty years failing that sky. Look up for me in the west — they say it\'s dawn-coloured.' },
  ],

  // ===========================================================================
  // THE WEST (walkthrough/04-west) — Hushfrost, the Solarium, the Sunvault
  // Climb, the Coldfog detour (ZERO humour) and Nightreach. Voice: cold ache →
  // golden bittersweet → drained dread → reverent vastness. Sanctioned wry
  // lines: the W1 marker sign, the three troupe lines, the Nightreach inn
  // guest, and trainer defeats — nothing else.
  // ===========================================================================

  // --- Hushfrost Pass I -------------------------------------------------------
  // The cluster's ONE dry sign (bathos-in-officialdom; everything else sincere).
  'sign.hushfrost_marker': [
    { text: 'HUSHFROST PASS. The quietest road in Vesperholm. The Pass Committee thanks you.' },
  ],
  'sign.hushfrost_coldfog': [
    { text: '[[WEST — THE COLDFOG THROAT.]] Only a warded ember walks through.' },
  ],
  'npc.hushfrost_pass_tender': [
    { speaker: 'PASS-TENDER', text: 'It creeps further every year. Your lamp might hold. [[Warm the throat through]] — the kin past it have gone quiet.' },
  ],
  'npc.hushfrost_lampman_after': [
    { speaker: 'DUNSTAN', text: 'My lamp holds better for watching yours. Don\'t stop to listen to the fog.' },
  ],
  'npc.hushfrost_survivor_after': [
    { speaker: 'HESPER', text: 'You\'ll do. Past the throat the fog THINS, not ENDS. You\'ll come out the gold side.' },
  ],

  // --- Hushfrost Pass II (X1 — grief register, zero humour) -------------------
  // The hook line, VERBATIM from the walkthrough — her waiting stage.
  'npc.numbed_kin_caretaker': [
    { speaker: 'CARETAKER', text: 'It used to glow like a hearth. Now it just sleeps. They tell us that\'s mercy. I light a lamp by it anyway.' },
    { speaker: 'CARETAKER', text: '[[Aurora-oil pools under the ice]], [[in the hollow north]]. Your flame is warded.' },
  ],
  'npc.caretaker_after': [
    { speaker: 'CARETAKER', text: 'She sleeps easier in the light. You can tell, with someone you\'ve sat beside.' },
    { speaker: 'CARETAKER', text: 'I don\'t ask the lamp to wake her. Only to be there if she does. That\'s what it\'s FOR.' },
  ],
  // The numbed Hearthkit (interact reads; the flag:dawn swap is postgame's).
  'npc.numbed_kin_sleeping': [
    { text: 'A Hearthkit lies curled, grey as banked ash, breathing slow and far away. No warmth at all.' },
  ],
  'npc.numbed_kin_awake': [
    { text: 'The Hearthkit sits up, blinking at the daylight, glowing hearth-warm.' },
    { speaker: 'CARETAKER', text: 'She woke with the dawn. She was only waiting for something worth waking FOR.' },
  ],
  'npc.hushfrost_thawtender_after': [
    { speaker: 'TILDA', text: 'Straight on for the gold, Wayfarer. Tell the warm I swept the road for it.' },
  ],
  'sign.hushfrost_aurora': [
    { text: 'AURORA HOLLOW. The lights pool under the ice. A warded flame may look up.' },
  ],
  'sign.hushfrost_gold': [
    { text: '[[WEST — THE SUNKEN SOLARIUM.]] The gold on the fog is stored daylight.' },
  ],

  // --- Sunken Solarium ---------------------------------------------------------
  'sign.solarium_welcome': [
    { text: 'THE SUNKEN SOLARIUM. The sun drowned here. Listen close: it\'s only sleeping.' },
  ],
  'sign.solarium_halls': [
    { text: 'THE FLOODED HALLS. The moon-tide parts for a called tide.' },
  ],
  'sign.solarium_backfold': [
    { text: 'Night-flowers seal this fold. A pocket of daylight would wake them.' },
  ],
  'sign.solarium_climb': [
    { text: '[[WEST — THE SUNVAULT CLIMB.]] The garden-roads rise toward the stars.' },
  ],
  'npc.solarium_brazier_dead': [
    { text: 'The brazier is full of drowned daylight. It wants [[a sunmote, fetched up from the halls]].' },
    { text: 'Lucan Pyre, pacing the stage-edge, has the look of a man with a speech about it.' },
  ],
  'npc.lucan_not_ready': [
    { speaker: 'LUCAN PYRE', text: 'Eager! But nobody tests a bond on a DARK stage. [[Fetch daylight up from the halls]].' },
  ],
  'npc.lucan_waiting': [
    { speaker: 'LUCAN PYRE', text: '[[The phials glint in the flooded halls]]. Spark by spark. The troupe is in costume.' },
  ],
  'npc.lucan_after': [
    { speaker: 'LUCAN PYRE', text: 'My stage lit under seven Gleams. [[Up the Climb]] — the eighth act is Nessa\'s.' },
    { speaker: 'LUCAN PYRE', text: 'When the histories are written, tell them the sun came back THROUGH HERE first.' },
  ],
  'npc.troupe_waiting': [
    { speaker: 'TROUPE PLAYER', text: 'In costume since noon, the stage dark as the flood. We wait BEAUTIFULLY.' },
  ],
  // HUMOUR slot 1 — the stilts (builder-sanctioned copy).
  'npc.troupe_stilts': [
    { speaker: 'STILT-WALKER', text: 'Forty years we\'ve staged "The Sun Returns". One night soon I\'d like the title to stop being the ambitious part.' },
  ],
  'npc.troupe_mask_waiting': [
    { speaker: 'TROUPE PLAYER', text: '[[The side room off the flooded halls]] — the water took my mask.' },
  ],
  // HUMOUR slot 2 — the mask, after (builder-sanctioned copy).
  'npc.troupe_mask_after': [
    { speaker: 'TROUPE PLAYER', text: 'You dredged my face out of a drowned cellar. I\'ve never looked better. That\'s theatre.' },
  ],
  'npc.solarium_witness': [
    { speaker: 'OLD STAGEHAND', text: 'I rigged that stage as a boy. Tonight I watched it light, and sat down on a prop crate.' },
  ],
  // The walkthrough's signature festival-goer line, verbatim.
  'npc.solarium_festival_goer': [
    { speaker: 'FESTIVAL-GOER', text: 'Last warm day of the year, they call it. Been calling it that for as long as the night\'s been long. We just keep spending warm days until one of them sticks.' },
  ],
  'npc.solarium_bread': [
    { speaker: 'BREAD-SHARER', text: 'Warm bread, no charge. Stored daylight in the oven. Eat it warm — that\'s the custom.' },
  ],
  'npc.solarium_kid': [
    { speaker: 'FESTIVAL KID', text: 'Put your hand in the water where the gold shines — it\'s WARM! Everybody\'s done it.' },
  ],
  'npc.solarium_gleam_watcher': [
    { speaker: 'FESTIVAL-GOER', text: 'SEVEN stars. The sun\'s own, over the garden it drowned in. This year\'s paid in advance.' },
  ],
  'npc.solarium_gleam_elder': [
    { speaker: 'FESTIVAL ELDER', text: 'Tonight\'s the first warm day that felt like a down payment, not a goodbye. THAT is a Gleam.' },
  ],
  'npc.troupe_player_a_after': [
    { speaker: 'CALLA', text: 'The understudies talk of nothing else. You\'ve set the company back a WEEK.' },
  ],
  'npc.troupe_player_b_after': [
    { speaker: 'ORSINO', text: 'I\'ve worked your bout into act two. With permission. Or — with enthusiasm, certainly.' },
  ],

  // --- Solarium Lumenary (the green room — the region's rest point) -----------
  // HUMOUR slot 3 — the prompter (builder-sanctioned copy).
  'npc.solarium_prompter': [
    { speaker: 'PROMPTER', text: 'Everyone\'s a critic. The dark heckled us forty years. Tonight it loses its seat.' },
  ],
  'npc.solarium_hall_keeper': [
    { speaker: 'SUN-LEDGER KEEPER', text: 'Every ledger entry ends "and the stage stayed dark." Tonight needs a WIDER page.' },
  ],
  'npc.solarium_hall_festival': [
    { speaker: 'TROUPE PLAYER', text: 'A toast to the apprentice who fetched the sun up spark by spark. You drink FIRST.' },
  ],

  // --- Sunvault Climb ----------------------------------------------------------
  'sign.sunvault_welcome': [
    { text: 'THE SUNVAULT CLIMB. Mind the overgrowth — it minds you back.' },
  ],
  'sign.sunvault_vines': [
    { text: 'The sun-vine bridge died with the night. A pocket of daylight would wake it.' },
  ],
  'npc.sunvault_terracer_after': [
    { speaker: 'BEL', text: 'The beds grow toward the boundary vines. The garden knows what\'s coming.' },
  ],
  'npc.sunvault_wayfarer': [
    { speaker: 'RESTING WAYFARER', text: 'Kindest stretch of road in Vesperholm — gold underfoot, stars ahead. Rest a while.' },
  ],
  // The walkthrough's vine-tender line, verbatim.
  'npc.sunvault_vine_tender': [
    { speaker: 'VINE-TENDER', text: 'Eleven winters shut, and your little pocket of daylight woke them like they\'d only dozed. ...Maybe nothing\'s gone for good. Maybe it\'s all just waiting for the right lamp.' },
  ],
  'npc.sunvault_skywatcher_after': [
    { speaker: 'TAM', text: '[[The dome\'s ahead]], under the densest sky in Vesperholm. Walk in soft.' },
  ],
  'sign.sunvault_helia': [
    { text: 'HELIA VAULT. Sealed by night-flowers. This door kept dry what drowned.' },
  ],
  'sign.sunvault_observatory': [
    { text: '[[NORTH — NIGHTREACH OBSERVATORY.]] Seven lamps for seven stars.' },
  ],

  // --- Helia Vault ---------------------------------------------------------------
  'sign.helia_entry': [
    { text: 'The Helia Vault. What the Solarium couldn\'t keep dry, sealed here — with flowers.' },
  ],
  'npc.helia_far_vine': [
    { text: 'The great vine sleeps beyond your pocket of daylight, across a chasm. Something here must bend the light.' },
  ],

  // --- The Coldfog detour (ZERO humour — every line elegiac) -------------------
  'sign.coldfog_marches': [
    { text: 'COLDFOG MARCHES. The lamps here have been put to sleep. Let them rest.' },
  ],
  'sign.coldfog_boundary': [
    { text: 'Deep coldfog past this stone. Only a warded ember keeps.' },
  ],
  // The hooks' marsh-hermit line, VERBATIM.
  'npc.coldfog_marsh_hermit': [
    { speaker: 'MARSH-HERMIT', text: 'They didn\'t burn it. They didn\'t break it. They just... turned the light down, lantern by lantern, until the whole fen forgot it was ever lit. Kindest thing, they said. Kindest thing.' },
  ],
  // Posted by the Hollowing — courteous, awful.
  'sign.coldfog_works': [
    { text: 'HOLLOWFEN STILLWORKS. Every lamp within is resting. Please do not wake them.' },
  ],
  'sign.coldfog_beacon': [
    { text: '[[WEST — DROWNLIGHT BEACON.]] Drowned in its own keeping. No keeper answers.' },
  ],
  'sign.coldfog_backdoor': [
    { text: '[[NORTH-WEST — NIGHTREACH]], BY THE FOG ROAD. Short, dark, and wrong.' },
  ],
  'npc.coldfog_quiet_camp': [
    { text: 'Two bedrolls, rolled square. The fire-ring swept, a lantern cold where a hand left it. Nobody hurried. That is the worst of it.' },
  ],
  'npc.hollowfen_door': [
    { text: 'No handle. A grey light breathes under the door — a gap for a glimmer-step.' },
  ],
  // The hooks' husk-keeper line, VERBATIM — the sexton among graves.
  'npc.hollowfen_husk_keeper': [
    { speaker: 'HUSK-KEEPER', text: 'Every lamp in here is sleeping, not dead. That\'s the horror of it — and the mercy he believes in. One day the whole sky\'s meant to look like this room.' },
    { speaker: 'HUSK-KEEPER', text: 'I dust the collars. Somebody should. They were LAMPS, once.' },
  ],
  'npc.hollowfen_engine': [
    { text: 'The null-engine: a bell of held dark, polished like a font. Its gauge rests at zero, lovingly kept. A font, not a weapon. That part follows you out.' },
  ],
  'npc.drownlight_door': [
    { text: 'Swollen shut by salt and years. High above, the lamp room keeps its dark.' },
  ],

  // --- Nightreach Observatory ----------------------------------------------------
  'sign.nightreach_welcome': [
    { text: 'NIGHTREACH OBSERVATORY. The sky is closest here. The watchers are counting.' },
  ],
  'sign.nightreach_walk': [
    { text: 'THE ASTRAL WALK. Seven lamps, [[lit in the order the stars came home]].' },
  ],
  'sign.nightreach_fogroad': [
    { text: '[[EAST — THE FOG ROAD.]] Short, dark, and wrong. Only a warded flame holds.' },
  ],
  'sign.nightreach_lanternway': [
    { text: '[[WEST — THE LANTERNWAY.]] Every lit road meets at the Waystone.' },
  ],
  'npc.watch_lamp_unstruck': [
    { text: 'The first watch-lamp waits cold. It wants [[the old watcher\'s striker]], lost on the Sunvault road.' },
  ],
  'npc.watch_lamp_cold': [
    { text: 'This lamp keeps its place in the order. An earlier watch-fire is still dark.' },
  ],
  // C4 — Fenn's placements around lamp 5.
  'npc.fenn_waits': [
    { speaker: 'FENN', text: 'Go on with your lamps, child — I\'ll keep the frost-lamp\'s place. Some things are better lit together.' },
  ],
  'npc.fenn_after': [
    { speaker: 'FENN', text: 'I\'ll watch from here. When the eighth lights... look south a moment? An old man would like to think you knew he saw it.' },
  ],
  // A5 — Wren's placements around lamp 6.
  'npc.wren_waits': [
    { speaker: 'WREN', text: 'I\'m not lighting it without you, so you may as well hurry up with lamp five.' },
  ],
  'npc.wren_nightreach_after': [
    { speaker: 'WREN', text: 'One lamp left, one star left, one of us pretending not to be nervous. [[Nessa\'s at the seventh]] — and I don\'t think her telescope\'s pointed at the sky.' },
  ],
  // B4's threshold — Nessa at the seventh lamp, before the naming.
  'npc.nessa_at_seven': [
    { speaker: 'NESSA COLE', text: 'The seventh lamp is yours to light. And then... something I\'ve watched grow on the mountain. The time for watching it alone is over.' },
  ],
  'npc.junior_watcher_b_after': [
    { speaker: 'OS', text: 'Lira\'s charting the sky as it comes back. Don\'t say I said brilliant. She logs compliments.' },
  ],
  'npc.junior_watcher_working': [
    { speaker: 'LIRA', text: '[[The Sunvault terrace, our roof past the scree]] — and the Coldfog cairn if your nerve runs deep; it\'s optional. Look PROPERLY. I\'ll know if you skimmed.' },
  ],
  'npc.junior_watcher_after': [
    { speaker: 'LIRA', text: 'The chart\'s at the Waystone with my name on it. The senior watchers asked for a COPY. I\'ve written that down twice, in capitals.' },
  ],
  // The Star-vigil's keeper, after the watch is stood.
  'npc.star_vigil_warden_after': [
    { speaker: 'VIGIL WARDEN', text: 'Seven lamps burning, the eighth row waiting. The town has watched half its life for this. We can watch a little longer — that is what watching IS.' },
  ],
  'npc.nightreach_watcher_steps_a': [
    { speaker: 'OLD WATCHER', text: 'I held the Storm-watcher\'s lamp eleven winters before it lit. Was it worth it? Nobody whose lamp is LIT ever asks.' },
  ],
  'npc.nightreach_watcher_steps_b': [
    { speaker: 'WATCH KID', text: 'I\'m the eighth row\'s runner! When the last star comes home I ring the bell down the steps. Practised nine hundred times. It could ALWAYS be tonight.' },
  ],
  'npc.nightreach_festival_a': [
    { speaker: 'WATCHER', text: 'Eight lamps, eight stars. I count them like children home — and they\'re all there.' },
  ],
  'npc.nightreach_festival_b': [
    { speaker: 'WATCHER', text: 'The Crown is closed. Generations kept this vigil and never saw the sky finished. I shall be UNBEARABLE about it. I\'ve earned it.' },
  ],
  // The naming lands on a person (requires flag:great_null_known).
  'npc.nightreach_witness': [
    { speaker: 'TOWNSWOMAN', text: 'Nessa swung the great telescope at the MOUNTAIN. Thirty years, never below the sky. I didn\'t hear what she told you... but I keep standing nearer the lamps.' },
  ],

  // --- Nightreach Lumenary --------------------------------------------------------
  'npc.nessa_not_ready': [
    { speaker: 'NESSA COLE', text: 'Not yet. [[Seven watch-fires, lit in the order]] the stars came home — the eighth is not asked for over dark lamps.' },
    { speaker: 'NESSA COLE', text: 'And if you have not heard me out properly yet — I am right here. Talk to me.' },
  ],
  'npc.nessa_keeping': [
    { speaker: 'NESSA COLE', text: 'The walk is yours. [[Ember-light first, sun-light last.]] I will know each one the moment it takes.' },
  ],
  'npc.nessa_cole': [
    { speaker: 'NESSA COLE', text: 'Seven lamps. You know what I showed you, and you came down the walk steady anyway. Steadiness is most of what the dream-hours respect.' },
    { speaker: 'NESSA COLE', text: '[[Step to the dais]] when ready. The eighth star has waited longest — I would not make it wait politely much longer.' },
  ],
  'npc.nessa_after': [
    { speaker: 'NESSA COLE', text: 'The Crown is whole, and the Penumbra is parting. [[The mountain road north of the Crossroads]] will carry you to the Spire.' },
    { speaker: 'NESSA COLE', text: 'Remember harder than he has forgotten. And after... come back one clear night. Eight constellations from this chair, and we will not say anything at all.' },
  ],
  'npc.nightreach_hall_keeper': [
    { speaker: 'NIGHT-CLERK', text: 'The star-ledger\'s "lost" column has had eleven years of custom. I\'ve ruled a fresh page for tonight, just in case. ...I rule one every night.' },
  ],
  'npc.nightreach_hall_festival': [
    { speaker: 'WATCHER', text: 'The eighth watch-lamp lit ITSELF — no hand near it. The sky kept its own vigil. That story will never need improving.' },
  ],

  // --- Nightreach inn ("The Long Watch") + home ------------------------------------
  // The cluster's ONE permitted dry line (builder-sanctioned copy).
  'npc.nightreach_inn_guest': [
    { speaker: 'TIRED GUEST', text: 'Eight years I\'ve kept the quietest watch in Vesperholm, and the sky saves all its history for the week I booked off. Wake me if the dawn comes in.' },
  ],
  'npc.nightreach_inn_watcher': [
    { speaker: 'OFF-SHIFT WATCHER', text: 'Nothing ever happens at dawn-watch. Used to be a sad joke. Soon it\'ll be a SCHEDULING problem, and I couldn\'t be happier.' },
  ],
  'npc.nightreach_home_elder': [
    { speaker: 'LENS-GRINDER', text: 'I ground the dome\'s first lens — a year of my hands in that glass. Now I hear what it sees and polish my spectacles. It IS the same work.' },
  ],
  'npc.nightreach_home_kid': [
    { speaker: 'WATCHER KID', text: 'My chart\'s under my pillow. Seven stars inked, one space saved. The space is the IMPORTANT part. I said it first.' },
  ],

  // --- The Crossroads' Nightreach spoke (W4's gate pair) + R5's hung chart ---------
  'npc.waykeeper_chart_hung': [
    { speaker: 'WAYKEEPER', text: 'The true sky hangs on the Waystone now. Travellers look UP before they pick a direction. That\'s the Lanternway, working.' },
  ],

  // ===========================================================================
  // CENTRAL / ENDGAME (05-central-endgame). The threshold register holds from
  // the Penumbra inward: sincere, elegiac, ZERO humour — the hub's warmth is
  // the one bright counterweight (and Wren's f1 line is the ONE wry-warm beat).
  // ===========================================================================

  // --- Vesper Crossroads — the endgame hub stages ------------------------------
  'sign.crossroads_spire_open': [
    { text: 'THE INWARD ROAD — OPEN. Eight braziers LIT. [[Beyond: the Penumbra and the Spire]]. Rest first. No bed past this stone.' },
  ],
  'npc.fenn_counsel_after': [
    { speaker: 'FENN', text: 'I am where I mean to be: the centre of every road you walked. Go well. Remember loudly.' },
  ],
  'npc.waystone_kid_trail': [
    { speaker: 'WAYSTONE KID', text: 'Did you see it?! It does the lamps in ORDER, like it\'s TENDING them! [[Follow the flickers round the ring]]!' },
  ],
  'npc.waystone_kid_trail_done': [
    { speaker: 'WAYSTONE KID', text: 'You FOUND it! Lamp-kin used to follow the tenders\' rounds, and now one follows YOU. Best thing ever at this crossroads. I\'m counting.' },
  ],
  'npc.dusk_lamp_quiet': [
    { text: 'A brass-capped dusk-lamp. Its flame burns small and steady, well kept.' },
  ],
  'npc.lampling_shy': [
    { text: 'Whatever warmed this lamp\'s glass is sulking deep in the wick-light. It won\'t show itself till you\'ve [[won {remaining} more battles]].' },
  ],
  'npc.lampling_after': [
    { text: 'The dusk-lamp burns easy. Whatever it hosted found a better lamp — yours.' },
  ],
  'npc.waykeeper_round_done': [
    { speaker: 'WAYKEEPER', text: 'The chart on the stone, the festivals, my old Way-lamp in your satchel. The Round is kept, child. Walk far.' },
  ],

  // --- The Penumbra Ring (the threshold register: awe and held breath) --------
  'sign.penumbra_ascent': [
    { text: 'THE NINTH LANTERN. Starlight or nothing. Lamps out of respect; hearts lit out of spite.' },
  ],
  'sign.penumbra_starwell': [
    { text: '[[EAST — THE STARWELL.]] Where a star fell and never went cold.' },
    { text: 'Nobody knows why. The Hollowing never touched it. Step soft on the dark.' },
  ],
  'npc.penumbra_tended_row': [
    { text: 'Two null-lanterns, swept, holding no light with great care. Someone walks this row.' },
  ],
  'npc.penumbra_snuffed_shrine': [
    { text: 'A wayshrine. Its lamp was put out gently, the way you close a sleeping kin\'s door.' },
  ],

  // --- Starwell (the SILENCE register) -----------------------------------------
  'npc.starwell_still': [
    { text: 'The pool lies flat and shining. It will not give up what sank for [[{remaining} more battles]] yet.' },
  ],
  'npc.starwell_after': [
    { text: 'The well holds only starlight now — gladly. The water is warm.' },
  ],
  // THE NULL-WORKS POOL — Nullmajor #150, the great dark made kin (post-dawn
  // set-piece on umbral_spire_f2; the Còr-mercy register: woken gently, never
  // destroyed). Cooldown + after lines for script.nullworks_nullmajor.
  'npc.nullworks_still': [
    { text: 'The pool of gathered dark is resting. Not for [[{remaining} more battles]].' },
  ],
  'npc.nullworks_after': [
    { text: 'The null-pool is only water now, holding the morning upside down. In your lamp, Còr\'s dark is kept instead of feared.' },
  ],

  // --- The Umbral Spire — Wren at your side (A5→A6), one line per floor.
  // f1's beat (the ONE sanctioned wry-warm one) moved into script.spire_wren_camp,
  // the gatehouse heal anchor; f3 and the summit stay sincere.
  'npc.wren_spire_f2': [
    { speaker: 'WREN', text: 'They tuck them in. Look — they SWEEP in here. Sad, isn\'t it. ...Doesn\'t make them right. Keep climbing.' },
  ],
  'npc.wren_spire_f3': [
    { speaker: 'WREN', text: 'Listen. Wind, this deep in the mountain. The sky is just up there — and it\'s FULL of your lamps.' },
  ],
  'npc.wren_spire_summit': [
    { speaker: 'WREN', text: 'I\'m right here. Whatever he says — and he\'ll say it kindly — you remember louder. Go on.' },
  ],

  // The acolytes, beaten — softer now, still believing (grief doesn't argue).
  'npc.hollowing_acolyte_a_after': [
    { speaker: 'MERRIN', text: 'Thirty years of wicks, and yours made the watching look worth it. ...I still think the dark is kinder. Just less sure it\'s KINDEST.' },
  ],
  'npc.hollowing_acolyte_b_after': [
    { speaker: 'TACE', text: 'We were never cruel — only tired. ...Go gently at the top. He is the tiredest of us.' },
  ],
  'npc.hollowing_acolyte_c_after': [
    { speaker: 'IVORWEN', text: 'Go on up, dear, slowly. ...Four winters. I would have kept a fifth. Fancy me forgetting that, of all things.' },
  ],
  'npc.hollowing_acolyte_d_after': [
    { speaker: 'HARL', text: 'The gallery is yours. ...Eight lamps on eight doorposts, and I never once knocked. If the sky changes, maybe I will.' },
  ],
  'npc.hollowing_acolyte_e_after': [
    { speaker: 'SEFA', text: 'The wind\'s up. She said that meant the sky was paying attention. ...The north roads first, Wayfarer. You promised the beaten half of me.' },
  ],

  // The alcove sleepers (read triggers; the dawn flips them).
  'npc.spire_sleeper': [
    { text: 'A drained kin sleeps under a worked cloth, its light banked to an ember. A cushion under its head. Someone visits.' },
  ],
  'npc.spire_sleeper_awake': [
    { text: 'The alcove is empty, blanket folded. Small bright footprints lead out toward the morning, in no hurry — the way you walk when you know the way home.' },
  ],
  'sign.spire_lantern': [
    { text: 'THE NINTH LANTERN — HIGH GALLERY. The keepers rested here and read the sky before the last stair. The sky is back. Rest. Read it.' },
  ],
  'npc.spire_shaft_dark': [
    { text: 'The open core falls away into dark. The hoist-lamp at the lip is unlit — [[someone above must kindle the line]].' },
  ],
  'npc.dawn_road_waits': [
    { text: 'A cobbled road descends the summit\'s east shoulder into the dark. The keepers called it the dawn road. It is waiting for the name to be true.' },
  ],

  // Còr at the summit — the belt-and-braces interact (the band fires first) and
  // the man after: undone, not destroyed; remembering.
  'npc.cor_summit': [
    { speaker: 'CÒR', text: 'A moment more, apprentice. The sky is very fine tonight — your doing — and I take the fine moments slowly. We have all the dark there is.' },
  ],
  'npc.cor_after': [
    { speaker: 'CÒR', text: 'I keep listing them — the fair, the bell, the kites, the bread. Twenty years of careful forgetting, undone by somebody else\'s lamp. ...Thank you. I am out of practice at saying it to a light.' },
  ],

  // The Keylumen's withdraw line (cooldown 0 — it cannot strand; kept for the
  // op's contract and the one frame where a miss needs answering).
  'npc.keylumen_waits': [
    { text: 'The white-gold light folds back into the dais. Waiting. [[Raise your lamp again]].' },
  ],

  // ===========================================================================
  // THE THREE HOURS (walkthrough/07-the-three) — the legendary triad's sites.
  // Reverent-melancholy register, BINDING: zero humour at the Hours, their
  // verses, or their battles; each chain's one dry line rides its rumour-giver
  // script. The three resting lines are §7 VERBATIM ({remaining} is replaced
  // by the engine with the victories still owed — a cost, never a timer).
  // ===========================================================================

  // --- Site I: Tideglass Cavern (South) — the Dusk Hour below the glass ------
  'sign.tideglass_mouth': [
    { text: 'TIDEGLASS CAVERN. The sea smoothed it; lamp-light finishes it.' },
  ],
  'sign.tideglass_nook': [
    { text: 'Cut in the glass: "THE GLASS REMEMBERS EVERY LIGHT IT IS SHOWN. SHOW IT GOOD ONES."' },
  ],
  // The wreck-lamp before the old fisher's tale is heard (S3's gate).
  'npc.tideglass_wrecklamp_cold': [
    { text: 'A broken boat, her stern-lamp guttered under years of salt. Somebody\'s tended story, and you don\'t know it yet.', style: 'narrate' },
  ],
  'npc.tideglass_wrecklamp_lit': [
    { text: 'The wreck-lamp burns as it burned three days for a drowning man, forty years ago. The debt is paid. The light never counted it.', style: 'narrate' },
  ],
  // The verse plaque's inert twin (before the wreck-lamp burns).
  'sign.tideglass_verse': [
    { text: 'A glass hood over a cold stern-lamp, etched line on line. Unreadable in the dark.' },
  ],
  // The relay's wrong-order/cold line (shared by all three lenses).
  'npc.tideglass_lens_cold': [
    { text: 'A tall lens of sea-glass, cold. Your light slides off it. [[The verse named an order]], and this is not its turn.', style: 'narrate' },
  ],
  // The stair seam, sealed until lens C rings (warp blocked_ref).
  'npc.tideglass_stair_sealed': [
    { text: 'A seam in the glass breathes cold air. It is not open.', style: 'narrate' },
    { text: 'The standing lenses round the pool all seem to lean toward this seam.', style: 'narrate' },
  ],
  // The Dusk Hour's withdrawal (cooldownRef — §7 verbatim).
  'npc.three_dusk_resting': [
    { text: 'The lenses hold your own lamp-light and nothing else. The Dusk Hour has folded itself back into the seam between the days — win {remaining} more battles, and the glass may warm to you again.' },
  ],
  // The netmender, once her rumour is told (consumes flag:three_dusk_rumour).
  'npc.netmender_hours_after': [
    { speaker: 'NETMENDER', text: 'Still singing of an evening, that cliff. You went and listened — you stand like somebody who\'s been NEAR something.' },
  ],

  // --- Site II: the Hourfold (North) — Midnight in the deep ice --------------
  // The sealed fold (host warp blocked_ref — §5 verbatim).
  'npc.hourfold_sealed': [
    { text: 'The fold is shut fast with ice that has opinions about visitors. Something in there is not ready to be looked at.', style: 'narrate' },
    { text: 'Ysolde would know what keeps it.', style: 'narrate' },
  ],
  // The aurora names the snuffing order (§5: east, the water-ice, west).
  'sign.hourfold_aurora': [
    { text: 'Cut into the blue ice: "READ THE SKY BEFORE THE SHELF. The ribbon kneels [[east, then over the water-ice, then west]]."' },
  ],
  // The Unstruck Toll's wrong-order refusal (shared by all three braziers).
  'npc.hourfold_flame_leans': [
    { text: 'The vigil-flame leans from the snuffer — not this one. [[The aurora named an order]].', style: 'narrate' },
  ],
  // The Still Hour's withdrawal (cooldownRef — §7 verbatim).
  'npc.three_midnight_resting': [
    { text: 'The fold is only ice and aurora tonight. Midnight has kept its watch longer than anyone alive; it can outlast you without noticing — {remaining} battles won, and it may consent to be witnessed again.' },
  ],
  // The aurora-watcher, once her rumour is told (consumes flag:three_mid_rumour).
  'npc.aurorawatcher_after': [
    { speaker: 'WATCHER', text: 'Stand a moment before you go down to the fold. That is all the watch asks — that the dark be WITNESSED, not braved.' },
  ],
  // Ysolde, once the snuffer is handed over (consumes flag:three_mid_snuffer).
  'npc.ysolde_snuffer_after': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'You carry the snuffer like a lamp, not a tool. Put the vigil out gently, wanderer. The Still Hour has watched better flames put out.' },
  ],

  // --- Site III: the Unrisen Stair (West) — the Dawn that waited -------------
  // The sealed stair (host warp blocked_ref — §6 verbatim).
  'npc.unrisen_sealed': [
    { text: 'A stair behind the seal, climbing toward nothing the sky currently offers. The basin before it is dry.', style: 'narrate' },
  ],
  // The basin before Lucan's phial is carried (trigger blocked_ref).
  'npc.three_dawn_basin_dry': [
    { text: 'A bone-dry sun-basin, set where a first light was meant to land. It waits for morning, with the patience of masonry.', style: 'narrate' },
  ],
  // The sun-mirror flower before vine A blooms (trigger blocked_ref).
  'npc.unrisen_mirror_waits': [
    { text: 'A bronze-and-glass flower, shut, facing a sunrise that is not there. Nothing you carry is morning enough — yet.', style: 'narrate' },
  ],
  // The far vine's lock, narrated on every early attempt (band blocked_ref).
  'npc.unrisen_far_vine': [
    { text: 'The far sun-vine sleeps across the water. The poured daylight must be [[BENT here]] before the far bank believes in morning.', style: 'narrate' },
  ],
  // The east flight opens (the bloom_b band's ref).
  'npc.unrisen_stair_wakes': [
    { text: 'The bent daylight crosses; the far vine blooms up the east flight like a road remembering itself. At the top, something faces east.', style: 'narrate' },
  ],
  // The Lost Hour's withdrawal (cooldownRef — §7 verbatim).
  'npc.three_dawn_resting': [
    { text: 'The basin stands dry and the stair unrisen. The Hour that has waited years for its morning can wait a little longer than you — {remaining} more battles won, and it may risk believing again.' },
  ],
  // Nessa, once her reading is shared (consumes flag:three_dawn_rumour).
  'npc.nessa_hours_after': [
    { speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'The bell that hasn\'t rung is still there, due south. ...Go gently. It has waited long for a morning.' },
  ],
  // Lucan, once the phial is given (consumes flag:three_dawn_phial).
  'npc.lucan_phial_after': [
    { speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'bittersweet', text: 'Forty years I kept that phial, and the theatre feels LIGHTER without it. Pour it true. First light is an entrance no one makes twice.' },
  ],
  // ===========================================================================
  // DAWNSTEAD — the post-game epilogue town (06-postgame, R2). Bittersweet-
  // warm; Còr never gloated over; the lamp a keepsake now, not a necessity.
  // ===========================================================================
  // Còr's standing lines at his lamp (pre-wick, and after it comes home).
  'npc.cor_lamp': [
    { speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'They offered me a place again. I asked for a lamp instead — one lamp, kept properly, is a whole creed.' },
  ],
  'npc.cor_lamp_after': [
    { speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'The wick draws well. It will hold the first night of the new dark, when it comes. A lamp should have work ahead.' },
  ],
  // Fenn, the survey done — the mentor at rest.
  'npc.fenn_dawnstead_after': [
    { speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'No errands left, apprentice. I checked twice — the second for pleasure. The sky\'s yours now. I only watch how well it\'s kept.' },
  ],
  // Latched doors — everyone\'s out in the sun (no silent doors).
  'door.dawnstead_store': [
    { text: 'Latched lightly. A chalked note on the shutter: "OUT. LOOK UP."' },
  ],
  'door.dawnstead_cottage': [
    { text: 'The hearth cold for the first kind reason in years. Everyone\'s out in the sun.' },
  ],
  'door.dawnstead_home': [
    { text: 'The same stiff latch as home, the same worn step. Nobody\'s in. On a morning like this, why would they be?' },
  ],
  // Signs.
  'sign.dawnstead_town': [
    { text: 'DAWNSTEAD — Tinderwick, by morning light. The lamps are resting. Let them.' },
  ],
  'sign.dawnstead_verge': [
    { text: 'The moths came out gold this morning. Catch one — they won\'t keep; nothing does. That\'s why you catch it.' },
  ],
  // The survey marks before Fenn asks for them (the blocked_ref tease).
  'sign.dawnstead_blooms': [
    { text: 'Dawn-blooms, wide open. Something gold-winged has been feeding here.' },
  ],
  // The first-dawn festival folk (Arc E capstone — belonging, not conquest).
  'npc.dawnstead_piper': [
    { speaker: 'PIPER', text: 'Every festival tune I know leans on the dark somewhere. So I\'m writing a ninth. It keeps coming out in major. I\'ve stopped fighting it.' },
  ],
  'npc.dawnstead_baker': [
    { speaker: 'BAKER', text: 'First batch proved by SUNLIGHT. Tastes the same. Tastes completely different. Both true — have a heel of it.' },
  ],
  'npc.dawnstead_kid': [
    { speaker: 'KID', text: 'Why carry a lamp? The sky does it for free now... oh. OH. Were you the one who—? GRAN! COME AND SEE WHO IT IS!' },
  ],

  // --- The Starfall Vigils (06-postgame · R3) ---------------------------------
  // The Dawnstead witness — points the player to Nightreach when the first
  // shard falls (requires flag:dawn, hidden once flag:starfall_begun).
  'npc.starfall_witness': [
    { speaker: 'WITNESS', text: 'Did you SEE? Not a star going out — one came DOWN, trailing gold, off east.' },
    { speaker: 'WITNESS', text: '[[Nightreach]]\'s beside itself. [[Watcher Oriel]] saw it land. Go and ask her.' },
    { speaker: 'WITNESS', text: 'Last time they fell, they came down cold, and we were frightened. These come down warm. I\'ve decided that\'s the same thing, forgiven.' },
  ],
  // The blocked_ref on every Vigil-site host warp, until its reading is held —
  // the scar of starlight is visible post-dawn, sealed until read (the watchers' voice).
  // (2026-10 audit) the summit dais after the relight, until the five Vigils are kept
  'npc.starfall_round_waiting': [
    { text: 'The Keystar burns steady. Five empty sockets ring the dais — for [[shards of fallen stars]], each kept by someone in the valleys.' },
  ],
  'npc.vigil_scar_sealed': [
    { text: 'A seam of starlight, shut tight. It waits to be read first.' },
    { text: '[[The star-reading at Nightreach]] names these scars, one at a time.' },
  ],
  // The kept placements — each Vigilant's plain line after their vigil is kept
  // (requires flag:vigil_<n>_kept, hidden once flag:starfall_crown swaps in the
  // re-runnable bout). Each points the player on along the chain.
  'npc.vigil_hearthfall_kept': [
    { speaker: 'WICK-MOTHER ESRA', text: 'Off you go, dear — [[the second fell east]], under the hill where the moss has opinions. Seventy years of dusk; I\'ve earned a sunrise.' },
  ],
  'npc.vigil_grovefall_kept': [
    { speaker: 'OLD FOREMAN BRAMM', text: '[[Third one went north]] — the wind\'s spare pocket, the watcher says. Mind the roost. ...And tell Otho he still exaggerates.' },
  ],
  'npc.vigil_stormfall_kept': [
    { speaker: 'ONDRA VAEL', text: '[[The fourth fell west]], where they kept the summer safe. Bow to Dame Solenne.' },
  ],
  'npc.vigil_sunfall_kept': [
    { speaker: 'DAME SOLENNE', text: '[[The last rests in the marshes]], where the water is learning to speak again. Carry my regards to the warden there.' },
  ],
  'npc.vigil_murkfall_kept': [
    { speaker: 'WARDEN MER', text: '[[Carry the five up the mountain]]. The old man has waited long to give his best.' },
  ],
  // Dawnbrael's cooldownRef — the static catch withdrew with the next dark; it
  // returns with the next sunrise (no re-fighting the Round). cooldownBattles is
  // 0, so {remaining} never reads — the line is the re-approach hint only.
  'npc.dawnbrael_resting': [
    { text: 'The Ninth Lantern stands quiet, the five shards seated. Dawnbrael drew back into the morning — [[raise the lamp again]].' },
  ],
  // Oriel's terrace re-reads — the chain's noticeboard. Lost the thread? She
  // repeats the current reading, verbatim, slightly wearily. Flag-disjoint
  // placements (the Fenn-waystone pattern) carry exactly the held reading.
  'npc.oriel_read_1': [
    { speaker: 'WATCHER ORIEL', text: '...The first again? Very well. [[The first came down in the south]] — where the first lamp learned its name. Climb past the lantern that taught the sky to answer; it fell on the bluff above, where even the gulls go quiet.' },
  ],
  'npc.oriel_read_2': [
    { speaker: 'WATCHER ORIEL', text: '[[The second went to earth in the east]] — under the hill, where the wood keeps its own weather and the moss has opinions. Bring a light. Bring patience.' },
  ],
  'npc.oriel_read_3': [
    { speaker: 'WATCHER ORIEL', text: '[[The third went north]], into the wind\'s spare pocket — the roost where storms go off duty. Take the kite. Take a coat.' },
  ],
  'npc.oriel_read_4': [
    { speaker: 'WATCHER ORIEL', text: '[[The fourth fell where summer was put away]] for safekeeping — the high terraces that remembered daylight before the rest of us believed in it again.' },
  ],
  'npc.oriel_read_5': [
    { speaker: 'WATCHER ORIEL', text: '[[The last fell where the water forgot how to speak]]. It is learning again — go gently into the murk. One there has waited a long time to greet you.' },
  ],
  'npc.oriel_carry': [
    { speaker: 'WATCHER ORIEL', text: 'Five shards, five vigils kept. The sixth never fell — it waits where the night ended. [[Carry the five up the mountain]] and ask the old man what he sees.' },
  ],
  'npc.oriel_epilogue': [
    { speaker: 'WATCHER ORIEL', text: 'Star-tender, is it now. I read the falls; you kept them. Not a bad night\'s watching.' },
  ],
  // The three Vigilants who climbed ahead, waiting at the Ninth Lantern before
  // the Round (requires flag:vigil_5_kept, hidden once flag:starfall_lesson).
  'npc.vigil_ondra_summit': [
    { speaker: 'ONDRA VAEL', text: 'We came to watch the old man\'s lesson; the watching turned into a queue. [[Raise the lamp at the lantern]] when ready — it\'s cold up here.' },
  ],
  'npc.vigil_solenne_summit': [
    { speaker: 'DAME SOLENNE', text: 'The finest house I ever played. Three of us, then the old man — no interval. [[Touch the lantern]] and the curtain rises.' },
  ],
  'npc.vigil_mer_summit': [
    { speaker: 'WARDEN MER', text: 'Forty years he\'s waited for this lesson. So have I. [[Ask the lantern]] when steady.' },
  ],
  // ---------------------------------------------------------------------------
  // The easter-egg breadcrumb trail.
  //
  // The egg itself is S4 "The Booji-Wooji Man" — the Lifting House at the TOP of
  // Pearlmoor Quay, and Paul at the dark lamp out past the breakwater's end.
  // These lines are the trail to it: Andrew names the thing back in Tinderwick,
  // two walkers on the coast road repeat it as gossip, and the Waykeeper's
  // road-teller at the Crossroads finally points at the building. Nobody ever
  // says what it IS — the joke only lands if the player goes and finds out.
  // ---------------------------------------------------------------------------
  'npc.egg_hint_coast': [
    { speaker: 'WALKER', text: 'Heading north? Keep your lamp up — and your eyes open besides.' },
    { speaker: 'WALKER', text: 'There\'s an easter egg hidden in Vesperholm. Never found it. My cousin swears she has, but she also swears she once out-argued a Lampwarden.' },
  ],
  'npc.egg_hint_flats': [
    { speaker: 'NET-MENDER', text: 'You\'ve the look of someone hunting for something that isn\'t on the road.' },
    { speaker: 'NET-MENDER', text: 'The easter egg? In the quay town up the coast — NOT at the water\'s edge. Look uphill.' },
  ],
  'npc.egg_hint_crossroads': [
    { speaker: 'ROAD-TELLER', text: 'Every road in the valley walks past this waystone and tells you something.' },
    { speaker: 'ROAD-TELLER', text: 'Lately: the easter egg\'s in Pearlmoor Quay, in the building at the very TOP. Not the hall, not the inn — the one with the noise coming out of it.' },
    { speaker: 'ROAD-TELLER', text: 'Ask inside for the old man. That\'s all anyone will say, and they say it like they\'re enjoying themselves.' },
  ],

  // ===========================================================================
  // THE PERIL THREAD (R9) — static lines for the thread's signs + the bookend.
  // Staged scripts live in scripts.ts (same banner); design in
  // docs/world/walkthrough/08-the-peril-thread.md.
  // ===========================================================================
  // N1 — the Hollowing's notice on Galehigh's plaza. Grief dressed as mercy:
  // courteous, unsigned, never a threat.
  'sign.peril_quiet_notice': [
    { text: 'A neat notice:\nTO ANY WHO ARE TIRED. The dark does not take. It only keeps.' },
    { text: 'Nothing you love need ever fade again. When you are ready to rest, the Quiet will be waiting. No one will be cross with you.' },
  ],
  // S3 (deferred placement — Pearlmoor Quay harbour board; see the doc).
  'sign.peril_pearlmoor_board': [
    { text: 'HARBOUR NOTICE\nThe north shore\'s tide-lamps have gone dark.' },
    { text: 'Boats are asked not to put in after dusk. The villagers are well. And very quiet.' },
  ],
  // P1 — the bookend: Maudie in Dawnstead, sending the player home to look.
  'npc.peril_maudie_dawn': [
    { speaker: 'MAUDIE', text: "Parcel run: duskapple whips from old Wendel. Four wheels on the cart. I counted." },
    { speaker: 'MAUDIE', text: "His crater's flowered, love, and the star in it's woken bright. [[Worth the walk home]], if you've not been." },
  ],
  // R9 "The Old Light" — Lightkeeper's Point + the joke-tower (content/oldlight.ts).
  ...OLDLIGHT_DIALOGUE,
  ...REGION_EXTRA_DIALOGUE,
};

const FALLBACK: DialogueLine[] = [{ text: '...' }];

/** Resolve a dialogue ref to its pages, or a quiet fallback if unknown. */
export function getDialogue(ref: string | undefined): DialogueLine[] {
  if (!ref) return FALLBACK;
  return DIALOGUE[ref] ?? FALLBACK;
}
