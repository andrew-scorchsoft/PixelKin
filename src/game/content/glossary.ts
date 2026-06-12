/**
 * Glossary — the in-vesperlamp codex of Vesperholm's vocabulary (pause menu -> LORE).
 *
 * The opening hour introduces a lot of bespoke words — kin, Gleam, Lumenary, the
 * Hollowing — and our player is a time-poor adult who may return after a week away.
 * This is their quiet reference: "what was a Gleam again?", answered in the lamp's
 * own keeping. Entries are ORDERED (the list shows them in this order); `unlock_flag`
 * staggers discovery off flags the journey already sets, so the codex fills in as the
 * world is learned without any new story wiring.
 *
 * Authoring: cosy, a little melancholy, canon vocabulary only (never
 * monster/gym/badge or another franchise's terms). Keep each `desc` to 2-3 sentences
 * so it wraps cleanly in the detail pane. Add new terms here as later regions
 * introduce them; pick an `unlock_flag` the relevant beat already raises.
 */
import type { GlossaryEntry } from './types';

export const GLOSSARY: readonly GlossaryEntry[] = [
  // --- Known from the first step (a thing every Vesperholm child grows up with) ---
  {
    id: 'vesperholm',
    term: 'Vesperholm',
    desc: 'Your homeland: a crescent of nine valleys around a darkened mountain, caught in a dusk that will not lift.',
  },
  {
    id: 'kin',
    term: 'Kin',
    desc: "The creatures you walk beside. Some carry a little of the sky's light — and to befriend one is to share it. You keep them; they keep you.",
  },
  {
    id: 'wayfaring',
    term: 'the Wayfaring',
    desc: "The coming-of-age walk: 'complete the map' — visit every valley, befriend its kin, learn its tale — and be counted a true wanderer.",
  },
  {
    id: 'vesperlamp',
    term: 'Vesperlamp',
    desc: 'The brass clamshell lantern gifted at the start of your Wayfaring. It holds the light you restore and grows brighter the further you walk.',
  },
  {
    id: 'lamp',
    term: 'Lamps',
    desc: "Throwable lanterns. You don't trap a wild kin — you coax its light to settle and rest inside, gently, with its leave.",
  },
  {
    id: 'kindling',
    term: 'Kindling',
    desc: 'How a kin grows: taking on more light and blazing into a brighter, stronger form. The same verb the whole journey turns on.',
  },
  {
    id: 'hearth',
    term: 'the Hearth',
    desc: 'The warm keep where your kin rest when not in your lamp. A full lamp just means the next friend waits for you by the fire.',
  },
  {
    id: 'skyweave',
    term: 'the Skyweave',
    desc: 'The old belief that the stars are tied to gleaming kin below — and that tending the light keeps dusk and dawn turning.',
  },
  {
    id: 'wicks',
    term: 'Wicks',
    desc: "Vesperholm's coin: waxed, brass-capped lamp-wicks, bundled and traded. In a land without dawn, everyone always needs one more.",
  },

  // --- Learned on the road (staggered off flags the journey already raises) ---
  {
    id: 'lumenary',
    term: 'Lumenary',
    desc: "A valley's lantern-hall, kept by its Lampwarden. Its Gleam isn't won by a fight alone — but by proving your bond is worth the sky.",
    unlock_flag: 'flag:beacon_quest',
  },
  {
    id: 'lampwarden',
    term: 'Lampwarden',
    desc: "Keeper of a valley's Lumenary and its constellation. Eight tend the rim; each will vouch for a Wayfarer who has truly bonded.",
    unlock_flag: 'flag:beacon_quest',
  },
  {
    id: 'gleam',
    term: 'Gleam',
    desc: "A relit constellation — a homecoming, not a trophy, given inside a town's festival. Each warms the dusk a shade; eight complete the Crown.",
    unlock_flag: 'gleam:ember',
  },
  {
    id: 'lamplight',
    term: 'Lamplight',
    desc: 'Your young lamp reaches only a small circle in the dark. Each Gleam you relight widens it, until you all but carry the dawn in hand.',
    unlock_flag: 'gleam:ember',
  },
  {
    id: 'lantern_fair',
    term: 'the Lantern-fair',
    desc: "Tinderwick's festival, the first most Wayfarers stand inside: the whole town out under strung lanterns, a Gleam given like a welcome home. A small flame's no lesser thing — that is the fair's whole sermon.",
    unlock_flag: 'gleam:ember',
  },
  {
    id: 'hollowing',
    term: 'the Hollowing',
    desc: "Not villains — frightened folk who'd let the long night come gently and stay. They put luminous kin to sleep and carry their light away.",
    unlock_flag: 'flag:dusk_begins',
  },
  {
    id: 'star_chart',
    term: 'Star-chart',
    desc: 'A pressed chart of one small constellation figure. A kin that studies it by lamplight learns to draw that figure in battle — one study burns the glow out.',
    unlock_flag: 'flag:has_starter',
  },
  {
    id: 'lantern_gift',
    term: 'Lantern Gift',
    desc: 'A knack a Lampwarden teaches with their Gleam — Tidecall crosses night-water; more come later. Each reopens places you once walked past.',
    unlock_flag: 'gleam:tide',
  },
  {
    id: 'tide_blessing',
    term: 'the Tide-blessing',
    desc: "Pearlmoor's festival: when the Moor-bell rings, the quay's boats put out lantern-lit to bless the night-water that feeds the town. The sea keeps no lamps of its own — so once a season, the quay lends it theirs.",
    unlock_flag: 'gleam:tide',
  },
  {
    id: 'lanternway',
    term: 'the Lanternway',
    desc: 'The lit road that rings Vesperholm, spoke to far-off spoke, meeting at the Vesper Crossroads. Its lamps wake region by region as the Gleams return.',
    unlock_flag: 'flag:fenn_errand',
  },
  {
    id: 'skyweave_crown',
    term: 'the Skyweave Crown',
    desc: 'The ring the eight constellations make when all stand lit — closed one quadrant at a time, two Gleams to a quarter. A whole Crown, the old charts say, can part the Penumbra itself.',
    unlock_flag: 'flag:crown_south',
  },
  {
    id: 'glowmoss_bloom',
    term: 'the Glowmoss Bloom',
    desc: "Lowleaf's festival, when the hollow's glowmoss flowers all at once: lantern-strings in the trunks, the wood outshining them. The shy folk let the moss do their speaking — once a year, it has plenty to say.",
    unlock_flag: 'gleam:verdant',
  },
  {
    id: 'lampdown_vigil',
    term: 'the Lamp-down Vigil',
    desc: "Cinderhead's solemn festival: the miners dim their lamps together, honouring the dark they work in. It is not surrender — every lamp is relit before the vigil ends. The town keeps the dark, and keeps its light.",
    unlock_flag: 'gleam:stone',
  },
  {
    id: 'kite_rising',
    term: 'the Kite-rising',
    desc: 'Galehigh\'s festival: on the windiest dusk of the year the whole town flies lit kites, "so the relit constellations have something to answer." Warm, communal, a little daft — and no one is allowed to merely watch.',
    unlock_flag: 'gleam:storm',
  },
  {
    id: 'aurora_watch',
    term: 'the Aurora-watch',
    desc: "Pale Vault's festival, kept in silence: the town gathers on the open ice, each with one lit lamp, watching the aurora till it fades. Calm as any quieted valley — except every flame is lit, and someone chose to hold it.",
    unlock_flag: 'gleam:frost',
  },
  {
    id: 'warden_cor',
    term: 'Warden Còr',
    desc: 'The Hollowing\'s keeper: a star-tender once, courteous and sad, who lost something to the turning of the cycles and decided no one should have to again. He does not fight. He asks — and that is the danger of him.',
    unlock_flag: 'flag:met_cor',
  },
  {
    id: 'coldfog',
    term: 'Coldfog',
    desc: 'The Hollowing\'s creeping mist — a damp dark that snuffs ordinary flame and closes whole passes. Only an Emberward\'s tended ember pushes through it.',
    unlock_flag: 'gleam:frost',
  },
  {
    id: 'last_warm_day',
    term: 'the Last-Warm-Day',
    desc: "The Sunken Solarium's festival: once a year the town gathers in the drowned sun-garden to spend the last warm day before the dark — stored-daylight lanterns, warm bread shared freely, a troupe on the old stage. Warmth, spent on purpose, knowing it fades. That is the point.",
    unlock_flag: 'gleam:solar',
  },
  {
    id: 'sunsketch',
    term: 'Sunsketch',
    desc: 'The Solar Lantern Gift: a pocket of stored daylight, released from the lamp. Shut night-flowers bloom into living bridges at its touch — the drowned garden\'s roads, reopened one bloom at a time.',
    unlock_flag: 'gleam:solar',
  },
  {
    id: 'star_vigil',
    term: 'the Star-vigil',
    desc: "Nightreach's festival, the grandest and most silent: the town keeps a night-long watch at the telescopes as the Crown nears its closing, each watcher lighting one lamp when their star comes home. Belonging as witness — somebody watching when the sky remembers.",
    unlock_flag: 'gleam:lunar',
  },
  {
    id: 'starreach',
    term: 'Starreach',
    desc: 'The Lunar Lantern Gift, last of the six: starlight drawn down to stand on, a stride across short voids of pure dark. The Penumbra\'s final crossings hold under it — the road to the Spire itself.',
    unlock_flag: 'gleam:lunar',
  },
  {
    id: 'great_null',
    term: 'the Great Null',
    desc: 'A lantern built to hold no light, raised on the Umbral Spire and aimed at the Keystar — the one star the whole sky rekindles from. Còr means it kindly. That is the most frightening thing about it.',
    unlock_flag: 'flag:great_null_known',
  },
];

/** Lookup by id (for cutscenes that might surface a single definition later). */
export function getGlossaryEntry(id: string): GlossaryEntry | undefined {
  return GLOSSARY.find((e) => e.id === id);
}
