import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, COLORS } from '@game/config';

/**
 * Loads the game's assets behind a progress bar. Right now there is almost
 * nothing to load — as sprites, tilesets, maps, music and sfx land in
 * public/assets/, queue them here and the progress bar handles the rest.
 */
export class PreloadScene extends Phaser.Scene {
  constructor() {
    super('Preload');
  }

  preload(): void {
    this.drawLoadingUi();

    // --- Queue real assets here as they arrive, e.g.: ---
    // this.load.spritesheet('player', 'assets/sprites/player.png', { frameWidth: 16, frameHeight: 24 });
    // this.load.tilemapTiledJSON('town', 'assets/maps/town.json');
    // this.load.audio('overworld', 'assets/audio/music/overworld.mp3');

    // Battle music — lush SNES-era dusk themes. 'dusk-duel' is the default
    // wild-encounter theme; emberfall/nightfall/veil are interchangeable
    // siblings to rotate per encounter so random battles stay fresh. Each is a
    // seamless loop, so play with `{ loop: true }`.
    this.load.audio('battle-dusk-duel', 'assets/audio/music/battle-main-dusk-duel.mp3');
    this.load.audio('battle-emberfall', 'assets/audio/music/battle-emberfall.mp3');
    this.load.audio('battle-nightfall', 'assets/audio/music/battle-nightfall.mp3');
    this.load.audio('battle-veil', 'assets/audio/music/battle-veil.mp3');
    // Boss / hard-opponent theme — grander, with a key-lifting climax.
    this.load.audio('battle-boss-eclipse', 'assets/audio/music/battle-boss-eclipse.mp3');
  }

  create(): void {
    this.scene.start('Title');
  }

  private drawLoadingUi(): void {
    const cx = GAME_WIDTH / 2;
    const cy = GAME_HEIGHT / 2;

    const logo = this.add.image(cx, cy - 18, 'logo').setOrigin(0.5);
    const maxLogoWidth = GAME_WIDTH - 48;
    if (logo.width > maxLogoWidth) {
      logo.setScale(maxLogoWidth / logo.width);
    }

    const barWidth = GAME_WIDTH - 80;
    const barHeight = 6;
    const barX = cx - barWidth / 2;
    const barY = cy + 40;

    const frame = this.add.graphics();
    frame.lineStyle(1, Phaser.Display.Color.HexStringToColor(COLORS.diamond).color, 1);
    frame.strokeRect(barX - 1, barY - 1, barWidth + 2, barHeight + 2);

    const fill = this.add.graphics();
    this.load.on('progress', (value: number) => {
      fill.clear();
      fill.fillStyle(Phaser.Display.Color.HexStringToColor(COLORS.diamond).color, 1);
      fill.fillRect(barX, barY, barWidth * value, barHeight);
    });
  }
}
