<?php
require __DIR__ . '/includes/config.php';
page_head(
    'About',
    'about.php',
    'Why we made PixelKin: a love letter to handheld-era creature-collecting. The feeling we\'re selling — nostalgia, collecting, exploration, delight — and why every kin, sprite, and note is original.'
);
?>

<section class="page-hero">
    <h1>Why we made PixelKin</h1>
    <p class="page-hero-sub">A love letter to handheld gaming — the kind you played hunched over a screen in the back of a car.</p>
</section>

<section class="band prose">
    <div class="prose-col">
        <h2>The feeling we're selling</h2>
        <p>
            PixelKin sells a feeling: the warm, wide-eyed wonder of being a kid
            in the late '90s, discovering a whole world one tall-grass step at a
            time. It's for the player who grew up on creature-collecting RPGs and
            now has a job, maybe kids, and not much time — but a deep, specific
            nostalgia for the era of the handheld. They don't want a slot-machine
            mobile game. They want the <em>thing they remember</em>: the quiet
            thrill of a new town, a full party of creatures they've grown attached
            to, a map that keeps unfolding.
        </p>
        <p>
            We're not chasing the hardcore completionist or the modern-AAA player.
            We're making the game our player wishes they could go back and play
            again for the first time.
        </p>

        <h2>The world that holds it</h2>
        <p>
            That feeling needed somewhere to live, so we built
            <strong>Vesperholm</strong> — a crescent of valleys around a darkened
            mountain, caught in the <strong>Long Dusk</strong> after night fell
            and wouldn't lift. You play a lamp-tender's apprentice on your
            <strong>Wayfaring</strong>, relighting the sky one constellation at a
            time. It's cosy and a little melancholy: lanterns in the dark. Even
            the antagonists — the <strong>Hollowing</strong>, who would let the
            dark stay — are sympathetic rather than cruel. We wanted a story you
            could sit with, not one that shouts.
        </p>

        <h2>A copy of nothing</h2>
        <p>
            PixelKin is <strong>inspired by</strong> the monster-collecting genre
            and is <strong>a copy of nothing</strong>. The genre's ideas — collect
            creatures, build a party, turn-based elemental battles, explore a
            region — belong to everyone. The specific expression of any one
            franchise does not, and we never borrow it. Every kin, name, sprite,
            town, item, track, and line of text is original to PixelKin. We borrow
            the warmth of the era; we take none of its assets. When in doubt, we
            make it more original, not less — so you feel the nostalgia <em>and</em>
            recognise PixelKin as its own thing.
        </p>

        <h2>The look, on purpose</h2>
        <p>
            The art is handheld-era pixel work, and it grows the way the real
            hardware did — anchored in a tight, bold palette and allowed to lean
            into a slightly richer register as the journey goes on. The internal
            resolution is fixed and small, scaled up with nearest-neighbour, so
            pixels stay crisp, square, and deliberate at any size. No smooth,
            modern, vector-y art. Ever. The music leans chiptune; the menus go
            <em>blip</em>.
        </p>
    </div>

    <aside class="lore-aside">
        <h3>What we promise ourselves</h3>
        <dl class="lore-list">
            <dt>Not</dt><dd>paywalls, energy timers, or microtransactions.</dd>
            <dt>Not</dt><dd>photorealistic, 3D, or a modern restyle of a retro idea.</dd>
            <dt>Not</dt><dd>a clone trading on another game's content or identity.</dd>
            <dt>Always</dt><dd>cosy, never cynical — charm in the small moments.</dd>
        </dl>
    </aside>
</section>

<section class="band">
    <h2 class="band-title">Four feelings, in order</h2>
    <p class="band-sub">Every decision serves these. If a feature doesn't strengthen one of them, it probably isn't PixelKin.</p>
    <div class="feature-grid">
        <article class="feature">
            <span class="feature-ico" data-ico="moon">🌙</span>
            <h3>Nostalgia</h3>
            <p>It should <em>feel</em> like turn-of-the-millennium handheld gaming — not a parody of it, a loving continuation. Chunky pixels, a tight palette, chiptune-leaning music.</p>
        </article>
        <article class="feature">
            <span class="feature-ico" data-ico="kin">🦊</span>
            <h3>Collecting</h3>
            <p>The core loop. Finding a new kin, completing a set, watching a favourite <strong>kindle</strong>. The joy is in the gathering and the attachment, not the grind.</p>
        </article>
        <article class="feature">
            <span class="feature-ico" data-ico="map">🗺️</span>
            <h3>Exploration</h3>
            <p>A world that rewards curiosity. Routes, towns, caves, and secrets behind a ledge you couldn't reach an hour ago. The map is the adventure.</p>
        </article>
        <article class="feature">
            <span class="feature-ico" data-ico="lantern">🏮</span>
            <h3>Delight</h3>
            <p>Small, frequent moments of charm — an animation, a line of dialogue, a kin's idle wiggle. Cosy, never cynical.</p>
        </article>
    </div>
</section>

<section class="band">
    <h2 class="band-title">Wander a little deeper</h2>
    <p class="band-sub">Everything above lives in the game. Here's where to read more.</p>
    <div class="feature-grid">
        <a class="feature" href="story.php">
            <span class="feature-ico" data-ico="moon">🌙</span>
            <h3>The World →</h3>
            <p>Vesperholm, the Long Dusk, the Hollowing, and the words of the world — the story you step into.</p>
        </a>
        <a class="feature" href="creatures.php">
            <span class="feature-ico" data-ico="kin">🦊</span>
            <h3>The Kin →</h3>
            <p>Over 150 original creatures across ten elements. Meet the founding trio and browse the first fifty.</p>
        </a>
        <a class="feature" href="faq.php">
            <span class="feature-ico" data-ico="map">🗺️</span>
            <h3>FAQ →</h3>
            <p>How it plays, what it costs, where it runs, and what's coming — the practical questions answered.</p>
        </a>
        <a class="feature" href="license.php">
            <span class="feature-ico" data-ico="lantern">🏮</span>
            <h3>Licensing →</h3>
            <p>Built by <?= e(STUDIO_NAME) ?>. Talk to us about licensing the game, the engine, or the studio's work.</p>
        </a>
    </div>
</section>

<section class="band cta-band">
    <div class="cta-inner">
        <h2>Come see what we mean.</h2>
        <a class="btn btn-primary btn-lg" href="<?= e(GAME_URL) ?>">Play in your browser</a>
    </div>
</section>

<?php page_foot(); ?>
