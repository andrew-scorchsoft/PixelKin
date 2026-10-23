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
 * in your lamp it comes out to meet her (`setLead` puts it in front, undone at scene end; a `travel`
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

/**
 * THE THREE RAILS (2026-10). Every shirt Paul owns is OUT (safe to be seen in),
 * IN (house only) or NEVER (not to be worn at all, roped off). Each rail is a
 * "hold one up" menu, so it rewards coming back; looking through all three
 * turns up a note in the last pocket (once).
 */
const RAIL_FLAGS = ['flag:paul_rail_out', 'flag:paul_rail_in', 'flag:paul_rail_never'];
const shirtPick = (label: string, ...lines: string[]) => ({
  label,
  ops: lines.map((text): CutsceneStep => ({ op: 'narrate', text })),
});
const railMenu = (seen: string, shirts: ReturnType<typeof shirtPick>[]): CutsceneStep[] => [
  { op: 'setFlag', flag: seen },
  { op: 'choice', prompt: 'Hold one up?', options: [...shirts, { label: 'Leave them', ops: [] }] },
  { op: 'run', ref: 'script.paul_rails_all' },
];

/**
 * THE FESTIVAL OF THE IMAGINED (2026-10, after Paul's own booklet). A programme
 * you page through on the museum lectern: imagined people from Vesperholm's
 * old tales meet "in conversation". Every name is ORIGINAL (VISION.md); the
 * last page asks who YOU would invite, as a typed answer that is never stored.
 */
const FEST_PAGES: string[][] = [
  [
    'A hand-printed programme. The cover is all loud red-and-black circus letters over a jumble of half-words in soft colours:',
    'FESTIVAL OF THE IMAGINED.',
  ],
  [
    'WELCOME to the first Festival of the Imagined, to be held on the twenty-ninth of the short month — a day that only turns up one winter in four, so we thought it could spare us an evening.',
    'There will be people in conversation, pictures on the walls, and a night of lantern-shows. This is only the first, so we have not tried to do everything. We hope you leave imagining what might come next.',
  ],
  [
    'THE LAMPLIGHTER\'S DAUGHTER AND THE GIRL WHO FELL UP THE WELL, IN CONVERSATION.',
    'They have written to each other for years but never met. Both grew up to be nursery stories and both went to great lengths to live quietly anyway. They will talk about growing older, the end of childhood, and whether you can lose the knack of imagining. (You can\'t. Probably.)',
  ],
  [
    'THE LONG-ROAD DRIFTER AND THE MAN WHO WALKED OUT OF THE MAP, IN CONVERSATION.',
    'Two men who have wandered every dust road, crossroads inn and shuttered car-station in the old songs. They will talk about wanting things, being afraid of things, and the strange comfort of the road. Drinks will be served. It will go late.',
  ],
  [
    'THE SORTING-OFFICE POET AND THE WOMAN WHO HEARD THE POST-HORN, IN CONVERSATION.',
    'A pair of outsiders: one sorts letters by night and writes on the backs of them; one keeps finding a muffled horn drawn in the margins of everything. Topics: how to live in a world that has stopped making sense. They have asked for a dance floor, and intend to use it.',
  ],
  [
    'THREE ARTISTS IN CONVERSATION: ART?',
    'A painter who sleeps under his own canvases, a sculptor of hanging things, and an old woman who has drawn the same harbour every morning for sixty years.',
    'They have asked to begin from one word, sent in by post with no name on it: DESASOSIEGO. The itch that won\'t let you sit still until you\'ve made something. Should be quite an evening.',
  ],
  [
    'TICKETS. There is no charge. Write to us and tell us your name, and why you want to come. One event each — if you and a friend want the same evening, you each write your own letter. Your ticket will come back by return of post.',
  ],
];

/** One page: its text, then turn on or close (a choice so a reader can stop any time). */
const festPage = (i: number): CutsceneStep[] => [
  ...FEST_PAGES[i].map((text): CutsceneStep => ({ op: 'narrate', text })),
  {
    op: 'choice',
    options: [
      { label: 'Turn the page', ops: [{ op: 'run', ref: i + 1 < FEST_PAGES.length ? `script.paul_festival_${i + 1}` : 'script.paul_festival_last' }] },
      { label: 'Close it', ops: [] },
    ],
  },
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
  // ---- Rose --------------------------------------------------------------------------
  // Paul's daughter, minding the kettle in the kitchen (paul_house_1). Exactly one
  // story-stage line plays (before the bird-pig / after it / after the cup), then
  // the standing patter. Warm; she never says what her dad IS either.
  'script.paul_rose': [
    { op: 'face', actor: 'rose', facing: 'down' },
    { op: 'say', unless_flag: 'flag:paul_rose_met', speaker: 'ROSE', text: 'Oh! Hello. You\'ll be another of Dad\'s strays. I\'m Rose. He\'s out walking. He\'s always out walking.' },
    { op: 'say', if_flag: 'flag:paul_rose_met', speaker: 'ROSE', text: 'Back again? Kettle\'s on. It\'s always on. Dad says a cold kettle is how a house forgets you.' },
    { op: 'say', unless_flag: CP, speaker: 'ROSE', text: 'Lottie\'s up in the attic, drawing chickens. And pigs. She keeps asking me which one would win. I keep saying "a nap".' },
    { op: 'say', if_flag: CP, unless_flag: 'flag:q_south_wander_done', speaker: 'ROSE', text: 'Is that a FEATHER on your sleeve? Green, curly... Oh, Lottie is going to lose her mind. Go on up. I\'ll stay here and hold the teapot steady.' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'ROSE', text: 'He came home with a tin cup and a grin and won\'t say where he got either. Whatever you did up that wood, thank you. He\'s been humming.' },
    { op: 'say', speaker: 'ROSE', text: 'If you go up to his shirts: the NEVER rail is mine and Lottie\'s doing. He wore ASK ME ABOUT MY KNEES to a christening. Somebody asked.' },
    { op: 'say', unless_flag: 'flag:paul_rose_met', speaker: 'ROSE', text: 'He\'s planning a festival again, too. The Festival of the Imagined. The programmes are upstairs. Everyone on the bill is somebody out of a story, which does keep the catering simple.' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', unless_flag: 'flag:paul_milagro_given', speaker: 'ROSE', text: 'And if he\'s in a good mood, ask him about his cards. The painted ones. He pretends he doesn\'t want to show you.' },
    { op: 'say', unless_flag: 'flag:paul_rose_met', speaker: 'ROSE', text: 'And that poster by the fire is a JOKE. Probably. I stopped asking around the time I learned to make tea.' },
    { op: 'setFlag', flag: 'flag:paul_rose_met' },
  ],

  // The museum placard at the top of the stairs (once).
  'script.paul_museum': [
    { op: 'narrate', text: 'A hand-lettered placard at the top of the stairs:' },
    { op: 'narrate', text: 'THE MUSEUM OF T-SHIRTS. ADMISSION: ONE STORY. PLEASE DO NOT TOUCH THE EXHIBITS. (LOTTIE MAY TOUCH THE EXHIBITS.)' },
    { op: 'narrate', text: 'Underneath, smaller: THE WORKING RAILS — OUT. IN. NEVER. (THE THIRD ONE IS NOT A CHALLENGE.)' },
    { op: 'setFlag', flag: 'flag:paul_museum_seen' },
  ],

  // ---- the Festival of the Imagined (the museum lectern) ---------------------------------
  'script.paul_festival': festPage(0),
  ...Object.fromEntries(FEST_PAGES.slice(1).map((_, k) => [`script.paul_festival_${k + 1}`, festPage(k + 1)])),
  'script.paul_festival_last': [
    { op: 'narrate', text: 'The last page is almost empty. In the middle, in the same careful print:' },
    { op: 'narrate', text: 'AND — WHO WILL WE SEE IN YOUR FESTIVAL OF THE IMAGINED?' },
    { op: 'narrate', if_flag: 'flag:paul_festival_written', text: 'Underneath, in your own hand, is the name you wrote last time. There\'s room for another.' },
    {
      op: 'askName',
      title: 'WHO WILL YOU INVITE?',
      fallback: '...',
      store: false,
      matches: [
        { value: 'PAUL', flag: 'flag:paul_festival_paul' },
        { value: 'ROSE', flag: 'flag:paul_festival_family' },
        { value: 'LOTTIE', flag: 'flag:paul_festival_family' },
      ],
    },
    { op: 'narrate', unless_flag: 'flag:paul_festival_paul', text: 'You write the name on the last page, small and neat. Somewhere in the house a floorboard creaks, as if the room has started setting out another chair.' },
    { op: 'narrate', if_flag: 'flag:paul_festival_paul', text: 'You write PAUL on the last page. It looks right there. You suspect he\'d grumble, go red, and then turn up an hour early to help with the chairs.' },
    { op: 'narrate', if_flag: 'flag:paul_festival_family', text: 'Next to your name, in crayon, somebody has already added: "AND THE BIRD-PIG."' },
    { op: 'setFlag', flag: 'flag:paul_festival_paul', value: false },
    { op: 'setFlag', flag: 'flag:paul_festival_family', value: false },
    { op: 'setFlag', flag: 'flag:paul_festival_written' },
  ],

  // ---- the milagro cards ----------------------------------------------------------------
  // Paul's lamp menu, once the cup's yours: he deals them (the key item, once).
  'script.paul_milagro_cards': [
    { op: 'say', speaker: 'PAUL', text: 'My cards? Ha. Somebody\'s been talking. ...Rose. It\'s always Rose.' },
    { op: 'say', speaker: 'PAUL', text: 'In the sun country, over the western sea, folk hang little tin charms in the chapels — a tin heart, a tin leg, a tin eye — for whatever wants mending. Milagros, they call them. Small miracles.' },
    { op: 'say', speaker: 'PAUL', text: 'I can\'t work tin. So I paint them. Here — I\'ll deal you a hand.' },
    { op: 'narrate', text: 'THE HEART. A red heart with a crack mended in gold thread. For anything that\'s broken and taking its time.' },
    { op: 'narrate', text: 'THE LAMP. A lamp in a window. For whoever leaves one on for somebody.' },
    { op: 'narrate', text: 'THE WALKER. A little figure on a long road, not lost. You recognise the hat.' },
    { op: 'narrate', text: 'THE BIRD-PIG. Painted this year, by request. The request was in crayon.' },
    { op: 'narrate', text: 'And the last card, painted almost black, with one small restless flame in the middle. Lettered along the bottom: DESASOSIEGO.' },
    { op: 'say', speaker: 'PAUL', text: 'That one\'s the oldest. It\'s their word for it — the unease that won\'t let you sit still until you\'ve made something. Gets in at night. Paces the kitchen.' },
    { op: 'say', speaker: 'PAUL', text: 'Folk think it\'s a sickness. It isn\'t. It\'s the cure, turning up early. Every card I ever painted, that\'s who painted it. I just held the brush.' },
    { op: 'giveItem', unless_flag: 'flag:paul_milagro_given', item: 'milagro_cards', count: 1 },
    { op: 'say', unless_flag: 'flag:paul_milagro_given', text: 'Paul squares the cards and presses them into your hand. Received the MILAGRO CARDS!' },
    { op: 'say', unless_flag: 'flag:paul_milagro_given', speaker: 'PAUL', text: 'Keep them. When the itch comes for you — and it will, you\'ve the look — don\'t fight it. Make something. Then come and show me.' },
    { op: 'say', if_flag: 'flag:paul_milagro_given', speaker: 'PAUL', text: 'You\'ve already got a hand. Use it. That\'s the only rule.' },
    { op: 'setFlag', flag: 'flag:paul_milagro_given' },
  ],
  // The framed set on the kitchen wall.
  'script.paul_milagro_wall': [
    { op: 'narrate', text: 'Three painted cards pinned in a little frame: a cracked heart mended in gold, a lamp in a window, and a dark card with one small flame.' },
    { op: 'narrate', text: 'Under the dark one, a label in Paul\'s loopy hand: "DESASOSIEGO. the itch to make a thing. do not scratch. MAKE THE THING."' },
    { op: 'narrate', unless_flag: 'flag:paul_milagro_given', text: 'There are pinholes for more. Wherever the rest of the set is, it\'s probably in his coat pocket.' },
  ],

  // ---- the three rails ------------------------------------------------------------------
  'script.paul_rail_out': [
    { op: 'narrate', text: 'A tidy rail under a green board: OUT. Pressed, buttoned, collared. A card in Paul\'s loopy hand: "SAFE TO BE SEEN IN. LOTTIE HAS APPROVED EACH ONE IN WRITING."' },
    ...railMenu(RAIL_FLAGS[0], [
      shirtPick('The navy one', 'Plain navy, two buttons, not a crease on it. The card: "for the bank and the barber. same shirt for thirty years. neither of them has noticed."'),
      shirtPick('The white one', 'Crisp white, with a tiny lighthouse stitched over the pocket. The card: "lottie ironed this one. it is now a slightly different shape. still wearing it."'),
      shirtPick('The mustard one', 'Mustard yellow with a proper collar. The card: "collars mean you can be trusted with a ladder. that\'s the rule. i didn\'t make it. (i made it.)"'),
    ]),
  ],
  'script.paul_rail_in': [
    { op: 'narrate', text: 'A worn wooden rail under an amber board: IN. Faded, baggy, much-loved. A pair of slippers waits underneath. The card: "HOUSE ONLY. THE DOOR IS A BORDER."' },
    ...railMenu(RAIL_FLAGS[1], [
      shirtPick('The holey one', 'Grey, and more hole than shirt. The card: "do not mend. the hole is load-bearing."'),
      shirtPick('The stripy one', 'Blue-and-white stripes, soft as a cloud, very clearly half of a pair of pyjamas. The card: "the bottoms are on a beach in the cape country. long story. good beach."'),
      shirtPick('The pink one', 'A big pink one that reaches the knees. The card: "it\'s a nightshirt now. dignity is optional indoors."'),
      shirtPick('The painty one', 'Grey, splattered yellow, red and green. The card: "painted the kitchen in this. then the chair. then, briefly, me."'),
    ]),
  ],
  'script.paul_rail_never': [
    { op: 'narrate', text: 'An iron rail under a red board: NEVER! A velvet rope hangs across the front, padlocked to the post. Tucked into the padlock, a card in Lottie\'s crayon:' },
    { op: 'narrate', text: '"GRANDAD THESE ARE BANNED. NOT OUTSIDE. NOT INSIDE. NOT EVER. — LOTTIE (IN CHARGE)"' },
    { op: 'narrate', unless_flag: RAIL_FLAGS[2], text: 'The rope is only padlocked at one end. You lift it, very carefully, and duck under.' },
    { op: 'emote', unless_flag: RAIL_FLAGS[2], actor: 'player', emote: 'sweat' },
    ...railMenu(RAIL_FLAGS[2], [
      shirtPick('The lime one', 'Lime green with yellow zigzags, and in enormous letters: ASK ME ABOUT MY KNEES. Paul\'s card: "nobody asks. everybody is told."'),
      shirtPick('The pink one', 'Hot pink, with a beaming cartoon bun: CERTIFIED BUN INSPECTOR. Lottie\'s crayon underneath: "CONFISKATED. EVIDENSE."'),
      shirtPick('The black one', 'Black, with one word in tall white letters: NO. Paul\'s card: "wore it to a wedding. the vicar asked me a question. i didn\'t even have to answer."'),
      shirtPick('The orange one', 'Bright orange and completely plain. You turn it round. On the back: I\'M NOT LOST, I\'M WANDERING. Paul\'s card: "banned for being too true. i appealed. i lost."'),
    ]),
  ],
  // Looked through all three rails: a note in the last pocket (once).
  'script.paul_rails_all': [
    { op: 'run', if_flag: RAIL_FLAGS[0], ref: 'script.paul_rails_all_2' },
  ],
  'script.paul_rails_all_2': [
    { op: 'run', if_flag: RAIL_FLAGS[1], ref: 'script.paul_rails_all_3' },
  ],
  'script.paul_rails_all_3': [
    { op: 'run', if_flag: RAIL_FLAGS[2], unless_flag: 'flag:paul_rails_note', ref: 'script.paul_rails_note' },
  ],
  'script.paul_rails_note': [
    { op: 'narrate', text: 'As you hang the shirt back, something crackles in its pocket: a folded note.' },
    { op: 'narrate', text: '"IF YOU\'RE READING THIS YOU\'VE BEEN THROUGH ALL THREE RAILS. THAT MAKES YOU A CURATOR. CURATORS GET PAID. — p."' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'narrate', text: 'Folded inside is a GLOW CHARGE. Received a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:paul_rails_note' },
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
