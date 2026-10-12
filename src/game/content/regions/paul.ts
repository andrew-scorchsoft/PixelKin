/**
 * PAUL'S HOUSE (2026-10) — the Booji-Wooji Man's crooked three-storey home on
 * Wayward Rise, beside the Wayward Arms (`paul_house_1/2/3`; builders
 * tools/maps/build_paul_house.py + the exterior in build_wayward_rise.py; art
 * tools/maps/paulforge.py + the generated `paul_house`/`paul_bike`/`paul_washing_line`).
 *
 * Who he is (S4/S5, content/scripts.ts): the quiet wanderer at the dark lamp on
 * the breakwater, who walks the old wood and is never lost. The house is all the
 * evidence and none of it agrees: a lifetime between the maple country across
 * the northern sea and the cape country far to the south, t-shirts from
 * everywhere (each with a story), the bike he rides down to the Lifting House,
 * a WANTED poster from "a far-off bureau" he swears is a joke. Paul is NEVER home
 * — he's out walking; a note on the kitchen table says so. The Registry story
 * stays unconfirmed. NOBODY here says what the Booji-Wooji Man is.
 *
 * The heart of it is LOTTIE, his granddaughter, in the attic. The Rise is only
 * reachable after the waystone's word (S5), which itself needs the Chickenpig —
 * so in play she always meets you AFTER `flag:chickenpig_caught`. The tiny
 * "before" branch is a safety net for odd saves and gives nothing away (she
 * likes chickens, and pigs, separately). AFTER: her walls are covered in
 * Chickenpig drawings, she has a plush, she shrieks — and if your Chickenpig is
 * in your lamp it comes out to meet her (`setLead` puts it in front; a `travel`
 * re-entry onto the same tile spawns the visitor NPC `lottie_cp`, gated on
 * `flag:paul_lottie_cp_out`, which the scene clears again). First meeting: a
 * dance and a keepsake (LOTTIE'S DRAWING). Repeat visits: short and happy.
 *
 * Staging tiles (paul_house_3): Lottie (5,5); the visitor appears at (6,6); the
 * player re-enters at (4,6) facing right. Never progression: nothing here gates.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const CP = 'flag:chickenpig_caught';
const SCENE = 'flag:paul_lottie_scene'; // the first after-catch shriek has happened
const MET = 'flag:paul_lottie_cp_met'; // the Chickenpig has met her (gift given)
const OUT = 'flag:paul_lottie_cp_out'; // the visitor NPC is in the room
const L = 'LOTTIE';

/** Out of the lamp: the Chickenpig steps in front, the room re-enters with it in it. */
const LET_IT_OUT: CutsceneStep[] = [
  { op: 'setLead', kin: 163, missingRef: 'npc.paul_lottie_cp_missing' },
  { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 600 },
  { op: 'sfx', key: 'world-lantern-light' },
  { op: 'setFlag', flag: OUT },
  { op: 'travel', map: 'paul_house_3', to: { tx: 4, ty: 6 }, facing: 'right' },
  { op: 'face', actor: 'lottie', facing: 'down' },
  { op: 'sfx', key: 'cry-163' },
  { op: 'hop', actor: 'lottie_cp', times: 2 },
];

/** Back into the lamp (the visitor leaves when the scene ends and the flag is re-read). */
const BACK_IN: CutsceneStep[] = [
  { op: 'sfx', key: 'world-lantern-light' },
  { op: 'hideActor', actor: 'lottie_cp' },
  { op: 'setFlag', flag: OUT, value: false },
];

export const PAUL_SCRIPTS: ScriptRegistry = {
  // ---- the house ------------------------------------------------------------------------
  'script.paul_house_welcome': [
    { op: 'narrate', text: 'The door isn\'t locked. It doesn\'t look as if it has ever been locked. It doesn\'t look as if it has ever been entirely SHUT.' },
    { op: 'narrate', text: 'Inside, every wall is busy: tickets, paintings, carvings, a kettle still warm on the bench. Somewhere upstairs, someone small is singing to herself.' },
    { op: 'setFlag', flag: 'flag:paul_house_seen' },
  ],
  // The note on the kitchen table. Paul is never home.
  'script.paul_note': [
    { op: 'narrate', text: 'A note, propped against the candle in big loopy capitals:' },
    { op: 'narrate', unless_flag: 'flag:q_south_wander_done', text: '"GONE WALKING. UP THE OLD WOOD. BACK WHEN I\'M BACK. KETTLE\'S YOURS. DON\'T TOUCH THE SHIRTS. — p."' },
    { op: 'narrate', if_flag: 'flag:q_south_wander_done', text: '"GONE TO KEEP THE DARK COMPANY. LOTTIE\'S UPSTAIRS — SHE\'LL SHOW YOU EVERYTHING WHETHER YOU LIKE IT OR NOT. KETTLE\'S YOURS. — p."' },
    { op: 'narrate', text: 'Under it, in different ink: "P.S. if anyone from a bureau asks, I am a retired cheese-bun inspector!!!!!!"' },
  ],
  // The museum placard at the top of the stairs (once).
  'script.paul_museum': [
    { op: 'narrate', text: 'A hand-lettered placard at the top of the stairs:' },
    { op: 'narrate', text: 'THE MUSEUM OF T-SHIRTS. ADMISSION: ONE STORY. PLEASE DO NOT TOUCH THE EXHIBITS. (LOTTIE MAY TOUCH THE EXHIBITS.)' },
    { op: 'setFlag', flag: 'flag:paul_museum_seen' },
  ],

  // ---- Lottie ---------------------------------------------------------------------------
  // Exactly one branch: the return visit FIRST, so the first scene (which sets
  // SCENE at its end) never falls through into it.
  'script.paul_lottie': [
    { op: 'run', ref: 'script.paul_lottie_again', if_flag: SCENE },
    { op: 'run', ref: 'script.paul_lottie_first', if_flag: CP, unless_flag: SCENE },
    { op: 'run', ref: 'script.paul_lottie_before', unless_flag: CP },
  ],

  // The safety-net "before" (unreachable in normal play): a cheerful kid, no hints.
  'script.paul_lottie_before': [
    { op: 'face', actor: 'lottie', facing: 'down' },
    { op: 'say', speaker: L, text: 'Hello! Are you here for Grandad? He\'s out walking. He\'s ALWAYS out walking. He says he\'s not lost, he\'s just somewhere else on purpose.' },
    { op: 'say', speaker: L, text: 'Did you see his shirts? He\'s got one from EVERYWHERE. He says if you don\'t come home with a shirt, you weren\'t really there.' },
    { op: 'say', speaker: L, text: 'I like chickens. And pigs. Separately. Normal amounts.' },
  ],

  // THE SCENE — the first visit after the Chickenpig is caught.
  'script.paul_lottie_first': [
    { op: 'face', actor: 'lottie', facing: 'down' },
    { op: 'say', speaker: L, text: 'Hello! Are you here for Grandad? He\'s out walking, he\'s always out walk—' },
    { op: 'emote', actor: 'lottie', emote: 'alert', holdMs: 700 },
    { op: 'narrate', text: 'She stops. She is looking at your sleeve. Stuck to it is one long, curling, emerald-green tail-feather.' },
    { op: 'say', speaker: L, text: '...Where did you get that.' },
    { op: 'shakeActor', actor: 'lottie', ms: 500, px: 1 },
    { op: 'say', speaker: L, text: 'That\'s a SICKLE feather. That\'s a CHICKENPIG sickle feather. Grandad TOLD me about it — the bird that\'s a pig, the pig that\'s a bird, the only one that still crows for the morning —' },
    { op: 'say', speaker: L, text: '— and NOBODY at school believed me, and Grandad said "believe what you like, Lots, the morning\'s on its way regardless" —' },
    { op: 'say', speaker: L, text: 'HAVE YOU GOT A CHICKENPIG IN THERE?!' },
    { op: 'emote', actor: 'player', emote: 'sweat' },
    { op: 'narrate', text: 'From your vesperlamp comes a small, smug sound: half crow, half oink.' },
    { op: 'shake', ms: 450, intensity: 0.004 },
    { op: 'say', speaker: L, text: 'EEEEEEEEEEEEEEEEEE!!!' },
    { op: 'hop', actor: 'lottie', times: 3, height: 6 },
    { op: 'emote', actor: 'lottie', emote: 'heart', holdMs: 900 },
    { op: 'narrate', text: 'Somewhere far below, a kettle rattles on its hob in sympathy.' },
    { op: 'say', speaker: L, text: 'Look! LOOK! I drew it! Before I\'d even SEEN one! I drew it ninety times! That\'s not true. I drew it four times. They\'re the best four.' },
    { op: 'cameraFocus', to: { tx: 7, ty: 2 }, ms: 700 },
    { op: 'narrate', text: 'Crayon Chickenpigs cover the wall: under a sun, in a cloud of hearts, holding a little girl\'s hand, and one under a rainbow that is MUCH too big.' },
    { op: 'cameraFocus', to: { tx: 7, ty: 7 }, ms: 600 },
    { op: 'say', speaker: L, text: 'And that\'s Sir Oinksalot. Grandad sewed him. His comb fell off twice. He\'s very brave about it.' },
    { op: 'cameraReset', ms: 500 },
    { op: 'say', speaker: L, text: 'Can I meet it? Please? PLEASE? I\'ll be so gentle. I\'ll be the gentlest anyone\'s EVER been. Look, I\'m being gentle right now.' },
    { op: 'shakeActor', actor: 'lottie', ms: 400, px: 1 },
    { op: 'narrate', text: 'She is vibrating.' },
    { op: 'setFlag', flag: SCENE },
    {
      op: 'choice',
      prompt: 'Let the Chickenpig out to meet Lottie?',
      options: [
        { label: 'LET IT OUT', ops: [{ op: 'run', ref: 'script.paul_lottie_meet' }] },
        {
          label: 'NOT RIGHT NOW',
          ops: [
            { op: 'say', speaker: L, text: 'That\'s okay. It\'s probably asleep. Chickenpigs need eleventy hours of sleep. I read that. I wrote it, actually. But I READ it after.' },
            { op: 'say', speaker: L, text: 'Come back when it\'s awake! I\'ll be here. I am VERY good at waiting.' },
            { op: 'narrate', text: 'She is not very good at waiting.' },
          ],
        },
      ],
    },
  ],

  // The meeting, the dance, the keepsake (once).
  'script.paul_lottie_meet': [
    ...LET_IT_OUT,
    { op: 'narrate', text: 'You lift your vesperlamp. The Chickenpig decides, entirely on its own, that this is its moment — and steps out into the attic like it owns the place.' },
    { op: 'emote', actor: 'lottie', emote: 'alert' },
    { op: 'say', speaker: L, text: '...' },
    { op: 'say', speaker: L, text: '...it\'s REAL.' },
    { op: 'face', actor: 'lottie_cp', facing: 'up' },
    { op: 'sfx', key: 'cry-163' },
    { op: 'narrate', text: 'The Chickenpig looks Lottie up and down, ruffles its one red wing, and CROWS at her.' },
    { op: 'say', speaker: L, text: 'It crowed at ME! It crowed AT ME! Grandad, it — oh, he\'s not here. Wait till I TELL him. He\'ll pretend he isn\'t impressed. He\'ll be SO impressed.' },
    { op: 'hop', actor: 'lottie', times: 2, height: 5 },
    { op: 'emote', actor: 'lottie', emote: 'heart' },
    { op: 'emote', actor: 'lottie_cp', emote: 'heart' },
    { op: 'say', speaker: L, text: 'Hello. Hello, Chickenpig. I\'m Lottie. I\'m seven and three-quarters. I have drawn you four times and I am going to draw you a HUNDRED.' },
    { op: 'narrate', text: 'The Chickenpig considers this offer gravely, and oinks once. It is clearly a yes.' },
    { op: 'say', speaker: L, text: 'Do you dance? Grandad says everybody dances, some people just haven\'t found out yet.' },
    { op: 'music', key: 'pearlmoor-blessing' },
    { op: 'spin', actor: 'lottie', turns: 2, ms: 120 },
    { op: 'hop', actor: 'lottie_cp', times: 2 },
    { op: 'spin', actor: 'lottie_cp', turns: 2, ms: 120 },
    { op: 'hop', actor: 'lottie', times: 2 },
    { op: 'emote', actor: 'lottie', emote: 'music' },
    { op: 'emote', actor: 'lottie_cp', emote: 'music' },
    { op: 'spin', actor: 'lottie', turns: 3, ms: 100 },
    { op: 'spin', actor: 'lottie_cp', turns: 3, ms: 100 },
    { op: 'narrate', text: 'What follows can only be described as a dance. Lottie does a sort of hop-hop-twirl. The Chickenpig does a sort of hop-hop-oink. Neither of them leads. Both of them win.' },
    { op: 'action', actor: 'player', action: 'laugh', holdMs: 900 },
    { op: 'sfx', key: 'cry-163' },
    { op: 'hop', actor: 'lottie_cp', times: 3, height: 6 },
    { op: 'narrate', text: 'At the big finish it crows and oinks at the SAME TIME — which should not be possible, and which Lottie will be describing to everyone she meets for the rest of her life.' },
    { op: 'shakeActor', actor: 'lottie', ms: 600, px: 1 },
    { op: 'say', speaker: L, text: 'BEST. DAY. EVER.' },
    { op: 'musicFade', ms: 900 },
    { op: 'face', actor: 'lottie', facing: 'left' },
    { op: 'say', speaker: L, text: 'I made you something. Well — I made it for the Chickenpig, but it can\'t hold things, it\'s got a wing and a trotter, so you have to carry it.' },
    { op: 'say', speaker: L, text: 'It\'s the best one. Don\'t look at the ones on the wall, they\'re worse. (They\'re not worse. They\'re all the best.)' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'lottie_drawing', count: 1 },
    { op: 'say', text: 'Lottie hands you a crayon drawing, slightly crumpled from being held very tightly. Received LOTTIE\'S DRAWING!' },
    { op: 'say', speaker: L, text: 'Keep it somewhere it can see the sky. That\'s what Grandad says about everything.' },
    { op: 'setFlag', flag: MET },
    { op: 'narrate', text: 'The Chickenpig gives Lottie one last appraising look, oinks something that sounds a lot like "see you", and hops back into your lamp\'s light.' },
    ...BACK_IN,
    { op: 'emote', actor: 'lottie', emote: 'heart' },
    { op: 'narrate', text: '(The Chickenpig has decided it is leading your party now. It will not be argued with. You can move it in KIN — if you dare.)' },
    { op: 'music', key: 'interior-sunny' },
  ],

  // Return visits: short and happy, and the Chickenpig can come out again any time.
  'script.paul_lottie_again': [
    { op: 'face', actor: 'lottie', facing: 'down' },
    { op: 'emote', actor: 'lottie', emote: 'heart' },
    { op: 'say', speaker: L, if_flag: MET, text: 'You\'re BACK! Is it in there? Is it awake? Can I say hello? HELLO, CHICKENPIG!' },
    { op: 'say', speaker: L, unless_flag: MET, text: 'You came back! Is it awake now? Can I meet it? I\'ve been waiting. Not very well.' },
    {
      op: 'choice',
      prompt: 'Let the Chickenpig out?',
      options: [
        { label: 'LET IT OUT', unless_flag: MET, ops: [{ op: 'run', ref: 'script.paul_lottie_meet' }] },
        { label: 'LET IT OUT', if_flag: MET, ops: [{ op: 'run', ref: 'script.paul_lottie_visit' }] },
        {
          label: 'JUST VISITING',
          ops: [
            { op: 'say', speaker: L, text: 'Grandad\'s still out walking. He came back for ONE cup of tea and then went out again. He said the hill was "making eyes at him".' },
          ],
        },
      ],
    },
  ],
  'script.paul_lottie_visit': [
    ...LET_IT_OUT,
    { op: 'say', speaker: L, text: 'HELLO! Hello hello hello. I drew you again. You\'re on the front door now. Grandad says that\'s the first thing visitors see. Grandad is RIGHT.' },
    { op: 'sfx', key: 'cry-163' },
    { op: 'spin', actor: 'lottie', turns: 2, ms: 120 },
    { op: 'spin', actor: 'lottie_cp', turns: 2, ms: 120 },
    { op: 'emote', actor: 'lottie', emote: 'music' },
    { op: 'emote', actor: 'lottie_cp', emote: 'heart' },
    { op: 'narrate', text: 'One quick hop-hop-twirl, one quick hop-hop-oink. A shorter dance, but no less sincere.' },
    { op: 'say', speaker: L, text: 'Okay. Okay. You can go back in. I\'ll see you next time. I\'ll draw you NINETY times by then.' },
    ...BACK_IN,
  ],
};

export const PAUL_DIALOGUE: DialogueRegistry = {
  // Setlead's missing line: the Chickenpig's resting at the Hearth (or too tired to stand).
  'npc.paul_lottie_cp_missing': [
    { speaker: 'LOTTIE', text: 'It\'s... not in your lamp? Is it resting at the HEARTH?' },
    { speaker: 'LOTTIE', text: 'That\'s okay. Bring it next time — awake and ready. I\'ll wait right here. I am VERY good at waiting. (I\'m not.)' },
  ],

  // ---- outside -----------------------------------------------------------------------------
  'sign.paul_bike': [
    { text: 'A sturdy old bicycle with a wicker basket, leaning on its stand by the door. A gym towel is rolled up in the basket; the saddle is worn shiny.' },
    { text: 'Every morning, they say, he rides it down the hill and round the quay to the Lifting House — and walks it back up, because hills, he says, are for thinking.' },
  ],
  'sign.paul_washing_line': [
    { text: 'T-shirts drying on the line: red, mustard, teal, a white one with a red leaf, a hooped green-and-gold.' },
    { text: 'Why own one shirt, when you could own a story?' },
  ],

  // ---- ground floor ------------------------------------------------------------------------
  'sign.paul_wanted': [
    { text: 'A poster, yellowed at the corners. WANTED — by a bureau so far off nobody can pronounce it — FOR EXCESSIVE CHARM.' },
    { text: 'Underneath, in pencil: "& crimes against fashion." Pinned beside it, in Paul\'s hand: "it\'s a joke. — p."' },
    { text: 'The story on the back has been crossed out and rewritten four times. Every version is different. Every version is signed.' },
  ],
  'sign.paul_pinboard': [
    { text: 'Tickets. Ferry stubs, rail stubs, a lift-pass from a mountain you\'ve never heard of. A postcard of a frozen lake from the maple country across the northern sea; another of a flat-topped mountain from the cape country far to the south.' },
    { text: 'Every one of them is stamped. Some are stamped twice — going the other way.' },
  ],
  'sign.paul_cape_day': [
    { text: 'A sunny painting: a great flat-topped mountain above a blue bay, a white cloud poured over its top like a tablecloth. The cape country, far to the south.' },
    { text: 'On the frame, in pencil: "home, the first time."' },
  ],
  'sign.paul_tea': [
    { text: 'A dented kettle, still warm, two mugs, and a red tin of red-bush tea from the cape country, half full.' },
    { text: 'A note taped to the lid: "NOT for guests. (Fine. For guests.) — p."' },
  ],
  'sign.paul_antelope': [
    { text: 'A carved wooden antelope with long corkscrew horns, worn smooth by hands. A tag round its neck:' },
    { text: '"from the cape country. it watches the door. it is very bad at it."' },
  ],
  'sign.paul_gym_kit': [
    { text: 'A battered bike helmet sitting on top of a gym bag. The bag smells of chalk and harbour-stone.' },
    { text: 'A tag: PROPERTY OF THE LIFTING HOUSE — RETURN IF FOUND. And under it, in Paul\'s hand: "never found. always going."' },
  ],
  'sign.paul_trunk': [
    { text: 'A travel trunk plastered with stickers — so many that the trunk underneath is mostly a rumour.' },
  ],
  'sign.paul_chair': [
    { text: 'Paul\'s chair, angled at the fire. The cushion has long since given up and become the exact shape of one man.' },
  ],

  // ---- the T-shirt museum ------------------------------------------------------------------
  'sign.paul_shirt_race': [
    { text: 'A red race shirt, the number still pinned on. The card reads:' },
    { text: '"the race i didn\'t finish. stopped at mile nine to help a fella fix his bike. we finished his bike. great day."' },
  ],
  'sign.paul_shirt_sun': [
    { text: 'Mustard yellow, with a little sun on it. The card reads:' },
    { text: '"from a summer before the dusk, when it barely got dark at all. there was one, you know. ask anyone old. ask me."' },
  ],
  'sign.paul_shirt_ferry': [
    { text: 'Teal, with a wave across the chest. The card reads:' },
    { text: '"swapped a stranger for it on a ferry. he got my good shirt. i got this one and his whole life story. i won."' },
  ],
  'sign.paul_shirt_leaf': [
    { text: 'White, with a big red leaf. The card reads:' },
    { text: '"the maple country, across the northern sea. snow to your knees, and everyone says sorry to you about the weather like it\'s their fault."' },
  ],
  'sign.paul_shirt_gym': [
    { text: 'Navy, with a white dumbbell. The card reads:' },
    { text: '"the lifting house, year one. andy said i should frame it. so i did. andy said that\'s not what he meant."' },
  ],
  'sign.paul_shirt_stripe': [
    { text: 'A hooped green-and-gold jersey, mud still in the collar. The card reads:' },
    { text: '"the cape country, far to the south. played one match. lost one tooth. would do again."' },
  ],
  'sign.paul_shirt_boat': [
    { text: 'Orange, with a little white sail. The card reads:' },
    { text: '"learned to sail. un-learned to sail. learned to swim."' },
  ],
  'sign.paul_shirt_star': [
    { text: 'Purple, with a gold star. The card reads:' },
    { text: '"from a festival nobody else remembers. i remember it. it was excellent."' },
  ],
  'sign.paul_lake': [
    { text: 'A painting of a frozen lake under the stars, dark pines along the shore — the maple country, across the northern sea.' },
    { text: 'In the corner, in tiny letters: "cold enough to freeze a word in the air. i said a lot of them."' },
  ],
  'sign.paul_antlers': [
    { text: 'An enormous spread of antlers on a wooden shield. The card reads:' },
    { text: '"did NOT shoot this. found it. carried it eleven miles. regret nothing."' },
  ],
  'sign.paul_paddle': [
    { text: 'A canoe paddle, its blade painted red and cream. The card reads:' },
    { text: '"from a lake in the maple country. the canoe is still out there. probably upside down."' },
  ],
  'sign.paul_rack': [
    { text: 'A rail of t-shirts: every colour, every size, every one of them his. Some name places. Some name things that don\'t make sense anymore. One just says NO.' },
  ],
  'sign.paul_rack_b': [
    { text: 'More shirts. A card on the rail says OVERFLOW. Another card under it says OVERFLOW OVERFLOW.' },
  ],
  'sign.paul_folded': [
    { text: 'Folded shirts under the candle, too precious to hang: the very first one, one with a hole shaped like a coastline, and one signed by an entire ferry crew.' },
  ],
  'sign.paul_protea': [
    { text: 'A painting of a great pink flower, all spiky crown and soft heart — the cape country\'s own. The card reads:' },
    { text: '"looks fierce. isn\'t. like most things worth knowing."' },
  ],
  'sign.paul_beadwork': [
    { text: 'A panel of tiny glass beads in bright diamonds, hung from a little rod, from the cape country. The card reads:' },
    { text: '"took her a whole winter. she gave it me for helping carry a stove up four flights. i still owe her."' },
  ],
  'sign.paul_sunset': [
    { text: 'A sunset over the flat-topped mountain: pink sky, purple rock, a gold road laid across the sea.' },
    { text: 'On the frame: "home, the last time." Crossed out. "the latest time." Crossed out. "never the last time."' },
  ],
  'sign.paul_rugby': [
    { text: 'An oval leather ball on a little wooden kicking-tee, scuffed from years of use. The card reads:' },
    { text: '"it bounces wrong on purpose. so do i."' },
  ],
  'sign.paul_trunk_stickers': [
    { text: 'Another trunk. This one is labelled MORE STICKERS. It is full of more stickers.' },
  ],
  'sign.paul_globe': [
    { text: 'A little globe on a brass stand. Someone has drawn a dotted pencil line round and round it, until the line simply became the globe.' },
  ],
  'sign.paul_plaid': [
    { text: 'A red-and-black checked lumber-jacket from the maple country, and a bobble hat on the peg above it.' },
    { text: 'The hat is Lottie\'s size. The jacket is not. She wears it anyway.' },
  ],
  'sign.paul_syrup': [
    { text: 'A tin of maple syrup with a red-leaf label, beside a tin mug. The tin is empty.' },
    { text: 'Paul keeps it anyway. The smell, he says, is the souvenir.' },
  ],

  // ---- Lottie's attic ----------------------------------------------------------------------
  'sign.paul_drawing_bike': [
    { text: 'A crayon drawing: a stick-man on a bicycle, going VERY fast (there are speed lines). Labelled: GRANDAD GOING TO THE JIM.' },
  ],
  'sign.paul_drawing_sea': [
    { text: 'A crayon drawing of the quay: a boat, the sea, and one tall lamp coloured all in black. Labelled: GRANDAD\'S LAMP. IT\'S DARK ON PURPOSE.' },
  ],
  'sign.paul_cp_drawing_a': [
    { text: 'A crayon Chickenpig under a crayon sun. Labelled: CHICKENPIG. MORNING. (SAME THING.)' },
  ],
  'sign.paul_cp_drawing_b': [
    { text: 'A crayon Chickenpig in a cloud of hearts. So many hearts. One of the hearts has a heart in it.' },
  ],
  'sign.paul_cp_drawing_c': [
    { text: 'Lottie and the Chickenpig, holding hands. Well — hand and wing. Labelled: BEST FRENDS (OFISHUL).' },
  ],
  'sign.paul_cp_drawing_d': [
    { text: 'A rainbow over an extremely large Chickenpig. Labelled: THE BIGGEST ONE. And then, smaller: it is probly not that big in real life.' },
  ],
  'sign.paul_plush': [
    { text: 'A Chickenpig plush, lumpy and much-loved. Its comb has been sewn back on twice, in two different reds.' },
    { text: 'It has button eyes and an expression of total confidence. A label on its foot: SIR OINKSALOT.' },
  ],
  'sign.paul_lottie_bed': [
    { text: 'Lottie\'s bed. A crayon sign on the pillow: NO GROWN-UPS. (EXCEPT GRANDAD.) (EXCEPT YOU, MAYBE.)' },
  ],
  'sign.paul_lottie_desk': [
    { text: 'Crayons, all worn down to stubs — except the black one, which has hardly been touched. Grandad\'s lamp, presumably, gets drawn very carefully.' },
  ],
  'sign.paul_lottie_toys': [
    { text: 'A stack of toy crates: a wooden boat, a kite with no string, three spinning tops, and a little bicycle bell.' },
  ],
};
