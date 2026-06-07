/**
 * The founding trio offered at the start of the Wayfaring. These are canon: the
 * three kin on the logo. The mentor lets the apprentice choose one. Species ids
 * resolve via SPECIES_BY_ID (dex.ts): #1 Vulpyre (Ember), #2 Brinix (Tide),
 * #152 Cloverkit (Verdant).
 */
import type { StarterOption } from './types';
import { SPECIES_BY_ID, MOVE_BY_ID } from '@game/data/dex';
import type { KinInstanceData } from '@game/systems/save/types';

export const STARTERS: StarterOption[] = [
  { species_id: 1, blurb: 'Ember — a hearth-spark fox. Warm, eager, quick to flare.' },
  { species_id: 2, blurb: 'Tide — a moonlit pooler. Calm, steady, deep as the bay.' },
  { species_id: 152, blurb: 'Verdant — a clover sprite. Gentle, lucky, stubbornly alive.' },
];

/** Starting level for a chosen starter. */
export const STARTER_LEVEL = 5;

/**
 * Build a fresh owned-kin save record for a species at a level. Mirrors the
 * standard HP formula the battle layer uses so the kin starts at full health, and
 * seeds the latest up-to-4 level-up moves it would know. Returns plain save data
 * (KinInstanceData) so it works without the battle runtime loaded.
 */
export function makeStarterKin(speciesId: number, level: number = STARTER_LEVEL): KinInstanceData {
  const species = SPECIES_BY_ID.get(speciesId);
  if (!species) throw new Error(`No species ${speciesId} for starter`);

  const maxHp = Math.floor((2 * species.stats.hp * level) / 100) + level + 10;
  const moveIds = species.learnset.levelup
    .filter((m) => m.level <= level)
    .map((m) => m.move)
    .slice(-4);
  const moves = moveIds.map((id) => ({ id, charges: MOVE_BY_ID.get(id)?.charges ?? 10 }));

  return { species_id: speciesId, level, exp: 0, hp: maxHp, moves, status: 'none' };
}
