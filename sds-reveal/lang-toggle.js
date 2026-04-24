/*
 * Bilingual EN/JA slide toggle.
 *
 * Press `L` (or `l`) to toggle between English and Japanese on any slide.
 * The chosen language persists across page reloads via localStorage.
 *
 * Paired content is authored in the .qmd as:
 *   ::: {.lang-en}  ...English...  :::
 *   ::: {.lang-ja}  ...Japanese... :::
 *
 * The CSS in lang-toggle.css hides whichever language is inactive; this
 * script just flips body.show-ja on L keypress and keeps the badge in sync.
 * We never re-render content — both language blocks stay in the DOM so
 * KaTeX math and Mermaid diagrams only need to render once.
 */

(function () {
  const STORAGE_KEY = 'hml-slide-lang';
  const TOGGLE_KEY = 'l';

  function getLang() {
    try {
      return localStorage.getItem(STORAGE_KEY) === 'ja' ? 'ja' : 'en';
    } catch (_) {
      return 'en';
    }
  }

  function setLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (_) { /* ignore quota / privacy-mode errors */ }
    document.body.classList.toggle('show-ja', lang === 'ja');
    updateBadge(lang);
  }

  function updateBadge(lang) {
    const badge = document.querySelector('.lang-badge .lang-current');
    if (badge) badge.textContent = lang.toUpperCase();
  }

  function mountBadge() {
    if (document.querySelector('.lang-badge')) return;
    const el = document.createElement('div');
    el.className = 'lang-badge';
    el.innerHTML = '<span class="lang-current">EN</span><span class="lang-hint">Press L</span>';
    document.body.appendChild(el);
  }

  function toggle() {
    setLang(getLang() === 'ja' ? 'en' : 'ja');
  }

  function isTypingTarget(el) {
    if (!el) return false;
    return el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.isContentEditable;
  }

  function handleKeyFallback(e) {
    // Fallback for non-Reveal pages. On Reveal pages we register via
    // Reveal.addKeyBinding below so our L takes priority over nav.
    if (isTypingTarget(e.target)) return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if ((e.key || '').toLowerCase() !== TOGGLE_KEY) return;
    e.preventDefault();
    e.stopPropagation();
    toggle();
  }

  function registerWithReveal() {
    // Reveal's addKeyBinding claims the key at a higher priority than the
    // default navigation handlers, so pressing L toggles language without
    // also advancing the slide.
    //   76 = 'L' (case-insensitive — Reveal normalizes)
    if (!window.Reveal || typeof window.Reveal.addKeyBinding !== 'function') {
      return false;
    }
    try {
      window.Reveal.addKeyBinding(
        { keyCode: 76, key: 'L', description: 'Toggle language (EN/JA)' },
        toggle
      );
      return true;
    } catch (_) {
      return false;
    }
  }

  function init() {
    mountBadge();
    setLang(getLang()); // apply persisted choice on load

    if (window.Reveal && typeof window.Reveal.isReady === 'function' && window.Reveal.isReady()) {
      registerWithReveal() || document.addEventListener('keydown', handleKeyFallback);
    } else if (window.Reveal && typeof window.Reveal.on === 'function') {
      // Wait for Reveal to finish initialization, then bind.
      window.Reveal.on('ready', () => {
        registerWithReveal() || document.addEventListener('keydown', handleKeyFallback);
      });
    } else {
      // Plain page (no Reveal) — use the document listener.
      document.addEventListener('keydown', handleKeyFallback);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
