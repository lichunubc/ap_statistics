"""Verify Topic 1.7 content and arithmetic before browser checks."""
from pathlib import Path
import json,math,statistics
ROOT=Path(__file__).resolve().parents[3]
topic=ROOT/'Unit 1/Topic 1.7'
chapter=(topic/'topic-1-7.qmd').read_text()+'\n'+(topic/'_exam-question.qmd').read_text()
objectives=json.loads((topic/'objectives.json').read_text())
bank=json.loads((ROOT/'Problem Bank/original/unit-1/topic-1-7.json').read_text())
assert chapter.startswith('# Topic 1.7 Summary Statistics for One Quantitative Variable')
assert len(objectives['learning_objectives'])==6
assert len(objectives['essential_knowledge'])==17
covered={x for item in objectives['coverage'] for x in item['ids']}
assert set(objectives['essential_knowledge'])<=covered
assert chapter.count('<details')>=9
assert 'ap24-frq-statistics.pdf' in chapter and 'ap24-sg-statistics.pdf' in chapter
assert bank['topic']=='1.7' and len(bank['items'])==10
assert len({q['id'] for q in bank['items']})==10
assert {q['type'] for q in bank['items']}=={'mc','number','written'}
assert all(q['rights']=='original' and q['objectives'] and q['solution'] for q in bank['items'])
a=[5,8,10,12,12,14,15,16,18]
assert sum(a)==110 and math.isclose(statistics.mean(a),110/9)
assert statistics.median(a)==12
assert math.isclose(statistics.variance(a),16.694444444444443)
assert math.isclose(statistics.stdev(a),4.0858835573770875)
assert statistics.median([5,8,10,12])==9
assert statistics.median([14,15,16,18])==15.5
assert statistics.mean(a[:-1]+[50])==142/9
assert statistics.median(a[:-1]+[50])==12
assert statistics.variance([2,4,6])==4
o=[4,5,7,7,9,11,30]
assert 30>11+1.5*(11-5)
assert math.isclose(statistics.mean(o)+2*statistics.stdev(o),28.31179,abs_tol=.001)
assert math.isclose(statistics.stdev([10,12,14,14,15,16,17]),2.3804761428,abs_tol=1e-6)
assert math.isclose(statistics.stdev([6,11,14,14,15,19,24]),5.7071383873,abs_tol=1e-6)
print('Topic 1.7 coverage, original question schema and independent arithmetic passed.')
