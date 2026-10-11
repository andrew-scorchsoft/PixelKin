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
  '1.6': [
    'Look up now and then. The stars are still going out, and some of them are falling. Folk say every fall lands nearer the mountain.',
    'The roads have changed while you rested. Saltreach Fen has its reed-cutters back, the Hushfrost Pass has been carved anew, and the Coldfog stands even quieter than before.',
    'New faces in every valley: miners at Cinderhead, fisherfolk on the Quay, kite-weavers on the Galehigh terraces. Places you know may hold something you missed.',
    'Old friends have more to say, and more to carry. Listen for Fenn, for Wren, and for Warden Còr.',
  ],
};

/** The lines for a given version (empty when there's nothing to tell). */
export function whatsNewFor(version: string): string[] {
  return WHATS_NEW[version] ?? [];
}
