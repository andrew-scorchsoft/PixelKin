/**
 * Load an image (or a spritesheet of fixed-size frames) on demand, resolving
 * false (not throwing) if the file is missing — the visual sibling of loadAudio.
 *
 * Portraits, cold-open panels and other late-bound art use this so a missing
 * asset degrades gracefully (caller skips drawing it) instead of crashing. If
 * `frame` is given the texture is loaded as a spritesheet so individual frames
 * can be addressed by index.
 */
import Phaser from 'phaser';

export function loadImage(
  scene: Phaser.Scene,
  key: string,
  url: string,
  frame?: { frameWidth: number; frameHeight: number },
): Promise<boolean> {
  return new Promise((resolve) => {
    if (scene.textures.exists(key)) {
      resolve(true);
      return;
    }
    const onFile = (fileKey: string): void => {
      if (fileKey === key) {
        cleanup();
        resolve(true);
      }
    };
    const onError = (file: Phaser.Loader.File): void => {
      if (file.key === key) {
        cleanup();
        resolve(false);
      }
    };
    const cleanup = (): void => {
      scene.load.off(Phaser.Loader.Events.FILE_COMPLETE, onFile);
      scene.load.off(Phaser.Loader.Events.FILE_LOAD_ERROR, onError);
    };
    scene.load.on(Phaser.Loader.Events.FILE_COMPLETE, onFile);
    scene.load.on(Phaser.Loader.Events.FILE_LOAD_ERROR, onError);
    if (frame) scene.load.spritesheet(key, url, frame);
    else scene.load.image(key, url);
    scene.load.start();
  });
}
