/**
 * GleamsMenu — the Skyweave Crown / badge case (pause menu -> GLEAMS).
 *
 * The eight Gleams laid out as the Crown: four quadrant columns (South · East ·
 * North · West), two Gleams each. A relit constellation shows its emblem in its
 * element's colour; one you've yet to relight reads as a dim silhouette under its
 * region — so the case doubles as a map of where the remaining light waits. The
 * detail pane names the selected Gleam, its constellation, and the warden / town
 * it comes from, "linking" each badge back to the place you earn it.
 *
 * Emblem art is the served webp (content/gleams.ts); if a piece isn't on disk yet
 * the cell falls back to a drawn constellation roundel, so the screen always reads.
 * Promise-based and read-only: arrows move, B backs out. Built from the UI kit +
 * theme tokens, owns its own InputController (the house contract).
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { Panel } from './Panel';
import { loadImage } from '@game/systems/sprites/loadImage';
import { InputController, InputAction } from '@game/systems/input/InputController';
import { GLEAMS, type GleamEntry, type Quadrant } from '@game/content/gleams';
import type { Sfx } from '@game/systems/audio/Sfx';

const PAD = theme.space.lg;
const COLS: Quadrant[] = ['South', 'East', 'North', 'West'];
const EMBLEM_R = 15;
const LOCKED = 0x3a3850;

/** Tiny constellation figures (normalised −1..1), drawn star-to-star per Gleam. */
const FIGURES: Record<string, ReadonlyArray<readonly [number, number]>> = {
  ember: [[0, -0.8], [-0.55, 0.35], [0, -0.05], [0.55, 0.35], [0, 0.75]],
  tide: [[-0.8, 0.25], [-0.3, -0.3], [0.2, 0.3], [0.7, -0.3]],
  verdant: [[0, 0.8], [0, 0.05], [-0.55, -0.25], [0, 0.05], [0.45, -0.45]],
  stone: [[-0.4, -0.1], [0.4, -0.1], [0, -0.7], [0, 0.5]],
  storm: [[-0.45, -0.8], [0.1, -0.2], [-0.2, 0.15], [0.45, 0.75]],
  frost: [[-0.8, 0.2], [-0.4, -0.45], [0, -0.7], [0.4, -0.45], [0.8, 0.2]],
  solar: [[0, -0.85], [0, 0.85], [0, 0], [-0.85, 0], [0.85, 0]],
  lunar: [[-0.6, -0.55], [-0.72, 0.1], [-0.4, 0.62], [0.12, 0.72], [0.52, 0.42]],
};

interface Cell {
  gleam: GleamEntry;
  earned: boolean;
  container: Phaser.GameObjects.Container;
  cx: number;
  cy: number;
}

export class GleamsMenu {
  private readonly panel: Panel;
  private readonly cells: Cell[] = [];
  private readonly select: Phaser.GameObjects.Arc;
  private readonly detailTitle: Phaser.GameObjects.Text;
  private readonly detailFrom: Phaser.GameObjects.Text;
  private readonly detailBlurb: Phaser.GameObjects.Text;
  private index = 0;

  constructor(
    private readonly scene: Phaser.Scene,
    held: (flag: string) => boolean,
    private readonly sfx?: Sfx,
  ) {
    const width = GAME_WIDTH - 8;
    const height = GAME_HEIGHT - 8;
    this.panel = new Panel(scene, 4, 4, width, height).fixedToCamera().setDepth(theme.depth.panel);

    const earnedCount = GLEAMS.filter((g) => held(g.flag)).length;
    this.panel.add(makeText(scene, PAD, PAD - 2, 'THE SKYWEAVE CROWN', theme.text.accent));
    this.panel.add(
      makeText(scene, width - PAD, PAD - 2, `${earnedCount}/8`, theme.text.dim).setOrigin(1, 0),
    );

    // Four quadrant columns, two Gleams stacked per column.
    const innerL = PAD + 8;
    const colW = (width - innerL * 2) / COLS.length;
    const colX = (c: number): number => innerL + c * colW + colW / 2;
    const rowY = [42, 84];
    COLS.forEach((region, c) => {
      this.panel.add(
        makeText(scene, colX(c), 20, region.toUpperCase(), theme.text.dim).setOrigin(0.5, 0),
      );
    });

    // Cells in canonical order: col = floor(i/2), row = i%2 (two per quadrant).
    GLEAMS.forEach((gleam, i) => {
      const cx = colX(Math.floor(i / 2));
      const cy = rowY[i % 2];
      const earned = held(gleam.flag);
      const container = this.makeEmblem(gleam, earned, cx, cy);
      this.panel.add(container);
      this.cells.push({ gleam, earned, container, cx, cy });
    });

    // Selection ring (fill-less arc + an accent stroke).
    this.select = scene.add
      .circle(0, 0, EMBLEM_R + 3, 0x000000, 0)
      .setStrokeStyle(1, hex(theme.text.accent.color));
    this.panel.add(this.select);

    // Detail pane.
    const sepY = height - PAD - 36;
    const sep = scene.add
      .rectangle(PAD, sepY, width - PAD * 2, 1, hex(theme.color.panelEdge))
      .setOrigin(0, 0)
      .setAlpha(0.5);
    this.panel.add(sep);
    this.detailTitle = makeText(scene, PAD, sepY + 4, '', theme.text.accent);
    this.detailFrom = makeText(scene, PAD, sepY + 15, '', theme.text.dim);
    this.detailBlurb = makeText(scene, PAD, sepY + 25, '', theme.text.narrate);
    this.detailBlurb.setWordWrapWidth(width - PAD * 2);
    this.panel.add(this.detailTitle);
    this.panel.add(this.detailFrom);
    this.panel.add(this.detailBlurb);

    this.refresh();
  }

  /** Build a Gleam's emblem: a drawn constellation roundel, with the served art
   *  overlaid on top once it loads (degrades to the drawing if it's missing). */
  private makeEmblem(gleam: GleamEntry, earned: boolean, cx: number, cy: number): Phaser.GameObjects.Container {
    const color = earned ? hex(theme.typeColor[gleam.element as keyof typeof theme.typeColor] ?? '#ffd089') : LOCKED;
    const disc = this.scene.add.circle(0, 0, EMBLEM_R, 0x10121f, earned ? 0.9 : 0.65);
    disc.setStrokeStyle(1, color, earned ? 0.9 : 0.5);
    const figure = this.scene.add.graphics();
    const stars = FIGURES[gleam.id] ?? [];
    figure.lineStyle(1, color, earned ? 0.7 : 0.35);
    stars.forEach(([x, y], k) => {
      const px = x * (EMBLEM_R - 4);
      const py = y * (EMBLEM_R - 4);
      if (k === 0) {
        figure.beginPath();
        figure.moveTo(px, py);
      } else figure.lineTo(px, py);
    });
    figure.strokePath();
    figure.fillStyle(color, earned ? 1 : 0.45);
    for (const [x, y] of stars) {
      figure.fillCircle(x * (EMBLEM_R - 4), y * (EMBLEM_R - 4), earned ? 1.4 : 1.1);
    }
    const container = this.scene.add.container(cx, cy, [disc, figure]);

    // Overlay the served emblem art if present; tinted dark while still locked.
    const key = `gleam_${gleam.id}`;
    void loadImage(this.scene, key, gleam.art).then((ok) => {
      if (!ok || !this.scene.textures.exists(key)) return;
      const img = this.scene.add.image(0, 0, key).setDisplaySize(EMBLEM_R * 2, EMBLEM_R * 2);
      if (!earned) img.setTint(0x202234).setAlpha(0.7);
      figure.setVisible(false);
      container.add(img);
    });
    return container;
  }

  private refresh(): void {
    const cell = this.cells[this.index];
    this.select.setPosition(cell.cx, cell.cy);
    const g = cell.gleam;
    this.detailTitle.setText(`${g.constellation.toUpperCase()} - ${g.element.toUpperCase()} GLEAM`);
    if (cell.earned) {
      this.detailFrom.setText(`Relit at ${g.lumenary} - granted by ${g.warden}.`);
      this.detailBlurb.setText(g.blurb);
    } else {
      this.detailFrom.setText(`Not yet relit - ${g.lumenary}'s Lumenary (${g.region}).`);
      this.detailBlurb.setText("A constellation still dark. Earn its Lampwarden's trust to light it home.");
    }
  }

  /** Move within the 4x2 grid: col = floor(i/2), row = i%2. */
  private move(dx: number, dy: number): void {
    let col = Math.floor(this.index / 2);
    let row = this.index % 2;
    col = Phaser.Math.Clamp(col + dx, 0, COLS.length - 1);
    row = Phaser.Math.Clamp(row + dy, 0, 1);
    const next = col * 2 + row;
    if (next !== this.index) {
      this.index = next;
      this.refresh();
      void this.sfx?.play(theme.cursor.moveSfx);
    }
  }

  /** Show the badge case; resolve when the player backs out. */
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
        if (input.justPressed(InputAction.Left)) this.move(-1, 0);
        else if (input.justPressed(InputAction.Right)) this.move(1, 0);
        else if (input.justPressed(InputAction.Up)) this.move(0, -1);
        else if (input.justPressed(InputAction.Down)) this.move(0, 1);
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
    this.panel.destroy();
  }
}
