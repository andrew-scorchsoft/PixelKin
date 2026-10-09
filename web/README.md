# PixelKin website (`web/`)

The marketing/landing site for **pixelk.in** — a small static HTML site,
on-brand with the game. No framework and no server-side code: page bodies are
plain HTML fragments, and `tools/build/build_site.mjs` (Node) wraps them in the
shared chrome and writes static `.html` files. That's what lets the whole of
pixelk.in serve from a **Cloudflare Worker's static assets** (`wrangler.jsonc`).

This folder is the **source of truth**. The playable game is a *separate* build
(Vite → `dist/`); a release step staples the two together for upload (see
"Deploying" below).

## Layout

```
web/
  site.mjs        # constants, nav, PAGES (title/desc per page), starter/world/lumenary data,
                  #   type chart + colours, kin loader, and BLOCKS (the data-driven sections)
  layout.mjs      # header() — <head> (title + meta/OG/Twitter) + masthead; footer() + lightbox markup
  pages/          # one body fragment per page → served at /<stem> (index → /)
    index.html    #   landing (parallax hero, world gallery, features, starter trio, CTA)
    story.html    #   The Long Dusk — world & story + the eight Lumenaries
    creatures.html#   the starter trio + a clickable grid of the first 50 kin
    faq.html      #   player FAQ (native <details> accordion)
    license.html  #   licensing & partnerships → Scorchsoft contact form
    privacy.html  #   privacy policy
    terms.html    #   terms of use
    404.html      #   "Lost in the Dusk" (served for any unknown path)
  _redirects      # Cloudflare: 301s from the old *.php URLs to the clean ones
  .htaccess       # Apache twin of the above + clean URLs (legacy FTP host only)
  .assetsignore   # keeps .htaccess out of the Worker upload
  assets/
    css/style.css # brand styling (palette + pixel font from the game)
    js/main.js    # mobile nav, hero parallax, gallery lightbox (progressive enhancement)
    data/kin.json # first-50 kin (id/name/types/category) generated from species.json
    fonts/        # Press Start 2P (same pixel font the game uses) + licence
    img/          # logo.png + logo-text.webp + logo-hero.webp, hero/, kin/, world/, lumenary/
```

**Page bodies** use two placeholders, resolved at build time (an unknown one
fails the build): `{{TOKEN}}` for a value from `tokens()` in `site.mjs`
(`SITE_NAME`, `GAME_URL`, `STUDIO_NAME`, `YEAR`, `UPDATED`, … and
`{{tint:Solar}}` for a type colour), and `<!-- block:name -->` for a
data-driven section rendered by `BLOCKS[name]` (world gallery, starters, kin
grid, matchups…). **Add a page** = a `pages/<stem>.html` body + a `PAGES` row
(+ a `NAV` entry if it belongs in the menu). Links between pages use clean
URLs (`href="faq"`, home is `href="./"`).

**Interactivity (all vanilla JS in `main.js`, degrades without it):**
- *Hero* — the pixel-art Tinderwick scene (`img/hero/scene.webp`) under a tuned
  vignette, with a slow pan and pointer-reactive parallax. The translucent nav
  sits over it (it firms up once you scroll past the hero).
- *Lightbox* — any element with `data-lb` (grouped by `data-lb-group`) opens a
  modal with prev/next, keyboard (Esc / ← / →) and chips. Used by the world
  gallery, the Lumenaries, and the kin grid (which shows each kin's battle sprite).

Per-page SEO/social meta comes from each page's `PAGES` row — `layout.mjs`
turns it into `<title>`, `description`, and OpenGraph/Twitter tags. Studio
attribution and the licensing-contact link are `STUDIO_*` constants in `site.mjs`.

Each page also gets its own 1200×630 social-share card: layout.mjs maps the page's
stem to `assets/img/og/<stem>.jpg` (falling back to the logo if absent). They're
JPG, not WebP — Facebook/LinkedIn still don't render WebP link previews reliably.
The cards are a unique pixel-art background per page + the wordmark and page title
composited on top; rebuild them (e.g. after a copy tweak) with:

```bash
../venv/bin/python tools/build_og_cards.py   # from web/ — reads assets/img/og/src/*.webp
```

Edit the `PAGES` titles/subtitles in `tools/build_og_cards.py` to retext; to
re-art a card, regenerate its background master into `assets/img/og/src/<stem>.webp`
with the generate-image skill (dusk pixel-art brief, hero scene as palette ref).
The kin grid reads the generated `assets/data/kin.json` (so the site stays
standalone — it doesn't read `src/` at runtime).

Brand facts (the canon vocabulary, the founding trio, the palette) are sourced
from the game — palette hexes mirror `src/game/config.ts`, the trio mirrors
`src/game/content/starters.ts`. If those change, update `site.mjs`.

### Refreshing the copied art

`assets/img/` and `assets/fonts/` hold copies so the site deploys standalone.
To refresh them from the game masters:

```bash
cp public/assets/ui/logo.png                  web/assets/img/logo.png       # full logo (hero/footer)
cp public/assets/ui/pixelkin-logo-textonly.webp web/assets/img/logo-text.webp # text logo (header)
cp src/styles/fonts/PressStart2P-Regular.ttf  web/assets/fonts/
# starter art (front + portrait) for #001 / #002 / #152:
for d in 001_vulpyre 002_brinix 152_cloverkit; do
  cp public/assets/sprites/creatures/$d/battle_front.webp web/assets/img/kin/${d}_front.webp
  cp public/assets/sprites/creatures/$d/portrait.webp     web/assets/img/kin/${d}_portrait.webp
done
# world mood-pieces + Lumenary halls (concept-art masters → teaser galleries):
cp assets/concept-art/areas/{tinderwick,dimglass-coast,pearlmoor-quay,lanternway,hushfrost-pass,nightreach-observatory,sunken-solarium,vesper-crossroads,umbral-spire}.webp web/assets/img/world/
cp assets/concept-art/lumenaries/{ember,tide,verdant,stone,storm,frost,solar,lunar}.webp web/assets/img/lumenary/
# transparent hero logo + the hero backdrop scene (Tinderwick concept art):
cp public/assets/ui/logo-transparentbg.webp web/assets/img/logo-hero.webp
cp assets/concept-art/areas/tinderwick.webp web/assets/img/hero/scene.webp
```

The kin grid's data + the first-50 icons are generated from the game's
`species.json` (re-run when the roster art changes):

```bash
node -e '
const fs=require("fs");
const d=JSON.parse(fs.readFileSync("src/game/data/species.json")).species.filter(k=>k.id<=50).sort((a,b)=>a.id-b.id);
const out=d.map(k=>{const i=String(k.id).padStart(3,"0"),s=`public/assets/sprites/creatures/${i}_${k.slug}`;
  for(const[v,dir]of[["icon","icons"],["battle_front","battle"]])try{fs.copyFileSync(`${s}/${v}.webp`,`web/assets/img/kin/${dir}/${i}.webp`)}catch{}
  return{id:k.id,name:k.name,types:k.types,cat:k.dex?.category??""}});
fs.writeFileSync("web/assets/data/kin.json",JSON.stringify(out,null,4)+"\n");'
```

## Running locally

From the repo root:

```bash
npm run release:site   # render the pages into release/ (keeps a staged release/play/)
npm run site           # …then serve release/ with wrangler dev → http://localhost:8787
npm run preview:release   # rebuild the game too, then serve → / and /play/ both work
```

`wrangler dev` serves `release/` with exactly the production rules (clean URLs,
`_redirects`, the 404 page). If the game hasn't been built, `/play/` shows a
small "not built here" placeholder instead of 404ing. To work on the game
itself, use `npm run dev` (Vite).

## Deploying to pixelk.in (Cloudflare Workers)

`npm run release` builds the game (`build:dist`: shrunk audio via ffmpeg from
PATH or the `ffmpeg-static` devDependency, sourcemaps stripped) and assembles:

```
release/
  index.html, about.html, …, 404.html, _redirects, assets/   → pixelk.in/
  play/                                                      → pixelk.in/play/
```

`wrangler.jsonc` points the Worker's static assets at `release/`
(`html_handling: auto-trailing-slash` → `/about` serves `about.html`;
`not_found_handling: 404-page`). There's no Worker script.

**Workers Builds** (Cloudflare dashboard → the `pixelkin` Worker → Settings →
Build) is connected to the GitHub repo: build command `npm run release`, deploy
command `npx wrangler deploy`, preview command `npx wrangler versions upload`,
build variable `NODE_VERSION=22`. A push to `main` goes live; other branches get
preview URLs. By hand: `npm run deploy` (needs `wrangler login`).

The legacy FTP path (`npm run deploy:ftp`, the `deploy-ftp` skill) still works
— `release/` is plain static files, and `web/.htaccess` gives Apache the same
clean URLs and `.php` redirects.
