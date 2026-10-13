/**
 * MoveInfo — the "what does this move do?" pane beside the battle FIGHT menu.
 * OPT-IN (owner's call): it covers part of the foe, so FIGHT opens without it and
 * RIGHT shows it / LEFT hides it (BattleScene.fightMenu; the choice holds for the
 * rest of that battle).
 * As the cursor lands on a move it shows, in plain words: the move's type (in its
 * type colour), PHYSICAL / SPECIAL / STATUS, power, accuracy and the charges left,
 * and — only against a foe whose species you've CAUGHT (an earned hint, as before)
 * — how well it lands on that foe. The move's description goes in the battle
 * message strip underneath (BattleScene.fightMenu), so between them a player
 * never has to guess. Built from the shared Panel + Text + theme tokens.
 */
import Phaser from 'phaser';
import { theme } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { Panel } from '@game/ui/Panel';

const PAD = theme.space.lg;
/** Line pitch: the 8px font with a pixel of air. */
const LINE_H = 9;
/** Top inset: six lines at the 9px pitch fill the 60px pane with a pixel to spare. */
const TOP = theme.space.md;

export interface MoveInfoData {
  type: string;
  category: string;
  power: number;
  accuracy: number;
  charges: number;
  maxCharges: number;
  /** Damage multiplier vs the foe, or undefined when the hint isn't earned yet. */
  effect?: number;
}

const CATEGORY: Record<string, string> = { physical: 'PHYSICAL', special: 'SPECIAL', status: 'STATUS' };

export class MoveInfo {
  private readonly panel: Panel;
  private readonly lines: Phaser.GameObjects.Text[] = [];

  constructor(scene: Phaser.Scene, x: number, y: number, width: number, height: number) {
    // One band above the move list: when open it sits over the list's uses column.
    this.panel = new Panel(scene, x, y, width, height).fixedToCamera().setDepth(theme.depth.panel + 1);
    for (let i = 0; i < 6; i++) {
      const t = makeText(scene, PAD, TOP + i * LINE_H, '', theme.text.base);
      this.panel.add(t);
      this.lines.push(t);
    }
  }

  show(m: MoveInfoData): void {
    const [type, cat, pow, acc, uses, eff] = this.lines;
    type.setText(m.type.toUpperCase()).setColor(
      (theme.typeColor as Record<string, string>)[m.type] ?? theme.color.text,
    );
    cat.setText(CATEGORY[m.category] ?? m.category.toUpperCase()).setColor(theme.color.textDim);
    pow.setText(`POW ${m.power > 0 ? m.power : '--'}`);
    acc.setText(`ACC ${m.accuracy > 0 ? m.accuracy : '--'}`);
    uses.setText(`USES ${m.charges}/${m.maxCharges}`)
      .setColor(m.charges > 0 ? theme.color.text : theme.color.danger);
    const verdict = m.effect === undefined || m.category === 'status' || m.power <= 0
      ? null
      : m.effect === 0 ? ['NO EFFECT', theme.color.textDim]
        : m.effect > 1 ? ['SUPER!', theme.color.hpHigh]
          : m.effect < 1 ? ['RESISTED', theme.color.danger]
            : ['NEUTRAL', theme.color.textAccent];
    eff.setText(verdict?.[0] ?? '').setColor(verdict?.[1] ?? theme.color.text);
  }

  /** Show/hide the pane (it's opt-in: hidden until the player asks with RIGHT). */
  setVisible(v: boolean): void {
    this.panel.container.setVisible(v);
  }

  destroy(): void {
    this.panel.destroy();
  }
}
