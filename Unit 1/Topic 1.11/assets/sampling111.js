/* Accessible deterministic random-sampling explorer, no persistent state. */
(async function(){
'use strict';
const host=document.querySelector('[data-sampling111]');if(!host)return;
const script=document.currentScript;
const url=new URL('../data/population.json',script.src);
const select=host.querySelector('[data-s111-method]');
const seedInput=host.querySelector('[data-s111-seed]');
const grid=host.querySelector('[data-s111-grid]');
const status=host.querySelector('[data-s111-status]');
const summary=host.querySelector('[data-s111-summary]');
const explanation=host.querySelector('[data-s111-explanation]');
const step=host.querySelector('[data-s111-step]');
const all=host.querySelector('[data-s111-all]');
const reset=host.querySelector('[data-s111-reset]');
const descriptions={
 srs:'Every unordered group of six different people has the same chance; actual grade counts vary.',
 stratified:'Two distinct people are sampled independently from each grade. Every grade contributes.',
 cluster:'One advisory group is selected at random. All six members of that advisory are included.',
 systematic:'A start is chosen uniformly from positions 1–6 and every sixth roster position is included. This roster repeats grade patterns.',
 replacement:'Six independent draws from all 36 IDs. Duplicate draws count twice and may represent fewer than six distinct people.'
};
function randomSource(seed){let state=seed>>>0;return()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;};}
function integer(rng,n){return Math.floor(rng()*n);}
function shuffleCopy(arr,rng){const a=arr.slice();for(let i=0;i<a.length-1;i++){const j=i+integer(rng,a.length-i);[a[i],a[j]]=[a[j],a[i]];}return a;}
function choose(pop,method,seed){const rng=randomSource(seed);if(method==='replacement')return Array.from({length:6},()=>pop[integer(rng,pop.length)]);
 if(method==='srs')return shuffleCopy(pop,rng).slice(0,6);
 if(method==='stratified')return ['A','B','C'].flatMap(g=>shuffleCopy(pop.filter(x=>x.grade===g),rng).slice(0,2));
 if(method==='cluster'){const c=1+integer(rng,6);return pop.filter(x=>x.advisory===c);}
 if(method==='systematic'){const r=1+integer(rng,6);return pop.filter(x=>(x.id-r)%6===0&&x.id>=r);}
 throw Error('Unknown sampling method');
}
function makeCell(x){const e=document.createElement('div');e.className='sampling111-unit';e.dataset.id=x.id;e.dataset.picked='false';e.setAttribute('role','listitem');e.setAttribute('aria-label',`Student ${x.id}, advisory ${x.advisory}, grade ${x.grade}, commute ${x.commute_minutes} minutes`);e.innerHTML=`<strong>${String(x.id).padStart(2,'0')}</strong>Grade ${x.grade}<br>${x.commute_minutes} min<span class="sampling111-multiplicity" hidden></span>`;return e;}
let pop=[],planned=[],visible=0,ready=false;
function paint(){const shown=planned.slice(0,visible),ids=shown.map(x=>x.id),counts=Object.create(null);ids.forEach(x=>{counts[x]=(counts[x]||0)+1;});
 grid.querySelectorAll('.sampling111-unit').forEach(e=>{const n=counts[Number(e.dataset.id)]||0;e.dataset.picked=n>0?'true':'false';const multiple=e.querySelector('.sampling111-multiplicity');multiple.hidden=n<2;multiple.textContent=n>=2?`×${n} draws`:'';e.setAttribute('aria-label',e.getAttribute('aria-label').replace(/; selected \d+ time\(s\)$/,'')+(n?`; selected ${n} time(s)`:''));});
 const unique=new Set(ids);const grade=['A','B','C'].map(g=>`${g}: ${shown.filter(x=>x.grade===g).length}`).join(', ');
 const mean=visible?shown.reduce((s,x)=>s+x.commute_minutes,0)/visible:null;
 const meanLabel=visible===planned.length?'Sample mean':'Mean of selections revealed so far';
 summary.textContent=visible?`Selected roster IDs: ${ids.map(i=>String(i).padStart(2,'0')).join(', ')}. ${visible} draws, ${unique.size} distinct students; grade counts ${grade}; ${meanLabel}: ${mean.toFixed(2)} minutes (population 17).`:'All 36 students are available.';
 status.textContent=visible===0?'Ready. Choose a method, predict the result, and reveal the selections.':`Showing ${visible} of ${planned.length} selections. ${visible===planned.length?'Complete sample.':'Reveal the next selection when ready.'}`;
 explanation.textContent=descriptions[select.value];step.disabled=visible>=planned.length;all.disabled=visible>=planned.length;
}
function plan(){if(!ready)return;const s=Number(seedInput.value);if(!Number.isInteger(s)||s<1||s>999999){planned=[];visible=0;paint();status.textContent='Choose an integer seed between 1 and 999999.';step.disabled=all.disabled=true;return;}
 planned=choose(pop,select.value,s);visible=0;paint();}
try{const r=await fetch(url,{cache:'no-cache'});if(!r.ok)throw Error('Population data unavailable');const j=await r.json();pop=j.students;
 if(pop.length!==36||new Set(pop.map(x=>x.id)).size!==36||pop.reduce((a,x)=>a+x.commute_minutes,0)!==612)throw Error('Population data mismatch');
 pop.forEach((x,i)=>{if(i%6===0){const h=document.createElement('div');h.className='sampling111-group';h.textContent='Advisory '+(x.advisory);grid.append(h);}grid.append(makeCell(x));});ready=true;plan();
 step.addEventListener('click',()=>{if(visible<planned.length){visible++;paint();}});
 all.addEventListener('click',()=>{visible=planned.length;paint();});
 reset.addEventListener('click',()=>{select.value='srs';seedInput.value='1729';plan();});
 select.addEventListener('change',plan);seedInput.addEventListener('input',plan);seedInput.addEventListener('change',plan);
}catch(e){status.textContent='Sampling explorer unavailable: '+e.message;step.disabled=all.disabled=true;}
})();
