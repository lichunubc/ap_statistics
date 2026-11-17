/* Topic 2.3: accessible, offline three-fair-toss simulation. No user data or networking. */
(()=>{"use strict";
const NS="http://www.w3.org/2000/svg";
const node=(tag,attrs={})=>{const n=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,String(v)));return n;};
function install(root){
  if(root.dataset.enhanced==="true")return;
  let trials=0,hits=0,last="",history=[];
  const status=root.querySelector("[data-sim23-status]");
  const total=root.querySelector("[data-sim23-total]");
  const good=root.querySelector("[data-sim23-hits]");
  const share=root.querySelector("[data-sim23-share]");
  const plot=root.querySelector("[data-sim23-plot]");
  const lastLabel=root.querySelector("[data-sim23-last]");
  function render(){
    total.textContent=String(trials);good.textContent=String(hits);
    share.textContent=trials?(hits/trials).toFixed(3):"—";
    lastLabel.textContent=trials?"Last complete trial: "+last+".":"Last complete trial: none yet.";
    if(!trials){
      status.textContent="No trials yet. Press a Run button to start.";
      plot.replaceChildren(Object.assign(document.createElement("p"),{textContent:"Run the simulation to display the relative-frequency graph."}));
      plot.setAttribute("aria-label","No simulated trials yet.");
      return;
    }
    status.textContent=hits+" of "+trials+" complete three-toss trials had at least two heads (estimated probability "+(hits/trials).toFixed(3)+").";
    const w=600,h=244,m={left:46,right:16,top:14,bottom:37},pw=w-m.left-m.right,ph=h-m.top-m.bottom;
    const svg=node("svg",{viewBox:"0 0 600 244","aria-hidden":"true",focusable:"false"});
    const y=v=>m.top+(1-v)*ph;const x=i=>m.left+(i/trials)*pw;
    [0,.25,.5,.75,1].forEach(v=>{
      svg.appendChild(node("line",{x1:m.left,y1:y(v),x2:w-m.right,y2:y(v),stroke:v===.5?"#0e8589":"#e2e8eb","stroke-width":v===.5?2:1,"stroke-dasharray":v===.5?"5 4":""}));
      const t=node("text",{x:m.left-8,y:y(v)+4,"text-anchor":"end",fill:"#334c56","font-size":12});t.textContent=v.toFixed(2);svg.appendChild(t);
    });
    const axis=node("line",{x1:m.left,y1:y(0),x2:w-m.right,y2:y(0),stroke:"#647781"});svg.appendChild(axis);
    const nMax=Math.min(history.length,300);const stride=Math.max(1,Math.ceil(history.length/nMax));
    const take=history.filter((_,i)=>i===0 || i===history.length-1 || i%stride===0);
    svg.appendChild(node("polyline",{points:take.map(p=>x(p[0])+","+y(p[1])).join(" "),fill:"none",stroke:"#9a621e","stroke-width":2.6,"stroke-linejoin":"round"}));
    for(const i of [0,trials]){const t=node("text",{x:x(i),y:h-14,"text-anchor":i?"end":"start",fill:"#334c56","font-size":12});t.textContent=String(i);svg.appendChild(t);}
    const xt=node("text",{x:w/2,y:h-2,"text-anchor":"middle",fill:"#334c56","font-size":11});xt.textContent="Completed three-toss trials";svg.appendChild(xt);
    const title=node("title");title.textContent="Cumulative success proportion (amber) and model probability one half (teal).";svg.prepend(title);
    plot.replaceChildren(svg);
    plot.setAttribute("aria-label","After "+trials+" completed three-toss trials, "+hits+" successes give a running proportion of "+(hits/trials).toFixed(3)+". Dashed reference is 0.5.");
  }
  function run(n){
    for(let i=0;i<n;i++){
      let heads=0;last="";
      for(let toss=0;toss<3;toss++){const c=Math.random()<.5?"H":"T";last+=c;if(c==="H")heads++;}
      trials++;if(heads>=2)hits++;
      history.push([trials,hits/trials]);
    }
    render();
  }
  root.querySelectorAll("[data-sim23-n]").forEach(b=>b.addEventListener("click",()=>run(Number(b.dataset.sim23N))));
  root.querySelector("[data-sim23-reset]").addEventListener("click",()=>{trials=0;hits=0;last="";history=[];render();});
  root.dataset.enhanced="true";render();
}
function start(){document.querySelectorAll("[data-sim23]").forEach(install);}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});else start();
})();
