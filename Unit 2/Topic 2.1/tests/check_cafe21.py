"""Validate Topic 2.1 original material and the exact 24 café orders."""
from pathlib import Path
import csv,json,subprocess
root=Path(__file__).resolve().parents[3]
t=root/'Unit 2/Topic 2.1'
qmd=(t/'topic-2-1.qmd').read_text()
obj=json.loads((t/'objectives.json').read_text())
bank=json.loads((root/'Problem Bank/original/unit-2/topic-2-1.json').read_text())
rows=list(csv.DictReader((t/'data/cafe_orders.csv').open()))
assert len(rows)==24 and [int(r['order_id']) for r in rows]==list(range(1,25))
c={(channel,drink):sum(r['ordering_channel']==channel and r['drink_type']==drink for r in rows) for channel in ('App','Counter') for drink in ('Coffee','Tea','Smoothie')}
assert c=={('App','Coffee'):4,('App','Tea'):2,('App','Smoothie'):2,('Counter','Coffee'):4,('Counter','Tea'):8,('Counter','Smoothie'):4}
assert qmd.startswith('# Topic 2.1 Tabular and Graphical') and qmd.count('## Practice')==1
assert 'data-original-practice="2.1"' in qmd
assert obj['learning_objectives']==['2.1.A','2.1.B']
assert {e for x in obj['coverage'] for e in x['ids']}>=set(obj['essential_knowledge'])
assert len(bank['items'])==8 and len(set(x['id'] for x in bank['items']))==8
assert all(x['rights']=='original' and x['answer'] in 'ABCD' and len(x['options'])==4 and x['solution'] for x in bank['items'])
assert all((t/'assets'/p).exists() for p in ('cafe21.js','cafe21.css','cafe21-footer.html'))
r=subprocess.run(['node','--check',str(t/'assets/cafe21.js')],capture_output=True,text=True)
assert r.returncode==0,r.stderr
js=(t/'assets/cafe21.js').read_text().lower()
assert all(s not in js for s in ('fetch(','xmlhttprequest','localstorage','sendbeacon'))
assert (8/24)*(2/8)==2/24 and 4/8==.5 and 4/16==.25
print('Topic 2.1: data, curriculum, practice, privacy, arithmetic and JS syntax passed.')
