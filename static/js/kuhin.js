/**
 * KUHIN — Progressive Enhancement JS
 * ====================================
 * Core interactivity is handled inline in base.html.
 * This file provides additional progressive enhancement.
 */

document.addEventListener('DOMContentLoaded', function () {

  /* ── Smooth anchor scroll ── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const offset = document.getElementById('mainNav')?.offsetHeight || 80;
        window.scrollTo({ top: target.offsetTop - offset - 16, behavior: 'smooth' });
      }
    });
  });

  /* ── Form submit feedback ── */
  document.querySelectorAll('form[method="post"]').forEach(form => {
    form.addEventListener('submit', function () {
      const btn = this.querySelector('button[type="submit"]');
      if (btn && !btn.disabled) {
        btn.setAttribute('data-original', btn.innerHTML);
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2" aria-hidden="true"></i>Sending…';
        btn.disabled = true;
        // Re-enable after 8s as fallback (in case of validation errors)
        setTimeout(() => {
          btn.disabled = false;
          const orig = btn.getAttribute('data-original');
          if (orig) btn.innerHTML = orig;
        }, 8000);
      }
    });
  });

  /* ── Auto-dismiss flash messages after 5s ── */
  document.querySelectorAll('.ku-alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  /* ── Active nav link highlight ── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links .nav-link, .nav-mobile-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });

});
