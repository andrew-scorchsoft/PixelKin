/**
 * Runtime UI preferences — the live, in-memory side of the persisted Settings
 * (SaveManager.loadSettings). Boot applies the stored values once; the
 * SettingsMenu writes through here when the player changes them. Game code
 * reads these getters (DialogueBox for the typewriter, Player for auto-run)
 * instead of re-reading storage every frame.
 */

export type TextSpeed = 'cosy' | 'brisk' | 'instant';

let textSpeed: TextSpeed = 'cosy';
let alwaysRun = false;

export function setTextSpeed(speed: TextSpeed): void {
  textSpeed = speed;
}

export function getTextSpeed(): TextSpeed {
  return textSpeed;
}

/** Multiplier applied to the theme's chars-per-second (Infinity = instant). */
export function textSpeedMultiplier(): number {
  switch (textSpeed) {
    case 'brisk':
      return 2;
    case 'instant':
      return Number.POSITIVE_INFINITY;
    default:
      return 1;
  }
}

export function setAlwaysRun(on: boolean): void {
  alwaysRun = on;
}

export function getAlwaysRun(): boolean {
  return alwaysRun;
}
