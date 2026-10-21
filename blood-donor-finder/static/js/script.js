/**
 * script.js – LifeLine Blood Donor Finder
 * Mobile nav toggle, flash auto-dismiss, data-confirm handler
 */

(function () {
  'use strict';

  // ── Mobile navigation toggle ───────────────────────────────────────────────
  const navToggle = document.getElementById('navToggle');
  const navMenu   = document.getElementById('navMenu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = navMenu.classList.toggle('nav__menu--open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('nav__menu--open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        navMenu.classList.remove('nav__menu--open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.focus();
      }
    });
  }

  // ── Auto-dismiss flash messages ────────────────────────────────────────────
  const AUTO_DISMISS_MS = 6000;

  function dismissFlash(el) {
    el.style.transition = 'opacity 0.4s ease, max-height 0.4s ease, padding 0.4s ease';
    el.style.opacity = '0';
    el.style.maxHeight = el.offsetHeight + 'px';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        el.style.maxHeight = '0';
        el.style.padding   = '0';
      });
    });
    setTimeout(() => el.remove(), 500);
  }

  document.querySelectorAll('.flash').forEach((flash) => {
    // Close button
    const closeBtn = flash.querySelector('.flash__close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => dismissFlash(flash));
    }

    // Auto-dismiss (skip for warnings/danger so user has time to read)
    const category = [...flash.classList]
      .find(c => c.startsWith('flash--') && c !== 'flash')
      ?.replace('flash--', '');

    if (category === 'success' || category === 'info') {
      setTimeout(() => dismissFlash(flash), AUTO_DISMISS_MS);
    }
  });

  // ── data-confirm handler for destructive forms ─────────────────────────────
  // Usage: <form data-confirm="Are you sure?">
  document.querySelectorAll('form[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      const msg = form.getAttribute('data-confirm') || 'Are you sure? This action cannot be undone.';
      if (!window.confirm(msg)) {
        e.preventDefault();
      }
    });
  });

  // ── Star rating accessibility ──────────────────────────────────────────────
  // Keyboard support: arrow keys cycle through star values
  const starGroup = document.querySelector('.star-rating');
  if (starGroup) {
    const radios = Array.from(starGroup.querySelectorAll('.star-radio'));
    radios.forEach((radio, idx) => {
      radio.addEventListener('keydown', (e) => {
        let target = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          // radios are reversed (5→1), so "up" in score = lower index
          target = radios[Math.max(0, idx - 1)];
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          target = radios[Math.min(radios.length - 1, idx + 1)];
        }
        if (target) {
          target.checked = true;
          target.focus();
          e.preventDefault();
        }
      });
    });
  }

  // ── Form: phone input — digits only ───────────────────────────────────────
  document.querySelectorAll('input[type="tel"]').forEach((input) => {
    input.addEventListener('input', () => {
      input.value = input.value.replace(/\D/g, '').slice(0, 10);
    });
  });

  // ── Admin: auto-submit status dropdowns already handled by onchange ────────
  // Additional: highlight active row on hover for readability — handled via CSS

})();
