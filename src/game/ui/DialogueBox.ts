/**
 * DialogueBox — the bottom text box used by signs, NPCs and cutscenes. Reveals each
 * page with a typewriter (hold Confirm to fast-forward; tap to skip to full, then
 * advance), shows a blinking caret when a page is complete, and resolves its promise
 * when the last page is dismissed. Owns its own input so `await box.run(lines)` works
 * anywhere. One consistent look via the theme + Panel.
 *
 * Authors write one `DialogueLine` per *thought*, not per screen: any line too long
 * for the box is auto-paginated here (word-wrapped, then split into box-height pages),
 * so a long message just chunks itself on playback — no need to hand-split it into
 * multiple lines in the JSON.
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
const HEIGHT = 52;
const PAD = theme.space.lg;
/** Body text sits below the speaker-name row. */
const BODY_TOP = PAD + 8;

export class DialogueBox {
  private readonly panel: Panel;
  private readonly body: Phaser.GameObjects.Text;
  private readonly name: Phaser.GameObjects.Text;
  private readonly caret: Phaser.GameObjects.Text;
  private readonly wrapWidth: number;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly sfx?: Sfx,
  ) {
    const width = GAME_WIDTH - MARGIN * 2;
    const y = GAME_HEIGHT - HEIGHT - MARGIN;
    this.panel = new Panel(scene, MARGIN, y, width, HEIGHT).fixedToCamera().setDepth(theme.depth.panel);

    this.wrapWidth = width - PAD * 2;
    this.name = makeText(scene, PAD, PAD - 2, '', theme.text.accent);
    this.body = makeText(scene, PAD, BODY_TOP, '', theme.text.base);
    this.body.setWordWrapWidth(this.wrapWidth);
    this.caret = makeText(scene, width - PAD - 6, HEIGHT - PAD - 6, '▼', theme.text.accent);
    this.panel.add(this.name);
    this.panel.add(this.body);
    this.panel.add(this.caret);
  }

  /**
   * Split an authored line into box-sized pages: word-wrap it to the body width
   * (so we break on word boundaries, never mid-word), then group the wrapped lines
   * into chunks that fit the box vertically. Returns at least one page so an empty
   * line still advances.
   */
  private paginate(line: DialogueLine, maxLines: number): DialogueLine[] {
    const wrapped = this.body.getWrappedText(line.text);
    if (wrapped.length === 0) return [{ speaker: line.speaker, text: '' }];
    const pages: DialogueLine[] = [];
    for (let i = 0; i < wrapped.length; i += maxLines) {
      pages.push({ speaker: line.speaker, text: wrapped.slice(i, i + maxLines).join('\n') });
    }
    return pages;
  }

  /** How many wrapped lines fit in the body area, from the measured font line height. */
  private maxBodyLines(): number {
    const prev = this.body.text;
    this.body.setWordWrapWidth(0); // measure a single unwrapped line
    this.body.setText('Mg');
    const lineHeight = this.body.height;
    this.body.setWordWrapWidth(this.wrapWidth);
    this.body.setText(prev);
    const available = HEIGHT - BODY_TOP - PAD;
    return Math.max(1, Math.floor(available / Math.max(1, lineHeight)));
  }

  /** Show the pages in order; resolve once the last is dismissed. */
  run(lines: DialogueLine[]): Promise<void> {
    const input = new InputController(this.scene);
    let armed = false; // ignore the keypress that opened the box until released

    // Expand each authored line into one-or-more box-sized pages up front.
    const maxLines = this.maxBodyLines();
    const pages: DialogueLine[] = lines.flatMap((line) => this.paginate(line, maxLines));

    let page = 0;
    let shown = 0; // chars revealed
    let acc = 0; // ms accumulator
    let full = '';

    const startPage = (): void => {
      const line = pages[page];
      this.name.setText(line.speaker ?? '');
      full = line.text;
      shown = 0;
      acc = 0;
      this.body.setText('');
      this.caret.setVisible(false);
    };

    return new Promise((resolve) => {
      if (pages.length === 0) {
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
            if (page >= pages.length) {
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
