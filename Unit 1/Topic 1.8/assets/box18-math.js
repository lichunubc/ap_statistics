function computeBoxplot(values) {
  const sorted = values.slice().sort((a,b)=>a-b);
  function med(a){const k=a.length;return k%2?a[(k-1)/2]:(a[k/2-1]+a[k/2])/2;}
  const h=Math.floor(sorted.length/2),q1=med(sorted.slice(0,h)),q3=med(sorted.slice(-h));
  const m=med(sorted),delta=q3-q1,low=q1-1.5*delta,high=q3+1.5*delta;
  const good=sorted.filter(v=>v>=low && v<=high);
  return {sorted,q1,q3,m,delta,low,high,good};
}
