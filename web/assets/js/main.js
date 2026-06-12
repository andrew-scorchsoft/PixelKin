/* Progressive enhancement for the PixelKin site. No framework, no build step —
   the site works without JS; this adds the mobile nav, the hero parallax, and
   the gallery lightbox. */
(function () {
    'use strict';

    /* --- Mobile nav toggle -------------------------------------------------- */
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.nav');
    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            var open = nav.classList.toggle('open');
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        nav.addEventListener('click', function (e) {
            if (e.target.tagName === 'A') {
                nav.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    /* --- Firm up the nav once scrolled off the hero ----------------------- */
    var masthead = document.querySelector('.masthead');
    if (masthead) {
        var onScroll = function () {
            masthead.classList.toggle('scrolled', window.scrollY > 40);
        };
        onScroll();
        window.addEventListener('scroll', onScroll, { passive: true });
    }

    /* --- Hero parallax (mouse / pointer reactive) -------------------------- */
    var hero = document.getElementById('hero');
    if (hero) {
        var layers = hero.querySelectorAll('[data-depth]');
        var raf = null, px = 0, py = 0;
        function apply() {
            raf = null;
            layers.forEach(function (el) {
                var d = parseFloat(el.dataset.depth) || 0;
                el.style.setProperty('--px', (-px * d) + 'px');
                el.style.setProperty('--py', (-py * d * 0.5) + 'px');
            });
        }
        hero.addEventListener('pointermove', function (e) {
            var r = hero.getBoundingClientRect();
            px = (e.clientX - r.left) / r.width - 0.5;
            py = (e.clientY - r.top) / r.height - 0.5;
            if (!raf) raf = requestAnimationFrame(apply);
        });
        hero.addEventListener('pointerleave', function () {
            px = 0; py = 0;
            if (!raf) raf = requestAnimationFrame(apply);
        });
    }

    /* --- Gallery lightbox -------------------------------------------------- */
    var lb = document.getElementById('lightbox');
    if (lb) {
        var lbImg = lb.querySelector('.lb-img');
        var lbTitle = lb.querySelector('.lb-title');
        var lbBlurb = lb.querySelector('.lb-blurb');
        var lbChips = lb.querySelector('.lb-chips');
        var lbCount = lb.querySelector('.lb-count');
        var group = [], idx = 0, lastFocus = null;

        function itemsIn(g) {
            return Array.prototype.slice.call(
                document.querySelectorAll('[data-lb][data-lb-group="' + g + '"]')
            );
        }
        function render() {
            var el = group[idx];
            if (!el) return;
            lbImg.src = el.dataset.lbImg;
            lbImg.alt = el.dataset.lbTitle || '';
            lbImg.classList.toggle('pixel', el.dataset.lbPixel === '1');
            lbTitle.textContent = el.dataset.lbTitle || '';
            lbBlurb.textContent = el.dataset.lbBlurb || '';
            lbChips.innerHTML = '';
            (el.dataset.lbChips || '').split(';').forEach(function (pair) {
                if (!pair) return;
                var bits = pair.split(',');
                var chip = document.createElement('span');
                chip.className = 'type-chip';
                chip.textContent = bits[0];
                if (bits[1]) chip.style.setProperty('--tint', bits[1]);
                lbChips.appendChild(chip);
            });
            lbCount.textContent = group.length > 1 ? (idx + 1) + ' / ' + group.length : '';
        }
        function open(el) {
            lastFocus = document.activeElement;
            group = itemsIn(el.dataset.lbGroup);
            idx = group.indexOf(el);
            if (idx < 0) idx = 0;
            render();
            lb.hidden = false;
            document.body.classList.add('lb-open');
            lb.querySelector('.lb-close').focus();
        }
        function close() {
            lb.hidden = true;
            document.body.classList.remove('lb-open');
            if (lastFocus && lastFocus.focus) lastFocus.focus();
        }
        function step(n) {
            if (!group.length) return;
            idx = (idx + n + group.length) % group.length;
            render();
        }

        document.addEventListener('click', function (e) {
            var trigger = e.target.closest('[data-lb]');
            if (trigger) { open(trigger); return; }
            if (e.target.closest('[data-lb-close]')) close();
            else if (e.target.closest('[data-lb-prev]')) step(-1);
            else if (e.target.closest('[data-lb-next]')) step(1);
        });
        document.addEventListener('keydown', function (e) {
            var trigger = e.target.closest && e.target.closest('[data-lb]');
            if (trigger && (e.key === 'Enter' || e.key === ' ')) {
                e.preventDefault(); open(trigger); return;
            }
            if (lb.hidden) return;
            if (e.key === 'Escape') close();
            else if (e.key === 'ArrowLeft') step(-1);
            else if (e.key === 'ArrowRight') step(1);
        });
    }

    /* --- Storybook (page-flipping tale) ----------------------------------- */
    var book = document.getElementById('book');
    if (book) {
        var pages = Array.prototype.slice.call(book.querySelectorAll('[data-page]'));
        var prevBtn = book.querySelector('.book-prev');
        var nextBtn = book.querySelector('.book-next');
        var dotsWrap = document.getElementById('bookDots');
        var current = 0, animating = false;
        var reduce = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (pages.length > 1) {
            pages[0].classList.add('is-active');

            // Build the dot indicators.
            var dots = [];
            if (dotsWrap) {
                pages.forEach(function (_, i) {
                    var d = document.createElement('button');
                    d.type = 'button';
                    d.setAttribute('role', 'tab');
                    d.setAttribute('aria-label', 'Page ' + (i + 1));
                    d.addEventListener('click', function () { turn(i); });
                    dotsWrap.appendChild(d);
                    dots.push(d);
                });
            }

            var sync = function () {
                if (prevBtn) prevBtn.hidden = current === 0;
                if (nextBtn) nextBtn.hidden = current === pages.length - 1;
                book.classList.toggle('is-end', current === pages.length - 1);
                dots.forEach(function (d, i) {
                    d.classList.toggle('active', i === current);
                    d.setAttribute('aria-selected', i === current ? 'true' : 'false');
                });
            };

            // Wait for a transform transition to finish, with a safety fallback.
            var onEnd = function (el, done) {
                var fired = false;
                var finish = function () {
                    if (fired) return; fired = true;
                    el.removeEventListener('transitionend', handler);
                    done();
                };
                var handler = function (e) { if (e.propertyName === 'transform') finish(); };
                el.addEventListener('transitionend', handler);
                setTimeout(finish, 820);
            };

            var turn = function (to) {
                if (animating || to === current || to < 0 || to >= pages.length) return;
                var forward = to > current;
                var leaving = pages[current];
                var entering = pages[to];

                if (reduce) {
                    leaving.classList.remove('is-active');
                    entering.classList.add('is-active');
                    current = to; sync();
                    return;
                }

                animating = true;
                book.classList.add('is-turning');

                if (forward) {
                    entering.style.zIndex = '1';
                    leaving.style.zIndex = '4';
                    entering.classList.add('is-active');
                    void book.offsetWidth;            // reflow so the next transform animates
                    leaving.classList.add('turning'); // current page flips away to the left
                    onEnd(leaving, function () {
                        leaving.classList.remove('is-active', 'turning');
                        leaving.style.zIndex = '';
                        entering.style.zIndex = '';
                        current = to; animating = false;
                        book.classList.remove('is-turning'); sync();
                    });
                } else {
                    entering.style.zIndex = '4';
                    leaving.style.zIndex = '1';
                    entering.classList.add('is-active', 'pre-turned');
                    void book.offsetWidth;
                    entering.classList.remove('pre-turned');
                    entering.classList.add('turning-back'); // previous page flips back into view
                    onEnd(entering, function () {
                        entering.classList.remove('turning-back');
                        leaving.classList.remove('is-active');
                        leaving.style.zIndex = '';
                        entering.style.zIndex = '';
                        current = to; animating = false;
                        book.classList.remove('is-turning'); sync();
                    });
                }
            };

            if (nextBtn) nextBtn.addEventListener('click', function () { turn(current + 1); });
            if (prevBtn) prevBtn.addEventListener('click', function () { turn(current - 1); });

            // Tap anywhere on the page (but not a button/link) advances.
            book.querySelector('.book-inner').addEventListener('click', function (e) {
                if (e.target.closest('a, button')) return;
                if (current < pages.length - 1) turn(current + 1);
            });

            // Keyboard when the book has focus.
            book.addEventListener('keydown', function (e) {
                if (e.key === 'ArrowRight') { e.preventDefault(); turn(current + 1); }
                else if (e.key === 'ArrowLeft') { e.preventDefault(); turn(current - 1); }
            });

            // Swipe on touch.
            var sx = 0, sy = 0, tracking = false;
            book.addEventListener('touchstart', function (e) {
                var t = e.changedTouches[0]; sx = t.clientX; sy = t.clientY; tracking = true;
            }, { passive: true });
            book.addEventListener('touchend', function (e) {
                if (!tracking) return; tracking = false;
                var t = e.changedTouches[0];
                var dx = t.clientX - sx, dy = t.clientY - sy;
                if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
                    turn(current + (dx < 0 ? 1 : -1));
                }
            }, { passive: true });

            sync();
        }
    }
})();
