/**
 * TRAINER ART — the trainer-intro beat (2026-10).
 *
 * Every trainer battle opens with the trainer on screen before their kin (and your
 * apprentice's back on the near side), and the trainer slides back in after a win
 * for closing words. This registry says WHICH 64×64 battle sprite a trainer wears
 * (`public/assets/sprites/trainer_battle/<key>.webp`, masters + briefs in
 * `assets/trainers/battle/`) and what a CLASS trainer says when no lines are authored.
 *
 *  - Bosses and set-pieces (Lampwardens, Wren, Còr, Fenn, Georgina, the Vigilants,
 *    the Old Light's whole cast…) have a UNIQUE sprite, keyed by trainer id.
 *  - Everyone else shares a CLASS sprite picked by their `title` (a lamp-tender, a
 *    fisher, a miner…), plus a small pool of in-voice intro/outro quips. A trainer
 *    always gets the same quip (hashed by id), so a re-fight reads consistently.
 *  - Authored `intro_ref` / `defeat_ref` lines always win over a quip; uniques with
 *    no authored lines just get the banner (their own cutscene already spoke).
 */
import type { TrainerDef } from './types';

/** The player's back view on the near side of the intro. */
export const PLAYER_BACK_SPRITE = 'player_back';

interface TrainerClass {
  sprite: string;
  intro: string[];
  outro: string[];
}

export const TRAINER_CLASSES: Record<string, TrainerClass> = {
  wayfarer: {
    sprite: 'wayfarer',
    intro: ["Another Wayfarer! Let's see whose lamp burns brighter.", 'The road is long. A bout makes it shorter.'],
    outro: ['Well walked. Mind the next bend.', "Your lamp's steadier than mine. I'll trim my wick and try again."],
  },
  wick_tender: {
    sprite: 'wick_tender',
    intro: ['Every lamp on this stretch is mine to tend. Yours included.', 'Hold your light up. Let me see how it burns.'],
    outro: ['A clean, bright flame. Go on, then.', "Trimmed and outshone. I'll be back on my rounds."],
  },
  courier: {
    sprite: 'courier',
    intro: ["I've a parcel due before dusk deepens. One quick bout first!", 'Special delivery: one battle, signed for!'],
    outro: ["Delivered: one defeat, to me. I'd best run.", "You're quicker than my legs. Mind how you go."],
  },
  moss_warden: {
    sprite: 'moss_warden',
    intro: ['Mind the moss. And mind my kin, they bite back.', "Things grow slow in the dark. Let's see how you've grown."],
    outro: ["You've a green thumb for battling. Off you grow.", 'Pulled up by the roots. Lovely bout.'],
  },
  fen_folk: {
    sprite: 'fen_folk',
    intro: ["Out here you learn to keep your boots dry and your lamp lit. Let's see if you have.", 'The fen gives up its secrets slowly. Its fights? Fast!'],
    outro: ["Wet through and beaten. That's the fen for you.", 'Keep to the planks, Wayfarer. You did well.'],
  },
  net_hand: {
    sprite: 'net_hand',
    intro: ["The tide's turning. So's the fight!", "I've hauled bigger catches than you. Probably."],
    outro: ['Slipped right through my nets, you did.', 'Back to mending, then. Good bout.'],
  },
  miner: {
    sprite: 'miner',
    intro: ["Down here it's dark, and we like it lit. Show us your lamp!", "Pick's down, lamp's up. Let's dig in!"],
    outro: ["Struck a seam I didn't see coming. Well dug.", 'You hit hard. Mind your head on the way out.'],
  },
  kite_hand: {
    sprite: 'kite_hand',
    intro: ['The wind picked you out for me. Ready?', 'Hold on to your hat, this one gusts!'],
    outro: ['Blown clean away. Lovely flying.', 'The wind favours you today. Go on, up you go.'],
  },
  frost_ward: {
    sprite: 'frost_ward',
    intro: ['Cold enough to freeze a flame. Is yours tough enough?', "Stamp your feet, keep warm, and fight!"],
    outro: ['Your lamp kept me warmer than mine. Thank you.', 'Thawed out and beaten. Mind the ice.'],
  },
  troupe_player: {
    sprite: 'troupe_player',
    intro: ['Places, everyone! Tonight: a battle in one act!', 'The stage is set. You play the challenger!'],
    outro: ['A standing ovation, from me, sitting down.', 'Bravo! Curtain falls on my side.'],
  },
  sky_watcher: {
    sprite: 'sky_watcher',
    intro: ["The stars are hiding. Let's give them something to watch.", 'I chart the sky. Let me chart your moves.'],
    outro: ['A new star on my chart. It looks a lot like you.', 'The sky will brighten. You will see to it.'],
  },
  sun_keeper: {
    sprite: 'sun_keeper',
    intro: ['I keep the old sun-rites. Let me test your warmth.', 'Even in the long dusk, the sun is somewhere. Show me yours.'],
    outro: ['You carry the morning with you. Go gently.', 'Warm as noon. Thank you.'],
  },
  junior: {
    sprite: 'junior',
    intro: ["I've been practising! Watch this!", "My big sister says I'm not ready. Let's prove her wrong!"],
    outro: ["Aww! I'll practise more!", "You're SO good. Teach me sometime?"],
  },
  acolyte: {
    sprite: 'acolyte',
    intro: ['The dark is gentle, if you let it be. Let me show you.', 'Hush. Your lamp is so loud. Let it rest.'],
    outro: ['...Your light did not hurt. I thought it would.', 'Go on. I will sit with the dark a while longer.'],
  },
  runner: {
    sprite: 'runner',
    intro: ['On your marks! Battle first, race after!', 'Fast hill, faster kin. Ready, steady—'],
    outro: ['Out-run and out-fought! Brilliant.', 'Right, rematch on the slopes. Some day.'],
  },
};

const TITLE_CLASS: Record<string, string> = {
  Wayfarer: 'wayfarer',
  'Wick-tender': 'wick_tender', Lampwright: 'wick_tender', 'Reed-lamplighter': 'wick_tender',
  'Coldfog Lampman': 'wick_tender',
  'Lamp-courier': 'courier', 'Plank-courier': 'courier',
  'Moss-tender': 'moss_warden', 'Deepwood Warden': 'moss_warden', 'Bloom-warden': 'moss_warden',
  'Terrace-farmer': 'moss_warden', 'Terrace-tender': 'moss_warden',
  'Fen-wader': 'fen_folk', 'Eel-catcher': 'fen_folk', 'Lamp-diver': 'fen_folk',
  'Net-hand': 'net_hand',
  'Vigil Miner': 'miner', 'Ore-hauler': 'miner', 'Seam-miner': 'miner',
  'Kite-hand': 'kite_hand', 'Wind-ward': 'kite_hand', 'Gale-watch': 'kite_hand',
  'Crag-hand': 'kite_hand', 'Crag-watch': 'kite_hand', 'Kite-runner': 'kite_hand',
  'Frost-ward': 'frost_ward', 'Pass Survivor': 'frost_ward', 'Thaw-tender': 'frost_ward',
  'Rime-walker': 'frost_ward', 'Fog-walker': 'frost_ward',
  'Troupe Player': 'troupe_player',
  'Sky-watcher': 'sky_watcher', 'Star-watcher': 'sky_watcher', 'Junior Watcher': 'junior',
  'Sun-keeper': 'sun_keeper',
  'Hollowing Acolyte': 'acolyte',
  Runner: 'runner', "Runners' Captain": 'runner',
  'Hall Sparrer': 'wick_tender', // the Lumenary sparring partners (content/sparring.ts)
  // the Farlamp Isles (Lane C1)
  Oarsman: 'net_hand', 'Kelp-farmer': 'net_hand', 'Isle Keeper': 'wick_tender',
  Salvager: 'net_hand', 'Fog-pilot': 'net_hand', // C1 pass 2: the Shelfwater + Fogwall boats
  // Lane N1 (11 Parts A + E): the Hollowing's elders and their old lamplighter
  'Hollowing Elder': 'acolyte', 'Hollowing Lamplighter': 'wick_tender',
  // S7 the Wakeful Fair's three optional bouts
  'Latte Artist': 'junior', Cupper: 'net_hand', 'Head Barista': 'sun_keeper',
};

/** Unique battle sprites, by trainer id (bosses, set-pieces, the Old Light's cast). */
const UNIQUE_SPRITE: Record<string, string> = {
  lampwarden_tinderwick: 'brisa', lampwarden_pearlmoor: 'reyl', lampwarden_lowleaf: 'sable',
  lampwarden_cinderhead: 'otho', mira_vael: 'mira', ysolde_frost: 'ysolde', lucan_pyre: 'lucan',
  nessa_cole: 'nessa',
  wren_dimglass: 'wren', wren_pale_vault: 'wren', wren_nightreach: 'wren', wren_rematch: 'wren',
  warden_cor: 'cor', startender_fenn: 'fenn', trainer_georgina: 'georgina',
  breakwater_paul: 'paul', breakwater_paul_rematch: 'paul', breakwater_paul_rematch_post: 'paul',
  vigilant_esra: 'esra', vigilant_bramm: 'bramm', vigilant_ondra: 'ondra', vigilant_ondra_summit: 'ondra',
  vigilant_solenne: 'solenne', vigilant_solenne_summit: 'solenne', vigilant_mer: 'mer',
  vigilant_mer_summit: 'mer',
  oldlight_heckler: 'heckler', oldlight_ringmaster: 'ringmaster', oldlight_usher: 'usher',
  oldlight_juggler: 'juggler', oldlight_pie_thrower: 'pie_thrower', oldlight_critic: 'critic',
  oldlight_mirror: 'player_front', // THE MIRROR wears your own face
  oldlight_headliners: 'punchwheel', // Mr. Punchwheel presents his act
  // Lane E (walkthrough/10 Part III): Gran Tallow on her reef, by the old Tinder Light
  lowtinder_ottery: 'ottery',
  // Lane N2 (walkthrough/11 Part B): the Drownlight's Shutterkeeper
  drownlight_shutterkeeper: 'shutterkeeper',
};

function pick<T>(xs: T[], seed: string): T {
  let h = 0;
  for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0;
  return xs[h % xs.length];
}

export interface TrainerArt {
  /** Battle sprite key (texture `tb_<key>`), or undefined if the trainer has none. */
  sprite?: string;
  /** In-voice quips for a class trainer with no authored lines. */
  introQuip?: string;
  outroQuip?: string;
}

export function trainerArt(t: TrainerDef | undefined): TrainerArt {
  if (!t) return {};
  const unique = t.sprite ?? UNIQUE_SPRITE[t.id];
  if (unique) return { sprite: unique };
  const cls = t.title ? TRAINER_CLASSES[TITLE_CLASS[t.title] ?? ''] : undefined;
  if (!cls) return {};
  return { sprite: cls.sprite, introQuip: pick(cls.intro, t.id), outroQuip: pick(cls.outro, t.id + ':out') };
}

/** Texture key for a battle sprite. */
export const trainerBattleTexture = (key: string): string => `tb_${key}`;
