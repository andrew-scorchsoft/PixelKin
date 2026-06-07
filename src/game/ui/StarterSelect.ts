/**
 * StarterSelect — the choose-your-companion screen shown in the intro cutscene.
 * Lists the founding trio with a short blurb each; up/down + Confirm picks one
 * (not cancellable — you must choose). Promise-based: resolves with the chosen
 * species id. Built from the shared kit so it matches every other screen. Real
 * portraits will drop in later (creature art isn't packed to public/ yet); for now
 * each option shows a type-tinted swatch.
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
import type { Sfx } from '@game/systems/audio/Sfx';

const TYPE_TINT: Partial<Record<KinType, string>> = {
  Ember: '#ff8a3d',
  Tide: '#4fb4ff',
  Verdant: '#7bdc6b',
};

const ROW_H = 26;
const PAD = theme.space.lg;

export class StarterSelect {
  private readonly panel: Panel;
  private readonly cursor: Cursor;
  private readonly swatches: Phaser.GameObjects.Rectangle[] = [];
  private index = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly sfx?: Sfx,
  ) {
    const width = GAME_WIDTH - 24;
    const height = PAD * 2 + 12 + STARTERS.length * ROW_H;
    const x = (GAME_WIDTH - width) / 2;
    const y = 12;
    this.panel = new Panel(scene, x, y, width, height).fixedToCamera().setDepth(theme.depth.panel);

    this.panel.add(makeText(scene, PAD, PAD - 2, 'CHOOSE A COMPANION', theme.text.accent));

    STARTERS.forEach((opt, i) => {
      const species = SPECIES_BY_ID.get(opt.species_id);
      const rowY = PAD + 12 + i * ROW_H;
      const type = species?.types[0];
      const tint = (type && TYPE_TINT[type]) || theme.color.panelEdge;

      const swatch = scene.add
        .rectangle(PAD + 12, rowY + 4, 16, 16, hex(tint))
        .setOrigin(0, 0)
        .setStrokeStyle(1, hex(theme.color.panelShadow));
      this.panel.add(swatch);
      this.swatches.push(swatch);

      const name = `${species?.name ?? '???'}  ${species?.types.join('/') ?? ''}`;
      this.panel.add(makeText(scene, PAD + 34, rowY, name, theme.text.base));
      const blurb = makeText(scene, PAD + 34, rowY + 10, opt.blurb, theme.text.dim);
      blurb.setWordWrapWidth(width - (PAD + 34) - PAD);
      this.panel.add(blurb);
    });

    this.cursor = new Cursor(scene).setScrollFactor0();
    this.panel.add(this.cursor.sprite);
    this.placeCursor();
  }

  private placeCursor(): void {
    this.cursor.moveTo(PAD + 2, PAD + 12 + this.index * ROW_H + 10);
  }

  private move(dir: number): void {
    const next = (this.index + dir + STARTERS.length) % STARTERS.length;
    if (next !== this.index) {
      this.index = next;
      this.placeCursor();
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
