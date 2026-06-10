/**
 * Screen transitions — promise-based so flows read top-to-bottom:
 *   await fadeOut(scene); switchMap(); await fadeIn(scene);
 * Used by warps (fade / door) and encounters (battle swoosh). All honour theme timings.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';

export function fadeOut(scene: Phaser.Scene, ms: number = theme.transition.fadeMs): Promise<void> {
  return new Promise((resolve) => {
    scene.cameras.main.once(Phaser.Cameras.Scene2D.Events.FADE_OUT_COMPLETE, () => resolve());
    scene.cameras.main.fadeOut(ms, 0, 0, 0);
  });
}

export function fadeIn(scene: Phaser.Scene, ms: number = theme.transition.fadeMs): Promise<void> {
  return new Promise((resolve) => {
    scene.cameras.main.once(Phaser.Cameras.Scene2D.Events.FADE_IN_COMPLETE, () => resolve());
    scene.cameras.main.fadeIn(ms, 0, 0, 0);
  });
}

export function flash(scene: Phaser.Scene, ms = 120): Promise<void> {
  return new Promise((resolve) => {
    scene.cameras.main.once(Phaser.Cameras.Scene2D.Events.FLASH_COMPLETE, () => resolve());
    scene.cameras.main.flash(ms, 159, 231, 255); // diamond cyan
  });
}

/** A coloured camera flash (generalises `flash`'s hard-coded cyan). */
export function flashColor(scene: Phaser.Scene, ms = 120, color = 0x9fe7ff): Promise<void> {
  const c = Phaser.Display.Color.IntegerToColor(color);
  return new Promise((resolve) => {
    scene.cameras.main.once(Phaser.Cameras.Scene2D.Events.FLASH_COMPLETE, () => resolve());
    scene.cameras.main.flash(ms, c.red, c.green, c.blue);
  });
}

/** Wrap the camera shake in a promise so cutscenes can await it. */
export function shake(scene: Phaser.Scene, ms = 240, intensity = 0.005): Promise<void> {
  return new Promise((resolve) => {
    scene.cameras.main.once(Phaser.Cameras.Scene2D.Events.SHAKE_COMPLETE, () => resolve());
    scene.cameras.main.shake(ms, intensity);
  });
}

// Camera-fixed singletons so repeated calls reuse the same bars / wash rather
// than stacking new game objects each cutscene step.
const LETTERBOX_KEY = '__pk_letterbox';
const TINT_KEY = '__pk_tint';

/**
 * Cinematic letterbox — two black bars slide in from top and bottom to frame a
 * dramatic beat, and slide back out on `off`. Bars are fixed to the camera and
 * sit just under the dialogue panel so a text box still reads over the lower bar.
 */
export function letterbox(scene: Phaser.Scene, on: boolean, ms: number = theme.cinematic.letterboxMs): Promise<void> {
  const barH = Math.round(GAME_HEIGHT * 0.14); // ~22px bars
  type Bars = { top: Phaser.GameObjects.Rectangle; bottom: Phaser.GameObjects.Rectangle };
  let bars = scene.data.get(LETTERBOX_KEY) as Bars | undefined;
  if (!bars) {
    const top = scene.add
      .rectangle(0, -barH, GAME_WIDTH, barH, hex(theme.color.panelShadow), 1)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.letterbox);
    const bottom = scene.add
      .rectangle(0, GAME_HEIGHT, GAME_WIDTH, barH, hex(theme.color.panelShadow), 1)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.letterbox);
    bars = { top, bottom };
    scene.data.set(LETTERBOX_KEY, bars);
  }
  const top = bars.top;
  const bottom = bars.bottom;
  return new Promise((resolve) => {
    scene.tweens.add({
      targets: top,
      y: on ? 0 : -barH,
      duration: ms,
      ease: 'Cubic.inOut',
    });
    scene.tweens.add({
      targets: bottom,
      y: on ? GAME_HEIGHT - barH : GAME_HEIGHT,
      duration: ms,
      ease: 'Cubic.inOut',
      onComplete: () => resolve(),
    });
  });
}

/**
 * Full-screen colour wash — tween a camera-fixed rectangle to `alpha` over `ms`
 * (and back to 0 when alpha is 0). Reuses one rectangle so dread/warmth washes
 * don't accumulate. Use a brief warm wash on a Gleam, a cold one on the dusk omen.
 */
export function tint(scene: Phaser.Scene, color: number, alpha = 0.4, ms: number = theme.cinematic.holdMs): Promise<void> {
  let rect = scene.data.get(TINT_KEY) as Phaser.GameObjects.Rectangle | undefined;
  if (!rect) {
    rect = scene.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, color, 0)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(theme.depth.tint);
    scene.data.set(TINT_KEY, rect);
  }
  rect.setFillStyle(color);
  return new Promise((resolve) => {
    scene.tweens.add({
      targets: rect,
      alpha,
      duration: ms,
      ease: 'Sine.inOut',
      onComplete: () => resolve(),
    });
  });
}

/** A quick into-battle swoosh: cyan flash then a short shake before the scene swaps. */
export async function battleSwoosh(scene: Phaser.Scene, ms: number = theme.transition.swooshMs): Promise<void> {
  scene.cameras.main.shake(ms, 0.004);
  await flash(scene, Math.min(160, ms / 2));
  await fadeOut(scene, ms / 2);
}
