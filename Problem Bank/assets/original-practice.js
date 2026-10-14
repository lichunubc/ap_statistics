/* Public original questions: no user data leaves the browser. */
(function () {
  "use strict";
  const hosts=[...document.querySelectorAll("[data-original-practice]")];
  if(!hosts.length)return;
  const build=(tag,klass,text)=>{
    const x=document.createElement(tag);
    if(klass)x.className=klass;
    if(text!==undefined)x.textContent=text;
    return x;
  };
  hosts.forEach(async host=>{
    const topic=host.dataset.originalPractice, url=host.dataset.bankUrl||("../../Problem%20Bank/original/unit-1/topic-1-7.json");
    let items=[],at=0,selected=null;
    const status=build("p","original-status","");
    status.setAttribute("role","status");status.setAttribute("aria-live","polite");
    const shell=build("div","original-shell");host.replaceChildren(shell,status);
    async function load(){
      const response=await fetch(url,{cache:"no-cache"});
      if(!response.ok)throw Error("Could not load the original-practice file (HTTP "+response.status+").");
      const pack=await response.json();
      if(pack.schema_version!==1||pack.topic!==topic||!Array.isArray(pack.items)||!pack.items.length)throw Error("Practice file is invalid or belongs to another topic.");
      const ids=new Set();
      for(const q of pack.items){
        if(!q.id||ids.has(q.id)||typeof q.prompt!=="string"||!["mc","number","written"].includes(q.type)||typeof q.solution!=="string")throw Error("Malformed or duplicate practice question.");
        if(q.type==="mc"&&(!Array.isArray(q.options)||q.options.length<2||!q.options.some(opt=>opt.label===q.answer)))throw Error("Invalid multiple-choice key.");
        if(q.type==="number"&&(!Number.isFinite(q.answer)||!Number.isFinite(q.tolerance)))throw Error("Invalid numerical answer key.");
        ids.add(q.id);
      }
      items=pack.items;render();
    }
    function render(){
      const q=items[at],heading=build("h3","original-question-title","Question "+(at+1)+" of "+items.length);
      const meta=build("p","original-meta",q.difficulty+" · "+q.id+" · "+q.tags.join(", "));
      const question=build("p","original-prompt",q.prompt);
      const answerArea=build("div","original-answer");let field=null;
      if(q.type==="mc"){
        const f=build("fieldset"),legend=build("legend","","Choose one answer");f.append(legend);
        for(const opt of q.options){
          const label=build("label","original-choice");
          const radio=build("input");radio.type="radio";radio.name="original-"+q.id;radio.value=opt.label;label.append(radio,document.createTextNode(" "+opt.label+". "+opt.text));f.append(label);
        }
        answerArea.append(f);field=f;
      }else if(q.type==="number"){
        const label=build("label","original-response-label","Your numerical answer");
        const input=build("input");input.type="number";input.step="any";input.autocomplete="off";
        input.setAttribute("aria-label","Numerical answer for question "+(at+1));
        label.append(input);answerArea.append(label);field=input;
      }else{
        const label=build("label","original-response-label","Your written justification");
        const textarea=build("textarea");textarea.rows=4;textarea.placeholder="Explain in context; include numerical evidence and limitations.";
        label.append(textarea);answerArea.append(label);field=textarea;
      }
      const feedback=build("p","original-feedback","");
      feedback.setAttribute("role","status");feedback.setAttribute("aria-live","polite");
      const hint=build("div","original-hint"),solution=build("div","original-solution");
      hint.hidden=true;solution.hidden=true;
      hint.append(build("p","",q.hint||"Revisit the relevant worked example."));
      solution.append(build("strong","",q.type==="written"?"Model answer and self-check rubric":"Worked solution"));
      solution.append(build("p","",q.solution));
      if(q.type==="written")solution.append(build("p","",q.rubric||"Check your justification, evidence and context."));
      const controls=build("div","original-controls");
      const make=(label,act,handler)=>{
        const b=build("button","original-button",label);b.type="button";b.dataset.action=act;
        b.addEventListener("click",handler);controls.append(b);return b;
      };
      const prior=make("Previous","previous",()=>{at--;render();});prior.disabled=at===0;
      const next=make("Next question","next",()=>{at++;render();});next.disabled=at===items.length-1;
      make("Check answer","check",()=>{
        if(q.type==="mc"){
          const value=field.querySelector("input:checked");
          if(!value){feedback.textContent="Choose an answer before checking.";return;}
          feedback.textContent=value.value===q.answer?"Correct. Explain why the alternatives are unsuitable.":"Not yet. Use the hint or review the worked example.";
        }else if(q.type==="number"){
          const value=field.value.trim(),n=Number(value);
          if(!value||!Number.isFinite(n)){feedback.textContent="Enter a numerical answer before checking.";return;}
          feedback.textContent=Math.abs(n-q.answer)<=q.tolerance?"Correct, within rounding tolerance.":"Not yet. Check the formula and units.";
        }else{
          if(!field.value.trim()){feedback.textContent="Write a justification first; then compare against the model answer.";return;}
          feedback.textContent="Written response saved only in this page. Reveal the model answer to self-assess; no automated grading is performed.";
        }
      });
      const hintBtn=make("Show hint","hint",()=>{
        hint.hidden=!hint.hidden;hintBtn.textContent=hint.hidden?"Show hint":"Hide hint";
      });
      const solutionBtn=make("Show solution","solution",()=>{
        solution.hidden=!solution.hidden;solutionBtn.textContent=solution.hidden?"Show solution":"Hide solution";
      });
      make("Reset question","reset",()=>render());
      const aside=build("p","original-privacy","Teacher-authored practice. Responses stay in this page and are not transmitted or tracked.");
      shell.replaceChildren(heading,meta,question,answerArea,feedback,controls,hint,solution,aside);
      status.textContent="Showing question "+(at+1)+" of "+items.length+".";
    }
    function printAll(){
      if(!items.length)return;
      const print=build("section","original-print-set");
      print.append(build("h3","", "Original practice: Topic "+topic+" — questions and solutions"));
      for(const q of items){
        const article=build("article","original-print-question");
        article.append(build("h4","",q.id),build("p","",q.prompt));
        if(q.options)for(const option of q.options)article.append(build("p","",option.label+". "+option.text));
        article.append(build("p","", "Solution: "+q.solution));
        if(q.rubric)article.append(build("p","", "Rubric: "+q.rubric));
        print.append(article);
      }
      host.append(print);
    }
    const before=()=>printAll();
    const after=()=>host.querySelector(".original-print-set")?.remove();
    window.addEventListener("beforeprint",before);window.addEventListener("afterprint",after);
    try{await load();}catch(error){status.textContent="Practice unavailable: "+error.message;host.dataset.loadError="true";}
  });
}());
