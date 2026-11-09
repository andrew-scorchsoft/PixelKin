/**
 * DialogueBox — the bottom text box used by signs, NPCs and cutscenes. Reveals each
 * page with a typewriter (hold Confirm to fast-forward; tap to skip to full, then
 * advance), shows a blinking caret when a page is complete, and resolves its promise
 * when the last page is dismissed. Owns its own input so `await box.run(lines)` works
 * anywhere. One consistent look via the theme + Panel.
 *
 * Authors write one `DialogueLine` per *thought*, not per screen: any line too long
 * for the box is auto-paginated here (word-wrapped, then split into box-height pages),
 * so a long message just chunks itself on playback — no need to hand-split it.
 *
 * A line may also carry a character `portrait` (a 32×32 bust drawn top-left, the body
 * text reflowing — and paginating — beside it) and/or `style: 'narrate'` (un-attributed,
 * softer prose for cold-open / cutscene narration). Both are additive: a missing portrait
 * or a plain `{speaker,text}` line renders exactly as before.
 *
 * Text wrapped in `[[double brackets]]` is KEY INFORMATION (where to go, who to see,
 * what to bring): it's drawn underlined in lamp-gold, revealed with the typewriter.
 * PressStart2P is monospace, so a marked run is simply columns × glyph width: the
 * base text blanks those cells and a gold overlay draws them (ui/textMarks.ts,
 * docs/world/dialogue-rubric.md §6).
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { resolvePortrait } from '@game/content/portraits';
import { textSpeedMultiplier } from './preferences';
import { parseMarks, runsForRows, type MarkRun } from './textMarks';
import type { DialogueLine } from '@game/content/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const MARGIN = 6;
const HEIGHT = 52;
const PAD = theme.space.lg;
/** Body text sits below the speaker-name row. */
const BODY_TOP = PAD + 8;

/** A box-sized page: the line's attributes, its wrapped rows, and its key-info runs. */
type Page = DialogueLine & { runs: MarkRun[] };

export class DialogueBox {
  private readonly panel: Panel;
  private readonly body: Phaser.GameObjects.Text;
  private readonly name: Phaser.GameObjects.Text;
  private readonly caret: Phaser.GameObjects.Text;
  private readonly width: number;
  private portrait?: Phaser.GameObjects.Image;
  /** Key-information overlay: gold glyphs + underline for the current page's marks. */
  private readonly underline: Phaser.GameObjects.Graphics;
  private markTexts: Phaser.GameObjects.Text[] = [];
  private glyph = { w: 8, h: 8 };
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
    this.body = makeText(scene, PAD, BODY_TOP, '', theme.text.base);
    this.body.setWordWrapWidth(this.width - PAD * 2);
    this.caret = makeText(scene, this.width - PAD - 6, HEIGHT - PAD - 6, '▼', theme.text.accent);
    this.panel.add(this.name);
    this.panel.add(this.body);
    this.panel.add(this.caret);
    this.underline = scene.add.graphics();
    this.panel.add(this.underline);
  }

  /** The portrait bust to show for a line, if one resolves and its texture is loaded. */
  private portraitFor(line: DialogueLine): { def: { id: string }; frame: number } | undefined {
    if (line.style === 'narrate') return undefined;
    const pr = resolvePortrait(line.portrait, line.expr);
    return pr && this.scene.textures.exists(pr.def.id) ? pr : undefined;
  }

  /** Left edge of the text column — shifted right when a portrait bust is present. */
  private textLeft(pr: { def: { id: string } } | undefined): number {
    return pr ? theme.portrait.inset + theme.portrait.size + theme.portrait.gap : PAD;
  }

  /** Body word-wrap width for a line (narrower when a portrait sits to its left). */
  private bodyWrap(pr: { def: { id: string } } | undefined): number {
    return this.width - this.textLeft(pr) - PAD;
  }

  /**
   * Split an authored line into box-sized pages: word-wrap it to the line's body width
   * (so we break on word boundaries, never mid-word), then group the wrapped lines into
   * chunks that fit the box vertically. Carries the line's speaker/portrait/style onto
   * every page. Returns at least one page so an empty line still advances.
   */
  private paginate(line: DialogueLine, maxLines: number): Page[] {
    const { plain, marked } = parseMarks(line.text);
    this.body.setWordWrapWidth(this.bodyWrap(this.portraitFor(line)));
    const wrapped = this.body.getWrappedText(plain);
    if (wrapped.length === 0) return [{ ...line, text: '', runs: [] }];
    const pages: Page[] = [];
    let from = 0;
    for (let i = 0; i < wrapped.length; i += maxLines) {
      const rows = wrapped.slice(i, i + maxLines);
      const { runs, next } = runsForRows(plain, marked, rows, from);
      from = next;
      pages.push({ ...line, text: rows.join('\n'), runs });
    }
    return pages;
  }

  /** Blank the marked cells of a page so the gold overlay is the only glyph there. */
  private static blankRuns(text: string, runs: MarkRun[]): string {
    if (runs.length === 0) return text;
    const chars = text.split('');
    for (const r of runs) for (let i = 0; i < r.end - r.start; i++) chars[r.offset + i] = ' ';
    return chars.join('');
  }

  /** Lay out one gold overlay Text per marked run of a new page. */
  private startMarks(page: Page): void {
    for (const t of this.markTexts) t.destroy();
    this.markTexts = page.runs.map((r) => {
      const t = makeText(this.scene, this.body.x + r.start * this.glyph.w, this.body.y + r.row * this.glyph.h, '', theme.text.key);
      this.panel.add(t);
      return t;
    });
    this.underline.clear();
  }

  /** Reveal the marked runs up to the typewriter's `shown` character. */
  private drawMarks(page: Page, shown: number): void {
    if (page.runs.length === 0) return;
    const rows = page.text.split('\n');
    this.underline.clear();
    this.underline.fillStyle(Phaser.Display.Color.HexStringToColor(theme.color.keyInfoRule).color, 1);
    page.runs.forEach((r, i) => {
      const vis = Math.max(0, Math.min(r.end - r.start, shown - r.offset));
      this.markTexts[i]?.setText(rows[r.row].slice(r.start, r.start + vis));
      if (vis > 0) {
        const x = this.body.x + r.start * this.glyph.w;
        // Rows sit flush (8px font, 8px rows), so the rule lives in the glyph cell's
        // blank bottom row and is a deeper amber than the glyphs: it reads as a rule,
        // never as the top stroke of a letter on the row below.
        const y = this.body.y + r.row * this.glyph.h + this.glyph.h - 1;
        this.underline.fillRect(x, y, vis * this.glyph.w, 1);
      }
    });
  }

  /** How many wrapped lines fit in the body area, from the measured font line height. */
  private maxBodyLines(): number {
    const prev = this.body.text;
    this.body.setWordWrapWidth(0); // measure a single unwrapped line
    this.body.setText('M');
    this.glyph.w = this.body.width; // PressStart2P is monospace
    this.body.setText('Mg');
    const lineHeight = this.body.height;
    this.glyph.h = lineHeight;
    this.body.setWordWrapWidth(this.width - PAD * 2);
    this.body.setText(prev);
    const available = HEIGHT - BODY_TOP - PAD;
    return Math.max(1, Math.floor(available / Math.max(1, lineHeight)));
  }

  /** Position the portrait / name / body for this page and pick the typewriter speed. */
  private layout(line: DialogueLine): { cps: number; fastCps: number } {
    const pr = this.portraitFor(line);

    // Portrait bust, vertically centred at the box's left edge when present.
    if (pr) {
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

    const left = this.textLeft(pr);
    this.name.setX(left);
    this.body.setX(left);

    let speed: { cps: number; fastCps: number };
    if (line.style === 'narrate') {
      this.name.setVisible(false);
      this.body.setStyle(theme.text.narrate);
      speed = { cps: theme.typewriter.narrateCps, fastCps: theme.typewriter.fastCps };
    } else {
      this.name.setVisible(true);
      this.body.setStyle(theme.text.base);
      speed = { cps: theme.typewriter.cps, fastCps: theme.typewriter.fastCps };
    }
    // Pages arrive pre-wrapped (paginate), so the body draws them as-is: no re-wrap
    // that could fold a row whose key-info cells are blanked to spaces. Set AFTER
    // setStyle (which replaces the style config) so it sticks.
    this.body.setWordWrapWidth(null);
    return speed;
  }

  /** Show the pages in order; resolve once the last is dismissed. */
  run(lines: DialogueLine[]): Promise<void> {
    const input = new InputController(this.scene);
    this.input = input;
    let armed = false; // ignore the keypress that opened the box until released

    // Expand each authored line into one-or-more box-sized pages up front.
    const maxLines = this.maxBodyLines();
    const pages: Page[] = lines.flatMap((line) => this.paginate(line, maxLines));

    let page = 0;
    let shown = 0; // chars revealed
    let acc = 0; // ms accumulator
    let full = '';
    let speed: { cps: number; fastCps: number } = { cps: theme.typewriter.cps, fastCps: theme.typewriter.fastCps };

    const startPage = (): void => {
      const line = pages[page];
      speed = this.layout(line);
      this.name.setText(line.speaker ?? '');
      full = DialogueBox.blankRuns(line.text, line.runs);
      shown = 0;
      acc = 0;
      this.body.setText('');
      this.startMarks(line);
      this.caret.setVisible(false);
    };

    return new Promise((resolve) => {
      if (pages.length === 0) {
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
          if (input.justPressed(InputAction.Confirm) || textSpeedMultiplier() === Number.POSITIVE_INFINITY) {
            shown = full.length;
          } else {
            const cps =
              (input.isDown(InputAction.Confirm) ? speed.fastCps : speed.cps) * textSpeedMultiplier();
            acc += this.scene.game.loop.delta;
            const reveal = Math.floor((acc / 1000) * cps);
            if (reveal > shown) {
              shown = Math.min(full.length, reveal);
              void this.sfx?.play('ui-text-blip');
            }
          }
          this.body.setText(full.slice(0, shown));
          this.drawMarks(pages[page], shown);
          if (shown >= full.length) this.caret.setVisible(true);
        } else {
          this.caret.setVisible(true);
          if (input.justPressed(InputAction.Confirm)) {
            void this.sfx?.play(theme.cursor.confirmSfx);
            page++;
            if (page >= pages.length) {
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
