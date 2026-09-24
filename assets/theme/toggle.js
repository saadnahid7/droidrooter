/* Dark / light switch. Dark is Command Center, light is Terminal. */
(() => {
  const root = document.documentElement;
  const COLOR_KEY = 'droidrooter-color-mode';

  function render(mode) {
    root.dataset.colorMode = mode;
    root.dataset.design = mode === 'light' ? 'terminal' : 'command';
    root.style.colorScheme = mode;
    const dark = mode === 'dark';
    document.querySelectorAll('[data-theme-toggle]').forEach(button => {
      button.setAttribute('aria-pressed', String(dark));
      button.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
      button.title = dark ? 'Switch to light theme' : 'Switch to dark theme';
      const label = button.querySelector('[data-theme-label]');
      if (label) label.textContent = dark ? 'Light' : 'Dark';
    });
  }

  render(root.dataset.colorMode === 'light' ? 'light' : 'dark');
  document.querySelectorAll('[data-theme-controls]').forEach(group => { group.hidden = false; });
  document.querySelectorAll('[data-theme-toggle]').forEach(button => {
    button.addEventListener('click', () => {
      const mode = root.dataset.colorMode === 'dark' ? 'light' : 'dark';
      render(mode);
      try { localStorage.setItem(COLOR_KEY, mode); } catch (_) { /* the choice still applies to this page */ }
    });
  });

  // Keep other open tabs in step.
  window.addEventListener('storage', event => {
    if (event.key === COLOR_KEY || event.key === null) render(event.newValue === 'light' ? 'light' : 'dark');
  });
})();
