/**
 * DialogueBox — the bottom text box used by signs, NPCs and cutscenes. Reveals each
 * page with a typewriter (hold Confirm to fast-forward; tap to skip to full, then
 * advance), shows a blinking caret when a page is complete, and resolves its promise
 * when the last page is dismissed. Owns its own input so `await box.run(lines)` works
 * anywhere. One consistent look via the theme + Panel.
 *
 * A line may carry a character `portrait` (a 32×32 bust drawn top-left, the body
 * text reflowing beside it) and/or `style: 'narrate'` (un-attributed, softer prose
 * for cold-open / cutscene narration). Both are additive: a missing portrait or a
 * plain `{speaker,text}` line renders exactly as before.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { resolvePortrait } from '@game/content/portraits';
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
  private readonly width: number;
  private portrait?: Phaser.GameObjects.Image;
  private input?: InputController;
  private tickFn?: () => void;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly sfx?: Sfx,
  ) {
    this.width = GAME_WIDTH - MARGIN * 2;
    const y = GAME_HEIGHT - HEIGHT - MARGIN;
    this.panel = new Panel(scene, MARGIN, y, this.width, HEIGHT).fixedToCamera().setDepth(theme.depth.panel);

    this.name = makeText(scene, PAD, PAD - 2, '', theme.text.accent);
    this.body = makeText(scene, PAD, PAD + 8, '', theme.text.base);
    this.caret = makeText(scene, this.width - PAD - 6, HEIGHT - PAD - 6, '▼', theme.text.accent);
    this.panel.add(this.name);
    this.panel.add(this.body);
    this.panel.add(this.caret);
  }

  /** Position the portrait / name / body and the body wrap for this page's layout. */
  private layout(line: DialogueLine): { cps: number; fastCps: number } {
    const narrate = line.style === 'narrate';
    const pr = narrate ? undefined : resolvePortrait(line.portrait, line.expr);

    // Portrait bust, vertically centred at the box's left edge when present.
    if (pr && this.scene.textures.exists(pr.def.id)) {
      const size = theme.portrait.size;
      const py = Math.round((HEIGHT - size) / 2);
      if (!this.portrait) {
        this.portrait = this.scene.add.image(theme.portrait.inset, py, pr.def.id, pr.frame).setOrigin(0, 0);
        this.panel.add(this.portrait);
      }
      this.portrait.setTexture(pr.def.id, pr.frame).setVisible(true);
    } else {
      this.portrait?.setVisible(false);
    }

    const textLeft = this.portrait?.visible ? theme.portrait.inset + theme.portrait.size + theme.portrait.gap : PAD;
    this.name.setX(textLeft);
    this.body.setX(textLeft);
    this.body.setWordWrapWidth(this.width - textLeft - PAD);

    if (narrate) {
      this.name.setVisible(false);
      this.body.setStyle(theme.text.narrate).setY(PAD + 4);
      return { cps: theme.typewriter.narrateCps, fastCps: theme.typewriter.fastCps };
    }
    this.name.setVisible(true);
    this.body.setStyle(theme.text.base).setY(PAD + 8);
    return { cps: theme.typewriter.cps, fastCps: theme.typewriter.fastCps };
  }

  /** Show the pages in order; resolve once the last is dismissed. */
  run(lines: DialogueLine[]): Promise<void> {
    const input = new InputController(this.scene);
    this.input = input;
    let armed = false; // ignore the keypress that opened the box until released
    let page = 0;
    let shown = 0; // chars revealed
    let acc = 0; // ms accumulator
    let full = '';
    let speed: { cps: number; fastCps: number } = { cps: theme.typewriter.cps, fastCps: theme.typewriter.fastCps };

    const startPage = (): void => {
      const line = lines[page];
      speed = this.layout(line);
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
            const cps = input.isDown(InputAction.Confirm) ? speed.fastCps : speed.cps;
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
      this.tickFn = tick;
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  /** Tear down UI + input. Safe to call mid-run (e.g. a cold open skipped mid-page),
   *  which the normal completion path also does once the last page is dismissed. */
  destroy(): void {
    if (this.tickFn) {
      this.scene.events.off(Phaser.Scenes.Events.UPDATE, this.tickFn);
      this.tickFn = undefined;
    }
    this.input?.destroy();
    this.input = undefined;
    this.portrait?.destroy();
    this.panel.destroy();
  }
}
