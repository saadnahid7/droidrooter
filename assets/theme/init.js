/* Apply saved design and color before first paint. First visits get Command Center, dark. */
(() => {
  const root = document.documentElement;
  const read = key => {
    try { return localStorage.getItem(key); } catch (_) { return null; }
  };
  root.dataset.design = read('droidrooter-design') === 'terminal' ? 'terminal' : 'command';
  root.dataset.colorMode = read('droidrooter-color-mode') === 'light' ? 'light' : 'dark';
  root.style.colorScheme = root.dataset.colorMode;
})();
