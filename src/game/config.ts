/**
 * Global game configuration and shared constants.
 *
 * The internal render resolution is fixed and small on purpose: 240x160 is the
 * Game Boy Advance's native canvas, one step on from the Game Boy Color's
 * 160x144. We render the world at this size and let Phaser's Scale.FIT blow it
 * up with nearest-neighbour sampling, so every pixel stays a crisp, chunky
 * square at any window size. That is the whole nostalgia play — the art reads
 * as authentic handheld-era pixel art rather than smooth modern vector work.
 */
export const GAME_WIDTH = 240;
export const GAME_HEIGHT = 160;

/** Logical tile size in source pixels. 16x16 is the classic handheld RPG tile. */
export const TILE_SIZE = 16;

/**
 * Render supersample factor — how many real device pixels we render each logical
 * 240x160 pixel into.
 *
 * The world is pixel art and stays deliberately chunky: tiles/sprites keep
 * nearest-neighbour sampling, so a 16px tile still reads as fat retro squares.
 * But everything is drawn into a *higher-resolution* framebuffer (the Phaser
 * canvas is sized GAME_WIDTH*RENDER_SCALE x GAME_HEIGHT*RENDER_SCALE via the
 * scale manager's `zoom`). That gives the in-canvas pixel font real pixels to
 * render into, so text comes out crisp instead of being a 240x160 bitmap blown
 * up by nearest-neighbour. See `main.ts` (zoom) and `ui/Text.ts` (resolution),
 * which both read this value. Logical game coordinates are unchanged — only the
 * framebuffer resolution grows.
 *
 * We size the framebuffer to roughly match the on-screen device pixels at boot
 * (so Scale.FIT lands near 1:1 and nothing is re-sampled), clamped to a sane
 * range so we never allocate an enormous buffer on a 4K/Retina panel.
 */
export const RENDER_SCALE = computeRenderScale();

function computeRenderScale(): number {
  if (typeof window === 'undefined') return 4; // SSR / tooling fallback
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const fit = Math.min(window.innerWidth / GAME_WIDTH, window.innerHeight / GAME_HEIGHT);
  // Round to the device pixels a logical pixel covers, clamped to 2..8.
  return Math.max(2, Math.min(8, Math.round(fit * dpr)));
}

/** Brand palette — a few anchor colours pulled from the PixelKin logo. */
export const COLORS = {
  night: '#0b1026',
  deepBlue: '#13205a',
  diamond: '#9fe7ff',
  grass: '#7bdc6b',
  fire: '#ff8a3d',
  water: '#4fb4ff',
  ink: '#1a1430',
  bone: '#f5f0e1',
} as const;
