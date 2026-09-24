/* Apply the saved color mode before first paint. The site uses the Command Center
   design in both modes; first visits get dark. */
(() => {
  const root = document.documentElement;
  let mode = 'dark';
  try {
    if (localStorage.getItem('droidrooter-color-mode') === 'light') mode = 'light';
    // A design choice saved by an earlier release no longer applies.
    localStorage.removeItem('droidrooter-design');
  } catch (_) { /* Storage may be unavailable in private or embedded browsers. */ }
  root.dataset.design = 'command';
  root.dataset.colorMode = mode;
  root.style.colorScheme = mode;
})();
