/* Maple Hill School: original cafe two-way table explorer. No network/storage. */
(()=>{'use strict';const counts={App:{Coffee:4,Tea:2,Smoothie:2},Counter:{Coffee:4,Tea:8,Smoothie:4}},total={App:8,Counter:16};
function setup(root){const plot=root.querySelector('[data-cafe21-bars]'),status=root.querySelector('[data-cafe21-status]');if(!plot||!status)return;
function draw(mode){const pct=mode==='percent';plot.textContent='';
for(const ch of ['App','Counter'])for(const d of ['Coffee','Tea','Smoothie']){const n=counts[ch][d],v=pct?100*n/total[ch]:n;
const row=document.createElement('div');row.className='cafe21-row';row.dataset.channel=ch;
const label=document.createElement('span');label.textContent=ch+' · '+d;
const track=document.createElement('div');track.className='cafe21-track';const fill=document.createElement('span');fill.className='cafe21-fill';fill.style.width=(pct?v:12.5*v)+'%';track.append(fill);
const value=document.createElement('strong');value.textContent=pct?v.toFixed(0)+'%':String(n);row.append(label,track,value);plot.append(row)}
status.textContent=pct?'Within App: Coffee 50%, Tea 25%, Smoothie 25%. Within Counter: Coffee 25%, Tea 50%, Smoothie 25%.':'Counts: App 8 orders, Counter 16 orders; common zero baseline.';
root.querySelectorAll('[data-view]').forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.view===mode)));
}root.querySelectorAll('[data-view]').forEach(btn=>btn.addEventListener('click',()=>draw(btn.dataset.view)));
root.dataset.enhanced='true';draw('counts')}
function init(){document.querySelectorAll('[data-cafe21]').forEach(setup)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init()})();
