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
