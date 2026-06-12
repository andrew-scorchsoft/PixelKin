<?php
/** Shared <head> + masthead. Set via page_head(): $GLOBALS __title / __page / __desc. */
$title = $GLOBALS['__title'] ?? SITE_NAME;
$page  = $GLOBALS['__page']  ?? 'index.php';
$desc  = $GLOBALS['__desc']  ?? SITE_DESC;
$ogTitle = $title === 'Home'
    ? SITE_NAME . ' — ' . SITE_TAGLINE
    : $title . ' · ' . SITE_NAME;
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#0b1026">
    <title><?= e($ogTitle) ?></title>
    <meta name="description" content="<?= e($desc) ?>">
    <meta name="author" content="<?= e(STUDIO_NAME) ?>">
    <link rel="canonical" href="<?= e($page === 'index.php' ? './' : $page) ?>">
    <meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
    <meta property="og:title" content="<?= e($ogTitle) ?>">
    <meta property="og:description" content="<?= e($desc) ?>">
    <meta property="og:type" content="website">
    <meta property="og:image" content="assets/img/logo.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="<?= e($ogTitle) ?>">
    <meta name="twitter:description" content="<?= e($desc) ?>">
    <meta name="twitter:image" content="assets/img/logo.png">
    <link rel="icon" type="image/png" href="assets/img/logo.png">
    <link rel="preload" href="assets/fonts/PressStart2P-Regular.ttf" as="font" type="font/ttf" crossorigin>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="starfield" aria-hidden="true"></div>

    <header class="masthead">
        <a class="brand" href="index.php" aria-label="<?= e(SITE_NAME) ?> home">
            <img src="assets/img/logo-text.webp" alt="<?= e(SITE_NAME) ?>" class="brand-logo">
        </a>
        <button class="nav-toggle" aria-label="Menu" aria-expanded="false">
            <span></span><span></span><span></span>
        </button>
        <nav class="nav">
            <?php foreach (NAV as $label => $href): ?>
                <a href="<?= e($href) ?>"<?= $href === $page ? ' class="active"' : '' ?>><?= e($label) ?></a>
            <?php endforeach; ?>
            <a class="nav-cta" href="<?= e(GAME_URL) ?>">Play</a>
        </nav>
    </header>

    <main>
