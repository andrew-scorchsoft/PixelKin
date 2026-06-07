/**
 * Menu — a themed vertical list of choices (title menu, battle Fight/Catch/Run,
 * item lists, settings). Promise-based: `await menu.run()` resolves with the chosen
 * value, or null if cancelled. It owns its own input polling so it works from any
 * scene or cutscene without the host running an input loop.
 */
import Phaser from 'phaser';
import { theme } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import type { Sfx } from '@game/systems/audio/Sfx';

export interface MenuOption {
  label: string;
  value: string;
  enabled?: boolean;
}

export interface MenuConfig {
  x: number;
  y: number;
  /** Fixed width; defaults to fit the widest label. */
  width?: number;
  /** Allow cancel (B) to close with null. Default true. */
  cancellable?: boolean;
  sfx?: Sfx;
  /** Pin to camera (HUD/modal). Default true. */
  fixed?: boolean;
}

const ROW_H = 12;
const PAD = theme.space.lg;
const CURSOR_GAP = 8;

export class Menu {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly rows: Phaser.GameObjects.Text[] = [];
  private index = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly options: MenuOption[],
    private readonly config: MenuConfig,
  ) {
    const charW = 8;
    const longest = Math.max(...options.map((o) => o.label.length));
    const width = config.width ?? PAD * 2 + CURSOR_GAP + longest * charW;
    const height = PAD * 2 + options.length * ROW_H;
    this.panel = new Panel(scene, config.x, config.y, width, height);

    options.forEach((opt, i) => {
      const t = makeText(
        scene,
        PAD + CURSOR_GAP,
        PAD + i * ROW_H,
        opt.label,
        opt.enabled === false ? theme.text.dim : theme.text.base,
      );
      this.panel.add(t);
      this.rows.push(t);
    });

    this.cursor = new Cursor(scene);
    this.panel.add(this.cursor.sprite);
    // re-add so cursor renders above rows within the container
    this.panel.container.bringToTop(this.cursor.sprite);

    if (config.fixed !== false) {
      this.panel.fixedToCamera();
      this.cursor.setScrollFactor0();
    }
    this.index = this.firstEnabled(0, 1);
    this.placeCursor();
  }

  private firstEnabled(from: number, dir: number): number {
    let i = from;
    for (let n = 0; n < this.options.length; n++) {
      if (this.options[i]?.enabled !== false) return i;
      i = (i + dir + this.options.length) % this.options.length;
    }
    return from;
  }

  private placeCursor(): void {
    // Cursor is a child of the panel container → use local coords.
    this.cursor.moveTo(PAD, PAD + this.index * ROW_H + 4);
  }

  private move(dir: number): void {
    let i = this.index;
    do {
      i = (i + dir + this.options.length) % this.options.length;
    } while (this.options[i]?.enabled === false && i !== this.index);
    if (i !== this.index) {
      this.index = i;
      this.placeCursor();
      void this.config.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the menu and resolve with the chosen value (or null if cancelled). */
  run(): Promise<string | null> {
    const input = new InputController(this.scene);
    let armed = false; // ignore the keypress that opened this menu until released
    return new Promise((resolve) => {
      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
          return;
        }
        if (input.justPressed(InputAction.Up)) this.move(-1);
        else if (input.justPressed(InputAction.Down)) this.move(1);
        else if (input.justPressed(InputAction.Confirm)) {
          const opt = this.options[this.index];
          if (opt && opt.enabled !== false) {
            void this.config.sfx?.play(theme.cursor.confirmSfx);
            finish(opt.value);
          }
        } else if (input.justPressed(InputAction.Cancel) && this.config.cancellable !== false) {
          void this.config.sfx?.play(theme.cursor.cancelSfx);
          finish(null);
        }
      };
      const finish = (value: string | null): void => {
        this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
        input.destroy();
        this.destroy();
        resolve(value);
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
  }
}
