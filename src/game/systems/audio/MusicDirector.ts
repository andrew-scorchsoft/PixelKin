/**
 * MusicDirector — owns the background music track and swaps it per map / battle,
 * and gives cutscenes a way to use music as drama.
 *
 * Phaser's sound manager is game-global, so music keeps playing across scene work.
 * Tracks are loaded lazily and missing files are tolerated (silent), so a map that
 * references an unrendered loop simply plays nothing rather than crashing.
 *
 * Beyond the plain `play`/`stop`, cutscenes can `crossfade` between beds, `fadeToSilence`
 * for a held dread beat, `duck` under a one-shot, and fire a `playSting` cue over the
 * current bed. Volume changes ride tweens on a small proxy so the manager stays
 * framework-agnostic and the silent-fallback (missing file → no-op) is preserved.
 */
import Phaser from 'phaser';
import { loadAudio } from './loadAudio';

export class MusicDirector {
  private current?: Phaser.Sound.BaseSound;
  private currentKey?: string;

  constructor(
    private readonly scene: Phaser.Scene,
    private readonly volume = 0.45,
  ) {}

  get playingKey(): string | undefined {
    return this.current?.isPlaying ? this.currentKey : undefined;
  }

  /** Play a loop by key (loading `url` if needed). No-op if already on this key. */
  async play(key: string, url: string): Promise<void> {
    if (this.currentKey === key && this.current?.isPlaying) return;
    const ok = await loadAudio(this.scene, key, url);
    if (!ok) return;
    this.stop();
    const sound = this.scene.sound.add(key, { loop: true, volume: this.volume });
    sound.play();
    this.current = sound;
    this.currentKey = key;
  }

  /**
   * Crossfade to a new bed: bring the current track down to silence while the new
   * one rises from 0 to target, then drop the old one. Falls back to a hard `play`
   * if there's nothing currently playing (or the new file is missing → silence).
   */
  async crossfade(key: string, url: string, ms = 700): Promise<void> {
    if (this.currentKey === key && this.current?.isPlaying) return;
    const ok = await loadAudio(this.scene, key, url);
    if (!ok) {
      // Target missing: at least fade the old bed out so we don't jump-cut.
      await this.fadeToSilence(ms);
      return;
    }
    const outgoing = this.current;
    const incoming = this.scene.sound.add(key, { loop: true, volume: 0 });
    incoming.play();
    this.current = incoming;
    this.currentKey = key;

    if (outgoing) this.tweenVolume(outgoing, 0, ms, () => this.disposeOf(outgoing));
    await this.tweenVolume(incoming, this.volume, ms);
  }

  /** Fade the current bed down to silence and stop it (a held, quiet beat). */
  async fadeToSilence(ms = 700): Promise<void> {
    const sound = this.current;
    if (!sound) return;
    this.current = undefined;
    this.currentKey = undefined;
    await this.tweenVolume(sound, 0, ms);
    this.disposeOf(sound);
  }

  /** Dip the bed for `holdMs`, then restore — clears room for a sting. */
  async duck(ms: number, holdMs: number): Promise<void> {
    const sound = this.current;
    if (!sound) return;
    await this.tweenVolume(sound, this.volume * 0.25, ms);
    await new Promise<void>((r) => this.scene.time.delayedCall(holdMs, () => r()));
    await this.tweenVolume(sound, this.volume, ms);
  }

  /** Fire a one-shot cue over the current bed (e.g. the Gleam fanfare). */
  playSting(key: string, url: string, volume = 0.6): void {
    void loadAudio(this.scene, key, url).then((ok) => {
      if (ok) this.scene.sound.play(key, { volume });
    });
  }

  setVolume(v: number): void {
    const s = this.current as Phaser.Sound.BaseSound & { setVolume?: (v: number) => void };
    s?.setVolume?.(v);
  }

  stop(): void {
    if (this.current) {
      this.disposeOf(this.current);
      this.current = undefined;
      this.currentKey = undefined;
    }
  }

  /** Tween a sound's volume to a target, awaitable; resolves immediately if the
   *  backend lacks setVolume (e.g. a no-audio fallback manager). */
  private tweenVolume(sound: Phaser.Sound.BaseSound, to: number, ms: number, onDone?: () => void): Promise<void> {
    const s = sound as Phaser.Sound.BaseSound & { volume?: number; setVolume?: (v: number) => void };
    if (typeof s.setVolume !== 'function') {
      onDone?.();
      return Promise.resolve();
    }
    return new Promise((resolve) => {
      const proxy = { v: s.volume ?? this.volume };
      this.scene.tweens.add({
        targets: proxy,
        v: to,
        duration: ms,
        ease: 'Linear',
        onUpdate: () => s.setVolume?.(proxy.v),
        onComplete: () => {
          s.setVolume?.(to);
          onDone?.();
          resolve();
        },
      });
    });
  }

  private disposeOf(sound: Phaser.Sound.BaseSound): void {
    sound.stop();
    sound.destroy();
  }
}
