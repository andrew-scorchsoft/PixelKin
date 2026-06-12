<?php
require __DIR__ . '/includes/config.php';
page_head(
    'Terms of Use',
    'terms.php',
    'The terms for using PixelKin. The game and website are provided free, "as is", with no warranties. Scorchsoft owns all rights and may change, suspend or withdraw the game at any time.'
);
$updated = 'June 2026';
?>

<section class="page-hero">
    <h1>Terms of Use</h1>
    <p class="page-hero-sub">Last updated: <?= e($updated) ?></p>
</section>

<section class="band prose prose-center">
    <div class="prose-col legal">
        <p>
            These terms govern your use of the <?= e(SITE_NAME) ?> website and game
            (together, "<?= e(SITE_NAME) ?>"), provided by <?= e(STUDIO_NAME) ?>
            ("we", "us"). By using <?= e(SITE_NAME) ?>, you agree to these terms. If
            you don't agree, please don't use it.
        </p>

        <h2>1. Free to play, for personal enjoyment</h2>
        <p>
            We make <?= e(SITE_NAME) ?> available free of charge for your personal,
            non-commercial enjoyment. You may play it and share links to it. You may
            not sell access to it, or pass it off as your own.
        </p>

        <h2>2. We own it</h2>
        <p>
            <?= e(SITE_NAME) ?> — including its name, world, characters, story,
            artwork, music, code and all other content — is the original work of
            <?= e(STUDIO_NAME) ?> and is protected by copyright and other rights.
            All rights are reserved. You may not copy, reproduce, distribute,
            modify, reverse-engineer, or create derivative works from any part of it
            except as expressly allowed by these terms or by law. To licence any
            part of <?= e(SITE_NAME) ?>, see our
            <a href="license.php">Licensing</a> page.
        </p>

        <h2>3. Provided "as is" — no warranties</h2>
        <p>
            <?= e(SITE_NAME) ?> is provided <strong>"as is" and "as available",
            without warranties of any kind</strong>, whether express or implied,
            including any implied warranties of merchantability, fitness for a
            particular purpose, or non-infringement. We do not warrant that
            <?= e(SITE_NAME) ?> will be uninterrupted, error-free, secure, or free of
            bugs, or that any defects will be fixed. You use it at your own risk.
        </p>

        <h2>4. We may change or withdraw it at any time</h2>
        <p>
            <?= e(SITE_NAME) ?> is offered on an ongoing, discretionary basis. We
            reserve the right, at any time and without notice or liability, to
            modify, update, suspend, restrict, or <strong>permanently take
            <?= e(SITE_NAME) ?> offline</strong>, in whole or in part. We are under
            no obligation to keep it available, to preserve any content, or to
            maintain your saved progress.
        </p>

        <h2>5. Your saved progress</h2>
        <p>
            Game progress is stored locally in your browser and is your
            responsibility. It may be lost through browser settings, device changes,
            or updates to the game. We are not responsible for any lost progress.
        </p>

        <h2>6. Limitation of liability</h2>
        <p>
            To the fullest extent permitted by law, <?= e(STUDIO_NAME) ?> will not be
            liable for any indirect, incidental, special, consequential or punitive
            damages, or for any loss of data, profits, goodwill or progress, arising
            out of or relating to your use of (or inability to use) <?= e(SITE_NAME) ?>.
            Nothing in these terms excludes any liability that cannot be excluded by law.
        </p>

        <h2>7. Acceptable use</h2>
        <p>
            Don't misuse <?= e(SITE_NAME) ?>: for example, don't attempt to disrupt
            it, gain unauthorised access to it, use it unlawfully, or interfere with
            anyone else's use of it.
        </p>

        <h2>8. Changes to these terms</h2>
        <p>
            We may update these terms from time to time. The "last updated" date
            above shows when they last changed. Continued use after a change means
            you accept the updated terms.
        </p>

        <h2>9. Governing law</h2>
        <p>
            These terms are governed by the laws of England and Wales, and the
            courts of England and Wales have exclusive jurisdiction, except where
            local law gives you other rights that cannot be overridden.
        </p>

        <h2>Contact</h2>
        <p>
            Questions about these terms? Reach us through the
            <a href="<?= e(STUDIO_CONTACT) ?>" target="_blank" rel="noopener"><?= e(STUDIO_NAME) ?> contact form</a>.
        </p>

        <p class="copyright-note">
            These terms are provided for general information and are not legal advice.
        </p>
    </div>
</section>

<?php page_foot(); ?>
