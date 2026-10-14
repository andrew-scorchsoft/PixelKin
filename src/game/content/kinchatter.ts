/**
 * Kin chatter — what a grazing AMBIENT kin "says" when you greet it.
 *
 * Face an ambient kin (`NpcPlacement.ambient`, systems/world/Ambience.ts) from the
 * next tile and press Confirm: it stops, turns to you, plays its CRY
 * (systems/audio/cries.ts) and a box shows `<NAME>: <line>`. Kin don't speak
 * human language, so a line is onomatopoeia + a narrated action/observation —
 * never words in its mouth.
 *
 * Lookup (WorldScene.greetAmbientKin → `pickKinChatter`):
 *   1. the species' bespoke entry in KIN_CHATTER (every kin placed as ambient on a
 *      map has one), else
 *   2. TYPE_CHATTER for its primary type (3–5 lines each, so repeats vary).
 * After `flag:dawn` an entry's `dawn` lines (the woken sky) are preferred.
 *
 * A line may carry a `react` — the little body-language beat the kin does while
 * its cry plays (hop / shake / twirl; default: just turn to you). An entry may
 * carry ONE `event`, which fires the first time you greet that species on this
 * save (once-flag `flag:kinchat_<slug>`): a short script (`script.kinchat_*`,
 * ordinary cutscene ops — lore, a tiny find, a starfall), and/or `follow_ms`
 * (it tags along behind you for a few steps, then wanders home). The script
 * runs AFTER the line, and the engine banks the once-flag — scripts never
 * `setFlag` it themselves. Greeting a kin you've never met also notes it as SEEN
 * in the REGISTER (engine side, every kin).
 *
 * Mix (bespoke entries): ~half plain lines, ~a third line + reaction, ~a fifth
 * events. Gifts are deliberately tiny and few (one Tallow Balm in the whole
 * game) — never wicks, never a Lumen Drop, nothing the economy model prices.
 */
import type { KinType } from '@game/data/dex';
import type { ScriptRegistry } from './types';

export type KinReaction = 'turn' | 'hop' | 'shake' | 'twirl';

export interface KinChatterLine {
  text: string;
  react?: KinReaction;
}

export interface KinChatterEvent {
  /** The once-per-save flag (the engine sets it after the event plays). */
  flag: string;
  /** A `script.kinchat_*` ref in KINCHAT_SCRIPTS, run after the line. */
  script?: string;
  /** Tag along behind the player for this long, then wander home. */
  follow_ms?: number;
}

export interface KinChatterEntry {
  lines: KinChatterLine[];
  /** Preferred once `flag:dawn` is held — the woken sky. */
  dawn?: KinChatterLine[];
  event?: KinChatterEvent;
}

/** Fallback lines by PRIMARY type, for any kin without a bespoke entry. */
export const TYPE_CHATTER: Record<KinType, KinChatterLine[]> = {
  Ember: [
    { text: '"Fff-tchk!" A puff of sparks, and it looks very pleased with itself.' },
    { text: '"Hrrff." It leans toward your lamp, as if to compare flames.', react: 'hop' },
    { text: '"Tik-tik-tik." The air around it smells of warm wax and woodsmoke.' },
    { text: '"Fwah!" It sneezes a little ember and pretends that was on purpose.', react: 'shake' },
  ],
  Tide: [
    { text: '"Blrrp!" It blows a bubble at your lamp and watches it drift.' },
    { text: '"Plish." A drip runs off it and it shakes the rest at your boots.', react: 'shake' },
    { text: '"Wooo-oop." The sound rolls out slow, like a wave thinking it over.' },
    { text: '"Plip-plip!" It splashes in place, delighted with nothing at all.', react: 'hop' },
  ],
  Verdant: [
    { text: '"Rrsh-rrsh." It rustles, and a leaf settles on your sleeve.' },
    { text: '"Pff!" A tiny cloud of pollen. It looks sorry. It is not sorry.', react: 'shake' },
    { text: '"Mm-mmm." It hums low, the way grass sounds before rain.' },
    { text: '"Tsip!" It turns its face to your lamp like a sprout to the sun.', react: 'twirl' },
  ],
  Stone: [
    { text: '"Grrnk." It settles heavier, as if you might try to move it.' },
    { text: '"Tok. Tok." It knocks its head on the ground. A greeting, probably.', react: 'hop' },
    { text: '"Hrrmm." A long, gravelly hum you feel more than hear.' },
  ],
  Storm: [
    { text: '"Kzzt!" Your hair lifts for a moment, then settles.', react: 'shake' },
    { text: '"Krrk-krrk!" It fluffs up, crackling, and looks very important.' },
    { text: '"Zip-zip!" It darts a little circle and lands right where it began.', react: 'twirl' },
  ],
  Frost: [
    { text: '"Tsing!" A thin bright note, and a scatter of frost on the ground.' },
    { text: '"Hff." Its breath hangs in the air like a tiny cloud. It watches it go.' },
    { text: '"Krr-sha!" It skids, stops, and acts as though that was the plan.', react: 'hop' },
  ],
  Solar: [
    { text: '"Wa-haa!" It glows a shade warmer, the way a hearth does when you sit by it.', react: 'hop' },
    { text: '"Mrrah." It turns to your lamp the way a flower turns to morning.' },
    { text: '"Paa-aa!" A bright little bray. It wants the whole valley to hear.' },
  ],
  Lunar: [
    { text: '"Mmmoo-oo." A soft, sleepy sound. It blinks very slowly at you.' },
    { text: '"Hnn." It watches the sky over your shoulder, as if expecting someone.' },
    { text: '"Wuuu." It sways gently, half in a dream, and you nearly yawn.', react: 'twirl' },
  ],
  Light: [
    { text: '"Ting-a-ling!" It blinks in time with your lamp. Blink. Blink.', react: 'hop' },
    { text: '"Pii-ii." Its glow brightens to match yours, then shyly dims.' },
    { text: '"Ting." One clear note, like a lantern-chime in a still night.' },
  ],
  Dark: [
    { text: '"Hssh." It keeps to the edge of your light and watches from there.' },
    { text: '"Grrrm." Not a growl. More of a question.', react: 'shake' },
    { text: '"...hff." It edges a half-step closer to your lamp, then thinks better of it.' },
  ],
};

/** Bespoke chatter for every kin placed as ambient on a map (+ room for more). */
export const KIN_CHATTER: Record<number, KinChatterEntry> = {
  // --- South ---------------------------------------------------------------
  8: { // Glimflit — the blinking courier (Duskapple Orchard)
    lines: [
      { text: '"Pip! Pip-pip!" Its tail-lantern blinks a rhythm at you. Blink, blink... blink.', react: 'hop' },
      { text: '"Pip?" It blinks twice and waits, as if you were meant to blink back.' },
    ],
    dawn: [{ text: '"Pip-pip-pip!" It blinks at the morning sky, and for once the sky blinks back.', react: 'twirl' }],
    event: { flag: 'flag:kinchat_glimflit', script: 'script.kinchat_glimflit' },
  },
  10: { // Tallowpup — the candle-tailed pup (Tinderwick, the Lanternway, the orchard)
    lines: [
      { text: '"Yip! Yip-yip!" Its candle-tail wags so hard the flame leans sideways.', react: 'hop' },
      { text: '"Arf." It sniffs your lamp, decides it is a friend, and sits.' },
      { text: '"Hrrm-yip." It curls its tail around its paws to keep the flame out of the wind.' },
    ],
    dawn: [{ text: '"Yip!" Its candle-tail looks pale in the daylight. It does not seem to mind.' }],
    event: { flag: 'flag:kinchat_tallowpup', script: 'script.kinchat_tallowpup' },
  },
  16: { // Wickmoth — follows warm light (Tinderwick, the Lanternway)
    lines: [
      { text: '"Fwip-fwip." It circles your lamp once, twice, and bumps it. Ow.', react: 'twirl' },
      { text: '"Fwip." It lands on the lamp\'s rim to warm its wings, then thinks better of it.' },
    ],
    event: { flag: 'flag:kinchat_wickmoth', follow_ms: 6000 },
  },
  26: { // Brinelet — the trinket-collector (Dimglass Coast, Pearlmoor Quay)
    lines: [
      { text: '"Brrlp!" It blows a bubble at your lamp and watches it drift.', react: 'hop' },
      { text: '"Brr-brr." It rolls over to show you its belly-dip: a pebble, a shell, a button.' },
      { text: '"Blup?" It peers up at you, one eye then the other.' },
    ],
    dawn: [{ text: '"Brrlp!" The tide comes in gold this morning. It rolls about in it, beside itself.' }],
    event: { flag: 'flag:kinchat_brinelet', script: 'script.kinchat_brinelet' },
  },
  27: { // Brineroll — the grown-up roller (Dimglass II, the fen)
    lines: [
      { text: '"Brrrrolll!" It spins in place, very fast, so you can see how fast it is.', react: 'twirl' },
      { text: '"Brr-ump." It tucks into its ridged shell and rocks, waiting to be admired.' },
    ],
  },
  29: { // Glostern — the harbour jelly-lantern (Gullcry Rock)
    lines: [
      { text: '"Wooo-mm." Its bell pulses slowly, soft as moonlight under water.' },
      { text: '"Mmm-ooo." It dims when your lamp comes near, then brightens to match.' },
    ],
  },
  31: { // Lumpin — the lighthouse-limpet (Wrackline, Pearlmoor, the fen)
    lines: [
      { text: '"Pomp. Pomp." Its shell pulses a slow beacon, the way the old lights did.' },
      { text: '"Mmp!" It clamps to its rock, then relaxes when it sees your lamp.', react: 'shake' },
    ],
  },
  // The Wild Ways — the Mirelights' own (the Glassmere)
  22: { // Tidwraith — the will-light wraith (the Glassmere)
    lines: [
      { text: '"Hoooo." It drifts a little way off, then waits, as if you were meant to follow.' },
      { text: '"Hh-oo?" Its glow flickers toward the water. You stay on the boards.', react: 'twirl' },
    ],
  },
  32: { // Lumplass — the grown lighthouse-limpet (the Glassmere, the chapel)
    lines: [
      { text: '"Pomm. Pomm." Its beacon pulses steady and slow, like a lamp left in a window.' },
      { text: '"Mm!" It shines a little brighter at your lamp, then settles, satisfied.', react: 'hop' },
    ],
  },
  47: { // Pebbit — the bouncing pebble (Dimglass II)
    lines: [
      { text: '"Tok!" It bounces once, twice, and lands exactly where it started.', react: 'hop' },
      { text: '"Tik-tok." It rolls behind a stone. You can still see it.' },
    ],
  },
  53: { // Oreling — the ore-grub (Sounding Cave, the Lanternfall road)
    lines: [
      { text: '"Bonk." It headbutts the nearest rock, chews the flake, and looks at you. Bonk.', react: 'shake' },
      { text: '"Grumm." It is heavier than it was this morning. It is very proud.' },
    ],
  },
  56: { // Sporeling — the mushroom sprite (the Wanderwood, Glowmoss Deep)
    lines: [
      { text: '"Pff-pff!" Its cap pulses brighter. A puff of sleepy spores drifts your way.', react: 'shake' },
      { text: '"Pomf." It sits down very suddenly, as mushrooms do.' },
    ],
  },
  105: { // Snoozlet — the moon-sheep (the far Wanderwood)
    lines: [
      { text: '"Baaa-aa... zzz." It falls asleep halfway through saying hello.' },
      { text: '"Mmmbaa." A dream-mote drifts off its wool and pops against your lamp.' },
    ],
    dawn: [{ text: '"Mbaa?" It squints at the bright sky and burrows into its own wool.' }],
    event: { flag: 'flag:kinchat_snoozlet', script: 'script.kinchat_snoozlet' },
  },

  // --- East ----------------------------------------------------------------
  59: { // Dewling — the dewdrop seedling (Saltreach Fen)
    lines: [
      { text: '"Plink." The seed inside it glows, and a ring spreads across the pool.' },
      { text: '"Plink-plink!" It wobbles like a raindrop deciding where to fall.', react: 'hop' },
    ],
  },
  60: { // Poolfrond — the lily-pad glider (Saltreach Fen)
    lines: [
      { text: '"Shhhwoo." It glides a slow circle, fronds trailing, very serene, slightly absurd.', react: 'twirl' },
      { text: '"Shoo-shoo." Its fronds stir. Something in the water told it you were coming.' },
    ],
  },
  65: { // Glowsip — the liquid-light larva (Lowleaf Hollow, Spore Grotto)
    lines: [
      { text: '"Slrrp." It sips a glowmoss drop. Its belly brightens like a filled lamp.' },
      { text: '"Sip-sip." Its antennae drip cyan light onto the moss, where it lingers.', react: 'shake' },
    ],
  },
  67: { // Fennlight — the fern-serpent (Lowleaf Hollow, Glowmoss Deep)
    lines: [
      { text: '"Ssss-ting." It traces a fern\'s outline in light, then darts behind the real one.' },
      { text: '"Tsss." It pulses cyan, three quick and one slow, and is gone into the fronds.', react: 'twirl' },
    ],
  },

  // --- North ---------------------------------------------------------------
  71: { // Iceling — very sophisticated ice (Pale Vault glacier)
    lines: [
      { text: '"Tink!" It bounces off the ice. The philosophers say it is ice. It says "tink."', react: 'hop' },
      { text: '"Tsing." It is colder up close than it looks. It seems sorry about that.' },
    ],
  },
  74: { // Geolace — the geode crab (Windward Stair II)
    lines: [
      { text: '"Click-click." It opens its shell a crack. Inside, the frost-crystals catch your lamp.' },
      { text: '"Clk." It scuttles sideways, stops, and scuttles back. Undecided.', react: 'shake' },
    ],
  },
  77: { // Chillpip — the snow-chick (Windward Stair I)
    lines: [
      { text: '"Cheep-cheep-cheep!" It tumbles over its own feet and chirps anyway.', react: 'hop' },
      { text: '"Peep!" Its down throws a tiny rainbow from your lamp onto the snow.' },
    ],
  },
  80: { // Snowcune — the snow-hare (Pale Vault glacier)
    lines: [
      { text: '"Hff-hff." It thumps a big foot. The snow barely notices.', react: 'hop' },
      { text: '"Mff." It sits up tall, ears turning, and leaves almost no footprint at all.' },
    ],
  },
  81: { // Blizzrhare — the hare-ghost (Hushfrost Pass)
    lines: [
      { text: '"Hwhooo!" A little snow-devil spins up around it, and then it is somewhere else.', react: 'twirl' },
      { text: '"Hrff." It holds very still. For a hare-ghost, that is a great compliment.' },
    ],
  },
  84: { // Hushbore — the silent burrower (Hushfrost Pass)
    lines: [
      { text: '"...!" It opens its mouth wide. The cry comes out muffled, as if through a door.' },
      { text: '"..." It taps its ice-plated shoulder against yours. The quiet feels like company.', react: 'shake' },
    ],
  },
  88: { // Sparrowcaw — the flint sparrow (Galehigh terraces)
    lines: [
      { text: '"Chk-chk!" It shows you a flint-chip from under its wing, then hides it again.', react: 'hop' },
      { text: '"Tchirr!" It pecks the cliff. A spark. It looks at you: did you see that?' },
    ],
    event: { flag: 'flag:kinchat_sparrowcaw', script: 'script.kinchat_sparrowcaw' },
  },
  89: { // Flintbeak — the spark-chisel (Windward Stair I)
    lines: [
      { text: '"Tak-tak-KRAK!" Three pecks at the rock, and the third one sparks.', react: 'shake' },
      { text: '"Krrk." It cleans its beak on the stone with great care.' },
    ],
  },
  90: { // Strikeaven — the apex flint-raven (Thunderroost)
    lines: [
      { text: '"KRAAAWK!" Static runs down its beak and crackles off into the wind.' },
      { text: '"Krawk." It looks down at you from its perch. It does not look down on you.' },
    ],
    dawn: [{ text: '"Krraawk." It spreads its wings in the first warm wind of the morning.' }],
  },
  91: { // Cirruff — the cloud-fluff pup (Galehigh terraces)
    lines: [
      { text: '"Arf-zzt!" You reach to pat it. It shocks you. It wags anyway.', react: 'shake' },
      { text: '"Rrff." Its fur glows gold at the edges. That means it is happy.', react: 'hop' },
    ],
  },

  // --- The Farlamp Isles (post-game; Lane B) ---------------------------------
  // No `dawn` pools on purpose: the isles keep their own dusk after the mainland
  // morning (10-the-farlamp-isles.md §1), so the plain lines are the ones heard.
  172: { // Fathomote — the lantern-fish fry (the deep, the isles' shallows)
    lines: [
      { text: '"Blip!" Its lure flicks on, off, on. It is very proud of that.', react: 'hop' },
      { text: '"Bloop." It swims a circle round your lamp, as if checking whose light is bigger.', react: 'twirl' },
      { text: '"Blip-blip." It noses your boot, then darts back to show its little light to the others.' },
    ],
    event: { flag: 'flag:kinchat_fathomote', script: 'script.kinchat_fathomote' },
  },
  173: { // Fathomere — the grown lantern-fish
    lines: [
      { text: '"Mmmmohh." A slow, deep hum. Its lure dims, then brightens, like a lamp being trimmed.' },
      { text: '"Ohhmm." It turns its light toward the open sea and holds it there, steady, the way a keeper would.', react: 'turn' },
    ],
  },
  174: { // Hermiwick — the hermit crab in a broken lamp-glass
    lines: [
      { text: '"Clik-clik." It backs into its cracked glass until only its eyes show. Then, slowly, the claws.', react: 'shake' },
      { text: '"Tik." It polishes one chipped pane with its small claw, very carefully, and waits for you to notice.' },
      { text: '"Clk-clk!" It peers into your vesperlamp a long time. Looking for the lamp its glass came from.', react: 'hop' },
    ],
  },
  175: { // Beaconclaw — the crab-lighthouse
    lines: [
      { text: '"KLAK." It raises its great claw like a shield, then lowers it. You passed.', react: 'shake' },
      { text: '"Hmmm-klak." The lamp on its back turns once, slow, and sweeps its beam right across you.', react: 'twirl' },
    ],
  },
  176: { // Fogwisp — the sea-fog moth (the Fogwall, the Undertide)
    lines: [
      { text: '"...fffh." It drifts to your lamp and settles on the glass. The glass goes cold and grey.' },
      { text: '"Hhhh." It flutters a slow circle. When it is gone the air still smells of the sea.', react: 'twirl' },
      { text: '"...ff." It tries to land on your lamp-flame, thinks better of it, and sits on your hat instead.', react: 'hop' },
    ],
  },
  // ---- Lane A — the Ashfall Shelf (walkthrough/10 Part II) ----
  49: { // Gravelo — the slag-heap boulder (the Ashfall Shelf)
    lines: [
      { text: '"Grrmmm." It settles deeper into the slag with a sound like a cart tipping.', react: 'shake' },
      { text: '"Hrmp." A little avalanche of cinders runs off its back. It looks pleased.' },
    ],
  },
  63: { // Stonebark — the ash-grass stump (the Ashfall Shelf, rare)
    lines: [
      { text: '"...rrrk." Grey grass rustles on its shoulders. It turns, very slowly, to face the wind.', react: 'hop' },
      { text: '"Hhhm." It roots its toes in the ash. Something green pokes up beside them.' },
    ],
    dawn: [{ text: '"Hhhmm!" The ash-grass on its back has gone a little green at the tips.' }],
  },
  // --- Lane E (10 Part III): Lowtinder, the town under the bay ----------------
  11: { // Tallowcrest — warms itself in the drowned hearths (Lowtinder)
    lines: [
      { text: '"Fff." It sits in an old fireplace that has not had a fire in forty years, and glows, so now it has one.', react: 'hop' },
      { text: '"Tsss." A drop of sea lands on its back and steams. It looks offended at the whole ocean.' },
    ],
    dawn: [{ text: '"Fff-fff!" It basks in a square of real sunlight on the old cobbles, belly-up.' }],
  },
  21: { // Tidmaren — the tide-pool glimmer (Lowtinder, the bay)
    lines: [
      { text: '"Plip." It bobs in a puddle that used to be somebody\'s kitchen, and blinks a little light at you.', react: 'hop' },
      { text: '"Plip-plip." It drifts round your boots like you are a rock worth circling.' },
    ],
  },
  39: { // Mossmantle — the moss that kept the lamp-school's lesson (the moss-garden)
    lines: [
      { text: '"Mmmm." Its mossy cloak glows a little brighter as your lamp comes near, like a pupil answering a question.', react: 'twirl' },
      { text: '"Mm." It shuffles over and settles by your feet, warm and damp and quite pleased with itself.' },
    ],
    dawn: [{ text: '"Mmmm!" A thread of daylight finds the garden through the fallen roof. It leans toward it, every frond at once.' }],
  },
};

/** The event scripts (spread into content/scripts.ts SCRIPTS). Lore, finds and
 *  small moments — never progression, never wicks; the engine banks each once-flag. */
export const KINCHAT_SCRIPTS: ScriptRegistry = {
  // Glimflit: the blink-code, and the Skyweave (story-bible §2/§11 rule 1).
  'script.kinchat_glimflit': [
    { op: 'emote', actor: 'player', emote: 'question', holdMs: 700 },
    { op: 'narrate', text: 'Blink. Blink... blink. The pattern repeats. Then, far above, one dim star seems to blink the same way.' },
    { op: 'narrate', text: 'Old lamp-tenders say every star has a kin on the ground that carries its spark. Maybe this one is just saying hello to a cousin.' },
  ],
  // Tallowpup: a tiny find (the game's one kinchatter gift).
  'script.kinchat_tallowpup': [
    { op: 'narrate', text: 'It trots off, digs at the roots, and trots back with something in its mouth. It drops it at your feet, tail-flame wagging.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 1 },
    { op: 'say', text: 'Found a TALLOW BALM, a little chewed.' },
  ],
  // Brinelet: what the tide brings — the falling cinders (story-bible §11).
  'script.kinchat_brinelet': [
    { op: 'narrate', text: 'It rolls over and shows you its treasures. Among the shells is a chip of something dark and cold, with a blue-grey glow in its cracks.' },
    { op: 'narrate', text: 'It will not give that one up. It rolls it back into its belly-dip, carefully, the way you would keep something that was not quite asleep.' },
  ],
  // Snoozlet: a dream-mote, and the Long Dusk's eleven winters (story-bible §12).
  'script.kinchat_snoozlet': [
    { op: 'emote', actor: 'player', emote: 'sleep', holdMs: 900 },
    { op: 'narrate', text: 'A dream-mote drifts off its wool and opens like a soap-bubble. Inside, for a heartbeat: a meadow, in sunlight.' },
    { op: 'narrate', text: 'It has never seen a morning. Nothing its age has. Eleven winters of dusk, and still it dreams of one.' },
  ],
  // Sparrowcaw: the falls over the high terraces (peril thread — told, not shown).
  'script.kinchat_sparrowcaw': [
    { op: 'emote', actor: 'player', emote: 'alert', holdMs: 600 },
    { op: 'narrate', text: 'It stops pecking and stares straight up, every feather flat. You look too. Nothing, only the dark.' },
    { op: 'narrate', text: 'Up here they say the birds see the falling stars before anyone does. It watches for a long while before it goes back to its flint.' },
  ],
  // Fathomote: the shoal answers your lamp (the Farlamp Isles' lore, §1).
  'script.kinchat_fathomote': [
    { op: 'emote', actor: 'player', emote: 'alert', holdMs: 700 },
    { op: 'narrate', text: 'It dives. A moment later the dark water lights up, one small lure after another, until a whole shoal is blinking back at your lamp.' },
    { op: 'narrate', text: 'Driftholm folk used to set lamps by the water for the fry. Eleven winters, and the fry still come to any light that waits for them.' },
  ],
};

/** A seeded-enough pick: plain Math.random, kept here so callers stay one line. */
function pick<T>(xs: readonly T[]): T {
  return xs[Math.floor(Math.random() * xs.length)];
}

/**
 * What a greeted kin does and says: the entry (bespoke, else its primary type's
 * pool), a line (the dawn pool once the sky has woken), and the event when its
 * once-flag isn't held yet.
 */
export function pickKinChatter(
  speciesId: number,
  primaryType: KinType,
  hasFlag: (flag: string) => boolean,
): { line: KinChatterLine; event?: KinChatterEvent } {
  const entry = KIN_CHATTER[speciesId];
  const pool = entry?.dawn && hasFlag('flag:dawn') ? entry.dawn : entry?.lines ?? TYPE_CHATTER[primaryType];
  const line = pick(pool.length > 0 ? pool : TYPE_CHATTER[primaryType]);
  const event = entry?.event && !hasFlag(entry.event.flag) ? entry.event : undefined;
  return { line, event };
}
