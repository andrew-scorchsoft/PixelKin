/**
 * The founding trio offered at the start of the Wayfaring. These are canon: the
 * three kin on the logo. The mentor lets the apprentice choose one. Species ids
 * resolve via SPECIES_BY_ID (dex.ts): #1 Vulpyre (Ember), #2 Brinix (Tide),
 * #152 Cloverkit (Verdant).
 */
import type { StarterOption } from './types';

export const STARTERS: StarterOption[] = [
  { species_id: 1, blurb: 'Ember — a hearth-spark fox. Warm, eager, quick to flare.' },
  { species_id: 2, blurb: 'Tide — a moonlit pooler. Calm, steady, deep as the bay.' },
  { species_id: 152, blurb: 'Verdant — a clover sprite. Gentle, lucky, stubbornly alive.' },
];

/** Starting level for a chosen starter. */
export const STARTER_LEVEL = 5;
