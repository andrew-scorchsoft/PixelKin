<?php
require __DIR__ . '/includes/config.php';
page_head(
    'FAQ',
    'faq.php',
    'Answers to common questions about playing PixelKin — how to start, the controls, saving your progress, catching and raising kin, and what makes this original creature-collecting adventure tick.'
);
?>

<section class="page-hero">
    <h1>Questions &amp; Answers</h1>
    <p class="page-hero-sub">Everything you need to know before — and during — your Wayfaring.</p>
</section>

<section class="band faq">
    <h2 class="band-title">Getting started</h2>
    <div class="faq-list">
        <details class="faq-item">
            <summary>Is PixelKin free to play?</summary>
            <div class="faq-body">
                <p>
                    Yes. <?= e(SITE_NAME) ?> plays free in your browser — no purchase,
                    no subscription, no ads. Just open it and start your Wayfaring.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Do I need to download or install anything?</summary>
            <div class="faq-body">
                <p>
                    No. The whole game runs inside your web browser. There's nothing
                    to install and no account to create — head to
                    <a href="<?= e(GAME_URL) ?>">Play</a> and you're in.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>What devices and browsers does it work on?</summary>
            <div class="faq-body">
                <p>
                    <?= e(SITE_NAME) ?> is built web-first and plays on desktop and
                    mobile alike — any reasonably modern browser (Chrome, Edge,
                    Firefox, Safari) will do. On a phone or tablet you get on-screen
                    touch controls; on a computer you play with the keyboard.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Is there a mobile app?</summary>
            <div class="faq-body">
                <p>
                    Not yet — for now <?= e(SITE_NAME) ?> is a browser game, and it's
                    built to play beautifully on a phone or tablet straight from the web,
                    with on-screen touch controls. You can add it to your home screen
                    from your browser for a quick, app-like shortcut.
                </p>
                <p>
                    We may consider a dedicated mobile app version down the line. If we
                    do, it would be a <strong>paid version</strong> — the browser game
                    stays free to play.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>How do I move and choose things?</summary>
            <div class="faq-body">
                <p>On a <strong>keyboard</strong>:</p>
                <ul>
                    <li><strong>Move</strong> — Arrow keys or <strong>W A S D</strong></li>
                    <li><strong>Confirm / talk / enter a door</strong> — <strong>Enter</strong>, <strong>Space</strong> or <strong>Z</strong></li>
                    <li><strong>Cancel / back</strong> — <strong>X</strong> or <strong>Backspace</strong></li>
                    <li><strong>Menu</strong> — <strong>Esc</strong> (or Enter when no dialogue is open)</li>
                </ul>
                <p>
                    On a <strong>touch screen</strong> the same actions live on the
                    on-screen pad and buttons. You can hide or show the touch
                    controls from the in-game Settings menu.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>There's no music or sound — what's wrong?</summary>
            <div class="faq-body">
                <p>
                    Nothing's broken. Browsers won't let a page play audio until you
                    interact with it, so the game waits for your first tap or key
                    press on the opening screen before the music starts. Press a key
                    (or tap) to begin and the sound will come in. You can also mute or
                    un-mute any time from the in-game Settings menu.
                </p>
            </div>
        </details>
    </div>
</section>

<section class="band faq">
    <h2 class="band-title">Saving &amp; your progress</h2>
    <div class="faq-list">
        <details class="faq-item">
            <summary>Does the game save automatically?</summary>
            <div class="faq-body">
                <p>
                    Yes. <?= e(SITE_NAME) ?> autosaves whenever you enter a new area,
                    so <strong>Continue</strong> always picks up close to where you
                    left off. You can also save deliberately at any time:
                    open the menu and choose <strong>Save</strong>.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Where is my save kept? Is it in the cloud?</summary>
            <div class="faq-body">
                <p>
                    Your progress is stored <strong>locally in your own browser</strong>,
                    on your device — it never leaves it, and we can't see it. That
                    means there's no login and nothing to sync, but it also means a
                    save belongs to the specific browser you played in.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Could I lose my progress?</summary>
            <div class="faq-body">
                <p>
                    Because the save lives in your browser, clearing your browser
                    data (history, cookies, site storage), playing in private /
                    incognito mode, or switching to a different browser or device can
                    leave it behind. To keep a copy safe, use <strong>Export
                    save</strong> (below) now and then.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Can I move my game to another device or browser?</summary>
            <div class="faq-body">
                <p>
                    Yes. In the in-game <strong>Settings</strong> menu choose
                    <strong>Export save</strong> to download your progress as a small
                    file. On the other device, open the game, go to Settings and
                    choose <strong>Import save</strong> to load that file. It's also
                    the simplest way to back up before clearing your browser.
                </p>
            </div>
        </details>
    </div>
</section>

<section class="band faq">
    <h2 class="band-title">Playing the game</h2>
    <div class="faq-list">
        <details class="faq-item">
            <summary>How do I catch kin?</summary>
            <div class="faq-body">
                <p>
                    In a wild encounter, choose to throw your <strong>vesperlamp</strong> —
                    your lamp is also your catching device, and a plain throw is always
                    free. Wearing a wild kin down first, or leaving it dozing or chilled,
                    makes it far easier to catch. For tougher kin you can spend a
                    <strong>charge</strong> (Glow, Beacon and others, bought or earned)
                    for a single, stronger throw.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>How do I heal my kin?</summary>
            <div class="faq-body">
                <p>
                    Rest. Inns and your own home restore your whole party to full —
                    talk to the keeper or step into bed. You can also use
                    healing items (gathered, bought, or found) from the Items menu
                    during your travels.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Do my kin evolve?</summary>
            <div class="faq-body">
                <p>
                    They <strong>kindle</strong> — the genre's "evolution",
                    reimagined. Most kin kindle into a stronger form once they reach a
                    certain level; some kindle only when the bond between you has grown
                    warm enough. When a kin is ready, the game asks if you'd like it to
                    kindle, and you can always say "not yet" and be offered again later.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>How many kin are there to collect?</summary>
            <div class="faq-body">
                <p>
                    Over 150 original kin, across ten elements — ember, tide, verdant,
                    stone, storm, frost, solar, lunar, light and dark. Every one is
                    original art and design. You can browse the first fifty on the
                    <a href="creatures.php">Kin</a> page.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>How do type strengths and weaknesses work?</summary>
            <div class="faq-body">
                <p>
                    Every kin and every move belongs to one of the ten elements, and
                    some elements beat others. When you attack, the game multiplies your
                    damage by how well your move's type matches the <em>defender's</em>
                    type:
                </p>
                <ul class="eff-legend" aria-label="Effectiveness multipliers">
                    <li><span class="eff-mult eff-x0">×0</span> no effect — it can't be hurt by that type</li>
                    <li><span class="eff-mult eff-xhalf">×½</span> resisted — half damage</li>
                    <li><span class="eff-mult eff-x1">×1</span> normal damage</li>
                    <li><span class="eff-mult eff-x2">×2</span> super-effective — double damage</li>
                </ul>
                <p>
                    Many kin have <strong>two</strong> types, and the multipliers simply
                    multiply together. So a move that's super-effective against
                    <em>both</em> of a kin's types lands a huge <span class="eff-mult eff-x2">×4</span>,
                    while one that's strong against one type but resisted by the other
                    cancels back to a normal <span class="eff-mult eff-x1">×1</span>. You
                    don't have to do the sums in your head — the game tells you "It's
                    super-effective!" or "It's not very effective…" after each hit.
                </p>

                <h4 class="faq-subhead">The two mirror axes</h4>
                <p>
                    Most matchups run one way — water beats fire, and so on. But four of
                    the elements are tied to the sky, and two pairs of them strike each
                    other <strong>super-effectively both ways</strong>. These are the
                    <em>mirror axes</em>, and they make for fast, knife-edge battles:
                </p>
                <div class="mirror-axes">
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
                <p>
                    Normally a type that hits hard also takes hits hard back, but each
                    side of a mirror axis can flatten the other in a single turn — so
                    these fights swing wildly, which is exactly why the game saves them
                    for rare, late and legendary kin. Want it in one sentence?
                    <strong>Solar and Lunar wreck each other; Light and Dark wreck each
                    other</strong> — bring the right answer and hit first.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>What are Gleams, Lumenaries and Lantern Gifts?</summary>
            <div class="faq-body">
                <p>
                    They're the heart of the journey. A <strong>Lumenary</strong> is a
                    valley's warden-hall; best its <strong>Lampwarden</strong> and you
                    earn a <strong>Gleam</strong> — a constellation relit, which blooms
                    back into the night sky for real. Along the way you gain
                    <strong>Lantern Gifts</strong>: field powers that open new roads as
                    you travel. There's a fuller glossary on
                    <a href="story.php">The World</a> page.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>What's the Hearth?</summary>
            <div class="faq-body">
                <p>
                    The <strong>Hearth</strong> is a warm keep where your kin rest when
                    they're not travelling in your lamp — the genre's storage box, made
                    cosy. You carry a party of up to six; the rest wait safely at the
                    Hearth, tended by the Hearthkeeper, ready to swap in whenever you like.
                </p>
            </div>
        </details>
    </div>
</section>

<section class="band faq">
    <h2 class="band-title">About PixelKin</h2>
    <div class="faq-list">
        <details class="faq-item">
            <summary>Is this Pokémon?</summary>
            <div class="faq-body">
                <p>
                    No. <?= e(SITE_NAME) ?> is an original creature-collecting
                    adventure — inspired by the genre, a copy of nothing. Every
                    creature, name, sprite, piece of music and line of story is our own.
                    It shares the warm, nostalgic <em>feeling</em> of handheld-era
                    monster-collecting, but its world, characters and lore are all new.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>What's the game actually about?</summary>
            <div class="faq-body">
                <p>
                    Night has fallen over the valleys of <strong>Vesperholm</strong>
                    and won't lift. You play a lamp-tender's apprentice setting out to
                    relight the sky, one constellation at a time, with the kin who walk
                    the dark beside you. It's a cosy, slightly melancholy tale — read
                    more on <a href="story.php">The World</a> page.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Is it finished? Will it keep getting updates?</summary>
            <div class="faq-body">
                <p>
                    <?= e(SITE_NAME) ?> is in active development. The world, story,
                    creatures and soundtrack are designed and locked, and more of the
                    journey opens up over time. Because saves live in your browser, a
                    major update can occasionally reset progress — exporting a save
                    keeps a copy you can re-import.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Is it suitable for children?</summary>
            <div class="faq-body">
                <p>
                    Yes — it's family-friendly. The story is gentle, the conflict is
                    never cruel (even the opposing Hollowing are weary, not wicked), and
                    there's nothing to buy or sign up for inside the game.
                </p>
            </div>
        </details>
        <details class="faq-item">
            <summary>Who makes PixelKin? Can I license or partner on it?</summary>
            <div class="faq-body">
                <p>
                    <?= e(SITE_NAME) ?> is designed and built by
                    <a href="<?= e(STUDIO_URL) ?>" target="_blank" rel="noopener"><?= e(STUDIO_NAME) ?></a>,
                    app, web and game developers. For licensing, partnership or press
                    enquiries, see the <a href="license.php">Licensing</a> page.
                </p>
            </div>
        </details>
    </div>
</section>

<section class="band cta-band">
    <div class="cta-inner">
        <h2>Still curious? Go and wander.</h2>
        <p>The fastest way to your questions' answers is to light the lamp.</p>
        <a class="btn btn-primary btn-lg" href="<?= e(GAME_URL) ?>">Play in your browser</a>
    </div>
</section>

<?php page_foot(); ?>
