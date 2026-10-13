/**
 * PagedText — a word-wrapped Text held to a fixed number of lines. Anything
 * longer is split into pages that turn by themselves every few seconds, with a
 * small "n/m" marker, so a description is never cut off at a pane's edge however
 * long it runs (the detail panes of ITEMS, the Register, the Journal, the LORE
 * codex, the Charts, Travel and the Gleams all used to spill off the screen).
 *
 * The caller owns the Text (its position, style and wrap width) and where the
 * marker sits; PagedText only decides what's showing.
 */
import Phaser from 'phaser';
import { theme } from './theme';
import { makeText } from './Text';

/** How long each page holds before turning (ms). */
const PAGE_MS = 2800;

export class PagedText {
  private timer?: Phaser.Time.TimerEvent;
  readonly marker: Phaser.GameObjects.Text;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly text: Phaser.GameObjects.Text,
    private readonly maxLines: number,
    /** Line pitch in px: the 8px font plus this much air. */
    lineH = 9,
    /** Where the "n/m" marker's RIGHT edge sits (same coordinate space as `text`). */
    marker?: { x: number; y: number },
  ) {
    text.setLineSpacing(lineH - 8);
    this.marker = makeText(scene, marker?.x ?? 0, marker?.y ?? 0, '', theme.text.dim)
      .setOrigin(1, 0.5)
      .setBackgroundColor(theme.color.panelFill)
      .setPadding(2, 0, 0, 0)
      .setVisible(false);
  }

  /** Show `value`, paging it when it wraps past the line budget. */
  set(value: string): void {
    this.timer?.remove();
    this.timer = undefined;
    const lines = this.text.getWrappedText(value);
    const pages: string[] = [];
    for (let i = 0; i < lines.length; i += this.maxLines) {
      pages.push(lines.slice(i, i + this.maxLines).join('\n'));
    }
    let page = 0;
    const show = (): void => {
      this.text.setText(pages[page] ?? '');
      this.marker.setText(`${page + 1}/${pages.length}`).setVisible(pages.length > 1);
    };
    show();
    if (pages.length > 1) {
      this.timer = this.scene.time.addEvent({
        delay: PAGE_MS,
        loop: true,
        callback: () => {
          page = (page + 1) % pages.length;
          show();
        },
      });
    }
  }

  destroy(): void {
    this.timer?.remove();
    this.marker.destroy();
  }
}
