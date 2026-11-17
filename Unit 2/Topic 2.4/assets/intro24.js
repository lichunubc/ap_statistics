/* Offline six-sided-die event and complement explorer; no tracking or storage. */
(()=>{"use strict";
const events={even:{name:"even",f:[2,4,6]},high:{name:"greater than 4",f:[5,6]},prime:{name:"prime",f:[2,3,5]},notone:{name:"not 1",f:[2,3,4,5,6]}};
function install(root){
 if(root.dataset.enhanced==="true")return;
 const buttons=[...root.querySelectorAll("[data-prob24-choice]")];
 const faces=[...root.querySelectorAll("[data-prob24-face]")];
 const status=root.querySelector("[data-prob24-status]");
 const count=root.querySelector("[data-prob24-count]");
 const p=root.querySelector("[data-prob24-p]");
 const pc=root.querySelector("[data-prob24-pc]");
 function display(key){
  const e=key?events[key]:null;
  buttons.forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.prob24Choice===key)));
  faces.forEach(f=>f.classList.toggle("favorable",!!e && e.f.includes(Number(f.dataset.prob24Face))));
  count.textContent=e?String(e.f.length):"—";
  p.textContent=e?e.f.length+"/6":"—";
  pc.textContent=e?(6-e.f.length)+"/6":"—";
  status.textContent=e?"Event "+e.name+": "+e.f.length+" favorable outcomes. Its complement has "+(6-e.f.length)+" outcomes.":"No event selected. Predict the probability, then choose an event.";
 }
 buttons.forEach(b=>b.addEventListener("click",()=>display(b.dataset.prob24Choice)));
 root.querySelector("[data-prob24-reset]").addEventListener("click",()=>display(null));
 root.dataset.enhanced="true";display(null);
}
function start(){document.querySelectorAll("[data-prob24]").forEach(install);}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});else start();
})();
