/**
 * What's new — a tiny, optional changelog the "world has changed" notice reads.
 *
 * When a save from an older build is loaded (WorldScene.showVersionNotice), the
 * lines keyed by the CURRENT GAME_VERSION (version.ts, "major.minor") are shown
 * after the opening line, one short page each. No entry for this version = the
 * notice simply skips them. Keep each line short, warm and in-canon (kin,
 * Gleams, the Wayfaring, the vesperlamp) — it's read by the fire, not a patch log.
 */
export const WHATS_NEW: Record<string, string[]> = {
  '1.9': [
    'Step indoors and the music steps in with you — every inn, shop and hearth has its own tune now, and the Crossroads, the Lanternway and Pearlmoor sing their own songs.',
    'Some places remember what happened there. Walk the old orchard again, and listen.',
    'Turn the whole world up or down with the little slider under the screen, or in Settings. The bleeps and footsteps have been asked to speak a little softer.',
    'Paul, Andrew and the strongmen of the Lifting House have had their portraits taken again, and stand a little taller for it.',
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
