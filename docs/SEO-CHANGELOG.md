# DroidRooter SEO Change Log

**Purpose:** Record every SEO-affecting change before and after publication. This file is an internal working document and must not be linked from the public site.

## Rules

- Preserve the existing framework and generated design system.
- Check `.droidrooter/protected-page-registry.jsonc` before editing any page.
- Tier A pages are additive-only: do not change their title, H1, URL, body order, or existing copy without an explicit approved migration.
- Never invent GSC measurements. Leave unknown fields as `TBD`.
- Never future-date an entry or content.
- Record rollback steps before deployment.
- Recheck title, H1, canonical, schema, links, robots, sitemap membership, and rendered output after a change.

## Reusable entry template

| date | URL | page tier | change type | exact files changed | reason | pre-change GSC clicks/impressions/CTR/position | post-change field to fill later | rollback note |
|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | `/example/` | A / B / C | additive / metadata / redirect / internal-link / correction | `path/to/file` | Owner-approved reason | TBD unless supplied | Fill after a comparable GSC window | Restore the named files and regenerate/deploy the prior artifact |

## Baseline supplied for this repository

The only supplied GSC baseline is an aggregate window, not a URL-level baseline:

- **Window:** 2026-05-14 through 2026-08-13
- **Clicks:** 4,883
- **Impressions:** 291,779
- **CTR:** 1.67%
- **Average position:** approximately 9.3 overall

Do not copy these aggregate figures into a URL-specific changelog row.

## Pre-publication checklist

- [ ] Protected-page registry checked
- [ ] Exact URL and page tier recorded
- [ ] Source/build repository available, or static-artifact limitation documented
- [ ] Owner facts verified and linked in the facts registry
- [ ] No unsupported compatibility, price, turnaround, trust, warranty, staff, or business claims added
- [ ] Title and meta description checked
- [ ] Canonical and redirect behavior checked
- [ ] Schema matches rendered content
- [ ] Internal links resolve
- [ ] Sitemap and robots behavior checked
- [ ] Rollback note written

## Post-publication fields

For each entry, record the first comparable GSC window after enough time has passed:

- URL clicks:
- URL impressions:
- URL CTR:
- URL average position:
- Indexing/coverage observations:
- User/conversion observations:
- Follow-up decision:

## 2026-08-27 — Technical URL and date normalization

| date | URL | page tier | change type | exact files changed | reason | pre-change GSC clicks/impressions/CTR/position | post-change field to fill later | rollback note |
|---|---|---|---|---|---|---|---|---|
| 2026-08-27 | Sitewide technical files and generated date references | Mixed; Tier A protected | redirects, canonical alignment, sitemap cleanup, date correction | nginx rules in `/etc/nginx/conf.d/droidrooter.conf` on the VPS (reference copy: `.droidrooter/nginx-droidrooter.conf`); `404.html`; `sitemap.xml`; removed `sitemap-0.xml` and `sitemap-index.xml`; 32 generated HTML files containing future date references; `.droidrooter/normalize-generated-site.py`; `.droidrooter/test-routing.py`; `docs/HIGH-RISK-CONSOLIDATION-CANDIDATES.md` | Consolidate low-risk duplicate URL forms, align the sitemap with existing no-slash canonicals, remove a self-canonical from the noindex 404 page, and replace future dates with the earliest Git-supported repository date | Aggregate baseline only: 4,883 clicks / 291,779 impressions / 1.67% CTR / approximately position 9.3. No URL-level values supplied. | Compare canonical coverage, redirected-alias indexing, and affected landing-page GSC performance after a comparable period | Restore the prior sitemap files and generated HTML from the pre-change Git revision; restore the prior nginx conf and reload; redeploy the prior artifact |

### Exact permanent aliases added

- Homepage: `/index`, `/index/`, `/index.html`, `/index.php` → `/`
- Core `.html` aliases: `/about.html`, `/blog.html`, `/contact.html`, `/faq.html`, `/glossary.html`, `/how-it-works.html`, `/locations.html`, `/portfolio.html`, `/pricing.html`, `/privacy.html`, `/services.html`, and `/terms.html` → their matching no-slash canonical
- Redirect-only device hub: `/devices`, `/devices/`, `/devices/index.html`, and `/devices.html` → `/devices/samsung`
- Redirect-only tools hub: `/tools`, `/tools/`, `/tools/index.html`, and `/tools.html` → `/tools/rootability-checker`
- Generic one-, two-, and three-segment trailing-slash and `/index.html` aliases → the corresponding no-slash canonical

Redirects are implemented as nginx `location =` and regex rules in `/etc/nginx/conf.d/droidrooter.conf` on the VPS (the site is served by standalone nginx on port 8094, not Cloudflare Pages). Query strings are preserved via `$is_args$args`. Existing legacy blog-slug redirect destinations were also normalized to no-slash targets to avoid two-hop chains.

### Deliberately deferred

- `/blog/rootable-android-devices-complete-list-2025.html`
- `/blog/rootable-android-devices-complete-list-2025/`
- `/blog/android-custom-kernel-guide-2025`
- `/blog/unlock-bootloader-android-guide`
- All other pre-existing 2025 meta-refresh stubs

No new permanent redirects were added for those URLs. See `docs/HIGH-RISK-CONSOLIDATION-CANDIDATES.md`.

### Validation completed before deployment

- 122 canonical indexable URLs in the sitemap
- 686 JSON-LD blocks parse successfully
- No `AggregateRating` markup present
- No visible or ISO date later than 2026-08-16 remains
- All 10 Tier A title/H1 snapshots match their pre-change values
- High-risk URLs are absent from the nginx redirect rules

## 2026-08-27 — Legitimate consumer modification service cluster

| date | URL | page tier | change type | exact files changed | reason | pre-change GSC clicks/impressions/CTR/position | post-change field to fill later | rollback note |
|---|---|---|---|---|---|---|---|---|
| 2026-08-27 | `/services/android-rooting` | Existing ranking service page | content correction and intent refinement | `services/android-rooting/index.html` | Replace unsupported all-brand, timing, integrity-evasion, guarantee, and pricing claims with device-first compatibility checks, explicit risks, scope, rollback, checker, and rescue paths while preserving the URL | Approximately 68 clicks and average position 13.3 supplied; impressions and CTR not supplied | Compare URL clicks, impressions, CTR, position, and conversions after a comparable period | Restore the prior generated HTML from Git and redeploy |
| 2026-08-27 | `/services/bootloader-unlock` | New | new specialist service page | `services/bootloader-unlock/index.html` | Separate bootloader unlock intent from carrier/SIM and account locks; document exact-variant, official-path, data-wipe, and permanent-flag requirements | New URL; no baseline | Fill after first comparable indexed period | Remove the route, sitemap entry, and hub links, then redeploy |
| 2026-08-27 | `/services/magisk-installation` | New | new specialist service page | `services/magisk-installation/index.html` | Document exact-firmware matching, boot/init_boot verification, optional module scope, rollback, and rescue handling without timing promises | New URL; no baseline | Fill after first comparable indexed period | Remove the route, sitemap entry, and hub links, then redeploy |
| 2026-08-27 | `/services/custom-rom-installation` | New | new specialist service page | `services/custom-rom-installation/index.html` | Document device-supported ROM selection, firmware/vendor prerequisites, clean/dirty flash, GApps/de-Googled choices, feature tradeoffs, GrapheneOS limits, and return to stock | New URL; no baseline | Fill after first comparable indexed period | Remove the route, sitemap entry, and hub links, then redeploy |
| 2026-08-27 | `/services/advanced-mods` | Existing hub | content correction and internal linking | `services/advanced-mods/index.html` | Convert a duplicate/unsupported sales page into a decision hub for rooting, bootloader, Magisk/modules, custom ROMs, recovery, automation, and scoped developer/business work | URL-level baseline not supplied | Compare hub impressions, child-page discovery, and assisted conversions | Restore the prior generated HTML from Git and redeploy |

Additional files: `sitemap.xml` and internal generator/test files under `.droidrooter/`.

### Service-cluster controls

- No device/brand compatibility table was generated because `currentDeviceMatrix` is disabled and no verified model/firmware database is present.
- No pricing band, success rate, turnaround promise, pay-after-success promise, warranty, or app-integrity guarantee was added.
- Structured data is limited to `WebPage` and `BreadcrumbList`; no `FAQPage`, `Service`, or `Offer` schema is present on the five pages.
- Rooting retains its existing `/services/android-rooting` URL and links to the checker, bootloader, Magisk, custom ROM, firmware, rescue, and educational paths.
- The advanced-mods page is a navigation hub rather than a competing generic service page.

## 2026-08-28 — Redistribute normalized 2026 guide dates

- Synced the public DroidRooter files from GitHub `main` into the Replit workspace.
- Replaced the shared `2026-08-16` publication date on 15 of the 16 affected 2026 guides with weekly dates from `2026-05-03` through `2026-08-09`.
- Preserved the guides' original planned sequence; the newest guide, `/blog/android-debloating-guide-2026`, remains dated `2026-08-16`.
- Updated article metadata, Article JSON-LD, visible bylines, blog/category listings, and related-post cards together.
- Left `/blog/android-frp-bypass-guide-2026` unchanged at `2026-08-15`.

## 2026-08-28 — Canonical alternate cleanup for Render static hosting

| date | URL | page tier | change type | exact files changed | reason | pre-change GSC clicks/impressions/CTR/position | post-change field to fill later | rollback note |
|---|---|---|---|---|---|---|---|---|
| 2026-08-28 | Sitewide generated HTML | Mixed; Tier A content unchanged | redirect fallback, internal-link normalization, and schema correction | Generated HTML; `.droidrooter/normalize-generated-site.py`; `.droidrooter/test-routing.py` | GSC reported 44 alternate canonicals: 42 trailing-slash paths, `/index.html`, and an inactive SearchAction query URL. Remove the unsupported SearchAction, normalize 19 internal links to their no-slash destinations, and normalize alternate paths at runtime on Render while retaining server-side 301 rules in the Nginx reference. | Coverage export only; 44 affected alternate URLs. No URL-level performance values supplied. | Compare the “Alternative page with proper canonical tag” count after Google recrawls the affected paths. | Restore generated HTML and control scripts from the prior Git revision. |

Render static sites serve existing `directory/index.html` resources before applying
dashboard redirect rules and do not provide a configurable trailing-slash policy.
The public Render deployment therefore uses an early canonical-path redirect script
as a fallback. The VPS Nginx reference continues to define permanent 301 redirects
for hosts where that server configuration controls the public response.