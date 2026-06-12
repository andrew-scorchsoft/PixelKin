<?php
/**
 * Dev-only router for the PHP built-in server (`npm run site`).
 *
 * The marketing site lives in web/; the playable game is a SEPARATE build that
 * only lands at /play/ after `npm run release` assembles it. Under the bare dev
 * server there is no /play/, and PHP's built-in server would otherwise fall back
 * to serving the root index.php for that path — which then renders unstyled
 * (its relative asset links resolve against /play/ and 404). This router
 * intercepts /play/ and shows a small, on-brand "not built here" placeholder
 * instead, so clicking Play during local dev is informative rather than broken.
 *
 * It does NOT live in web/, so it never gets copied into a release.
 * Usage (see package.json "site"): php -S localhost:8000 -t web tools/dev/site-router.php
 */

$uri = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';

// Anything under /play/ → dev placeholder (the real game replaces this on release).
if (preg_match('#^/play(/|$)#', $uri)) {
    header('Content-Type: text/html; charset=utf-8');
    ?>
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Play · PixelKin (dev)</title>
<style>
  body{margin:0;min-height:100vh;display:grid;place-items:center;text-align:center;
    font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
    color:#f5f0e1;background:radial-gradient(1000px 500px at 50% -10%,rgba(159,231,255,.12),transparent 60%),linear-gradient(180deg,#0b1026,#0a0d1f);padding:2rem;}
  .card{max-width:560px;background:rgba(19,32,90,.5);border:1px solid rgba(159,231,255,.22);
    border-radius:14px;padding:2.5rem;box-shadow:0 8px 28px rgba(0,0,0,.45);}
  h1{color:#9fe7ff;font-size:1.4rem;margin:0 0 1rem;}
  code{background:rgba(0,0,0,.35);padding:.15rem .45rem;border-radius:5px;color:#ffd76b;font-size:.95em;}
  p{line-height:1.6;color:#d8d2e8;margin:0 0 1rem;}
  a{color:#9fe7ff;}
  .tag{font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:#ff8a3d;margin-bottom:1rem;}
</style></head>
<body><div class="card">
  <div class="tag">Local dev · /play/</div>
  <h1>The game isn't built here yet</h1>
  <p><code>npm run site</code> serves only the marketing site (<code>web/</code>).
     The playable game is a separate build that lands at <code>/play/</code> when you assemble a release.</p>
  <p>To preview the site <em>and</em> the game together, exactly as they'll sit on the server:</p>
  <p><code>npm run release</code> &nbsp;then&nbsp; <code>php -S localhost:8000 -t release</code></p>
  <p>Or just iterate on the game itself with <code>npm run dev</code>.</p>
  <p><a href="/">← Back to the site</a></p>
</div></body></html>
    <?php
    exit;
}

// Everything else: let the built-in server serve the static file or run the .php page.
return false;
