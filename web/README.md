# PixelKin website (`web/`)

The marketing/landing site for **pixelk.in** — a small, self-contained PHP +
HTML site, on-brand with the game. No framework: a few flat `.php` pages share
chrome through `includes/` partials.

This folder is the **source of truth**. The playable game is a *separate* build
(Vite → `dist/`); a release step staples the two together for upload (see
"Deploying" below).

## Layout

```
web/
  index.php       # landing (parallax hero, world gallery, features, starter trio, CTA)
  story.php       # The Long Dusk — world & story + the eight Lumenaries
  creatures.php   # the starter trio + a clickable grid of the first 50 kin
  faq.php         # player FAQ — getting started, controls, saving, gameplay basics (native <details> accordion)
  license.php     # licensing & partnerships → Scorchsoft contact form
  privacy.php     # privacy policy
  terms.php       # terms of use (as-is, no warranties, may be taken offline)
  includes/
    config.php    # constants, starter/world/lumenary data, type colours, kin loader, page_head()
    header.php    # <head> (per-page title + meta/OG/Twitter) + masthead/nav
    footer.php    # footer (Scorchsoft attribution, licensing + legal nav) + shared lightbox markup
  assets/
    css/style.css # brand styling (palette + pixel font from the game)
    js/main.js    # mobile nav, hero parallax, gallery lightbox (progressive enhancement)
    data/kin.json # first-50 kin (id/name/types/category) generated from species.json
    fonts/        # Press Start 2P (same pixel font the game uses) + licence
    img/          # logo.png + logo-text.webp + logo-hero.webp, hero/, kin/, world/, lumenary/
```

**Interactivity (all vanilla JS in `main.js`, degrades without it):**
- *Hero* — the pixel-art Tinderwick scene (`img/hero/scene.webp`) under a tuned
  vignette, with a slow pan and pointer-reactive parallax. The translucent nav
  sits over it (it firms up once you scroll past the hero).
- *Lightbox* — any element with `data-lb` (grouped by `data-lb-group`) opens a
  modal with prev/next, keyboard (Esc / ← / →) and chips. Used by the world
  gallery, the Lumenaries, and the kin grid (which shows each kin's battle sprite).

Per-page SEO/social meta is driven by `page_head($title, $page, $desc)` — header.php
turns it into `<title>`, `description`, and OpenGraph/Twitter tags. Studio
attribution and the licensing-contact link are `STUDIO_*` constants in `config.php`.
The kin grid reads the generated `assets/data/kin.json` (so the site stays
standalone — it doesn't read `src/` at runtime).

Brand facts (the canon vocabulary, the founding trio, the palette) are sourced
from the game — palette hexes mirror `src/game/config.ts`, the trio mirrors
`src/game/content/starters.ts`. If those change, update `includes/config.php`.

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
php -r '
$d=json_decode(file_get_contents("src/game/data/species.json"),true)["species"];
usort($d,fn($a,$b)=>$a["id"]<=>$b["id"]); $out=[];
foreach($d as $k){ if($k["id"]>50) continue;
  $i=str_pad((string)$k["id"],3,"0",STR_PAD_LEFT);
  @copy("public/assets/sprites/creatures/{$i}_{$k["slug"]}/icon.webp","web/assets/img/kin/icons/$i.webp");
  @copy("public/assets/sprites/creatures/{$i}_{$k["slug"]}/battle_front.webp","web/assets/img/kin/battle/$i.webp");
  $out[]=["id"=>$k["id"],"name"=>$k["name"],"types"=>$k["types"],"cat"=>$k["dex"]["category"]??""]; }
file_put_contents("web/assets/data/kin.json",json_encode($out,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n");'
```

## Running locally

PHP's built-in server (no Apache/MAMP needed). From the repo root:

```bash
npm run site        # → http://localhost:8000
```

The **Play** link points at `/play/`, which only exists once you assemble a
release (the game isn't served by the PHP dev server). Under `npm run site` a
small dev placeholder explains this (a router, `tools/dev/site-router.php`,
intercepts `/play/`). To preview the site **and** game together exactly as on
the server:

```bash
npm run preview:release   # assembles release/ then serves it → / and /play/ both work
```

To work on the game itself, use `npm run dev` (Vite).

## Deploying to pixelk.in (WHM/cPanel via FTP)

The game uses Vite `base: './'`, so it runs from any subfolder unchanged. A
release bundle is assembled into `release/` (gitignored), which you FTP into
`public_html/`:

```
release/            ← upload the CONTENTS of this into public_html/
  index.php …       → pixelk.in/
  play/             → pixelk.in/play/
```

Pick what to ship:

```bash
npm run release         # build the game + assemble site AND game
npm run release:site    # site only — refresh the pages without rebuilding the game
npm run release:game    # rebuild the game + refresh only release/play/
```

`release:site` leaves an already-staged `release/play/` untouched, so you can
push a copy tweak without re-uploading the whole game. Then FTP the contents of
`release/` into `public_html/`.
