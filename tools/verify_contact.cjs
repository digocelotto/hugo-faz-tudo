const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../src/site.js'), 'utf8');
function submit(values, valid = true) {
  let listener, destination, prevented = false;
  const form = { addEventListener: (_, fn) => { listener = fn; }, reportValidity: () => valid };
  const elements = { 'quote-form': form, 'quote-service': { value: values.service }, 'quote-city': { value: values.city }, 'quote-description': { value: values.details || '' } };
  vm.runInNewContext(source, { document: { getElementById: id => elements[id] }, window: { location: { assign: url => { destination = url; } } } });
  listener({ preventDefault: () => { prevented = true; } });
  return { destination, prevented };
}
const result = submit({ service: 'Instalação de TV', city: 'Embu das Artes', details: 'TV 50 polegadas & prateleira\nBairro: Centro' });
const url = new URL(result.destination);
assert.equal(url.origin + url.pathname, 'https://wa.me/5511983229289');
assert.equal(result.prevented, true);
assert.match(url.searchParams.get('text'), /Serviço: Instalação de TV/);
assert.match(url.searchParams.get('text'), /Cidade: Embu das Artes/);
assert.match(url.searchParams.get('text'), /TV 50 polegadas & prateleira\nBairro: Centro/);
const second = submit({ service: 'Elétrica', city: 'Taboão da Serra' });
assert.match(new URL(second.destination).searchParams.get('text'), /Taboão da Serra/);
assert.doesNotMatch(new URL(second.destination).searchParams.get('text'), /undefined|Detalhes:/);
assert.equal(submit({ service: '', city: '' }, false).destination, undefined);
vm.runInNewContext(source, { document: { getElementById: () => null } });
console.log('PASS: correct WhatsApp recipient, service/city/details, accents and special characters, optional field, invalid form and pages without form.');
