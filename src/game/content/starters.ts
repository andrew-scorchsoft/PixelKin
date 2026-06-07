/**
 * The founding trio offered at the start of the Wayfaring. These are canon: the
 * three kin on the logo. The mentor lets the apprentice choose one. Species ids
 * resolve via SPECIES_BY_ID (dex.ts): #1 Vulpyre (Ember), #2 Brinix (Tide),
 * #152 Cloverkit (Verdant).
 */
import type { StarterOption } from './types';
import type { KinInstanceData } from '@game/systems/save/types';
import { KinInstance } from '@game/systems/party/KinInstance';

export const STARTERS: StarterOption[] = [
  { species_id: 1, blurb: 'Ember — a hearth-spark fox. Warm, eager, quick to flare.' },
  { species_id: 2, blurb: 'Tide — a moonlit pooler. Calm, steady, deep as the bay.' },
  { species_id: 152, blurb: 'Verdant — a clover sprite. Gentle, lucky, stubbornly alive.' },
];

/** Starting level for a chosen starter. */
export const STARTER_LEVEL = 5;

/**
 * Build a fresh owned-kin save record for a species at a level. Delegates to
 * KinInstance (the single source of truth for stats/exp/moves) so the starter's
 * exp matches its level and it begins at full health — then serialises to plain
 * save data (KinInstanceData).
 */
export function makeStarterKin(speciesId: number, level: number = STARTER_LEVEL): KinInstanceData {
  return KinInstance.create(speciesId, level).toData();
}
