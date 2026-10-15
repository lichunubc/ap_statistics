"""Full local HTTP browser gate: 1.9 comparisons, z-scores, keyboard/math, bank, no-JS, print and responsive."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import threading,os,json,math
ROOT=Path(__file__).resolve().parents[3]
DOCS=ROOT/'docs';QA=ROOT/'qa';QA.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(DOCS)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
url=base+quote('Unit 1/Topic 1.9/topic-1-9.html',safe='/')
errors=[];responses=[]
try:
 with sync_playwright() as p:
  kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
  browser=p.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
  for width in [1440,768,390]:
   context=browser.new_context(viewport={'width':width,'height':960},reduced_motion='reduce')
   page=context.new_page()
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:responses.append((r.status,r.url)) if r.status>=400 and r.url.startswith(base) else None)
   page.goto(url,wait_until='networkidle')
   assert page.locator('h1').inner_text().startswith('Topic 1.9 Comparisons of the Distributions')
   lab=page.locator('[data-compare19]');lab.locator('svg circle').first.wait_for()
   assert lab.locator('[data-compare19-chart] svg circle').count()==24
   assert abs(float(lab.get_attribute('data-mean-a'))-16.5)<.001
   assert abs(float(lab.get_attribute('data-mean-b'))-187/12)<.001
   assert float(lab.get_attribute('data-median-b'))==13.5
   assert float(lab.get_attribute('data-iqr-b'))==5
   assert float(lab.get_attribute('data-outliers-b'))==1
   lab.locator('[data-compare19-mode]').select_option('box')
   assert lab.get_attribute('data-mode')=='box'
   assert lab.locator('[data-compare19-chart] svg rect').count()==2
   lab.locator('[data-compare19-mode]').select_option('hist')
   assert lab.get_attribute('data-mode')=='hist'
   assert lab.locator('[data-compare19-chart] svg rect').count()>=4
   lab.locator('[data-compare19-scenario]').select_option('replaced')
   assert float(lab.get_attribute('data-outliers-b'))==0
   assert float(lab.get_attribute('data-sd-b'))<7
   lab.locator('[data-compare19-scenario]').select_option('shifted')
   assert abs(float(lab.get_attribute('data-mean-b'))-21.5)<.001
   assert float(lab.get_attribute('data-iqr-b'))==3
   lab.locator('[data-compare19-largest]').fill('50')
   lab.locator('[data-compare19-action="apply"]').click()
   assert 'between 0 and 45' in lab.locator('[data-compare19-message]').inner_text()
   lab.locator('[data-compare19-action="reset"]').click()
   assert lab.get_attribute('data-mode')=='dot'
   assert float(lab.get_attribute('data-outliers-b'))==1
   z=page.locator('[data-z19]');z.locator('svg').wait_for()
   assert float(z.get_attribute('data-z-a'))==2
   assert float(z.get_attribute('data-z-b'))==1
   z.locator('[data-z19-key="sdB"]').fill('5')
   z.locator('[data-z19-action="calculate"]').click()
   assert float(z.get_attribute('data-z-b'))==2
   z.locator('[data-z19-key="sdB"]').fill('0')
   z.locator('[data-z19-action="calculate"]').click()
   assert z.get_attribute('data-valid')=='false'
   assert 'undefined' in z.locator('[data-z19-status]').inner_text()
   z.locator('[data-z19-action="reset"]').click()
   assert z.get_attribute('data-valid')=='true' and float(z.get_attribute('data-z-b'))==1
   notes=page.locator('main details.math-note')
   assert notes.count()>=5
   notes.first.locator('summary').focus();page.keyboard.press('Enter')
   assert notes.first.get_attribute('open') is not None
   assert page.locator('main math').count()>=3,"Expected real MathML, not raw TeX text"
   host=page.locator('.original-practice');host.locator('.original-question-title').wait_for()
   assert host.locator('.original-question-title').inner_text()=='Question 1 of 10'
   assert host.locator('input[type=radio]:checked').count()==0
   host.locator('[data-action=check]').click()
   assert 'Choose an answer' in host.locator('.original-feedback').inner_text()
   host.locator('input[type=radio][value=C]').check()
   host.locator('[data-action=check]').click()
   assert 'Correct' in host.locator('.original-feedback').inner_text()
   host.locator('[data-action=hint]').click();assert host.locator('.original-hint').is_visible()
   host.locator('[data-action=solution]').click();assert host.locator('.original-solution').is_visible()
   host.locator('[data-action=next]').click()
   assert host.locator('.original-question-title').inner_text()=='Question 2 of 10'
   assert host.locator('.original-hint').is_hidden()
   host.locator('[data-action=previous]').click()
   assert host.locator('input[type=radio]:checked').count()==0
   page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
   assert host.locator('.original-print-question').count()==10
   page.evaluate('window.dispatchEvent(new Event("afterprint"))')
   assert host.locator('.original-print-question').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),f'Horizontal page overflow at {width}'
   if width==390:page.screenshot(path=str(QA/'topic-1-9-mobile.png'),full_page=True)
   context.close()
  nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':860})
  page=nojs.new_page();page.goto(url,wait_until='networkidle')
  assert page.locator('.original-nojs li').count()==10
  assert 'Static alternative' in page.locator('main').inner_text()
  nojs.close();browser.close()
finally:server.shutdown()
assert not errors,errors
assert not responses,responses
(QA/'topic-1-9-browser.json').write_text(json.dumps({'widths':[1440,768,390],'practice':10,'mathml':True,'no_js':True,'errors':errors,'failed_requests':responses},indent=2))
print('Topic 1.9: graphs, z-scores, hint/check/next/previous/reset, derivations, MathML, no-JS, print, responsive and HTTP checks passed.')
