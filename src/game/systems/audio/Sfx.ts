/**
 * Sfx — named one-shot sound effects.
 *
 * The full SFX set is already rendered under public/assets/audio/sfx/. Effects are
 * loaded on first use and cached; a missing key is tolerated (silent). Many effects
 * ship as a/b/c variants — `playVariant` rotates them so repeated actions (footsteps,
 * hits) don't feel robotic. Keys match the rendered filenames (e.g. 'ui-confirm').
 */
import Phaser from 'phaser';
import { loadAudio } from './loadAudio';

const SFX_DIR = 'assets/audio/sfx/';

export class Sfx {
  constructor(
    private readonly scene: Phaser.Scene,
    private readonly volume = 0.6,
  ) {}

  /** Play a single named effect (filename stem, no extension). */
  async play(key: string): Promise<void> {
    const ok = await loadAudio(this.scene, key, `${SFX_DIR}${key}.mp3`);
    if (!ok) return;
    this.scene.sound.play(key, { volume: this.volume });
  }

  /** Play a random a/b/c variant of an effect, e.g. playVariant('world-footstep', ['a','b']). */
  async playVariant(base: string, variants: string[]): Promise<void> {
    const v = variants[Math.floor(Math.random() * variants.length)];
    await this.play(`${base}-${v}`);
  }
}
