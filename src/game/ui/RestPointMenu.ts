/**
 * RestPointMenu — SETTINGS → "Return to rest point": the list of every inn /
 * home / camp fire the player has rested at (newest first), plus a confirm. It's
 * fast travel AND the anti-softlock escape hatch, so it's offered from the very
 * first rest — never gated on the hub or on Gleams.
 *
 * Promise-based: `await new RestPointMenu(scene, points, sfx).run()` resolves with
 * the chosen (and confirmed) RestPoint, or null if the player backed out. It only
 * PICKS — the host (WorldScene) does the journey itself (save, fade, re-enter).
 * Built from the shared kit (Menu windowed via `maxVisible`, DialogueBox, Text).
 */
import Phaser from 'phaser';
import { GAME_WIDTH } from '@game/config';
import { theme } from './theme';
import { makeText } from './Text';
import { Menu } from './Menu';
import { DialogueBox } from './DialogueBox';
import type { Sfx } from '@game/systems/audio/Sfx';
import type { RestPoint } from '@game/data/world/types';
import { restPointLongName } from '@game/systems/world/restPoints';

/** Rows shown at once: title row at y 4, list from y 14, ≤ the 160px screen. */
const VISIBLE_ROWS = 11;
/** Characters that fit a row at the list's width (8px glyphs, cursor gutter). */
const ROW_CHARS = 25;

function fit(label: string): string {
  return label.length <= ROW_CHARS ? label : `${label.slice(0, ROW_CHARS - 2)}..`;
}

export class RestPointMenu {
  constructor(
    private readonly scene: Phaser.Scene,
    /** Travellable points, already newest-first (restPoints.travellableRestPoints). */
    private readonly points: RestPoint[],
    private readonly sfx?: Sfx,
  ) {}

  async run(): Promise<RestPoint | null> {
    if (this.points.length === 0) {
      await new DialogueBox(this.scene, this.sfx).run([
        {
          text: "Your vesperlamp hasn't learned a hearth yet. Rest at an inn or a home, and it will always remember the road back.",
        },
      ]);
      return null;
    }

    let cursor = 0;
    for (;;) {
      const title = makeText(this.scene, GAME_WIDTH / 2, 4, 'RETURN TO A REST POINT', theme.text.accent)
        .setOrigin(0.5, 0)
        .setScrollFactor(0)
        .setDepth(theme.depth.text);
      const choice = await new Menu(
        this.scene,
        this.points.map((p, i) => ({ label: fit(p.label), value: String(i) })),
        {
          x: 8,
          y: 14,
          width: GAME_WIDTH - 16,
          sfx: this.sfx,
          cancellable: true,
          fixed: true,
          maxVisible: VISIBLE_ROWS,
          initialIndex: cursor,
        },
      ).run();
      title.destroy();
      if (choice === null) return null;

      cursor = Number(choice);
      const point = this.points[cursor];
      if (!point) return null;
      if (await this.confirm(point)) return point;
    }
  }

  private async confirm(point: RestPoint): Promise<boolean> {
    await new DialogueBox(this.scene, this.sfx).run([
      {
        text: `Return to ${restPointLongName(point)}? Your journey is written down first, then your vesperlamp lights the road back.`,
      },
    ]);
    const answer = await new Menu(
      this.scene,
      [
        { label: 'STAY HERE', value: 'no' },
        { label: 'TRAVEL', value: 'yes' },
      ],
      { x: 8, y: 8, sfx: this.sfx, cancellable: true },
    ).run();
    return answer === 'yes';
  }
}
