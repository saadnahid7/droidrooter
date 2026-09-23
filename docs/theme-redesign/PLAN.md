# Terminal implementation plan (first branch)

Current scope: finish only design/terminal-light, with both color modes. The user deferred the Command Center branch. Original two-branch design context is retained below.
Baseline: f1a24af692a7e63722394657ef6728616b655716 (main). Deployment configuration and main remain untouched.

1. Preserve existing static routing, HTML, scripts, metadata, structured data and assets. Add shared theme assets and a head initialization script; insert an accessible toggle in the public navigation, with a floating fallback for redirects, 404 and dashboard routes.
2. Convert hard-coded colors in existing CSS and inline style blocks to semantic variables so both modes cover all templates. Keep component geometry and interactions, then add scoped design refinements for Terminal and Command Center.
3. Terminal branch: spacious terminal headings, green accents, separated cards, square corners. Command Center branch: panel grid, stronger navigation borders, compact structured cards and a split homepage hero. Both default dark; explicit saved light preference wins.
4. Audit all 180 HTML documents against the baseline: visible text (excluding the new toggle), links, images, metadata, JSON-LD, original script contents, sitemap and robots. Record pre-existing issues separately. Re-run the repository routing checks.
5. Browser audit all non-redirect routes in both modes at desktop/mobile sizes: overflow, JavaScript errors, missing local assets, theme toggle and persistence. Exercise navigation, FAQs, code copying, forms without submission, tool controls and dashboard login surface without authentication changes. Review representative screenshots.
6. Commit the implementation, reproducible scripts and audit findings on each new branch. Push branch refs only. Do not merge or change Render settings.

Review risks: blocked localStorage, JavaScript disabled, direct deep links, mobile navigation wrapping, horizontally scrolling code/tables, private dashboard noindex and API behavior.
