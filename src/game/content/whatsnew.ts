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
    'Your vesperlamp now remembers every hearth you have rested by. SETTINGS - "Return to rest point" carries you back to any of them.',
    'Some roads have been re-laid and a few new faces have settled in. Places you know may hold something new.',
  ],
};

/** The lines for a given version (empty when there's nothing to tell). */
export function whatsNewFor(version: string): string[] {
  return WHATS_NEW[version] ?? [];
}
