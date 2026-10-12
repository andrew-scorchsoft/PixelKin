/**
 * THE WILD WAYS (2026-10, docs/world/walkthrough/09-the-wild-ways.md §C2) — the
 * Reckoning-Works and its side quest "The Long Way Round".
 *
 * A brass-and-punch-card works on the Rimeway Fold, where clerks and their kin run
 * calculating engines that compute the STAR-TABLES (when each lamp wants trimming,
 * where each constellation rises). For eleven winters no tender has come up the
 * road for them (the Dusk; the Rime Gate barred) — and nobody stopped making them.
 * The engines run faster every winter; the output board climbs; the tables stack
 * unread. The clerks' VALUES (care, precision, pride in the craft) are good and stay
 * intact; what they have lost is the why. You tell them about Paul (S4/S5), the old
 * man who wanders and is never lost; one by one they go for a walk, each comes back
 * with something, the engines make something new — and the tables are still exact.
 *
 * This lane OWNS this file: new scripts + dialogue only, spread into the registries
 * via regions/index.ts (a ref here must be NEW, never an override).
 *
 * Flags this file owns:
 *   flag:q_works_begun     met Overseer Ketterly (or Nib) — JOURNAL start
 *   flag:works_met_ketterly  Ketterly's first brush-off has played
 *   flag:q_works_nib       Nib the apprentice offered you the floor
 *   flag:q_works_story     you told them about Paul; the clerks went wandering
 *   flag:works_found_nib / _hollis / _teague / _brann   each wanderer found + heard
 *                          (Nib: the star-room window; Hollis: Pale Vault's west ledge;
 *                          Teague: the Ascent's shelf 2; Brann: the Fold's lower plateau)
 *   flag:works_all_found   all four found (set by Ketterly's tally chain)
 *   flag:q_works_done      the engines play the aurora; the board is chalked anew
 * Reads: flag:q_south_booji_met (you've met Paul), flag:q_south_wander_done (S5 — you
 *   walked his wood), flag:rime_gate_open (the rime-lamps are lit), gleam:frost.
 *
 * NB: the S5 waystone's quoted line is the ONE sanctioned verbatim quote in the game —
 * nothing here quotes or paraphrases it. These words are the works' own.
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const BEGUN = 'flag:q_works_begun';
const MET_K = 'flag:works_met_ketterly';
const NIBF = 'flag:q_works_nib';
const STORY = 'flag:q_works_story';
const DONE = 'flag:q_works_done';
const ALL = 'flag:works_all_found';
const F_NIB = 'flag:works_found_nib';
const F_HOL = 'flag:works_found_hollis';
const F_TEA = 'flag:works_found_teague';
const F_BRA = 'flag:works_found_brann';
const MET_PAUL = 'flag:q_south_booji_met';
const WALKED_WOOD = 'flag:q_south_wander_done';
const LAMPS_LIT = 'flag:rime_gate_open';

export const RECKONWORKS_SCRIPTS: ScriptRegistry = {
  // ---- Overseer Ketterly (the office, across her desk) ---------------------------
  'script.works_ketterly': [
    { op: 'run', ref: 'script.works_k_after', if_flag: DONE },
    { op: 'run', ref: 'script.works_k_wait', if_flag: STORY, unless_flag: DONE },
    { op: 'run', ref: 'script.works_k_busy', unless_flag: STORY },
  ],
  'script.works_k_busy': [
    { op: 'say', speaker: 'KETTERLY', unless_flag: MET_K, text: 'A visitor. Unscheduled. Ketterly — overseer of the Reckoning-Works. Mind the belt on your way out. It doesn\'t stop for anyone.' },
    { op: 'say', speaker: 'KETTERLY', unless_flag: MET_K, text: 'We compute the star-tables. Which lamp wants trimming when, which constellation rises where — to the minute, for every tender in the North.' },
    { op: 'say', speaker: 'KETTERLY', unless_flag: MET_K, text: 'Output is up a ninth on last winter. Up a ninth on the winter before that. The board is very clear.' },
    { op: 'say', speaker: 'KETTERLY', unless_flag: MET_K, text: 'Who reads them? ...The board is very clear on how MANY. That\'s the part one can measure. Good day.' },
    { op: 'say', speaker: 'KETTERLY', if_flag: MET_K, text: 'Still here? The board\'s climbing. I\'d hate for you to miss it.' },
    { op: 'setFlag', flag: BEGUN },
    { op: 'setFlag', flag: MET_K },
  ],
  // after the story: count who's home (the AND of four flags, as a nested chain)
  'script.works_k_wait': [
    { op: 'run', ref: 'script.works_k_tally_1', if_flag: F_NIB },
    { op: 'run', ref: 'script.works_k_finale', if_flag: ALL },
    { op: 'run', ref: 'script.works_k_notyet', unless_flag: ALL },
  ],
  'script.works_k_tally_1': [{ op: 'run', ref: 'script.works_k_tally_2', if_flag: F_HOL }],
  'script.works_k_tally_2': [{ op: 'run', ref: 'script.works_k_tally_3', if_flag: F_TEA }],
  'script.works_k_tally_3': [{ op: 'setFlag', flag: ALL, if_flag: F_BRA }],
  'script.works_k_notyet': [
    { op: 'say', speaker: 'KETTERLY', text: 'Half my floor has gone for a WALK. Do you know what that does to the board? ...It\'s stopped. The board has stopped. I have never once seen it stop.' },
    { op: 'say', speaker: 'KETTERLY', unless_flag: F_NIB, text: 'Nib went through my office to the old star-room. I didn\'t know that door still opened.' },
    { op: 'say', speaker: 'KETTERLY', unless_flag: F_HOL, text: 'Hollis said something about checking the weather "for the tables". All the way down to the Pale Vault, by the look of his boots.' },
    { op: 'say', speaker: 'KETTERLY', unless_flag: F_TEA, text: 'Teague went down the Rimeway after a Snowcune. Across the GLARE. In office shoes.' },
    { op: 'say', speaker: 'KETTERLY', unless_flag: F_BRA, text: 'And Brann is just outside, somewhere down the ladder on the Fold, standing very still. Listening, he says. To what, he didn\'t say.' },
    { op: 'say', speaker: 'KETTERLY', text: 'Bring them back. Or — don\'t. I haven\'t decided. Go and see what they\'re doing out there.' },
  ],
  'script.works_k_after': [
    { op: 'say', speaker: 'KETTERLY', text: 'Tables went down the road this morning. Hale wept on his rota. The Pale Vault watchers sent up a jar of honey and a very long letter about the ferns.' },
    { op: 'say', speaker: 'KETTERLY', text: 'Output is down a third. Accuracy: unchanged. Nobody on the floor has looked this awake in eleven winters. I\'ve stopped putting that on the board. I\'ve started putting it in the window.' },
  ],

  // ---- the finale (talk to Ketterly with all four found) ---------------------------
  'script.works_k_finale': [
    { op: 'say', speaker: 'KETTERLY', text: 'You. Come and look at this. ...No, properly — come and LOOK.' },
    { op: 'say', speaker: 'KETTERLY', text: 'They\'re all back. Hollis has an aurora. Teague has a dance — off a Snowcune, on the Glare, in office shoes. Brann has two notes. Nib has frost. I sent them for nothing, and they\'ve brought me a scrapbook.' },
    { op: 'say', speaker: 'KETTERLY', text: 'And now they want to feed it to the ENGINES.' },
    { op: 'musicFade', ms: 700 },
    { op: 'cameraFocus', to: { tx: 7, ty: 6 }, ms: 900 },
    { op: 'narrate', text: 'Out on the engine floor the clerks are at work: the same work, with the same care. Hollis punches the aurora into a card, three long folds and then a short one. Teague sets the belt to a hop, a hop, a long skid, a hop.' },
    { op: 'narrate', text: 'Brann tunes the card-drum to the lamp\'s two notes. Nib, very carefully, threads the first card through.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'shake', ms: 400, intensity: 0.002 },
    { op: 'narrate', text: 'The engines clatter. Stutter. Catch. And for the first time anyone in the works can remember, they are not counting.' },
    { op: 'music', key: 'reckoning-aurora' },
    { op: 'emote', actor: 'engine_chillpip', emote: 'music' },
    { op: 'emote', actor: 'engine_snowcune', emote: 'music' },
    { op: 'setFlag', flag: DONE },
    { op: 'narrate', text: 'On the output board, the tallies are wiped away. In their place, in chalk: an aurora across the top, frost-ferns in every corner, and a trail of small paw-prints along the bottom.' },
    { op: 'cameraReset', ms: 700 },
    { op: 'say', speaker: 'HOLLIS', text: 'And before anyone asks: I checked the tables. TWICE. Every lamp, every star, to the minute. Not one figure out.' },
    { op: 'say', speaker: 'KETTERLY', text: 'Of course they aren\'t. Same engines, same cards, same care. I\'d not have it any other way.' },
    { op: 'say', speaker: 'KETTERLY', text: 'Eleven winters we measured how fast we were going. Not once did anybody look up to see where.' },
    { op: 'say', speaker: 'KETTERLY', text: 'The tables go down the mountain again from tomorrow — Hale wants his rota, the Lumenaries want their nights. The margins go with them. Let whoever reads them wonder what the ferns are for.' },
    { op: 'say', speaker: 'KETTERLY', text: 'Your man Paul. If you see him, tell him the Reckoning-Works went for a walk. He\'ll know what that\'s worth. We\'re still working it out.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'aurora_card', count: 1 },
    { op: 'narrate', text: 'She hands you a punched card, still warm from the engine. Hold it to the light and the holes make the shape of the aurora. You got the AURORA CARD!' },
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: 800 },
    { op: 'say', speaker: 'KETTERLY', text: 'And 800 wicks. Filed as an unscheduled consultancy fee. Don\'t argue; it took me a whole afternoon to invent the column.' },
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'Received 2 BEACON CHARGES — "the engines\' spares", by the label.' },
  ],

  // ---- Nib, the apprentice (the first to listen) ----------------------------------
  'script.works_nib': [
    { op: 'run', ref: 'script.works_nib_after', if_flag: F_NIB },
    { op: 'run', ref: 'script.works_nib_ferns', if_flag: STORY, unless_flag: F_NIB },
    { op: 'run', ref: 'script.works_nib_jam', unless_flag: STORY },
  ],
  'script.works_nib_jam': [
    { op: 'narrate', unless_flag: NIBF, text: 'A young clerk in an apprentice\'s apron is feeding the same handful of cards into the belt, again and again. The engine spits them out. She feeds them back in.' },
    { op: 'say', speaker: 'NIB', unless_flag: NIBF, text: 'Sorry — sorry, I can\'t stop, this table\'s jammed. Same table. Hundredth time. It keeps coming out exactly the same as yesterday\'s.' },
    { op: 'say', speaker: 'NIB', unless_flag: NIBF, text: 'Overseer Ketterly says if it jams, run it faster. I\'ve run it faster. It\'s jammed faster.' },
    { op: 'say', speaker: 'NIB', unless_flag: NIBF, text: 'Can I ask you something? You\'ve been OUT there. Down the road and back, all of it. What\'s it LIKE?' },
    { op: 'setFlag', flag: BEGUN },
    { op: 'setFlag', flag: NIBF },
    { op: 'say', speaker: 'NIB', text: 'Everyone — stop a moment! The Wayfarer\'s going to tell us something that isn\'t a number.' },
    {
      op: 'choice',
      speaker: 'NIB',
      prompt: 'What will you tell them?',
      options: [
        { label: 'About Paul', ops: [{ op: 'run', ref: 'script.works_paul_story' }] },
        {
          label: 'A number',
          ops: [
            { op: 'narrate', text: 'You say: "Forty-two." Three clerks write it down. Brann underlines it twice. Nib looks very quietly let down.' },
            { op: 'say', speaker: 'NIB', text: '...Maybe something else? Next time?' },
          ],
        },
        {
          label: 'Not now',
          ops: [{ op: 'say', speaker: 'NIB', text: 'Oh. That\'s all right. The engines will still be going. They always are.' }],
        },
      ],
    },
  ],
  // the story of Paul — in the player's own words, never the waystone's
  'script.works_paul_story': [
    { op: 'narrate', text: 'The engines clatter on. You clear your throat and tell them anyway.' },
    { op: 'narrate', if_flag: MET_PAUL, text: '"Down on the Pearlmoor breakwater there\'s an old man called Paul. I\'ve met him. He keeps one lamp dark on purpose, lifts harbour-stones nobody else can shift, and answers every question with a better one."' },
    { op: 'narrate', unless_flag: MET_PAUL, text: '"Down on the Pearlmoor coast they talk about an old man called Paul. He keeps one lamp dark on the breakwater, on purpose, and lifts harbour-stones nobody else can shift."' },
    { op: 'narrate', text: '"Every evening he puts down whatever he\'s doing and goes for a walk. No map, no list, nowhere in particular. Up the hill. Into the trees. Out along the boards. Wherever his feet are curious."' },
    { op: 'narrate', text: '"Folk ask him if he ever loses his way. He laughs at them. He says you can\'t lose a way you weren\'t keeping to — and that the looking was the point all along."' },
    { op: 'narrate', text: '"And every time, he comes back with something. A question. A story. A joke he can\'t finish for laughing. Never anything you\'d have found by going faster."' },
    { op: 'narrate', if_flag: WALKED_WOOD, text: '"I followed him once, up into an old wood behind the quay. It was the long way round. It was the best way I\'ve ever been."' },
    { op: 'wait', ms: 400 },
    { op: 'say', speaker: 'HOLLIS', text: 'Walking. With no destination. ...Then how does he know when he\'s arrived?' },
    { op: 'say', speaker: 'TEAGUE', text: 'Sounds a very inefficient man.' },
    { op: 'say', speaker: 'BRANN', text: 'Ha! A walk. In the cold. On PURPOSE.' },
    { op: 'narrate', text: 'Nobody laughs after that. The belt runs on. Nib\'s jammed table comes out, for the hundred-and-first time, exactly the same.' },
    { op: 'emote', actor: 'clerk_hollis', emote: 'ellipsis' },
    { op: 'say', speaker: 'HOLLIS', text: '...I\'ll just. Check the weather. For the tables. It\'s a perfectly sound reason to go outside.' },
    { op: 'emote', actor: 'clerk_teague', emote: 'question' },
    { op: 'say', speaker: 'TEAGUE', text: 'There\'s a Snowcune that keeps hopping past the yard. Somebody ought to follow it. Er. Check on it.' },
    { op: 'say', speaker: 'BRANN', text: 'And somebody ought to see whether those old rime-lamps are still out on the Fold. For the record.' },
    { op: 'emote', actor: 'clerk_nib', emote: 'alert' },
    { op: 'say', speaker: 'NIB', text: 'Then I\'m going to open the shutters in the old star-room. The big window. Nobody\'s opened it since I came here.' },
    { op: 'fade', dir: 'out', ms: 500 },
    { op: 'sfx', key: 'world-door-open' },
    { op: 'setFlag', flag: STORY },
    { op: 'narrate', text: 'One by one, quietly, as though each had thought of it on their own, the clerks put down their cards and go out. From the office comes the sound of an overseer dropping her pen.' },
    { op: 'fade', dir: 'in', ms: 500 },
  ],
  'script.works_nib_ferns': [
    { op: 'narrate', text: 'Nib has the star-room\'s shutters open. Frost has grown across the old window in feathers and ferns, each one branching like a little tree.' },
    { op: 'say', speaker: 'NIB', text: 'Look at the frost. It does the same thing over and over — a line, then two lines off it, then two off each of those — and it never comes out the same twice.' },
    { op: 'say', speaker: 'NIB', text: 'That\'s what our engines do. Same steps, over and over. Only the engines always come out the same. ...I think the frost is the better engine.' },
    { op: 'say', speaker: 'NIB', text: 'And look past it. Up there. That\'s the Frost constellation. That\'s what our tables are FOR. I\'ve been tending it on paper for two winters and I didn\'t know which one it was.' },
    { op: 'say', speaker: 'NIB', if_flag: 'gleam:frost', text: 'It\'s lit, too. Somebody relit it. ...Was that YOU?' },
    { op: 'say', speaker: 'NIB', text: 'The others went further. Hollis said the weather, so — down to the Pale Vault, I\'d guess. Teague went after that Snowcune down the Rimeway. Brann\'s out on the Fold somewhere. Would you find them? I want to hear what they found.' },
    { op: 'setFlag', flag: F_NIB },
  ],
  'script.works_nib_after': [
    { op: 'say', speaker: 'NIB', unless_flag: DONE, text: 'I\'m drawing the ferns. Line, two lines, two lines each. Go and find the others — I\'ll keep the window.' },
    { op: 'say', speaker: 'NIB', if_flag: DONE, text: 'Ketterly put a stool by the window. Says we each take an hour a night up here now. It\'s on the rota. It\'s the only line on the rota nobody has to be reminded of.' },
  ],

  // ---- the wanderers, out in the North --------------------------------------------
  'script.works_wander_hollis': [
    { op: 'say', speaker: 'HOLLIS', text: 'Shh. No — it\'s fine, you can talk. I just didn\'t want to miss the next one.' },
    { op: 'narrate', text: 'Above the glacier the aurora hangs in long green folds, moving like something breathing in its sleep.' },
    { op: 'say', speaker: 'HOLLIS', text: 'I\'ve computed when it should be visible for eleven winters. To the minute. I have never once looked at it.' },
    { op: 'say', speaker: 'HOLLIS', text: 'It repeats, did you know? Not exactly. Three long folds, then a short one, then it sort of... changes its mind. You can\'t put that in a table. I tried. Twice. I want to try again.' },
    { op: 'say', speaker: 'HOLLIS', text: 'This Paul of yours — how far did he walk, exactly? ...No. Never mind. Never mind! I\'m learning.' },
    { op: 'say', speaker: 'HOLLIS', text: 'I\'ll take it back to the engines. Ketterly will say it isn\'t a figure. She\'ll be right. It\'s better than a figure.' },
    { op: 'setFlag', flag: F_HOL },
  ],
  'script.works_wander_teague': [
    { op: 'say', speaker: 'TEAGUE', text: 'Don\'t step on them! ...Sorry. Sorry. Look.' },
    { op: 'narrate', text: 'A Snowcune\'s track runs across the snow: hop, hop, a long skid, hop. It goes nowhere in particular, and takes its time about it.' },
    { op: 'say', speaker: 'TEAGUE', text: 'Hop, hop, skid, hop. It\'s a RHYTHM. I\'ve punched a thousand cards a day and never thought of them as anything but holes. But holes in a pattern are a tune, aren\'t they? Or a dance.' },
    { op: 'say', speaker: 'TEAGUE', text: 'I came down the Glare after it. In office shoes. I slid for about a week. Best thing I\'ve done in years.' },
    { op: 'say', speaker: 'TEAGUE', text: 'Tell Ketterly I\'m on my way. Tell her I\'m bringing a dance.' },
    { op: 'setFlag', flag: F_TEA },
  ],
  'script.works_wander_brann': [
    { op: 'narrate', text: 'Brann stands beside a rime-lamp with his eyes shut and his hat in his hands.' },
    { op: 'say', speaker: 'BRANN', text: 'Listen. ...No. LISTEN.' },
    { op: 'narrate', unless_flag: LAMPS_LIT, text: 'The wind comes across the Fold and through the dead lamp\'s empty cage, and the cold brass hums: one low note, then a higher one, over and over.' },
    { op: 'narrate', if_flag: LAMPS_LIT, text: 'The wind comes across the Fold and up through the lit lamp\'s chimney, and the warm brass hums: one low note, then a higher one, over and over.' },
    { op: 'say', speaker: 'BRANN', text: 'Forty years I\'ve worked that belt. Never came out of the door except to go home. And the lamps have been singing out here the whole time. Two notes. Like a question and its answer.' },
    { op: 'say', speaker: 'BRANN', text: 'Your fellow Paul. I\'d like to shake his hand. Then I\'d like to walk somewhere with him and not say anything at all.' },
    { op: 'say', speaker: 'BRANN', text: 'Right. Back to the belt. I\'ve got two notes to put in it.' },
    { op: 'setFlag', flag: F_BRA },
  ],

  // ---- the hall: clerks, kin, the board, the window, the stacks --------------------
  'script.works_hollis': [
    { op: 'say', speaker: 'HOLLIS', unless_flag: STORY, text: 'Can\'t talk. Column nine. If you need the way out, the door is behind you. Eleven paces. I counted them once. I count them every day, actually.' },
    { op: 'say', speaker: 'HOLLIS', if_flag: F_HOL, unless_flag: DONE, text: 'I\'m punching the aurora into a card. The engine keeps asking me for a number. I keep giving it a fold.' },
    { op: 'say', speaker: 'HOLLIS', if_flag: DONE, text: 'Accuracy: unchanged, perfect. Delight: up a very great deal. I\'ve started a column for it. Ketterly pretends not to read it.' },
  ],
  'script.works_teague': [
    { op: 'say', speaker: 'TEAGUE', unless_flag: STORY, text: 'Feeding the belt, feeding the belt. The Snowcune does the lifting; I do the worrying. ...Sorry, did you say something? I can\'t hear you over the output.' },
    { op: 'say', speaker: 'TEAGUE', if_flag: F_TEA, unless_flag: DONE, text: 'Hop, hop, skid, hop! I\'m teaching it to the belt. The cards come out in a little dance, and every single one of them is still exactly right.' },
    { op: 'say', speaker: 'TEAGUE', if_flag: DONE, text: 'We sent the Glare\'s tables down in the dance first. The ice-walkers will laugh. Then they\'ll trust them more, I think. Things made with care look made with care.' },
  ],
  'script.works_brann': [
    { op: 'say', speaker: 'BRANN', unless_flag: STORY, text: 'Forty years on this belt. Never missed a card. Never looked up, either. Don\'t need to, do I? Cards come in, cards go out.' },
    { op: 'say', speaker: 'BRANN', if_flag: F_BRA, unless_flag: DONE, text: 'Two notes. Low, then high. I\'ve put them on the card-drum. Don\'t tell Ketterly I\'m humming.' },
    { op: 'say', speaker: 'BRANN', if_flag: DONE, text: 'Sef out on the Fold reckons its whole population is Vaultclaws, Hale\'s lamp and himself. Never counted us. Fair enough. We never came out to be counted. We will now.' },
  ],
  'script.works_engine_kin': [
    { op: 'narrate', unless_flag: DONE, text: 'A kin turns the engine\'s crank with grim, round-eyed devotion. It has not looked up from the cards in a long, long time.' },
    { op: 'narrate', if_flag: DONE, text: 'The kin at the engine turns the crank in time to the music, swaying very slightly. It looks up at you, and then at the window.' },
  ],
  'script.works_board': [
    { op: 'narrate', unless_flag: DONE, text: 'THE OUTPUT BOARD. Columns of tallies, climbing. A brass marker at the top reads THIS WINTER: MORE. Under it, smaller, in much older chalk: FOR THE TENDERS. Somebody has nearly rubbed it out.' },
    { op: 'narrate', if_flag: DONE, text: 'THE OUTPUT BOARD, wiped and chalked anew: an aurora, frost-ferns, little paw-prints. In one corner, small and exact: TABLES CORRECT TO THE MINUTE. FOR THE TENDERS. AND FOR LOOKING UP.' },
  ],
  'script.works_window': [
    { op: 'narrate', unless_flag: STORY, text: 'A tall arched window, shuttered and furred with dust. Through a crack in the shutters, a thin slice of night sky.' },
    { op: 'narrate', if_flag: STORY, text: 'The star-window stands open. Frost-ferns grow across the panes, and beyond them is the whole of the northern sky.' },
  ],
  'script.works_stacks': [
    { op: 'narrate', unless_flag: DONE, text: 'Star-tables in twine-tied bundles, stacked to the rafters. The bottom bundle is dated eleven winters ago. Nobody came up the road for them after that, and nobody stopped making them.' },
    { op: 'narrate', if_flag: DONE, text: 'The bundles are being sorted at last, tied with fresh twine and labelled for the road down: HALE. PALE VAULT. THE LUMENARIES.' },
  ],
};

export const RECKONWORKS_DIALOGUE: DialogueRegistry = {
  'sign.reckoning_works': [
    { text: 'THE RECKONING-WORKS. Star-tables for every tender in the North, reckoned to the minute. (A newer plate, screwed beneath:) OUTPUT UP A NINTH. NO CALLERS.' },
  ],
};
