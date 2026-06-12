<?php
require __DIR__ . '/includes/config.php';
page_head(
    'Privacy Policy',
    'privacy.php',
    'How PixelKin and Scorchsoft handle your data. The PixelKin website is informational and the game stores your progress locally in your own browser — we do not collect personal information through it.'
);
$updated = 'June 2026';
?>

<section class="page-hero">
    <h1>Privacy Policy</h1>
    <p class="page-hero-sub">Last updated: <?= e($updated) ?></p>
</section>

<section class="band prose prose-center">
    <div class="prose-col legal">
        <p>
            This policy explains how <?= e(STUDIO_NAME) ?> ("we", "us") handles
            information in connection with the <?= e(SITE_NAME) ?> website and game
            (together, "<?= e(SITE_NAME) ?>"). We've tried to keep it short and plain.
        </p>

        <h2>The short version</h2>
        <p>
            <?= e(SITE_NAME) ?> is an informational website and a game that runs
            entirely in your browser. We do <strong>not</strong> ask you to create
            an account, and we do <strong>not</strong> collect personal information
            through the site or the game.
        </p>

        <h2>Your game progress stays on your device</h2>
        <p>
            When you play, your save data (your progress, party and settings) is
            stored <strong>locally in your own browser</strong> on your device. It
            is not transmitted to us and we cannot see it. Clearing your browser
            storage, switching devices or browsers, or certain game updates may
            remove or reset that data — please don't rely on it as permanent storage.
        </p>

        <h2>Server logs</h2>
        <p>
            Like most websites, our hosting provider may automatically record
            standard technical information (such as your IP address, browser type
            and the pages requested) in server logs. This is used only to operate
            and secure the site, and is not used to identify you.
        </p>

        <h2>Cookies &amp; tracking</h2>
        <p>
            The <?= e(SITE_NAME) ?> website does not set advertising or
            cross-site tracking cookies. The game may use your browser's local
            storage to keep your save and settings, as described above — this is
            functional, not tracking, and never leaves your device.
        </p>

        <h2>Links to other sites</h2>
        <p>
            Some pages link to <?= e(STUDIO_NAME) ?> (scorchsoft.com), including a
            contact form for enquiries. Those pages have their own privacy
            practices; this policy covers only <?= e(SITE_NAME) ?>. If you contact
            us through the <?= e(STUDIO_NAME) ?> form, the details you submit are
            handled under Scorchsoft's own policy.
        </p>

        <h2>Children</h2>
        <p>
            <?= e(SITE_NAME) ?> is family-friendly and does not knowingly collect
            personal information from anyone, including children.
        </p>

        <h2>Changes</h2>
        <p>
            We may update this policy from time to time. The "last updated" date
            above shows when it last changed. Continued use of <?= e(SITE_NAME) ?>
            after a change means you accept the updated policy.
        </p>

        <h2>Contact</h2>
        <p>
            Questions about privacy? Reach us through the
            <a href="<?= e(STUDIO_CONTACT) ?>" target="_blank" rel="noopener"><?= e(STUDIO_NAME) ?> contact form</a>.
        </p>

        <p class="copyright-note">
            This policy is provided for general information and is not legal advice.
        </p>
    </div>
</section>

<?php page_foot(); ?>
