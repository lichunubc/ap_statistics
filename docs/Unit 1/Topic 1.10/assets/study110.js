/* Interactive investigative question builder and study-design choices. */
(function(){
"use strict";
var builder=document.querySelector("[data-study110-builder]");
if(builder){
  var goal=builder.querySelector("[data-study110-goal]"),outcome=builder.querySelector("[data-study110-outcome]"),panel=builder.querySelector("[data-study110-question]");
  var v={attendance:{noun:"willingness to attend morning review",mean:"proportion",parameter:"population proportion"},quiz:{noun:"next quiz score (points)",mean:"mean quiz score",parameter:"population mean quiz score"},sleep:{noun:"hours of sleep on school nights",mean:"mean hours of sleep",parameter:"population mean sleep duration"}};
  function updateBuilder(){
    var q=v[outcome.value],population="current grade 10 students at this school",x=goal.value;
    var question,parameter,design;
    if(x==="estimate"){question=outcome.value==="attendance"?"What proportion of "+population+" would attend morning review?":"What is the "+q.mean+" among "+population+"?";parameter=q.parameter+" among "+population;design="Choose a sample representing the target population and measure the outcome consistently.";}
    else if(x==="compare"){question="Among "+population+", is "+q.mean+" greater for students assigned morning review than for those assigned no review?";parameter="Difference between population "+q.mean+" values under the two assigned conditions";design="Random assignment is needed for a defensible causal interpretation; population sampling affects generalization.";}
    else{question="Among "+population+", is students' voluntary review attendance associated with "+q.noun+"?";parameter="Population association of naturally occurring attendance and "+q.noun;design="Observe, rather than assign, attendance; examine plausible confounders.";}
    panel.replaceChildren();
    function add(tag,text){var e=document.createElement(tag);e.textContent=text;panel.appendChild(e);}
    add("strong","Investigative question");add("p",question);add("p","Target: "+parameter+".");add("p",design);
  }
  goal.addEventListener("change",updateBuilder);outcome.addEventListener("change",updateBuilder);
  builder.querySelector("[data-study110-builder-reset]").addEventListener("click",function(){goal.value="estimate";outcome.value="attendance";updateBuilder();});updateBuilder();
}
var lab=document.querySelector("[data-study110-lab]");
if(lab){
  var selection=lab.querySelector("[data-study110-selection]"),type=lab.querySelector("[data-study110-type]"),assignment=lab.querySelector("[data-study110-assignment]");
  function render(){
    var imposed=type.value==="impose";assignment.disabled=!imposed;
    if(!imposed)assignment.value="none";else if(assignment.value==="none")assignment.value="random";
    var s=selection.value==="random",a=imposed&&assignment.value==="random";
    lab.querySelector('[data-study110-node="selection"]').textContent=s?"Randomly selected students":"Volunteers / convenience sample";
    lab.querySelector('[data-study110-node="treatment"]').textContent=imposed?(a?"Randomly assigned treatment":"Deliberately assigned treatment"):"Observed existing habits";
    function sentence(selector,title,detail){
      var el=lab.querySelector(selector),b=document.createElement("strong");b.textContent=title+": ";el.replaceChildren(b,document.createTextNode(detail));
    }
    sentence("[data-study110-generalize]","Generalization",s?"With appropriate measurement and response, inference may extend to the sampled school population.":"Broad population generalization is limited; evidence applies primarily to participants and similar people.");
    sentence("[data-study110-cause]","Causation",a?"Random treatment assignment supports a causal comparison if the rest of the study is sound.":imposed?"Treatment was imposed, but deliberate assignment can leave pre-existing differences between groups.":"No treatment was assigned; the observed association alone does not establish causation.");
    lab.querySelector("[data-study110-explain]").textContent=imposed?(a?"Randomization does not guarantee exactly balanced groups, cure attrition or repair inaccurate outcomes.":"The assignment method may create systematically different groups."):"Consider confounders associated with both voluntary attendance and quiz scores.";
  }
  [selection,type,assignment].forEach(function(e){e.addEventListener("change",render)});
  lab.querySelector("[data-study110-lab-reset]").addEventListener("click",function(){selection.value="voluntary";type.value="observe";assignment.value="none";render();});
  render();
}
}());