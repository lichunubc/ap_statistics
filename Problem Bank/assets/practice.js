/* Local class-file reader. No question content or responses are transmitted. */
(() => {
  'use strict';
  const catalog = window.MHSProblemCatalog;
  const roots = [...document.querySelectorAll('.homework-bank')];
  if (!catalog || !roots.length) return;
  const key = 'mhs-ap-statistics-class-file-v1';
  const maxBytes = 8 * 1024 * 1024;
  const metadata = new Map(catalog.items.map(item => [item.id, item]));
  let questions = new Map();
  let saved = false;
  const views = [];
  const text = (value, limit = 10000) => typeof value === 'string' && value.length <= limit;
  const requireThat = (condition, message) => { if (!condition) throw new Error(message); };
  function validateBlock(block) {
    requireThat(block && typeof block === 'object', 'Invalid content block.');
    if (block.type === 'paragraph' || block.type === 'pre') {
      requireThat(text(block.text), 'Invalid text block.');
    } else if (block.type === 'table') {
      requireThat(Array.isArray(block.headers) && block.headers.length > 0 && block.headers.length <= 12 && block.headers.every(x => text(x, 500)), 'Invalid table headers.');
      requireThat(Array.isArray(block.rows) && block.rows.length <= 100 && block.rows.every(row => Array.isArray(row) && row.length === block.headers.length && row.every(x => text(x, 1000))), 'Invalid table rows.');
      requireThat(block.caption === undefined || text(block.caption, 1000), 'Invalid table caption.');
    } else if (block.type === 'figure') {
      requireThat(text(block.alt, 2000) && typeof block.src === 'string' && block.src.length <= 2000000 && /^data:image\/png;base64,iVBORw0KGgo[A-Za-z0-9+/=\r\n]+$/.test(block.src), 'Figures must be embedded PNG images, not external URLs or executable content.');
    } else {
      throw new Error('Unsupported content block.');
    }
  }
  function validateBlocks(blocks) {
    requireThat(Array.isArray(blocks) && blocks.length > 0 && blocks.length <= 30, 'Invalid question content.');
    blocks.forEach(validateBlock);
  }
  function validatePack(pack) {
    requireThat(pack && pack.schema_version === 1 && pack.bank_id === catalog.bank_id && pack.catalog_revision === catalog.revision, 'This class file belongs to a different bank or revision. Ask your teacher for the current file.');
    requireThat(Array.isArray(pack.items) && pack.items.length === catalog.items.length, 'The class file must contain all selected questions.');
    const seen = new Set();
    for (const item of pack.items) {
      requireThat(item && metadata.has(item.id) && !seen.has(item.id), 'Unknown or duplicate question ID.');
      seen.add(item.id);
      validateBlocks(item.blocks);
      requireThat(Array.isArray(item.options) && item.options.length === 4, 'Each question needs four choices.');
      item.options.forEach((option, index) => {
        requireThat(option && option.label === 'ABCD'[index], 'Choices must remain in source order A–D.');
        validateBlocks(option.blocks);
      });
      requireThat(typeof item.answer === 'string' && /^[ABCD]$/.test(item.answer) && text(item.explanation) && item.explanation.length > 0, 'Missing answer or explanation.');
      requireThat(Array.isArray(item.editorial_notes) && item.editorial_notes.length <= 10 && item.editorial_notes.every(x => text(x, 2000)), 'Invalid editorial notes.');
    }
    return pack;
  }
  function el(tag, className, value) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  }
  function statusNode() {
    const p = el('p', 'bank-status');
    p.setAttribute('role', 'status');
    p.setAttribute('aria-live', 'polite');
    p.setAttribute('aria-atomic', 'true');
    return p;
  }
  function renderBlocks(blocks, parent) {
    for (const block of blocks) {
      if (block.type === 'paragraph' || block.type === 'pre') {
        parent.append(el(block.type === 'pre' ? 'pre' : 'p', '', block.text));
      } else if (block.type === 'table') {
        const wrap = el('div', 'bank-table-wrap');
        wrap.tabIndex = 0;
        wrap.setAttribute('role', 'region');
        wrap.setAttribute('aria-label', block.caption || 'Question data table');
        const table = el('table');
        if (block.caption) table.append(el('caption', '', block.caption));
        const head = el('thead'), row = el('tr');
        for (const value of block.headers) {
          const th = el('th', '', value); th.scope = 'col'; row.append(th);
        }
        head.append(row); table.append(head);
        const body = el('tbody');
        for (const values of block.rows) {
          const tr = el('tr');
          values.forEach((value, i) => {
            const cell = el(i === 0 ? 'th' : 'td', '', value);
            if (i === 0) cell.scope = 'row';
            tr.append(cell);
          });
          body.append(tr);
        }
        table.append(body); wrap.append(table); parent.append(wrap);
      } else if (block.type === 'figure') {
        const figure = el('figure', 'bank-figure');
        const image = el('img'); image.src = block.src; image.alt = block.alt; image.loading = 'lazy';
        const expand = el('button', 'bank-figure-button', 'Enlarge figure'); expand.type = 'button';
        expand.addEventListener('click', () => {
          const dialog = el('dialog', 'bank-image-dialog');
          dialog.setAttribute('aria-label', 'Enlarged question figure');
          const close = el('button', '', 'Close figure'); close.type = 'button';
          const large = image.cloneNode(); large.loading = 'eager';
          const wrap = el('div', 'bank-image-scroll'); wrap.append(large);
          dialog.append(close, wrap); document.body.append(dialog);
          close.addEventListener('click', () => dialog.close());
          dialog.addEventListener('close', () => { dialog.remove(); expand.focus(); });
          dialog.showModal(); close.focus();
        });
        figure.append(image, expand); parent.append(figure);
      }
    }
  }
  function card(meta, view) {
    const article = el('article', 'bank-question'); article.id = meta.id;
    const h = el('h3', '', `Week ${meta.source_week} · Question ${meta.source_question}`);
    const source = el('p', 'bank-source', `Source: Week ${meta.source_week} homework, ${meta.source_pages.length === 1 ? 'page' : 'pages'} ${meta.source_pages.join(', ')}.`);
    article.append(h, source);
    const item = questions.get(meta.id);
    if (!item) {
      article.append(el('p', 'bank-locked', 'Open the class question file above to display this question, its original diagrams, and the explanation. You can also work from the homework page listed here.'));
      return article;
    }
    article.dataset.loaded = 'true';
    const body = el('div', 'bank-prompt'); renderBlocks(item.blocks, body); article.append(body);
    const form = el('form'), fieldset = el('fieldset');
    fieldset.append(el('legend', '', 'Choose one answer'));
    for (const option of item.options) {
      const choice = el('div', 'bank-choice');
      const radio = el('input'); radio.type = 'radio'; radio.name = `${view.id}-${item.id}`; radio.value = option.label;
      radio.id = `${view.id}-${item.id}-${option.label}`;
      radio.setAttribute('aria-describedby', `${radio.id}-content`);
      const label = el('label', '', option.label + '.'); label.htmlFor = radio.id;
      const content = el('div', 'bank-choice-content'); content.id = `${radio.id}-content`;
      renderBlocks(option.blocks, content);
      if (view.answers.get(item.id) === option.label) radio.checked = true;
      choice.append(radio, label, content);
      content.addEventListener('click', event => {
        if (event.target.closest('button, a')) return;
        radio.checked = true; radio.dispatchEvent(new Event('change'));
      });
      radio.addEventListener('change', () => {
        view.answers.set(item.id, radio.value); feedback.textContent = ''; feedback.removeAttribute('data-result'); solution.open = false;
      });
      fieldset.append(choice);
    }
    const controls = el('div', 'bank-question-controls');
    const check = el('button', '', 'Check answer'); check.type = 'submit';
    const reset = el('button', '', 'Reset question'); reset.type = 'button';
    controls.append(check, reset);
    const feedback = statusNode(); feedback.classList.add('bank-feedback');
    const solution = el('details', 'bank-solution');
    solution.append(el('summary', '', 'Show answer and explanation'), el('p', '', `Answer: ${item.answer}. ${item.explanation}`));
    form.append(fieldset, controls, feedback);
    form.addEventListener('submit', event => {
      event.preventDefault();
      const selected = form.querySelector('input:checked');
      if (!selected) { feedback.textContent = 'Choose an answer before checking.'; return; }
      const correct = selected.value === item.answer;
      feedback.dataset.result = correct ? 'correct' : 'incorrect';
      feedback.textContent = correct ? 'Correct. Open the explanation to check your reasoning.' : 'Not yet. Review the question and try again, or open the explanation.';
    });
    reset.addEventListener('click', () => {
      form.reset(); form.querySelectorAll('input').forEach(input => { input.checked = false; });
      view.answers.delete(item.id); feedback.textContent = ''; feedback.removeAttribute('data-result'); solution.open = false;
    });
    article.append(form, solution);
    return article;
  }
  function render(view) {
    const query = view.search.value.trim().toLowerCase();
    const topic = view.select ? view.select.value : view.topic;
    const matches = catalog.items.filter(meta => (topic === 'all' || meta.topic === topic) && `${meta.id} ${meta.title} ${meta.skills.join(' ')} week ${meta.source_week} question ${meta.source_question}`.toLowerCase().includes(query));
    view.list.replaceChildren(...matches.map(meta => card(meta, view)));
    view.count.textContent = `${matches.length} selected ${matches.length === 1 ? 'question' : 'questions'}${questions.size ? ' · class file open' : ' · source references only'}`;
    if (!matches.length) view.list.append(el('p', '', 'No selected questions match this filter.'));
  }
  function refresh(message) {
    for (const view of views) {
      view.notice.textContent = message;
      view.forget.disabled = !questions.size;
      render(view);
    }
  }
  try {
    const raw = sessionStorage.getItem(key);
    if (raw) { const pack = validatePack(JSON.parse(raw)); questions = new Map(pack.items.map(item => [item.id, item])); saved = true; }
  } catch (_) { try { sessionStorage.removeItem(key); } catch (_) {} }
  roots.forEach((root, index) => {
    const view = {id: `bank-${index}`, topic: root.dataset.topic || 'all', answers: new Map()};
    root.replaceChildren(); root.dataset.bankReady = 'true';
    const box = el('div', 'bank-loader');
    const label = el('label', 'bank-file-label', 'Open class question file');
    const input = el('input'); input.type = 'file'; input.accept = '.json,application/json'; input.id = `${view.id}-file`; label.htmlFor = input.id;
    const privacy = el('p', 'bank-privacy', 'Open mhs-week-2-3.practice.json provided by your teacher. Use Forget class file to clear it from this tab.');
    view.forget = el('button', '', 'Forget class file'); view.forget.type = 'button';
    view.notice = statusNode();
    box.append(label, input, privacy, view.forget, view.notice);
    const filters = el('div', 'bank-filters');
    if (view.topic === 'all') {
      const topicLabel = el('label', '', 'Topic');
      view.select = el('select'); view.select.setAttribute('aria-label', 'Filter selected questions by topic');
      const all = el('option', '', 'All selected topics'); all.value = 'all'; view.select.append(all);
      for (const topic of [...new Set(catalog.items.map(meta => meta.topic))]) {
        const option = el('option', '', `Topic ${topic} — ${catalog.topics[topic]}`); option.value = topic; view.select.append(option);
      }
      topicLabel.append(view.select); filters.append(topicLabel);
      view.select.addEventListener('change', () => render(view));
    }
    const searchLabel = el('label', '', 'Find a question');
    view.search = el('input'); view.search.type = 'search'; view.search.placeholder = 'Skill, question number, or ID';
    view.search.setAttribute('aria-label', 'Find a selected question'); searchLabel.append(view.search); filters.append(searchLabel);
    view.count = statusNode(); view.list = el('div', 'bank-question-list');
    view.search.addEventListener('input', () => render(view));
    input.addEventListener('change', async () => {
      const file = input.files[0]; if (!file) return;
      try {
        requireThat(file.size <= maxBytes, 'The class file is too large (maximum 8 MB).');
        const pack = validatePack(JSON.parse(await file.text()));
        questions = new Map(pack.items.map(item => [item.id, item]));
        views.forEach(v => v.answers.clear()); saved = false;
        try { sessionStorage.setItem(key, JSON.stringify(pack)); saved = true; } catch (_) {}
        refresh(saved ? 'Class file open for this tab. Choose an answer below.' : 'Class file open for this page only. Browser storage is unavailable; reopen the file after changing pages.');
      } catch (error) {
        view.notice.textContent = `Could not open this file: ${error instanceof SyntaxError ? 'Choose the JSON class question file, not a PDF.' : error.message} The previously opened class file, if any, is unchanged.`;
      } finally { input.value = ''; }
    });
    view.forget.addEventListener('click', () => {
      questions.clear(); saved = false;
      try { sessionStorage.removeItem(key); } catch (_) {}
      document.querySelectorAll('.bank-image-dialog').forEach(dialog => dialog.close());
      views.forEach(v => v.answers.clear());
      refresh('Class file removed from this tab. Only source references remain.');
    });
    root.append(box, filters, view.count, view.list); views.push(view);
  });
  refresh(saved ? 'Class file restored for this tab. Responses are not submitted or carried between pages.' : 'No class file is open. The references below identify the selected homework questions.');
  window.MHSProblemBank = Object.freeze({validatePack});
})();
