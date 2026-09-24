(() => {
  const root = document.documentElement;
  const buttons = document.querySelectorAll('[data-theme-toggle]');
  function render(mode) {
    root.dataset.colorMode = mode;
    root.style.colorScheme = mode;
    buttons.forEach(button => {
      const dark = mode === 'dark';
      button.setAttribute('aria-pressed', String(dark));
      button.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
      button.title = dark ? 'Switch to light theme' : 'Switch to dark theme';
      button.querySelector('[data-theme-label]').textContent = dark ? 'Light' : 'Dark';
    });
  }
  render(root.dataset.colorMode === 'light' ? 'light' : 'dark');
  buttons.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
      const mode = root.dataset.colorMode === 'dark' ? 'light' : 'dark';
      render(mode);
      try { localStorage.setItem('droidrooter-color-mode', mode); } catch (_) {}
    });
  });
  window.addEventListener('storage', event => {
    if (event.key === 'droidrooter-color-mode' || event.key === null) {
      render(event.newValue === 'light' ? 'light' : 'dark');
    }
  });
})();
