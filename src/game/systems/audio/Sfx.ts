/**
 * Sfx — named one-shot sound effects.
 *
 * The full SFX set is rendered under public/assets/audio/sfx/ (by generate-midi),
 * where almost every cue ships as a/b/c VARIANTS (e.g. `ui-confirm-a.mp3`) so a
 * repeated action doesn't sound robotic — there is usually NO bare `ui-confirm.mp3`.
 * Callers still use the *base* key (`play('ui-confirm')`); we resolve it to a random
 * available variant via the manifest. Effects are loaded on first use and cached; a
 * missing key is tolerated (silent). When you add/re-render SFX, regenerate the
 * manifest: see public/assets/audio/sfx/sfx.manifest.json.
 */
import Phaser from 'phaser';
import { loadAudio } from './loadAudio';
import { sfxMasterGain } from '@game/ui/preferences';
import sfxManifest from '../../../../public/assets/audio/sfx/sfx.manifest.json';

const SFX_DIR = 'assets/audio/sfx/';

/** Two requests for the same cue inside this window play once: a script's own
 *  `sfx world-pickup` beside the `giveItem` that voices itself used to stack two
 *  random variants on one frame (a flammed, doubled-loud chirp). */
const DEDUPE_MS = 90;
/**
 * Per-cue overrides. The typewriter blip fires on every revealed character (30-60
 * a second), so with no spacing its 80 ms copies stacked into one loud buzz — the
 * playtest's "text beeping ignores the effects volume". It is spaced so copies never
 * overlap, and trimmed ~7 dB: it's a near-full-scale square and the most-heard cue.
 */
const CUE_DEDUPE_MS: Record<string, number> = { 'ui-text-blip': 70 };
const CUE_TRIM: Record<string, number> = { 'ui-text-blip': 0.45 };
const lastPlayed = new Map<string, number>();

/** All rendered SFX stems (filenames without extension). */
const STEMS = new Set<string>((sfxManifest as { stems: string[] }).stems);

/** base key -> the variant letters that exist for it (e.g. 'ui-confirm' -> ['a','b','c']). */
const VARIANTS = ((): Map<string, string[]> => {
  const m = new Map<string, string[]>();
  for (const stem of STEMS) {
    const dash = stem.lastIndexOf('-');
    if (dash < 0) continue;
    const base = stem.slice(0, dash);
    const v = stem.slice(dash + 1);
    if (v.length === 1) (m.get(base) ?? m.set(base, []).get(base)!).push(v);
  }
  return m;
})();

export class Sfx {
  constructor(
    private readonly scene: Phaser.Scene,
    /** One-shot level before the player's Effects setting. Was 0.6, which put chip
     *  effects ~8 dB over the remastered score's loud passages (playtest, 2026-10);
     *  0.3 (-6 dB) lands them just above the music, clear but not jumpy. */
    private readonly volume = 0.3,
  ) {}

  /**
   * Resolve a requested key to an actual rendered stem: the key itself if a bare
   * file exists, otherwise a random a/b/c variant. Null if neither exists.
   */
  private resolveStem(key: string): string | null {
    if (STEMS.has(key)) return key;
    const variants = VARIANTS.get(key);
    if (variants && variants.length > 0) {
      return `${key}-${variants[Math.floor(Math.random() * variants.length)]}`;
    }
    return null;
  }

  /** Whether a key resolves to a rendered effect (bare stem or a/b/c variants) —
   *  lets callers prefer a specific cue (e.g. 'world-footstep-sand') and fall back. */
  has(key: string): boolean {
    return STEMS.has(key) || (VARIANTS.get(key)?.length ?? 0) > 0;
  }

  /** Play a single named effect (base key, no extension). Picks a variant if needed. */
  async play(key: string): Promise<void> {
    await this.start(key);
  }

  /**
   * Play an effect and resolve when it has finished (or straight away if it is
   * silent, missing or muted) — for a jingle a beat must wait on, like the rest
   * lullaby over the black screen. `maxMs` caps the wait in case the backend never
   * reports completion.
   */
  async playToEnd(key: string, maxMs = 6000): Promise<void> {
    const sound = await this.start(key);
    if (!sound) return;
    await new Promise<void>((resolve) => {
      let done = false;
      const finish = (): void => {
        if (done) return;
        done = true;
        resolve();
      };
      sound.once(Phaser.Sound.Events.COMPLETE, finish);
      sound.once(Phaser.Sound.Events.DESTROY, finish);
      this.scene.time.delayedCall(maxMs, finish);
    });
  }

  /** Resolve, load and start one effect; the playing sound, or null if silent. */
  private async start(key: string): Promise<Phaser.Sound.BaseSound | null> {
    const gain = sfxMasterGain();
    if (gain <= 0) return null; // OFF: true silence, skip the one-shot entirely
    const now = Date.now();
    // Dedupe on the BASE cue, so play('x') and playVariant('x', …) count as one.
    const base = /-[a-z]$/.test(key) && VARIANTS.has(key.slice(0, -2)) ? key.slice(0, -2) : key;
    if (now - (lastPlayed.get(base) ?? -Infinity) < (CUE_DEDUPE_MS[base] ?? DEDUPE_MS)) return null;
    const stem = this.resolveStem(key);
    if (!stem) return null; // not a rendered effect — stay silent rather than 404
    lastPlayed.set(base, now);
    const ok = await loadAudio(this.scene, stem, `${SFX_DIR}${stem}.mp3`);
    if (!ok) return null;
    // add + play (not sound.play) so the caller can wait on this instance; Phaser
    // frees it on completion.
    const sound = this.scene.sound.add(stem, { volume: this.volume * gain * (CUE_TRIM[base] ?? 1) });
    sound.once(Phaser.Sound.Events.COMPLETE, () => sound.destroy());
    sound.play();
    return sound;
  }

  /**
   * Play a specific subset of variants, e.g. playVariant('world-footstep', ['a','b']).
   * (Equivalent to `play(base)` when you want every available variant — kept for
   * call sites that pin an explicit set.)
   */
  async playVariant(base: string, variants: string[]): Promise<void> {
    const v = variants[Math.floor(Math.random() * variants.length)];
    await this.play(`${base}-${v}`);
  }
}
