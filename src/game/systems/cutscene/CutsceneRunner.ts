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
import type { Facing, EncounterTerrain } from '@game/data/world/types';
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
  /** Hand the player a specific kin at a level (a gift kin); joins party or Hearth. */
  onGiveKin?(speciesId: number, level: number): void;
  onGiveItem(item: string, count: number): void;
  /** Whether the player currently holds at least one of `item` (ensureItem's gate). */
  hasItem?(item: string): boolean;
  /** Run a trainer battle; resolves true if the player won (false aborts the scene). */
  startTrainerBattle?(trainer: string): Promise<boolean>;
  /**
   * Where a battle-counted cooldown stands for a named one-off encounter.
   *  - 'caught'   : `caughtFlag` is held — the encounter is done forever.
   *  - 'cooldown' : it withdrew after a recent failure; `remaining` battles to go.
   *  - 'ready'    : fightable now.
   */
  legendaryState?(name: string, caughtFlag: string): { phase: 'caught' | 'cooldown' | 'ready'; remaining: number };
  /**
   * Run a SET-PIECE wild battle (the kin can't flee; the player can). Resolves the
   * raw outcome so the runner can branch: a catch sets the caughtFlag, a KO/flee
   * stamps the cooldown.
   */
  startSetPieceBattle?(kin: number, level: number, terrain?: EncounterTerrain): Promise<'caught' | 'koed' | 'fled' | 'lost'>;
  /** Stamp a `cooldownBattles`-long (in WON battles) withdrawal under `name`. */
  setLegendaryCooldown?(name: string, cooldownBattles: number): void;
  /** Fully restore the party (the inn-rest / hearthside-heal op). `rest` (default
   *  true) also banks the spot as the blackout wake-point. */
  onHealParty?(rest: boolean): void;
  /** Hand the player wicks (quest rewards, found purses). */
  onGiveMoney?(amount: number): void;
  /** Open a shop counter by id (mutates inventory + wicks via the host). */
  openShop?(shopId: string): Promise<void>;
  /** Pan/zoom the camera onto a world tile (host supplies tile→pixel + freeze). */
  cameraFocusTile?(tx: number, ty: number, ms: number, zoom?: number): Promise<void>;
  /** Re-follow the player and restore zoom after a focus. */
  cameraReset?(ms: number): Promise<void>;
  /**
   * Persist the save, then hand the whole screen to a CinematicScript
   * (CinematicScene). The world scene ends here — the runner aborts the
   * remaining steps, so the op belongs at the very end of a script.
   */
  startCinematic?(id: string): Promise<void>;
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
    if (actor.tx === tx && actor.ty === ty) break;
    let facing: Facing;
    if (actor.tx < tx) facing = 'right';
    else if (actor.tx > tx) facing = 'left';
    else if (actor.ty < ty) facing = 'down';
    else facing = 'up';
    const ok = await stepAsync(actor, facing, canEnter);
    if (!ok) break;
  }
  // Settle the walk cycle onto the idle pose. The continuous-run loop relies on the
  // per-frame `stopWalking()` in the world update, which is gated off while a scene
  // runs — so without this the actor jogs in place until the world loop resumes.
  actor.stopWalking();
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
    case 'giveKin': {
      ctx.onGiveKin?.(step.kin, step.level);
      void ctx.sfx.play('dex-register');
      return true;
    }
    case 'giveItem':
      ctx.onGiveItem(step.item, step.count ?? 1);
      void ctx.sfx.play('world-pickup');
      return true;
    case 'ensureItem': {
      // Safety net for must-have set-piece items: grant only when the player
      // holds none (a spent Starlamp must not strand the Keylumen asking).
      if (ctx.hasItem?.(step.item)) return true;
      ctx.onGiveItem(step.item, step.count ?? 1);
      void ctx.sfx.play('world-pickup');
      if (step.text) await new DialogueBox(scene, ctx.sfx).run([{ text: step.text, style: 'narrate' }]);
      return true;
    }
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
    case 'legendaryBattle': {
      // A static one-off catch with a battles-won failure cooldown. The host owns
      // the bookkeeping (battles_won / cooldowns); the runner just orchestrates the
      // diegetic flow. Missing host hooks degrade to a silent no-op.
      if (!ctx.legendaryState || !ctx.startSetPieceBattle) return true;
      const state = ctx.legendaryState(step.name, step.caughtFlag);
      if (state.phase === 'caught') return true; // already ours — fall through quietly
      if (state.phase === 'cooldown') {
        // It withdrew after a recent miss — play the hint, substituting {remaining}.
        const lines = getDialogue(step.cooldownRef).map((l) => ({
          ...l,
          text: l.text.replace(/\{remaining\}/g, String(state.remaining)),
        }));
        await new DialogueBox(scene, ctx.sfx).run(lines);
        return false; // end the scene here — the encounter isn't available yet
      }
      // Ready: run the set-piece. The kin can't flee; the player can.
      const outcome = await ctx.startSetPieceBattle(step.kin, step.level, step.terrain);
      if (outcome === 'caught') {
        ctx.flags.set(step.caughtFlag, true);
        return true; // let the script narrate the catch
      }
      if (outcome === 'lost') return false; // party wiped — the host's blackout takes over
      // KO'd or the player fled: the kin withdraws for a spell.
      ctx.setLegendaryCooldown?.(step.name, step.cooldownBattles);
      return false; // a failed catch doesn't narrate a triumphant tail
    }
    case 'heal':
      ctx.onHealParty?.(step.rest !== false);
      void ctx.sfx.playVariant('world-heal', ['a', 'b']);
      return true;
    case 'giveMoney':
      ctx.onGiveMoney?.(step.amount);
      void ctx.sfx.playVariant('world-pickup', ['a', 'b', 'c']);
      return true;
    case 'shop':
      await ctx.openShop?.(step.shop);
      return true;
    case 'gleam': {
      void ctx.sfx.playVariant('world-gleam', ['a', 'b', 'c']);
      // A short triumphant fanfare for relighting a constellation (one-shot, over the bed).
      ctx.music.playSting('gleam-fanfare', MUSIC_URL('gleam-fanfare'), 0.6);
      await flash(scene, 220);
      return true;
    }
    case 'cinematic':
      // The hand-over: the host persists, then starts CinematicScene. The world
      // scene is being replaced, so end the cutscene here (nothing after plays;
      // any progression flags must have been set by earlier steps).
      await ctx.startCinematic?.(step.id);
      return false;
  }
}

/** Play a scene's steps in order. Returns true if it ran to completion (not aborted). */
export async function runCutscene(ctx: CutsceneContext, steps: CutsceneStep[]): Promise<boolean> {
  for (const step of steps) {
    // Per-step guard: an `if_flag` step plays only while that flag is held —
    // the data-level conditional for optional colour (never progression).
    if (step.if_flag && !ctx.flags.get(step.if_flag)) continue;
    const carryOn = await runStep(ctx, step);
    if (!carryOn) return false;
  }
  return true;
}
