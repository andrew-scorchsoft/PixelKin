/**
 * Site-wide configuration, shared data, and the render helpers for the PixelKin
 * marketing site. tools/build/build_site.mjs pulls everything from here and
 * stamps web/pages/<stem>.html bodies into full static pages.
 *
 * No framework, no server: the output is plain HTML so the whole of pixelk.in
 * serves from a Cloudflare Worker's static assets (or any static host). Keep
 * brand facts (vocabulary, the starter trio, the palette) sourced from the game
 * canon so the site never drifts from CLAUDE.md / the design docs.
 *
 * Page bodies use two kinds of placeholder:
 *   {{TOKEN}}            — a value from TOKENS (or {{tint:Type}} for a type colour)
 *   <!-- block:name -->  — a data-driven section rendered by BLOCKS[name]
 */

import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const HERE = fileURLToPath(new URL('.', import.meta.url));

/** Where the playable game lives once a release is assembled
 *  (tools/build/assemble_release.mjs drops dist/ into release/play/). */
export const GAME_URL = '/play/';

/** Site identity. */
export const SITE_NAME = 'PixelKin';
export const SITE_TAGLINE = 'Lanterns in the dark.';
export const SITE_DESC = 'A retro, handheld-era creature-collecting adventure. Relight the sky one constellation at a time across the valleys of Vesperholm — collect over 150 original kin in your browser.';

/** Studio behind the game. */
export const STUDIO_NAME = 'Scorchsoft';
export const STUDIO_URL = 'https://www.scorchsoft.com/';
export const STUDIO_CONTACT = 'https://www.scorchsoft.com/contact-scorchsoft/';

/** Public source repository. */
export const GITHUB_URL = 'https://github.com/andrew-scorchsoft/PixelKin';

/**
 * Every page. stem = web/pages/<stem>.html → served at /<stem> (index → /).
 * title feeds <title>/og:title; desc the meta/og description.
 */
export const PAGES = [
    { stem: 'index', title: 'Home', desc: 'PixelKin is a retro, handheld-era creature-collecting adventure, free to play in your browser. Relight the constellations of Vesperholm, collect over 150 original kin, and wander fourteen lamplit valleys.' },
    { stem: 'about', title: 'About', desc: 'Why we made PixelKin: a love letter to handheld-era creature-collecting. The feeling we\'re selling — nostalgia, collecting, exploration, delight — and why every kin, sprite, and note is original.' },
    { stem: 'story', title: 'The World', desc: 'The story of PixelKin: night fell over Vesperholm and won\'t lift. Play a lamp-tender\'s apprentice relighting the sky, befriend the kin, and meet the Hollowing — a cult that would let the dark stay.' },
    { stem: 'creatures', title: 'Kin', desc: 'Meet the kin of PixelKin — over 150 original creatures across ten elements, from the ember-fox Vulpyre to the tide-hum Brinix and the lucky Cloverkit. An empirically balanced roster, a copy of nothing.' },
    { stem: 'faq', title: 'FAQ', desc: 'Answers to common questions about playing PixelKin — how to start, the controls, saving your progress, catching and raising kin, and what makes this original creature-collecting adventure tick.' },
    { stem: 'license', title: 'Licensing', desc: 'Interested in licensing PixelKin, its world, characters, music or artwork? PixelKin is created and owned by Scorchsoft — get in touch through the Scorchsoft contact form to discuss licensing and partnerships.' },
    { stem: 'privacy', title: 'Privacy Policy', updated: 'June 2026', desc: 'How PixelKin and Scorchsoft handle your data. The PixelKin website is informational and the game stores your progress locally in your own browser — we do not collect personal information through it.' },
    { stem: 'terms', title: 'Terms of Use', updated: 'June 2026', desc: 'The terms for using PixelKin. The game and website are provided free, "as is", with no warranties. Scorchsoft owns all rights and may change, suspend or withdraw the game at any time.' },
    { stem: '404', title: 'Lost in the Dusk', noindex: true, desc: 'This road leads nowhere — the page you were looking for isn\'t here.' },
];

/** Clean URL for a page stem (Cloudflare serves /about from about.html). */
export const href = (stem) => (stem === 'index' ? './' : stem);

/** Top-nav links. [label, stem]. */
export const NAV = [
    ['Home', 'index'],
    ['About', 'about'],
    ['The World', 'story'],
    ['Kin', 'creatures'],
    ['FAQ', 'faq'],
    ['Licensing', 'license'],
];

/** Footer-only legal links. */
export const LEGAL_NAV = [
    ['Privacy', 'privacy'],
    ['Terms', 'terms'],
];

/** The ten type colours — mirrors theme.ts typeColor (used for kin/type chips). */
export const TYPE_COLORS = {
    Ember: '#ff8a3d', Tide: '#4fb4ff', Verdant: '#7bdc6b',
    Stone: '#c9a86a', Storm: '#b9a6ff', Frost: '#a9e8ff',
    Solar: '#ffd76b', Lunar: '#8aa0ff', Light: '#fff3c0',
    Dark: '#6b6480',
};

/** Colour for a type name (falls back to diamond). */
export const typeColor = (type) => TYPE_COLORS[type] ?? '#9fe7ff';

/** The ten types in canon order (constellation eight + Light/Dark). */
export const TYPE_ORDER = ['Ember', 'Tide', 'Verdant', 'Stone', 'Storm', 'Frost', 'Solar', 'Lunar', 'Light', 'Dark'];

/**
 * Elemental type chart — mirrors src/game/data/type-chart.json (the
 * authoritative, balance-locked source). chart[ATTACKER][DEFENDER] = damage
 * multiplier; any pair not listed is neutral (×1). If the game's chart ever
 * changes, mirror it here. Mirror axes deal mutual ×2: Solar↔Lunar, Light↔Dark.
 */
export const TYPE_CHART = {
    Ember: { Verdant: 2, Frost: 2, Ember: 0.5, Tide: 0.5, Stone: 0.5, Solar: 0.5 },
    Tide: { Ember: 2, Stone: 2, Tide: 0.5, Verdant: 0.5, Storm: 0.5, Lunar: 0.5 },
    Verdant: { Tide: 2, Stone: 2, Verdant: 0.5, Ember: 0.5 },
    Stone: { Ember: 2, Storm: 2, Stone: 0.5, Tide: 0.5, Verdant: 0.5 },
    Storm: { Tide: 2, Verdant: 2, Solar: 2, Storm: 0.5, Frost: 0.5, Stone: 0 },
    Frost: { Verdant: 2, Storm: 2, Stone: 2, Frost: 0.5, Ember: 0.5, Tide: 0.5, Solar: 0.5 },
    Solar: { Frost: 2, Lunar: 2, Dark: 2, Solar: 0.5, Ember: 0.5, Tide: 0.5, Stone: 0.5 },
    Lunar: { Solar: 2, Tide: 2, Lunar: 0.5, Dark: 0 },
    Light: { Dark: 2, Light: 0.5, Stone: 0.5 },
    Dark: { Light: 2, Lunar: 2, Dark: 0.5, Solar: 0.5 },
};

/** Damage multiplier for one attacker→defender pair (1 = neutral). */
export const typeMultiplier = (a, d) => TYPE_CHART[a]?.[d] ?? 1;

/** Offensive/defensive profile for one type, from TYPE_CHART. */
export function typeProfile(t) {
    const p = { strong: [], noEffect: [], weak: [], resists: [], immune: [] };
    for (const other of TYPE_ORDER) {
        const out = typeMultiplier(t, other);
        if (out >= 2) p.strong.push(other);
        else if (out === 0) p.noEffect.push(other);

        const inc = typeMultiplier(other, t);
        if (inc >= 2) p.weak.push(other);
        else if (inc === 0.5) p.resists.push(other);
        else if (inc === 0) p.immune.push(other);
    }
    return p;
}

/** Escape helper. */
export const e = (s) => String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

/** A single type as a tinted chip. */
export const typeChip = (name, extra = '') =>
    `<span class="${e('type-chip' + (extra ? ' ' + extra : ''))}" style="--tint: ${e(typeColor(name))}">${e(name)}</span>`;

/** A list of types as chips, or an em-dash when empty. */
export const typeChips = (names) =>
    names.length ? names.map((n) => typeChip(n)).join('') : '<span class="mtype-none">—</span>';

/** The first-50 kin list generated from species.json into assets/data/kin.json. */
export function loadKin() {
    const path = `${HERE}assets/data/kin.json`;
    return existsSync(path) ? JSON.parse(readFileSync(path, 'utf8')) : [];
}

/** The founding trio — canon (the three kin on the logo). Mirrors
 *  src/game/content/starters.ts. Image stems live under assets/img/kin/. */
export const STARTERS = [
    { name: 'Vulpyre', type: 'Ember', tint: '#ff8a3d', cat: 'Hearth-Fox Kin', img: '001_vulpyre',
      blurb: 'A hearth-spark fox. Warm, eager, quick to flare — when a Vulpyre trusts you, its mane burns a steadier gold.' },
    { name: 'Brinix', type: 'Tide', tint: '#4fb4ff', cat: 'Tide-Hum Kin', img: '002_brinix',
      blurb: 'A moonlit pooler. Calm, steady, deep as the bay — it hums a bubbling tune that settles nervous kin.' },
    { name: 'Cloverkit', type: 'Verdant', tint: '#7bdc6b', cat: 'Clover-Cub Kin', img: '152_cloverkit',
      blurb: 'A clover sprite. Gentle, lucky, stubbornly alive — its four-leaf clover gathers what light remains and glows a soft green.' },
];

/** World mood-pieces (concept-art masters copied into assets/img/world/). */
export const WORLD_GALLERY = [
    { img: 'tinderwick', name: 'Tinderwick', blurb: 'The ember-lit harbour town where every Wayfaring begins.' },
    { img: 'dimglass-coast', name: 'Dimglass Coast', blurb: 'A darkened shore where the first wild kin roam the verge.' },
    { img: 'pearlmoor-quay', name: 'Pearlmoor Quay', blurb: 'A tide-washed jetty town of lamplit boardwalks.' },
    { img: 'lanternway', name: 'The Lanternway', blurb: 'Sleeping roads strung with lanterns between the valleys.' },
    { img: 'hushfrost-pass', name: 'Hushfrost Pass', blurb: 'A frostbound mountain road where the cold keeps its own counsel.' },
    { img: 'nightreach-observatory', name: 'Nightreach', blurb: 'Star-tenders chart the dimming sky from a clifftop dome.' },
    { img: 'sunken-solarium', name: 'Sunken Solarium', blurb: 'A drowned hall where trapped sunlight still glimmers.' },
    { img: 'vesper-crossroads', name: 'Vesper Crossroads', blurb: 'The hub where every sleeping road in Vesperholm meets.' },
    { img: 'umbral-spire', name: 'The Umbral Spire', blurb: 'The four-way heart that opens once all eight Gleams are earned.' },
];

/** Homepage "explore the rest of the site" teasers. Mirrors NAV (sans Home). */
export const EXPLORE = [
    { stem: 'story', ico: '🌙', label: 'The World',
      blurb: 'Step into the Long Dusk — the tale of Vesperholm, the gentle Hollowing, and the night that forgot to lift.' },
    { stem: 'creatures', ico: '🦊', label: 'Meet the Kin',
      blurb: 'Browse the first fifty of over 150 original creatures — their elements, kindlings and matchups.' },
    { stem: 'faq', ico: '❓', label: 'FAQ',
      blurb: 'Is it free? Does it save? Works on mobile? The quick answers before you set out.' },
    { stem: 'about', ico: '✨', label: 'About the game',
      blurb: 'Why we made PixelKin — a love letter to handheld-era creature-collecting, and how it\'s built.' },
    { stem: 'license', ico: '📜', label: 'Licensing',
      blurb: 'Like the world, characters, music or art? Talk to us about licensing and partnerships.' },
];

/** The eight Lumenaries (masters copied into assets/img/lumenary/). */
export const LUMENARIES = ['Ember', 'Tide', 'Verdant', 'Stone', 'Storm', 'Frost', 'Solar', 'Lunar']
    .map((type) => ({ img: type.toLowerCase(), type, tint: TYPE_COLORS[type] }));

/** Simple {{TOKEN}} values available to every page body. */
export function tokens(page) {
    const contact = new URL(STUDIO_CONTACT);
    return {
        SITE_NAME, SITE_TAGLINE, GAME_URL, STUDIO_NAME, STUDIO_URL, STUDIO_CONTACT,
        STUDIO_CONTACT_LABEL: contact.host + contact.pathname,
        YEAR: String(new Date().getFullYear()),
        UPDATED: page.updated ?? '',
    };
}

/** Data-driven sections, keyed by the <!-- block:name --> marker. */
export const BLOCKS = {
    'world-gallery': () => WORLD_GALLERY.map((w) => `
            <figure class="shot" tabindex="0" role="button"
                    data-lb data-lb-group="world"
                    data-lb-img="assets/img/world/${e(w.img)}.webp"
                    data-lb-title="${e(w.name)}"
                    data-lb-blurb="${e(w.blurb)}">
                <img src="assets/img/world/${e(w.img)}.webp" alt="${e(w.name)}" loading="lazy">
                <figcaption>
                    <span class="shot-name">${e(w.name)}</span>
                    <span class="shot-blurb">${e(w.blurb)}</span>
                </figcaption>
                <span class="shot-zoom" aria-hidden="true">⤢</span>
            </figure>`).join(''),

    starters: () => STARTERS.map((k) => `
            <article class="kin-card" style="--tint: ${e(k.tint)}">
                <div class="kin-art">
                    <img src="assets/img/kin/${e(k.img)}_front.webp" alt="${e(k.name)}" loading="lazy">
                </div>
                <h3 class="kin-name">${e(k.name)}</h3>
                <span class="type-chip">${e(k.type)}</span>
                <p class="kin-blurb">${e(k.blurb)}</p>
            </article>`).join(''),

    'starters-lg': () => STARTERS.map((k) => `
            <article class="kin-card kin-card-lg" style="--tint: ${e(k.tint)}">
                <div class="kin-art">
                    <img src="assets/img/kin/${e(k.img)}_front.webp" alt="${e(k.name)}" loading="lazy">
                </div>
                <h3 class="kin-name">${e(k.name)}</h3>
                <span class="type-chip">${e(k.type)}</span>
                <p class="kin-cat">${e(k.cat)}</p>
                <p class="kin-blurb">${e(k.blurb)}</p>
            </article>`).join(''),

    explore: () => EXPLORE.map((x) => `
            <a class="explore-card" href="${e(href(x.stem))}">
                <span class="explore-ico" aria-hidden="true">${x.ico}</span>
                <span class="explore-head">
                    <span class="explore-label">${e(x.label)}</span>
                    <span class="explore-arrow" aria-hidden="true">›</span>
                </span>
                <span class="explore-blurb">${e(x.blurb)}</span>
            </a>`).join(''),

    lumenaries: () => LUMENARIES.map((l) => `
            <figure class="lumen" style="--tint: ${e(l.tint)}" tabindex="0" role="button"
                    data-lb data-lb-group="lumen"
                    data-lb-img="assets/img/lumenary/${e(l.img)}.webp"
                    data-lb-title="${e(l.type)} Lumenary"
                    data-lb-blurb="The ${e(l.type)} warden's hall — best its Lampwarden to earn the ${e(l.type)} Gleam."
                    data-lb-chips="${e(l.type + ',' + l.tint)}">
                <img src="assets/img/lumenary/${e(l.img)}.webp" alt="${e(l.type)} Lumenary" loading="lazy">
                <figcaption class="type-chip">${e(l.type)}</figcaption>
                <span class="shot-zoom" aria-hidden="true">⤢</span>
            </figure>`).join(''),

    'kin-grid': () => loadKin().map((k) => {
        const id3 = String(k.id).padStart(3, '0');
        const chips = k.types.map((t) => `${t},${typeColor(t)}`).join(';');
        return `
            <figure class="kin-cell" style="--tint: ${e(typeColor(k.types[0]))}" tabindex="0" role="button"
                    data-lb data-lb-group="kin" data-lb-pixel="1"
                    data-lb-img="assets/img/kin/battle/${e(id3)}.webp"
                    data-lb-title="#${e(id3)} · ${e(k.name)}"
                    data-lb-blurb="${e(k.cat)}"
                    data-lb-chips="${e(chips)}">
                <img src="assets/img/kin/icons/${e(id3)}.webp" alt="${e(k.name)}" loading="lazy">
                <figcaption>${e(k.name)}</figcaption>
                <span class="kin-no">#${e(id3)}</span>
            </figure>`;
    }).join(''),

    'type-legend': () => TYPE_ORDER.map((t) => `
                ${typeChip(t)}`).join(''),

    matchups: () => TYPE_ORDER.map((t) => {
        const p = typeProfile(t);
        return `
            <article class="mtype-card" style="--tint: ${e(typeColor(t))}">
                <h3 class="mtype-head">${typeChip(t)}</h3>
                <dl class="mtype-rows">
                    <div class="mtype-row mtype-strong">
                        <dt>Strong vs</dt>
                        <dd>${typeChips(p.strong)}</dd>
                    </div>
                    <div class="mtype-row mtype-weak">
                        <dt>Weak to</dt>
                        <dd>${typeChips(p.weak)}</dd>
                    </div>
                    <div class="mtype-row mtype-resist">
                        <dt>Resists</dt>
                        <dd>${typeChips(p.resists)}</dd>
                    </div>${p.immune.length ? `
                    <div class="mtype-row mtype-immune">
                        <dt>Immune to</dt>
                        <dd>${typeChips(p.immune)}</dd>
                    </div>` : ''}
                </dl>${p.noEffect.length ? `
                <p class="mtype-note">Can't damage ${e(p.noEffect.join(', '))}.</p>` : ''}
            </article>`;
    }).join(''),
};
