const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const menuEvents = {};
const documentEvents = {};
let resize;
let focused = false;
const inside = {};
const toggle = { focus: () => { focused = true; } };
const menu = {
  open: true,
  querySelector: () => toggle,
  contains: (target) => target === inside,
  addEventListener: (event, handler) => { menuEvents[event] = handler; },
};

vm.runInNewContext(
  fs.readFileSync(path.join(__dirname, '../src/site.js'), 'utf8'),
  {
    document: {
      getElementById: (id) => id === 'mobile-menu' ? menu : null,
      addEventListener: (event, handler) => { documentEvents[event] = handler; },
    },
    window: {
      matchMedia: () => ({ addEventListener: (_, handler) => { resize = handler; } }),
    },
  },
);

documentEvents.click({ target: inside });
assert.equal(menu.open, true);
documentEvents.click({ target: {} });
assert.equal(menu.open, false);

menu.open = true;
menuEvents.click({ target: { closest: () => ({}) } });
assert.equal(menu.open, false);

menu.open = true;
let prevented = false;
documentEvents.keydown({ key: 'Escape', preventDefault: () => { prevented = true; } });
assert.equal(menu.open, false);
assert.equal(focused, true);
assert.equal(prevented, true);

menu.open = true;
menuEvents.focusout({ relatedTarget: inside });
assert.equal(menu.open, true);
menuEvents.focusout({ relatedTarget: null });
assert.equal(menu.open, true);
menuEvents.focusout({ relatedTarget: {} });
assert.equal(menu.open, false);

menu.open = true;
resize({ matches: true });
assert.equal(menu.open, true);
resize({ matches: false });
assert.equal(menu.open, false);

console.log('PASS: menu fecha ao navegar, clicar fora, sair pelo teclado e mudar para desktop; Escape devolve o foco.');
