const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');

// Head initializer: always Command Center; dark by default; saved light applies; bad or blocked storage is safe.
const init = read('assets/theme/init.js');
function runInit(saved, blocked = false) {
  const html = { dataset: {}, style: {} }; const removed = [];
  vm.runInNewContext(init, { document: { documentElement: html }, localStorage: {
    getItem(key) { if (blocked) throw Error('blocked'); return saved[key] ?? null; },
    removeItem(key) { if (blocked) throw Error('blocked'); removed.push(key); } } });
  return { design: html.dataset.design, color: html.dataset.colorMode, scheme: html.style.colorScheme, removed };
}
assert.deepEqual(runInit({}), { design: 'command', color: 'dark', scheme: 'dark', removed: ['droidrooter-design'] });
assert.equal(runInit({ 'droidrooter-color-mode': 'light' }).color, 'light');
// A Terminal choice saved by the earlier release no longer changes the design.
assert.equal(runInit({ 'droidrooter-design': 'terminal' }).design, 'command');
assert.equal(runInit({ 'droidrooter-color-mode': 'purple' }).color, 'dark');
assert.doesNotThrow(() => runInit({}, true));
assert.deepEqual(runInit({}, true), { design: 'command', color: 'dark', scheme: 'dark', removed: [] });

// Switch: updates root, label, pressed state and storage.
const attrs = {}; const label = { textContent: '' }; let click = null; const group = { hidden: true }; const store = {};
const button = { title: '', setAttribute(k, v) { attrs[k] = v; }, querySelector(sel) { return sel === '[data-theme-label]' ? label : null; }, addEventListener(t, fn) { if (t === 'click') click = fn; } };
const html = { dataset: { design: 'command', colorMode: 'dark' }, style: {} };
const doc = { documentElement: html, querySelectorAll(sel) { return sel === '[data-theme-toggle]' ? [button] : sel === '[data-theme-controls]' ? [group] : []; } };
vm.runInNewContext(read('assets/theme/toggle.js'), { document: doc, localStorage: { setItem(k, v) { store[k] = v; } }, window: { addEventListener() {} } });
assert.equal(group.hidden, false); assert.equal(attrs['aria-pressed'], 'true'); assert.equal(label.textContent, 'Light');
click();
assert.equal(html.dataset.colorMode, 'light'); assert.equal(html.style.colorScheme, 'light'); assert.equal(html.dataset.design, 'command');
assert.equal(attrs['aria-pressed'], 'false'); assert.equal(label.textContent, 'Dark'); assert.equal(store['droidrooter-color-mode'], 'light');
click(); assert.equal(html.dataset.colorMode, 'dark');

// Only the Command Center stylesheet exists; it is gated and loads nothing remote.
assert.ok(!fs.existsSync(path.join(root, 'assets/theme/terminal.css')), 'Terminal stylesheet must be removed');
const css = read('assets/theme/command.css');
for (const rule of css.split('}').map(r => r.trim()).filter(r => r && !r.startsWith('/*') && !r.startsWith('@media'))) {
  const selector = rule.split('{')[0].replace(/^.*\{/, '').trim();
  if (selector) assert.ok(selector.startsWith('html[data-design=command]'), `ungated rule ${selector}`);
}
assert.doesNotMatch(css, /https?:\/\//);
console.log('PASS: Command Center only, dark default, saved/invalid/blocked storage, dark/light switch');
