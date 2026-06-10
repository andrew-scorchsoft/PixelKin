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
    music: 'battle-emberfall',
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
  'trainer.lampwarden_pearlmoor.intro': [
    { speaker: 'REYL WASH', text: 'Apprentice, is it. I have ferried a hundred Wayfarers across this harbour. Few read the water right.' },
    { speaker: 'REYL WASH', text: 'Tides go out so they can come back, see. Show me your bond holds against mine — then I will teach you to ask the sea to part.' },
  ],
  'trainer.lampwarden_pearlmoor.defeat': [
    { speaker: 'REYL WASH', text: 'Well rowed, Wayfarer. The Tide constellation answers you — see it shiver awake over the masts.' },
    { speaker: 'REYL WASH', text: 'The Tide Gleam is yours, and with it the Tidecall. Step to the shallows now; the moon-water will part where it would not before.' },
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
