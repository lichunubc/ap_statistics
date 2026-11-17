"""Native HTTP/Playwright checks for Topic 2.3 simulator, original practice and no-JS fallback."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import os,threading,json
ROOT=Path(__file__).resolve().parents[3];QA=ROOT/'qa';QA.mkdir(exist_ok=True)
remote=os.environ.get('SIM23_BASE_URL','').rstrip('/')
server=None
if remote:base=remote+'/'
else:
 class Quiet(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'docs')))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 base=f'http://127.0.0.1:{server.server_port}/'
url=base+quote('Unit 2/Topic 2.3/topic-2-3.html',safe='/')
errors=[];bad=[]
try:
 with sync_playwright() as p:
  kw={'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
  br=p.chromium.launch(headless=True,args=['--no-sandbox'],**kw)
  for width in (1440,768,390):
   context=br.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
   page=context.new_page()
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 and r.url.startswith(base) else None)
   response=page.goto(url,wait_until='networkidle',timeout=60000)
   assert response and response.ok
   assert page.locator('h1').inner_text().startswith('Topic 2.3 Estimating')
   panel=page.locator('[data-sim23]')
   assert panel.get_attribute('data-enhanced')=='true'
   assert panel.locator('[data-sim23-total]').inner_text()=='0'
   assert 'No trials yet' in panel.locator('[data-sim23-status]').inner_text()
   assert panel.locator('[data-sim23-share]').inner_text()=='—'
   panel.locator('[data-sim23-n="10"]').focus();page.keyboard.press('Enter')
   assert panel.locator('[data-sim23-total]').inner_text()=='10'
   assert panel.locator('[data-sim23-plot] svg').count()==1
   assert '10 completed' in panel.get_attribute('aria-label') if panel.get_attribute('aria-label') else True
   panel.locator('[data-sim23-n="100"]').click()
   assert panel.locator('[data-sim23-total]').inner_text()=='110'
   panel.locator('[data-sim23-reset]').click()
   assert panel.locator('[data-sim23-total]').inner_text()=='0'
   assert 'none yet' in panel.locator('[data-sim23-last]').inner_text()
   q=page.locator('.original-practice')
   q.locator('.original-question-title').wait_for(timeout=15000)
   assert q.locator('.original-question-title').inner_text()=='Question 1 of 8'
   assert q.locator('input:checked').count()==0
   q.locator('[data-action=check]').click()
   assert 'Choose an answer' in q.locator('.original-feedback').inner_text()
   q.locator('input[value=A]').check()
   q.locator('[data-action=check]').click()
   assert 'Correct' in q.locator('.original-feedback').inner_text()
   page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
   assert q.locator('.original-print-question').count()==8
   page.evaluate('window.dispatchEvent(new Event("afterprint"))')
   assert q.locator('.original-print-question').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2'),width
   context.close()
  context=br.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
  page=context.new_page();page.goto(url,wait_until='domcontentloaded')
  assert page.locator('.original-nojs li').count()==8
  assert 'No trials yet' in page.locator('[data-sim23-status]').inner_text()
  assert '505/1000' in page.locator('.sim23-static').inner_text()
  assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+2')
  context.close();br.close()
finally:
 if server:server.shutdown();server.server_close()
assert not errors,errors
assert not bad,bad
(QA/('live-sim23-browser.json' if remote else 'sim23-browser.json')).write_text(json.dumps({'viewports':[1440,768,390],'questions':8,'nojs':True},indent=2)+'\n')
print('Topic 2.3 browser, offline simulation and original practice checks passed.')
