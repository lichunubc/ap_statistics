/* Topic 1.9: accessible linked comparisons and standardized-score explorer. */
(function(){
"use strict";
const M=window.COMPARE19_MATH;
if(!M)return;
const NS="http://www.w3.org/2000/svg";
const fmt=(n,d=2)=>Number(n).toFixed(d);
const node=(tag,attrs={},content)=>{
 const el=document.createElementNS(NS,tag);
 Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,String(v)));
 if(content!==undefined)el.textContent=String(content);
 return el;
};
const palette=["#075c83","#b44f1e"],light=["#b6e2f3","#fbd8bc"];
const xcoord=v=>65+(v/45)*690;
function line(svg,x1,y1,x2,y2,color="#304b5e",w=1){
 svg.append(node("line",{x1,y1,x2,y2,stroke:color,"stroke-width":w}));
}
function text(svg,x,y,value,attrs={}){
 svg.append(node("text",{x,y,fill:"#203a50","font-size":14,...attrs},value));
}
function plotDot(svg,stat,y,idx){
 const stack=new Map();
 for(const value of stat.sorted){
  const n=stack.get(value)||0;stack.set(value,n+1);
  svg.append(node("circle",{cx:xcoord(value),cy:y-n*14,r:5.5,fill:palette[idx],stroke:"#173e51","stroke-width":1,"aria-label":fmt(value,0)+" minutes"}));
 }
}
function plotBox(svg,stat,y,idx){
 const start=stat.leftWhisker,end=stat.rightWhisker;
 line(svg,xcoord(start),y,xcoord(end),y,palette[idx],3);
 for(const v of [start,end])line(svg,xcoord(v),y-12,xcoord(v),y+12,palette[idx],3);
 svg.append(node("rect",{x:xcoord(stat.q1),y:y-22,width:Math.max(1,xcoord(stat.q3)-xcoord(stat.q1)),height:44,fill:light[idx],stroke:palette[idx],"stroke-width":2}));
 line(svg,xcoord(stat.median),y-22,xcoord(stat.median),y+22,"#192f3b",4);
 stat.outliers.forEach(v=>svg.append(node("circle",{cx:xcoord(v),cy:y,r:7,fill:"#fff",stroke:"#a32334","stroke-width":3})));
}
function plotHist(svg,stat,y,idx){
 const counts=M.frequencies(stat.sorted);
 const maxHeight=counts.length?Math.max(...counts):0;
 counts.forEach((count,i)=>{
   const x=xcoord(i*5)+2,w=xcoord(5)-xcoord(0)-4;
   if(count>0)svg.append(node("rect",{x,y:y-count*10,width:w,height:count*10,fill:light[idx],stroke:palette[idx],"stroke-width":2}));
 });
 text(svg,750,y-102,"count scale: 1 = 10px",{"text-anchor":"end","font-size":12});
}
document.querySelectorAll("[data-compare19]").forEach(root=>{
 const select=root.querySelector("[data-compare19-scenario]"),mode=root.querySelector("[data-compare19-mode]");
 const largest=root.querySelector("[data-compare19-largest]"),chart=root.querySelector("[data-compare19-chart]");
 const message=root.querySelector("[data-compare19-message]"),interpret=root.querySelector("[data-compare19-interpret]");
 let a=[...M.scenarios.original.a],b=[...M.scenarios.original.b];
 function render(){
  const x=M.summary(a),y=M.summary(b);
  for(const [key,v] of Object.entries({meanA:x.mean,meanB:y.mean,medianA:x.median,medianB:y.median,sdA:x.sd,sdB:y.sd,iqrA:x.iqr,iqrB:y.iqr,outliersB:y.outliers.length})){root.dataset[key]=fmt(v,3);}
  for(const [id,s] of [["a",x],["b",y]]){
   const row=root.querySelector('[data-compare19-row="'+id+'"]');
   [...row.querySelectorAll("td")].forEach((td,i)=>{td.textContent=[s.n,fmt(s.mean),fmt(s.median),fmt(s.iqr),fmt(s.sd),fmt(s.range),s.outliers.length][i];});
  }
  const graph=node("svg",{viewBox:"0 0 800 350",role:"img","aria-label":"Route A and Route B "+mode.value+" plots on a common journey-time axis. Numerical comparison follows in a table."});
  graph.append(node("title",{},"Two route distributions, common numerical scale"));
  const display=mode.value;
  text(graph,65,24,"Compare one-way journey times (minutes)",{"font-size":18,"font-weight":"bold"});
  for(const v of [0,5,10,15,20,25,30,35,40,45]){
   const px=xcoord(v);
   line(graph,px,46,px,306,"#d5e1e7",1);
   line(graph,px,305,px,312,"#3b5364",2);
   text(graph,px,332,v,{"text-anchor":"middle","font-size":12});
  }
  line(graph,65,306,755,306,"#354d5c",2);
  text(graph,410,348,"One-way journey time (minutes)",{"text-anchor":"middle","font-size":14});
  for(const [i,stat] of [[0,x],[1,y]]){
    const baseline=i===0?151:277;
    text(graph,12,baseline-47,"Route "+(i===0?"A":"B"),{"font-weight":"bold","font-size":15});
    if(display==="dot")plotDot(graph,stat,baseline,i);
    else if(display==="box")plotBox(graph,stat,baseline,i);
    else plotHist(graph,stat,baseline,i);
  }
  chart.replaceChildren(graph);
  const center=fmt(x.median-y.median),mid=fmt(x.iqr),other=fmt(y.iqr);
  interpret.textContent="Median A − median B: "+center+" minutes. IQR A: "+mid+" minutes; IQR B: "+other+" minutes. "+(y.outliers.length?"Route B has "+y.outliers.length+" value(s) outside its calculated 1.5-IQR fences. ":"Neither route B extreme exceeds its 1.5-IQR fences. ")+"Compare the graph's tails, gaps, and sample SDs before drawing conclusions.";
  root.dataset.mode=display;
 }
 function fromScenario(){
  const set=M.scenarios[select.value];a=[...set.a];b=[...set.b];largest.value=Math.max(...b);message.textContent="Showing "+select.options[select.selectedIndex].text+"; all observations are invented for this lesson.";render();
 }
 select.addEventListener("change",fromScenario);
 mode.addEventListener("change",()=>{render();message.textContent="Graph type switched; numerical observations and common axis are unchanged.";});
 root.querySelector('[data-compare19-action="apply"]').addEventListener("click",()=>{
  if(!largest.value.trim()){message.textContent="Enter a nonnegative journey time between 0 and 45 minutes.";return;}
  const v=Number(largest.value);
  if(!Number.isFinite(v)||v<0||v>45){message.textContent="Journey time must be between 0 and 45 minutes.";return;}
  const i=b.indexOf(Math.max(...b));b[i]=v;
  render();message.textContent="Replaced one previous largest Route B observation with "+v+" minutes. Inspect the updated statistics.";
 });
 root.querySelector('[data-compare19-action="reset"]').addEventListener("click",()=>{
  select.value="original";mode.value="dot";fromScenario();message.textContent="Original datasets, dotplots and summaries restored.";
 });
 fromScenario();
});
document.querySelectorAll("[data-z19]").forEach(root=>{
 const defaults={muA:70,sdA:8,xA:86,muB:80,sdB:10,xB:90};
 const get=k=>root.querySelector('[data-z19-key="'+k+'"]');
 const status=root.querySelector("[data-z19-status]"),figure=root.querySelector("[data-z19-figure]"),result=root.querySelector("[data-z19-result]");
 function calculate(){
   const vals={};for(const k of Object.keys(defaults)){
     const s=get(k).value.trim();
     if(!s||!Number.isFinite(Number(s))){status.textContent="All six entries must be finite numbers.";root.dataset.valid="false";return;}
     vals[k]=Number(s);
   }
   if(vals.sdA<=0||vals.sdB<=0){status.textContent="Each standard deviation must be greater than zero. A z-score is undefined when SD = 0.";root.dataset.valid="false";return;}
   const za=M.zScore(vals.xA,vals.muA,vals.sdA),zb=M.zScore(vals.xB,vals.muB,vals.sdB);
   root.dataset.valid="true";root.dataset.zA=fmt(za,4);root.dataset.zB=fmt(zb,4);
   status.textContent="Assessment A: z = "+fmt(za)+"; Assessment B: z = "+fmt(zb)+".";
   result.textContent=Math.abs(za-zb)<1e-9?"Both observations are equally far above/below their own means in SD units (signed z-scores match).":za>zb?"Assessment A has the greater standardized score (more SDs above its own mean, or fewer below).":"Assessment B has the greater standardized score (more SDs above its own mean, or fewer below).";
   const svg=node("svg",{viewBox:"0 0 800 245",role:"img","aria-label":"Two horizontal z-score number lines, labelled −4 to +4; coloured points identify each assessment's standardized position, with exact values in text."});
   svg.append(node("title",{},"Standardized position comparison; not a normal distribution curve"));
   text(svg,22,25,"Relative position in standard deviation units, not probability",{"font-size":17,"font-weight":"bold"});
   const xp=z=>70+((Math.max(-4,Math.min(4,z))+4)/8)*660;
   for(const [i,score] of [[0,za],[1,zb]]){
    const base=i===0?94:174;
    text(svg,17,base-23,"Assessment "+(i?"B":"A"),{"font-weight":"bold"});
    line(svg,70,base,730,base,"#344e5f",2);
    for(let z=-4;z<=4;z++){line(svg,xp(z),base-6,xp(z),base+6,"#344e5f");text(svg,xp(z),base+23,z,{"text-anchor":"middle","font-size":12});}
    const mark=xp(score);
    line(svg,mark,base-30,mark,base-2,palette[i],3);
    svg.append(node("circle",{cx:mark,cy:base,r:7,fill:palette[i],stroke:"#193547","stroke-width":1}));
    text(svg,Math.max(60,Math.min(730,mark)),base-34,"z = "+fmt(score),{"text-anchor":"middle","font-size":13,"font-weight":"bold"});
   }
   figure.replaceChildren(svg);
 }
 root.querySelector('[data-z19-action="calculate"]').addEventListener("click",calculate);
 root.querySelector('[data-z19-action="reset"]').addEventListener("click",()=>{for(const[k,v]of Object.entries(defaults))get(k).value=v;calculate();});
 calculate();
});
})();
