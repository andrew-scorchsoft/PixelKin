/**
 * Shared page chrome: <head> (per-page title + meta/OG/Twitter) + masthead,
 * and the footer + shared lightbox markup. Pure functions → HTML strings.
 */

import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import {
    e, href, NAV, LEGAL_NAV, GAME_URL, GITHUB_URL,
    SITE_NAME, SITE_TAGLINE, SITE_DESC, STUDIO_NAME, STUDIO_URL, STUDIO_CONTACT,
} from './site.mjs';

const HERE = fileURLToPath(new URL('.', import.meta.url));

export function header(page) {
    const desc = page.desc || SITE_DESC;
    const ogTitle = page.title === 'Home' ? `${SITE_NAME} — ${SITE_TAGLINE}` : `${page.title} · ${SITE_NAME}`;
    // Per-page social card (1200x630). Falls back to the logo if a page has none.
    const ogCard = existsSync(`${HERE}assets/img/og/${page.stem}.jpg`);
    const ogImage = ogCard ? `assets/img/og/${page.stem}.jpg` : 'assets/img/logo.png';
    const nav = NAV.map(([label, stem]) =>
        `\n            <a href="${e(href(stem))}"${stem === page.stem ? ' class="active"' : ''}>${e(label)}</a>`).join('');
    return `<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#0b1026">${page.noindex ? `
    <base href="/">
    <meta name="robots" content="noindex">` : ''}
    <title>${e(ogTitle)}</title>
    <meta name="description" content="${e(desc)}">
    <meta name="author" content="${e(STUDIO_NAME)}">${page.noindex ? '' : `
    <link rel="canonical" href="${e(href(page.stem))}">`}
    <meta property="og:site_name" content="${e(SITE_NAME)}">
    <meta property="og:title" content="${e(ogTitle)}">
    <meta property="og:description" content="${e(desc)}">
    <meta property="og:type" content="website">
    <meta property="og:image" content="${e(ogImage)}">${ogCard ? `
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">` : ''}
    <meta property="og:image:alt" content="${e(ogTitle)}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${e(ogTitle)}">
    <meta name="twitter:description" content="${e(desc)}">
    <meta name="twitter:image" content="${e(ogImage)}">
    <link rel="icon" type="image/png" href="assets/img/logo.png">
    <link rel="preload" href="assets/fonts/PressStart2P-Regular.ttf" as="font" type="font/ttf" crossorigin>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="starfield" aria-hidden="true"></div>

    <header class="masthead">
        <a class="brand" href="./" aria-label="${e(SITE_NAME)} home">
            <img src="assets/img/logo-text.webp" alt="${e(SITE_NAME)}" class="brand-logo">
        </a>
        <button class="nav-toggle" aria-label="Menu" aria-expanded="false">
            <span></span><span></span><span></span>
        </button>
        <nav class="nav">${nav}
            <a class="nav-cta" href="${e(GAME_URL)}">Play</a>
        </nav>
    </header>

    <main>
`;
}

export function footer() {
    const nav = NAV.map(([label, stem]) => `\n                <a href="${e(href(stem))}">${e(label)}</a>`).join('');
    const legal = LEGAL_NAV.map(([label, stem]) => `\n                <a href="${e(href(stem))}">${e(label)}</a>`).join('');
    return `    </main>

    <footer class="site-footer">
        <div class="foot-inner">
            <a href="./" class="foot-logo-link" aria-label="${e(SITE_NAME)} home">
                <img src="assets/img/logo-text.webp" alt="${e(SITE_NAME)}" class="foot-logo">
            </a>
            <p class="foot-tag">${e(SITE_TAGLINE)}</p>
            <nav class="foot-nav">${nav}
                <a href="${e(GAME_URL)}">Play</a>
            </nav>
            <p class="foot-studio">
                Designed &amp; built by
                <a href="${e(STUDIO_URL)}" target="_blank" rel="noopener">${e(STUDIO_NAME)}</a>
                — app, web &amp; game developers.
                <a href="${e(href('license'))}">Licensing&nbsp;enquiries&nbsp;›</a>
            </p>
            <nav class="foot-legal">${legal}
                <a href="${e(STUDIO_CONTACT)}" target="_blank" rel="noopener">Contact</a>
                <a class="foot-gh" href="${e(GITHUB_URL)}" target="_blank" rel="noopener" aria-label="PixelKin on GitHub">
                    <svg class="gh-ico" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false">
                        <path fill="currentColor" fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.76-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                    GitHub
                </a>
            </nav>
            <p class="foot-fine">
                © ${new Date().getFullYear()} ${e(STUDIO_NAME)}. ${e(SITE_NAME)} is an original
                creature-collecting adventure — inspired by the genre, a copy of nothing.
                Free to play; all rights reserved.
            </p>
        </div>
    </footer>

    <!-- Shared lightbox: any element with [data-lb] (grouped by data-lb-group) opens here. -->
    <div class="lightbox" id="lightbox" hidden aria-modal="true" role="dialog" aria-label="Gallery viewer">
        <div class="lb-backdrop" data-lb-close></div>
        <button class="lb-btn lb-close" data-lb-close aria-label="Close">×</button>
        <button class="lb-btn lb-prev" data-lb-prev aria-label="Previous">‹</button>
        <figure class="lb-figure">
            <img class="lb-img" alt="">
            <figcaption class="lb-cap">
                <span class="lb-chips"></span>
                <span class="lb-title"></span>
                <span class="lb-blurb"></span>
            </figcaption>
        </figure>
        <button class="lb-btn lb-next" data-lb-next aria-label="Next">›</button>
        <div class="lb-count"></div>
    </div>

    <script src="assets/js/main.js" defer></script>
</body>
</html>
`;
}
