"""Content, mathematics, public rights and JavaScript syntax for Topic 1.12."""
from pathlib import Path
import json, subprocess
root=Path(__file__).resolve().parents[3]
topic=root/'Unit 1/Topic 1.12'
qmd=(topic/'topic-1-12.qmd').read_text()
obj=json.loads((topic/'objectives.json').read_text())
bank=json.loads((root/'Problem Bank/original/unit-1/topic-1-12.json').read_text())
assert qmd.startswith('# Topic 1.12 Potential Problems with Sampling')
assert qmd.count('## Practice')==1
assert 'data-original-practice="1.12"' in qmd
assert (40*10+60*30)/100==22
assert obj['learning_objectives']==['1.12.A']
assert set(obj['essential_knowledge'])=={'1.12.A.'+str(i) for i in range(1,7)}
assert {a for c in obj['coverage'] for a in c['ids']}>=set(obj['essential_knowledge'])
assert all(c['section'] in qmd for c in obj['coverage'])
assert len(bank['items'])==8
assert len({i['id'] for i in bank['items']})==8
for i in bank['items']:
    assert i['rights']=='original' and i['objectives']==['1.12.A']
    assert i['solution'] and i['prompt']
    if i['type']=='mc': assert i['answer'] in 'ABCD' and len(i['options'])==4
    if i['type']=='number': assert i['answer']==22
    if i['type']=='written': assert i['rubric']
p=topic/'assets/bias112.js'
r=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
assert r.returncode==0,(r.stdout,r.stderr)
print('Topic 1.12 original practice, CED scope, arithmetic and JS syntax passed.')
