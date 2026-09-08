(() => {
  'use strict';
  function setupMenu() {
    const menu = document.getElementById('mobile-menu');
    if (!menu) return;

    const toggle = menu.querySelector('summary');
    const closeMenu = (restoreFocus = false) => {
      menu.open = false;
      if (restoreFocus) toggle.focus();
    };
    menu.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('click', (event) => {
      if (menu.open && !menu.contains(event.target)) closeMenu();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menu.open) {
        event.preventDefault();
        closeMenu(true);
      }
    });
    menu.addEventListener('focusout', (event) => {
      if (event.relatedTarget && !menu.contains(event.relatedTarget)) closeMenu();
    });
    window.matchMedia('(max-width: 800px)').addEventListener('change', (event) => {
      if (!event.matches) closeMenu();
    });
  }

  function setupQuoteForm() {
    const form = document.getElementById('quote-form');
    if (!form) return;

    form.addEventListener('submit', (event) => {
      if (!form.reportValidity()) return;
      event.preventDefault();

      const service = document.getElementById('quote-service').value;
      const city = document.getElementById('quote-city').value;
      const description = document.getElementById('quote-description').value.trim();
      const message = [
        'Olá, Hugo! Vim pelo site e gostaria de pedir um orçamento.',
        '',
        `Serviço: ${service}`,
        `Cidade: ${city}`,
        description ? `Detalhes: ${description}` : '',
        '',
        'Podemos conversar sobre o atendimento?',
      ].filter((line, index, lines) => line || (index > 0 && lines[index - 1]))
        .join('\n');

      // Só monta o rascunho. Quem envia é a pessoa, lá no WhatsApp.
      window.location.assign(`https://wa.me/5511983229289?text=${encodeURIComponent(message)}`);
    });
  }

  setupMenu();
  setupQuoteForm();
})();
