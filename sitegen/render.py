import base64
import hashlib
import json

from .components import e, footer, header
from .config import AREAS, BASE, CSS, DIST, JS, JSON_HASHES, PAGES
from .templates import render_template

def base_schema(path, title, description):
    return [
        {'@type': 'Organization', '@id': BASE + '/#hugo', 'name': 'Hugo Faz Tudo', 'alternateName': 'Hugo Serviços', 'url': BASE + '/', 'telephone': '+55-11-98322-9289', 'description': 'Manutenção e pequenos reparos residenciais em Embu das Artes e Taboão da Serra.', 'areaServed': AREAS, 'contactPoint': {'@type': 'ContactPoint', 'telephone': '+55-11-98322-9289', 'contactType': 'customer service', 'availableLanguage': 'Portuguese', 'areaServed': ['Embu das Artes', 'Taboão da Serra']}},
        {'@type': 'WebSite', '@id': BASE + '/#website', 'name': 'Hugo Faz Tudo', 'alternateName': 'Hugo Serviços', 'url': BASE + '/', 'inLanguage': 'pt-BR', 'publisher': {'@id': BASE + '/#hugo'}},
        {'@type': 'WebPage', '@id': BASE + path + '#webpage', 'url': BASE + path, 'name': title, 'description': description, 'inLanguage': 'pt-BR', 'isPartOf': {'@id': BASE + '/#website'}, 'about': {'@id': BASE + '/#hugo'}}
    ]


def write_page(path, title, description, body, extra=None, noindex=False):
    schema = {'@context': 'https://schema.org', '@graph': base_schema(path, title, description) + (extra or [])}
    schema_text = json.dumps(schema, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    JSON_HASHES.add('sha256-' + base64.b64encode(hashlib.sha256(schema_text.encode()).digest()).decode())
    page = render_template(
        'page.html',
        title=e(title),
        description=e(description),
        robots='noindex, follow' if noindex else 'index, follow, max-image-preview:large',
        base=BASE,
        path=path,
        css=CSS,
        schema_text=schema_text,
        js=JS,
        header=header(),
        body=body,
        footer=footer(),
    )
    target = DIST / ('index.html' if path == '/' else path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding='utf-8')
    if not noindex:
        PAGES.append(path)
