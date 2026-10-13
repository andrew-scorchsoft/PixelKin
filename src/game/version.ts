/**
 * Single source of truth for the game's displayed version.
 *
 * ▶ To change the version, edit GAME_VERSION below — that's the only line you
 *   need to touch. It surfaces in two places automatically:
 *     • the title screen, bottom-right corner (at-a-glance, in-game)
 *     • the browser tab title, e.g. "PixelKin v1.1" (set in main.ts)
 *
 * Keep package.json's "version" in step if you want them to match, but THIS
 * constant is what the game itself shows the player.
 */
export const GAME_VERSION = '1.24';

/** Pre-formatted label for display, e.g. "v1.1". */
export const GAME_VERSION_LABEL = `v${GAME_VERSION}`;

/**
 * Compare two "major.minor[.patch]" strings numerically: <0 if a is older than b,
 * 0 if equal, >0 if newer. A missing/empty/garbled version counts as the oldest
 * (a save from before version tracking).
 */
export function compareVersions(a: string | undefined | null, b: string | undefined | null): number {
  const parse = (v: string | undefined | null): number[] =>
    (v ?? '').split('.').map((n) => Number.parseInt(n, 10)).map((n) => (Number.isFinite(n) ? n : -1));
  const pa = a ? parse(a) : [-1];
  const pb = b ? parse(b) : [-1];
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const d = (pa[i] ?? 0) - (pb[i] ?? 0);
    if (d !== 0) return d;
  }
  return 0;
}
