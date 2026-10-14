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
  name: string;
  gleam: string;
  party: [number, number][]; // [species_id, level], ace last
  voice: [string, string, string]; // greeting, after a win, while resting
}

const HALLS: Hall[] = [
  {
    hall: 'tinderwick', name: 'ROSIE WICKERS', gleam: 'gleam:ember',
    party: [[16, 8], [10, 8], [18, 9]],
    voice: [
      'Brisa says I need the practice. Spar with me? I\'ll pay out of my own wick-tin, fair and square.',
      'Ow. Good bout! That\'s the tin\'s worth. Brisa will say I dropped my guard. I did drop my guard.',
      'Still getting my breath back. Win {remaining} more fights out there and I\'ll be ready again.',
    ],
  },
  {
    hall: 'pearlmoor', name: 'TOMAS SPRAT', gleam: 'gleam:tide',
    party: [[26, 13], [27, 14], [24, 15]],
    voice: [
      'Reyl has me sparring every comer who\'s earned the Tide. One bout? The hall pays the winner.',
      'Washed out! Here, the hall\'s purse is yours. Same again when the tide comes back round?',
      'The tide\'s out on me for now. {remaining} more wins out there, then come and splash me again.',
    ],
  },
  {
    hall: 'lowleaf', name: 'HAZEL ALDER', gleam: 'gleam:verdant',
    party: [[56, 19], [59, 20], [66, 21]],
    voice: [
      'Sable likes the hall to keep growing. A friendly bout? There are wicks in it for whoever wins.',
      'Well grown. Take the purse. I\'ll go and sit in some moss and think about what I did.',
      'My kin are still resting in the moss. {remaining} more wins elsewhere and we\'ll be green again.',
    ],
  },
  {
    hall: 'cinderhead', name: 'COBB COLLIER', gleam: 'gleam:stone',
    party: [[48, 25], [46, 26], [55, 27]],
    voice: [
      'Otho says a wall that\'s never hit forgets it\'s a wall. Hit mine? The hall pays a fair rate.',
      'Cracked us. Fair\'s fair: here\'s your rate. Mind the rubble on the way out.',
      'Still shoring up. {remaining} more wins down the seams, then we\'ll stand for you again.',
    ],
  },
  {
    hall: 'galehigh', name: 'KESTREL TOWE', gleam: 'gleam:storm',
    party: [[98, 31], [89, 32], [90, 33]],
    voice: [
      'Mira wants her kites tested in any weather. You\'re weather. Spar? Purse to the winner.',
      'Blown clean off the terrace! The purse is yours. Come back when the wind turns.',
      'The wind\'s gone out of us. {remaining} more wins out there and we\'ll be flying again.',
    ],
  },
  {
    hall: 'pale_vault', name: 'INGA SNELL', gleam: 'gleam:frost',
    party: [[72, 37], [84, 38], [87, 39]],
    voice: [
      'Ysolde says the cold is patient. I am not. Spar with me? The hall pays in wicks.',
      'Thawed. Take the purse, and the hall\'s respect, which is colder but lasts longer.',
      'We\'re still thawing out. {remaining} more wins in the snow and we\'ll be sharp again.',
    ],
  },
  {
    hall: 'sunken_solarium', name: 'LIO BRASS', gleam: 'gleam:solar',
    party: [[117, 43], [104, 44], [123, 45]],
    voice: [
      'Lucan says every understudy needs an audience. Be mine? There\'s a purse for the winner.',
      'Curtain! You take the purse and the bow. I\'ll practise my falling over.',
      'Still in the wings. {remaining} more wins out there and I\'ll be back under the lights.',
    ],
  },
  {
    hall: 'nightreach', name: 'MAB HOLLOWAY', gleam: 'gleam:lunar',
    party: [[106, 49], [112, 50], [107, 51]],
    voice: [
      'Nessa keeps me sharp on anyone who reaches the dome. Spar under the stars? The purse is good.',
      'Eclipsed! The purse is yours. The stars saw it, so it definitely happened.',
      'My kin are still star-gazing. {remaining} more wins and they\'ll come down to fight.',
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
      title: 'Hall Sparrer',
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
