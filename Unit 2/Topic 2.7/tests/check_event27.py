"""Topic 2.7 source, CED, arithmetic, rights and implementation checks."""
from pathlib import Path
import json, subprocess
R=Path(__file__).resolve().parents[3]
F=R/'Unit 2/Topic 2.7'
q=(F/'topic-2-7.qmd').read_text(encoding='utf-8')
o=json.loads((F/'objectives.json').read_text(encoding='utf-8'))
bank=json.loads((R/'Problem Bank/original/unit-2/topic-2-7.json').read_text(encoding='utf-8'))
assert q.startswith('# Topic 2.7 Independent Events and Unions of Events')
assert q.count('## Practice')==1 and 'data-original-practice="2.7"' in q
for key in ('independence27','contrast27','union27','explorer27','cards27','complement27','routine27','practice27'):
    assert '{#'+key+'}' in q,key
assert set(o['learning_objectives'])=={'2.7.A'}
assert set(o['essential_knowledge'])=={'2.7.A.1','2.7.A.2','2.7.A.3'}
assert {x for part in o['coverage'] for x in part['ids']}>=set(o['essential_knowledge'])
assert len(bank['items'])==8
assert len({x['id'] for x in bank['items']})==8
assert all(x['rights']=='original' and x['answer'] in 'ABCD' and x['hint'] and x['solution'] and len(x['options'])==4 for x in bank['items'])
assert all(x['options'][ord(x['answer'])-65]['label']==x['answer'] for x in bank['items'])
assert not any(marker in q+json.dumps(bank) for marker in ('Week 9','AP Classroom homework','secure MCQ','teacher-only exam'))
assert abs((3+2-1)/6-2/3)<1e-12
assert abs((13+4-1)/52-4/13)<1e-12
assert abs(1-(5/6)**3-91/216)<1e-12
assert abs(1-.7**4-.7599)<1e-12
assert abs(.45+.4-.18-.67)<1e-12
cases={'evenmultiple':({2,4,6},{3,6}),'evenodd':({2,4,6},{1,3,5}),'evengreater':({2,4,6},{4,5,6}),'lowhigh':({1,2},{5,6})}
for a,b in cases.values():
    assert len(a|b)==len(a)+len(b)-len(a&b)
    assert 0<=len(a&b)<=len(a|b)<=6
assert len(cases['evenmultiple'][0]&cases['evenmultiple'][1])==1
assert len(cases['evengreater'][0]&cases['evengreater'][1])==2
assert len(cases['evenodd'][0]&cases['evenodd'][1])==0
for f in ['event27.css','event27.js','event27-footer.html']:
    assert (F/'assets'/f).exists(),f
s=(F/'assets/event27.js').read_text(encoding='utf-8').lower()
assert not any(x in s for x in ('fetch(','xmlhttprequest','localstorage','sendbeacon','google-analytics','eval('))
p=subprocess.run(['node','--check',str(F/'assets/event27.js')],capture_output=True,text=True)
assert p.returncode==0,p.stderr
print('Topic 2.7 CED, arithmetic, 8 original items, JS, rights and data checks passed.')
