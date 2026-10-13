"""Verify the deployed revision, five unit pages, six topics, legacy URLs and data."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import quote,unquote,urlsplit
import os,json,time,urllib.request
base=os.environ.get('SITE_URL','').rstrip('/')
assert base=='https://lichunubc.github.io/ap_statistics',base
expected=os.environ.get('GITHUB_SHA','')
def fetch(path,marker=None):
    url=base+'/'+quote(path,safe='/%')+'?release='+expected
    last=None
    for attempt in range(12):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'MapleHillCourse-DeploymentCheck'}),timeout=20) as response:
                text=response.read().decode('utf-8');assert response.status==200
                if marker:assert marker in text, f'Missing marker: {marker}'
                return text
        except Exception as e:
            last=e
            if attempt<11:time.sleep(5)
    raise RuntimeError(f'Public verification failed: {url}: {last}')
release=json.loads(fetch('release.json'))
assert release['source_commit']==expected,(release,expected)
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'project/topic-status.json').read_text())
units=json.loads((root/'project/unit-status.json').read_text())['units']
checked=[]
for topic in manifest['topics']:
    path=topic['chapter'].replace('.qmd','.html')
    fetch(path,'Topic '+topic['id']+' '+topic['title']);checked.append(path)
for name,entry in json.loads((root/'Unit 1/legacy-pages.json').read_text()).items():
    fetch(name,'<h1');checked.append(name)
text=fetch('topic-1-2.html','data-variables="classify"')
assert 'data-variables="summary"' in text and 'data-variables="recode"' in text
assert text.count('<details>')>=10
home=fetch('index.html','Choose a unit')
assert home.count('data-unit-status="under-construction"')==4
assert 'unit-grid' in home and 'topic-grid' not in home
for unit in units:
    path=unit['landing'].replace('.qmd','.html')
    text=fetch(path,f"Unit {unit['id']}: {unit['title']}")
    if unit['id']==1:
        assert 'topic-grid' in text and 'data-chart="commute-dot"' in text
    else:
        assert 'Under construction' in text and 'construction-note' in text
    checked.append(path)
checked.append('index.html')
fetch('site/assets/navigation.js','courseNavigationReady')
fetch('site/assets/navigation.css','course-topic-list[hidden]')
fetch('Unit 1/Topic 1.2/assets/variables.js','window.VARIABLES_TEST')
shared=json.loads(fetch('Unit 1/Shared/data/foundations.json'))
assert shared['school_a']['counts']==[8,6,18,8]
fetch('Unit 1/Topic 1.2/data/illustrative-records.csv','A,Bus,24.0')
report={'site':base,'source_commit':expected,'pages_checked':checked,'unit_landing_pages':5,'under_construction_units':[2,3,4,5],'new_activity_markers':3,'dataset_verified':True}
(root/'qa').mkdir(exist_ok=True);(root/'qa/live-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
