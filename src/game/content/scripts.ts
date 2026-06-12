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

  // ===========================================================================
  // CINDERHEAD MINE — the Stone wall (walkthrough/02-east; Lumenary 4: Otho
  // Grist). The Descent Vigil earned loop (spine §5 shape #4, the HEAVY loop)
  // + the Lamp-down vigil festival + E3 (The Foreman's Ledger) + the hub
  // shortcut. The Stone Gleam is the curve's one designed WALL made diegetic.
  // ===========================================================================

  // Otho's hook — the vigil-lamp errand (the loop's collinear descent; sends the
  // player through the 24-27 galleries before the wall, the §4 gap-closer).
  'script.otho_quest': [
    { op: 'say', speaker: 'OTHO GRIST', text: "You'll be the Wayfarer the vigil's been muttering about. Come for a Gleam, have you." },
    { op: 'say', speaker: 'OTHO GRIST', text: "Down here, light's not GIVEN. It's kept. My crew left the vigil-lamp at the third gallery when the dark came up — still lit, if they did their job." },
    { op: 'say', speaker: 'OTHO GRIST', text: "Bring it back up STILL BURNING. Then I'll know your light holds when the rock leans in, and we'll talk about a Gleam. Not before." },
    { op: 'setFlag', flag: 'flag:q_east_vigil' },
  ],

  // Carrying the vigil-lamp up (in the deep) — the §8 restoration beat, the
  // melancholy edition: the gallery lamps lean toward the one flame that kept.
  'script.take_vigil_lamp': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The vigil-lamp sits where the crew left it — a small steady flame in a cage of old brass, burning yet, after all this dark. Somebody kept it fed in their heart, and so it kept.' },
    { op: 'silence', ms: 900 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.30, ms: 700 },
    { op: 'narrate', text: 'You lift it carefully, cupping the flame. It does not gutter. As you turn for the long climb, the gallery lamps you passed seem to lean toward it — waiting their turn.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 700 },
    { op: 'letterbox', on: false, ms: 320 },
    { op: 'setFlag', flag: 'flag:q_east_vigil_lamp' },
  ],

  // The Stone bond-test + Gleam (Otho's hall) — the most MELANCHOLY swell of the
  // eight: lean on `silence` before the lift (Arc E, the Lamp-down vigil). Sets
  // gleam:stone; the engine derives flag:crown_east (East's second quadrant).
  'script.lumenary_cinderhead': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'otho', facing: 'down' },
    { op: 'say', speaker: 'OTHO GRIST', text: "You carried it up still burning. Through the deep galleries, in the dark, without letting it go out." },
    { op: 'say', speaker: 'OTHO GRIST', text: "Anyone can LIGHT a lamp. Carrying one through the dark without dropping it — that's the trick of the whole thing. Now show me your kin can do it too." },
    { op: 'battle', trainer: 'lampwarden_cinderhead' },
    { op: 'musicFade', ms: 600 },
    { op: 'silence', ms: 1100 },
    { op: 'narrate', text: 'Otho says nothing for a long moment. Then he lifts the vigil-lamp from its cage — and one by one, all through the town behind him, the lowered lamps begin to rise.' },
    { op: 'tint', color: '#caa46a', alpha: 0.34, ms: 800 },
    { op: 'narrate', text: 'And overhead, through a fault in the cavern roof no miner ever marked, the STONE constellation steadies in the dark — patient, unhurried, the way the mountain is.' },
    { op: 'gleam', element: 'stone' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 1000 },
    { op: 'tint', color: '#caa46a', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'OTHO GRIST', text: "The Stone Gleam. Four constellations relit — and the southern and eastern crowns both yours now. The mountain remembers a steady light." },
    { op: 'say', speaker: 'OTHO GRIST', text: "Galehigh's up the deep galleries and out the far side. Cold wind, high ledges — a different kind of dark. You'll do. Mind the lamp." },
  ],

  // The vigil-fire rest (the town's full heal — the standing per-region kit).
  'script.cinderhead_rest': [
    { op: 'say', speaker: 'VIGIL COOK', text: "Sit by the vigil-fire, Wayfarer. We keep it low — but we keep it. Warm your kin and your hands both." },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'VIGIL COOK', text: "There. Rested and ready. The dark's long — but the fire's longer." },
  ],

  // Cinderhead's one-time shop kit + the open counter (the standing pattern).
  'script.shop_kit_cinderhead': [
    { op: 'say', speaker: 'PIT-PROVISIONER', text: "Fronting up to Otho, are you? Here — the pit-kit. Custom for every Wayfarer who does. No charge; you'll need it more than my shelf does." },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'say', speaker: 'PIT-PROVISIONER', text: "Two warm balms and a pair of charges. Otho's kin hit like a roof-fall — stock balms, not bravado." },
    { op: 'setFlag', flag: 'flag:cinderhead_kit' },
  ],
  'script.shop_cinderhead': [
    { op: 'dialogue', ref: 'npc.cinderhead_provisioner' },
    { op: 'shop', shop: 'cinderhead_provisioner' },
  ],

  // E3 "The Foreman's Ledger" — the lone miner by the deep mouth (giver); the
  // ledger is recovered a gallery down (script.pickup_ledger), returned for pay.
  'script.ledger_quest': [
    { op: 'say', speaker: 'LONE MINER', text: "You're going down anyway, by the look of your lamp. Do an old hand a turn?" },
    { op: 'say', speaker: 'LONE MINER', text: "The foreman's ledger — every seam and shoring the crew ever cut — got left in a side gallery when the dark came up. I can't face the deep no more. You can." },
    { op: 'say', speaker: 'LONE MINER', text: "Bring it home and the crew's whole history's yours to thank. Good crystal down there too, mind — honest pay for honest dark." },
    { op: 'setFlag', flag: 'flag:q_east_ledger' },
  ],
  'script.pickup_ledger': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'say', text: 'A water-swollen ledger in cracked leather, wedged in a dry niche. Recovered the FOREMAN\'S LEDGER!' },
    { op: 'say', text: 'The last legible page lists galleries "past the lamp\'s reach" — names you can\'t make out in this light. Something for a brighter lamp, another day.' },
    { op: 'setFlag', flag: 'flag:q_east_ledger_found' },
  ],
  'script.ledger_reward': [
    { op: 'say', speaker: 'LONE MINER', text: "The ledger! After all these years — I'd given it up to the wet. Bless your lamp, Wayfarer." },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'He presses a STARGLASS SHARD into your hand — "deep-cut crystal, the good stuff. Sell it well."' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: "And a foreman's thank-you: 300 WICKS!" },
    { op: 'setFlag', flag: 'flag:q_east_ledger_done' },
  ],

  // The sealed mine door, opened from the inside — the hub re-link. The trigger
  // sets flag:shortcut_mine; this is the cutscene that sells it (spine §0 rule 3).
  'script.open_mine_shortcut': [
    { op: 'narrate', text: 'A sealed door, timbered shut from the far side a generation ago. From in here the bar lifts easily — it was only ever meant to keep the dark from wandering UP.' },
    { op: 'sfx', key: 'world-door' },
    { op: 'narrate', text: 'It swings onto a cart-track you half recognise: the old hoist-line, running straight back to the Vesper Crossroads. The east just got a great deal smaller.' },
  ],

  // Cinderhead caches (variety rule: a gallery crystal valuable, loose wicks, a
  // balm in the mine; a deep MOTH-AMBER a choke off the lane, the §4 grind reward).
  'script.pickup_cinderhead_crystal': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'A fist of raw crystal still in its matrix, catching your lamp. Found a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_cinderhead_crystal' },
  ],
  'script.pickup_cinderhead_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 160 },
    { op: 'say', text: 'A pay-tin in a niche, forgotten when the shift ran out. Found 160 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_cinderhead_wicks' },
  ],
  'script.pickup_cinderhead_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: "A miner's belt-pouch, balms still sealed. Found 2 WARM BALMS!" },
    { op: 'setFlag', flag: 'flag:picked_cinderhead_balm' },
  ],
  'script.pickup_deepcrystal': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Wedged in a deep seam, a knot of MOTH-AMBER — a collector would pay dearly for it. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_deepcrystal' },
  ],
  // deeper-floor caches (the descent maze pays in kind, a choke off the lane)
  'script.pickup_cinderhead_wicks_deep': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: 'A strongbox tucked behind a pit-prop, the crew\'s float still inside. Found 200 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_cinderhead_wicks_deep' },
  ],
  'script.pickup_cinderhead_balm_deep': [
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'A vigil-relief cache by the down-ladder — balms and a charge for the long climb back. Took them!' },
    { op: 'setFlag', flag: 'flag:picked_cinderhead_balm_deep' },
  ],

  // The two vigil-miner SIGHT trainers holding the Descent Vigil leg (keeper class).
  'script.gallery_miner_a': [
    { op: 'say', speaker: 'DRUSE', text: "Hold up. Nobody walks my gallery toward the vigil-lamp without weighing their wick against mine. Crew rule, old as the seam." },
    { op: 'battle', trainer: 'gallery_miner_a' },
    { op: 'say', speaker: 'DRUSE', text: "Steady light. Go on — the lamp's two chambers down, still burning if I know my crew." },
    { op: 'setFlag', flag: 'flag:gallery_miner_a_beaten' },
  ],
  'script.gallery_miner_b': [
    { op: 'say', speaker: 'HOBB', text: "The last lamp before the vigil-lamp's mine to keep. Druse softens them, I finish them — that's the crew way, down here." },
    { op: 'battle', trainer: 'gallery_miner_b' },
    { op: 'say', speaker: 'HOBB', text: "Finished proper. Carry it up gentle, Wayfarer — a flame that crossed the dark deserves a steady hand." },
    { op: 'setFlag', flag: 'flag:gallery_miner_b_beaten' },
  ],

  // ===========================================================================
  // THE NORTH (walkthrough/03-north) — Galehigh Terraces (Lumenary 5: Mira
  // Vael, Storm + the Kite-rising), Windward Stair I→II, Pale Vault Glacier
  // (Lumenary 6: Ysolde Frost + the Aurora-watch), and the B3/C3/A4 cluster —
  // the character-drama peak of the midgame. Staging per cinematics.md:
  // portraits + silence over spectacle.
  // ===========================================================================

  // --- Galehigh: the Kite-Rising Winch (spine §5 shape #5) -------------------
  // Mira's hook, shouted down from the launch ledge as the player first crosses
  // the festival terrace (trigger band sets flag:q_north_kite).
  'script.mira_quest': [
    { op: 'narrate', text: 'High above the festival terrace, kite-strings climb all the way to a launch ledge in the last of the sunset — and something up there is FLYING, looping the updrafts like it was hatched in them.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'HOY! Down there — the new lamp out of the mine! Yes, YOU, with the four Gleams and the indoor shoulders!' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'You want the Storm Gleam? Then FLY! Nobody meets the wind from the ground — that is not me being poetic, that is a RULE.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'Raise a kite with the town — the kite-maker on the lower terrace will see you right — and fly it at the Rising. Do that, and the winch will bring you up to me and the wind both.' },
    { op: 'narrate', text: 'She peels away into a gust, whooping. Far below, the festival cheers her without looking up — they know the sound by heart.' },
  ],

  // The kite-maker's three storm-scattered pieces — chained caches on the lower
  // terraces (each pick reveals the next; the flags drive the map's chain).
  'script.pickup_kite_a': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'kite_spar', count: 1 },
    { op: 'say', text: 'Wedged in the wind-break hedge, whole and sound: a wind-tempered KITE SPAR! The sail can\'t have blown much further.' },
    { op: 'setFlag', flag: 'flag:picked_kite_a' },
  ],
  'script.pickup_kite_b': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'kite_sail', count: 1 },
    { op: 'say', text: 'Snagged on a terrace post, tugging to be off again: the lantern-orange KITE SAIL! Now — where would a tail land...' },
    { op: 'setFlag', flag: 'flag:picked_kite_b' },
  ],
  'script.pickup_kite_c': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'kite_tail', count: 1 },
    { op: 'say', text: 'Coiled neat as a sleeping cat in the dry grass: the KITE TAIL, every little wick-lamp unbroken. Spar, sail and tail — back to the kite-maker!' },
    { op: 'setFlag', flag: 'flag:picked_kite_c' },
  ],

  // The kite-maker builds the town's kite back out of your three finds.
  'script.kite_built': [
    { op: 'say', speaker: 'KITE-MAKER', text: 'The spar! The sail! The — oh, the TAIL, with the lamps still in it! You walked half the terraces for a stranger\'s kite.' },
    { op: 'narrate', text: 'She works without another word — spar sleeved into sail, tail bent on, every knot tested twice against her wrist. It takes her minutes. It would have taken you a season.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'There. My best kite, twice-built — once by me, once by you. That makes it the TOWN\'S kite now; that\'s how the custom works.' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'Take it to the winch-keeper on the festival terrace and fly it at the Rising. And mind the tail-lamps — the stars are watching for them.' },
    { op: 'setFlag', flag: 'flag:q_north_kite_ready' },
  ],

  // Arc E — the Kite-rising itself: warm, communal, a little daft. The crest is
  // sincere (humour lives in the build-up, never the crest).
  'script.galehigh_kite_rising': [
    { op: 'say', speaker: 'WINCH-KEEPER', text: 'A town-built kite and a wind from the south-east — Wayfarer, your timing is a festival in itself. PLACES, everyone! The Rising rises!' },
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicCrossfade', key: 'galehigh-terraces-b', ms: 900 },
    { op: 'narrate', text: 'The whole terrace pays out string at once. Kites stagger up into the gusts — patched ones, proud ones, one shaped alarmingly like the winch-keeper — every tail strung with tiny lit wick-lamps.' },
    { op: 'say', speaker: 'FESTIVAL KID', text: 'Yours next! Don\'t let it dip past the third gust, the third gust is a BITER—' },
    { op: 'narrate', text: 'You let the wind take the town\'s kite. It dips past the third gust — which bites — staggers, steadies... and CLIMBS, lamp-tail writing a wobbly line of light all the way up the dark.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.22, ms: 800 },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'And for one held breath the whole hill goes quiet, necks craned, a hundred small flames swaying overhead — so the stars have something to climb back up. Daft, maybe. But the night is a little less long for it.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 900 },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'say', speaker: 'WINCH-KEEPER', text: 'FLOWN AND BLESSED! Wayfarer — Mira watched every yard of that. The drum turns for you now. Up you go, and wave back on the way!' },
    { op: 'musicCrossfade', key: 'galehigh-terraces-a', ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
    { op: 'setFlag', flag: 'flag:q_north_kite_blessed' },
  ],

  // Galehigh's sight trainers (route class) + the skyloft's wind-wards (keeper).
  'script.galehigh_kitehand': [
    { op: 'say', speaker: 'PERRIN', text: 'Hold the lane, Wayfarer! Festival rule — every lamp that crosses the terraces gets weighed against the wind. I AM the wind\'s representative.' },
    { op: 'battle', trainer: 'galehigh_kitehand' },
    { op: 'say', speaker: 'PERRIN', text: 'Weighed, and the wind approves. The kite-maker\'s stall is down the steps — tell her Perrin still owes her a spar.' },
    { op: 'setFlag', flag: 'flag:galehigh_kitehand_beaten' },
  ],
  'script.galehigh_terracer': [
    { op: 'say', speaker: 'SORREL', text: 'Off my beds, off my beds — round the LANE, like a— oh, you\'re a Wayfarer. Well then. Terrace custom: the crops watch a bout before you pass.' },
    { op: 'battle', trainer: 'galehigh_terracer' },
    { op: 'say', speaker: 'SORREL', text: 'Beaten on my own terrace. The cabbages saw everything. We shall never speak of it.' },
    { op: 'setFlag', flag: 'flag:galehigh_terracer_beaten' },
  ],
  'script.skyloft_ward_a': [
    { op: 'say', speaker: 'TAMSIN', text: 'A rider off the winch! Then the town blessed your kite — but the LEDGE answers to the wind-wards. Show us your flame stands up here, where the gusts mean it.' },
    { op: 'battle', trainer: 'skyloft_ward_a' },
    { op: 'say', speaker: 'TAMSIN', text: 'Well flown. And I\'d trained that gust personally. Go on — Bran holds the last stretch.' },
    { op: 'setFlag', flag: 'flag:skyloft_ward_a_beaten' },
  ],
  'script.skyloft_ward_b': [
    { op: 'say', speaker: 'BRAN', text: 'Last ward before the launch ledge. Mira asks one thing of everyone who stands there: that the wind has already said yes. Let\'s hear it say so.' },
    { op: 'battle', trainer: 'skyloft_ward_b' },
    { op: 'say', speaker: 'BRAN', text: 'It said yes. Loudly. The ledge is ahead, Wayfarer — she\'ll be the one mid-air.' },
    { op: 'setFlag', flag: 'flag:skyloft_ward_b_beaten' },
  ],

  // Lumenary 5 — Mira Vael at the launch ledge. Win → gleam:storm + Updraft
  // Kite (TRAINERS['mira_vael'] carries the grants). The ceremony is the
  // BINDING Gleam cadence: silence → warm tint → lamp sfx → gleam → swell.
  'script.lumenary_galehigh': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'mira_vael', facing: 'down' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'There you are! I watched your kite take the third gust and KEEP CLIMBING. The wind talked about it all the way up the winch — it does go on, the wind.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'You don\'t fight the wind, apprentice. You ask it to lift you — and you thank it when it does. Same as a kin. Same as a town.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'So! Last asking, and the sky\'s watching: show me a bond the storm itself would carry!' },
    { op: 'battle', trainer: 'mira_vael' },
    { op: 'musicFade', ms: 500 },
    { op: 'silence', ms: 1000 },
    { op: 'tint', color: '#ffd089', alpha: 0.38, ms: 700 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Mira raises her lamp off the launch ledge, and every kite-tail over Galehigh lifts its little flames with it — a hill of held light, offered up. And overhead, the STORM takes it.' },
    { op: 'gleam', element: 'storm' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'The Storm Gleam stands! Five relit — listen to the town! That cheer is YOURS, and so is this:' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'The Updraft Kite. A storm-kin\'s gift: warm thermals to lift you up the high ledges, and a long glide where the ground runs out. The wind says yes to you now. It told me.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'And the first taste is the best one — step off the ledge, Wayfarer. GLIDE down to your festival. I\'ll race you!' },
  ],

  // Rest, kit and counter (the standing per-region kit).
  'script.galehigh_inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'In out of the gusts, Wayfarer. The fire\'s banked high and the shutters only rattle in a friendly way.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Kin bright-eyed and boots warm. The mountain will still be there in the morning — it\'s very reliable that way.' },
  ],
  'script.shop_kit_galehigh': [
    { op: 'say', speaker: 'KITE-KEEPER', text: 'In off the mine road! Then the climb-kit\'s yours — terrace custom, and no arguing with custom at festival.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', speaker: 'KITE-KEEPER', text: 'Two charges and two warm balms. The Stair above us is long and the glacier past it is longer — and Pale Vault keeps no counter, so stock HERE or go without.' },
    { op: 'setFlag', flag: 'flag:galehigh_kit' },
  ],
  'script.shop_galehigh': [
    { op: 'dialogue', ref: 'npc.galehigh_shopkeeper' },
    { op: 'shop', shop: 'galehigh' },
  ],

  // Galehigh caches (the standing variety: wicks, a valuable, the Updraft-gated
  // hidden find, the skyloft drop-box, and N1's ledge-herb).
  'script.pickup_galehigh_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: "A festival takings-tin, lidded against the gusts. Found 200 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_galehigh_wicks' },
  ],
  'script.pickup_galehigh_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Tucked under a terrace stone where the wind can\'t pry: a MOTH-AMBER, warm with old light!' },
    { op: 'setFlag', flag: 'flag:picked_galehigh_amber' },
  ],
  'script.pickup_galehigh_high': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'Only the thermals reach this ledge — and whoever left a BRIGHT BALM up here for the next flier. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_galehigh_high' },
  ],
  'script.pickup_skyloft_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A wind-ward\'s drop-box, lashed to the railing. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_skyloft_charge' },
  ],
  'script.pickup_ledge_herb': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'ledge_herb', count: 1 },
    { op: 'say', text: 'Growing wind-burnt and stubborn in the highest crack of the terrace: the LEDGE-HERB! Sharp and warm to the nose — the crag-tender on the Stair swears by it.' },
    { op: 'setFlag', flag: 'flag:picked_ledge_herb' },
  ],

  // N3 "Wren's Ribbon" — Mira, quietly, after the wobble (requires met_cor).
  'script.ribbon_quest': [
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'Wayfarer. No shouting today — come here a moment.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'Found this on the festival terrace after the Rising. It\'s Wren\'s — off their kite. They flew with us all evening and laughed in all the right places, and then I heard what the ice road did to them, up your way.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'wren_ribbon', count: 1 },
    { op: 'say', text: 'She presses a kite-ribbon into your hand, festival-smoke still in the weave. Received WREN\'S RIBBON!' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'neutral', text: 'There\'s a quiet ledge on the second stair — west side, behind the crag. Wren sat there an hour on the way up, flying nothing. Leave it there for them.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'Don\'t write anything. Don\'t wait. Some things you just leave where a friend will pass — the wind minds the rest.' },
    { op: 'setFlag', flag: 'flag:q_north_ribbon' },
  ],

  // R4 — the Waykeeper's Round, leg 4: the commissioned kite, kite-maker →
  // waystone kid. (The giver sets q_round_kite_taken; delivery sets q_round_kite.)
  'script.round_kite': [
    { op: 'say', speaker: 'KITE-MAKER', text: 'Ah — the kite-finder! Then you\'re the hands I\'ve been waiting on. The Waykeeper at the Crossroads commissioned this in the spring: one kite, sturdy, for the waystone kid.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'round_kite', count: 1 },
    { op: 'say', text: 'A small kite in Lanternway colours, wrapped against the road. Received the WAYSTONE KITE!' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'Built to survive an owner of eight, which is the hardest weather there is. Down the spoke to the Crossroads with it — and tell the kid: the string hand is everything. The kite already knows the rest.' },
    { op: 'setFlag', flag: 'flag:q_round_kite_taken' },
  ],
  'script.round_kite_deliver': [
    { op: 'say', speaker: 'WAYSTONE KID', text: 'Is that— it IS. It\'s MINE. The Waykeeper said it was coming with the next good Wayfarer and that I would know them by the walk and I DO—' },
    { op: 'narrate', text: 'The kid takes the kite the way some folk take a lamp at their naming. The Waykeeper, watching from the waystone, counts out your carriage-fee with great ceremony.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'Received 300 WICKS and 2 WARM BALMS — "Round rates, plus the weather."' },
    { op: 'say', speaker: 'WAYSTONE KID', text: 'The string hand is everything. I KNOW. Watch. ...Well, watch TOMORROW, when the wind\'s back. But then — watch!' },
    { op: 'setFlag', flag: 'flag:q_round_kite' },
  ],

  // --- Windward Stair: the climb, the kettle, the crags ----------------------
  'script.windward_craghand': [
    { op: 'say', speaker: 'EDDA', text: 'Hold at the bend, Wayfarer! Stair custom — the climb tests your legs, and the crag-hands test the rest.' },
    { op: 'battle', trainer: 'windward_craghand' },
    { op: 'say', speaker: 'EDDA', text: 'Four hundred and twelve steps I climb a day, and today the lesson walked UP to me. Well fought — the wind-gap\'s above, and it is exactly as rude as it sounds.' },
    { op: 'setFlag', flag: 'flag:windward_craghand_beaten' },
  ],
  'script.windward_galewatch': [
    { op: 'say', speaker: 'ROWAN', text: 'A lamp on the high leg! Good. The gale-watch greets every flame that climbs this far — and the greeting is a bout. Keeps us both warm.' },
    { op: 'battle', trainer: 'windward_galewatch' },
    { op: 'say', speaker: 'ROWAN', text: 'Warm enough. Mind the crag-tender\'s camp on the upper switchback — her kettle has saved more climbers than the rope has.' },
    { op: 'setFlag', flag: 'flag:windward_galewatch_beaten' },
  ],
  'script.windward_cragwatch': [
    { op: 'say', speaker: 'MERLE', text: 'Off the wind-gap with your boots still on — then you\'re worth a crag-watch\'s while. One bout, Wayfarer; the glacier ahead doesn\'t practise mercy and neither should you.' },
    { op: 'battle', trainer: 'windward_cragwatch' },
    { op: 'say', speaker: 'MERLE', text: 'That\'ll do. Pale Vault\'s down the far slope — walk in QUIET, mind. The whole town keeps a watch, and it isn\'t the kind with shouting.' },
    { op: 'setFlag', flag: 'flag:windward_cragwatch_beaten' },
  ],

  // N1 "The Crag-tender's Kettle" — the giver camps on the upper switchbacks.
  'script.kettle_quest': [
    { op: 'say', speaker: 'CRAG-TENDER', text: 'Sit a moment, child — everyone sits at this bend, it\'s where the legs find out what they\'ve agreed to. The kettle\'s on. The kettle is ALWAYS on.' },
    { op: 'say', speaker: 'CRAG-TENDER', text: 'Though it\'s a thin brew tonight, I\'ll own it. The proper one wants LEDGE-HERB — wind-burnt, sharp, grows in the high cracks of Galehigh\'s top terraces. My ledge days are forty years behind me.' },
    { op: 'say', speaker: 'CRAG-TENDER', text: 'But a Wayfarer with the Storm\'s own gift could ride the thermals up and pick a sprig before their tea cooled. If you ever do... my kettle would remember it.' },
    { op: 'setFlag', flag: 'flag:q_north_kettle' },
  ],
  'script.kettle_done': [
    { op: 'say', speaker: 'CRAG-TENDER', text: 'Ledge-herb! Look at it — burnt on the windward side, exactly right. You RODE for this.' },
    { op: 'narrate', text: 'She brews it slow, the way things are done at this height: melt-water, three pinches, patience. The steam off the kettle smells like a kinder season.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'warm_flask', count: 1 },
    { op: 'say', text: 'She fills her own felt-wrapped flask and folds your hands around it. Received the WARM FLASK!' },
    { op: 'say', speaker: 'CRAG-TENDER', text: 'For the glacier, child. When the chill gets into your kin past what a fire mends — that\'s the brew, and that\'s the flask, and now they\'re yours.' },
    // Only the done-flag here: her three placements key on picked_ledge_herb /
    // q_north_kettle_done, so both orders hold (herb-first skips kettle_quest
    // entirely; quest-first already set q_north_kettle there) — and nothing
    // consumes q_north_kettle, so it is not re-set.
    { op: 'setFlag', flag: 'flag:q_north_kettle_done' },
  ],

  // The crags band — flag:shortcut_windward is set by the trigger; this is the
  // "now accessible" callout that sells the drop home (spine §0 rule 3).
  'script.windward_crags': [
    { op: 'narrate', text: 'The stair tops out onto the high crags — bare, bright, the warm colours all spent somewhere below. Snow lies in the lee of every stone.' },
    { op: 'narrate', text: 'And off the south-west shelf, far down through clean air, Galehigh\'s terraces glow like banked coals. A glide-ledge drops straight toward them — the long climb home, repaid in one held breath.' },
    { op: 'say', text: 'The Windward shortcut stands open: a one-glide drop from the crags back to Galehigh\'s fires.' },
  ],

  // N3's payoff — wordless by design: ONE narration line, nothing else.
  'script.place_ribbon': [
    { op: 'narrate', text: 'You tuck Wren\'s ribbon under a stone at the quiet ledge\'s lip, where a friend who sat here once would see it — and the wind, for a wonder, lets it lie.' },
  ],

  // N2 viewpoint one — the Windward crag vista (the sketcher's first asking).
  'script.sketch_crag': [
    { op: 'narrate', text: 'The sketcher\'s first viewpoint. You stand at the crag\'s lip and look, properly, the way she asked: the whole North laid out under the aurora — the Stair falling away, Galehigh\'s small warm fires, the glacier ahead like a held wave.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'You stay until the cold finds your collar, fixing it all somewhere a sketch can be made from. One of three.' },
  ],

  // Windward caches (stair I: balm / wicks / valuable; stair II: amber + kit).
  'script.pickup_windward_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A climber\'s cache in the lee of the cairn, wax seal sound. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_windward_balm' },
  ],
  'script.pickup_windward_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: "A courier's purse, dropped on the switchback and wedged two bends down. Found 250 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_windward_wicks' },
  ],
  'script.pickup_windward_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Glinting in the scree where no lamp should reach: a STARGLASS SHARD, fallen from a sky this stair climbs toward!' },
    { op: 'setFlag', flag: 'flag:picked_windward_shard' },
  ],
  'script.pickup_windward_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'In a crack of the crag, out of the weather: a MOTH-AMBER, its caught shimmer still turning. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_windward_amber' },
  ],
  'script.pickup_windward_kit': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'A crag-watch relief cache — a balm and a charge for whoever the mountain is hardest on today. Took them!' },
    { op: 'setFlag', flag: 'flag:picked_windward_kit' },
  ],

  // Wind-Eye + Thunderroost — the Updraft spurs pay (10-economy cache variety).
  'script.pickup_windeye_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'A flier\'s offering-box in the alcove, dry as the day it was lashed shut. Found 2 BEACON CHARGES — left, perhaps, for exactly the kin that nest in the Eye.' },
    { op: 'setFlag', flag: 'flag:picked_windeye_charge' },
  ],
  'script.pickup_windeye_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'At the oculus\'s rim, where the wind sets down what it loves best: a STARGLASS SHARD, singing very faintly in the updraft!' },
    { op: 'setFlag', flag: 'flag:picked_windeye_glass' },
  ],
  'script.pickup_roost_prize': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'chart_tempest', count: 1 },
    { op: 'say', text: 'Wedged behind the boulder choke, in a bone-dry chart-tube older than the dusk: a STAR-CHART: TEMPEST — pressed at the aerie itself, the only one of its figure!' },
    { op: 'say', text: 'Above you, the storm-birds shift on the nest and permit it. Apparently.' },
    { op: 'setFlag', flag: 'flag:picked_roost_prize' },
  ],

  // --- Pale Vault: the Lamp-Line (spine §5 shape #6) -------------------------
  // Ysolde's hook at the undercroft door (sets flag:q_north_lampline).
  'script.ysolde_quest': [
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'You walked in off the crags. Good. The light should be free to all who seek it — no Gift, no gate, only the cold, and the cold is honest.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'Look through the blue ice, there, beside the door. Seven brackets, descending. Dark a long time now. They are my vault\'s whole liturgy, and I have not had a flame worth walking them.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Cold does not hate the flame, wanderer. It only waits to see if the flame means it. Walk my vault. Light the seven brackets, in order, none hurried — and let me see the light hold.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'They burn aurora-oil, and only that. The tallow-keeper in the approach hollows renders it — though I hear her hearth went out in the storm, and an unlit hearth renders nothing. Begin there.' },
    { op: 'setFlag', flag: 'flag:q_north_lampline' },
  ],

  'script.pickup_stormwood': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'stormwood', count: 1 },
    { op: 'say', text: 'Storm-felled wood off the Windward heights, stacked by the wind itself and dry under the snow-crust. Took an armful of STORM-KINDLING!' },
    { op: 'setFlag', flag: 'flag:picked_stormwood' },
  ],

  // The tallow-keeper's hearth relit + the oil rendered (her camp's doused→lit
  // MapObject pair swaps on flag:q_north_aurora_oil).
  'script.render_oil': [
    { op: 'say', speaker: 'TALLOW-KEEPER', text: 'Storm-kindling! Dry to the heart — the mountain does love a Wayfarer. Give it here, and stand out of the smoke\'s way.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.24, ms: 600 },
    { op: 'narrate', text: 'The hearth takes the wood like an apology accepted. Warmth crawls back into the stones, and the kettle, and — visibly, by degrees — the keeper.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'She renders the tallow slow and pale, tilting the pan toward the sky now and then — "so it remembers" — until the oil holds a faint moving light that is not the fire\'s.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'aurora_oil', count: 1 },
    { op: 'say', text: 'Received the AURORA-OIL!' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: 'And the rendering-fee, pressed on you over your objections: 200 WICKS. "The vault pays its lamplighters. It always has."' },
    { op: 'say', speaker: 'TALLOW-KEEPER', text: 'Seven brackets, child, and they light in ORDER — a line is a promise kept one lamp at a time. Ysolde will tell you the same, with longer pauses.' },
    { op: 'setFlag', flag: 'flag:q_north_aurora_oil' },
  ],

  // B3 — CÒR APPEARS (the midgame's emotional spine; cinematics.md binding:
  // letterbox, the aurora bed to near-silence, long portrait holds, the cool
  // tint on the quieted vista, NO battle). The trigger sets flag:met_cor.
  // He is courteous, sad, REASONABLE — grief dressed as mercy. The player
  // should walk away half-agreeing, and hating that they do.
  'script.cor_appears': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'The wind stops. On open ice that should mean nothing. It does not feel like nothing.' },
    { op: 'narrate', text: 'A figure stands on the drained shelf below the lane — cowled, unhurried, hands folded. As if he has been waiting exactly as long as was polite.' },
    { op: 'cameraFocus', actor: 'cor_figure', ms: 1000 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'Good evening, apprentice. Forgive the theatre of meeting you out here — I find towns flinch at me, and I have grown careful of other people\'s evenings.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'I am Còr. The gentle ones you met in the grey wood — the lanterns built to hold nothing — they are mine. You have been undoing my work, kindly and well, for some weeks. I thought you were owed a face.' },
    { op: 'narrate', text: 'He turns, and his hand moves over the valley below the shelf — grey moss, still ice, a quiet with no edges to it.' },
    { op: 'tint', color: '#2a3550', alpha: 0.38, ms: 1000 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'Look at it. Truly look, before anyone tells you what to see. No lamp gutters here. No wick burns down while somebody watches, helpless, pretending to mend nets. Nothing in this valley will ever be lost again — because nothing in it is still spending itself.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'You keep lamps. Then you already know the cruellest thing about them: a lamp asks to be WATCHED. Every light you have relit on your road, you have volunteered someone to grieve.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'I am not your enemy, apprentice. I am only tired of grief — and I think, if you are honest with the hour, so is everyone you have ever lit a lamp for.' },
    { op: 'narrate', text: 'It would be easier if he were wrong in some plain, loud way. Standing here, with the valley so still — it is not loud, and it is not plain.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'Fenn will come — he always comes, after me, like the apology after the truth. Ask him whether the sky was worth what it cost him. He will say yes. Watch his face while he says it.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'No — I will not fight you. The Hollowing takes nothing from the unwilling, whatever the wardens tell their halls. Keep your Gleams. Light your seven brackets. I only leave you a question, since you are collecting things:' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'When the last light you love fails — and it will, that is what loving a light means — would you rather have watched it burn... or been spared the dark after? Take your time. I did.' },
    { op: 'tint', color: '#2a3550', alpha: 0, ms: 1000 },
    { op: 'narrate', text: 'He bows — courteous, unhurried — and walks into the dark between the ice-spires, and the dark does not trouble him at all.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'The wind remembers itself. The aurora overhead seems thinner than it did, and you cannot decide whether it truly is.' },
    { op: 'cameraReset', ms: 700 },
    { op: 'musicCrossfade', key: 'pale-vault-glacier-a', ms: 1400 },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // C3 — Fenn and the shared past. On Còr's heels: two faces and the quiet.
  // No swell, no sting; the trigger sets flag:fenn_c3.
  'script.fenn_shared_past': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'Child. I came as fast as these legs agree to come, and still — he was already here. I can feel the quiet he leaves. Like a room where a clock has stopped.' },
    { op: 'narrate', text: 'Fenn looks at the drained shelf for a long time. He does not ask what Còr said. He seems to know it by heart.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'We read the same sky once, he and I. Two star-tenders, one ladder, forty years of cold mornings. I steadied the ladder. He named the stars as they came loose.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'And then we lost the same thing, in the same season. I will not tell you what — it is half his grief, and I do not lend out what is half another man\'s.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'neutral', text: 'He chose to stop the cycle, so it could never hurt anyone again. I chose to keep lighting lamps, knowing every one of them will someday want lighting again. Two answers, child. One question. You have now heard it asked in his voice.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: '...I still believe I was right. And I have never once stopped understanding him. Both of those are true, and carrying both is the whole weight of being his friend.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'So do not hate him — hating him misses the point of him entirely. OUT-REMEMBER him. Every lamp you relight is a thing he has made himself forget the feel of. It is the only argument I have ever seen him flinch at.' },
    { op: 'narrate', text: 'He presses your shoulder once, and goes, slower than he came. The quiet stays a while after him.' },
  ],

  // A4 — WREN'S WOBBLE at the undercroft door: the hard rival battle, at the
  // exact threshold of the light-holding trial. Opens on 'unsure'; afterward
  // silence and an unresolved exit — Wren is NOT consoled (that is A5's work).
  'script.wren_pale_vault': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'Oh. It\'s you. ...Of course it\'s you.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'I talked to him. Còr. Out on the ice, same as you, I\'d wager. Everyone says you don\'t talk to the Hollowing — nobody warns you that he\'s KIND. That\'s the unfair part.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'I keep doing the sums and they keep coming out his way. No more guttering. No more goodbyes. Every town he\'s quieted, nothing in it got HURT. Tell me what\'s wrong with that. Go on. Because I\'ve been standing at this door an hour and I can\'t find it.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'You\'re about to walk down there and prove a light can hold. And I\'m up here wondering if I even want it to.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'So show me. Properly. No friendly-battle rules, no two-levels-kinder — everything you have. Because if YOUR light can\'t make me feel it... then maybe there\'s nothing to feel.' },
    { op: 'battle', trainer: 'wren_pale_vault' },
    { op: 'silence', ms: 1600 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'You fight like you\'ve got something the dark can\'t take. I don\'t know if I\'ve got that.' },
    { op: 'narrate', text: 'Wren looks at the undercroft door for a long moment. Then away from it.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: '...I need to walk a while. Don\'t follow me. Please.' },
    { op: 'narrate', text: 'They go — not toward town, not toward anywhere in particular. The wind takes their footprints almost as fast as they leave them.' },
    { op: 'setFlag', flag: 'flag:wren_pale_vault_battled' },
  ],

  // The undercroft's two frost-ward sight keepers (dungeon keeper class).
  'script.undercroft_ward_a': [
    { op: 'say', speaker: 'SELA', text: 'Hold, lamplighter. The second gallery is mine to keep — and the vault admits no flame the wards haven\'t weighed. The brackets deserve that much care.' },
    { op: 'battle', trainer: 'undercroft_ward_a' },
    { op: 'say', speaker: 'SELA', text: 'Weighed and worthy. Walk on — and keep your order. The line knows when it\'s been skipped.' },
    { op: 'setFlag', flag: 'flag:undercroft_ward_a_beaten' },
  ],
  'script.undercroft_ward_b': [
    { op: 'say', speaker: 'ORRIN', text: 'The third gallery, and the last ward. Ysolde waits at the heart, and I send her nothing the cold could blow out on the way.' },
    { op: 'battle', trainer: 'undercroft_ward_b' },
    { op: 'say', speaker: 'ORRIN', text: 'Steady to the last. Finish the line, Wayfarer — the vault has waited years to be bright.' },
    { op: 'setFlag', flag: 'flag:undercroft_ward_b_beaten' },
  ],

  // The seven brackets — lit in line, mounting quiet wonder. (Each trigger
  // chains on the previous flag; the lit/dark bracket objects swap on them.)
  'script.light_lamp_1': [
    { op: 'narrate', text: 'The first bracket. You tip the aurora-oil into the old iron well and touch your vesperlamp to the wick.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.18, ms: 500 },
    { op: 'narrate', text: 'It takes — pale and cool, a flame the colour of the sky outside. The aurora, come indoors. One.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 600 },
  ],
  'script.light_lamp_2': [
    { op: 'narrate', text: 'The second bracket takes the flame — and the ICE takes the light. It runs into the blue wall like water into a vein, glowing faintly a full arm-span deep.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.2, ms: 500 },
    { op: 'narrate', text: 'Two. Behind you, the first lamp burns on. You had not realised you were checking.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 600 },
  ],
  'script.light_lamp_3': [
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Three. As the wick catches, the light finds something IN the wall: a lamplighter\'s mark, scratched beside the bracket by some cold-stiff hand, years and years of dark ago.' },
    { op: 'narrate', text: 'Someone walked this line before you. The vault kept their soot. It has been waiting, the whole time, to be a lit place again.' },
  ],
  'script.light_lamp_4': [
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.22, ms: 600 },
    { op: 'narrate', text: 'Four — past the halfway. You look back up the gallery and the line LOOKS BACK: four pale flames hung in blue ice, and your own shadow walking beside you like a second lamplighter.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
  ],
  'script.light_lamp_5': [
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Five. And the vault begins, very quietly, to HUM — the ice carrying some held note from bracket to bracket, the way a glass sings under a wet finger.' },
    { op: 'narrate', text: 'It is not a cold sound. You would not have believed that, an hour ago.' },
  ],
  'script.light_lamp_6': [
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.24, ms: 700 },
    { op: 'narrate', text: 'Six. Above the sixth bracket the ice ceiling thins, and through it — blurred, green, moving — the aurora itself, bending along its slow road. The flame below it leans the same way.' },
    { op: 'narrate', text: 'Sky above, sky within. One bracket left.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
  ],
  'script.light_lamp_7': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'silence', ms: 1300 },
    { op: 'narrate', text: 'The seventh bracket. You pour the last of the aurora-oil, steady your hand against the cold iron, and ask your flame to cross one more time.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.34, ms: 900 },
    { op: 'narrate', text: 'Seven. The whole line stands lit behind you, door to heart — and the vault ANSWERS: every wall waking blue-green at once, the hum settling into something like a chord, the dark walked all the way down.' },
    { op: 'narrate', text: 'The light holds.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 1100 },
    { op: 'say', speaker: 'YSOLDE FROST', text: '...So. It holds.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // Lumenary 6 — Ysolde Frost at the vault's heart. Win → gleam:frost +
  // Emberward; with Storm already held the ENGINE closes flag:crown_north.
  // Cool minor→major: the cold mirror of Galehigh's warm ceremony.
  'script.lumenary_pale_vault': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'ysolde_vault', facing: 'down' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Seven flames, walked in order, none hurried. I watched the light arrive ahead of you, wanderer. It spoke well of its keeper.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'One asking remains, and it is the same one. Cold does not hate the flame — it only waits to see if the flame means it. Warm your kin... and let me see the light hold.' },
    { op: 'battle', trainer: 'ysolde_frost' },
    { op: 'musicFade', ms: 600 },
    { op: 'silence', ms: 1200 },
    { op: 'tint', color: '#9fd4ff', alpha: 0.36, ms: 800 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Ysolde lifts her lamp, and the seven brackets rise with it — their light climbing the blue ice, floor through ceiling, out into the night above. And high over the glacier, the FROST remembers how to shine.' },
    { op: 'gleam', element: 'frost' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 1000 },
    { op: 'tint', color: '#9fd4ff', alpha: 0, ms: 1000 },
    { op: 'narrate', text: 'And it does not stop there. Storm and Frost stand together now — and between them the whole northern quadrant of the Skyweave Crown closes overhead, quiet as snowfall. Out on the festival ice, one by one, the watchers lift their lamps.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'warm', text: 'The Frost Gleam, and the northern crown with it. You have made my vault a lit place, wanderer. I do not have the words for what that is — so I will give you something better than words.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'The Emberward. A tended ember the coldfog cannot snuff — the Hollowing\'s mist parts before it. The pass west of town has been shut to every flame in this valley for years. Yours, now, it will not shut out.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'warm', text: 'Go and stand the Aurora-watch before you walk on. You have earned the right to hold a lamp among us — and that is the whole ceremony, and it is enough.' },
  ],

  // Arc E — the Aurora-watch: the SILENT VIGIL. Stage as silence + slow light;
  // it rhymes with Còr's calm — and refutes it (the lamps are LIT). No humour.
  'script.pale_vault_aurora_watch': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'The town stands out on the festival ice, spaced wide as standing stones, every face turned up. Nobody speaks. The vigil-keeper raises one hand.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.14, ms: 900 },
    { op: 'narrate', text: 'A single lamp lights at the line\'s end.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.2, ms: 900 },
    { op: 'narrate', text: 'Then the next. Then the next — lamp answering lamp down the whole standing line, unhurried as the aurora walking its slow green road overhead.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.26, ms: 1100 },
    { op: 'narrate', text: 'A lamp is put into your hands. You light it from your vesperlamp and hold it, and stand, and look up, and that is all that is asked.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 900 },
    { op: 'silence', ms: 1400 },
    { op: 'narrate', text: 'It is very calm, out on the ice. As calm as any quieted valley. But nothing here has been surrendered to the dark — every point of stillness is a kept flame, watched by someone who chose to watch. The lamps burn. That is the whole of the Aurora-watch.' },
    { op: 'say', speaker: 'VIGIL-KEEPER', text: 'It is enough to stand. It is enough to burn. Keep the watch as long as you wish, Wayfarer — the sky knows you are here.' },
    { op: 'musicCrossfade', key: 'pale-vault-glacier-a', ms: 1400 },
    { op: 'letterbox', on: false, ms: 420 },
    { op: 'setFlag', flag: 'flag:aurora_watch_seen' },
  ],

  // N2 "The Aurora Sketcher" — the painter at the festival ice; pure stillness.
  'script.sketch_quest': [
    { op: 'say', speaker: 'SKETCHER', text: 'Mind the easel, please — forty years I have tried to put that sky on paper, and it has never once held still for me. We have an understanding. I keep failing; it keeps being worth it.' },
    { op: 'say', speaker: 'SKETCHER', text: 'There are three views I need and my knees no longer agree to: the Windward crag above the wind-gap, the glacier shore west of town, and this festival ice from the far brazier line.' },
    { op: 'say', speaker: 'SKETCHER', text: 'Go and STAND in them, Wayfarer. Look properly — long enough to be cold — then come back able to tell me what the light DID. Lend me your eyes, and I\'ll finish the sketch I started forty years ago.' },
    { op: 'setFlag', flag: 'flag:q_north_sketch' },
  ],
  'script.sketch_shore': [
    { op: 'narrate', text: 'The glacier shore. The ice stands off the water like a wave that was asked to wait — and the aurora lies doubled in the black shallows, two slow green roads, one above and one below.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'You stand until you can keep it. Two of three.' },
  ],
  'script.sketch_festival': [
    { op: 'narrate', text: 'The far brazier line. From here the festival ice is people-shaped lamplight — the whole town small under the sky, each holding their single flame, none of them hurrying it.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'The sky does its slow work overhead, and the town simply keeps it company. Three of three. The sketcher will want to hear about this one slowly.' },
  ],
  'script.sketch_done': [
    { op: 'say', speaker: 'SKETCHER', text: 'Sit. Talk. Slowly — the crag first.' },
    { op: 'narrate', text: 'You tell her. The North laid out under the aurora; the wave that waits; the town keeping the sky company. She works the whole time, charcoal first, then the pale washes, glancing up at you instead of the sky.' },
    { op: 'say', speaker: 'SKETCHER', text: '...There. Forty years, and what I was missing was somebody to hold still INSTEAD of the sky. Look at it. We made that, you and I and three cold views.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'aurora_charm', count: 1 },
    { op: 'say', text: 'She unclips a charm from her easel — dipped in aurora-oil, faintly aglow — and gives it over. Received the AURORA CHARM!' },
    { op: 'giveMoney', amount: 400 },
    { op: 'say', text: 'And her colour-fund, folded into your hand without negotiation: 400 WICKS.' },
    { op: 'say', speaker: 'SKETCHER', text: 'Raise it toward a Frost-hearted kin and your lamp burns the way the sky does tonight. Toward anything else it is only a lamp — the aurora keeps its own, same as the sea.' },
    { op: 'setFlag', flag: 'flag:q_north_sketch_done' },
  ],

  // Pale Vault rest + caches (no shop here — the town is deliberately sparse).
  'script.pale_vault_inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'Come in quiet, Wayfarer. The hearth is low but it is LIT, and that is the house\'s whole boast.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'INNKEEP', text: 'Rested, and your kin with you. The watch keeps the night; you needn\'t.' },
  ],
  'script.pickup_pale_vault_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'A watcher\'s cache in the lee of the hollow, felt-wrapped against the frost. Found 2 WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_pale_vault_balm' },
  ],
  'script.pickup_pale_vault_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: "A trader's purse, frozen into a drift and chipped patiently free. Found 300 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_pale_vault_wicks' },
  ],
  'script.pickup_pale_vault_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Deep in the blue ice, where only a warded flame walks: a STARGLASS SHARD, holding its constellation like a breath. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_pale_vault_shard' },
  ],
  'script.pickup_pale_vault_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'An offering left at the brazier line, wax seal sound. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_pale_vault_charge' },
  ],
  'script.pickup_undercroft_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'In a niche behind the second gallery, dry these hundred years: a MOTH-AMBER, its little light untroubled by all that ice. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_undercroft_amber' },
  ],
  'script.pickup_undercroft_balm': [
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'A lamplighter\'s reserve, cached a choke off the line for the worst night: a BRIGHT BALM. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_undercroft_balm' },
  ],

  // ===========================================================================
  // THE WEST (walkthrough/04-west) — Hushfrost Pass (X1, the caretaker),
  // the Sunken Solarium (Lumenary 7: Lucan Pyre, the Lit Stage + the
  // Last-Warm-Day), the Sunvault Climb + Helia Vault, the Coldfog detour
  // (B4's shown half — ZERO humour), and Nightreach Observatory (Lumenary 8:
  // Nessa Cole, the Vigil of the Seven carrying C4/A5/B4). Staging per
  // cinematics.md: the West is the threshold of the endgame — cold ache →
  // golden bittersweet → drained dread → reverent vastness.
  // ===========================================================================

  // --- Hushfrost Pass I — the snow canyon's three route sight trainers -------
  'script.hushfrost_lampman': [
    { op: 'say', speaker: 'DUNSTAN', text: 'Hold there, Wayfarer! That fog at the throat has been beating my lamp back a season at a time — so the pass has one rule now. Every flame that means to face it gets weighed first. By me.' },
    { op: 'battle', trainer: 'hushfrost_lampman' },
    { op: 'say', speaker: 'DUNSTAN', text: 'That will burn through, I reckon. The throat is west — walk warded, and do not stop to listen to the fog. It has nothing kind to say.' },
    { op: 'setFlag', flag: 'flag:hushfrost_lampman_beaten' },
  ],
  'script.hushfrost_survivor': [
    { op: 'say', speaker: 'HESPER', text: 'Stop a moment. I came out of the deep fog once on one lamp and no luck — so now I test every flame that passes. Call it a toll. Call it a kindness. It is both.' },
    { op: 'battle', trainer: 'hushfrost_survivor' },
    { op: 'say', speaker: 'HESPER', text: 'Steady right through. Good. Then it will not be you I lie awake over.' },
    { op: 'setFlag', flag: 'flag:hushfrost_survivor_beaten' },
  ],

  // --- Hushfrost Pass II — the coldfog throat + X1 "The Caretaker's Lamp" ----
  'script.hushfrost_thawtender': [
    { op: 'say', speaker: 'TILDA', text: 'Mind the lane — I have just swept it! Rime off the gold mouth, every morning, so the warmth shows through. A clear road is paid for with a bout; that is the rule I brought with me.' },
    { op: 'battle', trainer: 'hushfrost_thawtender' },
    { op: 'say', speaker: 'TILDA', text: 'Well fought. And look — the gold on the fog is real. Stored daylight, a whole drowned gardenful of it. Walk toward the warmth, Wayfarer.' },
    { op: 'setFlag', flag: 'flag:hushfrost_thawtender_beaten' },
  ],
  // X1, the ask. Grief register — zero humour anywhere near this shelter.
  // She sits with a numbed Hearthkit the coldfog touched; the kin SLEEPS,
  // and stays asleep (B-arc weight; it wakes only at flag:dawn, postgame).
  'script.caretaker_quest': [
    { op: 'say', speaker: 'CARETAKER', text: 'Soft, now. She is sleeping. ...She is always sleeping, since the fog came through.' },
    { op: 'say', speaker: 'CARETAKER', text: 'It used to glow like a hearth. Now it just sleeps. They tell us that\'s mercy. I light a lamp by it anyway.' },
    { op: 'say', speaker: 'CARETAKER', text: 'Only my lamp is down to the dregs, and the only oil that holds against this cold is aurora-oil — the kind that remembers the sky. It pools in the hollow north of here, under the old ice. My knees stopped being equal to that road years ago.' },
    { op: 'say', speaker: 'CARETAKER', text: 'You carry a warded flame. If you would fill an old woman\'s lamp... she would sleep in the light, at least. That is not nothing. That is nearly everything I have left to give her.' },
    { op: 'setFlag', flag: 'flag:q_west_caretaker' },
  ],
  'script.caretaker_done': [
    { op: 'say', speaker: 'CARETAKER', text: 'Aurora-oil. You walked the hollow for us.' },
    { op: 'narrate', text: 'She fills the lamp slowly, the way things are done when they matter. The flame takes — pale and steady, with a faint moving light in it that is not the fire\'s.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'The light settles over the sleeping kin. It does not wake. But something in the set of it eases — the way a sleeper eases when a door is closed against the cold.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 800 },
    { op: 'say', speaker: 'CARETAKER', text: 'There. She sleeps easier in the light. ...So will I, now.' },
    { op: 'say', speaker: 'CARETAKER', text: 'Take my own bright lamp, Wayfarer — I kept it for a steadier hand than mine, and here one is. May every wild heart you raise it toward know it was a watched flame.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'caretaker_lamp', count: 1 },
    { op: 'say', text: 'Received the BRIGHT LAMP!' },
    { op: 'setFlag', flag: 'flag:q_west_caretaker_done' },
  ],

  // Hushfrost caches (the standing variety: wicks / balms / the missable shard).
  'script.pickup_hushfrost_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: "A courier's purse, frozen into the drift and chipped patiently free. Found 300 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_wicks' },
  ],
  'script.pickup_hushfrost_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A climber\'s cache on the wind-blown terrace, felt-wrapped against the cold. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_balm' },
  ],
  'script.pickup_hushfrost_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Deep in a wall-hollow past the lamp\'s easy reach: a STARGLASS SHARD, cold as the sky it fell from. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_shard' },
  ],
  'script.pickup_hushfrost_warm_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Left on the shelter\'s sill for whoever the fog is hardest on today. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_warm_balm' },
  ],
  'script.pickup_hushfrost_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'In the lee of a blighted finger, untouched by the grey: a MOTH-AMBER, its little caught shimmer still turning. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_amber' },
  ],

  // --- Aurora Hollow — the Emberward spur (X1's oil + the detour's own pay) --
  'script.pickup_aurora_oil': [
    { op: 'narrate', text: 'In the deepest pocket of the hollow the aurora pools UNDER the ice — and where it pools, the old renderers left their catch-jars, sealed and waiting.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'aurora_oil', count: 1 },
    { op: 'say', text: 'One jar still holds true — a pale oil with a slow light moving in it. Took the AURORA-OIL!' },
    { op: 'setFlag', flag: 'flag:picked_aurora_oil' },
  ],
  'script.pickup_aurora_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'An offering-box wedged in the blue ice, wax seals sound. Found 2 BEACON CHARGES — left, perhaps, for exactly the kin that den under the lights.' },
    { op: 'setFlag', flag: 'flag:picked_aurora_charge' },
  ],
  'script.pickup_aurora_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Under the vault where the aurora burns brightest, the ice gives one back: a STARGLASS SHARD, green-lit to its heart. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_aurora_shard' },
  ],

  // --- Sunken Solarium — arrival (the Arc D pivot: warmth, remembered) -------
  'script.solarium_arrival': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The fog thins — and the cold simply stops, the way a held breath stops. Ahead, half-drowned in still black water, a ruined sun-garden GLOWS.' },
    { op: 'tint', color: '#ffd089', alpha: 0.26, ms: 900 },
    { op: 'narrate', text: 'Stored daylight, shining up through the flood. Golden architecture gone soft at the edges. Warmth — real warmth, on your face, for the first time since the south.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'They say the sun drowned here. Standing in its light, you would swear it was only sleeping.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // E — the Last-Warm-Day (banded on the festival terrace). Bittersweet,
  // golden, a little defiant — the fire-warm swell AFTER the coldest regions.
  // The build-up may smile; the crest itself is sincere (humour rules).
  'script.solarium_last_warm_day': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 600 },
    { op: 'narrate', text: 'The sunlit terrace is full of people. Stored-daylight lanterns on every table, warm bread passing hand to hand, and the whole drowned garden gold around them — the Last-Warm-Day, underway.' },
    { op: 'tint', color: '#ffd089', alpha: 0.3, ms: 900 },
    { op: 'musicCrossfade', key: 'sunken-solarium-b', ms: 1200 },
    { op: 'narrate', text: 'Once a year, the Solarium gathers to spend the last warm day before the dark — daylight saved all season, spent all at once, on purpose, together.' },
    { op: 'say', speaker: 'FESTIVAL ELDER', text: 'Sit, Wayfarer. Eat something warm. The dark gets the whole rest of the year — today is OURS, and we spend it where it can see us.' },
    { op: 'narrate', text: 'Somebody presses bread into your hands, oven-warm. Nobody asks if you have earned it. That is the whole custom: warmth, spent freely, knowing it fades.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1100 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // --- The Lit Stage (spine §5 shape #7) — Lucan's hook ----------------------
  'script.lucan_quest': [
    { op: 'say', speaker: 'LUCAN PYRE', text: 'STOP — hold the light just there. Yes. An apprentice lamp-tender, six Gleams over one shoulder, walking out of a frozen pass into MY festival. You could not have staged a better entrance with a season of rehearsal.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'They say the sun drowned here, apprentice. I say it only went to sleep — and every warm day we spend is a promise we made to wake it. Tonight the troupe plays the closing scene of the year... on a dark stage. Three braziers, dead as the deep water.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'A bond that remembers the sun! Then prove the memory — the stage is dark and the daylight\'s drowned. Fetch it up, spark by spark.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'Three sunmote phials wait in the flooded halls — stored daylight, sunk where only a called tide can walk. Pearlmoor taught you that art long ago. Light my stage, Wayfarer, and the Solar Gleam will have a floor worth standing on.' },
    { op: 'setFlag', flag: 'flag:q_west_stage' },
  ],

  // The three sunmote phials (Tidecall water; each lighting wakes the next glimmer).
  'script.sunmote_1': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'sunmote_phial', count: 1 },
    { op: 'say', text: 'On a drowned islet, glinting through the black water: a SUNMOTE PHIAL, warm through the glass. One spark of the drowned daylight, fetched up.' },
    { op: 'setFlag', flag: 'flag:q_west_mote_1' },
  ],
  'script.sunmote_2': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'sunmote_phial', count: 1 },
    { op: 'say', text: 'The second phial, woken by the first brazier\'s glow — it shines from a far-shore pocket like a coin at the bottom of a well. Fetched it up!' },
    { op: 'setFlag', flag: 'flag:q_west_mote_2' },
  ],
  'script.sunmote_3': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'sunmote_phial', count: 1 },
    { op: 'say', text: 'The last phial, deepest in the halls, burning softly through the flood like a sunrise under glass. Three sparks of daylight, fetched up — back to the braziers!' },
    { op: 'setFlag', flag: 'flag:q_west_mote_3' },
  ],

  // The three braziers — escalating warmth; the troupe reacts per lighting.
  // (Trigger chain sets the brazier flags; the night-flower rows bloom per
  // lighting — a purely visual Sunsketch foreshadow.)
  'script.brazier_1': [
    { op: 'narrate', text: 'You pour the first phial into the cold brazier. For a breath, nothing — then the stored daylight takes the coals all at once.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Gold light climbs the broken proscenium. Along the stage rim, a row of shut night-flowers stirs — and BLOOMS, leaning into the warmth like an audience leaning forward.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'Across the water, the troupe has gone very quiet. One of them is gripping another\'s arm. One brazier burns. Out in the drowned halls, something else has begun to glimmer.' },
  ],
  'script.brazier_2': [
    { op: 'narrate', text: 'The second phial. The brazier drinks it and FLARES — and this time the light reaches the costumes, the gilt, the painted sun on the backdrop nobody has seen lit in forty years.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.28, ms: 800 },
    { op: 'narrate', text: 'A second row of night-flowers blooms along the rim. Somewhere behind you a troupe player starts humming the overture, catches themselves, and does not stop.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 800 },
    { op: 'narrate', text: 'Two braziers burn. The stage is more light than shadow now — and the last glimmer waits in the deepest hall.' },
  ],
  'script.brazier_3': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The last phial, into the last brazier. You stand back.' },
    { op: 'silence', ms: 900 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.36, ms: 1000 },
    { op: 'narrate', text: 'The Heliarium stage lights WHOLE — three crowns of stored daylight, the proscenium gold rim to rim, the final row of night-flowers blooming so fast you hear it, a soft sound like rain starting.' },
    { op: 'narrate', text: 'And the troupe takes the stage. No cue, no speech — they simply walk into the light they have waited forty years for, and the festival on the terrace rises to its feet.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1000 },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'HOUSE UP! The stage is LIT! — apprentice, when you are ready, it is yours. The Solar Gleam is tested on those boards tonight, and not before the closing scene. I have WAITED for this curtain.' },
    { op: 'musicCrossfade', key: 'sunken-solarium-b', ms: 1000 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // Lumenary 7 — Lucan Pyre, ON the lit stage. Win → gleam:solar + Sunsketch
  // (TRAINERS['lucan_pyre'] carries the grants). The binding Gleam cadence,
  // fire-warm — the Arc D pivot's payoff after the coldest regions.
  'script.lumenary_solarium': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'Centre stage, apprentice — the light loves you, do not argue with it. Spark by spark you woke my theatre; now show me the bond that did it.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'The closing scene of the Last-Warm-Day, played on a lit stage, for the first time since the night fell. Places... and BEGIN!' },
    { op: 'battle', trainer: 'lucan_pyre' },
    { op: 'musicFade', ms: 500 },
    { op: 'silence', ms: 1000 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.4, ms: 800 },
    { op: 'narrate', text: 'Lucan raises his lamp like a curtain call — and every stored-daylight lantern on the terrace lifts with it, a hundred small suns offered up over the drowned garden. And overhead, the SUN\'S OWN constellation takes the light.' },
    { op: 'gleam', element: 'solar' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'The SOLAR GLEAM stands! Seven relit — listen to the house! Forty years we played "The Sun Returns" to a dark sky, and tonight the sky read the script!' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'And no performer leaves my stage unpaid. The Sunsketch — a pocket of daylight, yours to release. Shut night-flowers bloom into bridges at its touch.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'The sun-vine bridge on the Climb west of here has been shut since the night fell — it will open UNDER YOUR FEET now. And the sealed Helia Vault off the high terraces... ah, but that would be telling. Some doors deserve their reveal.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'Go and spend what is left of the warm day with us first, apprentice. Encores are short. That is what makes them encores.' },
  ],

  // X2 "The Troupe's Sun-mask" — the post-stage troupe player's ask.
  'script.mask_quest': [
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'Wayfarer — a small thing, while the stage is yours. Our gilt sun-mask, the face of the closing scene... it sank in the side room off the flooded halls, the winter the water rose. Forty years of "The Sun Returns", and the sun has been understudied by a PAINTED PLATE.' },
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'You walk the called tide like a garden path. Dive the side room and bring our face home — tonight of all nights, the scene should wear its own gold.' },
    { op: 'setFlag', flag: 'flag:q_west_mask' },
  ],
  'script.pickup_sun_mask': [
    { op: 'narrate', text: 'In the drowned side room, half-buried in silt, something smiles up through the black water.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'sun_mask', count: 1 },
    { op: 'say', text: 'Recovered the GILT SUN-MASK — silt-scoured, smiling, and somehow still warm.' },
    { op: 'setFlag', flag: 'flag:picked_sun_mask' },
  ],
  'script.mask_done': [
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'The mask! Oh — look at it. Look at HIM. Silt in the smile and not a scratch on the gold.' },
    { op: 'narrate', text: 'She holds it up to the brazier-light, and for a moment the painted face and the stage\'s stored daylight wear the same warmth.' },
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'The closing scene wears its own sun tonight, thanks to you. Here — pressed from the mask\'s spare gilt, the way the old prop-masters made their luck. The festival\'s thanks, and mine.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'sun_charm', count: 1 },
    { op: 'say', text: 'Received the SUN CHARM!' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'And a share of the night\'s takings, pressed on you over your objections: 300 WICKS!' },
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'Raise it toward a Solar-hearted kin and your lamp plays the remembered noon. Toward anyone else it is only a lamp — every prop knows its scene.' },
    { op: 'setFlag', flag: 'flag:q_west_mask_found' },
  ],

  // The troupe's two sight trainers on the flooded lanes (route class).
  'script.troupe_player_a': [
    { op: 'say', speaker: 'CALLA', text: 'A walker in the wings! House rule, friend — nobody crosses the flooded lanes during rehearsal without giving the understudies a scene. We are VERY behind on scenes.' },
    { op: 'battle', trainer: 'troupe_player_a' },
    { op: 'say', speaker: 'CALLA', text: 'Upstaged in my own water. Go on through — and if you find any daylight down there, it is SPOKEN FOR.' },
    { op: 'setFlag', flag: 'flag:troupe_player_a_beaten' },
  ],
  'script.troupe_player_b': [
    { op: 'say', speaker: 'ORSINO', text: 'HALT — forgive me, that is the line from act two, it comes out when I am nervous. One bout, traveller. The drowned halls make a tremendous house, and the fish are an unforgiving audience.' },
    { op: 'battle', trainer: 'troupe_player_b' },
    { op: 'say', speaker: 'ORSINO', text: 'Bravo. Truly. I have died on stage a hundred times, and that was the most convincing of them.' },
    { op: 'setFlag', flag: 'flag:troupe_player_b_beaten' },
  ],

  // The Lumenary green room — the region's rest point (the standing kit;
  // the Solarium is a ruin, not a town: the matron's hearth IS the inn).
  'script.solarium_rest': [
    { op: 'say', speaker: 'MATRON', text: 'In off the water, pilgrim. The green room keeps a warm corner for every walker the festival washes up — that is what a tiring-house is FOR, whatever the players tell you.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'MATRON', text: 'There. Kin warm, boots dry, and the stage none the wiser. The warm day keeps a while yet.' },
  ],

  // Solarium caches (the standing variety; the shard is the flooded missable).
  'script.pickup_solarium_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A festival hamper, set above the waterline and forgotten. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_solarium_balm' },
  ],
  'script.pickup_solarium_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Wedged in a bone column\'s crack, warm side up: a MOTH-AMBER, glowing along with the garden. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_solarium_amber' },
  ],
  'script.pickup_solarium_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: "A festival takings-tin, lidded against the damp. Found 250 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_solarium_wicks' },
  ],
  'script.pickup_solarium_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A pilgrim\'s offering, wax seal unbroken, left where the daylight glows brightest. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_solarium_charge' },
  ],
  'script.pickup_solarium_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Deep in the flooded halls, where only the called tide walks: a STARGLASS SHARD, holding its constellation under the water like a kept promise. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_solarium_shard' },
  ],

  // --- Sunvault Climb — the golden road's two sight trainers + the kit -------
  'script.sunvault_terracer': [
    { op: 'say', speaker: 'BEL', text: 'Mind the beds! These terraces fed a garden by sunlight once — now they make do with mine. Every lamp that climbs through gets weighed against the gold. Custom of the road.' },
    { op: 'battle', trainer: 'sunvault_terracer' },
    { op: 'say', speaker: 'BEL', text: 'Weighed, and the garden approves — the overgrowth leaned toward you the whole bout. It has never once done that for me, and I PRUNE it.' },
    { op: 'setFlag', flag: 'flag:sunvault_terracer_beaten' },
  ],
  'script.sunvault_skywatcher': [
    { op: 'say', speaker: 'TAM', text: 'You are climbing into the brightest sky in Vesperholm, friend — seven constellations and the dome that watched them home. The watchers send nothing up the rim untested. Consider me the test.' },
    { op: 'battle', trainer: 'sunvault_skywatcher' },
    { op: 'say', speaker: 'TAM', text: 'Passed, and then some. Go on up. And when the dome takes your breath — that is not the climb. That is the sky.' },
    { op: 'setFlag', flag: 'flag:sunvault_skywatcher_beaten' },
  ],
  // X3 leg 1 — the star-reading from the high terrace (the N2 stillness pattern).
  'script.chart_sunvault': [
    { op: 'narrate', text: 'The junior watcher\'s first viewpoint. You stand at the terrace rim and read the sky the way she asked: seven constellations over the golden climb, the sun-vines below holding their light up to be counted.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'You stay until the figures hold still in your keeping. One reading of three — though she said the third was for the brave, and meant it.' },
  ],
  'script.pickup_striker': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'watch_striker', count: 1 },
    { op: 'say', text: 'In a pocket of the high terrace, on a worn cord: the old watcher\'s STRIKER, lost on the road down and never replaced. The Astral Walk\'s first lamp has waited years for this spark.' },
    { op: 'setFlag', flag: 'flag:picked_striker' },
  ],
  'script.pickup_sunvault_balm': [
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'A climber\'s reserve in the lower garden, gold-wrapped against the dew. Found a BRIGHT BALM!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_balm' },
  ],
  'script.pickup_sunvault_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: "A gardener's pay-tin under the terrace stair, sound and dry. Found 250 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_sunvault_wicks' },
  ],
  'script.pickup_sunvault_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'On a shelf only a bloomed vine reaches: a MOTH-AMBER, sunning itself in the stored light. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_amber' },
  ],
  'script.pickup_sunvault_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A sky-watcher\'s drop-box lashed to the bridge post. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_charge' },
  ],

  // --- Helia Vault — the Sunsketch puzzle reliquary (3 blooms + the mirror) --
  'script.helia_bloom_1': [
    { op: 'narrate', text: 'You raise your lamp and release a pocket of daylight over the antechamber\'s shut vines.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.2, ms: 600 },
    { op: 'narrate', text: 'The double vine unfurls underfoot, petal over petal, forty years of waiting undone in a breath. The way on climbs toward a ledge already gold with stored light.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 600 },
  ],
  'script.helia_bloom_2': [
    { op: 'narrate', text: 'From the sunnier ledge, the light you stand in is the light you bloom with — your pocket of daylight comes away richer, and the north vine answers it at once.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'It opens like a hand. Higher again. The vault is teaching you its own liturgy: climb to the light, then lend it on.' },
  ],
  'script.helia_bloom_3': [
    { op: 'narrate', text: 'The high gallery\'s west vine takes your daylight and BLOOMS — and from up here you finally see the trouble: the great far vine, across a chasm no pocket of light can jump.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'But on the east spur, something round and dish-shaped catches your lamp and gives it back. The keepers left a mirror in their garden.' },
  ],
  'script.helia_mirror': [
    { op: 'narrate', text: 'The sun-mirror flower is stiff with years, but it turns — petal-dish grinding round until it faces the far dark.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'narrate', text: 'The dish-bloom turns. Somewhere deeper, gold light lands where your hands cannot.' },
  ],
  'script.helia_bloom_far': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The bent daylight lies across the chasm like a drawn line. You raise your lamp and send your own pocket of light down it.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.3, ms: 900 },
    { op: 'narrate', text: 'The great vine WAKES — a bridge of opening flowers rolling away across the dark, and beyond it the reliquary lights from within: the most concentrated pocket of stored daylight in Vesperholm, unsealed.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
  ],
  'script.pickup_helia_relic': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'chart_sunburst_nova', count: 1 },
    { op: 'say', text: 'In the reliquary\'s heart, dry these forty years in a case of gold glass: a STAR-CHART: SUNBURST NOVA — the sun\'s own remembered blaze, pressed by the keepers before the night fell.' },
    { op: 'say', text: 'The vault\'s hush approves of your hands. Probably.' },
    { op: 'setFlag', flag: 'flag:picked_helia_relic' },
  ],
  'script.pickup_helia_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'A keeper\'s offering-box beneath the first vine, seals sound. Found 2 BEACON CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_helia_charge' },
  ],

  // ===========================================================================
  // THE COLDFOG DETOUR (B4's shown half) — the drained land. ZERO humour in
  // this whole block; the register is elegiac, merciful-and-wrong. The kin are
  // asleep, never harmed; nothing is broken; that is the horror of it.
  // ===========================================================================

  // X3 leg 3 — the bravest reading: the one sky that gives nothing back.
  'script.chart_coldfog': [
    { op: 'narrate', text: 'The survey cairn on the bluff, over the deep fog. You take the third reading the junior watcher called "for the brave" — and understand, now, why she would not ask it outright.' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'There is nothing to read. Above the drained marsh the sky is a held grey blank — no figures, no glimmer, not one of the seven you have given back. You chart the absence, carefully, because the absence is the finding.' },
    { op: 'narrate', text: 'The fog below does not move. You finish the reading and do not stay.' },
  ],
  // The B4 band — the Stillworks shown. Letterbox + silence; NO sting resolve;
  // end on the gauge at zero. Sets flag:seen_stillworks only (the trigger);
  // flag:great_null_known is Nessa's, at Nightreach.
  'script.hollowfen_stillworks': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'The passage opens, and the works show you what they are.' },
    { op: 'tint', color: '#202430', alpha: 0.42, ms: 900 },
    { op: 'narrate', text: 'Rows of null-lanterns on swept gantries — dozens of them, hung in clean lines, each one holding its little piece of dark. Not one is broken. Not one is dusty. Somebody still tends the collars.' },
    { op: 'narrate', text: 'At the far wall stands the engine of it: a bell of held dark on cradle-pipes, polished like a font. It is not running. It does not need to be. The fen outside is the proof of its work.' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'There is a gauge on the casing, brass-rimmed, lovingly kept. Its needle rests at zero, and has for years — because zero, here, is the finished number. Zero is what the light comes to.' },
    { op: 'tint', color: '#202430', alpha: 0, ms: 1100 },
    { op: 'narrate', text: 'No one stops you. No one hurries you. The works are quiet the way a sleeping ward is quiet — and someone, gently, has seen to it that they stay that way.' },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // Coldfog caches (the drained fen's finds; the murk is dead — these sit on
  // what banks and islets the old road left).
  'script.pickup_coldfog_embergloss': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'embergloss', count: 1 },
    { op: 'say', text: 'At a snuffed wayshrine, a knot of old hearth-resin the fog never managed to cool: EMBERGLOSS, faintly warm at the heart. Took it.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_embergloss' },
  ],
  'script.pickup_coldfog_murk_pearl': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'murk_pearl', count: 1 },
    { op: 'say', text: 'On the islet, in a shell that stopped closing years ago: a MURK PEARL — lightless, flawless, heavier than it should be. Took it.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_murk_pearl' },
  ],
  'script.pickup_coldfog_drowned_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: 'A courier\'s strongtin where the old road drowned, lid rusted shut and patiently worked free. 250 WICKS, dry inside. Whoever they were for is long past needing them.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_drowned_wicks' },
  ],
  'script.pickup_coldfog_camp_tonic': [
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'In the quieted camp, set out neat beside the cold fire-ring: a BRIGHT BALM, stoppered and sound. It was left ready for a morning that never came. You take it, and leave the camp as you found it.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_camp_tonic' },
  ],
  'script.pickup_coldfog_bank_charm': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'On the high bank, a waxed charm-bundle tied the old wardens\' way — and inside, kept dry against the fen, a BEACON CHARGE. A light, hidden from the place that eats them.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_bank_charm' },
  ],
  'script.pickup_coldfog_keepers_cache': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'The last keeper\'s cache, set out neat on the islet stone: a BRIGHT BALM and a BEACON CHARGE, arranged the way a table is laid for a guest. Took them — gently.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_keepers_cache' },
  ],
  'script.pickup_coldfog_works_store': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'The works\' store alcove, swept and ordered. Among the spare collars and labelled jars: a STARGLASS SHARD, shelved like an exhibit — a piece of the sky, filed under what the light used to be. You take it back outside, where it belongs.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_works_store' },
  ],

  // ===========================================================================
  // NIGHTREACH OBSERVATORY — the Vigil of the Seven (spine §5 shape #8, the
  // capstone ceremony walk) + the C4/A5/B4 cluster + Lumenary 8. Reverent,
  // vast; the cluster's ONE dry line lives with the inn guest.
  // ===========================================================================

  // Nessa's hook, from the eyepiece (interior; sets flag:q_west_vigil).
  'script.nessa_quest': [
    { op: 'narrate', text: 'The Lampwarden of Nightreach does not look up from the eyepiece. You get the sense she has not looked up from it in some years.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Seven, now. I watched the seventh come home from this chair — gold, over the drowned garden. You have been busy with my sky, Wayfarer.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Seven watch-fires for seven stars you\'ve already given back. Light their lamps along the walk — then come tell the eighth it\'s time.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'The Astral Walk, up the telescope terrace. Seven watch-lamps, dark since the night fell, one for each constellation in the order they came home — ember-light first, sun-light last. The sky is lit, Wayfarer. The lamps below should not still be ashamed to meet it.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'The first lamp wants the old watcher\'s striker — lost on the Sunvault road, if the road has kept it. The rest want only a steady hand and a good memory. ...Bring both.' },
    { op: 'setFlag', flag: 'flag:q_west_vigil' },
  ],

  // THE SEVEN LAMPS — each a remembrance of its region: the game remembering
  // itself, one constellation at a time. (Trigger chain banks the lamp flags.)
  // Lamp 1 — EMBER: Tinderwick's hearths, where the Wayfaring began.
  'script.west_lamp_1': [
    { op: 'narrate', text: 'The first watch-lamp, polished and cold. You set the old watcher\'s striker to the wick and strike — once, twice — and the spark takes, ember-orange, the colour of home.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Ember-light. Tinderwick: a beacon on a bluff, a wick-key three hundred years old, a town that danced under strung lanterns because a small flame is no lesser thing. Far to the south, over the people who taught you that, its constellation burns on.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'One of seven. Above you, the Ember seems to settle — the way a hearth settles when the house is finally home.' },
  ],
  // Lamp 2 — TIDE: Pearlmoor's bell, and the water that parts for the asking.
  'script.west_lamp_2': [
    { op: 'narrate', text: 'The second lamp takes your flame and stands it up cool and silver — and the light sways, faintly, the way lamplight sways on harbour water.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Tide-light. Pearlmoor: a bell that hung silent until you carried its rope home, buoys answering mast by mast, the whole quay singing the going-out song to the boats. Tides go out so they can come back. You have been coming back ever since.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'Two of seven. Somewhere very far south, you would swear, a bell answers.' },
  ],
  // Lamp 3 — VERDANT: Lowleaf's moss, the kept light that vouches.
  'script.west_lamp_3': [
    { op: 'narrate', text: 'The third lamp catches green-gold, and holds it soft — not a blaze but a glow, the kind that comes up out of old moss when the dark is kind.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fe8b8', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Verdant-light. Lowleaf: an Elder Bed grey at its own festival, warmed back rim to rim like a rumour through a crowd, and a child saying, very clearly, "it was SLEEPING." The moss keeps a little light where it can. Be like the moss.' },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'Three of seven. The lamp glows on, unhurried, asking nothing — exactly the way Sable would want it.' },
  ],
  // Lamp 4 — STONE: Cinderhead's vigil, the flame carried through the dark.
  'script.west_lamp_4': [
    { op: 'narrate', text: 'The fourth lamp is heavier ironwork than its sisters, miner-made. Your flame crosses into it and steadies at once, patient as the rock.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#caa46a', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Stone-light. Cinderhead: a vigil-lamp burning alone in the third gallery, carried up through the leaning dark without once going out — because anyone can LIGHT a lamp; carrying one is the trick of the whole thing. The lowered lamps rose for you that night.' },
    { op: 'tint', color: '#caa46a', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'Four of seven. Past the halfway. Behind you the walk is a line of kept flames — and you had not realised, until now, that you were checking each one.' },
  ],
  // Lamp 5 — FROST: the aurora — and C4, Fenn's counsel. He lights it WITH
  // you; portrait + quiet, no swell. He does not march; he sends you up clear.
  'script.fenn_counsel': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Child. I hoped I would catch you at this one. The frost-lamp was always my favourite of the seven — it burns the colour of patience.' },
    { op: 'narrate', text: 'You tip the oil together, his old hand steadying the well while yours brings the flame. The wick takes pale and cool — aurora-light, indoors.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Frost-light. Pale Vault: seven brackets walked in order, none hurried; a town standing out on black ice, each holding one chosen flame under the slow green roads of the sky. Calm as any quieted valley — except every light was lit on purpose.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'Eight stars, nearly. When the Crown closes, the dark will part and the Spire will open its roads. You won\'t beat him up there, apprentice. You\'ll just have to remember harder than he\'s forgotten.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'He will ask you his question again, at the top of the world, with everything he has built standing behind it. And every lamp on this walk — every lamp on your whole long road — is a word of your answer, already lit.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'I will not climb with you. An old man on the stair would only give you something else to carry — and besides, somebody should be watching from here when the sky finishes. I have waited forty years for that particular view.' },
    { op: 'narrate', text: 'He presses your shoulder once, the way he did at the waystone, a Wayfaring ago. Five of seven. He stays by the lamp as you walk on — and does not stop looking up.' },
  ],
  // Lamp 6 — STORM: the kites — and A5, Wren resolved (the warm mirror of A4).
  // The ribbon line fires only if N3 was kept (flag:q_north_ribbon_placed —
  // the per-step if_flag guard; purely optional colour). The friendly bout is
  // part of the reunion: A2's register, returned.
  'script.wren_nightreach': [
    { op: 'narrate', text: 'Somebody is sitting under the sixth watch-lamp with their back against the post, flying nothing, easy as a harbour evening.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Took you long enough. I counted four lamps come on down the walk and thought — that walk, I know that walk. Same one as the coast road.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'I went and looked at the quiet, like Còr wanted. Properly looked. Sat in one of his valleys a whole day with my lamp shut. It\'s peaceful, all right. Peaceful as a held breath. ...I\'d rather breathe.' },
    { op: 'say', if_flag: 'flag:q_north_ribbon_placed', speaker: 'WREN', portrait: 'wren', expr: 'soft', text: 'And — the ledge on the second stair. My ribbon, under a stone, where I\'d been sitting being sorry for myself. No note. No waiting around to be thanked. ...It smelled of festival smoke the whole way down the mountain. That was you, and you\'re not allowed to deny it.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'So. Before we light this one — friendly rules, like the coast. One bout, for the road\'s sake. I want to remember what all this is FOR, with the person I learnt it next to.' },
    { op: 'battle', trainer: 'wren_nightreach' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'soft', text: 'Ha. There it is. THAT\'s the thing the quiet doesn\'t have — and Còr can keep every silent valley in Vesperholm, he\'s not getting that one.' },
    { op: 'narrate', text: 'You light the sixth lamp together, Wren\'s hand over yours on the striker, laughing at nothing the way you did at the start.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Storm-light. Galehigh: a whole hill paying out string at once, a hundred small flames climbing the dark on kite-tails — so the stars have something to climb back up. Daft, maybe. The night is shorter for it.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 700 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'Six of seven. Come on — let\'s go light the last one.' },
    { op: 'setFlag', flag: 'flag:wren_nightreach_battled' },
  ],
  // Lamp 7 — SOLAR: the stage — and B4, THE GREAT NULL NAMED. The information
  // set-piece: letterbox, Nessa's haunted portrait-register, a silence + one
  // cold tint on "aimed at the Keystar"; let it sit. (The trigger banks
  // flag:q_west_lamp_7 + flag:q_west_vigil_kept + flag:great_null_known.)
  'script.great_null_named': [
    { op: 'narrate', text: 'Nessa Cole is waiting at the seventh lamp, beside the great telescope she has carried out onto the terrace. She watches you light it — sun-gold, the warmest of the seven, the colour of a drowned garden remembering.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.24, ms: 700 },
    { op: 'narrate', text: 'Solar-light. The Solarium: three braziers fed spark by spark out of the flood, a troupe walking onto a lit stage after forty years, a festival spending its last warm day where the dark could watch. Seven of seven. The Astral Walk stands lit, end to end, under seven answering stars.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 700 },
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'say', speaker: 'NESSA COLE', text: 'Seven kept flames. Thank you, Wayfarer. I needed to see the walk lit before I showed you this — so you would know, exactly, the size of what I am about to say.' },
    { op: 'narrate', text: 'She steps to the great telescope and swings it — not up, but ACROSS, levelling it at the darkened mountain at the centre of the world.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Look. The Umbral Spire\'s crown. The scaffolding on the north face — there, where no light catches. He has been building it for two years. My charts watched it grow the way you watch a storm come in over water: slowly, then all at once.' },
    { op: 'say', if_flag: 'flag:seen_stillworks', speaker: 'NESSA COLE', text: 'You have walked the Hollowfen, I think — you carry the look of it. The rows of sleeping lanterns. The font with its gauge at zero. Then you have already seen this thing\'s little sister, Wayfarer. The works were the rehearsal.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'He calls it the Great Null. A lantern that holds no light — aimed at the Keystar, the one we all rekindle from. Snuff that, and the sky stops being able to remember itself.' },
    { op: 'silence', ms: 1600 },
    { op: 'tint', color: '#2a3550', alpha: 0.4, ms: 900 },
    { op: 'narrate', text: 'Every constellation you have relit, relit because the Keystar held. Every lamp on the walk behind you, lit from a sky that can still remember. One star anchors all of it — and the gentlest man in Vesperholm has built a dark to fit it exactly.' },
    { op: 'tint', color: '#2a3550', alpha: 0, ms: 1100 },
    { op: 'say', speaker: 'NESSA COLE', text: '...I knew him, once. He was the gentlest of us. That\'s the part that keeps me awake.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'The Crown wants one more star, and the roads to the Spire open with it. Come down to the hall when you are ready, Wayfarer. The vigil is kept; the eighth is yours to ask for — and after tonight, I think the asking had better not wait.' },
    { op: 'narrate', text: 'She looks back along the lit walk — seven flames, seven stars — and for a moment the haunted look eases into something older and steadier. The vigil of the seven is kept. The eighth watch waits below.' },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // The Astral Walk's two junior-watcher SIGHT keepers (keeper class).
  'script.junior_watcher_a': [
    { op: 'say', speaker: 'LIRA', text: 'Hold the walk, please! Seven lamps, seven stars, and a junior watcher to keep the order of it. Nobody crosses my stretch unweighed — even the senior watchers. ESPECIALLY the senior watchers.' },
    { op: 'battle', trainer: 'junior_watcher_a' },
    { op: 'say', speaker: 'LIRA', text: 'Weighed and recorded. ...In my own ledger, which nobody reads. Keep the order, Wayfarer — ember-light first, sun-light last.' },
    { op: 'setFlag', flag: 'flag:junior_watcher_a_beaten' },
  ],
  'script.junior_watcher_b': [
    { op: 'say', speaker: 'OS', text: 'A lamp on the high terrace! Good — the vigil likes a tested flame. I keep the last stretch before the seventh lamp. Show me yours keeps too.' },
    { op: 'battle', trainer: 'junior_watcher_b' },
    { op: 'say', speaker: 'OS', text: 'It keeps. Walk on, and walk soft — Nessa has been at the eyepiece three nights straight, waiting on whatever it is you\'re carrying.' },
    { op: 'setFlag', flag: 'flag:junior_watcher_b_beaten' },
  ],

  // X3 "Charting the Dark" — Lira's quest (her beaten swap is the giver).
  'script.chart_quest': [
    { op: 'say', speaker: 'LIRA', text: 'Wayfarer — a proper asking, now the weighing\'s done. I\'m charting the sky as it COMES BACK. Nobody has ever had the chance before; nobody may again. Seven constellations relit in one lifetime — in one YEAR — and the senior watchers are all too busy watching the eighth to write any of it down.' },
    { op: 'say', speaker: 'LIRA', text: 'I need readings from three high points my watch rota will never let me reach: the Sunvault terrace on the climb you came up, our own roof terrace past the scree, and — for the brave, and ONLY the brave — the survey cairn over the Coldfog Marches, where the sky gives nothing back at all.' },
    { op: 'say', speaker: 'LIRA', text: 'Stand in them. Look properly — long enough to be cold. The first two will finish the chart; the third would make it TRUE. Bring me what the sky does, and I\'ll press the rest.' },
    { op: 'setFlag', flag: 'flag:q_west_chart' },
  ],
  // X3 leg 2 — the roof-terrace reading (the observatory's own sky).
  'script.chart_observatory': [
    { op: 'narrate', text: 'The roof terrace, past the scree. The dome below you, the Astral Walk a thread of lamps, and overhead — the densest starfield in Vesperholm, seven constellations deep, near-dawn pallor along the north horizon.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'You take the reading slowly, because hurrying it would be a kind of lie. Two readings kept. The junior watcher will want to hear about this one twice.' },
  ],
  // X3 done — requires _1 + _2 only (Coldfog's _3 stays the optional, bravest
  // leg, never demanded). The finished chart NAMES STARWELL — the tease-closer.
  'script.chart_done': [
    { op: 'say', speaker: 'LIRA', text: 'The terrace AND the roof — sit down, talk, slowly, I\'m pressing as you speak—' },
    { op: 'narrate', text: 'She works the way the kite-maker worked: fast, certain, glancing up at you instead of the sky. Figure by figure the chart fills — seven constellations as they came home, and the pale beginnings of an eighth.' },
    { op: 'say', speaker: 'LIRA', text: 'There. The sky, coming BACK — the first chart of its kind since the night fell. And look — here, where the old charts go quiet, at the mountain\'s foot...' },
    { op: 'narrate', text: 'Her finger rests on a small, careful figure inked at the Penumbra\'s edge: a well of gathered starlight the old watchers only ever drew from hearsay. Under it, in her neat hand: STARWELL.' },
    { op: 'say', speaker: 'LIRA', text: 'The old charts say it\'s real — a shrine of fallen starlight, inside the dark ring, found only when the Crown is whole. If you\'re truly going in there, Wayfarer... go and stand in THAT view for me too, one day.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveMoney', amount: 400 },
    { op: 'say', text: 'She presses her chart-fund on you, over every objection: 400 WICKS. "Readings are PAID. That\'s what makes it a survey."' },
    { op: 'setFlag', flag: 'flag:q_west_chart_done' },
  ],
  // R5 "A Chart for the Waykeeper" — the Round's last leg, the take side.
  'script.round_chart_take': [
    { op: 'say', speaker: 'LIRA', text: 'One more thing — and this one\'s an honour, not an errand. The Waykeeper at the Crossroads has hung a fresh chart on the Waystone every year since before the night fell. He hasn\'t had a TRUE one to hang in forty.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'round_chart', count: 1 },
    { op: 'say', text: 'She rolls a fresh pressing of the relit sky, seals it, and lays it across your hands like a lamp at a naming. Received the FRESH STAR-CHART!' },
    { op: 'say', speaker: 'LIRA', text: 'Down the Lanternway with it, Wayfarer. Tell him it\'s from the Nightreach watch — and that the sky\'s worth charting again. He\'ll know what we mean by it.' },
    { op: 'setFlag', flag: 'flag:q_round_chart_taken' },
  ],
  // R5, the delivery (the Crossroads Waykeeper) — the Round comes full circle.
  'script.round_chart_deliver': [
    { op: 'say', speaker: 'WAYKEEPER', text: 'That seal... that\'s a Nightreach pressing. Hand it here, hand it here — careful — forty YEARS I\'ve hung guesswork on this stone and called it custom—' },
    { op: 'narrate', text: 'He unrolls it against the Waystone, and goes still. Seven constellations, true as the night above him — and an eighth sketched faint, waiting. When he hangs it, he does it the way a Gleam is given: slowly, so the moment knows it is one.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'narrate', text: 'The fresh chart hangs on the Waystone, lamp-lit at the centre of every road in Vesperholm. Travellers are already drifting over to look up and point.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'The Round\'s last leg, walked by the same pair of boots that lit half the sky on it. Round rates, Wayfarer — plus the years.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 400 },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'Received 400 WICKS and a BRIGHT BALM!' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Kite, moss, letters, lamps, and now the sky itself — the Waykeeper\'s Round is KEPT this year. Every road home is lit, child. You saw to that personally.' },
    { op: 'setFlag', flag: 'flag:q_round_chart' },
  ],

  // E — the Star-vigil (the warden of the watch, on the temple steps): the
  // grandest, most reverent festival — kept in silence, BEFORE the eighth
  // lights; it crests with the Lunar Gleam in the hall. No humour.
  'script.nightreach_star_vigil': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'The whole town is on the temple steps, spaced wide, faces up, each with one unlit lamp in their hands. Nobody speaks. This is the Star-vigil: the night-long watch kept as the Crown nears its closing.' },
    { op: 'narrate', text: 'Seven of the watchers stand apart, lamps LIT — one for each constellation that has come home. Theirs lit the moment "their" star did; some have held them burning for half a year.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fd4ff', alpha: 0.18, ms: 900 },
    { op: 'narrate', text: 'A watcher meets your eye and inclines her head — toward the eighth row, where the unlit lamps wait. An empty place stands at the row\'s end. Nobody says it is yours. Everybody knows it is.' },
    { op: 'tint', color: '#9fd4ff', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'You stand the watch a while, under seven answered stars and one long-waiting dark. The vigil asks nothing else: only that somebody is watching when the sky remembers.' },
    { op: 'letterbox', on: false, ms: 420 },
    { op: 'setFlag', flag: 'flag:star_vigil_seen' },
  ],

  // Lumenary 8 — Nessa Cole, under the great eyepiece. Win → gleam:lunar +
  // Starreach; the ENGINE derives crown_west + hub_unlocked (last quadrant).
  // THE GRANDEST Gleam cadence of the eight: silence cresting exactly as the
  // eighth constellation lights, each watcher's lamp a small flashColor.
  'script.lumenary_nightreach': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'say', speaker: 'NESSA COLE', text: 'The walk is lit, the vigil is kept, and the eighth star has waited longest of all. One asking remains, Wayfarer — mine.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'My kin keep the dream-hours: the soft dark, the kind that closes your eyes for you. Còr would tell you that is mercy. Stay awake through it... and we will go and wake the sky together.' },
    { op: 'battle', trainer: 'nessa_cole' },
    { op: 'musicFade', ms: 600 },
    { op: 'silence', ms: 1800 },
    { op: 'narrate', text: 'Nessa says nothing. She crosses to the eighth watch-lamp beside the great eyepiece — the one no striker has touched — and waits, her hand NOT on it, her face turned up to the dome.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fd4ff', alpha: 0.3, ms: 1100 },
    { op: 'narrate', text: 'And the eighth watch-lamp lights ITSELF — kindled from above, as the eighth constellation answers your bond and takes its place in the sky.' },
    { op: 'gleam', element: 'lunar' },
    { op: 'narrate', text: 'Outside, down the temple steps, the Star-vigil crests in perfect silence: lamp after lamp after lamp catching light in watching hands, the whole town kindling person by person under a finished sky.' },
    { op: 'flashColor', color: '#cfe8ff', ms: 260 },
    { op: 'flashColor', color: '#cfe8ff', ms: 260 },
    { op: 'flashColor', color: '#ffd089', ms: 300 },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 1200 },
    { op: 'tint', color: '#9fd4ff', alpha: 0, ms: 1200 },
    { op: 'narrate', text: 'Eight stars. The Skyweave Crown closes overhead, quiet as snowfall — and far away at the centre of the world, the Penumbra PARTS: the four cardinal roads opening inward at the Crossroads, toward the mountain, toward him.' },
    { op: 'narrate', if_flag: 'flag:wren_nightreach_battled', text: 'At the hall door, Wren is leaning on the frame with their lamp held up among all the others, grinning like the coast road. They do not come in. They do not need to. Same road, different lamps — all the way to the end of the sky.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'The Lunar Gleam, Wayfarer — and the whole Crown standing with it. I have watched this sky my entire life, and tonight is the first time it has ever watched back.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Take the Starreach. Starlight, drawn down to stand on — a stride across the short voids of pure dark. The Penumbra\'s last crossings will hold under you now... all the way up the Spire\'s roads.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Stand the vigil\'s end with us before you go down to the Crossroads. Eight lamps, eight stars, one night with nothing missing. Even the dark deserves to see what it is being asked to give back.' },
  ],

  // Rest + caches (the standing kit; "The Long Watch" inn).
  'script.nightreach_inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'In quietly, Wayfarer — half my guests sleep by day and watch by night, and the floorboards know which half. The hearth\'s low and the bunks are warm.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Rested, and your kin with you. The watch keeps the sky; you needn\'t — not tonight.' },
  ],
  'script.pickup_nightreach_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'On the roof terrace, where the sky is closest: a STARGLASS SHARD, bright to its heart under the densest stars in Vesperholm. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_nightreach_shard' },
  ],
  'script.pickup_nightreach_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: "A watcher's pay-purse, set down at shift-change and never missed. Found 300 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_nightreach_wicks' },
  ],
  'script.pickup_nightreach_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A vigil drop-box by the temple steps, seal sound. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_nightreach_charge' },
  ],
  'script.pickup_nightreach_balm': [
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'Tucked in the fog-gate\'s lee, against the worst of the east road: a BRIGHT BALM. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_nightreach_balm' },
  ],

  // ===========================================================================
  // CENTRAL / ENDGAME (walkthrough/05-central-endgame) — the Crossroads' last
  // quiet hour, the Penumbra crossed on starlight, and the ascent of the Ninth
  // Lantern. ZERO humour past the hub (the one sanctioned warm send-off lives
  // in the inn's done-stage; Wren's one wry-warm beat lives in npc.wren_spire_f1).
  // ===========================================================================

  // --- C4 — Fenn's counsel before the Spire (the crossroads waystone). Short by
  // design: the lamp-5 counsel at Pale Vault did the heavy lifting; this sends
  // the player up CLEAR-EYED. His "best Lamp for the Keylumen" travels with
  // Wren (script.wren_joins — the un-missable band), so the gift cannot be lost.
  'script.fenn_crossroads_counsel': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Child. Of course I am here — I watched the eighth star come home from this very stone, and my feet refused every other road.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'You know it all already. You cannot out-fight Còr; he is not your enemy, and beating him proves nothing he has not already grieved his way past. Go up there to remember louder than he can grieve. That is the whole of my counsel, and you have carried it for half the sky.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'One thing more. The Keystar keeps a living heart — the old books call it the Keylumen — and it will want asking, not winning. I have sent something up the inward road with a friend of yours, for exactly that asking. Spend it nowhere else.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'I will be here, watching the centre of the sky. When it changes — and it is going to change, child — I should like to be standing where your road began.' },
    // The Three Hours' foreshadow payoff (07-the-three §6) — optional colour,
    // played only if the player has already stood before the Lost Hour.
    { op: 'say', if_flag: 'flag:three_dawn_met', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'So you found the third watch. Still facing east, was it? ...Then it has never stopped believing the wheel can turn. Neither have I. Go and prove the pair of us right.' },
    { op: 'narrate', text: 'He presses your shoulder once, the way he did at the very start, a whole Wayfaring ago. He does not say goodbye. Lamp-tenders never do.' },
    { op: 'setFlag', flag: 'flag:fenn_counsel_given' },
  ],

  // --- A5→A6 — Wren joins for the climb (the inward road's full-cut band; also
  // the Wren NPC standing at the roadside). Carries Fenn's Starlamp up with
  // them, so the Keylumen's asking-gift is banked on the only road in.
  'script.wren_joins': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'There you are. I watched the fog go down like a curtain and thought — right, that road, that walk, any minute now.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'I went all the way round it, you know. The Hollowing. They\'re right that it hurts. ...I just don\'t think "never again" is worth "never at all."' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'So. Come on — I\'m not letting you climb that thing alone. Same road, different lamps. All the way up, this time.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Oh — and the old man sent this up for you. Wouldn\'t say what it was. Held it like it was somebody\'s heart, so I didn\'t ask twice.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starlamp', count: 1 },
    { op: 'say', text: 'Received the STARLAMP! A cell of caught starlight — Fenn has kept it forty years for one particular asking, at the top of the sky.' },
    { op: 'setFlag', flag: 'flag:wren_joined' },
  ],

  // --- C1 "Lampling's Trail" — the Waystone kid's lamp-flickers (three
  // guttering dusk-lamps around the plaza, then the trail's end at the fourth).
  'script.lampling_trail_start': [
    { op: 'say', speaker: 'WAYSTONE KID', text: 'Psst! Wayfarer! The plaza lamps keep GUTTERING — one at a time, round and round, like something\'s going lamp to lamp tasting them.' },
    { op: 'say', speaker: 'WAYSTONE KID', text: 'The Waykeeper says his wicks are sound, and his wicks are ALWAYS sound. So it\'s something little, and quick, and it likes lamplight better than anything in the world. Follow the flickers! Start at the north-west lamp — that\'s where I saw it first!' },
    { op: 'setFlag', flag: 'flag:q_central_trail' },
  ],
  'script.trail_lamp_1': [
    { op: 'narrate', text: 'As you reach the lamp, its flame dips and dances — and a curl of warm light no bigger than a teacup whisks out of the lantern-glass and away across the plaza, leaving the wick burning none the worse.' },
    { op: 'narrate', text: 'It was not a draught. Draughts do not look back at you. The next flicker is already starting, away at the north-east lamp.' },
  ],
  'script.trail_lamp_2': [
    { op: 'narrate', text: 'The flame here is still wobbling, delighted with itself. From inside the lantern-glass comes the faintest sound — like a kettle humming to itself about something it remembers fondly.' },
    { op: 'narrate', text: 'The little light spills out, circles the lamp-post once — twice — and streaks off low across the plaza, toward the south-west lamp.' },
  ],
  'script.trail_lamp_3': [
    { op: 'narrate', text: 'You arrive in time to see it plainly at last: a tiny lantern-shaped kin sitting INSIDE the lamp, warming its hands at the wick like a traveller at an inn fire.' },
    { op: 'narrate', text: 'It startles, blushes a deep gold, and pours itself away toward the last lamp of the ring — where it waits. Visibly. Politely. The way you wait when you have decided to be found.' },
  ],
  'script.lampling_catch': [
    { op: 'narrate', text: 'The little kin is sitting on top of the dusk-lamp with its glow turned up bright, exactly where you can see it. The trail was never a chase. It was an introduction.' },
    { op: 'legendaryBattle', name: 'lampling', kin: 148, level: 30, caughtFlag: 'flag:lampling_caught', cooldownBattles: 3, cooldownRef: 'npc.lampling_shy' },
    { op: 'narrate', text: 'The Lampling settles into your lamp like a wick into wax — home at once, and warm. Around the plaza, all four dusk-lamps burn a shade brighter than their oil should allow.' },
    { op: 'setFlag', flag: 'flag:q_central_trail_done' },
  ],

  // --- C2 "The Inn's Empty Lamps" — the waystation innkeeper's four festival
  // lamps (one lamp-token per quadrant's festival, hung in fixed order
  // south→east→north→west via the boolean chain). Every stage rest-heals and
  // opens the counter: the hub is the last shop and bed before the mountain.
  'script.inn_empty_lamps': [
    { op: 'say', speaker: 'INNKEEP', text: 'In you come, Wayfarer — the kettle\'s on and the bunks are warm. This inn has fed every road in Vesperholm at one time or another; the least it can do is feed you.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Rested, the lot of you. ...And since you\'re the sort who finishes things — look up a moment. Four lamp-brackets over my hearth, and all four empty since the night fell.' },
    { op: 'say', speaker: 'INNKEEP', text: 'One for each quadrant\'s festival, they were. The festivals are BACK now — thanks to somebody — and each one presses little wax lamp-tokens for its own. Bring me one from each: south first, the old order. Tide-blessing, Lamp-down, Aurora-watch, Star-vigil. Fill my brackets and I\'ll fill your hand, fair\'s fair.' },
    { op: 'setFlag', flag: 'flag:q_central_tokens' },
    { op: 'say', speaker: 'INNKEEP', text: 'Meanwhile the counter\'s open. No shop past this door, mind — the mountain doesn\'t keep a till.' },
    { op: 'shop', shop: 'crossroads_inn' },
  ],
  'script.inn_rest_waiting': [
    { op: 'say', speaker: 'INNKEEP', text: 'Back again! Bunks are yours, same as ever.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Rested, and your kin with you. ...The brackets are still counting, when you\'ve a festival road to walk: south, east, north, west — the old order. The festivals know their own; just ask at the lamp-lit end of each.' },
    { op: 'shop', shop: 'crossroads_inn' },
  ],
  'script.inn_lamps_hang': [
    { op: 'say', speaker: 'INNKEEP', text: 'All FOUR. Hand them here — no, stay, you should see this done properly.' },
    { op: 'narrate', text: 'She melts each token gently into a bracket-lamp\'s wax — bell, vigil-mark, held flame, watcher\'s star — and lights them in the order the Gleams came home. South. East. North. West.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.22, ms: 900 },
    { op: 'narrate', text: 'Four festivals burn over one hearth, at the place where every road meets. Travellers at the long table go quiet — the good kind of quiet, the kind people save for things they thought they would not see again.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'INNKEEP', text: 'And fair\'s fair, as promised. I pressed the spare token-wax round one of my own trimmed wicks all season. There\'s a whole year\'s belonging in that cell — throw it at a heart worth keeping.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'radiant_lamp', count: 1 },
    { op: 'say', text: 'Received the RADIANT LAMP!' },
    { op: 'setFlag', flag: 'flag:q_central_tokens_done' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'Bunks and counter are yours whenever, Wayfarer. This hearth doesn\'t forget its lamp-fillers.' },
    { op: 'shop', shop: 'crossroads_inn' },
  ],
  // The done stage — the inn at full warmth. Carries the region's ONE sanctioned
  // warm send-off line (humour-sheet: innkeeper's patter; a smile, not a laugh).
  'script.inn_rest_crossroads': [
    { op: 'say', speaker: 'INNKEEP', text: 'In you come — four festivals over the hearth and the kettle never off. Bunks first, talk after.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Rested, and your kin with you. Off up the mountain, is it? Then mind you come back down — I\'ve started keeping your usual bunk free, and an empty bed is TERRIBLE for business.' },
    { op: 'shop', shop: 'crossroads_inn' },
  ],

  // --- C3 "The Long Round" — the Waykeeper, once the Round's last leg is kept
  // (flag:q_round_chart ⇒ all five legs, the boolean chain). One last walk of
  // the plaza lamps; the keepsake; the Lamplight tease.
  'script.long_round': [
    { op: 'say', speaker: 'WAYKEEPER', text: 'Kite, moss, letters, lamps, and the sky itself — the whole Round, walked in one pair of boots. Indulge an old keeper, then: one last walk of my plaza lamps, before you take the inward road. It is how a Round was always closed, in the lit years.' },
    { op: 'narrate', text: 'You walk the ring of dusk-lamps with him, sunwise, the way the Round runs. At each lamp he stops, trims nothing — they are all burning perfectly — and touches the post once, like a man counting his children home.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Forty years I kept this Round alone, on roads that mostly slept. Now every spoke is lit and the fresh chart hangs on the stone — and the Round is KEPT, properly kept, for the first time since the night fell.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'way_lamp', count: 1 },
    { op: 'say', text: 'Received the WAY-LAMP — the Waykeeper\'s own hand-lamp, retired this very hour.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Keep it by you when the dark leans close. A lamp that has walked every road burns a little farther — and yours, Wayfarer, has walked them ALL. You\'ll find the night shows you more than it used to. It can hardly help itself now.' },
    { op: 'setFlag', flag: 'flag:q_central_round_done' },
  ],

  // --- C2's four token givers — riding the festival NPCs' post-gleam stages in
  // their towns. Each replays the festival line, then hands the token only once
  // the chain has reached it (the per-step if_flag carries the south→east→
  // north→west order; until then the stage is plain festival colour and stays).
  'script.token_south': [
    { op: 'dialogue', ref: 'npc.blessing_singer' },
    { op: 'say', if_flag: 'flag:q_central_tokens', speaker: 'BLESSING SINGER', text: 'The crossroads inn is filling its festival brackets again? Oh, the quay would LOVE that — the going-out song was always sung for travellers as much as boats.' },
    { op: 'sfx', if_flag: 'flag:q_central_tokens', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:q_central_tokens', item: 'lamp_token_south' },
    { op: 'say', if_flag: 'flag:q_central_tokens', text: 'She presses a wax token into your palm — a bell over water, still warm from the stamp. Received the LAMP-TOKEN (SOUTH)!' },
    { op: 'setFlag', if_flag: 'flag:q_central_tokens', flag: 'flag:q_token_south' },
  ],
  'script.token_east': [
    { op: 'dialogue', ref: 'npc.vigil_raised_a' },
    { op: 'say', if_flag: 'flag:q_token_south', speaker: 'VIGIL MINER', text: 'A bracket at the crossroads, for the Lamp-down? Then take the vigil with you, friend — dimmed and relit, same as we keep it down here. The inn road was cut from this mountain\'s stone, you know.' },
    { op: 'sfx', if_flag: 'flag:q_token_south', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:q_token_south', item: 'lamp_token_east' },
    { op: 'say', if_flag: 'flag:q_token_south', text: 'He stamps a token against his own lamp\'s warmth — a flame dimmed, then relit. Received the LAMP-TOKEN (EAST)!' },
    { op: 'setFlag', if_flag: 'flag:q_token_south', flag: 'flag:q_token_east' },
  ],
  'script.token_north': [
    { op: 'dialogue', ref: 'npc.pale_vault_gleam_watcher' },
    { op: 'say', if_flag: 'flag:q_token_east', speaker: 'AURORA WATCHER', text: 'The waystation hearth, hanging the four festivals together? ...The watch would be honoured. We have always known the lamps are one lamp, really. It is good that an inn knows it too.' },
    { op: 'sfx', if_flag: 'flag:q_token_east', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:q_token_east', item: 'lamp_token_north' },
    { op: 'say', if_flag: 'flag:q_token_east', text: 'She presses the token in silence, the watch\'s way — one held flame under a moving sky. Received the LAMP-TOKEN (NORTH)!' },
    { op: 'setFlag', if_flag: 'flag:q_token_east', flag: 'flag:q_token_north' },
  ],
  'script.token_west': [
    { op: 'dialogue', ref: 'npc.nightreach_festival_a' },
    { op: 'say', if_flag: 'flag:q_token_north', speaker: 'STAR-VIGIL WATCHER', text: 'The last bracket? Then the Star-vigil closes the ring, as it closed the Crown. Carry it carefully, Wayfarer — this one was pressed the night the eighth star came home.' },
    { op: 'sfx', if_flag: 'flag:q_token_north', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:q_token_north', item: 'lamp_token_west' },
    { op: 'say', if_flag: 'flag:q_token_north', text: 'A watcher\'s lamp, lit at last, stamped small in wax. Received the LAMP-TOKEN (WEST)! The inn\'s four brackets wait.' },
    { op: 'setFlag', if_flag: 'flag:q_token_north', flag: 'flag:q_token_west' },
  ],

  // --- THE PENUMBRA RING — the threshold register: the held breath, not a beat.
  // No progression flag (the trigger banks the presentational once-only).
  'script.penumbra_threshold': [
    { op: 'musicFade', ms: 900 },
    { op: 'silence', ms: 2000 },
    { op: 'narrate', text: 'The dark here has edges. It has drawn back from the roads you lit — and what is left of it does not want you.' },
    { op: 'narrate', text: 'Your lamp-glow is the only colour in the world. Ahead, off the north rim, something vast holds the sky out of the sky: the Umbral Spire, wearing the last of the night.' },
    { op: 'say', if_flag: 'flag:wren_joined', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: '...Keep your lamp up. Almost there. A year ago this was a wall nobody could pass.' },
    { op: 'musicCrossfade', key: 'penumbra-ring-a', ms: 1600 },
  ],
  'script.pickup_penumbra_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'On the islet in the void-field, where only starlight can carry you: a STARGLASS SHARD — starlight made stone, bright to its heart. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_penumbra_shard' },
  ],
  'script.pickup_penumbra_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 600 },
    { op: 'say', text: "A courier's satchel, dropped at the old fog-line and sealed in by the dark for years. Found 600 WICKS — carried home at last." },
    { op: 'setFlag', flag: 'flag:picked_penumbra_wicks' },
  ],

  // --- STARWELL — the well of fallen starlight, and Lunaveil (the SILENCE
  // register: the quietest set-piece in the game; a chance, not a gift).
  'script.starwell_lunaveil': [
    { op: 'musicFade', ms: 900 },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'The pool stirs. Not with wind — there is no wind here — but the way a sleeper stirs when a lamp is carried into the room.' },
    { op: 'narrate', text: 'A vast wing crosses the starlight, soundless, trailing veils of pale dusk — and the Lunaveil settles on the basin rim, regarding your small warm light with eyes like the moment before moonrise.' },
    { op: 'legendaryBattle', name: 'lunaveil', kin: 132, level: 54, caughtFlag: 'flag:lunaveil_caught', cooldownBattles: 12, cooldownRef: 'npc.starwell_still' },
    { op: 'narrate', text: 'The Lunaveil folds itself into your lamp like dusk folding into a valley — vast, then gone, then quietly THERE, the way the moon is there behind a thin cloud.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'The well\'s light eases, as if it has been holding something carefully for years and may finally set it down. The water keeps shining anyway. Some places simply do.' },
  ],
  'script.pickup_starwell_amber': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'At the frozen pool\'s edge, set down like an offering: a MOTH-AMBER, its caught shimmer answering the well\'s. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_starwell_amber' },
  ],

  // --- THE UMBRAL SPIRE — the ascent of the Ninth Lantern. The acolytes are
  // small griefs: each a PERSON doing a careful, terrible kindness. Gentle asks,
  // sad-not-bitter defeats, no mook energy, zero humour.
  'script.hollowing_acolyte_a': [
    { op: 'say', speaker: 'MERRIN', text: 'You shouldn\'t be up here, apprentice. ...I dipped wicks in a coast-town chandlery for thirty years. I know good lamp-work when it walks in carrying it.' },
    { op: 'say', speaker: 'MERRIN', text: 'That is WHY I am here. Every wick I ever dipped burned down while somebody watched. We\'re not cruel — your kin will only sleep. No more guttering, no more loss. ...Won\'t you let us be kind to it?' },
    { op: 'battle', trainer: 'hollowing_acolyte_a' },
    { op: 'say', speaker: 'MERRIN', text: '...Still burning. All of yours, still burning. Go on, then — the gate was never locked. We always rather hoped no one would notice that.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_a_beaten' },
  ],
  'script.hollowing_acolyte_b': [
    { op: 'say', speaker: 'TACE', text: 'Mind the alcoves, please — they\'re sleeping. ...I kept a ferry once, south of here. Twenty years of carrying people home to lamps that had gone out by the time we docked.' },
    { op: 'say', speaker: 'TACE', text: 'The Warden was the first person who didn\'t tell me it gets easier. He said it could STOP. Put your kin down gently, traveller, and it stops tonight — for you, for them, for everyone.' },
    { op: 'battle', trainer: 'hollowing_acolyte_b' },
    { op: 'say', speaker: 'TACE', text: '...No. Of course not. You\'re the sort who docks at the dark jetty and lights it anyway. ...The ferry could have used you, all those years.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_b_beaten' },
  ],
  'script.hollowing_acolyte_c': [
    { op: 'say', speaker: 'IVORWEN', text: 'Hush, dear — softly through here. I tuck them in myself, every one. Warm where I can manage it. ...I nursed my husband\'s lamp four winters at the end. I know exactly how heavy watching is.' },
    { op: 'say', speaker: 'IVORWEN', text: 'Nobody up here is angry at the light, child. We just couldn\'t hold it any more. Let me take yours a while — you\'ve carried it so terribly far.' },
    { op: 'battle', trainer: 'hollowing_acolyte_c' },
    { op: 'say', speaker: 'IVORWEN', text: '...Four winters, and I would have kept a fifth if I could. There. That\'s the thing I wasn\'t letting myself remember. ...Go up, dear. Mind the draught on the gallery stair.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_c_beaten' },
  ],
  'script.hollowing_acolyte_d': [
    { op: 'say', speaker: 'HARL', text: 'Far enough, Wayfarer. ...I was a Cinderhead man, deep-galleries. Carried my crew\'s lamps home the bad year — all eight of them, and none of the hands that hung them by their doors.' },
    { op: 'say', speaker: 'HARL', text: 'The mountain taught me to outlast. The Warden taught me what for. This gallery is the last kindness before the summit — and I keep it like I kept the deep: nothing passes that the dark could hurt.' },
    { op: 'battle', trainer: 'hollowing_acolyte_d' },
    { op: 'say', speaker: 'HARL', text: '...You out-lasted me. The deep way. ...Eight lamps, Wayfarer. If you can keep yours lit where I couldn\'t — keep theirs lit too. Somebody should.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_d_beaten' },
  ],
  'script.hollowing_acolyte_e': [
    { op: 'say', speaker: 'SEFA', text: 'You can hear the wind from here. The Warden says it is the sky breathing on the glass. ...My wife lit the north roads, lamp by lamp, every dusk for eleven years. One dusk the fog put them out faster than she could walk.' },
    { op: 'say', speaker: 'SEFA', text: 'I am not here because I stopped loving lamplight, apprentice. I am here because I couldn\'t watch it lose again. Please — be tired. Be sensible. Be SPARED.' },
    { op: 'battle', trainer: 'hollowing_acolyte_e' },
    { op: 'say', speaker: 'SEFA', text: '...She would have liked you. She was exactly this stubborn about exactly this. ...Go on up. And if the sky takes the trouble to change — light the north roads first. For me.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_e_beaten' },
  ],

  // The Spire gatehouse camp — the climb's heal anchor (the C5 panel's MAJOR:
  // a blackout on the mountain respawned at Tinderwick with no rest closer than
  // the crossroads inn). Wren holds the gatehouse fire while you climb — the
  // standing inn-rest kit, staged as the A5 side-by-side promise kept. The f3
  // shaft compressor makes the descent-to-rest two rooms, not four floors.
  'script.spire_wren_camp': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'So this is where the dusk lives. ...It\'s tidier than I expected. Stay close — I didn\'t climb all this way to lose you in the dark.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'I\'ve got the gatehouse brazier going — wick-tender\'s privilege, don\'t tell the management. Sit down a minute. Lamps and kin first; heroics keep.' },
    { op: 'fade', dir: 'out' },
    { op: 'wait', ms: 700 },
    { op: 'heal' },
    { op: 'fade', dir: 'in' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'There. Whatever\'s waiting up there gets both of us at our best. Same road, different lamps — go on. I\'ll keep the fire.' },
  ],

  // The look-up bands: the Skyweave Crown through the open shafts (atmosphere
  // only — the darkest place in the game, under the greatest light).
  'script.spire_crown_1': [
    { op: 'narrate', text: 'Through the gatehouse\'s broken shaft, far overhead, the night is FULL: eight constellations standing lit at once, the Skyweave Crown complete, its light falling down the black throat of the mountain like rain into a well.' },
    { op: 'tint', color: '#9fd4ff', alpha: 0.16, ms: 900 },
    { op: 'narrate', text: 'The darkest place in Vesperholm — directly beneath the greatest light it has ever raised. Every lamp you lit is up there, looking back down the climb with you.' },
    { op: 'tint', color: '#9fd4ff', alpha: 0, ms: 900 },
  ],
  'script.spire_crown_2': [
    { op: 'narrate', text: 'Another open shaft; another column of Crown-light standing in the dark like a pillar holding the room up. The null-works hum somewhere below the floor — and the starlight comes down anyway. It always came down. It was only ever waiting to be answered.' },
  ],
  // The high-gallery breather: the wind above the world + the shaft hoist
  // (sets flag:spire_shaft via the trigger — the sanctioned re-climb compressor).
  'script.spire_wind': [
    { op: 'narrate', text: 'The gallery opens to the night, and there is WIND — true wind, the sky\'s own breath, this deep in the mountain. Every constellation you have relit hangs in the column of air above the shaft, near enough to read by.' },
    { op: 'narrate', text: 'An old hoist-lamp waits at the shaft\'s lip, wick sound, oil long set. You warm it with your own flame until it remembers its work.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Far below, a thread of starlight steadies down the spire\'s open core — the old hoist-line, lit end to end. The climb keeps a road home now.' },
  ],
  'script.pickup_spire_gatehouse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 2 },
    { op: 'say', text: 'A dead Lumenary\'s vestry chest, dry and sound: two BRIGHT BALMS, laid in against a long vigil that never came. Found them!' },
    { op: 'setFlag', flag: 'flag:picked_spire_gatehouse' },
  ],
  'script.pickup_spire_landing': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'On the hidden side-landing, where the Ninth Lantern\'s keepers once watched the sky: a STARGLASS SHARD and a BRIGHT BALM, kept forty years by the dark and the dry. Found them!' },
    { op: 'setFlag', flag: 'flag:picked_spire_landing' },
  ],
  'script.pickup_spire_gallery': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 800 },
    { op: 'say', text: "A toll-box from the lit years, its lock long since surrendered: 800 WICKS that never made it down the mountain. Found them!" },
    { op: 'setFlag', flag: 'flag:picked_spire_gallery' },
  ],

  // --- THE SUMMIT CHAIN ------------------------------------------------------
  // 1. The Great Null, SEEN (B5's reveal — the player has known its name since
  // Nightreach; no re-explaining, just the scale of it and the swept floor).
  'script.great_null': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 900 },
    { op: 'silence', ms: 2200 },
    { op: 'narrate', text: 'It fills the summit the way held breath fills a room: a bell of patient dark, vast as a Lumenary\'s dome, aimed with terrible courtesy at the one star that lets the others rekindle.' },
    { op: 'narrate', text: 'The Great Null. You have carried its name up half a world. Nothing about the name prepared you for how QUIET it is.' },
    { op: 'narrate', text: 'At its foot, a single gauge rests at zero. The floor around it has been swept — recently, carefully, by someone who still believes tidiness is a kindness you can do for the dark.' },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // 2. THE SCENE — Warden Còr's case at full strength, the battle as form, and
  // the resolution: he is NOT defeated. Winning earns the right to answer; the
  // answer is the out-remembering — every relit constellation named back at him
  // in one rising passage (the lamp-remembrance voice). His certainty breaks
  // INTO remembering. (Trigger banks flag:cor_answered; a loss aborts, retry-safe.)
  'script.warden_cor_final': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 900 },
    { op: 'silence', ms: 2000 },
    { op: 'narrate', text: 'He is standing with his back to you, hands folded, watching the Keystar the way other people watch a hearth. He knows you are there. He has known for eight constellations.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'You climbed kindly. My people sleep unhurt below, every one — I notice these things, apprentice. I have watched your lamps come up my dark like a slow sunrise, and I find I am glad of the company. Especially tonight.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'I had hoped you\'d be tired enough to agree with me. You\'ve seen the quieted towns — you\'ve seen how peaceful it is. I am not cruel, apprentice. I only want the grieving to stop.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'One lamp. This one — the last anchoring light — left gently unlit, and the long night settles soft and permanent over every valley that is tired of losing things. No more guttering. No more goodbyes. No more standing at a window with a wick in your hand, counting its hours and calling it hope.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'You could simply stop. That is all I have ever asked of anyone. Set the lamp down, apprentice — and be the first soul in Vesperholm the dark never takes anything from again.' },
    { op: 'say', if_flag: 'flag:wren_joined', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: '...Don\'t argue with him. You can\'t. Remember louder. Go on — I\'m right here.' },
    { op: 'narrate', text: 'You raise the vesperlamp. It is the only answer you have ever had — and tonight, at last, it is bright enough to be one.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: '...So be it. I will not pretend I hoped otherwise. And I will not pretend that some old, unhelpful corner of me is not proud of you.' },
    { op: 'letterbox', on: false, ms: 300 },
    { op: 'battle', trainer: 'warden_cor' },
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 700 },
    { op: 'silence', ms: 2200 },
    { op: 'narrate', text: 'His kin sleep where they fell — unhurt, every one; he is gentle even in losing. He gathers them in with a murmur each, like a man banking a fire for the night. He is not beaten. Nothing about him is beaten.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'Well kept, apprentice. ...But you understand by now that the battle proves nothing. I have lost arguments before. Grief always loses the argument — and then it stays anyway, and keeps the house.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'So. Say your piece. I have heard every argument in Vesperholm; I made most of them myself, alone, in this very dark. Say something I have not already grieved my way past.' },
    { op: 'narrate', text: 'You do not argue. You lift the vesperlamp between you — and let it remember.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.1, ms: 800 },
    { op: 'narrate', text: 'EMBER — a coast-town fair under strung lanterns, a whole harbour told that a small flame is no lesser thing. TIDE — a moor-bell rolling out over lantern-lit boats, a quay lending the sea its lamps because the sea keeps none of its own.' },
    { op: 'narrate', text: 'VERDANT — a hollow where the moss flowered all at once and outshone its own lantern-strings. STONE — a mining town dimming every lamp on purpose, honouring its dark, and lighting every single one again.' },
    { op: 'tint', color: '#ffd089', alpha: 0.2, ms: 800 },
    { op: 'narrate', text: 'STORM — a hundred small flames climbing the night on kite-tails, so the stars had something to answer. FROST — a town out on black ice in perfect silence, every flame held in a bare hand, every flame CHOSEN.' },
    { op: 'narrate', text: 'SOLAR — the last warm day, spent gladly, in front of the watching dark, knowing it fades; that being the point. LUNAR — a town that watches all night, every night, so that the sky is never once alone.' },
    { op: 'flashColor', color: '#ffd089', ms: 260 },
    { op: 'tint', color: '#ffd089', alpha: 0.3, ms: 900 },
    { op: 'narrate', text: 'And the kin. The small bright lives that chose your road and walked it — light caught, light kindled, light carried in a lamp and carried back OUT of it, freely, over and over, all the way up this mountain. Every one of them a goodbye waiting to happen. Every one of them worth it. Every one.' },
    { op: 'silence', ms: 1800 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: '...You\'re not arguing with me. You\'re REMEMBERING at me. All of it — every lamp, every name, every small goodbye you\'d have me erase.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'I remember the ache, apprentice. I built every stone of this against the ache. But the fair, the bell, the kites on the dark, the bread going round while the braziers held... I had forgotten it was worth the ache.' },
    { op: 'narrate', text: 'His certainty does not shatter. It goes the way ice goes at the first thaw — quietly, from underneath, into something that moves again.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'at_peace', text: 'The gauge stands at zero. It has always stood at zero. Two years I told myself I was waiting to be certain — and certainty never came, because some mercies cannot survive being looked at by a lit lamp.' },
    { op: 'narrate', text: 'Warden Còr folds his hands, and steps aside from his own great work — undone by no force in Vesperholm except everything he had made himself forget.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'at_peace', text: 'Go and wake the Keystar, apprentice. It has been listening to you far longer than I have.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1100 },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // 3. The Keylumen — the climax catch/relight (interact at the dais, requires
  // flag:cor_answered). A set-piece battle, not a wild roll: the kin cannot
  // flee, a miss withdraws for ZERO won battles (raise the lamp and ask again —
  // the climax never strands), and Fenn's Starlamp is the intended asking.
  // The apex Gleam cadence: the game's longest silence, then minor→major on
  // umbral-spire-c ("First True Dawn"). Trigger banks flag:keystar_relit.
  'script.keystar_relight': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'narrate', text: 'Above the Great Null\'s silenced mouth the Keystar hangs small and patient, the one light the whole sky remembers itself by. And in the dais under your hands, something stirs toward your lamp-glow.' },
    { op: 'narrate', text: 'A curl of white-gold light unfolds from the old lantern-housing: the KEYLUMEN, the Keystar\'s living heart, asleep in the Ninth Lantern since the night fell — awake now, and regarding your lamp the way a kin regards a door held open.' },
    { op: 'narrate', if_flag: 'flag:wren_joined', text: 'Behind you, Wren says nothing at all — just lifts their lamp, the way you both learnt on the coast road. The asking is yours.' },
    { op: 'narrate', if_flag: 'flag:fenn_counsel_given', text: 'In your satchel, Fenn\'s starlamp is warm as a held hand. Forty years he kept it — for exactly this asking.' },
    // The asking must never dangle on a spent key item: if the Starlamp went to
    // some other wonder on the road, the dais holds a second (Fenn never trusted
    // a single road) — granted only when the satchel is empty of one.
    { op: 'ensureItem', item: 'starlamp', count: 1, text: 'Set into the dais\'s old lantern-housing, wrapped against the dust: a STARLAMP. A star-tender\'s hand placed it here long ago — Fenn never did trust a single road to carry anything that mattered.' },
    { op: 'letterbox', on: false, ms: 300 },
    { op: 'legendaryBattle', name: 'keylumen', kin: 149, level: 55, caughtFlag: 'flag:keylumen_caught', cooldownBattles: 0, cooldownRef: 'npc.keylumen_waits' },
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 700 },
    { op: 'silence', ms: 2600 },
    { op: 'narrate', text: 'The Keylumen settles into your lamp — and then rises THROUGH it, up the open shaft of the mountain, up past the Crown, a thread of white-gold paying out from your hands into the highest dark.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#fff3c9', alpha: 0.35, ms: 1400 },
    { op: 'gleam', element: 'light' },
    { op: 'musicCrossfade', key: 'umbral-spire-c', ms: 1400 },
    { op: 'narrate', text: 'The Keystar CATCHES. Light pours back along the Skyweave like a tide remembering its shore — eight constellations flaring in answer, the Crown blazing whole, the night over Vesperholm turning legible from rim to rim.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'at_peace', text: '...There it is. The view from the top of the ladder. I named half those stars, apprentice — and tonight is the first time in twenty years I have let myself look at them.' },
    { op: 'flashColor', color: '#fff3c9', ms: 300 },
    { op: 'tint', color: '#fff3c9', alpha: 0, ms: 1600 },
    { op: 'narrate', text: 'The Keystar holds. The sky remembers itself. And somewhere below the mountain, in valley after valley, lamps are going up in windows to answer it.' },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // 4. DAWN BREAKS — fired as you turn from the dais and walk back into the
  // world (requires flag:keystar_relit). Sets flag:dawn ITSELF (the cinematic
  // hand-over never returns, so the trigger's banking can't be relied on), then
  // Fenn's offer to Còr — mercy answered with mercy — and the hand-over to the
  // dawn panels + credits (the dawn-breaks track belongs to the cinematic).
  'script.dawn_breaks': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'silence', ms: 1800 },
    { op: 'narrate', text: 'You turn from the dais — and the light comes with you. Over the rim of the world, for the first time in years, the east goes grey. Then silver. Then, unbelievably, GOLD.' },
    { op: 'setFlag', flag: 'flag:dawn' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.25, ms: 1600 },
    { op: 'narrate', text: 'A lamp is climbing the dawn road below — small, steady, unhurried. Star-tender Fenn, who would not climb in the dark, climbing in the light.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'I watched it begin from the waystone, child. Then I looked down and found my legs had already started walking.' },
    { op: 'narrate', text: 'He passes you with one press of your shoulder — and goes to the rail, where Còr stands with the morning on his face like a man rereading an old letter.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'You read the same sky I did, old friend. There\'s still a lamp lit for you. ...Come down and tend it with me.' },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'Còr does not answer in words. He picks up his cold hand-lamp, turns it over once — and follows his friend down toward the morning, leaving the Great Null to the swallows and the rust.' },
    { op: 'say', if_flag: 'flag:wren_joined', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'Same road, different lamps — all the way to the end of the sky. ...And now we get to see where it goes in daylight. Come on, Wayfarer. Walk me home.' },
    { op: 'narrate', text: 'The long night breaks. Not into a victory — into a morning. Dusk will come again; that is the whole of it. The dawn is worth the dark precisely because it can be lost.' },
    { op: 'cinematic', id: 'ending_credits' },
  ],

  // ===========================================================================
  // THE THREE HOURS (walkthrough/07-the-three) — the legendary triad: Gloamber
  // (#160, Tideglass Gallery), Noctilune (#161, the Hourfold), Erstmorn (#162,
  // the Unrisen Stair). Awe-and-ache register, BINDING: zero humour at the
  // sites; each chain's ONE dry line lives on its rumour-giver below. The
  // three legendaryBattle ops are the spec's VERBATIM shapes. Catch tails
  // follow the §3 cadence: a held quiet, then the area bed returns warmer.
  // ===========================================================================

  // --- H1 "The Hour Below" — the unlock chain (Pearlmoor → Tideglass) --------
  // The netmender's terminal S1 stage now carries the rumour: her done-line
  // always plays; the rumour rides if_flag gleam:verdant (Glimmerstep held —
  // the cavern is reachable) and banks flag:three_dusk_rumour, swapping her
  // placement to npc.netmender_hours_after. Intentional data conditional:
  // optional-content unlock, not progression.
  'script.netmender_hours': [
    { op: 'dialogue', ref: 'npc.netmender_done' },
    { op: 'say', if_flag: 'gleam:verdant', speaker: 'NETMENDER', text: 'And since you keep turning up wherever a lamp wants tending — here\'s a thing I would tell nobody sensible.' },
    { op: 'say', if_flag: 'gleam:verdant', speaker: 'NETMENDER', text: 'There\'s a low singing in the cliff at lamp-lighting time. Could be the tide. Tide\'s never once kept a tune before, mind.' },
    { op: 'say', if_flag: 'gleam:verdant', speaker: 'NETMENDER', text: 'It comes up out of Tideglass — the glass cavern under the coast, where the old fisher\'s wreck went down. Deep-walkers\' ground now, with that glimmer-step of yours. If something under the glass sings the evening in... somebody who LIGHTS things ought to go and hear it.' },
    { op: 'setFlag', if_flag: 'gleam:verdant', flag: 'flag:three_dusk_rumour' },
  ],

  // --- Tideglass Cavern: the wreck-lamp (S3 "The Cavern Keeps a Light" pays).
  // Interact gated on flag:q_south_wrecklamp (the fisher's tale); the trigger
  // banks flag:q_south_wrecklamp_lit — consumed by the inn's thanks stage AND
  // the verse plaque's live twin.
  'script.tideglass_wrecklamp': [
    { op: 'narrate', text: 'The wreck at last — her ribs glass-smooth, her stern-lamp wedged where she broke, exactly as a drowning man has remembered it for forty years.' },
    { op: 'narrate', text: 'The wick is salt-stiff and patient. You trim it the way you were taught, and lend it your flame.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.2, ms: 700 },
    { op: 'narrate', text: 'It takes. Light walks out across the smoothed glass in every direction — the walls, the black water, the veined teal deep of it — and the cavern that kept one light burning for three days is a lit place again.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'An old man at a quayside inn is owed the telling. And under your boots, faint as a held note, something low sings the evening in.' },
  ],

  // The verse on the wreck-lamp's glass hood. ONE requires_flag rides the
  // trigger (the lamp burning); the rumour gate lives HERE — without the
  // netmender's word the etching stays craft, never directions, and the flag
  // is only banked once both are held (the spec's wiring-pass note).
  'script.three_dusk_verse': [
    { op: 'narrate', text: 'With the wreck-lamp burning, its glass hood comes alive: etched lines catch the flame and stand out silver — verse-marks, in an old lampwright\'s hand, sure and small.' },
    { op: 'narrate', if_flag: 'flag:three_dusk_rumour', text: '"LAST LIGHT FIRST; THE LOW LIGHT AFTER; THE DEEP LIGHT ONCE THE OTHERS HOLD."' },
    { op: 'narrate', if_flag: 'flag:three_dusk_rumour', text: 'Three standing lenses wait in the cavern\'s dark — the west shelf, the mid-pool, the stair seam. The low singing under the floor has not stopped. It is, you realise, keeping time.' },
    { op: 'setFlag', if_flag: 'flag:three_dusk_rumour', flag: 'flag:three_dusk_verse' },
  ],

  // The Lampwright's Relay — three lenses lit in verse order (the triggers
  // chain the flags; cold twins swap on the same flags; wrong order answers
  // with npc.tideglass_lens_cold).
  'script.three_dusk_lens_a': [
    { op: 'narrate', text: 'The amber lens, on the west shelf — last light: the colour of an evening\'s end. You raise the vesperlamp to it.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'The glass warms from cold to honey, and the wreck-lamp\'s far beam leans INTO it, gathered and carried one span deeper into the dark. Somewhere below, the low singing turns toward you.' },
  ],
  'script.three_dusk_lens_b': [
    { op: 'narrate', text: 'The low lens, out on the mid-pool islet, barely above the black water.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'It takes the amber beam and bends it low across the pool — light skating the still water the way dusk lies down along a valley floor. One span deeper. The singing is very close now.' },
  ],
  'script.three_dusk_lens_c': [
    { op: 'narrate', text: 'The deep lens, by the stair seam — and behind you the other two hold, exactly as the verse asked.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.2, ms: 700 },
    { op: 'narrate', text: 'The relayed beam pours through it and DOWN, into the seam — and the glass rings: one low note through the floor, through your boots, through the water. The whole cavern is the bell.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'The stair seam breathes open. Below, in a chamber you cannot see, the pooled light is being waited on.' },
  ],

  // The Dusk Hour (Tideglass Gallery) — the game's first legendaryBattle.
  // Spec-verbatim staging + op; the catch tail returns the area bed warmer.
  'script.three_dusk_battle': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'The glass warms. Something that has carried the evening a long time lifts its head.' },
    { op: 'letterbox', on: false },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    { op: 'legendaryBattle',
      name: 'three_dusk', kin: 160, level: 38,
      caughtFlag: 'flag:three_dusk_caught',
      cooldownBattles: 10,
      cooldownRef: 'npc.three_dusk_resting',
      terrain: 'cave' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'The Dusk Hour folds itself into your lamp the way evening folds into a valley — heavily, gratefully, an old weight set down at last. Among your kin, its chest-coal settles to a banked and steady glow.' },
    { op: 'musicCrossfade', key: 'dimglass-coast-c', ms: 1600 },
  ],

  // Tideglass caches (the standing region kit; the nook is the spine §5
  // Starlight reveal — its placement is gated on flag:lamplight_starlight).
  'script.pickup_tideglass_starshard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In the cavern\'s deepest fold, where only a Starlight lamp reaches: a STARGLASS SHARD, dusk-coloured to its heart — the old fisher\'s deeper page, kept by the glass. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_tideglass_starshard' },
  ],
  'script.pickup_tideglass_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'A deep-walker\'s tin, wedged dry above the waterline on the west shelf. Found 2 WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_tideglass_balm' },
  ],
  'script.pickup_tideglass_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: 'The wrecked boat\'s strongbox, holding exactly what a small fisher\'s boat would hold. Found 250 WICKS — forty years too late for her keeper, and right on time for her lamp.' },
    { op: 'setFlag', flag: 'flag:picked_tideglass_wicks' },
  ],

  // --- H2 "The Longest Watch" — the unlock chain (Pale Vault → the Hourfold).
  // The aurora-watcher's post-Frost stage carries the rumour (her dry line is
  // the chain's one sanctioned humour beat), then Ysolde's snuffer arms the
  // fold's warp gate.
  'script.aurorawatcher_hours': [
    { op: 'say', speaker: 'WATCHER', text: 'You again, with the warded flame. Good. Stand with me a moment and look where I am looking — past the blue fold, into the deep ice.' },
    { op: 'say', speaker: 'WATCHER', text: 'The aurora bends round that fold like it\'s queuing. Forty years I\'ve watched the sky. It has never once queued for me.' },
    { op: 'say', speaker: 'WATCHER', text: 'Whatever it waits on, it is a watcher\'s matter, and the ice has sealed it shut. Ysolde keeps the undercroft below the vault. She will know what a vigil that old asks of a visitor — ask her before you go prying at the fold.' },
    { op: 'setFlag', flag: 'flag:three_mid_rumour' },
  ],
  'script.ysolde_snuffer': [
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'The watcher sent you. I wondered which winter would finally ask. ...Yes. Something keeps the deep ice, wanderer — has kept it since before this vault had brackets to light. The Still Hour. Midnight itself, standing a watch with no relief.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Three vigil-braziers burn at the bottom of the fold. Ours — kept lit by generations of watchers, so the Hour would not stand unwitnessed. But it will not be SEEN by their light. To meet midnight, you must bring it the dark: kept, and deliberate.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'vigil_snuffer', count: 1 },
    { op: 'say', text: 'Received the VIGIL SNUFFER — a long-handled cap of cold iron, worn smooth by careful hands.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'You have spent the whole road lighting things. The Still Hour will want to see that you understand the other half of tending.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'The aurora will name the order — read the sky before the shelf. And wanderer: what you put out down there, you put out ON PURPOSE. That is the entire difference between a tender and the Hollowing.' },
    { op: 'setFlag', flag: 'flag:three_mid_snuffer' },
  ],

  // The Unstruck Toll — three braziers SNUFFED in aurora order (east →
  // water-ice → west). The one inverted light verb in the game; the dark made
  // here is kept, not surrendered. Triggers chain the flags; lit→snuffed
  // object swaps ride the same flags; wrong order answers with
  // npc.hourfold_flame_leans. Nothing resets — the cooldown is the cost.
  'script.three_mid_brazier_a': [
    { op: 'narrate', text: 'The east brazier first, under the kneeling ribbon. You raise the Vigil Snuffer the way Ysolde would — slowly, and on purpose — and cap the blue-white flame like a door held open for someone leaving.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'The flame goes, gently. The dark that takes its place is not the Hollowing\'s — it is yours, chosen and kept. One. Overhead, the aurora pours a shade brighter.' },
  ],
  'script.three_mid_brazier_b': [
    { op: 'narrate', text: 'The centre brazier, out on the water-ice. Your own lamp seems very loud here.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'Two. The shelf is more aurora than firelight now, and the silence has changed its quality — from an empty room to an occupied one.' },
  ],
  'script.three_mid_brazier_c': [
    { op: 'narrate', text: 'The west brazier, last. The snuffer is steady. Your hands, less so.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 700 },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'The dark does not deepen. It straightens, as if relieved of a stoop.' },
    { op: 'narrate', text: 'On the far shelf, what you took for a dome of black ice unrolls — pane over pane of midnight glass, one star kept in each — and stands. A sentinel, hooded in the whole night sky, regarding your small kept dark.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The Still Hour (the Hourfold's bottom shelf) — spec-verbatim op.
  'script.three_midnight_battle': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'It does not move as you approach. It has been still long enough to grow stars. Only the thin silver crescents of its eyes turn — and the unstruck bell at its throat holds its silence like a kept vow.' },
    { op: 'letterbox', on: false },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    { op: 'legendaryBattle',
      name: 'three_midnight', kin: 161, level: 48,
      caughtFlag: 'flag:three_mid_caught',
      cooldownBattles: 14,
      cooldownRef: 'npc.three_midnight_resting',
      terrain: 'cave' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'The Still Hour folds into your lamp pane by pane — the midnight sky kneeling down small, the watch handed over at last. Somewhere in the lamp-light, for the first time in years, midnight is relieved.' },
    { op: 'musicCrossfade', key: 'pale-vault-glacier-c', ms: 1600 },
  ],

  // The fold's one [MISSABLE] cache, behind the false ledge-line (mundane
  // periphery — the one sanctioned dry note at this site lives on a tin).
  'script.pickup_hourfold_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Wedged in the pocket where every wrong ledge-drop lands: a MOTH-AMBER, glowing patiently. Found it! Whoever dropped it took the false line too, and decided against climbing back for it.' },
    { op: 'setFlag', flag: 'flag:picked_hourfold_amber' },
  ],

  // --- H3 "The Unrisen Stair" — the unlock chain (Nightreach → the Solarium).
  // Nessa is sincere — she is the haunted one; Lucan carries the chain's one
  // dry line with the First-Light Phial.
  'script.nessa_hours': [
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'Wayfarer. Come up to the eyepiece — no, you needn\'t look. Listening is the trouble, tonight.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'Every chart says the morning bell should hang due west of here. There is no morning bell. There has been no morning. And yet three nights running I have heard a bell that hasn\'t rung — WAITING makes a sound, you know, if it goes on long enough.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'reverent', text: 'Due west is the Solarium\'s drowned garden — and off its deepest fold, the old processional stair no one has climbed since the sky kept hours. If something waits there for a morning... it has been waiting longest of anything alive.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'neutral', text: 'Lucan kept the last warm day. Ask him whether anyone thought to keep the last MORNING. If anyone would know, it is the man who hoards daylight.' },
    { op: 'setFlag', flag: 'flag:three_dawn_rumour' },
  ],
  'script.lucan_phial': [
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'grand', text: 'The last MORNING? ...Nessa heard her bell again, didn\'t she. Then it is time — and I have been holding this cue for forty years.' },
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'bittersweet', text: 'I kept the last warm day for forty years. Apparently somebody kept the last morning and never thought to mention it. Theatrical of them. I approve.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'first_light_phial', count: 1 },
    { op: 'say', text: 'Received the FIRST-LIGHT PHIAL — one cupful of daylight, drawn the morning before the Long Dusk fell. Through the glass it beats faintly, like something with a pulse.' },
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'bittersweet', text: 'The dry sun-basin at the garden\'s deepest fold, before the sealed stair. Pour it there — all of it, mind. No saving some for later. First light is an entrance; you do not make half of one.' },
    { op: 'setFlag', flag: 'flag:three_dawn_phial' },
  ],

  // The basin pour (host trigger on sunken_solarium banks flag:three_dawn_poured
  // — the warp gate's key and bloom A's requires).
  'script.three_dawn_basin': [
    { op: 'narrate', text: 'The sun-basin waits where a first light was meant to land. You unstop the First-Light Phial — and for one moment the smell of MORNING, bread-warm and years gone, stands in the dark garden like a person.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#fff3c9', alpha: 0.14, ms: 900 },
    { op: 'narrate', text: 'You pour. One cupful of daylight fills the basin to its brim and HOLDS, lying there like the first coin of a sunrise. Beyond the seal, on the stair no one has climbed, the lowest sun-vine stirs in its sleep.' },
    { op: 'tint', color: '#fff3c9', alpha: 0, ms: 1100 },
  ],

  // The Bloom Ascent — sequential + redirect (the Sunsketch dimension in
  // full). Bloom A rides the step_on bands; the mirror is the redirect; the
  // far vine's bands answer npc.unrisen_far_vine until the daylight is bent.
  'script.three_dawn_bloom_a': [
    { op: 'narrate', text: 'The basin\'s pocket of morning climbs the stair with you — and the first sun-vine takes it: blooms, swells, and lays itself across the black water, a bridge that believes you about the daylight.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Across the second water, the far vine sleeps on, untouched. And on the east spur, something of bronze and glass turns very slightly, the way a sleeper turns toward a window.' },
  ],
  'script.three_dawn_mirror': [
    { op: 'narrate', text: 'The sun-mirror flower, shut these long years, feels the cupful of morning arrive and turns its face to it.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#fff3c9', alpha: 0.12, ms: 800 },
    { op: 'narrate', text: 'It opens — bronze petal by glass petal — and BENDS the pocket of daylight out across the water in one long bright line, to the far bank, where the last vine sleeps. The old gardeners\' redirect, working one more time.' },
    { op: 'tint', color: '#fff3c9', alpha: 0, ms: 900 },
  ],

  // The flight-two cache ([MISSABLE], a fallen capital).
  'script.pickup_unrisen_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In a fallen capital off the second flight, set down by some procession that never came back: a STARGLASS SHARD, keeping its light face-down against the years. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_unrisen_shard' },
  ],

  // The Lost Hour (the head terrace) — the climax foreshadow. Sets
  // flag:three_dawn_met BEFORE the op, win or withdraw (Fenn's Crossroads
  // line consumes it); the false-dawn tint deliberately rhymes with the
  // Keystar relight (#fff3c9 — same family, a fraction of the strength). The
  // op is spec-verbatim: NO terrain — the last Hour offers no shortcuts.
  'script.three_dawn_battle': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 1200 },
    { op: 'setFlag', flag: 'flag:three_dawn_met' },
    { op: 'tint', color: '#fff3c9', alpha: 0.12, ms: 1400 },
    { op: 'narrate', text: 'For one held breath, the stair remembers what it was for.' },
    { op: 'tint', color: '#fff3c9', alpha: 0, ms: 1100 },
    { op: 'narrate', text: 'Where the first light was meant to land, something half-finished stands facing east. It has been facing east for years. It does not turn — but its sketched ear tilts, very slightly, toward your lamp.' },
    { op: 'letterbox', on: false },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    { op: 'legendaryBattle',
      name: 'three_dawn', kin: 162, level: 55,
      caughtFlag: 'flag:three_dawn_caught',
      cooldownBattles: 18,
      cooldownRef: 'npc.three_dawn_resting' },
    { op: 'silence', ms: 1400 },
    { op: 'narrate', text: 'The Lost Hour steps into your lamp mid-stride, the way it has stood for years — and does not quite finish arriving, because part of it is still waiting where every morning waits. It will go with you. It was never going to stop facing east.' },
    { op: 'musicCrossfade', key: 'sunken-solarium-c', ms: 1600 },
  ],

  // Fenn's counsel-after stage (Vesper Crossroads) — wraps the standing line
  // and adds the §6 payoff once flag:three_dawn_met is held (the flag's one
  // consumer alongside the counsel script's guarded step).
  'script.fenn_counsel_after': [
    { op: 'dialogue', ref: 'npc.fenn_counsel_after' },
    { op: 'say', if_flag: 'flag:three_dawn_met', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'So you found the third watch. Still facing east, was it? ...Then it has never stopped believing the wheel can turn. Neither have I. Go and prove the pair of us right.' },
  ],
  // ===========================================================================
  // DAWNSTEAD — the post-game epilogue town (walkthrough 06-postgame, R2).
  // The quiet exhale after the climax: almost no spectacle, all warmth and
  // faces. Canon tone: bittersweet-warm — the cycle has resumed, dusk will
  // come again, and that is exactly the point.
  // ===========================================================================

  // THE ARRIVAL — the first scripted beat is simply the sky. Let the player
  // stand in it; the map's own music IS the lullaby returned in major.
  'script.dawnstead_arrival': [
    { op: 'wait', ms: 500 },
    { op: 'narrate', text: 'Morning. Not lamplight, not moonrise, not the kind hour of a festival — morning, blue and gold, lying over everything at once.' },
    { op: 'tint', color: '#ffd98a', alpha: 0.18, ms: 1200 },
    { op: 'narrate', text: 'Warm shadows. Open sky. Somewhere up the green, the old lullaby — the one every lamp-tender hums — and for the first time in years it is not asking the dark for anything.' },
    { op: 'tint', color: '#ffd98a', alpha: 0, ms: 1400 },
    { op: 'narrate', text: 'The rooflines are Tinderwick\'s. The dock is Tinderwick\'s. It is home, and it is not — because the dark has lifted, and nothing that woke this morning is quite what it was.' },
  ],

  // THE FIRST-DAWN FESTIVAL (Arc E capstone) — the whole town out in the sun:
  // the thesis of "belonging, not conquest," now in daylight. Ambient colour,
  // a small warm swell that hands straight back to the town loop.
  'cutscene.dawnstead_first_dawn': [
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'narrate', text: 'The square is full. Nobody organised it; the sun came up and Vesperholm walked outside to be underneath it — the first-dawn festival, the one no calendar ever dared to print.' },
    { op: 'say', text: '"No lanterns tonight!" someone calls, and laughs, and then has to sit down on the well-step about it.' },
    { op: 'narrate', text: 'Eight festivals taught the valleys how to gather in the dark. This is what all that practice was for.' },
    { op: 'musicCrossfade', key: 'dawnstead-a', ms: 1400 },
  ],

  // FENN ON THE FRONT — the mentor's arc settles into peace (Arc D payoff,
  // spec lines verbatim), then the post-game slate: P2 "A Wick for Còr" and
  // P3 "The Day-form Survey" (boolean-chain fallback, spine §8).
  'script.fenn_dawnstead': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'First true morning in years. Don\'t waste it asking whether it\'ll last — it won\'t. That\'s the bargain. Dusk for dawn, dawn for dusk. We tend the turning, that\'s all.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'You did well, apprentice. Go and look at your sky.' },
    { op: 'wait', ms: 350 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: '...Still here? Then I\'ll be a teacher one minute longer. Two errands, neither urgent — nothing is urgent any more; I keep saying it to feel it said.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'The first: Còr keeps a lamp on the west strand, past the old tree. Climb the Tinderwick Beacon and draw him a fresh wick from the lantern room. A lamp burns as its wick is given — and his was given in the dark. Let it be given again in daylight.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'The second: the relit sky is WAKING things. Sun-bright moths in the verge grass — day-forms, the old journals called them. Walk the sunlit verge and find me three signs of them. One at a time, mind; surveys are patience wearing boots.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Start by the verge\'s north corner — the dawn-blooms there have been fed on. Something gold did the feeding.' },
    // P2's assignment flag gates the Beacon wick-case (QA MIN-1: without it the
    // wick could be drawn before Fenn frames the errand — a narrative skip).
    { op: 'setFlag', flag: 'flag:q_post_wick_asked' },
    { op: 'setFlag', flag: 'flag:q_post_survey' },
  ],
  // P3, the waiting stage — Fenn names ONE mark at a time (the chained finds
  // order the if_flag lines: the latest held flag reads last and truest).
  'script.fenn_survey_wait': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'The survey, apprentice. The verge\'s north corner first — the fed-on dawn-blooms. Look close and bring me what the morning left.' },
    { op: 'say', if_flag: 'flag:q_post_survey_1', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'A wing-scale, gold as a struck match — the moth\'s page is inked. Next: the verge\'s south skirt, by the shore side. Something shed its dusk coat there and did not look back.' },
    { op: 'say', if_flag: 'flag:q_post_survey_2', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'A whole moult, dusk-grey, empty as an outgrown word. One sign left: the blooms by the garden mouth — there\'s a warm burrow under them, and its keeper came home at sunrise.' },
  ],
  'script.fenn_survey_done': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Scale, moult, and a warm doorstep. Three signs, three day-forms — the sky relit, and the small lives answered it first. That is the whole of star-tending in one verge.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Take the page — I have been keeping it for exactly this. And mark the note at the bottom: your vesperlamp is at its brightest now, Radiant as it will ever be. The dark places you crept through at a candle\'s reach... walk them again. They have been holding things for you.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fenn_journal_page', count: 1 },
    { op: 'say', text: 'Received FENN\'S JOURNAL PAGE!' },
    { op: 'setFlag', flag: 'flag:q_post_survey_done' },
  ],
  // The three survey-mark finds (interact, chained 1 -> 2 -> 3).
  'script.survey_find_1': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'Under the fed-on dawn-blooms: a single wing-scale, gold as a struck match and warm to the touch. The moths came out bright this morning.' },
    { op: 'setFlag', flag: 'flag:q_post_survey_1' },
  ],
  'script.survey_find_2': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'In the grass by the shore skirt: a shed moult, dusk-grey and paper-light — the whole night-coat, stepped out of and left where it fell. Whatever wore it is wearing morning now.' },
    { op: 'setFlag', flag: 'flag:q_post_survey_2' },
  ],
  'script.survey_find_3': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'Beneath the blooms at the garden mouth, a burrow — lined, lived-in, and warm as a banked hearth. Its keeper came home with the sunrise and is sleeping off the dark.' },
    { op: 'setFlag', flag: 'flag:q_post_survey_3' },
  ],

  // WREN BY THE WATER — A6, the rival-friend arc's warm coda (spec lines
  // verbatim). Talk first; the rematch is offered, not forced — it waits on
  // the next placement, re-runnable forever.
  'script.wren_dawnstead': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'I spent the whole Wayfaring asking if the Hollowing had a point. Turns out they did — and so did the dawn. Both true. Funny how that works.' },
    { op: 'wait', ms: 600 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'One more battle? For old times. Loser buys the lanterns.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'Whenever you like. I\'m not going anywhere — that\'s rather the point of here.' },
    { op: 'setFlag', flag: 'flag:wren_a6' },
  ],
  'script.wren_rematch': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'Lanterns on the line, then. Friendly rules — the morning\'s watching.' },
    { op: 'battle', trainer: 'wren_rematch' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'Worth it every single time. Same shore tomorrow, if the sun keeps its word — and I\'m told it does, now.' },
  ],

  // CÒR TENDING A LAMP — the resolution payoff (Arc B close; spec lines
  // verbatim). The toolkit's gentlest beat: low music, a touch of warm tint,
  // never gloating, never punished. Sets no progression flag — the band's own
  // hide flag is its only bookkeeping.
  'cutscene.cor_resolution': [
    { op: 'musicFade', ms: 900 },
    { op: 'narrate', text: 'Off to one side of the morning, where the strand narrows past the old tree, a man in faded warden\'s grey kneels at a single lamp — trimming it, steadying it, the way you tend a thing you mean to keep.' },
    { op: 'say', speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'I wanted to spare everyone the dusk. I had forgotten that the lamp is for the dark — not against it.' },
    { op: 'tint', color: '#ffd98a', alpha: 0.14, ms: 1100 },
    { op: 'narrate', text: 'He tends the flame.' },
    { op: 'say', speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'It will fall again, you know. The night. I find I no longer mind. I\'ll be here to light it.' },
    { op: 'tint', color: '#ffd98a', alpha: 0, ms: 1300 },
    { op: 'musicCrossfade', key: 'dawnstead-a', ms: 1600 },
  ],
  // P2 — the wick comes home (hand-in). His lamp burns a shade warmer
  // thereafter (the deco swap pair rides flag:q_post_wick_given).
  'script.cor_wick_given': [
    { op: 'say', speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'gentle', text: 'From the Beacon\'s own lantern room. Fenn\'s doing — he always did teach by errand.' },
    { op: 'narrate', text: 'Còr takes the First-Dawn Wick in both hands, the way the Hearthkeeper takes a tired kin, and sets it to the flame.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd98a', alpha: 0.2, ms: 900 },
    { op: 'say', speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'There. A wick dipped in daylight, burning toward the next dark. That is the whole prayer, apprentice — I simply used to say it backwards.' },
    { op: 'tint', color: '#ffd98a', alpha: 0, ms: 1100 },
    { op: 'setFlag', flag: 'flag:q_post_wick_given' },
  ],
  // P2 — the wick itself, drawn in the Beacon's lantern room (tinderwick_
  // beacon_top; cache appears post-dawn, vanishes once drawn).
  'script.pickup_post_wick': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'The lantern room keeps a case of fresh-dipped wicks, as it always has. You draw one — dipped this very morning, the first wick in years to be made by daylight.' },
    { op: 'giveItem', item: 'dawn_wick', count: 1 },
    { op: 'say', text: 'Took the FIRST-DAWN WICK! Còr keeps his lamp on Dawnstead\'s west strand.' },
    { op: 'setFlag', flag: 'flag:q_post_wick' },
  ],

  // P1 "FIRST-DAWN LETTERS" — the Waykeeper's daylight round (giver: the
  // post-bag at the Vesper Crossroads waystone). Deliverable in any order;
  // the quadrant-seat wardens stamp their replies (the keepsake reward).
  'script.post_letters_give': [
    { op: 'say', speaker: 'WAYKEEPER', text: 'Ah — the feet themselves. The dawn came up and half of Vesperholm wrote to the other half about it; my round\'s never been so heavy or so happy.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Take the bundle? Wren and old Fenn are down in Dawnstead, and there\'s a letter for every Lampwarden\'s town besides — eight of them, any order you please. The roads are awake again; somebody should walk all of them at once.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'dawn_letters', count: 1 },
    { op: 'say', text: 'Received the FIRST-DAWN LETTERS!' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'No hurry, mind. First post in years that nobody\'s waiting on in the dark.' },
    { op: 'setFlag', flag: 'flag:q_post_letters' },
  ],
  'script.post_letter_wren': [
    { op: 'narrate', text: 'A letter for Wren, in the Waykeeper\'s careful hand.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'For ME? ...It\'s from the kite-makers at Galehigh. They want the ribbon back for the museum wall. HA! Tell them to come and take it.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_wren' },
  ],
  'script.post_letter_fenn': [
    { op: 'narrate', text: 'A letter for Star-tender Fenn.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Post, at my age, in this light. ...It\'s from the Waykeeper himself. One word. "WELL?" — and do you know, for once I haven\'t a correction to make.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_fenn' },
  ],
  'script.post_letter_tinderwick': [
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'First-dawn post! Look at it — somebody wrote the word "morning" and didn\'t put a candle-count after it. Frame-worthy, that.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_tinderwick' },
  ],
  'script.post_letter_pearlmoor': [
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'A letter that crossed no dark water to get here. Longest I\'ve waited for any post in my life.' },
    { op: 'narrate', text: 'Reyl presses his wax stamp to the reply — the southern quadrant\'s thanks, kept.' },
    { op: 'giveItem', item: 'dawn_stamp', count: 1 },
    { op: 'setFlag', flag: 'flag:q_post_letter_pearlmoor' },
  ],
  'script.post_letter_lowleaf': [
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'Oh — post. In the sun. The Elder Bed greened before any of us were up, you know. It always was the better botanist.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_lowleaf' },
  ],
  'script.post_letter_cinderhead': [
    { op: 'say', speaker: 'OTHO GRIST', text: 'Mail, up from the morning. The deep way\'s the same as ever — but the walk OUT ends in daylight now, and the crews keep finding reasons to make it.' },
    { op: 'narrate', text: 'Otho stamps the reply with the pit-seal — the eastern quadrant\'s thanks, kept.' },
    { op: 'giveItem', item: 'dawn_stamp', count: 1 },
    { op: 'setFlag', flag: 'flag:q_post_letter_cinderhead' },
  ],
  'script.post_letter_galehigh': [
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'A letter! Carried on FOOT? In THIS wind? We\'d have flown it for you — oh, but then we\'d have missed you. Fair trade!' },
    { op: 'setFlag', flag: 'flag:q_post_letter_galehigh' },
  ],
  'script.post_letter_pale_vault': [
    { op: 'say', speaker: 'YSOLDE', portrait: 'ysolde', expr: 'serene', text: 'The glacier took the sunrise like a held breath let go. Your letter arrives second, and is welcome anyway.' },
    { op: 'narrate', text: 'Ysolde sets her frost-seal to the reply — the northern quadrant\'s thanks, kept.' },
    { op: 'giveItem', item: 'dawn_stamp', count: 1 },
    { op: 'setFlag', flag: 'flag:q_post_letter_pale_vault' },
  ],
  'script.post_letter_solarium': [
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'grand', text: 'Post! Delivered into an ENCORE — the sun is doing my whole repertoire for free, and I find I could not be happier about the competition.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_solarium' },
  ],
  'script.post_letter_nightreach': [
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'reverent', text: 'A first-dawn letter. I watched the whole sky come back, and still — ink on paper, carried by hand. That is the light I trust most.' },
    { op: 'narrate', text: 'Nessa presses the observatory\'s star-seal to the reply — the western quadrant\'s thanks, kept.' },
    { op: 'giveItem', item: 'dawn_stamp', count: 1 },
    { op: 'setFlag', flag: 'flag:q_post_letter_nightreach' },
  ],

  // The strand cache (the variety rule: loose wicks off the lane).
  'script.pickup_dawnstead_cache': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'Tucked in the lee of the knoll, oilcloth-dry: a pouch of wicks, hidden before the dark came down and never needed after all.' },
    { op: 'giveMoney', amount: 400 },
    { op: 'say', text: 'Found 400 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_dawnstead_cache' },
  ],

  // ===========================================================================
  // THE STARFALL VIGILS (06-postgame · R3) — the endgame challenge chain. All
  // data: flags + warps + NPC/object swaps + EventTriggers + the trainer/item
  // entries above. The trials are sequential battle ops; a LOSS aborts the
  // script (engine convention), so EVERY grant/setFlag is authored AFTER the
  // battle — a blackout re-runs the trial from its trigger, never half-granting.
  // Keeper lines + readings are VERBATIM from the 06-postgame site sections.
  // Tone: post-dawn wonder; the dry glint holds ~1 in 6; Mer + the summit are
  // sincere throughout.
  // ===========================================================================

  // The opening — Watcher Oriel reads the first fall (Nightreach terrace).
  // Interact, requires flag:dawn, once:true. Sets flag:starfall_begun +
  // flag:vigil_reading_1 and speaks reading 1. Small and warm — wonder, not dread.
  'cutscene.starfall_begins': [
    // sfx, not musicSting: world-lantern-light is an SFX key — a sting would
    // resolve a music URL that doesn't exist and play silence (QA MINOR-1).
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'flashColor', color: '#ffe9a8', ms: 320 },
    { op: 'say', speaker: 'WATCHER ORIEL', text: 'All those years we watched the sky lose lights. Last night it GAVE one back — shed it, like a tree sheds a leaf it\'s finished with. The old watchers used to call them star-shards. The very old watchers used to call them invitations.' },
    { op: 'say', speaker: 'WATCHER ORIEL', text: 'I read where it fell. I\'d fetch it myself, but somebody promoted me, and now I\'m not allowed anywhere with weather.' },
    { op: 'setFlag', flag: 'flag:starfall_begun' },
    { op: 'setFlag', flag: 'flag:vigil_reading_1' },
    // Reading 1 — Hearthfall (south).
    { op: 'say', speaker: 'WATCHER ORIEL', text: 'The first came down in the south — where the first lamp learned its name. Climb past the lantern that taught the sky to answer; it fell on the bluff above, where even the gulls go quiet.' },
  ],

  // --- Vigil I — Hearthfall -------------------------------------------------
  // intro -> battle -> defeat -> grants (Starfall Shard + Radiant Charm) ->
  // flags (vigil_1_kept + vigil_reading_2). Esra reads reading 2 in the glint.
  'script.vigil_hearthfall': [
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'I dipped Brisa\'s first wick when she came up to my elbow, dear. She vouches for you. Wicks don\'t lie — but let\'s check.' },
    { op: 'battle', trainer: 'vigilant_esra' },
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'Steady as her best. Take the shard — and the charm; I pressed it for whoever finally came.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveItem', item: 'radiant_charm' },
    { op: 'setFlag', flag: 'flag:vigil_1_kept' },
    { op: 'setFlag', flag: 'flag:vigil_reading_2' },
    // Reading 2 — Grovefall (east).
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'There — see how it glints? It\'s already reading us the next. The second went to earth in the east — under the hill, where the wood keeps its own weather and the moss has opinions. Bring a light. Bring patience. The grotto has both, and shares neither.' },
  ],
  'script.vigil_hearthfall_again': [
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'Back for another, are we? Good. A flame wants checking now and then. Up you come.' },
    { op: 'battle', trainer: 'vigilant_esra' },
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'Steady as ever. Off you go, dear — and mind the gulls.' },
  ],

  // --- Vigil II — Grovefall (cave) ------------------------------------------
  'script.vigil_grovefall': [
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'Otho says you out-lasted him. Otho exaggerates. ...Show me he doesn\'t.' },
    { op: 'battle', trainer: 'vigilant_bramm' },
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'Hah. He doesn\'t. The deep way, walked all the way up. Take the chart — we never minted a Stone figure; turns out the sky did it for us.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveItem', item: 'chart_tremor_quake' },
    { op: 'setFlag', flag: 'flag:vigil_2_kept' },
    { op: 'setFlag', flag: 'flag:vigil_reading_3' },
    // Reading 3 — Stormfall (north).
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'The shard\'s already telling the next. The third went north, into the wind\'s spare pocket — the roost where storms go when they\'re off duty. Take the kite. Take a coat. Retrieve your own hat; I shan\'t fetch it.' },
  ],
  'script.vigil_grovefall_again': [
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'The grotto\'s grown another season since. Come and walk the deep way again — it keeps you honest.' },
    { op: 'battle', trainer: 'vigilant_bramm' },
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'Still lasting. The moss approves, and the moss is never wrong. Go on.' },
  ],

  // --- Vigil III — Stormfall ------------------------------------------------
  // The storm-tithe is the wick jackpot (giveMoney 5000); the cache by the nest
  // is the Starglass ×2 (the tithe's second half — placed in the map JSON).
  'script.vigil_stormfall': [
    { op: 'say', speaker: 'ONDRA VAEL', text: 'Mira flies in what I called a light breeze at her age. Stand up straight — the sky\'s sent us a present, and I open my own post.' },
    { op: 'battle', trainer: 'vigilant_ondra' },
    { op: 'say', speaker: 'ONDRA VAEL', text: 'HA! You\'d have made a kite-flier. The aerie\'s tithed every storm since the dawn broke — take it; I can\'t spend wind.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveMoney', amount: 5000 },
    { op: 'setFlag', flag: 'flag:vigil_3_kept' },
    { op: 'setFlag', flag: 'flag:vigil_reading_4' },
    // Reading 4 — Sunfall (west).
    { op: 'say', speaker: 'ONDRA VAEL', text: 'The shard\'s pointing already — west, it says. The fourth fell where summer was put away for safekeeping — the high terraces that remembered daylight before the rest of us believed in it again.' },
  ],
  'script.vigil_stormfall_again': [
    { op: 'say', speaker: 'ONDRA VAEL', text: 'Weather\'s up. Good weather for it. Stand up straight, then — same as before.' },
    { op: 'battle', trainer: 'vigilant_ondra' },
    { op: 'say', speaker: 'ONDRA VAEL', text: 'HA! Still a kite-flier in you. Off the ledge, mind your footing.' },
  ],

  // --- Vigil IV — Sunfall ---------------------------------------------------
  'script.vigil_sunfall': [
    { op: 'say', speaker: 'DAME SOLENNE', text: 'I kept the last warm day for forty years, and now the mornings come free. Indulge an old keeper — one encore, full light.' },
    { op: 'battle', trainer: 'vigilant_solenne' },
    { op: 'say', speaker: 'DAME SOLENNE', text: 'Curtain. ...Do you know, I don\'t mourn the last warm day any more. There will be others. Take the figure — it\'s the sun\'s whole bow.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveItem', item: 'chart_sunburst_nova' },
    { op: 'setFlag', flag: 'flag:vigil_4_kept' },
    { op: 'setFlag', flag: 'flag:vigil_reading_5' },
    // Reading 5 — Murkfall (the outer marches, the mirror axis).
    { op: 'say', speaker: 'DAME SOLENNE', text: 'One last reading in the glint, my dear, and it is a sad and lovely one. The last fell where the water forgot how to speak. It is learning again — go gently into the murk; some of what you\'ll meet is still waking. And one of them has waited a long time to greet you.' },
  ],
  'script.vigil_sunfall_again': [
    { op: 'say', speaker: 'DAME SOLENNE', text: 'An encore of the encore? You spoil an old keeper. Places, then — full light.' },
    { op: 'battle', trainer: 'vigilant_solenne' },
    { op: 'say', speaker: 'DAME SOLENNE', text: 'Curtain, again. The sun bows lower for you every time. Go on.' },
  ],

  // --- Vigil V — Murkfall ---------------------------------------------------
  // No reading 6 — Mer's pointer + Oriel's flag:vigil_5_kept placement carry the
  // player to the summit. Sincere throughout (no glint at the marshes).
  'script.vigil_murkfall': [
    { op: 'say', speaker: 'WARDEN MER', text: 'I carried a null-lantern through this marsh once. I carry this now. Before I hand the light back, I will know the hand I hand it to is steady.' },
    { op: 'battle', trainer: 'vigilant_mer' },
    { op: 'say', speaker: 'WARDEN MER', text: 'It holds. Brighter hands than mine ever were. ...The marsh thanks you. Both of us do — both of me, perhaps.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveItem', item: 'morrow_charm' },
    { op: 'setFlag', flag: 'flag:vigil_5_kept' },
    { op: 'say', speaker: 'WARDEN MER', text: 'The sixth never fell, you know. It\'s been waiting where the night ended. Carry the five up the mountain — and ask the old man what he sees.' },
  ],
  'script.vigil_murkfall_again': [
    { op: 'say', speaker: 'WARDEN MER', text: 'The marsh is brighter every time you come. I find I am too. One more steadiness, then?' },
    { op: 'battle', trainer: 'vigilant_mer' },
    { op: 'say', speaker: 'WARDEN MER', text: 'It holds. It always holds, with you. Go gently back.' },
  ],

  // --- The Vigil-site caches (one per annex; Stormfall's is the tithe's
  // second half — its site prize is the wick jackpot, not a chart) ----------
  'script.pickup_vigil_hearth_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Wedged in the bluff grass where the fall scattered it — a STARGLASS SHARD, still warm with morning.' },
    { op: 'setFlag', flag: 'flag:picked_vigil_hearth_glass' },
  ],
  'script.pickup_vigil_grove_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'The moss has grown a careful cradle around it in a single season — a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_vigil_grove_glass' },
  ],
  'script.pickup_vigil_storm_tithe': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 2 },
    { op: 'say', text: 'The aerie\'s tithe, lashed down against the wind — 2 STARGLASS SHARDS, fulgurite-bright!' },
    { op: 'setFlag', flag: 'flag:picked_vigil_storm_tithe' },
  ],
  'script.pickup_vigil_sun_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Caught in a cracked sun-basin, drinking the daylight — a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_vigil_sun_glass' },
  ],
  'script.pickup_vigil_murk_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Glowing softly in the shallow black water — a STARGLASS SHARD. The murk gives it up without a fight.' },
    { op: 'setFlag', flag: 'flag:picked_vigil_murk_glass' },
  ],

  // --- The Last Lesson — the summit Round (requires flag:vigil_5_kept) -------
  // Three Vigilants back-to-back -> heal (Fenn's diegetic line) -> Fenn at full
  // strength. A loss anywhere aborts before the flag, so the whole Round re-runs
  // from its trigger (the intended shape of the ultimate). On the win: the apex
  // gleam cadence seats the five shards and sets flag:starfall_lesson.
  'script.starfall_round': [
    { op: 'narrate', text: 'At the foot of the empty Ninth Lantern — five sockets, five shards in your satchel — three figures wait, lamps lit, who have no business being this high and every right to be.' },
    { op: 'say', speaker: 'ONDRA VAEL', text: 'We came to watch the old man\'s lesson. The watching turned into a queue.' },
    { op: 'battle', trainer: 'vigilant_ondra_summit' },
    { op: 'battle', trainer: 'vigilant_solenne_summit' },
    { op: 'battle', trainer: 'vigilant_mer_summit' },
    { op: 'heal' },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'I\'ll want you at your best. I have waited a very long time to be allowed mine.' },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'No satchel this time. No errand. One lesson left, and it\'s the one I never could teach you — what you do when the teacher steps aside. Everything I have, apprentice. Show me everything you\'ve become.' },
    { op: 'battle', trainer: 'startender_fenn' },
    // WIN — everything below is post-battle (a loss aborted the script already).
    { op: 'say', speaker: 'STAR-TENDER FENN', text: '...There it is. The whole sky in one steady lamp.' },
    // The shards seated — the apex gleam cadence (the Keystar relight's quieter sibling).
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'silence', ms: 2200 },
    { op: 'narrate', text: 'You lift the five shards to the Ninth Lantern\'s empty collar, one to each cold socket. They settle as if they were always going to — gold finding gold, the sky remembering one more of its own pieces.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.28, ms: 1200 },
    { op: 'gleam', element: 'solar' },
    { op: 'setFlag', flag: 'flag:starfall_lesson' },
    { op: 'narrate', text: 'The collar takes the light and holds it — and far below the rim of the world, where the night ended, the sixth shard answers. It never fell. It could not. It is the morning itself.' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 1200 },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1100 },
    { op: 'letterbox', on: false, ms: 420 },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'There. Five seated, and the sixth come of its own accord. ...Go to the lantern, apprentice. Something is waking that has waited longer than any of us.' },
  ],
  // Post-crown re-runnable Last Lesson (the bout only, full payout).
  'script.last_lesson_again': [
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'One more, apprentice? The old man will always have one more. Everything I have — again.' },
    { op: 'battle', trainer: 'startender_fenn' },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: '...Still the whole sky in one steady lamp. Go on, Star-tender. I\'ll be here.' },
  ],

  // --- Dawnbrael wakes — the first-morning kin (the static catch) ------------
  // requires flag:starfall_lesson (so a fled/KO\'d Dawnbrael is re-approachable
  // WITHOUT re-fighting the Round); cooldownBattles 0 so the climax never
  // strands (raise the lamp and ask again). The trigger also carries
  // hidden_when_flag:flag:dawnbrael_caught so a caught Dawnbrael never re-stages.
  'cutscene.dawnbrael_wakes': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'narrate', text: 'The relit Ninth Lantern pours its new light down the shaft — and in the heart of it, the morning takes a shape. DAWNBRAEL: the first-morning kin, Solar and Light, regarding your lamp the way the sunrise regards a window.' },
    { op: 'flashColor', color: '#fff3c9', ms: 280 },
    { op: 'letterbox', on: false, ms: 300 },
    { op: 'legendaryBattle', name: 'dawnbrael', kin: 151, level: 70, caughtFlag: 'flag:dawnbrael_caught', cooldownBattles: 0, cooldownRef: 'npc.dawnbrael_resting' },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'Dawnbrael settles into your lamp — and the lamp, for the first time, is warmer than the morning around it.' },
  ],

  // --- The title beat — Fenn names the Star-tender (once:true) ---------------
  // After the Dawnbrael catch. Grants Fenn\'s Field-Glass, sets flag:starfall_crown.
  // Staging rhymes with the satchel ceremony — the game\'s first gift and its last.
  'cutscene.startender_named': [
    { op: 'silence', ms: 1400 },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'I have nothing left to teach. Stand up straight, Star-tender — the title was always going to be yours. I\'m only the one saying it out loud.' },
    { op: 'tint', color: '#ffe9a8', alpha: 0.18, ms: 900 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'giveItem', item: 'fenns_glass' },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'Take the field-glass. Forty years it showed me the sky. You\'ll see further than I did — that\'s the whole of the job, in the end: hand it on to someone who sees further.' },
    { op: 'setFlag', flag: 'flag:starfall_crown' },
    { op: 'narrate', text: 'The apprentice who began with a satchel errand at a waystone ends a Star-tender, named by the man who sent them out — under an open summit sky, with the morning on every lamp.' },
    { op: 'tint', color: '#ffe9a8', alpha: 0, ms: 1100 },
  ],
};

export function getScript(ref: string): import('./types').CutsceneStep[] | undefined {
  return SCRIPTS[ref];
}
