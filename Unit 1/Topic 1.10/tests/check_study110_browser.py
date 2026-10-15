"""Browser/MathML/responsive/quiz checks for Topic 1.10."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import threading,os,json
ROOT=Path(__file__).resolve().parents[3];DOCS=ROOT/'docs';QA=ROOT/'qa';QA.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(DOCS)))
threading.Thread(target=srv.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{srv.server_port}/'
url=base+quote('Unit 1/Topic 1.10/topic-1-10.html',safe='/')
errors=[];bad=[]
try:
 with sync_playwright() as p:
  kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
  b=p.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
  for width in [1440,768,390]:
   ctx=b.new_context(viewport={'width':width,'height':950},reduced_motion='reduce')
   page=ctx.new_page()
   page.on('pageerror',lambda error:errors.append(str(error)))
   page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 and r.url.startswith(base) else None)
   response=page.goto(url,wait_until='domcontentloaded',timeout=30000)
   assert response and response.ok
   assert page.locator('h1').inner_text().startswith('Topic 1.10')
   assert page.locator('main math').count()>=2,'Quarto must render real MathML'
   assert page.locator('main .study110-disclosure').count()>=3
   builder=page.locator('[data-study110-builder]')
   builder.locator('[data-study110-goal]').select_option('association')
   assert 'associated' in builder.locator('[data-study110-question]').inner_text()
   builder.locator('[data-study110-outcome]').select_option('sleep')
   assert 'sleep' in builder.locator('[data-study110-question]').inner_text()
   builder.locator('[data-study110-builder-reset]').click()
   assert builder.locator('[data-study110-goal]').input_value()=='estimate'
   lab=page.locator('[data-study110-lab]')
   lab.locator('[data-study110-selection]').select_option('random')
   assert 'sampled school population' in lab.locator('[data-study110-generalize]').inner_text()
   lab.locator('[data-study110-type]').select_option('impose')
   assert not lab.locator('[data-study110-assignment]').is_disabled()
   assert 'causal comparison' in lab.locator('[data-study110-cause]').inner_text()
   lab.locator('[data-study110-assignment]').select_option('deliberate')
   assert 'pre-existing' in lab.locator('[data-study110-cause]').inner_text()
   lab.locator('[data-study110-lab-reset]').click()
   assert lab.locator('[data-study110-assignment]').is_disabled()
   assert 'does not establish causation' in lab.locator('[data-study110-cause]').inner_text()
   host=page.locator('.original-practice');host.locator('.original-question-title').wait_for(timeout=15000)
   assert host.locator('.original-question-title').inner_text()=='Question 1 of 10'
   assert host.locator('input:checked').count()==0
   host.locator('[data-action=next]').click()
   assert host.locator('.original-question-title').inner_text()=='Question 2 of 10'
   host.locator('[data-action=previous]').click()
   assert host.locator('.original-question-title').inner_text()=='Question 1 of 10'
   host.locator('[data-action=check]').click()
   assert 'Choose an answer' in host.locator('.original-feedback').inner_text()
   host.locator('input[value=B]').check();host.locator('[data-action=check]').click()
   assert 'Correct' in host.locator('.original-feedback').inner_text()
   host.locator('[data-action=hint]').click();assert host.locator('.original-hint').is_visible()
   host.locator('[data-action=solution]').click();assert host.locator('.original-solution').is_visible()
   host.locator('[data-action=reset]').click() if host.locator('[data-action=reset]').count() else None
   page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
   assert host.locator('.original-print-question').count()==10
   page.evaluate('window.dispatchEvent(new Event("afterprint"))')
   assert host.locator('.original-print-question').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),f'overflow {width}'
   if width==390:page.screenshot(path=str(QA/'topic-1-10-mobile.png'),full_page=True)
   ctx.close()
  nojs=b.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
  page=nojs.new_page();page.goto(url,wait_until='domcontentloaded')
  assert page.locator('.original-nojs li').count()==10
  assert 'Part (a)' in page.locator('main').inner_text()
  nojs.close();b.close()
finally:srv.shutdown()
assert not errors,errors
assert not bad,bad
(QA/'topic-1-10-browser.json').write_text(json.dumps({'tested_widths':[1440,768,390],'questions':10,'mathml':True,'no_js':True,'errors':errors,'bad_local_requests':bad},indent=2))
print('Topic 1.10 native HTTP, interactions, MathML, practice, no-JS, print and responsive checks passed.')
