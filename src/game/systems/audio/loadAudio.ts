/**
 * Load an audio file on demand, resolving false (not throwing) if it's missing.
 * Music and sfx are loaded lazily as scenes need them; a missing file must never
 * break gameplay, so callers can simply skip playback when this returns false.
 */
import Phaser from 'phaser';

export function loadAudio(scene: Phaser.Scene, key: string, url: string): Promise<boolean> {
  return new Promise((resolve) => {
    if (scene.cache.audio.exists(key)) {
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
    scene.load.audio(key, url);
    scene.load.start();
  });
}
