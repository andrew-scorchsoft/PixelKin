/**
 * A toggleable developer overlay (default off; press `0` to toggle).
 *
 * Shows the player's tile, facing, current map, and set flags so triggers / warps /
 * encounters / collision can be verified without leaning on finished art. Pure dev
 * aid — pinned to the camera, above everything.
 */
import Phaser from 'phaser';
import { makeText } from './Text';
import { theme } from './theme';

export class DebugOverlay {
  private readonly text: Phaser.GameObjects.Text;
  private visible = false;

  constructor(scene: Phaser.Scene) {
    this.text = makeText(scene, 2, 2, '', theme.text.small)
      .setScrollFactor(0)
      .setDepth(theme.depth.toast + 10)
      .setVisible(false);
    this.text.setColor('#9fe7ff');
    scene.input.keyboard?.on('keydown-ZERO', () => this.toggle());
  }

  toggle(): void {
    this.visible = !this.visible;
    this.text.setVisible(this.visible);
  }

  set(lines: string[]): void {
    if (this.visible) this.text.setText(lines.join('\n'));
  }
}
