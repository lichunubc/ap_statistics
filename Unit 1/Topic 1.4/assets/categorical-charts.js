/* Topic 1.4: accessible, dependency-free categorical graph laboratory.
 * Counts mirror data/foundations.json and are checked independently by check_charts.py.
 * No network calls, local storage, student identifiers, or telemetry.
 */
(() => {
  'use strict';
  const labels = ['Walk', 'Bicycle', 'Bus', 'Car'];
  const groups = {
    A: {label:'School A', n:40, counts:[8,6,18,8]},
    B: {label:'School B', n:60, counts:[9,6,18,27]}
  };
  const colors = ['#147c85','#d3a047','#7772aa','#5b9e75'];
  const sum = values => values.reduce((total,value) => total+value,0);
  const percentage = (value,total) => 100*value/total;
  const displayPct = (value,total) => percentage(value,total).toFixed(1).replace(/\.0$/,'')+'%';
  const deg = (value,total) => Math.round(value/total*360);
  const esc = value => String(value).replace(/[&<>"']/g, ch =>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const format = (value,type) => type === 'count' ? String(value) : String(value)+'%';
  const svgStart = desc => '<svg class="cat-viz" viewBox="0 0 780 392" role="img" aria-label="'+esc(desc)+'"><title>'+
    esc(desc)+'</title>';
  function singleBars(group,type,step) {
    const relative = type === 'percent';
    const maximum = relative ? 50 : 30;
    const ticks = relative ? [0,10,20,30,40,50] : [0,10,20,30];
    const y0=308, top=53, height=y0-top;
    const count = group.counts;
    const description=group.label+': '+labels.map((name,i)=>
      name+' '+count[i]+' students ('+displayPct(count[i],group.n)+')').join(', ')+'.';
    let svg=svgStart(description);
    ticks.forEach(value => {
      const y=y0-height*value/maximum;
      svg+='<line class="gridline" x1="89" y1="'+y+'" x2="753" y2="'+y+'"></line>'+
        '<text class="cat-tick" x="80" y="'+(y+5)+'" text-anchor="end">'+value+
        (relative?'%':'')+'</text>';
    });
    svg+='<line class="axis" x1="90" y1="'+top+'" x2="90" y2="'+y0+'"></line>'+
      '<line class="axis" x1="90" y1="'+y0+'" x2="755" y2="'+y0+'"></line>'+
      '<text class="cat-axis-label" x="91" y="27">'+(relative?'Percentage of sampled students':'Number of sampled students')+'</text>';
    count.forEach((value,i) => {
      const x=164+160*i;
      svg+='<text class="cat-axis-label" x="'+x+'" y="341" text-anchor="middle">'+labels[i]+'</text>';
      if(i<step){
        const plotted=relative ? percentage(value,group.n) : value;
        const barHeight=height*plotted/maximum;
        const y=y0-barHeight;
        svg+='<rect data-cat-bar="'+i+'" class="cat-chart-bar bar-outline" x="'+(x-40)+
          '" y="'+y+'" width="80" height="'+barHeight+'" fill="'+colors[i]+'"></rect>'+
          '<text class="cat-value-label" x="'+x+'" y="'+(y-9)+'" text-anchor="middle">'+
          (relative?displayPct(value,group.n):value)+'</text>';
      }
    });
    svg+='<text class="cat-axis-label" x="420" y="379" text-anchor="middle">Usual main travel method</text></svg>';
    return svg;
  }
  function polar(cx,cy,r,angle) {
    const radians=angle*Math.PI/180;
    return [(cx+r*Math.cos(radians)).toFixed(3),(cy+r*Math.sin(radians)).toFixed(3)];
  }
  function pieSector(cx,cy,r,start,sweep) {
    const a=polar(cx,cy,r,start),b=polar(cx,cy,r,start+sweep);
    return 'M '+cx+' '+cy+' L '+a.join(' ')+' A '+r+' '+r+' 0 '+(sweep>180?1:0)+' 1 '+
      b.join(' ')+' Z';
  }
  function pie(group,step) {
    let svg=svgStart(group.label+': pie chart of '+group.n+' sampled students. Each of the four categories represents a disjoint share of the full sample.');
    const cx=250,cy=193,r=130;
    svg+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="#e9eef0" stroke="#47646b" stroke-width="1"></circle>';
    let angle=-90;
    group.counts.forEach((count,i) => {
      const sweep=count/group.n*360;
      if(i<step) svg+='<path data-cat-sector="'+i+'" class="cat-pie-sector" d="'+
        pieSector(cx,cy,r,angle,sweep)+'" fill="'+colors[i]+'" stroke="#fff" stroke-width="2"></path>';
      angle+=sweep;
      const y=112+53*i;
      svg+='<rect x="450" y="'+(y-17)+'" width="18" height="18" fill="'+colors[i]+'"></rect>'+
        '<text class="cat-legend" x="481" y="'+(y-2)+'">'+labels[i]+': '+
        displayPct(count,group.n)+' · '+deg(count,group.n)+'°</text>';
    });
    svg+='<text class="cat-tick" x="250" y="354" text-anchor="middle">'+
      'One circle = '+group.n+' sampled students</text></svg>';
    return svg;
  }
  function groupTable(g) {
    return '<div class="cat-chart-data"><table class="compact-table">'+
      '<caption>Complete frequency table: '+esc(g.label)+' (n = '+g.n+')</caption>'+
      '<thead><tr><th scope="col">Method</th><th scope="col">Count</th><th scope="col">Sample share</th><th scope="col">Pie angle</th></tr></thead><tbody>'+
      labels.map((name,i)=>'<tr><th scope="row">'+name+'</th><td>'+g.counts[i]+
        '</td><td>'+displayPct(g.counts[i],g.n)+'</td><td>'+deg(g.counts[i],g.n)+'°</td></tr>').join('')+
      '</tbody><tfoot><tr><th scope="row">Total</th><td>'+g.n+
      '</td><td>100%</td><td>360°</td></tr></tfoot></table></div>';
  }
  function builder(root) {
    let source='A',type='count',step=0;
    root.innerHTML='<h3>Build the categorical graph</h3>'+
      '<p class="small-note">The underlying observations never change when you change the representation.</p>'+
      '<div class="controls"><label>Dataset <select data-source aria-label="Select sample"><option value="A">School A · 40 sampled students</option>'+
      '<option value="B">School B · 60 sampled students</option></select></label>'+
      '<label>Graph type <select data-type aria-label="Select chart type">'+
      '<option value="count">Frequency bar chart</option><option value="percent">Percentage bar chart</option>'+
      '<option value="pie">Pie chart</option></select></label></div>'+
      '<div class="controls"><button type="button" data-next class="primary">Draw next category</button>'+
      '<button type="button" data-full>Show complete graph</button>'+
      '<button type="button" data-reset>Clear drawing</button></div>'+
      '<div class="cat-chart-stage" data-plot></div><div data-table></div>'+
      '<p class="status" role="status" aria-live="polite"></p>';
    const status=root.querySelector('.status');
    const plot=root.querySelector('[data-plot]'),table=root.querySelector('[data-table]');
    function render(){
      const group=groups[source];
      root.dataset.step=String(step);
      root.dataset.group=source;root.dataset.mode=type;
      root.dataset.total=String(sum(group.counts));
      plot.innerHTML=type==='pie'?pie(group,step):singleBars(group,type,step);
      table.innerHTML=groupTable(group);
      root.querySelector('[data-next]').disabled=step===4;
      root.querySelector('[data-full]').disabled=step===4;
      root.querySelector('[data-reset]').disabled=step===0;
      const typeText=type==='pie'?'pie-chart slice':type==='percent'?'percentage bar':'count bar';
      status.textContent=step===0?
        'Ready: no slices or bars drawn. The table lists all '+group.n+' recorded responses.':
        step===4?
        'Complete '+group.label+' graph: all four '+typeText+'s are drawn. Counts total '+group.n+'; relative shares total 100%.':
        'Drawn '+step+' of 4 categories. Latest '+typeText+': '+labels[step-1]+' = '+
          group.counts[step-1]+' of '+group.n+' ('+displayPct(group.counts[step-1],group.n)+
          '), pie angle '+deg(group.counts[step-1],group.n)+'°. ';
    }
    root.querySelector('[data-source]').addEventListener('change',e=>{source=e.target.value;step=0;render();});
    root.querySelector('[data-type]').addEventListener('change',e=>{type=e.target.value;step=0;render();});
    root.querySelector('[data-next]').addEventListener('click',()=>{step=Math.min(4,step+1);render();});
    root.querySelector('[data-full]').addEventListener('click',()=>{step=4;render();});
    root.querySelector('[data-reset]').addEventListener('click',()=>{step=0;render();});
    render();
  }
  function compareBars(type) {
    const relative=type==='percent',maximum=relative?50:30;
    const ticks=relative?[0,10,20,30,40,50]:[0,10,20,30];
    const y0=304,top=57,scale=(y0-top)/maximum;
    let svg=svgStart('Two samples compared by '+(relative?'within-group percentages':'counts')+
      '. School A n=40, School B n=60. Bus: 18 (45%) in A and 18 (30%) in B.');
    ticks.forEach(t=>{
      const y=y0-t*scale;
      svg+='<line class="gridline" x1="90" y1="'+y+'" x2="753" y2="'+y+'"></line>'+
        '<text class="cat-tick" x="78" y="'+(y+4)+'" text-anchor="end">'+t+(relative?'%':'')+'</text>';
    });
    svg+='<line class="axis" x1="90" y1="'+top+'" x2="90" y2="'+y0+'"></line>'+
      '<line class="axis" x1="90" y1="'+y0+'" x2="755" y2="'+y0+'"></line>'+
      '<text class="cat-axis-label" x="95" y="26">'+
      (relative?'Percent within each sampled school':'Number of sampled students')+'</text>';
    labels.forEach((name,i)=>{
      const center=178+i*156;
      svg+='<text class="cat-axis-label" x="'+center+'" y="336" text-anchor="middle">'+name+'</text>';
      ['A','B'].forEach((key,j)=>{
        const group=groups[key],v=group.counts[i];
        const plotted=relative?percentage(v,group.n):v;
        const h=plotted*scale,x=center+(j===0?-39:5),y=y0-h;
        svg+='<rect data-sample="'+key+'" data-category="'+i+'" class="cat-compare-bar bar-outline sample-'+key.toLowerCase()+
          '" x="'+x+'" y="'+y+'" width="34" height="'+h+'"></rect>'+
          '<text class="cat-value-label" x="'+(x+17)+'" y="'+(y-8)+'" text-anchor="middle" font-size="12">'+
          (relative?displayPct(v,group.n):v)+'</text>';
      });
    });
    svg+='<rect x="275" y="355" width="16" height="16" class="sample-a"></rect>'+
      '<text class="cat-legend" x="298" y="369">School A (n=40)</text>'+
      '<rect x="489" y="355" width="16" height="16" class="sample-b"></rect>'+
      '<text class="cat-legend" x="512" y="369">School B (n=60)</text></svg>';
    return svg;
  }
  function comparisonTable(active) {
    return '<div class="cat-chart-data"><table class="compact-table"><caption>Same categorical variable in two independent hypothetical school samples</caption>'+
      '<thead><tr><th scope="col">Method</th><th scope="col">A (n=40)</th><th scope="col">A %</th>'+
      '<th scope="col">B (n=60)</th><th scope="col">B %</th></tr></thead><tbody>'+
      labels.map((name,i)=>'<tr'+(i===active?' class="active"':'')+'><th scope="row">'+name+
        '</th><td>'+groups.A.counts[i]+'</td><td>'+displayPct(groups.A.counts[i],40)+
        '</td><td>'+groups.B.counts[i]+'</td><td>'+displayPct(groups.B.counts[i],60)+'</td></tr>').join('')+
      '</tbody></table></div>';
  }
  function compare(root){
    let type='percent',active=-1;
    root.innerHTML='<h3>Compare School A and School B</h3>'+
      '<div class="controls"><label>Shared vertical scale <select data-scale aria-label="Compare counts or percentages">'+
      '<option value="percent">Within-group percentages</option><option value="count">Sample counts</option></select></label></div>'+
      '<div class="cat-chart-stage" data-plot></div>'+
      '<p><strong>Choose a method to interpret:</strong></p><div class="cat-compare-nav" data-buttons></div>'+
      '<p class="status" role="status" aria-live="polite"></p><div data-table></div>';
    root.querySelector('[data-buttons]').innerHTML=labels.map((name,i)=>
      '<button type="button" data-category-choice="'+i+'" aria-pressed="false">'+name+'</button>').join('');
    function render(){
      root.dataset.mode=type;
      root.dataset.selected=active===-1?'':String(active);
      root.querySelector('[data-plot]').innerHTML=compareBars(type);
      root.querySelector('[data-table]').innerHTML=comparisonTable(active);
      root.querySelectorAll('[data-category-choice]').forEach(b=>
        b.setAttribute('aria-pressed',String(Number(b.dataset.categoryChoice)===active)));
      const status=root.querySelector('.status');
      if(active<0){
        status.textContent='No method selected. Choose a category to compare its count and percentage across the two samples.';
      }else{
        const a=groups.A.counts[active],b=groups.B.counts[active];
        const pa=percentage(a,40),pb=percentage(b,60);
        status.textContent=labels[active]+': School A '+a+' of 40 ('+displayPct(a,40)+
          '); School B '+b+' of 60 ('+displayPct(b,60)+'). '+
          (pa===pb?'The sampled shares are equal.':
            (pa>pb?'School A':'School B')+' has a sample share '+Math.abs(pa-pb).toFixed(1).replace(/\.0$/,'')+
            ' percentage points higher.')+
          (active===2?' The counts are both 18, but the sample percentages differ.':'')+
          ' The comparison is descriptive; it does not establish full-school population proportions.';
      }
    }
    root.querySelector('[data-scale]').addEventListener('change',e=>{type=e.target.value;render();});
    root.querySelectorAll('[data-category-choice]').forEach(button=>
      button.addEventListener('click',()=>{active=Number(button.dataset.categoryChoice);render();}));
    render();
  }
  const cases=[
    {
      question:'In the School A sample, Bus is the largest category at 45%. Which claim is supported?',
      choices:['A majority of all 1,000 School A students use Bus.','Bus was the most frequent method among the 40 sampled students.','The population Bus proportion is exactly 45%.'],
      correct:1,
      why:'Eighteen Bus responses exceed every other individual category, so Bus is the sample modal category. But 18/40=45% is not a majority, and the sample does not reveal the exact population share.'
    },
    {
      question:'Both school samples contain 18 bus riders. Which visual comparison best conveys relative use?',
      choices:['A count-only chart proves both schools have the same Bus share.','A pie combining both schools into one circle answers the within-school question.','Use within-school percentages: 45% (A) versus 30% (B).'],
      correct:2,
      why:'Each share uses its own school-sample denominator: 18/40=45% for A and 18/60=30% for B. Equal counts do not imply equal relative frequencies.'
    },
    {
      question:'A frequency bar chart begins its vertical axis at 7 instead of 0. What is the main concern?',
      choices:['Truncation exaggerates bar-length differences.','The chart must be a histogram.','All categorical axes should begin at 7.'],
      correct:0,
      why:'Bar length is measured from a baseline. Omitting the bottom portion can make small differences seem proportionally much larger; start a conventional frequency bar chart at zero.'
    },
    {
      question:'Movie satisfaction levels are recoded as 1,2,3,4,5. How should the chart be interpreted?',
      choices:['The numbers guarantee equal intervals between satisfaction levels.','Keep the natural order; these remain ordered categorical levels.','Always sort the categories alphabetically.'],
      correct:1,
      why:'A one-to-one code retains category identity and ordering. Numeric labels do not automatically create a quantitative scale with equal distances.'
    },
    {
      question:'A survey lets each person check every transport method they use. Is a single pie chart of respondent-selection rates appropriate?',
      choices:['Yes; overlapping percentages must sum to 100%.','Yes; a three-dimensional pie fixes the overlap.','Not generally; a person can appear in several categories, so the slices need not partition one whole.'],
      correct:2,
      why:'A conventional pie divides one whole into disjoint categories. Multiple-response counts may overlap and their percentages of people may total more than 100%. A bar chart of labelled selection rates is clearer.'
    }
  ];
  function audit(root){
    let index=0;
    root.innerHTML='<h3>Inspect the evidence</h3><div class="controls">'+
      '<button type="button" data-next>Next case</button><button type="button" data-clear>Clear answer</button></div>'+
      '<p data-progress class="small-note"></p><p data-question style="font-weight:650"></p>'+
      '<div class="choice-list"></div><p class="status" role="status" aria-live="polite"></p>';
    function render(){
      const item=cases[index];
      root.dataset.case=String(index);root.dataset.selected='';
      root.querySelector('[data-progress]').textContent='Case '+(index+1)+' of '+cases.length;
      root.querySelector('[data-question]').textContent=item.question;
      root.querySelector('.choice-list').innerHTML=item.choices.map((choice,i)=>
        '<button type="button" data-option="'+i+'" aria-pressed="false"><strong>'+
          String.fromCharCode(65+i)+'.</strong> '+esc(choice)+'</button>').join('');
      root.querySelector('.status').textContent='No answer selected. Choose one option.';
      root.querySelectorAll('[data-option]').forEach(button=>button.addEventListener('click',()=>{
        const selected=Number(button.dataset.option);
        root.dataset.selected=String(selected);
        root.querySelectorAll('[data-option]').forEach(b=>{
          b.setAttribute('aria-pressed','false');b.classList.remove('correct','incorrect');
        });
        button.setAttribute('aria-pressed','true');
        button.classList.add(selected===item.correct?'correct':'incorrect');
        root.querySelector('.status').textContent=
          (selected===item.correct?'Correct. ':'Not quite. ')+item.why;
      }));
    }
    root.querySelector('[data-next]').addEventListener('click',()=>{
      index=(index+1)%cases.length;render();
    });
    root.querySelector('[data-clear]').addEventListener('click',render);
    render();
  }
  const init={builder,compare,audit};
  document.querySelectorAll('[data-cat-chart]').forEach(root=>{
    if(init[root.dataset.catChart])init[root.dataset.catChart](root);
  });
  let printed=[];
  const removePrint=()=>{printed.forEach(x=>x.remove());printed=[];};
  window.addEventListener('beforeprint',()=>{
    removePrint();
    document.querySelectorAll('[data-cat-chart]').forEach(root=>{
      const reference=document.createElement('section');
      reference.className='cat-chart-print';
      const kind=root.dataset.catChart;
      if(kind==='builder'){
        reference.innerHTML='<h3>Completed School A reference charts</h3>'+
          singleBars(groups.A,'count',4)+pie(groups.A,4)+groupTable(groups.A);
      }else if(kind==='compare'){
        reference.innerHTML='<h3>Comparison of within-group percentages</h3>'+
          compareBars('percent')+comparisonTable(-1)+
          '<p>Bus: 18/40=45% for School A; 18/60=30% for School B.</p>';
      }else{
        reference.innerHTML='<h3>Chart-audit answer key</h3>'+cases.map((item,i)=>
          '<p><strong>Case '+(i+1)+': '+String.fromCharCode(65+item.correct)+'.</strong> '+
          esc(item.choices[item.correct])+' '+esc(item.why)+'</p>').join('');
      }
      root.after(reference);printed.push(reference);
    });
  });
  window.addEventListener('afterprint',removePrint);
  window.CAT_CHART_TEST=Object.freeze({
    A:Object.freeze(groups.A.counts.slice()),B:Object.freeze(groups.B.counts.slice()),
    nA:groups.A.n,nB:groups.B.n,
    anglesA:Object.freeze(groups.A.counts.map(x=>deg(x,groups.A.n))),
    anglesB:Object.freeze(groups.B.counts.map(x=>deg(x,groups.B.n))),
    answerKeys:Object.freeze(cases.map(c=>c.correct))
  });
})();
