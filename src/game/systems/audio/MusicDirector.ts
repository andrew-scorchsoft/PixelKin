/**
 * MusicDirector — owns the background music track and swaps it per map / battle.
 *
 * Phaser's sound manager is game-global, so music keeps playing across scene work.
 * Tracks are loaded lazily and missing files are tolerated (silent), so a map that
 * references an unrendered loop simply plays nothing rather than crashing. A short
 * fade smooths swaps (town → battle → town).
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

  stop(): void {
    if (this.current) {
      this.current.stop();
      this.current.destroy();
      this.current = undefined;
      this.currentKey = undefined;
    }
  }
}
