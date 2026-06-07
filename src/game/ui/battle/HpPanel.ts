/**
 * HpPanel — the name + level + HP-bar plate for one combatant, built from the
 * shared Panel + Text so it matches the rest of the game. The bar tweens to a
 * new value (so a hit reads as a smooth drain) and recolours green → amber → red
 * as the kin weakens. The player's plate also shows the numeric HP.
 */
import Phaser from 'phaser';
import { COLORS } from '@game/config';
import { theme, hex } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { Panel } from '@game/ui/Panel';
import type { KinInstance } from '@game/systems/party/KinInstance';

const BAR_W = 48;
const BAR_H = 4;

export class HpPanel {
  private readonly panel: Panel;
  private readonly bar: Phaser.GameObjects.Rectangle;
  private readonly barBg: Phaser.GameObjects.Rectangle;
  private readonly nameText: Phaser.GameObjects.Text;
  private readonly hpText?: Phaser.GameObjects.Text;
  private kin: KinInstance;

  constructor(
    private readonly scene: Phaser.Scene,
    x: number,
    y: number,
    kin: KinInstance,
    showNumbers: boolean,
  ) {
    this.kin = kin;
    const w = 78;
    const h = showNumbers ? 34 : 26;
    this.panel = new Panel(scene, x, y, w, h).fixedToCamera();

    this.nameText = makeText(scene, theme.space.lg, theme.space.md, '', theme.text.base);
    const lvlY = theme.space.md;
    const barY = 16;
    this.panel.add(this.nameText);

    this.barBg = scene.add
      .rectangle(theme.space.lg, barY, BAR_W, BAR_H, hex(theme.color.panelShadow))
      .setOrigin(0, 0)
      .setScrollFactor(0);
    this.bar = scene.add
      .rectangle(theme.space.lg, barY, BAR_W, BAR_H, hex(COLORS.grass))
      .setOrigin(0, 0)
      .setScrollFactor(0);
    this.panel.add(this.barBg);
    this.panel.add(this.bar);

    // "Lv" label sits to the right of the name.
    void lvlY;

    if (showNumbers) {
      this.hpText = makeText(scene, theme.space.lg, barY + 6, '', theme.text.dim);
      this.panel.add(this.hpText);
    }

    this.refresh();
  }

  /** Point the panel at a different kin (after a switch). */
  setKin(kin: KinInstance): void {
    this.kin = kin;
    this.refresh();
  }

  /** Snap all readouts to the current kin state. */
  refresh(): void {
    this.nameText.setText(`${this.kin.displayName}  Lv${this.kin.level}`);
    const ratio = this.kin.hpRatio;
    this.bar.width = Math.max(0, Math.round(BAR_W * ratio));
    this.bar.fillColor = this.colorFor(ratio);
    this.hpText?.setText(`${Math.max(0, this.kin.hp)}/${this.kin.maxHp}`);
  }

  private colorFor(ratio: number): number {
    if (ratio > 0.5) return hex(COLORS.grass);
    if (ratio > 0.2) return hex('#ffd86b');
    return hex(theme.color.danger);
  }

  /** Tween the bar to the kin's current hp; resolves when done. */
  animateTo(): Promise<void> {
    return new Promise((resolve) => {
      const ratio = this.kin.hpRatio;
      const target = Math.max(0, Math.round(BAR_W * ratio));
      this.bar.fillColor = this.colorFor(ratio);
      this.hpText?.setText(`${Math.max(0, this.kin.hp)}/${this.kin.maxHp}`);
      this.scene.tweens.add({
        targets: this.bar,
        width: target,
        duration: 360,
        ease: 'Quad.out',
        onUpdate: () => {
          // recolour mid-drain
          const r = this.bar.width / BAR_W;
          this.bar.fillColor = this.colorFor(r);
        },
        onComplete: () => resolve(),
      });
    });
  }

  destroy(): void {
    this.bar.destroy();
    this.barBg.destroy();
    this.panel.destroy();
  }
}
