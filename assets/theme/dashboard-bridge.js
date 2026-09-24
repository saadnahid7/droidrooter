/* Command Center: align the native console mode with the public site. */
(() => {
  const root = document.documentElement;
  const siteKey = 'droidrooter-color-mode';
  const adminKey = 'drvcam.admin.theme';
  const valid = mode => mode === 'dark' || mode === 'light';
  const read = key => { try { return localStorage.getItem(key); } catch (_) { return null; } };
  const save = (key, mode) => { try { localStorage.setItem(key, mode); } catch (_) {} };
  const initial = read(siteKey);
  const mode = valid(initial) ? initial : (valid(read(adminKey)) ? read(adminKey) : 'dark');
  root.dataset.theme = mode;
  root.dataset.colorMode = mode;
  root.style.colorScheme = mode;
  save(adminKey, mode);
  const label = button => {
    const current = root.dataset.theme === 'light' ? 'light' : 'dark';
    button.textContent = current === 'dark' ? 'Light mode' : 'Dark mode';
    button.setAttribute('aria-label', 'Switch to ' + (current === 'dark' ? 'light' : 'dark') + ' mode');
    button.setAttribute('aria-pressed', String(current === 'light'));
  };
  document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('[data-dashboard-theme-toggle]');
    const app = document.getElementById('root');
    if (!button || !app) return;
    const refresh = () => {
      button.hidden = !app.querySelector('.login-card');
      label(button);
    };
    button.addEventListener('click', () => {
      const next = root.dataset.theme === 'light' ? 'dark' : 'light';
      root.dataset.theme = next;
      root.dataset.colorMode = next;
      root.style.colorScheme = next;
      save(adminKey, next);
      save(siteKey, next);
      label(button);
    });
    new MutationObserver(refresh).observe(app, { childList: true, subtree: true });
    new MutationObserver(() => {
      const next = root.dataset.theme;
      if (valid(next)) {
        root.dataset.colorMode = next;
        root.style.colorScheme = next;
        save(siteKey, next);
        label(button);
      }
    }).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
    refresh();
  });
})();
