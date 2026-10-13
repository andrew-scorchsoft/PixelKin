/**
 * HpPanel — the name + level + HP-bar plate for one combatant, built from the
 * shared Panel + Text so it matches the rest of the game. The bar tweens to a
 * new value (so a hit reads as a smooth drain) and recolours green → amber → red
 * as the kin weakens. The player's plate also shows the numeric HP.
 *
 * The foe's plate can carry the LAMP MARK: a tiny code-drawn vesperlamp beside
 * the bar when that species is already in your Register as caught (the genre's
 * "you've got one of these" cue). Pass `isCaught`; it's re-asked on every
 * refresh, so a trainer's next kin gets the right mark after a switch.
 */
import Phaser from 'phaser';
import { COLORS } from '@game/config';
import { theme, hex } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { Panel } from '@game/ui/Panel';
import { battlePaceFactor } from '@game/ui/preferences';
import type { KinInstance } from '@game/systems/party/KinInstance';

const BAR_W = 48;
const BAR_H = 4;
const PAD = theme.space.lg;
/** Floor so the bar (and HP numbers) always fit even for very short names. */
const MIN_W = PAD * 2 + BAR_W;
/** The lamp mark: a 7x9 pixel vesperlamp drawn just right of the bar. */
const MARK_GAP = 4;
const MARK_W = 7;
const LAMP_MARK = [
  '..mmm..',
  '.m...m.',
  'mmmmmmm',
  '.mgggm.',
  '.mgwgm.',
  '.mgggm.',
  '.mgggm.',
  'mmmmmmm',
  '..mmm..',
];

/**
 * Where the panel is pinned. The foe plate hugs the top-left and grows
 * rightwards; the player plate hugs the bottom-right and grows leftwards, so a
 * long "Name  Lv99" can never run off the right edge of the 240px screen (the
 * bug where Vulpyre's level was clipped).
 */
export type HpPanelAlign = 'left' | 'right';

export class HpPanel {
  private readonly panel: Panel;
  private readonly bar: Phaser.GameObjects.Rectangle;
  private readonly barBg: Phaser.GameObjects.Rectangle;
  private readonly nameText: Phaser.GameObjects.Text;
  private readonly hpText?: Phaser.GameObjects.Text;
  private readonly height: number;
  private readonly mark?: Phaser.GameObjects.Graphics;
  private kin: KinInstance;

  constructor(
    private readonly scene: Phaser.Scene,
    /** The pinned x: the panel's left edge when align='left', its right edge when align='right'. */
    private readonly anchorX: number,
    private readonly y: number,
    kin: KinInstance,
    showNumbers: boolean,
    private readonly align: HpPanelAlign = 'left',
    /** Is this species already caught? Shows the lamp mark beside the bar. */
    private readonly isCaught?: (speciesId: number) => boolean,
  ) {
    this.kin = kin;
    this.height = showNumbers ? 34 : 26;
    this.panel = new Panel(scene, anchorX, this.y, MIN_W, this.height).fixedToCamera();

    this.nameText = makeText(scene, PAD, theme.space.md, '', theme.text.base);
    const barY = 16;
    this.panel.add(this.nameText);

    this.barBg = scene.add
      .rectangle(PAD, barY, BAR_W, BAR_H, hex(theme.color.panelShadow))
      .setOrigin(0, 0)
      .setScrollFactor(0);
    this.bar = scene.add
      .rectangle(PAD, barY, BAR_W, BAR_H, hex(COLORS.grass))
      .setOrigin(0, 0)
      .setScrollFactor(0);
    this.panel.add(this.barBg);
    this.panel.add(this.bar);

    if (isCaught) {
      this.mark = this.drawLampMark(PAD + BAR_W + MARK_GAP, barY - 3);
      this.panel.add(this.mark);
    }

    if (showNumbers) {
      this.hpText = makeText(scene, PAD, barY + 6, '', theme.text.dim);
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
    this.mark?.setVisible(this.isCaught?.(this.kin.species.id) ?? false);
    this.layout();
  }

  /** The lamp mark, pixel by pixel: brass frame (m), warm glow (g), a bright wick (w). */
  private drawLampMark(x: number, y: number): Phaser.GameObjects.Graphics {
    const g = this.scene.add.graphics().setScrollFactor(0).setPosition(x, y);
    const fill: Record<string, number> = {
      m: hex(theme.color.textDim),
      g: hex(theme.color.lampGlow),
      w: hex(theme.color.text),
    };
    LAMP_MARK.forEach((row, py) => [...row].forEach((c, px) => {
      if (fill[c] === undefined) return;
      g.fillStyle(fill[c], 1).fillRect(px, py, 1, 1);
    }));
    return g;
  }

  /** Grow the frame to fit the name+level line and re-pin it to its anchor edge. */
  private layout(): void {
    const markW = this.mark?.visible ? MARK_GAP + MARK_W : 0;
    const w = Math.max(MIN_W + markW, Math.ceil(this.nameText.width) + PAD * 2);
    this.panel.bg.setSize(w, this.height);
    const x = this.align === 'right' ? this.anchorX - w : this.anchorX;
    this.panel.container.setPosition(x, this.y);
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
        duration: 360 * battlePaceFactor(),
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

  /** Hide/show the plate (hidden during the trainer-intro beat, before a kin is out). */
  setVisible(v: boolean): void {
    this.panel.container.setVisible(v);
  }

  destroy(): void {
    this.mark?.destroy();
    this.bar.destroy();
    this.barBg.destroy();
    this.panel.destroy();
  }
}
