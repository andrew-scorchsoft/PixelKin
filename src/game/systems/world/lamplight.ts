/**
 * Lamplight — the vesperlamp's brightness tiers, the CONTINUOUS exploration axis
 * (walkthrough spine §5). Each relit constellation feeds the lamp, so the tier is
 * a pure function of held Gleams. The binding rule: Lamplight is ADDITIVE, never
 * blocking — it only ever reveals optional content (caches, side-cells, alcoves);
 * the main path is diegetically lit and stays visible/walkable at every tier.
 *
 * Two consumers:
 *  - FlagStore.derive() raises the threshold flags (`flag:lamplight_warmlight` …
 *    `flag:lamplight_radiant`) from the Gleam count — derived and self-healing,
 *    NEVER hand-set by content (the crowns/hub pattern). Reveal content gates on
 *    those flags with ordinary `requires_flag`, so no new engine field exists.
 *  - The dark-map reveal mask (WorldScene) reads `revealRadiusTiles` for the lit
 *    circle's size.
 */

/** The five tiers, in order, with the spine §5 thresholds (Gleams held). */
export const LAMPLIGHT_TIERS = [
  { name: 'Ember-glow', minGleams: 0 }, // a candle's circle — the cosy opening
  { name: 'Warmlight', minGleams: 2 }, // a lantern's reach
  { name: 'Brightlight', minGleams: 4 }, // a strong, confident lamp
  { name: 'Starlight', minGleams: 6 }, // a far, clean reach
  { name: 'Radiant', minGleams: 8 }, // near-daylight — you carry the dawn
] as const;

export type LamplightTierName = (typeof LAMPLIGHT_TIERS)[number]['name'];

/**
 * The derived threshold flags, raised by FlagStore.derive() the moment the Gleam
 * count crosses each tier's minimum. Content must never list these in
 * sets_flags/reward_flags (validate.mjs's derived-flag guard enforces it) — gate
 * reveals on them with `requires_flag` instead.
 */
export const LAMPLIGHT_FLAGS: ReadonlyArray<{ flag: string; minGleams: number }> = [
  { flag: 'flag:lamplight_warmlight', minGleams: 2 },
  { flag: 'flag:lamplight_brightlight', minGleams: 4 },
  { flag: 'flag:lamplight_starlight', minGleams: 6 },
  { flag: 'flag:lamplight_radiant', minGleams: 8 },
];

/** Tier index (0..4) for a held-Gleam count. */
export function lamplightTier(gleams: number): number {
  let tier = 0;
  for (let i = 0; i < LAMPLIGHT_TIERS.length; i++) {
    if (gleams >= LAMPLIGHT_TIERS[i].minGleams) tier = i;
  }
  return tier;
}

/** The LORE-friendly tier name for a held-Gleam count ("Warmlight", …). */
export function lamplightTierName(gleams: number): LamplightTierName {
  return LAMPLIGHT_TIERS[lamplightTier(gleams)].name;
}

/**
 * The lit circle's radius on dark maps, in tiles, per tier. Tuned so the main
 * lane always reads even at Ember-glow (the darkness beyond is partial anyway —
 * see LamplightMask), and Radiant all but banishes the dark on a 240×160 view.
 */
const REVEAL_RADIUS_TILES = [3, 4, 5, 6.5, 8] as const;

export function revealRadiusTiles(gleams: number): number {
  return REVEAL_RADIUS_TILES[lamplightTier(gleams)];
}
