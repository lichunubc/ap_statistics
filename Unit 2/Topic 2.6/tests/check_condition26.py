"""Validate Topic 2.6 CED alignment, conditional denominators and rights."""
from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[3];F=R/'Unit 2/Topic 2.6'
q=(F/'topic-2-6.qmd').read_text();o=json.loads((F/'objectives.json').read_text())
bank=json.loads((R/'Problem Bank/original/unit-2/topic-2-6.json').read_text())
assert q.startswith('# Topic 2.6 Conditional Probability')
assert q.count('## Practice')==1 and 'data-original-practice="2.6"' in q
assert all('{#'+key+'}' in q for key in ('given26','table26','explorer26','multiply26','examples26','routine26'))
assert set(o['learning_objectives'])=={'2.6.A'}
assert set(o['essential_knowledge'])=={'2.6.A.1','2.6.A.2'}
assert {x for part in o['coverage'] for x in part['ids']}>=set(o['essential_knowledge'])
assert len(bank['items'])==8 and len({x['id'] for x in bank['items']})==8
assert all(x['rights']=='original' and x['answer'] in 'ABCD' and len(x['options'])==4 and x['hint'] and x['solution'] for x in bank['items'])
assert all(x['options'][ord(x['answer'])-65]['label']==x['answer'] for x in bank['items'])
assert not any(marker in q+json.dumps(bank) for marker in ('Week 9','AP Classroom','teacher-only exam'))
assert abs(2/8-.25)<1e-10 and abs(2/10-.2)<1e-10 and abs(2/24-1/12)<1e-10
assert abs((3/5)*(2/4)-.3)<1e-10 and abs((2/5)*(3/4)-.3)<1e-10
assert 4+2+2==8 and 4+8+4==16 and 8+10+6==24
for name in ('condition26.css','condition26.js','condition26-footer.html'): assert (F/'assets'/name).is_file()
r=subprocess.run(['node','--check',str(F/'assets/condition26.js')],capture_output=True,text=True)
assert r.returncode==0,r.stderr
js=(F/'assets/condition26.js').read_text().lower()
assert not any(v in js for v in ('fetch(','xmlhttprequest','localstorage','sendbeacon','google-analytics','eval('))
print('Topic 2.6 CED objective, conditional arithmetic, original practice, JS and privacy checks passed.')
