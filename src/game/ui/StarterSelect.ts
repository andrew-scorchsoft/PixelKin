/**
 * StarterSelect — the choose-your-companion screen shown in the intro cutscene.
 * Lists the founding trio as compact rows (icon + name + type), with a detail
 * pane below that shows only the *selected* starter's blurb and updates as the
 * cursor moves — so long descriptions never overlap the list and the choice stays
 * in view, using the small screen well. up/down + Confirm picks one (not
 * cancellable — you must choose). Promise-based: resolves with the chosen species
 * id. Built from the shared kit so it matches every other screen. Real portraits
 * drop in later (creature art isn't packed to public/ yet); for now each option
 * shows a type-tinted swatch.
 */
import Phaser from 'phaser';
import { GAME_WIDTH } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { Cursor } from './Cursor';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { SPECIES_BY_ID, type KinType } from '@game/data/dex';
import { STARTERS } from '@game/content/starters';
import { hasCreatureSprite, loadCreatureSprite } from '@game/systems/sprites/CreatureSprites';
import type { Sfx } from '@game/systems/audio/Sfx';

const TYPE_TINT: Partial<Record<KinType, string>> = {
  Ember: '#ff8a3d',
  Tide: '#4fb4ff',
  Verdant: '#7bdc6b',
};

const PAD = theme.space.lg;
/** One compact list row: just enough for the 16px icon + a name line. */
const ROW_H = 20;
/** Vertical room reserved for the header line. */
const HEADER_H = 12;
/** Detail pane: lines × line-height, sized for the longest blurb so nothing clips. */
const DETAIL_LINE_H = 9;
const DETAIL_LINES = 4;

export class StarterSelect {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly swatches: Phaser.GameObjects.Rectangle[] = [];
  private readonly names: Phaser.GameObjects.Text[] = [];
  private readonly detail: Phaser.GameObjects.Text;
  private readonly listTop: number;
  private index = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly sfx?: Sfx,
  ) {
    const width = GAME_WIDTH - 24;
    this.listTop = PAD + HEADER_H;
    const detailTop = this.listTop + STARTERS.length * ROW_H + PAD;
    const height = detailTop + DETAIL_LINES * DETAIL_LINE_H + PAD;
    const x = (GAME_WIDTH - width) / 2;
    const y = 12;
    this.panel = new Panel(scene, x, y, width, height).fixedToCamera().setDepth(theme.depth.panel);

    this.panel.add(makeText(scene, PAD, PAD - 2, 'CHOOSE A COMPANION', theme.text.accent));

    STARTERS.forEach((opt, i) => {
      const species = SPECIES_BY_ID.get(opt.species_id);
      const rowY = this.listTop + i * ROW_H;
      const type = species?.types[0];
      const tint = (type && TYPE_TINT[type]) || theme.color.panelEdge;

      const swatch = scene.add
        .rectangle(PAD + 10, rowY + 2, 16, 16, hex(tint))
        .setOrigin(0, 0)
        .setStrokeStyle(1, hex(theme.color.panelShadow));
      this.panel.add(swatch);
      this.swatches.push(swatch);

      // Swap the swatch for the real kin icon once it loads.
      if (hasCreatureSprite(opt.species_id, 'icon')) {
        void loadCreatureSprite(scene, opt.species_id, 'icon').then((key) => {
          if (key && swatch.active) {
            const icon = scene.add.image(PAD + 10, rowY + 2, key).setOrigin(0, 0).setDisplaySize(16, 16);
            this.panel.add(icon);
            this.panel.container.bringToTop(this.cursor.sprite);
            swatch.setVisible(false);
          }
        });
      }

      const label = `${species?.name ?? '???'}  ${species?.types.join('/') ?? ''}`;
      const name = makeText(scene, PAD + 30, rowY + 5, label, theme.text.base);
      this.panel.add(name);
      this.names.push(name);
    });

    // Detail pane: a thin separator + the selected starter's blurb, wrapped to the
    // panel width and refreshed on every cursor move (never stacked per-row).
    const sep = scene.add
      .rectangle(PAD, detailTop - Math.floor(PAD / 2), width - PAD * 2, 1, hex(theme.color.panelEdge))
      .setOrigin(0, 0)
      .setAlpha(0.5);
    this.panel.add(sep);

    this.detail = makeText(scene, PAD, detailTop, '', theme.text.dim);
    this.detail.setWordWrapWidth(width - PAD * 2);
    this.panel.add(this.detail);

    this.cursor = new Cursor(scene).setScrollFactor0();
    this.panel.add(this.cursor.sprite);
    this.refresh();
  }

  /** Reflect the current selection: cursor position, highlighted name, blurb. */
  private refresh(): void {
    this.cursor.moveTo(PAD, this.listTop + this.index * ROW_H + ROW_H / 2);
    this.names.forEach((name, i) =>
      name.setColor(i === this.index ? theme.text.accent.color : theme.text.base.color),
    );
    this.detail.setText(STARTERS[this.index].blurb);
  }

  private move(dir: number): void {
    const next = (this.index + dir + STARTERS.length) % STARTERS.length;
    if (next !== this.index) {
      this.index = next;
      this.refresh();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the screen; resolve with the chosen species id. */
  run(): Promise<number> {
    const input = new InputController(this.scene);
    let armed = false;
    return new Promise((resolve) => {
      const tick = (): void => {
        input.update();
        if (!armed) {
          if (!input.isDown(InputAction.Confirm)) armed = true;
          return;
        }
        if (input.justPressed(InputAction.Up)) this.move(-1);
        else if (input.justPressed(InputAction.Down)) this.move(1);
        else if (input.justPressed(InputAction.Confirm)) {
          void this.sfx?.play(theme.cursor.confirmSfx);
          const chosen = STARTERS[this.index].species_id;
          this.scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
          input.destroy();
          this.destroy();
          resolve(chosen);
        }
      };
      this.scene.events.on(Phaser.Scenes.Events.UPDATE, tick);
    });
  }

  destroy(): void {
    this.cursor.destroy();
    this.panel.destroy();
  }
}
