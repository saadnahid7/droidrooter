# DroidRooter Dual Theme Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Back up the current production commit, combine Command Center and Terminal into one fast selectable theme system, verify every route, and publish the verified commit to `main`.

**Architecture:** Start from the current production commit on `feature/dual-theme-production`. Preserve HTML content and SEO by applying marker-delimited presentation additions only. A head initializer applies independent design and color preferences before paint; a deferred controller updates accessible controls. Shared CSS provides color tokens and control styling, while two selector-gated variant files provide the designs.

**Tech Stack:** Static HTML/CSS/JavaScript, Python 3 audit tooling, Node.js tests, Playwright/Chromium browser audit, Lighthouse, Git/GitHub, Render static hosting.

**Spec:** `docs/superpowers/specs/2026-09-24-dual-theme-production-design.md`

## Global Constraints

- Production baseline is `f41d1ef8fe61bb4478458f91b803f732ac1cfef6`.
- Backup branch is `backup/main-before-dual-theme-2026-09-24` and must remain pinned to the baseline.
- First visit defaults to `data-design="command"` and `data-color-mode="dark"`.
- Valid design values are exactly `command` and `terminal`; valid color values are exactly `dark` and `light`.
- Do not change visible content, routes, headings, SEO metadata, structured data, internal links, sitemap, robots.txt, manifest, redirects, or the current DRVCAM bundle.
- Add no framework, remote font, image, analytics script, animation library, or third-party runtime asset.
- Production update is blocked by content/SEO differences, new broken targets, browser errors, serious accessibility errors, or material performance regression.

## Review Focus

- Invalid or inaccessible localStorage must produce Command Center dark without throwing.
- A saved design and color combination must apply before first paint on direct navigation.
- Controls must remain keyboard accessible and accurately expose selected state at narrow mobile widths.
- Redirect documents and the authenticated DRVCAM console must retain their original behavior.
- Re-running the installer must not duplicate theme assets, controls, or markers.

---

### Task 1: Preserve Production and Establish the Integration Baseline

**Files:**
- Existing: Git refs only
- Verify: `docs/superpowers/specs/2026-09-24-dual-theme-production-design.md`

**Interfaces:**
- Consumes: GitHub `main` at the baseline SHA.
- Produces: immutable backup ref and isolated integration checkout.

- [ ] **Step 1: Verify production has not advanced**

Run:
```bash
git fetch origin main feature/dual-theme-production
test "$(git rev-parse origin/main)" = "f41d1ef8fe61bb4478458f91b803f732ac1cfef6"
git status --short
```
Expected: the SHA comparison succeeds and the checkout has no unrelated changes.

- [ ] **Step 2: Create and verify the backup branch**

Run:
```bash
git push origin f41d1ef8fe61bb4478458f91b803f732ac1cfef6:refs/heads/backup/main-before-dual-theme-2026-09-24
test "$(git ls-remote origin refs/heads/backup/main-before-dual-theme-2026-09-24 | cut -f1)" = "f41d1ef8fe61bb4478458f91b803f732ac1cfef6"
```
Expected: remote backup SHA exactly matches the production baseline.

- [ ] **Step 3: Enter an isolated worktree**

Run:
```bash
git worktree add .worktrees/dual-theme feature/dual-theme-production
cd .worktrees/dual-theme
git status --short --branch
```
Expected: clean `feature/dual-theme-production` checkout.

### Task 2: Implement Independent Design and Color State

**Files:**
- Create: `assets/theme/command.css`
- Create: `assets/theme/terminal.css`
- Modify: `assets/theme/base.css`
- Modify: `assets/theme/init.js`
- Modify: `assets/theme/toggle.js`
- Test: `.droidrooter/tests/theme.test.cjs`

**Interfaces:**
- Consumes: localStorage keys `droidrooter-design` and `droidrooter-color-mode`.
- Produces: root `data-design` and `data-color-mode`; controls with `data-theme-design` and `data-theme-color`.

- [ ] **Step 1: Add failing state tests**

Add Node tests that execute the initializer with empty, valid, invalid, and throwing storage. Required assertions:
```js
assert.equal(root.dataset.design, 'command');
assert.equal(root.dataset.colorMode, 'dark');
assert.deepEqual(runWith({design:'terminal', color:'light'}), {
  design: 'terminal', colorMode: 'light'
});
assert.doesNotThrow(() => runWithThrowingStorage());
```
Add controller tests that click each option, verify root attributes, verify `aria-pressed`, and verify both storage keys.

- [ ] **Step 2: Run the tests and confirm failure**

Run:
```bash
node --test .droidrooter/tests/theme.test.cjs
```
Expected: failure because design selection and dual controls do not exist.

- [ ] **Step 3: Implement the head initializer**

Implement this behavior in `assets/theme/init.js`:
```js
(() => {
  const root = document.documentElement;
  const read = key => {
    try { return localStorage.getItem(key); } catch (_) { return null; }
  };
  const design = read('droidrooter-design');
  const color = read('droidrooter-color-mode');
  root.dataset.design = design === 'terminal' ? 'terminal' : 'command';
  root.dataset.colorMode = color === 'light' ? 'light' : 'dark';
  root.style.colorScheme = root.dataset.colorMode;
})();
```

- [ ] **Step 4: Implement accessible controls and persistence**

Use two grouped controls: Command Center/Terminal and Dark/Light. On activation, set the matching root attribute, persist the valid value, synchronize every copy of the control on the page, update `aria-pressed`, and dispatch no navigation. Catch storage failures.

- [ ] **Step 5: Separate variant CSS**

Move existing Command Center rules into `command.css` under selectors beginning `:root[data-design=command]`. Move existing Terminal rules into `terminal.css` under `:root[data-design=terminal]`. Keep palettes, typography safeguards, focus treatment, and selector control layout in `base.css`. Remove blur-heavy and continuously animated effects.

- [ ] **Step 6: Run state and CSS contract tests**

Run:
```bash
node --test .droidrooter/tests/theme.test.cjs
```
Expected: all tests pass; CSS contract test confirms both variant files are selector-gated and contain no remote URLs.

- [ ] **Step 7: Commit**

Run:
```bash
git add assets/theme .droidrooter/tests/theme.test.cjs
git commit -m "feat: add selectable design and color themes"
```

### Task 3: Integrate the Selector Across Public Pages Idempotently

**Files:**
- Modify: `.droidrooter/apply-theme.py`
- Modify: all eligible public `*.html`
- Test: `.droidrooter/tests/theme.test.cjs`

**Interfaces:**
- Consumes: marker-free or previously themed public HTML.
- Produces: exactly one initializer, asset block, and dual selector per nonredirect public document.

- [ ] **Step 1: Add an idempotence test**

Copy a representative document to a temporary directory, run the installer twice, and assert:
```js
assert.equal(count(html, 'data-dr-theme-init'), 1);
assert.equal(count(html, 'data-theme-design'), 2);
assert.equal(count(html, 'data-theme-color'), 2);
assert.equal(count(html, '/assets/theme/command.css'), 1);
assert.equal(count(html, '/assets/theme/terminal.css'), 1);
```
Also assert a redirect fixture stays byte identical.

- [ ] **Step 2: Run the test and confirm failure**

Run:
```bash
node --test .droidrooter/tests/theme.test.cjs
```

- [ ] **Step 3: Update the installer**

The installer must first remove each existing `dr-theme-*:start/end` block and root theme attributes, then insert:

```html
<!-- dr-theme-head:start --><script data-dr-theme-init src="/assets/theme/init.js"></script><!-- dr-theme-head:end -->
<!-- dr-theme-assets:start --><link rel="stylesheet" href="/assets/theme/base.css"><link rel="stylesheet" href="/assets/theme/command.css"><link rel="stylesheet" href="/assets/theme/terminal.css"><script src="/assets/theme/toggle.js" defer></script><!-- dr-theme-assets:end -->
```

Insert one compact fieldset containing four buttons with visible labels and `aria-pressed`. Skip documents containing an HTTP refresh redirect.

- [ ] **Step 4: Apply the installer**

Run:
```bash
python3 .droidrooter/apply-theme.py
python3 .droidrooter/apply-theme.py
```
Expected: the second run produces no Git diff.

- [ ] **Step 5: Run integration tests**

Run:
```bash
node --test .droidrooter/tests/theme.test.cjs
```
Expected: all state, asset, control, and idempotence tests pass.

- [ ] **Step 6: Commit**

Run:
```bash
git add .droidrooter/apply-theme.py .droidrooter/tests/theme.test.cjs '*.html' '*/**/*.html'
git commit -m "feat: install dual theme controls across public pages"
```

### Task 4: Preserve and Bridge the DRVCAM Console

**Files:**
- Modify: `assets/theme/dashboard-bridge.js`
- Modify: `assets/theme/dashboard-bridge.css`
- Modify: 14 `drvcam/control/**/index.html` shells
- Test: `.droidrooter/tests/theme.test.cjs`

**Interfaces:**
- Consumes: shared color preference and native `drvcam.admin.theme`.
- Produces: dark-first sign-in control; authenticated console continues using its native menu.

- [ ] **Step 1: Add console preservation tests**

For every console shell, strip marker blocks and root theme attributes, normalize line endings, and compare with the baseline blob. Assert unchanged module script, hashed stylesheet, robots `noindex`, title, CSP/header file, and route count of 14.

- [ ] **Step 2: Add bridge behavior tests**

Assert public `light` initializes console light, missing preferences initialize dark, sign-in control updates both storage keys, and the floating control hides after `.login-card` disappears.

- [ ] **Step 3: Run tests and confirm any missing behavior fails**

Run:
```bash
node --test .droidrooter/tests/theme.test.cjs
```

- [ ] **Step 4: Implement the bridge and shell markers**

Load the bridge before the console module. Add the bridge stylesheet once and the hidden sign-in control once. Observe the console root to show the control only on the login view and synchronize native theme changes back to `droidrooter-color-mode`.

- [ ] **Step 5: Run tests**

Run:
```bash
node --test .droidrooter/tests/theme.test.cjs
```
Expected: console behavior and baseline preservation checks pass.

- [ ] **Step 6: Commit**

Run:
```bash
git add assets/theme/dashboard-bridge.* drvcam/control .droidrooter/tests/theme.test.cjs
git commit -m "feat: align DRVCAM sign-in color preference"
```

### Task 5: Run the Full Static Content, SEO, and Route Audit

**Files:**
- Modify: `.droidrooter/audit-theme.py`
- Create: `docs/theme-redesign/production-static-audit.json`

**Interfaces:**
- Consumes: baseline commit and candidate worktree.
- Produces: machine-readable audit with all routes and errors.

- [ ] **Step 1: Update normalization and required controls**

Normalize only marker-delimited additions plus `data-design` and `data-color-mode`. Require exactly one initializer/assets block and one selector on each eligible page. Keep baseline comparisons for titles, meta tags, canonical, structured data, visible text, headings, links, and protected files.

- [ ] **Step 2: Run the static audit**

Run:
```bash
python3 .droidrooter/audit-theme.py
```
Expected summary:
```json
{
  "html_pages": 179,
  "redirect_pages": 18,
  "application_shells": 14,
  "preservation_errors": [],
  "new_missing_local_targets": [],
  "new_missing_fragments": []
}
```

- [ ] **Step 3: Verify protected files directly**

Run:
```bash
git diff --exit-code f41d1ef8fe61bb4478458f91b803f732ac1cfef6 -- sitemap.xml robots.txt manifest.json drvcam/control/_headers
```
Expected: no diff.

- [ ] **Step 4: Commit**

Run:
```bash
git add .droidrooter/audit-theme.py docs/theme-redesign/production-static-audit.json
git commit -m "test: audit dual theme content and SEO preservation"
```

### Task 6: Browser, Accessibility, and Performance Verification

**Files:**
- Modify: `.droidrooter/browser-audit.cjs`
- Create: `docs/theme-redesign/production-browser-audit.json`
- Create: `docs/theme-redesign/production-performance-audit.json`

**Interfaces:**
- Consumes: locally served baseline and candidate builds.
- Produces: route-by-route browser report and baseline/candidate performance comparison.

- [ ] **Step 1: Extend the browser matrix**

For 161 nonredirect routes, test four combinations at 390×844 and 1440×900: Command dark, Command light, Terminal dark, Terminal light. That is 1,288 render states. For each state assert successful response, no failed local asset, no browser error, correct root attributes, visible selector, no horizontal overflow, and no element collision covering the main heading or primary navigation.

- [ ] **Step 2: Run the browser audit**

Run:
```bash
node .droidrooter/browser-audit.cjs
```
Expected: 1,288/1,288 render states pass and 18/18 redirects resolve to their expected targets.

- [ ] **Step 3: Run automated accessibility checks**

On home, blog index, one long article, services index, contact, 404, and DRVCAM sign-in in all four theme states, verify keyboard traversal, visible focus, control names/states, document landmarks, and WCAG AA text contrast. Record zero serious or critical violations.

- [ ] **Step 4: Compare representative Lighthouse runs**

Serve an untouched baseline worktree and candidate worktree with identical local server settings. Run three mobile Lighthouse passes per route for home, services index, blog index, long article, and 404. Record medians for performance score, LCP, CLS, total blocking time, request count, and transferred bytes.

Acceptance: no candidate route loses more than 3 performance-score points, adds more than 100 ms median blocking time, adds more than 0.02 CLS, or regresses LCP by more than 10%. If a threshold is crossed, optimize and repeat all affected runs.

- [ ] **Step 5: Commit reports and audit runner**

Run:
```bash
git add .droidrooter/browser-audit.cjs docs/theme-redesign/production-browser-audit.json docs/theme-redesign/production-performance-audit.json
git commit -m "test: verify dual themes across routes and viewports"
```

### Task 7: Final Review, Publish, and Live Smoke Test

**Files:**
- Create: `docs/theme-redesign/PRODUCTION-RELEASE.md`

**Interfaces:**
- Consumes: verified integration commit and audit reports.
- Produces: updated `main`, Render deployment confirmation, and rollback record.

- [ ] **Step 1: Run the complete verification suite fresh**

Run:
```bash
node --test .droidrooter/tests/theme.test.cjs
python3 .droidrooter/audit-theme.py
node .droidrooter/browser-audit.cjs
git diff --check
git status --short
```
Expected: all tests and audits pass; only generated release documentation may be uncommitted.

- [ ] **Step 2: Review the complete production diff**

Run:
```bash
git diff --stat f41d1ef8fe61bb4478458f91b803f732ac1cfef6..HEAD
git diff --name-status f41d1ef8fe61bb4478458f91b803f732ac1cfef6..HEAD
```
Verify every changed path belongs to theme assets, marker-delimited HTML integration, audit tooling/reports, or design documentation.

- [ ] **Step 3: Record release evidence**

Write `PRODUCTION-RELEASE.md` with baseline SHA, backup SHA, integration SHA, route counts, browser-state counts, redirect checks, accessibility results, Lighthouse medians, protected-file checks, and rollback command.

- [ ] **Step 4: Commit the release record**

Run:
```bash
git add docs/theme-redesign/PRODUCTION-RELEASE.md
git commit -m "docs: record dual theme production verification"
```

- [ ] **Step 5: Reconfirm main and backup refs, then update production**

Run:
```bash
test "$(git ls-remote origin refs/heads/main | cut -f1)" = "f41d1ef8fe61bb4478458f91b803f732ac1cfef6"
test "$(git ls-remote origin refs/heads/backup/main-before-dual-theme-2026-09-24 | cut -f1)" = "f41d1ef8fe61bb4478458f91b803f732ac1cfef6"
git push origin HEAD:main
```
Expected: fast-forward production update.

- [ ] **Step 6: Verify Render deployment and live pages**

Wait for the deployment tied to the new main SHA. Check live home, blog index, one long article, services index, 404, and DRVCAM sign-in. Confirm both design choices, both color choices, persistence across navigation, no console errors, correct canonical/meta data, and successful local assets.

- [ ] **Step 7: Report completion**

Provide links to `main`, the backup branch, integration history, audit reports, and release record. Include exact test counts and Lighthouse medians. If Render has not deployed or a live check fails, report the active blocker and keep the backup untouched.
