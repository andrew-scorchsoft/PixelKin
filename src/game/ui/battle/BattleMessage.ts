/**
 * BattleMessage — the persistent text strip along the bottom of a battle. Unlike
 * DialogueBox (which is modal, per-conversation), this one lives for the whole
 * fight and shows fast, mostly auto-advancing combat lines ("Vulpyre used Ember
 * Jab!"). `show(text)` resolves after a short beat (or immediately on Confirm),
 * so the scene can `await` each beat of a turn. Built from the shared Panel/Text.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme } from '@game/ui/theme';
import { makeText } from '@game/ui/Text';
import { Panel } from '@game/ui/Panel';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { battlePaceFactor } from '@game/ui/preferences';

const MARGIN = 4;
const HEIGHT = 34;
const PAD = theme.space.lg;
/** How long an auto-advancing line lingers before resolving (ms) at cosy pace;
 *  scaled by the Settings battle-pace factor (×0.5 on Swift). */
const HOLD_MS = 650;

export class BattleMessage {
  private readonly panel: Panel;
  private readonly body: Phaser.GameObjects.Text;
  private readonly input: InputController;

  constructor(private readonly scene: Phaser.Scene) {
    const width = GAME_WIDTH - MARGIN * 2;
    const y = GAME_HEIGHT - HEIGHT - MARGIN;
    this.panel = new Panel(scene, MARGIN, y, width, HEIGHT).fixedToCamera().setDepth(theme.depth.panel);
    this.body = makeText(scene, PAD, PAD, '', theme.text.base);
    this.body.setWordWrapWidth(width - PAD * 2);
    this.panel.add(this.body);
    this.input = new InputController(scene);
  }

  /** Set text without waiting (used while a sub-menu is open). */
  set(text: string): void {
    this.body.setText(text);
  }

  /**
   * Show a line and resolve after a short hold, or as soon as the player taps
   * Confirm. `wait:false` resolves on the next frame (for chained quick lines).
   */
  show(text: string, opts: { wait?: boolean } = {}): Promise<void> {
    this.body.setText(text);
    const wait = opts.wait !== false;
    return new Promise((resolve) => {
      let elapsed = 0;
      let armed = false;
      const tick = (): void => {
        this.input.update();
        if (!armed) {
          if (!this.input.isDown(InputAction.Confirm)) armed = true;
        } else if (this.input.justPressed(InputAction.Confirm)) {
          finish();
          return;
        }
        if (wait) {
          elapsed += this.scene.game.loop.delta;
          if (elapsed >= HOLD_MS * battlePaceFactor()) finish();
        } else if (elapsed++ > 0) {
          finish();
        }
      };
      const finish = (): void => {
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        resolve();
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  setVisible(v: boolean): void {
    this.panel.setVisible(v);
  }

  destroy(): void {
    this.panel.destroy();
  }
}
