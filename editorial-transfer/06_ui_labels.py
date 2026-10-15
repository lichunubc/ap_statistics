from pathlib import Path
import os,json,hashlib
R=Path(os.environ['SOURCE_ROOT'])
changes={
'Unit 1/Topic 1.1/assets/foundations.js':{'Each mark is one hypothetical student.':'Each mark is one student.'},
'Unit 1/Topic 1.2/assets/variables.js':{' Nothing is submitted.':''},
'Unit 1/Topic 1.3/assets/categorical-tables.js':{'A simulated order from the fixed hypothetical total of 40 responses. ':'','Percentages while building use the number tallied so far; at completion, the denominator is 40.':'As you tally, each percentage uses the number of responses counted so far. The completed table uses all 40 responses.'},
'Unit 1/Topic 1.9/assets/compare19.js':{'Two hypothetical route distributions, common numerical scale':'Two route distributions, common numerical scale'},
'Unit 1/Shared/assets/site.js':{' · hypothetical illustration':'',' · hypothetical':'',' This practice check is not submitted to a teacher.':''},
'Problem Bank/assets/practice.js':{'Class file restored for this tab. Responses are not submitted or carried between pages.':'Class file restored. Choose a question to begin.'}}
for name,replacements in changes.items():
 p=R/name;s=p.read_text()
 for a,b in replacements.items():s=s.replace(a,b)
 p.write_text(s)
p=R/'Unit 1/Shared/tests/preserved-assets.json';data=json.loads(p.read_text())
for item in data:
 actual=hashlib.sha256((R/item['path']).read_bytes()).hexdigest()
 if actual!=item['sha256']:
  assert item['path'] in changes,item['path']
  item['prior_sha256']=item.get('prior_sha256',item['sha256']);item['sha256']=actual
  item['change_note']='2026-10-15: user-requested visible wording cleanup only; calculations, data and interactions unchanged.'
p.write_text(json.dumps(data,indent=2)+'\n')
