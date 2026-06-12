/**
 * Runtime UI preferences — the live, in-memory side of the persisted Settings
 * (SaveManager.loadSettings). Boot applies the stored values once; the
 * SettingsMenu writes through here when the player changes them. Game code
 * reads these getters (DialogueBox for the typewriter, Player for auto-run)
 * instead of re-reading storage every frame.
 */

export type TextSpeed = 'cosy' | 'brisk' | 'instant';
export type BattlePace = 'cosy' | 'swift';
/** Stepped volume level shared by music + sfx (OFF is true silence). */
export type VolumeLevel = 'off' | 'low' | 'mid' | 'full';

let textSpeed: TextSpeed = 'cosy';
let alwaysRun = false;
let battlePace: BattlePace = 'cosy';
let musicVolume: VolumeLevel = 'full';
let sfxVolume: VolumeLevel = 'full';

/** OFF/LOW/MID/FULL -> 0/0.33/0.66/1. */
const VOLUME_GAIN: Record<VolumeLevel, number> = {
  off: 0,
  low: 0.33,
  mid: 0.66,
  full: 1,
};

export function volumeGain(level: VolumeLevel): number {
  return VOLUME_GAIN[level];
}

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

// ----------------------------------------------------------------- battle pace --

export function setBattlePace(pace: BattlePace): void {
  battlePace = pace;
}

export function getBattlePace(): BattlePace {
  return battlePace;
}

/** Multiplier for battle waits / tween durations (1 = cosy, 0.5 = swift). */
export function battlePaceFactor(): number {
  return battlePace === 'swift' ? 0.5 : 1;
}

// ------------------------------------------------------------------- volumes --

/**
 * Live volume changes need to re-apply to already-playing music (the MusicDirector
 * instance for the current scene). Audio modules subscribe; the SettingsMenu /
 * boot writes through the setters below, which notify subscribers.
 */
const musicVolumeSubscribers = new Set<() => void>();

export function onMusicVolumeChange(cb: () => void): () => void {
  musicVolumeSubscribers.add(cb);
  return () => musicVolumeSubscribers.delete(cb);
}

export function setMusicVolume(level: VolumeLevel): void {
  musicVolume = level;
  for (const cb of musicVolumeSubscribers) cb();
}

export function getMusicVolume(): VolumeLevel {
  return musicVolume;
}

/** Master gain (0..1) applied to all music playback. */
export function musicMasterGain(): number {
  return VOLUME_GAIN[musicVolume];
}

export function setSfxVolume(level: VolumeLevel): void {
  sfxVolume = level;
}

export function getSfxVolume(): VolumeLevel {
  return sfxVolume;
}

/** Master gain (0..1) applied to all one-shot sound effects. */
export function sfxMasterGain(): number {
  return VOLUME_GAIN[sfxVolume];
}
