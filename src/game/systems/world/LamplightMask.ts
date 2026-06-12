/**
 * LamplightMask — the dark-map reveal mask (walkthrough spine §5).
 *
 * On maps flagged `dark` in the registry, the world beyond the vesperlamp's
 * reveal radius falls into partial dusk: a single pre-rendered canvas texture
 * (dark everywhere, a stepped radial hole in the middle) drawn as one Image
 * centred on the player every frame. One texture per tier, generated at runtime
 * and cached — no art assets, no per-frame redraw.
 *
 * Renderer notes:
 *  - A CanvasTexture Image works identically in Canvas and WebGL (BitmapMask is
 *    WebGL-only, so we deliberately avoid masks).
 *  - The texture is drawn at LOGICAL resolution (240×160 world pixels); the
 *    RENDER_SCALE-zoomed framebuffer upscales it nearest-neighbour, so the
 *    stepped rings come out as crisp chunky bands — the retro register, not a
 *    smooth modern vignette.
 *  - NON-BLOCKING is the law: the dark is PARTIAL (MAX_ALPHA, never 1) and the
 *    main lane is diegetically lit, so everything required stays readable at
 *    Ember-glow. The mask sits at theme.depth.lamplight — above world/actors,
 *    below dialogue, cinematic tint/letterbox, and all UI.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, TILE_SIZE, COLORS } from '@game/config';
import { theme } from '@game/ui/theme';
import { lamplightTier, revealRadiusTiles } from './lamplight';

/** The darkness never exceeds this — partial dusk, never pitch black. */
const MAX_ALPHA = 0.6;

/** Stepped erase bands (fraction of radius -> erase strength). Hard steps so the
 *  ring quantises into chunky retro bands instead of a smooth gradient. */
const STEPS: ReadonlyArray<[number, number]> = [
  [0.55, 1.0], // fully lit core
  [0.7, 0.75],
  [0.82, 0.5],
  [0.92, 0.25],
  [1.0, 0.0], // full dusk beyond the radius
];

export class LamplightMask {
  private image: Phaser.GameObjects.Image;
  private tier = -1;

  constructor(
    private scene: Phaser.Scene,
    gleams: number,
  ) {
    this.image = scene.add
      .image(0, 0, this.textureFor(gleams))
      .setDepth(theme.depth.lamplight)
      .setAlpha(MAX_ALPHA);
  }

  /** Re-centre the dusk on the player (call every frame with the sprite's x/y). */
  follow(x: number, y: number): void {
    this.image.setPosition(x, y);
  }

  /** Re-check the tier (call when flags may have changed — cheap if unchanged). */
  setBrightness(gleams: number): void {
    if (lamplightTier(gleams) === this.tier) return;
    this.image.setTexture(this.textureFor(gleams));
  }

  destroy(): void {
    this.image.destroy();
  }

  /** Build (or fetch the cached) dusk texture for this tier. */
  private textureFor(gleams: number): string {
    this.tier = lamplightTier(gleams);
    const key = `lamplight-mask-${this.tier}`;
    if (this.scene.textures.exists(key)) return key;

    // Centred on the player with the camera following, the visible window never
    // extends more than a full screen from the player (camera clamped at map
    // edges is the worst case), so 2x the screen covers everything.
    const w = GAME_WIDTH * 2;
    const h = GAME_HEIGHT * 2;
    const canvas = this.scene.textures.createCanvas(key, w, h);
    if (!canvas) return key; // texture manager refused (shutdown) — tolerate
    const ctx = canvas.getContext();

    ctx.fillStyle = COLORS.night;
    ctx.fillRect(0, 0, w, h);

    // Carve the stepped hole: destination-out erases by the gradient's alpha.
    const radius = revealRadiusTiles(gleams) * TILE_SIZE;
    const grad = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, radius);
    let prev = STEPS[0][1];
    grad.addColorStop(0, `rgba(0,0,0,${prev})`);
    for (const [stop, erase] of STEPS) {
      grad.addColorStop(Math.max(0, stop - 0.001), `rgba(0,0,0,${prev})`);
      grad.addColorStop(stop, `rgba(0,0,0,${erase})`);
      prev = erase;
    }
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);
    ctx.globalCompositeOperation = 'source-over';

    canvas.refresh();
    return key;
  }
}
