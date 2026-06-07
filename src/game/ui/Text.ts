/**
 * Themed text factory. The one place text styles come from, so every label in the
 * game speaks with the same voice (the bundled pixel font + theme colours). Pass a
 * style token from `theme.text`; never hand-write fontFamily/size in a screen.
 */
import Phaser from 'phaser';
import { theme } from './theme';

export type TextStyleToken = { fontFamily: string; fontSize: string; color: string };

export function makeText(
  scene: Phaser.Scene,
  x: number,
  y: number,
  content: string,
  style: TextStyleToken = theme.text.base,
): Phaser.GameObjects.Text {
  const t = scene.add.text(x, y, content, {
    fontFamily: style.fontFamily,
    fontSize: style.fontSize,
    color: style.color,
  });
  // Pixel font: keep it crisp, no smoothing, no sub-pixel drift.
  t.setResolution(1);
  return t;
}
