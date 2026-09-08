from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
DIST = ROOT / 'dist'
BASE = 'https://xn--hugoservios-u9a.com'
PHONE = '(11) 98322-9289'
SERVICES = json.loads((SRC / 'services.json').read_text(encoding='utf-8'))
ICONS = json.loads((SRC / 'icons.json').read_text(encoding='utf-8'))
HOME_FAQ = json.loads((SRC / 'faq.json').read_text(encoding='utf-8'))
AREAS = [
    {'@type': 'City', 'name': name,
     'containedInPlace': {'@type': 'State', 'name': 'São Paulo'}}
    for name in ('Embu das Artes', 'Taboão da Serra')
]
CSS = f'/assets/site.{hashlib.sha256((SRC / "site.css").read_bytes()).hexdigest()[:10]}.css'
JS = f'/assets/site.{hashlib.sha256((SRC / "site.js").read_bytes()).hexdigest()[:10]}.js'
PAGES = []
JSON_HASHES = set()
