"""Topic 1.10: objective mapping, original practice, source and interaction invariants."""
from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parents[3]
topic=root/'Unit 1/Topic 1.10'
content=(topic/'topic-1-10.qmd').read_text()
obj=json.loads((topic/'objectives.json').read_text())
bank=json.loads((root/'Problem Bank/original/unit-1/topic-1-10.json').read_text())
assert content.startswith('# Topic 1.10 The Investigative Question Revisited and Data Collection')
assert obj['learning_objectives']==['1.10.A','1.10.B','1.10.C','1.10.D','1.10.E']
expected={'1.10.A.1','1.10.A.2','1.10.A.2.i','1.10.A.2.ii','1.10.A.3','1.10.B.1','1.10.C.1','1.10.C.2','1.10.C.3','1.10.C.4','1.10.D.1','1.10.D.2','1.10.D.3','1.10.D.4','1.10.D.5','1.10.E.1','1.10.E.2','1.10.E.3','1.10.E.4'}
assert set(obj['essential_knowledge'])==expected
assert set(v for entry in obj['coverage'] for v in entry['ids'])==expected
assert all(entry['section'] in content for entry in obj['coverage'])
assert 'data-study110-builder' in content and 'data-study110-lab' in content
assert '## Practice {#practice-110}' in content
assert 'data-original-practice="1.10"' in content
assert 'ap24-frq-statistics.pdf#page=7' in content and 'ap24-frq-statistics.pdf#page=8' in content
assert '$$' in content and 'H_a' in content
assert '\\(' not in content, 'Use Quarto inline dollar math, not raw TeX delimiters'
assert content.index('<details class="study110-disclosure study110-sources">')>content.index('## Practice')
assert len(bank['items'])==10 and len({q['id'] for q in bank['items']})==10
assert {q['type'] for q in bank['items']}=={'mc','written'}
assert sum(q['type']=='written' for q in bank['items'])>=3
assert all(q['primary_topic']=='1.10' and q['rights']=='original' and q['hint'] and q['solution'] for q in bank['items'])
assert all(set(q['objectives'])<=set(obj['learning_objectives']) for q in bank['items'])
for q in bank['items']:
 if q['type']=='mc':
  assert len(q['options'])==4 and q['answer'] in 'ABCD'
 else:assert q['rubric']
assert [q['answer'] for q in bank['items'] if q['type']=='mc']==['B','A','C','B','A','D','B']
assert 'Random selection' in content and 'Random assignment' in content
for word in ['survey','prospective','retrospective','census','confounding','ethical','factor','levels','response']:
 assert word.lower() in content.lower(),word
subprocess.run(['node','--check',str(topic/'assets/study110.js')],check=True)
print('Topic 1.10: full Fall 2026 objective coverage, 10 original exercises, controls, study classifications and sourced exam checked.')
