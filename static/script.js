// Libris — Library Management System
// Global JS utilities

document.addEventListener('DOMContentLoaded', () => {

  // ── AUTO-DISMISS FLASH MESSAGES ──────────────────────────────────────────
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.4s ease, max-height 0.4s ease';
      el.style.opacity = '0';
      el.style.maxHeight = '0';
      el.style.overflow = 'hidden';
      setTimeout(() => el.remove(), 420);
    }, 3600);
  });

  // ── MARK ACTIVE NAV ITEM ────────────────────────────────────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(link => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });

  // ── CONFIRM DESTRUCTIVE ACTIONS (fallback) ──────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm(btn.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // ── ANIMATE STAT VALUES ─────────────────────────────────────────────────
  document.querySelectorAll('.stat-value').forEach(el => {
    const target = parseInt(el.textContent, 10);
    if (isNaN(target) || target === 0) return;

    let start = 0;
    const duration = 600;
    const step = 16;
    const increment = target / (duration / step);

    const timer = setInterval(() => {
      start += increment;
      if (start >= target) {
        el.textContent = target;
        clearInterval(timer);
      } else {
        el.textContent = Math.floor(start);
      }
    }, step);
  });

});