from datetime import datetime
import html
from urllib.parse import quote

from .config import ICONS, PHONE, SERVICES
from .templates import render_template

def e(value):
    return html.escape(str(value), quote=True)


def icon(name):
    return f'<svg class="icon" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def wa(service=None):
    text = 'Olá, Hugo! Vim pelo site e gostaria de pedir um orçamento.' if not service else f'Olá, Hugo! Vim pelo site e gostaria de um orçamento para {service}.'
    return 'https://wa.me/5511983229289?text=' + quote(text)


def cta(label='Pedir orçamento no WhatsApp', service=None, classes='button-orange', position='content'):
    return f'<a class="button {classes}" href="{wa(service)}" data-contact="{e(position)}">{icon("wa")}<span>{e(label)}</span>{icon("arrow")}</a>'


def brand():
    return '<a class="brand" href="/" aria-label="Hugo Faz Tudo — página inicial"><span class="brand-name">HUGO<span>.</span></span><span class="brand-description">FAZ TUDO<br>EM MANUTENÇÕES</span></a>'


def header():
    return render_template(
        'header.html',
        brand=brand(),
        header_cta=cta('Falar no WhatsApp', classes='button-blue button-small', position='header'),
        icon_menu=icon('menu'),
        icon_close=icon('close'),
        icon_right=icon('right'),
    )


def footer():
    links = ''.join(f'<a href="/servicos/{s["slug"]}/">{e(s.get("short", s["name"]))}</a>' for s in SERVICES)
    return render_template(
        'footer.html',
        brand=brand(),
        links=links,
        wa=wa(),
        phone=PHONE,
        year=datetime.now().year,
        mobile_cta=cta('Pedir orçamento', classes='button-orange', position='mobile-fixed'),
        icon_phone=icon('phone'),
    )


def faq_html(questions):
    return '<div class="faq-list">' + ''.join(f'<details><summary>{e(item["q"])}</summary><p>{e(item["a"])}</p></details>' for item in questions) + '</div>'


def service_cards():
    return ''.join(f'''<a class="service-card" href="/servicos/{s['slug']}/" aria-label="Saiba mais sobre {e(s['phrase'])} em Embu das Artes"><div class="service-top"><span class="service-icon">{icon(s['icon'])}</span><span class="service-number">0{i}</span></div><h3>{e(s.get('short',s['name']))}</h3><p>{e(s['summary'])}</p><span class="service-tags">{e(s['tags'])}</span><span class="service-more">Conhecer o serviço {icon('arrow')}</span></a>''' for i, s in enumerate(SERVICES, 1))
