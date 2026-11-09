/**
 * THE WILD WAYS (2026-10, docs/world/walkthrough/09-the-wild-ways.md) — the Old Seams (D): the sealed deep workings under Cinderhead, Emberroot.
 * This area's lane OWNS this file: new scripts + dialogue only, spread into the
 * registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * Maps: cinderhead_mine (the seam-door + Otho), old_seams_i (the Shaft Benches),
 * old_seams_ii (the Rail Yard), old_seams_iii (the Scree Galleries),
 * emberroot_heart (the first star). Builders: tools/maps/build_old_seams_*.py,
 * build_emberroot_heart.py.
 *
 * Flags this file owns:
 *   flag:old_seams_open          Otho has opened the seam-door (post-Stone)
 *   flag:seams_lever_1..3        the rail yard's three levers (thrown = turnout)
 *   flag:seams_lever_tmp         transient: a lever's previous state, cleared at once
 *   flag:emberroot_heart_seen    the awe beat at the bottom has played
 *   flag:emberroot_caught        set by the legendaryBattle op on a catch
 * Reads the DERIVED flag:lamplight_starlight (six Gleams) on the heart's ladder.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const OPEN = 'flag:old_seams_open';
const CAUGHT = 'flag:emberroot_caught';
const TMP = 'flag:seams_lever_tmp';

/** A yard lever: flips flag:seams_lever_<n> (via a transient copy of its old
 *  state, so the two setFlag guards can't both fire) and says what moved. */
function lever(n: number, points: string): CutsceneStep[] {
  const F = `flag:seams_lever_${n}`;
  return [
    { op: 'setFlag', flag: TMP, if_flag: F },
    { op: 'setFlag', flag: F, unless_flag: TMP },
    { op: 'setFlag', flag: F, value: false, if_flag: TMP },
    { op: 'sfx', key: 'world-door-close' },
    { op: 'shake', ms: 220, intensity: 0.002 },
    { op: 'narrate', if_flag: F, text: `You haul LEVER ${n} over. ${points} clanks across: [[RED, the turnout]].` },
    { op: 'narrate', unless_flag: F, text: `You haul LEVER ${n} back. ${points} clanks home: [[WHITE, the straight]].` },
    { op: 'setFlag', flag: TMP, value: false },
  ];
}

function seamMiner(id: string, name: string, before: string, after: string): CutsceneStep[] {
  return [
    { op: 'say', speaker: name, text: before },
    { op: 'battle', trainer: id },
    { op: 'say', speaker: name, text: after },
    { op: 'setFlag', flag: `flag:${id}_beaten` },
  ];
}

function find(flag: string, gives: CutsceneStep[], text: string): CutsceneStep[] {
  return [{ op: 'sfx', key: 'world-pickup' }, ...gives, { op: 'say', text }, { op: 'setFlag', flag }];
}

export const OLDSEAMS_SCRIPTS: ScriptRegistry = {
  // ---- the seam-door (Cinderhead Mine) -----------------------------------------
  // The hall's post-Gleam Otho: his usual word, then the seam — and off he goes
  // to wait at its door (one Otho at a time; build_cinderhead_interiors.py).
  'script.otho_after_seams': [
    { op: 'dialogue', ref: 'npc.otho_after' },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'grave', text: 'One more thing. A door in [[the north workings]] has been shut since my grandmother\'s day. I\'d show it to a steady lamp. [[Find me there]].' },
    { op: 'setFlag', flag: 'flag:old_seams_told' },
    { op: 'narrate', text: 'Otho takes a hand-lamp from its hook and heads off toward the north workings.' },
  ],
  'script.old_seams_otho': [
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'neutral', text: 'Found my door, have you. Most nights since your Gleam I\'ve stood here.' },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'grave', text: 'My grandmother\'s crew sealed this seam seventy winters back. "The seam we don\'t work," says the ledger. No reason. Foremen never give one.' },
    { op: 'say', if_flag: 'flag:q_east_ledger_done', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'neutral', text: 'You carried that ledger up. That last page, too faded to read? This is its seam.' },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'grave', text: 'The old hands say, quiet: the coal\'s warm because something down there breathes on it. Older than the mine. Older than lamps.' },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'warm', text: 'You carried a lit lamp through my dark. I\'ll trust you with this.' },
    { op: 'sfx', key: 'world-door-open' },
    { op: 'shake', ms: 500, intensity: 0.004 },
    { op: 'narrate', text: 'Otho shoulders the iron bar. Seventy winters of rust give, and warm air breathes out of the dark — coal, and faintly, summer.' },
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'OTHO GRIST', portrait: 'otho', expr: 'neutral', text: '[[Mind the shafts]]. Past the third gallery, lamps go small. If yours won\'t hold, [[come back when it will]].' },
  ],

  // ---- the rail yard's levers ----------------------------------------------------
  'script.seams_lever_1': lever(1, 'the first points'),
  'script.seams_lever_2': lever(2, 'the second points'),
  'script.seams_lever_3': lever(3, 'the third points, far across the yard,'),

  // ---- the foremen's camp (old_seams_iii) — the descent's rest point -------------
  'script.old_seams_camp_rest': [
    { op: 'narrate', text: 'The foremen\'s camp: barrels, rusted picks, a brazier unfed seventy winters. Still warm.' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'Your kin doze against the barrels, warm through. Rested.' },
  ],

  // ---- the seam-miners ---------------------------------------------------------
  'script.seams_miner_kester': seamMiner('seams_miner_kester', 'KESTER',
    'Otho let a few old hands down. My grandad sealed this very bench — I owed it a visit. And you owe me a bout.',
    'Fair\'s fair. Mind the boards, mind. Grandad swore the shafts go down forever. Grandad swore a lot of things.'),
  'script.seams_miner_wenna': seamMiner('seams_miner_wenna', 'WENNA',
    'You found the siding! Most folk ride straight past it and never know. Fancy a bout while you\'re here?',
    '[[Lever three]] lives [[out here on the siding]], not on the board. Foremen liked their little jokes.'),
  'script.seams_miner_tam': seamMiner('seams_miner_tam', 'TAM',
    'The east stage — where they sorted warm coal from cold. Only there never was any cold. Kin out!',
    'Riding for the far platform? You\'ll want [[the third points thrown]] — and that lever\'s not on the board.'),
  'script.seams_miner_penhal': seamMiner('seams_miner_penhal', 'PENHAL',
    'Deepest I\'ve ever been, and the warmest. You can take your coat off down here. Let\'s see your kin sweat!',
    'The foremen camped by the barrels. Their brazier\'s still going — rest there if the deep wears you thin.'),
  'script.seams_miner_jory': seamMiner('seams_miner_jory', 'JORY',
    'Hear that? That hush, like a held breath? Listen long enough and you\'ll hear it let go. ...Battle first, though.',
    'The last ladder\'s down in [[the root gallery]]. My lamp went small as a candle at the top. Yours might do better.'),

  // ---- caches ------------------------------------------------------------------
  'script.pickup_seams_islet': find('flag:picked_seams_islet', [{ op: 'giveItem', item: 'beacon_charge', count: 1 }],
    'On a pillar of rock above the dark, where only a plank reaches: a foreman\'s tin. Found a BEACON CHARGE!'),
  'script.pickup_seams_bench_balm': find('flag:picked_seams_bench_balm', [{ op: 'giveItem', item: 'warm_balm', count: 2 }],
    'A miner\'s kit-bag, hung on a peg and forgotten. Found 2 WARM BALMS!'),
  'script.pickup_seams_bench_tin': find('flag:picked_seams_bench_tin', [{ op: 'giveItem', item: 'glow_charge', count: 1 }],
    'A snuff-tin tucked behind a prop in the bench\'s far corner. Found a GLOW CHARGE!'),
  'script.pickup_seams_siding': find('flag:picked_seams_siding', [{ op: 'giveItem', item: 'starglass_shard', count: 1 }],
    'In the siding\'s buffer-box, in oilcloth: a STARGLASS SHARD — a warm fall from before the Dusk. The crew\'s luckiest find, never sold.'),
  'script.pickup_seams_stage': find('flag:picked_seams_stage', [{ op: 'giveItem', item: 'glow_charge', count: 2 }],
    'A sorter\'s tin on the east stage. Found 2 GLOW CHARGES!'),
  'script.pickup_seams_scree_ledge': find('flag:picked_seams_scree_ledge', [{ op: 'giveItem', item: 'lumen_drop', count: 1 }],
    'Only a scree-rider stops here. Wedged in a crack: a LUMEN DROP!'),
  'script.pickup_seams_root_charge': find('flag:picked_seams_root_charge', [{ op: 'giveItem', item: 'beacon_charge', count: 1 }],
    'A foreman\'s strongbox, its lock rusted to nothing. Found a BEACON CHARGE!'),
  'script.pickup_seams_ledger_page': [
    { op: 'sfx', key: 'world-chart' },
    { op: 'say', text: 'Under a stone where the chalk ends: the Foreman\'s Ledger\'s LAST PAGE.' },
    { op: 'say', text: '"The seam we don\'t work. There is a star at the bottom of Cinderhead, and it is not cold. The coal is its breath and the mountain is its house and we are its lodgers. Close the door gently behind you."' },
    { op: 'setFlag', flag: 'flag:picked_seams_ledger_page' },
  ],

  // ---- the first star (emberroot_heart) ------------------------------------------
  'script.emberroot_heart_enter': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 1000 },
    { op: 'narrate', text: 'The last ladder ends. The dark ends with it.' },
    { op: 'narrate', text: 'The chamber is warm as a kitchen at midnight. In root-rock at its middle, something glows — not like a lamp. Like a hearth that never once went out.' },
    { op: 'narrate', text: 'It is a star, come down so long ago no one saw it fall. Every coal seam in Cinderhead runs out of this room like roots from a tree.' },
    { op: 'letterbox', on: false },
  ],
  'script.emberroot_wake': [
    { op: 'letterbox', on: true },
    { op: 'silence', ms: 900 },
    { op: 'narrate', text: 'At the star\'s foot, what you took for a ridge of coal draws one long, slow breath — and the whole mountain breathes with it.' },
    { op: 'narrate', text: 'EMBERROOT opens one eye, banked-ember orange, and regards your lamp as if it remembers lamps.' },
    { op: 'letterbox', on: false },
    { op: 'musicSting', key: 'sting-hour' },
    { op: 'music', key: 'battle-hours' },
    {
      op: 'legendaryBattle',
      name: 'emberroot',
      kin: 166,
      level: 46,
      caughtFlag: CAUGHT,
      cooldownBattles: 12,
      cooldownRef: 'npc.emberroot_resting',
      terrain: 'cave',
    },
    { op: 'silence', ms: 1200 },
    { op: 'narrate', text: 'Emberroot settles into your lamp like a coal into a grate, with a sigh. Behind you the first star breathes on, a little lighter. A cinder is never dead.' },
    { op: 'musicCrossfade', key: 'old-seams', ms: 1600 },
  ],
  'script.emberroot_star': [
    { op: 'narrate', unless_flag: CAUGHT, text: 'The star is warm from a pace away. Its cracks pulse, slow, slow, with the breathing at its foot.' },
    { op: 'narrate', if_flag: CAUGHT, text: 'The first star breathes on alone, warm and steady. It never needed watching — only someone to come all the way down and see it.' },
  ],
};

export const OLDSEAMS_DIALOGUE: DialogueRegistry = {
  'npc.old_seams_sealed': [
    { text: 'A seam-door, iron-banded. Chalked across it: THE SEAM WE DON\'T WORK.' },
    { text: 'Barred this side. Only [[whoever keeps this mine\'s light]] would lift it.' },
  ],
  'npc.emberroot_dark': [
    { text: 'The last ladder drops into a dark so thick your lamplight stops a hand\'s breadth from the glass. Below, something breathes: slow, warm, enormous.' },
    { text: 'Your vesperlamp can\'t hold this dark. Not yet. A lamp that has [[seen more of the sky relit]] might.' },
  ],
  'npc.emberroot_resting': [
    { text: 'Emberroot has curled round the star\'s foot, breathing slow and deep. It won\'t wake until you\'ve won {remaining} more battles up in the world.' },
  ],
  'sign.old_seams_i': [
    { text: 'THE OLD SEAMS. [[Walk the boards]], not the dark. The shafts have no bottom.' },
  ],
  'sign.old_seams_yard': [
    { text: 'THE YARD. On the stands: [[WHITE runs straight]], [[RED takes the turnout]].' },
    { text: 'Levers 1 and 2 here. [[Lever 3: south-west siding]]. Every line runs home.' },
  ],
  'sign.old_seams_root': [
    { text: 'No sign — only old chalk on the last ladder: LAMP GONE SMALL? GO BACK UP. Under it, newer: IT\'S ONLY BREATHING.' },
  ],
  'npc.seams_miner_kester_after': [{ speaker: 'KESTER', text: 'Every bench a little warmer than the one above. Makes you think.' }],
  'npc.seams_miner_wenna_after': [{ speaker: 'WENNA', text: 'Throw three, ride home, ride out again. That\'s the trick of the yard.' }],
  'npc.seams_miner_tam_after': [{ speaker: 'TAM', text: 'Not one cold lump in seventy years of tally-books. Not one.' }],
  'npc.seams_miner_penhal_after': [{ speaker: 'PENHAL', text: 'If my coat comes off any further I\'ll be down to my vest.' }],
  'npc.seams_miner_jory_after': [{ speaker: 'JORY', text: '...There. Did you hear it let go?' }],
};
