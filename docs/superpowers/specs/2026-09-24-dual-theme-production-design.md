# DroidRooter Dual Theme Production Design

**Date:** 2026-09-24  
**Repository:** `saadnahid7/droidrooter`  
**Production baseline:** `f41d1ef8fe61bb4478458f91b803f732ac1cfef6`

## Goal

Publish the two approved visual designs on the production site while preserving every route, page body, SEO field, internal link, redirect, and the current DRVCAM console bundle. Visitors can select Command Center or Terminal independently from dark or light color mode. First visits use Command Center in dark mode.

## Backup and rollback

Before production integration, create `backup/main-before-dual-theme-2026-09-24` at the exact production baseline SHA. The branch is the rollback source and must never be advanced as part of this work.

Implementation occurs on `feature/dual-theme-production`. Production `main` advances only after all required checks pass. If the deployed result has a material regression, restore `main` from the backup commit using a normal revert or fast-forward-compatible recovery procedure that preserves history.

## Theme model

The theme has two independent saved settings:

- Design: `command` or `terminal`; default `command`.
- Color: `dark` or `light`; default `dark`.

The root HTML element exposes the active values through `data-design` and `data-color-mode`. A small inline or early local initializer reads valid saved values before first paint and applies both attributes to avoid a flash of the wrong theme. Invalid, blocked, or missing storage falls back safely to Command Center dark.

A compact accessible control provides both settings. Each control has a visible label, keyboard focus styling, an accurate accessible name, and a pressed/selected state. Settings persist in localStorage and apply immediately without navigation or page reload.

## Assets and performance

Reuse the existing shared theme palette and behavior. Split design rules into focused `command.css` and `terminal.css` assets. Both files may be linked because their selectors are gated by the root `data-design` value; their combined size is small and avoids a runtime stylesheet request during a switch. JavaScript remains dependency free.

No framework, remote font, image, analytics script, animation library, or other third-party asset is added. Theme controls use text and existing CSS tokens. The initializer stays in the document head; interaction code is deferred. CSS effects that are expensive on low-end mobile devices, such as large blur filters or continuous animations, are excluded.

The performance acceptance gate compares production baseline and candidate pages on representative home, service, blog index, long blog article, and 404 routes. The candidate must introduce no material regression in LCP, CLS, INP/blocking time, request count, or transferred bytes. Any measurable regression must be explained and reduced before production update.

## Public HTML integration

Apply the shared theme assets and selector exactly once to every nonredirect public HTML document. Redirect stubs remain behaviorally identical. Do not alter:

- Visible copy, headings, lists, tables, images, or calls to action.
- Titles, meta descriptions, canonical URLs, robots directives, Open Graph/Twitter metadata, hreflang, or structured data.
- URLs, filenames, anchors, internal links, sitemap, robots.txt, or manifest.
- Existing forms, scripts, or page-specific behavior.

The generated theme installer remains idempotent so future regenerated HTML can receive the same integration without duplicate controls or assets.

## DRVCAM console

Preserve the current console JavaScript, CSS, route shells, CSP/header file, and `noindex` metadata. The console keeps its native authenticated theme menu. Its sign-in screen receives a lightweight color-mode control and defaults to dark. The public color preference can initialize the console color, and console changes can synchronize the shared color preference. Design switching does not restyle or interfere with the application console.

## Validation

Static validation covers all 179 HTML routes:

- Route inventory unchanged from the baseline.
- Theme assets and controls occur exactly once on each eligible page.
- Page content and SEO metadata normalize identically to the baseline after removing theme additions.
- Sitemap, robots.txt, manifest, redirect targets, DRVCAM protected files, and current hashed console assets remain unchanged.
- No newly broken internal URL, fragment, image, script, or stylesheet reference.
- Default state is Command Center dark and all four design/color combinations resolve correctly.
- Storage failure and invalid saved values return to safe defaults.

Browser validation covers every nonredirect route at mobile and desktop widths in all four combinations: Command dark, Command light, Terminal dark, and Terminal light. It checks navigation, overflow, overlapping or clipped content, missing assets, console errors, keyboard access, readable contrast, and layout stability. Redirect routes are checked separately.

Representative Lighthouse runs compare the baseline and candidate. Production update is blocked by new 404s, SEO differences, content differences, broken controls, serious accessibility errors, console errors, or material performance regressions.

## Delivery

After validation, advance `main` to the verified integration commit and confirm the remote branch SHA. Review the Render deployment and repeat smoke checks on the live home page, blog index, one article, one service page, 404 page, and DRVCAM sign-in. Record commit SHAs, test counts, Lighthouse results, deployment status, and any remaining limitation in the final report.
