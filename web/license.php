<?php
require __DIR__ . '/includes/config.php';
page_head(
    'Licensing',
    'license.php',
    'Interested in licensing PixelKin, its world, characters, music or artwork? PixelKin is created and owned by Scorchsoft — get in touch through the Scorchsoft contact form to discuss licensing and partnerships.'
);
?>

<section class="page-hero">
    <h1>Licensing &amp; partnerships</h1>
    <p class="page-hero-sub">
        PixelKin — its world, characters, story, artwork and music — is an
        original creation, designed and built by <?= e(STUDIO_NAME) ?>.
    </p>
</section>

<section class="band prose prose-center">
    <div class="prose-col">
        <h2>Want to license PixelKin?</h2>
        <p>
            If you'd like to license PixelKin — the game, the brand, individual
            kin, the soundtrack, or the artwork — or you're interested in a
            collaboration, publishing, merchandise, or any other partnership,
            we'd love to hear from you. Every part of PixelKin is owned by
            <?= e(STUDIO_NAME) ?>, so licensing runs through us directly.
        </p>
        <p>
            The quickest way to start a conversation is the <?= e(STUDIO_NAME) ?>
            contact form. Tell us a little about what you have in mind and we'll
            get back to you.
        </p>
        <div class="band-actions">
            <a class="btn btn-primary btn-lg" href="<?= e(STUDIO_CONTACT) ?>" target="_blank" rel="noopener">
                Contact <?= e(STUDIO_NAME) ?>
            </a>
        </div>
        <p class="muted-note">
            Opens <a href="<?= e(STUDIO_CONTACT) ?>" target="_blank" rel="noopener"><?= e(parse_url(STUDIO_CONTACT, PHP_URL_HOST) . parse_url(STUDIO_CONTACT, PHP_URL_PATH)) ?></a>
        </p>
    </div>
</section>

<section class="band prose prose-center">
    <div class="prose-col">
        <h2>About <?= e(STUDIO_NAME) ?></h2>
        <p>
            <?= e(STUDIO_NAME) ?> is a UK app, web and game development studio.
            PixelKin is one of our original titles — built the same way we build
            for clients: web-first, made to port cleanly to mobile.
            <a href="<?= e(STUDIO_URL) ?>" target="_blank" rel="noopener">Visit scorchsoft.com</a>
            to see more of our work.
        </p>
        <p class="copyright-note">
            PixelKin is inspired by the creature-collecting genre and is a copy of
            nothing: every creature, name, sprite, track and line of text is original.
            All rights reserved © <?= date('Y') ?> <?= e(STUDIO_NAME) ?>.
        </p>
    </div>
</section>

<?php page_foot(); ?>
