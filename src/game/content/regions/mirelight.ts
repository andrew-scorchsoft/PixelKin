/**
 * THE WILD WAYS (2026-10, docs/world/walkthrough/09-the-wild-ways.md) — the Mirelights (B): the Glassmere ferry, the false lights, Lanthorne.
 * This area's lane OWNS this file: new scripts + dialogue only, spread into the
 * registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * The lore (story-bible §11, the cinder law): the Glassmere's wandering blue
 * lights were once ONE light — the fen's own lamp, a kin that walked the drowned
 * causeway ahead of lost boats and brought them home. The Hollowing, in its early
 * kindness, put it to sleep in a null-lantern so nothing could ever hurt it; a
 * sleeping luminous kin starves its star (rule 2). What's left are its dreams:
 * false lights that lead nowhere. Elegiac and cosy, never horror.
 *
 * Flags this file owns:
 *   flag:q_mirelight_begun     the eel-wife asks you to look for Tobin (JOURNAL start)
 *   flag:q_mirelight_ansel     Ansel names his price: a Pale Vault true-eye
 *   flag:mirelight_ferry       Ansel has seen the Frostglass Lens — the ferry runs
 *   flag:mirelight_crossed     the first (narrated) crossing is done
 *   flag:mirelight_tobin_found Tobin found in the sunk street; he's home after
 *   flag:lanthorne_caught      the fen's lamp is woken and yours (the legendaryBattle)
 * Read, set elsewhere: flag:has_frostglass_lens (Isel the lens-grinder, Pale Vault —
 * the Rimeway lane).
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const BEGUN = 'flag:q_mirelight_begun';
const ASKED = 'flag:q_mirelight_ansel';
const LENS = 'flag:has_frostglass_lens';
const FERRY = 'flag:mirelight_ferry';
const CROSSED = 'flag:mirelight_crossed';
const TOBIN = 'flag:mirelight_tobin_found';
const CAUGHT = 'flag:lanthorne_caught';

/** A false board gives way: a splash, and you haul out at the walk's mouth. */
function dunk(map: string, tx: number, ty: number, facing: 'up' | 'down' | 'left' | 'right', line: string): CutsceneStep[] {
  return [
    { op: 'sfx', key: 'world-splash' },
    { op: 'shake', ms: 260, intensity: 0.004 },
    { op: 'narrate', text: line },
    { op: 'travel', map, to: { tx, ty }, facing },
    { op: 'narrate', text: 'You haul out at the boards\' mouth, dripping. The blue light hangs on, patient.' },
  ];
}

/** Old Ansel's stage (the blocked ferry warp on row `y` of the fen's east edge). */
function anselStage(y: number): ScriptRegistry {
  const k = `script.mirelight_ansel_stage_${y}`;
  return {
    [k]: [
      { op: 'dialogue', ref: 'npc.mirelight_ansel_blocked', unless_flag: LENS },
      { op: 'run', ref: `${k}_lens`, if_flag: LENS },
    ],
    [`${k}_lens`]: [
      { op: 'emote', actor: 'ansel', emote: 'alert' },
      { op: 'face', actor: 'player', facing: 'left' },
      { op: 'move', actor: 'ansel', to: { tx: 28, ty: 23 } },
      { op: 'move', actor: 'ansel', to: { tx: 30, ty: y } },
      { op: 'face', actor: 'ansel', facing: 'right' },
      { op: 'run', ref: 'script.mirelight_ansel' },
      { op: 'run', ref: 'script.mirelight_ferry_ride', if_flag: FERRY },
    ],
  };
}

export const MIRELIGHT_SCRIPTS: ScriptRegistry = {
  // ---- Saltreach Fen I: the eel-wife's ask + Old Ansel's stage --------------------------
  'script.mirelight_eelwife': [
    { op: 'run', ref: 'script.fen_eelwife' },
    { op: 'say', if_flag: BEGUN, unless_flag: TOBIN, speaker: 'EEL-WIFE', text: 'No sign of my Tobin? ...No. Half the fen says the lights took him. The other half says he\'s too stubborn to be took.' },
    { op: 'face', unless_flag: BEGUN, actor: 'fen_eelwife', facing: 'right' },
    { op: 'say', unless_flag: BEGUN, speaker: 'EEL-WIFE', text: 'You\'ve a lamp. Then I\'ll ask what I ask everyone with a lamp. Look east, over the water. See the blue ones?' },
    { op: 'say', unless_flag: BEGUN, speaker: 'EEL-WIFE', text: 'The Mirelights. My boy Tobin rowed out after them at the season\'s turn. Said one was waving at him. He\'s eleven. Everything waves when you\'re eleven.' },
    { op: 'say', unless_flag: BEGUN, speaker: 'EEL-WIFE', text: '[[Old Ansel]] keeps the ferry stage [[at the east end]]. He won\'t cross — but someone with a lamp might shift him. Look for my boy out there.' },
    { op: 'setFlag', unless_flag: BEGUN, flag: BEGUN },
    { op: 'say', if_flag: TOBIN, speaker: 'EEL-WIFE', text: 'He\'s HOME. On my step eating eel-pie like he never left. If he so much as looks at a blue light again, I\'ll cut him into the reeds myself.' },
  ],
  'script.mirelight_ansel': [
    { op: 'say', if_flag: FERRY, speaker: 'OLD ANSEL', text: 'Stage is yours. Step aboard and I\'ll pole you over. Keep that lens to your eye.' },
    { op: 'say', unless_flag: LENS, speaker: 'OLD ANSEL', text: 'The Glassmere. A causeway-village under it, blue lights over it. Forty years I\'ve ferried this fen, and I don\'t cross THAT water.' },
    { op: 'say', unless_flag: LENS, speaker: 'OLD ANSEL', text: 'Half those lights are lies. Follow one and it hangs over deep water till you\'re in it. The boards are rotten where they point, sound where they don\'t.' },
    { op: 'say', if_flag: BEGUN, unless_flag: LENS, speaker: 'OLD ANSEL', text: 'The eel-wife\'s boy. Aye. I know. Don\'t think I don\'t look east every night.' },
    { op: 'say', unless_flag: LENS, speaker: 'OLD ANSEL', text: 'I\'d want a true-eye first: [[Pale Vault frost-glass]], cut [[up in the ice country]]. Through that, they say, a false light looks false.' },
    { op: 'setFlag', unless_flag: LENS, flag: ASKED },
    { op: 'say', if_flag: LENS, unless_flag: FERRY, speaker: 'OLD ANSEL', text: 'Frost-glass? Pale Vault cut — I\'d know that grind anywhere. Give it here.' },
    { op: 'face', if_flag: LENS, unless_flag: FERRY, actor: 'ansel', facing: 'right' },
    { op: 'tint', if_flag: LENS, unless_flag: FERRY, color: '#bfe6ff', alpha: 0.2, ms: 500 },
    { op: 'narrate', if_flag: LENS, unless_flag: FERRY, text: 'Ansel looks east through the lens a long while. The blue lights turn merely blue — and low on the water, old reed-lanterns glow warm.' },
    { op: 'tint', if_flag: LENS, unless_flag: FERRY, color: '#bfe6ff', alpha: 0, ms: 700 },
    { op: 'say', if_flag: LENS, unless_flag: FERRY, speaker: 'OLD ANSEL', text: 'The old causeway-reeds. Lit, where the boards are true. Well. I\'ll be.' },
    { op: 'say', if_flag: LENS, unless_flag: FERRY, speaker: 'OLD ANSEL', text: 'Right. I\'ll take you to the landing, no further. Keep the lens up: [[a LIT reed]] at a walk\'s mouth [[means sound boards]]. A dead one means swim.' },
    { op: 'sfx', if_flag: LENS, unless_flag: FERRY, key: 'world-keyitem' },
    { op: 'setFlag', if_flag: LENS, unless_flag: FERRY, flag: FERRY },
  ],
  // Walking onto the stage with the lens already in hand (playtest 2026-10): he
  // used to say "off my stage" and leave you to go back and talk to him. Now he
  // spots it, walks over, has his look and poles you straight across.
  ...anselStage(23),
  ...anselStage(24),
  'script.mirelight_ferry_ride': [
    { op: 'setFlag', flag: CROSSED },
    { op: 'letterbox', on: true },
    { op: 'narrate', text: 'Ansel holds the punt steady. You climb in. He pushes off without a word.' },
    { op: 'narrate', text: 'The reeds fall behind. The water goes black and glassy, and the blue lights drift to meet you — close enough to touch, no warmer than moonlight on a knife.' },
    { op: 'say', speaker: 'OLD ANSEL', text: 'Don\'t look at them. Look at the lens. ...There. The landing.' },
    { op: 'letterbox', on: false },
    { op: 'travel', map: 'mirelight_landing', to: { tx: 1, ty: 23 }, facing: 'right' },
    { op: 'say', speaker: 'OLD ANSEL', text: 'I\'ll wait with the punt. [[Walk off the stage, west]], for the fen.' },
  ],
  'script.mirelight_tobin_home': [
    { op: 'say', speaker: 'TOBIN', text: 'Mum says I\'m not allowed east of the reed-mere till I\'m forty. ...Did you wake the big lantern? I keep dreaming it can\'t find the boards.' },
    { op: 'say', if_flag: CAUGHT, speaker: 'TOBIN', text: 'You DID. The Glassmere went bright last night. Mum said it was the moon. It wasn\'t.' },
  ],

  // ---- the Landing ----------------------------------------------------------------------
  'script.mirelight_ansel_landing': [
    { op: 'say', speaker: 'OLD ANSEL', text: 'I\'ll keep the punt. [[Walk off the stage, west]] — home before the eels notice.' },
    { op: 'say', unless_flag: TOBIN, speaker: 'OLD ANSEL', text: 'Find the boy. And mind which boards you trust.' },
  ],
  'script.mirelight_nell': [
    { op: 'say', speaker: 'NELL', text: 'A visitor! On MY causeway! Not since the water came past the third step. Sit, sit — no, not there, that\'s the river.' },
    { op: 'say', speaker: 'NELL', text: 'You\'ll want to know about the lights. Everyone does. They weren\'t always many, dear. Once there was just the one.' },
    { op: 'say', speaker: 'NELL', text: 'The fen\'s own lamp: a kin with a lantern-glow in its chest, walking the causeway ahead of the boats at dusk. My gran swore it looked back to check she followed.' },
    { op: 'say', speaker: 'NELL', text: 'Fifteen winters back the quiet folk came, gentle, with grey lanterns. They put our lamp to sleep in the chapel, so nothing could ever hurt it.' },
    { op: 'say', speaker: 'NELL', text: 'And nothing has. It\'s only dreaming. Those blue lights are its dreams — trying to lead the boats home, and not knowing the way any more.' },
    { op: 'say', unless_flag: TOBIN, speaker: 'NELL', text: 'Tobin? He went by on the boards chasing a light. I leave a pie out every other night. The dish comes back empty, so he\'s alive, and he\'s rude.' },
    { op: 'say', if_flag: TOBIN, speaker: 'NELL', text: 'Tobin got home, I hear. Good. The causeway always let the children through.' },
  ],
  'script.mirelight_empty_hut': [
    { op: 'narrate', text: 'The hut door is roped shut. Chalked on the boards: GONE TO PEARLMOOR. KEY UNDER THE EEL. There is no eel.' },
  ],
  'script.mirelight_tobins_boat': [
    { op: 'narrate', text: 'A small fen-boat. TOBIN on the bow, by a hand that ran out of room for the N.' },
    { op: 'narrate', unless_flag: TOBIN, text: 'Oars shipped, painter tied to the first board. He didn\'t lose the boat. He went on foot, along the boards, after the lights.' },
    { op: 'narrate', if_flag: TOBIN, text: 'Ansel will tow it home in spring. Tobin says he\'ll row it. Ansel says no.' },
  ],
  'script.mire_eelcatcher': [
    { op: 'say', speaker: 'MOSS', text: 'Ansel brought you? ANSEL?! Then let\'s see if your kin are worth it.' },
    { op: 'battle', trainer: 'mire_eelcatcher' },
    { op: 'say', speaker: 'MOSS', text: 'Fair\'s fair. I set eel-lines here. The middle walk is sound every winter; the others look the same and aren\'t. Don\'t ask how I know.' },
    { op: 'setFlag', flag: 'flag:mire_eelcatcher_beaten' },
  ],
  'script.pickup_mire_landing_reeds': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glow_charge', count: 2 },
    { op: 'say', text: 'Under a reed-stook, kept dry: a tin. Found 2 GLOW CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_mire_landing_reeds' },
  ],
  'script.pickup_mire_landing_tin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'A fen-family\'s tin, left for whoever made it across. Found a BRIGHT BALM!' },
    { op: 'setFlag', flag: 'flag:picked_mire_landing_tin' },
  ],

  // ---- the Glassmere ---------------------------------------------------------------------
  'script.mirelight_dunk_landing_north': dunk('mirelight_landing', 19, 30, 'right', 'The last board isn\'t there. The blue light was hanging just past it, so near — and then it\'s hanging above you, and you\'re in black water to the neck.'),
  'script.mirelight_dunk_landing_south': dunk('mirelight_landing', 19, 38, 'right', 'The board under your foot is only reed-weed and a memory of a board. It folds. SPLASH.'),
  'script.mirelight_dunk_mere_a_north': dunk('mirelight_glassmere', 3, 28, 'up', 'Four boards, and then a fifth that is only the light\'s reflection. You step onto the reflection.'),
  'script.mirelight_dunk_mere_a_south': dunk('mirelight_glassmere', 6, 38, 'right', 'The boards end where the light begins. You learn this the wet way.'),
  'script.mirelight_dunk_mere_b_east': dunk('mirelight_glassmere', 16, 30, 'up', 'The light bobs, as if pleased you came. The board gives way, as if it isn\'t.'),
  'script.mirelight_dunk_mere_c_north': dunk('mirelight_glassmere', 13, 17, 'up', 'A dead reed stood at the mouth of this walk. You remember that now, from underneath it.'),
  'script.mirelight_dunk_mere_d_west': dunk('mirelight_glassmere', 22, 18, 'up', 'So close to the far shore. So far from the board you needed. The Glassmere takes you in, and then, quite politely, gives you back.'),
  'script.mire_lampdiver': [
    { op: 'say', speaker: 'ODO', text: 'I dive for the old village\'s lamps — brass, glass, the odd candlestick. You\'re on my best spot. Let\'s settle it.' },
    { op: 'battle', trainer: 'mire_lampdiver' },
    { op: 'say', speaker: 'ODO', text: 'Down there the street\'s still paved, kettles on hooks, like they just stepped out. [[The east current]] runs to my old cache. Walk back.' },
    { op: 'setFlag', flag: 'flag:mire_lampdiver_beaten' },
  ],
  'script.pickup_mire_pearl': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'glassmere_pearl', count: 1 },
    { op: 'say', text: 'Only the current comes here. In a diver\'s sealed jar: a pearl, a blue light turning inside. Found a GLASSMERE PEARL!' },
    { op: 'setFlag', flag: 'flag:picked_mire_pearl' },
  ],
  'script.pickup_mire_glassmere_balm': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 1 },
    { op: 'say', text: 'At the end of the true boards, a balm left for the next one across. Found a BRIGHT BALM!' },
    { op: 'setFlag', flag: 'flag:picked_mire_glassmere_balm' },
  ],

  // ---- the Drowned Chapel ------------------------------------------------------------------
  'script.mirelight_tobin': [
    { op: 'emote', actor: 'tobin', emote: 'alert' },
    { op: 'say', speaker: 'TOBIN', text: 'Don\'t — oh. You\'ve got a LAMP. A real one. I thought you were another blue one.' },
    { op: 'say', speaker: 'TOBIN', text: 'I\'m not lost. I KNOW where I am: the sunk street. I just... don\'t know where the boards back are. The lights kept moving them.' },
    { op: 'say', speaker: 'TOBIN', text: 'I got to the chapel and pried the door. Stairs, water, and a big grey lantern with something IN it. Asleep. Eyes shut, but... glowing at me.' },
    { op: 'say', speaker: 'TOBIN', text: 'So I ran. I\'ve lived on Nell\'s pies since. Don\'t tell Mum I ran.' },
    { op: 'say', speaker: 'TOBIN', text: 'Here — I was saving these to catch a light. You\'ve the lamp for it.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'narrate', text: 'Tobin gave you 2 BEACON CHARGES!' },
    { op: 'say', speaker: 'TOBIN', text: 'With your lens I can see the real reeds now. I\'ll go home by the boards. ...Mum\'s going to kill me, isn\'t she.' },
    { op: 'setFlag', flag: TOBIN },
    { op: 'narrate', text: 'Tobin sets off for the landing, stepping only where the reeds are lit. The chapel door stands pried a finger\'s width open.' },
  ],
  'script.mirelight_chapel_bell': [
    { op: 'narrate', text: 'The bell-rope hangs by the porch, green with fen-weed. This bell rang the boats home once, when the lamp walked the causeway.' },
    { op: 'sfx', key: 'world-moorbell' },
    { op: 'narrate', unless_flag: CAUGHT, text: 'One soft note goes out over the Glassmere. Every blue light turns at once toward the chapel. Then they forget, and drift.' },
    { op: 'narrate', if_flag: CAUGHT, text: 'One soft note goes out over the Glassmere. Fewer blue lights now — and the ones left hang still, as if listening.' },
  ],
  'script.mire_acolyte': [
    { op: 'say', speaker: 'BROTHER IVES', text: 'Peace, traveller. I keep the chapel\'s watch. Our first here laid the fen\'s lamp to rest, so the dark could never hurt it. It sleeps very sweetly.' },
    { op: 'say', speaker: 'BROTHER IVES', text: '...You\'ve the look of someone who\'d wake it. I\'m bound to ask you not to. Gently. Then less gently.' },
    { op: 'battle', trainer: 'mire_acolyte' },
    { op: 'say', speaker: 'BROTHER IVES', text: 'Well. I asked. What the Warden won\'t say: every winter, more blue lights, fewer boats home. Rest at [[my camp, east bank]]. The fire doesn\'t mind.' },
    { op: 'setFlag', flag: 'flag:mire_acolyte_beaten' },
  ],
  'script.mirelight_camp_rest': [
    { op: 'narrate', text: 'A small kept camp: grey blanket, kettle, lantern turned low. Chalked on the kettle: WHOEVER YOU ARE, YOU ARE WELCOME.' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'You sit by the low fire with your kin. Rested.' },
  ],
  'script.pickup_mire_street_tin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'In a sunk-street doorway, a tin someone small has been rationing. Found 2 WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_mire_street_tin' },
  ],
  'script.pickup_mire_meadow_charge': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'Under the old boat\'s hull, still sealed: a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_mire_meadow_charge' },
  ],
  'script.pickup_mire_bank_balm': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 2 },
    { op: 'say', text: 'At the west bank\'s corner, a fen-wife\'s picnic tin. Found 2 WARM BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_mire_bank_balm' },
  ],

  // ---- Lanthorne Hollow: the set-piece (07-the-three's staging) ----------------------------
  'script.mirelight_lanthorne': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'The great grey lantern stands on its dais, furred with a long, long sleep. Inside, something folded and blue is dreaming, its light slow as breathing.' },
    { op: 'narrate', text: 'You raise your lamp. The Frostglass Lens catches it — and for the first time in years, a TRUE light falls through the null-glass.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#7fd6ff', alpha: 0.24, ms: 700 },
    { op: 'narrate', text: 'The sleeper\'s eyes open. It looks at your light the way a lost thing looks at a window — and the lantern\'s door swings wide.' },
    { op: 'tint', color: '#7fd6ff', alpha: 0, ms: 900 },
    { op: 'letterbox', on: false },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    { op: 'legendaryBattle',
      name: 'lanthorne', kin: 165, level: 45,
      caughtFlag: CAUGHT,
      cooldownBattles: 12,
      cooldownRef: 'npc.lanthorne_resting',
      terrain: 'water' },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'Lanthorne settles into your lamp like a boat into a known stage — slowly, the long way round. Its light steadies, warm and patient.' },
    { op: 'musicCrossfade', key: 'mirelight', ms: 1600 },
    { op: 'starfall', wait: true },
    { op: 'narrate', text: 'Far above, a small star you never noticed burns brighter. On the Glassmere, the blue lights go out one by one, like a dream ending.' },
  ],
  'script.mirelight_lantern_empty': [
    { op: 'narrate', unless_flag: CAUGHT, text: 'The grey glass is cold. Inside, something breathes, very slowly.' },
    { op: 'narrate', if_flag: CAUGHT, text: 'The null-lantern stands open and empty. Someone — Brother Ives, perhaps — has already swept the dais.' },
  ],
};

export const MIRELIGHT_DIALOGUE: DialogueRegistry = {
  'npc.mirelight_ansel_blocked': [
    { speaker: 'OLD ANSEL', text: 'Off my stage, please. Nobody crosses the Glassmere till I\'ve a true-eye: [[Pale Vault frost-glass]]. Then we\'ll talk.' },
  ],
  'sign.mirelight_ferry': [
    { text: 'THE GLASSMERE FERRY. Ansel, ferryman. CROSSINGS SUSPENDED. (Underneath, smaller:) Until the lights tell the truth.' },
  ],
  'sign.mirelight_landing': [
    { text: 'LANTERN CAUSEWAY. Pop. 1 (NELL). Wipe your boots. Do not follow the lights.' },
  ],
  'sign.mirelight_boards': [
    { text: 'THE BOARDS. Through a true-eye: a LIT reed at a walk\'s mouth means sound boards. A DEAD reed means a bath.' },
  ],
  'sign.mirelight_glassmere': [
    { text: 'THE GLASSMERE. The old causeway runs island to island underwater. Trust the lit reeds, not the blue lights. Currents run one way.' },
  ],
  'sign.mirelight_current': [
    { text: 'CURRENT BELOW. South to the diver\'s islet, never back. Walk the boards home.' },
  ],
  'sign.mirelight_chapel': [
    { text: 'CHAPEL OF THE CAUSEWAY. Its bell rang the boats home. Way down: [[the east bank]].' },
  ],
  'sign.lanthorne_hollow': [
    { text: 'Scratched into the stair, in a careful grey hand: LET IT SLEEP. Below, in a smaller one: IT\'S LONELY.' },
  ],
  'npc.mirelight_chapel_door': [
    { text: 'The chapel door is swollen shut. Fresh pry-marks, low on the jamb — someone small tried it, not long ago.' },
  ],
  'npc.lanthorne_resting': [
    { text: 'The lantern\'s door has swung shut. Inside, the blue light has curled back into its dream. It won\'t stir for {remaining} more battles.' },
  ],
  'npc.mire_eelcatcher_after': [
    { speaker: 'MOSS', text: 'Nell says the lights were one, once. Nell says a lot. ...Nell\'s usually right.' },
  ],
  'npc.mire_lampdiver_after': [
    { speaker: 'ODO', text: 'Swim the shelf all you like — Tidecall\'s fine near the islands. Out in the black, there\'s no bottom I\'ve ever found.' },
  ],
  'npc.mire_acolyte_after': [
    { speaker: 'BROTHER IVES', text: 'If you wake it, be kind. It\'s slept a very long time, and never asked to.' },
  ],
};
