/* Topic 1.3: local, reproducible categorical-table activities. No network or persistence. */
(() => {
  'use strict';
  const labels = ['Walk', 'Bicycle', 'Bus', 'Car'];
  const counts = [8, 6, 18, 8];
  const n = counts.reduce((a, b) => a + b, 0);
  const esc = value => String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const pct = (value, denom) => denom === 0 ? '—' : (100 * value / denom).toFixed(1).replace(/\.0$/, '') + '%';
  const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);

  // This is a deterministic teaching shuffle of hypothetical totals, not collection-order data.
  const shuffled = counts.flatMap((count, category) => Array(count).fill(category));
  let state = 20261013;
  const random = () => { state = (Math.imul(1664525, state) + 1013904223) >>> 0; return state / 4294967296; };
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  const tally = amount => {
    const groups = Array(Math.floor(amount / 5)).fill('||||/');
    if (amount % 5) groups.push('|'.repeat(amount % 5));
    return groups.join(' ') || '—';
  };
  function tableHtml(data, active, processed) {
    const rows = labels.map((name, i) => {
      const recent = active === i ? '<span class="cat-recent">Latest</span>' : '';
      return '<tr data-category="' + i + '"' + (active === i ? ' class="cat-current"' : '') + '><th scope="row">' +
        name + ' ' + recent + '</th><td class="cat-tallies">' + tally(data[i]) + '</td><td>' + data[i] +
        '</td><td>' + pct(data[i], processed) + '</td></tr>';
    }).join('');
    return '<div class="table-responsive"><table class="compact-table cat-table"><caption>Processed responses: ' +
      processed + ' of ' + n + '. Percentages refer to responses processed so far.</caption>' +
      '<thead><tr><th scope="col">Method</th><th scope="col">Tally</th><th scope="col">Count</th><th scope="col">Relative share</th></tr></thead>' +
      '<tbody>' + rows + '</tbody><tfoot><tr><th scope="row">Total</th><td>—</td><td>' +
      processed + '</td><td>' + pct(processed, processed) + '</td></tr></tfoot></table></div>';
  }
  function tallyActivity(root) {
    let step = 0;
    root.innerHTML = '<h3>School A · one-response tally builder</h3>' +
      '<p class="small-note">A simulated order from the fixed hypothetical total of 40 responses. Percentages while building use the number tallied so far; at completion, the denominator is 40.</p>' +
      '<div class="controls"><button type="button" data-add-one class="primary">Record 1</button>' +
      '<button type="button" data-add-five>Record 5</button>' +
      '<button type="button" data-finish>Complete all 40</button>' +
      '<button type="button" data-reset>Reset</button></div>' +
      '<div data-display></div><p class="status" role="status" aria-live="polite"></p>';
    const display = root.querySelector('[data-display]');
    const update = () => {
      const running = [0, 0, 0, 0];
      shuffled.slice(0, step).forEach(category => { running[category]++; });
      const active = step ? shuffled[step - 1] : null;
      display.innerHTML = tableHtml(running, active, step);
      root.dataset.processed = String(step);
      root.dataset.counts = running.join(',');
      root.querySelector('[data-add-one]').disabled = step === n;
      root.querySelector('[data-add-five]').disabled = step === n;
      root.querySelector('[data-finish]').disabled = step === n;
      root.querySelector('[data-reset]').disabled = step === 0;
      root.querySelector('.status').textContent = step === 0 ?
        'Ready: 0 of 40 responses recorded. No categories selected and no percentages computed yet.' :
        step === n ?
        'Completed: 40 of 40 responses. Walk 8 (20%), Bicycle 6 (15%), Bus 18 (45%), Car 8 (20%). Frequencies total 40 and relative frequencies total 100%.' :
        step + ' of 40 responses recorded. Latest category: ' + labels[active] + '. The percentages describe only the ' + step + ' responses processed so far.';
    };
    root.querySelector('[data-add-one]').addEventListener('click', () => { step = Math.min(n, step + 1); update(); });
    root.querySelector('[data-add-five]').addEventListener('click', () => { step = Math.min(n, step + 5); update(); });
    root.querySelector('[data-finish]').addEventListener('click', () => { step = n; update(); });
    root.querySelector('[data-reset]').addEventListener('click', () => { step = 0; update(); });
    update();
  }

  function denominatorActivity(root) {
    const options = labels.map((label, i) => '<option value="' + i + '">' + label + '</option>').join('');
    root.innerHTML = '<h3>Which group is the denominator?</h3><div class="controls">' +
      '<label>Category being described <select data-numerator aria-label="Numerator category">' + options + '</select></label>' +
      '<label>Compare with <select data-comparison aria-label="Denominator group"><option value="all">All 40 sampled students</option>' +
      options + '</select></label><button type="button" data-reset>Reset</button></div>' +
      '<div class="cat-math" aria-live="off"></div><p class="status" role="status" aria-live="polite"></p>';
    const numerator = root.querySelector('[data-numerator]');
    const compare = root.querySelector('[data-comparison]');
    numerator.value = '2'; compare.value = 'all';
    function render() {
      const a = Number(numerator.value), reference = compare.value;
      const total = reference === 'all' ? n : counts[Number(reference)];
      const ratio = counts[a] / total;
      const isWhole = reference === 'all';
      const numeratorLabel = labels[a];
      const denominatorLabel = isWhole ? 'all 40 sampled students' : labels[Number(reference)] + ' respondents';
      const g = gcd(counts[a], total);
      root.dataset.numerator = String(a);
      root.dataset.denominator = String(reference);
      root.querySelector('.cat-math').innerHTML = '<p><strong>' + counts[a] + ' / ' + total + '</strong> = ' +
        ratio.toFixed(3).replace(/0+$/, '').replace(/\.$/, '') +
        (isWhole ? ' = <strong>' + pct(counts[a], total) + '</strong>' : '') +
        '</p><p>Labelled ratio: <strong>' + numeratorLabel + ' to ' +
        (isWhole ? 'all' : labels[Number(reference)]) + ' = ' + counts[a] + ':' + total +
        ' = ' + (counts[a] / g) + ':' + (total / g) + '</strong></p>';
      root.querySelector('.status').textContent = isWhole ?
        'Part to whole: ' + counts[a] + ' of the ' + n + ' sampled students reported ' +
          numeratorLabel + ', which is ' + pct(counts[a], n) + ' of the sample.' :
        'Part to part: among the recorded single-response counts, ' + numeratorLabel +
          ' has ' + counts[a] + ' observations, while ' + labels[Number(reference)] +
          ' has ' + total + '. The quotient ' + ratio.toFixed(2) +
          ' compares these category counts; it is not a percentage of all 40 respondents.';
      root.querySelector('.cat-math').setAttribute('aria-label','Numerator '+numeratorLabel+'; denominator '+denominatorLabel);
    }
    numerator.addEventListener('change', render);
    compare.addEventListener('change', render);
    root.querySelector('[data-reset]').addEventListener('click', () => { numerator.value='2';compare.value='all';render(); });
    render();
  }

  const cases = [
    {
      question:'Which statement is justified by the School A frequency table?',
      choices:['A majority of the 40 sampled students chose Bus.','Bus was the most common individual category in the sample.','Exactly 45% of the full population of 1,000 students chose Bus.','Bus and Car have the same frequency.'],
      correct:1,
      why:'Bus has 18 responses, more than Walk (8), Bicycle (6), or Car (8), so it is the modal category. But 18/40=45%, less than a majority. A sample does not determine the exact population percentage.'
    },
    {
      question:'What proportion of the 40 respondents chose Walk OR Bicycle?',
      choices:['35% (14 of 40)','15% (6 of 40)','65% (26 of 40)','14% (14 of 100)'],
      correct:0,
      why:'Walk and Bicycle are mutually exclusive in this one-response table, so the combined count is 8+6=14. The correct denominator remains all 40 sample responses; 14/40=35%.'
    },
    {
      question:'What is the correctly labelled ratio of Bus to Car responses?',
      choices:['18:40, Bus to all responses','18:8, Bus to Car','8:18, Bus to Car','45:100, Bus to Car'],
      correct:1,
      why:'Bus to Car compares the 18 Bus responses directly with the 8 Car responses: 18:8 = 9:4. The ratio 18:40 instead compares Bus to all sample responses.'
    },
    {
      question:'Why can the category totals in a choose-all-that-apply survey exceed the number of respondents?',
      choices:['All survey percentages must sum to 100%.','Relative frequencies are never meaningful for categories.','The same person may be counted in several categories.','A sample is automatically a census.'],
      correct:2,
      why:'When answers overlap, one respondent can appear in multiple category counts. Dividing category counts by the number of people then gives separate selection rates, not a one-answer categorical distribution summing to 100%.'
    }
  ];
  function quizActivity(root) {
    let index = 0;
    root.innerHTML = '<h3>Explain the evidence</h3><div class="controls"><button type="button" data-next>Next case</button>' +
      '<button type="button" data-clear>Clear answer</button></div>' +
      '<p class="small-note" data-progress></p><p data-question class="cat-question"></p>' +
      '<div class="choice-list"></div><p class="status" role="status" aria-live="polite"></p>';
    function render() {
      const example = cases[index];
      root.dataset.case = String(index);
      root.dataset.selected = '';
      root.querySelector('[data-progress]').textContent = 'Case ' + (index + 1) + ' of ' + cases.length;
      root.querySelector('[data-question]').textContent = example.question;
      root.querySelector('.choice-list').innerHTML = example.choices.map((choice, i) =>
        '<button type="button" data-option="' + i + '" aria-pressed="false"><strong>' +
        String.fromCharCode(65 + i) + '.</strong> ' + esc(choice) + '</button>').join('');
      root.querySelector('.status').textContent = 'No answer selected yet. Choose one option.';
      root.querySelectorAll('[data-option]').forEach(button => button.addEventListener('click', () => {
        const selected = Number(button.dataset.option);
        root.dataset.selected = String(selected);
        root.querySelectorAll('[data-option]').forEach(b => {
          b.setAttribute('aria-pressed','false');
          b.classList.remove('correct','incorrect');
        });
        button.setAttribute('aria-pressed','true');
        button.classList.add(selected === example.correct ? 'correct' : 'incorrect');
        root.querySelector('.status').textContent =
          (selected === example.correct ? 'Correct. ' : 'Not quite. ') + example.why;
      }));
    }
    root.querySelector('[data-next]').addEventListener('click', () => {
      index = (index + 1) % cases.length; render();
    });
    root.querySelector('[data-clear]').addEventListener('click', render);
    render();
  }

  const builders = {tally:tallyActivity, denominator:denominatorActivity, claim:quizActivity};
  document.querySelectorAll('[data-cat-table]').forEach(root => {
    const make = builders[root.dataset.catTable];
    if (make) make(root);
  });
  const references = {
    tally: '<h3>Completed one-response frequency table</h3>' + tableHtml(counts, null, n),
    denominator: '<h3>Denominator reference</h3><p>Bus as part of all sampled students: 18/40 = 45%. Bus to Car: 18:8 = 9:4. Bus within the Bus-or-Bicycle subset: 18/(18+6) = 75%.</p>',
    claim: '<h3>Checkpoint answer key</h3>' + cases.map((c, i) =>
      '<p><strong>Case ' + (i+1) + ': ' + String.fromCharCode(65 + c.correct) + '.</strong> ' +
      esc(c.choices[c.correct]) + ' ' + esc(c.why) + '</p>').join('')
  };
  let printed = [];
  const clearPrint = () => { printed.forEach(node => node.remove()); printed = []; };
  window.addEventListener('beforeprint', () => {
    clearPrint();
    document.querySelectorAll('[data-cat-table]').forEach(root => {
      const node = document.createElement('div');
      node.className = 'cat-print';
      node.innerHTML = references[root.dataset.catTable] || '';
      root.after(node);
      printed.push(node);
    });
  });
  window.addEventListener('afterprint', clearPrint);
  window.CAT_TABLE_TEST = Object.freeze({
    counts:Object.freeze(counts.slice()),
    sampleOrder:Object.freeze(shuffled.slice()),
    n,
    answerKeys:Object.freeze(cases.map(c => c.correct))
  });
})();
