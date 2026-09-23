#!/usr/bin/env python3
"""Idempotent theme installation for the generated static site (run after publishing new HTML)."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
# Theme values are separate from existing tokens to avoid variable cycles.
def color(match,prop):
 value=match.group(0); alpha=1
 if value.startswith('#'):
  h=value[1:]
  if len(h) in (3,4):h=''.join(c*2 for c in h)
  if len(h) not in (6,8):return value
  rgb=[int(h[i:i+2],16) for i in (0,2,4)]
  if len(h)==8:alpha=int(h[6:8],16)/255
 else:
  nums=re.findall(r'[\d.]+',value)
  if len(nums)<3:return value
  rgb=list(map(float,nums[:3]));alpha=float(nums[3]) if len(nums)>3 else 1
 if alpha==0:return value
 r,g,b=rgb; mx=max(rgb);mn=min(rgb)
 is_text=prop in ('color','fill','stroke','-webkit-text-fill-color')
 if mx<55:token='--dr-on-accent' if is_text else '--dr-bg' if mx<18 else '--dr-panel'
 elif mn>220:token='--dr-ink' if is_text else '--dr-panel'
 elif g>r*1.25 and g>b*1.1:token='--dr-accent'
 elif b>r*1.35 and g>r*1.3:token='--dr-cyan'
 elif r>g*1.25 and b>g*1.1:token='--dr-magenta'
 elif r>160 and g>140 and b<100:token='--dr-warning'
 elif mx-mn<75:token='--dr-muted' if is_text else '--dr-line'
 else:return value
 base='var('+token+')'
 return base if alpha==1 else f'color-mix(in srgb, {base} {alpha*100:.2f}%, transparent)'
def colors(css):
 def decl(m):
  prop=m[1];value=m[2]
  if prop.startswith('--') or 'url(' in value:return m[0]
  value=re.sub(r'#[0-9a-fA-F]{3,8}\b|rgba?\([\d.,\s]+\)',lambda c:color(c,prop),value)
  return prop+':'+value
 return re.sub(r'([\w-]+):([^;{}]+)',decl,css)
for f in ROOT.rglob('*.css'):
 if 'assets/theme' in f.relative_to(ROOT).as_posix():continue
 s=f.read_text();f.write_text(colors(s))
button='''<!-- dr-theme-toggle:start --><button type="button" class="dr-theme-toggle" data-theme-toggle hidden aria-label="Switch to light theme" aria-pressed="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4m11.2 11.2L19 19M5 19l1.4-1.4M17.6 6.4L19 5"/></svg><span data-theme-label>Light</span></button><!-- dr-theme-toggle:end -->'''
for f in ROOT.rglob('*.html'):
 s=f.read_text()
 if 'data-dr-theme-init' in s or re.search(r'http-equiv=[\"\']refresh',s,re.I):continue
 s=re.sub(r'(<html\b)',r'\1 data-design="'+('command' if (ROOT/'assets/theme/variant.css').read_text().startswith('/* command') else 'terminal')+'" data-color-mode="dark"',s,count=1)
 s=re.sub(r'(<head\b[^>]*>)',r'\1<!-- dr-theme-head:start --><script data-dr-theme-init src="/assets/theme/init.js"></script><!-- dr-theme-head:end -->',s,count=1)
 s=s.replace('</head>','<!-- dr-theme-assets:start --><link rel="stylesheet" href="/assets/theme/base.css"><link rel="stylesheet" href="/assets/theme/variant.css"><script src="/assets/theme/toggle.js" defer></script><!-- dr-theme-assets:end --></head>')
 if '<nav class="dr-nav-links"' in s:s=s.replace('<nav class="dr-nav-links"',button+'<nav class="dr-nav-links"',1)
 else:s=s.replace('</body>',button.replace('class="dr-theme-toggle"','class="dr-theme-toggle dr-theme-toggle--floating"')+'</body>',1)
 s=re.sub(r'(<style\b[^>]*>)(.*?)(</style>)',lambda m:m[1]+colors(m[2])+m[3],s,flags=re.S)
 # Inline color attributes (syntax highlighted code) are presentation, not content.
 s=re.sub(r'style="([^"]*)"',lambda m:'style="'+colors(m[1])+'"',s)
 f.write_text(s)
print('Theme installed across',len(list(ROOT.rglob('*.html'))),'HTML documents')
