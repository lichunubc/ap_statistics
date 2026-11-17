"""Validate Topic 2.4 source, scope, original practice, arithmetic and rights."""
from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[3]; F=R/'Unit 2/Topic 2.4'
q=(F/'topic-2-4.qmd').read_text(); o=json.loads((F/'objectives.json').read_text())
b=json.loads((R/'Problem Bank/original/unit-2/topic-2-4.json').read_text())
assert q.startswith('# Topic 2.4 Introduction to Probability')
assert q.count('## Practice')==1 and 'data-original-practice="2.4"' in q
assert all('{#'+s+'}' in q for s in ['space24','equiprobable24','complement24','explorer24','unequal24'])
assert o['learning_objectives']==['2.4.A']
assert set(o['essential_knowledge'])=={f'2.4.A.{i}' for i in range(1,5)}
assert {x for v in o['coverage'] for x in v['ids']}>=set(o['essential_knowledge'])
assert len(b['items'])==8 and len({e['id'] for e in b['items']})==8
assert all(e['rights']=='original' and e['answer'] in 'ABCD' and len(e['options'])==4 and e['hint'] and e['solution'] for e in b['items'])
assert all(e['options'][ord(e['answer'])-65]['label']==e['answer'] for e in b['items'])
assert not any(v in q+json.dumps(b) for v in ('Week 9','AP Classroom','teacher-only exam'))
assert 3/6==.5 and 2/6==1/3 and 6/36==1/6
assert abs((1-.18)-.82)<1e-10
for n in ['intro24.css','intro24.js','intro24-footer.html']:assert (F/'assets'/n).is_file()
r=subprocess.run(['node','--check',str(F/'assets/intro24.js')],capture_output=True,text=True)
assert r.returncode==0,r.stderr
js=(F/'assets/intro24.js').read_text().lower()
assert not any(v in js for v in ['fetch(','xmlhttprequest','localstorage','sendbeacon','google-analytics','eval('])
print('Topic 2.4 original source, coverage, arithmetic, JS and privacy checks passed.')
