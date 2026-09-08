"""Confere páginas, links, metadados e tamanho dos arquivos."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote, parse_qs
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
BASE = 'https://xn--hugoservios-u9a.com'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.links = []
        self.assets = []
        self.meta = {}
        self.canonical = []
        self.h1 = 0
        self.title = ''
        self.schema = []
        self.forms = []
        self.images = []
        self.lang = None
        self._title = False
        self._json = False
        self._json_data = ''
    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self._title = True
        if tag == 'meta': self.meta[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag == 'link':
            if a.get('rel') == 'canonical': self.canonical.append(a['href'])
            if a.get('rel') in ('stylesheet', 'preload', 'icon'): self.assets.append(a['href'])
        if tag == 'img':
            self.images.append(a)
            self.assets.append(a['src'])
            if a.get('srcset'):
                self.assets += [item.strip().split()[0] for item in a['srcset'].split(',')]
        if tag == 'script':
            if a.get('src'): self.assets.append(a['src'])
            if a.get('type') == 'application/ld+json':
                self._json = True
                self._json_data = ''
        if tag == 'form': self.forms.append(a)
    def handle_data(self, data):
        if self._title: self.title += data
        if self._json: self._json_data += data
    def handle_endtag(self, tag):
        if tag == 'title': self._title = False
        if tag == 'script' and self._json:
            self.schema.append(json.loads(self._json_data))
            self._json = False

def target(url):
    p = urlparse(url).path
    return DIST / (p.lstrip('/') + 'index.html' if p.endswith('/') else p.lstrip('/'))

pages = {}
errors = []
warnings = []
for file in DIST.rglob('*.html'):
    page = Page(file)
    content = file.read_text(encoding='utf-8')
    page.feed(content)
    pages[file.resolve()] = page
    if page.h1 != 1: errors.append(f'{file.name}: expected one h1, found {page.h1}')
    if page.lang != 'pt-BR': errors.append(f'{file.name}: incorrect language')
    if len(page.ids) != len(set(page.ids)): errors.append(f'{file}: duplicate IDs')
    if len(page.canonical) != 1: errors.append(f'{file}: canonical missing or duplicated')
    if not page.meta.get('description'): errors.append(f'{file}: description missing')
    if len(page.meta.get('description', '')) > 175: warnings.append(f'{file.relative_to(DIST)}: description {len(page.meta["description"])} chars')
    if not page.title or len(page.title) > 72: warnings.append(f'{file}: title length {len(page.title)}')
    if 'conteudo' not in page.ids: errors.append(f'{file}: skip-link target missing')
    if not page.schema: errors.append(f'{file}: schema missing')
    for data in page.schema:
        organization = next(n for n in data['@graph'] if n['@type'] == 'Organization')
        if organization['telephone'] != '+55-11-98322-9289': errors.append('Incorrect phone in schema')
        if {a['name'] for a in organization['areaServed']} != {'Embu das Artes', 'Taboão da Serra'}: errors.append('Incorrect service areas')
    for a in page.images:
        if not all(key in a for key in ('width', 'height', 'alt')): errors.append(f'{file}: incomplete image accessibility or dimensions')
    for asset in page.assets:
        if not asset.startswith('/'): errors.append(f'{file}: external runtime asset {asset}')
        elif not target(asset).is_file(): errors.append(f'{file}: asset missing {asset}')
    for link in page.links:
        parsed = urlparse(link)
        if parsed.netloc == 'wa.me':
            if parsed.path != '/5511983229289': errors.append(f'{file}: wrong WhatsApp number')
            if not parse_qs(parsed.query).get('text'): errors.append(f'{file}: WhatsApp draft missing')
        if parsed.scheme == 'tel' and parsed.path != '+5511983229289': errors.append(f'{file}: wrong telephone')
    if re.search(r'(password|senha|ftp://|ftps://|BEGIN .*PRIVATE KEY)', content, re.I): errors.append(f'{file}: unexpected credential-related content')

for file, page in pages.items():
    for link in page.links:
        parsed = urlparse(link)
        if parsed.scheme or parsed.netloc: continue
        dest = target(link).resolve() if parsed.path else file
        if dest not in pages:
            if not dest.is_file(): errors.append(f'{file}: broken internal link {link}')
        elif parsed.fragment and unquote(parsed.fragment) not in pages[dest].ids:
            errors.append(f'{file}: missing anchor {link}')

sitemap = ET.parse(DIST / 'sitemap.xml')
sitemap_urls = [n.text for n in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
for url in sitemap_urls:
    if not url.startswith(BASE + '/'): errors.append('Sitemap uses wrong host')
    file = target(url).resolve()
    if file not in pages: errors.append(f'Sitemap missing page {url}')
    elif pages[file].canonical != [url]: errors.append(f'Canonical mismatch {url}')
if len(sitemap_urls) != 8: errors.append('Expected home, six service pages and privacy in sitemap')
if b'wOF2' != (DIST / 'assets/manrope-latin.woff2').read_bytes()[:4]: errors.append('Font is not WOFF2')
home = pages[(DIST / 'index.html').resolve()]
base_assets = [DIST / 'index.html'] + [target(u) for u in home.assets if not u.endswith('.webp')]
compressed_base = sum(len(gzip.compress(p.read_bytes())) if p.suffix in ('.html','.css','.js','.svg') else p.stat().st_size for p in set(base_assets))
initial_mobile_bytes = compressed_base + (DIST / 'assets/hugo-ferramentas-800.webp').stat().st_size
if initial_mobile_bytes > 250_000: errors.append('Initial page transfer exceeds 250 KB budget')
report = {'status': 'PASS' if not errors else 'FAIL', 'html_pages': len(pages), 'indexed_pages': len(sitemap_urls), 'internal_links': sum(len([u for u in p.links if u.startswith(('/', '#'))]) for p in pages.values()), 'whatsapp_links': sum(len([u for u in p.links if u.startswith('https://wa.me/')]) for p in pages.values()), 'estimated_initial_bytes_with_800px_hero': initial_mobile_bytes, 'warnings': warnings, 'errors': errors}
(ROOT / 'reports/validation.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(report, indent=2, ensure_ascii=False))
raise SystemExit(bool(errors))
