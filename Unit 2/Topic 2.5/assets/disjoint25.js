/* Original offline die-event intersection explorer. No storage, analytics or remote calls. */
(()=>{'use strict';
const pairs={
 evenodd:{a:[2,4,6],b:[1,3,5],name:'Even and odd'},
 evenhigh:{a:[2,4,6],b:[4,5,6],name:'Even and at least 4'},
 lowhigh:{a:[1,2],b:[5,6],name:'At most 2 and at least 5'},
 loweven:{a:[1,2],b:[2,4,6],name:'At most 2 and even'}
};
function install(root){
 if(root.dataset.enhanced==='true')return;
 const buttons=[...root.querySelectorAll('[data-disjoint25-choice]')];
 const faces=[...root.querySelectorAll('[data-disjoint25-face]')];
 const status=root.querySelector('[data-disjoint25-status]');
 const set=root.querySelector('[data-disjoint25-set]');
 const prob=root.querySelector('[data-disjoint25-p]');
 const answer=root.querySelector('[data-disjoint25-answer]');
 function draw(key){
  const p=key?pairs[key]:null, both=p?p.a.filter(v=>p.b.includes(v)):[];
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.disjoint25Choice===key)));
  faces.forEach(f=>{
   const v=Number(f.dataset.disjoint25Face);
   const role=!p?'none':p.a.includes(v)&&(p.b.includes(v))?'both':p.a.includes(v)?'a':p.b.includes(v)?'b':'neither';
   f.dataset.member=role;
   f.setAttribute('aria-label','Face '+v+(p?'; '+({a:'A only',b:'B only',both:'both A and B',neither:'neither'}[role]):'; no pair selected'));
  });
  set.textContent=p?(both.length?'{'+both.join(', ')+'}':'∅'):'—';
  prob.textContent=p?both.length+'/6':'—';
  answer.textContent=p?(both.length===0?'Yes':'No'):'—';
  status.textContent=p?(p.name+': '+both.length+' shared faces. The events '+(both.length===0?'are mutually exclusive.':'are not mutually exclusive.')):'No pair selected. Choose a pair to classify the overlap.';
 }
 buttons.forEach(b=>b.addEventListener('click',()=>draw(b.dataset.disjoint25Choice)));
 root.querySelector('[data-disjoint25-reset]').addEventListener('click',()=>draw(null));
 root.dataset.enhanced='true';draw(null);
}
function init(){document.querySelectorAll('[data-disjoint25]').forEach(install);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();