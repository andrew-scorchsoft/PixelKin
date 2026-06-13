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

  // --- The Lifting House (S4 "The Booji-Wooji Man") — the quayside gym --------
  'sign.lifting_house_rules': [
    { text: 'HOUSE RULES\n1. Put the stones back.\n2. Spot whoever asks.\n3. If PAUL offers you advice, take it. If he offers you a story, count your pockets after.' },
  ],
  'npc.booji_andy_wait': [
    { speaker: 'ANDY', text: 'Abdul first — he\'s seen where the old man goes. Then Sid, if you can get three words out of him. That\'s two more than usual.' },
    { speaker: 'ANDY', text: 'And if you find Paul — ask him about the Registry. For me. For all of us. Mostly for me.' },
  ],
  'npc.booji_andy_after': [
    { speaker: 'ANDY', text: 'Every dusk he doesn\'t come in, I tell a new lifter about him. Every dusk he DOES come in, I pretend I never talk about him at all.' },
    { speaker: 'ANDY', text: 'Anyway. As I was saying. The bench. The knee. Have I told you about the knee?' },
  ],
  'npc.booji_abdul_pre': [
    { speaker: 'ABDUL', text: 'Stones don\'t lift themselves. ...That\'s it. That\'s the whole wisdom.' },
  ],
  'npc.booji_abdul_after': [
    { speaker: 'ABDUL', text: 'Do I carry my lamp, or does my lamp carry me... Three dusks that\'s kept me up now. Tell the old man thanks for nothing.' },
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
    { speaker: 'PAUL', text: 'Still here. Still not telling. The cup of something stands exactly as promised — some night.' },
    { speaker: 'PAUL', text: 'Keep the folio somewhere it doesn\'t belong. Things like that go stale on a proper shelf.' },
  ],
  // Andrew — the OTHER bench guy (two separate lifters; Andy talks, Andrew lifts).
  'npc.booji_andrew': [
    { speaker: 'ANDREW', text: 'Can\'t talk long. Mid-set. The bench waits for no man.' },
    { speaker: 'ANDREW', text: 'Paul? He spotted me once. Didn\'t say a word the whole set — just stood there. Best lifting I\'ve ever done. Make of that what you will.' },
  ],
  // Rot — the house's strongest, and its oldest. An allotment-keeper of seventy-two
  // who presses the big harbour-stone clean overhead. Points the player on to Paul
  // (out at the breakwater), and seeds the Chickenpig WITHOUT naming it.
  'npc.booji_rot': [
    { speaker: 'ROT', text: 'YEAH! There it goes — clean, and over the head. A hundred and twenty kilos of harbour-stone, friend, and I am SEVENTY-TWO summers old. Nothing but a peanut.' },
    { speaker: 'ROT', text: 'Don\'t gawp. I keep an allotment up the hill — marrows, leeks, a turnip that ought to pay rent. You haul wet earth from one dusk to the next, the stones come up like loaves.' },
    { speaker: 'ROT', text: 'My Anth says I love that allotment more than I love her. I tell her there is NO contest. ...I am careful never to say which way. That\'s a joke, mind — don\'t you go telling Anth.' },
    { speaker: 'ROT', text: 'One thing out there I cannot beat: the squirrels. Thieving little stone-heads. I can press a mooring-block overhead and I cannot keep ONE off my marrows. There\'s a lesson in that. Seventy-two years and I have not found it.' },
    { speaker: 'ROT', text: 'You\'ll be after the old man. PAUL. He\'s not in the house, lad — he\'s out past the bell, the very end of the breakwater, where the boards give out. Stood at a lamp he won\'t light. Go and find him. He\'s worth the walk.' },
    { speaker: 'ROT', text: 'And keep your lamp up out there. Paul\'s got... company at that dark lamp. Something I\'ve no name for — and I have named every kin on this coast. Crows at the black like the morning\'s already its idea. Daft little thing. ...You bring it home, if it\'ll have you.' },
  ],
  // The Chickenpig at Paul's dark lamp (post-S4 set-piece catch).
  'npc.chickenpig_shy': [
    { text: 'The chicken-pig tucks its head under its one red wing and is immediately, profoundly asleep. Even heralds nap. It will hear you out again once you have won {remaining} more battles.' },
  ],
  'npc.chickenpig_after': [
    { text: 'Only the dark lamp now, and the old man\'s company. Somewhere in your lamp, a rooster-pig is practising being right about the morning.' },
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

  // The onward roads are shut to a Wayfarer with no kin yet — the opening's
  // soft wall, pointing a brand-new player back to Fenn at the Waystone (the
  // East/North warps gate on flag:has_starter, so this only ever fires pre-kin).
  'crossroads.no_kin_yet': [
    { text: 'No kin walks at your side yet, and the roads beyond the crossroads are no place to wander alone. Star-tender Fenn waits at the Waystone — see him, and take up your first lamp, before you set out.' },
  ],
  // The inward (Spire) road's "not yet" — fires until all eight Gleams stand
  // (flag:hub_unlocked). Echoes sign.crossroads_spire so a new player learns it
  // is the endgame road, never the way out of the opening.
  'crossroads.spire_not_yet': [
    { text: 'The inward road runs to the dark mountain itself, and its gate stays shut till all eight Gleams stand lit in the sky. No road for a Wayfarer just setting out — the lit ways are yours first.' },
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

  // ===========================================================================
  // THE NORTH — Galehigh Terraces (walkthrough/03-north). Voice: the last warm
  // colour before the cold leg; the Kite-rising is the game's humour-warmest
  // beat (the winch notice is the town's ONE wry sign).
  // ===========================================================================
  'sign.galehigh_welcome': [
    { text: 'GALEHIGH TERRACES\nThe last fire before the climb. Mind the gusts.' },
  ],
  'sign.galehigh_winch': [
    { text: 'THE KITE-RISING WINCH\nRiders ascend at their own joy. The Festival Committee asks that you wave back — the children keep count.' },
  ],
  'sign.galehigh_high_ledges': [
    { text: 'The high terraces open only to a kin that rides the thermals. The wind takes nobody it has not been introduced to.' },
  ],
  'sign.galehigh_windeye': [
    { text: 'THE WIND-EYE\nOn a clear dusk the updraft column sings. The grotto keeps what the wind keeps — climbers say a sky-kin nests at the eye itself.' },
  ],
  'sign.galehigh_lanternway': [
    { text: 'SOUTH: THE LANTERNWAY\nThe lit road to the Vesper Crossroads, where every way in Vesperholm meets.' },
  ],
  'sign.crossroads_galehigh': [
    { text: 'NORTH-WEST: GALEHIGH TERRACES\nThe mountain spoke. Its lamps wake with the Storm constellation — high road, high wind.' },
  ],
  'npc.waykeeper_galehigh_gate': [
    { speaker: 'WAYKEEPER', text: 'The Galehigh spoke sleeps yet, Wayfarer — its lamps answer the Storm, and the Storm is still dark.' },
    { speaker: 'WAYKEEPER', text: 'The road north runs the long way for now: east through the fen, up through Cinderhead\'s deep, and out the mountain\'s far side. Relight the Storm and this spoke will carry you home after.' },
  ],
  'npc.waystone_kid_kite': [
    { speaker: 'WAYSTONE KID', text: 'LOOK at it go! The kite-maker put little LAMPS on the tail — Gran says if I\'m not careful I\'ll have the whole Lanternway lit. GOOD.' },
    { speaker: 'WAYSTONE KID', text: 'The string hand is everything, you know. A Wayfarer told me that. It was you. I\'m telling everyone.' },
  ],
  // The festival, pre-Gleam (warm, communal, a little daft — the build-up).
  'npc.galehigh_festival_piper': [
    { speaker: 'FESTIVAL PIPER', text: 'A reel for the Rising! I play to the kites, you understand — the dancers just happen to benefit.' },
    { speaker: 'FESTIVAL PIPER', text: 'Mira\'s up at the launch ledge already. She says the wind practises all year for tonight. She talks about the wind the way other folk talk about a sister.' },
  ],
  'npc.galehigh_festival_kid': [
    { speaker: 'FESTIVAL KID', text: 'My kite\'s got NINE lamps on the tail. Talo\'s only has six. It\'s not a contest, Gran says. Gran counted them for me though.' },
  ],
  'npc.galehigh_festival_goer': [
    { speaker: 'FESTIVAL-GOER', text: 'We fly the kites so the stars have something to climb back up. Daft, maybe. But the night\'s a little less long when the whole hill\'s lit.' },
  ],
  'npc.galehigh_quest_witness': [
    { speaker: 'TERRACE AUNTIE', text: 'Mira shouted the whole asking down from the ledge, didn\'t she. She does that. We\'ve given up sending letters up the winch — she answers them off the cliff at volume.' },
    { speaker: 'TERRACE AUNTIE', text: 'The kite-maker\'s your next call, love — lower terrace, the stall with the orange silk. Her best kite blew to bits in the squall and she\'s been too proud to ask for legs.' },
  ],
  // Arc A foreshadow — Wren at the festival, bright on top, quieter underneath.
  // (A4 lands at Pale Vault; this only plants the doubt.)
  'npc.wren_galehigh': [
    { speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'This festival is RIDICULOUS. I\'ve flown three kites, eaten something called a gust-cake, and been adopted by at least one grandmother.' },
    { speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: '...Heard a trader on the stair, though. Said the towns the Hollowing\'s quieted sound peaceful. Quiet towns. No more lamps guttering, no more goodbyes. ...Doesn\'t sound like the worst thing, does it?' },
    { speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Forget I said it. Race you up the Stair — when the wind lets you.' },
  ],
  // The winch-keeper's three stages + the winch warp's "not yet".
  'npc.winch_keeper_wait': [
    { speaker: 'WINCH-KEEPER', text: 'She hauls riders to the launch ledge, this old drum — but only at the Rising, and only for a kite the town has flown. Festival law, older than me, and I am EXTREMELY old.' },
    { speaker: 'WINCH-KEEPER', text: 'Want up to Mira? Then get yourself a kite worth blessing. The kite-maker\'s on the lower terrace, and between us — she needs the errand more than you need the ledge.' },
  ],
  'npc.winch_not_ready': [
    { speaker: 'WINCH-KEEPER', text: 'Easy there! The drum turns for blessed kites and nothing else — raise one with the town first. Kite-maker\'s stall, then the Rising. THEN the sky.' },
  ],
  'npc.winch_keeper_after': [
    { speaker: 'WINCH-KEEPER', text: 'Up you go, any time — the drum knows you now. And you waved back on the first ride. The children noted it down. You\'re in the GOOD ledger.' },
  ],
  // The kite-maker's stages (lost → built → festival → the Round leg).
  'npc.kite_maker_lost': [
    { speaker: 'KITE-MAKER', text: 'Spar, sail and tail — my best kite, in three pieces, somewhere down the lower terraces. One squall. ONE. Thirty years of knots and the sky just... helped itself.' },
    { speaker: 'KITE-MAKER', text: 'If your road takes you across the lower terraces anyway — and it will, all roads here do — keep an eye down. Lantern-orange silk. You can\'t miss it. I miss it terribly.' },
  ],
  'npc.kite_maker_after': [
    { speaker: 'KITE-MAKER', text: 'She flies TRUE — I watched the trim from here. Get to the winch terrace before the Rising peaks, Wayfarer. A town-built kite wants a town watching.' },
  ],
  'npc.kite_maker_round_after': [
    { speaker: 'KITE-MAKER', text: 'Mind the cross-wind where the spoke meets the Crossroads — and tell the waystone kid what I told you. The string hand is everything. The kite already knows the rest.' },
  ],
  // Mira's town stages (post-Gleam callouts → the N3 ribbon-giver swap).
  'npc.mira_galehigh_after': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'Still here! Good — the wind kept three places for you and I promised it I\'d nag: the WIND-EYE, off our own high terrace. THUNDERROOST, off the second stair. And the drop-ledge home from the crags, once you\'ve stood on them.' },
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'And mind the Storm\'s manners now you carry its Gleam — a numbed kin is a kite with a fouled string. Carry balms. Ask the wind. Thank it after.' },
  ],
  'npc.mira_ribbon_after': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'The quiet ledge, west of the second stair, behind the crag. No note, no waiting. The wind will mind it better than words would.' },
  ],
  'npc.mira_skyloft': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'You don\'t fight the wind, apprentice. You ask it to lift you — and you thank it when it does. Step up to the ledge when your kin are ready.' },
  ],
  'npc.mira_skyloft_after': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'Off the ledge and glide LONG — that\'s the whole trick of the Updraft Kite. And the Wind-Eye first, before the Stair takes you north. Promise me the Wind-Eye. The wind sings there, and it so rarely gets an audience.' },
  ],
  'npc.mira_not_ready': [
    { speaker: 'MIRA VAEL', portrait: 'mira', expr: 'neutral', text: 'Not yet, apprentice — the town flies FIRST. That\'s the whole shape of the thing. Down you go: raise a kite with them, fly it at the Rising, and the winch will bring you back to me.' },
  ],
  // Ambient town + interiors.
  'npc.galehigh_farmer': [
    { speaker: 'TERRACE FARMER', text: 'Everything on these terraces grows bent — crops, fences, farmers. You learn to read it: the bend SHOWS you the wind. Straight things up here are just things that haven\'t listened yet.' },
  ],
  'npc.galehigh_gleam_kid': [
    { speaker: 'TERRACE KID', text: 'The STORM one! Right overhead! It came back the same night the kites went up — Gran says the kites showed it the way and I believe Gran over everyone.' },
  ],
  'npc.galehigh_gleam_farmer': [
    { speaker: 'TERRACE FARMER', text: 'Five constellations standing, and ours among them. The crops won\'t grow any straighter for it — but I find I stand a bit straighter, and that\'ll do.' },
  ],
  'npc.galehigh_hall_keeper': [
    { speaker: 'HALL-KEEPER', text: 'Looking for Mira? The Lampwarden is not in her hall, dear — the Lampwarden is in the SKY. The hall is where the sky\'s business gets written down after.' },
    { speaker: 'HALL-KEEPER', text: 'The Storm Gleam is met at the launch ledge, up the great winch. And the winch answers the festival, not the wind — fly a kite with the town first.' },
  ],
  'npc.galehigh_hall_festival': [
    { speaker: 'HALL WARDEN', text: 'The Storm stands, and the hall\'s banners haven\'t hung still since. Three hundred years this hall kept the Storm\'s ledger — tonight we wrote the good line in it.' },
  ],
  'npc.galehigh_inn_guest': [
    { speaker: 'INN GUEST', text: 'I asked the keeper for the room out of the wind. She laughed for quite some time. There is no room out of the wind. It is, I am told, part of the charm.' },
  ],
  'npc.galehigh_home_elder': [
    { speaker: 'TERRACE ELDER', text: 'I flew my first Rising off that same launch ledge, seventy years gone. The wind hasn\'t changed. That\'s the comfort of living up here — the wind is the one thing the dusk never managed to quiet.' },
  ],
  'npc.galehigh_home_kid': [
    { speaker: 'TERRACE KID', text: 'When I\'m big I\'m going to ride the winch AND the thermals AND a storm-bird. Da says one impossible thing a year. Da is slow.' },
  ],
  'npc.galehigh_shopkeeper': [
    { speaker: 'KITE-KEEPER', text: 'Storm charts off the last cart — Thunder Kick, Volt Arc, and the big Gale Slam for them as can read it. And stock your balms HERE, Wayfarer: Pale Vault keeps no counter. Lovely town. Terrible shopping.' },
  ],
  // Sight-trainer after-states.
  'npc.galehigh_kitehand_after': [
    { speaker: 'PERRIN', text: 'The wind still approves of you — it mentions it most gusts. Fly at the Rising if you haven\'t. The third gust bites, but it means well.' },
  ],
  'npc.galehigh_terracer_after': [
    { speaker: 'SORREL', text: 'The cabbages have agreed to forget the bout if I have. Upward and onward, Wayfarer — and if you meet the wind-gap, give it my regards from a safe distance.' },
  ],
  'npc.skyloft_ward_a_after': [
    { speaker: 'TAMSIN', text: 'The ledge is yours to stand. Mind the rail on the west side — the wind uses it as a doorway, and it doesn\'t knock.' },
  ],
  'npc.skyloft_ward_b_after': [
    { speaker: 'BRAN', text: 'The wind said yes to you — I heard it plain. It doesn\'t say it twice, so walk like you remember the once.' },
  ],

  // ===========================================================================
  // THE NORTH — Windward Stair I → II. Quiet transit, Arc D pacing: the warmth
  // handed over to the high blue. The distance-marker is the cluster's one wry
  // line; everything past the wind-gap runs sincere.
  // ===========================================================================
  'sign.windward_marker': [
    { text: 'WINDWARD STAIR\nGalehigh: 412 steps down. Pale Vault: a good deal more up.' },
    { text: 'The stair-warden counted once, in better weather, and asks that you not make him do it again.' },
  ],
  'sign.windward_windgap': [
    { text: 'THE WIND-GAP\nThe stair ends here; the wind goes on. Only a kin that rides the thermals crosses the gap.' },
  ],
  'sign.windward_roost': [
    { text: 'THUNDERROOST — across the lip.\nThe storm-birds keep it. Mind the nest, and the weather it dreams.' },
  ],
  'npc.windward_pilgrim': [
    { speaker: 'PILGRIM', text: 'I walk up every year for the Aurora-watch. You stand on the ice, you hold your lamp, and nobody speaks for an hour. It is the only crowd I have ever been able to bear.' },
    { speaker: 'PILGRIM', text: 'The glacier folk say the sky comes nearer up there. I think it\'s the other way about. I think Pale Vault is where the ground stops insisting.' },
  ],
  // The crag-tender — N1's keeper (post-kettle on Stair I) and the shortcut
  // ledge's rounds (Stair II); one ref serves both placements by design.
  'npc.windward_crag_tender': [
    { speaker: 'CRAG-TENDER', text: 'The kettle\'s on, child — it is always on, that\'s the whole ministry. Sip from the flask when the glacier finds your bones; it\'s the same brew, and it remembers you fetched the herb for it.' },
    { speaker: 'CRAG-TENDER', text: 'Cold up here, isn\'t it. If your lamp gutters, just step off that ledge — it\'s a short glide home to Galehigh\'s fires. Knowing the way back is half of going on.' },
  ],
  'npc.windward_craghand_after': [
    { speaker: 'EDDA', text: 'Rest at the bends, climb between them — that\'s the stair\'s whole wisdom. The crag-tender\'s camp is two switchbacks up, and her kettle is better company than I am.' },
  ],
  'npc.windward_galewatch_after': [
    { speaker: 'ROWAN', text: 'The wind-gap\'s ahead — the stair just stops, like the mason lost his nerve. It wants a thermal-rider. You have the look of one now.' },
  ],
  'npc.windward_cragwatch_after': [
    { speaker: 'MERLE', text: 'Thunderroost\'s across the east lip, if your kite-kin fancies meeting the storm-birds at home. And the glacier\'s down the far slope. Walk in quiet — Pale Vault hears everything and answers almost none of it.' },
  ],

  // ===========================================================================
  // THE NORTH — Pale Vault Glacier + the Undercroft. The lonely aurora; the
  // B3/C3/A4 cluster lands here. ZERO humour past the inn (the one permitted
  // dry line below); the Aurora-watch is a silent vigil.
  // ===========================================================================
  'sign.pale_vault_welcome': [
    { text: 'PALE VAULT GLACIER\nThe vault keeps its quiet. Walk softly, and keep your lamp close.' },
  ],
  'sign.pale_vault_undercroft': [
    { text: 'THE LUMENARY UNDERCROFT\nThrough the blue ice, seven dark brackets descend into the glacier. The door answers aurora-oil, and nothing else.' },
  ],
  'sign.pale_vault_pass': [
    { text: 'WEST: HUSHFROST PASS\nColdfog holds the far throat. Only a warded flame walks through.' },
  ],
  'sign.pale_vault_deepice': [
    { text: 'THE DEEP ICE\nThe glacier closes this fold to any flame that cannot ward itself. What sleeps past the blue does not wake for plain light.' },
  ],
  // Ysolde's stages + the Lamp-Line's blocked lines (all in her voice or the
  // vault's).
  'npc.ysolde_waiting': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'The oil first, wanderer. The tallow-keeper renders it in the approach hollows — though her hearth wants waking before her pans do. Storm-felled wood lies up toward the crags; the mountain is generous to the patient.' },
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'There is no hurry. The brackets have been dark for years; they can be dark one evening more. But not, I think, two.' },
  ],
  'npc.ysolde_door_unlit': [
    { speaker: 'YSOLDE FROST', text: 'The vault answers oil, wanderer, not eagerness. Come back with aurora-oil in hand, and the door will know you.' },
  ],
  'npc.ysolde_vault': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Walk the line slowly, if you like. The cold has waited years; it can wait an evening. It is the meaning that must not be hurried, not the flame.' },
  ],
  'npc.ysolde_not_ready': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'Brackets behind you still hold their dark, wanderer. The line is not lit — and I test no bond under an unfinished vault. Walk back, and finish what the first flame promised.' },
  ],
  'npc.ysolde_hall_after': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'warm', text: 'The vault is a lit place, and the northern crown stands. I find I keep going down just to look at the brackets. Do not tell the town; they believe me serene.' },
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Your Emberward opens the Hushfrost throat, west — and our own deep ice, past the blue fold. Sweep the fold before you go; the glacier keeps rare hearts where only a warded flame walks. Then the pass, and the long road to the Solarium.' },
  ],
  'npc.undercroft_bracket_cold': [
    { text: 'The bracket is cold, and means to stay so. A line lights in order — the flame nearer the door has not yet been asked.', style: 'narrate' },
  ],
  'npc.undercroft_ward_a_after': [
    { speaker: 'SELA', text: 'The line remembers every hand that lights it. Yours it will remember kindly — walk on, and keep your order.' },
  ],
  'npc.undercroft_ward_b_after': [
    { speaker: 'ORRIN', text: 'Ysolde waits at the heart. She has waited years for a flame like yours, and will deny having waited at all.' },
  ],
  // The tallow-keeper's stages around script.render_oil.
  'npc.tallow_keeper_doused': [
    { speaker: 'TALLOW-KEEPER', text: 'Mind the camp, child — there\'s nothing on. The storm put my hearth out and the cold got into the stones, and a doused hearth renders nothing. Years of keeping the vault\'s oil, and now the vault waits on ME.' },
    { speaker: 'TALLOW-KEEPER', text: 'Storm-felled wood would wake it — dry-hearted, the kind the gales stack along the upper hollows. My carrying days are done. Perhaps yours are just starting.' },
  ],
  'npc.tallow_keeper_after': [
    { speaker: 'TALLOW-KEEPER', text: 'The kettle sings, the pans run pale and bright, and the vault has its oil again. Seven brackets, child — in ORDER. A line is a promise kept one lamp at a time.' },
  ],
  // B3's quiet cast: the figure before the scene, the witness after.
  'npc.cor_quiet': [
    { text: 'The figure on the shelf does not turn. The cold coming off the quieted valley below is not weather.', style: 'narrate' },
    { text: 'It waits — courteously, patiently — as if it were you who asked to speak.', style: 'narrate' },
  ],
  'npc.pale_vault_witness': [
    { speaker: 'GLACIER WIDOW', text: 'You spoke with him. We all have, once. He buried two of ours the winter the dusk fell — dug the ground himself, said the words kindly, and wept where he thought nobody watched. That is the trouble with Còr. He MEANS it.' },
    { speaker: 'GLACIER WIDOW', text: 'Nobody in this town joined him. But nobody here laughs at the ones who did, either. Now you know why.' },
  ],
  // The Aurora-watch's keepers and watchers.
  'npc.vigil_keeper_after': [
    { speaker: 'VIGIL-KEEPER', text: 'You stood well. The watch is older than the dusk, you know — we were keeping it when the sky was full, and we will keep it when the sky is full again. The standing IS the keeping.' },
  ],
  'npc.aurora_watcher_a': [
    { speaker: 'WATCHER', text: 'No singing here, no dancing. We stand, and we hold our lamps, and the sky walks over us. Other towns find it cold. We find the other towns loud.' },
  ],
  'npc.aurora_watcher_b': [
    { speaker: 'WATCHER', text: 'My mother stood this ice, and hers. The aurora is the one light the dusk never took — we hold our lamps up so it knows we noticed.' },
  ],
  'npc.pale_vault_townsfolk': [
    { speaker: 'GLACIER-DWELLER', text: 'We do not shout in Pale Vault. The glacier carries a whisper further than a yell, and it keeps everything you give it. Speak as if the ice were listening. It is.' },
  ],
  'npc.pale_vault_inn_guest': [
    { speaker: 'INN GUEST', text: 'Quietest inn in Vesperholm. The ice creaks once a night, around third bell. We all look forward to it enormously.' },
  ],
  'npc.pale_vault_home_elder': [
    { speaker: 'GLACIER ELDER', text: 'Folk ask how we bear the loneliness. Child, the aurora has crossed my window every night of my life. I have never once been alone up here. Cold, yes. Alone, never.' },
  ],
  'npc.pale_vault_home_kid': [
    { speaker: 'GLACIER KID', text: 'I can hear the undercroft through the floor when I press my ear down. It used to hum nothing. Lately it hums SOMETHING. I check every morning.' },
  ],
  'npc.pale_vault_hall_keeper': [
    { speaker: 'HALL-KEEPER', text: 'Ysolde keeps the hall, but the hall does not keep Ysolde — she is at the undercroft door more nights than not, looking at seven dark brackets through the ice. Begin there, Wayfarer. She will already know you are coming.' },
  ],
  'npc.pale_vault_hall_festival': [
    { speaker: 'OIL-WARDEN', text: 'The Frost stands, the brackets burn, and the hall smells of aurora-oil for the first time in years. Ysolde has read the same ledger page four times tonight. We pretend not to see.' },
  ],
  'npc.pale_vault_gleam_watcher': [
    { speaker: 'YOUNG WATCHER', text: 'Storm and Frost together — the whole northern crown, closed over our ice. At the watch tonight nobody spoke, same as ever. But every lamp on the line was lit. EVERY one. That has not happened in my lifetime.' },
  ],
  'npc.pale_vault_gleam_kid': [
    { speaker: 'GLACIER KID', text: 'The undercroft hums a CHORD now. I checked this morning. The ice is happy. I am telling everyone the ice is happy and no one is arguing.' },
  ],
  // N2's giver between viewpoints, and after.
  'npc.sketcher_working': [
    { speaker: 'SKETCHER', text: 'The crag above the wind-gap, the glacier shore, the festival ice from the far braziers — in that order, and LOOK properly. Long enough to be cold. I will know if you skimmed.' },
  ],
  'npc.sketcher_after': [
    { speaker: 'SKETCHER', text: 'Forty years of failing to catch that sky, and what I was missing was somebody to hold still instead of it. The sketch is done. When the passes take you west, look up for me — they say the sky out there is nearly dawn-coloured.' },
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
    { text: 'HUSHFROST PASS. The quietest road in Vesperholm. The Pass Committee thanks you for not testing this.' },
  ],
  'sign.hushfrost_coldfog': [
    { text: 'WEST — THE COLDFOG THROAT. The canyon\'s far mouth is choked with a fog no ordinary flame survives. A warded ember walks through where every torch has failed.' },
  ],
  'npc.hushfrost_pass_tender': [
    { speaker: 'PASS-TENDER', text: 'It creeps further up the canyon every year now. My lamp won\'t hold against it — but yours might, traveller. Warm it through, and mind the kin on the far side. They\'ve gone... quiet.' },
  ],
  'npc.hushfrost_lampman_after': [
    { speaker: 'DUNSTAN', text: 'My lamp holds an inch better just from watching yours work. Warm the throat through, Wayfarer — and do not stop to listen to the fog.' },
  ],
  'npc.hushfrost_survivor_after': [
    { speaker: 'HESPER', text: 'You will do. Past the throat the fog THINS, mind — it does not END. Keep your flame fed and your kin close, and you will come out the gold side.' },
  ],

  // --- Hushfrost Pass II (X1 — grief register, zero humour) -------------------
  // The hook line, VERBATIM from the walkthrough — her waiting stage.
  'npc.numbed_kin_caretaker': [
    { speaker: 'CARETAKER', text: 'It used to glow like a hearth. Now it just sleeps. They tell us that\'s mercy. I light a lamp by it anyway.' },
    { speaker: 'CARETAKER', text: 'The aurora-oil pools under the old ice in the hollow north of here. Your flame is warded — mine never was. I\'ll be here. I\'m always here.' },
  ],
  'npc.caretaker_after': [
    { speaker: 'CARETAKER', text: 'She sleeps easier in the light — I can tell by the set of her, the way you can with someone you\'ve sat beside long enough.' },
    { speaker: 'CARETAKER', text: 'I don\'t ask the lamp to wake her any more. I only ask it to be there if she does. That\'s what a lamp is FOR, whatever else they tell you these days.' },
  ],
  // The numbed Hearthkit (interact reads; the flag:dawn swap is postgame's).
  'npc.numbed_kin_sleeping': [
    { text: 'A Hearthkit lies curled in the blankets, grey as banked ash. It is breathing — slow, and even, and far away. No warmth comes off it at all.' },
  ],
  'npc.numbed_kin_awake': [
    { text: 'The Hearthkit is sitting up in the blankets, blinking at the daylight — and glowing, hearth-warm, the way it must have glowed all along underneath.' },
    { speaker: 'CARETAKER', text: 'She woke with the dawn. Of course she did. She was only ever waiting for something worth waking FOR.' },
  ],
  'npc.hushfrost_thawtender_after': [
    { speaker: 'TILDA', text: 'Straight on for the gold, Wayfarer. Tell the warm I swept the road for it.' },
  ],
  'sign.hushfrost_aurora': [
    { text: 'AURORA HOLLOW. The lights pool under the ice here. A warded flame may walk in and look up.' },
  ],
  'sign.hushfrost_gold': [
    { text: 'WEST — THE SUNKEN SOLARIUM. That gold on the fog is stored daylight. Walk toward the warmth.' },
  ],

  // --- Sunken Solarium ---------------------------------------------------------
  'sign.solarium_welcome': [
    { text: 'THE SUNKEN SOLARIUM. The sun drowned here, they say. Listen close: it\'s only sleeping.' },
  ],
  'sign.solarium_halls': [
    { text: 'THE FLOODED HALLS. The moon-tide parts for a called tide — what drowned here waits for you.' },
  ],
  'sign.solarium_backfold': [
    { text: 'Night-flowers seal this fold of the garden. A pocket of daylight would wake them.' },
  ],
  'sign.solarium_climb': [
    { text: 'WEST — THE SUNVAULT CLIMB. The garden-roads rise toward the stars from here.' },
  ],
  'npc.solarium_brazier_dead': [
    { text: 'The brazier is dead — and not merely out. The bowl is full of drowned daylight, cold as the deep water it sank in. It wants its own light back: a sunmote, fetched up from the halls.' },
  ],
  'npc.lucan_not_ready': [
    { speaker: 'LUCAN PYRE', text: 'Eager! I admire it. But no, apprentice — nobody tests a bond on a DARK stage. The daylight\'s drowned and the braziers know it. Fetch it up, spark by spark, and then the boards are yours.' },
  ],
  'npc.lucan_waiting': [
    { speaker: 'LUCAN PYRE', text: 'The phials glint in the flooded halls — stored daylight always shines for somebody coming to fetch it. Spark by spark, apprentice. The troupe is in costume and the year is not getting any warmer.' },
  ],
  'npc.lucan_after': [
    { speaker: 'LUCAN PYRE', text: 'Seven Gleams over the garden and my stage lit under all of them. Go on up the Climb, Wayfarer — the eighth act is Nessa\'s, and she has been rehearsing it at that eyepiece her whole life.' },
    { speaker: 'LUCAN PYRE', text: 'And when the sky is whole and the histories are written — tell them the sun came back THROUGH HERE first. A theatre keeps its notices.' },
  ],
  'npc.troupe_waiting': [
    { speaker: 'TROUPE PLAYER', text: 'In costume since noon, and the stage dark as the bottom of the flood. We don\'t mind. Forty years of waiting teaches you how to wait BEAUTIFULLY.' },
  ],
  // HUMOUR slot 1 — the stilts (builder-sanctioned copy).
  'npc.troupe_stilts': [
    { speaker: 'STILT-WALKER', text: 'Forty years we\'ve staged "The Sun Returns". One night soon I\'d like the title to stop being the ambitious part.' },
  ],
  'npc.troupe_mask_waiting': [
    { speaker: 'TROUPE PLAYER', text: 'The side room off the flooded halls — the water took the mask the winter it rose, and none of us swim like a called tide. Tonight of all nights, the scene should wear its own gold.' },
  ],
  // HUMOUR slot 2 — the mask, after (builder-sanctioned copy).
  'npc.troupe_mask_after': [
    { speaker: 'TROUPE PLAYER', text: 'You dredged my face out of a drowned cellar and I\'ve never looked better. That\'s theatre.' },
  ],
  'npc.solarium_witness': [
    { speaker: 'OLD STAGEHAND', text: 'I rigged that stage as a boy, before the water came. Tonight I watched it light spark by spark, and I am not ashamed to say I sat down on a prop crate and stayed there.' },
  ],
  // The walkthrough's signature festival-goer line, verbatim.
  'npc.solarium_festival_goer': [
    { speaker: 'FESTIVAL-GOER', text: 'Last warm day of the year, they call it. Been calling it that for as long as the night\'s been long. We just keep spending warm days until one of them sticks.' },
  ],
  'npc.solarium_bread': [
    { speaker: 'BREAD-SHARER', text: 'Warm bread, no charge — today least of all. Stored daylight in the oven and forty years of practice in the crumb. Eat it while it\'s warm. That\'s the WHOLE custom.' },
  ],
  'npc.solarium_kid': [
    { speaker: 'FESTIVAL KID', text: 'I put my hand in the water where the gold shines up and it\'s WARM. The drowned sun is warm! Nobody believes me except everybody, because they\'ve all done it too.' },
  ],
  'npc.solarium_gleam_watcher': [
    { speaker: 'FESTIVAL-GOER', text: 'Seven stars. SEVEN. I watched the sun\'s own constellation stand up over the garden it drowned in. Whatever this year asks of me now, it has already paid in advance.' },
  ],
  'npc.solarium_gleam_elder': [
    { speaker: 'FESTIVAL ELDER', text: 'A hundred warm days I\'ve spent on this terrace, child, and tonight is the first one that felt like a down payment instead of a goodbye. THAT is what a Gleam is. Spend it well.' },
  ],
  'npc.troupe_player_a_after': [
    { speaker: 'CALLA', text: 'The understudies have talked of nothing else since. You\'ve set the company back a WEEK.' },
  ],
  'npc.troupe_player_b_after': [
    { speaker: 'ORSINO', text: 'I\'ve worked your bout into my act two. With permission. Or — well. With enthusiasm, certainly.' },
  ],

  // --- Solarium Lumenary (the green room — the region's rest point) -----------
  // HUMOUR slot 3 — the prompter (builder-sanctioned copy).
  'npc.solarium_prompter': [
    { speaker: 'PROMPTER', text: 'Everyone\'s a critic. The dark heckled us for forty years, and tonight it\'s losing its seat.' },
  ],
  'npc.solarium_hall_keeper': [
    { speaker: 'SUN-LEDGER KEEPER', text: 'The Heliarium\'s ledger — every Last-Warm-Day ever kept, who lit what and who wept where. Forty years of entries that end "and the stage stayed dark." Tonight\'s entry is going to need a WIDER page.' },
  ],
  'npc.solarium_hall_festival': [
    { speaker: 'TROUPE PLAYER', text: 'A toast — to the relit Solar, to the lit stage, and to the apprentice who fetched the sun up out of a flood spark by spark. The company drinks to you FIRST tonight. House rule, as of tonight.' },
  ],

  // --- Sunvault Climb ----------------------------------------------------------
  'sign.sunvault_welcome': [
    { text: 'THE SUNVAULT CLIMB. The old garden-roads rise toward the stars. Mind the overgrowth — it minds you back.' },
  ],
  'sign.sunvault_vines': [
    { text: 'The bridge of sun-vines died with the long night. Shut flowers, forty years. A pocket of daylight would wake them.' },
  ],
  'npc.sunvault_terracer_after': [
    { speaker: 'BEL', text: 'The beds grow toward the boundary vines now, did you notice? The garden knows what\'s coming up the road. Gardens always do.' },
  ],
  'npc.sunvault_wayfarer': [
    { speaker: 'RESTING WAYFARER', text: 'I\'ve walked every lit road in Vesperholm, and this stretch is the kindest of the lot — gold underfoot, stars ahead, and the climb gentle enough to think on. Rest a while. The eighth Lumenary keeps; it has kept for years.' },
  ],
  // The walkthrough's vine-tender line, verbatim.
  'npc.sunvault_vine_tender': [
    { speaker: 'VINE-TENDER', text: 'Forty years shut, and your little pocket of daylight woke them like they\'d only dozed. ...Maybe nothing\'s gone for good. Maybe it\'s all just waiting for the right lamp.' },
  ],
  'npc.sunvault_skywatcher_after': [
    { speaker: 'TAM', text: 'The dome\'s ahead, the densest sky in Vesperholm above it. Walk in soft — the whole town is listening to the stars come home.' },
  ],
  'sign.sunvault_helia': [
    { text: 'HELIA VAULT. A reliquary sealed by night-flowers. What the Solarium drowned, this door kept dry.' },
  ],
  'sign.sunvault_observatory': [
    { text: 'NORTH — NIGHTREACH OBSERVATORY. The watchers keep seven lamps for seven stars. Walk toward the brightest sky in Vesperholm.' },
  ],

  // --- Helia Vault ---------------------------------------------------------------
  'sign.helia_entry': [
    { text: 'The Helia Vault. What the Solarium could not keep dry, the keepers sealed here — and the seals are flowers.' },
  ],
  'npc.helia_far_vine': [
    { text: 'The great vine sleeps beyond your pocket of daylight — a chasm too wide for any light you can carry. Something here must bend the light.' },
  ],

  // --- The Coldfog detour (ZERO humour — every line elegiac) -------------------
  'sign.coldfog_marches': [
    { text: 'COLDFOG MARCHES. The lamps here have been put to sleep. Travellers are asked to let them rest.' },
  ],
  'sign.coldfog_boundary': [
    { text: 'Deep coldfog past this stone. No ordinary flame keeps. A warded ember walks where the fog is thickest.' },
  ],
  // The hooks' marsh-hermit line, VERBATIM.
  'npc.coldfog_marsh_hermit': [
    { speaker: 'MARSH-HERMIT', text: 'They didn\'t burn it. They didn\'t break it. They just... turned the light down, lantern by lantern, until the whole fen forgot it was ever lit. Kindest thing, they said. Kindest thing.' },
  ],
  // Posted by the Hollowing — courteous, awful.
  'sign.coldfog_works': [
    { text: 'HOLLOWFEN STILLWORKS. Every lamp within is resting. The Wardens of the Quiet ask that you not wake them.' },
  ],
  'sign.coldfog_beacon': [
    { text: 'WEST — DROWNLIGHT BEACON. The light that kept the fen-road drowned in its own keeping. No keeper answers.' },
  ],
  'sign.coldfog_backdoor': [
    { text: 'NORTH-WEST — NIGHTREACH, BY THE FOG ROAD. Short, dark, and wrong. The stars go the long way round.' },
  ],
  'npc.coldfog_quiet_camp': [
    { text: 'Two bedrolls, rolled square. The fire-ring is swept. A lantern stands where a hand left it, wick cold. Nobody hurried. That is somehow the worst of it.' },
  ],
  'npc.hollowfen_door': [
    { text: 'The seam of the door holds no handle. A thin grey light breathes under it — a gap only a glimmer-step could thread.' },
  ],
  // The hooks' husk-keeper line, VERBATIM — the sexton among graves.
  'npc.hollowfen_husk_keeper': [
    { speaker: 'HUSK-KEEPER', text: 'Every lamp in here is sleeping, not dead. That\'s the horror of it — and the mercy he believes in. One day the whole sky\'s meant to look like this room.' },
    { speaker: 'HUSK-KEEPER', text: 'I dust the collars. Somebody should. Whatever you think of the work... they were LAMPS, once. They are owed a keeper.' },
  ],
  'npc.hollowfen_engine': [
    { text: 'The null-engine: a bell of held dark on cradle-pipes, polished like a font. The gauge on the casing rests at zero, brass-rimmed and lovingly kept — a font, not a weapon, by every line of its making. That is the part that follows you out.' },
  ],
  'npc.drownlight_door': [
    { text: 'The door has swollen shut against its frame. Salt and years hold it better than any lock. High above, the lamp room keeps its dark.' },
  ],

  // --- Nightreach Observatory ----------------------------------------------------
  'sign.nightreach_welcome': [
    { text: 'NIGHTREACH OBSERVATORY. The sky is closest here. Walk softly — the watchers are counting.' },
  ],
  'sign.nightreach_walk': [
    { text: 'THE ASTRAL WALK. Seven watch-lamps for seven stars. Lit in the order they came home: ember-light first, sun-light last.' },
  ],
  'sign.nightreach_fogroad': [
    { text: 'EAST — THE FOG ROAD. Short, dark, and wrong. Only a warded flame holds the coldfog off.' },
  ],
  'sign.nightreach_lanternway': [
    { text: 'SOUTH — THE LANTERNWAY. Every lit road in Vesperholm meets at the Waystone.' },
  ],
  'npc.watch_lamp_unstruck': [
    { text: 'The first watch-lamp waits, polished and cold. Its wick wants the old watcher\'s striker — the one lost on the Sunvault road.' },
  ],
  'npc.watch_lamp_cold': [
    { text: 'This lamp keeps its place in the order. An earlier watch-fire is still dark.' },
  ],
  // C4 — Fenn's placements around lamp 5.
  'npc.fenn_waits': [
    { speaker: 'FENN', text: 'Go on with your lamps, child — I\'ll keep the frost-lamp\'s place till you reach it. Some things are better lit together.' },
  ],
  'npc.fenn_after': [
    { speaker: 'FENN', text: 'I\'ll watch from here, under the best sky in Vesperholm. When the eighth lights... look south a moment, would you? An old man would like to think you knew he saw it.' },
  ],
  // A5 — Wren's placements around lamp 6.
  'npc.wren_waits': [
    { speaker: 'WREN', text: 'I\'m not lighting it without you, so you may as well hurry up with lamp five.' },
  ],
  'npc.wren_nightreach_after': [
    { speaker: 'WREN', text: 'One lamp left, one star left, one of us still pretending they\'re not nervous. Go on — Nessa\'s waiting at the seventh with that telescope of hers, and I don\'t think it\'s pointed at the sky.' },
  ],
  // B4's threshold — Nessa at the seventh lamp, before the naming.
  'npc.nessa_at_seven': [
    { speaker: 'NESSA COLE', text: 'The seventh lamp is yours to light, Wayfarer. And then... there is something I have been watching grow on the mountain, and the time for watching it alone is over.' },
  ],
  'npc.junior_watcher_b_after': [
    { speaker: 'OS', text: 'Lira\'s charting the sky as it comes back, you know. First watcher in forty years with something NEW to write. Don\'t tell her I said it was brilliant. She logs compliments.' },
  ],
  'npc.junior_watcher_working': [
    { speaker: 'LIRA', text: 'The Sunvault terrace, our roof past the scree — and the Coldfog cairn only if your nerve runs that deep; the chart finishes without it. Look PROPERLY. Long enough to be cold. I\'ll know if you skimmed.' },
  ],
  'npc.junior_watcher_after': [
    { speaker: 'LIRA', text: 'The chart\'s away to the Waystone and my name\'s on the pressing. ...The senior watchers asked for a COPY. I have written that down in the ledger nobody reads, twice, in capitals.' },
  ],
  // The Star-vigil's keeper, after the watch is stood.
  'npc.star_vigil_warden_after': [
    { speaker: 'VIGIL WARDEN', text: 'Seven lamps burning on the steps, and the eighth row waiting. The town has watched half its life for this night, Wayfarer. We can watch a little longer — that is what watching IS.' },
  ],
  'npc.nightreach_watcher_steps_a': [
    { speaker: 'OLD WATCHER', text: 'I held the Storm-watcher\'s lamp for thirty years before it lit. People ask was it worth the holding. They have never once had to ask anyone whose lamp is LIT.' },
  ],
  'npc.nightreach_watcher_steps_b': [
    { speaker: 'WATCH KID', text: 'I\'m the eighth row\'s runner. When the last star comes home I run the steps ringing the little bell, fast as anything. I\'ve practised the route nine hundred times. Tonight could be the night. It could ALWAYS be the night.' },
  ],
  'npc.nightreach_festival_a': [
    { speaker: 'WATCHER', text: 'Eight lamps on the steps. Eight stars in the sky. I keep counting them over, the way you count children home — and they keep all being there.' },
  ],
  'npc.nightreach_festival_b': [
    { speaker: 'WATCHER', text: 'The Crown is closed. My grandmother kept this vigil, and hers, and not one of them saw the sky finished. I shall be UNBEARABLE about having been here. I have earned it.' },
  ],
  // The naming lands on a person (requires flag:great_null_known).
  'npc.nightreach_witness': [
    { speaker: 'TOWNSWOMAN', text: 'Nessa swung the great telescope at the MOUNTAIN. In thirty years she has never once pointed it below the sky. I didn\'t hear what she told you... and I find I keep standing nearer the lamps anyway.' },
  ],

  // --- Nightreach Lumenary --------------------------------------------------------
  'npc.nessa_not_ready': [
    { speaker: 'NESSA COLE', text: 'Not yet, Wayfarer. Seven watch-fires for seven stars — the walk is lit in the order they came home, and the eighth is not asked for over dark lamps. I will be here. I am always here.' },
  ],
  'npc.nessa_keeping': [
    { speaker: 'NESSA COLE', text: 'The walk is yours; the order keeps itself if you let it. Ember-light first, sun-light last. ...I will know each one the moment it takes. I always do.' },
  ],
  'npc.nessa_cole': [
    { speaker: 'NESSA COLE', text: 'Seven lamps. You know what I showed you on the terrace, and you came down the walk steady anyway. Good. Steadiness is most of what the dream-hours respect.' },
    { speaker: 'NESSA COLE', text: 'When you are ready, step to the dais. The eighth star has waited longest of all — and after tonight, I would not make it wait politely much longer.' },
  ],
  'npc.nessa_after': [
    { speaker: 'NESSA COLE', text: 'The Crown is whole, and the Penumbra is parting — my charts have never once shown me THAT. The Crossroads\' four inward roads will carry you to the Spire when you are ready.' },
    { speaker: 'NESSA COLE', text: 'Remember harder than he has forgotten, Wayfarer. And when it is done... come back one clear night. I will show you eight constellations from this chair, and we will not say anything at all.' },
  ],
  'npc.nightreach_hall_keeper': [
    { speaker: 'NIGHT-CLERK', text: 'The star-ledger: every watch ever kept under this dome, every star lost and every star come home. The "lost" column has had forty years of custom. I have ruled a fresh page for tonight, just in case. ...I rule one every night. Just in case.' },
  ],
  'npc.nightreach_hall_festival': [
    { speaker: 'WATCHER', text: 'The eighth watch-lamp lit ITSELF. I was here. I saw the wick take with no hand near it — the sky reached down and kept its own vigil. I shall be telling this for the rest of my life, and it will never once need improving.' },
  ],

  // --- Nightreach inn ("The Long Watch") + home ------------------------------------
  // The cluster's ONE permitted dry line (builder-sanctioned copy).
  'npc.nightreach_inn_guest': [
    { speaker: 'TIRED GUEST', text: 'Eight years I\'ve kept the quietest watch in Vesperholm, and the sky saves all its history for the week I booked off. Wake me if the dawn comes in.' },
  ],
  'npc.nightreach_inn_watcher': [
    { speaker: 'OFF-SHIFT WATCHER', text: 'Dawn-watch is the kind one — nothing ever happens at dawn-watch. That used to be a sad joke. The way things are going up there, it is about to become a SCHEDULING problem, and I could not be happier about it.' },
  ],
  'npc.nightreach_home_elder': [
    { speaker: 'LENS-GRINDER', text: 'I ground the dome\'s first lens, child — a year of my hands in that glass. They tell me what it sees these days, lamp by lamp coming home, and I polish my spectacles like it\'s the same work. It IS the same work.' },
  ],
  'npc.nightreach_home_kid': [
    { speaker: 'WATCHER KID', text: 'I keep my own chart — paper, under my pillow. Seven stars inked in and one space saved. The space is the IMPORTANT part. Everyone says so. I said it first.' },
  ],

  // --- The Crossroads' Nightreach spoke (W4's gate pair) + R5's hung chart ---------
  'sign.crossroads_nightreach': [
    { text: 'NORTH-WEST — THE NIGHTREACH SPOKE. Dark until the Lunar Gleam stands: the last spoke lights when the last lamp does.' },
  ],
  'npc.waykeeper_nightreach_gate': [
    { speaker: 'WAYKEEPER', text: 'The north-west spoke sleeps yet, friend — its lamps answer the Lunar, and the Lunar has not come home. When the watchers\' star stands up, this road will light itself the same hour. Last spoke of my Round. I keep its wicks trimmed anyway.' },
  ],
  'npc.waykeeper_chart_hung': [
    { speaker: 'WAYKEEPER', text: 'Forty years of guesswork charts, and now the true sky hangs on the Waystone where every road can see it. Travellers stop and look UP now, before they pick a direction. That is the whole Lanternway, working.' },
  ],

  // ===========================================================================
  // CENTRAL / ENDGAME (05-central-endgame). The threshold register holds from
  // the Penumbra inward: sincere, elegiac, ZERO humour — the hub's warmth is
  // the one bright counterweight (and Wren's f1 line is the ONE wry-warm beat).
  // ===========================================================================

  // --- Vesper Crossroads — the endgame hub stages ------------------------------
  'sign.crossroads_spire_open': [
    { text: 'THE INWARD ROAD — NOW OPEN. Eight braziers stand LIT around the fog-gate, one for each constellation. Beyond: the Penumbra Ring, and the Umbral Spire. Rest first. There is no bed past this stone.' },
  ],
  'npc.fenn_counsel_after': [
    { speaker: 'FENN', text: 'I am exactly where I mean to be, child: at the centre of every road you ever walked, watching the centre of the sky. Go well. Remember loudly.' },
  ],
  'npc.waystone_kid_trail': [
    { speaker: 'WAYSTONE KID', text: 'Did you see it?! It does the lamps in ORDER — north-west first, then across, then down. Like rounds! Like it\'s TENDING them! Follow the flickers round the ring!' },
  ],
  'npc.waystone_kid_trail_done': [
    { speaker: 'WAYSTONE KID', text: 'You FOUND it! The little lamp-kin! The Waykeeper says they used to follow the lamp-tenders\' rounds in the lit years — and now one follows YOU. That\'s the best thing that has ever happened at this crossroads. I\'m counting.' },
  ],
  'npc.dusk_lamp_quiet': [
    { text: 'A waystation dusk-lamp, brass-capped and patient. Its flame burns small and steady — exactly as a well-kept flame should.' },
  ],
  'npc.lampling_shy': [
    { text: 'The dusk-lamp burns plain and a little lonely. Whatever warmed its glass has tucked itself deep into the wick-light to sulk — it will not show itself again until you have won {remaining} more battles, and it has decided you meant no harm.' },
  ],
  'npc.lampling_after': [
    { text: 'The dusk-lamp burns bright and easy now. Whatever it was hosting has found a better lamp to live in — yours.' },
  ],
  'npc.waykeeper_round_done': [
    { speaker: 'WAYKEEPER', text: 'The chart on the stone, four festivals over the inn hearth, and my old Way-lamp in a Wayfarer\'s satchel. The Round is kept, child — better kept than I ever managed it. Walk far. The roads will tell me how you\'re doing.' },
  ],

  // --- The Penumbra Ring (the threshold register: awe and held breath) --------
  'sign.penumbra_ascent': [
    { text: 'THE NINTH LANTERN. The road up is starlight or nothing. Lamps out of respect; hearts lit out of spite.' },
  ],
  'sign.penumbra_starwell': [
    { text: 'EAST — THE STARWELL. Where a star fell and did not go out. Step soft on the dark.' },
  ],
  'npc.penumbra_tended_row': [
    { text: 'Two null-lanterns, tended and swept, holding no light with great care. Someone still walks this row.' },
  ],
  'npc.penumbra_snuffed_shrine': [
    { text: 'A wayshrine of the old inward road. Its lamp was not broken — it was put out, gently, the way you would close a sleeping kin\'s door.' },
  ],

  // --- Starwell (the SILENCE register) -----------------------------------------
  'npc.starwell_still': [
    { text: 'The pool lies flat and shining. Whatever rose from it has sunk deep again; the starlight will not give it up for {remaining} more battles yet.' },
  ],
  'npc.starwell_after': [
    { text: 'The well holds only starlight now — and holds it gladly. The water is warm.' },
  ],
  // THE NULL-WORKS POOL — Nullmajor #150, the great dark made kin (post-dawn
  // set-piece on umbral_spire_f2; the Còr-mercy register: woken gently, never
  // destroyed). Cooldown + after lines for script.nullworks_nullmajor.
  'npc.nullworks_still': [
    { text: 'The pool of gathered dark lies still. What sank back into it is resting — the old null will not rise again for {remaining} more battles yet.' },
  ],
  'npc.nullworks_after': [
    { text: 'The null-pool is only water now, holding the morning upside down. Somewhere in your lamp, the dark Còr made is finally being kept instead of feared.' },
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
    { speaker: 'MERRIN', text: 'Thirty years of wicks, and yours are the first I\'ve seen that made the watching look worth it. ...I still think the dark is kinder. I\'m just less sure it\'s KINDEST.' },
  ],
  'npc.hollowing_acolyte_b_after': [
    { speaker: 'TACE', text: 'The alcoves are warm, whatever you think of us. We were never cruel — only tired. ...Dock gently at the top, traveller. He is the tiredest of us all.' },
  ],
  'npc.hollowing_acolyte_c_after': [
    { speaker: 'IVORWEN', text: 'Go on up, dear — and take the stair slowly, it\'s steeper than it looks. ...Four winters. I would have kept a fifth. Fancy me forgetting that, of all things.' },
  ],
  'npc.hollowing_acolyte_d_after': [
    { speaker: 'HARL', text: 'The gallery is yours; I\'ll not test a flame twice. ...Eight lamps on eight doorposts, and I never once knocked. If the sky changes, maybe I will.' },
  ],
  'npc.hollowing_acolyte_e_after': [
    { speaker: 'SEFA', text: 'The wind\'s picked up. She always said that meant the sky was paying attention. ...The north roads, Wayfarer. First. You promised the beaten half of me.' },
  ],

  // The alcove sleepers (read triggers; the dawn flips them).
  'npc.spire_sleeper': [
    { text: 'A drained kin sleeps in the alcove, tucked under a worked cloth, its light banked to the faintest ember. Someone has set a cushion under its head. Someone visits.' },
  ],
  'npc.spire_sleeper_awake': [
    { text: 'The alcove is empty — blanket folded, cushion squared away. Small bright footprints lead out toward the morning, in no particular hurry, the way you walk when you know the way home.' },
  ],
  'sign.spire_lantern': [
    { text: 'THE NINTH LANTERN — HIGH GALLERY. In the lit years, the keepers rested here and read the sky before the last stair. The sky is back. Rest. Read it.' },
  ],
  'npc.spire_shaft_dark': [
    { text: 'The spire\'s open core falls away into the dark. An old hoist-lamp hangs at the lip, unlit — the starlight will not bear you down until someone above kindles the line.' },
  ],
  'npc.dawn_road_waits': [
    { text: 'A road descends the summit\'s east shoulder, kept and cobbled, vanishing into the dark below. The old keepers called it the dawn road. It is waiting for the name to be true again.' },
  ],

  // Còr at the summit — the belt-and-braces interact (the band fires first) and
  // the man after: undone, not destroyed; remembering.
  'npc.cor_summit': [
    { speaker: 'CÒR', text: 'A moment more, apprentice. The sky is very fine tonight — your doing — and I have learnt to take the fine moments slowly. We will speak when you are ready. We have all the dark there is.' },
  ],
  'npc.cor_after': [
    { speaker: 'CÒR', text: 'I find I keep listing them — the fair, the bell, the kites, the bread. Twenty years of careful forgetting, undone in one evening by somebody else\'s lamp. ...Thank you. I am told that is the customary thing to say to a light, and I am out of practice.' },
  ],

  // The Keylumen's withdraw line (cooldown 0 — it cannot strand; kept for the
  // op's contract and the one frame where a miss needs answering).
  'npc.keylumen_waits': [
    { text: 'The white-gold light folds back into the dais — not gone, not refused. Waiting. Raise your lamp and ask again; the Keystar has waited years, and will not begrudge you a breath.' },
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
    { text: 'TIDEGLASS CAVERN. The sea smoothed it; lamp-light finishes it. Mind the black water — the tide under the glass keeps its own hours.' },
  ],
  'sign.tideglass_nook': [
    { text: 'A lampwright\'s waymark, cut small and sure into the glass: "THE GLASS REMEMBERS EVERY LIGHT IT IS SHOWN. SHOW IT GOOD ONES."' },
  ],
  // The wreck-lamp before the old fisher's tale is heard (S3's gate).
  'npc.tideglass_wrecklamp_cold': [
    { text: 'An old boat lies broken in the rocks, her stern-lamp wedged where she split — guttered, with years of salt on the glass. It is somebody\'s tended story, and you do not know it yet.', style: 'narrate' },
  ],
  'npc.tideglass_wrecklamp_lit': [
    { text: 'The wreck-lamp burns steady in its glass throat, the way it burned three days for a drowning man forty years ago. The debt is paid. The light never counted it.', style: 'narrate' },
  ],
  // The verse plaque's inert twin (before the wreck-lamp burns).
  'sign.tideglass_verse': [
    { text: 'A glass hood over a cold stern-lamp, etched line on line — lampwright\'s marks, worn soft by salt. In the dark they refuse to be read.' },
  ],
  // The relay's wrong-order/cold line (shared by all three lenses).
  'npc.tideglass_lens_cold': [
    { text: 'A standing lens of sea-glass, taller than you, cold to the lamp. Your light slides off it and goes nowhere. The verse named an order, and this is not its turn.', style: 'narrate' },
  ],
  // The stair seam, sealed until lens C rings (warp blocked_ref).
  'npc.tideglass_stair_sealed': [
    { text: 'A seam in the glass breathes cold air. It is not open.', style: 'narrate' },
  ],
  // The Dusk Hour's withdrawal (cooldownRef — §7 verbatim).
  'npc.three_dusk_resting': [
    { text: 'The lenses hold your own lamp-light and nothing else. The Dusk Hour has folded itself back into the seam between the days — win {remaining} more battles, and the glass may warm to you again.' },
  ],
  // The netmender, once her rumour is told (consumes flag:three_dusk_rumour).
  'npc.netmender_hours_after': [
    { speaker: 'NETMENDER', text: 'Still singing of an evening, that cliff — low, like a lamp being hummed to. You went and listened, didn\'t you. I can tell. You stand like somebody who has been NEAR something.' },
  ],

  // --- Site II: the Hourfold (North) — Midnight in the deep ice --------------
  // The sealed fold (host warp blocked_ref — §5 verbatim).
  'npc.hourfold_sealed': [
    { text: 'The fold is shut fast with ice that has opinions about visitors. Something in there is not ready to be looked at.', style: 'narrate' },
  ],
  // The aurora names the snuffing order (§5: east, the water-ice, west).
  'sign.hourfold_aurora': [
    { text: 'A watcher\'s waymark, cut into the blue ice and glazed by forty winters: "READ THE SKY BEFORE THE SHELF. The ribbon kneels east, then over the water-ice, then west."' },
  ],
  // The Unstruck Toll's wrong-order refusal (shared by all three braziers).
  'npc.hourfold_flame_leans': [
    { text: 'The vigil-brazier burns blue-white and certain. As the snuffer rises, the flame leans away from it — not this one, not yet. The aurora named an order.', style: 'narrate' },
  ],
  // The Still Hour's withdrawal (cooldownRef — §7 verbatim).
  'npc.three_midnight_resting': [
    { text: 'The fold is only ice and aurora tonight. Midnight has kept its watch longer than anyone alive; it can outlast you without noticing — {remaining} battles won, and it may consent to be witnessed again.' },
  ],
  // The aurora-watcher, once her rumour is told (consumes flag:three_mid_rumour).
  'npc.aurorawatcher_after': [
    { speaker: 'WATCHER', text: 'The fold still queues the sky, and now you know why. Stand a moment before you go down to it. That is all the watch has ever asked of anyone — that the dark be WITNESSED, not braved.' },
  ],
  // Ysolde, once the snuffer is handed over (consumes flag:three_mid_snuffer).
  'npc.ysolde_snuffer_after': [
    { speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'You carry the snuffer the way a tender should — like a lamp, not a tool. Put the vigil out gently, wanderer. The Still Hour has watched the putting-out of better flames than ours.' },
  ],

  // --- Site III: the Unrisen Stair (West) — the Dawn that waited -------------
  // The sealed stair (host warp blocked_ref — §6 verbatim).
  'npc.unrisen_sealed': [
    { text: 'A stair behind the seal, climbing toward nothing the sky currently offers. The basin before it is dry.', style: 'narrate' },
  ],
  // The basin before Lucan's phial is carried (trigger blocked_ref).
  'npc.three_dawn_basin_dry': [
    { text: 'A sun-basin of pale stone, bone-dry, set where a first light was meant to land. It is not waiting for water. It is waiting for morning — and it has the patience of masonry.', style: 'narrate' },
  ],
  // The sun-mirror flower before vine A blooms (trigger blocked_ref).
  'npc.unrisen_mirror_waits': [
    { text: 'A great flower of bronze and glass, petals shut, turned to face a sunrise that is not there. Nothing you carry is morning enough to open it — not yet.', style: 'narrate' },
  ],
  // The far vine's lock, narrated on every early attempt (band blocked_ref).
  'npc.unrisen_far_vine': [
    { text: 'The far sun-vine sleeps across the black water, shut tight. The basin\'s cupful of daylight pools where it was poured — it must be BENT here, the way the old gardeners bent it, before the far bank will believe in morning.', style: 'narrate' },
  ],
  // The east flight opens (the bloom_b band's ref).
  'npc.unrisen_stair_wakes': [
    { text: 'The bent daylight crosses the water ahead of you, and the far vine takes it: blooms, climbs, and lays itself open up the east flight like a road remembering it is one. Above, at the head of the stair, something stands facing east.', style: 'narrate' },
  ],
  // The Lost Hour's withdrawal (cooldownRef — §7 verbatim).
  'npc.three_dawn_resting': [
    { text: 'The basin stands dry and the stair unrisen. The Hour that has waited years for its morning can wait a little longer than you — {remaining} more battles won, and it may risk believing again.' },
  ],
  // Nessa, once her reading is shared (consumes flag:three_dawn_rumour).
  'npc.nessa_hours_after': [
    { speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'The bell that hasn\'t rung is still there, due west, under everything. I hear it most on clear nights. ...Go gently, Wayfarer. Whatever has waited that long for a morning deserves not to be startled.' },
  ],
  // Lucan, once the phial is given (consumes flag:three_dawn_phial).
  'npc.lucan_phial_after': [
    { speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'bittersweet', text: 'Forty years I kept that phial against a day worth spending it on, and the moment I hand it over the theatre feels LIGHTER. Pour it true, apprentice. First light is an entrance no one gets to make twice.' },
  ],
  // ===========================================================================
  // DAWNSTEAD — the post-game epilogue town (06-postgame, R2). Bittersweet-
  // warm; Còr never gloated over; the lamp a keepsake now, not a necessity.
  // ===========================================================================
  // Còr's standing lines at his lamp (pre-wick, and after it comes home).
  'npc.cor_lamp': [
    { speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'The star-tenders offered me a place again. I asked for a lamp instead — one lamp, kept properly, is a whole creed. Mind the wind for me; it is the only argument we have left, the wind and I.' },
  ],
  'npc.cor_lamp_after': [
    { speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'The wick draws well. Daylight in the braid of it — it will hold the first night of the new dark, when that comes. And it will come. ...Good. A lamp should have work ahead of it.' },
  ],
  // Fenn, the survey done — the mentor at rest.
  'npc.fenn_dawnstead_after': [
    { speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'No errands left, apprentice. None. I have checked twice, and the second check was for the pleasure of it. ...The sky\'s yours now. I\'m only out here watching how well it\'s kept.' },
  ],
  // Latched doors — everyone\'s out in the sun (no silent doors).
  'door.dawnstead_store': [
    { text: 'The store is latched, lightly — a chalked note on the shutter reads: "OUT. LOOK UP." Everyone\'s out in the sun.' },
  ],
  'door.dawnstead_cottage': [
    { text: 'The door is on the latch, the hearth inside cold for the first kind reason in years. Everyone\'s out in the sun.' },
  ],
  'door.dawnstead_home': [
    { text: 'The latch lifts a half-inch and stops — the same stiff latch as home, the same worn step. Nobody\'s in. On a morning like this, why would they be?' },
  ],
  // Signs.
  'sign.dawnstead_town': [
    { text: 'DAWNSTEAD — Tinderwick, by morning light. The lamps are resting. Let them.' },
  ],
  'sign.dawnstead_verge': [
    { text: 'The moths came out gold this morning. Nobody\'s seen the like. Catch one — they won\'t keep; nothing does. That\'s why you catch it.' },
  ],
  // The survey marks before Fenn asks for them (the blocked_ref tease).
  'sign.dawnstead_blooms': [
    { text: 'Dawn-blooms, wide open to the sky. Something has been feeding here — something with gold dust on its wings.' },
  ],
  // The first-dawn festival folk (Arc E capstone — belonging, not conquest).
  'npc.dawnstead_piper': [
    { speaker: 'PIPER', text: 'I know eight festival tunes and every one of them leans on the dark somewhere. So this morning I\'m writing the ninth. It keeps coming out in major. I\'ve stopped fighting it.' },
  ],
  'npc.dawnstead_baker': [
    { speaker: 'BAKER', text: 'First batch proved by SUNLIGHT on the sill. Tastes the same, mind. Tastes completely different. Both true — have a heel of it, everyone else has.' },
  ],
  'npc.dawnstead_kid': [
    { speaker: 'KID', text: 'My gran says you carry a lamp EVERYWHERE. Why? The sky does it for free now... oh. OH. Were you the one who—? GRAN! GRAN, COME AND SEE WHO IT IS!' },
  ],

  // --- The Starfall Vigils (06-postgame · R3) ---------------------------------
  // The Dawnstead witness — points the player to Nightreach when the first
  // shard falls (requires flag:dawn, hidden once flag:starfall_begun).
  'npc.starfall_witness': [
    { speaker: 'WITNESS', text: 'Did you SEE it? Not a star going out — we\'ve all watched plenty of those. This one came DOWN. Shed itself, trailing gold, away off east.' },
    { speaker: 'WITNESS', text: 'Nightreach is beside itself. Watcher Oriel had the great eyepiece on it before it landed. Go up and ask her — she reads the sky for a living, and she\'s never read anything like THIS.' },
  ],
  // The blocked_ref on every Vigil-site host warp, until its reading is held —
  // the scar of starlight is visible post-dawn, sealed until read (the watchers' voice).
  'npc.vigil_scar_sealed': [
    { text: 'A seam of starlight, shut tight. Whatever fell here is waiting to be read first.' },
  ],
  // The kept placements — each Vigilant's plain line after their vigil is kept
  // (requires flag:vigil_<n>_kept, hidden once flag:starfall_crown swaps in the
  // re-runnable bout). Each points the player on along the chain.
  'npc.vigil_hearthfall_kept': [
    { speaker: 'WICK-MOTHER ESRA', text: 'Off you go, dear — the second fell east, under the hill where the moss has opinions. I\'ll sit with the morning a while. Seventy years of dusk; I\'ve earned a sunrise or two.' },
  ],
  'npc.vigil_grovefall_kept': [
    { speaker: 'OLD FOREMAN BRAMM', text: 'Third one went north — the wind\'s spare pocket, the watcher says. Mind the roost. ...And tell Otho he still exaggerates.' },
  ],
  'npc.vigil_stormfall_kept': [
    { speaker: 'ONDRA VAEL', text: 'The fourth fell west, where they kept the summer safe. Dress lighter than you did for me — and give Dame Solenne a proper bow; she taught everyone the bowing.' },
  ],
  'npc.vigil_sunfall_kept': [
    { speaker: 'DAME SOLENNE', text: 'The last rests in the marshes, where the water is learning to speak again. Go gently — and carry my regards to the warden who waits there. She has more than earned them.' },
  ],
  'npc.vigil_murkfall_kept': [
    { speaker: 'WARDEN MER', text: 'Carry the five up the mountain, Wayfarer. The old man has waited a long time to be allowed his best. The marsh and I will keep, until you have kept the last.' },
  ],
  // Dawnbrael's cooldownRef — the static catch withdrew with the next dark; it
  // returns with the next sunrise (no re-fighting the Round). cooldownBattles is
  // 0, so {remaining} never reads — the line is the re-approach hint only.
  'npc.dawnbrael_resting': [
    { text: 'The Ninth Lantern stands quiet, the five shards still seated in its collar. Dawnbrael drew back into the morning when you faltered — raise the lamp again, and it will answer with the next light.' },
  ],
  // Oriel's terrace re-reads — the chain's noticeboard. Lost the thread? She
  // repeats the current reading, verbatim, slightly wearily. Flag-disjoint
  // placements (the Fenn-waystone pattern) carry exactly the held reading.
  'npc.oriel_read_1': [
    { speaker: 'WATCHER ORIEL', text: '...The first one again? Very well. The first came down in the south — where the first lamp learned its name. Climb past the lantern that taught the sky to answer; it fell on the bluff above, where even the gulls go quiet.' },
  ],
  'npc.oriel_read_2': [
    { speaker: 'WATCHER ORIEL', text: 'The second, then. It went to earth in the east — under the hill, where the wood keeps its own weather and the moss has opinions. Bring a light. Bring patience. The grotto has both, and shares neither.' },
  ],
  'npc.oriel_read_3': [
    { speaker: 'WATCHER ORIEL', text: 'The third went north, into the wind\'s spare pocket — the roost where storms go when they\'re off duty. Take the kite. Take a coat. Retrieve your own hat; I shan\'t fetch it.' },
  ],
  'npc.oriel_read_4': [
    { speaker: 'WATCHER ORIEL', text: 'The fourth fell where summer was put away for safekeeping — the high terraces that remembered daylight before the rest of us believed in it again.' },
  ],
  'npc.oriel_read_5': [
    { speaker: 'WATCHER ORIEL', text: 'The last fell where the water forgot how to speak. It is learning again — go gently into the murk; some of what you\'ll meet is still waking. And one of them has waited a long time to greet you.' },
  ],
  'npc.oriel_carry': [
    { speaker: 'WATCHER ORIEL', text: 'Five shards, five vigils kept. The sixth never fell — it\'s been waiting where the night ended, at the top of the mountain. Carry the five up, the warden of the marshes said, and ask the old man what he sees. ...So go on. Ask him.' },
  ],
  'npc.oriel_epilogue': [
    { speaker: 'WATCHER ORIEL', text: 'Star-tender, is it now. I read the falls; you kept them. ...The sky has all its pieces back, and a name to call you by. Not a bad night\'s watching, between us.' },
  ],
  // The three Vigilants who climbed ahead, waiting at the Ninth Lantern before
  // the Round (requires flag:vigil_5_kept, hidden once flag:starfall_lesson).
  'npc.vigil_ondra_summit': [
    { speaker: 'ONDRA VAEL', text: 'We came up to watch the old man\'s lesson. The watching turned into a queue. Raise the lamp at the lantern when you\'re ready — and don\'t keep us waiting; it\'s cold up here.' },
  ],
  'npc.vigil_solenne_summit': [
    { speaker: 'DAME SOLENNE', text: 'The finest house I have ever played, and the best lit. Three of us, then the old man — back to back, no interval. Touch the lantern and the curtain rises.' },
  ],
  'npc.vigil_mer_summit': [
    { speaker: 'WARDEN MER', text: 'He has waited forty years for this lesson. So have I, in a way. When your lamp is steady, ask the lantern — we\'ll be right behind you, every step.' },
  ],
};

const FALLBACK: DialogueLine[] = [{ text: '...' }];

/** Resolve a dialogue ref to its pages, or a quiet fallback if unknown. */
export function getDialogue(ref: string | undefined): DialogueLine[] {
  if (!ref) return FALLBACK;
  return DIALOGUE[ref] ?? FALLBACK;
}
