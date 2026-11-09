/**
 * Key-information marks: `[[like this]]` in any dialogue text flags story-critical
 * information (where to go, who to see, what to bring, a new control). The
 * DialogueBox draws marked runs underlined in lamp-gold so they can't be lost in a
 * stream of colour; everywhere else (battle messages, menus) they're simply stripped.
 *
 * Authoring rules (what to mark, how sparingly) live in docs/world/dialogue-rubric.md §6.
 */

const OPEN = '[[';
const CLOSE = ']]';

/** Remove every mark, leaving the plain text. */
export function stripMarks(text: string): string {
  return text.includes(OPEN) ? text.split(OPEN).join('').split(CLOSE).join('') : text;
}

/**
 * Parse marks out of a line: the plain text, plus one flag per plain character
 * saying whether it was inside `[[...]]`. An unclosed `[[` marks to the end; a stray
 * `]]` is dropped — a typo degrades to a slightly-off underline, never raw brackets.
 */
export function parseMarks(text: string): { plain: string; marked: boolean[] } {
  if (!text.includes(OPEN) && !text.includes(CLOSE)) return { plain: text, marked: new Array(text.length).fill(false) };
  let plain = '';
  const marked: boolean[] = [];
  let inside = false;
  for (let i = 0; i < text.length; i++) {
    if (text.startsWith(OPEN, i)) {
      inside = true;
      i++;
      continue;
    }
    if (text.startsWith(CLOSE, i)) {
      inside = false;
      i++;
      continue;
    }
    plain += text[i];
    marked.push(inside);
  }
  return { plain, marked };
}

/** A marked run on one wrapped row of a page: columns [start, end) and its offset in the page text. */
export interface MarkRun {
  row: number;
  start: number;
  end: number;
  offset: number;
}

/**
 * Map the marks of a plain string onto its word-wrapped rows. Word wrap only removes or
 * swaps whitespace, so walking both in step (skipping whitespace the wrap dropped)
 * lines every wrapped character back up with its source character.
 * Returns the marked runs per row, with each run's character offset into
 * `rows.join('\n')` (the page text the typewriter reveals).
 */
export function runsForRows(plain: string, marked: boolean[], rows: string[], from = 0): { runs: MarkRun[]; next: number } {
  const runs: MarkRun[] = [];
  let p = from;
  let offset = 0;
  rows.forEach((row, r) => {
    let run: MarkRun | undefined;
    for (let c = 0; c < row.length; c++) {
      const ch = row[c];
      while (p < plain.length && plain[p] !== ch && /\s/.test(plain[p])) p++;
      const matched = p < plain.length && plain[p] === ch;
      const isMarked = matched && marked[p];
      if (matched) p++;
      if (isMarked) {
        if (run && run.end === c) run.end = c + 1;
        else {
          run = { row: r, start: c, end: c + 1, offset: offset + c };
          runs.push(run);
        }
      }
    }
    offset += row.length + 1; // + the '\n' joining rows
  });
  // Trim trailing spaces off runs (a mark never underlines into blank space).
  for (const run of runs) {
    const row = rows[run.row];
    while (run.end > run.start && /\s/.test(row[run.end - 1])) run.end--;
  }
  return { runs: runs.filter((r) => r.end > r.start), next: p };
}
