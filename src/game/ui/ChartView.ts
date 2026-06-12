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
/** Minimum caption-band height; the band grows to fit the wrapped mood line
 *  (a fixed slot clipped 3+-line subtitles off the 160px screen). */
const CAPTION_MIN_H = 30;
const CAPTION_PAD_Y = 4;
const CAPTION_GAP = 2;
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
      scene.add.rectangle(0, GAME_HEIGHT - CAPTION_MIN_H, GAME_WIDTH, CAPTION_MIN_H, hex(theme.color.panelShadow), 0.74)
        .setOrigin(0, 0),
    ).setDepth(BASE_DEPTH + 2);

    this.title = fixed(makeText(scene, PAD, 0, '', theme.text.accent))
      .setDepth(BASE_DEPTH + 3);
    this.subtitle = fixed(makeText(scene, PAD, 0, '', theme.text.narrate))
      .setDepth(BASE_DEPTH + 3);
    this.subtitle.setWordWrapWidth(GAME_WIDTH - PAD * 2);

    // The hint shares the title row (right-aligned) so a wrapped mood line can
    // never run underneath it; layoutCaption() positions both.
    this.hint = fixed(
      makeText(scene, GAME_WIDTH - PAD, 0, opts.mode === 'reveal' ? 'PRESS A' : 'B BACK', theme.text.dim),
    )
      .setOrigin(1, 0)
      .setDepth(BASE_DEPTH + 3);
    this.layoutCaption();

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
    this.layoutCaption();
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

  /** Bottom-anchor the caption band, sized to the wrapped subtitle (measured
   *  after setText), so long mood lines grow the band upward instead of
   *  clipping off the bottom of the 160px screen. */
  private layoutCaption(): void {
    const rowH = Math.max(this.title.height, this.hint.height);
    const h = Math.max(
      CAPTION_MIN_H,
      CAPTION_PAD_Y + rowH + CAPTION_GAP + this.subtitle.height + CAPTION_PAD_Y,
    );
    const top = GAME_HEIGHT - h;
    this.captionBg.setPosition(0, top).setSize(GAME_WIDTH, h);
    this.title.setPosition(PAD, top + CAPTION_PAD_Y);
    this.hint.setPosition(GAME_WIDTH - PAD, top + CAPTION_PAD_Y);
    this.subtitle.setPosition(PAD, top + CAPTION_PAD_Y + rowH + CAPTION_GAP);
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
