/**
 * The Lumenary sparring partners (2026-10 economy review, 10-economy §2).
 *
 * Wild battles pay nothing and almost every trainer fights once, so a player who
 * kept losing had no honest way to earn their wicks back. Each Lumenary now keeps
 * a hall apprentice who spars, once that hall's Gleam is relit: a team just under
 * the warden's, a KEEPER-class purse (20w × ace) every win, then EVERY hall's
 * sparrer rests (one shared rest) for SPAR_COOLDOWN won battles elsewhere (the `spar` op; the battle-counted cooldown
 * clock the legendaries already use). Fair, never broken: one bout per four wins,
 * paying a little under a warden's tier. Mirrored in progression.mjs BUILT_PAYOUTS.
 *
 * Placements: tools/maps/hand_placed_data.py (`_SPAR_POSTS`).
 */
import type { DialogueRegistry, ScriptRegistry, TrainerDef } from './types';

/** Won battles elsewhere before a hall apprentice will spar again. */
export const SPAR_COOLDOWN = 3;

interface Hall {
  hall: string; // the Lumenary interior map id (without _lumenary)
  title: string; // the hall's own trainer class (its battle sprite, TITLE_CLASS)
  name: string;
  gleam: string;
  party: [number, number][]; // [species_id, level], ace last
  voice: [string, string, string]; // greeting, after a win, while resting
}

const HALLS: Hall[] = [
  {
    hall: 'tinderwick', title: 'Wick-tender', name: 'ROSIE WICKERS', gleam: 'gleam:ember',
    party: [[16, 8], [10, 8], [18, 9]],
    voice: [
      'Brisa says I need the practice. Spar with me? I\'ll pay out of my own wick-tin, fair and square.',
      'Ow. Good bout! That\'s the tin\'s worth. Brisa will say I dropped my guard. I did drop my guard.',
      'The halls share one practice bell, and it\'s been rung. Win a few more out there ({remaining} to go) and I\'ll be ready.',
    ],
  },
  {
    hall: 'pearlmoor', title: 'Net-hand', name: 'TOMAS SPRAT', gleam: 'gleam:tide',
    party: [[26, 13], [27, 14], [24, 15]],
    voice: [
      'Reyl has me sparring every comer who\'s earned the Tide. One bout? The hall pays the winner.',
      'Washed out! Here, the hall\'s purse is yours. Same again when the tide comes back round?',
      'The tide\'s out on the practice floor for now. Win a few more out there ({remaining} to go), then come and splash me.',
    ],
  },
  {
    hall: 'lowleaf', title: 'Moss-tender', name: 'HAZEL ALDER', gleam: 'gleam:verdant',
    party: [[56, 19], [59, 20], [66, 21]],
    voice: [
      'Sable likes the hall to keep growing. A friendly bout? There are wicks in it for whoever wins.',
      'Well grown. Take the purse. I\'ll go and sit in some moss and think about what I did.',
      'The practice bell\'s resting, and so are my kin. Win a few more elsewhere ({remaining} to go).',
    ],
  },
  {
    hall: 'cinderhead', title: 'Seam-miner', name: 'COBB COLLIER', gleam: 'gleam:stone',
    party: [[48, 25], [46, 26], [55, 27]],
    voice: [
      'Otho says a wall that\'s never hit forgets it\'s a wall. Hit mine? The hall pays a fair rate.',
      'Cracked us. Fair\'s fair: here\'s your rate. Mind the rubble on the way out.',
      'The halls\' practice bell is resting. Win a few more down the seams ({remaining} to go), then we\'ll stand for you.',
    ],
  },
  {
    hall: 'galehigh', title: 'Kite-hand', name: 'KESTREL TOWE', gleam: 'gleam:storm',
    party: [[98, 31], [89, 32], [90, 33]],
    voice: [
      'Mira wants her kites tested in any weather. You\'re weather. Spar? Purse to the winner.',
      'Blown clean off the terrace! The purse is yours. Come back when the wind turns.',
      'The practice bell\'s quiet for now. Win a few more out there ({remaining} to go) and we\'ll fly for you.',
    ],
  },
  {
    hall: 'pale_vault', title: 'Frost-ward', name: 'INGA SNELL', gleam: 'gleam:frost',
    party: [[72, 37], [84, 38], [87, 39]],
    voice: [
      'Ysolde says the cold is patient. I am not. Spar with me? The hall pays in wicks.',
      'Thawed. Take the purse, and the hall\'s respect, which is colder but lasts longer.',
      'The practice bell is resting. Win a few more in the snow ({remaining} to go) and we\'ll be sharp for you.',
    ],
  },
  {
    hall: 'sunken_solarium', title: 'Sun-keeper', name: 'LIO BRASS', gleam: 'gleam:solar',
    party: [[117, 43], [104, 44], [123, 45]],
    voice: [
      'Lucan says every understudy needs an audience. Be mine? There\'s a purse for the winner.',
      'Curtain! You take the purse and the bow. I\'ll practise my falling over.',
      'The practice bell\'s resting, so I\'m in the wings. Win a few more out there ({remaining} to go).',
    ],
  },
  {
    hall: 'nightreach', title: 'Star-watcher', name: 'MAB HOLLOWAY', gleam: 'gleam:lunar',
    party: [[106, 49], [112, 50], [107, 51]],
    voice: [
      'Nessa keeps me sharp on anyone who reaches the dome. Spar under the stars? The purse is good.',
      'Eclipsed! The purse is yours. The stars saw it, so it definitely happened.',
      'The practice bell is resting; my kin are star-gazing. Win a few more ({remaining} to go).',
    ],
  },
];

const PAYOUT_RATE_KEEPER = 20;

export const SPAR_TRAINERS: Record<string, TrainerDef> = Object.fromEntries(
  HALLS.map((h) => {
    const ace = h.party[h.party.length - 1][1];
    const def: TrainerDef = {
      id: `spar_${h.hall}`,
      name: h.name,
      title: h.title,
      party: h.party.map(([species_id, level]) => ({ species_id, level })),
      payout: PAYOUT_RATE_KEEPER * ace, // keeper 20 × ace, every win (repeatable)
    };
    return [def.id, def];
  }),
);

export const SPARRING_SCRIPTS: ScriptRegistry = Object.fromEntries(
  HALLS.map((h) => [
    `script.spar_${h.hall}`,
    [
      { op: 'say', speaker: h.name, text: h.voice[0] },
      { op: 'spar', trainer: `spar_${h.hall}`, cooldown: SPAR_COOLDOWN, restingRef: `npc.spar_${h.hall}_resting` },
      { op: 'say', speaker: h.name, text: h.voice[1] },
    ],
  ]),
);

export const SPARRING_DIALOGUE: DialogueRegistry = Object.fromEntries(
  HALLS.map((h) => [`npc.spar_${h.hall}_resting`, [{ speaker: h.name, text: h.voice[2] }]]),
);

/** For the placements + docs: which Gleam wakes each hall's sparrer. */
export const SPAR_HALLS = HALLS.map((h) => ({ map: `${h.hall}_lumenary`, gleam: h.gleam, id: `spar_${h.hall}` }));
