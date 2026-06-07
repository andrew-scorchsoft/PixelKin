/**
 * Themed text factory. The one place text styles come from, so every label in the
 * game speaks with the same voice (the bundled pixel font + theme colours). Pass a
 * style token from `theme.text`; never hand-write fontFamily/size in a screen.
 */
import Phaser from 'phaser';
import { RENDER_SCALE } from '@game/config';
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
  // Render the glyph texture at the framebuffer's real device-pixel density
  // (the canvas is zoomed by RENDER_SCALE in main.ts). At resolution 1 the font
  // is a 240x160 bitmap blown up by nearest-neighbour and looks blocky; matching
  // the render scale gives it real pixels, so the pixel font stays sharp at any
  // window size. `width`/`height` stay in logical (240x160) units, so layout
  // maths elsewhere is unaffected.
  t.setResolution(RENDER_SCALE);
  return t;
}
