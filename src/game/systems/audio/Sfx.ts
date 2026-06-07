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
import sfxManifest from '../../../../public/assets/audio/sfx/sfx.manifest.json';

const SFX_DIR = 'assets/audio/sfx/';

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
    private readonly volume = 0.6,
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

  /** Play a single named effect (base key, no extension). Picks a variant if needed. */
  async play(key: string): Promise<void> {
    const stem = this.resolveStem(key);
    if (!stem) return; // not a rendered effect — stay silent rather than 404
    const ok = await loadAudio(this.scene, stem, `${SFX_DIR}${stem}.mp3`);
    if (!ok) return;
    this.scene.sound.play(stem, { volume: this.volume });
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
