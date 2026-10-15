/* Topic 1.2 Variables. Original classroom activities; no network calls or storage.
   Dataset source: ../../Shared/data/foundations.json (generated browser data file).
   Pure helpers are exported for arithmetic regression tests in Node. */
(() => {
  'use strict';
  const TYPES = ['Categorical', 'Quantitative — discrete', 'Quantitative — continuous'];
  const ROLES = ['Sample statistic', 'Population parameter', 'One individual datum'];
  const classify = [
    {question:'For each School A student: the usual main travel method.', answer:0,
     why:'Categorical. Walk, Bicycle, Bus, and Car are group labels. The frequency 18 for Bus is a summary of this categorical variable, not a measurement of travel method.'},
    {question:'For each student: the number of bus trips taken last week.', answer:1,
     why:'Discrete quantitative. Trips are counted, with possible values 0, 1, 2, and so on. A fractional trip count is not possible under this recording rule.'},
    {question:'For each journey: the actual elapsed travel time, subsequently recorded to the nearest minute. Classify the underlying elapsed time.', answer:2,
     why:'Continuous quantitative. Actual time is measured on a continuum. Rounding limits the recorded precision; it does not turn the underlying duration into a count.'},
    {question:'For each bus trip: its route number, such as 10, 20, or 25.', answer:0,
     why:'Categorical. The digits identify routes, not amounts. Subtracting route numbers does not measure a difference in travel distance or duration.'},
    {question:'For each examination: a score from 0 to 10, awarded only in half-point steps.', answer:1,
     why:'Discrete quantitative. The possible scores form a finite grid with 21 values: 0, 0.5, 1, and so on through 10. Having decimals does not make a variable continuous.'},
    {question:'For each viewer: satisfaction recorded as Very dissatisfied through Very satisfied and coded 1–5.', answer:0,
     why:'Categorical, with an order. The codes label satisfaction levels. An order does not establish equal measured gaps between the levels.'},
    {question:'For each parcel: its actual mass, measured in kilograms.', answer:2,
     why:'Continuous quantitative. Mass is a measured quantity that can take values throughout an interval; the instrument reports only finite precision.'},
    {question:'For each fixed-length traffic clip: the number of bicycles passing a marked line.', answer:1,
     why:'Discrete quantitative. The observational unit is a clip, and the value is a whole-number bicycle count for that clip.'},
    {question:'For each photograph: the weather category recorded using a defined coding rule.', answer:0,
     why:'Categorical. The values identify weather groups. A photograph is the recording medium; it does not by itself determine a variable type.'},
    {question:'For each recorded bird call: its actual duration, in seconds.', answer:2,
     why:'Continuous quantitative. Duration is a measured amount, even when the source is an audio recording rather than a spreadsheet.'}
  ];
  const summary = [
    {question:'18 of the 40 sampled School A students use Bus. The number being classified is the sample proportion, 45%.', answer:0,
     why:'Sample statistic. The 45% summarizes the 40 sampled students. The corresponding proportion p for all 1,000 enrolled students is not supplied.'},
    {question:'All 80 parcels in a specified shipment are weighed. With this entire shipment as the population, their mean mass is 2.40 kg.', answer:1,
     why:'Population parameter. The mean summarizes every parcel in the defined population. A parameter can be known after a census.'},
    {question:'The illustrative record for Student A gives that one student’s commute time as 24.0 minutes. Classify this individual recorded time.', answer:2,
     why:'One individual datum. This is a value recorded on one observational unit, not a summary calculated over a sample. It happens to equal the separate School A sample mean numerically.'},
    {question:'For the investigative question about all 1,000 School A students this term, p denotes the proportion who mainly travel by bus. Its value is unknown.', answer:1,
     why:'Population parameter. Its role is determined by the full group it describes, not by whether its value is known. The observed sample proportion 0.45 estimates this target; it is not automatically equal to p.'}
  ];
  function codedMean(counts, codes) {
    if (!Array.isArray(counts) || !Array.isArray(codes) || counts.length !== codes.length || !counts.length)
      throw new TypeError('Counts and codes must be nonempty arrays of equal length.');
    if (counts.some(n => !Number.isInteger(n) || n < 0) || codes.some(n => !Number.isFinite(n)))
      throw new RangeError('Counts must be nonnegative integers and codes must be finite.');
    const total = counts.reduce((a,b) => a+b,0);
    if (!total) throw new RangeError('At least one observation is required.');
    return counts.reduce((a,n,i) => a+n*codes[i],0)/total;
  }
  const model = {classify, summary, types:TYPES, roles:ROLES, codedMean};
  if (typeof module !== 'undefined' && module.exports) module.exports = model;
  if (typeof document === 'undefined') return;
  const esc = x => String(x).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function quiz(root, cases, options, prefix) {
    let index = 0;
    function draw(focus=false) {
      root.dataset.case = String(index);
      root.dataset.selected = '';
      root.dataset.correct = '';
      const item = cases[index];
      root.innerHTML = `<h3 tabindex="-1" data-case-title>Case ${index+1} of ${cases.length}</h3>
        <p class="variable-question">${esc(item.question)}</p>
        <form><fieldset><legend>Choose the best classification</legend>
        ${options.map((text,i) => `<label class="variable-choice"><input type="radio" name="${prefix}-answer" value="${i}"> <span>${esc(text)}</span></label>`).join('')}
        </fieldset><div class="controls"><button type="submit" data-check>Check answer</button>
        <button type="button" data-clear>Clear answer</button><button type="button" data-next>Next case</button>
        <button type="button" data-restart>Restart</button></div></form>
        <p class="status" role="status" aria-live="polite" aria-atomic="true">Choose an answer before checking.</p>`;
      const feedback = root.querySelector('.status');
      root.querySelector('form').addEventListener('submit', event => {
        event.preventDefault();
        const selected = root.querySelector('input:checked');
        if (!selected) { feedback.textContent='Select one classification, then press Check answer.'; return; }
        const correct = Number(selected.value) === item.answer;
        root.dataset.correct = String(correct);
        feedback.textContent = (correct ? 'Correct. ' : 'Not quite. ') + item.why;
      });
      root.querySelectorAll('input').forEach(input => input.addEventListener('change', () => {
        root.dataset.selected=input.value; root.dataset.correct='';
        feedback.textContent='Answer selected. Press Check answer to see the explanation.';
      }));
      root.querySelector('[data-clear]').addEventListener('click', () => {
        root.querySelector('form').reset();root.dataset.selected='';root.dataset.correct='';
        feedback.textContent='Cleared. Choose an answer before checking.';
      });
      root.querySelector('[data-next]').addEventListener('click', () => {index=(index+1)%cases.length;draw(true);});
      root.querySelector('[data-restart]').addEventListener('click', () => {index=0;draw(true);});
      if(focus) root.querySelector('[data-case-title]').focus({preventScroll:true});
    }
    draw();
  }
  function recode(root) {
    const school = window.UNIT1_FOUNDATIONS.school_a;
    const schemes = {
      words:{labels:school.categories, codes:null, explanation:'Words name the categories. There is no numerical code average to interpret.'},
      sequential:{labels:[1,2,3,4], codes:[1,2,3,4], explanation:'These arbitrary codes give an arithmetic average of 2.65, but it is not an average travel method.'},
      alternative:{labels:[4,1,9,2], codes:[4,1,9,2], explanation:'A different arbitrary labelling gives 5.40. The category memberships and counts have not changed.'},
      indicator:{labels:[0,0,1,0], codes:[0,0,1,0], explanation:'This is a derived numerical Bus indicator, not a one-to-one relabelling: Bus is 1 and every other category is 0. Its mean 0.45 equals the Bus proportion, but the indicator loses distinctions between non-Bus categories.'}
    };
    root.innerHTML=`<h3>Same students, different labels</h3><div class="controls"><label>Display labels
      <select data-scheme><option value="words">Category names</option><option value="sequential">Codes 1, 2, 3, 4</option>
      <option value="alternative">Codes 4, 1, 9, 2</option><option value="indicator">Bus indicator: 1 or 0</option></select></label>
      <button type="button" data-reset>Reset labels</button></div>
      <div class="variable-table-wrap" tabindex="0" role="region" aria-label="Travel category and code table"><table>
      <caption>Hypothetical School A sample — 40 students</caption><thead><tr><th scope="col">Category meaning</th><th scope="col">Displayed label</th><th scope="col">Frequency</th></tr></thead><tbody></tbody></table></div>
      <p data-average-label></p><p><strong>Invariant Bus proportion: 18/40 = 45%.</strong></p>
      <p class="status" role="status" aria-live="polite" aria-atomic="true"></p>`;
    const select=root.querySelector('select');
    function draw() {
      const scheme=schemes[select.value];
      root.dataset.scheme=select.value;
      root.dataset.average=scheme.codes ? String(codedMean(school.counts,scheme.codes)) : '';
      root.querySelector('tbody').innerHTML=school.categories.map((name,i) => `<tr><th scope="row">${esc(name)}</th><td>${esc(scheme.labels[i])}</td><td>${school.counts[i]}</td></tr>`).join('');
      root.querySelector('[data-average-label]').textContent=scheme.codes ? `Arithmetic code average: ${codedMean(school.counts,scheme.codes).toFixed(2)}.` : 'Arithmetic code average: not applicable to category names.';
      root.querySelector('.status').textContent=scheme.explanation;
    }
    select.addEventListener('change',draw);
    root.querySelector('[data-reset]').addEventListener('click',()=>{select.value='words';draw();});
    draw();
  }
  document.querySelectorAll('[data-variables="classify"]').forEach(root=>quiz(root,classify,TYPES,'variable-type'));
  document.querySelectorAll('[data-variables="summary"]').forEach(root=>quiz(root,summary,ROLES,'summary-role'));
  document.querySelectorAll('[data-variables="recode"]').forEach(recode);
  window.addEventListener('beforeprint',()=>{
    document.querySelectorAll('.variables-print').forEach(el=>el.remove());
    document.querySelectorAll('[data-variables]').forEach(root=>{
      const node=document.createElement('div');node.className='variables-print';
      const kind=root.dataset.variables;
      if(kind==='recode') node.innerHTML='<h3>Category-code reference</h3><p>School A: Walk 8, Bicycle 6, Bus 18, Car 8 (n = 40). Codes 1/2/3/4 give 2.65; codes 4/1/9/2 give 5.40. Neither is a measured travel method. The numerical Bus indicator has mean 0.45, the Bus share.</p>';
      else {
        const items=kind==='classify'?classify:summary;
        node.innerHTML='<h3>Activity answers and explanations</h3>'+items.map((item,i)=>`<p><strong>${i+1}. ${esc(item.question)}</strong><br>${esc(item.why)}</p>`).join('');
      }
      root.after(node);
    });
  });
  window.addEventListener('afterprint',()=>document.querySelectorAll('.variables-print').forEach(el=>el.remove()));
  window.VARIABLES_TEST = model;
})();
