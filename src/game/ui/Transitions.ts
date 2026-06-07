/**
 * Screen transitions — promise-based so flows read top-to-bottom:
 *   await fadeOut(scene); switchMap(); await fadeIn(scene);
 * Used by warps (fade / door) and encounters (battle swoosh). All honour theme timings.
 */
import Phaser from 'phaser';
import { theme } from './theme';

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

/** A quick into-battle swoosh: cyan flash then a short shake before the scene swaps. */
export async function battleSwoosh(scene: Phaser.Scene, ms: number = theme.transition.swooshMs): Promise<void> {
  scene.cameras.main.shake(ms, 0.004);
  await flash(scene, Math.min(160, ms / 2));
  await fadeOut(scene, ms / 2);
}
