/**
 * FrameReel — a short full-screen picture SEQUENCE over the world, the `frames`
 * cutscene op (content/types.ts): a handful of 3:2 stills played in order with
 * cross-dissolves between them, so a scene can be SHOWN rather than told — the
 * rolling thunder crossing the Sere from the Thunder Table is the worked example.
 *
 * Data only: the op lists the served stills, the hold and dissolve times, which
 * frames STRIKE (a white camera flash + a shake + `flashSfx`) and a one-shot `sfx`
 * that runs under the whole reel. Like every cinematic primitive it degrades
 * silently: a still that fails to load is skipped, and with none at all the reel
 * just plays its sound over the dark. Cancel (B) skips to the end.
 *
 * Camera-fixed, above the dialogue band (theme.depth.toast) so nothing of the
 * world shows through; the stills are 240x160 like the cinematic panels.
 */
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@game/config';
import { theme } from './theme';
import { loadImage } from '@game/systems/sprites/loadImage';
import { InputController, InputAction } from '@game/systems/input/InputController';
import type { Sfx } from '@game/systems/audio/Sfx';

export interface FrameReelSpec {
  frames: string[];
  holdMs?: number;
  fadeMs?: number;
  flash?: number[];
  sfx?: string;
  flashSfx?: string;
}

const DEPTH = theme.depth.toast + 5;
const DEFAULT_HOLD = 1400;
const DEFAULT_FADE = 600;

export class FrameReel {
  constructor(
    private readonly scene: Phaser.Scene,
    private readonly sfx?: Sfx,
  ) {}

  async play(spec: FrameReelSpec): Promise<void> {
    const scene = this.scene;
    const hold = spec.holdMs ?? DEFAULT_HOLD;
    const fade = spec.fadeMs ?? DEFAULT_FADE;
    const strikes = new Set(spec.flash ?? []);

    const black = scene.add
      .rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, 0x000000, 1)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(DEPTH)
      .setAlpha(0);
    await this.tween(black, 1, 350);

    // load every still first (a missing one is simply skipped)
    const keys: { key: string; i: number }[] = [];
    for (let i = 0; i < spec.frames.length; i++) {
      const key = `reel:${spec.frames[i]}`;
      if (await loadImage(scene, key, spec.frames[i])) keys.push({ key, i });
    }

    let skipped = false;
    const input = new InputController(scene);
    const tick = (): void => {
      input.update();
      if (input.justPressed(InputAction.Cancel)) skipped = true;
    };
    scene.events.on(Phaser.Scenes.Events.UPDATE, tick);

    if (spec.sfx) void this.sfx?.play(spec.sfx);
    const shown: Phaser.GameObjects.Image[] = [];
    try {
      for (let n = 0; n < keys.length && !skipped; n++) {
        const { key, i } = keys[n];
        const img = scene.add
          .image(GAME_WIDTH / 2, GAME_HEIGHT / 2, key)
          .setDisplaySize(GAME_WIDTH, GAME_HEIGHT)
          .setScrollFactor(0)
          .setDepth(DEPTH + 1 + n)
          .setAlpha(0);
        shown.push(img);
        await this.tween(img, 1, n === 0 ? 700 : fade);
        // only the newest still needs to stay drawn under the next dissolve
        while (shown.length > 2) shown.shift()?.destroy();
        if (strikes.has(i)) {
          if (spec.flashSfx) void this.sfx?.play(spec.flashSfx);
          scene.cameras.main.flash(260, 235, 240, 255);
          scene.cameras.main.shake(380, 0.006);
        }
        await this.wait(hold, () => skipped);
      }
      // let the last still breathe, then go to black
      for (const img of shown) void this.tween(img, 0, 700);
      await this.wait(700);
    } finally {
      scene.events.off(Phaser.Scenes.Events.UPDATE, tick);
      input.destroy();
      for (const img of shown) img.destroy();
    }
    await this.tween(black, 0, 450);
    black.destroy();
  }

  private tween(target: Phaser.GameObjects.GameObject, alpha: number, ms: number): Promise<void> {
    return new Promise((resolve) => {
      this.scene.tweens.add({ targets: target, alpha, duration: ms, onComplete: () => resolve() });
    });
  }

  private wait(ms: number, until?: () => boolean): Promise<void> {
    return new Promise((resolve) => {
      const t0 = this.scene.time.now;
      const ev = this.scene.time.addEvent({
        delay: 50,
        loop: true,
        callback: () => {
          if (this.scene.time.now - t0 >= ms || until?.()) {
            ev.remove();
            resolve();
          }
        },
      });
    });
  }
}
