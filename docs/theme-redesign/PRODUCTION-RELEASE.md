# Terminal · Light / Command Center · Dark production release

## Refs

- Baseline (production `main` when the build started): `fb7907c0ccad175eae98f6c58267a33d358b82cd`
- Backup branch `backup/main-before-dual-theme-2026-09-24`: `f41d1ef8fe61bb4478458f91b803f732ac1cfef6` (left untouched; it predates the `fb7907c` console fix)
- Integration branch: `feature/dual-theme-production`

## What changed

- Dark mode uses the Command Center design; light mode uses the Terminal design. First visits get dark (Command Center).
- One dark/light switch in the navigation (or floating on pages without one) changes both together. The choice is stored per browser (`droidrooter-color-mode`) and applied before first paint.
- Revisions: the first release had a separate design toggle (any design in any mode); the second briefly used Command Center for both modes. Both were corrected. A `droidrooter-design` value saved by the first release is cleared on the next visit.
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
| Content and SEO (`audit-theme.py`, against current `main` and against pre-theme `fb7907c`) | 0 differences on public pages after removing marker-delimited additions: titles, meta, canonicals, structured data, headings, text and links |
| Protected files | `sitemap.xml`, `robots.txt`, `manifest.json`, `drvcam/control/_headers`, console assets and manifest identical to baseline |
| Internal links and anchors | 0 missing targets, 0 missing fragments |
| Unit tests (`tests/theme.test.cjs`) | Dark = Command Center, light = Terminal, dark default, saved, invalid and blocked storage, switch, gated stylesheets |
| Browser audit (`browser-audit.cjs`) | 161 pages, 638 rendered states (dark and light at 1440 and 390 px); 0 overflow, covered controls, invisible text, script errors or missing assets on themed pages |
| Redirects | 18/18 reach their targets |
| Interactions | Mobile menu, keyboard toggles, preferences across navigation, FAQ, code copy, rootability checker, console contrast, blocked storage, JavaScript disabled |
| 320 px sweep (all public pages vs baseline) | 0 new overflows; 27 baseline overflows fixed |
| Idempotence | Re-running `apply-theme.py` produces no diff |

Not run: Lighthouse (not available in the build environment). Added weight per themed page is three small stylesheets and two small scripts from the same origin.

## Rollback

Revert the theme commits on `main` (`git revert 504cf2d 6a8801f 6a25a96`, newest first). Do not reset `main` to an older commit: Codex has published console fixes on top of the theme since, and a reset would remove them. The backup branch predates the `fb7907c` console fix as well.
