<?php
require __DIR__ . '/includes/config.php';
page_head(
    'The World',
    'story.php',
    'The story of PixelKin: night fell over Vesperholm and won\'t lift. Play a lamp-tender\'s apprentice relighting the sky, befriend the kin, and meet the Hollowing — a cult that would let the dark stay.'
);
?>

<section class="page-hero">
    <h1>The Long Dusk</h1>
    <p class="page-hero-sub">Night fell over Vesperholm and won't lift. Someone has to carry a light.</p>
</section>

<section class="band prose">
    <div class="prose-col">
        <h2>A crescent of valleys, one darkened mountain</h2>
        <p>
            <strong>Vesperholm</strong> is a crescent of valleys curled around a
            central peak that has gone black and cold. The stars that once kept
            the region's clock have guttered out, and a long, settled twilight —
            the <strong>Long Dusk</strong> — has taken their place. Lamps still
            burn in the windows. People still tend their gardens. But the sky has
            stopped turning, and everyone feels it.
        </p>

        <h2>You are a lamp-tender's apprentice</h2>
        <p>
            You begin your <strong>Wayfaring</strong> — the rite of leaving home
            with a <strong>vesperlamp</strong> in hand. Your task is quietly
            enormous: relight the sky, one constellation at a time. Each valley's
            <strong>Lampwarden</strong> guards a <strong>Lumenary</strong>, and
            besting one earns a <strong>Gleam</strong> — a constellation reborn,
            visible overhead for the rest of your journey.
        </p>

        <h2>The kin walk the dark beside you</h2>
        <p>
            You won't go alone. The valleys are full of <strong>kin</strong> —
            creatures of ten elements, from ember-foxes to tide-hums to clover
            sprites. Befriend them with your lamp, raise them, and watch them
            <strong>kindle</strong> into stronger forms. When they're not at your
            side they rest at <strong>the Hearth</strong>, a warm keep tended by
            the Hearthkeeper.
        </p>

        <h2>The Hollowing aren't villains</h2>
        <p>
            Not everyone wants the light back. The <strong>Hollowing</strong>,
            led by the weary <strong>Warden Còr</strong>, believe a gentle,
            permanent dark would be kinder — quieter, safer, free of the old
            burning urgency. They never raise a hand to harm. They simply ask you
            to stop. Whether the sky should turn again is, in the end, a question
            the game lets you sit with.
        </p>
    </div>

    <aside class="lore-aside">
        <h3>The words of Vesperholm</h3>
        <dl class="lore-list">
            <dt>Kin</dt><dd>The creatures you befriend and raise.</dd>
            <dt>Gleam</dt><dd>A relit constellation — earned from a Lampwarden, visible in the sky.</dd>
            <dt>Lumenary</dt><dd>A warden's hall — the genre's "gym," reimagined.</dd>
            <dt>Lantern Gift</dt><dd>A field power that opens new roads as you travel.</dd>
            <dt>Kindling</dt><dd>How a kin grows into its next form.</dd>
            <dt>The Hearth</dt><dd>The warm keep where kin rest when not in your lamp.</dd>
            <dt>Vesperlamp</dt><dd>Your lamp — light, map, and catching device in one.</dd>
        </dl>
    </aside>
</section>

<section class="band lumenaries">
    <h2 class="band-title">Eight Lumenaries, eight Gleams</h2>
    <p class="band-sub">Each valley keeps a Lumenary — a warden's hall built around one constellation element. Best its Lampwarden and a Gleam blooms back into the sky.</p>
    <div class="lumen-grid">
        <?php foreach (LUMENARIES as $l): ?>
            <figure class="lumen" style="--tint: <?= e($l['tint']) ?>" tabindex="0" role="button"
                    data-lb data-lb-group="lumen"
                    data-lb-img="assets/img/lumenary/<?= e($l['img']) ?>.webp"
                    data-lb-title="<?= e($l['type']) ?> Lumenary"
                    data-lb-blurb="The <?= e($l['type']) ?> warden's hall — best its Lampwarden to earn the <?= e($l['type']) ?> Gleam."
                    data-lb-chips="<?= e($l['type'] . ',' . $l['tint']) ?>">
                <img src="assets/img/lumenary/<?= e($l['img']) ?>.webp" alt="<?= e($l['type']) ?> Lumenary" loading="lazy">
                <figcaption class="type-chip"><?= e($l['type']) ?></figcaption>
                <span class="shot-zoom" aria-hidden="true">⤢</span>
            </figure>
        <?php endforeach; ?>
    </div>
    <p class="gallery-note">Tap a hall to look closer.</p>
</section>

<section class="band cta-band">
    <div class="cta-inner">
        <h2>Ready to relight the sky?</h2>
        <a class="btn btn-primary btn-lg" href="<?= e(GAME_URL) ?>">Play in your browser</a>
    </div>
</section>

<?php page_foot(); ?>
