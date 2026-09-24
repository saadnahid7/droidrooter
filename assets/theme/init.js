/* Apply the saved mode before first paint. Dark uses the Command Center design,
   light uses the Terminal design. First visits get dark. */
(() => {
  const root = document.documentElement;
  let mode = 'dark';
  try {
    if (localStorage.getItem('droidrooter-color-mode') === 'light') mode = 'light';
    // The design follows the mode; a separate design choice from an earlier release no longer applies.
    localStorage.removeItem('droidrooter-design');
  } catch (_) { /* Storage may be unavailable in private or embedded browsers. */ }
  root.dataset.design = mode === 'light' ? 'terminal' : 'command';
  root.dataset.colorMode = mode;
  root.style.colorScheme = mode;
})();
