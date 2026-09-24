# Dual theme production release

## Refs

- Baseline (production `main` when the build started): `fb7907c0ccad175eae98f6c58267a33d358b82cd`
- Backup branch `backup/main-before-dual-theme-2026-09-24`: `f41d1ef8fe61bb4478458f91b803f732ac1cfef6` (left untouched; it predates the `fb7907c` console fix)
- Integration branch: `feature/dual-theme-production`

## What changed

- Two designs, Command Center and Terminal, each in dark and light. First visits get Command Center, dark.
- One control group in the navigation (or floating on pages without one): a design toggle and a dark/light toggle. Both preferences are stored per browser (`droidrooter-design`, `droidrooter-color-mode`) and applied before first paint.
- Design stylesheets are selector-gated: `command.css` only matches `html[data-design=command]`, `terminal.css` only `html[data-design=terminal]`.
- Literal colours in site CSS, `<style>` blocks and `style=""` attributes were converted to theme tokens that keep the original colour as the fallback.
- DRVCAM console shells load only the sign-in colour bridge. The console bundle, its CSS, `_headers` and manifest are unchanged; signed-in staff keep the console's own theme menu.
- Narrow phones: service and blog cards now shrink with the viewport, which removes horizontal scrolling that 27 pages had at 320px on the baseline.

## Excluded on purpose

These three articles are byte-identical to the baseline and carry no theme controls; the owner will update them manually:

- `blog/monitor-teen-android-without-them-knowing-legal-guide/`
- `blog/mspy-vs-bark-vs-qustodio-comparison/`
- `blog/parental-control-app-detection-and-removal/`

They share the tokenised blog stylesheet, whose fallbacks keep their original colours. A pixel comparison against the baseline shows a maximum difference of 3/255 in one channel on about 1% of pixels (edges of translucent glows), from rounding 8-bit alpha to a percentage. Two of them already scroll sideways on phones on the baseline (a wide table); that is unchanged.

## Verification

| Check | Result |
|---|---|
| Route inventory | 179 HTML files: 144 themed public pages, 14 console shells, 18 redirects, 3 excluded |
| Content and SEO (`audit-theme.py`) | 0 differences after removing marker-delimited additions: titles, meta, canonicals, structured data, headings, text and links |
| Protected files | `sitemap.xml`, `robots.txt`, `manifest.json`, `drvcam/control/_headers`, console assets and manifest identical to baseline |
| Internal links and anchors | 0 missing targets, 0 missing fragments |
| Unit tests (`tests/theme.test.cjs`) | Defaults, saved, invalid and blocked storage, both toggles, gated variants |
| Browser audit (`browser-audit.cjs`) | 161 pages, 1,214 rendered states (public pages: 2 designs x 2 colours x 1440/390 px); 0 overflow, covered controls, invisible text, script errors or missing assets on themed pages |
| Redirects | 18/18 reach their targets |
| Interactions | Mobile menu, keyboard toggles, preferences across navigation, FAQ, code copy, rootability checker, console contrast, blocked storage, JavaScript disabled |
| 320 px sweep (all public pages vs baseline) | 0 new overflows; 27 baseline overflows fixed |
| Idempotence | Re-running `apply-theme.py` produces no diff |

Not run: Lighthouse (not available in the build environment). Added weight per themed page is three small stylesheets and two small scripts from the same origin.

## Rollback

`git revert` the integration merge on `main`, or reset `main` to `fb7907c0ccad175eae98f6c58267a33d358b82cd`. Do not reset to the backup branch: it predates the `fb7907c` console fix.
