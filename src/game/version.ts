/**
 * Single source of truth for the game's displayed version.
 *
 * ▶ To change the version, edit GAME_VERSION below — that's the only line you
 *   need to touch. It surfaces in two places automatically:
 *     • the title screen, bottom-right corner (at-a-glance, in-game)
 *     • the browser tab title, e.g. "PixelKin v1.1" (set in main.ts)
 *
 * Keep package.json's "version" in step if you want them to match, but THIS
 * constant is what the game itself shows the player.
 */
export const GAME_VERSION = '1.1';

/** Pre-formatted label for display, e.g. "v1.1". */
export const GAME_VERSION_LABEL = `v${GAME_VERSION}`;
