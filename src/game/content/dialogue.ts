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
    { speaker: 'FENN', text: 'Catch a kin in the verge grass by the north gate — tire it in battle, then raise your LAMP. Brisa will want to meet that new friend; her Lumenary is the tall hall up the square.' },
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
    { text: 'TINDERWICK LUMENARY — the town\'s lantern-hall.\nLampwarden Brisa Tallow tends the Ember light. Bring a kin and a steady hand.' },
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
    { speaker: 'GRAN', text: 'Off on your Wayfaring at last — away to walk the dark valleys, befriend their kin, and relight the sky, the way every lamp-tender\'s apprentice must.' },
    { speaker: 'GRAN', text: 'Old Fenn left word — the Star-tender, love, who minds what is left of the stars. He waits at the Crossroads waystone, east along the Lanternway. That is the lit road out of town.' },
    { speaker: 'GRAN', text: 'Keep to the lamps, love. And come home warm.' },
  ],
  // G4/F2 — the warm beat before the road: starter chosen, omen not yet fallen.
  // A keepsake and a specific human detail, so `dusk_begins` threatens a FACE.
  'npc.house_parent_warm': [
    { speaker: 'GRAN', text: 'Let me look at you. A lamp on your belt and a friend at your heel — oh, you are HIS apprentice all right.' },
    { speaker: 'GRAN', text: 'Your grandfather trimmed every lamp on that square for forty years. Out at first bell, rain or starfall, that old brass trimmer in his coat — and he\'d sing to the stubborn wicks. Swore they burned longer for it.' },
    { text: 'She takes the worn brass wick-trimmer down from the shelf, folds your fingers around it, and pats them shut.', style: 'narrate' },
    { speaker: 'GRAN', text: 'He\'d have walked you to the gate, love. Since he can\'t — carry his trimmer, and sing to the stubborn ones. Now: north past the gate, and home before the bread\'s stale.' },
  ],
  'npc.house_parent_wait': [
    { speaker: 'GRAN', text: 'Found him yet? The tidal flats, love — up past the coast road, where the buoys are. He\'ll be the untidy one watching the sky.' },
  ],
  'npc.house_parent_after': [
    { speaker: 'GRAN', text: 'I read his answer again last night and laughed all over. "Some of them are even yours" — honestly, that man.' },
    { speaker: 'GRAN', text: 'The kettle knows your cup now, love. However far the Wayfaring runs, it\'s never further than this kitchen.' },
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
    { speaker: 'SHOPKEEPER', text: 'How is the kit holding up? A charge brightens your lamp for one throw; the balm mends a weary kin. Use them well.' },
    { speaker: 'SHOPKEEPER', text: 'And the counter is open, dear. Wicks — those waxed lamp-wicks in your purse — are coin in every town under the dusk. Have a look.' },
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
  // Fenn on the flats once Gran's letter is delivered (S2 closed).
  'npc.flats_sky_watcher_after': [
    { speaker: 'STAR-TENDER FENN', text: 'Did she laugh? At the letter? ...Good. A laugh in a dark kitchen is worth two relit stars, and you may tell the sky I said so.' },
    { speaker: 'STAR-TENDER FENN', text: 'Pearlmoor keeps the second Gleam, child — the old ferryman reads water the way I read sky. Mind the bell.' },
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
  // The bond-test trigger's "not yet" (blocked_ref) — Reyl's voice, until the bell rings.
  'npc.reyl_blocked': [
    { speaker: 'REYL WASH', text: 'Easy, Wayfarer. The blessing waits on the moor-bell, and the moor-bell waits on you. Come speak with me first — the sea keeps her orders.' },
  ],
  // Reyl mid-quest: the hook is given, the bell still silent.
  'npc.reyl_waiting': [
    { speaker: 'REYL WASH', text: 'Still quiet out there. The netmender keeps the rope; her floats went south down the flats — ground you have already walked, if your boots remember.' },
    { speaker: 'REYL WASH', text: 'No hurry, mind. Tides go out so they can come back. But the blessing-boats are at their moorings, and the whole quay is listening for that bell.' },
  ],
  // Reyl post-Gleam, back in the hall while the blessing runs outside.
  'npc.reyl_after': [
    { speaker: 'REYL WASH', text: 'Hear them out on the water? Sixty voices and not one in a hurry. That is the Tide-blessing, and it is yours as much as theirs tonight.' },
    { speaker: 'REYL WASH', text: 'When the song lets you go: the Tidecall opens the islets, the sea-shrine, and the fen-road east. And Gullcry Rock, back down the flats — the buoys always did know the way.' },
  ],
  // --- The netmender (quay) — the Causeway Bell's keeper, then S1's giver ----
  'npc.netmender_pre': [
    { speaker: 'NETMENDER', text: 'Mind the coils, Wayfarer. Nets to mend, floats gone south, and a bell-rope nobody\'s fit to carry. The sea took a whole storm out of MY year, I tell you.' },
  ],
  'npc.netmender_floats': [
    { speaker: 'NETMENDER', text: 'Reyl sent you for the rope? Hmph. The rope is spliced and waiting — it is my FLOATS the sea owes me first.' },
    { speaker: 'NETMENDER', text: 'The storm carried them south down the tidal flats — cork floats, a whole string, stamped with my mark. Bring them home and the rope is yours, and gladly.' },
  ],
  'npc.netmender_sent': [
    { speaker: 'NETMENDER', text: 'The moor-gate\'s unchained — south end of the quay, where the boards run out. Hang the rope true and ring it LOUD, Wayfarer.' },
    { speaker: 'NETMENDER', text: 'And give Maren and Cob my regards. By which I mean: beat them politely.' },
  ],
  'npc.netmender_rung': [
    { speaker: 'NETMENDER', text: 'I heard it. The whole QUAY heard it. My splice, your hands — that bell will swing a hundred years on that rope.' },
    { speaker: 'NETMENDER', text: 'Reyl walked into his hall the moment it rang. Go on — the blessing waits on nobody now.' },
  ],
  'npc.netmender_buoys_wait': [
    { speaker: 'NETMENDER', text: 'Quay-outward, remember: the near one, the middle water, then the last buoy out. A line lights in ORDER or it isn\'t a line, it\'s a scatter.' },
  ],
  'npc.netmender_done': [
    { speaker: 'NETMENDER', text: 'Every night I count them now. Near, middle, far — all standing. You\'d think a body would tire of counting to three. A body does not.' },
  ],
  // The chained moor-gate (warp blocked_ref) — her voice, before the rope is earned.
  'npc.netmender_gate': [
    { speaker: 'NETMENDER', text: 'The moor-gate stays chained, Wayfarer — those boards have eaten bolder boots than yours. No one walks out to a silent bell without MY rope on their shoulder.' },
  ],
  // S1's buoys, refused out of order (trigger blocked_refs on Dimglass II).
  'npc.buoy_dark': [
    { text: 'The buoy rocks on its chain, wick drowned and dark. It is somebody\'s tended light — not yours to meddle with, unasked.', style: 'narrate' },
  ],
  'npc.buoy_order': [
    { text: 'This buoy\'s wick is sound but its line-mates nearer the quay still sit dark. A line lights in order, quay-outward — the netmender was firm on it.', style: 'narrate' },
  ],
  'npc.pearlmoor_innkeep': [
    { speaker: 'INNKEEP', text: "Rest your feet, Wayfarer. The Tide-blessing's near — the whole quay hangs fresh lanterns for it." },
    { speaker: 'INNKEEP', text: 'They say when Reyl relights the Tide, the harbour shallows answer a lit lamp. Old ferryman magic. The moon listens to him.' },
  ],
  'npc.pearlmoor_fisher': [
    { speaker: 'FISHER', text: 'Tide-blessing tonight! We string the buoys, sing the old going-out song, and ask the sea to bring our lights home.' },
    { speaker: 'FISHER', text: 'Reyl tends the Lumenary up the boardwalk — tallest hall on the quay, you cannot miss its moon-lamp.' },
  ],
  // --- The old fisher (quayside inn) — S3's giver, then keeper of the promise --
  'npc.old_fisher_pre': [
    { speaker: 'OLD FISHER', text: 'A dry corner and a warm tin — all an old boat-hand asks. The sea and I are square these days. Mostly square.' },
    { speaker: 'OLD FISHER', text: 'Ring that moor-bell back to life and maybe I\'ll tell you the story the quay thinks I made up.' },
  ],
  'npc.old_fisher_wait': [
    { speaker: 'OLD FISHER', text: 'Tideglass Cavern, off the flats — the dark cliff-mouth. No lamp of mine ever walked that dark, and yours can\'t yet either. East-country craft, the deep-walking. The GLIMMERSTEP, they call it.' },
    { speaker: 'OLD FISHER', text: 'No hurry, Wayfarer. That lamp has kept its own counsel forty years. But when your light learns to walk the dark — remember an old man\'s stern-lamp.' },
  ],
  'npc.old_fisher_after': [
    { speaker: 'OLD FISHER', text: 'Forty years I told that story to folk who smiled at their boots. Now look at them — they ask ME to tell it. You gave an old man his true back.' },
  ],
  // Tide-blessing festival NPCs — appear on the quay once 'gleam:tide' is lit.
  'npc.blessing_elder': [
    { speaker: 'QUAY ELDER', text: 'The Tide stands up over the water again. Sixty years I waited to see the going-out song sung under it.' },
    { speaker: 'QUAY ELDER', text: 'Tides go out so they can come back. Reyl always says it. Tonight, child, you brought one back.' },
  ],
  'npc.blessing_kid': [
    { speaker: 'DECKHAND', text: 'The shallows are ANSWERING! Watch — every buoy lights when the moon-water moves. The old folk are crying. Happy crying!' },
    { speaker: 'DECKHAND', text: 'They say the Wayfarer who relit it can walk the harbour water now. Gullcry Rock, the sea-shrine, all of it. Imagine!' },
  ],
  // A third blessing voice by the jetty — the going-out song, named and human.
  'npc.blessing_singer': [
    { speaker: 'BOAT-SINGER', text: '"Tides go out so they can come back—" sing it with me, Wayfarer, you of all people have the right tonight.' },
    { speaker: 'BOAT-SINGER', text: 'My mother led the going-out song from that bow for thirty years, under a dark sky. Tonight I get to sing it under a LIT one. That is your doing.' },
  ],
  // --- The breakwater (the Causeway Bell's walk) -------------------------------
  'sign.breakwater_gate': [
    { text: 'THE MOOR-GATE\nBreakwater boards beyond — bell-business and net-hands only. The moor-bell hangs silent at the far end, wanting a rope.' },
  ],
  'sign.breakwater_mid': [
    { text: 'Causeway litany, cut into the stone: "The sea is patient. Be lit, and be more patient."' },
  ],
  'sign.moorbell_shrine': [
    { text: 'THE MOOR-BELL SHRINE\nRung to open the Tide-blessing since Pearlmoor first strung a lantern. The sea hears it. So does the sky.' },
  ],
  'npc.net_hand_a_after': [
    { speaker: 'MAREN', text: 'Weighed and steady — I said it and I hold to it. The wind\'s kinder past the elbow lantern. Mostly.' },
  ],
  'npc.net_hand_b_after': [
    { speaker: 'COB', text: 'A week of mending, lost to a bell I could hear from my own bunk. Worth it. WORTH IT.' },
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

  // --- Glowmoss Deep (East — the first cave dungeon, B2) ----------------------
  'sign.glowmoss_mouth': [
    { text: 'GLOWMOSS DEEP\nThe moss keeps a little light where it can. Walk soft, Wayfarer — and lend yours back.' },
  ],
  'sign.glowmoss_grotto': [
    { text: 'LOWER GALLERIES — ladder down.\nThe dark below keeps the old beds. Count your turns, Wayfarer — the deep does not.' },
  ],
  'sign.glowmoss_b1f_grotto': [
    { text: 'SPORE GROTTO — through this notch.\nThe spore-beds answer no lamp but a Glimmerstep. Mind where the shrooms lean.' },
  ],
  'npc.glowmoss_keeper_a_after': [
    { speaker: 'DELL', text: 'The nursery beds are brightest they have been in years... all but the grey chamber.' },
    { speaker: 'DELL', text: 'We do not speak of the grey chamber. But you are going to walk through it, so — keep your lamp CLOSE.' },
  ],
  'npc.glowmoss_keeper_b_after': [
    { speaker: 'MIRREL', text: 'The mine road is east, past the gallery moss. Old Otho keeps the Stone light at the mouth.' },
    { speaker: 'MIRREL', text: 'If you meet the cowled ones again... I do not know. They were GENTLE. That is the part I cannot sit with.' },
  ],
  // The acolytes at the drained site (pre-restoration; kind, never cruel).
  'npc.glowmoss_acolyte_a': [
    { speaker: 'ACOLYTE', text: 'She is not hurt. She is resting. Does the quiet not look gentle, after all that flickering?' },
  ],
  'npc.glowmoss_acolyte_b': [
    { speaker: 'ACOLYTE', text: 'Warden Còr says the dark asks nothing of us. No more failing. No more grief. We only help the tired lights lie down.' },
    { speaker: 'ACOLYTE', text: 'You think us unkind. Everyone does, at first.' },
  ],
  'npc.glowmoss_cowled': [
    { text: 'The cowled figure regards you from deep in its hood. It says nothing.', style: 'narrate' },
    { text: 'It bows, slightly — as if in apology. There is no unkindness in it, which is somehow worse.', style: 'narrate' },
  ],
  // The sleeping luminous kin → the woken one (the flag-pair swap).
  'npc.glowmoss_sleeper': [
    { text: 'The Fennlight lies curled in the dead moss, barely aglow. Its light rises and falls, rises and falls — like slow breathing.', style: 'narrate' },
    { text: 'It will not wake.', style: 'narrate' },
  ],
  'npc.glowmoss_woken': [
    { text: 'The Fennlight turns in the air, trailing light like pollen. Wherever it drifts, the moss leans after it.', style: 'narrate' },
  ],
  // A3 — Wren, shaken, past the drained site. The first crack in the rivalry's
  // brightness; sympathy for the Hollowing voiced, then carried away unsettled.
  'npc.wren_glowmoss': [
    { speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'You woke it up. Good. I think.' },
    { speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'They did not fight us. They APOLOGISED. Who apologises while they... while they do that?' },
    { speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: '...What if they are not wrong? Nothing here got hurt. It was just quiet.' },
    { speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Forget it. Race you to the mine. ...I am not racing. Walk with me a bit?' },
  ],

  // --- Saltreach Fen I (the marsh route) ----------------------------------------
  'npc.fen_warden': [
    { speaker: 'FEN-WARDEN', text: "Mind the planks after dark — the fen's friendly, but it doesn't like to be hurried." },
    { speaker: 'FEN-WARDEN', text: 'Odd thing, though. The eastern woods have gone quiet of late. Quiet like held breath, not like sleep.' },
  ],
  'npc.fen_wader_a_after': [
    { speaker: 'MARIGOLD', text: 'The reeds north of here run right over the causeway — no way round but through. Mind your step and your lamp.' },
  ],
  'npc.fen_courier_b_after': [
    { speaker: 'OSPREY', text: 'The bank east of the causeway is worth the climb — waders leave what they cannot carry. And the hop down saves the walk back!' },
  ],
  'sign.spore_grotto': [
    { text: 'SPORE GROTTO\nThe old beds. The moss-tenders leave them be — what grows down here grew before lamps.' },
  ],
  'sign.fen_landing': [
    { text: 'SALTREACH FEN\nPlanks hold the road; the water holds everything else. North to Lowleaf Hollow, by the channel crossing.' },
  ],
  'sign.fen_channel': [
    { text: 'DEEP CHANNEL — planks end here.\nThe still water answers Tidecall. The islet keeps what the tide-walkers leave.' },
  ],
  'sign.fen_boundary': [
    { text: 'FEN BOUNDARY — Saltreach deepens past this channel.\nNo planks beyond: cross by Tidecall or turn back dry.' },
  ],

  // --- Saltreach Fen II (deep channels — Tidecall load-bearing) -----------------
  'sign.fen_ii_landing': [
    { text: 'SALTREACH DEEPS\nNo planks past this shore. The channels answer Tidecall; the isles keep their own counsel. North by the reed-lights to Lowleaf Hollow.' },
  ],
  'sign.sunkbell_turnoff': [
    { text: 'EAST, ACROSS THE WATER: SUNKBELL SHALLOWS\nThe drowned shrine. The bell has not rung in living memory — but the buoys still point the way, for those the tide will carry.' },
  ],
  'sign.fen_ii_treeline': [
    { text: 'NORTH: LOWLEAF HOLLOW\nFirm ground at last. Follow the green glow through the trees — and if you hear piping, the Bloom is on.' },
  ],
  // E1 "The Quiet Reeds" — the fisher's waiting/closing stages.
  'npc.fen_fisher_wait': [
    { speaker: 'FEN FISHER', text: 'Channel order, remember — near reed, mid-water, then the far one by the treeline. A line lights from home outward.' },
    { speaker: 'FEN FISHER', text: 'And thank you, tide-walker. The fen notices who tends it. It always has.' },
  ],
  'npc.fen_fisher_after': [
    { speaker: 'FEN FISHER', text: 'Two of three standing, and the fish already coming back to them. I count the far dark one every night, mind. In case it changes its... in case it changes.' },
  ],
  // The reeds, refused or revisited (trigger blocked_refs / post states).
  'npc.reed_unasked': [
    { text: 'A lantern-reed, dark over the water. It is somebody\'s tended light — not yours to meddle with, unasked.', style: 'narrate' },
  ],
  'npc.reed_order': [
    { text: 'This reed\'s wick is sound, but its line-mates nearer the jetty still sit dark. A line lights from home outward — the fisher was firm on it.', style: 'narrate' },
  ],
  'npc.reed_lit_a': [
    { text: 'The near lantern-reed burns amber and steady, a small kept light over the black water.', style: 'narrate' },
  ],
  'npc.reed_lit_b': [
    { text: 'The mid-water reed glows warm. Below it, quick silver shapes circle the light like a held breath let out.', style: 'narrate' },
  ],
  'npc.reed_dark_third': [
    { text: 'The far reed stands dark. Your flame would not take, and you somehow know it will not take twice.', style: 'narrate' },
    { text: 'The fen is very quiet here.', style: 'narrate' },
  ],
  'npc.reed_lamplighter_after': [
    { speaker: 'TARN', text: 'Reed-line\'s brighter tonight than all season — your doing, I hear. The treeline\'s just north. Tell Lowleaf the fen sent its regards.' },
  ],

  'npc.bloom_warden_a_after': [
    { speaker: 'IVY', text: 'The beds are lively tonight — Fennlight drifting in from the deep wood for the Bloom. If you mean to ask one home, a charged lamp asks nicer.' },
  ],
  'npc.bloom_warden_b_after': [
    { speaker: 'FERN', text: 'Sable watched your bout from her doorway, you know. She does that. She will deny it to her last breath.' },
  ],
  'npc.cottage_latched': [
    { text: 'The door is latched, with a sprig of glowmoss tucked through the handle — festival custom. Everyone who lives here is outside dancing.', style: 'narrate' },
  ],

  // --- Sunkbell Shallows (the flooded shrine spur) -------------------------------
  'sign.sunkbell_shrine': [
    { text: 'SUNKBELL SHALLOWS\nThe shrine drowned slowly, and the keepers rang the bell until the water reached the rope. So the fen-folk tell it. Tread soft on the steps — they remember feet.' },
  ],
  'sign.sunkbell_bell': [
    { text: 'The verdigris bell hangs silent over its own reflection. When the ripples settle, you can see a second bell in the black water, ringing nothing.', style: 'narrate' },
    { text: 'Rare kin circle the drowned steps, drawn to the quiet. The offering-niches have kept dry what the pilgrims left.', style: 'narrate' },
  ],

  // --- Lowleaf Hollow (the Glowmoss Bloom) ---------------------------------------
  'sign.lowleaf_welcome': [
    { text: 'LOWLEAF HOLLOW\nMind the moss — most of it is older than the town. During the Bloom, follow the lantern-strings and dance where there\'s room.' },
  ],
  'sign.lowleaf_lumenary': [
    { text: 'THE VERDANT LUMENARY\nLampwarden Sable Quill tends the Verdant light. Knock soft; she will not hear a loud knock any better.' },
  ],
  // The pinned letter — the first whisper of Còr's voice (B2 foreshadow; the
  // exact courteous text from the walkthrough; unsigned, never explained here).
  'sign.cor_letter': [
    { text: 'A letter is pinned to the Lumenary notice-board, unsigned, in a careful, courteous hand:' },
    { text: '"To whoever tends these lamps after me: do not grieve the dark. It asks nothing of you, and it never leaves."' },
    { text: 'Nobody in the festival crowd will say who pinned it, or when. Somebody has drawn a small worried face in the corner.' },
  ],
  'sign.lowleaf_deepwood': [
    { text: 'NORTH: GLOWMOSS DEEP\nDark past the first bough — true dark, the kind a plain lamp cannot walk. Without a Glimmerstep, the wood keeps itself.' },
  ],
  'sign.lowleaf_lanternway': [
    { text: 'WEST: THE LANTERNWAY\nThe lit road to the Vesper Crossroads, where every way in Vesperholm meets.' },
  ],
  // The Elder Bed (interact states ride the trigger chain; see build_lowleaf).
  'npc.elder_bed_cold': [
    { text: 'The Elder Bed. Up close the grey is worse — moss like burnt paper between the old stones, a century of kept light gone to ash-colour.', style: 'narrate' },
    { text: 'It is not dead. It is waiting for something, the way a cold hearth waits.', style: 'narrate' },
  ],
  'npc.elder_bed_green': [
    { text: 'The Elder Bed burns green-gold rim to rim, the festival\'s crown wreathing its tallest stone. The moss leans toward your lamp as you pass — it remembers you.', style: 'narrate' },
  ],
  // Festival voices. The fencer line is the B-arc fence (BINDING: nobody in
  // town names the Hollowing as a *presence* — escalation stays monotonic).
  'npc.bloom_fencer': [
    { speaker: 'FESTIVAL AUNTIE', text: 'The Elder Bed? Oh, don\'t you start as well. Not the Hollowing, love — just a tired old bed after a cold spring. Beds have bad years, same as folk.' },
    { speaker: 'FESTIVAL AUNTIE', text: '...Eat a moss-cake. You\'re too thin to be worrying about moss.' },
  ],
  'npc.bloom_piper': [
    { speaker: 'BLOOM PIPER', text: 'Rounds, rounds, the Bloom wants ROUNDS — nobody can sulk in six-eight time, that\'s science.' },
    { speaker: 'BLOOM PIPER', text: 'The dancing ring turns at the hollow\'s heart, where the Elder Bed lies. Always has. Even this year. ESPECIALLY this year.' },
  ],
  'npc.bloom_kid_a': [
    { speaker: 'MOSS KID', text: 'I caught a glow-mote in my HANDS and Gran says if you whisper a wish to it before it wriggles out, the moss keeps the wish FOR you!' },
    { speaker: 'MOSS KID', text: 'I wished for a Fennlight. Don\'t tell the moss I told you, it\'ll think I don\'t trust it.' },
  ],
  'npc.bloom_kid_b': [
    { speaker: 'FERN KID', text: 'The deep wood is RIGHT THERE and nobody will let me even LOOK down it. When I get my vesperlamp I\'m going to walk the dark like it\'s nothing.' },
    { speaker: 'FERN KID', text: '...Is it true your lamp can already do that? Walk it a LITTLE bit. I\'ll watch from here.' },
  ],
  // The kindling explainer (the starter kindles ~16–20; canon verb: KINDLE).
  'npc.kindle_elder': [
    { speaker: 'BLOOM ELDER', text: 'Your lead kin has that look about it, dear — banked too bright for its own little lamp. That\'s not a sickness. That\'s a kindling coming.' },
    { speaker: 'BLOOM ELDER', text: 'When it asks, let it. A kin kindles like a wick catching a bigger flame — same light, more of it. They never stop being who they were. They just get more room to be it in.' },
  ],
  // Wren in town — still BRIGHT (A3, the shaken beat, lands in the Deep).
  'npc.wren_lowleaf': [
    { speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'There you are! I\'ve eaten four moss-cakes and been blessed by two grandmothers, and you\'re out here doing ERRANDS. At a festival!' },
    { speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'They say the warden here would rather battle you than talk to you. Finally, my kind of Lampwarden. Race you to the Gleam — loser carries the moss-cakes.' },
  ],
  // The kilner's flag stages around script.kiln_relight.
  'npc.kilner_cold': [
    { speaker: 'KILNER', text: 'A festival with a cold kiln is a song with no drum, and here I stand, drumless. The wood-store\'s empty — every dry stick went to the lantern-strings.' },
    { speaker: 'KILNER', text: 'There\'s always dry fen-wood under the fringe ferns, east of town, where the Bloom-watch walks. If your lamp\'s not afraid of the lane, I\'d owe you the festival itself.' },
  ],
  'npc.kilner_after': [
    { speaker: 'KILNER', text: 'Hear her roar? Best burn in nine Blooms. And the old bed took the spore like it had only been waiting to be asked — which, between us, it had.' },
  ],
  // The stall-keeper's waiting/after stages (E2 rides script.stall_quest/_reward).
  'npc.stall_waiting': [
    { speaker: 'STALL-KEEPER', text: 'Three bundles, along the glow-beds in the Deep! And if something\'s sitting on one — there\'s always something sitting on one — be polite but FIRM.' },
  ],
  'npc.stall_after': [
    { speaker: 'STALL-KEEPER', text: 'Sold out twice tonight and restocked twice, all on your bundles. The Fennlight in the fringe grass, remember — a stall-keeper never forgets a debt OR a good tip.' },
  ],
  // Sable's "not yet" (the bond-test blocked_ref) + her hall stages.
  'npc.sable_not_ready': [
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: 'Oh — no, not yet. Please. The Bloom won\'t crown over a grey bed, and I won\'t test a bond under an unfinished sky.' },
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'Warm the old moss first. The kilner will know what it needs. Then... then we\'ll see what your light\'s worth.' },
  ],
  'npc.sable_waiting': [
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: 'The kilner by the square — she\'ll know what the bed needs. I\'d walk you there myself, but then everyone would want to TALK to me.' },
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'The moss doesn\'t hurry. You needn\'t either.' },
  ],
  'npc.sable_ready': [
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'The bed blooms. The whole hollow is an octave brighter and it\'s your doing. Step up to the moss-dais when you\'re ready — and we\'ll let the Verdant decide.' },
  ],
  'npc.sable_after': [
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'The Verdant stands, and my hall-moss won\'t settle down about it. Neither will I, quietly.' },
    { speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'Your Glimmerstep opens more than my deep wood, you know. The Spore Grotto, below the Deep. And back in the South — Tideglass Cavern, off the tidal flats. Dark places keep the best gardens. Go see.' },
  ],
  // The provisioner's counter line (script.shop_lowleaf opens the ShopMenu).
  'npc.lowleaf_provisioner': [
    { speaker: 'PROVISIONER', text: 'Balms, charges, and the Verdant chart slate — Spore Puff, Root Strike, Lifedrain. The deep wood doesn\'t forgive an empty satchel.' },
    { speaker: 'PROVISIONER', text: 'And the counter\'s open, festival prices. Which are the same as regular prices. It\'s the SPIRIT of the thing.' },
  ],
  // The guest-bower (interior): a Bloom guest by the long table.
  'npc.bower_guest': [
    { speaker: 'BLOOM GUEST', text: 'I walk in from Pearlmoor for every Bloom. Fen mud to the knee, twice a year, happily — there\'s nowhere else in Vesperholm where the LIGHT smells green.' },
  ],
  // The mapwide "now accessible" crier (post-Gleam, the §5 callout).
  'npc.bloom_crier': [
    { speaker: 'BLOOM CRIER', text: 'Hear it, hear it! The Verdant stands, the Bloom is crowned, and the Wayfarer\'s lamp walks the dark!' },
    { speaker: 'BLOOM CRIER', text: 'They say a Glimmerstep opens the deep wood north of town, the Spore Grotto under it — and old Tideglass Cavern, all the way back on the Dimglass flats! A whole dark map, gone friendly!' },
  ],

  // --- Vesper Crossroads (the Lanternway hub) ---------------------------------
  'sign.crossroads': [
    { text: 'VESPER CROSSROADS\nAll the Lanternway meets here. SOUTH-WEST: Tinderwick. SOUTH-EAST: Pearlmoor Quay. The other roads sleep, unlit.' },
  ],
  'sign.crossroads_spire': [
    { text: 'The inward road. Eight braziers stand cold around its gate — one for each constellation. The mountain waits.' },
  ],
  'npc.lanternway_keeper': [
    { speaker: 'WAYKEEPER', text: 'Every road in Vesperholm touches this stone sooner or later. I keep the lamps lit on the ones that walk.' },
    { speaker: 'WAYKEEPER', text: 'When more Gleams stand up in the sky, more roads wake. That is how the Lanternway has always worked.' },
    { speaker: 'WAYKEEPER', text: 'The inward road? Eight Gleams, Wayfarer. Eight. Do not hurry the dark.' },
  ],
  // The Lowleaf spoke — sleeping until the Verdant Gleam wakes it (its
  // blocked_ref below), then a lit road east-north to the Bloom.
  'sign.crossroads_lowleaf': [
    { text: 'EAST-NORTH: LOWLEAF HOLLOW\nThe forest spoke. Its lamps wake with the Verdant constellation — green road, green light.' },
  ],
  'npc.waykeeper_lowleaf_gate': [
    { speaker: 'WAYKEEPER', text: 'The Lowleaf spoke sleeps yet, Wayfarer — its lamps answer the Verdant, and the Verdant is still dark.' },
    { speaker: 'WAYKEEPER', text: 'The long way round is the fen-road east of Pearlmoor. Roads wake to Gleams; relight the green one and this one will carry you home after.' },
  ],

  // --- Locked-door lines (a gated door warp's blocked_ref) ---
  // Doors are walk-onto: stepping into a locked one (or pressing Confirm at it)
  // plays these instead of barring the way in silence. Keep the canon voice.
  'door.locked_lumenary': [
    { text: "The Lumenary's door is shut. A Lampwarden won't light a hall for a Wayfarer with no kin — find a friend first, then come back." },
  ],
  'door.locked_beacon': [
    { text: 'The beacon door is locked fast. It wants a wick-key — the Dimglass lamplighter keeps one.' },
  ],
  'door.locked_glimmerstep': [
    { text: 'The gap breathes cold dark, too narrow to chance. Without the Glimmerstep gift to thread it, the cave keeps its own counsel.' },
  ],

  // ===========================================================================
  // CINDERHEAD MINE — the Stone wall (walkthrough/02-east; Otho Grist, Stone)
  // ===========================================================================
  'sign.cinderhead_welcome': [
    { text: 'CINDERHEAD MINE\nWe lower the lamps to remember why we carry them. Then we light them again. Walk careful past the vigil, Wayfarer.' },
  ],
  'sign.cinderhead_deep_mouth': [
    { text: 'THE DEEP GALLERIES — down this mouth.\nThe dark below will not take a lamp that cannot see in it. No Glimmerstep, no descent.' },
  ],
  'sign.cinderhead_lumenary': [
    { text: 'STONE LUMENARY — Otho Grist, Lampwarden.\nDown here, light is not given. It is kept.' },
  ],
  'sign.cinderhead_sealed': [
    { text: 'SEALED — by order of the foreman.\nBarred from the OTHER side, years back, to keep the deep dark from wandering up the hoist-line. The bar lifts from here.' },
  ],
  'sign.cinderhead_crystoll': [
    { text: 'CRYSTOLL VAULT — across the void.\nThe floor gives out to pure dark. Only a Starreach steps across a gap like this. Come back when the last constellation is yours.' },
  ],
  // the Lamp-down vigil (unconditional — the vigil is underway on arrival)
  'npc.vigil_elder': [
    { speaker: 'VIGIL ELDER', text: 'We lower the lamps so we remember why we carry them. Then we light them again. That is the whole of it.' },
    { speaker: 'VIGIL ELDER', text: "But the vigil cannot CLOSE — not till the old crew's lamp comes up from the third gallery, still lit. Otho won't have it any other way." },
  ],
  'npc.vigil_miner_a': [
    { speaker: 'MINER', text: "Cowled folk passed through, talking gentle about letting the dark just... be. We told them where the door was." },
    { speaker: 'MINER', text: 'A miner does not surrender to the dark. A miner KEEPS a light in it. There is a difference, and it is the whole of us.' },
  ],
  'npc.vigil_miner_b': [
    { speaker: 'MINER', text: "Mind Otho. He is fair as a plumb-line and twice as hard. His kin are all roof and no rush — you will not out-hit them. Out-LAST them." },
  ],
  // post-Gleam payoff (Arc E: the town answers the win — the lamps are up)
  'npc.vigil_raised_a': [
    { speaker: 'VIGIL ELDER', text: 'Lamps all risen, and the Stone steady overhead. The vigil is CLOSED, Wayfarer — first time in a long dark. We will not forget the hand that carried it up.' },
  ],
  'npc.vigil_raised_b': [
    { speaker: 'PIT-CHILD', text: 'The lamps went UP! All at once, like a sunrise made of lanterns! Did you see? Did you SEE?' },
  ],
  'npc.cinderhead_deep_warden': [
    { speaker: 'DEEP-WARDEN', text: "The forest Wayfarer — Wren? — went down ahead of you, quiet as I've seen them. Something in that drained wood shook the bright right out of them." },
  ],
  // Otho's giver stages (his hall) — the Descent Vigil loop's grammar
  'npc.otho_waiting': [
    { speaker: 'OTHO GRIST', text: 'Lamp still up here, is it? The vigil-lamp is THREE galleries down, still burning. Bring it up. Then we talk.' },
  ],
  'npc.otho_ready': [
    { speaker: 'OTHO GRIST', text: 'You carried it up still lit. Through all that dark. ...Then we are ready, you and I. Step to the aisle when your kin are.' },
  ],
  'npc.otho_after': [
    { speaker: 'OTHO GRIST', text: 'The Stone is yours, and the eastern crown with it. Galehigh waits up the deep and out the far side — keep your light steady, the wind up there is not.' },
  ],
  'npc.otho_not_ready': [
    { speaker: 'OTHO GRIST', text: "No vigil-lamp, no bond-test. I don't hand a Gleam to a lamp I've not seen cross the dark. Down you go." },
  ],
  // E3 The Foreman's Ledger
  'npc.ledger_waiting': [
    { speaker: 'LONE MINER', text: 'Side gallery off the west chamber, that is where it fell. Mind the galleries — they bite, this deep.' },
  ],
  'npc.ledger_after': [
    { speaker: 'LONE MINER', text: 'The whole crew, written down and remembered. You have given an old hand his sleep back, Wayfarer.' },
  ],
  'npc.cinderhead_sealed_miner': [
    { speaker: 'OLD HOIST-HAND', text: "Been meaning to clear that door for years. You did it in a turn. Now the cart-line runs straight to the Crossroads — no more trudging the long fen-road home." },
  ],
  'npc.cinderhead_provisioner': [
    { speaker: 'PIT-PROVISIONER', text: 'Balms, charges, and a chart or two for the deep. What does the dark owe you today?' },
  ],
  // the two vigil-miner sight trainers, beaten
  'npc.gallery_miner_a_after': [
    { speaker: 'DRUSE', text: 'Lamp two chambers down, still lit. Carry it gentle. Hobb is on the last neck before it — he will want his bout.' },
  ],
  'npc.gallery_miner_b_after': [
    { speaker: 'HOBB', text: 'The vigil-lamp is just there, in the chamber beyond. Lift it slow. A flame that kept this long has earned a careful hand.' },
  ],
  'sign.crossroads_mineshortcut': [
    { text: 'CINDERHEAD CART-HOIST.\nThe deep-mine line. The cars run when the sealed gallery door is opened from the far side — not before.' },
  ],
};

const FALLBACK: DialogueLine[] = [{ text: '...' }];

/** Resolve a dialogue ref to its pages, or a quiet fallback if unknown. */
export function getDialogue(ref: string | undefined): DialogueLine[] {
  if (!ref) return FALLBACK;
  return DIALOGUE[ref] ?? FALLBACK;
}
