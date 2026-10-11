/**
 * Kin cries — each kin's own short chip call, rendered for the whole roster by
 * tools/audio/kin_cries.py to public/assets/audio/sfx/cry-NNN.mp3 (3-digit id:
 * a 1-char suffix would read as an a/b/c variant in Sfx). Played when a kin
 * enters battle, on a catch, from the REGISTER, and when you greet a grazing
 * ambient kin. A cry that isn't rendered is silence (Sfx degrades quietly).
 */
import type { Sfx } from './Sfx';

/** The sfx stem for a species' cry. */
export function cryKey(speciesId: number): string {
  return `cry-${String(speciesId).padStart(3, '0')}`;
}

/** Play a kin's cry (silent if it isn't rendered or SFX are off). */
export function playCry(sfx: Sfx | undefined, speciesId: number): void {
  if (!sfx) return;
  const key = cryKey(speciesId);
  if (sfx.has(key)) void sfx.play(key);
}
