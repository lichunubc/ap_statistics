import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, realpathSync } from 'node:fs';
import { relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const html = readFileSync(new URL('../assets/expanded-bank.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const hash = createHash('sha256').update(script).digest('base64');
const csp = html.match(/http-equiv="Content-Security-Policy" content="([^"]+)"/)[1];
for (const directive of ["default-src 'none'", "connect-src 'none'", "img-src blob:", "form-action 'none'", `script-src 'sha256-${hash}'`]) {
  assert.ok(csp.split('; ').includes(directive));
}
assert.doesNotMatch(html, /<(?:script[^>]+src|img[^>]+src|iframe\b|link\b|form\b)/i);
assert.doesNotMatch(script, /\b(?:innerHTML|outerHTML|insertAdjacentHTML|fetch|XMLHttpRequest|WebSocket|sendBeacon|localStorage|sessionStorage|indexedDB)\b/);

const downloaded = [];
const ids = new Map();
const urls = new Map();
const scheduled = [];
let nextURL = 0;
let activeElement;
const walk = node => [node, ...node.children.flatMap(walk)];

// This small DOM facade exercises event and rendering logic. It does not render a browser page.
class Element {
  constructor(tag, text = '') {
    this.tagName = tag;
    this.children = [];
    this.parent = null;
    this.attributes = {};
    this.handlers = new Map();
    this.text = text;
    this.value = '';
  }

  set textContent(value) {
    this.replaceChildren();
    this.text = String(value);
  }

  get textContent() {
    return this.text + this.children.map(child => child.textContent).join('');
  }

  setAttribute(key, value) {
    this.attributes[key] = String(value);
  }

  append(...children) {
    for (const child of children) {
      child.parent = this;
      this.children.push(child);
    }
  }

  add(option) {
    this.append(option);
  }

  replaceChildren(...children) {
    for (const child of this.children) child.parent = null;
    this.children = [];
    this.text = '';
    this.append(...children);
  }

  remove() {
    this.parent.children = this.parent.children.filter(child => child !== this);
    this.parent = null;
  }

  get isConnected() {
    return this === document.body || this.parent?.isConnected === true;
  }

  addEventListener(type, fn) {
    if (!this.handlers.has(type)) this.handlers.set(type, []);
    this.handlers.get(type).push(fn);
  }

  async fire(type) {
    await Promise.all((this.handlers.get(type) || []).map(fn => fn({ target: this })));
  }

  click() {
    if (this.download) downloaded.push({ name: this.download, blob: urls.get(this.href) });
    return this.fire('click');
  }

  focus() {
    activeElement = this;
  }

  querySelector(selector) {
    assert.equal(selector, 'input:checked');
    return walk(this).find(child => child.tagName === 'input' && child.checked);
  }
}

const document = {
  body: new Element('body'),
  createElement: tag => new Element(tag),
  createTextNode: text => new Element('#text', text),
  getElementById: id => ids.get(id) || walk(document.body).find(node => node.id === id),
  get activeElement() { return activeElement; }
};

for (const [, tag, id] of html.matchAll(/<([a-z0-9]+)[^<>]*?\sid="([^"]+)"/g)) {
  const element = new Element(tag);
  element.id = id;
  ids.set(id, element);
  document.body.append(element);
}

const context = vm.createContext({
  document, URLSearchParams, Blob, location: { search: '?skill=rate-check' },
  URL: {
    createObjectURL(blob) {
      const url = 'blob:test/' + ++nextURL;
      urls.set(url, blob);
      return url;
    },
    revokeObjectURL(url) { urls.delete(url); }
  },
  Option: class extends Element {
    constructor(label, value) {
      super('option', label);
      this.value = value;
    }
  },
  setTimeout(fn) { scheduled.push(fn); }
});
vm.runInContext(script, context, { filename: 'expanded-bank.html' });
const $ = document.getElementById;
const find = (node, tag, text) => walk(node).find(child => child.tagName === tag && child.textContent === text);
const localJSON = (name, data) => {
  const raw = typeof data === 'string' ? data : JSON.stringify(data);
  return { name, size: Buffer.byteLength(raw), text: async () => raw };
};

const malicious = '<img src="https://example.invalid/unsafe" onerror="globalThis.injected = true">';
const mcq = {
  id: 'original-demo-mcq', title: 'Garden rate', question_text: 'Which rate compares sprouted seeds to all planted seeds? ' + malicious,
  question_html: '<script>globalThis.rawHTMLInjected = true</script>',
  Source: 'Practice Exam', practice_exam: 'Garden exercise', Type: 'MCQ', Current: 'Yes', year: null,
  unit_ids: ['u1'], knowledge_component_ids: ['rate-check'],
  choices: [{ label: 'A', text: 'Sprouted divided by planted' }, { label: 'B', text: 'Planted divided by sprouted' }],
  correct_choice: 'A', answer_overview: 'Use the number planted as the denominator.',
  question_page_assets: [
    { src: 'https://example.invalid/assets/garden.jpg' }, { src: 'assets/../secret.jpg' },
    { src: 'assets/fake.jpg' }, { src: 'assets/duplicate.jpg' }, { src: 'assets/garden.jpg', page: 3 }
  ],
  alignment: { topics: ['demo alignment'] }, parts: []
};
const frq = {
  id: 'original-demo-frq', title: 'Seed packet count', question_text: 'Explain how to choose a sample of seed packets.',
  Source: 'Past Exam', Type: 'FRQ', Current: 'No', year: 2024, form: 'Example',
  unit_ids: ['u1'], knowledge_component_ids: ['plan-sample'],
  parts: [{ label: 'a', prompt: 'Explain how to choose a sample of seed packets.', answer_summary: 'Use random labels.', max_points: 1 }]
};
const progress = {
  ...mcq, id: 'original-demo-pc', title: 'Flower comparison', Source: 'Progress Check', Unit: 'Unit Demo', progress_check_part: 'A'
};
const fixture = {
  schema_version: '1.2.0', metadata: { question_count: 3 },
  taxonomy: {
    units: [{ id: 'u1', label: 'Gardening statistics' }],
    knowledge_components: [{ id: 'rate-check', label: 'Compare garden rates' }, { id: 'plan-sample', label: 'Plan a sample' }]
  },
  sources: [{ filename: 'demo-source.pdf', sha256: 'a'.repeat(64) }],
  questions: [mcq, frq, progress]
};

async function openFile(file) {
  $('bank-file').files = [file];
  await $('bank-file').fire('change');
}

await openFile(localJSON('synthetic-bank.json', fixture));
assert.match($('file-status').textContent, /3 questions loaded/);
assert.equal($('skill').value, 'rate-check');
assert.match($('results-status').textContent, /2 matching/);
assert.equal($('workspace').hidden, false);
await $('reset-filters').click();
assert.match($('results-status').textContent, /3 matching/);
$('search').value = 'garden sprouted';
await $('search').fire('input');
assert.match($('results-status').textContent, /2 matching/);
$('source').value = 'Practice Exam';
await $('source').fire('change');
assert.match($('results-status').textContent, /1 matching/);
await $('results').children[0].children[0].click();
assert.equal(document.activeElement.id, 'question-title');
assert.ok($('question').textContent.includes(malicious));
assert.ok(!find($('question'), 'img', ''));
assert.ok(!$('question').textContent.includes('globalThis.rawHTMLInjected'));
assert.equal(context.injected, undefined);
assert.ok(!find($('question'), 'summary', 'Show solution and scoring').parent.open);
await find($('question'), 'button', 'Check answer').click();
assert.match($('question').textContent, /Choose an option first/);
const options = walk($('question')).filter(node => node.tagName === 'input');
options[1].checked = true;
await find($('question'), 'button', 'Check answer').click();
assert.match($('question').textContent, /Try again/);
options[1].checked = false;
options[0].checked = true;
await find($('question'), 'button', 'Check answer').click();
assert.match($('question').textContent, /Correct/);

const raster = (name, bytes) => Object.assign(new Blob([new Uint8Array(bytes)]), { webkitRelativePath: name });
$('asset-files').files = [
  raster('package/assets/garden.jpg', [255, 216, 255, 217]),
  raster('package/assets/fake.jpg', [60, 115, 118, 103]),
  raster('package/one/assets/duplicate.jpg', [255, 216, 255]),
  raster('package/two/assets/duplicate.jpg', [255, 216, 255]),
  raster('package/assets/not-a-photo.svg', [255, 216, 255])
];
await $('asset-files').fire('change');
await find($('question'), 'button', 'Show question pages').click();
const images = walk($('question')).filter(node => node.tagName === 'img');
assert.equal(images.length, 1);
assert.equal(urls.get(images[0].src).type, 'image/jpeg');
assert.match(images[0].alt, /page 3/);
assert.match($('question').textContent, /Some source pages are unavailable/);

await find($('question'), 'button', 'Add to selection').click();
assert.equal($('selected-count').textContent, '1 selected');
assert.equal(find($('question'), 'button', 'Remove from selection').attributes['aria-pressed'], 'true');
await $('download').click();
assert.equal(downloaded.length, 1);
assert.equal(downloaded[0].name, 'ap_statistics_selected_questions.json');
const exported = JSON.parse(await downloaded[0].blob.text());
assert.deepEqual(exported.questions, [mcq]);
assert.deepEqual(exported.sources, fixture.sources);
assert.deepEqual(exported.taxonomy, fixture.taxonomy);
assert.equal(exported.metadata.question_count, 1);
assert.deepEqual(exported.metadata.papers, []);
assert.deepEqual(exported.metadata.practice_exams, [{ name: 'Garden exercise', question_count: 1, type_counts: { MCQ: 1, FRQ: 0 } }]);
scheduled.splice(0).forEach(fn => fn());
assert.equal(urls.size, 1);

$('only-selected').checked = true;
await $('only-selected').fire('change');
await find($('question'), 'button', 'Remove from selection').click();
assert.match($('results-status').textContent, /No matching/);
assert.equal(document.activeElement, $('only-selected'));
assert.equal(urls.size, 0);

await openFile(localJSON('subset.json', exported));
assert.match($('file-status').textContent, /1 questions loaded/);
await openFile(localJSON('invalid.json', '<html>'));
assert.match($('file-status').textContent, /does not contain valid JSON.*previous bank is still open/);
assert.match($('results-status').textContent, /1 matching/);
await openFile(localJSON('duplicate.json', { ...fixture, questions: [mcq, mcq] }));
assert.match($('file-status').textContent, /unique ID/);
await openFile(localJSON('wrong-shape.json', { metadata: {} }));
assert.match($('file-status').textContent, /version 1 AP Statistics/);

const paged = Array.from({ length: 31 }, (_, index) => ({ ...mcq, id: 'synthetic-' + index }));
await openFile(localJSON('paged.json', { ...fixture, questions: paged }));
assert.match($('results-status').textContent, /31 matching · page 1 of 2/);
assert.equal($('results').children.length, 30);
$('next').focus();
await $('next').click();
assert.match($('results-status').textContent, /page 2 of 2/);
assert.equal($('results').children.length, 1);
assert.equal(document.activeElement, $('previous'));

$('search').value = 'previous search text';
$('only-selected').checked = true;
let finishRead;
const pending = openFile({ name: 'waiting.json', size: 1, text: () => new Promise(resolve => { finishRead = resolve; }) });
await $('clear-bank').click();
finishRead(JSON.stringify(fixture));
await pending;
assert.equal($('workspace').hidden, true);
assert.equal($('file-status').textContent, 'Local files cleared.');
assert.equal($('results').children.length, 0);
assert.equal($('asset-files').disabled, true);
assert.equal($('search').value, '');
assert.equal($('only-selected').checked, false);
assert.equal($('selected-count').textContent, '0 selected');
assert.equal(document.activeElement, $('bank-file'));

context.fixtureData = fixture;
const allExport = JSON.parse(vm.runInContext('JSON.stringify(exportSelection(fixtureData, new Set(fixtureData.questions.map(q => q.id))))', context));
assert.deepEqual(allExport.metadata.papers, [{ year: 2024, form: 'Example', question_count: 1 }]);
assert.deepEqual(allExport.metadata.progress_check_sets, [{ unit: 'Unit Demo', type: 'MCQ', part: 'A', question_count: 1 }]);
assert.equal(allExport.metadata.subpart_count, 1);
console.log('Expanded bank CSP, local import, filtering, inert text, choice checking, figures, selection/export, pagination and clear passed in the Node DOM facade.');

if (process.env.APSTATS_PRIVATE_BANK) {
  const root = fileURLToPath(new URL('../..', import.meta.url));
  const path = realpathSync(process.env.APSTATS_PRIVATE_BANK);
  assert.ok(relative(root, path).startsWith('..' + sep), 'Private test input must be outside the repository.');
  const data = readFileSync(path);
  assert.equal(createHash('sha256').update(data).digest('hex'), '15f7800d3f3c83fbd68eb0c8d22460711a9cebc88e76122b60ed5062a231587a');
  context.canonicalText = data.toString('utf8');
  const counts = JSON.parse(vm.runInContext(`JSON.stringify((() => {
    const parsed = parseBank(canonicalText);
    const value = parsed.value;
    const exportAll = exportSelection(value, new Set(parsed.questionRows.map(row => row.question.id)));
    return {
      questions: parsed.questionRows.length, skills: parsed.skillLabels.size,
      units: parsed.unitLabels.size, sources: value.sources.length,
      parts: exportAll.metadata.subpart_count,
      exactRecords: exportAll.questions.every((question, index) => question === value.questions[index]),
      exactTaxonomy: exportAll.taxonomy === value.taxonomy,
      exactSources: exportAll.sources === value.sources,
      everyTaxonomyId: parsed.questionRows.every(row =>
        row.unitIds.length === row.question.unit_ids.length &&
        row.skillIds.length === row.question.knowledge_component_ids.length),
      choices: parsed.questionRows.filter(row =>
        row.type === 'MCQ' && row.question.choices.some(choice => choice.label === row.question.correct_choice)
      ).length
    };
  })())`, context));
  assert.deepEqual(counts, {
    questions: 488, skills: 200, units: 11, sources: 112, parts: 778,
    exactRecords: true, exactTaxonomy: true, exactSources: true, everyTaxonomyId: true, choices: 261
  });
  console.log('Verified private v7 input outside the repository. Parsed 488 questions, 778 parts, 200 skill IDs, 11 units and 112 source records. Whole-record exports preserve payloads.');
}
