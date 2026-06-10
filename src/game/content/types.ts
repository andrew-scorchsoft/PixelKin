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

/** One screen of text, optionally attributed to a speaker.
 *  `portrait`/`expr` show a character bust (see content/portraits.ts); `style`
 *  switches between attributed speech and un-attributed narration. All optional,
 *  so existing dialogue keeps rendering exactly as before. */
export interface DialogueLine {
  speaker?: string;
  text: string;
  portrait?: string; // portrait registry id, e.g. 'fenn'
  expr?: string; // expression name within that portrait, e.g. 'warm'
  style?: 'speech' | 'narrate';
}

/** ref -> ordered pages of dialogue. */
export type DialogueRegistry = Record<string, DialogueLine[]>;

// ---- Cutscene scripts -------------------------------------------------------

/** An actor in a cutscene: the player, or an NPC by its placement id on the map. */
export type ActorRef = 'player' | string;

/** A single cutscene instruction. The CutsceneRunner interprets these in order. */
export type CutsceneStep =
  | { op: 'say'; speaker?: string; text: string; portrait?: string; expr?: string; style?: 'speech' | 'narrate' }
  | { op: 'narrate'; text: string } // un-attributed, full-width prose (a say with style:'narrate')
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
  | { op: 'music'; key: string | null } // swap the bed (crossfades when one is playing)
  | { op: 'musicCrossfade'; key: string; ms?: number } // explicit crossfade to a new bed
  | { op: 'musicFade'; ms?: number } // fade the current bed to silence
  | { op: 'musicSting'; key: string; volume?: number } // one-shot cue over the current bed
  | { op: 'silence'; ms: number } // fade to silence and hold — the dread beat
  | { op: 'letterbox'; on: boolean; ms?: number } // cinematic bars in/out
  | { op: 'shake'; ms: number; intensity?: number } // camera shake
  | { op: 'tint'; color: string; alpha?: number; ms?: number } // full-screen colour wash
  | { op: 'flashColor'; color: string; ms?: number } // a coloured flash (cyan default via 'gleam')
  | { op: 'cameraFocus'; actor?: ActorRef; to?: TileCoord; ms?: number; zoom?: number } // pan/zoom onto a subject
  | { op: 'cameraReset'; ms?: number } // re-follow the player, restore zoom
  | { op: 'battle'; trainer: string } // start a trainer battle by id
  | { op: 'heal' } // fully restore the party (inn rest, hearthside kindness)
  | { op: 'gleam'; element: string } // diegetic Gleam cue (relight the sky)
  | { op: 'giveMoney'; amount: number } // hand the player wicks (quest rewards, finds)
  | { op: 'shop'; shop: string }; // open a shop's buy/sell counter (content/shops.ts)

/** ref -> a cutscene's steps. */
export type ScriptRegistry = Record<string, CutsceneStep[]>;

// ---- Items ------------------------------------------------------------------

export type ItemCategory = 'lamp' | 'medicine' | 'chart' | 'valuable' | 'key' | 'misc';

export interface ItemDef {
  id: string;
  name: string;
  desc: string;
  category: ItemCategory;
  /** Capture multiplier for 'lamp' items (vesperlamp = 1.0). */
  catch_bonus?: number;
  /** HP restored for 'medicine' items. */
  heal?: number;
  /**
   * Shop price in wicks. An item with no price is never stocked or buyable
   * (key items, quest charms). Sell value defaults to half price — see
   * content/economy.ts `sellValue()`; 'valuable' items set `sell` explicitly.
   */
  price?: number;
  /** Explicit sell value in wicks (overrides the half-price default). */
  sell?: number;
  /** For 'chart' items (Star-charts): the move id this chart teaches. */
  teach_move?: string;
}

export type ItemRegistry = Record<string, ItemDef>;

// ---- Shops ------------------------------------------------------------------

/**
 * A shop's counter: what the keeper stocks, in display order. Prices come from
 * each ItemDef (`price`), so one item costs the same across Vesperholm; a shop
 * is purely a *selection*. Opened by the cutscene op `{ op: 'shop', shop: id }`,
 * so a keeper script can chat first and trade after — pure data either way.
 */
export interface ShopDef {
  id: string;
  /** Counter title, e.g. 'TINDERWICK GENERAL'. */
  name: string;
  /** Item ids stocked, in display order. Every id must have a `price`. */
  stock: string[];
}

export type ShopRegistry = Record<string, ShopDef>;

// ---- Glossary ---------------------------------------------------------------

/**
 * One entry in the in-vesperlamp glossary (pause menu -> LORE): a canon term and
 * its cosy, lore-true definition. `unlock_flag` staggers discovery — an entry with
 * no flag is known from the start (a thing every Vesperholm child grows up with),
 * one with a flag stays a "? ? ?" tease until that flag is set, so the codex visibly
 * fills in as the player learns the world. We deliberately reuse flags the journey
 * already sets (e.g. `gleam:ember`, `flag:dusk_begins`), so staggering costs no new
 * story wiring.
 */
export interface GlossaryEntry {
  /** Stable id (also the display order is the registry's array order). */
  id: string;
  /** The term as it reads in dialogue, e.g. 'Gleam', 'the Hollowing'. */
  term: string;
  /** 2-3 sentences, canon voice, wrappable to the detail pane. */
  desc: string;
  /** When omitted, always known; when set, revealed once that flag/gleam is held. */
  unlock_flag?: WorldFlag;
}

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
  /**
   * Wicks paid out when the player wins. Authored to the economy formula
   * (docs/mechanics/10-economy.md): payout = class rate × ace level — route
   * trainer 16, dungeon keeper 20, rival 24, Lampwarden 60, Còr 120. Re-run
   * `node tools/balance/progression.mjs` after changing payouts.
   */
  payout?: number;
}

export type TrainerRegistry = Record<string, TrainerDef>;
