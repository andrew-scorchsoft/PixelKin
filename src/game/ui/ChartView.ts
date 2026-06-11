/**
 * ChartView — a single concept-art "chart" shown full-screen, with a caption band
 * (name + mood line) over the art. Shared by two callers:
 *
 *  - the first-visit REVEAL (WorldScene): a "A NEW CHART" banner + the piece, held
 *    until the player presses on; and
 *  - the gallery (ChartsMenu): the same piece, flipped left/right through the charts
 *    the player has collected so far.
 *
 * The concept art is a 3:2 piece and the screen is 3:2 (240x160), so it fills exactly
 * with no distortion (the same trick CinematicScene uses). Missing art degrades to a
 * framed name card, so the gallery never shows a black hole. Everything sits above the
 * panel band (so it covers the gallery list) and is camera-fixed (the world scrolls).
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme, hex } from './theme';
import { makeText } from './Text';
import { loadImage } from '@game/systems/sprites/loadImage';
import { REGION_LABELS } from '@game/content/charts';
import type { ChartEntry } from '@game/content/types';

const PAD = theme.space.lg;
const CAPTION_H = 38;
const BANNER_H = 13;
// Sits above the panel band so it covers the gallery list beneath it.
const BASE_DEPTH = theme.depth.toast;

export interface ChartViewOptions {
  /** 'reveal' shows the "A NEW CHART" banner; 'gallery' shows the ‹ › flip arrows. */
  mode: 'reveal' | 'gallery';
}

export class ChartView {
  private readonly dim: Phaser.GameObjects.Rectangle;
  private readonly img: Phaser.GameObjects.Image;
  private readonly fallback: Phaser.GameObjects.Text;
  private readonly captionBg: Phaser.GameObjects.Rectangle;
  private readonly title: Phaser.GameObjects.Text;
  private readonly subtitle: Phaser.GameObjects.Text;
  private readonly hint: Phaser.GameObjects.Text;
  private readonly bannerBg?: Phaser.GameObjects.Rectangle;
  private readonly banner?: Phaser.GameObjects.Text;
  private readonly arrowLeft?: Phaser.GameObjects.Text;
  private readonly arrowRight?: Phaser.GameObjects.Text;
  private destroyed = false;

  constructor(
    private readonly scene: Phaser.Scene,
    opts: ChartViewOptions,
  ) {
    const fixed = <T extends Phaser.GameObjects.GameObject>(o: T): T => {
      (o as unknown as { setScrollFactor: (n: number) => void }).setScrollFactor(0);
      return o;
    };

    this.dim = fixed(
      scene.add.rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, hex(theme.color.panelShadow), 1).setOrigin(0, 0),
    ).setDepth(BASE_DEPTH);

    this.img = fixed(scene.add.image(GAME_WIDTH / 2, GAME_HEIGHT / 2, '__DEFAULT').setVisible(false))
      .setDepth(BASE_DEPTH + 1);

    this.fallback = fixed(makeText(scene, GAME_WIDTH / 2, GAME_HEIGHT / 2 - 6, '', theme.text.accent))
      .setOrigin(0.5)
      .setDepth(BASE_DEPTH + 1)
      .setVisible(false);

    this.captionBg = fixed(
      scene.add.rectangle(0, GAME_HEIGHT - CAPTION_H, GAME_WIDTH, CAPTION_H, hex(theme.color.panelShadow), 0.74)
        .setOrigin(0, 0),
    ).setDepth(BASE_DEPTH + 2);

    this.title = fixed(makeText(scene, PAD, GAME_HEIGHT - CAPTION_H + 5, '', theme.text.accent))
      .setDepth(BASE_DEPTH + 3);
    this.subtitle = fixed(makeText(scene, PAD, GAME_HEIGHT - CAPTION_H + 17, '', theme.text.narrate))
      .setDepth(BASE_DEPTH + 3);
    this.subtitle.setWordWrapWidth(GAME_WIDTH - PAD * 2);

    this.hint = fixed(
      makeText(scene, GAME_WIDTH - PAD, GAME_HEIGHT - PAD, opts.mode === 'reveal' ? 'PRESS A' : 'B BACK', theme.text.dim),
    )
      .setOrigin(1, 1)
      .setDepth(BASE_DEPTH + 3);

    if (opts.mode === 'reveal') {
      this.bannerBg = fixed(
        scene.add.rectangle(0, 0, GAME_WIDTH, BANNER_H, hex(theme.color.panelShadow), 0.62).setOrigin(0, 0),
      ).setDepth(BASE_DEPTH + 2);
      this.banner = fixed(makeText(scene, GAME_WIDTH / 2, 3, '', theme.text.accent))
        .setOrigin(0.5, 0)
        .setDepth(BASE_DEPTH + 3);
    } else {
      this.arrowLeft = fixed(makeText(scene, PAD - 2, GAME_HEIGHT / 2, '<', theme.text.accent))
        .setOrigin(0, 0.5)
        .setDepth(BASE_DEPTH + 3);
      this.arrowRight = fixed(makeText(scene, GAME_WIDTH - PAD + 2, GAME_HEIGHT / 2, '>', theme.text.accent))
        .setOrigin(1, 0.5)
        .setDepth(BASE_DEPTH + 3);
    }
  }

  /** Show a chart. Loads its art (lazily), fills the screen, and writes the caption.
   *  In gallery mode, `arrows` toggles the ‹ › flip affordances. */
  async setChart(chart: ChartEntry, arrows?: { left: boolean; right: boolean }): Promise<void> {
    this.title.setText(chart.name.toUpperCase());
    this.subtitle.setText(chart.subtitle);
    this.banner?.setText(`A NEW CHART  -  ${REGION_LABELS[chart.region]}`);
    this.arrowLeft?.setVisible(arrows?.left ?? false);
    this.arrowRight?.setVisible(arrows?.right ?? false);

    const ok = this.scene.textures.exists(chart.art) || (await loadImage(this.scene, chart.art, chart.art));
    if (this.destroyed) return;
    if (ok) {
      this.img.setTexture(chart.art).setDisplaySize(GAME_WIDTH, GAME_HEIGHT).setVisible(true);
      this.fallback.setVisible(false);
    } else {
      // No art on disk yet — a framed name card keeps the gallery whole.
      this.img.setVisible(false);
      this.fallback.setText(chart.name.toUpperCase()).setVisible(true);
    }
  }

  /** Fade the whole view in (used by the reveal for a gentle bloom). */
  fadeIn(ms = theme.cinematic.dissolveMs): Promise<void> {
    const targets = this.members();
    for (const t of targets) (t as unknown as { setAlpha: (n: number) => void }).setAlpha(0);
    return new Promise((resolve) => {
      this.scene.tweens.add({ targets, alpha: 1, duration: ms, ease: 'Sine.inOut', onComplete: () => resolve() });
    });
  }

  private members(): Phaser.GameObjects.GameObject[] {
    const all = [
      this.dim,
      this.img,
      this.fallback,
      this.captionBg,
      this.title,
      this.subtitle,
      this.hint,
      this.bannerBg,
      this.banner,
      this.arrowLeft,
      this.arrowRight,
    ];
    return all.filter((o): o is NonNullable<typeof o> => o != null);
  }

  destroy(): void {
    this.destroyed = true;
    for (const o of this.members()) o.destroy();
  }
}
