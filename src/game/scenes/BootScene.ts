import Phaser from 'phaser';

/**
 * First scene to run. Keep it tiny: load only what the loading screen itself
 * needs, then hand straight over to PreloadScene which loads the bulk of the
 * assets behind a progress bar.
 */
export class BootScene extends Phaser.Scene {
  constructor() {
    super('Boot');
  }

  preload(): void {
    // The logo doubles as the loading-screen art, so it's the one asset we
    // pull in before the main preload.
    this.load.image('logo', 'assets/ui/logo.png');
  }

  create(): void {
    this.scene.start('Preload');
  }
}
