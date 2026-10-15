"""Topic 1.9 official coverage, independent statistical arithmetic, original rights and deterministic JS checks."""
from pathlib import Path
import json,math,statistics,subprocess
ROOT=Path(__file__).resolve().parents[3]
TOP=ROOT/'Unit 1/Topic 1.9'
chapter=(TOP/'topic-1-9.qmd').read_text()
parts=['_comparison.qmd','_laboratory.qmd','_standardization.qmd','_exam-and-practice.qmd']
for part in parts:assert (TOP/part).exists(),part
lessons='\n'.join((TOP/p).read_text() for p in parts)
objectives=json.loads((TOP/'objectives.json').read_text())
data=json.loads((TOP/'data/route-scenarios.json').read_text())
bank=json.loads((ROOT/'Problem Bank/original/unit-1/topic-1-9.json').read_text())
assert chapter.startswith('# Topic 1.9 Comparisons of the Distributions for One Quantitative Variable')
assert objectives['learning_objectives']==['1.9.A','1.9.B','1.9.C','1.9.D','1.9.E']
assert objectives['essential_knowledge']==['1.9.A.1','1.9.B.1','1.9.C.1','1.9.D.1','1.9.D.2','1.9.E.1']
covered={v for entry in objectives['coverage'] for v in entry['ids']}
assert covered==set(objectives['essential_knowledge'])
assert all(entry['section'] in lessons for entry in objectives['coverage'])
assert lessons.count('<details class="math-note">')>=5
for word in ['Optional enrichment','normal','2026','ap26-frq-statistics.pdf','ap26-sg-statistics.pdf','data-z19','data-compare19']:
    assert word in lessons,word
assert 'original-practice-host data-original-practice="1.9"' in lessons
assert bank['topic']=='1.9' and len(bank['items'])==10
assert len({q['id'] for q in bank['items']})==10
assert {q['type'] for q in bank['items']}=={'mc','number','written'}
assert all(q['rights']=='original' and q['solution'] and q['hint'] and q['objectives'] and q['primary_topic']=='1.9' for q in bank['items'])
assert all(q['id'].startswith('MHS-U1-T19-') for q in bank['items'])
assert all(set(q['objectives'])<=set(objectives['learning_objectives']) for q in bank['items'])
assert all(q['tolerance']>=0 for q in bank['items'] if q['type']=='number')
a,b=data['route_a'],data['route_b']
assert len(a)==len(b)==12
assert sum(a)==198 and sum(b)==187
assert statistics.mean(a)==16.5 and statistics.median(a)==16.5
assert statistics.mean(b)==187/12 and statistics.median(b)==13.5
assert statistics.median(a[:6])==15 and statistics.median(a[6:])==18
assert statistics.median(b[:6])==11.5 and statistics.median(b[6:])==16.5
assert math.isclose(statistics.stdev(a),2.393172105652397,abs_tol=1e-12)
assert math.isclose(statistics.stdev(b),7.63316130545867,abs_tol=1e-12)
assert 16.5+1.5*(16.5-11.5)==24
assert 38>24 and 19<24
assert (86-70)/8==2 and (90-80)/10==1 and (73-85)/6==-2
assert 60+(-1.5)*4==54
assert data['alternate_scenarios']['shifted_b']==[x+5 for x in a]
assert data['licensing']=='original'
engine=TOP/'assets/compare19-math.js'
ui=TOP/'assets/compare19.js'
for js in [engine,ui]:subprocess.run(['node','--check',str(js)],check=True)
node_test=r"""
const fs=require('fs'),vm=require('vm');
const root={};vm.createContext(root);vm.runInContext(fs.readFileSync(process.argv[1],'utf8'),root);
const E=root.COMPARE19_MATH;
const JSONDATA=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const fail=m=>{throw new Error(m)};
if(JSON.stringify(E.scenarios.original.a)!==JSON.stringify(JSONDATA.route_a))fail('Route A disagreement');
if(JSON.stringify(E.scenarios.original.b)!==JSON.stringify(JSONDATA.route_b))fail('Route B disagreement');
for(const [key,other] of Object.entries(JSONDATA.alternate_scenarios)){
 if(JSON.stringify(E.scenarios[key.replace(/_b$/,'')].b)!==JSON.stringify(other))fail('Scenario mismatch '+key);
}
let a=E.summary(E.scenarios.original.a),b=E.summary(E.scenarios.original.b);
if(a.mean!==16.5||a.median!==16.5||a.iqr!==3||Math.abs(a.sd-2.39317210565)>1e-9)fail('A mismatch');
if(b.median!==13.5||b.iqr!==5||b.high!==24||b.outliers.length!==1||b.rightWhisker!==19)fail('B outliers mismatch');
if(E.zScore(86,70,8)!==2||E.zScore(90,80,10)!==1||E.zScore(73,85,6)!==-2)fail('z mismatch');
for(const bad of [0,-1]){let error=false;try{E.zScore(1,2,bad);}catch(e){error=true};if(!error)fail('Accepted invalid sd');}
if(E.frequencies(E.scenarios.original.a).reduce((u,v)=>u+v,0)!==12)fail('Histogram total');
if(E.frequencies(E.scenarios.original.b).reduce((u,v)=>u+v,0)!==12)fail('Histogram total');
let shifted=E.summary(E.scenarios.shifted.b);
if(Math.abs(shifted.sd-a.sd)>1e-9||Math.abs(shifted.iqr-a.iqr)>1e-9||shifted.mean-a.mean!==5)fail('Shift invariant');
if(!(E.summary(E.scenarios.replaced.b).sd<b.sd))fail('Replacing extreme must reduce SD');
"""
subprocess.run(['node','-e',node_test,str(engine),str(TOP/'data/route-scenarios.json')],check=True)
print('Topic 1.9: objective coverage, 10 original questions, all hypothetical datasets, statistics, source and JS mathematics verified.')
