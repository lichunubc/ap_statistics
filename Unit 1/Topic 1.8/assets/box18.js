/* Topic 1.8: accessible, deterministic, browser-local stepwise boxplot. */
(function () {
"use strict";
const scenarios={
  typical:[5,8,10,12,12,14,15,16,18],
  extreme:[5,8,10,12,12,14,15,16,50],
  left:[1,32,33,34,35,36,37,38,39],
  bimodal:[5,6,6,7,7,7,20,20,21,21,22,22]
};
const NS="http://www.w3.org/2000/svg",fmt=x=>Number(x.toFixed(2)).toString();
document.querySelectorAll("[data-box18]").forEach(root=>{
 const scenario=root.querySelector("[data-box18-scenario]");
 const style=root.querySelector("[data-box18-style]");
 const input=root.querySelector("[data-box18-values]");
 const status=root.querySelector("[data-box18-step]");
 const description=root.querySelector("[data-box18-explanation]");
 const chart=root.querySelector("[data-box18-chart]");
 const row=root.querySelector("[data-box18-row]");
 let values=[...scenarios.typical],step=0;
 function make(tag,attributes={},text) {
   const el=document.createElementNS(NS,tag);
   Object.entries(attributes).forEach(([key,value])=>el.setAttribute(key,String(value)));
   if(text!==undefined)el.textContent=String(text);
   return el;
 }
 function render() {
   const s=computeBoxplot(values),a=s.sorted,mean=a.reduce((u,v)=>u+v,0)/a.length;
   const modified=style.value==="modified";
   const wLeft=modified?s.good[0]:a[0], wRight=modified?s.good.at(-1):a.at(-1);
   Object.entries({min:a[0],q1:s.q1,q3:s.q3,median:s.m,mean,iqr:s.delta,whiskerRight:wRight,flagged:s.sorted.filter(x=>x<s.low||x>s.high).length,step}).forEach(([k,v])=>root.dataset[k]=fmt(v));
   const vals=[a[0],s.q1,s.m,s.q3,a.at(-1),mean,s.delta,fmt(s.low)+", "+fmt(s.high),fmt(wLeft)+", "+fmt(wRight)];
   const names=["Minimum","First quartile","Median","Third quartile","Maximum","Mean","IQR","Outlier fences","Whisker endpoints"];
   [...row.children].forEach((td,i)=>{td.textContent=fmtOrText(vals[i]);td.setAttribute("aria-label",names[i]+": "+td.textContent+" minutes");});
   const svg=make("svg",{viewBox:"0 0 740 250",role:"img","aria-label":"Data dotplot above a progressively constructed boxplot. "+a.length+" observed times, median "+fmt(s.m)+" minutes."});
   svg.append(make("title",{},"Boxplot lab: original observations and five-number-summary construction"));
   const scale=x=>35+x*11;
   for(let v=0;v<=60;v+=10){
     const x=scale(v);
     svg.append(make("line",{x1:x,x2:x,y1:209,y2:216,stroke:"#3b5066"}));
     svg.append(make("text",{x,y:232,"text-anchor":"middle",fill:"#29465c","font-size":13},v));
   }
   svg.append(make("line",{x1:scale(0),x2:scale(60),y1:209,y2:209,stroke:"#3b5066","stroke-width":2}));
   svg.append(make("text",{x:365,y:249,"text-anchor":"middle",fill:"#29465c","font-size":13},"One-way journey time (minutes)"));
   svg.append(make("text",{x:35,y:22,fill:"#29465c","font-size":14},"Observed journeys · every dot is one measurement"));
   const stack=new Map();
   a.forEach(v=>{
     const height=stack.get(v)||0;stack.set(v,height+1);
     svg.append(make("circle",{cx:scale(v),cy:96-height*15,r:5,fill:"#267db5",stroke:"#0c3d66","stroke-width":1}));
   });
   if(step>=1){
     for(const [label,value,y] of [["min",a[0],119],["max",a.at(-1),119]]){
       svg.append(make("text",{x:scale(value),y,"text-anchor":"middle","font-size":12,fill:"#3b5066"},label));
     }
   }
   if(step>=2){
     svg.append(make("rect",{x:scale(s.q1),y:145,width:scale(s.q3)-scale(s.q1),height:39,fill:"#bce2e6",stroke:"#116a79","stroke-width":2}));
     for(const [label,v] of [["Q1",s.q1],["Q3",s.q3]]){
       svg.append(make("text",{x:scale(v),y:140,"text-anchor":"middle","font-size":12,fill:"#145f69"},label));
     }
   }
   if(step>=3){
     svg.append(make("line",{x1:scale(s.m),x2:scale(s.m),y1:143,y2:186,stroke:"#d04d21","stroke-width":4}));
     svg.append(make("text",{x:scale(s.m),y:200,"text-anchor":"middle","font-size":12,fill:"#a33618"},"median"));
   }
   if(step>=4){
     for(const [x1,x2] of [[wLeft,s.q1],[s.q3,wRight]]){
       svg.append(make("line",{x1:scale(x1),x2:scale(x2),y1:164,y2:164,stroke:"#145f69","stroke-width":3}));
       svg.append(make("line",{x1:scale(x1),x2:scale(x1),y1:155,y2:173,stroke:"#145f69","stroke-width":3}));
     }
     if(modified)for(const v of s.sorted.filter(x=>x<s.low||x>s.high)){
       svg.append(make("circle",{cx:scale(v),cy:164,r:6,fill:"#d04d21",stroke:"#84270d","stroke-width":2}));
     }
   }
   chart.replaceChildren(svg);
   const texts=[
     "Study the individual values. Each blue dot represents a journey; repeated times are stacked.",
     "Locate the actual minimum and maximum. These remain in the five-number summary even when there is an outlier.",
     "Draw the middle-half box from Q1 = "+fmt(s.q1)+" to Q3 = "+fmt(s.q3)+" minutes. Its width is the IQR = "+fmt(s.delta)+".",
     "Mark the median at "+fmt(s.m)+" minutes, not at the sample mean of "+fmt(mean)+" minutes.",
     "Whiskers end at "+fmt(wLeft)+" and "+fmt(wRight)+" minutes. "+(modified?"The "+(s.flagged?.length||0)+" flagged observations are marked separately.":"Unmodified whiskers extend to the observed extremes.")
   ];
   const flagCount=s.sorted.filter(v=>v<s.low||v>s.high).length;
   status.textContent="Step "+(step+1)+" of 5 · "+(modified?"Modified":"Unmodified")+" boxplot";
   description.textContent=texts[step].replace("The "+(s.flagged?.length||0)+" flagged","The "+flagCount+" flagged");
   root.querySelector('[data-box18-action="previous"]').disabled=step===0;
   root.querySelector('[data-box18-action="next"]').disabled=step===4;
 }
 function fmtOrText(v){return typeof v==="number"?fmt(v):v;}
 function reset(which="typical"){
   values=[...scenarios[which]];input.value=values.join(", ");step=0;render();
 }
 scenario.addEventListener("change",()=>reset(scenario.value));
 style.addEventListener("change",render);
 root.querySelector('[data-box18-action="next"]').addEventListener("click",()=>{step=Math.min(4,step+1);render();});
 root.querySelector('[data-box18-action="previous"]').addEventListener("click",()=>{step=Math.max(0,step-1);render();});
 root.querySelector('[data-box18-action="reset"]').addEventListener("click",()=>{
   scenario.value="typical";style.value="modified";reset();
 });
 root.querySelector('[data-box18-action="apply"]').addEventListener("click",()=>{
   const parts=input.value.split(",").map(v=>v.trim());
   const numbers=parts.map(Number);
   if(parts.length<3||parts.length>40||parts.some(v=>v==="")||numbers.some(v=>!Number.isFinite(v)||v<0||v>60)){
     status.textContent="Invalid entry. Supply 3–40 numerical measurements between 0 and 60 minutes.";return;
   }
   values=numbers;step=0;render();
 });
 render();
});
}());
