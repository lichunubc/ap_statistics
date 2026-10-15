/* Deterministic numerical engine for Topic 1.9: original hypothetical teaching values. */
(function(root){
"use strict";
const scenarios=Object.freeze({
 original:{a:[12,14,15,15,16,16,17,17,18,18,19,21],b:[9,10,11,12,13,13,14,15,16,17,19,38]},
 replaced:{a:[12,14,15,15,16,16,17,17,18,18,19,21],b:[9,10,11,12,13,13,14,15,16,17,19,20]},
 shifted:{a:[12,14,15,15,16,16,17,17,18,18,19,21],b:[17,19,20,20,21,21,22,22,23,23,24,26]},
 concentrated:{a:[12,14,15,15,16,16,17,17,18,18,19,21],b:[14,14,14,14,15,15,15,16,16,16,16,17]}
});
function median(a){if(!a.length)throw new Error("Cannot find median of empty set");const m=Math.floor(a.length/2);return a.length%2?a[m]:(a[m-1]+a[m])/2;}
function summary(values) {
 if(!Array.isArray(values)||values.length<3||values.some(v=>typeof v!=="number"||!Number.isFinite(v)))throw new Error("Expect at least three finite observations.");
 const a=[...values].sort((x,y)=>x-y),n=a.length,k=Math.floor(n/2);
 const mean=a.reduce((s,v)=>s+v,0)/n, med=median(a),q1=median(a.slice(0,k)),q3=median(a.slice(n%2?k+1:k)),iqr=q3-q1;
 const variance=a.reduce((s,v)=>s+(v-mean)**2,0)/(n-1),sd=Math.sqrt(variance),low=q1-1.5*iqr,high=q3+1.5*iqr;
 const within=a.filter(v=>v>=low&&v<=high),outliers=a.filter(v=>v<low||v>high);
 return {sorted:a,n,mean,median:med,q1,q3,iqr,sd,variance,min:a[0],max:a[n-1],range:a[n-1]-a[0],low,high,within,outliers,leftWhisker:within[0]??a[0],rightWhisker:within.at(-1)??a[n-1]};
}
function zScore(value,mean,sd){if(![value,mean,sd].every(Number.isFinite)||sd<=0)throw new Error("Finite values and positive standard deviation required");return (value-mean)/sd;}
function frequencies(values,min=0,max=45,width=5){
 if(!Number.isInteger((max-min)/width))throw new Error("Invalid bin design");
 const bins=Array((max-min)/width).fill(0);
 for(const v of values){
   if(v<min||v>max)throw new Error("Value outside histogram axis");
   bins[Math.min(bins.length-1,Math.floor((v-min)/width))]++;
 }
 return bins;
}
root.COMPARE19_MATH={scenarios,summary,zScore,frequencies};
})(typeof window==="undefined"?globalThis:window);
