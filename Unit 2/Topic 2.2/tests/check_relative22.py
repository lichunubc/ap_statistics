"""Validate Topic 2.2 source, café arithmetic, learning objectives, and original practice."""
from pathlib import Path
import csv,json,subprocess
ROOT=Path(__file__).resolve().parents[3]
F=ROOT/'Unit 2/Topic 2.2'
qmd=(F/'topic-2-2.qmd').read_text()
obj=json.loads((F/'objectives.json').read_text())
bank=json.loads((ROOT/'Problem Bank/original/unit-2/topic-2-2.json').read_text())
rows=list(csv.DictReader((ROOT/'Unit 2/Topic 2.1/data/cafe_orders.csv').open()))
assert len(rows)==24
assert sum(x['ordering_channel']=='App' for x in rows)==8
assert sum(x['ordering_channel']=='Counter' for x in rows)==16
assert sum(x['drink_type']=='Tea' for x in rows)==10
assert sum(x['ordering_channel']=='App' and x['drink_type']=='Tea' for x in rows)==2
assert 2/8==.25 and 2/10==.2 and 8/16==.5 and 10/24==5/12
assert qmd.startswith('# Topic 2.2 Summary Statistics for Two Categorical Variables')
assert qmd.count('## Practice')==1 and 'data-original-practice="2.2"' in qmd
assert obj['learning_objectives']==['2.2.A','2.2.B','2.2.C']
assert {t for x in obj['coverage'] for t in x['ids']}>=set(obj['essential_knowledge'])
assert len(bank['items'])==8 and len({x['id'] for x in bank['items']})==8
assert all(x['rights']=='original' and len(x['options'])==4 and x['answer'] in 'ABCD' and x['solution'] for x in bank['items'])
assert subprocess.run(['node','--check',str(F/'assets/relative22.js')],capture_output=True).returncode==0
assert not any(x in (F/'assets/relative22.js').read_text().lower() for x in ('fetch(', 'localstorage', 'xmlhttprequest', 'sendbeacon'))
print('Topic 2.2 source, math, practice and objective checks passed.')
