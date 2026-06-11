/**
 * Trainer registry — authored opponents (rivals, Lampwardens). Adding a trainer
 * is a data edit here, never engine code. Each entry maps to a `BattleRequest`
 * of kind 'trainer' by id (see BattleScene). Intro/defeat lines are supplied as
 * dialogue here so a trainer fight is self-contained (the BattleScene reads
 * `getTrainer(id)` and `getTrainerLines(ref)` rather than the world DialogueRegistry).
 *
 * First Lumenary: Brisa Tallow, the Lampwarden of Tinderwick (Ember). Beating
 * her relights the first constellation — the player earns the Ember Gleam and the
 * 'crown_south' progression flag.
 */
import type { DialogueLine, TrainerDef, TrainerRegistry } from './types';

export const TRAINERS: TrainerRegistry = {
  lampwarden_tinderwick: {
    id: 'lampwarden_tinderwick',
    name: 'BRISA TALLOW',
    title: 'Lampwarden',
    party: [
      { species_id: 10, level: 7 }, // Tallowpup — Ember
      { species_id: 18, level: 10 }, // Hearthkit — Ember (ace ~10 per walkthrough/01-south)
    ],
    intro_ref: 'trainer.lampwarden_tinderwick.intro',
    defeat_ref: 'trainer.lampwarden_tinderwick.defeat',
    reward_flags: ['gleam:ember', 'crown_south'],
    payout: 600, // Lampwarden 60 × ace 10
    music: 'battle-emberfall',
    ai: 'smart', // Lampwardens play the matchup, not just the biggest number
  },

  // The Beacon ascent (Tinderwick): Brisa's wick-tenders hold the stair floors —
  // SIGHT trainers pitched between the coast road (~6) and Brisa's ace 10, so the
  // climb itself is the on-ramp to the bond-test.
  beacon_keeper_a: {
    id: 'beacon_keeper_a',
    name: 'TANSY',
    title: 'Wick-tender',
    party: [
      { species_id: 16, level: 7 }, // Wickmoth — Ember
    ],
    payout: 140, // keeper 20 × ace 7
    music: 'battle-emberfall',
  },
  beacon_keeper_b: {
    id: 'beacon_keeper_b',
    name: 'COLE',
    title: 'Wick-tender',
    party: [
      { species_id: 10, level: 7 }, // Tallowpup — Ember
      { species_id: 16, level: 8 }, // Wickmoth — Ember
    ],
    payout: 160, // keeper 20 × ace 8
    music: 'battle-emberfall',
  },

  // A2 — Wren's first FRIENDLY battle on Dimglass Coast I (walkthrough/01-south §2):
  // teaches trainer battles in a low-stakes, cosy frame, pitched ~2 levels under the
  // player (~7 at the second grass beat). No reward flags — the route trigger tracks it.
  wren_dimglass: {
    id: 'wren_dimglass',
    name: 'WREN',
    title: 'Wayfarer',
    party: [
      { species_id: 8, level: 5 }, // Glimflit — Light
      { species_id: 26, level: 6 }, // Brinelet — Tide
    ],
    intro_ref: 'trainer.wren_dimglass.intro',
    defeat_ref: 'trainer.wren_dimglass.defeat',
    payout: 144, // rival 24 × ace 6
    music: 'battle-emberfall',
  },

  // Dimglass Coast II route trainers — the XP bridge between the Ember Gleam (~10)
  // and Pearlmoor (rec. 12): two travelling Wayfarers on the tidal flats.
  flats_wayfarer_a: {
    id: 'flats_wayfarer_a',
    name: 'MORROW',
    title: 'Wayfarer',
    party: [
      { species_id: 26, level: 9 }, // Brinelet — Tide
      { species_id: 31, level: 9 }, // Lumpin — Tide/Light
    ],
    intro_ref: 'trainer.flats_wayfarer_a.intro',
    defeat_ref: 'trainer.flats_wayfarer_a.defeat',
    payout: 144, // route 16 × ace 9
    music: 'battle-emberfall',
  },
  flats_wayfarer_b: {
    id: 'flats_wayfarer_b',
    name: 'ELSPETH',
    title: 'Lamp-courier',
    party: [
      { species_id: 27, level: 10 }, // Brineroll — Tide
      { species_id: 31, level: 11 }, // Lumpin — Tide/Light
    ],
    intro_ref: 'trainer.flats_wayfarer_b.intro',
    defeat_ref: 'trainer.flats_wayfarer_b.defeat',
    payout: 176, // route 16 × ace 11
    music: 'battle-emberfall',
  },

  // Glowmoss Deep (East) — the first cave dungeon's SIGHT keepers (dungeon
  // keeper class, 10-economy §4), pitched to the walkthrough's ~20 rec. band:
  // the on-ramp between Sable Quill's ace 22 and the Cinderhead galleries.
  glowmoss_keeper_a: {
    id: 'glowmoss_keeper_a',
    name: 'DELL',
    title: 'Moss-tender',
    party: [
      { species_id: 56, level: 19 }, // Sporeling — Verdant
      { species_id: 57, level: 20 }, // Sporemid — Verdant (ace)
    ],
    payout: 400, // keeper 20 × ace 20
    music: 'battle-emberfall',
  },
  glowmoss_keeper_b: {
    id: 'glowmoss_keeper_b',
    name: 'MIRREL',
    title: 'Deepwood Warden',
    party: [
      { species_id: 65, level: 20 }, // Glowsip — Verdant/Light
      { species_id: 67, level: 21 }, // Fennlight — Verdant/Light (ace)
    ],
    payout: 420, // keeper 20 × ace 21
    music: 'battle-emberfall',
  },

  // Saltreach Fen I route trainers — the 16→18 on-ramp between Pearlmoor and
  // the Lowleaf cluster (route class, 10-economy §4).
  fen_wader_a: {
    id: 'fen_wader_a',
    name: 'MARIGOLD',
    title: 'Fen-wader',
    party: [
      { species_id: 59, level: 16 }, // Dewling — Verdant/Tide
      { species_id: 27, level: 17 }, // Brineroll — Tide (ace)
    ],
    payout: 272, // route 16 × ace 17
    music: 'battle-emberfall',
  },
  fen_courier_b: {
    id: 'fen_courier_b',
    name: 'OSPREY',
    title: 'Plank-courier',
    party: [
      { species_id: 31, level: 17 }, // Lumpin — Tide/Light
      { species_id: 60, level: 18 }, // Poolfrond — Verdant/Tide (ace)
    ],
    payout: 288, // route 16 × ace 18
    music: 'battle-emberfall',
  },

  // Saltreach Fen II — the deep channels' one route trainer: the reed-line
  // lamplighter who keeps the lantern-reeds (the 17→18 top of the fen ramp).
  reed_lamplighter: {
    id: 'reed_lamplighter',
    name: 'TARN',
    title: 'Reed-lamplighter',
    party: [
      { species_id: 31, level: 17 }, // Lumpin — Tide/Light
      { species_id: 59, level: 18 }, // Dewling — Verdant/Tide (ace)
    ],
    payout: 288, // route 16 × ace 18
    music: 'battle-emberfall',
  },

  // Lowleaf Hollow — the forest-fringe lane's two bloom-warden SIGHT trainers
  // (keeper class, 10-economy §4): the 19–21 on-ramp to Sable's ace 22, posted
  // on the fen-wood lane so the Tended Bed errand walks through them.
  bloom_warden_a: {
    id: 'bloom_warden_a',
    name: 'IVY',
    title: 'Bloom-warden',
    party: [
      { species_id: 56, level: 19 }, // Sporeling — Verdant
      { species_id: 65, level: 20 }, // Glowsip — Verdant/Light (ace)
    ],
    payout: 400, // keeper 20 × ace 20
    music: 'battle-emberfall',
  },
  bloom_warden_b: {
    id: 'bloom_warden_b',
    name: 'FERN',
    title: 'Bloom-warden',
    party: [
      { species_id: 38, level: 20 }, // Mossglow — Light/Verdant
      { species_id: 67, level: 21 }, // Fennlight — Verdant/Light (ace)
    ],
    payout: 420, // keeper 20 × ace 21
    music: 'battle-emberfall',
  },

  // E2 "Spores for the Stall" — the cross Sporeling squatting on the third
  // spore cache in Glowmoss Deep. A wild heart in a trainer's frame (the
  // scripted-battle pattern); it pays no wicks — it is not a person.
  spore_squatter: {
    id: 'spore_squatter',
    name: 'CROSS SPORELING',
    party: [
      { species_id: 56, level: 21 }, // Sporeling — Verdant, cross as a wet cat
    ],
    music: 'battle-emberfall',
  },

  // Pearlmoor breakwater — the Causeway Bell loop's two net-hand SIGHT trainers
  // (route class, 10-economy §4): the 12→14 on-ramp between arrival (~12) and
  // Reyl's ace 16, posted so the causeway crossing is mandatory.
  net_hand_a: {
    id: 'net_hand_a',
    name: 'MAREN',
    title: 'Net-hand',
    party: [
      { species_id: 26, level: 12 }, // Brinelet — Tide
      { species_id: 31, level: 12 }, // Lumpin — Tide/Light (ace)
    ],
    intro_ref: 'trainer.net_hand_a.intro',
    defeat_ref: 'trainer.net_hand_a.defeat',
    payout: 192, // route 16 × ace 12
    music: 'battle-emberfall',
  },
  net_hand_b: {
    id: 'net_hand_b',
    name: 'COB',
    title: 'Net-hand',
    party: [
      { species_id: 31, level: 13 }, // Lumpin — Tide/Light
      { species_id: 27, level: 14 }, // Brineroll — Tide (ace)
    ],
    intro_ref: 'trainer.net_hand_b.intro',
    defeat_ref: 'trainer.net_hand_b.defeat',
    payout: 224, // route 16 × ace 14
    music: 'battle-emberfall',
  },

  // Second Lumenary: Reyl Wash, the Lampwarden of Pearlmoor Quay (Tide) — an old
  // ferryman. Beating him relights the Tide constellation: the player earns the Tide
  // Gleam AND the Tidecall Lantern Gift (granted via reward_abilities). 'crown_south'
  // is set once both Ember + Tide are held, so it's listed here too (the FlagStore
  // ignores a re-set, and a player can reach Pearlmoor before clearing Tinderwick).
  lampwarden_pearlmoor: {
    id: 'lampwarden_pearlmoor',
    name: 'REYL WASH',
    title: 'Lampwarden',
    party: [
      { species_id: 26, level: 12 }, // Brinelet — Tide
      { species_id: 31, level: 13 }, // Lumpin — Tide/Light
      { species_id: 27, level: 14 }, // Brineroll — Tide
      { species_id: 24, level: 16 }, // Shimmral — Tide/Light (ace)
    ],
    intro_ref: 'trainer.lampwarden_pearlmoor.intro',
    defeat_ref: 'trainer.lampwarden_pearlmoor.defeat',
    reward_flags: ['gleam:tide', 'crown_south'],
    reward_abilities: ['tidecall'],
    payout: 960, // Lampwarden 60 × ace 16
    music: 'battle-emberfall',
    ai: 'smart', // Lampwardens play the matchup, not just the biggest number
  },

  // Third Lumenary: Sable Quill, the Lampwarden of Lowleaf Hollow (Verdant) —
  // a shy botanist whose glowmoss vouches where she won't speak. Beating her
  // relights the Verdant constellation AND grants Glimmerstep. NOTE: she does
  // NOT carry 'crown_east' — the quadrant crown rides the warden reward_flags
  // pattern (South's worked example), and East is strictly linear, so the
  // crown lands on Otho Grist (the SECOND East Gleam) when Cinderhead builds.
  lampwarden_lowleaf: {
    id: 'lampwarden_lowleaf',
    name: 'SABLE QUILL',
    title: 'Lampwarden',
    party: [
      { species_id: 56, level: 18 }, // Sporeling — Verdant
      { species_id: 59, level: 19 }, // Dewling — Verdant/Tide
      { species_id: 65, level: 20 }, // Glowsip — Verdant/Light
      { species_id: 66, level: 22 }, // Lumournis — Verdant/Light (ace)
    ],
    intro_ref: 'trainer.lampwarden_lowleaf.intro',
    defeat_ref: 'trainer.lampwarden_lowleaf.defeat',
    reward_flags: ['gleam:verdant'],
    reward_abilities: ['glimmerstep'],
    payout: 1320, // Lampwarden 60 × ace 22
    music: 'battle-emberfall',
    ai: 'smart', // Lampwardens play the matchup, not just the biggest number
  },

  // Fourth Lumenary: Otho Grist, Lampwarden of Cinderhead Mine (Stone) — the
  // curve's one deliberate WALL (§4: rec ~26 after the Descent Vigil vs ace 28).
  // A bulk team (roof, not rush): high def/hp Stone that punishes a glass cannon.
  // His win relights the Stone constellation AND, as East's SECOND Gleam, the
  // engine derives flag:crown_east (the warden reward_flags pattern, South's
  // worked example — Stone grants NO Lantern Gift, so no reward_abilities).
  lampwarden_cinderhead: {
    id: 'lampwarden_cinderhead',
    name: 'OTHO GRIST',
    title: 'Lampwarden',
    party: [
      { species_id: 48, level: 25 }, // Rubbol — Stone
      { species_id: 46, level: 26 }, // Voltcrag — Stone/Storm
      { species_id: 69, level: 27 }, // Riddlestone — Stone
      { species_id: 55, level: 28 }, // Ferrolith — Stone (ace, the wall)
    ],
    intro_ref: 'trainer.lampwarden_cinderhead.intro',
    defeat_ref: 'trainer.lampwarden_cinderhead.defeat',
    reward_flags: ['gleam:stone'],
    payout: 1680, // Lampwarden 60 × ace 28
    music: 'battle-emberfall',
    ai: 'smart',
  },

  // The two vigil-miner SIGHT trainers in Cinderhead Deep (keeper class) — they
  // hold the Descent Vigil's chamber leg, the §4 gap-closer made mandatory.
  gallery_miner_a: {
    id: 'gallery_miner_a',
    name: 'DRUSE',
    title: 'Vigil Miner',
    party: [
      { species_id: 47, level: 24 }, // Pebbit — Stone
      { species_id: 49, level: 25 }, // Gravelo — Stone (ace)
    ],
    intro_ref: 'trainer.gallery_miner_a.intro',
    defeat_ref: 'trainer.gallery_miner_a.defeat',
    payout: 500, // keeper 20 × ace 25
    music: 'battle-emberfall',
  },
  gallery_miner_b: {
    id: 'gallery_miner_b',
    name: 'HOBB',
    title: 'Vigil Miner',
    party: [
      { species_id: 45, level: 25 }, // Sparkrat — Stone/Storm
      { species_id: 48, level: 26 }, // Rubbol — Stone (ace)
    ],
    intro_ref: 'trainer.gallery_miner_b.intro',
    defeat_ref: 'trainer.gallery_miner_b.defeat',
    payout: 520, // keeper 20 × ace 26
    music: 'battle-emberfall',
  },
};

/** Intro/defeat dialogue for trainers, kept beside the roster they belong to. */
export const TRAINER_DIALOGUE: Record<string, DialogueLine[]> = {
  'trainer.lampwarden_tinderwick.intro': [
    { speaker: 'BRISA TALLOW', text: 'So the lamp-tender sends an apprentice. Good. The dark needs fewer cowards.' },
    { speaker: 'BRISA TALLOW', text: 'Show me your spark, Wayfarer. If it holds, the Ember Gleam is yours.' },
  ],
  'trainer.lampwarden_tinderwick.defeat': [
    { speaker: 'BRISA TALLOW', text: 'Hah! A warm flame indeed. The southern crown remembers your light.' },
    { speaker: 'BRISA TALLOW', text: 'Take the Ember Gleam. One constellation relit — only seven dusks to go.' },
  ],
  'trainer.wren_dimglass.intro': [
    { speaker: 'WREN', text: "No Lamps, no stakes — just us and our partners. Show me what your bond's worth." },
    {
      speaker: 'WREN',
      text: "And a kindness, since we're friends: ember chars the green, green drinks the tide, tide drowns the ember — round and round. Match your move to that, not your mood.",
    },
  ],
  'trainer.wren_dimglass.defeat': [
    { speaker: 'WREN', text: "Ha! Knew you'd be good. Race you to Pearlmoor — keep to the lamps, Wayfarer." },
  ],
  'trainer.flats_wayfarer_a.intro': [
    { speaker: 'MORROW', text: 'Hold there, friend. Two lamps on a dark flat had better test their wicks — that is the custom.' },
  ],
  'trainer.flats_wayfarer_a.defeat': [
    { speaker: 'MORROW', text: 'A steady flame, yours. Pearlmoor sits past the buoys — the old ferryman keeps the second Gleam.' },
  ],
  'trainer.flats_wayfarer_b.intro': [
    { speaker: 'ELSPETH', text: 'Courier post! Letters for Pearlmoor — and a standing wager for any Wayfarer who dares the flats.' },
  ],
  'trainer.flats_wayfarer_b.defeat': [
    { speaker: 'ELSPETH', text: 'The wager is yours. Mind the tide pools, and tell Reyl his letters are late because of you.' },
  ],
  'trainer.net_hand_a.intro': [
    { speaker: 'MAREN', text: 'Nobody walks the moor-boards but bell-business and net-hands — and you don\'t smell of either yet.' },
    { speaker: 'MAREN', text: 'Rope or no rope, the causeway tests every lamp it carries. Out here that\'s the LAW.' },
  ],
  'trainer.net_hand_a.defeat': [
    { speaker: 'MAREN', text: 'Steady on wet stone — that\'s rarer than you\'d think. Go on, then. Mind Cob by the far lantern; he\'s been spoiling for a bout all season.' },
  ],
  'trainer.net_hand_b.intro': [
    { speaker: 'COB', text: 'Past Maren with your boots still dry! Then you\'re the one carrying the old rope home.' },
    { speaker: 'COB', text: 'One more net between you and the bell, Wayfarer. Mine\'s the heavier.' },
  ],
  'trainer.net_hand_b.defeat': [
    { speaker: 'COB', text: 'Hah! Well hauled. The shrine\'s at the causeway\'s end — ring it LOUD, so the whole quay hears it come back.' },
  ],
  'trainer.lampwarden_pearlmoor.intro': [
    { speaker: 'REYL WASH', text: 'Apprentice, is it. I have ferried a hundred Wayfarers across this harbour. Few read the water right.' },
    { speaker: 'REYL WASH', text: 'Tides go out so they can come back, see. Show me your bond holds against mine — then I will teach you to ask the sea to part.' },
  ],
  'trainer.lampwarden_pearlmoor.defeat': [
    { speaker: 'REYL WASH', text: 'Well rowed, Wayfarer. The Tide constellation answers you — see it shiver awake over the masts.' },
    { speaker: 'REYL WASH', text: 'The Tide Gleam is yours, and with it the Tidecall. Step to the shallows now; the moon-water will part where it would not before.' },
  ],
  'trainer.lampwarden_lowleaf.intro': [
    { speaker: 'SABLE QUILL', text: 'I\'m better at this part than the talking part. My moss thinks so too.' },
    { speaker: 'SABLE QUILL', text: 'Everything green in this hall keeps a little light it was never asked to keep. Show me your kin do the same.' },
  ],
  'trainer.lampwarden_lowleaf.defeat': [
    { speaker: 'SABLE QUILL', text: '...Oh. Oh, that was LOVELY. Don\'t tell anyone I said that out loud.' },
    { speaker: 'SABLE QUILL', text: 'The Verdant Gleam is yours — the moss vouched for you, and the moss has never once been wrong about a person.' },
  ],
  'trainer.lampwarden_cinderhead.intro': [
    { speaker: 'OTHO GRIST', text: 'No rush in my kin and no rush in me. We are the mountain, Wayfarer. We OUTLAST.' },
    { speaker: 'OTHO GRIST', text: 'Show me a light that does not gutter when the rock leans in. That is all a Gleam ever was.' },
  ],
  'trainer.lampwarden_cinderhead.defeat': [
    { speaker: 'OTHO GRIST', text: 'Hah. You did not out-hit them. You out-LASTED them. ...That, I respect. That is the deep way.' },
    { speaker: 'OTHO GRIST', text: 'A steady light. The Stone remembers it. Come — let the vigil see what you carried up.' },
  ],
  'trainer.gallery_miner_a.intro': [
    { speaker: 'DRUSE', text: 'Wick against wick, Wayfarer. Crew rule. You do not pass the gallery till you have weighed it.' },
  ],
  'trainer.gallery_miner_a.defeat': [
    { speaker: 'DRUSE', text: 'Steady enough. The lamp is two chambers on — and Hobb is between you and it.' },
  ],
  'trainer.gallery_miner_b.intro': [
    { speaker: 'HOBB', text: 'Last lamp before the vigil-lamp, and it is mine to keep. Come on, then.' },
  ],
  'trainer.gallery_miner_b.defeat': [
    { speaker: 'HOBB', text: 'Well held. Lift the vigil-lamp gentle, now — it has waited a long dark for a steady hand.' },
  ],
};

export function getTrainer(id: string): TrainerDef | undefined {
  return TRAINERS[id];
}

/** Resolve a trainer dialogue ref to its pages (empty array if unknown/absent). */
export function getTrainerLines(ref: string | undefined): DialogueLine[] {
  if (!ref) return [];
  return TRAINER_DIALOGUE[ref] ?? [];
}
