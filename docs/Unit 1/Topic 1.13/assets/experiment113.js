/* Topic 1.13: self-contained original random-assignment model; no tracking or external calls. */
(function () {
"use strict";
var host=document.querySelector("[data-experiment113]");
if(!host)return;
var method=host.querySelector("[data-e113-method]");
var status=host.querySelector("[data-e113-status]");
var results=host.querySelector("[data-e113-table]");
var interp=host.querySelector("[data-e113-interpret]");
var run=0;
var offsets=[0,1,-1,2,-2,0,1,-1,2,-2,0,0];
function rng(seed){var s=seed>>>0;return function(){s=(Math.imul(1664525,s)+1013904223)>>>0;return s/4294967296;};}
function shuffle(a,next){for(var i=a.length-1;i>0;i--){var j=Math.floor(next()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
function assign(mode,seed) {
  var next=rng(seed),panels=Array.from({length:24},function(_,id){
    var batch=id<12?1:2;
    return {id:id,batch:batch,base:(batch===1?38:70)+offsets[id%12],treatment:""};
  });
  if(mode==="block"){
    for(var b=1;b<=2;b++){
      var indices=shuffle(panels.filter(function(p){return p.batch===b;}).map(function(p){return p.id;}),next);
      indices.forEach(function(id,i){panels[id].treatment=i<6?"A":"B";});
    }
  } else {
    var ids=shuffle(panels.map(function(p){return p.id;}),next);
    ids.forEach(function(id,i){panels[id].treatment=i<12?"A":"B";});
  }
  panels.forEach(function(p){p.wear=p.base-(p.treatment==="B"?8:0);});
  return panels;
}
function stats(rows,which){var x=rows.filter(function(p){return p.treatment===which;});return x.reduce(function(s,p){return s+p.wear;},0)/x.length;}
function counts(rows,b,t){return rows.filter(function(p){return p.batch===b&&p.treatment===t;}).length;}
function reset(){
  run=0;method.value="crd";
  status.textContent="Before assignment: 12 panels in each batch. Predict how batch imbalance may affect a coating comparison.";
  results.innerHTML="<p>No assignment yet. Each panel will receive exactly one coating.</p>";
  interp.textContent="For each random allocation, compute the mean wear in the B group minus the mean wear in the A group. The simulated causal effect is -8 mg, but the observed difference can vary.";
}
function draw(){
  var mode=method.value;if(!["crd","block"].includes(mode))return;
  var rows=assign(mode,113+run*131),a=stats(rows,"A"),b=stats(rows,"B"),diff=b-a;run++;
  var table=document.createElement("table");
  var caption=document.createElement("caption");caption.textContent="Panels receiving each coating by manufacturing batch";table.appendChild(caption);
  var header=document.createElement("thead");var tr=document.createElement("tr");
  ["Panel batch","Coating A","Coating B","Total"].forEach(function(t){var th=document.createElement("th");th.scope="col";th.textContent=t;tr.appendChild(th);});header.appendChild(tr);table.appendChild(header);
  var body=document.createElement("tbody");[1,2].forEach(function(id){var r=document.createElement("tr");var vals=["Batch "+id,counts(rows,id,"A"),counts(rows,id,"B"),12];vals.forEach(function(v,i){var cell=document.createElement(i===0?"th":"td");if(i===0)cell.scope="row";cell.textContent=String(v);r.appendChild(cell);});body.appendChild(r);});table.appendChild(body);
  var total=document.createElement("tr");["Both batches",12,12,24].forEach(function(v,i){var cell=document.createElement(i===0?"th":"td");if(i===0)cell.scope="row";cell.textContent=String(v);total.appendChild(cell);});body.appendChild(total);results.replaceChildren(table);
  status.textContent="Assignment "+run+" complete. Each of the 24 panels received exactly one coating.";
  interp.textContent="Mean wear: A "+a.toFixed(2)+" mg; B "+b.toFixed(2)+" mg. Observed B minus A = "+diff.toFixed(2)+" mg. The simulated treatment effect is -8.00 mg. "+(mode==="block"?"Each batch contains both treatments, so the batch effect is balanced within this allocation.":"Group-level batch imbalance can move the observed difference away from -8 mg.")+" Repeat to compare random allocations.";
}
host.querySelector("[data-e113-run]").addEventListener("click",draw);
host.querySelector("[data-e113-reset]").addEventListener("click",reset);
method.addEventListener("change",function(){status.textContent="Method changed; click Randomly assign for a new allocation.";results.innerHTML="<p>No assignment yet for this method.</p>";});
reset();
})();