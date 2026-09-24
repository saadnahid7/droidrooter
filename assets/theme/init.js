/* Apply before page paint; first visits intentionally default to dark. */
(() => {
  let mode = 'dark';
  try {
    const saved = localStorage.getItem('droidrooter-color-mode');
    if (saved === 'light' || saved === 'dark') mode = saved;
  } catch (_) { /* Storage may be unavailable in private/embedded browsers. */ }
  document.documentElement.dataset.design = 'command';
  document.documentElement.dataset.colorMode = mode;
  document.documentElement.style.colorScheme = mode;
})();
