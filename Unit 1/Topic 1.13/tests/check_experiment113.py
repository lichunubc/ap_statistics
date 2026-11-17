"""Check Topic 1.13 Fall-2026 objectives, original practice, rights and code."""
from pathlib import Path
import json
import subprocess
root=Path(__file__).resolve().parents[3]
topic=root/'Unit 1/Topic 1.13'
qmd=(topic/'topic-1-13.qmd').read_text()
obj=json.loads((topic/'objectives.json').read_text())
bank=json.loads((root/'Problem Bank/original/unit-1/topic-1-13.json').read_text())
assert qmd.startswith('# Topic 1.13 Experimental Design')
assert qmd.count('## Practice')==1 and 'data-original-practice="1.13"' in qmd
assert obj['learning_objectives']==['1.13.A','1.13.B','1.13.C','1.13.D']
assert len(set(obj['essential_knowledge']))==20
assert set(obj['essential_knowledge']) <= {i for e in obj['coverage'] for i in e['ids']}
assert all(e['section'] in qmd for e in obj['coverage'])
assert '1.13.C.1' in obj['essential_knowledge']
for anchor in ['four-113','extraneous-113','masking-113','designs-113','lab-113','scope-113','practice-113']:
    assert '{#'+anchor+'}' in qmd
assert 'standard care plus Drug X' in qmd and 'standard care plus a matching placebo' in qmd
assert 'Scribbr' not in qmd and 'accuracy-precision-scribbr' not in qmd
assert len(bank['items'])==8 and len({x['id'] for x in bank['items']})==8
for x in bank['items']:
    assert x['rights']=='original' and x['objectives'][0].startswith('1.13.')
    assert x['solution'] and x['prompt'] and x['hint']
    if x['type']=='mc':
        assert x['answer'] in 'ABCD' and len(x['options'])==4
        assert set(o['label'] for o in x['options'])==set('ABCD')
    if x['type']=='written': assert x['rubric']
assert abs(sum([-3,-3,-4,-1])/4+2.75)<1e-12
assert len(set(obj['essential_knowledge']))==20
js=topic/'assets/experiment113.js'
css=topic/'assets/experiment113.css'
footer=topic/'assets/experiment113-footer.html'
for f in [js,css,footer]: assert f.is_file()
r=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
assert r.returncode==0,(r.stdout,r.stderr)
assert all(s not in js.read_text().lower() for s in ['fetch(', 'xmlhttprequest', 'localstorage', 'sendbeacon'])
print('Topic 1.13 source, original items, objective mapping, arithmetic, JS syntax and rights checks passed.')
