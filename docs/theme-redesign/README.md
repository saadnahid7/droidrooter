# Terminal theme — first branch

Branch: `design/terminal-light`
Baseline: `f1a24af692a7e63722394657ef6728616b655716`

## Delivered

- Terminal-inspired typography, spacing, cards and green palette across the public site and the existing dashboard shells.
- Light/dark button in the public header; floating control on the dashboard.
- Dark is the default for new visitors, regardless of OS preference. An explicit choice is saved under `droidrooter-color-mode` and applied before paint on subsequent pages. Blocked storage is handled. Without JavaScript the site stays dark and the inactive toggle stays hidden.
- Responsive fixes for four existing plain article tables and portfolio cards; dashboard primary-button contrast corrected after independent code review.
- Existing HTML content, navigation destinations, images, scripts, metadata and JSON-LD preserved. The 18 redirect stubs remain byte-for-byte unchanged.
- No edits to sitemap, robots, manifest, dashboard security headers, deployment settings, backend/API logic or the main branch.
- Command Center is deferred at the user's request. Only this branch is intended to be pushed in this session.

## Verification

| Check | Result |
|---|---|
| HTML inventory and preservation | 180 documents, zero content/metadata preservation errors |
| Rendered pages | 162 non-redirect documents, including 15 dashboard entry shells |
| Browser states | 648: every page at 1440px and 390px in dark and light |
| Browser errors / missing local assets | Zero |
| Page horizontal overflow after fixes | Zero |
| Exact foreground/background collision check | Zero on checked text/control elements |
| Broken loaded images | Zero |
| Legacy redirects | 18/18 resolve to their intended destinations |
| Local links, assets and fragments | Zero unresolved targets |
| Existing repository routing suite | 146 canonical URLs, 741 valid JSON-LD blocks |
| Default and remembered mode | Passed on all 162 rendered pages |
| Keyboard toggle, cross-page preference, blocked storage, no-JS fallback | Passed |
| Mobile menu and Escape, article FAQ, code-copy control, device search | Exercised successfully |
| Code review | Important contrast finding fixed and re-reviewed |

Raw route-by-route evidence is in `static-audit.json` and `browser-audit.json`.

### Verification limits

This is a local Chromium review, not a claim of universal browser/accessibility certification. External analytics, Google Fonts and API requests were blocked during browser tests. Font fallbacks were rendered. Existing external URLs were preserved, not exhaustively live-crawled. Dashboard routes were reviewed as unauthenticated login entry points; authenticated business operations and real form submissions were not exercised. The API-unavailable message in the isolated dashboard test is expected from blocked external requests. Render preview/deployment was not created or changed; production HTTP redirect/header behavior depends on existing Render configuration.

## Reproduce

No application build or package installation is needed: this repository is the generated static site.

```sh
node .droidrooter/tests/theme.test.cjs
python .droidrooter/test-routing.py
python .droidrooter/audit-theme.py
# Install Playwright and a Chromium binary in your test environment, then:
PLAYWRIGHT_MODULE=/absolute/path/to/playwright \
CHROMIUM_PATH=/absolute/path/to/chromium \
node .droidrooter/browser-audit.cjs
```

The browser script runs a temporary local server and does not submit forms or mutate backend data.

After upstream regeneration adds/replaces HTML, rerun `python .droidrooter/apply-theme.py`, then repeat the audits. The installer skips redirect stubs and already themed HTML. Shared theme files live in `assets/theme/`. Deploy this branch only through an explicitly selected Render service/preview; merging it into the production branch is a separate decision.
