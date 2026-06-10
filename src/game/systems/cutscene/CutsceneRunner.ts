/**
 * CutsceneRunner — interprets a CutsceneStep[] (from content/scripts.ts) as an
 * async sequence: walk actors, speak, fade, set flags, give the starter/items,
 * start a trainer battle, play a Gleam cue. Scene-agnostic: it talks to the world
 * through a CutsceneContext the host (WorldScene) supplies, so cutscenes are data,
 * not bespoke code. `await runCutscene(ctx, steps)` resolves when the scene ends.
 */
import Phaser from 'phaser';
import type { CutsceneStep, ActorRef } from '@game/content/types';
import type { Actor } from '@game/entities/Actor';
import type { Facing } from '@game/data/world/types';
import { DialogueBox } from '@game/ui/DialogueBox';
import { StarterSelect } from '@game/ui/StarterSelect';
import { fadeIn, fadeOut, flash, flashColor, shake, tint, letterbox } from '@game/ui/Transitions';
import { hex } from '@game/ui/theme';
import { getDialogue } from '@game/content/dialogue';
import type { FlagStore } from '@game/systems/flags/FlagStore';
import type { Sfx } from '@game/systems/audio/Sfx';
import type { MusicDirector } from '@game/systems/audio/MusicDirector';

export interface CutsceneContext {
  scene: Phaser.Scene;
  sfx: Sfx;
  music: MusicDirector;
  flags: FlagStore;
  getActor(ref: ActorRef): Actor | undefined;
  canEnter(tx: number, ty: number): boolean;
  onGiveStarter(speciesId: number): void;
  onGiveItem(item: string, count: number): void;
  /** Run a trainer battle; resolves true if the player won (false aborts the scene). */
  startTrainerBattle?(trainer: string): Promise<boolean>;
  /** Fully restore the party (the inn-rest / hearthside-heal op). */
  onHealParty?(): void;
  /** Pan/zoom the camera onto a world tile (host supplies tile→pixel + freeze). */
  cameraFocusTile?(tx: number, ty: number, ms: number, zoom?: number): Promise<void>;
  /** Re-follow the player and restore zoom after a focus. */
  cameraReset?(ms: number): Promise<void>;
}

const MUSIC_URL = (key: string): string => `assets/audio/music/${key}.mp3`;

function delay(scene: Phaser.Scene, ms: number): Promise<void> {
  return new Promise((resolve) => scene.time.delayedCall(ms, () => resolve()));
}

/** Step one tile and resolve when the move finishes (false if it was blocked). */
function stepAsync(actor: Actor, facing: Facing, canEnter: (tx: number, ty: number) => boolean): Promise<boolean> {
  return new Promise((resolve) => {
    const started = actor.step(facing, canEnter, () => resolve(true));
    if (!started) resolve(false);
  });
}

/** Walk an actor toward a tile (x then y), stopping if blocked. */
async function walkTo(
  actor: Actor,
  tx: number,
  ty: number,
  canEnter: (tx: number, ty: number) => boolean,
): Promise<void> {
  for (let guard = 0; guard < 64; guard++) {
    if (actor.tx === tx && actor.ty === ty) return;
    let facing: Facing;
    if (actor.tx < tx) facing = 'right';
    else if (actor.tx > tx) facing = 'left';
    else if (actor.ty < ty) facing = 'down';
    else facing = 'up';
    const ok = await stepAsync(actor, facing, canEnter);
    if (!ok) return;
  }
}

/** Run one step. Returns false to ABORT the rest of the scene (a lost battle). */
async function runStep(ctx: CutsceneContext, step: CutsceneStep): Promise<boolean> {
  const { scene } = ctx;
  switch (step.op) {
    case 'say':
      await new DialogueBox(scene, ctx.sfx).run([
        { speaker: step.speaker, text: step.text, portrait: step.portrait, expr: step.expr, style: step.style },
      ]);
      return true;
    case 'narrate':
      await new DialogueBox(scene, ctx.sfx).run([{ text: step.text, style: 'narrate' }]);
      return true;
    case 'dialogue':
      await new DialogueBox(scene, ctx.sfx).run(getDialogue(step.ref));
      return true;
    case 'wait':
      await delay(scene, step.ms);
      return true;
    case 'move': {
      const actor = ctx.getActor(step.actor);
      if (actor) await walkTo(actor, step.to.tx, step.to.ty, ctx.canEnter);
      return true;
    }
    case 'face': {
      ctx.getActor(step.actor)?.setFacing(step.facing);
      return true;
    }
    case 'emote': {
      await ctx.getActor(step.actor)?.showEmote(step.emote, step.holdMs);
      return true;
    }
    case 'action': {
      await ctx.getActor(step.actor)?.playAction(step.action, step.holdMs);
      return true;
    }
    case 'fade':
      if (step.dir === 'out') await fadeOut(scene, step.ms);
      else await fadeIn(scene, step.ms);
      return true;
    case 'setFlag':
      ctx.flags.set(step.flag, step.value ?? true);
      return true;
    case 'giveStarter': {
      const speciesId = await new StarterSelect(scene, ctx.sfx).run();
      ctx.onGiveStarter(speciesId);
      void ctx.sfx.play('dex-register');
      return true;
    }
    case 'giveItem':
      ctx.onGiveItem(step.item, step.count ?? 1);
      void ctx.sfx.play('world-pickup');
      return true;
    case 'sfx':
      void ctx.sfx.play(step.key);
      return true;
    case 'music':
      // Crossfade when a bed is already playing (smooth swaps); fade to silence on null.
      if (step.key === null) await ctx.music.fadeToSilence();
      else if (ctx.music.playingKey) await ctx.music.crossfade(step.key, MUSIC_URL(step.key));
      else await ctx.music.play(step.key, MUSIC_URL(step.key));
      return true;
    case 'musicCrossfade':
      await ctx.music.crossfade(step.key, MUSIC_URL(step.key), step.ms);
      return true;
    case 'musicFade':
      await ctx.music.fadeToSilence(step.ms);
      return true;
    case 'musicSting':
      ctx.music.playSting(step.key, MUSIC_URL(step.key), step.volume);
      return true;
    case 'silence':
      // The dread beat: fade the bed out and hold on the quiet.
      await ctx.music.fadeToSilence(Math.min(400, step.ms));
      await delay(scene, step.ms);
      return true;
    case 'letterbox':
      await letterbox(scene, step.on, step.ms);
      return true;
    case 'shake':
      await shake(scene, step.ms, step.intensity);
      return true;
    case 'tint':
      await tint(scene, hex(step.color), step.alpha, step.ms);
      return true;
    case 'flashColor':
      await flashColor(scene, step.ms, hex(step.color));
      return true;
    case 'cameraFocus': {
      const ms = step.ms ?? 600;
      let tx = step.to?.tx;
      let ty = step.to?.ty;
      if (step.actor) {
        const a = ctx.getActor(step.actor);
        if (a) {
          tx = a.tx;
          ty = a.ty;
        }
      }
      if (tx !== undefined && ty !== undefined) await ctx.cameraFocusTile?.(tx, ty, ms, step.zoom);
      return true;
    }
    case 'cameraReset':
      await ctx.cameraReset?.(step.ms ?? 600);
      return true;
    case 'battle':
      // A lost trainer battle aborts the scene (so a defeat never narrates a win).
      if (ctx.startTrainerBattle) return ctx.startTrainerBattle(step.trainer);
      return true;
    case 'heal':
      ctx.onHealParty?.();
      void ctx.sfx.playVariant('world-heal', ['a', 'b']);
      return true;
    case 'gleam': {
      void ctx.sfx.playVariant('world-gleam', ['a', 'b', 'c']);
      // A short triumphant fanfare for relighting a constellation (one-shot, over the bed).
      ctx.music.playSting('gleam-fanfare', MUSIC_URL('gleam-fanfare'), 0.6);
      await flash(scene, 220);
      return true;
    }
  }
}

/** Play a scene's steps in order. Returns true if it ran to completion (not aborted). */
export async function runCutscene(ctx: CutsceneContext, steps: CutsceneStep[]): Promise<boolean> {
  for (const step of steps) {
    const carryOn = await runStep(ctx, step);
    if (!carryOn) return false;
  }
  return true;
}
