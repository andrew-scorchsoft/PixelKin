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
      { species_id: 10, level: 6 }, // Tallowpup — Ember
      { species_id: 18, level: 8 }, // Hearthkit — Ember
    ],
    intro_ref: 'trainer.lampwarden_tinderwick.intro',
    defeat_ref: 'trainer.lampwarden_tinderwick.defeat',
    reward_flags: ['gleam:ember', 'crown_south'],
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
};

export function getTrainer(id: string): TrainerDef | undefined {
  return TRAINERS[id];
}

/** Resolve a trainer dialogue ref to its pages (empty array if unknown/absent). */
export function getTrainerLines(ref: string | undefined): DialogueLine[] {
  if (!ref) return [];
  return TRAINER_DIALOGUE[ref] ?? [];
}
