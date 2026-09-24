const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');

// Head initializer: Command Center dark by default; saved values apply; bad or blocked storage is safe.
const init = read('assets/theme/init.js');
function runInit(saved, blocked = false) {
  const html = { dataset: {}, style: {} };
  vm.runInNewContext(init, { document: { documentElement: html }, localStorage: { getItem(key) { if (blocked) throw Error('blocked'); return saved[key] ?? null; } } });
  return { design: html.dataset.design, color: html.dataset.colorMode, scheme: html.style.colorScheme };
}
assert.deepEqual(runInit({}), { design: 'command', color: 'dark', scheme: 'dark' });
assert.deepEqual(runInit({ 'droidrooter-design': 'terminal', 'droidrooter-color-mode': 'light' }), { design: 'terminal', color: 'light', scheme: 'light' });
assert.deepEqual(runInit({ 'droidrooter-design': 'bogus', 'droidrooter-color-mode': 'purple' }), { design: 'command', color: 'dark', scheme: 'dark' });
assert.doesNotThrow(() => runInit({}, true));
assert.deepEqual(runInit({}, true), { design: 'command', color: 'dark', scheme: 'dark' });

// Controller: both toggles update the root, labels, pressed state and storage.
function fakeButton(labelAttr) {
  const attrs = {}; const label = { textContent: '' }; let handler = null;
  return { attrs, label, title: '', setAttribute(k, v) { attrs[k] = v; }, querySelector(sel) { return sel === labelAttr ? label : null; },
    addEventListener(type, fn) { if (type === 'click') handler = fn; }, click() { handler(); } };
}
const color = fakeButton('[data-theme-label]'); const design = fakeButton('[data-design-label]'); const group = { hidden: true };
const store = {}; const html = { dataset: { design: 'command', colorMode: 'dark' }, style: {} };
const doc = { documentElement: html, querySelectorAll(sel) { return sel === '[data-theme-toggle]' ? [color] : sel === '[data-design-toggle]' ? [design] : sel === '[data-theme-controls]' ? [group] : []; } };
vm.runInNewContext(read('assets/theme/toggle.js'), { document: doc, localStorage: { setItem(k, v) { store[k] = v; } }, window: { addEventListener() {} } });
assert.equal(group.hidden, false);
assert.equal(color.attrs['aria-pressed'], 'true'); assert.equal(color.label.textContent, 'Light');
assert.equal(design.label.textContent, 'Terminal');
color.click();
assert.equal(html.dataset.colorMode, 'light'); assert.equal(html.style.colorScheme, 'light');
assert.equal(color.attrs['aria-pressed'], 'false'); assert.equal(store['droidrooter-color-mode'], 'light');
design.click();
assert.equal(html.dataset.design, 'terminal'); assert.equal(design.label.textContent, 'Command');
assert.match(design.attrs['aria-label'], /^Design: Terminal\./); assert.equal(store['droidrooter-design'], 'terminal');

// Variant stylesheets are gated to their design and load nothing remote.
for (const [file, gate] of [['assets/theme/command.css', 'html[data-design=command]'], ['assets/theme/terminal.css', 'html[data-design=terminal]']]) {
  const css = read(file);
  const rules = css.split('}').map(r => r.trim()).filter(r => r && !r.startsWith('/*') && !r.startsWith('@media'));
  for (const rule of rules) { const selector = rule.split('{')[0].replace(/^.*\{/, '').trim(); if (selector) assert.ok(selector.startsWith(gate), `${file}: ungated rule ${selector}`); }
  assert.doesNotMatch(css, /https?:\/\//);
}
console.log('PASS: defaults, saved/invalid/blocked storage, both toggles, gated variants');
