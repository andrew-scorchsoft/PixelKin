#!/usr/bin/env node
/**
 * build_music_data.mjs — the website's soundtrack listing (web/assets/data/music.json).
 *
 * One row per music cue the GAME actually uses (a track referenced anywhere in
 * src/), grouped by region, with:
 *   - where it plays: the display names of every map whose `music` is that file
 *     (src/game/data/world/maps.ts → the map JSON's display_name), else the cue's
 *     remaster `where` (battles, cutscenes, stings);
 *   - the classic render and, once it exists, the remastered score + its loop point
 *     (src/game/data/music-remaster.json), so the page loops it like the game does.
 *
 * Audio URLs are relative to the site root and point INTO the game build
 * (play/assets/audio/music/…), so the site ships no second copy of the music.
 *
 *   node tools/build/build_music_data.mjs [--check]
 */
import { readFileSync, readdirSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('../../', import.meta.url)));
const MUSIC = join(ROOT, 'public/assets/audio/music');
const OUT = join(ROOT, 'web/assets/data/music.json');

/** Region groups, in journey order. First matching prefix wins. */
const GROUPS = [
    ['South — the blue-hour start', ['tinderwick', 'duskapple', 'beacon', 'dimglass-coast', 'pearlmoor']],
    ['East — wonder & discovery', ['saltreach-fen', 'lowleaf-hollow', 'cinderhead-mine']],
    ['North — energy & cold beauty', ['galehigh-terraces', 'windward-stair', 'pale-vault-glacier']],
    ['West — reaching for dawn', ['hushfrost-pass', 'sunken-solarium', 'sunvault-climb', 'nightreach-observatory']],
    ['The outer ring', ['vesper-crossroads', 'coldfog-marches', 'lanternway']],
    ['Central — darkest, then the turn', ['penumbra-ring', 'umbral-spire']],
    ['Epilogue', ['dawnstead', 'dawn-breaks', 'ending-credits']],
    ['Indoors — rooms, shops, inns & halls', ['interior-hearth', 'interior-sunny', 'interior-lamplit', 'interior-study', 'interior-hush', 'interior-unease', 'shop-', 'inn-', 'lumenary-']],
    ['Battles', ['battle-']],
    ['Story & fanfares', ['title', 'coldopen', 'gleam-', 'sting-']],
];

/** Friendly names for cues that aren't a single place. */
const CUE_NAMES = {
    'title': 'Title screen',
    'coldopen-foreboding': 'The cold open',
    'gleam-fanfare': 'A Gleam relit (fanfare)',
    'gleam-emotional': 'A Gleam relit',
    'sting-hour': 'The Hours (sting)',
    'dawn-breaks': 'Dawn breaks',
    'ending-credits': 'Ending credits',
    'battle-main-dusk-duel': 'Battle — wild kin & trainers',
    'battle-emberfall': 'Battle — route trainers & Lampwardens',
    'battle-nightfall': 'Battle — Vigilants & the Hollowing',
    'battle-veil': 'Battle — Wren, your rival',
    'battle-boss-eclipse': 'Battle — the last stand',
    'battle-hours': 'Battle — the Three Hours',
    'pearlmoor-blessing': 'The Tide blessing',
    'duskapple-orchard': 'Duskapple Orchard — the fallen star',
    'beacon-stair': 'The Tinderwick Beacon',
    'interior-hearth': 'Indoors — a warm home',
    'interior-sunny': 'Indoors — sunny rooms',
    'interior-lamplit': 'Indoors — lamplit rooms',
    'interior-study': 'Indoors — charts & lenses',
    'interior-hush': 'Indoors — the quiet after',
    'interior-unease': 'Indoors — a cold hearth',
    'shop-counter': 'Shops',
    'inn-rest': 'Inns — rest a while',
    'lumenary-hall': 'The Lumenary halls',
    'lanternway-a': 'The Lanternway',
    'dimglass-coast-b': 'The coast road, last light',
};

function walk(dir) {
    const out = [];
    for (const name of readdirSync(dir)) {
        const p = join(dir, name);
        if (statSync(p).isDirectory()) out.push(...walk(p));
        else if (/\.(ts|json)$/.test(name)) out.push(p);
    }
    return out;
}

const srcText = walk(join(ROOT, 'src'))
    .filter((p) => !p.endsWith('music-remaster.json'))
    .map((p) => readFileSync(p, 'utf8'))
    .join('\n');

// map id -> music file id, display name
const mapsTs = readFileSync(join(ROOT, 'src/game/data/world/maps.ts'), 'utf8');
const placesByTrack = {};
for (const m of mapsTs.matchAll(/^ {2}(\w+): \{([\s\S]*?)^ {2}\},?$/gm)) {
    const body = m[2];
    // Every cue the map can play: its own music AND any story-state `music_when` rule.
    const musics = [...body.matchAll(/music: '([^']+)'/g)].map((x) => x[1]);
    const json = body.match(/json: '([^']+)'/)?.[1];
    if (!musics.length || !json) continue;
    let name = m[1];
    try {
        name = JSON.parse(readFileSync(join(ROOT, 'public', json), 'utf8')).display_name || name;
    } catch { /* keep the id */ }
    for (const music of musics) {
        const id = music.split('/').pop().replace(/\.mp3$/, '');
        (placesByTrack[id] ??= new Set()).add(name);
    }
}

const remaster = JSON.parse(readFileSync(join(ROOT, 'src/game/data/music-remaster.json'), 'utf8')).tracks;

const groups = GROUPS.map(([title]) => ({ title, tracks: [] }));
for (const file of readdirSync(MUSIC).filter((f) => f.endsWith('.mp3')).sort()) {
    const id = file.replace(/\.mp3$/, '');
    if (!new RegExp(`['/]${id}(\\.mp3)?'`).test(srcText)) continue; // unused variant
    const gi = GROUPS.findIndex(([, pre]) => pre.some((p) => id.startsWith(p)));
    const r = remaster[id];
    const places = [...(placesByTrack[id] ?? [])];
    const base = id.replace(/-[abc]$/, '');
    const fallbackTitle = base.split('-').map((w) => w[0].toUpperCase() + w.slice(1)).join(' ');
    groups[gi < 0 ? groups.length - 1 : gi].tracks.push({
        id,
        title: CUE_NAMES[id] ?? (places[0] ?? fallbackTitle),
        where: places.length ? places.join(' · ') : (r?.where ?? ''),
        mood: r?.mood ?? '',
        classic: `play/assets/audio/music/${id}.mp3`,
        remaster: r ? `play/assets/audio/music/remaster/${id}.mp3` : null,
        loop_start: r ? r.loop_start : null,
    });
}

// Journey order inside each group: by the GROUPS prefix order, then -a/-b/-c.
for (const [gi, g] of groups.entries()) {
    const pre = GROUPS[gi][1];
    const rank = (id) => { const i = pre.findIndex((p) => id.startsWith(p)); return i < 0 ? 99 : i; };
    g.tracks.sort((a, b) => rank(a.id) - rank(b.id) || a.id.localeCompare(b.id));
}

const data = JSON.stringify({ _generated: 'tools/build/build_music_data.mjs', groups: groups.filter((g) => g.tracks.length) }, null, 1) + '\n';
if (process.argv.includes('--check')) {
    const cur = existsSync(OUT) ? readFileSync(OUT, 'utf8') : '';
    if (cur !== data) {
        console.error('web/assets/data/music.json is stale: run node tools/build/build_music_data.mjs');
        process.exit(1);
    }
    console.log('music.json up to date');
} else {
    writeFileSync(OUT, data);
    const n = groups.reduce((a, g) => a + g.tracks.length, 0);
    const nr = groups.reduce((a, g) => a + g.tracks.filter((t) => t.remaster).length, 0);
    console.log(`wrote web/assets/data/music.json (${n} cues, ${nr} remastered)`);
}
