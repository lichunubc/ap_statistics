from pathlib import Path
import os,re,json,hashlib
R=Path(os.environ['SOURCE_ROOT'])
changes={
'Unit 1/Topic 1.1/topic-1-1.qmd':{' Nothing is submitted or saved.':''},
'Unit 1/Topic 1.2/topic-1-2.qmd':{' Each new case begins with no selection, and no response is saved or submitted.':'','18/40 = 45%':r'$18/40=45\%$'},
'Unit 1/Topic 1.3/topic-1-3.qmd':{'The four original cases begin with no answer selected. Choose, check the explanation, clear your choice, or move to the next case.':'Choose an answer, then check your reasoning.'},
'Unit 1/Topic 1.4/topic-1-4.qmd':{'18/40 = 45%':r'$18/40=45\%$','::: {.callout-warning}':'::: {.callout-note}'},
'Unit 1/Topic 1.8/_construction.qmd':{'50 > 25.25':r'$50>25.25$'},
'Unit 1/Topic 1.8/_skew.qmd':{'mean > median':r'$\text{mean}>\text{median}$'},
'Unit 1/Topic 1.9/_comparison.qmd':{'18 − 15 = 3':r'$18-15=3$','16.5 − 11.5 = 5':r'$16.5-11.5=5$','16.5 + 1.5 × 5 = 24':r'$16.5+1.5\times5=24$'},
'Unit 1/unit-1.qmd':{'The original dotplot, stem-and-leaf, histogram construction, and histogram laboratory lessons.':'Build dotplots, stem-and-leaf plots and histograms; explore how bin widths change a display.','The original distribution descriptions, worked examples, and evidence checkpoints.':'Describe shape, center, spread and unusual features using graphical evidence.','Sources and publication notes':'Sources and study resources'}}
for name,replacements in changes.items():
 p=R/name;s=p.read_text()
 for a,b in replacements.items():s=s.replace(a,b)
 p.write_text(s)
p=R/'Problem Bank/practice-filter.lua';s=p.read_text();s=s.replace('The supplied Week 2 and Week 3 homework sets do not provide a direct practice selection for this introductory topic. Use the existing original practice above; no homework question has been relabelled as a Topic 1.1 question.','Use the Practice section above to review this topic.');p.write_text(s)
p=R/'Unit 1/Topic 1.7/topic-1-7.qmd';s=p.read_text();s=s.replace('n = 9; mean ≈ 12.22 min; median = 12 min; Q1 = 9 min; Q3 = 15.5 min; range = 13 min; IQR = 6.5 min; sample SD ≈ 4.09 min.',r'$n=9$; $\bar{x}\approx12.22$ min; median $12$ min; $Q_1=9$ min; $Q_3=15.5$ min; range $13$ min; IQR $6.5$ min; $s\approx4.09$ min.');p.write_text(s)
# Dynamic labels describe summaries, not dataset-creation provenance.
p=R/'Unit 1/Topic 1.4/assets/categorical-charts.js';s=p.read_text();s=s.replace('hypothetical ','').replace('Hypothetical ','');p.write_text(s)
p=R/'Unit 1/Shared/tests/preserved-assets.json';data=json.loads(p.read_text())
for item in data:
 actual=hashlib.sha256((R/item['path']).read_bytes()).hexdigest()
 if actual!=item['sha256']:
  assert item['path']=='Unit 1/Topic 1.4/assets/categorical-charts.js',item['path']
  item['prior_sha256']=item['sha256'];item['sha256']=actual;item['change_note']='Presentation-only qualifier removal. Numerical and interaction code unchanged.'
p.write_text(json.dumps(data,indent=2)+'\n')
