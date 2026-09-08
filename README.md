# Hugo Faz Tudo

Fiz esse site para o Hugo divulgar os serviços dele em Embu das Artes e Taboão da Serra. Ele trabalha com manutenção e pequenos reparos, como instalação de TV, montagem de móveis e elétrica.

A pessoa pode ver os serviços e preencher um pedido de orçamento. O site junta as informações numa mensagem, que ela revisa e envia pelo WhatsApp.

[Ver o site](https://xn--hugoservios-u9a.com/)

![Página inicial](docs/prints/01-inicio-desktop.png)

## O que usei

HTML, CSS e JavaScript, com Python para montar as páginas. Depois de gerar os arquivos, a hospedagem só precisa servir o site estático.

Cada serviço tem sua página, com explicações e dúvidas comuns. O layout também se adapta ao celular. Usei imagens em WebP e deixei a fonte junto dos arquivos do site.

## Como rodar

Com Python 3.10 ou mais recente, abra o terminal na pasta do projeto e rode:

```sh
python build.py
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Depois, abra [localhost:8000](http://127.0.0.1:8000). No Windows, pode usar `py` no lugar de `python`.

As imagens e a fonte já estão na pasta. Não precisa instalar pacotes para gerar o site.

## Para mexer no código

- `src/`: estilos, JavaScript, imagens e textos dos serviços.
- `templates/`: HTML das páginas.
- `sitegen/`: código que monta o site.
- `dist/`: arquivos gerados para publicar.

Depois de alterar alguma coisa, rode `python build.py` de novo. Evite editar direto em `dist/`, porque o build sobrescreve esses arquivos.

## Testes

Com Node.js também instalado, rode:

```sh
python tools/check.py
```

Isso gera o site e confere os links, as páginas, o menu e a montagem da mensagem do WhatsApp, sem enviar nada.

Para publicar na hospedagem, envie o conteúdo de `dist/`, incluindo o `.htaccess`.

[Mais prints](docs/prints/README.md) · [Detalhes técnicos](docs/tecnico.md) · [Créditos](docs/creditos.md)
