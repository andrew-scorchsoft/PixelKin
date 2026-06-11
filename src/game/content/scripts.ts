/**
 * Cutscene script registry — keyed by the `ref` cutscene/script triggers use
 * (EventTrigger.ref, e.g. 'script.intro_mentor'). Each is an ordered list of
 * CutsceneStep the CutsceneRunner interprets. Adding a scene is a data edit here.
 */
import type { ScriptRegistry } from './types';

export const SCRIPTS: ScriptRegistry = {
  // --- The opening: the satchel errand at the Vesper Crossroads -----------------
  // C1 (walkthrough/01-south §2) is now a small LOOP, not a tile-touch: the north
  // gate-warden turns you back (it's dangerous out there), everyone points EAST to
  // Star-tender Fenn at the Crossroads waystone, Fenn has left his satchel on the
  // Tinderwick store counter, and the lamp-and-starter ceremony happens at the
  // waystone once you bring it out to him. Warm, unhurried, never a "Professor".

  // The north gate, pre-starter: the warden (posted in the gap at (14,1)) spots the
  // player on the open column (13,1), warns them off, and walks them back a step.
  // The trigger band is hidden_when 'flag:has_starter'; the warden swaps for a
  // well-wisher (gatewarden_post) the moment the Wayfaring begins.
  'script.gate_warden': [
    { op: 'emote', actor: 'gatewarden_pre', emote: 'alert' },
    { op: 'face', actor: 'gatewarden_pre', facing: 'left' },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Whoa there, apprentice! Not one step up the coast road without a kin of your own at your side — the grass out there is crawling with wild ones since the dusk.' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Star-tender Fenn was asking after you this very morning. He walked out EAST, along the Lanternway — the Crossroads waystone wanted tending.' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Go on, find him. He had that look about him. The one that means it is YOUR turn.' },
    { op: 'move', actor: 'player', to: { tx: 13, ty: 3 } },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'gatewarden_pre', facing: 'down' },
  ],

  // Crossing into the waystone plaza for the first time: Fenn hails the player
  // from across the clearing so there's no "who do I talk to?" beat to fumble.
  'script.fenn_wave': [
    { op: 'emote', actor: 'fenn_pre', emote: 'alert' },
    { op: 'cameraFocus', actor: 'fenn_pre', ms: 500 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Ho — over here, apprentice! By the waystone!' },
    { op: 'cameraReset', ms: 500 },
  ],

  // Fenn at the waystone: delight, then the small ask — his satchel, forgotten on
  // the Tinderwick store counter, with the whole Wayfaring packed inside it.
  'script.fenn_crossroads': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'There you are. The sky lost another light in the small hours — I felt it go. So I came out to tend the waystone lamp... and to wait for you.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'It is time for your Wayfaring, at last. I have everything you need right here in my—' },
    { op: 'emote', actor: 'fenn_pre', emote: 'sweat' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: '...my satchel. Which is sitting on the counter of the Tinderwick store, sure as sunrise used to be. Old hands, old head.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Run it out to me, would you? Back west along the Lanternway — the lamps hold that road safe. Your Wayfaring can spare you one small errand first.' },
    { op: 'setFlag', flag: 'flag:fenn_errand' },
  ],

  // The satchel on the store counter (an item_cache placement in tinderwick_shop;
  // appears once Fenn asks, vanishes once taken).
  'script.take_satchel': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fenn_satchel', count: 1 },
    { op: 'say', text: "The Star-tender's field-satchel, heavier than it looks. Took FENN'S SATCHEL!" },
    { op: 'setFlag', flag: 'flag:has_satchel' },
  ],

  // The ceremony at the waystone: the satchel comes home, and out of it come the
  // two things every Wayfarer leaves with. The cosy bed holds; the grave notes ride
  // portraits, not music changes — warmth held, dread only in Fenn's face.
  'script.intro_mentor': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'My satchel — and my apprentice. Both delivered by the same pair of feet. A tidy omen, that.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Now. Every Wayfarer leaves with two things, and they have been riding in this old bag all along.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'The first — a lamp, to carry the light home. Take it. Your vesperlamp.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.28, ms: 240 }, // a warm bloom as the lamp kindles
    { op: 'giveItem', item: 'vesperlamp', count: 1 },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 600 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'It does more than light the road. Raise it toward a weary wild kin, and it coaxes them in to rest — every friend you make rides safe inside its glow.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'And the second — a friend, to share the walk through the dark. Go on. Choose.' },
    { op: 'giveStarter' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Mind you tend them both, and they will tend you. And fitting, is it not — every Wayfaring in Vesperholm begins at a crossroads.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Back along the Lanternway with you now. Catch a second friend in the verge grass by the north gate — tire a wild kin in battle first, then raise your LAMP and ask kindly.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Stop in at the store as you pass — the keeper holds a Wayfarer\'s kit for you. Town custom.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Then call on Brisa at the Lumenary — the tall lantern-hall up the square. She keeps the Ember constellation, and she will start you toward your first Gleam.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'And if an old word ever slips you — kin, Gleam, Lumenary — ask your lamp. It keeps a little book of LORE for exactly that.' },
    { op: 'setFlag', flag: 'flag:has_vesperlamp' },
    { op: 'setFlag', flag: 'flag:has_starter' },
  ],

  // (The first Gleam moved from the Lumenary hall to the BEACON TOP —
  // script.beacon_battle below; the hall now stages Brisa's quest beats.)

  // The Beacon's wick-tenders — SIGHT trainers on the stair floors.
  'script.beacon_keeper_a': [
    { op: 'say', speaker: 'TANSY', text: 'A climber! Brisa said the key might come home today. Floor rule, though — every flame is tested.' },
    { op: 'battle', trainer: 'beacon_keeper_a' },
    { op: 'say', speaker: 'TANSY', text: 'Steady enough for the stairs. Up you go!' },
    { op: 'setFlag', flag: 'flag:beacon_keeper_a_beaten' },
  ],
  'script.beacon_keeper_b': [
    { op: 'say', speaker: 'COLE', text: 'Tansy let you past? Then one test left before the lantern room. Mine is not so gentle.' },
    { op: 'battle', trainer: 'beacon_keeper_b' },
    { op: 'say', speaker: 'COLE', text: 'Well burned. The lantern room is just above — Brisa is already there.' },
    { op: 'setFlag', flag: 'flag:beacon_keeper_b_beaten' },
  ],

  // Second Lumenary (pearlmoor_lumenary): the player crosses the sea-shrine chamber to
  // old ferryman Reyl Wash, hears him out, battles him, and on victory relights the Tide
  // constellation — the second Gleam, wrapped in the Tide-blessing festival (Arc E). The
  // trainer's reward_flags ('gleam:tide', 'crown_south') AND reward_abilities ('tidecall')
  // are applied by the BattleScene on a win; here we add the diegetic Gleam cue and the
  // closing beat handing over the Lantern Gift.
  'script.lumenary_pearlmoor': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'reyl', facing: 'down' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'Came on foot, did you — no need of the tides to reach my door. Good. The light should be free to all who seek it.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'Now. Read the water with me, Wayfarer, and we shall see if the sea will listen to you.' },
    { op: 'battle', trainer: 'lampwarden_pearlmoor' },
    // The second Gleam, wrapped in the Tide-blessing — same minor→major payoff, in a
    // cool moon-on-water key rather than Tinderwick's ember-warm one.
    { op: 'musicFade', ms: 500 },
    { op: 'tint', color: '#4fb4ff', alpha: 0.36, ms: 600 },
    { op: 'narrate', text: 'Reyl rings the moor-bell. Out on the black water, buoy after buoy answers — and overhead, the Tide remembers how to shine.' },
    { op: 'gleam', element: 'tide' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'proud', text: 'The Tide Gleam stands up over Pearlmoor again. And the Tidecall is yours — go on, ask the shallows to part. The harbour keeps its secrets for those who can cross.' },
  ],

  // --- The Causeway Bell (Pearlmoor's earned second Gleam; spine §5 shape #2) --
  // The Tide-blessing cannot begin until the Moor-bell rings, and the bell-rope
  // is in the netmender's keeping: Reyl's hook (hall) -> the net-floats errand
  // (Dimglass II) -> the rope -> the breakwater walk -> the bell. All data.
  'script.reyl_quest': [
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'So. The apprentice with the new Ember in their sky. I have ferried a hundred Wayfarers over this harbour, and I read a bond the way I read weather. Yours is nearly ripe for the testing.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'Nearly. Tides go out so they can come back — but the blessing waits on the moor-bell, and the moor-bell waits on you.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'grave', text: 'It has hung silent at the breakwater\'s end since the last storm carried its rope away. No bell, no Tide-blessing. No blessing, no bond-test. That is the order of things, and the sea keeps her orders.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'The NETMENDER on the quay splices the only rope fit to hang there. Ask her kindly — though I warn you, her temper went south with her floats in that same storm.' },
    { op: 'setFlag', flag: 'flag:q_south_bell' },
  ],

  // The netmender, floats home: the rope changes keeping (her swap stage runs this).
  'script.netmender_rope': [
    { op: 'say', speaker: 'NETMENDER', text: 'My floats! Every one of them — salt-bleached, sand-scoured, and SOUND. You walked the flats for a stranger\'s nets.' },
    { op: 'say', speaker: 'NETMENDER', text: 'Then the rope is yours to carry. I spliced it the winter the bell first went quiet, and I have waited on a steady pair of hands since.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bell_rope', count: 1 },
    { op: 'say', text: 'She lays a coil of salt-stiff rope across your arms. Received the MOOR-BELL ROPE!' },
    { op: 'say', speaker: 'NETMENDER', text: 'The moor-gate\'s unchained for you — south end of the quay, where the boards run out over the black water. Walk it to the end, hang the rope true, and ring it LOUD.' },
    { op: 'say', speaker: 'NETMENDER', text: 'And mind Maren and Cob out on the causeway. Net-hands the both of them, and bored. They will want a bout off you. Custom.' },
    { op: 'setFlag', flag: 'flag:q_south_has_rope' },
  ],

  // The breakwater's two net-hand SIGHT trainers (the 12->14 on-ramp to Reyl's 16).
  'script.net_hand_a': [
    { op: 'say', speaker: 'MAREN', text: 'Hold it right there, rope-runner! Causeway custom: every lamp that walks the moor-boards gets weighed.' },
    { op: 'battle', trainer: 'net_hand_a' },
    { op: 'say', speaker: 'MAREN', text: 'Weighed and found steady. The bell\'s been waiting longer than you have — get on.' },
    { op: 'setFlag', flag: 'flag:net_hand_a_beaten' },
  ],
  'script.net_hand_b': [
    { op: 'say', speaker: 'COB', text: 'Oi! Nobody rings MY bell without ringing me first. Nets up, Wayfarer!' },
    { op: 'battle', trainer: 'net_hand_b' },
    { op: 'say', speaker: 'COB', text: 'Hah — well hauled! Go on then. Ring it loud enough to reach the flats; Maren bet me a week of mending it can\'t be done.' },
    { op: 'setFlag', flag: 'flag:net_hand_b_beaten' },
  ],

  // The Moor-bell, rung at the shrine — the loop's payoff and the blessing's first
  // note. Quiet -> the bell -> the harbour answering: a small minor->major of its
  // own (the full festival swell waits on the Gleam; docs/world/cinematics.md).
  'script.ring_moorbell': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 500 },
    { op: 'silence', ms: 900 }, // the held breath before the bell
    { op: 'narrate', text: 'You hang the netmender\'s rope where the old one frayed, take the cold span in both hands — and pull.' },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.3, ms: 500 },
    { op: 'narrate', text: 'The moor-bell swings. Once. Twice. The sound rolls out flat and silver over the black water, the way it has not rolled in years.' },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'narrate', text: 'And the harbour ANSWERS. Buoy by buoy, mast by mast, lanterns kindle along the quay behind you — and somewhere among the boats, somebody starts to sing the going-out song.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'The Tide-blessing has begun. Reyl Wash will be waiting at his sea-altar.' },
    { op: 'musicCrossfade', key: 'dimglass-coast-a', ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // E — the Tide-blessing proper (post `gleam:tide`, banded on the quay forecourt):
  // Pearlmoor's festival, deliberately the COOL mirror of Tinderwick's warm fair —
  // open water, moonlight, the bell as its signature note, the new cool-tidal cue.
  'script.tide_blessing': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 500 },
    { op: 'silence', ms: 900 },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'narrate', text: 'Out at the breakwater\'s end the moor-bell is swinging again — and under it, new in the sky, the TIDE hangs over its own reflection.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.32, ms: 700 },
    { op: 'musicCrossfade', key: 'pearlmoor-blessing', ms: 1200 },
    { op: 'narrate', text: 'The blessing-boats put out in a slow lantern-line, moon on the water and a light on every bow. The whole quay is singing the going-out song — soft, and sure, and not at all sad.' },
    { op: 'say', speaker: 'QUAY ELDER', text: 'Tides go out so they can come back. Sing it home, child. Tonight, YOU are the rhythm it kept.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 1100 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // S1 "The Last Buoy Out" — the netmender, once the Tide stands and the player
  // can walk the water: three of her line went dark in the storm. Lit in order,
  // quay outward — the LAST buoy out is the one she frets for.
  'script.netmender_buoys': [
    { op: 'say', speaker: 'NETMENDER', text: 'Walking the moon-water now, are you. Then I have one more asking in me — and this one I cannot give anyone else.' },
    { op: 'say', speaker: 'NETMENDER', text: 'Three of my buoy-line went dark in the storm that took the rope. The flats south of here — you will know mine by the drowned wicks.' },
    { op: 'say', speaker: 'NETMENDER', text: 'Light them quay-outward, the way the line was laid: near one first, then the middle water, then the LAST BUOY OUT. That far one has been dark the longest, and I fret for it.' },
    { op: 'setFlag', flag: 'flag:q_south_buoys' },
  ],
  // The three buoys (Dimglass II, Tidecall water) — small, quiet relights.
  'script.buoy_first': [
    { op: 'narrate', text: 'The near buoy rocks on its chain, wick drowned and dark. You steady it and touch your vesperlamp to the well.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'It takes — a small stubborn flame in a glass throat. One. The line remembers where it was going.' },
  ],
  'script.buoy_second': [
    { op: 'narrate', text: 'The middle-water buoy lists with a belly full of storm-sand. You bail it with a cupped hand and lend it your flame.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Two. Behind you, the near buoy answers it across the dark water like a held note.' },
  ],
  'script.buoy_last': [
    { op: 'narrate', text: 'The last buoy out. Farthest from the quay, first into every storm — its glass is crazed and its chain sings with the swell.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.25, ms: 500 },
    { op: 'narrate', text: 'Three. The whole line stands lit, quay to open sea — a road of small lights for whoever the dark still holds out there.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 800 },
  ],
  'script.netmender_drift': [
    { op: 'say', speaker: 'NETMENDER', text: 'I watched from the quay-end. Near, middle... and then the far one stood up in the dark, and I am not ashamed to say I sat down on a crab-pot.' },
    { op: 'say', speaker: 'NETMENDER', text: 'My gran tended that line, and hers before. You kept it a road tonight. Here — this is not payment, it is BELONGING.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'drift_charm', count: 1 },
    { op: 'say', text: 'A buoy-wick charm, still smelling of the going-out song. Received the DRIFT CHARM!' },
    { op: 'say', speaker: 'NETMENDER', text: 'Feed it to your lamp over open water and no wild heart will mistake you for a stranger. Ashore it is only a lamp — the sea keeps her own.' },
    { op: 'setFlag', flag: 'flag:q_south_buoys_done' },
  ],

  // S2 "A Letter for Fenn" — Gran, after the omen: the game's first delivery
  // quest. Her shaken witness beat IS the hook (dread lands on a face, F2/G4).
  'script.gran_letter': [
    { op: 'say', speaker: 'GRAN', text: '...You felt it too, out on the coast? A star went dark, love. I was at the window with your grandfather\'s trimmer in my hand, and the wick I\'d just cut GUTTERED. Forty years that\'s never once happened.' },
    { op: 'say', speaker: 'GRAN', text: 'I am not frightened. I am only old enough to know what the quiet sounds like before it gets bigger.' },
    { op: 'say', speaker: 'GRAN', text: 'So — a favour, while your boots are still warm. I sat up last night and wrote to old Fenn. He watches the sky from the tidal flats now, up past the coast road.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fenn_letter', count: 1 },
    { op: 'say', text: 'She presses a wax-sealed letter into your hands, flat from a night under her pillow. Received GRAN\'S LETTER!' },
    { op: 'say', speaker: 'GRAN', text: 'Ask him plain what I ask him in there: is it coming HERE. And whatever face he makes before he answers — remember it for me.' },
    { op: 'setFlag', flag: 'flag:q_south_letter' },
  ],
  // Fenn takes the letter at his sky-watcher spot on the flats.
  'script.fenn_letter': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'A letter? For ME? Nobody has written to me since— well. Since I last forgot to write back.' },
    { op: 'narrate', text: 'He breaks the wax with his thumbnail and reads it twice, the second time slower. Somewhere in the middle, he smiles at a line he does not share.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'She asks if the dark is coming to Tinderwick. The honest answer is: it is coming everywhere, child. That is why there are Wayfarers.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'But tell her this, from me, in these words: "The lamps are in good hands. Some of them are even yours." She will know what I mean by it.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'And tell her the trade-cart being late is NOT an omen, it is the axle. I do like knowing things.' },
    { op: 'setFlag', flag: 'flag:q_south_letter_given' },
  ],
  'script.gran_thanks': [
    { op: 'say', speaker: 'GRAN', text: '"The lamps are in good hands. Some of them are even yours." ...That man. Sixty years and he still answers a frightened letter with a WINK.' },
    { op: 'narrate', text: 'She laughs — properly laughs — and the kitchen is warm again in a way the hearth alone never quite manages.' },
    { op: 'say', speaker: 'GRAN', text: 'Here, love. Walking fare. A body that carries letters through wild grass deserves better than cold boots and an empty tin.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Received 2 TALLOW BALMS and a WARM BALM!' },
    { op: 'say', speaker: 'GRAN', text: 'Now off with you — the sky doesn\'t relight itself. And come home warm, you hear?' },
    { op: 'setFlag', flag: 'flag:q_south_letter_done' },
  ],

  // S3 "The Cavern Keeps a Light" — the old fisher at the quayside inn. The
  // wreck-lamp itself waits in Tideglass Cavern (Glimmerstep, East) — this is
  // the deliberate long-game promise; the trigger lands with that map.
  'script.fisher_wrecklamp': [
    { op: 'say', speaker: 'OLD FISHER', text: 'You\'re the one who rang the bell back. Then you\'re the one I\'ll tell it to.' },
    { op: 'say', speaker: 'OLD FISHER', text: 'Forty years back my boat went down off the flats, and the sea walked me — don\'t ask me how — into Tideglass Cavern. Dark as a closed eye, that place. All but one light.' },
    { op: 'say', speaker: 'OLD FISHER', text: 'My boat\'s own stern-lamp, wedged in the rocks where she broke. Still burning. It burned three days while I found my way out by it, and I have owed it a wick ever since.' },
    { op: 'say', speaker: 'OLD FISHER', text: 'It will have guttered by now — years it\'s had. The cavern keeps a dark no lamp of MINE can walk. But a vesperlamp that learns the deep-walking art... go in one day, Wayfarer. Light her stern-lamp again. Then come tell an old man it still burns.' },
    { op: 'setFlag', flag: 'flag:q_south_wrecklamp' },
  ],
  'script.fisher_thanks': [
    { op: 'say', speaker: 'OLD FISHER', text: '...It burns? You stood under it and it BURNS?' },
    { op: 'narrate', text: 'For a long moment he looks past you, at some black water forty years gone. Then he nods, once, like a man setting down a net he has carried too far.' },
    { op: 'say', speaker: 'OLD FISHER', text: 'Then the debt\'s paid, and not by me. Here — she\'d want you to have this. Took the Tide Charm to the wreck-light in my dreams a hundred times; you took it for true.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'wrecklight_charm', count: 1 },
    { op: 'say', text: 'Received the WRECKLIGHT CHARM!' },
    { op: 'setFlag', flag: 'flag:q_south_wrecklamp_done' },
  ],

  // A2 (Dimglass Coast I): Wren's first FRIENDLY trainer battle. Wren is a SIGHT
  // trainer — spots the player on the lane, runs up (the engine plays the alert +
  // approach), and this script carries the words + battle. Low-stakes by design.
  'script.wren_dimglass': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'There you are! I was starting to think the grass ate you.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: "Listen — every Wayfarer's first proper battle should be with a friend. So?" },
    { op: 'battle', trainer: 'wren_dimglass' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Same road, different lamps. See you up the coast!' },
    { op: 'setFlag', flag: 'flag:wren_dimglass_battled' },
  ],

  // B1 (Dimglass Coast I): the inciting incident — a far constellation winks out on the
  // first nightfall here. The dread is in the QUIET: letterbox in, fade the bed to
  // silence and hold, then the gutter sting + cold wash + shake as the star dies. This
  // is the first-hour's load-bearing foreboding beat (walkthrough/01-south; the
  // cinematic cadence is binding — see docs/world/cinematics.md).
  'script.dusk_begins': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'silence', ms: 1200 }, // the held quiet before the light fails
    { op: 'narrate', text: 'Far out over the water, a constellation flickers — and goes dark.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'tint', color: '#0b1026', alpha: 0.55, ms: 180 }, // the dark presses in
    { op: 'shake', ms: 320, intensity: 0.006 },
    { op: 'narrate', text: 'For a heartbeat, every lantern-buoy on the coast gutters, as if the sea itself flinched.' },
    { op: 'tint', color: '#0b1026', alpha: 0, ms: 700 },
    { op: 'narrate', text: "That's the third star gone south of here this month. The Long Dusk is getting deeper — and it is getting closer." },
    { op: 'musicCrossfade', key: 'dimglass-coast-a', ms: 900 }, // the bed returns, a shade uneasier
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // Dimglass Coast II route trainers (the XP bridge toward Pearlmoor's 12) —
  // SIGHT trainers: the engine plays the alert + walk-up, these carry the words.
  'script.flats_trainer_a': [
    { op: 'say', speaker: 'MORROW', text: 'Hold up there, Wayfarer! The flats test every lamp that crosses — mine first.' },
    { op: 'battle', trainer: 'flats_wayfarer_a' },
    { op: 'say', speaker: 'MORROW', text: 'Well fought. The dune grass ahead is livelier than it looks — good place to toughen up.' },
    { op: 'setFlag', flag: 'flag:flats_trainer_a_beaten' },
  ],
  'script.flats_trainer_b': [
    { op: 'say', speaker: 'ELSPETH', text: 'A letter-runner never passes a fellow lamp without a bout. Rules of the road!' },
    { op: 'battle', trainer: 'flats_wayfarer_b' },
    { op: 'say', speaker: 'ELSPETH', text: 'Ha! Reyl Wash at Pearlmoor — now THERE is a battle worth the walk. Go see.' },
    { op: 'setFlag', flag: 'flag:flats_trainer_b_beaten' },
  ],

  // --- The Beacon quest (Tinderwick's earned first Gleam) ---------------------
  // Brisa sends the new Wayfarer up the coast road for the beacon's lost
  // wick-key before she'll hold the bond-test at the lantern.
  'script.brisa_quest': [
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'So you have made your first friend. Good. Then hear the truth of it, dear — the EMBER, the south\'s own constellation, is not relit from this hall.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'It is relit from the OLD BEACON, on the bluff east of the square. And the beacon has stood dark since its wick-key was lost on the coast road.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'The old lamplighter who carried it walks Dimglass Coast still, up by the north boundary. Find him. Bring the key home.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'Mind the grass, mind the dark — and come back stronger than you leave. The lantern asks a steady flame.' },
    { op: 'setFlag', flag: 'flag:beacon_quest' },
  ],
  // The old lamplighter (Dimglass I, appears after dusk_begins) hands the key. His
  // closing aside is the first-hour's quiet Hollowing SEED — a cold that "follows the
  // dark down off the north road" — foreboding only, no name, no fight (B2 still
  // introduces the Hollowing formally in East; see docs/world/cinematics.md §tone).
  'script.give_wick': [
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'grave', text: 'You stood under it too, did you. One breath it was there — the next, a hole in the sky shaped like a star.' },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'neutral', text: 'Third one this season. I am too old to climb the Tinderwick beacon now... but you are not, are you.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_wick', count: 1 },
    { op: 'say', text: 'The lamplighter presses a worn brass key into your hand. Received the BEACON WICK-KEY!' },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'grave', text: "And mind yourself out past the north boundary. There's a cold that follows the dark down off that road — quiet, and patient, and it doesn't feel like weather." },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'neutral', text: 'Tell Brisa Tallow the road is darker than she remembers. And walk LIT, young one.' },
    { op: 'setFlag', flag: 'flag:has_beacon_wick' },
  ],
  // The lantern room, beacon top: the bond-test, then the Ember Gleam relit FROM
  // THE TOWER — the first constellation answering the town's own light.
  'script.beacon_battle': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'brisa', facing: 'down' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'Up all those dark stairs with the wick-key in your hand. The lamp-tender chose well.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'This lantern lit the Ember for three hundred years, dear. Show me your flame is steady enough to wake it.' },
    { op: 'battle', trainer: 'lampwarden_tinderwick' },
    // The Gleam payoff: minor→major. Hold a beat of silence, the lantern blooms (warm
    // wash + the lamp sfx), the constellation answers (gleam sting + flash), then the
    // festival swell rises as the town below begins to dance (Arc E).
    { op: 'musicFade', ms: 500 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.4, ms: 600 },
    { op: 'narrate', text: 'Brisa turns the wick-key. The great lantern blooms — and far above, in the dark, a warm light answers.' },
    { op: 'gleam', element: 'ember' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'proud', text: 'There — the Ember Gleam burns again in the southern sky. Go down to the square, dear. I believe the town wants to dance with you.' },
  ],

  // --- Rest points (the genre's heal loop, diegetic) -------------------------
  // The inn: a paid-in-kindness full rest. The innkeep NPC's dialogue_ref runs this.
  'script.inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'Rest your feet, Wayfarer — and your kin. The hearth is warm and the boards are dry.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Lamps trimmed, kin bright-eyed. The dusk can wait on you a while yet.' },
  ],
  // Home: the bed in the apprentice's house. Free, always — home is home.
  'script.home_rest': [
    { op: 'say', text: 'Your own bed, under the old quilt. The lamp hums low...' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', text: 'You wake warm. Your kin are rested and bright.' },
  ],

  // --- Wayfarer's kits + the open counters ------------------------------------
  // Each town keeper hands a starter bundle ONCE (the kit NPC swaps for the
  // trading keeper via flags), and thereafter keeps a live counter: the keeper's
  // script says its flavour line then opens the shop (content/shops.ts) with the
  // 'shop' op. Buying/selling is the ShopMenu; prices live on the ItemDefs.
  'script.shop_kit_tinderwick': [
    { op: 'say', speaker: 'SHOPKEEPER', text: 'Welcome in, out of the dusk. Off on your Wayfaring? Then the first kit is on the house — town custom.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', speaker: 'SHOPKEEPER', text: 'Two glow charges and a pot of tallow balm. Feed a charge to your lamp for one brighter, surer throw; the balm mends a hurt kin. The road north is long.' },
    { op: 'setFlag', flag: 'flag:tinderwick_kit' },
  ],
  'script.shop_kit_pearlmoor': [
    { op: 'say', speaker: 'CHANDLER', text: 'Welcome in off the boards. Facing Reyl, are you? Take the crossing-kit — the sea is kinder to the prepared.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', speaker: 'CHANDLER', text: 'Feed a charge to your lamp before a throw — a charged flame holds a catch better than a plain one.' },
    { op: 'say', speaker: 'CHANDLER', text: 'And mind the old triangle, dear: Ember scorches Verdant, Verdant drinks Tide, Tide drowns Ember. His whole crew runs Tide — bring what beats it.' },
    { op: 'setFlag', flag: 'flag:pearlmoor_kit' },
  ],

  // The open counters (the post-kit keepers' dialogue_refs point here).
  'script.shop_tinderwick': [
    { op: 'dialogue', ref: 'npc.tinderwick_shopkeeper' },
    { op: 'shop', shop: 'tinderwick_general' },
  ],
  'script.shop_pearlmoor': [
    { op: 'dialogue', ref: 'npc.pearlmoor_shopkeeper' },
    { op: 'shop', shop: 'pearlmoor_chandlery' },
  ],

  // --- Route item caches (sprite 'item_cache' NPCs; vanish via hidden_when_flag)
  'script.pickup_dimglass_balm': [
    { op: 'giveItem', item: 'tallow_balm', count: 1 },
    { op: 'say', text: 'A waxed bundle, left for whoever needs it. Found a TALLOW BALM!' },
    { op: 'setFlag', flag: 'flag:picked_dimglass_balm' },
  ],
  'script.pickup_dimglass_lamps': [
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'say', text: "A wayfarer's drop-cache under the lamp post. Found 2 GLOW CHARGES!" },
    { op: 'setFlag', flag: 'flag:picked_dimglass_lamps' },
  ],
  'script.pickup_flats_balm': [
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: 'Sea-wrapped and sound. Found 2 TALLOW BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_flats_balm' },
  ],
  'script.pickup_flats_lamp': [
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'Tucked dry in the dune grass. Found a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_flats_lamp' },
  ],
  // The cache-variety finds (spine rule): a found-to-sell nugget in Tinderwick's
  // SW corner, and loose wicks west of the flats' lane.
  'script.pickup_tinderwick_waxcake': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'wax_cake', count: 1 },
    { op: 'say', text: 'Wrapped in oilcloth behind the hedgerow — a pressed WAX CAKE! Any keeper will trade well for it.' },
    { op: 'setFlag', flag: 'flag:picked_tinderwick_waxcake' },
  ],
  'script.pickup_flats_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 80 },
    { op: 'say', text: "A dropped courier's purse, half-buried in the sand. Found 80 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_flats_wicks' },
  ],
  // The netmender's storm-drifted net-floats (the Causeway Bell's collinear
  // errand leg — appears on the flats once Reyl sets the quest).
  'script.pickup_net_floats': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'net_floats', count: 1 },
    { op: 'say', text: 'A string of cork floats, storm-tangled in the dune grass — every one stamped with the Pearlmoor netmender\'s mark. Took the NET-FLOATS!' },
    { op: 'setFlag', flag: 'flag:picked_net_floats' },
  ],
  // Breakwater caches (off the lane, the standing kit).
  'script.pickup_breakwater_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Lashed dry under a coil of old net, against the spray. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_breakwater_balm' },
  ],
  'script.pickup_breakwater_charge': [
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'A bell-tender\'s drop-box, wedged in the stones. Found a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_breakwater_charge' },
  ],
  // --- Glowmoss Deep (East) — the first cave dungeon + the B2 set-piece -------
  // The deep wood's sight keepers (level-design §11 rule 7): they hold the lane
  // into the moss chambers and the gallery out toward the mine.
  'script.glowmoss_keeper_a': [
    { op: 'say', speaker: 'DELL', text: 'Hold the lane, Wayfarer! Past me are the nursery beds — every moss-mound a hundred years of held light.' },
    { op: 'say', speaker: 'DELL', text: 'Show me your lamp walks soft before I let it walk far.' },
    { op: 'battle', trainer: 'glowmoss_keeper_a' },
    { op: 'say', speaker: 'DELL', text: 'Soft enough. Go on, then... and mind the grey chamber past the beds. Something has been TENDING it, and not kindly.' },
    { op: 'setFlag', flag: 'flag:glowmoss_keeper_a_beaten' },
  ],
  'script.glowmoss_keeper_b': [
    { op: 'say', speaker: 'MIRREL', text: 'Out of the grey chamber with your lamp still lit. Most come out quieter than they went in.' },
    { op: 'say', speaker: 'MIRREL', text: 'One more test before the mine road, then. Deepwood custom.' },
    { op: 'battle', trainer: 'glowmoss_keeper_b' },
    { op: 'say', speaker: 'MIRREL', text: 'Well held. The mine-mouth lies east — tell old Otho Grist the deep wood sent you.' },
    { op: 'setFlag', flag: 'flag:glowmoss_keeper_b_beaten' },
  ],

  // B2 — FIRST HOLLOWING CONTACT (walkthrough/02-east; cinematics.md cadence:
  // a "light fails" beat — letterbox, silence, the cold wash; the dread is the
  // gentleness). Fires on the only choke into the drained site; the cast are
  // NPC placements (acolyte_a/b, cowled_figure, sleeping_fennlight) that
  // withdraw via hidden_when_flag once the lantern is relit.
  'script.glowmoss_drained': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'silence', ms: 1400 }, // the moss-light dies at the choke-stone
    { op: 'narrate', text: 'The glow stops at the choke-stone, as if it had been told to. Past it, the moss lies GREY — a whole chamber of kept light, gone out.' },
    { op: 'tint', color: '#202430', alpha: 0.4, ms: 600 }, // the drained cold
    { op: 'cameraFocus', to: { tx: 17, ty: 8 }, ms: 900 },
    { op: 'narrate', text: 'At the heart of it a Fennlight lies curled in the dead moss, dim as a coal under ash. It is not hurt. It is not waking. Beside it stands a lantern built to hold nothing at all.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'Oh — a Wayfarer. Please, tread soft. She is not hurt. She is RESTING.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'Does the quiet not look gentle, after all that flickering? No more guttering. No more going out. Just... rest.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'We are the Hollowing. Our Warden Còr teaches that the dark asks nothing of anyone. We only help the tired lights lie down.' },
    { op: 'cameraFocus', to: { tx: 20, ty: 7 }, ms: 800 },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'At the chamber\'s far edge a cowled figure stands very still, watching you. It bows its head — sorrowing, almost kind — then turns, and is gone into the dark.' },
    { op: 'cameraReset', ms: 600 },
    { op: 'tint', color: '#202430', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'The null-lantern waits beside the sleeping kin, holding its little piece of dark. Your vesperlamp leans toward it like a struck note.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The null-lantern restoration — the first time the player UNDOES the
  // Hollowing's work. QUIET by design (a small warm bloom, no festival swell —
  // this is grief eased, not a Gleam). Sets flag:met_hollowing via the trigger;
  // the site's cast swaps grey→green on the flag (the §8 null-lantern pattern).
  'script.glowmoss_relight': [
    { op: 'cameraFocus', to: { tx: 18, ty: 8 }, ms: 700 },
    { op: 'narrate', text: 'The null-lantern stands cold at the chamber\'s heart. You raise your vesperlamp and touch flame to the hollow wick.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fe8b8', alpha: 0.3, ms: 600 }, // a small green-gold bloom
    { op: 'narrate', text: 'It takes — small, stubborn, certain. Colour climbs back through the moss-beds like water finding old roots.' },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'In the green hush, the Fennlight stirs — blinks — and lifts into the air, trailing light like pollen.' },
    { op: 'narrate', text: 'The acolytes gather their grey bundles without a word. The last of them pauses at the passage mouth, bows to the waking glow, and follows the dark out.' },
    { op: 'setFlag', flag: 'flag:met_hollowing' },
    { op: 'cameraReset', ms: 600 },
  ],

  // Glowmoss Deep item caches (the standing kit: one valuable, one consumable,
  // one loose-wicks find — walkthrough README "Item caches").
  'script.pickup_glowmoss_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Half-buried in the oldest moss-bed: a bead of resin with a glow-moth caught mid-shimmer. Found a MOTH-AMBER!' },
    { op: 'say', text: 'It still holds a little light. A keeper would trade a fair purse for it.' },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_amber' },
  ],
  'script.pickup_glowmoss_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A waxed tin left where the moss grows thickest, still warm to the touch. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_balm' },
  ],
  'script.pickup_glowmoss_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: "A miner's drop-purse, stitched shut against the damp. Found 200 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_wicks' },
  ],
  // B1F dead-end A: the maze pays in kind — a Star-chart, dry in its tube.
  'script.pickup_b1f_chart': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'chart_focus_mind', count: 1 },
    { op: 'say', text: 'A chart-tube wedged in the rocks, sound and dry. Found a STAR-CHART: FOCUS MIND!' },
    { op: 'setFlag', flag: 'flag:picked_b1f_chart' },
  ],

  // --- Saltreach Fen I (East) — the marsh route's beats ------------------------
  'script.fen_wader_a': [
    { op: 'say', speaker: 'MARIGOLD', text: 'Hold the plank, friend! Fen custom — two lamps that meet on one causeway test their wicks.' },
    { op: 'battle', trainer: 'fen_wader_a' },
    { op: 'say', speaker: 'MARIGOLD', text: 'A dry flame in a wet country — well kept. The fen will let you by.' },
    { op: 'setFlag', flag: 'flag:fen_wader_a_beaten' },
  ],
  'script.fen_courier_b': [
    { op: 'say', speaker: 'OSPREY', text: 'Post for Lowleaf — and a standing toll for the north shore. Paid in a bout, not in wicks!' },
    { op: 'battle', trainer: 'fen_courier_b' },
    { op: 'say', speaker: 'OSPREY', text: 'Toll paid in full. The channel ahead answers Tidecall — Pearlmoor taught you that one, I hope.' },
    { op: 'setFlag', flag: 'flag:fen_courier_b_beaten' },
  ],
  'script.pickup_fen_reed': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'Tucked behind the reed screen, dry in its wax wrap. Found a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_fen_reed' },
  ],
  'script.pickup_fen_bank_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 150 },
    { op: 'say', text: "A wader's purse, left high and dry on the bank. Found 150 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_fen_bank_wicks' },
  ],
  'script.pickup_grotto_starglass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Wedged in the spore-soft dark, a sliver of fallen sky. Found a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_grotto_starglass' },
  ],
  'script.pickup_fen_islet': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Only the tide-walkers reach this islet — and whoever left a WARM BALM for them.' },
    { op: 'setFlag', flag: 'flag:picked_fen_islet' },
  ],

  // --- Saltreach Fen II (East) — deep channels, Tidecall load-bearing ----------
  // The route's one sight trainer: the reed-line lamplighter, posted where the
  // channels give way to firm ground (the 17→18 top of the fen ramp).
  'script.reed_lamplighter': [
    { op: 'say', speaker: 'TARN', text: 'Walked the moon-channels, did you. Then you owe the reed-line a toll — every tide-walker does. Keeps the lamps in oil!' },
    { op: 'battle', trainer: 'reed_lamplighter' },
    { op: 'say', speaker: 'TARN', text: 'Paid in full. The treeline ahead is Lowleaf ground — follow the green glow and mind the Bloom crowds.' },
    { op: 'setFlag', flag: 'flag:reed_lamplighter_beaten' },
  ],

  // E1 "The Quiet Reeds" — the fen fisher on the channel jetty. Three of the
  // lantern-reeds on her line have gone dark; the first two take a flame, the
  // THIRD will not light, and nobody says why. (The B2 foreshadow stays SILENT
  // — no one names the Hollowing east of Glowmoss Deep.)
  'script.fen_fisher': [
    { op: 'say', speaker: 'FEN FISHER', text: 'Evening, tide-walker. You\'ll have seen them on your way in — my lantern-reeds. Three gone dark this season, and reeds don\'t gutter. Reeds GLOW. It\'s what they\'re for.' },
    { op: 'say', speaker: 'FEN FISHER', text: 'My knees don\'t do channels any more, so the line goes untended and the fish go elsewhere. You carry a lit lamp — would you walk it for me?' },
    { op: 'say', speaker: 'FEN FISHER', text: 'Channel order, mind: the near reed first, then the mid-water one, then the far one up by the treeline. A line lights from home outward. Always has.' },
    { op: 'setFlag', flag: 'flag:q_east_reeds' },
  ],
  'script.reed_first': [
    { op: 'narrate', text: 'The near lantern-reed leans dark over its own reflection. You cup the seed-head and touch your vesperlamp to the wick inside.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffb86b', alpha: 0.2, ms: 400 },
    { op: 'narrate', text: 'It takes — a warm amber globe waking over the black water. One. Somewhere below, something small and silver turns toward the light.' },
    { op: 'tint', color: '#ffb86b', alpha: 0, ms: 600 },
  ],
  'script.reed_second': [
    { op: 'narrate', text: 'The mid-water reed is furred with cold moss, its globe long dark. You clear the wick with a thumbnail and lend it your flame.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffb86b', alpha: 0.2, ms: 400 },
    { op: 'narrate', text: 'Two. Behind you the near reed answers it across the channel, the way a held note answers a held note.' },
    { op: 'tint', color: '#ffb86b', alpha: 0, ms: 600 },
  ],
  // The third reed — it will NOT light. A quiet dread beat, no explanation:
  // that answer belongs to Glowmoss Deep. (cinematics.md: dread = the quiet.)
  'script.reed_third': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The far reed stands dark against the treeline. You raise your vesperlamp and touch flame to the wick, the way you have twice tonight.' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'The wick drinks your flame and stays dark.' },
    { op: 'narrate', text: 'You try again, shielding it with both hands. The flame goes into it like a stone into deep water — no smoke, no spark, no reason. The reed is not wet. It is not broken. It is just... finished.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'Out in the dark fen, nothing moves. The two reeds you lit burn steadily behind you, and somehow that is worse.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],
  'script.fen_fisher_report': [
    { op: 'say', speaker: 'FEN FISHER', text: 'I watched the near two stand up from right here — bless your quick hands. And the far one?' },
    { op: 'narrate', text: 'You tell her. The flame that sank like a stone. The wick that was not wet, and not broken, and would not take.' },
    { op: 'say', speaker: 'FEN FISHER', text: '...Hm. Forty years on this water and I\'d have said there\'s no such thing as a reed that won\'t light.' },
    { op: 'say', speaker: 'FEN FISHER', text: 'Probably nothing. A bad wick. A cold spring.' },
    { op: 'narrate', text: 'She looks past you at the treeline for a long moment, and does not say what she is thinking.' },
    { op: 'say', speaker: 'FEN FISHER', text: 'Here — the line\'s thanks, and mine. A reed-wick lamp, dipped the old way. In deep growth it burns twice as sure; the fen looks after them as walk it kindly.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'marsh_lamp', count: 1 },
    { op: 'say', text: 'Received the MARSH LAMP!' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: 'She presses a knotted purse on you too — 200 WICKS. "For the oil you burned. No arguing."' },
    { op: 'setFlag', flag: 'flag:q_east_reeds_done' },
  ],

  // Fen II caches (the standing kit: a valuable on the tide-walk isle, loose
  // wicks off the lane, a consumable by the landing).
  'script.pickup_fen_isle_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'No plank reaches this isle — only the parted water. Half-sunk in the reed-root: a MOTH-AMBER, still warm with old light!' },
    { op: 'setFlag', flag: 'flag:picked_fen_isle_amber' },
  ],
  'script.pickup_fen_ii_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 150 },
    { op: 'say', text: "A fisher's drop-tin, lashed above the waterline. Found 150 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_fen_ii_wicks' },
  ],
  'script.pickup_fen_ii_balm': [
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: 'Wax-wrapped against the damp, left for the next walker. Found 2 TALLOW BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_fen_ii_balm' },
  ],

  // --- Sunkbell Shallows (Tidecall spur) — the half-flooded shrine -------------
  'script.pickup_sunkbell_charges': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'A pilgrim\'s offering-box, sealed with wax against the flood. Found 2 BEACON CHARGES — left, perhaps, for exactly the kin that swim here.' },
    { op: 'setFlag', flag: 'flag:picked_sunkbell_charges' },
  ],
  'script.pickup_sunkbell_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Tucked dry in a niche of the drowned steps. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_sunkbell_balm' },
  ],

  // --- Lowleaf Hollow (East) — the Glowmoss Bloom + the Tended Bed -------------
  // Arrival: the festival reveal + the grey Elder Bed tease, banded across the
  // south corridor so the first walk in always lands it.
  'script.glowmoss_bloom_arrival': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicCrossfade', key: 'lowleaf-hollow-b', ms: 900 },
    { op: 'narrate', text: 'The fen gives way to ferns, and the ferns are FULL of light. Lantern-strings between the trunks, stalls under striped awnings, moss glowing green-gold on every roof — Lowleaf Hollow, and the Glowmoss Bloom is in full swing.' },
    { op: 'narrate', text: 'Children chase a drift of glow-motes across the lane. Somewhere a piper is playing rounds, and nobody is dancing in step, and nobody minds.' },
    { op: 'cameraFocus', to: { tx: 15, ty: 13 }, ms: 900 },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'But at the hollow\'s heart, where the dancing ring turns — the oldest moss-bed in town lies GREY. The festival flows around it the way a song flows around a missed note.' },
    { op: 'cameraReset', ms: 600 },
    { op: 'musicCrossfade', key: 'lowleaf-hollow-a', ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The Tended Bed (spine §5 shape #3 — the LIGHT loop). Sable's hook:
  'script.sable_quest': [
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: 'Oh — a Wayfarer. With two Gleams already over your shoulder, if I\'m reading your lamp right. I, um. Welcome to the Bloom.' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'You\'ll have seen the Elder Bed on your way in. Grey, at its own festival. Everyone keeps asking me to make a speech about it, and I\'d rather... not make speeches.' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'The Bloom won\'t crown over a grey bed. Warm the old moss first — then we\'ll see what your light\'s worth.' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: 'The kilner by the square will know what it needs. Moss doesn\'t want speeches either. It wants warmth, and somebody patient.' },
    { op: 'setFlag', flag: 'flag:q_east_bloom' },
  ],

  // The fen-wood cache on the forest fringe (the bloom-warden lane).
  'script.pickup_fenwood': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fen_wood', count: 1 },
    { op: 'say', text: 'Stacked dry under the ferns where the kilners always stack it. Took an armful of FEN-WOOD!' },
    { op: 'setFlag', flag: 'flag:picked_fenwood' },
  ],

  // The kilner fires a hearth-spore from your fen-wood.
  'script.kiln_relight': [
    { op: 'say', speaker: 'KILNER', text: 'Fen-wood! Dry as a sermon and twice as useful. Give it here, give it here—' },
    { op: 'narrate', text: 'She racks the wood, strikes her flint twice, and the bloom-kiln wakes with a breath like a sleeping animal rolling over.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.25, ms: 500 },
    { op: 'say', speaker: 'KILNER', text: 'Now — the part nobody under sixty remembers. You don\'t warm an elder bed with fire. You warm it with what fire LEAVES.' },
    { op: 'narrate', text: 'She rakes the first coals, lifts something from their heart with bronze tongs, and folds it into a wax paper twist: a kiln-fired glowmoss spore, warm as a held coal.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 600 },
    { op: 'giveItem', item: 'hearth_spore', count: 1 },
    { op: 'say', text: 'Received the HEARTH-SPORE!' },
    { op: 'giveMoney', amount: 150 },
    { op: 'say', text: '"And the kiln-fee — the festival pays whoever feeds the kiln. Tonight that\'s you." Received 150 WICKS!' },
    { op: 'say', speaker: 'KILNER', text: 'Tuck it under the old moss and STEP BACK. Beds remember what to do. They just need reminding they\'re not done.' },
    { op: 'setFlag', flag: 'flag:q_east_hearthspore' },
  ],

  // Warming the Elder Bed — the loop's payoff: the grey→green swap (the §8
  // null-lantern pattern, warm edition: flag-gated objects + festival NPCs).
  'script.warm_elder_bed': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'You kneel at the stone ring. Up close the grey is worse — moss like burnt paper, a century of kept light gone to ash-colour.' },
    { op: 'silence', ms: 1000 },
    { op: 'narrate', text: 'You work the hearth-spore down under the cold cushion, the way you\'d bank a coal for morning. And step back.' },
    { op: 'wait', ms: 600 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fe8b8', alpha: 0.35, ms: 800 },
    { op: 'narrate', text: 'Nothing. Nothing. Then — between two stones, one thread of moss remembers its colour. Then ten. Then the whole bed at once, green-gold racing rim to rim like a rumour through a crowd.' },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'Behind you, the piper stops mid-round. The whole festival has turned to look. A child says, very clearly, "it was SLEEPING," and the dancing ring re-forms around the Elder Bed where it has always belonged.' },
    { op: 'musicCrossfade', key: 'lowleaf-hollow-b', ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The bloom-warden sight trainers on the fen-wood lane (keeper class).
  'script.bloom_warden_a': [
    { op: 'say', speaker: 'IVY', text: 'Hold the lane! Past me are the fringe beds — festival or no festival, every lamp that walks them gets weighed.' },
    { op: 'battle', trainer: 'bloom_warden_a' },
    { op: 'say', speaker: 'IVY', text: 'Weighed and welcome. The dry fen-wood is stacked under the far ferns — mind where the moss is sleeping.' },
    { op: 'setFlag', flag: 'flag:bloom_warden_a_beaten' },
  ],
  'script.bloom_warden_b': [
    { op: 'say', speaker: 'FERN', text: 'A Wayfarer on the wood-lane! Good. Ivy softens them up and I finish the lesson — that\'s the Bloom-watch way.' },
    { op: 'battle', trainer: 'bloom_warden_b' },
    { op: 'say', speaker: 'FERN', text: 'Lesson finished. You\'d give Sable herself a fair evening — and I don\'t say that at every festival.' },
    { op: 'setFlag', flag: 'flag:bloom_warden_b_beaten' },
  ],

  // The Verdant bond-test + Gleam ceremony (Sable's hall; minor→major, the
  // Glowmoss Bloom swell — the third "Gleam = belonging" payoff).
  'script.lumenary_lowleaf': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'sable', facing: 'down' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'You didn\'t make a speech at it. You just... warmed it, and stepped back, and let it remember itself. I watched from the door.' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'So I won\'t make a speech either. The moss vouches for you. Now show me it\'s right.' },
    { op: 'battle', trainer: 'lampwarden_lowleaf' },
    { op: 'musicFade', ms: 500 },
    { op: 'tint', color: '#9fe8b8', alpha: 0.36, ms: 600 },
    { op: 'narrate', text: 'Sable opens the hall doors wide. Outside, the Elder Bed answers her hall-moss glow for glow — and overhead, threading green-gold between the stars, the VERDANT remembers how to shine.' },
    { op: 'gleam', element: 'verdant' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'The moss doesn\'t shine FOR anyone. It just... keeps a little light where it can. Be like the moss. Here — this\'ll let you walk where it\'s dark.' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: 'The Glimmerstep. The deep wood north of town has been shut to me my whole life — too dark past the first bough. Your lamp won\'t mind it now. ...Tell me what grows in there. Please.' },
  ],

  // The festival crowns around the green bed — banded in town, post-Gleam.
  'script.bloom_crowning': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'narrate', text: 'The hollow is roaring — as much as a town of botanists ever roars. The Elder Bed burns green-gold at the heart of the dancing ring, and over the treeline the Verdant constellation hangs new-lit in the dark.' },
    { op: 'narrate', text: 'Somebody has crowned the bed\'s tallest stone with a wreath of glowmoss. Somebody else is crying into a moss-cake. The piper has given up on rounds and is simply playing.' },
    { op: 'say', speaker: 'BLOOM ELDER', text: 'A hundred and nine Blooms I\'ve danced, and I never saw the Bed crowned before. Belonging, child — that\'s what a Gleam is. Tonight you belong to Lowleaf.' },
    { op: 'musicCrossfade', key: 'lowleaf-hollow-b', ms: 1100 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // E2 "Spores for the Stall" — the Bloom stall-keeper's gathering errand.
  'script.stall_quest': [
    { op: 'say', speaker: 'STALL-KEEPER', text: 'Moss-cakes! Glow-jars! Spore-bread warm from the— oh, who am I fooling. Look at my shelf. EMPTY. The Bloom eats spores faster than the deep wood sends them.' },
    { op: 'say', speaker: 'STALL-KEEPER', text: 'My gatherer won\'t go past the first bough since the wood went quiet, and now there\'s a lamp in town that walks the dark like it\'s a garden path. That\'s you. I\'ve seen you.' },
    { op: 'say', speaker: 'STALL-KEEPER', text: 'Three spore-caches, left bundled along the glow-beds in the Deep. Bring them home and the stall feeds the rest of the festival — and you, for life, within reason.' },
    { op: 'setFlag', flag: 'flag:q_east_spores' },
  ],
  'script.pickup_spore_a': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bloom_spores', count: 1 },
    { op: 'say', text: 'A gatherer\'s cloth bundle, heavy with glowing spores. One of three. The moss around it leans toward your lamp as you lift it.' },
    { op: 'setFlag', flag: 'flag:picked_spore_a' },
  ],
  'script.pickup_spore_b': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bloom_spores', count: 1 },
    { op: 'say', text: 'The second spore-bundle, tucked in a root-hollow. Two of three. Something further up the gallery chitters at you — twice, pointedly.' },
    { op: 'setFlag', flag: 'flag:picked_spore_b' },
  ],
  // The third cache has a squatter: a cross Sporeling, driven off in a battle.
  'script.spore_squatter': [
    { op: 'narrate', text: 'The third bundle is RIGHT THERE — and sitting on it, puffed to twice its size, is a Sporeling with the expression of a landlord.' },
    { op: 'say', text: 'It chitters. It is not a welcoming chitter.' },
    { op: 'battle', trainer: 'spore_squatter' },
    { op: 'narrate', text: 'The Sporeling huffs one last cloud of indignation, hops off the bundle, and flounces away into the glow-beds — pride dented, dignity intact.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bloom_spores', count: 1 },
    { op: 'say', text: 'Took the last spore-bundle. Three of three!' },
    { op: 'setFlag', flag: 'flag:spore_squatter_beaten' },
  ],
  'script.stall_reward': [
    { op: 'say', speaker: 'STALL-KEEPER', text: 'Three bundles! And one of them argued for — I can smell the huff on it. You beautiful walking lantern.' },
    { op: 'narrate', text: 'She has the shelf restocked before you finish explaining, hands moving like a card-sharp\'s. A queue forms behind you instantly.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'glow_salve', count: 1 },
    { op: 'say', text: 'Received a GLOW SALVE — "festival pressing, not for sale, don\'t tell the provisioner."' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'And a share of the stall\'s evening: 300 WICKS!' },
    { op: 'say', speaker: 'STALL-KEEPER', text: 'One more thing, since you like the deep wood: the Fennlight drift into the fringe grass while the Bloom\'s lit. The town\'s own kin, green-and-gold. Take a charge out there and ask one home — no stall-keeper ever had a better lamp-piece.' },
    { op: 'setFlag', flag: 'flag:q_east_spores_done' },
  ],

  // Lowleaf's one-time shop kit + the open counter (the standing pattern).
  'script.shop_kit_lowleaf': [
    { op: 'say', speaker: 'PROVISIONER', text: 'In off the fen! Then you\'ll want the Bloom-kit — festival custom, no charge, stop arguing.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', speaker: 'PROVISIONER', text: 'Two glow charges and a warm balm. The fringe grass is generous during the Bloom — and the deep wood past it is not. Stock accordingly.' },
    { op: 'setFlag', flag: 'flag:lowleaf_kit' },
  ],
  'script.shop_lowleaf': [
    { op: 'dialogue', ref: 'npc.lowleaf_provisioner' },
    { op: 'shop', shop: 'lowleaf_provisioner' },
  ],

  // The guest-bower's rest (the town's full heal — the standing kit).
  'script.lowleaf_rest': [
    { op: 'say', speaker: 'BOWER-KEEPER', text: 'Festival or fen-mud, every walker gets the same bower. In you go — the moss-bunks are warm and the lamps are low.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'BOWER-KEEPER', text: 'There. Kin bright-eyed, boots dry. The Bloom keeps till morning — it always does.' },
  ],

  // Lowleaf caches (variety rule: wicks behind the cottages, a charge by the fringe).
  'script.pickup_lowleaf_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 120 },
    { op: 'say', text: 'A festival takings-tin, forgotten behind the cottage. Found 120 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_lowleaf_wicks' },
  ],
  'script.pickup_lowleaf_balm': [
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: 'A festival hamper, tucked out of the dancing. Found 2 TALLOW BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_lowleaf_balm' },
  ],
  'script.pickup_lowleaf_charge': [
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'Left on the fringe-side fence post, wax seal unbroken. Found a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_lowleaf_charge' },
  ],

  // Gullcry Rock's prize: the Tide Charm (a sea-blessed lamp; see items.ts).
  'script.pickup_gullcry_charm': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'tide_charm', count: 1 },
    { op: 'say', text: 'Lashed to the highest stone, wave-worn and humming. Found the TIDE CHARM!' },
    { op: 'say', text: 'It beats softly in your hand, like a held breath of the sea.' },
    { op: 'setFlag', flag: 'flag:picked_gullcry_charm' },
  ],
};

export function getScript(ref: string): import('./types').CutsceneStep[] | undefined {
  return SCRIPTS[ref];
}
