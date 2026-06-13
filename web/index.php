<?php
require __DIR__ . '/includes/config.php';
page_head(
    'Home',
    'index.php',
    'PixelKin is a retro, handheld-era creature-collecting adventure, free to play in your browser. Relight the constellations of Vesperholm, collect over 150 original kin, and wander fourteen lamplit valleys.'
);
?>

<section class="hero" id="hero">
    <div class="hero-parallax" aria-hidden="true">
        <div class="plx plx-scene" data-depth="10"></div>
        <div class="hero-vignette"></div>
    </div>
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="hero-inner">
        <img src="assets/img/logo-hero.webp" alt="<?= e(SITE_NAME) ?>" class="hero-logo" width="1448" height="1086">
        <p class="hero-tagline"><?= e(SITE_TAGLINE) ?></p>
        <p class="hero-lede">
            <strong>PixelKin</strong> is a cosy, retro creature-collecting RPG —
            free to play in your browser. Explore a world where night fell and never
            lifted — catch, raise and battle over 150 original creatures, and
            relight the stars one by one. You play a young lamp-keeper, setting
            out to bring the daylight back.
        </p>
        <div class="hero-actions">
            <a class="btn btn-primary" href="<?= e(GAME_URL) ?>">Play in your browser</a>
            <a class="btn btn-ghost" href="story.php">Enter the Long Dusk</a>
        </div>
        <p class="hero-note">No install · plays on desktop &amp; mobile · free to play</p>
    </div>
</section>

<section class="band features">
    <h2 class="band-title">How PixelKin plays</h2>
    <p class="band-sub">New to creature-collecting games? Here's the gist.</p>
    <div class="feature-grid">
        <article class="feature">
            <span class="feature-ico" data-ico="kin">🦊</span>
            <h3>Catch &amp; raise creatures</h3>
            <p>Befriend, train and evolve over 150 original creatures — the game calls them <strong>kin</strong> — across ten elemental types. Every one is an original design: a copy of nothing.</p>
        </article>
        <article class="feature">
            <span class="feature-ico" data-ico="lantern">🏮</span>
            <h3>Battle for badges of light</h3>
            <p>Take on each region's champion in a turn-based battle. Win, and you earn a <strong>Gleam</strong> — your badge of progress, and a constellation that lights back up in the real night sky.</p>
        </article>
        <article class="feature">
            <span class="feature-ico" data-ico="map">🗺️</span>
            <h3>Explore fourteen regions</h3>
            <p>Coast roads, deep caves, festival towns. New traversal powers (the game's <strong>Lantern Gifts</strong>) open fresh paths as you go.</p>
        </article>
        <article class="feature">
            <span class="feature-ico" data-ico="moon">🌙</span>
            <h3>A cosy, story-driven world</h3>
            <p>A gentle, melancholy tale. Even the folk who'd let the dark stay — the <strong>Hollowing</strong> — aren't villains, just tired. The story is yours to turn.</p>
        </article>
    </div>
</section>

<section class="band storybook" id="storybook" aria-label="The story of PixelKin">
    <h2 class="band-title">Turn the page</h2>
    <p class="band-sub">A little of the tale that waits in the dark. Turn the page when you're ready.</p>

    <div class="book" id="book" tabindex="0" role="group" aria-roledescription="storybook" aria-label="The Long Dusk — a short tale">
        <div class="book-inner">
            <article class="book-page book-page--cover" data-page>
                <div class="page-content">
                    <span class="page-eyebrow">Vesperholm</span>
                    <h3 class="page-title">The Long&nbsp;Dusk</h3>
                    <p class="page-flourish">— a tale of lanterns in the dark —</p>
                </div>
            </article>

            <article class="book-page" data-page>
                <div class="page-content">
                    <p class="page-drop">Once, the stars kept the world's clock.</p>
                    <p>Then, one evening, night fell over the valleys of Vesperholm — and simply forgot to lift.</p>
                </div>
            </article>

            <article class="book-page" data-page>
                <div class="page-content">
                    <p>The lamps still burn in the windows. The gardens still grow. But the sky has stopped turning, and the long, settled dark has crept into everything.</p>
                    <p>This is the <em>Long Dusk</em>.</p>
                </div>
            </article>

            <article class="book-page" data-page>
                <div class="page-content">
                    <p>You are a lamp-tender's apprentice. Today you take up your <em>vesperlamp</em> and begin your <em>Wayfaring</em> —</p>
                    <p>the old rite of walking out into the dusk to do something quietly enormous.</p>
                </div>
            </article>

            <article class="book-page" data-page>
                <div class="page-content">
                    <p>You won't go alone. The <em>kin</em> walk the dark beside you — creatures of ember and tide, frost and storm.</p>
                    <p>Befriend them with your lamp, and they will light the way.</p>
                </div>
            </article>

            <article class="book-page" data-page>
                <div class="page-content">
                    <p>One valley at a time, you'll relight the constellations.</p>
                    <p>Every <em>Gleam</em> you earn blooms back into the night sky — for real, and for good.</p>
                </div>
            </article>

            <article class="book-page book-page--end" data-page>
                <div class="page-content">
                    <span class="page-ellipsis" aria-hidden="true">…</span>
                    <p class="page-flourish">The lamp is lit. The road is dark.<br>The rest is yours to write.</p>
                    <a class="btn btn-primary btn-lg" href="<?= e(GAME_URL) ?>">Begin your Wayfaring</a>
                </div>
            </article>
        </div>

        <button class="book-nav book-prev" type="button" aria-label="Previous page" hidden>‹</button>
        <button class="book-nav book-next" type="button" aria-label="Next page">›</button>
        <div class="book-curl" aria-hidden="true"></div>
    </div>

    <div class="book-dots" id="bookDots" role="tablist" aria-label="Story pages"></div>
    <p class="book-hint">Tap the page, swipe, or use the arrow keys.</p>
</section>

<section class="band world">
    <h2 class="band-title">Wander fourteen lamplit valleys</h2>
    <p class="band-sub">From the harbour town where you start to the spire at the world's heart — a glimpse of Vesperholm in the Long Dusk.</p>
    <div class="gallery">
        <?php foreach (WORLD_GALLERY as $w): ?>
            <figure class="shot" tabindex="0" role="button"
                    data-lb data-lb-group="world"
                    data-lb-img="assets/img/world/<?= e($w['img']) ?>.webp"
                    data-lb-title="<?= e($w['name']) ?>"
                    data-lb-blurb="<?= e($w['blurb']) ?>">
                <img src="assets/img/world/<?= e($w['img']) ?>.webp" alt="<?= e($w['name']) ?>" loading="lazy">
                <figcaption>
                    <span class="shot-name"><?= e($w['name']) ?></span>
                    <span class="shot-blurb"><?= e($w['blurb']) ?></span>
                </figcaption>
                <span class="shot-zoom" aria-hidden="true">⤢</span>
            </figure>
        <?php endforeach; ?>
    </div>
    <p class="gallery-note">Tap a valley to explore. Concept art — the look the game's pixel maps are built toward.</p>
</section>

<section class="band starters">
    <h2 class="band-title">Choose your first companion</h2>
    <p class="band-sub">Like every adventure in the genre, you'll start by picking one of three creatures. Choose the one whose light you'll carry.</p>
    <div class="kin-row">
        <?php foreach (STARTERS as $k): ?>
            <article class="kin-card" style="--tint: <?= e($k['tint']) ?>">
                <div class="kin-art">
                    <img src="assets/img/kin/<?= e($k['img']) ?>_front.webp" alt="<?= e($k['name']) ?>" loading="lazy">
                </div>
                <h3 class="kin-name"><?= e($k['name']) ?></h3>
                <span class="type-chip"><?= e($k['type']) ?></span>
                <p class="kin-blurb"><?= e($k['blurb']) ?></p>
            </article>
        <?php endforeach; ?>
    </div>
    <div class="band-actions">
        <a class="btn btn-ghost" href="creatures.php">Meet more kin</a>
    </div>
</section>

<section class="band explore">
    <h2 class="band-title">More to explore</h2>
    <p class="band-sub">Just passing through the homepage? Here's the rest of Vesperholm's lamplight.</p>
    <div class="explore-grid">
        <?php foreach (EXPLORE as $x): ?>
            <a class="explore-card" href="<?= e($x['href']) ?>">
                <span class="explore-ico" aria-hidden="true"><?= $x['ico'] ?></span>
                <span class="explore-head">
                    <span class="explore-label"><?= e($x['label']) ?></span>
                    <span class="explore-arrow" aria-hidden="true">›</span>
                </span>
                <span class="explore-blurb"><?= e($x['blurb']) ?></span>
            </a>
        <?php endforeach; ?>
    </div>
</section>

<section class="band cta-band">
    <div class="cta-inner">
        <h2>The lamp is lit. The road is dark.</h2>
        <p>Take your first step into Vesperholm — right now, in your browser.</p>
        <a class="btn btn-primary btn-lg" href="<?= e(GAME_URL) ?>">Begin your Wayfaring</a>
    </div>
</section>

<?php page_foot(); ?>
