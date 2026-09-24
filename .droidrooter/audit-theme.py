#!/usr/bin/env python3
"""Compare every generated page with an immutable git baseline; inventory local links and SEO."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import subprocess,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=__import__('os').environ.get('AUDIT_BASE','94afa8007287c7688417405bc338f277e3b9ca22')
# Pages the owner updates manually; they must stay byte-identical to the baseline.
EXCLUDED={'blog/monitor-teen-android-without-them-knowing-legal-guide/index.html','blog/mspy-vs-bark-vs-qustodio-comparison/index.html','blog/parental-control-app-detection-and-removal/index.html'}
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT).decode().replace('\r\n','\n')
def remove_additions(s):
 s=re.sub(r'<!-- dr-theme-([\w-]+):start -->.*?<!-- dr-theme-\1:end -->','',s,flags=re.S)
 s=re.sub(r' data-(?:design|color-mode)="[^"]*"','',s)
 return s
def normalized(s):
 s=remove_additions(s)
 s=re.sub(r'(<style\b[^>]*>).*?(</style>)',r'\1PRESENTATION\2',s,flags=re.S)
 s=re.sub(r'style="[^"]*"','style="PRESENTATION"',s)
 return s
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.links=[];self.assets=[];self.ids=set();self.title=[];self.meta=[];self.headings=[];self.canonical=[];self.state=None;self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if t=='a' and a.get('href'):self.links.append(a['href'])
  if t in ('img','script','source') and a.get('src'):self.assets.append(a['src'])
  if t=='link' and a.get('rel')=='stylesheet':self.assets.append(a.get('href',''))
  if t=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  if t=='meta':self.meta.append(a)
  if t in ('title','h1'):self.state=t
 def handle_endtag(self,t):
  if t==self.state:self.state=None
 def handle_data(self,d):
  if self.state=='title':self.title.append(d)
  if self.state=='h1':self.headings.append(d)
files=git('ls-tree','-r','--name-only',BASE).splitlines()
html=[x for x in files if x.endswith('.html')]
assert html==sorted(str(x.relative_to(ROOT)) for x in ROOT.rglob('*.html')),'HTML route inventory changed'
errors=[];pages={};oldpages={};redirects=[]
for name in html:
 old=git('show',BASE+':'+name);new=(ROOT/name).read_bytes().decode().replace('\r\n','\n')
 if normalized(old)!=normalized(new):errors.append({'page':name,'error':'Non-presentation HTML changed'})
 redirect=bool(re.search(r'http-equiv=["\']refresh',old,re.I))
 if (name in EXCLUDED or redirect) and old!=new:errors.append({'page':name,'error':'Excluded or redirect page modified'})
 elif name.startswith('drvcam/'):
  if new.count('data-dr-theme-init')!=1 or new.count('data-dashboard-theme-toggle')!=1 or '/assets/theme/base.css' in new:errors.append({'page':name,'error':'Console shell bridge missing, duplicated or loads public theme CSS'})
 elif not (name in EXCLUDED or redirect) and (new.count('data-dr-theme-init')!=1 or new.count('data-theme-controls')!=1 or new.count('data-design-toggle')!=0 or new.count('data-theme-toggle')!=1 or new.count('/assets/theme/command.css')!=1 or new.count('/assets/theme/terminal.css')!=0):errors.append({'page':name,'error':'Missing or duplicate theme controls'})
 pages[name]=Page(new);oldpages[name]=Page(old)
 if re.search(r'http-equiv=["\']refresh',old,re.I):redirects.append(name)
 if pages[name].canonical!=oldpages[name].canonical or pages[name].meta!=oldpages[name].meta:errors.append({'page':name,'error':'SEO metadata changed'})
for name in ['sitemap.xml','robots.txt','manifest.json','drvcam/control/_headers']:
 if git('show',BASE+':'+name)!=(ROOT/name).read_text():errors.append({'file':name,'error':'Protected file changed'})
def resolve(url):
 p=unquote(urlsplit(url).path).lstrip('/')
 if not p:p='index.html'
 if (ROOT/p).is_file():return p
 if (ROOT/p/'index.html').is_file():return p.rstrip('/')+'/index.html'
 # extensionless variants on Render's static routing
 if (ROOT/(p+'.html')).is_file():return p+'.html'
 return None
missing=[];anchors=[]
for name,page in pages.items():
 base='https://www.droidrooter.com/'+name.removesuffix('index.html')
 for kind,links in [('link',page.links),('asset',page.assets)]:
  for href in links:
   url=urljoin(base,href);u=urlsplit(url)
   if u.netloc not in ('www.droidrooter.com','droidrooter.com') or u.scheme not in ('http','https'):continue
   target=resolve(url)
   if target is None:missing.append({'page':name,'kind':kind,'target':href,'preexisting':href in (oldpages[name].links+oldpages[name].assets)})
   elif kind=='link' and u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:anchors.append({'page':name,'target':href,'preexisting':href in oldpages[name].links})
report={'baseline':BASE,'excluded_pages':sorted(EXCLUDED),'themed_public_pages':len([x for x in html if not x.startswith('drvcam/') and x not in EXCLUDED and x not in redirects]),'html_pages':len(html),'redirect_pages':len(redirects),'application_shells':len([x for x in html if x.startswith('drvcam/')]),'preservation_errors':errors,'missing_local_targets':missing,'missing_fragments':anchors,'routes':[{'file':n,'redirect':n in redirects} for n in html]}
folder=ROOT/'docs/theme-redesign';folder.mkdir(parents=True,exist_ok=True);(folder/'static-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('routes','missing_local_targets','missing_fragments')},indent=2));print('Missing targets:',len(missing),'unique:',len(set(x['target'] for x in missing)),'missing fragments:',len(anchors))
print('Targets:',sorted(set(x['target'] for x in missing)))
assert not errors
assert not any(not x['preexisting'] for x in missing+anchors),'New broken targets'
