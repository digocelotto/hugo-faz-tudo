# Como o site funciona

O Python junta os dados dos serviços e os modelos HTML. O resultado são páginas estáticas que a hospedagem entrega diretamente ao navegador.

```text
src/services.json + src/faq.json + templates/
                      |
                   build.py
                      |
                    dist/
                      |
            hospedagem Apache/LiteSpeed
```

## Organização

- `sitegen/config.py`: caminhos, domínio, dados e identificação das versões do CSS e JavaScript.
- `sitegen/components.py`: links de contato, ícones, cartões e elementos compartilhados.
- `sitegen/pages.py`: conteúdo usado para montar cada página.
- `sitegen/render.py`: metadados, dados estruturados e gravação do HTML.
- `sitegen/output.py`: sitemap, robots, favicon e `.htaccess`.
- `sitegen/templates.py`: preenchimento dos modelos com a biblioteca padrão do Python.

Os modelos usam campos como `${title}`. Os valores vindos dos serviços passam por escape de HTML antes de entrar nas páginas. A indentação dos modelos serve para a edição e é removida na geração. Mantenha os espaços necessários entre palavras e elementos na mesma linha.

## Contato

O visitante seleciona serviço e cidade, podendo acrescentar uma descrição de até 700 caracteres. O JavaScript valida o formulário e monta o endereço do WhatsApp com a mensagem codificada. O envio depende da confirmação da pessoa no próprio WhatsApp.

Não existe integração com a API do WhatsApp, envio automático ou gravação do formulário em banco de dados neste projeto.

## Publicar na hospedagem

1. Gere e confira o site com `python tools/check.py`.
2. Guarde uma cópia da versão atualmente publicada.
3. Envie o conteúdo de `dist/` para a raiz pública da hospedagem, incluindo `.htaccess`.
4. Confira a página inicial, uma página de serviço, o menu no celular e a abertura do rascunho no WhatsApp.

Os nomes do CSS e JavaScript mudam quando seus conteúdos mudam. O build deixa versões anteriores em `dist/` para evitar apagar arquivos de uma publicação em andamento; para um pacote limpo, gere a partir de uma cópia nova do repositório. Na hospedagem, mantenha os assets antigos durante a troca e retire-os depois que as páginas em cache deixarem de apontar para eles.

## Segurança e limites da revisão

O `.htaccess` mantém a política de conteúdo com hashes dos blocos JSON-LD, restrições de incorporação, tipos de conteúdo, permissões e redirecionamentos para HTTPS. Se o JSON-LD mudar, o build recalcula os hashes.

O servidor local do Python não aplica `.htaccess`. Testes locais de interface não comprovam redirecionamentos ou cabeçalhos em produção. A revisão deste pacote preserva essa configuração em relação ao original; não é um pentest nem uma certificação de segurança.

O site possui estrutura para indexação e buscas locais. Não foram medidos posicionamento no Google, aumento de orçamentos ou conversão.
