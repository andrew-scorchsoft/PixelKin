/**
 * Typed access to the data-driven creature/battle definitions.
 *
 * The JSON files (type-chart.json, moves.json, species.json) are the single
 * source of truth, shared with the balance tooling in tools/balance/. This
 * module layers PixelKin's TypeScript types over them and exposes a few small
 * helpers (type effectiveness, lookups). Design docs: docs/mechanics/.
 */
import typeChartJson from './type-chart.json';
import movesJson from './moves.json';
import speciesJson from './species.json';

export const KIN_TYPES = [
  'Ember', 'Tide', 'Verdant', 'Stone', 'Storm',
  'Frost', 'Solar', 'Lunar', 'Light', 'Dark',
] as const;
export type KinType = (typeof KIN_TYPES)[number];
/** Move type: any kin type, or the typeless 'Plain' category. */
export type MoveType = KinType | 'Plain';

export type MoveCategory = 'physical' | 'special' | 'status';
export type Tier = 'A' | 'B' | 'C' | 'D' | 'E' | 'F';
export type Rarity = 'common' | 'uncommon' | 'rare' | 'very_rare' | 'legendary';

export interface Stats {
  hp: number; atk: number; def: number; spa: number; spd: number; spe: number;
}

export interface Move {
  id: string;
  name: string;
  type: MoveType;
  category: MoveCategory;
  power: number;
  accuracy: number;
  charges: number;
  priority: number;
  target: string;
  effect: Record<string, unknown> | null;
  flags: string[];
  desc: string;
  signature?: boolean;
}

export interface Ability {
  id: string;
  name: string;
  tier: 'minor' | 'standard' | 'strong';
  eps: number;
  effect: Record<string, unknown>;
  desc: string;
}

export interface KindlingTrigger {
  kind: 'level' | 'bond' | 'stone' | 'location' | 'time' | 'linked';
  level?: number;
  when?: 'day' | 'night';
  item?: string;
  area?: string;
  min?: number;
}

export interface Kindling {
  into: number;
  trigger: KindlingTrigger;
}

export interface LearnMove { level: number; move: string; }

export interface Species {
  id: number;
  slug: string;
  name: string;
  types: KinType[];
  role: string;
  tier: Tier;
  stats: Stats;
  bst: number;
  ability: string;
  hidden_ability: string | null;
  catchRate: number;
  kindling: Kindling | null;
  from: number | null;
  stage: number;
  learnset: { levelup: LearnMove[]; kindling: string[]; tutor: string[] };
  dex: {
    entry: string; category: string;
    size_cm: number; weight_kg: number; habitat: string;
  };
  encounters: Array<{ area: string; terrain: string; rarity: Rarity; min: number; max: number }>;
  scripted: boolean;
  art: { silhouette: string; palette: string; direction: string };
  provenance_concept_id: string;
}

const typeChart = (typeChartJson as { chart: Record<string, Record<string, number>> }).chart;

export const MOVES: Move[] = (movesJson as { moves: Move[] }).moves;
export const ABILITIES: Ability[] = (movesJson as { abilities: Ability[] }).abilities;
export const SPECIES: Species[] = (speciesJson as { species: Species[] }).species;

export const MOVE_BY_ID: Map<string, Move> = new Map(MOVES.map((m) => [m.id, m]));
export const ABILITY_BY_ID: Map<string, Ability> = new Map(ABILITIES.map((a) => [a.id, a]));
export const SPECIES_BY_ID: Map<number, Species> = new Map(SPECIES.map((s) => [s.id, s]));

/** Damage multiplier of an attacking move type against one or two defender types. */
export function typeEffectiveness(attack: MoveType, defenders: readonly KinType[]): number {
  if (attack === 'Plain') return 1;
  const row = typeChart[attack] ?? {};
  let mult = 1;
  for (const d of defenders) mult *= row[d] ?? 1;
  return mult;
}
