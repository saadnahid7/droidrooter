#!/usr/bin/env python3
"""Idempotent theme installation for the generated static site: dark uses the
Command Center design, light uses the Terminal design.

Run after publishing new HTML. Re-running produces no diff: every addition is
marker-delimited and removed before it is inserted again, and colour tokens are
only applied to declarations that do not already use them.

- Public pages get the head initializer, the theme stylesheets and one
  dark/light switch. Dark is the default.
- Literal colours in site CSS, <style> blocks and style="" attributes become
  theme tokens that keep the original colour as a fallback, so any page without
  the theme stylesheets (see EXCLUDED) still renders exactly as before.
- Redirect stubs and EXCLUDED pages are never modified.
- DRVCAM console shells only receive the sign-in colour bridge; the console
  bundle, its CSS and its own theme system are left untouched.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# Pages the owner will update manually; left byte-identical.
EXCLUDED = {
    'blog/monitor-teen-android-without-them-knowing-legal-guide/index.html',
    'blog/mspy-vs-bark-vs-qustodio-comparison/index.html',
    'blog/parental-control-app-detection-and-removal/index.html',
}
CONSOLE_PREFIX = 'drvcam/'
SKIP_DIRS = ('.git/', 'docs/', '.worktrees/', 'node_modules/')
REDIRECT = re.compile(r'http-equiv=["\']refresh', re.I)
MARKERS = re.compile(r'<!-- dr-theme-([\w-]+):start -->.*?<!-- dr-theme-\1:end -->', re.S)
ROOT_ATTRS = re.compile(r' data-(?:design|color-mode)="[^"]*"')


def rel(path):
    return path.relative_to(ROOT).as_posix()


# Read and write without newline translation so untouched bytes (including CRLF) are preserved.
def read(path):
    with open(path, encoding='utf-8', newline='') as handle:
        return handle.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8', newline='') as handle:
        handle.write(text)


def color(match, prop):
    value = match.group(0)
    alpha = 1
    if value.startswith('#'):
        h = value[1:]
        if len(h) in (3, 4):
            h = ''.join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return value
        rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        if len(h) == 8:
            alpha = int(h[6:8], 16) / 255
    else:
        nums = re.findall(r'[\d.]+', value)
        if len(nums) < 3:
            return value
        rgb = list(map(float, nums[:3]))
        alpha = float(nums[3]) if len(nums) > 3 else 1
    if alpha == 0:
        return value
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    is_text = prop in ('color', 'fill', 'stroke', '-webkit-text-fill-color')
    if mx < 55:
        token = '--dr-on-accent' if is_text else '--dr-bg' if mx < 18 else '--dr-panel'
    elif mn > 220:
        token = '--dr-ink' if is_text else '--dr-panel'
    elif g > r * 1.25 and g > b * 1.1:
        token = '--dr-accent'
    elif b > r * 1.35 and g > r * 1.3:
        token = '--dr-cyan'
    elif r > g * 1.25 and b > g * 1.1:
        token = '--dr-magenta'
    elif r > 160 and g > 140 and b < 100:
        token = '--dr-warning'
    elif mx - mn < 75:
        token = '--dr-muted' if is_text else '--dr-line'
    else:
        return value
    # The original colour stays as the fallback for pages without theme tokens. For
    # translucent colours the fallback is the opaque colour, because color-mix below
    # already applies the alpha (a translucent fallback would apply it twice).
    if alpha == 1:
        return f'var({token}, {value})'
    opaque = 'rgb({}, {}, {})'.format(*[round(c) if float(c).is_integer() else c for c in rgb])
    return f'color-mix(in srgb, var({token}, {opaque}) {alpha * 100:.2f}%, transparent)'


def colors(css):
    def decl(m):
        prop, value = m[1], m[2]
        # Custom properties, images and already-tokenised values stay as they are.
        if prop.startswith('--') or 'url(' in value or 'var(--dr-' in value:
            return m[0]
        value = re.sub(r'#[0-9a-fA-F]{3,8}\b|rgba?\([\d.,\s]+\)', lambda c: color(c, prop), value)
        return prop + ':' + value
    return re.sub(r'([\w-]+):([^;{}]+)', decl, css)


ICON_SUN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4m11.2 11.2L19 19M5 19l1.4-1.4M17.6 6.4L19 5"/></svg>'


def controls(floating):
    extra = ' dr-theme-controls--floating' if floating else ''
    return ('<!-- dr-theme-toggle:start -->'
            f'<div class="dr-theme-controls{extra}" data-theme-controls hidden>'
            f'<button type="button" class="dr-theme-toggle" data-theme-toggle aria-label="Switch to light theme" aria-pressed="true">{ICON_SUN}<span data-theme-label>Light</span></button>'
            '</div><!-- dr-theme-toggle:end -->')


HEAD = '<!-- dr-theme-head:start --><script data-dr-theme-init src="/assets/theme/init.js"></script><!-- dr-theme-head:end -->'
ASSETS = ('<!-- dr-theme-assets:start --><link rel="stylesheet" href="/assets/theme/base.css">'
          '<link rel="stylesheet" href="/assets/theme/command.css"><link rel="stylesheet" href="/assets/theme/terminal.css">'
          '<script src="/assets/theme/toggle.js" defer></script><!-- dr-theme-assets:end -->')

CONSOLE_HEAD = '<!-- dr-theme-head:start --><script data-dr-theme-init src="/assets/theme/dashboard-bridge.js"></script><!-- dr-theme-head:end -->'
CONSOLE_ASSETS = '<!-- dr-theme-assets:start --><link rel="stylesheet" href="/assets/theme/dashboard-bridge.css"><!-- dr-theme-assets:end -->'
CONSOLE_TOGGLE = '<!-- dr-theme-toggle:start --><button class="dr-dashboard-toggle" type="button" data-theme-toggle hidden data-dashboard-theme-toggle aria-label="Switch to light mode">Light mode</button><!-- dr-theme-toggle:end -->'


def strip(s):
    return ROOT_ATTRS.sub('', MARKERS.sub('', s))


def install_public(s):
    s = strip(s)
    s = re.sub(r'(<html\b)', r'\1 data-design="command" data-color-mode="dark"', s, count=1)
    s = re.sub(r'(<head\b[^>]*>)', lambda m: m[1] + HEAD, s, count=1)
    s = s.replace('</head>', ASSETS + '</head>', 1)
    if '<nav class="dr-nav-links"' in s:
        s = s.replace('<nav class="dr-nav-links"', controls(False) + '<nav class="dr-nav-links"', 1)
    else:
        s = s.replace('</body>', controls(True) + '</body>', 1)
    s = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m[1] + colors(m[2]) + m[3], s, flags=re.S)
    # Inline colour attributes (syntax-highlighted code) are presentation, not content.
    s = re.sub(r'style="([^"]*)"', lambda m: 'style="' + colors(m[1]) + '"', s)
    return s


def install_console(s):
    s = strip(s)
    s = re.sub(r'(<html\b)', r'\1 data-design="command" data-color-mode="dark"', s, count=1)
    # The bridge runs before the console module so the first paint uses the saved colour.
    s = s.replace('<script type="module"', CONSOLE_HEAD + '<script type="module"', 1)
    s = s.replace('</head>', CONSOLE_ASSETS + '</head>', 1)
    s = s.replace('</body>', CONSOLE_TOGGLE + '</body>', 1)
    return s


def main():
    css_changed = 0
    for f in sorted(ROOT.rglob('*.css')):
        name = rel(f)
        if name.startswith(('assets/theme/', CONSOLE_PREFIX) + SKIP_DIRS):
            continue
        before = read(f)
        after = colors(before)
        if after != before:
            write(f, after)
            css_changed += 1
    counts = {'public': 0, 'console': 0, 'redirect': 0, 'excluded': 0}
    for f in sorted(ROOT.rglob('*.html')):
        name = rel(f)
        if name.startswith(SKIP_DIRS):
            continue
        s = read(f)
        if name in EXCLUDED:
            counts['excluded'] += 1
            continue
        if REDIRECT.search(s):
            counts['redirect'] += 1
            continue
        if name.startswith(CONSOLE_PREFIX):
            new = install_console(s)
            counts['console'] += 1
        else:
            new = install_public(s)
            counts['public'] += 1
        if new != s:
            write(f, new)
    print('Theme installed:', counts, '| CSS files tokenised:', css_changed)


if __name__ == '__main__':
    main()
