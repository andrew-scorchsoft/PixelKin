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
import { fadeIn, fadeOut, flash } from '@game/ui/Transitions';
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
  startTrainerBattle?(trainer: string): Promise<void>;
}

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

async function runStep(ctx: CutsceneContext, step: CutsceneStep): Promise<void> {
  const { scene } = ctx;
  switch (step.op) {
    case 'say':
      await new DialogueBox(scene, ctx.sfx).run([{ speaker: step.speaker, text: step.text }]);
      return;
    case 'dialogue':
      await new DialogueBox(scene, ctx.sfx).run(getDialogue(step.ref));
      return;
    case 'wait':
      await delay(scene, step.ms);
      return;
    case 'move': {
      const actor = ctx.getActor(step.actor);
      if (actor) await walkTo(actor, step.to.tx, step.to.ty, ctx.canEnter);
      return;
    }
    case 'face': {
      ctx.getActor(step.actor)?.setFacing(step.facing);
      return;
    }
    case 'fade':
      if (step.dir === 'out') await fadeOut(scene, step.ms);
      else await fadeIn(scene, step.ms);
      return;
    case 'setFlag':
      ctx.flags.set(step.flag, step.value ?? true);
      return;
    case 'giveStarter': {
      const speciesId = await new StarterSelect(scene, ctx.sfx).run();
      ctx.onGiveStarter(speciesId);
      void ctx.sfx.play('dex-register');
      return;
    }
    case 'giveItem':
      ctx.onGiveItem(step.item, step.count ?? 1);
      void ctx.sfx.play('world-pickup');
      return;
    case 'sfx':
      void ctx.sfx.play(step.key);
      return;
    case 'music':
      if (step.key === null) ctx.music.stop();
      else void ctx.music.play(step.key, `assets/audio/music/${step.key}.mp3`);
      return;
    case 'battle':
      if (ctx.startTrainerBattle) await ctx.startTrainerBattle(step.trainer);
      return;
    case 'gleam':
      void ctx.sfx.playVariant('world-gleam', ['a', 'b', 'c']);
      await flash(scene, 220);
      return;
  }
}

export async function runCutscene(ctx: CutsceneContext, steps: CutsceneStep[]): Promise<void> {
  for (const step of steps) await runStep(ctx, step);
}
