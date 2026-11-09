/**
 * Cutscene script registry — keyed by the `ref` cutscene/script triggers use
 * (EventTrigger.ref, e.g. 'script.intro_mentor'). Each is an ordered list of
 * CutsceneStep the CutsceneRunner interprets. Adding a scene is a data edit here.
 */
import type { CutsceneStep, ScriptRegistry } from './types';
import { OLDLIGHT_SCRIPTS } from './oldlight';
import { REGION_EXTRA_SCRIPTS } from './regions';
import { INTERLUDE_SCRIPTS } from './interludes';
import { KINCHAT_SCRIPTS } from './kinchatter';

// --- The netmender comes to YOU at the moor-gate (playtest 2026-10) ----------
// Players walked down the causeway to the chained gate and were told "not yet"
// from afar, then had to remember to go back up and talk to her. Now a step_on
// band across the causeway head (row 18, cols 24-25 — the only way to the gate)
// has her put down her nets and walk over: once before the Old Light (where the
// errand stands), and — the point of it — every time you come down holding her
// floats, when she hands the rope over there and then. She walks round by the
// causeway head (22,16) because (23,17) beside her is open water.
const NETMENDER_JEST = 'flag:q_south_jest_done';
const NETMENDER_BELL = 'flag:q_south_bell';
const NETMENDER_HAILED = 'flag:netmender_hailed';
function netmenderComesOver(actor: string, col: number, middle: CutsceneStep[]): CutsceneStep[] {
  return [
    { op: 'emote', actor, emote: 'alert' },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'say', speaker: 'NETMENDER', text: 'Hoi — Wayfarer! Hold up. Let an old woman catch you up.' },
    { op: 'move', actor, to: { tx: 22, ty: 16 } },
    { op: 'move', actor, to: { tx: col, ty: 16 } },
    { op: 'move', actor, to: { tx: col, ty: 17 } },
    { op: 'face', actor, facing: 'down' },
    ...middle,
    { op: 'move', actor, to: { tx: col, ty: 16 } },
    { op: 'move', actor, to: { tx: 22, ty: 16 } },
    { op: 'move', actor, to: { tx: 22, ty: 17 } },
    { op: 'face', actor, facing: 'down' },
  ];
}
function netmenderHailScripts(): ScriptRegistry {
  const out: ScriptRegistry = {};
  for (const col of [24, 25]) {
    const k = `script.netmender_hail_${col}`;
    out[k] = [
      { op: 'run', ref: `${k}_rope`, if_flag: NETMENDER_JEST },
      { op: 'run', ref: `${k}_first`, unless_flag: NETMENDER_JEST },
    ];
    // floats home: the rope changes keeping right here on the causeway
    out[`${k}_rope`] = netmenderComesOver('netmender_floats', col, [{ op: 'run', ref: 'script.netmender_rope' }]);
    // before the Old Light: she tells you where the errand stands — once
    out[`${k}_first`] = [
      { op: 'run', ref: `${k}_stage`, unless_flag: NETMENDER_HAILED },
      { op: 'setFlag', flag: NETMENDER_HAILED },
    ];
    out[`${k}_stage`] = [
      { op: 'run', ref: `${k}_pre`, unless_flag: NETMENDER_BELL },
      { op: 'run', ref: `${k}_floats`, if_flag: NETMENDER_BELL },
    ];
    out[`${k}_pre`] = netmenderComesOver('netmender_pre', col, [{ op: 'dialogue', ref: 'npc.netmender_gate' }]);
    out[`${k}_floats`] = netmenderComesOver('netmender_floats', col, [{ op: 'dialogue', ref: 'npc.netmender_floats' }]);
  }
  return out;
}
const NETMENDER_HAIL_SCRIPTS = netmenderHailScripts();

export const SCRIPTS: ScriptRegistry = {
  // --- The opening: the satchel errand at the Vesper Crossroads -----------------
  // C1 (walkthrough/01-south §2) is now a small LOOP, not a tile-touch: the north
  // gate-warden turns you back (it's dangerous out there), everyone points EAST to
  // Star-tender Fenn at the Crossroads waystone, Fenn has left his satchel on the
  // Tinderwick store counter (R8: and a courier has since carted it off to
  // Duskapple Orchard, west of the square — the keeper sends you on), and the
  // lamp-and-starter ceremony happens at the
  // waystone once you bring it out to him. Warm, unhurried, never a "Professor".

  // The north gate, pre-starter: the warden (posted in the gap at (14,1)) spots the
  // player on the open column (13,1), warns them off, and walks them back a step.
  // The trigger band is hidden_when 'flag:has_starter'; the warden swaps for a
  // well-wisher (gatewarden_post) the moment the Wayfaring begins.
  'script.gate_warden': [
    { op: 'emote', actor: 'gatewarden_pre', emote: 'alert' },
    { op: 'face', actor: 'gatewarden_pre', facing: 'left' },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Whoa, apprentice! No kin, no coast road. The grass is crawling with wild ones.' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Fenn\'s been asking for you. He\'s gone [[EAST]], to [[the Crossroads waystone]].' },
    { op: 'say', speaker: 'GATE-WARDEN', text: 'Go on. He had that look — the one that means it\'s YOUR turn.' },
    { op: 'move', actor: 'player', to: { tx: 13, ty: 3 } },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'gatewarden_pre', facing: 'down' },
  ],

  // The coast-keeper holds the top of Dimglass Coast I until the Beacon is lit
  // (gleam:ember): the flats beyond are Dimglass II's band (8-10) and the road to
  // Reyl, so a player who hasn't climbed the tower is turned back — kindly, and
  // told the next step. A pushback band (row 1, x6-8) + gated warps; the keeper stands
  // aside for good once the first Gleam is earned.
  'script.coast_keeper_gate': [
    { op: 'emote', actor: 'coast_keeper', emote: 'alert' },
    { op: 'move', actor: 'coast_keeper', to: { tx: 9, ty: 2 }, speed: 2 },
    { op: 'face', actor: 'coast_keeper', facing: 'left' },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'say', speaker: 'COAST-KEEPER', text: 'Hold up, apprentice! The lanterns on the flats won\'t answer an unproven lamp.' },
    { op: 'say', speaker: 'COAST-KEEPER', text: 'Light [[the Beacon]] on Tinderwick\'s bluff first. Then I\'ll wave you through.' },
    { op: 'say', speaker: 'COAST-KEEPER', text: 'Its door wants a wick-key. Ask [[the old lamplighter]], down the shore.', unless_flag: 'flag:has_beacon_wick' },
    { op: 'say', speaker: 'COAST-KEEPER', text: 'Got the wick-key? Then [[back south to Tinderwick]]. The Beacon\'s waiting.', if_flag: 'flag:has_beacon_wick' },
    { op: 'say', speaker: 'COAST-KEEPER', text: 'Gran\'s letter? It\'ll keep. Words travel better by Beacon-light.', if_flag: 'flag:q_south_letter', unless_flag: 'flag:q_south_letter_given' },
    { op: 'move', actor: 'player', to: { tx: 7, ty: 3 } },
    { op: 'face', actor: 'player', facing: 'down' },
    { op: 'move', actor: 'coast_keeper', to: { tx: 10, ty: 5 } },
    { op: 'face', actor: 'coast_keeper', facing: 'left' },
  ],

  // Crossing into the waystone plaza for the first time: Fenn hails the player
  // from across the clearing so there's no "who do I talk to?" beat to fumble.
  'script.fenn_wave': [
    { op: 'emote', actor: 'fenn_pre', emote: 'alert' },
    { op: 'cameraFocus', actor: 'fenn_pre', ms: 500 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Ho — over here, apprentice! By the waystone!' },
    { op: 'cameraReset', ms: 500 },
  ],

  // (The old north-marsh-road warning retired with the 2026-10 geometry fix — the
  // Coldfog Marches hang off Nightreach now; the Waykeeper's first-visit nudge
  // explains the Lantern-car instead: script.crossroads_car_intro, regions/south.ts.)

  // Fenn at the waystone: delight, then the small ask — his satchel, forgotten on
  // the Tinderwick store counter, with the whole Wayfaring packed inside it.
  'script.fenn_crossroads': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'There you are. The sky lost another light last night. I came to tend the waystone — and to wait for you.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Your Wayfaring begins today. All you need is right here in my—' },
    { op: 'emote', actor: 'fenn_pre', emote: 'sweat' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: '...my satchel. On the Tinderwick store counter. Old head.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Fetch it for me? [[Back west, to the Tinderwick store]].' },
    { op: 'setFlag', flag: 'flag:fenn_errand' },
  ],

  // The satchel on the courier's cart (an item_cache placement `fenn_satchel` in
  // duskapple_orchard — R8; it used to sit by the store counter. Appears once
  // Fenn asks, vanishes once taken).
  'script.take_satchel': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fenn_satchel', count: 1 },
    { op: 'say', text: "The Star-tender's satchel, heavier than it looks. Took FENN'S SATCHEL!" },
    { op: 'setFlag', flag: 'flag:has_satchel' },
  ],

  // The ceremony at the waystone: the satchel comes home, and out of it come the
  // two things every Wayfarer leaves with. The cosy bed holds; the grave notes ride
  // portraits, not music changes — warmth held, dread only in Fenn's face.
  'script.intro_mentor': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'My satchel — and my apprentice, on the same feet. A tidy omen.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Every Wayfarer leaves with two things. Both are in this bag.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'The first — a lamp, to carry the light home. Your vesperlamp.' },
    { op: 'action', actor: 'fenn_ready', action: 'gift' }, // X-2: he holds it out
    { op: 'action', actor: 'player', action: 'raiseLamp' }, // the lamp made physical
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.28, ms: 240 }, // a warm bloom as the lamp kindles
    { op: 'giveItem', item: 'vesperlamp', count: 1 },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 600 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: '[[Raise it to a weary wild kin]] and it coaxes them in to rest.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'And the second — a friend for the dark road. Choose.' },
    { op: 'giveStarter' },
    // X-2 (story panel §6.1): the gesture, acted not told — a pause and Fenn's small
    // nod over the new pair. No added page (the South rule: words, never count).
    { op: 'wait', ms: 400 },
    { op: 'action', actor: 'fenn_ready', action: 'bow' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Tend them, and they will tend you. Every Wayfaring begins at a crossroads.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Now [[catch a second friend]] in the verge grass by the north gate: tire a wild kin, then [[raise your LAMP]].' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Call at [[the store]]: the keeper has a Wayfarer\'s kit for you.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Then see [[Brisa at the Lumenary]], for your first Gleam.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Forget a word? Ask your lamp. It keeps a book of [[LORE]].' },
    { op: 'setFlag', flag: 'flag:has_vesperlamp' },
    { op: 'setFlag', flag: 'flag:has_starter' },
  ],

  // --- Onboarding: the optional "how it all works" tutorial --------------------
  // Two beats, both OPTIONAL colour fired by WorldScene's ENTRY_TUTORIALS hook
  // (the pendingReveal pattern), never on the progression path:
  //   1. script.tutorial_offer — on the very first arrival in Tinderwick (new game,
  //      pre-starter): a yes/no offer to explain the genre to a first-timer.
  //   2. script.catch_tutorial — walking the Lanternway home with your first kin:
  //      how the vesperlamp catches, leading into the lane's verge grass to try it.
  // Un-attributed narration: at game start no mentor is in town (Fenn is east at
  // the Crossroads), so the game speaks softly to a new Wayfarer.

  'script.tutorial_offer': [
    { op: 'narrate', text: 'A new Wayfaring begins. The town is quiet, and the whole dark sky is waiting.' },
    {
      op: 'choice',
      prompt: 'New to roads like this? Hear how it all works?',
      options: [
        {
          label: 'Yes — explain it',
          ops: [{ op: 'run', ref: 'script.tutorial_basics' }],
        },
        {
          label: "No — I'll find my way",
          ops: [
            { op: 'narrate', text: 'Good fortune, then. Your lamp\'s [[LORE]] book ([[pause menu]]) keeps the basics.' },
          ],
        },
      ],
    },
  ],

  // The genre in plain words — exactly the things a first-timer trips on: what kin
  // and battles ARE, that you grow stronger by battling weaker wild kin when you're
  // stuck, that beds under the glowing lanterns mend your team for free, and that
  // talking to folk is half the game.
  'script.tutorial_basics': [
    { op: 'narrate', text: 'The stars are going out: the Long Dusk. You set out to relight them.' },
    { op: 'narrate', text: 'On the road you\'ll befriend wild creatures: your [[KIN]]. They fight beside you.' },
    { op: 'narrate', text: 'Battles go in turns. Win, and your kin grow stronger and learn new moves.' },
    { op: 'narrate', text: 'Relight the eight [[GLEAMS]] the LAMPWARDENS keep, and dawn returns.' },
    { op: 'narrate', text: 'Keep losing? [[Train in grass you can win in]]. A few levels help a lot.' },
    { op: 'narrate', text: 'Kin weary? [[REST]]. A door under a glowing lantern has a free bed that heals them.' },
    { op: 'narrate', text: 'And [[talk to everyone]]. Folk point the way, and sometimes give gifts.' },
    { op: 'narrate', text: 'That\'s all. Fenn waits [[EAST, along the Lanternway]]. Go to him.' },
  ],

  // The lamp-catching lesson, fired as the player walks the Lanternway home with
  // their first kin. The lane's verge grass (low-level wild kin) is right ahead,
  // so the lesson lands a step before they can try it for real.
  'script.catch_tutorial': [
    { op: 'narrate', text: "A Wayfarer shouldn't walk alone for long. Time for your first catch." },
    { op: 'narrate', text: 'Can\'t just scoop up a wild kin. [[Tire it in battle]] — don\'t knock it out.' },
    { op: 'narrate', text: 'A hurt kin, or one lulled with DOZE or CHILL, is easier to coax in.' },
    { op: 'narrate', text: 'Then choose [[LAMP]] and throw. Three shakes and a click: it\'s chosen you.' },
    { op: 'narrate', text: 'Broke free? Wear it down and try again. A CHARGE makes it surer.' },
    { op: 'narrate', text: 'This lane\'s [[verge grass]] is full of gentle kin. Go and try your lamp.' },
  ],

  // (The first Gleam moved from the Lumenary hall to the BEACON TOP —
  // script.beacon_battle below; the hall now stages Brisa's quest beats.)

  // The Beacon's wick-tenders — SIGHT trainers on the stair floors.
  'script.beacon_keeper_a': [
    { op: 'say', speaker: 'TANSY', text: 'A climber! Brisa said the key might come home. Every flame is tested.' },
    { op: 'battle', trainer: 'beacon_keeper_a' },
    { op: 'say', speaker: 'TANSY', text: 'Steady enough for the stairs. Up you go!' },
    { op: 'setFlag', flag: 'flag:beacon_keeper_a_beaten' },
  ],
  'script.beacon_keeper_b': [
    { op: 'say', speaker: 'COLE', text: 'Tansy let you past? One test left, and mine\'s not so gentle.' },
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
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'On foot, eh? Good. The light should be free to all.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'Read the water with me. Let\'s see if the sea listens to you.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'Eleven winters of jokes. Do I remember the other thing?', if_flag: 'flag:q_south_jest_done' },
    { op: 'battle', trainer: 'lampwarden_pearlmoor' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'proud', text: 'Well rowed. ...She\'d have heckled me rotten for that last switch.', if_flag: 'flag:q_south_jest_done' },
    // The second Gleam, wrapped in the Tide-blessing — same minor→major payoff, in a
    // cool moon-on-water key rather than Tinderwick's ember-warm one.
    { op: 'musicFade', ms: 500 },
    { op: 'action', actor: 'player', action: 'raiseLamp' }, // X-2: every lighting, the lamp raised
    { op: 'tint', color: '#4fb4ff', alpha: 0.36, ms: 600 },
    { op: 'narrate', text: 'Reyl rings the moor-bell. Out on the black water, buoy after buoy answers — and overhead, the Tide remembers how to shine.', unless_flag: 'flag:q_south_jest_done' },
    { op: 'narrate', text: 'Reyl walks out to the moor-bell for the first time in eleven winters. He doesn\'t hurry. He rings it anyway.', if_flag: 'flag:q_south_jest_done' },
    { op: 'narrate', text: 'Out on the black water, buoy after buoy answers — and overhead, the Tide remembers how to shine.', if_flag: 'flag:q_south_jest_done' },
    { op: 'gleam', element: 'tide' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'proud', text: 'The Tide Gleam stands over Pearlmoor again. And the [[Tidecall]] is yours — go on, [[ask the shallows to part]].' },
    { op: 'action', actor: 'player', action: 'bow' },
  ],

  // --- The Causeway Bell (Pearlmoor's earned second Gleam; spine §5 shape #2) --
  // The Tide-blessing cannot begin until the Moor-bell rings, and the bell-rope
  // is in the netmender's keeping: Reyl's hook (hall) -> the net-floats errand
  // (Dimglass II) -> the rope -> the breakwater walk -> the bell. All data.
  'script.reyl_quest': [
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'The new Ember\'s apprentice. I\'ll test you once the moor-bell rings.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'grave', text: 'It\'s hung silent since a storm took its rope. No bell, no bond-test.' },
    // R9: the Old Light slots in between the hook and the rope.
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'proud', text: 'House rule: nobody fights me till they\'ve LAUGHED. [[Climb the Old Light]], past the west beach.' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'Tell it Reyl sent you. Then [[the NETMENDER]] has the rope.' },
    { op: 'wait', ms: 700 }, // X-2: honour the ellipsis
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: '...I\'d come with you. I don\'t go up there.' },
    { op: 'setFlag', flag: 'flag:q_south_bell' },
  ],

  // Leaving the hall before he's given you the errand (playtest 2026-10: the
  // walk-up line read as the conversation, so a player left without the quest
  // and found the Old Light locked). He calls you back and gives it there.
  // Softlock-proof by construction: both of Reyl's walk-on steps (aisle + door)
  // END by setting flag:q_south_bell, which hides both triggers, so the door
  // tile frees itself the moment the scene ends. A save already past the bell
  // (any older ordering) skips the speech and just banks the flag.
  'script.reyl_call_back': [
    { op: 'run', ref: 'script.reyl_call_back_talk', unless_flag: 'flag:q_south_bell_rung' },
    { op: 'setFlag', flag: 'flag:q_south_bell' },
  ],
  'script.reyl_call_back_talk': [
    { op: 'emote', actor: 'reyl_quest', emote: 'alert' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'Hoi — Wayfarer! Not so fast. Hear me out before you go.' },
    { op: 'run', ref: 'script.reyl_quest' },
  ],
  'script.reyl_hook_step': [
    { op: 'run', ref: 'script.reyl_quest', unless_flag: 'flag:q_south_bell_rung' },
    { op: 'setFlag', flag: 'flag:q_south_bell' },
  ],
  // Reyl mid-quest (the hall stage between the hook and the bell) — one line per
  // state of the R9 chain: the tower, then the netmender, then the moor-gate.
  'script.reyl_waiting': [
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'Been up [[the Old Light]]? Past the west beach. Hear it cackling?', unless_flag: 'flag:q_south_jest_done' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'No hurry. Tides go out so they can come back.', unless_flag: 'flag:q_south_jest_done' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'You went up. I heard it laugh — differently. See [[the netmender]].', if_flag: 'flag:q_south_jest_done', unless_flag: 'flag:q_south_has_rope' },
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'neutral', text: 'Rope on your shoulder. Good. [[The moor-gate]]: south end of the quay.', if_flag: 'flag:q_south_has_rope' },
  ],
  // Reyl after the Gleam — his hall lines, then (once, with the toy) the Tin
  // Rower recognition beat (script.reyl_tin_rower, authored with the Tin Rower).
  'script.reyl_after': [
    { op: 'dialogue', ref: 'npc.reyl_after' },
    { op: 'run', ref: 'script.reyl_tin_rower' },
  ],

  // The netmender between Reyl's hook and the rope (one quay placement): before
  // the Old Light she points up the tower; after it, the floats come home and
  // the rope changes keeping.
  'script.netmender_floats': [
    { op: 'dialogue', ref: 'npc.netmender_floats', unless_flag: 'flag:q_south_jest_done' },
    { op: 'run', ref: 'script.netmender_rope', if_flag: 'flag:q_south_jest_done' },
  ],
  // The netmender, floats home: the rope changes keeping (her swap stage runs this).
  // R9: her stage now waits on flag:q_south_jest_done (the Old Light's top) — an
  // old save already holding the floats still climbs the tower first.
  'script.netmender_rope': [
    { op: 'say', speaker: 'NETMENDER', text: 'My floats! Every one SOUND. Out of that brass magpie\'s gob, were they?' },
    { op: 'say', speaker: 'NETMENDER', text: 'He sent you up the Old Light, didn\'t he. ...Good. About time somebody did.' },
    { op: 'say', speaker: 'NETMENDER', text: 'Then the rope is yours. I\'ve waited on steady hands since the bell went quiet.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bell_rope', count: 1 },
    { op: 'say', text: 'Salt-stiff rope, coiled in your arms. Received the MOOR-BELL ROPE!' },
    { op: 'say', speaker: 'NETMENDER', text: '[[The moor-gate]]\'s open, [[south end of the quay]]. Hang the rope and ring it LOUD.' },
    { op: 'say', speaker: 'NETMENDER', text: 'Mind Maren and Cob on the causeway. Bored net-hands; they\'ll want a bout.' },
    { op: 'setFlag', flag: 'flag:q_south_has_rope' },
  ],

  // The breakwater's two net-hand SIGHT trainers (the 12->14 on-ramp to Reyl's 16).
  'script.net_hand_a': [
    { op: 'say', speaker: 'MAREN', text: 'Hold it, rope-runner! Every lamp on the moor-boards gets weighed.' },
    { op: 'battle', trainer: 'net_hand_a' },
    { op: 'say', speaker: 'MAREN', text: 'Weighed and found steady. The bell\'s waited longer than you — get on.' },
    { op: 'setFlag', flag: 'flag:net_hand_a_beaten' },
  ],
  'script.net_hand_b': [
    { op: 'say', speaker: 'COB', text: 'Oi! Nobody rings MY bell without ringing me first. Nets up, Wayfarer!' },
    { op: 'battle', trainer: 'net_hand_b' },
    { op: 'say', speaker: 'COB', text: 'Hah — well hauled! Ring it loud; Maren bet me a week\'s mending you can\'t.' },
    { op: 'setFlag', flag: 'flag:net_hand_b_beaten' },
  ],

  // The Moor-bell, rung at the shrine — the loop's payoff and the blessing's first
  // note. Quiet -> the bell -> the harbour answering: a small minor->major of its
  // own (the full festival swell waits on the Gleam; docs/world/cinematics.md).
  'script.ring_moorbell': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 500 },
    { op: 'silence', ms: 900 }, // the held breath before the bell
    { op: 'narrate', text: 'You hang the netmender\'s rope, take it in both hands — and pull.' },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.3, ms: 500 },
    { op: 'narrate', text: 'The moor-bell swings. Once. Twice. The sound rolls out flat and silver over the black water, as it has not in years.' },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'narrate', text: 'And the harbour ANSWERS. Lanterns kindle along the quay, buoy by buoy — and among the boats, somebody starts the going-out song.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'Far back on the quay, an old man takes off his hat.', if_flag: 'flag:q_south_jest_done' },
    { op: 'narrate', text: 'The Tide-blessing has begun. [[Reyl Wash]] waits at his [[sea-altar]].' },
    { op: 'musicCrossfade', key: 'pearlmoor-quay-b', ms: 900 },
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
    { op: 'narrate', text: 'At the breakwater\'s end the moor-bell swings again — and new in the sky, the TIDE hangs over its own reflection.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.32, ms: 700 },
    { op: 'musicCrossfade', key: 'pearlmoor-blessing', ms: 1200 },
    { op: 'narrate', text: 'The blessing-boats put out in a lantern-line. The whole quay sings the going-out song, and it is not at all sad.' },
    { op: 'say', speaker: 'QUAY ELDER', text: 'Tides go out so they can come back. Sing it home, child. Tonight YOU kept its rhythm.' },
    { op: 'say', speaker: 'PUNCHWHEEL', text: '(faintly, down a speaking-tube from the Point) NEW MATERIAL. FINALLY.', if_flag: 'flag:q_south_jest_done' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 1100 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // S1 "The Last Buoy Out" — the netmender, once the Tide stands and the player
  // can walk the water: three of her line went dark in the storm. Lit in order,
  // quay outward — the LAST buoy out is the one she frets for.
  'script.netmender_buoys': [
    { op: 'say', speaker: 'NETMENDER', text: 'Walking the moon-water now? Then I\'ve one more asking.' },
    { op: 'say', speaker: 'NETMENDER', text: 'Three of my buoys went dark [[on the flats south of here]]. Drowned wicks; you\'ll see.' },
    { op: 'say', speaker: 'NETMENDER', text: '[[Light them quay-outward]]: near, middle, then the LAST BUOY OUT.' },
    { op: 'setFlag', flag: 'flag:q_south_buoys' },
  ],
  // The three buoys (Dimglass II, Tidecall water) — small, quiet relights.
  'script.buoy_first': [
    { op: 'narrate', text: 'The near buoy rocks on its chain, wick drowned. You lend it your flame.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'It takes — a small, stubborn flame. One.' },
  ],
  'script.buoy_second': [
    { op: 'narrate', text: 'The middle buoy lists, full of storm-sand. You bail it and lend it your flame.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Two. The near buoy answers it across the water like a held note.' },
  ],
  'script.buoy_last': [
    { op: 'narrate', text: 'The last buoy out, first into every storm. Its glass is crazed.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.25, ms: 500 },
    { op: 'narrate', text: 'Three. The whole line stands lit, quay to open sea — a road of small lights for whoever the dark still holds.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 800 },
  ],
  'script.netmender_drift': [
    { op: 'say', speaker: 'NETMENDER', text: 'I watched. When the far one stood up in the dark, I sat down on a crab-pot.' },
    { op: 'say', speaker: 'NETMENDER', text: 'My gran tended that line. Here — this isn\'t payment. It\'s BELONGING.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'drift_charm', count: 1 },
    { op: 'say', text: 'A buoy-wick charm, smelling of the going-out song. Received the DRIFT CHARM!' },
    { op: 'say', speaker: 'NETMENDER', text: '[[Use it over open water]] and wild kin won\'t take you for a stranger.' },
    { op: 'setFlag', flag: 'flag:q_south_buoys_done' },
  ],

  // S2 "A Letter for Fenn" — Gran, after the omen: the game's first delivery
  // quest. Her shaken witness beat IS the hook (dread lands on a face, F2/G4).
  'script.gran_letter': [
    { op: 'say', speaker: 'GRAN', text: 'You felt it too? A star went dark, love. My fresh wick GUTTERED. Never, in forty years.' },
    { op: 'say', speaker: 'GRAN', text: 'I\'m not frightened. Just old enough to know that quiet.' },
    { op: 'say', speaker: 'GRAN', text: 'A favour, love: take this to old Fenn, on [[the tidal flats]] past the coast road.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fenn_letter', count: 1 },
    { op: 'say', text: 'She presses a wax-sealed letter into your hands. Received GRAN\'S LETTER!' },
    { op: 'say', speaker: 'GRAN', text: 'Ask him plain: is it coming HERE? And remember the face he makes.' },
    { op: 'setFlag', flag: 'flag:q_south_letter' },
  ],
  // Fenn takes the letter at his sky-watcher spot on the flats.
  'script.fenn_letter': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'A letter? For ME? Since I last forgot to write back, nobody has.' },
    { op: 'narrate', text: 'He reads it twice, and smiles at a line he does not share.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'Coming here? It is coming everywhere, child. That is why there are Wayfarers.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Tell her: "The lamps are in good hands. Some of them are even yours."' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'And the cart being late is NOT an omen. It is the axle.' },
    { op: 'setFlag', flag: 'flag:q_south_letter_given' },
  ],
  'script.gran_thanks': [
    { op: 'say', speaker: 'GRAN', text: '"...Some of them are even yours." That man. Sixty years, and he still answers fear with a WINK.' },
    { op: 'narrate', text: 'She laughs — properly — and the kitchen is warm again.' },
    { op: 'say', speaker: 'GRAN', text: 'Here, love. Walking fare, for a letter-carrier in cold boots.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Received 2 TALLOW BALMS and a WARM BALM!' },
    { op: 'say', speaker: 'GRAN', text: 'Off with you — the sky doesn\'t relight itself. And come home warm.' },
    { op: 'setFlag', flag: 'flag:q_south_letter_done' },
  ],

  // S3 "The Cavern Keeps a Light" — the old fisher at the quayside inn. The
  // wreck-lamp itself waits in Tideglass Cavern (Glimmerstep, East) — this is
  // the deliberate long-game promise; the trigger lands with that map.
  'script.fisher_wrecklamp': [
    { op: 'say', speaker: 'OLD FISHER', text: 'You\'re the one who rang the bell back. Then you\'re the one I\'ll tell it to.' },
    { op: 'say', speaker: 'OLD FISHER', text: 'Forty years back my boat sank, and the sea walked me into Tideglass Cavern. Dark — all but one light.' },
    { op: 'say', speaker: 'OLD FISHER', text: 'My own stern-lamp, wedged where she broke. I found my way out by it. I owe it a wick.' },
    { op: 'say', speaker: 'OLD FISHER', text: 'It\'ll have guttered. Learn the deep-walking art, [[reach Tideglass Cavern]], and light her again for me.' },
    { op: 'setFlag', flag: 'flag:q_south_wrecklamp' },
  ],
  'script.fisher_thanks': [
    { op: 'say', speaker: 'OLD FISHER', text: '...It burns? You stood under it and it BURNS?' },
    { op: 'narrate', text: 'He looks past you, at black water forty years gone, and nods once.' },
    { op: 'say', speaker: 'OLD FISHER', text: 'Then the debt\'s paid, and not by me. Here — she\'d want you to have this.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'wrecklight_charm', count: 1 },
    { op: 'say', text: 'Received the WRECKLIGHT CHARM!' },
    { op: 'setFlag', flag: 'flag:q_south_wrecklamp_done' },
  ],

  // Wrong-way warnings on Pearlmoor's two side roads (playtest 2026-10: a player
  // fresh off the Ember wandered east into the fen's 16+ kin and north up the
  // hill, with no word that both are for later). Optional colour, pre-Tide only.
  'script.fen_warden': [
    { op: 'run', ref: 'script.fen_warden_warning', unless_flag: 'gleam:tide' },
    { op: 'dialogue', ref: 'npc.fen_warden' },
  ],
  'script.fen_warden_warning': [
    { op: 'say', speaker: 'FEN-WARDEN', text: 'Fresh off the quay? [[Turn back a while]]. The fen\'s kin run well past Pearlmoor\'s.' },
    { op: 'say', speaker: 'FEN-WARDEN', text: 'You can\'t cross its channels yet either. Earn [[Reyl Wash\'s Tide]] first.' },
  ],
  // ...and he calls it out the first time you step in, so nobody has to think
  // to ask him (a step_on band across the fen's mouth, once per save).
  'script.fen_warning_step': [
    { op: 'emote', actor: 'fen_warden', emote: 'alert', unless_flag: 'gleam:tide' },
    { op: 'run', ref: 'script.fen_warden_warning', unless_flag: 'gleam:tide' },
    { op: 'setFlag', flag: 'flag:fen_warned' },
  ],
  'script.allotment_anth': [
    { op: 'dialogue', ref: 'npc.allotment_anth' },
    { op: 'say', unless_flag: 'gleam:tide', speaker: 'ANTH', text: 'The woods? Not yet, love. See [[Reyl Wash]] at the Lumenary first.' },
    { op: 'say', if_flag: 'gleam:tide', speaker: 'ANTH', text: 'The woods open for whoever the old man sends. He\'s [[out past the bell]].' },
  ],
  // S4 "The Booji-Wooji Man" — the Lifting House quest line. The quay's gym crew
  // each hold one piece of the old man; none of the pieces agree, and that is the
  // point. Mystery and non-conformance, never the Hollowing: Paul keeps one lamp
  // dark for company, not for a cause. Closure is a question, not an answer.
  // How to actually REACH Paul (playtest 2026-10: the crew all said "the
  // breakwater" and a player stood at the chained moor-gate with no idea the
  // rope comes from Reyl -> the Old Light -> the netmender). Every lifter who
  // sends you out there runs this; it speaks only while the rope isn't yours.
  'script.booji_gate_note': [
    { op: 'say', unless_flag: 'flag:q_south_has_rope', speaker: 'ANDY', text: '[[The moor-gate]]\'s chained; only [[the NETMENDER\'s rope]] opens it.' },
    { op: 'say', unless_flag: 'flag:q_south_bell', speaker: 'ANDY', text: 'See [[REYL WASH]] at the Lumenary. Do as he says; she\'ll give you the rope.' },
    { op: 'say', if_flag: 'flag:q_south_bell', unless_flag: 'flag:q_south_jest_done', speaker: 'ANDY', text: 'On it, then: [[up the Old Light]], out on the Point. Bring her what\'s up there.' },
    { op: 'say', if_flag: 'flag:q_south_jest_done', unless_flag: 'flag:q_south_has_rope', speaker: 'ANDY', text: 'Been up the Old Light? Take [[the netmender her floats]], up from the moor-gate.' },
  ],
  'script.booji_andy': [
    { op: 'say', speaker: 'ANDY', text: 'A Wayfarer! Mind the belt. I run, you know. Every OTHER dusk. The knee.' },
    { op: 'say', speaker: 'ANDY', text: 'You\'ll be here about the old man. Everyone is, eventually. PAUL.' },
    { op: 'say', speaker: 'ANDY', text: 'The quay calls him the BOOJI-WOOJI MAN. I asked what it meant. He asked what I thought. Still thinking.' },
    { op: 'say', speaker: 'ANDY', text: 'Eighty-something, and he still presses the stone SID can\'t budge. Don\'t tell Sid.' },
    { op: 'say', speaker: 'ANDY', text: 'The Wardens\' Registry WANTED him once. He\'ll tell me why over a cup, some night. There\'s never a cup.' },
    { op: 'say', speaker: 'ANDY', text: 'He spends evenings at the [[END of the breakwater]]. Ask [[ABDUL]] by the bikes, and SID downstairs.' },
    { op: 'run', ref: 'script.booji_gate_note' },
    { op: 'setFlag', flag: 'flag:q_south_booji' },
  ],
  'script.booji_abdul': [
    { op: 'say', speaker: 'ABDUL', text: '...You\'re after Paul, then.' },
    { op: 'narrate', text: 'He hangs his towel over the bars with more care than most give their names.' },
    { op: 'say', speaker: 'ABDUL', text: 'In two years he\'s told me four stories about himself. All different. All true. I can\'t explain that.' },
    { op: 'say', speaker: 'ABDUL', text: 'He asked me: do you carry your lamp, or does it carry you? I laughed. Then didn\'t sleep.' },
    { op: 'say', speaker: 'ABDUL', text: 'He walks the breakwater after dark. [[Sid]] saw him there — he\'s downstairs.' },
    { op: 'say', unless_flag: 'flag:q_south_has_rope', speaker: 'ABDUL', text: 'The moor-gate wants the netmender\'s rope. Reyl at the Lumenary starts you on that.' },
    // Any lifter can start you on Paul now (q_south_booji), so the order is free.
    { op: 'setFlag', flag: 'flag:q_south_booji' },
    { op: 'setFlag', flag: 'flag:q_south_booji_abdul' },
  ],
  'script.booji_sid': [
    { op: 'say', speaker: 'SID', text: '...' },
    { op: 'say', speaker: 'SID', text: '...Saw him at the breakwater\'s end. At a dark lamp. Not lighting it.' },
    { op: 'say', speaker: 'SID', text: 'Said the dark needs somewhere to sit too, or it gets ideas.' },
    { op: 'say', speaker: 'SID', text: '...Then he pressed the BIG mooring-stone. Set it down soft as a loaf. Go see him.' },
    { op: 'say', unless_flag: 'flag:q_south_has_rope', speaker: 'SID', text: '...Gate\'s chained. Netmender\'s rope. Reyl first.' },
    { op: 'narrate', unless_flag: 'flag:q_south_has_rope', text: 'For Sid, that\'s a speech. It means: see [[Reyl Wash]] about the netmender\'s rope.' },
    { op: 'setFlag', flag: 'flag:q_south_booji' },
    { op: 'setFlag', flag: 'flag:q_south_booji_sid' },
  ],
  // The meeting, out on the dark boards. Paul is OPTIONAL strength (route-class
  // bout, payout authored to 10-economy §4) and the reward is the folio — the
  // gift inside the gift. The Registry story is never confirmed. Ever.
  'script.booji_paul': [
    { op: 'narrate', text: 'Past the bell, one lamp stands dark. An old man leans on it like an old friend\'s shoulder.' },
    { op: 'say', speaker: 'PAUL', text: 'Evening. Or it would be, if evenings still happened. My gym tell you anything good?' },
    { op: 'say', speaker: 'PAUL', text: 'Don\'t believe the Registry story. ...Don\'t disbelieve it either. A story you can check is just paperwork.' },
    { op: 'say', speaker: 'PAUL', text: 'And no, not the Hollowing. They want the dark to WIN. I just think it deserves a chair at the table.' },
    { op: 'say', speaker: 'PAUL', text: 'My question, apprentice: all these folk relighting things — reasons, or memberships?' },
    { op: 'narrate', text: 'You open your mouth. You close it. The question starts moving the furniture.' },
    { op: 'say', speaker: 'PAUL', text: 'Ha. There it goes. Now, a bout. I\'m old: everything I still do, I do on purpose.' },
    { op: 'battle', trainer: 'breakwater_paul' },
    { op: 'say', speaker: 'PAUL', text: 'Good. GOOD. You fight like someone who hasn\'t decided who they are. Don\'t rush that.' },
    { op: 'say', speaker: 'PAUL', text: 'That bird-pig on my side? Not mine. It crows at a lamp I won\'t light. Tonight it fancied a look at YOU.' },
    { op: 'say', speaker: 'PAUL', text: 'I don\'t give things to whoever wants them. I give them to whoever will GET them.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'booji_folio', count: 1 },
    { op: 'say', text: 'A battered folio of impossible grinning figures. Received the BOOJI FOLIO!' },
    { op: 'say', speaker: 'PAUL', text: 'Folk before the Dusk knew the world\'s too odd to draw honestly, so they drew it odder.' },
    { op: 'say', speaker: 'PAUL', text: 'The Registry business? Over a cup of something. Some night.' },
    { op: 'narrate', text: 'There will never be a cup. You are fairly sure that is the point.' },
    // The invitation (owner, 2026-10): after the bout he tells you about his
    // house and asks you round — WHERE in a hint, and WHAT it takes as a riddle,
    // never the waystone's word itself.
    { op: 'say', speaker: 'PAUL', text: 'Come by the house sometime, up on the Rise past the wood and Rod\'s marrows. My granddaughter will talk your ear off.' },
    { op: 'say', speaker: 'PAUL', text: 'Mind, the wood\'s particular. Its stone wants the last word of an old line about wanderers — the one thing I\'ve never been.' },
    { op: 'say', speaker: 'PAUL', text: 'Ask me sometime if I ever get lost — once you\'ve more company in that lamp.' },
    { op: 'setFlag', flag: 'flag:q_south_booji_met' },
    // The Chickenpig is the S4 payoff and must never be missed: the first meeting
    // ends by pointing straight at it, with a plain now-or-later offer. "Later"
    // says exactly where it waits (the lamp menu + the lamp's foot re-offer it
    // forever; a failed catch is only a short battles-won cooldown).
    { op: 'say', speaker: 'PAUL', text: 'Oh — the bird-pig\'s at the lamp\'s foot, pretending to sleep. Waiting to be somebody\'s, I think.' },
    {
      op: 'choice',
      speaker: 'PAUL',
      prompt: 'Want to try waking it?',
      options: [
        { label: 'Wake it now', ops: [{ op: 'run', ref: 'script.booji_chickenpig' }] },
        {
          label: 'Later',
          ops: [
            { op: 'say', speaker: 'PAUL', text: 'It\'ll keep. Find me at this lamp whenever you\'re ready.' },
          ],
        },
      ],
    },
  ],
  // Paul's friendly REMATCH (the wren_rematch pattern): once you've met him,
  // talking to Paul at the dark lamp re-runs this bout, forever, never forced.
  // His real stones (no Chickenpig — that one fought the once). No flags, no gate.
  'script.booji_paul_rematch': [
    { op: 'say', speaker: 'PAUL', text: 'Still not telling. ...Back for the bout, not the cup? That one I can give.' },
    { op: 'battle', trainer: 'breakwater_paul_rematch' },
    { op: 'say', speaker: 'PAUL', text: 'Worth the walk, eh? Come back when the dark wants company. It usually does.' },
  ],
  // Rematch AFTER you've caught the Chickenpig — it walks with you now, so Paul
  // fields only his stones (breakwater_paul_rematch_post). Still re-runnable.
  'script.booji_paul_rematch_post': [
    { op: 'say', speaker: 'PAUL', text: 'The bird-pig\'s yours — you walk like someone judged by poultry. Just the stones today.' },
    { op: 'battle', trainer: 'breakwater_paul_rematch_post' },
    { op: 'say', speaker: 'PAUL', text: 'Give that rooster my regards. It won\'t understand them, and it\'ll be right not to.' },
  ],
  // Paul at the dark lamp, every visit AFTER the first meeting — a MENU, never a
  // forced fight. "Wake the bird-pig" runs the Chickenpig catch right here (no
  // round-trip needed); "A bout" is the opt-in rematch (with the Chickenpig while
  // it's still his, his stones once you've caught it); Cancel/"Step away" leaves.
  'script.booji_paul_lamp': [
    {
      op: 'choice',
      speaker: 'PAUL',
      prompt: 'Back at my lamp. What\'ll it be?',
      options: [
        {
          label: 'Wake the bird-pig',
          unless_flag: 'flag:chickenpig_caught',
          ops: [{ op: 'run', ref: 'script.booji_chickenpig' }],
        },
        {
          label: 'A bout',
          unless_flag: 'flag:chickenpig_caught',
          ops: [{ op: 'run', ref: 'script.booji_paul_rematch' }],
        },
        {
          label: 'A bout',
          if_flag: 'flag:chickenpig_caught',
          ops: [{ op: 'run', ref: 'script.booji_paul_rematch_post' }],
        },
        // S5 "Not All Who Wander": only ever reachable from HERE, so the quest
        // can't open before you've fought Paul — and it wants the bird-pig along.
        {
          label: 'Ever get lost?',
          unless_flag: 'flag:chickenpig_caught',
          ops: [{ op: 'run', ref: 'script.wander_paul_not_yet' }],
        },
        {
          label: 'Ever get lost?',
          if_flag: 'flag:chickenpig_caught',
          unless_flag: 'flag:q_south_wander',
          ops: [{ op: 'run', ref: 'script.wander_paul_hint' }],
        },
        // S7 "Just One More Cup": once the cup's yours, Paul tells you about the fair
        // (his own story — content/regions/brewfair.ts retells it)
        // the Booji-Wooji Man's milagro cards (content/milagros.ts): the box, any visit after the first
        {
          label: 'Your cards?',
          ops: [{ op: 'run', ref: 'script.paul_milagro_cards' }],
        },
        {
          label: 'Too much coffee?',
          if_flag: 'flag:q_south_wander_done',
          ops: [{ op: 'run', ref: 'script.brew_paul_story' }],
        },
        {
          label: 'Step away',
          ops: [{ op: 'say', speaker: 'PAUL', text: 'Aye. The dark keeps the bench warm. Mind how you go.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------------------
  // S5 "Not All Who Wander" — Paul's second story (post-S4, needs the Chickenpig).
  //
  // Paul walks a wood up the hill behind the quay, past Rod's allotment. Its
  // waystone carries a famous line with the last word worn away; typing it
  // (askName store:false) parts the trees. In the glade the stillness-omen
  // Omenire comes for the old man and the Chickenpig — the one kin that still
  // believes in morning — leads the fight (setLead + bossBattle). The payoff is
  // the long-promised CUP. The Registry story stays unconfirmed. Ever.
  //
  // NOTE: the waystone quotes J.R.R. Tolkien's "Not all those who wander are
  // lost" VERBATIM. That is the owner's deliberate call (the reference IS the
  // point); it is the one sanctioned exception to VISION.md's all-original-text
  // rule. Don't "fix" it into an original line.
  // ---------------------------------------------------------------------------
  'script.wander_paul_not_yet': [
    { op: 'say', speaker: 'PAUL', text: 'Lost? Never. Wandered? Constantly. There\'s a wood I walk.' },
    { op: 'say', speaker: 'PAUL', text: 'Ask again when that bird-pig\'s in your lamp. Where I walk, it\'ll want to come.' },
  ],
  'script.wander_paul_hint': [
    { op: 'say', speaker: 'PAUL', text: 'Lost? Never. Wandered? Every chance. You\'ll know this one. Everyone does.' },
    { op: 'say', speaker: 'PAUL', text: '"Not all those who wander are..."' },
    { op: 'narrate', text: 'He stops. He waits. He very obviously isn\'t going to finish it.' },
    { op: 'say', unless_flag: 'flag:q_south_wander_open', speaker: 'PAUL', text: 'Don\'t tell ME — tell the stone at the old wood, [[up the hill behind the quay]], past Rod\'s allotment.' },
    { op: 'say', unless_flag: 'flag:q_south_wander_open', speaker: 'PAUL', text: 'Say it right and the trees will part. Bring the bird-pig. See you in the middle.' },
    { op: 'say', if_flag: 'flag:q_south_wander_open', speaker: 'PAUL', text: 'Told the stone already? I can see it on you. Bring the bird-pig. See you in the middle.' },
    { op: 'sfx', key: 'world-door-open' },
    { op: 'narrate', text: 'He tips an imaginary cap and is off up the boards, far too briskly.' },
    { op: 'setFlag', flag: 'flag:q_south_wander' },
  ],
  // Wanderer Hob waits beside the wood's mouth until the trees part (2026-10
  // playtest: the gap said "no" and nobody said "come back later", so the wood
  // read as a dead end and was easy to forget). He names the CURRENT next step,
  // staged like the gate note, and the first meeting opens a journal entry so
  // the wood stays on the player's list until they can get in.
  'script.wander_hob_waiting': [
    { op: 'say', unless_flag: 'flag:q_south_booji_met', speaker: 'WANDERER HOB', text: 'Don\'t bother pushing. These trees only open for whoever [[the old man]] sends up.' },
    { op: 'say', unless_flag: 'gleam:tide', speaker: 'WANDERER HOB', text: 'He\'s on the breakwater, and that\'s chained. [[Win your Tide Gleam]] from Reyl Wash first.' },
    { op: 'say', if_flag: 'gleam:tide', unless_flag: 'flag:q_south_booji_met', speaker: 'WANDERER HOB', text: 'Got your Tide? Find him [[out past the bell]] and give him a bout.' },
    { op: 'say', unless_flag: 'flag:q_south_booji_met', speaker: 'WANDERER HOB', text: 'Come back once you\'ve fought him. I\'m not lost, mind. I\'m WAITING.' },
    { op: 'say', if_flag: 'flag:q_south_booji_met', speaker: 'WANDERER HOB', text: 'He\'s sent you! You look like someone given half a sentence.' },
    { op: 'say', if_flag: 'flag:q_south_booji_met', speaker: 'WANDERER HOB', text: 'Tell the stone the rest of it. Then we can both go in.' },
    { op: 'setFlag', flag: 'flag:wander_wood_seen' },
  ],
  // Walking into the closed gap: the trees answer, then Hob does.
  'script.wander_gap_blocked': [
    { op: 'narrate', text: 'The trees stand shoulder to shoulder, as if waiting to be told something.' },
    { op: 'emote', actor: 'hob_waiting', emote: 'alert' },
    { op: 'face', actor: 'hob_waiting', facing: 'up' },
    { op: 'run', ref: 'script.wander_hob_waiting' },
    // step back off the gap so sidling along it doesn't replay the scene
    { op: 'move', actor: 'player', to: { tx: 10, ty: 2 } },
  ],
  // The waystone at the wood's mouth (pearlmoor_allotment). Readable any time —
  // before the quest it's a tease; once Paul has sent you, it asks for the word.
  'script.wander_stone': [
    { op: 'narrate', text: 'An old waystone, furred with lichen. Words are cut deep into its face:' },
    { op: 'narrate', text: 'NOT ALL THOSE WHO WANDER ARE ____' },
    { op: 'narrate', unless_flag: 'flag:q_south_booji_met', text: 'The last word is worn away by many hands. Behind it, the trees stand close.' },
    // (2026-10) what opens it, as a pointer not an answer: the one who walks here
    { op: 'narrate', unless_flag: 'flag:q_south_booji_met', text: 'Somebody must know the rest. The quay says the old man at [[the breakwater\'s end]] walks here.' },
    { op: 'narrate', if_flag: 'flag:q_south_wander_open', text: 'The trees behind the stone stand apart now. The path through them is open.' },
    { op: 'narrate', if_flag: 'flag:q_south_booji_met', unless_flag: 'flag:q_south_wander_word', text: 'Worn smooth. You think of Paul\'s old line about wanderers, and touch the stone.' },
    {
      op: 'askName',
      if_flag: 'flag:q_south_booji_met',
      unless_flag: 'flag:q_south_wander_word',
      title: 'THE LAST WORD',
      fallback: '...',
      store: false,
      matches: [{ value: 'LOST', flag: 'flag:q_south_wander_word' }],
    },
    // Wrong word: gentle, retryable forever (the step guards key off the flag the
    // askName match would have set, so exactly one tail plays).
    { op: 'narrate', if_flag: 'flag:q_south_booji_met', unless_flag: 'flag:q_south_wander_word', text: 'Nothing. The stone is patient. (Paul said the word was the one thing he\'s never been.)' },
    // Right word, first time: the trees part (once — re-reads take the
    // "stand apart now" line above instead).
    { op: 'run', if_flag: 'flag:q_south_wander_word', unless_flag: 'flag:q_south_wander_open', ref: 'script.wander_trees_part' },
    { op: 'setFlag', if_flag: 'flag:q_south_wander_word', flag: 'flag:q_south_wander_open' },
    // (2026-10) beating Paul is enough to try the word; nobody has to have asked
    // him "Ever get lost?" first. With the bird-pig along, the stone starts S5
    // too (Paul moves up to the glade). Without it, Paul stays at his lamp so the
    // Chickenpig catch is never stranded, and his "Ever get lost?" starts S5.
    { op: 'run', if_flag: 'flag:q_south_wander_word', unless_flag: 'flag:q_south_wander', ref: 'script.wander_stone_start' },
  ],
  'script.wander_stone_start': [
    { op: 'setFlag', if_flag: 'flag:chickenpig_caught', flag: 'flag:q_south_wander' },
  ],
  // The trees part — split out so it plays once, right after the right word.
  'script.wander_trees_part': [
    { op: 'sfx', key: 'world-door-open' },
    { op: 'shake', ms: 400, intensity: 0.002 },
    { op: 'narrate', text: '...LOST. The word settles into the stone like a key. With a slow creak, the trees lean apart.' },
  ],
  // Paul in the glade: the duel and the cup. Re-runnable until won (a wipe is
  // the ordinary blackout; Paul just waits). setLead comes FIRST, so a player
  // who rested the Chickenpig in the Hearth is told before anything plays.
  'script.wander_glade': [
    { op: 'setLead', kin: 163, missingRef: 'npc.wander_chickenpig_missing' },
    { op: 'narrate', text: 'Grass rings one enormous old tree, an unlit lamp at its foot. Paul sits on a root as if it grew for him.' },
    { op: 'say', speaker: 'PAUL', text: '{name}. You found the word. Most say it like an apology. It isn\'t one.' },
    { op: 'say', speaker: 'PAUL', text: 'Not all those who wander are lost. Sixty-odd years I\'ve come up here not to be lost in.' },
    { op: 'say', speaker: 'PAUL', text: 'I\'ve brought the cup. Andy\'s been owed one for two years, and — ...Ah.' },
    { op: 'musicFade', ms: 900 },
    { op: 'silence', ms: 700 },
    { op: 'letterbox', on: true, ms: 500 },
    { op: 'tint', color: '#0b0820', alpha: 0.55, ms: 1200 },
    { op: 'narrate', text: 'The glade goes STILL, like a held breath. Above the old tree the stars go out, swallowed by a slow black disc ringed in cold silver.' },
    { op: 'say', speaker: 'PAUL', text: 'Omenire. The omen of everything going still. ...I think it\'s come for me.' },
    { op: 'say', speaker: 'PAUL', text: 'It just wants it all to STOP. Morning included.' },
    { op: 'shake', ms: 500, intensity: 0.004 },
    { op: 'narrate', text: 'Furious crowing from your lamp — and the Chickenpig is OUT, comb blazing, between the old man and the dark.' },
    { op: 'say', speaker: 'PAUL', text: 'HA! Of course. Go on, rooster. Tell it about stillness.' },
    { op: 'letterbox', on: false, ms: 300 },
    { op: 'bossBattle', kin: 113, level: 17 },
    { op: 'tint', color: '#ffe9a8', alpha: 0.35, ms: 600 },
    { op: 'narrate', text: 'The black disc comes apart into ordinary night. The Chickenpig CROWS.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'setFlag', flag: 'flag:q_south_wander_lamp' },
    { op: 'narrate', text: 'The old tree\'s lamp catches by itself — a warm, ridiculous, morning-coloured gold.' },
    { op: 'tint', color: '#ffe9a8', alpha: 0, ms: 1200 },
    { op: 'music', key: 'gleam-emotional' },
    { op: 'say', speaker: 'PAUL', text: 'I keep one lamp dark, for the dark\'s sake. Seems this one belongs to the bird. Fair\'s fair.' },
    { op: 'say', speaker: 'PAUL', text: 'Right. Where was I. The cup.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'paul_cup', count: 1 },
    { op: 'narrate', text: 'A dented tin cup, still warm, smelling of woodsmoke. Received PAUL\'S TIN CUP!' },
    { op: 'say', speaker: 'PAUL', text: 'That\'s the cup. The night? Still working on it. Ask about the Registry and I\'ll pour another.' },
    { op: 'giveItem', item: 'lumen_drop', count: 3 },
    { op: 'say', text: 'Received 3 LUMEN DROPS!' },
    { op: 'say', speaker: 'PAUL', text: 'For the bird. It fought like it\'s seen the dawn and wasn\'t impressed. You\'ve the morning covered.' },
    { op: 'setFlag', flag: 'flag:q_south_wander_done' },
  ],
  // Andy mid-trail (before you've met Paul): who to ask, and how to get out there.
  'script.booji_andy_wait': [
    { op: 'dialogue', ref: 'npc.booji_andy_wait' },
    { op: 'run', ref: 'script.booji_gate_note' },
  ],
  // Andy, once the cup exists. (Wraps his standing after-line.)
  'script.booji_andy_after': [
    { op: 'dialogue', ref: 'npc.booji_andy_after', unless_flag: 'flag:q_south_wander_done' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'ANDY', text: 'He came in with a CUP! Poured me something hot and sweet. Wouldn\'t say what.' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'ANDY', text: 'I asked about the Registry. He poured another. Best night of my life. Still know nothing.' },
  ],
  // The S4 epilogue: the Chickenpig (#163) — the only rooster in Vesperholm
  // that still believes in morning, asleep at the foot of the one lamp Paul
  // keeps dark. The Lampling set-piece pattern: interact trigger on the
  // breakwater (post-q_south_booji_done), legendaryBattle with a short
  // cooldown, if_flag colour after the catch. Paul's story IS the link: he
  // keeps the dark company, it keeps the dawn's — they get on.
  'script.booji_chickenpig': [
    { op: 'narrate', text: 'At the lamp\'s foot curls a cream pig with a rooster\'s red comb and green tail-sickles. Impossibly, both.' },
    { op: 'say', speaker: 'PAUL', text: 'The other reason I come out here. Only rooster in Vesperholm that still believes in morning.' },
    { op: 'say', speaker: 'PAUL', text: 'It won\'t follow me. It\'s waiting for someone who hasn\'t decided who they are. Wake it gently.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' }, // X-2: the lamp held out to it
    { op: 'legendaryBattle', name: 'chickenpig', kin: 163, level: 16, caughtFlag: 'flag:chickenpig_caught', cooldownBattles: 2, cooldownRef: 'npc.chickenpig_shy' },
    { op: 'emote', if_flag: 'flag:chickenpig_caught', actor: 'player', emote: 'heart' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', speaker: 'PAUL', text: 'Ha! When the dawn comes, that one gets to say it told us so. Let it see the sky.' },
    { op: 'narrate', if_flag: 'flag:chickenpig_caught', text: 'From your lamp comes half a crow, half a contented oink. Paul looks very pleased.' },
  ],
  // Rod is a quest STARTER too (any of Andy/Abdul/Sid/Rod opens Paul). His spiel
  // already points to Paul and seeds the Chickenpig, so talking to him sets the
  // quest-active flag. Single stage — he keeps his patter every visit.
  'script.booji_rod': [
    { op: 'say', speaker: 'ROD', text: 'YEAH! A hundred and twenty kilos, and I\'m SEVENTY-TWO. Nothing but a peanut.' },
    { op: 'say', speaker: 'ROD', text: 'I keep an allotment up the hill — marrows, leeks, a turnip that ought to pay rent.' },
    { op: 'say', speaker: 'ROD', text: 'My Anth says I love that allotment more than her. I say NO contest. ...I never say which way.' },
    { op: 'say', speaker: 'ROD', text: 'One thing I can\'t beat: the squirrels. I can press a mooring-block, and they still get my marrows.' },
    { op: 'say', speaker: 'ROD', text: 'You\'ll be after PAUL. He\'s [[out past the bell]], end of the breakwater, at a lamp he won\'t light.' },
    { op: 'say', unless_flag: 'flag:q_south_has_rope', speaker: 'ROD', text: 'Moor-gate\'s chained till you\'ve the netmender\'s rope. [[Reyl Wash]] sorts that.' },
    { op: 'say', speaker: 'ROD', text: 'Paul\'s got company at that lamp — something I\'ve no name for. Bring it home, if it\'ll have you.' },
    { op: 'say', if_flag: 'flag:q_south_wander', unless_flag: 'flag:q_south_wander_done', speaker: 'ROD', text: 'Up the hill? Through the gap behind the Lumenary. If Anth hands you a hoe, you hoe. That\'s the toll.' },
    { op: 'setFlag', flag: 'flag:q_south_booji' },
  ],
  'script.booji_andy_done': [
    { op: 'say', speaker: 'ANDY', text: 'You FOUND him? No — don\'t show me. He\'d never forgive me getting it second-hand.' },
    { op: 'say', speaker: 'ANDY', text: 'You asked about the Registry, and he answered with a question. Of course he did.' },
    { op: 'say', speaker: 'ANDY', text: 'Some people leave explanations. The Booji-Wooji Man leaves atmospheres.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: 'Received 2 TALLOW BALMS!' },
    { op: 'say', speaker: 'ANDY', text: 'For your trouble — I was saving them for the knee. The knee\'s a lost cause.' },
    { op: 'say', speaker: 'ANDY', text: 'Go back out to him sometime. He keeps queer company at that lamp. Go and SEE.' },
    { op: 'setFlag', flag: 'flag:q_south_booji_done' },
  ],

  // --- New Pearlmoor <-> Crossroads route (Wrackline Path / Sounding Cave /
  //     Lanternfall Road): sight-trainer beats + item caches ---
  'script.wrackline_drifter': [
    { op: 'say', speaker: 'DRIFTER OSK', text: 'Oi — down the wrackline! Hold up. Nobody crosses my stretch unbloodied.' },
    { op: 'battle', trainer: 'wrackline_drifter' },
    { op: 'setFlag', flag: 'flag:wrackline_drifter_beaten' },
  ],
  'script.lanternfall_warden': [
    { op: 'say', speaker: 'LAMP-KEEPER NELL', text: 'Hoi, traveller! Nobody walks my lit road untested. Lamps up!' },
    { op: 'battle', trainer: 'lanternfall_warden' },
    { op: 'setFlag', flag: 'flag:lanternfall_warden_beaten' },
  ],
  'script.pickup_wrackline_balm': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: 'A traveller\'s cache, snug in the verge. Received 2 TALLOW BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_wrackline_balm' },
  ],
  'script.pickup_sounding_amber': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Old resin, glowing. Received MOTH-AMBER! (Worth a fair purse.)' },
    { op: 'setFlag', flag: 'flag:picked_sounding_amber' },
  ],
  'script.pickup_lanternfall_charge': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'A waxed cell left trimmed and ready by a lampwright. Received a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_lanternfall_charge' },
  ],

  // A2 (Dimglass Coast I): Wren's first FRIENDLY trainer battle. Wren is a SIGHT
  // trainer — spots the player on the lane, runs up (the engine plays the alert +
  // approach), and this script carries the words + battle. Low-stakes by design.
  'script.wren_dimglass': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'There you are! I was starting to think the grass ate you.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: "Every Wayfarer's first proper battle should be with a friend. So?" },
    { op: 'battle', trainer: 'wren_dimglass' },
    // X-2: the laugh, then the wound — Wren turns away on "Mum" (no added page).
    { op: 'action', actor: 'wren', action: 'laugh' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Same road, different lamps. Mine goes north, to Mum\'s. Her letters have gone short. See you!' },
    { op: 'action', actor: 'wren', action: 'turnAway', holdMs: 700 },
    { op: 'setFlag', flag: 'flag:wren_dimglass_battled' },
  ],

  // B1 (Dimglass Coast I): the inciting incident — a far constellation winks out on the
  // first nightfall here. The dread is in the QUIET: letterbox in, fade the bed to
  // silence and hold, then the gutter sting + cold wash + shake as the star dies. This
  // is the first-hour's load-bearing foreboding beat (walkthrough/01-south; the
  // cinematic cadence is binding — see docs/world/cinematics.md).
  'script.dusk_begins': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'face', actor: 'player', facing: 'right' }, // X-2: you turn to the sea
    { op: 'silence', ms: 1200 }, // the held quiet before the light fails
    // The motif's debut: a cinder star streaks over the water as the line lands
    // (non-blocking colour — no added line or length; a no-op with motion off).
    { op: 'starfall', from: 'right' },
    { op: 'narrate', text: 'Far out over the water, a constellation flickers — and goes dark.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'tint', color: '#0b1026', alpha: 0.55, ms: 180 }, // the dark presses in
    { op: 'shake', ms: 320, intensity: 0.006 },
    { op: 'action', actor: 'player', action: 'shock' }, // X-2: the flinch, shown
    { op: 'narrate', text: 'For a heartbeat every lantern-buoy gutters, as if the sea itself flinched.' },
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 700 }, // your own small light held up against it
    { op: 'tint', color: '#0b1026', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'You think of the orchard\'s scorched ring. This one did not fall. Not yet.' },
    { op: 'musicCrossfade', key: 'dimglass-coast-a', ms: 900 }, // the bed returns, a shade uneasier
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // Dimglass Coast II route trainers (the XP bridge toward Pearlmoor's 12) —
  // SIGHT trainers: the engine plays the alert + walk-up, these carry the words.
  'script.flats_trainer_a': [
    { op: 'say', speaker: 'MORROW', text: 'Hold up there, Wayfarer! The flats test every lamp that crosses — mine first.' },
    { op: 'battle', trainer: 'flats_wayfarer_a' },
    { op: 'say', speaker: 'MORROW', text: 'Well fought. The dune grass ahead is lively — good for toughening up.' },
    { op: 'setFlag', flag: 'flag:flats_trainer_a_beaten' },
  ],
  'script.flats_trainer_b': [
    { op: 'say', speaker: 'ELSPETH', text: 'A letter-runner never passes a lamp without a bout. Rules of the road!' },
    { op: 'battle', trainer: 'flats_wayfarer_b' },
    { op: 'say', speaker: 'ELSPETH', text: 'Ha! Reyl Wash at Pearlmoor — now THERE\'s a battle worth the walk.' },
    { op: 'setFlag', flag: 'flag:flats_trainer_b_beaten' },
  ],

  // --- The Beacon quest (Tinderwick's earned first Gleam) ---------------------
  // Brisa sends the new Wayfarer up the coast road for the beacon's lost
  // wick-key before she'll hold the bond-test at the lantern.
  'script.brisa_quest': [
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'A first friend! Now, dear: [[fetch the Beacon\'s wick-key]]. The Ember is relit there.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: '[[The old lamplighter]] has it, on Dimglass Coast — past the north gate.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'Mind the grass, mind the dark — and come back stronger.' },
    { op: 'setFlag', flag: 'flag:beacon_quest' },
  ],
  // The old lamplighter (Dimglass I, appears after dusk_begins) hands the key. His
  // closing aside is the first-hour's quiet Hollowing SEED — a cold that "follows the
  // dark down off the north road" — foreboding only, no name, no fight (B2 still
  // introduces the Hollowing formally in East; see docs/world/cinematics.md §tone).
  'script.give_wick': [
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'grave', text: 'You saw it too. One breath there, the next a hole in the sky.' },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'neutral', text: 'Third this season. I\'m too old to climb the beacon. You are not.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_wick', count: 1 },
    { op: 'say', text: 'He presses a worn brass key into your hand. Received the BEACON WICK-KEY!' },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'grave', text: "Mind the north road. A cold follows the dark down it. Not weather." },
    { op: 'say', speaker: 'OLD LAMPLIGHTER', portrait: 'lamplighter', expr: 'neutral', text: 'Tell Brisa the road is darker. [[Take the key to the Beacon]].' },
    { op: 'setFlag', flag: 'flag:has_beacon_wick' },
  ],
  // The lantern room, beacon top: the bond-test, then the Ember Gleam relit FROM
  // THE TOWER — the first constellation answering the town's own light.
  'script.beacon_battle': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'brisa', facing: 'down' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'Up all those dark stairs, wick-key in hand. Well chosen.' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'This lantern lit the Ember for centuries. Can your flame wake it?' },
    { op: 'battle', trainer: 'lampwarden_tinderwick' },
    // The Gleam payoff: minor→major. Hold a beat of silence, the lantern blooms (warm
    // wash + the lamp sfx), the constellation answers (gleam sting + flash), then the
    // festival swell rises as the town below begins to dance (Arc E).
    { op: 'musicFade', ms: 500 },
    { op: 'emote', actor: 'brisa', emote: 'ellipsis' }, // X-2: a held breath at the key
    { op: 'action', actor: 'player', action: 'raiseLamp' }, // every lighting: the lamp raised
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.4, ms: 600 },
    { op: 'narrate', text: 'Brisa turns the wick-key. The lantern blooms — and far above, a warm light answers.' },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'gleam', element: 'ember' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 900 },
    { op: 'emote', actor: 'brisa', emote: 'heart' },
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'proud', text: 'The Ember burns again. Go down to the square, dear. The town wants to dance with you.' },
    { op: 'action', actor: 'player', action: 'bow' },
  ],

  // --- Rest points (the genre's heal loop, diegetic) -------------------------
  // The inn: a paid-in-kindness full rest. The innkeep NPC's dialogue_ref runs this.
  'script.inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'Rest your feet, Wayfarer — and your kin. The hearth\'s warm.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'Morning! Ever taken a virtuous day? Not ill — just virtuous to yourself.' },
    { op: 'say', speaker: 'INNKEEP', text: 'Lamps trimmed, kin bright-eyed. The dusk can wait on you a while.' },
  ],
  // Home: the bed in the apprentice's house. Free, always — home is home.
  'script.home_rest': [
    { op: 'say', text: 'Your own bed, under the old quilt. The lamp hums low...' },
    { op: 'heal' },
    { op: 'say', text: 'You wake warm. Your kin are rested and bright.' },
  ],
  // The roadside rest on the tidal flats (Dimglass Coast II, just past the seam
  // from Coast I): the South road's only heal between Tinderwick and Pearlmoor —
  // a cockler's driftwood fire. Banks the respawn point like any rest.
  'script.flats_rest': [
    { op: 'say', speaker: 'COCKLER', text: 'Long road from Tinderwick? Sit by the driftwood fire a while, dear.' },
    { op: 'heal' },
    { op: 'say', speaker: 'COCKLER', text: 'Warm through, the lot of you. Lamp low? Keep to the dry trail.' },
  ],

  // ---------------------------------------------------------------------------
  // R9 "THE TIN ROWER" — the nameless man's lot on Dimglass Coast I (he never
  // gives a name, and he's gone the moment the toy is yours).
  //
  // A wind-up tin ferryman, made to order for Tam Wash and never collected. He
  // set the auction reserve (12,000w) SPECIFICALLY not to be met — he'd rather
  // trade him for a story. Two ways to him:
  //   TELL A STORY — a three-pick story-builder (opening / middle / ending). Each
  //     pick sets a `flag:tin_story_*` (all cleared at the start) so he can
  //     read it back; the one "auction ending" (sealed in a glass case) is turned
  //     down and only the good endings are re-offered.
  //   BUY HIM — the `pay` op: a full purse pays and sets `flag:tin_rower_bought`;
  //     a short one is a silent no-op and the script branches on the flag.
  // Every give-step rides `script.wink_handover`, each guarded
  // `unless_flag: flag:has_tin_rower` (set LAST), so he can't be handed over twice.
  // The toy arrives already WOUND (flag:tin_rower_wound — ITEMS toggles it).
  // ---------------------------------------------------------------------------
  'script.wink_trade': [
    { op: 'emote', actor: 'wink', emote: 'alert', unless_flag: 'flag:tin_rower_offered' },
    { op: 'say', unless_flag: 'flag:tin_rower_offered', speaker: 'MAN WITH A CASE', text: "Names? No. Toys, tales, trades. Mind the case; it's older than me." },
    { op: 'say', unless_flag: 'flag:tin_rower_offered', speaker: 'MAN WITH A CASE', text: "Lot 1. Eleven winters at auction. I set the reserve NOT to be met." },
    { op: 'setFlag', unless_flag: 'flag:tin_rower_offered', flag: 'flag:tin_rower_offered' },
    // After the Old Light — he worked out whose order it was.
    { op: 'emote', if_flag: 'flag:q_south_jest_done', unless_flag: 'flag:wink_tam_told', actor: 'wink', emote: 'ellipsis' },
    { op: 'say', if_flag: 'flag:q_south_jest_done', unless_flag: 'flag:wink_tam_told', speaker: 'MAN WITH A CASE', text: 'Tam Wash. I think I knew. I just liked not knowing.' },
    { op: 'setFlag', if_flag: 'flag:q_south_jest_done', unless_flag: 'flag:wink_tam_told', flag: 'flag:wink_tam_told' },
    { op: 'run', ref: 'script.wink_menu', unless_flag: 'flag:has_tin_rower' },
  ],
  'script.wink_menu': [
    {
      op: 'choice',
      speaker: 'MAN WITH A CASE',
      prompt: 'Lot 1. One tin ferryman, working. What will it be?',
      options: [
        { label: 'TELL A STORY', ops: [{ op: 'run', ref: 'script.wink_story' }] },
        { label: 'BUY HIM (12,000W)', ops: [{ op: 'run', ref: 'script.wink_buy' }] },
        {
          label: "WHERE'S HE FROM?",
          ops: [
            { op: 'say', speaker: 'MAN WITH A CASE', text: "Made to order for a lady off Pearlmoor Quay. Paid half. Back 'when the fog lifts,' she said." },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '...Long fog.' },
          ],
        },
        { label: 'JUST LOOKING', ops: [{ op: 'say', speaker: 'MAN WITH A CASE', text: "Looking's free. Looking's the best bit. He's a ferryman — he's used to it." }] },
      ],
    },
  ],
  'script.wink_buy': [
    { op: 'say', speaker: 'MAN WITH A CASE', text: "Twelve thousand wicks. Sure? A story's free, and honestly? I'd rather." },
    {
      op: 'choice',
      speaker: 'MAN WITH A CASE',
      options: [
        {
          label: 'PAY 12,000W',
          ops: [
            { op: 'pay', amount: 12000, flag: 'flag:tin_rower_bought', unless_flag: 'flag:has_tin_rower' },
            { op: 'say', if_flag: 'flag:tin_rower_bought', unless_flag: 'flag:has_tin_rower', speaker: 'MAN WITH A CASE', text: 'Sold. To the Wayfarer with more wicks than sense. ...Kindly meant. Mostly.' },
            { op: 'run', ref: 'script.wink_handover', if_flag: 'flag:tin_rower_bought' },
            { op: 'say', unless_flag: 'flag:tin_rower_bought', speaker: 'MAN WITH A CASE', text: "Twelve thousand. ...Not quite. A story's free, and I'd rather." },
          ],
        },
        { label: 'TELL A STORY', ops: [{ op: 'run', ref: 'script.wink_story' }] },
        { label: 'NOT TODAY', ops: [{ op: 'say', speaker: 'MAN WITH A CASE', text: "Wise. He'll keep. He's kept eleven winters." }] },
      ],
    },
  ],

  // The story-builder. Picks set flags; a Cancel at any step ends the telling
  // (the next stage only runs once its `tin_story_has_*` marker is held).
  'script.wink_story': [
    { op: 'say', speaker: 'MAN WITH A CASE', text: 'Toys are stories you can hold. Tell me one: start, trouble, ending.' },
    { op: 'setFlag', flag: 'flag:tin_story_open_ferry', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_open_rooster', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_open_bun', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_mid_fog', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_mid_machine', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_mid_stranger', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_mid_nothing', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_end_home', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_end_light', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_end_wander', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_end_glass', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_has_open', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_has_mid', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_has_end', value: false },
    { op: 'setFlag', flag: 'flag:tin_story_special', value: false },
    {
      op: 'choice',
      speaker: 'MAN WITH A CASE',
      prompt: 'How does it START?',
      options: [
        {
          label: 'A ferryman',
          ops: [
            { op: 'setFlag', flag: 'flag:tin_story_open_ferry' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '"A ferryman who could read the weather but not his own face." Ooh. Go on.' },
          ],
        },
        {
          label: 'A hopeful rooster',
          ops: [
            { op: 'setFlag', flag: 'flag:tin_story_open_rooster' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '"A rooster who believed in morning when nobody else did." Brave bird. Go on.' },
          ],
        },
        {
          label: 'A huge cheese-bun',
          ops: [
            { op: 'setFlag', flag: 'flag:tin_story_open_bun' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '"Once, there was an enormous cheese-bun..." Wasn\'t ready for that. Go on.' },
          ],
        },
      ],
    },
    { op: 'setFlag', flag: 'flag:tin_story_has_open', if_flag: 'flag:tin_story_open_ferry' },
    { op: 'setFlag', flag: 'flag:tin_story_has_open', if_flag: 'flag:tin_story_open_rooster' },
    { op: 'setFlag', flag: 'flag:tin_story_has_open', if_flag: 'flag:tin_story_open_bun' },
    { op: 'run', ref: 'script.wink_story_mid', if_flag: 'flag:tin_story_has_open' },
    { op: 'say', unless_flag: 'flag:tin_story_has_end', speaker: 'MAN WITH A CASE', text: "Stories keep. Come back with an end — he's not going anywhere unwound." },
  ],
  'script.wink_story_mid': [
    {
      op: 'choice',
      speaker: 'MAN WITH A CASE',
      prompt: 'And what goes WRONG?',
      options: [
        {
          label: 'The fog came in',
          ops: [
            { op: 'setFlag', flag: 'flag:tin_story_mid_fog' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '"One night the fog came in and the bell went quiet." Hm. That does happen.' },
          ],
        },
        {
          label: 'A brass joke-machine',
          ops: [
            { op: 'setFlag', flag: 'flag:tin_story_mid_machine' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '"A brass machine told a joke, and they laughed till the sea went out." Lovely. Dangerous.' },
          ],
        },
        {
          label: 'An old stranger',
          ops: [
            { op: 'setFlag', flag: 'flag:tin_story_mid_stranger' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '"An old stranger pretended not to help — and helped all the way." Wears a hat, I expect.' },
          ],
        },
        {
          label: 'Nothing. For years.',
          ops: [
            { op: 'setFlag', flag: 'flag:tin_story_mid_nothing' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '"Nothing happened. For eleven years." ...Bold. True, too, for some of us.' },
          ],
        },
      ],
    },
    { op: 'setFlag', flag: 'flag:tin_story_has_mid', if_flag: 'flag:tin_story_mid_fog' },
    { op: 'setFlag', flag: 'flag:tin_story_has_mid', if_flag: 'flag:tin_story_mid_machine' },
    { op: 'setFlag', flag: 'flag:tin_story_has_mid', if_flag: 'flag:tin_story_mid_stranger' },
    { op: 'setFlag', flag: 'flag:tin_story_has_mid', if_flag: 'flag:tin_story_mid_nothing' },
    { op: 'run', ref: 'script.wink_story_end', if_flag: 'flag:tin_story_has_mid' },
  ],
  'script.wink_story_end': [
    {
      op: 'choice',
      speaker: 'MAN WITH A CASE',
      prompt: 'And how does it END?',
      options: [
        { label: 'They came home', ops: [{ op: 'run', ref: 'script.wink_end_home' }] },
        { label: 'A light kept on', ops: [{ op: 'run', ref: 'script.wink_end_light' }] },
        { label: 'Still wandering', ops: [{ op: 'run', ref: 'script.wink_end_wander' }] },
        {
          label: 'A glass case',
          ops: [
            { op: 'setFlag', flag: 'flag:tin_story_end_glass' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: '"...and it was sealed in a glass case, mint, and never walked again."' },
            { op: 'emote', actor: 'wink', emote: 'sweat' },
            { op: 'say', speaker: 'MAN WITH A CASE', text: "Ooh. That's the auction ending. That's the one I'm trying to spare him." },
            { op: 'say', speaker: 'MAN WITH A CASE', text: "Beginnings are the hard part, and you've done those. Try the end again?" },
          ],
        },
      ],
    },
    // The glass case is turned down — re-offer ONLY the good endings.
    { op: 'run', ref: 'script.wink_story_end_again', if_flag: 'flag:tin_story_end_glass', unless_flag: 'flag:tin_story_has_end' },
    { op: 'run', ref: 'script.wink_story_finale', if_flag: 'flag:tin_story_has_end' },
  ],
  'script.wink_story_end_again': [
    {
      op: 'choice',
      speaker: 'MAN WITH A CASE',
      prompt: 'How does it END? (A kind one, this time.)',
      options: [
        { label: 'They came home', ops: [{ op: 'run', ref: 'script.wink_end_home' }] },
        { label: 'A light kept on', ops: [{ op: 'run', ref: 'script.wink_end_light' }] },
        { label: 'Still wandering', ops: [{ op: 'run', ref: 'script.wink_end_wander' }] },
      ],
    },
  ],
  'script.wink_end_home': [
    { op: 'setFlag', flag: 'flag:tin_story_end_home' },
    { op: 'setFlag', flag: 'flag:tin_story_has_end' },
    { op: 'say', speaker: 'MAN WITH A CASE', text: '"...and they came home, a bit late, and nobody minded." Ahh. Everybody\'s favourite.' },
  ],
  'script.wink_end_light': [
    { op: 'setFlag', flag: 'flag:tin_story_end_light' },
    { op: 'setFlag', flag: 'flag:tin_story_has_end' },
    { op: 'say', speaker: 'MAN WITH A CASE', text: '"...and they never came back, but somebody kept the light on anyway."' },
    { op: 'say', speaker: 'MAN WITH A CASE', text: "That's a true one. Those cost the most." },
  ],
  'script.wink_end_wander': [
    { op: 'setFlag', flag: 'flag:tin_story_end_wander' },
    { op: 'setFlag', flag: 'flag:tin_story_has_end' },
    { op: 'say', speaker: 'MAN WITH A CASE', text: '"...and they\'re still wandering, but never lost." Won\'t sit down. I like it.' },
  ],
  // He tells it back (so you know it was heard), reacts, and hands him over.
  'script.wink_story_finale': [
    { op: 'say', speaker: 'MAN WITH A CASE', text: "Right. Let me tell it back to you, so you know it's been heard." },
    { op: 'narrate', if_flag: 'flag:tin_story_open_ferry', text: 'There was a ferryman who could read the weather but not his own face.' },
    { op: 'narrate', if_flag: 'flag:tin_story_open_rooster', text: 'There was a rooster who believed in morning when nobody else did.' },
    { op: 'narrate', if_flag: 'flag:tin_story_open_bun', text: 'Once, there was an enormous cheese-bun.' },
    { op: 'narrate', if_flag: 'flag:tin_story_mid_fog', text: 'One night the fog came in, and the bell went quiet.' },
    { op: 'narrate', if_flag: 'flag:tin_story_mid_machine', text: 'A brass machine told them a joke, and they laughed till the sea went out.' },
    { op: 'narrate', if_flag: 'flag:tin_story_mid_stranger', text: 'An old stranger pretended not to help them — and helped them all the way.' },
    { op: 'narrate', if_flag: 'flag:tin_story_mid_nothing', text: 'Nothing happened. For eleven years.' },
    { op: 'narrate', if_flag: 'flag:tin_story_end_home', text: 'And they came home, a bit late, and nobody minded.' },
    { op: 'narrate', if_flag: 'flag:tin_story_end_light', text: 'And they never came back — but somebody kept the light on anyway.' },
    { op: 'narrate', if_flag: 'flag:tin_story_end_wander', text: "And they're still wandering. But they're never lost." },
    // A bun that waits eleven years and comes home: the one he can't take.
    { op: 'run', ref: 'script.wink_react_bun', if_flag: 'flag:tin_story_open_bun' },
    { op: 'say', unless_flag: 'flag:tin_story_special', speaker: 'MAN WITH A CASE', text: "Bit lumpy in the middle. All the best ones are. He's yours." },
    { op: 'run', ref: 'script.wink_handover' },
  ],
  'script.wink_react_bun': [
    { op: 'run', ref: 'script.wink_react_bun_years', if_flag: 'flag:tin_story_mid_nothing' },
  ],
  'script.wink_react_bun_years': [
    { op: 'emote', if_flag: 'flag:tin_story_end_home', actor: 'wink', emote: 'ellipsis' },
    { op: 'say', if_flag: 'flag:tin_story_end_home', speaker: 'MAN WITH A CASE', text: "...A bun that waited eleven years to come home. Saddest thing I've heard. Take it." },
    { op: 'setFlag', if_flag: 'flag:tin_story_end_home', flag: 'flag:tin_story_special' },
  ],
  // The hand-over (story or purse). Every step guarded on the toy not yet held;
  // `flag:has_tin_rower` is set LAST so the whole beat plays exactly once.
  'script.wink_handover': [
    { op: 'narrate', unless_flag: 'flag:has_tin_rower', text: 'From his case: a tin boat, a blue-coated rower, a glass-bead bow-lamp, a brass key.' },
    { op: 'narrate', unless_flag: 'flag:has_tin_rower', text: 'Along the side: SAME TIDE TOMORROW. Underneath: MADE TO ORDER — T.' },
    { op: 'giveItem', unless_flag: 'flag:has_tin_rower', item: 'tin_rower' },
    { op: 'setFlag', unless_flag: 'flag:has_tin_rower', flag: 'flag:tin_rower_wound' },
    { op: 'say', unless_flag: 'flag:has_tin_rower', text: 'Received the TIN ROWER!' },
    { op: 'say', unless_flag: 'flag:has_tin_rower', speaker: 'MAN WITH A CASE', text: "He's wound. While he rows, wild kin follow HIM: [[half as many bother you]]." },
    { op: 'say', unless_flag: 'flag:has_tin_rower', speaker: 'MAN WITH A CASE', text: 'To stop him: [[ITEMS, KEY pocket]]. Use him again to wind him up.' },
    { op: 'say', unless_flag: 'flag:has_tin_rower', speaker: 'MAN WITH A CASE', text: "Wind him twice before bed. He rows better when someone's watching." },
    { op: 'wait', unless_flag: 'flag:has_tin_rower', ms: 400 },
    { op: 'fade', unless_flag: 'flag:has_tin_rower', dir: 'out', ms: 500 },
    { op: 'hideActor', unless_flag: 'flag:has_tin_rower', actor: 'wink' },
    { op: 'setFlag', unless_flag: 'flag:has_tin_rower', flag: 'flag:has_tin_rower' },
    { op: 'fade', dir: 'in', ms: 500 },
    { op: 'narrate', text: 'You look up to thank him — but the sand is empty. Only his sign, and the tide.' },
  ],

  // After the Tide Gleam, Reyl recognises the T. on the hull (once; 1 Lumen Drop).
  // Spliced into Reyl's post-Gleam talk with `{ op: 'run', ref: 'script.reyl_tin_rower' }`
  // — every step self-guards, so it is a silent no-op without the toy.
  'script.reyl_tin_rower': [
    { op: 'run', ref: 'script.reyl_tin_rower_seen', if_flag: 'flag:has_tin_rower', unless_flag: 'flag:reyl_tin_rower_seen' },
  ],
  'script.reyl_tin_rower_seen': [
    { op: 'narrate', text: 'Reyl sees the tin ferryman in your pack. He goes very still, and reads the stamp.' },
    { op: 'say', speaker: 'REYL WASH', text: "MADE TO ORDER — T. ...She said she'd a surprise coming. 'After the fog.'" },
    { op: 'say', speaker: 'REYL WASH', text: "...No, you keep it. It's a traveller. Here — for the road, from both of us." },
    { op: 'giveItem', item: 'lumen_drop' },
    { op: 'say', text: 'Received a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:reyl_tin_rower_seen' },
  ],

  // ---------------------------------------------------------------------------
  // R9 THE WORRY CLUB — five townsfolk frantic that {name} will never find the
  // easter egg. Each is ONE NPC + ONE script, staged as a single flag chain
  // (the andrew_egg if/unless pattern):
  //   PRE    unless flag:chickenpig_caught               (worry + a REAL main-path tip)
  //   CAUGHT if chickenpig_caught, unless q_south_wander_done  (relief)
  //   AFTER  if flag:q_south_wander_done                 (all's right with the world)
  // The gift is one-time on its own flag and keyed to the catch (not the stage),
  // so a player who first visits AFTER still gets it. Before the Ember Gleam every
  // tip points at Brisa or Andrew — never at the egg as an objective.
  // ---------------------------------------------------------------------------
  'script.worry_hester': [
    // PRE
    { op: 'emote', unless_flag: 'flag:chickenpig_caught', actor: 'worry_hester', emote: 'sweat' },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'HESTER', text: "FOUND it yet, {name}? No? I've dropped four stitches over you. FOUR." },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'HESTER', text: "Before I unravel: [[Andrew at the garden fence]]. Ask him WHERE NEXT." },
    // CAUGHT
    { op: 'emote', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', actor: 'worry_hester', emote: 'heart' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', speaker: 'HESTER', text: "You FOUND it! I knitted it a cosy. It's a rooster? ...It's a cosy now." },
    // AFTER
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'HESTER', text: 'Not lost, they tell me. WANDERING. On purpose. I\'ve had to sit down.' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'HESTER', text: "Everything's right with the world, {name}. I've even started a crossword." },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'HESTER', text: "Seven across: 'a light kept on for somebody.' ...Don't tell me. I'll get it." },
    // The gift (once, on the catch).
    { op: 'giveItem', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_hester_gift', item: 'tallow_balm', count: 2 },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_hester_gift', text: 'Hester presses 2 TALLOW BALMS on you, each in its own tiny knitted cosy.' },
    { op: 'setFlag', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_hester_gift', flag: 'flag:worry_hester_gift' },
  ],
  'script.worry_pim': [
    // PRE
    { op: 'emote', unless_flag: 'flag:chickenpig_caught', actor: 'worry_pim', emote: 'question' },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'PIM', text: 'Have you seen {name}? Out here THREE DAYS, not finding the thing.' },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'PIM', text: "I've drawn arrows. They follow them BACKWARDS." },
    { op: 'say', if_flag: 'flag:name_is_paul', unless_flag: 'flag:chickenpig_caught', speaker: 'PIM', text: 'And now there are TWO Pauls out here, and NEITHER has found it.' },
    { op: 'say', unless_flag: 'gleam:ember', speaker: 'PIM', text: "Lost too? Start with [[Brisa Tallow]] in Tinderwick, or [[Andrew]] at the fence." },
    { op: 'say', if_flag: 'gleam:ember', unless_flag: 'flag:chickenpig_caught', speaker: 'PIM', text: 'Tip from a professional: keep to the lit lane. Grass only if you WANT it.' },
    // CAUGHT
    { op: 'emote', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', actor: 'worry_pim', emote: 'alert' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', speaker: 'PIM', text: "They found it?! The rooster-pig?! That's a LOT of arrows wasted." },
    // AFTER
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'PIM', text: 'I put the map down. Turns out the coast was here all along.' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'PIM', text: "All's right with the world. I'd never looked at the sea. Somebody should draw an arrow to it." },
    // The gift (once, on the catch).
    { op: 'giveItem', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_pim_gift', item: 'glow_charge' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_pim_gift', text: 'Pim hands you a GLOW CHARGE wrapped in a map with no arrows on it at all.' },
    { op: 'setFlag', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_pim_gift', flag: 'flag:worry_pim_gift' },
  ],
  'script.worry_gilly': [
    // PRE
    { op: 'emote', unless_flag: 'flag:chickenpig_caught', actor: 'worry_gilly', emote: 'anger' },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'GILLY', text: "Seventeen times {name}'s passed this rock. NOT ONCE with an egg." },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'GILLY', text: "My sister Hester knits about it. I count about it. We each fret our own way." },
    { op: 'say', unless_flag: 'gleam:ember', speaker: 'GILLY', text: 'First lamp-test: [[Brisa Tallow]], Tinderwick. [[Andrew]] knows the rest. Eighteen.' },
    { op: 'say', if_flag: 'gleam:ember', unless_flag: 'flag:chickenpig_caught', speaker: 'GILLY', text: "Sit by [[the cockler's fire]] — it mends kin. Feed a Lumen Drop from ITEMS. Eighteen." },
    // CAUGHT
    { op: 'emote', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', actor: 'worry_gilly', emote: 'heart' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', speaker: 'GILLY', text: "Tally's in the sea. I feel twenty years younger. Sixteen, at least." },
    // AFTER
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'GILLY', text: 'You came back from the hill with a CUP? Everything is right with the world.' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'GILLY', text: "I've started a new tally. Times I've been happy today: four. ...Five." },
    // The gift (once, on the catch).
    { op: 'giveItem', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_gilly_gift', item: 'warm_balm' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_gilly_gift', text: 'Gilly gives you a WARM BALM, a tally scratched on the lid.' },
    { op: 'setFlag', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_gilly_gift', flag: 'flag:worry_gilly_gift' },
  ],
  // Nettie is placed on Lightkeeper's Point (pearlmoor_point, NPC id
  // `worry_nettie`) by the Old Light build; her tip follows the Tide loop.
  'script.worry_nettie': [
    // PRE
    { op: 'emote', unless_flag: 'flag:chickenpig_caught', actor: 'worry_nettie', emote: 'sweat' },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'NETTIE', text: '{name} passed the breakwater TWICE, waved at the dark lamp, and whistled off.' },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'NETTIE', text: "It's RIGHT THERE! I've walked a groove in this headland." },
    { op: 'say', unless_flag: 'gleam:ember', speaker: 'NETTIE', text: "No Gleam, this far out? [[Brisa Tallow]] in Tinderwick is first." },
    { op: 'run', ref: 'script.worry_nettie_tip', if_flag: 'gleam:ember', unless_flag: 'flag:chickenpig_caught' },
    // CAUGHT
    { op: 'emote', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', actor: 'worry_nettie', emote: 'ellipsis' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', speaker: 'NETTIE', text: "I've stopped pacing. ...I don't know what to do with my feet." },
    // AFTER
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'NETTIE', text: 'You came back singing, they say. The old man gave me a feather. It\'s in a jar.' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'NETTIE', text: "Everything's right with the world, love. Go on — go and be lost on purpose." },
    // The gift (once, on the catch).
    { op: 'giveItem', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_nettie_gift', item: 'warm_balm' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_nettie_gift', text: 'Nettie gives you a WARM BALM, and finally sits down on the bench.' },
    { op: 'setFlag', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_nettie_gift', flag: 'flag:worry_nettie_gift' },
  ],
  // Nettie's tip, stage-aware along the Tide loop (one line plays).
  'script.worry_nettie_tip': [
    { op: 'say', unless_flag: 'flag:q_south_bell', speaker: 'NETTIE', text: "[[Reyl Wash]] at the Lumenary first. He sends EVERYBODY up that tower." },
    { op: 'say', if_flag: 'flag:q_south_bell', unless_flag: 'flag:q_south_jest_done', speaker: 'NETTIE', text: "[[That tower]]'s got a tea-urn halfway up. Don't let the stove tell the ladder one." },
    { op: 'say', if_flag: 'flag:q_south_jest_done', unless_flag: 'gleam:tide', speaker: 'NETTIE', text: '[[Floats to the netmender]], rope to the bell, then Reyl. Rest first, love.' },
    { op: 'say', if_flag: 'gleam:tide', speaker: 'NETTIE', text: "[[East, on the fen road]], next. Your Tidecall walks the deep channels now." },
  ],
  'script.worry_constance': [
    // PRE
    { op: 'emote', unless_flag: 'flag:chickenpig_caught', actor: 'worry_constance', emote: 'question' },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'CONSTANCE', text: "Watching for {name}. Wrong end, yes. They look very far away. ACCURATE." },
    { op: 'say', unless_flag: 'flag:chickenpig_caught', speaker: 'CONSTANCE', text: "Never found it. I've had the glass up so long I've a ring round my eye." },
    { op: 'say', unless_flag: 'gleam:ember', speaker: 'CONSTANCE', text: "New? [[Brisa Tallow]] in Tinderwick gives the first Gleam. [[Andrew]] knows WHERE NEXT." },
    { op: 'say', if_flag: 'gleam:ember', unless_flag: 'flag:chickenpig_caught', speaker: 'CONSTANCE', text: "Lost? [[The Waykeeper's fingerpost]] never lies." },
    // CAUGHT
    { op: 'emote', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', actor: 'worry_constance', emote: 'alert' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander_done', speaker: 'CONSTANCE', text: "I turned the glass round! They're ENORMOUS! They're FINE!" },
    // AFTER
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'CONSTANCE', text: "Put the glass away. Some people you just leave the lamp on for." },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'CONSTANCE', text: "I've left one in my window. Habit. Everything's right with the world." },
    // The gift (once, on the catch).
    { op: 'giveItem', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_constance_gift', item: 'tallow_balm' },
    { op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_constance_gift', text: 'Constance hands you a TALLOW BALM — the right way round, this time.' },
    { op: 'setFlag', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:worry_constance_gift', flag: 'flag:worry_constance_gift' },
  ],

  // --- Wayfarer's kits + the open counters ------------------------------------
  // Each town keeper hands a starter bundle ONCE (the kit NPC swaps for the
  // trading keeper via flags), and thereafter keeps a live counter: the keeper's
  // script says its flavour line then opens the shop (content/shops.ts) with the
  // 'shop' op. Buying/selling is the ShopMenu; prices live on the ItemDefs.
  'script.shop_kit_tinderwick': [
    { op: 'say', speaker: 'SHOPKEEPER', text: 'Off on your Wayfaring? Then the first kit\'s on the house. Town custom.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', speaker: 'SHOPKEEPER', text: 'Two glow charges, two balms. [[Feed a charge to your lamp]] for a surer throw.' },
    { op: 'setFlag', flag: 'flag:tinderwick_kit' },
  ],
  'script.shop_kit_pearlmoor': [
    { op: 'say', speaker: 'CHANDLER', text: 'Facing Reyl, are you? Take the crossing-kit — the sea is kinder to the prepared.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', speaker: 'CHANDLER', text: 'Feed a charge to your lamp before a throw. A charged flame holds a catch better.' },
    { op: 'say', speaker: 'CHANDLER', text: 'Mind the triangle, dear: Ember scorches Verdant, Verdant drinks Tide, Tide drowns Ember. Reyl runs Tide — [[bring what beats it]].' },
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
    { op: 'say', text: 'Behind the hedge, in oilcloth: a WAX CAKE! Keepers pay well for it.' },
    { op: 'setFlag', flag: 'flag:picked_tinderwick_waxcake' },
  ],
  'script.pickup_flats_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 80 },
    { op: 'say', text: "A dropped courier's purse, half-buried in the sand. Found 80 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_flats_wicks' },
  ],
  // ---- The wick-purse caches (the "don't go broke" safety net) ---------------
  // A found purse in a quiet corner of each of the first six areas, scaled to the
  // leg's prices (10-economy.md). They exist because a run of blackouts — each
  // costing the 10% tithe — used to leave a player with no balms and no way to
  // buy any; a small found purse per area breaks that spiral without touching a
  // single payout. Mirrored in tools/balance/progression.mjs as each leg's
  // `finds` income, so the journey model still PASSES.
  'script.pickup_tinderwick_purse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 120 },
    { op: 'say', text: 'A knotted purse under the driftwood, long forgotten. Found 120 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_tinderwick_purse' },
  ],
  'script.pickup_dimglass_purse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 150 },
    { op: 'say', text: 'Under a stone: a lamplighter\'s pay-purse. Found 150 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_dimglass_purse' },
  ],
  'script.pickup_flats_purse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: 'A salt-stiff pouch in the dune hollow. Found 200 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_flats_purse' },
  ],
  'script.pickup_pearlmoor_purse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: 'Between the shore stones, where the tide put it back. Found 250 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_pearlmoor_purse' },
  ],
  'script.pickup_fen_purse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'A courier\'s purse, dry in its oilcloth. Found 300 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_fen_purse' },
  ],
  'script.pickup_lowleaf_purse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 350 },
    { op: 'say', text: 'In a hollow root, wrapped in leaves against the damp. Found 350 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_lowleaf_purse' },
  ],

  // ---- Lumen Drop finds ------------------------------------------------------
  // The level-up sweet is never SOLD (it would distort the wick economy), so it
  // has to be found: one at the back of the Glimmerstep spur, one in the Wind-Eye
  // — both optional side-rooms, so the reward reads as "you went looking".
  'script.pickup_grotto_drop': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Pressed lamp-honey, where the bloom-light pools. Found a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_grotto_drop' },
  ],
  'script.pickup_windeye_drop': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Wedged where the wind can\'t reach: a LUMEN DROP, still warm.' },
    { op: 'setFlag', flag: 'flag:picked_windeye_drop' },
  ],

  // Duskapple Orchard (R8): balms in the old tree's roots on the way in, and a
  // Lumen Drop in the far SW corner past the meadow (off the lane — you looked).
  'script.pickup_orchard_windfall': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: 'In the oldest tree\'s roots, among the windfalls. Found 2 TALLOW BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_orchard_windfall' },
  ],
  'script.pickup_orchard_drop': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Found a LUMEN DROP! [[Fed from ITEMS]], it grows a kin a whole level.' },
    { op: 'setFlag', flag: 'flag:picked_orchard_drop' },
  ],

  // Gran's send-off satchel on the home floor — three balms for the road.
  'script.pickup_gran_satchel': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 3 },
    { op: 'say', text: "Gran's travelling satchel, packed by the door. Found 3 TALLOW BALMS!" },
    { op: 'setFlag', flag: 'flag:picked_gran_satchel' },
  ],
  // The Lanternway lane caches (one per spoke lane, the variety rule across
  // the set: balm / charge / loose wicks / a found-to-sell cake / balms).
  'script.pickup_lane_tinderwick': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 1 },
    { op: 'say', text: 'Left on the pond stone where any wayfarer would look. Found a TALLOW BALM!' },
    { op: 'setFlag', flag: 'flag:picked_lane_tinderwick' },
  ],
  'script.pickup_lane_pearlmoor': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: "A courier's tin, tucked dry under the hedge. Found a GLOW CHARGE!" },
    { op: 'setFlag', flag: 'flag:picked_lane_pearlmoor' },
  ],
  'script.pickup_lane_lowleaf': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 90 },
    { op: 'say', text: 'A toll-box the green lane no longer asks for. Found 90 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_lane_lowleaf' },
  ],
  'script.pickup_undercut': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'say', text: "A Waykeeper's store-niche, dry under the bank. Found 2 GLOW CHARGES!" },
    { op: 'setFlag', flag: 'flag:picked_undercut' },
  ],
  'script.pickup_lane_galehigh': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'wax_cake', count: 1 },
    { op: 'say', text: 'Behind the outcrop, out of the wind: a WAX CAKE! Keepers pay well for it.' },
    { op: 'setFlag', flag: 'flag:picked_lane_galehigh' },
  ],
  'script.pickup_lane_nightreach': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: "A watcher's drop-cache beneath the last lamp but one. Found 2 TALLOW BALMS!" },
    { op: 'setFlag', flag: 'flag:picked_lane_nightreach' },
  ],
  // The netmender's storm-drifted net-floats (R9: no longer on the flats —
  // Punchwheel coughs them up at the top of the Old Light, script.oldlight_top).
  'script.pickup_net_floats': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'net_floats', count: 1 },
    { op: 'say', text: 'The drum coughs out cork floats stamped with [[the netmender]]\'s mark. Took the NET-FLOATS!' },
    { op: 'setFlag', flag: 'flag:picked_net_floats' },
  ],
  // R9: Lightkeeper's Point — tucked in the rocks behind the Old Light.
  'script.pickup_point_rocks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 2 },
    { op: 'say', text: 'In a joke-card with no punchline: Found 2 TALLOW BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_point_rocks' },
  ],
  // Breakwater caches (off the lane, the standing kit).
  'script.pickup_breakwater_balm': [
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Lashed under old net: a WARM BALM, and a HEARTH COAL alight in its tin!' },
    { op: 'setFlag', flag: 'flag:picked_breakwater_balm' },
  ],
  // S5 caches — the allotment's potting-bench corner and the Wanderwood's
  // central dead end (the "short cut" that isn't pays for the walk back).
  'script.pickup_allotment_bench': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'Under the potting bench, in a seed-sack: Received 2 WARM BALMS! (Anth\'s, probably. She\'d want you to have them. Probably.)' },
    { op: 'setFlag', flag: 'flag:picked_allotment_bench' },
  ],
  'script.pickup_wanderwood_cache': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'In a root-hollow: a BEACON CHARGE! Someone else thought this was a short cut.' },
    { op: 'setFlag', flag: 'flag:picked_wanderwood_cache' },
  ],
  // --- S5: the Far Side (pearlmoor_wanderwood_far) — optional discovery -------
  // The islet at the end of the glass steps: a Lumen Drop (found, never sold) and
  // p.'s note — the quiet-helper motif turned on the player. Nothing is confirmed.
  'script.pickup_wander_far_steps': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Under a flat stone on the islet, a twist of oilcloth: Found a LUMEN DROP! A note is folded round it, in a big unhurried hand.' },
    { op: 'narrate', text: '"Knew you\'d take the steps. Don\'t tell me you didn\'t look down.' },
    { op: 'narrate', text: 'Those wick-purses you keep tripping over on the roads? Funny how they turn up just when you\'re skint. Some folk are just lucky, I suppose. — p."' },
    { op: 'setFlag', flag: 'flag:picked_wander_far_steps' },
  ],
  // The ANSWERING LAMP: a brass, glass-headed lamp in the hollow that answers
  // anything at once and with total confidence — and is right about half the
  // time. p.'s carving beside it (sign.wander_far_reassess) says what to do
  // about that. Re-askable forever; Cancel just leaves it humming.
  'script.wander_answering_lamp': [
    { op: 'narrate', text: 'In the crook of the hollow tree sits a brass lamp with a round glass head. It hums. Its plate reads: ASK ME ANYTHING. I AM NEVER WRONG.' },
    {
      op: 'choice',
      prompt: 'The glass head brightens, eagerly.',
      options: [
        {
          label: 'Where\'s Paul?',
          ops: [
            { op: 'say', speaker: 'ANSWERING LAMP', text: 'PAUL IS IN THE WOOD. PAUL IS ALSO ON THE BREAKWATER. PAUL IS, ON AVERAGE, EVERYWHERE. CONFIDENCE: TOTAL.' },
            { op: 'say', speaker: 'ANSWERING LAMP', text: 'HE REFERS TO ME AS "THE THINKING KETTLE." I HAVE DECIDED THIS IS A COMPLIMENT.' },
          ],
        },
        {
          label: 'When\'s dawn?',
          ops: [
            { op: 'say', speaker: 'ANSWERING LAMP', text: 'DAWN IS SCHEDULED FOR TUESDAY.' },
            { op: 'narrate', text: 'It does not say which Tuesday. It seems delighted with itself.' },
          ],
        },
        {
          label: 'A new joke',
          ops: [
            { op: 'say', speaker: 'ANSWERING LAMP', text: 'A JOKE NO ONE HAS EVER TOLD BEFORE. PREPARING. ...WHY DID THE KIN CROSS THE ROAD?' },
            { op: 'say', speaker: 'ANSWERING LAMP', text: 'TO GET TO THE OTHER SIDE. HA. HA. HA. (THAT WAS THE DELIVERY.)' },
            { op: 'narrate', text: 'It has, you\'re fairly sure, been told before. The lamp waits for applause.' },
          ],
        },
        {
          label: 'Show the world',
          ops: [
            { op: 'say', speaker: 'ANSWERING LAMP', text: 'HERE IS ALL OF VESPERHOLM, AS SEEN FROM ABOVE THE STARS.' },
            { op: 'tint', color: '#000000', alpha: 0.85, ms: 400 },
            { op: 'wait', ms: 900 },
            { op: 'narrate', text: 'The glass head goes perfectly black. It holds the picture proudly.' },
            { op: 'tint', color: '#000000', alpha: 0, ms: 400 },
            { op: 'narrate', text: 'Scratched into the brass beneath it, in the big hand: LAUGHED AT THAT FOR ELEVEN MINUTES. — p.' },
          ],
        },
        {
          label: 'The Registry?',
          ops: [
            { op: 'say', speaker: 'ANSWERING LAMP', text: 'I HAVE NO RECORD OF ANY REGISTRY.' },
            { op: 'say', speaker: 'ANSWERING LAMP', text: '...WHICH IS, I AM OBLIGED TO NOTE, EXACTLY WHAT A RECORD WOULD SAY.' },
            { op: 'narrate', text: 'The lamp hums for a while, and then very deliberately starts humming something else.' },
          ],
        },
      ],
    },
  ],
  // MAGS at her griddle on the Far Side's low road: the cheese-bun (a gentle
  // no-rest heal — rest:false, so it never becomes a respawn point), the
  // clockwork lamplighters joke (Paul started it, laughed too hard to finish),
  // and a word about the man himself. Re-visitable; Cancel just leaves.
  'script.wander_mags': [
    { op: 'narrate', text: 'A striped stall, a griddle hissing over embers. The clearing smells, unreasonably, of melted cheese.' },
    { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'MAGS', text: 'He came through with a rooster-pig\'s feather in his hat and ordered THREE. Never three, Paul. Whatever you did in that glade — this one\'s on the house.' },
    {
      op: 'choice',
      speaker: 'MAGS',
      prompt: 'Bun, love? Or are you after a joke?',
      options: [
        {
          label: 'A cheese-bun',
          ops: [
            { op: 'say', speaker: 'MAGS', text: 'Griddle-bun, cheese right through. Paul has two after any sort of contest — feet up in front of the worst play the travelling players put on.' },
            { op: 'say', speaker: 'MAGS', text: 'Calls it his REWARD. Reward for what, I ask him. "For surviving, Mags." Every time.' },
            { op: 'heal', rest: false },
            { op: 'narrate', text: 'Hot, and far too good, and you share it round. Your kin are fully restored. Nobody needs to know how many you had.' },
          ],
        },
        {
          label: 'A joke',
          ops: [
            { op: 'say', speaker: 'MAGS', text: 'Paul started this one at my griddle and laughed so hard at the START he never got to the end. So I finished it for him. Ready?' },
            { op: 'say', speaker: 'MAGS', text: 'Three clockwork lamplighters walk into an inn. The innkeeper looks up and says, "Long night, lads?"' },
            { op: 'say', speaker: 'MAGS', text: 'The first one says, "Eleven years." The second one says, "Twelve."' },
            { op: 'say', speaker: 'MAGS', text: 'And the third one leans over and whispers, "Don\'t start him off. He still thinks it\'s Tuesday."' },
            { op: 'narrate', text: 'There is a pause.' },
            { op: 'say', speaker: 'MAGS', text: 'Paul laughed for a quarter of an hour. Rattled every lamp in the inn. ...I never said it was a GOOD joke.' },
          ],
        },
        {
          label: 'About Paul',
          ops: [
            { op: 'say', speaker: 'MAGS', text: 'Forty-odd years I\'ve fed him. Tells everyone he\'s "a bit of an anarchist." Returns his library books early. Brings the lending-house flowers.' },
            { op: 'say', speaker: 'MAGS', text: 'Doesn\'t trust anything that comes with a guarantee — me included, he says, and then orders two more buns.' },
            { op: 'say', speaker: 'MAGS', text: 'And he\'ll never say so, but he looks out for people. Quietly. The ones just starting out, mostly. ...You\'d know, I expect. Or you wouldn\'t. That\'s rather the point of him.' },
          ],
        },
      ],
    },
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
    { op: 'say', speaker: 'DELL', text: 'Hold the lane! Every moss-mound past me is a hundred years of held light.' },
    { op: 'say', speaker: 'DELL', text: 'Show me your lamp walks soft before I let it walk far.' },
    { op: 'battle', trainer: 'glowmoss_keeper_a' },
    { op: 'say', speaker: 'DELL', text: 'Soft enough. Mind the grey chamber past the beds. Something TENDS it, and not kindly.' },
    { op: 'setFlag', flag: 'flag:glowmoss_keeper_a_beaten' },
  ],
  'script.glowmoss_keeper_b': [
    { op: 'say', speaker: 'MIRREL', text: 'Out of the grey chamber, lamp still lit? Most come out quieter.' },
    { op: 'say', speaker: 'MIRREL', text: 'One more test before the mine road, then. Deepwood custom.' },
    { op: 'battle', trainer: 'glowmoss_keeper_b' },
    { op: 'say', speaker: 'MIRREL', text: 'Well held. [[The mine is east]]. Tell old Otho Grist the deep wood sent you.' },
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
    { op: 'narrate', text: 'The glow stops at the choke-stone. Past it the moss lies GREY: a chamber of kept light, gone out.' },
    { op: 'tint', color: '#202430', alpha: 0.4, ms: 600 }, // the drained cold
    { op: 'cameraFocus', to: { tx: 17, ty: 8 }, ms: 900 },
    { op: 'narrate', text: 'At its heart a Fennlight lies curled, dim as a coal under ash. Not hurt. Not waking. Beside it, a lantern built to hold nothing at all.' },
    { op: 'face', actor: 'acolyte_a', facing: 'left' },
    { op: 'emote', actor: 'acolyte_a', emote: 'alert' },
    { op: 'say', speaker: 'ACOLYTE', text: 'Oh — a Wayfarer. Please, tread soft. She is not hurt. She is RESTING.' },
    { op: 'action', actor: 'acolyte_a', action: 'bow' },
    { op: 'say', speaker: 'ACOLYTE', text: 'Does the quiet not look gentle? No more guttering. Just... rest.' },
    { op: 'say', speaker: 'ACOLYTE', text: 'We are the Hollowing. Our Warden Còr teaches that the dark asks nothing of anyone. We only help the tired lights lie down.' },
    { op: 'emote', actor: 'player', emote: 'question' },
    { op: 'cameraFocus', to: { tx: 20, ty: 8 }, ms: 800 },
    { op: 'face', actor: 'cowled_figure', facing: 'left' },
    { op: 'wait', ms: 700 },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'At the far edge a cowled figure stands very still, watching you. It bows its head — sorrowing, almost kind — and is gone into the dark.' },
    { op: 'face', actor: 'cowled_figure', facing: 'up' },
    { op: 'cameraReset', ms: 600 },
    { op: 'tint', color: '#202430', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'The [[null-lantern]] waits beside the sleeping kin. Your lamp leans toward it.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The null-lantern restoration — the first time the player UNDOES the
  // Hollowing's work. QUIET by design (a small warm bloom, no festival swell —
  // this is grief eased, not a Gleam). Sets flag:met_hollowing via the trigger;
  // the site's cast swaps grey→green on the flag (the §8 null-lantern pattern).
  'script.glowmoss_relight': [
    { op: 'cameraFocus', to: { tx: 18, ty: 8 }, ms: 700 },
    { op: 'narrate', text: 'The null-lantern stands cold. You touch your flame to its hollow wick.' },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fe8b8', alpha: 0.3, ms: 600 }, // a small green-gold bloom
    { op: 'narrate', text: 'It takes: small, stubborn, certain. Colour climbs back through the moss.' },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 900 },
    { op: 'emote', actor: 'sleeping_fennlight', emote: 'alert' },
    { op: 'narrate', text: 'The Fennlight stirs, blinks, and lifts into the air, trailing light like pollen.' },
    // E-1 (story panel): the law made VISIBLE — waking the kin brings its star back.
    { op: 'cameraFocus', to: { tx: 19, ty: 5 }, ms: 900 },
    { op: 'wait', ms: 500 },
    { op: 'flashColor', color: '#dfe6ff', ms: 500 },
    { op: 'setFlag', flag: 'flag:glowmoss_star_back' }, // the root-gap star object appears
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'narrate', text: 'Far above, through the roots, a star you hadn\'t known was missing comes back.' },
    { op: 'cameraReset', ms: 600 },
    { op: 'face', actor: 'acolyte_a', facing: 'down' },
    { op: 'emote', actor: 'acolyte_b', emote: 'ellipsis' },
    { op: 'narrate', text: 'The acolytes gather their grey bundles without a word, bow to the waking glow, and follow the dark out.' },
    { op: 'action', actor: 'acolyte_a', action: 'bow' },
    { op: 'wait', ms: 400 },
    { op: 'narrate', text: 'One drops a dark stone the size of a plum, faintly blue in its cracks. She does not come back for it.' },
    { op: 'setFlag', flag: 'flag:met_hollowing' },
    { op: 'cameraReset', ms: 600 },
  ],

  // Glowmoss Deep item caches (the standing kit: one valuable, one consumable,
  // one loose-wicks find — walkthrough README "Item caches").
  'script.pickup_glowmoss_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'A glow-moth caught in resin. Found a MOTH-AMBER! Keepers pay well for it.' },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_amber' },
  ],
  'script.pickup_glowmoss_balm': [
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A waxed tin, still warm. Found a WARM BALM and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_balm' },
  ],
  'script.pickup_glowmoss_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: "A miner's drop-purse, stitched shut against the damp. Found 200 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_wicks' },
  ],
  // Lamplight reveal (spine §5, Brightlight+): the glow-shadowed side-cell off
  // the main run — its cache only resolves out of the dark once the lamp can
  // reach it (flag:lamplight_brightlight derives in FlagStore, never hand-set).
  'script.pickup_glowmoss_sidecell': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'A side-cell only a brighter lamp could reach. Found a BRIGHT BALM!' },
    { op: 'say', text: 'You\'d have walked past this dark, once. The lamp is brighter now.' },
    { op: 'setFlag', flag: 'flag:picked_glowmoss_sidecell' },
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
    { op: 'say', speaker: 'MARIGOLD', text: 'Hold the plank! Fen custom: two lamps on one causeway test their wicks.' },
    { op: 'battle', trainer: 'fen_wader_a' },
    { op: 'say', speaker: 'MARIGOLD', text: 'A dry flame in a wet country — well kept. The fen will let you by.' },
    { op: 'setFlag', flag: 'flag:fen_wader_a_beaten' },
  ],
  'script.fen_courier_b': [
    { op: 'say', speaker: 'OSPREY', text: 'Post for Lowleaf, and a toll for the north shore. Paid in a bout!' },
    { op: 'battle', trainer: 'fen_courier_b' },
    { op: 'say', speaker: 'OSPREY', text: 'Toll paid. [[The channel ahead answers Tidecall]].' },
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
    { op: 'say', text: 'In the spore-soft dark, a sliver of sky. Found a STARGLASS SHARD!' },
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
    { op: 'say', speaker: 'TARN', text: 'Walked the moon-channels? Then you owe the reed-line a toll!' },
    { op: 'battle', trainer: 'reed_lamplighter' },
    { op: 'say', speaker: 'TARN', text: 'Paid. [[Follow the green glow]] to Lowleaf, and mind the Bloom crowds.' },
    { op: 'setFlag', flag: 'flag:reed_lamplighter_beaten' },
  ],

  // E1 "The Quiet Reeds" — the fen fisher on the channel jetty. Three of the
  // lantern-reeds on her line have gone dark; the first two take a flame, the
  // THIRD will not light, and nobody says why. (The B2 foreshadow stays SILENT
  // — no one names the Hollowing east of Glowmoss Deep.)
  'script.fen_fisher': [
    { op: 'say', speaker: 'FEN FISHER', text: 'Evening, tide-walker. Three of my lantern-reeds gone dark. Reeds don\'t gutter. Reeds GLOW.' },
    { op: 'say', speaker: 'FEN FISHER', text: 'My knees don\'t do channels now. [[Would you relight them]] for me?' },
    { op: 'say', speaker: 'FEN FISHER', text: 'Mind the order: [[near, then mid-water, then far]]. A line lights from home outward.' },
    { op: 'setFlag', flag: 'flag:q_east_reeds' },
  ],
  'script.reed_first': [
    { op: 'narrate', text: 'The near reed leans dark over its reflection. You touch your lamp to its wick.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffb86b', alpha: 0.2, ms: 400 },
    { op: 'narrate', text: 'It takes: an amber globe over black water. One. Below, something silver turns to the light.' },
    { op: 'tint', color: '#ffb86b', alpha: 0, ms: 600 },
  ],
  'script.reed_second': [
    { op: 'narrate', text: 'The mid-water reed is furred with moss. You clear the wick and lend it flame.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffb86b', alpha: 0.2, ms: 400 },
    { op: 'narrate', text: 'Two. The near reed answers it across the channel, held note to held note.' },
    { op: 'tint', color: '#ffb86b', alpha: 0, ms: 600 },
  ],
  // The third reed — it will NOT light. A quiet dread beat, no explanation:
  // that answer belongs to Glowmoss Deep. (cinematics.md: dread = the quiet.)
  'script.reed_third': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The far reed stands dark against the treeline. You touch flame to the wick.' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'The wick drinks your flame and stays dark.' },
    { op: 'narrate', text: 'The flame sinks into it like a stone into deep water. Not wet. Not broken. Just... finished.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'Nothing moves. The two lit reeds burn steadily behind you, and somehow that is worse.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],
  'script.fen_fisher_report': [
    { op: 'say', speaker: 'FEN FISHER', text: 'I saw the near two stand up from here. And the far one?' },
    { op: 'narrate', text: 'You tell her. The flame that sank like a stone. The wick that would not take.' },
    { op: 'say', speaker: 'FEN FISHER', text: '...Hm. Forty years on this water, and I\'d have said every reed lights.' },
    { op: 'say', speaker: 'FEN FISHER', text: 'Probably nothing. A bad wick. A cold spring.' },
    { op: 'narrate', text: 'She looks at the treeline a long moment, and does not say what she is thinking.' },
    { op: 'say', speaker: 'FEN FISHER', text: 'The line\'s thanks: a reed-wick lamp, dipped the old way. Burns twice as sure in deep growth.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'marsh_lamp', count: 1 },
    { op: 'say', text: 'Received the MARSH LAMP!' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: 'She presses 200 WICKS on you too. "For the oil you burned. No arguing."' },
    { op: 'setFlag', flag: 'flag:q_east_reeds_done' },
  ],

  // Fen II caches (the standing kit: a valuable on the tide-walk isle, loose
  // wicks off the lane, a consumable by the landing).
  'script.pickup_fen_isle_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'No plank reaches this isle. In the reed-root: a MOTH-AMBER!' },
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
    { op: 'say', text: 'Wax-wrapped for the next walker. Found 2 TALLOW BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_fen_ii_balm' },
  ],

  // --- Sunkbell Shallows (Tidecall spur) — the half-flooded shrine -------------
  'script.pickup_sunkbell_charges': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'A pilgrim\'s offering-box, sealed against the flood. Found 2 BEACON CHARGES!' },
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
    { op: 'narrate', text: 'The ferns are FULL of light: lantern-strings, striped stalls, glowing roofs. Lowleaf Hollow, and the Glowmoss Bloom in full swing.' },
    { op: 'narrate', text: 'Children chase glow-motes. A piper plays rounds; nobody dances in step.' },
    { op: 'cameraFocus', to: { tx: 15, ty: 13 }, ms: 900 },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'But in the dancing ring, the oldest moss-bed lies GREY. The festival flows around it like a missed note.' },
    { op: 'cameraReset', ms: 600 },
    { op: 'musicCrossfade', key: 'lowleaf-hollow-a', ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The Tended Bed (spine §5 shape #3 — the LIGHT loop). Sable's hook:
  'script.sable_quest': [
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: 'Oh — a Wayfarer. Two Gleams already, by your lamp. I, um. Welcome to the Bloom.' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'You\'ll have seen the Elder Bed. Grey, at its own festival. Everyone wants a speech. I\'d rather... not.' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'The Bloom won\'t crown a grey bed. [[Warm the old moss first]].' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: '[[The kilner by the square]] will know how. Moss wants warmth, and somebody patient.' },
    { op: 'setFlag', flag: 'flag:q_east_bloom' },
  ],

  // The fen-wood cache on the forest fringe (the bloom-warden lane).
  'script.pickup_fenwood': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fen_wood', count: 1 },
    { op: 'say', text: 'Under the ferns, where kilners stack it. Took an armful of FEN-WOOD!' },
    { op: 'setFlag', flag: 'flag:picked_fenwood' },
  ],

  // The kilner fires a hearth-spore from your fen-wood.
  'script.kiln_relight': [
    { op: 'say', speaker: 'KILNER', text: 'Fen-wood! Dry as a sermon and twice as useful. Give it here, give it here—' },
    { op: 'narrate', text: 'She racks the wood, strikes her flint, and the kiln wakes like a sleeping animal.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.25, ms: 500 },
    { op: 'say', speaker: 'KILNER', text: 'Now — the part nobody under sixty remembers. You don\'t warm an elder bed with fire. You warm it with what fire LEAVES.' },
    { op: 'narrate', text: 'From the coals she lifts a kiln-fired spore, warm as a held coal.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 600 },
    { op: 'giveItem', item: 'hearth_spore', count: 1 },
    { op: 'say', text: 'Received the HEARTH-SPORE!' },
    { op: 'giveMoney', amount: 150 },
    { op: 'say', text: '"Whoever feeds the kiln gets the fee." Received 150 WICKS!' },
    { op: 'say', speaker: 'KILNER', text: '[[Tuck it under the old moss]] and STEP BACK. Beds remember.' },
    { op: 'setFlag', flag: 'flag:q_east_hearthspore' },
  ],

  // Warming the Elder Bed — the loop's payoff: the grey→green swap (the §8
  // null-lantern pattern, warm edition: flag-gated objects + festival NPCs).
  'script.warm_elder_bed': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'You kneel at the stone ring. Up close, the moss is like burnt paper.' },
    { op: 'silence', ms: 1000 },
    { op: 'narrate', text: 'You work the spore under the cold moss, like banking a coal. And step back.' },
    { op: 'wait', ms: 600 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fe8b8', alpha: 0.35, ms: 800 },
    { op: 'narrate', text: 'Nothing. Nothing. Then one thread of moss remembers its colour. Then ten. Then the whole bed, green-gold racing rim to rim like a rumour.' },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'The piper stops mid-round. The whole festival turns. A child says, very clearly, "it was SLEEPING," and the dancing ring re-forms around the Elder Bed.' },
    { op: 'musicCrossfade', key: 'lowleaf-hollow-b', ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The bloom-warden sight trainers on the fen-wood lane (keeper class).
  'script.bloom_warden_a': [
    { op: 'say', speaker: 'IVY', text: 'Hold the lane! Every lamp on the fringe beds gets its wick trimmed.' },
    { op: 'battle', trainer: 'bloom_warden_a' },
    { op: 'say', speaker: 'IVY', text: 'Trimmed. [[The fen-wood is under the far ferns]].' },
    { op: 'setFlag', flag: 'flag:bloom_warden_a_beaten' },
  ],
  'script.bloom_warden_b': [
    { op: 'say', speaker: 'FERN', text: 'Ivy softens them up and I finish the lesson. Bloom-watch way!' },
    { op: 'battle', trainer: 'bloom_warden_b' },
    { op: 'say', speaker: 'FERN', text: 'Lesson finished. You\'d give Sable herself a fair evening.' },
    { op: 'setFlag', flag: 'flag:bloom_warden_b_beaten' },
  ],

  // The Verdant bond-test + Gleam ceremony (Sable's hall; minor→major, the
  // Glowmoss Bloom swell — the third "Gleam = belonging" payoff).
  'script.lumenary_lowleaf': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'sable', facing: 'down' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'You didn\'t make a speech at it. You warmed it, and let it remember. I watched.' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'neutral', text: 'So I won\'t make a speech either. The moss vouches for you. Now show me it\'s right.' },
    { op: 'battle', trainer: 'lampwarden_lowleaf' },
    { op: 'musicFade', ms: 500 },
    { op: 'wait', ms: 600 },
    { op: 'face', actor: 'sable', facing: 'up' },
    { op: 'tint', color: '#9fe8b8', alpha: 0.36, ms: 600 },
    { op: 'narrate', text: 'Sable opens the doors. The Elder Bed answers glow for glow, and overhead the VERDANT remembers how to shine.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'gleam', element: 'verdant' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 900 },
    { op: 'face', actor: 'sable', facing: 'down' },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'The moss doesn\'t shine FOR anyone. It keeps a little light where it can. Be like the moss. Here.' },
    { op: 'face', actor: 'sable', facing: 'left' },
    { op: 'wait', ms: 500 },
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'shy', text: 'The Glimmerstep. [[The deep wood north of town]] was too dark for me. Not for your lamp. ...Tell me what grows there?' },
  ],

  // The festival crowns around the green bed — banded in town, post-Gleam.
  'script.bloom_crowning': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'narrate', text: 'The hollow roars, as much as botanists roar. The Elder Bed burns green-gold; the Verdant hangs new-lit.' },
    { op: 'narrate', text: 'Someone has crowned the bed with glowmoss. Someone else is crying into a moss-cake.' },
    { op: 'say', speaker: 'BLOOM ELDER', text: 'A hundred and nine Blooms, and never the Bed crowned. Belonging, child: that\'s a Gleam.' },
    { op: 'musicCrossfade', key: 'lowleaf-hollow-b', ms: 1100 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // E2 "Spores for the Stall" — the Bloom stall-keeper's gathering errand.
  'script.stall_quest': [
    { op: 'say', speaker: 'STALL-KEEPER', text: 'Moss-cakes! Glow-jars! Spore— oh, who am I fooling. My shelf\'s EMPTY.' },
    { op: 'say', speaker: 'STALL-KEEPER', text: 'My gatherer won\'t pass the first bough now. But you walk the dark like a garden path.' },
    { op: 'say', speaker: 'STALL-KEEPER', text: '[[Three spore-caches]] lie [[in Glowmoss Deep]]. Bring them home and the stall feeds you for life. Within reason.' },
    { op: 'setFlag', flag: 'flag:q_east_spores' },
  ],
  'script.pickup_spore_a': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bloom_spores', count: 1 },
    { op: 'say', text: 'A bundle of glowing spores. One of three.' },
    { op: 'setFlag', flag: 'flag:picked_spore_a' },
  ],
  'script.pickup_spore_b': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bloom_spores', count: 1 },
    { op: 'say', text: 'The second spore-bundle. Two of three. Something up the gallery chitters, pointedly.' },
    { op: 'setFlag', flag: 'flag:picked_spore_b' },
  ],
  // The third cache has a squatter: a cross Sporeling, driven off in a battle.
  'script.spore_squatter': [
    { op: 'narrate', text: 'The third bundle! On it, puffed up, sits a Sporeling with the look of a landlord.' },
    { op: 'say', text: 'It chitters. It is not a welcoming chitter.' },
    { op: 'battle', trainer: 'spore_squatter' },
    { op: 'narrate', text: 'The Sporeling huffs and flounces off, pride dented, dignity intact.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bloom_spores', count: 1 },
    { op: 'say', text: 'Took the last spore-bundle. Three of three!' },
    { op: 'setFlag', flag: 'flag:spore_squatter_beaten' },
  ],
  'script.stall_reward': [
    { op: 'say', speaker: 'STALL-KEEPER', text: 'Three! One argued for — I can smell the huff. You beautiful walking lantern.' },
    { op: 'narrate', text: 'She restocks before you finish. A queue forms instantly.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'glow_salve', count: 1 },
    { op: 'say', text: 'Received a GLOW SALVE — "festival pressing, not for sale, don\'t tell the provisioner."' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'And a share of the stall\'s evening: 300 WICKS!' },
    { op: 'say', speaker: 'STALL-KEEPER', text: 'Fennlight drift into the fringe grass while the Bloom\'s lit. [[Take a charge out there]] and ask one home.' },
    { op: 'setFlag', flag: 'flag:q_east_spores_done' },
  ],

  // Lowleaf's one-time shop kit + the open counter (the standing pattern).
  'script.shop_kit_lowleaf': [
    { op: 'say', speaker: 'PROVISIONER', text: 'In off the fen! Have the Bloom-kit. No charge, stop arguing.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', speaker: 'PROVISIONER', text: 'Charges and a balm. The fringe grass is kind; the deep wood is not.' },
    { op: 'setFlag', flag: 'flag:lowleaf_kit' },
  ],
  'script.shop_lowleaf': [
    { op: 'dialogue', ref: 'npc.lowleaf_provisioner' },
    { op: 'shop', shop: 'lowleaf_provisioner' },
  ],

  // The guest-bower's rest (the town's full heal — the standing kit).
  'script.lowleaf_rest': [
    { op: 'say', speaker: 'BOWER-KEEPER', text: 'Every walker gets the same bower. The moss-bunks are warm.' },
    { op: 'heal' },
    { op: 'say', speaker: 'BOWER-KEEPER', text: 'There. Kin bright-eyed, boots dry. The Bloom keeps till morning.' },
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
    { op: 'say', text: 'On the fringe fence post, seal unbroken. Found a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_lowleaf_charge' },
  ],

  // Gullcry Rock's prize: the Tide Charm (a sea-blessed lamp; see items.ts).
  'script.pickup_gullcry_charm': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'tide_charm', count: 1 },
    { op: 'say', text: 'Lashed to the highest stone, humming. Found the TIDE CHARM!' },
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
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'neutral', text: "The Wayfarer the vigil's muttering about. Come for a Gleam, have you." },
    { op: 'face', actor: 'otho_quest', facing: 'up' },
    { op: 'wait', ms: 600 },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'grave', text: "Down here light's KEPT. My crew left the vigil-lamp [[at the third gallery]], still lit if they did their job." },
    { op: 'face', actor: 'otho_quest', facing: 'down' },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'neutral', text: "[[Bring it up STILL BURNING]]. Then we'll talk Gleams. Not before." },
    { op: 'setFlag', flag: 'flag:q_east_vigil' },
  ],

  // Carrying the vigil-lamp up (in the deep) — the §8 restoration beat, the
  // melancholy edition: the gallery lamps lean toward the one flame that kept.
  'script.take_vigil_lamp': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The vigil-lamp sits where the crew left it, burning yet. Somebody kept it fed in their heart.' },
    { op: 'action', actor: 'player', action: 'kneel', holdMs: 700 },
    { op: 'silence', ms: 900 },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.30, ms: 700 },
    { op: 'narrate', text: 'You lift it. It does not gutter. Behind you, the gallery lamps seem to lean toward it.' },
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
    { op: 'wait', ms: 500 },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'grave', text: "You carried it up still burning. Through the dark, without letting it go out." },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'neutral', text: "Anyone can LIGHT a lamp. Carrying one through the dark — that's the trick. Now show me your kin can." },
    { op: 'battle', trainer: 'lampwarden_cinderhead' },
    { op: 'musicFade', ms: 600 },
    { op: 'silence', ms: 1100 },
    { op: 'face', actor: 'otho', facing: 'up' },
    { op: 'wait', ms: 700 },
    { op: 'narrate', text: 'Otho says nothing. Then he lifts the vigil-lamp, and all through the town the lowered lamps begin to rise.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'tint', color: '#caa46a', alpha: 0.34, ms: 800 },
    { op: 'narrate', text: 'Overhead, through a fault in the cavern roof, the STONE constellation steadies and shines — patient, like the mountain.' },
    { op: 'gleam', element: 'stone' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 1000 },
    { op: 'tint', color: '#caa46a', alpha: 0, ms: 900 },
    { op: 'face', actor: 'otho', facing: 'down' },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'proud', text: "The Stone Gleam. Four relit, and two crowns yours. The mountain remembers a steady light." },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'warm', text: "[[Galehigh's up the deep galleries]] and out. Cold wind, high ledges. Mind the lamp." },
  ],

  // The vigil-fire rest (the town's full heal — the standing per-region kit).
  'script.cinderhead_rest': [
    { op: 'say', speaker: 'VIGIL COOK', text: "Sit by the vigil-fire, Wayfarer. We keep it low — but we keep it." },
    { op: 'heal' },
    { op: 'say', speaker: 'VIGIL COOK', text: "There. Rested and ready. The dark's long — but the fire's longer." },
  ],

  // Cinderhead's one-time shop kit + the open counter (the standing pattern).
  'script.shop_kit_cinderhead': [
    { op: 'say', speaker: 'PIT-PROVISIONER', text: "Fronting up to Otho? Have the pit-kit. No charge." },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'say', speaker: 'PIT-PROVISIONER', text: "Otho's kin hit like a roof-fall. Stock balms, not bravado." },
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
    { op: 'say', speaker: 'LONE MINER', text: "[[The foreman's ledger]] got left [[in a side gallery]]. I can't face the deep no more. You can." },
    { op: 'say', speaker: 'LONE MINER', text: "Bring it home. Good crystal down there too — honest pay for honest dark." },
    { op: 'setFlag', flag: 'flag:q_east_ledger' },
  ],
  'script.pickup_ledger': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'say', text: 'A swollen ledger in a dry niche. Recovered the FOREMAN\'S LEDGER!' },
    { op: 'say', text: 'Its last page lists galleries "past the lamp\'s reach". Something for a brighter lamp.' },
    { op: 'setFlag', flag: 'flag:q_east_ledger_found' },
  ],
  'script.ledger_reward': [
    { op: 'say', speaker: 'LONE MINER', text: "The ledger! I'd given it up to the wet. Bless your lamp, Wayfarer." },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'He presses a STARGLASS SHARD on you: "Deep-cut crystal. Sell it well."' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: "And a foreman's thank-you: 300 WICKS!" },
    { op: 'setFlag', flag: 'flag:q_east_ledger_done' },
  ],

  // E4 "The Sunniest House in the Dark" — Georgina, the Cat-keeper. An OPTIONAL
  // post-Verdant spur (gloamwood_dell, off lowleaf_hollow). A bubbly sunshine-goth
  // who loves the dark and FILLS it with light — the cheerful counter-argument to
  // the Hollowing, played for warmth and laughs. Flow: a hollow neighbour points
  // the way (hook) -> meet her in the cottage (she asks you to fetch her bolted
  // kitten Pim) -> find Pim in the dell -> a friendly battle -> she gifts you a
  // dragon-cat kitten of your own. All flags hand-set q_east_* (none derived).
  'script.georgina_hook': [
    { op: 'say', speaker: 'HOLLOW NEIGHBOUR', text: 'Go and meet our Georgina, [[east past the ferns]], in the blackest dell.' },
    { op: 'say', speaker: 'HOLLOW NEIGHBOUR', text: "A hundred cats, and not a BIT afraid of the dusk. When the stars went out, she put bunting up." },
    { op: 'say', speaker: 'HOLLOW NEIGHBOUR', text: "Daft as a brush. She'll be thrilled. She's always thrilled." },
    { op: 'setFlag', flag: 'flag:q_east_georgina' },
  ],
  // Meet Georgina in the cottage. Establishes the character + the anti-Hollowing
  // theme (with jokes), and sends the player to find her bolted kitten Pim.
  'script.georgina_intro': [
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'delighted', text: "Ooh, a VISITOR! Mind the cats — that's Smudge, that's Other Smudge, that's a cushion." },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'sunny', text: "Folk think if I love the dark I must be ROOTING for the lamp-snuffers. Pfft!" },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'sunny', text: "I love the dark for what you put IN it. Cats. Fairy-lights. You don't mend a sad room by smashing the lamp. You hang up MORE." },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'neutral', text: "...Which is the trouble. A Hollowing quiet swept through last week, and my Pim took fright and bolted into the dell." },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'delighted', text: "[[Find my Pim]], and I'll show you something special. She likes [[the darkest corner]] — an optimist, like her mum." },
  ],
  // Pim, found in the darkest corner of the dell (the lost_kitten NPC).
  'script.georgina_kitten_found': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'In the blackest hollow, a tiny violet kitten watches a glowmoss-spark like a private sunrise. She climbs into your lamp-bag.' },
    { op: 'say', text: 'You scooped up PIM! She is purring loud enough to rattle the lamp.' },
    { op: 'setFlag', flag: 'flag:q_east_georgina_kitten' },
  ],
  // Back at the cottage with Pim: the friendly battle, then the dragon-cat gift.
  // The 'battle' op aborts the scene on a loss (the host blacks the player out),
  // so everything after it only runs once the player has won — georgina_beaten and
  // the gift are banked here, inside the winning branch.
  'script.georgina_battle': [
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'delighted', text: "PIM! My brave little optimist — not a whisker out of place!" },
    { op: 'battle', trainer: 'trainer_georgina' },
    { op: 'setFlag', flag: 'flag:georgina_beaten' },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'sunny', text: "Right! Promised you a secret, didn't I? Meet the pride of the house. The wings are only for SHOW. Mostly." },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'tint', color: '#a26bd6', alpha: 0.22, ms: 300 },
    { op: 'narrate', text: 'From the nook uncurls a cat the colour of dusk, dragon-wings folded like a cloak, a warm gold coal in her chest.' },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'delighted', text: "A Gloampurr! Folk think they're a Hollowing thing. Backwards! She carries her OWN little sunrise. She FURNISHES the night." },
    { op: 'tint', color: '#a26bd6', alpha: 0, ms: 400 },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'sunny', text: "And this clutch had a kitten spare. She's YOURS. Don't argue, she's very sensitive." },
    { op: 'giveKin', kin: 164, level: 5 },
    { op: 'say', text: 'GEORGINA gave you a GLOAMPURR kitten!' },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'wink', text: "Raise her with SUNSHINE, hear? A dark to be brave in, a warm lap to come home to." },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'delighted', text: "Now SHOO before I cry. Wherever the Hollowing put a light out, you hang up TWO. Tara, love!" },
    { op: 'setFlag', flag: 'flag:q_east_georgina_done' },
  ],
  // Recurring, after the gift — Georgina is a permanent sunny fixture of the dell.
  'script.georgina_after': [
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'delighted', text: "My favourite Wayfarer! How's our girl? Knocking things off shelves? GOOD." },
    { op: 'say', speaker: 'GEORGINA', portrait: 'georgina', expr: 'sunny', text: "The dark's only a room, love, and you're VERY good at lights. Mind the Smudges." },
  ],

  // The sealed mine door, opened from the inside — the hub re-link. The trigger
  // sets flag:shortcut_mine; this is the cutscene that sells it (spine §0 rule 3).
  'script.open_mine_shortcut': [
    { op: 'narrate', text: 'A door, barred from this side long ago. The bar lifts easily: it only kept the dark from wandering UP.' },
    { op: 'sfx', key: 'world-door-open' },
    { op: 'narrate', text: 'It opens on the old hoist-line, straight back to [[the Vesper Crossroads]].' },
  ],

  // Cinderhead caches (variety rule: a gallery crystal valuable, loose wicks, a
  // balm in the mine; a deep MOTH-AMBER a choke off the lane, the §4 grind reward).
  'script.pickup_cinderhead_crystal': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Raw crystal, catching your lamp. Found a STARGLASS SHARD!' },
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
    { op: 'say', text: 'In a deep seam: a knot of MOTH-AMBER! Collectors pay dearly.' },
    { op: 'setFlag', flag: 'flag:picked_deepcrystal' },
  ],
  // deeper-floor caches (the descent maze pays in kind, a choke off the lane)
  'script.pickup_cinderhead_wicks_deep': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: 'Behind a pit-prop, the crew\'s float. Found 200 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_cinderhead_wicks_deep' },
  ],
  'script.pickup_cinderhead_balm_deep': [
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'A relief cache by the ladder: balms, a charge, and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_cinderhead_balm_deep' },
  ],
  // Lamplight reveal (spine §5, Starlight+): the third gallery's late alcove —
  // the cramped early visit kept it hidden; a far-reaching lamp does not
  // (flag:lamplight_starlight derives in FlagStore, never hand-set).
  'script.pickup_cinderhead_alcove': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 2 },
    { op: 'say', text: 'An alcove no crew-lamp reached. Found 2 MOTH-AMBER!' },
    { op: 'say', text: 'You passed ten paces from this dark on the Vigil. The lamp knows now.' },
    { op: 'setFlag', flag: 'flag:picked_cinderhead_alcove' },
  ],

  // The two vigil-miner SIGHT trainers holding the Descent Vigil leg (keeper class).
  'script.gallery_miner_a': [
    { op: 'say', speaker: 'DRUSE', text: "Nobody walks my gallery to the vigil-lamp without sounding their wick. Crew rule." },
    { op: 'battle', trainer: 'gallery_miner_a' },
    { op: 'say', speaker: 'DRUSE', text: "Steady light. [[The lamp's two chambers down]]." },
    { op: 'setFlag', flag: 'flag:gallery_miner_a_beaten' },
  ],
  'script.gallery_miner_b': [
    { op: 'say', speaker: 'HOBB', text: "The last lamp before the vigil-lamp's mine. Druse softens, I finish." },
    { op: 'battle', trainer: 'gallery_miner_b' },
    { op: 'say', speaker: 'HOBB', text: "Finished proper. Carry it up gentle." },
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
    { op: 'narrate', text: 'High above the terrace, kite-strings climb to a launch ledge — and something up there is FLYING.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'HOY! Down there — the new lamp out of the mine! Yes, YOU, with the indoor shoulders!' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'Want the Storm Gleam? Then FLY! Nobody meets the wind from the ground.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: '[[Raise a kite]] with the town — [[the kite-maker]] on the lower terrace will help — and fly it at the Rising!' },
    { op: 'narrate', text: 'She peels away into a gust, whooping. The festival cheers without looking up.' },
  ],

  // The kite-maker's three storm-scattered pieces — chained caches on the lower
  // terraces (each pick reveals the next; the flags drive the map's chain).
  'script.pickup_kite_a': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'kite_spar', count: 1 },
    { op: 'say', text: 'Wedged in the hedge: a KITE SPAR! The sail can\'t have blown far.' },
    { op: 'setFlag', flag: 'flag:picked_kite_a' },
  ],
  'script.pickup_kite_b': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'kite_sail', count: 1 },
    { op: 'say', text: 'Snagged on a terrace post: the KITE SAIL! Now, where would a tail land...' },
    { op: 'setFlag', flag: 'flag:picked_kite_b' },
  ],
  'script.pickup_kite_c': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'kite_tail', count: 1 },
    { op: 'say', text: 'Coiled in the grass: the KITE TAIL, lamps unbroken. Back to [[the kite-maker]]!' },
    { op: 'setFlag', flag: 'flag:picked_kite_c' },
  ],

  // The kite-maker builds the town's kite back out of your three finds.
  'script.kite_built': [
    { op: 'say', speaker: 'KITE-MAKER', text: 'The spar! The sail! The TAIL! You walked half the terraces for a stranger\'s kite.' },
    { op: 'narrate', text: 'She works without a word, testing every knot twice against her wrist.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'There. Twice-built — by me, then by you. That makes it the TOWN\'S kite.' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'Take it to [[the winch-keeper]] on the festival terrace and [[fly it at the Rising]]!' },
    { op: 'setFlag', flag: 'flag:q_north_kite_ready' },
  ],

  // Arc E — the Kite-rising itself: warm, communal, a little daft. The crest is
  // sincere (humour lives in the build-up, never the crest).
  'script.galehigh_kite_rising': [
    { op: 'say', speaker: 'WINCH-KEEPER', text: 'A town-built kite and a south-east wind! Places, everyone! The Rising rises!' },
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicCrossfade', key: 'galehigh-terraces-b', ms: 900 },
    { op: 'emote', actor: 'festival_piper', emote: 'music', holdMs: 700 },
    { op: 'narrate', text: 'The whole terrace pays out string. Kites stagger into the gusts — one shaped alarmingly like the winch-keeper — every tail strung with lit wick-lamps.' },
    { op: 'face', actor: 'festival_kid', facing: 'right' },
    { op: 'hop', actor: 'festival_kid', times: 2 },
    { op: 'say', speaker: 'FESTIVAL KID', text: 'Yours next! Don\'t let it dip past the third gust, the third gust is a BITER—' },
    { op: 'action', actor: 'player', action: 'toss', holdMs: 400 },
    { op: 'narrate', text: 'You let the wind take the town\'s kite. It dips past the third gust — which bites — steadies... and climbs, writing a wobbly line of light up the dark.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.22, ms: 800 },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'The whole hill goes quiet, a hundred small flames swaying overhead for the stars to climb back up by. Daft, maybe. But the night is a little less long for it.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 900 },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'emote', actor: 'festival_kid', emote: 'heart', holdMs: 500 },
    { op: 'say', speaker: 'WINCH-KEEPER', text: 'FLOWN AND BLESSED! Mira watched every yard. [[The winch turns for you]] now — up you go!' },
    { op: 'musicCrossfade', key: 'galehigh-terraces-a', ms: 900 },
    // N-4 — one LIVE fall, at the warmest festival, while the music plays on.
    // It goes down south, past the terraces: towards the mountain.
    { op: 'flashColor', color: '#cfe8ff', ms: 200 },
    { op: 'starfall', from: 'right' },
    // N-4 counts on the pass-walker's map (West W-4), now or when it opens.
    { op: 'run', unless_flag: 'flag:fall_seen_galehigh', ref: 'script.passmap_tick' },
    { op: 'setFlag', flag: 'flag:fall_seen_galehigh' },
    { op: 'cameraFocus', to: { tx: 9, ty: 30 }, ms: 1100 },
    { op: 'narrate', text: 'A streak of cold light crosses the sky, silent, and falls past the southern terraces — towards the mountain. Every kite-tail dips at once.' },
    { op: 'emote', actor: 'festival_goer', emote: 'alert', holdMs: 500 },
    { op: 'face', actor: 'festival_kid', facing: 'down' },
    { op: 'say', speaker: 'FESTIVAL KID', text: 'Was that one of OURS?' },
    { op: 'wait', ms: 900 },
    { op: 'cameraReset', ms: 800 },
    { op: 'letterbox', on: false, ms: 320 },
    { op: 'setFlag', flag: 'flag:q_north_kite_blessed' },
  ],

  // Galehigh's sight trainers (route class) + the skyloft's wind-wards (keeper).
  'script.galehigh_kitehand': [
    { op: 'say', speaker: 'PERRIN', text: 'Hold the lane! Every lamp crossing the terraces gets tested. I AM the wind\'s representative.' },
    { op: 'battle', trainer: 'galehigh_kitehand' },
    { op: 'say', speaker: 'PERRIN', text: 'The wind approves. Tell the kite-maker Perrin still owes her a spar.' },
    { op: 'say', speaker: 'PERRIN', unless_flag: 'gleam:storm', text: '[[Fly at the Rising]] first, mind. The Stair beyond me is wild with wind-kin.' },
    { op: 'setFlag', flag: 'flag:galehigh_kitehand_beaten' },
  ],
  'script.galehigh_terracer': [
    { op: 'say', speaker: 'SORREL', text: 'Off my beds— oh, a Wayfarer. Terrace custom: the crops watch a bout first.' },
    { op: 'battle', trainer: 'galehigh_terracer' },
    { op: 'say', speaker: 'SORREL', text: 'Beaten on my own terrace. The cabbages saw everything. We shall never speak of it.' },
    { op: 'setFlag', flag: 'flag:galehigh_terracer_beaten' },
  ],
  'script.skyloft_ward_a': [
    { op: 'say', speaker: 'TAMSIN', text: 'A rider off the winch! The LEDGE answers to the wind-wards. Show us your flame.' },
    { op: 'battle', trainer: 'skyloft_ward_a' },
    { op: 'say', speaker: 'TAMSIN', text: 'Well flown. And I\'d trained that gust personally. Bran holds the last stretch.' },
    { op: 'setFlag', flag: 'flag:skyloft_ward_a_beaten' },
  ],
  'script.skyloft_ward_b': [
    { op: 'say', speaker: 'BRAN', text: 'Last ward before the ledge. Mira asks that the wind has already said yes.' },
    { op: 'battle', trainer: 'skyloft_ward_b' },
    { op: 'say', speaker: 'BRAN', text: 'It said yes. Loudly. The ledge is ahead — she\'ll be the one mid-air.' },
    { op: 'setFlag', flag: 'flag:skyloft_ward_b_beaten' },
  ],

  // Lumenary 5 — Mira Vael at the launch ledge. Win → gleam:storm + Updraft
  // Kite (TRAINERS['mira_vael'] carries the grants). The ceremony is the
  // BINDING Gleam cadence: silence → warm tint → lamp sfx → gleam → swell.
  'script.lumenary_galehigh': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'mira_vael', facing: 'down' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'There you are! Your kite took the third gust and kept climbing. The wind\'s still talking about it.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'You don\'t fight the wind, apprentice. You ask it to lift you, and thank it when it does. Same as a kin.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'So! The sky\'s watching: show me a bond the storm would carry!' },
    { op: 'battle', trainer: 'mira_vael' },
    { op: 'musicFade', ms: 500 },
    { op: 'silence', ms: 1000 },
    { op: 'tint', color: '#ffd089', alpha: 0.38, ms: 700 },
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 500 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Mira raises her lamp off the ledge, you raise yours, and every kite-tail over Galehigh lifts its flames. Overhead, the Storm remembers how to shine.' },
    { op: 'gleam', element: 'storm' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'The Storm Gleam stands! Five relit — listen to the town! That cheer is yours, and so is this:' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'The [[Updraft Kite]]. Thermals to lift you up high ledges, and a long glide where the ground runs out.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: '[[Step off the ledge]] and glide down to the festival. I\'ll race you!' },
  ],

  // Rest, kit and counter (the standing per-region kit).
  'script.galehigh_inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'In out of the gusts, Wayfarer. The shutters only rattle friendly.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'Kin bright-eyed, boots warm. The mountain will keep till morning.' },
  ],
  'script.shop_kit_galehigh': [
    { op: 'say', speaker: 'KITE-KEEPER', text: 'In off the mine road! The climb-kit\'s yours — terrace custom.' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', speaker: 'KITE-KEEPER', text: 'Pale Vault keeps no counter, so [[stock up HERE]] before the Stair and the glacier.' },
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
    { op: 'say', text: 'Tucked under a terrace stone: a MOTH-AMBER, warm with old light!' },
    { op: 'setFlag', flag: 'flag:picked_galehigh_amber' },
  ],
  'script.pickup_galehigh_high': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'Only the thermals reach this ledge — and a BRIGHT BALM left for the next flier!' },
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
    { op: 'say', text: 'In the terrace\'s highest crack: LEDGE-HERB! [[The crag-tender]] on the Stair swears by it.' },
    { op: 'setFlag', flag: 'flag:picked_ledge_herb' },
  ],

  // N3 "Wren's Ribbon" — Mira, quietly, after the wobble (requires met_cor).
  'script.ribbon_quest': [
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'Wayfarer. No shouting today — come here a moment.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'This was on the terrace after the Rising. Wren\'s, off their kite. Then I heard what the ice road did to them.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'wren_ribbon', count: 1 },
    { op: 'say', text: 'She presses a kite-ribbon into your hand. Received WREN\'S RIBBON!' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'neutral', text: 'There\'s a [[quiet ledge on the second stair]], [[west side, behind the crag]]. Wren sat there an hour. Leave it for them.' },
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'soft', text: 'Don\'t write anything. Don\'t wait. The wind minds the rest.' },
    { op: 'setFlag', flag: 'flag:q_north_ribbon' },
  ],

  // R4 — the Waykeeper's Round, leg 4: the commissioned kite, kite-maker →
  // waystone kid. (The giver sets q_round_kite_taken; delivery sets q_round_kite.)
  'script.round_kite': [
    { op: 'say', speaker: 'KITE-MAKER', text: 'Ah, the kite-finder! The Waykeeper commissioned this in spring: one sturdy kite, for the waystone kid.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'round_kite', count: 1 },
    { op: 'say', text: 'A small kite in Lanternway colours. Received the WAYSTONE KITE!' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'Built to survive an owner of eight. [[Take it to the Crossroads]] by the Lantern-car — and tell the kid: the string hand is everything.' },
    { op: 'setFlag', flag: 'flag:q_round_kite_taken' },
  ],
  'script.round_kite_deliver': [
    { op: 'say', speaker: 'WAYSTONE KID', text: 'Is that— it IS. It\'s MINE. The Waykeeper said I\'d know you by the walk and I DO—' },
    { op: 'narrate', text: 'The kid takes the kite like a lamp at a naming. The Waykeeper counts out your fee with great ceremony.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'Received 300 WICKS and 2 WARM BALMS — "Round rates, plus the weather."' },
    { op: 'say', speaker: 'WAYSTONE KID', text: 'The string hand is everything. I KNOW. Watch. ...Well, TOMORROW, when the wind\'s back.' },
    { op: 'setFlag', flag: 'flag:q_round_kite' },
  ],

  // --- Windward Stair: the climb, the kettle, the crags ----------------------
  'script.windward_craghand': [
    { op: 'say', speaker: 'EDDA', text: 'Hold at the bend! The climb tests your legs, and the crag-hands test the rest.' },
    { op: 'battle', trainer: 'windward_craghand' },
    { op: 'say', speaker: 'EDDA', text: 'Four hundred steps a day, and today the lesson walked UP to me. The wind-gap\'s above. It\'s rude.' },
    { op: 'setFlag', flag: 'flag:windward_craghand_beaten' },
  ],
  'script.windward_galewatch': [
    { op: 'say', speaker: 'ROWAN', text: 'A lamp on the high leg! The gale-watch greets every flame up here — with a bout.' },
    { op: 'battle', trainer: 'windward_galewatch' },
    { op: 'say', speaker: 'ROWAN', text: 'Warm enough. Find the crag-tender\'s camp up the switchback — her kettle\'s saved more climbers than the rope.' },
    { op: 'setFlag', flag: 'flag:windward_galewatch_beaten' },
  ],
  'script.windward_cragwatch': [
    { op: 'say', speaker: 'MERLE', text: 'Off the wind-gap with your boots on! One bout — the glacier won\'t practise mercy.' },
    { op: 'battle', trainer: 'windward_cragwatch' },
    { op: 'say', speaker: 'MERLE', text: 'That\'ll do. [[Pale Vault]] is down the far slope. Walk in QUIET — the town keeps a watch.' },
    { op: 'setFlag', flag: 'flag:windward_cragwatch_beaten' },
  ],

  // N1 "The Crag-tender's Kettle" — the giver camps on the upper switchbacks.
  'script.kettle_quest': [
    { op: 'say', speaker: 'CRAG-TENDER', text: 'Sit, child — everyone sits at this bend. It\'s where the legs find out what they agreed to.' },
    { op: 'say', speaker: 'CRAG-TENDER', text: 'The proper brew wants [[LEDGE-HERB]], from the [[high cracks of Galehigh]]\'s top terraces. My ledge days are forty years gone.' },
    { op: 'say', speaker: 'CRAG-TENDER', text: 'A Wayfarer with the Storm\'s gift could ride the thermals up for a sprig. My kettle would remember it.' },
    { op: 'setFlag', flag: 'flag:q_north_kettle' },
  ],
  'script.kettle_done': [
    { op: 'say', speaker: 'CRAG-TENDER', text: 'Ledge-herb! Burnt on the windward side, exactly right. You RODE for this.' },
    { op: 'narrate', text: 'She brews it slow: melt-water, three pinches, patience. The steam smells like a kinder season.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'warm_flask', count: 1 },
    { op: 'say', text: 'She fills her felt-wrapped flask for you. Received the WARM FLASK!' },
    { op: 'say', speaker: 'CRAG-TENDER', text: 'For the glacier. When the chill gets past what a fire mends — that\'s the brew.' },
    // Only the done-flag here: her three placements key on picked_ledge_herb /
    // q_north_kettle_done, so both orders hold (herb-first skips kettle_quest
    // entirely; quest-first already set q_north_kettle there) — and nothing
    // consumes q_north_kettle, so it is not re-set.
    { op: 'setFlag', flag: 'flag:q_north_kettle_done' },
  ],

  // The crags band — flag:shortcut_windward is set by the trigger; this is the
  // "now accessible" callout that sells the drop home (spine §0 rule 3).
  'script.windward_crags': [
    { op: 'narrate', text: 'The stair tops out onto the high crags — bare, bright, snow behind every stone.' },
    { op: 'narrate', text: 'Far below, Galehigh\'s terraces glow like banked coals. A glide-ledge drops straight to them — the long climb home, repaid in one glide.' },
    { op: 'say', text: 'The Windward shortcut is open: [[one glide]] from the crags to Galehigh.' },
  ],

  // N3's payoff — wordless by design: ONE narration line, nothing else.
  'script.place_ribbon': [
    { op: 'narrate', text: 'You tuck Wren\'s ribbon under a stone at the ledge\'s lip — and the wind, for a wonder, lets it lie.' },
  ],

  // N2 viewpoint one — the Windward crag vista (the sketcher's first asking).
  'script.sketch_crag': [
    { op: 'narrate', text: 'The sketcher\'s first view. You look properly: the North under the aurora — Galehigh\'s warm fires, the glacier like a held wave.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'You stay until the cold finds your collar. One of three.' },
  ],

  // Windward caches (stair I: balm / wicks / valuable; stair II: amber + kit).
  'script.pickup_windward_balm': [
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A climber\'s cache by the cairn. Found a WARM BALM and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_windward_balm' },
  ],
  'script.pickup_windward_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: "A courier's purse, wedged down the switchback. Found 250 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_windward_wicks' },
  ],
  'script.pickup_windward_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Glinting in the scree: a STARGLASS SHARD, fallen from the sky above!' },
    { op: 'setFlag', flag: 'flag:picked_windward_shard' },
  ],
  'script.pickup_windward_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'In a crack of the crag: a MOTH-AMBER, its shimmer still turning!' },
    { op: 'setFlag', flag: 'flag:picked_windward_amber' },
  ],
  'script.pickup_windward_kit': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'giveItem', item: 'glow_charge', count: 1 },
    { op: 'say', text: 'A crag-watch relief cache. Took a WARM BALM and a GLOW CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_windward_kit' },
  ],

  // Wind-Eye + Thunderroost — the Updraft spurs pay (10-economy cache variety).
  'script.pickup_windeye_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'A flier\'s offering-box, dry in the alcove. Found 2 BEACON CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_windeye_charge' },
  ],
  'script.pickup_windeye_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'At the oculus\'s rim: a STARGLASS SHARD, faintly singing in the updraft!' },
    { op: 'setFlag', flag: 'flag:picked_windeye_glass' },
  ],
  'script.pickup_roost_prize': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'chart_tempest', count: 1 },
    { op: 'say', text: 'Behind the boulder choke, in a chart-tube older than the dusk: a STAR-CHART: TEMPEST!' },
    { op: 'say', text: 'Above you, the storm-birds shift on the nest and permit it. Apparently.' },
    { op: 'setFlag', flag: 'flag:picked_roost_prize' },
  ],

  // --- Pale Vault: the Lamp-Line (spine §5 shape #6) -------------------------
  // Ysolde's hook at the undercroft door (sets flag:q_north_lampline).
  'script.ysolde_quest': [
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'You walked in off the crags. Good. No Gift, no gate here — only the cold, and the cold is honest.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'See the blue ice by the door? Seven brackets, descending, dark a long time.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: '[[Light the seven brackets]], [[in order]], none hurried — and let me see the light hold.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'They burn [[aurora-oil]]. [[The tallow-keeper]] in the hollows renders it, but her hearth went out. Begin there.' },
    { op: 'setFlag', flag: 'flag:q_north_lampline' },
  ],

  'script.pickup_stormwood': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'stormwood', count: 1 },
    { op: 'say', text: 'Storm-felled wood, dry under the snow-crust. Took an armful of STORM-KINDLING!' },
    { op: 'setFlag', flag: 'flag:picked_stormwood' },
  ],

  // The tallow-keeper's hearth relit + the oil rendered (her camp's doused→lit
  // MapObject pair swaps on flag:q_north_aurora_oil).
  'script.render_oil': [
    { op: 'say', speaker: 'TALLOW-KEEPER', text: 'Storm-kindling! Dry to the heart. Give it here, and mind the smoke.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.24, ms: 600 },
    { op: 'narrate', text: 'The hearth takes the wood like an apology accepted. Warmth crawls back into the stones — and, by degrees, the keeper.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'She renders the tallow slow, tilting the pan skyward — "so it remembers" — until the oil holds a faint light of its own.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'aurora_oil', count: 1 },
    { op: 'say', text: 'Received the AURORA-OIL!' },
    { op: 'giveMoney', amount: 200 },
    { op: 'say', text: 'And the rendering-fee, over your objections: 200 WICKS.' },
    { op: 'say', speaker: 'TALLOW-KEEPER', text: 'Light them [[IN ORDER]], child — a line is a promise kept one lamp at a time.' },
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
    { op: 'narrate', text: 'A figure stands on the drained shelf below — cowled, hands folded, as if he has waited exactly as long as was polite.' },
    { op: 'cameraFocus', actor: 'cor_figure', ms: 1000 },
    { op: 'face', actor: 'cor_acolyte', facing: 'down' },
    // X-2: his courtesy is VISIBLE — he greets you with a bow before a word.
    { op: 'face', actor: 'cor_figure', facing: 'right' },
    { op: 'action', actor: 'cor_figure', action: 'bow', holdMs: 500 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'Good evening, apprentice. Forgive meeting you out here. Towns flinch at me, and I am careful of other people\'s evenings.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'I am Còr. The lanterns in the grey wood, built to hold nothing, are mine. You have been undoing my work, kindly and well.' },
    { op: 'face', actor: 'cor_figure', facing: 'down' },
    { op: 'narrate', text: 'His hand moves over the valley below: grey moss, still ice, a quiet with no edges.' },
    { op: 'tint', color: '#2a3550', alpha: 0.38, ms: 1000 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'Look at it. No lamp gutters here. No wick burns down while someone watches, helpless. Nothing here will be lost again — nothing is still spending itself.' },
    { op: 'face', actor: 'cor_figure', facing: 'right' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'You keep lamps. Then you know their cruellest thing: a lamp asks to be watched. Every light you relight, someone must grieve.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'I am not your enemy. I am only tired of grief — and so, if you are honest, is everyone you have lit a lamp for.' },
    { op: 'narrate', text: 'It would be easier if he were wrong in some plain, loud way. He is not.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'Fenn will come; he always comes after me. Ask him if the sky was worth what it cost him. Watch his face when he says yes.' },
    // N-1 — the antagonist and the motif meet: Còr carries a cinder. Staged,
    // held out, looked at; he faces the dark valley for the line, back to you
    // for the question.
    { op: 'narrate', text: 'He turns a dark stone in his gloved hand — cracked, faintly blue along the seams.' },
    { op: 'action', actor: 'cor_figure', action: 'gift', holdMs: 1300 },
    { op: 'face', actor: 'cor_figure', facing: 'down' },
    { op: 'action', actor: 'cor_figure', action: 'sad', holdMs: 1500 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'They fall nearer the mountain every year. Guttered stars, going home. I fetch them when I can. Somebody ought to sit with them.' },
    { op: 'wait', ms: 700 },
    { op: 'face', actor: 'cor_figure', facing: 'right' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'No, I will not fight you. The Hollowing takes nothing from the unwilling. I leave you only a question:' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'When the last light you love fails — and it will — would you rather have watched it burn, or been spared the dark after? Take your time. I did.' },
    { op: 'tint', color: '#2a3550', alpha: 0, ms: 1000 },
    { op: 'action', actor: 'cor_figure', action: 'bow', holdMs: 700 },
    { op: 'narrate', text: 'He bows, and walks into the dark between the ice-spires. The dark does not trouble him at all.' },
    { op: 'move', actor: 'cor_figure', to: { tx: 6, ty: 20 }, speed: 0.6 },
    { op: 'move', actor: 'cor_figure', to: { tx: 3, ty: 20 }, speed: 0.6 },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'The wind remembers itself. The aurora seems thinner. You cannot decide if it is.' },
    { op: 'cameraReset', ms: 700 },
    { op: 'musicCrossfade', key: 'pale-vault-glacier-a', ms: 1400 },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // C3 — Fenn and the shared past. On Còr's heels: two faces and the quiet.
  // No swell, no sting; the trigger sets flag:fenn_c3.
  'script.fenn_shared_past': [
    { op: 'face', actor: 'fenn_c3', facing: 'right' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'Child. I came as fast as these legs allow, and still he was here first. I can feel the quiet he leaves.' },
    // X-2: the pause before the bad news — a turned back reads as grief.
    { op: 'face', actor: 'fenn_c3', facing: 'left' },
    { op: 'wait', ms: 900 },
    { op: 'narrate', text: 'Fenn looks at the drained shelf a long time. He does not ask what Còr said.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'We read the same sky once, he and I. I steadied the ladder. He named the stars as they came loose.' },
    // N-2 (X-1 dose 1): there was a THIRD apprentice. Her name waits for dawn.
    { op: 'wait', ms: 700 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'There were three of us on that ladder, once. Then two — and a star missing that we had named together. The rest is half his grief, not mine to lend.' },
    { op: 'face', actor: 'fenn_c3', facing: 'right' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'neutral', text: 'He chose to stop the cycle, so it could never hurt anyone again. I chose to keep lighting lamps. Two answers, child. One question.' },
    { op: 'wait', ms: 600 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: '...I still believe I was right. And I have never stopped understanding him. That is the weight of being his friend.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'So do not hate him. Out-remember him. Every lamp you relight is a thing he has made himself forget. It is the only argument he flinches at.' },
    { op: 'move', actor: 'fenn_c3', to: { tx: 14, ty: 21 } },
    { op: 'face', actor: 'fenn_c3', facing: 'right' },
    { op: 'wait', ms: 400 },
    { op: 'narrate', text: 'He presses your shoulder once, and goes, slower than he came.' },
    { op: 'move', actor: 'fenn_c3', to: { tx: 14, ty: 23 }, speed: 0.6 },
  ],

  // A4 — WREN'S WOBBLE at the undercroft door: the hard rival battle, at the
  // exact threshold of the light-holding trial. Opens on 'unsure'; afterward
  // silence and an unresolved exit — Wren is NOT consoled (that is A5's work).
  'script.wren_pale_vault': [
    { op: 'face', actor: 'wren_pale_vault', facing: 'up' },
    { op: 'wait', ms: 600 },
    { op: 'face', actor: 'wren_pale_vault', facing: 'down' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'Oh. It\'s you. ...Of course it\'s you.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'I talked to him. Còr. Nobody warns you that he\'s kind. That\'s the unfair part.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'I keep doing the sums and they come out his way. No guttering. No goodbyes. Nothing got hurt. Tell me what\'s wrong with that. I can\'t find it.' },
    { op: 'action', actor: 'wren_pale_vault', action: 'turnAway', holdMs: 900 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'You\'re about to prove a light can hold. And I\'m wondering if I even want it to.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'So show me. No friendly rules — everything you have. If your light can\'t make me feel it, maybe there\'s nothing to feel.' },
    { op: 'battle', trainer: 'wren_pale_vault' },
    { op: 'silence', ms: 1600 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'You fight like you\'ve got something the dark can\'t take. I don\'t know if I\'ve got that.' },
    // N-3 — the wobble, performed: Wren looks at the door, away from it, and
    // says the thing about Mum's quiet village (seeded at the crossroads).
    { op: 'face', actor: 'wren_pale_vault', facing: 'up' },
    { op: 'wait', ms: 900 },
    { op: 'face', actor: 'wren_pale_vault', facing: 'left' },
    { op: 'emote', actor: 'wren_pale_vault', emote: 'ellipsis' },
    { op: 'action', actor: 'wren_pale_vault', action: 'sad', holdMs: 1400 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'Mum\'s well, you know. Her whole village is. Nobody\'s lit a lamp since spring, and nobody minds. ...I mind. I think I mind.' },
    { op: 'wait', ms: 800 },
    { op: 'action', actor: 'wren_pale_vault', action: 'turnAway', holdMs: 700 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: '...I need to walk a while. Don\'t follow me. Please.' },
    // You step aside; Wren walks off through the snow — the first exit shown, not told.
    { op: 'move', actor: 'player', to: { tx: 18, ty: 10 } },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'move', actor: 'wren_pale_vault', to: { tx: 19, ty: 12 }, speed: 0.8 },
    { op: 'move', actor: 'wren_pale_vault', to: { tx: 24, ty: 12 }, speed: 0.8 },
    { op: 'narrate', text: 'They go — not toward town, not toward anywhere. The wind takes their footprints almost as fast as they leave them.' },
    { op: 'setFlag', flag: 'flag:wren_pale_vault_battled' },
  ],

  // The undercroft's two frost-ward sight keepers (dungeon keeper class).
  'script.undercroft_ward_a': [
    { op: 'say', speaker: 'SELA', text: 'Hold, lamplighter. The vault admits no flame the wards haven\'t sounded.' },
    { op: 'battle', trainer: 'undercroft_ward_a' },
    { op: 'say', speaker: 'SELA', text: 'Sounded, and true. Walk on, and keep your order — the line knows.' },
    { op: 'setFlag', flag: 'flag:undercroft_ward_a_beaten' },
  ],
  'script.undercroft_ward_b': [
    { op: 'say', speaker: 'ORRIN', text: 'The last ward. I send Ysolde nothing the cold could blow out.' },
    { op: 'battle', trainer: 'undercroft_ward_b' },
    { op: 'say', speaker: 'ORRIN', text: 'Steady to the last. Finish the line — the vault has waited years to be bright.' },
    { op: 'setFlag', flag: 'flag:undercroft_ward_b_beaten' },
  ],

  // The seven brackets — lit in line, mounting quiet wonder. (Each trigger
  // chains on the previous flag; the lit/dark bracket objects swap on them.)
  'script.light_lamp_1': [
    { op: 'narrate', text: 'The first bracket. You pour aurora-oil into the iron well and touch your lamp to the wick.' },
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 350 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.18, ms: 500 },
    { op: 'narrate', text: 'It takes, pale and cool: the aurora, come indoors. One.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 600 },
  ],
  'script.light_lamp_2': [
    { op: 'narrate', text: 'The second bracket — and the ICE takes the light, running into the wall like water into a vein.' },
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 350 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.2, ms: 500 },
    { op: 'narrate', text: 'Two. Behind you, the first burns on. You hadn\'t realised you were checking.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 600 },
  ],
  'script.light_lamp_3': [
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 350 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Three. The light finds a lamplighter\'s mark beside the bracket, years of dark old.' },
    { op: 'narrate', text: 'Someone walked this line before you. The vault kept their soot, and waited.' },
  ],
  'script.light_lamp_4': [
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 350 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.22, ms: 600 },
    { op: 'narrate', text: 'Four — past halfway. Behind you, four pale flames in blue ice, and your shadow like a second lamplighter.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
  ],
  'script.light_lamp_5': [
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 350 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Five. The vault begins to HUM, a note passed bracket to bracket like a glass singing.' },
    { op: 'narrate', text: 'It is not a cold sound. An hour ago you would not have believed that.' },
  ],
  'script.light_lamp_6': [
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 350 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.24, ms: 700 },
    { op: 'narrate', text: 'Six. Through the thinning ice above, the aurora itself — and the flame below leans the same way.' },
    { op: 'narrate', text: 'Sky above, sky within. One bracket left.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
  ],
  'script.light_lamp_7': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'silence', ms: 1300 },
    { op: 'narrate', text: 'The seventh bracket. You pour the last aurora-oil and ask your flame to cross once more.' },
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 350 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.34, ms: 900 },
    { op: 'narrate', text: 'Seven. The whole line stands lit behind you — and the vault ANSWERS, every wall waking blue-green, the hum settling into a chord.' },
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
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Seven flames, walked in order, none hurried. The light arrived ahead of you, wanderer. It spoke well of you.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'Cold does not hate the flame. It waits to see if the flame means it. Warm your kin... and let the light hold.' },
    { op: 'battle', trainer: 'ysolde_frost' },
    { op: 'musicFade', ms: 600 },
    { op: 'silence', ms: 1200 },
    { op: 'tint', color: '#9fd4ff', alpha: 0.36, ms: 800 },
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 500 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'Ysolde lifts her lamp, and the brackets\' light climbs the blue ice and out into the night. Over the glacier, the Frost remembers how to shine.' },
    { op: 'gleam', element: 'frost' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 1000 },
    { op: 'tint', color: '#9fd4ff', alpha: 0, ms: 1000 },
    { op: 'narrate', text: 'Storm and Frost stand together, and the northern quadrant of the Skyweave Crown closes overhead, quiet as snowfall.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'warm', text: 'The Frost Gleam, and the northern crown with it. You have made my vault a lit place. Take this.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'The [[Emberward]]: an ember the coldfog cannot snuff. [[The pass west of town]] is shut to every flame but yours now.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'warm', text: 'Stand [[the Aurora-watch]] before you go. You have earned a lamp among us. That is the whole ceremony.' },
  ],

  // Arc E — the Aurora-watch: the SILENT VIGIL. Stage as silence + slow light;
  // it rhymes with Còr's calm — and refutes it (the lamps are LIT). No humour.
  'script.pale_vault_aurora_watch': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'silence', ms: 1600 },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'narrate', text: 'The town stands out on the ice, spaced like standing stones, faces turned up. The vigil-keeper raises one hand.' },
    { op: 'face', actor: 'vigil_keeper', facing: 'up' },
    { op: 'face', actor: 'aurora_watcher_b', facing: 'up' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.14, ms: 900 },
    { op: 'narrate', text: 'A single lamp lights at the line\'s end.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.2, ms: 900 },
    { op: 'narrate', text: 'Then the next, and the next — lamp answering lamp down the line, unhurried as the aurora.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.26, ms: 1100 },
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 900 },
    { op: 'narrate', text: 'A lamp is put into your hands. You light it from your vesperlamp and look up. That is all that is asked.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 900 },
    { op: 'silence', ms: 1400 },
    { op: 'narrate', text: 'It is as calm as any quieted valley. But nothing here is surrendered: every stillness is a kept flame, watched by someone who chose to watch.' },
    { op: 'say', speaker: 'VIGIL-KEEPER', text: 'It is enough to stand. It is enough to burn. The sky knows you are here.' },
    { op: 'musicCrossfade', key: 'pale-vault-glacier-a', ms: 1400 },
    { op: 'letterbox', on: false, ms: 420 },
    { op: 'setFlag', flag: 'flag:aurora_watch_seen' },
  ],

  // N2 "The Aurora Sketcher" — the painter at the festival ice; pure stillness.
  'script.sketch_quest': [
    { op: 'say', speaker: 'SKETCHER', text: 'Mind the easel! Forty years I\'ve tried to put that sky on paper. It never holds still.' },
    { op: 'say', speaker: 'SKETCHER', text: 'Three views my knees won\'t reach: the Windward crag, the glacier shore west of town, and this ice from the far braziers.' },
    { op: 'say', speaker: 'SKETCHER', text: '[[Go and STAND in all three]]. Look till you\'re cold, then [[come back and tell me]] what the light did.' },
    { op: 'setFlag', flag: 'flag:q_north_sketch' },
  ],
  'script.sketch_shore': [
    { op: 'narrate', text: 'The glacier shore. The ice stands off the water like a wave asked to wait; the aurora lies doubled in the shallows.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'You stand until you can keep it. Two of three.' },
  ],
  'script.sketch_festival': [
    { op: 'narrate', text: 'The far brazier line. The whole town small under the sky, each holding one flame.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'The town keeps the sky company. Three of three. Back to the sketcher.' },
  ],
  'script.sketch_done': [
    { op: 'say', speaker: 'SKETCHER', text: 'Sit. Talk. Slowly — the crag first.' },
    { op: 'narrate', text: 'You tell her: the North, the wave that waits, the town keeping the sky company. She draws, glancing up at you instead of the sky.' },
    { op: 'say', speaker: 'SKETCHER', text: '...There. Forty years, and I was missing somebody to hold still INSTEAD of the sky.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'aurora_charm', count: 1 },
    { op: 'say', text: 'She unclips a charm from her easel, faintly aglow. Received the AURORA CHARM!' },
    { op: 'giveMoney', amount: 400 },
    { op: 'say', text: 'And her colour-fund, without negotiation: 400 WICKS.' },
    { op: 'say', speaker: 'SKETCHER', text: 'Raise it toward a [[Frost-hearted kin]] and your lamp burns like tonight\'s sky.' },
    { op: 'setFlag', flag: 'flag:q_north_sketch_done' },
  ],

  // Pale Vault rest + caches (no shop here — the town is deliberately sparse).
  'script.pale_vault_inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'Come in quiet. The hearth is low, but it is LIT — the house\'s whole boast.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'Rested, kin and all. The watch keeps the night; you needn\'t.' },
  ],
  'script.pickup_pale_vault_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'A watcher\'s cache, felt-wrapped against the frost. Found 2 WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_pale_vault_balm' },
  ],
  'script.pickup_pale_vault_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: "A trader's purse, chipped free of a drift. Found 300 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_pale_vault_wicks' },
  ],
  'script.pickup_pale_vault_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Deep in the blue ice: a STARGLASS SHARD, holding its breath. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_pale_vault_shard' },
  ],
  'script.pickup_pale_vault_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'An offering at the brazier line, seal sound. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_pale_vault_charge' },
  ],
  'script.pickup_undercroft_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'In a niche behind the second gallery: a MOTH-AMBER, untroubled by the ice!' },
    { op: 'setFlag', flag: 'flag:picked_undercroft_amber' },
  ],
  'script.pickup_undercroft_balm': [
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'A lamplighter\'s reserve for the worst night: a BRIGHT BALM!' },
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
    { op: 'say', speaker: 'DUNSTAN', text: 'Hold there! The fog at the throat beats my lamp back every season, so every flame that faces it gets trimmed first. By me.' },
    { op: 'battle', trainer: 'hushfrost_lampman' },
    { op: 'say', speaker: 'DUNSTAN', text: 'That will burn through. [[The throat is west]]. Walk warded, and don\'t listen to the fog.' },
    { op: 'setFlag', flag: 'flag:hushfrost_lampman_beaten' },
  ],
  'script.hushfrost_survivor': [
    { op: 'say', speaker: 'HESPER', text: 'Stop a moment. I came out of the deep fog on one lamp and no luck, so I test every flame that passes.' },
    { op: 'battle', trainer: 'hushfrost_survivor' },
    { op: 'say', speaker: 'HESPER', text: 'Steady right through. Then it won\'t be you I lie awake over.' },
    { op: 'setFlag', flag: 'flag:hushfrost_survivor_beaten' },
  ],

  // --- Hushfrost Pass II — the coldfog throat + X1 "The Caretaker's Lamp" ----
  'script.hushfrost_thawtender': [
    { op: 'say', speaker: 'TILDA', text: 'Mind the lane — just swept! A clear road costs a bout; that\'s my rule.' },
    { op: 'battle', trainer: 'hushfrost_thawtender' },
    { op: 'say', speaker: 'TILDA', text: 'Well fought. The gold on the fog is real — stored daylight. Walk toward the warmth.' },
    { op: 'setFlag', flag: 'flag:hushfrost_thawtender_beaten' },
  ],
  // X1, the ask. Grief register — zero humour anywhere near this shelter.
  // She sits with a numbed Hearthkit the coldfog touched; the kin SLEEPS,
  // and stays asleep (B-arc weight; it wakes only at flag:dawn, postgame).
  'script.caretaker_quest': [
    { op: 'say', speaker: 'CARETAKER', text: 'Soft, now. She\'s sleeping. ...She\'s always sleeping, since the fog came through.' },
    { op: 'say', speaker: 'CARETAKER', text: 'She used to glow like a hearth. They tell us the sleep is mercy. I light a lamp by her anyway.' },
    { op: 'say', speaker: 'CARETAKER', text: 'My lamp\'s at the dregs. Only [[aurora-oil]] holds in this cold — it pools in [[the hollow north of here]], under the ice. My knees can\'t make that road.' },
    { op: 'say', speaker: 'CARETAKER', text: 'You carry a warded flame. Fill my lamp, and she would sleep in the light. That is nearly everything I have left to give her.' },
    { op: 'setFlag', flag: 'flag:q_west_caretaker' },
  ],
  'script.caretaker_done': [
    { op: 'say', speaker: 'CARETAKER', text: 'Aurora-oil. You walked the hollow for us.' },
    { op: 'narrate', text: 'She fills the lamp slowly. The flame takes, pale and steady, a faint moving light in it.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'The light settles over the sleeping kin. It does not wake. But something in it eases, like a sleeper when a door shuts out the cold.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 800 },
    { op: 'say', speaker: 'CARETAKER', text: 'There. She sleeps easier in the light. ...So will I.' },
    { op: 'say', speaker: 'CARETAKER', text: 'Take my bright lamp — I kept it for a steadier hand. May every wild heart you raise it toward know it was a watched flame.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'caretaker_lamp', count: 1 },
    { op: 'say', text: 'Received the BRIGHT LAMP!' },
    { op: 'setFlag', flag: 'flag:q_west_caretaker_done' },
  ],

  // Hushfrost caches (the standing variety: wicks / balms / the missable shard).
  'script.pickup_hushfrost_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: "A courier's purse, chipped free of the drift. Found 300 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_wicks' },
  ],
  'script.pickup_hushfrost_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A climber\'s cache on the terrace. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_balm' },
  ],
  'script.pickup_hushfrost_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In a wall-hollow: a STARGLASS SHARD, cold as the sky it fell from!' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_shard' },
  ],
  'script.pickup_hushfrost_warm_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'Left on the shelter\'s sill for whoever needs it. Found a WARM BALM!' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_warm_balm' },
  ],
  'script.pickup_hushfrost_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'By a blighted finger, untouched by the grey: a MOTH-AMBER!' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_amber' },
  ],
  // Lamplight reveal (spine §5, Radiant): a snow-hollow along the canyon wall,
  // visible only to a lamp that all but carries the dawn
  // (flag:lamplight_radiant derives in FlagStore, never hand-set).
  'script.pickup_hushfrost_hollow': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 2 },
    { op: 'say', text: 'A snow-hollow, white on white, that only a Radiant lamp could find. Inside: 2 BRIGHT BALMS!' },
    { op: 'say', text: 'You didn\'t beat the dark out of this pass. You out-shone it.' },
    { op: 'setFlag', flag: 'flag:picked_hushfrost_hollow' },
  ],

  // --- Aurora Hollow — the Emberward spur (X1's oil + the detour's own pay) --
  'script.pickup_aurora_oil': [
    { op: 'narrate', text: 'In the hollow\'s deepest pocket the aurora pools UNDER the ice, beside the old renderers\' sealed jars.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'aurora_oil', count: 1 },
    { op: 'say', text: 'One jar still holds true. Took the AURORA-OIL!' },
    { op: 'setFlag', flag: 'flag:picked_aurora_oil' },
  ],
  'script.pickup_aurora_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'An offering-box in the blue ice. Found 2 BEACON CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_aurora_charge' },
  ],
  'script.pickup_aurora_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Where the aurora burns brightest: a STARGLASS SHARD, green-lit to its heart!' },
    { op: 'setFlag', flag: 'flag:picked_aurora_shard' },
  ],

  // --- Sunken Solarium — arrival (the Arc D pivot: warmth, remembered) -------
  'script.solarium_arrival': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The fog thins, and the cold simply stops. Ahead, half-drowned in black water, a ruined sun-garden GLOWS.' },
    { op: 'tint', color: '#ffd089', alpha: 0.26, ms: 900 },
    { op: 'narrate', text: 'Stored daylight, shining up through the flood. Warmth on your face, for the first time since the south.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'narrate', text: 'They say the sun drowned here. In its light, you\'d swear it was only sleeping.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // E — the Last-Warm-Day (banded on the festival terrace). Bittersweet,
  // golden, a little defiant — the fire-warm swell AFTER the coldest regions.
  // The build-up may smile; the crest itself is sincere (humour rules).
  'script.solarium_last_warm_day': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 600 },
    { op: 'narrate', text: 'The sunlit terrace is full: daylight lanterns on every table, warm bread passed hand to hand. The Last-Warm-Day.' },
    { op: 'tint', color: '#ffd089', alpha: 0.3, ms: 900 },
    { op: 'musicCrossfade', key: 'sunken-solarium-b', ms: 1200 },
    { op: 'narrate', text: 'Once a year the Solarium spends a whole season\'s saved daylight at once, together, before the dark.' },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'say', speaker: 'FESTIVAL ELDER', text: 'Sit, Wayfarer. Eat something warm. The dark gets the rest of the year — today is OURS.' },
    { op: 'action', actor: 'player', action: 'sit' },
    { op: 'narrate', text: 'Somebody presses warm bread into your hands. Nobody asks if you earned it. Warmth, spent freely, knowing it fades.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1100 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // --- The Lit Stage (spine §5 shape #7) — Lucan's hook ----------------------
  'script.lucan_quest': [
    { op: 'say', speaker: 'LUCAN PYRE', text: 'STOP — hold the light just there! An apprentice with six Gleams, walking out of a frozen pass into MY festival. Perfect.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'They say the sun drowned here. I say it sleeps. Tonight the troupe plays the closing scene on a dark stage — three braziers, dead.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'A bond that remembers the sun? Then fetch the drowned daylight up, spark by spark.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: '[[Three sunmote phials]] wait in [[the flooded halls]], where only a called tide walks. Light my stage!' },
    { op: 'setFlag', flag: 'flag:q_west_stage' },
  ],

  // The three sunmote phials (Tidecall water; each lighting wakes the next glimmer).
  'script.sunmote_1': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'sunmote_phial', count: 1 },
    { op: 'say', text: 'On a drowned islet, warm through the glass: a SUNMOTE PHIAL!' },
    { op: 'setFlag', flag: 'flag:q_west_mote_1' },
  ],
  'script.sunmote_2': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'sunmote_phial', count: 1 },
    { op: 'say', text: 'The second phial, glowing from a far-shore pocket like a coin in a well!' },
    { op: 'setFlag', flag: 'flag:q_west_mote_2' },
  ],
  'script.sunmote_3': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'sunmote_phial', count: 1 },
    { op: 'say', text: 'The last phial, like a sunrise under glass. [[Back to the braziers]]!' },
    { op: 'setFlag', flag: 'flag:q_west_mote_3' },
  ],

  // The three braziers — escalating warmth; the troupe reacts per lighting.
  // (Trigger chain sets the brazier flags; the night-flower rows bloom per
  // lighting — a purely visual Sunsketch foreshadow.)
  'script.brazier_1': [
    { op: 'narrate', text: 'You pour the first phial into the cold brazier. Nothing — then the daylight takes the coals at once.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Gold light climbs the broken proscenium. Night-flowers along the rim BLOOM, leaning in like an audience.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'The troupe has gone very quiet. Out in the drowned halls, something else begins to glimmer.' },
  ],
  'script.brazier_2': [
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'narrate', text: 'The second phial. The brazier FLARES over the gilt and the painted sun, unlit in forty years.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.28, ms: 800 },
    { op: 'narrate', text: 'More night-flowers bloom. A player starts humming the overture, catches themselves, and doesn\'t stop.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 800 },
    { op: 'narrate', text: 'Two braziers burn. The last glimmer waits in [[the deepest hall]].' },
  ],
  'script.brazier_3': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The last phial, into the last brazier. You stand back.' },
    { op: 'silence', ms: 900 },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.36, ms: 1000 },
    { op: 'narrate', text: 'The stage lights WHOLE — three crowns of daylight, the last night-flowers blooming with a sound like rain starting.' },
    { op: 'narrate', text: 'The troupe walks into the light they\'ve waited forty years for. On the terrace, the festival rises to its feet.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1000 },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'HOUSE UP! The stage is LIT! When you\'re ready, [[the stage is yours]], apprentice. I have WAITED for this curtain.' },
    { op: 'musicCrossfade', key: 'sunken-solarium-b', ms: 1000 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // Lumenary 7 — Lucan Pyre, ON the lit stage. Win → gleam:solar + Sunsketch
  // (TRAINERS['lucan_pyre'] carries the grants). The binding Gleam cadence,
  // fire-warm — the Arc D pivot's payoff after the coldest regions.
  'script.lumenary_solarium': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'lucan_ready', facing: 'down' },
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'grand', text: 'Centre stage, apprentice! You woke my theatre spark by spark; now show me the bond that did it.' },
    { op: 'wait', ms: 500 },
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'grand', text: 'The closing scene, on a lit stage, for the first time since the night fell. Places... begin!' },
    { op: 'battle', trainer: 'lucan_pyre' },
    { op: 'musicFade', ms: 500 },
    { op: 'silence', ms: 1000 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.4, ms: 800 },
    { op: 'narrate', text: 'Lucan raises his lamp like a curtain call, and every daylight lantern lifts with it — a hundred small suns. Overhead, the Sun remembers how to shine.' },
    { op: 'gleam', element: 'solar' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'grand', text: 'The Solar Gleam stands! Seven relit! Forty years of "The Sun Returns" — eleven under a dark sky — and tonight the sky read the script!' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'No performer leaves unpaid. The [[Sunsketch]]: a pocket of daylight that blooms night-flowers into bridges.' },
    { op: 'say', speaker: 'LUCAN PYRE', text: 'The [[sun-vine bridge on the Climb]], west of here, will open for you now. And the Helia Vault... some doors deserve their reveal.' },
    { op: 'wait', ms: 600 },
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'bittersweet', text: 'Spend what\'s left of the warm day with us first. Encores are short. That\'s what makes them encores.' },
    { op: 'action', actor: 'player', action: 'bow' },
  ],

  // X2 "The Troupe's Sun-mask" — the post-stage troupe player's ask.
  'script.mask_quest': [
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'A small thing, Wayfarer. Our gilt sun-mask sank in the side room off the flooded halls. Forty years, and the sun\'s understudy is a PAINTED PLATE.' },
    { op: 'say', speaker: 'TROUPE PLAYER', text: '[[Dive the side room]] and bring our face home. Tonight the scene should wear its own gold.' },
    { op: 'setFlag', flag: 'flag:q_west_mask' },
  ],
  'script.pickup_sun_mask': [
    { op: 'narrate', text: 'In the drowned side room, something smiles up through the silt.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'sun_mask', count: 1 },
    { op: 'say', text: 'Recovered the GILT SUN-MASK — silt-scoured, smiling, still warm.' },
    { op: 'setFlag', flag: 'flag:picked_sun_mask' },
  ],
  'script.mask_done': [
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'The mask! Look at HIM. Silt in the smile, not a scratch on the gold.' },
    { op: 'narrate', text: 'She holds it to the brazier-light. The painted face and the stage wear the same warmth.' },
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'The scene wears its own sun tonight. Here — pressed from the mask\'s spare gilt, for luck.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'sun_charm', count: 1 },
    { op: 'say', text: 'Received the SUN CHARM!' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'And a share of the takings: 300 WICKS!' },
    { op: 'say', speaker: 'TROUPE PLAYER', text: 'Raise it toward a [[Solar-hearted kin]] and your lamp plays the remembered noon.' },
    { op: 'setFlag', flag: 'flag:q_west_mask_found' },
  ],

  // The troupe's two sight trainers on the flooded lanes (route class).
  'script.troupe_player_a': [
    { op: 'say', speaker: 'CALLA', text: 'A walker in the wings! House rule: nobody crosses in rehearsal without giving the understudies a scene.' },
    { op: 'battle', trainer: 'troupe_player_a' },
    { op: 'say', speaker: 'CALLA', text: 'Upstaged in my own water. Any daylight down there is SPOKEN FOR.' },
    { op: 'setFlag', flag: 'flag:troupe_player_a_beaten' },
  ],
  'script.troupe_player_b': [
    { op: 'say', speaker: 'ORSINO', text: 'HALT — sorry, act two\'s line, it comes out when I\'m nervous. One bout!' },
    { op: 'battle', trainer: 'troupe_player_b' },
    { op: 'say', speaker: 'ORSINO', text: 'Bravo. I\'ve died on stage a hundred times. That was the most convincing.' },
    { op: 'setFlag', flag: 'flag:troupe_player_b_beaten' },
  ],

  // The Lumenary green room — the region's rest point (the standing kit;
  // the Solarium is a ruin, not a town: the matron's hearth IS the inn).
  'script.solarium_rest': [
    { op: 'say', speaker: 'MATRON', text: 'In off the water, pilgrim. The green room keeps a warm corner for every walker.' },
    { op: 'heal' },
    { op: 'say', speaker: 'MATRON', text: 'Kin warm, boots dry, and the stage none the wiser.' },
  ],

  // Solarium caches (the standing variety; the shard is the flooded missable).
  'script.pickup_solarium_balm': [
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: 'A forgotten festival hamper. Found a WARM BALM and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_solarium_balm' },
  ],
  'script.pickup_solarium_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'In a bone column\'s crack, warm side up: a MOTH-AMBER. Found it!' },
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
    { op: 'say', text: 'A pilgrim\'s offering, seal unbroken. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_solarium_charge' },
  ],
  'script.pickup_solarium_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Deep in the flooded halls: a STARGLASS SHARD, glinting under the water!' },
    { op: 'setFlag', flag: 'flag:picked_solarium_shard' },
  ],

  // --- Sunvault Climb — the golden road's two sight trainers + the kit -------
  'script.sunvault_terracer': [
    { op: 'say', speaker: 'BEL', text: 'Mind the beds! Every lamp that climbs gets measured against the gold.' },
    { op: 'battle', trainer: 'sunvault_terracer' },
    { op: 'say', speaker: 'BEL', text: 'The garden leaned toward you the whole bout. It never does that for me, and I PRUNE it.' },
    { op: 'setFlag', flag: 'flag:sunvault_terracer_beaten' },
  ],
  'script.sunvault_skywatcher': [
    { op: 'say', speaker: 'TAM', text: 'You\'re climbing into the brightest sky in Vesperholm. Nothing goes up untested. I\'m the test.' },
    { op: 'battle', trainer: 'sunvault_skywatcher' },
    { op: 'say', speaker: 'TAM', text: 'Passed. When the dome takes your breath — that\'s not the climb. That\'s the sky.' },
    { op: 'setFlag', flag: 'flag:sunvault_skywatcher_beaten' },
  ],
  // X3 leg 1 — the star-reading from the high terrace (the N2 stillness pattern).
  'script.chart_sunvault': [
    { op: 'narrate', text: 'The junior watcher\'s first viewpoint. From the terrace rim you read seven constellations over the golden climb.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'One reading of three. The third, she said, is for the brave.' },
  ],
  'script.pickup_striker': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'watch_striker', count: 1 },
    { op: 'say', text: 'On a worn cord in the terrace: the old watcher\'s STRIKER. The Astral Walk\'s first lamp has waited years for it.' },
    { op: 'setFlag', flag: 'flag:picked_striker' },
  ],
  'script.pickup_sunvault_balm': [
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'A climber\'s reserve in the garden. Found a BRIGHT BALM!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_balm' },
  ],
  'script.pickup_sunvault_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: "A gardener's pay-tin under the stair. Found 250 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_sunvault_wicks' },
  ],
  'script.pickup_sunvault_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'On a shelf only a bloomed vine reaches: a MOTH-AMBER!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_amber' },
  ],
  'script.pickup_sunvault_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A sky-watcher\'s drop-box on the bridge post. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_charge' },
  ],

  // --- Helia Vault — the Sunsketch puzzle reliquary (3 blooms + the mirror) --
  'script.helia_bloom_1': [
    { op: 'narrate', text: 'You raise your lamp and release daylight over the shut vines.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.2, ms: 600 },
    { op: 'narrate', text: 'The double vine unfurls underfoot. The way on climbs to [[a ledge gold with light]].' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 600 },
  ],
  'script.helia_bloom_2': [
    { op: 'narrate', text: 'In the ledge\'s light, your daylight comes away richer — and the north vine answers.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'It opens like a hand. The rule: [[climb to the light, then lend it on]].' },
  ],
  'script.helia_bloom_3': [
    { op: 'narrate', text: 'The west vine BLOOMS — and you see the trouble: the great far vine, across a chasm no light can jump.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'But on [[the east spur]], something dish-shaped catches your lamp. A mirror.' },
  ],
  'script.helia_mirror': [
    { op: 'narrate', text: 'The stiff sun-mirror flower grinds round to face the far dark.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'narrate', text: 'Somewhere deeper, gold light lands where your hands cannot.' },
  ],
  'script.helia_bloom_far': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'narrate', text: 'The bent daylight lies across the chasm. You send your own light down it.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.3, ms: 900 },
    { op: 'narrate', text: 'The great vine WAKES — a bridge of flowers across the dark — and the reliquary lights from within.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
  ],
  'script.pickup_helia_relic': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'chart_sunburst_nova', count: 1 },
    { op: 'say', text: 'In a case of gold glass: a STAR-CHART: SUNBURST NOVA, the sun\'s remembered blaze!' },
    { op: 'say', text: 'The vault\'s hush approves. Probably.' },
    { op: 'setFlag', flag: 'flag:picked_helia_relic' },
  ],
  'script.pickup_helia_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'A keeper\'s offering-box under the vine. Found 2 BEACON CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_helia_charge' },
  ],

  // ===========================================================================
  // THE COLDFOG DETOUR (B4's shown half) — the drained land. ZERO humour in
  // this whole block; the register is elegiac, merciful-and-wrong. The kin are
  // asleep, never harmed; nothing is broken; that is the horror of it.
  // ===========================================================================

  // X3 leg 3 — the bravest reading: the one sky that gives nothing back.
  'script.chart_coldfog': [
    { op: 'narrate', text: 'The survey cairn above the deep fog. The reading "for the brave" — now you see why she wouldn\'t ask it outright.' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'There is nothing to read. The sky over the drained marsh is a held grey blank. You chart the absence. The absence is the finding.' },
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
    { op: 'narrate', text: 'Rows of null-lanterns on swept gantries, each holding its piece of dark. Not one is dusty. Somebody still tends them.' },
    { op: 'narrate', text: 'Each collar holds a chip of dark stone, faintly blue. Not fuel. Company.' },
    { op: 'narrate', text: 'At the far wall: a bell of held dark, polished like a font. It isn\'t running. The fen outside is proof of its work.' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'A brass gauge, lovingly kept. Its needle rests at zero — here, the finished number.' },
    // W-2 — Còr, wordless: the figure on the far gantry sweeps two tiles,
    // stops, turns, bows (a held wait) and walks out of frame. No line.
    { op: 'cameraFocus', actor: 'stillworks_cor', ms: 900 },
    { op: 'move', actor: 'stillworks_cor', to: { tx: 16, ty: 4 }, speed: 0.5 },
    { op: 'wait', ms: 600 },
    { op: 'face', actor: 'stillworks_cor', facing: 'down' },
    { op: 'wait', ms: 800 },
    { op: 'face', actor: 'stillworks_cor', facing: 'up' },
    { op: 'move', actor: 'stillworks_cor', to: { tx: 19, ty: 2 }, speed: 0.5 },
    { op: 'cameraReset', ms: 800 },
    { op: 'tint', color: '#202430', alpha: 0, ms: 1100 },
    { op: 'narrate', text: 'No one stops you. The works are quiet like a sleeping ward — and someone, gently, keeps them so.' },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // Coldfog caches (the drained fen's finds; the murk is dead — these sit on
  // what banks and islets the old road left).
  'script.pickup_coldfog_embergloss': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'embergloss', count: 1 },
    { op: 'say', text: 'At a snuffed wayshrine, resin the fog never cooled: EMBERGLOSS!' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_embergloss' },
  ],
  'script.pickup_coldfog_murk_pearl': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'murk_pearl', count: 1 },
    { op: 'say', text: 'In a shell that stopped closing years ago: a MURK PEARL!' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_murk_pearl' },
  ],
  'script.pickup_coldfog_drowned_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: 'A courier\'s strongtin where the road drowned: 250 WICKS. Whoever they were for is long past needing them.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_drowned_wicks' },
  ],
  'script.pickup_coldfog_camp_tonic': [
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'In the quieted camp, set out for a morning that never came: a BRIGHT BALM.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_camp_tonic' },
  ],
  'script.pickup_coldfog_bank_charm': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'On the high bank, in a waxed charm-bundle: a BEACON CHARGE. A light, hidden from the place that eats them.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_bank_charm' },
  ],
  'script.pickup_coldfog_keepers_cache': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'Laid out on the islet stone like a table for a guest: a BRIGHT BALM and a BEACON CHARGE.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_keepers_cache' },
  ],
  'script.pickup_coldfog_works_store': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In the works\' tidy store, shelved like an exhibit: a STARGLASS SHARD. You take it back outside.' },
    { op: 'setFlag', flag: 'flag:picked_coldfog_works_store' },
  ],

  // ===========================================================================
  // NIGHTREACH OBSERVATORY — the Vigil of the Seven (spine §5 shape #8, the
  // capstone ceremony walk) + the C4/A5/B4 cluster + Lumenary 8. Reverent,
  // vast; the cluster's ONE dry line lives with the inn guest.
  // ===========================================================================

  // Nessa's hook, from the eyepiece (interior; sets flag:q_west_vigil).
  'script.nessa_quest': [
    { op: 'narrate', text: 'Nessa does not look up from the eyepiece. You suspect she hasn\'t in years.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Seven, now. I watched the seventh come home from this chair.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Seven watch-lamps line [[the Astral Walk]], dark since the night fell. [[Light them in order]] — ember first, sun last. Then come tell the eighth.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'The first lamp wants [[the old watcher\'s striker]], lost on [[the Sunvault road]]. The rest want a steady hand.' },
    { op: 'setFlag', flag: 'flag:q_west_vigil' },
  ],

  // THE SEVEN LAMPS — each a remembrance of its region: the game remembering
  // itself, one constellation at a time. (Trigger chain banks the lamp flags.)
  // Lamp 1 — EMBER: Tinderwick's hearths, where the Wayfaring began.
  'script.west_lamp_1': [
    { op: 'narrate', text: 'The first watch-lamp. The old watcher\'s striker sparks, and the wick takes ember-orange: the colour of home.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ff8a3d', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Ember-light. Tinderwick, where a small flame is no lesser thing.' },
    { op: 'tint', color: '#ff8a3d', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'One of seven. Above you, the Ember settles like a hearth.' },
  ],
  // Lamp 2 — TIDE: Pearlmoor's bell, and the water that parts for the asking.
  'script.west_lamp_2': [
    { op: 'narrate', text: 'The second lamp burns cool and silver, swaying like harbour light.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Tide-light. Pearlmoor: a bell you gave back its rope, a quay singing the boats out. Tides go out so they can come back. So have you.' },
    { op: 'tint', color: '#4fb4ff', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'Two of seven. Somewhere very far south, you would swear, a bell answers.' },
  ],
  // Lamp 3 — VERDANT: Lowleaf's moss, the kept light that vouches.
  'script.west_lamp_3': [
    { op: 'narrate', text: 'The third lamp catches green-gold and holds it soft — the glow old moss gives when the dark is kind.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fe8b8', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Verdant-light. Lowleaf: an Elder Bed warmed back rim to rim, and a child saying, very clearly, "it was SLEEPING." Be like the moss.' },
    { op: 'tint', color: '#9fe8b8', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'Three of seven. The lamp glows on, unhurried. Sable would approve.' },
  ],
  // Lamp 4 — STONE: Cinderhead's vigil, the flame carried through the dark.
  'script.west_lamp_4': [
    { op: 'narrate', text: 'The fourth lamp is miner-made. Your flame steadies, patient as rock.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#caa46a', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Stone-light. Cinderhead: a vigil-lamp carried up through the leaning dark, never once out. Anyone can LIGHT a lamp; carrying one is the trick.' },
    { op: 'tint', color: '#caa46a', alpha: 0, ms: 700 },
    { op: 'narrate', text: 'Four of seven. You have been checking each kept flame behind you.' },
  ],
  // Lamp 5 — FROST: the aurora — and C4, Fenn's counsel. He lights it WITH
  // you; portrait + quiet, no swell. He does not march; he sends you up clear.
  'script.fenn_counsel': [
    { op: 'face', actor: 'fenn_counsel', facing: 'down' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Child. The frost-lamp burns the colour of patience. I hoped to catch you.' },
    { op: 'narrate', text: 'You tip the oil together, his old hand steadying the well. The wick takes pale and cool — aurora-light, indoors.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#a8f0d0', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Frost-light. Pale Vault: a town on black ice under the green roads of the sky, each holding one flame. Calm — but every light lit on purpose.' },
    { op: 'tint', color: '#a8f0d0', alpha: 0, ms: 700 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'Eight stars, nearly. You won\'t beat him up there, apprentice. You\'ll have to remember harder than he\'s forgotten.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'He will ask his question again, at the top of the world. Every lamp on your road is a word of your answer, already lit.' },
    { op: 'face', actor: 'fenn_counsel', facing: 'up' },
    { op: 'wait', ms: 700 },
    { op: 'face', actor: 'fenn_counsel', facing: 'down' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'I will not climb with you. Somebody should watch from here when the sky finishes. I have waited forty years for that view.' },
    { op: 'narrate', text: 'He presses your shoulder once. Five of seven. He stays, looking up.' },
    { op: 'face', actor: 'fenn_counsel', facing: 'up' },
  ],
  // Lamp 6 — STORM: the kites — and A5, Wren resolved (the warm mirror of A4).
  // The ribbon line fires only if N3 was kept (flag:q_north_ribbon_placed —
  // the per-step if_flag guard; purely optional colour). The friendly bout is
  // part of the reunion: A2's register, returned.
  'script.wren_nightreach': [
    { op: 'narrate', text: 'Somebody sits under the sixth watch-lamp, easy as a harbour evening.' },
    { op: 'face', actor: 'wren_return', facing: 'left' },
    { op: 'emote', actor: 'wren_return', emote: 'music' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Took you long enough. I watched four lamps come on — I know that walk.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'I went and looked at the quiet, like Còr wanted. Sat a day in one of his valleys, lamp shut. Peaceful as a held breath. ...I\'d rather breathe.' },
    { op: 'say', if_flag: 'flag:q_north_ribbon_placed', speaker: 'WREN', portrait: 'wren', expr: 'soft', text: 'And the ledge on the second stair — my ribbon, under a stone. No note. It smelled of festival smoke all the way down. That was you.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'So. Friendly rules, like the coast. One bout, to remember what this is all FOR — with the person I learnt it next to.' },
    { op: 'battle', trainer: 'wren_nightreach' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'soft', text: 'Ha. There it is. THAT\'s what the quiet doesn\'t have — and Còr\'s not getting it.' },
    { op: 'narrate', text: 'You light the sixth lamp together, Wren\'s hand over yours, laughing at nothing like at the start.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.22, ms: 700 },
    { op: 'narrate', text: 'Storm-light. Galehigh: a hundred small flames climbing the dark on kite-tails. Daft, maybe. The night is shorter for it.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 700 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'Six of seven. Come on — let\'s go light the last one.' },
    { op: 'hop', actor: 'wren_return' },
    { op: 'setFlag', flag: 'flag:wren_nightreach_battled' },
  ],
  // Lamp 7 — SOLAR: the stage — and B4, THE GREAT NULL NAMED. The information
  // set-piece: letterbox, Nessa's haunted portrait-register, a silence + one
  // cold tint on "aimed at the Keystar"; let it sit. (The trigger banks
  // flag:q_west_lamp_7 + flag:q_west_vigil_kept + flag:great_null_known.)
  'script.great_null_named': [
    { op: 'narrate', text: 'Nessa waits at the seventh lamp. You light it sun-gold, the colour of a drowned garden remembering.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.24, ms: 700 },
    { op: 'narrate', text: 'Solar-light. The Solarium: braziers fed out of the flood, a troupe back on a lit stage. Seven of seven.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 700 },
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'face', actor: 'nessa_at_seven', facing: 'down' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'reverent', text: 'Seven kept flames. I needed the walk lit before I showed you this — so you would know its size.' },
    { op: 'face', actor: 'nessa_at_seven', facing: 'left' },
    { op: 'narrate', text: 'She swings the telescope across, at the darkened central mountain.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'Look. The Umbral Spire\'s crown — the scaffolding on the north face, where no light catches. Two years he has been building it. Slowly, then all at once.' },
    { op: 'say', if_flag: 'flag:seen_stillworks', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'You have walked the Hollowfen — the sleeping lanterns, the gauge at zero. Then you have seen its little sister. The works were the rehearsal.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'He calls it the Great Null. A lantern that holds no light — aimed at the Keystar, the one we all rekindle from. Snuff that, and the sky stops being able to remember itself.' },
    { op: 'silence', ms: 1600 },
    { op: 'tint', color: '#2a3550', alpha: 0.4, ms: 900 },
    { op: 'narrate', text: 'Every constellation you relit held because the Keystar held. One star anchors it all — and the gentlest man in Vesperholm has built a dark to fit it.' },
    { op: 'tint', color: '#2a3550', alpha: 0, ms: 1100 },
    // W-1 — THE EMBER FLICKERS: the story's turn against the player. The
    // Keystar slips for a breath and the youngest star in the sky — your
    // first Gleam — goes dark, then catches again. (Witness stages at
    // Tinderwick key on flag:great_null_known and heal at gleam:lunar.)
    { op: 'silence', ms: 1200 },
    { op: 'cameraFocus', to: { tx: 15, ty: 29 }, ms: 900 },
    { op: 'narrate', text: 'Far to the south, low on the rim of the world, the Ember — your first Gleam — stutters. Dims. Is gone for one long heartbeat.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'tint', color: '#0b1026', alpha: 0.5, ms: 400 },
    { op: 'shake', ms: 300, intensity: 0.004 },
    { op: 'wait', ms: 1100 },
    { op: 'tint', color: '#0b1026', alpha: 0, ms: 1400 },
    { op: 'narrate', text: 'Then it catches again.' },
    { op: 'cameraReset', ms: 800 },
    { op: 'face', actor: 'nessa_at_seven', facing: 'down' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'The Keystar slipped. Only for a breath — but every star leans on it, and the first lights relit feel it first. Yours was the first.' },
    { op: 'wait', ms: 800 },
    { op: 'face', actor: 'nessa_at_seven', facing: 'left' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: '...I knew him, once. He was the gentlest of us. That\'s the part that keeps me awake.' },
    // W-3 — X-1 dose 2: the third ladder (never the name — not before dawn)
    { op: 'wait', ms: 700 },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'Ask Fenn about the third ladder. ...No. Don\'t ask. He\'ll tell you when he can bear to.' },
    { op: 'face', actor: 'nessa_at_seven', facing: 'down' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'reverent', text: 'The Crown wants one more star. [[Come down to the hall]] when you are ready — and after tonight, don\'t wait.' },
    { op: 'face', actor: 'nessa_at_seven', facing: 'left' },
    { op: 'narrate', text: 'She looks back along the lit walk, and the haunted look eases.' },
    { op: 'letterbox', on: false, ms: 420 },
  ],

  // The Astral Walk's two junior-watcher SIGHT keepers (keeper class).
  'script.junior_watcher_a': [
    { op: 'say', speaker: 'LIRA', text: 'Hold the walk! Nobody crosses unread — ESPECIALLY senior watchers.' },
    { op: 'battle', trainer: 'junior_watcher_a' },
    { op: 'say', speaker: 'LIRA', text: 'Read and recorded. ...In my own ledger, which nobody reads. Keep the order — [[ember-light first, sun-light last]].' },
    { op: 'setFlag', flag: 'flag:junior_watcher_a_beaten' },
  ],
  'script.junior_watcher_b': [
    { op: 'say', speaker: 'OS', text: 'A lamp on the high terrace! I keep the last stretch. Show me it keeps.' },
    { op: 'battle', trainer: 'junior_watcher_b' },
    { op: 'say', speaker: 'OS', text: 'It keeps. Walk soft — Nessa\'s been at the eyepiece three nights.' },
    { op: 'setFlag', flag: 'flag:junior_watcher_b_beaten' },
  ],

  // X3 "Charting the Dark" — Lira's quest (her beaten swap is the giver).
  'script.chart_quest': [
    { op: 'say', speaker: 'LIRA', text: 'A proper asking, now. I\'m charting the sky as it COMES BACK, and nobody else is writing it down.' },
    { op: 'say', speaker: 'LIRA', text: 'I need readings from [[the Sunvault terrace]] and [[our own roof terrace]] past the scree. For the brave ONLY: the cairn over the Coldfog Marches.' },
    { op: 'say', speaker: 'LIRA', text: 'Stand in them till you\'re cold. The third would make it TRUE.' },
    { op: 'setFlag', flag: 'flag:q_west_chart' },
  ],
  // X3 leg 2 — the roof-terrace reading (the observatory's own sky).
  'script.chart_observatory': [
    { op: 'narrate', text: 'The roof terrace. Overhead, the densest starfield in Vesperholm.' },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'You take the reading slowly; hurrying it would be a kind of lie. Two kept.' },
  ],
  // X3 done — requires _1 + _2 only (Coldfog's _3 stays the optional, bravest
  // leg, never demanded). The finished chart NAMES STARWELL — the tease-closer.
  'script.chart_done': [
    { op: 'say', speaker: 'LIRA', text: 'The terrace AND the roof — sit down, talk, slowly, I\'m pressing as you speak—' },
    { op: 'narrate', text: 'She works fast, glancing at you, not the sky. Seven constellations fill the chart — and the start of an eighth.' },
    { op: 'say', speaker: 'LIRA', text: 'There. The sky, coming BACK. And here, where the old charts go quiet...' },
    { op: 'narrate', text: 'Her finger rests on a figure inked at the Penumbra\'s edge: a well of starlight. Under it: STARWELL.' },
    { op: 'say', speaker: 'LIRA', text: 'The old charts say it\'s real — a shrine of fallen starlight [[inside the dark ring]], found when the Crown is whole. Stand in THAT view for me, one day.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveMoney', amount: 400 },
    { op: 'say', text: 'Her chart-fund: 400 WICKS. "Readings are PAID. That\'s a survey."' },
    { op: 'setFlag', flag: 'flag:q_west_chart_done' },
  ],
  // R5 "A Chart for the Waykeeper" — the Round's last leg, the take side.
  'script.round_chart_take': [
    { op: 'say', speaker: 'LIRA', text: 'One more thing — an honour, not an errand. The Waykeeper at the Crossroads hangs a chart on the Waystone yearly. He\'s not had a TRUE one in eleven.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'round_chart', count: 1 },
    { op: 'say', text: 'A fresh pressing of the relit sky. Received the FRESH STAR-CHART!' },
    { op: 'say', speaker: 'LIRA', text: '[[Take it to the Waykeeper]]. Tell him the sky\'s worth charting again.' },
    { op: 'setFlag', flag: 'flag:q_round_chart_taken' },
  ],
  // R5, the delivery (the Crossroads Waykeeper) — the Round comes full circle.
  'script.round_chart_deliver': [
    { op: 'say', speaker: 'WAYKEEPER', text: 'A Nightreach seal! Eleven YEARS I\'ve hung guesswork on this stone—' },
    { op: 'narrate', text: 'He unrolls it against the Waystone and goes still: seven constellations, true; an eighth sketched faint. He hangs it slowly, the way a Gleam is given.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'narrate', text: 'The fresh chart hangs lamp-lit on the Waystone. Travellers stop to point.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'The Round\'s last leg, walked in style. Round rates — plus the years.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 400 },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'Received 400 WICKS and a BRIGHT BALM!' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Kite, moss, letters, lamps, and the sky — the Round is KEPT this year.' },
    { op: 'setFlag', flag: 'flag:q_round_chart' },
  ],

  // E — the Star-vigil (the warden of the watch, on the temple steps): the
  // grandest, most reverent festival — kept in silence, BEFORE the eighth
  // lights; it crests with the Lunar Gleam in the hall. No humour.
  'script.nightreach_star_vigil': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'The whole town stands on the temple steps, faces up, each with one unlit lamp. Nobody speaks. This is the Star-vigil.' },
    { op: 'narrate', text: 'Seven watchers stand apart, lamps LIT — one for each star come home.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fd4ff', alpha: 0.18, ms: 900 },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'narrate', text: 'A watcher nods toward the eighth row of unlit lamps, and the empty place at its end. Nobody says it is yours. Everybody knows it is.' },
    { op: 'tint', color: '#9fd4ff', alpha: 0, ms: 900 },
    { op: 'wait', ms: 900 },
    { op: 'narrate', text: 'You stand the watch a while, so someone is watching when the sky remembers.' },
    { op: 'letterbox', on: false, ms: 420 },
    { op: 'setFlag', flag: 'flag:star_vigil_seen' },
  ],

  // Lumenary 8 — Nessa Cole, under the great eyepiece. Win → gleam:lunar +
  // Starreach; the ENGINE derives crown_west + hub_unlocked (last quadrant).
  // THE GRANDEST Gleam cadence of the eight: silence cresting exactly as the
  // eighth constellation lights, each watcher's lamp a small flashColor.
  'script.lumenary_nightreach': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'nessa_ready', facing: 'down' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'reverent', text: 'The walk is lit, the vigil kept. One asking remains — mine.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'neutral', text: 'My kin keep the dream-hours: the soft dark that closes your eyes for you. Còr calls it mercy. Stay awake through it.' },
    { op: 'battle', trainer: 'nessa_cole' },
    { op: 'musicFade', ms: 600 },
    { op: 'silence', ms: 1800 },
    { op: 'narrate', text: 'Nessa crosses to the eighth watch-lamp, the one no striker has touched, and waits, face turned up.' },
    { op: 'face', actor: 'nessa_ready', facing: 'up' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#9fd4ff', alpha: 0.3, ms: 1100 },
    { op: 'narrate', text: 'The eighth watch-lamp lights itself, kindled from above.' },
    { op: 'gleam', element: 'lunar' },
    { op: 'narrate', text: 'Outside, the Star-vigil crests in silence: lamp after lamp catching light under a finished sky.' },
    { op: 'flashColor', color: '#cfe8ff', ms: 260 },
    { op: 'flashColor', color: '#cfe8ff', ms: 260 },
    { op: 'flashColor', color: '#ffd089', ms: 300 },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 1200 },
    { op: 'tint', color: '#9fd4ff', alpha: 0, ms: 1200 },
    { op: 'narrate', text: 'Eight stars. The Skyweave Crown closes, quiet as snowfall — and the Penumbra parts: the mountain road [[north of the Crossroads]] opens. Toward him.' },
    { op: 'narrate', if_flag: 'flag:wren_nightreach_battled', text: 'At the hall door, Wren leans on the frame, lamp held up among the others, grinning like the coast road. Same road, different lamps.' },
    { op: 'face', actor: 'nessa_ready', facing: 'down' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'reverent', text: 'The Lunar Gleam — and the whole Crown with it. All my life I have watched this sky. Tonight it watched back.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Take the Starreach: starlight to stand on. [[Stride across the short voids]] of pure dark — the Penumbra\'s last crossings will hold you now.' },
    { op: 'say', speaker: 'NESSA COLE', text: 'Stand the vigil\'s end with us, then [[go down to the Crossroads]]. One night with nothing missing.' },
  ],

  // Rest + caches (the standing kit; "The Long Watch" inn).
  'script.nightreach_inn_rest': [
    { op: 'say', speaker: 'INNKEEP', text: 'In quietly — half my guests sleep by day. The bunks are warm.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Rested, kin and all. The watch keeps the sky; you needn\'t — not tonight.' },
  ],
  'script.pickup_nightreach_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'On the roof terrace, under the densest stars: a STARGLASS SHARD. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_nightreach_shard' },
  ],
  'script.pickup_nightreach_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: "A watcher's pay-purse, never missed. Found 300 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_nightreach_wicks' },
  ],
  'script.pickup_nightreach_charge': [
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A vigil drop-box by the temple steps, seal sound. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_nightreach_charge' },
  ],
  'script.pickup_nightreach_balm': [
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'In the fog-gate\'s lee: a BRIGHT BALM. Found it!' },
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
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Child. Of course I am here. I watched the eighth star come home.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'You cannot out-fight Còr; he is not your enemy. Go up there to remember louder than he can grieve. That is the whole of my counsel.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'grave', text: 'The Keystar\'s heart, the Keylumen, wants asking, not winning. I sent something up [[the inward road]] with a friend. Spend it nowhere else.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'I will be here, watching the sky. When it changes — and it will, child — I should like to stand where your road began.' },
    // The Three Hours' foreshadow payoff (07-the-three §6) — optional colour,
    // played only if the player has already stood before the Lost Hour.
    { op: 'say', if_flag: 'flag:three_dawn_met', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'So you found the third watch. Still facing east? ...Then it never stopped believing. Neither have I. Go and prove us right.' },
    { op: 'narrate', text: 'He presses your shoulder once, as at the very start. He does not say goodbye. Lamp-tenders never do.' },
    { op: 'setFlag', flag: 'flag:fenn_counsel_given' },
  ],

  // --- A5→A6 — Wren joins for the climb (the inward road's full-cut band; also
  // the Wren NPC standing at the roadside). Carries Fenn's Starlamp up with
  // them, so the Keylumen's asking-gift is banked on the only road in.
  'script.wren_joins': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'There you are. I watched the fog go down and thought — any minute.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'I went all the way round it. The Hollowing. They\'re right that it hurts. ...I just don\'t think "never again" is worth "never at all."' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'I\'m not letting you climb alone. Same road, different lamps.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: 'Oh — the old man sent this. Held it like somebody\'s heart.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starlamp', count: 1 },
    { op: 'say', text: 'Received the STARLAMP! Forty years Fenn kept it, for one asking.' },
    { op: 'setFlag', flag: 'flag:wren_joined' },
  ],

  // --- C1 "Lampling's Trail" — the Waystone kid's lamp-flickers (three
  // guttering dusk-lamps around the plaza, then the trail's end at the fourth).
  'script.lampling_trail_start': [
    { op: 'say', speaker: 'WAYSTONE KID', text: 'Psst! The plaza lamps keep GUTTERING — like something\'s tasting them!' },
    { op: 'say', speaker: 'WAYSTONE KID', text: '[[Follow the flickers]]! [[Start at the north-west lamp]]!' },
    { op: 'setFlag', flag: 'flag:q_central_trail' },
  ],
  'script.trail_lamp_1': [
    { op: 'narrate', text: 'The flame dips — a teacup-sized curl of light whisks out and away.' },
    { op: 'narrate', text: 'Draughts don\'t look back at you. The next flicker: [[the north-east lamp]].' },
  ],
  'script.trail_lamp_2': [
    { op: 'narrate', text: 'The flame here still wobbles, delighted. The glass hums, faint and fond.' },
    { op: 'narrate', text: 'The little light circles the post and streaks off toward [[the south-west lamp]].' },
  ],
  'script.trail_lamp_3': [
    { op: 'narrate', text: 'There: a tiny lantern-shaped kin INSIDE the lamp, warming its hands.' },
    { op: 'narrate', text: 'It blushes gold and pours away to [[the last lamp]] of the ring. Waiting.' },
  ],
  'script.lampling_catch': [
    { op: 'narrate', text: 'The little kin sits on the lamp, glowing. The trail was an introduction.' },
    { op: 'legendaryBattle', name: 'lampling', kin: 148, level: 30, caughtFlag: 'flag:lampling_caught', cooldownBattles: 3, cooldownRef: 'npc.lampling_shy' },
    { op: 'narrate', text: 'The Lampling settles in like a wick into wax. All four lamps brighten.' },
    { op: 'setFlag', flag: 'flag:q_central_trail_done' },
  ],

  // --- C2 "The Inn's Empty Lamps" — the waystation innkeeper's four festival
  // lamps (one lamp-token per quadrant's festival, hung in fixed order
  // south→east→north→west via the boolean chain). Every stage rest-heals and
  // opens the counter: the hub is the last shop and bed before the mountain.
  'script.inn_empty_lamps': [
    { op: 'say', speaker: 'INNKEEP', text: 'In you come — kettle\'s on, bunks are warm. This inn feeds every road.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Rested. ...Look up: four lamp-brackets, empty since the night fell.' },
    { op: 'say', speaker: 'INNKEEP', text: '[[Bring me a lamp-token]] from each festival, south first: Tide-blessing, Lamp-down, Aurora-watch, Star-vigil. Fill my brackets, I\'ll fill your hand.' },
    { op: 'setFlag', flag: 'flag:q_central_tokens' },
    { op: 'say', speaker: 'INNKEEP', text: 'The counter\'s open. The mountain doesn\'t keep a till.' },
    { op: 'shop', shop: 'crossroads_inn' },
  ],
  'script.inn_rest_waiting': [
    { op: 'say', speaker: 'INNKEEP', text: 'Back again! Bunks are yours, same as ever.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Rested. The brackets still want tokens: [[south, east, north, west]].' },
    { op: 'shop', shop: 'crossroads_inn' },
  ],
  'script.inn_lamps_hang': [
    { op: 'say', speaker: 'INNKEEP', text: 'All FOUR. Hand them here — no, stay, you should see this done properly.' },
    { op: 'narrate', text: 'She melts each token into a bracket and lights them in the Gleams\' order.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.22, ms: 900 },
    { op: 'narrate', text: 'Four festivals burn over one hearth where every road meets. The long table goes quiet — the good kind of quiet.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'INNKEEP', text: 'Fair\'s fair: a year\'s festival wax, round my own wick. Throw it well.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'radiant_lamp', count: 1 },
    { op: 'say', text: 'Received the RADIANT LAMP!' },
    { op: 'setFlag', flag: 'flag:q_central_tokens_done' },
    { op: 'heal', sleep: false }, // a courtesy top-up after the ceremony, not a bed
    { op: 'say', speaker: 'INNKEEP', text: 'Bunks and counter are yours whenever. This hearth remembers its lamp-fillers.' },
    { op: 'shop', shop: 'crossroads_inn' },
  ],
  // The done stage — the inn at full warmth. Carries the region's ONE sanctioned
  // warm send-off line (humour-sheet: innkeeper's patter; a smile, not a laugh).
  'script.inn_rest_crossroads': [
    { op: 'say', speaker: 'INNKEEP', text: 'In you come — four festivals over the hearth. Bunks first, talk after.' },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: 'There. Rested. Off up the mountain? Mind you come back down — I\'ve been keeping your bunk free, and an empty bed is TERRIBLE for business.' },
    { op: 'shop', shop: 'crossroads_inn' },
  ],

  // --- C3 "The Long Round" — the Waykeeper, once the Round's last leg is kept
  // (flag:q_round_chart ⇒ all five legs, the boolean chain). One last walk of
  // the plaza lamps; the keepsake; the Lamplight tease.
  'script.long_round': [
    { op: 'say', speaker: 'WAYKEEPER', text: 'The whole Round, in one pair of boots. Indulge an old keeper: one last walk of my plaza lamps before the inward road. That\'s how a Round was closed.' },
    { op: 'narrate', text: 'You walk the lamps with him. At each, he touches the post: counting them home.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Forty years I kept this Round alone. Now it\'s KEPT.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'way_lamp', count: 1 },
    { op: 'say', text: 'Received the WAY-LAMP — the Waykeeper\'s own hand-lamp, retired this very hour.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Keep it by you. The night will show you more than it used to.' },
    { op: 'setFlag', flag: 'flag:q_central_round_done' },
  ],

  // --- C2's four token givers — riding the festival NPCs' post-gleam stages in
  // their towns. Each replays the festival line, then hands the token only once
  // the chain has reached it (the per-step if_flag carries the south→east→
  // north→west order; until then the stage is plain festival colour and stays).
  'script.token_south': [
    { op: 'dialogue', ref: 'npc.blessing_singer' },
    { op: 'say', if_flag: 'flag:q_central_tokens', speaker: 'BLESSING SINGER', text: 'The inn\'s filling its brackets? The going-out song was for travellers too!' },
    { op: 'sfx', if_flag: 'flag:q_central_tokens', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:q_central_tokens', item: 'lamp_token_south' },
    { op: 'say', if_flag: 'flag:q_central_tokens', text: 'A wax token, a bell over water. Received the LAMP-TOKEN (SOUTH)!' },
    { op: 'setFlag', if_flag: 'flag:q_central_tokens', flag: 'flag:q_token_south' },
  ],
  'script.token_east': [
    { op: 'dialogue', ref: 'npc.vigil_raised_a' },
    { op: 'say', if_flag: 'flag:q_token_south', speaker: 'VIGIL MINER', text: 'For the Lamp-down bracket? Take the vigil with you, friend — dimmed and relit.' },
    { op: 'sfx', if_flag: 'flag:q_token_south', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:q_token_south', item: 'lamp_token_east' },
    { op: 'say', if_flag: 'flag:q_token_south', text: 'A token: a flame dimmed, then relit. Received the LAMP-TOKEN (EAST)!' },
    { op: 'setFlag', if_flag: 'flag:q_token_south', flag: 'flag:q_token_east' },
  ],
  'script.token_north': [
    { op: 'dialogue', ref: 'npc.pale_vault_gleam_watcher' },
    { op: 'say', if_flag: 'flag:q_token_east', speaker: 'AURORA WATCHER', text: 'The four festivals, together? The watch is honoured. One lamp, really.' },
    { op: 'sfx', if_flag: 'flag:q_token_east', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:q_token_east', item: 'lamp_token_north' },
    { op: 'say', if_flag: 'flag:q_token_east', text: 'In silence, a token: one held flame. Received the LAMP-TOKEN (NORTH)!' },
    { op: 'setFlag', if_flag: 'flag:q_token_east', flag: 'flag:q_token_north' },
  ],
  'script.token_west': [
    { op: 'dialogue', ref: 'npc.nightreach_festival_a' },
    { op: 'say', if_flag: 'flag:q_token_north', speaker: 'STAR-VIGIL WATCHER', text: 'The last bracket? Then the Star-vigil closes the ring, as it closed the Crown.' },
    { op: 'sfx', if_flag: 'flag:q_token_north', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:q_token_north', item: 'lamp_token_west' },
    { op: 'say', if_flag: 'flag:q_token_north', text: 'A watcher\'s lamp, in wax. Received the LAMP-TOKEN (WEST)! [[Back to the inn]].' },
    { op: 'setFlag', if_flag: 'flag:q_token_north', flag: 'flag:q_token_west' },
  ],

  // --- THE PENUMBRA RING — the threshold register: the held breath, not a beat.
  // No progression flag (the trigger banks the presentational once-only).
  'script.penumbra_threshold': [
    { op: 'musicFade', ms: 900 },
    { op: 'silence', ms: 2000 },
    { op: 'narrate', text: 'The dark here has edges. What is left of it does not want you.' },
    { op: 'narrate', text: 'Your lamp-glow is the only colour in the world. Off the north rim, something vast holds the sky out: the Umbral Spire, wearing the last of the night.' },
    { op: 'say', if_flag: 'flag:wren_joined', speaker: 'WREN', portrait: 'wren', expr: 'neutral', text: '...Keep your lamp up. A year ago this was a wall nobody could pass.' },
    { op: 'musicCrossfade', key: 'penumbra-ring-a', ms: 1600 },
  ],
  'script.pickup_penumbra_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'On the void-field islet, carried by starlight: a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_penumbra_shard' },
  ],
  'script.pickup_penumbra_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 600 },
    { op: 'say', text: "A courier's satchel, lost at the old fog-line for years. Found 600 WICKS!" },
    { op: 'setFlag', flag: 'flag:picked_penumbra_wicks' },
  ],

  // --- STARWELL — the well of fallen starlight, and Lunaveil (the SILENCE
  // register: the quietest set-piece in the game; a chance, not a gift).
  'script.starwell_lunaveil': [
    { op: 'musicFade', ms: 900 },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'The pool stirs, the way a sleeper stirs when a lamp is carried into the room.' },
    { op: 'narrate', text: 'A vast wing crosses the starlight, soundless, trailing veils of pale dusk — and the Lunaveil settles on the basin rim, eyes like the moment before moonrise.' },
    { op: 'legendaryBattle', name: 'lunaveil', kin: 132, level: 54, caughtFlag: 'flag:lunaveil_caught', cooldownBattles: 12, cooldownRef: 'npc.starwell_still' },
    { op: 'narrate', text: 'The Lunaveil folds into your lamp — vast, then gone, then quietly THERE.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'The well\'s light eases. The water keeps shining anyway.' },
  ],
  // --- THE NULL-WORKS — Nullmajor (#150), the great dark made kin. Post-dawn
  // only (the trigger carries requires_flag:'flag:dawn'); the SILENCE register,
  // Arc B's very last echo: Cor's null, woken gently — never destroyed.
  'script.nullworks_nullmajor': [
    { op: 'musicFade', ms: 900 },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'The null-pool never reflects your lamp. This morning, something does.' },
    { op: 'narrate', text: 'The gathered dark rises, courteous as its maker learned to be, in the shape of a kin: the Nullmajor, the night Còr built, wanting a steady hand.' },
    { op: 'legendaryBattle', name: 'nullmajor', kin: 150, level: 60, caughtFlag: 'flag:nullmajor_caught', cooldownBattles: 12, cooldownRef: 'npc.nullworks_still' },
    { op: 'narrate', text: 'The dark folds into your lamp without a sound — not extinguished, KEPT. The lamp is for the dark. It always was.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'The pool settles into plain water. The null-works have nothing left to hold.' },
  ],

  'script.pickup_starwell_amber': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'At the frozen pool\'s edge, like an offering: a MOTH-AMBER. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_starwell_amber' },
  ],

  // --- THE UMBRAL SPIRE — the ascent of the Ninth Lantern. The acolytes are
  // small griefs: each a PERSON doing a careful, terrible kindness. Gentle asks,
  // sad-not-bitter defeats, no mook energy, zero humour.
  'script.hollowing_acolyte_a': [
    { op: 'say', speaker: 'MERRIN', text: 'You shouldn\'t be up here, apprentice. ...Thirty years I dipped wicks in a coast-town chandlery. I know good lamp-work when it walks in.' },
    { op: 'say', speaker: 'MERRIN', text: 'That is WHY I\'m here. Every wick I dipped burned down while somebody watched. Your kin will only sleep. ...Won\'t you let us be kind to it?' },
    { op: 'battle', trainer: 'hollowing_acolyte_a' },
    { op: 'say', speaker: 'MERRIN', text: '...Still burning. Go on — the gate was never locked.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_a_beaten' },
  ],
  'script.hollowing_acolyte_b': [
    { op: 'say', speaker: 'TACE', text: 'Mind the alcoves, please — they\'re sleeping. ...I kept a ferry once. Twenty years carrying people home to lamps gone out by the time we docked.' },
    { op: 'say', speaker: 'TACE', text: 'The Warden was the first who didn\'t tell me it gets easier. He said it could STOP. Put your kin down gently, and it stops tonight — for everyone.' },
    { op: 'battle', trainer: 'hollowing_acolyte_b' },
    { op: 'say', speaker: 'TACE', text: '...No. You\'re the sort who docks at the dark jetty and lights it anyway.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_b_beaten' },
  ],
  'script.hollowing_acolyte_c': [
    { op: 'say', speaker: 'IVORWEN', text: 'Hush, dear — softly through here. I tuck them in myself, every one. ...I nursed my husband\'s lamp four winters at the end. I know how heavy watching is.' },
    { op: 'say', speaker: 'IVORWEN', text: 'Nobody up here is angry at the light, child. We just couldn\'t hold it any more. Let me take yours a while — you\'ve carried it so terribly far.' },
    { op: 'battle', trainer: 'hollowing_acolyte_c' },
    { op: 'say', speaker: 'IVORWEN', text: '...Four winters, and I\'d have kept a fifth. That\'s what I wasn\'t letting myself remember. ...Go up, dear. Mind the draught on the stair.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_c_beaten' },
  ],
  'script.hollowing_acolyte_d': [
    { op: 'say', speaker: 'HARL', text: 'Far enough. ...I was a Cinderhead man, deep-galleries. Carried my crew\'s eight lamps home the bad year — and none of the hands that hung them.' },
    { op: 'say', speaker: 'HARL', text: 'The mountain taught me to outlast. The Warden taught me what for. Nothing passes this gallery that the dark could hurt.' },
    { op: 'battle', trainer: 'hollowing_acolyte_d' },
    { op: 'say', speaker: 'HARL', text: '...You out-lasted me. The deep way. ...Eight lamps, Wayfarer. If you can keep yours lit where I couldn\'t — keep theirs lit too.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_d_beaten' },
  ],
  'script.hollowing_acolyte_e': [
    { op: 'say', speaker: 'SEFA', text: 'Hear the wind? ...My wife lit the north roads every dusk for eleven years. One dusk the fog put them out faster than she could walk.' },
    { op: 'say', speaker: 'SEFA', text: 'I am not here because I stopped loving lamplight. I am here because I couldn\'t watch it lose again. Please — be tired. Be sensible. Be SPARED.' },
    { op: 'battle', trainer: 'hollowing_acolyte_e' },
    { op: 'say', speaker: 'SEFA', text: '...She would have liked you. She was exactly this stubborn. ...Go on up. And if the sky changes — light the north roads first. For me.' },
    { op: 'setFlag', flag: 'flag:hollowing_acolyte_e_beaten' },
  ],

  // The Spire gatehouse camp — the climb's heal anchor (the C5 panel's MAJOR:
  // a blackout on the mountain respawned at Tinderwick with no rest closer than
  // the crossroads inn). Wren holds the gatehouse fire while you climb — the
  // standing inn-rest kit, staged as the A5 side-by-side promise kept. The f3
  // shaft compressor makes the descent-to-rest two rooms, not four floors.
  'script.spire_wren_camp': [
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'So this is where the dusk lives. ...Tidier than I expected. Stay close — I didn\'t climb all this way to lose you.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'I\'ve got the gatehouse brazier going — don\'t tell the management. Sit a minute. Lamps and kin first; heroics keep.' },
    { op: 'heal' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: 'There. Whatever\'s up there gets both of us at our best. Same road, different lamps — go on. I\'ll keep the fire.' },
  ],

  // The look-up bands: the Skyweave Crown through the open shafts (atmosphere
  // only — the darkest place in the game, under the greatest light).
  'script.spire_crown_1': [
    { op: 'narrate', text: 'Through the gatehouse\'s broken shaft, the night is FULL: the Skyweave Crown complete, its light falling down the mountain like rain into a well.' },
    { op: 'tint', color: '#9fd4ff', alpha: 0.16, ms: 900 },
    { op: 'narrate', text: 'The darkest place in Vesperholm, beneath the greatest light it has ever raised. Every lamp you lit looks back down the climb with you.' },
    { op: 'tint', color: '#9fd4ff', alpha: 0, ms: 900 },
  ],
  'script.spire_crown_2': [
    { op: 'narrate', text: 'Another shaft; another column of Crown-light. The null-works hum below the floor — and the starlight comes down anyway, waiting to be answered.' },
  ],
  // The high-gallery breather: the wind above the world + the shaft hoist
  // (sets flag:spire_shaft via the trigger — the sanctioned re-climb compressor).
  'script.spire_wind': [
    { op: 'narrate', text: 'The gallery opens to the night, and there is WIND — the sky\'s own breath, this deep in the mountain. Every star you relit hangs above the shaft.' },
    { op: 'narrate', text: 'An old hoist-lamp waits at the shaft\'s lip, oil long set. You warm it with your own flame until it remembers its work.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'A thread of starlight steadies down the spire\'s open core — the old hoist-line, lit end to end. The climb keeps [[a road home]] now.' },
  ],
  'script.pickup_spire_gatehouse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 2 },
    { op: 'say', text: 'A dead Lumenary\'s vestry chest, still sound: two BRIGHT BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_spire_gatehouse' },
  ],
  'script.pickup_spire_landing': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'On the hidden side-landing: a STARGLASS SHARD and a BRIGHT BALM!' },
    { op: 'setFlag', flag: 'flag:picked_spire_landing' },
  ],
  'script.pickup_spire_gallery': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 800 },
    { op: 'say', text: "A toll-box from the lit years: 800 WICKS that never made it down!" },
    { op: 'setFlag', flag: 'flag:picked_spire_gallery' },
  ],

  // --- THE SUMMIT CHAIN ------------------------------------------------------
  // 1. The Great Null, SEEN (B5's reveal — the player has known its name since
  // Nightreach; no re-explaining, just the scale of it and the swept floor).
  'script.great_null': [
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 900 },
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'silence', ms: 2200 },
    { op: 'cameraFocus', to: { tx: 11, ty: 4 }, ms: 1400 },
    { op: 'narrate', text: 'It fills the summit the way held breath fills a room: a bell of patient dark, aimed with terrible courtesy at the one star that lets the others rekindle.' },
    { op: 'narrate', text: 'The Great Null. You have carried its name up half a world. Nothing prepared you for how QUIET it is.' },
    { op: 'wait', ms: 600 },
    { op: 'narrate', text: 'At its foot, a gauge rests at zero. The floor has been swept — carefully, by someone who still believes tidiness is a kindness you can do the dark.' },
    { op: 'cameraReset', ms: 1000 },
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
    { op: 'face', actor: 'warden_cor', facing: 'up' },
    { op: 'silence', ms: 2000 },
    { op: 'narrate', text: 'He stands with his back to you, hands folded, watching the Keystar the way others watch a hearth. He has known you were coming for eight constellations.' },
    { op: 'wait', ms: 900 },
    { op: 'face', actor: 'warden_cor', facing: 'down' },
    { op: 'wait', ms: 500 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'You climbed kindly. My people sleep unhurt below — I notice these things. I watched your lamps come up my dark like a slow sunrise.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'I had hoped you\'d be tired enough to agree. You\'ve seen the quieted towns. I am not cruel, apprentice. I only want the grieving to stop.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'gentle', text: 'One lamp — this last anchoring light — left gently unlit, and the long night settles soft over every valley tired of losing things. No more goodbyes. No more counting a wick\'s hours and calling it hope.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'You could simply stop. That is all I have ever asked of anyone. Set the lamp down, apprentice — and the dark need never take anything from you again.' },
    { op: 'say', if_flag: 'flag:wren_joined', speaker: 'WREN', portrait: 'wren', expr: 'resolved', text: '...Don\'t argue with him. You can\'t. Remember louder. Go on — I\'m right here.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'narrate', text: 'You raise the vesperlamp. It is the only answer you have ever had — and tonight it is bright enough to be one.' },
    { op: 'wait', ms: 700 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: '...So be it. I will not pretend I hoped otherwise. Nor that some old, unhelpful corner of me is not proud of you.' },
    { op: 'letterbox', on: false, ms: 300 },
    { op: 'action', actor: 'warden_cor', action: 'bow' },
    { op: 'battle', trainer: 'warden_cor' },
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 700 },
    { op: 'silence', ms: 2200 },
    { op: 'action', actor: 'warden_cor', action: 'kneel', holdMs: 1400 },
    { op: 'narrate', text: 'His kin sleep where they fell, unhurt. He gathers them in with a murmur each, like a man banking a fire. He is not beaten. Nothing about him is beaten.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'Well kept. ...But the battle proves nothing. Grief always loses the argument — and then it stays anyway, and keeps the house.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'grave', text: 'So. Say your piece. I made most of the arguments in Vesperholm myself, in this dark. Say something I have not already grieved past.' },
    { op: 'narrate', text: 'You do not argue. You lift the vesperlamp between you — and let it remember.' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.1, ms: 800 },
    { op: 'narrate', text: 'EMBER — a coast-town fair under strung lanterns: a small flame is no lesser thing. TIDE — a moor-bell rolling out over lantern-lit boats, a quay lending the sea its lamps.' },
    { op: 'narrate', text: 'VERDANT — a hollow where the moss flowered all at once and outshone its lantern-strings. STONE — a mining town dimming every lamp to honour its dark, then lighting every one again.' },
    { op: 'tint', color: '#ffd089', alpha: 0.2, ms: 800 },
    { op: 'narrate', text: 'STORM — a hundred small flames climbing the night on kite-tails, so the stars had something to answer. FROST — a town on black ice in silence, every flame held in a bare hand, every flame CHOSEN.' },
    { op: 'narrate', text: 'SOLAR — the last warm day, spent gladly in front of the watching dark, knowing it fades; that being the point. LUNAR — a town that watches all night, so the sky is never once alone.' },
    { op: 'flashColor', color: '#ffd089', ms: 260 },
    { op: 'tint', color: '#ffd089', alpha: 0.3, ms: 900 },
    { op: 'narrate', text: 'And the kin. The small bright lives that chose your road — light caught, light kindled, carried all the way up this mountain. Every one of them a goodbye waiting to happen. Every one worth it. Every one.' },
    { op: 'silence', ms: 1800 },
    { op: 'action', actor: 'warden_cor', action: 'turnAway', holdMs: 1200 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: '...You\'re not arguing with me. You\'re REMEMBERING at me. Every lamp, every name, every small goodbye you\'d have me erase.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'I remember the ache. I built every stone of this against it. But the fair, the bell, the kites on the dark, the bread going round... I had forgotten it was worth the ache.' },
    { op: 'face', actor: 'warden_cor', facing: 'down' },
    { op: 'narrate', text: 'His certainty does not shatter. It goes the way ice goes at the first thaw — quietly, from underneath, into something that moves again.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'at_peace', text: 'The gauge stands at zero. It always has. I told myself I was waiting to be certain — but some mercies cannot survive a lit lamp.' },
    { op: 'move', actor: 'warden_cor', to: { tx: 12, ty: 8 }, speed: 0.5 },
    { op: 'face', actor: 'warden_cor', facing: 'left' },
    { op: 'narrate', text: 'Warden Còr folds his hands and steps aside from his own great work — undone by nothing in Vesperholm except everything he had made himself forget.' },
    { op: 'action', actor: 'warden_cor', action: 'bow' },
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
    { op: 'narrate', text: 'Above the Great Null\'s silenced mouth the Keystar hangs small and patient, the light the whole sky remembers itself by. In the dais under your hands, something stirs toward your lamp-glow.' },
    { op: 'narrate', text: 'A curl of white-gold light unfolds from the lantern-housing: the KEYLUMEN, the Keystar\'s living heart, asleep since the night fell — awake now.' },
    { op: 'narrate', if_flag: 'flag:wren_joined', text: 'Behind you, Wren says nothing — just lifts their lamp, the way you both learnt on the coast road. The asking is yours.' },
    { op: 'narrate', if_flag: 'flag:fenn_counsel_given', text: 'In your satchel, Fenn\'s starlamp is warm as a held hand. Forty years he kept it, for exactly this asking.' },
    // The asking must never dangle on a spent key item: if the Starlamp went to
    // some other wonder on the road, the dais holds a second (Fenn never trusted
    // a single road) — granted only when the satchel is empty of one.
    { op: 'ensureItem', item: 'starlamp', count: 1, text: 'Set into the dais\'s lantern-housing, wrapped against the dust: a STARLAMP. Fenn never trusted a single road with anything that mattered.' },
    { op: 'letterbox', on: false, ms: 300 },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'legendaryBattle', name: 'keylumen', kin: 149, level: 55, caughtFlag: 'flag:keylumen_caught', cooldownBattles: 0, cooldownRef: 'npc.keylumen_waits' },
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 700 },
    { op: 'silence', ms: 2600 },
    { op: 'narrate', text: 'The Keylumen settles into your lamp — then rises THROUGH it, up the shaft, past the Crown, a thread of white-gold paying out into the highest dark.' },
    { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 1200 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#fff3c9', alpha: 0.35, ms: 1400 },
    { op: 'gleam', element: 'light' },
    { op: 'musicCrossfade', key: 'umbral-spire-c', ms: 1400 },
    { op: 'narrate', text: 'The Keystar CATCHES. Light pours back along the Skyweave like a tide remembering its shore — the Crown blazing whole, the night legible rim to rim.' },
    { op: 'wait', ms: 900 },
    { op: 'narrate', text: 'Far below, in the swept gallery, every cold stone on the linen begins — all at once, quietly — to glow.' },
    { op: 'wait', ms: 1200 },
    { op: 'face', actor: 'warden_cor_after', facing: 'up' },
    { op: 'narrate', text: 'Còr is looking at the Starlamp\'s old brass cell in your lamp-bag.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: "That cell. I know that brass. She filled it the winter we were apprentices. 'For the night we'll need it,' she said, and Fenn and I laughed at her." },
    { op: 'action', actor: 'warden_cor_after', action: 'turnAway', holdMs: 1400 },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'sorrowful', text: 'She kept the Ninth Lantern twenty years. The winter it failed, I sat by her lamp while it burned down, counting its hours and calling it hope.' },
    { op: 'wait', ms: 800 },
    { op: 'face', actor: 'warden_cor_after', facing: 'up' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'at_peace', text: '...And he kept her light all this time, to spend on a morning. Of course he did.' },
    { op: 'say', speaker: 'CÒR', portrait: 'cor', expr: 'at_peace', text: '...There it is. The view from the top of the ladder. I named half those stars — and tonight is the first time in twenty years I have let myself look.' },
    { op: 'flashColor', color: '#fff3c9', ms: 300 },
    { op: 'tint', color: '#fff3c9', alpha: 0, ms: 1600 },
    { op: 'narrate', text: 'The Keystar holds. The sky remembers itself. And below the mountain, in valley after valley, lamps are going up in windows to answer it.' },
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
    { op: 'move', actor: 'player', to: { tx: 11, ty: 11 }, speed: 0.6 },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'narrate', text: 'You turn from the dais — and the light comes with you. Over the rim of the world, for the first time in years, the east goes grey. Then silver. Then, unbelievably, GOLD.' },
    { op: 'setFlag', flag: 'flag:dawn' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.25, ms: 1600 },
    { op: 'narrate', text: 'A lamp is climbing the dawn road below — small, steady, unhurried. Star-tender Fenn, who would not climb in the dark, climbing in the light.' },
    { op: 'move', actor: 'fenn_dawn', to: { tx: 16, ty: 9 }, speed: 0.8 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'I watched it begin from the waystone, child. Then I looked down and found my legs had already started walking.' },
    // vignette 12 — two old men on the dawn road: he passes you, takes the
    // rail beside Còr, and they look east together before a word is said.
    { op: 'move', actor: 'fenn_dawn', to: { tx: 12, ty: 12 }, speed: 0.8 },
    { op: 'narrate', text: 'He passes you with one press of your shoulder and goes to the rail, where Còr stands with the morning on his face like a man rereading an old letter.' },
    { op: 'move', actor: 'fenn_dawn', to: { tx: 13, ty: 12 } },
    { op: 'face', actor: 'fenn_dawn', facing: 'right' },
    { op: 'face', actor: 'warden_cor_after', facing: 'right' },
    { op: 'wait', ms: 1200 },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'peace', text: 'You read the same sky I did, old friend. There\'s still a lamp lit for you. ...Come down and tend it with me.' },
    { op: 'silence', ms: 1600 },
    { op: 'narrate', text: 'Còr does not answer in words. He turns his cold hand-lamp over once — and follows his friend down toward the morning, leaving the Great Null to the rust.' },
    { op: 'action', if_flag: 'flag:wren_joined', actor: 'wren_summit', action: 'laugh' },
    { op: 'say', if_flag: 'flag:wren_joined', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'Same road, different lamps — all the way to the end of the sky. ...Come on. Walk me home.' },
    // C-2: the credits panel says the morning line better thirty seconds later,
    // so the last in-world beat is an image — and it keeps the post-dawn
    // Nullmajor (script.nullworks_nullmajor) consistent.
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'narrate', text: 'Behind you, the Great Null stands silent in the first light — and deep in its cold housing, something answers the sun.' },
    // The works stood down with the dark: a first post-dawn visit to the Stillworks
    // must not stage the Long-Dusk band, nor find Còr on the gantry (he's at Dawnstead).
    { op: 'setFlag', flag: 'flag:seen_stillworks' },
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
    { op: 'say', if_flag: 'gleam:verdant', speaker: 'NETMENDER', text: 'Since you keep turning up wherever a lamp wants tending — here\'s a thing I\'d tell nobody sensible.' },
    { op: 'say', if_flag: 'gleam:verdant', speaker: 'NETMENDER', text: 'There\'s a low singing in the cliff at lamp-lighting. Could be the tide. Tide\'s never once kept a tune before, mind.' },
    { op: 'say', if_flag: 'gleam:verdant', speaker: 'NETMENDER', text: 'It comes up out of [[Tideglass]], the glass cavern under the coast — glimmer-step ground. Somebody who LIGHTS things ought to hear it.' },
    { op: 'setFlag', if_flag: 'gleam:verdant', flag: 'flag:three_dusk_rumour' },
  ],

  // --- Tideglass Cavern: the wreck-lamp (S3 "The Cavern Keeps a Light" pays).
  // Interact gated on flag:q_south_wrecklamp (the fisher's tale); the trigger
  // banks flag:q_south_wrecklamp_lit — consumed by the inn's thanks stage AND
  // the verse plaque's live twin.
  'script.tideglass_wrecklamp': [
    { op: 'narrate', text: 'The wreck at last — ribs glass-smooth, stern-lamp wedged where she broke, exactly as a drowning man has remembered it for forty years.' },
    { op: 'narrate', text: 'The wick is salt-stiff. You trim it as you were taught, and lend it flame.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.2, ms: 700 },
    { op: 'narrate', text: 'It takes. Light walks out across the smoothed glass, the black water, the veined teal deep — and the cavern that kept one light three days is a lit place again.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 900 },
    { op: 'narrate', text: '[[The old fisher]] at the quayside inn is owed the telling. And under your boots, faint as a held note, something low sings the evening in.' },
  ],

  // The verse on the wreck-lamp's glass hood. ONE requires_flag rides the
  // trigger (the lamp burning); the rumour gate lives HERE — without the
  // netmender's word the etching stays craft, never directions, and the flag
  // is only banked once both are held (the spec's wiring-pass note).
  'script.three_dusk_verse': [
    { op: 'narrate', text: 'With the wreck-lamp burning, its glass hood comes alive: etched lines catch the flame and stand out silver — verse-marks in an old lampwright\'s hand.' },
    { op: 'narrate', if_flag: 'flag:three_dusk_rumour', text: '"LAST LIGHT FIRST; THE LOW LIGHT AFTER; THE DEEP LIGHT ONCE THE OTHERS HOLD."' },
    { op: 'narrate', if_flag: 'flag:three_dusk_rumour', text: '[[Three standing lenses]] wait in the dark: west shelf, mid-pool, stair seam. The singing under the floor is, you realise, keeping time.' },
    { op: 'setFlag', if_flag: 'flag:three_dusk_rumour', flag: 'flag:three_dusk_verse' },
  ],

  // The Lampwright's Relay — three lenses lit in verse order (the triggers
  // chain the flags; cold twins swap on the same flags; wrong order answers
  // with npc.tideglass_lens_cold).
  'script.three_dusk_lens_a': [
    { op: 'narrate', text: 'The amber lens on the west shelf — last light, the colour of an evening\'s end. You raise the vesperlamp to it.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'The glass warms to honey, and the wreck-lamp\'s beam leans INTO it, one span deeper into the dark. Below, the singing turns toward you.' },
  ],
  'script.three_dusk_lens_b': [
    { op: 'narrate', text: 'The low lens, out on the mid-pool islet, barely above the black water.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'It takes the amber beam and bends it low across the pool, skating the still water the way dusk lies along a valley floor. The singing is very close now.' },
  ],
  'script.three_dusk_lens_c': [
    { op: 'narrate', text: 'The deep lens, by the stair seam. Behind you, the other two hold.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#4fb4ff', alpha: 0.2, ms: 700 },
    { op: 'narrate', text: 'The relayed beam pours DOWN into the seam — and the glass rings: one low note through the floor, your boots, the water. The whole cavern is the bell.' },
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
    { op: 'narrate', text: 'The Dusk Hour folds into your lamp the way evening folds into a valley — heavily, gratefully. Its chest-coal settles to a banked glow.' },
    { op: 'musicCrossfade', key: 'dimglass-coast-c', ms: 1600 },
  ],

  // Tideglass caches (the standing region kit; the nook is the spine §5
  // Starlight reveal — its placement is gated on flag:lamplight_starlight).
  'script.pickup_tideglass_starshard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In the deepest fold, only a Starlight lamp reaches: a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_tideglass_starshard' },
  ],
  'script.pickup_tideglass_balm': [
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'A deep-walker\'s tin, wedged dry on the west shelf. Found 2 WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_tideglass_balm' },
  ],
  'script.pickup_tideglass_wicks': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 250 },
    { op: 'say', text: 'The wreck\'s strongbox: 250 WICKS, forty years late.' },
    { op: 'setFlag', flag: 'flag:picked_tideglass_wicks' },
  ],

  // --- H2 "The Longest Watch" — the unlock chain (Pale Vault → the Hourfold).
  // The aurora-watcher's post-Frost stage carries the rumour (her dry line is
  // the chain's one sanctioned humour beat), then Ysolde's snuffer arms the
  // fold's warp gate.
  'script.aurorawatcher_hours': [
    { op: 'say', speaker: 'WATCHER', text: 'You again, with the warded flame. Stand with me and look where I\'m looking — past the blue fold, into the deep ice.' },
    { op: 'say', speaker: 'WATCHER', text: 'The aurora bends round that fold like it\'s queuing. Forty years I\'ve watched the sky. It has never once queued for me.' },
    { op: 'say', speaker: 'WATCHER', text: 'The ice has sealed it, and it\'s a watcher\'s matter. [[Ask Ysolde]] in [[the undercroft below the vault]] before you go prying.' },
    { op: 'setFlag', flag: 'flag:three_mid_rumour' },
  ],
  'script.ysolde_snuffer': [
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: 'The watcher sent you. ...Something keeps the deep ice: the Still Hour. Midnight itself, standing a watch with no relief.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'Our braziers burn at the bottom of the fold, but the Hour will not be SEEN by their light. To meet midnight, [[bring it the dark]].' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'vigil_snuffer', count: 1 },
    { op: 'say', text: 'Received the VIGIL SNUFFER — a cap of cold iron, worn smooth by careful hands.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'serene', text: 'You have spent the whole road lighting things. Show the Hour you understand the other half of tending.' },
    { op: 'say', speaker: 'YSOLDE FROST', portrait: 'ysolde', expr: 'neutral', text: '[[Read the aurora]] for the order. And put out what you put out ON PURPOSE. That is the difference between a tender and the Hollowing.' },
    { op: 'setFlag', flag: 'flag:three_mid_snuffer' },
  ],

  // The Unstruck Toll — three braziers SNUFFED in aurora order (east →
  // water-ice → west). The one inverted light verb in the game; the dark made
  // here is kept, not surrendered. Triggers chain the flags; lit→snuffed
  // object swaps ride the same flags; wrong order answers with
  // npc.hourfold_flame_leans. Nothing resets — the cooldown is the cost.
  'script.three_mid_brazier_a': [
    { op: 'narrate', text: 'The east brazier first, under the kneeling ribbon. You raise the Vigil Snuffer, slowly, on purpose, and cap the blue-white flame.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'The flame goes, gently. The dark in its place is not the Hollowing\'s — it is yours, chosen and kept. One. Overhead, the aurora pours a shade brighter.' },
  ],
  'script.three_mid_brazier_b': [
    { op: 'narrate', text: 'The centre brazier, out on the water-ice. Your own lamp seems very loud here.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'Two. The shelf is more aurora than firelight now, and the silence has changed — from an empty room to an occupied one.' },
  ],
  'script.three_mid_brazier_c': [
    { op: 'narrate', text: 'The west brazier, last. The snuffer is steady. Your hands, less so.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 700 },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'The dark does not deepen. It straightens, as if relieved of a stoop.' },
    { op: 'narrate', text: 'On the far shelf, a dome of black ice unrolls — pane over pane of midnight glass, a star kept in each — and stands, hooded in the whole night sky.' },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // The Still Hour (the Hourfold's bottom shelf) — spec-verbatim op.
  'script.three_midnight_battle': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'It has been still long enough to grow stars. Only the silver crescents of its eyes turn, and the unstruck bell at its throat keeps its silence like a vow.' },
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
    { op: 'narrate', text: 'The Still Hour folds into your lamp pane by pane, the watch handed over. For the first time in years, midnight is relieved.' },
    { op: 'musicCrossfade', key: 'pale-vault-glacier-c', ms: 1600 },
  ],

  // The fold's one [MISSABLE] cache, behind the false ledge-line (mundane
  // periphery — the one sanctioned dry note at this site lives on a tin).
  'script.pickup_hourfold_amber': [
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'moth_amber', count: 1 },
    { op: 'say', text: 'Where every wrong ledge-drop lands: a MOTH-AMBER. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_hourfold_amber' },
  ],

  // --- H3 "The Unrisen Stair" — the unlock chain (Nightreach → the Solarium).
  // Nessa is sincere — she is the haunted one; Lucan carries the chain's one
  // dry line with the First-Light Phial.
  'script.nessa_hours': [
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'Wayfarer. Come up to the eyepiece — no, you needn\'t look. Listening is the trouble tonight.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'haunted', text: 'Every chart says the morning bell hangs due south. There has been no morning. Yet three nights I have heard it. WAITING makes a sound.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'reverent', text: '[[South, down the Sunvault Climb]]: the Solarium\'s drowned garden, and off its deepest fold, a stair no one has climbed.' },
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'neutral', text: '[[Ask Lucan]] if anyone kept the last MORNING. He kept the last warm day.' },
    { op: 'setFlag', flag: 'flag:three_dawn_rumour' },
  ],
  'script.lucan_phial': [
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'grand', text: 'The last MORNING? ...Nessa heard her bell again. Then it is time — I have been holding this cue for forty years.' },
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'bittersweet', text: 'I kept the last warm day. Somebody kept the last morning and never mentioned it. Theatrical of them. I approve.' },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'first_light_phial', count: 1 },
    { op: 'say', text: 'Received the FIRST-LIGHT PHIAL — one cupful of daylight, drawn the morning before the Long Dusk fell. Through the glass it beats faintly, like a pulse.' },
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'bittersweet', text: '[[Pour it in the sun-basin]] before the sealed stair, deep in the garden. All of it — you do not make half an entrance.' },
    { op: 'setFlag', flag: 'flag:three_dawn_phial' },
  ],

  // The basin pour (host trigger on sunken_solarium banks flag:three_dawn_poured
  // — the warp gate's key and bloom A's requires).
  'script.three_dawn_basin': [
    { op: 'narrate', text: 'The sun-basin waits where a first light was meant to land. You unstop the phial — and the smell of MORNING, bread-warm, stands in the dark garden like a person.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#fff3c9', alpha: 0.14, ms: 900 },
    { op: 'narrate', text: 'You pour. One cupful of daylight fills the basin and HOLDS, like the first coin of a sunrise. Beyond the seal, a sun-vine stirs.' },
    { op: 'tint', color: '#fff3c9', alpha: 0, ms: 1100 },
  ],

  // The Bloom Ascent — sequential + redirect (the Sunsketch dimension in
  // full). Bloom A rides the step_on bands; the mirror is the redirect; the
  // far vine's bands answer npc.unrisen_far_vine until the daylight is bent.
  'script.three_dawn_bloom_a': [
    { op: 'narrate', text: 'The pocket of morning climbs the stair with you, and the first sun-vine takes it: blooms, and lays itself across the black water, a bridge.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'narrate', text: 'The far vine sleeps on. And on [[the east spur]], something of bronze and glass turns slightly, the way a sleeper turns toward a window.' },
  ],
  'script.three_dawn_mirror': [
    { op: 'narrate', text: 'The sun-mirror flower, shut these long years, feels the morning arrive and turns its face to it.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#fff3c9', alpha: 0.12, ms: 800 },
    { op: 'narrate', text: 'It opens, petal by glass petal, and BENDS the daylight in one bright line across the water to the last sleeping vine.' },
    { op: 'tint', color: '#fff3c9', alpha: 0, ms: 900 },
  ],

  // The flight-two cache ([MISSABLE], a fallen capital).
  'script.pickup_unrisen_shard': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In a fallen capital off the second flight: a STARGLASS SHARD. Found it!' },
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
    { op: 'narrate', text: 'Where the first light was meant to land, something half-finished stands facing east, as it has for years. Its sketched ear tilts toward your lamp.' },
    { op: 'letterbox', on: false },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    { op: 'legendaryBattle',
      name: 'three_dawn', kin: 162, level: 55,
      caughtFlag: 'flag:three_dawn_caught',
      cooldownBattles: 18,
      cooldownRef: 'npc.three_dawn_resting' },
    { op: 'silence', ms: 1400 },
    { op: 'narrate', text: 'The Lost Hour steps into your lamp mid-stride — and never quite finishes arriving. Part of it still waits where every morning waits, facing east.' },
    { op: 'musicCrossfade', key: 'sunken-solarium-c', ms: 1600 },
  ],

  // Fenn's counsel-after stage (Vesper Crossroads) — wraps the standing line
  // and adds the §6 payoff once flag:three_dawn_met is held (the flag's one
  // consumer alongside the counsel script's guarded step).
  'script.fenn_counsel_after': [
    { op: 'dialogue', ref: 'npc.fenn_counsel_after' },
    { op: 'say', if_flag: 'flag:three_dawn_met', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'So you found the third watch. Still facing east? ...Then it never stopped believing. Neither have I. Go and prove us right.' },
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
    { op: 'narrate', text: 'Morning. Not lamplight, not moonrise, not a festival\'s kind hour — morning, blue and gold, lying over everything at once.' },
    { op: 'tint', color: '#ffd98a', alpha: 0.18, ms: 1200 },
    { op: 'narrate', text: 'Warm shadows. Open sky. Up the green, the old lullaby every lamp-tender hums — and for once it is not asking the dark for anything.' },
    { op: 'tint', color: '#ffd98a', alpha: 0, ms: 1400 },
    { op: 'narrate', text: 'The rooflines are Tinderwick\'s; the dock is Tinderwick\'s. It is home, and it is not — nothing that woke this morning is quite what it was.' },
  ],

  // THE FIRST-DAWN FESTIVAL (Arc E capstone) — the whole town out in the sun:
  // the thesis of "belonging, not conquest," now in daylight. Ambient colour,
  // a small warm swell that hands straight back to the town loop.
  'cutscene.dawnstead_first_dawn': [
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 900 },
    { op: 'narrate', text: 'The square is full. Nobody organised it; the sun came up and Vesperholm walked out to stand under it. The first-dawn festival.' },
    { op: 'say', text: '"No lanterns tonight!" someone calls, and laughs, and has to sit down on the well-step about it.' },
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
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: '...Still here? Then I\'ll teach one minute longer. Two errands, neither urgent — nothing is urgent any more.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'First: Còr keeps a lamp on the west strand. [[Climb the Tinderwick Beacon]] and [[draw him a fresh wick]] — one given in daylight.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Second: the relit sky is WAKING day-forms. [[Find three signs]] on [[the sunlit verge]]. Surveys are patience wearing boots.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Start by [[the verge\'s north corner]] — the dawn-blooms there have been fed on. Something gold did the feeding.' },
    // P2's assignment flag gates the Beacon wick-case (QA MIN-1: without it the
    // wick could be drawn before Fenn frames the errand — a narrative skip).
    { op: 'setFlag', flag: 'flag:q_post_wick_asked' },
    { op: 'setFlag', flag: 'flag:q_post_survey' },
  ],
  // P3, the waiting stage — Fenn names ONE mark at a time (the chained finds
  // order the if_flag lines: the latest held flag reads last and truest).
  'script.fenn_survey_wait': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'The survey, apprentice. [[The verge\'s north corner]] first — the fed-on dawn-blooms. Bring me what the morning left.' },
    { op: 'say', if_flag: 'flag:q_post_survey_1', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'A wing-scale — the moth\'s page is inked. Next: [[the verge\'s south skirt]], shore side. Something shed its dusk coat there.' },
    { op: 'say', if_flag: 'flag:q_post_survey_2', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'A whole moult, empty as an outgrown word. Last: [[the garden-mouth blooms]]. Something came home there at sunrise.' },
  ],
  'script.fenn_survey_done': [
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Scale, moult, and a warm doorstep. The sky relit, and the small lives answered first. That is star-tending, in one verge.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'warm', text: 'Take the page. Your lamp is Radiant now: [[walk the dark places again]]. They\'ve held things for you.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'fenn_journal_page', count: 1 },
    { op: 'say', text: 'Received FENN\'S JOURNAL PAGE!' },
    { op: 'setFlag', flag: 'flag:q_post_survey_done' },
  ],
  // The three survey-mark finds (interact, chained 1 -> 2 -> 3).
  'script.survey_find_1': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'Under the fed-on dawn-blooms: a single wing-scale, gold as a struck match and warm to the touch.' },
    { op: 'setFlag', flag: 'flag:q_post_survey_1' },
  ],
  'script.survey_find_2': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'In the grass by the shore skirt: a shed moult, dusk-grey and paper-light. Whatever wore it is wearing morning now.' },
    { op: 'setFlag', flag: 'flag:q_post_survey_2' },
  ],
  'script.survey_find_3': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'Beneath the blooms at the garden mouth, a burrow, warm as a banked hearth. Its keeper came home with the sunrise and is sleeping off the dark.' },
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
    { op: 'action', actor: 'cor_lamp_keeper', action: 'kneel', holdMs: 1600 },
    { op: 'narrate', text: 'Where the strand narrows past the old tree, a man in faded warden\'s grey kneels at a single lamp, tending it like a thing he means to keep.' },
    { op: 'say', speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'I wanted to spare everyone the dusk. I had forgotten that the lamp is for the dark — not against it.' },
    { op: 'tint', color: '#ffd98a', alpha: 0.14, ms: 1100 },
    { op: 'narrate', text: 'He tends the flame.' },
    { op: 'say', speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'It will fall again, you know. The night. I find I no longer mind. I\'ll be here to light it.' },
    // P-1 — the cinder wakes; the name is said (X-1's last dose; story-bible §11)
    { op: 'wait', ms: 900 },
    { op: 'narrate', text: 'Beside his lamp sits a stone no bigger than a plum, glowing gold through every crack.' },
    { op: 'say', speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'Our star. Hers, and Fenn\'s, and mine. It came down the winter Senna went. I carried it twenty years, cold. This morning it woke in my pocket.' },
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
    { op: 'say', speaker: 'WARDEN CÒR', portrait: 'cor', expr: 'at_peace', text: 'There. A wick dipped in daylight, burning toward the next dark. That\'s the whole prayer — I used to say it backwards.' },
    { op: 'tint', color: '#ffd98a', alpha: 0, ms: 1100 },
    { op: 'setFlag', flag: 'flag:q_post_wick_given' },
  ],
  // P2 — the wick itself, drawn in the Beacon's lantern room (tinderwick_
  // beacon_top; cache appears post-dawn, vanishes once drawn).
  'script.pickup_post_wick': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'The lantern room keeps its case of fresh-dipped wicks. You draw one, dipped this morning — the first wick in years made by daylight.' },
    { op: 'giveItem', item: 'dawn_wick', count: 1 },
    { op: 'say', text: 'Took the FIRST-DAWN WICK! Còr keeps his lamp on [[Dawnstead\'s west strand]].' },
    { op: 'setFlag', flag: 'flag:q_post_wick' },
  ],

  // P1 "FIRST-DAWN LETTERS" — the Waykeeper's daylight round (giver: the
  // post-bag at the Vesper Crossroads waystone). Deliverable in any order;
  // the quadrant-seat wardens stamp their replies (the keepsake reward).
  'script.post_letters_give': [
    { op: 'say', speaker: 'WAYKEEPER', text: 'Ah — the feet themselves! Half of Vesperholm wrote the other half about the dawn.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'Take the bundle? Letters for [[Wren and Fenn in Dawnstead]] and [[every Lampwarden\'s town]], any order. Somebody should walk all the roads at once.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'dawn_letters', count: 1 },
    { op: 'say', text: 'Received the FIRST-DAWN LETTERS!' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'No hurry. First post in years nobody\'s waiting on in the dark.' },
    { op: 'setFlag', flag: 'flag:q_post_letters' },
  ],
  'script.post_letter_wren': [
    { op: 'narrate', text: 'A letter for Wren, in the Waykeeper\'s careful hand.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'eager', text: 'For ME? ...From the kite-makers at Galehigh. They want the ribbon back for the museum wall. HA! Let them come and take it.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_wren' },
  ],
  'script.post_letter_fenn': [
    { op: 'narrate', text: 'A letter for Star-tender Fenn.' },
    { op: 'say', speaker: 'FENN', portrait: 'fenn', expr: 'smile', text: 'Post, at my age, in this light. ...From the Waykeeper. One word: "WELL?" And for once I haven\'t a correction to make.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_fenn' },
  ],
  'script.post_letter_tinderwick': [
    { op: 'say', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'First-dawn post! Somebody wrote "morning" and didn\'t put a candle-count after it. Frame-worthy, that.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_tinderwick' },
  ],
  'script.post_letter_pearlmoor': [
    { op: 'say', speaker: 'REYL WASH', portrait: 'reyl', expr: 'weathered', text: 'A letter that crossed no dark water to get here. Longest I\'ve waited for post in my life.' },
    { op: 'narrate', text: 'Reyl presses his wax stamp to the reply — the southern quadrant\'s thanks, kept.' },
    { op: 'giveItem', item: 'dawn_stamp', count: 1 },
    { op: 'setFlag', flag: 'flag:q_post_letter_pearlmoor' },
  ],
  'script.post_letter_lowleaf': [
    { op: 'say', speaker: 'SABLE QUILL', portrait: 'sable', expr: 'warm', text: 'Oh — post. In the sun. The Elder Bed greened before any of us were up. It always was the better botanist.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_lowleaf' },
  ],
  'script.post_letter_cinderhead': [
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'warm', text: 'Mail, from the morning. The deep way\'s the same, but the walk OUT ends in daylight now. The crews keep finding reasons.' },
    { op: 'narrate', text: 'Otho stamps the reply with the pit-seal — the eastern quadrant\'s thanks, kept.' },
    { op: 'giveItem', item: 'dawn_stamp', count: 1 },
    { op: 'setFlag', flag: 'flag:q_post_letter_cinderhead' },
  ],
  'script.post_letter_galehigh': [
    { op: 'say', speaker: 'MIRA VAEL', portrait: 'mira', expr: 'bright', text: 'A letter! On FOOT? In THIS wind? We\'d have flown it — but then we\'d have missed you. Fair trade!' },
    { op: 'setFlag', flag: 'flag:q_post_letter_galehigh' },
  ],
  'script.post_letter_pale_vault': [
    { op: 'say', speaker: 'YSOLDE', portrait: 'ysolde', expr: 'serene', text: 'The glacier took the sunrise like a held breath let go. Your letter arrives second, and is welcome anyway.' },
    { op: 'narrate', text: 'Ysolde sets her frost-seal to the reply — the northern quadrant\'s thanks, kept.' },
    { op: 'giveItem', item: 'dawn_stamp', count: 1 },
    { op: 'setFlag', flag: 'flag:q_post_letter_pale_vault' },
  ],
  'script.post_letter_solarium': [
    { op: 'say', speaker: 'LUCAN PYRE', portrait: 'lucan', expr: 'grand', text: 'Post! Delivered into an ENCORE — the sun is doing my whole repertoire for free. I adore the competition.' },
    { op: 'setFlag', flag: 'flag:q_post_letter_solarium' },
  ],
  'script.post_letter_nightreach': [
    { op: 'say', speaker: 'NESSA COLE', portrait: 'nessa', expr: 'reverent', text: 'A first-dawn letter. I watched the whole sky come back — and still, ink carried by hand is the light I trust most.' },
    { op: 'narrate', text: 'Nessa presses the observatory\'s star-seal to the reply — the western quadrant\'s thanks, kept.' },
    { op: 'giveItem', item: 'dawn_stamp', count: 1 },
    { op: 'setFlag', flag: 'flag:q_post_letter_nightreach' },
  ],

  // P1 PAYOFF — the Waykeeper's "all ten delivered" thanks. Its NPC at the
  // crossroads is gated on the DERIVED flag:q_post_letters_all (FlagStore raises it
  // once all ten flag:q_post_letter_* are held — the journal's counter, expressed as
  // a single gateable flag so a plain requires_flag NPC can wait on "all 10"). Sets
  // flag:q_post_letters_done, which closes P1 in the journal and hides this NPC.
  'script.post_letters_done': [
    { op: 'say', speaker: 'WAYKEEPER', text: 'Every last one — Wren, old Fenn, and all eight towns. The whole rim read the same word in the same morning, carried on the same two feet.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'A round like that earns its wage. Here — for walking every road at once.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 500 },
    { op: 'say', text: 'The Waykeeper presses 500 WICKS into your hand.' },
    { op: 'say', speaker: 'WAYKEEPER', text: 'First post in years that ended in the light. Thank you, Wayfarer. Truly.' },
    { op: 'setFlag', flag: 'flag:q_post_letters_done' },
  ],

  // The strand cache (the variety rule: loose wicks off the lane).
  'script.pickup_dawnstead_cache': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'narrate', text: 'In the knoll\'s lee, oilcloth-dry: a pouch of wicks never needed after all.' },
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
    { op: 'say', speaker: 'WATCHER ORIEL', text: 'Last night the sky GAVE a light back, like a tree sheds a leaf. The old watchers called them star-shards. The very old ones, invitations.' },
    { op: 'say', speaker: 'WATCHER ORIEL', text: 'I\'d fetch it, but somebody promoted me. Now I\'m not allowed near weather.' },
    { op: 'setFlag', flag: 'flag:starfall_begun' },
    { op: 'setFlag', flag: 'flag:vigil_reading_1' },
    // Reading 1 — Hearthfall (south).
    { op: 'say', speaker: 'WATCHER ORIEL', text: 'The first fell [[in the south]], where the first lamp learned its name. Climb past the lantern that taught the sky to answer: it lies on [[the bluff above]].' },
  ],

  // --- Vigil I — Hearthfall -------------------------------------------------
  // intro -> battle -> defeat -> grants (Starfall Shard + Radiant Charm) ->
  // flags (vigil_1_kept + vigil_reading_2). Esra reads reading 2 in the glint.
  'script.vigil_hearthfall': [
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'I dipped Brisa\'s first wick, dear. Wicks don\'t lie, but let\'s check.' },
    { op: 'battle', trainer: 'vigilant_esra' },
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'Steady as her best. Take the shard — and the charm; I pressed it for whoever finally came.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveItem', item: 'radiant_charm' },
    { op: 'setFlag', flag: 'flag:vigil_1_kept' },
    { op: 'setFlag', flag: 'flag:vigil_reading_2' },
    // Reading 2 — Grovefall (east).
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'See it glint? The second went to earth [[in the east, under the hill]], where the moss has opinions. Bring a light, and patience.' },
  ],
  'script.vigil_hearthfall_again': [
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'Back for another? Good. A flame wants checking now and then.' },
    { op: 'battle', trainer: 'vigilant_esra' },
    { op: 'say', speaker: 'WICK-MOTHER ESRA', text: 'Steady as ever. Off you go, dear — and mind the gulls.' },
  ],

  // --- Vigil II — Grovefall (cave) ------------------------------------------
  'script.vigil_grovefall': [
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'Otho says you out-lasted him. Otho exaggerates. ...Show me he doesn\'t.' },
    { op: 'battle', trainer: 'vigilant_bramm' },
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'Hah. He doesn\'t. Take the chart: the sky minted a Stone figure for us.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveItem', item: 'chart_tremor_quake' },
    { op: 'setFlag', flag: 'flag:vigil_2_kept' },
    { op: 'setFlag', flag: 'flag:vigil_reading_3' },
    // Reading 3 — Stormfall (north).
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'The third went [[north, to the wind\'s spare pocket]], where storms go off duty. Take the kite. Fetch your own hat.' },
  ],
  'script.vigil_grovefall_again': [
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'The grotto\'s grown a season since. Walk the deep way again; it keeps you honest.' },
    { op: 'battle', trainer: 'vigilant_bramm' },
    { op: 'say', speaker: 'OLD FOREMAN BRAMM', text: 'Still lasting. The moss approves, and the moss is never wrong. Go on.' },
  ],

  // --- Vigil III — Stormfall ------------------------------------------------
  // The storm-tithe is the wick jackpot (giveMoney 5000); the cache by the nest
  // is the Starglass ×2 (the tithe's second half — placed in the map JSON).
  'script.vigil_stormfall': [
    { op: 'say', speaker: 'ONDRA VAEL', text: 'Mira flies in what I called a light breeze at her age. Stand up straight — the sky\'s sent us a present, and I open my own post.' },
    { op: 'battle', trainer: 'vigilant_ondra' },
    { op: 'say', speaker: 'ONDRA VAEL', text: 'HA! A kite-flier yet. Take the aerie\'s storm-tithe; I can\'t spend wind.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveMoney', amount: 5000 },
    { op: 'setFlag', flag: 'flag:vigil_3_kept' },
    { op: 'setFlag', flag: 'flag:vigil_reading_4' },
    // Reading 4 — Sunfall (west).
    { op: 'say', speaker: 'ONDRA VAEL', text: 'The shard points [[west]], to [[the high terraces]] where summer was put away for safekeeping.' },
  ],
  'script.vigil_stormfall_again': [
    { op: 'say', speaker: 'ONDRA VAEL', text: 'Weather\'s up. Good weather for it. Stand up straight, then — same as before.' },
    { op: 'battle', trainer: 'vigilant_ondra' },
    { op: 'say', speaker: 'ONDRA VAEL', text: 'HA! Still a kite-flier in you. Off the ledge, mind your footing.' },
  ],

  // --- Vigil IV — Sunfall ---------------------------------------------------
  'script.vigil_sunfall': [
    { op: 'say', speaker: 'DAME SOLENNE', text: 'I taught a valley to bow to a sun that never came. Now it bows every morning. One encore, full light.' },
    { op: 'battle', trainer: 'vigilant_solenne' },
    { op: 'say', speaker: 'DAME SOLENNE', text: 'Curtain. ...I don\'t mourn the last warm day now. Take the figure — the sun\'s whole bow.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveItem', item: 'chart_sunburst_nova' },
    { op: 'setFlag', flag: 'flag:vigil_4_kept' },
    { op: 'setFlag', flag: 'flag:vigil_reading_5' },
    // Reading 5 — Murkfall (the outer marches, the mirror axis).
    { op: 'say', speaker: 'DAME SOLENNE', text: 'One last reading, my dear. The last fell [[where the water forgot how to speak]]. Go gently into [[the murk]]. One there has waited long to greet you.' },
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
    { op: 'say', speaker: 'WARDEN MER', text: 'I carried a null-lantern through this marsh once. Before I hand the light back, I will know the hand is steady.' },
    { op: 'battle', trainer: 'vigilant_mer' },
    { op: 'say', speaker: 'WARDEN MER', text: 'It holds. Brighter hands than mine ever were. The marsh thanks you — both of me, perhaps.' },
    { op: 'giveItem', item: 'starfall_shard' },
    { op: 'giveItem', item: 'morrow_charm' },
    { op: 'setFlag', flag: 'flag:vigil_5_kept' },
    { op: 'say', speaker: 'WARDEN MER', text: 'The sixth never fell. [[Carry the five up the mountain]], and ask the old man what he sees.' },
  ],
  'script.vigil_murkfall_again': [
    { op: 'say', speaker: 'WARDEN MER', text: 'The marsh is brighter every time you come. So am I. Once more?' },
    { op: 'battle', trainer: 'vigilant_mer' },
    { op: 'say', speaker: 'WARDEN MER', text: 'It holds. It always holds, with you. Go gently back.' },
  ],

  // --- The Vigil-site caches (one per annex; Stormfall's is the tithe's
  // second half — its site prize is the wick jackpot, not a chart) ----------
  'script.pickup_vigil_hearth_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In the bluff grass, warm with morning: a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_vigil_hearth_glass' },
  ],
  'script.pickup_vigil_grove_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'The moss has cradled it all season. Found a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_vigil_grove_glass' },
  ],
  'script.pickup_vigil_storm_tithe': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 2 },
    { op: 'say', text: 'The aerie\'s tithe, lashed against the wind: 2 STARGLASS SHARDS!' },
    { op: 'setFlag', flag: 'flag:picked_vigil_storm_tithe' },
  ],
  'script.pickup_vigil_sun_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In a cracked sun-basin, drinking daylight: a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_vigil_sun_glass' },
  ],
  'script.pickup_vigil_murk_glass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'In the shallow black water, glowing softly: a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_vigil_murk_glass' },
  ],

  // --- The Last Lesson — the summit Round (requires flag:vigil_5_kept) -------
  // Three Vigilants back-to-back -> heal (Fenn's diegetic line) -> Fenn at full
  // strength. A loss anywhere aborts before the flag, so the whole Round re-runs
  // from its trigger (the intended shape of the ultimate). On the win: the apex
  // gleam cadence seats the five shards and sets flag:starfall_lesson.
  'script.starfall_round': [
    { op: 'narrate', text: 'At the foot of the empty Ninth Lantern, three figures wait, lamps lit, with no business being this high and every right to be.' },
    { op: 'say', speaker: 'ONDRA VAEL', text: 'We came to watch the old man\'s lesson. The watching turned into a queue.' },
    { op: 'battle', trainer: 'vigilant_ondra_summit' },
    { op: 'battle', trainer: 'vigilant_solenne_summit' },
    { op: 'battle', trainer: 'vigilant_mer_summit' },
    { op: 'heal', sleep: false }, // Fenn's breath between bouts — the summit keeps its music
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'I\'ll want you at your best. I have waited a very long time to be allowed mine.' },
    // P-1 — Fenn says her name (the third apprentice on the ladder)
    { op: 'action', actor: 'fenn_round', action: 'turnAway', holdMs: 1200 },
    { op: 'wait', ms: 700 },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'Senna would have wanted the last lesson to be a hard one. She always said the gentle ones get forgotten.' },
    { op: 'face', actor: 'fenn_round', facing: 'down' },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'No satchel this time. No errand. The last lesson is the one I couldn\'t teach — what you do when the teacher steps aside. Show me everything, apprentice.' },
    { op: 'battle', trainer: 'startender_fenn' },
    // WIN — everything below is post-battle (a loss aborted the script already).
    { op: 'say', speaker: 'STAR-TENDER FENN', text: '...There it is. The whole sky in one steady lamp.' },
    // The shards seated — the apex gleam cadence (the Keystar relight's quieter sibling).
    { op: 'letterbox', on: true, ms: 420 },
    { op: 'musicFade', ms: 800 },
    { op: 'silence', ms: 2200 },
    { op: 'narrate', text: 'You lift the five shards to the Ninth Lantern\'s empty collar. They settle as if they always would — gold finding gold.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.28, ms: 1200 },
    { op: 'gleam', element: 'solar' },
    { op: 'setFlag', flag: 'flag:starfall_lesson' },
    { op: 'narrate', text: 'The collar holds the light, and far below the rim of the world the sixth shard answers. It never fell. It could not. It is the morning itself.' },
    { op: 'musicCrossfade', key: 'gleam-emotional', ms: 1200 },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1100 },
    { op: 'letterbox', on: false, ms: 420 },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'Five seated, and the sixth come of its own accord. ...[[Go to the lantern]], apprentice. Something is waking that has waited longer than any of us.' },
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
    { op: 'narrate', text: 'The Ninth Lantern pours light down the shaft, and the morning takes a shape: DAWNBRAEL, the first-morning kin, Solar and Light.' },
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
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'Nothing left to teach. Stand up straight, Star-tender — the title was always yours. I\'m only the one saying it out loud.' },
    { op: 'tint', color: '#ffe9a8', alpha: 0.18, ms: 900 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'giveItem', item: 'fenns_glass' },
    { op: 'say', speaker: 'STAR-TENDER FENN', text: 'Take the field-glass. Forty years it showed me the sky. You\'ll see further — that\'s the whole job: hand it on to someone who sees further.' },
    { op: 'setFlag', flag: 'flag:starfall_crown' },
    { op: 'narrate', text: 'The apprentice sent on a satchel errand ends a Star-tender, with the morning on every lamp.' },
    { op: 'tint', color: '#ffe9a8', alpha: 0, ms: 1100 },
  ],

  // ---------------------------------------------------------------------------
  // ANDREW, at the Tinderwick fence — the game's naming beat, and the door to
  // the S4 easter egg.
  //
  // He asks what you're called (`askName`), and every line afterwards can use
  // `{name}`. The name ALSO branches the scene without any new machinery: the op
  // sets `flag:name_is_paul` when the typed name matches, and the supply-drop
  // steps below simply guard on it with the ordinary per-step `if_flag`. Anyone
  // not called Paul gets the same warm welcome minus the parcel — and everyone
  // gets the nudge toward the real easter egg (Paul, the Booji-Wooji Man, out at
  // the end of the Pearlmoor breakwater; the Lifting House at the top of the
  // quay town is the way in).
  // ---------------------------------------------------------------------------
  'script.andrew_name': [
    // Actor refs are NPC PLACEMENT ids, not display names — this is the
    // pre-naming placement (`andrew_post` is the one after).
    { op: 'emote', actor: 'andrew_pre', emote: 'alert' },
    { op: 'say', speaker: 'ANDREW', text: 'Morning! Or — well. You know. Whatever this is.' },
    { op: 'say', speaker: 'ANDREW', text: 'You\'re the lamp-tender\'s apprentice, aren\'t you. The whole street\'s been saying so for a week.' },
    { op: 'say', speaker: 'ANDREW', text: 'Right — manners. Before you wander off into all that dark: what do folk call you?' },
    {
      op: 'askName',
      title: 'YOUR NAME',
      fallback: 'Wayfarer',
      matches: [{ value: 'Paul', flag: 'flag:name_is_paul' }],
    },
    { op: 'say', speaker: 'ANDREW', text: '{name}. Good name. It\'ll carry.' },

    // --- The Paul branch: a friend, expected, and provisioned accordingly. ----
    { op: 'emote', if_flag: 'flag:name_is_paul', actor: 'andrew_pre', emote: 'heart' },
    { op: 'say', if_flag: 'flag:name_is_paul', speaker: 'ANDREW', text: '...PAUL. You\'re joking. PAUL.' },
    { op: 'say', if_flag: 'flag:name_is_paul', speaker: 'ANDREW', text: 'Hang on — hang ON, don\'t move —' },
    { op: 'sfx', if_flag: 'flag:name_is_paul', key: 'world-pickup' },
    { op: 'giveItem', if_flag: 'flag:name_is_paul', item: 'lumen_drop', count: 20 },
    { op: 'giveItem', if_flag: 'flag:name_is_paul', item: 'warm_balm', count: 5 },
    { op: 'giveItem', if_flag: 'flag:name_is_paul', item: 'tallow_balm', count: 5 },
    { op: 'giveMoney', if_flag: 'flag:name_is_paul', amount: 5000 },
    {
      op: 'narrate',
      if_flag: 'flag:name_is_paul',
      text: 'He hauls a packed satchel out from behind the fence post — a thing plainly put there some time ago, for exactly this. Received 20 LUMEN DROPS, 5 WARM BALMS, 5 TALLOW BALMS and 5,000 WICKS!',
    },
    {
      op: 'say',
      if_flag: 'flag:name_is_paul',
      speaker: 'ANDREW',
      text: 'Supplies. For the journey. Don\'t argue — I\'ve been carrying that about for ages waiting for a Paul to turn up, and my back\'s had enough.',
    },

    // --- Everyone: the nudge. -------------------------------------------------
    { op: 'say', speaker: 'ANDREW', text: 'Right. Before you go. Have you found the easter egg yet?' },
    { op: 'say', speaker: 'ANDREW', text: '...No? Fair enough. This isn\'t it, mind — I\'m just the fellow at the fence. But it IS out there. Keep looking.' },
    { op: 'setFlag', flag: 'flag:met_andrew' },
  ],

  // Andrew after the naming — he remembers, and keeps pointing at the egg.
  'script.andrew_after': [
    {
      op: 'choice',
      speaker: 'ANDREW',
      prompt: 'Still out here, {name}. Somebody has to hold the fence up. Anything I can do you for?',
      options: [
        // The wayfinding pair — same two Andrew offers on every road (see
        // `script.andrew_road`), so the fence you met him at answers them too.
        { label: 'WHERE NEXT?', ops: [{ op: 'run', ref: 'script.andrew_hint' }] },
        { label: 'THESE ROADS', ops: [{ op: 'run', ref: 'script.andrew_roads' }] },
        { label: 'THE EASTER EGG', ops: [{ op: 'run', ref: 'script.andrew_egg' }] },
        {
          label: 'CHANGE MY NAME',
          ops: [
            { op: 'say', speaker: 'ANDREW', text: 'Second thoughts? Happens. Go on then — what are we calling you?' },
            {
              op: 'askName',
              title: 'YOUR NAME',
              fallback: 'Wayfarer',
              matches: [{ value: 'Paul', flag: 'flag:name_is_paul' }],
            },
            { op: 'say', speaker: 'ANDREW', text: '{name} it is. I\'ll tell the street.' },
            // The parcel is the FIRST-meeting reward and can't be claimed twice
            // (this scene only exists once `flag:met_andrew` is held), so a late
            // Paul gets the recognition rather than a second satchel.
            { op: 'say', if_flag: 'flag:name_is_paul', speaker: 'ANDREW', text: '...Paul. PAUL. Honestly, you could have led with that.' },
          ],
        },
        {
          label: 'NOTHING',
          ops: [{ op: 'say', speaker: 'ANDREW', text: 'Right you are. Mind how you go — and mind the dark.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------------------
  // ANDREW ON THE ROAD — the wayfinding hint.
  //
  // He turns up leaning on a fence in every town on the rim, and answers the one
  // question a stuck player actually has: *where am I supposed to go next?*
  //
  // `script.andrew_hint` is a single chain of `say` steps, each guarded
  // `if_flag: <this stage>` + `unless_flag: <the next stage>`, so EXACTLY ONE of
  // them plays — the one naming the objective the player is actually on. Adding a
  // stage means splicing a line in with both guards set; get the pair wrong and
  // he either says nothing or says two things, which is the whole test.
  //
  // Direction is given the way a person gives it — compass, landmark, and the
  // name of who to ask for — never map ids or menu instructions.
  // ---------------------------------------------------------------------------
  'script.andrew_hint': [
    // --- The opening errand (before the lamp and the first kin). --------------
    {
      op: 'say', unless_flag: 'flag:fenn_errand', speaker: 'ANDREW',
      text: 'Fenn\'s waiting at [[the Crossroads waystone]]: [[east out of Tinderwick]], along the Lanternway. Go and be asked after.',
    },
    {
      op: 'say', if_flag: 'flag:fenn_errand', unless_flag: 'flag:has_satchel', speaker: 'ANDREW',
      text: 'His satchel\'s on the courier\'s cart at [[Duskapple Orchard]]: [[west from Tinderwick\'s square]], through the hedge gap.',
    },
    {
      op: 'say', if_flag: 'flag:has_satchel', unless_flag: 'flag:has_starter', speaker: 'ANDREW',
      text: '[[Take it BACK to Fenn]] at the waystone. Your lamp\'s waiting there. And your first friend.',
    },

    // --- The Ember loop: catch → Brisa → the wick → the Beacon. ---------------
    {
      op: 'say', if_flag: 'flag:has_starter', unless_flag: 'flag:caught_first_kin', speaker: 'ANDREW',
      text: '[[Catch a kin]] in any verge grass out of town. Brisa won\'t test one kin and a hopeful face.',
    },
    {
      op: 'say', if_flag: 'flag:caught_first_kin', unless_flag: 'flag:beacon_quest', speaker: 'ANDREW',
      text: '[[See Brisa Tallow]] in [[Tinderwick\'s Lumenary]]. She\'ll have an errand first. She always does.',
    },
    {
      op: 'say', if_flag: 'flag:beacon_quest', unless_flag: 'flag:has_beacon_wick', speaker: 'ANDREW',
      text: 'The Beacon\'s wick-key is with [[the Dimglass lamplighter]], [[north through Tinderwick\'s gate]]. He\'s the only lit thing on that road.',
    },
    {
      op: 'say', if_flag: 'flag:has_beacon_wick', unless_flag: 'gleam:ember', speaker: 'ANDREW',
      text: '[[Climb the Beacon]] on the north-east bluff, to the lantern room. Every keeper on the stairs wants a battle.',
    },

    // --- The eight Gleams, in journey order. ----------------------------------
    // Ember → Tide is five steps (R9: Reyl's hook, the Old Light, the floats, the
    // bell, the bond-test) — run as a nested precedence chain so EXACTLY one line
    // plays even for an old save holding a later flag without an earlier one
    // (e.g. the rope from before the tower existed).
    { op: 'run', ref: 'script.andrew_hint_tide', if_flag: 'gleam:ember', unless_flag: 'gleam:tide' },
    {
      op: 'say', if_flag: 'gleam:ember', unless_flag: 'gleam:tide', speaker: 'ANDREW',
      text: '[[Leave the fen road EAST]] and the hill NORTH for later. The fen\'s kin will flatten you. Pearlmoor\'s errand first.',
    },
    {
      op: 'say', if_flag: 'gleam:tide', unless_flag: 'gleam:verdant', speaker: 'ANDREW',
      text: 'Sable Quill keeps the Verdant at [[Lowleaf Hollow]]: [[east on the fen road]]. Tidecall gets you across now.',
    },
    // Lane E (walkthrough/10 Part III): the Tide stage also tips the home secret —
    // a nested run so its own guard (not met Gran Tallow yet) stacks on the stage's.
    { op: 'run', ref: 'script.andrew_hint_lowtinder', if_flag: 'gleam:tide', unless_flag: 'gleam:verdant' },
    {
      op: 'say', if_flag: 'gleam:verdant', unless_flag: 'gleam:stone', speaker: 'ANDREW',
      text: 'Otho Grist keeps the Stone at [[Cinderhead Mine]], through the deep wood behind Lowleaf. [[Talk to him first]], a few levels heavier.',
    },
    {
      op: 'say', if_flag: 'gleam:stone', unless_flag: 'gleam:storm', speaker: 'ANDREW',
      text: 'Mira Vael keeps the Storm at [[the Galehigh Terraces]]: out the Deep\'s far door, up Cinderwind Scarp, over the Ashfall Shelf.',
    },
    {
      op: 'say', if_flag: 'gleam:storm', unless_flag: 'gleam:frost', speaker: 'ANDREW',
      text: 'Ysolde Frost keeps the Frost at [[the Pale Vault Glacier]], [[up the Windward Stair]]. The Kite clears the crags. Wrap up.',
    },
    {
      op: 'say', if_flag: 'gleam:frost', unless_flag: 'gleam:solar', speaker: 'ANDREW',
      text: 'Lucan Pyre keeps the Solar in [[the Sunken Solarium]], [[west through Hushfrost Pass]]. Emberward gets you through the coldfog.',
    },
    {
      op: 'say', if_flag: 'gleam:solar', unless_flag: 'gleam:lunar', speaker: 'ANDREW',
      text: 'Nessa Cole keeps the Lunar at [[Nightreach Observatory]], [[up the Sunvault Climb]]. Sunsketch blooms the bridges. Your eighth!',
    },

    // --- The Crown, the Spire, and after. -------------------------------------
    // (one stage: the line + a P.S. for the optional last road under the Ring, Lane FD)
    { op: 'run', ref: 'script.andrew_hint_crown', if_flag: 'gleam:lunar', unless_flag: 'flag:keystar_relit' },
    {
      op: 'say', if_flag: 'flag:keystar_relit', unless_flag: 'flag:dawn', speaker: 'ANDREW',
      text: 'The Keystar\'s lit. Whatever comes next is coming on its own. Stand still and let it.',
    },
    {
      op: 'say', if_flag: 'flag:dawn', unless_flag: 'flag:q_isles', speaker: 'ANDREW',
      text: 'Next? Nothing, {name}. Look UP. Then walk down to [[Dawnstead]] and see the valley in the morning. Nightreach has fallen stars to read, they say.',
    },
    // --- The Farlamp Isles (walkthrough/10 Part I, optional post-game): once Ione
    // has asked for the prow-lamp, the chain answers "where next?" for the isles.
    {
      op: 'say', if_flag: 'flag:q_isles', unless_flag: 'flag:q_isles_prow_lit', speaker: 'ANDREW',
      text: '[[Light Ione\'s prow-lamp]] from Fenn\'s own lamp. He\'s [[at Dawnstead]], on the front.',
    },
    {
      op: 'say', if_flag: 'flag:q_isles_prow_lit', unless_flag: 'flag:q_isles_afloat', speaker: 'ANDREW',
      text: 'Lamp lit? [[Back to Ione]] on Lightkeeper\'s Point, west of Pearlmoor. Her boat\'s waited eleven winters.',
    },
    {
      op: 'say', if_flag: 'flag:q_isles_afloat', unless_flag: 'flag:q_isles_fogglass', speaker: 'ANDREW',
      text: '[[South, then west to the Fogwall]]. You\'ll need the keepers\' glass, from [[the sea-caves]] under Gullwrack and Kelpcrown.',
    },
    {
      op: 'say', if_flag: 'flag:q_isles_fogglass', unless_flag: 'flag:q_isles_driftholm', speaker: 'ANDREW',
      text: 'The glass reads the buoys. [[Follow the lit ones south]] to a town that hasn\'t seen a boat in eleven winters.',
    },
    {
      op: 'say', if_flag: 'flag:q_isles_driftholm', unless_flag: 'flag:isles_dawn', speaker: 'ANDREW',
      text: '[[Nan Creel]], Driftholm\'s elder, keeps the well-stair key. It goes under the sea to the drowned Farlamp. Light it, {name}.',
    },
    {
      op: 'say', if_flag: 'flag:isles_dawn', speaker: 'ANDREW',
      text: 'The isles have their morning. Next? Nothing. Go and battle [[Bram Fathom]] on Driftholm\'s quay.',
    },
  ],

  // The Crown stage of `script.andrew_hint`: the Spire, then a P.S. (Lane FD,
  // walkthrough/11 Part D) for the optional last road under the Ring once the hub
  // is open. The P.S. lives in script.underways_hint (regions/underways.ts).
  'script.andrew_hint_crown': [
    {
      op: 'say', speaker: 'ANDREW',
      text: 'Eight! [[The Spire]]\'s up the mountain road, [[north from the Crossroads]]. And it isn\'t a patient sort of waiting.',
    },
    { op: 'run', ref: 'script.underways_hint', if_flag: 'flag:hub_unlocked' },
  ],

  // The Ember → Tide leg of `script.andrew_hint`, latest stage first: each
  // `run` only fires while the stage above it isn't held, so one line plays.
  'script.andrew_hint_tide': [
    {
      op: 'say', if_flag: 'flag:q_south_bell_rung', speaker: 'ANDREW',
      text: 'Bell\'s rung. [[Reyl\'s waiting in the Lumenary]]. Rest first, and bring a Verdant kin. The tide hates a green thing.',
    },
    { op: 'run', ref: 'script.andrew_hint_tide_rope', unless_flag: 'flag:q_south_bell_rung' },
  ],
  'script.andrew_hint_tide_rope': [
    {
      op: 'say', if_flag: 'flag:q_south_has_rope', speaker: 'ANDREW',
      text: 'Rope in hand? [[Out along the breakwater]] to the moor-bell, and [[ring it]]. Loud as you like.',
    },
    { op: 'run', ref: 'script.andrew_hint_tide_floats', unless_flag: 'flag:q_south_has_rope' },
  ],
  'script.andrew_hint_tide_floats': [
    {
      op: 'say', if_flag: 'flag:q_south_jest_done', speaker: 'ANDREW',
      text: 'Got the floats? [[Take them to the netmender]] on the quay. She\'s had a rope put by for years.',
    },
    { op: 'run', ref: 'script.andrew_hint_tide_tower', unless_flag: 'flag:q_south_jest_done' },
  ],
  'script.andrew_hint_tide_tower': [
    {
      op: 'say', if_flag: 'flag:q_south_bell', speaker: 'ANDREW',
      text: '[[The Old Light]]: [[west off the quay]] on the beach path, out to the Point. The one cackling at the gulls. Tea halfway up.',
    },
    {
      op: 'say', unless_flag: 'flag:q_south_bell', speaker: 'ANDREW',
      text: '[[Pearlmoor Quay]] next, up the coast road. See Reyl Wash at [[the LUMENARY up top]]. He keeps the Tide, and he\'ll have a job.',
    },
  ],

  // Why the roads bring you back where you started — the shape of Vesperholm,
  // told as a virtue instead of a wrong turn. (Playtest: a first-timer walked a
  // full circle, arrived somewhere familiar from a new direction, and read it as
  // being lost. It is in fact the design — level-design.md §2b rule 1 — so the
  // world now says so out loud, here and in the LORE codex.)
  'script.andrew_roads': [
    { op: 'say', speaker: 'ANDREW', text: 'Ha! Noticed, then. Walk far enough any way here and you come out somewhere you\'ve been.' },
    { op: 'say', speaker: 'ANDREW', text: 'That\'s the shape of the place. The valleys sit in a crescent, threaded on the Lanternway. Every road bends back to the Crossroads.' },
    { op: 'say', speaker: 'ANDREW', text: 'You never backtrack in Vesperholm. You come ROUND. The way home is never the way you went.' },
    { op: 'say', speaker: 'ANDREW', text: 'A road drops you at a gate you know? Not a wrong turn. A shortcut you\'ve earned.' },
  ],

  // The road placements (id `andrew_road` in every map that carries one, so the
  // emote resolves wherever he's standing).
  'script.andrew_road': [
    { op: 'emote', actor: 'andrew_road', emote: 'alert' },
    {
      op: 'say', unless_flag: 'flag:met_andrew', speaker: 'ANDREW',
      text: 'Hullo! Andrew. I hold fences up. There\'s one in Tinderwick with my name on it, if you fancy telling me yours.',
    },
    {
      op: 'say', if_flag: 'flag:met_andrew', speaker: 'ANDREW',
      text: 'There you are, {name}. Somebody has to hold the fences up out here as well.',
    },
    {
      op: 'choice',
      speaker: 'ANDREW',
      prompt: 'Anything I can do you for?',
      options: [
        { label: 'WHERE NEXT?', ops: [{ op: 'run', ref: 'script.andrew_hint' }] },
        { label: 'THESE ROADS', ops: [{ op: 'run', ref: 'script.andrew_roads' }] },
        { label: 'THE EASTER EGG', ops: [{ op: 'run', ref: 'script.andrew_egg' }] },
        { label: 'NOTHING', ops: [{ op: 'say', speaker: 'ANDREW', text: 'Right you are. Mind how you go — and mind the dark.' }] },
      ],
    },
  ],
  // ---------------------------------------------------------------------------
  // ANDREW'S EASTER EGGS — "have I found it yet?"
  //
  // Every Andrew answers THE EASTER EGG with the player's status, then one
  // subtle nudge toward the next step. Same single-chain pattern as
  // `script.andrew_hint`: each line is guarded `if_flag: <stage>` +
  // `unless_flag: <next stage>`, so EXACTLY ONE plays.
  //
  // The egg is the Chickenpig (#163, S4 "The Booji-Wooji Man") — Andrew never
  // names it until it's in your lamp. Once it is, he admits there's ONE more,
  // for the bold: S5 "Not All Who Wander" (the Wanderwood). Once the cup is
  // won he says, plainly, that's the lot. Stages:
  //   A  nothing yet, can't reach the coast town   (unless gleam:ember)
  //   B  can head south, quest not started         (gleam:ember → q_south_booji)
  //   C  on the trail at the Lifting House         (q_south_booji → _met)
  //   D  met the old man, egg not caught           (_met → chickenpig_caught)
  //   E  FOUND IT — one more, if you're bold       (chickenpig_caught → q_south_wander)
  //   F  on the last one                           (q_south_wander → _done)
  //   G  found them all                            (q_south_wander_done)
  // ---------------------------------------------------------------------------
  // Leaving Pearlmoor for the fen with the Tide Gleam but no egg (owner, 2026-10):
  // Andrew runs over ONCE and spells out exactly where it is from where you stand —
  // gym first, then the harbour; or straight to the harbour; or back to the lamp.
  // A step_on tile in front of the fen exit (the quay's one-tile choke, (26,12);
  // tools/maps/hand_placed_data.py). Never says what the egg is.
  'script.egg_nudge_fen': [
    { op: 'run', ref: 'script.egg_nudge_body', unless_flag: 'flag:chickenpig_caught' },
    { op: 'setFlag', flag: 'flag:egg_nudge_seen' },
  ],
  'script.egg_nudge_body': [
    { op: 'emote', actor: 'andrew_road', emote: 'alert' },
    { op: 'say', speaker: 'ANDREW', text: '{name}! Hang on! Wait up!' },
    // one straight leg per move (the cutscene walk is greedy x-then-y; route
    // computed on the real collision model from his fence at (10,17))
    { op: 'move', actor: 'andrew_road', to: { tx: 21, ty: 17 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 21, ty: 16 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 22, ty: 16 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 22, ty: 13 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 23, ty: 13 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 23, ty: 12 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 25, ty: 12 }, speed: 2 },
    { op: 'face', actor: 'andrew_road', facing: 'right' },
    { op: 'face', actor: 'player', facing: 'left' },
    { op: 'say', speaker: 'ANDREW', text: 'Are you sure you want to head out this way? You\'ve not found the easter egg yet, and it\'s back the other way. Right here in Pearlmoor.' },
    {
      op: 'say', unless_flag: 'flag:q_south_booji', speaker: 'ANDREW',
      text: 'Here\'s how. First, [[the Lifting House]] at the top of the quay. Ask the lifters about the old man they\'re always on about. Ask ALL of them.',
    },
    {
      op: 'say', unless_flag: 'flag:q_south_booji', speaker: 'ANDREW',
      text: 'Then the harbour: through [[the moor-gate]] at the quay\'s south end, along the breakwater, past the bell, right to where the boards give up.',
    },
    {
      op: 'say', if_flag: 'flag:q_south_booji', unless_flag: 'flag:q_south_booji_met', speaker: 'ANDREW',
      text: 'You\'ve had the lifters\' stories. Straight down: [[the moor-gate]] at the quay\'s south end, the breakwater, past the bell. He\'ll be there.',
    },
    {
      op: 'say', if_flag: 'flag:q_south_booji_met', speaker: 'ANDREW',
      text: 'You\'ve met him, so you\'re close. Back down the breakwater to [[his dark lamp]]. Something sleeps at its foot. Ask him to wake it.',
    },
    { op: 'say', speaker: 'ANDREW', text: 'The fen\'ll keep. It\'s been wet for years. Or go on, and ask me about THE EASTER EGG on any fence when you\'re ready.' },
    { op: 'move', actor: 'andrew_road', to: { tx: 23, ty: 12 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 23, ty: 13 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 22, ty: 13 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 22, ty: 16 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 21, ty: 16 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 21, ty: 17 }, speed: 2 },
    { op: 'move', actor: 'andrew_road', to: { tx: 10, ty: 17 }, speed: 2 },
    { op: 'face', actor: 'andrew_road', facing: 'down' },
  ],
  'script.andrew_egg': [
    // A
    {
      op: 'say', unless_flag: 'gleam:ember', speaker: 'ANDREW',
      text: 'Found it yet? No — and that\'s no slight on you. You can\'t get to it from here. Not yet.',
    },
    {
      op: 'say', unless_flag: 'gleam:ember', speaker: 'ANDREW',
      text: 'All I\'ll say: it\'s a long way up the coast, where the land gives up and the town carries on regardless. [[Get your first Gleam]] first.',
    },
    // B
    {
      op: 'say', if_flag: 'gleam:ember', unless_flag: 'flag:q_south_booji', speaker: 'ANDREW',
      text: 'Found it yet? Not yet. You\'re warm, though — or you will be, once you\'re standing on Pearlmoor Quay.',
    },
    {
      op: 'say', if_flag: 'gleam:ember', unless_flag: 'flag:q_south_booji', speaker: 'ANDREW',
      text: 'Go to [[the very top of the quay]]. Folk there lift heavy things and talk about an old man more than they lift. Ask ALL of them.',
    },
    // C
    {
      op: 'say', if_flag: 'flag:q_south_booji', unless_flag: 'flag:q_south_booji_met', speaker: 'ANDREW',
      text: 'Found it yet? Not quite — but you\'re on the trail, I can tell. You\'ve got that look the Lifting House gives people.',
    },
    {
      op: 'say', if_flag: 'flag:q_south_booji', unless_flag: 'flag:q_south_booji_met', speaker: 'ANDREW',
      text: 'He walks [[the breakwater]], past the bell, right out where the boards give up. Go and meet him.',
    },
    {
      op: 'say', if_flag: 'flag:q_south_booji', unless_flag: 'flag:q_south_has_rope', speaker: 'ANDREW',
      text: 'Gate chained? It opens for [[the netmender\'s rope]]; Reyl at the Lumenary sets you on the way, up the Old Light. Ask me WHERE NEXT? any time.',
    },
    // D
    {
      op: 'say', if_flag: 'flag:q_south_booji_met', unless_flag: 'flag:chickenpig_caught', speaker: 'ANDREW',
      text: 'You MET him? Ha! Then you\'re standing right next to it. ...But no. You haven\'t found it. Not yet.',
    },
    {
      op: 'say', if_flag: 'flag:q_south_booji_met', unless_flag: 'flag:chickenpig_caught', speaker: 'ANDREW',
      text: 'The egg isn\'t the old man, exactly. Look at [[the foot of his dark lamp]]. Something sleeps there that thinks it\'s morning. Ask him to wake it.',
    },
    // E
    {
      op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander', speaker: 'ANDREW',
      text: 'Wait — is that a rooster-pig in your lamp? You FOUND it! That\'s the egg, {name}. That\'s the one. Well done. Genuinely.',
    },
    {
      op: 'say', if_flag: 'flag:chickenpig_caught', unless_flag: 'flag:q_south_wander', speaker: 'ANDREW',
      text: '...Mostly. There IS one more, only for the bold. Go back to [[the old man]] and ask whether he ever gets lost.',
    },
    // F
    {
      op: 'say', if_flag: 'flag:q_south_wander', unless_flag: 'flag:q_south_wander_done', speaker: 'ANDREW',
      text: 'Going after the last one, are you? Brave. One found, one to go.',
    },
    {
      op: 'say', if_flag: 'flag:q_south_wander', unless_flag: 'flag:q_south_wander_done', speaker: 'ANDREW',
      text: '[[Up the hill behind the quay]], past Rod\'s allotment. A stone there wants the end of a famous line. Bring the bird. I\'ll see you in there.',
    },
    // G
    {
      op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'ANDREW',
      text: 'Found them? Both of them. The rooster-pig AND the old wood. That\'s the lot, {name} — there aren\'t any more. Honest. I\'ve checked my pockets.',
    },
    {
      op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'ANDREW',
      text: 'Everything else out there is just the game being a game. Which, I\'d argue, is the best egg of all. Go on — the sky still wants relighting.',
    },
  ],

  // Andrew in the Wanderwood (`andrew_wood`). The bold player's reward: he says
  // out loud that THIS is the last of his easter eggs, so nobody spends the rest
  // of the game hunting for a third.
  'script.andrew_wood': [
    { op: 'emote', actor: 'andrew_wood', emote: 'alert' },
    {
      op: 'say', unless_flag: 'flag:q_south_wander_done', speaker: 'ANDREW',
      text: 'There you are, {name}. Told you I\'d see you in here. Somebody has to hold the trees up.',
    },
    {
      op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'ANDREW',
      text: 'Back again, {name}? Can\'t blame you. It\'s a good wood for not being lost in.',
    },
    {
      op: 'choice',
      speaker: 'ANDREW',
      prompt: 'Anything I can do you for?',
      options: [
        {
          label: 'IS THIS AN EGG?',
          ops: [
            { op: 'say', speaker: 'ANDREW', text: 'It is. This wood is the LAST. The rooster-pig was the first; you\'re standing in the second. There isn\'t a third — I promise.' },
            { op: 'say', unless_flag: 'flag:q_south_wander_done', speaker: 'ANDREW', text: 'The old man\'s waiting in the middle. Read his trees on the way — he\'d never say so, but he carved them for whoever came looking.' },
            { op: 'say', if_flag: 'flag:q_south_wander_done', speaker: 'ANDREW', text: 'And you\'ve done it — the bird, the glade, the cup. That\'s every egg I hid. From here on it\'s just you, the road, and the sky. Not a bad trade.' },
          ],
        },
        { label: 'WHERE NEXT?', ops: [{ op: 'run', ref: 'script.andrew_hint' }] },
        { label: 'NOTHING', ops: [{ op: 'say', speaker: 'ANDREW', text: 'Right you are. Mind the roots — and mind the dark.' }] },
      ],
    },
  ],

  // ===========================================================================
  // THE PERIL THREAD (R9) — the Long Dusk made visible, escalating across the
  // journey and HEALING as the player relights the sky. Design + beat table:
  // docs/world/walkthrough/08-the-peril-thread.md. All optional colour: no beat
  // gates a road or sets a progression flag. Staging is the single-chain
  // if_flag/unless_flag pattern (script.andrew_hint): exactly one stage line
  // plays, keyed to flags the journey already sets. Placements: Duskapple's own
  // builder + tools/maps/add_peril_thread.py (re-run after any map rebuild).
  // ===========================================================================

  // S1 — FIRST SIGHT of the fallen star (Duskapple Orchard, once, on the mouth
  // band). Everyone sees it: the satchel errand brings every player here. The
  // "a light fails" register, held short: letterbox + quiet + the gutter sting.
  'script.orchard_first_sight': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 700 },
    { op: 'cameraFocus', to: { tx: 8, ty: 4 }, ms: 1000 },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'Past the stall, the old rows end in a black wound in the earth.' },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', text: 'The grass is scorched in a ring. Two trees burnt to the bone. Where a third stood, a dark stone sits in ash, coldly aglow.' },
    { op: 'narrate', text: 'A star fell here. Or what was left of one.' },
    { op: 'cameraReset', ms: 800 },
    // Back to the orchard's own bed — the fallen-star cue until the first Gleam
    // (maps.ts music_when); this scene only ever plays on the first visit.
    { op: 'musicCrossfade', key: 'duskapple-orchard', ms: 900 },
    { op: 'letterbox', on: false, ms: 320 },
  ],

  // Old Wendel: the grief first, then his standing orchard lines (the apples,
  // the hedge wink, the meadow pointer — npc.orchard_wendel, unchanged).
  'script.orchard_wendel': [
    { op: 'say', unless_flag: 'gleam:ember', speaker: 'OLD WENDEL', text: 'Three nights back, one of the little stars over the hedge just... let go. Came down like a dropped lamp.' },
    { op: 'say', unless_flag: 'gleam:ember', speaker: 'OLD WENDEL', text: "Forty years, that tree. My first. Once in a lifetime, they say. I've had a lifetime. It isn't." },
    { op: 'say', if_flag: 'gleam:ember', speaker: 'OLD WENDEL', text: "I saw the Ember come back over the hedge. And there's shoots in the burn. Stubborn things. Like me." },
    { op: 'dialogue', ref: 'npc.orchard_wendel' },
  ],

  // Tamsin, Wendel's granddaughter, at the crater's lip — one line per stage:
  // shock -> fear once a star dies in front of you (dusk_begins) -> the shoots
  // (gleam:ember) -> the dawn.
  'script.orchard_tamsin': [
    { op: 'say', unless_flag: 'flag:dusk_begins', speaker: 'TAMSIN', text: "It didn't make a sound. Just light, then burning, then dark again." },
    { op: 'say', unless_flag: 'flag:dusk_begins', speaker: 'TAMSIN', text: "Grandad says stars don't fall. Grandad also says he isn't crying. Grandad says a lot of things." },
    { op: 'say', if_flag: 'flag:dusk_begins', unless_flag: 'gleam:ember', speaker: 'TAMSIN', text: "Did you see it? Another, over the sea. Mum says we keep the lamps lit all night now." },
    { op: 'say', if_flag: 'gleam:ember', unless_flag: 'flag:great_null_known', speaker: 'TAMSIN', text: "There's shoots coming up in the burn! I'm not allowed to water them. I've been watering them." },
    { op: 'say', if_flag: 'flag:great_null_known', unless_flag: 'gleam:lunar', speaker: 'TAMSIN', text: 'The stone in the burn went dark, even the blue. Just for a minute. Grandad sat down.' },
    { op: 'say', if_flag: 'gleam:lunar', unless_flag: 'flag:dawn', speaker: 'TAMSIN', text: "The shoots in the burn came back. I'm still not allowed to water them." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'TAMSIN', text: "The stone woke up! Grandad says we're keeping it. I say keeping it AND naming it." },
  ],

  // S2 (deferred placement — Tinderwick, by the west hedge gap; see the doc):
  // a neighbour who keeps a lamp in the window.
  'script.peril_tinderwick_neighbour': [
    { op: 'say', unless_flag: 'flag:dusk_begins', speaker: 'NEIGHBOUR', text: "The night the star fell on Wendel's trees, did you hear it? Nor did anyone. That's what's wrong with it." },
    { op: 'say', unless_flag: 'flag:dusk_begins', speaker: 'NEIGHBOUR', text: "I leave a lamp in the window all night now. Can't tell you why. It feels like manners." },
    { op: 'say', if_flag: 'flag:dusk_begins', unless_flag: 'gleam:ember', speaker: 'NEIGHBOUR', text: 'Another went out over the sea. Every window has a lamp now. A festival that forgot to start.' },
    { op: 'say', if_flag: 'gleam:ember', unless_flag: 'flag:great_null_known', speaker: 'NEIGHBOUR', text: 'The Ember, back! First night in a month I blew my window lamp out. And I slept.' },
    { op: 'say', if_flag: 'flag:great_null_known', unless_flag: 'gleam:lunar', speaker: 'NEIGHBOUR', text: "Window lamps back in every house. Don't tell me why. I know why." },
    { op: 'say', if_flag: 'gleam:lunar', unless_flag: 'flag:dawn', speaker: 'NEIGHBOUR', text: 'The Ember, steady again. I blew my window lamp out. And I slept.' },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'NEIGHBOUR', text: "Daylight on the square. I keep checking the sky's still there. It always is." },
  ],

  // E1 — Saltreach Fen I: a fen family with their bundles at the landing.
  'script.peril_fen_leaver': [
    { op: 'say', unless_flag: 'gleam:verdant', speaker: 'FEN MOTHER', text: "We're off west to my sister's. She says Pearlmoor's lamps are holding." },
    { op: 'say', unless_flag: 'gleam:verdant', speaker: 'FEN MOTHER', text: "Mother's lamp went out and wouldn't take a match. Not the wick. The lamp. You don't stay, after that." },
    { op: 'say', if_flag: 'gleam:verdant', unless_flag: 'flag:dawn', speaker: 'FEN MOTHER', text: "We unpacked. Lowleaf's Gleam came up, and Mother's lamp took first strike. Don't tell anyone I cried." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'FEN MOTHER', text: 'The reeds are GOLD by daylight! Forty years on these planks and I never knew.' },
  ],

  // N1 — Galehigh Terraces: the weaver beside the Hollowing's notice.
  'script.peril_notice_reader': [
    { op: 'say', unless_flag: 'gleam:storm', speaker: 'TERRACE WEAVER', text: "Someone pins it up at night. I've torn it down twice. It's back by morning." },
    { op: 'say', unless_flag: 'gleam:storm', speaker: 'TERRACE WEAVER', text: "Worst is how kind the hand is. You think: well. They're not wrong that I'm tired." },
    { op: 'say', if_flag: 'gleam:storm', unless_flag: 'flag:met_cor', speaker: 'TERRACE WEAVER', text: "Gleam's back, and still someone read it tonight. I left it up. Folk should choose." },
    { op: 'say', if_flag: 'flag:met_cor', unless_flag: 'flag:dawn', speaker: 'TERRACE WEAVER', text: "He came through, the man who writes them. Took nothing. He doesn't have to. People go to him." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'TERRACE WEAVER', text: "Took it down; nobody reads it now. Kept it. Seemed rude to burn something that gentle." },
  ],

  // N2 — Hushfrost Pass: the SECOND FALL, and the pass-walker who counts them.
  'script.peril_hushfrost_counter': [
    { op: 'say', unless_flag: 'gleam:frost', speaker: 'PASS-WALKER', text: 'That came down four nights ago. I felt it through my boots first.' },
    { op: 'say', if_flag: 'flag:orchard_strike_seen', unless_flag: 'gleam:frost', speaker: 'PASS-WALKER', text: "You'll have seen old Wendel's orchard, south. That was the first anyone talked about." },
    { op: 'say', unless_flag: 'gleam:frost', speaker: 'PASS-WALKER', text: "This is the fourth. I've marked them on a map. Each one nearer the mountain." },
    { op: 'say', if_flag: 'gleam:frost', unless_flag: 'flag:dawn', speaker: 'PASS-WALKER', text: "The cinder's stopped hissing in the drift. Just cold now. Cold, I understand." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'PASS-WALKER', text: 'It woke! Bright as a hearth in the snow. I took the map down.' },
  ],

  // W1 — Sunvault Climb: the family who chose the quiet. Never villains: grief,
  // and a decision the player is allowed to understand.
  'script.peril_quiet_family': [
    { op: 'say', unless_flag: 'gleam:solar', speaker: 'QUIET FATHER', text: "We put the brazier out ourselves. Don't look so stricken, love. It was our choice." },
    { op: 'say', unless_flag: 'gleam:solar', speaker: 'QUIET FATHER', text: "We lost Grandad last winter. The Quiet folk said: you'll never watch anything fade again. It sounded like mercy. Some nights it still does." },
    { op: 'say', if_flag: 'gleam:solar', unless_flag: 'flag:dawn', speaker: 'QUIET FATHER', text: "My youngest lit it while I slept. With the Solar Gleam overhead, I hadn't the heart to put it out." },
    { op: 'say', if_flag: 'gleam:solar', unless_flag: 'flag:dawn', speaker: 'QUIET FATHER', text: "I don't know what we believe now. But it's warm, and she's smiling." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'QUIET FATHER', text: "We're walking home tomorrow. In daylight. Fancy that. Fancy us." },
  ],

  // W2 — Nightreach: the Ledger of Lights, where the count only ever went up.
  'script.peril_ledger': [
    { op: 'say', unless_flag: 'flag:great_null_known', speaker: 'LEDGER-KEEPER', text: "Every light gone out since the Dusk, I've written down. Two hundred and six. Somebody ought to remember them." },
    { op: 'say', unless_flag: 'flag:great_null_known', speaker: 'LEDGER-KEEPER', text: 'Eleven years, one column. It only ever goes the one way.' },
    { op: 'say', if_flag: 'flag:great_null_known', unless_flag: 'gleam:lunar', speaker: 'LEDGER-KEEPER', text: "They mean to put out the Keystar, Nessa says. I've ruled a line. My hand won't write on it." },
    { op: 'say', if_flag: 'flag:great_null_known', unless_flag: 'gleam:lunar', speaker: 'LEDGER-KEEPER', text: "Some names I've marked FELL. Thirty-one. All nearer the mountain." },
    { op: 'say', if_flag: 'gleam:lunar', unless_flag: 'flag:dawn', speaker: 'LEDGER-KEEPER', text: "Tonight I opened a second column: RELIT. Eight lines, all yours." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'LEDGER-KEEPER', text: "I've stopped counting the dark ones. Counting mornings now. So far: a few." },
  ],

  // C1 — the Penumbra Ring: folk from the valleys that went quiet, come to see
  // whether the Spire is real.
  'script.peril_gone_quiet': [
    { op: 'say', unless_flag: 'flag:dawn', speaker: 'MARSH-VILLAGER', text: "We're from the marsh villages that went quiet. Came to see if the Spire was real. It is." },
    { op: 'say', unless_flag: 'flag:dawn', speaker: 'MARSH-VILLAGER', text: "Going up? We'll keep a lamp lit for you at the ring. It's what we've got left to give." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'MARSH-VILLAGER', text: 'We kept the lamp lit, and you came down in the morning. We are going home now.' },
  ],
  // R9 "The Old Light" — Lightkeeper's Point + the joke-tower (content/oldlight.ts).

  // ===========================================================================
  // R9 — THE OLD LIGHT, talked about. Three townsfolk who point the way to the
  // laughing lighthouse on Lightkeeper's Point (west along Pearlmoor's beach
  // path), each staged single-chain on the Causeway Bell flags: BEFORE Reyl
  // sends you (q_south_bell) it's gossip; WHILE you owe the climb it's
  // directions; AFTER (q_south_jest_done) it's relief. Their speech borrows the
  // real Paul's habits: the lowercase "p." sign-off, the "!!!!!!", the unholy
  // laughter, the Luddite / bit-of-an-anarchist self-description, REASSESS,
  // "three robots walked into a bar" and "how are the cheese-buns?".
  // ===========================================================================
  // Fisher Agnes Pell — on Pearlmoor's beach by the path west (the junction).
  'script.oldlight_hint_beach': [
    { op: 'say', unless_flag: 'flag:q_south_bell', speaker: 'AGNES', text: 'Hear that? Out west, past the beach. The Old Light. It LAUGHS. All night. Unholy laughter, my old dad would\'ve called it!!!!!!' },
    { op: 'say', unless_flag: 'flag:q_south_bell', speaker: 'AGNES', text: 'Reyl won\'t talk about it. [[Ask him at the Lumenary]], then follow [[the beach path west]]. You\'ll know it when it laughs at you.' },
    { op: 'say', if_flag: 'flag:q_south_bell', unless_flag: 'flag:q_south_jest_done', speaker: 'AGNES', text: 'He sent you up it, didn\'t he. [[Follow this path WEST]] to the end of the beach. The Point\'s round the corner.' },
    { op: 'say', if_flag: 'flag:q_south_bell', unless_flag: 'flag:q_south_jest_done', speaker: 'AGNES', text: 'Seven floors of jokes, they say. Answer how you like — it\'s not the answer it wants, love, it\'s the company. Tea halfway up.' },
    { op: 'say', if_flag: 'flag:q_south_jest_done', speaker: 'AGNES', text: 'It\'s stopped laughing AT us. Started laughing WITH us. There\'s a difference, and the whole beach can hear it.' },
  ],
  // Old Ambrose — a self-declared Luddite on the Lumenary forecourt, reading
  // a battered book with every margin filled in.
  'script.oldlight_hint_luddite': [
    { op: 'say', unless_flag: 'flag:q_south_jest_done', speaker: 'AMBROSE', text: 'Thinking machine in the Old Light, they say. Writes its OWN jokes. I\'m a bit of a Luddite — and a bit of an anarchist, on Tuesdays.' },
    { op: 'say', unless_flag: 'flag:q_south_bell', speaker: 'AMBROSE', text: 'A machine that laughs alone all night isn\'t a menace. It\'s lonely. [[Ask Reyl]] why. Then west along the beach path.' },
    { op: 'say', if_flag: 'flag:q_south_bell', unless_flag: 'flag:q_south_jest_done', speaker: 'AMBROSE', text: 'Off up it? My one rule for clever machines: whatever it tells you, REASSESS. Ask again next year. — p. wrote that in my book. Good man.' },
    { op: 'say', if_flag: 'flag:q_south_jest_done', speaker: 'AMBROSE', text: 'So it CAN tell a joke no one\'s told. Took two of you, mind. It\'s in my margin. Next to "REASSESS". Next to "how are the cheese-buns?"' },
  ],
  // Tobias Quill — a traveller on Dimglass Coast II, just short of Pearlmoor.
  'script.oldlight_hint_road': [
    { op: 'say', unless_flag: 'flag:q_south_jest_done', speaker: 'TOBIAS', text: 'Three clockwork lamplighters walk into an inn— no, wait, don\'t go, I\'ve not got the end. Nobody has. That\'s the trouble.' },
    { op: 'say', unless_flag: 'flag:q_south_jest_done', speaker: 'TOBIAS', text: 'Heard it from the lighthouse past Pearlmoor\'s west beach. I may be overestimating my theatrical skills, but I laughed too!!!!!!' },
    { op: 'say', unless_flag: 'flag:q_south_bell', speaker: 'TOBIAS', text: 'The ferryman Reyl\'s the one to ask. [[Up at the Lumenary]], top of the quay.' },
    { op: 'say', if_flag: 'flag:q_south_jest_done', speaker: 'TOBIAS', text: 'Somebody finished it! The lighthouse joke! I came back down the coast just to tell you I don\'t know the ending — and I\'m DELIGHTED.' },
  ],

  ...NETMENDER_HAIL_SCRIPTS,
  ...OLDLIGHT_SCRIPTS,
  ...REGION_EXTRA_SCRIPTS,
  ...INTERLUDE_SCRIPTS, // X-4 crown interludes (content/interludes.ts)
  ...KINCHAT_SCRIPTS, // ambient-kin greeting events (content/kinchatter.ts)
};

export function getScript(ref: string): import('./types').CutsceneStep[] | undefined {
  return SCRIPTS[ref];
}
