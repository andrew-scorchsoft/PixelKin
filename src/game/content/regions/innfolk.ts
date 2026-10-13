/**
 * THE INN FOLK (2026-10, QoL round) — two counter characters for the things a
 * Wayfarer wants done to a kin, both running `kinService` (ui/KinServices).
 *
 *  * HESPER VANE, THE ECHO-READER — sits by the hearth in EVERY inn (Crossroads,
 *    Pearlmoor, Lowleaf, Galehigh, Pale Vault, Nightreach). A retired lamp-tender
 *    who reads the "echoes" a kin's moves leave in lamp-light. Running gag: she is
 *    always a car ahead of you ("Before you ask: the Lantern-car. I take the early
 *    one."). Services: REMEMBER A MOVE (HESPER_FEE wicks, charged only if a move is
 *    learned; mirrored in tools/balance/progression.mjs PRICES + 10-economy.md),
 *    LET A MOVE GO, READ MY KIN (kindling forecast + bond warmth). Each inn holds
 *    one memory of her old kin Sorrel (`flag:hesper_<inn>`, any order); hear all
 *    six and she gives you Sorrel's last two Lumen Drops (`flag:hesper_gift`).
 *  * OTTILIE PENN, THE NAMEWRIGHT — at the Wickstead lamp-school's bookcase. A name
 *    given at the catch is kept; she alone changes one (free).
 *
 * Placements: tools/maps/hand_placed_data.py (id `hesper` in each inn, `namewright`
 * in wickstead_school). Pure optional service + colour: nothing here gates anything.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

/** Wicks Hesper asks to coax a forgotten move back. */
export const HESPER_FEE = 250;

const H = 'HESPER';
const N = 'OTTILIE';
const h = (text: string): CutsceneStep => ({ op: 'say', speaker: H, text });
const n = (text: string): CutsceneStep => ({ op: 'say', speaker: N, text });

/** The six inns, each holding one memory of Sorrel. */
const INNS: Array<{ id: string; quip: string; memory: string }> = [
  {
    id: 'crossroads',
    quip: 'The Crossroads. Every road comes through here eventually, and so does everyone on them.',
    memory: 'My Sorrel was born under this roof, did you know? A little ember-kin, no bigger than a teacup. She sneezed sparks into the innkeeper\'s porridge.',
  },
  {
    id: 'pearlmoor',
    quip: 'Before you ask: the Lantern-car. I take the early one. You walk; I sit. We both get here.',
    memory: 'Sorrel loved the quay. She\'d sit on the bollards and glare at the gulls. When the Dusk came, she forgot every move she had, all in one night. Lamps went dim, and so did she.',
  },
  {
    id: 'lowleaf',
    quip: 'Lowleaf! They do a mushroom broth here that I would cross the whole crescent for. I nearly have.',
    memory: 'That\'s how I learned to read echoes. Every move a kin has known leaves a little light behind, like a warm cup leaves a ring. I sat with Sorrel\'s lamp every night and coaxed hers back, one by one.',
  },
  {
    id: 'galehigh',
    quip: 'Windy up here, isn\'t it? I lost a perfectly good hat on the terraces. A kite-child is wearing it now. Suits her.',
    memory: 'Took me three winters to bring back her first move. The silliest one, of course: a little puff of smoke she used to make at strangers. I cried like a kettle.',
  },
  {
    id: 'pale_vault',
    quip: 'Cold enough to freeze a thought halfway. Sit by the fire with me; the echoes read clearer when you\'re warm.',
    memory: 'Sorrel\'s old now. She rests in a Hearth back home, curled round the warm stones. She can\'t come on the cars with me. So I listen to other people\'s lamps instead. It keeps my hands in.',
  },
  {
    id: 'nightreach',
    quip: 'Nightreach. They watch the sky here like it owes them money. I like them enormously.',
    memory: 'Last winter Sorrel said my name. Not in words, kin don\'t. But she looked up when I came in, the way she used to. All her moves are home now. Every one.',
  },
];

const innScripts: ScriptRegistry = {};
for (const inn of INNS) {
  innScripts[`script.hesper_${inn.id}`] = [
    { op: 'run', ref: 'script.hesper_meet', unless_flag: 'flag:met_hesper' },
    { ...h(inn.quip), unless_flag: `flag:hesper_${inn.id}` },
    { ...h(inn.memory), unless_flag: `flag:hesper_${inn.id}` },
    { op: 'setFlag', flag: `flag:hesper_${inn.id}` },
    { op: 'run', ref: 'script.hesper_gift_0', unless_flag: 'flag:hesper_gift' },
    { op: 'run', ref: 'script.hesper_menu' },
  ];
}

// The gift chain: each link runs the next only while that inn's memory is held,
// so the last link (the gift) plays only once all six are heard.
const giftChain: ScriptRegistry = {};
INNS.forEach((inn, i) => {
  giftChain[`script.hesper_gift_${i}`] = [
    { op: 'run', ref: `script.hesper_gift_${i + 1}`, if_flag: `flag:hesper_${inn.id}` },
  ];
});
giftChain[`script.hesper_gift_${INNS.length}`] = [
  h('Six inns, and you\'ve sat through every one of my stories. Most people leave after the porridge.'),
  h('Here. Sorrel saved these for a kin who\'d need them more than she does. She was very firm about it. Well. I was. On her behalf.'),
  { op: 'giveItem', item: 'lumen_drop', count: 2 },
  { op: 'say', text: 'Received two LUMEN DROPS!' },
  { op: 'setFlag', flag: 'flag:hesper_gift' },
];

export const INNFOLK_SCRIPTS: ScriptRegistry = {
  ...innScripts,
  ...giftChain,

  'script.hesper_meet': [
    h('Oh! A lamp-tender. Come and sit; I don\'t bite, and the fire\'s the good chair.'),
    h('Hesper Vane. I read echoes. Every move your kin has ever known leaves a little light in its lamp, and I can coax one back out, if it\'s been forgotten.'),
    h('Or help one go, if it\'s crowding the others. Or just tell you how your kin are getting on. I\'m in every inn, more or less. Don\'t ask how.'),
    { op: 'setFlag', flag: 'flag:met_hesper' },
  ],

  'script.hesper_menu': [
    {
      op: 'choice',
      speaker: H,
      prompt: 'What can I do for you?',
      options: [
        {
          label: 'REMEMBER A MOVE',
          ops: [
            h(`A forgotten move, coaxed back. ${HESPER_FEE} wicks for the lamp-oil, and only if it takes.`),
            { op: 'kinService', service: 'relearn', cost: HESPER_FEE, speaker: H },
          ],
        },
        { label: 'LET A MOVE GO', ops: [{ op: 'kinService', service: 'forget', speaker: H }] },
        {
          label: 'READ MY KIN',
          ops: [
            h('Hold its lamp up to the fire. Let\'s see.'),
            { op: 'kinService', service: 'read', speaker: H },
          ],
        },
        {
          label: 'YOUR STORY',
          ops: [
            h('Mine? Oh, it\'s Sorrel\'s really. I tell a bit of it in every inn. Find me in the others and you\'ll have the lot.'),
          ],
        },
        { label: 'NOTHING', ops: [h('Then sit a while anyway. Mind the cat; it\'s not mine.')] },
      ],
    },
  ],

  'script.namewright': [
    { ...n('Ottilie Penn, Namewright. I write the names on the lamp-school\'s slates, and in the big book behind me.'), unless_flag: 'flag:met_namewright' },
    { ...n('A name you give at the catch is a promise, so it sticks. But promises can be rewritten, with care. That\'s my trade.'), unless_flag: 'flag:met_namewright' },
    { op: 'setFlag', flag: 'flag:met_namewright' },
    {
      op: 'choice',
      speaker: N,
      prompt: 'A name to write?',
      options: [
        {
          label: 'RENAME A KIN',
          ops: [
            n('Which one? And think it over. A name is the first lantern you hang on someone.'),
            { op: 'kinService', service: 'rename', speaker: N },
          ],
        },
        {
          label: 'WHY NAMES?',
          ops: [
            n('In the old days, a lamp-tender named a kin before they ever lit for it. If you know what to call something, you can call it home.'),
            n('Leave it blank and I\'ll write the old name back. No shame in that. It was a good name when you found it.'),
          ],
        },
        { label: 'NOTHING', ops: [n('Come back with a story. I\'ll find it a name.')] },
      ],
    },
  ],
};

export const INNFOLK_DIALOGUE: DialogueRegistry = {};
