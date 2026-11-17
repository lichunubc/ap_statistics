/* Original standalone die-event explorer. All calculations local; no network, storage, or tracking. */
(()=>{'use strict';
const cases={
 evenmultiple:{name:'Even and multiple of 3',a:[2,4,6],b:[3,6]},
 evenodd:{name:'Even and odd',a:[2,4,6],b:[1,3,5]},
 evengreater:{name:'Even and at least 4',a:[2,4,6],b:[4,5,6]},
 lowhigh:{name:'1–2 and 5–6',a:[1,2],b:[5,6]}
};
function fraction(n,d=6){return n+'/'+d;}
function show(root,key){
 const x=key?cases[key]:null;
 const inter=x?x.a.filter(v=>x.b.includes(v)):[];
 const union=x?[...new Set([...x.a,...x.b])]:[];
 root.querySelectorAll('[data-event27-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.event27Choice===key)));
 root.querySelectorAll('[data-event27-face]').forEach(li=>{
  const v=+li.dataset.event27Face,inA=!!x&&x.a.includes(v),inB=!!x&&x.b.includes(v);
  const status=!x?'Choose events':inA&&inB?'Both':inA?'A only':inB?'B only':'Neither';
  li.classList.remove('event27-a','event27-b','event27-both','event27-neither');
  if(x)li.classList.add(inA&&inB?'event27-both':inA?'event27-a':inB?'event27-b':'event27-neither');
  li.querySelector('small').textContent=status;
 });
 const fields={intersection:x?'{'+inter.join(', ')+'}':'—',joint:x?fraction(inter.length):'—',product:x?(x.a.length+'×'+x.b.length+'/36'):'—',independent:x?(inter.length*6===x.a.length*x.b.length?'Yes':'No'):'—',union:x?fraction(union.length):'—'};
 for(const [field,value] of Object.entries(fields))root.querySelector('[data-event27-'+field+']').textContent=value;
 root.querySelector('[data-event27-status]').textContent=x?(x.name+': intersection '+fields.intersection+'; independence '+fields.independent.toLowerCase()+'; union '+fields.union+'.'):'No pair selected. Choose a pair to compare independence and overlap.';
}
function install(root){
 if(root.dataset.enhanced==='true')return;
 root.querySelectorAll('[data-event27-choice]').forEach(b=>b.addEventListener('click',()=>show(root,b.dataset.event27Choice)));
 root.querySelector('[data-event27-reset]').addEventListener('click',()=>show(root,null));
 root.dataset.enhanced='true';show(root,null);
}
function start(){document.querySelectorAll('[data-event27]').forEach(install);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();