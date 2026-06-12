<?php
require __DIR__ . '/includes/config.php';
page_head(
    'Kin',
    'creatures.php',
    'Meet the kin of PixelKin — over 150 original creatures across ten elements, from the ember-fox Vulpyre to the tide-hum Brinix and the lucky Cloverkit. An empirically balanced roster, a copy of nothing.'
);
?>

<section class="page-hero">
    <h1>The Kin of Vesperholm</h1>
    <p class="page-hero-sub">
        Over a hundred and fifty original creatures across ten elements —
        Ember, Tide, Verdant, Stone, Storm, Frost, Solar, Lunar, Light and Dark.
        Here are the three you'll meet first.
    </p>
</section>

<section class="band starters">
    <div class="kin-row kin-row-lg">
        <?php foreach (STARTERS as $k): ?>
            <article class="kin-card kin-card-lg" style="--tint: <?= e($k['tint']) ?>">
                <div class="kin-art">
                    <img src="assets/img/kin/<?= e($k['img']) ?>_front.webp" alt="<?= e($k['name']) ?>" loading="lazy">
                </div>
                <h3 class="kin-name"><?= e($k['name']) ?></h3>
                <span class="type-chip"><?= e($k['type']) ?></span>
                <p class="kin-cat"><?= e($k['cat']) ?></p>
                <p class="kin-blurb"><?= e($k['blurb']) ?></p>
            </article>
        <?php endforeach; ?>
    </div>
</section>

<section class="band kindex">
    <h2 class="band-title">The first fifty</h2>
    <p class="band-sub">
        A field guide to the kin you'll meet across the southern valleys.
        Tap any to look closer — the rest of the <strong>162</strong> you'll have
        to find for yourself, out in the dark.
    </p>
    <div class="kin-grid">
        <?php foreach (load_kin() as $k):
            $id3 = str_pad((string)$k['id'], 3, '0', STR_PAD_LEFT);
            $lead = type_color($k['types'][0]);
            $chips = implode(';', array_map(fn($t) => $t . ',' . type_color($t), $k['types']));
        ?>
            <figure class="kin-cell" style="--tint: <?= e($lead) ?>" tabindex="0" role="button"
                    data-lb data-lb-group="kin" data-lb-pixel="1"
                    data-lb-img="assets/img/kin/battle/<?= e($id3) ?>.webp"
                    data-lb-title="#<?= e($id3) ?> · <?= e($k['name']) ?>"
                    data-lb-blurb="<?= e($k['cat']) ?>"
                    data-lb-chips="<?= e($chips) ?>">
                <img src="assets/img/kin/icons/<?= e($id3) ?>.webp" alt="<?= e($k['name']) ?>" loading="lazy">
                <figcaption><?= e($k['name']) ?></figcaption>
                <span class="kin-no">#<?= e($id3) ?></span>
            </figure>
        <?php endforeach; ?>
        <div class="kin-cell kin-locked" aria-hidden="true">
            <span class="lock-glyph">?</span>
            <figcaption>…and 112 more</figcaption>
        </div>
    </div>
    <div class="band-actions">
        <a class="btn btn-primary" href="<?= e(GAME_URL) ?>">Find the rest in-game</a>
    </div>
</section>

<section class="band prose prose-center">
    <div class="prose-col">
        <h2>Ten elements, two mirror axes</h2>
        <p>
            Every kin belongs to one or two of ten types. Eight are the
            constellation elements; two more — <strong>Light</strong> and
            <strong>Dark</strong> — sit opposite each other, as do
            <strong>Solar</strong> and <strong>Lunar</strong>. The roster is
            <em>empirically balanced</em>: a Monte-Carlo simulation keeps every
            type within a whisker of a fair fight, so your favourites are always
            viable.
        </p>
        <div class="type-legend">
            <?php
            $types = [
                'Ember'=>'#ff8a3d','Tide'=>'#4fb4ff','Verdant'=>'#7bdc6b','Stone'=>'#c9a86a',
                'Storm'=>'#b9a6ff','Frost'=>'#a9e8ff','Solar'=>'#ffd76b','Lunar'=>'#8aa0ff',
                'Light'=>'#fff3c0','Dark'=>'#6b6480',
            ];
            foreach ($types as $name => $tint): ?>
                <span class="type-chip" style="--tint: <?= e($tint) ?>"><?= e($name) ?></span>
            <?php endforeach; ?>
        </div>

        <h3 class="axes-subhead">The two mirror axes</h3>
        <p>
            Most matchups run one way — water beats fire, and so on. But two pairs
            of the sky elements strike each other <strong>super-effectively both
            ways</strong>. These <em>mirror axes</em> make for fast, knife-edge
            battles, so the game saves them for rare, late and legendary kin.
        </p>
        <div class="mirror-axes mirror-axes-center">
            <div class="axis-card">
                <span class="type-chip" style="--tint: <?= e(type_color('Solar')) ?>">Solar</span>
                <span class="axis-arrow" aria-label="each hits the other for double damage">⇄ <small>×2</small></span>
                <span class="type-chip" style="--tint: <?= e(type_color('Lunar')) ?>">Lunar</span>
                <p class="axis-note">Day against night.</p>
            </div>
            <div class="axis-card">
                <span class="type-chip" style="--tint: <?= e(type_color('Light')) ?>">Light</span>
                <span class="axis-arrow" aria-label="each hits the other for double damage">⇄ <small>×2</small></span>
                <span class="type-chip" style="--tint: <?= e(type_color('Dark')) ?>">Dark</span>
                <p class="axis-note">Radiance against the null — the endgame.</p>
            </div>
        </div>
    </div>
</section>

<section class="band matchups">
    <h2 class="band-title">What beats what</h2>
    <p class="band-sub">
        Every element's strengths and weaknesses at a glance. In battle the game
        multiplies your damage by the matchup — and for a two-type kin it
        multiplies <em>both</em> ways, so the right move can hit for ×4 (or fizzle
        to nothing).
    </p>

    <ul class="matchup-key" aria-label="What the rows mean">
        <li><span class="key-dot key-strong"></span> <strong>Strong vs</strong> — deals double (×2)</li>
        <li><span class="key-dot key-weak"></span> <strong>Weak to</strong> — takes double (×2)</li>
        <li><span class="key-dot key-resist"></span> <strong>Resists</strong> — takes half (×½)</li>
        <li><span class="key-dot key-immune"></span> <strong>Immune</strong> — takes nothing (×0)</li>
    </ul>

    <div class="matchup-grid">
        <?php foreach (TYPE_ORDER as $t): $p = type_profile($t); ?>
            <article class="mtype-card" style="--tint: <?= e(type_color($t)) ?>">
                <h3 class="mtype-head"><?= type_chip($t) ?></h3>
                <dl class="mtype-rows">
                    <div class="mtype-row mtype-strong">
                        <dt>Strong vs</dt>
                        <dd><?= type_chips($p['strong']) ?></dd>
                    </div>
                    <div class="mtype-row mtype-weak">
                        <dt>Weak to</dt>
                        <dd><?= type_chips($p['weak']) ?></dd>
                    </div>
                    <div class="mtype-row mtype-resist">
                        <dt>Resists</dt>
                        <dd><?= type_chips($p['resists']) ?></dd>
                    </div>
                    <?php if ($p['immune']): ?>
                        <div class="mtype-row mtype-immune">
                            <dt>Immune to</dt>
                            <dd><?= type_chips($p['immune']) ?></dd>
                        </div>
                    <?php endif; ?>
                </dl>
                <?php if ($p['noEffect']): ?>
                    <p class="mtype-note">Can't damage <?= e(implode(', ', $p['noEffect'])) ?>.</p>
                <?php endif; ?>
            </article>
        <?php endforeach; ?>
    </div>

    <p class="axes-more">
        Want the maths? The <a href="faq.php">FAQ</a> breaks down how the ×2 / ×½
        multipliers stack for double-typed kin.
    </p>
</section>

<section class="band cta-band">
    <div class="cta-inner">
        <h2>Find the rest in the dark</h2>
        <p>The full dex fills in as you wander. Go and meet them.</p>
        <a class="btn btn-primary btn-lg" href="<?= e(GAME_URL) ?>">Start collecting</a>
    </div>
</section>

<?php page_foot(); ?>
