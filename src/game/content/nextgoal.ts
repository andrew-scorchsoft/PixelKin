/**
 * The pause menu's NEXT line: the main journey's current step in a few plain
 * words (playtest 2026-10: getting lost was the commonest complaint, and the
 * answer lived only with Andrew on a fence or deep in the JOURNAL).
 *
 * It mirrors `script.andrew_hint` stage for stage (same flags), but short:
 * compass + landmark + who. Ordered LATEST stage first and the first held flag
 * wins, so an old save holding a later flag without an earlier one still reads
 * one true line. Add a stage here whenever Andrew's chain gains one.
 */
import type { WorldFlag } from '@game/data/world/types';

interface GoalStage {
  /** Held → this is the current step (no flag = the very start). */
  flag?: WorldFlag;
  text: string;
}

export const NEXT_GOALS: GoalStage[] = [
  // the Farlamp Isles (optional post-game; walkthrough/10 Part I) — once begun
  { flag: 'flag:isles_dawn', text: 'The Farlamp burns. Battle Bram Fathom on Driftholm\'s quay.' },
  { flag: 'flag:q_isles_driftholm', text: 'Take Elder Creel\'s well-stair under the sea to the drowned Farlamp, and light it.' },
  { flag: 'flag:q_isles_fogglass', text: 'Follow the lit buoys south through the Fogwall to Driftholm.' },
  { flag: 'flag:q_isles_afloat', text: 'Row south across the Sound; find the old keepers\' fog-glass in the sea-caves under the isles.' },
  { flag: 'flag:q_isles_prow_lit', text: 'Take the lit prow-lamp back to Ione on Lightkeeper\'s Point.' },
  { flag: 'flag:q_isles', text: 'Have Fenn light Ione\'s prow-lamp, at Dawnstead on the front.' },
  { flag: 'flag:dawn', text: 'Look up. Then walk down to Dawnstead and see the valley in the morning.' },
  { flag: 'flag:keystar_relit', text: 'The Keystar is lit. Stand still and let what comes, come.' },
  { flag: 'gleam:lunar', text: 'The Crown is whole: climb the Umbral Spire, up the mountain road north of the Vesper Crossroads.' },
  { flag: 'gleam:solar', text: 'Lunar Gleam: Nessa Cole at Nightreach Observatory, top of the Sunvault Climb.' },
  { flag: 'gleam:frost', text: 'Solar Gleam: Lucan Pyre in the Sunken Solarium, west through Hushfrost Pass.' },
  { flag: 'gleam:storm', text: 'Frost Gleam: Ysolde Frost at the Pale Vault Glacier, up the Windward Stair.' },
  { flag: 'gleam:stone', text: 'Storm Gleam: Mira Vael on the Galehigh Terraces, up Cinderwind Scarp.' },
  { flag: 'gleam:verdant', text: 'Stone Gleam: Otho Grist at Cinderhead Mine, through the deep wood behind Lowleaf.' },
  { flag: 'gleam:tide', text: 'Verdant Gleam: Sable Quill at Lowleaf Hollow, east of Pearlmoor on the fen road.' },
  { flag: 'flag:q_south_bell_rung', text: 'Tide Gleam: face Reyl Wash at the Lumenary atop Pearlmoor Quay.' },
  { flag: 'flag:q_south_has_rope', text: 'Ring the moor-bell at the far end of Pearlmoor\'s breakwater.' },
  { flag: 'flag:q_south_jest_done', text: 'Take the floats to the netmender on Pearlmoor Quay.' },
  { flag: 'flag:q_south_bell', text: 'Climb the Old Light on the Point, west of Pearlmoor Quay.' },
  { flag: 'gleam:ember', text: 'Go to Pearlmoor Quay, north up the coast, and see Reyl Wash at its Lumenary.' },
  { flag: 'flag:has_beacon_wick', text: 'Climb Tinderwick\'s Beacon on the north-east bluff to the lantern room.' },
  { flag: 'flag:beacon_quest', text: 'Fetch the Beacon\'s wick-key from the lamplighter on the Dimglass Coast.' },
  { flag: 'flag:caught_first_kin', text: 'See Brisa Tallow at Tinderwick\'s Lumenary.' },
  { flag: 'flag:has_starter', text: 'Catch a wild kin in the verge grass with your vesperlamp.' },
  { flag: 'flag:has_satchel', text: 'Take Fenn\'s satchel back to him at the Vesper Crossroads waystone.' },
  { flag: 'flag:fenn_errand', text: 'Find Fenn\'s satchel on the courier\'s cart in Duskapple Orchard, west of Tinderwick.' },
  { text: 'Meet Star-tender Fenn at the Vesper Crossroads waystone, east along the Lanternway.' },
];

/** The current step for whatever flags are held. */
export function nextGoal(held: (flag: WorldFlag) => boolean): string {
  return (NEXT_GOALS.find((g) => !g.flag || held(g.flag)) ?? NEXT_GOALS[NEXT_GOALS.length - 1]).text;
}
