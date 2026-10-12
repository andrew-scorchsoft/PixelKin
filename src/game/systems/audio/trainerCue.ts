/**
 * The trainer-spots-you cue ("trainer-eyes"): the genre's eyes-meet moment. A
 * short startled phrase plays ONCE, then a "get ready" loop runs under the
 * trainer's walk-up and challenge lines until the battle theme takes over.
 *
 * One file, chip-only (battles are classic-only): the intro/loop split rides the
 * classic intro table `data/music-classic.json` (tools/audio/stitch_intro_loop.py).
 *
 * This module only DECIDES whether a scene is a plain challenge; WorldScene plays
 * the cue and hands the soundtrack back (`startBattle` stops it; an un-fought
 * scene restores the map's bed).
 */
import type { CutsceneStep } from '@game/content/types';
import { getScript } from '@game/content/scripts';
import { getTrainer } from '@game/content/trainers';

export const TRAINER_EYES_KEY = 'trainer-eyes';
export const TRAINER_EYES_URL = 'assets/audio/music/trainer-eyes.mp3';

/** Ops that mean the scene is scoring itself — never talk over its own music beat. */
const SCORED_OPS = new Set<CutsceneStep['op']>([
  'music',
  'musicCrossfade',
  'musicFade',
  'musicSting',
  'silence',
  'cinematic',
  'heal',
]);

/** More lines than this before the fight = a story beat with a battle in it, not a dare. */
const MAX_LEAD_IN_LINES = 3;
const LINE_OPS = new Set<CutsceneStep['op']>(['say', 'narrate', 'dialogue']);

/**
 * Is this scene a plain trainer CHALLENGE — does it reach an unguarded trainer
 * `battle` against a route-tier trainer, after only a short lead-in and before
 * any music beat of its own? Follows unguarded `run` composition; a battle behind
 * a flag guard or a `choice` branch is not a certain challenge, so it doesn't count.
 *
 * Skipped on purpose:
 *  - the 'smart' tier — Lampwardens, the rival's later duels, Vigilants, the
 *    Hollowing's acolytes, Còr: story set-pieces whose weight a jaunty dare would
 *    undercut (they go straight into their own battle theme, as before);
 *  - a long lead-in (> MAX_LEAD_IN_LINES lines) — a conversation that ends in a bout;
 *  - a scene that scores itself (music / silence / a rest / a cinematic first).
 */
export function opensWithChallenge(steps: readonly CutsceneStep[]): boolean {
  const seen = new Set<string>();
  let lines = 0;
  const walk = (list: readonly CutsceneStep[]): boolean | undefined => {
    for (const s of list) {
      if (SCORED_OPS.has(s.op)) return false; // it scores itself (or may) — stay out
      if (s.if_flag || s.unless_flag) continue;
      if (LINE_OPS.has(s.op) && ++lines > MAX_LEAD_IN_LINES) return false;
      if (s.op === 'battle') return getTrainer(s.trainer)?.ai !== 'smart';
      if (s.op === 'run' && !seen.has(s.ref)) {
        seen.add(s.ref);
        const inner = getScript(s.ref);
        const r = inner ? walk(inner) : undefined;
        if (r !== undefined) return r;
      }
      if (s.op === 'choice') return false; // what follows depends on the player
    }
    return undefined;
  };
  return walk(steps) ?? false;
}
