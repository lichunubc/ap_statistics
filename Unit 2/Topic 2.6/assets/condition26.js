/* Original offline conditional probability denominator explorer. No storage/network. */
(()=>{'use strict';
const examples={
 teaapp:{name:'Tea given App',group:'App (8 orders)',num:2,den:8,cell:'app-tea',condition:'app'},
 apptea:{name:'App given Tea',group:'Tea (10 orders)',num:2,den:10,cell:'app-tea',condition:'tea'},
 teacounter:{name:'Tea given Counter',group:'Counter (16 orders)',num:8,den:16,cell:'counter-tea',condition:'counter'},
 countertea:{name:'Counter given Tea',group:'Tea (10 orders)',num:8,den:10,cell:'counter-tea',condition:'tea'}
};
function install(root){
 if(root.dataset.enhanced==='true')return;
 const buttons=[...root.querySelectorAll('[data-condition26-choice]')];
 const cells=[...root.querySelectorAll('[data-condition26-cell]')];
 const totals=[...root.querySelectorAll('[data-condition26-total]')];
 const status=root.querySelector('[data-condition26-status]');
 const group=root.querySelector('[data-condition26-group]');
 const count=root.querySelector('[data-condition26-count]');
 const answer=root.querySelector('[data-condition26-answer]');
 function show(key){
  const item=key?examples[key]:null;
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.condition26Choice===key)));
  cells.forEach(c=>{
   const tag=c.dataset.condition26Cell;
   const included=!!item&&(item.condition==='app'?tag.startsWith('app-'):item.condition==='counter'?tag.startsWith('counter-'):tag.endsWith('-tea'));
   c.classList.toggle('condition26-selected',included);
   c.classList.toggle('condition26-intersection',!!item&&tag===item.cell);
  });
  totals.forEach(t=>t.classList.toggle('condition26-denominator',!!item&&t.dataset.condition26Total===item.condition));
  group.textContent=item?item.group:'—';
  count.textContent=item?String(item.num):'—';
  answer.textContent=item?item.num+'/'+item.den:'—';
  status.textContent=item?(item.name+': '+item.num+' of '+item.den+' orders satisfy the target event.'):('No question selected. Choose a condition to update the denominator.');
 }
 buttons.forEach(b=>b.addEventListener('click',()=>show(b.dataset.condition26Choice)));
 root.querySelector('[data-condition26-reset]').addEventListener('click',()=>show(null));
 root.dataset.enhanced='true';show(null);
}
function start(){document.querySelectorAll('[data-condition26]').forEach(install);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();