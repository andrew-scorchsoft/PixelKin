/**
 * Cursor — the blinking pointer that sits beside the selected menu row. Purely
 * visual; menus move it and play the cursor sfx. Texture is generated at runtime.
 */
import Phaser from 'phaser';
import { theme, hex } from './theme';

const CURSOR_KEY = 'ui_cursor_tri';

function ensureCursorTexture(scene: Phaser.Scene): void {
  if (scene.textures.exists(CURSOR_KEY)) return;
  const g = scene.add.graphics();
  g.fillStyle(hex(theme.color.textAccent), 1);
  // a small right-pointing triangle, 5x7
  g.beginPath();
  g.moveTo(0, 0);
  g.lineTo(5, 3.5);
  g.lineTo(0, 7);
  g.closePath();
  g.fillPath();
  g.generateTexture(CURSOR_KEY, 5, 7);
  g.destroy();
}

export class Cursor {
  readonly sprite: Phaser.GameObjects.Image;
  private blink?: Phaser.Tweens.Tween;

  constructor(scene: Phaser.Scene) {
    ensureCursorTexture(scene);
    this.sprite = scene.add.image(0, 0, CURSOR_KEY).setOrigin(0, 0.5).setDepth(theme.depth.cursor);
    this.blink = scene.tweens.add({
      targets: this.sprite,
      alpha: 0.25,
      duration: theme.cursor.blinkMs,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.inOut',
    });
  }

  moveTo(x: number, y: number): void {
    this.sprite.setPosition(x, y);
  }

  setScrollFactor0(): this {
    this.sprite.setScrollFactor(0);
    return this;
  }

  setVisible(v: boolean): this {
    this.sprite.setVisible(v);
    return this;
  }

  destroy(): void {
    this.blink?.remove();
    this.sprite.destroy();
  }
}
