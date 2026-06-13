/**
 * Portrait registry — character busts shown in the dialogue box and cutscenes.
 *
 * Each portrait is ONE spritesheet of 32×32 frames (the same frame size as the
 * world action sheets), with named expressions mapping to a frame index. A
 * dialogue line opts in with `{ portrait: 'fenn', expr: 'warm' }`; the DialogueBox
 * draws the frame top-left and shrinks the text wrap to fit. Missing art falls
 * back to a name-only box (today's behaviour), so portraits are purely additive.
 *
 * Adding a character = drop a 32×N sheet under public/assets/portraits/ and add
 * an entry here. The served path drops the `public/` prefix (see CLAUDE.md).
 */

export interface PortraitDef {
  /** Texture key (also the load key). */
  id: string;
  /** Served sheet path, e.g. 'assets/portraits/fenn.png'. */
  path: string;
  /** Expression name → frame index within the sheet. 'neutral' should exist. */
  expressions: Record<string, number>;
}

/** Standard portrait frame size (square bust). */
export const PORTRAIT_FRAME = { frameWidth: 32, frameHeight: 32 };

/**
 * First-hour cast. Frame order is the authoring contract for the sheets the
 * generate-sprite-sheet skill produces: col 0 neutral, then the listed moods.
 */
export const PORTRAITS: Record<string, PortraitDef> = {
  fenn: {
    id: 'portrait_fenn',
    path: 'assets/portraits/fenn.png',
    expressions: { neutral: 0, warm: 1, grave: 2, smile: 3, peace: 4 },
  },
  wren: {
    id: 'portrait_wren',
    path: 'assets/portraits/wren.png',
    expressions: { neutral: 0, eager: 1, unsure: 2, resolved: 3 },
  },
  brisa: {
    id: 'portrait_brisa',
    path: 'assets/portraits/brisa.png',
    expressions: { neutral: 0, warm: 1, proud: 2 },
  },
  reyl: {
    id: 'portrait_reyl',
    path: 'assets/portraits/reyl.png',
    expressions: { neutral: 0, weathered: 1, proud: 2 },
  },
  lamplighter: {
    id: 'portrait_lamplighter',
    path: 'assets/portraits/lamplighter.png',
    expressions: { neutral: 0, grave: 1 },
  },
  // The Hearthkeeper — tends the Hearth (kin storage); met early, warm and motherly.
  hearthkeeper: {
    id: 'portrait_hearthkeeper',
    path: 'assets/portraits/hearthkeeper.png',
    expressions: { neutral: 0, warm: 1 },
  },
  // Georgina, the Cat-keeper — a bubbly sunshine-goth who keeps cats (and one
  // dragon-cat) in a fairy-lit cottage deep in the dark wood. The anti-Hollowing:
  // loves the dark, fills it with light. Optional East side quest.
  georgina: {
    id: 'portrait_georgina',
    path: 'assets/portraits/georgina.png',
    expressions: { neutral: 0, sunny: 1, delighted: 2, wink: 3 },
  },
  // Sable Quill — the Verdant Lampwarden of Lowleaf Hollow; a shy botanist.
  sable: {
    id: 'portrait_sable',
    path: 'assets/portraits/sable.png',
    expressions: { neutral: 0, shy: 1, warm: 2 },
  },
  // Warden Còr — the Hollowing's gentle, sorrowful leader; the marquee face of the
  // late game (B3 Pale Vault, the Spire summit, the post-game lamp-room).
  cor: {
    id: 'portrait_cor',
    path: 'assets/portraits/cor.png',
    expressions: { neutral: 0, grave: 1, gentle: 2, sorrowful: 3, at_peace: 4 },
  },
  // Mira Vael — the Storm Lampwarden of Galehigh Terraces; breathless kite-flier.
  mira: {
    id: 'portrait_mira',
    path: 'assets/portraits/mira.png',
    expressions: { neutral: 0, bright: 1, soft: 2 },
  },
  // Ysolde Frost — the Frost Lampwarden of Pale Vault; still, watchful, quietly kind.
  ysolde: {
    id: 'portrait_ysolde',
    path: 'assets/portraits/ysolde.png',
    expressions: { neutral: 0, serene: 1, warm: 2 },
  },
  // Lucan Pyre — the Solar Lampwarden of the Sunken Solarium; theatrical, bittersweet.
  lucan: {
    id: 'portrait_lucan',
    path: 'assets/portraits/lucan.png',
    expressions: { neutral: 0, grand: 1, bittersweet: 2 },
  },
  // Nessa Cole — the Lunar Lampwarden of Nightreach; haunted astronomer-priestess.
  nessa: {
    id: 'portrait_nessa',
    path: 'assets/portraits/nessa.png',
    expressions: { neutral: 0, haunted: 1, reverent: 2 },
  },
};

/** Resolve a portrait id + expression to its texture key and frame index. */
export function resolvePortrait(id: string | undefined, expr?: string): { def: PortraitDef; frame: number } | undefined {
  if (!id) return undefined;
  const def = PORTRAITS[id];
  if (!def) return undefined;
  const idx = expr ? def.expressions[expr] : undefined;
  const frame = idx ?? def.expressions.neutral ?? 0;
  return { def, frame };
}

/** Every portrait sheet path + frame size, for PreloadScene to queue eagerly. */
export const PORTRAIT_SHEETS: ReadonlyArray<{ key: string; path: string }> = Object.values(PORTRAITS).map((p) => ({
  key: p.id,
  path: p.path,
}));
