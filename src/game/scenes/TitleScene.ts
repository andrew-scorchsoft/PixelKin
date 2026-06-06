import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS } from '@game/config';

/**
 * The title screen — the first real taste of the game's feel. Logo, a gentle
 * "press to start" prompt that works for both keyboard and touch, and a soft
 * float on the logo so the screen breathes. The world scene plugs in from here
 * once it exists.
 */
export class TitleScene extends Phaser.Scene {
  constructor() {
    super('Title');
  }

  create(): void {
    const cx = GAME_WIDTH / 2;
    const cy = GAME_HEIGHT / 2;

    const logo = this.add.image(cx, cy - 16, 'logo').setOrigin(0.5);
    const maxLogoWidth = GAME_WIDTH - 32;
    if (logo.width > maxLogoWidth) {
      logo.setScale(maxLogoWidth / logo.width);
    }

    // Gentle bob — cheap motion that makes a static title feel alive.
    this.tweens.add({
      targets: logo,
      y: logo.y - 4,
      duration: 1600,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.inOut',
    });

    const prompt = this.add
      .text(cx, cy + 48, 'PRESS ENTER / TAP', {
        fontFamily: 'monospace',
        fontSize: '10px',
        color: COLORS.bone,
      })
      .setOrigin(0.5);

    this.tweens.add({
      targets: prompt,
      alpha: 0.2,
      duration: 700,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.inOut',
    });

    const start = () => this.startGame();
    this.input.keyboard?.once('keydown-ENTER', start);
    this.input.keyboard?.once('keydown-SPACE', start);
    this.input.once('pointerdown', start);
  }

  private startGame(): void {
    // TODO: swap for the WorldScene once it exists.
    this.cameras.main.fadeOut(300, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.restart();
    });
  }
}
