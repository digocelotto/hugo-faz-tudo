from datetime import datetime

from .components import cta, e, faq_html, icon, service_cards, wa
from .config import AREAS, BASE, HOME_FAQ, PHONE, SERVICES
from .render import write_page
from .templates import render_template

def home():
    options = ''.join(f'<option value="{e(s["name"])}">{e(s["name"])}</option>' for s in SERVICES)
    body = render_template(
        'home.html',
        icon_pin=icon('pin'),
        hero_cta=cta(position='hero'),
        icon_right=icon('right'),
        icon_check=icon('check'),
        icon_home=icon('home'),
        icon_chat=icon('chat'),
        icon_list=icon('list'),
        service_cards=service_cards(),
        wa=wa(),
        icon_arrow=icon('arrow'),
        icon_wa=icon('wa'),
        phone=PHONE,
        options=options,
        faq=faq_html(HOME_FAQ),
        final_cta=cta('Me chame no WhatsApp', position='final'),
    )
    catalog = {'@type': 'OfferCatalog', '@id': BASE + '/#servicos', 'name': 'Serviços de manutenção e pequenos reparos', 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['name'], 'url': BASE + '/servicos/' + s['slug'] + '/', 'provider': {'@id': BASE + '/#hugo'}, 'areaServed': AREAS}} for s in SERVICES]}
    write_page('/', 'Faz-tudo em Embu das Artes | Hugo Faz Tudo', 'Hugo Faz Tudo: instalação de TV, montagem de móveis, elétrica e pequenos reparos em Embu das Artes e Taboão da Serra. Peça seu orçamento pelo WhatsApp.', body, [catalog])


def detail(service):
    s = service
    path = '/servicos/' + s['slug'] + '/'
    short = s.get('short', s['name'])
    title = s['name'] + ' em Embu das Artes'
    items = ''.join(f'<li>{icon("check")}<span>{e(item)}</span></li>' for item in s['items'])
    related = ''.join(f'<a href="/servicos/{other["slug"]}/">{e(other.get("short",other["name"]))}</a>' for other in SERVICES if other != s)
    body = render_template(
        'service.html',
        short_name=e(short),
        service_icon=icon(s['icon']),
        title=e(title),
        intro=e(s['intro']),
        icon_pin=icon('pin'),
        phrase=e(s['phrase']),
        hero_cta=cta('Pedir orçamento', s['phrase'], position='service-hero'),
        phone=PHONE,
        items=items,
        preparation=e(s['prepare']),
        scope=e(s['scope']),
        contact_url=wa(s['phrase']),
        icon_arrow=icon('arrow'),
        faq=faq_html(s['faq']),
        final_cta=cta('Fale comigo', s['phrase'], position='service-final'),
        related=related,
    )
    extra = [
        {'@type': 'Service', '@id': BASE + path + '#service', 'name': title, 'serviceType': s['name'], 'description': s['intro'], 'url': BASE + path, 'areaServed': AREAS, 'provider': {'@id': BASE + '/#hugo'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': BASE + '/'}, {'@type': 'ListItem', 'position': 2, 'name': short, 'item': BASE + path}]}
    ]
    description = f'{s["name"]} em Embu das Artes e Taboão da Serra com Hugo Faz Tudo. {s["summary"]} Peça orçamento pelo WhatsApp.'
    write_page(path, s['title'], description, body, extra)


def legal_and_error():
    body = render_template(
        'privacy.html',
        wa=wa(),
        phone=PHONE,
        updated_at=datetime.now().strftime('%d/%m/%Y'),
    )
    write_page('/privacidade/', 'Privacidade | Hugo Faz Tudo', 'Saiba como funciona o formulário e o contato pelo WhatsApp no site do Hugo Faz Tudo.', body)
    error = render_template(
        '404.html',
        icon_right=icon('right'),
    )
    write_page('/404.html', 'Página não encontrada | Hugo Faz Tudo', 'Encontre os serviços de manutenção e pequenos reparos do Hugo Faz Tudo.', error, noindex=True)
