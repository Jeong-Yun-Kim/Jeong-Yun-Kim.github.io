"""Check published HTML, links, assets, metadata, and preserved project records."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, urljoin
import json
import re

ROOT=Path(__file__).resolve().parent.parent
DIST=ROOT/'dist'
ORIGIN='https://jeong-yun-kim.github.io'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.links=[]; self.h1=0; self.main=0; self.template=0
        self.title=False; self.lang=None; self.description=False; self.canonical=None
        self.og=False; self.errors=[]; self.heading=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='template': self.template+=1
        if self.template: return
        if tag=='html': self.lang=a.get('lang')
        if tag=='title': self.title=True
        if tag=='main': self.main+=1
        if tag=='meta':
            if a.get('name')=='description' and a.get('content'): self.description=True
            if a.get('property')=='og:image': self.og=True
        if tag=='link' and a.get('rel')=='canonical': self.canonical=a.get('href')
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        if re.fullmatch(r'h[1-6]',tag):
            level=int(tag[1])
            if level>self.heading+1: self.errors.append('heading jump to '+tag)
            self.heading=level
        if tag in ('a','link') and a.get('href'): self.links.append(a['href'])
        if tag in ('img','script') and a.get('src'): self.links.append(a['src'])
        if tag=='img' and not all(k in a for k in ('alt','width','height')): self.errors.append('image metadata missing')
        if a.get('target')=='_blank' and not {'noopener','noreferrer'} <= set(a.get('rel','').split()): self.errors.append('unsafe external link')
    def handle_endtag(self,tag):
        if tag=='template': self.template-=1

def validate():
    pages={}; errors=[]; links=0
    for path in DIST.rglob('*.html'):
        parser=Page(); text=path.read_text(); parser.feed(text); pages[path.resolve()]=parser
        checks=[(parser.lang=='ko','language'),(parser.h1==1,'one h1'),(parser.main==1,'one main'),(parser.title,'title'),(parser.description,'description'),(parser.og,'og:image'),(bool(parser.canonical and parser.canonical.startswith(ORIGIN+'/')),'canonical'),(len(parser.ids)==len(set(parser.ids)),'unique IDs')]
        errors.extend(f'{path.relative_to(DIST)}: {label}' for okay,label in checks if not okay)
        errors.extend(f'{path.relative_to(DIST)}: {issue}' for issue in parser.errors)
        if re.search(r'\[이름\]|\[프로젝트 설명\]|Lorem ipsum|PLACEHOLDER',text): errors.append(f'{path}: placeholder')
    for path,parser in pages.items():
        route='/'+str(path.relative_to(DIST)).replace('index.html','')
        for raw in parser.links:
            url=urlsplit(urljoin(ORIGIN+route,raw))
            if url.scheme not in ('http','https') or url.netloc!='jeong-yun-kim.github.io': continue
            target=(DIST/unquote(url.path).lstrip('/')).resolve()
            if target.is_dir(): target=target/'index.html'
            if not target.is_file(): errors.append(f'{path.name}: missing {raw}'); continue
            links+=1
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids: errors.append(f'{path.name}: anchor {raw}')
    required=['index.html','portfolio.html','404.html','about/index.html','projects/index.html','resume/index.html','projects/ai-rescue-box/index.html','robots.txt','sitemap-index.xml','sitemap-0.xml','favicon.svg','images/og-cover.png']
    errors.extend('missing '+name for name in required if not (DIST/name).is_file())
    projects=json.loads((ROOT/'src/data/projects.json').read_text())
    for p in projects:
        path=DIST/'projects'/p['slug']/'index.html'
        if not path.is_file(): errors.append('missing project '+p['slug']); continue
        text=path.read_text()
        from html import escape
        for field in ('overview','background','sourceNote'):
            if escape(p[field],quote=True) not in text: errors.append(f'{p["slug"]}: missing {field}')
        for field in ('results','limits','evaluation'):
            for value in p[field]:
                if escape(value,quote=True) not in text: errors.append(f'{p["slug"]}: omitted {field}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(json.dumps({'status':'passed','htmlPages':len(pages),'internalReferences':links,'projectRecords':len(projects)},ensure_ascii=False))

if __name__=='__main__': validate()
