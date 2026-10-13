"""Topic 1.2 source, arithmetic, accessibility and browser regression checks."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
import json, os, subprocess, sys, threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'_quarto.yml').exists())
sys.path.insert(0,str(ROOT/'tools'))
from browser_support import load_page
DOCS=ROOT/'docs';QA=ROOT/'qa';QA.mkdir(exist_ok=True)
source=ROOT/'Unit 1/Topic 1.2'
data=json.loads((ROOT/'Unit 1/Shared/data/foundations.json').read_text())
school=data['school_a'];assert school['counts']==[8,6,18,8]
assert sum(school['counts'])==40 and school['counts'][2]/40==.45
assert school['commute_total_minutes']/40==24
assert len([i/2 for i in range(21)])==21
assert sum(n*c for n,c in zip(school['counts'],[1,2,3,4]))/40==2.65
assert sum(n*c for n,c in zip(school['counts'],[4,1,9,2]))/40==5.4
assert sum(n*c for n,c in zip(school['counts'],[0,0,1,0]))/40==.45
node="""const assert=require('node:assert/strict');const t=require(process.argv[1]);
const counts=[8,6,18,8];assert.equal(t.codedMean(counts,[1,2,3,4]),2.65);
assert.equal(t.codedMean(counts,[4,1,9,2]),5.4);assert.equal(t.codedMean(counts,[0,0,1,0]),.45);
assert.throws(()=>t.codedMean([],[]));assert.throws(()=>t.codedMean([0],[1]));
assert.throws(()=>t.codedMean([-1],[2]));assert.throws(()=>t.codedMean([1],[NaN]));
assert.deepEqual(t.classify.map(x=>x.answer),[0,1,2,0,1,0,2,1,0,2]);
assert.deepEqual(t.summary.map(x=>x.answer),[0,1,2,1]);console.log('Node arithmetic and answer keys passed.');"""
subprocess.run(['node','-e',node,str(source/'assets/variables.js')],check=True)
obj=json.loads((source/'objectives.json').read_text())
assert obj['title']=='Variables' and obj['learning_objectives']==['1.2.A','1.2.B','1.2.C']
assert obj['ced_printed_pages']=='32–33'
canonical='Unit 1/Topic 1.2/topic-1-2.html'
for name in [canonical,'topic-1-2.html']:
    soup=BeautifulSoup((DOCS/name).read_text(),'html.parser')
    assert soup.h1.get_text(' ',strip=True)=='Topic 1.2 Variables'
    assert len(soup.select('.solution details'))==10
    assert len(soup.select('math'))>10
    assert len(soup.select('[data-variables]'))==3
    assert 'not a raw-data extract' in soup.get_text(' ',strip=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(DOCS)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
errors=[]
with sync_playwright() as p:
    kwargs={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kwargs)
    for width in [1440,768,390,360]:
        page=browser.new_page(viewport={'width':width,'height':1000})
        page.on('pageerror',lambda e:errors.append(str(e)))
        load_page(page,DOCS/canonical,base+quote(canonical,safe='/'))
        page.wait_for_function('window.VARIABLES_TEST !== undefined')
        assert page.locator('input:checked').count()==0
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),width
        if width in [1440,390]:page.screenshot(path=str(QA/f'variables-opening-{width}.png'))
        for kind,answers in [('classify',[0,1,2,0,1,0,2,1,0,2]),('summary',[0,1,2,1])]:
            quiz=page.locator(f'[data-variables={kind}]')
            quiz.locator('[data-check]').click()
            assert 'Select one classification' in quiz.inner_text()
            assert quiz.get_attribute('data-correct')==''
            for i,answer in enumerate(answers):
                assert quiz.get_attribute('data-case')==str(i)
                assert quiz.locator('input:checked').count()==0
                quiz.locator(f'input[value="{(answer+1)%3}"]').check()
                quiz.locator('[data-check]').click()
                assert quiz.get_attribute('data-correct')=='false'
                assert 'Not quite.' in quiz.locator('.status').inner_text()
                quiz.locator('[data-clear]').click()
                assert quiz.locator('input:checked').count()==0
                quiz.locator(f'input[value="{answer}"]').focus();page.keyboard.press('Space')
                quiz.locator('[data-check]').focus();page.keyboard.press('Enter')
                assert quiz.get_attribute('data-correct')=='true'
                assert 'Correct.' in quiz.locator('.status').inner_text()
                quiz.locator('[data-next]').click()
                assert quiz.get_attribute('data-correct')==''
                assert quiz.locator('input:checked').count()==0
            assert quiz.get_attribute('data-case')=='0'
            quiz.locator('[data-next]').click();quiz.locator('[data-restart]').click()
            assert quiz.get_attribute('data-case')=='0'
            if width in [1440,390]:quiz.screenshot(path=str(QA/f'variables-{kind}-{width}.png'))
        lab=page.locator('[data-variables=recode]')
        for scheme,mean in [('sequential','2.65'),('alternative','5.4'),('indicator','0.45'),('words','')]:
            lab.locator('select').select_option(scheme)
            assert lab.get_attribute('data-average')==mean
            assert lab.locator('tbody tr').count()==4
            assert '18/40 = 45%' in lab.inner_text()
        lab.locator('select').select_option('alternative');lab.locator('[data-reset]').click()
        assert lab.get_attribute('data-scheme')=='words'
        lab.locator('select').select_option('indicator')
        if width in [1440,390]:lab.screenshot(path=str(QA/f'variables-recoding-{width}.png'))
        details=page.locator('.solution details')
        details.first.locator('summary').click();assert details.first.get_attribute('open') is not None
        page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
        assert page.locator('.variables-print').count()==3
        assert page.locator('.solution details[open]').count()==10
        page.emulate_media(media='print')
        assert page.locator('.variables-print').first.is_visible()
        page.emulate_media(media='screen')
        page.evaluate('window.dispatchEvent(new Event("afterprint"))')
        assert page.locator('.variables-print').count()==0
        assert page.locator('.solution details[open]').count()==1
        assert lab.get_attribute('data-scheme')=='indicator'
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),width
        page.close()
    # The public compatibility address loads independently and starts neutral.
    page=browser.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    load_page(page,DOCS/'topic-1-2.html',base+'topic-1-2.html')
    page.wait_for_function('window.VARIABLES_TEST !== undefined')
    assert page.locator('input:checked').count()==0
    page.close()
    page=browser.new_page(java_script_enabled=False)
    load_page(page,DOCS/canonical,base+quote(canonical,safe='/'))
    assert 'Without JavaScript' in page.locator('[data-variables=classify]').inner_text()
    page.locator('.solution details').first.locator('summary').click()
    assert page.locator('.solution details[open]').count()==1
    browser.close()
server.shutdown()
assert not errors,errors
report={'topic':'1.2 Variables','widths':[1440,768,390,360],'classification_cases':10,'summary_cases':4,'recoding_modes':4,'worked_practice':10,'mode':'offline inlining' if os.environ.get('INLINE_BROWSER') else 'HTTP browser','checks':['arithmetic and Node helpers','unselected/check/wrong/clear/correct/next/restart','native keyboard input','canonical and compatibility page','no-JavaScript fallback','print and restoration','mobile overflow'],'javascript_errors':errors}
(QA/'variables-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
