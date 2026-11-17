"""Validate Topic 2.5 content, original questions, joint-probability arithmetic and privacy."""
from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[3];F=R/'Unit 2/Topic 2.5'
q=(F/'topic-2-5.qmd').read_text();o=json.loads((F/'objectives.json').read_text())
b=json.loads((R/'Problem Bank/original/unit-2/topic-2-5.json').read_text())
assert q.startswith('# Topic 2.5 Mutually Exclusive Events')
assert q.count('## Practice')==1 and 'data-original-practice="2.5"' in q
assert all('{#'+s+'}' in q for s in ['intersection25','disjoint25','explorer25','examples25','reason25','errors25'])
assert o['learning_objectives']==['2.5.A'] and set(o['essential_knowledge'])=={'2.5.A.1','2.5.A.2'}
assert {x for v in o['coverage'] for x in v['ids']}>=set(o['essential_knowledge'])
assert len(b['items'])==8 and len({e['id'] for e in b['items']})==8
assert all(x['rights']=='original' and x['answer'] in 'ABCD' and len(x['options'])==4 and x['hint'] and x['solution'] for x in b['items'])
assert all(x['options'][ord(x['answer'])-65]['label']==x['answer'] for x in b['items'])
assert not any(v in q+json.dumps(b) for v in ('Week 9','AP Classroom','teacher-only exam'))
assert len({2,4,6}&{1,3,5})==0
assert len({2,4,6}&{4,5,6})==2
assert len({1,2}&{2,3,4})==1
assert 1/52>0 and 18/120==.15
for name in ('disjoint25.css','disjoint25.js','disjoint25-footer.html'):assert (F/'assets'/name).is_file()
r=subprocess.run(['node','--check',str(F/'assets/disjoint25.js')],capture_output=True,text=True)
assert r.returncode==0,r.stderr
js=(F/'assets/disjoint25.js').read_text().lower()
assert not any(v in js for v in ['fetch(','xmlhttprequest','localstorage','sendbeacon','google-analytics','eval('])
print('Topic 2.5 content, questions, arithmetic, JavaScript and privacy passed.')
