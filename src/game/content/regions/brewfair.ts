/**
 * THE WAKEFUL FAIR (2026-10) — S7 "Just One More Cup": the great coffee festival in
 * the striped marquee on Wayward Rise (maps: wakeful_fair / _loft / _dream, builder
 * tools/maps/build_wakeful_fair.py; art tools/maps/brewforge.py).
 *
 * PAUL'S STORY, RETOLD. He went to a coffee festival once, just for a cup. Every
 * stall had a free sample, and he is not a man who can say no to a free thing
 * offered nicely — and before he knew it he was very nearly hallucinating. The fair
 * replays that afternoon for the player: sixteen stalls, sixteen samples, and the
 * marquee getting stranger with every one. It is Paul content (hidden real-people
 * content): never in the changelog, never in the guide (tools/build/guide.mjs
 * FORBIDDEN), never named by the Worry Club or Andrew.
 *
 * The rules of the place:
 *  * THE CUP. The flap only opens for someone with a cup of their own — Paul's Tin
 *    Cup, S5's reward (`flag:q_south_wander_done`). The stallholders all know that
 *    cup: an old fellow came through with it once and tried EVERYTHING.
 *  * SIXTEEN SAMPLES. Each stall (and both free-sample hawkers) sets
 *    `flag:brew_stamp_<n>` (the tasting card) and `flag:brewcup_<n>` (the caffeine).
 *    The decaf stall stamps #17 and pours no caffeine at all. FlagStore derives the
 *    stage from the cups (COUNT_AT_LEAST): PERKY 3, BUZZING 7, SEEING 12 — and the
 *    marquee's ambience + music follow live (MapAmbience.when / music_when, re-read
 *    after every scene by WorldScene.refreshStoryState).
 *  * THE CAFFEINE IS THE KEY. Perky talks you past the TRADE ONLY steward (the
 *    loft); buzzing walks you THROUGH the Siphon Lab's queue and shows you the Stall
 *    That Isn't There; seeing wakes the Grand Urn, turns every brewer into a kin and
 *    opens the puddle at the urn's foot — the way down into the cup. The doors key
 *    on ANY_OF flags (`flag:brew_was_perky`, `flag:brew_was_buzzing`), so they stay
 *    open after you've slept it off.
 *  * THE BOTTOM OF THE CUP. A caramel slick (ice: slide till something stops you)
 *    to the Bottomless Cup, where THE BUZZ — your own heartbeat, given wings
 *    (Thrumble #98, a `bossBattle`, no lamp, no running) — won't let you rest until
 *    you make it. Then a Snoozlet, and sleep, and you wake in the Quiet Tent. The
 *    wake clears every cup and stage flag (the hallucinations end) and sets
 *    `flag:q_south_brew_done`; the stamps stay, so the card can still be finished.
 *  * THE RECORD. The plaque in the Quiet Tent: P., with a tin cup, twenty-three.
 *    There are only sixteen stalls. Nobody knows where he found the other seven.
 *
 * Tone: funny, warm, a little silly, never mean — coffee as a festival, not a drug.
 * No brand names (it's "the press pot", "the siphon", "the eight-sided moka pot").
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

export const BREW_DONE = 'flag:q_south_brew_done';
const PERKY = 'flag:brew_perky';
const BUZZING = 'flag:brew_buzzing';
const SEEING = 'flag:brew_seeing';
const HAS_CARD = 'flag:brew_has_card';
const STAMP = (n: number): string => `flag:brew_stamp_${n}`;
const CUP = (n: number): string => `flag:brewcup_${n}`;
/** The sixteen caffeinated samples, by stamp number (the decaf is #17). */
export const BREW_SAMPLES = 16;

/** One sample: stamp the card, count the cup (not once you've slept it off), react. */
const sip = (n: number): CutsceneStep[] => [
  { op: 'sfx', key: 'world-pickup' },
  { op: 'setFlag', flag: STAMP(n) },
  { op: 'setFlag', flag: CUP(n), unless_flag: BREW_DONE },
  { op: 'run', ref: 'script.brew_after_sip' },
];

const say = (speaker: string, text: string, extra: Partial<CutsceneStep> = {}): CutsceneStep =>
  ({ op: 'say', speaker, text, ...extra }) as CutsceneStep;
const nar = (text: string, extra: Partial<CutsceneStep> = {}): CutsceneStep =>
  ({ op: 'narrate', text, ...extra }) as CutsceneStep;

/**
 * A stall's whole conversation: the AGAIN branch is checked FIRST so the first
 * visit (which stamps the card at its end) never falls through into it.
 */
function stall(n: number): CutsceneStep[] {
  return [
    { op: 'run', ref: `script.brew_again_${n}`, if_flag: STAMP(n) },
    { op: 'run', ref: `script.brew_first_${n}`, unless_flag: STAMP(n) },
  ];
}

/** The two halves each stall registers (first visit, every visit after). */
const STALLS: Record<number, { first: CutsceneStep[]; again: CutsceneStep[] }> = {};

// ---- 1 · THE EMBER ROAST (Corbin, a Cinderhead miner) -------------------------------
const CORBIN = 'CORBIN';
STALLS[1] = {
  first: [
    say(CORBIN, 'Ember Roast! Dark as a mineshaft, roasted over a live Ember kin\'s tail. Ethically. She volunteers. She likes the warmth.', { unless_flag: SEEING }),
    say('VULPYRE', 'Yip! Yip yip! ...Ahem. I mean: Ember Roast. Dark as a mineshaft. Would you like an espresso?', { if_flag: SEEING }),
    nar('A thimble of black coffee lands on the counter with a sound like a decision.'),
    say(CORBIN, 'Strong enough to stand a spoon in. We tested. The spoon left.'),
    nar('It tastes like a bonfire that went to school.'),
    ...sip(1),
  ],
  again: [
    say(CORBIN, 'Back for the spoon? It\'s in Cinderhead now. It\'s doing well for itself.', { unless_flag: SEEING }),
    say('VULPYRE', 'Yip! (It\'s offering you a second espresso with its whole face.)', { if_flag: SEEING }),
  ],
};

// ---- 2 · THE POUR-OVER BAR (Prudence) ------------------------------------------------
const PRUDENCE = 'PRUDENCE';
STALLS[2] = {
  first: [
    say(PRUDENCE, 'Shh. The bloom.', { unless_flag: SEEING }),
    say('GLIMFLIT', '...circles... small circles... shh... the bloom...', { if_flag: SEEING }),
    nar('She pours a thin ring of water over the grounds in a paper cone. She waits. She pours another ring. She looks at you as if you\'d interrupted, although you didn\'t say anything.'),
    {
      op: 'choice',
      speaker: PRUDENCE,
      prompt: 'How long should it bloom?',
      options: [
        { label: 'THIRTY SECONDS', ops: [say(PRUDENCE, 'Thirty. Correct. You may stay.')] },
        { label: 'FORTY-FIVE', ops: [say(PRUDENCE, 'Forty-five. Bold. Wrong, but bold.')] },
        { label: 'JUST POUR IT', ops: [nar('Somewhere, a kettle gasps.'), say(PRUDENCE, '...I am going to pretend you said thirty.')] },
      ],
    },
    nar('Four whole minutes later, a cup. It tastes of berries, and patience, and a faint disappointment in you.'),
    ...sip(2),
  ],
  again: [
    say(PRUDENCE, 'Another cup is four more minutes. You don\'t have four more minutes in you. I can tell. Your leg is going.', { unless_flag: BREW_DONE }),
    say(PRUDENCE, 'You look calmer. Good. Calm people bloom properly.', { if_flag: BREW_DONE }),
  ],
};

// ---- 3 · THE PRESS POTS (Bryn Hefty, a Galehigh kite-weaver with arms like rope) -----
const BRYN = 'BRYN HEFTY';
STALLS[3] = {
  first: [
    say(BRYN, 'Press pot! Four minutes steeping, then — the PLUNGE.', { unless_flag: SEEING }),
    say('RUBBOL', 'Rrrumble. (It\'s a small round boulder in an apron. It looks keen.)', { if_flag: SEEING }),
    nar('Bryn grips the plunger with both hands, plants her feet, breathes out slowly, and presses down like she\'s lifting a cart off a friend.'),
    { op: 'shake', ms: 250, intensity: 0.002 },
    say(BRYN, 'Personal best. Don\'t tell the Lifting House. They\'ll want me on the bench.'),
    nar('It\'s thick and heavy and it fills you right up to your eyebrows.'),
    ...sip(3),
  ],
  again: [
    say(BRYN, 'No more plunges today. I\'ve pressed my limit. Literally — the gauge says so.'),
  ],
};

// ---- 4 · COLD BREW (Tidwell Steep, a Saltreach fisher — the slowest man alive) -------
const TIDWELL = 'TIDWELL';
STALLS[4] = {
  first: [
    say(TIDWELL, 'Cold... ... ... brew.', { unless_flag: SEEING }),
    say('BRINEROLL', '...Cold... ... ... ... ... brew.', { if_flag: SEEING }),
    say(TIDWELL, 'Steeped... for... eighteen... hours.'),
    nar('He reaches for a bottle. You could have walked to Pearlmoor and back. Possibly twice.', { unless_flag: PERKY }),
    nar('He reaches for a bottle. You are vibrating. He is not. Somebody in this conversation is going to have to wait, and it isn\'t going to be him.', { if_flag: PERKY }),
    say(TIDWELL, 'There... you... go.'),
    nar('It\'s cold and smooth and sweet, like the sea if the sea had made an effort.'),
    ...sip(4),
  ],
  again: [
    say(TIDWELL, 'Next... batch... ready... in...'),
    nar('He\'s still saying it. You decide not to wait for the number.'),
  ],
};

// ---- 5 · THE SAND POT (Grandmother Ilka, who reads the grounds) ---------------------
const ILKA = 'GRANDMOTHER ILKA';
STALLS[5] = {
  first: [
    say(ILKA, 'Sit, child. The little pots cook in the hot sand, slow, slow. And when you finish, I read the grounds.', { unless_flag: SEEING }),
    say('RIDDLESTONE', 'What is small, and hot, and tells your future in mud? ...Me. Sit down.', { if_flag: SEEING }),
    nar('She lifts a long-handled pot out of the sand just as it froths, and pours a tiny, thick, fragrant cup. You drink it. She takes the cup and peers into the bottom.'),
    say(ILKA, 'I see... a long road. A lamp. A great many friends with too many legs.'),
    say(ILKA, 'And I see...', { unless_flag: PERKY }),
    say(ILKA, '...more coffee. Oh, child. So much more coffee.', { unless_flag: PERKY }),
    say(ILKA, 'And I see... a puddle. A swirling one. Mind your feet near big urns.', { if_flag: PERKY }),
    ...sip(5),
  ],
  again: [
    say(ILKA, 'Your future hasn\'t changed since you last sat. It is still mostly coffee.', { unless_flag: BREW_DONE }),
    say(ILKA, 'The grounds say you went down into the cup and came back up. Not many do it with their sense of humour.', { if_flag: BREW_DONE }),
  ],
};

// ---- 6 · MUSHROOM BREW (Mossy Margery, from the Lowleaf hollows) ---------------------
const MARGERY = 'MOSSY MARGERY';
STALLS[6] = {
  first: [
    say(MARGERY, 'Mushroom coffee, dear. Grounding. Earthy. Some say it\'s mostly mushroom.', { unless_flag: SEEING }),
    say('SPORELING', 'Mushroom coffee! Made of my cousins! ...With their blessing. Mostly.', { if_flag: SEEING }),
    say(MARGERY, 'Some say it\'s ALL mushroom. I say: drink it and find out.'),
    nar('It tastes like a forest floor that\'s very pleased to see you.'),
    ...sip(6),
  ],
  again: [
    say(MARGERY, 'Feeling grounded? No? That\'s the other eleven cups, dear. Not my fault.', { unless_flag: BREW_DONE }),
    say(MARGERY, 'There. Feet on the floor at last. Mushrooms can\'t do everything.', { if_flag: BREW_DONE }),
  ],
};

// ---- 7 · LATTE ART (Fern Rosetta, fourteen, a genius with a milk jug) ----------------
const FERN = 'FERN';
STALLS[7] = {
  first: [
    say(FERN, 'Latte art! I can draw anything in the foam. Anything at all. What do you want?', { unless_flag: SEEING }),
    say('PRISMCUB', 'Latte art! I can draw anything! (It\'s a small crystal cub in a hairnet. It is extremely sure of itself.)', { if_flag: SEEING }),
    {
      op: 'choice',
      speaker: FERN,
      prompt: 'What should Fern draw?',
      options: [
        { label: 'A HEART', ops: [nar('She tips the jug and a perfect heart blooms in the foam.')] },
        { label: 'MY FACE', ops: [nar('She concentrates very hard. It is a leaf.'), say(FERN, 'That\'s you. From the side. In a wind.')] },
        { label: 'MY KIN', ops: [nar('She concentrates very hard. It is a leaf.'), say(FERN, 'It\'s curled up asleep. You can tell because it\'s a leaf.')] },
        { label: 'A LEAF', ops: [nar('It is the best leaf you have ever seen. It might be the only thing she can draw. It doesn\'t matter.')] },
      ],
    },
    nar('You drink the art. It feels a bit rude, but it\'s delicious.'),
    ...sip(7),
    say(FERN, 'Hey — you battle, right? Art is a battle. Come back and I\'ll show you.'),
  ],
  again: [
    say(FERN, 'Ready? Art is a battle. Battle is art. I\'ve been waiting all day to say that to someone.', { unless_flag: 'flag:brew_fern_beaten' }),
    {
      op: 'choice',
      unless_flag: 'flag:brew_fern_beaten',
      speaker: FERN,
      prompt: 'A bout with Fern?',
      options: [
        { label: 'ART IS A BATTLE', ops: [{ op: 'battle', trainer: 'brewfair_fern' }, { op: 'setFlag', flag: 'flag:brew_fern_beaten' }, say(FERN, 'Fine. FINE. You\'re a better artist than me. ...In battles. Only in battles.')] },
        { label: 'LATER', ops: [say(FERN, 'The foam will wait. Foam\'s patient. Foam has nowhere to be.')] },
      ],
    },
    say(FERN, 'I\'m practising faces. Hold still. ...It\'s a leaf. Sorry.', { if_flag: 'flag:brew_fern_beaten' }),
  ],
};

// ---- 8 · THE CUPPING TABLE (Slurrington, competitive cupper; the loft) ---------------
const SLURR = 'SLURRINGTON';
STALLS[8] = {
  first: [
    say(SLURR, 'This is a CUPPING. Professional tasting. One does not sip. One SLURPS. Loudly. It aerates the coffee across the palate.', { unless_flag: SEEING }),
    say('DEWLING', 'SLLLLLLLRRRRP. (It\'s a dewdrop kin with a spoon. It has been waiting its whole life for this.)', { if_flag: SEEING }),
    say(SLURR, 'Spoon. Bowl. Now: as loud as you dare.'),
    {
      op: 'choice',
      speaker: SLURR,
      prompt: 'How loud?',
      options: [
        { label: 'A POLITE SLURP', ops: [nar('Slurp.'), say(SLURR, 'Pathetic. The palate barely noticed.')] },
        { label: 'A LOUD SLURP', ops: [nar('SLURRRP.'), say(SLURR, 'Acceptable. Amateur, but acceptable.')] },
        { label: 'EVERYTHING YOU HAVE', ops: [{ op: 'shake', ms: 400, intensity: 0.004 }, nar('SSSLLLLUUURRRRRRP. SLURRRRRP.'), nar('Three people at the far end of the loft turn round. A roaster drops a scoop.'), say(SLURR, '...Magnificent. Someone write that down.')] },
      ],
    },
    ...sip(8),
    say(SLURR, 'A real cupper fights for the table. Should you wish to.'),
  ],
  again: [
    {
      op: 'choice',
      unless_flag: 'flag:brew_slurrington_beaten',
      speaker: SLURR,
      prompt: 'A bout for the cupping table?',
      options: [
        { label: 'FOR THE TABLE', ops: [{ op: 'battle', trainer: 'brewfair_slurrington' }, { op: 'setFlag', flag: 'flag:brew_slurrington_beaten' }, say(SLURR, 'The table is yours. Treat it with respect. And slurp. Always slurp.')] },
        { label: 'NOT NOW', ops: [say(SLURR, 'Then practise. Quietly. No — loudly. Practise loudly.')] },
      ],
    },
    say(SLURR, 'You slurp with conviction. I\'ve told the others.', { if_flag: 'flag:brew_slurrington_beaten' }),
  ],
};

// ---- 11 · THE SIPHON LAB (Dr Alembic, a Nightreach star-watcher) ---------------------
const ALEMBIC = 'DR ALEMBIC';
STALLS[11] = {
  first: [
    say(ALEMBIC, 'Welcome to the Siphon Lab! Vacuum brewing! The water rises into the top chamber by SCIENCE, steeps, and then — watch — falls back down by MORE SCIENCE.', { unless_flag: SEEING }),
    say('FLICKORE', 'BZT. Welcome to the lab. BZT. The water goes up. BZT. Then down. Science. BZT.', { if_flag: SEEING }),
    nar('The blue flame burns. The water climbs into the glass globe as if it had somewhere to be. The doctor watches it with the look of someone meeting an old friend.'),
    say(ALEMBIC, 'That queue? Three hours, some of them. How did you get past them so quickly?'),
    nar('You try to explain. It comes out as one long word.'),
    say(ALEMBIC, '...Ah. Yes. You are very much the target market.'),
    ...sip(11),
  ],
  again: [
    say(ALEMBIC, 'Up, and down. Up, and down. It never gets old. I\'ve been here since the fair began. I think. What day is it?'),
  ],
};

// ---- 12 · FROST-BREW (Rime, a Pale Vault herder; the loft) --------------------------
const RIME = 'RIME';
STALLS[12] = {
  first: [
    say(RIME, 'Frost-brew. Poured over the breath of a Chillpip, served colder than the Rimeway in a bad winter.', { unless_flag: SEEING }),
    say('CHILLPIP', 'Pip. Pip pip. (It breathes on a glass. The glass frosts over. It looks extremely proud.)', { if_flag: SEEING }),
    nar('You drink it in one go. It is a mistake. A delicious mistake.'),
    { op: 'shake', ms: 300, intensity: 0.003 },
    nar('BRAIN. FREEZE.'),
    ...sip(12),
  ],
  again: [
    say(RIME, 'Sip it this time. Up north we say the brew is cold so you\'ll take your time. Nobody listens.'),
  ],
};

// ---- 13 · THE DAWNBEAN (Solveig, a Sunken Solarium sun-keeper; the loft) -------------
const SOLVEIG = 'SOLVEIG';
STALLS[13] = {
  first: [
    say(SOLVEIG, 'The Dawnbean. Grown under the last of the sunlamps in the Solarium. They say it tastes like morning.', { unless_flag: SEEING }),
    say('HELIBUD', 'Morning! Taste the morning! (It\'s a sunflower kin. It is glowing, a little, round the edges.)', { if_flag: SEEING }),
    nar('It\'s warm and bright and strange, and it tastes of something you can\'t quite name. Long light across a floor. A window someone opened.'),
    say(SOLVEIG, 'Nobody here remembers morning. Eleven winters of dusk. But everybody who drinks this goes quiet for a second, like they\'re trying.', { unless_flag: 'flag:dawn' }),
    say(SOLVEIG, 'Funny. Now the sky\'s come back, it tastes even more like it. Like a promise somebody kept.', { if_flag: 'flag:dawn' }),
    ...sip(13),
  ],
  again: [
    say(SOLVEIG, 'Keep the taste of it. You\'ll want it, one of these long nights.'),
  ],
};

// ---- 14 · MIDNIGHT OIL (Vesper, of the Hollowing — even they come to the fair) -------
const VESPER = 'VESPER';
STALLS[14] = {
  first: [
    say(VESPER, 'Midnight Oil. Roasted by moonlight, in the dark, the way the dark likes it. Triple strength.', { unless_flag: SEEING }),
    say('SNOOZLET', '...zzz... Midnight... Oil... zzz... (It\'s fast asleep. It\'s still somehow pouring.)', { if_flag: SEEING }),
    say(VESPER, 'Yes, I\'m Hollowing. We like a gentle dark, not a sleepy one. Even Còr takes his black.'),
    nar('It is the darkest coffee you have ever seen. Light goes into the cup and doesn\'t come out. You drink it anyway.'),
    { op: 'emote', actor: 'player', emote: 'alert' },
    nar('Every hair you own stands up and salutes.'),
    ...sip(14),
  ],
  again: [
    say(VESPER, 'A second cup of Midnight Oil has never been served. We aren\'t sure what would happen. We\'re not curious enough to find out.'),
  ],
};

// ---- 15 · THE STALL THAT ISN'T THERE (only the buzzing can see it) ------------------
const NOBODY = '???';
STALLS[15] = {
  first: [
    nar('There\'s a stall here. You\'re almost certain. You can see right through it, which is a bad sign for a stall.'),
    say(NOBODY, 'Hello! You can see me? Wonderful. Nobody can see me until about their seventh cup.'),
    say(NOBODY, 'I serve the coffee that isn\'t there. It\'s very light. Zero everything. Here.'),
    nar('You drink the coffee that isn\'t there. It\'s the best one yet. Your heart does a little cartwheel anyway.'),
    ...sip(15),
  ],
  again: [
    say(NOBODY, 'Still here! Well. Still not here. You know what I mean.', { unless_flag: BREW_DONE }),
    say(NOBODY, 'You can still see me, sober? Oh no. Oh, that\'s worse. That\'s so much worse for both of us.', { if_flag: BREW_DONE }),
  ],
};

// ---- 16 · PERCY'S MOKA STAND (the moka man from Duskapple, come to the fair) ---------
const PERCY = 'PERCY';
STALLS[16] = {
  first: [
    say(PERCY, 'You! From the orchard! You came! Now — have I told you about the eight-sided moka pot?', { unless_flag: SEEING }),
    say('HEARTHKIT', 'Mrrp! (A small warm kin in an apron is pointing proudly at an eight-sided moka pot.)', { if_flag: SEEING }),
    say(PERCY, 'Water in the bottom. Coffee in the middle. Heat. The pressure pushes it UP, through the grounds, into the top. Gurgle, gurgle — done.'),
    say(PERCY, 'Two hundred stalls at this fair, and only one of them is right. Guess which.'),
    nar('He pours a short, strong cup with the pride of a man defending a whole civilisation.'),
    ...sip(16),
    { op: 'giveItem', item: 'moka_cup', count: 1 },
    say(PERCY, 'And one for the road. Don\'t drink it now. ...You\'re going to drink it now.'),
  ],
  again: [
    say(PERCY, 'Did I mention it\'s EIGHT-sided? For the heat. The heat goes all the way round.', { unless_flag: BREW_DONE }),
    say(PERCY, 'Seven stalls tried to tell me a siphon is better. I said: does your siphon gurgle?', { if_flag: BREW_DONE }),
  ],
};

// ---- 17 · DECAF (Dennis, who has waited all day) — stamps the card, no caffeine -----
const DENNIS = 'DENNIS';

// The stalls' script keys -> their stamp number (map NPCs run script.brew_<kind>).
const STALL_KEYS: Record<string, number> = {
  ember: 1, pourover: 2, press: 3, coldbrew: 4, sandpot: 5, mushroom: 6, latte: 7,
  cupping: 8, siphon: 11, frost: 12, dawn: 13, midnight: 14, nothing: 15, moka: 16,
};

const stallScripts: ScriptRegistry = {};
for (const [key, n] of Object.entries(STALL_KEYS)) {
  stallScripts[`script.brew_${key}`] = stall(n);
  stallScripts[`script.brew_first_${n}`] = STALLS[n].first;
  stallScripts[`script.brew_again_${n}`] = STALLS[n].again;
}

/** A free-sample hawker: you will not be allowed to say no. */
function hawker(n: number, speaker: string, pitch: string): CutsceneStep[] {
  return [
    say(speaker, pitch),
    {
      op: 'choice',
      speaker,
      prompt: 'Try a free sample?',
      options: [
        { label: 'NO THANKS', ops: [nar('You say "no thanks". Your hand, independently, takes the cup.')] },
        { label: 'NO', ops: [nar('You say "no". It comes out as "mm, go on then".')] },
        { label: 'ABSOLUTELY NOT', ops: [say(speaker, 'That\'s the spirit!'), nar('You aren\'t sure what happened. You\'re holding a cup. The cup is empty. Your mouth is warm.')] },
      ],
    },
    nar('Free samples. You can\'t say no to a free thing offered nicely. Somebody you know is exactly the same.'),
    ...sip(n),
  ];
}

export const BREWFAIR_SCRIPTS: ScriptRegistry = {
  ...stallScripts,

  // ---- Paul, at his dark lamp (the lamp menu's "Too much coffee?") ------------------
  'script.brew_paul_story': [
    say('PAUL', 'Too much coffee? Ha. There\'s no such thing. ...There is. I\'ve met it.'),
    say('PAUL', 'Up past the wood, on the Rise, the brewers pitch a great striped tent. The Wakeful Fair. Every brewer in Vesperholm.', { unless_flag: BREW_DONE }),
    say('PAUL', 'I went once. Just for the one cup. But every stall had a free sample, and I\'m not a man who can say no to a free thing offered nicely.', { unless_flag: BREW_DONE }),
    say('PAUL', 'By the end of the afternoon the urn was singing to me. I had a long talk with a sugar cube. It had views.', { unless_flag: BREW_DONE }),
    say('PAUL', 'Take that cup. They won\'t let you in without one. And pace yourself.', { unless_flag: BREW_DONE }),
    { op: 'narrate', text: 'He considers you for a moment.', unless_flag: BREW_DONE },
    say('PAUL', 'You won\'t.', { unless_flag: BREW_DONE }),
    say('PAUL', 'You went! I can tell. You\'ve still got the look. How many? ...Ha. Twenty-three, me. The medic\'ll have told you.', { if_flag: BREW_DONE }),
    say('PAUL', 'Did the urn laugh at yours? Mine laughed. Nobody believes me. That\'s fine. That\'s how you know it was a good joke.', { if_flag: BREW_DONE }),
    { op: 'setFlag', flag: 'flag:brew_paul_told' },
  ],

  // ---- the doorman on the Rise (also the flap's "not yet") -------------------------
  'script.brewfair_doorman': [
    { op: 'run', ref: 'script.brewfair_doorman_after', if_flag: BREW_DONE },
    { op: 'run', ref: 'script.brewfair_doorman_in', if_flag: 'flag:q_south_wander_done', unless_flag: BREW_DONE },
    { op: 'run', ref: 'script.brewfair_doorman_no_cup', unless_flag: 'flag:q_south_wander_done' },
  ],
  'script.brewfair_doorman_no_cup': [
    say('DOORMAN', 'Evening! The Wakeful Fair — every brewer in Vesperholm under one roof of canvas. Free samples at every stall!'),
    say('DOORMAN', 'One rule. Bring your own cup. It\'s tradition. Also, in the third year we ran out of cups and we never recovered.'),
    say('DOORMAN', 'No cup? Then no coffee, friend. Sorry.'),
    say('DOORMAN', 'There\'s an old fellow walks the wood down there carries a tin cup everywhere. Ask him where a person gets a cup like that.', { unless_flag: 'flag:q_south_wander' }),
    say('DOORMAN', 'He\'s sent you up the wood, has he? Then finish what he started. Come back with a cup.', { if_flag: 'flag:q_south_wander' }),
    { op: 'setFlag', flag: 'flag:brew_fair_seen' },
  ],
  'script.brewfair_doorman_in': [
    say('DOORMAN', 'A cup! Let\'s see — oh. A TIN cup. With a dent in the rim just there.'),
    say('DOORMAN', '...I know that cup. Go on in, friend. Go on.'),
    say('DOORMAN', 'Pace yourself. Nobody ever does, but you can say you were told.'),
    { op: 'setFlag', flag: 'flag:brew_fair_seen' },
  ],
  'script.brewfair_doorman_after': [
    say('DOORMAN', 'You came out! Most do. Eventually. ...Your eyes have nearly stopped spinning.'),
  ],

  // ---- Marigold at the ticket table -------------------------------------------------
  'script.brewfair_welcome': [
    { op: 'emote', actor: 'marigold', emote: 'alert' },
    say('MARIGOLD', 'Welcome to the Wakeful Fair! Over here, love — cup?'),
    { op: 'face', actor: 'player', facing: 'left' },
    nar('You hold up Paul\'s Tin Cup.'),
    say('MARIGOLD', 'Oh. OH. That dent. That\'s — is that —? Never mind. Never you mind. You\'ll want a tasting card.'),
    { op: 'giveItem', item: 'tasting_card', count: 1 },
    { op: 'say', text: 'Got the TASTING CARD! Sixteen little squares for sixteen stalls, and a seventeenth that just says DECAF?' },
    say('MARIGOLD', 'Every stall pours you a free sample and stamps your card. Fill the whole card and come back to me — there\'s a prize.'),
    say('MARIGOLD', 'And a word to the wise: the samples are small. But there are a LOT of them.'),
    { op: 'setFlag', flag: HAS_CARD },
    { op: 'setFlag', flag: 'flag:brew_fair_seen' },
  ],
  'script.brewfair_marigold': [
    { op: 'run', ref: 'script.brewfair_marigold_prize', if_flag: 'flag:brew_card_full', unless_flag: 'flag:brew_card_prize' },
    say('MARIGOLD', 'A full card! Well, I never — well, I did, once. Enjoy the flask.', { if_flag: 'flag:brew_card_prize' }),
    say('MARIGOLD', 'Sixteen stalls, love, and one more if you\'re kind. Every square\'s a stamp. Don\'t forget upstairs.', { unless_flag: 'flag:brew_card_full' }),
    say('MARIGOLD', 'You\'re glowing a bit, love. The Quiet Tent\'s in the corner, if you want water. You won\'t want water.', { if_flag: BUZZING, unless_flag: SEEING }),
    say('MARIGOLD', 'Love, you\'re talking to the table. I\'m over here. No — here. That\'s the urn.', { if_flag: SEEING }),
  ],
  'script.brewfair_marigold_prize': [
    say('MARIGOLD', 'Every square! Even the decaf! Dennis will be beside himself.'),
    say('MARIGOLD', 'Here — the fair\'s own flask. Keep it open on the road and you\'ll fizz so loud the wild kin can hear you coming from a field away.'),
    { op: 'giveItem', item: 'wakeful_flask', count: 1 },
    { op: 'say', text: 'Got the WAKEFUL FLASK! (Open it from ITEMS: wild kin come to see what all the buzzing is.)' },
    { op: 'setFlag', flag: 'flag:brew_card_prize' },
  ],

  // ---- the stair to the loft: TRADE ONLY ------------------------------------------------
  'script.brewfair_trade_block': [
    { op: 'emote', actor: 'wilmot', emote: 'alert' },
    { op: 'face', actor: 'wilmot', facing: 'left' },
    say('WILMOT', 'Ah-ah. Trade only up there, I\'m afraid. Roasters and buyers. People who talk business. Fast.'),
    { op: 'move', actor: 'player', to: { tx: 1, ty: 4 } },
    say('WILMOT', 'You\'ll know it\'s you when you can\'t stop talking. It\'s usually about the third cup.'),
  ],
  'script.brewfair_wilmot': [
    say('WILMOT', 'Trade only, upstairs. The Roasters\' Loft. Buyers talk fast, and I only let in people who talk fast.', { unless_flag: 'flag:brew_was_perky' }),
    say('WILMOT', 'You? Go on up. You\'ve been explaining moka pots to me for four minutes and I didn\'t ask.', { if_flag: 'flag:brew_was_perky' }),
  ],

  // ---- the Siphon Lab's queue -----------------------------------------------------------
  'script.brewfair_queue': [
    say('THE QUEUE', 'We\'re queuing for the Siphon Lab. Since Tuesday. No, you can\'t go first.', { unless_flag: 'flag:brew_was_buzzing' }),
    say('THE QUEUE', '...Did you just walk THROUGH us? You did. You\'re vibrating at a frequency that should be illegal.', { if_flag: 'flag:brew_was_buzzing' }),
  ],

  // ---- the Grand Urn ---------------------------------------------------------------------
  'script.brewfair_urn': [
    nar('THE GRAND URN. Copper, enormous, older than the fair. A sign: PLEASE DO NOT CLIMB IN THE URN.', { unless_flag: SEEING }),
    nar('Someone has added underneath, in pencil: AGAIN.', { unless_flag: SEEING }),
    nar('The urn is singing. It has a lovely voice. It\'s singing your name, {name}, in harmony with itself.', { if_flag: SEEING }),
    nar('There\'s a puddle at its foot, swirling round and round, the colour of crema. It looks like it goes down a very long way.', { if_flag: SEEING, unless_flag: 'flag:brew_buzz_beaten' }),
    nar('It winks at you. It definitely winked.', { if_flag: BREW_DONE }),
  ],

  // ---- every cup: the inner voice, then (once each) the stage you've crossed into -------
  'script.brew_after_sip': [
    { op: 'run', ref: 'script.brew_after_sip_calm', if_flag: BREW_DONE },
    { op: 'run', ref: 'script.brew_after_sip_trip', unless_flag: BREW_DONE },
  ],
  'script.brew_after_sip_calm': [
    nar('Lovely. You feel perfectly, boringly fine. You stop at one, like a sensible person.'),
  ],
  'script.brew_after_sip_trip': [
    // the band you're IN (only once its arrival beat has played)
    nar('That\'s lovely, actually. Just the one more, though.', { unless_flag: PERKY }),
    nar('Your knee is bouncing. Your knee has its own plans. You\'ll try ONE more.', { if_flag: 'flag:brew_seen_perky', unless_flag: BUZZING }),
    nar('You can hear your own eyelashes. Just one more. Just a little one.', { if_flag: 'flag:brew_seen_buzzing', unless_flag: SEEING }),
    nar('Delicious. Purple, somehow. The cup thanks you for drinking it.', { if_flag: 'flag:brew_seen_seeing' }),
    // crossing into a new stage plays its beat once (latest first, so exactly one)
    { op: 'run', ref: 'script.brew_hit_seeing', if_flag: SEEING, unless_flag: 'flag:brew_seen_seeing' },
    { op: 'run', ref: 'script.brew_hit_buzzing', if_flag: BUZZING, unless_flag: 'flag:brew_seen_buzzing' },
    { op: 'run', ref: 'script.brew_hit_perky', if_flag: PERKY, unless_flag: 'flag:brew_seen_perky' },
  ],
  'script.brew_hit_perky': [
    { op: 'emote', actor: 'player', emote: 'music' },
    nar('Something\'s happening. Your foot is tapping. You didn\'t ask it to.'),
    nar('You feel GREAT. You could explain anything to anybody. Quickly. At length.'),
    nar('(Somewhere up the stair in the corner is a loft marked TRADE ONLY. You feel, suddenly, extremely trade.)'),
    { op: 'setFlag', flag: 'flag:brew_seen_perky' },
  ],
  'script.brew_hit_buzzing': [
    { op: 'shake', ms: 600, intensity: 0.003 },
    { op: 'emote', actor: 'player', emote: 'sweat' },
    nar('Your heart is doing a drumroll. It has been doing it for a while now. It shows no sign of getting to the big finish.'),
    nar('The colours are louder. The steam is spelling things. You could walk THROUGH a queue now. Not round it. Through it.'),
    nar('And over in the south-west corner there\'s a stall you\'re almost certain wasn\'t there a minute ago.'),
    nar('Just one more, though. Just one.'),
    { op: 'setFlag', flag: 'flag:brew_seen_buzzing' },
  ],
  'script.brew_hit_seeing': [
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'flashColor', color: '#c050ff', ms: 500 },
    { op: 'shake', ms: 900, intensity: 0.004 },
    nar('Wait.'),
    nar('Wait, wait, wait.'),
    nar('Everyone at the fair has turned into a kin. That\'s fine. That\'s normal. Everybody stay calm. You\'re calm. You are vibrating calmly.'),
    nar('And in the middle of the marquee, the Grand Urn has opened its eyes and started to sing.'),
    nar('There\'s a puddle swirling at its feet, round and round. It goes down a long, long way. It looks a lot like the bottom of a cup.'),
    { op: 'emote', actor: 'player', emote: 'heart' },
    nar('Just one more cup.'),
    { op: 'setFlag', flag: 'flag:brew_seen_seeing' },
  ],

  // ---- the way out, once: your feet turn round --------------------------------------
  'script.brewfair_one_more': [
    { op: 'spin', actor: 'player', turns: 1, end: 'up' },
    nar('You head for the flap. Your feet have other ideas. They turn you round and walk you back in.'),
    nar('There\'s a stall you haven\'t tried. Your feet can smell it.'),
    { op: 'move', actor: 'player', to: { tx: 15, ty: 18 } },
    nar('(Try leaving again if you really mean it. Your feet will sulk, but they\'ll go.)'),
    { op: 'setFlag', flag: 'flag:brew_tried_leave' },
  ],

  // ---- the free-sample hawkers (sight: they spot you, they march up) ------------------
  'script.brew_hawker_sal': hawker(9, 'SAMPLE SAL', 'FREE SAMPLE! Free sample, love! Our blend — a bit of everything, roasted by everybody! Nobody walks past Sal!'),
  'script.brew_hawker_sal_after': [
    say('SAMPLE SAL', 'One per customer! ...I mean that for you specifically. You\'ve had about nine.', { unless_flag: BREW_DONE }),
    say('SAMPLE SAL', 'Glad you\'re upright again, love. You were saying very nice things to a sugar cube earlier.', { if_flag: BREW_DONE }),
  ],
  'script.brew_hawker_fred': hawker(10, 'FREE-SAMPLE FRED', 'Ohhh no you don\'t! Nobody gets past Fred without a FREE SAMPLE! It\'s the law! Possibly! Here!'),
  'script.brew_hawker_fred_after': [
    say('FREE-SAMPLE FRED', 'Can\'t give you two. It\'s the law! Probably! I made it up!'),
  ],

  // ---- the decaf stall (stamp 17: no caffeine at all) ----------------------------------
  'script.brew_decaf': [
    { op: 'run', ref: 'script.brew_decaf_again', if_flag: STAMP(17) },
    { op: 'run', ref: 'script.brew_decaf_first', unless_flag: STAMP(17) },
  ],
  'script.brew_decaf_first': [
    say(DENNIS, '...Oh! A customer. Hello. Hello! Sorry — I wasn\'t expecting anyone. Nobody comes to the decaf stall.'),
    say(DENNIS, 'Would you... I mean, only if you want to... would you like some decaf?'),
    nar('He pours you a cup with enormous care. It\'s nice. It\'s honestly very nice. Nothing at all happens to your heart.'),
    { op: 'sfx', key: 'world-pickup' },
    { op: 'setFlag', flag: STAMP(17) },
    say(DENNIS, 'You liked it? You LIKED it. I\'m — sorry, I\'m fine. It\'s the steam.'),
    { op: 'giveItem', item: 'decaf_cup', count: 1 },
    { op: 'say', text: 'Got a CUP OF DECAF! For later. For when it all gets a bit much.' },
  ],
  'script.brew_decaf_again': [
    say(DENNIS, 'Decaf\'s not nothing, you know. Decaf is for the people who want to stay.', { unless_flag: BREW_DONE }),
    say(DENNIS, 'I heard you went down the cup. I sent some decaf down after you. Did it get there? I like to think it got there.', { if_flag: BREW_DONE }),
  ],

  // ---- the Quiet Tent's medic ----------------------------------------------------------
  'script.brewfair_medic': [
    say('MEDIC', 'The Quiet Tent. Lie down, drink water, stare at the canvas. Nobody ever takes the water.', { unless_flag: BUZZING }),
    say('MEDIC', 'Oh, look at you. Twitching like a kite in a gale. Have a lie down a minute.', { if_flag: BUZZING }),
    {
      op: 'choice',
      speaker: 'MEDIC',
      prompt: 'Have a lie down?',
      options: [
        {
          label: 'LIE DOWN',
          ops: [
            nar('You lie on a cot and stare at the canvas. The canvas stares back. Your kin curl up beside you.'),
            { op: 'heal', rest: false },
            say('MEDIC', 'There. Your kin are rested. You\'re not, but you knew that.'),
          ],
        },
        { label: 'NO, MORE COFFEE', ops: [say('MEDIC', 'They always say that. I\'ll keep your cot warm.')] },
      ],
    },
  ],

  // ---- THE BOTTOM OF THE CUP ------------------------------------------------------------
  'script.brewfair_buzz': [
    { op: 'letterbox', on: true, ms: 400 },
    nar('Something rises out of the Bottomless Cup. It\'s small, and it\'s very, very fast, and it\'s humming at exactly the speed of your heart.'),
    say('THE BUZZ', 'BZZZZT! Hello! I\'m you! The awake bit! We\'re having SUCH a lovely time!'),
    say('THE BUZZ', 'Sleep? SLEEP? Sleep is for people who haven\'t found the cold brew! One more cup! And one more! And one more!'),
    nar('It isn\'t going to let you rest. Not unless you make it.'),
    { op: 'letterbox', on: false, ms: 300 },
    { op: 'bossBattle', kin: 98, level: 20 },
    { op: 'run', ref: 'script.brewfair_sleep' },
  ],
  'script.brewfair_sleep': [
    nar('The Buzz wobbles, hums one last, smaller hum, and settles into the coffee like a sugar lump.'),
    nar('All at once you are very, very tired.'),
    nar('Something soft and round curls up on your chest. A Snoozlet. Where did a Snoozlet come from? It doesn\'t matter. It\'s warm.'),
    { op: 'musicFade', ms: 1200 },
    { op: 'fade', dir: 'out', ms: 900 },
    { op: 'wait', ms: 700 },
    { op: 'travel', map: 'wakeful_fair', to: { tx: 24, ty: 17 }, facing: 'right' },
    { op: 'run', ref: 'script.brewfair_wake' },
  ],
  'script.brewfair_wake': [
    nar('...'),
    nar('You wake up on a cot in the Quiet Tent with a blanket over your knees and a cup of water you didn\'t ask for.'),
    say('MEDIC', 'There you are. No — don\'t sit up yet. Do you know where you are? You kept telling the urn you loved it.'),
    say('MEDIC', 'Twelve samples, at least. In an afternoon. You were saying "just one more" and laughing at the tent poles.'),
    { op: 'emote', actor: 'player', emote: 'ellipsis' },
    say('MEDIC', 'Don\'t look like that. You\'re nowhere near the record. See the plaque?'),
    say('MEDIC', 'An old fellow with a tin cup. Same as yours, actually — VERY same as yours. Twenty-three samples. There are sixteen stalls. Nobody knows where he found the other seven.'),
    say('MEDIC', 'He said the urn laughed at his joke. We all said that was the coffee. ...The urn\'s never laughed at mine.'),
    // the trip is over: every cup and stage flag goes (the stamps stay on the card)
    ...Array.from({ length: BREW_SAMPLES }, (_, i): CutsceneStep => ({ op: 'setFlag', flag: CUP(i + 1), value: false })),
    { op: 'setFlag', flag: SEEING, value: false },
    { op: 'setFlag', flag: BUZZING, value: false },
    { op: 'setFlag', flag: PERKY, value: false },
    { op: 'setFlag', flag: BREW_DONE },
    say('MEDIC', 'Here. From Dennis at the decaf stall. He\'s been waiting all day for somebody to need him.'),
    { op: 'giveItem', item: 'lumen_drop', count: 2 },
    { op: 'say', text: 'Got 2 LUMEN DROPS! Tucked in a napkin, with a note: "for after. — D."' },
    nar('You feel... normal. Mostly. The tent has stopped breathing. The poles are just poles.'),
    nar('Out in the marquee, the Grand Urn is only an urn again. You could swear it winks at you as you pass.'),
  ],
  'script.brewfair_bottomless': [
    nar('THE BOTTOMLESS CUP. It goes down for ever. You can hear, faintly, somebody at the bottom asking for one more.'),
  ],
  'script.brewfair_teacup': [
    say('A TEACUP', 'We are the Previous Cups. Every one of us was somebody\'s "just one more".'),
    say('A TEACUP', 'Don\'t worry. We had a lovely time.'),
  ],
  'script.brewfair_dream_kin': [
    say('SPIRLET', 'Hello! Have you tried the oat milk? I haven\'t. I\'m a figment. Figments are lactose-free.'),
    say('SPIRLET', 'If you want the cup, slide until something stops you. That\'s also my advice for life.'),
  ],
  'script.brewfair_dream_moth': [
    say('FLUTTERWANE', 'I\'m the moth from the Stall That Isn\'t There. I\'m also not here. It\'s a family business.'),
    say('FLUTTERWANE', 'The buzzing thing at the cup won\'t let anyone sleep. Somebody ought to tire it out.', { unless_flag: 'flag:brew_buzz_beaten' }),
  ],

  // ---- the finds ------------------------------------------------------------------------
  'script.pickup_brew_wing': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'say', text: 'Wedged behind the bean sacks: 2 GLOW CHARGES. Somebody gave up their place in the queue and dropped these on the way out.' },
    { op: 'setFlag', flag: 'flag:picked_brew_wing' },
  ],
  'script.pickup_brew_loft': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'Tucked under the loft rail: 2 WARM BALMS, and a buyer\'s order for "as much as you have, no, more than that".' },
    { op: 'setFlag', flag: 'flag:picked_brew_loft' },
  ],
  'script.pickup_brew_dream': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'On the islet, a single perfect coffee bean. You pick it up and it turns into a LUMEN DROP. Dreams are like that.' },
    { op: 'setFlag', flag: 'flag:picked_brew_dream' },
  ],

  // ---- the champion of the loft ----------------------------------------------------------
  'script.brew_champion': [
    say('OTTOLINE', 'Ottoline Crema. Head Barista. Champion of the Wakeful Fair seven years running.', { unless_flag: 'flag:brew_champion_beaten' }),
    say('OTTOLINE', 'Everyone wants to lift the Golden Cup. Everyone thinks it\'s about the coffee. It\'s not. It\'s about NERVE.', { unless_flag: 'flag:brew_champion_beaten' }),
    {
      op: 'choice',
      unless_flag: 'flag:brew_champion_beaten',
      speaker: 'OTTOLINE',
      prompt: 'Challenge the Head Barista?',
      options: [
        {
          label: 'FOR THE GOLDEN CUP',
          ops: [
            { op: 'battle', trainer: 'brewfair_ottoline' },
            { op: 'setFlag', flag: 'flag:brew_champion_beaten' },
            say('OTTOLINE', '...Seven years. Seven years, and a Wayfarer with a tin cup walks in and — ha. Of course it was a tin cup.'),
            say('OTTOLINE', 'Hold the Golden Cup a moment. Everybody should, once.'),
            { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 900 },
            nar('You lift the Golden Cup. The loft cheers. Somebody slurps, very loudly, in your honour.'),
            { op: 'giveItem', item: 'beacon_charge', count: 2 },
            { op: 'say', text: 'Got 2 BEACON CHARGES — the champion\'s purse!' },
          ],
        },
        { label: 'NOT TODAY', ops: [say('OTTOLINE', 'Nerve, Wayfarer. Come back when you\'ve got some. Or when you\'ve had nine coffees, which feels the same.')] },
      ],
    },
    say('OTTOLINE', 'Next year I\'ll have it back. Nerve, and a new grinder.', { if_flag: 'flag:brew_champion_beaten' }),
  ],
};

export const BREWFAIR_DIALOGUE: DialogueRegistry = {
  // the crowd
  'npc.brewfair_goer_a': [{ speaker: 'BOY', text: 'Mum said one cup. I said one cup at EVERY STALL. It\'s called a loophole.' }],
  'npc.brewfair_goer_b': [{ speaker: 'GIRL', text: 'In the Long Dusk you never know when you\'re meant to sleep. So I just don\'t! Thanks, fair!' }],
  'npc.brewfair_goer_c': [{ speaker: 'FARMER', text: 'Have you seen the queue for the Siphon Lab? My grandad\'s in it. He joined as a young man.' }],
  'npc.brewfair_goer_d': [{ speaker: 'LAMPLIGHTER', text: 'I don\'t even drink coffee. I just come for the smell. And the sense of danger.' }],
  'npc.brewfair_goer_e': [{ speaker: 'FEN-WADER', text: 'I\'ve had four. I can hear colours. Is that normal? Don\'t answer. I can SEE your answer.' }],
  'npc.brewfair_goer_f': [{ speaker: 'MINER', text: 'Free samples! Every stall! I\'m not even thirsty! I\'m just completely unable to refuse!' }],
  'npc.brewfair_goer_g': [{ speaker: 'BUYER', text: 'I\'m a buyer. I\'m buying everything. I\'ve rather lost track of what money is.' }],
  'npc.brewfair_goer_h': [{ speaker: 'KNITTER', text: 'Trade only, up here. I told him I was trade. I\'m a knitter. Nobody checked.' }],

  'sign.brewfair_poster': [
    { text: 'THE WAKEFUL FAIR — every brewer in Vesperholm, under one roof of canvas. FREE SAMPLES AT EVERY STALL. Bring your own cup.' },
    { text: 'Underneath, smaller: "The fair accepts no responsibility for anything you see after your ninth."' },
  ],
  'sign.brewfair_record': [
    { text: 'A chalkboard: TODAY\'S SPECIALS — EVERYTHING. And under it: MOST SAMPLES IN ONE VISIT — P. (tin cup) — 23.' },
    { text: 'Somebody has drawn a little smiling urn next to the number.' },
  ],
  'sign.brewfair_trade_only': [
    { text: 'A chalk board by the stair: ROASTERS\' LOFT — TRADE ONLY. "If you have to ask, you\'re not talking fast enough."' },
  ],
  'sign.brewfair_aboard': [
    { text: 'A chalk board: TODAY — SIXTEEN STALLS. FREE SAMPLES. PLEASE KEEP MOVING. PLEASE DO NOT CLIMB IN THE URN.' },
  ],
  'sign.brewfair_water': [
    { text: 'The water table. A jug of water, a stack of cups, and absolutely no queue at all.' },
  ],
  'sign.brewfair_plaque': [
    { text: 'A brass plaque with a tin cup engraved on it: THE CUP RECORD. P. — TWENTY-THREE SAMPLES. "He said the urn laughed."' },
  ],
  'sign.brewfair_cot': [
    { text: 'A canvas camp-cot with a folded blanket. It\'s seen things. Mostly people staring at the ceiling, very fast.' },
  ],
  'sign.brewfair_roaster': [
    { text: 'The big drum roaster turns and turns, warm as a hearth. The beans go in green and come out the colour of the Long Dusk.' },
  ],
  'sign.brewfair_trophy': [
    { text: 'THE GOLDEN CUP. A coffee cup, but gold. But enormous. The plinth lists seven years of the same name: O. CREMA.' },
  ],
  'sign.brewfair_dream_door': [
    { text: 'A door, on its own, standing in the foam. It leads back to the fair. It looks a little embarrassed to be here.' },
  ],
};
