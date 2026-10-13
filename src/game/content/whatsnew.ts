/**
 * What's new — a tiny, optional changelog the "world has changed" notice reads.
 *
 * When a save from an older build is loaded (WorldScene.showVersionNotice), the
 * lines keyed by the CURRENT GAME_VERSION (version.ts, "major.minor") are shown
 * after the opening line, one short page each. No entry for this version = the
 * notice simply skips them. Keep each line short, warm and in-canon (kin,
 * Gleams, the Wayfaring, the vesperlamp) — it's read by the fire, not a patch log.
 *
 * NO SPOILERS for the hidden, real-people content (owner's rule, 2026-10): this
 * notice is read by the very people those places were built for. Never mention
 * Paul or anything of his — the Booji-Wooji Man / S4–S5 line, the Chickenpig,
 * the Lifting House (it's Paul's gym), Paul's house on Wayward Rise, the Wayward
 * Arms hotel, the Reckoning Works' walking-man story — nor the beacon-road man
 * with the case. Changes there ship SILENTLY; announce only general things.
 */
export const WHATS_NEW: Record<string, string[]> = {
  '1.26': [
    'Swapping kin mid-battle is a proper changeover now: you call your kin back into the lamp, and the next one blooms out of its light.',
    'The Backwards Inn\'s funhouse mirrors have opinions. Go and look in each one, and slip behind them while you\'re at it.',
  ],
  '1.25': [
    'Things you face and press A on now answer you properly: a few signs and curiosities (several in the Old Light) used to keep quiet unless you stood just so.',
    'A trainer\'s greeting in battle now waits for you to press A. Prefer it brisk? SETTINGS > Trainer talk: Auto.',
    'The Old Light\'s regulars have found some new material. Mind the bunting.',
  ],
  '1.24': [
    'Kindling is a proper ceremony now: your kin glows and flickers between its old shape and its new one, to a tune of its own. Press B before the light blooms if you would rather it waited.',
  ],
  '1.23': [
    'Trainer battles now open the old way: your opponent steps out to face you, says their piece, and sends out their kin. Win, and they come back for a few closing words.',
    'If you finished parts of the Wayfaring on an older build, places that later updates hung on quest steps you had already passed are now open to you.',
  ],
  '1.22': [
    'At the top of the Old Light, someone very protective of the last joke has hired an act to keep you away from it. There is a comfy chair by the stairs to rest in first.',
  ],
  '1.21': [
    'Fights inside the Old Light have a battle tune of their own now. It does not take itself seriously.',
  ],
  '1.20': [
    'The Old Light has its remastered score: one cheeky march that follows you up all seven floors, getting a little madder with every flight.',
  ],
  '1.19': [
    'Five new kin have moved into the Old Light, and they are clowns: JesterHalf, The Smiler and McClownface roam its halls, and two of them kindle into something even sillier.',
    'Every floor of the tower now has a look of its own in battle, and a few floors have changed shape. Mind the waxed gallery floor.',
    'An old friend of the house climbs alongside you now, one floor ahead, with a story to tell on the way up.',
  ],
  '1.18': [
    'The Old Light on Lightkeeper\'s Point has opened its doors properly: seven big floors to wander, a house full of regulars with jokes of their own, and a song that gets a little stranger with every flight of stairs.',
    'Wild kin roam the tower\'s halls now, and a few of its regulars fancy a bout. There are tea and a quiet chair on the way up, if you need a rest.',
    'Folk all over Vesperholm give clearer directions now: lost Wayfarers should find the next step easier to spot, and Andrew\'s advice holds true wherever he\'s leaning.',
  ],
  '1.17': [
    'The build number now sits quietly at the bottom of the loading screens, and fullscreen comes back after you keep a copy of your save.',
  ],
  '1.16': [
    'Roofs are friendlier now: you can slip along behind the peak of a house or a hall instead of walking all the way round it.',
  ],
  '1.15': [
    'Someone in Duskapple Orchard is brewing coffee in a little eight-sided pot, and would love to tell you everything about it. And at the foot of Lowleaf Hollow, Marisol is cooking something red.',
    'Andrew has been dressing for the weather, wherever you meet him.',
    'Holes, steps and ladders that lead somewhere now look like it, indoor walls meet their ceilings, and nobody is standing in the sea any more.',
  ],
  '1.14': [
    'Your whole lamp learns now: the kin that wins a fight keeps its full EXP, those who fought beside it take half, and the rest a quarter. (Settings → EXP share, if you prefer the old way.)',
    'The Old Light has a new machine on its tea floor, and its tower stairs now look like stairs.',
  ],
  '1.13': [
    'The Sunvault is a real climb now: ladders up the sandstone, ledges to edge along, and a long way down the other side. At the foot of the climb an old wax road waits — rent a runner and ride it all the way to the sea.',
    'If you have ever wondered about the lift-house by Lightkeeper\'s Point: its car is stuck at the top. Someone up there would have to free the brake.',
    'There are lights on the water east of Saltreach Fen, and a ferryman who will not row toward them. The lens-grinder in Pale Vault might know why.',
    'High above the glacier, an old road climbs into the frost, and in Cinderhead, Otho has a door he has been meaning to show someone.',
  ],
  '1.12': [
    'The roads of Vesperholm have been walked again and set true: leave a place to the north and you arrive somewhere north. The MAP now draws the world exactly as you walk it, and scrolls.',
    'From Pearlmoor, the road home runs round the bay — east into Saltreach Fen, then south down the old drowned road and the Wrackline shore.',
    'Lowleaf, Galehigh and Nightreach sit far up the mountain. The Lantern-car at the Crossroads carries you there once each valley is relit. Two new roads as well: Cinderwind Scarp above the mines, and the Umbral Approach up to the Penumbra.',
    'Past the shallows the open sea runs deep and dark. Tidecall carries you through the shallows, but not out to sea.',
    'If a road you once took has gone, SETTINGS → Return to rest point brings you home from anywhere.',
  ],
  '1.11': [
    'Rest at an inn or your own bed and the night really passes now: the lamps go out, a little lullaby plays, and you wake to the music you left.',
    'Every fight has somewhere to stand, from the Lanternway verge to the high Lumenary halls, and the battles sing their old chip songs again.',
    'Shopkeepers will talk to you across the counter. And on the coast road out of Tinderwick, one of Brisa\'s keepers now waits for those who have not yet lit the Beacon.',
  ],
  '1.9': [
    'Step indoors and the music steps in with you — every inn, shop and hearth has its own tune now, and the Crossroads, the Lanternway and Pearlmoor sing their own songs.',
    'Some places remember what happened there. Walk the old orchard again, and listen.',
    'Turn the whole world up or down with the little slider under the screen, or in Settings. The bleeps and footsteps have been asked to speak a little softer.',
  ],
  '1.8': [
    'Vesperholm has a new voice. Every town, road, cave and battle has been scored afresh around one melody from home — and if you miss the old tunes, Settings → Soundtrack brings them back.',
    'The kin in the grass will talk to you now. Walk up to a wandering one and press A — each has its own cry, and some have more to say than others.',
  ],
  '1.7': [
    'Look away from your own road now and then. Between the chapters of your Wayfaring, someone else is busy in the dark — and he is very tidy about it.',
    'The world can be heard now: surf on the coast, wind on the high stairs, drips in the caves, crickets in the hollows, and your own feet on sand and snow.',
    'The Hushfrost Pass has been carved anew, and the Starfall Vigils at Nightreach will open for anyone who has seen the dawn.',
    'If Georgina is still waiting on her kitten, look again in the darkest corner of the dell.',
  ],
  '1.6': [
    'Look up now and then. The stars are still going out, and some of them are falling. Folk say every fall lands nearer the mountain.',
    'The roads have changed while you rested. Saltreach Fen has its reed-cutters back, the Hushfrost Pass has been carved anew, and the Coldfog stands even quieter than before.',
    'New faces in every valley: miners at Cinderhead, fisherfolk on the Quay, kite-weavers on the Galehigh terraces. Places you know may hold something you missed.',
    'Old friends have more to say, and more to carry. Listen for Fenn, for Wren, and for Warden Còr.',
  ],
};

import { compareVersions } from '@game/version';

/** The lines for a given version (empty when there's nothing to tell). */
export function whatsNewFor(version: string): string[] {
  return WHATS_NEW[version] ?? [];
}

/**
 * Everything a returning player missed: the lines of every version newer than the
 * one their save was last played on, up to `current`, newest first (a 1.5 save
 * loading 1.7 hears 1.7's lines, then 1.6's). Capped so a very old save gets a
 * short, warm notice rather than a patch log.
 */
export function whatsNewSince(from: string, current: string, cap = 6): string[] {
  const versions = Object.keys(WHATS_NEW)
    .filter((v) => compareVersions(v, from) > 0 && compareVersions(v, current) <= 0)
    .sort((a, b) => compareVersions(b, a));
  return versions.flatMap((v) => WHATS_NEW[v]).slice(0, cap);
}
