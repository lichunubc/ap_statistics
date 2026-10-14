"""Check Topic 1.8 against official objective map, bank and independent arithmetic."""
from pathlib import Path
import json,statistics,subprocess,math
ROOT=Path(__file__).resolve().parents[3]
topic=ROOT/'Unit 1/Topic 1.8'
main=(topic/'topic-1-8.qmd').read_text()
parts=['_fundamentals.qmd','_construction.qmd','_lab.qmd','_interpretation.qmd','_shape.qmd','_skew.qmd','_exam_practice.qmd']
for p in parts:assert (topic/p).is_file(),p
text='\n'.join((topic/p).read_text() for p in parts)
obj=json.loads((topic/'objectives.json').read_text())
bank=json.loads((ROOT/'Problem Bank/original/unit-1/topic-1-8.json').read_text())
assert main.startswith('# Topic 1.8 Graphical Representations of Summary Statistics for One Quantitative Variable')
assert obj['learning_objectives']==['1.8.A','1.8.B']
assert obj['essential_knowledge']==['1.8.A.1','1.8.A.2','1.8.B.1']
covered={x for c in obj['coverage'] for x in c['ids']}
assert covered==set(obj['essential_knowledge'])
assert text.count('<details')>=4
assert '2019 AP Statistics FRQ' in text
assert 'ap19-frq-statistics.pdf' in text
assert bank['topic']=='1.8' and len(bank['items'])==9
assert len({q['id'] for q in bank['items']})==9
assert {q['type'] for q in bank['items']}=={'mc','number','written'}
assert all(q['rights']=='original' and q['objectives'] and q['solution'] for q in bank['items'])
a=[5,8,10,12,12,14,15,16,18]
assert sum(a)==110 and statistics.median(a)==12
assert statistics.median(a[:4])==9 and statistics.median(a[5:])==15.5
assert statistics.mean(a)==110/9
o=a[:-1]+[50]
assert statistics.mean(o)==142/9 and max(o[:-1])==16
assert (15.5-9)==6.5 and 15.5+1.5*6.5==25.25
assert math.isclose(285/9,31.66666666,abs_tol=1e-7)
assert 292-174==118 and 174-1.5*118==-3 and 292+1.5*118==469
k=ROOT/'Unit 1/Topic 1.8/assets/box18-math.js'
s=ROOT/'Unit 1/Topic 1.8/assets/box18.js'
assert k.exists() and s.exists()
js='const fs=require("fs"),vm=require("vm");let ctx={};vm.createContext(ctx);vm.runInContext(fs.readFileSync(process.argv[1],"utf8"),ctx);let x=ctx.computeBoxplot([5,8,10,12,12,14,15,16,50]);if(x.m!==12||x.q1!==9||x.q3!==15.5||x.good.at(-1)!==16||x.high!==25.25)throw Error(JSON.stringify(x));'
subprocess.run(['node','-e',js,str(k)],check=True)
print('Topic 1.8 objective coverage, nine original questions and independent arithmetic verified.')
