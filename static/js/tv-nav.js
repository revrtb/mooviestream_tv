/**
 * Smart TV / remote navigation (d-pad + Enter)
 * Spatial navigation and focus management for WebOS, Tizen, Android TV.
 * Does not change business logic; layout and interaction only.
 */
(function () {
    'use strict';

    var FOCUSABLE_SELECTOR = [
        'a[href]',
        'button:not([disabled])',
        'input:not([disabled])',
        'select:not([disabled])',
        'textarea:not([disabled])',
        '[tabindex]:not([tabindex="-1"])'
    ].join(', ');

    function getFocusables(container) {
        container = container || document;
        var nodes = container.querySelectorAll(FOCUSABLE_SELECTOR);
        return Array.prototype.filter.call(nodes, function (el) {
            if (el.offsetParent === null ||
                window.getComputedStyle(el).visibility === 'hidden' ||
                window.getComputedStyle(el).display === 'none') {
                return false;
            }
            /* Do not focus on genre tags in movie/TV detail pages */
            if (el.classList.contains('genre-tag') || el.closest('.movie-genres')) {
                return false;
            }
            /* In Video.js player: only the play button is focusable (big play or play/pause control) */
            if (el.closest('.video-js')) {
                if (el.classList.contains('vjs-big-play-button') || el.classList.contains('vjs-play-control')) {
                    return true;
                }
                return false;
            }
            return true;
        });
    }

    function getRect(el) {
        var r = el.getBoundingClientRect();
        return {
            top: r.top,
            left: r.left,
            right: r.right,
            bottom: r.bottom,
            width: r.width,
            height: r.height,
            midX: r.left + r.width / 2,
            midY: r.top + r.height / 2
        };
    }

    function findNearestInDirection(focusables, current, direction) {
        if (!current || focusables.length === 0) return null;
        var curRect = getRect(current);
        var candidates = [];
        var threshold = 50;

        focusables.forEach(function (el) {
            if (el === current) return;
            var r = getRect(el);
            var dx = r.midX - curRect.midX;
            var dy = r.midY - curRect.midY;

            var match = false;
            if (direction === 'left')  match = dx < -threshold && Math.abs(dy) < curRect.height;
            if (direction === 'right') match = dx > threshold && Math.abs(dy) < curRect.height;
            if (direction === 'up')   match = dy < -threshold && Math.abs(dx) < curRect.width;
            if (direction === 'down') match = dy > threshold && Math.abs(dx) < curRect.width;

            if (match) {
                var dist = Math.sqrt(dx * dx + dy * dy);
                candidates.push({ el: el, dist: dist, dx: dx, dy: dy });
            }
        });

        if (candidates.length === 0) {
            if (direction === 'left' || direction === 'right') {
                candidates = focusables.filter(function (el) {
                    var r = getRect(el);
                    if (direction === 'left')  return r.right <= curRect.left + 5;
                    if (direction === 'right') return r.left >= curRect.right - 5;
                    return false;
                }).map(function (el) {
                    var r = getRect(el);
                    var d = direction === 'left' ? curRect.left - r.right : r.left - curRect.right;
                    return { el: el, dist: Math.abs(d) };
                });
            } else {
                candidates = focusables.filter(function (el) {
                    var r = getRect(el);
                    if (direction === 'up')   return r.bottom <= curRect.top + 5;
                    if (direction === 'down') return r.top >= curRect.bottom - 5;
                    return false;
                }).map(function (el) {
                    var r = getRect(el);
                    var d = direction === 'up' ? curRect.top - r.bottom : r.top - curRect.bottom;
                    return { el: el, dist: Math.abs(d) };
                });
            }
        }

        if (candidates.length === 0) return null;
        candidates.sort(function (a, b) { return a.dist - b.dist; });
        return candidates[0].el;
    }

    function focusAndScroll(el) {
        if (!el) return;
        el.focus({ preventScroll: false });
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
    }

    function isTVContext() {
        return window.matchMedia('(min-width: 1280px) and (min-height: 720px)').matches;
    }

    function handleKeydown(e) {
        if (!isTVContext()) return;

        var key = e.key;
        var current = document.activeElement;

        if (key === 'ArrowLeft' || key === 'ArrowRight' || key === 'ArrowUp' || key === 'ArrowDown') {
            var focusables = getFocusables();
            if (focusables.length === 0) return;

            if (!current || focusables.indexOf(current) === -1) {
                focusAndScroll(focusables[0]);
                e.preventDefault();
                return;
            }

            var dir = key.replace('Arrow', '').toLowerCase();
            var next = findNearestInDirection(focusables, current, dir);
            if (next) {
                focusAndScroll(next);
            }
            /* Always prevent so player does not use arrows for volume/seek */
            e.preventDefault();
            return;
        }

        if (key === 'Enter' || key === ' ') {
            if (current && current.classList.contains('movie-card')) {
                var href = current.getAttribute('data-detail-href');
                if (href) {
                    window.location.href = href;
                    e.preventDefault();
                }
                return;
            }
            if (current && (current.tagName === 'A' && current.getAttribute('href') === '#')) {
                e.preventDefault();
                if (current.classList.contains('dropdown-toggle')) {
                    current.parentNode.classList.toggle('active');
                    var menu = current.parentNode.querySelector('.dropdown-menu');
                    if (menu) {
                        var first = menu.querySelector(FOCUSABLE_SELECTOR);
                        if (first) setTimeout(function () { first.focus(); }, 50);
                    }
                }
            }
            return;
        }

        if (key === 'Escape') {
            var openDropdown = document.querySelector('.dropdown.active');
            if (openDropdown) {
                var toggle = openDropdown.querySelector('.dropdown-toggle');
                openDropdown.classList.remove('active');
                if (toggle) toggle.focus();
                e.preventDefault();
                return;
            }
            var modal = document.querySelector('.modal[style*="block"]') || document.getElementById('trailer-modal');
            if (modal && modal.style.display === 'block') {
                var closeBtn = modal.querySelector('.close-modal');
                if (closeBtn) closeBtn.click();
                e.preventDefault();
            }
        }
    }

    var lastCardNav = 0;
    function getCardFromEvent(e) {
        var target = e.target && e.target.closest ? e.target.closest('.movie-card') : null;
        if (target && target.getAttribute && target.getAttribute('data-detail-href')) return target;
        /* WebOS: target can be wrong for pointer events; try element under coordinates */
        if (e.clientX != null && e.clientY != null) {
            var el = document.elementFromPoint(e.clientX, e.clientY);
            if (el) {
                var card = el.closest ? el.closest('.movie-card') : null;
                if (card && card.getAttribute && card.getAttribute('data-detail-href')) return card;
            }
        }
        return null;
    }
    function handleCardActivation(e) {
        if (e.target && e.target.closest && e.target.closest('a') && e.target.closest('a').getAttribute('href') !== '#') return;
        var card = getCardFromEvent(e);
        if (!card) return;
        var now = Date.now();
        if (now - lastCardNav < 500) return;
        lastCardNav = now;
        e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
        window.location.href = card.getAttribute('data-detail-href');
    }

    function init() {
        document.addEventListener('keydown', handleKeydown, true);
        document.addEventListener('click', handleCardActivation, true);
        document.addEventListener('pointerup', handleCardActivation, true);
        /* WebOS: pointer click often only fires pointerdown, not pointerup/click */
        document.addEventListener('pointerdown', handleCardActivation, true);
        if (document.body && isTVContext()) {
            document.body.classList.add('tv-nav-enabled');
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
