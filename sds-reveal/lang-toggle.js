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

  function handleKey(e) {
    // Skip if the user is typing in an input/textarea/contentEditable.
    const t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    // Skip if modifier keys are held (reserve toggle for bare L).
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if ((e.key || '').toLowerCase() !== TOGGLE_KEY) return;
    e.preventDefault();
    setLang(getLang() === 'ja' ? 'en' : 'ja');
  }

  function init() {
    mountBadge();
    setLang(getLang()); // apply persisted choice on load
    document.addEventListener('keydown', handleKey);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
