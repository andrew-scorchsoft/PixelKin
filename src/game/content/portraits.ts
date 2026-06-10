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
    expressions: { neutral: 0, warm: 1, grave: 2, smile: 3 },
  },
  wren: {
    id: 'portrait_wren',
    path: 'assets/portraits/wren.png',
    expressions: { neutral: 0, eager: 1, unsure: 2 },
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
