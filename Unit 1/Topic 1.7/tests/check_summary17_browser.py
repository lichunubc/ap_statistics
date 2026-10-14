"""Browser QA for Topic 1.7's linked diagram and compact original practice."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import os,threading,math,json
ROOT=Path(__file__).resolve().parents[3]
DOCS=ROOT/'docs'
QA=ROOT/'qa';QA.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(DOCS)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base='http://127.0.0.1:'+str(server.server_port)+'/'
errors=[]
try:
    with sync_playwright() as p:
        kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
        for width in (1440,768,390):
            context=browser.new_context(viewport={'width':width,'height':980})
            page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(base+quote('Unit 1/Topic 1.7/topic-1-7.html',safe='/'),wait_until='networkidle')
            assert page.locator('h1').inner_text()=='Topic 1.7 Summary Statistics for One Quantitative Variable'
            page.wait_for_function('window.SUMMARY17_TEST!==undefined')
            w=page.locator('[data-summary17]')
            assert math.isclose(float(w.get_attribute('data-mean')),110/9)
            assert w.locator('svg circle').count()==9
            w.locator('[data-summary17-action=extreme]').click()
            assert math.isclose(float(w.get_attribute('data-mean')),142/9)
            assert float(w.get_attribute('data-median'))==12
            w.locator('[data-summary17-action=seconds]').click()
            assert math.isclose(float(w.get_attribute('data-mean')),142/9*60)
            w.locator('[data-summary17-action=reset]').click()
            assert math.isclose(float(w.get_attribute('data-mean')),110/9)
            w.locator('textarea').fill('1, nope, 3')
            w.locator('[data-summary17-action=apply]').click()
            assert 'valid' in w.locator('[data-summary17-feedback]').inner_text()
            w.locator('[data-summary17-action=reset]').click()
            details=page.locator('main details.math-note')
            assert details.count()>=9 and details.first.get_attribute('open') is None
            details.first.locator('summary').click()
            assert details.first.get_attribute('open') is not None
            host=page.locator('.original-practice')
            host.locator('.original-question-title').wait_for()
            assert host.locator('.original-question-title').inner_text()=='Question 1 of 10'
            host.locator('input[type=number]').fill('12.22')
            host.locator('[data-action=check]').click()
            assert 'Correct' in host.locator('.original-feedback').inner_text()
            host.locator('[data-action=solution]').click()
            assert host.locator('.original-solution').is_visible()
            host.locator('[data-action=next]').click()
            assert host.locator('.original-question-title').inner_text()=='Question 2 of 10'
            assert host.locator('.original-solution').is_hidden()
            host.locator('[data-action=previous]').click()
            assert host.locator('input[type=number]').input_value()==''
            page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
            assert host.locator('.original-print-question').count()==10
            page.evaluate("window.dispatchEvent(new Event('afterprint'))")
            assert host.locator('.original-print-question').count()==0
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
            if width==390:page.screenshot(path=str(QA/'topic-1-7-mobile.png'),full_page=True)
            context.close()
        nojs=browser.new_context(java_script_enabled=False)
        p0=nojs.new_page();p0.goto(base+quote('Unit 1/Topic 1.7/topic-1-7.html',safe='/'))
        assert p0.locator('.original-nojs li').count()==10
        nojs.close();browser.close()
finally:server.shutdown()
assert not errors,errors
(QA/'topic-1-7-browser.json').write_text(json.dumps({'widths':[1440,768,390],'practice':10,'no_js':True,'errors':errors},indent=2))
print('Topic 1.7 responsive, keyboard-native controls, reset, practice, print and no-JS passed.')
