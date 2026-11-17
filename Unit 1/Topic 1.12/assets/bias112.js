/* Original, deterministic comparison of complete-frame SRS and convenience sampling. */
(function(){
"use strict";
var host=document.querySelector("[data-bias112]");if(!host)return;
var nEl=host.querySelector("[data-b112-n]"),mEl=host.querySelector("[data-b112-method]");
var status=host.querySelector("[data-b112-status]"),lab=host.querySelector("[data-b112-label]");
var bar=host.querySelector("[data-b112-bar]"),detail=host.querySelector("[data-b112-detail]");
var run=0;
function generator(seed){var s=seed>>>0;return function(){s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}
function sample(n,method,seed){
if(method==="gate")return {w:n,b:0,mean:10};
var a=Array.from({length:100},function(_,i){return i<40?10:30;});
var rand=generator(seed);
for(var i=99;i>0;i--){var j=Math.floor(rand()*(i+1)),t=a[i];a[i]=a[j];a[j]=t;}
var selected=a.slice(0,n),w=selected.filter(function(x){return x===10;}).length;
return {w:w,b:n-w,mean:selected.reduce(function(s,v){return s+v;},0)/n};
}
function clear(){
status.textContent="No sample drawn. Predict whether each method can include a bus rider.";
lab.textContent="Sample mean: not drawn";bar.style.width="0%";
detail.textContent="Population consists of 40 walkers at 10 minutes and 60 bus riders at 30 minutes.";
}
function draw(){
var n=Number(nEl.value),method=mEl.value;
if(![10,20,30,40].includes(n)||!["srs","gate"].includes(method))return;
var x=sample(n,method,112+101*run++);lab.textContent="Sample mean: "+x.mean.toFixed(1)+" minutes";
bar.style.width=(x.mean/40*100).toFixed(1)+"%";
detail.textContent=n+" selected: "+x.w+" walkers, "+x.b+" bus riders. Difference from the population mean: "+(x.mean-22).toFixed(1)+" minutes.";
status.textContent=method==="gate"?"Convenience method: bus riders were excluded. Increasing sample size does not change this exclusion.":"Simple random sample: every group of "+n+" distinct roster members had the same chance.";
}
host.querySelector("[data-b112-draw]").addEventListener("click",draw);
host.querySelector("[data-b112-reset]").addEventListener("click",function(){run=0;nEl.value="20";mEl.value="srs";clear();});
nEl.addEventListener("change",clear);mEl.addEventListener("change",clear);clear();
})();
