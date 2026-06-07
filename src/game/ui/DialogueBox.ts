/**
 * DialogueBox — the bottom text box used by signs, NPCs and cutscenes. Reveals each
 * page with a typewriter (hold Confirm to fast-forward; tap to skip to full, then
 * advance), shows a blinking caret when a page is complete, and resolves its promise
 * when the last page is dismissed. Owns its own input so `await box.run(lines)` works
 * anywhere. One consistent look via the theme + Panel.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { InputController, InputAction } from '@game/systems/input/InputController';
import type { DialogueLine } from '@game/content/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const MARGIN = 6;
const HEIGHT = 46;
const PAD = theme.space.lg;

export class DialogueBox {
  private readonly panel: Panel;
  private readonly body: Phaser.GameObjects.Text;
  private readonly name: Phaser.GameObjects.Text;
  private readonly caret: Phaser.GameObjects.Text;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly sfx?: Sfx,
  ) {
    const width = GAME_WIDTH - MARGIN * 2;
    const y = GAME_HEIGHT - HEIGHT - MARGIN;
    this.panel = new Panel(scene, MARGIN, y, width, HEIGHT).fixedToCamera().setDepth(theme.depth.panel);

    this.name = makeText(scene, PAD, PAD - 2, '', theme.text.accent);
    this.body = makeText(scene, PAD, PAD + 8, '', theme.text.base);
    this.body.setWordWrapWidth(width - PAD * 2);
    this.caret = makeText(scene, width - PAD - 6, HEIGHT - PAD - 6, '▼', theme.text.accent);
    this.panel.add(this.name);
    this.panel.add(this.body);
    this.panel.add(this.caret);
  }

  /** Show the pages in order; resolve once the last is dismissed. */
  run(lines: DialogueLine[]): Promise<void> {
    const input = new InputController(this.scene);
    let armed = false; // ignore the keypress that opened the box until released
    let page = 0;
    let shown = 0; // chars revealed
    let acc = 0; // ms accumulator
    let full = '';

    const startPage = (): void => {
      const line = lines[page];
      this.name.setText(line.speaker ?? '');
      full = line.text;
      shown = 0;
      acc = 0;
      this.body.setText('');
      this.caret.setVisible(false);
    };

    return new Promise((resolve) => {
      if (lines.length === 0) {
        input.destroy();
        this.destroy();
        resolve();
        return;
      }
      startPage();

      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm)) armed = true;
          return;
        }
        const complete = shown >= full.length;

        if (!complete) {
          // Typewriter; hold confirm to speed up, tap to complete instantly.
          if (input.justPressed(InputAction.Confirm)) {
            shown = full.length;
          } else {
            const cps = input.isDown(InputAction.Confirm) ? theme.typewriter.fastCps : theme.typewriter.cps;
            acc += this.scene.game.loop.delta;
            const reveal = Math.floor((acc / 1000) * cps);
            if (reveal > shown) {
              shown = Math.min(full.length, reveal);
              void this.sfx?.play('ui-text-blip');
            }
          }
          this.body.setText(full.slice(0, shown));
          if (shown >= full.length) this.caret.setVisible(true);
        } else {
          this.caret.setVisible(true);
          if (input.justPressed(InputAction.Confirm)) {
            void this.sfx?.play(theme.cursor.confirmSfx);
            page++;
            if (page >= lines.length) {
              this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
              input.destroy();
              this.destroy();
              resolve();
              return;
            }
            startPage();
          }
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.panel.destroy();
  }
}
