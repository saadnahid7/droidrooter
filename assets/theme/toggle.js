/* Theme controls: design (Command Center / Terminal) and color (dark / light). */
(() => {
  const root = document.documentElement;
  const DESIGN_KEY = 'droidrooter-design';
  const COLOR_KEY = 'droidrooter-color-mode';
  const NAMES = { command: 'Command Center', terminal: 'Terminal' };
  const save = (key, value) => { try { localStorage.setItem(key, value); } catch (_) { /* choice still applies to this page */ } };

  function renderColor(mode) {
    root.dataset.colorMode = mode;
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

  function renderDesign(design) {
    root.dataset.design = design;
    const other = design === 'terminal' ? 'command' : 'terminal';
    document.querySelectorAll('[data-design-toggle]').forEach(button => {
      button.setAttribute('aria-label', 'Design: ' + NAMES[design] + '. Switch to ' + NAMES[other]);
      button.title = 'Switch to ' + NAMES[other] + ' design';
      const label = button.querySelector('[data-design-label]');
      if (label) label.textContent = other === 'terminal' ? 'Terminal' : 'Command';
    });
  }

  renderColor(root.dataset.colorMode === 'light' ? 'light' : 'dark');
  renderDesign(root.dataset.design === 'terminal' ? 'terminal' : 'command');

  document.querySelectorAll('[data-theme-controls]').forEach(group => { group.hidden = false; });
  document.querySelectorAll('[data-theme-toggle]').forEach(button => {
    button.addEventListener('click', () => {
      const mode = root.dataset.colorMode === 'dark' ? 'light' : 'dark';
      renderColor(mode);
      save(COLOR_KEY, mode);
    });
  });
  document.querySelectorAll('[data-design-toggle]').forEach(button => {
    button.addEventListener('click', () => {
      const design = root.dataset.design === 'terminal' ? 'command' : 'terminal';
      renderDesign(design);
      save(DESIGN_KEY, design);
    });
  });

  // Keep other open tabs in step.
  window.addEventListener('storage', event => {
    if (event.key === COLOR_KEY || event.key === null) renderColor(event.newValue === 'light' ? 'light' : 'dark');
    if (event.key === DESIGN_KEY || event.key === null) renderDesign(event.newValue === 'terminal' ? 'terminal' : 'command');
  });
})();
