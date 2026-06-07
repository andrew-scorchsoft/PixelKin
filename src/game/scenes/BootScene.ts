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
    // Make sure the bundled pixel font is decoded before any scene draws text,
    // otherwise Phaser renders the first labels in a fallback font and won't
    // refresh them. Proceed anyway if the Font Loading API is unavailable.
    const fonts = (document as Document & { fonts?: FontFaceSet }).fonts;
    const go = (): void => {
      this.scene.start('Preload');
    };
    if (fonts?.load) {
      Promise.all([fonts.load('8px PixelKin'), fonts.load('16px PixelKin')])
        .then(go)
        .catch(go);
    } else {
      go();
    }
  }
}
