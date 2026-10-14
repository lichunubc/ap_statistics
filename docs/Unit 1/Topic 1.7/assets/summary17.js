/* Quantitative summary explorer: hypothetical teaching data, entirely browser-local. */
(function () {
  "use strict";
  function med(a) { const b=[...a].sort((x,y)=>x-y),k=b.length;return k%2?b[(k-1)/2]:(b[k/2-1]+b[k/2])/2; }
  function stats(a) {
    const b=[...a].sort((x,y)=>x-y),n=b.length,m=a.reduce((p,q)=>p+q,0)/n,k=Math.floor(n/2);
    const q1=med(b.slice(0,k)),q3=med(b.slice(n%2?k+1:k)),iqr=q3-q1;
    const variance=a.reduce((p,q)=>p+(q-m)**2,0)/(n-1),sd=Math.sqrt(variance);
    const fences=[q1-1.5*iqr,q3+1.5*iqr],sigma=[m-2*sd,m+2*sd];
    return {b,n,mean:m,median:med(b),q1,q3,iqr,variance,sd,range:b[n-1]-b[0],fences,sigma,
      iqrFlags:b.filter(x=>x<fences[0]||x>fences[1]),sdFlags:b.filter(x=>x<sigma[0]||x>sigma[1])};
  }
  window.SUMMARY17_TEST={stats:stats,median:med};
  const host=document.querySelector("[data-summary17]");if(!host)return;
  const source=host.querySelector("[data-summary17-values]"),
        chart=host.querySelector("[data-summary17-plot]"),
        results=host.querySelector("[data-summary17-results]"),
        info=host.querySelector("[data-summary17-feedback]"),
        caption=host.querySelector("[data-summary17-caption]");
  const init=[5,8,10,12,12,14,15,16,18];let values=[...init],unit="minutes";
  const fmt=v=>Number(v.toFixed(2)).toString();
  function read() {
    const parts=source.value.trim().split(/[,\s;]+/).filter(Boolean),data=parts.map(Number);
    if(data.length<3||data.length>30||data.some(x=>!Number.isFinite(x)||x<0||x>10000))throw Error("Enter 3–30 valid nonnegative numbers.");
    return data;
  }
  function show(a,message) {
    const st=stats(a);values=[...a];source.value=a.join(", ");info.textContent=message;
    const W=720,H=255,left=46,right=24,baseline=210,max=Math.max(1,...a)*1.08;
    const x=v=>left+v*(W-left-right)/max,NS="http://www.w3.org/2000/svg";
    const el=(name,attrs={},title)=>{
      const e=document.createElementNS(NS,name);
      for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));
      if(title){const t=document.createElementNS(NS,"title");t.textContent=title;e.append(t);}
      return e;
    };
    const svg=el("svg",{viewBox:"0 0 720 255",role:"img","aria-label":"Dotplot of "+st.n+" travel times in "+unit+" with mean, median and quartile lines"});
    svg.append(el("line",{x1:left,y1:baseline,x2:W-right,y2:baseline,class:"summary17-axis"}));
    for(let j=0;j<6;j++){
      const v=max*j/5,p=x(v);
      svg.append(el("line",{x1:p,x2:p,y1:baseline,y2:baseline+5,class:"summary17-tick"}));
      const t=el("text",{x:p,y:baseline+22,"text-anchor":"middle",class:"summary17-axis-label"});t.textContent=fmt(v);svg.append(t);
    }
    for(const [name,v,klass] of [["Q1",st.q1,"summary17-q"],["Q3",st.q3,"summary17-q"],["Median",st.median,"summary17-median"],["Mean",st.mean,"summary17-mean"]])
      svg.append(el("line",{x1:x(v),x2:x(v),y1:28,y2:baseline,class:"summary17-marker "+klass,"stroke-dasharray":name==="Mean"?"7 4":"3 5"},name+": "+fmt(v)+" "+unit));
    const counts=new Map();
    for(const v of st.b){const count=counts.get(v)||0;counts.set(v,count+1);
      const dot=el("circle",{cx:x(v),cy:baseline-12-count*14,r:5,class:"summary17-dot"},fmt(v)+" "+unit);
      svg.append(dot);
    }
    const xLabel=el("text",{x:W/2,y:252,"text-anchor":"middle",class:"summary17-axis-label"});
    xLabel.textContent="Travel time ("+unit+")";svg.append(xLabel);chart.replaceChildren(svg);
    caption.textContent="Hypothetical sample. Vertical markers: mean (long-dashed), median, Q1 and Q3. Every dot is one observation.";
    const table=document.createElement("table");table.className="summary17-table";
    const data=[
      ["Sample size",st.n],["Mean",fmt(st.mean)],["Median",fmt(st.median)],
      ["Minimum, maximum",fmt(st.b[0])+", "+fmt(st.b[st.n-1])],
      ["Q1, Q3",fmt(st.q1)+", "+fmt(st.q3)],["Range",fmt(st.range)],["IQR",fmt(st.iqr)],
      ["Sample variance",fmt(st.variance)+" "+(unit==="minutes"?"minutes squared":"seconds squared")],
      ["Sample standard deviation",fmt(st.sd)+" "+unit],
      ["1.5-IQR fences",st.fences.map(fmt).join(" to ")],
      ["Mean ± 2 sample SD",st.sigma.map(fmt).join(" to ")],
      ["IQR-flagged observations",st.iqrFlags.length?st.iqrFlags.join(", "):"None"],
      ["2-SD-flagged observations",st.sdFlags.length?st.sdFlags.join(", "):"None"]
    ];
    for(const [label,value] of data) {
      const tr=document.createElement("tr"),th=document.createElement("th"),td=document.createElement("td");
      th.scope="row";th.textContent=label;td.textContent=String(value);tr.append(th,td);table.append(tr);
    }
    results.replaceChildren(table);host.dataset.mean=st.mean;host.dataset.median=st.median;
  }
  host.addEventListener("click",event=>{
    const button=event.target.closest("button[data-summary17-action]");if(!button)return;
    try {
      const action=button.dataset.summary17Action;
      if(action==="reset"){unit="minutes";show(init,"Original example restored.");}
      else if(action==="apply"){show(read(),"Values updated. Compare the center and spread.");}
      else if(action==="extreme"){const data=read(),index=data.indexOf(Math.max(...data));data[index]=unit==="minutes"?50:3000;show(data,"The largest observation changed; compare mean and median.");}
      else if(action==="seconds"){if(unit==="seconds")throw Error("Already in seconds. Reset for minutes.");const data=read();unit="seconds";show(data.map(x=>x*60),"Times converted to seconds: spread scales, but shape is unchanged.");}
    }catch(e){info.textContent=e.message;}
  });
  show(init,"Ready. Make a prediction, change the largest observation, and read the new summaries.");
}());
