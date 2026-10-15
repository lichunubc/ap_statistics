/* Public original practice; editorial metadata stays in the structured source. */
(function(){
'use strict';
const build=(tag,klass,text)=>{const e=document.createElement(tag);if(klass)e.className=klass;if(text!==undefined)e.textContent=text;return e;};
document.querySelectorAll('[data-original-practice]').forEach(async host=>{
 const topic=host.dataset.originalPractice,url=host.dataset.bankUrl;
 const template=host.querySelector('template[data-practice-rich]'),rich=template?.content;
 let items=[],at=0;
 function fieldContent(q,field,tag='div',klass=''){
  const node=build(tag,klass),compiled=rich?.querySelector(`[data-practice-id="${CSS.escape(q.id)}"] [data-field="${field}"]`);
  if(compiled){const source=tag==='span'&&compiled.children.length===1&&compiled.firstElementChild.tagName==='P'?compiled.firstElementChild:compiled;node.append(...[...source.childNodes].map(child=>child.cloneNode(true)));}
  else{const value=field.startsWith('option-')?q.options?.find(o=>o.label===field.slice(7))?.text:q[field];node.textContent=value||'';}
  return node;
 }
 const status=build('p','original-status','');status.setAttribute('role','status');status.setAttribute('aria-live','polite');
 const shell=build('div','original-shell');host.replaceChildren(shell,status);
 function change(index,action){const x=scrollX,y=scrollY;at=index;render();const b=shell.querySelector(`[data-action="${action}"]`);if(b&&!b.disabled)b.focus({preventScroll:true});window.scrollTo(x,y);}
 function render(){
  const q=items[at],heading=build('h3','original-question-title','Question '+(at+1)+' of '+items.length),question=fieldContent(q,'prompt','div','original-prompt');
  const answerArea=build('div','original-answer');let field;
  if(q.type==='mc'){
   const f=build('fieldset');f.append(build('legend','','Choose one answer'));
   for(const opt of q.options){const label=build('label','original-choice'),radio=build('input');radio.type='radio';radio.name='original-'+q.id;radio.value=opt.label;label.append(radio,document.createTextNode(' '+opt.label+'. '),fieldContent(q,'option-'+opt.label,'span'));f.append(label);}
   answerArea.append(f);field=f;
  }else{
   const label=build('label','original-response-label',q.type==='number'?'Your numerical answer':'Your written justification');
   if(q.type==='number'){field=build('input');field.type='number';field.step='any';field.autocomplete='off';field.setAttribute('aria-label','Numerical answer for question '+(at+1));}
   else{field=build('textarea');field.rows=4;field.placeholder='Explain your reasoning in context.';}
   label.append(field);answerArea.append(label);
  }
  const feedback=build('p','original-feedback','');feedback.setAttribute('role','status');feedback.setAttribute('aria-live','polite');
  const hint=fieldContent(q,'hint','div','original-hint'),solution=build('div','original-solution');hint.hidden=true;solution.hidden=true;hint.id='practice-hint-'+q.id;solution.id='practice-solution-'+q.id;
  solution.append(build('strong','',q.type==='written'?'Model answer and self-check':'Worked solution'),fieldContent(q,'solution'));if(q.rubric)solution.append(fieldContent(q,'rubric'));
  const controls=build('div','original-controls');
  function make(label,act,handler){const b=build('button','original-button',label);b.type='button';b.dataset.action=act;b.addEventListener('click',handler);controls.append(b);return b;}
  make('Previous','previous',()=>change(at-1,'previous')).disabled=at===0;
  make('Next question','next',()=>change(at+1,'next')).disabled=at===items.length-1;
  make('Check answer','check',()=>{
   if(q.type==='mc'){const v=field.querySelector('input:checked');feedback.textContent=!v?'Choose an answer before checking.':v.value===q.answer?'Correct. Explain why the alternatives are unsuitable.':'Not yet. Use the hint or review the worked example.';}
   else if(q.type==='number'){const v=field.value.trim(),n=Number(v);feedback.textContent=!v||!Number.isFinite(n)?'Enter a numerical answer before checking.':Math.abs(n-q.answer)<=q.tolerance?'Correct, within rounding tolerance.':'Not yet. Check the formula and units.';}
   else feedback.textContent=field.value.trim()?'Compare your reasoning with the model answer and self-check.':'Write a justification first, then compare it with the model answer.';
  });
  function disclosure(label,act,target){const b=make('Show '+label,act,()=>{target.hidden=!target.hidden;b.textContent=(target.hidden?'Show ':'Hide ')+label;b.setAttribute('aria-expanded',String(!target.hidden));});b.setAttribute('aria-controls',target.id);b.setAttribute('aria-expanded','false');}
  disclosure('hint','hint',hint);disclosure('solution','solution',solution);make('Reset question','reset',()=>change(at,'reset'));
  shell.replaceChildren(heading,question,answerArea,feedback,controls,hint,solution);status.textContent='Showing question '+(at+1)+' of '+items.length+'.';
 }
 function printAll(){
  if(!items.length)return;host.querySelector('.original-print-set')?.remove();const print=build('section','original-print-set');print.append(build('h3','','Practice: Topic '+topic));
  items.forEach((q,i)=>{const article=build('article','original-print-question');article.append(build('h4','','Question '+(i+1)),fieldContent(q,'prompt'));for(const o of q.options||[])article.append(build('strong','',o.label+'.'),fieldContent(q,'option-'+o.label));article.append(build('strong','','Solution'),fieldContent(q,'solution'));if(q.rubric)article.append(fieldContent(q,'rubric'));print.append(article);});host.append(print);
 }
 window.addEventListener('beforeprint',printAll);window.addEventListener('afterprint',()=>host.querySelector('.original-print-set')?.remove());
 try{
  const response=await fetch(url,{cache:'no-cache'});if(!response.ok)throw Error('Unable to load the questions.');const pack=await response.json();
  if(pack.schema_version!==1||pack.topic!==topic||!Array.isArray(pack.items)||!pack.items.length)throw Error('The question file is not valid for this topic.');
  if(template&&Number(template.dataset.bankRevision)!==Number(pack.revision||1))throw Error('The questions have been updated. Please reload this page.');
  const ids=new Set();for(const q of pack.items){
   if(!q.id||ids.has(q.id)||typeof q.prompt!=='string'||!['mc','number','written'].includes(q.type)||typeof q.solution!=='string')throw Error('Invalid practice question.');
   if(q.type==='mc'&&(!Array.isArray(q.options)||q.options.length<2||!q.options.some(o=>o.label===q.answer)))throw Error('Invalid answer choices.');
   if(q.type==='number'&&(!Number.isFinite(q.answer)||!Number.isFinite(q.tolerance)||q.tolerance<0))throw Error('Invalid numerical answer.');ids.add(q.id);
  }
  items=pack.items;render();
 }catch(error){status.textContent='Practice unavailable: '+error.message;host.dataset.loadError='true';}
});
})();
