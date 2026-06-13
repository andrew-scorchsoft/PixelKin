<?php
/**
 * Site-wide configuration and shared data for the PixelKin marketing site.
 *
 * This is intentionally tiny — no framework, just a few constants and helpers
 * that the page templates and partials pull from. Keep brand facts (vocabulary,
 * the starter trio, the palette) sourced from the game canon so the site never
 * drifts from CLAUDE.md / the design docs.
 */

declare(strict_types=1);

/** Where the playable game lives, relative to the site root, once a release is
 *  assembled (tools/build/assemble_release.mjs drops dist/ into release/play/).
 *  Locally this 404s until you run `npm run release` — that's expected. */
const GAME_URL = '/play/';

/** Site identity. */
const SITE_NAME    = 'PixelKin';
const SITE_TAGLINE = 'Lanterns in the dark.';
const SITE_DESC    = 'A retro, handheld-era creature-collecting adventure. Relight the sky one constellation at a time across the valleys of Vesperholm — collect over 150 original kin in your browser.';

/** Studio behind the game. */
const STUDIO_NAME    = 'Scorchsoft';
const STUDIO_URL     = 'https://www.scorchsoft.com/';
const STUDIO_CONTACT = 'https://www.scorchsoft.com/contact-scorchsoft/';

/** Public source repository. */
const GITHUB_URL = 'https://github.com/andrew-scorchsoft/PixelKin';

/**
 * Top-nav links. label => href. Pages are flat .php files at the site root.
 */
const NAV = [
    'Home'      => 'index.php',
    'About'     => 'about.php',
    'The World' => 'story.php',
    'Kin'       => 'creatures.php',
    'FAQ'       => 'faq.php',
    'Licensing' => 'license.php',
];

/** Footer-only legal links. */
const LEGAL_NAV = [
    'Privacy'    => 'privacy.php',
    'Terms'      => 'terms.php',
];

/** The ten type colours — mirrors theme.ts typeColor (used for kin/type chips). */
const TYPE_COLORS = [
    'Ember'   => '#ff8a3d', 'Tide'  => '#4fb4ff', 'Verdant' => '#7bdc6b',
    'Stone'   => '#c9a86a', 'Storm' => '#b9a6ff', 'Frost'   => '#a9e8ff',
    'Solar'   => '#ffd76b', 'Lunar' => '#8aa0ff', 'Light'   => '#fff3c0',
    'Dark'    => '#6b6480',
];

/** Colour for a type name (falls back to diamond). */
function type_color(string $type): string {
    return TYPE_COLORS[$type] ?? '#9fe7ff';
}

/** The ten types in canon order (constellation eight + Light/Dark). */
const TYPE_ORDER = [
    'Ember', 'Tide', 'Verdant', 'Stone', 'Storm', 'Frost', 'Solar', 'Lunar', 'Light', 'Dark',
];

/**
 * Elemental type chart — mirrors src/game/data/type-chart.json (which is the
 * authoritative, balance-locked source shared by the game engine and the
 * Monte-Carlo simulator). chart[ATTACKER][DEFENDER] = damage multiplier; any
 * pair not listed is neutral (×1). If the game's chart ever changes, mirror it
 * here. Two deliberate "mirror" axes deal mutual ×2: Solar↔Lunar, Light↔Dark.
 */
const TYPE_CHART = [
    'Ember'   => ['Verdant' => 2, 'Frost' => 2, 'Ember' => 0.5, 'Tide' => 0.5, 'Stone' => 0.5, 'Solar' => 0.5],
    'Tide'    => ['Ember' => 2, 'Stone' => 2, 'Tide' => 0.5, 'Verdant' => 0.5, 'Storm' => 0.5, 'Lunar' => 0.5],
    'Verdant' => ['Tide' => 2, 'Stone' => 2, 'Verdant' => 0.5, 'Ember' => 0.5],
    'Stone'   => ['Ember' => 2, 'Storm' => 2, 'Stone' => 0.5, 'Tide' => 0.5, 'Verdant' => 0.5],
    'Storm'   => ['Tide' => 2, 'Verdant' => 2, 'Solar' => 2, 'Storm' => 0.5, 'Frost' => 0.5, 'Stone' => 0],
    'Frost'   => ['Verdant' => 2, 'Storm' => 2, 'Stone' => 2, 'Frost' => 0.5, 'Ember' => 0.5, 'Tide' => 0.5, 'Solar' => 0.5],
    'Solar'   => ['Frost' => 2, 'Lunar' => 2, 'Dark' => 2, 'Solar' => 0.5, 'Ember' => 0.5, 'Tide' => 0.5, 'Stone' => 0.5],
    'Lunar'   => ['Solar' => 2, 'Tide' => 2, 'Lunar' => 0.5, 'Dark' => 0],
    'Light'   => ['Dark' => 2, 'Light' => 0.5, 'Stone' => 0.5],
    'Dark'    => ['Light' => 2, 'Lunar' => 2, 'Dark' => 0.5, 'Solar' => 0.5],
];

/** Damage multiplier for one attacker→defender pair (1.0 = neutral). */
function type_multiplier(string $attacker, string $defender): float {
    return (float)(TYPE_CHART[$attacker][$defender] ?? 1.0);
}

/**
 * Build a defensive/offensive profile for one type, from TYPE_CHART:
 *   strong   — types this one deals ×2 to (offensive reach)
 *   noEffect — types this one can't damage at all (×0 offense)
 *   weak     — types that deal ×2 to this one (its weaknesses)
 *   resists  — types this one takes ×½ from
 *   immune   — types this one takes ×0 from (defensive immunity)
 */
function type_profile(string $t): array {
    $strong = $noEffect = $weak = $resists = $immune = [];
    foreach (TYPE_ORDER as $other) {
        $out = type_multiplier($t, $other);     // this type attacking $other
        if ($out >= 2)        $strong[]   = $other;
        elseif ($out === 0.0) $noEffect[] = $other;

        $in = type_multiplier($other, $t);       // $other attacking this type
        if ($in >= 2)         $weak[]    = $other;
        elseif ($in === 0.5)  $resists[] = $other;
        elseif ($in === 0.0)  $immune[]  = $other;
    }
    return compact('strong', 'noEffect', 'weak', 'resists', 'immune');
}

/** Render a single type as a tinted chip (markup helper). */
function type_chip(string $name, string $extraClass = ''): string {
    $cls = 'type-chip' . ($extraClass !== '' ? ' ' . $extraClass : '');
    return '<span class="' . e($cls) . '" style="--tint: ' . e(type_color($name)) . '">' . e($name) . '</span>';
}

/** Render a list of types as chips, or an em-dash when empty. */
function type_chips(array $names): string {
    if (!$names) return '<span class="mtype-none">—</span>';
    return implode('', array_map(fn($n) => type_chip($n), $names));
}

/** Load the first-50 kin list generated from species.json into assets/data/kin.json. */
function load_kin(): array {
    $path = __DIR__ . '/../assets/data/kin.json';
    if (!is_file($path)) return [];
    return json_decode((string)file_get_contents($path), true) ?? [];
}

/**
 * The founding trio — canon (the three kin on the logo). Mirrors
 * src/game/content/starters.ts and the per-kin species JSON. Image stems live
 * under assets/img/kin/.
 */
const STARTERS = [
    [
        'name'  => 'Vulpyre',
        'type'  => 'Ember',
        'tint'  => '#ff8a3d',
        'cat'   => 'Hearth-Fox Kin',
        'img'   => '001_vulpyre',
        'blurb' => 'A hearth-spark fox. Warm, eager, quick to flare — when a Vulpyre trusts you, its mane burns a steadier gold.',
    ],
    [
        'name'  => 'Brinix',
        'type'  => 'Tide',
        'tint'  => '#4fb4ff',
        'cat'   => 'Tide-Hum Kin',
        'img'   => '002_brinix',
        'blurb' => 'A moonlit pooler. Calm, steady, deep as the bay — it hums a bubbling tune that settles nervous kin.',
    ],
    [
        'name'  => 'Cloverkit',
        'type'  => 'Verdant',
        'tint'  => '#7bdc6b',
        'cat'   => 'Clover-Cub Kin',
        'img'   => '152_cloverkit',
        'blurb' => 'A clover sprite. Gentle, lucky, stubbornly alive — its four-leaf clover gathers what light remains and glows a soft green.',
    ],
];

/**
 * World mood-pieces to tease the regions of Vesperholm. Images are concept-art
 * masters copied into assets/img/world/. Captions stay in canon voice.
 */
const WORLD_GALLERY = [
    ['img' => 'tinderwick',              'name' => 'Tinderwick',     'blurb' => 'The ember-lit harbour town where every Wayfaring begins.'],
    ['img' => 'dimglass-coast',          'name' => 'Dimglass Coast', 'blurb' => 'A darkened shore where the first wild kin roam the verge.'],
    ['img' => 'pearlmoor-quay',          'name' => 'Pearlmoor Quay', 'blurb' => 'A tide-washed jetty town of lamplit boardwalks.'],
    ['img' => 'lanternway',              'name' => 'The Lanternway',  'blurb' => 'Sleeping roads strung with lanterns between the valleys.'],
    ['img' => 'hushfrost-pass',          'name' => 'Hushfrost Pass',  'blurb' => 'A frostbound mountain road where the cold keeps its own counsel.'],
    ['img' => 'nightreach-observatory',  'name' => 'Nightreach',      'blurb' => 'Star-tenders chart the dimming sky from a clifftop dome.'],
    ['img' => 'sunken-solarium',         'name' => 'Sunken Solarium', 'blurb' => 'A drowned hall where trapped sunlight still glimmers.'],
    ['img' => 'vesper-crossroads',       'name' => 'Vesper Crossroads','blurb' => 'The hub where every sleeping road in Vesperholm meets.'],
    ['img' => 'umbral-spire',            'name' => 'The Umbral Spire', 'blurb' => 'The four-way heart that opens once all eight Gleams are earned.'],
];

/**
 * Homepage "explore the rest of the site" teasers — a sign-posting band so a
 * reader who only ever sees the homepage can find the deeper pages. label =>
 * [href, icon, blurb]. Mirrors the NAV destinations (sans Home); keep blurbs in
 * canon voice and in step with each page's own intro.
 */
const EXPLORE = [
    [
        'href'  => 'story.php',
        'ico'   => '🌙',
        'label' => 'The World',
        'blurb' => 'Step into the Long Dusk — the tale of Vesperholm, the gentle Hollowing, and the night that forgot to lift.',
    ],
    [
        'href'  => 'creatures.php',
        'ico'   => '🦊',
        'label' => 'Meet the Kin',
        'blurb' => 'Browse the first fifty of over 150 original creatures — their elements, kindlings and matchups.',
    ],
    [
        'href'  => 'faq.php',
        'ico'   => '❓',
        'label' => 'FAQ',
        'blurb' => 'Is it free? Does it save? Works on mobile? The quick answers before you set out.',
    ],
    [
        'href'  => 'about.php',
        'ico'   => '✨',
        'label' => 'About the game',
        'blurb' => 'Why we made PixelKin — a love letter to handheld-era creature-collecting, and how it\'s built.',
    ],
    [
        'href'  => 'license.php',
        'ico'   => '📜',
        'label' => 'Licensing',
        'blurb' => 'Like the world, characters, music or art? Talk to us about licensing and partnerships.',
    ],
];

/**
 * The eight Lumenaries — one per constellation element. Image masters copied
 * into assets/img/lumenary/. Tints mirror theme.ts typeColor.
 */
const LUMENARIES = [
    ['img' => 'ember',   'type' => 'Ember',   'tint' => '#ff8a3d'],
    ['img' => 'tide',    'type' => 'Tide',    'tint' => '#4fb4ff'],
    ['img' => 'verdant', 'type' => 'Verdant', 'tint' => '#7bdc6b'],
    ['img' => 'stone',   'type' => 'Stone',   'tint' => '#c9a86a'],
    ['img' => 'storm',   'type' => 'Storm',   'tint' => '#b9a6ff'],
    ['img' => 'frost',   'type' => 'Frost',   'tint' => '#a9e8ff'],
    ['img' => 'solar',   'type' => 'Solar',   'tint' => '#ffd76b'],
    ['img' => 'lunar',   'type' => 'Lunar',   'tint' => '#8aa0ff'],
];

/**
 * Render a page. Pulls in the shared chrome around a body, keeping each page
 * file to just its own content.
 *   $title — the <title>/og:title prefix for this page.
 *   $page  — the current nav href (for active state).
 *   $desc  — the meta/og description for this page (falls back to SITE_DESC).
 */
function page_head(string $title, string $page, string $desc = ''): void {
    $GLOBALS['__page']  = $page;
    $GLOBALS['__title'] = $title;
    $GLOBALS['__desc']  = $desc !== '' ? $desc : SITE_DESC;
    require __DIR__ . '/header.php';
}

function page_foot(): void {
    require __DIR__ . '/footer.php';
}

/** Escape helper. */
function e(string $s): string {
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}
