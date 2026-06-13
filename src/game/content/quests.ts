/**
 * Quest registry — the Wayfarer's journal (pause menu -> JOURNAL).
 *
 * One QuestDef per NAMED quest across the whole journey (the per-region walkthrough
 * files' §"Named quests" slates). Pure data: every flag here is MINED from the built
 * content (content/scripts.ts setFlag ops + the map JSON) — the journal never invents
 * a flag, it only surfaces the journey the game already runs. A quest appears in the
 * journal once its `start_flag` is held (so unstarted quests never spoil), shows live
 * progress off `stage_flags`/`count_prefix`, and moves to KEPT once its `done_flag` is
 * held. See QuestDef (content/types.ts) for the field contract and FlagStore.countHeld
 * for the N-of-M counter.
 *
 * Authoring: cosy, a little melancholy, canon vocabulary only. Keep each blurb to 1-2
 * sentences so it wraps cleanly in the detail pane (240x160). Add a later region's
 * quests here keyed to flags that region's scripts already set — never new wiring.
 *
 * LEFT OUT (flags not yet in the build, per the "mine, don't invent" rule):
 *  - the Verdant warden "bloom" line (E) — it is the Gleam-earn loop, not a side quest;
 *    its closure is `gleam:verdant`, already covered by the dex/atlas, so it is not a
 *    journal quest.
 *  - Round legs R1 "Wicks for the Lamplighter" / R2 "Salt-glass for the Chandler" /
 *    R3 "Moss for the Quay" — their `flag:q_round_lamplighter`/`_chandler`/`_moss` are
 *    NOT set anywhere in the build yet (the walkthrough flags them "remain to wire at
 *    vesper_crossroads"). Only R4 (`q_round_kite`) and R5 (`q_round_chart`) are wired,
 *    so the Round is journalled as one umbrella quest off the legs that exist, closing
 *    on C3's `q_central_round_done`.
 */
import type { QuestDef, QuestRegistry } from './types';

export const QUESTS: QuestRegistry = [
  // ===== SOUTH ===============================================================
  {
    id: 's1_last_buoy',
    name: 'The Last Buoy Out',
    region: 'south',
    giver: 'the netmender',
    blurb: 'Relight the netmender\'s three storm-dark buoys out in the Dimglass water — in order, quay-outward — and the moor will keep its sea-road lit.',
    start_flag: 'flag:q_south_buoys',
    stage_flags: ['flag:q_south_buoy_a', 'flag:q_south_buoy_b', 'flag:q_south_buoys_lit'],
    done_flag: 'flag:q_south_buoys_done',
  },
  {
    id: 's2_letter_for_fenn',
    name: 'A Letter for Fenn',
    region: 'south',
    giver: 'the house parent',
    blurb: 'Gran has a letter for old Fenn, watching the sky out on the flats. Carry it to him, then bring her word back home.',
    start_flag: 'flag:q_south_letter',
    stage_flags: ['flag:q_south_letter_given'],
    done_flag: 'flag:q_south_letter_done',
  },
  {
    id: 's3_cavern_light',
    name: 'The Cavern Keeps a Light',
    region: 'south',
    giver: 'the old fisher',
    blurb: 'The old fisher\'s wrecked boat still holds a lamp, deep in Tideglass Cavern. Relight it for him, and tell him it still burns.',
    start_flag: 'flag:q_south_wrecklamp',
    stage_flags: ['flag:q_south_wrecklamp_lit'],
    done_flag: 'flag:q_south_wrecklamp_done',
  },
  {
    id: 's4_booji_wooji',
    name: 'The Booji-Wooji Man',
    region: 'south',
    giver: 'Andy at the Lifting House',
    blurb: 'The quay\'s old strongman has a name nobody explains and a story nobody can check. Follow what the Lifting House knows out to the dark end of the breakwater.',
    start_flag: 'flag:q_south_booji',
    stage_flags: ['flag:q_south_booji_abdul', 'flag:q_south_booji_sid', 'flag:q_south_booji_met'],
    done_flag: 'flag:q_south_booji_done',
  },

  // ===== EAST ================================================================
  {
    id: 'e1_quiet_reeds',
    name: 'The Quiet Reeds',
    region: 'east',
    giver: 'the fen fisher',
    blurb: 'Three lantern-reeds have gone dark along the fen channels. Re-kindle them in order — though the last one may not want to light.',
    start_flag: 'flag:q_east_reeds',
    stage_flags: ['flag:q_east_reed_a', 'flag:q_east_reed_b', 'flag:q_east_reed_third'],
    done_flag: 'flag:q_east_reeds_done',
  },
  {
    id: 'e2_spores_for_stall',
    name: 'Spores for the Stall',
    region: 'east',
    giver: 'the Bloom stall-keeper',
    blurb: 'The festival stall is bare. Gather the gatherer\'s spore-caches from Glowmoss Deep — and shoo off whatever has squatted on the last one.',
    start_flag: 'flag:q_east_spores',
    stage_flags: ['flag:picked_spore_a', 'flag:picked_spore_b'],
    done_flag: 'flag:q_east_spores_done',
  },
  {
    id: 'e3_foremans_ledger',
    name: "The Foreman's Ledger",
    region: 'east',
    giver: 'the lone miner',
    blurb: 'An old crew\'s ledger was left in a side gallery when the dark came up. Recover it from Cinderhead Deep and carry it home.',
    start_flag: 'flag:q_east_ledger',
    stage_flags: ['flag:q_east_ledger_found'],
    done_flag: 'flag:q_east_ledger_done',
  },
  {
    id: 'e4_sunniest_house',
    name: 'The Sunniest House in the Dark',
    region: 'east',
    giver: 'Georgina, the Cat-keeper',
    blurb: 'Deep in the hollow lives a keeper who loves the dark and fills it with cats and fairy-lights. Find her cottage, fetch her bolted kitten, and she may share the secret of her dragon-cat.',
    start_flag: 'flag:q_east_georgina',
    stage_flags: ['flag:q_east_georgina_kitten', 'flag:georgina_beaten'],
    done_flag: 'flag:q_east_georgina_done',
  },

  // ===== NORTH ===============================================================
  {
    id: 'n1_crag_kettle',
    name: "The Crag-tender's Kettle",
    region: 'north',
    giver: 'the crag-tender',
    blurb: 'Pick the wind-burnt ledge-herb from a high Galehigh terrace and carry it up to the crag-tender\'s kettle.',
    start_flag: 'flag:q_north_kettle',
    done_flag: 'flag:q_north_kettle_done',
  },
  {
    id: 'n2_aurora_sketcher',
    name: 'The Aurora Sketcher',
    region: 'north',
    giver: 'the painter at the Aurora-watch',
    blurb: 'Stand with the painter at three quiet viewpoints while she works the aurora onto paper. Pure stillness, and no hurry.',
    start_flag: 'flag:q_north_sketch',
    stage_flags: ['flag:q_north_sketch_1', 'flag:q_north_sketch_2', 'flag:q_north_sketch_3'],
    done_flag: 'flag:q_north_sketch_done',
  },
  {
    id: 'n3_wrens_ribbon',
    name: "Wren's Ribbon",
    region: 'north',
    giver: 'Mira',
    blurb: 'Wren dropped a kite-ribbon at the Kite-rising. Carry it to the quiet Windward ledge where they sat, and leave it there — no words needed.',
    start_flag: 'flag:q_north_ribbon',
    done_flag: 'flag:q_north_ribbon_placed',
  },

  // ===== WEST ================================================================
  {
    id: 'x1_caretakers_lamp',
    name: "The Caretaker's Lamp",
    region: 'west',
    giver: 'the caretaker',
    blurb: 'A coldfog-touched kin sleeps at the caretaker\'s side. Fetch aurora-oil from Aurora Hollow and fill her lamp, so it sleeps a little easier.',
    start_flag: 'flag:q_west_caretaker',
    done_flag: 'flag:q_west_caretaker_done',
  },
  {
    id: 'x2_troupe_sun_mask',
    name: "The Troupe's Sun-mask",
    region: 'west',
    giver: 'a troupe player',
    blurb: 'The troupe\'s gilt sun-mask sank in a side room off the flooded halls. Dive the night-water and bring it back for the closing scene.',
    start_flag: 'flag:q_west_mask',
    done_flag: 'flag:q_west_mask_found',
  },
  {
    id: 'x3_charting_dark',
    name: 'Charting the Dark',
    region: 'west',
    giver: 'the junior watcher',
    blurb: 'Take star-readings from three high points for the junior watcher\'s chart — the bravest, out at the Coldfog edge, is hers to skip if you like.',
    start_flag: 'flag:q_west_chart',
    stage_flags: ['flag:q_west_chart_1', 'flag:q_west_chart_2', 'flag:q_west_chart_3'],
    done_flag: 'flag:q_west_chart_done',
  },

  // ===== CENTRAL =============================================================
  {
    id: 'c1_lamplings_trail',
    name: "Lampling's Trail",
    region: 'central',
    giver: 'the Waystone kid',
    blurb: 'Follow the plaza lamp-flickers the Waystone kid has spotted. They lead, at the last gutter, to Lampling itself.',
    start_flag: 'flag:q_central_trail',
    done_flag: 'flag:q_central_trail_done',
  },
  {
    id: 'c2_inns_empty_lamps',
    name: "The Inn's Empty Lamps",
    region: 'central',
    giver: 'the innkeeper',
    blurb: 'Bring one lamp-token from each quadrant\'s festival and hang all four in the crossroads inn.',
    start_flag: 'flag:q_central_tokens',
    stage_flags: ['flag:q_token_south', 'flag:q_token_east', 'flag:q_token_north', 'flag:q_token_west'],
    done_flag: 'flag:q_central_tokens_done',
  },
  {
    id: 'waykeepers_round',
    name: "The Waykeeper's Round",
    region: 'central',
    giver: 'the Waykeeper',
    blurb: 'The cross-region delivery line: one parcel per waking spoke, carried road to far-off road, until the whole lit ring has been walked at last.',
    start_flag: 'flag:q_round_kite',
    stage_flags: ['flag:q_round_kite', 'flag:q_round_chart'],
    done_flag: 'flag:q_central_round_done',
  },

  // ===== POST-GAME ===========================================================
  {
    id: 'p1_first_dawn_letters',
    name: 'First-Dawn Letters',
    region: 'central',
    giver: 'the Waykeeper',
    blurb: 'Carry the first-dawn letters out along every spoke — to Wren, to Fenn, and to all eight wardens\' towns. Any order; the roads are awake again.',
    start_flag: 'flag:q_post_letters',
    count_prefix: 'flag:q_post_letter_',
    count_total: 10,
    done_flag: 'flag:q_post_letters_done',
  },
  {
    id: 'p2_wick_for_cor',
    name: 'A Wick for Còr',
    region: 'central',
    giver: 'Fenn',
    blurb: 'Draw a wick from the Tinderwick Beacon\'s lantern room — the first made by daylight in years — and carry it to Còr at his lamp on Dawnstead.',
    start_flag: 'flag:q_post_wick',
    done_flag: 'flag:q_post_wick_given',
  },
  {
    id: 'p3_day_form_survey',
    name: 'The Day-form Survey',
    region: 'central',
    giver: 'Fenn',
    blurb: 'Show Fenn three day-forms — the early kin of the valleys, woken sun-changed by the relit sky — for his field-journal.',
    start_flag: 'flag:q_post_survey',
    stage_flags: ['flag:q_post_survey_1', 'flag:q_post_survey_2', 'flag:q_post_survey_3'],
    done_flag: 'flag:q_post_survey_done',
  },
  {
    id: 'starfall_vigils',
    name: 'The Starfall Vigils',
    region: 'west',
    giver: 'Watcher Oriel',
    blurb: 'Star-shards have fallen where the woken constellations settled. At each, a Vigilant has come out of retirement to keep watch — and to try the hand that came to keep it.',
    start_flag: 'flag:starfall_begun',
    stage_flags: [
      'flag:vigil_1_kept',
      'flag:vigil_2_kept',
      'flag:vigil_3_kept',
      'flag:vigil_4_kept',
      'flag:vigil_5_kept',
      'flag:starfall_lesson',
    ],
    done_flag: 'flag:starfall_crown',
  },
];

/** Lookup by id. */
export function getQuest(id: string): QuestDef | undefined {
  return QUESTS.find((q) => q.id === id);
}
