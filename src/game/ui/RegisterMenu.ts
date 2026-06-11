/**
 * RegisterMenu — the vesperlamp's register (pause menu -> REGISTER): the
 * collection screen. Every kin of Vesperholm has a numbered line; ones you've
 * met show their name, ones that walk with you (caught) carry the lamp mark ●,
 * and the rest are an unmet "-----" the screen quietly dares you to fill in.
 *
 * Windowed list + detail pane (the GlossaryMenu/StarterSelect pattern): Up/Down
 * scroll the full 159, the pane below shows the selected kin — icon (lazy-loaded
 * via CreatureSprites; silhouetted until caught), types, dex category and, once
 * caught, the full register entry. The header keeps the score: SEEN n · KEPT m.
 * Read-only and promise-based; built from the shared kit + theme tokens.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { loadCreatureSprite, hasCreatureSprite } from '@game/systems/sprites/CreatureSprites';
import { SPECIES } from '@game/data/dex';
import type { Species } from '@game/data/dex';
import type { DexProgress } from '@game/systems/save/types';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const HEADER_H = 12;
const ROW_H = 12;
const DETAIL_LINE_H = 9;
const DETAIL_LINES = 5;
const ICON_BOX = 34; // detail-pane icon slot (icons are 32x32)
const UNMET = '-----';

interface Row {
  species: Species;
  seen: boolean;
  caught: boolean;
}

export class RegisterMenu {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly rows: Row[];
  private readonly rowTexts: Phaser.GameObjects.Text[] = [];
  private readonly detail: Phaser.GameObjects.Text;
  private readonly detailIcon: Phaser.GameObjects.Image;
  private readonly moreUp: Phaser.GameObjects.Text;
  private readonly moreDown: Phaser.GameObjects.Text;
  private readonly listTop: number;
  private readonly visibleRows: number;
  private index = 0;
  private scroll = 0;
  private destroyed = false;

  constructor(
    private readonly scene: Phaser.Scene,
    dex: DexProgress,
    private readonly sfx?: Sfx,
  ) {
    const seen = new Set(dex.seen);
    const caught = new Set(dex.caught);
    this.rows = [...SPECIES]
      .sort((a, b) => a.id - b.id)
      .map((species) => ({
        species,
        seen: seen.has(species.id) || caught.has(species.id),
        caught: caught.has(species.id),
      }));

    const width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.listTop = PAD + HEADER_H;
    const detailTop = height - PAD - DETAIL_LINES * DETAIL_LINE_H;
    const sepY = detailTop - 4;
    const listSpace = sepY - this.listTop;
    this.visibleRows = Math.max(1, Math.floor(listSpace / ROW_H));

    this.panel = new Panel(scene, 4, 4, width, height).fixedToCamera().setDepth(theme.depth.panel);

    const seenCount = this.rows.filter((r) => r.seen).length;
    const caughtCount = this.rows.filter((r) => r.caught).length;
    this.panel.add(makeText(scene, PAD, PAD - 2, 'THE REGISTER', theme.text.accent));
    this.panel.add(
      makeText(scene, width - PAD, PAD - 2, `SEEN ${seenCount} · KEPT ${caughtCount}`, theme.text.dim).setOrigin(1, 0),
    );

    for (let i = 0; i < this.visibleRows; i++) {
      const t = makeText(scene, PAD + 10, this.listTop + i * ROW_H + 3, '', theme.text.base);
      this.panel.add(t);
      this.rowTexts.push(t);
    }

    this.moreUp = makeText(scene, width - PAD, this.listTop - 1, '^', theme.text.dim).setOrigin(1, 0);
    this.moreDown = makeText(scene, width - PAD, sepY - DETAIL_LINE_H, 'v', theme.text.dim).setOrigin(1, 0);
    this.panel.add(this.moreUp);
    this.panel.add(this.moreDown);

    const sep = scene.add
      .rectangle(PAD, sepY, width - PAD * 2, 1, hex(theme.color.panelEdge))
      .setOrigin(0, 0)
      .setAlpha(0.5);
    this.panel.add(sep);

    // Detail: the kin's icon to the left, wrapped text to the right.
    this.detailIcon = scene.add
      .image(PAD + ICON_BOX / 2, detailTop + ICON_BOX / 2 + 2, '__MISSING')
      .setVisible(false);
    this.panel.add(this.detailIcon);
    this.detail = makeText(scene, PAD + ICON_BOX + 6, detailTop, '', theme.text.dim);
    this.detail.setWordWrapWidth(width - PAD * 2 - ICON_BOX - 6);
    this.panel.add(this.detail);

    this.cursor = new Cursor(scene).setScrollFactor0();
    this.panel.add(this.cursor.sprite);

    this.refresh();
  }

  private label(row: Row): string {
    const num = `No.${String(row.species.id).padStart(3, '0')}`;
    if (!row.seen) return `${num}  ${UNMET}`;
    return `${num}  ${row.species.name.toUpperCase()}${row.caught ? ' ●' : ''}`;
  }

  private refresh(): void {
    if (this.index < this.scroll) this.scroll = this.index;
    else if (this.index >= this.scroll + this.visibleRows) this.scroll = this.index - this.visibleRows + 1;

    this.rowTexts.forEach((t, i) => {
      const row = this.rows[this.scroll + i];
      if (!row) {
        t.setText('');
        return;
      }
      const selected = this.scroll + i === this.index;
      t.setText(this.label(row));
      t.setColor(
        selected ? theme.text.accent.color : row.seen ? theme.text.base.color : theme.text.dim.color,
      );
    });

    this.cursor.moveTo(PAD, this.listTop + (this.index - this.scroll) * ROW_H + ROW_H / 2);
    this.moreUp.setVisible(this.scroll > 0);
    this.moreDown.setVisible(this.scroll + this.visibleRows < this.rows.length);
    this.refreshDetail();
  }

  private refreshDetail(): void {
    const row = this.rows[this.index];
    this.detailIcon.setVisible(false);
    if (!row || !row.seen) {
      this.detail.setText(row ? 'Not yet met. Somewhere in the dusk, it is waiting.' : '');
      return;
    }

    const s = row.species;
    const types = s.types.join(' / ');
    if (row.caught) {
      this.detail.setText(`${s.name} — ${s.dex.category}\n${types}\n${s.dex.entry}`);
    } else {
      this.detail.setText(`${s.name} — ${s.dex.category}\n${types}\nCatch one, and the register will hold its story.`);
    }

    // Lazy icon: full colour once caught, a dark silhouette when merely seen.
    if (hasCreatureSprite(s.id, 'icon')) {
      const wantedId = s.id;
      void loadCreatureSprite(this.scene, s.id, 'icon').then((key) => {
        // The cursor may have moved (or the screen closed) while loading.
        if (this.destroyed || key === null || this.rows[this.index]?.species.id !== wantedId) return;
        this.detailIcon.setTexture(key).setVisible(true);
        if (row.caught) this.detailIcon.clearTint();
        else this.detailIcon.setTintFill(hex(theme.color.panelShadow));
      });
    }
  }

  private move(dir: number): void {
    const next = Math.min(this.rows.length - 1, Math.max(0, this.index + dir));
    if (next !== this.index) {
      this.index = next;
      this.refresh();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the register; resolve when the player backs out. */
  run(): Promise<void> {
    const input = new InputController(this.scene);
    let armed = false;
    return new Promise((resolve) => {
      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm) && !input.isDown(InputAction.Cancel)) armed = true;
          return;
        }
        // Left/Right leap a whole window — 159 lines is a long walk one row at a time.
        if (input.justPressed(InputAction.Up)) this.move(-1);
        else if (input.justPressed(InputAction.Down)) this.move(1);
        else if (input.justPressed(InputAction.Left)) this.move(-this.visibleRows);
        else if (input.justPressed(InputAction.Right)) this.move(this.visibleRows);
        else if (input.justPressed(InputAction.Cancel) || input.justPressed(InputAction.Confirm)) {
          void this.sfx?.play(theme.cursor.cancelSfx);
          this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
          input.destroy();
          this.destroy();
          resolve();
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.destroyed = true;
    this.cursor.destroy();
    this.panel.destroy();
  }
}
