import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { GAME_VERSION_LABEL } from '@game/version';
import { theme } from './theme';
import { makeText } from './Text';

/**
 * The quiet version stamp, centred on the bottom edge of the boot screens
 * (loading bar, studio sting, attract trailer) — so a player checking which
 * build they're on can read it the moment the page loads, without pressing
 * through to the title (which keeps its own corner stamp + NEW tag).
 */
export function addVersionStamp(scene: Phaser.Scene): Phaser.GameObjects.Text {
  return makeText(scene, GAME_WIDTH / 2, GAME_HEIGHT - 2, GAME_VERSION_LABEL, theme.text.dim)
    .setOrigin(0.5, 1)
    .setAlpha(0.7)
    .setDepth(theme.depth.text);
}
