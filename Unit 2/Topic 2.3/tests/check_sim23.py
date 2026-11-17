"""Validate Topic 2.3 official scope, original practice, simulation and privacy."""
from pathlib import Path
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[3]
F=ROOT/'Unit 2/Topic 2.3'
qmd=(F/'topic-2-3.qmd').read_text()
obj=json.loads((F/'objectives.json').read_text())
bank=json.loads((ROOT/'Problem Bank/original/unit-2/topic-2-3.json').read_text())
assert qmd.startswith('# Topic 2.3 Estimating Probabilities Using Simulation')
assert qmd.count('## Practice')==1 and 'data-original-practice="2.3"' in qmd
assert all(f'{{#{sec}}}' in qmd for sec in ('model23','design23','explorer23','longrun23','device23','interpret23'))
assert obj['learning_objectives']==['2.3.A']
assert set(obj['essential_knowledge'])=={f'2.3.A.{i}' for i in range(1,8)}
assert {e for d in obj['coverage'] for e in d['ids']}>=set(obj['essential_knowledge'])
assert len(bank['items'])==8 and len({x['id'] for x in bank['items']})==8
assert all(x['rights']=='original' and x['answer'] in 'ABCD' and len(x['options'])==4 and x['solution'] and x['hint'] for x in bank['items'])
assert all(x['options'][ord(x['answer'])-65]['label']==x['answer'] for x in bank['items'])
assert len({'HHH','HHT','HTH','HTT','THH','THT','TTH','TTT'})==8
assert len({'HHH','HHT','HTH','THH'})==4
assert 505/1000==.505 and 245/500==.49 and 482/1000==.482
assert all((F/'assets'/p).is_file() for p in ('sim23.css','sim23.js','sim23-footer.html'))
r=subprocess.run(['node','--check',str(F/'assets/sim23.js')],capture_output=True,text=True)
assert r.returncode==0,r.stderr
js=(F/'assets/sim23.js').read_text().lower()
assert not any(s in js for s in ('fetch(', 'xmlhttprequest','localstorage','sendbeacon','google-analytics','eval('))
assert 'No trials yet' in qmd and 'Reset' in qmd
assert 'MHS-U2-T23-001' in json.dumps(bank)
assert 'Week 9' not in qmd and 'Week 9' not in json.dumps(bank)
print('Topic 2.3 source, curriculum, math, privacy, JavaScript and practice checks passed.')
