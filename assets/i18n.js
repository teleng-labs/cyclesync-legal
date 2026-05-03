/* Global EN/ES toggle. Walks the DOM, swaps text nodes by data-i18n attrs.
   Persists choice in localStorage; floating switcher in the corner. */
(function () {
  const STORAGE_KEY = 'cs-lang';

  function detectInitial() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'en' || saved === 'es') return saved;
    } catch (_) {}
    return (navigator.language || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
  }

  function applyLang(lang) {
    document.documentElement.lang = lang;
    // Text content swap
    document.querySelectorAll('[data-en]').forEach((el) => {
      const v = el.getAttribute('data-' + lang);
      if (v != null) {
        // allow simple HTML in translations (em, br, code, span, a, strong)
        if (/<[a-z]/i.test(v)) {
          el.innerHTML = v;
        } else {
          el.textContent = v;
        }
      }
    });
    // Attribute swap (e.g. title, alt, aria-label, content for meta)
    document.querySelectorAll('[data-i18n-attr]').forEach((el) => {
      const spec = el.getAttribute('data-i18n-attr'); // e.g. "title|content"
      spec.split('|').forEach((attr) => {
        const v = el.getAttribute(`data-${attr}-${lang}`);
        if (v != null) el.setAttribute(attr, v);
      });
    });
    // Document title
    const titleEl = document.querySelector('title[data-en]');
    if (titleEl) {
      const v = titleEl.getAttribute('data-' + lang);
      if (v != null) document.title = v;
    }
    // Update switcher state
    document.querySelectorAll('.lang-switch button').forEach((b) => {
      b.classList.toggle('active', b.dataset.lang === lang);
      b.setAttribute('aria-pressed', b.dataset.lang === lang ? 'true' : 'false');
    });
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (_) {}
  }

  function buildSwitcher() {
    if (document.querySelector('.lang-switch')) return;
    const wrap = document.createElement('div');
    wrap.className = 'lang-switch';
    wrap.setAttribute('role', 'group');
    wrap.setAttribute('aria-label', 'Language');
    wrap.innerHTML = `
      <button data-lang="en" aria-pressed="false">EN</button>
      <span class="sep" aria-hidden="true">·</span>
      <button data-lang="es" aria-pressed="false">ES</button>
    `;
    document.body.appendChild(wrap);
    wrap.querySelectorAll('button').forEach((b) => {
      b.addEventListener('click', () => applyLang(b.dataset.lang));
    });
  }

  function init() {
    buildSwitcher();
    applyLang(detectInitial());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
