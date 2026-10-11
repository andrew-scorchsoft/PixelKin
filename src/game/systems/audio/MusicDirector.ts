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
import { musicMasterGain, onMusicVolumeChange, getMusicStyle, onMusicStyleChange } from '@game/ui/preferences';
import REMASTER from '@game/data/music-remaster.json';

/** A remastered track: one file = play-once intro [0, loop_start) + looping body. */
interface RemasterEntry {
  loop_start: number | null;
  duration: number;
}
const REMASTERED = (REMASTER as { tracks: Record<string, RemasterEntry> }).tracks;
const REMASTER_DIR = 'assets/audio/music/remaster/';

/** What to actually load for a requested (classic) key + url. */
interface Resolved {
  key: string;
  url: string;
  loopStart: number;
}

/**
 * A playing bed. Classic tracks are one looping sound; a remaster with an intro is
 * TWO sounds sharing one buffer — the intro marker [0, loop_start) and the body
 * marker [loop_start, end) looped, scheduled `delay: loop_start` later on the
 * same AudioContext clock, so the hand-off is sample-accurate and the intro
 * never replays (re-entering a map with the same bed is already a no-op).
 */
class Bed {
  private readonly parts: Phaser.Sound.BaseSound[] = [];
  private vol: number;

  constructor(scene: Phaser.Scene, key: string, loopStart: number, volume: number) {
    this.vol = volume;
    const body = scene.sound.add(key, { volume });
    const total = body.duration || body.totalDuration;
    if (loopStart > 0.05 && total > loopStart + 1) {
      const intro = scene.sound.add(key, { volume });
      intro.addMarker({ name: 'intro', start: 0, duration: loopStart });
      body.addMarker({ name: 'body', start: loopStart, duration: total - loopStart, config: { loop: true } });
      intro.play('intro', { volume });
      body.play('body', { volume, loop: true, delay: loopStart });
      this.parts.push(intro, body);
    } else {
      body.play({ volume, loop: true });
      this.parts.push(body);
    }
  }

  get isPlaying(): boolean {
    return this.parts.some((p) => p.isPlaying);
  }

  get volume(): number {
    return this.vol;
  }

  setVolume(v: number): void {
    this.vol = v;
    for (const p of this.parts) (p as Phaser.Sound.BaseSound & { setVolume?: (v: number) => void }).setVolume?.(v);
  }

  stop(): void {
    for (const p of this.parts) p.stop();
  }

  destroy(): void {
    for (const p of this.parts) p.destroy();
    this.parts.length = 0;
  }
}

export class MusicDirector {
  private current?: Bed;
  private currentKey?: string;
  /** The classic key/url last asked for — re-resolved when the style flips. */
  private requested?: { key: string; url: string };
  private readonly unsubscribe: () => void;
  private readonly unsubscribeStyle: () => void;

  constructor(
    private readonly scene: Phaser.Scene,
    /** Per-scene base level; the live master volume scales this. */
    private readonly baseVolume = 0.45,
  ) {
    // Re-apply the master volume to whatever is playing when the player changes it.
    this.unsubscribe = onMusicVolumeChange(() => this.applyMasterVolume());
    // Soundtrack style flipped in Settings: swap the current bed to the other score.
    this.unsubscribeStyle = onMusicStyleChange(() => {
      const r = this.requested;
      if (r && this.current) void this.crossfade(r.key, r.url, 500);
    });
    // Tear the subscriptions down with the scene so we don't leak across restarts.
    const off = (): void => {
      this.unsubscribe();
      this.unsubscribeStyle();
    };
    this.scene.events.once(Phaser.Scenes.Events.SHUTDOWN, off);
    this.scene.events.once(Phaser.Scenes.Events.DESTROY, off);
  }

  /** Current effective target volume: per-scene base scaled by the master gain. */
  private get volume(): number {
    return this.baseVolume * musicMasterGain();
  }

  /** Snap the playing bed to the current effective volume (live master change). */
  private applyMasterVolume(): void {
    this.current?.setVolume(this.volume);
  }

  get playingKey(): string | undefined {
    return this.current?.isPlaying ? this.requested?.key : undefined;
  }

  /** Map a classic track (`assets/audio/music/<id>.mp3`) to the selected score. */
  private resolve(key: string, url: string): Resolved {
    const id = url.split('/').pop()?.replace(/\.mp3$/i, '') ?? key;
    const r = getMusicStyle() === 'remastered' ? REMASTERED[id] : undefined;
    if (!r) return { key, url, loopStart: 0 };
    return { key: `${key}@remaster`, url: `${REMASTER_DIR}${id}.mp3`, loopStart: r.loop_start ?? 0 };
  }

  /** Load the resolved track, falling back to the classic file if a remaster is missing. */
  private async load(key: string, url: string): Promise<Resolved | undefined> {
    const r = this.resolve(key, url);
    if (await loadAudio(this.scene, r.key, r.url)) return r;
    if (r.key !== key && (await loadAudio(this.scene, key, url))) return { key, url, loopStart: 0 };
    return undefined;
  }

  /** Play a loop by key (loading `url` if needed). No-op if already on this key. */
  async play(key: string, url: string): Promise<void> {
    const want = this.resolve(key, url).key;
    if (this.currentKey === want && this.current?.isPlaying) return;
    this.requested = { key, url };
    const r = await this.load(key, url);
    if (!r) return;
    this.stop();
    this.current = new Bed(this.scene, r.key, r.loopStart, this.volume);
    this.currentKey = r.key;
    this.requested = { key, url };
  }

  /**
   * Crossfade to a new bed: bring the current track down to silence while the new
   * one rises from 0 to target, then drop the old one. Falls back to a hard `play`
   * if there's nothing currently playing (or the new file is missing → silence).
   */
  async crossfade(key: string, url: string, ms = 700): Promise<void> {
    const want = this.resolve(key, url).key;
    if (this.currentKey === want && this.current?.isPlaying) return;
    this.requested = { key, url };
    const r = await this.load(key, url);
    if (!r) {
      // Target missing: at least fade the old bed out so we don't jump-cut.
      await this.fadeToSilence(ms);
      return;
    }
    const outgoing = this.current;
    const incoming = new Bed(this.scene, r.key, r.loopStart, 0);
    this.current = incoming;
    this.currentKey = r.key;
    this.requested = { key, url };

    if (outgoing) this.tweenVolume(outgoing, 0, ms, () => this.disposeOf(outgoing));
    await this.tweenVolume(incoming, this.volume, ms);
  }

  /** Fade the current bed down to silence and stop it (a held, quiet beat). */
  async fadeToSilence(ms = 700): Promise<void> {
    const sound = this.current;
    if (!sound) return;
    this.current = undefined;
    this.currentKey = undefined;
    this.requested = undefined;
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
    const gain = musicMasterGain();
    if (gain <= 0) return; // OFF: true silence, skip the cue entirely
    void this.load(key, url).then((r) => {
      if (r) this.scene.sound.play(r.key, { volume: volume * gain });
    });
  }

  setVolume(v: number): void {
    this.current?.setVolume(v);
  }

  stop(): void {
    if (this.current) {
      this.disposeOf(this.current);
      this.current = undefined;
      this.currentKey = undefined;
      this.requested = undefined;
    }
  }

  /** Tween a sound's volume to a target, awaitable; resolves immediately if the
   *  backend lacks setVolume (e.g. a no-audio fallback manager). */
  private tweenVolume(sound: Bed, to: number, ms: number, onDone?: () => void): Promise<void> {
    const s = sound as Bed & { volume?: number; setVolume?: (v: number) => void };
    if (typeof s.setVolume !== 'function') {
      onDone?.();
      return Promise.resolve();
    }
    if (ms <= 0) {
      // Zero-duration: snap straight to target (no tween, no div-by-zero in ease).
      s.setVolume?.(to);
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

  private disposeOf(sound: Bed): void {
    sound.stop();
    sound.destroy();
  }
}
