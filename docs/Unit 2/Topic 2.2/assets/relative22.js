/* AP Statistics Topic 2.2: original local-only reference-group explorer. */
(()=>{
"use strict";
const cases={
 joint:[2,24,"8.3%","app-tea","all","Joint App and Tea"],
 "tea-app":[2,8,"25%","app-tea","app","Tea among App"],
 "app-tea":[2,10,"20%","app-tea","tea","App among Tea"],
 marginal:[10,24,"41.7%","tea","all","Marginal Tea"],
 "tea-counter":[8,16,"50%","counter-tea","counter","Tea among Counter"],
 "counter-coffee":[4,8,"50%","counter-coffee","coffee","Counter among Coffee"]
};
function start(root){
 const select=root.querySelector("[data-rel22-choice]");
 const display=root.querySelector("[data-rel22-result]");
 const cells=Array.from(root.querySelectorAll("[data-rel22-cell]"));
 function render(){
  const item=cases[select.value]||cases.joint;
  cells.forEach(c=>c.classList.toggle("rel22-mark",c.dataset.rel22Cell===item[3]||c.dataset.rel22Cell===item[4]));
  display.textContent=item[5]+": "+item[0]+" / "+item[1]+" = "+item[2]+". The denominator is the reference-group total.";
 }
 select.addEventListener("change",render);
 root.querySelector("[data-rel22-reset]").addEventListener("click",()=>{select.value="joint";render();});
 render();root.dataset.enhanced="true";
}
function ready(){document.querySelectorAll("[data-rel22]").forEach(start);}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",ready,{once:true});else ready();
})();