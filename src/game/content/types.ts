/**
 * Content registry contracts.
 *
 * These are the shapes for the game's *authored* content that isn't a kin/move
 * (those live in data/). Dialogue, cutscene scripts, items, starters and trainers
 * are all data: adding an NPC's lines, a cutscene, or an item is an edit to the
 * matching registry in this folder, never new engine code. Maps reference these
 * by string ref (e.g. EventTrigger.ref = 'sign.tinderwick_dock').
 */
import type { TileCoord, Facing, WorldFlag, AbilityId } from '@game/data/world/types';
import type { ActionName, EmoteName } from '@game/entities/Actor';

// ---- Dialogue ---------------------------------------------------------------

/** One screen of text, optionally attributed to a speaker. */
export interface DialogueLine {
  speaker?: string;
  text: string;
}

/** ref -> ordered pages of dialogue. */
export type DialogueRegistry = Record<string, DialogueLine[]>;

// ---- Cutscene scripts -------------------------------------------------------

/** An actor in a cutscene: the player, or an NPC by its placement id on the map. */
export type ActorRef = 'player' | string;

/** A single cutscene instruction. The CutsceneRunner interprets these in order. */
export type CutsceneStep =
  | { op: 'say'; speaker?: string; text: string }
  | { op: 'dialogue'; ref: string }
  | { op: 'wait'; ms: number }
  | { op: 'move'; actor: ActorRef; to: TileCoord }
  | { op: 'face'; actor: ActorRef; facing: Facing }
  | { op: 'emote'; actor: ActorRef; emote: EmoteName; holdMs?: number } // pop a bubble above an actor
  | { op: 'action'; actor: ActorRef; action: ActionName; holdMs?: number } // play a one-shot pose
  | { op: 'fade'; dir: 'out' | 'in'; ms?: number }
  | { op: 'setFlag'; flag: WorldFlag; value?: boolean }
  | { op: 'giveStarter' } // run StarterSelect, add chosen kin to the party
  | { op: 'giveItem'; item: string; count?: number }
  | { op: 'sfx'; key: string }
  | { op: 'music'; key: string | null }
  | { op: 'battle'; trainer: string } // start a trainer battle by id
  | { op: 'gleam'; element: string }; // diegetic Gleam cue (relight the sky)

/** ref -> a cutscene's steps. */
export type ScriptRegistry = Record<string, CutsceneStep[]>;

// ---- Items ------------------------------------------------------------------

export type ItemCategory = 'lamp' | 'medicine' | 'key' | 'misc';

export interface ItemDef {
  id: string;
  name: string;
  desc: string;
  category: ItemCategory;
  /** Capture multiplier for 'lamp' items (vesperlamp = 1.0). */
  catch_bonus?: number;
  /** HP restored for 'medicine' items. */
  heal?: number;
}

export type ItemRegistry = Record<string, ItemDef>;

// ---- Starters ---------------------------------------------------------------

/** One option in the choose-your-starter screen. */
export interface StarterOption {
  species_id: number;
  /** One-line flavour shown under the portrait. */
  blurb: string;
}

// ---- Trainers ---------------------------------------------------------------

export interface TrainerKin {
  species_id: number;
  level: number;
}

export interface TrainerDef {
  id: string;
  name: string;
  /** Title shown in the VS intro, e.g. 'Lampwarden'. */
  title?: string;
  /** Battle-sprite/portrait key (optional in the first cut). */
  sprite?: string;
  party: TrainerKin[];
  intro_ref?: string; // dialogue before the fight
  defeat_ref?: string; // dialogue after losing
  /** Flags set when the player wins (e.g. the first Gleam). */
  reward_flags?: WorldFlag[];
  /**
   * Lantern Gifts (abilities) granted when the player wins — e.g. a Lampwarden
   * handing over the traversal Gift tied to their constellation. Added to the
   * player's ability set and persisted, so they survive a save/load and
   * immediately unlock gated tiles/warps.
   */
  reward_abilities?: AbilityId[];
  /** Battle music key override. */
  music?: string;
}

export type TrainerRegistry = Record<string, TrainerDef>;
