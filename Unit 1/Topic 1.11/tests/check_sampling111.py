"""Topic 1.11 source, coverage, numerical and sampling-method invariants."""
from pathlib import Path
from math import comb
import json,subprocess
root=Path(__file__).resolve().parents[3]
topic=root/'Unit 1/Topic 1.11'
qmd=(topic/'topic-1-11.qmd').read_text(encoding='utf-8')
obj=json.loads((topic/'objectives.json').read_text())
bank=json.loads((root/'Problem Bank/original/unit-1/topic-1-11.json').read_text())
pop=json.loads((topic/'data/population.json').read_text())['students']
assert qmd.startswith('# Topic 1.11 Random Sampling')
assert obj['ced_printed_pages']==[48,49]
assert obj['learning_objectives']==['1.11.A','1.11.B']
required={f'1.11.A.{i}' for i in range(1,7)}|{'1.11.B.1'}
assert set(obj['essential_knowledge'])==required
assert {x for c in obj['coverage'] for x in c['ids']}==required
assert all(c['section'] in qmd for c in obj['coverage'])
assert len(pop)==36 and len({u['id'] for u in pop})==36
assert sorted(x['id'] for x in pop)==list(range(1,37))
assert sum(x['commute_minutes'] for x in pop)==612
assert sum(x['commute_minutes'] for x in pop)/len(pop)==17
assert {grade:sum(x['grade']==grade for x in pop) for grade in 'ABC'}=={'A':12,'B':12,'C':12}
assert {group:sum(x['advisory']==group for x in pop) for group in range(1,7)}==dict.fromkeys(range(1,7),6)
for group in range(1,7):
 for grade in 'ABC':assert sum(x['advisory']==group and x['grade']==grade for x in pop)==2
assert comb(6,2)==15
s=[pop[i-1] for i in [4,10,16,22,28,34]]
assert {u['grade'] for u in s}=={'A'} and sum(u['commute_minutes'] for u in s)/6==12
# Exhaustively verify the design's periodicity counterexample.
systematic_means=[]
for start in range(1,7):
 selected=[pop[i-1] for i in range(start,37,6)]
 assert len(selected)==6 and len({x['grade'] for x in selected})==1
 systematic_means.append(sum(u['commute_minutes'] for u in selected)/len(selected))
assert systematic_means==[10,16,22,12,18,24], systematic_means
assert sum(systematic_means)/6==17, 'Fair random start is unbiased despite periodicity'
assert max(systematic_means)-min(systematic_means)==14
assert '| 1 | A | 10 |' in qmd and '| 6 | C | 24 |' in qmd
assert 'E(\\bar{X})' in qmd and r'\mu=17' in qmd
# Cross-language fixture for the sampler's deterministic 32-bit LCG.
state=1; replacement=[]
for _ in range(6):
 state=(1664525*state+1013904223)%(2**32)
 replacement.append(1+(state*36)//(2**32))
assert replacement==[9,14,19,26,2,14]
assert len(set(replacement))==5
assert '×${n} draws' in (topic/'assets/sampling111.js').read_text()
assert 'sampling111-multiplicity' in (topic/'assets/sampling111.css').read_text()
assert "visible===planned.length?'Sample mean':'Mean of selections revealed so far'" in (topic/'assets/sampling111.js').read_text(), 'Incomplete draws must not be presented as a finished sample mean'
assert 'planned=[];visible=0;paint();status.textContent' in (topic/'assets/sampling111.js').read_text(), 'Invalid seed must clear stale highlights'
assert "seedInput.addEventListener('input',plan)" in (topic/'assets/sampling111.js').read_text(), 'Seed edits must immediately invalidate stale sample state'
assert 'class="sampling111-grid" role="list"' in qmd
assert len(bank['items'])==10 and len({x['id'] for x in bank['items']})==10
assert {x['type'] for x in bank['items']}=={'mc','number','written'}
assert sum(x['type']=='written' for x in bank['items'])>=3
assert all(set(q['objectives'])<=set(obj['learning_objectives']) for q in bank['items'])
for q in bank['items']:
 assert q['rights']=='original' and q['hint'] and q['solution']
 assert not any(x in q['solution'] for x in ['\x08','\x0c','\x0b'])
 if q['type']=='mc':assert len(q['options'])==4 and q['answer'] in 'ABCD'
 if q['type']=='written':assert q['rubric']
 if q['type']=='number':assert q['tolerance']>=0
assert [x['answer'] for x in bank['items'] if x['type']=='mc']==['B','C','D','A']
assert '## Practice {#practice-111}' in qmd
assert qmd.count('original-practice-host')==1
assert 'one question at a time' not in qmd.lower()
assert '1.11.A.1' not in qmd
assert 'ap25-q2-stem.png' in qmd and 'ap25-q2-parts.png' in qmd
assert qmd.count('class="exam-enlarge"')==2 and 'lesson-sources sampling111-sources' in qmd
assert 'data-sampling111' in qmd
subprocess.run(['node','--check',str(topic/'assets/sampling111.js')],check=True)
print('Topic 1.11 arithmetic, population/strata/cluster, objective and practice checks passed.')
