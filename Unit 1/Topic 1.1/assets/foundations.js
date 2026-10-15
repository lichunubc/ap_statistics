/* Maple Hill School foundations components. No network, storage, or learner tracking. */
(() => {
  'use strict';
  const N = 1000;
  const escape = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  // Reproducible partial Fisher-Yates sampling, without replacement.
  function sampleIndices(n, seed) {
    if (!Number.isInteger(n) || n < 0 || n > N) throw new RangeError('Invalid sample size');
    let state = seed >>> 0;
    const random = () => { state = (Math.imul(1664525, state) + 1013904223) >>> 0; return state / 4294967296; };
    const ids = Array.from({length:N}, (_, i) => i);
    for (let i = 0; i < n; i++) {
      const j = i + Math.floor(random() * (N-i));
      [ids[i],ids[j]] = [ids[j],ids[i]];
    }
    return ids.slice(0,n);
  }
  function population(root) {
    let n = 40, seed = 8126;
    root.innerHTML = '<h3>One population, different selections</h3><div class="controls"><label>Number selected <select data-size aria-label="Number of students selected"><option value="10">10 students</option><option value="40" selected>40 students</option><option value="100">100 students</option><option value="1000">All 1,000: census</option></select></label><button type="button" data-draw>Draw another selection</button><button type="button" data-reset>Reset</button></div><div class="foundation-grid"></div><p class="status" role="status" aria-live="polite"></p><p class="small-note">Teal marks with dark outlines are selected; pale marks are not. Each mark is one student. The grid positions are not measurements.</p>';
    function render() {
      const selected = new Set(sampleIndices(n, seed));
      const dots = Array.from({length:N}, (_,i) => `<circle cx="${14+(i%40)*17}" cy="${15+Math.floor(i/40)*13}" r="3.5" class="${selected.has(i)?'selected':'unselected'}"/>`).join('');
      root.querySelector('.foundation-grid').innerHTML = `<svg viewBox="0 0 700 346" role="img" aria-label="${n} selected students inside a fixed population of 1,000"><title>Population and selected group</title><desc>All 1,000 marks represent the population. ${n} marked students form the selected group.</desc>${dots}</svg>`;
      root.dataset.total = N; root.dataset.selected = n;
      root.querySelector('[data-draw]').disabled = n === N;
      root.querySelector('.status').textContent = n === N ? 'Population size N = 1,000. All 1,000 students are included: this is a census, not a smaller sample.' : `Population size N = 1,000. Sample size n = ${n}. The sample is the ${n} selected students—not the number ${n} by itself.`;
    }
    root.querySelector('[data-size]').addEventListener('change', event => { n=Number(event.target.value);render(); });
    root.querySelector('[data-draw]').addEventListener('click', () => { seed++;render(); });
    root.querySelector('[data-reset]').addEventListener('click', () => { n=40;seed=8126;root.querySelector('select').value='40';render(); });
    render();
  }
  const cases = [
    {title:'Identify the population',question:'The study concerns all 1,000 School A students enrolled this term. Forty students are selected. Which description names the population?',choices:['The 40 selected students','All 1,000 students enrolled at School A this term','Only students who travel by bus','All teenagers in the city'],answer:1,explanation:'The population is the entire group named by the question. The 40 selected students form the sample. Bus users are one part of the target group, and the city-wide group is too broad.'},
    {title:'Identify the investigative question',question:'Which question states the purpose of the School A bus-use study rather than asking for one response?',choices:['Do you usually use the bus?','What time did you leave home today?','What proportion of all School A students enrolled this term usually travel mainly by bus?','Are journeys good?'],answer:2,explanation:'The proportion question identifies a population and a specific characteristic. Asking one student about bus use can collect relevant data, but it is a survey question. Good is undefined.'},
    {title:'Match the data to the purpose',question:'To study the mean one-way commute time for School A students this term, which information is most directly relevant?',choices:['Each selected student\'s commute duration in minutes, using the same start and end points','Each selected student\'s favourite subject','The number of students in a randomly chosen classroom, without commute times','Whether the investigator personally likes public transit'],answer:0,explanation:'Comparable commute durations are the information needed for a mean-time question. The other answers do not supply the measurements required to address that purpose.'}
  ];
  function questionCheck(root) {
    let index=0;
    root.innerHTML='<h3>Read the purpose carefully</h3><div class="controls"><button type="button" data-next>Next case</button><button type="button" data-clear>Clear answer</button></div><p class="small-note" data-progress></p><p data-question></p><div class="choice-list"></div><p class="status" role="status" aria-live="polite"></p>';
    function render() {
      const c=cases[index];root.dataset.case=index;root.dataset.answer='';
      root.querySelector('[data-progress]').textContent=`Case ${index+1} of ${cases.length} · ${c.title}`;
      root.querySelector('[data-question]').textContent=c.question;
      root.querySelector('.choice-list').innerHTML=c.choices.map((choice,i)=>`<button type="button" data-option="${i}" aria-pressed="false"><strong>${String.fromCharCode(65+i)}.</strong> ${escape(choice)}</button>`).join('');
      root.querySelector('.status').textContent='Choose one answer. No option is selected yet.';
      root.querySelectorAll('[data-option]').forEach(button=>button.addEventListener('click',()=>{
        const selected=Number(button.dataset.option);root.dataset.answer=selected;
        root.querySelectorAll('[data-option]').forEach(b=>{b.setAttribute('aria-pressed','false');b.classList.remove('correct','incorrect');});
        button.setAttribute('aria-pressed','true');button.classList.add(selected===c.answer?'correct':'incorrect');
        root.querySelector('.status').textContent=(selected===c.answer?'Correct. ':'Not quite. ')+c.explanation;
      }));
    }
    root.querySelector('[data-next]').addEventListener('click',()=>{index=(index+1)%cases.length;render();});
    root.querySelector('[data-clear]').addEventListener('click',render);render();
  }
  document.querySelectorAll('[data-foundation="population"]').forEach(population);
  document.querySelectorAll('[data-foundation="question-check"]').forEach(questionCheck);
  // Print static references without changing the current on-screen selections.
  let printNodes=[];
  function cleanup() {printNodes.forEach(node=>node.remove());printNodes=[];}
  window.addEventListener('beforeprint',()=>{
    cleanup();
    document.querySelectorAll('[data-foundation]').forEach(root=>{
      const out=document.createElement('div');out.className='foundation-print';
      if(root.dataset.foundation==='population') out.innerHTML='<h3>Population and sample</h3>'+root.querySelector('.foundation-grid').innerHTML+'<p>'+escape(root.querySelector('.status').textContent)+'</p>';
      else if(root.dataset.foundation==='question-check') out.innerHTML='<h3>Question workshop: answers</h3>'+cases.map(c=>`<p><strong>${escape(c.title)}.</strong> ${escape(c.question)}</p><p><strong>Answer ${String.fromCharCode(65+c.answer)}:</strong> ${escape(c.choices[c.answer])}. ${escape(c.explanation)}</p>`).join('');
      if(out.innerHTML){root.after(out);printNodes.push(out);}
    });
  });
  window.addEventListener('afterprint',cleanup);
  window.FOUNDATION_TEST=Object.freeze({sampleIndices,populationSize:N,answers:cases.map(c=>c.answer)});
})();
