# Command Center branch review

Baseline: `f41d1ef8fe61bb4478458f91b803f732ac1cfef6`. All 179 HTML routes are present: 147 themed public documents, 18 redirect stubs, and 14 current DRVCAM console shells. The 14 console shells are identical on the baseline and retain the current JS, CSS, metadata, and noindex settings. Public presentation and route inventory derive from the previously audited Terminal branch; public source files on current main have not changed since that audit. The Command Center variant changes CSS and an early theme initializer only. First visits default to dark, with a public toggle and a console sign-in toggle; signed-in console users retain the native theme menu.

Run `python3 .droidrooter/audit-theme.py` to compare content, metadata, internal links, and route inventory against this baseline. Run `node .droidrooter/browser-audit.cjs` after generating the static report and installing Playwright to inspect every route in both modes and mobile/desktop viewports.

Browser rendering and link navigation on this branch have not been run because the execution workspace was unavailable during creation. Do not treat this branch as ready for deployment until these checks are completed.
