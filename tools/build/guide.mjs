/**
 * The player's walkthrough — docs/guide/*.md compiled into the website (web/).
 *
 * ONE source of truth: the Markdown chapters in docs/guide/ (player-facing, plain
 * words, no flags or file paths). Each starts with a small front-matter block:
 *
 *   ---
 *   title: Chapter 1 — Tinderwick & the Dimglass Coast
 *   section: Walkthrough        (one of GUIDE_SECTIONS below)
 *   order: 10                   (sort within its section)
 *   desc: One sentence for the index card and the meta description.
 *   spoilers: true              (optional: shows the spoiler note)
 *   ---
 *
 * A chapter can embed live game data with the site's blocks — `<!-- block:matchups -->`
 * renders the real type chart — and `{{TOKENS}}` like any page. It compiles to
 * `guide-<slug>.html` (served at /guide-<slug>), plus the `guide` index page.
 *
 * The hidden content made for real people (VISION/CLAUDE.md: the S4–S5 storyline)
 * must never reach the site: FORBIDDEN words fail the build.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { marked } from 'marked';

export const GUIDE_SECTIONS = [
    { id: 'Getting Started', blurb: 'The controls, the basics, and what everything on the screen means.' },
    { id: 'Walkthrough', blurb: 'The main journey, chapter by chapter, from Tinderwick to the dawn.' },
    { id: 'Side Areas & Secrets', blurb: 'Optional places worth the detour — and the reasons to go back.' },
    { id: 'After the Dawn', blurb: 'What opens once the sky is lit again.' },
    { id: 'Reference', blurb: 'Tables to keep beside you: types, Lumenaries, Gifts, wicks.' },
];

/** Never on the public site (owner's rule — the people it was built for read it). */
const FORBIDDEN = [/booji/i, /chicken-?pig/i, /\bpaul\b/i, /lifting house/i, /wayward/i, /lottie/i,
    /omenire/i, /wanderwood/i, /\baldous\b/i, /\bWink's\b/, /tin rower/i, /reckoning works/i];

function frontMatter(src, file) {
    const m = /^---\n([\s\S]*?)\n---\n?/.exec(src);
    if (!m) throw new Error(`guide: ${file} has no front-matter block`);
    const meta = {};
    for (const line of m[1].split('\n')) {
        const kv = /^(\w+):\s*(.*)$/.exec(line.trim());
        if (kv) meta[kv[1]] = kv[2];
    }
    for (const k of ['title', 'section', 'order', 'desc']) if (!meta[k]) throw new Error(`guide: ${file} is missing "${k}"`);
    if (!GUIDE_SECTIONS.some((s) => s.id === meta.section)) throw new Error(`guide: ${file} has unknown section "${meta.section}"`);
    return { meta, body: src.slice(m[0].length) };
}

const slugify = (t) => t.toLowerCase().replace(/<[^>]+>/g, '').replace(/&[a-z]+;/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

/** Load every chapter, sorted by section then order. */
export function loadGuide(root) {
    const dir = join(root, 'docs', 'guide');
    if (!existsSync(dir)) return [];
    const chapters = readdirSync(dir).filter((f) => f.endsWith('.md') && !f.startsWith('_')).map((file) => {
        const src = readFileSync(join(dir, file), 'utf8');
        for (const re of FORBIDDEN) if (re.test(src)) throw new Error(`guide: ${file} mentions hidden content (${re}) — keep it off the site`);
        const { meta, body } = frontMatter(src, file);
        const slug = file.replace(/\.md$/, '').replace(/^\d+[-_]/, '');
        return { file, slug, stem: `guide-${slug}`, title: meta.title, section: meta.section,
            order: Number(meta.order), desc: meta.desc, spoilers: meta.spoilers === 'true', body };
    });
    const secIdx = (c) => GUIDE_SECTIONS.findIndex((s) => s.id === c.section);
    chapters.sort((a, b) => secIdx(a) - secIdx(b) || a.order - b.order || a.slug.localeCompare(b.slug));
    const stems = new Set();
    for (const c of chapters) {
        if (stems.has(c.stem)) throw new Error(`guide: duplicate chapter slug "${c.slug}"`);
        stems.add(c.stem);
    }
    return chapters;
}

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** Markdown -> HTML with anchored h2/h3 and a list of the h2s for the on-page contents. */
function renderMarkdown(md, chapters) {
    const toc = [];
    const used = new Set();
    const renderer = new marked.Renderer();
    renderer.heading = function ({ tokens, depth }) {
        const text = this.parser.parseInline(tokens);
        let id = slugify(text) || 'section';
        while (used.has(id)) id += '-x';
        used.add(id);
        if (depth === 2) toc.push({ id, text });
        return `<h${depth} id="${id}"><a class="anchor" href="#${id}" aria-hidden="true">#</a>${text}</h${depth}>\n`;
    };
    // [[chapter-slug]] or [[chapter-slug|label]] links to another chapter
    const linked = md.replace(/\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]/g, (_, slug, label) => {
        const c = chapters.find((x) => x.slug === slug);
        if (!c) throw new Error(`guide: link to unknown chapter [[${slug}]]`);
        return `[${label ?? c.title}](guide-${slug})`;
    });
    const html = marked.parse(linked, { renderer, gfm: true });
    return { html, toc };
}

function sidebar(chapters, current) {
    return GUIDE_SECTIONS.map((s) => {
        const items = chapters.filter((c) => c.section === s.id);
        if (!items.length) return '';
        return `
            <div class="guide-nav-group">
                <h3>${esc(s.id)}</h3>
                <ul>${items.map((c) => `
                    <li><a href="${esc(c.stem)}"${c.stem === current ? ' class="active" aria-current="page"' : ''}>${esc(c.title)}</a></li>`).join('')}
                </ul>
            </div>`;
    }).join('');
}

/** One chapter page's body (the site wraps it in header/footer). */
export function chapterBody(c, chapters, expand) {
    const { html, toc } = renderMarkdown(c.body, chapters);
    const i = chapters.indexOf(c);
    const prev = chapters[i - 1];
    const next = chapters[i + 1];
    return `<section class="page-hero guide-hero">
    <p class="guide-crumb"><a href="guide">The Wayfarer's Guide</a> · ${esc(c.section)}</p>
    <h1>${esc(c.title)}</h1>
    <p class="page-hero-sub">${esc(c.desc)}</p>
</section>

<section class="guide-layout">
    <nav class="guide-nav" aria-label="Guide chapters">${sidebar(chapters, c.stem)}
    </nav>
    <article class="guide-article">${c.spoilers ? `
        <p class="guide-spoiler">This chapter walks through the story. If you'd rather discover it yourself, play first and come back when you're stuck.</p>` : ''}${toc.length > 2 ? `
        <details class="guide-toc" open><summary>On this page</summary><ol>${toc.map((t) => `<li><a href="#${t.id}">${t.text}</a></li>`).join('')}</ol></details>` : ''}
        ${expand(html)}
        <nav class="guide-pager">${prev ? `
            <a class="guide-prev" href="${esc(prev.stem)}">← ${esc(prev.title)}</a>` : '<span></span>'}${next ? `
            <a class="guide-next" href="${esc(next.stem)}">${esc(next.title)} →</a>` : ''}
        </nav>
    </article>
</section>`;
}

/** The guide's front page: every section and its chapters. */
export function indexBody(chapters) {
    return `<section class="page-hero">
    <h1>The Wayfarer's Guide</h1>
    <p class="page-hero-sub">A walkthrough of Vesperholm in the old style: read it chapter by chapter, or dip in when you're stuck.</p>
</section>
${GUIDE_SECTIONS.map((s) => {
        const items = chapters.filter((c) => c.section === s.id);
        if (!items.length) return '';
        return `
<section class="band guide-section">
    <h2 class="band-title">${esc(s.id)}</h2>
    <p class="guide-section-blurb">${esc(s.blurb)}</p>
    <div class="guide-cards">${items.map((c) => `
        <a class="guide-card" href="${esc(c.stem)}">
            <h3>${esc(c.title)}</h3>
            <p>${esc(c.desc)}</p>
        </a>`).join('')}
    </div>
</section>`;
    }).join('')}`;
}
