from string import Template

from .config import ROOT


def render_template(name, **values):
    source = (ROOT / 'templates' / name).read_text(encoding='utf-8')
    # A indentação ajuda na edição, mas não precisa ir para o HTML final.
    return Template(''.join(line.strip() for line in source.splitlines())).substitute(values)
