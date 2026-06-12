/**
 * Content registry contracts.
 *
 * These are the shapes for the game's *authored* content that isn't a kin/move
 * (those live in data/). Dialogue, cutscene scripts, items, starters and trainers
 * are all data: adding an NPC's lines, a cutscene, or an item is an edit to the
 * matching registry in this folder, never new engine code. Maps reference these
 * by string ref (e.g. EventTrigger.ref = 'sign.tinderwick_dock').
 */
import type { TileCoord, Facing, WorldFlag, AbilityId, EncounterTerrain } from '@game/data/world/types';
import type { Region } from '@game/data/world/graph';
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

/**
 * A LEGENDARY (or other one-off) set-piece catch with a battles-won failure
 * cooldown. The kin is a fixed wild battle that the kin itself cannot flee
 * (player flee is still allowed); the encounter is a CHANCE, not a gift, so a
 * miss has a cost.
 *
 *  - Already caught (`caughtFlag` held): the op falls through silently. Normal
 *    practice is to also `hidden_when_flag: caughtFlag` the trigger/NPC that runs
 *    the script, so a caught legendary never re-stages; the op's own check is the
 *    belt-and-braces.
 *  - On cooldown (it withdrew after a recent failure): the op plays `cooldownRef`
 *    — an ordinary dialogue ref (content/dialogue.ts), the diegetic hint — and
 *    ends the encounter. The line may include the token `{remaining}`, replaced
 *    with the number of battles the player must still WIN before it returns.
 *  - Ready: runs the set-piece wild battle. Outcomes:
 *      · caught  -> sets `caughtFlag` (the kin joins via the normal catch path:
 *                   party/Hearth + dex), encounter over for good.
 *      · KO'd / player fled -> the kin withdraws: a cooldown of `cooldownBattles`
 *                   WON battles is stamped under `name`. It cannot be re-fought
 *                   until that many victories have passed.
 *
 * Worked inline example (a content script in content/scripts.ts):
 *   'script.tide_sovereign': [
 *     { op: 'narrate', text: 'The water draws back, and something vast and patient lifts its head.' },
 *     { op: 'music', key: 'battle-legendary-tide' },
 *     { op: 'legendaryBattle',
 *       name: 'tide_sovereign',          // cooldown key (any stable string)
 *       kin: 137, level: 45,             // species id + level of the set-piece kin
 *       caughtFlag: 'flag:tide_sovereign_caught',
 *       cooldownBattles: 12,             // withdraws for 12 WON battles on a miss
 *       cooldownRef: 'npc.tide_sovereign_resting', // hint line, may use {remaining}
 *       terrain: 'water' },              // optional: lets conditional charges apply
 *   ],
 * with the hint line in content/dialogue.ts:
 *   'npc.tide_sovereign_resting': [
 *     { text: 'The tide lies flat and sullen. The Sovereign sank deep when you faltered; the water will not give it up for {remaining} more battles yet.' },
 *   ],
 * and the trigger that fires it carrying `hidden_when_flag: 'flag:tide_sovereign_caught'`.
 */
export interface LegendaryBattleStep {
  op: 'legendaryBattle';
  /** Stable cooldown key (also the `cooldowns` record key). */
  name: string;
  /** Species id of the set-piece kin. */
  kin: number;
  /** Level it appears at. */
  level: number;
  /** Flag set when the kin is caught — gate the staging trigger on this too. */
  caughtFlag: WorldFlag;
  /** Battles the player must WIN after a failed catch before it returns. */
  cooldownBattles: number;
  /** Dialogue ref for the diegetic "it withdrew" hint; may contain `{remaining}`. */
  cooldownRef: string;
  /** Encounter terrain (optional) — lets conditional charges (e.g. a water charm) apply. */
  terrain?: EncounterTerrain;
}

/**
 * A single cutscene instruction. The CutsceneRunner interprets these in order.
 * Any step may carry `if_flag`: the step plays only while that flag is held and
 * is silently skipped otherwise — the data-level conditional for small payoffs
 * (e.g. Wren's ribbon line at Nightreach fires only on `flag:q_north_ribbon_placed`).
 * Keep guarded steps OPTIONAL colour, never progression (a skipped setFlag is a bug).
 */
export type CutsceneStep = CutsceneStepBase & { if_flag?: WorldFlag };

type CutsceneStepBase =
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
  // Grant `item` ONLY if the player holds none, narrating `text` when it grants
  // (a quiet no-op otherwise). The safety-net op for must-have set-piece items —
  // the Keylumen dais re-offers the Starlamp with it, so the ending can never
  // dangle on a spent key item.
  | { op: 'ensureItem'; item: string; count?: number; text?: string }
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
  | LegendaryBattleStep // a static one-off catch with a battles-won failure cooldown
  | { op: 'heal' } // fully restore the party (inn rest, hearthside kindness)
  | { op: 'gleam'; element: string } // diegetic Gleam cue (relight the sky)
  | { op: 'giveMoney'; amount: number } // hand the player wicks (quest rewards, finds)
  | { op: 'shop'; shop: string } // open a shop's buy/sell counter (content/shops.ts)
  /**
   * Hand the world over to a full-screen CinematicScript (content/cinematics.ts)
   * — the endgame's dawn panels + credits roll. The host PERSISTS first (so a
   * Continue after the roll resumes exactly here, flags included), then starts
   * CinematicScene; nothing after this step plays, so make it the script's LAST
   * step and set any progression flags (e.g. flag:dawn) BEFORE it.
   */
  | { op: 'cinematic'; id: string };
// (per-step `if_flag` guard rides the CutsceneStep intersection above)

/** ref -> a cutscene's steps. */
export type ScriptRegistry = Record<string, CutsceneStep[]>;

// ---- Items ------------------------------------------------------------------

export type ItemCategory = 'charge' | 'medicine' | 'chart' | 'valuable' | 'key' | 'misc';

/**
 * Condition on a *conditional* charge (docs/mechanics/04-capture.md, "Specialty
 * charges"): the charge's `catch_bonus` applies only while the condition holds —
 * otherwise the throw burns the charge at a plain ×1.0. Evaluated at throw time
 * by the BattleScene (it knows the foe, the encounter terrain and the turn).
 * Data-shaped so new specialty charges are an items.ts edit, never engine code.
 */
export type ChargeCondition =
  | { kind: 'terrain'; terrain: EncounterTerrain } // met in this encounter terrain (e.g. Drift Charm on water)
  | { kind: 'hp_below'; ratio: number } // target's hp/maxHp strictly below ratio (e.g. 0.25)
  | { kind: 'status'; status: string } // target afflicted by this exact status (e.g. 'doze')
  | { kind: 'any_status' } // target afflicted by anything at all
  | { kind: 'defender_type'; types: string[] } // target carries one of these types (e.g. Lunar/Dark)
  | { kind: 'first_turn' }; // thrown on the encounter's first turn (the gamble throw)

export interface ItemDef {
  id: string;
  name: string;
  desc: string;
  category: ItemCategory;
  /**
   * Capture multiplier for 'charge' items — a waxed charge cell fed to the
   * vesperlamp for one boosted throw (a plain, chargeless throw = 1.0; a value
   * of 255 is a guaranteed catch, e.g. the Starlamp).
   */
  catch_bonus?: number;
  /**
   * For *conditional* charges only: `catch_bonus` applies while this holds,
   * otherwise the throw falls back to plain ×1.0 (the charge is still spent).
   * Unconditional charges simply omit it — they behave exactly as before.
   */
  condition?: ChargeCondition;
  /** For 'key' Kindlestone-type items: fires a kin's stone-trigger kindling. */
  kindle_stone?: boolean;
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
/** One stocked line: a plain item id, or one that only appears once a flag is
 *  held (e.g. Beacon Charges appearing after the first Gleam). */
export type ShopStockEntry = string | { item: string; requires_flag: WorldFlag };

export interface ShopDef {
  id: string;
  /** Counter title, e.g. 'TINDERWICK GENERAL'. */
  name: string;
  /** Items stocked, in display order. Every id must have a `price`. */
  stock: ShopStockEntry[];
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

// ---- Quests (the journal) ---------------------------------------------------

/**
 * One named quest in the Wayfarer's journal (pause menu -> JOURNAL). Data only:
 * the quest's flags are MINED from the built content (scripts.ts/maps) — a QuestDef
 * never invents a flag, it just surfaces the journey the game already runs.
 *
 * Visibility/progress all ride flags:
 *  - the quest appears in the journal only once `start_flag` is held (no spoilers);
 *  - it sits under UNDERWAY until `done_flag` is held, then moves to KEPT;
 *  - `stage_flags` (optional, ORDERED) drive the "n/m" progress readout — n = how
 *    many are held. For a counted quest (P1's ten letters) set `count_prefix`
 *    instead: the journal counts held flags matching the prefix (FlagStore.countHeld)
 *    against `count_total`, so a no-schema boolean fan-out reads as "n/10".
 */
export interface QuestDef {
  /** Stable id (also the journal's within-region display order = array order). */
  id: string;
  /** Title as it reads in the walkthrough, e.g. 'The Last Buoy Out'. */
  name: string;
  /** Which corner of Vesperholm it belongs to (journal grouping). */
  region: Region;
  /** Who gives it, for the detail pane (e.g. 'the netmender'). */
  giver: string;
  /** 1-2 sentences, canon voice — what the player is doing and why. */
  blurb: string;
  /** Quest enters the journal once this is held. */
  start_flag: WorldFlag;
  /** Quest moves to KEPT once this is held. */
  done_flag: WorldFlag;
  /** Optional ordered milestone flags — progress shown as held/total. */
  stage_flags?: WorldFlag[];
  /** Optional counted progress: held flags matching this prefix / count_total. */
  count_prefix?: string;
  /** Denominator for count_prefix progress (e.g. 10 letters). */
  count_total?: number;
}

export type QuestRegistry = readonly QuestDef[];

// ---- Charts (concept-art discovery) -----------------------------------------

/**
 * One discoverable "chart" in the Wayfarer's Charts gallery (pause menu -> CHARTS):
 * an area/route/landmark's mood piece (the concept art in `assets/concept-art/`),
 * surfaced in-game. The first time the player sets foot in any of `maps`, the chart
 * is discovered — a full-screen reveal plays and it joins the gallery; until then it
 * shows as a "? ? ?" tease so the world's shape (and what's left to find) is visible
 * without spoiling it. Charts are grouped by `region` so a player can feel they've
 * missed a corner of a place. A chart with an empty `maps` list is a forward tease
 * for content not yet built (e.g. the Lanternway) — permanently locked until a map
 * id is added here.
 */
export interface ChartEntry {
  /** Stable id; matches the concept-art filename stem (e.g. 'dimglass-coast'). */
  id: string;
  /** The place's name, revealed once discovered. */
  name: string;
  /** A short mood line (the subtitle on the reveal + the gallery's detail pane). */
  subtitle: string;
  /** Which corner of Vesperholm this sits in (gallery grouping). */
  region: Region;
  /** Coarse kind for the gallery's little tag. */
  kind: 'area' | 'route' | 'landmark';
  /** Served path to the concept art (runtime drops the public/ prefix). */
  art: string;
  /** Map ids whose first visit discovers this chart (may be empty = forward tease). */
  maps: string[];
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
   * Foe AI tier: 'smart' plays the matchup (type awareness, KO recognition,
   * status/utility timing) — set it on Lampwardens, the rival's later fights,
   * and Còr. Route trainers stay on the default 'basic' pick.
   */
  ai?: 'basic' | 'smart';
  /**
   * Wicks paid out when the player wins. Authored to the economy formula
   * (docs/mechanics/10-economy.md): payout = class rate × ace level — route
   * trainer 16, dungeon keeper 20, rival 24, Lampwarden 60, Còr 120. Re-run
   * `node tools/balance/progression.mjs` after changing payouts.
   */
  payout?: number;
}

export type TrainerRegistry = Record<string, TrainerDef>;
